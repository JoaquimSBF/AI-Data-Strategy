# Contrato do produto — Radar de Saúde do Cliente

Público: CS, operações, suporte e dados.
Período dos sinais: 2026-01 a 2026-03.
Conector: arquivos locais e `sample-data.js`. Sem CRM ao vivo.

## Jornada

```text
Importar ou usar demonstração
→ filtrar segmento e nível
→ observar carteira
→ abrir cliente e evidência
→ mover ação
→ exportar acompanhamento
```

## Telas

1. Visão executiva — clientes válidos, sinal alto, SLA e churn sem evidencia.
2. Carteira — tabela filtrável.
3. Cliente — detalhe e flags.
4. Sinais — matriz binária.
5. Ações — kanban persistente.
6. Dados — importar, restaurar, apagar, exportar.

## Regras

- Score = soma de flags; não é probabilidade.
- Sinal ≠ alerta ≠ inativo ≠ churn.
- `churn_clientes_pct` aparece como `sem evidencia`.
- NPS ausente não é imputado.
- Inativo no snapshot não prova saída.

## Persistência

- `localStorage` chave `client-health-radar-v1`.
- Guardar ações, filtros, notas e status.

## Segurança

- `textContent` para dados importados.
- Sem `innerHTML` com dado externo.
- Sem `eval` / `Function` / CDN.
- Arquivo máximo 5 MB; só `.csv` e `.json`.
- Bloquear PII e rótulo de probabilidade de churn.

## Fora de escopo

- CRM ao vivo.
- Modelo preditivo de churn.
- Cancelamento automático de contrato.

## Definição de pronto

A aplicação abre offline, mostra 6 clientes, 3 sinais altos, 4 SLAs estourados e recusa calcular churn.
