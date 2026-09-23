# Validação do case

Status: `PASS`

## Dados

| Arquivo | Linhas brutas | Observação |
|---|---:|---|
| clientes.csv | 8 | 6 válidos, 1 duplicata e 1 TESTE sem data |
| projetos.csv | 7 | 6 válidos; PR99 com atraso negativo |
| eventos.csv | 8 | comparecimento inconsistente padronizado |
| tickets.csv | 7 | 6 válidos; T99 com SLA n/a |
| nps.csv | 5 | 4 válidos; CL04 n/a; CL05 ausente |
| metas.csv | 3 | inclui churn, que permanece sem evidencia |

## Verificações executadas

- CSVs abrem e possuem cabeçalho.
- Quantidades conferidas.
- Duplicata didática de CL06 confirmada.
- CL99, PR99, T99 e NPS n/a isolados.
- `data_saida` vazia em todos os clientes.
- Direções das metas válidas.
- Varredura dos CSVs sem e-mail ou CPF em claro.
- Gerador determinístico executado com sucesso.
- Oito prompts presentes.
- Cada prompt separa `GUIA DO ALUNO`, `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
- Etapas com entrada listam nome e pasta de todos os arquivos necessários.
- Guias de arquivos, funcionamento e funcionalidades presentes.
- PDFs individuais e pacote completo gerados.
- Harness Silver/Gold executado: 6 clientes, 3 sinais altos, 4 SLAs, churn sem evidencia.

## Escopo validado

- dados sintéticos;
- limpeza e Silver;
- inteligência e Gold;
- livro de evidências;
- backlog operacional;
- contrato de produto;
- aplicação local com persistência;
- testes adversariais;
- juiz com rubrica.
