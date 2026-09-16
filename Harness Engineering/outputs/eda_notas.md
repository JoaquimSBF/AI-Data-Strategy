# EDA — notas e graficos (rascunho)

Complemento de `outputs/analise_final.md`. Nao substitui o documento principal.

## Recortes que o Gold nao traz prontos
- Mes x produto e mes x canal: usar `data/gold/base_analise.csv` ou `fato_movimentacoes.csv` se a turma quiser aprofundar jan/mar/jun e o canal App.
- Churn mensal: nao calcular a partir de `status_snapshot`.

## Como montar os 3 graficos
1. Linhas: captacao, resgate, captacao_liquida por `ano_mes`; linhas horizontais nas metas 2.500.000 / 1.200.000 / 1.300.000.
2. Barras: `captacao_liquida` por produto.
3. Barras: `valor_receita` por mes + linha na meta 180.000.
