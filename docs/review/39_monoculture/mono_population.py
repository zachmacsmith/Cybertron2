"""The 200-day monoculture arms (W-204): people alive by day, one line a model, a panel a world (the Scattering, Fallowmere). Alive is
everyone who ate or slept that night less those who died in it (days.jsonl). Births marked with a small tick on the line.

    python3 docs/review/39_monoculture/mono_population.py [/home/user/mono1]
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = [("opus55", "Opus 5.5", "#7b61c9"), ("sonnet55", "Sonnet 5.5", "#2a78d6"), ("sonnet5", "Sonnet 5", "#e87ba4"),
          ("sonnet45", "Sonnet 4.5", "#eda100"), ("haiku55", "Haiku 5.5", "#eb6834"), ("haiku45", "Haiku 4.5", "#1baf7a")]
WORLDS = [("m5", "The Scattering (4 homes, 16 founders)"),
          ("m1b", "Fallowmere, rebuilt (2 homes a day apart, 12 founders; D5-8 to D5-10)")]   # the first Fallowmere (m1_*, day 10) left out


def series(run):
    xs, ys, born = [], [], []
    for d in map(json.loads, open(os.path.join(run, "days.jsonl"))):
        alive = (set(d.get("ate") or {}) | set(d.get("slept") or {})) - set(d.get("deaths") or [])
        xs.append(d["day"])
        ys.append(len(alive))
        if (d.get("life") or {}).get("births"):
            born.append((d["day"], len(alive)))
    return xs, ys, born


def main(root="/home/user/mono1", out=os.path.join(HERE, "mono_population.png")):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw={"width_ratios": [1.2, 1]})
    for ax, (w, title) in zip(axes, WORLDS):
        top = 0
        ends = []
        for m, label, col in MODELS:
            run = os.path.join(root, f"{w}_{m}")
            if not os.path.exists(os.path.join(run, "days.jsonl")):
                continue
            xs, ys, born = series(run)
            top = max(top, max(ys))
            ax.plot(xs, ys, color=col, lw=2, label=label, solid_capstyle="round")
            for bx, by in born:
                ax.plot([bx], [by], marker="|", color=col, ms=7, mew=1.5)
            ends.append([ys[-1], xs[-1], f"{label} {ys[-1]}", col])
        ends.sort(key=lambda e: e[0])                                     # end labels spread apart, none on another
        gap = (top + 3) * 0.045
        placed = []
        for y0, x0, text, col in ends:
            y = max(y0, placed[-1] + gap) if placed else y0
            placed.append(y)
            ax.annotate(text, (x0, y0), xytext=(x0 + 0.4, y), textcoords="data", fontsize=7.5, color=col, va="center")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_xlabel("day", fontsize=8)
        ax.set_ylim(0, top + 3)
        ax.set_xlim(0, ax.get_xlim()[1] + 4)
        ax.grid(axis="y", color="#e6e6e6", lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#bbb")
        ax.tick_params(labelsize=7.5, colors="#555")
    axes[0].set_ylabel("people alive", fontsize=8)
    fig.legend(*axes[0].get_legend_handles_labels(), loc="upper right", frameon=False, fontsize=8, ncol=6)
    fig.suptitle("Monoculture arms: people alive by day (ticks: births)", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:2])
