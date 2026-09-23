# Notas de implementação — Radar de Saúde do Cliente

Aplicação local em `produto/`:

- `index.html` — seis seções, filtros de segmento e nível.
- `styles.css` — mesmo sistema visual da Inteligência do Portal.
- `app.js` — persistência `client-health-radar-v1`, bloqueio de rótulo de churn, `textContent`.
- `sample-data.js` — Gold da etapa 02 e ações da etapa 03.

Números da demonstração: 6 clientes, 3 sinais altos, 4 tickets com SLA estourado, churn = sem evidencia.

Abrir no browser: `python scripts/abrir_produto.py` → `http://127.0.0.1:8768/index.html`
