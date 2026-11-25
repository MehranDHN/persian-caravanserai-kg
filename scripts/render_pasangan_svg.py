#!/usr/bin/env python3
"""Draw Pasangan instance SVG from data/pasangan-coste.ttl.

Each bot:Space / bot:Element becomes an SVG group whose id is the local
name (wd_Q5959343_muleteer_platform_n_1). data-iri holds the full KG IRI.
Layout is the square four-iwan grammar (north at top, south entrance),
not a pixel trace of the Coste raster.

Series individuals (Coste 4, 5, 8, 9, 11, 12) are one hatched group.
Dashed cells are a morphological census only — they are not RDF.

    python scripts/render_pasangan_svg.py
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from rdflib import Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "data" / "pasangan-coste.ttl"
OUT_SVG = ROOT / "docs" / "infographics" / "pasangan-instances.svg"
OUT_HTML = ROOT / "docs" / "infographics" / "pasangan-instances.html"

NS = Namespace("https://w3id.org/persian-caravanserai-kg#")
BOT = Namespace("https://w3id.org/bot#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
PERS = Namespace("https://w3id.org/persian-architecture#")

CX, CY = 520.0, 500.0
# Envelope 40 m E–W × 38 m N–S (scale-bar E54).
HX, HY = 380.0, 361.0
W, H = 1040, 1240

# Ring radii as fractions of the half-envelope (inner → outer).
R_CIST = 0.13
R_SAHN = 0.46
R_PLAT = 0.54
R_HUJRA = 0.66
R_STABLE = 0.84
R_OUTER = 1.00

FILL = {
    "1": "#c56a4a",
    "2": "#e8b89a",
    "3": "#f7f1e8",
    "4": "#d5ebe6",
    "5": "#c9dcc4",
    "6": "#e8d5c4",
    "7": "#f3e2b0",
    "8": "#9c4328",
    "9": "#ddd6ce",
    "10": "#b7d0dc",
    "11": "#8a7a6b",
    "12": "#6b7c86",
    "tower": "#5c534c",
}


def load_graph() -> Graph:
    g = Graph()
    g.parse(TTL, format="turtle")
    return g


def label_of(g: Graph, uri: URIRef) -> str:
    for o in g.objects(uri, RDFS.label):
        if getattr(o, "language", None) == "en":
            return str(o)
    labs = list(g.objects(uri, RDFS.label))
    return str(labs[0]) if labs else uri.split("#")[-1]


def locator_of(g: Graph, uri: URIRef) -> str:
    for o in g.objects(uri, PERS.locator):
        return str(o)
    return ""


def neighbours(g: Graph, uri: URIRef) -> list[str]:
    out = []
    for p in (BOT.adjacentZone, BOT.adjacentElement, BOT.containsElement, BOT.containsZone):
        for o in g.objects(uri, p):
            if isinstance(o, URIRef):
                out.append(o.split("#")[-1])
    return sorted(set(out))


def pt(face: str, t: float, r: float) -> tuple[float, float]:
    hx, hy = HX * r, HY * r
    t = max(0.0, min(1.0, t))
    if face == "n":
        return (CX - hx + t * 2 * hx, CY - hy)
    if face == "s":
        return (CX - hx + t * 2 * hx, CY + hy)
    if face == "w":
        return (CX - hx, CY - hy + t * 2 * hy)
    if face == "e":
        return (CX + hx, CY - hy + t * 2 * hy)
    raise ValueError(face)


def ring_poly(face: str, t0: float, t1: float, r_in: float, r_out: float) -> str:
    a, b = pt(face, t0, r_in), pt(face, t1, r_in)
    c, d = pt(face, t1, r_out), pt(face, t0, r_out)
    return "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1])


def centroid(points: str) -> tuple[float, float]:
    xs, ys = [], []
    for pair in points.split():
        x, y = pair.split(",")
        xs.append(float(x))
        ys.append(float(y))
    return sum(xs) / len(xs), sum(ys) / len(ys)


def chamfer_pts(r: float, cut: float = 0.18) -> str:
    hx, hy = HX * r, HY * r
    c = cut
    pts = [
        (CX - hx + c * hx, CY - hy),
        (CX + hx - c * hx, CY - hy),
        (CX + hx, CY - hy + c * hy),
        (CX + hx, CY + hy - c * hy),
        (CX + hx - c * hx, CY + hy),
        (CX - hx + c * hx, CY + hy),
        (CX - hx, CY + hy - c * hy),
        (CX - hx, CY - hy + c * hy),
    ]
    return " ".join("%.1f,%.1f" % p for p in pts)


def square_pts(r: float) -> str:
    hx, hy = HX * r, HY * r
    return "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        CX - hx,
        CY - hy,
        CX + hx,
        CY - hy,
        CX + hx,
        CY + hy,
        CX - hx,
        CY + hy,
    )


def g_el(
    local: str,
    coste: str,
    points: str,
    g: Graph,
    extra: str = "",
    kind: str = "polygon",
    circle: tuple[float, float, float] | None = None,
    series: bool = False,
    shapes: list[str] | None = None,
    shown: str | None = None,
) -> str:
    uri = NS[local]
    lab = label_of(g, uri)
    loc = locator_of(g, uri)
    nbr = neighbours(g, uri)
    iri = str(uri)
    fill = FILL.get(coste, "#eee")
    title = "%s — %s" % (local, lab)
    data_nbr = " ".join(nbr)
    klass = "inst coste-%s" % coste
    if series:
        klass += " series"
    common = (
        'id="%s" class="%s" data-iri="%s" data-coste="%s" '
        'data-locator="%s" data-label="%s" data-nbr="%s" data-grain="%s"'
        % (
            local,
            klass,
            escape(iri, {"\"": "&quot;"}),
            coste,
            escape(loc, {"\"": "&quot;"}),
            escape(lab, {"\"": "&quot;"}),
            escape(data_nbr, {"\"": "&quot;"}),
            "series" if series else "instance",
        )
    )
    inner_title = "<title>%s</title>" % escape(title)
    href = iri
    body = []
    if kind == "circle" and circle:
        cx, cy, rad = circle
        body.append(
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#1c1714" stroke-width="1.2"/>'
            % (cx, cy, rad, fill)
        )
        if series:
            body.append(
                '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#hatch-series)" stroke="none"/>'
                % (cx, cy, rad)
            )
        tx, ty = cx, cy
    else:
        polys = shapes if shapes else [points]
        for p in polys:
            body.append(
                '<polygon points="%s" fill="%s" stroke="#1c1714" stroke-width="1.2"/>'
                % (p, fill)
            )
            if series:
                body.append(
                    '<polygon points="%s" fill="url(#hatch-series)" stroke="none"/>' % p
                )
        tx, ty = centroid(polys[0] if polys else points)
    label = shown if shown is not None else (loc if loc else local.replace("wd_Q5959343_", ""))
    if len(label) > 20:
        label = label[:18] + "…"
    text = (
        '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" '
        'font-size="8.5" font-family="Segoe UI, Source Sans 3, sans-serif" fill="#1c1714">%s</text>'
        % (tx, ty, escape(label))
    )
    return (
        '<a href="%s"><g %s>%s%s%s%s</g></a>\n'
        % (escape(href), common, inner_title, "".join(body), text, extra)
    )


def candidate(cid: str, coste: str, points: str, locator: str, note: str) -> str:
    tx, ty = centroid(points)
    title = escape("%s — %s (not in RDF)" % (cid, note))
    return (
        '<g id="%s" class="candidate coste-%s" data-iri="" data-coste="%s" '
        'data-locator="%s" data-label="%s" data-nbr="" data-grain="candidate">'
        "<title>%s</title>"
        '<polygon points="%s" fill="none" stroke="#9c4328" stroke-width="1.1" '
        'stroke-dasharray="5 3.5" opacity="0.95"/>'
        '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" '
        'font-size="7" font-family="Segoe UI, sans-serif" fill="#9c4328">%s</text>'
        "</g>\n"
        % (
            cid,
            coste,
            coste,
            escape(locator, {"\"": "&quot;"}),
            escape(note, {"\"": "&quot;"}),
            title,
            points,
            tx,
            ty,
            escape(locator),
        )
    )


def build_svg(g: Graph) -> str:
    parts: list[str] = []
    parts.append(
        '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-labelledby="title desc">
<title id="title">Pasangan instance plan — each shape is a KG individual</title>
<desc id="desc">Schematic square four-iwan generated from data/pasangan-coste.ttl.
Group ids match RDF local names. Series Coste keys 4, 5, 8, 9, 11, 12 are one
hatched IRI. Dashed cells are a morphological census and are not minted.
Example: wd_Q5959343_muleteer_platform_n_1.</desc>
<style>
  .inst {{ cursor: pointer; }}
  .inst:hover polygon, .inst:hover circle {{ stroke: #9c4328; stroke-width: 3; }}
  .inst.selected polygon, .inst.selected circle {{ stroke: #9c4328; stroke-width: 3.5; }}
  .candidate {{ cursor: pointer; }}
  .candidate:hover polygon {{ stroke-width: 2.4; }}
  .candidate.selected polygon {{ stroke-width: 2.6; fill: rgba(156,67,40,0.08); }}
  a {{ text-decoration: none; }}
  text {{ pointer-events: none; }}
</style>
<defs>
  <pattern id="hatch-series" patternUnits="userSpaceOnUse" width="7" height="7">
    <path d="M0,7 L7,0" stroke="#1c1714" stroke-width="0.55" opacity="0.28"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#f7f1e8"/>
<text x="520" y="32" text-anchor="middle" font-size="22" font-weight="700"
      font-family="Georgia, Source Serif 4, serif" fill="#1c1714">Pasangan — instance plan from BOT RDF</text>
<text x="520" y="54" text-anchor="middle" font-size="12"
      font-family="Segoe UI, sans-serif" fill="#5c534c">Coste Passencan 1867 · :wd_Q5959343 · solid = minted instance · hatch = series IRI · dashed = census, not in RDF · north at top</text>
'''.format(
            w=W, h=H
        )
    )

    parts.append(
        '<polygon points="%s" fill="none" stroke="#1c1714" stroke-width="2.6"/>\n'
        % square_pts(R_OUTER)
    )

    # Sahn 3 (chamfered court)
    parts.append(
        g_el(
            "wd_Q5959343_sahn",
            "3",
            chamfer_pts(R_SAHN),
            g,
            shown="3 sahn",
        )
    )
    # Cistern 10 + prayer platform (element on top of cistern)
    parts.append(
        g_el(
            "wd_Q5959343_cistern",
            "10",
            square_pts(R_CIST),
            g,
            shown="10 cistern",
        )
    )
    parts.append(
        g_el(
            "wd_Q5959343_prayer_platform",
            "10",
            "",
            g,
            kind="circle",
            circle=(CX, CY, 14),
            shown="10",
        )
    )

    # Traveller platforms 5 — one series IRI, four court-edge bands
    plat = [
        ring_poly("n", 0.08, 0.92, R_SAHN, R_PLAT),
        ring_poly("e", 0.08, 0.92, R_SAHN, R_PLAT),
        ring_poly("w", 0.08, 0.92, R_SAHN, R_PLAT),
        ring_poly("s", 0.08, 0.34, R_SAHN, R_PLAT),
        ring_poly("s", 0.66, 0.92, R_SAHN, R_PLAT),
    ]
    parts.append(
        g_el(
            "wd_Q5959343_traveller_platform",
            "5",
            plat[0],
            g,
            series=True,
            shapes=plat,
            shown="5 series",
        )
    )

    # Hujra 4 — one series IRI, inner lodging ring
    huj = [
        ring_poly("n", 0.06, 0.94, R_PLAT, R_HUJRA),
        ring_poly("e", 0.06, 0.94, R_PLAT, R_HUJRA),
        ring_poly("w", 0.06, 0.94, R_PLAT, R_HUJRA),
        ring_poly("s", 0.06, 0.32, R_PLAT, R_HUJRA),
        ring_poly("s", 0.68, 0.94, R_PLAT, R_HUJRA),
    ]
    parts.append(
        g_el(
            "wd_Q5959343_hujra",
            "4",
            huj[0],
            g,
            series=True,
            shapes=huj,
            shown="4 series",
        )
    )

    # Stables 6 — four instance ranges
    for face, local in (
        ("n", "wd_Q5959343_stables_n"),
        ("e", "wd_Q5959343_stables_e"),
        ("s", "wd_Q5959343_stables_s"),
        ("w", "wd_Q5959343_stables_w"),
    ):
        t0, t1 = (0.08, 0.92) if face != "s" else (0.06, 0.94)
        if face == "s":
            # south stables run either side of the porch stack
            parts.append(
                g_el(
                    local,
                    "6",
                    ring_poly("s", 0.06, 0.34, R_HUJRA, R_STABLE),
                    g,
                    shapes=[
                        ring_poly("s", 0.06, 0.34, R_HUJRA, R_STABLE),
                        ring_poly("s", 0.66, 0.94, R_HUJRA, R_STABLE),
                    ],
                    shown="6; S",
                )
            )
        else:
            parts.append(
                g_el(local, "6", ring_poly(face, t0, t1, R_HUJRA, R_STABLE), g)
            )

    # Muleteer 7 — sixteen instance rooms. N/S west→east; E/W north→south.
    n_bays = [
        ("wd_Q5959343_muleteer_platform_n_1", 0.00, 0.22),
        ("wd_Q5959343_muleteer_platform_n_2", 0.22, 0.44),
        ("wd_Q5959343_muleteer_platform_n_3", 0.56, 0.78),
        ("wd_Q5959343_muleteer_platform_n_4", 0.78, 1.00),
    ]
    for local, t0, t1 in n_bays:
        parts.append(g_el(local, "7", ring_poly("n", t0, t1, R_STABLE, R_OUTER), g))

    e_bays = [
        ("wd_Q5959343_muleteer_platform_e_1", 0.00, 0.22),
        ("wd_Q5959343_muleteer_platform_e_2", 0.22, 0.44),
        ("wd_Q5959343_muleteer_platform_e_3", 0.56, 0.78),
        ("wd_Q5959343_muleteer_platform_e_4", 0.78, 1.00),
    ]
    for local, t0, t1 in e_bays:
        parts.append(g_el(local, "7", ring_poly("e", t0, t1, R_STABLE, R_OUTER), g))

    s_bays = [
        ("wd_Q5959343_muleteer_platform_s_1", 0.00, 0.22),
        ("wd_Q5959343_muleteer_platform_s_2", 0.22, 0.38),
        ("wd_Q5959343_muleteer_platform_s_3", 0.62, 0.78),
        ("wd_Q5959343_muleteer_platform_s_4", 0.78, 1.00),
    ]
    for local, t0, t1 in s_bays:
        parts.append(g_el(local, "7", ring_poly("s", t0, t1, R_STABLE, R_OUTER), g))

    w_bays = [
        ("wd_Q5959343_muleteer_platform_w_1", 0.00, 0.22),
        ("wd_Q5959343_muleteer_platform_w_2", 0.22, 0.44),
        ("wd_Q5959343_muleteer_platform_w_3", 0.56, 0.78),
        ("wd_Q5959343_muleteer_platform_w_4", 0.78, 1.00),
    ]
    for local, t0, t1 in w_bays:
        parts.append(g_el(local, "7", ring_poly("w", t0, t1, R_STABLE, R_OUTER), g))

    # South entrance stack
    parts.append(
        g_el(
            "wd_Q5959343_porch",
            "2",
            ring_poly("s", 0.38, 0.62, R_SAHN, R_STABLE),
            g,
            shown="2 porch",
        )
    )
    parts.append(
        g_el(
            "wd_Q5959343_entrance",
            "1",
            ring_poly("s", 0.40, 0.60, R_STABLE, R_OUTER),
            g,
            shown="1",
        )
    )

    # Latrines 9 — one series IRI; plate has a 9 at each outer corner.
    # Four compact badges share the series IRI so the collapse is visible.
    corner_badges = []
    for face, t, r in (
        ("n", 0.05, (R_STABLE + R_OUTER) / 2),
        ("n", 0.95, (R_STABLE + R_OUTER) / 2),
        ("s", 0.05, (R_STABLE + R_OUTER) / 2),
        ("s", 0.95, (R_STABLE + R_OUTER) / 2),
    ):
        x, y = pt(face, t, r)
        s = 11
        corner_badges.append(
            "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f"
            % (x - s, y - s, x + s, y - s, x + s, y + s, x - s, y + s)
        )
    parts.append(
        g_el(
            "wd_Q5959343_latrines",
            "9",
            corner_badges[0],
            g,
            series=True,
            shapes=corner_badges,
            shown="9 series",
        )
    )

    # Stairs 8 — one series Element; plate repeats 8 at four inner corners
    stair_pts = []
    for face, t in (("n", 0.18), ("n", 0.82), ("s", 0.18), ("s", 0.82)):
        x, y = pt(face, t, (R_HUJRA + R_STABLE) / 2)
        stair_pts.append((x, y, 9))
    # draw as four circles inside one group
    uri = NS["wd_Q5959343_stairs"]
    lab = label_of(g, uri)
    loc = locator_of(g, uri)
    nbr = " ".join(neighbours(g, uri))
    parts.append(
        '<a href="%s"><g id="wd_Q5959343_stairs" class="inst series coste-8" '
        'data-iri="%s" data-coste="8" data-locator="%s" data-label="%s" '
        'data-nbr="%s" data-grain="series"><title>%s</title>'
        % (
            escape(str(uri)),
            escape(str(uri), {"\"": "&quot;"}),
            escape(loc, {"\"": "&quot;"}),
            escape(lab, {"\"": "&quot;"}),
            escape(nbr, {"\"": "&quot;"}),
            escape("wd_Q5959343_stairs — %s" % lab),
        )
    )
    for x, y, rad in stair_pts:
        parts.append(
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#1c1714" stroke-width="1.2"/>'
            % (x, y, rad, FILL["8"])
        )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="8" '
        'font-family="Segoe UI, sans-serif" fill="#fff">8</text></g></a>\n'
        % (stair_pts[0][0], stair_pts[0][1] + 0.5)
    )

    # Chimneys 11 and niches 12 — series fittings inside the hujra ring
    chim_pts = []
    for face, ts in (("n", (0.28, 0.72)), ("e", (0.28, 0.72)), ("w", (0.28, 0.72))):
        for t in ts:
            chim_pts.append(pt(face, t, (R_PLAT + R_HUJRA) / 2))
    parts.append(
        '<a href="%s"><g id="wd_Q5959343_chimneys" class="inst series coste-11" '
        'data-iri="%s" data-coste="11" data-locator="11" data-label="%s" '
        'data-nbr="%s" data-grain="series"><title>wd_Q5959343_chimneys — Chimneys (Coste 11)</title>'
        % (
            escape(str(NS["wd_Q5959343_chimneys"])),
            escape(str(NS["wd_Q5959343_chimneys"]), {"\"": "&quot;"}),
            escape(label_of(g, NS["wd_Q5959343_chimneys"]), {"\"": "&quot;"}),
            escape(" ".join(neighbours(g, NS["wd_Q5959343_chimneys"])), {"\"": "&quot;"}),
        )
    )
    for x, y in chim_pts:
        parts.append(
            '<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s" stroke="#1c1714" stroke-width="0.9"/>'
            % (x, y, FILL["11"])
        )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="8" '
        'font-family="Segoe UI, sans-serif" fill="#1c1714">11 series</text></g></a>\n'
        % (CX, CY - HY * (R_PLAT + R_HUJRA) / 2 + 18)
    )

    niche_pts = []
    for face, ts in (("n", (0.40, 0.60)), ("e", (0.40, 0.60)), ("w", (0.40, 0.60)), ("s", (0.22, 0.78))):
        for t in ts:
            niche_pts.append(pt(face, t, (R_PLAT + R_HUJRA) / 2 + 0.02))
    parts.append(
        '<a href="%s"><g id="wd_Q5959343_niches" class="inst series coste-12" '
        'data-iri="%s" data-coste="12" data-locator="12" data-label="%s" '
        'data-nbr="%s" data-grain="series"><title>wd_Q5959343_niches — Niches (Coste 12)</title>'
        % (
            escape(str(NS["wd_Q5959343_niches"])),
            escape(str(NS["wd_Q5959343_niches"]), {"\"": "&quot;"}),
            escape(label_of(g, NS["wd_Q5959343_niches"]), {"\"": "&quot;"}),
            escape(" ".join(neighbours(g, NS["wd_Q5959343_niches"])), {"\"": "&quot;"}),
        )
    )
    for x, y in niche_pts:
        parts.append(
            '<rect x="%.1f" y="%.1f" width="7" height="7" fill="%s" stroke="#1c1714" stroke-width="0.8"/>'
            % (x - 3.5, y - 3.5, FILL["12"])
        )
    parts.append("</g></a>\n")

    # Towers
    for name, (fx, fy) in (
        ("nw", (-1, -1)),
        ("ne", (1, -1)),
        ("sw", (-1, 1)),
        ("se", (1, 1)),
    ):
        x, y = CX + fx * HX, CY + fy * HY
        parts.append(
            g_el(
                "wd_Q5959343_tower_%s" % name,
                "tower",
                "",
                g,
                kind="circle",
                circle=(x, y, 22),
                shown=name.upper(),
            )
        )

    # --- Morphological census (presentation only) ---
    # Inner hujra cells Coste 4: 5 bays on N/E/W (incl. iwan), 2 south of porch.
    def bins(n: int, lo: float = 0.06, hi: float = 0.94):
        span = hi - lo
        return [(lo + i * span / n, lo + (i + 1) * span / n) for i in range(n)]

    for i, (t0, t1) in enumerate(bins(5), start=1):
        parts.append(
            candidate(
                "candidate_hujra_n_%d" % i,
                "4",
                ring_poly("n", t0, t1, R_PLAT, R_HUJRA),
                "4; N; cell %d" % i,
                "Closed inner cell on the north ring (Coste 4). Census only.",
            )
        )
        parts.append(
            candidate(
                "candidate_hujra_e_%d" % i,
                "4",
                ring_poly("e", t0, t1, R_PLAT, R_HUJRA),
                "4; E; cell %d" % i,
                "Closed inner cell on the east ring (Coste 4). Census only.",
            )
        )
        parts.append(
            candidate(
                "candidate_hujra_w_%d" % i,
                "4",
                ring_poly("w", t0, t1, R_PLAT, R_HUJRA),
                "4; W; cell %d" % i,
                "Closed inner cell on the west ring (Coste 4). Census only.",
            )
        )
    parts.append(
        candidate(
            "candidate_hujra_s_w",
            "4",
            ring_poly("s", 0.06, 0.32, R_PLAT, R_HUJRA),
            "4; S; W",
            "Hujra west of porch. Census only.",
        )
    )
    parts.append(
        candidate(
            "candidate_hujra_s_e",
            "4",
            ring_poly("s", 0.68, 0.94, R_PLAT, R_HUJRA),
            "4; S; E",
            "Hujra east of porch. Census only.",
        )
    )

    # Traveller platforms 5 in front of those cells (not on iwan axes).
    for face, idxs in (("n", (1, 2, 4, 5)), ("e", (1, 2, 4, 5)), ("w", (1, 2, 4, 5))):
        for i in idxs:
            t0, t1 = bins(5)[i - 1]
            parts.append(
                candidate(
                    "candidate_platform_%s_%d" % (face, i),
                    "5",
                    ring_poly(face, t0, t1, R_SAHN, R_PLAT),
                    "5; %s; cell %d" % (face.upper(), i),
                    "Court-edge platform (Coste 5). Census only.",
                )
            )
    parts.append(
        candidate(
            "candidate_platform_s_w",
            "5",
            ring_poly("s", 0.08, 0.32, R_SAHN, R_PLAT),
            "5; S; W",
            "Court-edge platform west of porch. Census only.",
        )
    )
    parts.append(
        candidate(
            "candidate_platform_s_e",
            "5",
            ring_poly("s", 0.68, 0.92, R_SAHN, R_PLAT),
            "5; S; E",
            "Court-edge platform east of porch. Census only.",
        )
    )

    # Four latrine candidates at the outer corners (printed 9 on the plate).
    for cid, face, t, loc in (
        ("candidate_latrine_nw", "n", 0.04, "9; NW"),
        ("candidate_latrine_ne", "n", 0.96, "9; NE"),
        ("candidate_latrine_sw", "s", 0.04, "9; SW"),
        ("candidate_latrine_se", "s", 0.96, "9; SE"),
    ):
        x, y = pt(face, t, (R_STABLE + R_OUTER) / 2)
        s = 16
        box = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            x - s,
            y - s,
            x + s,
            y - s,
            x + s,
            y + s,
            x - s,
            y + s,
        )
        parts.append(candidate(cid, "9", box, loc, "Corner latrine on the plate. Census only."))

    # North arrow
    parts.append(
        '<g transform="translate(520,86)" fill="#1c1714">'
        '<polygon points="0,-14 6,4 -6,4"/>'
        '<text y="18" text-anchor="middle" font-size="11">N</text></g>\n'
    )

    legend = [
        ("7 muleteer (16 IRIs)", FILL["7"]),
        ("6 stables (4 IRIs)", FILL["6"]),
        ("4 hujra (series)", FILL["4"]),
        ("5 platform (series)", FILL["5"]),
        ("1–2 entrance", FILL["1"]),
        ("9 latrine (series)", FILL["9"]),
        ("10 cistern", FILL["10"]),
        ("tower", FILL["tower"]),
    ]
    y = 1088
    x = 48
    parts.append('<g font-size="11" font-family="Segoe UI, sans-serif" fill="#1c1714">\n')
    for lab, col in legend:
        parts.append(
            '<rect x="%.0f" y="%.0f" width="14" height="14" fill="%s" stroke="#1c1714"/>'
            '<text x="%.0f" y="%.0f">%s</text>\n' % (x, y, col, x + 20, y + 12, escape(lab))
        )
        x += 122
    parts.append("</g>\n")

    # Census table
    parts.append(
        '''<g font-family="Segoe UI, sans-serif" fill="#1c1714">
<text x="70" y="1128" font-size="12" font-weight="700">Morphological census vs RDF (do not mint dashed cells until HITL)</text>
<text x="70" y="1148" font-size="11" fill="#5c534c">Key 4: 1 series Space · plate ~17 inner cells · Key 5: 1 series · plate ~14 platforms</text>
<text x="70" y="1166" font-size="11" fill="#5c534c">Key 6: 4 ranges minted · Key 7: 16 rooms minted · Key 8: 1 series Element · plate 4 flights</text>
<text x="70" y="1184" font-size="11" fill="#5c534c">Key 9: 1 series Space · plate 4 corner 9s · Keys 11–12: 1 series Element each · many fittings</text>
<text x="520" y="1218" text-anchor="middle" font-size="10" fill="#5c534c">Fragment IRI: …/pasangan-instances.svg#wd_Q5959343_muleteer_platform_n_1 · generated from data/pasangan-coste.ttl</text>
</g>
'''
    )
    parts.append("</svg>\n")
    return "".join(parts)


def build_html(svg: str) -> str:
    inner = svg.split("?>", 1)[-1].strip()
    if inner.startswith("<?xml"):
        inner = inner.split(">", 1)[-1].strip()
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Pasangan — instance plan (BOT RDF → SVG)</title>
  <style>
    :root { --ink:#1c1714; --muted:#5c534c; --paper:#f7f1e8; --card:#fffdf8; --hit:#9c4328; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:"Segoe UI", "Source Sans 3", sans-serif; background:var(--paper); color:var(--ink); }
    header { padding:20px 28px 8px; border-bottom:3px solid var(--ink); }
    header h1 { font-family: Georgia, serif; font-size:26px; margin:0 0 6px; }
    header p { margin:0; color:var(--muted); max-width: 70ch; }
    .wrap { display:grid; grid-template-columns: 1fr 340px; min-height: calc(100vh - 100px); }
    .stage { padding:8px; overflow:auto; }
    .stage svg { width:100%; height:auto; max-height:calc(100vh - 120px); }
    .inst.selected polygon, .inst.selected circle, .inst.selected rect { stroke:#9c4328; stroke-width:3.5; }
    aside { background:var(--card); border-left:1px solid #d4c7b8; padding:18px 20px; }
    aside h2 { font-size:13px; letter-spacing:.14em; text-transform:uppercase; color:var(--hit); margin:0 0 10px; }
    #iri { font-family: Consolas, "Courier New", monospace; font-size:12px; word-break:break-all; background:#f0e6d8; padding:8px; }
    #meta dt { color:var(--muted); font-size:12px; margin-top:10px; }
    #meta dd { margin:2px 0 0; font-size:14px; }
    #nbr a { display:block; font-size:12px; color:var(--hit); }
    .hint { font-size:13px; color:var(--muted); margin-top:16px; }
    .pill { display:inline-block; font-size:11px; letter-spacing:.08em; text-transform:uppercase;
            padding:2px 8px; border:1px solid var(--hit); color:var(--hit); border-radius:99px; }
  </style>
</head>
<body>
  <header>
    <h1>Pasangan instance plan</h1>
    <p>Each solid or hatched shape is one RDF individual from <code>data/pasangan-coste.ttl</code>.
       Hatched rooms are <strong>series</strong> (one IRI for many closed cells).
       Dashed outlines are a morphological census and are <strong>not</strong> in the graph until HITL review.</p>
  </header>
  <div class="wrap">
    <div class="stage" id="plan">
      SVG_INLINE
    </div>
    <aside>
      <h2>Selected instance</h2>
      <div id="grain" class="pill">instance</div>
      <div id="iri" style="margin-top:10px">https://w3id.org/persian-caravanserai-kg#wd_Q5959343_muleteer_platform_n_1</div>
      <dl id="meta">
        <dt>Label</dt><dd id="lab">Muleteer platform, north range bay 1</dd>
        <dt>Coste locator</dt><dd id="loc">7; N; bay 1 west to east</dd>
        <dt>Legend key</dt><dd id="coste">7</dd>
        <dt>BOT neighbours</dt><dd id="nbr"></dd>
      </dl>
      <p class="hint">Deep link: <code>pasangan-instances.svg#wd_Q5959343_muleteer_platform_n_1</code></p>
      <p class="hint">Identify misses: SPARQL inventory (<code>queries/validate-topology.rq</code> V4/V6) against the plate census in the SVG footer. Promote a dashed cell the same way as a MIFAO candidate — review, then mint.</p>
    </aside>
  </div>
  <script>
    const iriEl = document.getElementById('iri');
    const labEl = document.getElementById('lab');
    const locEl = document.getElementById('loc');
    const costeEl = document.getElementById('coste');
    const nbrEl = document.getElementById('nbr');
    const grainEl = document.getElementById('grain');
    function show(g) {
      document.querySelectorAll('.inst.selected, .candidate.selected').forEach(n => n.classList.remove('selected'));
      g.classList.add('selected');
      const grain = g.getAttribute('data-grain') || 'instance';
      grainEl.textContent = grain;
      const iri = g.getAttribute('data-iri') || '';
      iriEl.textContent = iri || '(not in RDF — census candidate)';
      labEl.textContent = g.getAttribute('data-label') || '';
      locEl.textContent = g.getAttribute('data-locator') || '';
      costeEl.textContent = g.getAttribute('data-coste') || '';
      const nbr = (g.getAttribute('data-nbr') || '').trim().split(/\\s+/).filter(Boolean);
      nbrEl.innerHTML = nbr.map(n => '<a href="https://w3id.org/persian-caravanserai-kg#'+n+'">'+n+'</a>').join('') || '—';
    }
    function bind(doc) {
      doc.querySelectorAll('g.inst, g.candidate').forEach(g => {
        g.addEventListener('click', ev => { ev.preventDefault(); ev.stopPropagation(); show(g); });
      });
      const hash = (location.hash || '#wd_Q5959343_muleteer_platform_n_1').slice(1);
      const start = doc.getElementById(hash) || doc.getElementById('wd_Q5959343_muleteer_platform_n_1');
      if (start) show(start);
    }
    bind(document);
  </script>
</body>
</html>
""".replace("SVG_INLINE", inner)


def main() -> int:
    g = load_graph()
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    svg = build_svg(g)
    OUT_SVG.write_text(svg, encoding="utf-8")
    OUT_HTML.write_text(build_html(svg), encoding="utf-8")
    print("Wrote", OUT_SVG)
    print("Wrote", OUT_HTML)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
