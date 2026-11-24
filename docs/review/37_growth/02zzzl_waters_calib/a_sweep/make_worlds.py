"""W-108 sweep, step 1: the generated environments (brief.md section 1). No people, no model calls.

    python3 docs/review/37_growth/02zzzl_waters_calib/a_sweep/make_worlds.py [--jobs 4] [--only id,id]

Three families, every one made by the land generator (cybertron2/landgen/write.generate) from its own configurations and settings:

- **cal**: the calibration suite's twelve kinds of place (cybertron2/specs/calibration/make_calibration_worlds.py WORLDS: the
  configuration, rain, warmth and wind each names), at seeds 1, 2 and 3, with three villages placed by the generator itself (GEN);
- **cfg**: the other callable configurations with rivers (landgen/vocab.py CONFIGS) at seed 1, the lowland's climate;
- **laid**: the water worlds' land (specs/make_water_worlds.py river_spec: one laid river from northern fells to the southern edge,
  wild upland above) with three villages pinned high, middle and low on it (`at` on its channel, as make_water_worlds.river_sites),
  the middle one with the generator's mill site; by the river's laid size (large, medium, a plain river), by climate (dry 500 mm,
  the default 900, wet 1,400) and by seed (5, Eelmouth's land, and 7).
- **lake**: the water worlds' lake world (make_water_worlds.lake_spec, Meresby on a laid mere) at seed 3, without people.

Each world gets the packs `wild` and `water` and the weather scheduler (climate `steady`), as every current world. The world files go
to worlds/ (not in git: remade exactly from the spec in index.json); the index (what was made, the spec, what was refused) to
data/worlds_index.json.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "cybertron2", "specs", "calibration"))

import numpy as np  # noqa: E402
import yaml  # noqa: E402

import make_calibration_worlds as MK  # noqa: E402
from cybertron2.specs import make_water_worlds as WW  # noqa: E402

WORLDS = os.path.join(HERE, "worlds")
DATA = os.path.join(HERE, "data")
BASE = {"days": 32, "calendar": {"season_days": 8}, "climate": {"era": "steady"}, "packs": ["wild", "water"]}
GEN = {"settlements": 3, "household_size": 3, "warn_only": ["capacity", "dependence", "chokepoint"]}
CFG_EXTRA = ["confluence plain", "river through a range", "basin in a ring of hills", "two valleys over a pass", "gated valley",
             "watershed divide", "settled lowland and frontier"]
LAID_AT_Y = {"Highpool": 0.74, "Middleham": 0.5, "Lowstrand": 0.26}   # make_water_worlds.RUNS_AT_Y: high, middle, low on the river
LAID = [  # (id, flow, rain_mm, temperature_c, seed)
    ("laid_large_s5", "large", 900.0, 9.0, 5), ("laid_large_s7", "large", 900.0, 9.0, 7),
    ("laid_large_dry_s5", "large", 500.0, 10.0, 5), ("laid_large_wet_s5", "large", 1400.0, 9.0, 5),
    ("laid_medium_s5", "medium", 900.0, 9.0, 5), ("laid_medium_s7", "medium", 900.0, 9.0, 7),
    ("laid_river_s5", "river", 900.0, 9.0, 5), ("laid_river_dry_s7", "river", 500.0, 10.0, 7),
]


def cal_specs() -> list:
    out = []
    for w in MK.WORLDS:
        for seed in (1, 2, 3):
            gen = {**copy.deepcopy(GEN), **copy.deepcopy(w["generate"]), "seed": seed}
            out.append({"id": f"{w['id']}_{w['slug']}_s{seed}", "family": "cal", "kind": w["name"], "configuration": gen.get("configuration"),
                        "spec": {"name": f"sweep_{w['id']}_s{seed}", "seed": seed, **copy.deepcopy(BASE), "generate": gen},
                        "require_lake": w.get("require_lake")})
    return out


def cfg_specs() -> list:
    out = []
    for c in CFG_EXTRA:
        gen = {**copy.deepcopy(GEN), "configuration": c, "rain_mm": 900.0, "temperature_c": 9.0, "seed": 1}
        slug = c.replace(" ", "_")
        out.append({"id": f"cfg_{slug}_s1", "family": "cfg", "kind": c, "configuration": c,
                    "spec": {"name": f"sweep_cfg_{slug}", "seed": 1, **copy.deepcopy(BASE), "generate": gen}})
    return out


def _laid_places(flow) -> dict:
    on = "big river" if flow == "large" else "river"
    out = {}
    for name in LAID_AT_Y:
        out[name] = {"households": 3, "on": on, "within": 1.5, "food_share": 0.6}
    out["Middleham"]["has"] = ["mill site"]
    return out


def laid_specs() -> list:
    out = []
    for wid, flow, rain, temp, seed in LAID:
        feats = copy.deepcopy(WW.river_spec(seed)["generate"]["features"])
        for f in feats:
            if f["kind"] == "river":
                f["flow"] = flow
        gen = {**copy.deepcopy(GEN), "seed": seed, "spacing_km": 11.0, "rain_mm": rain, "temperature_c": temp, "features": feats,
               "places": _laid_places(flow)}
        out.append({"id": wid, "family": "laid", "kind": f"laid {flow} river", "configuration": None, "flow": flow,
                    "spec": {"name": f"sweep_{wid}", "seed": seed, **copy.deepcopy(BASE), "generate": gen}})
    return out


def lake_specs() -> list:
    s = WW.lake_spec(3)
    gen = copy.deepcopy(s["generate"])
    gen["warn_only"] = GEN["warn_only"]
    return [{"id": "lake_meresby_s3", "family": "lake", "kind": "laid mere (Meresby)", "configuration": None,
             "spec": {"name": "sweep_lake", "seed": 3, **copy.deepcopy(BASE), "generate": gen}}]


def all_specs() -> list:
    return cal_specs() + cfg_specs() + laid_specs() + lake_specs()


def _sites(spec, at_y, min_class) -> dict:
    """make_water_worlds.river_sites, for any class: of the river cells of at least `min_class` near each latitude, the one draining
    the most land."""
    from cybertron2.landgen import write as W
    with contextlib.redirect_stdout(io.StringIO()):
        _, cells, _ = W.generate(copy.deepcopy(spec), people=False)
    x, y, r, acc = (np.asarray(cells[k]) for k in ("x", "y", "river", "acc"))
    S = float(np.max(x))
    big = r >= min_class
    out = {}
    for name, fy in at_y.items():
        for band in (1.0, 2.0, 3.0, 4.0):
            m = big & (np.abs(y - fy * S) <= band)
            if m.any():
                i = int(np.flatnonzero(m.ravel())[np.argmax(acc.ravel()[m.ravel()])])
                out[name] = [round(float(x.ravel()[i]), 2), round(float(y.ravel()[i]), 2)]
                break
    return out


def make_one(row) -> dict:
    from cybertron2.landgen import settle as ST, write as W
    t0 = time.time()
    spec = copy.deepcopy(row["spec"])
    out = {k: v for k, v in row.items() if k != "spec"}
    path = os.path.join(WORLDS, row["id"] + ".yaml")
    try:
        if row["family"] == "laid":
            at = _sites(spec, LAID_AT_Y, 3 if row["flow"] == "large" else 2)
            if len(at) < len(LAID_AT_Y):
                return {**out, "ok": False, "refused": f"no river cell near {sorted(set(LAID_AT_Y) - set(at))}"}
            for name, xy in at.items():
                spec["generate"]["places"][name]["at"] = xy
        with contextlib.redirect_stdout(io.StringIO()):
            world, cells, report = W.generate(copy.deepcopy(spec), None, people=False)
    except ST.Refused as e:
        return {**out, "ok": False, "refused": f"refused: {e}", "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {**out, "ok": False, "refused": f"crashed: {type(e).__name__}: {e}", "trace": traceback.format_exc()[-800:]}
    if report["refused"]:
        return {**out, "ok": False, "refused": "refused by checks: " + ", ".join(report["refused"])}
    need = row.get("require_lake")
    if need:
        S = float(np.max(cells["x"]))
        d = np.hypot(np.asarray(cells["x"]) - need["at"][0] * S, np.asarray(cells["y"]) - need["at"][1] * S)
        km2 = float((np.asarray(cells["lake"]) & (d <= need["km"])).sum()) * 0.0225
        if km2 < need["km2"]:
            return {**out, "ok": False, "refused": f"the laid mere holds {km2:.2f} km2 (wants {need['km2']})"}
    world.setdefault("agents", {})
    with open(path, "w") as f:
        yaml.safe_dump(world, f, sort_keys=False, width=200)
    with open(path.replace(".yaml", ".spec.json"), "w") as f:
        json.dump(spec, f, indent=1)
    return {**out, "ok": True, "path": os.path.relpath(path, ROOT), "spec": spec,
            "warnings": [k for k, v in report["checks"].items() if not v["ok"]], "seconds": round(time.time() - t0, 1)}


def main(argv=None):
    a = list(argv if argv is not None else sys.argv[1:])
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4
    rows = all_specs()
    if "--only" in a:
        keep = set(a[a.index("--only") + 1].split(","))
        rows = [r for r in rows if r["id"] in keep]
    os.makedirs(WORLDS, exist_ok=True)
    os.makedirs(DATA, exist_ok=True)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(jobs) as pool:
        res = pool.map(make_one, rows)
    # a refused calibration seed is replaced by the next spare seed (4, 5, 6), as the suite does
    for r in list(res):
        if r["ok"] or r["family"] != "cal":
            continue
        base = r["id"].rsplit("_s", 1)[0]
        wid = base.split("_")[0]
        for spare in (4, 5, 6):
            sid = f"{base}_s{spare}"
            if any(x["id"] == sid and x["ok"] for x in res):
                continue
            row = next(x for x in cal_specs() if x["id"].startswith(base))
            row = copy.deepcopy(row)
            row["id"] = sid
            row["spec"]["seed"] = spare
            row["spec"]["generate"]["seed"] = spare
            row["spare_for"] = r["id"]
            got = make_one(row)
            res.append(got)
            if got["ok"]:
                break
    idx_path = os.path.join(DATA, "worlds_index.json")
    old = json.load(open(idx_path))["rows"] if os.path.exists(idx_path) else []
    ids = {r["id"] for r in res}
    rows_out = sorted([r for r in old if r["id"] not in ids] + res, key=lambda r: r["id"])
    with open(idx_path, "w") as f:
        json.dump({"made by": os.path.relpath(__file__, ROOT), "rows": rows_out}, f, indent=1)
    for r in res:
        print(r["id"], "ok" if r["ok"] else r.get("refused"), r.get("seconds", ""), flush=True)


if __name__ == "__main__":
    main()
