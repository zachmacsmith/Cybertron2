"""W-108 sweep, section 5 (b to d): experiments on copies of the data, never in the engine (brief.md section 5).

    python3 docs/review/37_growth/02zzzl_waters_calib/a_sweep/experiments.py

Reads data/worlds/<id>.json (sweep_world.py) and data/exp_rows/<id>.json (experiments_rows.py); writes data/experiments.json and
prints its summary. Three experiments:

**(b) Timing drawn from conditions.** Each settled village's own nights from the sweep (its catchment's rain over the mean, the air
temperature at its node: sweep_world.runs `cond`) drive a run by a nightly chance under conditions, in a broad season, in place of
today's window and cue: each night a share h of what is still to run goes, h by the conditions (HAZARD below); an up-run's rest
enters on the season's last night, a down-run's rest stays (as today). Water temperature is the air's mean over the last five nights
(a presentation choice: the engine keeps no water temperature). The run's year's heads are the village's own from the fix arm (the
same fish, re-timed). The moon is left out: under the year clock a lunar month is under three world nights (29.5 / 11.4).

**(c) Other runs a temperate lowland river would have**, each sized from a real river's run (heads or kg a km2 of catchment a real
year; RUNS_REAL, sources by name, est. where no figure was found), compressed to the world year as D2-259 compressed the eels'
and the salmon's (x 32/365), at each settled village by the catchment above it (the land summary's areas, coarse: wild blocks are
8 km), in the season the real run comes.

**(d) Resident stocks from real productivity** (kg of whole fish a hectare a year, PRODUCTIVITY), on the water the engine's own
ecology counts (wild/ecology.py: a small stream 0.12 of a 150 m cell wide, 18 m; the large river's channel 0.6 of a cell, 90 m; a lake
by its km2; a fen parcel's dykes and pools a share of its area, est.), a sustained take of half the production, on two clocks: the
runs' and the harvests' (a real year's amount into the 32-day year, x 32/365: per night the real night's), and the year clock as the
shallows were calibrated in u1 section 2 (a real year's production in 32 nights, x 365/32 a night against the first).
"""
from __future__ import annotations

import glob
import json
import os
import statistics as stt
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analyse as AN  # noqa: E402

DATA = os.path.join(HERE, "data")
Y, S = 32, 8
FOOD_UNIT = 0.46                 # data.ITEMS fish: food a unit (about 1 kg gutted)
UNITS_KG = {"large": 0.53, "small": 0.75}   # fish units a kg of whole fish: make_water_worlds LAKE_FISH (0.53); u1 section 2 (small 0.75)
COMPRESS = 32.0 / 365.0
NEED_NIGHT = 11.0

# (b) the nightly chance under conditions [est.: the biology named, the numbers a first value to calibrate]
HAZARD = {
    # silver eels go down on dark nights of rising water as the water cools, from late summer into early winter
    "eel": {"season": (12, 27), "dir": "down", "rules": [(lambda c: c["wt"] <= 14 and c["rr"] >= 1.5, 0.45), (lambda c: c["wt"] <= 14, 0.06)]},
    # salmon come up on a fresh of water, more as the water cools, from late summer to the end of winter
    "salmon": {"season": (12, 31), "dir": "up", "rules": [(lambda c: c["rr"] >= 1.2, 0.35), (lambda c: c["wt"] <= 16, 0.04)]},
    # lampreys come up and spawn as the water warms past about 8 C, more on a rise of water, through spring into early summer
    "lamprey": {"season": (0, 12), "dir": "up", "rules": [(lambda c: c["wt"] >= 8 and c["rr"] >= 1.0, 0.35), (lambda c: c["wt"] >= 8, 0.10)]},
}

# (c) the runs a temperate lowland river would have: real size a km2 of catchment a real year, kg a head (whole), season nights
# (day of the 32-day year), where it runs, source
RUNS_REAL = {
    "river lamprey (sized as real)": {"per_km2": (5, 20), "kg": 0.06, "units": "small", "days": list(range(26, 32)) + list(range(0, 6)), "where": "any",
                                      "src": "est.: no run size found; the Yorkshire Ouse's commercial fishery is the named case (Masters et al. 2006, "
                                             "Aquatic Conservation; Hull's 2018-20 telemetry); up in late autumn and winter, spawning in spring"},
    "sea lamprey": {"per_km2": (0.2, 1.0), "kg": 1.0, "units": "large", "days": list(range(5, 12)), "where": "salmon river",
                    "src": "est.; up in May and June to spawn (Severn, Wye: Unlocking the Severn's telemetry, Yeldham et al. 2025)"},
    "elvers and glass eels": {"kg_km2": (1.0, 4.0), "units": "small", "days": list(range(3, 8)), "where": "below 4 stretches from the mouth",
                              "src": "the Severn's glass eel fishery: about 40 t a year in the late 1970s, about 10 t now (Cefas); the run 25 t "
                                     "(2020) to 76 t (2023 trial) by mark and recapture (glasseel.com), over 11,420 km2: 0.9 to 3.5 kg a km2 "
                                     "caught, 2 to 7 standing; April and May"},
    "twaite shad": {"per_km2": (10, 30), "kg": 0.45, "units": "large", "days": list(range(5, 12)), "where": "salmon river, below 4 stretches from the mouth",
                    "src": "the Severn's run 'hundreds of thousands' before the weirs (Unlocking the Severn), 7,000 to 14,000 past "
                           "Tewkesbury 2017-18, 1,541 in 2022 (Environment Agency counts), over 11,420 km2; late April to June; the "
                           "fish about 0.3 to 0.6 kg (est.)"},
    "sea trout": {"per_km2": (5, 20), "kg": 1.5, "units": "large", "days": list(range(9, 17)), "where": "any",
                  "src": "est. (the Welsh sea trout rivers, Tywi and Teifi, as the named case; no figure checked here); June to August"},
    "smelt": {"kg_km2": (0.5, 2.0), "units": "small", "days": list(range(28, 32)) + list(range(0, 3)), "where": "at the mouth",
              "src": "est.; the tidal reaches only (the Thames', the Cree's), February to April"},
}

# (d) a water's fish: production P and standing biomass B, kg of whole fish a hectare (a real year)
PRODUCTIVITY = {
    "brook": {"P": (20, 170), "B": (100, 200), "src": "u1 section 2 / fishing_ladder section 1: trout streams 20 to 168 kg a ha a year, 100 to 200 standing"},
    "river": {"P": (50, 100), "B": (150, 250), "src": "the River Eden (Kent), chub 54 + dace 17 kg a ha a year, 191 + 43 kg a ha standing (Mann's "
                                                       "school, 1982); Welcomme 1985 (FAO 262): floodplain rivers' catch 5 to 143 kg a ha a year"},
    "big river": {"P": (30, 80), "B": (100, 200), "src": "est.: a deep channel lower a hectare than the river's margins"},
    "lake": {"P": (20, 100), "B": (50, 300), "src": "Downing and Plante 1993 (CJFAS 50: 100 populations in 38 lakes); make_water_worlds' 'a real "
                                                    "lake's 50 to 300' kg a ha standing"},
    "fen": {"P": (30, 100), "B": (100, 300), "src": "est.: eels and coarse fish of fen dykes and pools"},
}
TAKE = 0.5                       # the share of production taken for good (est.; Welcomme's heavily fished rivers)
FEN_WATER = 0.10                 # open water a fen parcel's area (dykes and pools; est.)
HA_UNIT = 2.25                   # a unit of size (vocab km 0.15: a cell)


def load():
    D = AN.load_all()
    X = {}
    for p in glob.glob(os.path.join(DATA, "exp_rows", "*.json")):
        x = json.load(open(p))
        X[x["id"]] = x
    return D, X


# ---------------------------------------------------------------------- (b)
def hazard_runs(D):
    out = defaultdict(list)
    for wid, d in D.items():
        r = d.get("runs_fix") or {}
        if not r.get("active"):
            continue
        e0 = int(r["eco_day0"])
        ry = AN.run_years(d, "runs_fix")
        vill = {v["node"]: v for v in d["census_maker"]["villages"].values() if not v.get("wild")}
        for n in r["villages"]:
            if n not in vill:
                continue
            cond = r["cond"][n]
            temps = [c[2] for c in cond]
            for k, hz in HAZARD.items():
                heads = [ry[(n, k, yr)]["heads"] for (nn, kk, yr) in ry if nn == n and kk == k]
                if not heads or stt.mean(heads) < 1:
                    continue
                N = stt.mean(heads)
                lo, hi = hz["season"]
                for yr in range(-1, r["years"] + 1):
                    days = [yr * Y + lo + j for j in range(hi - lo + 1)]
                    idx = [dd - e0 for dd in days]
                    if min(idx) < 5 or max(idx) >= len(cond):
                        continue
                    left, got = N, []
                    for j, i in enumerate(idx):
                        c = {"rr": cond[i][1], "wt": stt.mean(temps[i - 5:i])}
                        h = next((p for f, p in hz["rules"] if f(c)), 0.0)
                        if j == len(idx) - 1 and hz["dir"] == "up":
                            h = 1.0
                        n_ = left * h
                        left -= n_
                        got.append(n_)
                    tot = sum(got)
                    ran = [j for j, x in enumerate(got) if x >= 1.0]
                    main_ = [j for j, x in enumerate(got) if x >= 0.1 * tot] if tot >= 1 else []
                    out[k].append({"world": wid, "village": n, "year": yr, "share_run": round(tot / N, 3), "nights": len(ran),
                                   "first": main_[0] if main_ else None, "top_share": round(max(got) / tot, 3) if tot > 0 else None,
                                   "last_night_share": round(got[-1] / tot, 3) if tot > 0 else None,
                                   "by_season": {s: round(sum(x for j, x in enumerate(got) if ((lo + j) % Y) // S == si), 1)
                                                 for si, s in enumerate(AN.SEASONS)}})
    summ = {}
    for k, rows in out.items():
        by_v = defaultdict(list)
        for x in rows:
            if x["first"] is not None:
                by_v[(x["world"], x["village"])].append(x["first"])
        sds = [stt.pstdev(v) for v in by_v.values() if len(v) > 1]
        firsts = [x["first"] for x in rows if x["first"] is not None]
        summ[k] = {"village-years": len(rows), "with no night of a head or more": sum(1 for x in rows if not x["nights"]),
                   "with under half the year's run gone": sum(1 for x in rows if x["share_run"] < 0.5),
                   "all on one night (>=90%)": sum(1 for x in rows if (x["top_share"] or 0) >= 0.9),
                   "first night with a tenth of the year's run, after the season opens": {"p10": AN.q(firsts, .1), "median": AN.q(firsts, .5), "p90": AN.q(firsts, .9)},
                   "first night's sd across years, median over villages": AN.med(sds),
                   "nights a year, median": AN.med([x["nights"] for x in rows]),
                   "share on the season's last night (up-runs), median": AN.med([x["last_night_share"] for x in rows if x["last_night_share"] is not None]),
                   "share of the run that goes, median": AN.med([x["share_run"] for x in rows])}
    return summ


def today_vs(D, X):
    """Today's rows (the fix arm, through the engine) and the data-only variants, per kind: the same measures as the hazard's."""
    out = {}
    names = sorted({v for x in X.values() for v in x["variants"]})
    for v in names:
        rows = [dict(r, world=wid) for wid, x in X.items() for r in x["variants"].get(v, [])]
        per, by_kind = AN.timing_stats([dict(r, rain_mm=None, upstream_km=None, to_mouth=None, salmon_river=None, elevation=None) for r in rows])
        food = defaultdict(lambda: defaultdict(list))
        for r in rows:
            for s, f in r["by_season"].items():
                food[r["kind"]][s].append(f)
        out[v] = {"timing": by_kind, "food a season, mean over village-years": {k: {s: round(stt.mean(x), 2) for s, x in fs.items()} for k, fs in food.items()}}
    return out


# ---------------------------------------------------------------------- (c)
def other_runs(D):
    rows = []
    for wid, d in D.items():
        conf = ((d["meta"].get("spec") or {}).get("generate") or {}).get("configuration") or ""
        tidal = conf in ("estuary and fens", "coast", "coastal strip under mountains", "fen with islands", "twin bays split by a spur", "isthmus")
        ry = AN.run_years(d, "runs_fix")
        for v in d["census_maker"]["villages"].values():
            if v.get("wild") or not v.get("on_river"):
                continue
            n = v["node"]
            cat = float(v.get("catchment_km2") or 0.0)
            today = {k: stt.mean([ry[x]["heads"] for x in ry if x[0] == n and x[1] == k] or [0.0]) for k in ("eel", "salmon", "lamprey")}
            rec = {"world": wid, "village": n, "catchment_km2": cat, "to_mouth": v.get("stretches_to_mouth"), "salmon_river": v.get("salmon_river"),
                   "eel heads a km2 (engine)": round(today["eel"] / cat, 2) if cat else None,
                   "salmon heads a km2 (engine)": round(today["salmon"] / cat, 2) if cat else None,
                   "lamprey heads a km2 (engine)": round(today["lamprey"] / cat, 3) if cat else None, "added": {}}
            for k, row in RUNS_REAL.items():
                w_ = row["where"]
                if "salmon river" in w_ and not v.get("salmon_river"):
                    continue
                if "below 4" in w_ and (v.get("stretches_to_mouth") or 99) > 4:
                    continue
                if w_ == "at the mouth" and ((v.get("stretches_to_mouth") or 99) > 1 or not tidal):
                    continue
                if "per_km2" in row:
                    kg = [x * row["kg"] * cat * COMPRESS for x in row["per_km2"]]
                else:
                    kg = [x * cat * COMPRESS for x in row["kg_km2"]]
                food = [x * UNITS_KG[row["units"]] * FOOD_UNIT for x in kg]
                seas = defaultdict(float)
                for dd in row["days"]:
                    seas[AN.SEASONS[dd // S]] += 1.0 / len(row["days"])
                rec["added"][k] = {"food a year (lo, hi)": [round(x, 1) for x in food],
                                   "by season (mid)": {s: round(sum(food) / 2 * f, 1) for s, f in seas.items()}}
            rows.append(rec)
    agg = defaultdict(lambda: defaultdict(list))
    for r in rows:
        for k, a in r["added"].items():
            agg[k]["lo"].append(a["food a year (lo, hi)"][0])
            agg[k]["hi"].append(a["food a year (lo, hi)"][1])
            agg[k]["spring"].append(a["by season (mid)"].get("spring", 0.0))
    summ = {k: {"villages it reaches": len(a["lo"]), "of": len(rows), "food a year, median (lo)": AN.med(a["lo"]),
                "food a year, median (hi)": AN.med(a["hi"]), "max (hi)": round(max(a["hi"]), 1),
                "spring food, median (mid)": AN.med(a["spring"])} for k, a in agg.items()}
    check = {"eel heads a km2 of catchment a world year (engine, fix arm), median": AN.med([r["eel heads a km2 (engine)"] for r in rows if r["eel heads a km2 (engine)"] is not None]),
             "against Burrishoole's 20 to 50 x 32/365": [round(20 * COMPRESS, 2), round(50 * COMPRESS, 2)],
             "salmon heads a km2 (engine), median over salmon rivers": AN.med([r["salmon heads a km2 (engine)"] for r in rows if r["salmon_river"] and r["salmon heads a km2 (engine)"]]),
             "against a real river's 5 to 20 x 32/365": [round(5 * COMPRESS, 2), round(20 * COMPRESS, 2)],
             "lamprey heads a km2 (engine), median": AN.med([r["lamprey heads a km2 (engine)"] for r in rows if r["lamprey heads a km2 (engine)"] is not None]),
             "against the river lamprey row's 5 to 20 x 32/365 (est.)": [round(5 * COMPRESS, 2), round(20 * COMPRESS, 2)]}
    return {"summary": summ, "check": check, "rows": rows}


# ---------------------------------------------------------------------- (d)
def resident(D):
    rows = []
    for wid, d in D.items():
        cm = d["census_maker"]
        for v in cm["villages"].values():
            if v.get("wild"):
                continue
            n = v["node"]
            water = {}
            km, big = float(v.get("river_km_home_ring") or 0.0), float(v.get("big_km") or 0.0)
            big = min(big, km)
            t = AN.water_class({"types": v["types"]})
            if km > 0 and v.get("on_river"):
                water["big river" if big > 0 else "river"] = (km - big) * 1.8 + big * 9.0     # ha (engine widths 18 m, 90 m)
                if big > 0 and km - big > 0:
                    water["river"] = (km - big) * 1.8
                    water["big river"] = big * 9.0
            lake = 0.0
            for bid in v["bodies"]:
                b = cm["bodies"].get(bid) or {}
                if b.get("kind") == "lake":
                    lake += float(b.get("km2") or 0.0) * 100.0
            if lake:
                water["lake"] = lake
            brook = sum(1 for bid in v["bodies"] if (cm["bodies"].get(bid) or {}).get("kind") in ("brook", "pool"))
            if brook:
                ps = [p for p, x in cm["parcels"].items() if x["node"] == n and x["type"] in ("brook", "pool")]
                water["brook"] = sum(cm["parcels"][p]["size"] for p in ps) * 0.15 * 0.3   # 0.15 km of a 3 m brook a unit (u1 section 2)
            fen = sum(cm["parcels"][p]["size"] for p in v.get("fen_parcels") or [])
            if fen:
                water["fen"] = fen * HA_UNIT * FEN_WATER
            if not water:
                continue
            take = {"lo": 0.0, "hi": 0.0}
            K = 0.0
            for wk, ha in water.items():
                pr = PRODUCTIVITY[wk]
                for j, key in enumerate(("lo", "hi")):
                    take[key] += TAKE * pr["P"][j] * ha * UNITS_KG["large"] * FOOD_UNIT      # food a real year
                K += sum(pr["B"]) / 2 * ha * UNITS_KG["large"]
            night_c = {k: x / 365.0 for k, x in take.items()}                                 # compressed: a real night's
            night_y = {k: x / 32.0 for k, x in take.items()}                                  # the year clock as u1 read it
            maker = v["fish_best_night"]["summer"] * FOOD_UNIT
            rows.append({"world": wid, "village": n, "class": t, "water ha": {k: round(x, 1) for k, x in water.items()},
                         "K units (productivity)": round(K, 0), "K units (maker)": v["fish_K"],
                         "food a night, compressed (lo, hi)": [round(night_c["lo"], 2), round(night_c["hi"], 2)],
                         "food a night, year clock as u1 (lo, hi)": [round(night_y["lo"], 2), round(night_y["hi"], 2)],
                         "food a night, maker": round(maker, 2), "shallows food a night (summer)": round(v["shallows_best_night"]["summer"] * FOOD_UNIT, 2),
                         "r to give the compressed mid (fast rule)": round(4 * (night_c["lo"] + night_c["hi"]) / 2 / FOOD_UNIT / K, 5) if K else None})
    agg = defaultdict(lambda: defaultdict(list))
    for r in rows:
        a = agg[r["class"]]
        a["c_lo"].append(r["food a night, compressed (lo, hi)"][0]); a["c_hi"].append(r["food a night, compressed (lo, hi)"][1])
        a["y_lo"].append(r["food a night, year clock as u1 (lo, hi)"][0]); a["y_hi"].append(r["food a night, year clock as u1 (lo, hi)"][1])
        a["maker"].append(r["food a night, maker"]); a["sh"].append(r["shallows food a night (summer)"])
        a["Kp"].append(r["K units (productivity)"]); a["Km"].append(r["K units (maker)"])
    summ = {k: {"villages": len(a["maker"]), "maker food a night, median": AN.med(a["maker"]),
                "productivity, compressed: median lo, hi": [AN.med(a["c_lo"]), AN.med(a["c_hi"])],
                "productivity, year clock: median lo, hi": [AN.med(a["y_lo"]), AN.med(a["y_hi"])],
                "shallows (summer), median": AN.med(a["sh"]),
                "K units: productivity median, maker median": [AN.med(a["Kp"]), AN.med(a["Km"])]} for k, a in sorted(agg.items())}
    return {"summary": summ, "rows": rows, "need a night": NEED_NIGHT, "a quarter of need": NEED_NIGHT / 4}


def main():
    D, X = load()
    out = {"hazard": hazard_runs(D), "rows_variants": today_vs(D, X), "other_runs": other_runs(D), "resident": resident(D),
           "inputs": {"HAZARD": {k: {"season": v["season"], "dir": v["dir"]} for k, v in HAZARD.items()},
                      "RUNS_REAL": {k: {x: y for x, y in v.items()} for k, v in RUNS_REAL.items()}, "PRODUCTIVITY": PRODUCTIVITY,
                      "TAKE": TAKE, "FEN_WATER": FEN_WATER, "COMPRESS": COMPRESS}}
    with open(os.path.join(DATA, "experiments.json"), "w") as f:
        json.dump(out, f, indent=1, default=str)
    small = {"hazard": out["hazard"], "rows_variants": out["rows_variants"], "other_runs": {k: out["other_runs"][k] for k in ("summary", "check")},
             "resident": out["resident"]["summary"], "inputs": out["inputs"]}
    with open(os.path.join(DATA, "experiments_summary.json"), "w") as f:
        json.dump(small, f, indent=1, default=str)
    print(json.dumps({"hazard": out["hazard"], "rows_variants": out["rows_variants"], "other_runs": {k: out["other_runs"][k] for k in ("summary", "check")},
                      "resident": out["resident"]["summary"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
