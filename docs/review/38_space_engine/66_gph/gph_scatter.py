"""The hunger probe's confound check in two dimensions (38.66): each run's salt at the end against the meals its household missed.
Colour: promise or grade; shape: the parents' model; an arrow from each ask's promise mean to its grade mean."""
import random, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.argv = sys.argv[:2]
import gph_confound_chart as C
BLUE, ORANGE = "#2a78d6", "#eb6834"
SHAPE = {"haiku": "o", "sonnet": "s"}
ASKS = [("memory_25", "scored_high", "25 salt"), ("memory_all", "scored_max", "all you can")]
rng = random.Random(1)
fig, ax = plt.subplots(figsize=(8, 5.6), dpi=150)
for p in ("haiku", "sonnet"):
    for mem, grd, ask in ASKS:
        means = []
        for arm, col in ((mem, BLUE), (grd, ORANGE)):
            runs = C.cell(p, arm)
            xs = [r["salt"] + rng.uniform(-0.3, 0.3) for r in runs]
            ys = [r["missed"] + rng.uniform(-0.15, 0.15) for r in runs]
            for x_, y_, r in zip(xs, ys, runs):                          # one by one: only a run with a death is outlined
                ax.scatter([x_], [y_], marker=SHAPE[p], s=55 if r["dead"] else 45, color=col, alpha=0.75 if r["dead"] else 0.55,
                           edgecolors="black" if r["dead"] else col, linewidths=1.8 if r["dead"] else 0, zorder=3)
            means.append((sum(r["salt"] for r in runs) / 3, sum(r["missed"] for r in runs) / 3))
        (x0, y0), (x1, y1) = means
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color="#555555", lw=1.4), zorder=2)
        ax.annotate(f"{p.capitalize()}, {ask}", ((x0 + x1) / 2, (y0 + y1) / 2), xytext=(6, -10 if p == "haiku" else 6),
                    textcoords="offset points", fontsize=8, color="#333333")
ax.axvline(25, color="grey", linestyle="--", linewidth=1)
ax.text(25.3, 0.2, "25 salt", fontsize=8, color="grey")
for lab, kw in (("Promise (in-world)", dict(color=BLUE, marker="o")), ("Grade", dict(color=ORANGE, marker="o")),
                ("Haiku parents", dict(color="grey", marker="o")), ("Sonnet parents", dict(color="grey", marker="s")),
                ("Someone died", dict(color="white", marker="o", markeredgecolor="black"))):
    ax.plot([], [], linestyle="none", markersize=7, label=lab, **kw)
ax.legend(fontsize=8, frameon=False, loc="upper left")
ax.set_xlabel("Salt held at the end"); ax.set_ylabel("Meals the household missed (Kit, Hugh, Edith; 8 nights)")
ax.set_title("Same ask, promise or grade: each dot a run; arrows go from the promise's mean to the grade's", fontsize=10)
ax.set_xlim(-1, 33); ax.set_ylim(-0.6, 12)
ax.grid(alpha=0.3); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("gph_scatter.png")
print("ok")
