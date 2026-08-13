import pytest

from src.dados import (
    carregar_cronograma,
    carregar_ipca_grupos,
    carregar_tratamentos,
)


def test_cronograma_cobre_toda_a_transicao():
    dados = carregar_cronograma()
    assert dados["ano"].tolist() == list(range(2026, 2034))


def test_transicao_termina_com_ibs_integral_e_legados_zerados():
    dados = carregar_cronograma().set_index("ano")
    assert dados.loc[2033, "percentual_ibs_referencia"] == 100
    assert dados.loc[2033, "percentual_icms_iss"] == 0


def test_pesos_do_ipca_somam_cem():
    dados = carregar_ipca_grupos()
    assert dados["peso_mensal_pct"].sum() == pytest.approx(100, abs=0.001)


def test_ipca_tem_nove_grupos():
    assert len(carregar_ipca_grupos()) == 9


def test_tratamentos_tem_rastreabilidade_legal():
    dados = carregar_tratamentos()
    assert dados["base_legal"].notna().all()
    assert set(dados["reducao_pct"].unique()).issubset({0, 30, 60, 100})


def test_cesta_basica_aponta_artigo_e_anexo():
    dados = carregar_tratamentos().set_index("id")
    assert "art. 125" in dados.loc["cesta_basica", "base_legal"]
    assert dados.loc["cesta_basica", "anexo"] == "Anexo I"
