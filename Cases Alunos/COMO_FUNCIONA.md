# Como funcionam os 4 produtos

Skills & Go — AI Data Strategy. Cada aluno monta **prompt a prompt** ate um HTML. Sem instalar nada (Gemini/ChatGPT + navegador).

Regra de ouro: o chat **nao grava arquivo**. Voce cola o prompt, cola os CSVs/JSON no bloco `<<< >>>`, copia a resposta para a pasta que o prompt indica (**ONDE SALVAR**). O mapa de cada case tem a tabela completa.

| Aluno | Produto que sai no prompt 04 | Pasta |
|-------|------------------------------|--------|
| Juliana Caballero | Mesa CS (pre/pos reuniao) | `CSOps Reunioes - Juliana Caballero/` |
| Eduardo Campregher | Landing com KPI e PT/EN/ES | `Landing de Dados - Eduardo Campregher/` |
| Sayuri Yamabe | Radar de risco (sinais, nao modelo) | `Risco de Churn - Sayuri Yamabe/` |
| Meliy Toda | Painel orcado vs realizado | `Orcado vs Realizado - Meliy Toda/` |

## Ordem igual para os quatro

0. `prompts/md/00_mestre.md` — instrucao fixa, sem CSV.
1. `01_…` — entrada em `dados/` → saida em `outputs/`.
2. `02_…` — entrada em `outputs/` → JSON do produto.
3. `03_…` — contrato da tela (ainda sem HTML).
4. `04_…` — o produto para usar ja esta em **`produto/index.html`**. Abra no navegador.
5. `05_…` — juiz.

Como usar cada tela: `prompts/md/MAPA_FUNCIONALIDADE.md` (PDF na pasta `pdf/`). Guia dos quatro: `Cases Alunos/MAPA_FUNCIONALIDADE.md`.

## Onde estao os arquivos

Uma pasta `prompts/` por case, com duas pastas dentro (igual a Allura):

- `prompts/md/` — `.md` editavel (prompts, mapa, como funciona)
- `prompts/pdf/` — PDFs para a turma, incluindo `Prompts_Completo.pdf`
