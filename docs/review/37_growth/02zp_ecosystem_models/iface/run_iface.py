import sys, time, json, numpy as np
sys.path.insert(0, "../../../../..")   # the repository root, on branch climate-calibration (5ef36fe or later)
from cybertron2.landgen import write as W
import iface as I
OUT = {}
for cfg, spacing in [("settled lowland and frontier", 17.0), (None, 17.0), (None, 8.0)]:
    world, cells, report = W.generate({"name": "t", "seed": 7, "days": 10, "calendar": {"season": "summer", "day": 3, "season_days": 8},
                                       "generate": {"seed": 7, "configuration": cfg, "spacing_km": spacing, "settlements": 4 if spacing > 10 else 6}})
    km = 0.15; cover = cells["cover"]; sea = cells["sea"].astype(bool)
    sites = [(int(n["site_km"][1] / km), int(n["site_km"][0] / km)) for k, n in report["nodes"].items() if k.startswith("s")]
    d01 = np.hypot(sites[0][0] - sites[1][0], sites[0][1] - sites[1][1]) * km
    structs = {
        "S1 grid 1 km": (I.grid_labels(cover.shape, 7, sea), 1.0),
        "S2 grid 1 km, x5": (I.grid_labels(cover.shape, 7, sea), 5.0),
        "S2 grid 1 km, x15": (I.grid_labels(cover.shape, 7, sea), 15.0),
        "S2 grid 1 km, x30": (I.grid_labels(cover.shape, 7, sea), 30.0),
        "S3 nested 300 m/1 km/5 km": (I.nested_labels(cover.shape, sites, km, sea), 1.0),
        "S4 graph, ring 5 km": (I.graph_labels(cover.shape, sites, km, sea, 5.0), 1.0),
        "S5 graph, ring 2.5 km": (I.graph_labels(cover.shape, sites, km, sea, 2.5), 1.0),
    }
    res = {}
    for name, (lab, k) in structs.items():
        t = time.time(); Z = I.Zones(lab, cover, km, sites); nv = len(sites)
        steady = {v: 1.0 for v in range(nv)}
        base = I.run(Z, 25, steady, k, k, seed=1)
        # village 0 hunts hard for 2 years from year 15, then stops; others steady
        pol = lambda y, s: {v: (3.0 if (v == 0 and 15 <= y < 17) else (0.0 if (v == 0 and y >= 17) else 1.0)) for v in range(nv)}
        hh = I.run(Z, 25, pol, k, k, seed=1)
        b0 = {kk: np.mean([base["local"][y][0][kk] for y in range(13, 15)]) for kk in ("hare", "deer", "boar")}
        dep1 = {kk: hh["local"][15][0][kk] / max(b0[kk], 1e-9) for kk in b0}
        dep2 = {kk: hh["local"][16][0][kk] / max(b0[kk], 1e-9) for kk in b0}
        refill = {kk: next((y - 16 for y in range(17, 25) if hh["local"][y][0][kk] >= 0.9 * b0[kk]), None) for kk in b0}
        nb = {kk: hh["local"][16][1][kk] / max(np.mean([base["local"][y][1][kk] for y in range(13, 15)]), 1e-9) for kk in ("deer", "boar")}
        crop = [base["village"][y][v]["crop_loss"] for y in range(5, 25) for v in range(nv)]
        meat = np.mean([base["village"][y][v]["meat"] for y in range(5, 25) for v in range(nv)]) / (12 * 365)   # share of a real year's need
        stock = float(np.median([base["village"][y][v]["stock_loss"] for y in range(5, 25) for v in range(nv)]))
        allhard = I.run(Z, 40, {v: 3.0 for v in range(nv)}, k, k, seed=1)
        reg0 = base["region"][-1]
        coll = {kk: allhard["region"][-1][kk] / max(reg0[kk], 1e-9) for kk in ("deer", "boar", "wolf")}
        yrs20 = {kk: next((y for y in range(40) if allhard["region"][y][kk] < 0.2 * reg0[kk]), None) for kk in ("deer", "wolf")}
        res[name] = {"zones": Z.n, "seconds": round(time.time() - t, 1), "dep_1yr": dep1, "dep_2yr": dep2, "refill_years": refill,
                     "neighbour_2yr": nb, "crop_loss_median": float(np.median(crop)), "crop_loss_p90": float(np.percentile(crop, 90)),
                     "meat_share": float(meat), "all_hard_40yr": coll, "years_to_20pct": yrs20}
        r = res[name]; f = lambda d: ", ".join(f"{a} {b:.2f}" for a, b in d.items())
        print(f"[{(cfg or 'plain') + ' ' + str(int(spacing)) + 'km'}] {name:28s} zones {r['zones']:5d} ({r['seconds']}s) | hard 1yr: {f(dep1)} | 2yr: {f(dep2)} | refill yrs {r['refill_years']}"
              f" | neighbour {f(nb)} (d {d01:.0f} km) | crop loss med {r['crop_loss_median']:.1%} p90 {r['crop_loss_p90']:.1%} | meat {meat:.1%} | beasts lost {stock:.2f}/yr"
              f" | all hard 40y: {f(coll)} yrs<20% {yrs20}", flush=True)
    OUT[(cfg or "plain") + f" {int(spacing)} km"] = res
json.dump(OUT, open("iface.json", "w"), default=float)
