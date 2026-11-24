"""The 30-day runs world with a model to each household (runs/water_runs_models_r1, W-58): people of each household alive by day,
one panel a village, one line a household and its model; beside World 0b's monocultures (w0b_population.png) for the five models
in both. A shared world, not a world a model: the households trade, marry and starve beside each other.

    python3 docs/review/39_monoculture/runs_models_population.py <people_days.parquet>
"""
import os
import sys

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VILLAGES = {"Highpool": ["Brook", "Marsh", "Shepherd"], "Middleham": ["Field", "Hart", "Fletcher"], "Lowstrand": ["Wright", "Cotter", "Wood"]}
TIER = {"strong": "#2a78d6", "middle": "#eb6834", "weak": "#1baf7a"}          # categorical slots 1 to 3 (validated)
TIERS = {"Brook": "strong", "Marsh": "middle", "Shepherd": "weak", "Field": "strong", "Hart": "middle", "Fletcher": "weak",
         "Wright": "strong", "Cotter": "middle", "Wood": "weak"}               # make_runs_models.TIERS by the seeded draw
SHORT = {"claude-fable-5-2": "Fable 5.2", "claude-sonnet-5": "Sonnet 5", "claude-sonnet-4-5": "Sonnet 4.5", "claude-opus-5-5": "Opus 5.5",
         "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-4-5": "Haiku 4.5", "claude-opus-5": "Opus 5", "claude-opus-4-5": "Opus 4.5",
         "claude-haiku-5-5": "Haiku 5.5"}


def main(src, out=os.path.join(HERE, "runs_models_population.png")):
    p = pd.read_parquet(src)
    a = p[p.alive]
    by = a.groupby(["day", "household"]).size().unstack(fill_value=0)
    model = p[p.day == 0].groupby("household").model.agg(lambda s: s.dropna().mode()[0])
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), sharey=True)
    for ax, (village, hhs) in zip(axes, VILLAGES.items()):
        for hh in hhs:
            ys = by[hh] if hh in by else pd.Series(0, index=by.index)
            col = TIER[TIERS[hh]]
            ax.plot(ys.index, ys.values, color=col, lw=2, marker="o", ms=2.5)
            ax.annotate(f"{hh}: {SHORT.get(model[hh], model[hh])}  {int(ys.values[-1])}", (ys.index[-1], ys.values[-1]),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=8, color="#333")
        ax.set_title(village, loc="left", fontsize=10)
        ax.set_xlim(0, 44)
        ax.set_xlabel("day", fontsize=8)
        ax.grid(axis="y", color="#e6e6e6", lw=0.8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#bbb")
        ax.tick_params(labelsize=7.5, colors="#555")
    axes[0].set_ylabel("people of the household alive", fontsize=8)
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], color=c, lw=2, label=f"{t} model of the village") for t, c in TIER.items()], loc="upper right",
               frameon=False, fontsize=8, ncol=3)
    fig.suptitle("The runs world, a model to each household (30 days, a shared world)", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
