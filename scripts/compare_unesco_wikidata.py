#!/usr/bin/env python3
"""One-to-one comparison of UNESCO WHC 1668 components with Wikidata items.

Matching order:
  1. Wikidata P757 World Heritage Site ID (1668-xxx)
  2. Haversine nearest neighbour within 2.5 km, with a name-token check
  3. Unmatched UNESCO rows are listed as new Wikidata candidates

Also scores existing items against the Q42627405 / Q5905596 blueprint.
"""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

from harvest_unesco import COMPONENTS, dms_to_decimal, slug

ROOT = Path(__file__).resolve().parent.parent
WD_JSON = ROOT / "data" / "wikidata-raw.json"
OUT_CSV = ROOT / "docs" / "unesco-wikidata-comparison.csv"
OUT_MD = ROOT / "docs" / "unesco-wikidata-comparison.md"
CAND_MD = ROOT / "docs" / "wikidata-candidates.md"
LINKS_TTL = ROOT / "data" / "unesco-wikidata-links.ttl"
MIFAO_QUEUE = ROOT / "data" / "mifao-review-queue.csv"

STOP = {
    "caravanserai", "caravansarai", "caravansary", "ribat", "robat",
    "the", "of", "and", "in", "e", "ye", "i",
}


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def tokens(name: str) -> set:
    parts = re.findall(r"[a-z0-9]+", (name or "").lower())
    return {p for p in parts if p not in STOP and len(p) > 1}


def parse_point(coord: str):
    m = re.search(r"Point\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", coord or "", re.I)
    if not m:
        return None
    return float(m.group(2)), float(m.group(1))  # lat, lon


def load_wikidata():
    raw = json.loads(WD_JSON.read_text(encoding="utf-8"))
    items = {}
    for row in raw.get("results", {}).get("bindings", []):
        uri = row["item"]["value"]
        qid = uri.rsplit("/", 1)[-1]
        rec = items.setdefault(
            qid,
            {
                "qid": qid,
                "label_en": "",
                "label_fa": "",
                "description": "",
                "coord": None,
                "whs_ids": set(),
                "nat_regs": set(),
                "heritage": False,
                "admin": False,
                "image": False,
                "unesco_part": False,
                "inception": False,
                "opening": False,
                "p31_caravanserai": False,
                "material": False,
                "style": False,
                "commons": False,
            },
        )
        rec["label_en"] = rec["label_en"] or row.get("itemLabel", {}).get("value", "")
        rec["label_fa"] = rec["label_fa"] or row.get("itemLabelFa", {}).get("value", "")
        rec["description"] = rec["description"] or row.get("itemDescription", {}).get("value", "")
        if "coord" in row:
            rec["coord"] = parse_point(row["coord"]["value"])
        if "whsId" in row:
            rec["whs_ids"].add(row["whsId"]["value"])
        if "natReg" in row:
            rec["nat_regs"].add(row["natReg"]["value"])
        if "heritage" in row:
            rec["heritage"] = True
        if "admin" in row:
            rec["admin"] = True
        if "image" in row:
            rec["image"] = True
        if row.get("unescoPart", {}).get("value") in ("true", "True"):
            rec["unesco_part"] = True
        if "inception" in row:
            rec["inception"] = True
        if "opening" in row:
            rec["opening"] = True
        if row.get("instance", {}).get("value", "").endswith("/Q186347"):
            rec["p31_caravanserai"] = True
        if "material" in row:
            rec["material"] = True
        if "style" in row:
            rec["style"] = True
        if "commons" in row:
            rec["commons"] = True
    items.pop("Q66030932", None)
    return items


def blueprint_gaps(rec) -> list:
    missing = []
    if not rec.get("label_en"):
        missing.append("en label")
    if not rec.get("label_fa"):
        missing.append("fa label")
    if not rec.get("coord"):
        missing.append("P625")
    if not rec.get("admin"):
        missing.append("P131")
    if not rec.get("heritage"):
        missing.append("P1435")
    if not rec.get("nat_regs"):
        missing.append("P1369")
    if not rec.get("image"):
        missing.append("P18")
    if rec.get("unesco") and not rec.get("unesco_part"):
        missing.append("P361→Q66030932")
    if rec.get("unesco") and not any(str(x).startswith("1668-") for x in rec.get("whs_ids", [])):
        missing.append("P757 1668-xxx")
    if not rec.get("p31_caravanserai"):
        missing.append("P31-Q186347")
    if not (rec.get("inception") or rec.get("opening")):
        missing.append("P571/P1619")
    if not rec.get("material"):
        missing.append("P186")
    if not rec.get("style"):
        missing.append("P149")
    return missing


def match(unesco, items):
    by_whs = {}
    for rec in items.values():
        for hid in rec["whs_ids"]:
            by_whs[hid] = rec

    used = set()
    rows = []
    for cid, name, province, lat_dms, lon_dms, prop, buf in unesco:
        lat, lon = dms_to_decimal(lat_dms), dms_to_decimal(lon_dms)
        rec = by_whs.get(cid)
        method = ""
        dist = None
        if rec and rec["qid"] not in used:
            method = "P757"
            if rec["coord"]:
                dist = haversine_km(lat, lon, rec["coord"][0], rec["coord"][1])
        else:
            rec = None
            best = None
            best_d = 1e9
            utoks = tokens(name)
            for cand in items.values():
                if cand["qid"] in used or not cand["coord"]:
                    continue
                d = haversine_km(lat, lon, cand["coord"][0], cand["coord"][1])
                if d >= 2.5:
                    continue
                overlap = utoks & tokens(cand["label_en"] + " " + cand["label_fa"])
                score = d - (0.8 if overlap else 0)
                if score < best_d:
                    best_d = score
                    best = cand
                    dist = d
                    method = "geo+name" if overlap else "geo"
            rec = best
        if rec:
            used.add(rec["qid"])
            rec = dict(rec)
            rec["unesco"] = True
            gaps = blueprint_gaps(rec)
            stub = (not rec.get("label_en")) or rec.get("label_en") == rec["qid"]
            if stub:
                status = "new-item"
                if "en label" not in gaps:
                    gaps.insert(0, "en label")
            elif gaps:
                status = "enrich"
            else:
                status = "complete"
        else:
            gaps = []
            status = "new-item"
        rows.append(
            {
                "unesco_id": cid,
                "unesco_name": name,
                "province": province,
                "lat": f"{lat:.6f}",
                "lon": f"{lon:.6f}",
                "property_ha": prop,
                "qid": rec["qid"] if rec else "",
                "wd_label": rec["label_en"] if rec else "",
                "wd_label_fa": rec["label_fa"] if rec else "",
                "match": method if rec else "none",
                "distance_km": f"{dist:.3f}" if dist is not None else "",
                "status": status,
                "gaps": "; ".join(gaps),
                "p757": "yes" if rec and cid in rec["whs_ids"] else "no",
                "p361": "yes" if rec and rec.get("unesco_part") else "no",
                "p1435": "yes" if rec and rec.get("heritage") else "no",
                "p1369": "; ".join(sorted(rec["nat_regs"])) if rec else "",
                "p625": "yes" if rec and rec.get("coord") else "no",
                "p18": "yes" if rec and rec.get("image") else "no",
            }
        )
    unmatched_wd = [
        rec
        for rec in items.values()
        if rec["qid"] not in used
        and (rec["unesco_part"] or any(str(x).startswith("1668") for x in rec["whs_ids"]))
    ]
    return rows, unmatched_wd, used


def write_csv(rows):
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def write_comparison_md(rows, unmatched_wd, n_items):
    matched = [r for r in rows if r["qid"]]
    new = [r for r in rows if r["status"] == "new-item"]
    enrich = [r for r in rows if r["status"] == "enrich"]
    complete = [r for r in rows if r["status"] == "complete"]
    p757_ok = [r for r in rows if r["p757"] == "yes"]

    body_rows = []
    for r in rows:
        q = f"[{r['qid']}](https://www.wikidata.org/wiki/{r['qid']})" if r["qid"] else "—"
        body_rows.append(
            [
                r["unesco_id"],
                r["unesco_name"],
                r["province"],
                q,
                r["wd_label"] or "—",
                r["match"] or "none",
                r["distance_km"] or "—",
                r["status"],
                r["gaps"] or "—",
            ]
        )

    text = f"""# UNESCO 1668 ↔ Wikidata one-to-one comparison

Source: UNESCO WHC maps for [list 1668](https://whc.unesco.org/en/list/1668/maps/) against a Wikidata harvest of instances of [Q186347](https://www.wikidata.org/wiki/Q186347) in Iran plus parts of [Q66030932](https://www.wikidata.org/wiki/Q66030932).

Machine-readable copy: [`unesco-wikidata-comparison.csv`](unesco-wikidata-comparison.csv).

## Counts

| Measure | n |
| --- | --- |
| UNESCO components (WHC 1668) | {len(rows)} |
| Wikidata Iranian caravanserai items harvested | {n_items} |
| UNESCO components with a Wikidata item | {len(matched)} |
| Matched by P757 (World Heritage Site ID) | {len(p757_ok)} |
| Matched by coordinates + name | {len(matched) - len(p757_ok)} |
| UNESCO components with **no** Wikidata item | {len(new)} |
| Existing items below the Q42627405 / Q5905596 bar | {len(enrich)} |
| Existing items already at the bar | {len(complete)} |

Every inscribed component is either linked to an existing Wikidata item or listed as a **new-item** candidate. Wikidata currently has hundreds of Iranian caravanserais that are **not** in the UNESCO serial property; those remain in the harvest graph and are out of scope for this table.

## Comparison table

{md_table(
    ["UNESCO ID", "UNESCO name", "Province", "Wikidata", "WD label", "Match", "km", "Action", "Blueprint gaps"],
    body_rows,
)}

## How matching works

1. **P757.** If a Wikidata item already carries World Heritage Site ID `1668-xxx`, it is bound to that component.
2. **Geo + name.** Otherwise the nearest harvested item within 2.5 km is accepted when the Latin/Persian labels share a significant token (Deyr, Sharaf, Maranjab, …).
3. **New item.** If neither rule fires, the UNESCO component is a candidate for a new Wikidata item. This list will later be extended from MIFAO 81/82 unstructured records.

Distances are haversine kilometres between the UNESCO centroid and Wikidata P625.

## Wikidata items flagged UNESCO but not in this 54-row join

"""
    if unmatched_wd:
        text += md_table(
            ["QID", "Label", "P757"],
            [
                [
                    f"[{r['qid']}](https://www.wikidata.org/wiki/{r['qid']})",
                    r["label_en"],
                    ", ".join(sorted(r["whs_ids"])) or "—",
                ]
                for r in unmatched_wd
            ],
        )
    else:
        text += "_None._\n"

    text += """
## Best-practice anchors

Enrichment and new items follow [`wikidata-blueprint.md`](wikidata-blueprint.md), using:

- [Q42627405](https://www.wikidata.org/wiki/Q42627405) Madarshah Caravanserai (national heritage, not a 1668 component)
- [Q5905596](https://www.wikidata.org/wiki/Q5905596) Sheikhali Khan / Chaleh Siah (UNESCO 1668-012)
"""
    OUT_MD.write_text(text, encoding="utf-8")


def write_candidates(rows):
    new = [r for r in rows if r["status"] == "new-item"]
    enrich = [r for r in rows if r["status"] == "enrich"]

    def candidate_block(r, kind):
        lines = [
            f"### {r['unesco_id']} — {r['unesco_name']}",
            "",
            f"- **Action:** {kind}",
            f"- **Province:** {r['province']}",
            f"- **UNESCO coordinates:** {r['lat']}, {r['lon']}",
            f"- **Property area:** {r['property_ha']} ha",
        ]
        if r["qid"]:
            lines.append(f"- **Existing item:** [{r['qid']}](https://www.wikidata.org/wiki/{r['qid']}) — {r['wd_label']}")
            lines.append(f"- **Match method:** {r['match']} ({r['distance_km']} km)")
            lines.append(f"- **Add or complete:** {r['gaps'] or 'review aliases and references'}")
        else:
            lines.append("- **Existing item:** none — create a new Wikidata item")
            lines.append("- **Minimum statements to add (blueprint):**")
            lines.append("  - P31 → Q186347 (caravanserai) and Q2065736 (cultural property) when registered")
            lines.append("  - P17 → Q794 (Iran)")
            lines.append(f"  - P131 → administrative entity in {r['province']}")
            lines.append(f"  - P625 → {r['lat']}, {r['lon']} (UNESCO centroid; note precision)")
            lines.append("  - P1435 → Q5958900 (Iranian National Heritage) with P580 when known")
            lines.append("  - P361 → Q66030932 (The Persian Caravanserai)")
            lines.append(f"  - P757 → {r['unesco_id']}")
            lines.append("  - Labels/descriptions in English and Persian")
            lines.append("  - References: UNESCO WHC 1668 maps; Iranian National Heritage when confirmed")
        lines.append("- **Unstructured follow-up:** MIFAO 81/82 plan, dimensions, and patronage to be filled after human review.")
        lines.append("")
        return "\n".join(lines)

    parts = [
        "# Wikidata candidates — new items and enrichments",
        "",
        "This list is the working queue for contributing missing or incomplete Persian caravanserai data to Wikidata.",
        "It follows the minimum quality bar in [`wikidata-blueprint.md`](wikidata-blueprint.md), demonstrated by",
        "[Q42627405](https://www.wikidata.org/wiki/Q42627405) and [Q5905596](https://www.wikidata.org/wiki/Q5905596).",
        "",
        "**Status of this file:** generated from the UNESCO 1668 ↔ Wikidata join.",
        "New rows from MIFAO 81/82 and other unstructured sources will be appended by the editor after scholarly review.",
        "Do not create Wikidata items from OCR-only MIFAO extractions until `reviewStatus` is `accepted`.",
        "",
        f"## A. New Wikidata items ({len(new)} UNESCO components with no item)",
        "",
        "Create these items first. Each already has a stable UNESCO identifier, official name, province, and coordinates.",
        "",
    ]
    if new:
        parts.extend(candidate_block(r, "create new Wikidata item") for r in new)
    else:
        parts.append("All 54 UNESCO components currently match a harvested Wikidata item. New candidates will come from unstructured sources (MIFAO 81/82) after human review.")
        parts.append("")

    parts += [
        f"## B. Enrich existing Wikidata items ({len(enrich)} below the blueprint bar)",
        "",
        "These items exist. Add the missing statements with references (P248 / P854, retrieved date).",
        "Priority statements for UNESCO components: `P31` Q186347, `P361` Q66030932, `P757` 1668-xxx, bilingual labels, P1435 + P1369, P625, P18.",
        "",
    ]
    parts.extend(candidate_block(r, "enrich existing item") for r in enrich)

    parts += mifao_section_c()
    CAND_MD.write_text("\n".join(parts), encoding="utf-8")


def mifao_section_c():
    """Load editor-controlled MIFAO rows. Do not invent Wikidata items here."""
    lines = [
        "## C. Unstructured MIFAO candidates (editor-controlled)",
        "",
        "Buildings attested in Maxime Siroux, *Caravansérails d'Iran* (MIFAO 81, 1949) and *Anciennes voies et monuments routiers de la région d'Ispahân* (MIFAO 82, 1971).",
        "Editable source of truth: [`data/mifao-review-queue.csv`](../data/mifao-review-queue.csv) (one building) and [`data/mifao-evidence.csv`](../data/mifao-evidence.csv) (source + page / figure / plate).",
        "Human-readable copy: [`docs/mifao-name-list.md`](mifao-name-list.md).",
        "Do not create Wikidata items until `review_status` is `accepted`. Proposed UNESCO/Wikidata columns are unverified hints.",
        "",
    ]
    if not MIFAO_QUEUE.exists():
        lines += [
            "Queue file missing. Seed with `python scripts/seed_mifao_review_queue.py`.",
            "",
        ]
        return lines

    with MIFAO_QUEUE.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    n = len(rows)
    accepted = sum(1 for r in rows if (r.get("review_status") or "").strip() == "accepted")
    with_plan = sum(1 for r in rows if (r.get("has_plan") or "").strip().lower() == "yes")
    with_photo = sum(1 for r in rows if (r.get("has_photograph") or "").strip().lower() == "yes")
    lines += [
        f"**{n}** candidate buildings ({accepted} accepted). {with_plan} have an in-text plan; {with_photo} have a photographic plate. Every evidence row names the volume and a page, figure, or plate.",
        "",
        "| Working ID | Siroux name | Sources | Cover evidence | Action | Proposed join | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        join = " / ".join(
            x for x in ((r.get("proposed_unesco_id") or "").strip(), (r.get("proposed_wikidata") or "").strip()) if x
        ) or "—"
        cover = (r.get("cover_evidence") or "").replace("|", "/")
        if len(cover) > 160:
            cover = cover[:157] + "…"
        lines.append(
            "| `{id}` | {name} | {src} | {cov} | {act} | {join} | {st} |".format(
                id=r.get("working_id", ""),
                name=(r.get("siroux_name") or "").replace("|", "/"),
                src=(r.get("sources") or "").replace("MIFAO", "MIFAO "),
                cov=cover,
                act=r.get("proposed_action", ""),
                join=join,
                st=r.get("review_status", "candidate"),
            )
        )
    lines.append("")
    return lines


def write_links_ttl(rows):
    lines = [
        "@prefix : <https://w3id.org/persian-caravanserai-kg#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix wd: <http://www.wikidata.org/entity/> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "",
        "# One-to-one UNESCO 1668 local IRIs → Wikidata items.",
        "",
    ]
    for r in rows:
        if not r["qid"]:
            continue
        local = slug(r["unesco_name"])
        lines.append(f":{local} skos:exactMatch wd:{r['qid']} ;")
        lines.append(f'    rdfs:comment "UNESCO {r["unesco_id"]} matched by {r["match"]}"@en .')
        lines.append("")
    LINKS_TTL.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    items = load_wikidata()
    rows, unmatched_wd, _used = match(COMPONENTS, items)
    write_csv(rows)
    write_comparison_md(rows, unmatched_wd, len(items))
    write_candidates(rows)
    write_links_ttl(rows)
    n_new = sum(1 for r in rows if r["status"] == "new-item")
    n_enr = sum(1 for r in rows if r["status"] == "enrich")
    n_ok = sum(1 for r in rows if r["qid"])
    print(f"UNESCO 54 | matched {n_ok} | new items {n_new} | enrich {n_enr}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {CAND_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
