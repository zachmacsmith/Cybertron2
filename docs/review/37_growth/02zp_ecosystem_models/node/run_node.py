import sys, json, numpy as np
sys.path.insert(0, "/home/user/cyb-climate")
from cybertron2.landgen import write as W
from cybertron2.landgen.ecology import ECOSYSTEMS
import node_eco as NE
WORLDS = [("settled lowland and frontier", 7), ("fen with islands", 7), ("upland and moor", 7), ("plain", 7), ("sand country", 7)]
CHOICES = {"farmers": {"gather": 0.2, "hunt": 0.0, "fish": 0.2},
           "mixed": {"gather": 0.6, "hunt": 0.5, "fish": 0.6},
           "hunters": {"gather": 0.6, "hunt": 1.8, "fish": 1.0, "hunt_reach": 1.5},
           "guarded": {"gather": 0.6, "hunt": 0.5, "fish": 0.6, "watch": 1.0, "scare": 0.5, "cats": True, "fold": 1.0, "fence": 1.0},
           "lord's forest": {"gather": 0.6, "hunt": 0.5, "fish": 0.6, "rights": "lord"}}
YEARS = {"normal": dict(mast=1.0, hard=False), "after a mast year (bust, hard winter)": dict(mast=0.1, hard=True), "mast year": dict(mast=3.0, hard=False)}
rows = []; rng = np.random.default_rng(0)
for cfg, seed in WORLDS:
    world, cells, report = W.generate({"name": "t", "seed": seed, "days": 10, "calendar": {"season": "summer", "day": 3, "season_days": 8},
                                       "generate": {"seed": seed, "configuration": None if cfg == "plain" else cfg}})
    eco = cells["eco"] if "eco" in cells else None
    km = float(cells.get("km", 0.15)) if isinstance(cells.get("km", 0.15), (int, float)) else 0.15
    for nid, n in world["nodes"].items():
        if not nid.startswith("s"): continue
        area = NE.village(world, nid)
        # the reservoir: cover within 5 km of the village's site, from the saved cells
        site = report["nodes"][nid]["site_km"] if "nodes" in report and nid in report["nodes"] else None
        around = {}
        if eco is not None and site is not None:
            ny, nx = eco.shape; yy, xx = np.mgrid[0:ny, 0:nx]
            r0, c0 = int(site[1] / km), int(site[0] / km)
            m = np.hypot(yy - r0, xx - c0) * km <= 5.0
            cov = np.vectorize(lambda e: ECOSYSTEMS.get(e, ("water",))[0])(eco[m])
            u, c = np.unique(cov, return_counts=True)
            around = {a: float(b) * km * km for a, b in zip(u, c)}
        for ch, choice in CHOICES.items():
            for yname, yr in YEARS.items():
                out, need, work, crop, beasts = NE.budget(area, 12, around, choice, rng, **yr)
                rows.append({"world": cfg, "node": nid, "choice": ch, "year": yname, "need": need, "work": work, "crop": crop,
                             "own": area, "around": around, "el": {k: {kk: float(vv) for kk, vv in v.items() if kk in ("food", "work", "loss")} for k, v in out.items()}})
json.dump(rows, open("node_rows.json", "w"))
print("rows", len(rows), "example around:", {k: round(v, 1) for k, v in rows[0]["around"].items()}, "own (ha):", rows[0]["own"])
