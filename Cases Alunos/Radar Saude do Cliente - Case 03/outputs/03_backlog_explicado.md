# Backlog explicado — etapa 03

## OPP-001 — Plano imediato para CL02
- problema_observado: CL02 (enterprise, ativo) tem score 5: atraso 21 dias, 2 ausências, 2 tickets abertos, NPS 28.
- evidencias: EVD-004, EVD-003
- acao_proposta: Reagendar QBR, tratar tickets abertos com SLA estourado e registrar pendências no workspace.
- resultado_esperado: Hipótese: reduzir score_risco de CL02. sem evidencia causal
- prioridade: alta (R3+U3+A3=9)
- confianca: media
- dono: cs_enterprise

## OPP-002 — Revisar CL04 inativo sem data de saída
- problema_observado: CL04 está inativo no snapshot, com atraso máximo 45 dias e NPS sem evidencia.
- evidencias: EVD-005, EVD-007
- acao_proposta: Confirmar com operações se CL04 está pausado, encerrado ou só com status inconsistente. Não rotular churn.
- resultado_esperado: Status humano confirmado. churn continua sem evidencia.
- prioridade: alta (R3+U3+A2=8)
- confianca: media
- dono: operacoes

## OPP-003 — Plano para CL06 com NPS 15 e ticket crítico
- problema_observado: CL06 está inativo, NPS 15, 1 ticket(s) aberto(s) e 1 ausência(s).
- evidencias: EVD-006
- acao_proposta: Abrir plano de recuperação com papéis de CS e suporte. Não pedir cancelamento.
- resultado_esperado: Hipótese: tratar sinais visíveis. sem evidencia causal
- prioridade: alta (R3+U3+A2=8)
- confianca: media
- dono: cs_enterprise

## OPP-004 — Coletar NPS de CL04 e CL05
- problema_observado: NPS ausente para CL04, CL05 após isolamento de n/a.
- evidencias: EVD-008
- acao_proposta: Registrar nova pesquisa. Não imputar NPS.
- resultado_esperado: Hipótese: eliminar nps_ausente.
- prioridade: media (R2+U2+A3=7)
- confianca: alta
- dono: dados

## OPP-005 — Tratar o gap de tickets com SLA estourado
- problema_observado: 4 tickets com SLA estourado versus meta 2 (nao_atingida).
- evidencias: EVD-003, EVD-009
- acao_proposta: Priorizar tickets abertos de CL02, CL04 e CL06 no kanban do produto.
- resultado_esperado: Hipótese: aproximar a meta de 2 tickets com SLA estourado. sem evidencia causal
- prioridade: media (R3+U2+A2=7)
- confianca: media
- dono: suporte

## OPP-006 — Manter churn como sem evidencia no produto
- problema_observado: churn_clientes_pct é sem evidencia: não há data_saida nem histórico de status.
- evidencias: EVD-007
- acao_proposta: Exibir a meta de churn com status sem evidencia. Bloquear rótulo de probabilidade.
- resultado_esperado: Produto não inventa churn.
- prioridade: alta (R3+U2+A3=8)
- confianca: alta
- dono: dados
