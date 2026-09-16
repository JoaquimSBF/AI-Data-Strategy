# ETAPA 02 — Fichas da Mesa CS (JSON)

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/CSOps Reunioes - Juliana Caballero/`

1. No mesmo chat, cole **este arquivo inteiro**.
2. No bloco `<<< >>>`, cole o que voce **ja salvou na etapa 01** (nao use mais o `dados/` cru):

| Arquivo | Pasta |
|---------|--------|
| `reunioes.csv` | `outputs/` |
| `transcricoes.csv` | `outputs/` |
| `clientes.csv` | `outputs/` |

3. Grave a resposta em **ONDE SALVAR**.

Para CADA reuniao valida, gere:
- reuniao_id, cliente_id, loja (sem nome de pessoa), data, cs, nps
- risco: ok | risco
- temas: lista curta (tecnico, expansao, suporte, sentimento_negativo, neutro)
- pre: o que o CS precisa saber ANTES (so com calls anteriores desta loja; se nao houver, "sem historico")
- pos: 3 acoes concretas
- resumo: 1-2 frases com evidencia da transcricao mascarada
- trecho_evidencia: recorte curto ja mascarado (nao invente)

Regras:
- Risco se NPS <= 4 OU texto com cancelar/travou/nao imprime/reduz contrato/inercia.
- Nao invente call que nao existe.
- Sem PII.

Formato: um unico JSON + uma tabela Markdown de conferencia.

Material:
<<<
[COLE os CSVs de outputs/ da etapa 01]
>>>

## ONDE SALVAR
- `outputs/02_fichas.json` — JSON completo (obrigatorio)
- `outputs/02_fichas.md` — tabela de conferencia
