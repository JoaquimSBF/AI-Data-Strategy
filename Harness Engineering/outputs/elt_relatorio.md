# Relatorio ELT / Gold

Status: **OK**

Fonte: Silver (`clientes`, `movimentacoes`, `produtos`, `receita`).
`metas.csv` nao entra na estrela — permanece no Silver para EDA/Board (comparacao com realizado).
Churn **mensal** nao e calculavel: Silver so tem `status` pontual, sem data de inativacao. Entregue snapshot.

## Diagrama textual da estrela

```
dim_cliente (cliente_id)
    nome, segmento, status, data_entrada
           \
            \
dim_produto (produto) ---- fato_movimentacoes ---- dim_canal (canal)
    classe, taxa_admin_aa,     id_mov, data, ano_mes,
    meta_captacao_mes          tipo, valor,
                               valor_captacao, valor_resgate,
                               cliente_id, produto, canal
                                      |
                                      +--> base_analise (fato LEFT JOIN dims)
                                      +--> kpis_mensais
                                      +--> mix_produto
                                      +--> mix_canal

receita_mensal (ano_mes, valor_receita)  -- independente, a partir de silver.receita
status_snapshot (status, qtd, pct)       -- a partir de dim_cliente.status
```

Hashes de PII do Silver **nao** foram levados ao Gold.

## SQL DuckDB por objeto

### dim_cliente
```sql
CREATE TABLE dim_cliente AS
SELECT cliente_id, nome, segmento, status, data_entrada
FROM read_csv_auto('data/silver/clientes.csv');
```

### dim_produto
```sql
CREATE TABLE dim_produto AS
SELECT produto, classe, taxa_admin_aa, meta_captacao_mes
FROM read_csv_auto('data/silver/produtos.csv');
```

### dim_canal
```sql
CREATE TABLE dim_canal AS
SELECT DISTINCT canal
FROM read_csv_auto('data/silver/movimentacoes.csv')
ORDER BY canal;
```

### fato_movimentacoes
```sql
CREATE TABLE fato_movimentacoes AS
SELECT
    id_mov, data, ano_mes, tipo, valor, produto, canal, cliente_id,
    CASE WHEN tipo = 'captacao' THEN valor ELSE 0.0 END AS valor_captacao,
    CASE WHEN tipo = 'resgate' THEN valor ELSE 0.0 END AS valor_resgate
FROM read_csv_auto('data/silver/movimentacoes.csv');
```

### kpis_mensais
```sql
CREATE TABLE kpis_mensais AS
SELECT
    ano_mes,
    SUM(valor_captacao) AS captacao,
    SUM(valor_resgate) AS resgate,
    SUM(valor_captacao) - SUM(valor_resgate) AS captacao_liquida,
    COUNT(DISTINCT cliente_id) AS clientes_movimentados,
    COUNT(DISTINCT id_mov) AS qtd_movimentos
FROM fato_movimentacoes
GROUP BY ano_mes
ORDER BY ano_mes;
```

### mix_produto / mix_canal
```sql
CREATE TABLE mix_produto AS
SELECT produto,
       SUM(valor_captacao) AS captacao,
       SUM(valor_resgate) AS resgate,
       SUM(valor_captacao) - SUM(valor_resgate) AS captacao_liquida,
       COUNT(*) AS qtd
FROM fato_movimentacoes
GROUP BY produto
ORDER BY captacao DESC;

CREATE TABLE mix_canal AS
SELECT canal,
       SUM(valor_captacao) AS captacao,
       SUM(valor_resgate) AS resgate,
       SUM(valor_captacao) - SUM(valor_resgate) AS captacao_liquida,
       COUNT(*) AS qtd
FROM fato_movimentacoes
GROUP BY canal
ORDER BY captacao DESC;
```

### receita_mensal
```sql
CREATE TABLE receita_mensal AS
SELECT ano_mes, SUM(valor_receita) AS valor_receita
FROM read_csv_auto('data/silver/receita.csv')
GROUP BY ano_mes
ORDER BY ano_mes;
```

### status_snapshot (nao e churn mensal)
```sql
CREATE TABLE status_snapshot AS
SELECT status,
       COUNT(*) AS qtd,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM dim_cliente
GROUP BY status
ORDER BY status;
```

### base_analise
```sql
CREATE TABLE base_analise AS
SELECT
    f.id_mov, f.data, f.ano_mes, f.tipo, f.valor,
    f.valor_captacao, f.valor_resgate,
    f.cliente_id, c.nome, c.segmento, c.status, c.data_entrada,
    f.produto, p.classe, p.taxa_admin_aa, p.meta_captacao_mes,
    f.canal
FROM fato_movimentacoes f
LEFT JOIN dim_cliente c USING (cliente_id)
LEFT JOIN dim_produto p USING (produto)
LEFT JOIN dim_canal d USING (canal);
```

## Contagens Gold
| objeto | linhas |
| --- | --- |
| dim_cliente | 40 |
| dim_produto | 5 |
| dim_canal | 3 |
| fato_movimentacoes | 180 |
| base_analise | 180 |
| kpis_mensais | 7 |
| mix_produto | 5 |
| mix_canal | 3 |
| receita_mensal | 7 |
| status_snapshot | 2 |

## Exemplos

### kpis_mensais (todas as linhas)
| ano_mes | captacao | resgate | captacao_liquida | clientes_movimentados | qtd_movimentos |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 240709.83 | 519723.03 | -279013.20 | 19 | 21 |
| 2025-02 | 585529.05 | 382420.23 | 203108.82 | 19 | 26 |
| 2025-03 | 504054.92 | 794471.73 | -290416.81 | 23 | 32 |
| 2025-04 | 610291.15 | 578010.58 | 32280.57 | 16 | 29 |
| 2025-05 | 561334.88 | 546083.50 | 15251.38 | 20 | 29 |
| 2025-06 | 386316.82 | 674588.98 | -288272.16 | 20 | 25 |
| 2025-07 | 389676.10 | 356005.16 | 33670.94 | 14 | 18 |

### base_analise (5 linhas)
| id_mov | data | ano_mes | tipo | valor | valor_captacao | valor_resgate | cliente_id | nome | segmento | status | data_entrada | produto | classe | taxa_admin_aa | meta_captacao_mes | canal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0001 | 2025-02-16 00:00:00 | 2025-02 | resgate | 21552.35 | 0.00 | 21552.35 | C021 | Elena Costa | Varejo | ativo | 2024-06-02 00:00:00 | Fundo Multimercado | Multimercado | 1.36 | 1200000.00 | App |
| M0002 | 2025-03-13 00:00:00 | 2025-03 | captacao | 20929.45 | 20929.45 | 0.00 | C035 | Nicolas Santos | Private | ativo | 2024-03-11 00:00:00 | Tesouro Selic | Renda Fixa | 1.67 | 500000.00 | App |
| M0003 | 2025-02-27 00:00:00 | 2025-02 | captacao | 62717.41 | 62717.41 | 0.00 | C013 | Iris Rodrigues | Private | ativo | 2023-01-22 00:00:00 | Fundo DI | Renda Fixa | 0.74 | 1200000.00 | Assessor |
| M0004 | 2025-03-03 00:00:00 | 2025-03 | resgate | 38411.32 | 0.00 | 38411.32 | C030 | Elena Silva | Varejo | ativo | 2023-09-18 00:00:00 | Fundo DI | Renda Fixa | 0.74 | 1200000.00 | Assessor |
| M0005 | 2025-02-12 00:00:00 | 2025-02 | captacao | 62445.56 | 62445.56 | 0.00 | C038 | Elena Souza | Varejo | inativo | 2023-08-08 00:00:00 | Tesouro Selic | Renda Fixa | 1.67 | 500000.00 | App |

### mix_produto
| produto | captacao | resgate | captacao_liquida | qtd |
| --- | --- | --- | --- | --- |
| Acoes Brasil | 959467.17 | 778098.27 | 181368.90 | 37 |
| Tesouro Selic | 750497.16 | 903710.63 | -153213.47 | 39 |
| Fundo DI | 604183.88 | 696989.04 | -92805.16 | 34 |
| Renda Fixa Credito | 573579.52 | 687456.08 | -113876.56 | 36 |
| Fundo Multimercado | 390185.02 | 785049.19 | -394864.17 | 34 |

### mix_canal
| canal | captacao | resgate | captacao_liquida | qtd |
| --- | --- | --- | --- | --- |
| Assessor | 1376523.08 | 1426863.44 | -50340.36 | 75 |
| App | 1184723.20 | 1719182.43 | -534459.23 | 69 |
| Parceiro | 716666.47 | 705257.34 | 11409.13 | 36 |

### receita_mensal
| ano_mes | valor_receita |
| --- | --- |
| 2025-01 | 331451.06 |
| 2025-02 | 272993.45 |
| 2025-03 | 289627.66 |
| 2025-04 | 345647.88 |
| 2025-05 | 259599.30 |
| 2025-06 | 346073.90 |
| 2025-07 | 253973.84 |

### status_snapshot
| status | qtd | pct |
| --- | --- | --- |
| ativo | 18 | 45.0 |
| inativo | 22 | 55.0 |

Inativos no snapshot: 22 de 40. Isso **nao** e taxa mensal de churn (meta `churn_clientes_pct` do Silver metas). Sem evidencia para churn mensal.

## Testes de integridade
- PASS: `fato_nao_vazio` (180 linhas)
- PASS: `base_analise_alinhada_ao_fato` (base=180 fato=180)
- PASS: `sem_pii` (cols=[])
- PASS: `fk_cliente` (orfaos=0)
- PASS: `fk_produto` (orfaos=0)
- PASS: `fk_canal` (orfaos=0)
- PASS: `kpi_captacao_bate_fato` (3277912.75 vs 3277912.75)
- PASS: `kpi_resgate_bate_fato` (3851303.21 vs 3851303.21)
- PASS: `valor_split_captacao_resgate` (valor = captacao + resgate)
- PASS: `base_sem_join_nulo` (nulos=0)
- PASS: `receita_mensal_nao_vazia` (7 meses)
- PASS: `status_snapshot_nao_vazio` ([{'status': 'ativo', 'qtd': 18, 'pct': 45.0}, {'status': 'inativo', 'qtd': 22, 'pct': 55.0}])

## O que nao deu para calcular
- Churn mensal: falta data de inativacao / evento de saida.
- Receita nao se junta ao fato por `id_mov` (nao ha chave comum de transacao).
- Metas nao sao dimensao da estrela; comparacao realizado vs meta fica para a EDA.

## ONDE SALVAR
- `data/gold/dim_cliente.csv`
- `data/gold/dim_produto.csv`
- `data/gold/dim_canal.csv`
- `data/gold/fato_movimentacoes.csv`
- `data/gold/base_analise.csv`
- `data/gold/kpis_mensais.csv`
- `data/gold/mix_produto.csv`
- `data/gold/mix_canal.csv`
- `data/gold/receita_mensal.csv`
- `data/gold/status_snapshot.csv`
- `outputs/elt_relatorio.md`

Status: **OK**
