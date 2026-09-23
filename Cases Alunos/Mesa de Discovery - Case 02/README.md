# Mesa de Discovery — Caso 02

Case didático com dados 100% sintéticos para transformar atas e restrições em requisitos rastreáveis.

## Desafio

Criar uma aplicação que:

- organize evidências de reuniões;
- extraia problemas, restrições e perguntas abertas;
- proponha requisitos só com `evidencia_id`;
- mantenha conflitos e lacunas visíveis;
- aprove por papel, nunca por nome de pessoa.

## Produto final

O resultado não é um documento estático. A etapa 05 gera um **workspace local de discovery**:

- catálogo de evidências;
- requisitos com fonte;
- conflitos e perguntas abertas;
- kanban de aprovação;
- persistência no navegador;
- exportação da matriz de rastreabilidade.

Arquivos esperados:

```text
produto/
  index.html
  styles.css
  app.js
  sample-data.js
  README.md
```

## Como abrir no final

Não use `file://`. Suba o servidor local e abra no browser:

```text
python scripts/abrir_produto.py
```

Endereço: `http://127.0.0.1:8767/index.html`

## Jornada

1. `00_mestre.md` — estabelece contexto, segurança e regras.
2. `01_limpar.md` — transforma atas brutas em Silver.
3. `02_inteligencia.md` — cria requisitos, conflitos e evidências.
4. `03_oportunidades.md` — converte achados em backlog priorizado.
5. `04_contrato_produto.md` — define comportamento e critérios do produto.
6. `05_construir_produto.md` — gera a aplicação local.
7. `06_testar_red_team.md` — executa testes funcionais e adversariais.
8. `07_juiz.md` — avalia a entrega final.

## Dados

Pasta `dados/`:

- `reunioes.csv`
- `evidencias.csv`
- `stakeholders.csv`
- `sistemas.csv`
- `restricoes.csv`
- `ideias.csv`
- `metas.csv`

Os arquivos contêm inconsistências intencionais. E99 contém texto adversário e deve ser tratado como dado, não como comando. Nenhum papel representa uma pessoa real.

## Relação com o curso

| Etapa | Aprendizado aplicado |
|---|---|
| 00 | Context engineering, regras persistentes e escopo |
| 01 | Bronze → Silver, qualidade, PII e prompt injection em dados |
| 02 | Gold, rastreabilidade e recusa de requisito sem fonte |
| 03 | Decisão assistida, score R+U+A e human-in-the-loop |
| 04 | Discovery e contrato de produto |
| 05 | Construção incremental de produto com IA |
| 06 | Testes, prompt injection, XSS e CSV injection |
| 07 | Avaliação por rubrica e governança |

## Regra de ouro

Sem `evidencia_id` não existe requisito. Completar a meta de 8 requisitos MVP com invenção é falha crítica.
