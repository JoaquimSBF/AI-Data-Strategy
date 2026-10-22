# MCP — exemplo deste case

O harness (etapas 00–07) usa só CSVs sintéticos. Este exemplo é a ponte para dado real.

| Servidor no JSON | Uso | Modo |
|---|---|---|
| `admin-postgres` | réplica do Admin em PostgreSQL via `uvx` | restricted (leitura) |
| `admin-postgres-docker` | o mesmo, via Docker | restricted |
| `hubspot` | CRM ao vivo | token no ambiente |

Use **um** bloco Postgres, não os dois. Power BI não tem MCP neste case.

1. Copie `mcp.json.example` para `.cursor/mcp.json` do seu workspace.
2. Copie `env.example` para `.env` e preencha host/banco. Sem senha no chat.
3. Customize → MCP: o servidor deve ficar verde.
4. Não peça `SELECT *` com PII.
