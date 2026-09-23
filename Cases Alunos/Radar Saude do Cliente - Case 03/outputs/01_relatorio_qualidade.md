# Relatório de qualidade — etapa 01

Premissa: data_saida vazia não é imputada. Churn não é calculado.

## clientes
- Antes: 8
- Silver: 6
- Quarentena: 2
- Problemas: {'duplicata_exata': 1, 'segmento_desconhecido': 1, 'data_entrada_nula_ou_invalida': 1}

## projetos
- Antes: 7
- Silver: 6
- Quarentena: 1
- Problemas: {'cliente_invalido': 1, 'fase_desconhecida': 1, 'atraso_invalido': 1}

## eventos
- Antes: 8
- Silver: 8
- Quarentena: 0
- Problemas: nenhum

## tickets
- Antes: 7
- Silver: 6
- Quarentena: 1
- Problemas: {'sla_invalido': 1}

## nps
- Antes: 5
- Silver: 4
- Quarentena: 1
- Problemas: {'nps_invalido': 1}

## metas
- Antes: 3
- Silver: 3
- Quarentena: 0
- Problemas: nenhum

## Regras aplicadas
- Datas: YYYY-MM-DD.
- Segmento: enterprise / mid / smb.
- Status cliente: ativo / inativo. Código I vira inativo.
- Booleanos: true/false.
- Atraso negativo isolado.
- SLA n/a isolado.
- NPS n/a isolado, sem imputação.

## Checklist
- Quarentena total: 5 linhas.
- PII em claro: nenhuma observada.
- Churn calculado: não.
- Chaves Silver únicas: sim.