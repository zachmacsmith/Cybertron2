"""Round 3: the refined web (kinds1) on the regenerated land: fit, evaluate everywhere, then the decisive tests.
A. persistence, densities, variation, sensitivity;  B. web variants;  C. heavy hunting and recovery;  D. land change;
E. the communities that form in each world."""
import copy, json, pickle, sys, numpy as np, web as W, calibrate as C, rounds as R, kinds1
KN = {"selfcap": 2.5}
OUT = {}
def save(): json.dump(OUT, open("round3.json", "w"), default=float)

# ---- A: fit and evaluate
kinds = copy.deepcopy(kinds1.KINDS)
REF = C.REF + ["w:drowned_isles", "w:flat_marsh", "w:ancient_wildwood"]
fitted, hist = C.fit(kinds, iters=7, years=50, knobs=KN, verbose=False, worlds=REF)
pickle.dump(fitted, open("kinds_r3.pkl", "wb"))
res = R.evaluate(fitted, R.ALL, years=60, knobs=KN)
summ = R.summary(res, fitted)
sens = {}
for w in ["plain_1", "w:flat_marsh", "w:alpine", "w:drowned_isles", "w:ancient_wildwood"]:
    s = R.sensitivity(fitted, w, draws=12, years=40, extra=KN)
    for n, v in s.items():
        if v["spread"] is not None:
            sens.setdefault(n, []).append(v)
OUT["A"] = {"summary": summ, "factors": {n: fitted[n]["k"] / max(kinds1.KINDS[n]["k"], 1e-9) for n in fitted},
            "sens": {n: {"spread": float(np.median([x["spread"] for x in v])), "extinct": float(np.mean([x["extinct_share"] for x in v]))} for n, v in sens.items()}}
print("A done", flush=True); save()
# ---- B: variants
def variant(name):
    k = copy.deepcopy(fitted); kn = dict(KN)
    if name == "no wolves or lynx": k = {n: v for n, v in k.items() if n not in ("wolf", "lynx")}
    if name == "no fox": k = {n: v for n, v in k.items() if n != "fox"}
    if name == "specialists":
        for v in k.values():
            top = max(v["diet"].items(), key=lambda x: x[1])[0]; v["diet"] = {top: 1.0}
    if name == "generalists":
        for v in k.values():
            v["diet"] = {x: 1.0 for x in v["diet"]}
    if name == "no weather": kn.update({"weather_sd": 0.0, "p_hard_winter": 0.0})
    if name == "no switching (no refuges)":
        for v in k.values(): v["switch"] = 1.0
    if name == "no self-limit": kn.pop("selfcap")
    if name == "rabbits introduced":
        k["rabbit"] = copy.deepcopy(kinds1.PACK["rabbit"]); k["rabbit"]["k"] *= 0.5
    return k, kn
VW = ["plain_1", "upland_and_moor_1", "fen_with_islands_1", "settled_lowland_and_frontier_1", "w:alpine", "w:flat_marsh"]
base = R.evaluate(fitted, VW, years=60, knobs=KN)
OUT["B"] = {}
for v in ["no wolves or lynx", "no fox", "specialists", "generalists", "no weather", "no switching (no refuges)", "no self-limit", "rabbits introduced"]:
    k, kn = variant(v)
    e = R.evaluate(k, VW, years=60, knobs=kn)
    per = {}
    for n in k:
        if n not in base[VW[0]]: continue
        lost = sum(1 for w in VW if base[w][n]["persist"] and not e[w][n]["persist"])
        ch = [np.log(max(e[w][n]["dens"], 1e-9) / max(base[w][n]["dens"], 1e-9)) for w in VW if base[w][n]["persist"]]
        cv = [e[w][n]["cv"] for w in VW if e[w][n]["persist"] and e[w][n]["cv"] is not None]
        per[n] = {"lost": lost, "ratio": float(np.exp(np.median(ch))) if ch else None, "cv": float(np.median(cv)) if cv else None}
    OUT["B"][v] = {"lost_total": sum(p["lost"] for p in per.values()), "big": {n: round(p["ratio"], 2) for n, p in per.items() if p["ratio"] and not 0.67 < p["ratio"] < 1.5},
                   "mean_cv": float(np.mean([p["cv"] for p in per.values() if p["cv"] is not None])), "per": per}
    print("B", v, OUT["B"][v]["lost_total"], OUT["B"][v]["big"], flush=True); save()
base_cv = float(np.mean([np.median([base[w][n]["cv"] for w in VW if base[w][n]["persist"] and base[w][n]["cv"] is not None] or [0]) for n in fitted]))
OUT["B"]["baseline_mean_cv"] = base_cv
# ---- C: heavy hunting for 20 years, then stop
GAME = [n for n, v in fitted.items() if v["people"] > 0]
OUT["C"] = {}
for w in ["plain_1", "settled_lowland_and_frontier_1", "w:flat_marsh", "w:alpine"]:
    fr = R.feat(w)
    out0, rec0 = W.run(fr["f"], fr["r"], fitted, years=40, knobs=KN)
    pol_heavy = {n: 4.0 for n in GAME}
    out1, rec1 = W.run(fr["f"], fr["r"], fitted, years=20, knobs=KN, policy=pol_heavy, dens0=rec0["final"], seed=1)
    out2, rec2 = W.run(fr["f"], fr["r"], fitted, years=30, knobs=KN, dens0=rec1["final"], seed=2)
    r = {}
    for n in fitted:
        b = np.mean(out0[n][-10:])
        if b <= 1e-9: continue
        low = min(out1[n]) / b
        rec_y = next((i + 1 for i, x in enumerate(out2[n]) if x >= 0.9 * b), None)
        r[n] = {"low": float(low), "recover_years": rec_y, "hunted": n in GAME}
    OUT["C"][w] = r
    print("C", w, {n: (round(v["low"], 2), v["recover_years"]) for n, v in r.items() if v["hunted"]}, flush=True); save()
# ---- D: land change, from the settled state
def change(fr, kind):
    f = {k: v.copy() for k, v in fr["f"].items()}; r = {k: v.copy() for k, v in fr["r"].items()}
    if kind == "fell half the woods":
        m = f["wood"] > 0.3; cut = 0.5 * f["wood"] * m
        f["wood"] -= cut; f["open"] += cut; f["old"] *= np.where(m, 0.3, 1)
        for x in ("mast", "nuts"): r[x] *= np.where(m, 0.5, 1)
        r["grass"] += cut * 0.8; r["browse"] *= np.where(m, 1.2, 1)
    if kind == "drain the wetlands":
        for x in ("wet",): f[x] *= 0.2
        r["aquatic"] *= 0.25; r["fish"] *= 0.7; r["grass"] += fr["f"]["wet"] * 0.6
    if kind == "abandon the farms":
        f["shrub"] = np.clip(f["shrub"] + f["farm"] * 0.6, 0, 1); f["farm"] *= 0
        for x in ("crops", "livestock", "stores"): r[x] *= 0
        r["browse"] += fr["f"]["farm"] * 0.5; r["fruit"] += fr["f"]["farm"] * 0.4
    return f, r
OUT["D"] = {}
for w in ["plain_1", "fen_with_islands_1", "settled_lowland_and_frontier_1"]:
    fr = R.feat(w)
    out0, rec0 = W.run(fr["f"], fr["r"], fitted, years=40, knobs=KN)
    OUT["D"][w] = {}
    for kind in ["fell half the woods", "drain the wetlands", "abandon the farms"]:
        f2, r2 = change(fr, kind)
        out1, rec1 = W.run(f2, r2, fitted, years=30, knobs=KN, dens0=rec0["final"], seed=3, people=(kind != "abandon the farms"))
        ch = {n: float(np.mean(out1[n][-10:]) / max(np.mean(out0[n][-10:]), 1e-9)) for n in fitted if np.mean(out0[n][-10:]) > 1e-9}
        ev = {"stock_killed": (float(np.mean(rec1["stock_killed"][-10:])), float(np.mean(rec0["stock_killed"][-10:]))),
              "crop_damage": (float(np.mean(rec1["crop_damage"][-10:])), float(np.mean(rec0["crop_damage"][-10:])))}
        OUT["D"][w][kind] = {"ratios": ch, "events": ev}
        print("D", w, kind, {n: round(x, 2) for n, x in ch.items() if not 0.67 < x < 1.5}, flush=True)
    save()
# ---- E: communities by world
OUT["E"] = {w: {n: {"dens": res[w][n]["dens"], "hab": res[w][n]["hab"], "persist": res[w][n]["persist"]} for n in fitted} for w in R.ALL}
OUT["E_rec"] = {w: res[w]["_rec"] for w in R.ALL}
save(); print("all done")
