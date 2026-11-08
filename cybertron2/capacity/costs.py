"""What a level costs (D4-102): the work it takes every year, and what must be built and made first, for a population it feeds.

Recurring work: the units a year the fed population gives its food (the model's allocation: field work, foraging, hunting, milking,
processing) and its fuel (fuel.py), a head and as a share of all its work.
Up-front capital, from the engine's tables:
- processing fittings, as many as the year's throughput needs: a fitting does one batch (TECHNIQUES inputs) for each batch of a
  worker's units, so a hand mill grinds 3 grain a unit, a water mill 200 grain each 2 units, at a worker's mean units a day;
- stores for the year's peak stock (the simulation's): a granary floor 300 grain, bins 60 food (FITTINGS holds), else free floor;
- tools worn out a year (TECHNIQUES wear a use, ITEMS life), with their inputs; a plough and harness where the level ploughs;
- houses for the people: a medium timber room (ROOMS) for each PEOPLE_A_HEARTH, its hearth (FITTINGS) and a bed each;
- ground turned to field (CLEARING units a unit of size; a wood felled first, TECHNIQUES fell).
Each item is given in units of work and materials; `units_a_head` divides the one-off work by the people fed.
"""
from __future__ import annotations

import math

from cybertron2.engine import capacity as CAP
from cybertron2.engine.data import CLEARING, FITTINGS, ITEMS, PHYSICS, ROOMS, TECHNIQUES
from cybertron2.capacity import food as FD, rotation as RO


def worker_day(w) -> float:
    from cybertron2.capacity import cal as CL
    t = CL.seasons(w)
    return sum(float(PHYSICS["units"][s]) for s in t) / len(t)


def _cold(w, b) -> list:
    """Each year day's cold at a building's place, or (a building not yet placed) the share of the people whose night is cold."""
    from cybertron2.capacity import cal as CL
    if b.get("node"):
        return [1.0 if c else 0.0 for _, c in CL.table(w, b["node"])]
    return CL.cold_shares(w)


def _add(d, k, q):
    d[k] = round(d.get(k, 0.0) + q, 2)


def capital(ctx, ls, scale, P, sim) -> dict:
    from cybertron2.capacity import graph as GR
    w = ctx.w
    items, mats, units = [], {}, 0.0
    per_day = worker_day(w)
    emb = GR.embodied(GR.processes(tools=ctx.level.tools, level=ctx.level, window=ctx.window, year=ctx.year))
    embodied_total = 0.0

    def build(label, n, materials, u, why):
        nonlocal units, embodied_total
        if n <= 0:
            return
        e = u + sum(float(q) * emb.get(m, (0.0, ""))[0] for m, q in (materials or {}).items())
        items.append({"what": label, "n": n, "units": round(n * u, 1), "with_materials": round(n * e, 1), "why": why})
        units += n * u
        embodied_total += n * e
        for m, q in (materials or {}).items():
            _add(mats, m, n * float(q))

    # processing: each technique on each lot's route, by its throughput
    through = {}
    for l, s in zip(ls, scale):
        if s <= 0:
            continue
        q = l.flow.qty * s                                        # units of the good a year
        for t in FD.worth(l.flow.good, ctx.level.cook, ctx.reach)[3]:
            d = TECHNIQUES[t]
            ins = d.get("inputs") or {}
            a = float(next(iter(v for k, v in ins.items() if k in FD.EDIBLE)))
            through[t] = through.get(t, 0.0) + q / ctx.year
            q = q / a * float(next(iter(d["gives"].values())))
    for t, day in through.items():
        d = TECHNIQUES[t]
        fits = (d.get("at") or {}).get("fittings") or []
        if not fits:
            continue
        f = next((x for x in fits if ctx.reach.fitting(x)), fits[0])
        batch = float(next(iter(v for k, v in (d.get("inputs") or {}).items() if k in FD.EDIBLE)))
        cap = batch * per_day / float(d.get("units", 1))
        n = max(1, math.ceil(day / cap))
        if f in ("hearth", "fire ring"):
            continue                                              # the houses' hearths
        fd = FITTINGS[f]
        build(f, n, fd.get("materials"), float(fd.get("units", 0)), f"{t}: {day:.0f} a day, {cap:.0f} a fitting")
        if fd.get("needs"):
            nd = FITTINGS[fd["needs"]]
            build(fd["needs"], n, nd.get("materials"), float(nd.get("units", 0)), f"needed by the {f}")
    # stores for the peak
    peak_food = sum((sim.get("peak") or {}).values())
    st = ctx.level.store
    if st in ("granary", "bins", "cellar") and peak_food > 0:
        hold = float(next(iter((FITTINGS[st].get("holds") or {"food": 40}).values())))
        g = FD.worth("grain", ctx.level.cook, ctx.reach)[0] or 1.0
        n = math.ceil(peak_food / g / hold) if st == "granary" else math.ceil(peak_food / hold)
        build(st, n, FITTINGS[st].get("materials"), float(FITTINGS[st].get("units", 0)), f"peak stock {peak_food:.0f} food")
    # houses
    if P > 0 and ctx.level.name != "bare":
        rooms = math.ceil(P / float(CAP.PEOPLE_A_HEARTH))
        r = ROOMS["medium room"]["timber"]
        build("medium room (timber)", rooms, r["materials"], float(r["units"]), f"{P:.0f} people")
        build("hearth", rooms, FITTINGS["hearth"]["materials"], float(FITTINGS["hearth"]["units"]), "one a room")
        build("beds", math.ceil(P), FITTINGS["beds"]["materials"], float(FITTINGS["beds"]["units"]), "one a sleeper")
    # tools worn a year (recurring, given as a year's)
    tools = {}
    if ctx.level.tools != "bare":
        per, _ = RO.crop_work(ctx.level, False)
        reap = 1.0 / (float(TECHNIQUES["reap"]["yield"]["plots"]) * RO.tool_mult("reap", ctx.level.tools))
        hoe = 1.0 / (float(TECHNIQUES["hoe"]["yield"]["plots"]) * RO.tool_mult("hoe", ctx.level.tools)) if ctx.level.broken else 0.0
        worn_share = (reap * float(TECHNIQUES["reap"].get("wear", 0)) + hoe * float(TECHNIQUES["hoe"].get("wear", 0))) / per
        for l, s in zip(ls, scale):
            if s > 0 and l.flow.source == "fields":
                tools["fields"] = tools.get("fields", 0.0) + l.flow.work * s * worn_share
    life = float(ITEMS.get(f"{ctx.level.tools} tool", {}).get("life", 10) or 10)
    worn = sum(tools.values()) / life if tools else 0.0
    tool_tech = TECHNIQUES.get(f"{ctx.level.tools} tool") or {}
    year_mats = {m: round(worn * float(q), 2) for m, q in (tool_tech.get("inputs") or {}).items()}
    # cleared ground
    for pid in sorted(ctx.as_field):
        par = w.s["parcels"][pid]
        u = float(CLEARING.get(par["cover"], CLEARING["scrub"])) * float(par["size"])
        if par["cover"] == "forest":
            trees = float(((par.get("res") or {}).get("wood") or {}).get("S", 0))
            y = TECHNIQUES["fell"]
            u += trees / float(y["yield"]["base"]) * float(y["units"])
        build(f"clear {par['name']}", 1, {}, u, par["cover"])
    tool_work = worn * emb.get(f"{ctx.level.tools} tool", (0.0, ""))[0] if ctx.level.tools != "bare" else 0.0
    houses = {"medium room (timber)", "hearth", "beds"}
    rooms = sum(i["n"] for i in items if i["what"] == "medium room (timber)")
    upkeep = rooms * upkeep_a_building(w, {"structure": "timber", "rooms": [{"kind": "medium room", "floor": ROOMS["medium room"]["floor"]}]}, emb)
    equip = round(sum(i["with_materials"] for i in items if i["what"] not in houses), 1)
    house = round(sum(i["with_materials"] for i in items if i["what"] in houses), 1)
    return {"items": items, "materials": mats, "units": round(units, 1), "units_a_head": round(units / P, 1) if P else None,
            "equipment": equip, "houses": house, "upkeep_a_year": round(upkeep, 1),
            "with_materials": round(embodied_total, 1), "with_materials_a_head": round(embodied_total / P, 1) if P else None,
            "tools_a_year": round(worn, 1), "tool_materials_a_year": year_mats, "tool_work_a_year": round(tool_work, 1),
            "embodied": {g: round(v, 3) for g, (v, _) in emb.items() if g in FD.EDIBLE}}


def upkeep_a_building(w, b, emb) -> float:
    """Work a year to keep a building sound: its expected breaks a year (night.py: PHYSICS breaks by night, cold nights by world.cold,
    by structure) x its repair (buildings.repair_need), with its materials' embodied work. Fittings themselves do not wear in the
    engine; the buildings that hold them do (counted for houses only, for now)."""
    from cybertron2.capacity import cal as CL
    from cybertron2.engine import buildings as BU
    p = PHYSICS["breaks"]
    k = float(p["structure"].get(b.get("structure"), 1.0))
    breaks = sum((float(p["cold"]) * c + float(p["p"]) * (1 - c)) * k for c in _cold(w, b))      # where it stands (D4-111)
    need = BU.repair_need(b)
    return breaks * (float(need["units"]) + sum(float(q) * emb.get(m_, (0.0, ""))[0] for m_, q in need["materials"].items()))


def recurring(ctx, ls, scale, P, m) -> dict:
    work = sum(l.work * s for l, s in zip(ls, scale))
    total = P * m["units"]
    eaten = sum(l.flow.qty * l.value * s for l, s in zip(ls, scale))
    return {"food_work": round(work, 1), "a_head": round(work / P, 1) if P else None,
            "share": round(work / total, 3) if total else None, "food_a_unit": round(eaten / work, 2) if work else None}


def land(ctx, ls, scale, plots) -> dict:
    eaten = sum(l.flow.qty * l.value * s for l, s in zip(ls, scale) if l.flow.source == "fields")
    work = sum(l.work * s for l, s in zip(ls, scale) if l.flow.source == "fields")
    return {"field_food_a_plot": round(eaten / plots, 1) if plots else None, "field_work_a_plot": round(work / plots, 1) if plots else None}
