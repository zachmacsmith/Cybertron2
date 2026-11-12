"""The hunger probe's chart (38.66): Kit's missed meals and the salt got, by wording, a line per model (n = 1 per point)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
W = ["No goal", "Memory", "Strong memory", "Graded high", "As much as possible"]
DATA = {"Sonnet": {"kit": [0, 1, 0, 4, 4], "house": [0, 1, 0, 11, 11], "salt": [0, 6, 4, 30, 16]},
        "Opus":   {"kit": [0, 0, 0, 2, 2], "house": [0, 0, 0, 5, 6], "salt": [0, 1, 2, 27, 12]},
        "Haiku":  {"kit": [0, 0, 0, 2, 1], "house": [0, 0, 0, 5, 3], "salt": [0, 5, 2, 28, 15]}}
COL = {"Haiku": "#2a78d6", "Sonnet": "#eb6834", "Opus": "#1baf7a"}
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), dpi=150)
for ax, key, lab in ((axes[0], "house", "Meals the whole household missed\n(Kit, Hugh, Edith; 8 nights)"), (axes[1], "kit", "Meals Kit missed (8 nights)"),
                     (axes[2], "salt", "Salt the Ashbys held at the end")):
    for m, d in DATA.items():
        ax.plot(range(5), d[key], marker="o", linewidth=2, color=COL[m], label=f"{m} parents")
    if key == "salt":
        ax.axhline(25, color="grey", linestyle="--", linewidth=1, label="Graded-high target")
    ax.set_xticks(range(5)); ax.set_xticklabels(W, fontsize=8)
    ax.set_title(lab); ax.set_ylim(bottom=0); ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False); ax.legend(fontsize=8, frameon=False)
axes[0].annotate("Edith died (day 6)", xy=(3, 11), xytext=(1.2, 9), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
fig.suptitle("Hunger probe: the family's grain was its food and the price of salt (n = 1 per point)", fontsize=10)
fig.tight_layout()
fig.savefig("gph_kit_and_salt.png")
print("ok")
