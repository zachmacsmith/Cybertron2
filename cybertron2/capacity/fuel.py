"""Fuel capacity (D4-102): how many people a world's woods keep warm and cooking, at three levels of woodcraft.

Need: a hearth's heat a year, night by night from the engine's calendar (PHYSICS heat: cold nights by world.cold), shared by
PEOPLE_A_HEARTH. Supply, from forests.py's own night rules (shed_a_night, young_step, trees_step; slowed by night.slow_season): dead
wood as the trees shed it, young growth and trees at their best steady take. Levels:
- gathered: dead wood only, by hand (TECHNIQUES firewood);
- cut: and young growth cut with a tool (TECHNIQUES cut);
- managed: and trees felled at their growth (TECHNIQUES fell).
Each level's heat counts its flow; `standing` is the one-off heat in the stocks (what a run can burn into), in years of the people's
need. Work a heat: each technique's yield a unit at its tool.
"""
from __future__ import annotations

from cybertron2.engine import capacity as CAP
from cybertron2.engine.data import ITEMS, PHYSICS, TECHNIQUES

LEVELS = ("gathered", "cut", "managed")
HEAT = {"firewood": float(ITEMS["firewood"]["heat"]), "timber": float(ITEMS["timber"]["heat"])}


def hearth_heat(w, nodes=None) -> float:
    """A hearth's heat a year by the engine's calendar: PHYSICS heat cold on cold nights (world.cold), normal on the rest; over
    several places, by the share of the people whose night is cold (cal.cold_shares; D4-111)."""
    from cybertron2.capacity import cal as CL
    hp = PHYSICS["heat"]
    return sum(float(hp["cold"]) * k + float(hp["normal"]) * (1 - k) for k in CL.cold_shares(w, nodes))


def need_per_person(w, nodes=None) -> float:
    return hearth_heat(w, nodes) / float(CAP.PEOPLE_A_HEARTH)


def _msy(step, K):
    best = 0.0
    for i in range(1, 200):
        S = K * i / 200
        best = max(best, step(S) - S)
    return best


def parcel_flows(w, par) -> dict:
    """{dead, young, trees} heat a year at the best steady take (forests.dead_step's inflow, forests.young_step and
    forests.trees_step at their best stock, by the calendar's slow season), and the standing heat in all three."""
    from cybertron2.capacity import cal as CL
    from cybertron2.engine import forests as FO, night as NI
    res = par.get("res") or {}
    year = float(w.year_days())
    days = CL.seasons(w)
    slow = [float(PHYSICS["regrow_winter"]) if NI.slow_season(s_) else 1.0 for s_ in days]
    t, y, d = res.get("wood"), res.get("young"), res.get("dead")
    out = {"dead": 0.0, "young": 0.0, "trees": 0.0, "standing": 0.0}
    if t and float(t["K"]) > 0:
        trees = float(t["S"])
        out["dead"] = len(days) * FO.shed_a_night(trees, year) * HEAT["firewood"]
        K, r = float(t["K"]), float(t["r"])
        out["trees"] = sum(_msy(lambda S, k=k: FO.trees_step(S, K, r, k), K) for k in slow) * HEAT["timber"]
        out["standing"] += trees * HEAT["timber"]
    if y and float(y["K"]) > 0:
        K, r = float(y["K"]), float(y["r"])
        out["young"] = sum(_msy(lambda S, k=k: FO.young_step(S, K, r, k), K) for k in slow) * HEAT["firewood"]
        out["standing"] += float(y["S"]) * HEAT["firewood"]
    if d:
        out["standing"] += float(d["S"]) * HEAT["firewood"]
    return out


def parcel_heat(w, par) -> float:
    f = parcel_flows(w, par)
    return f["dead"] + f["young"] + f["trees"]


def _per_unit():
    fw = float(TECHNIQUES["firewood"]["yield"]["base"]) * HEAT["firewood"]
    cut = float(TECHNIQUES["cut"]["yield"]["base"]) * float(TECHNIQUES["cut"]["tools"]["crude"]) * HEAT["firewood"] / float(TECHNIQUES["cut"]["units"])
    fell = float(TECHNIQUES["fell"]["yield"]["base"]) * float(TECHNIQUES["fell"]["tools"]["crude"]) * HEAT["timber"] / float(TECHNIQUES["fell"]["units"])
    return {"dead": fw, "young": cut, "trees": fell}


def supply(w, nodes=None, exclude=(), level="managed") -> dict:
    keys = {"gathered": ("dead",), "cut": ("dead", "young"), "managed": ("dead", "young", "trees")}[level]
    sus, standing, work, by = 0.0, 0.0, 0.0, {}
    pu = _per_unit()
    for pid, par in w.s["parcels"].items():
        if (nodes is not None and par["node"] not in nodes) or pid in exclude:
            continue
        f = parcel_flows(w, par)
        h = sum(f[k] for k in keys)
        if h > 0 or f["standing"] > 0:
            by[pid] = round(h, 1)
        sus += h
        standing += f["standing"]
        work += sum(f[k] / pu[k] for k in keys)
    return {"sustained": sus, "standing": standing, "work": work, "by_parcel": by}


def report(w, nodes, P) -> dict:
    npp = need_per_person(w, nodes)
    out = {"need_a_head": round(npp, 2), "levels": {}}
    for lvl in LEVELS:
        s = supply(w, nodes, level=lvl)
        sup = s["sustained"] / npp
        out["levels"][lvl] = {"supported": round(sup, 1), "ratio": round(sup / P, 2) if P else None,
                              "heat_a_year": round(s["sustained"], 1),
                              "work_a_head": round(s["work"] / max(sup, 1e-9), 1) if sup else None}
    s = supply(w, nodes)
    out["standing_years"] = round(s["standing"] / max(1e-9, P * npp), 1) if P else None
    out["standing_heat"] = round(s["standing"], 0)
    return out
