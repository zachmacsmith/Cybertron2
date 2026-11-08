"""M6b: can the engine's existing renewal rules already give a seasonal wild-food year (the hungry gap) as data only?
The periodic rule (built for fish runs): a resident stock K that regrows fast, and a run toward run_K in run_seasons."""
import sys; sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine import renewal as RN
from cybertron2.engine.data import PHYSICS
p = dict(PHYSICS)
SEAS = ["spring", "summer", "autumn", "winter"]
def year(res, effort, sd=8, years=3, base=1.2):
    out = {s: 0.0 for s in SEAS}; S0 = res["S"]
    for y in range(years):
        out = {s: 0.0 for s in SEAS}
        for d in range(4 * sd):
            season = SEAS[d // sd]
            K = res["K"]; S = res["S"]
            ref = max(K, res.get("run_K", K)) if season in res.get("run_seasons", []) else K
            take = min(base * effort * min(1.0, S / max(ref, 1e-9)), max(0.0, S - 0.1 * K))
            res["S"] = S - take; out[season] += take
            res["S"] = RN.RULES[res["renewal"]](p, res, {"winter": season == "winter", "season": season})
    return out
flat = year({"renewal": "fast", "K": 1.0, "S": 1.0, "r": 0.3}, 0.1)
seas = year({"renewal": "periodic", "K": 0.15, "S": 0.15, "r": 0.3, "run_K": 2.2, "run_r": 0.3, "run_seasons": ["summer", "autumn"]}, 0.1)
print("flat now (fast, K 1):        ", {k: round(v, 2) for k, v in flat.items()}, "year", round(sum(flat.values()), 2))
print("seasonal (periodic, K .15):  ", {k: round(v, 2) for k, v in seas.items()}, "year", round(sum(seas.values()), 2))
