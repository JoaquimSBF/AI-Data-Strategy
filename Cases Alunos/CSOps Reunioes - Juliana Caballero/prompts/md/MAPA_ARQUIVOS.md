# Mapa de arquivos — Mesa CS (Juliana Caballero)

Pasta raiz: `Cases Alunos/CSOps Reunioes - Juliana Caballero/`

Prompts: `prompts/md/` (editar) e `prompts/pdf/` (colar no Gemini).

Como usar: abra o Gemini/ChatGPT → cole o prompt da etapa → cole os **arquivos de entrada** no bloco `<<< >>>` → copie a resposta para a **saida**.

| Etapa | Prompt (cole no LLM) | Entrada (abrir e colar) | Pasta da entrada | Saida (onde gravar) |
|-------|----------------------|-------------------------|------------------|---------------------|
| 00 | `prompts/md/00_mestre.md` | nada | — | nada (instrucao fixa) |
| 01 | `prompts/md/01_limpar.md` | `clientes.csv`, `reunioes.csv`, `transcricoes.csv`, `metas.csv` (+ txt opcional) | `dados/` e `dados/transcricoes/` | `outputs/01_limpeza.md` + CSVs em `outputs/` |
| 02 | `prompts/md/02_fichas.md` | CSVs limpos da etapa 01 | `outputs/` | `outputs/02_fichas.json` e `outputs/02_fichas.md` |
| 03 | `prompts/md/03_contrato.md` | `02_fichas.json` | `outputs/` | `outputs/03_contrato_produto.md` |
| 04 | `prompts/md/04_produto.md` | `02_fichas.json` + `03_contrato_produto.md` | `outputs/` | **`produto/index.html`** |
| 05 | `prompts/md/05_juiz.md` | `index.html` + `02_fichas.json` | `produto/` e `outputs/` | `outputs/05_juiz.md` |

O chat **nao** grava no disco. Voce copia e salva.

Pacote unico (estilo Allura): `prompts/pdf/Prompts_Completo.pdf`.
Produto para usar: `produto/index.html`.
Como mexer na tela: `prompts/md/MAPA_FUNCIONALIDADE.md`.
