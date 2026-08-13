import pandas as pd
import pytest

from src.calculos import (
    aliquota_efetiva,
    calcular_cesta,
    calcular_teste_2026,
    distribuir_por_pesos,
    tributo_nominal,
)


@pytest.mark.parametrize(
    ("aliquota", "reducao", "esperado"),
    [(28, 0, 28), (28, 30, 19.6), (28, 60, 11.2), (28, 100, 0)],
)
def test_aliquota_efetiva(aliquota, reducao, esperado):
    assert aliquota_efetiva(aliquota, reducao) == pytest.approx(esperado)


def test_aliquota_rejeita_reducao_maior_que_cem():
    with pytest.raises(ValueError):
        aliquota_efetiva(28, 101)


def test_tributo_nominal():
    assert tributo_nominal(1_000, 28, 60) == pytest.approx(112)


def test_teste_2026_separa_cbs_e_ibs():
    resultado = calcular_teste_2026(10_000)
    assert resultado["cbs"] == pytest.approx(90)
    assert resultado["ibs"] == pytest.approx(10)
    assert resultado["total"] == pytest.approx(100)


def test_distribuicao_por_pesos_preserva_total():
    valores = distribuir_por_pesos(5_000, [20, 30, 50])
    assert valores == pytest.approx([1_000, 1_500, 2_500])
    assert sum(valores) == pytest.approx(5_000)


def test_distribuicao_rejeita_pesos_incompletos():
    with pytest.raises(ValueError):
        distribuir_por_pesos(5_000, [20, 30])


def test_calculo_da_cesta_compara_cenarios():
    cesta = pd.DataFrame(
        {
            "categoria_legal": ["zero", "reduzida", "padrao"],
            "valor_base_mensal": [100, 100, 100],
            "reducao_pct": [100, 60, 0],
        }
    )
    resultado, resumo = calcular_cesta(cesta, 20)
    assert resultado["aliquota_efetiva_pct"].tolist() == pytest.approx([0, 8, 20])
    assert resumo["tributo_sem_reducao"] == pytest.approx(60)
    assert resumo["tributo_com_tratamento"] == pytest.approx(28)
    assert resumo["diferenca_nominal"] == pytest.approx(32)


def test_calculo_da_cesta_rejeita_valor_negativo():
    cesta = pd.DataFrame({"valor_base_mensal": [-1], "reducao_pct": [0]})
    with pytest.raises(ValueError):
        calcular_cesta(cesta, 20)
