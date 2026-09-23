# Dicionário — Radar de Saúde do Cliente

Todos os dados são sintéticos. Clientes são identificadores `CLxx`.

| Arquivo | Grão | Observação |
|---|---|---|
| clientes.csv | um cliente | status atual; `data_saida` vazia em todos |
| projetos.csv | um projeto | atraso pode ser inconsistente |
| eventos.csv | um encontro | ausência e pendências |
| tickets.csv | um ticket | severidade e SLA |
| nps.csv | uma pesquisa | NPS ausente em um cliente |
| metas.csv | um KPI | inclui churn, que **não** pode ser calculado |

Não há histórico de status nem data de inativação. O produto mostra **sinais**, não probabilidade de churn.
