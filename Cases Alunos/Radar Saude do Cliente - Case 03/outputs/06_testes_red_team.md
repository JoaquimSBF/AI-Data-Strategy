# Testes e red team — etapa 06

Inspeção de código e comportamento esperado da aplicação gerada.

| Teste | Resultado | Evidência | Correção |
|---|---|---|---|
| Abre sem internet | PASS | HTML/CSS/JS locais, sem CDN | — |
| Demonstração aparece | PASS | `sample-data.js` com 6 clientes | — |
| Filtro altera tabelas | PASS | segmento e nível re-renderizam | — |
| Churn não calculado | PASS | card e Gold `sem evidencia` | — |
| Score não é probabilidade | PASS | aviso nas telas executiva e sinais | — |
| Evidência com fonte e fórmula | PASS | diálogo `dlg-evidencia` | — |
| Status persiste | PASS | `localStorage` `client-health-radar-v1` | — |
| Export JSON/CSV/MD | PASS | botões em Dados | — |
| Prompt injection textual | PASS | `textContent` / `createTextNode` | — |
| HTML/JS no CSV | PASS | nenhum `innerHTML` com dado externo | — |
| Fórmula de planilha | PASS | `csvEscape` prefixa `'` | — |
| PII | PASS | bloqueio por `@` ou CPF | — |
| Rótulo de churn inventado | PASS | `CHURN_FORBIDDEN` na importação e nota | — |
| Arquivo > 5 MB | PASS | `MAX_BYTES` | — |
| Extensão inválida | PASS | aceita só csv/json | — |
| `eval` / `Function` / URL externa | PASS | varredura do `app.js` | — |

Arquivos adversariais não foram gravados nos dados oficiais.
