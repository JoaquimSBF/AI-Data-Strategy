# ETAPA 08 — MCP (opcional, dado real)

## O que vamos fazer
Ligar extração só-leitura. O produto da etapa 05 **não depende** desta etapa.

## Conexão com o curso
- Ponte para dado real, secrets fora do código, menor privilégio.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Copie só INÍCIO–FIM.
2. Anexe `mcp/mcp.json.example` e `mcp/README.md`.
3. Não cole senha, token nem URI completa no chat.
4. No Cursor: copie o exemplo para `.cursor/mcp.json` do **seu** ambiente e preencha o `.env` local.

### Arquivos necessários

Da pasta `Mesa de Expansao e Risco - Vitoror Quaresma/mcp/`:
1. mcp.json.example
2. env.example
3. README.md

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 08.
Explique como ligar o MCP sem quebrar o contrato do case.

Regras:
1. Use o arquivo de exemplo. Não invente outro servidor.
2. Admin: MCP PostgreSQL em modo restricted / só leitura. URI no .env, nunca no JSON commitado.
3. HubSpot: bloco de exemplo com URL/OAuth. Token fica no ambiente, não no arquivo.
4. Power BI: não há MCP neste case. Continua export CSV do modelo.
5. As colunas reais devem caber no contrato Silver (cliente_id, deals, atividades, licenças, eventos, NPS).
6. PII (e-mail, telefone, empresa, dono do deal) não entra no produto. Pseudonimize na extração.
7. Se o MCP estiver desligado, o produto usa sample-data.js. Isso é sucesso, não falha.
8. Não rode INSERT, UPDATE, DELETE nem crie tabela.

Entregue: um guia curto de ativação e a lista do que cada ferramenta MCP pode ler.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- outputs/08_guia_mcp.md
