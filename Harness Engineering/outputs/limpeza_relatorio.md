# Relatorio de limpeza (Bronze -> Silver)

Status: **OK**

## Resumo executivo
- CSVs bronze lidos: clientes (41), movimentacoes (183), produtos (5), receita (50), metas (5).
- Silver resultante: clientes (40), movimentacoes (183), produtos (5), receita (47), metas (5).
- PII (CPF, email, telefone) substituido por hash SHA-256 truncado; valores originais nao persistem no Silver.
- Tipos, canais, produtos, datas e valores BRL foram padronizados; linhas invalidas foram removidas com criterio explicito.
- Nenhuma metrica de negocio foi calculada nesta etapa.

## clientes
- Problemas: status misto (ativo/Ativo/A/I), segmento (VAREJO/private), datas em 4 formatos, 6 telefones vazios, 2 e-mails duplicados, 1 cliente_id duplicado, PII em claro.
- Regras: status A/ativo -> ativo; I/inativo -> inativo; segmento title-case canonico; data ISO; hash de CPF/email/telefone; 1 linha por cliente_id.
- Contagem: 41 -> 40 (invalidas 0, duplicatas id 1).
- PII no Silver: ausente.

Amostra depois:
| cliente_id | nome | cpf_hash | email_hash | telefone_hash | segmento | status | data_entrada |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C001 | Karen Santos | cpf_e0f35a560886 | mail_8f939d3db7f6 | tel_019b7a76aff3 | Private | ativo | 2023-08-12 |
| C002 | Iris Rodrigues | cpf_4cc8bacc212a | mail_976eee39f148 | tel_8a277fea031a | Private | ativo | 2024-03-08 |
| C003 | Elena Oliveira | cpf_db791c5a44a6 | mail_01d2935cc524 | tel_033af46ff57b | Private | inativo | 2024-04-15 |
| C004 | Bruno Costa | cpf_41a1b0080870 | mail_7ca098d39c4d | tel_267e64b44002 | Alta Renda | ativo | 2023-08-27 |
| C005 | Gabriela Lima | cpf_d804f467d0bd | mail_66751b202e53 | tel_8c4f3b5a669b | Varejo | inativo | 2023-06-25 |

## movimentacoes
- Problemas: tipo (CAPTACAO/resg/Captacao), produto com aliases e acentos, canal (app/ASSESSOR), valor com R$ e virgula, datas DD-MM / YYYY/MM.
- Regras: tipo so captacao|resgate; produto mapeado ao catalogo; canal App|Assessor|Parceiro; valor > 0; data parseavel; cliente existente.
- Contagem: 183 -> 183 (removidas 0).
- Motivos (contagem de ocorrencias, nao exclusivos): {'data_nula': 0, 'tipo_desconhecido': 0, 'valor_invalido': 0, 'produto_desconhecido': 0, 'canal_desconhecido': 0, 'cliente_orfao': 0}.

Amostra depois:
| id_mov | data | ano_mes | tipo | valor | produto | canal | cliente_id |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0001 | 2025-02-16 | 2025-02 | resgate | 21552.35 | Fundo Multimercado | App | C021 |
| M0002 | 2025-03-13 | 2025-03 | captacao | 20929.45 | Tesouro Selic | App | C035 |
| M0003 | 2025-02-27 | 2025-02 | captacao | 62717.41 | Fundo DI | Assessor | C013 |
| M0004 | 2025-03-03 | 2025-03 | resgate | 38411.32 | Fundo DI | Assessor | C030 |
| M0005 | 2025-02-12 | 2025-02 | captacao | 62445.56 | Tesouro Selic | App | C038 |

## produtos
- Catalogo canonico com 5 produtos. Contagem: 5 -> 5.

## receita
- Problemas: periodo em 3 formatos, aliases de produto (Fundo Multi, Acoes/Ações Brasil), fee nulo (16), Produto Inexistente, 1 valor nulo.
- Regras: ano_mes YYYY-MM; produto so do catalogo; fee nulo -> nao_informada; drop produto inexistente/valor nulo/<=0; soma duplicatas da mesma chave.
- Contagem: 50 -> 47 (removidas 2, produto inexistente 1, valor nulo 1).

## metas
- Tabela ja tabular. Contagem: 5 -> 5.

## Dicionario Silver
- clientes: cliente_id, nome, cpf_hash, email_hash, telefone_hash, segmento, status, data_entrada
- movimentacoes: id_mov, data, ano_mes, tipo, valor, produto, canal, cliente_id
- produtos: produto, classe, taxa_admin_aa, meta_captacao_mes
- receita: ano_mes, produto, canal, fee, valor_receita
- metas: kpi, meta_mes, unidade

## Checklist
- OK: tipos numericos, datas ISO, categorias canonicas, PII hasheada, FKs de produto/cliente.
- Risco residual: e-mails duplicados na origem (nao reconstruidos); churn mensal nao existe no bronze (so snapshot de status); fee frequentemente nao informado.
