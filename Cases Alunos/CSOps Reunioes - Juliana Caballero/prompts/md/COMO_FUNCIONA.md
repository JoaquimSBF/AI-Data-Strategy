# Como funciona o produto — Mesa CS (Juliana Caballero)

## O que e

Uma **Mesa de Customer Success** em um unico HTML. O CS ve a reuniao, a transcricao (sem PII), o que precisa saber **antes** da call e as **acoes depois**.

Nao e o medalhao da Allura. Nao e board pack. Nao precisa instalar Python, Node nem MCP.

## Jornada (prompt a prompt)

1. **00 mestre** — personalidade do chat (CSOps, sem inventar, mascarar PII).
2. **01 limpar** — voce cola os CSVs de `dados/`; o modelo devolve CSVs prontos em `outputs/`.
3. **02 fichas** — o modelo vira cada reuniao em JSON (risco, temas, PRE, POS).
4. **03 contrato** — descreve a tela, sem gerar HTML ainda.
5. **04 produto** — gera `produto/index.html`. Voce abre no navegador.
6. **05 juiz** — PASS/FAIL contra o JSON.

O que colar em cada etapa e em qual pasta salvar: veja `prompts/md/MAPA_ARQUIVOS.md` (PDF em `prompts/pdf/`).

## Como o HTML trabalha

- Os dados da etapa 02 vao **dentro** do arquivo (por isso funciona offline, sem servidor).
- Badge ok/risco, lista clicavel, cards PRE e POS.
- PII nao pode aparecer: se o modelo deixar e-mail/CPF, o juiz da FAIL.

## O que codigo faria melhor (nao e obrigatorio)

Ler sozinho uma pasta cheia de Meet e mandar a ficha no Slack. Isso precisaria de programa instalado — fora deste curso.
