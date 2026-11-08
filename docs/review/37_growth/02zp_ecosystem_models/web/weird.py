"""Purposefully extreme worlds from the generator (scratch only: the moisture shift is a patch on physical.climate here)."""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.landgen import field as F, macro as M, physical as P, vocab as V, settle as ST, ecology as EC
WEIRD = {
    "drowned isles":      {"flood_m": 75.0},
    "alpine":             {"base_m": 350.0, "relief_m": 550.0, "temperature_c": 7.0},
    "flat marsh":         {"base_m": 4.0, "relief_m": 6.0, "tilt_m_km": 0.05, "moisture": 0.25, "wetness": 0.35},
    "dry chalk plateau":  {"chalk_n": -2.0, "base_m": 160.0, "moisture": -0.25, "wetness": -0.15},
    "sand sea":           {"sand_n": 2.0, "moisture": -0.2},
    "clay wetland":       {"clay_n": -2.0, "base_m": 40.0, "relief_m": 30.0, "moisture": 0.2, "wetness": 0.25},
    "cold north moor":    {"configuration": "upland and moor", "temperature_c": 6.0, "moisture": 0.15, "wetness": 0.1},
    "ancient wildwood":   {"configuration": "settled lowland and frontier", "settled": 0.92},
    "stripped land":      {"settled": 0.02},
    "fen under rising sea": {"configuration": "fen with islands", "flood_m": 4.0},
    "wet basin":          {"configuration": "basin in a ring of hills", "moisture": 0.3, "wetness": 0.25},
    "warm dry lowland":   {"temperature_c": 12.5, "moisture": -0.3, "wetness": -0.15},
}
def make(name, over, seed=4):
    conf = dict(V.DEFAULTS); conf.update({"seed": seed}); conf.update(over); conf["_people"] = {}
    g = F.grid(seed, conf["size_km"], conf["km"])
    L = P.build(conf, g, M.primitives(conf))
    try:
        sites = [rc for _, rc in ST.choose_sites(L, conf, {})]
    except Exception as e:
        sites = []; print("  no sites:", e)
    L.eco_natural = L.eco.copy()
    EC.settled(L, sites)
    return L, sites
if __name__ == "__main__":
    os.makedirs("weird", exist_ok=True)
    for name, over in WEIRD.items():
        try:
            L, sites = make(name, over)
        except Exception as e:
            print(name, "FAILED", type(e).__name__, e); continue
        fn = f"weird/{name.replace(' ', '_')}.npz"
        np.savez_compressed(fn, h=L.h, wet=L.wet, tex=L.tex, fert=L.fert, moist=L.moist, temp=L.temp, slope=L.slope, river=L.river,
                 near_river=L.near_river, c=L.c, f=L.f, terrain=np.array(P.TERRAIN_NAMES, dtype=object)[L.terrain].astype(str),
                 system=L.system.astype(str), eco0=L.eco_natural.astype(str), eco=L.eco.astype(str), band=L.band, sea=L.sea, lake=L.lake,
                 spring=L.spring, km_in=getattr(L, "km_in", np.zeros(L.g.shape)), sites=np.array(sites), km=L.g.km)
        land = ~L.sea
        u, c = np.unique(L.eco[land], return_counts=True)
        top = sorted(zip(u, c / c.sum()), key=lambda x: -x[1])
        print(f"{name:22s} land {land.mean():.0%} sites {len(sites)} | " + ", ".join(f"{a} {b:.0%}" for a, b in top if b >= 0.02), flush=True)
