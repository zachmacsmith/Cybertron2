"""W-82 (worktree only, never merged): a farming livelihood bot and a building layer for the livelihood bots, to read the building
clock (D2-276, D2-281) with bots. Registered into bots_livelihood's POLICIES at its import.

  - data: KNOBS of `farm`, BUILD (the layer's defaults); nothing is written to the world;
  - verbs: only the engine's own acts (work, gather, build, move);
  - signs: none; it reads the state a person there could see (its fields and crops, its herd, its stores, its buildings);
  - processes: none; bots_livelihood.plan calls `layer` between the policy and the fallback when the setting has `build`.

The farm policy (plain rules, a fair player): every member reaps the household's ripe crop; sows its empty plots in sowing time
(grain and beans in spring and summer, rye in autumn) with up to `sow_share` of the seed it holds; weeds a growing crop up to
`weed_a_plot` units a plot; milks the cows in milk; one person herds a herd that no shut fence holds while a crop stands at the
node; hay in summer for a herd while the store holds under `hay_keep`; the harvest into the house's store.

The building layer: each household works through a fixed list of projects, in order, with the units its members have left after
the day's food work: (1) a house where it has no dwelling but a camp (a small room, then a hearth, then a bed a member);
(2) a field where it holds none at the node (clearing a meadow, pasture or scrub it may take); (3) a fence round its herd's
parcel; (4) a granary when its grain is over what its bins hold by `granary_over`; (5) a weir across the river at the node, by
the household named `weir_by` with the head of `weir_with` as crew. Timber short for a project is felled first. It builds only
while the household's store holds `reserve` nights of food (else the units go to wild food), except the house, which takes at
least `house_least` units an adult a day while the household sleeps in a camp or out. A null arm sets `build: false`.
"""
from __future__ import annotations

import math

from cybertron2.engine import bots_livelihood as BL
from cybertron2.engine.data import CROPS, FITTINGS, ITEMS, ROOMS, SEED_CROP, TECHNIQUES

BUILD = {"reserve": 4.0, "house_least": 2, "urgent": ["house", "field"], "house_structure": "wattle", "granary_over": 60.0, "field_for": None, "weir_by": None, "weir_with": None,
         "projects": ["house", "field", "fence", "granary", "weir"]}


def _hold(day):
    """The keys a household's holdings are under (the household, its members)."""
    return {day.hh, *day.members} - {None}


def _claimed_by(day, thing) -> list:
    return [c["claimant"] for c in day.w.claims_on(thing)]


# ---------------------------------------------------------------------- farming
def _fields(day) -> list:
    """[(pid, holder key, record)] of the household's own holdings on the fields here."""
    from cybertron2.engine import farm as FM
    out = []
    for pid in day.parcels(("field",)):
        par = day.w.s["parcels"][pid]
        for h in FM.own_records(day.here, pid, {}):
            rec = FM.record(par, h)
            if rec is not None and FM.plots_of(par, h) > 0:
                out.append((pid, h, rec))
    return out


def _food_in_store(day) -> float:
    """Food the household can draw on here: what this person may take from (hands, the household's stores, what lies at their
    doors) and the other members' hands."""
    cids = set(day.w.takeable(day.name, day.node)) | {day.w.hands(m) for m in day.members}
    return sum(day.w.food_value(day.w.goods(c)) for c in cids)


def _nights(day) -> float:
    """Nights of food the household's store holds."""
    need = sum(day.ration(m) for m in day.w.members(day.hh)) if day.hh else day.ration(day.name)
    return _food_in_store(day) / max(0.1, need)


def _ripens_in_time(day, fam) -> bool:
    """A farmer knows the year: a crop sown today comes in before the winter stops it (a hardy crop: before the next summer ends),
    at its season's growth (CROPS growth), within 40 days."""
    from cybertron2.engine.farm import grow_days, rate
    w = day.w
    g = grow_days(w.year_days(), fam)
    prog = 0.0
    for k in range(40):
        se = w.calendar(w.d + k)["season"]
        r = rate(fam, se)
        if r <= 0 and not CROPS[fam]["hardy"] and prog > 0:
            return False
        prog += r / g
        if prog >= 1.0:
            return True
    return False


@BL.policy("farm", sow_share=0.7, weed_a_plot=4.0, hay_keep=40.0, herd=True)
def farm(day, p) -> None:
    from cybertron2.engine import farm as FM
    w, s, here = day.w, day.s, day.here
    n = max(1, len(day.members))
    got = set()
    for act in BL._store_moves(day, day.name, {}):                         # what is in hand into the house's store, first
        p.add("a", act, 0)
    if day.role == len(day.members) - 1 or len(day.members) == 1:          # the youngest keeps the firewood up
        short = BL._firewood_need(day) - day.reach("firewood")             # what lies at the door counts (a camp keeps little)
        BL._gather_wood(day, p, 0 if short <= 0 else min(4, math.ceil(short / float(s["wood_a_unit"]))))
    # 1. the harvest: every member reaps the household's ripe crop, a share each
    for pid, h, rec in _fields(day):
        c = rec.get("crop")
        if not c or float(c.get("area_left", 0.0)) <= 1e-6 or float(c.get("progress", 0.0) or 0.0) < 1.0:
            continue
        a = {"do": "work", "what": "reap", "at": day.pname(pid)}
        if FM.ready(here, "reap", pid, {}):
            continue
        want = math.ceil(float(c["area_left"]) / float(TECHNIQUES["reap"]["yield"]["plots"]) / n) + 1
        for _ in range(want):
            if not p.add("b", dict(a), 1):
                break
        got.add(CROPS[c["crop"]]["gives"])
    # 1b. a neighbour's harvest (a fixed custom of the bots, the fixture's): with units left and no ripe crop of its own, a person
    # reaps a ripe crop on another household's holding here and gives the holder half of what the sickle brings in
    if not got and s.get("help_reap", True):
        mine = set(FM._mine(here, {}))
        for pid in day.parcels(("field",)):
            par = w.s["parcels"][pid]
            for h, rec, c in FM.standing(par):
                holder = h if h is not None else next(iter(FM.whole(par)), None)
                if holder is None or holder in mine or float(c.get("area_left", 0.0)) <= 1e-6 \
                        or float(c.get("progress", 0.0) or 0.0) < 1.0:
                    continue
                k = min(p.left() - 2, math.ceil(float(c["area_left"]) / float(TECHNIQUES["reap"]["yield"]["plots"])))
                if k <= 0:
                    continue
                on = {"do": "work", "what": "reap", "at": day.pname(pid), "on": w.s["institutions"].get(holder, {}).get("name", holder)}
                n_ = sum(1 for _ in range(k) if p.add("b", dict(on), 1))
                each = float(c["left"]) / max(1e-9, float(c["area_left"])) * float(TECHNIQUES["reap"]["yield"]["plots"])
                give = round(0.5 * each * n_, 1)
                gives = CROPS[c["crop"]]["gives"]
                if give > 0.5 and holder in w.s["institutions"]:
                    p.add("b", {"do": "give", "to": w.s["institutions"][holder]["name"], "item": gives, "qty": give})
                got.add(gives)
                break
            if got:
                break
    # 2. sowing time
    season = day.season
    sow = {"spring": ("grain", "beans"), "summer": ("grain", "beans"), "autumn": ("rye", "grain")}.get(season, ())
    if day.role == 0:
        for pid, h, rec in _fields(day):
            c = rec.get("crop")
            if c and (float(c.get("area_left", 0.0)) > 1e-6):
                continue
            for seed in sow:
                if not _ripens_in_time(day, SEED_CROP[seed]):
                    continue
                # keep enough to eat until the harvest: the household's rations for the crop's growing days and the reaping
                fam = SEED_CROP[seed]
                from cybertron2.engine.farm import grow_days
                need = sum(day.ration(m) for m in w.members(day.hh)) * (grow_days(w.year_days(), fam) + 3)
                spare = max(0.0, _food_in_store(day) - need) / float(ITEMS[seed]["food"])
                have = min(day.reach(seed) * float(s["sow_share"]), spare)
                room = FM.plots_of(w.s["parcels"][pid], h) * float(w.p["farming"]["plot_seed"])
                q = min(have, room)
                if q < 4:
                    continue
                if FM.ready(here, "sow", pid, {"item": seed}):
                    continue
                for _ in range(math.ceil(q / float(TECHNIQUES["sow"]["yield"]["seed"]))):
                    if not p.add("b", {"do": "work", "what": "sow", "item": seed, "at": day.pname(pid)}, 1):
                        break
                break
    # 3. weeding a growing crop
    for pid, h, rec in _fields(day):
        c = rec.get("crop")
        if not c or float(c.get("progress", 0.0) or 0.0) >= 1.0 or float(c.get("area_left", 0.0)) <= 1e-6:
            continue
        if float(c.get("weeded", 0.0)) / max(1e-9, float(c["area"])) >= float(s["weed_a_plot"]):
            continue
        if FM.ready(here, "weed", pid, {}):
            continue
        for _ in range(2):
            p.add("b", {"do": "work", "what": "weed", "at": day.pname(pid)}, 1)
    # 4. the herd
    herds = [(hid, hd) for hid, hd in here.herds().items() if any(x in _hold(day) for x in _claimed_by(day, ("herd", hid)))
             or hd.get("holder") in _hold(day)]
    for hid, hd in herds:
        pid = hd["parcel"]
        milker = next((m for m in day.members if day.knows("milk", m)), None)
        if milker == day.name and not FM.ready(here, "milk", pid, {}):
            k = math.ceil(float(hd.get("in_milk", 0.0)) / float(TECHNIQUES["milk"]["yield"]["cows"]) / n)
            for _ in range(max(1, k)):
                p.add("b", {"do": "work", "what": "milk", "at": day.pname(pid)}, 1)
        from cybertron2.engine import herds as HD
        crops = any(FM.standing(w.s["parcels"][q]) for q in day.parcels(("field",)))
        if s["herd"] and crops and HD.through(w, pid) > 0.5 and day.role == len(day.members) - 1 and not FM.ready(here, "herd", pid, {}):
            p.add("b", {"do": "work", "what": "herd", "at": day.pname(pid)}, 1)
        if season == "summer" and day.role == 0 and float(day.store().get("hay", 0.0)) < float(s["hay_keep"]):
            past = [q for q in day.parcels(("pasture", "meadow")) if any(x in _hold(day) for x in _claimed_by(day, ("parcel", q)))]
            if past:
                for _ in range(2):
                    p.add("b", {"do": "gather", "what": "hay", "at": day.pname(past[0])}, 1)
    if day.home_b and got:
        for item in sorted(got):
            p.add("b", {"do": "move", "item": item, "qty": 9999, "to": "store", "at": day.bname(day.home)})


# ---------------------------------------------------------------------- the building layer
def _house(day):
    """The household's finished house here (a building with rooms that is not a camp nor a smokehouse), or None; dwellings first."""
    from cybertron2.engine import keeping as KP
    for b in day.w.homes(day.name):
        x = day.w.s["buildings"][b]
        if x["structure"] != "camp" and x["node"] == day.node and not x.get("monument") and not KP.is_smokehouse(x) \
                and x.get("rooms"):
            return b
    return None


def _own_unfinished(day, kind=None):
    for bid, b in sorted(day.here.buildings().items()):
        if b.get("unfinished") and any(x in _hold(day) for x in _claimed_by(day, ("building", bid))):
            if kind is None or (b["unfinished"].get("blueprint") == kind):
                return bid
    return None


def _fell(day, p, need, left) -> int:
    """Timber felled toward `need` (an act of 2 units gives 3 with a crude tool); returns the units planned."""
    short = need - day.reach("timber")
    if short <= 1e-6:
        return 0
    ps = [pid for pid in day.parcels(("forest",)) if float((day.w.s["parcels"][pid]["res"].get("wood") or {}).get("S", 0)) > 3]
    if not ps:
        return 0
    pid = max(ps, key=lambda q: (float(day.w.s["parcels"][q]["res"]["wood"]["S"]), q))
    tool = day.here.carried().get("crude tool", 0.0) >= 1 or day.here.carried().get("copper tool", 0.0) >= 1
    per = 3.0 * (1.0 if tool else 0.25)
    used = 0
    while short > 1e-6 and used + 2 <= left:
        if not p.add("b", {"do": "gather", "what": "fell", "at": day.pname(pid)}, 2):
            break
        used += 2
        short -= per
    return used


def _build_acts(day, p, act, left, cost=2, most=None) -> int:
    """Build acts up to `left` units (and `most` acts: no more than the work left, so a finished work is not built on again)."""
    used, n = 0, 0
    if most is None:
        most = _acts_left(day, act)
    while used + cost <= left and n < most:
        n += 1
        if not p.add("b", dict(act), cost):
            break
        used += cost
    return used


def _ground_parcel(day, floor):
    """Where to put up a house: the parcel of the household's camp, else built ground or scrub here with room."""
    from cybertron2.engine import buildings as BLD
    camp = next((day.w.s["buildings"][b]["parcel"] for b in day.w.dwellings(day.name)
                 if day.w.s["buildings"][b]["structure"] == "camp"), None)
    cands = ([camp] if camp else []) + day.parcels(("built", "scrub"))
    for pid in cands:
        par = day.w.s["parcels"][pid]
        if BLD.ground_total(par) > 0 and BLD.ground_free(pid, par, day.w.s["buildings"]) >= floor:
            return pid
    return None


def _p_house(day, p, left) -> tuple:
    """(units planned, done?) for the house: a small room, then a hearth, then beds."""
    st = day.s["house_structure"]
    house = _house(day)
    if house is None:
        ub = _own_unfinished(day, "small room")
        if ub:
            return _build_acts(day, p, {"do": "build", "what": "small room", "at": day.bname(ub)}, left), False
        if day.role != 0:
            return 0, False                               # the head starts it (the materials go in at the start)
        need = ROOMS["small room"][st]["materials"].get("timber", 0)
        used = _fell(day, p, need, left)
        if day.reach("timber") + 1e-6 < need:
            return used, False
        pid = _ground_parcel(day, int(ROOMS["small room"]["floor"]))
        if pid is None:
            return used, False
        a = {"do": "build", "what": "small room", "structure": st, "at": day.pname(pid), "name": f"{day.hh} House"}
        return used + _build_acts(day, p, a, left - used), False
    b = day.w.s["buildings"][house]
    under = b.get("fitting_work") or {}
    for what in ("hearth", "beds"):
        if what in under:
            return _build_acts(day, p, {"do": "build", "what": what, "at": b["name"]}, left), False
    fit = b.get("fittings") or {}
    if not fit.get("hearth") and day.knows("hearth"):
        if day.reach("stone") >= FITTINGS["hearth"]["materials"]["stone"] and day.role == 0:
            return _build_acts(day, p, {"do": "build", "what": "hearth", "at": b["name"]}, left), False
    beds = int(fit.get("beds", 0))
    want = len(day.w.members(day.hh)) if day.hh else 1
    if beds < want and day.role == 0:
        k = min(want - beds, int(day.reach("timber") // 1), int(day.reach("straw") // 2))
        if k <= 0:
            used = _fell(day, p, want - beds, left)
            return used, False
        return _build_acts(day, p, {"do": "build", "what": "beds", "qty": k, "at": b["name"]}, left), False
    return 0, beds >= want


def _p_field(day, p, left) -> tuple:
    if day.s.get("field_for") is not None and day.hh not in day.s["field_for"]:
        return 0, True
    if _fields(day) and not any(day.w.s["parcels"][q].get("clearing") for q in day.parcels(("meadow", "pasture", "scrub"))):
        return 0, True
    for pid in day.parcels(("meadow", "pasture", "scrub")):
        par = day.w.s["parcels"][pid]
        cl = _claimed_by(day, ("parcel", pid))
        if cl and not any(x in _hold(day) for x in cl):
            continue
        if any(b["parcel"] == pid for b in day.w.s["buildings"].values()):
            continue                                       # the knoll with the houses on it is not ploughed up
        if any(hd["parcel"] == pid for hd in day.here.herds().values()):
            continue
        return sum(1 for _ in range(left) if p.add("b", {"do": "work", "what": "clear", "at": day.pname(pid)}, 1)), False
    return 0, True


def _p_fence(day, p, left) -> tuple:
    from cybertron2.engine import farm as FM
    herds = [hd for hid, hd in day.here.herds().items() if any(x in _hold(day) for x in _claimed_by(day, ("herd", hid)))
             or hd.get("holder") in _hold(day)]
    if not herds:
        return 0, True
    own = [q for q in day.parcels(("pasture",)) if any(x in _hold(day) for x in _claimed_by(day, ("parcel", q)))]
    pid = own[0] if own else herds[0]["parcel"]
    fc = day.w.s["parcels"][pid].get("fence") or {}
    if fc.get("built") and int(fc.get("level", 0)) >= 2:
        return 0, True
    need = FM.fence_need(day.w.s["parcels"][pid], "wood")
    done = float(fc.get("units", 0.0)) / max(1e-9, need["units"])
    timber = need["inputs"]["timber"] * max(0.0, 1.0 - done)
    a_unit = need["inputs"]["timber"] / need["units"]
    used = 0
    if day.reach("timber") < a_unit * 2:
        used = _fell(day, p, min(timber, a_unit * left + 1), left)
    k = int(min(left - used, day.reach("timber") / max(1e-9, a_unit)))
    return used + sum(1 for _ in range(k) if p.add("b", {"do": "work", "what": "fence", "at": day.pname(pid)}, 1)), False


def _p_granary(day, p, left) -> tuple:
    house = _house(day)
    if house is None:
        return 0, False
    b = day.w.s["buildings"][house]
    if (b.get("fittings") or {}).get("granary"):
        return 0, True
    under = b.get("fitting_work") or {}
    if "granary" in under:
        return _build_acts(day, p, {"do": "build", "what": "granary", "at": b["name"]}, left), False
    grain = sum(float(day.store().get(i, 0.0)) for i in ("grain", "rye", "beans"))
    bins = 60.0 * int((b.get("fittings") or {}).get("bins", 0))
    if grain < bins + float(day.s["granary_over"]):
        return 0, True
    from cybertron2.engine import buildings as BLD
    if BLD.free_floor(b, day.w.goods(b["stock"])) < int(FITTINGS["granary"]["spaces"]):   # no floor: a room added first
        wk = b.get("works") or {}
        if wk.get("kind") == "room":
            return _build_acts(day, p, {"do": "build", "what": wk.get("room", "small room"), "at": b["name"]}, left), False
        if day.role != 0:
            return 0, False
        from cybertron2.engine.buildings import room_cost
        need = room_cost("small room", b["structure"], added=True).get("materials", {})
        used = _fell(day, p, need.get("timber", 0), left)
        if day.reach("timber") + 1e-6 < need.get("timber", 0) or day.reach("stone") + 1e-6 < need.get("stone", 0):
            return used, False
        return used + _build_acts(day, p, {"do": "build", "what": "small room", "at": b["name"]}, left - used), False
    if day.role != 0:
        return 0, False
    need = FITTINGS["granary"]["materials"]["timber"]
    used = _fell(day, p, need, left)
    if day.reach("timber") + 1e-6 < need:
        return used, False
    return used + _build_acts(day, p, {"do": "build", "what": "granary", "at": b["name"]}, left - used), False


def _p_weir(day, p, left) -> tuple:
    from cybertron2.engine import wild as WL
    by, crew = day.s.get("weir_by"), day.s.get("weir_with")
    if not by or day.hh not in (by, crew):
        return 0, True
    weirs = sorted(bid for bid, b in day.here.buildings().items() if b.get("monument") == "weir")
    done = [bid for bid in weirs if not day.w.s["buildings"][bid].get("unfinished")]
    if done:
        return 0, True
    if weirs:
        return _build_acts(day, p, {"do": "build", "what": "weir", "at": day.bname(weirs[0])}, left), False
    if day.hh != by or day.role != 0:
        return 0, False
    from cybertron2.engine.data import MONUMENTS
    need = MONUMENTS["weir"]["materials"]["timber"]
    used = _fell(day, p, need, left)
    if day.reach("timber") + 1e-6 < need:
        return used, False
    river = BL.river_parcels(day)
    mate = day.w.head(crew) if crew in day.w.s["institutions"] else None
    if not river or not mate or day.w.at(mate) != day.node:
        return used, False
    a = {"do": "build", "what": "weir", "at": day.pname(river[0]), "with": [mate]}
    return used + _build_acts(day, p, a, left - used), False


def _done(day, name) -> bool:
    if name == "house":
        h = _house(day)
        want = len(day.w.members(day.hh)) if day.hh else 1
        return h is not None and int((day.w.s["buildings"][h].get("fittings") or {}).get("beds", 0)) >= want
    if name == "field":
        return bool(_fields(day))
    return False


def _acts_left(day, act) -> int:
    """Acts of 2 units (x skill 1) that the work an act carries on still needs, shared among the household's adults; 99 for a start."""
    at = act.get("at")
    bid = next((b for b, x in day.here.buildings().items() if x["name"] == at), None)
    if bid is None:
        return 99
    b = day.here.buildings()[bid]
    what = act.get("what")
    if b.get("unfinished"):
        left = float(b["unfinished"]["units_left"])
    elif what in (b.get("fitting_work") or {}):
        left = float(b["fitting_work"][what]["units_left"])
    elif (b.get("works") or {}).get("kind") == "room" and what in ROOMS:
        left = float(b["works"].get("units_left", 0.0))
    else:
        return 99
    k = max(1, len([m for m in day.members if day.w.s["people"][m]["stage"] in ("adult", "youth")]))
    return max(1, math.ceil(left / 2.0 / k))


def _p_weir_sections(day, p, left) -> tuple:
    """Further wattle sections on the household's finished weir, up to its most (D2-210), by the weir's builders."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import gear as GR
    by, crew = day.s.get("weir_by"), day.s.get("weir_with")
    if not by or day.hh not in (by, crew):
        return 0, True
    weirs = sorted(bid for bid, b in day.here.buildings().items() if b.get("monument") == "weir" and not b.get("unfinished"))
    if not weirs:
        return 0, False
    b = day.w.s["buildings"][weirs[0]]
    if b.get("weir_work"):
        return _build_acts(day, p, {"do": "build", "what": "weir section", "structure": "wattle", "at": b["name"]}, left,
                           most=max(1, math.ceil(float(b["weir_work"].get("units_left", 2.0)) / 2.0 / 2))), False
    if len(WL.sections(b)) - 1 >= GR.most_added():
        return 0, True
    if day.hh != by or day.role != 0:
        return 0, False
    need = GR.cost(len(WL.sections(b)), "wattle")["materials"].get("timber", 0)
    used = _fell(day, p, need, left)
    if day.reach("timber") + 1e-6 < need:
        return used, False
    return used + _build_acts(day, p, {"do": "build", "what": "weir section", "structure": "wattle", "at": b["name"]}, left - used,
                              most=1), False


PROJECTS = {"weir sections": _p_weir_sections, "house": _p_house, "field": _p_field, "fence": _p_fence, "granary": _p_granary, "weir": _p_weir}


def layer(day, p) -> None:
    """The household's projects, in order, with the units left after the day's food work (see the module's docstring)."""
    s = {**BUILD, **day.s}
    day.s = s
    if not s.get("build") or day.w.s["people"][day.name]["stage"] not in ("adult", "youth"):
        return
    if day.home_b:                                                        # building stuff in hand into the house's store, so the
        for item in ("timber", "stone", "straw"):                         # one who starts a work can draw on it
            if day.here.carried().get(item, 0.0) > 1e-6:
                p.a.insert(0, {"do": "move", "item": item, "qty": 9999, "to": "store", "at": day.bname(day.home)})
    fed = _nights(day) >= float(s["reserve"])
    urgent = [x for x in s["projects"] if x in s["urgent"] and not _done(day, x)]
    if not fed and not urgent:
        return
    budget = p.left() if fed else min(p.left(), int(s["house_least"]))     # unfed: only the founding works, at their least
    start = p.cost
    for name in (s["projects"] if fed else urgent):
        left = budget - (p.cost - start)
        if left <= 0:
            break
        PROJECTS[name](day, p, left)
    if day.home_b and day.here.carried().get("timber", 0.0) >= 1:         # felled timber left over into the store
        p.add("b", {"do": "move", "item": "timber", "qty": 9999, "to": "store", "at": day.bname(day.home)})
