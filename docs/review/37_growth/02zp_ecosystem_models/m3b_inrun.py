"""M3b: a village's game over a run (64 days = 2 years of 32), under steady hunting, by three renewal rules:
(a) the engine now: threshold rule, r 0.25 a night, nothing below 15% of K;
(b) a year-clock rate: r 0.25 a year (red deer), no immigration;
(c) (b) plus immigration from the land around (a reservoir at its own capacity), the living_populations step 1."""
import sys, json, numpy as np
sys.path.insert(0, "/home/user/cybertron2")
from cybertron2.engine import night as NI
from cybertron2.engine.data import PHYSICS
p = dict(PHYSICS)
YEAR = 32
def sim(rule, K, days, take_per_day, imm=0.0, res_K=None, b=1.0):
    S = K; R = res_K if res_K else 0.0; out = []; got = 0.0
    for d in range(days):
        winter = (d % YEAR) // 8 == 3
        want = take_per_day * (S / K) ** b
        t = min(want, max(0.0, S - 0.0))
        S -= t; got += t
        if rule == "engine":
            S = NI.regrow(p, "threshold", S, K, 0.25, winter)
        else:
            r = 0.25 / YEAR
            S = S + r * S * (1 - S / K)
            if imm:
                flow = imm / YEAR * (R / res_K - S / K) * K        # movement toward equal density with the land around
                S += flow; R -= flow
                R = R + r * R * (1 - R / res_K)
        out.append(S / K)
    return out, got
K = 9.0   # deer in the village's wood: ~1 km2 of wood at the density wolves leave (M3)
res = {}
for take in (0.05, 0.1, 0.2):           # deer a day the village takes (food: a deer ~ 20 food)
    for rule, imm in (("engine", 0), ("year", 0), ("year", 2.0), ("year", 6.0)):
        tr, got = sim(rule, K, 64, take, imm=imm, res_K=K * 20)
        key = f"take {take}/day | {rule}{' imm ' + str(imm) if imm else ''}"
        res[key] = {"S_day32": round(tr[31], 2), "S_day64": round(tr[63], 2), "taken": round(got, 1)}
        print(f"{key:36s} stock day 32 {tr[31]:.2f}K, day 64 {tr[63]:.2f}K, deer taken {got:.1f}")
json.dump(res, open("m3b.json", "w"), indent=1)
