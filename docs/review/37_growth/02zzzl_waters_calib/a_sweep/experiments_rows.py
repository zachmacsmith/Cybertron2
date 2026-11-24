"""W-108 sweep, section 5 (a): the runs' rows changed as data only, run through the engine's own runs.advance on each world (a copy of
`kinds.RUNS` swapped in for the run and put back; no engine code changed). The base is the fix arm (sweep_world.runs reseed=True:
the up-runs' spawning stretches the build left empty reseeded), so a row's effect is not hidden by the history's lost spawners.

    python3 docs/review/37_growth/02zzzl_waters_calib/a_sweep/experiments_rows.py [--jobs 4] [--years 6]

Variants (each a copy of RUNS with one change):
- base: today's rows;
- eel_dry1: the eels' cue `rain_after_dry` 1 dry day before the heavy rain (was 2);
- eel_spate: the eels' cue a spate of 1.2 x the mean (as the salmon's), in place of rain after dry days;
- eel_wide: the eels' window autumn and the first half of winter (as the salmon's);
- lamprey_river: the lampreys spawn along the whole river by km (`spawn: river`, as the salmon), not in the head waters only,
  with no reseed (so the history's lost spawners are not refilled: does the row alone fix it);
- set_nights: today's rows on set nights (`weather=False`), the live worlds' way, over the same six years.
Writes data/exp_rows/<id>.json: per settled village on a river, per variant, the run years (analyse.run_years's fields, no days).
"""
from __future__ import annotations

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep_world as SW  # noqa: E402
import analyse as AN  # noqa: E402

OUT = os.path.join(HERE, "data", "exp_rows")


def variants():
    from cybertron2.wild import kinds as WK
    base = copy.deepcopy(WK.RUNS)
    v = {"base": (base, True, True)}
    x = copy.deepcopy(base); x["eel"]["cue"] = {"rain_after_dry": 1}; v["eel_dry1"] = (x, True, True)
    x = copy.deepcopy(base); x["eel"]["cue"] = {"spate": 1.2}; v["eel_spate"] = (x, True, True)
    x = copy.deepcopy(base); x["eel"]["seasons"] = {2: (0, 7), 3: (0, 3)}; v["eel_wide"] = (x, True, True)
    x = copy.deepcopy(base); x["lamprey"]["spawn"] = "river"; v["lamprey_river"] = (x, True, False)
    v["set_nights"] = (base, False, True)
    return v


def one(wid, years=6):
    from cybertron2.engine import wild as WL
    raw = SW.load(wid)
    raw.setdefault("agents", {})
    if wid != "eelmouth":
        raw["packs"] = sorted(set(raw.get("packs") or []) | {"wild", "water"})
    w = SW.build(raw)
    cen = SW.census(w, raw, "generated")
    settled = {n for n, v in cen["villages"].items() if not v.get("wild")}
    out = {"id": wid, "variants": {}}
    for name, (rows, cued, reseed) in variants().items():
        if name == "lamprey_river":                                         # the seed of a new spawning layout: as the build would
            from cybertron2.wild import kinds as WK, runs as RU             # (RU.seed at the world's making), then no reseed
            saved = copy.deepcopy(WK.RUNS)
            WK.RUNS.clear(); WK.RUNS.update(copy.deepcopy(rows))
            try:
                m = WL.model(w)
                st0 = copy.deepcopy(w.s["wild"]["state"])
                R = RU.state(st0)
                keep = R["spawned"].get("lamprey") or {}
                nt = RU.net(m)
                sp = {g: round(float(rows["lamprey"]["return"]["seed_km"]) * nt.km[g], 4) for g in nt.spawns("river", "river")}
                for g, x in keep.items():
                    sp[g] = x
                w.s["wild"]["state"], orig = st0, w.s["wild"]["state"]
                R["spawned"]["lamprey"] = sp
            finally:
                WK.RUNS.clear(); WK.RUNS.update(saved)
            r = SW.runs(w, years, cued=cued, run_rows=rows, reseed=False)
            w.s["wild"]["state"] = orig
        else:
            r = SW.runs(w, years, cued=cued, run_rows=rows, reseed=reseed)
        ry = AN.run_years({"x": r, "census_maker": cen}, "x")
        out["variants"][name] = [{"village": n, "kind": k, "year": yr, **{x: rec[x] for x in rec if x != "food_by_day"}}
                                 for (n, k, yr), rec in sorted(ry.items()) if n in settled]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, wid + ".json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    return wid


def main(argv=None):
    a = list(argv if argv is not None else sys.argv[1:])
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4
    years = int(a[a.index("--years") + 1]) if "--years" in a else 6
    ids = SW.ids_all()
    import multiprocessing as mp
    with mp.get_context("fork").Pool(jobs) as pool:
        for x in pool.starmap(one, [(i, years) for i in ids]):
            print(x, flush=True)


if __name__ == "__main__":
    main()
