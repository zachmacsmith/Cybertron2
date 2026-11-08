"""Tune W2's stabilisers on dynamics, not only levels: for each setting of the crowding brake (where it bites, how hard), refit the
nine food scales, then measure year-to-year variation, levels, local depletion under hunting near villages, and whether an
introduction and a removal move other kinds. Targets (real ranges, roughly): year CV 0.3-0.7 small mammals and grouse, 0.1-0.3
ungulates, 0.1-0.4 predators; hunting near villages should lower game there; introductions and removals should move someone."""
import copy, json, itertools, numpy as np, web2 as W2, kinds2, calibrate as C, calib3 as C3
from calib2 import ERA_OUT
BASE = {n: k for n, k in kinds2.KINDS.items() if n not in ERA_OUT}
WORLDS = ["plain_1", "upland_and_moor_1", "settled_lowland_and_frontier_1", "fen_with_islands_1"]
SMALL = ["voles and mice", "brown hare", "red grouse", "red squirrel", "rats", "water vole"]
UNG = ["red deer", "roe deer", "wild boar"]
PRED = ["fox", "wolf", "lynx", "owls", "stoat and polecat", "otter"]
GAME = ["red deer", "roe deer", "wild boar", "brown hare"]

def measure(kinds, scale, knobs, worlds=WORLDS, years=60):
    cv, rel, local = {}, {}, {}
    for w in worlds:
        fr = C.load(w); land = fr["f"]["land"]; near = fr["f"]["farm"] > 0.05
        out, rec = W2.run(fr["f"], fr["r"], kinds, years=years, scale=scale, knobs=knobs, seed=1)
        for n, k in kinds.items():
            s = np.array(out[n][-30:]); m = s.mean()
            hab = float((rec["suit"][n] * land).sum() / land.sum())
            if m > 1e-9 and hab > 0.01:
                cv.setdefault(n, []).append(s.std() / m); rel.setdefault(n, []).append(m / hab / k["ref"])
        for n in GAME:
            N = rec["final"][n]; su = rec["suit"][n]
            a = (N[near] / np.maximum(su[near], 1e-6)).mean(); b = (N[~near & (su > 0.2)] / np.maximum(su[~near & (su > 0.2)], 1e-6)).mean()
            local.setdefault(n, []).append(float(a / max(b, 1e-9)))
    return {n: float(np.median(v)) for n, v in cv.items()}, {n: float(np.median(v)) for n, v in rel.items()}, {n: float(np.median(v)) for n, v in local.items()}

def moves(kinds, scale, knobs, w="plain_1"):
    fr = C.load(w)
    o0, _ = W2.run(fr["f"], fr["r"], kinds, years=50, scale=scale, knobs=knobs, seed=2)
    k1 = dict(kinds); k1["rabbit"] = kinds2.KINDS["rabbit"]
    o1, _ = W2.run(fr["f"], fr["r"], k1, years=50, scale=scale, knobs=knobs, seed=2)
    k2 = {n: v for n, v in kinds.items() if n != "fox"}
    o2, _ = W2.run(fr["f"], fr["r"], k2, years=50, scale=scale, knobs=knobs, seed=2)
    def ch(o):
        r = {n: np.mean(o[n][-20:]) / max(np.mean(o0[n][-20:]), 1e-9) for n in kinds if n in o and np.mean(o0[n][-20:]) > 1e-9}
        return {n: round(float(x), 2) for n, x in r.items() if not 0.8 < x < 1.25}
    return ch(o1), ch(o2)

if __name__ == "__main__":
    out = {}
    for crowd, dis in itertools.product([3.0, 10.0, 30.0], [0.05, 0.15]):
        knobs = {"crowd": crowd / 3.0, "disease": dis}
        scale, lr = C3.fit(BASE, iters=6, years=40, worlds=WORLDS, verbose=False) if False else (None, None)
        # refit with these knobs
        sc = {f: 1.0 for f in C3.ANCHOR}
        for it in range(6):
            rel = {}
            for w in WORLDS:
                fr = C.load(w); land = fr["f"]["land"]
                o, rec = W2.run(fr["f"], fr["r"], BASE, years=40, seed=it, scale=sc, knobs=knobs)
                for f, n in C3.ANCHOR.items():
                    hab = float((rec["suit"][n] * land).sum() / land.sum())
                    if hab > 0.01: rel.setdefault(n, []).append(max(np.mean(o[n][-10:]) / hab / BASE[n]["ref"], 1e-3))
            for f, n in C3.ANCHOR.items():
                if n in rel: sc[f] = float(np.clip(sc[f] * np.exp(-0.5 * np.clip(np.median(np.log(rel[n])), -1.5, 1.5)), 0.02, 50))
        cv, rel, local = measure(BASE, sc, knobs)
        mv = moves(BASE, sc, knobs)
        key = f"crowd x{crowd:g} Damuth, disease {dis}"
        g = lambda names, d: float(np.median([d[n] for n in names if n in d])) if any(n in d for n in names) else None
        out[key] = {"scale": sc, "cv": cv, "rel": rel, "local": local, "rabbit": mv[0], "nofox": mv[1],
                    "cv_small": g(SMALL, cv), "cv_ung": g(UNG, cv), "cv_pred": g(PRED, cv),
                    "rel_spread": float(np.std(np.log([max(v, 1e-3) for v in rel.values()])))}
        o = out[key]
        print(f"{key:30s} CV small {o['cv_small']:.2f} ungulates {o['cv_ung']:.2f} predators {o['cv_pred']:.2f} | levels spread (log sd) {o['rel_spread']:.2f}"
              f" | near/far game {', '.join(f'{n[:4]} {x:.2f}' for n, x in local.items())}", flush=True)
        print(f"   rabbits in: {o['rabbit']} | fox out: {o['nofox']}", flush=True)
        json.dump(out, open("tune.json", "w"))
