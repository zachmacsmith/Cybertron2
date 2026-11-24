"""W-108 sweep, steps 2 and 3 on one world (brief.md sections 2, 3): the waters' census and the runs over several years, no people.

    python3 docs/review/37_growth/02zzzl_waters_calib/a_sweep/sweep_world.py <world id | all> [--years 6] [--jobs 4]

**The census** (section 2): the world is built by the engine (World: the wild layer's ten-year history runs at the build, as in every
world) three ways for the resident fish, which the land generator never writes (37.2, 23 Nov; make_water_worlds.py docstring):
`as generated` (none), `maker` (today's maker rule applied first: make_water_worlds.water_stocks, K 8 x RESIDENT_FISH 2.2 a unit of
size, r 0.3, a mere by its area; Eelmouth's own RESIDENT_SHARE 0.25 where the world is Eelmouth), and the productivity rule of the
experiments (experiments.py, from the water's own size and kind). The shallows (wild/water.py) and the food web's own fish (the wild
layer's `fish` food, kg a km2 by the water share of each area, wild/ecology.py) are the engine's, read as generated.

**The runs** (section 3): the wild layer's own night loop, as engine/wild.py `night` and `_runs_night` call it with no people: each
night EC.step (the food web), then the ice at each village's first river parcel (wild/water.py `ice`, as `stretch_ice`), then
RU.advance with tonight's and tomorrow's weather (WL.weather), the dams' stops (a shut mill's, `_dam_stops`; none unless the arm
sets one) and the cue on (`weather=True`), or on set nights (`weather=False`, as `runs_set_nights` worlds such as Eelmouth run).
What passed each village's water is counted as the engine's own tally counts it (a pulse at the stretch on its day, once, the night
it moves on; held under ice to the next open night), before any take. Each start is recorded with its cause: the cue (the
catchment's rain, read as runs.cued reads it), the window's last day (an up-run's rest), or a set night.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import yaml  # noqa: E402

WORLDS = os.path.join(HERE, "worlds")
OUT = os.path.join(HERE, "data", "worlds")
EELMOUTH = os.path.join(ROOT, "cybertron2", "specs", "nutrition", "eelmouth.yaml")
NEED = {"spring": 11.0, "summer": 11.0, "autumn": 11.0, "winter": 12.0}   # ten people a night (brief.md; spring_gap.md)
FOOD_KG = 0.46                                                             # data.ITEMS fish: food a kg
SEASONS = ("spring", "summer", "autumn", "winter")


def load(wid):
    if wid == "eelmouth":
        return yaml.safe_load(open(EELMOUTH))
    return yaml.safe_load(open(os.path.join(WORLDS, wid + ".yaml")))


def build(world):
    from cybertron2.engine.world import World
    with contextlib.redirect_stdout(io.StringIO()):
        return World(copy.deepcopy(world))


# ---------------------------------------------------------------------- yields
def best_fast(K, r, winter=False):
    """The most a `fast` (or `periodic` out of its run) stock gives a night for good (engine/night.py regrow): the max over S of
    r S (1 - S/K) + 0.01 (K - S), r x regrow_winter in winter."""
    if K <= 0:
        return 0.0
    rr = r * (0.25 if winter else 1.0)
    S = np.linspace(0, K, 401)
    return float(np.max(rr * S * (1 - S / K) + 0.01 * (K - S)))


def best_threshold(K, r, winter=False):
    if K <= 0:
        return 0.0
    rr = r * (0.25 if winter else 1.0)
    S = np.linspace(0.15 * K, K, 401)                                      # below 15% it does not come back (game_threshold)
    return float(np.max(rr * S * (1 - S / K)))


def best_shallows(K, season):
    """The shallows' most a night for good (wild/water.py renew): max over S of r S (1 - S/K) + 0.01 K r / 0.10."""
    from cybertron2.wild import water as WT
    r = float(WT.SHALLOWS["r"][season])
    if K <= 0:
        return 0.0
    S = np.linspace(0, K, 401)
    return float(np.max(np.minimum(K - S, r * S * (1 - S / K) + 0.01 * K * r / 0.10)))


def fish_yield(rec, season):
    if not rec:
        return 0.0
    K, r = float(rec.get("K", 0)), float(rec.get("r", 0.3))
    rule = rec.get("renewal") or "periodic"
    winter = season == "winter"
    return best_threshold(K, r, winter) if rule == "threshold" else best_fast(K, r, winter)


# ---------------------------------------------------------------------- the census
def village_place(w, m, nt, node):
    from cybertron2.wild import runs as RU
    g = f"v:{node}"
    land = w.s["wild"]["land"]
    out = {"node": node, "name": w.s["nodes"][node].get("name", node), "elevation": None, "on_river": g in nt.members,
           "wild": bool(w.s["nodes"][node].get("unexplored"))}
    home = land["home"].get(node)
    if home:
        a = land["areas"][home]
        out["elevation"] = a.get("elevation")
        out["temp"] = a.get("temp")
    if g not in nt.members:
        return out
    up = nt.upstream(g)
    path = nt.path_up(g)                                                  # mouth .. g
    lag = sum(nt.lag(a, b, 10.0) for a, b in zip(path, path[1:]))
    below_km = sum(nt.km[x] for x in path[:-1])
    cat_km2 = sum(float(land["areas"][a]["km2"]) for h in up for a in nt.members[h])
    out.update({"stretch_km": round(nt.km[g], 2), "big_km": round(nt.big[g], 2), "upstream_river_km": round(sum(nt.km[h] for h in up), 1),
                "upstream_big_km": round(sum(nt.big[h] for h in up), 1), "stretches_above": len(up) - 1,
                "stretches_to_mouth": len(path) - 1, "river_km_below": round(below_km, 1), "catchment_km2": round(cat_km2, 1),
                "lag_from_mouth": lag, "mouth": nt.mouth(g), "mouth_out": (land.get("down") or {}).get(nt.members[nt.mouth(g)][0]) == "out",
                "salmon_river": any(nt.big[h] > 0 for h in path)})
    return out


def census(w, world, variant):
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU, water as WT
    m = WL.model(w)
    nt = RU.net(m)
    land = w.s["wild"]["land"]
    villages = sorted(n for n, x in w.s["nodes"].items() if land["home"].get(n) and not x.get("wild"))
    fishK = m.cap("fish")
    out = {"villages": {}, "bodies": {}, "parcels": {}}
    for bid, b in sorted((land.get("waters") or {}).items()):
        rec = (w.s.get("waters") or {}).get(bid) or {}
        f = rec.get("fish")
        nodes = sorted({w.s["parcels"][p]["node"] for p in b.get("parcels") or [] if p in w.s["parcels"]})
        if not b.get("parcels") and not nodes:
            continue                                                       # a wild reach with no water parcel: no stock to hold
        web = sum(float(fishK[m.ids.index(a)]) * float(m.km2[m.ids.index(a)]) for a in (b.get("areas") or {}) if a in m.ids)
        out["bodies"][bid] = {"kind": b.get("kind"), "river_km": b.get("river_km"), "big_river_km": b.get("big_river_km"), "km2": b.get("km2"),
                              "parcels": b.get("parcels"), "nodes": nodes,
                              "parcel_units": sum(int(w.s["parcels"][p].get("size", 1)) for p in b.get("parcels") or [] if p in w.s["parcels"]),
                              "fish": {k: f[k] for k in ("K", "S", "r", "renewal") if k in f} if f else None,
                              "fish_best_night": {s: round(fish_yield(f, s), 3) for s in SEASONS} if f else None,
                              "web_fish_K_kg": round(web, 1)}
    for pid, p in sorted(w.s["parcels"].items()):
        if p.get("cover") not in ("water", "fen"):
            continue
        sh = p["res"].get("shallows")
        out["parcels"][pid] = {"node": p["node"], "cover": p["cover"], "size": p.get("size", 1), "type": WT.water_type(w, pid),
                               "body": (p.get("land") or {}).get("water_body"), "river": (p.get("land") or {}).get("river"),
                               "elevation": (p.get("land") or {}).get("elevation"), "terrain": p.get("terrain"),
                               "shallows_K": sh["K"] if sh else 0.0,
                               "shallows_best_night": {s: round(best_shallows(float(sh["K"]), s), 3) for s in SEASONS} if sh else None,
                               "fish_K": (p["res"].get("fish") or {}).get("K"),
                               "run_reach": WT.run_reach(w, pid), "pinch": WT.pinch(w, pid)}
    for node in villages:
        v = village_place(w, m, nt, node)
        ps = {pid: x for pid, x in out["parcels"].items() if x["node"] == node}
        bodies = sorted({x["body"] for x in ps.values() if x["body"]})
        home = land["home"][node]
        ring = [a for a, x in land["areas"].items() if x.get("kind") == "ring" and x.get("node") == node]
        idx = [m.ids.index(a) for a in [home] + ring]
        v.update({"water_parcels": sorted(p for p, x in ps.items() if x["cover"] == "water"),
                  "fen_parcels": sorted(p for p, x in ps.items() if x["cover"] == "fen"),
                  "types": sorted({x["type"] for x in ps.values() if x["type"]}), "bodies": bodies,
                  "lake_km2": round(sum(float(land["areas"][a].get("lake_km2") or 0) for a in [home] + ring), 3),
                  "river_km_home_ring": round(sum(float(land["areas"][a].get("river_km") or 0) for a in [home] + ring), 2),
                  "web_fish_K_kg": round(float(sum(fishK[i] * m.km2[i] for i in idx)), 1),
                  "web_water_km2": round(float(sum(m.f["water"][i] * m.km2[i] for i in idx)), 4)})
        v["shallows_best_night"] = {s: round(sum((x["shallows_best_night"] or {}).get(s, 0.0) for x in ps.values()), 3) for s in SEASONS}
        v["shallows_K"] = round(sum(x["shallows_K"] for x in ps.values()), 2)
        fb = {s: 0.0 for s in SEASONS}
        fK = 0.0
        for bid in bodies:
            b = out["bodies"].get(bid) or {}
            if b.get("fish"):
                fK += float(b["fish"]["K"])
                for s in SEASONS:
                    fb[s] += b["fish_best_night"][s]
        v["fish_K"] = round(fK, 2)
        v["fish_best_night"] = {s: round(x, 3) for s, x in fb.items()}
        out["villages"][node] = v
    return out


# ---------------------------------------------------------------------- the runs
def stretch_ice(w, node, day):
    from cybertron2.engine import wild as WL
    from cybertron2.wild import water as WT
    for pid in sorted(w.s["parcels"]):
        par = w.s["parcels"][pid]
        if par.get("node") == node and par.get("cover") == "water" and WL._river_parcel(w, pid):
            return WT.ice(w, pid, day)
    return "open"


def runs(w, years, cued=True, stops=None, run_rows=None, ice=True, reseed=False):
    """The runs over `years` years from the world's first day; returns per village and night what passed, and the starts' causes."""
    from cybertron2.engine import wild as WL
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.wild import ecology as EC, kinds as WK, runs as RU
    m = WL.model(w)
    if not RU.active(m):
        return {"active": False}
    saved = None
    if run_rows is not None:
        saved = copy.deepcopy(WK.RUNS)
        WK.RUNS.clear()
        WK.RUNS.update(copy.deepcopy(run_rows))
    try:
        nt = RU.net(m)
        st = copy.deepcopy(w.s["wild"]["state"])
        R = RU.state(st)
        if reseed:                                                          # the fix arm: an up-run's spawning stretches that the build
            for k, r in RU.runners_of(m).items():                           # left empty (the history's end drops the pulses still in
                if r["dir"] != "up":                                        # flight) get the build's own seed, seed_km a km
                    continue
                sp = R["spawned"].setdefault(k, {})
                for g in nt.spawns(r.get("where", "river"), r.get("spawn")):
                    if float(sp.get(g, 0.0)) <= 1e-6:
                        sp[g] = round(float(r["return"]["seed_km"]) * nt.km[g], 4)
        Y = w.year_days()
        nodes = sorted(set(m.nodes))
        land = w.s["wild"]["land"]
        villages = sorted(n for n in w.s["nodes"] if f"v:{n}" in nt.members)
        K = RU.runners_of(m)
        lagm = {}
        for n in villages:
            path = nt.path_up(f"v:{n}")
            lagm[n] = sum(nt.lag(a, b, float(WK.RUN["km_a_day"])) for a, b in zip(path, path[1:]))
        passed = {n: [] for n in villages}                                  # [day, kind, heads, held]
        starts = []                                                         # [d1, kind, stretch, heads, cause]
        cond = {n: [] for n in villages}                                    # [day, rain ratio at its catchment, temp, flow, ice]
        mouth_cue = []                                                      # [d1, kind, mouth, inside, last, cued]
        village_cue = []                                                    # [d1, kind, village, cued, iced]: a down-run's own stretch
        rain_sum = {n: 0.0 for n in villages}                               # the engine's rain at each village's catchment, mm a day
        wx_next = WL.weather(w, nodes, 0)
        for d in range(years * Y):
            eday = WL.eco_day(w, d)
            wx = wx_next
            wx_next = WL.weather(w, nodes, d + 1)
            EC.step(m, st, eday, wx, WL.draws(w, eday, "sweep"), history=True)
            iced = {}
            if ice:
                for n in villages:
                    ic = stretch_ice(w, n, d)
                    if ic != "open":
                        iced[f"v:{n}"] = ic
            mem0 = R.setdefault("rain", {})
            mem = {nd: [round(float((wx.get(nd) or {}).get("rain", 0.0)), 3)] + list(mem0.get(nd) or [])[:RU.MEMORY - 1]
                   for nd in sorted({x for g in nt.catch for x in nt.catch[g]})}
            for n in villages:
                g = f"v:{n}"
                rr = RU.catch_rain(nt, g, mem, 0) / RU.RAIN_MEAN
                rain_sum[n] += RU.catch_rain(nt, g, mem, 0)
                fl = RU.flow(nt, g, mem, WATER_WORKS["weir"]["wear"]["flow_at"])
                cond[n].append([d, round(rr, 3), round(float(wx[nt.node[g]]["temp"]), 2), fl, iced.get(g, "open")])
                for p in RU.today(m, st, eday):
                    if p["g"] != g or float(p["n"]) <= 1e-6:
                        continue
                    ic = iced.get(g)
                    if not p.get("held") and ic and (p["dir"] == "down" or ic == "over"):
                        continue                                            # held under the ice: counted the night it moves on
                    passed[n].append([d, p["k"], round(float(p["n"]), 3), bool(p.get("held"))])
            cue_mem = {nd: [round(float((wx_next.get(nd) or {}).get("rain", 0.0)), 3)] + list(mem.get(nd) or [])[:RU.MEMORY - 1] for nd in mem}
            d1 = eday + 1
            pre = {}
            for k, r in K.items():
                inside, first, last = RU._window(m, d1, r["seasons"])
                if not inside:
                    continue
                cal = RU._calendar_cue(m, d1, r["seasons"])
                if r["dir"] == "up":
                    for mo in sorted({nt.mouth(g) for g in (R["due"].get(k) or {})} | {nt.mouth(g) for g in nt.spawns(r.get("where", "river"), r.get("spawn"))}):
                        c = RU.cued(nt, mo, r["cue"], cue_mem) if cued else cal
                        mouth_cue.append([d + 1, k, mo, True, bool(last), bool(c)])
                        pre[(k, mo)] = "cue" if c and cued else ("set night" if c else ("last day" if last else None))
                else:
                    for g in nt.members:
                        c = RU.cued(nt, g, r["cue"], cue_mem) if cued else cal
                        pre[(k, g)] = ("cue" if cued else "set night") if c else None
                        if g.startswith("v:") and g[2:] in passed:
                            village_cue.append([d + 1, k, g[2:], bool(c), bool(g in iced)])
            pool = {}
            for k, r in K.items():                                          # what each stretch has still to run tonight, before it starts
                inside, first, last = RU._window(m, d1, r["seasons"])
                if not inside:
                    continue
                yr = d1 // m.Y
                if r["dir"] == "down":
                    pop = st["pop"].get(k)
                    if first or R["year"].get(k) != yr:
                        q = {}
                        for g_, ms in nt.members.items():
                            for a in ms:
                                i = nt.ix[a]
                                if float(land["areas"][a].get("river_km", 0.0)) > 0 or a in land.get("down", {}):
                                    c = float(pop[i]) * float(m.km2[i]) * float(r["year"])
                                    if c > 1e-6:
                                        q[a] = c
                    else:
                        q = dict(R["quota"].get(k) or {})
                    pool[k] = q
                else:
                    if first or R["year"].get(k) != yr:
                        ret = r["return"]
                        q = {}
                        for g_, s_ in (R["spawned"].get(k) or {}).items():
                            cap = float(ret["cap_km"]) * max(nt.km.get(g_, 0.0), 1e-6)
                            n_ = float(ret["r"]) * float(s_) / (1.0 + float(s_) / cap)
                            if n_ > 1e-6:
                                q[g_] = n_
                    else:
                        q = dict(R["due"].get(k) or {})
                    pool[k] = q
            RU.advance(m, st, eday, wx, wx_next, stops=stops, weather=cued, iced=iced)
            for k, q in pool.items():
                after = (R["quota"].get(k) or {}) if K[k]["dir"] == "down" else (R["due"].get(k) or {})
                by = {}
                for a, x in q.items():
                    n_ = x - float(after.get(a, 0.0))
                    if n_ > 1e-6:
                        key = nt.group[a] if K[k]["dir"] == "down" else nt.mouth(a)
                        by[key] = by.get(key, 0.0) + n_
                for key, n_ in sorted(by.items()):
                    starts.append([d + 1, k, key, round(n_, 3), pre.get((k, key)) or "?"])
        return {"active": True, "years": years, "Y": Y, "villages": villages, "lag_from_mouth": lagm, "passed": passed, "cond": cond,
                "starts": starts, "mouth_cue": mouth_cue, "village_cue": village_cue,
                "catch_rain_mean": {n: round(x / (years * Y), 3) for n, x in rain_sum.items()}, "kinds": {k: {"dir": r["dir"], "seasons": r["seasons"]} for k, r in K.items()},
                "eco_day0": WL.eco_day(w, 0)}
    finally:
        if saved is not None:
            WK.RUNS.clear()
            WK.RUNS.update(saved)


# ---------------------------------------------------------------------- one world
def maker_stock(world, wid):
    from cybertron2.specs import make_water_worlds as WW
    world = copy.deepcopy(world)
    if wid == "eelmouth":
        return world, "eelmouth's own (make_nutrition_runs RESIDENT_SHARE 0.25: K 4.4 a unit of size, r 0.3, fast)"
    WW.water_stocks(world, 32)
    return world, "make_water_worlds.water_stocks (K 17.6 a unit of size, r 0.3; a mere 16,500 a km2, LAKE_TURNOVER 0.4)"


def mill_stops(w, m):
    """The laid worlds' dam arm: a shut mill at the village whose generated mill stands (Middleham), stop 0.5."""
    from cybertron2.engine.data import WATER_WORKS
    out = {}
    for bid, b in sorted(w.s["buildings"].items()):
        if (b.get("fittings") or {}).get("water wheel"):
            out[f"v:{b['node']}"] = float(WATER_WORKS["mill"]["stop"])
    return out


def one(wid, years=6) -> dict:
    t0 = time.time()
    out = {"id": wid, "seconds": {}}
    try:
        raw = load(wid)
        raw.setdefault("agents", {})
        if wid != "eelmouth":
            raw["packs"] = sorted(set(raw.get("packs") or []) | {"wild", "water"})
        w0 = build(raw)
        out["census_generated"] = census(w0, raw, "generated")
        stocked, how = maker_stock(raw, wid)
        w = build(stocked) if wid != "eelmouth" else w0
        out["census_maker"] = census(w, stocked, "maker")
        out["maker_rule"] = how
        out["seconds"]["census"] = round(time.time() - t0, 1)
        out["runs_cue"] = runs(w, years, cued=True)
        out["seconds"]["runs_cue"] = round(time.time() - t0, 1)
        out["runs_set"] = runs(w, 2, cued=False)
        out["runs_fix"] = runs(w, years, cued=True, reseed=True)
        R0 = w.s["wild"]["state"]["runs"]
        out["spawned_at_build"] = {k: {g: round(float(x), 2) for g, x in (R0["spawned"].get(k) or {}).items()} for k in R0["spawned"]}
        from cybertron2.engine import wild as WL
        st_ = mill_stops(w, WL.model(w))
        if st_:
            out["dam_stops"] = st_
            out["runs_dam"] = runs(w, years, cued=True, stops=st_)
        out["seconds"]["all"] = round(time.time() - t0, 1)
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
        out["trace"] = traceback.format_exc()[-1500:]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, wid + ".json"), "w") as f:
        json.dump(out, f, separators=(",", ":"), default=float)
    return {"id": wid, "error": out.get("error"), "seconds": out["seconds"]}


def ids_all():
    idx = json.load(open(os.path.join(HERE, "data", "worlds_index.json")))
    return [r["id"] for r in idx["rows"] if r["ok"]] + ["eelmouth"]


def main(argv=None):
    a = list(argv if argv is not None else sys.argv[1:])
    years = int(a[a.index("--years") + 1]) if "--years" in a else 6
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 4
    which = a[0] if a and not a[0].startswith("--") else "all"
    ids = ids_all() if which == "all" else which.split(",")
    if "--skip-done" in a:
        ids = [i for i in ids if not os.path.exists(os.path.join(OUT, i + ".json"))]
    if jobs <= 1 or len(ids) == 1:
        res = [one(i, years) for i in ids]
    else:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(jobs) as pool:
            res = pool.starmap(one, [(i, years) for i in ids])
    for r in res:
        print(r, flush=True)


if __name__ == "__main__":
    main()
