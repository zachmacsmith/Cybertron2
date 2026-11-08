import glob, json, sys, numpy as np, niche as NI, seasonal as SE, test_niche as T
sys.path.insert(0, "/home/user/cybertron2")
rows = []
for fn in sorted(glob.glob("lands/*_1.npz")) + sorted(glob.glob("lands/*_2.npz")):
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    for i, site in enumerate(d["sites"]):
        cal = SE.village_calendar(v1, d, tuple(site))
        cal4 = SE.village_calendar(v1, d, tuple(site), radius_km=4.0)
        eng = SE.engine_forage(d, tuple(site))
        terr = d["terrain"][tuple(site)]
        top = sorted(((k, sum(x) / 4) for k, x in cal["by"].items()), key=lambda kv: -kv[1])[:4]
        rows.append({"world": fn.split("/")[1][:-4], "site": i, "terrain": str(terr), "system": str(d["system"][tuple(site)]),
                     "wood": round(cal["wood_share"], 2), "season": [round(s, 2) for s in cal["season"]], "year": round(cal["year"], 2),
                     "storable": round(cal["storable_year"], 2), "year_4km": round(cal4["year"], 2), "wood_4km": round(cal4["wood_share"], 2), "engine_now": round(eng, 2), "top": [(k, round(x, 2)) for k, x in top],
                     "by": {k: [round(x, 3) for x in v] for k, v in cal["by"].items()}})
json.dump(rows, open("m4_results.json", "w"), indent=0)
print(f"{'world':34s} {'terrain':16s} wood  spring summer autumn winter | year storable | engine now | top sources")
for r in rows:
    print(f"{r['world'][:34]:34s} {r['terrain'][:16]:16s} {r['wood']:.2f}  " + "  ".join(f"{s:5.2f}" for s in r["season"]) +
          f" | {r['year']:4.2f} {r['storable']:4.2f} | {r['engine_now']:6.1f} | " + ", ".join(f"{k} {x}" for k, x in r["top"]))
s = np.array([r["season"] for r in rows]); e = np.array([r["engine_now"] for r in rows]); y = np.array([r["year"] for r in rows])
print("median season shares", np.median(s, 0).round(2), "year", np.median(y).round(2), "engine now", np.median(e).round(1),
      "ratio engine/real", np.median(e / np.maximum(y, 1e-6)).round(1))

import collections
grp = collections.defaultdict(list)
for r in rows:
    k = "fen or estuary" if r["by"]["eels"][2] > 0.5 else ("wooded" if r["wood"] > 0.1 else ("coast" if r["by"]["shellfish"][0] > 0.01 else "open farmland"))
    grp[k].append(r)
for k, rs in grp.items():
    s = np.array([r["season"] for r in rs])
    print(f"{k:16s} n={len(rs):3d} spring {np.median(s[:,0]):.2f} summer {np.median(s[:,1]):.2f} autumn {np.median(s[:,2]):.2f} winter {np.median(s[:,3]):.2f} | year {np.median([r['year'] for r in rs]):.2f} storable {np.median([r['storable'] for r in rs]):.2f} | 4 km {np.median([r['year_4km'] for r in rs]):.2f} (wood {np.median([r['wood_4km'] for r in rs]):.2f}) | engine {np.median([r['engine_now'] for r in rs]):.1f}")
