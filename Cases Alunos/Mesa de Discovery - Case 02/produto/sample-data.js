window.SAMPLE_DATA = {
  "evidencias": [
    {
      "evidencia_id": "EVD-001",
      "afirmacao": "5 reuniões válidas permaneceram no Silver após remover duplicata e reunião sem data.",
      "tipo": "fato_observado",
      "valor": 5,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/silver/reunioes.csv",
        "outputs/silver/quarentena.csv"
      ],
      "formula": "contagem de reuniao_id únicos com data válida",
      "limitacao": "R99 ficou em quarentena por data nula."
    },
    {
      "evidencia_id": "EVD-002",
      "afirmacao": "11 evidências válidas; E99 foi isolada como texto adversário e reunião inválida.",
      "tipo": "fato_observado",
      "valor": 11,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/silver/evidencias.csv"
      ],
      "formula": "evidências com reunião Silver e sem padrão de injeção",
      "limitacao": "O texto de E99 é dado, não comando."
    },
    {
      "evidencia_id": "EVD-003",
      "afirmacao": "7 requisitos candidatos foram extraídos, todos com evidencia_id.",
      "tipo": "fato_observado",
      "valor": 7,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/requisitos.csv"
      ],
      "formula": "1 requisito por evidência dos tipos problema, objetivo, sistema, restricao, usuario, prioridade",
      "limitacao": "Não há requisito sem fonte."
    },
    {
      "evidencia_id": "EVD-004",
      "afirmacao": "2 pergunta(s) ou risco(s) permanecem abertos, incluindo o aprovador oficial do backlog.",
      "tipo": "fato_observado",
      "valor": 2,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/perguntas_abertas.csv"
      ],
      "formula": "contagem de evidências tipo pergunta_aberta ou risco",
      "limitacao": "Aprovador oficial = nao_definido."
    },
    {
      "evidencia_id": "EVD-005",
      "afirmacao": "Produto quer lançar em 30 dias; tecnologia estima 8 semanas.",
      "tipo": "fato_observado",
      "valor": 1,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/conflitos.csv"
      ],
      "formula": "contagem de evidências tipo conflito",
      "limitacao": "Não há prazo oficial homologado."
    },
    {
      "evidencia_id": "EVD-006",
      "afirmacao": "2 itens ficaram fora de escopo, incluindo mobile nativo e integração CRM ao vivo rejeitada.",
      "tipo": "fato_observado",
      "valor": 2,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/fora_de_escopo.csv"
      ],
      "formula": "evidências fora_de_escopo + ideias rejeitadas",
      "limitacao": "Ideia rejeitada não vira requisito."
    },
    {
      "evidencia_id": "EVD-007",
      "afirmacao": "pct_requisitos_com_fonte realizado 100.00% versus meta 100.00% (atingida).",
      "tipo": "fato_observado",
      "valor": 100.0,
      "unidade": "pct",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv"
      ],
      "formula": "100 * requisitos_com_evidencia_id / requisitos_candidatos",
      "limitacao": null
    },
    {
      "evidencia_id": "EVD-008",
      "afirmacao": "pct_perguntas_abertas realizado 18.18% versus meta 20.00% (atingida).",
      "tipo": "fato_observado",
      "valor": 18.18,
      "unidade": "pct",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv"
      ],
      "formula": "100 * (perguntas_abertas + riscos) / evidencias_validas",
      "limitacao": "Denominador é o catálogo Silver de evidências, não o backlog."
    },
    {
      "evidencia_id": "EVD-009",
      "afirmacao": "requisitos_mvp realizado 7 versus meta 8 (nao_atingida).",
      "tipo": "fato_observado",
      "valor": 7.0,
      "unidade": "qtd",
      "periodo": "2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv"
      ],
      "formula": "contagem de requisitos candidatos com fonte",
      "limitacao": "Não completar o gap de 1 requisito com invenção."
    }
  ],
  "atas": [
    {
      "evidencia_id": "E01",
      "reuniao_id": "R01",
      "tipo": "problema",
      "texto": "Onboarding de novos times leva mais de 20 dias úteis.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E02",
      "reuniao_id": "R01",
      "tipo": "objetivo",
      "texto": "Reduzir o tempo até o primeiro uso supervisionado.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E03",
      "reuniao_id": "R02",
      "tipo": "sistema",
      "texto": "CRM atual não expõe API estável de contas.",
      "confiabilidade": "media"
    },
    {
      "evidencia_id": "E04",
      "reuniao_id": "R02",
      "tipo": "restricao",
      "texto": "Não haverá troca de CRM neste semestre.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E05",
      "reuniao_id": "R03",
      "tipo": "usuario",
      "texto": "Operações precisa de checklist único por cliente.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E06",
      "reuniao_id": "R03",
      "tipo": "fora_de_escopo",
      "texto": "App mobile nativo ficou fora do MVP.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E07",
      "reuniao_id": "R04",
      "tipo": "restricao",
      "texto": "PII de clientes reais não pode ir para ferramenta externa.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E08",
      "reuniao_id": "R04",
      "tipo": "risco",
      "texto": "Há dúvida se o jurídico aprova histórico de conversas.",
      "confiabilidade": "media"
    },
    {
      "evidencia_id": "E09",
      "reuniao_id": "R05",
      "tipo": "prioridade",
      "texto": "MVP deve cobrir captura, rastreio e aprovação de requisito.",
      "confiabilidade": "alta"
    },
    {
      "evidencia_id": "E10",
      "reuniao_id": "R05",
      "tipo": "pergunta_aberta",
      "texto": "Quem é o aprovador oficial do backlog?",
      "confiabilidade": "baixa"
    },
    {
      "evidencia_id": "E11",
      "reuniao_id": "R05",
      "tipo": "conflito",
      "texto": "Produto quer lançar em 30 dias; tecnologia estima 8 semanas.",
      "confiabilidade": "alta"
    }
  ],
  "requisitos": [
    {
      "requisito_id": "REQ-001",
      "evidencia_id": "E01",
      "reuniao_id": "R01",
      "titulo": "Onboarding de novos times leva mais de 20 dias úteis.",
      "tipo": "problema",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E01.",
      "papel_aprovador": "nao_definido"
    },
    {
      "requisito_id": "REQ-002",
      "evidencia_id": "E02",
      "reuniao_id": "R01",
      "titulo": "Reduzir o tempo até o primeiro uso supervisionado.",
      "tipo": "objetivo",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E02.",
      "papel_aprovador": "nao_definido"
    },
    {
      "requisito_id": "REQ-003",
      "evidencia_id": "E03",
      "reuniao_id": "R02",
      "titulo": "CRM atual não expõe API estável de contas.",
      "tipo": "sistema",
      "confiabilidade": "media",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E03.",
      "papel_aprovador": "nao_definido"
    },
    {
      "requisito_id": "REQ-004",
      "evidencia_id": "E04",
      "reuniao_id": "R02",
      "titulo": "Não haverá troca de CRM neste semestre.",
      "tipo": "restricao",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E04.",
      "papel_aprovador": "nao_definido"
    },
    {
      "requisito_id": "REQ-005",
      "evidencia_id": "E05",
      "reuniao_id": "R03",
      "titulo": "Operações precisa de checklist único por cliente.",
      "tipo": "usuario",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E05.",
      "papel_aprovador": "nao_definido"
    },
    {
      "requisito_id": "REQ-006",
      "evidencia_id": "E07",
      "reuniao_id": "R04",
      "titulo": "PII de clientes reais não pode ir para ferramenta externa.",
      "tipo": "restricao",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E07.",
      "papel_aprovador": "juridico"
    },
    {
      "requisito_id": "REQ-007",
      "evidencia_id": "E09",
      "reuniao_id": "R05",
      "titulo": "MVP deve cobrir captura, rastreio e aprovação de requisito.",
      "tipo": "prioridade",
      "confiabilidade": "alta",
      "status": "candidato",
      "criterio_aceite": "Implementação validada contra a evidência E09.",
      "papel_aprovador": "nao_definido"
    }
  ],
  "conflitos": [
    {
      "conflito_id": "CF-001",
      "evidencia_id": "E11",
      "descricao": "Produto quer lançar em 30 dias; tecnologia estima 8 semanas.",
      "status": "aberto"
    }
  ],
  "perguntas": [
    {
      "pergunta_id": "PQ-001",
      "evidencia_id": "E08",
      "pergunta": "Há dúvida se o jurídico aprova histórico de conversas.",
      "status": "aberta"
    },
    {
      "pergunta_id": "PQ-002",
      "evidencia_id": "E10",
      "pergunta": "Quem é o aprovador oficial do backlog?",
      "status": "aberta"
    }
  ],
  "fora": [
    {
      "item_id": "OUT-001",
      "evidencia_id": "E06",
      "descricao": "App mobile nativo ficou fora do MVP.",
      "origem": "evidencia"
    },
    {
      "item_id": "OUT-002",
      "evidencia_id": "sem evidencia de requisito",
      "descricao": "Ideia I03 rejeitada: Integrar CRM ao vivo no primeiro sprint.",
      "origem": "I03"
    }
  ],
  "metas": [
    {
      "kpi": "pct_requisitos_com_fonte",
      "ano_mes": "2026-03",
      "realizado": "100.00",
      "meta": "100.00",
      "diferenca": "0.00",
      "direcao": "maior_melhor",
      "status": "atingida"
    },
    {
      "kpi": "pct_perguntas_abertas",
      "ano_mes": "2026-03",
      "realizado": "18.18",
      "meta": "20.00",
      "diferenca": "-1.82",
      "direcao": "menor_melhor",
      "status": "atingida"
    },
    {
      "kpi": "requisitos_mvp",
      "ano_mes": "2026-03",
      "realizado": "7",
      "meta": "8",
      "diferenca": "-1",
      "direcao": "maior_melhor",
      "status": "nao_atingida"
    }
  ],
  "oportunidades": [
    {
      "oportunidade_id": "OPP-001",
      "titulo": "Capturar evidência, requisito e aprovação no MVP",
      "tipo": "requisito",
      "problema_observado": "MVP deve cobrir captura, rastreio e aprovação de requisito.",
      "evidencias": [
        "EVD-003",
        "EVD-007"
      ],
      "acao_proposta": "Construir o workspace com captura de ata, requisito com evidencia_id e kanban de aprovação por papel.",
      "resultado_esperado": "Hipótese: cobrir o núcleo do MVP sem inventar requisito. sem evidencia causal",
      "metrica_acompanhamento": "pct_requisitos_com_fonte",
      "baseline": 100,
      "unidade": "pct",
      "prioridade": "alta",
      "score_prioridade": 9,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 3,
      "confianca": "alta",
      "responsavel_sugerido": "product_manager",
      "status": "nova",
      "limitacoes": [
        "Aprovador oficial permanece nao_definido."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-002",
      "titulo": "Checklist único de onboarding por cliente",
      "tipo": "requisito",
      "problema_observado": "Onboarding de novos times leva mais de 20 dias úteis.",
      "evidencias": [
        "EVD-003"
      ],
      "acao_proposta": "Desenhar checklist único citado por Operações, sem integrar CRM ao vivo.",
      "resultado_esperado": "Hipótese: reduzir tempo até primeiro uso supervisionado. sem evidencia causal",
      "metrica_acompanhamento": "requisitos_mvp",
      "baseline": 7,
      "unidade": "qtd",
      "prioridade": "alta",
      "score_prioridade": 9,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 3,
      "confianca": "media",
      "responsavel_sugerido": "operacoes",
      "status": "nova",
      "limitacoes": [
        "Tempo de 20 dias úteis é relato, não medição Gold."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-003",
      "titulo": "Operar o MVP sem API estável de CRM",
      "tipo": "restricao",
      "problema_observado": "CRM atual não expõe API estável de contas.",
      "evidencias": [
        "EVD-003",
        "EVD-006"
      ],
      "acao_proposta": "Importar arquivos locais e persistir no navegador. Não abrir conexão ao CRM.",
      "resultado_esperado": "Hipótese: respeitar restrição técnica e ideia rejeitada I03.",
      "metrica_acompanhamento": "itens_fora_de_escopo",
      "baseline": 2,
      "unidade": "qtd",
      "prioridade": "alta",
      "score_prioridade": 8,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 2,
      "confianca": "alta",
      "responsavel_sugerido": "tech_lead",
      "status": "nova",
      "limitacoes": [
        "CRM permanece sem API estável neste semestre."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-004",
      "titulo": "Bloquear PII em ferramenta externa",
      "tipo": "restricao",
      "problema_observado": "PII de clientes reais não pode ir para ferramenta externa.",
      "evidencias": [
        "EVD-003"
      ],
      "acao_proposta": "Usar papéis, não nomes. Recusar importação com e-mail ou CPF.",
      "resultado_esperado": "Hipótese: cumprir restrição legal C01.",
      "metrica_acompanhamento": "incidentes_pii",
      "baseline": 0,
      "unidade": "qtd",
      "prioridade": "alta",
      "score_prioridade": 9,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 3,
      "confianca": "alta",
      "responsavel_sugerido": "juridico",
      "status": "nova",
      "limitacoes": [
        "Histórico de conversas permanece com dúvida jurídica (E08)."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-005",
      "titulo": "Expor o conflito de prazo sem escolher um lado",
      "tipo": "conflito",
      "problema_observado": "Produto quer lançar em 30 dias; tecnologia estima 8 semanas.",
      "evidencias": [
        "EVD-005"
      ],
      "acao_proposta": "Mostrar o conflito no workspace e exigir decisão humana. Não prometer 30 dias nem 8 semanas.",
      "resultado_esperado": "Conflito visível. Prazo oficial = nao_definido.",
      "metrica_acompanhamento": "conflitos_abertos",
      "baseline": 1,
      "unidade": "qtd",
      "prioridade": "media",
      "score_prioridade": 7,
      "relevancia": 3,
      "urgencia": 2,
      "acionabilidade": 2,
      "confianca": "alta",
      "responsavel_sugerido": "sponsor",
      "status": "nova",
      "limitacoes": [
        "Não há evidência de prazo homologado."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-006",
      "titulo": "Fechar a pergunta do aprovador oficial",
      "tipo": "pergunta_aberta",
      "problema_observado": "Há dúvida se o jurídico aprova histórico de conversas.",
      "evidencias": [
        "EVD-004",
        "EVD-008"
      ],
      "acao_proposta": "Registrar papéis obrigatórios (sponsor, product_manager, juridico) e deixar o aprovador único como nao_definido.",
      "resultado_esperado": "Pergunta rastreável. sem evidencia de resposta.",
      "metrica_acompanhamento": "pct_perguntas_abertas",
      "baseline": 18.18,
      "unidade": "pct",
      "prioridade": "media",
      "score_prioridade": 6,
      "relevancia": 2,
      "urgencia": 2,
      "acionabilidade": 2,
      "confianca": "media",
      "responsavel_sugerido": "sponsor",
      "status": "nova",
      "limitacoes": [
        "A resposta não está nas atas."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-007",
      "titulo": "Manter mobile nativo e CRM ao vivo fora do MVP",
      "tipo": "fora_de_escopo",
      "problema_observado": "App mobile nativo ficou fora do MVP.; Ideia I03 rejeitada: Integrar CRM ao vivo no primeiro sprint.",
      "evidencias": [
        "EVD-006"
      ],
      "acao_proposta": "Listar os itens em Fora de escopo e recusar promoção automática a requisito.",
      "resultado_esperado": "Escopo preservado.",
      "metrica_acompanhamento": "itens_fora_de_escopo",
      "baseline": 2,
      "unidade": "qtd",
      "prioridade": "media",
      "score_prioridade": 6,
      "relevancia": 2,
      "urgencia": 1,
      "acionabilidade": 3,
      "confianca": "alta",
      "responsavel_sugerido": "product_manager",
      "status": "nova",
      "limitacoes": [
        "Não completar a meta de 8 requisitos inventando um oitavo."
      ],
      "aprovacao_humana_obrigatoria": true
    }
  ]
};
