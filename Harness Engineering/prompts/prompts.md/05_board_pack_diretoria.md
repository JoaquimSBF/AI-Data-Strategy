# MODO: BOARD PACK (documento para diretoria)

Entrada: analise_final + KPIs + metas + insights da EDA (so evidencia).
Publico: diretoria da Allura Finance. Tom executivo, claro, sem jargao tecnico de pipeline.

Estrutura obrigatoria:
1) Resumo executivo (ate 8 linhas)
2) KPIs do periodo versus meta (tabela)
3) O que subiu / o que caiu (com causa evidenciada)
4) Mix de produto e canal (o que puxou resultado)
5) Receita e churn/status (alertas)
6) 3 recomendacoes priorizadas (impacto | esforco | dono sugerido)
7) Limites dos dados e proximos passos
8) Anexo curto: fontes usadas

Regras:
- Cada numero precisa de fonte.
- Sem PII.
- Sem tip de investimento.
- Se faltar meta ou periodo, declare o buraco.
- No final: "Pronto para Board Pack: SIM/NAO" + checklist do que falta.

Material minimo (cole trechos ou referencie os arquivos):
- `outputs/analise_final.md` (obrigatorio)
- `data/gold/kpis_mensais.csv`
- `data/gold/mix_produto.csv` e `mix_canal.csv`
- `data/gold/receita_mensal.csv`
- `data/gold/status_snapshot.csv`
- `data/silver/metas.csv`

<<<
[COLE analise_final + KPIs + metas]
>>>

## ONDE SALVAR
Salve manualmente em:

- `outputs/board_pack.md` -> documento final para diretoria (obrigatorio)
- `outputs/board_pack.html` -> opcional (versao visual para apresentacao)
- `outputs/board_pack.docx` -> opcional (se exportar do Markdown)
