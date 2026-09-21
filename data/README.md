# Dados — Allura Finance

## O que fica no repositório

Somente **`bronze/`** — CSVs crus de entrada (100% sintéticos):

- `movimentacoes.csv`
- `clientes.csv`
- `produtos.csv`
- `receita.csv`
- `metas.csv`

## O que é gerado ao rodar o notebook

| Camada | Pasta | Quando aparece |
|--------|-------|----------------|
| Silver | `data/silver/` | Etapas de limpeza e pseudonimização |
| Gold | `data/gold/` ou DuckDB | Etapa ELT / star schema |
| RAG | `outputs/rag_context.json` | Etapa RAG (usado pelo Streamlit) |

Essas pastas **não** precisam ser versionadas — o `Data_AI.ipynb` recria tudo a partir do Bronze.

## Colab

Na célula de Bronze, faça upload dos 5 CSVs (podem ser os mesmos arquivos desta pasta).
