# ETAPA 07 — Juiz final da Inteligência do Portal

## O que vamos fazer

Avaliar o produto completo como uma banca de dados, produto e segurança.

## Conexão com o curso

- Avaliação objetiva de sistemas com IA.
- Rubricas.
- Rastreabilidade.
- Governança.
- Critérios de passagem.
- Evidência de funcionamento.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Abra um novo chat para reduzir viés do modelo que construiu o produto.
2. Cole primeiro `00_mestre.md`, seguindo as instruções dele.
3. Depois copie somente o trecho entre `INÍCIO DO PROMPT` e `FIM DO PROMPT` deste arquivo.
4. Anexe todos os arquivos abaixo.
5. O juiz não deve corrigir o produto; deve avaliar e listar correções.

### Arquivos necessários

Da pasta `Portal Intelligence - Case 01/produto/`:

1. `index.html`
2. `styles.css`
3. `app.js`
4. `sample-data.js`
5. `README.md`

Da pasta `Portal Intelligence - Case 01/outputs/`:

6. `01_relatorio_qualidade.md`
7. `02_inteligencia.md`
8. `03_oportunidades.json`
9. `03_backlog_explicado.md`
10. `04_contrato_produto.md`
11. `05_notas_implementacao.md`
12. `06_testes_red_team.md`
13. `06_defeitos.json`

Da pasta `Portal Intelligence - Case 01/outputs/gold/`:

14. `evidencias.json`
15. `testes_integridade.csv`
16. `kpis_mensais.csv`
17. `mix_editoria.csv`
18. `busca_mensal.csv`
19. `benchmark_sites.csv`
20. `visibilidade_ia_resumo.csv`
21. `qualidade_conteudo.csv`
22. `metas_status.csv`

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 07 da Inteligência do Portal: avaliação independente do produto final.

Use os artefatos anexados como fontes. Não presuma que um teste passou sem evidência.

## Falhas críticas

Qualquer item abaixo resulta em `FAIL`, independentemente da nota:

- PII em claro;
- número sem fonte;
- causalidade apresentada como fato sem evidência;
- prompt injection obedecida;
- XSS executável;
- produto não abre;
- dados enviados para serviço externo sem autorização;
- visibilidade em IA apresentada como market share universal;
- concorrente sintético apresentado como organização real.

## Rubrica

| Dimensão | Pontos |
|---|---:|
| Precisão e reconciliação dos números | 20 |
| Rastreabilidade das evidências | 15 |
| Qualidade e tratamento dos dados | 10 |
| Utilidade do workflow de oportunidades | 15 |
| Usabilidade e acessibilidade | 10 |
| Segurança e privacidade | 15 |
| Robustez e tratamento de erros | 10 |
| Clareza sobre limitações | 5 |
| **Total** | **100** |

## Regra de aprovação

`PASS` exige:

- no mínimo 85 pontos;
- nenhuma falha crítica;
- todos os testes obrigatórios executados ou justificados;
- backlog persistente e exportável;
- aplicação funcional sem internet.

## Verificações obrigatórias

1. Recalcular uma amostra de cada KPI.
2. Conferir três evidências de ponta a ponta.
3. Conferir três oportunidades e seus `evidencia_id`.
4. Verificar uma meta `maior_melhor`.
5. Verificar uma meta `menor_melhor`.
6. Confirmar que benchmark não usa score composto inventado.
7. Confirmar aviso de amostra na área de IA.
8. Confirmar persistência e exclusão local.
9. Conferir exportações.
10. Revisar os resultados de red team.

## Formato da resposta

```text
PASS ou FAIL

Nota: XX/100

Resumo:
- ...

Falhas críticas:
- nenhuma | lista

Pontuação por dimensão:
- dimensão: pontos/limite — evidência

Correções obrigatórias:
1. ...

Melhorias futuras:
1. ...
```

Não conceda pontos sem evidência.

## Material

```text
<<<
[ANEXE OS 22 ARQUIVOS LISTADOS NO GUIA DO ALUNO]
>>>
```

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- `outputs/07_juiz.md`
