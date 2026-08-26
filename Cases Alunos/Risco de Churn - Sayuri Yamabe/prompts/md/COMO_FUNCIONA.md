# Como funciona o produto — Radar de risco (Sayuri Yamabe)

## O que e

Uma lista priorizada de clientes com **sinais** (inativo, ticket, downgrade, pedido de cancelamento). Nao e previsao estatistica e nao e modelo treinado.

HTML unico, abre no navegador. PII nao aparece (so IDs).

## Jornada

1. **00** — proibe % de churn inventado.
2. **01** — limpa `dados/` e **declara o buraco**: snapshot sem data de saida.
3. **02** — JSON com pontos e faixa (regra explicita, nao ML).
4. **03** — contrato da tela.
5. **04** — `produto/index.html`.
6. **05** — juiz (FAIL se aparecer probabilidade).

O que colar e onde salvar: `prompts/md/MAPA_ARQUIVOS.md`.

## Como o HTML trabalha

JSON embutido. Clique na linha = eventos. KPI de churn do periodo fica "sem evidencia".

## O que codigo faria melhor

Treinar/avaliar modelo (split no tempo, metrica). Fora deste curso.
