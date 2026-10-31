# Case studies designated for persarch import

These ten records are modelled with BOT topology (spaces, bare zones, elements) and CIDOC CRM events (production, modification, agents, materials). They are the proof that [persarch](https://github.com/MehranDHN/persarch) aligns with real caravanserai instances.

Load `../ontology/persarch-caravanserai-extension.ttl` together with `persarch-import.ttl`.

Ribat-e Sharaf already exists in persarch (`data/ribat-i-sharaf.ttl`) under `https://w3id.org/persian-architecture/data/ribat-sharaf#`. This file restates the dual-court pattern and adds UNESCO / Wikidata / IIIF links so the two graphs join with `skos:exactMatch`.

| # | Local IRI | Name | UNESCO | Wikidata | Why selected |
| --- | --- | --- | --- | --- | --- |
| 1 | `:ribat_sharaf` | Ribat-e Sharaf | 1668-005 | Q2577338 | Dual-court Seljuk; persarch reference |
| 2 | `:deyr_e_gachin` | Deyr-e Gachin | 1668-001 | Q6394061 | Sasanian core; “mother” of the series |
| 3 | `:sheikhali_khan` | Sheikhali Khan | 1668-012 | Q5905596 | Wikidata blueprint item |
| 4 | `:maranjab` | Maranjab | 1668-013 | Q5730585 | Safavid four-iwan desert plan |
| 5 | `:zeynoddin` | Zein-o-din | 1668-028 | Q15068974 | Circular plan, adaptive reuse |
| 6 | `:ganjali_khan` | Ganjali Khan | 1668-033 | Q5905314 | Urban bazaar caravanserai |
| 7 | `:izadkhast` | Izadkhast | 1668-031 | Q5873579 | Cliff-edge topography |
| 8 | `:parand` | Parand | 1668-004 | Q42575545 | Stone roadside ribat |
| 9 | `:qasr_e_bahram` | Qasr-e Bahram | 1668-024 | Q5867812 | Stone Safavid, large buffer |
| 10 | `:miandasht` | Miandasht | 1668-027 | Q5705395 | Multi-court Safavid + Qajar complex |

Import into persarch by copying this Turtle (or per-building subsets) into `persarch/data/` and keeping the `persarch:` class IRIs unchanged.
