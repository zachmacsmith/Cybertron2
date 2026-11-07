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
              "Work is in units (a person gives 5 to 7 a day). Equipment and houses are built once; their work includes their materials'.", "",
              "| Level | Fed | Food a plot a year | Food a unit of work | Food work a year | Equipment, once | Houses, once | Tools worn a year (work) | Waste |",
              "|---|---|---|---|---|---|---|---|---|"]
    for l, v in reg["levels"].items():
        a = v["at_supported"]
        c = a["capital"]
        eq = ", ".join(f"{i['n']} {i['what']}" for i in c["items"] if i["what"] not in ("medium room (timber)", "hearth", "beds"))
        lines.append(f"| {WORDS[l]} | {v['supported']:g} | {a['land']['field_food_a_plot'] or '-'} | {a['recurring']['food_a_unit'] or '-'} | "
                     f"{a['recurring']['food_work']:g} | {c['equipment']:g}" + (f" ({eq})" if eq else "") +
                     f" | {c['houses']:g} | {c['tool_work_a_year']:g} | {a['waste_share']:.0%} |")
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
        from cybertron2.capacity import ladder as LD
        home = max((k for k in rep["nodes"] if k != "(region)"), key=lambda k: rep["nodes"][k]["people"])
        rungs = LD.climb(w, {home})
        rep["ladder"] = {"node": home, "rungs": rungs}
        with open(os.path.join(d, "report.json"), "w") as f:
            json.dump(rep, f, indent=1, default=str)
        lines = ["", f"**The ladder of practice ({home}, {rep['nodes'][home]['people']} people):** from bare, one change at a time, "
                 "each the most people fed for its cost.", "",
                 "Capital is built once (units of work, with materials'); ongoing work is each year's running, tools worn and upkeep. "
                 "Steps are ranked by people fed for the extra ongoing work plus the capital spread over one year; the two are reported apart.", "",
                 "| Change | Fed | Ratio | Capital added, once | Equipment held | Ongoing work a year | Ongoing a head | Share of their work (at the people there) | Food a unit of work | Food a plot a year |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rungs:
            lines.append(f"| {r['change']} | {r['supported']:g} | {r['ratio']} | {r.get('capital_added', '-')} | {r['equipment']:g}"
                         + (f" ({', '.join(r['items'])})" if r["items"] else "") + f" | {r['ongoing']:g} | {r['ongoing_a_head']} | "
                         f"{r['ongoing_share_here'] if r['ongoing_share_here'] is not None else '-'} | {r['food_a_unit']} | {r['food_a_plot']} |")
        with open(os.path.join(d, "summary.md"), "w") as f:
            f.write(summary(name, rep) + "\n".join(lines) + "\n")
        if a.figures:
            svgs = {"bounds": FG.bounds(rep, f"{name}: carrying capacity"), "costs": FG.costs(rep, f"{name}: what each level costs"),
                    "region": FG.region(w, rep, "standing", f"{name}: the land as it stands"),
                    "sensitivity": FG.sensitivity(FG.sensitivity_data(w), f"{name}: what moves capacity"),
                    "frontier": FG.frontier(SP.frontier(w, rep, "worked"), f"{name}: expanding outward"),
                    "ladder": FG.ladder(rungs, rep["nodes"][home]["people"], f"{name}: the ladder of practice at {home}")}
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
