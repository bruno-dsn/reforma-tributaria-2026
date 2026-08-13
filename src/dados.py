"""Leitura e validação dos dados usados no painel."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@lru_cache(maxsize=None)
def _ler_csv(nome: str) -> pd.DataFrame:
    caminho = DATA_DIR / nome
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {caminho}")
    return pd.read_csv(caminho)


def carregar_cronograma() -> pd.DataFrame:
    return _ler_csv("cronograma_transicao.csv").copy()


def carregar_tratamentos() -> pd.DataFrame:
    dados = _ler_csv("tratamentos_legais.csv").copy()
    esperadas = {
        "setor",
        "categoria",
        "tratamento",
        "reducao_pct",
        "fator_aliquota",
        "base_legal",
    }
    if not esperadas.issubset(dados.columns):
        raise ValueError("A base de tratamentos legais está incompleta.")
    return dados


def carregar_ipca_grupos() -> pd.DataFrame:
    dados = _ler_csv("ipca_grupos_2026_07.csv").copy()
    soma = float(dados["peso_mensal_pct"].sum())
    if abs(soma - 100) > 0.01:
        raise ValueError("Os pesos mensais do IPCA não somam 100%.")
    return dados


def carregar_indicadores_ipca() -> pd.DataFrame:
    return _ler_csv("indicadores_ipca_2026_07.csv").copy()


def carregar_cesta_exemplo() -> pd.DataFrame:
    return _ler_csv("cesta_familiar_exemplo.csv").copy()
