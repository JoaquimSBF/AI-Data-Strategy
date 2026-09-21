# Relatorio ELT / Gold

Status: **OK**

## Diagrama da estrela
```
dim_cliente (cliente_id) ──┐
dim_produto (produto) ─────┼── fato_movimentacoes ── base_analise
dim_canal (canal) ─────────┘
                              ├── kpis_mensais
                              ├── mix_produto
                              └── mix_canal
receita_mensal (ano_mes) independente, a partir de Silver receita
status_snapshot a partir de dim_cliente.status
```

## Passos pandas (equivalente DuckDB)
1. dim_cliente = clientes sem hashes PII.
2. dim_produto = catalogo Silver.
3. dim_canal = distinct canal do fato.
4. fato_movimentacoes = Silver movimentacoes + valor_captacao/valor_resgate.
5. base_analise = fato LEFT JOIN dims.
6. kpis_mensais = soma captacao/resgate por ano_mes + clientes distintos + qtd movimentos.
7. mix_produto / mix_canal = soma por dimensao.
8. receita_mensal = soma valor_receita por ano_mes.

## Exemplos

kpis_mensais (todas as linhas):
| ano_mes | captacao | resgate | clientes_movimentados | qtd_movimentos | captacao_liquida |
| --- | --- | --- | --- | --- | --- |
| 2025-01 | 240,709.83 | 519,723.03 | 19 | 21 | -279,013.20 |
| 2025-02 | 585,529.05 | 382,420.23 | 19 | 26 | 203,108.82 |
| 2025-03 | 548,662.31 | 794,471.73 | 23 | 32 | -245,809.42 |
| 2025-04 | 610,291.15 | 698,585.84 | 16 | 29 | -88,294.69 |
| 2025-05 | 561,334.88 | 546,083.50 | 20 | 29 | 15,251.38 |
| 2025-06 | 386,316.82 | 674,588.98 | 20 | 25 | -288,272.16 |
| 2025-07 | 389,676.10 | 356,005.16 | 14 | 18 | 33,670.94 |

base_analise (5 linhas):
| id_mov | data | ano_mes | tipo | valor | produto | canal | cliente_id | valor_captacao | valor_resgate | nome | segmento | status | data_entrada | classe | taxa_admin_aa | meta_captacao_mes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M0001 | 2025-02-16 | 2025-02 | resgate | 21,552.35 | Fundo Multimercado | App | C021 | 0.00 | 21,552.35 | Elena Costa | Varejo | ativo | 2024-06-02 | Multimercado | 1.36 | 1,200,000.00 |
| M0002 | 2025-03-13 | 2025-03 | captacao | 20,929.45 | Tesouro Selic | App | C035 | 20,929.45 | 0.00 | Nicolas Santos | Private | ativo | 2024-03-11 | Renda Fixa | 1.67 | 500,000.00 |
| M0003 | 2025-02-27 | 2025-02 | captacao | 62,717.41 | Fundo DI | Assessor | C013 | 62,717.41 | 0.00 | Iris Rodrigues | Private | ativo | 2023-01-22 | Renda Fixa | 0.74 | 1,200,000.00 |
| M0004 | 2025-03-03 | 2025-03 | resgate | 38,411.32 | Fundo DI | Assessor | C030 | 0.00 | 38,411.32 | Elena Silva | Varejo | ativo | 2023-09-18 | Renda Fixa | 0.74 | 1,200,000.00 |
| M0005 | 2025-02-12 | 2025-02 | captacao | 62,445.56 | Tesouro Selic | App | C038 | 62,445.56 | 0.00 | Elena Souza | Varejo | inativo | 2023-08-08 | Renda Fixa | 1.67 | 500,000.00 |

## Testes de integridade
- PASS: fato_nao_vazio (183 linhas)
- PASS: base_alinhada_fato (base=183 fato=183)
- PASS: sem_pii_claro (cols=[])
- PASS: fk_cliente (todas as FKs)
- PASS: fk_produto (todas as FKs)
- PASS: kpi_bate_fato_captacao (3322520.14 vs 3322520.14)
- PASS: kpi_bate_fato_resgate (3971878.47 vs 3971878.47)
- PASS: split_captacao_resgate (valor = cap+res)
- PASS: silver_mov_eq_fato (183 vs 183)
- PASS: dim_cliente_eq_silver (40)
- PASS: kpis_meses_preenchidos (['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'])
