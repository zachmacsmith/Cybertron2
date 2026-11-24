"""World 0b's population by day, one line a model (W-202): from each arm's log ("day N: alive X"), day 0 the 21 founders; births and
deaths from the run's events. The arms stopped on 24 Nov at different days (Zach); the restart on the try fix marked.

    python3 docs/review/39_monoculture/w0b_population.py
"""
import os
import re
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RUNS = "/home/user/mono1"
HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = [("sonnet55", "Sonnet 5.5", "#2a78d6"), ("haiku55", "Haiku 5.5", "#eb6834"), ("haiku45", "Haiku 4.5", "#1baf7a"),
        ("sonnet45", "Sonnet 4.5", "#eda100"), ("sonnet5", "Sonnet 5", "#e87ba4")]   # categorical slots 1 to 5 (validated)


def series(arm):
    alive = {0: 21}
    for line in open(os.path.join(RUNS, f"w0b_{arm}.log")):
        m = re.match(r"day (\d+): alive (\d+)", line)
        if m:
            alive[int(m.group(1))] = int(m.group(2))
    c = sqlite3.connect(os.path.join(RUNS, f"w0b_{arm}", "run.db"))
    births = [int(d) + 1 for (d,) in c.execute("select day from events where kind='birth'")]
    return sorted(alive.items()), births


def main(out=os.path.join(HERE, "w0b_population.png")):
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for arm, label, col in ARMS:
        pts, births = series(arm)
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=2, marker="o", ms=3.5, label=label, solid_capstyle="round")
        for b in births:
            y = dict(pts).get(b)
            if y is not None:
                ax.scatter([b], [y], s=90, marker="*", color=col, edgecolor="white", linewidth=0.8, zorder=5)
        up = 9 if ys[-1] >= 21 else 0                                    # the arms still at 21 lie on the others' lines: lift
        ax.annotate(f"{label}  {ys[-1]}", (xs[-1], ys[-1]), xytext=(4, up), textcoords="offset points", va="center",
                    fontsize=9, color="#333")
    ax.set_xlim(0, 27)
    ax.set_ylim(0, 23)
    ax.set_xlabel("day", fontsize=9)
    ax.set_ylabel("people alive", fontsize=9)
    ax.grid(axis="y", color="#e6e6e6", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#bbb")
    ax.tick_params(labelsize=8, colors="#555")
    ax.axhline(21, color="#bbb", lw=0.8, ls=(0, (3, 3)))
    ax.text(0.3, 21.4, "21 founders", fontsize=8, color="#777")
    ax.scatter([], [], s=90, marker="*", color="#777", label="a birth")
    ax.legend(loc="lower left", frameon=False, fontsize=8.5, ncol=3)
    ax.set_title("World 0b: people alive by day, one model a world (stopped 24 Nov)", loc="left", fontsize=11)
    import textwrap
    fig.text(0.01, 0.01, textwrap.fill("Each arm is one model for all 21 people (13 acting at the start), the same world, the graded goal. Stopped at "
                         "different days by the usage window and then by hand. On the interface audited in prompt_audit.md (before D5-2).", 150),
             fontsize=7.5, color="#555")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(out, dpi=150)
    print(out)


if __name__ == "__main__":
    main()
