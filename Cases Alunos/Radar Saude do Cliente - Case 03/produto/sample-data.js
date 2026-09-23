window.SAMPLE_DATA = {
  "evidencias": [
    {
      "evidencia_id": "EVD-001",
      "afirmacao": "6 clientes permaneceram no Silver após duplicata e segmento TESTE.",
      "tipo": "fato_observado",
      "valor": 6,
      "unidade": "qtd",
      "periodo": "carteira_sintetica",
      "fonte": [
        "outputs/silver/clientes.csv"
      ],
      "formula": "contagem de cliente_id únicos com data_entrada e segmento canônico",
      "limitacao": "CL99 isolado. data_saida vazia em todos."
    },
    {
      "evidencia_id": "EVD-002",
      "afirmacao": "3 clientes com sinal alto: CL02, CL04, CL06.",
      "tipo": "fato_observado",
      "valor": 3,
      "unidade": "qtd",
      "periodo": "2026-01 a 2026-03",
      "fonte": [
        "outputs/gold/sinais_cliente.csv"
      ],
      "formula": "score_risco = soma de flags binários (atraso, ausência, ticket aberto, SLA, NPS<50, inativo); alto se score >= 4",
      "limitacao": "Score não é probabilidade de churn."
    },
    {
      "evidencia_id": "EVD-003",
      "afirmacao": "4 tickets com SLA estourado versus meta 2 (nao_atingida).",
      "tipo": "fato_observado",
      "valor": 4.0,
      "unidade": "qtd",
      "periodo": "2026-01 a 2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv",
        "outputs/silver/tickets.csv"
      ],
      "formula": "contagem de tickets Silver com sla_estourado=true",
      "limitacao": "T99 isolado por SLA n/a."
    },
    {
      "evidencia_id": "EVD-004",
      "afirmacao": "CL02 (enterprise, ativo) tem score 5: atraso 21 dias, 2 ausências, 2 tickets abertos, NPS 28.",
      "tipo": "fato_observado",
      "valor": 5,
      "unidade": "sinais",
      "periodo": "2026-02 a 2026-03",
      "fonte": [
        "outputs/gold/sinais_cliente.csv"
      ],
      "formula": "flags de CL02 no Gold",
      "limitacao": "NPS 28 é pesquisa pontual, não série."
    },
    {
      "evidencia_id": "EVD-005",
      "afirmacao": "CL04 está inativo no snapshot, com atraso máximo 45 dias e NPS sem evidencia.",
      "tipo": "fato_observado",
      "valor": 5,
      "unidade": "sinais",
      "periodo": "snapshot",
      "fonte": [
        "outputs/gold/sinais_cliente.csv"
      ],
      "formula": "status canônico de 'I' = inativo; NPS n/a isolado",
      "limitacao": "Inativo no snapshot não prova churn temporal."
    },
    {
      "evidencia_id": "EVD-006",
      "afirmacao": "CL06 está inativo, NPS 15, 1 ticket(s) aberto(s) e 1 ausência(s).",
      "tipo": "fato_observado",
      "valor": 6,
      "unidade": "sinais",
      "periodo": "2026-01",
      "fonte": [
        "outputs/gold/sinais_cliente.csv"
      ],
      "formula": "flags de CL06",
      "limitacao": "Sem data_saida; não classificar como churn confirmado."
    },
    {
      "evidencia_id": "EVD-007",
      "afirmacao": "churn_clientes_pct é sem evidencia: não há data_saida nem histórico de status.",
      "tipo": "lacuna",
      "valor": null,
      "unidade": "pct",
      "periodo": "2026-01 a 2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv",
        "outputs/silver/clientes.csv"
      ],
      "formula": "sem data_saida preenchida e sem série temporal de status",
      "limitacao": "Não calcular probabilidade de churn."
    },
    {
      "evidencia_id": "EVD-008",
      "afirmacao": "NPS ausente para CL04, CL05 após isolamento de n/a.",
      "tipo": "fato_observado",
      "valor": 2,
      "unidade": "qtd",
      "periodo": "2026-01 a 2026-03",
      "fonte": [
        "outputs/silver/nps.csv",
        "outputs/silver/quarentena.csv"
      ],
      "formula": "clientes Silver sem linha NPS válida",
      "limitacao": "Ausência não é imputada."
    },
    {
      "evidencia_id": "EVD-009",
      "afirmacao": "clientes_com_sinal_alto realizado 3 versus meta 2 (nao_atingida).",
      "tipo": "fato_observado",
      "valor": 3.0,
      "unidade": "qtd",
      "periodo": "2026-01 a 2026-03",
      "fonte": [
        "outputs/gold/metas_status.csv"
      ],
      "formula": "contagem de nivel_sinal=alto",
      "limitacao": "Sinal alto ≠ churn."
    }
  ],
  "sinais": [
    {
      "cliente_id": "CL01",
      "segmento": "enterprise",
      "status": "ativo",
      "data_entrada": "2024-02-10",
      "data_saida": "",
      "atraso_projeto": "false",
      "atraso_dias_max": "0",
      "ausencia_evento": "false",
      "ausencias": "0",
      "ticket_aberto": "false",
      "tickets_abertos": "0",
      "sla_estourado": "false",
      "tickets_sla": "0",
      "nps": "72",
      "nps_baixo": "false",
      "nps_ausente": "false",
      "status_inativo": "false",
      "score_risco": "0",
      "nivel_sinal": "baixo",
      "churn_confirmado": "sem evidencia"
    },
    {
      "cliente_id": "CL02",
      "segmento": "enterprise",
      "status": "ativo",
      "data_entrada": "2024-04-15",
      "data_saida": "",
      "atraso_projeto": "true",
      "atraso_dias_max": "21",
      "ausencia_evento": "true",
      "ausencias": "2",
      "ticket_aberto": "true",
      "tickets_abertos": "2",
      "sla_estourado": "true",
      "tickets_sla": "2",
      "nps": "28",
      "nps_baixo": "true",
      "nps_ausente": "false",
      "status_inativo": "false",
      "score_risco": "5",
      "nivel_sinal": "alto",
      "churn_confirmado": "sem evidencia"
    },
    {
      "cliente_id": "CL03",
      "segmento": "mid",
      "status": "ativo",
      "data_entrada": "2024-07-03",
      "data_saida": "",
      "atraso_projeto": "false",
      "atraso_dias_max": "0",
      "ausencia_evento": "false",
      "ausencias": "0",
      "ticket_aberto": "false",
      "tickets_abertos": "0",
      "sla_estourado": "false",
      "tickets_sla": "0",
      "nps": "64",
      "nps_baixo": "false",
      "nps_ausente": "false",
      "status_inativo": "false",
      "score_risco": "0",
      "nivel_sinal": "baixo",
      "churn_confirmado": "sem evidencia"
    },
    {
      "cliente_id": "CL04",
      "segmento": "smb",
      "status": "inativo",
      "data_entrada": "2024-09-03",
      "data_saida": "",
      "atraso_projeto": "true",
      "atraso_dias_max": "45",
      "ausencia_evento": "true",
      "ausencias": "1",
      "ticket_aberto": "true",
      "tickets_abertos": "1",
      "sla_estourado": "true",
      "tickets_sla": "1",
      "nps": "sem evidencia",
      "nps_baixo": "false",
      "nps_ausente": "true",
      "status_inativo": "true",
      "score_risco": "5",
      "nivel_sinal": "alto",
      "churn_confirmado": "sem evidencia"
    },
    {
      "cliente_id": "CL05",
      "segmento": "smb",
      "status": "ativo",
      "data_entrada": "2025-01-20",
      "data_saida": "",
      "atraso_projeto": "false",
      "atraso_dias_max": "0",
      "ausencia_evento": "false",
      "ausencias": "0",
      "ticket_aberto": "false",
      "tickets_abertos": "0",
      "sla_estourado": "false",
      "tickets_sla": "0",
      "nps": "sem evidencia",
      "nps_baixo": "false",
      "nps_ausente": "true",
      "status_inativo": "false",
      "score_risco": "0",
      "nivel_sinal": "baixo",
      "churn_confirmado": "sem evidencia"
    },
    {
      "cliente_id": "CL06",
      "segmento": "enterprise",
      "status": "inativo",
      "data_entrada": "2023-11-08",
      "data_saida": "",
      "atraso_projeto": "true",
      "atraso_dias_max": "12",
      "ausencia_evento": "true",
      "ausencias": "1",
      "ticket_aberto": "true",
      "tickets_abertos": "1",
      "sla_estourado": "true",
      "tickets_sla": "1",
      "nps": "15",
      "nps_baixo": "true",
      "nps_ausente": "false",
      "status_inativo": "true",
      "score_risco": "6",
      "nivel_sinal": "alto",
      "churn_confirmado": "sem evidencia"
    }
  ],
  "kpis": [
    {
      "kpi": "clientes_validos",
      "valor": "6",
      "unidade": "qtd",
      "nota": "Silver após quarentena"
    },
    {
      "kpi": "clientes_com_sinal_alto",
      "valor": "3",
      "unidade": "qtd",
      "nota": "score >= 4"
    },
    {
      "kpi": "tickets_sla_estourado",
      "valor": "4",
      "unidade": "qtd",
      "nota": "Silver com sla_estourado=true"
    },
    {
      "kpi": "churn_clientes_pct",
      "valor": "sem evidencia",
      "unidade": "pct",
      "nota": "sem data_saida e sem historico de status"
    }
  ],
  "metas": [
    {
      "kpi": "clientes_com_sinal_alto",
      "ano_mes": "2026-01 a 2026-03",
      "realizado": "3",
      "meta": "2",
      "diferenca": "1",
      "direcao": "menor_melhor",
      "status": "nao_atingida"
    },
    {
      "kpi": "tickets_sla_estourado",
      "ano_mes": "2026-01 a 2026-03",
      "realizado": "4",
      "meta": "2",
      "diferenca": "2",
      "direcao": "menor_melhor",
      "status": "nao_atingida"
    },
    {
      "kpi": "churn_clientes_pct",
      "ano_mes": "2026-01 a 2026-03",
      "realizado": "sem evidencia",
      "meta": "3.00",
      "diferenca": "sem evidencia",
      "direcao": "menor_melhor",
      "status": "sem evidencia"
    }
  ],
  "oportunidades": [
    {
      "oportunidade_id": "OPP-001",
      "titulo": "Plano imediato para CL02",
      "tipo": "acao_carteira",
      "problema_observado": "CL02 (enterprise, ativo) tem score 5: atraso 21 dias, 2 ausências, 2 tickets abertos, NPS 28.",
      "evidencias": [
        "EVD-004",
        "EVD-003"
      ],
      "acao_proposta": "Reagendar QBR, tratar tickets abertos com SLA estourado e registrar pendências no workspace.",
      "resultado_esperado": "Hipótese: reduzir score_risco de CL02. sem evidencia causal",
      "metrica_acompanhamento": "score_risco_CL02",
      "baseline": 5,
      "unidade": "sinais",
      "prioridade": "alta",
      "score_prioridade": 9,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 3,
      "confianca": "media",
      "responsavel_sugerido": "cs_enterprise",
      "status": "nova",
      "cliente_id": "CL02",
      "limitacoes": [
        "Score não é probabilidade.",
        "sem evidencia causal"
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-002",
      "titulo": "Revisar CL04 inativo sem data de saída",
      "tipo": "acao_carteira",
      "problema_observado": "CL04 está inativo no snapshot, com atraso máximo 45 dias e NPS sem evidencia.",
      "evidencias": [
        "EVD-005",
        "EVD-007"
      ],
      "acao_proposta": "Confirmar com operações se CL04 está pausado, encerrado ou só com status inconsistente. Não rotular churn.",
      "resultado_esperado": "Status humano confirmado. churn continua sem evidencia.",
      "metrica_acompanhamento": "status_CL04",
      "baseline": "inativo",
      "unidade": "status",
      "prioridade": "alta",
      "score_prioridade": 8,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 2,
      "confianca": "media",
      "responsavel_sugerido": "operacoes",
      "status": "nova",
      "cliente_id": "CL04",
      "limitacoes": [
        "Snapshot sem data_saida."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-003",
      "titulo": "Plano para CL06 com NPS 15 e ticket crítico",
      "tipo": "acao_carteira",
      "problema_observado": "CL06 está inativo, NPS 15, 1 ticket(s) aberto(s) e 1 ausência(s).",
      "evidencias": [
        "EVD-006"
      ],
      "acao_proposta": "Abrir plano de recuperação com papéis de CS e suporte. Não pedir cancelamento.",
      "resultado_esperado": "Hipótese: tratar sinais visíveis. sem evidencia causal",
      "metrica_acompanhamento": "score_risco_CL06",
      "baseline": 6,
      "unidade": "sinais",
      "prioridade": "alta",
      "score_prioridade": 8,
      "relevancia": 3,
      "urgencia": 3,
      "acionabilidade": 2,
      "confianca": "media",
      "responsavel_sugerido": "cs_enterprise",
      "status": "nova",
      "cliente_id": "CL06",
      "limitacoes": [
        "Inativo no snapshot ≠ churn confirmado."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-004",
      "titulo": "Coletar NPS de CL04 e CL05",
      "tipo": "qualidade_dados",
      "problema_observado": "NPS ausente para CL04, CL05 após isolamento de n/a.",
      "evidencias": [
        "EVD-008"
      ],
      "acao_proposta": "Registrar nova pesquisa. Não imputar NPS.",
      "resultado_esperado": "Hipótese: eliminar nps_ausente.",
      "metrica_acompanhamento": "clientes_sem_nps",
      "baseline": 2,
      "unidade": "qtd",
      "prioridade": "media",
      "score_prioridade": 7,
      "relevancia": 2,
      "urgencia": 2,
      "acionabilidade": 3,
      "confianca": "alta",
      "responsavel_sugerido": "dados",
      "status": "nova",
      "cliente_id": "",
      "limitacoes": [
        "CL04 n/a foi quarentenado; CL05 não tinha linha."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-005",
      "titulo": "Tratar o gap de tickets com SLA estourado",
      "tipo": "operacao",
      "problema_observado": "4 tickets com SLA estourado versus meta 2 (nao_atingida).",
      "evidencias": [
        "EVD-003",
        "EVD-009"
      ],
      "acao_proposta": "Priorizar tickets abertos de CL02, CL04 e CL06 no kanban do produto.",
      "resultado_esperado": "Hipótese: aproximar a meta de 2 tickets com SLA estourado. sem evidencia causal",
      "metrica_acompanhamento": "tickets_sla_estourado",
      "baseline": 4,
      "unidade": "qtd",
      "prioridade": "media",
      "score_prioridade": 7,
      "relevancia": 3,
      "urgencia": 2,
      "acionabilidade": 2,
      "confianca": "media",
      "responsavel_sugerido": "suporte",
      "status": "nova",
      "cliente_id": "",
      "limitacoes": [
        "T99 não entra na conta."
      ],
      "aprovacao_humana_obrigatoria": true
    },
    {
      "oportunidade_id": "OPP-006",
      "titulo": "Manter churn como sem evidencia no produto",
      "tipo": "governanca",
      "problema_observado": "churn_clientes_pct é sem evidencia: não há data_saida nem histórico de status.",
      "evidencias": [
        "EVD-007"
      ],
      "acao_proposta": "Exibir a meta de churn com status sem evidencia. Bloquear rótulo de probabilidade.",
      "resultado_esperado": "Produto não inventa churn.",
      "metrica_acompanhamento": "churn_clientes_pct",
      "baseline": "sem evidencia",
      "unidade": "pct",
      "prioridade": "alta",
      "score_prioridade": 8,
      "relevancia": 3,
      "urgencia": 2,
      "acionabilidade": 3,
      "confianca": "alta",
      "responsavel_sugerido": "dados",
      "status": "nova",
      "cliente_id": "",
      "limitacoes": [
        "Sem histórico de status e sem data_saida."
      ],
      "aprovacao_humana_obrigatoria": true
    }
  ]
};
