# MIFAO 81 & 82 name list (human-editable)

Working list of caravanserais and related roadside buildings extracted from Maxime Siroux:

- **MIFAO 81** — *Caravansérails d'Iran et petites constructions routières* (IFAO, 1949). [Internet Archive](https://archive.org/details/MIFAO81)
- **MIFAO 82** — *Anciennes voies et monuments routiers de la région d'Ispahân* (IFAO, 1971). [Internet Archive](https://archive.org/details/MIFAO82)

Machine-readable copies: [`data/mifao-review-queue.csv`](../data/mifao-review-queue.csv) (one row per building) and [`data/mifao-evidence.csv`](../data/mifao-evidence.csv) (one row per source attestation). **Edit the CSVs.** This markdown is regenerated from `scripts/seed_mifao_review_queue.py` only when reseeding.

## Status

Every row is `review_status=candidate`. OCR of the 1949/1971 scans mangles names; plans and photographs are poor-quality rasters. Do not ingest RDF or create Wikidata items until a reviewer sets `review_status=accepted` and fills `unesco_id` / `wikidata` (accepted joins). Columns `proposed_unesco_id` and `proposed_wikidata` are unverified hints.

| Count | n |
| --- | --- |
| Buildings in this list | **99** |
| Attested in MIFAO 81 | 54 |
| Attested in MIFAO 82 | 79 |
| With an in-text plan (figure) | 80 |
| With a photograph (plate) | 68 |
| With a proposed UNESCO join | 13 |

## How to edit

1. Open `data/mifao-review-queue.csv`.
2. Correct `siroux_name` against the printed page (the index of MIFAO 82 was normalised with Jean Aubin).
3. Fill `normalized_en` and `normalized_fa`.
4. Confirm or clear `proposed_unesco_id` / `proposed_wikidata`, then copy accepted values into `unesco_id` / `wikidata`.
5. Flag the plan/photograph for IIIF (`has_plan` / `has_photograph`).
6. Set `review_status` to `accepted` or `rejected`. Put free-text judgement in `editor_notes`.
7. Add a new evidence row in `data/mifao-evidence.csv` whenever you cite another page, figure, or plate. Keep `source_name` + `locator` (page or plate) on every row.

Integrated graph data must stay distinguished by source: each statement carries `persarch:mifaoReference` (volume + page/figure/plate) after acceptance.

## A. Robât names (MIFAO 82 index, editor priority)

These sixteen names are the printed index cluster the editor asked to capture first. Two periods at Robât-e-Soltân are separate rows.

| Working ID | Siroux name | Type | Site | Sources | Cover evidence | Plan | Photo | Proposed action | Proposed UNESCO / Wikidata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `MIFAO82-robat-agha-kemal` | Robât-e-âghâ Kemâl | caravanserai | 20 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.148; MIFAO 82 (Siroux 1971) index p.20, 148; MIFAO 82 (Siroux 1971) index p.12, 20-22, 148-151, 155, 162-164, 167, 186, 188-189, 201; MIFAO 82 (Siroux 1971) fig. 41; MIFAO 82 (Siroux 1971) pl. XII F; pl. XIII A-B | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-atabaki` | Robât-e-atâbaki | robat | 3 | MIFAO 82;MIFAO 81 | MIFAO 82 (Siroux 1971) p.47; MIFAO 82 (Siroux 1971) index p.47; MIFAO 82 (Siroux 1971) fig. 5; MIFAO 82 (Siroux 1971) pl. III C-D; MIFAO 81 (Siroux 1949) p.86; MIFAO 81 (Siroux 1949) fig. 47 | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-golkan` | Robât-e-Golkân | robat | — | MIFAO 82 | MIFAO 82 (Siroux 1971) index p.11, 14; MIFAO 82 (Siroux 1971) itinerary p.11, 14 |  |  | new-item or enrich | — |
| `MIFAO81-robat-kerim` | Robat-e-Kerim | robat | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.46-49; MIFAO 81 (Siroux 1949) fig. 14; MIFAO 81 (Siroux 1949) pl. III 1-4; MIFAO 82 (Siroux 1971) index p.51, 74, 91-92, 117-118; MIFAO 82 (Siroux 1971) p.51, 74 | yes | yes | enrich | 1668-004 / Q42575545 |
| `MIFAO82-robat-meymeh` | Robat-e-Meymeh | robat | — | MIFAO 82 | MIFAO 82 (Siroux 1971) index p.12; MIFAO 82 (Siroux 1971) itinerary p.10-12 |  |  | new-item or enrich | — |
| `MIFAO82-robat-miyan` | Robât-e-Miyân | robat | — | MIFAO 82 | MIFAO 82 (Siroux 1971) p.87-88; MIFAO 82 (Siroux 1971) index p.18, 87; MIFAO 82 (Siroux 1971) index p.22, 87-88, 92, 113, 209 |  |  | new-item or enrich | — |
| `MIFAO82-robat-mourtcheh-khort` | Robât-e-Mourtcheh-Khort | robat | — | MIFAO 82 | MIFAO 82 (Siroux 1971) p.87; MIFAO 82 (Siroux 1971) index p.87; MIFAO 82 (Siroux 1971) index p.10-11, 15-19, 21-22, 25, 40, 44, 87, 109, 164, 175, 192, 194, 216 |  |  | new-item or enrich | — |
| `MIFAO82-robat-sanches` | Robât-e-Sanchés | robat | — | MIFAO 82;MIFAO 81 | MIFAO 82 (Siroux 1971) index p.92, 97; MIFAO 81 (Siroux 1949) p.see chap. VI notes |  |  | new-item or enrich | — |
| `MIFAO82-robat-sangui-aliabad` | Robât-e-Sangui (d'Ali-âbâd) | robat | — | MIFAO 82 | MIFAO 82 (Siroux 1971) index p.91-93; MIFAO 82 (Siroux 1971) fig. 13 | yes |  | new-item or enrich | — |
| `MIFAO82-robat-sangui-allahvidjeh` | Robât-e-Sangui (d'Allah-vidjeh) | robat | 9 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.98; MIFAO 82 (Siroux 1971) index p.10, 119-121, 130; MIFAO 82 (Siroux 1971) index p.98, 116-117, 119-121, 130, 133; MIFAO 82 (Siroux 1971) fig. 23; MIFAO 82 (Siroux 1971) pl. VII E-F | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-sangui-natanz` | Robât-e-Sangui (de Natanz) | robat | 2 / 6 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.44; MIFAO 82 (Siroux 1971) p.74; MIFAO 82 (Siroux 1971) index p.23, 44, 48, 55, 74, 81, 91-93, 115-118, 121, 272; MIFAO 82 (Siroux 1971) fig. 4; MIFAO 82 (Siroux 1971) pl. II E-F; pl. III A-B | yes | yes | new-item or enrich | — |
| `MIFAO81-robat-sharaf` | Robat-e-Sharraf | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.49-51; MIFAO 82 (Siroux 1971) index p.91-92, 116-117, 119; MIFAO 82 (Siroux 1971) p.91-92 |  |  | enrich | 1668-005 / Q2577338 |
| `MIFAO82-robat-soltan-sassanid` | Robât-e-Soltân | robat | 1 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.40; MIFAO 82 (Siroux 1971) index p.40, 44, 48, 55, 272, 289, 291; MIFAO 82 (Siroux 1971) fig. 1-3; MIFAO 82 (Siroux 1971) pl. II A-D | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-soltan-seljuk` | Robât-e-Soltân (Seldjoucide) | caravanserai | 5 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.66; MIFAO 82 (Siroux 1971) index p.68, 74, 85, 91-93, 105, 116, 118, 120, 139; MIFAO 82 (Siroux 1971) fig. 16; MIFAO 82 (Siroux 1971) pl. V A-F | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-turk` | Robât-e-Turk | robat | 7 | MIFAO 82;MIFAO 81 | MIFAO 82 (Siroux 1971) p.75-87; MIFAO 82 (Siroux 1971) index p.12, 14, 16, 75, 87-88, 91-93, 111, 113, 116, 118, 120-121, 188, 209, 272; MIFAO 82 (Siroux 1971) fig. 17-19; MIFAO 82 (Siroux 1971) pl. VI A-F; pl. VII A; MIFAO 81 (Siroux 1949) itinerary p.17 | yes | yes | new-item or enrich | — |
| `MIFAO82-robat-zendan` | Robât-e-Zendân | robat | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.103-106; MIFAO 81 (Siroux 1949) fig. 63-65; MIFAO 81 (Siroux 1949) pl. XI 4-6; MIFAO 82 (Siroux 1971) index p.47; MIFAO 82 (Siroux 1971) index p.47 | yes | yes | new-item or enrich | — |

## B. Other Siroux buildings (plans, photographs, national survey)

| Working ID | Siroux name | Type | Site | Sources | Cover evidence | Plan | Photo | Proposed action | Proposed UNESCO / Wikidata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `MIFAO82-tchah-e-siyah-qadim` | Tchâh-e-siyâh qadim | caravanserai | 4 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.57-66; MIFAO 82 (Siroux 1971) index p.10, 15, 49, 57, 64-66, 91, 116, 118-119, 121, 175; MIFAO 82 (Siroux 1971) fig. 9-12; MIFAO 82 (Siroux 1971) pl. III F; pl. IV A-E | yes | yes | new-item or enrich | — |
| `MIFAO82-qaleh-vedar` | Qaleh Védar | qaleh | 4 B | MIFAO 82 | MIFAO 82 (Siroux 1971) p.66; MIFAO 82 (Siroux 1971) fig. 15; MIFAO 82 (Siroux 1971) pl. IV F | yes | yes | review-type | — |
| `MIFAO82-tchahar-bordj` | Tchahâr-Bordj | caravanserai | 8 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.95; MIFAO 82 (Siroux 1971) index p.57, 95, 98, 116-117, 119-121, 124, 135, 156, 175; MIFAO 82 (Siroux 1971) fig. 22; MIFAO 82 (Siroux 1971) pl. VII C-D | yes | yes | new-item or enrich | — |
| `MIFAO82-tchahar-abad-b` | Tchahâr-âbâd B | caravanserai | 12 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.99; MIFAO 82 (Siroux 1971) fig. 24-25; MIFAO 82 (Siroux 1971) pl. VIII A | yes | yes | new-item or enrich | — |
| `MIFAO82-tchahar-abad-a` | Tchahâr-âbâd A | casernement | 10 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.105; MIFAO 82 (Siroux 1971) index p.10, 28, 90, 99, 105, 107-109, 113, 118-121, 167, 182, 187-188; MIFAO 82 (Siroux 1971) fig. 24, 26; MIFAO 82 (Siroux 1971) pl. VIII B | yes | yes | review-type | — |
| `MIFAO82-dombi-casernement` | Dombi A | casernement | 11 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.107; MIFAO 82 (Siroux 1971) fig. 27; MIFAO 82 (Siroux 1971) pl. VIII C-F | yes | yes | review-type | — |
| `MIFAO82-gourgab` | Qaleh de Gourgâb | casernement | 28 bis | MIFAO 82 | MIFAO 82 (Siroux 1971) p.109; MIFAO 82 (Siroux 1971) fig. 28; MIFAO 82 (Siroux 1971) pl. IX A-B | yes | yes | review-type | — |
| `MIFAO82-qaleh-moutah` | Qaleh de Moutah | qaleh | 28 E | MIFAO 82 | MIFAO 82 (Siroux 1971) p.111; MIFAO 82 (Siroux 1971) fig. 29; MIFAO 82 (Siroux 1971) pl. IX C-D | yes | yes | review-type | — |
| `MIFAO81-mahyar` | Mâhyâr | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.58; MIFAO 81 (Siroux 1949) fig. 19; MIFAO 81 (Siroux 1949) pl. IV 5; pl. V 2, 6; MIFAO 82 (Siroux 1971) p.123; MIFAO 82 (Siroux 1971) fig. 30; MIFAO 82 (Siroux 1971) pl. X D; MIFAO 82 (Siroux 1971) index p.32, 123, 126, 133, 135, 164, 185, 187, 189, 194 | yes | yes | enrich | 1668-016 / Q5904114 |
| `MIFAO82-dhor` | Dhor | caravanserai | 13 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.126; MIFAO 82 (Siroux 1971) index p.9-11, 14, 47, 126, 128, 130, 138, 142, 144, 185, 188; MIFAO 82 (Siroux 1971) fig. 31; MIFAO 82 (Siroux 1971) pl. IX E-F; pl. X A | yes | yes | new-item or enrich | — |
| `MIFAO81-riavad-e-bostan` | Riâvad-e-Bostân | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.60; MIFAO 81 (Siroux 1949) fig. 20-21; MIFAO 82 (Siroux 1971) p.128; MIFAO 82 (Siroux 1971) index p.29, 31, 128, 135, 185, 188 | yes |  | new-item or enrich | — |
| `MIFAO82-bahram` | Bahrâm | caravanserai | 14 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.128; MIFAO 82 (Siroux 1971) index p.26, 128, 135, 139, 172, 186; MIFAO 82 (Siroux 1971) fig. 32 | yes |  | new-item or enrich | — |
| `MIFAO81-passengan` | Passengân | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.64; MIFAO 81 (Siroux 1949) fig. 24; MIFAO 81 (Siroux 1949) pl. VI 1; MIFAO 82 (Siroux 1971) p.130; MIFAO 82 (Siroux 1971) pl. X B; MIFAO 82 (Siroux 1971) index p.130, 133, 147, 156, 185 | yes | yes | new-item or enrich | — |
| `MIFAO81-haouz-e-soltan-safavid` | Haouz-é-Sultan (safawide) | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.67; MIFAO 81 (Siroux 1949) fig. 27; MIFAO 81 (Siroux 1949) pl. VI 2, 6; MIFAO 82 (Siroux 1971) p.131; MIFAO 82 (Siroux 1971) index p.131, 185, 201 | yes | yes | new-item or enrich | — |
| `MIFAO82-moutah-safavid` | Moutah | caravanserai | 14 B | MIFAO 82 | MIFAO 82 (Siroux 1971) p.131; MIFAO 82 (Siroux 1971) index p.131; MIFAO 82 (Siroux 1971) fig. 33; MIFAO 82 (Siroux 1971) pl. X E-F; pl. XI A-B | yes | yes | new-item or enrich | — |
| `MIFAO82-sagzi` | Sagzi-âbâd | caravanserai | 15 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.133; MIFAO 82 (Siroux 1971) index p.26-27, 30, 133, 156, 186, 194; MIFAO 82 (Siroux 1971) fig. 34; MIFAO 82 (Siroux 1971) pl. X C; pl. XI C | yes | yes | new-item or enrich | — |
| `MIFAO81-yezd-e-khast` | Yezd-é-Khast | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.65-67; MIFAO 81 (Siroux 1949) fig. 25; MIFAO 81 (Siroux 1949) pl. V 1; pl. VI 3; MIFAO 82 (Siroux 1971) p.137; MIFAO 82 (Siroux 1971) fig. 35; MIFAO 82 (Siroux 1971) index p.25, 31-32, 137, 139, 159, 165, 172, 183, 186, 188, 279 | yes | yes | enrich | 1668-031 / Q5873579 |
| `MIFAO81-shurgestan` | Shurgestan | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.67; MIFAO 81 (Siroux 1949) fig. 26; MIFAO 82 (Siroux 1971) p.139; MIFAO 82 (Siroux 1971) index p.139, 170, 186 | yes |  | new-item or enrich | — |
| `MIFAO82-behdjat-abad` | Behdjat-âbâd | caravanserai | 16 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.139; MIFAO 82 (Siroux 1971) index p.18-19, 23, 25, 74, 99, 139, 186-187, 189; MIFAO 82 (Siroux 1971) fig. 36-37; MIFAO 82 (Siroux 1971) pl. XI D-E | yes | yes | new-item or enrich | — |
| `MIFAO82-kouh-roud` | Kouh-roûd | caravanserai | 17 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.142; MIFAO 82 (Siroux 1971) index p.20-23, 124, 142, 144, 150, 162, 164, 186-189, 194, 279; MIFAO 82 (Siroux 1971) fig. 38; MIFAO 82 (Siroux 1971) pl. I A; pl. XI F | yes | yes | new-item or enrich | — |
| `MIFAO82-aznidjeh` | Aznidjeh | caravanserai | 18 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.144; MIFAO 82 (Siroux 1971) index p.8, 10, 144, 155, 159, 186, 190, 194; MIFAO 82 (Siroux 1971) fig. 39; MIFAO 82 (Siroux 1971) pl. XII A-B | yes | yes | new-item or enrich | — |
| `MIFAO82-dombi-safavid` | Dombi B | caravanserai | 19 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.145; MIFAO 82 (Siroux 1971) index p.18-19, 23, 25, 44, 74-75, 99, 107, 113, 116-121, 142, 145, 162, 170, 186, 189, 226; MIFAO 82 (Siroux 1971) fig. 40; MIFAO 82 (Siroux 1971) pl. XII C-E | yes | yes | new-item or enrich | — |
| `MIFAO82-gabr-abad` | Gabr-âbâd | caravanserai | 21 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.150; MIFAO 82 (Siroux 1971) index p.22, 116, 150, 159, 162, 186, 188-189, 194, 201, 215; MIFAO 82 (Siroux 1971) fig. 42; MIFAO 82 (Siroux 1971) pl. XIII C-F | yes | yes | enrich | 1668-015 / Q5873197 |
| `MIFAO82-kouh-payeh` | Kouh-pâyeh | caravanserai | 22 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.156; MIFAO 82 (Siroux 1971) index p.27-31, 54, 63, 91, 116, 118, 156, 161, 164, 186-189, 198, 219-220, 226, 229, 238, 255, 261, 271-272, 283; MIFAO 82 (Siroux 1971) fig. 43-44; MIFAO 82 (Siroux 1971) pl. XIV A-F; pl. XV A-B | yes | yes | enrich | 1668-018 / Q5906011 |
| `MIFAO82-qaleh-qadim-kouhpayeh` | Qaleh-qadim de Kouh-pâyeh | qaleh | 22 B | MIFAO 82 | MIFAO 82 (Siroux 1971) p.54; MIFAO 82 (Siroux 1971) index p.27, 54, 115, 156, 218; MIFAO 82 (Siroux 1971) fig. 7-8; MIFAO 82 (Siroux 1971) pl. III E | yes | yes | review-type | — |
| `MIFAO82-bisyoun` | Bisyoun | caravanserai | 23 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.159; MIFAO 82 (Siroux 1971) index p.30, 39, 159, 165, 185, 187-188, 237, 259; MIFAO 82 (Siroux 1971) fig. 45; MIFAO 82 (Siroux 1971) pl. XV C-D | yes | yes | new-item or enrich | — |
| `MIFAO82-narendj-qaleh-bisyoun` | Nârendj-Qaleh de Bisyoun | qaleh | 23 bis | MIFAO 82 | MIFAO 82 (Siroux 1971) p.88; MIFAO 82 (Siroux 1971) fig. 20 | yes |  | review-type | — |
| `MIFAO82-vendad-deh` | Vendâd-deh | caravanserai | 24 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.162; MIFAO 82 (Siroux 1971) index p.12, 21, 148, 150, 162, 165, 167-168, 173, 187-189; MIFAO 82 (Siroux 1971) fig. 46; MIFAO 82 (Siroux 1971) pl. XV E; pl. XVI A-E | yes | yes | new-item or enrich | — |
| `MIFAO82-gez` | Gêz | caravanserai | 25 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.164; MIFAO 82 (Siroux 1971) index p.9, 15-17, 21, 109, 146, 148, 150, 159, 162, 164, 168, 173, 186, 188-189, 192, 225, 288; MIFAO 82 (Siroux 1971) fig. 47-48; MIFAO 82 (Siroux 1971) pl. XVI F; pl. XVII A-D | yes | yes | enrich | 1668-017 / Q5871566 |
| `MIFAO82-sardahan` | Sardahan | caravanserai | 26 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.167; MIFAO 82 (Siroux 1971) index p.23, 25, 44, 101, 142, 162, 167, 173, 187, 189, 274; MIFAO 82 (Siroux 1971) fig. 49-50; MIFAO 82 (Siroux 1971) pl. XVII E-F; pl. XVIII A | yes | yes | new-item or enrich | — |
| `MIFAO81-natenz` | Natenz | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.69; MIFAO 81 (Siroux 1949) fig. 28; MIFAO 81 (Siroux 1949) pl. VI 4; MIFAO 82 (Siroux 1971) p.171; MIFAO 82 (Siroux 1971) fig. 51; MIFAO 82 (Siroux 1971) pl. XVIII B; MIFAO 82 (Siroux 1971) index p.196, 201 | yes | yes | new-item or enrich | — |
| `MIFAO81-zawareh` | Zawareh | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.69; MIFAO 81 (Siroux 1949) fig. 29; MIFAO 81 (Siroux 1949) pl. VII 1, 3; MIFAO 82 (Siroux 1971) p.172; MIFAO 82 (Siroux 1971) fig. 52; MIFAO 82 (Siroux 1971) index p.26, 29, 155, 172, 186, 199 | yes | yes | new-item or enrich | — |
| `MIFAO81-mader-e-chah-mourtcheh` | Mâder-e-Châh (de Mourtcheh-Khort) | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.79-81; MIFAO 81 (Siroux 1949) fig. 36-39, 89; MIFAO 81 (Siroux 1949) pl. VIII 4-5; pl. IX 3; pl. XII 1; MIFAO 82 (Siroux 1971) p.175; MIFAO 82 (Siroux 1971) fig. 54; MIFAO 82 (Siroux 1971) index p.15, 175, 187-188 | yes | yes | enrich | Q42627405 |
| `MIFAO82-tchah-e-siyah-now` | Tchâh-e-siyâh now | caravanserai | 27 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.175; MIFAO 82 (Siroux 1971) index p.168, 175, 179, 182, 187-190; MIFAO 82 (Siroux 1971) fig. 55-56; MIFAO 82 (Siroux 1971) pl. XVIII C-F | yes | yes | enrich | 1668-012 / Q5905596 |
| `MIFAO82-mader-e-chah-dhor` | Mâder-e-Châh du col de Dhor | caravanserai | 28 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.179; MIFAO 82 (Siroux 1971) index p.11, 179, 187-188; MIFAO 82 (Siroux 1971) fig. 57-58; MIFAO 82 (Siroux 1971) pl. XIX A-C | yes | yes | new-item or enrich | — |
| `MIFAO82-bagher-abad-tchapar` | Tchapar-khâneh de Bâgher-âbâd | tchaparkhaneh | 35 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.192; MIFAO 82 (Siroux 1971) fig. 59; MIFAO 82 (Siroux 1971) pl. XIX D | yes | yes | review-type | — |
| `MIFAO82-soh` | Sôh | caravanserai | 29 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.194; MIFAO 82 (Siroux 1971) index p.20, 22, 144, 162, 164, 194, 201; MIFAO 82 (Siroux 1971) fig. 60; MIFAO 82 (Siroux 1971) pl. XIX E; pl. XX A | yes | yes | new-item or enrich | — |
| `MIFAO82-qaleh-chour` | Qaleh-Chour | caravanserai | 30 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.194; MIFAO 82 (Siroux 1971) index p.32, 172, 194, 201; MIFAO 82 (Siroux 1971) fig. 61; MIFAO 82 (Siroux 1971) pl. XIX F; pl. XX B | yes | yes | new-item or enrich | — |
| `MIFAO82-chahi` | Châhi | caravanserai | 31 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.197; MIFAO 82 (Siroux 1971) index p.33, 197; MIFAO 82 (Siroux 1971) fig. 62 | yes |  | new-item or enrich | — |
| `MIFAO82-qaleh-ali-agha` | Qaleh Ali-âghâ | qaleh | 32 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.198; MIFAO 82 (Siroux 1971) index p.34, 198; MIFAO 82 (Siroux 1971) fig. 63; MIFAO 82 (Siroux 1971) pl. XX C | yes | yes | review-type | — |
| `MIFAO82-taqi-abad` | Taqi-âbâd | caravanserai | 33 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.199; MIFAO 82 (Siroux 1971) fig. 64-65 | yes |  | new-item or enrich | — |
| `MIFAO82-zizeh` | Zizeh | caravanserai | 34 | MIFAO 82 | MIFAO 82 (Siroux 1971) p.201; MIFAO 82 (Siroux 1971) index p.25, 201; MIFAO 82 (Siroux 1971) fig. 66-67; MIFAO 82 (Siroux 1971) pl. XX D-E | yes | yes | new-item or enrich | — |
| `MIFAO82-mader-e-chah-isfahan` | Mâder-e-Châh à Ispahân | urban-caravanserai | A 48 | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.117-119; MIFAO 81 (Siroux 1949) fig. 79; MIFAO 82 (Siroux 1971) p.284-288; MIFAO 82 (Siroux 1971) fig. 97; MIFAO 82 (Siroux 1971) pl. XXX A-B; MIFAO 82 (Siroux 1971) index p.189, 284 | yes | yes | enrich or new-item | — |
| `MIFAO82-kunar-e-siyah` | Kunâr-e-Siyâh | caravanserai | — | MIFAO 82 | MIFAO 82 (Siroux 1971) p.54; MIFAO 82 (Siroux 1971) index p.54-55, 74, 91-92, 115 |  |  | new-item or enrich | — |
| `MIFAO82-bisoutoun` | Bisoutoun | caravanserai | — | MIFAO 82 | MIFAO 82 (Siroux 1971) p.51; MIFAO 82 (Siroux 1971) index p.51, 91, 115-116, 118, 121; MIFAO 82 (Siroux 1971) fig. 6; MIFAO 82 (Siroux 1971) pl. VII B | yes | yes | enrich | 1668-032 / Q5908224 |
| `MIFAO81-nere` | Néré | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.35; MIFAO 81 (Siroux 1949) fig. 2; MIFAO 81 (Siroux 1949) pl. I 4 | yes | yes | new-item or enrich | — |
| `MIFAO81-imamzadeh-hachem` | Imam-zadeh Hachem | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.36; MIFAO 81 (Siroux 1949) fig. 3; MIFAO 81 (Siroux 1949) pl. II 3 | yes | yes | new-item or enrich | — |
| `MIFAO81-gamboudcht` | Gamboudcht | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.36; MIFAO 81 (Siroux 1949) fig. 4-5; MIFAO 81 (Siroux 1949) pl. I 2 | yes | yes | new-item or enrich | — |
| `MIFAO81-peylour` | Peylour | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.37; MIFAO 81 (Siroux 1949) fig. 6; MIFAO 81 (Siroux 1949) pl. II 2 | yes | yes | new-item or enrich | — |
| `MIFAO81-mirza-abdullah-khan` | Mirza-Abdullah-Khan | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.38; MIFAO 81 (Siroux 1949) fig. 7 | yes |  | new-item or enrich | — |
| `MIFAO81-chebli` | Chebli | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.40; MIFAO 81 (Siroux 1949) fig. 8-10; MIFAO 81 (Siroux 1949) pl. II 1, 4-5 | yes | yes | new-item or enrich | — |
| `MIFAO81-abbassi-abali` | Abbassi près d'Ab-Ali | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.43; MIFAO 81 (Siroux 1949) fig. 11 | yes |  | new-item or enrich | — |
| `MIFAO81-hint-khatunabad` | Khatunabad (mountain) | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) index p.unconfirmed in TOC |  |  | enrich or new-item | — |
| `MIFAO81-hint-gaduk` | Gaduk near Firuzkuh | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) itinerary p.13-14 |  |  | enrich or new-item | — |
| `MIFAO81-darwazeh-gatch` | Darwazeh-Gatch | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.45; MIFAO 81 (Siroux 1949) fig. 12; MIFAO 82 (Siroux 1971) index p.32, 51, 91, 115 | yes |  | new-item or enrich | — |
| `MIFAO81-semnan` | près de Semnan | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.49 |  |  | new-item or enrich | — |
| `MIFAO81-zaffarounie` | Zalfarounie | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.49; MIFAO 82 (Siroux 1971) index p.85, 119 |  |  | enrich | 1668-021 / Q5923727 |
| `MIFAO81-kaleh-sangui` | Kaleh-Sangui | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.51; MIFAO 81 (Siroux 1949) fig. 15; MIFAO 81 (Siroux 1949) pl. III 5-6 | yes | yes | new-item or enrich | — |
| `MIFAO81-sertchem` | Sertchem | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.53; MIFAO 81 (Siroux 1949) fig. 16-18; MIFAO 81 (Siroux 1949) pl. IV 1-2, 4; MIFAO 82 (Siroux 1971) p.172-174; MIFAO 82 (Siroux 1971) fig. 14; MIFAO 82 (Siroux 1971) index p.63, 91-92, 95, 116, 118-120, 146, 148, 156, 173 | yes | yes | new-item or enrich | — |
| `MIFAO81-airandibi` | Airandibi | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.57; MIFAO 81 (Siroux 1949) pl. IV 3; MIFAO 82 (Siroux 1971) index p.92, 95, 117, 119-120 |  | yes | new-item or enrich | — |
| `MIFAO81-sangbast` | Sangbast | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.60; MIFAO 81 (Siroux 1949) pl. V 5; MIFAO 82 (Siroux 1971) index p.185, 188 |  | yes | new-item or enrich | — |
| `MIFAO81-guilak` | Guilak | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.62; MIFAO 81 (Siroux 1949) fig. 22-23; MIFAO 81 (Siroux 1949) pl. V 3-4; MIFAO 82 (Siroux 1971) index p.130, 133, 135 | yes | yes | new-item or enrich | — |
| `MIFAO81-roudehen` | Roudehen | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.67; MIFAO 81 (Siroux 1949) pl. VI 5; MIFAO 82 (Siroux 1971) index p.13 |  | yes | new-item or enrich | — |
| `MIFAO81-siah-kouh-abbasabad` | Siah-Kouh (Abbas-abad) | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.72; MIFAO 81 (Siroux 1949) pl. VII 2, 4-6; pl. VIII 6 |  | yes | new-item or enrich | — |
| `MIFAO81-dehbid-safavid` | Deh-Bid (polygonal safawide) | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.73; MIFAO 81 (Siroux 1949) fig. 30; MIFAO 82 (Siroux 1971) p.183; MIFAO 82 (Siroux 1971) index p.32, 90, 101, 183, 201 | yes |  | new-item or enrich | — |
| `MIFAO81-amin-abad` | Amin-Abad | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.73; MIFAO 81 (Siroux 1949) fig. 31; MIFAO 82 (Siroux 1971) p.183; MIFAO 82 (Siroux 1971) index p.32, 90, 101, 183 | yes |  | enrich | 1668-014 / Q5907540 |
| `MIFAO81-khan-e-khurra` | Khan-é-Khurra | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.73; MIFAO 82 (Siroux 1971) p.183; MIFAO 82 (Siroux 1971) index p.90, 101, 183 |  |  | new-item or enrich | — |
| `MIFAO81-djemal-abad` | Djemal-Abad | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.73; MIFAO 81 (Siroux 1949) fig. 32-33; MIFAO 81 (Siroux 1949) pl. VIII 1; MIFAO 82 (Siroux 1971) p.172-174; MIFAO 82 (Siroux 1971) index p.175, 187 | yes | yes | enrich | 1668-009 / Q5907713 |
| `MIFAO81-nikpey` | Nikpey | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.75; MIFAO 81 (Siroux 1949) fig. 34; MIFAO 81 (Siroux 1949) pl. VIII 3; MIFAO 82 (Siroux 1971) p.172-174; MIFAO 82 (Siroux 1971) index p.161, 172-173, 187 | yes | yes | new-item or enrich | — |
| `MIFAO81-jam` | Jam | caravanserai | C | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.77; MIFAO 81 (Siroux 1949) fig. 35; MIFAO 81 (Siroux 1949) pl. VIII 2; MIFAO 82 (Siroux 1971) p.172-174; MIFAO 82 (Siroux 1971) index p.161, 172, 187 | yes | yes | new-item or enrich | — |
| `MIFAO81-abbas-abad-khorassan` | Abbas-Abad (route du Khorassan) | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.81; MIFAO 81 (Siroux 1949) pl. IX 1-2 |  | yes | new-item or enrich | — |
| `MIFAO81-between-shahroud-miandacht` | entre Chahroud et Miandacht | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.81; MIFAO 81 (Siroux 1949) pl. IX 5 |  | yes | new-item or enrich | — |
| `MIFAO81-miandacht` | Miandacht | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.81; MIFAO 81 (Siroux 1949) pl. IX 4, 6 |  | yes | enrich | 1668-027 / Q5705395 |
| `MIFAO81-tchehel-hessieh` | Tchehel-Hessieh | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.81; MIFAO 81 (Siroux 1949) fig. 40 | yes |  | new-item or enrich | — |
| `MIFAO81-dehbid-qajar` | Deh-Bid (kadjar) | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.83; MIFAO 81 (Siroux 1949) fig. 41-43 | yes |  | new-item or enrich | — |
| `MIFAO81-ardakan` | Ardakan | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.83; MIFAO 81 (Siroux 1949) fig. 44-46, 88; MIFAO 82 (Siroux 1971) index p.172, 201 | yes |  | new-item or enrich | — |
| `MIFAO81-perech` | Perech | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.86; MIFAO 81 (Siroux 1949) fig. 48-50; MIFAO 82 (Siroux 1971) index p.201 | yes |  | new-item or enrich | — |
| `MIFAO81-rah-dar` | Rah-Dar | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.86; MIFAO 81 (Siroux 1949) fig. 51-52; MIFAO 82 (Siroux 1971) index p.201 | yes |  | new-item or enrich | — |
| `MIFAO81-haouz-e-soltan-qajar` | Haouz-é-Sultan (kadjar) | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.89; MIFAO 81 (Siroux 1949) fig. 53; MIFAO 81 (Siroux 1949) pl. X 1-2 | yes | yes | new-item or enrich | — |
| `MIFAO81-kale-kermes` | Kalé-Kermès | caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.90; MIFAO 81 (Siroux 1949) fig. 54 | yes |  | new-item or enrich | — |
| `MIFAO81-ali-abad` | Ali-Abad | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.92-96; MIFAO 81 (Siroux 1949) fig. 55-59, 96-97; MIFAO 81 (Siroux 1949) pl. X 3-5; pl. XI 1-2; MIFAO 82 (Siroux 1971) index p.201 | yes | yes | new-item or enrich | — |
| `MIFAO81-manzarieh` | Manzarieh | caravanserai | — | MIFAO 81;MIFAO 82 | MIFAO 81 (Siroux 1949) p.96; MIFAO 81 (Siroux 1949) fig. 60-61; MIFAO 81 (Siroux 1949) pl. XI 3; MIFAO 82 (Siroux 1971) index p.201 | yes | yes | new-item or enrich | — |
| `MIFAO81-kachan-octogonal` | caravansérail octogonal dans le bazar de Kachan | urban-caravanserai | — | MIFAO 81 | MIFAO 81 (Siroux 1949) p.119; MIFAO 81 (Siroux 1949) fig. 80 | yes |  | review-type | — |

## Disambiguation rules (do not collapse without review)

- **Mâder-e-Châh** is three buildings: Murcheh Khvort (Q42627405), the pass of Dhor, and the urban Isfahan complex (later Abbasi Hotel).
- **Robât-e-Mourtcheh-Khort** is the earlier ribat at the same station as Madarshah.
- **Tchâh-e-siyâh qadim** (site 4) and **Tchâh-e-siyâh now** (site 27, proposed 1668-012 Sheikhali Khan) are two buildings.
- **Robât-e-Sangui de Natanz** (sites 2/6) is not the large Safavid Natanz caravanserai (site C / MIFAO 81 Natenz).
- **Bahrâm** on the Ardestan road is not Qasr-e Bahram (UNESCO 1668-024).
- **Bisyoun** (Isfahan–Nain) is not **Bisoutoun / Bisotun** (Kermanshah).
- **Ali-Abad** on the Tehran–Qom road is not **Robât-e-Sangui d'Ali-âbâd**.
- **Aghâ-Kemâl Bala** (Tchâh-gadeh, site 20) is not **Aghâ-Kemâl-Païn** (Vendâd-deh, site 24).

## Complementary documents

Siroux's value for this graph is the unpublished plans (`*` / inédit) and the photographic plates. Scan quality on Internet Archive is poor (600 ppi photographs of worn collotypes). After a name is accepted:

1. Re-photograph or re-scan the plate if a better copy exists.
2. Add a canvas to the building's IIIF manifest (`persarch:hasPlanPresentation` / `persarch:Photograph`).
3. Quote the printed page in `persarch:mifaoReference`, for example `MIFAO 82 p. 148, fig. 41, pl. XII F`.
