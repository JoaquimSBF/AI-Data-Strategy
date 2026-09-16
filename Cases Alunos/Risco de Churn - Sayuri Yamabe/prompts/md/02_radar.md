# ETAPA 02 — JSON do radar (sinais, nao previsao)

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/Risco de Churn - Sayuri Yamabe/`

1. Cole **este arquivo inteiro**.
2. Cole no `<<< >>>` os CSVs da etapa 01, pasta `outputs/` (nao `dados/`):

| Arquivo | Pasta |
|---------|--------|
| `clientes.csv`, `eventos.csv`, `snapshot_status.csv` | `outputs/` |

Regras de pontos: +3 inativo; +3 cancelamento_solicitado; +2 downgrade; +2 se tickets>=2; +1 se 1 ticket.
Faixa: alto >=3; medio >=1; baixo = 0.
Proibido: probabilidade, percent_churn, score_ml.

Material:
<<<
[COLE os CSVs de outputs/]
>>>

## ONDE SALVAR
- `outputs/02_radar.json`
- `outputs/02_radar.md`
