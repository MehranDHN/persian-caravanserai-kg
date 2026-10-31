# Harvesting Notes — Unstructured Sources (MIFAO 81 & 82)

## Primary sources

- **MIFAO 81**: Maxime Siroux, *Caravansérails d'Iran et petites constructions routières*, Mémoires de l’Institut français d’archéologie orientale, t. 81, Le Caire, 1949.  
  Internet Archive: https://archive.org/details/MIFAO81 (OCR available).  
  National survey of roadside inns and minor road buildings; measured plans, dimensions, historical notes.

- **MIFAO 82**: Maxime Siroux, *Anciennes voies et monuments routiers de la région d'Ispahân*, MIFAO t. 82, Le Caire, 1971.  
  Internet Archive: https://archive.org/details/MIFAO82 (OCR available).  
  About 60 caravanserais and 33 other buildings within ~200 km of Isfahan; 98 plans, 170 photographs. Completes and updates the 1949 survey for the Isfahan region.

OCR of 1949/1971 French typography mangles proper names, dimensions, and Persian transliterations. Plans are raster figures. Automated geometry extraction is unreliable. Period attributions (Seljuk, Safavid, Qajar) must be checked against UNESCO, Wikidata, and later scholarship (Kleiss).

## Human-in-the-loop protocol

1. **Candidate extraction** — printed TOC, name index, figure and plate lists → `data/mifao-review-queue.csv` (one building) and `data/mifao-evidence.csv` (source name + page/figure/plate). Status starts as `candidate`.
2. **Review** — a scholar:
   - normalizes English and Persian labels
   - confirms period and patronage
   - joins to an existing Wikidata item **or** proposes a new item following `docs/wikidata-blueprint.md` (Q42627405 pattern)
   - flags the plan/photograph for IIIF
   - sets `reviewStatus` to `accepted` or `rejected`
3. **Ingestion** — only `accepted` rows are committed as RDF (`persarch:mifaoReference`, `crm:P70_documents` pointing at the MIFAO page/figure) and appended to `docs/wikidata-candidates.md` §C.
4. **IIIF** — digitized plans become canvases linked with `persarch:hasPlanPresentation`.

The editor will modify the new-candidate list after this review. Harvest scripts must not invent Wikidata items from OCR.

## Technical issues that require a human

| Issue | Why automation fails |
| --- | --- |
| French → Persian name mapping | Siroux spellings (Ispahân, Robât, Deyr-i-Guetchin) diverge from UNESCO and Wikidata labels |
| Two buildings at one station | Ahovan stone vs Shah Abbasi (1668-002 / 1668-003); dual courts at Miandasht |
| Missing coordinates | Siroux gives itineraries, not GPS; join to UNESCO/Wikidata/OSM by a reviewer |
| Adaptive reuse | Abbasi Hotel (converted Madar-i Shah caravanserai in Isfahan city) is a different building from Q42627405 Madarshah at Murcheh Khvort |
| Plan scale | Figure scales and north arrows need visual reading |

## Review queue

Editable files (source of truth after this extraction):

| File | Role |
| --- | --- |
| [`data/mifao-review-queue.csv`](../data/mifao-review-queue.csv) | One row per building. Editor fills Persian labels, accepted UNESCO/Wikidata joins, `review_status`. |
| [`data/mifao-evidence.csv`](../data/mifao-evidence.csv) | One row per attestation. `source_name` + `locator` (page, figure, or plate) is the cover evidence. |
| [`docs/mifao-name-list.md`](mifao-name-list.md) | Human-readable copy of the same list. |

Seed script: `python scripts/seed_mifao_review_queue.py` (overwrites the CSVs; do not re-run after editorial edits).

Names were taken from the printed tables of contents, the MIFAO 82 *Index des noms*, the table of figures, and the table of plates. Internet Archive OCR was a finding aid only. Plans and photographs on the public scans are poor-quality rasters; they remain complementary documents for IIIF after visual review.

Integrated statements must stay distinguished by source. After `accepted`, RDF uses `persarch:mifaoReference` such as `MIFAO 82 p. 148, fig. 41, pl. XII F`, with `crm:P70_documents` pointing at that page or plate.
