"""Review 38.67 charts: offers_price.png. Binned means of rel (log of the asking against the run's going rate for the pair) with 95%
intervals, by the maker's model; and how often offers were taken against rel."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("offers.csv")
d = d[(d.model != "bot") & (d.n_give == 1) & (d.n_get == 1) & (d.give_qty > 0) & (d.get_qty > 0) & (d.give_later != 1) & (d.get_later != 1)
      & (d.give_item != d.get_item) & d.people_here.notna()].copy()
d["grp"] = d.run + d.give_item + d.get_item
d["lp"] = np.log(d.get_qty / d.give_qty)
d = d[d.groupby("grp").lp.transform("size") >= 2]
d["rel"] = d.lp - d.groupby("grp").lp.transform("mean")
d["own"] = d.give_household / d.hh_size.clip(lower=1)
COL = {"haiku": "#eb6834", "sonnet": "#2a78d6", "opus": "#3a3a3a"}

def binned(ax, x, bins, labels, title, xlabel, df=None):
    df = d if df is None else df
    for i, (mdl, g) in enumerate(df.groupby("model")):
        b = pd.cut(g[x], bins, labels=False, include_lowest=True)
        s = g.groupby(b).rel.agg(["mean", "sem", "size"])
        s = s[s["size"] >= 5]
        xs = s.index.values + (i - 1) * 0.12
        ax.errorbar(xs, s["mean"], yerr=1.96 * s["sem"], marker="o", ms=5, capsize=3, lw=1.6, color=COL[mdl], label=f"{mdl} ({len(g)})")
    ax.axhline(0, color="#999", lw=0.8)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
    ax.set_title(title, fontsize=11, loc="left"); ax.set_xlabel(xlabel)

fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
binned(axs[0], "own", [-0.01, 3, 10, 1e9], ["<3", "3-10", ">10"],
       "Asking against the maker's own stock", "the maker's household holding of the good given, a head\n(work offered left out: it is not held)", df=d[d.give_item != "work (days)"])
axs[0].set_ylabel("log(asking / the run's going rate for the pair)\nabove 0: asks more than the going rate")
binned(axs[1], "hh_food_days", [-0.01, 2, 5, 10, 1e9], ["<2", "2-5", "5-10", ">10"],
       "Asking against the household's food", "the maker's household food, in days a head")
axs[0].legend(frameon=False, fontsize=9, title="maker's model (offers)", title_fontsize=9)
b = pd.cut(d.rel, [-9, -0.2, -0.02, 0.02, 0.2, 9], labels=["much\ncheaper", "cheaper", "at the\nrate", "dearer", "much\ndearer"])
s = d.assign(acc=d.taken.gt(0)).groupby(b, observed=True).acc.agg(["mean", "size"])
axs[2].bar(range(len(s)), s["mean"], color="#9aa5b1", width=0.6)
for i, (v, n) in enumerate(zip(s["mean"], s["size"])):
    axs[2].text(i, v + 0.01, f"n={n}", ha="center", fontsize=8)
axs[2].set_xticks(range(len(s))); axs[2].set_xticklabels(s.index)
axs[2].set_ylabel("share taken at least once"); axs[2].set_ylim(0, 0.6)
axs[2].set_title("Taken, against the asking", fontsize=11, loc="left"); axs[2].set_xlabel("the asking against the run's going rate (to the taker)")
for a in axs: a.spines[["top", "right"]].set_visible(False)
fig.suptitle(f"Offers in cybertron2 runs with a state each dawn ({len(d)} single-item spot offers, {d.run.nunique()} runs)", x=0.01, ha="left", fontsize=12)
fig.tight_layout(); fig.savefig("offers_price.png", dpi=150)
