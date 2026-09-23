# Como funciona — Inteligência do Portal

## O produto

A Inteligência do Portal é um workspace local de inteligência editorial.

Ele combina:

- audiência;
- engajamento;
- busca;
- auditoria comparativa;
- amostras de visibilidade em IA;
- metas;
- evidências;
- backlog de oportunidades.

O valor não está apenas em mostrar gráficos. O produto conecta:

```text
dado → evidência → decisão → oportunidade → acompanhamento
```

## Por que existem oito etapas

### 00 — Constituição

Evita que regras essenciais sejam esquecidas ao longo da conversa.

### 01 — Silver

Impede que tipos misturados, duplicatas ou dados inválidos contaminem as conclusões.

### 02 — Inteligência

Cria métricas reproduzíveis e um livro de evidências.

### 03 — Oportunidades

Converte fatos em ações testáveis, sem inventar causas.

### 04 — Contrato

Define o produto antes do código.

### 05 — Construção

Gera uma aplicação local com importação, persistência, workflow e exportação.

### 06 — Red team

Testa erros, PII, prompt injection, XSS e arquivos malformados.

### 07 — Juiz

Recalcula amostras, confere requisitos e decide `PASS` ou `FAIL`.

## O que torna este case diferente

O produto não é:

- uma auditoria SEO real;
- uma integração ao vivo;
- um sistema que mede toda a presença em IAs;
- uma ferramenta para copiar concorrentes;
- uma máquina de afirmar causalidade.

Ele é uma simulação auditável de como dados e IA podem apoiar decisões editoriais.

## Como usar em aula

1. Executar uma etapa por vez.
2. Discutir a saída antes de avançar.
3. Pedir que outro grupo revise as evidências.
4. Trocar um arquivo por uma versão adversarial.
5. Comparar produtos gerados por modelos diferentes.
6. Encerrar com a banca da etapa 07.
7. Abrir o produto no browser: `python scripts/abrir_produto.py` → `http://127.0.0.1:8766/index.html`.

## Aprendizado esperado

Ao final, o aluno deve conseguir:

- preparar dados;
- definir métricas;
- reconhecer limites;
- escrever contratos;
- construir um produto com IA;
- testar segurança;
- defender decisões com evidências.
