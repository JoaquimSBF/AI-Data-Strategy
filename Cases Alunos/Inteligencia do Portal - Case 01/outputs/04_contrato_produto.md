# Contrato do produto — Inteligência do Portal

Público: liderança editorial, audiência, SEO, produto digital e dados.
Período de demonstração: 2026-01 a 2026-06.
Conector: arquivos locais (CSV/JSON) e `sample-data.js`. Sem dado ao vivo.

## Jornada

```text
Importar ou usar demonstração
→ validar
→ filtrar período
→ observar KPIs e evidências
→ revisar backlog
→ atribuir papel, status, prazo e nota
→ exportar acompanhamento
```

## Telas

1. Visão executiva — KPIs, metas, variações e limitações.
2. Audiência — mix por editoria e tabela mensal.
3. Busca — impressões, cliques, CTR e posição ponderados.
4. Benchmark — scores separados, mesma data, concorrentes fictícios.
5. Visibilidade em IA — 10 testes/mês, aviso de amostra.
6. Oportunidades — lista/kanban persistente.
7. Dados — importar, restaurar, apagar, exportar.

## Regras de cálculo

- Usuários mensais = soma(usuarios), premissa de atribuição exclusiva.
- Tempo e rejeição ponderados por sessões.
- CTR = 100 * cliques / impressões.
- Posição ponderada por impressões.
- Share de IA = 100 * testes do domínio / 10.
- Sem score composto de SEO.
- Meta só entra se o mês estiver na vigência.

## Persistência

- `localStorage` chave `portal-intelligence-v1`.
- Guardar backlog, notas e status.
- Botão para apagar dados locais.
- Não enviar nada a servidor.

## Segurança

- `textContent` para dados importados.
- Sem `innerHTML` com dado externo.
- Sem `eval` / `Function` / CDN.
- Arquivo máximo 5 MB; só `.csv` e `.json`.
- PII: bloquear ou pseudonimizar.

## Fora de escopo

- Integração Analytics/Search Console ao vivo.
- Market share universal de IA.
- Causalidade entre schema e audiência.
- Login, nuvem ou multiempresa.

## Definição de pronto

A aplicação abre offline, mostra os números Gold, permite abrir evidência, persistir backlog e exportar JSON/CSV/Markdown.
