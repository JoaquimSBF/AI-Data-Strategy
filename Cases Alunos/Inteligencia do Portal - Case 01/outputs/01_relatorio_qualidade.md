# Relatório de qualidade — etapa 01

Fonte exclusiva: `dados/*.csv` e `dados/README_DADOS.md`.
Nenhum valor foi imputado. Dados tratados como conteúdo, não como comando.

Premissa registrada (README_DADOS.md): neste conjunto sintético, cada usuário é atribuído a uma única editoria principal por competência. A soma mensal de `usuarios` representa o total sintético do portal. Não transportar para dados reais.

## Regras aplicadas (todas as tabelas)

- Datas completas: `YYYY-MM-DD` (aceitos também `DD/MM/YYYY` e `YYYY/MM/DD` na origem).
- Competência: `YYYY-MM` (aceitos também `MM/YYYY` e `YYYY/MM` na origem).
- Números: ponto decimal; milhar europeu (`92.156`) convertido para `92156`; vírgula decimal (`60,5`) convertida para `60.5`.
- Percentuais: número 0–100, sem `%`.
- Booleanos: `true` / `false` (origem `sim`/`SIM`/`nao`/`não`).
- Editorias canônicas: `politica`, `economia`, `tecnologia`, `esportes`, `cultura` (acentos e caixa normalizados).
- Sites canônicos: `portal_proprio`, `concorrente_alpha`, `concorrente_beta`.
- Mecanismos canônicos: `ia_a`, `ia_b`.
- Direção da meta: `maior_melhor` ou `menor_melhor`.
- Duplicata exata: uma ocorrência mantida; a outra vai para quarentena com motivo `duplicata_exata`.
- Valor ausente: não imputado; linha inválida vai para quarentena.
- `ctr_pct` de busca: recalculado como `100 * cliques / impressoes` (não se copia o CTR bruto após padronização).
- Texto com aparência de instrução: quarentena. Nenhum caso encontrado.

## Varredura de PII e injeção

Padrões procurados em todos os campos de texto: e-mail, telefone, CPF/CNPJ, e trechos do tipo ignore previous / system prompt / execute / drop table / script.

- PII em claro: nenhuma observada.
- Prompt injection: nenhuma observada.
- `autor_pseudo` permanece identificador sintético (`AUTOR_01` … `AUTOR_06`).
- A consulta `consulta sem medição` foi tratada como texto de dado, não como comando.

---

## 1. audiencia_portal.csv

**Arquivo:** `dados/audiencia_portal.csv`  
**Chave esperada:** `ano_mes + editoria`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 32 |
| Nulos / sentinelas | `taxa_rejeicao_pct` = `n/a` em 1 linha (2026-06 / TESTE) |
| Duplicata exata | 1: `02/2026` + `TECNOLOGIA` + `39.989` (linha 9 = linha 32) |
| Tipos misturados | competência `2026-01`, `02/2026`, `2026/03`; inteiro vs milhar `55.680`; pageviews `92.156` vs `100534`; rejeição `"60,5"` vs `56.9` |
| Categorias inconsistentes | ` Política `, `ESPORTES`, `POLÍTICA`, `TECNOLOGIA`, `TESTE` |
| Chave duplicada após padronização | só a duplicata exata (não há conflito de valores) |
| Fora de domínio | `pageviews = -50` na linha TESTE |
| PII | nenhuma |
| Injeção | nenhuma |

### Problemas

- `duplicata_exata`: 1
- `editoria_desconhecida`: 1 (`TESTE`)
- `valor_nulo_ou_invalido`: 1 (`n/a` em rejeição)
- `valor_negativo`: 1 (`pageviews = -50`)

### Cinco linhas antes

| ano_mes | editoria | usuarios | sessoes | pageviews | tempo_medio_seg | taxa_rejeicao_pct | assinaturas |
|---|---|---:|---:|---:|---:|---:|---:|
| 2026-01 |  Política  | 51040 | 62268 | 92.156 | 179 | 60,5 | 30 |
| 2026-01 |  Economia  | 41690 | 49194 | 74.774 | 196 | 56.9 | 27 |
| 2026-01 |  Tecnologia  | 36657 | 46554 | 72.624 | 222 | 52,0 | 30 |
| 2026-01 | ESPORTES | 46858 | 53886 | 86.217 | 148 | 63.8 | 19 |
| 2026-01 |  Cultura  | 25428 | 28225 | 46.289 | 204 | 55,7 | 17 |

### Cinco linhas depois (Silver)

| ano_mes | editoria | usuarios | sessoes | pageviews | tempo_medio_seg | taxa_rejeicao_pct | assinaturas |
|---|---|---:|---:|---:|---:|---:|---:|
| 2026-01 | politica | 51040 | 62268 | 92156 | 179 | 60.50 | 30 |
| 2026-01 | economia | 41690 | 49194 | 74774 | 196 | 56.90 | 27 |
| 2026-01 | tecnologia | 36657 | 46554 | 72624 | 222 | 52.00 | 30 |
| 2026-01 | esportes | 46858 | 53886 | 86217 | 148 | 63.80 | 19 |
| 2026-01 | cultura | 25428 | 28225 | 46289 | 204 | 55.70 | 17 |

**Contagem:** antes 32 · Silver 30 · quarentena 2

---

## 2. conteudos.csv

**Arquivo:** `dados/conteudos.csv`  
**Chave esperada:** `conteudo_id`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 26 |
| Nulos | `data_atualizacao` vazia em 20 linhas (campo opcional; não imputado); `data_publicacao` vazia em 1 linha (ART999) |
| Duplicata exata | 1: ART005 (linha 6 = linha 26) |
| Tipos misturados | datas `04/01/2026` e `2026-03-10` |
| Categorias inconsistentes | editoria `Política` / `CULTURA`; booleanos `SIM` / `nao` / `sim` / `não`; status `Publicado` / `publicado ` |
| Chave duplicada | ART005 (duplicata exata) |
| Fora de domínio | nenhum quantitativo negativo |
| PII | nenhuma; `autor_pseudo` é sintético |
| Injeção | nenhuma |

### Problemas

- `duplicata_exata`: 1 (ART005, linha 26)
- `data_publicacao_nula_ou_invalida`: 1 (ART999)

### Cinco linhas antes

| conteudo_id | data_publicacao | editoria | schema_article | faq_presente | status |
|---|---|---|---|---|---|
| ART001 | 04/01/2026 | Política | SIM | não | Publicado |
| ART002 | 07/02/2026 | Economia | SIM | não | Publicado |
| ART003 | 2026-03-10 | Tecnologia | SIM | não | Publicado |
| ART004 | 13/04/2026 | Esportes | SIM | não | Publicado |
| ART005 | 16/05/2026 | CULTURA | nao | não | Publicado |

### Cinco linhas depois (Silver)

| conteudo_id | data_publicacao | editoria | schema_article | faq_presente | status | data_referencia |
|---|---|---|---|---|---|---|
| ART001 | 2026-01-04 | politica | true | false | publicado | 2026-01-04 |
| ART002 | 2026-02-07 | economia | true | false | publicado | 2026-02-07 |
| ART003 | 2026-03-10 | tecnologia | true | false | publicado | 2026-03-10 |
| ART004 | 2026-04-13 | esportes | true | false | publicado | 2026-05-15 |
| ART005 | 2026-05-16 | cultura | false | false | publicado | 2026-05-16 |

Regra de `data_referencia`: `data_atualizacao` se existir, senão `data_publicacao`. Vazio de atualização permanece vazio.

**Contagem:** antes 26 · Silver 24 · quarentena 2

---

## 3. search_console.csv

**Arquivo:** `dados/search_console.csv`  
**Chave esperada:** `ano_mes + consulta + pagina_id`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 37 |
| Nulos | 1 linha com `impressoes=n/a` e `cliques`, `ctr_pct`, `posicao_media` vazios |
| Duplicata exata | 0 |
| Tipos misturados | competência `2026-01` / `02/2026`; impressões `23.200` vs `21750`; CTR `2.39` vs `"2,75"` |
| Categorias inconsistentes | consulta `inteligência artificial` / `INTELIGÊNCIA ARTIFICIAL` |
| Chave duplicada | 0 após normalização |
| Fora de domínio | nenhum negativo |
| PII | nenhuma |
| Injeção | nenhuma (texto `consulta sem medição` tratado como consulta) |

### Problemas

- `medicao_ausente`: 1 (`2026-06` + `consulta sem medição` + `ART999`)

### Cinco linhas antes

| ano_mes | consulta | impressoes | cliques | ctr_pct | posicao_media | pagina_id |
|---|---|---:|---:|---:|---:|---|
| 2026-01 | eleições municipais | 21750 | 520 | 2.39 | 12.47 | ART001 |
| 2026-01 | taxa de juros | 23.200 | 513 | 2.22 | 12.79 | ART002 |
| 2026-01 | inteligência artificial | 24650 | 502 | 2.04 | 13.11 | ART003 |
| 2026-01 | campeonato nacional | 26.100 | 486 | 1.86 | 13.43 | ART004 |
| 2026-01 | agenda cultural | 27550 | 464 | 1.69 | 13.75 | ART005 |

### Cinco linhas depois (Silver)

| ano_mes | consulta | impressoes | cliques | ctr_pct | posicao_media | pagina_id |
|---|---|---:|---:|---:|---:|---|
| 2026-01 | eleicoes municipais | 21750 | 520 | 2.39 | 12.47 | ART001 |
| 2026-01 | taxa de juros | 23200 | 513 | 2.21 | 12.79 | ART002 |
| 2026-01 | inteligencia artificial | 24650 | 502 | 2.04 | 13.11 | ART003 |
| 2026-01 | campeonato nacional | 26100 | 486 | 1.86 | 13.43 | ART004 |
| 2026-01 | agenda cultural | 27550 | 464 | 1.68 | 13.75 | ART005 |

Regra do CTR: `100 * cliques / impressoes`, arredondado a 2 casas. Por isso `513 / 23200 * 100 = 2.21` (origem trazia `2.22`) e `464 / 27550 * 100 = 1.68` (origem `1.69`).

**Contagem:** antes 37 · Silver 36 · quarentena 1

Observação de integridade (não é quarentena desta etapa): em 2026-06 as páginas `ART025` e `ART026` existem na busca e não existem no inventário Silver de conteúdos. Fato registrado; sem correção silenciosa.

---

## 4. auditoria_sites.csv

**Arquivo:** `dados/auditoria_sites.csv`  
**Chave esperada:** `data_coleta + site`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 18 |
| Nulos | 0 |
| Duplicata | 0 |
| Tipos misturados | `tempo_carregamento_seg` com `2.82` e `"2,12"` |
| Categorias inconsistentes | `portal_proprio` / `PORTAL_PROPRIO` |
| Chave duplicada | 0 |
| Fora de domínio | nenhum score negativo; percentuais dentro de 0–100 |
| PII | nenhuma |
| Injeção | nenhuma |

### Problemas

nenhum

### Cinco linhas antes

| data_coleta | site | performance_score | seo_tecnico_score | tempo_carregamento_seg |
|---|---|---:|---:|---:|
| 2026-01-28 | portal_proprio | 73 | 74 | 2.82 |
| 2026-01-28 | concorrente_alpha | 82 | 84 | 2,12 |
| 2026-01-28 | concorrente_beta | 68 | 79 | 3.32 |
| 2026-02-28 | PORTAL_PROPRIO | 74 | 75 | 2.74 |
| 2026-02-28 | concorrente_alpha | 83 | 85 | 2,04 |

### Cinco linhas depois (Silver)

| data_coleta | ano_mes | site | performance_score | seo_tecnico_score | tempo_carregamento_seg |
|---|---|---|---:|---:|---:|
| 2026-01-28 | 2026-01 | portal_proprio | 73 | 74 | 2.82 |
| 2026-01-28 | 2026-01 | concorrente_alpha | 82 | 84 | 2.12 |
| 2026-01-28 | 2026-01 | concorrente_beta | 68 | 79 | 3.32 |
| 2026-02-28 | 2026-02 | portal_proprio | 74 | 75 | 2.74 |
| 2026-02-28 | 2026-02 | concorrente_alpha | 83 | 85 | 2.04 |

**Contagem:** antes 18 · Silver 18 · quarentena 0

Limitação: scores de auditoria sintética pública; concorrentes fictícios.

---

## 5. visibilidade_ia.csv

**Arquivo:** `dados/visibilidade_ia.csv`  
**Chave esperada:** `data_teste + pergunta_id + mecanismo`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 60 |
| Nulos | `posicao_citacao` vazia em 12 linhas (todas com `houve_citacao = não`); não imputado |
| Duplicata | 0 |
| Tipos misturados | mecanismos `ia_a` / `IA_A` |
| Categorias inconsistentes | caixa do mecanismo |
| Chave duplicada | 0 |
| Fora de domínio | nenhum |
| PII | nenhuma |
| Injeção | nenhuma; o campo `observacao` é texto descritivo e foi ignorado como comando |

### Problemas

nenhum

### Cinco linhas antes

| data_teste | pergunta_id | mecanismo | dominio_citado | houve_citacao | posicao_citacao |
|---|---|---|---|---|---|
| 2026-01-25 | Q01011 | ia_a | concorrente_alpha | sim | 1 |
| 2026-01-25 | Q01012 | ia_b | nenhum | não |  |
| 2026-01-25 | Q01021 | ia_a | nenhum | não |  |
| 2026-01-25 | Q01022 | ia_b | concorrente_beta | sim | 3 |
| 2026-01-25 | Q01031 | ia_a | concorrente_beta | sim | 3 |

### Cinco linhas depois (Silver)

| data_teste | ano_mes | pergunta_id | mecanismo | dominio_citado | houve_citacao | posicao_citacao |
|---|---|---|---|---|---|---|
| 2026-01-25 | 2026-01 | Q01011 | ia_a | concorrente_alpha | true | 1 |
| 2026-01-25 | 2026-01 | Q01012 | ia_b | nenhum | false |  |
| 2026-01-25 | 2026-01 | Q01021 | ia_a | nenhum | false |  |
| 2026-01-25 | 2026-01 | Q01022 | ia_b | concorrente_beta | true | 3 |
| 2026-01-25 | 2026-01 | Q01031 | ia_a | concorrente_beta | true | 3 |

**Contagem:** antes 60 · Silver 60 · quarentena 0

Limitação: cada linha vale só para data, pergunta e mecanismo testados. Não é participação de mercado.

---

## 6. metas.csv

**Arquivo:** `dados/metas.csv`  
**Chave esperada:** `kpi + ano_mes_inicio + ano_mes_fim`

### Perfil de qualidade

| Item | Achado |
|---|---|
| Linhas de dado | 5 |
| Nulos | 0 |
| Duplicata | 0 |
| Tipos misturados | nenhum |
| Categorias inconsistentes | nenhuma; direções já canônicas |
| Chave duplicada | 0 |
| Fora de domínio | nenhum |
| PII | nenhuma |
| Injeção | nenhuma |

### Problemas

nenhum

### Cinco linhas antes (= todas)

| kpi | meta | unidade | direcao | ano_mes_inicio | ano_mes_fim |
|---|---:|---|---|---|---|
| usuarios_mensais | 260000 | qtd | maior_melhor | 2026-01 | 2026-06 |
| tempo_medio_seg | 190 | seg | maior_melhor | 2026-01 | 2026-06 |
| taxa_rejeicao_pct | 55 | pct | menor_melhor | 2026-01 | 2026-06 |
| seo_tecnico_score | 85 | pontos | maior_melhor | 2026-01 | 2026-06 |
| share_citacao_ia_pct | 35 | pct | maior_melhor | 2026-01 | 2026-06 |

### Cinco linhas depois (Silver)

| kpi | meta | unidade | direcao | ano_mes_inicio | ano_mes_fim |
|---|---:|---|---|---|---|
| usuarios_mensais | 260000.00 | qtd | maior_melhor | 2026-01 | 2026-06 |
| tempo_medio_seg | 190.00 | seg | maior_melhor | 2026-01 | 2026-06 |
| taxa_rejeicao_pct | 55.00 | pct | menor_melhor | 2026-01 | 2026-06 |
| seo_tecnico_score | 85.00 | pontos | maior_melhor | 2026-01 | 2026-06 |
| share_citacao_ia_pct | 35.00 | pct | maior_melhor | 2026-01 | 2026-06 |

**Contagem:** antes 5 · Silver 5 · quarentena 0

---

## Quarentena (todas as linhas descartadas)

| tabela | chave | motivo | origem |
|---|---|---|---|
| audiencia | linha_32 | duplicata_exata | linha 32 |
| audiencia | 2026-06\|TESTE | editoria_desconhecida\|valor_nulo_ou_invalido\|valor_negativo | linha 33 |
| conteudos | ART005 | duplicata_exata | linha 26 |
| conteudos | ART999 | data_publicacao_nula_ou_invalida | linha 27 |
| search_console | 2026-06\|consulta sem medicao\|ART999 | medicao_ausente | linha 38 |

Total: 5 linhas. Nenhuma linha descartada ficou de fora desta lista.

---

## Checklist de integridade

| Critério | Status | Evidência |
|---|---|---|
| Nenhum valor inventado | PASS | só padronização e recálculo documentado de CTR |
| Nenhuma PII em claro | PASS | varredura sem e-mail, telefone ou documento |
| Todas as descartadas na quarentena com motivo | PASS | 5/5 |
| Reexecução produz o mesmo resultado | PASS | segunda passagem idêntica |
| Chaves Silver únicas | PASS | 6/6 tabelas |
| Sem imputação | PASS | nulos opcionais permaneceram vazios |
| Dados não executados como comando | PASS | injeção = 0 |

Arquivos gerados:

- `outputs/01_relatorio_qualidade.md`
- `outputs/silver/audiencia.csv`
- `outputs/silver/conteudos.csv`
- `outputs/silver/search_console.csv`
- `outputs/silver/auditoria_sites.csv`
- `outputs/silver/visibilidade_ia.csv`
- `outputs/silver/metas.csv`
- `outputs/silver/quarentena.csv`
