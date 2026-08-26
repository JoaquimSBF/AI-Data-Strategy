# Cases dos alunos — prompt a prompt até o produto

Igual à Allura na **jornada** (um prompt por vez, salvar o artefato). Diferente no **final**: não é board pack, é o produto de cada aluno.

Funciona em qualquer máquina: só Gemini/ChatGPT na web + um navegador. Sem instalar nada.

| Pasta | Aluno | Produto que sai no último prompt |
|-------|--------|----------------------------------|
| `CSOps Reunioes - Juliana Caballero/` | Juliana Caballero | Mesa CS (`produto/index.html`) |
| `Landing de Dados - Eduardo Campregher/` | Eduardo Campregher | Landing com i18n (`produto/index.html`) |
| `Risco de Churn - Sayuri Yamabe/` | Sayuri Yamabe | Radar de risco (`produto/index.html`) |
| `Orcado vs Realizado - Meliy Toda/` | Meliy Toda | Painel de desvio (`produto/index.html`) |

## Como usar (todo mundo igual)

1. Cole `prompts/md/00_mestre.md` (ou o PDF em `prompts/pdf/`) nas instruções do chat.
2. Cole o `01`, depois os CSVs de `dados/`. Salve onde o prompt manda (**ONDE SALVAR**).
3. Repita com `02`, `03`, `04` (o `04` gera o HTML).
4. `05` é o juiz do produto.
5. Abra o `produto/index.html` no navegador (mapa de botoes: `prompts/md/MAPA_FUNCIONALIDADE.md`).

Em cada case há **uma** pasta `prompts/` com duas pastas dentro:

- `prompts/md/` — fonte editável
- `prompts/pdf/` — para colar no Gemini (inclui `Prompts_Completo.pdf`, no mesmo estilo da Allura)

Mapa de arquivos, como funciona e **mapa de funcionabilidade do HTML** estão em `prompts/md/` e `prompts/pdf/`.

Guia dos quatro produtos: `Cases Alunos/COMO_FUNCIONA.pdf`.
