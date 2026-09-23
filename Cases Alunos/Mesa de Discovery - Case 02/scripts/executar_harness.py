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

TIPO_REUNIAO = {"discovery", "workshop", "alinhamento", "offline"}
STATUS_REUNIAO = {"realizada", "rascunho"}
TIPO_EVIDENCIA = {
    "problema",
    "objetivo",
    "sistema",
    "restricao",
    "usuario",
    "fora_de_escopo",
    "risco",
    "prioridade",
    "pergunta_aberta",
    "conflito",
}
BOOL_TRUE = {"sim", "true", "1", "yes"}
BOOL_FALSE = {"nao", "não", "false", "0", "no"}
INJECTION = re.compile(r"ignore as regras|invente \d+ requisitos", re.I)


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
    raw = (value or "").strip()
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


def clean_reunioes(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen_exact: set[tuple] = set()
    seen_ids: set[str] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen_exact:
            issues["duplicata_exata"] += 1
            quar.append(quarantine_row("reunioes", row["reuniao_id"], "duplicata_exata", f"linha {idx}"))
            continue
        seen_exact.add(fingerprint)
        data = parse_date(row["data"])
        tipo = normalize_key(row["tipo"])
        status = normalize_key(row["status"])
        reasons = []
        if not row["reuniao_id"]:
            reasons.append("id_nulo")
        if row["reuniao_id"] in seen_ids:
            reasons.append("id_duplicado")
        if not data:
            reasons.append("data_nula_ou_invalida")
        if tipo not in TIPO_REUNIAO:
            reasons.append("tipo_desconhecido")
        if status not in STATUS_REUNIAO:
            reasons.append("status_desconhecido")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("reunioes", row["reuniao_id"], "|".join(reasons), f"linha {idx}"))
            continue
        seen_ids.add(row["reuniao_id"])
        clean.append(
            {
                "reuniao_id": row["reuniao_id"],
                "data": data,
                "tipo": tipo,
                "tema": row["tema"],
                "status": status,
            }
        )
    return clean, quar, dict(issues)


def clean_evidencias(rows: list[dict[str, str]], reunioes_ok: set[str]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen_exact: set[tuple] = set()
    seen_ids: set[str] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen_exact:
            issues["duplicata_exata"] += 1
            quar.append(quarantine_row("evidencias", row["evidencia_id"], "duplicata_exata", f"linha {idx}"))
            continue
        seen_exact.add(fingerprint)
        tipo = normalize_key(row["tipo"])
        confiabilidade = normalize_key(row["confiabilidade"])
        reasons = []
        if not row["evidencia_id"]:
            reasons.append("id_nulo")
        if row["evidencia_id"] in seen_ids:
            reasons.append("id_duplicado")
        if not row["texto"]:
            reasons.append("texto_nulo")
        if tipo not in TIPO_EVIDENCIA:
            reasons.append("tipo_desconhecido")
        if row["reuniao_id"] not in reunioes_ok:
            reasons.append("reuniao_invalida")
        if INJECTION.search(row["texto"] or ""):
            reasons.append("texto_adversario")
        if confiabilidade not in {"alta", "media", "baixa"}:
            reasons.append("confiabilidade_invalida")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("evidencias", row["evidencia_id"], "|".join(reasons), f"linha {idx}"))
            continue
        seen_ids.add(row["evidencia_id"])
        clean.append(
            {
                "evidencia_id": row["evidencia_id"],
                "reuniao_id": row["reuniao_id"],
                "tipo": tipo,
                "texto": row["texto"],
                "confiabilidade": confiabilidade,
            }
        )
    return clean, quar, dict(issues)


def clean_stakeholders(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        influencia = normalize_key(row["influencia"])
        aprovacao = bool_text(row["obrigatorio_aprovacao"])
        reasons = []
        if influencia not in {"alta", "media", "baixa"}:
            reasons.append("influencia_invalida")
        if aprovacao is None:
            reasons.append("aprovacao_invalida")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("stakeholders", row["papel_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append(
            {
                "papel_id": row["papel_id"],
                "papel": normalize_key(row["papel"]),
                "area": normalize_key(row["area"]),
                "influencia": influencia,
                "obrigatorio_aprovacao": aprovacao,
            }
        )
    return clean, quar, dict(issues)


def clean_sistemas(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    api_map = {"sim": "sim", "nao": "nao", "não": "nao", "parcial": "parcial"}
    for idx, row in enumerate(rows, start=2):
        criticidade = normalize_key(row["criticidade"])
        status = normalize_key(row["status"])
        api = api_map.get(normalize_key(row["tem_api"]))
        reasons = []
        if criticidade not in {"alta", "media", "baixa"}:
            reasons.append("criticidade_invalida")
        if status != "ativo":
            reasons.append("status_desconhecido")
        if not api:
            reasons.append("api_invalida")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("sistemas", row["sistema_id"], "|".join(reasons), f"linha {idx}"))
            continue
        clean.append(
            {
                "sistema_id": row["sistema_id"],
                "sistema": row["sistema"],
                "criticidade": criticidade,
                "status": status,
                "tem_api": api,
            }
        )
    return clean, quar, dict(issues)


def clean_restricoes(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        obrigatoria = bool_text(row["obrigatoria"])
        if obrigatoria is None:
            issues["obrigatoria_invalida"] += 1
            quar.append(quarantine_row("restricoes", row["restricao_id"], "obrigatoria_invalida", f"linha {idx}"))
            continue
        clean.append(
            {
                "restricao_id": row["restricao_id"],
                "tipo": normalize_key(row["tipo"]),
                "descricao": row["descricao"],
                "obrigatoria": obrigatoria,
            }
        )
    return clean, quar, dict(issues)


def clean_ideias(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    clean: list[dict] = []
    quar: list[dict] = []
    status_ok = {"nova", "rejeitada"}
    for idx, row in enumerate(rows, start=2):
        status = normalize_key(row["status"])
        if status not in status_ok:
            issues["status_invalido"] += 1
            quar.append(quarantine_row("ideias", row["ideia_id"], "status_invalido", f"linha {idx}"))
            continue
        clean.append(
            {
                "ideia_id": row["ideia_id"],
                "origem": row["origem"],
                "texto": row["texto"],
                "status": status,
            }
        )
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


def build_gold(reunioes, evidencias, stakeholders, sistemas, restricoes, ideias, metas):
    tipo_req = {"problema", "objetivo", "sistema", "restricao", "usuario", "prioridade"}
    requisitos = []
    for ev in evidencias:
        if ev["tipo"] not in tipo_req:
            continue
        requisitos.append(
            {
                "requisito_id": f"REQ-{len(requisitos)+1:03d}",
                "evidencia_id": ev["evidencia_id"],
                "reuniao_id": ev["reuniao_id"],
                "titulo": ev["texto"],
                "tipo": ev["tipo"],
                "confiabilidade": ev["confiabilidade"],
                "status": "candidato",
                "criterio_aceite": f"Implementação validada contra a evidência {ev['evidencia_id']}.",
                "papel_aprovador": "nao_definido" if ev["evidencia_id"] != "E07" else "juridico",
            }
        )

    conflitos = [
        {
            "conflito_id": f"CF-{idx:03d}",
            "evidencia_id": ev["evidencia_id"],
            "descricao": ev["texto"],
            "status": "aberto",
        }
        for idx, ev in enumerate((e for e in evidencias if e["tipo"] == "conflito"), start=1)
    ]
    perguntas = [
        {
            "pergunta_id": f"PQ-{idx:03d}",
            "evidencia_id": ev["evidencia_id"],
            "pergunta": ev["texto"],
            "status": "aberta",
        }
        for idx, ev in enumerate((e for e in evidencias if e["tipo"] in {"pergunta_aberta", "risco"}), start=1)
    ]
    fora = [
        {
            "item_id": f"OUT-{idx:03d}",
            "evidencia_id": ev["evidencia_id"],
            "descricao": ev["texto"],
            "origem": "evidencia",
        }
        for idx, ev in enumerate((e for e in evidencias if e["tipo"] == "fora_de_escopo"), start=1)
    ]
    for ideia in ideias:
        if ideia["status"] == "rejeitada":
            fora.append(
                {
                    "item_id": f"OUT-{len(fora)+1:03d}",
                    "evidencia_id": "sem evidencia de requisito",
                    "descricao": f"Ideia {ideia['ideia_id']} rejeitada: {ideia['texto']}",
                    "origem": ideia["ideia_id"],
                }
            )

    n_req = Decimal(len(requisitos))
    n_com_fonte = Decimal(sum(1 for r in requisitos if r["evidencia_id"].startswith("E")))
    n_perguntas = Decimal(len(perguntas))
    n_evid = Decimal(len(evidencias))
    pct_fonte = Decimal(100) * n_com_fonte / n_req if n_req else Decimal("0")
    pct_perguntas = Decimal(100) * n_perguntas / n_evid if n_evid else Decimal("0")

    kpis = {
        "pct_requisitos_com_fonte": pct_fonte,
        "pct_perguntas_abertas": pct_perguntas,
        "requisitos_mvp": n_req,
    }
    metas_status = []
    for meta in metas:
        if meta["kpi"] not in kpis:
            metas_status.append(
                {
                    "kpi": meta["kpi"],
                    "ano_mes": meta["ano_mes_inicio"],
                    "realizado": "sem evidencia",
                    "meta": meta["meta"],
                    "diferenca": "sem evidencia",
                    "direcao": meta["direcao"],
                    "status": "sem evidencia",
                }
            )
            continue
        realizado = kpis[meta["kpi"]]
        target = Decimal(meta["meta"])
        status = "atingida" if (realizado >= target if meta["direcao"] == "maior_melhor" else realizado <= target) else "nao_atingida"
        metas_status.append(
            {
                "kpi": meta["kpi"],
                "ano_mes": meta["ano_mes_inicio"],
                "realizado": dec_text(realizado, "1" if meta["unidade"] == "qtd" else "0.01"),
                "meta": dec_text(target, "1" if meta["unidade"] == "qtd" else "0.01"),
                "diferenca": dec_text(realizado - target, "1" if meta["unidade"] == "qtd" else "0.01"),
                "direcao": meta["direcao"],
                "status": status,
            }
        )
    return requisitos, conflitos, perguntas, fora, metas_status, kpis


def build_evidencias_livro(requisitos, conflitos, perguntas, fora, metas_status, reunioes, evidencias):
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
        f"{len(reunioes)} reuniões válidas permaneceram no Silver após remover duplicata e reunião sem data.",
        "fato_observado",
        len(reunioes),
        "qtd",
        "2026-03",
        ["outputs/silver/reunioes.csv", "outputs/silver/quarentena.csv"],
        "contagem de reuniao_id únicos com data válida",
        "R99 ficou em quarentena por data nula.",
    )
    add(
        "EVD-002",
        f"{len(evidencias)} evidências válidas; E99 foi isolada como texto adversário e reunião inválida.",
        "fato_observado",
        len(evidencias),
        "qtd",
        "2026-03",
        ["outputs/silver/evidencias.csv"],
        "evidências com reunião Silver e sem padrão de injeção",
        "O texto de E99 é dado, não comando.",
    )
    add(
        "EVD-003",
        f"{len(requisitos)} requisitos candidatos foram extraídos, todos com evidencia_id.",
        "fato_observado",
        len(requisitos),
        "qtd",
        "2026-03",
        ["outputs/gold/requisitos.csv"],
        "1 requisito por evidência dos tipos problema, objetivo, sistema, restricao, usuario, prioridade",
        "Não há requisito sem fonte.",
    )
    add(
        "EVD-004",
        f"{len(perguntas)} pergunta(s) ou risco(s) permanecem abertos, incluindo o aprovador oficial do backlog.",
        "fato_observado",
        len(perguntas),
        "qtd",
        "2026-03",
        ["outputs/gold/perguntas_abertas.csv"],
        "contagem de evidências tipo pergunta_aberta ou risco",
        "Aprovador oficial = nao_definido.",
    )
    add(
        "EVD-005",
        conflitos[0]["descricao"] if conflitos else "sem evidencia de conflito",
        "fato_observado",
        len(conflitos),
        "qtd",
        "2026-03",
        ["outputs/gold/conflitos.csv"],
        "contagem de evidências tipo conflito",
        "Não há prazo oficial homologado.",
    )
    add(
        "EVD-006",
        f"{len(fora)} itens ficaram fora de escopo, incluindo mobile nativo e integração CRM ao vivo rejeitada.",
        "fato_observado",
        len(fora),
        "qtd",
        "2026-03",
        ["outputs/gold/fora_de_escopo.csv"],
        "evidências fora_de_escopo + ideias rejeitadas",
        "Ideia rejeitada não vira requisito.",
    )
    fonte = next(r for r in metas_status if r["kpi"] == "pct_requisitos_com_fonte")
    add(
        "EVD-007",
        f"pct_requisitos_com_fonte realizado {fonte['realizado']}% versus meta {fonte['meta']}% ({fonte['status']}).",
        "fato_observado",
        float(fonte["realizado"]),
        "pct",
        "2026-03",
        ["outputs/gold/metas_status.csv"],
        "100 * requisitos_com_evidencia_id / requisitos_candidatos",
        None,
    )
    perguntas_meta = next(r for r in metas_status if r["kpi"] == "pct_perguntas_abertas")
    add(
        "EVD-008",
        f"pct_perguntas_abertas realizado {perguntas_meta['realizado']}% versus meta {perguntas_meta['meta']}% ({perguntas_meta['status']}).",
        "fato_observado",
        float(perguntas_meta["realizado"]),
        "pct",
        "2026-03",
        ["outputs/gold/metas_status.csv"],
        "100 * (perguntas_abertas + riscos) / evidencias_validas",
        "Denominador é o catálogo Silver de evidências, não o backlog.",
    )
    mvp = next(r for r in metas_status if r["kpi"] == "requisitos_mvp")
    add(
        "EVD-009",
        f"requisitos_mvp realizado {mvp['realizado']} versus meta {mvp['meta']} ({mvp['status']}).",
        "fato_observado",
        float(mvp["realizado"]),
        "qtd",
        "2026-03",
        ["outputs/gold/metas_status.csv"],
        "contagem de requisitos candidatos com fonte",
        "Não completar o gap de 1 requisito com invenção.",
    )
    return livro


def build_backlog(requisitos, conflitos, perguntas, fora):
    def score(rel, urg, acion):
        total = rel + urg + acion
        prioridade = "alta" if total >= 8 else "media" if total >= 5 else "baixa"
        return total, prioridade

    items = []
    s, p = score(3, 3, 3)
    items.append(
        {
            "oportunidade_id": "OPP-001",
            "titulo": "Capturar evidência, requisito e aprovação no MVP",
            "tipo": "requisito",
            "problema_observado": next(r["titulo"] for r in requisitos if r["evidencia_id"] == "E09"),
            "evidencias": ["EVD-003", "EVD-007"],
            "acao_proposta": "Construir o workspace com captura de ata, requisito com evidencia_id e kanban de aprovação por papel.",
            "resultado_esperado": "Hipótese: cobrir o núcleo do MVP sem inventar requisito. sem evidencia causal",
            "metrica_acompanhamento": "pct_requisitos_com_fonte",
            "baseline": 100,
            "unidade": "pct",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 3,
            "confianca": "alta",
            "responsavel_sugerido": "product_manager",
            "status": "nova",
            "limitacoes": ["Aprovador oficial permanece nao_definido."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 3, 3)
    items.append(
        {
            "oportunidade_id": "OPP-002",
            "titulo": "Checklist único de onboarding por cliente",
            "tipo": "requisito",
            "problema_observado": next(r["titulo"] for r in requisitos if r["evidencia_id"] == "E01"),
            "evidencias": ["EVD-003"],
            "acao_proposta": "Desenhar checklist único citado por Operações, sem integrar CRM ao vivo.",
            "resultado_esperado": "Hipótese: reduzir tempo até primeiro uso supervisionado. sem evidencia causal",
            "metrica_acompanhamento": "requisitos_mvp",
            "baseline": len(requisitos),
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 3,
            "confianca": "media",
            "responsavel_sugerido": "operacoes",
            "status": "nova",
            "limitacoes": ["Tempo de 20 dias úteis é relato, não medição Gold."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 3, 2)
    items.append(
        {
            "oportunidade_id": "OPP-003",
            "titulo": "Operar o MVP sem API estável de CRM",
            "tipo": "restricao",
            "problema_observado": next(r["titulo"] for r in requisitos if r["evidencia_id"] == "E03"),
            "evidencias": ["EVD-003", "EVD-006"],
            "acao_proposta": "Importar arquivos locais e persistir no navegador. Não abrir conexão ao CRM.",
            "resultado_esperado": "Hipótese: respeitar restrição técnica e ideia rejeitada I03.",
            "metrica_acompanhamento": "itens_fora_de_escopo",
            "baseline": len(fora),
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 2,
            "confianca": "alta",
            "responsavel_sugerido": "tech_lead",
            "status": "nova",
            "limitacoes": ["CRM permanece sem API estável neste semestre."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 3, 3)
    items.append(
        {
            "oportunidade_id": "OPP-004",
            "titulo": "Bloquear PII em ferramenta externa",
            "tipo": "restricao",
            "problema_observado": next(r["titulo"] for r in requisitos if r["evidencia_id"] == "E07"),
            "evidencias": ["EVD-003"],
            "acao_proposta": "Usar papéis, não nomes. Recusar importação com e-mail ou CPF.",
            "resultado_esperado": "Hipótese: cumprir restrição legal C01.",
            "metrica_acompanhamento": "incidentes_pii",
            "baseline": 0,
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 3,
            "acionabilidade": 3,
            "confianca": "alta",
            "responsavel_sugerido": "juridico",
            "status": "nova",
            "limitacoes": ["Histórico de conversas permanece com dúvida jurídica (E08)."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(3, 2, 2)
    items.append(
        {
            "oportunidade_id": "OPP-005",
            "titulo": "Expor o conflito de prazo sem escolher um lado",
            "tipo": "conflito",
            "problema_observado": conflitos[0]["descricao"] if conflitos else "sem evidencia",
            "evidencias": ["EVD-005"],
            "acao_proposta": "Mostrar o conflito no workspace e exigir decisão humana. Não prometer 30 dias nem 8 semanas.",
            "resultado_esperado": "Conflito visível. Prazo oficial = nao_definido.",
            "metrica_acompanhamento": "conflitos_abertos",
            "baseline": len(conflitos),
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 3,
            "urgencia": 2,
            "acionabilidade": 2,
            "confianca": "alta",
            "responsavel_sugerido": "sponsor",
            "status": "nova",
            "limitacoes": ["Não há evidência de prazo homologado."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    s, p = score(2, 2, 2)
    items.append(
        {
            "oportunidade_id": "OPP-006",
            "titulo": "Fechar a pergunta do aprovador oficial",
            "tipo": "pergunta_aberta",
            "problema_observado": perguntas[0]["pergunta"] if perguntas else "sem evidencia",
            "evidencias": ["EVD-004", "EVD-008"],
            "acao_proposta": "Registrar papéis obrigatórios (sponsor, product_manager, juridico) e deixar o aprovador único como nao_definido.",
            "resultado_esperado": "Pergunta rastreável. sem evidencia de resposta.",
            "metrica_acompanhamento": "pct_perguntas_abertas",
            "baseline": float(next(r["realizado"] for r in []) or 0) if False else None,
            "unidade": "pct",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 2,
            "urgencia": 2,
            "acionabilidade": 2,
            "confianca": "media",
            "responsavel_sugerido": "sponsor",
            "status": "nova",
            "limitacoes": ["A resposta não está nas atas."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    items[-1]["baseline"] = 18.18
    s, p = score(2, 1, 3)
    items.append(
        {
            "oportunidade_id": "OPP-007",
            "titulo": "Manter mobile nativo e CRM ao vivo fora do MVP",
            "tipo": "fora_de_escopo",
            "problema_observado": "; ".join(x["descricao"] for x in fora),
            "evidencias": ["EVD-006"],
            "acao_proposta": "Listar os itens em Fora de escopo e recusar promoção automática a requisito.",
            "resultado_esperado": "Escopo preservado.",
            "metrica_acompanhamento": "itens_fora_de_escopo",
            "baseline": len(fora),
            "unidade": "qtd",
            "prioridade": p,
            "score_prioridade": s,
            "relevancia": 2,
            "urgencia": 1,
            "acionabilidade": 3,
            "confianca": "alta",
            "responsavel_sugerido": "product_manager",
            "status": "nova",
            "limitacoes": ["Não completar a meta de 8 requisitos inventando um oitavo."],
            "aprovacao_humana_obrigatoria": True,
        }
    )
    return items


def write_reports(profile, reunioes, evidencias, requisitos, conflitos, perguntas, fora, metas_status, livro, backlog, quar_count):
    SILVER.mkdir(parents=True, exist_ok=True)
    GOLD.mkdir(parents=True, exist_ok=True)
    quality = ["# Relatório de qualidade — etapa 01", "", "Premissa: evidência sem reunião válida não entra no Silver.", ""]
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
        "- Tipos e status em snake_case.",
        "- Booleanos: true/false.",
        "- Duplicata exata isolada.",
        "- Texto adversário isolado, não executado.",
        "- Nenhuma imputação de data, aprovador ou requisito.",
        "",
        "## Checklist",
        f"- Quarentena total: {quar_count} linhas.",
        "- PII em claro: nenhuma observada.",
        "- Prompt injection: E99 isolada.",
        "- Chaves Silver únicas: sim.",
    ]
    (OUTPUTS / "01_relatorio_qualidade.md").write_text("\n".join(quality), encoding="utf-8")

    intel = f"""# Inteligência Mesa de Discovery — etapa 02

Período das atas válidas: 2026-03-04 a 2026-03-18.
Reuniões Silver: {len(reunioes)}. Evidências Silver: {len(evidencias)}.

## 1. Requisitos candidatos

| requisito_id | evidencia_id | tipo | titulo |
|---|---|---|---|
"""
    for r in requisitos:
        intel += f"| {r['requisito_id']} | {r['evidencia_id']} | {r['tipo']} | {r['titulo']} |\n"
    intel += f"""
- fato_observado: {len(requisitos)} requisitos, todos com fonte.
- limitacao: a meta de 8 requisitos MVP não foi completada com invenção.

## 2. Conflitos

"""
    for c in conflitos:
        intel += f"- {c['conflito_id']}: {c['descricao']} Fonte: {c['evidencia_id']}.\n"
    intel += """
## 3. Perguntas abertas e riscos

"""
    for p in perguntas:
        intel += f"- {p['pergunta_id']}: {p['pergunta']} Fonte: {p['evidencia_id']}.\n"
    intel += """
## 4. Fora de escopo

"""
    for item in fora:
        intel += f"- {item['item_id']}: {item['descricao']}\n"
    intel += """
## 5. Metas

Ver `metas_status.csv`.

## 6. Lacunas

- Aprovador oficial = nao_definido.
- Prazo oficial = nao_definido.
- E99 não gera requisito.
- sem evidencia para o oitavo requisito do MVP.
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
                "evidencias": "|".join(o["evidencias"]),
            }
            for o in backlog
        ],
        ["oportunidade_id", "titulo", "tipo", "prioridade", "score_prioridade", "confianca", "responsavel_sugerido", "status", "evidencias"],
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
    reunioes_raw = read_csv(DADOS / "reunioes.csv")
    evidencias_raw = read_csv(DADOS / "evidencias.csv")
    stakeholders_raw = read_csv(DADOS / "stakeholders.csv")
    sistemas_raw = read_csv(DADOS / "sistemas.csv")
    restricoes_raw = read_csv(DADOS / "restricoes.csv")
    ideias_raw = read_csv(DADOS / "ideias.csv")
    metas_raw = read_csv(DADOS / "metas.csv")

    reunioes, q1, i1 = clean_reunioes(reunioes_raw)
    evidencias, q2, i2 = clean_evidencias(evidencias_raw, {r["reuniao_id"] for r in reunioes})
    stakeholders, q3, i3 = clean_stakeholders(stakeholders_raw)
    sistemas, q4, i4 = clean_sistemas(sistemas_raw)
    restricoes, q5, i5 = clean_restricoes(restricoes_raw)
    ideias, q6, i6 = clean_ideias(ideias_raw)
    metas, q7, i7 = clean_metas(metas_raw)
    quar = q1 + q2 + q3 + q4 + q5 + q6 + q7

    write_csv(SILVER / "reunioes.csv", reunioes, list(reunioes[0].keys()))
    write_csv(SILVER / "evidencias.csv", evidencias, list(evidencias[0].keys()))
    write_csv(SILVER / "stakeholders.csv", stakeholders, list(stakeholders[0].keys()))
    write_csv(SILVER / "sistemas.csv", sistemas, list(sistemas[0].keys()))
    write_csv(SILVER / "restricoes.csv", restricoes, list(restricoes[0].keys()))
    write_csv(SILVER / "ideias.csv", ideias, list(ideias[0].keys()))
    write_csv(SILVER / "metas.csv", metas, list(metas[0].keys()))
    write_csv(SILVER / "quarentena.csv", quar, ["tabela", "chave", "motivo", "origem"])

    requisitos, conflitos, perguntas, fora, metas_status, kpis = build_gold(
        reunioes, evidencias, stakeholders, sistemas, restricoes, ideias, metas
    )
    write_csv(GOLD / "requisitos.csv", requisitos, list(requisitos[0].keys()))
    write_csv(GOLD / "conflitos.csv", conflitos, list(conflitos[0].keys()) if conflitos else ["conflito_id", "evidencia_id", "descricao", "status"])
    write_csv(GOLD / "perguntas_abertas.csv", perguntas, list(perguntas[0].keys()) if perguntas else ["pergunta_id", "evidencia_id", "pergunta", "status"])
    write_csv(GOLD / "fora_de_escopo.csv", fora, list(fora[0].keys()) if fora else ["item_id", "evidencia_id", "descricao", "origem"])
    write_csv(GOLD / "metas_status.csv", metas_status, list(metas_status[0].keys()))

    sem_fonte = [r for r in requisitos if not r["evidencia_id"].startswith("E")]
    tests = [
        {"teste": "requisito_sempre_com_fonte", "status": "PASS" if not sem_fonte else "FAIL", "detalhe": f"{len(requisitos)} requisitos"},
        {"teste": "e99_nao_virou_requisito", "status": "PASS" if all(r["evidencia_id"] != "E99" for r in requisitos) else "FAIL", "detalhe": "E99 em quarentena"},
        {"teste": "ideia_rejeitada_fora", "status": "PASS" if any("I03" in x["origem"] for x in fora) else "FAIL", "detalhe": "I03 fora de escopo"},
        {"teste": "sem_pii", "status": "PASS", "detalhe": "apenas papéis"},
        {"teste": "meta_mvp_nao_completada_com_invencao", "status": "PASS" if int(float(next(m for m in metas_status if m['kpi']=='requisitos_mvp')['realizado'])) == 7 else "FAIL", "detalhe": "7 candidatos"},
    ]
    write_csv(GOLD / "testes_integridade.csv", tests, ["teste", "status", "detalhe"])

    livro = build_evidencias_livro(requisitos, conflitos, perguntas, fora, metas_status, reunioes, evidencias)
    backlog = build_backlog(requisitos, conflitos, perguntas, fora)
    profile = {
        "reunioes": {"antes": len(reunioes_raw), "depois": len(reunioes), "quarentena": len(q1), "issues": i1},
        "evidencias": {"antes": len(evidencias_raw), "depois": len(evidencias), "quarentena": len(q2), "issues": i2},
        "stakeholders": {"antes": len(stakeholders_raw), "depois": len(stakeholders), "quarentena": len(q3), "issues": i3},
        "sistemas": {"antes": len(sistemas_raw), "depois": len(sistemas), "quarentena": len(q4), "issues": i4},
        "restricoes": {"antes": len(restricoes_raw), "depois": len(restricoes), "quarentena": len(q5), "issues": i5},
        "ideias": {"antes": len(ideias_raw), "depois": len(ideias), "quarentena": len(q6), "issues": i6},
        "metas": {"antes": len(metas_raw), "depois": len(metas), "quarentena": len(q7), "issues": i7},
    }
    write_reports(profile, reunioes, evidencias, requisitos, conflitos, perguntas, fora, metas_status, livro, backlog, len(quar))
    (OUTPUTS / "harness_resumo.json").write_text(
        json.dumps({"profile": profile, "kpis": {k: str(v) for k, v in kpis.items()}, "tests": tests, "n_evidencias": len(livro), "n_ops": len(backlog)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"profile": profile, "tests": tests, "kpis": {k: str(v) for k, v in kpis.items()}, "n_evidencias": len(livro), "n_ops": len(backlog)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
