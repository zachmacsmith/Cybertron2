"""Fit each kind's intake factor so its density in good habitat on the reference worlds matches a real value; report the factors.
A factor far from 1 (below 0.25 or above 4) says the kind's diet or habitat is mis-specified."""
import pickle, json, sys, time, copy, numpy as np, web as W
REF = ["plain_1", "upland_and_moor_1", "fen_with_islands_1", "settled_lowland_and_frontier_1", "sand_country_1", "scarp_and_vale_1",
       "isthmus_1", "w:cold_north_moor", "w:alpine"]
def load(n): return pickle.load(open(f"feat/{n}.pkl", "rb"))
def density(out, rec, kinds, feat, last=15):
    res = {}
    for n in kinds:
        s = rec["suit"][n]; land = feat["land"]
        hab = float((s * land).sum() / land.sum())
        res[n] = (float(np.mean(out[n][-last:])) / hab) if hab > 1e-4 else None
    return res
def fit(kinds, iters=6, years=40, worlds=REF, verbose=True, knobs=None, only=None):
    kinds = copy.deepcopy(kinds); F = {w: load(w) for w in worlds}
    hist = []
    for it in range(iters):
        t = time.time(); dens = {n: [] for n in kinds}
        for w, fr in F.items():
            out, rec = W.run(fr["f"], fr["r"], kinds, years=years, seed=it, knobs=knobs)
            for n, x in density(out, rec, kinds, fr["f"]).items():
                if x is not None and rec["suit"][n].sum() > 2: dens[n].append(x)
        err = {}
        for n, k in kinds.items():
            if not dens[n] or k["migrant"] is not None or (only is not None and n not in only): continue
            m = float(np.exp(np.mean(np.log(np.maximum(dens[n], 1e-6)))))
            ratio = m / k["target"]
            err[n] = ratio
            k["k"] = max(k["k"] * float(np.clip(ratio, 0.33, 3.0)) ** 0.7, k.setdefault("k0", k["k"]) * 0.2)   # never eats nothing
        hist.append(err)
        if verbose:
            bad = {n: round(r, 2) for n, r in err.items() if not 0.67 < r < 1.5}
            print(f"iter {it} ({time.time()-t:.0f}s): off by >1.5x: {bad}", flush=True)
    return kinds, hist
if __name__ == "__main__":
    import kinds0
    k, hist = fit(kinds0.KINDS)
    base = kinds0.KINDS
    print("\nfitted intake factors (x the Kleiber first value):")
    for n in k:
        if k[n]["migrant"] is None:
            f = k[n]["k"] / base[n]["k"]
            print(f"  {n:20s} {f:7.2f} {'<- mis-specified?' if not 0.25 < f < 4 else ''}  last ratio {hist[-1].get(n, float('nan')):.2f}")
    pickle.dump(k, open("kinds_fit0.pkl", "wb")); json.dump(hist, open("fit0_hist.json", "w"))
