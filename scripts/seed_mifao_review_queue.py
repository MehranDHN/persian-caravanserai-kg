#!/usr/bin/env python3
"""Seed the human-editable MIFAO 81/82 review queue.

Names, site numbers, pages, figures, and plates are taken from the printed
tables of contents, name index, table of figures, and table of plates in:

  MIFAO 81  Siroux, Caravansérails d'Iran…, IFAO, 1949
            https://archive.org/details/MIFAO81
  MIFAO 82  Siroux, Anciennes voies… région d'Ispahân, IFAO, 1971
            https://archive.org/details/MIFAO82

OCR of the Internet Archive scans is used only as a finding aid. Spellings
follow the printed index (MIFAO 82 was normalised with Jean Aubin). Status
of every row is `candidate`. Do not mint Wikidata items until reviewStatus
is accepted.

Re-running this script overwrites data/mifao-review-queue.csv and
data/mifao-evidence.csv. After editorial work, treat those CSVs as the
source of truth and do not re-seed.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "mifao-review-queue.csv"
EVIDENCE = ROOT / "data" / "mifao-evidence.csv"
NAME_LIST = ROOT / "docs" / "mifao-name-list.md"

SOURCES = {
    "MIFAO81": {
        "source_id": "MIFAO81",
        "source_name": "Siroux, Maxime. Caravansérails d'Iran et petites constructions routières. Mémoires de l'Institut français d'archéologie orientale, t. 81. Le Caire: IFAO, 1949.",
        "source_short": "MIFAO 81 (Siroux 1949)",
        "year": "1949",
        "ia_item": "https://archive.org/details/MIFAO81",
    },
    "MIFAO82": {
        "source_id": "MIFAO82",
        "source_name": "Siroux, Maxime. Anciennes voies et monuments routiers de la région d'Ispahân. Mémoires de l'Institut français d'archéologie orientale, t. 82. Le Caire: IFAO, 1971.",
        "source_short": "MIFAO 82 (Siroux 1971)",
        "year": "1971",
        "ia_item": "https://archive.org/details/MIFAO82",
    },
}

# evidence tuples: (source_id, kind, locator, detail)
# kind: page | figure | plate | index | itinerary

BUILDINGS = [
    # ------------------------------------------------------------------
    # MIFAO 82 Robâts named in the printed index (editor priority list)
    # ------------------------------------------------------------------
    dict(
        working_id="MIFAO82-robat-agha-kemal",
        siroux_name="Robât-e-âghâ Kemâl",
        siroux_name_alt="Tchâh-gadeh; Aghâ-Kemâl Bala; Robât-âgha-Kemâl",
        normalized_en="Robat-e Agha Kamal / Chahgadeh",
        building_type="caravanserai",
        site_number="20",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        notes="Index: Robât-e-âghâ Kemâl (c.) (ou Tchâh-gadeh). Same as Tchâh-gadeh (Aghâ-Kemâl Bala), site 20. Distinct from Vendâd-deh / Aghâ-Kemâl-Païn (site 24).",
        evidence=[
            ("MIFAO82", "page", "148", "Chap. IX, site 20, caravansérail de Tchâh-gadeh"),
            ("MIFAO82", "index", "20, 148", "Robât-e-âghâ Kemâl (c.) (ou Tchâh-gadeh)"),
            ("MIFAO82", "index", "12, 20-22, 148-151, 155, 162-164, 167, 186, 188-189, 201", "Tchâh-gadeh (c.) (Robât-âgha-Kemâl)"),
            ("MIFAO82", "figure", "fig. 41", "plan, site 20"),
            ("MIFAO82", "plate", "pl. XII F; pl. XIII A-B", "photographs of portail, eïwan, stables"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-atabaki",
        siroux_name="Robât-e-atâbaki",
        siroux_name_alt="Qaleh atâbaki de Dhor; Qaleh Atabaki",
        normalized_en="Robat-e Atabaki / Qaleh Atabaki of Dhar",
        building_type="robat",
        site_number="3",
        period_guess="pre-Seljuk / Atabeg",
        proposed_action="new-item or enrich",
        notes="Index: Robât-e-atâbaki (r.) (ou Qaleh atâbaki). MIFAO 81 also has a later Atabaki caravanserai (plain type) — do not collapse the two without review.",
        evidence=[
            ("MIFAO82", "page", "47", "Chap. III, Qaleh atâbaki de Dhor, site 3"),
            ("MIFAO82", "index", "47", "Robât-e-atâbaki (r.)"),
            ("MIFAO82", "figure", "fig. 5", "plan, site 3"),
            ("MIFAO82", "plate", "pl. III C-D", "photographs"),
            ("MIFAO81", "page", "86", "Caravansérail Atabaki (plain type; confirm identity)"),
            ("MIFAO81", "figure", "fig. 47", "plan (inédit)"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-golkan",
        siroux_name="Robât-e-Golkân",
        siroux_name_alt="Robat-e-Goïkân",
        normalized_en="Robat-e Golkan",
        building_type="robat",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        notes="Index-only. Siroux notes a name on some maps and that the ruin was not found during survey. Keep as unlocated candidate.",
        evidence=[
            ("MIFAO82", "index", "11, 14", "Robât-e-Golkân (r.)"),
            ("MIFAO82", "itinerary", "11, 14", "named on the Delijan / Golpaygan approaches; ruin not located"),
        ],
    ),
    dict(
        working_id="MIFAO81-robat-kerim",
        siroux_name="Robat-e-Kerim",
        siroux_name_alt="Robat-Kérim; Robat Kerim; Caravansérail près de Robat Kerim",
        normalized_en="Robat Karim / Parand",
        building_type="robat",
        site_number="C",
        period_guess="Samanid / 10th c. (Siroux)",
        proposed_unesco_id="1668-004",
        proposed_wikidata="Q42575545",
        proposed_action="enrich",
        notes="First analysed intact building in MIFAO 81 chap. VI. Figure caption says 'près de Robat Kerim'. Proposed join to UNESCO Parand / Wikidata Robat Karim Stone Caravanserai — confirm by plan and coordinates before accepting.",
        evidence=[
            ("MIFAO81", "page", "46-49", "Chap. VI, Caravansérail de Robat-Kérim"),
            ("MIFAO81", "figure", "fig. 14", "plan (inédit), listed as près de Robat Kerim"),
            ("MIFAO81", "plate", "pl. III 1-4", "photographs of angle, iwan, trompillon, portal"),
            ("MIFAO82", "index", "51, 74, 91-92, 117-118", "Robat-e-Kerim (r.); site C = already in Caravansérails d'Iran"),
            ("MIFAO82", "page", "51, 74", "comparative discussion with early courtyard type"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-meymeh",
        siroux_name="Robat-e-Meymeh",
        siroux_name_alt="",
        normalized_en="Robat-e Meymeh",
        building_type="robat",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        notes="Index-only mention on the Meymeh itinerary. No dedicated plan in the figure table.",
        evidence=[
            ("MIFAO82", "index", "12", "Robat-e-Meymeh (r.)"),
            ("MIFAO82", "itinerary", "10-12", "Meymeh as a station on the northern approaches to Isfahan"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-miyan",
        siroux_name="Robât-e-Miyân",
        siroux_name_alt="Bâgh-e-Mirân; Bagh-e-Mirân",
        normalized_en="Robat-e Miyan / Bagh-e Miran",
        building_type="robat",
        site_number="",
        period_guess="Seljuk?",
        proposed_action="new-item or enrich",
        notes="Index: Robât-e-Miyân (r.) (ou Bâgh-e-Mirân). Treated with the Robâts of Bâgh-e-Mirân and Mourtcheh-Khort in chap. IV p. 87.",
        evidence=[
            ("MIFAO82", "page", "87-88", "Chap. IV, les Robâts de Bâgh-e-Mirân et de Mourtcheh-Khort"),
            ("MIFAO82", "index", "18, 87", "Bagh-e-Mirân (s.) (Robât-e-Miyân)"),
            ("MIFAO82", "index", "22, 87-88, 92, 113, 209", "Robât-e-Miyân (r.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-mourtcheh-khort",
        siroux_name="Robât-e-Mourtcheh-Khort",
        siroux_name_alt="Robât-e-Mourtcheh-Kort; qaleh of Mourtcheh-Kort",
        normalized_en="Robat-e Murcheh Khvort (early ribat)",
        building_type="robat",
        site_number="",
        period_guess="pre-Safavid ribat",
        proposed_action="new-item or enrich",
        notes="Early ribat at Murcheh Khvort, distinct from the royal Safavid Mâder-e-Châh caravanserai at the same station (Q42627405). Harvesting notes already flag this adaptive-reuse / two-building risk.",
        evidence=[
            ("MIFAO82", "page", "87", "Chap. IV, Robâts de Bâgh-e-Mirân et de Mourtcheh-Khort"),
            ("MIFAO82", "index", "87", "Robât-e-Mourtcheh-Khort (r.)"),
            ("MIFAO82", "index", "10-11, 15-19, 21-22, 25, 40, 44, 87, 109, 164, 175, 192, 194, 216", "Mourtcheh-Kort (s.) station"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-sanches",
        siroux_name="Robât-e-Sanchés",
        siroux_name_alt="Robat-é-Senchas (MIFAO 81, citing Survey)",
        normalized_en="Robat-e Sanches",
        building_type="robat",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        notes="Index entry without (c.)/(r.) qualifier. MIFAO 81 mentions Robat-é-Senchas via Survey. Confirm whether this is a building Siroux visited or a literature citation.",
        evidence=[
            ("MIFAO82", "index", "92, 97", "Robât-e-Sanchés"),
            ("MIFAO81", "page", "see chap. VI notes", "Robat-é-Senchas cited from Survey (OCR; confirm printed page)"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-sangui-aliabad",
        siroux_name="Robât-e-Sangui (d'Ali-âbâd)",
        siroux_name_alt="Qaleh-sangui d'Ali-âbâd",
        normalized_en="Robat-e Sangi of Aliabad",
        building_type="robat",
        site_number="",
        period_guess="early Islamic / stone fort",
        proposed_action="new-item or enrich",
        notes="Stone ribat, not the large Qajar Ali-Abad complex on the Tehran–Qom road (MIFAO 81 p. 92).",
        evidence=[
            ("MIFAO82", "index", "91-93", "Robât-e-Sangui (d'Ali-âbâd)"),
            ("MIFAO82", "figure", "fig. 13", "Plan du Qaleh sangui d'Ali-âbâd (site C in figure table)"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-sangui-allahvidjeh",
        siroux_name="Robât-e-Sangui (d'Allah-vidjeh)",
        siroux_name_alt="Qaleh-Sangui du col d'Allah-vidjeh; Qaleh-sangui d'Allahvidjeh",
        normalized_en="Robat-e Sangi of Allahvidjeh pass",
        building_type="robat",
        site_number="9",
        period_guess="13th–14th c. (Siroux chap. V)",
        proposed_action="new-item or enrich",
        notes="Site 9. Index also lists Allah-vidjeh (s. car.).",
        evidence=[
            ("MIFAO82", "page", "98", "Chap. V, Qaleh Sangui du col d'Allah-vidjeh, site 9"),
            ("MIFAO82", "index", "10, 119-121, 130", "Robât-e-Sangui (d'Allah-vidjeh)"),
            ("MIFAO82", "index", "98, 116-117, 119-121, 130, 133", "Qaleh-Sangui d'Allahvidjeh"),
            ("MIFAO82", "figure", "fig. 23", "plan, site 9"),
            ("MIFAO82", "plate", "pl. VII E-F", "photographs of south facade and east wing ruins"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-sangui-natanz",
        siroux_name="Robât-e-Sangui (de Natanz)",
        siroux_name_alt="Qaleh-Sangui (de Natanz); Robât-e-sangui de Natanz",
        normalized_en="Robat-e Sangi of Natanz",
        building_type="robat",
        site_number="2 / 6",
        period_guess="Sasanian core; later additions (site 6)",
        proposed_action="new-item or enrich",
        notes="Site 2 (early stone fort) with site 6 additions. Distinct from the large Safavid Natanz caravanserai (site C, MIFAO 81 Natenz).",
        evidence=[
            ("MIFAO82", "page", "44", "Chap. III, site 2"),
            ("MIFAO82", "page", "74", "Chap. IV, adjonctions, site 6"),
            ("MIFAO82", "index", "23, 44, 48, 55, 74, 81, 91-93, 115-118, 121, 272", "Robât-e-Sangui (de Natanz)"),
            ("MIFAO82", "figure", "fig. 4", "plan, site 6 in caption table / site 2 in TOC"),
            ("MIFAO82", "plate", "pl. II E-F; pl. III A-B", "photographs of facades and doors"),
        ],
    ),
    dict(
        working_id="MIFAO81-robat-sharaf",
        siroux_name="Robat-e-Sharraf",
        siroux_name_alt="Robat-Sharaf; Robat-é-Sharaf; Robât-e-Sharraf",
        normalized_en="Ribat-e Sharaf",
        building_type="caravanserai",
        site_number="C",
        period_guess="Seljuk",
        proposed_unesco_id="1668-005",
        proposed_wikidata="Q2577338",
        proposed_action="enrich",
        notes="Dual-court Seljuk ribat. Already a persarch case study. Proposed UNESCO/Wikidata join is strong by name; still confirm against Siroux's description before accepting MIFAO plans into the graph.",
        evidence=[
            ("MIFAO81", "page", "49-51", "Chap. VI, Caravansérail Robat-Sharaf"),
            ("MIFAO82", "index", "91-92, 116-117, 119", "Robat-e-Sharraf (c.)"),
            ("MIFAO82", "page", "91-92", "comparative discussion of early dual-court type"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-soltan-sassanid",
        siroux_name="Robât-e-Soltân",
        siroux_name_alt="Robat-e-Soltan (Sassanide); site 1",
        normalized_en="Robat-e Soltan (Sasanian post)",
        building_type="robat",
        site_number="1",
        period_guess="Sasanian",
        proposed_action="new-item or enrich",
        notes="Siroux splits the oasis: Sasanian fort (site 1) vs Seljuk caravanserai (site 5). Keep two working IDs until a reviewer decides they are one heritage item with phases.",
        evidence=[
            ("MIFAO82", "page", "40", "Chap. III, Robat-e-Soltân site 1"),
            ("MIFAO82", "index", "40, 44, 48, 55, 272, 289, 291", "Robât-e-Soltân (q.) (Sassanide)"),
            ("MIFAO82", "figure", "fig. 1-3", "ensemble, complexe, fortin; site 5 captions in figure table overlap — check plates"),
            ("MIFAO82", "plate", "pl. II A-D", "photographs of the Sasanian post"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-soltan-seljuk",
        siroux_name="Robât-e-Soltân (Seldjoucide)",
        siroux_name_alt="Robât-e-Soltân 2e époque; site 5",
        normalized_en="Robat-e Soltan (Seljuk caravanserai)",
        building_type="caravanserai",
        site_number="5",
        period_guess="Seljuk",
        proposed_action="new-item or enrich",
        notes="Second and third periods at the same oasis as site 1. Fig. 16 = 2e époque.",
        evidence=[
            ("MIFAO82", "page", "66", "Chap. IV, Robât-e-Soltân deuxième époque, site 5"),
            ("MIFAO82", "index", "68, 74, 85, 91-93, 105, 116, 118, 120, 139", "Robât-e-Soltân (Seldjoucide)"),
            ("MIFAO82", "figure", "fig. 16", "plan 2e et 3e époque, site 5"),
            ("MIFAO82", "plate", "pl. V A-F", "photographs of portal, iwans, courts"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-turk",
        siroux_name="Robât-e-Turk",
        siroux_name_alt="Robat-é-Turk",
        normalized_en="Robat-e Tork",
        building_type="robat",
        site_number="7",
        period_guess="Seljuk (two phases)",
        proposed_action="new-item or enrich",
        notes="Site 7. Dimensions given by Siroux 76.30 x 71.60 m. Two reconstructed states (fig. 17-19).",
        evidence=[
            ("MIFAO82", "page", "75-87", "Chap. IV, site 7, première et deuxième époque seldjoucide"),
            ("MIFAO82", "index", "12, 14, 16, 75, 87-88, 91-93, 111, 113, 116, 118, 120-121, 188, 209, 272", "Robât-e-Turk (q.)"),
            ("MIFAO82", "figure", "fig. 17-19", "état actuel; plan 1re époque; plan 2e époque"),
            ("MIFAO82", "plate", "pl. VI A-F; pl. VII A", "photographs of towers, portal, vaults"),
            ("MIFAO81", "itinerary", "17", "car. Robat-é-Turk on the Qom–Isfahan itinerary"),
        ],
    ),
    dict(
        working_id="MIFAO82-robat-zendan",
        siroux_name="Robât-e-Zendân",
        siroux_name_alt="Robat de Zendum; prison d'Haroun-al-Rachid; Zendand",
        normalized_en="Robat-e Zendan / Zendum",
        building_type="robat",
        site_number="",
        period_guess="early Islamic (Siroux chap. VII in MIFAO 81)",
        proposed_action="new-item or enrich",
        notes="MIFAO 81 monograph 'Le Robat de Zendum' with plans after Bazargan. MIFAO 82 index: Robât-e-Zendân (q.) (ou prison d'Haroun-al-Rachid).",
        evidence=[
            ("MIFAO81", "page", "103-106", "Chap. VII, Le Robat de Zendum"),
            ("MIFAO81", "figure", "fig. 63-65", "plans and sections after M. Bazargan"),
            ("MIFAO81", "plate", "pl. XI 4-6", "exterior and trompillons"),
            ("MIFAO82", "index", "47", "Robât-e-Zendân (q.)"),
            ("MIFAO82", "index", "47", "Haroun-al-Rachid (e.) (prison ou Zendand)"),
        ],
    ),
    # ------------------------------------------------------------------
    # MIFAO 82 numbered roadside monuments (Isfahan region)
    # ------------------------------------------------------------------
    dict(
        working_id="MIFAO82-tchah-e-siyah-qadim",
        siroux_name="Tchâh-e-siyâh qadim",
        siroux_name_alt="Tchâb-e-siyâh qadim; Kunâr-e-Siyâh related type",
        normalized_en="Chah Siah qadim (old Chaleh Siah)",
        building_type="caravanserai",
        site_number="4",
        period_guess="pre-Seljuk / early Islamic",
        proposed_action="new-item or enrich",
        notes="Old Chah Siah. Do not merge with Tchâh-e-siyâh now (site 27 / UNESCO Sheikhali Khan) without review. Two buildings at one station is a known Siroux pattern.",
        evidence=[
            ("MIFAO82", "page", "57-66", "Chap. IV, Tchâh-e-Siyâh Qadim, site 4"),
            ("MIFAO82", "index", "10, 15, 49, 57, 64-66, 91, 116, 118-119, 121, 175", "Tchâh-e-siyâh qadim (c.)"),
            ("MIFAO82", "figure", "fig. 9-12", "site, état actuel, restitution, details"),
            ("MIFAO82", "plate", "pl. III F; pl. IV A-E", "photographs of portal, gallery, court"),
        ],
    ),
    dict(
        working_id="MIFAO82-qaleh-vedar",
        siroux_name="Qaleh Védar",
        siroux_name_alt="Qaleh-Védar; kaleh de Yedar; Vedar (q.)",
        normalized_en="Qaleh Vedar",
        building_type="qaleh",
        site_number="4 B",
        period_guess="",
        proposed_action="review-type",
        notes="Site 4 B, treated with Tchâh-e-siyâh qadim. Confirm whether this is a caravanserai or a castle.",
        evidence=[
            ("MIFAO82", "page", "66", "Chap. IV, Qaleh de Vedar, site 4 B"),
            ("MIFAO82", "figure", "fig. 15", "croquis du kaleh de Yedar"),
            ("MIFAO82", "plate", "pl. IV F", "vue sud-ouest"),
        ],
    ),
    dict(
        working_id="MIFAO82-tchahar-bordj",
        siroux_name="Tchahâr-Bordj",
        siroux_name_alt="Caravansérail Tchahâr-bordj",
        normalized_en="Chahar Borj",
        building_type="caravanserai",
        site_number="8",
        period_guess="13th–14th c.",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "95", "Chap. V, site 8"),
            ("MIFAO82", "index", "57, 95, 98, 116-117, 119-121, 124, 135, 156, 175", "Tchahâr-bordj (c.)"),
            ("MIFAO82", "figure", "fig. 22", "plan, site 8"),
            ("MIFAO82", "plate", "pl. VII C-D", "south facade and court north facade"),
        ],
    ),
    dict(
        working_id="MIFAO82-tchahar-abad-b",
        siroux_name="Tchahâr-âbâd B",
        siroux_name_alt="Tchahâr-âbâd (c.) building B",
        normalized_en="Chaharabad B",
        building_type="caravanserai",
        site_number="12",
        period_guess="13th–14th c.",
        proposed_action="new-item or enrich",
        notes="Siroux splits Tchahâr-âbâd into B (site 12, chap. V) and A (site 10, Ilkhanid casernement, chap. VI).",
        evidence=[
            ("MIFAO82", "page", "99", "Chap. V, Tchahâr-âbâd B, site 12"),
            ("MIFAO82", "figure", "fig. 24-25", "ensemble A et B; état actuel B"),
            ("MIFAO82", "plate", "pl. VIII A", "portail du caravansérail B"),
        ],
    ),
    dict(
        working_id="MIFAO82-tchahar-abad-a",
        siroux_name="Tchahâr-âbâd A",
        siroux_name_alt="casernement Tchahâr-âbâd A",
        normalized_en="Chaharabad A",
        building_type="casernement",
        site_number="10",
        period_guess="Ilkhanid",
        proposed_action="review-type",
        evidence=[
            ("MIFAO82", "page", "105", "Chap. VI, Tchahâr-âbâd A, site 10"),
            ("MIFAO82", "index", "10, 28, 90, 99, 105, 107-109, 113, 118-121, 167, 182, 187-188", "Tchahâr-âbâd (c.)"),
            ("MIFAO82", "figure", "fig. 24, 26", "ensemble; état actuel A"),
            ("MIFAO82", "plate", "pl. VIII B", "salle nord-est of A"),
        ],
    ),
    dict(
        working_id="MIFAO82-dombi-casernement",
        siroux_name="Dombi A",
        siroux_name_alt="casernements de Dombi",
        normalized_en="Dombi barracks",
        building_type="casernement",
        site_number="11",
        period_guess="Ilkhanid–pre-Safavid",
        proposed_action="review-type",
        notes="Same oasis later has a Safavid caravanserai (site 19). Keep separate.",
        evidence=[
            ("MIFAO82", "page", "107", "Chap. VI, Dombi A, site 11"),
            ("MIFAO82", "figure", "fig. 27", "plan des casernements"),
            ("MIFAO82", "plate", "pl. VIII C-F", "photographs of the barracks"),
        ],
    ),
    dict(
        working_id="MIFAO82-gourgab",
        siroux_name="Qaleh de Gourgâb",
        siroux_name_alt="casernement de Goürgab",
        normalized_en="Gurgab qaleh",
        building_type="casernement",
        site_number="28 bis",
        period_guess="Ilkhanid–pre-Safavid",
        proposed_action="review-type",
        evidence=[
            ("MIFAO82", "page", "109", "Chap. VI, Qaleh de Gourgâb, site 28 bis"),
            ("MIFAO82", "figure", "fig. 28", "plan et coupe"),
            ("MIFAO82", "plate", "pl. IX A-B", "photographs"),
        ],
    ),
    dict(
        working_id="MIFAO82-qaleh-moutah",
        siroux_name="Qaleh de Moutah",
        siroux_name_alt="Qaleh Moutah",
        normalized_en="Muteh qaleh",
        building_type="qaleh",
        site_number="28 E",
        period_guess="",
        proposed_action="review-type",
        notes="Distinct from the Safavid caravanserai of Moutah (site 14 B).",
        evidence=[
            ("MIFAO82", "page", "111", "Chap. VI, Qaleh de Moutah, site 28 E"),
            ("MIFAO82", "figure", "fig. 29", "croquis"),
            ("MIFAO82", "plate", "pl. IX C-D", "court facades"),
        ],
    ),
    dict(
        working_id="MIFAO81-mahyar",
        siroux_name="Mâhyâr",
        siroux_name_alt="Maïar; Caravansérail Maïar",
        normalized_en="Mahyar",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_unesco_id="1668-016",
        proposed_wikidata="Q5904114",
        proposed_action="enrich",
        evidence=[
            ("MIFAO81", "page", "58", "Chap. VI, Caravansérail Maïar"),
            ("MIFAO81", "figure", "fig. 19", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. IV 5; pl. V 2, 6", "court, iwan, entrance and bazaar"),
            ("MIFAO82", "page", "123", "Chap. VIII, Caravansérail Mâhyâr, site C"),
            ("MIFAO82", "figure", "fig. 30", "plan"),
            ("MIFAO82", "plate", "pl. X D", "niche on exterior facade"),
            ("MIFAO82", "index", "32, 123, 126, 133, 135, 164, 185, 187, 189, 194", "Mâhyâr (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-dhor",
        siroux_name="Dhor",
        siroux_name_alt="car. de Dhor; Dhôr",
        normalized_en="Dhar / Deh-e Hur?",
        building_type="caravanserai",
        site_number="13",
        period_guess="16th–early 17th c. (pre-Abbas I in Siroux's grouping)",
        proposed_action="new-item or enrich",
        notes="Roadside caravanserai of Dhor, distinct from Qaleh atâbaki de Dhor (site 3) and from Mâder-e-Châh du col de Dhor (site 28).",
        evidence=[
            ("MIFAO82", "page", "126", "Chap. VIII, car. de Dhor, site 13"),
            ("MIFAO82", "index", "9-11, 14, 47, 126, 128, 130, 138, 142, 144, 185, 188", "Dhor (s. car.)"),
            ("MIFAO82", "figure", "fig. 31", "plan, site 13"),
            ("MIFAO82", "plate", "pl. IX E-F; pl. X A", "facades and portal"),
        ],
    ),
    dict(
        working_id="MIFAO81-riavad-e-bostan",
        siroux_name="Riâvad-e-Bostân",
        siroux_name_alt="Riavade-é-Bostan",
        normalized_en="Riavad-e Bostan",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "60", "Chap. VI"),
            ("MIFAO81", "figure", "fig. 20-21", "plan and section (inédit)"),
            ("MIFAO82", "page", "128", "Chap. VIII, site C"),
            ("MIFAO82", "index", "29, 31, 128, 135, 185, 188", "Riâvad-e-Bostân (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-bahram",
        siroux_name="Bahrâm",
        siroux_name_alt="car. Bahrâm (piste Ardestan)",
        normalized_en="Bahram (Isfahan–Ardestan road)",
        building_type="caravanserai",
        site_number="14",
        period_guess="16th–early 17th c.",
        proposed_action="new-item or enrich",
        notes="On the Isfahan–Aliabad–Bagherabad–Bahram–Ardestan itinerary. Not Qasr-e Bahram / UNESCO 1668-024 in the Kavir.",
        evidence=[
            ("MIFAO82", "page", "128", "Chap. VIII, car. Bahrâm, site 14"),
            ("MIFAO82", "index", "26, 128, 135, 139, 172, 186", "Bahrâm (car.)"),
            ("MIFAO82", "figure", "fig. 32", "plan, site 14"),
        ],
    ),
    dict(
        working_id="MIFAO81-passengan",
        siroux_name="Passengân",
        siroux_name_alt="Passengan",
        normalized_en="Pasangan",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "64", "Chap. VI, Caravansérail Passengan"),
            ("MIFAO81", "figure", "fig. 24", "plan (d'après Coste)"),
            ("MIFAO81", "plate", "pl. VI 1", "vue extérieure"),
            ("MIFAO82", "page", "130", "Chap. VIII"),
            ("MIFAO82", "plate", "pl. X B", "façade et citernes mongoles"),
            ("MIFAO82", "index", "130, 133, 147, 156, 185", "Passengân (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-haouz-e-soltan-safavid",
        siroux_name="Haouz-é-Sultan (safawide)",
        siroux_name_alt="Haouz-e-Soltân (car.); petit car. d'Haouz-e-Soltân",
        normalized_en="Howz-e Soltan (Safavid)",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        notes="Siroux publishes a Safavid building and a separate Qajar building at Howz-e Soltan. Keep both.",
        evidence=[
            ("MIFAO81", "page", "67", "Chap. VI, Caravansérail d'Haouz-é-Sultan (safawide)"),
            ("MIFAO81", "figure", "fig. 27", "plan d'ensemble (inédit)"),
            ("MIFAO81", "plate", "pl. VI 2, 6", "court and portal"),
            ("MIFAO82", "page", "131", "Chap. VIII, petit car. d'Haouz-e-Soltân"),
            ("MIFAO82", "index", "131, 185, 201", "Haouz-e-Soltân (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-moutah-safavid",
        siroux_name="Moutah",
        siroux_name_alt="car. de Moutah (safavide)",
        normalized_en="Muteh caravanserai",
        building_type="caravanserai",
        site_number="14 B",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "131", "Chap. VIII, car. de Moutah, site 14 B"),
            ("MIFAO82", "index", "131", "Moutah (car.)"),
            ("MIFAO82", "figure", "fig. 33", "plan"),
            ("MIFAO82", "plate", "pl. X E-F; pl. XI A-B", "facade, court, vaults"),
        ],
    ),
    dict(
        working_id="MIFAO82-sagzi",
        siroux_name="Sagzi-âbâd",
        siroux_name_alt="Sagzi; Sagzi-âbàd",
        normalized_en="Sagziabad",
        building_type="caravanserai",
        site_number="15",
        period_guess="16th–early 17th c.",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "133", "Chap. VIII, car. de Sagzi-âbâd, site 15"),
            ("MIFAO82", "index", "26-27, 30, 133, 156, 186, 194", "Sagzi (c.)"),
            ("MIFAO82", "figure", "fig. 34", "plan"),
            ("MIFAO82", "plate", "pl. X C; pl. XI C", "portal and court angle"),
        ],
    ),
    dict(
        working_id="MIFAO81-yezd-e-khast",
        siroux_name="Yezd-é-Khast",
        siroux_name_alt="Yezd-e-Khâst",
        normalized_en="Izadkhast",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid (Shah Abbas I inscription, Siroux)",
        proposed_unesco_id="1668-031",
        proposed_wikidata="Q5873579",
        proposed_action="enrich",
        evidence=[
            ("MIFAO81", "page", "65-67", "Chap. VI, Caravansérail de Yezd-é-Khast"),
            ("MIFAO81", "figure", "fig. 25", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. V 1; pl. VI 3", "inscription; ensemble"),
            ("MIFAO82", "page", "137", "Chap. IX, site C"),
            ("MIFAO82", "figure", "fig. 35", "plan"),
            ("MIFAO82", "index", "25, 31-32, 137, 139, 159, 165, 172, 183, 186, 188, 279", "Yezd-e-Khâst (m.t.c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-shurgestan",
        siroux_name="Shurgestan",
        siroux_name_alt="Chourgestân",
        normalized_en="Shurjestan",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "67", "Chap. VI, Caravansérail de Shurgestan"),
            ("MIFAO81", "figure", "fig. 26", "plan (inédit)"),
            ("MIFAO82", "page", "139", "Chap. IX, car. de Chourgestân"),
            ("MIFAO82", "index", "139, 170, 186", "Chourgestân (s. car.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-behdjat-abad",
        siroux_name="Behdjat-âbâd",
        siroux_name_alt="Bebdjat-âbâd",
        normalized_en="Behjatabad",
        building_type="caravanserai",
        site_number="16",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "139", "Chap. IX, site 16"),
            ("MIFAO82", "index", "18-19, 23, 25, 74, 99, 139, 186-187, 189", "Behdjat-âbâd (car.)"),
            ("MIFAO82", "figure", "fig. 36-37", "site and plan"),
            ("MIFAO82", "plate", "pl. XI D-E", "ruined SE facade; court north angle"),
        ],
    ),
    dict(
        working_id="MIFAO82-kouh-roud",
        siroux_name="Kouh-roûd",
        siroux_name_alt="Koub-roûd",
        normalized_en="Kuhrud",
        building_type="caravanserai",
        site_number="17",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "142", "Chap. IX, site 17"),
            ("MIFAO82", "index", "20-23, 124, 142, 144, 150, 162, 164, 186-189, 194, 279", "Kouh-roûd (s. car.)"),
            ("MIFAO82", "figure", "fig. 38", "plan"),
            ("MIFAO82", "plate", "pl. I A; pl. XI F", "village view; ruined entrance from court"),
        ],
    ),
    dict(
        working_id="MIFAO82-aznidjeh",
        siroux_name="Aznidjeh",
        siroux_name_alt="Aznidjeb",
        normalized_en="Aznijeh",
        building_type="caravanserai",
        site_number="18",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "144", "Chap. IX, site 18"),
            ("MIFAO82", "index", "8, 10, 144, 155, 159, 186, 190, 194", "Aznidjeh (s. car.)"),
            ("MIFAO82", "figure", "fig. 39", "plan et coupe"),
            ("MIFAO82", "plate", "pl. XII A-B", "exterior and court north facade"),
        ],
    ),
    dict(
        working_id="MIFAO82-dombi-safavid",
        siroux_name="Dombi B",
        siroux_name_alt="caravansérail safavide de Dombi",
        normalized_en="Dombi Safavid caravanserai",
        building_type="caravanserai",
        site_number="19",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "145", "Chap. IX, car. de Dombi B, site 19"),
            ("MIFAO82", "index", "18-19, 23, 25, 44, 74-75, 99, 107, 113, 116-121, 142, 145, 162, 170, 186, 189, 226", "Dombi (car. q.)"),
            ("MIFAO82", "figure", "fig. 40", "plan"),
            ("MIFAO82", "plate", "pl. XII C-E", "portal, Mongol iwan, turret"),
        ],
    ),
    dict(
        working_id="MIFAO82-gabr-abad",
        siroux_name="Gabr-âbâd",
        siroux_name_alt="",
        normalized_en="Gabrabad",
        building_type="caravanserai",
        site_number="21",
        period_guess="Safavid",
        proposed_unesco_id="1668-015",
        proposed_wikidata="Q5873197",
        proposed_action="enrich",
        evidence=[
            ("MIFAO82", "page", "150", "Chap. IX, site 21"),
            ("MIFAO82", "index", "22, 116, 150, 159, 162, 186, 188-189, 194, 201, 215", "Gabr-âbâd (car.)"),
            ("MIFAO82", "figure", "fig. 42", "plan"),
            ("MIFAO82", "plate", "pl. XIII C-F", "platform, entrance pavilion, portal, belvedere"),
        ],
    ),
    dict(
        working_id="MIFAO82-kouh-payeh",
        siroux_name="Kouh-pâyeh",
        siroux_name_alt="Kouh-pâyek; Kou-pâ; Koub-pâyeh",
        normalized_en="Kuhpayeh",
        building_type="caravanserai",
        site_number="22",
        period_guess="Safavid (Abbas I and later)",
        proposed_unesco_id="1668-018",
        proposed_wikidata="Q5906011",
        proposed_action="enrich",
        notes="Distinct from Qaleh-qadim de Kouh-pâyeh (site 22 B).",
        evidence=[
            ("MIFAO82", "page", "156", "Chap. X, site 22"),
            ("MIFAO82", "index", "27-31, 54, 63, 91, 116, 118, 156, 161, 164, 186-189, 198, 219-220, 226, 229, 238, 255, 261, 271-272, 283", "Kouh-pâyek (s.m.q.)"),
            ("MIFAO82", "figure", "fig. 43-44", "plan; coupe et bala-khaneh"),
            ("MIFAO82", "plate", "pl. XIV A-F; pl. XV A-B", "esplanade, pavilion, cistern, court, stables"),
        ],
    ),
    dict(
        working_id="MIFAO82-qaleh-qadim-kouhpayeh",
        siroux_name="Qaleh-qadim de Kouh-pâyeh",
        siroux_name_alt="Qaleh Qadim (de Kouh-pâyeh)",
        normalized_en="Kuhpayeh old qaleh",
        building_type="qaleh",
        site_number="22 B",
        period_guess="Sasanian–early Islamic (Siroux chap. IV)",
        proposed_action="review-type",
        evidence=[
            ("MIFAO82", "page", "54", "Chap. IV, Qaleh Qadim de Kouh-pâyeh, site 22 B"),
            ("MIFAO82", "index", "27, 54, 115, 156, 218", "Qaleh Qadim (de Kouh-pâyeh)"),
            ("MIFAO82", "figure", "fig. 7-8", "état actuel; restitution"),
            ("MIFAO82", "plate", "pl. III E", "trompillon"),
        ],
    ),
    dict(
        working_id="MIFAO82-bisyoun",
        siroux_name="Bisyoun",
        siroux_name_alt="car. de Bisyoun",
        normalized_en="Bisyun (Isfahan–Nain road)",
        building_type="caravanserai",
        site_number="23",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        notes="Isfahan–Nain road. Distinct from Bisoutoun / Behistoun (Kermanshah, UNESCO 1668-032) and from Nârendj-Qaleh de Bisyoun (site 23 bis).",
        evidence=[
            ("MIFAO82", "page", "159", "Chap. X, site 23"),
            ("MIFAO82", "index", "30, 39, 159, 165, 185, 187-188, 237, 259", "Bisyoun (car.)"),
            ("MIFAO82", "figure", "fig. 45", "plan"),
            ("MIFAO82", "plate", "pl. XV C-D", "exterior and SE court angle"),
        ],
    ),
    dict(
        working_id="MIFAO82-narendj-qaleh-bisyoun",
        siroux_name="Nârendj-Qaleh de Bisyoun",
        siroux_name_alt="Nârendj-Qaleh",
        normalized_en="Narenj Qaleh of Bisyun",
        building_type="qaleh",
        site_number="23 bis",
        period_guess="pre-13th c.",
        proposed_action="review-type",
        evidence=[
            ("MIFAO82", "page", "88", "Chap. IV, Nârendj Qaleh de Bisyoun, site 23 bis"),
            ("MIFAO82", "figure", "fig. 20", "plan"),
        ],
    ),
    dict(
        working_id="MIFAO82-vendad-deh",
        siroux_name="Vendâd-deh",
        siroux_name_alt="Yendâd-deb; Aghâ-Kemâl-Païn",
        normalized_en="Vandaddeh / Agha Kamal pain",
        building_type="caravanserai",
        site_number="24",
        period_guess="Safavid (inscription 1013 H. on pl. XVI E)",
        proposed_action="new-item or enrich",
        notes="Figure table: Aghâ-Kemâl-Païn. Distinct from Tchâh-gadeh / Aghâ-Kemâl Bala (site 20).",
        evidence=[
            ("MIFAO82", "page", "162", "Chap. X, site 24"),
            ("MIFAO82", "index", "12, 21, 148, 150, 162, 165, 167-168, 173, 187-189", "Vendâd-deb (car.)"),
            ("MIFAO82", "figure", "fig. 46", "plan"),
            ("MIFAO82", "plate", "pl. XV E; pl. XVI A-E", "facade, portal, vaults, inscription 1013 H."),
        ],
    ),
    dict(
        working_id="MIFAO82-gez",
        siroux_name="Gêz",
        siroux_name_alt="Gez; Gèz",
        normalized_en="Gaz",
        building_type="caravanserai",
        site_number="25",
        period_guess="Safavid",
        proposed_unesco_id="1668-017",
        proposed_wikidata="Q5871566",
        proposed_action="enrich",
        evidence=[
            ("MIFAO82", "page", "164", "Chap. X, site 25"),
            ("MIFAO82", "index", "9, 15-17, 21, 109, 146, 148, 150, 159, 162, 164, 168, 173, 186, 188-189, 192, 225, 288", "Gêz (s. car.)"),
            ("MIFAO82", "figure", "fig. 47-48", "plan and details"),
            ("MIFAO82", "plate", "pl. XVI F; pl. XVII A-D", "south facade, portal, dome, phare tower"),
        ],
    ),
    dict(
        working_id="MIFAO82-sardahan",
        siroux_name="Sardahan",
        siroux_name_alt="",
        normalized_en="Sardahan",
        building_type="caravanserai",
        site_number="26",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "167", "Chap. X, site 26"),
            ("MIFAO82", "index", "23, 25, 44, 101, 142, 162, 167, 173, 187, 189, 274", "Sardahan (c.)"),
            ("MIFAO82", "figure", "fig. 49-50", "plans and section"),
            ("MIFAO82", "plate", "pl. XVII E-F; pl. XVIII A", "portal, north iwan, guardroom vault"),
        ],
    ),
    dict(
        working_id="MIFAO81-natenz",
        siroux_name="Natenz",
        siroux_name_alt="Natanz (car.); car. de Natanz",
        normalized_en="Natanz caravanserai",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid (Abbas I; Olearius 1637 in Siroux)",
        proposed_action="new-item or enrich",
        notes="Large courtyard caravanserai 58.70 x 67.50 m (Siroux). Distinct from Robât-e-Sangui de Natanz (sites 2/6).",
        evidence=[
            ("MIFAO81", "page", "69", "Chap. VI, Caravansérail de Natenz"),
            ("MIFAO81", "figure", "fig. 28", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. VI 4", "vestibule interior"),
            ("MIFAO82", "page", "171", "Chap. X, car. de Natanz, site C"),
            ("MIFAO82", "figure", "fig. 51", "plan"),
            ("MIFAO82", "plate", "pl. XVIII B", "belvédère de Natanz"),
            ("MIFAO82", "index", "196, 201", "Natanz (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-zawareh",
        siroux_name="Zawareh",
        siroux_name_alt="Zavâreh; Zavâreb",
        normalized_en="Zavareh",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "69", "Chap. VI, Caravansérail de Zawareh"),
            ("MIFAO81", "figure", "fig. 29", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. VII 1, 3", "vestibule from court; stair to bala-khaneh"),
            ("MIFAO82", "page", "172", "Chap. X, car. de Zavâreh, site C"),
            ("MIFAO82", "figure", "fig. 52", "plan"),
            ("MIFAO82", "index", "26, 29, 155, 172, 186, 199", "Zavâreb (s.c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-mader-e-chah-mourtcheh",
        siroux_name="Mâder-e-Châh (de Mourtcheh-Khort)",
        siroux_name_alt="Mader-é-Chah; Madarshah",
        normalized_en="Madarshah Caravanserai (Murcheh Khvort)",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid; Qajar renovation",
        proposed_unesco_id="",
        proposed_wikidata="Q42627405",
        proposed_action="enrich",
        notes="Blueprint item Q42627405. National heritage, not UNESCO 1668. Distinct from the urban Mâder-e-Châh complex in Isfahan and from Mâder-e-Châh du col de Dhor. Distinct from the earlier Robât-e-Mourtcheh-Khort.",
        evidence=[
            ("MIFAO81", "page", "79-81", "Chap. VI, Caravansérail de Mader-é-Chah"),
            ("MIFAO81", "figure", "fig. 36-39, 89", "ensemble, dome, plan, section; hammam and cistern"),
            ("MIFAO81", "plate", "pl. VIII 4-5; pl. IX 3; pl. XII 1", "entrance, exterior, east iwan, interior"),
            ("MIFAO82", "page", "175", "Chap. X, car. Mâder-e-Châh de Mourtcheh-Khort, site C"),
            ("MIFAO82", "figure", "fig. 54", "plan"),
            ("MIFAO82", "index", "15, 175, 187-188", "Mâder-e-Châh de Mourtcheh-Khort"),
        ],
    ),
    dict(
        working_id="MIFAO82-tchah-e-siyah-now",
        siroux_name="Tchâh-e-siyâh now",
        siroux_name_alt="Tchâh-e-siyâb now; Chaleh Siah; Sheikhali Khan",
        normalized_en="Chah Siah now / Sheikhali Khan",
        building_type="caravanserai",
        site_number="27",
        period_guess="Safavid royal",
        proposed_unesco_id="1668-012",
        proposed_wikidata="Q5905596",
        proposed_action="enrich",
        notes="Proposed join to UNESCO Sheikhali Khan / Wikidata Chaleh Siah. Confirm against the old Chah Siah (site 4) before accepting.",
        evidence=[
            ("MIFAO82", "page", "175", "Chap. X, Tchâh-e-siyâh-now, site 27"),
            ("MIFAO82", "index", "168, 175, 179, 182, 187-190", "Tchâh-e-siyâh now (c.)"),
            ("MIFAO82", "figure", "fig. 55-56", "plan and axial section"),
            ("MIFAO82", "plate", "pl. XVIII C-F", "exterior, portal, east court facade, west court"),
        ],
    ),
    dict(
        working_id="MIFAO82-mader-e-chah-dhor",
        siroux_name="Mâder-e-Châh du col de Dhor",
        siroux_name_alt="Mâder-e-Ckâk du col de Dlior",
        normalized_en="Madarshah of Dhar pass",
        building_type="caravanserai",
        site_number="28",
        period_guess="Safavid royal",
        proposed_action="new-item or enrich",
        notes="Third Mâder-e-Châh building. Do not merge with Murcheh Khvort or the Isfahan urban complex.",
        evidence=[
            ("MIFAO82", "page", "179", "Chap. X, site 28"),
            ("MIFAO82", "index", "11, 179, 187-188", "Mâder-e-Châh du col de Dhor (car.)"),
            ("MIFAO82", "figure", "fig. 57-58", "site and plan"),
            ("MIFAO82", "plate", "pl. XIX A-C", "exterior, entrance pavilion, vaults"),
        ],
    ),
    dict(
        working_id="MIFAO82-bagher-abad-tchapar",
        siroux_name="Tchapar-khâneh de Bâgher-âbâd",
        siroux_name_alt="Bâgher-âbâd (tk.)",
        normalized_en="Bagherabad chapar-khaneh",
        building_type="tchaparkhaneh",
        site_number="35",
        period_guess="post-Safavid / Qajar",
        proposed_action="review-type",
        notes="Postal relay, not a courtyard caravanserai. Keep as a related roadside monument.",
        evidence=[
            ("MIFAO82", "page", "192", "Chap. XII, site 35"),
            ("MIFAO82", "figure", "fig. 59", "plan"),
            ("MIFAO82", "plate", "pl. XIX D", "vue extérieure"),
        ],
    ),
    dict(
        working_id="MIFAO82-soh",
        siroux_name="Sôh",
        siroux_name_alt="Soh",
        normalized_en="Soh",
        building_type="caravanserai",
        site_number="29",
        period_guess="post-Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "194", "Chap. XII, site 29"),
            ("MIFAO82", "index", "20, 22, 144, 162, 164, 194, 201", "Sôh (c.)"),
            ("MIFAO82", "figure", "fig. 60", "plan"),
            ("MIFAO82", "plate", "pl. XIX E; pl. XX A", "exterior; portal vault and inscription"),
        ],
    ),
    dict(
        working_id="MIFAO82-qaleh-chour",
        siroux_name="Qaleh-Chour",
        siroux_name_alt="Qaleh Chour; Qaleh-Cbour",
        normalized_en="Qaleh Shur",
        building_type="caravanserai",
        site_number="30",
        period_guess="post-Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "194", "Chap. XII, site 30"),
            ("MIFAO82", "index", "32, 172, 194, 201", "Qaleh Chour (c.)"),
            ("MIFAO82", "figure", "fig. 61", "plan"),
            ("MIFAO82", "plate", "pl. XIX F; pl. XX B", "exterior; court north angle"),
        ],
    ),
    dict(
        working_id="MIFAO82-chahi",
        siroux_name="Châhi",
        siroux_name_alt="Ghâbi (OCR); car. Châhi",
        normalized_en="Shahi",
        building_type="caravanserai",
        site_number="31",
        period_guess="post-Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "197", "Chap. XII, site 31"),
            ("MIFAO82", "index", "33, 197", "Châhi (car.)"),
            ("MIFAO82", "figure", "fig. 62", "plan"),
        ],
    ),
    dict(
        working_id="MIFAO82-qaleh-ali-agha",
        siroux_name="Qaleh Ali-âghâ",
        siroux_name_alt="Qaleh Ali-Aghâ",
        normalized_en="Qaleh Ali Agha",
        building_type="qaleh",
        site_number="32",
        period_guess="post-Safavid",
        proposed_action="review-type",
        evidence=[
            ("MIFAO82", "page", "198", "Chap. XII, site 32"),
            ("MIFAO82", "index", "34, 198", "Qaleh Ali-âghâ (c.)"),
            ("MIFAO82", "figure", "fig. 63", "plan"),
            ("MIFAO82", "plate", "pl. XX C", "vue extérieure"),
        ],
    ),
    dict(
        working_id="MIFAO82-taqi-abad",
        siroux_name="Taqi-âbâd",
        siroux_name_alt="halte de Taqi-âbâd; caravansérail-écurie",
        normalized_en="Taqiabad",
        building_type="caravanserai",
        site_number="33",
        period_guess="post-Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "199", "Chap. XII, site 33"),
            ("MIFAO82", "figure", "fig. 64-65", "ensemble; plan of caravanserai-stable"),
        ],
    ),
    dict(
        working_id="MIFAO82-zizeh",
        siroux_name="Zizeh",
        siroux_name_alt="caravansérail circulaire de Zizeh",
        normalized_en="Zizeh",
        building_type="caravanserai",
        site_number="34",
        period_guess="post-Safavid / Qajar circular",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO82", "page", "201", "Chap. XII, site 34"),
            ("MIFAO82", "index", "25, 201", "Zizeh (c.)"),
            ("MIFAO82", "figure", "fig. 66-67", "situation; plan and section"),
            ("MIFAO82", "plate", "pl. XX D-E", "portal and court"),
        ],
    ),
    dict(
        working_id="MIFAO82-mader-e-chah-isfahan",
        siroux_name="Mâder-e-Châh à Ispahân",
        siroux_name_alt="caravansérail urbain Mader-é-Chah; Abbasi Hotel",
        normalized_en="Madar-i Shah urban caravanserai (Isfahan)",
        building_type="urban-caravanserai",
        site_number="A 48",
        period_guess="Safavid (Shah Sultan Husayn)",
        proposed_action="enrich or new-item",
        notes="Urban complex (madrasa, bazaar, caravanserai). Harvesting notes: this is a different building from Q42627405 Madarshah at Murcheh Khvort.",
        evidence=[
            ("MIFAO81", "page", "117-119", "Annexe I, caravansérails urbains; plan after Coste"),
            ("MIFAO81", "figure", "fig. 79", "plan of caravanserai and madrasa (d'après Coste)"),
            ("MIFAO82", "page", "284-288", "Chap. XVIII, site A 48, ensemble de Mâder-e-Chah"),
            ("MIFAO82", "figure", "fig. 97", "plan of the ensemble"),
            ("MIFAO82", "plate", "pl. XXX A-B", "restored court facades"),
            ("MIFAO82", "index", "189, 284", "Mâder-e-Châh ensemble à Ispahân (m. car.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-kunar-e-siyah",
        siroux_name="Kunâr-e-Siyâh",
        siroux_name_alt="Kunar-siâh; Shish-Kunar related",
        normalized_en="Kunar-e Siyah",
        building_type="caravanserai",
        site_number="",
        period_guess="Sasanian–early Islamic (Siroux chap. IV)",
        proposed_action="new-item or enrich",
        notes="Discussed as a type-example with Bisoutoun and Qaleh-qadim. Confirm whether Siroux surveyed the building or cited it comparatively.",
        evidence=[
            ("MIFAO82", "page", "54", "Chap. IV, Kunâr-e-Siyâh"),
            ("MIFAO82", "index", "54-55, 74, 91-92, 115", "Kunar-siâh (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO82-bisoutoun",
        siroux_name="Bisoutoun",
        siroux_name_alt="Behistoun; monument de Bisoutoun",
        normalized_en="Bisotun caravanserai",
        building_type="caravanserai",
        site_number="",
        period_guess="Sasanian–early Islamic core discussed; later Shah Abbasi building is UNESCO",
        proposed_unesco_id="1668-032",
        proposed_wikidata="Q5908224",
        proposed_action="enrich",
        notes="Kermanshah. Proposed UNESCO join is by famous place-name; Siroux discusses 'le monument de Bisoutoun' as an early type. Confirm the surveyed remains equal the inscribed Shah Abbasi caravanserai.",
        evidence=[
            ("MIFAO82", "page", "51", "Chap. IV, le monument de Bisoutoun"),
            ("MIFAO82", "index", "51, 91, 115-116, 118, 121", "Bisoutoun (Behistoun) (s. car.)"),
            ("MIFAO82", "figure", "fig. 6", "croquis de l'édifice de Bisoutoun (OCR: Risoutoun)"),
            ("MIFAO82", "plate", "pl. VII B", "mihrab brickwork at Bisyoun — verify this plate is Bisotun not Bisyun"),
        ],
    ),
    # ------------------------------------------------------------------
    # MIFAO 81 mountain caravanserais (chap. V)
    # ------------------------------------------------------------------
    dict(
        working_id="MIFAO81-nere",
        siroux_name="Néré",
        siroux_name_alt="",
        normalized_en="Nere",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "35", "Chap. V, Caravansérail Néré"),
            ("MIFAO81", "figure", "fig. 2", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. I 4", "vue extérieure"),
        ],
    ),
    dict(
        working_id="MIFAO81-imamzadeh-hachem",
        siroux_name="Imam-zadeh Hachem",
        siroux_name_alt="ITmam-Zadeh Hachem",
        normalized_en="Imamzadeh Hashem",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "36", "Chap. V"),
            ("MIFAO81", "figure", "fig. 3", "plan (inédit)"),
            ("MIFAO81", "plate", "pl. II 3", "imamzadeh and caravanserai"),
        ],
    ),
    dict(
        working_id="MIFAO81-gamboudcht",
        siroux_name="Gamboudcht",
        siroux_name_alt="Gambuj; Gamboudcht east of Tehran (Iranica mountain type)",
        normalized_en="Gambuj / Gambudcht",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        notes="Matches the earlier queue hint 'Gambuj (east of Tehran)'.",
        evidence=[
            ("MIFAO81", "page", "36", "Chap. V, Caravansérail Gamboudcht"),
            ("MIFAO81", "figure", "fig. 4-5", "plan, coupe, coupole"),
            ("MIFAO81", "plate", "pl. I 2", "vue extérieure"),
        ],
    ),
    dict(
        working_id="MIFAO81-peylour",
        siroux_name="Peylour",
        siroux_name_alt="",
        normalized_en="Peylor",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "37", "Chap. V"),
            ("MIFAO81", "figure", "fig. 6", "plan et coupe (inédit)"),
            ("MIFAO81", "plate", "pl. II 2", "vue extérieure"),
        ],
    ),
    dict(
        working_id="MIFAO81-mirza-abdullah-khan",
        siroux_name="Mirza-Abdullah-Khan",
        siroux_name_alt="Mirza Adbullah Khan",
        normalized_en="Mirza Abdullah Khan",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "38", "Chap. V"),
            ("MIFAO81", "figure", "fig. 7", "plan et coupe (inédit)"),
        ],
    ),
    dict(
        working_id="MIFAO81-chebli",
        siroux_name="Chebli",
        siroux_name_alt="col de Chebli; Cbebli",
        normalized_en="Shebli pass",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "40", "Chap. V, Caravansérail du col de Chebli"),
            ("MIFAO81", "figure", "fig. 8-10", "plans after Texier and Siroux; sections"),
            ("MIFAO81", "plate", "pl. II 1, 4-5", "exterior and gallery vaults"),
        ],
    ),
    dict(
        working_id="MIFAO81-abbassi-abali",
        siroux_name="Abbassi près d'Ab-Ali",
        siroux_name_alt="caravansérail Abbassi",
        normalized_en="Abbasi near Abali",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid mountain type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "43", "Chap. V, Caravansérail Abbassi"),
            ("MIFAO81", "figure", "fig. 11", "plan (inédit)"),
        ],
    ),
    dict(
        working_id="MIFAO81-hint-khatunabad",
        siroux_name="Khatunabad (mountain)",
        siroux_name_alt="Khātūnābād",
        normalized_en="Khatunabad",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid?",
        proposed_action="enrich or new-item",
        notes="Not a MIFAO 81 chapter heading. Cited in Encyclopaedia Iranica 'Caravansary' as a mountain type with Kleiss/Siroux. Confirm against the volume before creating an item.",
        evidence=[
            ("MIFAO81", "index", "unconfirmed in TOC", "Iranica cites MIFAO 81 / Kleiss for a mountain caravanserai at Khatunabad"),
        ],
    ),
    dict(
        working_id="MIFAO81-hint-gaduk",
        siroux_name="Gaduk near Firuzkuh",
        siroux_name_alt="Gadūk",
        normalized_en="Gaduk",
        building_type="caravanserai",
        site_number="",
        period_guess="mountain type",
        proposed_action="enrich or new-item",
        notes="Not a MIFAO 81 chapter heading. Mountain type; Kleiss plan exists. Confirm in Siroux itineraries (Firouz-kouh zone) before creating an item.",
        evidence=[
            ("MIFAO81", "itinerary", "13-14", "Elbourz / Firouz-kouh zone; confirm Gaduk by visual reading"),
        ],
    ),
    # ------------------------------------------------------------------
    # Remaining MIFAO 81 plain caravanserais (chap. VI) not already listed
    # ------------------------------------------------------------------
    dict(
        working_id="MIFAO81-darwazeh-gatch",
        siroux_name="Darwazeh-Gatch",
        siroux_name_alt="Danvazeh-Gatch; Darvâzek-gatcb; Darvâzeh-gatch",
        normalized_en="Darvazeh Gach",
        building_type="caravanserai",
        site_number="C",
        period_guess="early courtyard type",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "45", "Chap. VI, Caravansérail Darwazeh-Gatch"),
            ("MIFAO81", "figure", "fig. 12", "plan after Sir Aurel Stein"),
            ("MIFAO82", "index", "32, 51, 91, 115", "Darvâzeh-gatch (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-semnan",
        siroux_name="près de Semnan",
        siroux_name_alt="Caravansérail près de Semnan",
        normalized_en="near Semnan",
        building_type="caravanserai",
        site_number="",
        period_guess="related to Robat-Kerim type (Siroux)",
        proposed_action="new-item or enrich",
        notes="Unnamed beyond 'près de Semnan'. Reviewer should identify against Ahovan / Noushirvan (UNESCO 1668-002/003) or another Semnan building.",
        evidence=[
            ("MIFAO81", "page", "49", "Chap. VI, Caravansérail près de Semnan"),
        ],
    ),
    dict(
        working_id="MIFAO81-zaffarounie",
        siroux_name="Zalfarounie",
        siroux_name_alt="Zaffarounie; Zaffarounyeb",
        normalized_en="Zaferaniyeh",
        building_type="caravanserai",
        site_number="",
        period_guess="Seljuk (luxurious type with Robat-Sharaf)",
        proposed_unesco_id="1668-021",
        proposed_wikidata="Q5923727",
        proposed_action="enrich",
        evidence=[
            ("MIFAO81", "page", "49", "Chap. VI, Caravansérail de Zalfarounie"),
            ("MIFAO82", "index", "85, 119", "Zaffarounyeb (Zaffarounie) (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-kaleh-sangui",
        siroux_name="Kaleh-Sangui",
        siroux_name_alt="Qaleh-Sangui (national survey example)",
        normalized_en="Qaleh Sangi",
        building_type="caravanserai",
        site_number="",
        period_guess="Seljuk / early courtyard",
        proposed_action="new-item or enrich",
        notes="MIFAO 81 national example. Several Qaleh-Sangui buildings exist (Natanz, Allahvidjeh, Aliabad). Do not merge until the 1949 plan is identified.",
        evidence=[
            ("MIFAO81", "page", "51", "Chap. VI, Caravansérail de Kaleh-Sangui"),
            ("MIFAO81", "figure", "fig. 15", "plan (inédit); TOC page 51, figure table OCR says 62 — confirm"),
            ("MIFAO81", "plate", "pl. III 5-6", "trompillon and portal"),
        ],
    ),
    dict(
        working_id="MIFAO81-sertchem",
        siroux_name="Sertchem",
        siroux_name_alt="Sartchem; Setchem; Sartcbem",
        normalized_en="Sarcham",
        building_type="caravanserai",
        site_number="C",
        period_guess="Seljuk with Safavid reconstruction",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "53", "Chap. VI, Caravansérail de Sertchem"),
            ("MIFAO81", "figure", "fig. 16-18", "plan état actuel; court angle; restitution"),
            ("MIFAO81", "plate", "pl. IV 1-2, 4", "portal, court angle, iwan masonry"),
            ("MIFAO82", "page", "172-174", "Chap. X, comparative Azerbaijan group"),
            ("MIFAO82", "figure", "fig. 14", "plan du caravansérail de Sartchem"),
            ("MIFAO82", "index", "63, 91-92, 95, 116, 118-120, 146, 148, 156, 173", "Sartcbem (c.) (Sertcbem)"),
        ],
    ),
    dict(
        working_id="MIFAO81-airandibi",
        siroux_name="Airandibi",
        siroux_name_alt="Aïrandibi",
        normalized_en="Airandibi",
        building_type="caravanserai",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "57", "Chap. VI, Caravansérail d'Airandibi"),
            ("MIFAO81", "plate", "pl. IV 3", "portail d'un caravansérail près d'Airandibi"),
            ("MIFAO82", "index", "92, 95, 117, 119-120", "Aïrandibi (s. car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-sangbast",
        siroux_name="Sangbast",
        siroux_name_alt="",
        normalized_en="Sangbast",
        building_type="caravanserai",
        site_number="C",
        period_guess="",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "60", "Chap. VI, Caravansérail Sangbast"),
            ("MIFAO81", "plate", "pl. V 5", "entrée"),
            ("MIFAO82", "index", "185, 188", "Sangbast (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-guilak",
        siroux_name="Guilak",
        siroux_name_alt="",
        normalized_en="Gilak",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "62", "Chap. VI, Caravansérail de Guilak"),
            ("MIFAO81", "figure", "fig. 22-23", "plan; voûte de l'entrée"),
            ("MIFAO81", "plate", "pl. V 3-4", "intérieur and extérieur"),
            ("MIFAO82", "index", "130, 133, 135", "Guilak (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-roudehen",
        siroux_name="Roudehen",
        siroux_name_alt="Roudeben",
        normalized_en="Rudehen",
        building_type="caravanserai",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "67", "Chap. VI, Caravansérail de Roudehen"),
            ("MIFAO81", "plate", "pl. VI 5", "portail, vue extérieure"),
            ("MIFAO82", "index", "13", "Roudeben (s.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-siah-kouh-abbasabad",
        siroux_name="Siah-Kouh (Abbas-abad)",
        siroux_name_alt="Abbas-Abad de Siah-kouh",
        normalized_en="Abbasabad Siah Kuh",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        notes="Do not auto-join to UNESCO Abbas Abad Taybad (1668-008) or Abbas Abad Semnan (1668-026).",
        evidence=[
            ("MIFAO81", "page", "72", "Chap. VI, Caravansérail de Siah-Kouh (Abbas-abad)"),
            ("MIFAO81", "plate", "pl. VII 2, 4-6; pl. VIII 6", "exterior, tower, facade, portal, interior court"),
        ],
    ),
    dict(
        working_id="MIFAO81-dehbid-safavid",
        siroux_name="Deh-Bid (polygonal safawide)",
        siroux_name_alt="Deh-bid octogonal",
        normalized_en="Dehbid (Safavid polygonal)",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid polygonal",
        proposed_action="new-item or enrich",
        notes="Siroux later groups Deh-bid, Amin-âbâd and Khan-e-Khurra as octagonal royal type (MIFAO 82 p. 183).",
        evidence=[
            ("MIFAO81", "page", "73", "Chap. VI, Caravansérail de Deh-Bid"),
            ("MIFAO81", "figure", "fig. 30", "polygonal plan after Texier"),
            ("MIFAO82", "page", "183", "Chap. X, caravansérails octogonaux, site C"),
            ("MIFAO82", "index", "32, 90, 101, 183, 201", "Deh-bid (s.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-amin-abad",
        siroux_name="Amin-Abad",
        siroux_name_alt="Amin-âbâd (route Chiraz); Amir-âbâd (MIFAO 82 octagonal group)",
        normalized_en="Aminabad",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid polygonal",
        proposed_unesco_id="1668-014",
        proposed_wikidata="Q5907540",
        proposed_action="enrich",
        notes="MIFAO 82 p. 183 writes Amir-âbâd in the octagonal group; index has Amin-âbâd (route Chiraz). Confirm spelling and that this is UNESCO Amin Abad, not Nezam-abad on the Natanz road.",
        evidence=[
            ("MIFAO81", "page", "73", "Chap. VI, Caravansérail Amin-Abad"),
            ("MIFAO81", "figure", "fig. 31", "polygonal plan after Coste"),
            ("MIFAO82", "page", "183", "octagonal group"),
            ("MIFAO82", "index", "32, 90, 101, 183", "Amin-âbâd (route Chiraz) (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-khan-e-khurra",
        siroux_name="Khan-é-Khurra",
        siroux_name_alt="Khân-e-Khurra; Khan-é-kurrah",
        normalized_en="Khan-e Khurra",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid octagonal",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "73", "Chap. VI, Caravansérail Khan-é-Khurra"),
            ("MIFAO82", "page", "183", "Chap. X, octagonal group, site C"),
            ("MIFAO82", "index", "90, 101, 183", "Khân-e-Khurra (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-djemal-abad",
        siroux_name="Djemal-Abad",
        siroux_name_alt="Djemal-âbâd",
        normalized_en="Jamalabad",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_unesco_id="1668-009",
        proposed_wikidata="Q5907713",
        proposed_action="enrich",
        evidence=[
            ("MIFAO81", "page", "73", "Chap. VI, Caravansérail de Djemal-Abad"),
            ("MIFAO81", "figure", "fig. 32-33", "plan; voussure"),
            ("MIFAO81", "plate", "pl. VIII 1", "portail"),
            ("MIFAO82", "page", "172-174", "Azerbaijan comparative group"),
            ("MIFAO82", "index", "175, 187", "Djemal-âbâd (car.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-nikpey",
        siroux_name="Nikpey",
        siroux_name_alt="",
        normalized_en="Nikpey",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "75", "Chap. VI, Caravansérail de Nikpey"),
            ("MIFAO81", "figure", "fig. 34", "accès d'une écurie"),
            ("MIFAO81", "plate", "pl. VIII 3", "portail"),
            ("MIFAO82", "page", "172-174", "Azerbaijan comparative group"),
            ("MIFAO82", "index", "161, 172-173, 187", "Nikpey (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-jam",
        siroux_name="Jam",
        siroux_name_alt="Jam près de Tabriz; Jamb-Djam",
        normalized_en="Jam (near Tabriz)",
        building_type="caravanserai",
        site_number="C",
        period_guess="Safavid / Mongol postal name (jam)",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "77", "Chap. VI, Caravansérail de Jam"),
            ("MIFAO81", "figure", "fig. 35", "plan (inédit), près de Tabriz"),
            ("MIFAO81", "plate", "pl. VIII 2", "portail"),
            ("MIFAO82", "page", "172-174", "Azerbaijan comparative group"),
            ("MIFAO82", "index", "161, 172, 187", "Jam (car.) (Jamb-Djam)"),
        ],
    ),
    dict(
        working_id="MIFAO81-abbas-abad-khorassan",
        siroux_name="Abbas-Abad (route du Khorassan)",
        siroux_name_alt="",
        normalized_en="Abbasabad on the Khorasan road",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid",
        proposed_action="new-item or enrich",
        notes="Ambiguous among UNESCO Abbas Abad Taybad (1668-008) and Abbas Abad Semnan (1668-026). Do not join until the plates are read.",
        evidence=[
            ("MIFAO81", "page", "81", "Chap. VI, Caravansérail Abbas-Abad (route du Khorassan)"),
            ("MIFAO81", "plate", "pl. IX 1-2", "portail and interior"),
        ],
    ),
    dict(
        working_id="MIFAO81-between-shahroud-miandacht",
        siroux_name="entre Chahroud et Miandacht",
        siroux_name_alt="",
        normalized_en="between Shahrud and Miandasht",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid?",
        proposed_action="new-item or enrich",
        notes="Unnamed in the TOC. Plate IX 5 shows a portal. Identify against the Shahrud–Miandasht chain before creating an item.",
        evidence=[
            ("MIFAO81", "page", "81", "Chap. VI"),
            ("MIFAO81", "plate", "pl. IX 5", "portail d'un caravansérail entre Miandacht et Chahroud"),
        ],
    ),
    dict(
        working_id="MIFAO81-miandacht",
        siroux_name="Miandacht",
        siroux_name_alt="Miandasht",
        normalized_en="Miandasht",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid + later courts",
        proposed_unesco_id="1668-027",
        proposed_wikidata="Q5705395",
        proposed_action="enrich",
        notes="Multi-building complex. Siroux plates show two courts.",
        evidence=[
            ("MIFAO81", "page", "81", "Chap. VI, Caravansérail de Miandacht"),
            ("MIFAO81", "plate", "pl. IX 4, 6", "portail; communication between the two courts"),
        ],
    ),
    dict(
        working_id="MIFAO81-tchehel-hessieh",
        siroux_name="Tchehel-Hessieh",
        siroux_name_alt="Tchehel-hessieh",
        normalized_en="Chehel Hessieh",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid (after Texier)",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "81", "Chap. VI, Caravansérail de Tchehel-Hessieh"),
            ("MIFAO81", "figure", "fig. 40", "after Texier"),
        ],
    ),
    dict(
        working_id="MIFAO81-dehbid-qajar",
        siroux_name="Deh-Bid (kadjar)",
        siroux_name_alt="",
        normalized_en="Dehbid (Qajar)",
        building_type="caravanserai",
        site_number="",
        period_guess="Qajar",
        proposed_action="new-item or enrich",
        notes="Second Deh-bid building. Keep separate from the Safavid polygonal inn.",
        evidence=[
            ("MIFAO81", "page", "83", "Chap. VI, Caravansérail de Deh-Bid (kadjar)"),
            ("MIFAO81", "figure", "fig. 41-43", "plan (inédit); court; portal"),
        ],
    ),
    dict(
        working_id="MIFAO81-ardakan",
        siroux_name="Ardakan",
        siroux_name_alt="Ardakân",
        normalized_en="Ardakan",
        building_type="caravanserai",
        site_number="",
        period_guess="Safavid / later",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "83", "Chap. VI, Caravansérail d'Ardakan"),
            ("MIFAO81", "figure", "fig. 44-46, 88", "plan; east iwan and ventilation tower; exterior; ab-ambar"),
            ("MIFAO82", "index", "172, 201", "Ardakân (s.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-perech",
        siroux_name="Perech",
        siroux_name_alt="Perech (Mouchiri)",
        normalized_en="Perech (Moshiri)",
        building_type="caravanserai",
        site_number="",
        period_guess="Qajar (Moshir)",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "86", "Chap. VI, Caravansérail Perech"),
            ("MIFAO81", "figure", "fig. 48-50", "plan; portal from court; west iwan"),
            ("MIFAO82", "index", "201", "Perech (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-rah-dar",
        siroux_name="Rah-Dar",
        siroux_name_alt="Râh-dar; Rah-dar",
        normalized_en="Rahdar",
        building_type="caravanserai",
        site_number="",
        period_guess="Qajar?",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "86", "Chap. VI, Caravansérail de Rah-Dar"),
            ("MIFAO81", "figure", "fig. 51-52", "plan; court"),
            ("MIFAO82", "index", "201", "Râh-dar (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-haouz-e-soltan-qajar",
        siroux_name="Haouz-é-Sultan (kadjar)",
        siroux_name_alt="",
        normalized_en="Howz-e Soltan (Qajar)",
        building_type="caravanserai",
        site_number="",
        period_guess="Qajar",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "89", "Chap. VI"),
            ("MIFAO81", "figure", "fig. 53", "vue d'ensemble"),
            ("MIFAO81", "plate", "pl. X 1-2", "east iwan; forecourt"),
        ],
    ),
    dict(
        working_id="MIFAO81-kale-kermes",
        siroux_name="Kalé-Kermès",
        siroux_name_alt="Kaleh-Kermès; Kâleh Kermes",
        normalized_en="Qaleh Kermes",
        building_type="caravanserai",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        notes="Surveyed with Ali-Abad and Howz-e Soltan near the former lake / Tehran–Qom approaches.",
        evidence=[
            ("MIFAO81", "page", "90", "Chap. VI, Caravansérail de Kalé-Kermès"),
            ("MIFAO81", "figure", "fig. 54", "plan (inédit)"),
        ],
    ),
    dict(
        working_id="MIFAO81-ali-abad",
        siroux_name="Ali-Abad",
        siroux_name_alt="Ali-âbâd (entre Téhéran et Qom)",
        normalized_en="Aliabad (Tehran–Qom road)",
        building_type="caravanserai",
        site_number="",
        period_guess="Qajar large complex",
        proposed_action="new-item or enrich",
        notes="Large complex with hotel block, founder's house, hammam. Distinct from Robât-e-Sangui d'Ali-âbâd and from Ali-âbâd near Natanz.",
        evidence=[
            ("MIFAO81", "page", "92-96", "Chap. VI, Caravansérail d'Ali-Abad"),
            ("MIFAO81", "figure", "fig. 55-59, 96-97", "ensemble, buildings, tower, hotel, founder's house, hammam"),
            ("MIFAO81", "plate", "pl. X 3-5; pl. XI 1-2", "ensemble, entrance, court, south tower, property gate"),
            ("MIFAO82", "index", "201", "Ali-âbâd (car.) (entre Téhéran et Qom)"),
        ],
    ),
    dict(
        working_id="MIFAO81-manzarieh",
        siroux_name="Manzarieh",
        siroux_name_alt="",
        normalized_en="Manzariyeh",
        building_type="caravanserai",
        site_number="",
        period_guess="",
        proposed_action="new-item or enrich",
        evidence=[
            ("MIFAO81", "page", "96", "Chap. VI, Caravansérail de Manzarieh"),
            ("MIFAO81", "figure", "fig. 60-61", "entrance detail; exterior"),
            ("MIFAO81", "plate", "pl. XI 3", "north iwan"),
            ("MIFAO82", "index", "201", "Manzarieh (c.)"),
        ],
    ),
    dict(
        working_id="MIFAO81-kachan-octogonal",
        siroux_name="caravansérail octogonal dans le bazar de Kachan",
        siroux_name_alt="",
        normalized_en="Kashan bazaar octagonal caravanserai",
        building_type="urban-caravanserai",
        site_number="",
        period_guess="",
        proposed_action="review-type",
        evidence=[
            ("MIFAO81", "page", "119", "Annexe I, caravansérails urbains"),
            ("MIFAO81", "figure", "fig. 80", "plan et coupe (inédit)"),
        ],
    ),
]


QUEUE_FIELDS = [
    "working_id",
    "siroux_name",
    "siroux_name_alt",
    "normalized_en",
    "normalized_fa",
    "building_type",
    "site_number",
    "period_guess",
    "sources",
    "cover_evidence",
    "has_plan",
    "has_photograph",
    "proposed_unesco_id",
    "proposed_wikidata",
    "unesco_id",
    "wikidata",
    "review_status",
    "proposed_action",
    "notes",
    "editor_notes",
]

EVIDENCE_FIELDS = [
    "working_id",
    "source_id",
    "source_short",
    "source_name",
    "source_year",
    "evidence_kind",
    "locator",
    "detail",
    "ia_item",
    "notes",
]


def cover_evidence(evidence):
    parts = []
    for source_id, kind, locator, detail in evidence:
        short = SOURCES[source_id]["source_short"]
        if kind == "page":
            parts.append(f"{short} p.{locator}")
        elif kind == "figure":
            parts.append(f"{short} {locator}")
        elif kind == "plate":
            parts.append(f"{short} {locator}")
        elif kind == "index":
            parts.append(f"{short} index p.{locator}")
        elif kind == "itinerary":
            parts.append(f"{short} itinerary p.{locator}")
        else:
            parts.append(f"{short} {kind} {locator}")
        _ = detail
    return "; ".join(parts)


def sources_of(evidence):
    seen = []
    for source_id, *_ in evidence:
        if source_id not in seen:
            seen.append(source_id)
    return ";".join(seen)


def write_csv():
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with QUEUE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=QUEUE_FIELDS, extrasaction="ignore")
        w.writeheader()
        for b in BUILDINGS:
            ev = b["evidence"]
            kinds = {k for _, k, _, _ in ev}
            row = {
                "working_id": b["working_id"],
                "siroux_name": b["siroux_name"],
                "siroux_name_alt": b.get("siroux_name_alt", ""),
                "normalized_en": b.get("normalized_en", ""),
                "normalized_fa": b.get("normalized_fa", ""),
                "building_type": b.get("building_type", ""),
                "site_number": b.get("site_number", ""),
                "period_guess": b.get("period_guess", ""),
                "sources": sources_of(ev),
                "cover_evidence": cover_evidence(ev),
                "has_plan": "yes" if "figure" in kinds else "",
                "has_photograph": "yes" if "plate" in kinds else "",
                "proposed_unesco_id": b.get("proposed_unesco_id", ""),
                "proposed_wikidata": b.get("proposed_wikidata", ""),
                "unesco_id": "",
                "wikidata": "",
                "review_status": "candidate",
                "proposed_action": b.get("proposed_action", "new-item or enrich"),
                "notes": b.get("notes", ""),
                "editor_notes": "",
            }
            w.writerow(row)

    with EVIDENCE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=EVIDENCE_FIELDS)
        w.writeheader()
        for b in BUILDINGS:
            for source_id, kind, locator, detail in b["evidence"]:
                src = SOURCES[source_id]
                w.writerow(
                    {
                        "working_id": b["working_id"],
                        "source_id": src["source_id"],
                        "source_short": src["source_short"],
                        "source_name": src["source_name"],
                        "source_year": src["year"],
                        "evidence_kind": kind,
                        "locator": locator,
                        "detail": detail,
                        "ia_item": src["ia_item"],
                        "notes": "OCR is a finding aid; confirm against the printed page or plate. Scan quality of plans and photographs is poor.",
                    }
                )


def md_escape(text):
    return (text or "").replace("|", "\\|")


def write_markdown():
    by_id = {b["working_id"]: b for b in BUILDINGS}
    n = len(BUILDINGS)
    n81 = sum(1 for b in BUILDINGS if any(s == "MIFAO81" for s, *_ in b["evidence"]))
    n82 = sum(1 for b in BUILDINGS if any(s == "MIFAO82" for s, *_ in b["evidence"]))
    n_plan = sum(1 for b in BUILDINGS if any(k == "figure" for _, k, _, _ in b["evidence"]))
    n_photo = sum(1 for b in BUILDINGS if any(k == "plate" for _, k, _, _ in b["evidence"]))
    n_unesco = sum(1 for b in BUILDINGS if b.get("proposed_unesco_id"))

    def rows(ids):
        lines = [
            "| Working ID | Siroux name | Type | Site | Sources | Cover evidence | Plan | Photo | Proposed action | Proposed UNESCO / Wikidata |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for i in ids:
            b = by_id[i]
            ev = b["evidence"]
            kinds = {k for _, k, _, _ in ev}
            join = " / ".join(
                x for x in (b.get("proposed_unesco_id"), b.get("proposed_wikidata")) if x
            )
            lines.append(
                "| `{id}` | {name} | {typ} | {site} | {src} | {cov} | {plan} | {photo} | {act} | {join} |".format(
                    id=b["working_id"],
                    name=md_escape(b["siroux_name"]),
                    typ=b.get("building_type", ""),
                    site=b.get("site_number", "") or "—",
                    src=sources_of(ev).replace("MIFAO", "MIFAO "),
                    cov=md_escape(cover_evidence(ev)),
                    plan="yes" if "figure" in kinds else "",
                    photo="yes" if "plate" in kinds else "",
                    act=b.get("proposed_action", ""),
                    join=join or "—",
                )
            )
        return "\n".join(lines)

    priority = [
        "MIFAO82-robat-agha-kemal",
        "MIFAO82-robat-atabaki",
        "MIFAO82-robat-golkan",
        "MIFAO81-robat-kerim",
        "MIFAO82-robat-meymeh",
        "MIFAO82-robat-miyan",
        "MIFAO82-robat-mourtcheh-khort",
        "MIFAO82-robat-sanches",
        "MIFAO82-robat-sangui-aliabad",
        "MIFAO82-robat-sangui-allahvidjeh",
        "MIFAO82-robat-sangui-natanz",
        "MIFAO81-robat-sharaf",
        "MIFAO82-robat-soltan-sassanid",
        "MIFAO82-robat-soltan-seljuk",
        "MIFAO82-robat-turk",
        "MIFAO82-robat-zendan",
    ]
    rest = [b["working_id"] for b in BUILDINGS if b["working_id"] not in priority]

    text = f"""# MIFAO 81 & 82 name list (human-editable)

Working list of caravanserais and related roadside buildings extracted from Maxime Siroux:

- **MIFAO 81** — *Caravansérails d'Iran et petites constructions routières* (IFAO, 1949). [Internet Archive](https://archive.org/details/MIFAO81)
- **MIFAO 82** — *Anciennes voies et monuments routiers de la région d'Ispahân* (IFAO, 1971). [Internet Archive](https://archive.org/details/MIFAO82)

Machine-readable copies: [`data/mifao-review-queue.csv`](../data/mifao-review-queue.csv) (one row per building) and [`data/mifao-evidence.csv`](../data/mifao-evidence.csv) (one row per source attestation). **Edit the CSVs.** This markdown is regenerated from `scripts/seed_mifao_review_queue.py` only when reseeding.

## Status

Every row is `review_status=candidate`. OCR of the 1949/1971 scans mangles names; plans and photographs are poor-quality rasters. Do not ingest RDF or create Wikidata items until a reviewer sets `review_status=accepted` and fills `unesco_id` / `wikidata` (accepted joins). Columns `proposed_unesco_id` and `proposed_wikidata` are unverified hints.

| Count | n |
| --- | --- |
| Buildings in this list | **{n}** |
| Attested in MIFAO 81 | {n81} |
| Attested in MIFAO 82 | {n82} |
| With an in-text plan (figure) | {n_plan} |
| With a photograph (plate) | {n_photo} |
| With a proposed UNESCO join | {n_unesco} |

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

{rows(priority)}

## B. Other Siroux buildings (plans, photographs, national survey)

{rows(rest)}

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
"""
    NAME_LIST.write_text(text, encoding="utf-8")


def main():
    write_csv()
    write_markdown()
    print(f"wrote {QUEUE} ({len(BUILDINGS)} buildings)")
    n_ev = sum(len(b['evidence']) for b in BUILDINGS)
    print(f"wrote {EVIDENCE} ({n_ev} evidence rows)")
    print(f"wrote {NAME_LIST}")


if __name__ == "__main__":
    main()
