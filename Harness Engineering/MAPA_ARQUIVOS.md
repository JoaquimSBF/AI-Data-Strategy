# Mapa rapido: etapa -> arquivo

| Etapa | Arquivo(s) |
|-------|------------|
| Bronze (entrada) | `data/bronze/*.csv` (movimentacoes, clientes, produtos, receita, metas) |
| Limpeza | `data/silver/*.csv` + `outputs/limpeza_relatorio.md` + `outputs/linhas_invalidas/*.csv` |
| ELT/Gold | `data/gold/dim_*.csv`, `fato_movimentacoes.csv`, `base_analise.csv`, `kpis_mensais.csv`, `mix_produto.csv`, `mix_canal.csv`, `receita_mensal.csv`, `status_snapshot.csv` + `outputs/elt_relatorio.md` |
| EDA | `outputs/analise_final.md` (+ opcional `outputs/eda_notas.md`) |
| RAG contexto | `rag/rag_context.md` + `outputs/rag_context.json` |
| RAG chat | `rag/perguntas_respostas.md` + `outputs/rag_ultima_resposta.md` |
| Juiz | `outputs/juiz_avaliacoes.md` |
| Board Pack | `outputs/board_pack.md` (+ opcional `outputs/board_pack.html`) |
| QA automatizado | `outputs/teste_harness.md` (via `python run_harness.py`) |

## Entrega final para diretoria

O artefato principal e `outputs/board_pack.md`, montado a partir de:

- `outputs/analise_final.md`
- `data/gold/kpis_mensais.csv`
- `data/gold/mix_produto.csv` / `mix_canal.csv`
- `data/gold/receita_mensal.csv`
- `data/gold/status_snapshot.csv`
- `data/silver/metas.csv`

Deve terminar com `Pronto para Board Pack: SIM/NAO` e checklist do que falta.
