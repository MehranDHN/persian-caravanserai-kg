#!/usr/bin/env python3
"""Harvest Iranian caravanserais from Wikidata and emit Turtle aligned with persarch.

Sources:
  - instances of Q186347 (caravanserai) with country Iran (Q794)
  - parts of Q66030932 (The Persian Caravanserai / UNESCO 1668)

Usage:
  python harvest_wikidata.py
  python harvest_wikidata.py --out data/wikidata-iran-caravanserais.ttl
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests

ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = "persian-caravanserai-kg/0.2 (https://github.com/MehranDHN/persian-caravanserai-kg)"

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT_QUERY = ROOT / "queries" / "wikidata-harvest.rq"

NS_PCKG = "https://w3id.org/persian-caravanserai-kg#"
NS_PERSARCH = "https://w3id.org/persian-architecture#"
NS_BOT = "https://w3id.org/bot#"
NS_CRM = "http://www.cidoc-crm.org/cidoc-crm/"
NS_CRMBA = "http://www.cidoc-crm.org/extensions/crmba/"

FALLBACK_QUERY = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX bd: <http://www.bigdata.com/rdf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>

SELECT DISTINCT ?item ?itemLabel ?itemLabelFa ?itemDescription
       ?coord ?heritage ?heritageLabel ?admin ?adminLabel
       ?inception ?image ?unescoPart ?whsId ?natReg
       ?material ?materialLabel ?style ?styleLabel ?commons
WHERE {
  {
    ?item wdt:P31/wdt:P279* wd:Q186347 ;
          wdt:P17 wd:Q794 .
  } UNION {
    ?item wdt:P361 wd:Q66030932 .
  }
  OPTIONAL { ?item wdt:P625 ?coord . }
  OPTIONAL { ?item wdt:P1435 ?heritage . }
  OPTIONAL { ?item wdt:P131 ?admin . }
  OPTIONAL { ?item wdt:P571 ?inception . }
  OPTIONAL { ?item wdt:P18 ?image . }
  OPTIONAL { ?item wdt:P361 wd:Q66030932 . BIND(true AS ?unescoPart) }
  OPTIONAL { ?item wdt:P757 ?whsId . }
  OPTIONAL { ?item wdt:P1369 ?natReg . }
  OPTIONAL { ?item wdt:P186 ?material . }
  OPTIONAL { ?item wdt:P149 ?style . }
  OPTIONAL { ?item wdt:P373 ?commons . }
  OPTIONAL { ?item rdfs:label ?itemLabelFa FILTER(LANG(?itemLabelFa) = "fa") }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,fa". }
}
ORDER BY ?itemLabel
"""


def load_query(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return FALLBACK_QUERY


def harvest(query: str) -> dict:
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": USER_AGENT,
    }
    r = requests.get(ENDPOINT, params={"query": query}, headers=headers, timeout=120)
    r.raise_for_status()
    return r.json()


def qid(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]


def slug(label: str, fallback: str) -> str:
    text = (label or fallback).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text or fallback.lower()


def parse_wkt_point(coord: str):
    # Wikidata returns "Point(long lat)"
    m = re.search(r"Point\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", coord or "", re.I)
    if not m:
        return None
    lon, lat = m.group(1), m.group(2)
    return lon, lat


def ttl_escape(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .replace("\r", " ")
    )


def bindings_to_records(bindings: list) -> dict:
    records = {}
    for row in bindings:
        item = row["item"]["value"]
        rec = records.setdefault(
            item,
            {
                "uri": item,
                "qid": qid(item),
                "label_en": "",
                "label_fa": "",
                "description": "",
                "coord": None,
                "heritages": set(),
                "admins": set(),
                "inception": "",
                "opening": "",
                "image": "",
                "unesco": False,
                "instances": set(),
                "whs_ids": set(),
                "nat_regs": set(),
                "materials": set(),
                "styles": set(),
                "commons": "",
            },
        )
        rec["label_en"] = rec["label_en"] or row.get("itemLabel", {}).get("value", "")
        rec["label_fa"] = rec["label_fa"] or row.get("itemLabelFa", {}).get("value", "")
        rec["description"] = rec["description"] or row.get("itemDescription", {}).get("value", "")
        if "coord" in row:
            rec["coord"] = row["coord"]["value"]
        if "heritage" in row:
            rec["heritages"].add(row["heritage"]["value"])
        if "admin" in row:
            rec["admins"].add(row["admin"]["value"])
        if "inception" in row:
            rec["inception"] = rec["inception"] or row["inception"]["value"]
        if "opening" in row:
            rec["opening"] = rec["opening"] or row["opening"]["value"]
        if "instance" in row:
            rec["instances"].add(row["instance"]["value"])
        if "image" in row:
            rec["image"] = rec["image"] or row["image"]["value"]
        if row.get("unescoPart", {}).get("value") in ("true", "True", True):
            rec["unesco"] = True
        if "whsId" in row:
            rec["whs_ids"].add(row["whsId"]["value"])
        if "natReg" in row:
            rec["nat_regs"].add(row["natReg"]["value"])
        if "material" in row:
            rec["materials"].add(row["material"]["value"])
        if "style" in row:
            rec["styles"].add(row["style"]["value"])
        if "commons" in row:
            rec["commons"] = rec["commons"] or row["commons"]["value"]
    return records


def emit_turtle(records: dict) -> str:
    lines = [
        "@prefix : <https://w3id.org/persian-caravanserai-kg#> .",
        "@prefix persarch: <https://w3id.org/persian-architecture#> .",
        "@prefix bot: <https://w3id.org/bot#> .",
        "@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .",
        "@prefix crmba: <http://www.cidoc-crm.org/extensions/crmba/> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix geo: <http://www.opengis.net/ont/geosparql#> .",
        "@prefix wd: <http://www.wikidata.org/entity/> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix prov: <http://www.w3.org/ns/prov#> .",
        "",
        "# Auto-generated from Wikidata SPARQL. Do not hand-edit;",
        "# refine instances in data/case-studies/ and re-harvest to refresh this file.",
        "",
        f":Harvest_Wikidata_Iran_Caravanserais a prov:Activity ;",
        f'    rdfs:label "Wikidata harvest of Iranian caravanserais"@en ;',
        f"    prov:used <https://query.wikidata.org/> ;",
        f"    dcterms:source wd:Q186347 , wd:Q66030932 .",
        "",
    ]

    for item, rec in sorted(records.items(), key=lambda kv: (kv[1]["label_en"] or kv[1]["qid"]).lower()):
        if rec["qid"] == "Q66030932":
            continue
        local = f"wd_{rec['qid']}"
        labels = []
        if rec["label_en"]:
            labels.append(f'rdfs:label "{ttl_escape(rec["label_en"])}"@en')
        if rec["label_fa"] and rec["label_fa"] != rec["label_en"]:
            labels.append(f'rdfs:label "{ttl_escape(rec["label_fa"])}"@fa')
        stmts = [
            f":{local} a persarch:Caravanserai , bot:Building , crmba:B1_Built_Work ;",
        ]
        if labels:
            stmts[0] = stmts[0]
            for lab in labels:
                stmts.append(f"    {lab} ;")
        stmts.append(f"    skos:exactMatch wd:{rec['qid']} ;")
        stmts.append(f"    dcterms:source wd:{rec['qid']} ;")
        if rec["description"]:
            stmts.append(f'    dcterms:description "{ttl_escape(rec["description"])}"@en ;')
        whs = {h for h in rec["whs_ids"] if str(h).startswith("1668-")}
        is_unesco = rec["unesco"] or bool(whs)
        if is_unesco:
            stmts.append("    crm:P46i_forms_part_of :unesco_persian_caravanserai ;")
            stmts.append("    persarch:isUnescoComponent true ;")
        else:
            stmts.append("    persarch:isUnescoComponent false ;")
        for hid in sorted(rec["whs_ids"]):
            stmts.append(f'    persarch:unescoComponentId "{ttl_escape(hid)}" ;')
        for nr in sorted(rec["nat_regs"]):
            stmts.append(f'    persarch:nationalHeritageNumber "{ttl_escape(nr)}" ;')
        parsed = parse_wkt_point(rec["coord"] or "")
        if parsed:
            lon, lat = parsed
            stmts.append(f'    geo:asWKT "POINT({lon} {lat})"^^geo:wktLiteral ;')
            stmts.append(f"    crm:P53_has_former_or_current_location :place_{local} ;")
        if rec["image"]:
            stmts.append(f"    persarch:hasPresentation <{rec['image']}> ;")
        if rec["commons"]:
            commons_uri = "https://commons.wikimedia.org/wiki/Category:" + rec["commons"].replace(" ", "_")
            stmts.append(f"    dcterms:isPartOf <{commons_uri}> ;")
        stmts.append("    prov:wasGeneratedBy :Harvest_Wikidata_Iran_Caravanserais .")
        lines.append("\n".join(stmts))
        lines.append("")
        if parsed:
            lon, lat = parsed
            lines.append(f":place_{local} a crm:E53_Place ;")
            lines.append(f'    rdfs:label "Location of {ttl_escape(rec["label_en"] or rec["qid"])}"@en ;')
            lines.append(f'    geo:asWKT "POINT({lon} {lat})"^^geo:wktLiteral .')
            lines.append("")
        for admin in sorted(rec["admins"]):
            lines.append(f":{local} crm:P89_falls_within <{admin}> .")
        for h in sorted(rec["heritages"]):
            lines.append(f":{local} crm:P2_has_type <{h}> .")
        for m in sorted(rec["materials"]):
            lines.append(f":{local} crm:P45_consists_of <{m}> .")
        for s in sorted(rec["styles"]):
            lines.append(f":{local} crm:P2_has_type <{s}> .")
        if rec["admins"] or rec["heritages"] or rec["materials"] or rec["styles"]:
            lines.append("")

    lines.append(":unesco_persian_caravanserai a crm:E27_Site ;")
    lines.append('    rdfs:label "The Persian Caravanserai"@en ;')
    lines.append("    skos:exactMatch wd:Q66030932 ;")
    lines.append('    persarch:unescoListId "1668" ;')
    lines.append("    dcterms:source <https://whc.unesco.org/en/list/1668/> .")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", type=Path, default=DEFAULT_QUERY)
    parser.add_argument("--out", type=Path, default=ROOT / "data" / "wikidata-iran-caravanserais.ttl")
    parser.add_argument("--json-out", type=Path, default=ROOT / "data" / "wikidata-raw.json")
    parser.add_argument("--stdout-json", action="store_true")
    args = parser.parse_args(argv)

    query = load_query(args.query)
    data = harvest(query)
    bindings = data.get("results", {}).get("bindings", [])
    records = bindings_to_records(bindings)
    ttl = emit_turtle(records)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(ttl, encoding="utf-8")
    args.json_out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Harvested {len(records)} items from {len(bindings)} bindings.", file=sys.stderr)
    print(f"Wrote {args.out}", file=sys.stderr)
    print(f"Wrote {args.json_out}", file=sys.stderr)
    if args.stdout_json:
        print(json.dumps({"count": len(records), "items": [r["qid"] for r in records.values()]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
