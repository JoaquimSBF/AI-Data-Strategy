# Inteligência Radar de Saúde do Cliente — etapa 02

Clientes Silver: 6.
Sinal alto: 3.
Tickets com SLA estourado: 4.
churn_clientes_pct: sem evidencia.

## 1. Sinais por cliente

| cliente | segmento | status | score | nivel | nps | atraso | tickets abertos |
|---|---|---|---:|---|---|---:|---:|
| CL01 | enterprise | ativo | 0 | baixo | 72 | 0 | 0 |
| CL02 | enterprise | ativo | 5 | alto | 28 | 21 | 2 |
| CL03 | mid | ativo | 0 | baixo | 64 | 0 | 0 |
| CL04 | smb | inativo | 5 | alto | sem evidencia | 45 | 1 |
| CL05 | smb | ativo | 0 | baixo | sem evidencia | 0 | 0 |
| CL06 | enterprise | inativo | 6 | alto | 15 | 12 | 1 |

- fato_observado: score é soma de flags, não probabilidade.
- limitacao: snapshot de status; sem data_saida.

## 2. Metas

Ver `metas_status.csv`. A meta de churn permanece sem evidencia.

## 3. Lacunas

- CL04 e CL05 sem NPS válido.
- CL04 e CL06 inativos sem data de saída.
- T99 isolado.
- sem evidencia causal entre ausência em QBR e risco futuro.
