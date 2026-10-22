# ETAPA 01 — Limpeza e Silver

## Conexão com o curso
- Qualidade, chave de cliente, quarentena, recálculo de alocação.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

Anexe só a pasta dados/. Não use outputs/.

### Arquivos necessários

Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/dados/`:
1. clientes.csv
2. crm_deals.csv
3. crm_atividades.csv
4. licencas.csv
5. eventos_contrato.csv
6. nps_export.csv
7. metas.csv
8. README_DADOS.md

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 01.
Padronize datas para YYYY-MM-DD e competência para YYYY-MM.
Padronize segmento (enterprise/mid/smb), status de cliente (ativo/inativo), status de deal (aberto/ganho/perdido) e tipo de evento (upgrade/downsell/upsell).
Recalcule alocacao_pct. Não impute MAU, NPS, data de evento nem data_saida.
Quarentena: duplicata exata, segmento TESTE, cliente sem data_entrada, valor negativo, quantidade negativa, competência inválida, alocação acima de 100% sem justificativa, evento sem data, NPS n/a ou nulo.
Não calcule churn. Não preveja churn.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- outputs/01_relatorio_qualidade.md
- outputs/silver/*.csv
- outputs/silver/quarentena.csv
