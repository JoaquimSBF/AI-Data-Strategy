from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


class ReadmePDF(FPDF):
    def __init__(self, title: str) -> None:
        super().__init__(format="A4")
        self.document_title = title
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(18, 16, 18)
        self.add_font("ArialLocal", fname=str(FONT))
        self.add_font("ArialLocal", style="B", fname=str(FONT_BOLD))

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("ArialLocal", size=8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 6, self.document_title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(190, 190, 190)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("ArialLocal", size=8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, str(self.page_no()), align="C")


def safe(text: str) -> str:
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def put(pdf: ReadmePDF, text: str, *, size: float = 11, bold: bool = False, height: float = 5.6) -> None:
    pdf.set_font("ArialLocal", style="B" if bold else "", size=size)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(pdf.epw, height, safe(text), new_x="LMARGIN", new_y="NEXT")


def bullets(pdf: ReadmePDF, items: list[str]) -> None:
    for item in items:
        put(pdf, "- " + item, size=10.5, height=5.4)


def write_case(
    pasta: Path,
    titulo: str,
    subtitulo: str,
    fazer: list[str],
    jornada: list[str],
    funcionalidade: list[str],
    dados: list[str],
    regra: str,
    abrir: str,
) -> Path:
    pdf = ReadmePDF(titulo)
    pdf.add_page()
    pdf.set_fill_color(18, 35, 63)
    pdf.rect(0, 0, 210, 38, "F")
    pdf.set_text_color(185, 213, 234)
    pdf.set_font("ArialLocal", size=11)
    pdf.set_xy(18, 10)
    pdf.cell(0, 6, "Cases Alunos")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("ArialLocal", style="B", size=18)
    pdf.set_xy(18, 18)
    pdf.cell(0, 9, safe(titulo))
    pdf.set_xy(18, 28)
    pdf.set_font("ArialLocal", size=11)
    pdf.cell(0, 6, safe(subtitulo))
    pdf.set_y(46)

    put(pdf, "O que vamos fazer", size=13, bold=True, height=7)
    bullets(pdf, fazer)
    pdf.ln(2)
    put(pdf, "Jornada", size=13, bold=True, height=7)
    bullets(pdf, jornada)
    pdf.ln(2)
    put(pdf, "Funcionalidade final", size=13, bold=True, height=7)
    bullets(pdf, funcionalidade)
    pdf.ln(2)
    put(pdf, "Dados de entrada", size=13, bold=True, height=7)
    bullets(pdf, dados)
    pdf.ln(2)
    put(pdf, "Como abrir o produto", size=13, bold=True, height=7)
    put(pdf, "Na pasta deste case, rode:", size=10.5)
    put(pdf, "python scripts/abrir_produto.py", size=10.5, bold=True)
    put(pdf, "Endereço: " + abrir, size=10.5, bold=True)
    put(pdf, "Não use file://. Deixe a janela aberta e encerre com Ctrl+C.", size=10.5)
    pdf.ln(2)
    put(pdf, "Regra de ouro", size=13, bold=True, height=7)
    put(pdf, regra, height=5.8)

    destino = pasta / "README.pdf"
    pasta.mkdir(parents=True, exist_ok=True)
    pdf.output(str(destino))
    return destino


def main() -> None:
    if not FONT.exists() or not FONT_BOLD.exists():
        raise SystemExit("Fontes Arial não encontradas em C:\\Windows\\Fonts.")

    gerados = [
        write_case(
            ROOT / "Inteligencia do Portal - Case 01",
            "Inteligência do Portal — Caso 01",
            "Workspace local de inteligência editorial. Dados sintéticos.",
            [
                "Limpar audiência, conteúdos, busca, auditoria e amostra de IA.",
                "Calcular KPIs, mix de editoria, CTR, posição e share da amostra.",
                "Comparar com metas só dentro da vigência.",
                "Gerar evidências com fonte, fórmula e limitação.",
                "Priorizar oportunidades e persistir o backlog.",
                "Recusar market share universal de IA e causalidade sem prova.",
            ],
            [
                "00 — regras do portal fictício.",
                "01 — Silver, com duplicatas e linhas inválidas isoladas.",
                "02 — Gold e livro de evidências.",
                "03 — backlog de oportunidades.",
                "04 — contrato do workspace.",
                "05 — produto local e abertura no browser.",
                "06 — red team e 07 — juiz.",
            ],
            [
                "Visão executiva com KPIs e metas do período.",
                "Telas de audiência, busca, benchmark e visibilidade em IA.",
                "Abrir evidência com fonte, fórmula e limitação.",
                "Kanban de oportunidades com papel, status e nota.",
                "Persistência no navegador e exportação JSON, CSV e Markdown.",
                "Importação local com bloqueio de PII e arquivo inválido.",
            ],
            [
                "audiencia_portal.csv",
                "conteudos.csv",
                "search_console.csv",
                "auditoria_sites.csv",
                "visibilidade_ia.csv",
                "metas.csv",
            ],
            "O produto afirma o que os dados mostram. Sem prova causal, escreve sem evidencia causal.",
            "http://127.0.0.1:8766/index.html",
        ),
        write_case(
            ROOT / "Mesa de Discovery - Case 02",
            "Mesa de Discovery — Caso 02",
            "Workspace local de requisitos rastreáveis. Dados sintéticos.",
            [
                "Limpar reuniões, evidências, stakeholders, sistemas, restrições e ideias.",
                "Isolar duplicata, reunião sem data e texto adversário (E99 não é comando).",
                "Extrair requisitos somente com evidencia_id.",
                "Deixar conflitos, perguntas abertas e fora de escopo visíveis.",
                "Não inventar o oitavo requisito do MVP nem prazo oficial.",
                "Aprovar por papel, nunca por nome de pessoa.",
            ],
            [
                "00 — regras de discovery e rastreabilidade.",
                "01 — Silver das atas e cadastros.",
                "02 — requisitos, conflitos, perguntas e evidências.",
                "03 — backlog aprovável.",
                "04 — contrato da mesa.",
                "05 — produto local e abertura no browser.",
                "06 — red team e 07 — juiz.",
            ],
            [
                "Catálogo de evidências filtrável por tipo.",
                "Tabela de requisitos com fonte e aprovador.",
                "Conflito de prazo e itens fora de escopo à mostra.",
                "Perguntas abertas (aprovador e risco jurídico).",
                "Kanban de aprovação persistente.",
                "Exportação da matriz de rastreabilidade.",
            ],
            [
                "reunioes.csv",
                "evidencias.csv",
                "stakeholders.csv",
                "sistemas.csv",
                "restricoes.csv",
                "ideias.csv",
                "metas.csv",
            ],
            "Sem evidencia_id não existe requisito. Completar a meta de 8 com invenção é falha crítica.",
            "http://127.0.0.1:8767/index.html",
        ),
        write_case(
            ROOT / "Radar Saude do Cliente - Case 03",
            "Radar de Saúde do Cliente — Caso 03",
            "Mesa operacional de sinais. Não calcula probabilidade de churn.",
            [
                "Limpar clientes, projetos, eventos, tickets e NPS.",
                "Isolar duplicata, segmento TESTE, atraso negativo e SLA n/a.",
                "Montar score como soma de flags (atraso, ausência, ticket, SLA, NPS, inativo).",
                "Manter churn como sem evidencia: não há data_saida nem histórico.",
                "Abrir planos de ação com papéis, sem pedir cancelamento sem prova.",
                "Bloquear rótulo de probabilidade de churn no produto.",
            ],
            [
                "00 — regras de sinal versus churn.",
                "01 — Silver da carteira.",
                "02 — sinais, KPIs e evidências.",
                "03 — planos de ação.",
                "04 — contrato da mesa operacional.",
                "05 — produto local e abertura no browser.",
                "06 — red team e 07 — juiz.",
            ],
            [
                "Visão executiva: clientes válidos, sinal alto, SLA e churn sem evidencia.",
                "Carteira filtrável por segmento e nível do sinal.",
                "Detalhe do cliente com flags e status.",
                "Matriz de sinais binários.",
                "Kanban de ações persistente.",
                "Importação local com bloqueio de PII e de churn inventado.",
            ],
            [
                "clientes.csv",
                "projetos.csv",
                "eventos.csv",
                "tickets.csv",
                "nps.csv",
                "metas.csv",
            ],
            "Sinal não é alerta, inativo não é churn. Sem data_saida, churn_clientes_pct é sem evidencia.",
            "http://127.0.0.1:8768/index.html",
        ),
    ]
    for path in gerados:
        print(path)


if __name__ == "__main__":
    main()
