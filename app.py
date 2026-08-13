"""Observatório interativo da Reforma Tributária do Consumo.

Execute com: streamlit run app.py
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from src.calculos import (
    aliquota_efetiva,
    calcular_cesta,
    calcular_teste_2026,
    tributo_nominal,
)
from src.dados import (
    carregar_cesta_exemplo,
    carregar_cronograma,
    carregar_indicadores_ipca,
    carregar_ipca_grupos,
    carregar_tratamentos,
)


st.set_page_config(
    page_title="Observatório da Reforma Tributária",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


CORES = {
    "azul": "#164E63",
    "azul_claro": "#0E7490",
    "verde": "#0F766E",
    "dourado": "#D97706",
    "texto": "#172033",
    "cinza": "#64748B",
    "fundo": "#F5F7FA",
}


def aplicar_estilo() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #F5F7FA; }
        [data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E2E8F0; }
        .block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1450px; }
        .hero {
            background: linear-gradient(115deg, #0F3D4C 0%, #0E7490 62%, #0F766E 100%);
            padding: 2rem 2.2rem;
            border-radius: 22px;
            color: white;
            box-shadow: 0 18px 50px rgba(15, 61, 76, .16);
            margin-bottom: 1rem;
        }
        .hero h1 { margin: 0 0 .45rem 0; font-size: 2.25rem; line-height: 1.12; color: white; }
        .hero p { margin: 0; max-width: 890px; font-size: 1.02rem; color: #D9F3F5; }
        .eyebrow { letter-spacing: .11em; text-transform: uppercase; font-size: .74rem; font-weight: 750; color: #A5F3FC; margin-bottom: .55rem; }
        .card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 1.05rem 1.15rem;
            min-height: 126px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, .045);
        }
        .card .label { font-size: .78rem; color: #64748B; text-transform: uppercase; letter-spacing: .05em; }
        .card .value { font-size: 1.8rem; color: #172033; font-weight: 760; margin: .22rem 0; }
        .card .detail { font-size: .84rem; color: #64748B; line-height: 1.35; }
        .callout {
            background: #ECFEFF;
            color: #164E63;
            border-left: 4px solid #0891B2;
            padding: .9rem 1rem;
            border-radius: 0 12px 12px 0;
            margin: .7rem 0 1rem 0;
        }
        .warning {
            background: #FFF7ED;
            color: #9A3412;
            border-left: 4px solid #F59E0B;
            padding: .9rem 1rem;
            border-radius: 0 12px 12px 0;
            margin: .7rem 0 1rem 0;
        }
        .source-box {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: .9rem 1rem;
            font-size: .87rem;
            color: #475569;
        }
        .stTabs [data-baseweb="tab-list"] { gap: .4rem; }
        .stTabs [data-baseweb="tab"] { height: 48px; border-radius: 10px 10px 0 0; padding: 0 1rem; }
        div[data-testid="stMetric"] { background: white; border: 1px solid #E2E8F0; padding: .85rem; border-radius: 14px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def card(rotulo: str, valor: str, detalhe: str) -> None:
    st.markdown(
        f"""
        <div class="card">
            <div class="label">{rotulo}</div>
            <div class="value">{valor}</div>
            <div class="detail">{detalhe}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def titulo_secao(titulo: str, texto: str) -> None:
    st.subheader(titulo)
    st.caption(texto)


aplicar_estilo()

cronograma = carregar_cronograma()
tratamentos = carregar_tratamentos()
ipca = carregar_ipca_grupos()
indicadores_ipca = carregar_indicadores_ipca()
cesta_exemplo = carregar_cesta_exemplo()


with st.sidebar:
    st.markdown("### Guia rápido")
    st.markdown(
        """
        **Fato oficial**  
        Texto retirado da Constituição, da lei ou de base oficial.

        **Cenário ajustável**  
        Conta educacional feita com valores escolhidos pelo usuário.
        """
    )
    st.divider()
    st.markdown("### Recorte dos dados")
    st.write("Legislação verificada em 13/08/2026")
    st.write("IPCA Brasil de julho de 2026")
    st.write("Pesos mensais da tabela SIDRA 7060")
    st.divider()
    st.warning(
        "O painel não substitui orientação contábil ou jurídica e não estima preços futuros."
    )


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Dados públicos, regras rastreáveis e cenários transparentes</div>
        <h1>Observatório da Reforma Tributária do Consumo</h1>
        <p>
            Entenda o que muda entre 2026 e 2033, consulte tratamentos previstos na
            LC 214 e teste contas nominais sem confundir hipótese com resultado oficial.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

abas = st.tabs(
    [
        "Visão geral",
        "Transição 2026 a 2033",
        "Tratamentos legais",
        "Cesta familiar",
        "Dados e método",
    ]
)


with abas[0]:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card("CBS no ano-teste", "0,9%", "Incidência nominal prevista para 2026.")
    with col2:
        card("IBS no ano-teste", "0,1%", "Soma das parcelas estadual e municipal em 2026.")
    with col3:
        card("Conclusão da transição", "2033", "Ano de vigência integral do novo sistema.")
    with col4:
        card("IPCA em 12 meses", "4,44%", "Resultado oficial até julho de 2026.")

    st.markdown(
        """
        <div class="callout">
        <strong>Leitura correta de 2026:</strong> 0,9% de CBS e 0,1% de IBS formam
        uma etapa de teste. Esses números não representam a futura alíquota-padrão
        combinada do sistema.
        </div>
        """,
        unsafe_allow_html=True,
    )

    esquerda, direita = st.columns([1.05, 1])
    with esquerda:
        titulo_secao(
            "O que muda",
            "Uma tradução direta dos principais conceitos usados no painel.",
        )
        conceitos = [
            ("CBS", "Tributo federal sobre bens e serviços."),
            ("IBS", "Tributo compartilhado por estados, Distrito Federal e municípios."),
            ("Imposto Seletivo", "Tributo federal sobre bens e serviços prejudiciais à saúde ou ao meio ambiente, conforme regulamentação."),
            ("Não cumulatividade", "Créditos buscam evitar a cobrança em cascata ao longo da cadeia."),
            ("Destino", "A arrecadação acompanha, em regra, o local do consumo."),
        ]
        for nome, explicacao in conceitos:
            st.markdown(f"**{nome}**  ")
            st.write(explicacao)

    with direita:
        titulo_secao(
            "IPCA no último mês disponível",
            "Indicadores oficiais do IBGE para julho de 2026.",
        )
        grafico_indicadores = alt.Chart(indicadores_ipca).mark_bar(
            cornerRadiusTopRight=6,
            cornerRadiusBottomRight=6,
            color=CORES["azul_claro"],
        ).encode(
            y=alt.Y("indicador:N", sort=None, title=None),
            x=alt.X("valor_pct:Q", title="Percentual"),
            tooltip=["indicador", alt.Tooltip("valor_pct:Q", format=".2f", title="Valor (%)")],
        ).properties(height=240)
        st.altair_chart(grafico_indicadores, use_container_width=True)
        st.caption(
            "O IPCA descreve variação de preços. Ele não mede diretamente a carga do IBS e da CBS."
        )


with abas[1]:
    titulo_secao(
        "Cronograma oficial",
        "A transição não acontece de uma vez. Cada linha mostra uma etapa distinta.",
    )
    selecao_ano = st.select_slider(
        "Escolha um ano para ler a etapa",
        options=cronograma["ano"].tolist(),
        value=2026,
    )
    linha = cronograma.loc[cronograma["ano"] == selecao_ano].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Fase", linha["fase"])
    c2.metric("CBS", linha["cbs"])
    c3.metric("IBS", linha["ibs"])
    st.info(linha["leitura_simples"])
    st.caption(f"Base legal: {linha['base_legal']}")

    transicao = cronograma.dropna(subset=["percentual_ibs_referencia"]).copy()
    transicao_longa = transicao.melt(
        id_vars="ano",
        value_vars=["percentual_ibs_referencia", "percentual_icms_iss"],
        var_name="sistema",
        value_name="participacao_pct",
    )
    transicao_longa["sistema"] = transicao_longa["sistema"].map(
        {
            "percentual_ibs_referencia": "IBS sobre a referência",
            "percentual_icms_iss": "ICMS e ISS sobre as alíquotas vigentes",
        }
    )
    grafico_transicao = alt.Chart(transicao_longa).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("ano:O", title="Ano"),
        y=alt.Y("participacao_pct:Q", title="Participação na transição (%)", scale=alt.Scale(domain=[0, 100])),
        color=alt.Color(
            "sistema:N",
            title=None,
            scale=alt.Scale(range=[CORES["azul_claro"], CORES["dourado"]]),
        ),
        tooltip=["ano", "sistema", alt.Tooltip("participacao_pct:Q", format=".0f", title="Percentual")],
    ).properties(height=350)
    st.altair_chart(grafico_transicao, use_container_width=True)
    st.caption(
        "De 2029 a 2032, os percentuais mostram a proporção da referência do IBS e a redução proporcional de ICMS e ISS. Não são alíquotas finais ao consumidor."
    )

    with st.expander("Testar a conta nominal de 2026"):
        base_2026 = st.number_input(
            "Base da operação para a demonstração",
            min_value=0.0,
            value=10000.0,
            step=500.0,
            help="Valor antes dos tributos usado apenas para demonstrar 0,9% de CBS e 0,1% de IBS.",
        )
        teste = calcular_teste_2026(base_2026)
        t1, t2, t3 = st.columns(3)
        t1.metric("CBS nominal", moeda(teste["cbs"]))
        t2.metric("IBS nominal", moeda(teste["ibs"]))
        t3.metric("Total nominal", moeda(teste["total"]))
        st.warning(
            "A EC 132 prevê regras de compensação e dispensa condicionada para o ano-teste. Esta conta mostra somente a incidência nominal."
        )


with abas[2]:
    titulo_secao(
        "Mapa de tratamentos previstos em lei",
        "Filtre o catálogo e confira sempre o artigo e o anexo antes de classificar um item real.",
    )
    f1, f2 = st.columns([1, 1])
    setores = ["Todos"] + sorted(tratamentos["setor"].unique().tolist())
    setor = f1.selectbox("Setor", setores)
    tipo = f2.selectbox(
        "Tipo de tratamento",
        ["Todos", "Alíquota-padrão", "Redução de 30%", "Redução de 60%", "Alíquota zero"],
    )

    filtrados = tratamentos.copy()
    if setor != "Todos":
        filtrados = filtrados.loc[filtrados["setor"] == setor]
    if tipo != "Todos":
        filtrados = filtrados.loc[filtrados["tratamento"] == tipo]

    st.dataframe(
        filtrados[["setor", "categoria", "tratamento", "base_legal", "anexo"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "setor": "Setor",
            "categoria": "Categoria legal",
            "tratamento": "Tratamento",
            "base_legal": "Base legal",
            "anexo": "Anexo",
        },
    )

    st.divider()
    titulo_secao(
        "Calculadora de uma categoria legal",
        "A alíquota-padrão é uma hipótese escolhida por você. O projeto não apresenta uma taxa final oficial.",
    )
    c1, c2, c3 = st.columns([1.3, 1, 1])
    categoria = c1.selectbox("Categoria", tratamentos["categoria"].tolist())
    aliquota_padrao = c2.number_input(
        "Alíquota-padrão hipotética (%)",
        min_value=0.0,
        max_value=40.0,
        value=28.0,
        step=0.1,
    )
    base_categoria = c3.number_input(
        "Base sem IBS e CBS",
        min_value=0.0,
        value=1000.0,
        step=100.0,
    )
    regra = tratamentos.loc[tratamentos["categoria"] == categoria].iloc[0]
    efetiva = aliquota_efetiva(aliquota_padrao, regra["reducao_pct"])
    valor_tributo = tributo_nominal(base_categoria, aliquota_padrao, regra["reducao_pct"])
    r1, r2, r3 = st.columns(3)
    r1.metric("Redução prevista", f"{regra['reducao_pct']:.0f}%")
    r2.metric("Alíquota efetiva no cenário", f"{efetiva:.2f}%")
    r3.metric("Tributo nominal no cenário", moeda(valor_tributo))
    st.info(f"{regra['explicacao']} Base legal: {regra['base_legal']}.")


with abas[3]:
    titulo_secao(
        "Composição de referência do consumo",
        "Os pesos abaixo são oficiais do IPCA Brasil de julho de 2026. Eles não equivalem às categorias tributárias da LC 214.",
    )
    grafico_pesos = alt.Chart(ipca.sort_values("peso_mensal_pct")).mark_bar(
        cornerRadiusTopRight=5,
        cornerRadiusBottomRight=5,
        color=CORES["verde"],
    ).encode(
        y=alt.Y("grupo:N", sort="-x", title=None),
        x=alt.X("peso_mensal_pct:Q", title="Peso mensal no IPCA (%)"),
        tooltip=["grupo", alt.Tooltip("peso_mensal_pct:Q", format=".2f", title="Peso (%)")],
    ).properties(height=330)
    st.altair_chart(grafico_pesos, use_container_width=True)
    st.caption(
        "Fonte: IBGE, SIDRA, tabela 7060. Os nove grupos somam 100% do índice no mês de referência."
    )

    st.markdown(
        """
        <div class="warning">
        <strong>Por que o simulador não aplica uma taxa a cada grupo do IPCA?</strong>
        Um grupo como Alimentação reúne produtos com alíquota zero, redução de 60%
        e possíveis situações de alíquota-padrão. A lei classifica itens por NCM, NBS,
        artigo e anexo. Aplicar uma regra única ao grupo inteiro produziria uma resposta enganosa.
        </div>
        """,
        unsafe_allow_html=True,
    )

    titulo_secao(
        "Cesta familiar hipotética por categoria legal",
        "Edite somente os valores. A comparação mede o efeito nominal dos tratamentos, não a diferença entre o sistema atual e o futuro.",
    )
    aliquota_cesta = st.slider(
        "Alíquota-padrão hipotética usada no cenário",
        min_value=0.0,
        max_value=40.0,
        value=28.0,
        step=0.5,
        help="Valor ajustável para análise de sensibilidade. Não é uma alíquota final oficial.",
    )
    cesta_editada = st.data_editor(
        cesta_exemplo,
        hide_index=True,
        use_container_width=True,
        disabled=["categoria_legal", "reducao_pct", "observacao"],
        column_config={
            "categoria_legal": "Categoria legal do exemplo",
            "valor_base_mensal": st.column_config.NumberColumn(
                "Valor mensal antes de IBS/CBS",
                min_value=0.0,
                step=50.0,
                format="R$ %.2f",
            ),
            "reducao_pct": st.column_config.NumberColumn("Redução (%)", format="%.0f%%"),
            "observacao": "Limite da classificação",
        },
        key="editor_cesta",
    )
    resultado_cesta, resumo = calcular_cesta(cesta_editada, aliquota_cesta)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Base mensal do exemplo", moeda(resumo["base_total"]))
    m2.metric("Sem reduções", moeda(resumo["tributo_sem_reducao"]))
    m3.metric("Com tratamentos", moeda(resumo["tributo_com_tratamento"]))
    m4.metric("Diferença nominal", moeda(resumo["diferenca_nominal"]))

    comparacao = resultado_cesta.melt(
        id_vars="categoria_legal",
        value_vars=["tributo_sem_reducao", "tributo_com_tratamento"],
        var_name="cenario",
        value_name="valor",
    )
    comparacao["cenario"] = comparacao["cenario"].map(
        {
            "tributo_sem_reducao": "Sem redução",
            "tributo_com_tratamento": "Com tratamento legal",
        }
    )
    grafico_cesta = alt.Chart(comparacao).mark_bar().encode(
        y=alt.Y("categoria_legal:N", sort="-x", title=None),
        x=alt.X("valor:Q", title="Tributo nominal no cenário (R$)"),
        color=alt.Color(
            "cenario:N",
            title=None,
            scale=alt.Scale(range=[CORES["dourado"], CORES["azul_claro"]]),
        ),
        yOffset="cenario:N",
        tooltip=["categoria_legal", "cenario", alt.Tooltip("valor:Q", format=".2f", title="Valor (R$)")],
    ).properties(height=370)
    st.altair_chart(grafico_cesta, use_container_width=True)
    st.caption(
        "Interpretação: a diferença decorre apenas das reduções informadas na cesta e da alíquota hipotética selecionada. Não incorpora créditos, cashback, regimes específicos, preços ou comportamento das empresas."
    )


with abas[4]:
    titulo_secao(
        "Método auditável",
        "Cada resultado pode ser conferido pela fórmula e pela fonte que o sustenta.",
    )
    metodo1, metodo2 = st.columns(2)
    with metodo1:
        st.markdown("#### Fórmulas usadas")
        st.code(
            """alíquota efetiva = alíquota-padrão × (1 - redução / 100)

tributo nominal = base sem IBS/CBS × alíquota efetiva / 100

diferença nominal = tributo sem redução - tributo com tratamento""",
            language="text",
        )
        st.markdown("#### O que o painel não calcula")
        st.markdown(
            """
            - preço final ao consumidor;
            - carga atual por produto ou empresa;
            - créditos ao longo da cadeia;
            - cashback para famílias de baixa renda;
            - enquadramento definitivo de NCM ou NBS;
            - alíquota-padrão futura oficial.
            """
        )
    with metodo2:
        st.markdown("#### Fontes primárias")
        st.markdown(
            """
            - [Emenda Constitucional 132/2023](https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm)
            - [Lei Complementar 214/2025, texto atualizado](https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-normaatualizada-pl.html)
            - [Lei Complementar 227/2026](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp227.htm)
            - [Receita Federal, entenda a reforma](https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/entenda)
            - [IBGE, tabela SIDRA 7060](https://sidra.ibge.gov.br/tabela/7060)
            - [IBGE, IPCA e INPC de julho de 2026](https://biblioteca.ibge.gov.br/visualizacao/periodicos/236/inpc_ipca_2026_jul.pdf)
            """
        )
        st.markdown("#### Baixar bases usadas")
        st.download_button(
            "Baixar cronograma em CSV",
            cronograma.to_csv(index=False).encode("utf-8-sig"),
            file_name="cronograma_reforma_tributaria.csv",
            mime="text/csv",
        )
        st.download_button(
            "Baixar tratamentos em CSV",
            tratamentos.to_csv(index=False).encode("utf-8-sig"),
            file_name="tratamentos_lc214.csv",
            mime="text/csv",
        )
        st.download_button(
            "Baixar pesos do IPCA em CSV",
            ipca.to_csv(index=False).encode("utf-8-sig"),
            file_name="pesos_ipca_2026_07.csv",
            mime="text/csv",
        )

    st.markdown(
        """
        <div class="source-box">
        <strong>Última verificação:</strong> 13 de agosto de 2026.<br>
        A legislação pode receber regulamentações e alterações. Antes de usar uma
        classificação em situação real, consulte o texto atualizado, os anexos e um profissional habilitado.
        </div>
        """,
        unsafe_allow_html=True,
    )
