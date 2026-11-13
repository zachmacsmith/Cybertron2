"""Review 38.69: maps of the designed worlds (design.py), one PNG each. Positions are the design's (a presentation of the intended
layout, not generated land); road times are the straight distance at a day's road per 17 km, x1.5 over hills."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import design as D

PEOPLE = {"A": "#d1495b", "B": "#2a78d6", "C": "#e3a21a"}
RES = {"seam": "Cu", "quarry": "St", "salt": "Sa", "fish": "Fi", "game": "Gm", "wood": "Ti", "grass": "Gr", "mill site": "Mill"}


def fmt(h):
    return f"{h:.0f}h" if h < 7.5 else f"{h / 8:.1f}d"


def draw(key, w):
    W_, H_ = w["size"]
    fig, ax = plt.subplots(figsize=(min(19, 8 + W_ / 7), min(13, 3 + H_ / 7)))
    pl = {p["name"]: p for p in w["places"]}
    import numpy as np
    for kind, pts in D.FEATURES.get(key, []):
        if pts == "ring":
            t = np.linspace(0, 2 * np.pi, 200)
            xs, ys = 42 + 22 * np.cos(t), 42 + 22 * np.sin(t)
        else:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        sty = {"ridge": dict(color="#b8a88a", lw=9, alpha=0.35, solid_capstyle="round"),
               "river": dict(color="#5d9cd6", lw=2.2, alpha=0.7),
               "coast": dict(color="#5d9cd6", lw=7, alpha=0.3)}[kind]
        ax.plot(xs, ys, zorder=0, **sty)
    for a, b in w["roads"]:
        pa, pb = pl[a], pl[b]
        hill = (a, b) in w["hills"] or (b, a) in w["hills"]
        ax.plot([pa["x"], pb["x"]], [pa["y"], pb["y"]], color="#8a7a66", lw=1.6, ls=(0, (4, 3)) if hill else "-", zorder=1)
        ax.text((pa["x"] + pb["x"]) / 2, (pa["y"] + pb["y"]) / 2, fmt(D.hours(w, a, b)), fontsize=7, color="#5a4a3a", ha="center",
                va="center", zorder=2, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    for p in w["places"]:
        col = D.LAND[p["land"]][1]
        if p["kind"] == "stop":
            ax.scatter(p["x"], p["y"], s=40, marker="s", color="#bbbbbb", edgecolor="#666", zorder=3)
            ax.text(p["x"], p["y"] - 1.8, p["name"], fontsize=6.5, color="#666", ha="center", va="top", zorder=4)
            continue
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
        ax.text(p["x"], p["y"] - 2.4, p["name"], fontsize=8.5, weight="bold" if (home or p["value"] == 2) else "normal",
                ha="center", va="top", zorder=4)
        if res:
            ax.text(p["x"], p["y"] - 4.4, res, fontsize=7, color="#444", ha="center", va="top", zorder=4)
    ax.set_xlim(-6, W_ + 6); ax.set_ylim(-8, H_ + 6); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#ccc")
    lands = sorted({p["land"] for p in w["places"] if p["kind"] != "stop"})
    h1 = [Patch(color=D.LAND[l][1], label=f"{l}:\n  {', '.join(D.LAND[l][0])}") for l in lands]
    h2 = [Line2D([], [], marker="o", ls="", ms=11, mfc="white", mec=PEOPLE[x], mew=3, label=f"people {x}: starting village") for x in w["peoples"]]
    h2 += [Line2D([], [], marker="o", ls="", ms=10, mfc="white", mec="#c8a000", mew=2.5, label="high value (contested by design)"),
           Line2D([], [], marker="s", ls="", ms=6, mfc="#bbb", mec="#666", label="stopping place"),
           Line2D([], [], color="#8a7a66", ls=(0, (4, 3)), label="hill road (x1.5 time)"),
           Line2D([], [], color="#b8a88a", lw=8, alpha=0.35, label="ridge"), Line2D([], [], color="#5d9cd6", lw=2, label="river"),
           Line2D([], [], color="#5d9cd6", lw=6, alpha=0.3, label="coast")]
    leg = ax.legend(handles=h1 + h2, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8,
                    title="Circle size: soil (rich, fair, poor)\nCu copper seam  St stone  Sa salt  Fi fish\nGm game  Ti timber  Gr grazing  Mill mill site",
                    title_fontsize=8)
    leg._legend_box.align = "left"
    ax.set_title(w["title"], loc="left", fontsize=12)
    import textwrap
    fig.text(0.01, 0.01, textwrap.fill(w["summary"], 150), fontsize=8, va="bottom", ha="left", color="#333")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(f"{key}.png", dpi=130)
    plt.close(fig)


for k, w in D.WORLDS.items():
    draw(k, w)
print("ok")
