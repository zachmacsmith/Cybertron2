"""The ladder of practice (D4-102): the levels as a graded order, one improvement at a time.

The levels are bundles of switches and dials. The ladder starts bare and climbs one change at a time: on each rung it tries every
single change the world can reach (a dial raised to any higher setting: cooking raw, boiled, ground, milled; storing open, house, bins, cellar,
granary; weeding 0, 8, 16; tools bare, crude, copper; or a switch on: fields, rotation, breaking, manure, herds, selection, master
farmers, rye over winter, hunting) and takes the one that adds most people fed for its cost. Two costs, kept apart:
- capital, once: the equipment the step needs (with its materials' work);
- ongoing work a year: running it (food work), tools worn, and the houses' upkeep (expected breaks x repair).
Only to rank the steps is the capital spread over AMORTISE years and added to the extra ongoing work a head (for all fed); a step that
costs nothing more is taken first, largest gain first. Each rung reports both, people fed and the ratio to the people there, the
ongoing work as a share of the people's work, and food a plot and a unit of work.
"""
from __future__ import annotations

from dataclasses import replace

from cybertron2.capacity import costs as CO, levels as LV, model as M

AMORTISE = 1.0          # years over which a step's equipment is spread when ranking steps (an engine year); reported apart, never added
DIALS = {"cook": ("raw", "boiled", "ground", "milled"), "store": ("open", "house", "bins", "cellar", "granary"),
         "weed": (0.0, 8.0, 16.0), "tools": ("bare", "crude", "copper"), "rotation": ("once", "best"),
         "herds": ("none", "milk", "milk+offtake")}
SWITCHES = ("fields", "broken", "manure", "selection", "master", "winter_crop", "hunt")
WORDS = {"cook": "cook", "store": "keep in", "weed": "weed (units a plot)", "tools": "tools", "rotation": "crops a year",
         "herds": "herds", "fields": "sow the fields", "broken": "break the soil", "manure": "manure", "selection": "select seed",
         "master": "master farmers", "winter_crop": "rye over winter", "hunt": "hunt"}


def evaluate(w, lv, nodes, m, P_here) -> dict:
    r = LV.reach(w)
    lv = lv.within(r)
    from cybertron2.capacity import cal as CL
    ctx = M.Ctx(w=w, level=lv, reach=r, year=w.year_days(), season_len=w.season_len, cal=CL.table(w), window=CL.growing_window(w))
    ls = M.lots(ctx, M.flows(ctx, nodes))
    sup = M.people_supported(ctx, ls, m)
    scale = M.allocate(ls, sup * m["units"] * lv.labour_share)
    sim = M.simulate(ctx, ls, scale, sup * m["eats"])
    cap = CO.capital(ctx, ls, scale, sup, sim)
    rec = CO.recurring(ctx, ls, scale, sup, m)
    plots = sum(float(p["size"]) for p in w.s["parcels"].values() if (nodes is None or p["node"] in nodes) and p["cover"] == "field")
    land = CO.land(ctx, ls, scale, plots)
    ongoing = rec["food_work"] + cap["tool_work_a_year"] + cap["upkeep_a_year"]
    return {"level": lv, "supported": sup, "ratio": round(sup / P_here, 2) if P_here else None, "equipment": cap["equipment"],
            "houses": cap["houses"], "tools_work": cap["tool_work_a_year"], "upkeep": cap["upkeep_a_year"], "food_work": rec["food_work"],
            "ongoing": round(ongoing, 1), "ongoing_a_head": round(ongoing / sup, 1) if sup else None,
            "ongoing_share_here": round(ongoing / max(sup, 1e-9) * P_here / (P_here * m["units"]), 3) if P_here and sup else None,
            "food_a_unit": rec["food_a_unit"], "food_a_plot": land["field_food_a_plot"],
            "items": [f"{i['n']} {i['what']}" for i in cap["items"] if i["what"] not in ("medium room (timber)", "hearth", "beds")]}


def moves(lv) -> list:
    out = []
    for k, steps in DIALS.items():
        cur = getattr(lv, k)
        i = steps.index(cur) if cur in steps else 0
        out += [(k, x) for x in steps[i + 1:]]                    # any higher notch: a granary need not follow a cellar
    for k in SWITCHES:
        if not getattr(lv, k):
            out.append((k, True))
    return out


def climb(w, nodes=None, start="bare", max_rungs=20) -> list:
    hb = M.homes_by_node(w)
    names = [n for k, v in hb.items() if nodes is None or k in nodes for n in v]
    m = M.mix(w, names) if names else M.mix(w)
    P_here = len(names)
    base = replace(LV.LEVELS[start], name="ladder", gave_up=(), rotation="once", fields=False, broken=False, weed=0.0, manure=False,
                   master=False, selection=False, winter_crop=False, cook="raw", store="open", tools="bare", herds="none",
                   hunt=False)
    r = LV.reach(w)
    cur = evaluate(w, base, nodes, m, P_here)
    rungs = [{"change": "nothing: wild food, raw, as gathered", **{k: v for k, v in cur.items() if k != "level"}}]
    lv = base
    for _ in range(max_rungs):
        best = None
        for k, v in moves(lv):
            trial = replace(lv, **{k: v})
            if getattr(trial.within(r), k) != v:                       # out of reach in this world
                continue
            e = evaluate(w, trial, nodes, m, P_here)
            gain = e["supported"] - cur["supported"]
            if gain <= 0.05:
                continue
            d_ongoing = max(0.0, e["ongoing_a_head"] - (cur["ongoing_a_head"] or 0.0)) * e["supported"]   # more work a head, for all fed
            d_capital = max(0.0, e["equipment"] - cur["equipment"])
            cost = d_ongoing + d_capital / AMORTISE
            score = (cost <= 1e-6, gain / max(cost, 1e-6), gain)
            if best is None or score > best[0]:
                best = (score, k, v, e, cost)
        if best is None:
            break
        _, k, v, e, cost = best
        lv = replace(lv, **{k: v})
        cur = e
        label = f"{WORDS[k]}: {v}" if k in DIALS else WORDS[k]
        rungs.append({"change": label, "capital_added": round(max(0.0, e["equipment"] - rungs[-1]["equipment"]), 1),
                      **{kk: vv for kk, vv in e.items() if kk != "level"}})
    return rungs
