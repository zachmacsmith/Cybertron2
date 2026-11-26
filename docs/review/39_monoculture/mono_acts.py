"""What each monoculture arm spends its acts on (W-204): every planned act (turns.jsonl `plan`) put in one of a dozen kinds of work, the
share of each kind by model, and how varied each arm's acts are, by phase of the year. One run a model.

    python3 docs/review/39_monoculture/mono_acts.py [/home/user/mono1]
"""
import collections
import json
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {
    "farming": ["assess grain", "burn the stubble", "clear", "dung", "guard the field", "hoe", "manure", "pest work", "plough", "reap", "sow",
                "weed", "grind", "work"],
    "herding": ["herd", "milk", "slaughter", "hay", "gather hay", "dry fodder", "drive"],
    "fishing and hunting": ["angle", "fish by hand", "gill net", "set gill nets", "set wicker traps", "set", "wicker trap", "tend", "stalk",
                            "hunt the wild", "hunting drive", "snare", "set snares", "den work", "net"],
    "wild food": ["gather wild food", "gather"],
    "keeping and storing food": ["boil salt", "salt pan", "salt fish", "salt meat", "dry fish", "dry meat", "hot smoke fish", "hot smoke meat", "smoke fish",
                     "tend the smoke", "take", "move"],
    "fuel and wood": ["firewood", "gather firewood", "fell", "cut", "cut withies", "charcoal", "burn", "fire", "fire ring", "hearth"],
    "making gear": ["crude tool", "crude weapon", "make", "make clappers", "make crude tools", "make crude weapon", "make fishing rod",
                    "make snares", "make tallow lights", "make wicker trap", "bone hook", "copper tool", "fishing rod", "gill nets", "hand line",
                    "snares", "twist cord", "mend gear", "wicker traps"],
    "building and repair": ["build", "beds", "bins", "camp", "clear for building", "granary", "small room", "owl hole", "repair"],
    "guarding": ["fence", "shut", "shut the gate", "guard", "watch"],
    "family and care": ["care", "try", "partner", "teach", "learn", "bury", "name"],
    "dealing with others": ["agree", "accept", "admit", "give", "grant", "join", "meet", "say", "order", "claim", "found"],
    "travel": ["go", "come"],
    "mining": ["mine", "smelt"],
    "rest": ["rest", "sleep"],
}
ACT = {a: k for k, acts in NAMES.items() for a in acts}
COLOURS = ["#1baf7a", "#eda100", "#2a78d6", "#7cc36b", "#e87ba4", "#8a6d3b", "#7b61c9", "#eb6834", "#4f9fd0", "#d14f7a", "#2bb5b0",
           "#999999", "#5a5a5a", "#cccccc", "#f2c94c"]
MODELS = [("opus55", "Opus 5.5"), ("sonnet55", "Sonnet 5.5"), ("sonnet5", "Sonnet 5"), ("sonnet45", "Sonnet 4.5"), ("haiku55", "Haiku 5.5"),
          ("haiku45", "Haiku 4.5")]
PHASES = [(0, 15, "spring and summer"), (16, 31, "autumn and winter"), (32, 49, "the next spring")]


def acts(run, lo=0, hi=10 ** 6):
    out = []
    for t in map(json.loads, open(os.path.join(run, "turns.jsonl"))):
        if lo <= t["day"] <= hi:
            out += [str(p.get("do")) for p in (t.get("plan") or []) if isinstance(p, dict)]
    return out


def diversity(xs):
    c = collections.Counter(xs)
    n = sum(c.values())
    if not n:
        return None, None, None
    h = -sum(v / n * math.log(v / n) for v in c.values())
    return len(c), round(math.exp(h), 1), round(100 * sum(v for _, v in c.most_common(5)) / n)


def main(root="/home/user/mono1", out=os.path.join(HERE, "mono_acts.png")):
    rows = []
    for world in ("m5", "m1"):
        for m, label in MODELS:
            run = os.path.join(root, f"{world}_{m}")
            if not os.path.exists(os.path.join(run, "turns.jsonl")):
                continue
            xs = acts(run)
            share = collections.Counter(ACT.get(a, "other") for a in xs)
            n = sum(share.values())
            rows.append((world, label, {k: share.get(k, 0) / n for k in list(NAMES) + ["other"]}, xs, run))
    print("share of acts by kind (%)")
    kinds = list(NAMES) + ["other"]
    for world, label, sh, xs, run in rows:
        print(f"  {world} {label:10} " + "  ".join(f"{k[:12]} {100 * sh[k]:4.1f}" for k in kinds if sh[k] >= 0.005))
    print("\ndiversity by phase (different acts, effective acts, top-five share %)")
    for world, label, sh, xs, run in rows:
        cells = []
        for lo, hi, name in PHASES:
            d = diversity(acts(run, lo, hi))
            cells.append(f"{name}: {d[0]}/{d[1]}/{d[2]}%" if d[0] else f"{name}: -")
        print(f"  {world} {label:10} " + " | ".join(cells))
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={"width_ratios": [6, 5]})
    for ax, world, title in ((axes[0], "m5", "The Scattering (to day 50 or dying out)"), (axes[1], "m1", "Fallowmere (to day 10)")):
        sel = [r for r in rows if r[0] == world]
        left = [0.0] * len(sel)
        for i, k in enumerate(kinds):
            vals = [100 * r[2][k] for r in sel]
            ax.barh([r[1] for r in sel], vals, left=left, color=COLOURS[i % len(COLOURS)], label=k, height=0.65)
            for j, (v, l0) in enumerate(zip(vals, left)):
                if v >= 7:
                    ax.text(l0 + v / 2, j, f"{v:.0f}", ha="center", va="center", fontsize=7, color="white")
            left = [a + b for a, b in zip(left, vals)]
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_xlabel("share of all acts (%)", fontsize=8)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=8)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=8, frameon=False, fontsize=7.5)
    fig.suptitle("What each model spends its people's work on (every planned act, by kind)", x=0.01, ha="left", fontsize=11)
    fig.tight_layout(rect=(0, 0.08, 1, 0.94))
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main(*sys.argv[1:2])
