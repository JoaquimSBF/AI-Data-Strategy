# ETAPA 03 — Fila de ação

## Conexão com o curso
- Playbook, priorização R+U+A, human-in-the-loop.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

Anexe inteligência e Gold.

### Arquivos necessários

Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/outputs/`:
1. 02_inteligencia.md
Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/outputs/gold/`:
2. base_cliente.csv
3. sinais_cliente.csv
4. kpis_carteira.csv
5. metas_status.csv
6. evidencias.json
7. testes_integridade.csv

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 03.
Crie no máximo 8 ações. Cada uma cita evidencia_id, cliente_id, tipo (risco_downsell / hipotese_upsell / shelfware / qualidade_dados), papel (cs/comercial/produto/dados) e score R+U+A (8-9 alta, 5-7 media, 3-4 baixa).
Não peça cancelamento de contrato sem evento de churn.
Não trate score como probabilidade.
Ação sobre cliente sem chave nas três fontes: tipo qualidade_dados.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- outputs/03_oportunidades.json
- outputs/03_oportunidades.csv
- outputs/03_backlog_explicado.md
