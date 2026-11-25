# From Coste plan to BOT topology — Amin-Abad

Amin-Abad (UNESCO [1668-014](https://whc.unesco.org/en/list/1668), Wikidata [Q5907540](https://www.wikidata.org/wiki/Q5907540), Coste’s *Amin-Abad*, PL. LXVI) is the second harvest record whose **present topology** is read from a measured plate. Raster: [`images/plans/amin_abad.png`](../images/plans/amin_abad.png) (4088×5437). Enrichment: [`data/amin-abad-coste.ttl`](../data/amin-abad-coste.ttl) on `:wd_Q5907540`. UNESCO `:amin_abad` stays the harvest stub (`skos:exactMatch`).

Pasangan was the square four-iwan pilot. Amin-Abad is the octagonal pilot at the same instance grain.

## Legend → individuals

Coste’s printed keys (south entrance; north at B):

| Key | Coste | Grain | Class |
| --- | --- | --- | --- |
| 1 | Entrée du Caravansérail | one space | `persarch:PishtaqSpace` |
| 2 | Porche | one space | `persarch:Hashti` |
| 3 | Concierge et dépendance | `_w`, `_e` | `bot:Space` |
| 4 | Escaliers du 1er étage et des Terrasses | `_w`, `_e` | `bot:Element` |
| 5 | Cour | one octagonal sahn | `persarch:Sahn` |
| 6 | Estrade pour la Prière | one element in the sahn | `bot:Element` |
| 7 | Chambres des Voyageurs | series Zone + **20** rooms | `persarch:Hujra` |
| 8 | Écuries | series Zone + **4** diagonal ranges | `persarch:Stable` |
| 9 | Estrades et chambres pour les muletiers | series Zone + **9** labelled rooms | `bot:Space` |
| 10 | Latrines | series Zone + **4** labelled towers | `bot:Space` |
| 11 | Bassin en dehors | one howz outside the envelope | `persarch:Howz` |

Eight unnumbered circular **corner towers**. Storeys: ground (plan), first floor and terrace (coupe A–B / Coste 4; no separate upper plans).

Hujra index: N/S west→east; E/W north→south; NW diagonal inner north-east→south-west. Coste prints **7** on the NW diagonal inner ring; NE/SE/SW diagonals show stable stalls there — those stalls are not minted as hujras. Coste **9** and **10** are minted only where the numeral is on the raster.

## Scale-bar dimensions

Plan 0–40 m ≈ 1010 px (25.25 px/m); coupes 0–20 m share that graphic length. Envelope ±2 m.

| Dimension | Value |
| --- | --- |
| E–W including towers | 64 m |
| N–S including towers | 63 m |
| Octagon envelope area | 3400 m² |
| Courtyard flat-to-flat | 32 m |

UNESCO `propertyAreaHectare` 0.4 ha is the inscribed site, not this envelope.

## Instance presentation (SVG)

Each space and element is a shape in [`docs/infographics/amin-abad-instances.svg`](infographics/amin-abad-instances.svg). The SVG `id` is the RDF local name, so

`amin-abad-instances.svg#wd_Q5907540_hujra_nw_2`

is the presentation of `:wd_Q5907540_hujra_nw_2`. The group carries `data-iri`, `data-locator`, and `data-nbr` (BOT neighbours). Interactive panel: [`amin-abad-instances.html`](infographics/amin-abad-instances.html). Regenerate after TTL edits:

```powershell
python scripts/render_amin_abad_svg.py
```

This is a schematic from the octagon grammar (face + bay + Coste key), not a pixel trace of the lithograph.

Dashed `g.candidate` groups on the NE, E, SE, and SW outer rings are closed rooms visible on PL. LXVI where Coste does not print `9`. They are a morphological census, not RDF. Do not mint them until HITL review (same rule as unlabelled 9/10/7). Method: [`docs/coste-plan-to-bot.md`](coste-plan-to-bot.md#identifying-missed-space-instances). SPARQL: `queries/validate-topology.rq` V4.

## Reconstruction as accuracy test

A BOT graph is accurate when a **plan can be redrawn from the RDF** and match the source plate. Target: more than 90% agreement with Coste PL. LXVI.

Score three layers separately:

1. **Inventory** — count and type of spaces/elements (legend keys, bay index, storeys).
2. **Topology** — adjacency/containment graph (`bot:adjacentZone`, `containsZone`, `hasSpace`, `adjacentElement`). Symmetric BOT `adjacentZone` may be inferred; the census must still be true.
3. **Layout** — a drawable plan. Instance locators (face + bay) plus `persarch:OctagonalCaravanserai` plus E54 lengths give an octagon grammar. Overlay that drawing on the raster.

Inventory and topology can already be checked with SPARQL against this Turtle. Visual overlay above 90% still needs coordinates on the instances (IIIF `#xywh` or GeoSPARQL). Bay index plus metres place rooms on the octagon; they do not yet pin wall thickness or unlabelled stalls.

OWL consistency (BOT transitivity, symmetry, disjoint Space/Element) is a **logical** check. Reconstruction is a **fidelity** check. Both are required.

## Adjacency (from the plan)

- 1 entrance `adjacentZone` 2 porch `adjacentZone` 5 sahn
- 3 concierge and 4 stairs flank the porch, west and east
- 5 sahn `adjacentZone` every court-facing Coste 7; `containsElement` 6
- each Coste 8 range `adjacentZone` its diagonal’s inner 7s and outer 9s
- 10 latrines sit in towers NNW, WNW, WSW, SSW
- 11 basin is outside; the building `adjacentZone` it
