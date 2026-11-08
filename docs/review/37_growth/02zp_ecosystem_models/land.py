"""Build generator land for a configuration (no people, no writer)."""
import sys, time, numpy as np
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.landgen import field as F, macro as M, physical as P, vocab as V, settle as ST, ecology as EC

def land(config=None, seed=1, settled="settled", size_km=50.0, km=0.15, n_sites=4):
    conf = dict(V.DEFAULTS); conf.update({"configuration": config, "seed": seed, "settled": settled, "size_km": size_km, "km": km,
                                          "settlements": n_sites})
    conf["_people"] = {}
    g = F.grid(seed, conf["size_km"], conf["km"])
    prims = M.primitives(conf)
    L = P.build(conf, g, prims)
    try:
        chosen = ST.choose_sites(L, conf, {})
        sites = [rc for _, rc in chosen]
    except Exception as e:
        print("sites failed", e); sites = []
    import copy
    L.eco_natural = L.eco.copy()
    EC.settled(L, sites)
    L.sites = sites
    return L

if __name__ == "__main__":
    for cfg in [None] + [k for k in V.CONFIGS if k != "plain"]:
        t = time.time()
        L = land(cfg)
        land_mask = ~L.sea
        vals, cnt = np.unique(L.eco[land_mask], return_counts=True)
        share = sorted(zip(vals, cnt / cnt.sum()), key=lambda x: -x[1])
        print(f"{str(cfg):32s} {time.time()-t:5.1f}s ", ", ".join(f"{v} {s:.0%}" for v, s in share if s >= 0.01))
