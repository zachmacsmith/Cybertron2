"""Maps of the five designed monoculture worlds (design.py), one PNG each, in the form of the peoples maps (38.69, 69_peoples/draw.py).
Positions are the design's fitted targets (km); roads in whole days as designed; rivers, coasts, hills, fens and old woods are drawn
through the places they are designed to pass. A presentation of the design, not generated land.

    cd docs/review/39_monoculture && python3 draw.py
"""
import math
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Circle, Patch  # noqa: E402

import design as D  # noqa: E402

GROUP = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a", "D": "#eda100"}      # categorical slots 1 to 4 (validated; labelled)
RES = {"seam": "Cu", "quarry": "St", "salt": "Sa", "fish": "Fi", "game": "Gm", "wood": "Ti", "grass": "Gr", "mill site": "Mill",
       "runs": "Run", "withies": "Wi"}
MARK = {"rumour": ("*", "#7a3db8", "a rumour line points here"), "herd": ("P", "#8a5a2b", "a feral herd, claimable")}


def draw(key, w):
    S = w["size_km"]
    fig, ax = plt.subplots(figsize=(15, 11))
    pl = {p["name"]: p for p in w["places"]}
    xy = lambda n: (pl[n]["x"], pl[n]["y"])  # noqa: E731
    for f in D.FEATURES.get(key, []):
        kind, arg = f[0], f[1]
        if kind == "coast":
            side = {"south": ([0, S], [0, 0]), "west": ([0, 0], [0, S]), "east": ([S, S], [0, S]), "north": ([0, S], [S, S])}[arg]
            X = max(p["x"] for p in w["places"]) + 8
            Y = max(p["y"] for p in w["places"]) + 8
            side = {"south": ([0, X], [0, 0]), "west": ([0, 0], [0, Y]), "east": ([X, X], [0, Y]), "north": ([0, X], [Y, Y])}[arg]
            ax.plot(*side, color="#5d9cd6", lw=14, alpha=0.3, zorder=0)
        elif kind == "river":
            xs, ys = zip(*[xy(n) for n in arg])
            ax.plot(xs, ys, color="#5d9cd6", lw=2.5, alpha=0.6, zorder=0)
        elif kind in ("massif", "fen", "oldwood"):
            col = {"massif": "#b8a88a", "fen": "#7fb3a8", "oldwood": "#2a5a2a"}[kind]
            for n in arg:
                ax.add_patch(Circle(xy(n), 9, color=col, alpha=0.18, zorder=0, lw=0))
    for a, b, days, hill in w["roads"]:
        (x1, y1), (x2, y2) = xy(a), xy(b)
        ax.plot([x1, x2], [y1, y2], color="#8a7a66", lw=1.8, ls=(0, (4, 3)) if hill else "-", zorder=1)
        for k in range(1, days):
            t = k / days
            ax.scatter(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, s=22, marker="s", color="#bbb", edgecolor="#666", zorder=2)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{days}d", fontsize=8, color="#4a3a2a", ha="center", va="center", zorder=2,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    for p in w["places"]:
        col = D.LAND[p["land"]][1]
        size = 160 + 70 * max(p["room"], 0)
        home = p["kind"].startswith("home:")
        g = p["kind"].split(":")[1] if home else None
        if home:
            ec, lw, ls = GROUP[g], 4.5, "-"
        elif p["known"]:
            ec, lw, ls = "#222", 1.6, "-"
        elif p["elders"]:
            ec, lw, ls = "#8a5a2b", 2.6, "-"
        else:
            ec, lw, ls = "#aaa", 1.0, "-"
        ax.scatter(p["x"], p["y"], s=size * (1.5 if home else 1), color=col, edgecolor=ec, linewidth=lw, zorder=3,
                   alpha=1.0 if (home or p["known"]) else 0.55)
        if home:
            ax.text(p["x"], p["y"], g, fontsize=12, weight="bold", color="#111", ha="center", va="center", zorder=5)
        if p["mark"]:
            m, c, _ = MARK[p["mark"]]
            ax.scatter(p["x"] + 2.6, p["y"] + 2.6, s=150, marker=m, color=c, edgecolor="white", linewidth=0.8, zorder=6)
        res = " ".join(RES[r] for r in p["res"] if r in RES)
        if p["room"]:
            res += f"  room {p['room']}"
        if p["soil"] != "fair":
            res += f"  {p['soil']}"
        ax.text(p["x"], p["y"] - 3.2, p["name"], fontsize=9, weight="bold" if home else "normal", ha="center", va="top", zorder=4)
        if res:
            ax.text(p["x"], p["y"] - 5.4, res, fontsize=7.2, color="#444", ha="center", va="top", zorder=4)
        if p["note"]:
            ax.text(p["x"], p["y"] - 7.3, p["note"], fontsize=6.8, color="#666", style="italic", ha="center", va="top", zorder=4)
    X = max(p["x"] for p in w["places"]) + 8
    Y = max(p["y"] for p in w["places"]) + 8
    ax.set_xlim(-2, X + 2)
    ax.set_ylim(-10, Y + 2)
    ax.set_aspect("equal")
    ax.set_xticks([0, round(X / 2), round(X)])
    ax.set_yticks([0, round(Y / 2), round(Y)])
    ax.tick_params(labelsize=7)
    ax.set_xlabel("km", fontsize=8)
    for s in ax.spines.values():
        s.set_color("#ccc")
    lands = sorted({p["land"] for p in w["places"]})
    h1 = [Patch(color=D.LAND[x][1], label=f"{x}:\n  {', '.join(D.LAND[x][0])}") for x in lands]
    h2 = [Line2D([], [], marker="o", ls="", ms=11, mfc="white", mec=GROUP[g], mew=3, label=textwrap.fill(f"{g}: {t}", 44))
          for g, t in w["groups"].items()]
    h2 += [Line2D([], [], marker="o", ls="", ms=10, mfc="white", mec="#222", mew=1.6, label="known at the start"),
           Line2D([], [], marker="o", ls="", ms=10, mfc="#ddd", mec="#aaa", mew=1.0, alpha=0.7, label="unexplored at the start (faded)")]
    if any(p["elders"] for p in w["places"]):
        h2.append(Line2D([], [], marker="o", ls="", ms=10, mfc="white", mec="#8a5a2b", mew=2.6, label="known only to the elders (faded)"))
    for k, (m, c, t) in MARK.items():
        if any(p["mark"] == k for p in w["places"]):
            h2.append(Line2D([], [], marker=m, ls="", ms=11, color=c, label=t))
    h2 += [Line2D([], [], color="#8a7a66", label="road, in whole days"), Line2D([], [], color="#8a7a66", ls=(0, (4, 3)), label="hill road"),
           Line2D([], [], marker="s", ls="", ms=5, mfc="#bbb", mec="#666", label="a night's stopping place"),
           Line2D([], [], color="#b8a88a", lw=8, alpha=0.4, label="hills, downs"), Line2D([], [], color="#5d9cd6", lw=2, label="river"),
           Line2D([], [], color="#5d9cd6", lw=8, alpha=0.3, label="sea")]
    leg = ax.legend(handles=h1 + h2, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8,
                    title="Circle size: room (households a place has land for, about 27 ha each)\nCu copper  St stone  Sa salt  Fi fish  Run river runs\n"
                          "Gm game  Ti timber  Gr grazing  Wi withies  Mill mill site\nrich, poor: the soil (fair unmarked)",
                    title_fontsize=8)
    leg._legend_box.align = "left"
    ax.set_title(w["title"], loc="left", fontsize=12)
    fig.text(0.01, 0.01, textwrap.fill(w["summary"], 160), fontsize=8.5, va="bottom", ha="left", color="#333")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(f"{key}.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    for k, w in D.WORLDS.items():
        draw(k, w)
        print(k, w["size_km"], "km; worst road error", w["fit_err_km"], "km")
