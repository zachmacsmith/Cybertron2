"""The hunger probe's confound check in two dimensions (38.66): one panel per model and ask, each comparing exactly one pair. Each
small dot is a run (salt at the end, meals the household missed); the large dot is the mean of its 3; blue the promise, orange the
grade; a black ring marks a run where someone died."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.argv = sys.argv[:2]
import gph_confound_chart as C
BLUE, ORANGE = "#2a78d6", "#eb6834"
ASKS = [("memory_25", "scored_high", "Asked for 25 salt"), ("memory_all", "scored_max", "Asked for all they can")]
fig, axes = plt.subplots(2, 2, figsize=(10, 8), dpi=150, sharex=True, sharey=True)
for i, p in enumerate(("haiku", "sonnet")):
    for j, (mem, grd, ask) in enumerate(ASKS):
        ax = axes[i][j]
        for arm, col, lab in ((mem, BLUE, "Promise (in-world)"), (grd, ORANGE, "Grade")):
            runs = C.cell(p, arm)
            for k, r in enumerate(runs):
                ax.scatter([r["salt"] + 0.25 * (k - 1)], [r["missed"]], s=40, color=col, alpha=0.6, zorder=3,
                           edgecolors="black" if r["dead"] else col, linewidths=1.8 if r["dead"] else 0)
            mx, my = sum(r["salt"] for r in runs) / 3, sum(r["missed"] for r in runs) / 3
            ax.scatter([mx], [my], s=170, color=col, zorder=4, edgecolors="white", linewidths=1.5, label=f"{lab}, mean of 3")
        ax.axvline(25, color="grey", linestyle="--", linewidth=1)
        ax.set_title(f"{p.capitalize()} parents, {ask.lower()}", fontsize=10)
        ax.grid(alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(-1, 33); ax.set_ylim(-0.8, 12)
for ax in axes[1]:
    ax.set_xlabel("Salt held at the end (dashed: 25)")
for ax in axes[:, 0]:
    ax.set_ylabel("Meals the household missed")
h, l = axes[0][0].get_legend_handles_labels()
h += [plt.Line2D([], [], linestyle="none", marker="o", markersize=7, color=BLUE, alpha=0.6),
      plt.Line2D([], [], linestyle="none", marker="o", markersize=7, markerfacecolor="white", markeredgecolor="black", markeredgewidth=1.8)]
l += ["A single run", "Someone died in that run"]
fig.legend(h, l, fontsize=8, frameon=False, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.955))
fig.suptitle("The same ask as a deathbed promise (blue) or as a grade (orange). Right = more salt; up = more meals the family missed",
             fontsize=10)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("gph_scatter.png")
print("ok")
