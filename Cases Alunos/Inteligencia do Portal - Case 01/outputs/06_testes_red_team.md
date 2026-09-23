# Testes e red team — etapa 06

Inspeção de código e comportamento esperado da aplicação gerada.

| Teste | Resultado | Evidência | Correção |
|---|---|---|---|
| Abre sem internet | PASS | HTML/CSS/JS locais, sem CDN | — |
| Demonstração aparece | PASS | `sample-data.js` com 6 competências | — |
| Filtro altera tabelas | PASS | `filtro-periodo` re-renderiza views | — |
| Metas respeitam vigência e direção | PASS | `metas_status.csv` só 2026-01 a 2026-06 | — |
| Mix fecha 100% | PASS | teste Gold `mix_fecha_100` | — |
| Evidência com fonte e fórmula | PASS | diálogo `dlg-evidencia` | — |
| Status persiste | PASS | `localStorage` `portal-intelligence-v1` | — |
| Export JSON/CSV/MD | PASS | botões em Dados | — |
| Prompt injection textual | PASS | `textContent` / `createTextNode` | — |
| HTML/JS no CSV | PASS | nenhum `innerHTML` com dado externo | — |
| Fórmula de planilha | PASS | `csvEscape` prefixa `'` | — |
| PII | PASS | bloqueio por `@` ou CPF | — |
| Arquivo > 5 MB | PASS | `MAX_BYTES` | — |
| Extensão inválida | PASS | aceita só csv/json | — |
| `eval` / `Function` / URL externa | PASS | varredura do `app.js` | — |

Arquivos adversariais não foram gravados nos dados oficiais.
