"""M2 calibration: controlled plots of uniform ground, a seed source or not, against the real timescales."""
import numpy as np, niche as NI, succession as SU, json, sys

def plot(F, R, N, h=60.0, n=21, wood_cols=0, S=0.0):
    sh = (n, n)
    d = {"h": np.full(sh, h), "sea": np.zeros(sh, bool), "lake": np.zeros(sh, bool), "river": np.zeros(sh, int)}
    land = SU.Land.__new__(SU.Land)
    land.d = dict(d, terrain=np.full(sh, "x"), system=np.full(sh, "x")); land.shape = sh
    land.cond0 = {"F": np.full(sh, F), "R": np.full(sh, R), "N": np.full(sh, N), "S": np.full(sh, S),
                  "alt": np.clip((NI.P["treeline_m"] - np.full(sh, h)) / NI.P["treeline_w"], 0, 1), "rock": np.zeros(sh, bool), "h": np.full(sh, h)}
    land.dN = np.zeros(sh); land.dF = np.zeros(sh); land.water = np.zeros(sh, bool)
    return land

def run(land, use0, use, years, wood_cols=0, deer=None, track=(9, 10)):
    """Settle the plot under use0 for 30 years (its managed state), then run `use` and watch the centre cells."""
    v = NI.vegetation(land.cond(), **{k: v for k, v in use0.items() if k in ("graze", "mow", "burn")},
                      canopy_open=np.broadcast_to(use0.get("open", False), land.shape))
    st = SU.start(land, v)
    if use0.get("open") or use0.get("graze", 0) > 0 or use0.get("mow", 0) > 0 or use0.get("burn", 0) > 0:
        st["T"][:] = 0.0; st["B"][:] = 0.0                # a managed open start
    if wood_cols:                                   # a wood along one side: the seed source
        st["T"][:, :wood_cols] = 0.85
    for _ in range(30):
        st = SU.step(land, st, use0); 
        if wood_cols: st["T"][:, :wood_cols] = np.maximum(st["T"][:, :wood_cols], 0.85)
    out = []
    for y in range(years):
        st = SU.step(land, st, use, deer=deer)
        if wood_cols: st["T"][:, :wood_cols] = np.maximum(st["T"][:, :wood_cols], 0.85)
        c = slice(track[0], track[1] + 1)
        lab = SU.classify(land, st)
        out.append({"T": float(st["T"][c, c].mean()), "B": float(st["B"][c, c].mean()), "lab": str(lab[track[0], track[0]])})
    return out

def first(out, f):
    for i, o in enumerate(out):
        if f(o): return i + 1
    return None

E = {}
# E1 Broadbalk: base-rich loam, a wood next to the field (abandoned arable)
o = run(plot(6.0, 7.0, 6.5), {"crop": 1.0, "open": True}, {}, 100, wood_cols=4, track=(5, 5))
E["E1 Broadbalk (base-rich, seed near)"] = {"scrub": first(o, lambda x: x["B"] >= 0.45 or x["T"] >= 0.3), "wood": first(o, lambda x: x["T"] >= 0.5), "target": "wood 25-40"}
# E2 Geescroft: acid loam, no wood near
o = run(plot(5.5, 4.0, 4.5), {"crop": 1.0, "open": True}, {}, 120, wood_cols=0)
E["E2 Geescroft (acid, seed far)"] = {"T30": round(o[29]["T"], 2), "wood": first(o, lambda x: x["T"] >= 0.5), "target": "T<0.2 at 30; wood 60-80"}
# E3 lowland heath, grazing and burning stop
o = run(plot(5.2, 3.0, 2.5), {"graze": 0.2, "burn": 0.3, "cut_bracken": 0.6, "cut_gorse": 0.5}, {}, 80, wood_cols=0)
E["E3 heath abandoned"] = {"T>0.1": first(o, lambda x: x["T"] >= 0.1), "wood": first(o, lambda x: x["T"] >= 0.5), "labels": [o[i]["lab"] for i in (4, 14, 29, 59)], "target": "invasion 10-15; birch wood 20-40"}
# E4 chalk grassland, grazing stops
o = run(plot(4.5, 8.0, 3.5, h=150), {"graze": 0.6}, {}, 80, wood_cols=0)
E["E4 chalk grazing stops"] = {"scrub": first(o, lambda x: x["B"] >= 0.45), "wood": first(o, lambda x: x["T"] >= 0.5), "labels": [o[i]["lab"] for i in (4, 14, 29, 59)], "target": "scrub 10-20"}
# E5 fen, cutting stops
o = run(plot(9.5, 6.2, 6.0, h=1), {"mow": 0.7, "cut_reed": 0.5}, {}, 80, wood_cols=0)
E["E5 fen uncut"] = {"wood": first(o, lambda x: x["T"] >= 0.5), "labels": [o[i]["lab"] for i in (4, 14, 29, 59)], "target": "carr 20-40"}
# E6 wood pasture: grazed wood with no thorny shelter
land = plot(6.0, 6.5, 6.0)
o = run(land, {}, {"graze": 0.6, "cut_bramble": 1.0, "cut_hawthorn": 1.0, "cut_blackthorn": 1.0}, 200)
E["E6 wood pasture, no recruitment"] = {"T": [round(o[i]["T"], 2) for i in (0, 49, 99, 149, 199)], "below 0.5": first(o, lambda x: x["T"] < 0.5), "target": "thins over a century or more"}
# E7 a felled wood regrowing, with deer
for deer in (0, 3, 6, 10, 15):
    o = run(plot(6.0, 6.5, 6.0), {"fell": 1.0}, {}, 80, wood_cols=4, deer=deer)
    E[f"E7 felled wood, deer {deer}/km2"] = {"wood": first(o, lambda x: x["T"] >= 0.5), "T40": round(o[39]["T"], 2)}
for k, v in E.items(): print(f"{k:42s} {v}")
json.dump(E, open("m2_calib.json", "w"), indent=1)
