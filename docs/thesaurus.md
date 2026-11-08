# Caravanserai concept thesaurus (recommended scope)

A **limited SKOS concept scheme** belongs in this graph. It is the right place for names of spaces, elements, building types, and periods. It is the wrong place for BOT topology or for a general Islamic-architecture vocabulary.

## Why a thesaurus, not more OWL classes

BOT already answers “what kind of zone is this”: `bot:Space`, `bot:Element`, `bot:Zone`. `persarch:Sahn` and `persarch:Iwan` subclass those so a courtyard can `bot:adjacentZone` an iwan.

AAT, LCSH, and Wikidata answer a different question: “what cultural concept is this called, and what is it the same as elsewhere?” Those authorities publish **concepts**, not BOT classes. Mapping an OWL class with `owl:sameAs` to AAT or Wikidata is the mistake this project already forbids. `skos:exactMatch` / `closeMatch` / `relatedMatch` / `broadMatch` on **SKOS concepts** is the match.

The existing `crm:E55_Type` individuals (`persarch:type_caravanserai`, `style_safavid`, …) are a seed. Promote them into a concept scheme instead of growing a second OWL taxonomy.

## Scope (keep it small)

Include only terms that appear on Persian caravanserais in this graph:

| Facet | Examples |
| --- | --- |
| Building types | caravanserai, ribat / robât, urban caravanserai, mountain caravanserai, octagonal, circular, dual-court |
| Spaces (`bot:Space`) | sahn, iwan / eïwan, hashti, hujra, stable, mosque space, hammam, ab-anbar, kitchen |
| Elements (`bot:Element`) | pishtaq, mihrab, dome, howz, well, corner tower, inscription |
| Roadside kin | tchapar-khaneh, tchaï-khaneh, qaleh used as a stage |
| Periods / styles | Sasanian, Seljuk, Ilkhanid, Timurid, Safavid, Qajar |
| Materials | brick, stone, adobe, tile, stucco |

Exclude: general mosque typology, cities, people, materials beyond those used in the case studies, and any AAT branch that is not cited from a record here.

Each concept carries:

- preferred labels in English and Persian
- alternate labels for Siroux French (`eïwan`, `robât`, `âb-ambar`, `tchapar-khâneh`) and UNESCO English
- `skos:inScheme` this thesaurus
- one mapping to AAT, LCSH, and Wikidata when the match is known, with the **strength** stated

## Mapping policy

| Property | Use when |
| --- | --- |
| `skos:exactMatch` | Same concept, same scope (caravanserai ↔ AAT 300007148 ↔ WD Q186347) |
| `skos:closeMatch` | Same idea, slightly different scope (sahn ↔ AAT courtyard 300004095) |
| `skos:broadMatch` | Our term is narrower (hujra ↔ lodging room) |
| `skos:relatedMatch` | Associated, not equivalent (ribat ↔ caravanserai; chapar-khaneh ↔ caravanserai) |

Do not use `owl:sameAs` for AAT, LCSH, or Wikidata concepts. LCSH headings are subjects (`lcsh:sh85020073` Caravansaries); they are close or exact matches, not OWL classes.

Link the OWL class to the concept with `skos:exactMatch` or `crm:P2_has_type`, so a `persarch:Iwan` space is typed by the iwan concept and still participates in `bot:adjacentZone`.

## What this is for

- Reconciling Siroux, UNESCO, Wikidata, and (later) Wolfram labels without collapsing buildings.
- IIIF canvas metadata (`motivation: classifying`) pointing at a concept, not a free-text “iwan”.
- SPARQL: “spaces that are iwans” via the concept, including French captions.

File when implemented: `ontology/caravanserai-thesaurus.ttl` (SKOS only). Keep it editor-reviewed; do not auto-mint concepts from OCR.

Arcade , رشته طاق يا طاقها
Arcogival, قوس جناغی
Arcature Courante, طاق نما
Arc Porteur, طاق باربر
alcôves, فرورفتگی
Arcature, طاق نما
Arc Ovoide, قوس تخم مرغی/هلوچين
Baie, روزنه/درگاهی باز
Bâtisses en terre, ساختمانهای خشتی
Bosquet, مرغزار
Bivouaque, اردوگاه موقت
En berceau, گهواره‌ای
Berceau Brise, گهواره‌ای جناغی/تيز
Bute, تکيه گاه/آغاز شده
chambres, اطاقها
charvadars, چاروادار
Constructions, ساخت و ساز
Cupole Plate, گنبد کم خيز
Vule Defoure, طاق ربعی
Cintre(Plain Cintre), نيم‌دايره
Cinter, طاق زدن
Dublean, طاق عرضی چهار بخش
Encoignure, زاويه دو برابر
Eeoincon, لچکی
ecuries, اصطبلها
Foundation, شالوده
Goute De Suif, خياره‌ای
hall central, تالار مرکزی
Hôteliers, اقامتگاه
installations intérieures, فضاهای داخلی
Lieu d;etape, منزلگاه
eïwan , ايوان
matériaux, مصالح
Mottr, کلوخ
Niche, تورفتگی/طاقچه/درگاه
Niche Aveugle, طاق نما/طاقچه
passage, راه رو/گذرگاه
Pavillon, عمارت منفرد/کلاه فرنگی
Pendantif, گوشوار
perpendiculairement,  به طور عمود
Peristyle, دالان ستون دار/رواق دوره
Porche, سرپوشيده
Portail, سر در
Portique,  رواق
Refection, بازسازی
Restituer, احيا کردن/ به صورت اوليه
Restauration, مرمت
Soubassement, زيربنا
Sanctuaire, گنبدخانه/مقصوره/حرم
tours, برجهت
Trompe, ترنب/ترنبه
Trompillon, ترنب کوجک
Trajet, خط سير
Trave, دهانه/دربند/کوچه
Typan, پيشانی بالای در ورودی
Voute en Plein Cintre, طاق نيمدايره
Voute en Plein Berceau, گهواره‌ای
Voute en Plein Ogive, جناغی
Voute en Plein d'arete, تيزدار
Voute en Plein tunel, کوره پوش
