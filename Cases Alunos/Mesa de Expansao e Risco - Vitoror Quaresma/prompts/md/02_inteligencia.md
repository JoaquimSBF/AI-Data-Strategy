# ETAPA 02 — Cruzamento e evidências

## Conexão com o curso
- Star/join por cliente, score explicável, recusa de métrica impossível.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

Use Silver + dicionário.

### Arquivos necessários

Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/outputs/silver/`:
1. clientes.csv
2. crm_deals.csv
3. crm_atividades.csv
4. licencas.csv
5. eventos_contrato.csv
6. nps_export.csv
7. metas.csv
8. quarentena.csv
Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/dados/`:
9. README_DADOS.md

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 02.
Cruze as três origens por cliente_id. Cliente só no CRM, só no Admin ou só no export de NPS: declare a lacuna.
Por cliente e competência mais recente válida, calcule: mau, nps, alocacao_pct, deals abertos, deals ganhos, deals perdidos, soma de atividades, ultimo_evento_contrato.
Sinais binários documentados, por exemplo: alocacao abaixo da meta, nps abaixo da meta, recuo de mau, deal perdido no período, downsell datado, deal aberto sem fechamento com muitas atividades.
Score de risco = soma desses sinais. Não é probabilidade.
Meta de churn_previsto_pct: status `sem evidencia`.
Gere evidencias.json (EVD-001 em diante) e testes de integridade (mix de alocação, chaves, recálculo).

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- outputs/02_inteligencia.md
- outputs/gold/base_cliente.csv
- outputs/gold/kpis_carteira.csv
- outputs/gold/sinais_cliente.csv
- outputs/gold/metas_status.csv
- outputs/gold/evidencias.json
- outputs/gold/testes_integridade.csv
