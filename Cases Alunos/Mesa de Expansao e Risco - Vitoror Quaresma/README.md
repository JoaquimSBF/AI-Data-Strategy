# Mesa de Expansão e Risco — Vitoror Quaresma

Case didático com dados 100% sintéticos para cruzar CRM, Admin e export de NPS e sair com fila de ação.

## Desafio

Cruzar MAU, NPS, % de alocação de licenças, deals e histórico de upsell/downsell sem puxar tudo à mão.

Power BI não é fonte. Os dashes são o sintoma.

## Jornada

1. `00_mestre.md` — regras e limites.
2. `01_limpar.md` — Bronze → Silver.
3. `02_inteligencia.md` — cruzamento, sinais e evidências.
4. `03_oportunidades.md` — fila de ação.
5. `04_contrato_produto.md` — comportamento do produto.
6. `05_construir_produto.md` — HTML local.
7. `06_testar_red_team.md` — testes e segurança.
8. `07_juiz.md` — rubrica.
9. `08_mcp.md` — opcional: exemplo de MCP para dado real.

## Como abrir no final

```text
python scripts/abrir_produto.py
```

Endereço: `http://127.0.0.1:8769/index.html`

## MCP

Pasta `mcp/`: `mcp.json.example` e `env.example`. Só-leitura. O produto da etapa 05 não depende do MCP.

## Regra de ouro

Score de risco ≠ probabilidade. Sem evento `churn` datado, previsão de churn é `sem evidencia`.
