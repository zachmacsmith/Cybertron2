"""World 0b's people alive by day, by village: each model a colour, the broken prompt dashed (w0b_*), the fixed one solid (w0c_*)
(W-202). A person's village is the one they slept in that night, else their founding household's; a death is counted the night it
happens.

    python3 docs/review/39_monoculture/w0_population_compare.py /home/user/mono1
"""
import json
import os
import sys

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MODELS = [("sonnet55", "Sonnet 5.5", "#2a78d6"), ("haiku55", "Haiku 5.5", "#eb6834"), ("haiku45", "Haiku 4.5", "#1baf7a")]
HOUSE = {"Brook House": "Highpool", "Marsh House": "Highpool", "Field House": "Middleham", "Fletcher House": "Middleham"}
HH = {"Brook": "Highpool", "Marsh": "Highpool", "Field": "Middleham", "Fletcher": "Middleham"}


def series(run, home):
    out = {"Highpool": [], "Middleham": [], "both": []}
    last = {}
    for d in map(json.loads, open(os.path.join(run, "days.jsonl"))):
        here = set(d.get("ate") or {}) | set(d.get("slept") or {})
        here -= set(d.get("deaths") or [])                                 # those who died that night
        count = {"Highpool": 0, "Middleham": 0}
        for n in here:
            v = HOUSE.get((d.get("slept") or {}).get(n)) or last.get(n) or HH.get(home.get(n)) or "Middleham"
            last[n] = v
            count[v] += 1
        for k in count:
            out[k].append((d["day"], count[k]))
        out["both"].append((d["day"], sum(count.values())))
    return out


def main(root):
    home = {n: a.get("household") for n, a in yaml.safe_load(open(os.path.join(ROOT, "cybertron2/specs/mono/world0b_sonnet55.yaml")))["agents"].items()}
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), sharey=False)
    for ax, key, title in zip(axes, ("both", "Highpool", "Middleham"), ("Both villages", "Highpool (fishing, salt)", "Middleham (farming, mill)")):
        for m, label, col in MODELS:
            for tag, ls in (("w0b", (0, (4, 3))), ("w0c", "-")):
                run = os.path.join(root, f"{tag}_{m}")
                if not os.path.exists(os.path.join(run, "days.jsonl")):
                    continue
                pts = series(run, home)[key]
                if not pts:
                    continue
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color=col, lw=2 if tag == "w0c" else 1.6, ls=ls, alpha=1 if tag == "w0c" else 0.85)
                ax.annotate(str(ys[-1]), (xs[-1], ys[-1]), xytext=(3, 0), textcoords="offset points", fontsize=7.5, color=col, va="center")
        ax.axvline(13, color="#999", lw=0.8, ls=":")
        ax.text(13.2, ax.get_ylim()[1] * 0.97 if ax.get_ylim()[1] else 1, "first frost (13)", fontsize=7, color="#777", va="top")
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_xlim(0, 26)
        ax.set_xlabel("day", fontsize=8)
        ax.grid(axis="y", color="#e6e6e6", lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#bbb")
        ax.tick_params(labelsize=7.5, colors="#555")
    axes[0].set_ylabel("people alive", fontsize=8)
    handles = [Line2D([], [], color=c, lw=2, label=l) for _, l, c in MODELS] + \
              [Line2D([], [], color="#555", lw=2, label="fixed prompt"), Line2D([], [], color="#555", lw=1.6, ls=(0, (4, 3)), label="broken prompt")]
    fig.legend(handles=handles, loc="upper right", frameon=False, fontsize=8, ncol=5)
    fig.suptitle("World 0b: people alive by day, the models on the broken and the fixed prompt", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out = os.path.join(HERE, "w0_population_compare.png")
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
