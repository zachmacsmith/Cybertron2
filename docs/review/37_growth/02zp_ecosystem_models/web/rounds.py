"""The design loop's tools: fit a set of kinds, then evaluate it on every world: persistence, density, year-to-year variation,
variation between worlds, sensitivity to its numbers, and interaction strength (knock each kind out)."""
import glob, pickle, copy, json, numpy as np, web as W, calibrate as C
ALL = sorted(p.split("/")[1][:-4] for p in glob.glob("feat/*.pkl"))
NORMAL = [w for w in ALL if not w.startswith("w:")]
EXTREME = [w for w in ALL if w.startswith("w:")]
FEAT = {}
def feat(w):
    if w not in FEAT: FEAT[w] = C.load(w)
    return FEAT[w]

def evaluate(kinds, worlds, years=60, seed=0, last=30, policy=None, knobs=None, events_fn=None):
    res = {}
    for w in worlds:
        fr = feat(w)
        out, rec = W.run(fr["f"], fr["r"], kinds, years=years, seed=seed, policy=policy, knobs=knobs, events=events_fn(fr) if events_fn else None)
        land = fr["f"]["land"]
        r = {}
        for n, k in kinds.items():
            hab = float((rec["suit"][n] * land).sum() / land.sum())
            ser = np.array(out[n][-last:])
            mean = float(ser.mean())
            ref = k.get("target", 1.0) * max(hab, 1e-6)
            r[n] = {"hab": hab, "dens": mean, "rel": mean / ref if hab > 0.003 else None,
                    "cv": float(ser.std() / mean) if mean > 1e-9 else None,
                    "persist": (mean > 0.02 * ref) if hab > 0.003 else None}
        r["_rec"] = {"crop_damage": float(np.mean(rec["crop_damage"][-last:])), "stock_killed": float(np.mean(rec["stock_killed"][-last:])),
                     "store_loss": float(np.mean(rec["store_loss"][-last:])),
                     "take": {n: float(np.mean(rec["people_take"][n][-last:])) for n in kinds}}
        res[w] = r
    return res

def summary(res, kinds):
    rows = {}
    for n in kinds:
        rel = [r[n]["rel"] for r in res.values() if r[n]["rel"] is not None]
        per = [r[n]["persist"] for r in res.values() if r[n]["persist"] is not None]
        cv = [r[n]["cv"] for r in res.values() if r[n]["cv"] is not None and r[n]["persist"]]
        dens = [r[n]["dens"] for r in res.values() if r[n]["persist"]]
        rows[n] = {"worlds_with_habitat": len(per), "persists": (sum(per) / len(per)) if per else None,
                   "rel_median": float(np.median(rel)) if rel else None,
                   "year_cv": float(np.median(cv)) if cv else None,
                   "between_worlds_cv": float(np.std(dens) / np.mean(dens)) if len(dens) > 2 and np.mean(dens) > 0 else None}
    return rows

def sensitivity(kinds, world, draws=24, sd=0.25, years=50, seed=7, extra=None):
    """Every kind's b, m and k, and every resource's production, scaled by lognormal(0, sd); how often each kind dies out and how
    much its density moves."""
    rng = np.random.default_rng(seed)
    base = evaluate(kinds, [world], years=years, knobs=extra)[world]
    ext = {n: 0 for n in kinds}; ratios = {n: [] for n in kinds}
    for i in range(draws):
        knobs = dict(extra or {})
        for n in kinds:
            for p in ("b", "k"):
                knobs[f"{p}_{n}"] = float(np.exp(rng.normal(0, sd)))
        for r in W.RES:
            knobs["prod_" + r] = float(np.exp(rng.normal(0, sd)))
        kk = copy.deepcopy(kinds)
        for n in kk:
            kk[n]["m"] = kk[n]["m"] * float(np.exp(rng.normal(0, sd)))
        e = evaluate(kk, [world], years=years, knobs=knobs, seed=i)[world]
        for n in kinds:
            if base[n]["persist"]:
                if not e[n]["persist"]: ext[n] += 1
                if base[n]["dens"] > 0: ratios[n].append(e[n]["dens"] / base[n]["dens"])
    return {n: {"extinct_share": ext[n] / draws if base[n]["persist"] else None,
                "spread": float(np.std(np.log(np.maximum(ratios[n], 1e-6)))) if ratios[n] else None} for n in kinds}

def knockout(kinds, world, years=50, extra=None):
    base = evaluate(kinds, [world], years=years, knobs=extra)[world]
    eff = {}
    for n in kinds:
        if not base[n]["persist"]: continue
        kk = {m: v for m, v in kinds.items() if m != n}
        e = evaluate(kk, [world], years=years, knobs=extra)[world]
        ch = {m: e[m]["dens"] / base[m]["dens"] for m in kk if base[m]["persist"] and base[m]["dens"] > 0}
        big = {m: round(x, 2) for m, x in ch.items() if x > 1.5 or x < 0.67}
        eff[n] = {"strength": float(np.mean([abs(np.log(max(x, 1e-3))) for x in ch.values()])) if ch else 0.0, "big": big}
    return eff
