# Mapa de funcionabilidade — Landing Orbe Digital

Produto: `produto/index.html`  
Abrir: dois cliques no Chrome, Edge ou Firefox. Sem instalar nada.

## Tela (de cima para baixo)

```
[ Orbe Digital ]                    [ PT ] [ EN ] [ ES ]
[ Conectar CSV ] [ Copiar para o Gemini ] [ Amostra ] [ fonte ]
[ Hero: titulo + subtitulo + botao Ver mix ]
[ 4 KPIs: sessoes | leads | conversao | receita ]
[ Tabela por mes ]
[ Mix produto (barras) ]
[ Mix canal (barras) ]
[ Rodape: arquivo local, nao e Power BI ao vivo ]
```

## Controles

| O que voce ve | O que faz |
|---------------|-----------|
| **PT / EN / ES** | Troca os textos da landing. Se faltar traducao, o HTML nao inventa |
| **Conectar CSV** | Selecione um ou mais: `dados/metricas.csv`, `produtos.csv`, `canais.csv`, `textos_ui.csv` |
| **Copiar para o Gemini** | Gera copy i18n. Depois cola o JSON no alerta |
| **Amostra** | Volta aos numeros que ja vem no HTML |
| **Ver mix de produto** | Rola ate as barras de mix |
| KPIs | Ultimo mes com evidencia. `null` aparece como "sem evidencia" |
| Barras | Tamanho proporcional ao valor (CSS, sem biblioteca) |

## Roteiro de uso (5 minutos)

1. Abra `produto/index.html`.
2. Confira os 4 KPIs (ultimo mes com dado).
3. Clique **EN** e **ES** — o titulo muda; campo sem traducao nao e inventado.
4. Role ate o mix. Pago deve liderar em leads; Landing Analytics no mix de produto.
5. Opcional: conectar os CSVs de `dados/`.

## O que NAO faz

Nao atualiza sozinho (nao e Power BI / MCP). E HTML estatico + arquivo local.
