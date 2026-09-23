# ETAPA 05 — Construir a Inteligência do Portal

## O que vamos fazer

Gerar uma aplicação local completa, não apenas uma página de apresentação.

O produto deve permitir observar, decidir, agir e acompanhar.

## Conexão com o curso

- Construção incremental com IA.
- Código como artefato verificável.
- Estado e persistência.
- Produto orientado a workflow.
- Guardrails no frontend.
- Evidência incorporada à experiência.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Continue no mesmo chat ou abra um agente de código na pasta do case.
2. Copie somente o trecho entre `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
3. Cole o prompt.
4. Anexe os arquivos listados abaixo.
5. Se usar chat web, copie cada arquivo gerado para `produto/`.
6. Se usar Cursor, peça para escrever e testar os arquivos diretamente.
7. No final, abra o produto no browser via localhost. Não use `file://`.
   Comando: `python scripts/abrir_produto.py`
   Endereço: `http://127.0.0.1:8766/index.html`

### Arquivos necessários

Da pasta `Portal Intelligence - Case 01/outputs/`:

1. `02_inteligencia.md`
2. `03_oportunidades.json`
3. `03_backlog_explicado.md`
4. `04_contrato_produto.md`

Da pasta `Portal Intelligence - Case 01/outputs/gold/`:

5. `kpis_mensais.csv`
6. `mix_editoria.csv`
7. `busca_mensal.csv`
8. `benchmark_sites.csv`
9. `visibilidade_ia_resumo.csv`
10. `qualidade_conteudo.csv`
11. `metas_status.csv`
12. `evidencias.json`
13. `testes_integridade.csv`

Não anexe os CSVs brutos de `dados/`.

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 05 da Inteligência do Portal: construir e testar a aplicação local definida no contrato.

Use somente os artefatos derivados listados no guia. Não recalcule dados a partir dos arquivos brutos.

## Instrução de implementação

Crie os arquivos:

```text
produto/index.html
produto/styles.css
produto/app.js
produto/sample-data.js
produto/README.md
```

Se estiver em um agente de código, escreva os arquivos diretamente.  
Se estiver em um chat web, devolva um bloco nomeado para cada arquivo, pronto para copiar.

## Restrições técnicas

- HTML, CSS e JavaScript puros.
- Sem CDN.
- Sem chamadas externas.
- Sem framework.
- Sem build.
- Deve abrir em `http://127.0.0.1:8766/index.html` (servidor local). Não usar `file://`.
- Persistência em `localStorage`.
- Dados de demonstração em `sample-data.js`.
- Upload usando `FileReader`.
- Exportações geradas no navegador.

## Funcionalidades obrigatórias

### Dados

- Iniciar com os dados de demonstração.
- Importar arquivos locais.
- Validar nomes de colunas.
- Mostrar quantidade aceita, rejeitada e motivos.
- Restaurar demonstração.
- Apagar dados locais.

### Análise

- Filtro de período.
- KPIs com fonte e fórmula.
- Comparação com meta vigente.
- Audiência e mix de editoria.
- Busca.
- Benchmark.
- Visibilidade em IA com aviso de amostra.
- Tabelas acessíveis acompanhando qualquer visual.

### Evidências

- Botão `Ver evidência` em cada insight.
- Exibir fonte, fórmula, período e limitação.
- Não mostrar insight se o `evidencia_id` não existir.

### Oportunidades

- Lista e kanban.
- Alterar status.
- Atribuir papel responsável.
- Definir prazo.
- Adicionar nota.
- Criar oportunidade manual.
- Vincular evidências.
- Manter histórico local.
- Exportar CSV e JSON.

### Resumo

- Gerar Markdown executivo usando apenas dados carregados.
- Cada número precisa de fonte.
- Separar fato e interpretação.
- Incluir limitações.

## Design

- Aparência editorial e executiva.
- Hierarquia clara.
- Navegação lateral ou superior.
- Máximo de uma cor de destaque além dos estados semânticos.
- Sem gradiente, excesso de cards ou elementos decorativos.
- Responsivo.
- Impressão legível.

## Segurança de renderização

- Usar `textContent` para dados importados.
- Não inserir texto importado via `innerHTML`.
- Não usar `eval`, `Function`, script dinâmico ou URL externa.
- Tratar fórmulas como texto.
- Rejeitar arquivo acima de 5 MB.
- Aceitar apenas `.csv` e `.json`.

## Autoavaliação obrigatória

Antes de entregar:

1. Conferir console sem erros.
2. Abrir com dados de demonstração.
3. Testar filtro.
4. Alterar uma oportunidade e recarregar a página.
5. Exportar backlog.
6. Restaurar demonstração.
7. Testar arquivo inválido.
8. Confirmar ausência de PII.
9. Confirmar que nenhum número foi digitado fora de `sample-data.js`.
10. Confirmar que a aplicação funciona sem internet.
11. Subir `python scripts/abrir_produto.py` e abrir `http://127.0.0.1:8766/index.html` no browser.

## Material

```text
<<<
[ANEXE OU COLE OS QUATRO ARQUIVOS DE outputs/ E OS NOVE DE outputs/gold/]
>>>
```

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- `produto/index.html`
- `produto/styles.css`
- `produto/app.js`
- `produto/sample-data.js`
- `produto/README.md`
- `outputs/05_notas_implementacao.md`

## Como abrir

```text
python scripts/abrir_produto.py
```

Endereço: `http://127.0.0.1:8766/index.html`
