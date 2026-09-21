# MODO: EDA (perguntas de negocio)

Entrada: Gold (kpis_mensais, mix produto/canal, receita, churn/status, metas).
Objetivo: responder perguntas de negocio com evidencia.

Perguntas obrigatorias:
1) Como estao captacao, resgate e captacao liquida por mes?
2) Quais produtos puxam o resultado?
3) Quais canais se destacam?
4) Como estao receita e churn/status? Ha alerta versus meta?

Importante sobre churn:
- `status_snapshot` / clientes inativos e um **snapshot pontual**, nao taxa mensal de churn.
- Se nao houver data de inativacao, escreva **sem evidencia** para comparar com a meta `churn_clientes_pct`.
- Nao confunda % de inativos com churn mensal.

Tarefa:
- Responda cada pergunta com numeros da base.
- Cite a tabela/fonte usada.
- Aponte 3 insights acionaveis e 2 riscos/limites dos dados.
- Sugira 3 graficos (titulo + eixos + o que mostram).
- Gere o arquivo completo analise_final.md.

Regras:
- Nao invente valor. Se nao estiver nos dados, escreva "sem evidencia".
- Separar fato observado de interpretacao.
- Status OK/NOK no final.

Dados Gold:
<<<
[COLE KPIs / TABELAS / TRECHOS]
>>>

## ONDE SALVAR
Salve manualmente em:

- `outputs/analise_final.md` -> documento principal da EDA (obrigatorio)
- `outputs/eda_notas.md` -> opcional (rascunhos e graficos sugeridos)
