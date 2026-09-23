# Radar de Saúde do Cliente — Caso 03

Case didático com dados 100% sintéticos para operar sinais de saúde de clientes e projetos.

## Desafio

Criar uma aplicação que:

- consolide sinais de projeto, reunião, ticket e NPS;
- explique cada alerta com fonte e fórmula;
- abra plano de ação com papéis;
- recuse churn sem histórico de saída.

## Produto final

O resultado não é um dashboard de probabilidade. A etapa 05 gera uma **mesa operacional local**:

- carteira com score de sinais;
- detalhe do cliente;
- kanban de ações;
- persistência no navegador;
- churn mensal sempre como `sem evidencia` neste conjunto.

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

Endereço: `http://127.0.0.1:8768/index.html`

## Jornada

1. `00_mestre.md` — estabelece contexto, segurança e regras.
2. `01_limpar.md` — transforma a carteira bruta em Silver.
3. `02_inteligencia.md` — cria sinais, KPIs e evidências.
4. `03_oportunidades.md` — converte sinais em planos de ação.
5. `04_contrato_produto.md` — define comportamento e critérios do produto.
6. `05_construir_produto.md` — gera a aplicação local.
7. `06_testar_red_team.md` — executa testes funcionais e adversariais.
8. `07_juiz.md` — avalia a entrega final.

## Dados

Pasta `dados/`:

- `clientes.csv`
- `projetos.csv`
- `eventos.csv`
- `tickets.csv`
- `nps.csv`
- `metas.csv`

Clientes são identificadores `CLxx`. `data_saida` está vazia em todas as linhas. Não há histórico de status.

## Relação com o curso

| Etapa | Aprendizado aplicado |
|---|---|
| 00 | Context engineering, limites de churn e anti-causalidade |
| 01 | Bronze → Silver, status canônico e ausência de data de saída |
| 02 | Score explicável e recusa de métrica impossível |
| 03 | Playbook, priorização e human-in-the-loop |
| 04 | Contrato de produto e estados de erro |
| 05 | Workspace operacional, não painel morto |
| 06 | Segurança e recusa de métrica inventada |
| 07 | Rubrica e governança de métrica |

## Regra de ouro

Sinal ≠ alerta ≠ inativo ≠ churn. Sem `data_saida` e sem histórico de status, `churn_clientes_pct` é `sem evidencia`.
