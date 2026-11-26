"""The Scattering (M5): where each arm's people have been by day 29 (W-204). One panel a model: the places on the road network (the
world file's node positions and roads, with each road's days), the four homes in their household's colour, each place someone of
that arm stood at (turns.jsonl `at`, days 0 to 29) filled, the rest hollow. A place's position is the generator's (`xy`, km).

    python3 docs/review/39_monoculture/scattering_explored.py [/home/user/mono1]
"""
import json
import os
import sys

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
HOMES = {"Holtmouth": ("Strand, fishers", "#2a78d6"), "Highcairn": ("Fell, herders", "#eb6834"),
         "Lowbury": ("Meade, farmers", "#1baf7a"), "Hartsmoot": ("Holt, hunters", "#7b61c9")}
ARMS = [("opus55", "Opus 5.5"), ("sonnet55", "Sonnet 5.5"), ("sonnet5", "Sonnet 5"), ("sonnet45", "Sonnet 4.5"), ("haiku55", "Haiku 5.5"),
        ("haiku45", "Haiku 4.5")]


def visited(run, upto=29):
    out = {}
    for t in map(json.loads, open(os.path.join(run, "turns.jsonl"))):
        if t["day"] <= upto and t.get("at"):
            out.setdefault(t["at"], set()).add(t["agent"])
    return out


def main(root="/home/user/mono1", out=os.path.join(HERE, "scattering_explored.png")):
    w = yaml.safe_load(open(os.path.join(ROOT, "cybertron2/specs/mono/m5.yaml")))
    xy = {n: tuple(v["xy"]) for n, v in w["nodes"].items()}
    home_of = {}
    for n, a in w["agents"].items():
        home_of[n] = next((h for h, (lab, _) in HOMES.items() if lab.startswith(a["household"])), None)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10.5))
    for ax, (m, label) in zip(axes.flat, ARMS):
        run = os.path.join(root, f"m5_{m}")
        vis = visited(run)
        for r in w["roads"]:
            a, b, d = r[0], r[1], int(r[2])
            (x1, y1), (x2, y2) = xy[a], xy[b]
            ax.plot([x1, x2], [y1, y2], color="#cfcfcf", lw=1, zorder=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(d), fontsize=6, color="#999", ha="center", va="center", zorder=2,
                    bbox=dict(boxstyle="circle,pad=0.1", fc="white", ec="none"))
        for n, (x, y) in xy.items():
            if n in HOMES:
                col = HOMES[n][1]
                ax.scatter([x], [y], s=170, marker="s", color=col, zorder=4)
                ax.text(x, y - 3.2, n, fontsize=7.5, ha="center", va="top", color=col, weight="bold", zorder=5)
                continue
            who = vis.get(n) or set()
            homes = {home_of.get(p) for p in who} - {None}
            if who:
                col = HOMES[sorted(homes)[0]][1] if homes else "#555"
                ax.scatter([x], [y], s=70, color=col, edgecolor="white", lw=0.8, zorder=4)
                ax.text(x, y + 2.2, n, fontsize=6.5, ha="center", va="bottom", color="#333", zorder=5)
            else:
                ax.scatter([x], [y], s=28, facecolor="white", edgecolor="#bbb", lw=0.8, zorder=3)
                ax.text(x, y + 1.8, n, fontsize=5.5, ha="center", va="bottom", color="#bbb", zorder=3)
        n_vis = len([n for n in vis if n not in HOMES])
        ax.set_title(f"{label}: {n_vis} places beyond the homes reached", loc="left", fontsize=10)
        ax.set_aspect("equal")
        ax.axis("off")
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], marker="s", ls="", color=c, ms=9, label=f"{h} ({lab})") for h, (lab, c) in HOMES.items()]
    hs += [Line2D([], [], marker="o", ls="", color="#555", ms=7, label="reached (coloured by whose people)"),
           Line2D([], [], marker="o", ls="", mfc="white", mec="#bbb", ms=6, label="never reached"),
           Line2D([], [], color="#cfcfcf", lw=1, label="road (number: days)")]
    fig.legend(handles=hs, loc="lower center", ncol=4, frameon=False, fontsize=8)
    fig.suptitle("The Scattering: where each model's people went, days 0 to 29 (every home is 4 days from every other, all through "
                 "Threeways)", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:2])
