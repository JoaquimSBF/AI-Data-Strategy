# Harness Engineering · Allura Finance

Versao **low-code com prompts** do mesmo caso do notebook `Data_AI.ipynb`.
Mesma jornada medalhao + EDA + RAG + entrega executiva, mas usando Gemini/ChatGPT em vez de codigo.

## Relacao com o notebook

| Etapa | Notebook `Data_AI.ipynb` | Harness (prompts) |
|-------|--------------------------|-------------------|
| Limpeza | Silver com colunas `*_padrao` | Silver canônico (`data`, `tipo`, `produto`, `canal`) |
| Gold | DuckDB em memoria | CSVs em `data/gold/` |
| EDA | Graficos Plotly na tela | `outputs/analise_final.md` |
| RAG | `outputs/rag_context.json` com chunks | `rag/rag_context.md` + JSON estruturado |
| Front | Streamlit (Allura Finance Lab) | **Board Pack** para diretoria |

Os numeros de negocio devem bater entre as duas trilhas. O harness documenta o **contrato de entrega** que o aluno precisa produzir no chat.

## Estrutura

```
Harness Engineering/
  data/
    bronze/     # CSVs crus (mesmos do repo raiz)
    silver/     # CSVs limpos
    gold/       # estrela / KPIs (CSVs exportados)
  prompts/
    prompts.md/   # fonte editavel (Cursor / Git)
    prompts_pdf/  # versao para turma (copiar no Gemini)
  rag/          # contexto e historico de perguntas
  outputs/      # analise_final, board pack, relatorios, juiz
  run_harness.py  # valida o pipeline e gera artefatos de referencia
```

## Como usar (turma)

1. Abra o chat (Gemini Gem / ChatGPT / Custom GPT).
2. Cole `prompts/prompts.md/00_mestre.md` nas instrucoes fixas (opcional).
3. Para cada etapa, cole o prompt correspondente **e os dados** (CSVs ou trechos).
4. No final de cada prompt ha a secao **ONDE SALVAR** — copie a saida do modelo para o caminho indicado.
5. Na etapa 05, entregue o **Board Pack** (`outputs/board_pack.md`).

O chat **nao grava sozinho** no disco. O aluno salva manualmente cada artefato.

## Ordem das etapas

1. `01_limpeza_bronze_silver.md` → Silver + `outputs/limpeza_relatorio.md`
2. `02_elt_silver_gold.md` → Gold CSVs + `outputs/elt_relatorio.md`
3. `03_eda_analise_final.md` → `outputs/analise_final.md`
4. `04_rag_assistente.md` (+ `04b_juiz.md` para avaliar respostas)
5. `05_board_pack_diretoria.md` → `outputs/board_pack.md` (entrega final)

## Validar localmente (professor / QA)

```bash
cd "Harness Engineering"
python run_harness.py
```

Gera/atualiza Silver, Gold, `analise_final.md`, `board_pack.md`, RAG e `outputs/teste_harness.md` com PASS/FAIL.

## Formatos para turma

- `prompts/prompts.md/*.md` → fonte editavel
- `prompts/prompts_pdf/*.pdf` → abrir e copiar no Gemini/GPT
- `prompts/prompts_pdf/Harness_Engineering_Prompts_Completo.pdf` → pacote unico

Cases da turma (outra logica, HTML sem instalar): pasta `../Cases Alunos/`.
