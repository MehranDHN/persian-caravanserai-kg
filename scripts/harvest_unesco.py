#!/usr/bin/env python3
"""Emit Turtle for the 54 UNESCO WHC 1668 components.

Coordinates, property areas, and buffer zones come from
https://whc.unesco.org/en/list/1668/maps/ (retrieved 2026-03-30).
Province attributions follow the Wikipedia list of The Persian Caravanserai.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# id, unesco_name, province, lat_dms, lon_dms, property_ha, buffer_ha
COMPONENTS = [
    ("1668-001", "Deyr-e Gachin", "Qom", "N35 3 30.07", "E51 25 12.49", 1.9, 237.1),
    ("1668-002", "Noushirvan", "Semnan", "N35 46 14.63", "E53 43 56.54", 0.64, 99.79),
    ("1668-003", "Ahovan", "Semnan", "N35 46 13.94", "E53 43 48.52", 0.69, None),
    ("1668-004", "Parand", "Tehran", "N35 27 29.62", "E50 58 28.55", 0.4, 45.09),
    ("1668-005", "Robat-e Sharaf", "Razavi Khorasan", "N36 15 59.65", "E60 39 18.58", 1.12, 82.16),
    ("1668-006", "Anjireh Ajori", "Yazd", "N32 9 11.68", "E54 28 37.59", 1.76, 275.74),
    ("1668-007", "Anjireh Sangi", "Yazd", "N32 9 43.96", "E54 29 2.54", 0.09, None),
    ("1668-008", "Abbas Abad Taybad", "Razavi Khorasan", "N34 59 45.37", "E60 43 6.12", 0.41, 150.33),
    ("1668-009", "Jamal Abad", "East Azerbaijan", "N37 16 18.89", "E47 50 35.16", 0.37, 13.83),
    ("1668-010", "Qelli", "North Khorasan", "N37 9 11.86", "E56 55 14.67", 0.2, 83.71),
    ("1668-011", "Fakhr-e Davud", "Razavi Khorasan", "N35 59 59.59", "E59 18 48.55", 0.16, 10.09),
    ("1668-012", "Sheikhali Khan", "Isfahan", "N32 52 5.37", "E51 22 13.45", 0.82, 15.46),
    ("1668-013", "Maranjab", "Isfahan", "N34 17 56.89", "E51 48 44.59", 0.46, 226.33),
    ("1668-014", "Amin Abad", "Isfahan", "N31 40 21.7", "E52 4 6.41", 0.4, 5.23),
    ("1668-015", "Gabr Abad", "Isfahan", "N33 46 6.96", "E51 29 22.29", 0.44, 71.13),
    ("1668-016", "Mahyar", "Isfahan", "N32 15 54.06", "E51 48 35.04", 0.92, 76.45),
    ("1668-017", "Gaz", "Isfahan", "N32 48 33.69", "E51 36 33.56", 0.9, 20.36),
    ("1668-018", "Kuhpayeh", "Isfahan", "N32 42 48.35", "E52 26 8.83", 0.61, 6.74),
    ("1668-019", "Mazinan", "Razavi Khorasan", "N36 18 28.36", "E56 48 23.19", 0.47, 22.21),
    ("1668-020", "Mehr", "Razavi Khorasan", "N36 17 4.53", "E57 8 36.97", 0.57, 67.05),
    ("1668-021", "Zaferaniyeh", "Razavi Khorasan", "N36 9 56.59", "E58 5 10.43", 0.63, 29.79),
    ("1668-022", "Fakhr Abad", "Razavi Khorasan", "N34 44 40.69", "E58 3 19.39", 0.32, 16.68),
    ("1668-023", "Sarayan", "South Khorasan", "N33 51 19.03", "E58 31 4.86", 0.19, 3.61),
    ("1668-024", "Qasr-e Bahram", "Semnan", "N34 45 55.01", "E52 10 37.69", 0.65, 769.49),
    ("1668-025", "Mayamey", "Semnan", "N36 24 33.07", "E55 39 11.88", 0.53, 2.39),
    ("1668-026", "Abbas Abad", "Semnan", "N36 21 40.39", "E56 23 16.35", 0.86, 30.63),
    ("1668-027", "Miandasht", "Semnan", "N36 25 41.27", "E56 3 38.08", 2.44, 197.84),
    ("1668-028", "Zeynoddin", "Yazd", "N31 24 42.69", "E54 42 24.67", 0.41, 269.93),
    ("1668-029", "Meybod", "Yazd", "N32 13 40.53", "E54 0 33.1", 0.67, 9.98),
    ("1668-030", "Farasfaj", "Hamedan", "N34 29 16.68", "E48 16 58.76", 0.46, 12.56),
    ("1668-031", "Izadkhast", "Fars", "N31 30 48.11", "E52 7 59.54", 0.49, 37.65),
    ("1668-032", "Bisotun", "Kermanshah", "N34 23 04.32", "E47 26 05.76", 0.81, 35.36),
    ("1668-033", "Ganjali Khan", "Kerman", "N30 17 27.44", "E57 4 44.17", 0.38, 7.27),
    ("1668-034", "Yengeh Emam", "Alborz", "N35 56 10.63", "E50 43 10.64", 0.49, 12.29),
    ("1668-035", "Khajeh Nazar", "East Azerbaijan", "N38 58 38.8", "E45 34 37.1", 0.23, 18.75),
    ("1668-036", "Goujebel", "East Azerbaijan", "N38 20 38.02", "E46 51 48.06", 0.15, 10.93),
    ("1668-037", "Saeen", "Ardabil", "N38 0 3.76", "E47 52 53.71", 0.06, 74.04),
    ("1668-038", "Titi", "Gilan", "N37 2 41.19", "E49 54 8.05", 0.11, 12.29),
    ("1668-039", "Dehdasht", "Kohgiluyeh and Boyer-Ahmad", "N30 47 17.53", "E50 33 41.49", 0.16, 4.51),
    ("1668-040", "Khoy", "West Azerbaijan", "N38 27 57.6", "E44 37 24.7", 0.04, 6.96),
    ("1668-041", "Bagh-e Sheikh", "Markazi", "N34 59 26.99", "E50 26 49.04", 0.53, 30.8),
    ("1668-042", "Neyestanak", "Isfahan", "N32 58 16.34", "E52 47 57.71", 0.48, 25.39),
    ("1668-043", "Chehel Payeh", "Kerman", "N31 56 24.04", "E57 8 25.47", 0.33, 45.54),
    ("1668-044", "Khan", "South Khorasan", "N33 21 58.97", "E56 4 13.49", 0.34, 8.67),
    ("1668-045", "Deh Mohammad", "South Khorasan", "N33 59 29.62", "E56 58 45.04", 0.25, 10.68),
    ("1668-046", "Taj Abad", "Hamedan", "N34 52 35.88", "E48 13 14.62", 0.28, 6.56),
    ("1668-047", "Chah Kuran", "Kerman", "N31 34 9.6", "E56 51 0.61", 0.16, 35.69),
    ("1668-048", "Kharanaq", "Yazd", "N32 20 41.81", "E54 40 4.74", 0.28, 17.34),
    ("1668-049", "Rashti", "Yazd", "N32 26 26.6", "E53 37 51.79", 0.5, 9.54),
    ("1668-050", "Borazjan", "Bushehr", "N29 16 1.61", "E51 12 29.73", 0.78, 6.01),
    ("1668-051", "Chameshk", "Lorestan", "N33 14 16.64", "E48 12 40.81", 0.22, 11.67),
    ("1668-052", "Afzal", "Khuzestan", "N32 2 38.26", "E48 51 7.66", 0.1, 1.42),
    ("1668-053", "Bastak", "Hormozgan", "N27 11 54.6", "E54 22 33.5", 0.1, 2.24),
    ("1668-054", "Saadossaltaneh", "Qazvin", "N36 16 9.46", "E50 0 2.55", 2.58, 11.28),
]


def dms_to_decimal(token: str) -> float:
    hemi = token[0]
    parts = token[1:].split()
    deg = float(parts[0])
    minutes = float(parts[1]) if len(parts) > 1 else 0.0
    seconds = float(parts[2]) if len(parts) > 2 else 0.0
    value = deg + minutes / 60.0 + seconds / 3600.0
    if hemi in "SW":
        value = -value
    return value


def slug(name: str) -> str:
    return (
        name.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("'", "")
        .replace("ʿ", "")
    )


def emit() -> str:
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
        "# UNESCO World Heritage List 1668 — The Persian Caravanserai.",
        "# 54 components inscribed 17 September 2023, criteria (ii)(iii).",
        "# Source: https://whc.unesco.org/en/list/1668/maps/",
        "",
        ":unesco_persian_caravanserai a crm:E27_Site , bot:Site ;",
        '    rdfs:label "The Persian Caravanserai"@en ;',
        '    rdfs:label "کاروانسراهای ایرانی"@fa ;',
        "    skos:exactMatch wd:Q66030932 ;",
        '    persarch:unescoListId "1668" ;',
        '    dcterms:date "2023-09-17"^^xsd:date ;',
        "    dcterms:source <https://whc.unesco.org/en/list/1668/> ;",
        '    dcterms:description "Serial World Heritage property of fifty-four caravanserais along historic roads of Iran."@en .',
        "",
        ":Harvest_UNESCO_1668 a prov:Activity ;",
        '    rdfs:label "UNESCO WHC 1668 component harvest"@en ;',
        "    prov:used <https://whc.unesco.org/en/list/1668/maps/> .",
        "",
    ]
    for cid, name, province, lat_dms, lon_dms, prop, buf in COMPONENTS:
        lat = dms_to_decimal(lat_dms)
        lon = dms_to_decimal(lon_dms)
        local = slug(name)
        lines.append(f":{local} a persarch:Caravanserai , bot:Building , crmba:B1_Built_Work ;")
        lines.append(f'    rdfs:label "{name}"@en ;')
        lines.append(f'    persarch:unescoComponentId "{cid}" ;')
        lines.append("    persarch:isUnescoComponent true ;")
        lines.append("    crm:P46i_forms_part_of :unesco_persian_caravanserai ;")
        lines.append(f'    persarch:province "{province}"@en ;')
        lines.append(f'    geo:asWKT "POINT({lon:.6f} {lat:.6f})"^^geo:wktLiteral ;')
        lines.append(f'    persarch:propertyAreaHectare "{prop}"^^xsd:decimal ;')
        if buf is not None:
            lines.append(f'    persarch:bufferAreaHectare "{buf}"^^xsd:decimal ;')
        lines.append("    dcterms:source <https://whc.unesco.org/en/list/1668/maps/> ;")
        lines.append("    prov:wasGeneratedBy :Harvest_UNESCO_1668 .")
        lines.append("")
        lines.append(f":unesco_persian_caravanserai bot:hasBuilding :{local} .")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    out = ROOT / "data" / "unesco-1668.ttl"
    out.write_text(emit(), encoding="utf-8")
    print(f"Wrote {len(COMPONENTS)} UNESCO components to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
