# Notas de implementação — etapa 05

- Aplicação em HTML/CSS/JS puros, sem CDN.
- Números apenas em `sample-data.js`, gerado a partir do Gold.
- Persistência: `localStorage` `portal-intelligence-v1`.
- Dados importados entram via `textContent` / `FileReader`; sem `innerHTML` com dado externo.
- CSV export prefixa `'` em valores que começam com `= + - @`.
- PII aparente (`@` ou CPF) bloqueia o arquivo.
- Filtro de período altera KPIs, mix, busca, benchmark e IA.
- Abrir no browser: `python scripts/abrir_produto.py` → `http://127.0.0.1:8766/index.html`
