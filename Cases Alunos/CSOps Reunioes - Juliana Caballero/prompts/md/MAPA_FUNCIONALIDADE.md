# Mapa de funcionabilidade — Mesa CS

Produto: `produto/index.html`  
Abrir: dois cliques no Chrome, Edge ou Firefox. Sem instalar nada.

## Tela (de cima para baixo)

```
[ Titulo Mesa CS ]                         [ Fonte: amostra / arquivo ]
[ Conectar CSV/TXT ] [ Copiar para o Gemini ] [ Colar JSON ] [ Voltar à amostra ]
[ Lista de reunioes ]  [ Transcricao mascarada ]  [ PRE | POS | caixa de texto ]
```

## Controles

| O que voce ve | O que faz |
|---------------|-----------|
| Lista a esquerda | Clique numa reuniao para abrir transcricao + fichas |
| Badge **ok** / **risco** | Classificacao da call (NPS baixo ou palavras como cancelar, travou, nao imprime) |
| Centro | Transcricao com e-mail, telefone e CPF trocados por `[EMAIL]` `[TEL]` `[CPF]` |
| **Pre-reuniao** | Historico da mesma loja (calls anteriores). Se nao houver: "sem historico" |
| **Pos-reuniao** | Temas + 3 acoes |
| **Colar transcricao avulsa** | Cola um Meet novo; use com "Copiar para o Gemini" |
| **Conectar CSV / TXT** | Carrega `dados/reunioes.csv`, `transcricoes.csv`, `clientes.csv` ou um `.txt` da pasta `dados/transcricoes/` |
| **Copiar para o Gemini** | Copia o prompt da reuniao atual. Cole no Gemini. Depois use Colar JSON |
| **Colar JSON do Gemini** | Cola `{"fichas":[...]}` e atualiza PRE/POS |
| **Voltar a amostra** | Restaura os dados que ja vem no HTML |

## Roteiro de uso (5 minutos)

1. Abra `produto/index.html`.
2. Clique em **Loja Centro** (R003 ou R010) — deve aparecer **risco**.
3. Clique em **Loja Moema** (R001) — deve aparecer **ok** e PRE com historico.
4. Opcional: Conectar os CSVs de `dados/`.
5. Opcional: Copiar para o Gemini → colar a resposta em Colar JSON.

## O que NAO faz

Nao le a pasta do Google Meet sozinho. Nao manda Slack. Nao calcula % de churn.
