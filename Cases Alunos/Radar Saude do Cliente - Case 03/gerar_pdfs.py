from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF


ROOT = Path(__file__).resolve().parent
MD_DIR = ROOT / "prompts" / "md"
PDF_DIR = ROOT / "prompts" / "pdf"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


class PromptPDF(FPDF):
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
        self.multi_cell(self.epw, 5, self.document_title)
        self.set_draw_color(190, 190, 190)
        self.line(18, self.get_y(), 192, self.get_y())
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("ArialLocal", size=8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, str(self.page_no()), align="C")


def clean(text: str) -> str:
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("**", "")
        .replace("`", "")
    )


def put(
    pdf: PromptPDF,
    text: str,
    *,
    size: float = 11,
    bold: bool = False,
    height: float = 5.6,
    fill: bool = False,
) -> None:
    pdf.set_font("ArialLocal", style="B" if bold else "", size=size)
    pdf.multi_cell(
        pdf.epw,
        height,
        clean(text) if text else " ",
        fill=fill,
        new_x="LMARGIN",
        new_y="NEXT",
    )


def render_markdown(pdf: PromptPDF, markdown_text: str) -> None:
    lines = markdown_text.replace("\r\n", "\n").splitlines()
    is_code = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            is_code = not is_code
            continue
        if not stripped:
            pdf.ln(2)
            continue
        if is_code:
            pdf.set_fill_color(244, 246, 248)
            put(pdf, line, size=9, height=5, fill=True)
            continue
        if stripped.startswith("# INÍCIO DO PROMPT"):
            pdf.ln(2)
            pdf.set_fill_color(223, 240, 252)
            put(pdf, stripped.lstrip("# "), size=12, bold=True, height=7, fill=True)
            pdf.ln(2)
            continue
        if stripped.startswith("# FIM DO PROMPT"):
            pdf.ln(2)
            pdf.set_fill_color(223, 240, 252)
            put(pdf, stripped.lstrip("# "), size=12, bold=True, height=7, fill=True)
            pdf.ln(2)
            continue
        if line.startswith("# "):
            pdf.ln(2)
            put(pdf, line[2:], size=15, bold=True, height=7)
            continue
        if line.startswith("## "):
            pdf.ln(3)
            put(pdf, line[3:], size=12, bold=True, height=6.5)
            continue
        if line.startswith("### "):
            pdf.ln(2)
            put(pdf, line[4:], size=11, bold=True, height=6)
            continue
        if line.startswith("|"):
            put(pdf, line, size=9, height=5.2)
            continue
        if line.startswith("- "):
            put(pdf, "- " + line[2:], size=10.5)
            continue
        put(pdf, line, size=10.5)


def write_pdf(markdown_paths: list[Path], destination: Path, title: str) -> None:
    pdf = PromptPDF(title)
    pdf.add_page()
    put(pdf, title, size=16, bold=True, height=8)
    put(
        pdf,
        "As paginas GUIA DO ALUNO nao devem ser coladas. Copie somente o trecho entre INICIO DO PROMPT e FIM DO PROMPT.",
        size=10,
        bold=True,
        height=5.5,
    )
    pdf.ln(4)

    for index, markdown_path in enumerate(markdown_paths):
        if index:
            pdf.add_page()
        put(pdf, markdown_path.name, size=12, bold=True, height=7)
        pdf.ln(2)
        render_markdown(pdf, markdown_path.read_text(encoding="utf-8"))

    destination.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(destination))


def main() -> None:
    if not FONT.exists() or not FONT_BOLD.exists():
        raise SystemExit("Fontes Arial não encontradas em C:\\Windows\\Fonts.")

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    markdown_paths = sorted(MD_DIR.glob("*.md"))
    prompt_paths = [
        path for path in markdown_paths if re.match(r"^\d{2}_", path.name)
    ]

    for markdown_path in markdown_paths:
        write_pdf(
            [markdown_path],
            PDF_DIR / f"{markdown_path.stem}.pdf",
            f"Radar de Saúde do Cliente - {markdown_path.stem}",
        )

    write_pdf(
        prompt_paths,
        PDF_DIR / "Prompts_Completo.pdf",
        "Radar de Saúde do Cliente - Prompts completos",
    )
    print(f"PDFs gerados: {len(markdown_paths) + 1}")


if __name__ == "__main__":
    main()
