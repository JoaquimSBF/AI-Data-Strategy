# Como funciona o produto — Landing de Dados (Eduardo Campregher)

## O que e

Uma **landing page** (site de produto) com KPIs, mix e troca PT/EN/ES. Um unico HTML. Dois cliques no navegador.

Nao e Power BI, nao e dashboard interno, nao e board pack.

## Jornada

1. **00** — regras (nao inventar numero, nao vender dado ao vivo).
2. **01** — cola CSVs de `dados/`; sai CSVs limpos em `outputs/`.
3. **02** — JSON da landing (serie, mix, i18n so com o que existe).
4. **03** — contrato das telas.
5. **04** — `produto/index.html`.
6. **05** — juiz.

O que colar e onde salvar: `prompts/md/MAPA_ARQUIVOS.md`.

## Como o HTML trabalha

JSON da etapa 02 vai **dentro** do arquivo (offline). Seletor de idioma. Barra CSS, sem biblioteca. Traducao vazia vira "sem traducao", nao texto inventado.

## O que codigo faria melhor

Pagina ligada a Power BI, Oracle ou MCP. Isso exige instalar conector — fora deste curso.
