# Wikidata Enrichment Blueprint for Persian Caravanserais

This document is the quality bar for completing Wikidata items and for proposing **new** items. It is based on:

- [Q42627405](https://www.wikidata.org/wiki/Q42627405) — Madarshah Caravanserai (Murcheh Khvort). National heritage, **not** a UNESCO 1668 component. Use this as the model for non-inscribed roadside inns and for new items from MIFAO.
- [Q5905596](https://www.wikidata.org/wiki/Q5905596) — Sheikhali Khan / Chaleh Siah Caravanserai. UNESCO **1668-012**. Use this as the model for inscribed components.

## What Q42627405 demonstrates

| Statement | Pattern |
| --- | --- |
| P31 | cultural property (Q2065736) *and should also have* caravanserai (Q186347) |
| P17 | Iran (Q794) |
| P131 | Murcheh Khvort Rural District (most specific) |
| P625 | 33°0'47"N, 51°29'57"E |
| P1435 | Iranian National Heritage (Q5958900), start time 6 November 2005 |
| P1369 | 13657 (via heritage API reference) |
| P186 | stone (foundation), brick, mortar, tile |
| P149 | Safavid; Qajar (renovation) |
| P1619 | 17th century; 1835 renovation |
| P18 / Commons | Category:Madarshah Caravanserai |
| Labels | English + Persian description as national heritage site |

References point at the Wikimedia heritage API (`srcountry=ir`, registration id).

## What Q5905596 demonstrates (UNESCO component)

Everything above, plus:

| Statement | Pattern |
| --- | --- |
| P361 / heritage | part of UNESCO World Heritage Site Q66030932, start 17 September 2023 |
| P757 | `1668-012` |
| official name | Sheikhali Khān Caravanserai (qualifier) |
| area | 0.82 ha (UNESCO property) |
| P1369 | 1716 |
| aliases | Sheikh Ali Khan Zanganeh; Chaleh Siah |

The current harvest still lacks `P361` → Q66030932 on this item (and on every other 1668 component). Adding that statement, with a reference to https://whc.unesco.org/en/list/1668/maps/, is the single highest-value batch edit.

## Minimum required statements

| Property | Value / pattern | Priority | Notes |
| --- | --- | --- | --- |
| P31 | Q186347 | Required | Also Q2065736 when nationally registered |
| P17 | Q794 | Required | |
| P131 | province → county → rural district | Required | Most specific available |
| P625 | coordinates | Required | Prefer UNESCO centroid for 1668 components; note precision |
| Labels | English + Persian | Required | P1705 for native Persian label |
| Description | bilingual | Recommended | “caravanserai in [place], Iranian national heritage site” (+ “and World Heritage site” when inscribed) |
| P1435 | Q5958900 | High | Include P580 and a reference |
| P1369 | registration number | High | When known |
| P361 | Q66030932 | UNESCO components | Official name qualifier |
| P757 | 1668-xxx | UNESCO components | |
| P18 / P373 | image / Commons | Recommended | |
| P186 | materials | Medium | |
| P571 / P1619 | inception or opening | Medium | Hijri + Gregorian as labels on the same time-span in *this* graph; Wikidata uses one dated statement |

## Contribution workflow

1. Run `python scripts/compare_unesco_wikidata.py` and open `docs/wikidata-candidates.md`.
2. For each UNESCO row: **enrich** the matched QID. Do not mint a duplicate.
3. For 1668-044 Khan / Q138647472: complete the stub (labels first) rather than creating a second item.
4. For MIFAO 81/82: extract a candidate into `data/mifao-review-queue.csv`, review, then either link to an existing QID or add a **new-item** row in `docs/wikidata-candidates.md` §C.
5. Always add references (P248, P854, retrieved date). UNESCO maps URL for P361/P757; heritage API for P1435/P1369; Siroux 1949/1971 for plans and dimensions after human validation.
6. Re-harvest this repository after Wikidata edits.

## Gap detection SPARQL

See `queries/wikidata-gaps.rq`. Rebuild the candidate markdown from the harvest; do not hand-maintain the UNESCO section of the candidate list.
