#!/usr/bin/env python3
"""Draw Amin-Abad instance SVG from data/amin-abad-coste.ttl.

Each bot:Space / bot:Element becomes an SVG group whose id is the local
name (wd_Q5907540_hujra_nw_2). data-iri holds the full KG IRI. Layout is
the octagon grammar (flat-topped, south entrance), not a pixel trace of
the Coste raster. Regenerate after TTL edits:

    python scripts/render_amin_abad_svg.py
"""
from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

from rdflib import Graph, Namespace, URIRef

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "data" / "amin-abad-coste.ttl"
OUT_SVG = ROOT / "docs" / "infographics" / "amin-abad-instances.svg"
OUT_HTML = ROOT / "docs" / "infographics" / "amin-abad-instances.html"

NS = Namespace("https://w3id.org/persian-caravanserai-kg#")
BOT = Namespace("https://w3id.org/bot#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
PERS = Namespace("https://w3id.org/persian-architecture#")

CX, CY = 520.0, 500.0
R = 390.0  # vertex radius of outer envelope
W, H = 1040, 1180

# Flat-top octagon vertices, CCW from ENE (degrees from +x, SVG y down).
VERT_DEG = [22.5 + 45 * k for k in range(8)]
# v0 ENE, v1 NNE, v2 NNW, v3 WNW, v4 WSW, v5 SSW, v6 SSE, v7 ESE
FACES = {
    "ne": (0, 1),
    "n": (1, 2),
    "nw": (2, 3),
    "w": (3, 4),
    "sw": (4, 5),
    "s": (5, 6),
    "se": (6, 7),
    "e": (7, 0),
}
TOWER_AT = {
    "ene": 0,
    "nne": 1,
    "nnw": 2,
    "wnw": 3,
    "wsw": 4,
    "ssw": 5,
    "sse": 6,
    "ese": 7,
}

# Ring radii as fractions of R (inner → outer).
R_PRAYER = 0.16
R_SAHN = 0.40
R_HUJRA = 0.55
R_STABLE = 0.74
R_OUTER = 0.90
R_TOWER = 1.00

FILL = {
    "7": "#d5ebe6",
    "8": "#e8d5c4",
    "9": "#f3e2b0",
    "10": "#ddd6ce",
    "1": "#c56a4a",
    "2": "#e8b89a",
    "3": "#f0d0c0",
    "4": "#9c4328",
    "5": "#f7f1e8",
    "6": "#c4a574",
    "11": "#b7d0dc",
    "tower": "#5c534c",
}


def polar(deg: float, radius: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return (CX + radius * math.cos(rad), CY - radius * math.sin(rad))


def lerp(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def face_point(face: str, t: float, radius: float) -> tuple[float, float]:
    i, j = FACES[face]
    a = polar(VERT_DEG[i], radius)
    b = polar(VERT_DEG[j], radius)
    return lerp(a, b, t)


def ring_poly(face: str, t0: float, t1: float, r_in: float, r_out: float) -> str:
    pts = [
        face_point(face, t0, r_in * R),
        face_point(face, t1, r_in * R),
        face_point(face, t1, r_out * R),
        face_point(face, t0, r_out * R),
    ]
    return " ".join("%.1f,%.1f" % p for p in pts)


def octagon_pts(radius: float) -> str:
    return " ".join("%.1f,%.1f" % polar(d, radius) for d in VERT_DEG)


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
    for p in (BOT.adjacentZone, BOT.adjacentElement, BOT.containsElement):
        for o in g.objects(uri, p):
            if isinstance(o, URIRef):
                out.append(o.split("#")[-1])
    return sorted(set(out))


def g_el(
    local: str,
    coste: str,
    points: str,
    g: Graph,
    extra: str = "",
    kind: str = "polygon",
    circle: tuple[float, float, float] | None = None,
) -> str:
    uri = NS[local]
    lab = label_of(g, uri)
    loc = locator_of(g, uri)
    nbr = neighbours(g, uri)
    iri = str(uri)
    fill = FILL.get(coste, "#eee")
    title = "%s — %s" % (local, lab)
    data_nbr = " ".join(nbr)
    common = (
        'id="%s" class="inst coste-%s" data-iri="%s" data-coste="%s" '
        'data-locator="%s" data-label="%s" data-nbr="%s"'
        % (
            local,
            coste,
            escape(iri, {"\"": "&quot;"}),
            coste,
            escape(loc, {"\"": "&quot;"}),
            escape(lab, {"\"": "&quot;"}),
            escape(data_nbr, {"\"": "&quot;"}),
        )
    )
    inner_title = "<title>%s</title>" % escape(title)
    href = iri
    if kind == "circle" and circle:
        cx, cy, r = circle
        shape = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#1c1714" stroke-width="1.2"/>' % (
            cx,
            cy,
            r,
            fill,
        )
    else:
        shape = '<polygon points="%s" fill="%s" stroke="#1c1714" stroke-width="1.2"/>' % (
            points,
            fill,
        )
    short = local.replace("wd_Q5907540_", "")
    # centroid-ish for label: average of polygon points, or circle center
    if kind == "circle" and circle:
        tx, ty = circle[0], circle[1]
    else:
        xs, ys = [], []
        for pair in points.split():
            x, y = pair.split(",")
            xs.append(float(x))
            ys.append(float(y))
        tx, ty = sum(xs) / len(xs), sum(ys) / len(ys)
    text = (
        '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" '
        'font-size="9" font-family="Segoe UI, Source Sans 3, sans-serif" fill="#1c1714">%s</text>'
        % (tx, ty + 0.5, escape(short.replace("hujra_", "7·").replace("muleteer_", "9·").replace("stables_", "8·").replace("latrine_", "10·")))
    )
    # shorter on-plan labels: Coste number + bay
    shown = loc if loc else short
    if len(shown) > 18:
        shown = shown[:16] + "…"
    text = (
        '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" '
        'font-size="8.5" font-family="Segoe UI, Source Sans 3, sans-serif" fill="#1c1714">%s</text>'
        % (tx, ty, escape(shown))
    )
    return (
        '<a href="%s"><g %s>%s%s%s%s</g></a>\n'
        % (escape(href), common, inner_title, shape, text, extra)
    )


def build_svg(g: Graph) -> str:
    parts: list[str] = []
    parts.append(
        '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"
     aria-labelledby="title desc">
<title id="title">Amin-Abad instance plan — each shape is a KG individual</title>
<desc id="desc">Schematic octagon generated from data/amin-abad-coste.ttl.
Group ids match RDF local names. Click a room to open its w3id IRI.
Example: wd_Q5907540_hujra_nw_2.</desc>
<style>
  .inst {{ cursor: pointer; }}
  .inst:hover polygon, .inst:hover circle {{ stroke: #9c4328; stroke-width: 3; }}
  .inst.selected polygon, .inst.selected circle {{ stroke: #9c4328; stroke-width: 3.5; fill-opacity: 1; }}
  .candidate {{ cursor: pointer; }}
  .candidate:hover polygon {{ stroke-width: 2.4; }}
  .candidate.selected polygon {{ stroke-width: 2.6; fill: rgba(156,67,40,0.08); }}
  a {{ text-decoration: none; }}
  text {{ pointer-events: none; }}
</style>
<rect width="100%" height="100%" fill="#f7f1e8"/>
<text x="520" y="36" text-anchor="middle" font-size="22" font-weight="700"
      font-family="Georgia, Source Serif 4, serif" fill="#1c1714">Amin-Abad — instance plan from BOT RDF</text>
<text x="520" y="58" text-anchor="middle" font-size="12"
      font-family="Segoe UI, sans-serif" fill="#5c534c">Coste PL. LXVI · :wd_Q5907540 · hover a room for its IRI · north at top</text>
'''.format(
            w=W, h=H
        )
    )

    # Envelope (no IRI — building already has the plate)
    parts.append(
        '<polygon points="%s" fill="none" stroke="#1c1714" stroke-width="2.4"/>\n'
        % octagon_pts(R_OUTER * R)
    )

    # Sahn 5
    parts.append(
        g_el(
            "wd_Q5907540_sahn",
            "5",
            octagon_pts(R_SAHN * R),
            g,
        )
    )
    # Prayer 6
    parts.append(
        g_el(
            "wd_Q5907540_prayer_platform",
            "6",
            octagon_pts(R_PRAYER * R),
            g,
        )
    )

    # --- Hujras on cardinal inner rings ---
    # North inner: n_1, n_2, n_3 west→east along N face (t from NNW=0 to NNE=1 in our face_point
    # face n is v1 NNE → v2 NNW, so t=0 is east, t=1 is west. Reverse for west→east.
    def bins(n: int):
        return [(i / n, (i + 1) / n) for i in range(n)]

    # N face: t=0 at NNE (east), t=1 at NNW (west). n_1 west = high t.
    n_ts = [(1 - (i + 1) / 3, 1 - i / 3) for i in range(3)]  # n_1, n_2, n_3
    for local, (t0, t1) in zip(
        ["wd_Q5907540_hujra_n_1", "wd_Q5907540_hujra_n_2", "wd_Q5907540_hujra_n_3"],
        n_ts,
    ):
        parts.append(g_el(local, "7", ring_poly("n", t0, t1, R_SAHN, R_HUJRA), g))

    # E face: v7 ESE → v0 ENE, t=0 south, t=1 north. e_1 north = high t.
    e_ts = [(1 - (i + 1) / 3, 1 - i / 3) for i in range(3)]
    for local, (t0, t1) in zip(
        ["wd_Q5907540_hujra_e_1", "wd_Q5907540_hujra_e_2", "wd_Q5907540_hujra_e_3"],
        e_ts,
    ):
        parts.append(g_el(local, "7", ring_poly("e", t0, t1, R_SAHN, R_HUJRA), g))

    # W face: v3 WNW → v4 WSW, t=0 north, t=1 south. w_1 north = low t.
    w_ts = bins(3)
    for local, (t0, t1) in zip(
        ["wd_Q5907540_hujra_w_1", "wd_Q5907540_hujra_w_2", "wd_Q5907540_hujra_w_3"],
        w_ts,
    ):
        parts.append(g_el(local, "7", ring_poly("w", t0, t1, R_SAHN, R_HUJRA), g))

    # S face: v5 SSW → v6 SSE, t=0 west, t=1 east. Leave center third for porch.
    parts.append(g_el("wd_Q5907540_hujra_s_w", "7", ring_poly("s", 0.00, 0.28, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_s_e", "7", ring_poly("s", 0.72, 1.00, R_SAHN, R_HUJRA), g))

    # NW diagonal inner hujras: face nw v2 NNW → v3 WNW, t=0 north, t=1 west.
    # nw_n circular at N end, nw_1..3, nw_w circular at W end.
    parts.append(g_el("wd_Q5907540_hujra_nw_n", "7", ring_poly("nw", 0.00, 0.18, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_nw_1", "7", ring_poly("nw", 0.18, 0.39, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_nw_2", "7", ring_poly("nw", 0.39, 0.61, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_nw_3", "7", ring_poly("nw", 0.61, 0.82, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_nw_w", "7", ring_poly("nw", 0.82, 1.00, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_hujra_ne_n", "7", ring_poly("ne", 0.82, 1.00, R_SAHN, R_HUJRA), g))

    # Domed hujras: mid-ring on cardinal axes
    def axis_circle(deg: float, rfrac: float, rad: float = 18.0):
        return polar(deg, rfrac * R) + (rad,)

    parts.append(
        g_el(
            "wd_Q5907540_hujra_n_dome",
            "7",
            "",
            g,
            kind="circle",
            circle=axis_circle(90, (R_HUJRA + R_STABLE) / 2, 20),
        )
    )
    parts.append(
        g_el(
            "wd_Q5907540_hujra_e_dome",
            "7",
            "",
            g,
            kind="circle",
            circle=axis_circle(0, (R_HUJRA + R_STABLE) / 2, 20),
        )
    )
    parts.append(
        g_el(
            "wd_Q5907540_hujra_w_dome",
            "7",
            "",
            g,
            kind="circle",
            circle=axis_circle(180, (R_HUJRA + R_STABLE) / 2, 20),
        )
    )

    # Stables on four diagonals
    for face, local in (
        ("nw", "wd_Q5907540_stables_nw"),
        ("ne", "wd_Q5907540_stables_ne"),
        ("se", "wd_Q5907540_stables_se"),
        ("sw", "wd_Q5907540_stables_sw"),
    ):
        parts.append(g_el(local, "8", ring_poly(face, 0.08, 0.92, R_HUJRA, R_STABLE), g))

    # Muleteers: north outer, west outer, NW outer 5 bays
    parts.append(g_el("wd_Q5907540_muleteer_n_w", "9", ring_poly("n", 0.52, 0.92, R_STABLE, R_OUTER), g))
    parts.append(g_el("wd_Q5907540_muleteer_n_e", "9", ring_poly("n", 0.08, 0.48, R_STABLE, R_OUTER), g))
    parts.append(g_el("wd_Q5907540_muleteer_w_1", "9", ring_poly("w", 0.00, 0.28, R_STABLE, R_OUTER), g))
    parts.append(g_el("wd_Q5907540_muleteer_w_2", "9", ring_poly("w", 0.28, 0.55, R_STABLE, R_OUTER), g))
    for local, (t0, t1) in zip(
        [
            "wd_Q5907540_muleteer_nw_1",
            "wd_Q5907540_muleteer_nw_2",
            "wd_Q5907540_muleteer_nw_3",
            "wd_Q5907540_muleteer_nw_4",
            "wd_Q5907540_muleteer_nw_5",
        ],
        # bay 1 at WNW (t=1) … bay 5 at NNW (t=0): reverse
        [(1 - (i + 1) / 5, 1 - i / 5) for i in range(5)],
    ):
        parts.append(g_el(local, "9", ring_poly("nw", t0, t1, R_STABLE, R_OUTER), g))

    # Presentation-only census: unlabelled outer 9s on NE / E / SE / SW.
    # Not minted — Coste prints 9 only on west and north.
    def candidate(cid: str, face: str, t0: float, t1: float, locator: str) -> str:
        pts = ring_poly(face, t0, t1, R_STABLE, R_OUTER)
        xs, ys = [], []
        for pair in pts.split():
            x, y = pair.split(",")
            xs.append(float(x))
            ys.append(float(y))
        tx, ty = sum(xs) / len(xs), sum(ys) / len(ys)
        return (
            '<g id="%s" class="candidate coste-9" data-iri="" data-coste="9" '
            'data-locator="%s" data-label="Unlabelled outer room (census only)" '
            'data-nbr="" data-grain="candidate">'
            "<title>%s — closed outer room, numeral 9 not printed</title>"
            '<polygon points="%s" fill="none" stroke="#9c4328" stroke-width="1.1" '
            'stroke-dasharray="5 3.5"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="middle" '
            'font-size="7" font-family="Segoe UI, sans-serif" fill="#9c4328">%s</text>'
            "</g>\n" % (cid, locator, cid, pts, tx, ty, locator)
        )

    for i, (t0, t1) in enumerate([(1 - (k + 1) / 5, 1 - k / 5) for k in range(5)], start=1):
        parts.append(candidate("candidate_muleteer_ne_%d" % i, "ne", t0, t1, "9?; NE; bay %d" % i))
        parts.append(candidate("candidate_muleteer_se_%d" % i, "se", t0, t1, "9?; SE; bay %d" % i))
        parts.append(candidate("candidate_muleteer_sw_%d" % i, "sw", t0, t1, "9?; SW; bay %d" % i))
    parts.append(candidate("candidate_muleteer_e_n", "e", 0.55, 0.92, "9?; E; N"))
    parts.append(candidate("candidate_muleteer_e_s", "e", 0.08, 0.45, "9?; E; S"))

    # South entrance stack on S face, outer rings
    parts.append(g_el("wd_Q5907540_porch", "2", ring_poly("s", 0.32, 0.68, R_SAHN, R_HUJRA), g))
    parts.append(g_el("wd_Q5907540_entrance", "1", ring_poly("s", 0.34, 0.66, R_STABLE, R_OUTER), g))
    parts.append(g_el("wd_Q5907540_concierge_w", "3", ring_poly("s", 0.05, 0.32, R_HUJRA, R_STABLE), g))
    parts.append(g_el("wd_Q5907540_concierge_e", "3", ring_poly("s", 0.68, 0.95, R_HUJRA, R_STABLE), g))
    # stairs as small bars
    sw = face_point("s", 0.30, (R_HUJRA + R_STABLE) / 2 * R)
    se = face_point("s", 0.70, (R_HUJRA + R_STABLE) / 2 * R)
    parts.append(
        g_el("wd_Q5907540_stairs_w", "4", "", g, kind="circle", circle=(sw[0], sw[1], 9))
    )
    parts.append(
        g_el("wd_Q5907540_stairs_e", "4", "", g, kind="circle", circle=(se[0], se[1], 9))
    )

    # Towers + latrines
    for name, idx in TOWER_AT.items():
        x, y = polar(VERT_DEG[idx], R_TOWER * R)
        parts.append(
            g_el(
                "wd_Q5907540_tower_%s" % name,
                "tower",
                "",
                g,
                kind="circle",
                circle=(x, y, 16),
            )
        )
    for name, idx in (
        ("nnw", 2),
        ("wnw", 3),
        ("wsw", 4),
        ("ssw", 5),
    ):
        x, y = polar(VERT_DEG[idx], R_TOWER * R)
        parts.append(
            g_el(
                "wd_Q5907540_latrine_%s" % name,
                "10",
                "",
                g,
                kind="circle",
                circle=(x, y, 8),
            )
        )

    # Basin 11 south of entrance
    bx, by = CX, CY + R_OUTER * R + 70
    parts.append(
        g_el(
            "wd_Q5907540_basin",
            "11",
            "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f"
            % (bx - 36, by - 28, bx + 36, by - 28, bx + 36, by + 28, bx - 36, by + 28),
            g,
        )
    )

    # North arrow
    parts.append(
        '<g transform="translate(520,92)" fill="#1c1714">'
        '<polygon points="0,-14 6,4 -6,4"/>'
        '<text y="18" text-anchor="middle" font-size="11">N</text></g>\n'
    )

    # Legend
    legend = [
        ("7 hujra", FILL["7"]),
        ("8 stables", FILL["8"]),
        ("9 muleteer", FILL["9"]),
        ("10 latrine", FILL["10"]),
        ("1–3 entrance", FILL["1"]),
        ("5 sahn / 6 estrade", FILL["5"]),
        ("11 basin", FILL["11"]),
        ("tower", FILL["tower"]),
    ]
    y = 1080
    x = 70
    parts.append('<g font-size="11" font-family="Segoe UI, sans-serif" fill="#1c1714">\n')
    for lab, col in legend:
        parts.append(
            '<rect x="%.0f" y="%.0f" width="14" height="14" fill="%s" stroke="#1c1714"/>'
            '<text x="%.0f" y="%.0f">%s</text>\n'
            % (x, y, col, x + 20, y + 12, escape(lab))
        )
        x += 120
    parts.append("</g>\n")
    parts.append(
        '<text x="520" y="1164" text-anchor="middle" font-size="10" fill="#5c534c" '
        'font-family="Segoe UI, sans-serif">Fragment IRI: …/amin-abad-instances.svg#wd_Q5907540_hujra_nw_2'
        " · generated from data/amin-abad-coste.ttl</text>\n"
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
  <title>Amin-Abad — instance plan (BOT RDF → SVG)</title>
  <style>
    :root { --ink:#1c1714; --muted:#5c534c; --paper:#f7f1e8; --card:#fffdf8; --hit:#9c4328; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:"Segoe UI", "Source Sans 3", sans-serif; background:var(--paper); color:var(--ink); }
    header { padding:20px 28px 8px; border-bottom:3px solid var(--ink); }
    header h1 { font-family: Georgia, serif; font-size:26px; margin:0 0 6px; }
    header p { margin:0; color:var(--muted); }
    .wrap { display:grid; grid-template-columns: 1fr 340px; min-height: calc(100vh - 88px); }
    .stage { padding:8px; overflow:auto; }
    .stage svg { width:100%; height:auto; max-height:calc(100vh - 110px); }
    .inst.selected polygon, .inst.selected circle { stroke:#9c4328; stroke-width:3.5; }
    aside { background:var(--card); border-left:1px solid #d4c7b8; padding:18px 20px; }
    aside h2 { font-size:13px; letter-spacing:.14em; text-transform:uppercase; color:var(--hit); margin:0 0 10px; }
    #iri { font-family: Consolas, "Courier New", monospace; font-size:12px; word-break:break-all; background:#f0e6d8; padding:8px; }
    #meta dt { color:var(--muted); font-size:12px; margin-top:10px; }
    #meta dd { margin:2px 0 0; font-size:14px; }
    #nbr a { display:block; font-size:12px; color:var(--hit); }
    .hint { font-size:13px; color:var(--muted); margin-top:16px; }
  </style>
</head>
<body>
  <header>
    <h1>Amin-Abad instance plan</h1>
    <p>Each solid shape is one RDF individual from <code>data/amin-abad-coste.ttl</code>. Dashed outlines are unlabelled closed rooms on the plate (Coste 9 on NE/E/SE/SW) and are not minted until HITL review.</p>
  </header>
  <div class="wrap">
    <div class="stage" id="plan">
      SVG_INLINE
    </div>
    <aside>
      <h2>Selected instance</h2>
      <div id="iri">https://w3id.org/persian-caravanserai-kg#wd_Q5907540_hujra_nw_2</div>
      <dl id="meta">
        <dt>Label</dt><dd id="lab">Hujra, NW diagonal inner bay 2</dd>
        <dt>Coste locator</dt><dd id="loc">7; NW; bay 2 north-east to south-west</dd>
        <dt>Legend key</dt><dd id="coste">7</dd>
        <dt>BOT neighbours</dt><dd id="nbr"></dd>
      </dl>
      <p class="hint">Deep link: <code>amin-abad-instances.svg#wd_Q5907540_hujra_nw_2</code></p>
    </aside>
  </div>
  <script>
    const iriEl = document.getElementById('iri');
    const labEl = document.getElementById('lab');
    const locEl = document.getElementById('loc');
    const costeEl = document.getElementById('coste');
    const nbrEl = document.getElementById('nbr');
    function show(g) {
      document.querySelectorAll('.inst.selected, .candidate.selected').forEach(n => n.classList.remove('selected'));
      g.classList.add('selected');
      iriEl.textContent = g.getAttribute('data-iri') || '(not in RDF — census candidate)';
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
      const hash = (location.hash || '#wd_Q5907540_hujra_nw_2').slice(1);
      const start = doc.getElementById(hash) || doc.getElementById('wd_Q5907540_hujra_nw_2');
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
