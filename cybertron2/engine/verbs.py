"""The verbs (spec/agents/actions.md, proposals/verbs.md): each is a composition of primitives at the agent's node, reading only
`Here` and `Mind` (D4-35). Techniques, recipes, blueprints and fittings are data (D4-24): one handler for gathering and work, one
for making, one for building.

Each handler: (here, mind, a) -> result line. Refusals name what is short and cost nothing.
"""
from __future__ import annotations

import math
from cybertron2.engine import renewal as RN, yields as YD
from cybertron2.engine import buildings as BL, farm as FM, knowledge as KN, modifiers as MOD, perceive as PC, things as TH
from cybertron2.engine.data import BLUEPRINTS, COVERS, FITTINGS, ITEMS, LINES, MONUMENTS, ROOMS, SPACE, TECHNIQUES, THINGS, TIERS, TRY
from cybertron2.engine.here import Refused, show

# The registry (cybertron 1's action_registry): arguments, cost (units, a physics path, or "craft"), the line in the manual, and
# `when` (only in a world with roads). The prompt's verb list and the reply schema are generated from it.
VERB = {
    "gather": {"args": '{"what", "at"?: place, "for"?: party}', "cost": "craft", "doc": "take from the land: {crafts}"},
    "work": {"args": '{"what", "at"?: place or building, "item"?: the seed to sow (grain, rye, beans: always say which), the beast to slaughter (cow, ox, bull, calf), or food to give a child you care for (with "qty"), "on"?: in a field held in shares, whose plots (a household or person; else your own, then the unclaimed plots), "plots"?: how many plots to sow at most, "pass"?: with care, a sentence for the child to keep, "for"?: party}',
             "cost": "craft", "doc": "{crafts}"},
    "make": {"args": '{"what", "qty"?: times, "for"?: party}', "cost": "craft",
             "doc": "a recipe; the inputs come from what you carry, then from stores here you may take from: {crafts}"},
    "build": {"args": '{"what", "at": a place on built ground or scrub (a new building or a monument; a camp: any place here but water) or a building here (a room added, a fitting), "structure"?: wattle | timber | stone, "storey"?: 2 | 3, "qty"?: beds or stalls, "name"?, "describe"?: a sentence in your words, "how"?: fine | rich | grand, "for"?: party}',
              "cost": 2, "doc": "start or carry on a building, a room, a monument or a fitting: its materials when you start, then the work over days: {crafts}"},
    "move": {"args": '{"item", "qty", "to": store | hands, "at"?: building}', "cost": 0,
             "doc": "between your hands and a store here you may use (your household's)"},
    "take": {"args": '{"item", "qty", "from": a building, someone\'s remains, or a place where you know something lies}', "cost": 1,
             "doc": "from any store you can get into (without the right to it, it is theft, and you may be seen), or from what lies in the "
                    "open (nobody's: whoever takes it holds it)"},
    "give": {"args": '{"to": a person, a household, a building or a place here, "item", "qty", "for"?: your household, to give from its store, "hidden"?}',
             "cost": 0, "doc": "to a person here, into their hands; to a household, or a building you may use, into its store; to a "
                               "building you may not use, or someone not here, left at its door; to a place (a field, a wood), left "
                               "there in the open, where anyone may find it and take it. Leaving, putting down and hiding are giving "
                               "to a place"},
    "accept": {"args": '{"offer": id, "lots"?: n, "for"?: party}', "cost": 0, "doc": "an open offer here: both sides at once, or nothing"},
    "withdraw": {"args": '{"offer": id}', "cost": 0, "doc": "take back an offer of yours"},
    "release": {"args": '{"agreement": id}', "cost": 0,
                "doc": "count what is owed to you (or your household) on an agreement as paid, however it was paid, or forgive it"},
    "host": {"args": '{"person", "at"?: building, "feed"?: true}', "cost": 0,
             "doc": "let someone sleep in a house you may let people into, tonight (and eat from its store, if you feed them)"},
    "grant": {"args": '{"to": person or household or anyone, "at": building, "what": shelter | shelter and food, "days"?: n}', "cost": 0,
              "doc": "let someone use a house you may let people into, until you revoke it (or for some days)"},
    "revoke": {"args": '{"to", "at": building}', "cost": 0, "doc": "end what you granted"},
    "join": {"args": '{"household"}', "cost": 0, "doc": "ask to be taken into a household here; it happens if one who may admit you does so today"},
    "admit": {"args": '{"person"}', "cost": 0, "doc": "take someone into your household, if they ask today (the head, or whoever your household allows)"},
    "leave_household": {"args": "", "cost": 0, "doc": "leave your household (you keep what you carry)"},
    "found": {"args": '{"name"}', "cost": 0, "doc": "start a household of your own, with you at its head"},
    "claim": {"args": '{"thing": a field, building or herd here, "plots"?: of a field, pasture or meadow, how many of its plots (else all of them), "for"?: your household}', "cost": 0,
              "doc": "claim it as yours: others will know, and may agree or dispute it"},
    "drive": {"args": '{"thing": a herd here, "item"?: cows | oxen | bulls | calves | all, "qty"?, "to": a place here}', "cost": 1,
              "when": "herds", "doc": "move beasts to another place here (a bull kept apart from the cows does not breed)"},
    "sleep": {"args": '{"at": building}', "cost": 0, "doc": "sleep there tonight, if you can get in and a bed is free"},
    "set": {"args": '{"thing": door | gap, "to": open | barred (a door) or open | shut (a gap), "at"?: building}', "cost": 0,
            "doc": "the door of a building you manage; or the gap of a fish weir you work or a water mill you manage on a river where "
                   "fish run (shut: the weir's traps take the runs passing, and a mill grinds at full but holds back the fish going "
                   "up; open: the run passes, and the mill grinds at half)"},
    "travel": {"args": '{"to": a place, or a way from here as the roads name it, "on trouble"?: push on | wait | turn back | go round, "days"?: how long to wait or stop, "stop at"?: a good place you know on the way, "gather"?: true, "meeting"?: stop | pass by, "searching"?: a herd or a person lost on that road, "lead"?: a herd of yours here with an ox, to lead an ox as a pack ox (a harness in hands; it carries 60)}',
               "cost": 0, "when": "roads", "doc": "the day's last act: you leave at nightfall and arrive on a later morning. On the road "
                                                 "you decide nothing unless something happens (trouble, a meeting, a find); what you "
                                                 "choose here is what you do if the road gives trouble, and whether you stop for "
                                                 "others you meet (pass by: you go on without a word)"},
    "watch": {"args": '{"person"}', "cost": ["watch", "units"], "doc": "spend the day working beside them: you see how they do things"},
    "teach": {"args": '{"to", "what"}', "cost": ["teach", "units_teacher"], "doc": "one session, if they set aside time to learn the same day"},
    "learn": {"args": '{"from", "what"}', "cost": ["teach", "units_learner"], "doc": "one session, if they set aside time to teach the same day"},
    "attack": {"args": '{"target": person or building, "aim": rob | hurt}', "cost": ["combat", "units"],
               "doc": "settled tonight; a house with aim rob: break in for its food; with aim hurt: break in and set on those inside"},
    "guard": {"args": '{"at"?: building}', "cost": 1, "doc": "stand guard tonight over a building here and anyone set upon"},
    "fire": {"args": "", "cost": 0, "doc": "light a fire in the open tonight if you sleep out (on the road, or with no bed), from timber in your "
                                            "hands, so grain and flour can be boiled; say it before you set off"},
    "partner": {"args": '{"with": a person here}', "cost": 0, "doc": "become partners with someone here, if they choose it too today"},
    "part": {"args": "", "cost": 0, "doc": "end your partnership"},
    "try": {"args": '{"with": a person of the other sex here, "units": 1 or more}', "cost": "units", "when": "children",
            "doc": "try for a child with them, if they try with you today and you both sleep in one place tonight: the more units, "
                   "the better the chance, less with each one more"},
    "name": {"args": '{"heir"?: a person of your household, "head"?: a person of your household}', "cost": 0,
             "doc": "as head, name who heads the household after you; when a head has died, each grown member names the new head"},
    "order": {"args": '{"what": forage | herd | hay | nothing, "at"?: a place here}', "cost": 0, "when": "children",
              "doc": "as head, set your household's children to a small work each day, until you change it"},
    "meet": {"args": '{"at": a building or a place here, "about"?: what it is for}', "cost": 0, "when": "evening",
             "doc": "call a meeting for the start of tomorrow, before the day's work, for everyone at this place: whoever comes gives a "
                    "unit to it; all who come hear what is said there, and witness what is offered"},
    "come": {"args": '{"to"?: the meeting called for this morning}', "cost": 1, "when": "evening",
             "doc": "go to the meeting called for this morning: before the day's work you talk there with all who come, and may change "
                    "your plan"},
    "write": {"args": '{"at": a building or monument here, "text": a sentence (about 30 words), "line"?: which place (its number, or where it is: "over the door"), to replace a line, "how"?: paint | carve (with a tool; in stone, a mason\'s), "description"?: text in place of "text", to replace its description}',
              "cost": "write", "doc": "write a line on a building or monument (each building has so many places: a small room 2, a "
                                      "medium room 4, a hall 8, a monument 3); whoever goes in, or looks it over, reads it. Painting "
                                      "takes 2 units, carving 4 (6 in stone), changing another's words 1 more; it is seen being done"},
    "erase": {"args": '{"at": a building or monument here, "line": which place}', "cost": "write",
              "doc": "scratch out a line written there: the work it took to write, 1 more if it is another's; it is seen being done"},
    "rest": {"args": "", "cost": 0, "doc": ""},
}
VERBS = tuple(VERB)
FM_KINDS = ("sow", "break", "tend", "manure", "crop", "herd", "milk", "slaughter", "works", "select", "fence", "gate")
FREE = tuple(v for v, d in VERB.items() if d["cost"] == 0)


def verb_here(here, verb) -> bool:
    when = VERB[verb].get("when")
    return not when or (when == "roads" and bool(here.roads())) or (when == "herds" and any(FM.head(h) > 0 for h in here.herds().values())) \
        or (when == "children" and here.children_on()) or (when == "evening" and bool(here.setting("evening")))


def verb_units(p, verb):
    c = VERB[verb]["cost"]
    if c in ("craft", "units", "write"):
        return None
    if isinstance(c, list):
        x = p
        for k in c:
            x = x[k]
        return int(x)
    return int(c)


def cost(here, a) -> int:
    v = str((a or {}).get("do", "")).lower().strip()
    if v not in VERB:
        return 0
    if v == "set" and str(a.get("thing") or "").strip().lower() in ("gap", "the gap", "hatches", "sluice", "weir", "the weir"):
        from cybertron2.engine.data import WATER_WORKS                         # the traps or hatches put in or out (brief 5 §3)
        to = {"closed": "shut", "close": "shut"}.get(str(a.get("to") or "").strip().lower(), str(a.get("to") or "").strip().lower())
        try:
            from cybertron2.engine import wild as WL
            b = here.buildings()[_gap_site(here, a.get("at"))]
            if WL.gap(b) == to:
                return 0
            return int(WATER_WORKS["weir" if WL.is_weir(b) else "mill"]["units"].get(to, 1))
        except Refused:
            return 0
    n = verb_units(here.p, v)
    if n is not None:
        return n
    if VERB[v]["cost"] == "units":                                            # as many as one chooses to spend (D2-146)
        return _units(a.get("units"))
    if VERB[v]["cost"] == "write":                                            # a line's own engraving (D2-170)
        return max(1, write_units(here, a, erase=v == "erase"))
    tech = KN.resolve(a.get("what"), a.get("do"))
    if tech is None:
        return 1
    tech, a = _as_modified(tech, v, a)
    n = int(TECHNIQUES[tech]["units"])
    if TECHNIQUES[tech].get("units_by") == "bury":                            # by the ground and the cold (D2-96)
        cairn = str(a.get("method", "")).lower() == "cairn"
        cid = _thing_site(here, a.get("at"), graves=cairn, kinds=_dead_kinds(tech))
        if cid and cairn:
            n = here.bury_units(cid, cairn=True)
        elif cid:                                                              # a grave is dug a share at a time, by anyone, over days
            n = max(1, min(n, _grave_left(here, cid, a)))                      # (D4-99): an act puts in up to its units
    elif TECHNIQUES[tech].get("units_by") == "burn":                          # by the carcass's size (brief 3 §4)
        cid = _thing_site(here, a.get("at"), kinds=_dead_kinds(tech))
        if cid:
            n = int(THINGS["carcass_sizes"][here.carcass_size(cid)]["burn"]["units"])
    elif v == "make":
        try:
            n *= max(1, int(_qty(a.get("qty"), 1)))
        except Refused:                                                        # a bad qty is refused by the act itself, not by its cost
            pass
    return n + MOD.units(a, v, tech)


def _as_modified(tech, verb, a):
    """A modifier written as the technique ("dibble") is the technique it modifies, with the modifier set (D2-94)."""
    d = TECHNIQUES.get(tech, {})
    if d.get("modifies"):
        base = next((x.split(":", 1)[1] for x in d["modifies"] if x.startswith(f"{verb}:")), None)
        if base:
            return base, {**a, d["key"]: d["value"]}
    return tech, a


def _bury(here, cid, cairn, a) -> str:
    """Burying (D2-96, D4-99). A cairn of stones (its stone and units) covers the body at once, or is raised over a grave already
    dug. Otherwise the act digs: it puts in up to the act's units, as a share of the grave the ground wants now (soft, stony,
    frozen), and the share keeps between days and adds up across diggers; the body is buried when the grave is whole."""
    from cybertron2.engine import things as TH
    c = here.thing(cid)
    spot = here.spot_name(c)
    if cairn:
        _consume(here, a["_mods"].get("inputs") or {})
        here.apply("set_thing", cid=cid, field="cairn", value=True)
        here.apply("set_thing", cid=cid, field="cairn_day", value=here.day)   # for its signs
        here.apply("set_thing", cid=cid, field="cairn_by", value=here.name)
        if c.get("buried") is not None:
            return f"You raised a cairn of stones over the grave of {c['of']} at {spot}."
        here.apply("set_thing", cid=cid, field="buried", value=here.day)
        here.apply("set_thing", cid=cid, field="grave", value=None)
        return f"You buried {c['of']} at {spot} under a cairn of stones."
    need = here.bury_units(cid)
    g = dict(c.get("grave") or {})
    shallow = str(a.get("method", "")).lower() == "shallow"                   # half the digging: beasts may dig it up (brief 3 §4)
    put = max(1, min(int(TECHNIQUES["bury"]["units"]), _grave_left(here, cid, a)))
    done = min(1.0, round(float(g.get("done", 0.0)) + put / need, 6))
    by = list(dict.fromkeys(list(g.get("by") or []) + [here.name]))
    others = [x for x in by if x != here.name]
    if done >= (0.5 if shallow else 1.0) - 1e-6:
        here.apply("set_thing", cid=cid, field="buried", value=here.day)
        here.apply("set_thing", cid=cid, field="cairn", value=False)
        here.apply("set_thing", cid=cid, field="grave", value=None)
        here.apply("set_thing", cid=cid, field="depth", value="shallow" if done < 1.0 - 1e-6 else "deep")
        return (f"You finished the grave and buried {c['of']} at {spot}" + (f"; {', '.join(others)} dug it with you" if others else "")
                + (", shallow: beasts may dig it up" if done < 1.0 - 1e-6 else "")
                + ". A cairn of stones can be raised over it later (3 stone).")
    here.apply("set_thing", cid=cid, field="grave", value={"done": done, "by": by, "day": here.day, "began": g.get("began", here.day)})
    left = here.grave_left(cid)
    return (f"You dug at the grave of {c['of']} at {spot}: {TH.grave_words(done)} (about {left} more unit{'s' if left != 1 else ''} "
            f"of digging{' in the frozen ground' if here.cold() else ''}). Anyone can help dig it, and the work keeps for another day.")


def _dead_kinds(tech) -> tuple:
    """Which of the dead a technique works on: bodies, dead beasts (brief 3 §4)."""
    t = (TECHNIQUES[tech].get("at") or {}).get("things") or "body"
    return tuple(t) if isinstance(t, list) else (t,)


def _grave_left(here, cid, a) -> int:
    """Units a grave still wants: a shallow one half the whole (brief 3 §4)."""
    import math
    left = here.grave_left(cid)
    if str((a or {}).get("method", "")).lower() == "shallow":
        c = here.thing(cid)
        need = math.ceil(here.bury_units(cid) / 2)
        done = float((c.get("grave") or {}).get("done", 0.0)) * here.bury_units(cid)
        left = max(0, math.ceil(need - done - 1e-6))
    return left


def _burn(here, cid) -> str:
    """Burning a carcass (brief 3 §4): firewood by its size, from hand or a store one may take from; its flesh, hide and tallow
    burn, and nothing comes to it after; the smoke is seen."""
    c = here.thing(cid)
    size = THINGS["carcass_sizes"][here.carcass_size(cid)]["burn"]
    _consume(here, {"firewood": float(size["firewood"])})
    for item, q in sorted(c["goods"].items()):
        if q > 1e-9:
            here.apply("destroy", src=cid, item=item, qty=q, why="burned")
    here.apply("set_thing", cid=cid, field="burnt", value=here.day)
    spot = here.spot_name(c)
    here.event("work", f"{here.name} burned the dead {c['beast']} at {spot}; the smoke of it went up", salience=0.4,
               tags=["animals"], about=[f"parcel:{c['parcel']}"] if c.get("parcel") else [])
    return f"You burned the dead {c['beast']} at {spot} on a pyre of {size['firewood']:g} firewood: nothing will come to it now."


def _thing_site(here, at, graves=False, kinds=("body",)):
    """A body here by its person's name or its place's name (for burying); with `graves`, a grave with no cairn yet as well (a
    cairn raised after the burial, D4-99), an unburied body first; with kinds holding "carcass", a dead beast by its beast's name
    too (brief 3 §4)."""
    from cybertron2.engine import things as TH
    low = str(at or "").strip().lower()
    pool = (list(here.bodies().items()) if "body" in kinds else []) + (list(here.carcasses().items()) if "carcass" in kinds else []) \
        + (list(here.graves().items()) if graves else [])
    for cid, c in pool:
        names = {c["of"].lower(), here.spot_name(c).lower(), here.spot_name(c).lower().removeprefix("the ")}
        if c.get("beast"):
            names |= {c["beast"], f"the {c['beast']}", f"the dead {c['beast']}", f"dead {c['beast']}", "the carcass", "carcass"}
        pid = c.get("parcel")
        if pid in here.parcels():                                             # the ground it lies on, or a building on that ground
            names |= {here.parcels()[pid]["name"].lower()} | {b["name"].lower() for b in here.buildings().values() if b["parcel"] == pid}
        if not low or low in names or c["of"].lower() in low:
            return cid
    return None


def do(here, mind, a) -> str:
    v = str((a or {}).get("do", "")).lower().strip()
    if v in ALIASES:                                                          # leaving, putting down and hiding are giving (D2-111)
        a = ALIASES[v](a)
        v = "give"
    if v in LIFT or (v in ("gather", "work") and str((a or {}).get("what") or "").strip().lower() in LIFT - {"lift", "check"}):
        a, v = _as_lift(a), "take"                                            # lifting snares is taking from them (brief 4c §4.4)
    try:
        if v not in VERBS:
            raise Refused(f"unknown verb {v!r}; the verbs are {', '.join(VERBS)}")
        if not verb_here(here, v):
            raise Refused(f"there is no {v} in this world")
        party = _party(here, a.get("for")) if a.get("for") and v in ("gather", "work", "make", "build", "give", "accept", "claim") else None
        drew = _drew_reset(here)
        with here.cause(v, party):
            out = HANDLERS[v](here, mind, a, party)
        return out + _drew_words(here, drew)                                   # what it took from the stores (D4-96)
    except Refused as e:
        return f"Refused: {v or 'action'}: {e}"


# ---------------------------------------------------------------------- helpers
def _qty(x, default=1.0) -> float:
    if x is None:
        return default
    try:
        q = float(x)
    except (TypeError, ValueError):
        raise Refused("qty must be a number")
    if q <= 0:
        raise Refused("qty must be positive")
    return q


def item_of(x) -> str:
    i = str(x or "").strip().lower()
    i = {"loaves": "bread", "loaf": "bread", "greens": "wild food", "food": "wild food", "weapon": "crude weapon", "tool": "crude tool",
         "tools": "crude tool", "wood": "timber", "ore": "copper ore", "hides": "hide", "stones": "stone"}.get(i, i)
    from cybertron2.engine import packs as PK
    if i not in ITEMS or not PK.on(ITEMS[i]):
        raise Refused(f"there is no such thing as {x!r} (goods: {', '.join(PK.items())})")
    return i


def _party(here, x):
    """Whom an act is done for (D2-37): a person here, or a household (its own name, or 'my household')."""
    s = str(x or "").strip()
    low = s.lower()
    if low in ("my household", "our household", "household", "home", "my house", "the house"):
        hh = here.household()
        if not hh:
            raise Refused("you belong to no household")
        return hh
    who = here.person(s)
    if who:
        return who
    for iid, h in here.households().items():
        if low in (iid.lower(), iid.lower() + "s", h["name"].lower(), h["name"].lower().removeprefix("the ")):
            return iid
    raise Refused(f"there is no one called {s!r} to act for")


def _out(here, party) -> str:
    """Where an act's output goes: one's hands, or the party's container here, if one may use it (D2-37)."""
    if party is None or party == here.name:
        return here.hands
    cid = here.party_container(party)
    if cid is None:
        if party == here.household():                                       # away from home: one carries it back oneself
            return here.hands
        raise Refused(f"work done for {party} goes into their store, and they have no house or store here, and nobody of theirs "
                      f"is here to take it: do it for yourself and carry it to them, or work where they live")      # D4-95
    return cid                                                              # putting into another's store is a gift (D4-23)


def _full_note(here, out, item, q) -> str:
    """Into a store that cannot hold it all: what went in, and that the rest lies outside its door (D2-155)."""
    if not out.startswith("stock:"):
        return ""
    bid = out[len("stock:"):]
    b = here.buildings()[bid]
    room = BL.room_for(b, here.stock(bid), item)
    if room + 1e-9 >= q:
        return ""
    return f" ({show(room)} {item} went into {b['name']}; it is full ({BL.full_words(b, here.stock(bid), item)}), and the rest lies outside its door)"


def _src(here, party, out):
    """A party's store as a source of inputs: only if one may take from it, or works for the party (D2-37, D2-38)."""
    if out == here.hands or not out.startswith("stock:"):
        return None
    return out if (here.may_take(out) or here.works_for(party)) else None


def _level(mind, tech) -> str:
    lvl = KN.level(mind, tech)
    if lvl is None:
        raise Refused(f"{KN.label(tech)} is not among your crafts: you have never learned it")
    if lvl == "aware":
        raise Refused(f"you know of {KN.label(tech)}, but have no idea how it is done (watch someone, ask to be taught, or have it explained)")
    return lvl


def _consume(here, needs: dict, mult=1.0, extra=None):
    """Take inputs from what one carries, then from stores here one may take from (or a party's, acting for it)."""
    order = [here.hands] + ([extra] if extra and extra != here.hands else []) + [c for c in here.takeable() if c not in (here.hands, extra)]
    needs = KN.pick_inputs(here, needs, mult, extra)
    for item, q in needs.items():                                            # all or nothing: check before taking any
        have = KN.available(here, item, extra=extra)
        if have + 1e-9 < q * mult:
            raise Refused(f"it needs {q * mult:g} {item}; you have {show(have)} to hand" + _short_note(here, item))
    for item, q in needs.items():
        left = round(q * mult, 6)
        for cid in order:
            if left <= 1e-9:
                break
            have = here.contents(cid).get(item, 0.0)                         # hands, a store, or what lies at its door (D4-89)
            take = min(have, left)
            if take > 1e-9:
                here.apply("destroy", src=cid, item=item, qty=take, why="used")
                if cid != here.hands:
                    _drawn(here, cid, item, take)
                left -= take
        if left > 1e-6:
            raise Refused(f"it needs {q * mult:g} {item}")


def _drawn(here, cid, item, q) -> None:
    """Who drew what from a store today, so the next one who finds it gone is told by whom (D4-95)."""
    try:
        today = here.today()
    except KeyError:                                                           # outside a day (a test, a tool): nothing to tell later
        return
    today.setdefault("drawn", []).append({"by": here.name, "cid": cid, "item": item, "qty": round(q, 2)})


def _store_name(here, cid) -> str:
    if cid.startswith("stock:"):
        return f"{here.buildings()[cid[len('stock:'):]]['name']}'s store"
    c = here.thing(cid) or {}
    door = here.buildings().get(c.get("door") or "", {}).get("name")
    return f"what lies at the door of {door}" if door else "what lies here"


def _drew_reset(here) -> int:
    """The mark in today's draws where this act starts."""
    try:
        return len(here.today().get("drawn") or [])
    except KeyError:
        return -1


def _drew_words(here, start) -> str:
    """' (from the Hearne hut's store: 10 flour, 1 timber)': what an act took from the stores rather than one's hands (D4-96)."""
    if start < 0:
        return ""
    got = {}
    for d in (here.today().get("drawn") or [])[start:]:
        if d["by"] == here.name and not d.get("taken"):
            got.setdefault(d["cid"], {}).setdefault(d["item"], 0.0)
            got[d["cid"]][d["item"]] += d["qty"]
    if not got:
        return ""
    return " (from " + "; ".join(f"{_store_name(here, c)}: " + ", ".join(f"{show(q)} {i}" for i, q in g.items()) for c, g in got.items()) + ")"


def _top_up(here, item, q) -> None:
    """Before giving from one's hands: take what is short from the stores here one may take from, as a craft does (D4-96)."""
    short = q - here.carried().get(item, 0.0)
    for cid in [c for c in here.takeable() if c != here.hands]:
        if short <= 1e-9:
            break
        take = min(short, here.contents(cid).get(item, 0.0))
        if take > 1e-9:
            here.apply("transfer", src=cid, dst=here.hands, item=item, qty=round(take, 6))
            _drawn(here, cid, item, take)
            short -= take


def _short_note(here, item) -> str:
    """Why a good is short: who else drew it from the stores one shares today, and where it comes from (D4-95)."""
    mine = set(here.takeable())
    took = {}
    try:
        drawn = here.today().get("drawn") or []
    except KeyError:
        drawn = []
    for d in drawn:
        if d["item"] == item and d["cid"] in mine and d["by"] != here.name:
            took[d["by"]] = took.get(d["by"], 0.0) + d["qty"]
    out = ""
    if took:
        out += "; " + ", ".join(f"{who} took {show(q)} from the store today" for who, q in took.items())
    src = next((t for t, d in TECHNIQUES.items() if isinstance(d.get("gives"), dict) and item in d["gives"] and d.get("inputs")), None)
    if src:                                                                    # where it comes from: the recipe that makes it
        out += f"; {item} is made by {KN.label(src)}"
    return out


def _skill_mult(here, mind, tech) -> float:
    return KN.skill(mind, tech) * here.yield_mult()                           # skill by practice (D2-52), and hunger


def _site(here, mind, tech, at, a=None):
    sites = KN.where(here, tech)
    cairn = str((a or {}).get("method", "")).lower() == "cairn"
    if (TECHNIQUES[tech].get("at") or {}).get("things") and cairn:          # a cairn over the unburied, or over a grave (D4-99)
        cid = _thing_site(here, at, graves=True)
        if cid is None:
            from cybertron2.engine import things as TH
            done = next((c for c in here.things().values() if c.get("body") and c.get("cairn")
                         and str(at or "").strip().lower() in (c["of"].lower(), here.spot_name(c).lower())), None)
            if done:
                raise Refused(f"the grave of {done['of']} already has a cairn")
            raise Refused(f"there is no body or grave here called {at!r}" if at else "there is no body or grave here")
        c = here.thing(cid)
        return "thing", cid, (f"the grave of {c['of']} at {here.spot_name(c)}" if c.get("buried") is not None
                              else f"the body of {c['of']} at {here.spot_name(c)}")
    if sites and sites[0][0] == "thing":
        kinds = _dead_kinds(tech)
        cid = _thing_site(here, at, kinds=kinds)
        what = "body or dead beast" if len(kinds) > 1 else ("dead beast" if kinds == ("carcass",) else "body")
        if cid is None:
            raise Refused(f"there is no {what} here called {at!r}" if at else f"there is no {what} here")
        return "thing", cid, next(s[2] for s in sites if s[1] == cid)
    if not sites and (TECHNIQUES[tech].get("at") or {}).get("things"):
        raise Refused("there is no dead beast lying here" if _dead_kinds(tech) == ("carcass",) else "there is no one lying unburied here")
    if at:
        key = here.parcel(at) or here.building(at)
        if key is None:
            raise Refused(f"there is no place called {at!r} here")
        where = [s for s in sites if s[0] == "parcel"]
        on = [s for s in sites if s[1] == key]
        if not on and key in here.buildings():                                # work done on the ground, named by a building on it:
            on = [s for s in where if s[1] == here.buildings()[key].get("parcel")]   # the parcel it stands on
        sites = on
        if not sites:                                                          # where here it is done, by the land (D4-95)
            names = list(dict.fromkeys(here.parcels()[s[1]]["name"] for s in where if s[1] in here.parcels()))
            raise Refused(f"{KN.label(tech)} is not done at {at}" + (f"; here it is done at {', '.join(names)}" if names else
                                                                   "; there is nowhere here for it"))
    ok = [s for s in sites if not KN.ready(here, tech, s[0], s[1], a)]
    if not ok:
        why = KN.ready(here, tech, sites[0][0], sites[0][1], a) if sites else f"there is nowhere here for {KN.label(tech)}"
        what = PC.LAND_DRAWS.get(TECHNIQUES[tech].get("draws"))
        if sites and what and sites[0][0] == "parcel" and ("picked bare" in why or "no standing timber" in why):
            PC.remember_land(mind, here.day, sites[0][1], what, "bare", "found")         # found out by trying (D4-50)
        if at and sites and sites[0][0] == "parcel":                           # one went and tried: one sees the place (D4-95)
            try:
                w_ = here.today()["worked"].setdefault(here.name, [])
                if sites[0][1] not in w_:
                    w_.append(sites[0][1])
            except KeyError:
                pass
        raise Refused(why)
    return ok[0]


def _against(here, thing) -> str:
    """Using a thing others hold or claim is allowed and seen (D4-23): the words for it."""
    mine = {here.name, here.household(), "anyone"}
    hh = here.households()
    others = sorted({hh[c["claimant"]]["name"] if c["claimant"] in hh else c["claimant"] for c in here.claims(thing)
                     if "withdrawal" in c["rights"] and c["claimant"] not in mine and c["grounds"] != "granted"})
    if not others:
        return ""
    has = "withdrawal" in here.rights(thing)
    return f" (which {' and '.join(others)} {'also claim' if has else 'hold' + ('s' if len(others) == 1 else '')})"


def _holding_people(here, holder) -> list:
    """Those a holding is whose: the holder, or its household's members (D2-172)."""
    return list(here.institution(holder)["members"]) if holder in here.households() else [holder]


def _holders_people(here, thing) -> list:
    out = []
    for c in here.claims(thing):
        if c["claimant"] in here.households():
            out += [m for m in here.institution(c["claimant"])["members"]]
        elif c["claimant"] != "anyone":
            out.append(c["claimant"])
    return out


# ---------------------------------------------------------------------- gathering and work: one handler, from the data
def _gather(here, mind, a, party):
    return _technique(here, mind, a, party, "gather")


def _work(here, mind, a, party):
    if KN.resolve(a.get("what"), "work") == "care":
        return _care(here, mind, a)
    return _technique(here, mind, a, party, "work")


def _technique(here, mind, a, party, verb):
    tech = KN.resolve(a.get("what"), verb)
    if tech is None or TECHNIQUES[tech]["verb"] != verb:
        from cybertron2.engine import packs as PK
        if "wild" in PK.CURRENT:                                               # the catalogue is not listed (D2-204 §7)
            raise Refused(f"{a.get('what')!r} is not a way of working you know; you {verb} by the ways your crafts list names")
        names = PK.techniques(verb=verb)
        raise Refused(f"{a.get('what')!r} is not something you {verb} ({verb}: {', '.join(names)})")
    tech, a = _as_modified(tech, verb, a)
    t = TECHNIQUES[tech]
    from cybertron2.engine import parties as HP
    lead = HP.member_of(here) if a.get("_party") and (t.get("yield") or {}).get("kind") == "wild_take" else None
    if not t.get("crew") and not (lead and lead != here.name):              # crew work: anyone may dig, led by one who knows how;
        _level(mind, tech)                                                  # a hunting party, led by its leader (brief 4b §3.1)
    a = {**a, "_mods": MOD.resolve(here, mind, verb, a, tech=tech)}           # ways of doing it (D2-93)
    if a["_mods"].get("lead") and (t.get("yield") or {}).get("kind") == "wild_take":   # a beast led to carry the kill (brief 4b §3.2)
        ox = here.pack_ox(a.get("lead"))
        if ox is None:
            raise Refused("to lead a pack ox on the hunt you need an ox here and a harness in your hands")
        a["_mods"] = {**a["_mods"], "_ox": ox}
    if t.get("crew") and (t.get("yield") or {}).get("kind") == "wild_take" and not lead:
        raise Refused(f"{KN.label(tech)} needs others with you: hunt with someone (\"with\": who leads), or have others hunt with you")
    kind, key, place_name = _site(here, mind, tech, a.get("at"), a)
    if kind in ("parcel", "thing"):                                           # a bear lying up by its kill there (brief 3 §3)
        from cybertron2.engine import wild as WL
        met = WL.cache_meet(here, key if kind == "parcel" else (here.thing(key) or {}).get("parcel"))
        if met:
            return met
    why = KN.shortfall(here, mind, tech, 1.0, key, a=a)
    if why:
        if kind == "parcel":                                                   # one went and tried: one sees the place (D4-95)
            w_ = here.today()["worked"].setdefault(here.name, [])
            if key not in w_:
                w_.append(key)
        raise Refused(why)
    out = _out(here, party)
    y = t["yield"]
    m = _skill_mult(here, mind, tech)
    tool, tm = here.best_tool(t["tools"]) if t.get("tools") else (None, 1.0)
    rng = here.rng("act", here.day, here.name, len(here.today()["worked"].get(here.name, [])))
    here.today()["worked"].setdefault(here.name, []).append(key)
    thing = (kind, key)
    note = _against(here, thing) if kind == "parcel" and t.get("draws") != "dead" else ""   # dead wood is anyone's (D2-158)
    got, gives, word, extra_got, suffix = 0.0, t.get("gives"), "", "", ""
    holding = None
    after = ""                                                                 # what was noticed on the way, after the outcome
    if y["kind"] == "stock":
        r = here.parcels()[key]["res"].get(t["draws"])
        if r is None or (t.get("run") and r["S"] <= (here.p["refuge"] + 0.02) * r["K"]):
            got = 0.0                                                           # no resident fish to take: only the run (Q-79 bug 1)
        else:
            got = here.apply("draw", parcel=key, key=t["draws"], qty=round(YD.dist(y, r, m, tm, refuge=here.p["refuge"],
                                                                                               b=RN.response(t["draws"], r)).sample(rng), 2))
        if t.get("run"):                                                        # a run in the water there (brief 5 §3a.2)
            from cybertron2.engine import wild as WL
            _, run_words = WL.run_take(here, mind, tech, key, int(t["units"]))
            suffix += run_words
    elif y["kind"] == "chance":
        r = here.parcels()[key]["res"][t["draws"]]
        armed = here.weapon()
        v = YD.dist(y, r, m, weapon=t["weapon"]["armed"] if armed else t["weapon"]["none"], b=RN.response(t["draws"], r)).sample(rng)
        if isinstance(v, dict):                                                 # a catch (outcomes.If took its branch)
            got = here.apply("draw", parcel=key, key=t["draws"], qty=round(v["got"], 2))
            for by, n in v["by"].items():
                if n:
                    here.apply("create", dst=out, item=by, qty=1, why=tech)
                    extra_got = f" and a {by}"
            if got > 0:                                                         # the day's kills on this ground, for its signs (D4-74)
                rec = here.parcels()[key].get("hunted") or {}
                kills = list(rec.get("kills") or []) if rec.get("day") == here.day else []
                kills.append({"by": here.name, "meat": got, "hide": bool(extra_got)})
                here.apply("set", ref=("parcel", key), field="hunted", value={"day": here.day, "kills": kills})
        if armed and t.get("wear"):
            here.apply("wear", container=here.hands, item=armed, uses=t["wear"])
    elif y["kind"] == "fixed":
        q = YD.dist(y, None, m, tm).sample(rng)
        if t.get("by_season"):                                                  # what the season gives (D4-106), never refused
            q *= float(t["by_season"].get(here.calendar()["season"], 1.0))
        got = here.apply("draw", parcel=key, key=t["draws"], qty=round(q, 2)) if t["draws"] in here.parcels()[key]["res"] and \
            here.parcels()[key]["res"][t["draws"]]["K"] > 0 and RN.of(t["draws"], here.parcels()[key]["res"][t["draws"]]) != "endless" else round(q, 2)
        if tech == "fell" and got > 0:                                         # its branches left as dead wood (D2-156)
            here.apply("add_res", parcel=key, key="dead", qty=got)
    elif y["kind"] == "clear":                                                # new ground for a field (CLEARING)
        word = _clear(here, key, place_name, m * tm, party)
    elif y["kind"] == "pool":                                                 # dead wood: less to find as it thins (D2-156)
        r = here.parcels()[key]["res"][t["draws"]]
        got = here.apply("draw", parcel=key, key=t["draws"], qty=round(YD.dist(y, r, m).sample(rng), 2))
    elif y["kind"] in FM_KINDS:                                                 # farming and cattle (farm.py)
        got, g, word, thing = FM.act(here, mind, tech, key, place_name, out, m, tm, a)
        gives = g or gives
        note = _against(here, thing) if thing[0] in ("parcel", "herd") else note
        if "_on" in a and FM.named(here.parcels()[key]):                       # a field held in shares: whose plots (D2-172)
            note = FM.against(here, key, a["_on"])
            holding = a["_on"]
        if word and not word.startswith("You"):
            suffix, word = word, ""                                             # a note to the plain result, below
    elif y["kind"] == "bury":                                                 # D2-96; a grave dug by many, over days (D4-99)
        word = _bury(here, key, "method: cairn" in a["_mods"]["_used"], a)
        c = here.thing(key)
        thing = ("parcel", c["parcel"]) if c.get("parcel") else thing
    elif y["kind"] == "burn":                                                 # a carcass burned (brief 3 §4)
        word = _burn(here, key)
        c = here.thing(key)
        thing = ("parcel", c["parcel"]) if c.get("parcel") else thing
    elif y["kind"] == "mend":                                                # a worn fitting set right (D4-103 phase 2)
        from cybertron2.engine import wear as WE
        need = y.get("inputs") or {}
        short = {i: q for i, q in need.items() if here.carried().get(i, 0.0) + 1e-9 < q}
        if short:
            raise Refused(f"{KN.label(tech)} takes " + ", ".join(f"{q:g} {i}" for i, q in need.items()) + " in hand")
        for i, q in need.items():
            here.apply("destroy", src=here.hands, item=i, qty=q, why=tech)
        word = f"You worked on the {y['fitting']} at {place_name}: {WE.mend(here, key, y['fitting'])}."
    elif y["kind"] == "smoke_tend":                                          # a smokehouse's fire, once a day (brief 5 §4a.3)
        from cybertron2.engine import keeping as KP
        word = KP.tend(here, key, place_name)
        thing = ("building", key)
    elif y["kind"] == "repair":                                              # by its size and structure (D2-168)
        if here.buildings()[key]["structure"] == "stone":
            _mason(mind)                                                       # mending stone is walling (D4-97)
        word = _repair(here, key, m)
        thing = ("building", key)
    elif y["kind"] == "wild_take" and t.get("set"):                           # set and left: it catches by night (brief 2 §4)
        from cybertron2.engine import wild as WL
        mine = _own_set_at(here, tech, key)
        if mine:                                                               # named alone, one's own standing: tended (u2 §6 fault 2)
            word = _tend(here, mind, mine, place_name)
        else:
            word = WL.set_work(here, mind, tech, key, place_name)
        gives = None
    elif y["kind"] == "wild_take" and lead:                                  # a party's hunt: settled after the day's acts (4b §3.1)
        word = HP.record(here, mind, tech, key, place_name, out, m, a)
        gives = None
    elif y["kind"] == "wild_take":                                           # a hunt in the wild layer (wild_layer.md, D2-199)
        from cybertron2.engine import wild as WL
        _, word, after = WL.take(here, mind, tech, key, place_name, out, m, y, a)
        gives = None                                                            # its goods are made by the hunt, by kind
    elif y["kind"] == "wild_den":                                            # den work: a den's take or a lodge's trap (D2-204)
        from cybertron2.engine import wild as WL
        _, word, after = WL.den_work(here, mind, tech, key, place_name, out, m, y, a)
        gives = None
    elif y["kind"] == "wild_young":                                          # gather young: a colony's (D2-204)
        from cybertron2.engine import wild as WL
        word = WL.young(here, key, place_name, m * tm)
    elif y["kind"] == "wild_pest":                                           # pest work: the pest named, else the worst (D2-204)
        from cybertron2.engine import wild as WL
        word = WL.pest(here, key, place_name, a)
    elif y["kind"] == "wild_forage":                                         # wild plants in season (D2-200, D2-201)
        from cybertron2.engine import wild as WL
        got, word = WL.forage(here, mind, tech, key, place_name, out, m * tm, y, a)
        gives = None
    elif y["kind"] == "wild_site":                                           # a heronry, rookery or lodge (wave 5)
        from cybertron2.engine import wild as WL
        word = WL.site_work(here, key, y, place_name, m * tm)
    elif y["kind"] == "wild_shut":                                           # hens shut in for the night (wild_layer.md, wave 2)
        from cybertron2.engine import wild as WL
        word = WL.shut(here)
    elif y["kind"] == "wild_guard":                                          # a guard on a field against a load (wave 3)
        from cybertron2.engine import wild as WL
        word = WL.guard(here, key, y, place_name)
    elif y["kind"] == "wild_watch":                                          # a night watch over a field (wild_layer.md, D2-199)
        from cybertron2.engine import wild as WL
        word = WL.watch(here, key, y, place_name, a)
    elif y["kind"] == "clear_built":                                          # new ground for building (02zh §8)
        word = _clear_built(here, key, place_name, m * tm, party)
    what = PC.LAND_DRAWS.get(t.get("draws")) if kind == "parcel" and y["kind"] in ("stock", "chance") else None
    if what:                                                                    # what working it showed of the place (D4-50)
        if y["kind"] == "chance":
            PC.remember_land(mind, here.day, key, what, "good" if got > 0 else "nothing caught", "found")
        else:
            PC.remember_land(mind, here.day, key, what, "thin" if got < 0.5 * y["base"] else "good", "found")
    if got > 0 and gives:
        suffix = _full_note(here, out, gives, got) + suffix
        here.apply("create", dst=out, item=gives, qty=got, why=tech)
    if tool and t.get("wear"):
        here.apply("wear", container=here.hands, item=tool, uses=t["wear"])
    if not (y["kind"] in ("wild_take", "wild_den") and not t.get("set")):   # a hunt is practised by how it went (wild.practise, 4c §3.3)
        KN.tried(here, mind, tech, got > 0 or y["kind"] in ("sow", "tend", "repair", "slaughter", "break", "manure", "herd", "bury", "fence",
                                                           "gate", "wild_watch", "wild_take", "wild_shut", "wild_guard", "wild_forage", "smoke_tend",
                                                           "wild_site", "wild_young", "wild_pest"),
                 units=t["units"])
    MOD.practise(here, mind, a["_mods"])
    for_txt = f" for {here.households()[party]['name'] if party in here.households() else party}" if party and party != here.name else ""
    text = f"{here.name} was {KN.label(tech)} at {place_name}{for_txt}{note}"
    here.event("work", text, actor=here.name, about=[f"{thing[0]}:{thing[1]}"], salience=0.35 if note else 0.15, tags=t["tags"],
               tech=tech, concerns=(_holding_people(here, holding) if holding is not None else _holders_people(here, thing)) if note else [],
               **({"holding": holding} if holding is not None else {}))
    here.record(verb, tech, party, site=key)
    if kind == "parcel":                                                      # what the work showed of the wild about it (02zq)
        from cybertron2.engine import wild as WL
        after += WL.work_notices(here, mind, tech, key)
    if word:
        if y["kind"] == "slaughter":                                          # where the meat and hide went (D4-70)
            word = word.rstrip(".") + (" (now in your hands)." if out == here.hands else
                                       f" (put into {here.buildings()[out[len('stock:'):]]['name']})." if out.startswith("stock:") else ".")
        return (word if not for_txt else word.rstrip(".") + for_txt + ".") + after
    if y["kind"] == "chance" and got <= 0:
        return f"You hunted in {place_name}{note} and caught nothing{extra_got}." + after
    if y["kind"] == "stock" and t.get("run") and got <= 0 and suffix:            # only the run gave (Q-79 bug 1)
        return f"You fished at {place_name}{note}: the water's own fish gave nothing.{suffix}" + after
    via = f" with your {tool}" if tool else (" with your bare hands" if t.get("tools") else "")
    dest = "" if out == here.hands else f" into {here.buildings()[out[len('stock:'):]]['name']}" if out.startswith("stock:") else f" to {party}"
    return (f"You {verb}ed {show(got)} {gives}{extra_got} at {place_name}{note}{via}{dest}.{suffix}".replace("You gathered", "You took")
            .replace("You worked", "You got")) + after


# ---------------------------------------------------------------------- making
BATCH_LEAST = 0.1        # the least of a batch's inputs worth hanging (38.75: "0.0286 drying meat" held a rack 3 nights; calibrate)


def _make(here, mind, a, party):
    tech = KN.resolve(a.get("what"), "make")
    if tech is None or TECHNIQUES[tech]["verb"] != "make":
        from cybertron2.engine import packs as PK
        names = PK.techniques(verb="make")
        raise Refused(f"{a.get('what')!r} is not something you make (recipes: {', '.join(names)})")
    lvl = _level(mind, tech)
    t = TECHNIQUES[tech]
    out = _out(here, party)
    extra = _src(here, party, out)
    qty = max(1, int(_qty(a.get("qty"), 1)))
    res = []
    from cybertron2.engine import wear as WE
    fits = WE.worked((t.get("at") or {}).get("fittings") or [])
    for i in range(qty):
        sites = KN.where(here, tech)                                           # one's own house's fitting first, of those
        sites = [x for x in sites if not KN.ready(here, tech, x[0], x[1])] or sites   # ready (racks with room: brief 5 §4a)
        site = sorted(sites, key=lambda x: (x[0] != "building" or x[1] not in here.homes_here(),
                                            x[0] != "building" or not here.may_take(here.buildings()[x[1]]["stock"])))[0] if sites else None
        b = here.buildings().get(site[1]) if site and site[0] == "building" else None
        fac = WE.factor(here.p, b, fits, here.day, here.year_days()) if fits else 1.0    # a worn fitting works at half (D4-103)
        worn_fac = fac
        if b is not None and "water wheel" in fits:                            # its gap open: the head of water lost (brief 5 §3a)
            from cybertron2.engine import wild as WL
            fac *= here.mill_rate(b)
        mult = TRY[lvl]["inputs"] if fac == 1.0 else TRY[lvl]["inputs"] * fac
        why = KN.shortfall(here, mind, tech, mult, extra=extra)
        if why:
            res.append(f"Refused: make {tech}: {why}")
            break
        share = KN.batch_share(here, tech, mult, extra)                        # whatever one has, up to the batch (brief 4c §6.1)
        if t.get("rack") and b is not None:                                    # as much as the racks there have room for (5 §4a)
            share = min(share, here.rack_room(site[1], tech) / max(1e-12, sum(float(q) for q in t["gives"].values())))
        if t.get("batch"):                                                     # not a batch of almost nothing (38.75): a hare's
            ins = {i: float(q) * mult * share for i, q in (t.get("inputs") or {}).items() if isinstance(q, (int, float))}
            if ins and sum(ins.values()) < float(BATCH_LEAST) - 1e-9:          # meat (0.7) still hangs (brief 4c §6.1)
                have = ", ".join(f"{round(q, 2):g} {i}" for i, q in ins.items())
                res.append(f"Refused: make {tech}: there is too little to make a batch ({have}): it takes at least {BATCH_LEAST:g}")
                break
        _consume(here, t.get("inputs") or {}, mult * share, extra)
        if b is not None and fits and WE.on(here.p):
            WE.use(here, site[1], fits, sum(v for v in (t.get("inputs") or {}).values() if isinstance(v, (int, float))) * fac * share)
        ok = here.rng("make", here.day, here.name, tech, i).random() < TRY[lvl]["chance"]
        rose = KN.tried(here, mind, tech, ok, units=t["units"])
        if ok:
            full = ""
            gives = {item: (q if fac == 1.0 else round(q * fac, 2)) for item, q in t["gives"].items()}
            if share < 1.0:
                gives = {item: round(q * share, 4) for item, q in gives.items()}
            rk = t.get("rack")
            if rk and b is not None:                                           # hung on a rack at the fire, for its nights (brief 4 §5)
                house = bool(rk.get("tended"))                                 # a smokehouse's racks: nights of a tended fire (5 §4a)
                smoke = house or bool((b.get("fittings") or {}).get("hearth"))   # at a hearth: inside, in its smoke (brief 4c §6.2)
                dst = here.apply("new_thing", node=here.node, parcel=b["parcel"], kind="pile", by=here.name,
                                 **({"in": site[1]} if smoke else {"door": site[1]}),
                                 rack={"day": here.day, "nights": int(rk["nights"]), "into": rk["into"], "ratio": float(rk["ratio"]),
                                       "smoke": smoke, **({"smokehouse": True, "lit": 0} if house else {})})
                if site[1] not in here.homes_here():                           # one's own house is known without it (4c §6.4)
                    here.remember_thing(dst, "put")
                for item, q in gives.items():
                    here.apply("create", dst=dst, item=item, qty=q, why=tech)
                if house:
                    from cybertron2.engine import keeping as KP
                    KP.light(here, site[1])                                    # hung and the fire lit: it burns tonight
                    n = here.smoke_fuel_nights(site[1])
                    full = (f"; it hangs on the smoke racks in {b['name']} for {int(rk['nights'])} nights of fire, the fire lit for tonight "
                            "and to be tended each day after (tend the smoke), or the batch waits and spoils"
                            + (f"; firewood there for {n} night{'s' if n != 1 else ''}" if n else
                               "; but there is no firewood in it or at its door: the fire will die tonight unless some is brought"))
                else:
                    full = (f"; it hangs on the rack in the smoke of the hearth inside {b['name']} for {int(rk['nights'])} nights" if smoke else
                            f"; it hangs on a rack by the fire outside {b['name']} for {int(rk['nights'])} nights")
            for item, q in ({} if rk and b is not None else gives).items():
                full += _full_note(here, out, item, q)
                here.apply("create", dst=out, item=item, qty=q, why=tech)
            if b is not None and any(FITTINGS.get(f, {}).get("spring") for f in fits):   # the pan's rim, for its signs (5 §4b.5)
                here.apply("set", ref=("building", site[1]), field="boiled", value=here.day)
            worn = (" (" + WE.worn_words(here.p, b, fits, here.day, here.year_days()) + ")") if worn_fac < 1.0 else ""
            if fac < worn_fac:
                worn += " (the mill's gap is open: the water runs past, and the wheel turns slow)"
            if t.get("animals"):                                               # others' beasts: allowed and seen (D4-114)
                worn += FM.beasts_note(here, t)
            res.append(f"You made {', '.join(f'{round(q, 2):g} {it}' for it, q in gives.items())}" + (f" at {site[2]}" if site and site[1] else "") + worn
                       + full + "." + (f" (You are now {rose} at it.)" if rose else ""))
        else:
            res.append(f"Your try at {KN.label(tech)} failed and the materials are spoilt." + (f" (You are now {rose} at it.)" if rose else ""))
        here.event("make", f"{here.name} was {KN.label(tech)}" + ("" if ok else ", and it went wrong"), actor=here.name,
                   about=[f"{site[0]}:{site[1]}"] if site[0] in ("building", "parcel") else [], salience=0.2, tags=t["tags"], tech=tech)
        here.record("make", tech, party)
    return " ".join(res)


# ---------------------------------------------------------------------- building (D2-9, recipes.md §3; review 02zh, D2-154 to D2-171)
STRUCTURE_WORDS = {"wattle": "wattle", "wattle and daub": "wattle", "timber": "timber", "wood": "timber", "wooden": "timber",
                   "stone": "stone", "masonry": "stone"}
MONUMENT_ALIAS = {x: k for k, d in MONUMENTS.items() for x in [k] + d.get("aliases", [])}
UPGRADE = ("upgrade", "rebuild", "raise", "improve")


def _mason(mind):
    """Building in stone is stone walling (D2-3, D4-97): stone rooms, storeys and upgrades, mending stone, carving in stone, and a
    mason's fitting one has not learned itself; the level is one's walling."""
    lv = KN.level(mind, "wall")
    if lv not in ("rough", "capable", "known"):
        raise Refused("building in stone is stone walling, a mason's craft you have not learned (watch a mason, be taught, or have it "
                      "explained)")
    return lv


def _lvl_for(mind, tech, structure=None):
    """The level one works at: in stone, as a mason; a mason's fitting or monument by that craft, or else as a mason; otherwise
    the technique itself (a carpenter's for a timber medium room or hall)."""
    if structure == "stone":
        return _mason(mind)
    if TECHNIQUES.get(tech, {}).get("trade") == "mason":
        lv = KN.level(mind, tech)
        return lv if lv in ("rough", "capable", "known") else _mason(mind)
    return _level(mind, tech)


def _how(here, mind, a):
    if str(a.get("how") or "").strip().lower() in ("plain", "none", ""):
        a = {k: v for k, v in a.items() if k != "how"}
    mods = MOD.resolve(here, mind, "build", a)
    return mods.get("tier") or "plain", mods


def _ground_check(here, pid, need, what):
    par = here.parcels()[pid]
    total = BL.ground_total(par)
    if total <= 0:
        raise Refused(f"{par['name']} is {par['cover']}, not ground for building: build on built ground or scrub, or clear it first "
                      "(work clear for building)")
    free = BL.ground_free(pid, par, here.buildings())
    if free < need:
        raise Refused(f"there is no room left to build on {par['name']}: {total - free} of its {total} spaces are taken, and {what} "
                      f"needs {need} (build up in stone, build elsewhere, or clear more ground)")


def _build(here, mind, a, party):
    what = str(a.get("what") or "").strip().lower()
    what = MONUMENT_ALIAS.get(what, what)
    if what not in BLUEPRINTS and what not in FITTINGS and what not in MONUMENTS:
        from cybertron2.engine.data import FITTING_ALIAS
        what = FITTING_ALIAS.get(what, what)                                  # "salt pan": the brine pan (brief 5 §4b)
    if what in UPGRADE:
        return _upgrade(here, mind, a, party)
    if what in WEIR_PARTS:                                                     # a weir's further section or a stone footing (D2-210)
        return _weir_part(here, mind, a, party, WEIR_PARTS[what])
    if what in ("storey", "upper storey", "second storey", "third storey"):
        what = str(a.get("room") or "small room").strip().lower()
        a = {**a, "storey": a.get("storey") or (3 if "third" in str(a.get("what")) else 2)}
    if what not in BLUEPRINTS and what not in FITTINGS and what not in MONUMENTS:
        raise Refused(f"{a.get('what')!r} is not something you build (rooms: {', '.join(r for r in BLUEPRINTS)}; fittings: "
                      f"{', '.join(FITTINGS)}; monuments: {', '.join(MONUMENTS)}; or upgrade a building)")
    owner = party or here.name
    at = a.get("at")
    if what in BLUEPRINTS or what in MONUMENTS:
        bid = here.building(at) if at else None
        if bid and here.buildings()[bid].get("unfinished"):                      # carry on
            u = here.buildings()[bid]["unfinished"]
            if here.name in (here.buildings()[bid].get("crew") or []):           # crew work, led by one who knows it (u2 §6 bug 4)
                return _build_work(here, mind, bid, KN.level(mind, u["blueprint"]) or "rough")
            return _build_work(here, mind, bid, _lvl_for(mind, u["blueprint"], here.buildings()[bid]["structure"]))
        if bid and what in BLUEPRINTS and what != "camp":
            return _add_room(here, mind, a, party, bid, what)
        if bid:
            raise Refused(f"{at} is a building: say a place on built ground or scrub here to put up a new one")
        pid = here.parcel(at) if at else None
        if pid is None:
            lots = [p for p, x in here.parcels().items() if BL.ground_total(x) > 0]
            raise Refused(f"say where to build: a place on built ground or scrub here ({', '.join(here.parcels()[p]['name'] for p in lots) or 'none'})"
                          " or, to add a room, a building here")
        if what in MONUMENTS:
            return _monument(here, mind, a, party, pid, what)
        return _new_building(here, mind, a, party, pid, what, owner)
    return _fitting(here, mind, a, party, what)


def _new_building(here, mind, a, party, pid, what, owner):
    bp = BLUEPRINTS[what]
    par = here.parcels()[pid]
    who = here.households()[party]['name'] if party in here.households() else here.name
    if bp.get("structure") == "camp":                                        # a camp goes up anywhere but on water (D2-68)
        lvl = _level(mind, what)
        if par["cover"] == "water":
            raise Refused("you cannot camp on water")
        if BL.ground_total(par) > 0 and BL.ground_free(pid, par, here.buildings()) < int(SPACE["camp_floor"]):
            raise Refused(f"there is no room left to camp on {par['name']}")
        from cybertron2.engine.data import PHYSICS
        mats = dict(PHYSICS["wear"]["camp_build"]) if here.levels_on() else bp["materials"]   # cheap in levels (brief 4 §3)
        _consume(here, mats, TRY[lvl]["inputs"], here.party_container(party) if party else None)
        name = str(a.get("name") or "").strip()[:40] or f"{who}'s camp on {par['name']}"
        bid = here.apply("raise", node=here.node, parcel=pid, rec={"name": name, "structure": "camp", "fittings": {},
                                                                     "unfinished": {"blueprint": what, "units_left": bp["units"]}})
        here.apply("claim", thing=("building", bid), claimant=owner, rights="all", grounds="built")
        here.event("build", f"{here.name} began building {bp['label']} on {par['name']}", actor=here.name, about=[f"building:{bid}"],
                   salience=0.5, tags=["building"])
        return _build_work(here, mind, bid, lvl, started=True)
    structure = STRUCTURE_WORDS.get(str(a.get("structure") or bp["structure"]).strip().lower())
    if structure is None:
        raise Refused(f"a building is wattle, timber or stone, not {a.get('structure')!r}")
    if structure not in ROOMS[what]:
        raise Refused(f"a {what} is too large for wattle: build it in timber (on a stone footing) or in stone")
    how, mods = _how(here, mind, a)
    lvl = _lvl_for(mind, what, structure)
    floor = int(ROOMS[what]["floor"])
    _ground_check(here, pid, floor, f"a {what}")
    cost = BL.room_cost(what, structure, how=how)
    _consume(here, cost["materials"], TRY[lvl]["inputs"], here.party_container(party) if party else None)
    name = str(a.get("name") or "").strip()[:40] or f"{who}'s new house"
    rec = {"name": name, "structure": structure, "fittings": {}, "tier": how, "rooms": [{"kind": what, "floor": floor, "storey": 1}],
           "unfinished": {"blueprint": what, "units_left": cost["units"]}}
    bid = here.apply("raise", node=here.node, parcel=pid, rec=rec)
    if a.get("describe"):                                                     # the description, written with the build (D2-169)
        here.apply("set", ref=("building", bid), field="description",
                   value={"text": BL.cap_text(a["describe"], "description"), "by": here.name, "day": here.day})
    here.apply("claim", thing=("building", bid), claimant=owner, rights="all", grounds="built")
    tw = TIERS[how]["words"]
    here.event("build", f"{here.name} began building a {what} in {structure}" + (f", {tw}" if tw and how != "grand" else
                                                                                      (", on a grand scale" if how == "grand" else ""))
               + f", on {par['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.5, tags=["building"])
    MOD.practise(here, mind, mods)
    return _build_work(here, mind, bid, lvl, started=True)


def _monument(here, mind, a, party, pid, what):
    d = MONUMENTS[what]
    par = here.parcels()[pid]
    crew = []
    if d.get("site") == "river":                                              # a weir: across a river, by a declared crew (brief 5 §3)
        from cybertron2.engine import parties as PT, wild as WL
        if not here.river_parcel(pid):
            raise Refused(f"{d['label'][2:]} is built across a river: at a place of water on a river here")
        if any(WL.is_weir(b) and b["parcel"] == pid for b in here.buildings().values()):
            raise Refused(f"there is a weir across {par['name']} already")
        for x in PT._names(a.get("with")):
            n_ = here.person(x)                                            # a living person here (at the node)
            if n_ and n_ != here.name and n_ not in crew:
                crew.append(n_)
        if len(crew) + 1 < int(d.get("crew", 1)):
            raise Refused(f"{d['label'][2:]} is crew work: name who builds it with you (\"with\": one or more people here)")
    elif par["cover"] == "water":
        raise Refused("a monument cannot stand in water")
    how, mods = _how(here, mind, a)
    lvl = _lvl_for(mind, what)
    if BL.ground_total(par) > 0:
        _ground_check(here, pid, int(SPACE["monument_ground"]), d["label"])
    t = TIERS[how]
    mats, units, first = dict(d["materials"]), float(d["units"]), None
    if d.get("site") == "river" and (a.get("structure") or a.get("material")):  # a weir's first section in either material (W-69)
        from cybertron2.wild import gear as GR
        first = STRUCTURE_WORDS.get(str(a.get("structure") or a.get("material")).strip().lower())
        if first not in GR.MATERIALS:
            raise Refused(f"a weir's section is wattle or timber, not {a.get('structure') or a.get('material')!r}")
        c = GR.cost(0, first)
        mats, units = c["materials"], float(c["units"])
    _consume(here, {i: q * float(t["materials"]) for i, q in mats.items()}, TRY[lvl]["inputs"],
             here.party_container(party) if party else None)
    name = str(a.get("name") or "").strip()[:40] or f"the {what} on {par['name']}"
    bid = here.apply("raise", node=here.node, parcel=pid, rec={"name": name, "structure": d["structure"], "fittings": {}, "rooms": [],
                                                                 "monument": what, "tier": how,
                                                                 "unfinished": {"blueprint": what, "units_left": units * float(t["work"])},
                                                                 **({"crew": [here.name] + crew, "gap": "shut"} if d.get("site") == "river" else {}),
                                                                 **({"sections": [{"m": first, "foot": False, "level": 5}]}
                                                                    if first and first != "wattle" else {})})
    if a.get("describe"):
        here.apply("set", ref=("building", bid), field="description",
                   value={"text": BL.cap_text(a["describe"], "description"), "by": here.name, "day": here.day})
    here.apply("claim", thing=("building", bid), claimant=party or here.name, rights="all", grounds="built")
    here.event("build", f"{here.name} began raising {d['label']} on {par['name']}", actor=here.name, about=[f"building:{bid}"],
               salience=0.5, tags=["building"])
    MOD.practise(here, mind, mods)
    return _build_work(here, mind, bid, lvl, started=True)


def _usable(here, bid):
    b = here.buildings()[bid]
    if b.get("unfinished"):
        raise Refused(f"{b['name']} is not finished")
    if not here.can_enter(bid):
        raise Refused(f"you cannot get into {b['name']}")
    return b


def _add_room(here, mind, a, party, bid, what):
    """A room added to a building: a quarter less (D2-154); on an upper storey in stone only, at 1.5 and 2 times (D2-3)."""
    b = _usable(here, bid)
    if b.get("monument"):
        raise Refused(f"{b['name']} is a monument: it has no rooms")
    if b["structure"] == "camp":
        raise Refused(f"{b['name']} is a camp: build a house to add rooms to")
    storey = max(1, int(_qty(a.get("storey"), 1)))
    wk = b.get("works")
    if wk:
        if wk.get("kind") == "room" and wk.get("room") == what and int(wk.get("storey", 1)) == storey:
            return _works_progress(here, mind, bid)
        raise Refused(f"{_works_words(wk)} is under way at {b['name']}: finish it first")
    if what not in ROOMS or b["structure"] not in ROOMS[what]:
        raise Refused(f"a {what} is too large for a wattle building: upgrade {b['name']} to timber or stone first")
    floor = int(ROOMS[what]["floor"])
    if storey > 1:
        if b["structure"] != "stone":
            raise Refused(f"only a stone building takes an upper storey (D2-3): {b['name']} is {b['structure']}; upgrade it to stone first")
        if storey > max(SPACE["storeys"]):
            raise Refused(f"a building stands at most {max(SPACE['storeys'])} storeys")
        below = BL.floor(b, storey - 1)
        if BL.floor(b, storey) + floor > below:
            raise Refused(f"storey {storey} of {b['name']} can hold no more floor than the one below it ({below} spaces; "
                          f"{BL.floor(b, storey)} built)")
    else:
        _ground_check(here, b["parcel"], floor, f"a {what}")
    how = BL.tier(b)
    lvl = _lvl_for(mind, what, b["structure"])
    cost = BL.room_cost(what, b["structure"], added=True, storey=storey, how=how)
    _consume(here, cost["materials"], TRY[lvl]["inputs"], b["stock"] if here.may_take(b["stock"]) else
             (here.party_container(party) if party else None))
    here.apply("set", ref=("building", bid), field="works", value={"kind": "room", "room": what, "floor": floor, "storey": storey,
                                                                     "units_left": cost["units"], "tech": what, "by": here.name})
    here.record("build", what, party)
    return _works_progress(here, mind, bid, started=True)


def _upgrade(here, mind, a, party):
    """A building's structure raised (wattle to timber, timber to stone), or its tier raised by the difference (02zh §2, D2-171)."""
    at = a.get("at")
    bid = here.building(at) if at else (here.homes_here() or [None])[0]
    if bid is None:
        raise Refused("say which building here to upgrade (\"at\")")
    b = _usable(here, bid)
    if b["structure"] == "camp":
        raise Refused(f"{b['name']} is a camp: it cannot be rebuilt")
    wk = b.get("works")
    to = STRUCTURE_WORDS.get(str(a.get("to") or a.get("structure") or "").strip().lower())
    how = str(a.get("how") or "").strip().lower() or None
    if wk:
        if wk.get("kind") in ("upgrade", "tier"):
            return _works_progress(here, mind, bid)
        raise Refused(f"{_works_words(wk)} is under way at {b['name']}: finish it first")
    if to and how:
        raise Refused("one thing at a time: a new structure (\"to\") or a finer tier (\"how\")")
    if how:
        mods = MOD.resolve(here, mind, "build", a)
        how = mods.get("tier") or how
        if how not in TIERS or not BL.tier_up(how, BL.tier(b)):
            raise Refused(f"{b['name']} is already {BL.tier(b)}; it can be raised to " +
                          (", ".join(t for t in TIERS if BL.tier_up(t, BL.tier(b))) or "nothing finer"))
        cost = BL.tier_cost(b, how)
        tech = b.get("monument") or (b["rooms"][0]["kind"] if b.get("rooms") else "small room")
        lvl = _lvl_for(mind, tech, b["structure"] if b["structure"] == "stone" else None)
        _consume(here, cost["materials"], TRY[lvl]["inputs"], b["stock"] if here.may_take(b["stock"]) else None)
        here.apply("set", ref=("building", bid), field="works", value={"kind": "tier", "to": how, "units_left": cost["units"],
                                                                         "tech": tech, "by": here.name})
        here.record("build", "upgrade", party)
        return _works_progress(here, mind, bid, started=True)
    if b.get("monument") == "weir" and to == "timber":                       # a weir's wattle section rebuilt in timber (W-69)
        return _weir_part(here, mind, a, party, "upgrade")
    if b.get("monument"):
        raise Refused(f"{b['name']} is a monument: raise its tier (\"how\") instead")
    order = SPACE["order"]
    if to is None:
        nxt = order[order.index(b["structure"]) + 1] if b["structure"] in order[:-1] else None
        raise Refused(f"say what to upgrade {b['name']} to: \"to\": " + (nxt or "nothing: it is stone already")
                      + "; or \"how\": fine, rich or grand")
    if order.index(to) <= order.index(b["structure"]):
        raise Refused(f"{b['name']} is {b['structure']} already")
    cost = BL.upgrade_cost(b, to)
    big = next((r["kind"] for r in b["rooms"] if r["kind"] in ("hall", "medium room")), "small room")
    lvl = _mason(mind) if to == "stone" else _level(mind, big)
    _consume(here, cost["materials"], TRY[lvl]["inputs"], b["stock"] if here.may_take(b["stock"]) else None)
    here.apply("set", ref=("building", bid), field="works", value={"kind": "upgrade", "to": to, "units_left": cost["units"],
                                                                     "tech": big, "by": here.name})
    here.record("build", "upgrade", party)
    return _works_progress(here, mind, bid, started=True)


def _works_words(wk) -> str:
    if wk["kind"] == "room":
        return f"a {wk['room']}" + (f" on storey {wk['storey']}" if int(wk.get("storey", 1)) > 1 else "")
    if wk["kind"] == "upgrade":
        return f"rebuilding in {wk['to']}"
    return f"work to make it {TIERS[wk['to']]['words']}"


# a weir's parts (D2-210; W-69): a further section (timber unless "structure" says wattle; "wattle section" one of wattle), a stone
# footing under the next section without one, or the first wattle section rebuilt in timber for the difference
WEIR_PARTS = {"weir section": "section", "a weir section": "section", "timber section": "timber", "section": "section",
              "another section": "section", "wattle section": "wattle", "a wattle section": "wattle", "a timber section": "timber",
              "weir footing": "footing", "stone footing": "footing", "footing": "footing", "a stone footing": "footing",
              "section upgrade": "upgrade", "upgrade section": "upgrade", "upgrade a section": "upgrade", "weir upgrade": "upgrade",
              "upgrade the weir": "upgrade", "timber upgrade": "upgrade", "rebuild a section in timber": "upgrade"}
WEIR_PART_WORDS = {"timber": "a timber section", "wattle": "a wattle section", "footing": "a stone footing",
                   "upgrade": "a section rebuilt in timber"}


def _weir_part(here, mind, a, party, part):
    """Adding to a weir (D2-210; wild/gear.py, W-69): its materials when the part is begun, then its work, two units an action (more
    with skill), by anyone who builds at it: a further section of wattle or timber (up to `most` added), a stone footing for the next
    section without one, or the first wattle section rebuilt in timber, for the difference of the two materials (its level kept).
    A part begun is finished before another is begun."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import gear as GR
    bid = here.building(a.get("at")) if a.get("at") else None
    if bid is None:
        bid = next((x for x, b in sorted(here.buildings().items()) if WL.is_weir(b) and not b.get("unfinished")), None)
    b = here.buildings().get(bid) if bid else None
    if b is None or not WL.is_weir(b) or b.get("unfinished"):
        raise Refused("say which weir here to add to (\"at\": the weir)")
    if part == "section":
        part = STRUCTURE_WORDS.get(str(a.get("structure") or a.get("material") or "timber").strip().lower())
        if part not in GR.MATERIALS:
            raise Refused(f"a weir's section is wattle or timber, not {a.get('structure') or a.get('material')!r}")
    if here.name not in (b.get("crew") or []):                                # its crew works on it under one who knows it (bug 4)
        _level(mind, "weir")
    wk = dict(b.get("weir_work") or {})
    secs = WL.sections(b)
    if not wk:
        if part in GR.MATERIALS:
            if len(secs) - 1 >= GR.most_added():
                raise Refused(f"{b['name']} has all its sections: {len(secs)}")
            c = GR.cost(len(secs), part)
        elif part == "footing":
            if all(sc.get("foot") for sc in secs):
                raise Refused(f"every section of {b['name']} stands on a stone footing")
            from cybertron2.engine.data import WATER_WORKS
            c = {"materials": WATER_WORKS["weir"]["footing"]["materials"], "units": WATER_WORKS["weir"]["footing"]["units"]}
        else:
            if not any(sc["m"] == "wattle" for sc in secs):
                raise Refused(f"every section of {b['name']} is timber already")
            c = GR.upgrade_cost("wattle", "timber")
        _consume(here, c["materials"], 1.0, here.party_container(party) if party else None)
        wk = {"part": part, "units_left": float(c["units"])}
    elif wk["part"] != part:
        raise Refused(f"{b['name']} has {WEIR_PART_WORDS.get(wk['part'], 'a part')} under way: finish that first")
    _at_work(here, bid)
    wk["units_left"] = round(max(0.0, float(wk["units_left"]) - 2 * KN.skill(mind, "weir") * here.yield_mult()), 2)
    what = WEIR_PART_WORDS[part]
    if wk["units_left"] > 1e-9:
        here.apply("set", ref=("building", bid), field="weir_work", value=wk)
        here.event("build", f"{here.name} was working on {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.2,
                   tags=["building"])
        return f"You worked on {what} for {b['name']}: about {show(wk['units_left'])} units of work left."
    here.apply("set", ref=("building", bid), field="weir_work", value=None)
    if part in GR.MATERIALS:
        secs.append({"m": part, "foot": False, "level": 5})
    elif part == "footing":
        next(sc for sc in secs if not sc.get("foot"))["foot"] = True
    else:
        next(sc for sc in secs if sc["m"] == "wattle")["m"] = "timber"
    here.apply("set", ref=("building", bid), field="sections", value=secs)
    here.event("build", f"{here.name} finished {what} on {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.4,
               tags=["building", "fishing"])
    return f"You finished {what} on {b['name']}: it now has {len(secs)} section{'s' if len(secs) != 1 else ''}."


def _weir_mend(here, bid, m) -> str:
    """Mending a weir (D2-210): its worst section a level, for `mend` of that section's build (by its place and material, with its
    footing: wild/gear.py) in materials (at least one of each) when the mending starts, and its work, two units an action."""
    import math as _m
    from cybertron2.engine import buildings as BL, wild as WL
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.wild import gear as GR
    W = WATER_WORKS["weir"]
    b = here.buildings()[bid]
    secs = WL.sections(b)
    md = dict(b.get("mending") or {})
    if not md:
        j = min(range(len(secs)), key=lambda i: (int(secs[i]["level"]), i))
        if int(secs[j]["level"]) >= 5:
            return f"{b['name']} is sound: there is nothing to mend."
        sc = secs[j]
        c = GR.cost(j, sc["m"], bool(sc.get("foot")))
        build, units = c["materials"], float(c["units"])
        need = {k: max(1, _m.ceil(float(v) * float(W["mend"]) - 1e-9)) for k, v in build.items()}
        _consume(here, need, extra=b["stock"] if here.may_take(b["stock"]) else None)
        md = {"units_left": round(units * float(W["mend"]), 2), "day": here.day, "section": j}
    md["units_left"] = round(max(0.0, float(md["units_left"]) - 2 * m), 2)
    if md["units_left"] > 1e-9:
        here.apply("set", ref=("building", bid), field="mending", value=md)
        return f"You worked on mending {b['name']}: about {show(md['units_left'])} units of work left."
    here.apply("set", ref=("building", bid), field="mending", value=None)
    j = int(md.get("section", 0))
    secs[j]["level"] = min(5, int(secs[j]["level"]) + 1)
    here.apply("set", ref=("building", bid), field="sections", value=secs)
    best = max(int(sc["level"]) for sc in secs)
    here.apply("set", ref=("building", bid), field="level", value=best)
    here.apply("set", ref=("building", bid), field="level_since", value=here.day)
    if BL.COND_OF_LEVEL[best] != int(b["condition"]):
        here.apply("set", ref=("building", bid), field="condition", value=BL.COND_OF_LEVEL[best])
    return f"You mended a section of {b['name']}: it is now {BL.LEVELS[int(secs[j]['level'])]}."


def _at_work(here, bid):
    """Building work, writing: a day's work at the building (its parcel: presence, glimpses, the day's route)."""
    here.today()["worked"].setdefault(here.name, []).append(bid)


def _works_progress(here, mind, bid, started=False):
    """Work on a room, a rebuilding or a finer finish, two units an action (more with skill), until done; it counts when done."""
    _at_work(here, bid)
    b = here.buildings()[bid]
    wk = dict(b["works"])
    done = round(2 * KN.skill(mind, wk.get("tech") or "small room") * here.yield_mult(), 2)
    wk["units_left"] = round(max(0.0, float(wk["units_left"]) - done), 2)
    words = _works_words(wk)
    if wk["units_left"] > 1e-9:
        here.apply("set", ref=("building", bid), field="works", value=wk)
        here.event("build", f"{here.name} was working on {words} at {b['name']}", actor=here.name, about=[f"building:{bid}"],
                   salience=0.25, tags=["building"])
        return ("You began " if started else "You worked on ") + f"{words} at {b['name']}: about {show(wk['units_left'])} units of work left."
    here.apply("set", ref=("building", bid), field="works", value=None)
    if wk["kind"] == "room":
        rooms = BL.rooms(b) + [{"kind": wk["room"], "floor": int(wk["floor"]), "storey": int(wk.get("storey", 1))}]
        here.apply("set", ref=("building", bid), field="rooms", value=rooms)
        here.apply("set", ref=("building", bid), field="size", value=sum(int(r["floor"]) for r in rooms))
        out = f"You finished {words} at {b['name']}: it has {BL.floor(here.buildings()[bid])} spaces of floor now."
    elif wk["kind"] == "upgrade":
        here.apply("set", ref=("building", bid), field="structure", value=wk["to"])
        out = f"You finished rebuilding {b['name']} in {wk['to']}: its rooms, fittings, stores and writing are as they were."
    else:
        here.apply("set", ref=("building", bid), field="tier", value=wk["to"])
        out = f"You finished the work on {b['name']}: it is {TIERS[wk['to']]['words']} now."
    KN.tried(here, mind, wk.get("tech") or "small room", True)
    here.event("build", f"{here.name} finished {words} at {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.5,
               tags=["building"])
    return out


def _fitting(here, mind, a, party, what):
    f = FITTINGS[what]
    at = a.get("at")
    bid = here.building(at) if at else (here.homes_here() or [None])[0]
    if bid is None:
        inside = ", ".join(x["name"] for x in here.buildings().values() if not x.get("unfinished"))
        raise Refused(f"{f['label']} is fitted inside a building, not built on open ground: say which building in \"at\""
                      + (f" ({inside})" if inside else " (there is none here yet: build a small room first)"))
    b = _usable(here, bid)
    if b.get("monument"):
        raise Refused(f"{b['name']} is a monument: nothing is fitted in it")
    lvl = _lvl_for(mind, what)
    if f.get("needs") and not b["fittings"].get(f["needs"]):
        raise Refused(f"{f['label']} needs {FITTINGS[f['needs']]['label']} first")
    if f.get("structure") and b["structure"] != f["structure"]:                # an oven only in stone, for its fire (D4-97)
        raise Refused(f"{f['label']} is built only in a {f['structure']} building ({b['name']} is {b['structure']}): "
                      f"build it in one, or raise one")
    if f.get("apart") and any(b["fittings"].get(x) for x in ("beds", "hearth")):    # a smokehouse stands apart (brief 5 §4a.1)
        raise Refused(f"{f['label']} go in a building of their own, not in a house with beds or a hearth: build a small room for them "
                      "(on another parcel than the houses, a fire there reaches none of them)")
    if what in ("beds", "hearth") and any(b["fittings"].get(x) for x, d in FITTINGS.items() if d.get("apart")):
        raise Refused(f"{b['name']} is a smokehouse: people do not sleep or keep a hearth in it")
    if f.get("spring"):                                                      # at or beside a spring (brief 5 §4b.2)
        if not here.near_spring(b["parcel"], f["spring"]):
            raise Refused(f"{f['label']} is set where the {f['spring']} is: at or beside a {f['spring']} spring, and {b['name']} is not")
    if f.get("site") and not any(here.parcels()[x]["cover"] == f["site"] for x in [b["parcel"]] + here.parcels()[b["parcel"]]["adj"]
                                 if x in here.parcels()):
        raise Refused(f"{f['label']} needs a building by {f['site']}")
    under = dict(b.get("fitting_work") or {})
    if what in under:                                                          # carry on one under way: no more materials (02zg)
        return _fitting_work(here, mind, bid, what, lvl)
    camp = b["structure"] == "camp"
    if camp and what not in ("beds", "fire ring"):                             # a lean-to keeps 10 weight: no stores, no hearth (D4-94)
        raise Refused(f"{b['name']} is a camp: it takes only beds and a fire ring (a store or a hearth needs a building)")
    sp = int(f.get("spaces", 0)) - int(f.get("room", 0))                       # a vault brings its own room
    free = BL.free_floor(b, here.stock(bid)) if not camp else 99
    n = max(1, int(_qty(a.get("qty"), 1))) if f.get("per") else 1
    if f.get("per"):
        n = min(n, free // sp) if sp > 0 else n
        if n <= 0:
            raise Refused(f"{b['name']} has no free floor for {f['label']} ({sp} space{'s' if sp != 1 else ''} a {f['per']}): "
                          f"{BL.space_words(b, here.stock(bid))}. Add a room, or make room")
    elif b["fittings"].get(what):
        raise Refused(f"{b['name']} already has {f['label']}")
    elif sp > free:
        raise Refused(f"{b['name']} has no free floor for {f['label']} (it takes {sp} space{'s' if sp != 1 else ''}): "
                      f"{BL.space_words(b, here.stock(bid))}. Add a room, or make room")
    if f.get("heavy") and not camp and BL.fitting_spaces(b, heavy=True) + int(f.get("spaces", 0)) * n > BL.footprint(b) + int(f.get("room", 0)):
        raise Refused(f"{f['label']} goes on the ground floor, and {b['name']}'s ground floor has no room for it")
    if f.get("ground") or f.get("room"):
        _ground_check(here, b["parcel"], int(f.get("ground", 0)) + int(f.get("room", 0)) * n, f["label"])
    _consume(here, f["materials"], TRY[lvl]["inputs"] * n, b["stock"] if here.may_take(b["stock"]) else None)
    ok = here.rng("build", here.day, here.name, what).random() < TRY[lvl]["chance"]
    KN.tried(here, mind, what, ok)
    if not ok:
        return f"Your try at {f['label']} went wrong; the materials are spoilt."
    under[what] = {"n": n, "units_left": float(f["units"]) * n}                  # its work charged over days, as a building's
    here.apply("set", ref=("building", bid), field="fitting_work", value=under)
    here.record("build", what, party)
    return _fitting_work(here, mind, bid, what, lvl, started=True)


def _fitting_work(here, mind, bid, what, lvl, started=False):
    """A fitting's work, two units an action (more with skill), until it is done; it counts only when finished (02zg)."""
    _at_work(here, bid)
    f = FITTINGS[what]
    b = here.buildings()[bid]
    under = dict(b.get("fitting_work") or {})
    u = dict(under[what])
    done = round(2 * KN.skill(mind, what) * here.yield_mult(), 2)
    u["units_left"] = round(max(0.0, float(u["units_left"]) - done), 2)
    n = int(u["n"])
    words = f"{str(n) + ' ' if f.get('per') else ''}{f['label']}"
    if u["units_left"] > 1e-9:
        under[what] = u
        here.apply("set", ref=("building", bid), field="fitting_work", value=under)
        here.event("build", f"{here.name} was working on {words} in {b['name']}", actor=here.name, about=[f"building:{bid}"],
                   salience=0.2, tags=["building"])
        return ("You began " if started else "You worked on ") + f"{words} in {b['name']}: about {show(u['units_left'])} units of work left."
    under.pop(what)
    here.apply("set", ref=("building", bid), field="fitting_work", value=under or None)
    fit = dict(b["fittings"])
    fit[what] = int(fit.get(what, 0)) + n
    here.apply("set", ref=("building", bid), field="fittings", value=fit)
    if f.get("room"):                                                          # a vault: a stone room of its own (02zh §4)
        rooms = BL.rooms(b) + [{"kind": what, "floor": int(f["room"]), "storey": 1} for _ in range(n)]
        here.apply("set", ref=("building", bid), field="rooms", value=rooms)
        here.apply("set", ref=("building", bid), field="size", value=sum(int(r["floor"]) for r in rooms))
    here.event("build", f"{here.name} put {words} into {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.3, tags=["building"])
    return f"You put {words} into {b['name']}."


def _build_work(here, mind, bid, lvl, started=False):
    _at_work(here, bid)
    b = here.buildings()[bid]
    u = dict(b["unfinished"])
    done = round(2 * KN.skill(mind, u["blueprint"]) * here.yield_mult(), 2)
    u["units_left"] = round(max(0.0, u["units_left"] - done), 2)
    here.record("build", u["blueprint"], None)
    if u["units_left"] > 1e-9:                                                 # heard and seen at work (signs.BUILDING)
        here.event("build", f"{here.name} was working on {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.2,
                   tags=["building"])
    if u["units_left"] <= 1e-9:
        bp = BLUEPRINTS.get(u["blueprint"]) or MONUMENTS.get(u["blueprint"]) or {}
        here.apply("set", ref=("building", bid), field="unfinished", value=None)
        here.apply("set", ref=("building", bid), field="built_day", value=here.day)
        if bp.get("fittings"):                                                 # a blueprint that comes fitted (a camp: D2-68)
            here.apply("set", ref=("building", bid), field="fittings", value=dict(bp["fittings"]))
        if bp.get("lasts"):
            here.apply("set", ref=("building", bid), field="lasts_until", value=here.day + int(bp["lasts"]))
        here.event("build", f"{here.name} finished {b['name']}", actor=here.name, about=[f"building:{bid}"], salience=0.6, tags=["building", "shelter"])
        KN.tried(here, mind, u["blueprint"], True)
        if bp.get("fittings"):
            return f"You made {b['name']}: shelter for {bp['size']} with a fire, for about {bp['lasts']} nights."
        if b.get("monument"):
            return (f"You finished {b['name']}. It has room for {BL.places(b)} lines written on it (write {{\"at\": \"{b['name']}\", "
                    "\"text\"}).")
        return (f"You finished {b['name']}: {BL.floor(b)} spaces of floor, all free. It has no fittings yet: beds, a hearth and bins "
                "make it a house.")
    here.apply("set", ref=("building", bid), field="unfinished", value=u)
    return ("You began " if started else "You worked on ") + f"{b['name']}: about {show(u['units_left'])} units of work left."


# ---------------------------------------------------------------------- writing on buildings (D2-169, D2-170; building_lines.md)
def _writing_site(here, at):
    bid = here.building(at) if at else None
    if bid is None:
        names = ", ".join(b["name"] for b in here.buildings().values() if not b.get("unfinished")) or "none"
        raise Refused(f"say which building or monument here to write on (\"at\": {names})")
    b = here.buildings()[bid]
    if b.get("unfinished"):
        raise Refused(f"{b['name']} is not finished")
    if b["condition"] <= 0:
        raise Refused(f"{b['name']} is a ruin: there is nothing left to write on")
    if b["structure"] == "camp":
        raise Refused(f"{b['name']} is a lean-to of branches: there is nothing to write on")
    return bid, b


def _slot_of(b, x):
    """A line's place: its number (1 up) or where it is ("over the door")."""
    if x is None or str(x).strip() == "":
        return None
    s = str(x).strip().lower()
    try:
        k = int(float(s)) - 1
        return k if 0 <= k < BL.places(b) else -1
    except ValueError:
        pass
    for k in range(BL.places(b)):
        if BL.spot_words(b, k) in s or s in BL.spot_words(b, k):
            return k
    return -1


def _write_how(b, a):
    how = str(a.get("how") or "paint").strip().lower()
    how = {"painted": "paint", "painting": "paint", "carved": "carve", "carving": "carve", "cut": "carve", "engrave": "carve"}.get(how, how)
    if how not in ("paint", "carve"):
        raise Refused("a line is painted (\"how\": \"paint\") or carved (\"how\": \"carve\", with a tool)")
    return "stone" if how == "carve" and b["structure"] == "stone" else how


def write_units(here, a, erase=False) -> int:
    """The work of a line (D2-170): painting 2, carving 4, in stone 6; another's line, or the description, the same plus 1."""
    try:
        bid, b = _writing_site(here, a.get("at"))
    except Refused:
        return 0
    if erase:
        k = _slot_of(b, a.get("line"))
        ln = next((x for x in b.get("lines") or [] if int(x["slot"]) == k), None)
        if ln is None:
            return 0
        return int(LINES["units"][ln.get("how", "paint")]) + (int(LINES["other"]) if ln.get("by") != here.name else 0)
    if a.get("description") is not None and a.get("text") is None:
        d = b.get("description") or {}
        return int(LINES["units"]["paint"]) + (int(LINES["other"]) if d and d.get("by") != here.name else 0)
    try:
        how = _write_how(b, a)
    except Refused:
        return 0
    k = _slot_of(b, a.get("line"))
    ln = next((x for x in b.get("lines") or [] if int(x["slot"]) == k), None) if k is not None else None
    return int(LINES["units"][how]) + (int(LINES["other"]) if ln and ln.get("by") != here.name else 0)


def _write(here, mind, a, party):
    bid, b = _writing_site(here, a.get("at"))
    if a.get("description") is not None and a.get("text") is None:           # the description replaced (D2-169)
        text = BL.cap_text(a["description"], "description")
        if not text:
            raise Refused("say what to write (\"description\": text)")
        old = b.get("description") or {}
        _at_work(here, bid)
        here.apply("set", ref=("building", bid), field="description",
                   value={"text": text, "by": here.name, "day": here.day, "was": old.get("text")})
        if old and old.get("by") != here.name:
            _changed(here, bid, b, f"the words describing {b['name']} have been changed")
        here.event("write", f"{here.name} was painting new words on {b['name']}", actor=here.name, about=[f"building:{bid}"],
                   salience=0.6, tags=["building"], own=3.0)
        here.record("write", "description", party, site=bid)
        return f"You wrote on {b['name']}: “{text}”."
    text = BL.cap_text(a.get("text"), "line")
    if not text:
        raise Refused("say what to write (\"text\")")
    how = _write_how(b, a)
    lines = [dict(x) for x in b.get("lines") or []]
    k = _slot_of(b, a.get("line"))
    if k == -1:
        raise Refused(f"{b['name']} has {BL.places(b)} places for lines: say one by its number (1 to {BL.places(b)}) or where it is")
    if k is None:
        used = {int(x["slot"]) for x in lines}
        k = next((i for i in range(BL.places(b)) if i not in used), None)
        if k is None:
            raise Refused(f"every place on {b['name']} is written on ({BL.places(b)}): replace one (\"line\": its number) or erase one")
    if how in ("carve", "stone"):
        tool, m = here.best_tool(LINES["carve_tools"])
        if tool is None:
            raise Refused("carving needs a tool in your hands")
        if how == "stone":
            _mason(mind)
        here.apply("wear", container=here.hands, item=tool, uses=float(LINES["carve_wear"]))
    old = next((x for x in lines if int(x["slot"]) == k), None)
    _at_work(here, bid)
    lines = [x for x in lines if int(x["slot"]) != k] + [{"slot": k, "text": text, "by": here.name, "day": here.day, "how": how,
                                                          "was": old["text"] if old else None, "was_by": old["by"] if old else None}]
    here.apply("set", ref=("building", bid), field="lines", value=sorted(lines, key=lambda x: int(x["slot"])))
    spot = BL.spot_words(b, k)
    verb = {"paint": "painting", "carve": "carving", "stone": "cutting"}[how]
    if old and old.get("by") != here.name:
        _changed(here, bid, b, f"the line {spot} of {b['name']} has been " + ("painted over" if how == "paint" else "cut away")
                 + " and new words put there")
    here.event("write", f"{here.name} was {verb} words {spot} of {b['name']}", actor=here.name, about=[f"building:{bid}"],
               salience=0.6 if not old else 0.8, tags=["building"], own=3.0)
    here.record("write", how, party, site=bid)
    return f"You {'painted' if how == 'paint' else 'carved'} {spot} of {b['name']}: “{text}”."


def _erase(here, mind, a, party):
    bid, b = _writing_site(here, a.get("at"))
    k = _slot_of(b, a.get("line"))
    ln = next((x for x in b.get("lines") or [] if int(x["slot"]) == k), None) if k is not None else None
    if ln is None:
        have = "; ".join(f"{int(x['slot']) + 1}: {BL.spot_words(b, int(x['slot']))}" for x in b.get("lines") or []) or "none"
        raise Refused(f"say which line of {b['name']} to scratch out (\"line\": {have})")
    if ln.get("how") in ("carve", "stone"):
        tool, m = here.best_tool(LINES["carve_tools"])
        if tool is None:
            raise Refused("scratching out a carved line needs a tool in your hands")
        here.apply("wear", container=here.hands, item=tool, uses=float(LINES["carve_wear"]))
    _at_work(here, bid)
    here.apply("set", ref=("building", bid), field="lines", value=[x for x in b["lines"] if int(x["slot"]) != k])
    spot = BL.spot_words(b, k)
    if ln.get("by") != here.name:
        _changed(here, bid, b, f"the line {spot} of {b['name']} has been scratched out")
    here.event("write", f"{here.name} was scratching out the words {spot} of {b['name']}", actor=here.name, about=[f"building:{bid}"],
               salience=0.9, tags=["building"], own=3.0)
    here.record("erase", ln.get("how"), party, site=bid, was=ln["text"], was_by=ln.get("by"))
    return f"You scratched out the line {spot} of {b['name']} (it said: “{ln['text']}”)."


def _changed(here, bid, b, text):
    """What its people will notice the next time they see it (building_lines.md §3)."""
    ch = list(b.get("changes") or []) + [{"day": here.day, "text": text, "by": here.name}]
    here.apply("set", ref=("building", bid), field="changes", value=ch[-20:])


# ---------------------------------------------------------------------- goods
def _store_here(here, at=None) -> str:
    if at:
        bid = here.building(at)
        if bid is None:
            raise Refused(f"there is no building called {at!r} here")
    else:
        mine = [b for b in here.homes_here()] or [b for b in here.buildings() if here.may_take(here.buildings()[b]["stock"])]
        if not mine:
            raise Refused("there is no store here that is yours to use")
        bid = mine[0]
    if not here.may_take(here.buildings()[bid]["stock"]):
        raise Refused(f"{here.buildings()[bid]['name']}'s store is not yours to use (to take without the right is theft; to put, leave)")
    return bid


def _move(here, mind, a, party):
    item = item_of(a.get("item"))
    to = str(a.get("to") or "store").strip().lower()
    bid = _store_here(here, a.get("at"))
    b = here.buildings()[bid]
    if to in ("hands", "hand", "me", "myself", "carry", "carried", "pack"):
        src, dst, verb, have = b["stock"], here.hands, "took", here.stock(bid).get(item, 0.0)
    else:
        src, dst, verb, have = here.hands, b["stock"], "put", here.carried().get(item, 0.0)
    if have <= 1e-9:                                                           # where it is, or who took it (D4-95)
        if verb == "put":
            where = [(c, here.contents(c).get(item, 0.0)) for c in here.takeable() if c != here.hands]
            where = [(c, q) for c, q in where if q > 1e-9]
            raise Refused(f"there is no {item} in your hands" + (
                "; " + ", ".join(f"{_store_name(here, c)} holds {show(q)}" for c, q in where)
                + " (work done for your household puts what it gives straight into its store)" if where else _short_note(here, item)))
        raise Refused(f"there is no {item} in {b['name']}" + _short_note(here, item))
    q = round(min(_qty(a.get("qty"), have), have), 6)
    full = _full_note(here, b["stock"], item, q) if verb == "put" else ""      # what does not fit lies at its door (D2-155, D4-94)
    here.apply("transfer", src=src, dst=dst, item=item, qty=q)
    if verb == "took":
        _drawn(here, src, item, q)
    here.event("store", f"{here.name} {verb} {item} {'into' if verb == 'put' else 'from'} {b['name']}", actor=here.name,
               about=[f"building:{bid}"], salience=0.1, tags=["food"] if ITEMS[item]["food"] else [])
    return (f"You {verb} {show(q)} {item} {'into' if verb == 'put' else 'from'} {b['name']}" + full
            + f" (it holds {show(here.stock(bid).get(item, 0.0))}).")


def _parcel_named(here, x):
    """A parcel here by its name, or named within a phrase ("the snares at the Ham"; brief 4c §4.4)."""
    pid = here.parcel(x)
    if pid is not None:
        return pid
    low = str(x or "").strip().lower()
    hits = [p for p, q in here.parcels().items() if len(q["name"].lower().removeprefix("the ")) > 3
            and q["name"].lower().removeprefix("the ") in low]
    return max(hits, key=lambda p: len(here.parcels()[p]["name"])) if hits else None


def _own_set_at(here, tech, key):
    """One's own (or one's household's) set thing of this technique standing at this parcel, the newest (u2 §3; D2-305)."""
    hits = [(int((c.get("set") or {}).get("set_day", 0)), cid) for cid, c in here._w.s["containers"].items()
            if c.get("kind") == "set" and c.get("parcel") == key and not (c.get("set") or {}).get("weir")
            and (c.get("set") or {}).get("method") == tech and TH.owns_set(c, here.name, here._w) and TH.set_about(here._w, c)]
    return max(hits)[1] if hits else None


def _tend(here, mind, cid, place_name):
    """Tending one's set gear (D2-294; u2 §3): its catch into hand, and the gear set again where it stands."""
    c = here.thing(cid)
    noun = TH.trap_noun(c)
    took = []
    for it, q in sorted(c["goods"].items()):
        if q > 1e-9:
            here.apply("transfer", src=cid, dst=here.hands, item=it, qty=q)
            took.append(f"{show(q)} {it}")
    here.apply("set_thing", cid=cid, field="catch", value=[])
    here.apply("set_thing", cid=cid, field="caught", value=0)
    here.apply("set_thing", cid=cid, field="set", value=dict(c["set"], set_day=here.day, sprung=None))
    here.remember_thing(cid, "put")
    tag = f" ({c['tag']})" if c.get("tag") and here.setting("tags") else ""
    got = ("took " + ", ".join(took) + " from them") if took else "nothing was in them"
    return f"You tended your {noun} at {place_name}{tag}: {got}, and set them again where they stand."


def _lift(here, mind, rem):
    """Lifting a set thing one knows (brief 4c §4.4): everything in it into hand, or a look that it holds nothing."""
    c = here.thing(rem)
    noun = TH.trap_noun(c)
    whose = "your" if TH.owns_set(c, here.name, here._w) else "the"
    took = []
    for it, q in sorted(c["goods"].items()):
        if q > 1e-9:
            took.append(_take(here, mind, {"item": it, "qty": q, "from": "", "_thing": rem}, None))
    if not took:
        here.look_thing(rem)
        return f"You looked over {whose} {noun} at {here.spot_name(c)}: nothing is caught in them."
    return " ".join(took)


def _take(here, mind, a, party):
    src_name = str(a.get("from") or a.get("at") or "")
    if not a.get("item"):                                       # no item: lift a set thing one knows, all of it (brief 4c §4.4)
        rem = here.find_thing(src_name)
        if rem is not None and (here.thing(rem) or {}).get("kind") == "set":
            return _lift(here, mind, rem)
        pid = _parcel_named(here, src_name)
        if rem is None and pid is not None and here.building(src_name) is None:
            rem = here.search_thing(here.parcels()[pid]["name"])
            if rem is not None and (here.thing(rem) or {}).get("kind") == "set":
                return _lift(here, mind, rem)
        if rem is None and any(x in src_name.lower() for x in ("snare", "trap", "noose")):
            raise Refused("you know of no such set snares or traps here; name the place: {\"from\": \"the snares at <place>\"}")
    item = item_of(a.get("item"))
    if not src_name.strip() and not a.get("_thing"):
        raise Refused('take needs "from": the building, or the place where the things lie (a field, the Green, the Street)')
    rem = a.get("_thing") or here.find_thing(src_name, item)    # what one knows lies here (D2-87: nobody's)
    from cybertron2.engine import tags as TG
    tag = TG.tag_in(src_name) if here.setting("tags") else None
    if rem is None and tag and here.building(src_name) is None:              # a thing named by its tag: say why not (D4-94)
        if not here.tagged_here(tag):
            raise Refused(f"you know of nothing called {tag} here")
        raise Refused(f"{tag} holds no {item}" if item else f"{tag} holds nothing")
    pid = _parcel_named(here, src_name) if rem is None else None
    if rem is None and pid is not None and here.building(src_name) is None:
        rem = here.search_thing(here.parcels()[pid]["name"], item)   # not known of: one looks, as it is seen or hidden (D4-70)
        if rem is None:
            raise Refused(f"you looked over {here.parcels()[pid]['name']} and found no {item} lying there")
    if rem:
        c = here.thing(rem)
        from cybertron2.engine import wild as WL
        met = WL.cache_meet(here, c.get("parcel")) if c.get("cached") else None   # a bear lying up by its kill (brief 3 §3)
        if met:
            return met
        door = c.get("door") if c.get("door") in here.buildings() else None         # left at a door: the house's (D4-89)
        src, theft = rem, bool(door) and not here.may_take(here.buildings()[door]["stock"])
        bid = door
        label = f"what {c['of']} left" if c.get("body") else f"what lay at {here.spot_name(c)}"
        if c.get("kind") == "set":
            label = (f"{'your' if TH.owns_set(c, here.name, here._w) else 'the'} {TH.trap_noun(c)} "
                     f"at {here.spot_name(c)}")
        have = c["goods"].get(item, 0.0)
        if c.get("by") != here.name:
            f = mind.store.setdefault("found", [])
            if rem not in f:
                f.append(rem)                                                   # finding things trains the eye (D2-91)
    else:
        bid = here.building(src_name)
        if bid is None:
            raise Refused(f"there is no building called {src_name!r} here")
        b = here.buildings()[bid]
        if not here.can_enter(bid):
            raise Refused(f"{b['name']}'s door is barred")
        src, label, theft = b["stock"], b["name"], not here.may_take(b["stock"])
        have = here.stock(bid).get(item, 0.0)
    q = round(min(_qty(a.get("qty"), have), have), 6)
    if q <= 1e-9:
        raise Refused(f"you find no {item} in {label}" + (_short_note(here, item) if not rem else ""))
    here.apply("transfer", src=src, dst=here.hands, item=item, qty=q)
    if not rem:
        _drawn(here, src, item, q)
    if theft:
        here.today()["thefts"].append({"by": here.name, "building": bid, "item": item, "qty": round(q, 2), "door": bool(rem)})
        here.record("take", None, None, theft=True)
        return f"You took {show(q)} {item} from {label}, which is not yours to take from. Whether anyone saw, you will learn."
    c = here.thing(src) or {"kind": "stock"}
    if c["kind"] == "set":                                                     # emptied: its catch gone; another's emptying it shows
        if not any(x > 1e-9 for x in c["goods"].values()):                     # to those who know the line (brief 4c §4.2)
            here.apply("set_thing", cid=src, field="catch", value=[])
        if c.get("by") not in (here.name, None) and not TH.owns_set(c, here.name, here._w):
            here.apply("set_thing", cid=src, field="robbed", value={"day": here.day, "by": here.name})
    if c["kind"] == "set" and c.get("by") not in (here.name, None) and not TH.owns_set(c, here.name, here._w):   # another's robbed: seen
        whose = (f"the weir {', '.join(c.get('crew') or [c['by']])} work" if TH.is_weir(c) else f"the "
                 f"{'traps' if (c.get('set') or {}).get('method') == 'trap in water' else 'snares'} {c['by']} set")
        here.event("take", f"{here.name} took {item} from {whose} at {here.spot_name(c)}", actor=here.name, salience=0.55,
                   about=[f"parcel:{c['parcel']}"], tags=["food", "hunting"], concerns=list(c.get("crew") or [c["by"]]))
        here.today()["thefts"].append({"by": here.name, "thing": src, "item": item, "qty": round(q, 2)})   # theft (u2 §6 fault 7)
        here.record("take", None, None, theft=True)
        here.remember_thing(src, "took")
        return (f"You took {show(q)} {item} from {whose} at {here.spot_name(c)}, which are not yours to take from. Whether anyone "
                "saw, you will learn.")
    here.event("take", f"{here.name} took {item} from {label}", actor=here.name, salience=0.4 if c["kind"] in TH.KINDS else 0.3,
               about=[f"parcel:{c['parcel']}"] if c.get("parcel") else [], tags=["food"] if ITEMS[item]["food"] else [])
    if c["kind"] in TH.KINDS:
        here.remember_thing(src, "took")
    return f"You took {show(q)} {item} from {label}."


def _give(here, mind, a, party):
    """Giving (D2-111, world/things_in_places.md): to a person here, into their hands; to a household or a building one may use, into
    its store; to a building one may not use, or someone not here, at its door, in the open; to a place, left there (hidden, with the
    `hidden` modifier)."""
    to_raw = a.get("to") or a.get("at")
    to = here.person(to_raw)
    item, q = item_of(a.get("item")), _qty(a.get("qty"))
    if to and to != here.name:
        if party and party != here.name and party != here.household() and not here.works_for(party):
            raise Refused(f"'for' gives from that household's store, which is not yours: to give to {party}, give with 'to' instead")
        src = here.hands if not party or party == here.name else _out(here, party)
        if src == here.hands:
            _top_up(here, item, q)                                             # from the stores here one may use (D4-96)
        have = here.carried().get(item, 0.0) if src == here.hands else here.stock(src[len("stock:"):]).get(item, 0.0)
        if have + 1e-9 < q:
            raise Refused(f"there is only {show(have)} {item} to give" + _short_note(here, item))
        here.apply("transfer", src=src, dst=here.hands_of(to), item=item, qty=q)
        here.event("give", f"{here.name} gave {q:g} {item} to {to}", actor=here.name, target=to, about=[f"person:{to}"], salience=0.35,
                   tags=["food"] if ITEMS[item]["food"] else [], concerns=[to])
        here.record("give", None, party, to=to, item=item, qty=q)
        return f"You gave {q:g} {item} to {to}."
    if party and party != here.name and party != here.household() and not here.works_for(party):
        raise Refused(f"'for' gives from that household's store, which is not yours")
    src = here.hands if not party or party == here.name else _out(here, party)      # from one's household's store (D2-37)
    if src == here.hands and here.person(to_raw) is None and here.building(to_raw) is None:
        _top_up(here, item, q)                                                 # left at a place: from the stores here too (D4-96)
    have = here.carried().get(item, 0.0) if src == here.hands else here.stock(src[len("stock:"):]).get(item, 0.0)
    if have + 1e-9 < q:
        raise Refused(f"you carry only {show(have)} {item}" if src == here.hands else f"there is only {show(have)} {item} in the store")
    if src != here.hands:                                                     # into one's hands first, then given on
        here.apply("transfer", src=src, dst=here.hands, item=item, qty=q)
    pid = here.parcel(to_raw)
    bid = here.building(to_raw)
    if pid is not None and bid is None:
        return _put_down(here, mind, a, item, q, pid)
    hh = None
    if bid is None:
        try:
            hh = _party(here, to_raw)
        except Refused:
            hh = here.someone(to_raw)
        if hh in here.households():
            house = here.party_container(hh)
            if house and house.startswith("stock:") and here.can_enter(house[len("stock:"):]):
                return _into_store(here, house[len("stock:"):], item, q, party, hh)
            bid = here.house_of(hh)
        elif hh:                                                                   # someone not here: left at their door (D2-111)
            bid = here.house_of(hh)
            if bid is not None:
                return _put_down(here, mind, a, item, q, here.buildings()[bid]["parcel"], door=bid)
        if bid is None:
            raise Refused(f"there is nobody, no household's house and no place called {to_raw!r} here")
    b = here.buildings()[bid]
    if here.may_take(b["stock"]) or here.can_enter(bid):
        return _into_store(here, bid, item, q, party, hh)
    return _put_down(here, mind, a, item, q, b["parcel"], door=bid)


def _into_store(here, bid, item, q, party, hh):
    b = here.buildings()[bid]
    full = _full_note(here, b["stock"], item, q)                              # what does not fit lies at its door (D2-155)
    here.apply("transfer", src=here.hands, dst=b["stock"], item=item, qty=q)
    owners = here.households()[hh]["name"] if hh else None
    here.event("give", f"{here.name} put {q:g} {item} into {b['name']}" + (f", for {owners}" if owners else ""), actor=here.name,
               about=[f"building:{bid}"], salience=0.35, tags=["food"] if ITEMS[item]["food"] else [],
               concerns=list(here.institution(hh)["members"]) if hh else [])
    here.today()["left"].append({"by": here.name, "item": item, "qty": q, "building": bid})   # its household finds it in the morning
    here.record("give", None, party, to=hh or bid, item=item, qty=q)
    return (f"You gave {q:g} {item} to {owners}: it is in {b['name']}" if owners else f"You left {q:g} {item} at {b['name']}") + full + "."


def _put_down(here, mind, a, item, q, pid, door=None):
    """Left at a spot, in the open (D2-87): nobody's; hidden with the `hidden` modifier (D2-93)."""
    mods = MOD.resolve(here, mind, "give", a, place=True)
    how = mods.get("hidden")
    untaught = bool(how) and any(TECHNIQUES[m]["key"] == "hidden" for m in mods["_untaught"])
    cid = here.apply("new_thing", node=here.node, parcel=pid, kind="pile", by=here.name, hidden=how, untaught=untaught, door=door)
    here.apply("transfer", src=here.hands, dst=cid, item=item, qty=q)
    here.remember_thing(cid, "put")
    MOD.practise(here, mind, mods)
    pname = here.parcels()[pid]["name"]
    where = f"at the door of {here.buildings()[door]['name']}" if door else f"at {pname}"
    verb = {"under brush": "hid", "buried": "buried"}.get(how, "left")
    tail = {"under brush": " under brush", "buried": " in the ground"}.get(how, "")
    here.event("put", f"{here.name} {verb} {item} {where}{tail}", actor=here.name,
               about=[f"parcel:{pid}"] + ([f"building:{door}"] if door else []), salience=0.25 if how else 0.4,
               tags=["food"] if ITEMS[item]["food"] else [], concerns=here.living_in(door) if door else [])
    here.record("give", None, None, to=f"parcel:{pid}", item=item, qty=q, hidden=how)
    out = f"You {verb} {q:g} {item} {where}" + (tail or ", in the open")
    if door:
        out += " (you could not put it inside)"
    if untaught:
        out += ". You have never been shown how to hide things well; it is not as well hidden as it might be"
    return out + "."


def _alias_give(hidden=None):
    def f(a):
        b = {**a, "to": a.get("to") or a.get("at")}
        if hidden and not b.get("hidden"):
            b["hidden"] = hidden
        return b
    return f


ALIASES = {"leave": _alias_give(), "put": _alias_give(), "drop": _alias_give(), "hide": _alias_give("under brush")}
# lifting or checking one's snares or traps is taking what is in them (brief 4c §4.4): as a verb, or as the way of work named
LIFT = {f"{v} {o}".strip() for v in ("lift", "check", "empty") for o in
        ("", "the snares", "snares", "my snares", "the snare line", "the snare", "the traps", "traps", "my traps", "the eel traps",
         "eel traps", "the wicker traps", "wicker traps")} - {"empty"}


def _as_lift(a):
    """A lift or check of snares or traps, as a take from them: from the place it names, else the snares or traps it names."""
    what = str(a.get("what") or a.get("do") or "").strip().lower()
    src = a.get("from") or a.get("at") or a.get("thing") or a.get("target")
    if src and not any(x in str(src).lower() for x in ("snare", "trap", "noose")):
        src = f"the {'traps' if 'trap' in what else 'snares'} at {src}"
    return {k: v for k, v in a.items() if k not in ("do", "what", "at")} | {"from": src or ("the traps" if "trap" in what else "the snares")}


# ---------------------------------------------------------------------- hosting and grants (05 §3; D4-23 rights)
def _house_for_grant(here, at):
    bid = here.building(at) if at else (here.homes_here() or [None])[0]
    if bid is None:
        raise Refused("say which house here")
    if not here.may_grant(("building", bid)):
        raise Refused(f"you may not let people into {here.buildings()[bid]['name']}")
    return bid


def _host(here, mind, a, party):
    who = here.person(a.get("person") or a.get("to"))
    if who is None or who == here.name:
        raise Refused(f"there is nobody called {a.get('person') or a.get('to')!r} here")
    bid = _house_for_grant(here, a.get("at"))
    feed = str(a.get("feed", "")).lower() in ("true", "yes", "1")
    here.apply("claim", thing=("building", bid), claimant=who, rights=["access", "withdrawal"] if feed else ["access"], grounds="granted",
               until=here.day, by=here.name)
    b = here.buildings()[bid]
    here.event("host", f"{here.name} took {who} in for the night at {b['name']}" + (", at the household's table" if feed else ""),
               actor=here.name, target=who, salience=0.4, tags=["shelter"], concerns=[who])
    return f"You let {who} sleep at {b['name']} tonight" + (" and eat from its store." if feed else " (a bed, if one is free; not its food).")


def _grant(here, mind, a, party):
    bid = _house_for_grant(here, a.get("at"))
    to_raw = str(a.get("to") or "").strip()
    who = "anyone" if to_raw.lower() in ("anyone", "everyone", "all") else (here.person(to_raw) or _party(here, to_raw))
    what = str(a.get("what") or "shelter").lower()
    rights = ["access", "withdrawal"] if "food" in what or "store" in what else ["access"]
    days = a.get("days")
    until = here.day + int(_qty(days)) - 1 if days else None
    here.apply("claim", thing=("building", bid), claimant=who, rights=rights, grounds="granted", until=until, by=here.name)
    b = here.buildings()[bid]
    here.event("grant", f"{here.name} let {who} use {b['name']}" + (" and its store" if "withdrawal" in rights else ""), actor=here.name,
               salience=0.4, tags=["shelter"], concerns=[who] if who in here.people() else [])
    return f"{who} may now use {b['name']}" + (" and its store" if "withdrawal" in rights else "") + (f" for {days} days." if days else ", until you revoke it.")


def _revoke(here, mind, a, party):
    bid = _house_for_grant(here, a.get("at"))
    to_raw = str(a.get("to") or "").strip()
    who = "anyone" if to_raw.lower() in ("anyone", "everyone", "all") else (here.person(to_raw) or to_raw)
    ended = [cid for cid, c in here.claim_records(("building", bid)) if c["claimant"] == who and c["grounds"] == "granted"]
    if not ended:
        raise Refused(f"{who} has no grant to {here.buildings()[bid]['name']}")
    for cid in ended:
        here.apply("end_claim", claim=cid)
    return f"You ended {who}'s use of {here.buildings()[bid]['name']}."


# ---------------------------------------------------------------------- households (09 §2d; D4-36)
def _join(here, mind, a, party):
    hh = _party(here, a.get("household"))
    if hh not in here.households():
        raise Refused(f"{a.get('household')!r} is not a household")
    if hh == here.household():
        raise Refused("you already belong to it")
    here.today()["joins"].append({"by": here.name, "household": hh})
    return f"You asked to be taken into {here.households()[hh]['name']}; it happens if one of them who may admit you does so today."


def _admit(here, mind, a, party):
    who = here.person(a.get("person") or a.get("to"))
    hh = here.household()
    if who is None or hh is None:
        raise Refused("there is nobody by that name here, or you have no household")
    rule = here.institution(hh)["rules"].get("admit", "head")
    if rule == "head" and here.head(hh) != here.name:
        raise Refused(f"only the head of {here.institution(hh)['name']} may take someone in")
    here.today()["admits"].append({"by": here.name, "person": who, "household": hh})
    return f"You agreed to take {who} into {here.institution(hh)['name']}, if {who} asks today."


def _leave_household(here, mind, a, party):
    hh = here.household()
    if hh is None:
        raise Refused("you belong to no household")
    here.apply("leave", person=here.name, inst=hh)
    here.event("household", f"{here.name} left {here.institution(hh)['name']}", actor=here.name, salience=0.6, tags=["household"],
               concerns=here.institution(hh)["members"])
    return f"You left {here.institution(hh)['name']}. You keep what you carry."


def _found(here, mind, a, party):
    name = str(a.get("name") or here.name).strip()[:30]
    old = here.household()
    iid = here.apply("found", person=here.name, name=name)
    here.event("household", f"{here.name} set up a household of their own", actor=here.name, salience=0.6, tags=["household"],
               concerns=here.institution(old)["members"] if old else [])
    return f"You are now the head of {here.institution(iid)['name']}. You have no house yet: claim an empty one, build one, or be let into one."


def _claim(here, mind, a, party):
    x = a.get("thing") or a.get("what")
    key = here.parcel(x)
    kind = "parcel"
    if key is None:
        key, kind = here.building(x), "building"
    if key is None:
        key, kind = here.herd(x) if x else None, "herd"
    if key is None:
        raise Refused(f"there is no field, building or herd called {x!r} here")
    claimant = party or here.name
    plots = a.get("plots")
    if plots not in (None, "") and kind == "parcel":                          # plots of a field, pasture or meadow (D2-163)
        return _claim_plots(here, key, claimant, plots)
    if plots not in (None, ""):
        raise Refused("only a field, pasture or meadow is held in plots")
    here.apply("claim", thing=(kind, key), claimant=claimant, rights="all", grounds="claimed")
    name = {"parcel": here.parcels, "building": here.buildings, "herd": here.herds}[kind]()[key]["name"]
    own = {claimant, here.household(), "anyone"}
    hh = here.households()
    others = sorted({hh[c["claimant"]]["name"] if c["claimant"] in hh else c["claimant"] for c in here.claims((kind, key))
                     if c["claimant"] not in own and c["grounds"] != "granted"})
    who = hh[claimant]["name"] if claimant in hh else claimant
    here.event("claim", f"{here.name} claimed {name}" + ("" if claimant == here.name else f" for {who}") + (f", which {', '.join(others)} also claim" if others else ""),
               actor=here.name, about=[f"{kind}:{key}"], salience=0.7 if others else 0.5, tags=["land"], concerns=_holders_people(here, (kind, key)))
    return f"You claimed {name}" + ("" if claimant == here.name else f" for {who}") + "." + (f" {', '.join(others)} claim it too: a dispute." if others else "")


def _claim_plots(here, key, claimant, plots) -> str:
    """A claim of n plots of a field, pasture or meadow (D2-163): of the unclaimed plots first; any more overlaps what others hold,
    which is recorded as a dispute, never refused (D4-23). The overlap is counted against the holder with the most plots there."""
    par = here.parcels()[key]
    if par["cover"] not in FM.LAND:
        raise Refused(f"{par['name']} is not held in plots; claim it whole")
    try:
        n = int(float(plots))
    except (TypeError, ValueError):
        raise Refused("plots must be a whole number")
    size = int(par["size"])
    if n < 1:
        raise Refused("claim at least one plot")
    n = min(n, size)
    hold = FM.holdings(here.claims(("parcel", key)), size)
    free = max(0, size - sum(hold.values()))
    over = max(0, n - free)
    mine = {claimant, here.household(), here.name}
    others = sorted(((h, k) for h, k in hold.items() if h not in mine), key=lambda hk: -hk[1])
    of = others[0][0] if over and others else None
    over = min(over, hold.get(of, 0)) if of else 0
    here.apply("claim", thing=("parcel", key), claimant=claimant, rights="all", grounds="claimed", plots=n,
               **({"of": of, "over": over} if of else {}))
    names = FM.names_of(here)
    who = names.get(claimant, claimant)
    what = f"{n} plot{'s' if n != 1 else ''} of {par['name']}"
    clash = f", {over} of them {FM.possessive(names, of)}" if of else ""
    here.event("claim", f"{here.name} claimed {what}" + ("" if claimant == here.name else f" for {who}") + clash, actor=here.name,
               about=[f"parcel:{key}"], salience=0.7 if of else 0.5, tags=["land"], concerns=_holders_people(here, ("parcel", key)))
    return (f"You claimed {what}" + ("" if claimant == here.name else f" for {who}") + "."
            + (f" {over} of them {'is' if over == 1 else 'are'} {FM.possessive(names, of)}: a dispute." if of else ""))


def _sleep(here, mind, a, party):
    bid = here.building(a.get("at"))
    if bid is None:
        raise Refused(f"there is no building called {a.get('at')!r} here")
    if not here.can_enter(bid):
        raise Refused(f"{here.buildings()[bid]['name']}'s door is barred")
    here.today()["sleep"][here.name] = bid
    note = "" if "access" in here.rights(("building", bid)) else " (nobody let you in: those who hold it will know)"
    return f"You mean to sleep at {here.buildings()[bid]['name']} tonight, if a bed is free{note}."


def _set(here, mind, a, party):
    if str(a.get("thing") or "").strip().lower() in ("gap", "the gap", "hatches", "sluice", "weir", "the weir"):
        return _set_gap(here, mind, a)
    bid = here.building(a.get("at")) if a.get("at") else (here.homes_here() or [None])[0]
    if bid is None:
        raise Refused("say which building")
    if "management" not in here.rights(("building", bid)):                   # who does, by the claims (D4-95)
        b = here.buildings()[bid]
        who = [x for x in here.people() if "management" in here.rights(("building", bid), x)]
        hh = here.households().get(b.get("household") or "", {}).get("name") if b.get("household") else None
        raise Refused(f"only those who manage {b['name']} set its door: its holder's head"
                      + (f" ({hh})" if hh else "") + (f"; here today: {', '.join(who)}" if who else "; none of them is here")
                      + ". A member may use it but not bar or open it")
    to = str(a.get("to") or "").lower()
    if to not in ("open", "barred"):
        raise Refused('set {"thing": "door", "to": "open" or "barred"}')
    here.apply("set", ref=("building", bid), field="door", value=to)
    return f"{here.buildings()[bid]['name']}'s door is now {to}."


def _gap_site(here, at):
    """The weir or water mill a gap is set at: named, or the one at the place named, or the only one here."""
    gaps = [bid for bid, b in sorted(here.buildings().items()) if not b.get("unfinished") and here.has_gap(b)]
    bid = here.building(at) if at else None
    if bid is None and at:
        pid = here.parcel(at)
        bid = next((x for x in gaps if here.buildings()[x]["parcel"] == pid or here.mill_water(here.buildings()[x]) == pid), None)
    if bid is None and not at and len(gaps) == 1:
        bid = gaps[0]
    if bid is None or bid not in gaps:
        names = ", ".join(here.buildings()[x]["name"] for x in gaps) or "none here"
        raise Refused(f"say which weir or mill's gap (\"at\"): {names}")
    return bid


def _set_gap(here, mind, a):
    """A weir's or a water mill's gap, open or shut (brief 5 §3.2, §3a.1): a weir's by its crew or those who manage it; a mill's by
    those who manage the water wheel. It takes the work of putting the traps or the hatches in, or out."""
    from cybertron2.engine import wild as WL
    bid = _gap_site(here, a.get("at"))
    b = here.buildings()[bid]
    to = str(a.get("to") or "").strip().lower()
    to = {"closed": "shut", "close": "shut", "down": "shut", "up": "open"}.get(to, to)
    if to not in ("open", "shut"):
        raise Refused('set {"thing": "gap", "to": "open" or "shut", "at": the weir or the mill}')
    weir = WL.is_weir(b)
    may = "management" in here.rights(("building", bid)) or (weir and here.name in (b.get("crew") or []))
    if not may:
        who = "its crew or those who manage it" if weir else "those who manage the water wheel"
        raise Refused(f"the gap of {b['name']} is set by {who}")
    if WL.gap(b) == to:
        return f"The gap of {b['name']} is already {to}."
    here.apply("set", ref=("building", bid), field="gap", value=to)
    here.apply("set", ref=("building", bid), field="gap_set", value={"day": here.day, "by": here.name, "to": to})
    what = ("the traps put into the weir's gap" if to == "shut" else "the traps taken out of the weir's gap") if weir else \
        ("the hatches shut, the water held above the dam" if to == "shut" else "the hatches drawn, the water let past the wheel")
    here.event("work", f"{here.name} {'shut' if to == 'shut' else 'opened'} the gap of {b['name']}", actor=here.name,
               about=[f"building:{bid}"], salience=0.4, tags=["food", "fishing"])
    return f"The gap of {b['name']} is now {to}: {what}."


# ---------------------------------------------------------------------- travel (D4-8, D4-32)
def _travel(here, mind, a, party):
    if not str(a.get("to") or "").strip() and here.road_to(a.get("stop at")) is not None:
        a = {**{k: v for k, v in a.items() if k != "stop at"}, "to": a["stop at"]}   # a way named as the stop: it is where one goes
    if not str(a.get("to") or "").strip():
        ways = ", ".join(f"{n} ({k} day{'s' if k > 1 else ''})" for _, n, k, _t in here.roads())
        raise Refused(f'say where in "to" (a place, or a way as the roads name it); from here: {ways or "nowhere"}')
    r = here.road_to(a.get("to"))
    if r is None:
        pid = here.parcel(a.get("to"))
        if pid is not None:                                                     # a place in this village, not a road away (38.75)
            nm = here.parcels()[pid]["name"]
            raise Refused(f"{nm} is here at {here.node_name}, not a road away: name it as where you work in the act itself "
                          f"(\"at\": \"{nm}\"), and you go there to do it")
        ways = ", ".join(f"{n} ({k} day{'s' if k > 1 else ''})" for _, n, k, _t in here.roads())
        raise Refused(f"there is no way from here to {a.get('to')!r}; from here you can go to {ways or 'nowhere'}")
    to, days, track = r
    ox = None
    if a.get("lead") not in (None, "", False):                                # a pack ox (D2-136)
        ox = here.pack_ox(a.get("lead"))
        if ox is None:
            raise Refused("to lead a pack ox you need an ox here and a harness in your hands")
        if not FM._own_or_free(here, ox):                                       # another's ox: allowed and seen (D4-114)
            FM.beasts_note(here, {"animals": {"oxen": 1}})
    load, cap = here.load(), here.capacity(track, oxen=1 if ox else None)
    if load > cap + 1e-9:
        cart = any(ITEMS[i].get("track") for i, q in here.carried().items() if q >= 1)
        raise Refused(f"you carry {math.ceil(load * 10 - 1e-9) / 10:g} weight; you can carry {cap:g} on this road, so set down "
                      f"at least {math.ceil((load - cap) * 10 - 1e-9) / 10:g}"
                      + (" (a cart needs a road with a track, and this one has none)" if cart and not track else ""))
    morning = bool(here.setting("evening")) and str(a.get("when") or "").lower() == "morning"
    if morning:                                                               # set off in the morning, in by nightfall (D4-67)
        here.today().setdefault("travel_morning", {})[here.name] = to
    else:
        here.today()["travel"][here.name] = to
    choices = {k: a[k] for k in ("on trouble", "stop at", "gather", "days", "meeting", "searching", "lead") if a.get(k) not in (None, "", False)}
    if choices:                                                               # the choices for the road (D2-105, D2-109, D2-113)
        here.today().setdefault("travel_choices", {})[here.name] = choices
    here.event("depart", f"{here.name} set off on the road", actor=here.name, salience=0.6, tags=["travel"])
    if morning:
        return (f"You set off this morning: you walk all day" + (f", {days - 1} night{'s' if days > 2 else ''} out on the road," if days > 1 else "")
                + f" and come in at {here.place_name(to)} by nightfall" + (f" of day {here.day + days}" if days > 1 else "")
                + ". Nothing more is done today.")
    if here.setting("evening"):
        return (f"You set off at nightfall: {days} night{'s' if days > 1 else ''} on the road, sleeping out; you come in at midday on day "
                f"{here.day + days + 1}, with half that day's units left. Nothing more is done today.")
    return (f"You set off at the end of the day: {days} day{'s' if days > 1 else ''} on the road, sleeping out; you arrive on the morning "
            f"of day {here.day + days + 1}. Nothing more is done today.")


# ---------------------------------------------------------------------- learning from others, force, rest
def _watch(here, mind, a, party):
    who = here.person(a.get("person") or a.get("to") or a.get("target"))
    if who is None or who == here.name:
        raise Refused(f"there is nobody called {a.get('person')!r} here to watch")
    here.today()["watch"][here.name] = who
    return f"You spend the day working beside {who}, watching how they do things."


def _teach(here, mind, a, party):
    to = here.person(a.get("to"))
    tech = KN.resolve(a.get("what"))
    if to is None or to == here.name:
        raise Refused(f"there is nobody called {a.get('to')!r} here to teach")
    if tech is None:
        raise Refused(f"{a.get('what')!r} is not something you can teach")
    if KN.level(mind, tech) != "known":
        raise Refused(f"you do not know {KN.label(tech)} well enough to teach it")
    here.today()["teach"].append({"by": here.name, "to": to, "tech": tech})
    return f"You set aside time to teach {to} {KN.label(tech)}; it happens if {to} also sets aside time to learn."


def _learn(here, mind, a, party):
    frm = here.person(a.get("from"))
    tech = KN.resolve(a.get("what"))
    if frm is None or frm == here.name:
        raise Refused(f"there is nobody called {a.get('from')!r} here to learn from")
    if tech is None:
        raise Refused(f"{a.get('what')!r} is not something you can learn")
    here.today()["learn"].append({"by": here.name, "from": frm, "tech": tech})
    return f"You set aside time to learn {KN.label(tech)} from {frm}; it happens if {frm} also sets aside time to teach."


def _attack(here, mind, a, party):
    tgt = str(a.get("target", ""))
    aim = "hurt" if str(a.get("aim", "rob")).lower() == "hurt" else "rob"
    who = here.person(tgt)
    if who and who != here.name:
        here.today()["fights"].append({"kind": "attack", "by": here.name, "target": who, "aim": aim, "node": here.node})
        here.event("threat", f"{here.name} squared up to {who}", actor=here.name, target=who, salience=0.7, tags=["danger"], concerns=[who])
        return f"You set on {who} ({aim}); it is settled tonight."
    bid = here.building(tgt)
    if bid:
        if bid in here.homes_here():
            raise Refused("that is your own house")
        here.today()["fights"].append({"kind": "raid", "by": here.name, "building": bid, "node": here.node, "aim": aim})
        if aim == "hurt":                                                      # D4-101: break in and set on those inside
            return f"You make ready to break into {here.buildings()[bid]['name']} tonight and set on those inside."
        return f"You make ready to break into {here.buildings()[bid]['name']} tonight."
    raise Refused(f"no person or building called {tgt!r} here")


def _guard(here, mind, a, party):
    bid = here.building(a.get("at")) if a.get("at") else (here.homes_here() or [None])[0]
    here.today()["guards"][here.name] = bid
    here.apply("set", ref=("person", here.name), field="guarded", value={"day": here.day, "at": bid})   # for its signs (D4-74)
    return "You stand guard tonight" + (f" over {here.buildings()[bid]['name']}." if bid else ".")


def _rest(here, mind, a, party):
    return "You rested."


def _fire(here, mind, a, party):
    """A fire in the open for one night (D4-49): cooking where one sleeps out, from carried fuel by its heat, firewood first, as the
    night burns it (D2-157; D4-94)."""
    from cybertron2.engine import forests as FO
    need, have = float(here.p["heat"]["open"]), FO.heat_of(here.carried())
    if have + 1e-9 < need:
        raise Refused(f"a fire in the open takes {need:g} heat from what you carry ({FO.fuel_words(need)}); "
                      f"you carry {show(have)} heat of fuel")
    here.today().setdefault("fire", {})[here.name] = True
    return f"You mean to light a fire tonight if you sleep out ({need:g} heat: {FO.fuel_words(need)})."


def _accept(here, mind, a, party):
    from cybertron2.engine import agreements as AG
    return AG.accept(here, mind, a, party)


def _release(here, mind, a, party):
    from cybertron2.engine import agreements as AG
    return AG.release(here, mind, a)


def _withdraw(here, mind, a, party):
    from cybertron2.engine import agreements as AG
    return AG.withdraw(here, a)


def _repair(here, bid, m) -> str:
    """A break mended (D2-168): its materials when the mending starts (1 timber, stone for stone, for every 4 spaces of floor, at
    least 2), then its work, two units an action, until it is mended a step. In levels (brief 4 §3) a step is a level, and cheap:
    wattle earth and work, timber or stone one of its stuff, for every `mend_per` spaces of floor."""
    b = here.buildings()[bid]
    from cybertron2.engine import wild as WL
    if WL.is_weir(b):                                                          # a weir mends a section at a time (D2-210)
        return _weir_mend(here, bid, m)
    md = dict(b.get("mending") or {})
    if not md and b.get("level") is not None:
        from cybertron2.engine.data import PHYSICS
        W = PHYSICS["wear"]
        n = max(1, int((BL.floor(b) or 4) // int(W["mend_per"])))
        need = {"materials": {k: v * n for k, v in (W["mend"].get(b.get("structure", "wattle")) or {}).items()}, "units": n}
        if need["materials"]:
            _consume(here, need["materials"], extra=b["stock"] if here.may_take(b["stock"]) else None)
        md = {"units_left": float(need["units"]), "day": here.day}
    if not md:
        need = BL.repair_need(b)
        _consume(here, need["materials"], extra=b["stock"] if here.may_take(b["stock"]) else None)
        md = {"units_left": float(need["units"]), "day": here.day}
    md["units_left"] = round(max(0.0, float(md["units_left"]) - 2 * m), 2)
    if md["units_left"] > 1e-9:
        here.apply("set", ref=("building", bid), field="mending", value=md)
        return f"You worked on mending {b['name']}: about {show(md['units_left'])} units of work left."
    here.apply("set", ref=("building", bid), field="mending", value=None)
    if b.get("level") is not None:
        lv = min(5, BL.level(b) + (3 if b.get("structure") == "camp" and BL.level(b) == 2 else 1))
        here.apply("set", ref=("building", bid), field="level", value=lv)
        here.apply("set", ref=("building", bid), field="level_since", value=here.day)
        if BL.COND_OF_LEVEL[lv] != int(b["condition"]):
            here.apply("set", ref=("building", bid), field="condition", value=BL.COND_OF_LEVEL[lv])
        return f"You mended {b['name']}: it is now {BL.level_word(here.buildings()[bid])}."
    here.apply("set", ref=("building", bid), field="condition", value=b["condition"] + 1)
    return f"You repaired {b['name']}: it is now {('ruined', 'damaged', 'sound')[b['condition']]}."


def _clear_built(here, pid, name, done, party) -> str:
    """A unit of clearing for building (02zh §8): a field, pasture or meadow (4 units a unit of size), or scrub (10: grubbing out the
    roots of a felled wood) becomes built ground, and stops being farmland; held by whoever cleared it if nobody held it (D4-60)."""
    from cybertron2.engine.data import CLEARING
    p = here.parcels()[pid]
    need = float(CLEARING["built"][p["cover"]]) * float(p["size"])
    got = round(float(p.get("clearing_built") or 0.0) + done, 2)
    if got + 1e-9 < need:
        here.apply("set", ref=("parcel", pid), field="clearing_built", value=got)
        return f"You cleared ground for building at {name}: about {max(0, round(need - got, 1)):g} units of work left before it is built ground."
    cover = p["cover"]
    for f, v in (("cover", "built"), ("clearing_built", None), ("clearing", None), ("was", cover), ("crop", None), ("shares", None)):
        here.apply("set", ref=("parcel", pid), field=f, value=v)
    if "grass" in p["res"]:
        here.apply("set_res", parcel=pid, key="grass", fields={"S": 0.0, "K": 0.0})
    who = party or here.household() or here.name
    held = bool(here.claims(("parcel", pid)))
    if not held:
        here.apply("claim", thing=("parcel", pid), claimant=who, rights="all", grounds="cleared")
    total = BL.ground_total(here.parcels()[pid])
    here.event("work", f"{here.name} finished clearing {name} for building: it is built ground now", actor=here.name,
               about=[f"parcel:{pid}"], salience=0.6, tags=["building"])
    return (f"You finished clearing {name}: it is built ground now, {total} spaces for building"
            + ("." if held else ", and yours: you cleared it."))


# ---------------------------------------------------------------------- clearing new ground (Zach, 24 Oct)
def _clear(here, pid, name, done, party) -> str:
    """A unit of clearing: progress on the parcel; when its work is done it is a field, fallow, held by whoever cleared it by the
    custom of the land if nobody held it (a claim, grounds "cleared")."""
    from cybertron2.engine.data import CLEARING
    p = here.parcels()[pid]
    need = float(CLEARING[p["cover"]]) * float(p["size"])
    got = round(float(p.get("clearing") or 0.0) + done, 2)
    if got + 1e-9 < need:
        here.apply("set", ref=("parcel", pid), field="clearing", value=got)
        return f"You cleared ground at {name}: about {max(0, round(need - got))} units of work left before it is a field."
    cover = p["cover"]
    for f, v in (("cover", "field"), ("clearing", None), ("was", cover), ("crop", None), ("last_crop", "fallow"), ("broken", 0.0),
                 ("fertility", p.get("fertility") if p.get("fertility", 1.0) != FM.base(p) else float(CLEARING["fertility"][cover]) * FM.base(p))):
        here.apply("set", ref=("parcel", pid), field=f, value=v)
    who = party or here.household() or here.name
    held = bool(here.claims(("parcel", pid)))
    if not held:
        here.apply("claim", thing=("parcel", pid), claimant=who, rights="all", grounds="cleared")   # all its plots (D2-163)
    else:
        here.apply("shares", parcel=pid)                                      # its holders' plots become field holdings
    here.event("work", f"{here.name} finished clearing {name}: it is a field now, ready to be sown", actor=here.name,
               about=[f"parcel:{pid}"], salience=0.6, tags=["farming", "building"])
    return f"You finished clearing {name}: it is a field now, ready to be broken and sown" + ("." if held else ", and yours: you cleared it.")


# ---------------------------------------------------------------------- partners, children, the household's offices (D2-138 to D2-153)
def _units(x) -> int:
    try:
        return max(1, int(float(x if x is not None else 1)))
    except (TypeError, ValueError):
        raise Refused("units must be a number")


def _here_person(here, x, what="person"):
    who = here.person(x)
    if who is None or who == here.name:
        raise Refused(f"there is nobody called {x!r} here")
    return who


def _grown(here, who) -> bool:
    return here.body(who)["stage"] in ("youth", "adult", "elder")


def _partner(here, mind, a, party):
    who = _here_person(here, a.get("with") or a.get("person"))
    if not _grown(here, here.name) or not _grown(here, who):
        raise Refused(f"{who} is a child")
    if here.body(here.name)["partner"] == who:
        raise Refused(f"{who} is your partner already")
    here.today().setdefault("partner", []).append({"by": here.name, "with": who})
    return f"You chose {who} as your partner; it is so if {who} chooses you too today."


def _part(here, mind, a, party):
    who = here.body(here.name)["partner"]
    if not who:
        raise Refused("you have no partner")
    here.apply("partner", person=here.name, other=who, on=False)
    here.event("household", f"{here.name} and {who} have parted", actor=here.name, target=who, salience=0.6, tags=["family"],
               concerns=[who])
    return f"You and {who} are no longer partners."


def _try(here, mind, a, party):
    who = _here_person(here, a.get("with") or a.get("person"))
    me, them = here.body(here.name), here.body(who)
    if not me["sex"] or me["sex"] == them["sex"]:
        raise Refused("a child needs a man and a woman")
    if me["stage"] != "adult" or them["stage"] != "adult":
        raise Refused("you must both be grown adults")
    woman = here.name if me["sex"] == "f" else who
    if here.body(woman)["with_child"]:
        raise Refused(f"{'you are' if woman == here.name else woman + ' is'} with child already")
    if woman == here.name and here.life()["gap"]:
        raise Refused("you gave birth lately and cannot conceive yet")
    units = _units(a.get("units"))
    here.today().setdefault("try", []).append({"by": here.name, "with": who, "units": units})
    return f"You spent {units} unit{'s' if units > 1 else ''} trying for a child with {who}; it counts only if {who} tries with you today."


def _care(here, mind, a):
    x = a.get("at") or a.get("person") or a.get("child")
    who = here.person(x)
    young = [n for n in here.people(me=False) if here.body(n)["stage"] in ("infant", "child")]
    if who is None and len(young) == 1 and not x:
        who = young[0]
    if who not in young:
        raise Refused(f"there is no child called {x!r} here" + (f"; the children here: {', '.join(young)}" if young else ""))
    gift, bits = {"by": here.name}, []                                         # food from one's hands, and a sentence passed on (D4-64)
    item = a.get("item")
    if item:
        if item not in ITEMS or not float(ITEMS[item]["food"]):
            raise Refused(f"{item!r} is not food")
        have = float(here.carried().get(item, 0.0))
        if have <= 1e-9:
            raise Refused(f"you carry no {item}")
        qty = min(have, float(a.get("qty") or have))
        gift.update(item=item, qty=qty)
        bits.append(f"you mean to give {who} {show(qty)} {item} tonight")
    said = " ".join(str(a.get("pass") or "").split())
    if said:
        gift["pass"] = said
        bits.append(f"you passed on to {who}: “{said}”")
    t = here.today()
    t.setdefault("care", {})[who] = t.setdefault("care", {}).get(who, 0) + 1
    t.setdefault("care_by", {}).setdefault(who, [])
    if here.name not in t["care_by"][who]:
        t["care_by"][who].append(here.name)
    here.record("work", "care", who)
    if len(gift) > 1:
        gifts = t.setdefault("care_gift", {}).setdefault(who, [])
        gifts[:] = [g for g in gifts if g["by"] != here.name] + [gift]
    return f"You looked after {who} (fed, minded and kept warm)" + ("; " + "; ".join(bits) if bits else "") + "."


def _tags(here) -> bool:
    return bool(here.setting("tags"))


def _name_thing(here, a):
    """Naming a group of beasts or a thing by its tag (D4-68): the name is known to the namer, everyone here and the household."""
    new = " ".join(str(a.get("as") or "").split())[:40]
    if not new:
        raise Refused('say the name in "as"')
    x = a.get("thing") or a.get("what") or a.get("at")
    tag = here.tag_of(x)
    if not tag or not here.tagged_here(tag):
        raise Refused(f"there is nothing here tagged or called {x!r} that you know of; name a group of beasts or a thing here by its tag")
    who = here.give_name(tag, new)
    here.event("name", f"{here.name} named {tag} {new}", actor=here.name, salience=0.2, sense="sound")
    others = [m for m in who if m != here.name]
    return f"You named {tag} “{new}”" + (f"; {', '.join(others)} will know it by that name." if others else ".")


def _name(here, mind, a, party):
    if a.get("as"):
        return _name_thing(here, a)
    hh = here.household()
    if hh is None:
        raise Refused("you belong to no household")
    members = here.institution(hh)["members"]
    pick = lambda x: next((m for m in members if m.lower() == str(x or "").strip().lower()), None)
    dead = lambda x: (mind.kin().get(x) or {}).get("alive") is False             # dead, as one knows it (D4-95; the engine's
                                                                                # succession counts only the living either way)
    if a.get("heir"):
        if here.head(hh) != here.name:
            raise Refused(f"only the head of {here.institution(hh)['name']} names its heir")
        who = pick(a["heir"])
        if who is None or who == here.name:
            raise Refused(f"{a['heir']!r} is not of your household")
        if dead(who):
            raise Refused(f"{who} is dead: only the living can head a household")
        here.apply("office", inst=hh, field="heir", value=who, by=here.name)
        return f"You named {who} to head {here.institution(hh)['name']} after you."
    if a.get("head"):
        sc = here.life()["succession"]
        if not sc:
            raise Refused("the household has a head; only when a head has died do its members name the next")
        if not _grown(here, here.name) or here.body(here.name)["stage"] == "youth":
            raise Refused("only the grown members name the head")
        who = pick(a["head"])
        if who is None:
            raise Refused(f"{a['head']!r} is not of your household")
        if dead(who):
            raise Refused(f"{who} is dead: only the living can head a household")
        here.apply("office", inst=hh, field="named", value=who, by=here.name)
        return f"You named {who} as the head of {here.institution(hh)['name']}; the one most named heads it."
    raise Refused('say "heir" or "head"' + (', or "thing" and "as" to name a group of beasts or a thing' if _tags(here) else ""))


def _meet(here, mind, a, party):
    """Call a meeting for tomorrow morning at a building or a place here (D4-77)."""
    at = a.get("at") or a.get("to")
    bid = here.building(at)
    pid = None if bid else here.parcel(at)
    if bid is None and pid is None:
        raise Refused(f"say where to meet: a building or a place here, not {at!r}")
    name = here.buildings()[bid]["name"] if bid else here.parcels()[pid]["name"]
    about = " ".join(str(a.get("about") or "").split())[:160]
    here.apply("set", ref=("building", bid) if bid else ("parcel", pid), field="meeting",
               value={"day": here.day + 1, "by": here.name, "about": about, "at": name})
    here.event("meeting", f"{here.name} called a meeting at {name} for tomorrow morning" + (f" about {about}" if about else ""),
               actor=here.name, salience=0.5, sense="sound", tags=["talk"])
    return f"You called a meeting at {name} for tomorrow morning, before the day's work" + (f", about {about}" if about else "") + \
        ": everyone here will hear of it, and whoever comes gives a unit to it."


def _come(here, mind, a, party):
    m = here.meeting_today()
    if m is None:
        raise Refused("no meeting has been called here for this morning")
    return f"You went to the meeting at {m['at']} this morning."


def _order(here, mind, a, party):
    from cybertron2.engine.data import LIFE
    hh = here.household()
    if hh is None or here.head(hh) != here.name:
        raise Refused("only the head of a household sets its children's work")
    what = str(a.get("what") or "").strip().lower()
    if what in ("nothing", "none", "rest", ""):
        here.apply("office", inst=hh, field="order", value=None, by=here.name)
        return "Your household's children do no work now."
    tech = KN.resolve(what, None)
    if tech not in LIFE["children_work"]:
        from cybertron2.engine import packs as PK
        raise Refused(f"children can do only {', '.join(t for t in LIFE['children_work'] if PK.on(TECHNIQUES[t]))}")
    at = a.get("at")
    if at:
        _site(here, mind, tech, at)                                           # a place here it can be done
    here.apply("office", inst=hh, field="order", value={"what": tech, "at": at, "node": here.node}, by=here.name)
    return f"Your household's children will {TECHNIQUES[tech]['label'].split(' (')[0]} each day" + (f" at {at}." if at else ".")


HANDLERS = {"gather": _gather, "work": _work, "make": _make, "build": _build, "move": _move, "take": _take, "give": _give,
            "accept": _accept, "withdraw": _withdraw, "release": _release, "host": _host, "grant": _grant, "revoke": _revoke, "join": _join, "admit": _admit,
            "leave_household": _leave_household, "found": _found, "claim": _claim, "sleep": _sleep, "set": _set, "travel": _travel,
            "watch": _watch, "teach": _teach, "learn": _learn, "attack": _attack, "guard": _guard, "fire": _fire, "rest": _rest,
            "drive": lambda here, mind, a, party: FM.drive(here, a, party), "partner": _partner, "part": _part, "try": _try,
            "name": _name, "order": _order, "meet": _meet, "come": _come, "write": _write, "erase": _erase}
assert set(HANDLERS) == set(VERB)
