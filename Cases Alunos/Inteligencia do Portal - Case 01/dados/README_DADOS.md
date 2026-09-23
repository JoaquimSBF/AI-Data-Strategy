# Dicionário dos dados sintéticos

Todos os dados deste diretório são sintéticos e didáticos.

## audiencia_portal.csv

Grão esperado após limpeza: uma linha por `ano_mes + editoria`.

| Coluna | Significado |
|---|---|
| ano_mes | Competência da medição |
| editoria | Categoria editorial |
| usuarios | Usuários atribuídos à editoria principal no período |
| sessoes | Sessões no período |
| pageviews | Visualizações de página |
| tempo_medio_seg | Tempo médio em segundos |
| taxa_rejeicao_pct | Taxa de rejeição percentual |
| assinaturas_atribuidas | Assinaturas atribuídas ao conteúdo |

Problemas intencionais: datas mistas, separador de milhar, decimal com vírgula, categorias com caixa/espaço, duplicata e linha inválida.

Neste conjunto sintético, cada usuário é atribuído a uma única editoria principal por competência. Portanto, a soma mensal de `usuarios` representa o total sintético do portal. Essa premissa precisa ser registrada; não deve ser transportada automaticamente para dados reais.

## conteudos.csv

Grão: uma linha por conteúdo.

Não há nome real de autor. `autor_pseudo` é um identificador sintético.

Problemas intencionais: datas mistas, categorias inconsistentes, booleanos heterogêneos, duplicata e conteúdo sem data.

## search_console.csv

Grão esperado: uma linha por `ano_mes + consulta + pagina_id`.

Representa uma exportação sintética de desempenho em busca. Não veio de Google Search Console real.

Problemas intencionais: números formatados, caixa inconsistente e uma consulta sem medição.

## auditoria_sites.csv

Grão: uma linha por `data_coleta + site`.

Os concorrentes `concorrente_alpha` e `concorrente_beta` são fictícios. Os scores representam uma auditoria pública sintética e não devem ser apresentados como medição real.

## visibilidade_ia.csv

Grão: uma linha por execução de pergunta em um mecanismo.

Os mecanismos `ia_a` e `ia_b` são fictícios. Cada observação vale somente para a data, pergunta e mecanismo testados. Não representa participação universal em respostas de IA.

## metas.csv

Contém valor, unidade, direção e período de vigência. A direção impede interpretações erradas:

- `maior_melhor`
- `menor_melhor`

## Regras de privacidade

- Não adicionar nome, e-mail, telefone, documento ou identificador pessoal.
- Se dados reais forem usados futuramente, pseudonimizar antes da importação.
- Não enviar arquivos proprietários para ferramentas sem autorização.
