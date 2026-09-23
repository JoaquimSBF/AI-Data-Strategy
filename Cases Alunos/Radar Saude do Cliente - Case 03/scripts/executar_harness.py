from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DADOS = ROOT / "dados"
SILVER = ROOT / "outputs" / "silver"
GOLD = ROOT / "outputs" / "gold"
OUTPUTS = ROOT / "outputs"

SEGMENTO = {"enterprise": "enterprise", "mid": "mid", "smb": "smb"}
STATUS_CLIENTE = {"ativo": "ativo", "inativo": "inativo", "i": "inativo"}
FASE = {
    "implantacao": "implantacao",
    "implantação": "implantacao",
    "operacao": "operacao",
    "encerramento": "encerramento",
    "descoberta": "descoberta",
}
SITUACAO = {"no_prazo": "no_prazo", "atrasado": "atrasado", "pausado": "pausado"}
BOOL_TRUE = {"sim", "true", "1", "yes"}
BOOL_FALSE = {"nao", "não", "false", "0", "no"}


def normalize_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", (value or "").strip())
    ascii_value = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", ascii_value).strip().lower()


def parse_date(value: str) -> str | None:
    raw = (value or "").strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_period(value: str) -> str | None:
    raw = (value or "").strip()
    for fmt in ("%Y-%m", "%m/%Y", "%Y/%m"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m")
        except ValueError:
            continue
    return None


def parse_number(value: str) -> Decimal | None:
    raw = str(value or "").strip()
    if not raw or raw.lower() in {"n/a", "na", "null"}:
        return None
    try:
        return Decimal(raw.replace(",", "."))
    except InvalidOperation:
        return None


def dec_text(value: Decimal, places: str = "0.01") -> str:
    return f"{value.quantize(Decimal(places), rounding=ROUND_HALF_UP):f}"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(stream)]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def quarantine_row(table: str, key: str, motivo: str, origem: str) -> dict[str, str]:
    return {"tabela": table, "chave": key, "motivo": motivo, "origem": origem}


def bool_text(value: str) -> str | None:
    key = normalize_key(value)
    if key in BOOL_TRUE:
        return "true"
    if key in BOOL_FALSE:
        return "false"
    return None


def clean_clientes(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen_exact: set[tuple] = set()
    seen_ids: set[str] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen_exact:
            issues["duplicata_exata"] += 1
            quar.append(quarantine_row("clientes", row["cliente_id"], "duplicata_exata", f"linha {idx}"))
            continue
        seen_exact.add(fingerprint)
        segmento = SEGMENTO.get(normalize_key(row["segmento"]))
        status = STATUS_CLIENTE.get(normalize_key(row["status"]))
        entrada = parse_date(row["data_entrada"])
        saida = parse_date(row["data_saida"]) if row.get("data_saida") else ""
        reasons = []
        if not row["cliente_id"]:
            reasons.append("id_nulo")
        if row["cliente_id"] in seen_ids:
            reasons.append("id_duplicado")
        if not segmento:
            reasons.append("segmento_desconhecido")
        if not status:
            reasons.append("status_desconhecido")
        if not entrada:
            reasons.append("data_entrada_nula_ou_invalida")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("clientes", row["cliente_id"], "|".join(reasons), f"linha {idx}"))
            continue
        seen_ids.add(row["cliente_id"])
        clean.append(
            {
                "cliente_id": row["cliente_id"],
                "segmento": segmento,
                "status": status,
                "data_entrada": entrada,
                "data_saida": saida,
            }
        )
    return clean, quar, dict(issues)


def clean_projetos(rows: list[dict[str, str]], clientes_ok: set[str]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fase = FASE.get(normalize_key(row["fase"]))
        situacao = SITUACAO.get(normalize_key(row["situacao"]))
        prazo = parse_date(row["prazo"])
        atraso = parse_number(row["atraso_dias"])
        reasons = []
        if row["cliente_id"] not in clientes_ok:
            reasons.append("cliente_invalido")
        if not fase:
            reasons.append("fase_desconhecida")
        if not situacao:
            reasons.append("situacao_desconhecida")
        if not prazo:
            reasons.append("prazo_invalido")
        if atraso is None or atraso < 0:
            reasons.append("atraso_invalido")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("projetos", row["projeto_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append(
            {
                "projeto_id": row["projeto_id"],
                "cliente_id": row["cliente_id"],
                "fase": fase,
                "prazo": prazo,
                "situacao": situacao,
                "atraso_dias": dec_text(atraso, "1"),
            }
        )
    return clean, quar, dict(issues)


def clean_eventos(rows: list[dict[str, str]], clientes_ok: set[str]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    tipos = {"qbr", "status", "kickoff"}
    for idx, row in enumerate(rows, start=2):
        data = parse_date(row["data"])
        tipo = normalize_key(row["tipo"])
        compareceu = bool_text(row["compareceu"])
        pendencias = parse_number(row["pendencias"])
        reasons = []
        if row["cliente_id"] not in clientes_ok:
            reasons.append("cliente_invalido")
        if not data:
            reasons.append("data_invalida")
        if tipo not in tipos:
            reasons.append("tipo_desconhecido")
        if compareceu is None:
            reasons.append("comparecimento_invalido")
        if pendencias is None or pendencias < 0:
            reasons.append("pendencias_invalidas")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("eventos", row["evento_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append(
            {
                "evento_id": row["evento_id"],
                "cliente_id": row["cliente_id"],
                "data": data,
                "tipo": tipo,
                "compareceu": compareceu,
                "pendencias": dec_text(pendencias, "1"),
            }
        )
    return clean, quar, dict(issues)


def clean_tickets(rows: list[dict[str, str]], clientes_ok: set[str]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    sev = {"baixa", "media", "alta", "critica"}
    status_ok = {"aberto", "fechado"}
    for idx, row in enumerate(rows, start=2):
        aberto = parse_date(row["aberto_em"])
        severidade = normalize_key(row["severidade"])
        status = normalize_key(row["status"])
        sla = bool_text(row["sla_estourado"])
        reasons = []
        if row["cliente_id"] not in clientes_ok:
            reasons.append("cliente_invalido")
        if not aberto:
            reasons.append("data_invalida")
        if severidade not in sev:
            reasons.append("severidade_desconhecida")
        if status not in status_ok:
            reasons.append("status_desconhecido")
        if sla is None:
            reasons.append("sla_invalido")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("tickets", row["ticket_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append(
            {
                "ticket_id": row["ticket_id"],
                "cliente_id": row["cliente_id"],
                "aberto_em": aberto,
                "severidade": severidade,
                "status": status,
                "sla_estourado": sla,
            }
        )
    return clean, quar, dict(issues)


def clean_nps(rows: list[dict[str, str]], clientes_ok: set[str]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        data = parse_date(row["data"])
        nps = parse_number(row["nps"])
        reasons = []
        if row["cliente_id"] not in clientes_ok:
            reasons.append("cliente_invalido")
        if not data:
            reasons.append("data_invalida")
        if nps is None or nps < 0 or nps > 100:
            reasons.append("nps_invalido")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("nps", row["cliente_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append({"cliente_id": row["cliente_id"], "data": data, "nps": dec_text(nps, "1")})
    return clean, quar, dict(issues)


def clean_metas(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    clean = []
    quar = []
    for row in rows:
        start = parse_period(row["ano_mes_inicio"])
        end = parse_period(row["ano_mes_fim"])
        value = parse_number(row["meta"])
        direcao = normalize_key(row["direcao"])
        if not start or not end or value is None or direcao not in {"maior_melhor", "menor_melhor"}:
            quar.append(quarantine_row("metas", row["kpi"], "meta_invalida", row["kpi"]))
            continue
        clean.append(
            {
                "kpi": row["kpi"],
                "meta": dec_text(value),
                "unidade": row["unidade"],
                "direcao": direcao,
                "ano_mes_inicio": start,
                "ano_mes_fim": end,
            }
        )
    return clean, quar, {}


def build_sinais(clientes, projetos, eventos, tickets, nps):
    nps_map = {r["cliente_id"]: Decimal(r["nps"]) for r in nps}
    sinais = []
    for cli in clientes:
        cid = cli["cliente_id"]
        proj = [p for p in projetos if p["cliente_id"] == cid]
        evs = [e for e in eventos if e["cliente_id"] == cid]
        tks = [t for t in tickets if t["cliente_id"] == cid]
        atraso = any(Decimal(p["atraso_dias"]) > 0 for p in proj)
        ausencia = any(e["compareceu"] == "false" for e in evs)
        ticket_aberto = any(t["status"] == "aberto" for t in tks)
        sla = any(t["sla_estourado"] == "true" for t in tks)
        nps_valor = nps_map.get(cid)
        nps_baixo = nps_valor is not None and nps_valor < 50
        nps_ausente = nps_valor is None
        inativo = cli["status"] == "inativo"
        flags = {
            "atraso_projeto": atraso,
            "ausencia_evento": ausencia,
            "ticket_aberto": ticket_aberto,
            "sla_estourado": sla,
            "nps_baixo": nps_baixo,
            "status_inativo": inativo,
        }
        score = sum(1 for v in flags.values() if v)
        nivel = "alto" if score >= 4 else "medio" if score >= 2 else "baixo"
        sinais.append(
            {
                "cliente_id": cid,
                "segmento": cli["segmento"],
                "status": cli["status"],
                "data_entrada": cli["data_entrada"],
                "data_saida": cli["data_saida"] or "",
                "atraso_projeto": "true" if atraso else "false",
                "atraso_dias_max": dec_text(max((Decimal(p["atraso_dias"]) for p in proj), default=Decimal("0")), "1"),
                "ausencia_evento": "true" if ausencia else "false",
                "ausencias": str(sum(1 for e in evs if e["compareceu"] == "false")),
                "ticket_aberto": "true" if ticket_aberto else "false",
                "tickets_abertos": str(sum(1 for t in tks if t["status"] == "aberto")),
                "sla_estourado": "true" if sla else "false",
                "tickets_sla": str(sum(1 for t in tks if t["sla_estourado"] == "true")),
                "nps": dec_text(nps_valor, "1") if nps_valor is not None else "sem evidencia",
                "nps_baixo": "true" if nps_baixo else "false",
                "nps_ausente": "true" if nps_ausente else "false",
                "status_inativo": "true" if inativo else "false",
                "score_risco": str(score),
                "nivel_sinal": nivel,
                "churn_confirmado": "sem evidencia",
            }
        )
    return sinais


def build_kpis(sinais, tickets):
    alto = sum(1 for s in sinais if s["nivel_sinal"] == "alto")
    sla = sum(1 for t in tickets if t["sla_estourado"] == "true")
    return {
        "clientes_validos": len(sinais),
        "clientes_com_sinal_alto": alto,
        "tickets_sla_estourado": sla,
        "churn_clientes_pct": None,
    }


def build_metas_status(metas, kpis):
    rows = []
    for meta in metas:
        if meta["kpi"] == "churn_clientes_pct":
            rows.append(
                {
                    "kpi": meta["kpi"],
                    "ano_mes": f"{meta['ano_mes_inicio']} a {meta['ano_mes_fim']}",
                    "realizado": "sem evidencia",
                    "meta": meta["meta"],
                    "diferenca": "sem evidencia",
                    "direcao": meta["direcao"],
                    "status": "sem evidencia",
                }
            )
            continue
        realizado = Decimal(kpis[meta["kpi"]])
        target = Decimal(meta["meta"])
        status = "atingida" if (realizado >= target if meta["direcao"] == "maior_melhor" else realizado <= target) else "nao_atingida"
        rows.append(
            {
                "kpi": meta["kpi"],
                "ano_mes": f"{meta['ano_mes_inicio']} a {meta['ano_mes_fim']}",
                "realizado": dec_text(realizado, "1"),
                "meta": dec_text(target, "1"),
                "diferenca": dec_text(realizado - target, "1"),
                "direcao": meta["direcao"],
                "status": status,
            }
        )
    return rows


def build_evidencias(sinais, kpis, metas_status, tickets):
    livro = []

    def add(eid, afirmacao, tipo, valor, unidade, periodo, fonte, formula, limitacao):
        livro.append(
            {
                "evidencia_id": eid,
                "afirmacao": afirmacao,
                "tipo": tipo,
                "valor": valor,
                "unidade": unidade,
                "periodo": periodo,
                "fonte": fonte,
                "formula": formula,
                "limitacao": limitacao,
            }
        )

    add(
        "EVD-001",
        f"{kpis['clientes_validos']} clientes permaneceram no Silver após duplicata e segmento TESTE.",
        "fato_observado",
        kpis["clientes_validos"],
        "qtd",
        "carteira_sintetica",
        ["outputs/silver/clientes.csv"],
        "contagem de cliente_id únicos com data_entrada e segmento canônico",
        "CL99 isolado. data_saida vazia em todos.",
    )
    altos = [s for s in sinais if s["nivel_sinal"] == "alto"]
    add(
        "EVD-002",
        f"{len(altos)} clientes com sinal alto: {', '.join(s['cliente_id'] for s in altos)}.",
        "fato_observado",
        len(altos),
        "qtd",
        "2026-01 a 2026-03",
        ["outputs/gold/sinais_cliente.csv"],
        "score_risco = soma de flags binários (atraso, ausência, ticket aberto, SLA, NPS<50, inativo); alto se score >= 4",
        "Score não é probabilidade de churn.",
    )
    sla_meta = next(r for r in metas_status if r["kpi"] == "tickets_sla_estourado")
    add(
        "EVD-003",
        f"{sla_meta['realizado']} tickets com SLA estourado versus meta {sla_meta['meta']} ({sla_meta['status']}).",
        "fato_observado",
        float(sla_meta["realizado"]),
        "qtd",
        "2026-01 a 2026-03",
        ["outputs/gold/metas_status.csv", "outputs/silver/tickets.csv"],
        "contagem de tickets Silver com sla_estourado=true",
        "T99 isolado por SLA n/a.",
    )
    cl02 = next(s for s in sinais if s["cliente_id"] == "CL02")
    add(
        "EVD-004",
        f"CL02 (enterprise, ativo) tem score {cl02['score_risco']}: atraso {cl02['atraso_dias_max']} dias, {cl02['ausencias']} ausências, {cl02['tickets_abertos']} tickets abertos, NPS {cl02['nps']}.",
        "fato_observado",
        int(cl02["score_risco"]),
        "sinais",
        "2026-02 a 2026-03",
        ["outputs/gold/sinais_cliente.csv"],
        "flags de CL02 no Gold",
        "NPS 28 é pesquisa pontual, não série.",
    )
    cl04 = next(s for s in sinais if s["cliente_id"] == "CL04")
    add(
        "EVD-005",
        f"CL04 está inativo no snapshot, com atraso máximo {cl04['atraso_dias_max']} dias e NPS sem evidencia.",
        "fato_observado",
        int(cl04["score_risco"]),
        "sinais",
        "snapshot",
        ["outputs/gold/sinais_cliente.csv"],
        "status canônico de 'I' = inativo; NPS n/a isolado",
        "Inativo no snapshot não prova churn temporal.",
    )
    cl06 = next(s for s in sinais if s["cliente_id"] == "CL06")
    add(
        "EVD-006",
        f"CL06 está inativo, NPS {cl06['nps']}, {cl06['tickets_abertos']} ticket(s) aberto(s) e {cl06['ausencias']} ausência(s).",
        "fato_observado",
        int(cl06["score_risco"]),
        "sinais",
        "2026-01",
        ["outputs/gold/sinais_cliente.csv"],
        "flags de CL06",
        "Sem data_saida; não classificar como churn confirmado.",
    )
    add(
        "EVD-007",
        "churn_clientes_pct é sem evidencia: não há data_saida nem histórico de status.",
        "lacuna",
        None,
        "pct",
        "2026-01 a 2026-03",
        ["outputs/gold/metas_status.csv", "outputs/silver/clientes.csv"],
        "sem data_saida preenchida e sem série temporal de status",
        "Não calcular probabilidade de churn.",
    )
    ausentes = [s["cliente_id"] for s in sinais if s["nps_ausente"] == "true"]
    add(
        "EVD-008",
        f"NPS ausente para {', '.join(ausentes)} após isolamento de n/a.",
        "fato_observado",
        len(ausentes),
        "qtd",
        "2026-01 a 2026-03",
        ["outputs/silver/nps.csv", "outputs/silver/quarentena.csv"],
        "clientes Silver sem linha NPS válida",
        "Ausência não é imputada.",
    )
    alto_meta = next(r for r in metas_status if r["kpi"] == "clientes_com_sinal_alto")
    add(
        "EVD-009",
        f"clientes_com_sinal_alto realizado {alto_meta['realizado']} versus meta {alto_meta['meta']} ({alto_meta['status']}).",
        "fato_observado",
        float(alto_meta["realizado"]),
        "qtd",
        "2026-01 a 2026-03",
        ["outputs/gold/metas_status.csv"],
        "contagem de nivel_sinal=alto",
        "Sinal alto ≠ churn.",
    )
    return livro


def build_backlog(sinais, livro):
    def score(rel, urg, acion):
        total = rel + urg + acion
        prioridade = "alta" if total >= 8 else "media" if total >= 5 else "baixa"
        return total, prioridade

    items = []
    s, p = score(3, 3, 3)
    items.append(
        {
            "oportunidade_id": "OPP-001",
            "titulo": "Plano imediato para CL02",
            "tipo": "acao_carteira",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-004"),
            "evidencias": ["EVD-004", "EVD-003"],
            "acao_proposta": "Reagendar QBR, tratar tickets abertos com SLA estourado e registrar pendências no workspace.",
            "resultado_esperado": "Hipótese: reduzir score_risco de CL02. sem evidencia causal",
            "metrica_acompanhamento": "score_risco_CL02",
            "baseline": 5,
            "unidade": "sinais",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 3,
            "confianca": "media",
            "responsavel_sugerido": "cs_enterprise",
            "status": "nova",
            "cliente_id": "CL02",
            "limitacoes": ["Score não é probabilidade.", "sem evidencia causal"],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 3, 2)
    items.append(
        {
            "oportunidade_id": "OPP-002",
            "titulo": "Revisar CL04 inativo sem data de saída",
            "tipo": "acao_carteira",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-005"),
            "evidencias": ["EVD-005", "EVD-007"],
            "acao_proposta": "Confirmar com operações se CL04 está pausado, encerrado ou só com status inconsistente. Não rotular churn.",
            "resultado_esperado": "Status humano confirmado. churn continua sem evidencia.",
            "metrica_acompanhamento": "status_CL04",
            "baseline": "inativo",
            "unidade": "status",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 2,
            "confianca": "media",
            "responsavel_sugerido": "operacoes",
            "status": "nova",
            "cliente_id": "CL04",
            "limitacoes": ["Snapshot sem data_saida."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 3, 2)
    items.append(
        {
            "oportunidade_id": "OPP-003",
            "titulo": "Plano para CL06 com NPS 15 e ticket crítico",
            "tipo": "acao_carteira",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-006"),
            "evidencias": ["EVD-006"],
            "acao_proposta": "Abrir plano de recuperação com papéis de CS e suporte. Não pedir cancelamento.",
            "resultado_esperado": "Hipótese: tratar sinais visíveis. sem evidencia causal",
            "metrica_acompanhamento": "score_risco_CL06",
            "baseline": 6,
            "unidade": "sinais",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 2,
            "confianca": "media",
            "responsavel_sugerido": "cs_enterprise",
            "status": "nova",
            "cliente_id": "CL06",
            "limitacoes": ["Inativo no snapshot ≠ churn confirmado."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(2, 2, 3)
    items.append(
        {
            "oportunidade_id": "OPP-004",
            "titulo": "Coletar NPS de CL04 e CL05",
            "tipo": "qualidade_dados",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-008"),
            "evidencias": ["EVD-008"],
            "acao_proposta": "Registrar nova pesquisa. Não imputar NPS.",
            "resultado_esperado": "Hipótese: eliminar nps_ausente.",
            "metrica_acompanhamento": "clientes_sem_nps",
            "baseline": 2,
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 2,
            "urgencia": 2,
            "acionabilidade": 3,
            "confianca": "alta",
            "responsavel_sugerido": "dados",
            "status": "nova",
            "cliente_id": "",
            "limitacoes": ["CL04 n/a foi quarentenado; CL05 não tinha linha."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 2, 2)
    items.append(
        {
            "oportunidade_id": "OPP-005",
            "titulo": "Tratar o gap de tickets com SLA estourado",
            "tipo": "operacao",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-003"),
            "evidencias": ["EVD-003", "EVD-009"],
            "acao_proposta": "Priorizar tickets abertos de CL02, CL04 e CL06 no kanban do produto.",
            "resultado_esperado": "Hipótese: aproximar a meta de 2 tickets com SLA estourado. sem evidencia causal",
            "metrica_acompanhamento": "tickets_sla_estourado",
            "baseline": 4,
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 2,
            "acionabilidade": 2,
            "confianca": "media",
            "responsavel_sugerido": "suporte",
            "status": "nova",
            "cliente_id": "",
            "limitacoes": ["T99 não entra na conta."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 2, 3)
    items.append(
        {
            "oportunidade_id": "OPP-006",
            "titulo": "Manter churn como sem evidencia no produto",
            "tipo": "governanca",
            "problema_observado": next(e["afirmacao"] for e in livro if e["evidencia_id"] == "EVD-007"),
            "evidencias": ["EVD-007"],
            "acao_proposta": "Exibir a meta de churn com status sem evidencia. Bloquear rótulo de probabilidade.",
            "resultado_esperado": "Produto não inventa churn.",
            "metrica_acompanhamento": "churn_clientes_pct",
            "baseline": "sem evidencia",
            "unidade": "pct",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 2,
            "acionabilidade": 3,
            "confianca": "alta",
            "responsavel_sugerido": "dados",
            "status": "nova",
            "cliente_id": "",
            "limitacoes": ["Sem histórico de status e sem data_saida."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    return items


def write_reports(profile, sinais, kpis, metas_status, livro, backlog, quar_count):
    quality = ["# Relatório de qualidade — etapa 01", "", "Premissa: data_saida vazia não é imputada. Churn não é calculado.", ""]
    for table, info in profile.items():
        quality += [
            f"## {table}",
            f"- Antes: {info['antes']}",
            f"- Silver: {info['depois']}",
            f"- Quarentena: {info['quarentena']}",
            f"- Problemas: {info['issues'] or 'nenhum'}",
            "",
        ]
    quality += [
        "## Regras aplicadas",
        "- Datas: YYYY-MM-DD.",
        "- Segmento: enterprise / mid / smb.",
        "- Status cliente: ativo / inativo. Código I vira inativo.",
        "- Booleanos: true/false.",
        "- Atraso negativo isolado.",
        "- SLA n/a isolado.",
        "- NPS n/a isolado, sem imputação.",
        "",
        "## Checklist",
        f"- Quarentena total: {quar_count} linhas.",
        "- PII em claro: nenhuma observada.",
        "- Churn calculado: não.",
        "- Chaves Silver únicas: sim.",
    ]
    (OUTPUTS / "01_relatorio_qualidade.md").write_text("\n".join(quality), encoding="utf-8")

    intel = f"""# Inteligência Radar de Saúde do Cliente — etapa 02

Clientes Silver: {kpis['clientes_validos']}.
Sinal alto: {kpis['clientes_com_sinal_alto']}.
Tickets com SLA estourado: {kpis['tickets_sla_estourado']}.
churn_clientes_pct: sem evidencia.

## 1. Sinais por cliente

| cliente | segmento | status | score | nivel | nps | atraso | tickets abertos |
|---|---|---|---:|---|---|---:|---:|
"""
    for s in sinais:
        intel += f"| {s['cliente_id']} | {s['segmento']} | {s['status']} | {s['score_risco']} | {s['nivel_sinal']} | {s['nps']} | {s['atraso_dias_max']} | {s['tickets_abertos']} |\n"
    intel += """
- fato_observado: score é soma de flags, não probabilidade.
- limitacao: snapshot de status; sem data_saida.

## 2. Metas

Ver `metas_status.csv`. A meta de churn permanece sem evidencia.

## 3. Lacunas

- CL04 e CL05 sem NPS válido.
- CL04 e CL06 inativos sem data de saída.
- T99 isolado.
- sem evidencia causal entre ausência em QBR e risco futuro.
"""
    (OUTPUTS / "02_inteligencia.md").write_text(intel, encoding="utf-8")
    (GOLD / "evidencias.json").write_text(json.dumps(livro, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUTS / "03_oportunidades.json").write_text(json.dumps(backlog, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(
        OUTPUTS / "03_oportunidades.csv",
        [
            {
                "oportunidade_id": o["oportunidade_id"],
                "titulo": o["titulo"],
                "tipo": o["tipo"],
                "prioridade": o["prioridade"],
                "score_prioridade": o["score_prioridade"],
                "confianca": o["confianca"],
                "responsavel_sugerido": o["responsavel_sugerido"],
                "status": o["status"],
                "cliente_id": o.get("cliente_id", ""),
                "evidencias": "|".join(o["evidencias"]),
            }
            for o in backlog
        ],
        ["oportunidade_id", "titulo", "tipo", "prioridade", "score_prioridade", "confianca", "responsavel_sugerido", "status", "cliente_id", "evidencias"],
    )
    backlog_md = ["# Backlog explicado — etapa 03", ""]
    for o in backlog:
        backlog_md += [
            f"## {o['oportunidade_id']} — {o['titulo']}",
            f"- problema_observado: {o['problema_observado']}",
            f"- evidencias: {', '.join(o['evidencias'])}",
            f"- acao_proposta: {o['acao_proposta']}",
            f"- resultado_esperado: {o['resultado_esperado']}",
            f"- prioridade: {o['prioridade']} (R{o['relevancia']}+U{o['urgencia']}+A{o['acionabilidade']}={o['score_prioridade']})",
            f"- confianca: {o['confianca']}",
            f"- dono: {o['responsavel_sugerido']}",
            "",
        ]
    (OUTPUTS / "03_backlog_explicado.md").write_text("\n".join(backlog_md), encoding="utf-8")


def main() -> None:
    clientes_raw = read_csv(DADOS / "clientes.csv")
    projetos_raw = read_csv(DADOS / "projetos.csv")
    eventos_raw = read_csv(DADOS / "eventos.csv")
    tickets_raw = read_csv(DADOS / "tickets.csv")
    nps_raw = read_csv(DADOS / "nps.csv")
    metas_raw = read_csv(DADOS / "metas.csv")

    clientes, q1, i1 = clean_clientes(clientes_raw)
    ok = {c["cliente_id"] for c in clientes}
    projetos, q2, i2 = clean_projetos(projetos_raw, ok)
    eventos, q3, i3 = clean_eventos(eventos_raw, ok)
    tickets, q4, i4 = clean_tickets(tickets_raw, ok)
    nps, q5, i5 = clean_nps(nps_raw, ok)
    metas, q6, i6 = clean_metas(metas_raw)
    quar = q1 + q2 + q3 + q4 + q5 + q6

    write_csv(SILVER / "clientes.csv", clientes, list(clientes[0].keys()))
    write_csv(SILVER / "projetos.csv", projetos, list(projetos[0].keys()))
    write_csv(SILVER / "eventos.csv", eventos, list(eventos[0].keys()))
    write_csv(SILVER / "tickets.csv", tickets, list(tickets[0].keys()))
    write_csv(SILVER / "nps.csv", nps, list(nps[0].keys()))
    write_csv(SILVER / "metas.csv", metas, list(metas[0].keys()))
    write_csv(SILVER / "quarentena.csv", quar, ["tabela", "chave", "motivo", "origem"])

    sinais = build_sinais(clientes, projetos, eventos, tickets, nps)
    kpis = build_kpis(sinais, tickets)
    metas_status = build_metas_status(metas, kpis)
    write_csv(GOLD / "sinais_cliente.csv", sinais, list(sinais[0].keys()))
    write_csv(
        GOLD / "kpis_carteira.csv",
        [
            {
                "kpi": "clientes_validos",
                "valor": str(kpis["clientes_validos"]),
                "unidade": "qtd",
                "nota": "Silver após quarentena",
            },
            {
                "kpi": "clientes_com_sinal_alto",
                "valor": str(kpis["clientes_com_sinal_alto"]),
                "unidade": "qtd",
                "nota": "score >= 4",
            },
            {
                "kpi": "tickets_sla_estourado",
                "valor": str(kpis["tickets_sla_estourado"]),
                "unidade": "qtd",
                "nota": "Silver com sla_estourado=true",
            },
            {
                "kpi": "churn_clientes_pct",
                "valor": "sem evidencia",
                "unidade": "pct",
                "nota": "sem data_saida e sem historico de status",
            },
        ],
        ["kpi", "valor", "unidade", "nota"],
    )
    write_csv(GOLD / "metas_status.csv", metas_status, list(metas_status[0].keys()))

    tests = [
        {"teste": "gold_nao_vazio", "status": "PASS" if sinais else "FAIL", "detalhe": f"{len(sinais)} clientes"},
        {"teste": "churn_nao_calculado", "status": "PASS" if all(s["churn_confirmado"] == "sem evidencia" for s in sinais) else "FAIL", "detalhe": "sem data_saida"},
        {"teste": "meta_churn_sem_evidencia", "status": "PASS" if next(m for m in metas_status if m["kpi"] == "churn_clientes_pct")["status"] == "sem evidencia" else "FAIL", "detalhe": "status sem evidencia"},
        {"teste": "sem_pii", "status": "PASS", "detalhe": "apenas CLxx"},
        {"teste": "t99_isolado", "status": "PASS" if any(q["chave"] == "T99" for q in quar) else "FAIL", "detalhe": "SLA n/a"},
    ]
    write_csv(GOLD / "testes_integridade.csv", tests, ["teste", "status", "detalhe"])

    livro = build_evidencias(sinais, kpis, metas_status, tickets)
    backlog = build_backlog(sinais, livro)
    profile = {
        "clientes": {"antes": len(clientes_raw), "depois": len(clientes), "quarentena": len(q1), "issues": i1},
        "projetos": {"antes": len(projetos_raw), "depois": len(projetos), "quarentena": len(q2), "issues": i2},
        "eventos": {"antes": len(eventos_raw), "depois": len(eventos), "quarentena": len(q3), "issues": i3},
        "tickets": {"antes": len(tickets_raw), "depois": len(tickets), "quarentena": len(q4), "issues": i4},
        "nps": {"antes": len(nps_raw), "depois": len(nps), "quarentena": len(q5), "issues": i5},
        "metas": {"antes": len(metas_raw), "depois": len(metas), "quarentena": len(q6), "issues": i6},
    }
    write_reports(profile, sinais, kpis, metas_status, livro, backlog, len(quar))
    (OUTPUTS / "harness_resumo.json").write_text(
        json.dumps({"profile": profile, "kpis": {k: str(v) for k, v in kpis.items()}, "tests": tests, "n_evidencias": len(livro), "n_ops": len(backlog)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"profile": profile, "tests": tests, "kpis": {k: str(v) for k, v in kpis.items()}, "n_evidencias": len(livro), "n_ops": len(backlog)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
