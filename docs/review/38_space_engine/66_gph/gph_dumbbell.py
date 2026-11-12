"""The hunger probe's confound check as a dumbbell (38.66): for each model and ask, the promise's mean and the grade's mean, joined;
each run a faint dot. Left: meals the household missed; right: salt held. Reads the runs from RUNS (default ../../../../runs)."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.argv = sys.argv[:2]
import gph_confound_chart as C          # cell(): the three runs of a cell
ROWS = [("haiku", "memory_25", "scored_high", "Haiku, 25 salt"), ("haiku", "memory_all", "scored_max", "Haiku, all you can"),
        ("sonnet", "memory_25", "scored_high", "Sonnet, 25 salt"), ("sonnet", "memory_all", "scored_max", "Sonnet, all you can")]
BLUE, ORANGE = "#2a78d6", "#eb6834"
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150, sharey=True)
for ax, key, lab in ((axes[0], "missed", "Meals the household missed (8 nights)"), (axes[1], "salt", "Salt held at the end")):
    for y, (p, mem, grd, name) in enumerate(ROWS):
        m, g = C.cell(p, mem), C.cell(p, grd)
        mv, gv = [r[key] for r in m], [r[key] for r in g]
        mm, gm = sum(mv) / 3, sum(gv) / 3
        ax.plot([mm, gm], [y, y], color="#999999", linewidth=2, zorder=1)
        ax.scatter(mv, [y - 0.25] * 3, color=BLUE, alpha=0.35, s=18, zorder=2)
        ax.scatter(gv, [y + 0.25] * 3, color=ORANGE, alpha=0.35, s=18, zorder=2)
        ax.scatter([mm], [y], color=BLUE, s=70, zorder=3, label="Promise (in-world)" if y == 0 else None)
        ax.scatter([gm], [y], color=ORANGE, s=70, zorder=3, label="Grade" if y == 0 else None)
        lo, hi = (mm, gm) if mm <= gm else (gm, mm)
        for v, col in ((mm, BLUE), (gm, ORANGE)):                     # the means' values outside the bar, clear of the dots
            left = v == lo and v != hi or (v == mm and mm == gm)
            ax.annotate(f"{v:.1f}", (v, y), xytext=(-9 if left else 9, -3), textcoords="offset points",
                        ha="right" if left else "left", fontsize=8, color=col, fontweight="bold")
    if key == "salt":
        ax.axvline(25, color="grey", linestyle="--", linewidth=1)
        ax.text(25.3, -0.45, "25 salt", fontsize=8, color="grey")
    ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([r[3] for r in ROWS])
    ax.set_xlim(*((-1.2, 12.5) if key == "missed" else (-3, 33)))
    ax.set_title(lab, fontsize=10); ax.grid(axis="x", alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylim(len(ROWS) - 0.5, -0.6)                          # first row on top (the axes share y: set once)
fig.legend(*axes[0].get_legend_handles_labels(), fontsize=9, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.94))
fig.suptitle("The same ask, framed as a deathbed promise or as a grade (mean of 3 runs; faint dots are single runs)", fontsize=10)
fig.tight_layout(rect=(0, 0, 1, 0.9))
fig.savefig("gph_dumbbell.png")
print("ok")
