# Mapa de funcionabilidade — Painel de desvio

Produto: `produto/index.html`  
Abrir: dois cliques no Chrome, Edge ou Firefox. Sem instalar nada.

## Tela (de cima para baixo)

```
[ Titulo Painel de desvio ]
[ Orçamento CSV ] [ Realizado CSV ] [ Copiar para o Gemini ] [ Amostra ]
[ 4 KPIs: orcado | realizado | desvio | qtd alertas TI-no-RH ]
[ Caixa vermelha de alertas (se houver) ]
[ Barras por centro de custo + tabela ]
[ Tabela por mes ]
```

## Controles

| O que voce ve | O que faz |
|---------------|-----------|
| **Orcamento CSV** | Carrega `dados/orcamento.csv` (substitui o orcado da amostra) |
| **Realizado CSV** | Carrega `dados/realizado.csv` (substitui o realizado) |
| **Copiar para o Gemini** | Copia totais e alertas para um resumo de diretorio. O painel ja e o produto |
| **Amostra** | Volta aos numeros embutidos |
| **KPI desvio** | Verde se realizado <= orcado; vermelho se estourou |
| **KPI alertas** | Quantos lancamentos de TI no centro de custo RH (notebooks, monitores) |
| **Caixa de alerta** | Lista id, mes, valor e descricao desses lancamentos |
| **Barras** | Realizado vs orcado por TI, RH, Marketing, Operacoes. Vermelho se estourou |
| **Tabela mes** | Desvio mes a mes |

## Roteiro de uso (5 minutos)

1. Abra `produto/index.html`.
2. Veja o KPI de **alertas** > 0 (TI no RH).
3. Leia a caixa vermelha: notebooks e monitores.
4. Compare barras: TI e RH devem aparecer no estouro em algum mes.
5. Opcional: carregue `dados/orcamento.csv` e depois `dados/realizado.csv`.

## O que NAO faz

Nao trava compra no ERP. Nao recomenda demissao.
