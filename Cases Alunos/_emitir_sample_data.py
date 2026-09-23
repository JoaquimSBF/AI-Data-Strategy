from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_js(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "window.SAMPLE_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


def discovery() -> None:
    base = ROOT / "Discovery Workbench - Case 02"
    gold = base / "outputs" / "gold"
    write_js(
        base / "produto" / "sample-data.js",
        {
            "evidencias": json.loads((gold / "evidencias.json").read_text(encoding="utf-8")),
            "atas": read_csv(gold.parent / "silver" / "evidencias.csv"),
            "requisitos": read_csv(gold / "requisitos.csv"),
            "conflitos": read_csv(gold / "conflitos.csv"),
            "perguntas": read_csv(gold / "perguntas_abertas.csv"),
            "fora": read_csv(gold / "fora_de_escopo.csv"),
            "metas": read_csv(gold / "metas_status.csv"),
            "oportunidades": json.loads((base / "outputs" / "03_oportunidades.json").read_text(encoding="utf-8")),
        },
    )


def health() -> None:
    base = ROOT / "Client Health Radar - Case 03"
    gold = base / "outputs" / "gold"
    write_js(
        base / "produto" / "sample-data.js",
        {
            "evidencias": json.loads((gold / "evidencias.json").read_text(encoding="utf-8")),
            "sinais": read_csv(gold / "sinais_cliente.csv"),
            "kpis": read_csv(gold / "kpis_carteira.csv"),
            "metas": read_csv(gold / "metas_status.csv"),
            "oportunidades": json.loads((base / "outputs" / "03_oportunidades.json").read_text(encoding="utf-8")),
        },
    )


if __name__ == "__main__":
    discovery()
    health()
    print("sample-data gerado")
