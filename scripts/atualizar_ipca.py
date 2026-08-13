"""Baixa pesos e variações dos grupos do IPCA pela API oficial do SIDRA."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
GRUPO = re.compile(r"^[1-9]\.\s*")


def consultar(variavel: int, periodo: str) -> list[dict[str, str]]:
    url = (
        "https://apisidra.ibge.gov.br/values/"
        f"t/7060/n1/all/v/{variavel}/p/{periodo}/c315/all"
    )
    with urlopen(url, timeout=30) as resposta:
        return json.load(resposta)[1:]


def grupos_por_codigo(linhas: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        linha["D4C"]: linha
        for linha in linhas
        if GRUPO.match(linha.get("D4N", ""))
    }


def main() -> None:
    periodo = sys.argv[1] if len(sys.argv) > 1 else "202607"
    if not re.fullmatch(r"\d{6}", periodo):
        raise SystemExit("Informe o período no formato AAAAMM, por exemplo 202607.")

    pesos = grupos_por_codigo(consultar(66, periodo))
    variacoes = grupos_por_codigo(consultar(63, periodo))
    if set(pesos) != set(variacoes) or len(pesos) != 9:
        raise RuntimeError("A estrutura retornada pelo SIDRA precisa ser revisada.")

    destino = ROOT / "data" / f"ipca_grupos_{periodo[:4]}_{periodo[4:]}.csv"
    with destino.open("w", encoding="utf-8", newline="") as arquivo:
        campos = [
            "codigo_sidra",
            "grupo",
            "peso_mensal_pct",
            "variacao_mensal_pct",
            "periodo",
            "fonte",
        ]
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        for codigo, linha in pesos.items():
            escritor.writerow(
                {
                    "codigo_sidra": codigo,
                    "grupo": GRUPO.sub("", linha["D4N"]),
                    "peso_mensal_pct": linha["V"],
                    "variacao_mensal_pct": variacoes[codigo]["V"],
                    "periodo": f"{periodo[:4]}-{periodo[4:]}",
                    "fonte": "IBGE, SIDRA, tabela 7060",
                }
            )
    print(f"Arquivo salvo: {destino}")


if __name__ == "__main__":
    main()
