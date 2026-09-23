from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTS = {".md", ".html", ".js", ".py"}
SKIP_NAMES = {"_titulos_pt.py", "_emitir_sample_data.py", "_gerar_prompts_novos_cases.py"}

PROTECT = [
    ("Portal Intelligence - Case 01", "@@P01@@"),
    ("Discovery Workbench - Case 02", "@@P02@@"),
    ("Client Health Radar - Case 03", "@@P03@@"),
]

TITLES = [
    ("Portal Intelligence", "Inteligência do Portal"),
    ("Discovery Workbench", "Mesa de Discovery"),
    ("Client Health Radar", "Radar de Saúde do Cliente"),
]

GRAMMAR = [
    ("construir o **Inteligência do Portal**", "construir a **Inteligência do Portal**"),
    ("construir o **Mesa de Discovery**", "construir a **Mesa de Discovery**"),
    ("Constituição do Inteligência do Portal", "Constituição da Inteligência do Portal"),
    ("Constituição do Mesa de Discovery", "Constituição da Mesa de Discovery"),
    ("Construir o Inteligência do Portal", "Construir a Inteligência do Portal"),
    ("Juiz final do Inteligência do Portal", "Juiz final da Inteligência do Portal"),
    ("como o Inteligência do Portal", "como a Inteligência do Portal"),
    ("O Inteligência do Portal é", "A Inteligência do Portal é"),
    ("do Inteligência do Portal", "da Inteligência do Portal"),
    ("do Mesa de Discovery", "da Mesa de Discovery"),
    ("Contrato do Mesa de Discovery", "Contrato da Mesa de Discovery"),
    (" — Case 01", " — Caso 01"),
    (" — Case 02", " — Caso 02"),
    (" — Case 03", " — Caso 03"),
]


def transform(text: str) -> str:
    for src, token in PROTECT:
        text = text.replace(src, token)
    for src, dst in TITLES:
        text = text.replace(src, dst)
    for src, dst in GRAMMAR:
        text = text.replace(src, dst)
    for src, token in PROTECT:
        text = text.replace(token, src)
    return text


def main() -> None:
    changed = 0
    folders = [
        ROOT / "Portal Intelligence - Case 01",
        ROOT / "Discovery Workbench - Case 02",
        ROOT / "Client Health Radar - Case 03",
    ]
    for folder in folders:
        for path in folder.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in EXTS:
                continue
            if path.name in SKIP_NAMES:
                continue
            original = path.read_text(encoding="utf-8")
            updated = transform(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                changed += 1
                print(path)
    print(f"arquivos alterados: {changed}")


if __name__ == "__main__":
    main()
