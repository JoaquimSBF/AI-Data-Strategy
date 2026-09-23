from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def write(name: str, fields: list[str], rows: list[dict]) -> None:
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write(
        "clientes.csv",
        ["cliente_id", "segmento", "status", "data_entrada", "data_saida"],
        [
            {"cliente_id": "CL01", "segmento": "Enterprise", "status": "ativo", "data_entrada": "2024-02-10", "data_saida": ""},
            {"cliente_id": "CL02", "segmento": "enterprise", "status": "Ativo", "data_entrada": "15/04/2024", "data_saida": ""},
            {"cliente_id": "CL03", "segmento": "Mid", "status": "ativo", "data_entrada": "2024/07/03", "data_saida": ""},
            {"cliente_id": "CL04", "segmento": "SMB", "status": "I", "data_entrada": "03-09-2024", "data_saida": ""},
            {"cliente_id": "CL05", "segmento": "smb", "status": "ativo", "data_entrada": "2025-01-20", "data_saida": ""},
            {"cliente_id": "CL06", "segmento": "Enterprise", "status": "inativo", "data_entrada": "2023-11-08", "data_saida": ""},
            {"cliente_id": "CL06", "segmento": "Enterprise", "status": "inativo", "data_entrada": "2023-11-08", "data_saida": ""},
            {"cliente_id": "CL99", "segmento": "TESTE", "status": "ativo", "data_entrada": "", "data_saida": ""},
        ],
    )
    write(
        "projetos.csv",
        ["projeto_id", "cliente_id", "fase", "prazo", "situacao", "atraso_dias"],
        [
            {"projeto_id": "PR01", "cliente_id": "CL01", "fase": "implantacao", "prazo": "2026-04-30", "situacao": "no_prazo", "atraso_dias": 0},
            {"projeto_id": "PR02", "cliente_id": "CL02", "fase": "Implantação", "prazo": "30/03/2026", "situacao": "atrasado", "atraso_dias": 21},
            {"projeto_id": "PR03", "cliente_id": "CL03", "fase": "operacao", "prazo": "2026/06/15", "situacao": "no_prazo", "atraso_dias": 0},
            {"projeto_id": "PR04", "cliente_id": "CL04", "fase": "encerramento", "prazo": "2026-02-28", "situacao": "Atrasado", "atraso_dias": 45},
            {"projeto_id": "PR05", "cliente_id": "CL05", "fase": "descoberta", "prazo": "15-05-2026", "situacao": "no_prazo", "atraso_dias": 0},
            {"projeto_id": "PR06", "cliente_id": "CL06", "fase": "operacao", "prazo": "2026-01-31", "situacao": "pausado", "atraso_dias": 12},
            {"projeto_id": "PR99", "cliente_id": "CL99", "fase": "teste", "prazo": "2026-06-01", "situacao": "no_prazo", "atraso_dias": -3},
        ],
    )
    write(
        "eventos.csv",
        ["evento_id", "cliente_id", "data", "tipo", "compareceu", "pendencias"],
        [
            {"evento_id": "EV01", "cliente_id": "CL01", "data": "2026-02-10", "tipo": "qbr", "compareceu": "sim", "pendencias": 1},
            {"evento_id": "EV02", "cliente_id": "CL02", "data": "12/02/2026", "tipo": "QBR", "compareceu": "nao", "pendencias": 4},
            {"evento_id": "EV03", "cliente_id": "CL02", "data": "2026/03/05", "tipo": "status", "compareceu": "Não", "pendencias": 5},
            {"evento_id": "EV04", "cliente_id": "CL03", "data": "2026-03-12", "tipo": "status", "compareceu": "SIM", "pendencias": 0},
            {"evento_id": "EV05", "cliente_id": "CL04", "data": "18-03-2026", "tipo": "qbr", "compareceu": "nao", "pendencias": 3},
            {"evento_id": "EV06", "cliente_id": "CL05", "data": "2026-03-20", "tipo": "kickoff", "compareceu": "sim", "pendencias": 1},
            {"evento_id": "EV07", "cliente_id": "CL06", "data": "2026-01-15", "tipo": "status", "compareceu": "nao", "pendencias": 6},
            {"evento_id": "EV08", "cliente_id": "CL01", "data": "2026-03-25", "tipo": "status", "compareceu": "sim", "pendencias": 0},
        ],
    )
    write(
        "tickets.csv",
        ["ticket_id", "cliente_id", "aberto_em", "severidade", "status", "sla_estourado"],
        [
            {"ticket_id": "T01", "cliente_id": "CL01", "aberto_em": "2026-03-01", "severidade": "baixa", "status": "fechado", "sla_estourado": "nao"},
            {"ticket_id": "T02", "cliente_id": "CL02", "aberto_em": "03/03/2026", "severidade": "alta", "status": "aberto", "sla_estourado": "SIM"},
            {"ticket_id": "T03", "cliente_id": "CL02", "aberto_em": "2026/03/10", "severidade": "critica", "status": "Aberto", "sla_estourado": "sim"},
            {"ticket_id": "T04", "cliente_id": "CL03", "aberto_em": "2026-02-20", "severidade": "media", "status": "fechado", "sla_estourado": "nao"},
            {"ticket_id": "T05", "cliente_id": "CL04", "aberto_em": "11-03-2026", "severidade": "alta", "status": "aberto", "sla_estourado": "sim"},
            {"ticket_id": "T06", "cliente_id": "CL06", "aberto_em": "2026-01-08", "severidade": "critica", "status": "aberto", "sla_estourado": "SIM"},
            {"ticket_id": "T99", "cliente_id": "CL05", "aberto_em": "2026-03-22", "severidade": "media", "status": "aberto", "sla_estourado": "n/a"},
        ],
    )
    write(
        "nps.csv",
        ["cliente_id", "data", "nps"],
        [
            {"cliente_id": "CL01", "data": "2026-02-10", "nps": 72},
            {"cliente_id": "CL02", "data": "12/02/2026", "nps": 28},
            {"cliente_id": "CL03", "data": "2026-03-12", "nps": 64},
            {"cliente_id": "CL04", "data": "2026-03-18", "nps": "n/a"},
            {"cliente_id": "CL06", "data": "2026-01-15", "nps": 15},
        ],
    )
    write(
        "metas.csv",
        ["kpi", "meta", "unidade", "direcao", "ano_mes_inicio", "ano_mes_fim"],
        [
            {"kpi": "clientes_com_sinal_alto", "meta": 2, "unidade": "qtd", "direcao": "menor_melhor", "ano_mes_inicio": "2026-01", "ano_mes_fim": "2026-03"},
            {"kpi": "tickets_sla_estourado", "meta": 2, "unidade": "qtd", "direcao": "menor_melhor", "ano_mes_inicio": "2026-01", "ano_mes_fim": "2026-03"},
            {"kpi": "churn_clientes_pct", "meta": 3, "unidade": "pct", "direcao": "menor_melhor", "ano_mes_inicio": "2026-01", "ano_mes_fim": "2026-03"},
        ],
    )
    print("Health Radar dados gerados")


if __name__ == "__main__":
    main()
