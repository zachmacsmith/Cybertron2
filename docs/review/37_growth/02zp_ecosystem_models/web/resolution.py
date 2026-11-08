import json, time, numpy as np, web2 as W2
from tune2 import BASE, WFN, assess, load, SMALL, UNG, PRED
import tune2
best = json.load(open("tune2.json"))["climate (steady), outbreaks 0.05"]
sc = best["scale"]
out = {}
for block, km in ((3, 0.45), (7, 1.05), (15, 2.25)):
    kn = {"crowd": 10 / 3, "disease": 0.03, "weather_fn": WFN, "epi_p0": 0.05, "move_scale": 1.05 / km}
    t = time.time()
    r = assess(sc, kn, block=block, years=60)
    r["seconds"] = time.time() - t
    out[f"{km} km"] = {k: v for k, v in r.items()}
    f = lambda x: "-" if x is None else f"{x:.2f}"
    print(f"{km:4.2f} km patches ({r['seconds']:.0f}s): year CV small {f(r['cv_small'])} ungulates {f(r['cv_ung'])} predators {f(r['cv_pred'])}"
          f" | near/far {', '.join(f'{n[:4]} {x:.2f}' for n, x in r['local'].items())}", flush=True)
    print(f"   fox out: {r['nofox']} | rabbits in: {r['rabbit']}", flush=True)
    rel = r["rel"]; print("   levels (x real):", {n: round(rel[n], 2) for n in ["red deer", "roe deer", "wild boar", "brown hare", "voles and mice", "fox", "red grouse", "badger", "brown bear", "capercaillie"] if n in rel}, flush=True)
json.dump(out, open("resolution.json", "w"), default=float)
