"""Prepare the prototype's inputs: five generated worlds (the generator on climate-calibration), each village's own land, the land
around it (within 2.5 km, by cover), and its daily weather from the engine's climate (D4-109) for ten years under several eras."""
import sys, pickle, collections, numpy as np
sys.path.insert(0, "../../../../..")   # the repository root on branch climate-calibration (5ef36fe or later); writes inputs.pkl
from cybertron2.landgen import write as W
from cybertron2.engine.world import World
from cybertron2.engine import climate as CL

WORLDS = [("settled lowland and frontier", 7), ("fen with islands", 7), ("upland and moor", 7), ("plain", 7), ("sand country", 7)]
ERAS = ["steady", "cold", "wet", "warm", "dry"]
YEARS = 10
HA = 2.0
KM = 0.15
out = {}
for cfg, seed in WORLDS:
    world, cells, report = W.generate({"name": "t", "seed": seed, "days": 10, "calendar": {"season": "spring", "day": 1, "season_days": 8},
                                       "generate": {"seed": seed, "configuration": None if cfg == "plain" else cfg, "spacing_km": 8.0,
                                                    "settlements": 4}})
    cover = cells["cover"]
    yy, xx = np.mgrid[0:cover.shape[0], 0:cover.shape[1]]
    vills = {}
    for k, n in report["nodes"].items():
        if not k.startswith("s"):
            continue
        nd = world["nodes"][k]
        own = collections.Counter()
        rivers = set()
        for p in nd["parcels"].values():
            own[p["cover"]] += p["size"] * HA
            rv = (p.get("land") or {}).get("river")
            if rv and rv != "none":
                rivers.add(rv)
        r0, c0 = n["site_km"][1] / KM, n["site_km"][0] / KM
        d = np.hypot(yy - r0, xx - c0) * KM
        ring = collections.Counter({str(c): float(((cover == c) & (d <= 2.5)).sum() * KM * KM) for c in np.unique(cover)})
        near_water = float(((cover == "water") & (d <= 1.5)).sum() * KM * KM)
        vills[k] = {"name": nd["name"], "own_ha": dict(own), "ring_km2": dict(ring), "rivers": sorted(rivers), "water_km2_1500m": near_water}
    wx = {}
    for era in ERAS:
        spec = dict(world); spec["climate"] = {"era": era}; spec.setdefault("agents", {})
        w = World(spec)
        assert w.year_days() == 32
        wx[era] = {k: [CL.env(w, k, d) for d in range(YEARS * 32)] for k in vills}
    out[cfg] = {"villages": vills, "weather": wx}
    print(cfg, {k: (v["name"], round(v["ring_km2"].get("forest", 0), 1), v["own_ha"].get("field", 0), v["rivers"], round(v["water_km2_1500m"], 2)) for k, v in vills.items()}, flush=True)
pickle.dump(out, open("inputs.pkl", "wb"))
