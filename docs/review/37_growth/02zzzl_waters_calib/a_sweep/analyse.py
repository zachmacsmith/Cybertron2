"""W-108 sweep, the tables (brief.md sections 1 to 4), read from data/worlds/<id>.json (sweep_world.py's output).

    python3 docs/review/37_growth/02zzzl_waters_calib/a_sweep/analyse.py

Writes data/tables.json (every number sweep.md quotes, small) and prints the markdown tables. Definitions:
- **food a night at best**: a stock's most sustained take a night (sweep_world.best_*: the renewal rule's maximum), x 0.46 food a kg;
- **passed**: the heads of a run at a village's stretch on a night, counted as the engine's tally counts them, before any take; kg by
  the kind's taken goods (eel 0.58, salmon 3.06, lamprey 0.19 kg of fish a head), food at 0.46 a kg;
- a **village** is a settled node on a river that a kind runs; the wild nodes (unexplored) are reported apart;
- **need**: ten people, 11 food a night, 12 in winter (brief.md); a season is 8 nights;
- **a year** is an ecology year (32 days from spring's first day); only whole years are read.
"""
from __future__ import annotations

import glob
import json
import math
import os
import statistics as stt
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SEASONS = ("spring", "summer", "autumn", "winter")
NEED = {"spring": 11.0, "summer": 11.0, "autumn": 11.0, "winter": 12.0}
FOOD_KG = 0.46
KG = {"eel": 0.58, "salmon": 3.06, "lamprey": 0.19}
S = 8
Y = 32


def load_all():
    idx = {r["id"]: r for r in json.load(open(os.path.join(DATA, "worlds_index.json")))["rows"]}
    out = {}
    for p in sorted(glob.glob(os.path.join(DATA, "worlds", "*.json"))):
        d = json.load(open(p))
        if d.get("error"):
            print("ERROR", d["id"], d["error"], file=sys.stderr)
            continue
        d["meta"] = idx.get(d["id"], {"id": d["id"], "family": "eelmouth", "kind": "Eelmouth (live run 1's world)"})
        out[d["id"]] = d
    return out


def rain_of(d):
    g = ((d["meta"].get("spec") or {}).get("generate") or {})
    return g.get("rain_mm", 900.0)


def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def med(xs):
    return round(q(xs, 0.5), 3) if xs else None


# ---------------------------------------------------------------------- section 1 and 2
def worlds_table(D):
    rows = []
    for wid, d in D.items():
        c = d["census_maker"]
        vs = [v for v in c["villages"].values() if not v.get("wild")]
        types = sorted({t for v in vs for t in v["types"]})
        rows.append({"world": wid, "family": d["meta"].get("family"), "kind": d["meta"].get("kind"), "rain_mm": rain_of(d),
                     "villages": len(vs), "on a river": sum(1 for v in vs if v.get("on_river")),
                     "water types at villages": types,
                     "bodies by kind": dict(sorted(_count(b["kind"] for b in c["bodies"].values()).items())),
                     "lake km2 at villages": round(sum(v["lake_km2"] for v in vs), 2)})
    return rows


def _count(xs):
    out = defaultdict(int)
    for x in xs:
        out[x] += 1
    return out


def body_rows(D, variant="census_maker"):
    rows = []
    for wid, d in D.items():
        c = d[variant]
        for bid, b in c["bodies"].items():
            ps = [c["parcels"][p] for p in b["parcels"] if p in c["parcels"]]
            types = sorted({p["type"] for p in ps if p["type"]})
            f = b.get("fish") or {}
            rows.append({"world": wid, "body": bid, "kind": b["kind"], "type": types[0] if types else b["kind"],
                         "river_km": b.get("river_km"), "big_river_km": b.get("big_river_km"), "km2": b.get("km2"),
                         "parcels": len(ps), "units": b.get("parcel_units"), "K": f.get("K"), "r": f.get("r"),
                         "renewal": f.get("renewal") or ("periodic->fast" if f else None),
                         "best_food_night_summer": round((b.get("fish_best_night") or {}).get("summer", 0.0) * FOOD_KG, 3),
                         "best_food_night_winter": round((b.get("fish_best_night") or {}).get("winter", 0.0) * FOOD_KG, 3),
                         "web_fish_K_kg": b.get("web_fish_K_kg"), "nodes": b.get("nodes")})
    return rows


def parcel_rows(D):
    rows = []
    for wid, d in D.items():
        for pid, p in d["census_generated"]["parcels"].items():
            rows.append({"world": wid, "parcel": pid, **{k: p[k] for k in ("cover", "size", "type", "shallows_K", "elevation", "run_reach", "pinch")},
                         "best_food_night": {s: round((p["shallows_best_night"] or {}).get(s, 0.0) * FOOD_KG, 3) for s in SEASONS}})
    return rows


def by_type(rows, key, val):
    g = defaultdict(list)
    for r in rows:
        if r.get(val) is not None:
            g[r[key]].append(r[val])
    return {k: {"n": len(v), "median": med(v), "min": round(min(v), 3), "max": round(max(v), 3)} for k, v in sorted(g.items())}


def village_rows(D):
    rows = []
    for wid, d in D.items():
        cg, cm = d["census_generated"], d["census_maker"]
        for n, v in cm["villages"].items():
            g = cg["villages"].get(n, {})
            rows.append({"world": wid, "family": d["meta"].get("family"), "rain_mm": rain_of(d), "village": v["name"], "node": n,
                         "wild": v.get("wild", False), "elevation": v.get("elevation"), "on_river": v.get("on_river"),
                         "types": v["types"], "stretch_km": v.get("stretch_km"), "big_km": v.get("big_km"),
                         "upstream_river_km": v.get("upstream_river_km"), "catchment_km2": v.get("catchment_km2"),
                         "stretches_to_mouth": v.get("stretches_to_mouth"), "salmon_river": v.get("salmon_river"),
                         "lake_km2": v["lake_km2"], "river_km_home_ring": v["river_km_home_ring"],
                         "fish_K_generated": g.get("fish_K", 0.0), "fish_K_maker": v["fish_K"],
                         "fish_food_night_maker": {s: round(v["fish_best_night"][s] * FOOD_KG, 3) for s in SEASONS},
                         "shallows_K": v["shallows_K"], "shallows_food_night": {s: round(v["shallows_best_night"][s] * FOOD_KG, 3) for s in SEASONS},
                         "web_fish_K_kg": v["web_fish_K_kg"], "web_water_km2": v["web_water_km2"]})
    return rows


# ---------------------------------------------------------------------- section 3
def run_years(d, arm="runs_cue"):
    """{(village, kind, year): {...}} from one world's runs."""
    r = d.get(arm) or {}
    if not r.get("active"):
        return {}
    e0 = int(r["eco_day0"])
    span = range(e0, e0 + r["years"] * Y)
    WS = {k: min(int(i) * S + int(w[0]) for i, w in v["seasons"].items()) for k, v in r["kinds"].items()}   # the window's first day
    starts = defaultdict(float)
    cause_of = {}
    for d1, k, key, h, cause in r["starts"]:
        if h < 0.5:
            continue
        starts[(d1, k, key)] += h
        cause_of[(d1, k, key)] = cause
    out = {}
    for n in r["villages"]:
        lag = int(r["lag_from_mouth"][n])
        nights = defaultdict(lambda: defaultdict(float))
        for day, k, h, held in r["passed"][n]:
            e = e0 + day
            nights[(k, (e - WS[k]) // Y)][e] += h                            # a run year: from its window's first day
        for k in r["kinds"]:
            whole = [yr for yr in range(-1, (e0 + r["years"] * Y) // Y + 1) if yr * Y + WS[k] in span and yr * Y + WS[k] + Y - 1 in span]
            for yr in whole:
                ns = nights.get((k, yr), {})
                ran = {dd: h for dd, h in ns.items() if h >= 1.0}
                tot = sum(ns.values())
                rec = {"heads": round(tot, 1), "kg": round(tot * KG[k], 1), "food": round(tot * KG[k] * FOOD_KG, 1),
                       "nights": len(ran), "first": (min(ran) - WS[k] - yr * Y) if ran else None, "last": (max(ran) - WS[k] - yr * Y) if ran else None,
                       "first_doy": (min(ran) % Y) if ran else None,
                       "top_share": round(max(ns.values()) / tot, 3) if tot > 0 else None,
                       "by_season": {s: round(sum(h for dd, h in ns.items() if (dd % Y) // S == i) * KG[k] * FOOD_KG, 2) for i, s in enumerate(SEASONS)},
                       "food_by_day": {int(dd % Y): round(h * KG[k] * FOOD_KG, 2) for dd, h in ns.items()}}
                if r["kinds"][k]["dir"] == "up" and tot > 0:          # an up-run arrives `lag` days after it starts at the mouth
                    last = 0.0
                    for dd, h in ns.items():
                        c = [cause_of.get((dd - e0 - lag, k, key)) for key in {kk for (_, kk_, kk) in starts if kk_ == k}]
                        c = [x for x in c if x]
                        if "last day" in c and "cue" not in c and "set night" not in c:
                            last += h
                    rec["last_day_share"] = round(last / tot, 3)
                out[(n, k, yr)] = rec
    return out


def cue_freq(D):
    """How often each kind's cue fires on a night of its window, by stretch kind (village stretches; mouth for up-runs)."""
    out = defaultdict(lambda: [0, 0])
    for wid, d in D.items():
        r = d.get("runs_cue") or {}
        if not r.get("active"):
            continue
        for d1, k, mo, inside, last, cued in r["mouth_cue"]:
            out[(k, "mouth")][0] += int(cued)
            out[(k, "mouth")][1] += 1
    return {f"{k} at {w}": {"cue nights": a, "window nights": b, "p": round(a / b, 3) if b else None} for (k, w), (a, b) in sorted(out.items())}


def eel_cue_by_rain(D):
    """The eels' cue against the catchment's rain at each settled village's stretch in the eel window: P(cue | a window night)."""
    g = defaultdict(lambda: [0, 0])
    for wid, d in D.items():
        r = d.get("runs_cue") or {}
        if not r.get("active"):
            continue
        e0 = int(r["eco_day0"])
        own = defaultdict(float)
        for d1, k, key, h, cause in r["starts"]:
            if k == "eel" and h >= 0.5:
                own[(d1, key)] += h
        for n in r["villages"]:
            for day, rr, temp, fl, ic in r["cond"][n]:
                yd = (e0 + day + 1) % Y
                if not (16 <= yd <= 23):
                    continue
                g[rain_of(d)][1] += 1
                g[rain_of(d)][0] += int(own.get((day + 1, f"v:{n}"), 0) > 0)
    return {f"{k:.0f} mm": {"eel start nights at the village's own stretch": a, "window nights": b, "p": round(a / b, 3)} for k, (a, b) in sorted(g.items())}


def runs_summary(D, arm="runs_cue", settled=True):
    rows = []
    for wid, d in D.items():
        vr = {v["node"]: v for v in d["census_maker"]["villages"].values()}
        for (n, k, yr), rec in run_years(d, arm).items():
            v = vr.get(n, {})
            if settled and v.get("wild"):
                continue
            rows.append({"world": wid, "village": n, "kind": k, "year": yr, "rain_mm": rain_of(d), "upstream_km": v.get("upstream_river_km"),
                         "to_mouth": v.get("stretches_to_mouth"), "salmon_river": v.get("salmon_river"), "elevation": v.get("elevation"),
                         **{x: rec[x] for x in rec if x != "food_by_day"}})
    return rows


def timing_stats(rows):
    g = defaultdict(list)
    for r in rows:
        g[(r["world"], r["village"], r["kind"])].append(r)
    per = {}
    for key, rs in g.items():
        ran = [r for r in rs if r["heads"] >= 1]
        firsts = [r["first"] for r in ran if r["first"] is not None]
        per[key] = {"years": len(rs), "years ran": sum(1 for r in rs if r["nights"] > 0), "firsts": firsts,
                    "first sd": round(stt.pstdev(firsts), 2) if len(firsts) > 1 else None,
                    "first range": (min(firsts), max(firsts)) if firsts else None,
                    "heads cv": round(stt.pstdev([r["heads"] for r in rs]) / stt.mean([r["heads"] for r in rs]), 3) if rs and stt.mean([r["heads"] for r in rs]) > 0 else None,
                    "one night years": sum(1 for r in ran if (r["top_share"] or 0) >= 0.9),
                    "last day share": [r.get("last_day_share") for r in ran if r.get("last_day_share") is not None]}
    by_kind = {}
    for kind in ("eel", "salmon", "lamprey"):
        ks = {k: v for k, v in per.items() if k[2] == kind}
        any_ = {k: v for k, v in ks.items() if v["years ran"] > 0}
        sds = [v["first sd"] for v in any_.values() if v["first sd"] is not None]
        lds = [x for v in any_.values() for x in v["last day share"]]
        allf = [x for v in any_.values() for x in v["firsts"]]
        yrs = sum(v["years"] for v in any_.values())
        by_kind[kind] = {"village stretches it reaches": len(any_), "of": len(ks),
                         "village-years": yrs, "village-years with no run": sum(v["years"] - v["years ran"] for v in any_.values()),
                         "village-years all on one night (>=90%)": sum(v["one night years"] for v in any_.values()),
                         "first night's sd across years, median over villages": med(sds), "sd max": max(sds) if sds else None,
                         "first night (day of year) over all village-years": {"min": min(allf) if allf else None, "p10": q(allf, .1),
                                                                             "median": q(allf, .5), "p90": q(allf, .9), "max": max(allf) if allf else None},
                         "share of a year's heads from the window's last day: median, max": [med(lds), max(lds) if lds else None],
                         "village-years with more than half from the last day": sum(1 for x in lds if x > 0.5),
                         "heads cv across years, median": med([v["heads cv"] for v in any_.values() if v["heads cv"] is not None])}
    return per, by_kind


# ---------------------------------------------------------------------- section 4
def food_year(D, arm="runs_cue", fish="census_maker"):
    """Per settled village on a river (and every settled village): the food passing a season (mean over whole years) by source."""
    out = []
    for wid, d in D.items():
        ry = run_years(d, arm)
        cm = d[fish]
        for n, v in cm["villages"].items():
            if v.get("wild"):
                continue
            yrs = sorted({yr for (nn, k, yr) in ry if nn == n})
            src = {}
            for k in ("eel", "salmon", "lamprey"):
                src[k] = {s: round(stt.mean([ry[(n, k, yr)]["by_season"][s] for yr in yrs if (n, k, yr) in ry]), 2) if yrs else 0.0 for s in SEASONS}
            src["resident fish (maker, at best)"] = {s: round(v["fish_best_night"][s] * FOOD_KG * S, 2) for s in SEASONS}
            src["shallows (at best)"] = {s: round(v["shallows_best_night"][s] * FOOD_KG * S, 2) for s in SEASONS}
            tot = {s: round(sum(x[s] for x in src.values()), 1) for s in SEASONS}
            need = {s: NEED[s] * S for s in SEASONS}
            # the longest stretch of nights in a year with no run food passing (circular), mean over years
            gaps = []
            for yr in yrs:
                fed = [0.0] * Y
                for k in ("eel", "salmon", "lamprey"):
                    for dd, f in (ry.get((n, k, yr)) or {}).get("food_by_day", {}).items():
                        fed[int(dd)] += f
                gaps.append(_longest_zero(fed, 1.0))
            out.append({"world": wid, "family": d["meta"].get("family"), "kind": d["meta"].get("kind"), "rain_mm": rain_of(d),
                        "village": n, "types": v["types"], "upstream_km": v.get("upstream_river_km"), "to_mouth": v.get("stretches_to_mouth"),
                        "salmon_river": v.get("salmon_river"), "on_river": v.get("on_river"), "sources": src, "total": tot,
                        "need": need, "share": {s: round(tot[s] / need[s], 2) for s in SEASONS},
                        "year_food": round(sum(tot.values()), 1), "year_need": sum(need.values()),
                        "runs_year": round(sum(src[k][s] for k in ("eel", "salmon", "lamprey") for s in SEASONS), 1),
                        "resident_year": round(sum(src["resident fish (maker, at best)"].values()), 1),
                        "shallows_year": round(sum(src["shallows (at best)"].values()), 1),
                        "longest_nights_without_a_run_meal": med(gaps) if gaps else Y})
    return out


def _longest_zero(xs, thr):
    n = len(xs)
    if all(x < thr for x in xs):
        return n
    best = cur = 0
    for x in xs + xs:
        cur = cur + 1 if x < thr else 0
        best = max(best, min(cur, n))
    return best


def water_class(r):
    t = r["types"]
    if "lake" in t:
        return "lake"
    if "big river" in t:
        return "big river"
    if "river" in t:
        return "river"
    if "brook" in t:
        return "brook"
    if "pool" in t:
        return "pool"
    if "fen" in t:
        return "fen only"
    return "no water parcel"


def cue_per_world(D):
    """Per world: the engine's mean rain a day at its villages' catchments (against runs.RAIN_MEAN 3.4) and the generator's rain_mm;
    per kind, the cue nights a window (eels: at each settled village's own stretch; up-runs: at each mouth), and the share of
    window-years with none."""
    from cybertron2.wild import runs as RU
    out = {}
    for wid, d in D.items():
        r = d.get("runs_cue") or {}
        if not r.get("active"):
            out[wid] = {"active": False}
            continue
        e0 = int(r["eco_day0"])
        settled = {v["node"] for v in d["census_maker"]["villages"].values() if not v.get("wild")}
        rm = [x for n, x in r["catch_rain_mean"].items() if n in settled] or list(r["catch_rain_mean"].values())
        rec = {"rain_mm (generator)": rain_of(d), "village node rain_mm (generator)": None,
               "engine rain a day, mean at the villages' catchments": round(stt.mean(rm), 2), "over RAIN_MEAN": round(stt.mean(rm) / RU.RAIN_MEAN, 2)}
        cnt = defaultdict(lambda: defaultdict(int))
        for d1, k, n, c, ic in r.get("village_cue") or []:
            if n not in settled:
                continue
            yr = (e0 + d1 - 16) // Y
            cnt[("eel", n)][yr] += int(c and not ic)
        for d1, k, mo, inside, last, c in r["mouth_cue"]:
            ws = 16 if k == "salmon" else 0
            yr = (e0 + d1 - ws) // Y
            cnt[(k, mo)][yr] += int(c)
        for kind in ("eel", "salmon", "lamprey"):
            ys = [v for (k, _), yrs in cnt.items() if k == kind for v in yrs.values()]
            if ys:
                rec[kind] = {"cue nights a window, mean": round(stt.mean(ys), 2), "window-years with none": round(sum(1 for x in ys if x == 0) / len(ys), 2),
                             "window-years": len(ys)}
        out[wid] = rec
    return out


def arms_compare(D):
    """The same villages under the arms: as built (cue), the fix (spawners reseeded), set nights, and the dam (laid worlds)."""
    out = {}
    for arm in ("runs_cue", "runs_fix", "runs_set", "runs_dam"):
        rs = runs_summary({k: v for k, v in D.items() if v.get(arm)}, arm)
        out[arm] = timing_stats(rs)[1]
    return out


def main():
    D = load_all()
    T = {"worlds": worlds_table(D)}
    B = body_rows(D)
    T["bodies_generated_with_fish"] = sum(1 for b in body_rows(D, "census_generated") if b["K"])
    T["bodies_maker_with_fish"] = sum(1 for b in B if b["K"])
    T["bodies_by_type_K"] = by_type(B, "type", "K")
    T["bodies_by_type_food_night"] = by_type(B, "type", "best_food_night_summer")
    T["bodies_by_type_river_km"] = by_type([b for b in B if b["river_km"]], "type", "river_km")
    T["bodies_by_type_units"] = by_type(B, "type", "units")
    T["bodies_by_type_web_K"] = by_type(B, "type", "web_fish_K_kg")
    P = parcel_rows(D)
    T["parcels_by_type_shallows_K"] = by_type(P, "type", "shallows_K")
    T["parcels_by_type_size"] = by_type(P, "type", "size")
    for r in P:
        r["summer"] = r["best_food_night"]["summer"]
    T["parcels_by_type_shallows_food_summer"] = by_type(P, "type", "summer")
    V = village_rows(D)
    T["villages"] = V
    rs = runs_summary(D)
    per, by_kind = timing_stats(rs)
    T["timing_by_kind"] = by_kind
    T["cue_freq"] = cue_freq(D)
    T["eel_cue_by_rain"] = eel_cue_by_rain(D)
    rs_set = runs_summary(D, "runs_set")
    T["timing_by_kind_set_nights"] = timing_stats(rs_set)[1]
    F = food_year(D)
    T["food"] = F
    T["food_fix"] = food_year(D, "runs_fix")
    T["cue_per_world"] = cue_per_world(D)
    T["arms"] = arms_compare(D)
    with open(os.path.join(DATA, "tables.json"), "w") as f:
        json.dump(T, f, indent=1, default=str)
    with open(os.path.join(DATA, "run_years.json"), "w") as f:
        json.dump(rs, f, separators=(",", ":"))
    print(json.dumps({k: T[k] for k in T if k not in ("villages", "food", "worlds")}, indent=1, default=str))


if __name__ == "__main__":
    main()
