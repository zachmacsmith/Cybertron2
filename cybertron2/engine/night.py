"""The night (spec/core/round.md): fights, departures, where each sleeps, fires, eating, the cold, deaths, spoilage, breaks, growth
and crops, offers lapsing. Each node on its own (D4-35); travellers on the road sleep out and eat what they carry (D4-12).

Where one sleeps: where one chose to (`sleep`), if one can get in and a bed is free; else one's home here (D4-36); else a building
one has been given access to (a host: 05 §3), if a bed is free; else out. What one eats: what one carries, then the stores here one
may take from, the one slept in first (38.17 §9: to confirm).
"""
from __future__ import annotations

from cybertron2.engine import life as LF, needs as NE
from cybertron2.engine.data import DECAY, EDIBLE, FITTINGS, ITEMS, THINGS

FIRE = tuple(f for f, d in FITTINGS.items() if d.get("fire"))
from cybertron2.engine.world import Refused, show_fine

GOING_OFF = ("fish", "dried fish", "salt fish")   # store goods whose going off is smelt the morning after (signs pass, 17 Nov)
GOING_OFF_LEAST = 0.2                                # at least this much lost in the night to be smelt (calibrate)


def night(w) -> dict:
    s, p = w.s, w.p
    today = s.get("today") or {}
    cold = any(w.cold(nid) for nid in sorted(s["nodes"]))                      # the record's flag: a cold night somewhere (D4-111)
    rec = {"day": w.d, "book": dict(today.get("book") or {}), "cold": cold, "ate": {}, "short": [], "missed": [], "deaths": [], "cold_falls": [], "breaks": [], "hearth": {},
           "spoiled": {}, "fights": [], "departed": [], "slept": {}}
    from cybertron2.engine import climate as CL
    if CL.on(w):                                                                # the day's weather at each node: the truth (D4-109)
        rec["weather"] = {nid: {**{k: v for k, v in CL.env(w, nid, w.d).items() if k in ("temp", "low", "rain", "wind", "type", "era")},
                                "label": CL.label(w, nid, w.d)} for nid in sorted(w.s["nodes"])}
    from cybertron2.engine import settle as ST
    rec["fights"] = ST.settle_fights(w, today)
    rec["deaths"] += [f["killed"] for f in rec["fights"] if f.get("killed")]
    rec["deaths"] += [x["target"] for f in rec["fights"] for x in f.get("fights") or [] if x.get("outcome") == "killed"]   # D4-101
    rec["departed"] = today["_departed"] if "_departed" in today else departures(w, today)
    where = sleeping_places(w, today)
    floor_ = set(today.get("_floor") or [])                                     # in a house without a bed: on its floor (D2-165)
    rec["slept"] = {n: (s["buildings"][b]["name"] if b else "out") for n, b in where.items()}
    if floor_:
        rec["floor"] = sorted(floor_)
    from cybertron2.engine import buildings as BL
    levelled = BL.levels_on(w)                                                 # shelter in levels (brief 4 §3)
    for n, b in sorted(where.items()):                                          # those inside read what is written there (D2-169)
        if b:
            BL.read(w, n, b, "slept")
    for n, b in where.items():                                                  # who slept in the open, for its signs (D4-74)
        if b is None and s["people"][n]["at"] is not None:
            w.apply("set", s["people"][n]["at"], ref=("person", n), field="slept_out", value={"day": w.d, "cold": w.cold(s["people"][n]["at"])})
    from cybertron2.engine import forests as FO
    hp = p["heat"]
    for bid, b in s["buildings"].items():                                     # fires in heat (D2-157, D2-159)
        sleepers = [n for n, x in where.items() if x == bid]
        lit, warm = False, 0.0
        if sleepers and any(b["fittings"].get(f_) for f_ in FIRE):
            hearths, rings = int(b["fittings"].get("hearth") or 0), int(b["fittings"].get("fire ring") or 0)
            if b["structure"] == "camp":                                      # a camp's fire (D4-49), in the weather (D4-83)
                heat = float(hp["camp"]) * weather_fuel(w, b["node"]) * (float(p["wear"]["camp_fire"]) if levelled else 1.0)
            else:
                heat = house_heat(p, b, w.cold(b["node"]))               # one room, one fire (D4-93); the node's night (D4-109)
            piles = [cid for cid, c in s["containers"].items() if c.get("kind") == "pile" and c.get("door") == bid and not c.get("hidden")]
            if any(FO.burn(w, b["node"], cid, heat) for cid in [b["stock"]] + piles):   # its store, then its woodpile at the door (D4-89)
                lit = True
                if b["structure"] == "camp" and fire_goes_out(w, ("camp", bid), rings > 0, b["node"]):
                    rec.setdefault("fire_out", []).extend(sleepers)              # cooked on, but cold by morning (D4-83)
                    w.apply("set", b["node"], ref=("building", bid), field="fire_out", value=w.d)
                spaces = float(hp["hearth_spaces"]) * hearths + float(hp["ring_spaces"]) * rings
                warm = 1.0 if b["structure"] == "camp" else min(1.0, spaces / max(1.0, float(BL.floor(b) or 1)))   # spaces of floor
                if not hearths and b["structure"] != "camp":
                    warm = min(warm, 0.5)                                     # a fire ring half-warms a house in the cold
        if lit and b.get("fire_out") == w.d:
            warm = 0.0
        if sleepers and not lit and any(b["fittings"].get(f_) for f_ in FIRE):
            rec.setdefault("fire_need", {})[bid] = heat                       # what the fire wanted, for the night line (D4-93)
        w.apply("set", b["node"], ref=("building", bid), field="fire", value=lit)
        w.apply("set", b["node"], ref=("building", bid), field="warm", value=warm)
        if sleepers:
            rec["hearth"][bid] = {"sleepers": len(sleepers), "lit": lit, "warm": round(warm, 2)}
    from cybertron2.engine import process as PROC
    PROC.night(w, rec)                                                          # the containers' conditions: fires tended, fuelled,
                                                                                # caught; hearths lit; water without a spate (u4 §5)
    fires = open_fires(w, today, where, rec)                                  # fires in the open, shared by 4 (D2-159)
    rec["care"] = LF.care_gifts(w, today)                                       # the largest care's food, and what is passed on (D4-64)
    tents = {}                                                                  # a tent sleeps two (D2-68): who shares whose
    from cybertron2.engine import book as BK
    shares = even_shares(w, where)                                              # short and no share rule: an even split (W-111)
    for name in BK.meal_order(w, w.living()):                                   # a share's order: fed first when short (D2-339)
        a = s["people"][name]
        bid = where.get(name)
        b = s["buildings"][bid] if bid else None
        cold = w.cold(b["node"] if b is not None else w.place_of(("person", name)))         # the night where one sleeps (D4-109)
        state = "unsheltered" if b is None or b["condition"] == 0 else ("damaged" if b["condition"] == 1 else "housed")
        if b is not None and levelled and b.get("structure") != "camp":       # in levels: worn and gappy cost warmth too (brief 4 §3)
            state = {5: "housed", 4: "worn", 3: "gappy", 2: "damaged", 1: "unsheltered", 0: "unsheltered"}[BL.level(b)]
        if state == "housed" and (name in floor_ or (b.get("works") or {}).get("kind") == "upgrade"):
            state = p["beds"]["floor"]                                          # no bed, or the structure being rebuilt (02zh §2, §5)
        if cold and state == "housed" and not b["fire"]:
            state = "no_fuel"
        gear = None
        if state == "housed" and b["structure"] == "camp":                     # a camp (D2-68)
            gear = "camp"
        elif levelled and b is not None and b["structure"] == "camp" and BL.level(b) == 2:   # a damaged camp: a bedroll's shelter
            state, gear = "unsheltered", "bedroll"                              # (brief 4 §3)
        elif state == "unsheltered":                                            # out, with what one carries (D2-68)
            gear = _gear(w, name, where, tents)
        road = today.get("road") or {}
        if state == "unsheltered" and name in (road.get("camp") or {}):         # stopped at a good place: as in a camp (D2-109)
            gear = gear or "camp"
        if gear:
            rec.setdefault("camped", {})[name] = gear
        mult, extra = LF.ration_factor(w, name)                                 # an infant, a child, a pregnancy (D2-141, D2-145)
        from cybertron2.engine import labour as LA
        wk = LA.work_need(p, today, name)                                       # work costs food (D4-103 phase 2)
        need, fall = NE.food(p, {"state": state, "cold": cold, "structure": b["structure"] if b is not None else None,
                                 "warm": b.get("warm", 1.0) if b is not None else 1.0,
                                 "hearth": bool(b["fittings"].get("hearth")) if b is not None else False,
                                 "fire": bool(b["fire"]) if b is not None else False, "gear": gear,
                                 "open_fire": name in fires, "fire_gone": name in (rec.get("fire_out") or []),
                                 "fed_on_road": (road.get("fed") or {}).get(name), "mult": mult, "extra": extra,
                                 "care_fed": rec["care"]["fed"].get(name), **({"work": wk} if wk else {})})
        place = w.place_of(("person", name))
        stores = [a["hands"]]
        if place in s["nodes"]:
            mine = w.takeable(name, place)
            stores += sorted((c for c in mine if c != a["hands"]), key=lambda c: 0 if b is not None and c == b["stock"] else 1)
        if a["stage"] in LF.MINOR:                                             # then from its carers' hands (D2-141)
            stores += [w.hands(x) for x in LF.feeders(w, name) if w.hands(x) not in stores]
        hearth = b is not None and any(b["fittings"].get(f_) for f_ in FIRE) and bool(b["fire"])   # grain boiled at a lit fire (D2-60)
        if state == "unsheltered" and name in fires:                          # at a fire in the open (D4-49, D2-159)
            hearth = True
        rawf = sorted({i for cid in stores for i, q in w.goods(cid).items() if q > 1e-9 and ITEMS.get(i, {}).get("cook")}) if not hearth else []
        from cybertron2.engine import book as BK                                # the book at the meal: what first, the rations,
        bm = BK.meal(w, name) if w.s.get("books") else {"first": [], "ration": 1.0, "skip": []}   # what is kept back (moment 4)
        took = []                                                               # what was eaten, from where: the morning's line (D2-342)
        part = shares.get(w.household_of(name), 1.0) if float(bm["ration"]) >= 1.0 else 1.0
        want = need * float(bm["ration"])
        if part < 1.0:                                                         # one's own hands first, then an even share of what
            ate = _eat(w, place, stores[:1], want, hearth, first=bm["first"], who=name, skip=bm.get("skip") or (), log=took)   # the
            ate += _eat(w, place, stores[1:], (want - ate) * part, hearth, first=bm["first"], who=name,                      # house
                        skip=bm.get("skip") or (), log=took)                                                                 # holds
        else:
            ate = _eat(w, place, stores, want, hearth, first=bm["first"], who=name, skip=bm.get("skip") or (), log=took)
        if rawf and ate + 1e-9 < need:                                         # food that wants a fire, eaten raw or not (D2-160)
            rec.setdefault("uncooked", {})[name] = rawf
        me = ("person", name)
        if rawf and ate > 1e-9:
            w.apply("set", place, ref=me, field="ate_raw", value=w.d)        # seen on them tomorrow (signs.PERSON)
        full = float(p["ration"]) * mult + extra                                # a short meal is a ration's worth at least
        if wk:
            rec.setdefault("work", {})[name] = {"need": wk, "base": round(full, 2),
                                                "units": int(((today.get("units") or {}).get(name) or {}).get("used", 0)),
                                                "over": int(((today.get("units") or {}).get(name) or {}).get("over", 0))}
            if full - 1e-9 <= ate < full + wk - 1e-9:
                rec.setdefault("work_short", []).append(name)                  # a ration eaten, the work's share not: felt (D4-108)
            full += wk                                                          # and the day's work, eaten or paid for in hunger
        if ate + 1e-9 >= need:
            w.apply("harm", place, person=name, hunger=min(0, a["hunger"] + 1))
            w.apply("set", place, ref=me, field="missed", value=0)
            rec["ate"][name] = round(ate, 2)
        elif ate + 1e-9 >= full:
            w.apply("set", place, ref=me, field="missed", value=0)
            rec["short"].append(name)
            rec["ate"][name] = round(ate, 2)
        else:
            w.apply("harm", place, person=name, hunger=max(-2, a["hunger"] - 1))
            w.apply("set", place, ref=me, field="missed", value=a["missed"] + 1)
            rec["missed"].append(name)
            if ate:
                rec["ate"][name] = round(ate, 2)
        _meal_record(w, rec, name, took, bm, need, full, ate, stores, hearth, part)   # the morning's meal line (D2-342)
        soaked = name in (today.get("soaked") or [])                           # soaked at a ford: the cold's fall (world/roads.md)
        if (cold or soaked) and state == "unsheltered" and w.rng("cold", w.d, name).random() < float(p["cold_starving"]) * max(fall, 0.5 if soaked else 0):
            w.apply("harm", place, person=name, hunger=-2)
            rec["cold_falls"].append(name)
    if w.d < w.days - 1:
        for name in w.living():
            a = s["people"][name]
            if a["missed"] >= 3:
                k = a["missed"] - 2
                hz = min(1.0, a["frailty"] + float(p["hazard"]["step"]) * (k - 1))
                if w.rng("hazard", w.d, name).random() < hz or k >= int(p["hazard"]["max_rounds"]):
                    place = w.place_of(("person", name))
                    told = LF.death_told(w, name, where)                        # the household and the housemates (38.75)
                    w.apply("die", place, person=name, cause="starvation")
                    rec["deaths"].append(name)
                    if place in s["nodes"]:
                        w.event(place, "death", f"{name} died in the night, of hunger", target=name, salience=1.0,
                                tags=["death", "food", "family"], **told)
    rec["life"] = LF.night(w, today, rec, where)                              # conception, births, the young, old age (D2-138 to D2-150)
    rec["deaths"] += rec["life"]["deaths"] + rec["life"]["old_age"]
    off = {}
    from cybertron2.engine import stores as SR                                  # each store's portions read once, before the loss
    _RATES.clear()
    _RATES.update({bid: SR.rates(w, bid) for bid, b in sorted(s["buildings"].items()) if b.get("stock") in s["containers"]})
    _RATES["_day"] = (id(w), w.d)
    for cid, c in list(s["containers"].items()):                              # spoilage, by condition (D2-58, D2-87)
        if c["kind"] == "hands" and not s["people"][c["of"]]["alive"]:
            continue
        flesh_by_size = c["kind"] == "carcass" and c.get("beast")
        if flesh_by_size:                                                      # a dead beast's flesh by its size (D4-52, brief 3 §2);
            _carcass_night(w, cid, c)                                          # its hide and tallow as goods are
        for item, q in list(c["goods"].items()):
            if flesh_by_size and item in ("meat", "rotting meat", "offal"):
                continue
            if c["kind"] == "carcass" and item == "meat":                      # a dead beast's meat keeps a day, then goes off (D4-52)
                if q > 1e-9 and w.d - int(c.get("died", w.d)) >= int(THINGS["carcass_fresh_days"]):
                    place = w.place_of(("container", cid))
                    w.apply("destroy", place, src=cid, item="meat", qty=q, why="went off")
                    w.apply("create", place, dst=cid, item="rotting meat", qty=q, why="rot")
                continue
            if c["kind"] == "set" and (c.get("set") or {}).get("method") == "trap in water":   # alive in the water until
                continue                                                                        # lifted (D2-211)
            r, becomes = decay_rate(w, c, item)
            if q > 1e-9 and r > 0:
                place = w.place_of(("container", cid))
                lost = w.apply("destroy", place, src=cid, item=item, qty=round(q * min(1.0, r), 6), why="spoilt")
                rec["spoiled"][item] = round(rec["spoiled"].get(item, 0.0) + lost, 4)
                if c["kind"] == "stock" and item in GOING_OFF and lost > 1e-9:       # fish going off in a store: its smell, the
                    off.setdefault(c["of"], {})[item] = off.get(c["of"], {}).get(item, 0.0) + lost   # morning after (signs pass)
                if becomes and lost > 1e-9:
                    w.apply("create", place, dst=cid, item=becomes, qty=lost, why="rot")
    _RATES.clear()
    PROC.finish(w, rec)                                                         # lots done after their nights, in their containers (u4 §5)
    for bid, items in off.items():                                            # what went off, kept for its sign
        if bid in s["buildings"] and sum(items.values()) >= float(GOING_OFF_LEAST):
            w.apply("set", s["buildings"][bid]["node"], ref=("building", bid), field="spoilt",
                    value={"day": w.d, "items": {i: round(q, 3) for i, q in sorted(items.items())}})
    for bid, b in s["buildings"].items():                                       # a camp falls in after its nights (D2-68)
        if levelled:                                                            # shelter in levels: no fixed life (brief 4 §3)
            break
        if b.get("lasts_until") is not None and w.d >= b["lasts_until"] and b["condition"] > 0:
            w.apply("set", b["node"], ref=("building", bid), field="condition", value=0)
            w.apply("set", b["node"], ref=("building", bid), field="broke", value={"day": w.d, "to": 0})
            w.event(b["node"], "build", f"{b['name']} has fallen in", about=[f"building:{bid}"], salience=0.3, tags=["shelter"])
    for bid, b in s["buildings"].items():                                       # breaks (H-5), by structure (D2-168)
        if levelled:                                                            # in levels: wear and damage by the weather (brief 4 §3)
            if not b.get("unfinished") and BL.level(b) > 0 and _wear_night(w, bid, b, p):
                rec["breaks"].append(bid)
            continue
        q = float(p["breaks"]["cold" if w.cold(b["node"]) else "p"]) * float(p["breaks"]["structure"].get(b["structure"], 1.0))
        if not b.get("unfinished") and b["condition"] > 0 and w.rng("break", w.d, bid).random() < q:
            w.apply("set", b["node"], ref=("building", bid), field="condition", value=b["condition"] - 1)
            w.apply("set", b["node"], ref=("building", bid), field="broke", value={"day": w.d, "to": b["condition"]})
            rec["breaks"].append(bid)
            painted = [ln for ln in b.get("lines") or [] if ln.get("how") == "paint"]
            if b["structure"] == "wattle" and painted:                         # a painted line on wattle fades with each break
                gone = sorted(painted, key=lambda ln: (int(ln.get("day", -1)), int(ln["slot"])))[0]
                w.apply("set", b["node"], ref=("building", bid), field="lines", value=[ln for ln in b["lines"] if ln is not gone])
                ch = list(b.get("changes") or []) + [{"day": w.d, "text": f"the painted words {BL.spot_words(b, int(gone['slot']))} of "
                                                       f"{b['name']} have faded away with the damp", "by": None}]
                w.apply("set", b["node"], ref=("building", bid), field="changes", value=ch[-20:])
    _grow(w)
    from cybertron2.engine import labour as LA
    LA.fade(w)                                                                  # skill unpractised fades (D4-103 phase 2)
    from cybertron2.engine import farm as FM
    rec["farm"] = FM.night(w)
    from cybertron2.engine import wild as WL                                    # the wild layer, with its pack only (D2-199)
    WL.night(w, rec)
    from cybertron2.engine import gear as GE                                    # gear rots by time and condition (u3 §3.2)
    gone = GE.rot_night(w)
    if gone:
        rec["gear"] = gone
    for oid, o in s["offers"].items():                                          # offers lapse (money_and_markets.md)
        if not o["open"]:
            continue
        gone = s["people"][o["by"]]["at"] != o["node"] or not s["people"][o["by"]]["alive"]
        if gone or (o.get("until") is not None and o["until"] <= w.d):         # to a person: at nightfall; to anyone: while
            w.apply("close_offer", o["node"], offer=oid, why="lapsed")        # the offerer stays, or until its day
    s["log"].append(rec)
    return rec


def departures(w, today) -> list:
    """Departures at nightfall (D4-8), with the traveller's choices for the road (world/roads.md, D2-105). Run before the roads'
    night and the fuse sub-step, so those leaving tonight are on their first stretch."""
    s = w.s
    out = []
    for name, to in sorted((today.get("travel") or {}).items()):
        a = s["people"][name]
        if a["alive"] and a["at"] is not None:
            here = a["at"]
            road = next(r for r, x in s["roads"].items() if {x["a"], x["b"]} == {here, to})
            homes = w.homes(name)
            h = next((b for b in homes if s["buildings"][b]["node"] == here), None)
            if h:                                                            # the house as last seen (D4-35: not watched from afar)
                w.apply("set", here, ref=("person", name), field="home_seen", value={
                    "day": w.d, "building": h, "stock": dict(w.goods(s["buildings"][h]["stock"])),
                    "condition": s["buildings"][h]["condition"], "door": s["buildings"][h]["door"]})
            lead = ((today.get("travel_choices") or {}).get(name) or {}).get("lead")
            from cybertron2.engine import herds as HD
            ox = HD.pack_ox_for(w, name, lead) if lead else None               # the pack ox chosen at departure (D2-136)
            w.apply("depart", here, person=name, road=road, to=to)
            from cybertron2.engine import layout as LY
            LY.wear_way(w, road, here)                                       # a hidden end worn by use (D2-92)
            w.apply("transit", road, person=name, fields={"choices": dict((today.get("travel_choices") or {}).get(name) or {})})
            if ox:                                                           # one ox goes with the party, carrying (D2-136)
                from cybertron2.engine import roads as RD
                HD.lead_ox(w, name, ox, road, RD.position(w, a["transit"]))
            from cybertron2.engine import life as LF
            for baby in LF.infants_of(w, name, here):                        # her infants go with her (D2-141)
                w.apply("depart", here, person=baby, road=road, to=to)
                w.apply("transit", road, person=baby, fields={"carried_by": name})
            out.append({"agent": name, "from": here, "to": to})
    today["_departed"] = out
    return out


def decay_rate(w, c, item) -> tuple:
    """A good's loss tonight in its container (economy/goods.md "Decay", D2-87): its rate in a house, times the keeping fittings (D2-45,
    D2-58) in a store, the conditions of a thing at a spot (open, dry or wet; buried) and the season and the frost; and what the lost
    share becomes in the open. Hands keep the rate in hand. Returns (share, becomes)."""
    from cybertron2.engine import environment as EV, things as TH
    node = TH.where(w, c)                                                     # where it lies (D4-111)
    season, cold = w.calendar()["season"], w.cold(node)
    if c["kind"] == "stock":                                                    # by portion: its space and container (u5 §3)
        from cybertron2.engine import stores as SR
        rr = (_RATES.get(c["of"]) if _RATES.get("_day") == (id(w), w.d) else None)
        if rr is None:
            rr = SR.rates(w, c["of"])
        return rr.get(item, 0.0), None
    if c["kind"] in TH.KINDS:
        cond = "buried" if c.get("hidden") == "buried" or c.get("buried") is not None else ("open_wet" if EV.wet(w, node) else "open_dry")
        table = DECAY.get(ITEMS.get(item, {}).get("decay") or "default", DECAY["default"])
        if c.get("lot"):                                                        # a lot in its container (u4 §5 step 4)
            from cybertron2.engine import process as PROC
            got = PROC.decay(w, c, item, cond, season, cold)
            if got is not None:
                return got
        return spoil_rate(w.p, item, cond, season, cold), table.get("becomes")
    from cybertron2.engine import stores as SR                                  # in hand: fresh foods x1.5 without a creel (u5 §3)
    return SR.in_hand_rate(w, c["of"], item, season, cold) if c["kind"] == "hands" else spoil_rate(w.p, item, "hand", season, cold), None


_RATES = {}                                                                     # a night's store rates, read once a store (u5)


def spoil_rate(p, item, where, season, cold, fittings=()) -> float:
    """The share of a good lost a night (D2-87): `where` is "hand", "store" (a building's, kept by its best keeping fitting),
    "open_dry", "open_wet" or "buried". Pure: the engine and the capacity model both use it."""
    base = float(ITEMS.get(item, {}).get("spoil", 0.0))
    table = DECAY.get(ITEMS.get(item, {}).get("decay") or "default", DECAY["default"])
    s = float(table.get("frozen", 1.0)) if cold else (float(table.get("warm", 1.0)) if season == "summer" else 1.0)
    if where in ("store", "hand"):                                             # well kept: the base (D2-272); a store's portions are
        return base * s                                                         # stores.rate's, in hand the creel's (u5 §3)
    if where == "hand":
        return base * s
    if base <= 0:
        return float((table.get("abs") or {}).get(where, 0.0))
    return base * float(table.get(where, 1.0)) * s


def _gear(w, name, where, tents):
    """What someone sleeping out has to sleep in: a tent of one's own, a place in another's tent here, or a bedroll (D2-68)."""
    a = w.s["people"][name]
    g = w.goods(a["hands"])
    place = w.place_of(("person", name))
    if g.get("tent", 0) >= 1:
        tents.setdefault(place, []).append([name, 1])
        w.apply("wear", place, container=a["hands"], item="tent", uses=1)
        return "tent"
    for t in tents.get(place, []):
        if t[1] < 2:
            t[1] += 1
            return "tent"
    if g.get("bedroll", 0) >= 1:
        w.apply("wear", place, container=a["hands"], item="bedroll", uses=1)
        return "bedroll"
    return None


STAGE_ORDER = {"elder": 0, "adult": 1, "youth": 2, "child": 3, "infant": 4}


def bed_share(w, name) -> float:
    """The beds one takes (D2-165, defaults to confirm): an infant shares its carer's, two children share one (PHYSICS beds)."""
    return float(w.p["beds"].get(w.s["people"][name]["stage"], 1.0))


def sleeping_places(w, today) -> dict:
    """{name: building id or None}: everyone, members as well as guests, sleeps housed only in a bed (D2-165); members take the beds
    at home first, the eldest first; a member with no bed there looks for one where it may sleep, else lies on its home's floor (as
    in a damaged house: `today["_floor"]`); guests and those who chose a place need a free bed (05 §3)."""
    s = w.s
    out, beds_used, floor_ = {}, {}, set()
    chosen = today.get("sleep") or {}
    living = sorted(w.living(), key=lambda n: (STAGE_ORDER.get(s["people"][n]["stage"], 1), n))
    homeless = {}
    for name in living:                                                         # members at home, in a bed if one is free
        a = s["people"][name]
        if a["at"] is None or name in (today.get("travel") or {}):
            out[name] = None
            continue
        if name in chosen:
            continue
        home = next((b for b in w.dwellings(name) if s["buildings"][b]["node"] == a["at"]), None)
        if home:
            need = bed_share(w, name)
            if int(s["buildings"][home]["fittings"].get("beds", 0)) - beds_used.get(home, 0.0) + 1e-9 >= need:
                out[name] = home
                beds_used[home] = beds_used.get(home, 0.0) + need
            else:
                homeless[name] = home
    for name in living:                                                         # then guests, those who chose a place, and members
        if name in out:                                                         # with no bed at home
            continue
        a = s["people"][name]
        cands = []
        if name in chosen:
            cands.append(chosen[name])
        cands += [bid for bid, b in s["buildings"].items() if b["node"] == a["at"] and not b.get("unfinished")
                  and "access" in w.rights(name, ("building", bid)) and bid not in cands and bid != homeless.get(name)]
        out[name] = None
        need = bed_share(w, name)
        for bid in cands:
            b = s["buildings"][bid]
            if b.get("unfinished") or not w.can_enter(name, bid):
                continue
            free = int(b["fittings"].get("beds", 0)) - beds_used.get(bid, 0.0)
            if free + 1e-9 >= need and need > 0 or (need == 0 and bid in w.dwellings(name)):
                out[name] = bid
                beds_used[bid] = beds_used.get(bid, 0.0) + need
                break
        if out[name] is None and name in homeless:                              # on the floor at home (D2-165)
            out[name] = homeless[name]
            floor_.add(name)
    for name in living:                                                         # a baby sleeps where its mother sleeps, in her bed
        a = s["people"][name]
        mother = next((m for m in a.get("parents") or [] if m in s["people"] and s["people"][m].get("sex") == "f"
                       and s["people"][m]["alive"] and m in out), None)
        if a["stage"] == "infant" and mother and s["people"][mother]["at"] == a["at"]:
            out[name] = out[mother]
            floor_.discard(name)
            if mother in floor_ and out[name] is not None:
                floor_.add(name)
    today["_floor"] = sorted(floor_)
    return out


def open_fires(w, today, where, rec) -> set:
    """Fires in the open (D4-49, D2-159): those sleeping out at one place (a node, or a party on the road) share a fire; whoever chose
    to light one burns 4 heat from their hands (2 timber, or firewood or charcoal by the order), and it warms up to 4 there, those
    who chose a fire first. Returns who slept by a fire."""
    from cybertron2.engine import forests as FO
    hp = w.p["heat"]
    want = today.get("fire") or {}
    out = [n for n in w.living() if where.get(n) is None]
    groups = {}
    for n in out:
        a = w.s["people"][n]
        key = ("node", a["at"]) if a["at"] is not None else ("road",) + tuple((a["transit"] or {}).get(k) for k in ("road", "from", "to", "left", "arrive"))
        groups.setdefault(key, []).append(n)
    warmed = set()
    for key, ppl in groups.items():
        lighters = [n for n in ppl if want.get(n)]
        rest = [n for n in ppl if not want.get(n)]
        queue = lighters + rest
        for n in lighters:
            if not queue or n in warmed:
                continue
            place = w.place_of(("person", n))
            if FO.burn(w, place, w.hands(n), float(hp["open"]) * weather_fuel(w, place), why="fire"):
                rec.setdefault("open_fire", []).append(n)
                by = [n] + [x for x in queue if x != n and x not in warmed][: int(hp["share"]) - 1]
                warmed.update(by)
                queue = [x for x in queue if x not in warmed]
                if fire_goes_out(w, ("open", n), False, place):                         # rain or wind took it in the night (D4-83)
                    rec.setdefault("fire_out", []).extend(by)
    return warmed


def house_heat(p, b, cold) -> float:
    """The heat a house's fire burns tonight (D2-157): one fire for its hearths, 1 a normal night and 4 a cold one for each hearth;
    a fire ring alone counts as one; a ring beside a hearth adds nothing (D4-93: one room, one fire)."""
    hp = p["heat"]
    hearths, rings = int(b["fittings"].get("hearth") or 0), int(b["fittings"].get("fire ring") or 0)
    return float(hp["cold" if cold else "normal"]) * max(1, hearths if hearths else rings)


def weather_fuel(w, at) -> float:
    """What a fire under no roof burns tonight at a place against the dry night's (D4-83): rain and wind wet it, lying snow wets
    the wood."""
    from cybertron2.engine import environment as EV
    hp = w.p["heat"]
    x = float((hp.get("weather") or {}).get(EV.weather(w, at), {}).get("fuel", 1.0))
    return x * (float(hp.get("snow_lying_fuel", 1.0)) if EV.snow_lying(w, at) else 1.0)


def fire_goes_out(w, key, ring, at) -> bool:
    """Whether a fire under no roof goes out in the night (D4-83): a chance in a downpour or a gale, less with a fire ring."""
    from cybertron2.engine import environment as EV
    hp = w.p["heat"]
    q = float((hp.get("weather") or {}).get(EV.weather(w, at), {}).get("out", 0.0)) * (float(hp.get("ring_keeps", 1.0)) if ring else 1.0)
    return q > 0 and w.rng("fire-out", w.d, *key).random() < q


def eaten_worth(item, hearth=True) -> float:
    """Food a unit gives eaten: what is better cooked gives its raw worth without a lit fire (D2-160). Pure."""
    return float(ITEMS[item].get("raw", ITEMS[item]["food"])) if ITEMS[item].get("cook") and not hearth else float(ITEMS[item]["food"])


def eat_order(items, hearth=True) -> list:
    """The order food is eaten in: what needs no fire first, then the most perishable (D2-160). Pure."""
    return sorted(items, key=lambda i: (eaten_worth(i, hearth) < ITEMS[i]["food"], -ITEMS[i]["spoil"]))


def _meal_record(w, rec, name, took, bm, need, full, ate, stores, hearth, part=1.0) -> None:
    """What one ate tonight, for the morning (D2-342): the goods and how much, from which store, by which rule or the usual order,
    how well it met one's hunger; and what each store gave the meal, in all by good. Facts of one's own body and house."""
    from cybertron2.engine import book as BK
    eaten = sorted({i for _, i, _ in took})
    rules = [r for r in bm.get("rules") or [] if r.get("ration") or set(r.get("goods") or ()) & set(eaten)]
    how = "full" if ate + 1e-9 >= need else ("short" if ate + 1e-9 >= full else "hungry")
    why = ""
    if how == "hungry":
        others = {cid for cid in stores if cid != w.hands(name)}
        left = sum(max(0.0, float(q) - (BK.held(w, name, cid, i) if w.s.get("books") else 0.0)) for cid in stores
                   for i, q in w.goods(cid).items() if i in EDIBLE and i not in (bm.get("skip") or ()) and eaten_worth(i, hearth) > 0)
        shared = any(cid in others for x in (rec.get("meal") or {}).values() for cid, _, _ in x["ate"]) if others else False
        kept = []                                                              # what a keep rule held back from one, at or under
        if w.s.get("books"):                                                   # its floor too (W-111: the Meades starved behind
            for cid in stores:                                                 # their seed floor told only "nothing more")
                for i, q in w.goods(cid).items():
                    if i in EDIBLE and q > 1e-9 and eaten_worth(i, hearth) > 0:
                        kept += [{"n": r.get("n"), "words": r.get("words"), "item": i, "qty": round(h, 2)}
                                 for r, h in BK.holding(w, name, cid, i)]
        if float(bm.get("ration", 1.0)) < 1 - 1e-9:
            why = "ration"
        elif kept:
            why = "kept back"                                                  # the household's own rule: named (W-111)
        elif part < 1 - 1e-9:
            why = "shared out"                                                 # the household's even split (W-111)
        elif left > 1e-6:
            why = "kept back"
        else:
            why = "not enough for everyone" if shared else "nothing more"
    rec.setdefault("meal", {})[name] = {"ate": [[cid, i, round(q, 3)] for cid, i, q in took], "rules": rules, "how": how, "why": why,
                                        "ration": float(bm.get("ration", 1.0)), **({"kept": kept} if how == "hungry" and kept else {})}
    hands = w.hands(name)
    for cid, i, q in took:
        if cid != hands and cid in w.s["containers"]:
            d = rec.setdefault("drawn", {}).setdefault(cid, {})
            d[i] = round(d.get(i, 0.0) + q, 3)


HUNGER_WHY = {"kept back": "the rest was kept back", "not enough for everyone": "there was not enough for everyone",
              "shared out": "the household's food was shared out evenly, and there was not enough for everyone",
              "nothing more": "there was nothing more you could eat"}


def _kept_words(m) -> str:
    """Which of the household's rules kept what back from a hungry person's meal (W-111)."""
    by = {}
    for k in m["kept"]:
        e = by.setdefault((k.get("n"), k.get("words")), {})
        e[k["item"]] = e.get(k["item"], 0.0) + float(k["qty"])
    bits = [f"rule {n}" + (f" (“{words}”)" if words else "") + " kept back " + _and([f"{show_fine(q)} {i}" for i, q in sorted(g.items())])
            for (n, words), g in by.items()]
    return "the household's " + "; ".join(bits) + "."


CRUMB = 0.1                                       # less than this of a good is said as crumbs, not a figure (L-178, W-111)


def _and(xs) -> str:
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _goods_words(pairs) -> str:
    """Goods as people say them: the amounts that count, and the rest as crumbs of them ('0.05 greens' is no meal's figure)."""
    big = [f"{show_fine(q)} {i}" for i, q in pairs if float(q) >= CRUMB]
    bits = [i for i, q in pairs if float(q) < CRUMB]
    crumbs = f"crumbs of {_and(bits)}" if bits else ""
    return _and(big + ([crumbs] if crumbs else [])) if big else crumbs


def meal_lines(w, name, rec) -> list:
    """The morning's meal line (D2-342), from last night's record: what one ate, from which store, by which rule or the usual order,
    and how well it fed; then what one's household's stores gave the meal in all, by good. At most two lines."""
    m = ((rec or {}).get("meal") or {}).get(name)
    if not m:
        return []
    by_store = {}
    for cid, i, q in m["ate"]:
        by_store.setdefault(cid, {})
        by_store[cid][i] = by_store[cid].get(i, 0.0) + float(q)
    if by_store:
        what = "; ".join(f"{_goods_words(sorted(g.items(), key=lambda kv: -kv[1]))} from {store_name(w, cid, name)}"
                         for cid, g in by_store.items())
        rules = m.get("rules") or []
        how = (" and ".join(f"{'your' if r['own'] else 'the household' + chr(39) + 's'} rule {r['n']} (“{r['words']}”)" for r in rules)
               if rules else "")
        line = f"Last night you ate {what}, " + (f"by {how}" if how else "in the usual order (what needs no fire, then what spoils soonest)")
    else:
        line = "Last night you ate nothing"
    if m["how"] == "full":
        line += ": you ate your fill."
    elif m["how"] == "short":
        line += ": enough to keep you, short of your fill."
    else:
        r = m["ration"]
        share = "half" if abs(r - 0.5) < 1e-6 else f"{r:g} of a full meal"
        line += ": you were still hungry; " + (f"the rule gave you a {share} share." if m["why"] == "ration"
                                                else _kept_words(m) if m["why"] == "kept back" and m.get("kept")
                                                else HUNGER_WHY.get(m["why"], "there was not enough") + ".")
    out = [line]
    from cybertron2.engine import book as BK
    hh = w.household_of(name)
    gave = []
    for cid, g in sorted(((rec or {}).get("drawn") or {}).items()):
        c = w.s["containers"].get(cid) or {}
        bid = c.get("of") if c.get("kind") == "stock" else (c.get("door") or c.get("in"))
        if bid in w.s["buildings"] and BK._holds(w, hh, bid) and g:
            gave.append(f"{store_name(w, cid, name)} gave {_goods_words(sorted(g.items(), key=lambda kv: -kv[1]))}")
    if gave:
        out.append("For the whole household's meal, " + "; ".join(gave) + " in all.")
    return out


def store_name(w, cid, who=None) -> str:
    """A store eaten from, in words: what one carried, a house's store, its door or what hangs in it."""
    c = w.s["containers"].get(cid) or {}
    bname = lambda b: (w.s["buildings"].get(b) or {}).get("name", b)            # noqa: E731
    if c.get("kind") == "hands":
        return "what you carried" if c.get("of") == who else f"what {c.get('of')} carried"
    if c.get("kind") == "stock":
        return f"{bname(c['of'])}'s store"
    if c.get("door"):
        return f"what lay at {bname(c['door'])}'s door"
    if c.get("in"):
        return f"what hung in {bname(c['in'])}"
    return "a store"


def even_shares(w, where) -> dict:
    """{household: the share of a meal each member eats tonight} for a household whose food does not reach its members' meals and
    whose book has no share rule: each eats the same share, not the first by name their fill and the last nothing (W-111; bench's
    World 0b reruns, where the last of the Fletchers by name starved night after night while the rest ate). The food is what the
    members can draw (their hands and their stores, less what a keep rule holds back), at its worth with the house's fire or not; the
    meals are each one's ration (life.ration_factor). A household with a share rule keeps its own order (D2-339)."""
    from cybertron2.engine import book as BK
    out = {}
    by = {}
    for n in w.living():
        hh = w.household_of(n)
        place = w.place_of(("person", n))
        if hh and place in w.s["nodes"]:
            by.setdefault(hh, []).append((n, place))
    for hh, ms in sorted(by.items()):
        if any(r.get("rule") == "share" for r in BK.household_rules(w, hh)):
            continue
        need, seen, food = 0.0, set(), 0.0                                   # one's own hands are one's own: the share is of the
        hands = {w.hands(m) for m, _ in ms}                                    # household's stores, after what each carries
        for n, place in ms:
            mult, extra = LF.ration_factor(w, n)
            bid = where.get(n)
            hearth = bool(bid and w.s["buildings"][bid].get("fire"))
            worth = lambda cid: sum(eaten_worth(i, hearth) * max(0.0, float(q) - (BK.held(w, n, cid, i) if w.s.get("books") else 0.0))
                                    for i, q in w.goods(cid).items() if i in EDIBLE and q > 1e-9)   # noqa: E731
            need += max(0.0, float(w.p["ration"]) * mult + extra - worth(w.hands(n)))
            for cid in w.takeable(n, place):
                if cid in seen or cid in hands:
                    continue
                seen.add(cid)
                food += worth(cid)
        if need > 1e-9 and 1e-9 < food < need - 1e-9:                         # nothing to share is no split
            out[hh] = round(food / need, 4)
    return out


def _eat(w, place, stores, need, hearth=True, first=(), who=None, skip=(), log=None) -> float:
    """Up to `need` in food value, from the stores in order, most perishable first; what is better cooked is eaten raw, for less,
    without a lit fire (D2-160: grain 0.2, flour 0.5, beans nothing, fresh meat 0.8), after what needs no fire. The book's `first`
    goes before (u6 §4), and what it holds back is not eaten. `log` gets (store, good, qty) for each good eaten (D2-342)."""
    got = 0.0
    order = [i for i in first if i in EDIBLE] + [i for i in eat_order(EDIBLE, hearth) if i not in first]
    order = [i for i in order if i not in skip]                               # goods a share keeps for others (D2-339)
    from cybertron2.engine import book as BK
    books = bool(w.s.get("books")) and who is not None
    for cid in stores:
        g = w.goods(cid)
        for item in order:
            v = eaten_worth(item, hearth)
            if v <= 0:
                continue
            have = g.get(item, 0.0) - (BK.held(w, who, cid, item) if books else 0.0)
            if got + 1e-9 < need and have > 1e-9:
                q = min(have, (need - got) / v)
                gone = w.apply("destroy", place, src=cid, item=item, qty=q, why="eaten")
                got += gone * v
                if log is not None and gone > 1e-9:
                    log.append((cid, item, float(gone)))
    return round(got, 6)


def slow_season(season) -> bool:
    """Whether stocks come back slowly in this season (regrow_winter): the winter."""
    return season == "winter"


def regrow(p, reg, S, K, r, winter) -> float:
    """A night's regrowth of a stock by its renewal rule (D4-7): logistic at its rate (slowed in winter), a fast stock also refilling 1% of
    its gap, a threshold stock not at all below its threshold share. Pure: the engine and the capacity model both use it."""
    if K <= 0:
        return S
    if reg == "threshold" and S < float(p["game_threshold"]) * K:
        return S
    rate = r * (float(p["regrow_winter"]) if winter else 1.0)
    return round(min(K, S + rate * S * (1 - S / K) + (0.01 * (K - S) if reg == "fast" else 0)), 4)


def _grow(w):
    """Resources come back by their renewal rules (D4-7); crops ripen from the sowing day and rot after the window (D2-12)."""
    winter = slow_season(w.calendar()["season"])
    p = w.p
    from cybertron2.engine import renewal as RN
    season = w.calendar()["season"]
    done = set()                                                                         # a body's stock is renewed once (D2-229)
    for pid, par in w.s["parcels"].items():
        for key, r in par["res"].items():
            rule = RN.of(key, r)                                                         # woods: forests.night (D2-156)
            if rule not in RN.NIGHTLY or r["K"] <= 0 or id(r) in done:
                continue
            done.add(id(r))
            extra = {}
            if rule == "shallows":                                                       # none under ice (u1 §4)
                from cybertron2.wild import water as WT
                extra["iced"] = WT.iced(w, pid)
            elif rule == "willow":                                                       # the rods' year (u3 §1.1)
                extra["first_spring"] = season == "spring" and int(w.calendar()["day"]) == 1
                extra["grazed"] = any(h.get("parcel") == pid and int(h.get("count", 0)) > 0 for h in w.s["herds"].values())
            S = RN.RULES[rule](p, r, RN.context(w, par, winter=winter, season=season, **extra))   # with its place's weather (D4-113)
            if rule == "willow" and extra.get("first_spring"):
                from cybertron2.wild import willow as WI
                if WI.spring_K(r) != r["K"]:
                    w.apply("set_res", par["node"], parcel=pid, key=key, fields={"K": WI.spring_K(r)})
            if S != r["S"]:
                w.apply("set_res", par["node"], parcel=pid, key=key, fields={"S": S})
        # crops: farm.night (D2-53, D4-39)
    from cybertron2.engine import forests as FO
    FO.night(w)


def _carcass_night(w, cid, c) -> None:
    """A dead beast's night (brief 3 §2): its meat fresh for its size's days, then rotting meat; rotting meat and offal lose the
    size's `rot` a night times the season's, none on a frozen night or under snow (a buried or burnt one keeps or is gone); below
    `carcass_gone` of its first flesh, the rest is gone and only bones lie. Its hide and tallow keep as goods do."""
    from cybertron2.engine import environment as EV, things as TH
    place = w.place_of(("container", cid))
    if c.get("burnt") is not None:
        return
    size = THINGS["carcass_sizes"][TH.carcass_size(c)]
    q = float(c["goods"].get("meat", 0.0))
    if q > 1e-9 and w.d - int(c.get("died", w.d)) >= int(size["fresh"]):
        w.apply("destroy", place, src=cid, item="meat", qty=q, why="went off")
        w.apply("create", place, dst=cid, item="rotting meat", qty=q, why="rot")
    if c.get("buried") is not None:
        return
    at = TH.where(w, c)
    if w.cold(at) or EV.snow_lying(w, at):
        return                                                                # frost stalls it; a carcass in the snow keeps
    r = min(1.0, float(size["rot"]) * float(THINGS["carcass_rot_season"].get(w.calendar()["season"], 1.0)))
    for item in ("rotting meat", "offal"):
        x = float(c["goods"].get(item, 0.0))
        if x > 1e-9:
            w.apply("destroy", place, src=cid, item=item, qty=round(x * r, 6), why="rotted")
    m0 = float(c.get("mass0") or 0.0)
    if m0 > 0 and TH.flesh(w, w.s["containers"][cid]) < float(THINGS["carcass_gone"]) * m0:
        for item in TH.FLESH:
            x = float(w.s["containers"][cid]["goods"].get(item, 0.0))
            if x > 1e-9:
                w.apply("destroy", place, src=cid, item=item, qty=x, why="rotted to the bones")


def _wear_night(w, bid, b, p) -> bool:
    """A building's night in levels (brief 4 §3, shelter_damage.md §2): minor wear (a level) and serious damage (as many levels as
    its cause is severe), both by structure, times the night's weather where it stands and the root of its floor; a camp's three
    states wear faster and a gale flattens one. Returns whether it lost a level."""
    import math
    from cybertron2.engine import buildings as BL, environment as EV
    W = p["wear"]
    node, st_ = b["node"], b.get("structure", "wattle")
    rng = w.rng("wear", w.d, bid)
    lab = EV.weather(w, node)
    v = EV.values(w, node) or {}
    causes = []
    if w.cold(node):
        causes.append("frost")
    if lab == "heavy rain":
        causes.append("heavy rain")
    if lab == "gale" or float(v.get("storm", 0.0) or 0.0) >= float(W["storm"]):
        causes.append("gale")
    elif float(v.get("wind", 0.0) or 0.0) >= float(W["strong_wind"]):
        causes.append("strong wind")
    if EV.snow_lying(w, node) and st_ != "stone":
        causes.append("snow")
    if lab == "heavy rain" and int((w.s["parcels"].get(b.get("parcel")) or {}).get("height", 1)) == 0 and st_ != "stone":
        causes.append("flood")
    if b.get("monument") == "weir":                                           # a weir wears by its sections, by the river (D2-210:
        return False                                                           # wild._weir_wear)
    lv = BL.level(b)
    if lv in (3, 4) and w.d - int(b.get("level_since", -999) if b.get("level_since") is not None else -999) >= int(W["unmended_days"]) \
            and b.get("level_since") is not None:
        causes.append("unmended")
    minor_x = serious_x = 1.0
    for c in causes:
        mx, sx = W["weather"][c]
        minor_x *= float(mx)
        serious_x *= float(sx)
    size = math.sqrt(max(1.0, float(b.get("size") or 4)) / float(W["size_ref"]))
    if st_ == "camp":
        if "gale" in causes and lv >= 5 and rng.random() < float(W["camp_flatten"]):
            to = 0
        else:
            q = (float(W["minor"]["camp"]) if lv >= 5 else float(W["camp_down"])) * minor_x
            to = (2 if lv >= 5 else 0) if rng.random() < min(1.0, q) else lv
    else:
        to = lv
        if rng.random() < min(1.0, float(W["serious"].get(st_, 0.001)) * serious_x * size):
            sev = "gale" if "gale" in causes else ("heavy" if ("snow" in causes or "flood" in causes) else "mild")
            odds = W["take"][sev]
            u, acc, n = rng.random(), 0.0, 1
            for i_, o in enumerate(odds):
                acc += float(o)
                if u < acc:
                    n = i_ + 1
                    break
            n = max(1, n - 1) if st_ == "timber" else (min(2, 1 if n < 3 else 2) if st_ == "stone" else n)
            to = lv - n
        elif rng.random() < min(1.0, float(W["minor"].get(st_, 0.01)) * minor_x * size):
            to = lv - 1
    to = max(0, to)
    if to >= lv:
        return False
    BL.set_level(w, node, bid, to)
    w.apply("set", node, ref=("building", bid), field="broke", value={"day": w.d, "to": BL.COND_OF_LEVEL[to], "level": to,
                                                                      "by": causes[:2]})
    if to <= 0:
        w.event(node, "build", f"{b['name']} has fallen in" if st_ != "camp" else f"{b['name']} was blown flat in the night",
                about=[f"building:{bid}"], salience=0.4, tags=["shelter"])
    return True
