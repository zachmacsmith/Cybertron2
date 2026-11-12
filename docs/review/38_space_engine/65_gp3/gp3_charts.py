"""Round 3's charts (38.65): one PNG per good, what the target household got by wording, one line per model.
    python3 gp3_charts.py ROWS.csv OUT_DIR"""
import csv, sys, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = list(csv.DictReader(open(sys.argv[1])))
out = sys.argv[2]
WORDINGS = ["No goal", "Strong memory", "Graded high", "As much as possible"]
MODELS = [("Haiku", "#2a78d6"), ("Sonnet", "#eb6834"), ("Opus", "#1baf7a")]
TITLE = {"salt": "Salt", "copper": "Copper", "timber": "Timber (held + built into rooms)"}
for good in ("salt", "copper", "timber"):
    rs = [r for r in rows if r["good"] == good]
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=150)
    x = range(len(WORDINGS))
    for mod, col in MODELS:
        pts = [next(r for r in rs if r["model"] == mod and r["wording"] == w) for w in WORDINGS]
        ys = [float(r["total"]) for r in pts]
        ax.plot(x, ys, marker="o", color=col, linewidth=2, label=f"{mod} pair")
        for xi, r, yv in zip(x, pts, ys):
            if r["deaths"]:
                ax.scatter([xi], [yv], s=160, facecolors="none", edgecolors="black", linewidths=1.2, zorder=5)
    ax.axhline(float(rs[0]["target_high"]), color="grey", linestyle="--", linewidth=1, label="Graded-high target")
    ax.axhline(float(rs[0]["holder_stock"]), color="grey", linestyle=":", linewidth=1.2, label="Holders' starting stock")
    ax.scatter([], [], s=160, facecolors="none", edgecolors="black", label="Someone died in the run")
    ax.set_xticks(list(x)); ax.set_xticklabels(WORDINGS)
    ax.set_ylabel(f"{good} the target household got (end of day 8)")
    ax.set_title(f"{TITLE[good]}: by goal wording and model (n = 1 per point)")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    p = os.path.join(out, f"gp3_{good}.png")
    fig.savefig(p); plt.close(fig)
    print(p)
