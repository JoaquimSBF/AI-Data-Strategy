# ETAPA 01 — Ler e limpar (dados crus -> prontos)

## COMO USAR ESTA ETAPA

Pasta do case: `Cases Alunos/CSOps Reunioes - Juliana Caballero/`

1. No **mesmo chat** do `00_mestre.md`, cole **este arquivo inteiro**.
2. Abra os arquivos abaixo, copie o conteudo e cole no bloco `<<< >>>`:

| Arquivo | Pasta |
|---------|--------|
| `clientes.csv` | `dados/` |
| `reunioes.csv` | `dados/` |
| `transcricoes.csv` | `dados/` |
| `metas.csv` | `dados/` |
| opcional: `R001_moema.txt`, `R003_centro.txt`, `R006_santana.txt` | `dados/transcricoes/` |

3. Copie a resposta do modelo e grave nos caminhos de **ONDE SALVAR**. O chat nao cria pasta sozinho.

Contexto: Vitrine Mais / Mesa CS (Juliana Caballero).

Tarefa:
1) Liste problemas de qualidade por arquivo (duplicata, data misturada, NPS em texto, transcricao vazia, PII no texto).
2) Regras de limpeza reproduziveis.
3) Padronize: data YYYY-MM-DD, nps 0-10 ou nulo, status_call ok|risco|indefinido, canal Google Meet.
4) Mascare PII nas transcricoes ([EMAIL], [TEL], [CPF], [CONTATO]). Nao mostre o valor original depois.
5) Descarte duplicata de reuniao_id e transcricao vazia. Diga o criterio.
6) Entregue CSV limpo de cada tabela + checklist OK/NOK.
7) Nao invente ficha de CS ainda. So dado pronto.

Formato:
- Resumo (5 linhas)
- Por tabela: problemas | regras | linhas antes/depois
- Blocos CSV nomeados
- Status: OK ou NOK

Dados:
<<<
[COLE aqui o conteudo dos arquivos da tabela acima]
>>>

## ONDE SALVAR
Crie a pasta `outputs/` se ainda nao existir. Salve:

- `outputs/01_limpeza.md` — relatorio desta etapa
- `outputs/clientes.csv`
- `outputs/reunioes.csv`
- `outputs/transcricoes.csv`
- `outputs/metas.csv`
- `outputs/linhas_invalidas.csv` — se houver descarte
