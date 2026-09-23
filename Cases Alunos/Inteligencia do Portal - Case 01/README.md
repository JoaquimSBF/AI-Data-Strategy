# Inteligência do Portal — Caso 01

Case didático com dados 100% sintéticos para construir um produto de inteligência editorial.

## Desafio

Criar uma aplicação que:

- acompanhe audiência e engajamento do portal;
- compare sinais públicos do portal com concorrentes sintéticos;
- avalie busca tradicional e visibilidade em respostas de IA;
- transforme evidências em oportunidades acompanháveis;
- nunca apresente correlação como causa;
- preserve a rastreabilidade de cada número.

## Produto final

O resultado não é apenas um dashboard. A etapa 05 gera um **workspace local de inteligência editorial**:

- importação de CSV/JSON;
- KPIs e séries;
- comparação com metas;
- análise de produto próprio e concorrentes;
- backlog de oportunidades;
- responsáveis, status e notas;
- persistência no navegador;
- exportação de dados e relatório;
- painel de evidências e limitações.

Arquivos esperados:

```text
produto/
  index.html
  styles.css
  app.js
  sample-data.js
  README.md
```

O produto abre no navegador sem CDN e sem transmitir os dados.

## Como abrir no final

Não use `file://`. Suba o servidor local e abra no browser:

```text
python scripts/abrir_produto.py
```

Endereço: `http://127.0.0.1:8766/index.html`

## Jornada

1. `00_mestre.md` — estabelece contexto, segurança e regras.
2. `01_limpar.md` — transforma dados brutos em dados confiáveis.
3. `02_inteligencia.md` — cria métricas, comparações e evidências.
4. `03_oportunidades.md` — converte achados em backlog priorizado.
5. `04_contrato_produto.md` — define comportamento e critérios do produto.
6. `05_construir_produto.md` — gera a aplicação local.
7. `06_testar_red_team.md` — executa testes funcionais e adversariais.
8. `07_juiz.md` — avalia a entrega final.

## Dados

Pasta `dados/`:

- `audiencia_portal.csv`
- `conteudos.csv`
- `search_console.csv`
- `auditoria_sites.csv`
- `visibilidade_ia.csv`
- `metas.csv`

Os arquivos contêm inconsistências intencionais para a etapa de limpeza. Nenhum domínio, portal, concorrente, consulta ou pessoa representa uma entidade real.

## Relação com o curso

| Etapa | Aprendizado aplicado |
|---|---|
| 00 | Context engineering, regras persistentes e escopo |
| 01 | Bronze → Silver, qualidade, PII e regras reproduzíveis |
| 02 | Gold, EDA, métricas, metas e separação fato/interpretação |
| 03 | IA orientada a decisão, priorização e evidência |
| 04 | Discovery, contrato de dados e contrato de produto |
| 05 | Construção incremental de produto com IA |
| 06 | Testes, prompt injection, segurança e observabilidade |
| 07 | Avaliação por rubrica, rastreabilidade e governança |

## Regra de ouro

O produto pode afirmar o que os dados mostram. Para explicar por que algo aconteceu, deve existir evidência causal; caso contrário, deve escrever `sem evidencia causal`.
