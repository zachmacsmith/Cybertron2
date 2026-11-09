"""Phase 1 of the wild layer (wild_layer.md §6): the ecology offline on generated worlds, driven by the engine's climate at each
area's node. Reports each kind's density in good habitat against a real one, its swings between years, and how worlds and eras
differ. Usage: python3 offline.py [years] [eras...]"""
import json, sys, time, collections
import numpy as np
sys.path.insert(0, "/home/user/cyb-ecology")
from cybertron2.landgen import write as W
from cybertron2.engine.world import World
from cybertron2.engine import climate as CL
from cybertron2.wild import ecology as EC, kinds as WK

WORLDS = [("settled lowland and frontier", 7), ("fen with islands", 7), ("upland and moor", 7), ("plain", 7), ("sand country", 7)]


def world_of(cfg, seed):
    world, cells, report = W.generate({"name": "t", "seed": seed, "days": 10, "calendar": {"season": "spring", "day": 1, "season_days": 8},
                                       "generate": {"seed": seed, "configuration": None if cfg == "plain" else cfg, "spacing_km": 8.0,
                                                    "settlements": 4}})
    return world


def weather_series(world, era, days):
    spec = dict(world); spec["climate"] = {"era": era}; spec.setdefault("agents", {})
    w = World(spec)
    nodes = sorted({a["node"] for a in world["wild"]["land"]["areas"].values()})
    out = []
    for d in range(days):
        day = {}
        for nd in nodes:
            e = CL.env(w, nd, d)
            day[nd] = {"temp": e["temp"], "low": e["low"], "rain": e["rain"], "snow": CL.label(w, nd, d) == "snow"}
        out.append(day)
    return out


def run(world, era, years, Y=32, seed=0, knobs=None):
    land = world["wild"]["land"]
    m = EC.Model(land, Y=Y, knobs=knobs)
    st = m.initial()
    wx = weather_series(world, era, years * Y)
    rng = np.random.default_rng(seed)
    yearly = collections.defaultdict(list)
    mast = []
    for d in range(years * Y):
        if d % Y == 0:
            u = float(rng.random())
            epi = {k: rng.random(m.n) for k in m.names}
        EC.step(m, st, d, wx[d], {"mast": u, "epi": epi})
        if d % Y == Y - 1:
            for k in m.names:
                N = np.asarray(st["pop"][k]); good = (m.suit[k] >= np.quantile(m.suit[k], 0.75)) & (m.suit[k] > 0.15)
                yearly[k].append(float((N[good]).mean()) if good.any() else 0.0)
            mast.append(st["mast"]["years"].get(str(d // Y)))
    return m, st, yearly, mast


if __name__ == "__main__":
    years = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    eras = sys.argv[2:] or ["steady"]
    out = {}
    for cfg, seed in WORLDS:
        t = time.time()
        world = world_of(cfg, seed)
        for era in eras:
            m, st, yearly, mast = run(world, era, years)
            res = {}
            for k in m.names:
                ys = np.array(yearly[k][years // 2:]) if not m.kinds[k]["migrant"] else np.array(yearly[k])
                ref = m.kinds[k]["ref"]
                res[k] = {"good_density": round(float(ys.mean()), 3), "ref": ref, "ratio": round(float(ys.mean()) / ref, 2) if ref else None,
                          "cv": round(float(ys.std() / max(ys.mean(), 1e-9)), 2), "good_areas": int(((m.suit[k] >= np.quantile(m.suit[k], 0.75)) & (m.suit[k] > 0.15)).sum())}
            out[f"{cfg} | {era}"] = {"kinds": res, "mast": mast}
            print(f"== {cfg} | {era} ({time.time() - t:.0f}s); mast {mast}")
            for k, r in res.items():
                print(f"   {k:16s} good {r['good_density']:9.3f} / ref {r['ref']:7} = {str(r['ratio']):>6}  cv {r['cv']:.2f}  areas {r['good_areas']}")
    json.dump(out, open("offline.json", "w"), indent=1)
