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

## Como baixar todo o conteúdo

**Opção 1 — Git (recomendado)**

```bash
git clone https://github.com/JoaquimSBF/AI-Data-Strategy.git
cd AI-Data-Strategy
```

**Opção 2 — ZIP (sem Git)**

1. Abra https://github.com/JoaquimSBF/AI-Data-Strategy
2. Clique em **Code** → **Download ZIP**
3. Extraia a pasta no seu computador

O repositório já inclui o notebook `Data_AI.ipynb`, os CSVs de entrada em `data/bronze/`, os PPTs, o app Streamlit e os cases da turma. As camadas Silver, Gold e `outputs/` são geradas ao executar o notebook.

## Execução local

1. Baixe o repositório (clone ou ZIP)
2. Copie `.env.example` para `.env` e preencha `GEMINI_API_KEY=sua_chave`
3. Abra e execute `Data_AI.ipynb` no **Google Colab** (recomendado) ou localmente
4. Na última célula, clique em **Abrir Allura Finance Lab** — no Colab o link abre direto no navegador, sem precisar de Jupyter no PC

> Todos os dados do caso são **100% sintéticos** e não representam informações reais da Allura Finance.

## Requisitos

- Python 3.11+
- Dependências instaladas automaticamente no notebook (DuckDB, Plotly, scikit-learn, google-genai, pydantic-ai, streamlit)

## Autor

[JoaquimSBF](https://github.com/JoaquimSBF)
