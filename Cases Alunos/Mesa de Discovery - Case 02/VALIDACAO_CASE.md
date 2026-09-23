# Validação do case

Status: `PASS`

## Dados

| Arquivo | Linhas brutas | Observação |
|---|---:|---|
| reunioes.csv | 7 | 5 válidas, 1 duplicata exata e 1 sem data |
| evidencias.csv | 12 | 11 válidas; E99 adversária e reunião inválida |
| stakeholders.csv | 5 | papéis, sem nome |
| sistemas.csv | 4 | API inconsistente padronizada |
| restricoes.csv | 4 | booleanos mistos |
| ideias.csv | 3 | 1 rejeitada |
| metas.csv | 3 | todas com direção e vigência |

## Verificações executadas

- CSVs abrem e possuem cabeçalho.
- Quantidades conferidas.
- Duplicata didática de R05 confirmada.
- Reunião sem data e E99 isoladas.
- Direções das metas válidas.
- Varredura dos CSVs sem e-mail ou CPF em claro.
- Gerador determinístico executado com sucesso.
- Oito prompts presentes.
- Cada prompt separa `GUIA DO ALUNO`, `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
- Etapas com entrada listam nome e pasta de todos os arquivos necessários.
- Guias de arquivos, funcionamento e funcionalidades presentes.
- PDFs individuais e pacote completo gerados.
- Harness Silver/Gold executado: 7 requisitos, 100% com fonte, MVP 7 versus 8.

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
