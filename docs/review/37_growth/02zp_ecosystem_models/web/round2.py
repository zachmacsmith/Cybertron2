"""Round 2: add each candidate group to the core web; fit only the newcomers; measure their own viability and what they do to
the core, on every world; then their sensitivity and interaction strength where they have the most habitat."""
import copy, json, pickle, sys, numpy as np, kinds0, calibrate as C, rounds as R
from round1 import CORE
KN = {"selfcap": 2.5}
GROUPS = {
    "wetland": ["crane", "grey heron", "water vole", "grey geese", "sea eagle"],
    "upland": ["golden eagle", "black grouse", "raven"],
    "wildwood big grazers": ["aurochs", "bison", "wild horse", "elk"],
    "wildwood others": ["brown bear", "lynx", "capercaillie", "red squirrel", "pine marten"],
    "small predators": ["wildcat", "stoat and polecat", "buzzard", "owls"],
    "open and dry": ["rabbit", "great bustard", "woodpigeon", "fallow deer"],
    "coast": ["seabirds", "seal"],
    "the salmon run": ["salmon"],
}
core = {n: copy.deepcopy(kinds0.KINDS[n]) for n in CORE}
core, _ = C.fit(core, iters=6, years=50, knobs=KN, verbose=False)
pickle.dump(core, open("kinds_core.pkl", "wb"))
base = R.evaluate(core, R.ALL, years=60, knobs=KN)
print("core fitted; red deer rel", round(R.summary(base, core)["red deer"]["rel_median"], 2), flush=True)
out = {"core_summary": R.summary(base, core)}
for g, names in GROUPS.items():
    kk = dict(core); kk.update({n: copy.deepcopy(kinds0.KINDS[n]) for n in names})
    kk, _ = C.fit(kk, iters=5, years=50, knobs=KN, verbose=False, only=set(names))
    res = R.evaluate(kk, R.ALL, years=60, knobs=KN)
    summ = R.summary(res, kk)
    eff = {}
    for c in CORE:
        ch = [np.log(max(res[w][c]["dens"], 1e-9) / max(base[w][c]["dens"], 1e-9)) for w in R.ALL if base[w][c]["persist"]]
        eff[c] = float(np.median(ch)) if ch else 0.0
    best = max(R.ALL, key=lambda w: sum(res[w][n]["hab"] for n in names))
    sens = R.sensitivity(kk, best, draws=12, years=40, extra=KN)
    ko = R.knockout({n: kk[n] for n in kk}, best, years=40, extra=KN) if len(names) else {}
    out[g] = {"summary": {n: summ[n] for n in names}, "core_effect": eff, "best_world": best, "sens": {n: sens[n] for n in names},
              "ko": {n: ko.get(n) for n in names}, "factors": {n: kk[n]["k"] / max(kinds0.KINDS[n]["k"], 1e-9) for n in names}}
    print(f"\n== {g} (sens and knockouts on {best})")
    for n in names:
        s = summ[n]; f = lambda x: "  -  " if x is None else f"{x:5.2f}"
        print(f"  {n:18s} worlds {s['worlds_with_habitat']:2d} persists {f(s['persists'])} rel {f(s['rel_median'])} yCV {f(s['year_cv'])} wCV {f(s['between_worlds_cv'])}"
              f" | spread {f(sens[n]['spread'])} ext {f(sens[n]['extinct_share'])} | strength {f((ko.get(n) or {}).get('strength'))} {(ko.get(n) or {}).get('big', '')} | factor {out[g]['factors'][n]:.2f}")
    big = {c: round(float(np.exp(v)), 2) for c, v in eff.items() if abs(v) > 0.18}
    print("  effect on the core (median ratio):", big)
    json.dump(out, open("round2.json", "w"), default=float)
