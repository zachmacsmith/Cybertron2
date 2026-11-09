"""Wave 1 over all villages and eras: where each kind matters, by policy (scripted), as a share of a village's food need a year."""
import collections, json, numpy as np
import sim, baselines as B
from village import FOOD_NEED

rows = collections.defaultdict(lambda: collections.defaultdict(list))
for r in sim.runs():
    for pname, pol in (("none", B.none), ("calendar", B.calendar), ("expert", B.expert())):
        v, obs = sim.simulate(r, pol, level="expert")
        tot = sim.totals(v)
        yrs = r["drv"].years
        for k, x in tot.items():
            rows[k][pname].append((x["loss"] - x["yield"]) / FOOD_NEED / yrs)
        rows["ALL (net incl. work)"][pname].append(-sim.net(v) / FOOD_NEED / yrs)
out = {k: {p: {"mean": float(np.mean(x)), "max": float(np.max(x))} for p, x in d.items()} for k, d in rows.items()}
for k, d in out.items():
    print(f"{k:22s} " + "  ".join(f"{p} {x['mean']:+.3f} (max {x['max']:+.3f})" for p, x in d.items()))
json.dump(out, open("survey.json", "w"), indent=1)
