from __future__ import annotations

import csv
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent


def write_csv(file_name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (DATA_DIR / file_name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_audiencia() -> None:
    editorias = {
        "Política": (58_000, 1.22, 176, 61.2, 34),
        "Economia": (47_000, 1.18, 194, 57.5, 29),
        "Tecnologia": (41_000, 1.27, 221, 52.4, 31),
        "Esportes": (52_000, 1.15, 148, 64.1, 18),
        "Cultura": (28_000, 1.11, 205, 55.8, 14),
    }
    month_factors = [0.88, 0.96, 1.04, 1.10, 1.03, 1.16]
    rows: list[dict[str, object]] = []

    for month_index, factor in enumerate(month_factors, start=1):
        for editoria_index, (editoria, values) in enumerate(editorias.items()):
            usuarios_base, sessoes_factor, tempo_base, rejeicao_base, assinaturas_base = values
            usuarios = int(usuarios_base * factor * (1 + editoria_index * 0.008))
            sessoes = int(usuarios * sessoes_factor)
            pageviews = int(sessoes * (1.48 + editoria_index * 0.04))
            tempo = tempo_base + month_index * 3 - editoria_index
            rejeicao = rejeicao_base - month_index * 0.7 + editoria_index * 0.15
            assinaturas = int(assinaturas_base * factor + month_index + editoria_index)

            month_value = (
                f"2026-{month_index:02d}"
                if month_index % 3 == 1
                else f"{month_index:02d}/2026"
                if month_index % 3 == 2
                else f"2026/{month_index:02d}"
            )
            editoria_value = (
                editoria.upper()
                if (month_index + editoria_index) % 4 == 0
                else f" {editoria} "
            )
            rows.append(
                {
                    "ano_mes": month_value,
                    "editoria": editoria_value,
                    "usuarios": f"{usuarios:,}".replace(",", ".") if month_index % 2 == 0 else usuarios,
                    "sessoes": sessoes,
                    "pageviews": f"{pageviews:,}".replace(",", ".") if month_index % 2 == 1 else pageviews,
                    "tempo_medio_seg": tempo,
                    "taxa_rejeicao_pct": f"{rejeicao:.1f}".replace(".", ",") if editoria_index % 2 == 0 else f"{rejeicao:.1f}",
                    "assinaturas_atribuidas": assinaturas,
                }
            )

    rows.append(rows[7].copy())
    rows.append(
        {
            "ano_mes": "2026-06",
            "editoria": "TESTE",
            "usuarios": 100,
            "sessoes": 120,
            "pageviews": -50,
            "tempo_medio_seg": 0,
            "taxa_rejeicao_pct": "n/a",
            "assinaturas_atribuidas": 0,
        }
    )
    write_csv(
        "audiencia_portal.csv",
        [
            "ano_mes",
            "editoria",
            "usuarios",
            "sessoes",
            "pageviews",
            "tempo_medio_seg",
            "taxa_rejeicao_pct",
            "assinaturas_atribuidas",
        ],
        rows,
    )


def build_conteudos() -> None:
    editorias = ["Política", "Economia", "Tecnologia", "Esportes", "Cultura"]
    formatos = ["noticia", "analise", "explicador", "entrevista"]
    rows: list[dict[str, object]] = []

    for index in range(1, 25):
        month = ((index - 1) % 6) + 1
        day = ((index * 3) % 27) + 1
        editoria = editorias[(index - 1) % len(editorias)]
        updated_month = min(month + (1 if index % 4 == 0 else 0), 6)
        rows.append(
            {
                "conteudo_id": f"ART{index:03d}",
                "data_publicacao": (
                    f"2026-{month:02d}-{day:02d}"
                    if index % 3 == 0
                    else f"{day:02d}/{month:02d}/2026"
                ),
                "editoria": editoria.upper() if index % 5 == 0 else editoria,
                "formato": formatos[(index - 1) % len(formatos)],
                "titulo_sintetico": f"Conteúdo sintético {index:02d} sobre {editoria}",
                "autor_pseudo": f"AUTOR_{((index - 1) % 6) + 1:02d}",
                "palavras": 520 + index * 37,
                "data_atualizacao": (
                    f"2026-{updated_month:02d}-{min(day + 2, 28):02d}"
                    if index % 4 == 0
                    else ""
                ),
                "schema_article": "SIM" if index % 5 != 0 else "nao",
                "faq_presente": "sim" if index % 6 == 0 else "não",
                "fontes_externas_qtd": (index * 2) % 7,
                "status": "Publicado" if index % 7 != 0 else "publicado ",
            }
        )

    rows.append(rows[4].copy())
    rows.append(
        {
            "conteudo_id": "ART999",
            "data_publicacao": "",
            "editoria": "Economia",
            "formato": "noticia",
            "titulo_sintetico": "Registro inválido sem data",
            "autor_pseudo": "AUTOR_99",
            "palavras": 450,
            "data_atualizacao": "",
            "schema_article": "sim",
            "faq_presente": "não",
            "fontes_externas_qtd": 1,
            "status": "publicado",
        }
    )
    write_csv(
        "conteudos.csv",
        [
            "conteudo_id",
            "data_publicacao",
            "editoria",
            "formato",
            "titulo_sintetico",
            "autor_pseudo",
            "palavras",
            "data_atualizacao",
            "schema_article",
            "faq_presente",
            "fontes_externas_qtd",
            "status",
        ],
        rows,
    )


def build_search_console() -> None:
    temas = [
        ("eleições municipais", "Política"),
        ("taxa de juros", "Economia"),
        ("inteligência artificial", "Tecnologia"),
        ("campeonato nacional", "Esportes"),
        ("agenda cultural", "Cultura"),
        ("explicador do dia", "Economia"),
    ]
    rows: list[dict[str, object]] = []

    for month in range(1, 7):
        for index, (consulta, editoria) in enumerate(temas, start=1):
            impressions = 18_000 + month * 2_300 + index * 1_450
            position = max(2.4, 12.8 - month * 0.65 + index * 0.32)
            ctr = min(12.0, 2.1 + (13 - position) * 0.55)
            clicks = int(impressions * ctr / 100)
            rows.append(
                {
                    "ano_mes": f"{month:02d}/2026" if month % 2 == 0 else f"2026-{month:02d}",
                    "consulta": consulta.upper() if index == 3 and month % 2 == 0 else consulta,
                    "editoria": editoria,
                    "impressoes": f"{impressions:,}".replace(",", ".") if index % 2 == 0 else impressions,
                    "cliques": clicks,
                    "ctr_pct": f"{ctr:.2f}".replace(".", ",") if month % 2 == 0 else f"{ctr:.2f}",
                    "posicao_media": f"{position:.2f}",
                    "pagina_id": f"ART{((month - 1) * 4 + index):03d}",
                }
            )

    rows.append(
        {
            "ano_mes": "2026-06",
            "consulta": "consulta sem medição",
            "editoria": "Tecnologia",
            "impressoes": "n/a",
            "cliques": "",
            "ctr_pct": "",
            "posicao_media": "",
            "pagina_id": "ART999",
        }
    )
    write_csv(
        "search_console.csv",
        [
            "ano_mes",
            "consulta",
            "editoria",
            "impressoes",
            "cliques",
            "ctr_pct",
            "posicao_media",
            "pagina_id",
        ],
        rows,
    )


def build_auditoria_sites() -> None:
    sites = {
        "portal_proprio": (72, 74, 58, 2.9, 82),
        "concorrente_alpha": (81, 84, 76, 2.2, 91),
        "concorrente_beta": (67, 79, 69, 3.4, 88),
    }
    rows: list[dict[str, object]] = []

    for month in range(1, 7):
        for site_index, (site, values) in enumerate(sites.items()):
            performance, seo, structured, load_time, mobile = values
            rows.append(
                {
                    "data_coleta": f"2026-{month:02d}-28",
                    "site": site.upper() if month == 2 and site_index == 0 else site,
                    "tipo": "proprio" if site == "portal_proprio" else "concorrente",
                    "performance_score": min(100, performance + month),
                    "seo_tecnico_score": min(100, seo + month // 2),
                    "dados_estruturados_pct": min(100, structured + month * 2),
                    "tempo_carregamento_seg": f"{max(1.2, load_time - month * 0.08):.2f}".replace(".", ",") if site_index == 1 else f"{max(1.2, load_time - month * 0.08):.2f}",
                    "mobile_score": min(100, mobile + month),
                    "paginas_amostradas": 50,
                    "fonte_coleta": "auditoria_sintetica_publica",
                }
            )

    write_csv(
        "auditoria_sites.csv",
        [
            "data_coleta",
            "site",
            "tipo",
            "performance_score",
            "seo_tecnico_score",
            "dados_estruturados_pct",
            "tempo_carregamento_seg",
            "mobile_score",
            "paginas_amostradas",
            "fonte_coleta",
        ],
        rows,
    )


def build_visibilidade_ia() -> None:
    temas = ["Política", "Economia", "Tecnologia", "Esportes", "Cultura"]
    engines = ["ia_a", "ia_b"]
    citation_cycle = [
        "portal_proprio",
        "concorrente_alpha",
        "nenhum",
        "concorrente_beta",
        "portal_proprio",
    ]
    rows: list[dict[str, object]] = []

    for month in range(1, 7):
        for theme_index, tema in enumerate(temas):
            for engine_index, engine in enumerate(engines):
                cited = citation_cycle[(month + theme_index + engine_index) % len(citation_cycle)]
                rows.append(
                    {
                        "data_teste": f"2026-{month:02d}-25",
                        "pergunta_id": f"Q{month:02d}{theme_index + 1:02d}{engine_index + 1}",
                        "tema": tema,
                        "mecanismo": engine.upper() if month % 2 == 0 else engine,
                        "dominio_citado": cited,
                        "houve_citacao": "sim" if cited != "nenhum" else "não",
                        "posicao_citacao": ((theme_index + engine_index) % 3) + 1 if cited != "nenhum" else "",
                        "resposta_verificada": "sim",
                        "observacao": "Amostra sintética; resultado válido somente na data do teste",
                    }
                )

    write_csv(
        "visibilidade_ia.csv",
        [
            "data_teste",
            "pergunta_id",
            "tema",
            "mecanismo",
            "dominio_citado",
            "houve_citacao",
            "posicao_citacao",
            "resposta_verificada",
            "observacao",
        ],
        rows,
    )


def build_metas() -> None:
    rows = [
        {
            "kpi": "usuarios_mensais",
            "meta": 260000,
            "unidade": "qtd",
            "direcao": "maior_melhor",
            "ano_mes_inicio": "2026-01",
            "ano_mes_fim": "2026-06",
        },
        {
            "kpi": "tempo_medio_seg",
            "meta": 190,
            "unidade": "seg",
            "direcao": "maior_melhor",
            "ano_mes_inicio": "2026-01",
            "ano_mes_fim": "2026-06",
        },
        {
            "kpi": "taxa_rejeicao_pct",
            "meta": 55,
            "unidade": "pct",
            "direcao": "menor_melhor",
            "ano_mes_inicio": "2026-01",
            "ano_mes_fim": "2026-06",
        },
        {
            "kpi": "seo_tecnico_score",
            "meta": 85,
            "unidade": "pontos",
            "direcao": "maior_melhor",
            "ano_mes_inicio": "2026-01",
            "ano_mes_fim": "2026-06",
        },
        {
            "kpi": "share_citacao_ia_pct",
            "meta": 35,
            "unidade": "pct",
            "direcao": "maior_melhor",
            "ano_mes_inicio": "2026-01",
            "ano_mes_fim": "2026-06",
        },
    ]
    write_csv(
        "metas.csv",
        ["kpi", "meta", "unidade", "direcao", "ano_mes_inicio", "ano_mes_fim"],
        rows,
    )


def main() -> None:
    build_audiencia()
    build_conteudos()
    build_search_console()
    build_auditoria_sites()
    build_visibilidade_ia()
    build_metas()
    print("Dados sintéticos gerados em", DATA_DIR)


if __name__ == "__main__":
    main()
