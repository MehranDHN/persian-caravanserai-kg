#!/usr/bin/env python3
"""Placeholder IIIF Presentation API 3 manifests for the ten case studies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "iiif"

CASES = [
    ("ribat-sharaf", "Ribat-e Sharaf", "1668-005", "Plans and photographs of the dual-court Seljuk ribat."),
    ("deyr-e-gachin", "Deyr-e Gachin", "1668-001", "Plans, photographs, and historical views of Deyr-e Gachin."),
    ("sheikhali-khan", "Sheikhali Khan Caravanserai", "1668-012", "Documentation of Chaleh Siah / Sheikhali Khan."),
    ("maranjab", "Maranjab Caravanserai", "1668-013", "Desert four-iwan plan and photographs."),
    ("zeynoddin", "Zein-o-din Caravanserai", "1668-028", "Circular plan and adaptive-reuse photographs."),
    ("ganjali-khan", "Ganjali Khan Caravanserai", "1668-033", "Urban caravanserai in the Ganjali Khan complex."),
    ("izadkhast", "Izadkhast Caravanserai", "1668-031", "Cliff-edge setting, plans and photographs."),
    ("parand", "Parand Caravanserai", "1668-004", "Stone ribat (Robat Karim) plans and photographs."),
    ("qasr-e-bahram", "Qasr-e Bahram", "1668-024", "Stone Safavid caravanserai in the Kavir."),
    ("miandasht", "Miandasht Caravanserai", "1668-027", "Multi-court Safavid and Qajar complex."),
]


def manifest(slug: str, label: str, unesco: str, summary: str) -> dict:
    mid = f"https://w3id.org/persian-caravanserai-kg/iiif/{slug}/manifest.json"
    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": mid,
        "type": "Manifest",
        "label": {"en": [label], "fa": []},
        "summary": {
            "en": [
                f"{summary} UNESCO {unesco}. Canvases will be filled with MIFAO plates, "
                "Wikimedia photographs, and survey drawings. Linked from the RDF graph via persarch:hasIiifManifest."
            ]
        },
        "metadata": [
            {"label": {"en": ["UNESCO component"]}, "value": {"en": [unesco]}},
            {"label": {"en": ["Model"]}, "value": {"en": ["persarch:hasPresentation / persarch:PlanImage / persarch:Photograph"]}},
            {"label": {"en": ["Rights"]}, "value": {"en": ["Replace with the licence of each canvas"]}},
        ],
        "items": [],
        "seeAlso": [
            {
                "id": f"https://w3id.org/persian-caravanserai-kg#{slug.replace('-', '_')}",
                "type": "Dataset",
                "format": "text/turtle",
                "label": {"en": ["RDF record in persian-caravanserai-kg"]},
            }
        ],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for slug, label, unesco, summary in CASES:
        path = OUT / f"{slug}.manifest.json"
        data = manifest(slug, label, unesco, summary)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        index.append(slug)
        print(f"Wrote {path}")
    (OUT / "example-manifest.json").write_text(
        json.dumps(manifest("example", "Example Caravanserai", "1668-xxx", "Placeholder."), indent=2)
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
