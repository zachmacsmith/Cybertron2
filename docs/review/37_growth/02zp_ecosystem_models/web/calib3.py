"""Calibrate W2 with one anchor per food (a plant-eater that lives mainly on it, with a well-known real density). Nine numbers;
every other kind, every predator, carrion and people's foods are left to emerge."""
import json, sys, numpy as np, web2 as W2, kinds2, calibrate as C
from calib2 import REF, ERA_OUT
ANCHOR = {"grass": "red deer", "sward": "brown hare", "browse": "roe deer", "heather": "mountain hare", "mast": "wild boar",
          "nuts": "red squirrel", "seeds": "voles and mice", "aquatic": "water vole", "fish": "eel"}
def fit(kinds, iters=12, years=40, worlds=REF, verbose=True):
    scale = {f: 1.0 for f in ANCHOR}
    for it in range(iters):
        rel = {n: [] for n in ANCHOR.values()}
        for w in worlds:
            fr = C.load(w); land = fr["f"]["land"]
            out, rec = W2.run(fr["f"], fr["r"], kinds, years=years, seed=it, scale=scale)
            for n in rel:
                hab = float((rec["suit"][n] * land).sum() / land.sum())
                if hab > 0.01:
                    rel[n].append(max(np.mean(out[n][-10:]) / hab / kinds[n]["ref"], 1e-3))
        lr = {n: float(np.median(np.log(v))) for n, v in rel.items() if v}
        for f, n in ANCHOR.items():
            if n in lr:
                scale[f] = float(np.clip(scale[f] * np.exp(-0.5 * np.clip(lr[n], -1.5, 1.5)), 0.02, 50))
        if verbose:
            print(f"iter {it}: " + ", ".join(f"{n} {np.exp(x):.2f}" for n, x in lr.items()), flush=True)
    return scale, lr
if __name__ == "__main__":
    kinds = {n: k for n, k in kinds2.KINDS.items() if n not in ERA_OUT}
    scale, lr = fit(kinds)
    print("scales:", {f: round(v, 2) for f, v in scale.items()})
    json.dump(scale, open("scale3.json", "w"))
