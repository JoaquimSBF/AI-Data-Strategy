# Analise final — Allura Finance

Periodo das movimentacoes: **2025-01 a 2025-07**.
Status: **OK**

Fontes usadas (Gold, salvo metas no Silver):
- `data/gold/kpis_mensais.csv`
- `data/gold/mix_produto.csv`
- `data/gold/mix_canal.csv`
- `data/gold/receita_mensal.csv`
- `data/gold/status_snapshot.csv`
- `data/gold/dim_produto.csv` (meta_captacao_mes por produto)
- `data/silver/metas.csv`

Regras: nenhum numero fora dessas tabelas. Onde o Gold nao permite o calculo, esta escrito **sem evidencia**.
Fato observado e interpretacao estao separados.

---

## 1) Como estao captacao, resgate e captacao liquida por mes?

Fonte: `data/gold/kpis_mensais.csv`  
Comparacao com meta mensal: `data/silver/metas.csv` (captacao 2.500.000 | resgate 1.200.000 | captacao_liquida 1.300.000, unidade BRL).

| ano_mes | captacao | resgate | captacao_liquida | clientes_movimentados | qtd_movimentos | vs meta captacao | vs meta liquida |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-01 | 240.709,83 | 519.723,03 | -279.013,20 | 19 | 21 | abaixo | abaixo |
| 2025-02 | 585.529,05 | 382.420,23 | 203.108,82 | 19 | 26 | abaixo | abaixo |
| 2025-03 | 504.054,92 | 794.471,73 | -290.416,81 | 23 | 32 | abaixo | abaixo |
| 2025-04 | 610.291,15 | 578.010,58 | 32.280,57 | 16 | 29 | abaixo | abaixo |
| 2025-05 | 561.334,88 | 546.083,50 | 15.251,38 | 20 | 29 | abaixo | abaixo |
| 2025-06 | 386.316,82 | 674.588,98 | -288.272,16 | 20 | 25 | abaixo | abaixo |
| 2025-07 | 389.676,10 | 356.005,16 | 33.670,94 | 14 | 18 | abaixo | abaixo |

Totais do periodo (soma de `kpis_mensais`):
- captacao: **3.277.912,75**
- resgate: **3.851.303,21**
- captacao liquida: **-573.390,46**

Medias mensais:
- captacao: **468.273,25** (meta 2.500.000,00)
- resgate: **550.186,17** (meta 1.200.000,00)
- captacao liquida: **-81.912,92** (meta 1.300.000,00)

**Fato observado**
- Liquida positiva em 2025-02, 2025-04, 2025-05 e 2025-07.
- Liquida negativa em 2025-01, 2025-03 e 2025-06.
- Melhor mes liquido: **2025-02** (203.108,82), com 19 clientes e 26 movimentos.
- Pior mes liquido: **2025-03** (-290.416,81), com o maior resgate do periodo (794.471,73) e 32 movimentos.
- Nenhum mes atinge a meta de captacao nem a de captacao liquida.
- Nenhum mes ultrapassa a meta cadastrada de resgate (1.200.000,00).

**Interpretacao**
O volume mensal de captacao esta em outra ordem de grandeza em relacao a meta (media ~468 mil vs 2,5 milhoes). A liquida do periodo e negativa porque o resgate acumulado supera a captacao, concentrado em tres meses de vazamento (jan, mar, jun).

---

## 2) Quais produtos puxam o resultado?

Fonte: `data/gold/mix_produto.csv` (acumulado do periodo, nao mensal).  
Meta por produto: `data/gold/dim_produto.csv` (`meta_captacao_mes` — meta **mensal**; o mix Gold e **do periodo**).

| produto | captacao | resgate | captacao_liquida | qtd | share captacao |
| --- | --- | --- | --- | --- | --- |
| Acoes Brasil | 959.467,17 | 778.098,27 | 181.368,90 | 37 | 29,3% |
| Tesouro Selic | 750.497,16 | 903.710,63 | -153.213,47 | 39 | 22,9% |
| Fundo DI | 604.183,88 | 696.989,04 | -92.805,16 | 34 | 18,4% |
| Renda Fixa Credito | 573.579,52 | 687.456,08 | -113.876,56 | 36 | 17,5% |
| Fundo Multimercado | 390.185,02 | 785.049,19 | -394.864,17 | 34 | 11,9% |

Media mensal aproximada (captacao do periodo / 7 meses) versus `meta_captacao_mes`:

| produto | media mensal (periodo/7) | meta_captacao_mes | gap |
| --- | --- | --- | --- |
| Acoes Brasil | 137.066,74 | 500.000,00 | -362.933,26 |
| Tesouro Selic | 107.213,88 | 500.000,00 | -392.786,12 |
| Fundo DI | 86.311,98 | 1.200.000,00 | -1.113.688,02 |
| Renda Fixa Credito | 81.939,93 | 1.200.000,00 | -1.118.060,07 |
| Fundo Multimercado | 55.740,72 | 1.200.000,00 | -1.144.259,28 |

Serie mensal por produto: **sem evidencia** em `mix_produto` (so existe acumulado). Quem precisar do recorte mes x produto deve usar `fato_movimentacoes` / `base_analise` numa etapa extra.

**Fato observado**
- Unico produto com liquida positiva no periodo: **Acoes Brasil** (181.368,90).
- Pior liquida: **Fundo Multimercado** (-394.864,17), apesar de menor captacao.
- Tesouro Selic tem a maior quantidade de movimentos (39) e liquida negativa.
- Todas as medias mensais de captacao por produto ficam abaixo da `meta_captacao_mes`.

**Interpretacao**
O resultado liquido e puxado por Acoes Brasil; o vazamento esta concentrado em Multimercado (e, em menor grau, Tesouro Selic e Renda Fixa Credito). Captacao de produto esta longe da meta mensal do catalogo — o gap e de metodo (periodo/7 vs meta mensal), mas a direcao e a mesma em todos os produtos.

---

## 3) Quais canais se destacam?

Fonte: `data/gold/mix_canal.csv` (acumulado do periodo).

| canal | captacao | resgate | captacao_liquida | qtd | share captacao |
| --- | --- | --- | --- | --- | --- |
| Assessor | 1.376.523,08 | 1.426.863,44 | -50.340,36 | 75 | 42,0% |
| App | 1.184.723,20 | 1.719.182,43 | -534.459,23 | 69 | 36,1% |
| Parceiro | 716.666,47 | 705.257,34 | 11.409,13 | 36 | 21,9% |

**Fato observado**
- Assessor concentra a maior captacao (42,0%) e o maior numero de movimentos (75), com liquida levemente negativa.
- App e o canal de maior vazamento liquido (-534.459,23): resgate supera captacao de forma clara.
- Parceiro e o **unico canal com liquida positiva** (11.409,13), com menor volume.

Serie mensal por canal: **sem evidencia** em `mix_canal`.

**Interpretacao**
Quem "puxa volume" e o Assessor; quem "fura a liquida" e o App. Parceiro contribui pouco em volume, mas nao destroi a liquida.

---

## 4) Como estao receita e churn/status? Ha alerta versus meta?

### Receita
Fonte: `data/gold/receita_mensal.csv`  
Meta: `data/silver/metas.csv` (`receita` = 180.000 BRL / mes).

| ano_mes | valor_receita | vs meta 180.000 |
| --- | --- | --- |
| 2025-01 | 331.451,06 | acima |
| 2025-02 | 272.993,45 | acima |
| 2025-03 | 289.627,66 | acima |
| 2025-04 | 345.647,88 | acima |
| 2025-05 | 259.599,30 | acima |
| 2025-06 | 346.073,90 | acima |
| 2025-07 | 253.973,84 | acima |

- Receita total do periodo: **2.099.367,09**
- Media mensal: **299.909,58**
- Meses abaixo da meta: **nenhum**

Receita nao se cruza com `fato_movimentacoes` por `id_mov`: **sem evidencia** de conciliar fee com AUM/movimento.

**Fato observado:** receita mensal ficou acima da meta em todos os 7 meses.  
**Interpretacao:** no recorte de receita nao ha alerta de queda abaixo da meta; o alerta esta em captacao/liquida, nao em fee do periodo.

### Churn / status
Fonte: `data/gold/status_snapshot.csv`  
Meta: `data/silver/metas.csv` (`churn_clientes_pct` = 3,0% **ao mes**).

| status | qtd | pct |
| --- | --- | --- |
| ativo | 18 | 45,0 |
| inativo | 22 | 55,0 |

**Fato observado:** 22 de 40 clientes estao inativos no snapshot (55%).

Taxa mensal de churn versus meta de 3%: **sem evidencia**.  
Nao ha data de inativacao nem painel longitudinal no Gold. O snapshot de 55% **nao e comparavel** a uma meta mensal de 3%.

**Alerta:** nao emitir alerta de "churn 55% vs meta 3%" — sao metricas diferentes. O alerta correto e **buraco de dado** para churn mensal.

---

## 3 insights acionaveis

1. Abrir **2025-03** (pior liquida, -290.416,81) e **2025-06** (-288.272,16) em produto/canal via `base_analise` — o Gold mensal ja aponta o mes; o mix so existe acumulado.
2. Tratar **App** como prioridade de retencao: e o canal que mais destroi liquida (-534.459,23) com 36,1% da captacao.
3. Preservar e entender **Acoes Brasil** e **Parceiro**: unicos recortes (produto e canal) com liquida positiva no periodo. Fundo Multimercado e o maior dreno (-394.864,17).

## 2 riscos / limites dos dados

1. Mix de produto/canal e acumulado do periodo; metas de captacao de produto e churn sao mensais. Comparar snapshot de status (55% inativos) com `churn_clientes_pct` seria erro.
2. Receita e movimentacao nao compartilham chave de transacao; fee muitas vezes vinha `nao_informada` no Silver. Dados sao sinteticos/didaticos.

---

## 3 graficos sugeridos

1. **Titulo:** Captacao, resgate e captacao liquida por mes (com metas).  
   **Eixos:** X = `ano_mes`; Y = BRL.  
   **O que mostra:** tendencia mensal, meses negativos e a distancia ate as metas de captacao (2,5 mi) e liquida (1,3 mi). Fonte: `kpis_mensais` + `metas`.

2. **Titulo:** Captacao liquida por produto.  
   **Eixos:** X = produto; Y = BRL (liquida).  
   **O que mostra:** Acoes Brasil positivo versus Multimercado como maior vazamento. Fonte: `mix_produto`.

3. **Titulo:** Receita mensal versus meta.  
   **Eixos:** X = `ano_mes`; Y = BRL.  
   **O que mostra:** todos os meses acima de 180.000, contrastando com o alerta de captacao. Fonte: `receita_mensal` + `metas`.

Nao sugerir grafico de "churn mensal vs meta": **sem evidencia**.

---

## Checklist de evidencia

- [x] Quatro perguntas respondidas com numero e fonte
- [x] Fato separado de interpretacao
- [x] Churn mensal declarado como sem evidencia
- [x] Sem PII

Pronto para a etapa RAG / Board Pack, usando este arquivo como contexto.

Status: **OK**
