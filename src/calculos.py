"""Cálculos transparentes usados pelo aplicativo.

O módulo não tenta reproduzir toda a apuração do IBS e da CBS. Ele calcula
apenas cenários nominais sobre uma base informada pelo usuário. Essa separação
deixa claro o que é regra legal e o que é hipótese de análise.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def _validar_nao_negativo(valor: float, nome: str) -> float:
    numero = float(valor)
    if numero < 0:
        raise ValueError(f"{nome} não pode ser negativo.")
    return numero


def aliquota_efetiva(aliquota_padrao_pct: float, reducao_pct: float) -> float:
    """Retorna a alíquota após aplicar uma redução prevista em lei.

    Exemplo: alíquota-padrão de 28% com redução de 60% resulta em 11,2%.
    """

    aliquota = _validar_nao_negativo(aliquota_padrao_pct, "A alíquota-padrão")
    reducao = _validar_nao_negativo(reducao_pct, "A redução")
    if reducao > 100:
        raise ValueError("A redução não pode ultrapassar 100%.")
    return aliquota * (1 - reducao / 100)


def tributo_nominal(
    base_sem_tributo: float,
    aliquota_padrao_pct: float,
    reducao_pct: float = 0,
) -> float:
    """Calcula IBS + CBS nominais sobre uma base sem esses tributos."""

    base = _validar_nao_negativo(base_sem_tributo, "A base")
    efetiva = aliquota_efetiva(aliquota_padrao_pct, reducao_pct)
    return base * efetiva / 100


def calcular_teste_2026(base_compensavel: float) -> dict[str, float]:
    """Separa a incidência nominal do ano-teste: CBS 0,9% e IBS 0,1%."""

    base = _validar_nao_negativo(base_compensavel, "A base")
    cbs = base * 0.009
    ibs = base * 0.001
    return {"base": base, "cbs": cbs, "ibs": ibs, "total": cbs + ibs}


def distribuir_por_pesos(
    valor_total: float,
    pesos_pct: Iterable[float],
) -> list[float]:
    """Distribui um valor segundo pesos percentuais que somam 100%."""

    total = _validar_nao_negativo(valor_total, "O valor total")
    pesos = [float(peso) for peso in pesos_pct]
    if not pesos:
        raise ValueError("A lista de pesos não pode estar vazia.")
    if any(peso < 0 for peso in pesos):
        raise ValueError("Os pesos não podem ser negativos.")
    if abs(sum(pesos) - 100) > 0.05:
        raise ValueError("Os pesos precisam somar aproximadamente 100%.")
    return [total * peso / 100 for peso in pesos]


def calcular_cesta(
    cesta: pd.DataFrame,
    aliquota_padrao_pct: float,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Compara alíquota cheia e tratamentos em uma cesta hipotética.

    O DataFrame deve conter `valor_base_mensal` e `reducao_pct`.
    """

    obrigatorias = {"valor_base_mensal", "reducao_pct"}
    ausentes = obrigatorias.difference(cesta.columns)
    if ausentes:
        raise ValueError(f"Colunas ausentes: {', '.join(sorted(ausentes))}")

    resultado = cesta.copy()
    resultado["valor_base_mensal"] = pd.to_numeric(
        resultado["valor_base_mensal"], errors="raise"
    )
    resultado["reducao_pct"] = pd.to_numeric(
        resultado["reducao_pct"], errors="raise"
    )

    if (resultado["valor_base_mensal"] < 0).any():
        raise ValueError("Os valores da cesta não podem ser negativos.")
    if ((resultado["reducao_pct"] < 0) | (resultado["reducao_pct"] > 100)).any():
        raise ValueError("As reduções da cesta precisam estar entre 0% e 100%.")

    aliquota = _validar_nao_negativo(aliquota_padrao_pct, "A alíquota-padrão")
    resultado["aliquota_efetiva_pct"] = resultado["reducao_pct"].map(
        lambda reducao: aliquota_efetiva(aliquota, reducao)
    )
    resultado["tributo_sem_reducao"] = (
        resultado["valor_base_mensal"] * aliquota / 100
    )
    resultado["tributo_com_tratamento"] = (
        resultado["valor_base_mensal"]
        * resultado["aliquota_efetiva_pct"]
        / 100
    )
    resultado["diferenca_nominal"] = (
        resultado["tributo_sem_reducao"]
        - resultado["tributo_com_tratamento"]
    )

    resumo = {
        "base_total": float(resultado["valor_base_mensal"].sum()),
        "tributo_sem_reducao": float(resultado["tributo_sem_reducao"].sum()),
        "tributo_com_tratamento": float(
            resultado["tributo_com_tratamento"].sum()
        ),
        "diferenca_nominal": float(resultado["diferenca_nominal"].sum()),
    }
    return resultado, resumo
