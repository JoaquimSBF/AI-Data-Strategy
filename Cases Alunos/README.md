# Cases Alunos — Skills & Go

Pasta completa dos **3 cases** da turma (prompts + dados + outputs + produto HTML).

## Cases

| Case | Pasta |
|------|-------|
| 01 — Inteligência do Portal | `Inteligencia do Portal - Case 01/` |
| 02 — Mesa de Discovery | `Mesa de Discovery - Case 02/` |
| 03 — Radar Saúde do Cliente | `Radar Saude do Cliente - Case 03/` |

## Estrutura de cada case

```
Case XX/
  dados/          # CSVs de entrada (bronze)
  outputs/        # silver, gold, relatórios, juiz, red team
  prompts/md/     # prompts editáveis
  prompts/pdf/    # prompts para colar no Gemini/GPT
  produto/        # app HTML (abra index.html no navegador)
  scripts/        # harness automatizado (opcional)
  README.md       # guia do case
```

## Como usar

1. Abra o `README.md` do case escolhido.
2. Cole os prompts (`prompts/pdf/` ou `prompts/md/`) no Gemini/ChatGPT.
3. Siga a ordem 01 → 07 e salve os artefatos em `outputs/`.
4. Abra `produto/index.html` no navegador para ver o resultado.

Documento geral da pasta: `README_PROJETO.pdf`.
