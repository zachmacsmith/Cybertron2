import copy, json, pickle, sys, numpy as np, kinds0, calibrate as C, rounds as R
from round1 import CORE
out = {}
for arm, knobs in (("no self-limit", None), ("self-limit 2.5x", {"selfcap": 2.5})):
    kinds = {n: copy.deepcopy(kinds0.KINDS[n]) for n in CORE}
    fitted, hist = C.fit(kinds, iters=6, years=50, knobs=knobs, verbose=False)
    res = R.evaluate(fitted, R.ALL, years=60, knobs=knobs)
    summ = R.summary(res, fitted)
    sens = R.sensitivity(fitted, "plain_1", draws=16, years=40, extra=knobs)
    out[arm] = {"summary": summ, "sens": sens, "factors": {n: fitted[n]["k"] / kinds[n]["k"] for n in fitted}}
    pickle.dump(fitted, open(f"kinds_r1b_{arm.split()[0]}.pkl", "wb"))
    print(f"== {arm}")
    print(f"{'kind':16s} persists rel   year-CV between-CV | spread  extinct | intake factor")
    for n, s in summ.items():
        f = lambda x: "  -  " if x is None else f"{x:5.2f}"
        print(f"{n:16s} {f(s['persists'])} {f(s['rel_median'])} {f(s['year_cv'])} {f(s['between_worlds_cv'])} | {f(sens[n]['spread'])} {f(sens[n]['extinct_share'])} | {out[arm]['factors'][n]:.2f}")
json.dump(out, open("round1b.json", "w"), default=float)
