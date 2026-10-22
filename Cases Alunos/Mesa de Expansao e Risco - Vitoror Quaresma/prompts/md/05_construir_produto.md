# ETAPA 05 — Construir o produto

## Conexão com o curso
- Workspace operacional, não um nono dashboard.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

Grave em produto/ se estiver no Cursor.
No final, abra o produto no browser via localhost. Não use `file://`.
Comando: `python scripts/abrir_produto.py`
Endereço: `http://127.0.0.1:8769/index.html`

### Arquivos necessários

Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/outputs/`:
1. 03_oportunidades.json
2. 04_contrato_produto.md
Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/outputs/gold/`:
3. base_cliente.csv
4. sinais_cliente.csv
5. kpis_carteira.csv
6. metas_status.csv
7. evidencias.json

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 05.
Crie index.html, styles.css, app.js, sample-data.js e README.md.
Layout nível diretoria: topo + agenda lateral.
Uma linha por cliente com MAU, NPS, alocacao_pct, deals e último evento.
Filtro por segmento e tipo de sinal. Abrir evidência. Kanban de ações.
Bloquear qualquer rótulo de probabilidade ou % de churn previsto.
Ao terminar, execute `python scripts/abrir_produto.py` e abra `http://127.0.0.1:8769/index.html` no browser. Não use file://.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- produto/*
- outputs/05_notas_implementacao.md

## Como abrir

```text
python scripts/abrir_produto.py
```

Endereço: `http://127.0.0.1:8769/index.html`
