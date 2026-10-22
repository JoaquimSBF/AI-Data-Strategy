# Mapa de arquivos — Mesa de Expansão e Risco

GUIA DO ALUNO não se cola. Copie só INÍCIO–FIM e anexe os arquivos da lista.

| Etapa | Anexar | Gravar em |
|---|---|---|
| 00 | nada | nada |
| 01 | dados/*.csv + README_DADOS.md | outputs/silver/ |
| 02 | silver + README_DADOS.md | outputs/gold/ |
| 03 | 02 + gold | outputs/03_* |
| 04 | 02, 03, gold | outputs/04_contrato_produto.md |
| 05 | 03, 04, gold | produto/ |
| 06 | produto + contrato + evidencias | outputs/06_* |
| 07 | produto + outputs 01–06 + gold | outputs/07_juiz.md |
| 08 | mcp/mcp.json.example + mcp/README.md | outputs/08_guia_mcp.md |

No final da etapa 05, abra `http://127.0.0.1:8769/index.html` com `python scripts/abrir_produto.py`.
