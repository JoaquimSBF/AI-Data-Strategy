# ETAPA 01 — Ler, limpar e declarar o buraco

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/Risco de Churn - Sayuri Yamabe/`

1. Cole **este arquivo inteiro** no mesmo chat do mestre.
2. Cole no `<<< >>>`:

| Arquivo | Pasta |
|---------|--------|
| `clientes.csv` | `dados/` |
| `eventos.csv` | `dados/` |
| `snapshot_status.csv` | `dados/` |
| `metas.csv` | `dados/` |

Tarefa: qualidade; saida de clientes **sem** nome/cpf/email/telefone; eventos invalidos em linhas_invalidas; declare se existe data de saida (nao existe → churn_pct = sem evidencia); nao invente coluna; sem ranking ainda.

Dados:
<<<
[COLE os CSVs de dados/]
>>>

## ONDE SALVAR
- `outputs/01_limpeza.md` (secao BURACO)
- `outputs/clientes.csv` (sem PII)
- `outputs/eventos.csv`
- `outputs/snapshot_status.csv`
- `outputs/metas.csv`
- `outputs/linhas_invalidas.csv`
