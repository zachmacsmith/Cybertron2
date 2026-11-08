"""Calibrate W2 once per food (never per kind): each food's growth is scaled by the densities, against real ones, of the
unterritorial plant-eaters that live on it, weighted by how much of their food it is. Predators, territorial kinds and migrants
are not anchors: they are left to emerge."""
import json, pickle, sys, numpy as np, web2 as W2, kinds2, calibrate as C
REF = ["plain_1", "upland_and_moor_1", "fen_with_islands_1", "settled_lowland_and_frontier_1", "sand_country_1", "scarp_and_vale_1",
       "w:flat_marsh", "w:alpine"]
ERA_OUT = ["aurochs", "bison", "wild horse", "elk", "rabbit", "fallow deer"]          # era and introduced packs, tested later
def anchors(kinds):
    return [n for n, k in kinds.items() if k["terr"] is None and k["migrant"] is None and k["cls"] in ("herb", "gran", "omni") and k["ref"]]
def fit(kinds, iters=10, years=40, worlds=REF, scale=None, verbose=True):
    scale = dict(scale or {})
    A = anchors(kinds)
    for it in range(iters):
        rel = {n: [] for n in A}; wsum = {}
        for w in worlds:
            fr = C.load(w); land = fr["f"]["land"]
            out, rec = W2.run(fr["f"], fr["r"], kinds, years=years, seed=it, scale=scale)
            for n in A:
                hab = float((rec["suit"][n] * land).sum() / land.sum())
                if hab > 0.01:
                    rel[n].append(max(np.mean(out[n][-10:]) / hab / kinds[n]["ref"], 1e-3))
        for n in A:                                                        # weight by what the diet calls for, so a kind
            d = {f: p for f, p in kinds[n]["diet"].items() if f in W2.FOOD or f in W2.SPLIT}   # that died out still counts
            t = sum(d.values()) or 1.0
            for f, p in d.items():
                wsum.setdefault(f, {}); wsum[f][n] = p / t
        lr = {n: float(np.mean(np.log(v))) for n, v in rel.items() if v}
        for f, d in wsum.items():
            tot = sum(d.values())
            if tot <= 0: continue
            m = sum(v * lr.get(n, 0.0) for n, v in d.items()) / tot
            scale[f] = float(np.clip(scale.get(f, 1.0) * np.exp(-0.5 * np.clip(m, -1.5, 1.5)), 0.02, 50))
        if verbose:
            print(f"iter {it}: " + ", ".join(f"{n} {np.exp(x):.2f}" for n, x in lr.items()), flush=True)
    return scale, lr
if __name__ == "__main__":
    kinds = {n: k for n, k in kinds2.KINDS.items() if n not in ERA_OUT}
    scale, lr = fit(kinds)
    print("scales:", {f: round(v, 2) for f, v in scale.items()})
    json.dump(scale, open("scale2.json", "w"))
