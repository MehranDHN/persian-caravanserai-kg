#!/usr/bin/env python3
"""Idempotent ingest of approved MIFAO rows, plus a cross-source coverage table.

Reads:
  data/mifao-review-queue.csv
  data/mifao-evidence.csv
  docs/unesco-wikidata-comparison.csv  (UNESCO ∩ Wikidata)
  data/wikidata-raw.json               (all harvested Wikidata items)

Writes (always overwritten; same inputs → same bytes):
  data/mifao-accepted.ttl
  data/source-coverage.csv
  iiif/mifao/<slug>.manifest.json      (accepted rows with plan or photograph)

Only rows with review_status=accepted are turned into RDF. Candidate rows
never mint buildings. UNESCO and Wikidata IRIs are reused when the editor
has filled unesco_id / wikidata, so a common record is one individual with
several persarch:attestedBy statements.

  python scripts/ingest_mifao_accepted.py
  python scripts/ingest_mifao_accepted.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from harvest_unesco import COMPONENTS, slug as unesco_slug
from harvest_wikidata import bindings_to_records

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "mifao-review-queue.csv"
EVIDENCE = ROOT / "data" / "mifao-evidence.csv"
COMPARE = ROOT / "docs" / "unesco-wikidata-comparison.csv"
WD_JSON = ROOT / "data" / "wikidata-raw.json"
OUT_TTL = ROOT / "data" / "mifao-accepted.ttl"
OUT_COV = ROOT / "data" / "source-coverage.csv"
IIIF_DIR = ROOT / "iiif" / "mifao"

SOURCE_IRIS = {
    "MIFAO81": "source_mifao81",
    "MIFAO82": "source_mifao82",
    "UNESCO": "source_unesco",
    "Wikidata": "source_wikidata",
    "Wolfram": "source_wolfram",
}
KIND_IRI = {
    "page": "evidence_page",
    "figure": "evidence_figure",
    "plate": "evidence_plate",
    "index": "evidence_index",
    "itinerary": "evidence_itinerary",
    "map": "evidence_map",
}
TYPE_CLASS = {
    "caravanserai": "persarch:Caravanserai",
    "robat": "persarch:Caravanserai",
    "urban-caravanserai": "persarch:UrbanCaravanserai",
    "mountain": "persarch:MountainCaravanserai",
    "octagonal": "persarch:OctagonalCaravanserai",
    "circular": "persarch:CircularCaravanserai",
}

UNESCO_LOCAL = {cid: unesco_slug(name) for cid, name, *_ in COMPONENTS}


def ttl_escape(s: str) -> str:
    return (
        (s or "")
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("\r", " ")
    )


def local_token(text: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", text or "").strip("_")
    return token or "x"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def accepted_rows(queue: list[dict]) -> list[dict]:
    out = []
    for row in queue:
        status = (row.get("review_status") or "").strip().lower()
        if status == "accepted":
            out.append(row)
    return sorted(out, key=lambda r: r.get("working_id") or "")


def parse_source_ids(cell: str) -> list[str]:
    seen = []
    for part in re.split(r"[;|,]", cell or ""):
        token = part.strip().upper().replace(" ", "")
        if token in ("MIFAO81", "MIFO81"):
            token = "MIFAO81"
        elif token in ("MIFAO82", "MIFO82"):
            token = "MIFAO82"
        if token in SOURCE_IRIS and token not in seen:
            seen.append(token)
    return seen


def canonical(row: dict) -> tuple[str, str]:
    """Return (local_name, origin) for the building IRI."""
    uid = (row.get("unesco_id") or "").strip()
    qid = (row.get("wikidata") or "").strip()
    if qid and not qid.upper().startswith("Q"):
        qid = "Q" + qid
    if uid:
        local = UNESCO_LOCAL.get(uid)
        if local:
            return local, "unesco"
    if qid:
        return f"wd_{qid}", "wikidata"
    return "mifao_" + local_token(row.get("working_id") or "unknown"), "mifao"


def building_class(row: dict) -> str:
    return TYPE_CLASS.get((row.get("building_type") or "").strip().lower(), "persarch:Caravanserai")


def attested_sources(row: dict) -> list[str]:
    found = parse_source_ids(row.get("sources") or "")
    if (row.get("unesco_id") or "").strip() and "UNESCO" not in found:
        found.append("UNESCO")
    if (row.get("wikidata") or "").strip() and "Wikidata" not in found:
        found.append("Wikidata")
    order = ["UNESCO", "Wikidata", "MIFAO81", "MIFAO82", "Wolfram"]
    return [s for s in order if s in found]


def emit_attestation(att_id: str, local: str, ev: dict, n: int) -> list[str]:
    src = (ev.get("source_id") or "").strip().upper()
    if src in ("MIFO81",):
        src = "MIFAO81"
    if src in ("MIFO82",):
        src = "MIFAO82"
    src_iri = SOURCE_IRIS.get(src)
    kind = (ev.get("evidence_kind") or "page").strip().lower()
    kind_iri = KIND_IRI.get(kind, "evidence_page")
    locator = (ev.get("locator") or "").strip()
    detail = (ev.get("detail") or "").strip()
    ia = (ev.get("ia_item") or "").strip()
    source_name = (ev.get("source_name") or ev.get("source_short") or src).strip()
    lines = [
        f":{att_id} a persarch:SourceAttestation , crm:E73_Information_Object ;",
        f'    rdfs:label "{ttl_escape(source_name)} {ttl_escape(locator)}"@en ;',
        f"    persarch:attestationSource :{src_iri} ;" if src_iri else "    persarch:attestationSource :source_mifao81 ;",
        f"    persarch:documentsBuilding :{local} ;",
        f"    crm:P70_documents :{local} ;",
        f"    persarch:evidenceKind persarch:{kind_iri} ;",
        f'    persarch:locator "{ttl_escape(locator)}" ;',
        f'    persarch:mifaoReference "{ttl_escape(src + " " + locator)}" ;',
    ]
    if detail:
        lines.append(f'    dcterms:description "{ttl_escape(detail)}"@en ;')
    if ia:
        lines.append(f"    foaf:page <{ia}> ;")
    if kind == "figure":
        lines.append("    a persarch:PlanImage ;")
    elif kind == "plate":
        lines.append("    a persarch:Photograph ;")
    elif kind == "map":
        lines.append("    a persarch:MapImage ;")
    lines[-1] = lines[-1].rstrip(" ;") + " ."
    extra = []
    if kind == "figure":
        extra.append(f":{local} persarch:hasPlanPresentation :{att_id} .")
    elif kind == "plate":
        extra.append(f":{local} persarch:hasPhotographPresentation :{att_id} .")
    elif kind == "map":
        extra.append(f":{local} persarch:hasMapPresentation :{att_id} .")
    extra.append("")
    return lines + extra


def emit_building(row: dict, evidence: list[dict]) -> tuple[str, list[str], str]:
    local, origin = canonical(row)
    sources = attested_sources(row)
    source_iris = [f":{SOURCE_IRIS[s]}" for s in sources]
    source_set = "|".join(s.lower() if s not in ("MIFAO81", "MIFAO82") else s.lower() for s in sources)
    # keep mifao81/mifao82 as sourceId spelling
    source_set = "|".join(
        {"UNESCO": "unesco", "Wikidata": "wikidata", "MIFAO81": "mifao81", "MIFAO82": "mifao82", "Wolfram": "wolfram"}[s]
        for s in sources
    )
    klass = building_class(row)
    types = f"{klass} , persarch:Caravanserai , bot:Building , crmba:B1_Built_Work"
    if klass == "persarch:Caravanserai":
        types = "persarch:Caravanserai , bot:Building , crmba:B1_Built_Work"
    label_en = (row.get("normalized_en") or row.get("siroux_name") or row["working_id"]).strip()
    label_fa = (row.get("normalized_fa") or "").strip()
    siroux = (row.get("siroux_name") or "").strip()
    alt = (row.get("siroux_name_alt") or "").strip()
    period = (row.get("period_guess") or "").strip()
    notes = (row.get("notes") or "").strip()
    uid = (row.get("unesco_id") or "").strip()
    qid = (row.get("wikidata") or "").strip()
    if qid and not qid.upper().startswith("Q"):
        qid = "Q" + qid
    wid = (row.get("working_id") or "").strip()
    cover = (row.get("cover_evidence") or "").strip()
    site = (row.get("site_number") or "").strip()

    stmts = [
        f":{local} a {types} ;",
        f'    rdfs:label "{ttl_escape(label_en)}"@en ;',
    ]
    if label_fa:
        stmts.append(f'    rdfs:label "{ttl_escape(label_fa)}"@fa ;')
    if siroux and siroux != label_en:
        stmts.append(f'    skos:altLabel "{ttl_escape(siroux)}"@fr ;')
    for alias in [a.strip() for a in alt.split(";") if a.strip()]:
        if alias not in (label_en, siroux):
            stmts.append(f'    skos:altLabel "{ttl_escape(alias)}"@fr ;')
    stmts.append(f'    persarch:workingId "{ttl_escape(wid)}" ;')
    stmts.append('    persarch:reviewStatus "accepted" ;')
    if site:
        stmts.append(f'    rdfs:comment "Siroux site {ttl_escape(site)}."@en ;')
    if notes:
        stmts.append(f'    dcterms:description "{ttl_escape(notes)}"@en ;')
    if period:
        stmts.append(f'    dcterms:temporal "{ttl_escape(period)}" ;')
    if uid:
        stmts.append(f'    persarch:unescoComponentId "{ttl_escape(uid)}" ;')
        stmts.append("    persarch:isUnescoComponent true ;")
    else:
        stmts.append("    persarch:isUnescoComponent false ;")
    if qid:
        stmts.append(f"    skos:exactMatch wd:{qid} ;")
    if (row.get("building_type") or "").strip().lower() == "robat":
        stmts.append("    crm:P2_has_type persarch:type_ribat ;")
    if cover:
        stmts.append(f'    persarch:mifaoReference "{ttl_escape(cover)}" ;')
    for iri in source_iris:
        stmts.append(f"    persarch:attestedBy {iri} ;")
    stmts.append(f'    persarch:sourceSet "{source_set}" ;')
    stmts.append(f'    persarch:sourceCount "{len(sources)}"^^xsd:integer ;')
    has_media = (row.get("has_plan") or "").strip().lower() == "yes" or (
        row.get("has_photograph") or ""
    ).strip().lower() == "yes"
    slug = local.replace("_", "-")
    if has_media:
        manifest = f"https://w3id.org/persian-caravanserai-kg/iiif/mifao/{slug}/manifest.json"
        stmts.append(f"    persarch:hasIiifManifest <{manifest}> ;")
    att_ids = []
    by_building = [e for e in evidence if (e.get("working_id") or "").strip() == wid]
    by_building.sort(key=lambda e: (e.get("source_id") or "", e.get("evidence_kind") or "", e.get("locator") or ""))
    for i, ev in enumerate(by_building, start=1):
        att_ids.append(f"att_{local_token(wid)}_{i:03d}")
    for att_id in att_ids:
        stmts.append(f"    persarch:hasAttestation :{att_id} ;")
    stmts.append("    prov:wasGeneratedBy :Ingest_MIFAO_accepted .")

    blocks = ["\n".join(stmts), ""]
    for att_id, ev in zip(att_ids, by_building):
        blocks.extend(emit_attestation(att_id, local, ev, 0))
    if origin == "unesco" and qid:
        blocks.append(f":{local} skos:exactMatch wd:{qid} .")
        blocks.append("")
    return local, blocks, slug if has_media else ""


def write_manifest(slug: str, row: dict, sources: list[str]) -> dict:
    label = (row.get("normalized_en") or row.get("siroux_name") or row["working_id"]).strip()
    mid = f"https://w3id.org/persian-caravanserai-kg/iiif/mifao/{slug}/manifest.json"
    cover = (row.get("cover_evidence") or "").strip()
    return {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": mid,
        "type": "Manifest",
        "label": {"en": [label], "fa": [row.get("normalized_fa") or ""]},
        "summary": {
            "en": [
                "Canvases for plans, photographs, and maps will be added after "
                "visual review of the MIFAO plates. Cover evidence: " + cover
            ]
        },
        "metadata": [
            {"label": {"en": ["Sources"]}, "value": {"en": [", ".join(sources)]}},
            {"label": {"en": ["Working ID"]}, "value": {"en": [row.get("working_id", "")]}},
            {"label": {"en": ["UNESCO"]}, "value": {"en": [row.get("unesco_id") or ""]}},
            {"label": {"en": ["Wikidata"]}, "value": {"en": [row.get("wikidata") or ""]}},
            {"label": {"en": ["Has plan"]}, "value": {"en": [row.get("has_plan") or ""]}},
            {"label": {"en": ["Has photograph"]}, "value": {"en": [row.get("has_photograph") or ""]}},
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


def emit_ttl(rows: list[dict], evidence: list[dict]) -> tuple[str, list[tuple[str, dict, list[str]]]]:
    lines = [
        "@prefix :         <https://w3id.org/persian-caravanserai-kg#> .",
        "@prefix persarch: <https://w3id.org/persian-architecture#> .",
        "@prefix bot:      <https://w3id.org/bot#> .",
        "@prefix crm:      <http://www.cidoc-crm.org/cidoc-crm/> .",
        "@prefix crmba:    <http://www.cidoc-crm.org/extensions/crmba/> .",
        "@prefix skos:     <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dcterms:  <http://purl.org/dc/terms/> .",
        "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd:      <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix foaf:     <http://xmlns.com/foaf/0.1/> .",
        "@prefix prov:     <http://www.w3.org/ns/prov#> .",
        "@prefix wd:       <http://www.wikidata.org/entity/> .",
        "",
        "# Idempotent ingest of review_status=accepted rows from",
        "# data/mifao-review-queue.csv. Do not hand-edit; re-run the script.",
        "# Load with data/sources.ttl. Common records reuse UNESCO or Wikidata IRIs",
        "# and list every source on persarch:attestedBy / persarch:sourceSet.",
        "",
        f":Ingest_MIFAO_accepted a prov:Activity ;",
        f'    rdfs:label "Ingest of accepted MIFAO review-queue rows"@en ;',
        f"    prov:used :source_mifao81 , :source_mifao82 ;",
        f'    dcterms:description "{len(rows)} accepted buildings."@en .',
        "",
    ]
    manifests: list[tuple[str, dict, list[str]]] = []
    if not rows:
        lines.append("# No accepted rows. Set review_status=accepted, fill unesco_id/wikidata if known, re-run.")
        lines.append("")
        return "\n".join(lines), manifests

    seen_locals = set()
    for row in rows:
        local, blocks, slug = emit_building(row, evidence)
        if local in seen_locals:
            lines.append(f"# NOTE: {row.get('working_id')} reuses :{local} (common record).")
        seen_locals.add(local)
        lines.extend(blocks)
        if slug:
            manifests.append((slug, row, attested_sources(row)))
    return "\n".join(lines), manifests


def load_wikidata_index() -> dict[str, dict]:
    if not WD_JSON.exists():
        return {}
    data = json.loads(WD_JSON.read_text(encoding="utf-8"))
    bindings = data.get("results", {}).get("bindings", [])
    records = bindings_to_records(bindings)
    return {rec["qid"]: rec for rec in records.values() if rec["qid"] != "Q66030932"}


def coverage_rows(accepted: list[dict], evidence: list[dict]) -> list[dict]:
    compare = read_csv(COMPARE)
    wd_index = load_wikidata_index()
    records: dict[str, dict] = {}

    def ensure(key: str, **kwargs) -> dict:
        rec = records.setdefault(
            key,
            {
                "record_key": key,
                "canonical_iri": "",
                "label": "",
                "unesco_id": "",
                "wikidata": "",
                "mifao_working_id": "",
                "in_unesco": "no",
                "in_wikidata": "no",
                "in_mifao81": "no",
                "in_mifao82": "no",
                "in_wolfram": "no",
                "source_count": "0",
                "sources": "",
                "overlap_note": "",
            },
        )
        for k, v in kwargs.items():
            if v:
                rec[k] = v
        return rec

    for row in compare:
        uid = row.get("unesco_id") or ""
        qid = row.get("qid") or ""
        local = UNESCO_LOCAL.get(uid, unesco_slug(row.get("unesco_name") or uid))
        rec = ensure(
            f"unesco:{uid}",
            canonical_iri=f"https://w3id.org/persian-caravanserai-kg#{local}",
            label=row.get("unesco_name") or row.get("wd_label") or "",
            unesco_id=uid,
            wikidata=qid,
        )
        rec["in_unesco"] = "yes"
        if qid:
            rec["in_wikidata"] = "yes"
            wd_index.pop(qid, None)

    for qid, rec_wd in wd_index.items():
        local = f"wd_{qid}"
        rec = ensure(
            f"wd:{qid}",
            canonical_iri=f"https://w3id.org/persian-caravanserai-kg#{local}",
            label=rec_wd.get("label_en") or qid,
            wikidata=qid,
        )
        rec["in_wikidata"] = "yes"
        if rec_wd.get("unesco") or any(str(h).startswith("1668-") for h in rec_wd.get("whs_ids") or []):
            rec["in_unesco"] = "yes"
            ids = sorted(h for h in rec_wd.get("whs_ids") or [] if str(h).startswith("1668-"))
            if ids:
                rec["unesco_id"] = ids[0]

    ev_by = defaultdict(list)
    for ev in evidence:
        ev_by[(ev.get("working_id") or "").strip()].append(ev)

    for row in accepted:
        uid = (row.get("unesco_id") or "").strip()
        qid = (row.get("wikidata") or "").strip()
        if qid and not qid.upper().startswith("Q"):
            qid = "Q" + qid
        local, origin = canonical(row)
        if uid:
            key = f"unesco:{uid}"
        elif qid:
            key = f"wd:{qid}"
        else:
            key = f"mifao:{row.get('working_id')}"
        rec = ensure(
            key,
            canonical_iri=f"https://w3id.org/persian-caravanserai-kg#{local}",
            label=(row.get("normalized_en") or row.get("siroux_name") or ""),
            unesco_id=uid,
            wikidata=qid,
            mifao_working_id=row.get("working_id") or "",
        )
        srcs = attested_sources(row)
        if "MIFAO81" in srcs:
            rec["in_mifao81"] = "yes"
        if "MIFAO82" in srcs:
            rec["in_mifao82"] = "yes"
        if "UNESCO" in srcs:
            rec["in_unesco"] = "yes"
        if "Wikidata" in srcs:
            rec["in_wikidata"] = "yes"
        if rec["mifao_working_id"] and row.get("working_id") not in rec["mifao_working_id"]:
            rec["mifao_working_id"] = rec["mifao_working_id"] + ";" + row["working_id"]

    flags = [
        ("in_unesco", "UNESCO"),
        ("in_wikidata", "Wikidata"),
        ("in_mifao81", "MIFAO81"),
        ("in_mifao82", "MIFAO82"),
        ("in_wolfram", "Wolfram"),
    ]
    out = []
    for rec in records.values():
        present = [name for flag, name in flags if rec[flag] == "yes"]
        rec["source_count"] = str(len(present))
        rec["sources"] = "|".join(present)
        if len(present) >= 2:
            rec["overlap_note"] = "common in " + " + ".join(present)
        else:
            rec["overlap_note"] = "single source"
        out.append(rec)
    out.sort(key=lambda r: (-int(r["source_count"]), r["record_key"]))
    return out


COV_FIELDS = [
    "record_key",
    "canonical_iri",
    "label",
    "unesco_id",
    "wikidata",
    "mifao_working_id",
    "in_unesco",
    "in_wikidata",
    "in_mifao81",
    "in_mifao82",
    "in_wolfram",
    "source_count",
    "sources",
    "overlap_note",
]


def write_coverage(rows: list[dict]) -> None:
    with OUT_COV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COV_FIELDS)
        w.writeheader()
        for rec in rows:
            w.writerow({k: rec.get(k, "") for k in COV_FIELDS})


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print counts; do not write files.")
    args = parser.parse_args(argv)

    queue = read_csv(QUEUE)
    evidence = read_csv(EVIDENCE)
    accepted = accepted_rows(queue)
    ttl, manifests = emit_ttl(accepted, evidence)
    coverage = coverage_rows(accepted, evidence)
    overlap = sum(1 for r in coverage if int(r["source_count"]) >= 2)

    print(f"Queue rows: {len(queue)}")
    print(f"Accepted:   {len(accepted)}")
    print(f"Evidence:   {len(evidence)}")
    print(f"Coverage:   {len(coverage)} records, {overlap} in two or more sources")
    print(f"Wolfram:    declared, harvestStatus=not-included (0 rows)")

    if args.dry_run:
        print("Dry run: no files written.")
        return 0

    OUT_TTL.write_text(ttl if ttl.endswith("\n") else ttl + "\n", encoding="utf-8")
    write_coverage(coverage)
    print(f"Wrote {OUT_TTL}")
    print(f"Wrote {OUT_COV}")

    IIIF_DIR.mkdir(parents=True, exist_ok=True)
    wanted = set()
    for slug, row, sources in manifests:
        path = IIIF_DIR / f"{slug}.manifest.json"
        path.write_text(json.dumps(write_manifest(slug, row, sources), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        wanted.add(path.name)
        print(f"Wrote {path}")
    if IIIF_DIR.exists():
        for stale in IIIF_DIR.glob("*.manifest.json"):
            if stale.name not in wanted:
                stale.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
