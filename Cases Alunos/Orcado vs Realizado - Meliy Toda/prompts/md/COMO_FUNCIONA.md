# Como funciona o produto — Painel de desvio (Meliy Toda)

## O que e

Um **painel de FP&A**: orcado versus realizado por centro de custo, com alerta quando TI lanca gasto no centro de RH.

Nao e ERP. Nao trava compra. Nao recomenda demissao.

## Jornada

1. **00** — regras de FP&A.
2. **01** — cola `dados/`; marca alerta de CC divergente (nao descarta).
3. **02** — JSON de totais, por CC, por mes, alertas.
4. **03** — contrato da tela.
5. **04** — `produto/index.html`.
6. **05** — juiz.

O que colar e onde salvar: `prompts/md/MAPA_ARQUIVOS.md`.

## Como o HTML trabalha

JSON embutido, offline. KPIs, lista de alertas, barras CSS, tabela mensal.

## O que codigo faria melhor

Travar a compra no sistema (permissao de centro de custo). Isso e ERP, nao HTML.
