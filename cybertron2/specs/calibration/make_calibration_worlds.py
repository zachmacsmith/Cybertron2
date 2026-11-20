"""The calibration suite's worlds (proposals/calibration_worlds.md; D2-228, D2-245; WORK W-54): twelve kinds of place, two seeds
each, generated with no people (no check of the suite needs them yet), for calibrating weather, the environment and the ecosystems
across a distribution of generated worlds. "Not to remove diversity but see that our calibrations generalize in relatively expected
ways ... Don't expect them to be the same." (Zach, 17 Nov.)

    python3 cybertron2/specs/calibration/make_calibration_worlds.py [--only w01,w06] [--seeds 1,2] [--jobs 4] [--force]

Each world is made from the generator's own configurations and settings (landgen/vocab.py CONFIGS, DEFAULTS) as the proposal's
table says, and where the table names no climate, the settings of the place it stands for (CLIMATE below, with the reason). No
generator setting is added: the high mountains are `upland and moor` with its moor raised (`configuration_params`) and a summit
laid on it; the lake country is `upland and moor` with a laid mere (a `lake` primitive, as brief 5's lake world) and the tarns the
upland system allows; the cold north is `plain` at 6 C.

Out, under `worlds/` (kept out of git: a world is remade exactly from its seed): `<id>_s<seed>.yaml`, `.cells.npz`, `.report.json`.
Into git, under `summary/`: `<id>_s<seed>.json`, a small summary of each world's land (land_summary below), and `index.json`, what
was made, which seeds were refused and why. A seed the generator refuses is replaced by the next spare seed, and the index says so.
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

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

WORLDS_DIR = os.path.join(HERE, "worlds")
SUMMARY_DIR = os.path.join(HERE, "summary")
SEEDS = (1, 2)                       # two seeds of each, so a seed's luck is not read as the world's nature
SPARE = (3, 4, 5, 6, 7, 8)           # tried in order if a seed is refused (the index records it)
YEAR_DAYS = 32                       # the engine's year in these worlds (season_days 8), as 02zzo's

# the base every suite world carries: the weather scheduler on (D4-109), the wild pack (the ecology and its history), no people
BASE = {"days": YEAR_DAYS, "calendar": {"season_days": YEAR_DAYS // 4}, "climate": {"era": "steady"}, "packs": ["wild"]}
GEN = {"settlements": 3, "household_size": 3, "warn_only": ["capacity"]}   # three villages give the water three reaches to read; their
                                                                           # land is sized for households no one generates


def _upland(moor_m: float, summit_m: float = 0.0, extra: list | None = None) -> dict:
    out = {"configuration": "upland and moor", "configuration_params": {"moor": {"height": moor_m}}}
    if summit_m:
        out["features"] = [{"kind": "massif", "name": "summit", "at": [0.78, 0.78], "r": 0.12, "height": summit_m}]
    if extra:
        out.setdefault("features", []).extend(extra)
    return out


# The twelve (the proposal's table). `climate` is rain a year on the windward lowland (mm), a year's mean at sea level (C) and the
# wind; `why` says where it came from: the proposal's table, or the place the world stands for (Met Office 1991-2020 station
# normals; see expectations.yaml's sources) where the table names none.
WORLDS = [
    {"id": "w01", "slug": "lowland", "name": "Lowland river country", "stands_for": "the English midlands",
     "generate": {"configuration": "plain", "rain_mm": 900.0, "temperature_c": 9.0}, "why": "the proposal's table"},
    {"id": "w02", "slug": "dry_east", "name": "Dry east", "stands_for": "East Anglia, a rain shadow",
     "generate": {"configuration": "plain", "rain_mm": 500.0, "temperature_c": 10.0, "wind": "east"}, "why": "the proposal's table"},
    {"id": "w03", "slug": "wet_west", "name": "Wet west, maritime", "stands_for": "Devon, west Wales",
     "generate": {"configuration": "coast", "rain_mm": 1400.0, "temperature_c": 10.0, "wild_shore": True},
     "why": "the proposal's table; wild_shore so the saltmarsh shore has a node"},
    {"id": "w04", "slug": "coast_mountains", "name": "Coast under mountains", "stands_for": "west Scotland's coast, the Lakes' west side",
     "generate": {"configuration": "coastal strip under mountains", "rain_mm": 1200.0, "temperature_c": 9.0, "wild_shore": True},
     "why": "the table names the configuration and the west wind; 1,200 mm and 9 C from west Scotland's coastal stations (Tiree, Dunstaffnage)"},
    {"id": "w05", "slug": "upland_moor", "name": "Upland and moor", "stands_for": "the Pennines",
     "generate": {"configuration": "upland and moor", "rain_mm": 950.0, "temperature_c": 9.0},
     "why": "the table names the configuration; 950 mm and 9 C at the Pennines' lowland foot (Bradford, Bingley)"},
    {"id": "w06", "slug": "high_mountains", "name": "High mountains", "stands_for": "the Highlands, a cold extreme (D2-227)",
     "generate": {**_upland(900.0, 300.0), "rain_mm": 1100.0, "temperature_c": 8.5},
     "why": "upland and moor with its moor raised from 560 to 900 m and a 300 m summit laid on it (existing settings: "
            "configuration_params and a massif), so the tops reach about 1,500 m (1,150 and 450 made 1,950 m); 1,100 mm and 8.5 C at a Highland glen's foot (Fort Augustus, Braemar)"},
    {"id": "w07", "slug": "cold_north", "name": "Cold north", "stands_for": "a northern lowland",
     "generate": {"configuration": "plain", "temperature_c": 6.0, "rain_mm": 800.0},
     "why": "the proposal's table (6 C); 800 mm as 02zzo's cold north (Aberdeenshire, Northumberland lowlands 700 to 850)"},
    {"id": "w08", "slug": "fen", "name": "Fen basin", "stands_for": "the Fens",
     "generate": {"configuration": "fen with islands", "rain_mm": 600.0, "temperature_c": 10.0},
     "why": "the table names the configuration; 600 mm and 10 C from the Fens' stations (Cambridge, Wisbech)"},
    {"id": "w09", "slug": "estuary", "name": "Estuary and saltmarsh", "stands_for": "the Severn, the Humber",
     "generate": {"configuration": "estuary and fens", "rain_mm": 750.0, "temperature_c": 10.0, "wild_shore": True},
     "why": "the table names the configuration; 750 mm and 10 C, between the Severn's (Bristol, 800) and the Humber's (Hull, 650)"},
    {"id": "w10", "slug": "chalk_clay", "name": "Chalk and clay", "stands_for": "the downs and their vale",
     "generate": {"configuration": "scarp and vale", "rain_mm": 800.0, "temperature_c": 10.0},
     "why": "the table names the configuration; 800 mm and 10 C from the downs' stations (Marlborough, Wantage)"},
    {"id": "w11", "slug": "sand_heath", "name": "Sand and heath", "stands_for": "the Brecks, the New Forest",
     "generate": {"configuration": "sand country", "rain_mm": 650.0, "temperature_c": 10.0},
     "why": "the table names the configuration; 650 mm and 10 C between the Brecks (Santon Downham, 600) and the New Forest (800)"},
    {"id": "w12", "slug": "lake_country", "name": "Lake country", "stands_for": "the Lakes, a mere district",
     "generate": {**_upland(560.0, 0.0, [{"kind": "lake", "name": "the_mere", "at": [0.5, 0.52], "r": 0.06}]),
                  "rain_mm": 1400.0, "temperature_c": 9.0, "lake_min_km2": 0.1},
     "why": "upland and moor with a laid mere (brief 5's lake primitive), its beck and outflow left to the land's own drainage "
            "(a laid beck into it was refused on 3 of 4 seeds: 'laid rivers run where laid'), tarns where the upland's hollows "
            "allow (lake_min_km2 0.1 lets the smaller ones stand); 1,400 mm and 9 C at a Lakeland valley foot (Keswick, Ambleside 1,450 to 1,800)"},
]
BY_ID = {w["id"]: w for w in WORLDS}


def spec_for(world: dict, seed: int) -> dict:
    gen = {**copy.deepcopy(GEN), **copy.deepcopy(world["generate"]), "seed": seed}
    return {"name": f"cal_{world['id']}_{world['slug']}", "seed": seed, **copy.deepcopy(BASE), "generate": gen}


def stem(world: dict, seed: int) -> str:
    return f"{world['id']}_{world['slug']}_s{seed}"


def world_path(world: dict, seed: int) -> str:
    return os.path.join(WORLDS_DIR, stem(world, seed) + ".yaml")


# ---------------------------------------------------------------------- the land summary (from the cells: what the land holds)
AWC_MM = {0: 70.0, 1: 170.0, 2: 150.0, 3: 140.0, 4: 300.0}      # landgen/write.py AWC_MM, by vocab texture code (mm a metre)
DRAIN = {0: 0.5, 1: 0.25, 2: 0.08, 3: 0.4, 4: 0.05}               # landgen/write.py DRAIN
TEXTURES = {0: "sand", 1: "loam", 2: "clay", 3: "chalk", 4: "peat"}


def _q(a, q):
    return round(float(np.percentile(a, q)), 1) if a.size else None


def _share(mask, of):
    n = int(of.sum())
    return round(float((mask & of).sum()) / n, 4) if n else 0.0


def group_stats(cells, m) -> dict:
    """What a group of cells holds: count, height, rain, warmth, wetness, soil water held (by texture and depth)."""
    if not m.any():
        return {"cells": 0}
    tex = cells["tex"][m]
    depth = np.clip(1 - cells["slope"][m] / 25.0, 0.1, 1.0) * 1.2                # physical.py's depth, as write.py's land.depth
    held = np.vectorize(AWC_MM.get)(tex) * depth
    return {"cells": int(m.sum()), "height m": _q(cells["h"][m], 50), "rain mm": _q(cells["rain"][m], 50) if "rain" in cells else None,
            "mean temp C": round(float(cells["temp"][m].mean()), 2), "wet": round(float(cells["wet"][m].mean()), 3),
            "held mm": round(float(held.mean()), 1), "drain": round(float(np.vectorize(DRAIN.get)(tex).mean()), 3)}


def probes(world_id: str, cells) -> dict:
    """Named groups of cells the ordering checks read (presentation choices, named as such: the generator has no such regions)."""
    h, c, x, y, tex = cells["h"], cells["c"], cells["x"], cells["y"], cells["tex"]
    land = ~cells["sea"] & ~cells["lake"] & (cells["river"] < 3)
    S = float(x.max())
    out = {"all land": land, "coast (within 3 km of the sea)": land & (c < 3.0),
           "inland lowland (over 10 km from the sea, under 150 m)": land & (c >= 10.0) & (h < 150),
           "tops (the highest 5% of land)": land & (h >= np.percentile(h[land], 95))}
    if world_id == "w04":                                                  # the range lies at x 0.4 of the window, 0.1 wide
        out["fells (the range, over 300 m)"] = land & (h >= 300) & (np.abs(x / S - 0.4) < 0.12)
        out["lee (east of the range, under 200 m)"] = land & (x / S > 0.56) & (h < 200)
        out["windward strip (west of the range, under 100 m)"] = land & (x / S < 0.3) & (h < 100) & ~cells["sea"]
    if world_id == "w10":
        out["downs (chalk)"] = land & (tex == 3)
        out["vale (clay)"] = land & (tex == 2)
    for t, nm in TEXTURES.items():
        out[f"on {nm}"] = land & (tex == t)
    return out


def land_summary(world_id: str, world: dict, cells) -> dict:
    """The land's numbers from its cells (no engine): the suite report reads these against the expectations."""
    sea, lake = cells["sea"], cells["lake"]
    tn = np.asarray(cells["terrain_names"])[cells["terrain"]]
    land = ~sea & (tn != "water")                                         # dry land (rivers of class 3 and lakes are water)
    notsea = ~sea
    eco, cover = cells["eco"].astype(str), cells["cover"].astype(str)
    km2 = float(cells.get("km", 0.15)) ** 2 if isinstance(cells, dict) else 0.0225
    h, sl, wet, f = cells["h"], cells["slope"], cells["wet"], cells["f"]
    out = {"land km2": round(float(land.sum()) * 0.0225, 1), "sea share": round(float(sea.mean()), 3)}
    out["height"] = {"median m": _q(h[land], 50), "p95 m": _q(h[land], 95), "max m": round(float(h[land].max()), 1),
                     "share over 300 m": _share(h >= 300, land), "share over 500 m": _share(h >= 500, land),
                     "share over 1000 m": _share(h >= 1000, land)}
    out["slope"] = {"median deg": _q(sl[land], 50), "p95 deg": _q(sl[land], 95), "share over 10 deg": _share(sl >= 10, land),
                    "share over 25 deg": _share(sl >= 25, land)}
    out["terrain"] = {t: _share(tn == t, notsea) for t in sorted(set(tn[notsea].tolist()))}
    out["floodplain share"] = out["terrain"].get("river floodplain", 0.0)
    out["terrace share"] = out["terrain"].get("river terrace", 0.0)
    near = f < 99
    out["low ground"] = {"share of land within 2 m of a river": _share(f < 2, land),
                         "share of land within 3 km of a river of class 2+ that is within 2 m of it": _share(f < 2, land & near)}
    out["wet ground share (wet >= 0.75)"] = _share(wet >= 0.75, land)
    out["texture"] = {nm: _share(cells["tex"] == t, land) for t, nm in TEXTURES.items()}
    depth = np.clip(1 - sl / 25.0, 0.1, 1.0) * 1.2
    held = np.vectorize(AWC_MM.get)(cells["tex"]) * depth
    out["soil"] = {"depth m mean": round(float(depth[land].mean()), 2), "held mm mean": round(float(held[land].mean()), 1),
                   "drain mean": round(float(np.vectorize(DRAIN.get)(cells["tex"][land]).mean()), 3),
                   "fertility mean": round(float(cells["fert"][land].mean()), 3)}
    out["cover"] = {k: _share(cover == k, notsea) for k in sorted(set(cover[notsea].tolist()))}
    out["ecosystem"] = {k: _share(eco == k, notsea) for k in sorted(set(eco[notsea].tolist()))}
    wood = np.isin(cover, ["forest"]) & land
    cold = land & (cells["temp"] < 4.6)                                    # vocab DEFAULTS treeline_c
    out["tree line"] = {"lowest land too cold for wood, m": _q(h[cold], 5) if cold.any() else None,
                        "highest wood (p99), m": _q(h[wood], 99) if wood.any() else None,
                        "land above the tree line share": _share(cold, land)}
    lab_n = 0
    from cybertron2.landgen import field as F
    lab, lab_n = F.components(lake)
    sizes = np.bincount(lab.ravel())[1:] * 0.0225 if lab_n else np.array([])
    out["water"] = {"lake share": _share(lake, notsea), "lakes": int(lab_n), "largest lake km2": round(float(sizes.max()), 2) if lab_n else 0.0,
                    "river km by class": {str(k): round(float((cells["river"] == k).sum()) * 0.15, 1) for k in (1, 2, 3)},
                    "springs": int(cells["spring"].sum())}
    out["climate (the generator's)"] = {"rain mm": {"median": _q(cells["rain"][land], 50), "p5": _q(cells["rain"][land], 5),
                                                     "p95": _q(cells["rain"][land], 95)} if "rain" in cells else None,
                                         "mean temp C": round(float(cells["temp"][land].mean()), 2),
                                         "coldest land C": round(float(cells["temp"][land].min()), 2)}
    out["probes"] = {k: group_stats(cells, m) for k, m in probes(world_id, cells).items()}
    out["nodes"] = node_summary(world, cells)
    out["water allocation"] = water_allocation(world, cells)
    return out


def node_summary(world: dict, cells) -> dict:
    place = cells["place"]
    out = {}
    for nid, n in world["nodes"].items():
        pids = list((n.get("parcels") or {}).keys())
        m = np.isin(place, pids)
        terr = [p.get("terrain") for p in n["parcels"].values()]
        out[nid] = {"name": n.get("name"), "kind": "village" if nid.startswith("s") else "other", "elevation": n.get("elevation"),
                    "rain_mm": n.get("rain_mm"), "xy": n.get("xy"), "sea km": round(float(cells["c"][m].min()), 1) if m.any() else None,
                    "terrain": max(set(terr), key=terr.count) if terr else None,
                    "mean temp C": round(float(cells["temp"][m].mean()), 2) if m.any() else None}
    return out


def water_allocation(world: dict, cells, field_km: float = 2.5) -> dict:
    """The generator's water for each village against the water within its reach (W-54's audit): water parcels and their cells
    against the river length, the lake area and the shore within field_km of its site (settle.allocate takes at most two cells)."""
    x, y, place = cells["x"], cells["y"], cells["place"]
    river, lake, sea = cells["river"], cells["lake"], cells["sea"]
    shore = sea & (_dilate(~sea))                                          # sea cells beside land
    out = {}
    for nid, n in world["nodes"].items():
        if not nid.startswith("s"):
            continue
        xy = n.get("xy")
        if not xy:
            continue
        d = np.hypot(x - xy[0], y - xy[1])
        reach = d <= field_km
        water = [pid for pid, p in n["parcels"].items() if p["cover"] == "water"]
        out[n["name"]] = {"water parcels": len(water), "water cells": int(np.isin(place, water).sum()),
                          "river km in reach (class 1+ / 2+)": [round(float((reach & (river >= 1)).sum()) * 0.15, 1),
                                                                 round(float((reach & (river >= 2)).sum()) * 0.15, 1)],
                          "lake km2 in reach": round(float((reach & lake).sum()) * 0.0225, 2),
                          "shore km in reach": round(float((reach & shore).sum()) * 0.15, 1)}
    return out


def _dilate(m):
    o = m.copy()
    o[1:] |= m[:-1]
    o[:-1] |= m[1:]
    o[:, 1:] |= m[:, :-1]
    o[:, :-1] |= m[:, 1:]
    return o


def load_cells(path: str) -> dict:
    z = np.load(path.replace(".yaml", ".cells.npz"), allow_pickle=True)
    cells = {k: z[k] for k in z.files}
    return cells


def with_rain(world: dict, cells: dict, spec: dict) -> dict:
    """The cells do not keep the generator's rain (mm a year); it is remade exactly from the seed by the land's own build."""
    if "rain" in cells:
        return cells
    from cybertron2.landgen import field as F, macro as M, physical as P
    from cybertron2.landgen.write import _conf
    conf = _conf(spec["generate"])
    g = F.grid(int(spec["generate"]["seed"]), conf["size_km"], conf["km"])
    mf = M.compose(g, M.primitives(conf))
    h = P.elevation(g, conf, mf)
    sea = P._sea(g, h, conf["sea_level"], mf)
    h = np.where((h < conf["sea_level"]) & ~sea, conf["sea_level"] + 0.5, h)
    P.climate(g, conf, h, sea, mf)                                       # the sweep over the land before valleys are cut, as build()
    cells["rain"] = mf["rain_mm"]
    return cells


# ---------------------------------------------------------------------- making
def make_one(world_id: str, seed: int, force: bool = False) -> dict:
    """Generate one world at one seed (no people); write it under worlds/ and its summary under summary/. Returns its index row."""
    from cybertron2.landgen import settle as ST, write as W
    world = BY_ID[world_id]
    os.makedirs(WORLDS_DIR, exist_ok=True)
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    path = world_path(world, seed)
    spec = spec_for(world, seed)
    row = {"world": world_id, "seed": seed, "path": os.path.relpath(path, ROOT)}
    t0 = time.time()
    if force or not os.path.exists(path):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                w_, cells, report = W.generate(copy.deepcopy(spec), None)
        except ST.Refused as e:
            return {**row, "ok": False, "refused": f"refused: {e}", "seconds": round(time.time() - t0, 1)}
        except Exception as e:  # noqa: BLE001 (a crash is a collapse finding, reported)
            return {**row, "ok": False, "refused": f"crashed: {type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:],
                    "seconds": round(time.time() - t0, 1)}
        if report["refused"]:
            return {**row, "ok": False, "refused": "refused by checks: " + ", ".join(report["refused"]),
                    "seconds": round(time.time() - t0, 1)}
        W.write(w_, cells, report, path, None)
    import yaml
    w_ = yaml.safe_load(open(path))
    rep = json.load(open(path.replace(".yaml", ".report.json")))
    cells = with_rain(w_, load_cells(path), spec)
    summ = {"world": world_id, "seed": seed, "name": world["name"], "stands for": world["stands_for"],
            "generate": spec["generate"], "settings why": world["why"],
            "generator checks": {k: v["ok"] for k, v in rep["checks"].items()},
            "land": land_summary(world_id, w_, cells)}
    with open(os.path.join(SUMMARY_DIR, stem(world, seed) + ".json"), "w") as f:
        json.dump(summ, f, indent=1, default=float)
    warn = [k for k, v in rep["checks"].items() if not v["ok"]]
    return {**row, "ok": True, "warnings": warn, "seconds": round(time.time() - t0, 1)}


def _job(args):
    return make_one(*args)


def make_all(ids=None, seeds=SEEDS, jobs: int = 4, force: bool = False) -> list:
    """Every world at its seeds; a refused seed is replaced by the next spare seed. Writes summary/index.json."""
    ids = ids or [w["id"] for w in WORLDS]
    rows = []
    todo = [(i, s, force) for i in ids for s in seeds]
    first = _map(todo, jobs)
    for i in ids:
        mine = [r for r in first if r["world"] == i]
        got = [r for r in mine if r["ok"]]
        rows += mine
        spares = [s for s in SPARE if s not in seeds]
        while len(got) < len(seeds) and spares:
            r = make_one(i, spares.pop(0), force)
            r["spare"] = True
            rows.append(r)
            if r["ok"]:
                got.append(r)
    idx_path = os.path.join(SUMMARY_DIR, "index.json")
    old = json.load(open(idx_path)) if os.path.exists(idx_path) else {"rows": []}
    keep = [r for r in old.get("rows", []) if r["world"] not in ids]
    index = {"made by": "cybertron2/specs/calibration/make_calibration_worlds.py", "seeds": list(seeds), "spare": list(SPARE),
             "rows": sorted(keep + rows, key=lambda r: (r["world"], r["seed"]))}
    with open(idx_path, "w") as f:
        json.dump(index, f, indent=1)
    return rows


def _map(todo, jobs):
    if jobs <= 1:
        return [_job(t) for t in todo]
    import multiprocessing as mp
    with mp.get_context("fork").Pool(jobs) as pool:
        return pool.map(_job, todo)


def made(index_path: str = os.path.join(SUMMARY_DIR, "index.json")) -> list:
    """[(world id, seed)] of the worlds made, two a world (spares where a seed was refused)."""
    rows = json.load(open(index_path))["rows"]
    out = []
    for w in WORLDS:
        ok = [r for r in rows if r["world"] == w["id"] and r["ok"]]
        out += [(w["id"], r["seed"]) for r in sorted(ok, key=lambda r: (bool(r.get("spare")), r["seed"]))[:len(SEEDS)]]
    return out


def main(argv=None):
    a = list(argv if argv is not None else sys.argv[1:])
    ids = a[a.index("--only") + 1].split(",") if "--only" in a else None
    seeds = tuple(int(s) for s in a[a.index("--seeds") + 1].split(",")) if "--seeds" in a else SEEDS
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4
    rows = make_all(ids, seeds, jobs, "--force" in a)
    for r in rows:
        print(r["world"], r["seed"], "ok" if r["ok"] else r.get("refused"), r.get("warnings", ""), f"{r['seconds']}s",
              "(spare)" if r.get("spare") else "", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
