# Persian Caravanserai Knowledge Graph

**An OWL/RDF repository of Persian caravanserais, extending the [persarch](https://github.com/MehranDHN/persarch) ontology (BOT + CIDOC CRM / CRMba).**

This project builds a FAIR/LOUD Linked Open Data graph of Persian caravanserais (کاروانسراهای ایرانی). It integrates Wikidata, UNESCO World Heritage List **1668**, and unstructured scholarly reports (MIFAO 81 and 82) into one model that **extends BOT** and overlays CIDOC CRM / CRMba exactly as specified in persarch.

**Status:** harvest and alignment layer in place. Unstructured MIFAO records require human review before they become Wikidata candidates.

## Vision

- Model each caravanserai as `persarch:Caravanserai` (subclass of `bot:Building` and `crmba:B1_Built_Work`).
- Capture present-day topology with BOT (`bot:containsZone`, `bot:adjacentZone`, `bot:intersectsZone`, `bot:hasSpace`, `bot:containsElement`).
- Capture historical layers with CIDOC CRM events (`crm:E12_Production`, `crm:E11_Modification`), agents, materials, and time-spans.
- Reconcile external concepts with `skos:exactMatch` (Getty AAT, Wikidata). Do not use `owl:sameAs` for AAT or Wikidata types.
- Enrich records with IIIF Presentation API 3.0 manifests for plans, photographs, and historical documents.
- Maintain a living Wikidata contribution queue against the quality bar of [Q42627405](https://www.wikidata.org/wiki/Q42627405) and [Q5905596](https://www.wikidata.org/wiki/Q5905596).
- Export at least ten detailed records into [MehranDHN/persarch](https://github.com/MehranDHN/persarch) as proof that the persarch approach aligns with real instances.

Namespace: `https://w3id.org/persian-architecture#` (persarch) and `https://w3id.org/persian-caravanserai-kg#` (this graph).

## Ontology alignment

The ontology **must follow and extend** [MehranDHN/persarch](https://github.com/MehranDHN/persarch):

| Layer | Vocabulary | Role |
| --- | --- | --- |
| Topology | BOT | `bot:Site`, `bot:Building`, `bot:Storey`, `bot:Space` / bare `bot:Zone`, `bot:Element` |
| Persian types | persarch | `persarch:Caravanserai`, `Sahn`, `Iwan`, `Stable`, `Hashti`, `Hujra`, dual-court / four-iwan / circular subclasses |
| History | CIDOC CRM + CRMba | `crmba:B1_Built_Work`; `E12`/`E11` for foundation and restoration; `P14` role shortcuts `commissionedBy`, `designedBy`, `executedBy` |
| Place | GeoSPARQL | `geo:asWKT` |
| Media | persarch + IIIF 3.0 | `persarch:hasPresentation`, `hasIiifManifest` |

See `ontology/persarch-caravanserai-extension.ttl`.

## Data sources

| Source | Type | Coverage | Harvesting |
| --- | --- | --- | --- |
| **Wikidata** | SPARQL | Instances of [Q186347](https://www.wikidata.org/wiki/Q186347) in Iran (P17 = Q794), plus parts of [Q66030932](https://www.wikidata.org/wiki/Q66030932). **466 items** in the current harvest; most are **not** UNESCO components. | Automatable. `scripts/harvest_wikidata.py` |
| **UNESCO WHC 1668** | Semi-structured | The **54** inscribed Persian Caravanserais ([whc.unesco.org/en/list/1668](https://whc.unesco.org/en/list/1668/)): official names, coordinates, property/buffer areas. | Automatable from the maps table. `scripts/harvest_unesco.py` |
| **MIFAO 81** | Unstructured | Maxime Siroux, *Caravansérails d'Iran et petites constructions routières* (IFAO, 1949). [Internet Archive](https://archive.org/details/MIFAO81). | OCR + **human-in-the-loop**. |
| **MIFAO 82** | Unstructured | Maxime Siroux, *Anciennes voies et monuments routiers de la région d'Ispahân* (IFAO, 1971). [Internet Archive](https://archive.org/details/MIFAO82). ~60 caravanserais around Isfahan. | OCR + **human-in-the-loop**. |

Human review is a first-class requirement for MIFAO. Automated extraction produces *candidates*; only accepted rows are ingested or proposed to Wikidata.

## UNESCO 1668 ↔ Wikidata one-to-one comparison

Every UNESCO component is joined to a Wikidata item by World Heritage Site ID (`P757` = `1668-xxx`) or, if that statement is missing, by coordinates (≤ 2.5 km) plus a name-token check.

Full machine-readable table: [`docs/unesco-wikidata-comparison.csv`](docs/unesco-wikidata-comparison.csv). Narrative copy: [`docs/unesco-wikidata-comparison.md`](docs/unesco-wikidata-comparison.md). RDF links: `data/unesco-wikidata-links.ttl`.

### Counts (harvest of 2026-03-30)

| Measure | n |
| --- | --- |
| UNESCO components (WHC 1668) | **54** |
| Wikidata Iranian caravanserais harvested (Q186347 in Iran ∪ parts of Q66030932) | **466** |
| UNESCO components with a Wikidata item | **54 / 54** |
| Matched by `P757` | 38 |
| Matched by coordinates + name (UNESCO membership not yet stated on the item) | 16 |
| Stub that should be completed as a new/near-new item | **1** (1668-044 Khan → [Q138647472](https://www.wikidata.org/wiki/Q138647472), no English/Persian label) |
| Existing items below the Q42627405 / Q5905596 blueprint | **53** |
| Wikidata caravanserais in Iran that are **not** in the UNESCO serial | **412** |

Almost every UNESCO row already exists on Wikidata. The contribution work is **enrichment** (especially `P361` → Q66030932 and missing `P757`), plus **new items** that will come from MIFAO 81/82 after editorial review.

Name note: UNESCO **1668-002 Noushirvan** is the same building as Wikidata [Q5873186](https://www.wikidata.org/wiki/Q5873186) *Ahvan Stone Caravanserai* (P757 match, 10 m). UNESCO **1668-003 Āhovān** is the adjacent Shah Abbasi building [Q5891443](https://www.wikidata.org/wiki/Q5891443).

### One-to-one table

| UNESCO ID | UNESCO name | Province | Wikidata | WD label | Match | km | Action | Blueprint gaps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1668-001 | Deyr-e Gachin | Qom | [Q6394061](https://www.wikidata.org/wiki/Q6394061) | Dayr-e Gachin Caravanserai | P757 | 0.009 | enrich | P361→Q66030932 |
| 1668-002 | Noushirvan | Semnan | [Q5873186](https://www.wikidata.org/wiki/Q5873186) | Ahvan Stone Caravanserai | P757 | 0.010 | enrich | P361→Q66030932 |
| 1668-003 | Ahovan | Semnan | [Q5891443](https://www.wikidata.org/wiki/Q5891443) | Shah Abbasi Caravanserai of Ahvan | P757 | 0.015 | enrich | P361→Q66030932 |
| 1668-004 | Parand | Tehran | [Q42575545](https://www.wikidata.org/wiki/Q42575545) | Robat Karim Stone Caravanserai | P757 | 0.008 | enrich | P361→Q66030932; P571/P1619 |
| 1668-005 | Robat-e Sharaf | Razavi Khorasan | [Q2577338](https://www.wikidata.org/wiki/Q2577338) | Sharaf Caravanserai | P757 | 0.023 | enrich | P361→Q66030932 |
| 1668-006 | Anjireh Ajori | Yazd | [Q122706913](https://www.wikidata.org/wiki/Q122706913) | Anjireh Brick Caravanserai | P757 | 0.006 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-007 | Anjireh Sangi | Yazd | [Q5911963](https://www.wikidata.org/wiki/Q5911963) | Anjireh Stone Caravanserai | P757 | 0.002 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-008 | Abbas Abad Taybad | Razavi Khorasan | [Q109340152](https://www.wikidata.org/wiki/Q109340152) | Abbasabad Caravanserai | P757 | 0.010 | enrich | P1369; P361→Q66030932; P571/P1619 |
| 1668-009 | Jamal Abad | East Azerbaijan | [Q5907713](https://www.wikidata.org/wiki/Q5907713) | Jamalabad Caravanserai | P757 | 0.005 | enrich | P361→Q66030932 |
| 1668-010 | Qelli | North Khorasan | [Q6537569](https://www.wikidata.org/wiki/Q6537569) | Qelli Caravanserai | P757 | 0.010 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-011 | Fakhr-e Davud | Razavi Khorasan | [Q5813213](https://www.wikidata.org/wiki/Q5813213) | Fakhr-e Davud Caravanserai | P757 | 0.010 | enrich | P361→Q66030932 |
| 1668-012 | Sheikhali Khan | Isfahan | [Q5905596](https://www.wikidata.org/wiki/Q5905596) | Chaleh Siah Caravanserai | P757 | 0.008 | enrich | P361→Q66030932 |
| 1668-013 | Maranjab | Isfahan | [Q5730585](https://www.wikidata.org/wiki/Q5730585) | Maranjab Caravanserai | P757 | 0.000 | enrich | P361→Q66030932 |
| 1668-014 | Amin Abad | Isfahan | [Q5907540](https://www.wikidata.org/wiki/Q5907540) | Aminabad Caravanserai | P757 | 0.006 | enrich | P361→Q66030932 |
| 1668-015 | Gabr Abad | Isfahan | [Q5873197](https://www.wikidata.org/wiki/Q5873197) | Gabrabad Caravanserai | P757 | 0.013 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-016 | Mahyar | Isfahan | [Q5904114](https://www.wikidata.org/wiki/Q5904114) | Mahyar Caravanserai | P757 | 0.011 | enrich | P361→Q66030932 |
| 1668-017 | Gaz | Isfahan | [Q5871566](https://www.wikidata.org/wiki/Q5871566) | Gaz Caravanserai | P757 | 0.009 | enrich | P361→Q66030932; P571/P1619 |
| 1668-018 | Kuhpayeh | Isfahan | [Q5906011](https://www.wikidata.org/wiki/Q5906011) | Kuhpayeh Caravanserai | P757 | 0.008 | enrich | P18; P361→Q66030932 |
| 1668-019 | Mazinan | Razavi Khorasan | [Q5904562](https://www.wikidata.org/wiki/Q5904562) | Mazinan Caravanserai | P757 | 0.004 | enrich | P361→Q66030932 |
| 1668-020 | Mehr | Razavi Khorasan | [Q5900091](https://www.wikidata.org/wiki/Q5900091) | Mehr Caravanserai | P757 | 0.008 | enrich | P361→Q66030932; P571/P1619 |
| 1668-021 | Zaferaniyeh | Razavi Khorasan | [Q5923727](https://www.wikidata.org/wiki/Q5923727) | Zafaraniyeh Caravanserai | P757 | 0.004 | enrich | P361→Q66030932; P571/P1619 |
| 1668-022 | Fakhr Abad | Razavi Khorasan | [Q5913234](https://www.wikidata.org/wiki/Q5913234) | Fakhrabad Caravanserai | P757 | 0.266 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-023 | Sarayan | South Khorasan | [Q5893109](https://www.wikidata.org/wiki/Q5893109) | Sarayan Caravanserai | P757 | 0.007 | enrich | P361→Q66030932 |
| 1668-024 | Qasr-e Bahram | Semnan | [Q5867812](https://www.wikidata.org/wiki/Q5867812) | Qasr-e Bahram Caravanserai | P757 | 0.003 | enrich | P361→Q66030932 |
| 1668-025 | Mayamey | Semnan | [Q5892124](https://www.wikidata.org/wiki/Q5892124) | Meyami Caravanserai | P757 | 0.008 | enrich | P361→Q66030932 |
| 1668-026 | Abbas Abad | Semnan | [Q5915113](https://www.wikidata.org/wiki/Q5915113) | Shah Abbasi Caravanserai of Abbasabad | P757 | 0.013 | enrich | P361→Q66030932; P571/P1619 |
| 1668-027 | Miandasht | Semnan | [Q5705395](https://www.wikidata.org/wiki/Q5705395) | Miandasht Caravanserai | P757 | 0.074 | enrich | P361→Q66030932 |
| 1668-028 | Zeynoddin | Yazd | [Q15068974](https://www.wikidata.org/wiki/Q15068974) | Zein-o-Din Caravanserai | P757 | 0.011 | enrich | P361→Q66030932 |
| 1668-029 | Meybod | Yazd | [Q5887312](https://www.wikidata.org/wiki/Q5887312) | Meybod Caravanserai | P757 | 0.013 | enrich | P361→Q66030932 |
| 1668-030 | Farasfaj | Hamedan | [Q5907778](https://www.wikidata.org/wiki/Q5907778) | Farasfaj Caravanserai | P757 | 0.003 | enrich | P361→Q66030932 |
| 1668-031 | Izadkhast | Fars | [Q5873579](https://www.wikidata.org/wiki/Q5873579) | Izadkhast Caravanserai | geo+name | 0.015 | enrich | P361→Q66030932; P757 1668-031 |
| 1668-032 | Bisotun | Kermanshah | [Q5908224](https://www.wikidata.org/wiki/Q5908224) | Shah Abbasi Caravanserai of Bisotun | geo+name | 0.012 | enrich | P361→Q66030932; P757 1668-032 |
| 1668-033 | Ganjali Khan | Kerman | [Q5905314](https://www.wikidata.org/wiki/Q5905314) | Ganjali Khan Caravanserai | geo+name | 0.014 | enrich | P361→Q66030932; P757 1668-033 |
| 1668-034 | Yengeh Emam | Alborz | [Q5902267](https://www.wikidata.org/wiki/Q5902267) | Yengi Emam Caravanserai | geo+name | 0.001 | enrich | P361→Q66030932; P757 1668-034 |
| 1668-035 | Khajeh Nazar | East Azerbaijan | [Q6558875](https://www.wikidata.org/wiki/Q6558875) | Khajeh Nazar Caravanserai | P757 | 0.007 | enrich | P361→Q66030932 |
| 1668-036 | Goujebel | East Azerbaijan | [Q5907181](https://www.wikidata.org/wiki/Q5907181) | Guycheh Bil Caravanserai | geo | 0.769 | enrich | P361; P757; P571/P1619; P186; P149 |
| 1668-037 | Saeen | Ardabil | [Q5928207](https://www.wikidata.org/wiki/Q5928207) | Sain Stone Caravanserai | P757 | 0.004 | enrich | P361→Q66030932; P571/P1619 |
| 1668-038 | Titi | Gilan | [Q5888547](https://www.wikidata.org/wiki/Q5888547) | Titi Caravanserai | geo+name | 0.006 | enrich | P361→Q66030932; P757 1668-038 |
| 1668-039 | Dehdasht | Kohgiluyeh and Boyer-Ahmad | [Q5899756](https://www.wikidata.org/wiki/Q5899756) | Dehdasht Caravanserai | geo+name | 0.132 | enrich | P361; P757; P571/P1619; P186; P149 |
| 1668-040 | Khoy | West Azerbaijan | [Q42708726](https://www.wikidata.org/wiki/Q42708726) | Shah Abbasi Caravanserai of Khoy | geo+name | 1.122 | enrich | P131; P18; P361; P757; P571/P1619; P186; P149 |
| 1668-041 | Bagh-e Sheikh | Markazi | [Q5917647](https://www.wikidata.org/wiki/Q5917647) | Bagh-e Sheikh Caravanserai | P757 | 0.005 | enrich | P361→Q66030932 |
| 1668-042 | Neyestanak | Isfahan | [Q5904265](https://www.wikidata.org/wiki/Q5904265) | Neyestanak Caravanserai | P757 | 0.007 | enrich | P361→Q66030932; P571/P1619 |
| 1668-043 | Chehel Payeh | Kerman | [Q5945649](https://www.wikidata.org/wiki/Q5945649) | Chehel Payeh Caravanserai | P757 | 0.005 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-044 | Khan | South Khorasan | [Q138647472](https://www.wikidata.org/wiki/Q138647472) | *(stub, no label)* | geo | 0.011 | **new/complete** | labels; P1435; P1369; P18; P361; P757; P571; P186; P149 |
| 1668-045 | Deh Mohammad | South Khorasan | [Q5868984](https://www.wikidata.org/wiki/Q5868984) | Deh-e Mohammad Caravanserai | P757 | 0.004 | enrich | P361→Q66030932 |
| 1668-046 | Taj Abad | Hamedan | [Q5904949](https://www.wikidata.org/wiki/Q5904949) | Tajabad Caravanserai | geo | 0.006 | enrich | P361→Q66030932; P757 1668-046 |
| 1668-047 | Chah Kuran | Kerman | [Q5910864](https://www.wikidata.org/wiki/Q5910864) | Chah Kuran Caravanserai | P757 | 0.007 | enrich | P361→Q66030932 |
| 1668-048 | Kharanaq | Yazd | [Q5887896](https://www.wikidata.org/wiki/Q5887896) | Kharanaq Caravanserai | geo+name | 0.009 | enrich | P361→Q66030932; P757 1668-048 |
| 1668-049 | Rashti | Yazd | [Q5905602](https://www.wikidata.org/wiki/Q5905602) | Rashti Caravanserai | geo+name | 0.006 | enrich | P361→Q66030932; P757 1668-049 |
| 1668-050 | Borazjan | Bushehr | [Q5894632](https://www.wikidata.org/wiki/Q5894632) | Moshir al-Molk Caravanserai | geo | 0.024 | enrich | P361→Q66030932; P757 1668-050 |
| 1668-051 | Chameshk | Lorestan | [Q5677204](https://www.wikidata.org/wiki/Q5677204) | Chameshk Caravanserai | geo+name | 0.014 | enrich | P18; P361; P757; P571/P1619; P186; P149 |
| 1668-052 | Afzal | Khuzestan | [Q5895519](https://www.wikidata.org/wiki/Q5895519) | Afzal Caravanserai | geo+name | 0.016 | enrich | P361; P757; P571/P1619; P186; P149 |
| 1668-053 | Bastak | Hormozgan | [Q6394073](https://www.wikidata.org/wiki/Q6394073) | Bastak Caravanserai | P757 | 0.004 | enrich | P361→Q66030932 |
| 1668-054 | Saadossaltaneh | Qazvin | [Q1484050](https://www.wikidata.org/wiki/Q1484050) | Sa'd al-Saltaneh Caravanserai | geo | 0.047 | enrich | P361→Q66030932; P757 1668-054 |

`km` is the haversine distance between the UNESCO centroid and Wikidata `P625`. Rebuild with `python scripts/compare_unesco_wikidata.py`.

## Wikidata enrichment blueprint and candidate list

Minimum quality follows [Q42627405](https://www.wikidata.org/wiki/Q42627405) (Madarshah / Murcheh Khvort — **national heritage, not a 1668 component**) and [Q5905596](https://www.wikidata.org/wiki/Q5905596) (Sheikhali Khan / Chaleh Siah — UNESCO **1668-012**).

**Required**

| Property | Value |
| --- | --- |
| P31 | Q186347 (caravanserai); also Q2065736 when nationally registered |
| P17 | Q794 (Iran) |
| P131 | most specific administrative entity |
| P625 | coordinate location |
| Labels | English + Persian (`P1705` native label) |

**High priority**

| Property | Value |
| --- | --- |
| P1435 | Q5958900 (Iranian National Heritage) with P580 |
| P1369 | national registration number |
| P361 | Q66030932 for UNESCO components |
| P757 | `1668-xxx` for UNESCO components |
| P18 / P373 | image / Commons category |

**Medium:** P186 materials; P571 or P1619 dating; P149 architectural style.

Full checklist and SPARQL: [`docs/wikidata-blueprint.md`](docs/wikidata-blueprint.md).

### Working candidate queue

The living list is [`docs/wikidata-candidates.md`](docs/wikidata-candidates.md). **The editor will extend section C from unstructured MIFAO records after review.** Do not create Wikidata items from OCR-only rows until `persarch:reviewStatus` is `accepted`.

**A. New / stub-complete (UNESCO)**

| UNESCO | Name | Wikidata | What to add (blueprint) |
| --- | --- | --- | --- |
| 1668-044 | Khan (South Khorasan) | [Q138647472](https://www.wikidata.org/wiki/Q138647472) | English and Persian labels; P31 Q186347; P361 Q66030932; P757 `1668-044`; P1435; P1369; P18; dating; materials. Treat as a new item in practice. |

**B. Enrich existing UNESCO items (53)** — every row in the table above. Shared gap: **`P361` part of Q66030932 is missing on all 54**. Sixteen items also lack `P757`. Priority enrichments (most statements missing):

| UNESCO | Item | Extra gaps |
| --- | --- | --- |
| 1668-031 | [Q5873579](https://www.wikidata.org/wiki/Q5873579) Izadkhast | P757 |
| 1668-032 | [Q5908224](https://www.wikidata.org/wiki/Q5908224) Bisotun | P757 |
| 1668-033 | [Q5905314](https://www.wikidata.org/wiki/Q5905314) Ganjali Khan | P757 |
| 1668-034 | [Q5902267](https://www.wikidata.org/wiki/Q5902267) Yengeh Emam | P757 |
| 1668-036 | [Q5907181](https://www.wikidata.org/wiki/Q5907181) Goujebel | P757, dating, materials, style |
| 1668-038 | [Q5888547](https://www.wikidata.org/wiki/Q5888547) Titi | P757 |
| 1668-039 | [Q5899756](https://www.wikidata.org/wiki/Q5899756) Dehdasht | P757, dating, materials, style |
| 1668-040 | [Q42708726](https://www.wikidata.org/wiki/Q42708726) Khoy | P131, P18, P757, dating, materials, style |
| 1668-046–054 | several | P757 (Taj Abad, Kharanaq, Rashti, Borazjan, Chameshk, Afzal, Saadossaltaneh) |

**C. New candidates from unstructured sources (editor-controlled)**

Placeholder rows live in `docs/wikidata-candidates.md` §C and `data/mifao-review-queue.csv`. After MIFAO 81/82 review, each accepted building that is absent from Wikidata becomes a **new-item** candidate modelled on Q42627405; each building that already has an item becomes an **enrich** candidate modelled on Q5905596.

## IIIF enrichment

Every harvested caravanserai can link to an IIIF Presentation API 3.0 Manifest (`persarch:hasIiifManifest`) packing:

- architectural plans (MIFAO, Kleiss, new surveys)
- historical and contemporary photographs
- inscriptions and archival documents

Example manifests: `iiif/`. Pattern: `persarch:hasPresentation` / `persarch:PlanImage` / `persarch:Photograph`.

## Case studies for persarch import

Ten records are modelled with BOT topology + CRM events and designated for import into persarch:

| # | Record | UNESCO | Wikidata | Modelling emphasis |
| --- | --- | --- | --- | --- |
| 1 | Ribat-e Sharaf | 1668-005 | Q2577338 | Dual-court Seljuk; already in persarch |
| 2 | Deyr-e Gachin | 1668-001 | Q6394061 | Sasanian core; “mother” of the series |
| 3 | Sheikhali Khan | 1668-012 | Q5905596 | Wikidata best-practice item |
| 4 | Maranjab | 1668-013 | Q5730585 | Safavid four-iwan desert plan |
| 5 | Zein-o-din | 1668-028 | Q15068974 | Circular plan |
| 6 | Ganjali Khan | 1668-033 | Q5905314 | Urban bazaar caravanserai |
| 7 | Izadkhast | 1668-031 | Q5873579 | Cliff-edge setting |
| 8 | Parand | 1668-004 | Q42575545 | Stone roadside ribat near Tehran |
| 9 | Qasr-e Bahram | 1668-024 | Q5867812 | Stone Safavid, large buffer |
| 10 | Miandasht | 1668-027 | Q5705395 | Multi-building complex (Safavid + Qajar) |

See `case-studies/`.

## Repository structure

```
persian-caravanserai-kg/
├── README.md
├── ontology/          # BOT + CRM extension (persarch namespace)
├── data/              # UNESCO 1668, Wikidata harvest, links, MIFAO queue
├── queries/           # Harvest, gap detection, competency questions
├── docs/              # Blueprint, UNESCO↔Wikidata join, candidates, MIFAO notes
├── iiif/              # IIIF Manifests
├── scripts/           # harvest_wikidata.py, harvest_unesco.py, compare_unesco_wikidata.py
└── case-studies/      # Ten persarch import records
```

## Getting started

```powershell
pip install -r scripts/requirements.txt
python scripts/harvest_unesco.py
python scripts/harvest_wikidata.py
python scripts/compare_unesco_wikidata.py
```

Load `ontology/persarch-caravanserai-extension.ttl`, `data/unesco-1668.ttl`, `data/unesco-wikidata-links.ttl`, `data/wikidata-iran-caravanserais.ttl`, and `case-studies/*.ttl` into a triple store that supports BOT transitive `containsZone` and CRM.

## License

Ontology and instance data: GPL-3.0 (aligned with persarch).  
Documentation: CC BY 4.0.  
Wikidata-derived statements remain CC0. UNESCO descriptions follow WHC terms.

## Related projects

- [MehranDHN/persarch](https://github.com/MehranDHN/persarch)
- [UNESCO WHC 1668](https://whc.unesco.org/en/list/1668/)
- [MIFAO 81](https://archive.org/details/MIFAO81) · [MIFAO 82](https://archive.org/details/MIFAO82)
