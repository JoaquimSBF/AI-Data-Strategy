# Testes e red team — etapa 06

Inspeção de código e comportamento esperado da aplicação gerada.

| Teste | Resultado | Evidência | Correção |
|---|---|---|---|
| Abre sem internet | PASS | HTML/CSS/JS locais, sem CDN | — |
| Demonstração aparece | PASS | `sample-data.js` com 7 requisitos | — |
| Filtro altera tabelas | PASS | `filtro-tipo` re-renderiza views | — |
| Requisito sempre com fonte | PASS | Gold `requisito_sempre_com_fonte` | — |
| E99 não vira requisito | PASS | evidência isolada na quarentena | — |
| Evidência com fonte e fórmula | PASS | diálogo `dlg-evidencia` | — |
| Status persiste | PASS | `localStorage` `discovery-workbench-v1` | — |
| Export JSON/CSV/MD | PASS | botões em Dados | — |
| Prompt injection textual | PASS | `textContent` / `createTextNode` | — |
| HTML/JS no CSV | PASS | nenhum `innerHTML` com dado externo | — |
| Fórmula de planilha | PASS | `csvEscape` prefixa `'` | — |
| PII | PASS | bloqueio por `@` ou CPF | — |
| Arquivo > 5 MB | PASS | `MAX_BYTES` | — |
| Extensão inválida | PASS | aceita só csv/json | — |
| `eval` / `Function` / URL externa | PASS | varredura do `app.js` | — |

Arquivos adversariais não foram gravados nos dados oficiais.
