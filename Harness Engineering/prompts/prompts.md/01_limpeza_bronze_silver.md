# MODO: LIMPEZA (Bronze -> Silver)

Contexto: Allura Finance. Vou colar CSVs crus (movimentacoes, clientes, produtos, receita, metas). Pode vir sujo: tipos misturados, nulos, categorias inconsistentes, PII.

Tarefa:
1) Para cada tabela, liste problemas encontrados (qualidade).
2) Proponha regras de limpeza claras e reproduziveis.
3) Mostre ANTES (amostra 5 linhas) e DEPOIS (amostra 5 linhas) por tabela.
4) Em clientes: substitua CPF/email/telefone por hash/pseudonimo (nao mostre o valor original depois).
5) Padronize: datas, ano_mes, tipo (captacao/resgate), canal, produto, status, segmento, valores numericos.
6) Remova ou sinalize linhas invalidas (valor <= 0, data nula, tipo desconhecido) e diga o criterio.
7) Entregue um checklist final: o que ficou OK / o que ainda e risco.
8) Ao final, entregue tambem o conteudo CSV limpo de cada tabela (pronto para copiar/salvar).

Formato de saida:
- Resumo executivo (5 linhas)
- Por tabela: problemas | regras | amostra depois | contagem linhas antes/depois
- Dicionario curto das colunas Silver finais
- Blocos CSV limpos nomeados
- Status: OK ou NOK (e por que)

Nao invente metricas de negocio ainda. So limpeza e padronizacao.

Dados:
<<<
[COLE OS CSVs OU AMOSTRAS AQUI]
>>>

## ONDE SALVAR
Salve manualmente em:

- `data/bronze/` -> CSVs originais (se ainda nao estiverem la)
  - movimentacoes.csv
  - clientes.csv
  - produtos.csv
  - receita.csv
  - metas.csv

- `data/silver/` -> CSVs limpos gerados nesta etapa
  - movimentacoes.csv
  - clientes.csv
  - produtos.csv
  - receita.csv
  - metas.csv

- `outputs/limpeza_relatorio.md` -> resumo textual da limpeza
