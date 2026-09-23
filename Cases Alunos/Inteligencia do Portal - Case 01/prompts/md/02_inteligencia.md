# ETAPA 02 — Inteligência, métricas e livro de evidências

## O que vamos fazer

Converter as tabelas Silver em métricas de negócio e evidências rastreáveis.

Ainda não vamos criar telas nem oportunidades.

## Conexão com o curso

- Silver → Gold.
- Modelagem analítica.
- EDA orientada a perguntas de negócio.
- Métricas ponderadas.
- Comparação com metas vigentes.
- Separação entre fato, interpretação e causalidade.
- Rastreabilidade para IA confiável.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Continue no mesmo chat.
2. Copie somente o trecho entre `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
3. Cole o prompt.
4. Anexe os arquivos listados abaixo. Não volte a usar os CSVs brutos de `dados/`.
5. Salve as respostas nos caminhos indicados.

### Arquivos necessários

Da pasta `Portal Intelligence - Case 01/outputs/silver/`:

1. `audiencia.csv`
2. `conteudos.csv`
3. `search_console.csv`
4. `auditoria_sites.csv`
5. `visibilidade_ia.csv`
6. `metas.csv`
7. `quarentena.csv`

Da pasta `Portal Intelligence - Case 01/dados/`:

8. `README_DADOS.md`

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 02 da Inteligência do Portal: inteligência, métricas e livro de evidências.

Você receberá os arquivos Silver da etapa 01 e o dicionário dos dados. Não use os CSVs brutos.

## Perguntas obrigatórias

1. Como audiência, sessões, pageviews e engajamento evoluíram?
2. Quais editorias ganharam ou perderam participação?
3. Como busca orgânica evoluiu em impressões, cliques, CTR e posição?
4. Como o portal próprio se compara aos concorrentes sintéticos?
5. Qual foi a presença observada nas amostras de respostas de IA?
6. Quais metas foram ou não atingidas durante a vigência?
7. Que lacunas impedem uma conclusão?

## Regras de cálculo

### Audiência mensal

- `usuarios_mensais = soma(usuarios)`.
- Essa soma só é permitida porque o dicionário sintético declara atribuição exclusiva por editoria.
- `sessoes = soma(sessoes)`.
- `pageviews = soma(pageviews)`.
- `assinaturas_atribuidas = soma(assinaturas_atribuidas)`.
- `sessoes_por_usuario = sessoes / usuarios_mensais`.
- `pageviews_por_sessao = pageviews / sessoes`.
- `tempo_medio_seg = soma(tempo_medio_seg * sessoes) / soma(sessoes)`.
- `taxa_rejeicao_pct = soma(taxa_rejeicao_pct * sessoes) / soma(sessoes)`.

### Mix de editoria

- Participação de usuários, sessões, pageviews e assinaturas por mês.
- Todo mix deve fechar 100%, tolerância de 0,02 ponto percentual.

### Busca

- `ctr_pct = 100 * soma(cliques) / soma(impressoes)`.
- `posicao_media = soma(posicao_media * impressoes) / soma(impressoes)`.
- Nunca calcular média simples de percentuais ou posições.

### Benchmark dos sites

- Não criar score composto.
- Mostrar separadamente performance, SEO técnico, dados estruturados, mobile e tempo de carregamento.
- Comparar sempre medições da mesma data.

### Visibilidade em IA

- `share_citacao_pct = 100 * testes_com_dominio_citado / total_de_testes`.
- Calcular para portal próprio, concorrentes e `nenhum`.
- Informar quantidade de testes junto com o percentual.
- Não chamar de market share.
- Não generalizar além das perguntas, mecanismos e datas testados.

### Conteúdo

- Usar a maior `data_publicacao` ou `data_atualizacao` disponível como data de referência sintética.
- Calcular presença de schema, FAQ, fontes externas e atualização.
- Não afirmar que um atributo causou audiência, busca ou citação em IA.

### Metas

- Comparar somente quando `ano_mes` estiver dentro de `ano_mes_inicio` e `ano_mes_fim`.
- Respeitar `direcao`.
- Exibir realizado, meta, diferença e status.

## Livro de evidências

Para cada conclusão, gerar:

```json
{
  "evidencia_id": "EVD-001",
  "afirmacao": "texto objetivo",
  "tipo": "fato_observado",
  "valor": 0,
  "unidade": "pct",
  "periodo": "YYYY-MM",
  "fonte": ["arquivo.csv"],
  "formula": "regra reproduzível",
  "limitacao": "null ou texto"
}
```

Interpretações não podem ocupar o campo `fato_observado`.

## Testes obrigatórios

- Gold não vazio.
- Chaves únicas.
- Mix fecha 100%.
- Nenhum percentual fora de 0 a 100.
- Toda meta respeita vigência e direção.
- Todo número do relatório possui uma evidência.
- Nenhuma coluna de PII.
- Nenhuma conclusão causal sem evidência.

## Material

```text
<<<
[ANEXE OU COLE OS SETE ARQUIVOS SILVER E README_DADOS.md]
>>>
```

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- `outputs/02_inteligencia.md`
- `outputs/gold/kpis_mensais.csv`
- `outputs/gold/mix_editoria.csv`
- `outputs/gold/busca_mensal.csv`
- `outputs/gold/benchmark_sites.csv`
- `outputs/gold/visibilidade_ia_resumo.csv`
- `outputs/gold/qualidade_conteudo.csv`
- `outputs/gold/metas_status.csv`
- `outputs/gold/evidencias.json`
- `outputs/gold/testes_integridade.csv`
