import sys, glob, numpy as np, collections
import niche as NI
FOREST = {"oak-ash wood", "beech wood", "alder carr", "birch and pine wood", "upland oak wood"}
def run(fn, verbose=False):
    d = dict(np.load(fn, allow_pickle=True))
    land = ~d["sea"] & ~d["lake"] & (d["eco"] != "water")
    cond = NI.conditions(d)
    # natural: nothing grazed or burnt
    v0 = NI.vegetation(cond)
    lab0 = NI.label(v0, cond, d["h"], d["terrain"]).reshape(d["h"].shape)
    # settled: the generator's cleared ground, grazed; wood stays
    cleared = ~np.isin(d["eco"], list(FOREST))
    gz = np.where(cleared, 0.5, 0.0)
    gz = np.where(np.isin(d["eco"], ["lowland heath", "moor"]), 0.2, gz)
    mow = np.where(d["eco"] == "hay meadow", 0.8, 0.0)
    heath = np.isin(d["eco"], ["lowland heath", "moor"])
    v1 = NI.vegetation(cond, graze=gz, mow=mow, canopy_open=cleared, burn=np.where(heath, 0.3, 0.0), cut={"bracken": np.where(heath, 0.6, 0.2), "gorse": np.where(heath, 0.5, 0.0)})
    lab1 = NI.label(v1, cond, d["h"], d["terrain"]).reshape(d["h"].shape)
    a0 = (lab0 == d["eco0"])[land].mean(); a1 = (lab1 == d["eco"])[land].mean()
    return d, land, lab0, lab1, a0, a1, v0, v1, cond
if __name__ == "__main__":
    files = sorted(glob.glob("lands/*_1.npz"))
    conf0 = collections.Counter(); conf1 = collections.Counter(); A = []
    for fn in files:
        d, land, lab0, lab1, a0, a1, *_ = run(fn)
        A.append((fn.split("/")[1][:-4], a0, a1))
        for x, y in zip(d["eco0"][land], lab0[land]): conf0[(x, y)] += 1
        for x, y in zip(d["eco"][land], lab1[land]): conf1[(x, y)] += 1
    for n, a0, a1 in A: print(f"{n:40s} natural {a0:.2f}  settled {a1:.2f}")
    print("mean", np.mean([a[1] for a in A]).round(3), np.mean([a[2] for a in A]).round(3))
    for nm, conf in (("natural", conf0), ("settled", conf1)):
        print("==", nm, "largest disagreements (generator -> niche)")
        tot = collections.Counter()
        for (x, y), n in conf.items(): tot[x] += n
        for (x, y), n in sorted(conf.items(), key=lambda kv: -kv[1]):
            if x != y and n > 0.002 * sum(tot.values()): print(f"   {x:22s} -> {y:22s} {n/tot[x]:.0%} of {x} ({n})")
