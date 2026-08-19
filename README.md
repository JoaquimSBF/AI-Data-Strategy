# Allura Finance — Data & AI Strategy

Notebook hands-on de **Data Strategy + IA aplicada** para a Allura Finance.

## Conteúdo

- **`Data_AI.ipynb`** — jornada completa da ingestão ao assistente com RAG e guardrails:
  1. Bronze — upload e inspeção dos dados
  2. Silver — limpeza, pseudonimização e qualidade
  3. Modelagem — arquitetura medalhão + estrela
  4. Gold — DuckDB analítico
  5. EDA — KPIs de negócio
  6. RAG — lexical, semântico e híbrido
  7. Guardrails — Pydantic AI, escopo, PII e evidências
  8. Aplicação — assistente NL + Streamlit

## Execução local

1. Clone o repositório
2. Coloque os CSVs em `data/bronze/` (movimentacoes, clientes, produtos, receita, metas)
3. Crie um `.env` com `GEMINI_API_KEY=sua_chave`
4. Abra e execute `Data_AI.ipynb`

> Todos os dados do caso são **100% sintéticos** e não representam informações reais da Allura Finance.

## Requisitos

- Python 3.11+
- Dependências instaladas automaticamente no notebook (DuckDB, Plotly, scikit-learn, google-genai, pydantic-ai, streamlit)

## Autor

[JoaquimSBF](https://github.com/JoaquimSBF)
