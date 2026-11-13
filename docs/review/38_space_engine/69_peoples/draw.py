"""Review 38.69: maps of the designed worlds (design.py), one PNG each. Positions are the design's fitted targets (km), roads in whole
days as designed; ridges, rivers and coasts are drawn through the places they are designed to pass. A presentation of the design, not
generated land."""
import math, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Circle
import design as D

PEOPLE = {"A": "#d1495b", "B": "#2a78d6", "C": "#e3a21a"}
RES = {"seam": "Cu", "quarry": "St", "salt": "Sa", "fish": "Fi", "game": "Gm", "wood": "Ti", "grass": "Gr", "mill site": "Mill"}


def draw(key, w):
    S = w["size_km"]
    fig, ax = plt.subplots(figsize=(15, 11))
    pl = {p["name"]: p for p in w["places"]}
    xy = lambda n: (pl[n]["x"], pl[n]["y"])
    for f in D.FEATURES.get(key, []):
        kind, arg = f[0], f[1]
        if kind == "coast":
            side = {"south": ([0, S], [0, 0]), "west": ([0, 0], [0, S]), "east": ([S, S], [0, S]), "north": ([0, S], [S, S])}[arg]
            ax.plot(*side, color="#5d9cd6", lw=14, alpha=0.3, zorder=0)
        elif kind == "river":
            xs, ys = zip(*[xy(n) for n in arg])
            ax.plot(xs, ys, color="#5d9cd6", lw=2.5, alpha=0.6, zorder=0)
        elif kind in ("massif", "fen", "oldwood", "basin"):
            col = {"massif": "#b8a88a", "fen": "#7fb3a8", "oldwood": "#2a5a2a", "basin": "#8fc45a"}[kind]
            for n in arg:
                ax.add_patch(Circle(xy(n), 9 if kind != "basin" else 12, color=col, alpha=0.18, zorder=0, lw=0))
        elif kind == "ridge":
            (x1, y1), (x2, y2) = xy(arg[0]), xy(arg[1])
            k = 1 - (f[2].get("stop_short", 0) if len(f) > 2 else 0)
            ax.plot([x1, x1 + (x2 - x1) * k], [y1, y1 + (y2 - y1) * k], color="#b8a88a", lw=12, alpha=0.4, zorder=0, solid_capstyle="round")
        elif kind == "ring":
            cx, cy = xy("The Mere")
            r = sum(math.dist(xy(n), (cx, cy)) for n in arg) / len(arg)
            ax.add_patch(Circle((cx, cy), r, fill=False, ec="#b8a88a", lw=12, alpha=0.4, zorder=0))
    for a, b, days, hill in w["roads"]:
        (x1, y1), (x2, y2) = xy(a), xy(b)
        ax.plot([x1, x2], [y1, y2], color="#8a7a66", lw=1.8, ls=(0, (4, 3)) if hill else "-", zorder=1)
        for k in range(1, days):                                            # the stopping places a road of 2 or more days will have
            t = k / days
            ax.scatter(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, s=22, marker="s", color="#bbb", edgecolor="#666", zorder=2)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{days}d", fontsize=8, color="#4a3a2a", ha="center", va="center", zorder=2,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    for p in w["places"]:
        col = D.LAND[p["land"]][1]
        size = {"rich": 520, "fair": 400, "poor": 300}[p["soil"]]
        home = p["kind"].startswith("home:")
        ec, lw = ("#222", 1.0)
        if home:
            ec, lw = PEOPLE[p["kind"].split(":")[1]], 4.5
        elif p["value"] == 2:
            ec, lw = "#c8a000", 3.0
        ax.scatter(p["x"], p["y"], s=size * (1.5 if home else 1), color=col, edgecolor=ec, linewidth=lw, zorder=3)
        if home:
            ax.text(p["x"], p["y"], p["kind"].split(":")[1], fontsize=12, weight="bold", color=PEOPLE[p["kind"].split(":")[1]],
                    ha="center", va="center", zorder=5)
        res = " ".join(RES[r] for r in p["res"] if r in RES)
        ax.text(p["x"], p["y"] - 3.2, p["name"], fontsize=9, weight="bold" if (home or p["value"] == 2) else "normal",
                ha="center", va="top", zorder=4)
        if res:
            ax.text(p["x"], p["y"] - 5.6, res, fontsize=7.5, color="#444", ha="center", va="top", zorder=4)
    ax.set_xlim(0, S); ax.set_ylim(-4, S); ax.set_aspect("equal")
    ax.set_xticks([0, S / 2, S]); ax.set_yticks([0, S / 2, S]); ax.tick_params(labelsize=7)
    ax.set_xlabel("km", fontsize=8)
    for s in ax.spines.values():
        s.set_color("#ccc")
    lands = sorted({p["land"] for p in w["places"]})
    h1 = [Patch(color=D.LAND[l][1], label=f"{l}:\n  {', '.join(D.LAND[l][0])}") for l in lands]
    h2 = [Line2D([], [], marker="o", ls="", ms=11, mfc="white", mec=PEOPLE[x], mew=3, label=f"people {x}: starting village") for x in w["peoples"]]
    h2 += [Line2D([], [], marker="o", ls="", ms=10, mfc="white", mec="#c8a000", mew=2.5, label="high value (contested by design)"),
           Line2D([], [], color="#8a7a66", label="road, in whole days"), Line2D([], [], color="#8a7a66", ls=(0, (4, 3)), label="hill road"),
           Line2D([], [], marker="s", ls="", ms=5, mfc="#bbb", mec="#666", label="a night's stopping place"),
           Line2D([], [], color="#b8a88a", lw=8, alpha=0.4, label="hills, ridge"), Line2D([], [], color="#5d9cd6", lw=2, label="river"),
           Line2D([], [], color="#5d9cd6", lw=8, alpha=0.3, label="sea")]
    leg = ax.legend(handles=h1 + h2, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8,
                    title="Circle size: soil (rich, fair, poor)\nCu copper seam  St stone  Sa salt  Fi fish\nGm game  Ti timber  Gr grazing  Mill mill site",
                    title_fontsize=8)
    leg._legend_box.align = "left"
    ax.set_title(w["title"], loc="left", fontsize=12)
    fig.text(0.01, 0.01, textwrap.fill(w["summary"], 160), fontsize=8.5, va="bottom", ha="left", color="#333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(f"{key}.png", dpi=120)
    plt.close(fig)


for k, w in D.WORLDS.items():
    draw(k, w)
print("ok")
