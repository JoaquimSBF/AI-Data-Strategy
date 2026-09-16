# AI Data Strategy — Allura Finance

Materiais do curso **Skills & Go (Alura)** e notebook hands-on de **Data Strategy + IA aplicada** para a Allura Finance.

## Materiais do curso

- `Aula1_Fundamentos_IA_Generativa_Alura.pptx` — fundamentos de IA generativa (Aula 1)
- `Passo_a_passo_API_Key_Google_AI_Studio.pptx` — como criar API Key no Google AI Studio (Gemini)
- `Passo_a_passo_API_Key_Grok_xAI.pptx` — como criar API Key no Grok (xAI)
- `Mapa_do_Projeto_Data_AI.pptx` — mapa do projeto Allura Finance (Data & AI)

## Notebook `Data_AI.ipynb`

Jornada completa da ingestão ao assistente com RAG e guardrails:

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
