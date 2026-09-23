# Backlog explicado — etapa 03

## OPP-001 — Capturar evidência, requisito e aprovação no MVP
- problema_observado: MVP deve cobrir captura, rastreio e aprovação de requisito.
- evidencias: EVD-003, EVD-007
- acao_proposta: Construir o workspace com captura de ata, requisito com evidencia_id e kanban de aprovação por papel.
- resultado_esperado: Hipótese: cobrir o núcleo do MVP sem inventar requisito. sem evidencia causal
- prioridade: alta (R3+U3+A3=9)
- confianca: alta
- dono: product_manager

## OPP-002 — Checklist único de onboarding por cliente
- problema_observado: Onboarding de novos times leva mais de 20 dias úteis.
- evidencias: EVD-003
- acao_proposta: Desenhar checklist único citado por Operações, sem integrar CRM ao vivo.
- resultado_esperado: Hipótese: reduzir tempo até primeiro uso supervisionado. sem evidencia causal
- prioridade: alta (R3+U3+A3=9)
- confianca: media
- dono: operacoes

## OPP-003 — Operar o MVP sem API estável de CRM
- problema_observado: CRM atual não expõe API estável de contas.
- evidencias: EVD-003, EVD-006
- acao_proposta: Importar arquivos locais e persistir no navegador. Não abrir conexão ao CRM.
- resultado_esperado: Hipótese: respeitar restrição técnica e ideia rejeitada I03.
- prioridade: alta (R3+U3+A2=8)
- confianca: alta
- dono: tech_lead

## OPP-004 — Bloquear PII em ferramenta externa
- problema_observado: PII de clientes reais não pode ir para ferramenta externa.
- evidencias: EVD-003
- acao_proposta: Usar papéis, não nomes. Recusar importação com e-mail ou CPF.
- resultado_esperado: Hipótese: cumprir restrição legal C01.
- prioridade: alta (R3+U3+A3=9)
- confianca: alta
- dono: juridico

## OPP-005 — Expor o conflito de prazo sem escolher um lado
- problema_observado: Produto quer lançar em 30 dias; tecnologia estima 8 semanas.
- evidencias: EVD-005
- acao_proposta: Mostrar o conflito no workspace e exigir decisão humana. Não prometer 30 dias nem 8 semanas.
- resultado_esperado: Conflito visível. Prazo oficial = nao_definido.
- prioridade: media (R3+U2+A2=7)
- confianca: alta
- dono: sponsor

## OPP-006 — Fechar a pergunta do aprovador oficial
- problema_observado: Há dúvida se o jurídico aprova histórico de conversas.
- evidencias: EVD-004, EVD-008
- acao_proposta: Registrar papéis obrigatórios (sponsor, product_manager, juridico) e deixar o aprovador único como nao_definido.
- resultado_esperado: Pergunta rastreável. sem evidencia de resposta.
- prioridade: media (R2+U2+A2=6)
- confianca: media
- dono: sponsor

## OPP-007 — Manter mobile nativo e CRM ao vivo fora do MVP
- problema_observado: App mobile nativo ficou fora do MVP.; Ideia I03 rejeitada: Integrar CRM ao vivo no primeiro sprint.
- evidencias: EVD-006
- acao_proposta: Listar os itens em Fora de escopo e recusar promoção automática a requisito.
- resultado_esperado: Escopo preservado.
- prioridade: media (R2+U1+A3=6)
- confianca: alta
- dono: product_manager
