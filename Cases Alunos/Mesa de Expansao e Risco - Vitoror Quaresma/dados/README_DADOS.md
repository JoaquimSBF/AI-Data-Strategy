# Dicionário — Mesa de Expansão e Risco

Todos os dados são sintéticos. Cliente é `CLxx`. Não há nome, e-mail nem empresa real.

Power BI **não é fonte**. `nps_export.csv` simula um export do modelo que hoje alimenta vários dashes.

| Arquivo | Origem simulada | Grão | Observação |
|---|---|---|---|
| clientes.csv | cadastro | um cliente | status atual; sem data_saida |
| crm_deals.csv | HubSpot | um deal | aberto/ganho/perdido; há duplicata e valor negativo |
| crm_atividades.csv | HubSpot | uma atividade | data nula e quantidade negativa existem |
| licencas.csv | Admin | cliente × competência | `alocacao_pct` deve ser recalculada: 100 * alocadas / contratadas |
| eventos_contrato.csv | Admin | um evento | upgrade/downsell/upsell **só com data**; não há evento de churn |
| nps_export.csv | export “Power BI” | cliente × competência | NPS `n/a` e competência em formato misto |
| metas.csv | planejamento | um KPI | `churn_previsto_pct` não tem vigência nem rótulo histórico |

Não existe histórico mensal de status de cliente. Sem evento `churn` datado, churn e “previsão de churn” são `sem evidencia`.
