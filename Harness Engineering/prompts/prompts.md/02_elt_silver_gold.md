# MODO: ELT / GOLD (medalhao + estrela)

Entrada: tabelas ja limpas (Silver) da etapa anterior.
Objetivo: materializar modelo analitico em estrela para negocio/IA.

Tarefa:
1) Proponha dimensoes: dim_cliente, dim_produto, dim_canal.
2) Proponha fato: fato_movimentacoes (com valor_captacao e valor_resgate).
3) Proponha base_analise (planilha unica: fato + dims).
4) Proponha kpis_mensais (ano_mes, captacao, resgate, captacao_liquida, clientes_movimentados, qtd_movimentos).
5) Inclua mix_produto e mix_canal.
6) Inclua receita_mensal e snapshot de churn/status a partir de Silver, se houver dado.
7) Escreva o SQL (DuckDB) de cada objeto Gold, ou equivalente em passos pandas se eu pedir.
8) Liste testes de integridade: fato nao vazio, base_analise alinhada ao fato, sem PII, chaves ok.
9) Entregue CSVs (ou tabelas Markdown convertiveis) de cada artefato Gold.

Formato de saida:
- Diagrama textual da estrela
- SQL/passos por tabela Gold
- Exemplos (5 linhas) de base_analise e kpis_mensais
- Testes: PASS/FAIL esperados
- Status: OK ou NOK

Use apenas colunas existentes no Silver. Se algo nao der para calcular, diga.

Silver:
<<<
[COLE SILVER / RESUMO + AMOSTRAS]
>>>

## ONDE SALVAR
Salve manualmente em:

- `data/gold/`
  - dim_cliente.csv
  - dim_produto.csv
  - dim_canal.csv
  - fato_movimentacoes.csv
  - base_analise.csv
  - kpis_mensais.csv
  - mix_produto.csv
  - mix_canal.csv

- `outputs/elt_relatorio.md` -> diagrama, SQL e testes
