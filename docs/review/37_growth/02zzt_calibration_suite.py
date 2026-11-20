"""02zzt: the calibration suite's report (proposals/calibration_worlds.md, "The checks"; D2-228, D2-245; WORK W-54).

    python3 docs/review/37_growth/02zzt_calibration_suite.py [--only w01,w08] [--years 20] [--jobs 4] [--make]

On every world of the suite (cybertron2/specs/calibration/make_calibration_worlds.py; `--make` makes any missing), offline and with
no people and no model calls:
- **ranges**: every measure against its range in cybertron2/specs/calibration/expectations.yaml, a row per world and seed, out of
  range marked; weather in two columns, the generator's own climate and the engine's weather (climate.py, D4-109);
- **orderings**: the pairs that must come out in a known order whatever the constants (expectations.yaml `orderings`);
- **collapse**: no system refuses or crashes on any world (the generator, the engine's world, its weather, the wild layer's
  history, 02zzn's water); no stock runs away and no kind dies out where its range includes the land (the ecology stepped on
  for `years` more years after its history, as engine/wild.py's own history does; the water on 02zzn's two clocks);
- **the generator audit** (W-54) is written by hand in the .md, from these tables.

The engine's weather reads only a node's height (02zzo), so its column is expected to miss every dry, cold and coastal
expectation until climate from the land (OPEN Q-56) is built: the report marks that as the known gap, not a fault of the suite.

Writes 02zzt_calibration_suite.json, and the tables into 02zzt_calibration_suite.md between its `suite:begin` and `suite:end`
markers (the hand-written audit outside them is kept).
"""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import math
import os
import sys
import time
import traceback
from collections import Counter

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
CAL = os.path.join(ROOT, "cybertron2", "specs", "calibration")
sys.path.insert(0, CAL)

import make_calibration_worlds as MK  # noqa: E402

_spec = importlib.util.spec_from_file_location("proto", os.path.join(HERE, "02zzn_environment_prototype.py"))
PR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PR)

EXP = yaml.safe_load(open(os.path.join(CAL, "expectations.yaml")))
OUT_JSON = os.path.join(HERE, "02zzt_calibration_suite.json")
OUT_MD = os.path.join(HERE, "02zzt_calibration_suite.md")
YEARS = 20
MARGIN = 0.05                               # an ordering passes only if its pair is apart by more than 5% of the larger
ECO_YEARS = 60                              # the ecology stepped on after its 10-year history: a bear takes about 50 to settle
SPIN = 32                                   # an engine year of spin-up before measuring (02zzo)
PACE = 365.0 / MK.YEAR_DAYS                 # two clocks: the seasonal stores move this many days an engine day (02zzn)
FIELD_OK = {"river floodplain", "river terrace", "clay vale", "lowland loam", "sandy ground", "chalk down", "hills", "coast"}  # vocab
WEATHER_KEYS = ["rain_mm", "wet_days", "mean_temp_c", "winter_c", "summer_c", "frost_nights", "snow_lying_days", "wind_ms", "gale_days"]
GEN_WEATHER = {"rain_mm", "mean_temp_c"}    # all the generator's climate holds
LAND_KEYS = ["max_height_m", "share_over_500m", "share_over_10deg", "floodplain_share", "terrace_share", "low_ground_share",
             "wet_ground_share", "treeline_m", "above_treeline_share"]
WATER_KEYS = ["spates_a_year", "floods_a_year", "flood_years", "low_water_share", "ice_days"]
ECO_KEYS = ["woodland_share", "heath_share", "moor_share", "wetland_share", "saltmarsh_share", "lake_share"]
ECO_GROUPS = {"heath_share": ["lowland heath"], "moor_share": ["moor", "blanket bog"],
              "wetland_share": ["fen", "reedbed", "alder carr", "wet grassland"], "saltmarsh_share": ["saltmarsh"]}
# probe names in expectations.yaml's orderings -> the maker's probe groups
PROBE = {"coast": "coast (within 3 km of the sea)", "fells": "fells (the range, over 300 m)", "lee": "lee (east of the range, under 200 m)",
         "tops": "tops (the highest 5% of land)", "downs": "downs (chalk)", "vale": "vale (clay)", "on sand": "on sand",
         "windward": "windward strip (west of the range, under 100 m)", "fells facing the wind": "fells, the slopes facing the wind",
         "fells facing away": "fells, the slopes facing away"}
ENGINE_PROBES = ("coast", "fells", "lee", "tops", "windward")


# ---------------------------------------------------------------------- the engine's weather, put per real year
def weather_stats(w, nodes_days: dict, spin: int) -> dict:
    """nodes_days: {node: [env dicts by day]}; the mean over the nodes of each measure (a real year's)."""
    from cybertron2.engine import climate as CL
    rows = []
    for nid, e in nodes_days.items():
        e = e[spin:]
        t = np.array([x["temp"] for x in e])
        lo = np.array([x["low"] for x in e])
        r = np.array([x["rain"] for x in e])
        wd = np.array([x["wind"] for x in e])
        st = np.array([x.get("storm", 0.0) for x in e])
        season = [w.calendar(spin + i)["season"] for i in range(len(e))]
        by = {s: float(np.mean([t[i] for i in range(len(e)) if season[i] == s])) for s in ("spring", "summer", "autumn", "winter")}
        rows.append({"rain_mm": float(r.mean()) * 365, "wet_days": float((r >= 1).mean()) * 365, "mean_temp_c": float(t.mean()),
                     "winter_c": by["winter"], "summer_c": by["summer"], "frost_nights": float((lo < 0).mean()) * 365,
                     "wind_ms": float(wd.mean()), "gale_days": float((wd >= 17).mean()) * 365,
                     "storm_days": float((st > 0).mean()) * 365, "snow_falling_days": float(((r > 0) & (t <= 1.5)).mean()) * 365,
                     "heavy_rain_days": float((r >= 10).mean()) * 365,
                     "rain a year, coefficient of variation between years": float(np.std(yr := r[:len(r) // 32 * 32].reshape(-1, 32).mean(1))
                                                                                  / max(1e-9, np.mean(yr)))})
    return {k: round(float(np.mean([r_[k] for r_ in rows])), 2) for k in rows[0]} if rows else {}


def env_days(w, nodes, days) -> dict:
    from cybertron2.engine import climate as CL
    return {n: [CL.env(w, n, d) for d in range(days)] for n in nodes}


def snow_days(series, pace=PACE) -> float:
    """Days a real year with snow lying (over 5 mm water), by 02zzn's snow rule on the two clocks, from one node's weather."""
    snow, m, lying = 0.0, None, 0
    for e in series[SPIN:]:
        dr, t = float(e["rain"]), float(e["temp"])
        m = dr if m is None else m + (dr - m) / 6.0
        if t <= PR.P["snow_c"]:
            snow += pace * min(dr, m)
        snow -= min(snow, max(0.0, t) * PR.P["melt_per_c"] * pace)
        lying += snow > 5
    return round(lying / max(1, len(series) - SPIN) * 365, 1)


def ice_days(series) -> float:
    W = {"n": [{"temp": e["temp"]} for e in series]}
    ice = PR.ice_series(W, "n", len(series))[SPIN:]
    return round(sum(1 for x in ice if x >= 5) / max(1, len(ice)) * 365, 1)


def probe_world(spec: dict, cells: dict, world_id: str):
    """The engine's weather at named places of the land: a copy of the world without the wild pack whose first nodes stand at the
    probes' heights and centres (as 02zzo's heights did; the engine's weather reads a node's height and its position only)."""
    from cybertron2.engine.world import World
    groups = MK.probes(world_id, cells)
    want = [(k, groups[PROBE[k]]) for k in ENGINE_PROBES if PROBE[k] in groups and groups[PROBE[k]].any()]
    sp = copy.deepcopy(spec)
    sp["packs"] = []
    sp.setdefault("agents", {})
    nodes = sorted(sp["nodes"])
    out = {}
    for (name, m), nid in zip(want, nodes):
        sp["nodes"][nid]["elevation"] = float(np.median(cells["h"][m]))
        sp["nodes"][nid]["xy"] = [round(float(cells["x"][m].mean()), 2), round(float(cells["y"][m].mean()), 2)]
        out[name] = nid
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(sp)
    return w, out


# ---------------------------------------------------------------------- the water on two clocks (02zzn), at the villages
def water(w, cells, years) -> dict:
    R, order = PR.reaches(w)
    days = SPIN + 32 * years
    W = PR.weather(w, sorted({r["node"] for r in R.values()}), days)
    Q, soil, snow = PR.simulate(R, order, W, days, pace=PACE)
    out, bad = {}, []
    for n, q in Q.items():
        if not np.all(np.isfinite(q)) or (q < 0).any():
            bad.append(f"{n}: flow not finite or below 0")
        s = soil[n]
        if not np.all(np.isfinite(s)) or s.min() < -1e-6 or s.max() > 1 + 1e-6:
            bad.append(f"{n}: soil outside its bucket")
    for n in R:
        if not n.startswith("v:"):
            continue
        v = n[2:]
        if not v.startswith("s"):
            continue
        q = Q[n][SPIN:]
        med = float(np.median(q))
        if med <= 0:
            out[v] = {"no flow": True}
            continue
        r = q / med
        bands = Counter(PR.band(x) for x in r)
        onsets, prev = Counter(), None
        for x in r:
            b = PR.band(x)
            if b in ("spate", "flood") and b != prev:
                onsets[b] += 1
            prev = b
        stage = PR.P["stage_m"] * (np.maximum(r, 1e-9) ** 0.4 - 1)
        pids = list((w.spec["nodes"][v].get("parcels") or {}).keys())
        m = np.isin(cells["place"], pids) & (cells["river"] == 0) & ~cells["sea"] & ~cells["lake"]
        fs = cells["f"][m]
        flooded = float(np.mean([(fs < st_).mean() for st_ in stage])) if fs.size else 0.0
        out[v] = {"spates_a_year": round(onsets["spate"] / years, 2), "floods_a_year": round(onsets["flood"] / years, 2),
                  "flood_years": round(float(np.mean([stage[32 * y:32 * y + 32].max() > 1.0 for y in range(years)])), 2),
                  "low_water_share": round((bands["low"] + bands["dry"]) / len(r), 3),
                  "ice_days": ice_days(W[R[n]["node"]]),
                  "snow_lying_days": round(int(np.sum(snow[n][SPIN:] > 5)) / len(r) * 365, 1),
                  "flooded": round(flooded, 4), "land within 1 m of a river": round(float((fs < 1).mean()), 4) if fs.size else 0.0, "peak / median": round(float(r.max()), 1),
                  "dry soil share (under a quarter)": round(float((soil[n][SPIN:] < 0.25).mean()), 3),
                  "yearly flow, coefficient of variation": round(float(np.std(yr := [q[32 * y:32 * y + 32].mean() for y in range(years)])
                                                                       / max(1e-9, np.mean(yr))), 2)}
    # a store that runs away drifts: the same ten years of weather four times over must give the same flows the second and the
    # fourth time (the yearly flow at every reach within 10%)
    k = min(10, years) * 32
    Wc = {nd: [ser[SPIN + (d % k)] for d in range(4 * k)] for nd, ser in W.items()}
    Qc, _, _ = PR.simulate(R, order, Wc, 4 * k, pace=PACE)
    drift = {}
    for n, q in Qc.items():
        a_, b_ = q[k:2 * k].mean(), q[3 * k:4 * k].mean()
        if a_ > 0:
            drift[n] = b_ / a_
            if not 0.9 <= drift[n] <= 1.1:
                bad.append(f"{n}: the same ten years gave {a_:.3g} the second time and {b_:.3g} the fourth")
    return {"villages": out, "collapse": bad, "reaches": len(R),
            "drift (4th / 2nd pass of the same weather), range": [round(min(drift.values()), 3), round(max(drift.values()), 3)] if drift else None}


# ---------------------------------------------------------------------- the ecology after its history, stepped on
def ecology(w, years) -> dict:
    from cybertron2.engine import wild as WL
    from cybertron2.wild import ecology as EC, runs as RU
    m = WL.model(w)
    st = copy.deepcopy(w.s["wild"]["state"])
    Y = w.year_days()
    off = (WL.HISTORY_AHEAD_YEARS + 30) * Y                                 # days of the climate past the history's
    nodes = sorted(set(m.nodes))
    k0 = WL.eco_day(w, 0)
    rivers = RU.active(m)
    tot = {k: [] for k in m.names}
    land_km2 = float(np.sum(m.km2))
    def totals():
        return {k: float(np.sum(np.array(st["pop"][k]) * m.km2)) for k in m.names}
    first = totals()
    dens0 = {k: np.array(st["pop"][k], dtype=float) for k in m.names}
    wx_next = WL.weather(w, nodes, off)
    for d in range(years * Y):
        wx = wx_next
        wx_next = WL.weather(w, nodes, off + d + 1)
        EC.step(m, st, k0 + d, wx, WL.draws(w, k0 + d, "suite"), history=True)
        if rivers:
            RU.advance(m, st, k0 + d, wx, wx_next, weather=WL._runs_cued(w))
        if d % (Y // 4) == 0:
            for k, v in totals().items():
                tot[k].append(v)
    yearly = {k: [max(v[4 * y:4 * y + 4]) for y in range(years)] for k, v in tot.items()}   # each year's highest season (migrants)
    bad, gone, kinds, slow, high = [], [], {}, [], []
    for k in m.names:
        yv = np.array(yearly[k])
        suit = float(np.max(m.suit[k]))
        f5, l5 = float(yv[:5].mean()), float(yv[-5:].mean())
        dens = yv[-1] / land_km2
        ref = float(m.kinds[k].get("ref") or 0) * float(m.kinds[k].get("d0") or 1)
        rising = yv[-1] > 1.1 * yv[-11] if len(yv) > 11 else False
        if not np.all(np.isfinite(yv)):
            bad.append(f"{k}: not finite")
        elif f5 > 0 and l5 > 3 * f5 and rising:
            bad.append(f"{k}: ran from {f5:.3g} to {l5:.3g} head over the window and still rising")
        if f5 > 0 and l5 > 2 * f5 and not rising:
            slow.append(f"{k}: settles at {l5 / f5:.1f} x where the history left it")
        if ref and dens > 3 * ref:
            high.append(f"{k}: settles at {dens:.3g} a km2, {dens / ref:.1f} x its reference density {ref:g}")
        if suit >= 0.2 and dens < 1e-4 and not m.kinds[k]["migrant"]:
            gone.append(f"{k}: suitability up to {suit:.2f}, {dens:.2g} a km2 at the end")
        where = dens0[k] / max(1e-12, dens0[k].sum())
        kinds[k] = {"head a km2 (after the history)": round(first[k] / land_km2, 4), "head a km2 (after the suite's years)": round(dens, 4),
                    "head a km2 (each year's highest season, mean)": round(float(yv.mean()) / land_km2, 4),
                    "last 5 / first 5 years": round(l5 / f5, 2) if f5 > 0 else None, "suitability max": round(suit, 2),
                    "where": {fe: round(float(np.sum(where * m.f[fe])), 3) for fe in ("wood", "grassy", "heath", "wet", "water", "farm")}}
    return {"kinds": kinds, "runaway": bad, "died out in range": gone, "slow to settle (the history too short)": slow,
            "settles above three times its reference density": high, "years": years, "areas": int(m.n), "land km2": round(land_km2, 1)}


# ---------------------------------------------------------------------- one world
def run_one(args) -> dict:
    world_id, seed, years = args
    world = MK.BY_ID[world_id]
    path = MK.world_path(world, seed)
    out = {"world": world_id, "seed": seed, "collapse": [], "times": {}}
    t0 = time.time()
    sp = yaml.safe_load(open(path))
    sp.setdefault("agents", {})
    spec = MK.spec_for(world, seed)
    cells = MK.with_rain(sp, MK.load_cells(path), spec)
    summ = json.load(open(os.path.join(MK.SUMMARY_DIR, MK.stem(world, seed) + ".json")))
    out["land"] = summ["land"]
    from cybertron2.engine.world import World
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            w = World(copy.deepcopy(sp))                                   # the wild pack's 10-year history runs here
    except Exception as e:  # noqa: BLE001
        out["collapse"].append(f"engine world: {type(e).__name__}: {e}")
        out["trace"] = traceback.format_exc()[-1500:]
        return out
    out["times"]["world"] = round(time.time() - t0, 1)
    days = SPIN + MK.YEAR_DAYS * years
    villages = sorted(n for n in w.s["nodes"] if n.startswith("s"))
    try:
        E = env_days(w, sorted(w.s["nodes"]), days)
        out["engine weather"] = {"villages": weather_stats(w, {n: E[n] for n in villages}, SPIN)}
        types = Counter(e["type"] for n in villages for e in E[n][SPIN:])
        out["engine weather"]["types (share of days)"] = {k: round(v / sum(types.values()), 3) for k, v in sorted(types.items())}
        from cybertron2.engine import climate as CL
        labels = Counter(CL.label(w, n, d) for n in villages for d in range(SPIN, days))
        out["engine weather"]["labels (days a real year)"] = {k: round(v / sum(labels.values()) * 365, 1) for k, v in sorted(labels.items())}
        out["engine weather"]["villages"]["snow_lying_days"] = round(float(np.mean([snow_days(E[n]) for n in villages])), 1)
        pw, pn = probe_world(sp, cells, world_id)
        PE = env_days(pw, list(pn.values()), days)
        out["engine weather"]["probes"] = {k: {**weather_stats(pw, {nid: PE[nid]}, SPIN), "snow_lying_days": snow_days(PE[nid]),
                                               "ice_days": ice_days(PE[nid])} for k, nid in pn.items()}
    except Exception as e:  # noqa: BLE001
        out["collapse"].append(f"engine weather: {type(e).__name__}: {e}")
        out["trace"] = traceback.format_exc()[-1500:]
    out["times"]["weather"] = round(time.time() - t0, 1)
    try:
        out["water"] = water(w, cells, years)
        out["collapse"] += [f"water: {b}" for b in out["water"]["collapse"]]
    except Exception as e:  # noqa: BLE001
        out["collapse"].append(f"water: {type(e).__name__}: {e}")
        out["trace"] = traceback.format_exc()[-1500:]
    out["times"]["water"] = round(time.time() - t0, 1)
    try:
        out["ecology"] = ecology(w, ECO_YEARS)
        out["collapse"] += [f"ecology: {b}" for b in out["ecology"]["runaway"]]
    except Exception as e:  # noqa: BLE001
        out["collapse"].append(f"ecology: {type(e).__name__}: {e}")
        out["trace"] = traceback.format_exc()[-1500:]
    out["times"]["ecology"] = round(time.time() - t0, 1)
    out["villages"] = {n: {"name": sp["nodes"][n]["name"], "elevation": sp["nodes"][n].get("elevation"),
                           "rain_mm": sp["nodes"][n].get("rain_mm"), **(out["land"]["nodes"].get(n) or {})} for n in villages}
    return out


# ---------------------------------------------------------------------- reading the measures
def gen_weather(r) -> dict:
    v = [x for x in r["villages"].values()]
    return {"rain_mm": round(float(np.mean([x["rain_mm"] for x in v])), 0),
            "mean_temp_c": round(float(np.mean([x["mean temp C"] for x in v])), 2)}


def land_measures(r) -> dict:
    L = r["land"]
    tl = L["tree line"]
    return {"max_height_m": L["height"]["max m"], "share_over_500m": L["height"]["share over 500 m"],
            "share_over_10deg": L["slope"]["share over 10 deg"], "floodplain_share": L["floodplain share"],
            "terrace_share": L["terrace share"], "low_ground_share": L["low ground"]["share of land within 2 m of a river"],
            "wet_ground_share": L["wet ground share (wet >= 0.75)"], "treeline_m": tl["lowest land too cold for wood, m"],
            "above_treeline_share": tl["land above the tree line share"]}


def eco_measures(r) -> dict:
    L = r["land"]
    out = {"woodland_share": L["cover"].get("forest", 0.0), "lake_share": L["water"]["lake share"]}
    for k, names in ECO_GROUPS.items():
        out[k] = round(sum(L["ecosystem"].get(n, 0.0) for n in names), 4)
    out["field_ok_share"] = round(sum(v for t, v in L["terrain"].items() if t in FIELD_OK), 4)
    return out


def water_measures(r) -> dict:
    v = [x for x in ((r.get("water") or {}).get("villages") or {}).values() if "spates_a_year" in x]
    if not v:
        return {}
    keys = WATER_KEYS + ["flooded", "snow_lying_days", "peak / median"]
    return {k: round(float(np.mean([x[k] for x in v])), 3) for k in keys}


def verdict(val, rng) -> str:
    if rng is None:
        return "n/e" if val is not None else "-"
    if isinstance(rng, list) and val is None:
        return "MISSING"
    if val is None:
        return "-"
    lo, hi = rng
    return "ok" if lo - 1e-9 <= val <= hi + 1e-9 else ("LOW" if val < lo else "HIGH")


def ranges(results) -> list:
    """[{world, seed, measure, group, column, value, range, verdict}]."""
    rows = []
    for r in results:
        e = EXP["worlds"][r["world"]]
        if r.get("land") is None:
            continue
        gw = gen_weather(r)
        ew = ((r.get("engine weather") or {}).get("villages") or {})
        wm = water_measures(r)
        for k in WEATHER_KEYS:
            rng = e["weather"].get(k)
            if k in GEN_WEATHER:
                rows.append(dict(world=r["world"], seed=r["seed"], group="weather", measure=k, column="generator",
                                 value=gw.get(k), range=rng, verdict=verdict(gw.get(k), rng)))
            val = wm.get("snow_lying_days") if k == "snow_lying_days" and wm else ew.get(k)
            rows.append(dict(world=r["world"], seed=r["seed"], group="weather", measure=k, column="engine",
                             value=None if val is None else round(val, 2), range=rng, verdict=verdict(val, rng)))
        lm = land_measures(r)
        for k in LAND_KEYS:
            rng = e["land"].get(k)
            v = lm.get(k)
            if k == "treeline_m" and rng is None:
                vd = "ok" if v is None else "n/e"
            elif k == "treeline_m" and v is None:
                vd = "HIGH"                                                   # expected a tree line, the land never gets that cold
            else:
                vd = verdict(v, rng)
            rows.append(dict(world=r["world"], seed=r["seed"], group="land", measure=k, column="land", value=v, range=rng, verdict=vd))
        for k in WATER_KEYS:
            rng = e["water"].get(k)
            rows.append(dict(world=r["world"], seed=r["seed"], group="water", measure=k, column="engine weather",
                             value=wm.get(k), range=rng, verdict=verdict(wm.get(k), rng)))
        em = eco_measures(r)
        for k in ECO_KEYS:
            rng = e["ecosystems"].get(k)
            rows.append(dict(world=r["world"], seed=r["seed"], group="ecosystems", measure=k, column="land", value=em.get(k),
                             range=rng, verdict=verdict(em.get(k), rng)))
        present = {k for k, v in r["land"]["ecosystem"].items() if v >= 0.001}
        for k in e["ecosystems"].get("present") or []:
            rows.append(dict(world=r["world"], seed=r["seed"], group="ecosystems", measure=f"present: {k}", column="land",
                             value=round(r["land"]["ecosystem"].get(k, 0.0), 4), range=None, verdict="ok" if k in present else "ABSENT"))
        for k in e["ecosystems"].get("absent") or []:
            v = r["land"]["ecosystem"].get(k, 0.0)
            rows.append(dict(world=r["world"], seed=r["seed"], group="ecosystems", measure=f"absent: {k}", column="land",
                             value=round(v, 4), range=None, verdict="ok" if v == 0 else "PRESENT"))
        kinds = ((r.get("ecology") or {}).get("kinds") or {})
        for k in (e.get("wildlife") or {}).get("present") or []:
            d = (kinds.get(k) or {}).get("head a km2 (each year's highest season, mean)")
            rows.append(dict(world=r["world"], seed=r["seed"], group="wildlife", measure=f"present: {k}", column="engine",
                             value=d, range=None, verdict="ok" if d is not None and d >= 0.01 else "ABSENT"))
    return rows


def value_at(r, where, measure, column):
    """A measure at a place of a world, in a column (generator or engine), for the orderings."""
    if where == "land":                                                    # the land is the generator's: no engine column
        return {**land_measures(r), **eco_measures(r)}.get(measure) if column == "generator" else None
    if where == "villages":
        if column == "generator":
            if measure in GEN_WEATHER:
                return gen_weather(r).get(measure)
            if measure == "flooded":                                       # the land's stand-in: village land within 1 m of a river
                v = [x["land within 1 m of a river"] for x in ((r.get("water") or {}).get("villages") or {}).values()
                     if "land within 1 m of a river" in x]
                return round(float(np.mean(v)), 4) if v else None
            return None
        wm = water_measures(r)
        if measure in wm:
            return wm[measure]
        return ((r.get("engine weather") or {}).get("villages") or {}).get(measure)
    if column == "generator":
        g = r["land"]["probes"].get(PROBE.get(where, where)) or {}
        return {"rain_mm": g.get("rain mm mean"), "mean_temp_c": g.get("mean temp C"), "held_mm": g.get("held mm"),
                "wet": g.get("wet")}.get(measure)
    p = (((r.get("engine weather") or {}).get("probes") or {}).get(where) or {})
    return p.get(measure)


def orderings(results) -> list:
    by = {(r["world"], r["seed"]): r for r in results}
    out = []
    for o in EXP["orderings"]:
        (wa, pa, ma), (wb, pb, mb) = o["a"], o["b"]
        row = {"name": o["name"], "from": o["from"], "a": o["a"], "b": o["b"], "columns": {}}
        for col in ("generator", "engine"):
            vals = []
            for sa, sb in zip(sorted(s for w_, s in by if w_ == wa), sorted(s for w_, s in by if w_ == wb)):
                ra, rb = by.get((wa, sa)), by.get((wb, sb))
                if ra is None or rb is None:
                    continue
                ma_, mb_ = ma, mb
                stand = None
                if col == "generator" and o.get("generator_stand_in") and ma != "flooded" and value_at(ra, pa, ma, col) is None:
                    ma_ = mb_ = o["generator_stand_in"].split(",")[0]
                    stand = o["generator_stand_in"]
                va, vb = value_at(ra, pa, ma_, col), value_at(rb, pb, mb_, col)
                if va is None or vb is None:
                    continue
                lo_, hi_ = (vb, va) if stand and "more" in stand else (va, vb)
                ok = hi_ - lo_ > MARGIN * max(abs(lo_), abs(hi_), 1e-9)      # apart by more than the margin, not a tie
                vals.append({"seeds": [sa, sb], "a": va, "b": vb, "ok": bool(ok), "stand_in": stand})
            if vals:
                row["columns"][col] = {"pairs": vals, "passes": all(v["ok"] for v in vals)}
        out.append(row)
    return out


# ---------------------------------------------------------------------- the report
def fmt(v):
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.3g}" if abs(v) < 10 else f"{v:.0f}"
    return str(v)


def md_tables(results, rng_rows, ords) -> str:
    L = []
    worlds = [w["id"] for w in MK.WORLDS]
    names = {w["id"]: w["name"] for w in MK.WORLDS}
    seeds = sorted({r["seed"] for r in results})
    # counts
    cnt = Counter((x["column"] if x["group"] == "weather" else x["group"], x["verdict"]) for x in rng_rows)
    L.append("### Counts\n")
    L.append("| Group (column) | in range | out of range | missing | no expectation |")
    L.append("|---|---|---|---|---|")
    for g in ("generator", "engine", "land", "water", "ecosystems", "wildlife"):
        ok = cnt[(g, "ok")]
        bad = sum(v for (gg, vd), v in cnt.items() if gg == g and vd in ("LOW", "HIGH", "ABSENT", "PRESENT"))
        miss = cnt[(g, "MISSING")]
        ne = cnt[(g, "n/e")] + cnt[(g, "-")]
        label = {"generator": "weather (the generator's climate)", "engine": "weather (the engine's)",
                 "water": "water (two clocks, on the engine's weather)"}.get(g, g)
        L.append(f"| {label} | {ok} | {bad} | {miss} | {ne} |")
    L.append("")
    for group, keys, cols in (("weather", WEATHER_KEYS, ("generator", "engine")), ("land", LAND_KEYS, ("land",)),
                              ("water", WATER_KEYS, ("engine weather",)), ("ecosystems", ECO_KEYS, ("land",))):
        L.append(f"### {group.capitalize()}\n")
        if group == "weather":
            L.append("At the villages. Each cell: the generator's value / the engine's (the generator holds only rain and the mean);"
                     " the range below the name. **Bold** is out of range; the engine's misses on dry, cold and coastal worlds are the known"
                     " gap (it reads only height, 02zzo; climate from the land, OPEN Q-56).\n")
        hdr = "| World | seed | " + " | ".join(keys) + " |"
        L.append(hdr)
        L.append("|" + "---|" * (len(keys) + 2))
        for wid in worlds:
            e = EXP["worlds"][wid]
            sect = e["weather" if group == "weather" else group]
            L.append(f"| {wid} {names[wid]} (range) | | " + " | ".join(
                (f"{fmt(sect.get(k)[0])} to {fmt(sect.get(k)[1])}" if isinstance(sect.get(k), list) else "none") for k in keys) + " |")
            for s in seeds:
                cells = []
                for k in keys:
                    bits = []
                    for col in cols:
                        x = next((x for x in rng_rows if x["world"] == wid and x["seed"] == s and x["measure"] == k and x["column"] == col), None)
                        if x is None:
                            bits.append("-" if col != "generator" or k in GEN_WEATHER else "")
                            continue
                        t = fmt(x["value"])
                        bits.append(f"**{t}**" if x["verdict"] in ("LOW", "HIGH", "MISSING") else t)
                    cells.append(" / ".join(b for b in bits if b != "") if group == "weather" else bits[0])
                L.append(f"| | {s} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("### Kinds present and absent\n")
    L.append("Ecosystems expected present (on at least 0.1% of the land) or absent, and wild kinds expected present (0.01 a km² or"
             " more in the year's highest season, the mean over the suite's years after the wild layer's history; the runs' salmon and"
             " lamprey live in the runs' own store and are not counted here). Only the misses are listed.\n")
    L.append("| World | seed | missed |")
    L.append("|---|---|---|")
    for wid in worlds:
        for s in seeds:
            miss = [f"{x['measure']} ({x['verdict'].lower()}, {fmt(x['value'])})" for x in rng_rows
                    if x["world"] == wid and x["seed"] == s and x["verdict"] in ("ABSENT", "PRESENT")]
            L.append(f"| {wid} {names[wid]} | {s} | {'; '.join(miss) or 'none'} |")
    L.append("")
    L.append("### The ordering checks\n")
    L.append(f"Each pair must come out a < b on both seeds (seed 1 against seed 1, seed 2 against seed 2), apart by more than"
             f" {MARGIN:.0%} of the larger (a tie fails). Values a / b. Rain at a probe is its mean (the catchment's), not its median.\n")
    L.append("| Ordering | from | the generator | the engine |")
    L.append("|---|---|---|---|")
    for o in ords:
        cells = []
        for col in ("generator", "engine"):
            c = o["columns"].get(col)
            if not c:
                cells.append("n/a")
                continue
            vals = "; ".join(f"{fmt(p['a'])} / {fmt(p['b'])}" for p in c["pairs"])
            stand = " (stand-in: " + c["pairs"][0]["stand_in"] + ")" if c["pairs"][0].get("stand_in") else ""
            cells.append(("passes" if c["passes"] else "**fails**") + f": {vals}{stand}")
        L.append(f"| {o['name']} | {o['from']} | {cells[0]} | {cells[1]} |")
    L.append("")
    L.append("### Collapse\n")
    L.append("| World | seed | generator | engine world, weather, water, ecology | kinds died out where their range includes the land |")
    L.append("|---|---|---|---|---|")
    idx = json.load(open(os.path.join(MK.SUMMARY_DIR, "index.json")))["rows"]
    for wid in worlds:
        for s in seeds:
            r = next((r for r in results if r["world"] == wid and r["seed"] == s), None)
            gi = next((x for x in idx if x["world"] == wid and x["seed"] == s), {})
            gen = "made" if gi.get("ok") else (gi.get("refused") or "-")
            col = "; ".join(r["collapse"]) if r and r["collapse"] else ("none" if r else "not run")
            died = "; ".join((r.get("ecology") or {}).get("died out in range") or []) if r else ""
            L.append(f"| {wid} {names[wid]} | {s} | {gen} | {col} | {died or 'none'} |")
    L.append("")
    L.append("### The ecology settling\n")
    L.append("Not collapses: each kind's numbers stepped on for the suite's ecology years after the wild layer's 10-year history"
             " (engine/wild.py HISTORY_YEARS). `slow` counts world-seeds where a kind settles at more than twice where the history left"
             " it (the history is too short for it); `high` where its settled density over the whole land is over three times its"
             " reference density (kinds.py `ref` x `d0`, a density of good habitat, so the whole land should be under it).\n")
    L.append("| Kind | reference a km2 | settled a km2 over the land (min to max) | slow | high |")
    L.append("|---|---|---|---|---|")
    from cybertron2.wild import kinds as WK
    eco = [r["ecology"] for r in results if r.get("ecology")]
    for k, kd in WK.KINDS.items():
        d = [e["kinds"][k]["head a km2 (after the suite's years)"] for e in eco if k in e["kinds"]]
        ns = sum(1 for e in eco if any(x.startswith(k + ":") for x in e["slow to settle (the history too short)"]))
        nh = sum(1 for e in eco if any(x.startswith(k + ":") for x in e["settles above three times its reference density"]))
        ref = (kd.get("ref") or 0) * (kd.get("d0") or 1)
        L.append(f"| {k} | {fmt(float(ref)) if ref else 'runs'} | {fmt(min(d)) if d else '-'} to {fmt(max(d)) if d else '-'} | {ns} of {len(eco)} | {nh} of {len(eco)} |")
    refused = [x for x in idx if not x["ok"]]
    if refused:
        L.append("")
        L.append("Seeds refused by the generator: " + "; ".join(f"{x['world']} seed {x['seed']}: {x['refused']}" for x in refused))
    L.append("")
    return "\n".join(L)


def write_md(text: str) -> None:
    begin, end = "<!-- suite:begin (written by 02zzt_calibration_suite.py) -->", "<!-- suite:end -->"
    old = open(OUT_MD).read() if os.path.exists(OUT_MD) else f"# 02zzt: the calibration suite\n\n{begin}\n{end}\n"
    if begin not in old:
        old = old.rstrip() + f"\n\n{begin}\n{end}\n"
    a, rest = old.split(begin, 1)
    _, b = rest.split(end, 1)
    with open(OUT_MD, "w") as f:
        f.write(a + begin + "\n\n" + text + "\n" + end + b)


def main(argv=None):
    a = list(argv if argv is not None else sys.argv[1:])
    ids = a[a.index("--only") + 1].split(",") if "--only" in a else [w["id"] for w in MK.WORLDS]
    years = int(a[a.index("--years") + 1]) if "--years" in a else YEARS
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4
    if "--make" in a or not os.path.exists(os.path.join(MK.SUMMARY_DIR, "index.json")):
        MK.make_all(ids, jobs=jobs)
    todo = [(w, s, years) for w, s in MK.made() if w in ids]
    missing = [(w, s) for w, s, _ in todo if not os.path.exists(MK.world_path(MK.BY_ID[w], s))]
    if missing:
        MK.make_all(sorted({w for w, _ in missing}), jobs=jobs)
    if jobs > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(jobs) as pool:
            results = pool.map(run_one, todo)
    else:
        results = [run_one(t) for t in todo]
    for r in results:
        print(r["world"], r["seed"], r["times"], r["collapse"][:3], file=sys.stderr)
    rng_rows = ranges(results)
    ords = orderings(results)
    out = {"years": years, "results": results, "ranges": rng_rows, "orderings": ords}
    if os.path.exists(OUT_JSON) and set(ids) != {w["id"] for w in MK.WORLDS}:
        old = json.load(open(OUT_JSON))                                    # a partial run keeps the other worlds' results
        keep = [r for r in old["results"] if r["world"] not in ids]
        results = sorted(keep + results, key=lambda r: (r["world"], r["seed"]))
        rng_rows, ords = ranges(results), orderings(results)
        out = {"years": years, "results": results, "ranges": rng_rows, "orderings": ords}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1, default=float)
    write_md(md_tables(results, rng_rows, ords))
    return 0


if __name__ == "__main__":
    sys.exit(main())
