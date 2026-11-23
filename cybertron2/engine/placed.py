"""Placed gear: set from the hands and tended (u2_taking.md §2, §3, §4.1, §5; D2-294, D2-304, D2-305; fault 12): the acts of the
placed-gear unit (D2-244). Its data are the set methods' rows (wild/methods.py `SETS`) and the gear's (engine/gear.py); its night is
engine/wild.py's `_set_night` and the river's wreck; its words are here. It reads the world only through `Here` (D4-35).

- **set** lays gear one holds (wicker traps, snares, a gill net, a set line) at a place: up to six traps or 25 snares an act (D2-264),
  a net or a set line; refused with none in hand, naming one's gear already standing and how to tend it. The set thing is the
  setter's household's (`household`), its gear and pieces kept apart from its catch.
- **tend** goes back to one's own placed gear at a place: one unit for all of one's own of that technique there (D2-304: a
  yield-taking act takes all of one's own); the catch into hand, the sound pieces set again, the broken brought home to mend; `up`
  brings it all home; `to` moves snares to another place. Named by its tag, another's gear is emptied as theft (stage 1's words).
- **a technique named alone** (`gather wicker traps`) tends one's own standing there, sets if none stands and one holds the gear,
  else is refused saying where one's gear is.
"""
from __future__ import annotations

from cybertron2.engine import gear as GE
from cybertron2.engine.here import Refused, show

METHODS = ("trap in water", "snare", "gill net", "set line")
WATER = ("trap in water", "gill net", "set line")
NOUN = {"trap in water": ("wicker trap", "wicker traps", "traps"), "snare": ("snare", "snares", "snares"),
        "gill net": ("gill net", "gill nets", "net"), "set line": ("set line", "set lines", "set line")}
WORDS = {"trap in water": ("wicker trap", "wicker traps", "traps", "trap", "eel traps", "eel trap", "trap in water", "traps in the water",
                           "wicker"),
         "snare": ("snare", "snares", "nooses", "noose", "snare line", "a line of snares"),
         "gill net": ("gill net", "gill nets", "net", "nets", "fish net"),
         "set line": ("set line", "set lines", "long line", "line of hooks", "hooks")}


def method_of(what) -> str | None:
    """The set method a phrase names: the gear ("wicker traps", "my snares", "the net") or the method's own name or aliases."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    low = str(what or "").strip().lower()
    for pre in ("my ", "the ", "our ", "a ", "some "):
        low = low.removeprefix(pre)
    for tech in METHODS:
        if tech in TECHNIQUES and (low == tech or low in WORDS[tech]):
            return tech
    t = KN.resolve(what, "gather")
    return t if t in METHODS else None


def noun(tech, n=2) -> str:
    one, many, _ = NOUN.get(tech, ("thing", "things", "things"))
    return one if n == 1 else many


def _n_words(tech, n) -> str:
    return f"{'a' if n == 1 else n} {noun(tech, n)}"


def _tag(here, c) -> str:
    return c.get("tag") if c.get("tag") and here.setting("tags") else ""


def _food(goods) -> float:
    from cybertron2.engine.data import ITEMS
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0)) for i, q in goods.items() if float(q) > 1e-9)


def _kg(goods) -> float:
    from cybertron2.engine.data import ITEMS
    return sum(float(q) * float((ITEMS.get(i) or {}).get("weight", 1.0)) for i, q in goods.items()
               if float(q) > 1e-9 and float((ITEMS.get(i) or {}).get("food", 0.0)) > 0)


def count_words(here, c) -> str:
    """The doer's own count of the heads in a set thing (u2 §5 rule 4): '11 eels', 'a hare and two salmon'."""
    n = {}
    for x in (c.get("catch") or []):
        n[x["kind"]] = n.get(x["kind"], 0) + int(x.get("n", 1))
    if not any(float(q) > 1e-9 for q in c["goods"].values()):
        return ""
    bits = [(("an " if k[0] in "aeiou" else "a ") + k) if q == 1 else f"{q} {here.plural(k)}"
            for k, q in sorted(n.items(), key=lambda kv: (-kv[1], kv[0]))]
    return " and ".join(bits)


def fishes(mind) -> bool:
    """One who fishes (u8 §0): any water craft from a rough idea up."""
    from cybertron2.engine import knowledge as KN
    return any(KN.level(mind, t) in ("rough", "capable", "known") for t in ("trap in water", "gill net", "set line", "weir", "net",
                                                                           "fish by hand", "angle") if t in mind.know)


def standing(here, tech=None, pid=None, own=True, include_weir=False) -> list:
    """Set things standing here [(cid, thing)], newest first: of a technique, at a parcel, one's own (or another's: own=False)."""
    out = []
    for cid, c in sorted(here.sets().items()):
        sp = c.get("set") or {}
        if sp.get("weir") and not include_weir:
            continue
        if tech and sp.get("method") != tech:
            continue
        if pid and c.get("parcel") != pid:
            continue
        if own is not None and here.owns_set(c) != own:
            continue
        out.append((cid, c))
    return sorted(out, key=lambda x: (-int((x[1].get("set") or {}).get("set_day", 0)), x[0]))


def _standing_words(here, tech, items) -> str:
    """'your 6 are in the Isel (T7, set autumn day 2)' for one's gear standing."""
    bits = []
    for cid, c in items:
        n = GE.fishing(c) or sum(GE.laid(c).values())
        day = here.day_words(int((c.get("set") or {}).get("set_day", here.day)))
        tag = _tag(here, c)
        bits.append(f"your {n} {'is' if n == 1 else 'are'} in {here.spot_name(c)} ({(tag + ', ') if tag else ''}set {day})")
    return "; ".join(bits)


def _iced_words(here, pid, tech) -> str:
    name = here.parcels()[pid]["name"]
    if tech == "trap in water":
        return f"The edges of {name} are ice: a trap set there now would take nothing until the thaw."
    return f"The edges of {name} are ice: {noun(tech, 1)} set there now would take nothing until the thaw."


# ---------------------------------------------------------------------------------------------------------------------- set
def lay(here, mind, tech, key, place_name, qty=None) -> str:
    """Set: lay gear one holds at a place (u2 §3; fault 12). Refused with none in hand, naming one's gear standing."""
    from cybertron2.engine.data import TECHNIQUES
    item = GE.SET_GEAR[tech]
    have = here.sound_held(item)
    mine = standing(here, tech)
    if have <= 0:
        why = f"You have no {noun(tech)} in hand"
        if mine:
            tags = ", ".join(_tag(here, c) for _, c in mine if _tag(here, c))
            why += f": {_standing_words(here, tech, mine)}. To take what they hold, tend " + (tags or "them")
        else:
            if GE.count({"goods": here.carried()}, item):
                why += " sound enough to set: they want mending"
            from cybertron2.engine import knowledge as KN
            craft = GE.craft_of(item)
            if craft and KN.level(mind, craft) in ("rough", "capable", "known"):
                why += f" ({noun(tech)} are made: make {craft})"
        raise Refused(why.rstrip(".") + ".")
    if tech in WATER and here.parcels()[key]["cover"] not in ("water", "fen"):
        waters = ", ".join(p["name"] for p in here.parcels().values() if p["cover"] in ("water", "fen")) or "nowhere"
        raise Refused(f"{noun(tech, 2).capitalize()} are set in water: here that is {waters}.")
    if tech in WATER and here.ice(key) != "open":
        raise Refused(_iced_words(here, key, tech))
    most = int(GE.SET_MOST.get(item, 1))
    want = most if qty in (None, "", 0) else max(1, int(float(qty)))
    n = min(want, most, have)
    sp = TECHNIQUES[tech]["set"]
    cid = here.apply("new_thing", node=here.node, parcel=key, kind="set", by=here.name, household=here.household(),
                     set={"method": tech, "base": float(sp["base"]), "set_day": here.day, "tended": here.day, "line": n,
                          "holds": int(sp.get("holds", 1)) * n, "gear": {}, "pieces": {}, "state": "fishing"})
    here.apply("lay", src=here.hands, dst=cid, item=item, qty=n)
    here.remember_thing(cid, "put")
    tag = _tag(here, here.thing(cid))
    where = f"in {place_name}" if tech in WATER else f"on the runs of {place_name}"
    out = f"You set {_n_words(tech, n)} {where}" + (f" ({tag})" if tag else "") + "."
    if want > most and have > most:
        out += f" ({most} is as many as one setting lays.)"
    elif n < want:
        out += f" You held only {n}."
    others = [(c2, x) for c2, x in standing(here, tech, key) if c2 != cid and GE.fishing(x) > 0]
    if others:
        out += " Your " + "; ".join(f"{GE.fishing(x)} there of {here.day_words(int(x['set']['set_day']))}"
                                    + (f" ({_tag(here, x)})" if _tag(here, x) else "") for _, x in others) + " still stand."
    if tech in WATER:
        out += water_tonight(here, mind, key)
    left = here.sound_held(item)
    if left:
        out += f" You hold {left} more."
    return out


def water_tonight(here, mind, key) -> str:
    """The water's axis at a setting (u2 §4.1; u8): for one who fishes, what runs there now; for anyone, a spate or a flood tonight."""
    name = here.parcels()[key]["name"]
    out = ""
    if fishes(mind):
        run = here.run_kinds(key)
        if "eel" in run:
            out += f" Eels are going down {name} tonight."
        elif run:
            out += f" {', '.join(k.capitalize() if i == 0 else k for i, k in enumerate(sorted(here.plural(x) for x in run)))} " \
                   f"{'are' if len(run) > 1 or True else 'is'} running in {name}."
    flow = here.flow_tonight()
    name = name[:1].upper() + name[1:]
    if flow == "spate" and here.river_parcel(key):
        out += f" {name} is in spate: traps in its main stream are torn away in water like this, half of them or more."
    elif flow == "flood" and here.river_parcel(key):
        out += f" {name} is in flood: traps in its main stream are torn away in water like this, nearly all of them."
    return out


# ---------------------------------------------------------------------------------------------------------------------- tend
def tended(here, c) -> None:
    """The parcel of a set thing one tended today (W-102): the river's signs read who was at the water (the catch carried home, u8
    §2.4), kept apart from `worked` so the day's act draws are as they were."""
    pid = c.get("parcel")
    try:
        today = here.today()
    except KeyError:
        return
    if pid and pid not in today.setdefault("tended", {}).setdefault(here.name, []):
        today["tended"][here.name].append(pid)


def tend_one(here, mind, cid, up=False, to=None, theft=False) -> str:
    """Tend one set thing (u2 §3, §4.1): the catch into hand; the sound pieces set again (or, `up`, all brought home); the broken
    brought home to mend; what the night did to it said. Another's named: emptied as theft, not set again."""
    c = here.thing(cid)
    sp = c.get("set") or {}
    tech = sp.get("method")
    name = here.spot_name(c)
    tag = _tag(here, c)
    goods = {i: float(q) for i, q in c["goods"].items() if float(q) > 1e-9}
    catch = count_words(here, c)
    kg, food = _kg(goods), _food(goods)
    tended(here, c)
    for it, q in sorted(goods.items()):
        here.apply("transfer", src=cid, dst=here.hands, item=it, qty=q)
    here.apply("set_thing", cid=cid, field="catch", value=[])
    here.apply("set_thing", cid=cid, field="caught", value=0)
    got = (f"{catch}, " if catch else "") + (f"about {show(kg)} kg of {'fish' if tech in WATER else 'meat'} (food worth about "
                                              f"{max(1, round(food))} meal{'s' if max(1, round(food)) != 1 else ''})" if kg > 0 else
                                              ", ".join(f"{show(q)} {i}" for i, q in sorted(goods.items())) or "")
    if theft:
        owner = c.get("by") or "another"
        here.apply("set_thing", cid=cid, field="robbed", value={"day": here.day, "by": here.name})
        for it, q in sorted(goods.items()):
            here.today()["thefts"].append({"by": here.name, "thing": cid, "item": it, "qty": round(q, 2)})
        here.event("take", f"{here.name} emptied the {noun(tech)} {owner} set at {name}", actor=here.name, salience=0.55,
                   about=[f"parcel:{c['parcel']}"], tags=["food", "hunting"], concerns=[owner])
        here.record("take", None, None, theft=True)
        here.remember_thing(cid, "took")
        return (f"You emptied {owner}'s {noun(tech)} in {name}" + (f" ({tag})" if tag else "") + ", which are not yours to take from: "
                + (got or "nothing was in them") + ". Whether anyone saw, you will learn.")
    if "gear" not in sp:                                                       # an older world's set: its catch, and it stands as it was
        here.apply("set_thing", cid=cid, field="set", value=dict(sp, tended=here.day))
        here.remember_thing(cid, "put")
        return (f"You tended your {noun(tech)} in {name}" + (f" ({tag})" if tag else "") + ": " + (got or "nothing in them")
                + ". You set them again.")
    gear = GE.laid(c)
    n0 = sum(gear.values())
    lost = dict(sp.get("lost") or {})
    inside = ", ".join(x for x in (tag, f"{n0} {noun(tech, n0)}" if n0 else "") if x)
    out = f"You tended your {noun(tech, max(1, n0))} in {name}" + (f" ({inside})" if inside else "") + ": "
    out += (got or "nothing in them") + "."
    if sp.get("full") and int(sp.get("full")) >= int(sp.get("tended", -1)):
        out += " They were full by morning."
    night = sp.get("night") or {}
    if fishes(mind) and tech in WATER and int(night.get("day", -9)) >= int(sp.get("tended", -1)):
        if night.get("run") and sp.get("full"):
            out += " Eels were still going down past them."
        elif night.get("run"):
            out += " Fish were running past them in the night."
        elif not goods:
            out += " Nothing ran last night."
    rb = c.get("robbed_by") or {}
    if rb and int(rb.get("day", -9)) >= int(sp.get("tended", -1)):
        out += f" An otter had been at them first: scales on the withies, {int(rb.get('n', 1))} gone."
    for why, words in (("spate", "torn from their stakes in the spate"), ("flood", "torn from their stakes in the flood"),
                       ("thaw", "crushed in the ice as it went out"), ("rotted", "rotted through and gone")):
        k = int(lost.get(why, 0))
        if k:
            out += f" {k} {noun(tech, k)} {'is' if k == 1 else 'are'} gone, {words}."
    if sp.get("state") == "idle":
        out += " The water is frozen at the edges: nothing has come to them."
    item = GE.SET_GEAR.get(tech)
    if not gear:
        here.apply("set_thing", cid=cid, field="set", value=dict(sp, state="spent", sprung=here.day, lost={}, tended=here.day))
        return out + f" Nothing of {tag or 'them'} is left standing."
    broken = sum(1 for p in GE.laid_pieces(c, item) if not GE.sound(p)) if GE.pieced(item) else 0
    if up:
        k = here.apply("unlay", src=cid, dst=here.hands, item=item, qty=gear.get(item, 0))
        here.apply("set_thing", cid=cid, field="set", value=dict(here.thing(cid)["set"], state="up", sprung=here.day, lost={},
                                                                tended=here.day))
        return out + f" You took them up: {_n_words(tech, k)} in hand" + (f" ({broken} worn past use, wanting mending)" if broken else "") + "."
    if broken:
        here.apply("unlay", src=cid, dst=here.hands, item=item, qty=broken, broken=True)
        out += f" {broken} {'is' if broken == 1 else 'are'} worn past use and want{'s' if broken == 1 else ''} mending: you took " \
               f"{'it' if broken == 1 else 'them'} home."
    sp2 = here.thing(cid)["set"]
    left = GE.fishing(here.thing(cid))
    if to:
        here.apply("set_thing", cid=cid, field="parcel", value=to)
        out += f" You moved them to {here.parcels()[to]['name']} and set them again."
    elif left:
        out += " You set them again." if left > 1 or tech != "gill net" else " You set it again."
    here.apply("set_thing", cid=cid, field="set", value=dict(sp2, tended=here.day, lost={}, full=None,
                                                            state="fishing" if left else "spent",
                                                            **({"sprung": here.day} if not left else {})))
    here.apply("set_thing", cid=cid, field="robbed_by", value=None)
    here.remember_thing(cid, "put")
    return out


def tend_verb(here, mind, a) -> str:
    """The `tend` act (u2 §3): {thing?: a tag, at?: place, what?: the gear, up?: true, to?: a place}. With a tag, that thing (another's,
    as theft); else all of one's own of that kind at the place (D2-304)."""
    from cybertron2.engine import tags as TG
    up = str(a.get("up") or "").strip().lower() in ("true", "yes", "1", "up")
    to = None
    if a.get("to"):
        to = here.parcel(a["to"])
        if to is None:
            raise Refused(f"there is no place called {a['to']!r} here")
    ref = a.get("thing") or a.get("what") or ""
    tag = TG.tag_in(str(ref)) if here.setting("tags") else None
    if tag or (a.get("thing") and here.find_thing(a["thing"]) is not None):
        cid = here.find_thing(a["thing"] if a.get("thing") else ref)
        c = here.thing(cid) if cid else None
        if not c or c.get("kind") != "set":
            raise Refused(f"you know of no set gear called {ref} here")
        if (c.get("set") or {}).get("weir"):
            return tend_weir(here, mind, cid)
        if not here.owns_set(c):
            return tend_one(here, mind, cid, theft=True)
        if to and (c.get("set") or {}).get("method") != "snare":
            raise Refused("only snares are moved as they are tended (\"to\"); traps and nets are taken up and set again")
        return tend_one(here, mind, cid, up=up, to=to)
    tech = method_of(a.get("what")) if a.get("what") else None
    if a.get("what") and tech is None and str(a.get("what")).strip().lower() in ("weir", "the weir", "weir traps", "the weir's traps"):
        cid = next((x for x, c in standing(here, None, None, own=True, include_weir=True) if (c.get("set") or {}).get("weir")), None)
        if cid is None:
            raise Refused("you work no weir here")
        return tend_weir(here, mind, cid)
    pid = here.parcel(a.get("at")) if a.get("at") else None
    if a.get("at") and pid is None:
        raise Refused(f"there is no place called {a.get('at')!r} here")
    mine = standing(here, tech, pid)
    weir = [x for x in standing(here, None, pid, own=True, include_weir=True) if (x[1].get("set") or {}).get("weir")] if tech in (None, "trap in water") else []
    if not mine and weir and not a.get("what"):
        return tend_weir(here, mind, weir[0][0])
    if not mine:
        where = here.parcels()[pid]["name"] if pid else "here"
        others = standing(here, tech, pid, own=False)
        out = f"You have no {noun(tech) if tech else 'set gear'} {'in ' + where if pid else 'set here'}."
        if others:
            out += " " + "; ".join(f"{_tag(here, c) or 'what stands'} there is {c.get('by')}'s" for _, c in others[:3]) + "."
        mine_any = standing(here, tech)
        if mine_any and pid:
            out += f" Elsewhere {_standing_words(here, tech, mine_any)}."
        raise Refused(out)
    places = sorted({c["parcel"] for _, c in mine})
    if len(places) > 1 and not pid:
        names = "; ".join(f"{here.parcels()[p]['name']} ({', '.join(_tag(here, c) for _, c in mine if c['parcel'] == p and _tag(here, c))})"
                          for p in places)
        raise Refused(f"your {noun(tech) if tech else 'gear'} stand in more than one place: say which (\"at\"): {names}")
    if to and any((c.get("set") or {}).get("method") != "snare" for _, c in mine):
        raise Refused("only snares are moved as they are tended (\"to\"); traps and nets are taken up and set again")
    return " ".join(tend_one(here, mind, cid, up=up, to=to) for cid, _ in mine)


def tend_weir(here, mind, cid) -> str:
    """The weir's traps emptied by its crew or holders (u2 §4.3), 1 unit for all its traps; another's, named, is theft."""
    c = here.thing(cid)
    name = here.spot_name(c)
    tag = _tag(here, c)
    goods = {i: float(q) for i, q in c["goods"].items() if float(q) > 1e-9}
    if not here.owns_set(c):
        holders = ", ".join(c.get("crew") or []) or "its crew"
        raise Refused(f"the weir's traps at {name} are {holders}'" + (f" ({tag})" if tag else "") + "; you are not of its crew")
    catch = here.catch_words(c)
    tended(here, c)
    for it, q in sorted(goods.items()):
        here.apply("transfer", src=cid, dst=here.hands, item=it, qty=q)
    here.apply("set_thing", cid=cid, field="catch", value=[])
    here.apply("set_thing", cid=cid, field="caught", value=0)
    here.remember_thing(cid, "took")
    if not goods:
        return f"You emptied the weir's traps at {name}" + (f" ({tag})" if tag else "") + ": nothing was in them."
    return (f"You emptied the weir's traps at {name}" + (f" ({tag})" if tag else "") + f": about {show(_kg(goods))} kg of fish"
            + (f", {catch}" if catch else "") + f" (food worth about {max(1, round(_food(goods)))} meal{'s' if max(1, round(_food(goods))) != 1 else ''}).")


# ---------------------------------------------------------------------------------------------------------------------- named alone
def named_alone(here, mind, tech, key, place_name, a) -> str:
    """A set technique named alone (u2 §3): tends one's own standing at the place; sets if none stands and one holds the gear; else
    refused, saying where one's gear is or that one has none. The result says which was done and how to ask for the other."""
    mine = standing(here, tech, key)
    item = GE.SET_GEAR[tech]
    if mine and not a.get("_new_set"):
        out = " ".join(tend_one(here, mind, cid) for cid, _ in mine)
        if here.sound_held(item):
            out += f" To lay the {here.sound_held(item)} {noun(tech, here.sound_held(item))} you carry beside them, set {noun(tech)}."
        return out
    return lay(here, mind, tech, key, place_name, a.get("qty"))
