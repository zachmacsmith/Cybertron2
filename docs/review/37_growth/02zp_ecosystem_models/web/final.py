"""02zp part two: the final run of the web (W2, kinds2 with the growth check and the last pass), driven by 37.4's climate.
A: every world (steady era); B: each era; C: packs, introductions and removals; D: heavy hunting and recovery, near and far."""
import json, copy, glob, numpy as np, web2 as W2, kinds2, calibrate as C, climate_bridge as CB
import tune, tune2
from tune2 import refit, assess
ERA_PACKS = ("aurochs", "bison", "wild horse", "elk", "rabbit", "fallow deer")
BASE = {n: k for n, k in kinds2.KINDS.items() if n not in ERA_PACKS}
tune.BASE = tune2.BASE = BASE
SPEC = "/home/user/cyb-climate/cybertron2/specs/plenty/brookend.yaml"
ser = {e: CB.seasons(SPEC, e, years=80) for e in ("steady", "warm", "cold", "wet", "dry", "stormy")}
_, NORMAL = CB.weather_fn(ser["steady"])
WF = {e: CB.weather_fn(s, NORMAL)[0] for e, s in ser.items()}
KN = lambda e="steady", **x: dict({"crowd": 10 / 3, "disease": 0.03, "weather_fn": WF[e], "epi_p0": 0.05}, **x)
ALL = sorted(p.split("/")[1][:-4] for p in glob.glob("feat/*.pkl"))
OUT = {"eras_climate": {e: {s: {k: float(np.mean([r[s][k] for r in v])) for k in ("temp", "wet", "frost", "snow")} for s in v[0]} for e, v in ser.items()}}
def save(): json.dump(OUT, open("final.json", "w"), default=float)
SC = refit(KN()); OUT["scale"] = SC; save(); print("refit", {f: round(v, 2) for f, v in SC.items()}, flush=True)

def run_world(w, kinds, kn, years=70, people=True, policy=None, seed=1):
    fr = C.load(w); land = fr["f"]["land"]
    o, rec = W2.run(fr["f"], fr["r"], kinds, years=years, scale=SC, knobs=kn, people=people, policy=policy, seed=seed)
    r = {}
    for n, k in kinds.items():
        s_ = np.array(o[n][-40:]); m = float(s_.mean()); hab = float((rec["suit"][n] * land).sum() / land.sum())
        r[n] = {"dens": m, "hab": hab, "rel": (m / hab / k["ref"]) if hab > 0.003 else None, "cv": float(s_.std() / m) if m > 1e-9 else None,
                "persist": (m > 0.01 * k["ref"] * hab) if hab > 0.003 else None}
    r["_events"] = {"crop": float(np.mean(rec["crop_damage"][-40:])), "stock": float(np.mean(rec["stock_killed"][-40:])),
                    "store": float(np.mean(rec["store_loss"][-40:]))}
    return r, o, rec

# A: every world
A = {}
for w in ALL:
    A[w], _, _ = run_world(w, BASE, KN())
OUT["A"] = A; save(); print("A done", flush=True)
# B: eras on four worlds
EW = ["plain_1", "upland_and_moor_1", "fen_with_islands_1", "settled_lowland_and_frontier_1"]
B = {}
for e in WF:
    B[e] = {w: run_world(w, BASE, KN(e))[0] for w in EW}
    print("B", e, flush=True)
OUT["B"] = B; save()
# C: packs and removals on representative worlds
Cr = {}
def compare(label, kinds, worlds, people=True, policy=None):
    res = {}
    for w in worlds:
        a, _, _ = run_world(w, BASE, KN(), people=people)
        b, _, _ = run_world(w, kinds, KN(), people=people, policy=policy)
        res[w] = {"added": {n: b[n] for n in kinds if n not in BASE},
                  "moved": {n: b[n]["dens"] / a[n]["dens"] for n in BASE if n in kinds and a[n]["dens"] > 1e-9 and not 0.8 < b[n]["dens"] / a[n]["dens"] < 1.25},
                  "removed_effect": {n: b[n]["dens"] / a[n]["dens"] for n in kinds if n in a and a[n]["dens"] > 1e-9 and not 0.8 < b[n]["dens"] / a[n]["dens"] < 1.25} if len(kinds) < len(BASE) else None}
    Cr[label] = res; OUT["C"] = Cr; save(); print("C", label, {w: (list(v["added"].items())[:1] and {n: round(x["rel"] or 0, 2) for n, x in v["added"].items()}, {n: round(x, 2) for n, x in v["moved"].items()}) for w, v in res.items()}, flush=True)
mega = dict(BASE); mega.update({n: kinds2.KINDS[n] for n in ("aurochs", "bison", "wild horse", "elk")})
compare("wildwood megafauna, no people", mega, ["w:ancient_wildwood", "settled_lowland_and_frontier_1", "w:cold_north_moor"], people=False)
compare("wildwood megafauna, hunted hard", mega, ["w:ancient_wildwood", "settled_lowland_and_frontier_1", "w:cold_north_moor"], policy={n: 6.0 for n in ("aurochs", "bison", "wild horse", "elk")})
compare("rabbits introduced", dict(BASE, rabbit=kinds2.KINDS["rabbit"]), ["plain_1", "scarp_and_vale_1", "sand_country_1"])
compare("fallow deer introduced", dict(BASE, **{"fallow deer": kinds2.KINDS["fallow deer"]}), ["plain_1", "settled_lowland_and_frontier_1"])
compare("fox removed", {n: k for n, k in BASE.items() if n != "fox"}, ["plain_1", "upland_and_moor_1", "settled_lowland_and_frontier_1"])
compare("wolves and lynx removed", {n: k for n, k in BASE.items() if n not in ("wolf", "lynx")}, ["settled_lowland_and_frontier_1", "w:ancient_wildwood", "upland_and_moor_1"])
# D: heavy hunting near villages for 15 years, then stop: near and far
GAME = ["red deer", "roe deer", "wild boar", "brown hare", "red grouse", "beaver", "eel", "wildfowl", "otter", "crane"]
D = {}
for w in ["plain_1", "settled_lowland_and_frontier_1", "fen_with_islands_1"]:
    fr = C.load(w); near = fr["f"]["farm"] > 0.05
    o0, r0 = W2.run(fr["f"], fr["r"], BASE, years=40, scale=SC, knobs=KN(), seed=1)
    o1, r1 = W2.run(fr["f"], fr["r"], BASE, years=15, scale=SC, knobs=KN(), policy={n: 5.0 for n in GAME}, dens0=r0["final"], seed=2)
    o2, r2 = W2.run(fr["f"], fr["r"], BASE, years=30, scale=SC, knobs=KN(), dens0=r1["final"], seed=3)
    res = {}
    for n in GAME:
        if n not in BASE: continue
        su = r0["suit"][n]; base_near = float((r0["final"][n] * near).sum()); hunted_near = float((r1["final"][n] * near).sum())
        b = np.mean(o0[n][-10:])
        if b <= 1e-9: continue
        res[n] = {"near_after": hunted_near / max(base_near, 1e-9), "region_low": float(min(o1[n]) / b),
                  "recover": next((i + 1 for i, x in enumerate(o2[n]) if x >= 0.9 * b), None)}
    D[w] = res; print("D", w, {n: (round(v["near_after"], 2), round(v["region_low"], 2), v["recover"]) for n, v in res.items()}, flush=True)
OUT["D"] = D; save(); print("all done", flush=True)
