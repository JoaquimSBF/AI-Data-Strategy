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
        ["cliente_id", "segmento", "status", "data_entrada"],
        [
            {"cliente_id": "CL01", "segmento": "Enterprise", "status": "ativo", "data_entrada": "2024-02-10"},
            {"cliente_id": "CL02", "segmento": "mid", "status": "Ativo", "data_entrada": "15/04/2024"},
            {"cliente_id": "CL03", "segmento": "SMB", "status": "ativo", "data_entrada": "2024/07/03"},
            {"cliente_id": "CL03", "segmento": "SMB", "status": "ativo", "data_entrada": "2024/07/03"},
            {"cliente_id": "CL04", "segmento": "enterprise", "status": "A", "data_entrada": "03-09-2024"},
            {"cliente_id": "CL05", "segmento": "smb", "status": "ativo", "data_entrada": "2025-01-20"},
            {"cliente_id": "CL06", "segmento": "Mid", "status": "ativo", "data_entrada": "2023-11-08"},
            {"cliente_id": "CL08", "segmento": "Enterprise", "status": "ativo", "data_entrada": "2024-06-01"},
            {"cliente_id": "CL99", "segmento": "TESTE", "status": "ativo", "data_entrada": ""},
        ],
    )
    write(
        "crm_deals.csv",
        ["deal_id", "cliente_id", "etapa", "status", "valor", "data_abertura", "data_fechamento", "atividades"],
        [
            {"deal_id": "D01", "cliente_id": "CL01", "etapa": "closedwon", "status": "ganho", "valor": "48000", "data_abertura": "2026-01-10", "data_fechamento": "2026-02-20", "atividades": "6"},
            {"deal_id": "D02", "cliente_id": "CL02", "etapa": "Closed Lost", "status": "Lost", "valor": "12000", "data_abertura": "12/01/2026", "data_fechamento": "2026/03/05", "atividades": "2"},
            {"deal_id": "D03", "cliente_id": "CL03", "etapa": "proposta", "status": "aberto", "valor": "18000", "data_abertura": "2026-03-01", "data_fechamento": "", "atividades": "9"},
            {"deal_id": "D04", "cliente_id": "CL04", "etapa": "negociacao", "status": "Open", "valor": "90000", "data_abertura": "18-02-2026", "data_fechamento": "", "atividades": "14"},
            {"deal_id": "D05", "cliente_id": "CL06", "etapa": "closedwon", "status": "ganho", "valor": "8000", "data_abertura": "2025-11-02", "data_fechamento": "2026-01-15", "atividades": "3"},
            {"deal_id": "D06", "cliente_id": "CL01", "etapa": "qualificacao", "status": "aberto", "valor": "15000", "data_abertura": "2026-05-02", "data_fechamento": "", "atividades": "4"},
            {"deal_id": "D06", "cliente_id": "CL01", "etapa": "qualificacao", "status": "aberto", "valor": "15000", "data_abertura": "2026-05-02", "data_fechamento": "", "atividades": "4"},
            {"deal_id": "D07", "cliente_id": "CL07", "etapa": "proposta", "status": "aberto", "valor": "22000", "data_abertura": "2026-04-10", "data_fechamento": "", "atividades": "1"},
            {"deal_id": "D99", "cliente_id": "CL99", "etapa": "teste", "status": "aberto", "valor": "-10", "data_abertura": "2026-06-01", "data_fechamento": "", "atividades": "0"},
        ],
    )
    write(
        "crm_atividades.csv",
        ["atividade_id", "cliente_id", "deal_id", "data", "tipo", "quantidade"],
        [
            {"atividade_id": "A01", "cliente_id": "CL01", "deal_id": "D01", "data": "2026-02-10", "tipo": "call", "quantidade": "3"},
            {"atividade_id": "A02", "cliente_id": "CL02", "deal_id": "D02", "data": "05/03/2026", "tipo": "email", "quantidade": "1"},
            {"atividade_id": "A03", "cliente_id": "CL03", "deal_id": "D03", "data": "2026/04/12", "tipo": "reuniao", "quantidade": "4"},
            {"atividade_id": "A04", "cliente_id": "CL04", "deal_id": "D04", "data": "22-04-2026", "tipo": "call", "quantidade": "8"},
            {"atividade_id": "A05", "cliente_id": "CL06", "deal_id": "D05", "data": "2026-01-08", "tipo": "email", "quantidade": "2"},
            {"atividade_id": "A06", "cliente_id": "CL04", "deal_id": "D04", "data": "", "tipo": "nota", "quantidade": "1"},
            {"atividade_id": "A99", "cliente_id": "CL99", "deal_id": "D99", "data": "2026-06-02", "tipo": "teste", "quantidade": "-2"},
        ],
    )
    write(
        "licencas.csv",
        ["cliente_id", "competencia", "licencas_contratadas", "licencas_alocadas", "mau"],
        [
            {"cliente_id": "CL01", "competencia": "2026-01", "licencas_contratadas": "100", "licencas_alocadas": "88", "mau": "81"},
            {"cliente_id": "CL01", "competencia": "2026-02", "licencas_contratadas": "100", "licencas_alocadas": "91", "mau": "84"},
            {"cliente_id": "CL01", "competencia": "2026-03", "licencas_contratadas": "120", "licencas_alocadas": "110", "mau": "97"},
            {"cliente_id": "CL01", "competencia": "2026-04", "licencas_contratadas": "120", "licencas_alocadas": "114", "mau": "101"},
            {"cliente_id": "CL01", "competencia": "2026-05", "licencas_contratadas": "120", "licencas_alocadas": "116", "mau": "104"},
            {"cliente_id": "CL01", "competencia": "2026-06", "licencas_contratadas": "120", "licencas_alocadas": "118", "mau": "108"},
            {"cliente_id": "CL02", "competencia": "2026-01", "licencas_contratadas": "80", "licencas_alocadas": "22", "mau": "18"},
            {"cliente_id": "CL02", "competencia": "2026-02", "licencas_contratadas": "80", "licencas_alocadas": "20", "mau": "15"},
            {"cliente_id": "CL02", "competencia": "2026-03", "licencas_contratadas": "80", "licencas_alocadas": "18", "mau": "12"},
            {"cliente_id": "CL02", "competencia": "2026-04", "licencas_contratadas": "60", "licencas_alocadas": "16", "mau": "11"},
            {"cliente_id": "CL02", "competencia": "2026-05", "licencas_contratadas": "60", "licencas_alocadas": "14", "mau": "9"},
            {"cliente_id": "CL02", "competencia": "2026-06", "licencas_contratadas": "60", "licencas_alocadas": "12", "mau": "8"},
            {"cliente_id": "CL03", "competencia": "2026-01", "licencas_contratadas": "40", "licencas_alocadas": "21", "mau": "19"},
            {"cliente_id": "CL03", "competencia": "2026-02", "licencas_contratadas": "40", "licencas_alocadas": "24", "mau": "22"},
            {"cliente_id": "CL03", "competencia": "2026-03", "licencas_contratadas": "40", "licencas_alocadas": "28", "mau": "25"},
            {"cliente_id": "CL03", "competencia": "2026-04", "licencas_contratadas": "40", "licencas_alocadas": "31", "mau": "29"},
            {"cliente_id": "CL03", "competencia": "2026-05", "licencas_contratadas": "50", "licencas_alocadas": "36", "mau": "33"},
            {"cliente_id": "CL03", "competencia": "2026-06", "licencas_contratadas": "50", "licencas_alocadas": "41", "mau": "38"},
            {"cliente_id": "CL04", "competencia": "2026-01", "licencas_contratadas": "200", "licencas_alocadas": "170", "mau": "160"},
            {"cliente_id": "CL04", "competencia": "2026-02", "licencas_contratadas": "200", "licencas_alocadas": "168", "mau": "150"},
            {"cliente_id": "CL04", "competencia": "2026-03", "licencas_contratadas": "200", "licencas_alocadas": "155", "mau": "132"},
            {"cliente_id": "CL04", "competencia": "2026-04", "licencas_contratadas": "200", "licencas_alocadas": "148", "mau": "121"},
            {"cliente_id": "CL04", "competencia": "2026-05", "licencas_contratadas": "200", "licencas_alocadas": "140", "mau": "110"},
            {"cliente_id": "CL04", "competencia": "2026-06", "licencas_contratadas": "200", "licencas_alocadas": "136", "mau": "98"},
            {"cliente_id": "CL05", "competencia": "2026-03", "licencas_contratadas": "25", "licencas_alocadas": "10", "mau": ""},
            {"cliente_id": "CL05", "competencia": "2026-04", "licencas_contratadas": "25", "licencas_alocadas": "11", "mau": "9"},
            {"cliente_id": "CL05", "competencia": "2026-05", "licencas_contratadas": "25", "licencas_alocadas": "12", "mau": "10"},
            {"cliente_id": "CL05", "competencia": "2026-06", "licencas_contratadas": "25", "licencas_alocadas": "12", "mau": "10"},
            {"cliente_id": "CL06", "competencia": "2026-01", "licencas_contratadas": "90", "licencas_alocadas": "70", "mau": "62"},
            {"cliente_id": "CL06", "competencia": "2026-02", "licencas_contratadas": "70", "licencas_alocadas": "48", "mau": "40"},
            {"cliente_id": "CL06", "competencia": "2026-03", "licencas_contratadas": "70", "licencas_alocadas": "44", "mau": "36"},
            {"cliente_id": "CL06", "competencia": "2026-04", "licencas_contratadas": "70", "licencas_alocadas": "41", "mau": "33"},
            {"cliente_id": "CL06", "competencia": "2026-05", "licencas_contratadas": "70", "licencas_alocadas": "39", "mau": "30"},
            {"cliente_id": "CL06", "competencia": "2026-06", "licencas_contratadas": "70", "licencas_alocadas": "38", "mau": "28"},
            {"cliente_id": "CL08", "competencia": "2026-04", "licencas_contratadas": "150", "licencas_alocadas": "90", "mau": "70"},
            {"cliente_id": "CL08", "competencia": "2026-05", "licencas_contratadas": "150", "licencas_alocadas": "95", "mau": "74"},
            {"cliente_id": "CL08", "competencia": "2026-06", "licencas_contratadas": "150", "licencas_alocadas": "99", "mau": "80"},
            {"cliente_id": "CL02", "competencia": "2026-13", "licencas_contratadas": "60", "licencas_alocadas": "200", "mau": "8"},
            {"cliente_id": "CL99", "competencia": "2026-06", "licencas_contratadas": "1", "licencas_alocadas": "1", "mau": "1"},
        ],
    )
    write(
        "eventos_contrato.csv",
        ["evento_id", "cliente_id", "data", "tipo", "licencas_antes", "licencas_depois"],
        [
            {"evento_id": "E01", "cliente_id": "CL01", "data": "2026-03-01", "tipo": "upgrade", "licencas_antes": "100", "licencas_depois": "120"},
            {"evento_id": "E02", "cliente_id": "CL02", "data": "01/04/2026", "tipo": "downsell", "licencas_antes": "80", "licencas_depois": "60"},
            {"evento_id": "E03", "cliente_id": "CL03", "data": "2026/05/01", "tipo": "upsell", "licencas_antes": "40", "licencas_depois": "50"},
            {"evento_id": "E04", "cliente_id": "CL06", "data": "2026-02-01", "tipo": "Downsell", "licencas_antes": "90", "licencas_depois": "70"},
            {"evento_id": "E05", "cliente_id": "CL04", "data": "", "tipo": "upgrade", "licencas_antes": "200", "licencas_depois": "220"},
            {"evento_id": "E99", "cliente_id": "CL99", "data": "2026-06-01", "tipo": "teste", "licencas_antes": "1", "licencas_depois": "1"},
        ],
    )
    write(
        "nps_export.csv",
        ["cliente_id", "competencia", "nps"],
        [
            {"cliente_id": "CL01", "competencia": "2026-01", "nps": "71"},
            {"cliente_id": "CL01", "competencia": "2026-03", "nps": "74"},
            {"cliente_id": "CL01", "competencia": "2026-06", "nps": "76"},
            {"cliente_id": "CL02", "competencia": "2026-01", "nps": "41"},
            {"cliente_id": "CL02", "competencia": "03/2026", "nps": "33"},
            {"cliente_id": "CL02", "competencia": "2026-06", "nps": "22"},
            {"cliente_id": "CL03", "competencia": "2026-02", "nps": "58"},
            {"cliente_id": "CL03", "competencia": "2026-05", "nps": "64"},
            {"cliente_id": "CL04", "competencia": "2026-01", "nps": "68"},
            {"cliente_id": "CL04", "competencia": "2026-04", "nps": "51"},
            {"cliente_id": "CL04", "competencia": "2026-06", "nps": "39"},
            {"cliente_id": "CL06", "competencia": "2026-02", "nps": "29"},
            {"cliente_id": "CL06", "competencia": "2026-06", "nps": "24"},
            {"cliente_id": "CL07", "competencia": "2026-06", "nps": "55"},
            {"cliente_id": "CL05", "competencia": "2026-06", "nps": "n/a"},
        ],
    )
    write(
        "metas.csv",
        ["kpi", "vigencia_inicio", "vigencia_fim", "meta", "direcao"],
        [
            {"kpi": "alocacao_pct", "vigencia_inicio": "2026-01", "vigencia_fim": "2026-06", "meta": "70", "direcao": "maior_melhor"},
            {"kpi": "nps", "vigencia_inicio": "2026-01", "vigencia_fim": "2026-06", "meta": "50", "direcao": "maior_melhor"},
            {"kpi": "mau", "vigencia_inicio": "2026-01", "vigencia_fim": "2026-06", "meta": "40", "direcao": "maior_melhor"},
            {"kpi": "churn_previsto_pct", "vigencia_inicio": "", "vigencia_fim": "", "meta": "5", "direcao": "menor_melhor"},
        ],
    )


if __name__ == "__main__":
    main()
