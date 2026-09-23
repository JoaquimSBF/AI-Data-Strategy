# Validação do case

Status: `PASS`

## Dados

| Arquivo | Linhas brutas | Observação |
|---|---:|---|
| audiencia_portal.csv | 32 | 30 linhas de negócio, 1 duplicata exata e 1 inválida |
| conteudos.csv | 26 | 24 conteúdos, 1 duplicata exata e 1 inválido |
| search_console.csv | 37 | 36 medições e 1 linha sem medição |
| auditoria_sites.csv | 18 | 6 meses × 3 sites |
| visibilidade_ia.csv | 60 | 6 meses × 5 temas × 2 mecanismos |
| metas.csv | 5 | todas com direção e vigência |

## Verificações executadas

- CSVs abrem e possuem cabeçalho.
- Quantidades conferidas.
- Duas duplicatas didáticas confirmadas.
- Três linhas inválidas intencionais confirmadas.
- Direções das metas válidas.
- Varredura dos CSVs sem e-mail ou CPF em claro.
- Gerador determinístico executado com sucesso.
- Oito prompts presentes.
- Cada prompt separa `GUIA DO ALUNO`, `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
- Etapas com entrada listam nome e pasta de todos os arquivos necessários.
- Guias de arquivos, funcionamento e funcionalidades presentes.
- PDFs individuais e pacote completo gerados.

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

## Limite

O produto ainda não foi implementado. Ele será construído pelo aluno na etapa 05, após executar as etapas de dados, evidências e contrato.
