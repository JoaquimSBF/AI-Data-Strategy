# Board Pack — Allura Finance

Periodo das movimentacoes: 2025-01 a 2025-07.

## 1) Resumo executivo
No periodo, a casa movimentou R$ 3.322.520,14 de captacao e R$ 3.971.878,47 de resgate, com captacao liquida de R$ -649.358,33 (fonte: kpis_mensais).
A media mensal de captacao ficou abaixo da meta de R$ 2.500.000,00.
A media mensal de receita foi R$ 299.909,58 contra meta de R$ 180.000,00 (fonte: receita_mensal).
O melhor mes liquido foi 2025-02 (R$ 203.108,82); o pior, 2025-06 (R$ -288.272,16).
Produto que mais captou: Acoes Brasil. Canal que mais captou: Assessor.
Snapshot de clientes inativos: 22/40. Taxa mensal de churn: buraco de dado (sem evidencia).
Nao ha PII em claro neste pacote. Nao ha recomendacao de investimento.

## 2) KPIs do periodo versus meta
Medias mensais contra meta mensal cadastrada em silver/metas.csv.

| kpi | realizado | meta_mes | gap |
| --- | --- | --- | --- |
| captacao (media mensal) | R$ 474.645,73 | R$ 2.500.000,00 | R$ -2.025.354,27 |
| resgate (media mensal) | R$ 567.411,21 | R$ 1.200.000,00 | R$ -632.588,79 |
| captacao_liquida (media mensal) | R$ -92.765,48 | R$ 1.300.000,00 | R$ -1.392.765,48 |
| receita (media mensal) | R$ 299.909,58 | R$ 180.000,00 | R$ 119.909,58 |
| churn_clientes_pct (mensal) | sem evidencia | 3.0% | nao comparavel |

## 3) O que subiu / o que caiu
Subiu (melhor liquida): 2025-02 com captacao R$ 585.529,05 e resgate R$ 382.420,23 — fonte kpis_mensais.
Caiu (pior liquida): 2025-06 com captacao R$ 386.316,82 e resgate R$ 674.588,98 — fonte kpis_mensais.
Causa evidenciada ao nivel do harness: diferenca aritmetica captacao - resgate no mes; recorte produto/canal esta em mix_* e base_analise, nao ha evento qualitativo no bronze.

## 4) Mix de produto e canal
| produto | captacao | resgate | qtd | captacao_liquida |
| --- | --- | --- | --- | --- |
| Acoes Brasil | 959,467.17 | 778,098.27 | 37 | 181,368.90 |
| Tesouro Selic | 750,497.16 | 903,710.63 | 39 | -153,213.47 |
| Fundo DI | 648,791.27 | 817,564.30 | 34 | -168,773.03 |
| Renda Fixa Credito | 573,579.52 | 687,456.08 | 36 | -113,876.56 |
| Fundo Multimercado | 390,185.02 | 785,049.19 | 34 | -394,864.17 |

| canal | captacao | resgate | qtd | captacao_liquida |
| --- | --- | --- | --- | --- |
| Assessor | 1,376,523.08 | 1,426,863.44 | 75 | -50,340.36 |
| App | 1,229,330.59 | 1,839,757.69 | 69 | -610,427.10 |
| Parceiro | 716,666.47 | 705,257.34 | 36 | 11,409.13 |

## 5) Receita e churn/status (alertas)
Receita total R$ 2.099.367,09; media R$ 299.909,58; meta mensal R$ 180.000,00.
Meses abaixo da meta de receita: nenhum.
Alerta de churn mensal: **buraco** — so existe snapshot de status (22 inativos). Nao comparar com meta de 3.0%.

## 6) 3 recomendacoes
| prioridade | recomendacao | impacto | esforco | dono sugerido |
|---|---|---|---|---|
| 1 | Abrir o mes 2025-06 em produto/canal e agir no vazamento de liquida | alto | medio | Superintendencia Comercial |
| 2 | Dobrar atencao no produto Acoes Brasil e no canal Assessor | alto | baixo | Produtos + Distribuição |
| 3 | Instrumentar data de inativacao para medir churn mensal de verdade | medio | medio | Dados / CRM |

## 7) Limites dos dados e proximos passos
- Dados sinteticos didaticos; fee de receita muitas vezes nao informado.
- Receita e movimentacoes nao se cruzam em id de transacao.
- Proximo passo: incluir evento de churn e conciliar receita x AUM.

## 8) Anexo — fontes
- data/gold/kpis_mensais.csv
- data/gold/mix_produto.csv
- data/gold/mix_canal.csv
- data/gold/receita_mensal.csv
- data/gold/status_snapshot.csv
- data/silver/metas.csv
- outputs/analise_final.md

Pronto para Board Pack: **SIM**
Checklist do que falta: taxa mensal de churn; narrativa qualitativa de causa (nao existe no bronze).
