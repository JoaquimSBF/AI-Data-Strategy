# ETAPA 01 — Ler e limpar metricas

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/Landing de Dados - Eduardo Campregher/`

1. No mesmo chat do `00_mestre.md`, cole **este arquivo inteiro**.
2. Cole no bloco `<<< >>>` o conteudo de:

| Arquivo | Pasta |
|---------|--------|
| `metricas.csv` | `dados/` |
| `produtos.csv` | `dados/` |
| `canais.csv` | `dados/` |
| `textos_ui.csv` | `dados/` |
| `metas.csv` | `dados/` |

3. Grave a resposta em **ONDE SALVAR**.

Tarefa:
1) Problemas por arquivo (mes misturado, milhar com ponto, duplicata, conversao negativa, traducao vazia).
2) Regras reproduziveis. ano_mes = YYYY-MM. Numeros com ponto decimal. Canal/produto canonicos.
3) Descarte valor < 0, n/a, duplicata de ano_mes+kpi. Nao invente lead de 2025-03 se estiver n/a.
4) textos_ui: nao invente EN/ES vazio.
5) CSVs limpos + checklist. Sem landing ainda.

Dados:
<<<
[COLE os CSVs de dados/]
>>>

## ONDE SALVAR
- `outputs/01_limpeza.md`
- `outputs/metricas.csv`
- `outputs/produtos.csv`
- `outputs/canais.csv`
- `outputs/textos_ui.csv`
- `outputs/metas.csv`
- `outputs/linhas_invalidas.csv`
