"""Gera PDFs no estilo Allura (texto completo, sem corte) e organiza prompts/md + prompts/pdf."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONTB = Path(r"C:\Windows\Fonts\arialbd.ttf")

CASES = [
    ROOT / "CSOps Reunioes - Juliana Caballero",
    ROOT / "Landing de Dados - Eduardo Campregher",
    ROOT / "Risco de Churn - Sayuri Yamabe",
    ROOT / "Orcado vs Realizado - Meliy Toda",
]


class PDF(FPDF):
    def __init__(self, heading: str) -> None:
        super().__init__(format="A4")
        self.heading = heading
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("A", fname=str(FONT))
        self.add_font("A", style="B", fname=str(FONTB))
        self.set_margins(18, 16, 18)

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("A", size=8)
        self.set_text_color(90, 90, 90)
        self.multi_cell(self.epw, 5, self.heading, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(180, 180, 180)
        y = self.get_y()
        self.line(18, y, 192, y)
        self.ln(4)
        self.set_text_color(20, 20, 20)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("A", size=8)
        self.set_text_color(120, 120, 120)
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


def put(pdf: PDF, text: str, size: float = 11, bold: bool = False, h: float | None = None) -> None:
    pdf.set_font("A", style="B" if bold else "", size=size)
    pdf.multi_cell(
        pdf.epw,
        h or (size * 0.5),
        clean(text) if text else " ",
        new_x="LMARGIN",
        new_y="NEXT",
    )


def parse_blocks(md: str) -> list[tuple[str, object]]:
    """Devolve blocos (kind, payload) para nao perder linha nem tabela."""
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[tuple[str, object]] = []
    i = 0
    in_code = False
    code: list[str] = []
    while i < len(lines):
        line = lines[i].rstrip()
        if line.strip().startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code)))
                code = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue
        if line.startswith("|"):
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw = lines[i].strip()
                inner = raw.replace("|", "").replace(" ", "").replace(":", "")
                i += 1
                if inner and set(inner) <= set("-"):
                    continue
                cells = [clean(c.strip()) for c in raw.strip("|").split("|")]
                rows.append(cells)
            if rows:
                blocks.append(("table", rows))
            continue
        if not line.strip():
            blocks.append(("gap", None))
            i += 1
            continue
        if line.startswith("# "):
            blocks.append(("h1", line[2:]))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:]))
        elif line.startswith("### "):
            blocks.append(("h3", line[4:]))
        elif line.startswith("- "):
            blocks.append(("li", line[2:]))
        elif re.match(r"^\d+[\.\)]\s", line):
            blocks.append(("p", line))
        else:
            blocks.append(("p", line))
        i += 1
    if code:
        blocks.append(("code", "\n".join(code)))
    return blocks


def render_md(pdf: PDF, md: str, *, skip_first_h1: bool = False) -> None:
    first_h1 = True
    for kind, payload in parse_blocks(md):
        if kind == "gap":
            pdf.ln(2)
        elif kind == "h1":
            if skip_first_h1 and first_h1:
                first_h1 = False
                put(pdf, str(payload), size=14, bold=True, h=7)
                pdf.ln(1)
                continue
            pdf.ln(2)
            put(pdf, str(payload), size=14, bold=True, h=7)
            pdf.ln(1)
        elif kind == "h2":
            pdf.ln(3)
            put(pdf, str(payload), size=12, bold=True, h=6.5)
            pdf.ln(1)
        elif kind == "h3":
            put(pdf, str(payload), size=11, bold=True, h=6)
        elif kind == "li":
            put(pdf, "- " + str(payload), size=11, h=5.6)
        elif kind == "code":
            pdf.set_fill_color(245, 245, 242)
            for cl in str(payload).split("\n") or [" "]:
                pdf.set_font("A", size=9)
                pdf.multi_cell(pdf.epw, 5, clean(cl) or " ", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif kind == "table":
            rows: list[list[str]] = payload  # type: ignore[assignment]
            for r_i, row in enumerate(rows):
                line = "  |  ".join(row)
                put(pdf, line, size=9 if r_i == 0 else 10, bold=(r_i == 0), h=5.4)
            pdf.ln(1)
        else:
            put(pdf, str(payload), size=11, h=5.6)


def md_file_to_pdf(md_path: Path, pdf_path: Path, heading: str) -> None:
    pdf = PDF(heading)
    pdf.add_page()
    put(pdf, md_path.name, size=9, bold=False, h=5)
    pdf.ln(1)
    render_md(pdf, md_path.read_text(encoding="utf-8"))
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(pdf_path))


def completo_pdf(prompt_mds: list[Path], pdf_path: Path, case_name: str) -> None:
    pdf = PDF(f"{case_name} · Prompts")
    pdf.add_page()
    put(pdf, f"{case_name} · Prompts", size=16, bold=True, h=8)
    put(
        pdf,
        "Material para colar no Gemini / ChatGPT. Fonte editavel: pasta prompts/md",
        size=10,
        h=5.5,
    )
    pdf.ln(4)
    for p in prompt_mds:
        put(pdf, p.name, size=12, bold=True, h=7)
        pdf.ln(1)
        render_md(pdf, p.read_text(encoding="utf-8"), skip_first_h1=True)
        pdf.ln(6)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(pdf_path))


def reorganize(case: Path) -> Path:
    """Garante prompts/md e prompts/pdf. Devolve pasta md."""
    prompts = case / "prompts"
    md_dir = prompts / "md"
    pdf_dir = prompts / "pdf"
    md_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    old_pdf = case / "prompts_pdf"
    if old_pdf.exists():
        shutil.rmtree(old_pdf)

    for p in list(prompts.glob("*.md")):
        dest = md_dir / p.name
        if p.resolve() != dest.resolve():
            shutil.move(str(p), str(dest))

    for name in ("MAPA_ARQUIVOS.md", "COMO_FUNCIONA.md"):
        src = case / name
        if src.exists():
            shutil.move(str(src), str(md_dir / name))

    for name in ("MAPA_ARQUIVOS.pdf", "COMO_FUNCIONA.pdf"):
        src = case / name
        if src.exists():
            src.unlink()

    return md_dir


def main() -> None:
    if not FONT.exists():
        raise SystemExit("Arial nao encontrada.")

    md_to_completo = ROOT / "COMO_FUNCIONA.md"
    if md_to_completo.exists():
        md_file_to_pdf(md_to_completo, ROOT / "COMO_FUNCIONA.pdf", "Cases dos alunos · como funcionam os produtos")

    func = ROOT / "MAPA_FUNCIONALIDADE.md"
    if func.exists():
        md_file_to_pdf(func, ROOT / "MAPA_FUNCIONALIDADE.pdf", "Cases dos alunos · mapa de funcionabilidade")

    for case in CASES:
        md_dir = reorganize(case)
        pdf_dir = case / "prompts" / "pdf"
        for old in pdf_dir.glob("*.pdf"):
            old.unlink()

        prompt_mds = sorted(
            p for p in md_dir.glob("*.md") if p.name[:2].isdigit() or p.stem.startswith("0")
        )
        # 00_ a 05_
        prompt_mds = sorted([p for p in md_dir.glob("*.md") if re.match(r"^\d{2}_", p.name)])

        for p in md_dir.glob("*.md"):
            md_file_to_pdf(p, pdf_dir / f"{p.stem}.pdf", f"{case.name} · {p.stem}")

        if prompt_mds:
            completo_pdf(prompt_mds, pdf_dir / "Prompts_Completo.pdf", case.name)
        print("OK", case.name, "->", pdf_dir)


if __name__ == "__main__":
    main()
