"""W-82: the batch's tables (markdown) from each run's measure.json. Writes runs_w82/summary.md and prints it.

    python3 runs_w82/summary.py
"""
import glob
import json
import os
import re

W82 = os.path.dirname(os.path.abspath(__file__))
ARMS = ["null", "today", "f40", "f15", "f7", "today_r16", "f15_r16", "f7_r16"]
WORKS = {
    "frontier_w82": [("houses (small room)", r"^(Ash|Bram|Cold) House$"), ("hearths", r"^a hearth in"), ("fields cleared", r"^field cleared"),
                     ("a room added", r"^a small room at"), ("granaries", r"^a granary floor")],
    "brookend_w82": [("Wright House", r"^Wright House$"), ("Wright beds", r"beds in Wright House"),
                     ("the Brakes cleared", r"^field cleared: the Brakes"), ("fence round Long Pasture", r"^fence round Long Pasture"),
                     ("granaries", r"^a granary floor"), ("rooms added", r"^a small room at")],
    "runs_w82": [("the weir", r"^the weir on"), ("weir sections", r"^a wattle section")],
}


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(W82, "*", "*_s*", "measure.json"))):
        run = os.path.dirname(f)
        world = os.path.basename(os.path.dirname(run))
        arm, seed = os.path.basename(run).rsplit("_s", 1)
        m = json.load(open(f))
        out.setdefault(world, {}).setdefault(arm, {})[int(seed)] = m
    return out


def fin_days(m, pat):
    """Days the matching works were finished, sorted; and how many were left unfinished."""
    days = sorted(d for k, d in m["finished"].items() if re.search(pat, k) and d is not None)
    nd = sum(1 for k, d in m["finished"].items() if re.search(pat, k) and d is None)
    left = sum(1 for k in m["unfinished"] if re.search(pat.replace("^", "").replace("a small room at", "room at")
                                                         .replace("a granary floor", "granary").replace("field cleared: ", "clearing "), k))
    return days, nd, left


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def table(world, arms):
    seeds = sorted({s for a in arms.values() for s in a})
    L = [f"### {world} ({len(seeds)} seeds, {next(iter(next(iter(arms.values())).values()))['days']} days)", ""]
    L.append("| arm | alive / people | deaths (all seeds) | households housed at the end | food at the end | missed meals | "
             "build units | timber units | food units | build share of work |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for arm in ARMS:
        if arm not in arms:
            continue
        ms = [arms[arm][s] for s in sorted(arms[arm])]
        alive = "/".join(str(m["alive"]) for m in ms) + f" of {ms[0]['people']}"
        deaths = {}
        for m in ms:
            for c, n in m["deaths"].items():
                deaths[c] = deaths.get(c, 0) + n
        housed = "/".join(str(sum(1 for v in m["households"].values() if v == "housed")) + f"of{len(m['households'])}" for m in ms)
        u = lambda k: mean([m["units"][k] for m in ms])
        work = mean([sum(v for k, v in m["units"].items()) for m in ms])
        L.append(f"| {arm} | {alive} | {', '.join(f'{c} {n}' for c, n in sorted(deaths.items())) or 'none'} | {housed} | "
                 f"{mean([m['food_end'] for m in ms]):.0f} | {mean([m['missed_meals'] for m in ms]):.1f} | {u('build'):.0f} | "
                 f"{u('timber'):.0f} | {u('food'):.0f} | {100 * u('build') / max(1, work):.0f}% |")
    L.append("")
    L.append("Days the works were finished (each seed; `-` never; `(n left)` begun and unfinished at the end):")
    L.append("")
    hdr = [w for w, _ in WORKS[world]]
    L.append("| arm | " + " | ".join(hdr) + " |")
    L.append("|---|" + "---|" * len(hdr))
    for arm in ARMS:
        if arm not in arms:
            continue
        cells = []
        for _, pat in WORKS[world]:
            per = []
            for s in sorted(arms[arm]):
                days, nd, left = fin_days(arms[arm][s], pat)
                txt = ",".join(str(d) for d in days) if days else ("done" if nd else "-")
                if left:
                    txt += f" ({left} left)"
                per.append(txt)
            cells.append(" / ".join(per))
        L.append(f"| {arm} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("Build units by work (mean over seeds):")
    L.append("")
    keys = sorted({k for a in arms.values() for m in a.values() for k in m["build_units_by"]})
    L.append("| arm | " + " | ".join(keys) + " |")
    L.append("|---|" + "---|" * len(keys))
    for arm in ARMS:
        if arm not in arms:
            continue
        ms = list(arms[arm].values())
        L.append(f"| {arm} | " + " | ".join(f"{mean([m['build_units_by'].get(k, 0) for m in ms]):.0f}" for k in keys) + " |")
    L.append("")
    return L


if __name__ == "__main__":
    data = load()
    L = []
    for world in ("frontier_w82", "brookend_w82", "runs_w82"):
        if world in data:
            L += table(world, data[world])
    open(os.path.join(W82, "summary.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
