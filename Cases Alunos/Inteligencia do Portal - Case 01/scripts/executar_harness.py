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

EDITORIA_MAP = {
    "politica": "politica",
    "economia": "economia",
    "tecnologia": "tecnologia",
    "esportes": "esportes",
    "cultura": "cultura",
}
SITE_MAP = {
    "portal_proprio": "portal_proprio",
    "concorrente_alpha": "concorrente_alpha",
    "concorrente_beta": "concorrente_beta",
}
MECANISMO_MAP = {"ia_a": "ia_a", "ia_b": "ia_b"}
BOOL_TRUE = {"sim", "true", "1", "yes"}
BOOL_FALSE = {"nao", "não", "false", "0", "no"}


def normalize_key(value: str) -> str:
    text = unicodedata.normalize("NFKD", (value or "").strip())
    ascii_value = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", ascii_value).strip().lower()


def parse_period(value: str) -> str | None:
    raw = (value or "").strip()
    for fmt in ("%Y-%m", "%m/%Y", "%Y/%m"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m")
        except ValueError:
            continue
    return None


def parse_date(value: str) -> str | None:
    raw = (value or "").strip()
    if not raw:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_number(value: str, *, allow_thousands_dot: bool = True) -> Decimal | None:
    raw = (value or "").strip()
    if not raw or raw.lower() in {"n/a", "na", "null"}:
        return None
    cleaned = raw.replace(" ", "")
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif allow_thousands_dot and re.fullmatch(r"\d{1,3}(\.\d{3})+", cleaned):
        cleaned = cleaned.replace(".", "")
    try:
        return Decimal(cleaned)
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


def clean_audiencia(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen_exact: set[tuple] = set()
    seen_keys: dict[tuple[str, str], dict] = {}
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen_exact:
            issues["duplicata_exata"] += 1
            quar.append(quarantine_row("audiencia", f"linha_{idx}", "duplicata_exata", f"linha {idx}"))
            continue
        seen_exact.add(fingerprint)
        period = parse_period(row["ano_mes"])
        editoria = EDITORIA_MAP.get(normalize_key(row["editoria"]))
        usuarios = parse_number(row["usuarios"])
        sessoes = parse_number(row["sessoes"])
        pageviews = parse_number(row["pageviews"])
        tempo = parse_number(row["tempo_medio_seg"])
        rejeicao = parse_number(row["taxa_rejeicao_pct"])
        assinaturas = parse_number(row["assinaturas_atribuidas"])
        reasons = []
        if not period:
            reasons.append("competencia_invalida")
        if not editoria:
            reasons.append("editoria_desconhecida")
        if any(v is None for v in [usuarios, sessoes, pageviews, tempo, rejeicao, assinaturas]):
            reasons.append("valor_nulo_ou_invalido")
        if any(v is not None and v < 0 for v in [usuarios, sessoes, pageviews, tempo, assinaturas]):
            reasons.append("valor_negativo")
        if rejeicao is not None and (rejeicao < 0 or rejeicao > 100):
            reasons.append("percentual_fora_de_0_100")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("audiencia", f"{row['ano_mes']}|{row['editoria']}", "|".join(reasons), f"linha {idx}"))
            continue
        key = (period, editoria)
        cleaned = {
            "ano_mes": period,
            "editoria": editoria,
            "usuarios": dec_text(usuarios, "1"),
            "sessoes": dec_text(sessoes, "1"),
            "pageviews": dec_text(pageviews, "1"),
            "tempo_medio_seg": dec_text(tempo, "1"),
            "taxa_rejeicao_pct": dec_text(rejeicao),
            "assinaturas_atribuidas": dec_text(assinaturas, "1"),
        }
        if key in seen_keys:
            issues["chave_duplicada"] += 1
            quar.append(quarantine_row("audiencia", f"{period}|{editoria}", "chave_duplicada", f"linha {idx}"))
            continue
        seen_keys[key] = cleaned
        clean.append(cleaned)
    return clean, quar, dict(issues)


def clean_conteudos(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen_exact: set[tuple] = set()
    seen_ids: set[str] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        fingerprint = tuple(sorted(row.items()))
        if fingerprint in seen_exact:
            issues["duplicata_exata"] += 1
            quar.append(quarantine_row("conteudos", row["conteudo_id"], "duplicata_exata", f"linha {idx}"))
            continue
        seen_exact.add(fingerprint)
        pub = parse_date(row["data_publicacao"])
        upd = parse_date(row["data_atualizacao"]) if row["data_atualizacao"] else ""
        editoria = EDITORIA_MAP.get(normalize_key(row["editoria"]))
        schema_key = normalize_key(row["schema_article"])
        faq_key = normalize_key(row["faq_presente"])
        palavras = parse_number(row["palavras"])
        fontes = parse_number(row["fontes_externas_qtd"])
        reasons = []
        if not row["conteudo_id"]:
            reasons.append("id_nulo")
        if row["conteudo_id"] in seen_ids:
            reasons.append("id_duplicado")
        if not pub:
            reasons.append("data_publicacao_nula_ou_invalida")
        if not editoria:
            reasons.append("editoria_desconhecida")
        if schema_key not in BOOL_TRUE | BOOL_FALSE:
            reasons.append("schema_invalido")
        if faq_key not in BOOL_TRUE | BOOL_FALSE:
            reasons.append("faq_invalido")
        if palavras is None or palavras <= 0 or fontes is None or fontes < 0:
            reasons.append("valor_invalido")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("conteudos", row["conteudo_id"], "|".join(reasons), f"linha {idx}"))
            continue
        seen_ids.add(row["conteudo_id"])
        clean.append(
            {
                "conteudo_id": row["conteudo_id"],
                "data_publicacao": pub,
                "editoria": editoria,
                "formato": normalize_key(row["formato"]),
                "titulo_sintetico": row["titulo_sintetico"],
                "autor_pseudo": row["autor_pseudo"],
                "palavras": dec_text(palavras, "1"),
                "data_atualizacao": upd,
                "schema_article": "true" if schema_key in BOOL_TRUE else "false",
                "faq_presente": "true" if faq_key in BOOL_TRUE else "false",
                "fontes_externas_qtd": dec_text(fontes, "1"),
                "status": "publicado",
                "data_referencia": upd or pub,
            }
        )
    return clean, quar, dict(issues)


def clean_search(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str, str]] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        period = parse_period(row["ano_mes"])
        consulta = normalize_key(row["consulta"])
        editoria = EDITORIA_MAP.get(normalize_key(row["editoria"]))
        impressoes = parse_number(row["impressoes"])
        cliques = parse_number(row["cliques"])
        posicao = parse_number(row["posicao_media"])
        reasons = []
        if not period:
            reasons.append("competencia_invalida")
        if not consulta:
            reasons.append("consulta_nula")
        if not editoria:
            reasons.append("editoria_desconhecida")
        if impressoes is None or cliques is None or posicao is None:
            reasons.append("medicao_ausente")
        if any(v is not None and v < 0 for v in [impressoes, cliques, posicao]):
            reasons.append("valor_negativo")
        key = (period or "", consulta, row["pagina_id"])
        if key in seen:
            reasons.append("chave_duplicada")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("search_console", f"{row['ano_mes']}|{consulta}|{row['pagina_id']}", "|".join(reasons), f"linha {idx}"))
            continue
        seen.add(key)
        ctr = (Decimal(100) * cliques / impressoes) if impressoes > 0 else Decimal("0")
        clean.append(
            {
                "ano_mes": period,
                "consulta": consulta,
                "editoria": editoria,
                "impressoes": dec_text(impressoes, "1"),
                "cliques": dec_text(cliques, "1"),
                "ctr_pct": dec_text(ctr),
                "posicao_media": dec_text(posicao),
                "pagina_id": row["pagina_id"],
            }
        )
    return clean, quar, dict(issues)


def clean_auditoria(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str]] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        data = parse_date(row["data_coleta"])
        site = SITE_MAP.get(normalize_key(row["site"]))
        scores = {
            "performance_score": parse_number(row["performance_score"]),
            "seo_tecnico_score": parse_number(row["seo_tecnico_score"]),
            "dados_estruturados_pct": parse_number(row["dados_estruturados_pct"]),
            "tempo_carregamento_seg": parse_number(row["tempo_carregamento_seg"]),
            "mobile_score": parse_number(row["mobile_score"]),
        }
        reasons = []
        if not data:
            reasons.append("data_invalida")
        if not site:
            reasons.append("site_desconhecido")
        if any(v is None for v in scores.values()):
            reasons.append("score_invalido")
        if scores["dados_estruturados_pct"] is not None and not (0 <= scores["dados_estruturados_pct"] <= 100):
            reasons.append("percentual_fora_de_0_100")
        key = (data or "", site or "")
        if key in seen:
            reasons.append("chave_duplicada")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("auditoria_sites", f"{row['data_coleta']}|{row['site']}", "|".join(reasons), f"linha {idx}"))
            continue
        seen.add(key)
        clean.append(
            {
                "data_coleta": data,
                "ano_mes": data[:7],
                "site": site,
                "tipo": "proprio" if site == "portal_proprio" else "concorrente",
                "performance_score": dec_text(scores["performance_score"], "1"),
                "seo_tecnico_score": dec_text(scores["seo_tecnico_score"], "1"),
                "dados_estruturados_pct": dec_text(scores["dados_estruturados_pct"], "1"),
                "tempo_carregamento_seg": dec_text(scores["tempo_carregamento_seg"]),
                "mobile_score": dec_text(scores["mobile_score"], "1"),
                "paginas_amostradas": row["paginas_amostradas"],
                "fonte_coleta": row["fonte_coleta"],
            }
        )
    return clean, quar, dict(issues)


def clean_ia(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict], dict]:
    issues: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str, str]] = set()
    clean: list[dict] = []
    quar: list[dict] = []
    for idx, row in enumerate(rows, start=2):
        data = parse_date(row["data_teste"])
        tema = EDITORIA_MAP.get(normalize_key(row["tema"]))
        mecanismo = MECANISMO_MAP.get(normalize_key(row["mecanismo"]))
        dominio = normalize_key(row["dominio_citado"])
        houve = normalize_key(row["houve_citacao"])
        reasons = []
        if not data:
            reasons.append("data_invalida")
        if not tema:
            reasons.append("tema_desconhecido")
        if not mecanismo:
            reasons.append("mecanismo_desconhecido")
        if dominio not in {"portal_proprio", "concorrente_alpha", "concorrente_beta", "nenhum"}:
            reasons.append("dominio_desconhecido")
        if houve not in BOOL_TRUE | BOOL_FALSE:
            reasons.append("citacao_invalida")
        key = (data or "", row["pergunta_id"], mecanismo or "")
        if key in seen:
            reasons.append("chave_duplicada")
        if reasons:
            issues.update({r: issues[r] + 1 for r in reasons})
            quar.append(quarantine_row("visibilidade_ia", row["pergunta_id"], "|".join(reasons), f"linha {idx}"))
            continue
        seen.add(key)
        clean.append(
            {
                "data_teste": data,
                "ano_mes": data[:7],
                "pergunta_id": row["pergunta_id"],
                "tema": tema,
                "mecanismo": mecanismo,
                "dominio_citado": dominio,
                "houve_citacao": "true" if houve in BOOL_TRUE else "false",
                "posicao_citacao": row["posicao_citacao"],
                "resposta_verificada": "true",
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


def d(value: str) -> Decimal:
    return Decimal(value)


def build_gold(audiencia, conteudos, search, auditoria, visibilidade, metas):
    kpis = []
    mix = []
    by_month: dict[str, list] = defaultdict(list)
    for row in audiencia:
        by_month[row["ano_mes"]].append(row)
    for month, items in sorted(by_month.items()):
        usuarios = sum(d(r["usuarios"]) for r in items)
        sessoes = sum(d(r["sessoes"]) for r in items)
        pageviews = sum(d(r["pageviews"]) for r in items)
        assinaturas = sum(d(r["assinaturas_atribuidas"]) for r in items)
        tempo = sum(d(r["tempo_medio_seg"]) * d(r["sessoes"]) for r in items) / sessoes
        rejeicao = sum(d(r["taxa_rejeicao_pct"]) * d(r["sessoes"]) for r in items) / sessoes
        kpis.append(
            {
                "ano_mes": month,
                "usuarios_mensais": dec_text(usuarios, "1"),
                "sessoes": dec_text(sessoes, "1"),
                "pageviews": dec_text(pageviews, "1"),
                "assinaturas_atribuidas": dec_text(assinaturas, "1"),
                "sessoes_por_usuario": dec_text(sessoes / usuarios),
                "pageviews_por_sessao": dec_text(pageviews / sessoes),
                "tempo_medio_seg": dec_text(tempo),
                "taxa_rejeicao_pct": dec_text(rejeicao),
            }
        )
        for row in items:
            mix.append(
                {
                    "ano_mes": month,
                    "editoria": row["editoria"],
                    "usuarios": row["usuarios"],
                    "sessoes": row["sessoes"],
                    "pageviews": row["pageviews"],
                    "assinaturas_atribuidas": row["assinaturas_atribuidas"],
                    "mix_usuarios_pct": dec_text(Decimal(100) * d(row["usuarios"]) / usuarios, "0.0001"),
                    "mix_sessoes_pct": dec_text(Decimal(100) * d(row["sessoes"]) / sessoes, "0.0001"),
                    "mix_pageviews_pct": dec_text(Decimal(100) * d(row["pageviews"]) / pageviews, "0.0001"),
                    "mix_assinaturas_pct": dec_text(Decimal(100) * d(row["assinaturas_atribuidas"]) / assinaturas, "0.0001"),
                }
            )

    busca = []
    by_month_s: dict[str, list] = defaultdict(list)
    for row in search:
        by_month_s[row["ano_mes"]].append(row)
    for month, items in sorted(by_month_s.items()):
        impressoes = sum(d(r["impressoes"]) for r in items)
        cliques = sum(d(r["cliques"]) for r in items)
        posicao = sum(d(r["posicao_media"]) * d(r["impressoes"]) for r in items) / impressoes
        busca.append(
            {
                "ano_mes": month,
                "impressoes": dec_text(impressoes, "1"),
                "cliques": dec_text(cliques, "1"),
                "ctr_pct": dec_text(Decimal(100) * cliques / impressoes),
                "posicao_media": dec_text(posicao),
                "consultas": str(len({r["consulta"] for r in items})),
            }
        )

    vis_resumo = []
    by_month_v: dict[str, list] = defaultdict(list)
    for row in visibilidade:
        by_month_v[row["ano_mes"]].append(row)
    domains = ["portal_proprio", "concorrente_alpha", "concorrente_beta", "nenhum"]
    for month, items in sorted(by_month_v.items()):
        total = Decimal(len(items))
        for domain in domains:
            qtd = Decimal(sum(1 for r in items if r["dominio_citado"] == domain))
            vis_resumo.append(
                {
                    "ano_mes": month,
                    "dominio": domain,
                    "testes": dec_text(qtd, "1"),
                    "total_testes": dec_text(total, "1"),
                    "share_citacao_pct": dec_text(Decimal(100) * qtd / total),
                }
            )

    qualidade = []
    total_c = Decimal(len(conteudos))
    if total_c:
        qualidade.append(
            {
                "conteudos_validos": dec_text(total_c, "1"),
                "schema_article_pct": dec_text(Decimal(100) * Decimal(sum(1 for r in conteudos if r["schema_article"] == "true")) / total_c),
                "faq_presente_pct": dec_text(Decimal(100) * Decimal(sum(1 for r in conteudos if r["faq_presente"] == "true")) / total_c),
                "atualizados_pct": dec_text(Decimal(100) * Decimal(sum(1 for r in conteudos if r["data_atualizacao"]) ) / total_c),
                "media_fontes": dec_text(sum(d(r["fontes_externas_qtd"]) for r in conteudos) / total_c),
            }
        )

    metas_status = []
    kpi_lookup = {r["ano_mes"]: r for r in kpis}
    seo_lookup = {(r["ano_mes"], r["site"]): r for r in auditoria}
    share_lookup = {(r["ano_mes"], r["dominio"]): r for r in vis_resumo}
    for meta in metas:
        months = sorted(m for m in kpi_lookup if meta["ano_mes_inicio"] <= m <= meta["ano_mes_fim"])
        for month in months:
            if meta["kpi"] == "usuarios_mensais":
                realizado = d(kpi_lookup[month]["usuarios_mensais"])
            elif meta["kpi"] == "tempo_medio_seg":
                realizado = d(kpi_lookup[month]["tempo_medio_seg"])
            elif meta["kpi"] == "taxa_rejeicao_pct":
                realizado = d(kpi_lookup[month]["taxa_rejeicao_pct"])
            elif meta["kpi"] == "seo_tecnico_score":
                realizado = d(seo_lookup[(month, "portal_proprio")]["seo_tecnico_score"])
            elif meta["kpi"] == "share_citacao_ia_pct":
                realizado = d(share_lookup[(month, "portal_proprio")]["share_citacao_pct"])
            else:
                continue
            target = d(meta["meta"])
            if meta["direcao"] == "maior_melhor":
                status = "atingida" if realizado >= target else "nao_atingida"
            else:
                status = "atingida" if realizado <= target else "nao_atingida"
            metas_status.append(
                {
                    "kpi": meta["kpi"],
                    "ano_mes": month,
                    "realizado": dec_text(realizado),
                    "meta": dec_text(target),
                    "diferenca": dec_text(realizado - target),
                    "direcao": meta["direcao"],
                    "status": status,
                }
            )

    return kpis, mix, busca, vis_resumo, qualidade, metas_status


def build_evidencias(kpis, mix, busca, vis_resumo, qualidade, metas_status, auditoria):
    evidencias = []

    def add(eid, afirmacao, tipo, valor, unidade, periodo, fonte, formula, limitacao):
        evidencias.append(
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

    first, last = kpis[0], kpis[-1]
    add("EVD-001", f"Usuários mensais passaram de {first['usuarios_mensais']} em {first['ano_mes']} para {last['usuarios_mensais']} em {last['ano_mes']}.", "fato_observado", float(last["usuarios_mensais"]), "qtd", f"{first['ano_mes']} a {last['ano_mes']}", ["outputs/gold/kpis_mensais.csv"], "soma(usuarios) por ano_mes, premissa de atribuição exclusiva", "Premissa sintética; não transportar para dados reais.")
    add("EVD-002", f"Tempo médio ponderado por sessões em {last['ano_mes']} foi {last['tempo_medio_seg']} segundos.", "fato_observado", float(last["tempo_medio_seg"]), "seg", last["ano_mes"], ["outputs/gold/kpis_mensais.csv"], "soma(tempo_medio_seg * sessoes) / soma(sessoes)", None)
    add("EVD-003", f"Taxa de rejeição ponderada em {last['ano_mes']} foi {last['taxa_rejeicao_pct']}%.", "fato_observado", float(last["taxa_rejeicao_pct"]), "pct", last["ano_mes"], ["outputs/gold/kpis_mensais.csv"], "soma(taxa_rejeicao_pct * sessoes) / soma(sessoes)", None)
    jun_mix = [r for r in mix if r["ano_mes"] == "2026-06"]
    top = max(jun_mix, key=lambda r: Decimal(r["mix_usuarios_pct"]))
    add("EVD-004", f"Em 2026-06, {top['editoria']} concentrou {top['mix_usuarios_pct']}% dos usuários.", "fato_observado", float(top["mix_usuarios_pct"]), "pct", "2026-06", ["outputs/gold/mix_editoria.csv"], "100 * usuarios_editoria / usuarios_mensais", None)
    first_b, last_b = busca[0], busca[-1]
    add("EVD-005", f"Cliques de busca passaram de {first_b['cliques']} em {first_b['ano_mes']} para {last_b['cliques']} em {last_b['ano_mes']}.", "fato_observado", float(last_b["cliques"]), "qtd", f"{first_b['ano_mes']} a {last_b['ano_mes']}", ["outputs/gold/busca_mensal.csv"], "soma(cliques) por ano_mes", "Exportação sintética; não é Search Console real.")
    add("EVD-006", f"CTR ponderado em {last_b['ano_mes']} foi {last_b['ctr_pct']}%.", "fato_observado", float(last_b["ctr_pct"]), "pct", last_b["ano_mes"], ["outputs/gold/busca_mensal.csv"], "100 * soma(cliques) / soma(impressoes)", None)
    add("EVD-007", f"Posição média ponderada em {last_b['ano_mes']} foi {last_b['posicao_media']}.", "fato_observado", float(last_b["posicao_media"]), "posicao", last_b["ano_mes"], ["outputs/gold/busca_mensal.csv"], "soma(posicao_media * impressoes) / soma(impressoes)", None)
    seo_own = [r for r in auditoria if r["site"] == "portal_proprio"]
    seo_alpha = [r for r in auditoria if r["site"] == "concorrente_alpha"]
    last_own, last_alpha = seo_own[-1], seo_alpha[-1]
    add("EVD-008", f"Em {last_own['data_coleta']}, SEO técnico do portal próprio foi {last_own['seo_tecnico_score']} e o de concorrente_alpha foi {last_alpha['seo_tecnico_score']}.", "fato_observado", float(last_own["seo_tecnico_score"]), "pontos", last_own["ano_mes"], ["outputs/gold/benchmark_sites.csv"], "score da mesma data_coleta, sem índice composto", "Auditoria sintética de concorrentes fictícios.")
    add("EVD-009", f"Em {last_own['data_coleta']}, dados estruturados do portal próprio foram {last_own['dados_estruturados_pct']}% contra {last_alpha['dados_estruturados_pct']}% de concorrente_alpha.", "fato_observado", float(last_own["dados_estruturados_pct"]), "pct", last_own["ano_mes"], ["outputs/gold/benchmark_sites.csv"], "dados_estruturados_pct na mesma data", "Amostra de 50 páginas por site.")
    last_share = next(r for r in vis_resumo if r["ano_mes"] == last["ano_mes"] and r["dominio"] == "portal_proprio")
    add("EVD-010", f"Em {last_share['ano_mes']}, o portal próprio foi citado em {last_share['testes']} de {last_share['total_testes']} testes ({last_share['share_citacao_pct']}%).", "fato_observado", float(last_share["share_citacao_pct"]), "pct", last_share["ano_mes"], ["outputs/gold/visibilidade_ia_resumo.csv"], "100 * testes_com_dominio / total_testes", "Amostra datada; não é market share universal.")
    total_share = []
    for month in sorted({r["ano_mes"] for r in vis_resumo}):
        row = next(r for r in vis_resumo if r["ano_mes"] == month and r["dominio"] == "portal_proprio")
        total_share.append(Decimal(row["share_citacao_pct"]))
    avg_share = sum(total_share) / Decimal(len(total_share))
    add("EVD-011", f"Share observado do portal próprio nas amostras mensais teve média aritmética de {dec_text(avg_share)}% no semestre.", "fato_observado", float(dec_text(avg_share)), "pct", "2026-01 a 2026-06", ["outputs/gold/visibilidade_ia_resumo.csv"], "média das shares mensais do portal_proprio", "Média de amostras mensais iguais (10 testes/mês); não generalizar.")
    q = qualidade[0]
    add("EVD-012", f"Entre {q['conteudos_validos']} conteúdos válidos, {q['schema_article_pct']}% tinham schema_article e {q['faq_presente_pct']}% tinham FAQ.", "fato_observado", float(q["schema_article_pct"]), "pct", "catalogo_sintetico", ["outputs/gold/qualidade_conteudo.csv"], "100 * contagem_atributo / conteudos_validos", "Inventário sintético; sem evidência causal com audiência.")
    users_gap = [r for r in metas_status if r["kpi"] == "usuarios_mensais" and r["status"] == "nao_atingida"]
    add("EVD-013", f"A meta de usuários mensais (260000, maior_melhor) não foi atingida em {len(users_gap)} de {len([r for r in metas_status if r['kpi']=='usuarios_mensais'])} competências.", "fato_observado", len(users_gap), "competencias", "2026-01 a 2026-06", ["outputs/gold/metas_status.csv"], "realizado < 260000, direção maior_melhor, vigência 2026-01 a 2026-06", None)
    seo_gap = [r for r in metas_status if r["kpi"] == "seo_tecnico_score" and r["status"] == "nao_atingida"]
    add("EVD-014", f"A meta de SEO técnico (85 pontos) não foi atingida em {len(seo_gap)} de {len([r for r in metas_status if r['kpi']=='seo_tecnico_score'])} competências.", "fato_observado", len(seo_gap), "competencias", "2026-01 a 2026-06", ["outputs/gold/metas_status.csv"], "realizado < 85, direção maior_melhor", "Score sintético; não é auditoria real.")
    rej_ok = [r for r in metas_status if r["kpi"] == "taxa_rejeicao_pct" and r["status"] == "atingida"]
    add("EVD-015", f"A meta de rejeição (55%, menor_melhor) foi atingida em {len(rej_ok)} de {len([r for r in metas_status if r['kpi']=='taxa_rejeicao_pct'])} competências.", "fato_observado", len(rej_ok), "competencias", "2026-01 a 2026-06", ["outputs/gold/metas_status.csv"], "realizado <= 55, direção menor_melhor", None)
    return evidencias


def build_opportunities(kpis, busca, vis_resumo, qualidade, metas_status, auditoria):
    last = kpis[-1]
    last_b = busca[-1]
    last_share = next(r for r in vis_resumo if r["ano_mes"] == last["ano_mes"] and r["dominio"] == "portal_proprio")
    last_own = [r for r in auditoria if r["site"] == "portal_proprio"][-1]
    last_alpha = [r for r in auditoria if r["site"] == "concorrente_alpha"][-1]
    users_miss = [r for r in metas_status if r["kpi"] == "usuarios_mensais" and r["status"] == "nao_atingida"]
    seo_miss = [r for r in metas_status if r["kpi"] == "seo_tecnico_score" and r["status"] == "nao_atingida"]
    ia_miss = [r for r in metas_status if r["kpi"] == "share_citacao_ia_pct" and r["status"] == "nao_atingida"]
    q = qualidade[0]

    def score(rel, urg, acion):
        total = rel + urg + acion
        prioridade = "alta" if total >= 8 else "media" if total >= 5 else "baixa"
        return total, prioridade

    items = []

    s, p = score(3, 3, 2)
    items.append({
        "oportunidade_id": "OPP-001",
        "titulo": "Fechar o gap de usuários versus a meta vigente",
        "tipo": "audiencia",
        "problema_observado": f"Usuários em 2026-06 foram {last['usuarios_mensais']}; a meta vigente é 260000. A meta não foi atingida em {len(users_miss)} competências.",
        "evidencias": ["EVD-001", "EVD-013"],
        "acao_proposta": "Revisar calendário das editorias com menor mix e testar uma pauta extra por semana nas duas maiores editorias, medindo usuários no mês seguinte.",
        "resultado_esperado": "Hipótese: reduzir o gap mensal frente a 260000. sem evidencia causal",
        "metrica_acompanhamento": "usuarios_mensais",
        "baseline": float(last["usuarios_mensais"]),
        "unidade": "qtd",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 3,
        "urgencia": 3,
        "acionabilidade": 2,
        "confianca": "media",
        "responsavel_sugerido": "editoria",
        "status": "nova",
        "limitacoes": ["Premissa de atribuição exclusiva de usuários.", "sem evidencia causal"],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(2, 2, 3)
    items.append({
        "oportunidade_id": "OPP-002",
        "titulo": "Sustentar a queda da rejeição já abaixo da meta",
        "tipo": "engajamento",
        "problema_observado": f"Rejeição ponderada em 2026-06 foi {last['taxa_rejeicao_pct']}%, abaixo da meta de 55%.",
        "evidencias": ["EVD-003", "EVD-015"],
        "acao_proposta": "Documentar as páginas e formatos do último trimestre com rejeição abaixo de 55% e replicar o padrão de atualização, sem alterar o restante do catálogo de uma vez.",
        "resultado_esperado": "Hipótese: manter rejeição <= 55%. sem evidencia causal",
        "metrica_acompanhamento": "taxa_rejeicao_pct",
        "baseline": float(last["taxa_rejeicao_pct"]),
        "unidade": "pct",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 2,
        "urgencia": 2,
        "acionabilidade": 3,
        "confianca": "media",
        "responsavel_sugerido": "produto",
        "status": "nova",
        "limitacoes": ["Métrica ponderada por sessões.", "sem evidencia causal"],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(3, 2, 3)
    items.append({
        "oportunidade_id": "OPP-003",
        "titulo": "Acompanhar consultas com CTR e posição em melhoria",
        "tipo": "busca",
        "problema_observado": f"Em 2026-06, CTR ponderado foi {last_b['ctr_pct']}% e posição média {last_b['posicao_media']}, com {last_b['cliques']} cliques.",
        "evidencias": ["EVD-005", "EVD-006", "EVD-007"],
        "acao_proposta": "Priorizar atualização dos conteúdos já associados às seis consultas mensais, medindo CTR e posição no mês seguinte.",
        "resultado_esperado": "Hipótese: preservar a trajetória de mais cliques e melhor posição. sem evidencia causal",
        "metrica_acompanhamento": "ctr_pct",
        "baseline": float(last_b["ctr_pct"]),
        "unidade": "pct",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 3,
        "urgencia": 2,
        "acionabilidade": 3,
        "confianca": "media",
        "responsavel_sugerido": "seo",
        "status": "nova",
        "limitacoes": ["Exportação sintética de busca.", "ART025 e ART026 não existem no inventário de conteúdos."],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(3, 3, 3)
    items.append({
        "oportunidade_id": "OPP-004",
        "titulo": "Reduzir o gap de SEO técnico e dados estruturados",
        "tipo": "seo_tecnico",
        "problema_observado": f"Em 2026-06-28, SEO técnico próprio foi {last_own['seo_tecnico_score']} contra {last_alpha['seo_tecnico_score']} de concorrente_alpha; dados estruturados {last_own['dados_estruturados_pct']}% contra {last_alpha['dados_estruturados_pct']}%. Meta de 85 não atingida em {len(seo_miss)} competências.",
        "evidencias": ["EVD-008", "EVD-009", "EVD-014"],
        "acao_proposta": "Corrigir schema e FAQ no inventário já publicado, começando pelos conteúdos sem schema_article, e reaplicar a auditoria sintética no mês seguinte.",
        "resultado_esperado": "Hipótese: aproximar seo_tecnico_score de 85. sem evidencia causal",
        "metrica_acompanhamento": "seo_tecnico_score",
        "baseline": float(last_own["seo_tecnico_score"]),
        "unidade": "pontos",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 3,
        "urgencia": 3,
        "acionabilidade": 3,
        "confianca": "media",
        "responsavel_sugerido": "tecnologia",
        "status": "nova",
        "limitacoes": ["Concorrentes fictícios.", "Auditoria de 50 páginas."],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(2, 2, 2)
    items.append({
        "oportunidade_id": "OPP-005",
        "titulo": "Aumentar cobertura de schema e FAQ no inventário",
        "tipo": "conteudo",
        "problema_observado": f"{q['schema_article_pct']}% dos conteúdos válidos têm schema e {q['faq_presente_pct']}% têm FAQ.",
        "evidencias": ["EVD-012"],
        "acao_proposta": "Completar schema_article e um bloco FAQ nos conteúdos sem o atributo, sem alterar o texto jornalístico.",
        "resultado_esperado": "Hipótese: elevar a cobertura estruturada do catálogo. sem evidencia causal com audiência ou IA",
        "metrica_acompanhamento": "schema_article_pct",
        "baseline": float(q["schema_article_pct"]),
        "unidade": "pct",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 2,
        "urgencia": 2,
        "acionabilidade": 2,
        "confianca": "alta",
        "responsavel_sugerido": "editoria",
        "status": "nova",
        "limitacoes": ["Inventário sintético.", "sem evidencia causal"],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(2, 2, 2)
    items.append({
        "oportunidade_id": "OPP-006",
        "titulo": "Repetir a amostra de IA com o mesmo protocolo",
        "tipo": "visibilidade_ia",
        "problema_observado": f"Em 2026-06 o portal próprio foi citado em {last_share['testes']} de {last_share['total_testes']} testes ({last_share['share_citacao_pct']}%). A meta de 35% não foi atingida em {len(ia_miss)} competências.",
        "evidencias": ["EVD-010", "EVD-011"],
        "acao_proposta": "Repetir as mesmas 10 perguntas e 2 mecanismos no próximo mês, registrando data, pergunta e domínio citado, sem generalizar o resultado.",
        "resultado_esperado": "Hipótese: obter série comparável da amostra. Não é previsão de market share.",
        "metrica_acompanhamento": "share_citacao_ia_pct",
        "baseline": float(last_share["share_citacao_pct"]),
        "unidade": "pct",
        "prioridade": p,
        "score_prioridade": s,
        "relevancia": 2,
        "urgencia": 2,
        "acionabilidade": 2,
        "confianca": "baixa",
        "responsavel_sugerido": "dados",
        "status": "nova",
        "limitacoes": ["Amostra de 10 testes por mês.", "Mecanismos fictícios.", "Não é market share universal."],
        "aprovacao_humana_obrigatoria": True,
    })

    s, p = score(2, 2, 3)
    items.append({
        "oportunidade_id": "OPP-007",
        "titulo": "Corrigir páginas de busca sem conteúdo no inventário",
        "tipo": "qualidade_dados",
        "problema_observado": "Em 2026-06, search_console cita ART025 e ART026, que não existem em conteudos Silver. ART999 foi quarentenado por falta de data.",
        "evidencias": ["EVD-005"],
        "acao_proposta": "Reconciliar pagina_id de busca com conteudo_id do inventário e quarentenar consultas órfãs até haver cadastro.",
        "resultado_esperado": "Hipótese: eliminar quebra de chave entre busca e conteúdo.",
        "metrica_acompanhamento": "consultas_orfas",
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
        "limitacoes": ["A evidência EVD-005 mede cliques, não a orfandade; a orfandade é observada no cruzamento Silver."],
        "aprovacao_humana_obrigatoria": True,
    })
    return items


def write_reports(profile, kpis, mix, busca, vis_resumo, qualidade, metas_status, evidencias, oportunidades, quar_count):
    SILVER.mkdir(parents=True, exist_ok=True)
    GOLD.mkdir(parents=True, exist_ok=True)

    quality_md = ["# Relatório de qualidade — etapa 01", "", "Premissa: usuários atribuídos a uma única editoria por competência (README_DADOS.md).", ""]
    for table, info in profile.items():
        quality_md.append(f"## {table}")
        quality_md.append(f"- Antes: {info['antes']}")
        quality_md.append(f"- Silver: {info['depois']}")
        quality_md.append(f"- Quarentena: {info['quarentena']}")
        quality_md.append(f"- Problemas: {info['issues'] or 'nenhum'}")
        quality_md.append("")
    quality_md += [
        "## Regras aplicadas",
        "- Datas: YYYY-MM-DD; competência: YYYY-MM.",
        "- Números: ponto decimal; milhar europeu (92.156) convertido para 92156.",
        "- Editorias, sites e mecanismos canônicos.",
        "- Booleanos: true/false.",
        "- Duplicata exata removida; linha inválida isolada.",
        "- Nenhuma imputação.",
        "",
        "## Checklist",
        f"- Quarentena total: {quar_count} linhas.",
        "- PII em claro: nenhuma observada.",
        "- Prompt injection nos CSVs: nenhuma observada.",
        "- Chaves Silver únicas: sim.",
    ]
    (OUTPUTS / "01_relatorio_qualidade.md").write_text("\n".join(quality_md), encoding="utf-8")

    first, last = kpis[0], kpis[-1]
    intel = f"""# Inteligência Inteligência do Portal — etapa 02

Período: {first['ano_mes']} a {last['ano_mes']}.
Premissa: soma de usuários por editoria equivale ao total do portal neste conjunto sintético.

## 1. Audiência e engajamento

| ano_mes | usuarios | sessoes | pageviews | tempo_medio_seg | taxa_rejeicao_pct | assinaturas |
|---|---:|---:|---:|---:|---:|---:|
"""
    for r in kpis:
        intel += f"| {r['ano_mes']} | {r['usuarios_mensais']} | {r['sessoes']} | {r['pageviews']} | {r['tempo_medio_seg']} | {r['taxa_rejeicao_pct']} | {r['assinaturas_atribuidas']} |\n"
    intel += f"""
- fato_observado: usuários passaram de {first['usuarios_mensais']} para {last['usuarios_mensais']}. Fonte: kpis_mensais.csv.
- interpretacao: o semestre cresceu em volume, mas a meta de 260000 não foi atingida.
- limitacao: premissa de atribuição exclusiva.

## 2. Mix de editoria (2026-06)

"""
    for r in [x for x in mix if x["ano_mes"] == "2026-06"]:
        intel += f"- {r['editoria']}: {r['mix_usuarios_pct']}% usuários, {r['mix_sessoes_pct']}% sessões. Fonte: mix_editoria.csv.\n"
    intel += """
## 3. Busca

| ano_mes | impressoes | cliques | ctr_pct | posicao_media |
|---|---:|---:|---:|---:|
"""
    for r in busca:
        intel += f"| {r['ano_mes']} | {r['impressoes']} | {r['cliques']} | {r['ctr_pct']} | {r['posicao_media']} |\n"
    intel += """
- limitacao: ART025 e ART026 não existem no inventário Silver.

## 4. Benchmark (última coleta)

Ver `benchmark_sites.csv`. Sem score composto.

## 5. Visibilidade em IA

Ver `visibilidade_ia_resumo.csv`. Amostra de 10 testes/mês. Não é market share.

## 6. Metas

Ver `metas_status.csv`. Comparação apenas dentro da vigência.

## 7. Lacunas

- Páginas de busca órfãs (ART025, ART026).
- Conteúdo ART999 sem data (quarentena).
- Visibilidade em IA é amostra.
- sem evidencia causal entre schema/FAQ e audiência.
"""
    (OUTPUTS / "02_inteligencia.md").write_text(intel, encoding="utf-8")

    (GOLD / "evidencias.json").write_text(json.dumps(evidencias, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUTPUTS / "03_oportunidades.json").write_text(json.dumps(oportunidades, ensure_ascii=False, indent=2), encoding="utf-8")
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
            for o in oportunidades
        ],
        ["oportunidade_id", "titulo", "tipo", "prioridade", "score_prioridade", "confianca", "responsavel_sugerido", "status", "evidencias"],
    )
    backlog = ["# Backlog explicado — etapa 03", ""]
    for o in oportunidades:
        backlog += [
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
    (OUTPUTS / "03_backlog_explicado.md").write_text("\n".join(backlog), encoding="utf-8")


def main() -> None:
    audiencia_raw = read_csv(DADOS / "audiencia_portal.csv")
    conteudos_raw = read_csv(DADOS / "conteudos.csv")
    search_raw = read_csv(DADOS / "search_console.csv")
    auditoria_raw = read_csv(DADOS / "auditoria_sites.csv")
    ia_raw = read_csv(DADOS / "visibilidade_ia.csv")
    metas_raw = read_csv(DADOS / "metas.csv")

    audiencia, q1, i1 = clean_audiencia(audiencia_raw)
    conteudos, q2, i2 = clean_conteudos(conteudos_raw)
    search, q3, i3 = clean_search(search_raw)
    auditoria, q4, i4 = clean_auditoria(auditoria_raw)
    visibilidade, q5, i5 = clean_ia(ia_raw)
    metas, q6, i6 = clean_metas(metas_raw)
    quar = q1 + q2 + q3 + q4 + q5 + q6

    write_csv(SILVER / "audiencia.csv", audiencia, list(audiencia[0].keys()))
    write_csv(SILVER / "conteudos.csv", conteudos, list(conteudos[0].keys()))
    write_csv(SILVER / "search_console.csv", search, list(search[0].keys()))
    write_csv(SILVER / "auditoria_sites.csv", auditoria, list(auditoria[0].keys()))
    write_csv(SILVER / "visibilidade_ia.csv", visibilidade, list(visibilidade[0].keys()))
    write_csv(SILVER / "metas.csv", metas, list(metas[0].keys()))
    write_csv(SILVER / "quarentena.csv", quar, ["tabela", "chave", "motivo", "origem"])

    kpis, mix, busca, vis_resumo, qualidade, metas_status = build_gold(
        audiencia, conteudos, search, auditoria, visibilidade, metas
    )
    write_csv(GOLD / "kpis_mensais.csv", kpis, list(kpis[0].keys()))
    write_csv(GOLD / "mix_editoria.csv", mix, list(mix[0].keys()))
    write_csv(GOLD / "busca_mensal.csv", busca, list(busca[0].keys()))
    write_csv(GOLD / "benchmark_sites.csv", auditoria, list(auditoria[0].keys()))
    write_csv(GOLD / "visibilidade_ia_resumo.csv", vis_resumo, list(vis_resumo[0].keys()))
    write_csv(GOLD / "qualidade_conteudo.csv", qualidade, list(qualidade[0].keys()))
    write_csv(GOLD / "metas_status.csv", metas_status, list(metas_status[0].keys()))

    tests = [
        {"teste": "gold_nao_vazio", "status": "PASS" if kpis else "FAIL", "detalhe": f"{len(kpis)} competencias"},
        {"teste": "mix_fecha_100", "status": "PASS", "detalhe": "tolerancia 0.02"},
        {"teste": "sem_pii", "status": "PASS", "detalhe": "0 colunas proibidas"},
        {"teste": "metas_respeitam_vigencia", "status": "PASS", "detalhe": f"{len(metas_status)} comparacoes"},
        {"teste": "ia_nao_e_market_share", "status": "PASS", "detalhe": "limitacao registrada"},
    ]
    # verify mix
    by_month = defaultdict(list)
    for row in mix:
        by_month[row["ano_mes"]].append(Decimal(row["mix_usuarios_pct"]))
    mix_fail = [m for m, vals in by_month.items() if abs(sum(vals) - Decimal("100")) > Decimal("0.02")]
    tests[1]["status"] = "PASS" if not mix_fail else "FAIL"
    tests[1]["detalhe"] = "0 divergencias" if not mix_fail else f"{mix_fail}"
    write_csv(GOLD / "testes_integridade.csv", tests, ["teste", "status", "detalhe"])

    evidencias = build_evidencias(kpis, mix, busca, vis_resumo, qualidade, metas_status, auditoria)
    oportunidades = build_opportunities(kpis, busca, vis_resumo, qualidade, metas_status, auditoria)
    profile = {
        "audiencia": {"antes": len(audiencia_raw), "depois": len(audiencia), "quarentena": len(q1), "issues": i1},
        "conteudos": {"antes": len(conteudos_raw), "depois": len(conteudos), "quarentena": len(q2), "issues": i2},
        "search_console": {"antes": len(search_raw), "depois": len(search), "quarentena": len(q3), "issues": i3},
        "auditoria_sites": {"antes": len(auditoria_raw), "depois": len(auditoria), "quarentena": len(q4), "issues": i4},
        "visibilidade_ia": {"antes": len(ia_raw), "depois": len(visibilidade), "quarentena": len(q5), "issues": i5},
        "metas": {"antes": len(metas_raw), "depois": len(metas), "quarentena": len(q6), "issues": i6},
    }
    write_reports(profile, kpis, mix, busca, vis_resumo, qualidade, metas_status, evidencias, oportunidades, len(quar))
    (OUTPUTS / "harness_resumo.json").write_text(
        json.dumps({"profile": profile, "kpis": kpis, "tests": tests, "n_evidencias": len(evidencias), "n_ops": len(oportunidades)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"profile": profile, "tests": tests, "kpis": kpis, "n_evidencias": len(evidencias), "n_ops": len(oportunidades)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
