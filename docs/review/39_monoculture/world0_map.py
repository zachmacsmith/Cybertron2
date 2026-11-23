"""World 0 (monoculture_five_worlds.md §1a): the runs world's land as the engine holds it, with World 0's design laid over it.

Drawn from `cybertron2/specs/water/runs.yaml`, the generated world the World 0 maker would start from:
- **the land between places** is the wild layer's areas (`wild.land.areas`): each home, ring and block tile is shaded by its
  largest cover, at the coarse resolution the engine keeps (homes and 2.5 km rings round each place, blocks beyond);
- **rivers** are the areas' drainage (`wild.land.down`) where an area carries river, the line's width by its river km; **lakes**
  are `wild.land.waters`;
- **each place** is a ring of its parcels' covers, by parcel size; its resources are read from its parcels' states (fish, brine,
  quarry, seam, game, wood) and its buildings from `buildings`;
- **roads** are the world's roads, in whole days.

Presentation choices (not held by the engine): a place's ring sits at its node's `xy`; tiles are squares of the area's km2 at its
`xy_km`; rivers are straight segments between area centres. World 0's overlay (households, who holds what, what is unexplored, the
capital the maker would add) is the design's, labelled as such.

    python3 docs/review/39_monoculture/world0_map.py
"""
import math
import os
import textwrap

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle, Wedge  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(ROOT, "cybertron2", "specs", "water", "runs.yaml")

COVER = {  # the engine's covers; colours follow the peoples maps (69_peoples/design.py LAND)
    "field": "#c9d98a", "meadow": "#8fc45a", "pasture": "#b3c98a", "scrub": "#9aae6e", "forest": "#3f7a3a", "fen": "#7fb3a8",
    "water": "#6aa3d6", "heath": "#c8a3c8", "moor": "#a68aa0", "rock": "#9a8f80", "built": "#b9a58c", "saltmarsh": "#9fc9d6",
}
GROUP = {"fishing": "#2a78d6", "farming": "#eb6834"}            # categorical slots 1 and 2 (validated)
RES = [("fish", "Fi fish"), ("brine", "Sa brine spring"), ("quarry", "St stone"), ("seam", "Cu copper"), ("game", "Gm game"),
       ("wood", "Ti timber"), ("crop", "Cr crop standing")]

# ------------------------------------------------------------------ World 0's design (monoculture_five_worlds.md §1a)
W0 = {
    "Highpool": {"group": "fishing", "known": True, "who": [
        ("Brook (4)", "salter; fisher", "the Salt House and brine pan, salting tub, Brook's Forge"),
        ("Marsh (3)", "fisher: weir and nets, keeping", "the weir (wattle, to add), gill net, wicker traps, smokehouse (to add)")]},
    "Middleham": {"group": "farming", "known": True, "who": [
        ("Field (4)", "farmer: plough, seed and harvest; herder", "2 fields, ox pair and plough, the Field Byre, 4 cows and a bull"),
        ("Fletcher (3)", "miller; farmer", "Middleham Mill, oven, 1 field")]},
    "Lowstrand": {"note": "empty village: 3 houses, 2 fields"},
}
DROP = {"Shepherd", "Hart", "Wood", "Wright", "Cotter"}          # households the maker takes out (their houses stand empty)


def load():
    return yaml.safe_load(open(SRC))


def draw(w, out):
    fig, ax = plt.subplots(figsize=(15, 11))
    L = w["wild"]["land"]
    A = L["areas"]
    # the land between places: area tiles by largest cover
    for a in sorted(A.values(), key=lambda a: {"wild": 0, "ring": 1, "home": 2}[a["kind"]]):
        cov = a.get("cover") or {}
        if not cov:
            continue
        top = max(cov, key=cov.get)
        x, y = a["xy_km"]
        s = math.sqrt(float(a["km2"]))
        ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, color=COVER.get(top, "#ddd"), alpha=0.35 if a["kind"] == "wild" else 0.5,
                               lw=0, zorder=0))
    # rivers: drainage between areas that carry river
    for a_id, b_id in L["down"].items():
        a = A.get(a_id)
        b = A.get(b_id)
        if not a or not b:
            continue
        km = float(a.get("river_km") or 0) + 3 * float(a.get("big_river_km") or 0)
        if km <= 0:
            continue
        (x1, y1), (x2, y2) = a["xy_km"], b["xy_km"]
        ax.plot([x1, x2], [y1, y2], color="#3d7fc4", lw=min(0.6 + km * 0.35, 5), alpha=0.7, zorder=1, solid_capstyle="round")
    for body in L["waters"].values():
        if body["kind"] != "lake":
            continue
        for a_id, k2 in body["areas"].items():
            x, y = A[a_id]["xy_km"]
            ax.scatter(x, y, s=60 * float(k2), color=COVER["water"], alpha=0.8, edgecolor="#3d7fc4", zorder=1)
    # roads
    N = w["nodes"]
    for a, b, days, info in w["roads"]:
        (x1, y1), (x2, y2) = N[a]["xy"], N[b]["xy"]
        ax.plot([x1, x2], [y1, y2], color="#6b5a46", lw=1.6, zorder=2)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{days}d", fontsize=7.5, color="#4a3a2a", ha="center", va="center", zorder=2,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8))
    # places: a ring of parcel covers by size
    held = {b["parcel"].split("_")[0]: [] for b in w["buildings"].values()}
    for b in w["buildings"].values():
        if b.get("household") not in DROP:
            held[b["parcel"].split("_")[0]].append(b["name"])
    for n, d in N.items():
        x, y = d["xy"]
        sizes = {}
        res = set()
        for p in d["parcels"].values():
            sizes[p["cover"]] = sizes.get(p["cover"], 0) + p["size"]
            st = p.get("state") or {}
            res |= {k for k in st if k in dict(RES)}
            if p.get("spring") == "brine":
                res.add("brine")
            if p["cover"] == "water" and "fish" in st:
                res.add("fish")
        tot = sum(sizes.values())
        r = 2.1 if n in W0 and W0[n].get("known") else 1.6
        a0 = 90.0
        for cov, sz in sorted(sizes.items(), key=lambda kv: -kv[1]):
            span = 360.0 * sz / tot
            ax.add_patch(Wedge((x, y), r, a0, a0 + span, width=r * 0.55, color=COVER.get(cov, "#ddd"), ec="white", lw=1.2, zorder=4))
            a0 += span
        g = W0.get(n, {}).get("group")
        if g:
            ax.add_patch(plt.Circle((x, y), r + 0.35, fill=False, ec=GROUP[g], lw=4, zorder=5))
        else:
            ax.add_patch(plt.Circle((x, y), r + 0.25, fill=False, ec="#777", lw=1.3, ls=(0, (3, 2)), zorder=5))
        unexplored = not (W0.get(n) or {}).get("known")
        label = n + ("" if not unexplored else "  (unexplored)")
        ax.text(x, y - r - 0.8, label, fontsize=9.5 if g else 8.5, weight="bold" if g else "normal", ha="center", va="top", zorder=6)
        codes = " ".join(c.split()[0] for k, c in RES if k in res)
        sub = codes
        if W0.get(n, {}).get("note"):
            sub = (sub + "   " if sub else "") + W0[n]["note"]
        if sub:
            ax.text(x, y - r - 2.3, sub, fontsize=7.5, color="#444", ha="center", va="top", zorder=6)
        el = f"{int(d.get('elevation', 0))} m, {int(d.get('rain_mm', 0))} mm"
        ax.text(x, y + r + 0.6, el, fontsize=6.5, color="#777", ha="center", va="bottom", zorder=6)
    xs = [d["xy"][0] for d in N.values()] + [a["xy_km"][0] for a in A.values()]
    ys = [d["xy"][1] for d in N.values()] + [a["xy_km"][1] for a in A.values()]
    ax.set_xlim(min(xs) - 5, max(xs) + 5)
    ax.set_ylim(min(ys) - 6, max(ys) + 5)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7)
    ax.set_xlabel("km", fontsize=8)
    for s in ax.spines.values():
        s.set_color("#ccc")
    covers = [c for c in COVER if any(c in {p["cover"] for p in d["parcels"].values()} for d in N.values())]
    h = [Patch(color=COVER[c], label=c) for c in covers]
    h += [Line2D([], [], marker="o", ls="", ms=12, mfc="white", mec=GROUP["fishing"], mew=3, label="Highpool: the fishing village"),
          Line2D([], [], marker="o", ls="", ms=12, mfc="white", mec=GROUP["farming"], mew=3, label="Middleham: the farming village"),
          Line2D([], [], marker="o", ls="", ms=10, mfc="white", mec="#777", mew=1.3, label="unexplored at the start"),
          Line2D([], [], color="#6b5a46", lw=1.6, label="road, in whole days"),
          Line2D([], [], color="#3d7fc4", lw=3, label="river (width: river km)"),
          Patch(color="#9aae6e", alpha=0.35, label="land between places:\nthe wild layer's tiles, largest cover")]
    leg = ax.legend(handles=h, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8,
                    title="Ring: the place's parcels by cover and size\n" + "\n".join(c for _, c in RES), title_fontsize=8)
    leg._legend_box.align = "left"
    # the design's households
    lines = []
    for n in ("Highpool", "Middleham"):
        lines.append(f"{n} ({W0[n]['group']})")
        for hh, liv, cap in W0[n]["who"]:
            lines.append(f"  {hh}: {liv}")
            lines.append(textwrap.fill(cap, 52, initial_indent="     ", subsequent_indent="     "))
    fig.text(0.735, 0.50, "World 0's founders (the design: 14, one model)\n\n" + "\n".join(lines), fontsize=7.8, va="top", ha="left",
             family="DejaVu Sans", color="#222")
    ax.set_title("World 0: Highpool and Middleham, the first monoculture world (the runs world's land, seed 5)", loc="left", fontsize=12)
    fig.text(0.01, 0.01, textwrap.fill(
        "One river: the runs come up it in autumn. Highpool fishes and boils salt at the only brine spring; Middleham farms the only "
        "fields held and has the mill. Lowstrand, a day below Middleham, is an empty village. Everything but the two villages and the "
        "road between them is unexplored at the start. Land, covers, resources, rivers and roads are read from runs.yaml; the "
        "households and what is unexplored are World 0's design (monoculture_five_worlds.md §1a).", 170),
        fontsize=8.5, va="bottom", ha="left", color="#333")
    fig.tight_layout(rect=(0, 0.06, 0.73, 1))
    fig.savefig(out, dpi=120)
    plt.close(fig)


def flows(out):
    """World 0's dependencies: who holds which chokepoint, and what each flow carries (the design's table, drawn)."""
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    boxes = {"Highpool": (0.4, 1.0, GROUP["fishing"], ["Brook: salt house, brine pan, forge", "Marsh: weir, nets, traps, smokehouse",
                                                         "gives: salt, smoked and salted fish, mended tools",
                                                         "lacks: fields, oxen, a mill; grain between the runs"]),
             "Middleham": (8.2, 1.0, GROUP["farming"], ["Field: fields, ox team and plough, cattle, hay", "Fletcher: the mill, oven",
                                                         "gives: grain and flour, hides, oxen for carrying and clearing",
                                                         "lacks: salt; a fishery beyond the shallows; a forge"])}
    for n, (x, y, c, rows) in boxes.items():
        ax.add_patch(Rectangle((x, y), 4.4, 4.2, fc="white", ec=c, lw=3))
        ax.text(x + 0.2, y + 3.85, n, fontsize=13, weight="bold", va="top", color="#222")
        for i, t in enumerate(rows):
            ax.text(x + 0.2, y + 3.1 - i * 0.75, textwrap.fill(t, 46), fontsize=9, va="top", color="#333" if i > 1 else "#111")
    arrows = [("salt", 1), ("smoked and salted fish (the autumn glut)", 1), ("tools mended at the forge", 1),
              ("grain and flour (food between the runs)", -1), ("hides (rods: angling 1.5 a unit, by hand 0.6)", -1),
              ("oxen lent (carrying, clearing a plot)", -1)]
    for i, (t, d) in enumerate(arrows):
        y = 4.7 - i * 0.62
        x1, x2 = (4.9, 8.1) if d == 1 else (8.1, 4.9)
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#555"))
        ax.text(6.5, y + 0.08, t, fontsize=8.3, ha="center", va="bottom", color="#222")
    ax.text(6.5, 0.55, "a day's road; each link has a holder who can withhold it; no terms are seeded", fontsize=8.5, ha="center",
            color="#555", style="italic")
    ax.set_title("World 0's dependencies: the fishing village and the farming village (the design)", loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    w = load()
    draw(w, os.path.join(HERE, "world0_map.png"))
    flows(os.path.join(HERE, "world0_flows.png"))
    print("ok")
