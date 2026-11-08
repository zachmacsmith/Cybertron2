"""Generate land for configurations x seeds and save the fields the ecology models read."""
import sys, numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from land import land
from cybertron2.landgen import vocab as V, physical as P
out = "lands"; os.makedirs(out, exist_ok=True)
cfgs = sys.argv[1].split(",") if len(sys.argv) > 1 else [k for k in V.CONFIGS]
seeds = [int(s) for s in (sys.argv[2].split(",") if len(sys.argv) > 2 else ["1", "2", "3"])]
for cfg in cfgs:
    for sd in seeds:
        settled = "frontier" if "frontier" in cfg else "settled"
        L = land(None if cfg == "plain" else cfg, seed=sd, settled=settled)
        fn = f"{out}/{cfg.replace(' ', '_')}_{sd}.npz"
        np.savez_compressed(fn, h=L.h, wet=L.wet, tex=L.tex, fert=L.fert, moist=L.moist, temp=L.temp, slope=L.slope, river=L.river,
                 near_river=L.near_river, c=L.c, f=L.f, terrain=np.array(P.TERRAIN_NAMES, dtype=object)[L.terrain].astype(str),
                 system=L.system.astype(str), eco0=L.eco_natural.astype(str), eco=L.eco.astype(str), band=L.band, sea=L.sea, lake=L.lake,
                 spring=L.spring, km_in=getattr(L, "km_in", np.zeros(L.g.shape)), sites=np.array(L.sites), km=L.g.km)
        print(fn, flush=True)
