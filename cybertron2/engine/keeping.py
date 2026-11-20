"""Keeping a glut and salt inland (build brief 5 §4a, §4b; proposals/river_and_water.md; D2-209).

The smokehouse: a building of its own (no beds or hearth in it) with smoke racks. `smoke fish` or `smoke meat` hangs a batch of up to
40 on its racks (a rack thing inside it, as a hearth's rack: brief 4c §6.2), for 3 nights of fire. The fire is tended once a day (a
unit, at the place; loading a batch lights it): a fire tended today burns tonight, taking about 1 firewood from the smokehouse's store
or the woodpile at its door; a night it does not burn, the batch pauses (no night counted) and spoils at the open rate. While it
burns, a keyed chance a night by the building's structure that it catches; the fire then takes the smokehouse and may spread to the
other buildings on its parcel. A batch done goes into the smokehouse's store if the one who hung it is of the household that holds
it; anyone else's waits on the racks for them. Its household sees its state without a roll (brief 4c §6.4).

Racks hold one batch a fitting at a time (a hearth's or a fire ring's 8, the smoke racks' 40): FITTINGS `racks`.

The brine spring: a `brine` stock on a parcel (endless). A brine pan is fitted only in a building at or beside one; `boil salt` is
done at it (TECHNIQUES `spring` via the fitting).
"""
from __future__ import annotations

from cybertron2.engine.data import FITTINGS, ITEMS, PHYSICS, TECHNIQUES


# ---------------------------------------------------------------------- racks
def active_racks(w, bid) -> dict:
    """The racks hanging in or at a building whose batch is not yet done: {thing id: thing}."""
    return {cid: c for cid, c in w.s["containers"].items() if c.get("kind") == "pile" and c.get("rack") and not c.get("hidden")
            and not c["rack"].get("done") and (c.get("in") == bid or c.get("door") == bid)}


def curing(c) -> float:
    """What hangs on a rack still curing (meat drying, fish or meat in the smoke)."""
    return sum(float(q) for i, q in c["goods"].items() if q > 1e-9 and ITEMS.get(i, {}).get("decay") == "drying meat")


def cured(c) -> str:
    """What cures on a rack, as people say it: 'fish', 'meat'."""
    return " and ".join(sorted({i.replace("smoking ", "").replace("drying ", "") for i, v in c["goods"].items() if v > 1e-9
                                and ITEMS.get(i, {}).get("decay") == "drying meat"})) or "nothing"


def room(w, bid, tech) -> float:
    """Room on a building's racks for a technique's batch: a batch a fitting (FITTINGS `racks`), less what hangs there now."""
    t = TECHNIQUES[tech]
    b = w.s["buildings"][bid]
    fits = (t.get("at") or {}).get("fittings") or []
    n = sum(int(FITTINGS[f].get("racks", 0)) * int((b.get("fittings") or {}).get(f) or 0) for f in fits)
    batch = sum(float(q) for q in (t.get("gives") or {}).values())
    used = sum(curing(c) for c in active_racks(w, bid).values())
    return max(0.0, n * batch - used)


def full_words(w, bid, tech) -> str:
    """Why a building's racks take no more: '' if they have room."""
    b = w.s["buildings"][bid]
    if room(w, bid, tech) > 1e-6:
        return ""
    rs = list(active_racks(w, bid).values())
    if not rs:
        return ""
    q = sum(curing(c) for c in rs)
    left = min(nights_left(w, c, w.d) for c in rs)
    what = "smoke racks" if is_smokehouse(b) else "rack at its fire"
    return (f"the {what} in {b['name']} {'are' if what.endswith('s') else 'is'} full ({_n(q)} hanging, {left} night{'s' if left != 1 else ''} "
            "left): another batch goes up when this one is done")


def nights_left(w, c, day) -> int:
    rk = c["rack"]
    if rk.get("smokehouse"):
        return max(1, int(rk["nights"]) - int(rk.get("lit", 0)))
    return max(1, int(rk["day"]) + int(rk["nights"]) - day)


def nights_done(w, rk) -> int:
    """Nights a batch has had: a smokehouse's by its fire, a hearth's by the calendar."""
    return int(rk.get("lit", 0)) if rk.get("smokehouse") else w.d - int(rk["day"]) + 1


def _n(q) -> str:
    from cybertron2.engine.world import show
    return show(round(float(q), 1))


# ---------------------------------------------------------------------- the smokehouse
def is_smokehouse(b) -> bool:
    return bool((b.get("fittings") or {}).get("smoke racks"))


def fuel_cids(w, bid) -> list:
    """Where a smokehouse's fire takes its wood: its store, then the woodpile at its door (as a hearth's, D4-89)."""
    b = w.s["buildings"][bid]
    return [b["stock"]] + [cid for cid, c in w.s["containers"].items() if c.get("kind") == "pile" and c.get("door") == bid
                           and not c.get("hidden") and not c.get("rack")]


def fuel_nights(w, bid) -> int:
    from cybertron2.engine import forests as FO
    heat = sum(FO.heat_of(w.goods(cid)) for cid in fuel_cids(w, bid))
    return int(heat / float(PHYSICS["smokehouse"]["fuel"]) + 1e-9)


def light(here, bid) -> None:
    """Loading a batch or tending the fire: it will burn tonight."""
    b = here.buildings()[bid]
    here.apply("set", ref=("building", bid), field="smoke", value={**(b.get("smoke") or {}), "tended": here.day, "by": here.name})


def tend(here, bid, place_name) -> str:
    """`tend the smoke`: the fire fed and banked for the night (brief 5 §4a.3). One who carries fuel and finds too little there for
    tonight puts a night's worth in."""
    from cybertron2.engine import forests as FO
    from cybertron2.engine.world import Refused
    w = here._w
    b = here.buildings()[bid]
    rs = active_racks(w, bid)
    if not rs:
        raise Refused(f"nothing is hanging in the smoke in {b['name']}: hang a batch first (make smoke fish, or smoke meat)")
    if (b.get("smoke") or {}).get("tended") == here.day:
        raise Refused(f"the fire in {b['name']} is already tended for tonight")
    need = float(PHYSICS["smokehouse"]["fuel"])
    fed = ""
    if fuel_nights(w, bid) < 1:
        for item in FO.fuel_order():
            have = float(here.carried().get(item, 0.0))
            q = round(min(have, need / float(ITEMS[item]["heat"])), 4)
            if q > 1e-9 and FO.heat_of({item: q}) + 1e-9 >= need:
                here.apply("transfer", src=here.hands, dst=b["stock"], item=item, qty=q)
                fed = f"; you put {_n(q)} {item} from your hands on it"
                break
    light(here, bid)
    q = sum(curing(c) for c in rs.values())
    what = " and ".join(sorted({cured(c) for c in rs.values()}))
    left = min(nights_left(w, c, here.day) for c in rs.values())
    n = fuel_nights(w, bid)
    fuel = (f"firewood there for {n} night{'s' if n != 1 else ''}" if n else
            "but there is no firewood in it or at its door for tonight: the fire will die unless some is brought")
    return (f"You tended the fire in {b['name']} and banked it for the night{fed}: {_n(q)} {what} curing, {left} night{'s' if left != 1 else ''} "
            f"left; {fuel}.")


def house_lines(here, bid) -> list:
    """A smokehouse's state for its household, known without a roll (brief 4c §6.4, brief 5 §4a.5): what cures and how many nights
    are left, its fire today and its fuel, and a night the fire died. Lines in lower case, without a full stop."""
    w = here._w
    b = here.buildings()[bid]
    rs = active_racks(w, bid)
    out = []
    for cid, c in sorted(rs.items()):
        q = curing(c)
        if q <= 1e-6:
            continue
        what = cured(c)
        left = nights_left(w, c, here.day)
        mine = c.get("by") in w.s["people"] and bid in w.homes(c["by"])
        out.append(f"on the smoke racks: {_n(q)} {what} curing, {left} night{'s' if left != 1 else ''} left"
                   + ("" if mine or not c.get("by") else f" (hung by {c['by']})"))
    sm = b.get("smoke") or {}
    if sm.get("night") == here.day - 1 and not sm.get("lit") and sm.get("had"):
        out.append("the fire died last night: the batch lost a night's smoke, and spoiled a little in the open air")
    if rs:
        if sm.get("tended") == here.day:
            out.append("the fire tended today")
        else:
            out.append("the fire not tended today: it dies tonight unless someone tends it")
        n = fuel_nights(w, bid)
        out.append("no firewood in it or at its door: the fire cannot burn tonight" if n == 0 else
                   "the fire low: firewood for 1 night" if n == 1 else f"firewood for {n} nights")
    return out


def night(w, rec) -> None:
    """Each smokehouse's fire tonight, before the night's spoiling: tended today and fuelled, it burns (each batch on its racks has a
    night of smoke, and a keyed chance it catches); else it dies (the batch pauses and spoils at the open rate)."""
    from cybertron2.engine import forests as FO
    P = PHYSICS["smokehouse"]
    for bid, b in sorted(w.s["buildings"].items()):
        if not is_smokehouse(b) or b.get("unfinished"):
            continue
        rs = {cid: c for cid, c in active_racks(w, bid).items() if c["rack"].get("smokehouse") and curing(c) > 1e-9}
        if not rs:
            continue
        sm = dict(b.get("smoke") or {})
        node = b["node"]
        lit = sm.get("tended") == w.d and any(FO.burn(w, node, cid, float(P["fuel"]), why="smoke fire") for cid in fuel_cids(w, bid))
        w.apply("set", node, ref=("building", bid), field="smoke", value={**sm, "night": w.d, "lit": bool(lit), "had": True})
        for cid, c in rs.items():
            rk = dict(c["rack"])
            if lit:
                rk["lit"] = int(rk.get("lit", 0)) + 1
            else:
                rk["out"] = w.d
            w.apply("set_thing", node, cid=cid, field="rack", value=rk)
        rec.setdefault("smokehouse", {})[bid] = {"lit": bool(lit), "batches": len(rs)}
        if lit and w.rng("smokehouse fire", w.d, bid).random() < float(P["fire"].get(b["structure"], P["fire"]["wattle"])):
            rec.setdefault("smokehouse_fires", []).append(catch(w, bid))


def catch(w, bid) -> dict:
    """A smokehouse's fire catches in the night (brief 5 §4a.1): it burns, its batch with it, and each other building on its parcel
    catches by its structure's `spread` chance."""
    P = PHYSICS["smokehouse"]
    b = w.s["buildings"][bid]
    burnt = [bid]
    for oid, o in sorted(w.s["buildings"].items()):
        if oid != bid and o["node"] == b["node"] and o["parcel"] == b["parcel"] and not o.get("unfinished") and not o.get("monument"):
            if w.rng("smokehouse spread", w.d, bid, oid).random() < float(P["spread"].get(o["structure"], P["spread"]["wattle"])):
                burnt.append(oid)
    for x in burnt:
        burn_building(w, b["node"], x, float(P["food"]), float(P["other"]), 1, w.d + 1, racks=True)
    return {"smokehouse": bid, "burnt": burnt}


def burn_building(w, node, bid, food, other, damage, day, racks=False) -> None:
    """A fire in a building (run.py's fire incident, and a smokehouse's): its store burnt but for its vault (D2-49), its condition or
    level down, the record for its signs (D4-74), the event; with `racks`, what hangs inside it too."""
    from cybertron2.engine import buildings as BL
    from cybertron2.engine.data import EDIBLE
    b = w.s["buildings"][bid]
    safe = BL.vaulted(b, w.goods(b["stock"]))
    for item, q in list(w.goods(b["stock"]).items()):
        share = food if item in EDIBLE else other
        w.apply("destroy", node, src=b["stock"], item=item, qty=max(0.0, q - safe.get(item, 0.0)) * share, why="fire")
    if racks:
        for cid, c in sorted(w.s["containers"].items()):
            if c.get("kind") == "pile" and c.get("in") == bid:
                for item, q in list(c["goods"].items()):
                    if q > 1e-9:
                        w.apply("destroy", node, src=cid, item=item, qty=q * (food if item in EDIBLE else other), why="fire")
                if c.get("rack") and not c["rack"].get("done"):
                    w.apply("set_thing", node, cid=cid, field="rack", value={**c["rack"], "out": w.d})
    if b.get("level") is not None:                                         # in levels: a fire takes it to holed or worse (brief 4 §3)
        BL.set_level(w, node, bid, min(BL.level(b), 2) - (int(damage) - 1))
    else:
        w.apply("set", node, ref=("building", bid), field="condition", value=max(0, b["condition"] - int(damage)))
    w.apply("set", node, ref=("building", bid), field="fire_hit", value={"day": day})   # for its signs (D4-74)
    live = [m for m in w.living() if bid in w.homes(m)]
    w.event(node, "fire", f"fire broke out in {b['name']} in the night: the store is burnt, most of its food is gone and the roof "
            "is damaged", about=[f"building:{bid}"], salience=0.95, tags=["danger", "food", "shelter"], concerns=live, dawn=True)


def done_into_store(w, c, bid) -> bool:
    """A batch done goes into the store of the building it hangs in: a hearth's always (brief 4c §6.3); a smokehouse's only when the
    one who hung it is of the household that holds it (anyone else's waits on the racks for them)."""
    if not (c.get("rack") or {}).get("smokehouse"):
        return True
    return bid in w.homes(c.get("by") or "") if c.get("by") in w.s["people"] else False


# ---------------------------------------------------------------------- the brine spring
def near_spring(w, pid, kind="brine") -> bool:
    """A spring of `kind` on a parcel or one beside it (brief 5 §4b.2)."""
    ps = w.s["parcels"]
    return any(x in ps and kind in (ps[x].get("res") or {}) and float(ps[x]["res"][kind].get("S", 0.0)) > 1e-9
               for x in [pid] + list(ps[pid].get("adj") or []))
