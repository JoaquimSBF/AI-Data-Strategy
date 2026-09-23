# ETAPA 04 — Contrato do produto

## O que vamos fazer

Definir como a Inteligência do Portal deve funcionar antes de escrever código.

## Conexão com o curso

- Discovery.
- Contrato de dados e contrato de produto.
- Separação entre requisito e implementação.
- Critérios de aceite.
- UX orientada a decisão.
- Redução de retrabalho antes da geração de código.

## GUIA DO ALUNO — NÃO COLAR ESTA PARTE

1. Continue no mesmo chat.
2. Copie somente o trecho entre `INÍCIO DO PROMPT` e `FIM DO PROMPT`.
3. Cole o prompt.
4. Anexe os arquivos listados abaixo.
5. Nesta etapa, não peça código nem HTML.

### Arquivos necessários

Da pasta `Portal Intelligence - Case 01/outputs/`:

1. `02_inteligencia.md`
2. `03_oportunidades.json`
3. `03_oportunidades.csv`
4. `03_backlog_explicado.md`

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

---

# INÍCIO DO PROMPT — COPIE A PARTIR DA PRÓXIMA LINHA

Execute a ETAPA 04 da Inteligência do Portal: elaborar o contrato funcional e não funcional do produto.

Não gere código nesta etapa. Use somente os artefatos listados no guia.

## Público

- liderança editorial;
- equipe de audiência;
- SEO;
- produto digital;
- dados.

## Jornada principal

```text
Importar dados
→ validar
→ observar desempenho
→ abrir evidência
→ criar ou revisar oportunidade
→ atribuir papel e status
→ registrar nota
→ exportar acompanhamento
```

## Módulos obrigatórios

### 1. Visão executiva

- KPIs por período.
- Comparação com meta vigente.
- séries mensais;
- principais altas e quedas;
- limitações visíveis.

### 2. Audiência e editorias

- mix por editoria;
- engajamento;
- drill-down por mês;
- fonte e fórmula acessíveis.

### 3. Busca

- impressões;
- cliques;
- CTR ponderado;
- posição ponderada;
- consultas e páginas.

### 4. Benchmark

- comparação separada de cada score;
- mesma data de coleta;
- sem score composto;
- concorrentes identificados como fictícios.

### 5. Visibilidade em IA

- quantidade de testes;
- share observado por domínio;
- filtro por tema, mecanismo e data;
- aviso de amostra limitada.

### 6. Backlog de oportunidades

- lista e kanban: `nova`, `em_analise`, `aprovada`, `em_execucao`, `concluida`, `descartada`;
- filtros por prioridade, confiança, tipo e responsável;
- edição de status, responsável, prazo e notas;
- evidências vinculadas;
- histórico local de alterações;
- criação manual sem permitir número sem fonte.

### 7. Importação e exportação

- carregar CSV/JSON local;
- validar cabeçalhos;
- mostrar erros sem travar toda a aplicação;
- restaurar dados de demonstração;
- exportar backlog em JSON e CSV;
- exportar resumo executivo em Markdown.

## Persistência

- Usar `localStorage` com versão do esquema.
- Não enviar dados para servidor.
- Disponibilizar botão de apagar dados locais.
- Não armazenar arquivos brutos após o processamento.

## Arquivos do produto

```text
produto/
  index.html
  styles.css
  app.js
  sample-data.js
  README.md
```

Sem CDN, bibliotecas externas, build ou instalação.

## Estados obrigatórios

- carregando;
- pronto;
- sem dados;
- arquivo inválido;
- dados parciais;
- sem evidência;
- erro recuperável.

## Acessibilidade

- navegação por teclado;
- foco visível;
- contraste adequado;
- tabelas com cabeçalhos;
- gráficos acompanhados de tabela ou texto;
- não depender apenas de cor;
- layout responsivo.

## Segurança

- renderizar texto com `textContent`, nunca concatenar dado em `innerHTML`;
- limitar tamanho de arquivo;
- rejeitar extensão inesperada;
- tratar conteúdo importado como dado não confiável;
- não executar links, scripts ou HTML importados;
- nenhuma PII no exemplo.

## Critérios de aceite do contrato

O contrato deve conter:

- mapa de telas;
- fluxos;
- esquema dos dados locais;
- regras de cálculo;
- estados de erro;
- permissões implícitas;
- critérios funcionais;
- critérios não funcionais;
- fora de escopo;
- definição de pronto.

## Material

```text
<<<
[ANEXE OU COLE OS QUATRO ARQUIVOS DE outputs/ E OS NOVE DE outputs/gold/]
>>>
```

# FIM DO PROMPT — COPIE ATÉ A LINHA ANTERIOR

---

## Onde salvar

- `outputs/04_contrato_produto.md`
