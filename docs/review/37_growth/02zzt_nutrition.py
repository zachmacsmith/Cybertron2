"""02zzt's nutrition measure: food a unit of work and food a year by source, on each calibration world (Zach, 20 Nov: "The
calibration should look how different sources of nutrition, different wildlife, different weather conditions and likelihood,
different world environments (e.g. soil types etc.) all vary across these worlds").

Two parts, both the engine's own models offline:
- **The land's year** (cybertron2/capacity, D4-102): at each village, at the levels bare, standing, worked and best, the food a
  year each source gives at full take and the work it takes (fields, herds, wild plants, game, resident fish), people fed by each
  source alone, arable food a plot by soil and ground, and the share lost in store (preserving's effect). The world is read without
  the wild pack (the capacity model reads the parcels' own stocks), with resident fish stocked in every water parcel as brief 5's
  worlds are (make_water_worlds.water_stocks: K 8 a unit of size, r 0.3).
- **The acts** (02zzd's harness, docs/review/37_growth/02zzd_ev/ev_harness.py): one probe person added to a village's first
  house (the only person in the world: a small cast where the check needs one), on the world with the wild and water packs, in
  autumn; each act tried on a fresh copy of the world (nothing depletes between tries), at novice, capable and master. Hunting the
  wild near, in the wood around and far, armed; gathering wild food in a wood and on open ground; eel traps and nets on the water;
  fishing by hand and with a rod. Food is the edible goods gained (ITEMS food a unit), a unit of work the act's own units with
  its range's.

The runs (salmon, lamprey, the eels' run down) are read from the ecology's runs in 02zzt_calibration_suite.py.
"""
from __future__ import annotations

import contextlib
import copy
import io
import os
import statistics
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "02zzd_ev"))
os.environ.setdefault("CYB_ROOT", os.path.abspath(os.path.join(HERE, "..", "..", "..")))

LEVELS_CAP = ("bare", "standing", "worked", "best")
HARD = (("novice", 1.0, 0.35), ("capable", 3.0, 0.6), ("master", 8.0, 0.6))      # the hunt's curve (02zzd's ev_region; brief 4c §3.1)
TRIES = 12                       # a try each, on a fresh copy; the hunt's cells take HUNT_TRIES (its luck is wider)
HUNT_TRIES = 20
AUTUMN = {"season": "autumn", "day": 2, "season_days": 8}


def _basic_levels():
    from cybertron2.engine.data import SKILL
    lo, hi = SKILL["basic"]
    return (("novice", float(lo), 0.35), ("capable", (float(lo) + float(hi)) / 2, 0.6), ("master", float(hi), 0.6))


def land_year(spec: dict) -> dict:
    """The capacity model at each village: food a year and a unit of work by source and level."""
    from cybertron2.capacity import model as CM
    from cybertron2.specs.make_water_worlds import water_stocks
    sp = copy.deepcopy(spec)
    sp["agents"] = {}
    sp["packs"] = ["water"]
    stocked = water_stocks(sp)
    with contextlib.redirect_stdout(io.StringIO()):
        w = CM.world_of(sp)
    m = CM.mix(w)
    need_year = m["eats"] * w.year_days()
    out = {"eats a day": m["eats"], "units a year": round(m["units"], 1), "water parcels stocked": stocked["water parcels stocked"],
           "villages": {}}
    for nid in sorted(n for n in w.s["nodes"] if n.startswith("s")):
        rec = {}
        for lvl in LEVELS_CAP:
            with contextlib.redirect_stdout(io.StringIO()):
                ctx = CM.context(w, lvl, nodes={nid})
                fl = CM.flows(ctx, {nid})
                ls = CM.lots(ctx, fl)
                sup = CM.people_supported(ctx, ls, m)
                at = sup if sup > 0 else 0.0
                scale = CM.allocate(ls, at * m["units"] * ctx.level.labour_share)
                sim = CM.simulate(ctx, ls, scale, CM.need(ctx, ls, scale, at, m))
            by = {}
            for l in ls:
                b = by.setdefault(l.flow.source, {"food a year": 0.0, "work a year": 0.0})
                b["food a year"] += l.flow.qty * l.value
                b["work a year"] += l.work
            for b in by.values():
                b["food a unit"] = round(b["food a year"] / b["work a year"], 3) if b["work a year"] > 0 else None
                b["people fed alone"] = round(b["food a year"] / need_year, 2)
                b["food a year"] = round(b["food a year"], 1)
                b["work a year"] = round(b["work a year"], 1)
            soil = {}
            if lvl in ("standing", "worked"):
                for l in ls:
                    if l.flow.source != "fields":
                        continue
                    p = w.s["parcels"].get(l.flow.where) or {}
                    sp_p = (sp["nodes"][nid]["parcels"].get(l.flow.where) or {})
                    key = f"{sp_p.get('soil', '?')} / {sp_p.get('terrain', '?')}"
                    s_ = soil.setdefault(key, {"plots": 0.0, "food": 0.0})
                    s_["plots"] += float(p.get("size", 1))
                    s_["food"] += l.flow.qty * l.value
                soil = {k: {"plots": v["plots"], "food a plot a year": round(v["food"] / max(v["plots"], 1e-9), 1)} for k, v in soil.items()}
            rec[lvl] = {"people supported": round(sup, 2), "by source": by,
                        "lost in store share": round(sim["waste"] / max(1e-9, sim["eaten"] + sim["waste"]), 3),
                        "gave up": list(ctx.level.gave_up), **({"fields by soil / ground": soil} if soil else {})}
        out["villages"][nid] = rec
    return out


def _probe_world(spec: dict, nid: str):
    from cybertron2.engine.world import World
    from cybertron2.specs.make_water_worlds import water_stocks
    sp = copy.deepcopy(spec)
    sp["calendar"] = dict(AUTUMN)
    sp["packs"] = ["wild", "water"]
    house = next(b for b in sp["buildings"].values() if (b.get("fittings") or {}).get("beds") and str(b["parcel"]).startswith(nid + "_"))
    sp["agents"] = {"Probe": {"household": house["household"], "born": -30, "stage": "adult", "sex": "m", "knows": {},
                              "holdings": {"crude tool": 1, "fishing rod": 1}, "model": "bot"}}
    water_stocks(sp)
    with contextlib.redirect_stdout(io.StringIO()):
        return World(sp)


def acts(spec: dict, nid: str, tries: int = TRIES) -> dict:
    """Food a unit of work by act and skill at one village, autumn, on fresh copies of the world."""
    import ev_harness as H
    w0 = _probe_world(spec, nid)
    pars = [p for p in w0.s["parcels"].values() if p["node"] == nid]
    pick = lambda covers: next((p["name"] for p in sorted(pars, key=lambda p: -float(p.get("size", 1))) if p.get("cover") in covers), None)
    forest, open_, water = pick({"forest"}), pick({"meadow", "pasture"}), pick({"water"})
    wetland = water or pick({"fen"})
    cells = [("hunt the wild", r, forest, True, HARD) for r in ("near", "the wood around", "far")]
    cells += [("gather wild food", None, forest, False, _basic_levels()), ("gather wild food", None, open_, False, _basic_levels())]
    cells += [("trap in water", "near", wetland, False, HARD), ("net", "near", wetland, False, HARD)]
    cells += [("fish by hand", None, water, False, _basic_levels()), ("angle", None, water, False, _basic_levels())]
    out = []
    for method, rng, where, armed, levels in cells:
        if where is None:
            out.append({"method": method, "range": rng, "at": None, "why": "no such ground at the village"})
            continue
        for lvl, sk, fam in levels:
            got = []
            for s in range(HUNT_TRIES if method == "hunt the wild" else tries):
                act = {"do": "gather", "what": method, "at": where}
                if rng:
                    act["range"] = rng
                g = H.attempt(w0, "Probe", act, method, sk, fam, f"{nid}{method}{rng}{where}{lvl}{s}", armed=armed)
                if g is not None:
                    got.append(g)
            u = H.units(method, rng) if rng else int(__import__("cybertron2.engine.data", fromlist=["T"]).TECHNIQUES[method]["units"])
            out.append({"method": method, "range": rng, "at": where, "level": lvl, "armed": armed, "tries": len(got),
                        "food a unit": round(statistics.mean(got) / u, 3) if got else None,
                        "share of tries with food": round(sum(1 for g in got if g > 0.05) / len(got), 2) if got else None,
                        **({} if got else {"why": "refused every try"})})
    return {"village": nid, "season": "autumn", "acts": out}


def nutrition(spec: dict) -> dict:
    """Both parts. The acts at the village with the most water (fishing needs water parcels; with none, the first village)."""
    out = {"land year": land_year(spec)}
    vil = sorted(n for n in spec["nodes"] if n.startswith("s"))
    water = {n: sum(float(p.get("size", 1)) for p in spec["nodes"][n]["parcels"].values() if p["cover"] == "water") for n in vil}
    nid = max(vil, key=lambda n: (water[n], -vil.index(n)))
    try:
        out["acts"] = acts(spec, nid)
    except Exception as e:  # noqa: BLE001 (reported)
        import traceback
        out["acts"] = {"village": nid, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1200:]}
    return out
