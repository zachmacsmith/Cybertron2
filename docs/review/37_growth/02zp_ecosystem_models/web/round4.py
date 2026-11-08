"""Round 4, on W2 with the standard stabilisers and nine food scales (calib3): every kind everywhere, sensitivity, the era and
introduction packs as dynamics, hunting and recovery, land change, food chains. Outcomes are read as dynamics: displacement and
variation are results; only model artefacts and outcomes decided by guessed numbers are faults."""
import copy, json, glob, numpy as np, web2 as W2, kinds2, calibrate as C
from calib2 import ERA_OUT
SCALE = json.load(open("scale3.json"))
ALL = sorted(p.split("/")[1][:-4] for p in glob.glob("feat/*.pkl"))
BASE = {n: k for n, k in kinds2.KINDS.items() if n not in ERA_OUT}
OUT = {}
def save(): json.dump(OUT, open("round4.json", "w"), default=float)

def ev(kinds, worlds, years=60, last=25, knobs=None, policy=None, people=True, seed=0, scale=SCALE):
    res = {}
    for w in worlds:
        fr = C.load(w); land = fr["f"]["land"]
        out, rec = W2.run(fr["f"], fr["r"], kinds, years=years, seed=seed, scale=scale, knobs=knobs, policy=policy, people=people)
        r = {}
        for n, k in kinds.items():
            hab = float((rec["suit"][n] * land).sum() / land.sum()); ser = np.array(out[n][-last:]); m = float(ser.mean())
            r[n] = {"hab": hab, "dens": m, "rel": (m / hab / (k["ref"] or 1)) if hab > 0.003 else None,
                    "cv": float(ser.std() / m) if m > 1e-9 else None, "persist": (m > 0.01 * (k["ref"] or 1) * hab) if hab > 0.003 else None,
                    "series": [round(x, 4) for x in out[n]]}
        r["_rec"] = {"crop": float(np.mean(rec["crop_damage"][-last:])), "stock": float(np.mean(rec["stock_killed"][-last:])),
                     "store": float(np.mean(rec["store_loss"][-last:])), "take": {n: float(np.mean(v[-last:])) for n, v in rec["take"].items()},
                     "final": rec["final"]}
        res[w] = r
    return res

def summ(res, kinds):
    o = {}
    for n in kinds:
        per = [r[n]["persist"] for r in res.values() if r[n]["persist"] is not None]
        rel = [r[n]["rel"] for r in res.values() if r[n]["rel"] and r[n]["persist"]]
        cv = [r[n]["cv"] for r in res.values() if r[n]["persist"] and r[n]["cv"] is not None]
        d = [r[n]["dens"] for r in res.values() if r[n]["persist"]]
        o[n] = {"worlds": len(per), "persists": (sum(per) / len(per)) if per else None, "rel": float(np.median(rel)) if rel else None,
                "rel_range": [float(np.percentile(rel, 10)), float(np.percentile(rel, 90))] if len(rel) > 3 else None,
                "year_cv": float(np.median(cv)) if cv else None, "between_cv": float(np.std(d) / np.mean(d)) if len(d) > 2 and np.mean(d) > 0 else None}
    return o

if __name__ == "__main__":
    # A: every kind on every world
    res = ev(BASE, ALL)
    OUT["A"] = summ(res, BASE)
    OUT["A_worlds"] = {w: {n: {k: v for k, v in r[n].items() if k != "series"} for n in BASE} for w, r in res.items()}
    print("A done", flush=True); save()
    # A2: sensitivity: every food scale and every kind's b and m by lognormal(0, 0.25)
    rng = np.random.default_rng(11); SW = ["plain_1", "upland_and_moor_1", "w:flat_marsh", "w:ancient_wildwood"]
    base_d = {w: {n: res[w][n]["dens"] for n in BASE} for w in SW}
    ext = {n: 0 for n in BASE}; cnt = {n: 0 for n in BASE}; spread = {n: [] for n in BASE}
    for i in range(10):
        sc = {f: v * float(np.exp(rng.normal(0, 0.25))) for f, v in SCALE.items()}
        kk = copy.deepcopy(BASE)
        for k in kk.values():
            k["b"] *= float(np.exp(rng.normal(0, 0.25))); k["m"] *= float(np.exp(rng.normal(0, 0.25)))
        e = ev(kk, SW, years=50, scale=sc, seed=100 + i)
        for w in SW:
            for n in BASE:
                if res[w][n]["persist"]:
                    cnt[n] += 1
                    if not e[w][n]["persist"]: ext[n] += 1
                    if base_d[w][n] > 0: spread[n].append(np.log(max(e[w][n]["dens"], 1e-9) / base_d[w][n]))
    OUT["A2"] = {n: {"extinct": ext[n] / cnt[n] if cnt[n] else None, "spread": float(np.std(spread[n])) if spread[n] else None} for n in BASE}
    print("A2 done", flush=True); save()
    # B: era and introduction packs, as dynamics (each from the settled base state)
    OUT["B"] = {}
    tests = {
        "wildwood megafauna, no people": (["aurochs", "bison", "wild horse", "elk"], False, ["w:ancient_wildwood", "settled_lowland_and_frontier_1", "w:flat_marsh", "w:cold_north_moor"]),
        "wildwood megafauna, hunted": (["aurochs", "bison", "wild horse", "elk"], True, ["w:ancient_wildwood", "settled_lowland_and_frontier_1", "w:flat_marsh", "w:cold_north_moor"]),
        "rabbits introduced": (["rabbit"], True, ["plain_1", "scarp_and_vale_1", "sand_country_1"]),
        "fallow deer introduced": (["fallow deer"], True, ["plain_1", "settled_lowland_and_frontier_1"]),
    }
    for name, (add, ppl, ws) in tests.items():
        kk = dict(BASE); kk.update({n: kinds2.KINDS[n] for n in add})
        hunt = {n: 3.0 for n in add} if ppl else None
        e = ev(kk, ws, people=ppl, policy=hunt)
        b = ev(BASE, ws, people=ppl)
        OUT["B"][name] = {w: {"added": {n: {k: v for k, v in e[w][n].items() if k != "series"} for n in add},
                              "residents": {n: e[w][n]["dens"] / b[w][n]["dens"] for n in BASE if b[w][n]["dens"] > 1e-9},
                              "series": {n: e[w][n]["series"] for n in add}} for w in ws}
        print("B", name, {w: {n: round(v["rel"] or 0, 2) for n, v in OUT["B"][name][w]["added"].items()} for w in ws}, flush=True)
        print("   residents moved >1.5x:", {w: {n: round(x, 2) for n, x in OUT["B"][name][w]["residents"].items() if not 0.67 < x < 1.5} for w in ws}, flush=True)
        save()
    # C: heavy hunting for 15 years then stop, from the settled state
    OUT["C"] = {}
    GAME = [n for n, k in BASE.items() if k["people"] > 0]
    for w in ["plain_1", "settled_lowland_and_frontier_1", "w:flat_marsh", "upland_and_moor_1"]:
        fr = C.load(w)
        o0, r0 = W2.run(fr["f"], fr["r"], BASE, years=40, scale=SCALE)
        o1, r1 = W2.run(fr["f"], fr["r"], BASE, years=15, scale=SCALE, policy={n: 5.0 for n in GAME}, dens0=r0["final"], seed=1)
        o2, r2 = W2.run(fr["f"], fr["r"], BASE, years=30, scale=SCALE, dens0=r1["final"], seed=2)
        OUT["C"][w] = {}
        for n in BASE:
            b = np.mean(o0[n][-10:])
            if b <= 1e-9: continue
            OUT["C"][w][n] = {"low": float(min(o1[n]) / b), "recover": next((i + 1 for i, x in enumerate(o2[n]) if x >= 0.9 * b), None),
                              "hunted": n in GAME}
        print("C", w, {n: (round(v["low"], 2), v["recover"]) for n, v in OUT["C"][w].items() if v["hunted"]}, flush=True); save()
    print("all done", flush=True)
