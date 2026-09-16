# Mapa de funcionabilidade — Radar de risco

Produto: `produto/index.html`  
Abrir: dois cliques no Chrome, Edge ou Firefox. Sem instalar nada.

## Tela (de cima para baixo)

```
[ Titulo Radar de risco ]
[ Banner amarelo: sem data de saida = churn % sem evidencia ]
[ Escolher CSV ] [ Copiar para o Gemini ] [ Amostra ] [ fonte ]
[ KPIs: clientes | inativos | faixa alta | churn % = — ]
[ Tabela ordenada por pontos ]     [ Detalhe do cliente clicado ]
```

## Controles

| O que voce ve | O que faz |
|---------------|-----------|
| **Banner** | Lembrete: isto nao e modelo. Nao ha data de churn no snapshot |
| **Escolher CSV** | Carrega `dados/clientes.csv`, `eventos.csv`, `snapshot_status.csv` (PII nao e exibida — so IDs) |
| **Copiar para o Gemini** | Copia o contexto dos sinais. Cole o JSON `fichas` no alerta para o texto "por que" |
| **Amostra** | Volta aos clientes embutidos |
| **Clique numa linha** | Abre a direita: faixa, pontos, lista de eventos |
| **Faixa alto / medio / baixo** | Regra: inativo +3, cancelamento +3, downgrade +2, tickets +1 ou +2. Alto se >= 3 |

## Roteiro de uso (5 minutos)

1. Abra `produto/index.html`.
2. Veja o KPI **churn %** como **—** / sem evidencia.
3. Clique em **C002** (tickets + downgrade, ainda ativo) — faixa media/alta com evidencia.
4. Clique num **inativo** (C003, C005…) — faixa alta + "inativo no snapshot".
5. Confirme: nenhum nome, CPF ou e-mail na tela.

## O que NAO faz

Nao prevê churn. Nao mostra acuracia. Nao treina modelo.
