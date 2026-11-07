"""python -m cybertron2.capacity INPUT ... [--out DIR] [--png] [--horizon DAYS] [--figures]

INPUT: a world file (YAML), or a run directory or run.db (the world it started from: the journal's spec). Writes for each:
DIR/<name>/report.json, summary.md, and with --figures the SVG figures (and PNGs with --png).
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3

import yaml


def load(path) -> tuple:
    if os.path.isdir(path):
        if not os.path.exists(os.path.join(path, "run.db")) and os.path.exists(os.path.join(path, "run.json")):
            return os.path.basename(os.path.normpath(path)), json.load(open(os.path.join(path, "run.json")))["spec"]
        path = os.path.join(path, "run.db")
    if path.endswith(".db"):
        c = sqlite3.connect(path)
        spec = json.loads(c.execute("SELECT value FROM meta WHERE key = 'spec'").fetchone()[0])
        return os.path.basename(os.path.dirname(os.path.abspath(path))), spec
    with open(path) as f:
        spec = yaml.safe_load(f)
    return os.path.splitext(os.path.basename(path))[0], spec


def summary(name, rep) -> str:
    from cybertron2.capacity.figures import WORDS
    lines = [f"# Carrying capacity: {name}", "",
             f"Year {rep['year']} days; day {rep['day']} is {rep['calendar']['season']} day {rep['calendar']['day']}. {rep['ceiling']}.", "",
             "| Where | People | " + " | ".join(WORDS[l] for l in rep["levels"]) + " | fuel (dead wood / + young / + trees) | buffer days | first harvest |",
             "|---|---|" + "---|" * len(rep["levels"]) + "---|---|---|"]
    for nid, r in rep["nodes"].items():
        if not r["people"] and r["levels"].get("best", {}).get("supported", 0) < 1:
            continue
        cells = []
        for l, v in r["levels"].items():
            cells.append(f"{v['supported']:g}" + (f" ({v['ratio']:g}x)" if v["ratio"] is not None else ""))
        fu = r["fuel"]["levels"]
        fh = r["first_harvest"]
        lost = f"; {len(fh['lost_to_frost'])} crop(s) the frost takes first" if fh["lost_to_frost"] else ""
        lines.append(f"| {nid} | {r['people']} | " + " | ".join(cells) +
                     f" | {fu['gathered']['supported']:g} / {fu['cut']['supported']:g} / {fu['managed']['supported']:g} | "
                     f"{r['buffer_days'] if r['buffer_days'] is not None else '-'} | {fh['first']} days{lost} |")
    reg = rep["nodes"]["(region)"]
    lines += ["", "**What each level costs (the whole region, at the people it feeds):**", "",
              "| Level | Fed | Food a plot a year | Food a unit of work | Work a head a year | Capital a head (with materials) | Waste |",
              "|---|---|---|---|---|---|---|"]
    for l, v in reg["levels"].items():
        a = v["at_supported"]
        lines.append(f"| {WORDS[l]} | {v['supported']:g} | {a['land']['field_food_a_plot'] or '-'} | {a['recurring']['food_a_unit'] or '-'} | "
                     f"{a['recurring']['a_head'] or '-'} | {a['capital']['with_materials_a_head'] or '-'} | {a['waste_share']:.0%} |")
    gave = {l: v["gave_up"] for l, v in reg["levels"].items() if v["gave_up"]}
    if gave:
        lines += ["", "Out of reach in this world: " + "; ".join(f"{WORDS[l]}: {', '.join(g)}" for l, g in gave.items()) + "."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", default="capacity_out")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--horizon", type=int, default=None)
    a = ap.parse_args(argv)
    from cybertron2.capacity import figures as FG, model as M, space as SP
    for inp in a.inputs:
        name, spec = load(inp)
        if not spec.get("nodes") or not spec.get("agents"):
            print(f"{name}: skipped (a generator spec, or no people)")
            continue
        w = M.world_of(spec)
        rep = M.analyse(w, horizon=a.horizon or int(spec.get("days") or 0) or None)
        d = os.path.join(a.out, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "report.json"), "w") as f:
            json.dump(rep, f, indent=1, default=str)
        with open(os.path.join(d, "summary.md"), "w") as f:
            f.write(summary(name, rep))
        if a.figures:
            svgs = {"bounds": FG.bounds(rep, f"{name}: carrying capacity"), "costs": FG.costs(rep, f"{name}: what each level costs"),
                    "region": FG.region(w, rep, "standing", f"{name}: the land as it stands"),
                    "sensitivity": FG.sensitivity(FG.sensitivity_data(w), f"{name}: what moves capacity"),
                    "frontier": FG.frontier(SP.frontier(w, rep, "worked"), f"{name}: expanding outward")}
            for nid, r in rep["nodes"].items():
                if nid != "(region)" and r["people"]:
                    svgs[f"node_{nid}"] = FG.node(w, rep, nid, "worked", f"{name}: {nid}, where the food comes from")
            paths = []
            for k, s in svgs.items():
                p = os.path.join(d, f"{k}.svg")
                with open(p, "w") as f:
                    f.write(s)
                paths.append(p)
            if a.png:
                FG.to_png(paths)
        print(f"{name}: {d}")


if __name__ == "__main__":
    main()
