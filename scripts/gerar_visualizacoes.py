"""Gera imagens estáticas usadas no README.

Execute na raiz do projeto:
    python scripts/gerar_visualizacoes.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

AZUL = "#0E7490"
AZUL_ESCURO = "#0F3D4C"
VERDE = "#0F766E"
DOURADO = "#D97706"
TEXTO = "#172033"
CINZA = "#64748B"
FUNDO = "#F5F7FA"
GRADE = "#DCE4EA"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.titlesize": 16,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    }
)


def salvar(figura: plt.Figure, nome: str) -> None:
    figura.savefig(ASSETS / nome, dpi=180, bbox_inches="tight", facecolor=figura.get_facecolor())
    plt.close(figura)


def grafico_transicao(cronograma: pd.DataFrame) -> None:
    dados = cronograma.dropna(subset=["percentual_ibs_referencia"])
    fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")
    ax.plot(
        dados["ano"],
        dados["percentual_ibs_referencia"],
        marker="o",
        linewidth=3,
        markersize=8,
        color=AZUL,
        label="IBS sobre a referência",
    )
    ax.plot(
        dados["ano"],
        dados["percentual_icms_iss"],
        marker="o",
        linewidth=3,
        markersize=8,
        color=DOURADO,
        label="ICMS e ISS sobre as alíquotas vigentes",
    )
    ax.set_title("Transição estadual e municipal", loc="left", color=TEXTO, weight="bold")
    ax.set_ylabel("Participação na transição (%)")
    ax.set_xlabel("Ano")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", color=GRADE, linewidth=0.8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left")
    ax.text(
        0,
        -0.18,
        "Fonte: EC 132/2023, ADCT, art. 128. Os percentuais não são alíquotas finais ao consumidor.",
        transform=ax.transAxes,
        color=CINZA,
        fontsize=9,
    )
    salvar(fig, "transicao_2029_2033.png")


def grafico_ipca(ipca: pd.DataFrame) -> None:
    dados = ipca.sort_values("peso_mensal_pct")
    fig, ax = plt.subplots(figsize=(12, 6.4), facecolor="white")
    barras = ax.barh(dados["grupo"], dados["peso_mensal_pct"], color=VERDE, height=0.66)
    ax.bar_label(barras, fmt="%.2f%%", padding=5, color=TEXTO, fontsize=9)
    ax.set_title("Peso mensal dos grupos do IPCA", loc="left", color=TEXTO, weight="bold")
    ax.set_xlabel("Peso em julho de 2026 (%)")
    ax.set_xlim(0, 24)
    ax.grid(axis="x", color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.text(
        0,
        -0.14,
        "Fonte: IBGE, SIDRA, tabela 7060, Brasil. Os pesos somam 100%.",
        transform=ax.transAxes,
        color=CINZA,
        fontsize=9,
    )
    salvar(fig, "pesos_ipca_julho_2026.png")


def grafico_tratamentos(tratamentos: pd.DataFrame) -> None:
    resumo = (
        tratamentos.groupby(["tratamento", "reducao_pct"], as_index=False)
        .size()
        .sort_values("reducao_pct")
    )
    fig, ax = plt.subplots(figsize=(10.5, 5.7), facecolor="white")
    cores = [AZUL_ESCURO, DOURADO, AZUL, VERDE]
    barras = ax.bar(resumo["tratamento"], resumo["size"], color=cores[: len(resumo)], width=0.62)
    ax.bar_label(barras, padding=4, color=TEXTO, fontsize=11, weight="bold")
    ax.set_title("Categorias documentadas por tratamento", loc="left", color=TEXTO, weight="bold")
    ax.set_ylabel("Quantidade de categorias no catálogo")
    ax.grid(axis="y", color=GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="x", rotation=8)
    ax.text(
        0,
        -0.18,
        "Catálogo didático baseado na LC 214/2025. O enquadramento real exige artigo, anexo e classificação.",
        transform=ax.transAxes,
        color=CINZA,
        fontsize=9,
    )
    salvar(fig, "tratamentos_legais.png")


def card(ax: plt.Axes, x: float, y: float, largura: float, titulo: str, valor: str, detalhe: str) -> None:
    caixa = FancyBboxPatch(
        (x, y),
        largura,
        0.17,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes,
        linewidth=1,
        edgecolor="#D8E1E7",
        facecolor="white",
    )
    ax.add_patch(caixa)
    ax.text(x + 0.018, y + 0.128, titulo.upper(), transform=ax.transAxes, fontsize=8, color=CINZA, weight="bold")
    ax.text(x + 0.018, y + 0.067, valor, transform=ax.transAxes, fontsize=22, color=TEXTO, weight="bold")
    ax.text(x + 0.018, y + 0.025, detalhe, transform=ax.transAxes, fontsize=7.8, color=CINZA)


def preview(cronograma: pd.DataFrame, ipca: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(16, 9), facecolor=FUNDO)
    ax_fundo = fig.add_axes([0, 0, 1, 1])
    ax_fundo.set_axis_off()

    hero = FancyBboxPatch(
        (0.035, 0.77),
        0.93,
        0.18,
        boxstyle="round,pad=0.012,rounding_size=0.025",
        transform=ax_fundo.transAxes,
        linewidth=0,
        facecolor=AZUL_ESCURO,
    )
    ax_fundo.add_patch(hero)
    ax_fundo.text(0.065, 0.907, "DADOS PÚBLICOS E CENÁRIOS TRANSPARENTES", transform=ax_fundo.transAxes, fontsize=9, color="#A5F3FC", weight="bold")
    ax_fundo.text(0.065, 0.85, "Observatório da Reforma Tributária", transform=ax_fundo.transAxes, fontsize=28, color="white", weight="bold")
    ax_fundo.text(0.065, 0.805, "Cronograma oficial, tratamentos da LC 214 e simulador educacional com limites explícitos.", transform=ax_fundo.transAxes, fontsize=11, color="#D9F3F5")

    card(ax_fundo, 0.045, 0.56, 0.21, "CBS no ano-teste", "0,9%", "Incidência nominal em 2026")
    card(ax_fundo, 0.275, 0.56, 0.21, "IBS no ano-teste", "0,1%", "Etapa inicial de implantação")
    card(ax_fundo, 0.505, 0.56, 0.21, "Conclusão", "2033", "Novo sistema integral")
    card(ax_fundo, 0.735, 0.56, 0.21, "IPCA 12 meses", "4,44%", "Até julho de 2026")

    ax1 = fig.add_axes([0.06, 0.11, 0.41, 0.36], facecolor="white")
    dados_t = cronograma.dropna(subset=["percentual_ibs_referencia"])
    ax1.plot(dados_t["ano"], dados_t["percentual_ibs_referencia"], color=AZUL, marker="o", linewidth=2.8, label="IBS")
    ax1.plot(dados_t["ano"], dados_t["percentual_icms_iss"], color=DOURADO, marker="o", linewidth=2.8, label="ICMS e ISS")
    ax1.set_title("Transição 2029 a 2033", loc="left", fontsize=13, weight="bold", color=TEXTO)
    ax1.set_ylim(0, 105)
    ax1.set_xticks(dados_t["ano"])
    ax1.set_ylabel("Participação (%)", fontsize=9)
    ax1.grid(axis="y", color=GRADE)
    ax1.spines[["top", "right", "left"]].set_visible(False)
    ax1.legend(frameon=False, fontsize=8, loc="upper left")

    ax2 = fig.add_axes([0.55, 0.11, 0.39, 0.36], facecolor="white")
    maiores = ipca.nlargest(5, "peso_mensal_pct").sort_values("peso_mensal_pct")
    ax2.barh(maiores["grupo"], maiores["peso_mensal_pct"], color=VERDE, height=0.62)
    ax2.set_title("Maiores pesos do IPCA", loc="left", fontsize=13, weight="bold", color=TEXTO)
    ax2.set_xlabel("Peso em julho de 2026 (%)", fontsize=9)
    ax2.grid(axis="x", color=GRADE)
    ax2.set_axisbelow(True)
    ax2.spines[["top", "right", "left"]].set_visible(False)

    ax_fundo.text(0.06, 0.04, "Fontes: EC 132/2023, LC 214/2025 atualizada, Receita Federal e IBGE/SIDRA.", transform=ax_fundo.transAxes, fontsize=8.5, color=CINZA)
    salvar(fig, "preview.png")


def main() -> None:
    cronograma = pd.read_csv(DATA / "cronograma_transicao.csv")
    tratamentos = pd.read_csv(DATA / "tratamentos_legais.csv")
    ipca = pd.read_csv(DATA / "ipca_grupos_2026_07.csv")
    grafico_transicao(cronograma)
    grafico_ipca(ipca)
    grafico_tratamentos(tratamentos)
    preview(cronograma, ipca)
    print(f"Imagens salvas em {ASSETS}")


if __name__ == "__main__":
    main()
