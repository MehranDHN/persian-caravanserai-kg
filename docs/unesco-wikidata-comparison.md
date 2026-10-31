# UNESCO 1668 ↔ Wikidata one-to-one comparison

Source: UNESCO WHC maps for [list 1668](https://whc.unesco.org/en/list/1668/maps/) against a Wikidata harvest of instances of [Q186347](https://www.wikidata.org/wiki/Q186347) in Iran plus parts of [Q66030932](https://www.wikidata.org/wiki/Q66030932).

Machine-readable copy: [`unesco-wikidata-comparison.csv`](unesco-wikidata-comparison.csv).

## Counts

| Measure | n |
| --- | --- |
| UNESCO components (WHC 1668) | 54 |
| Wikidata Iranian caravanserai items harvested | 466 |
| UNESCO components with a Wikidata item | 54 |
| Matched by P757 (World Heritage Site ID) | 38 |
| Matched by coordinates + name | 16 |
| UNESCO components with **no** Wikidata item | 1 |
| Existing items below the Q42627405 / Q5905596 bar | 53 |
| Existing items already at the bar | 0 |

Every inscribed component is either linked to an existing Wikidata item or listed as a **new-item** candidate. Wikidata currently has hundreds of Iranian caravanserais that are **not** in the UNESCO serial property; those remain in the harvest graph and are out of scope for this table.

## Comparison table

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
| 1668-031 | Izadkhast | Fars | [Q5873579](https://www.wikidata.org/wiki/Q5873579) | Izadkhast Caravanserai | geo+name | 0.015 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-032 | Bisotun | Kermanshah | [Q5908224](https://www.wikidata.org/wiki/Q5908224) | Shah Abbasi Caravanserai of Bisotun | geo+name | 0.012 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-033 | Ganjali Khan | Kerman | [Q5905314](https://www.wikidata.org/wiki/Q5905314) | Ganjali Khan Caravanserai | geo+name | 0.014 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-034 | Yengeh Emam | Alborz | [Q5902267](https://www.wikidata.org/wiki/Q5902267) | Yengi Emam Caravanserai | geo+name | 0.001 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-035 | Khajeh Nazar | East Azerbaijan | [Q6558875](https://www.wikidata.org/wiki/Q6558875) | Khajeh Nazar Caravanserai | P757 | 0.007 | enrich | P361→Q66030932 |
| 1668-036 | Goujebel | East Azerbaijan | [Q5907181](https://www.wikidata.org/wiki/Q5907181) | Guycheh Bil Caravanserai | geo | 0.769 | enrich | P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-037 | Saeen | Ardabil | [Q5928207](https://www.wikidata.org/wiki/Q5928207) | Sain Stone Caravanserai | P757 | 0.004 | enrich | P361→Q66030932; P571/P1619 |
| 1668-038 | Titi | Gilan | [Q5888547](https://www.wikidata.org/wiki/Q5888547) | Titi Caravanserai | geo+name | 0.006 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-039 | Dehdasht | Kohgiluyeh and Boyer-Ahmad | [Q5899756](https://www.wikidata.org/wiki/Q5899756) | Dehdasht Caravanserai | geo+name | 0.132 | enrich | P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-040 | Khoy | West Azerbaijan | [Q42708726](https://www.wikidata.org/wiki/Q42708726) | Shah Abbasi Caravanserai of Khoy | geo+name | 1.122 | enrich | P131; P18; P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-041 | Bagh-e Sheikh | Markazi | [Q5917647](https://www.wikidata.org/wiki/Q5917647) | Bagh-e Sheikh Caravanserai | P757 | 0.005 | enrich | P361→Q66030932 |
| 1668-042 | Neyestanak | Isfahan | [Q5904265](https://www.wikidata.org/wiki/Q5904265) | Neyestanak Caravanserai | P757 | 0.007 | enrich | P361→Q66030932; P571/P1619 |
| 1668-043 | Chehel Payeh | Kerman | [Q5945649](https://www.wikidata.org/wiki/Q5945649) | Chehel Payeh Caravanserai | P757 | 0.005 | enrich | P18; P361→Q66030932; P571/P1619 |
| 1668-044 | Khan | South Khorasan | [Q138647472](https://www.wikidata.org/wiki/Q138647472) | Q138647472 | geo | 0.011 | new-item | en label; fa label; P1435; P1369; P18; P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-045 | Deh Mohammad | South Khorasan | [Q5868984](https://www.wikidata.org/wiki/Q5868984) | Deh-e Mohammad Caravanserai | P757 | 0.004 | enrich | P361→Q66030932 |
| 1668-046 | Taj Abad | Hamedan | [Q5904949](https://www.wikidata.org/wiki/Q5904949) | Tajabad Caravanserai | geo | 0.006 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-047 | Chah Kuran | Kerman | [Q5910864](https://www.wikidata.org/wiki/Q5910864) | Chah Kuran Caravanserai | P757 | 0.007 | enrich | P361→Q66030932 |
| 1668-048 | Kharanaq | Yazd | [Q5887896](https://www.wikidata.org/wiki/Q5887896) | Kharanaq Caravanserai | geo+name | 0.009 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-049 | Rashti | Yazd | [Q5905602](https://www.wikidata.org/wiki/Q5905602) | Rashti Caravanserai | geo+name | 0.006 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-050 | Borazjan | Bushehr | [Q5894632](https://www.wikidata.org/wiki/Q5894632) | Moshir al-Molk Caravanserai | geo | 0.024 | enrich | P361→Q66030932; P757 1668-xxx |
| 1668-051 | Chameshk | Lorestan | [Q5677204](https://www.wikidata.org/wiki/Q5677204) | Chameshk Caravanserai | geo+name | 0.014 | enrich | P18; P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-052 | Afzal | Khuzestan | [Q5895519](https://www.wikidata.org/wiki/Q5895519) | Afzal Caravanserai | geo+name | 0.016 | enrich | P361→Q66030932; P757 1668-xxx; P571/P1619; P186; P149 |
| 1668-053 | Bastak | Hormozgan | [Q6394073](https://www.wikidata.org/wiki/Q6394073) | Bastak Caravanserai | P757 | 0.004 | enrich | P361→Q66030932 |
| 1668-054 | Saadossaltaneh | Qazvin | [Q1484050](https://www.wikidata.org/wiki/Q1484050) | Sa'd al-Saltaneh Caravanserai | geo | 0.047 | enrich | P361→Q66030932; P757 1668-xxx |

## How matching works

1. **P757.** If a Wikidata item already carries World Heritage Site ID `1668-xxx`, it is bound to that component.
2. **Geo + name.** Otherwise the nearest harvested item within 2.5 km is accepted when the Latin/Persian labels share a significant token (Deyr, Sharaf, Maranjab, …).
3. **New item.** If neither rule fires, the UNESCO component is a candidate for a new Wikidata item. This list will later be extended from MIFAO 81/82 unstructured records.

Distances are haversine kilometres between the UNESCO centroid and Wikidata P625.

## Wikidata items flagged UNESCO but not in this 54-row join

_None._

## Best-practice anchors

Enrichment and new items follow [`wikidata-blueprint.md`](wikidata-blueprint.md), using:

- [Q42627405](https://www.wikidata.org/wiki/Q42627405) Madarshah Caravanserai (national heritage, not a 1668 component)
- [Q5905596](https://www.wikidata.org/wiki/Q5905596) Sheikhali Khan / Chaleh Siah (UNESCO 1668-012)
