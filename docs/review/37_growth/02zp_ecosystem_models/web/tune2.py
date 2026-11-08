"""Stabilisers by episodes, with 37.4's climate driving the year: smooth crowding kept weak (x10 Damuth, 0.03); disease outbreaks
(p0 at crowding 1); the weather from the stand-in or from the climate (steady era). Food refit for each setting. Then the
resolution test at the best setting. Measured against real swings and against removal and introduction effects."""
import json, pickle, numpy as np, web2 as W2, kinds2, calibrate as C, calib3 as C3, climate_bridge as CB
from calib2 import ERA_OUT
from tune import BASE, SMALL, UNG, PRED, GAME
WORLDS = ["plain_1", "upland_and_moor_1", "settled_lowland_and_frontier_1"]
SER = CB.seasons("/home/user/cyb-climate/cybertron2/specs/plenty/brookend.yaml", "steady", years=80)
WFN, NORMAL = CB.weather_fn(SER)

def load(w, block=7):
    return C.load(w) if block == 7 else pickle.load(open(f"featb/{w}_b{block}.pkl", "rb"))

def refit(knobs, worlds=WORLDS, iters=6):
    sc = {f: 1.0 for f in C3.ANCHOR}
    for it in range(iters):
        rel = {}
        for w in worlds:
            fr = load(w); land = fr["f"]["land"]
            o, rec = W2.run(fr["f"], fr["r"], BASE, years=40, seed=it, scale=sc, knobs=knobs)
            for f, n in C3.ANCHOR.items():
                hab = float((rec["suit"][n] * land).sum() / land.sum())
                if hab > 0.01: rel.setdefault(n, []).append(max(np.mean(o[n][-10:]) / hab / BASE[n]["ref"], 1e-3))
        for f, n in C3.ANCHOR.items():
            if n in rel: sc[f] = float(np.clip(sc[f] * np.exp(-0.5 * np.clip(np.median(np.log(rel[n])), -1.5, 1.5)), 0.02, 50))
    return sc

def assess(sc, knobs, block=7, worlds=WORLDS, years=70):
    cv, rel, local = {}, {}, {}
    for w in worlds:
        fr = load(w, block); land = fr["f"]["land"]; near = fr["f"]["farm"] > 0.05
        o, rec = W2.run(fr["f"], fr["r"], BASE, years=years, scale=sc, knobs=knobs, seed=1)
        for n, k in BASE.items():
            s_ = np.array(o[n][-40:]); m = s_.mean(); hab = float((rec["suit"][n] * land).sum() / land.sum())
            if m > 1e-9 and hab > 0.01:
                cv.setdefault(n, []).append(s_.std() / m); rel.setdefault(n, []).append(m / hab / k["ref"])
        for n in GAME:
            N = rec["final"][n]; su = rec["suit"][n]; far = ~near & (su > 0.2)
            if near.any() and far.any():
                local.setdefault(n, []).append(float((N[near] / np.maximum(su[near], 1e-6)).mean() / max((N[far] / np.maximum(su[far], 1e-6)).mean(), 1e-9)))
    fr = load("plain_1", block)
    o0, _ = W2.run(fr["f"], fr["r"], BASE, years=50, scale=sc, knobs=knobs, seed=2)
    o1, _ = W2.run(fr["f"], fr["r"], {n: v for n, v in BASE.items() if n != "fox"}, years=50, scale=sc, knobs=knobs, seed=2)
    k2 = dict(BASE); k2["rabbit"] = kinds2.KINDS["rabbit"]
    o2, _ = W2.run(fr["f"], fr["r"], k2, years=50, scale=sc, knobs=knobs, seed=2)
    ch = lambda o: {n: round(float(np.mean(o[n][-20:]) / max(np.mean(o0[n][-20:]), 1e-9)), 2) for n in BASE if n in o and np.mean(o0[n][-20:]) > 1e-9}
    nofox = {n: x for n, x in ch(o1).items() if not 0.8 < x < 1.25}; rab = {n: x for n, x in ch(o2).items() if not 0.8 < x < 1.25}
    g = lambda names, d: float(np.median([np.median(d[n]) for n in names if n in d])) if any(n in d for n in names) else None
    return {"cv_small": g(SMALL, cv), "cv_ung": g(UNG, cv), "cv_pred": g(PRED, cv), "cv": {n: float(np.median(v)) for n, v in cv.items()},
            "rel": {n: float(np.median(v)) for n, v in rel.items()}, "local": {n: float(np.median(v)) for n, v in local.items()},
            "nofox": nofox, "rabbit": rab}

if __name__ == "__main__":
    out = {}
    base_kn = {"crowd": 10 / 3, "disease": 0.03}
    for label, extra in [("stand-in weather, no outbreaks", {}), ("stand-in weather, outbreaks 0.05", {"epi_p0": 0.05}),
                         ("climate (steady), no outbreaks", {"weather_fn": WFN}), ("climate (steady), outbreaks 0.05", {"weather_fn": WFN, "epi_p0": 0.05}),
                         ("climate (steady), outbreaks 0.15", {"weather_fn": WFN, "epi_p0": 0.15})]:
        kn = dict(base_kn, **extra)
        sc = refit(kn)
        r = assess(sc, kn); r["scale"] = sc
        out[label] = {k: v for k, v in r.items()}
        f = lambda x: "-" if x is None else f"{x:.2f}"
        print(f"{label:36s} year CV small {f(r['cv_small'])} ungulates {f(r['cv_ung'])} predators {f(r['cv_pred'])}"
              f" | near/far {', '.join(f'{n[:4]} {x:.2f}' for n, x in r['local'].items())}", flush=True)
        print(f"   fox out: {r['nofox']} | rabbits in: {r['rabbit']}", flush=True)
        json.dump(out, open("tune2.json", "w"), default=float)
