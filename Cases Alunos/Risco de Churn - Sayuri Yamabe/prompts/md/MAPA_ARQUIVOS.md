# Mapa de arquivos — Radar de risco (Sayuri Yamabe)

Pasta raiz: `Cases Alunos/Risco de Churn - Sayuri Yamabe/`

Prompts: `prompts/md/` (editar) e `prompts/pdf/` (colar no Gemini).

Cole o prompt no LLM → cole a entrada no `<<< >>>` → grave a saida. O chat nao salva sozinho.

| Etapa | Prompt (cole no LLM) | Entrada | Pasta da entrada | Saida |
|-------|----------------------|---------|------------------|--------|
| 00 | `prompts/md/00_mestre.md` | nada | — | nada |
| 01 | `prompts/md/01_limpar.md` | `clientes.csv`, `eventos.csv`, `snapshot_status.csv`, `metas.csv` | `dados/` | `outputs/` (CSVs sem PII + BURACO) |
| 02 | `prompts/md/02_radar.md` | CSVs da etapa 01 | `outputs/` | `outputs/02_radar.json` |
| 03 | `prompts/md/03_contrato.md` | `02_radar.json` | `outputs/` | `outputs/03_contrato_produto.md` |
| 04 | `prompts/md/04_produto.md` | JSON + contrato | `outputs/` | **`produto/index.html`** |
| 05 | `prompts/md/05_juiz.md` | HTML + JSON | `produto/` e `outputs/` | `outputs/05_juiz.md` |

Pacote unico: `prompts/pdf/Prompts_Completo.pdf`.
Produto para usar: `produto/index.html`.
Como mexer na tela: `prompts/md/MAPA_FUNCIONALIDADE.md`.
