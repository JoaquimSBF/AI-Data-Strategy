# Mapa de arquivos — Mesa de Discovery

Cada PDF tem GUIA DO ALUNO (não colar), INÍCIO DO PROMPT e FIM DO PROMPT.

| Etapa | Entrada | Saída |
|---|---|---|
| 00 | nenhuma | contexto |
| 01 | dados/*.csv | outputs/silver |
| 02 | silver | outputs/gold |
| 03 | gold | backlog |
| 04 | backlog | contrato |
| 05 | contrato + gold | produto/ e `http://127.0.0.1:8767/index.html` |
| 06 | produto | testes |
| 07 | tudo | juiz |
