"""Figures for a capacity report (D4-102), as SVG (no dependencies), drawn with c2viz's layouts.

The world has no coordinates: the region map places nodes by c2viz.layout.world_layout (from road days) and a node's parcels by
node_layout (from side, size and adjacency), both presentation choices, deterministic, as the map's own. Each figure shows only what
the report holds.

- bounds: people supported at each food level and fuel level, against the people there (log scale), a row a node and the region
- costs: each level's food a plot a year against food a unit of work, the mark's size its capital a head
- region: nodes coloured by people supported over people (diverging at 1), sized by people, roads with their days
- node: a node's parcels coloured by the food a year each gives at a level
- sensitivity: people supported at "worked" when one knob is set low or high
- frontier: people supported as land is taken outward from home, settled or carried home
"""
from __future__ import annotations

import html
import math
import os

SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
FOOD = {"bare": "#9ec5f4", "standing": "#5598e7", "worked": "#2a78d6", "best": "#1c5cab", "ceiling": "#0d366b"}
FUEL = {"gathered": "#f4b08f", "cut": "#eb6834", "managed": "#a8431c"}
WORDS = {"bare": "bare", "standing": "as it stands", "worked": "worked", "best": "best", "ceiling": "ceiling",
         "gathered": "dead wood", "cut": "+ young growth", "managed": "+ trees"}
CAT = ("#2a78d6", "#eb6834")
FONT = 'font-family="system-ui, -apple-system, Segoe UI, sans-serif"'


def _e(s):
    return html.escape(str(s))


def _t(x, y, s, size=12, fill=INK, anchor="start", weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT}>{_e(s)}</text>'


def _svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{_e(title)}</title>'
            f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>{body}</svg>')


def _mix(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def diverging(ratio):
    """Red under 1, grey at 1, blue over, on log2 of the ratio, clipped at 8x either way."""
    if ratio is None:
        return "#e1e0d9"
    if ratio <= 0:
        return "#e34948"
    v = max(-3.0, min(3.0, math.log2(ratio))) / 3
    return _mix("#f0efec", "#e34948", -v) if v < 0 else _mix("#f0efec", "#1c5cab", v)


def sequential(v, top):
    if not top or v <= 0:
        return "#f0efec"
    return _mix("#cde2fb", "#0d366b", min(1.0, math.sqrt(v / top)))


def nice(hi, n=4) -> list:
    """Round tick values from 0 to at least hi."""
    if hi <= 0:
        return [0, 1]
    raw = hi / n
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return [step * k for k in range(0, int(math.ceil(hi / step)) + 1)]


def _logx(v, lo, hi, x0, x1):
    v = max(v, lo)
    return x0 + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * (x1 - x0)


# ------------------------------------------------------------------------------------------------------------------- bounds
def bounds(report, title) -> str:
    rows = [(k, v) for k, v in report["nodes"].items() if k != "(region)" and (v["people"] or v["levels"].get("best", {}).get("supported", 0) >= 1)]
    rows.append(("(region)", report["nodes"]["(region)"]))
    allv = [x["supported"] for _, v in rows for x in v["levels"].values()] + [x["supported"] for _, v in rows for x in v["fuel"]["levels"].values()]
    allv += [v["people"] for _, v in rows]
    lo, hi = 0.1, 10 ** math.ceil(math.log10(max(allv + [10]) * 1.2))
    W, L, R, top, rh = 980, 190, 30, 96, 52
    H = top + rh * len(rows) + 50
    x0, x1 = L, W - R
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, "People supported for good at each level (log scale); the black bar is the people there.", 12, INK2)]
    lx = 16
    for k, c in FOOD.items():
        b.append(f'<circle cx="{lx + 6}" cy="68" r="6" fill="{c}" stroke="{SURFACE}" stroke-width="2"/>')
        b.append(_t(lx + 16, 72, WORDS[k], 12, INK2))
        lx += 26 + 7 * len(WORDS[k])
    lx += 10
    for k, c in FUEL.items():
        b.append(f'<path d="M{lx},74 l6,-11 l6,11 z" fill="{c}"/>')
        b.append(_t(lx + 16, 72, "fuel: " + WORDS[k] if k == "gathered" else WORDS[k], 12, INK2))
        lx += 30 + 7 * len(("fuel: " if k == "gathered" else "") + WORDS[k])
    ticks = [10 ** i for i in range(int(math.log10(lo)), int(math.log10(hi)) + 1)]
    for t in ticks:
        x = _logx(t, lo, hi, x0, x1)
        b.append(f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{top + rh * len(rows)}" stroke="{GRID}" stroke-width="1"/>')
        b.append(_t(x, top + rh * len(rows) + 18, f"{t:g}", 11, MUTED, "middle"))
    b.append(_t((x0 + x1) / 2, top + rh * len(rows) + 38, "people supported", 11, MUTED, "middle"))
    for i, (k, v) in enumerate(rows):
        y = top + i * rh + rh / 2 - 6
        name = "the whole region" if k == "(region)" else k
        b.append(_t(16, y + 4, name, 13, INK, weight=600 if k == "(region)" else 400))
        b.append(_t(16, y + 20, f"{v['people']} people", 11, INK2))
        b.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{AXIS}" stroke-width="1"/>')
        if v["people"]:
            xp = _logx(v["people"], lo, hi, x0, x1)
            b.append(f'<rect x="{xp - 1.5:.1f}" y="{y - 14}" width="3" height="34" rx="1.5" fill="{INK}"><title>{v["people"]} people</title></rect>')
        for lvl, x in v["levels"].items():
            xs = _logx(x["supported"], lo, hi, x0, x1)
            tip = f"{WORDS[lvl]}: {x['supported']:g} supported" + (f", {x['ratio']:g}x the people" if x["ratio"] is not None else "")
            b.append(f'<circle cx="{xs:.1f}" cy="{y}" r="6" fill="{FOOD[lvl]}" stroke="{SURFACE}" stroke-width="2"><title>{_e(tip)}</title></circle>')
        for lvl, x in v["fuel"]["levels"].items():
            xs = _logx(x["supported"], lo, hi, x0, x1)
            b.append(f'<path d="M{xs - 6:.1f},{y + 19} l6,-11 l6,11 z" fill="{FUEL[lvl]}"><title>{_e(WORDS[lvl])}: {x["supported"]:g} kept warm</title></path>')
    return _svg(W, H, "".join(b), title)


# ------------------------------------------------------------------------------------------------------------------- costs
def costs(report, title, node="(region)") -> str:
    rec = report["nodes"][node]
    pts = []
    for lvl, v in rec["levels"].items():
        a = v.get("at_supported") or {}
        fp, fu = (a.get("land") or {}).get("field_food_a_plot"), (a.get("recurring") or {}).get("food_a_unit")
        cap = (a.get("capital") or {}).get("with_materials_a_head")
        if fp and fu:
            pts.append((lvl, fp, fu, cap or 0.0, (a.get("recurring") or {}).get("a_head")))
    W, H, L, R, T, B = 860, 460, 70, 200, 70, 60
    if not pts:
        return _svg(W, 120, _t(16, 40, f"{title}: no fields at any level", 13), title)
    xs = [p[1] for p in pts]
    lo, hi = 10 ** math.floor(math.log10(min(xs))), 10 ** math.ceil(math.log10(max(xs)))
    ymax = max(p[2] for p in pts) * 1.25
    cmax = max(p[3] for p in pts) or 1.0
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, "Each level: food a plot of field a year (log) against food a unit of work; the mark's size is its capital a head.", 12, INK2)]
    for t in [10 ** i for i in range(int(math.log10(lo)), int(math.log10(hi)) + 1)]:
        x = _logx(t, lo, hi, L, W - R)
        b.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{H - B}" stroke="{GRID}"/>')
        b.append(_t(x, H - B + 18, f"{t:g}", 11, MUTED, "middle"))
    for k in range(0, 5):
        yv = ymax * k / 4
        y = H - B - (H - B - T) * k / 4
        b.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W - R}" y2="{y:.1f}" stroke="{GRID}"/>')
        b.append(_t(L - 8, y + 4, f"{yv:.1f}", 11, MUTED, "end"))
    b.append(_t((L + W - R) / 2, H - 16, "food a plot a year", 11, MUTED, "middle"))
    b.append(f'<text x="18" y="{(T + H - B) / 2}" font-size="11" fill="{MUTED}" transform="rotate(-90 18 {(T + H - B) / 2})" text-anchor="middle" {FONT}>food a unit of work</text>')
    for lvl, fp, fu, cap, ah in pts:
        x = _logx(fp, lo, hi, L, W - R)
        y = H - B - (H - B - T) * fu / ymax
        r = 6 + 14 * math.sqrt(cap / cmax)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{FOOD[lvl]}" fill-opacity="0.85" stroke="{SURFACE}" stroke-width="2">'
                 f'<title>{_e(WORDS[lvl])}: {fp:g} a plot, {fu:g} a unit, {ah} units a head a year, capital {cap:g} units a head</title></circle>')
        b.append(_t(x + r + 4, y + 4, f"{WORDS[lvl]}: capital {cap:.0f} units a head", 11, INK2))
    return _svg(W, H, "".join(b), title)


# ------------------------------------------------------------------------------------------------------------------- maps
def region(w, report, level, title) -> str:
    from c2viz import layout as LY
    pos = LY.world_layout(w.s["nodes"], w.s.get("roads") or {})
    W, H = 1000, 760
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, f"Each village: people supported at '{WORDS[level]}' over the people there (red short, grey even, blue spare); size: people.", 12, INK2)]
    oy = 60
    for r in (w.s.get("roads") or {}).values():
        if r.get("a") in pos and r.get("b") in pos:
            (ax, ay), (bx, by) = pos[r["a"]], pos[r["b"]]
            b.append(f'<line x1="{ax}" y1="{ay + oy}" x2="{bx}" y2="{by + oy}" stroke="{AXIS}" stroke-width="2"/>')
            b.append(_t((ax + bx) / 2, (ay + by) / 2 + oy - 4, f"{r.get('days', 1)} d", 10, MUTED, "middle"))
    for nid, (x, y) in pos.items():
        rec = report["nodes"].get(nid)
        if not rec:
            continue
        P = rec["people"]
        sup = rec["levels"][level]["supported"]
        ratio = sup / P if P else None
        r = 14 + 4 * math.sqrt(P)
        name = w.s["nodes"][nid].get("name", nid)
        b.append(f'<circle cx="{x}" cy="{y + oy}" r="{r:.1f}" fill="{diverging(ratio) if P else "#ffffff"}" stroke="{INK2}" stroke-width="1.5">'
                 f'<title>{_e(name)}: {P} people, {sup:g} supported</title></circle>')
        b.append(_t(x, y + oy + r + 14, name, 12, INK, "middle", 600))
        b.append(_t(x, y + oy + r + 28, f"{P} people, feeds {sup:g}", 11, INK2, "middle"))
    return _svg(W, H + oy, "".join(b), title)


def node(w, report, nid, level, title) -> str:
    from c2viz import layout as LY
    lay = LY.node_layout(nid, w.s["parcels"], w.s.get("roads") or {})
    by = report["nodes"][nid]["levels"][level].get("by_parcel") or {}
    top = max(by.values() or [1.0])
    W, H, oy = 1000, 700, 60
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, f"Food a year each parcel gives at '{WORDS[level]}' (darker: more). Cells are the map's presentation of the parcel graph.", 12, INK2)]
    for pid, poly in lay["cells"].items():
        v = by.get(pid, 0.0)
        pts = " ".join(f"{x:.1f},{y + oy:.1f}" for x, y in poly)
        par = w.s["parcels"][pid]
        b.append(f'<polygon points="{pts}" fill="{sequential(v, top)}" stroke="{SURFACE}" stroke-width="2"><title>{_e(par["name"])} ({par["cover"]}): {v:g} food a year</title></polygon>')
    for pid, (x, y) in lay["centre"].items():
        par = w.s["parcels"][pid]
        v = by.get(pid, 0.0)
        ink = "#ffffff" if v > 0.45 * top else INK
        b.append(_t(x, y + oy - 2, par["name"], 11, ink, "middle", 600))
        b.append(_t(x, y + oy + 12, f"{par['cover']}, {v:g}" if v else par["cover"], 10, ink, "middle"))
    return _svg(W, H + oy, "".join(b), title)


# ------------------------------------------------------------------------------------------------------------------- sensitivity
KNOBS = [("cook", "raw", "milled"), ("store", "open", "granary"), ("rotation", "once", "best"), ("broken", False, True),
         ("weed", 0.0, 16.0), ("tools", "bare", "copper"), ("herds", "none", "milk+offtake"), ("hunt", False, True),
         ("master", False, True), ("selection", False, True), ("manure", False, True), ("winter_crop", False, True)]


def sensitivity_data(w, nodes=None) -> dict:
    from dataclasses import replace
    from cybertron2.capacity import levels as LV, model as M
    base = LV.LEVELS["worked"]
    names = [n for k, v in M.homes_by_node(w).items() if nodes is None or k in nodes for n in v]
    m = M.mix(w, names) if names else M.mix(w)
    def P(lv):
        ctx = M.context(w, lv)
        return M.people_supported(ctx, M.lots(ctx, M.flows(ctx, nodes)), m)
    out = {"base": P(base), "knobs": []}
    for k, lo, hi in KNOBS:
        out["knobs"].append((k, lo, hi, P(replace(base, **{k: lo})), P(replace(base, **{k: hi}))))
    out["knobs"].sort(key=lambda x: -abs(x[4] - x[3]))
    return out


def sensitivity(data, title) -> str:
    rows = data["knobs"]
    W, L, R, T, rh = 900, 230, 60, 80, 30
    H = T + rh * len(rows) + 50
    vals = [data["base"]] + [x for r in rows for x in r[3:]]
    ticks = nice(max(vals) * 1.05 or 1.0)
    hi = ticks[-1]
    X = lambda v: L + (W - L - R) * v / hi
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, f"People supported at 'worked' ({data['base']:g}), with one setting lowered or raised.", 12, INK2)]
    b.append(f'<rect x="{L}" y="56" width="12" height="12" rx="3" fill="{CAT[1]}"/>' + _t(L + 18, 66, "lowered", 12, INK2))
    b.append(f'<rect x="{L + 90}" y="56" width="12" height="12" rx="3" fill="{CAT[0]}"/>' + _t(L + 108, 66, "raised", 12, INK2))
    xb = X(data["base"])
    for i, (k, lo, hi_, a, c) in enumerate(rows):
        y = T + i * rh + 8
        b.append(_t(L - 10, y + 13, f"{k} ({lo} / {hi_})", 12, INK, "end"))
        for v, col, lab in ((a, CAT[1], f"{lo}"), (c, CAT[0], f"{hi_}")):
            x0, x1 = sorted((xb, X(v)))
            if x1 - x0 < 1:
                continue
            b.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1 - x0:.1f}" height="18" rx="4" fill="{col}"><title>{_e(k)} = {_e(lab)}: {v:g}</title></rect>')
        b.append(_t(X(max(a, c, data["base"])) + 6, y + 13, f"{min(a, c):g} to {max(a, c):g}" if abs(a - c) > 1e-6 else "no effect here", 11, INK2))
    b.append(f'<line x1="{xb:.1f}" y1="{T - 4}" x2="{xb:.1f}" y2="{T + rh * len(rows)}" stroke="{INK}" stroke-width="2"/>')
    for v in ticks:
        b.append(_t(X(v), T + rh * len(rows) + 18, f"{v:g}", 11, MUTED, "middle"))
    b.append(_t((L + W - R) / 2, T + rh * len(rows) + 38, "people supported", 11, MUTED, "middle"))
    return _svg(W, H, "".join(b), title)


# ------------------------------------------------------------------------------------------------------------------- frontier
def frontier(fr, title) -> str:
    st = fr["steps"]
    W, H, L, R, T, B = 900, 440, 70, 170, 70, 80
    if not st:
        return _svg(W, 100, _t(16, 40, f"{title}: no nodes", 13), title)
    yt = nice(max(max(s["settle"], s["carry"]) for s in st) * 1.05 or 1.0)
    ymax = yt[-1]
    X = lambda i: L + (W - L - R) * (i / max(1, len(st) - 1))
    Y = lambda v: H - B - (H - B - T) * v / ymax
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, f"People supported at '{WORDS[fr['level']]}' as land is taken outward from {fr['home']}: settled where it lies, or its food carried home.", 12, INK2)]
    for v in yt:
        b.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - R}" y2="{Y(v):.1f}" stroke="{GRID}"/>' + _t(L - 8, Y(v) + 4, f"{v:g}", 11, MUTED, "end"))
    for i, s in enumerate(st):
        b.append(_t(X(i), H - B + 18, s["node"], 11, INK2, "middle"))
        b.append(_t(X(i), H - B + 32, f"{s['days']:g} d", 10, MUTED, "middle"))
    ys = {k: Y(st[-1][k]) for k in ("settle", "carry")}
    if abs(ys["settle"] - ys["carry"]) < 16:
        ys["settle"] -= 9
        ys["carry"] += 9
    for key, col, lab in (("settle", CAT[0], "settled"), ("carry", CAT[1], "carried home")):
        pts = " ".join(f"{X(i):.1f},{Y(s[key]):.1f}" for i, s in enumerate(st))
        b.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2"/>')
        for i, s in enumerate(st):
            b.append(f'<circle cx="{X(i):.1f}" cy="{Y(s[key]):.1f}" r="4.5" fill="{col}" stroke="{SURFACE}" stroke-width="2"><title>{lab}: {s[key]:g}</title></circle>')
        b.append(_t(X(len(st) - 1) + 10, ys[key] + 4, f"{lab} ({st[-1][key]:g})", 12, INK2))
    return _svg(W, H, "".join(b), title)


def to_png(svg_paths, scale=2) -> list:
    """Render SVG files to PNG beside them with the machine's Chromium (Node Playwright), if present."""
    import json as _json
    import subprocess
    import tempfile
    js = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const files = JSON.parse(process.argv[2]); const scale = Number(process.argv[3]);
  const b = await chromium.launch();
  for (const f of files) {
    const svg = fs.readFileSync(f, 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const w = m ? +m[1] : 1000, h = m ? +m[2] : 700;
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    await p.setContent('<html><body style="margin:0">' + svg + '</body></html>');
    await p.screenshot({ path: f.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: w, height: h } });
    await p.close();
  }
  await b.close();
})();
"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
    subprocess.run(["node", f.name, _json.dumps([os.path.abspath(p) for p in svg_paths]), str(scale)], check=True)
    return [p[:-4] + ".png" for p in svg_paths]


# ------------------------------------------------------------------------------------------------------------------- retrospective
def retro(rows, title) -> str:
    """Past runs: the worst-fed village's 'as it stands' ratio (log) against the share of the starting people who died of hunger;
    the mark's size is the run's length in days."""
    pts = [r for r in rows if r.get("worst") and r["worst"] > 0]
    W, H, L, R, T, B = 940, 520, 70, 40, 76, 70
    lo, hi = 0.02, 5.0
    X = lambda v: _logx(v, lo, hi, L, W - R)
    ymax = 1.0
    Y = lambda v: H - B - (H - B - T) * min(v, ymax) / ymax
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, "Each run: its worst-fed village's people supported 'as it stands' over the people there (log), against the share of "
                    "its starting people who died of hunger.", 12, INK2),
         _t(16, 62, "Size: days run. Red: the run reached a famine (a quarter or more died of hunger).", 12, INK2)]
    for t in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5):
        x = X(t)
        b.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{H - B}" stroke="{GRID if t != 1 else AXIS}" stroke-width="{1 if t != 1 else 2}"/>')
        b.append(_t(x, H - B + 18, f"{t:g}", 11, MUTED, "middle"))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        b.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - R}" y2="{Y(v):.1f}" stroke="{GRID}"/>' + _t(L - 8, Y(v) + 4, f"{v:.0%}", 11, MUTED, "end"))
    b.append(_t((L + W - R) / 2, H - 24, "worst village's ratio, as it stands (1 = feeds its people)", 11, MUTED, "middle"))
    placed = []
    for r in sorted(pts, key=lambda r: -r["days"]):
        x, y = X(r["worst"]), Y(r["hunger_share"])
        rad = 4 + 9 * math.sqrt(r["days"] / 80)
        col = "#e34948" if r["hunger_share"] >= 0.25 else "#2a78d6"
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{col}" fill-opacity="0.75" stroke="{SURFACE}" stroke-width="2">'
                 f'<title>{_e(r["run"])}: {r["days"]} days, {r["hunger"]} of {r["start"]} died of hunger; worst village {r["worst_node"]} '
                 f'{r["worst"]:g}; the region {r["region"]:g}</title></circle>')
        if r["label"] and all(abs(x - px) > 70 or abs(y - py) > 14 for px, py in placed):
            b.append(_t(x + rad + 3, y + 4, r["run"], 10, INK2))
            placed.append((x, y))
    return _svg(W, H, "".join(b), title)


# ------------------------------------------------------------------------------------------------------------------- ladder
def ladder(rungs, people, title) -> str:
    """The ladder of practice: each rung's change, the people fed after it, and its cost."""
    W, L, R, T, rh = 1000, 290, 260, 74, 28
    H = T + rh * len(rungs) + 40
    hi = nice(max(r["supported"] for r in rungs) * 1.05)[-1]
    X = lambda v: L + (W - L - R) * v / hi
    b = [_t(16, 26, title, 16, INK, weight=600),
         _t(16, 46, "From bare, one change at a time, each the most people fed for its cost. Right: ongoing work a head a year, and capital the step adds once.", 12, INK2),
         _t(16, 62, f"The black line is the {people} people there.", 12, INK2)]
    for i, r in enumerate(rungs):
        y = T + i * rh
        b.append(_t(L - 10, y + 15, r["change"], 12, INK, "end"))
        b.append(f'<rect x="{L}" y="{y + 4}" width="{max(2, X(r["supported"]) - L):.1f}" height="16" rx="4" fill="{FOOD["worked"]}">'
                 f'<title>{_e(r["change"])}: {r["supported"]:g} fed</title></rect>')
        b.append(_t(X(r["supported"]) + 6, y + 16, f"{r['supported']:g}", 11, INK2))
        cap = r.get("capital_added") or 0
        b.append(_t(W - R + 10, y + 16, f"{r['ongoing_a_head']} a head a year" + (f"; +{cap:g} once" if cap else ""), 11, MUTED))
    if people:
        x = X(people)
        b.append(f'<line x1="{x:.1f}" y1="{T}" x2="{x:.1f}" y2="{T + rh * len(rungs)}" stroke="{INK}" stroke-width="2"/>')
    for v in nice(hi):
        b.append(_t(X(v), T + rh * len(rungs) + 18, f"{v:g}", 11, MUTED, "middle"))
    return _svg(W, H, "".join(b), title)
