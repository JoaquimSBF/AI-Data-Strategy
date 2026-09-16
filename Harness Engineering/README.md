# Harness Engineering · Allura Finance

Pasta low-code de prompts + destino dos arquivos (medalhao).

## Estrutura

```
Harness Engineering/
  data/
    bronze/     # CSVs crus
    silver/     # CSVs limpos
    gold/       # estrela / KPIs
  prompts/      # prompts por etapa (com ONDE SALVAR no final)
  rag/          # contexto e historico de perguntas
  outputs/      # analise_final, board pack, logs de juiz
```

## Como usar

1. Abra o chat (Gemini Gem / ChatGPT / Custom GPT).
2. Cole o `prompts/00_mestre.md` nas instrucoes fixas (opcional).
3. Para cada etapa, cole o prompt correspondente e os dados.
4. No final do prompt ha a secao **ONDE SALVAR**.
5. Copie a saida do modelo e salve no caminho indicado.

## Ordem

1. `01_limpeza_bronze_silver.md`
2. `02_elt_silver_gold.md`
3. `03_eda_analise_final.md`
4. `04_rag_assistente.md` (+ `04b_juiz.md` se quiser)
5. `05_board_pack_diretoria.md`

## Observacao

O chat nao grava sozinho no disco. Este harness define o contrato:
prompt -> artefato -> pasta.

Cases da turma (outra logica, HTML sem instalar): pasta `../Cases Alunos/`.

## Formatos

- `prompts/*.md` → fonte editavel (Cursor / Git)
- `prompts_pdf/*.pdf` → versao para turma (abrir e copiar no Gemini/GPT)
- `prompts_pdf/Harness_Engineering_Prompts_Completo.pdf` → tudo em um arquivo
