# ETAPA 03 — Backlog de oportunidades orientado por evidências

## O que vamos fazer

Transformar achados analíticos em oportunidades que possam ser revisadas, atribuídas e acompanhadas no produto.

O objetivo não é gerar recomendações genéricas. Cada oportunidade deve nascer de uma evidência existente.

## Conexão com o curso

- IA como apoio à decisão.
- RORO: receber evidências estruturadas e devolver oportunidades estruturadas.
- Guardrails contra causalidade inventada.
- Priorização transparente.
- Human-in-the-loop.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Continue no mesmo chat.
2. Copie somente o trecho entre `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
3. Cole o prompt.
4. Anexe todos os arquivos abaixo.
5. Salve as três saídas indicadas.

### Arquivos necessários

Da pasta `Portal Intelligence - Case 01/outputs/`:

1. `02_inteligencia.md`

Da pasta `Portal Intelligence - Case 01/outputs/gold/`:

2. `kpis_mensais.csv`
3. `mix_editoria.csv`
4. `busca_mensal.csv`
5. `benchmark_sites.csv`
6. `visibilidade_ia_resumo.csv`
7. `qualidade_conteudo.csv`
8. `metas_status.csv`
9. `evidencias.json`
10. `testes_integridade.csv`

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 03 da Inteligência do Portal: transformar evidências em um backlog priorizado de oportunidades.

Use somente os arquivos da etapa 02 listados no guia. Não crie oportunidade sem `evidencia_id`.

## Tipos permitidos

- `audiencia`
- `engajamento`
- `busca`
- `seo_tecnico`
- `conteudo`
- `visibilidade_ia`
- `qualidade_dados`

## Estrutura da oportunidade

```json
{
  "oportunidade_id": "OPP-001",
  "titulo": "texto curto",
  "tipo": "busca",
  "problema_observado": "fato sem causalidade",
  "evidencias": ["EVD-001", "EVD-004"],
  "acao_proposta": "ação testável",
  "resultado_esperado": "hipótese, não promessa",
  "metrica_acompanhamento": "kpi existente",
  "baseline": 0,
  "unidade": "pct",
  "prioridade": "alta|media|baixa",
  "confianca": "alta|media|baixa",
  "responsavel_sugerido": "papel, não pessoa",
  "status": "nova",
  "limitacoes": ["texto"],
  "aprovacao_humana_obrigatoria": true
}
```

## Rubrica de prioridade

Avalie três dimensões de 1 a 3:

- `relevancia`: tamanho do gap ou volume afetado;
- `urgencia`: piora recente ou meta vigente não atingida;
- `acionabilidade`: existe ação e métrica de acompanhamento disponíveis.

`score_prioridade = relevancia + urgencia + acionabilidade`.

- 8–9: alta;
- 5–7: média;
- 3–4: baixa.

Mostre os três componentes. Não atribua nota sem justificar com evidência.

## Confiança

- Alta: duas ou mais fontes coerentes e sem lacuna material.
- Média: uma fonte suficiente ou amostra limitada.
- Baixa: dado incompleto, amostra pequena ou hipótese dependente de validação.

Resultados de visibilidade em IA não podem receber confiança alta neste case, pois são amostras limitadas.

## Regras

1. Cada oportunidade deve citar ao menos um `evidencia_id`.
2. Não inferir intenção de usuário, qualidade jornalística ou motivo de queda.
3. Não sugerir manipulação de buscadores ou produção de conteúdo enganoso.
4. Não copiar estratégia proprietária de concorrentes.
5. Ações devem ser experimentos ou verificações reversíveis.
6. O responsável é um papel: `editoria`, `seo`, `produto`, `dados` ou `tecnologia`.
7. Se não houver ação sustentada, não criar oportunidade.
8. Máximo de 12 oportunidades para manter foco.

## Material

```text
<<<
[ANEXE OU COLE 02_inteligencia.md E OS NOVE ARQUIVOS DE outputs/gold/]
>>>
```

## Critérios de aceite

- Nenhuma oportunidade sem evidência.
- Nenhuma promessa de resultado.
- Score recalculável.
- Limitações visíveis.
- Responsáveis sem PII.
- Pelo menos uma oportunidade de qualidade de dados, caso haja lacuna relevante.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- `outputs/03_oportunidades.json`
- `outputs/03_oportunidades.csv`
- `outputs/03_backlog_explicado.md`
