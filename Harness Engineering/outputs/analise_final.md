# Analise final — Allura Finance

Periodo observado nas movimentacoes: 2025-01 a 2025-07.
Fontes: `data/gold/kpis_mensais.csv`, `mix_produto.csv`, `mix_canal.csv`, `receita_mensal.csv`, `status_snapshot.csv`, `data/silver/metas.csv`.

## 1) Captacao, resgate e captacao liquida por mes
Fonte: gold/kpis_mensais.csv

| ano_mes | captacao | resgate | clientes_movimentados | qtd_movimentos | captacao_liquida |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 240,709.83 | 519,723.03 | 19 | 21 | -279,013.20 |
| 2025-02 | 585,529.05 | 382,420.23 | 19 | 26 | 203,108.82 |
| 2025-03 | 548,662.31 | 794,471.73 | 23 | 32 | -245,809.42 |
| 2025-04 | 610,291.15 | 698,585.84 | 16 | 29 | -88,294.69 |
| 2025-05 | 561,334.88 | 546,083.50 | 20 | 29 | 15,251.38 |
| 2025-06 | 386,316.82 | 674,588.98 | 20 | 25 | -288,272.16 |
| 2025-07 | 389,676.10 | 356,005.16 | 14 | 18 | 33,670.94 |

Totais do periodo: captacao R$ 3.322.520,14 | resgate R$ 3.971.878,47 | liquida R$ -649.358,33.
Melhor mes liquido: 2025-02 (R$ 203.108,82).
Pior mes liquido: 2025-06 (R$ -288.272,16).
Meta mensal de captacao R$ 2.500.000,00: meses abaixo da meta = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'].
Meta mensal de captacao liquida R$ 1.300.000,00: meses abaixo = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'].

Fato observado: a serie mensal existe e e internamente consistente com o fato (somas batem).
Interpretacao: ha variacao forte entre meses; a meta mensal de captacao e apertada frente ao volume observado.

## 2) Quais produtos puxam o resultado?
Fonte: gold/mix_produto.csv

| produto | captacao | resgate | qtd | captacao_liquida |
| --- | --- | --- | --- | --- |
| Acoes Brasil | 959,467.17 | 778,098.27 | 37 | 181,368.90 |
| Tesouro Selic | 750,497.16 | 903,710.63 | 39 | -153,213.47 |
| Fundo DI | 648,791.27 | 817,564.30 | 34 | -168,773.03 |
| Renda Fixa Credito | 573,579.52 | 687,456.08 | 36 | -113,876.56 |
| Fundo Multimercado | 390,185.02 | 785,049.19 | 34 | -394,864.17 |

Produto com maior captacao: Acoes Brasil (R$ 959.467,17).
Produto com pior captacao liquida: Fundo Multimercado (R$ -394.864,17).

## 3) Quais canais se destacam?
Fonte: gold/mix_canal.csv

| canal | captacao | resgate | qtd | captacao_liquida |
| --- | --- | --- | --- | --- |
| Assessor | 1,376,523.08 | 1,426,863.44 | 75 | -50,340.36 |
| App | 1,229,330.59 | 1,839,757.69 | 69 | -610,427.10 |
| Parceiro | 716,666.47 | 705,257.34 | 36 | 11,409.13 |

Canal com maior captacao: Assessor (R$ 1.376.523,08).

## 4) Receita e churn/status vs meta
Fonte receita: gold/receita_mensal.csv
Fonte status: gold/status_snapshot.csv (snapshot, nao taxa mensal de churn)

Receita por mes:
| ano_mes | valor_receita |
| --- | --- |
| 2025-01 | 331,451.06 |
| 2025-02 | 272,993.45 |
| 2025-03 | 289,627.66 |
| 2025-04 | 345,647.88 |
| 2025-05 | 259,599.30 |
| 2025-06 | 346,073.90 |
| 2025-07 | 253,973.84 |

Receita total do periodo: R$ 2.099.367,09. Media mensal: R$ 299.909,58. Meta mensal de receita: R$ 180.000,00.
Meses com receita abaixo da meta: nenhum.

Status de clientes (snapshot Silver):
| status | qtd | pct |
| --- | --- | --- |
| inativo | 22 | 55.00 |
| ativo | 18 | 45.00 |

Inativos: 22 de 40 (55.0%).
Meta `churn_clientes_pct` = 3.0% ao mes: **sem evidencia** para taxa mensal de churn (nao ha data de inativacao nem painel longitudinal). O snapshot de inativos (55.0%) nao deve ser comparado diretamente a essa meta mensal.

## Insights acionaveis
1. Investigar o(s) mes(es) de pior captacao liquida (2025-06) com corte produto/canal — o fato permite esse recorte.
2. Priorizar o produto lider de captacao (Acoes Brasil) e revisar o de pior liquida (Fundo Multimercado) contra `meta_captacao_mes` do catalogo.
3. Concentrar acao comercial no canal Assessor, que concentra a maior captacao.

## Riscos / limites dos dados
1. Churn mensal nao e calculavel com o bronze atual (so status pontual).
2. Receita tem fee frequentemente `nao_informada` e havia produto inexistente no bronze (removido); receita e movimentacao nao compartilham a mesma granularidade de transacao.
3. Dados sao sinteticos/didaticos; PII foi hasheada, mas nomes permaneceram no dim_cliente para analise (nao sao CPF/email/telefone).

## Graficos sugeridos
1. Titulo: Captacao vs resgate vs liquida por mes. Eixos: X=ano_mes, Y=BRL. Mostra tendencia e meses abaixo da meta.
2. Titulo: Mix de captacao liquida por produto. Eixos: X=produto, Y=BRL. Mostra quem puxa o resultado.
3. Titulo: Receita mensal vs meta. Eixos: X=ano_mes, Y=BRL. Mostra alerta de receita.

Status: **OK**
