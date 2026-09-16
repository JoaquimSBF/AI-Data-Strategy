# ETAPA 01 — Ler e limpar orcamento e realizado

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/Orcado vs Realizado - Meliy Toda/`

1. Cole **este arquivo inteiro** no mesmo chat do mestre.
2. Cole no `<<< >>>`:

| Arquivo | Pasta |
|---------|--------|
| `centros_custo.csv` | `dados/` |
| `orcamento.csv` | `dados/` |
| `realizado.csv` | `dados/` |
| `metas.csv` | `dados/` |

Canonico TI/RH/Marketing/Operacoes. Descarte valor <=0 e CC desconhecido.
**Nao** descarte TI no CC de RH — marque `alerta_cc_divergente`. Email vira hash.

Dados:
<<<
[COLE os CSVs de dados/]
>>>

## ONDE SALVAR
- `outputs/01_limpeza.md`
- `outputs/centros_custo.csv`
- `outputs/orcamento.csv`
- `outputs/realizado.csv`
- `outputs/metas.csv`
- `outputs/linhas_invalidas.csv`
