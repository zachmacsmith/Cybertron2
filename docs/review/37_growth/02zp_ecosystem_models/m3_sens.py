import json, itertools, numpy as np, populations as PO, run_m3 as R
fn = "lands/settled_lowland_and_frontier_1.npz"
d, pt = R.load(fn)
rows = []
for bs, half, Kw in itertools.product([6.0, 8.0, 10.0, 12.0], [2.0, 4.0, 6.0], [9.0, 12.0, 15.0]):
    PO.P["wood"]["browse_stop"] = bs; PO.P["wolf"]["half"] = half; PO.P["deer"]["K_wood"] = Kw
    for wolves in (True, False):
        w = PO.World(pt, seed=3, wolves=wolves)
        for y in range(100): w.step({"hunt": "light"})
        L = w.log[-10:]
        rows.append({"browse_stop": bs, "half": half, "K_wood": Kw, "wolves": wolves,
                     "deer": round(np.mean([r["deer_wood"] for r in L]), 2), "wolves_n": round(np.mean([r["wolves"] for r in L]), 1),
                     "wood_change": round(L[-1]["wood"] / w.log[0]["wood"] - 1, 3), "stock_kills": round(np.mean([r["stock_kills"] for r in L]), 1)})
json.dump(rows, open("m3_sens.json", "w"))
import collections
print("wood change over 100 years (with wolves / without), by browse_stop x K_wood, half=4")
for bs in [6.0, 8.0, 10.0, 12.0]:
    line = []
    for Kw in [9.0, 12.0, 15.0]:
        a = [r for r in rows if r["browse_stop"] == bs and r["K_wood"] == Kw and r["half"] == 4.0]
        ww = [r for r in a if r["wolves"]][0]; nw = [r for r in a if not r["wolves"]][0]
        line.append(f"K{Kw:.0f}: {ww['wood_change']:+.2f}/{nw['wood_change']:+.2f} (deer {ww['deer']}/{nw['deer']})")
    print(f" stop {bs:4.0f}  " + "  ".join(line))
print("wolves' effect on deer, by half-saturation (K 12, stop 8):", [(r["half"], r["deer"], r["wolves_n"]) for r in rows if r["K_wood"] == 12 and r["browse_stop"] == 8 and r["wolves"]])
