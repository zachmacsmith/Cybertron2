import glob, json, collections, numpy as np, trade as TR, test_niche as T
import sys; sys.path.insert(0, "/home/user/cybertron2")
out = []; spec_count = collections.Counter(); lack_count = collections.Counter(); tot_v = 0
for fn in sorted(glob.glob("lands/*_1.npz")) + sorted(glob.glob("lands/*_2.npz")) + sorted(glob.glob("lands/*_3.npz")):
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    src = TR.sources(v1, d); esrc = TR.engine_sources(d)
    km = float(d["km"])
    vill = [(TR.village_goods(src, d, tuple(s), 4.0, km), TR.village_goods(esrc, d, tuple(s), 4.0, km, goods={g: TR.GOODS[g] for g in TR.ENGINE_GOODS}))
            for s in d["sites"]]
    if len(vill) < 2: continue
    def stats(which, goods):
        has = [{g for g, x in vv[which].items() if x >= 1.0} for vv in vill]
        n = len(has)
        allg = set().union(*has)
        spec = [g for g in allg if sum(g in h for h in has) <= max(1, n // 3)]           # held by a third of villages or fewer
        needs = [g for g, (need, *_ ) in TR.GOODS.items() if need and g in goods]
        # dependence edges: a village lacking a need that another village has
        edges = sum(1 for i, h in enumerate(has) for g in needs if g not in h and any(g in hj for j, hj in enumerate(has) if j != i))
        unmet = sum(1 for h in has for g in needs if g not in h and not any(g in hj for hj in has))
        diff = np.mean([len(a ^ b) / max(len(a | b), 1) for i, a in enumerate(has) for b in has[i + 1:]])
        return {"goods_in_region": len(allg), "specialties": sorted(spec), "dep_edges": edges, "unmet_needs_region": unmet,
                "dissimilarity": round(float(diff), 2), "per_village": [sorted(h) for h in has]}
    rec = {"world": fn.split("/")[1][:-4], "proposal": stats(0, TR.GOODS), "engine": stats(1, TR.ENGINE_GOODS)}
    out.append(rec)
    for g in rec["proposal"]["specialties"]: spec_count[g] += 1
    for h in rec["proposal"]["per_village"]:
        tot_v += 1
        for g, (need, *_ ) in TR.GOODS.items():
            if need and g not in h: lack_count[g] += 1
json.dump(out, open("m5_results.json", "w"), indent=0)
P = [r["proposal"] for r in out]; E = [r["engine"] for r in out]
f = lambda L, k: np.median([x[k] for x in L])
print(f"regions {len(out)}")
print(f"engine now:  goods {f(E,'goods_in_region')}, specialties {np.median([len(x['specialties']) for x in E])}, dependence edges {f(E,'dep_edges')}, dissimilarity {f(E,'dissimilarity')}")
print(f"proposal:    goods {f(P,'goods_in_region')}, specialties {np.median([len(x['specialties']) for x in P])}, dependence edges {f(P,'dep_edges')}, dissimilarity {f(P,'dissimilarity')}, unmet in region {f(P,'unmet_needs_region')}")
print("specialties, how often (regions):", spec_count.most_common())
print("needs lacked, share of villages:", [(g, round(n / tot_v, 2)) for g, n in lack_count.most_common()])
for r in out[:4] + [x for x in out if "fen" in x["world"]][:2]:
    print(r["world"], "| proposal specialties", r["proposal"]["specialties"], "| engine", r["engine"]["specialties"])
