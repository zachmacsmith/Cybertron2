"""What a good is worth eaten, and how fast it spoils (D4-102), from the engine's tables.

`worth(good, cook, r)`: the food a unit gives at the best route the cook level and the world allow: eaten raw without a hearth
(ITEMS raw), boiled at one (ITEMS food), or through the food techniques of TECHNIQUES (verb make, tag food) whose fittings the cook
level allows and the world reaches: a search, so a technique added to the data joins without a change here. A route's work (units a
unit of the good) and its other inputs (timber for baking) come with it.

`rate(good, store, season, cold)`: the share lost a night, by night.spoil_rate (the rule the engine's nights use).
"""
from __future__ import annotations

from cybertron2.engine.data import ITEMS, PHYSICS, TECHNIQUES
from cybertron2.capacity.levels import COOK_FITTINGS

EDIBLE = tuple(sorted(i for i, d in ITEMS.items() if float(d.get("food", 0) or 0) > 0))
FOOD_TECHS = tuple(sorted(t for t, d in TECHNIQUES.items() if d.get("verb") == "make" and "food" in (d.get("tags") or [])
                          and isinstance(d.get("gives"), dict)))


def base(good, hearth=True) -> float:
    from cybertron2.engine import night as NI
    return NI.eaten_worth(good, hearth)


def _tech_ok(t, allowed, r) -> bool:
    d = TECHNIQUES[t]
    if r is not None and not r.knows(t):
        return False
    fits = (d.get("at") or {}).get("fittings") or []
    if fits and not any(f in allowed and (r is None or r.fitting(f)) for f in fits):
        return False
    if (d.get("animals") or {}).get("oxen") and (r is None or r.oxen < int(d["animals"]["oxen"])):
        return False
    other = [i for i in (d.get("inputs") or {}) if i not in EDIBLE]
    if r is not None and any(i not in r.goods and i != "fuel" for i in other):
        return False
    return True


def worth(good, cook, r=None, depth=3) -> tuple:
    """(food a unit, units of work a unit, other inputs a unit {good: qty}, route [techniques]) at the best route."""
    allowed = COOK_FITTINGS[cook]
    hearth = cook != "raw"
    best = (base(good, hearth), 0.0, {}, [])
    if depth <= 0 or cook == "raw":
        return best
    for t in FOOD_TECHS:
        d = TECHNIQUES[t]
        ins = d.get("inputs") or {}
        if good not in ins or not _tech_ok(t, allowed, r):
            continue
        a = float(ins[good])
        if any(i in EDIBLE and i != good for i in ins):       # a route that needs a second food (none yet) is left out
            continue
        units = float(d.get("units", 1)) / a
        others = {i: float(q) / a for i, q in ins.items() if i != good and not isinstance(q, dict)}
        for out, b in d["gives"].items():
            if out not in ITEMS or float(ITEMS[out].get("food", 0) or 0) <= 0:
                continue
            v, u, o2, route = worth(out, cook, r, depth - 1)
            k = float(b) / a
            val = k * v
            if val > best[0] + 1e-9:
                merged = dict(others)
                for i, q in o2.items():
                    merged[i] = merged.get(i, 0.0) + k * q
                best = (val, units + k * u, merged, [t] + route)
    return best


WHERE = {"open": ("open_dry", ()), "hand": ("hand", ()), "house": ("store", ()), "bins": ("store", ("bins",)),
         "cellar": ("store", ("cellar",)), "granary": ("store", ("granary",))}


def rate(good, store, season="spring", cold=False) -> float:
    """The share of a good lost a night kept this way: night.spoil_rate, the engine's own rule."""
    from cybertron2.engine import night as NI
    where, fits = WHERE[store]
    return min(1.0, NI.spoil_rate(PHYSICS, good, where, season, cold, fittings=fits))


def keeping_forms(good, cook, r=None) -> list:
    """Forms a good can be kept in until eaten: itself (eaten through its best route), and any food technique that turns it into a
    good that spoils slower (dried meat, cheese): [(form, units of form a unit, worth a unit of form, work a unit of good)]."""
    v, u, _, _ = worth(good, cook, r)
    out = [(good, 1.0, v, u)]
    if cook == "raw":
        return out
    for t in FOOD_TECHS:
        d = TECHNIQUES[t]
        ins = d.get("inputs") or {}
        if good not in ins or not _tech_ok(t, COOK_FITTINGS[cook], r):
            continue
        a = float(ins[good])
        for f, b in d["gives"].items():
            if f in ITEMS and float(ITEMS[f].get("spoil", 1)) < float(ITEMS[good].get("spoil", 1)) and float(ITEMS[f].get("food", 0)) > 0:
                vf = worth(f, cook, r)[0]
                out.append((f, float(b) / a, vf, float(d.get("units", 1)) / a))
    return out
