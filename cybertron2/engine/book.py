"""The household book (u6; D2-274, D2-279, D2-296, D2-301, D2-319; the rules' grammar D2-337, D2-338, D2-339; the build's stage 3,
W-99, rebuilt W-102): one book a household and one a person, in which the routine is set as records in a stated grammar. The engine
reads the fields, never the words (D2-337); the person's own sentence ("words") is shown beside the engine's reading. A rule reads
only what its household knows; going against a household rule is recorded.

The grammar (D2-339): rules come in the reply's own field "rules": [...] (free, at any time or in the evening; the old `rule` act is
still read), each one of five kinds, or drop:
  - set   {"name", "people"?, "goods"?, "places"?}: a named set; sets may hold sets (D2-338). Built in: people everyone, adults,
          children, elders, the head, whoever has time; goods the engine's kinds (fish, meat, grain, fuel, fresh food, keeping food...);
  - keep  {"goods", "in"?, "at least"?}: where a good lives (the sort) and a floor not eaten, drawn or used;
  - first {"goods": [ordered goods or sets]}: everything in the first, then the next, at the meal and in drawing;
  - share {"order"?: [people or sets, fed first when short], "who"?, "qty"?: full | half | a fraction, "goods"?}: the meal;
  - do    {"who"?, "act": an ordinary act, "when"?, "unless"?}: done with units left over; with no condition, a fallback;
  - drop  {"n"}.
Shared fields: "for": household | me, "words", "n" (to change one). Conditions are objects only: an amount {"goods"?, "in"?, "under"
| "over" | "full" | "room"}; a process {"in", "state": done | in process | fire out}; {"arrives": goods}; {"season"}; {"seen": the
run | frost | the river rising | rats}; {"starving": a person, a set or anyone}; {"home": a person}. Precedence: one's own before the
household's; a rule naming one person or good before one naming a set; newer before older. A rule missing a field or with a value
that cannot be read is refused naming the field and its form. Old records (go, hold back, eat, move, tend, chore) are converted as
they are read (`convert`), or dropped where they cannot be.

One feature unit (D2-244; feature_packages.md §9.1, §10):
  - data: s["books"]["household:<id>" or "person:<name>"] = {"rules": [rule], "n": next number, "proposals": [rule]}, written through
    the `book` primitive (world.py);
  - acts: the reply's "rules" field (`apply_rules`), the `rule` act (`act`); the reply's `fallback` field sets one's standing
    fallback (`set_fallback`: an own `do` with no condition), which stands until changed (L-142);
  - the store moments: `where_to` and `_arrive` (goods arriving go where a `keep` puts them), `keeps` (the sort), `held` (the floor a
    `keep` sets, at drawing and the meal), `meal` and `meal_order` (first, share);
  - processes: `spare_units` after every plan (D2-301: person by person, their own `do` rules first, then the household's);
  - what each sees: `rules_block` (the system prompt), `reading`, `morning_lines`, the day's record in today["book"].
"""
from __future__ import annotations

import json
import re

KINDS = ("set", "keep", "first", "share", "do", "drop")
OLD_KINDS = ("go", "hold back", "eat", "move", "tend", "chore")                 # read as before D2-339, converted (`convert`)
ROUNDS = 3                                           # cascades: at most three rounds of the household's rules a day
MOVE_KG_STEP = 800.0                                 # moving between buildings: 1 unit per 800 kg a parcel step (D2-274, provisional)
FREE_OR_TRAVEL = ("travel", "rest", "rule", "give", "accept", "offer", "withdraw", "release", "host", "grant", "revoke", "join", "admit",
                  "leave_household", "found", "claim", "sleep", "partner", "part", "name", "order", "meet", "write", "erase", "attack")
SEEN = {"run": ("running", "the run", "eels", "salmon", "lamprey", "shoal", "fish going up", "fish coming down"),
        "frost": ("frost", "ice on", "iced", "frozen"), "river rising": ("river is up", "rising", "spate", "flood", "brown and fast"),
        "rats": ("rats", "droppings", "gnaw", "mice")}
SEASONS = ("spring", "summer", "autumn", "winter")
KIND_GOODS = {"fish": ("fish",), "meat": ("meat",), "grain": ("grain", "rye", "beans", "oats"), "fuel": ("firewood", "timber", "charcoal"),
              "fresh food": ("fish", "meat", "milk", "greens", "berries", "mushrooms", "watercress"),
              "keeping food": ("smoked fish", "smoked meat", "salt fish", "salt meat", "dried fish", "dried meat", "hard-cured fish",
                               "hard-cured meat"),
              "fodder": ("hay", "straw")}
PEOPLE_SETS = ("everyone", "adults", "children", "elders", "the head", "whoever has time")
GOOD_SYNONYMS = {"fresh fish": "fish", "fresh meat": "meat", "eggs": "egg", "hens": "hen", "root": "roots", "salted fish": "salt fish",
                 "salted meat": "salt meat", "dry fish": "dried fish", "dry meat": "dried meat", "eels": "fish", "eel": "fish",
                 "dried food": "keeping food", "salted food": "keeping food", "smoked food": "keeping food", "wood": "firewood"}
SEEN_NAMES = {"the run": "run", "run": "run", "the eel run": "run", "the eels": "run", "frost": "frost", "the frost": "frost",
              "rats": "rats", "the rats": "rats", "the river rising": "river rising", "river rising": "river rising", "spate": "river rising"}
PROCESS_STATES = ("done", "in process", "fire out")
NEEDS = {"set": ("name",), "keep": ("goods",), "first": ("goods",), "share": (), "do": ("act",), "drop": ("n",)}
GOODS_FORM = "an item, a kind (fish, meat, grain, fuel, fodder, fresh food, keeping food, food, everything) or a set you named"
PEOPLE_FORM = "a person of the household, a set you named, or everyone | adults | children | elders | the head | whoever has time"
PLACE_FORM = "a building here, or a container in one (the racks in <building>, the salting tub, the hearth in <building>, the chest)"
COND_FORM = ('an object: {"goods"?, "in"?, "under": n | "over": n | "full": true | "room": true}, {"in", "state": done | in process | '
             'fire out}, {"arrives": goods}, {"season": spring | summer | autumn | winter}, {"seen": the run | frost | the river rising | '
             'rats}, {"starving": a person, a set or anyone} or {"home": a person}')
EXAMPLE = '{"rule": "first", "goods": ["fish", "keeping food"], "words": "we eat the fresh fish first"}'


# ---------------------------------------------------------------------------------------------------------------------- records
def key_of(w, whose) -> str:
    return whose if whose.startswith(("household:", "person:")) else (f"household:{whose}" if whose in w.s["institutions"] else f"person:{whose}")


def book(w, key) -> dict:
    return (w.s.get("books") or {}).get(key) or {"rules": [], "n": 1, "proposals": []}


def rules(w, key) -> list:
    """A book's rules as D2-339 reads them (old records converted, or dropped where they cannot be)."""
    return [x for x in (_current(w, key, r) for r in book(w, key)["rules"]) if x]


def p_book(w, key, value):
    """The book primitive: a book written whole (its rules, its next number, proposals to the head)."""
    w.s.setdefault("books", {})[key] = value
    return value


def _write(w, place, key, value) -> None:
    w.apply("book", place, key=key, value=value)


def household_rules(w, hh) -> list:
    return rules(w, f"household:{hh}") if hh else []


def own_rules(w, name) -> list:
    return rules(w, f"person:{name}")


# ---------------------------------------------------------------------------------------------------------------------- reading
def _goods(x) -> tuple:
    """A good, a kind of goods or everything: the items it names (a list: the union, in order)."""
    from cybertron2.engine.data import EDIBLE, ITEMS
    from cybertron2.engine.verbs import item_of
    if x is None:
        return ()
    if isinstance(x, (list, tuple)):
        out = []
        for y in x:
            out += [g for g in _goods(y) if g not in out]
        return tuple(out)
    t = str(x).strip().lower()
    t = GOOD_SYNONYMS.get(t, t)
    if t in ("everything", "all", "anything"):
        return ("*",)
    if t in ("food",):
        return tuple(sorted(EDIBLE))
    if t in ("dry goods",):
        from cybertron2.engine.stores import DRY
        return DRY
    if t in KIND_GOODS:
        return KIND_GOODS[t]
    for k, v in KIND_GOODS.items():
        if t.rstrip("s") == k.rstrip("s"):
            return v
    try:
        it = item_of(t)
    except Exception:                                                         # noqa: BLE001  (not a good)
        it = None
    return (it,) if it in ITEMS else ()


def names(rule) -> tuple:
    return _goods(rule.get("goods"))


def _num(x, default=None):
    if x is None:
        return default
    if isinstance(x, (int, float)):
        return float(x)
    m = re.search(r"(\d+(?:\.\d+)?)", str(x))
    return float(m.group(1)) if m else default


def state_of(x) -> dict | None:
    """A `when` or `unless` read as a state (u6 §3): {"state", "n"?, "set"?, "what"?}. Words never read the engine's hidden state: "when
    the eels run" reads as "seen: run"."""
    if x is None or x == "":
        return None
    if isinstance(x, dict):
        return dict(x)
    t = str(x).strip().lower()
    st = _state_of(t)
    if st and any(k in t for k in ("rack", "tub", "smoke", "bins", "store", "house", "hut", "granary", "chest", "cellar", "loft", "shed")):
        st["of"] = t                                                          # the container or store the state is of
    return st


def _state_of(t) -> dict | None:
    for s in SEASONS:
        if re.search(rf"\b{s}\b", t):
            return {"state": "season", "what": s}
    if "starv" in t:
        return {"state": "starving"}
    if any(k in t for k in ("fire died", "fire is out", "fire out", "fire went out")):
        return {"state": "fire out"}
    m = re.search(r"(\d+(?:\.\d+)?)\s+or more|\bat least\s+(\d+(?:\.\d+)?)", t)
    if m:                                                                    # "8 or more", "at least 6" (W-102)
        return {"state": "over", "n": float(m.group(1) or m.group(2)) - 1e-6}
    m = re.search(r"(\d+(?:\.\d+)?)\s+or (less|fewer)", t)
    if m:
        return {"state": "under", "n": float(m.group(1)) + 1e-6}
    if re.search(r"\b(under|below|less than|fewer than)\b", t):
        return {"state": "under", "n": _num(t, 0.0)}
    if re.search(r"\b(over|above|more than)\b", t) and _num(t) is not None:
        return {"state": "over", "n": _num(t, 0.0)}
    if "full" in t:
        return {"state": "full"}
    if "room" in t or "free up" in t or "empty" in t:
        return {"state": "room"}
    if any(k in t for k in ("done", "smoked", "cured", "dry", "dried", "retted", "finished", "ready")):
        return {"state": "done"}
    if any(k in t for k in ("smoking", "in process", "hangs", "hanging", "curing", "anything is", "while", "on the rack")):
        return {"state": "in process"}
    if any(k in t for k in ("arrive", "comes in", "come in", "comes home", "come home", "brought")):
        return {"state": "arrives"}
    if "away" in t:
        return {"state": "away", "what": t}
    if "home" in t:
        return {"state": "home", "what": t}
    for k, words in SEEN.items():
        if any(x_ in t for x_ in words) or k in t:
            return {"state": "seen", "set": k}
    if "seen" in t or "see" in t:
        return {"state": "seen", "set": "run"}
    return {"state": "words", "what": t}


def state_words(st) -> str:
    if not st:
        return ""
    k = st["state"]
    if st.get("of") and st.get("text") and k != "words":                      # a state of a named container: their own words
        return re.sub(r"^(when|while|if|unless)\s+", "", str(st["text"]).strip())
    return _state_bare(st)


def _state_bare(st) -> str:
    k = st["state"]
    return {"done": "a lot is done", "in process": "anything is smoking", "room": "they have room", "full": "they are full",
            "under": f"it holds under {st.get('n', 0):g}", "over": f"it holds over {st.get('n', 0):g}", "arrives": "it comes in",
            "fire out": "the fire died last night", "seen": f"one of you has seen {'the run' if st.get('set') == 'run' else st.get('set')}",
            "season": f"in {st.get('what')}", "starving": "someone is starving", "home": "at home", "away": "away",
            "words": f"({st.get('what')}: not a state the household can see; it never fires)"}.get(k, k)


# ---------------------------------------------------------------------------------------------------------------------- targets
def _home(w, hh, node) -> str | None:
    bs = [b for b in sorted(w.s["buildings"]) if w.s["buildings"][b]["node"] == node and _holds(w, hh, b)]
    beds = [b for b in bs if (w.s["buildings"][b].get("fittings") or {}).get("beds")]
    return (beds or bs or [None])[0]


def _holds(w, hh, bid) -> bool:
    return bool(hh) and any(c["claimant"] == hh and "withdrawal" in c["rights"] for c in w.claims_on(("building", bid)))


def _building(w, node, words) -> str | None:
    t = str(words or "").strip().lower()
    if not t:
        return None
    best = None
    for bid, b in sorted(w.s["buildings"].items()):
        if b["node"] != node:
            continue
        nm = b["name"].lower()
        for v in (nm, nm.removeprefix("the ")):
            if v and v in t and (best is None or len(v) > best[0]):
                best = (len(v), bid)
    return best[1] if best else None


def target(w, hh, node, words, goods=()) -> dict:
    """A rule's `to`/`in`/`from` read as a place (u6 §2): {"bid", "kind": store | racks | tub | hearth | a container kind | a space,
    "proc"?}. A smokehouse named alone is its racks; "the salting tub" or "salt" is salting at the house named, or at home."""
    from cybertron2.engine import stores as SR
    t = str(words or "").strip().lower()
    bid = _building(w, node, t)
    b = w.s["buildings"].get(bid) if bid else None
    smoke = [x for x in sorted(w.s["buildings"]) if w.s["buildings"][x]["node"] == node and _holds(w, hh, x)
             and (w.s["buildings"][x].get("fittings") or {}).get("smoke racks")]
    salted = any(g in ("salt fish", "salt meat") for g in goods)
    if any(k in t for k in ("tub", "brine", "salting", "barrel")) or t in ("salt", "salt them", "salt it"):
        return {"bid": bid or _home(w, hh, node), "kind": "tub", "proc": "salting"}
    if "hard cure" in t:
        return {"bid": bid or (smoke[0] if smoke else None), "kind": "racks", "proc": "hard cure"}
    if "hearth" in t or "drying rack" in t:
        return {"bid": bid or _home(w, hh, node), "kind": "hearth", "proc": "hearth rack"}
    if ("rack" in t or "smoke" in t or (b is not None and (b.get("fittings") or {}).get("smoke racks"))) and "store" not in t:
        return {"bid": bid if b is not None and (b.get("fittings") or {}).get("smoke racks") else (smoke[0] if smoke else None),
                "kind": "racks", "proc": "hard cure" if salted else "keeping smoke"}
    if t in ("hands", "my hands", "me"):
        return {"bid": None, "kind": "hands"}
    for k in list(SR.CONTAINERS) + list(SR.SPACES):
        if k in t or (k.endswith("s") is False and f"{k}s" in t):
            return {"bid": bid or _home(w, hh, node), "kind": k}
    return {"bid": bid or (_home(w, hh, node) if t in ("", "home", "the house", "store", "the store", "house") else None), "kind": "store"}


def _tech(proc, item) -> str | None:
    return {("keeping smoke", "fish"): "smoke fish", ("keeping smoke", "meat"): "smoke meat", ("hard cure", "salt fish"): "hard cure fish",
            ("hard cure", "salt meat"): "hard cure meat", ("hearth rack", "fish"): "dry fish", ("hearth rack", "meat"): "dry meat",
            ("salting", "fish"): "salt fish", ("salting", "meat"): "salt meat"}.get((proc, item))


# ---------------------------------------------------------------------------------------------------------------------- the act

# ---------------------------------------------------------------------------------------------------------------------- sets (D2-338)
def sets_of(w, name) -> dict:
    """The named sets one may use: the household's, then one's own over them (D2-338)."""
    hh = w.household_of(name) if name in w.s["people"] else None
    out = {}
    for r in household_rules(w, hh) + own_rules(w, name):
        if r.get("rule") == "set" and r.get("name"):
            out[str(r["name"]).strip().lower()] = r
    return out


def goods_of(w, name, x, depth=0) -> tuple:
    """The items a "goods" value names, sets expanded (a set may hold sets), in order."""
    if x is None or depth > 6:
        return ()
    if isinstance(x, (list, tuple)):
        out = []
        for y in x:
            out += [g for g in goods_of(w, name, y, depth) if g not in out]
        return tuple(out)
    st = sets_of(w, name).get(str(x).strip().lower())
    if st is not None:
        return goods_of(w, name, st.get("goods") or [], depth + 1)
    return _goods(x)


def people_of(w, name, x, depth=0) -> list | None:
    """The people a "people", "who" or "order" value names: the household's members; None for "whoever has time" (whoever has units
    left, chosen when the rule runs)."""
    hh = w.household_of(name) if name in w.s["people"] else None
    members = [m for m in (w.members(hh) if hh else [name]) if w.s["people"].get(m, {}).get("alive", True)]
    if x is None or depth > 6:
        return []
    if isinstance(x, (list, tuple)):
        out = []
        for y in x:
            got = people_of(w, name, y, depth)
            out += [m for m in (got or []) if m not in out]
        return out
    t = str(x).strip().lower()
    stage = lambda m: w.s["people"][m]["stage"]
    if t in ("whoever has time", "anyone", "whoever"):
        return None
    if t in ("everyone", "all", "the household", "us", "everybody"):
        return list(members)
    if t in ("adults", "the adults", "grown", "the grown"):
        return [m for m in members if stage(m) == "adult"]
    if t in ("children", "the children", "the young", "young"):
        return [m for m in members if stage(m) in ("infant", "child", "youth")]
    if t in ("elders", "the elders", "the old"):
        return [m for m in members if stage(m) == "elder"]
    if t in ("the head", "head"):
        return [w.head(hh)] if hh and w.head(hh) else []
    if t in ("me", "myself", "i"):
        return [name]
    st = sets_of(w, name).get(t)
    if st is not None:
        return people_of(w, name, st.get("people") or [], depth + 1) or []
    who = next((m for m in w.living() if m.lower() == t), None)
    return [who] if who else []


def _one(x) -> bool:
    """A value that names one person or one good (before a set, in precedence)."""
    return isinstance(x, str) and str(x).strip().lower() not in PEOPLE_SETS and not isinstance(x, (list, tuple))


# ---------------------------------------------------------------------------------------------------------------------- conditions
def _wrote(a) -> str:
    return json.dumps({k: v for k, v in dict(a).items() if not str(k).startswith("_")}, ensure_ascii=False, default=str)[:300]


def _place_ok(here, v) -> bool:
    w = here._w
    if str(v).strip().lower() in ("hands", "my hands"):
        return True
    tg = target(w, here.household(), here.node, v, ())
    return tg["bid"] is not None or _building(w, here.node, v) is not None


def _own_place(here, v) -> None:
    """A rule's place is its household's (or one's own house here): else refused, naming whose it is (a rule keeps what is the
    household's; store access between households is out of scope, D2-339)."""
    from cybertron2.engine.world import Refused
    w = here._w
    if str(v).strip().lower() in ("hands", "my hands"):
        return
    hh = here.household()
    tg = target(w, hh, here.node, v, ())
    bid = tg.get("bid") or _building(w, here.node, v)
    if bid is None:
        if tg.get("kind") in ("racks", "tub", "hearth"):
            raise Refused("your household has no " + {"racks": "smoke racks", "tub": "house to salt in", "hearth": "hearth"}[tg["kind"]] + " here")
        raise Refused(f"could not read the place {v!r} ({PLACE_FORM})")
    if not _holds(w, hh, bid) and bid not in here.homes_here():
        raise Refused(f"{w.s['buildings'][bid]['name']} is not your household's")


def cond(here, x, field):
    """A `when` or `unless` as one of D2-339's condition objects, checked; None for none. Raises Refused naming the field's form."""
    from cybertron2.engine.world import Refused
    if x in (None, "", {}):
        return None
    bad = lambda why: Refused(f"could not read \"{field}\": {_wrote(x) if isinstance(x, dict) else repr(x)} ({why}; it is {COND_FORM})")
    if not isinstance(x, dict):
        raise bad("not an object")
    c = {str(k).strip().lower(): v for k, v in x.items()}
    w = here._w
    if "state" in c:
        if str(c["state"]).strip().lower() not in PROCESS_STATES:
            raise bad("a process's state is done, in process or fire out")
        if not c.get("in") or not _place_ok(here, c["in"]):
            raise bad("a process names its container or building in \"in\"")
        return {"in": c["in"], "state": str(c["state"]).strip().lower()}
    amt = [k for k in ("under", "over", "full", "room") if k in c]
    if amt:
        out = {}
        if c.get("goods") not in (None, "", []):
            if not goods_of(w, here.name, c["goods"]):
                raise bad("its goods name no good")
            out["goods"] = c["goods"]
        if c.get("in") not in (None, ""):
            if not _place_ok(here, c["in"]):
                raise bad("its \"in\" names no building or container here")
            out["in"] = c["in"]
        k = amt[0]
        if k in ("under", "over"):
            if _num(c[k]) is None:
                raise bad(f"\"{k}\" is a number")
            if "goods" not in out:
                raise bad(f"an amount \"{k}\" names its goods")
            out[k] = float(_num(c[k]))
        else:
            out[k] = True
        return out
    if "arrives" in c:
        if not goods_of(w, here.name, c["arrives"]):
            raise bad("\"arrives\" names goods")
        return {"arrives": c["arrives"]}
    if "season" in c:
        s = str(c["season"]).strip().lower()
        if s not in SEASONS:
            raise bad("a season is spring, summer, autumn or winter")
        return {"season": s}
    if "seen" in c:
        s = SEEN_NAMES.get(str(c["seen"]).strip().lower())
        if s is None:
            raise bad("what is seen is the run, frost, the river rising or rats")
        return {"seen": s}
    if "starving" in c:
        v = c["starving"]
        if str(v).strip().lower() != "anyone" and not people_of(w, here.name, v):
            raise bad("\"starving\" names a person, a set or anyone")
        return {"starving": v}
    if "home" in c:
        if not people_of(w, here.name, c["home"]):
            raise bad("\"home\" names a person")
        return {"home": c["home"]}
    raise bad("no condition it knows")


def cond_holds(w, hh, node, c, name, who=None) -> bool:
    """Whether a condition object holds now (u6 §3), read only from what the household knows: its own containers and stores, its
    members' hunger and whereabouts, the calendar, what its members noticed. Lasting states hold until they end (the latch)."""
    from cybertron2.engine import process as PROC
    if not c:
        return False
    if "season" in c:
        return w.calendar()["season"] == c["season"]
    if "seen" in c:
        return seen(w, hh, c["seen"])
    if "starving" in c:
        v = c["starving"]
        ms = [who] if who else ((w.members(hh) if hh else [name]) if str(v).strip().lower() == "anyone" else (people_of(w, name, v) or []))
        return any(m in w.s["people"] and w.s["people"][m]["alive"] and int(w.s["people"][m].get("hunger", 0)) <= -2 for m in ms)
    if "home" in c:
        ms = people_of(w, name, c["home"]) or []
        return bool(ms) and all(w.at(m) == node for m in ms)
    if "arrives" in c:
        return any(_store_have(w, hh, node, i) > 1e-6 for i in goods_of(w, name, c["arrives"]) if i != "*")
    gs = [i for i in goods_of(w, name, c.get("goods")) if i != "*"]
    tg = target(w, hh, node, c.get("in"), tuple(gs)) if c.get("in") else {"bid": None, "kind": "store"}
    bid = tg.get("bid")
    if "state" in c:
        if bid is None:
            return False
        s = PROC.states(w, hh, bid)
        return {"done": s["done"] > 1e-6, "in process": s["in process"] > 1e-6, "fire out": bool(s["fire out"])}[c["state"]]
    if "under" in c or "over" in c:
        if bid is not None:
            q = sum(float(w.goods(w.s["buildings"][bid]["stock"]).get(i, 0.0)) for i in gs)
        else:
            q = sum(_store_have(w, hh, node, i) for i in gs)
        return q < float(c["under"]) if "under" in c else q > float(c["over"])
    if "full" in c or "room" in c:
        if bid is None:
            return False
        if tg.get("kind") in ("racks", "tub", "hearth") or PROC.states(w, hh, bid).get("room", 0) or PROC.states(w, hh, bid).get("full"):
            s = PROC.states(w, hh, bid)
            return bool(s["full"]) if "full" in c else s["room"] > 1e-6
        from cybertron2.engine import buildings as BL
        b = w.s["buildings"][bid]
        room = BL.room_for(b, w.goods(b["stock"]), gs[0] if gs else "firewood")
        return room <= 1e-6 if "full" in c else room > 1e-6
    return False


def cond_words(c) -> str:
    if not c:
        return ""
    if "state" in c:
        return {"done": f"a lot is done in {c['in']}", "in process": f"anything is smoking in {c['in']}",
                "fire out": f"the fire in {c['in']} died last night"}[c["state"]]
    g = _and(c["goods"]) if isinstance(c.get("goods"), (list, tuple)) else c.get("goods")
    where = f" in {c['in']}" if c.get("in") else ""
    if "under" in c:
        return f"{g}{where} is under {c['under']:g}"
    if "over" in c:
        return f"{g}{where} is over {c['over']:g}"
    if "full" in c:
        return f"{c.get('in') or g} is full"
    if "room" in c:
        return f"{c.get('in') or g} has room"
    if "arrives" in c:
        a = c["arrives"]
        return f"{_and(a) if isinstance(a, (list, tuple)) else a} comes in"
    if "season" in c:
        return f"in {c['season']}"
    if "seen" in c:
        return f"one of you has seen {'the run' if c['seen'] == 'run' else c['seen']}"
    if "starving" in c:
        return "someone is starving" if str(c["starving"]).lower() == "anyone" else f"{c['starving']} is starving"
    if "home" in c:
        return f"{c['home']} is home"
    return ""


# ---------------------------------------------------------------------------------------------------------------------- reading a rule
def _goods_field(here, r, f, a, many=False):
    from cybertron2.engine.world import Refused
    v = r.get(f)
    xs = v if isinstance(v, (list, tuple)) else [v]
    out = []
    for y in xs:
        t = GOOD_SYNONYMS.get(str(y).strip().lower(), str(y).strip().lower()) if isinstance(y, str) else y
        if not isinstance(t, str) or not goods_of(here._w, here.name, t):
            raise Refused(f"could not read \"{f}\": {y!r} ({GOODS_FORM}); you wrote {_wrote(a)}")
        out.append(t)
    return out if (many or len(out) > 1) else out[0]


def _people_field(here, r, f, a, many=False):
    from cybertron2.engine.world import Refused
    v = r.get(f)
    xs = v if isinstance(v, (list, tuple)) else [v]
    for y in xs:
        builtin = str(y).strip().lower() in PEOPLE_SETS + ("me", "anyone", "the children", "the adults", "the elders", "all")
        if not isinstance(y, str) or (people_of(here._w, here.name, y) == [] and not builtin):
            raise Refused(f"could not read \"{f}\": {y!r} ({PEOPLE_FORM}); you wrote {_wrote(a)}")
    return list(xs) if (many or len(xs) > 1) else xs[0]


def _act_field(here, act, a):
    """A `do` rule's act: an ordinary act, read as the actions are (the shapes when on); never travel or a free act."""
    from cybertron2.engine import shapes as SH, verbs as V
    from cybertron2.engine.world import Refused
    if not isinstance(act, dict) or not act.get("do"):
        raise Refused(f"could not read \"act\": an act is {{\"do\": a craft or an act, ...}} as in \"actions\"; you wrote {_wrote(a)}")
    x = act
    if SH.on(here):
        try:
            x = SH.normalize(here, here.mind(), act)
        except Refused as e:
            raise Refused(f"could not read \"act\": {e}; you wrote {_wrote(a)}")
    v = str(x.get("do") or "").strip().lower()
    if v not in V.VERB:
        raise Refused(f"could not read \"act\": {act.get('do')!r} is no act; you wrote {_wrote(a)}")
    if v in FREE_OR_TRAVEL:
        raise Refused("a rule's act is work done with units left over: travel and free acts cannot be one")
    return {k: val for k, val in x.items() if not str(k).startswith("_")}


def read(here, a) -> dict:
    """A rule as the book's record (D2-337, D2-339): its kind in "rule", each field read from its own field, a value mapped to its
    canonical name; an old kind converted. Raises Refused naming the field, its form and what was written."""
    from cybertron2.engine.world import Refused
    a = {str(k).strip(): v for k, v in dict(a or {}).items() if str(k).strip() != "do"}
    kind = str(a.get("rule") or "").strip().lower()
    if legacy({**a, "rule": kind}):
        conv = convert(here._w, here.household(), here.node, {**a, "rule": kind}, name=here.name)
        if conv is None:
            raise Refused(f"could not read this rule as one of {' | '.join(KINDS)}; you wrote {_wrote(a)}. As {EXAMPLE}")
        a, kind = conv, conv["rule"]
    if kind not in KINDS:
        raise Refused(f"a rule names its kind in \"rule\": {' | '.join(KINDS)}; you wrote {_wrote(a)}. As {EXAMPLE}")
    if "goods" not in a and a.get("item"):
        a["goods"] = a.pop("item")
    for f in NEEDS[kind]:
        if a.get(f) in (None, "", [], {}) and not (kind == "do" and a.get("acts")):
            form = {"goods": GOODS_FORM, "name": "the set's name", "act": 'an act, as in "actions"', "n": "the rule's number"}[f]
            raise Refused(f"'{kind}' needs \"{f}\" ({form}); you wrote {_wrote(a)}")
    r = {"rule": kind}
    for f in ("for", "words", "n", "standing"):
        if a.get(f) not in (None, ""):
            r[f] = a[f]
    if r.get("for") not in (None, "household", "me"):
        raise Refused(f"could not read \"for\": {r['for']!r} (household or me)")
    if kind == "set":
        nm = str(a["name"]).strip()
        if nm.lower() in PEOPLE_SETS or nm.lower() in KIND_GOODS:
            raise Refused(f"could not read \"name\": {nm!r} is a set the engine has already")
        r["name"] = nm
        if not any(a.get(f) for f in ("people", "goods", "places")):
            raise Refused(f"'set' needs \"people\", \"goods\" or \"places\" (lists); you wrote {_wrote(a)}")
        if a.get("people"):
            r["people"] = _people_field(here, a, "people", a, many=True)
        if a.get("goods"):
            r["goods"] = _goods_field(here, a, "goods", a, many=True)
        if a.get("places"):
            ps = a["places"] if isinstance(a["places"], (list, tuple)) else [a["places"]]
            for p in ps:
                if here.building(p) is None and here.parcel(p) is None:
                    raise Refused(f"could not read \"places\": {p!r} (a building or a place here); you wrote {_wrote(a)}")
            r["places"] = list(ps)
    elif kind == "keep":
        r["goods"] = _goods_field(here, a, "goods", a)
        if a.get("in") not in (None, ""):
            if not _place_ok(here, a["in"]):
                raise Refused(f"could not read \"in\": {a['in']!r} ({PLACE_FORM}); you wrote {_wrote(a)}")
            _own_place(here, a["in"])
            r["in"] = a["in"]
        if a.get("at least") not in (None, ""):
            v = a["at least"]
            if str(v).strip().lower() != "all" and _num(v) is None:
                raise Refused(f"could not read \"at least\": {v!r} (a number, or all)")
            r["at least"] = "all" if str(v).strip().lower() == "all" else float(_num(v))
        if "in" not in r and "at least" not in r:
            raise Refused(f"'keep' needs \"in\" ({PLACE_FORM}) or \"at least\" (a number, or all); you wrote {_wrote(a)}")
    elif kind == "first":
        r["goods"] = _goods_field(here, a, "goods", a, many=True)
    elif kind == "share":
        if not any(a.get(f) not in (None, "", []) for f in ("order", "who", "qty", "goods")):
            raise Refused(f"'share' needs \"order\", \"who\", \"qty\" or \"goods\"; you wrote {_wrote(a)}")
        if a.get("order"):
            r["order"] = _people_field(here, a, "order", a, many=True)
        if a.get("who"):
            r["who"] = _people_field(here, a, "who", a)
        if a.get("qty") not in (None, ""):
            q = _share_qty(a["qty"])
            if q is None:
                raise Refused(f"could not read \"qty\": {a['qty']!r} (full, half, or a fraction such as 0.75)")
            r["qty"] = q
        if a.get("goods"):
            r["goods"] = _goods_field(here, a, "goods", a)
            if not r.get("who"):
                raise Refused(f"'share' with \"goods\" needs \"who\" gets them ({PEOPLE_FORM}); you wrote {_wrote(a)}")
    elif kind == "do":
        if a.get("acts"):
            r["acts"] = [_act_field(here, x, a) for x in (a["acts"] if isinstance(a["acts"], list) else [a["acts"]])][:3]
        else:
            r["act"] = _act_field(here, a["act"], a)
        if a.get("who") not in (None, ""):
            r["who"] = _people_field(here, a, "who", a)
    elif kind == "drop":
        if _num(a.get("n")) is None:
            raise Refused(f"could not read \"n\": {a.get('n')!r} (the rule's number)")
    for f in ("when", "unless"):
        if a.get(f) not in (None, "", {}):
            if kind in ("set", "drop"):
                raise Refused(f"'{kind}' takes no \"{f}\"")
            r[f] = cond(here, a[f], f)
            if r[f].get("in"):
                _own_place(here, r[f]["in"])
    if kind == "do":                                                          # the places the act names: the household's
        for x in (r.get("acts") or [r.get("act")]):
            for f in ("from", "to") if x.get("do") == "move" else ():
                if x.get(f) and _building(here._w, here.node, x[f]) is not None:
                    _own_place(here, x[f])
    return r


def _share_qty(x):
    t = str(x).strip().lower()
    if t in ("full", "whole", "all", "1"):
        return "full"
    if t in ("half", "a half"):
        return 0.5
    words = {"a quarter": 0.25, "three quarters": 0.75, "a third": 1 / 3, "two thirds": 2 / 3}
    if t in words:
        return round(words[t], 3)
    q = _num(x)
    if q is None or not (0 < q <= 1.0):
        return None
    return 1.0 if q == 1.0 else q


# ---------------------------------------------------------------------------------------------------------------------- the old kinds
def _conv_state(x, r, place):
    """A condition of an old rule (a sentence or u6 §3's state dict) as a D2-339 object, or None where it named no state."""
    if x in (None, ""):
        return None
    st = dict(x) if isinstance(x, dict) else state_of(x)
    if not st:
        return None
    k = st.get("state")
    where = place
    if st.get("of"):
        where = st["of"]
    gs = r.get("goods")
    if k in ("done", "in process", "fire out"):
        return {"in": where, "state": k} if where else None
    if k in ("room", "full"):
        return {"in": where, k: True} if where else None
    if k in ("under", "over"):
        return {"goods": gs, **({"in": where} if where else {}), k: float(st.get("n") or 0)} if gs else None
    if k == "arrives":
        return {"arrives": gs} if gs else None
    if k == "season":
        return {"season": st.get("what")}
    if k == "starving":
        return {"starving": "anyone"}
    if k == "seen":
        return {"seen": st.get("set") or "run"}
    return None


def convert(w, hh, node, r, name=None) -> dict | None:
    """An old rule (u6 §2: go, keep, hold back, first, eat, move, tend, chore) in D2-339's kinds, or None where it cannot be: a go into
    a container or a tend or a move is a `do` of the act it stood for; a go into a store, a keep and a hold back are a `keep`; an eat
    is a `share`; a chore a `do`; first with "before" one ordered list."""
    k = str(r.get("rule") or "").strip().lower()
    out = {f: r[f] for f in ("n", "for", "words", "set_day", "set_by", "standing") if r.get(f) not in (None, "")}
    gs = r.get("goods")
    first_good = (list(_goods(gs)) or [None])[0] if gs else None
    if k in ("set", "share", "do", "drop"):
        return {**out, **{f: v for f, v in r.items() if f not in out}}
    if k == "go":
        tg = target(w, hh, node, r.get("to"), _goods(gs))
        if tg["kind"] in ("racks", "tub", "hearth") and tg.get("bid"):
            tech = _tech(tg["proc"], first_good) if first_good else None
            if tech is None:
                return None
            bn = w.s["buildings"][tg["bid"]]["name"]
            return {**out, "rule": "do", "who": r.get("by") or "whoever has time", "act": {"do": "make", "what": tech, "at": bn},
                    **_cw(r, bn, default={"arrives": gs})}
        if tg.get("bid"):
            return {**out, "rule": "keep", "goods": gs, "in": w.s["buildings"][tg["bid"]]["name"]}
        return None
    if k == "tend":
        at = r.get("at") or r.get("in") or r.get("to")
        tg = target(w, hh, node, at or "the racks", ())
        if not tg.get("bid"):
            return None
        bn = w.s["buildings"][tg["bid"]]["name"]
        return {**out, "rule": "do", "who": r.get("by") or "whoever has time", "act": {"do": "tend", "at": bn},
                **_cw(r, bn, default={"in": bn, "state": "in process"})}
    if k == "move":
        src = target(w, hh, node, r.get("from"), _goods(gs))
        dst = target(w, hh, node, r.get("to"), _goods(gs))
        if not first_good or not (src.get("bid") or r.get("from")) or not (dst.get("bid") or dst.get("kind") == "hands"):
            return None
        sn = w.s["buildings"][src["bid"]]["name"] if src.get("bid") else r.get("from")
        dn = w.s["buildings"][dst["bid"]]["name"] if dst.get("bid") else "hands"
        act = {"do": "move", "item": first_good, "from": sn, "to": dn, **({"qty": r["qty"]} if r.get("qty") not in (None, "") else {})}
        racks = src.get("kind") in ("racks", "hearth")
        return {**out, "rule": "do", "who": r.get("by") or "whoever has time", "act": act,
                **_cw(r, sn, default={"in": sn, "state": "done"} if racks else None)}
    if k in ("keep", "hold back"):
        q = r.get("qty")
        rec = {**out, "rule": "keep", "goods": gs or "everything"}
        if r.get("in") or (k == "keep" and r.get("to")):
            rec["in"] = r.get("in") or r.get("to")
        if k == "hold back":
            rec["at least"] = "all" if q in (None, "", "all") else (float(_num(q)) if _num(q) is not None else "all")
        return {**rec, **_cw(r, rec.get("in"))}
    if k == "first":
        order = list(_goods_list(gs)) + [g for g in _goods_list(r.get("before")) if g not in _goods_list(gs)]
        return {**out, "rule": "first", "goods": order, **_cw(r, None)} if order else None
    if k == "eat":
        q = _share_qty(r.get("qty") or "full") or "full"
        return {**out, "rule": "share", "qty": q, **({"order": [r["who"]]} if r.get("who") else {}), **_cw(r, None)}
    if k == "chore":
        acts = [x for x in (r.get("acts") or []) if isinstance(x, dict)]
        if not acts:
            return None
        return {**out, "rule": "do", "who": r.get("who") or ("me" if r.get("for") == "me" else "whoever has time"), "acts": acts,
                **_cw(r, None)}
    return None


def _goods_list(x) -> list:
    if x in (None, "", []):
        return []
    return [str(y) for y in x] if isinstance(x, (list, tuple)) else [y.strip() for y in re.split(r",|\band\b", str(x)) if y.strip()]


def _cw(r, place, default=None) -> dict:
    out = {}
    wn = _conv_state(r.get("when"), r, place)
    un = _conv_state(r.get("unless"), r, place)
    if wn or default:
        out["when"] = wn or default
    if un:
        out["unless"] = un
    return out


def _node_of(w, key) -> str | None:
    if key.startswith("person:"):
        return w.at(key[len("person:"):])
    hh = key[len("household:"):]
    h = w.head(hh) if hh in w.s["institutions"] else None
    if h and w.at(h):
        return w.at(h)
    return next((b["node"] for bid, b in sorted(w.s["buildings"].items()) if _holds(w, hh, bid)), None)


def legacy(r) -> bool:
    """A record written before D2-339 (an old kind, "before", an old keep's "to" or "qty", a condition as words or u6 §3's state)."""
    if r.get("rule") in OLD_KINDS or "before" in r:
        return True
    if r.get("rule") == "keep" and ("to" in r or "qty" in r) and "at least" not in r:
        return True
    for f in ("when", "unless"):
        c = r.get(f)
        if isinstance(c, str):
            return True
        if isinstance(c, dict) and ("text" in c or ("state" in c and (c["state"] not in PROCESS_STATES or "in" not in c))):
            return True
    return False


def _current(w, key, r) -> dict | None:
    """A record as D2-339 reads it: a new one as it is; an old one converted (or None: dropped)."""
    if not legacy(r) and r.get("rule") in KINDS:
        return r
    hh = key[len("household:"):] if key.startswith("household:") else None
    name = key[len("person:"):] if key.startswith("person:") else (w.head(hh) if hh in w.s["institutions"] else None)
    return convert(w, hh or (w.household_of(name) if name in w.s["people"] else None), _node_of(w, key), r, name=name)


# ---------------------------------------------------------------------------------------------------------------------- the act
def apply_rules(here, xs) -> list:
    """The reply's "rules" field (D2-339): each record set, changed or dropped, free; one result line each."""
    from cybertron2.engine.world import Refused
    out = []
    for x in [x for x in (xs or []) if isinstance(x, dict)][:8]:
        try:
            out.append(act(here, x))
        except Refused as e:
            out.append(f"Refused: rule: {e}")
    return out


def act(here, a) -> str:
    """A rule set, changed (with `n`) or dropped in one's own book or the household's (the head's; a member's is a proposal to the
    head): free, at any time or in the evening (D2-319). Returns the engine's reading beside their words, or why not."""
    from cybertron2.engine.world import Refused
    w = here._w
    r = read(here, a)
    kind = r["rule"]
    hh = here.household()
    whose = str(r.pop("for", "") or "").strip().lower()
    if whose not in ("household", "me"):
        whose = "household" if hh and w.head(hh) == here.name and str(r.get("who") or "").lower() != "me" else "me"
    if kind == "do" and whose == "me" and r.get("who") not in (None, "me", here.name):
        whose = "household"
    if whose == "household" and not hh:
        raise Refused("you belong to no household: a rule of yours goes in your own book (\"for\": \"me\")")
    key = f"household:{hh}" if whose == "household" else f"person:{here.name}"
    bk = book(w, key)
    rs = rules(w, key)
    if kind == "drop":
        n = int(_num(r.get("n"), 0) or 0)
        hit = [x for x in rs if int(x["n"]) == n]
        if not hit:
            raise Refused(f"there is no rule {n} in {'the household' if whose == 'household' else 'your'} book")
        if whose == "household" and w.head(hh) != here.name:
            return _propose(here, key, bk, {**hit[0], "drop": True}, f"drop rule {n}")
        _write(w, here.node, key, {**bk, "rules": [x for x in bk["rules"] if int(x["n"]) != n]})
        return f"Rule {n} ({'the household' if whose == 'household' else 'yours'}) dropped: {reading(w, hit[0])}."
    r["for"] = whose
    if r.get("n") not in (None, ""):
        n = int(_num(r["n"], 0) or 0)
        if not any(int(x["n"]) == n for x in bk["rules"]):
            raise Refused(f"there is no rule {n} to change")
        r["n"] = n
    else:
        r["n"] = int(bk.get("n", 1))
    r["set_day"], r["set_by"] = here.day, here.name
    if whose == "household" and w.head(hh) != here.name:
        return _propose(here, key, bk, r, "")
    out = [x for x in bk["rules"] if int(x["n"]) != int(r["n"])] + [r]
    _write(w, here.node, key, {**bk, "rules": sorted(out, key=lambda x: int(x["n"])), "n": max(int(bk.get("n", 1)), int(r["n"]) + 1)})
    return (f"Rule {r['n']} ({'the household' if whose == 'household' else 'yours'}): {reading(w, r)}"
            + (f" (your words: \"{r['words']}\")" if r.get("words") else "") + f". {_when_fires(r)}").rstrip()


def _when_fires(r) -> str:
    if r["rule"] == "do":
        return ("It is done with units left over after the day's plans, while that holds." if r.get("when") or r.get("unless")
                else "It is your fallback: done with units your plan leaves, every day until you change it." if r.get("for") == "me"
                else "It is done with units left over after the day's plans, every day.")
    if r["rule"] == "set":
        return "Rules may name it now."
    return "It applies from now on."


def reading(w, r) -> str:
    """The engine's reading of a rule (u6 §9)."""
    k = r.get("rule")
    g = r.get("goods")
    g = _and(g) if isinstance(g, (list, tuple)) else (g or "")
    tail = (f", when {cond_words(r.get('when'))}" if r.get("when") else "") + (f", unless {cond_words(r.get('unless'))}" if r.get("unless") else "")
    if k == "set":
        parts = [f"{_and(r[f])}" for f in ("people", "goods", "places") if r.get(f)]
        return f"the set \"{r['name']}\": " + "; ".join(parts)
    if k == "keep":
        x = []
        if r.get("in"):
            x.append(f"{g} kept in {r['in']}")
        if r.get("at least") not in (None, ""):
            x.append(("all the " + g if r["at least"] == "all" else f"at least {r['at least']:g} {g}") + " not eaten, drawn or used")
        return "; ".join(x) + tail
    if k == "first":
        gs = r.get("goods") if isinstance(r.get("goods"), (list, tuple)) else [r.get("goods")]
        return "take or eat " + ", then ".join(str(x) for x in gs) + " first" + tail
    if k == "share":
        x = []
        if r.get("order"):
            x.append(f"when food is short, {_and(r['order'])} are fed first, in that order")
        if r.get("qty") not in (None, ""):
            q = r["qty"]
            x.append(f"{r.get('who') or 'everyone'} eat{'s' if r.get('who') and _one(r['who']) else ''} "
                     + ("full rations" if q == "full" else "half rations" if q == 0.5 else f"{q:g} of a ration"))
        if r.get("goods"):
            x.append(f"the {g} go{'es' if not isinstance(r.get('goods'), list) else ''} to {r['who']}")
        return "; ".join(x) + tail
    if k == "do":
        acts = r.get("acts") or [r.get("act") or {}]
        who = r.get("who") or ("you" if r.get("for") == "me" else "whoever has time")
        return f"{who}: " + "; else ".join(_act_words(a) for a in acts) + (tail if tail else ", with units left over")
    return str(k)


def _and(xs) -> str:
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1] if xs else ""


def _act_words(x) -> str:
    out = " ".join(str(x[k]) for k in ("do", "qty", "what", "item") if x.get(k) not in (None, ""))
    for k, word in (("from", "from"), ("to", "to"), ("at", "at")):
        if x.get(k) not in (None, ""):
            out += f" {word} {x[k]}"
    return out


# ---------------------------------------------------------------------------------------------------------------------- the store moments
def _keep_in(w, hh, node, r, name):
    tg = target(w, hh, node, r.get("in"), tuple(goods_of(w, name, r.get("goods"))))
    return tg


def where_to(w, name, item) -> str | None:
    """Goods arriving for one's household (moment 1): the store a `keep` with "in" names (one's own first, then the household's).
    None: no rule."""
    hh = w.household_of(name)
    node = w.at(name)
    for r in _ranked(w, own_rules(w, name)) + _ranked(w, household_rules(w, hh)):
        if r["rule"] != "keep" or not r.get("in") or not _applies(w, hh, node, r, name):
            continue
        gs = goods_of(w, name, r.get("goods"))
        if item not in gs and "*" not in gs:
            continue
        tg = _keep_in(w, hh, node, r, name)
        if tg.get("bid") and tg["kind"] in ("store", "floor", "racks") and _holds(w, hh, tg["bid"]):
            return w.s["buildings"][tg["bid"]]["stock"]
    return None


def install(w) -> None:
    """Moment 1: goods coming into a household's store go where its `keep` rules put them, to another of its stores here."""
    w.hook("after", "create", lambda w_, call, out: _arrive(w_, call["kw"]["dst"], call["kw"]["item"], out))


def _arrive(w, cid, item, q) -> None:
    c = w.s["containers"].get(cid) or {}
    if c.get("kind") != "stock" or c.get("of") not in w.s["buildings"] or not q or float(q) <= 1e-9 or not w.s.get("books"):
        return
    bid = c["of"]
    node = w.s["buildings"][bid]["node"]
    for cl in w.claims_on(("building", bid)):
        hh = cl["claimant"]
        if hh not in w.s["institutions"] or "withdrawal" not in cl["rights"]:
            continue
        head = w.head(hh)
        for r in _ranked(w, household_rules(w, hh)):
            if r["rule"] != "keep" or not r.get("in"):
                continue
            gs = goods_of(w, head, r.get("goods"))
            if not (item in gs or "*" in gs) or not _applies(w, hh, node, r, head):
                continue
            tg = target(w, hh, node, r.get("in"), (item,))
            if tg["kind"] in ("store", "racks") and tg.get("bid") and tg["bid"] != bid and _holds(w, hh, tg["bid"]):   # its store
                from cybertron2.engine import buildings as BL
                dst = w.s["buildings"][tg["bid"]]
                k = min(float(q), float(w.goods(cid).get(item, 0.0)), BL.room_for(dst, w.goods(dst["stock"]), item))
                if k > 1e-6:
                    w.apply("transfer", node, src=cid, dst=dst["stock"], item=item, qty=round(k, 6))
            return
        return


def keeps(w, bid) -> list:
    """The household's `keep` rules for a building, as the sort reads them (moment 2): [(item, kind, qty)]."""
    out = []
    for c in w.claims_on(("building", bid)):
        hh = c["claimant"]
        if hh not in w.s["institutions"]:
            continue
        head = w.head(hh)
        for r in household_rules(w, hh):
            if r["rule"] != "keep" or not r.get("in"):
                continue
            tg = target(w, hh, w.s["buildings"][bid]["node"], r.get("in"), goods_of(w, head, r.get("goods")))
            if tg.get("bid") != bid:
                continue
            if tg["kind"] in ("racks", "tub", "hearth", "hands"):              # a processing container is no part of the sort
                continue
            for it in goods_of(w, head, r.get("goods")):
                if it != "*":
                    out.append((it, tg["kind"] if tg["kind"] not in ("store",) else "floor", None))
        break
    return out


def held(w, name, cid, item) -> float:
    """What of a good in a store is not eaten, drawn or used (moments 3, 4): the floor the household's `keep` rules set ("at least"),
    while their conditions hold; one's own rule for the good comes before (going against the household's, recorded)."""
    c = w.s["containers"].get(cid) or {}
    if c.get("kind") != "stock":
        return 0.0
    hh = w.household_of(name)
    if not hh or not _holds(w, hh, c["of"]):
        return 0.0
    node = w.s["buildings"][c["of"]]["node"]
    out = 0.0
    for r in household_rules(w, hh):
        if r["rule"] != "keep" or r.get("at least") in (None, ""):
            continue
        gs = goods_of(w, w.head(hh), r.get("goods"))
        if not (item in gs or "*" in gs):
            continue
        if r.get("in"):
            tg = target(w, hh, node, r.get("in"), gs)
            if tg.get("bid") not in (None, c["of"]):
                continue
        if not _applies(w, hh, node, r, name, who=name):
            continue
        if any(x["rule"] in ("first", "share") and item in goods_of(w, name, x.get("goods")) for x in own_rules(w, name)):
            _against(w, name, r, f"{name}'s own rule takes the {item} the household keeps back")
            continue
        q = r["at least"]
        have = float(w.goods(cid).get(item, 0.0))
        out += have if q == "all" else min(have, float(q))
    return out


def _applies(w, hh, node, r, name, who=None) -> bool:
    if r.get("when") and not cond_holds(w, hh, node, r["when"], name, who=who):
        return False
    if r.get("unless") and cond_holds(w, hh, node, r["unless"], name, who=who):
        return False
    return True


def _ranked(w, rs) -> list:
    """Precedence within one book (D2-339): a rule naming one person or one good before one naming a set; newer before older."""
    def k(r):
        x = r.get("who") if r["rule"] in ("do", "share") else r.get("goods")
        return (0 if _one(x) else 1, -int(r.get("n", 0)))
    return sorted(rs, key=k)


def meal(w, name) -> dict:
    """The night's meal by the book (moment 4): {"first": items in order, "ration": a share of the need, "skip": goods another's
    share keeps for them}. One's own rules before the household's (D2-339)."""
    hh = w.household_of(name)
    node = w.at(name)
    first, ration, skip, set_ration, used = [], 1.0, [], False, []
    mine_rs = _ranked(w, own_rules(w, name))
    own = {id(r) for r in mine_rs}
    rs = mine_rs + _ranked(w, household_rules(w, hh))

    def by(r, goods=(), ration=False):                                        # which rule shaped the meal, for the morning (D2-342)
        used.append({"n": r.get("n"), "own": id(r) in own, "words": str(r.get("words") or "").strip() or reading(w, r),
                     "goods": list(goods), "ration": ration})
    for r in rs:
        if not _applies(w, hh, node, r, name, who=name):
            continue
        if r["rule"] == "first":
            gs = [i for i in goods_of(w, name, r.get("goods")) if i not in first and i != "*"]
            first += gs
            by(r, gs)
        elif r["rule"] == "share":
            who = people_of(w, name, r.get("who")) if r.get("who") else None
            mine = who is None or name in (who or [])
            sets = r.get("qty") not in (None, "") and mine and not set_ration
            if sets:
                ration, set_ration = (1.0 if r["qty"] == "full" else float(r["qty"])), True
            gs = []
            if r.get("goods"):
                gs = [i for i in goods_of(w, name, r["goods"]) if i != "*"]
                if mine:
                    first = [i for i in gs if i not in first] + first
                else:
                    skip += [i for i in gs if i not in skip]
            if mine and (sets or gs):
                by(r, gs, ration=sets and ration < 1 - 1e-9)
    return {"first": first, "ration": ration, "skip": [i for i in skip if i not in first], "rules": used}


def meal_order(w, people) -> list:
    """The order the night's meal goes in (D2-339 share's "order": fed first when food is short): those a household's share rule
    orders, in that order, before the rest; otherwise as given."""
    if not w.s.get("books"):
        return list(people)
    rank = {}
    for hh in sorted({w.household_of(n) for n in people if w.household_of(n)}):
        for r in _ranked(w, household_rules(w, hh)):
            if r["rule"] == "share" and r.get("order"):
                order = people_of(w, w.head(hh), r["order"]) or []
                for i, m in enumerate(order):
                    rank.setdefault(m, i)
                break
    idx = {n: i for i, n in enumerate(people)}
    return sorted(people, key=lambda n: (0, rank[n]) if n in rank else (1, idx[n]))


def _against(w, name, r, words) -> None:
    t = w.s.get("today")
    if t is not None:
        t.setdefault("book", {}).setdefault("against", []).append({"by": name, "rule": r.get("n"), "words": words})


# ---------------------------------------------------------------------------------------------------------------------- proposals, sightings, stores
def _propose(here, key, bk, r, what) -> str:
    w = here._w
    head = w.head(here.household())
    _write(w, here.node, key, {**bk, "proposals": list(bk.get("proposals") or []) + [{**r, "by": here.name, "day": here.day}]})
    return f"Proposed to {head}, who heads the household: {what or reading(w, r)}. It stands once {head} takes it."



def seen(w, hh, which) -> bool:
    """A member noticed a sign of the set that day or the night before (u6 §3; D4-35): their held lines matched to the set's words.
    Never the engine's hidden state (a run's pulses)."""
    words = SEEN.get(which, (which,))
    for m in (w.members(hh) if hh else []):
        st = (w.s.get("mind") or {}).get(m) or {}
        t = st.get("today") or {}
        lines = [x for k in ("dawn", "concerned", "notice", "glimpse", "felt", "learned") for x in (t.get(k) or [])]
        days = st.get("days") or []
        if days and int(days[-1].get("day", -9)) >= w.d - 1:
            lines += list(days[-1].get("saw") or [])
        if any(any(x_ in str(line).lower() for x_ in words) for line in lines):
            return True
    return False


def _store_have(w, hh, node, item) -> float:
    return sum(float(w.goods(b["stock"]).get(item, 0.0)) for bid, b in sorted(w.s["buildings"].items())
               if b["node"] == node and _holds(w, hh, bid) and b.get("stock") in w.s["containers"])


def _stock_cids(w, hh, node, item, skip=None) -> list:
    return [b["stock"] for bid, b in sorted(w.s["buildings"].items()) if b["node"] == node and _holds(w, hh, bid) and bid != skip
            and float(w.goods(b["stock"]).get(item, 0.0)) > 1e-9]


# ---------------------------------------------------------------------------------------------------------------------- the spare units' day
class Day:
    """The spare-units phase's account of a day (u6 §5): each one's spare whole units, the chores' real fractions summed and charged
    as the walk is (a fraction carried until whole), what each rule did."""

    def __init__(self, w, names, budget, used, results):
        self.w, self.budget, self.used, self.results = w, budget, used, results
        self.work = {n: float(w.s["people"][n].get("chore_carry") or 0.0) for n in names}
        self.fired = set()
        self.empty = set()                                                     # (person, act) that gave nothing today (W-104)
        self.rec = {"fired": [], "partly": [], "missed": [], "against": [], "rest": {}}

    def spare(self, n) -> float:
        return float(self.budget[n]) - float(self.used[n]) - self.work[n]

    def can(self, n) -> bool:
        return self.spare(n) >= 1.0 - 1e-9

    def charge(self, n, f) -> None:
        self.work[n] += float(f)

    def close(self) -> None:
        for n, x in self.work.items():
            whole = int(x + 1e-9)
            self.used[n] += whole
            frac = round(x - whole, 4)
            if frac != round(float(self.w.s["people"][n].get("chore_carry") or 0.0), 4):
                self.w.apply("set", self.w.place_of(("person", n)), ref=("person", n), field="chore_carry", value=frac)


def _steps(w, a, b) -> int:
    """Parcel steps between two buildings (0 on one parcel)."""
    pa, pb = w.s["buildings"][a]["parcel"], w.s["buildings"][b]["parcel"]
    if pa == pb:
        return 0
    seen, frontier, k = {pa}, [pa], 0
    while frontier and k < 12:
        k += 1
        nxt = []
        for p in frontier:
            for q in w.s["parcels"][p].get("adj") or []:
                if q == pb:
                    return k
                if q not in seen and q in w.s["parcels"]:
                    seen.add(q)
                    nxt.append(q)
        frontier = nxt
    return k


# ---------------------------------------------------------------------------------------------------------------------- standing fallback
def set_fallback(w, name, acts) -> None:
    """The reply's `fallback` field sets one's standing fallback, which stands until changed (L-142; u6 Departure 6): one's own `do`
    with no condition (D2-339). An empty field changes nothing."""
    acts = [x for x in (acts or []) if isinstance(x, dict) and str(x.get("do", "")).lower() not in FREE_OR_TRAVEL][:3]
    if not acts:
        return
    key = f"person:{name}"
    bk = book(w, key)
    old = next((r for r in bk["rules"] if r["rule"] in ("do", "chore") and r.get("standing")), None)
    if old and old.get("acts") == acts and old["rule"] == "do":
        return
    n = int(old["n"]) if old else int(bk.get("n", 1))
    r = {"n": n, "rule": "do", "for": "me", "who": "me", "acts": acts, "standing": True, "set_day": w.d, "set_by": name}
    rs = [x for x in bk["rules"] if int(x["n"]) != n] + [r]
    _write(w, w.at(name) or next(iter(sorted(w.s["nodes"]))), key, {**bk, "rules": sorted(rs, key=lambda x: int(x["n"])),
                                                                    "n": max(int(bk.get("n", 1)), n + 1)})


# ---------------------------------------------------------------------------------------------------------------------- the spare units
def spare_units(w, names, order, budget, used, results, replies=None, skip=()) -> dict:
    """After every plan (u6 §5; D2-301, D2-339): person by person, their own `do` rules (those with a condition that holds, then their
    standing fallback), then, with units still spare, the household's: its `do` rules with a condition, each by whom it names (whoever
    has time: those with the most units left first) while it holds, then its `do` rules with none for each they name. A rule's act is
    an ordinary act at its own units, again while the units allow and it can be done. A rule never takes units from a plan; units
    left are rest. Returns the day's record (today["book"])."""
    d = Day(w, [n for n in names if n not in skip], budget, used, results)
    live = [n for n in order if n not in skip and w.s["people"][n]["alive"]]
    if replies:                                                               # the reply's field sets one's standing fallback (L-142)
        for n in live:
            set_fallback(w, n, (replies.get(n) or {}).get("fallback"))
    for n in live:                                                            # 1: one's own, conditions first, then the fallback
        mine = [r for r in _ranked(w, own_rules(w, n)) if r["rule"] == "do"]
        for r in [r for r in mine if r.get("when") or r.get("unless")] + [r for r in mine if not (r.get("when") or r.get("unless"))]:
            if w.at(n) is not None and _applies(w, w.household_of(n), w.at(n), r, n):
                _run(w, d, r, n, own=True)
    for hh in sorted({w.household_of(n) for n in live if w.household_of(n)}):   # 2: the household's
        members = [n for n in live if w.household_of(n) == hh]
        head = w.head(hh)
        hr = [r for r in _ranked(w, household_rules(w, hh)) if r["rule"] == "do"]
        missed = {}
        for _ in range(ROUNDS):                                               # one rule's work can make another's hold (cascades)
            fired = len(d.rec["fired"])
            for r in [r for r in hr if r.get("when") or r.get("unless")]:
                who = people_of(w, head, r.get("who")) if r.get("who") not in (None, "whoever has time") else None
                for node in sorted({w.at(n) for n in members if w.at(n) is not None}):
                    at = [n for n in members if w.at(n) == node and (who is None or n in who)]
                    if not _applies(w, hh, node, r, head):
                        continue
                    cands = sorted([n for n in at if d.can(n)], key=lambda n: (-d.spare(n), n))
                    if not cands:
                        missed[(r["n"], node)] = {"rule": r["n"], "household": hh, "person": None, "what": reading(w, r),
                                                  "why": "no one it names had units left there"}
                        continue
                    for n in cands:
                        if not _applies(w, hh, node, r, head):
                            break
                        _run(w, d, r, n, own=False)
            if len(d.rec["fired"]) == fired:
                break
        d.rec["missed"] += list(missed.values())
        for n in members:                                                     # 3: its fallbacks, for each they name
            for r in [r for r in hr if not (r.get("when") or r.get("unless"))]:
                who = people_of(w, head, r.get("who")) if r.get("who") not in (None, "whoever has time") else None
                if who is None or n in who:
                    _run(w, d, r, n, own=False, fallback=True)
    for n in live:
        left = int(d.spare(n) + 1e-9)
        if left > 0:
            d.rec["rest"][n] = left
    d.close()
    t = w.s.get("today")
    if t is not None:
        prev = t.get("book") or {}
        d.rec["against"] = list(prev.get("against") or []) + d.rec["against"]
        t["book"] = d.rec
    return d.rec


# ---------------------------------------------------------------------------------------------------------------------- an act that gives nothing
QUIET_PRIMS = ("learn", "wear", "draw", "harm")                 # practice, a tool's wear, a stock drawn, the body: not what an act gives
QUIET_TODAY = ("worked", "route", "book")                        # where one worked, one's walk, the book's own record


class _Watch:
    """What one act changed (W-104): the primitives it applied, and the day's record outside its bookkeeping. An act gave nothing when
    it moved no goods, changed no thing but its doer, and left the day's record as it was."""

    def __init__(self, w, name):
        from cybertron2.engine.world import PRIMITIVES
        self.w, self.name, self.calls, self.hooks = w, name, [], []
        for p in PRIMITIVES:
            fn = (lambda w_, call, out: self.calls.append((call["prim"], call["kw"], out)))
            w.hooks.setdefault(("after", p), []).append(fn)
            self.hooks.append((p, fn))
        self.today = self._sig()

    def _sig(self) -> dict:
        import json
        t = self.w.s.get("today") or {}
        return {k: hash(json.dumps(v, sort_keys=True, default=str)) for k, v in t.items() if k not in QUIET_TODAY}

    def close(self) -> bool:
        """Stop watching; True if the act gave or changed something."""
        for p, fn in self.hooks:
            self.w.hooks[("after", p)].remove(fn)
        for prim, kw, out in self.calls:
            if prim in QUIET_PRIMS:
                continue
            if prim == "set" and tuple(kw.get("ref") or ()) == ("person", self.name):
                continue
            if prim in ("create", "transfer", "destroy"):
                q = out if isinstance(out, (int, float)) else kw.get("qty")
                if not q or float(q) <= 1e-6:
                    continue
            return True
        return self._sig() != self.today


def _act_key(a) -> str:
    import json
    return json.dumps(a, sort_keys=True, default=str)


def _line(r, own, words) -> str:
    return (f"By your rule {r['n']}: " if own else f"By the household's rule {r['n']}: ") + words


def _run(w, d, r, n, own, fallback=False) -> bool:
    """A `do` rule's act by one person: again and in order while their units allow, it can be done and its condition holds; whole
    acts at their own units; travel and free acts never. True if anything was done."""
    from cybertron2.engine import verbs as V
    from cybertron2.engine.here import Here, Mind
    acts = [x for x in (r.get("acts") or [r.get("act")]) if isinstance(x, dict)][:3]
    hh = w.household_of(n)
    head = (w.head(hh) if hh else None) or n
    did = False
    standing = bool(r.get("standing")) or (own and not (r.get("when") or r.get("unless")))
    for _ in range(int(d.budget[n]) + 1):
        done = False
        for a in acts:
            node = w.at(n)
            if node is None or not d.can(n) or not _applies(w, hh, node, r, n if own else head):
                return did
            if (n, _act_key(a)) in d.empty:                                    # it gave nothing today: not again (W-104)
                continue
            here, mind = Here(w, n), Mind(w, n)
            c = V.cost(here, a)
            if c <= 0 or c > d.spare(n) + 1e-9 or str(a.get("do", "")).lower() in FREE_OR_TRAVEL:
                continue
            watch = _Watch(w, n)
            try:
                res = V.do(here, mind, a)
            finally:
                gave = watch.close()
            if res.startswith("Refused"):
                if not did and (r.get("when") or r.get("unless")):
                    d.rec["missed"].append({"rule": r["n"], "person": n, "household": None if own else hh, "what": reading(w, r), "why": res})
                continue
            d.used[n] += c
            if standing:
                line = res + " (your fallback)"
            elif fallback:
                line = res + f" (the household's rule {r['n']}: units left over)"
            else:
                line = _line(r, own, res)
            if not gave:                                                      # stopped for the day, and shown (W-104)
                d.empty.add((n, _act_key(a)))
                line += " It gave nothing, so it was not tried again today."
                d.rec.setdefault("empty", []).append({"rule": r["n"], "person": n, "own": own, "household": None if own else hh,
                                                      "fallback": standing, "act": _act_words(a)})
            d.results.setdefault(n, []).append(line)
            d.rec["fired"].append({"rule": r["n"], "person": n, "own": own, "units": c, "words": res, "fallback": standing or fallback})
            done = did = True
        if not done:
            break
    return did


# ---------------------------------------------------------------------------------------------------------------------- what each sees
GRAMMAR = ('Standing rules go in "rules": [...], free, at any time or in the evening, each {"rule": a kind, its fields, "words"?: your '
           'sentence, "for"?: household | me, "n"?: a rule\'s number to change}: set {"name", "people"?, "goods"?, "places"?}; keep '
           '{"goods", "in"?, "at least"?}; first {"goods": [in order]}; share {"order"?: [fed first when short], "who"?, "qty"?: full | '
           'half | a fraction, "goods"?}; do {"who"?, "act": an act, "when"?, "unless"?} (with no condition, a fallback); drop {"n"}. '
           'A condition is {"goods"?, "in"?, "under" | "over": n | "full" | "room": true}, {"in", "state": done | in process | fire '
           'out}, {"arrives": goods}, {"season"}, {"seen": the run | frost | rats}, {"starving": who} or {"home": who}. Yours come '
           'first; one naming a person or good before a set. As {"rule": "set", "name": "the young", "people": ["children"]}; '
           '{"rule": "do", "act": {"do": "tend", "at": "the Smokehouse"}, "when": {"in": "the Smokehouse", "state": "in process"}}.')


def rules_block(w, name) -> list:
    """The rules block in the system prompt (u6 §9): the household's rules, one's own, the grammar."""
    hh = w.household_of(name)
    out = []
    hr = household_rules(w, hh)
    head = w.head(hh) if hh else None
    if hh:
        nm = str(w.s["institutions"][hh].get("name") or hh).removeprefix("the ")
        if hr:
            out.append(f"The {nm} household's standing rules ({head} sets them{'' if head == name else '; you may propose'}):")
            out += [f"{r['n']}. {reading(w, r)}" for r in hr]
        else:
            out.append(f"The {nm} household has no standing rules yet ({head} sets them{'' if head == name else '; you may propose'}).")
    mine = own_rules(w, name)
    if mine:
        out.append("Your own rules: " + "; ".join(f"{r['n']}. " + ("your fallback: " + "; else ".join(_act_words(x) for x in r.get("acts") or [])
                                                                     + " (it comes before the household's for you)" if r.get("standing")
                                                                     else reading(w, r)) for r in mine) + ".")
    else:
        out.append("You have no rules of your own.")
    out.append(GRAMMAR)
    return out


def morning_lines(w, name) -> list:
    """What waits today by the rules (u6 §9's record; facts only): a `do` whose lasting condition holds (a lot done, a store under so
    much, a container with room or full) is still pending."""
    hh = w.household_of(name)
    node = w.at(name)
    if not hh or node is None:
        return []
    out = []
    for r in household_rules(w, hh) + own_rules(w, name):
        c = r.get("when") or {}
        if r["rule"] != "do" or not (c.get("state") == "done" or any(k in c for k in ("under", "over", "full", "room"))):
            continue
        if _applies(w, hh, node, r, w.head(hh) or name):
            out.append(f"Waiting today: {reading(w, r)} (rule {r['n']}).")
    return out


def day_lines(w, rec, name, when="yesterday") -> list:
    """The head's and the person's lines of what the book did yesterday (or today, at the evening) that they did not do themselves:
    what was missed, who went against a rule (u6 §7, §9); and a chore or fallback that gave nothing and stopped after one try (W-104)."""
    if not rec:
        return []
    hh = w.household_of(name)
    head = hh and w.head(hh) == name
    out = []
    for m in rec.get("missed") or []:
        if (m.get("household") == hh and head) or m.get("person") == name:
            out.append(f"Not done by the rules {when}: {m['what']} ({m['why']}).")
    for a in rec.get("against") or []:
        if head or a.get("by") == name:
            out.append(f"Against the household's rule {a.get('rule')}: {a['words']}.")
    out += empty_lines(rec, name, hh if head else None, when)
    return out


def empty_lines(rec, name, head_of=None, when="yesterday") -> list:
    """A chore or fallback that gave nothing (W-104), as a fact: one's own, and, for the head, the household's rules' for others."""
    out = []
    for e in (rec or {}).get("empty") or []:
        mine = e.get("person") == name
        if not mine and not (head_of and e.get("household") == head_of):
            continue
        what = ("your fallback" if e.get("fallback") else (f"your rule {e['rule']}" if e.get("own") else f"the household's rule {e['rule']}"))
        whom = "" if mine else f" {e['person']}"
        out.append(f"{what[:1].upper() + what[1:]}, {e['act']}, gave{whom} nothing {when}; it stopped after one try.")
    return out
