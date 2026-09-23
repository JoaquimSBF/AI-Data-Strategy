# Mapa de funcionalidades — Inteligência do Portal

Este mapa descreve o produto esperado após a etapa 05.

## Navegação

```text
[ Visão executiva ]
[ Audiência ]
[ Busca ]
[ Benchmark ]
[ Visibilidade em IA ]
[ Oportunidades ]
[ Dados e exportação ]
```

## Visão executiva

- filtro de período;
- KPIs;
- comparação com metas;
- variações;
- principais evidências;
- limitações.

Cada KPI deve permitir abrir:

- fonte;
- fórmula;
- período;
- limitação.

## Audiência

- usuários;
- sessões;
- pageviews;
- tempo médio;
- rejeição;
- assinaturas atribuídas;
- mix por editoria;
- tabela acessível.

## Busca

- impressões;
- cliques;
- CTR ponderado;
- posição ponderada;
- consulta;
- página;
- evolução mensal.

## Benchmark

- portal próprio;
- concorrente alpha;
- concorrente beta;
- performance;
- SEO técnico;
- dados estruturados;
- mobile;
- carregamento.

Não deve existir score geral inventado.

## Visibilidade em IA

- quantidade de testes;
- citações por domínio;
- `nenhum`;
- tema;
- mecanismo;
- data.

Aviso obrigatório: amostra sintética e datada.

## Oportunidades

Modos:

- lista;
- kanban.

Ações:

- filtrar;
- abrir evidências;
- alterar status;
- atribuir papel;
- definir prazo;
- incluir nota;
- criar oportunidade;
- descartar com justificativa;
- exportar.

## Dados e exportação

- importar CSV/JSON;
- validar cabeçalhos;
- exibir erros;
- restaurar demonstração;
- apagar dados locais;
- exportar backlog;
- gerar resumo Markdown.

## Comportamentos esperados

| Situação | Resposta |
|---|---|
| Métrica ausente | `sem evidencia` |
| Evidência causal ausente | `sem evidencia causal` |
| Arquivo inválido | erro explicativo sem travar |
| Texto malicioso | exibido como texto ou bloqueado |
| PII | bloquear/pseudonimizar e registrar |
| IA sem citação | contabilizar como `nenhum` |
| Meta fora da vigência | não comparar |
| Alteração no backlog | persistir localmente |

## Demonstração sugerida

1. Abrir com a amostra.
2. Filtrar um período.
3. Abrir a evidência de um KPI.
4. Comparar portal e concorrentes.
5. Mostrar a limitação da visibilidade em IA.
6. Mover uma oportunidade no kanban.
7. Recarregar e confirmar persistência.
8. Exportar o backlog.
9. Importar um arquivo inválido.
10. Apagar os dados locais.
