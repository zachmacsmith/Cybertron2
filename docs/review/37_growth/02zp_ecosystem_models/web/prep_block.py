"""Features at other patch sizes (block 3 = 450 m, 7 = 1 km, 15 = 2.25 km) for the resolution test."""
import sys, pickle, os, numpy as np, test_niche as T, web as W
os.makedirs("featb", exist_ok=True)
for fn in ["lands/plain_1.npz", "lands/upland_and_moor_1.npz", "lands/settled_lowland_and_frontier_1.npz"]:
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    v1 = dict(v1); v1["N"] = cond["N"].ravel()
    for b in (3, 15):
        f, r = W.features(d, v1, block=b)
        pickle.dump({"f": f, "r": r}, open(f"featb/{fn.split('/')[1][:-4]}_b{b}.pkl", "wb")); print(fn, b, f["land"].shape, flush=True)
