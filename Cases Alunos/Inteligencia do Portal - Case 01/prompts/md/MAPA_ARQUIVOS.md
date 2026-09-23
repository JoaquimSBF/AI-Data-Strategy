# Mapa de arquivos — Inteligência do Portal

Pasta raiz:

`Cases Alunos/Portal Intelligence - Case 01/`

## Fluxo

| Etapa | Prompt | Entrada | Saída principal |
|---|---|---|---|
| 00 | `00_mestre.md` | nenhuma | contexto permanente |
| 01 | `01_limpar.md` | seis CSVs de `dados/` | `outputs/silver/` |
| 02 | `02_inteligencia.md` | Silver + dicionário | `outputs/gold/` e `evidencias.json` |
| 03 | `03_oportunidades.md` | inteligência + Gold | backlog JSON/CSV |
| 04 | `04_contrato_produto.md` | evidências + backlog | contrato funcional |
| 05 | `05_construir_produto.md` | contrato + dados derivados | aplicação em `produto/` e abertura em `http://127.0.0.1:8766/index.html` |
| 06 | `06_testar_red_team.md` | produto + contratos | testes e defeitos |
| 07 | `07_juiz.md` | todos os artefatos | avaliação final |

## Como ler cada PDF

Cada PDF de prompt possui três partes:

1. `GUIA DO ALUNO — NÃO COLAR`: explica a etapa e lista os arquivos com pasta e nome.
2. `INÍCIO DO PROMPT`: comece a copiar na linha seguinte.
3. `FIM DO PROMPT`: pare de copiar na linha anterior.

Depois de colar o prompt, anexe os arquivos na ordem indicada no próprio PDF. Se o chat não aceitar anexos, cole o conteúdo precedido pelo caminho completo do arquivo.

Não copie o guia, o mapa nem a seção `Onde salvar` para o chat.

## Árvore esperada

```text
Portal Intelligence - Case 01/
├── README.md
├── dados/
│   ├── README_DADOS.md
│   ├── gerar_dados_sinteticos.py
│   ├── audiencia_portal.csv
│   ├── conteudos.csv
│   ├── search_console.csv
│   ├── auditoria_sites.csv
│   ├── visibilidade_ia.csv
│   └── metas.csv
├── prompts/
│   └── md/
│       ├── 00_mestre.md
│       ├── 01_limpar.md
│       ├── 02_inteligencia.md
│       ├── 03_oportunidades.md
│       ├── 04_contrato_produto.md
│       ├── 05_construir_produto.md
│       ├── 06_testar_red_team.md
│       ├── 07_juiz.md
│       ├── COMO_FUNCIONA.md
│       ├── MAPA_ARQUIVOS.md
│       └── MAPA_FUNCIONALIDADE.md
├── outputs/
│   ├── silver/
│   └── gold/
└── produto/
    ├── index.html
    ├── styles.css
    ├── app.js
    ├── sample-data.js
    └── README.md
```

## Regra prática

Sempre use a saída da etapa anterior. Não pule diretamente dos CSVs brutos para o produto.

O chat não salva automaticamente os arquivos quando usado na web. Copie cada saída para o caminho indicado no prompt.
