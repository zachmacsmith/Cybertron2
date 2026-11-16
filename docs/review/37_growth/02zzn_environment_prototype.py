"""02zzn: an offline prototype of environment_systems.md's water phase on brief 5's river world (WORK W-49; 16 Nov 2026).

Not engine code. It reads only what the generator already writes (the world's areas, links and `down`, the parcels' land, the
cells' height above the river) and the engine's own weather by place (climate.py, D4-109), and runs the agreed fast stocks:
  soil water (a bucket per area: held water from texture and depth, rain in, evaporation by warmth, drainage by texture),
  snow (lies when cold, melts by degree-days), a slow groundwater store (baseflow),
  river level on reaches (each village's home and ring is one reach, wild river areas are reaches; runoff routed down `down`
  with a lag by river length), floods by height above the river, ice on the village's water by frost degree-days.
It reports how often each band of river level, flood, low water and ice comes, and the slow loop's test: the woods above
Saltwell cleared.

    python3 docs/review/37_growth/02zzn_environment_prototype.py <world.yaml> [years]

Every rate is a first value (calibrate), chosen to be physically plausible per day; the engine's year is 32 days, so a year's
totals are about a tenth of a real year's (02zp §15) and frequencies are per engine year.
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
import yaml

AWC = {"sand": 70.0, "loam": 170.0, "clay": 150.0, "chalk": 140.0, "peat": 300.0}     # landgen/write.py AWC_MM, mm a metre
DRAIN = {"sand": 0.5, "loam": 0.25, "clay": 0.08, "chalk": 0.4, "peat": 0.05}         # landgen/write.py DRAIN
P = {
    "depth_m": 1.0,          # soil depth where an area has none of its own (areas carry no depth)
    "pet_per_c": 0.15,       # potential evaporation, mm a day for each degree above 0 (about 550 mm a real year at 10 °C)
    "snow_c": 1.0,           # at or below this mean temperature rain falls as snow
    "melt_per_c": 3.0,       # snowmelt, mm a day for each degree above 0
    "beta": 3.0,             # HBV: share of the day's water that leaves the soil for the stores = (soil / capacity)^beta
    "k_fast": 0.35,          # share of the fast store (surface and near-surface flow) reaching the river a day
    "k_slow": 0.01,          # share of the slow store (groundwater) reaching the river a day (a lowland river's slow recession)
    "to_slow_mm": 1.5,       # mm a day the fast store passes to the slow, x the texture's drain rate / 0.25
    "excess_mm": 12.0,       # rain above this a day runs straight off on land that drains like loam (scaled by drain rate / 0.25)
    "wood_intercept": 0.15,  # share of rain a full canopy holds back
    "wood_quick": 0.3,       # share of the fast store's outflow a full canopy holds back (litter, roots, rougher ground)
    "km_a_day": 15.0,        # a reach's water reaches the next after its river length / this (at least a day)
    "stage_m": 1.0,          # stage above normal water = stage_m x ((Q / median)^0.4 - 1)
    "bands": [(0.3, "dry"), (0.6, "low"), (2.0, "normal"), (4.0, "high"), (8.0, "spate"), (1e9, "flood")],
    "ice_k": 2.7,            # ice thickness, cm = ice_k x sqrt(frost degree-days) (Stefan's law); thaw takes 1.5 x the warmth
}


P.update(json.loads(os.environ.get("PROTO_P", "{}")))   # overrides for a sensitivity run, e.g. PROTO_P='{"k_slow": 0.01}'


def band(r):
    for top, name in P["bands"]:
        if r < top:
            return name
    return "flood"


def load(path):
    root = os.environ.get("CYB_ROOT") or os.getcwd()
    sys.path.insert(0, root)
    from cybertron2.engine.world import World
    w = World(yaml.safe_load(open(path)))
    cells = np.load(path.replace(".yaml", ".cells.npz"), allow_pickle=True)
    return w, cells


def reaches(w):
    """Reaches: each village's home and ring as one; every other area alone. Each with its area, soil, wood share, the node whose
    weather it has, its river length, and the reach its water goes to."""
    land = w.s["wild"]["land"]
    A = land["areas"]
    rid = {a: (f"v:{v['node']}" if v["kind"] in ("home", "ring") else a) for a, v in A.items()}
    R = {}
    for a, v in A.items():
        r = R.setdefault(rid[a], {"areas": [], "km2": 0.0, "cap": 0.0, "drain": 0.0, "wood": 0.0, "river_km": 0.0,
                                  "big_river_km": 0.0, "node": v["node"], "elev": 0.0})
        km2 = float(v["km2"])
        tex = v.get("texture") or {"loam": 1.0}
        cap = sum(s * AWC.get(t, 150.0) for t, s in tex.items()) * P["depth_m"] * (1 - float(v.get("rock") or 0))
        dr = sum(s * DRAIN.get(t, 0.25) for t, s in tex.items())
        wood = float((v.get("cover") or {}).get("forest", 0.0)) / max(km2, 1e-9)
        r["areas"].append(a)
        for k, x in (("cap", cap), ("drain", dr), ("wood", wood), ("elev", float(v.get("elevation") or 0))):
            r[k] += x * km2
        r["km2"] += km2
        r["river_km"] += float(v.get("river_km") or 0)
        r["big_river_km"] += float(v.get("big_river_km") or 0)
    for r in R.values():
        for k in ("cap", "drain", "wood", "elev"):
            r[k] /= max(r["km2"], 1e-9)
    down = land["down"]
    nb = defaultdict(list)
    for a, b, ln in land["links"]:
        nb[a].append(b)
        nb[b].append(a)
    for name, r in R.items():                       # where its water goes: out of the reach along `down`, else the lowest river neighbour
        to = None
        for a in r["areas"]:
            x = down.get(a)
            while x and x in A and rid[x] == name:
                x = down.get(x)
            if x and (x == "out" or (x in A and rid[x] != name)):
                to = rid[x] if x in A else "out"
                if r["river_km"] > 0:
                    break
        if to is None:
            cand = [rid[b] for a in r["areas"] for b in nb[a] if rid[b] != name and R.get(rid[b], {}).get("river_km", 0) > 0]
            cand = sorted(set(cand), key=lambda c: R[c]["elev"])
            to = cand[0] if cand else "out"
        r["to"] = to
        r["lag"] = max(1, round(r["river_km"] / P["km_a_day"]))
    order, seen = [], set()                           # upstream first
    def visit(n, stack=()):
        if n in seen or n == "out" or n in stack:
            return
        for m, q in R.items():
            if q["to"] == n:
                visit(m, stack + (n,))
        seen.add(n)
        order.append(n)
    for n in R:
        visit(n)
    return R, order


def weather(w, nodes, days):
    """The engine's weather by place (climate.py, D4-109), day by day; cached to a file named by WEATHER_CACHE if set."""
    import pickle
    cache = os.environ.get("WEATHER_CACHE")
    if cache and os.path.exists(cache):
        W = pickle.load(open(cache, "rb"))
        if all(n in W and len(W[n]) >= days for n in nodes):
            return W
    from cybertron2.engine import climate as CL
    W = {n: [{k: e[k] for k in ("rain", "temp", "low", "wind", "type")} for e in (CL.env(w, n, d) for d in range(days))]
         for n in nodes}
    if cache:
        pickle.dump(W, open(cache, "wb"))
    return W


def simulate(R, order, W, days, clear=(), pace=1.0, wood=None):
    """pace: real days of seasonal water balance an engine day stands for. 1 = every rate real (one clock). Above 1 (two clocks):
    evaporation, the soil, the slow store and snowmelt move `pace` days a day on the season's mean rain (a running mean of the
    weather), while the day's own rain above that mean runs through the fast store at real rates, so a storm is still one day."""
    st = {n: {"soil": 0.6 * r["cap"], "snow": 0.0, "gw": 30.0, "fast": 0.0} for n, r in R.items()}
    pipe = defaultdict(lambda: defaultdict(float))     # pipe[n][day] = water arriving at n on that day, m3
    Q = {n: np.zeros(days) for n in R}
    soil = {n: np.zeros(days) for n in R}
    snow = {n: np.zeros(days) for n in R}
    mean = {}
    for d in range(days):
        for n in order:
            r, s = R[n], st[n]
            e = W[r["node"]][d]
            wd = 0.0 if n in clear else (wood[n] if wood is not None and n in wood else r["wood"])
            day_rain, temp = float(e["rain"]), float(e["temp"])
            m = mean.setdefault(n, day_rain)
            m = mean[n] = m + (day_rain - m) / 6.0                 # the season's rain, a running mean over about six engine days
            if pace > 1:
                rain, storm = pace * min(day_rain, m), max(0.0, day_rain - m)
            else:
                rain, storm = day_rain, 0.0
            if temp <= P["snow_c"]:
                s["snow"] += rain
                inp = 0.0
            else:
                inp = rain
            melt = min(s["snow"], max(0.0, temp) * P["melt_per_c"] * pace)
            s["snow"] -= melt
            inp = inp * (1 - P["wood_intercept"] * wd) + melt
            dr = r["drain"] / 0.25
            excess = max(0.0, inp - P["excess_mm"] * dr) if pace <= 1 else 0.0   # rain too heavy to soak in (a storm's)
            inp -= excess
            rech = inp * min(1.0, s["soil"] / r["cap"]) ** P["beta"]
            s["soil"] += inp - rech
            pet = max(0.0, temp) * P["pet_per_c"] * pace
            s["soil"] -= min(s["soil"], pet * min(1.0, s["soil"] / (0.7 * r["cap"])))
            over = max(0.0, s["soil"] - r["cap"])
            s["soil"] -= over
            if pace > 1:                                           # the season's water feeds the slow store; the storm the fast
                s["gw"] += rech + over
                st_in = storm * (1 - P["wood_intercept"] * wd)
                st_x = max(0.0, st_in - P["excess_mm"] * dr)
                s["fast"] += st_x + (st_in - st_x) * min(1.0, s["soil"] / r["cap"]) ** P["beta"] + excess
            else:
                s["fast"] += rech + over + excess
                down_ = min(s["fast"], P["to_slow_mm"] * dr)
                s["fast"] -= down_
                s["gw"] += down_
            quick = P["k_fast"] * s["fast"] * (1 - P["wood_quick"] * wd)
            s["fast"] -= quick
            base = min(s["gw"], P["k_slow"] * pace * s["gw"]) if pace > 1 else P["k_slow"] * s["gw"]
            s["gw"] -= base
            q = (quick + base / (pace if pace > 1 else 1.0)) * r["km2"] * 1000.0 + pipe[n].pop(d, 0.0)
            Q[n][d] = q
            soil[n][d] = s["soil"] / r["cap"]
            snow[n][d] = s["snow"]
            if r["to"] != "out":
                pipe[r["to"]][d + r["lag"]] += q
    return Q, soil, snow


def ice_series(W, node, days, pace=1.0):
    """Ice on still water, cm, by Stefan's law on frost degree-days; a thaw takes 1.5 x the warmth. With two clocks ice is a
    seasonal stock: it builds on the season's mean temperature (a running mean of the weather) at `pace` days a day."""
    fdd, out, m = 0.0, [], None
    for d in range(days):
        t = float(W[node][d]["temp"])
        m = t if m is None else m + (t - m) / 6.0
        x = (t if pace <= 1 else m) * max(1.0, pace)
        fdd = max(0.0, fdd + (-x if x < 0 else -1.5 * x))
        out.append(P["ice_k"] * math.sqrt(fdd))
    return out


def parcel_heights(w, cells, node):
    """Each of the village's land parcels: its cells' heights above the river (the cells' `f`), leaving out river cells."""
    place, f, riv = cells["place"], cells["f"], cells["river"]
    out = {}
    for pid, p in w.spec["nodes"][node]["parcels"].items():
        m = (place == pid) & (riv == 0)
        if m.any() and p["cover"] != "water":
            out[pid] = (p["name"], p["cover"], np.sort(f[m]))
    return out


HEIGHTS = (0.5, 1.0, 1.5, 2.0, 3.0)
WEAR = {"dry": 0.5, "low": 0.5, "normal": 1.0, "high": 2.0, "spate": 5.0, "flood": 15.0}   # D2-210's flow factors on a weir


def village(w, cells, R, W, Q, soil, snow, v, years, spin, pace=1.0):
    n = f"v:{v}"
    q = Q[n][spin:]
    med = float(np.median(q))
    r = q / max(med, 1e-9)
    bands = Counter(band(x) for x in r)
    onsets, prev = Counter(), None
    for x in r:
        b = band(x)
        if b in ("spate", "flood") and b != prev:
            onsets[b] += 1
        prev = b
    stage = P["stage_m"] * (np.maximum(r, 1e-9) ** 0.4 - 1)
    flooded = {}
    for pid, (name, cover, fs) in parcel_heights(w, cells, v).items():
        some, half = int(np.sum(stage > fs[0])), int(np.sum(stage > fs[len(fs) // 2]))
        if some:
            flooded[f"{name} ({cover}, lowest {fs[0]:.1f} m)"] = [round(some / years, 1), round(half / years, 1)]
    ice = ice_series(W, v, len(Q[n]))[spin:]   # ice on the weather clock: the season's mean never freezes here (02zzn §3)
    return {
        "days a year in each band": {b: round(bands[b] / years, 1) for b in ("dry", "low", "normal", "high", "spate", "flood")},
        "spates / floods a year (onsets)": [round(onsets["spate"] / years, 2), round(onsets["flood"] / years, 2)],
        "highest flow / median": round(float(r.max()), 1), "highest stage, m": round(float(stage.max()), 2),
        "weir wear a year, x a year of normal flow (D2-210 flow factors)": round(sum(WEAR[band(x)] for x in r) / (32 * years), 2),
        "days a year the river stands above (m)": {h: round(int(np.sum(stage > h)) / years, 2) for h in HEIGHTS},
        "years with the river above 1 m at least once": round(float(np.mean([stage[32 * y:32 * y + 32].max() > 1.0
                                                                              for y in range(years)])), 2),
        "parcels with any / half their land under water, days a year": flooded,
        "soil under a quarter / half full, days a year": [round(int(np.sum(soil[n][spin:] < 0.25)) / years, 1),
                                                           round(int(np.sum(soil[n][spin:] < 0.5)) / years, 1)],
        "ice over 5 / 15 cm on still water, days a year": [round(sum(1 for x in ice if x >= 5) / years, 1),
                                                           round(sum(1 for x in ice if x >= 15) / years, 1)],
        "snow lying (> 5 mm), days a year": round(int(np.sum(snow[n][spin:] > 5)) / years, 1),
    }


def compare(a, b, years):
    med = float(np.median(a))
    return {"peak flow / median": [round(float(a.max()) / med, 1), round(float(b.max()) / med, 1)],
            "days a year at spate or flood": [round(int(np.sum(a / med >= 4)) / years, 2), round(int(np.sum(b / med >= 4)) / years, 2)],
            "days a year low or dry": [round(int(np.sum(a / med < 0.6)) / years, 2), round(int(np.sum(b / med < 0.6)) / years, 2)]}


def report(w, cells, years=10, spin=32, paces=(1.0, 11.4)):
    R, order = reaches(w)
    days = spin + 32 * years
    W = weather(w, sorted({r["node"] for r in R.values()}), days)
    villages = sorted(n[2:] for n in R if n.startswith("v:"))
    up = ([m for m in R if _upstream(R, m, "v:Saltwell")] + ["v:Saltwell"]) if "v:Saltwell" in R else []
    out = {"years": years, "reaches": len(R)}
    for pace in paces:
        key = "one clock (every rate real)" if pace <= 1 else f"two clocks (seasonal stores at {pace} days a day)"
        Q, soil, snow = simulate(R, order, W, days, pace=pace)
        o = out[key] = {v: village(w, cells, R, W, Q, soil, snow, v, years, spin, pace) for v in villages}
        if up and "v:Millham" in R:
            Qc, _, _ = simulate(R, order, W, days, clear=set(up), pace=pace)
            Qw, _, _ = simulate(R, order, W, days, pace=pace, wood={m: 0.8 for m in up})
            Qx, _, _ = simulate(R, order, W, days, pace=pace, wood={m: 0.0 for m in up})
            o["Millham, the woods above Saltwell cleared (before -> after)"] = dict(
                compare(Q["v:Millham"][spin:], Qc["v:Millham"][spin:], years),
                **{"reaches": len(up), "wood share before": round(float(np.average([R[m]["wood"] for m in up],
                                                                                    weights=[R[m]["km2"] for m in up])), 2)})
            o["Millham, the same land 80% wooded -> cleared"] = compare(Qw["v:Millham"][spin:], Qx["v:Millham"][spin:], years)
    return out


def _upstream(R, m, n):
    x, k = R[m]["to"], 0
    while x != "out" and k < 200:
        if x == n:
            return True
        x, k = R[x]["to"], k + 1
    return False


if __name__ == "__main__":
    w, cells = load(sys.argv[1])
    if len(sys.argv) > 3:                                 # an era to try instead of the world's own, e.g. cold
        w.spec.setdefault("climate", {})["era"] = sys.argv[3]
        w2 = type(w)(dict(w.spec))
        w = w2
    print(json.dumps(report(w, cells, int(sys.argv[2]) if len(sys.argv) > 2 else 10), indent=1))
