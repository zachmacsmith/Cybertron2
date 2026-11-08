"""M7: an interaction through the economy: draining a fen around a village (20 years), and stopping heath management.
Runs M2 on a window around the village, then reads M4's food calendar and M5's goods before and after."""
import sys; sys.path.insert(0, "/home/user/cybertron2")
import json, numpy as np, niche as NI, succession as SU, seasonal as SE, trade as TR, test_niche as T
FOREST = list(T.FOREST)
def window_run(fn, site_i, use_fn, years, r=27):
    d, land, lab0, lab1, a0, a1, v0, v1, cond = T.run(fn)
    s = tuple(d["sites"][site_i])
    w = ((max(0, s[0] - r), s[0] + r + 1), (max(0, s[1] - r), s[1] + r + 1))
    L = SU.Land(d, window=w)
    dd = L.d
    cleared = ~np.isin(dd["eco"], FOREST)
    heath = np.isin(dd["eco"], ["lowland heath", "moor"])
    base = {"graze": np.where(cleared, np.where(heath, 0.2, 0.5), 0.0), "mow": np.where(dd["eco"] == "hay meadow", 0.8, 0.0),
            "burn": np.where(heath, 0.3, 0.0), "cut_bracken": np.where(heath, 0.6, 0.2), "cut_gorse": np.where(heath, 0.5, 0.0),
            "cut_reed": np.where(np.isin(dd["eco"], ["fen", "reedbed"]), 0.5, 0.0), "mow_fen": 0}
    base["mow"] = np.where(np.isin(dd["eco"], ["fen"]), 0.6, base["mow"])
    v = NI.vegetation(L.cond(), graze=base["graze"], mow=base["mow"], burn=base["burn"], canopy_open=cleared,
                      cut={"bracken": base["cut_bracken"], "gorse": base["cut_gorse"], "reed": base["cut_reed"]})
    st = SU.start(L, v)
    site = (s[0] - w[0][0], s[1] - w[1][0])
    def read(st):
        vv = {"T": st["T"].ravel(), "B": st["B"].ravel(), "canopy": st["v"]["canopy"] if "v" in st else v["canopy"],
              "shrub": st["v"]["shrub"] if "v" in st else v["shrub"], "field": (st["fi"], st["field"])}
        dd2 = dict(dd); dd2["eco"] = SU.classify(L, st) if "v" in st else dd["eco"]
        cal = SE.village_calendar(vv, dd2, site, radius_km=4.0)
        goods = TR.village_goods(TR.sources(vv, dd2), dd2, site, 4.0, float(dd["km"]))
        u, c = np.unique(dd2["eco"], return_counts=True)
        return cal, goods, dict(zip(u, (c / c.sum()).round(3)))
    st0 = dict(st)
    for y in range(3): st = SU.step(L, st, base)
    before = read(st)
    for y in range(years): st = SU.step(L, st, use_fn(base, dd, y))
    after = read(st)
    return before, after
def show(name, b, a):
    print("==", name)
    print("   food by season (x need)  before", [round(x, 2) for x in b[0]["season"]], " after", [round(x, 2) for x in a[0]["season"]])
    keys = sorted(set(b[1]) | set(a[1]))
    ch = [(k, round(b[1].get(k, 0), 1), round(a[1].get(k, 0), 1)) for k in keys if abs(b[1].get(k, 0) - a[1].get(k, 0)) > 0.25 * max(b[1].get(k, 0), 0.5)]
    print("   goods that changed (x need):", ch)
    ek = sorted(set(b[2]) | set(a[2]), key=lambda k: -max(b[2].get(k, 0), a[2].get(k, 0)))[:7]
    print("   land:", [(k, b[2].get(k, 0), a[2].get(k, 0)) for k in ek])
    return {"before": {"season": b[0]["season"], "goods": b[1], "land": {k: float(v) for k, v in b[2].items()}},
            "after": {"season": a[0]["season"], "goods": a[1], "land": {k: float(v) for k, v in a[2].items()}}}
out = {}
def drain(base, dd, y):
    u = dict(base); wet = np.isin(dd["eco"], ["fen", "reedbed", "wet grassland", "alder carr"])
    u["drain"] = np.where(wet, 1.0, 0.0); u["cut_reed"] = 0.0
    u["graze"] = np.where(wet, 0.5, base["graze"]); u["mow"] = np.where(wet, 0.0, base["mow"])
    return u
b, a = window_run("lands/fen_with_islands_1.npz", 0, drain, 20)
out["drain the fen (20 years)"] = show("drain the fen, 20 years", b, a)
def heath_lapse(base, dd, y):
    u = dict(base); heath = np.isin(dd["eco"], ["lowland heath", "moor"])
    u["burn"] = 0.0; u["cut_bracken"] = 0.0; u["cut_gorse"] = 0.0; u["graze"] = np.where(heath, 0.05, base["graze"])
    return u
b, a = window_run("lands/sand_country_1.npz", 0, heath_lapse, 20)
out["heath management lapses (20 years)"] = show("heath management lapses, 20 years", b, a)
def abandon(base, dd, y):
    return {"graze": 0.0}
b, a = window_run("lands/plain_1.npz", 0, abandon, 30)
out["village abandoned (30 years)"] = show("village abandoned, 30 years", b, a)
json.dump(out, open("m7_results.json", "w"), default=float)
