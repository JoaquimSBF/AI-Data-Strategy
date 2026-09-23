# ETAPA 01 — Limpeza e Silver

## Conexão com o curso
- Qualidade, status canônico, quarentena, ausência de data de saída.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

Anexe só a pasta dados/. Não use outputs/.

### Arquivos necessários

Da pasta `Client Health Radar - Case 03/dados/`:
1. clientes.csv
2. projetos.csv
3. eventos.csv
4. tickets.csv
5. nps.csv
6. metas.csv
7. README_DADOS.md

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 01.
Padronize datas, segmento (enterprise/mid/smb), status (ativo/inativo), fase e severidade.
Quarentena: cliente sem data_entrada, atraso negativo, SLA n/a, duplicata, segmento TESTE.
Não impute data_saida. Não calcule churn.

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- outputs/01_relatorio_qualidade.md
- outputs/silver/*.csv
- outputs/silver/quarentena.csv
