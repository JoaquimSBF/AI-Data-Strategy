# Contrato do produto — Mesa de Discovery

Público: produto, operações, jurídico e tecnologia.
Período das atas: 2026-03-04 a 2026-03-18.
Conector: arquivos locais e `sample-data.js`. Sem Jira ou CRM ao vivo.

## Jornada

```text
Importar ou usar demonstração
→ validar evidências
→ filtrar tipo
→ abrir requisito com fonte
→ revisar conflitos e perguntas
→ mover aprovação
→ exportar matriz
```

## Telas

1. Visão executiva — cobertura de fonte, perguntas, MVP e conflitos.
2. Evidências — catálogo Silver, inclusive tipos sem requisito.
3. Requisitos — só itens com evidencia_id.
4. Conflitos — prazo em aberto e fora de escopo.
5. Perguntas — aprovador e risco jurídico.
6. Aprovação — kanban persistente por papel.
7. Dados — importar, restaurar, apagar, exportar.

## Regras

- Sem evidencia_id não existe requisito.
- E99 é texto adversário e não vira requisito.
- Prazo oficial = nao_definido.
- Aprovador único = nao_definido.
- Ideia rejeitada permanece fora de escopo.

## Persistência

- `localStorage` chave `discovery-workbench-v1`.
- Guardar backlog, notas e status.
- Botão para apagar dados locais.

## Segurança

- `textContent` para dados importados.
- Sem `innerHTML` com dado externo.
- Sem `eval` / `Function` / CDN.
- Arquivo máximo 5 MB; só `.csv` e `.json`.
- PII: bloquear e-mail ou CPF.

## Fora de escopo

- Jira ao vivo.
- CRM ao vivo.
- App mobile nativo.
- Inventar o oitavo requisito do MVP.

## Definição de pronto

A aplicação abre offline, mostra os 7 requisitos com fonte, o conflito de prazo, as perguntas abertas e exporta a matriz.
