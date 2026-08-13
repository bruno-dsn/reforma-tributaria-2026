# Fontes, método e rastreabilidade

## Data de corte

Legislação e páginas institucionais verificadas em 13 de agosto de 2026. Os
dados de inflação e os pesos mensais se referem a julho de 2026.

## Fontes legais

### Emenda Constitucional 132/2023

URL: https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm

Uso no projeto:

- ADCT, art. 125: ano-teste de 2026, com CBS de 0,9% e IBS de 0,1%;
- ADCT, arts. 126 e 127: etapa de 2027 e 2028;
- ADCT, art. 128: substituição gradual de ICMS e ISS entre 2029 e 2032;
- ADCT, art. 129: conclusão da transição em 2033.

### Lei Complementar 214/2025, texto atualizado

URL: https://www2.camara.leg.br/legin/fed/leicom/2025/leicomplementar-214-16-janeiro-2025-796905-normaatualizada-pl.html

Uso no projeto:

- art. 125 e Anexo I: Cesta Básica Nacional de Alimentos;
- art. 127: redução de 30% para profissões e condições listadas;
- arts. 128 a 142: grupos com redução de 60%;
- arts. 143 a 148: grupos com alíquota zero;
- anexos: delimitação por NCM ou NBS quando aplicável.

### Lei Complementar 227/2026

URL: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp227.htm

Uso no projeto: conferência das atualizações de 2026 e do ambiente institucional
do IBS.

### Receita Federal

URL: https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/programas-e-atividades/reforma-tributaria-do-consumo/entenda

Uso no projeto: explicação institucional da transição, dos tributos substituídos
e do ano-teste.

## Fontes estatísticas

### SIDRA, tabela 7060

Página: https://sidra.ibge.gov.br/tabela/7060

Consulta usada para os pesos de julho de 2026:

```text
https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/66/p/202607/c315/all
```

Filtros:

- território: Brasil;
- variável 66: IPCA, peso mensal;
- período: julho de 2026;
- classificação 315: geral, grupos, subgrupos, itens e subitens;
- recorte final: nove códigos de grupo.

### IPCA e INPC, julho de 2026

URL: https://biblioteca.ibge.gov.br/visualizacao/periodicos/236/inpc_ipca_2026_jul.pdf

Uso no projeto: IPCA mensal de 0,07%, acumulado no ano de 3,44%, acumulado em
12 meses de 4,44%, variações e impactos por grupo.

## Separação entre fato e cenário

Fatos oficiais são armazenados em CSV com fonte, período e base legal.
Simulações usam somente entradas do usuário e fórmulas explícitas.

O valor de 28% exibido inicialmente no simulador é uma hipótese ajustável para
demonstrar sensibilidade. Ele não é apresentado como alíquota-padrão oficial.

## Por que o IPCA não recebe uma regra tributária por grupo

Os grupos do IPCA são agregados estatísticos. A LC 214 trabalha com categorias,
condições e classificações NCM ou NBS. Dentro de Alimentação e bebidas, por
exemplo, podem coexistir itens da cesta básica com alíquota zero, alimentos com
redução de 60% e outros tratamentos.

Por isso, os pesos do IPCA aparecem como contexto real da composição do índice.
A simulação tributária usa uma cesta separada por categoria legal.

## Fórmulas

```text
alíquota efetiva = alíquota-padrão × (1 - redução / 100)
tributo nominal = base sem IBS/CBS × alíquota efetiva / 100
diferença nominal = tributo sem redução - tributo com tratamento
```

## Limites

Não são modelados:

- preço final e repasse ao consumidor;
- créditos da cadeia;
- carga atual de PIS, Cofins, ICMS, ISS e IPI;
- cashback;
- regimes específicos;
- enquadramento definitivo de produto ou serviço;
- alíquotas futuras definidas pelos entes.
