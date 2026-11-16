"""02zzo: the engine's weather (climate.py, D4-109) and the two-clock water (D2-214; 02zzn's prototype) across conditions: lowland,
dry, a wet coast with a rain shadow behind mountains, high mountains, a fen floodplain, a cold north. WORK W-51; Zach, 16 Nov: "try
test the weather in different conditions, like dry places, high mountains, flood plains, the coast etc to see that it makes sense".

    python3 docs/review/37_growth/02zzo_weather_conditions.py <out dir> [years]

For each condition it generates a world (no people) from a named configuration with the generator's own climate settings, then at
every node sets what the generator says the place's climate is (its rain a year, its mean temperature, its distance to the sea)
beside what the engine's weather gives there over the years, put per real year (mm a day x 365, shares of days), and, at each
settlement, the river and soil on the two clocks. Numbers to read against real places are in 02zzo_weather_conditions.md.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

_spec = importlib.util.spec_from_file_location("proto", os.path.join(HERE, "02zzn_environment_prototype.py"))
PR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PR)

BASE = {"days": 32, "calendar": {"season_days": 8}, "climate": {"era": "steady"}, "packs": ["wild"]}


def cfg(name):
    from cybertron2.landgen.vocab import CONFIGS
    return copy.deepcopy(CONFIGS[name])


def conditions():
    """(name, what it stands for, generate block)."""
    up = cfg("upland and moor")
    for f in up:
        if f.get("name") == "moor":
            f["height"] = 1000                                          # high mountains, not a moor
    up.append({"kind": "massif", "name": "summit", "at": [0.8, 0.8], "r": 0.12, "height": 500})
    return [
        ("lowland", "plain lowland, 900 mm, 9 C (the default)", {"configuration": "plain"}),
        ("dry", "plain lowland in a dry climate, 500 mm, 10 C", {"configuration": "plain", "rain_mm": 500.0, "temperature_c": 10.0}),
        ("coast and shadow", "a coastal strip under a 560 m range, west wind: the wet coast, the range, the lee",
         {"configuration": "coastal strip under mountains", "wild_shore": True}),
        ("mountains", "uplands rising to about 1500 m", {"features": up}),
        ("fen floodplain", "a fen basin open to the sea, a large river through it", {"configuration": "fen with islands"}),
        ("cold north", "plain lowland in a cold climate, 6 C", {"configuration": "plain", "temperature_c": 6.0, "rain_mm": 800.0}),
    ]


def make(out, name, gen, seed=4):
    from cybertron2.landgen import settle as ST, write as W
    path = os.path.join(out, name.replace(" ", "_") + ".yaml")
    if os.path.exists(path):
        return path
    for s in range(seed, seed + 12, 2):
        spec = dict(copy.deepcopy(BASE), name=f"cond_{name}", seed=s,
                    generate=dict({"seed": s, "settlements": 3, "household_size": 3, "warn_only": ["capacity"]}, **gen))
        try:
            world, cells, report = W.generate(spec, path)
        except ST.Refused as e:
            print(name, s, "refused:", e, file=sys.stderr)
            continue
        if report["refused"]:
            print(name, s, "refused by checks:", report["refused"], file=sys.stderr)
            continue
        W.write(world, cells, report, path, None)
        return path
    raise SystemExit(f"{name}: no seed made a world")


def node_facts(w, cells, nid):
    """What the generator says the place is: its height, its rain a year, its cells' mean temperature, the sea's distance."""
    n = w.spec["nodes"][nid]
    pids = list((n.get("parcels") or {}).keys())
    m = np.isin(cells["place"], pids) if pids else np.zeros(cells["place"].shape, bool)
    temp = float(np.mean(cells["temp"][m])) if m.any() else None
    sea = float(np.min(cells["c"][m])) if m.any() else None
    return {"name": n.get("name"), "kind": "settlement" if n.get("households") or nid.startswith("s") else "wild or town",
            "height m": n.get("elevation"), "rain mm a year": n.get("rain_mm"),
            "mean temp C": round(temp, 1) if temp is not None else None, "sea km": round(sea, 1) if sea is not None else None}


def weather_stats(w, W, nid, spin):
    e = W[nid][spin:]
    t = np.array([float(x["temp"]) for x in e])
    lo = np.array([float(x["low"]) for x in e])
    r = np.array([float(x["rain"]) for x in e])
    wd = np.array([float(x["wind"]) for x in e])
    season = [w.calendar(spin + i)["season"] for i in range(len(e))]
    seas = {s: round(float(np.mean([t[i] for i in range(len(e)) if season[i] == s])), 1)
            for s in ("spring", "summer", "autumn", "winter")}
    win = [i for i in range(len(e)) if season[i] == "winter"]
    return {"rain mm a real year": round(float(r.mean()) * 365), "wet days (>= 1 mm)": round(float((r >= 1).mean()), 2),
            "heaviest day mm": round(float(r.max()), 1), "mean temp C": round(float(t.mean()), 1), "by season": seas,
            "frost nights": round(float((lo < 0).mean()), 2), "winter frost nights": round(float((lo[win] < 0).mean()), 2),
            "days below 0 C mean": round(float((t < 0).mean()), 3),
            "snow days (falling)": round(float(((r > 0) & (t <= 1.5)).mean()), 3),
            "mean wind m/s": round(float(wd.mean()), 1), "gale days (>= 17 m/s)": round(float((wd >= 17).mean()), 3)}


def heights(out, years=20, hs=(0, 250, 500, 1000, 1500)):
    """The engine's weather by height alone: the lowland world with its nodes set to these heights (the spec's `elevation`, which
    the climate reads first). The generator put no node above about 500 m in the mountain world."""
    from cybertron2.engine.world import World
    sp = yaml.safe_load(open(os.path.join(out, "lowland.yaml")))
    sp.setdefault("agents", {})
    nodes = sorted(sp["nodes"])[:len(hs)]
    for nid, h in zip(nodes, hs):
        sp["nodes"][nid]["elevation"] = float(h)
    w = World(sp)
    W = PR.weather(w, nodes, 32 + 32 * years)
    return {f"{h} m": weather_stats(w, W, nid, 32) for nid, h in zip(nodes, hs)}


def run(out, years=20):
    os.makedirs(out, exist_ok=True)
    from cybertron2.engine.world import World
    res = {}
    spin = 32
    days = spin + 32 * years
    for name, what, gen in conditions():
        path = make(out, name, gen)
        sp = yaml.safe_load(open(path))
        sp.setdefault("agents", {})                                      # no people: the weather and the land only
        w = World(sp)
        cells = np.load(path.replace(".yaml", ".cells.npz"), allow_pickle=True)
        nodes = sorted(w.s["nodes"])
        W = PR.weather(w, nodes, days)
        o = res[name] = {"stands for": what, "world": os.path.basename(path), "nodes": {}}
        for nid in nodes:
            o["nodes"][nid] = {"generator": node_facts(w, cells, nid), "engine weather": weather_stats(w, W, nid, spin)}
        R, order = PR.reaches(w)
        pace = 365.0 / w.year_days()
        Q, soil, snow = PR.simulate(R, order, W, days, pace=pace)
        for nid in nodes:
            n = f"v:{nid}"
            if n not in R:
                continue
            q = Q[n][spin:]
            med = float(np.median(q))
            if med <= 0:
                continue
            rr = q / med
            stage = PR.P["stage_m"] * (np.maximum(rr, 1e-9) ** 0.4 - 1)
            from collections import Counter
            b = Counter(PR.band(x) for x in rr)
            fs = cells["f"][np.isin(cells["place"], list((w.spec["nodes"][nid].get("parcels") or {}).keys())) & (cells["river"] == 0)]
            o["nodes"][nid]["water, two clocks"] = {
                "river km in reach": round(R[n]["river_km"], 1), "reaches above": sum(1 for m in R if PR._upstream(R, m, n)),
                "days a year by band": {k: round(b[k] / years, 1) for k in ("dry", "low", "normal", "high", "spate", "flood")},
                "days a year the river stands 1 m up": round(int(np.sum(stage > 1.0)) / years, 1),
                "soil under a quarter full, days a year": round(int(np.sum(soil[n][spin:] < 0.25)) / years, 1),
                "snow lying, days a year": round(int(np.sum(snow[n][spin:] > 5)) / years, 1),
                "land within 2 m of the river": round(float((fs < 2).mean()), 2) if fs.size else None,
            }
        print(name, "done", file=sys.stderr)
    res["by height alone"] = heights(out, years)
    return res


if __name__ == "__main__":
    out = sys.argv[1]
    years = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(json.dumps(run(out, years), indent=1))
