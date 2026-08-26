# Relatorio de limpeza (Bronze -> Silver)

Status: **OK**

Limpeza e padronizacao apenas. Nenhuma metrica de negocio foi calculada.
PII (CPF, e-mail, telefone) nao e reproduzida neste relatorio: no ANTES aparece como `[PII]`; no DEPOIS so ha hash.

## Resumo executivo
- Bronze lido: clientes 41, movimentacoes 183, produtos 5, receita 50, metas 5.
- Silver gravado: clientes 40, movimentacoes 180, produtos 5, receita 47, metas 5.
- Clientes: PII hasheada (SHA-256 truncado); 1 `cliente_id` duplicado removido (C003); 2 e-mail(s) duplicado(s) na origem (mantidos como clientes distintos); telefones vazios viraram hash vazio.
- Movimentacoes: datas/tipos/produtos/canais/valores padronizados; 0 linha(s) invalida(s) por regra; 3 ocorrencia(s) extra de `id_mov` removida(s) (M0011 e M0026).
- Receita: 2 linha(s) removida(s) (produto inexistente e/ou valor nulo/<=0); aliases agregados na chave ano_mes+produto+canal+fee.

## clientes
**Problemas:** PII em claro; status misto (`ativo`/`Ativo`/`A`/`I`/`inativo`); segmento misto (`VAREJO`/`private`); datas em ISO, `DD/MM/YYYY` e `YYYY/MM/DD`; 6 telefones vazios; o mesmo e-mail aparece em dois `cliente_id` distintos (valor original nao reproduzido); `C003` repetido na ultima linha (duplicata identica).
**Regras:** `A`/`ativo` → `ativo`; `I`/`inativo` → `inativo`; segmento → Private | Alta Renda | Varejo; `data_entrada` → `YYYY-MM-DD`; CPF/e-mail/telefone → `cpf_hash`/`email_hash`/`telefone_hash`; 1 linha por `cliente_id` (keep first); nao persistir colunas originais de PII.
**Contagem:** 41 → 40 (invalidas 0, duplicatas de id removidas 1).

ANTES (PII mascarada):
| cliente_id | nome | cpf | email | telefone | segmento | status | data_entrada |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C001 | Karen Santos | [PII] | [PII] | [PII] | Private | ativo | 2023-08-12 |
| C002 | Iris Rodrigues | [PII] | [PII] | [PII] | Private | Ativo | 08/03/2024 |
| C003 | Elena Oliveira | [PII] | [PII] | [PII] | Private | I | 2024/04/15 |
| C004 | Bruno Costa | [PII] | [PII] | [PII] | Alta Renda | ativo | 2023-08-27 |
| C005 | Gabriela Lima | [PII] | [PII] | [PII] | VAREJO | I | 2023/06/25 |

DEPOIS:
| cliente_id | nome | cpf_hash | email_hash | telefone_hash | segmento | status | data_entrada |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C001 | Karen Santos | cpf_e0f35a560886 | mail_8f939d3db7f6 | tel_019b7a76aff3 | Private | ativo | 2023-08-12 |
| C002 | Iris Rodrigues | cpf_4cc8bacc212a | mail_976eee39f148 | tel_8a277fea031a | Private | ativo | 2024-03-08 |
| C003 | Elena Oliveira | cpf_db791c5a44a6 | mail_01d2935cc524 | tel_033af46ff57b | Private | inativo | 2024-04-15 |
| C004 | Bruno Costa | cpf_41a1b0080870 | mail_7ca098d39c4d | tel_267e64b44002 | Alta Renda | ativo | 2023-08-27 |
| C005 | Gabriela Lima | cpf_d804f467d0bd | mail_66751b202e53 | tel_8c4f3b5a669b | Varejo | inativo | 2023-06-25 |

## movimentacoes
**Problemas:** `tipo` com `CAPTAÇÃO`/`Captacao`/`resg`; produto com alias (`FUNDO DI`, `Fundo_DI`, `AcoesBrasil`, `Fundo Multi`, espaco em `Tesouro Selic `); canal `app`/`ASSESSOR`; valor com `R$`, milhar `.` e decimal `,`; datas `YYYY-MM-DD`, `DD-MM-YYYY`, `DD/MM/YYYY`, `YYYY/MM/DD`; `id_mov` duplicado (M0011 x3, M0026 x2).
**Regras:** tipo so `captacao`|`resgate`; produto mapeado ao catalogo; canal App|Assessor|Parceiro; valor > 0 em float; data parseavel + `ano_mes`; `cliente_id` existente; drop `id_mov` duplicado (keep first).
**Criterio de exclusao:** data nula; tipo desconhecido; valor nulo ou <= 0; produto fora do catalogo; canal desconhecido; cliente orfao.
**Contagem:** 183 → 180 (invalidas 0, extras de id_mov 3). Motivos nas invalidas: {}.

ANTES:
| id_mov | data | tipo | valor | produto | canal | cliente_id |
| --- | --- | --- | --- | --- | --- | --- |
| M0001 | 2025-02-16 | resgate | 21552,35 | Multimercado | app | C021 |
| M0002 | 13-03-2025 | CAPTAÇÃO | 20929.45 | Tesouro Selic  | App | C035 |
| M0003 | 2025-02-27 | captacao | 62717.41 | FUNDO DI | Assessor | C013 |
| M0004 | 03/03/2025 | Resgate | 38411.32 | fundo di | Assessor | C030 |
| M0005 | 2025-02-12 | Captacao | R$ 62.445,56 | Tesouro Selic  | App | C038 |

DEPOIS:
| id_mov | data | ano_mes | tipo | valor | produto | canal | cliente_id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0001 | 2025-02-16 | 2025-02 | resgate | 21552.35 | Fundo Multimercado | App | C021 |
| M0002 | 2025-03-13 | 2025-03 | captacao | 20929.45 | Tesouro Selic | App | C035 |
| M0003 | 2025-02-27 | 2025-02 | captacao | 62717.41 | Fundo DI | Assessor | C013 |
| M0004 | 2025-03-03 | 2025-03 | resgate | 38411.32 | Fundo DI | Assessor | C030 |
| M0005 | 2025-02-12 | 2025-02 | captacao | 62445.56 | Tesouro Selic | App | C038 |

## produtos
**Problemas:** nenhum estrutural; catalogo ja canonico (5 produtos). Usado como referencia de FK.
**Regras:** trim; nomes alinhados ao dicionario de aliases das outras tabelas.
**Contagem:** 5 → 5.

ANTES:
| produto | classe | taxa_admin_aa | meta_captacao_mes |
| --- | --- | --- | --- |
| Fundo DI | Renda Fixa | 0.74 | 1200000 |
| Fundo Multimercado | Multimercado | 1.36 | 1200000 |
| Tesouro Selic | Renda Fixa | 1.67 | 500000 |
| Acoes Brasil | Renda Variavel | 1.65 | 500000 |
| Renda Fixa Credito | Renda Fixa | 0.33 | 1200000 |

DEPOIS:
| produto | classe | taxa_admin_aa | meta_captacao_mes |
| --- | --- | --- | --- |
| Fundo DI | Renda Fixa | 0.74 | 1200000.0 |
| Fundo Multimercado | Multimercado | 1.36 | 1200000.0 |
| Tesouro Selic | Renda Fixa | 1.67 | 500000.0 |
| Acoes Brasil | Renda Variavel | 1.65 | 500000.0 |
| Renda Fixa Credito | Renda Fixa | 0.33 | 1200000.0 |

## receita
**Problemas:** `periodo` em `2025/01`, `2025-01`, `01/2025`; produto `Fundo Multi` / `Ações Brasil`; `Produto Inexistente`; `fee` nulo (16) e caixa mista; 1 `valor_receita` vazio (2025-05 Fundo DI / Assessor); formatos BRL mistos.
**Regras:** periodo → `ano_mes` `YYYY-MM`; produto so do catalogo; canal canonico; fee nulo → `nao_informada`; drop produto inexistente e valor nulo/<=0; somar duplicatas da mesma chave apos o mapeamento.
**Contagem:** 50 → 47 (linhas invalidas 2; apos agregacao a chave Silver tem 47 linhas). Motivos: {'produto_inexistente;': 1, 'valor_invalido;': 1}.

ANTES:
| periodo | produto | canal | fee | valor_receita |
| --- | --- | --- | --- | --- |
| 2025/01 | Fundo DI | app | admin | 16216,23 |
| 2025-01 | Fundo Multimercado | Assessor |  | 63857.74 |
| 01/2025 | Tesouro Selic | Assessor | Admin | 61537,21 |
| 2025-01 | Acoes Brasil | App | corretagem | 34335.75 |
| 2025-01 | Renda Fixa Credito | Assessor |  | 51882.49 |

DEPOIS:
| ano_mes | produto | canal | fee | valor_receita |
| --- | --- | --- | --- | --- |
| 2025-01 | Acoes Brasil | App | admin | 23277.55 |
| 2025-01 | Acoes Brasil | App | corretagem | 34335.75 |
| 2025-01 | Fundo DI | App | admin | 16216.23 |
| 2025-01 | Fundo Multimercado | App | nao_informada | 80344.09 |
| 2025-01 | Fundo Multimercado | Assessor | nao_informada | 63857.74 |

## metas
**Problemas:** nenhum. Ja tabular.
**Regras:** trim de `kpi`/`unidade`; `meta_mes` numerico.
**Contagem:** 5 → 5.

ANTES/DEPOIS:
| kpi | meta_mes | unidade |
| --- | --- | --- |
| captacao | 2500000.0 | BRL |
| resgate | 1200000.0 | BRL |
| captacao_liquida | 1300000.0 | BRL |
| receita | 180000.0 | BRL |
| churn_clientes_pct | 3.0 | pct |

## Dicionario Silver
- **clientes:** cliente_id, nome, cpf_hash, email_hash, telefone_hash, segmento (Private|Alta Renda|Varejo), status (ativo|inativo), data_entrada (YYYY-MM-DD)
- **movimentacoes:** id_mov, data (YYYY-MM-DD), ano_mes (YYYY-MM), tipo (captacao|resgate), valor (float > 0), produto, canal (App|Assessor|Parceiro), cliente_id
- **produtos:** produto, classe, taxa_admin_aa, meta_captacao_mes
- **receita:** ano_mes, produto, canal, fee (admin|corretagem|nao_informada), valor_receita
- **metas:** kpi, meta_mes, unidade (BRL|pct)

## Checklist
**OK**
- Tipos, datas ISO, `ano_mes`, categorias canonicas.
- PII ausente em claro no Silver.
- FKs de produto e cliente nas movimentacoes Silver.
- CSVs gravados em `data/silver/`.

**Risco residual**
- E-mail duplicado na origem (dois cliente_id distintos); nao reconstruimos identidade.
- Telefone vazio permanece como hash vazio (nao e PII, mas e dado faltante).
- Nome de cliente permanece (nao e CPF/e-mail/telefone); se a turma quiser, pode hashear tambem.
- Fee `nao_informada` frequente na receita.
- Churn mensal nao existe neste bronze (so status pontual) — fora desta etapa.

## ONDE SALVAR
- `data/silver/clientes.csv`
- `data/silver/movimentacoes.csv`
- `data/silver/produtos.csv`
- `data/silver/receita.csv`
- `data/silver/metas.csv`
- `outputs/limpeza_relatorio.md` (este arquivo)
- `outputs/linhas_invalidas/` (rejeitos e duplicatas, PII mascarada em clientes)

Status: **OK** — padronizacao concluida, PII hasheada, invalidos documentados, sem metricas de negocio.
