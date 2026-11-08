"""Patch features and food resources for every world (normal seeds 1-2 and the extreme set), cached for the web runs."""
import glob, pickle, os, sys, numpy as np, test_niche as T, web as W
os.makedirs("feat", exist_ok=True)
files = sys.argv[1:] or (sorted(glob.glob("lands/*_1.npz")) + sorted(glob.glob("lands/*_2.npz")) + sorted(glob.glob("weird/*.npz")))
for fn in files:
    name = ("w:" if fn.startswith("weird") else "") + fn.split("/")[1][:-4]
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    v1 = dict(v1); v1["N"] = cond["N"].ravel()
    f, r = W.features(d, v1)
    pickle.dump({"f": f, "r": r}, open(f"feat/{name}.pkl", "wb"))
    print(name, {k: round(float(v.mean()), 3) for k, v in f.items() if k in ("wood", "open", "heath", "wet", "water", "shore", "rock", "conifer", "farm")}, flush=True)
