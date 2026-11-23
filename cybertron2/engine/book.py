"""The household book (u6; D2-274, D2-279, D2-282, D2-296, D2-301, D2-319; the build's stage 3, W-99): one book a household and one a
person, in which the routine is set: where goods go, what is kept where and held back, what is taken or eaten first, the rations, what
is moved, hung, salted and tended and by whom, and what each does with units left over. A rule reads only what its household knows;
it is shown back in the engine's own reading beside the person's words; going against a household rule is recorded.

One feature unit (D2-244; feature_packages.md §9.1, §10):
  - data: s["books"]["household:<id>" or "person:<name>"] = {"rules": [rule], "n": next number, "proposals": [rule]}, written through
    the `book` primitive (world.py), so the journal records every change; a person's `chore_carry` (a chore's fraction carried until
    whole, as the walk's);
  - verbs: `rule` (free, at any time and at the evening: D2-319), `act`; the reply's `fallback` field sets one's standing fallback
    (`set_fallback`), which stands until changed (L-142);
  - the store moments: `where_to` (goods arriving, moment 1), `keeps` (the sort, moment 2), `held` (drawing and the meal, moments 3
    and 4), `meal` (the order and the rations);
  - processes: `spare_units` after every plan (moment 5; D2-301: person by person, their own rules and their own standing fallback
    first, then the household's keeping chores, then the head's fallback chores; no fallback at the start and nothing pushing for one;
    units left are rest);
  - what each sees: `rules_block` (the system prompt), `reading` (the `rule` act's result), `morning_lines` (what waits), the day's
    record in today["book"] (what fired, what was partly done, what was missed, what went against a rule).

The grammar (u6 §2): {"do": "rule", "rule": go | keep | hold back | first | eat | move | tend | chore | drop, "for"?: household | me,
"goods"?, "to" | "in" | "from"?, "qty"?, "before"?, "who"?, "by"?, "acts"?, "when"?, "unless"?, "words"?, "n"?}.
"""
from __future__ import annotations

import math
import re

KINDS = ("go", "keep", "hold back", "first", "eat", "move", "tend", "chore", "drop")
KEEPING = ("tend", "go", "move")                     # the keeping chores, in their order (u6 §5)
ROUNDS = 3                                           # cascades at most three rounds a day; each rule once (u6 Basis rows needed, 2)
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


# ---------------------------------------------------------------------------------------------------------------------- records
def key_of(w, whose) -> str:
    return whose if whose.startswith(("household:", "person:")) else (f"household:{whose}" if whose in w.s["institutions"] else f"person:{whose}")


def book(w, key) -> dict:
    return (w.s.get("books") or {}).get(key) or {"rules": [], "n": 1, "proposals": []}


def rules(w, key) -> list:
    return list(book(w, key)["rules"])


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
    """A good, a kind of goods or everything: the items it names."""
    from cybertron2.engine.data import EDIBLE, ITEMS
    from cybertron2.engine.verbs import item_of
    if x is None:
        return ()
    t = str(x).strip().lower()
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
    except Exception:                                                         # noqa: BLE001  (an unknown good: read as words)
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
    if any(k in t for k in ("smoking", "in process", "hangs", "hanging", "curing", "anything is", "while")):
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
    if "rack" in t or "smoke" in t or (b is not None and (b.get("fittings") or {}).get("smoke racks") and "store" not in t):
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
REFUSE_TRADE = ("Refused: a rule keeps, moves and tends what is your household's, and says what someone does with units left; trade, "
                "trips and what is another's are yours to choose each day.")


def act(here, a) -> str:
    """The `rule` act (u6 §2, §9; free, at any time and at the evening: D2-319): set, change (with `n`) or drop a rule in one's own book
    or the household's (the head's; a member's is a proposal to the head). Returns the engine's reading beside their words, or why not."""
    from cybertron2.engine.world import Refused
    w = here._w
    kind = str(a.get("rule") or "").strip().lower()
    if kind not in KINDS:
        raise Refused(f"a rule is one of: {', '.join(KINDS)}")
    hh = here.household()
    whose = str(a.get("for") or "").strip().lower()
    if whose not in ("household", "me"):
        whose = "household" if hh and kind not in ("chore",) and w.head(hh) == here.name else "me"
    if kind == "chore" and a.get("who") and str(a["who"]).strip() not in (here.name, "me"):
        whose = "household"
    if whose == "household" and not hh:
        raise Refused("you belong to no household: a rule of yours goes in your own book (\"for\": \"me\")")
    key = f"household:{hh}" if whose == "household" else f"person:{here.name}"
    bk = book(w, key)
    if kind == "drop":
        n = int(_num(a.get("n"), 0) or 0)
        hit = [r for r in bk["rules"] if int(r["n"]) == n]
        if not hit:
            raise Refused(f"there is no rule {n} in {'the household' if whose == 'household' else 'your'} book")
        if whose == "household" and w.head(hh) != here.name:
            return _propose(here, key, bk, {**hit[0], "drop": True}, f"drop rule {n}")
        _write(w, here.node, key, {**bk, "rules": [r for r in bk["rules"] if int(r["n"]) != n]})
        return f"Rule {n} ({'the household' if whose == 'household' else 'yours'}) dropped: {reading(w, hit[0])}."
    r = {"rule": kind, "for": whose}
    for f in ("goods", "to", "in", "from", "qty", "before", "who", "by", "when", "unless", "words", "at"):
        if a.get(f) not in (None, "", []):
            r[f] = a[f]
    if kind == "chore":
        acts = [x for x in (a.get("acts") or []) if isinstance(x, dict)][:3]
        if not acts:
            raise Refused("a chore says what to do with units left: \"acts\", in order")
        for x in acts:
            v = str(x.get("do", "")).lower()
            if v in ("travel",) or v in FREE_OR_TRAVEL:
                raise Refused("a fallback is work for units left over: travel and free acts cannot be one")
        r["acts"] = acts
    if kind in ("go", "move", "tend", "keep"):
        why = _check_target(here, r)
        if why:
            raise Refused(why)
    for f in ("when", "unless"):
        if r.get(f) is not None and not isinstance(r[f], dict):
            r[f] = {**(state_of(r[f]) or {}), "text": str(r[f])}
    if any(str(v).lower() in ("trade", "travel", "sell", "buy") for v in (a.get("rule"), *(a.get("acts") or []))):
        raise Refused(REFUSE_TRADE)
    if a.get("n") not in (None, ""):
        n = int(_num(a["n"], 0) or 0)
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
    seen = (" (it fires the day one of you has seen the run)" if (r.get("when") or {}).get("state") == "seen" else "")
    return (f"Rule {r['n']} ({'the household' if whose == 'household' else 'yours'}): {reading(w, r)}"
            + (f" (your words: \"{r['words']}\")" if r.get("words") else "") + f".{seen} " + _when_fires(r))


def _when_fires(r) -> str:
    st = (r.get("when") or {}).get("state")
    if r["rule"] in KEEPING + ("chore",):
        if st in ("done", "room", "full", "under", "over", "in process"):
            return "It fires while that holds and waits until someone with units left has done it."
        return "It is done with units left over after the day's plans."
    return "It applies from now on."


def _propose(here, key, bk, r, what) -> str:
    w = here._w
    head = w.head(here.household())
    _write(w, here.node, key, {**bk, "proposals": list(bk.get("proposals") or []) + [{**r, "by": here.name, "day": here.day}]})
    return f"Proposed to {head}, who heads the household: {what or reading(w, r)}. It stands once {head} takes it."


def _check_target(here, r) -> str:
    w = here._w
    hh = here.household()
    for f in ("to", "in", "from", "at"):
        if not r.get(f):
            continue
        tg = target(w, hh, here.node, r[f], names(r))
        if tg["kind"] == "hands":
            continue
        if tg["bid"] is None:
            bid = _building(w, here.node, r[f])
            if bid is not None:
                return f"Refused: {w.s['buildings'][bid]['name']} is not your household's."
            if tg["kind"] in ("racks", "tub", "hearth"):
                return "Refused: your household has no " + {"racks": "smoke racks", "tub": "house to salt in", "hearth": "hearth"}[tg["kind"]] + " here"
            continue
        if not _holds(w, hh, tg["bid"]) and tg["bid"] not in here.homes_here():
            return f"Refused: {w.s['buildings'][tg['bid']]['name']} is not your household's."
        if tg.get("proc") == "hard cure" and w.s["buildings"][tg["bid"]].get("structure") not in ("timber", "stone"):
            return (f"Refused: a hard cure needs the long cool smoke of a timber or stone smokehouse; the fire in "
                    f"{w.s['buildings'][tg['bid']]['name']} hangs too close and hot.")
    return ""


def reading(w, r) -> str:
    """The engine's reading of a rule (u6 §9)."""
    g = r.get("goods") or ("everything" if r["rule"] in ("keep", "hold back") else "")
    q = r.get("qty")
    q = f"{q} " if q not in (None, "", "all") else ""
    wn = state_words(r.get("when"))
    un = state_words(r.get("unless"))
    tail = (f", when {wn}" if wn else "") + (f", unless {un}" if un else "")
    by = r.get("by") or ("" if r["rule"] in ("keep", "hold back", "first", "eat") else "whoever has time" if r.get("for") == "household" else "")
    by = f"; {by}" if by else ""
    k = r["rule"]
    if k == "go":
        return f"{q}{g} that comes in goes to {r.get('to') or 'the house'}{tail}{by}"
    if k == "move":
        return f"move {q}{g} from {r.get('from') or 'the store'} to {r.get('to') or 'the house'}{tail}{by}"
    if k == "tend":
        return f"tend the fire in {r.get('at') or r.get('in') or 'the smokehouse'}{tail or ', while anything is smoking'}{by}"
    if k == "keep":
        return f"keep {q}{g} in {r.get('in') or r.get('to') or 'the store'}{tail}"
    if k == "hold back":
        return f"hold back {q}{g}: not drawn or eaten{tail}"
    if k == "first":
        return f"take or eat {g} first" + (f", before {r['before']}" if r.get("before") else "") + tail
    if k == "eat":
        return f"eat {r.get('qty') or 'full'} rations" + (f", {r['who']} first" if r.get("who") else "") + tail
    if k == "chore":
        acts = "; else ".join(_act_words(x) for x in r.get("acts") or [])
        who = r.get("who") or "you"
        return f"with units left over: {who} {acts}{tail}"
    return k


def _act_words(x) -> str:
    return " ".join(str(v) for k, v in x.items() if k in ("do", "what", "item", "at") and v)


# ---------------------------------------------------------------------------------------------------------------------- the store moments
def where_to(w, name, item) -> str | None:
    """Goods arriving for one's household (moment 1, u6 §4): the store a `go` rule names (one's own first, then the household's),
    when its state holds; a `go` into a container leaves them in that building's store, pending as a load chore. None: no rule."""
    hh = w.household_of(name)
    node = w.at(name)
    for r in own_rules(w, name) + household_rules(w, hh):
        if r["rule"] != "go" or not (item in names(r) or "*" in names(r)):
            continue
        if not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False):
            continue
        tg = target(w, hh, node, r.get("to"), (item,))
        if tg.get("bid") and _holds(w, hh, tg["bid"]):
            return w.s["buildings"][tg["bid"]]["stock"]
    return None


def install(w) -> None:
    """Moment 1 (u6 §4): goods coming into a household's store (work done for it, a gift, a purchase, salting) go where its `go` rules
    send them, to another of its stores here; a `go` into a container leaves them where they came, pending as a load chore."""
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
        for r in household_rules(w, hh):
            if r["rule"] != "go" or not (item in names(r) or "*" in names(r)):
                continue
            if not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False):
                continue
            tg = target(w, hh, node, r.get("to"), (item,))
            if tg["kind"] == "store" and tg.get("bid") and tg["bid"] != bid and _holds(w, hh, tg["bid"]):
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
        for r in household_rules(w, hh):
            if r["rule"] != "keep":
                continue
            tg = target(w, hh, w.s["buildings"][bid]["node"], r.get("in") or r.get("to"), names(r))
            if tg.get("bid") != bid:
                continue
            q = _num(r.get("qty"))
            for it in names(r):
                if it != "*":
                    out.append((it, tg["kind"] if tg["kind"] not in ("store",) else "floor", q))
        break
    return out


def held(w, name, cid, item) -> float:
    """What of a good in a store is held back from one's drawing and eating (moments 3, 4): the household's `hold back` rules for
    goods in its stores, unless their `unless` holds, or one's own rule says otherwise (going against it, recorded)."""
    c = w.s["containers"].get(cid) or {}
    if c.get("kind") != "stock":
        return 0.0
    hh = w.household_of(name)
    if not hh or not _holds(w, hh, c["of"]):
        return 0.0
    node = w.s["buildings"][c["of"]]["node"]
    out = 0.0
    for r in household_rules(w, hh):
        if r["rule"] != "hold back" or not (item in names(r) or "*" in names(r)):
            continue
        if r.get("in") or r.get("at"):
            tg = target(w, hh, node, r.get("in") or r.get("at"), names(r))
            if tg.get("bid") not in (None, c["of"]):
                continue
        if not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False, who=name):
            continue
        if any(x["rule"] in ("first", "eat") and item in names(x) for x in own_rules(w, name)):
            _against(w, name, r, f"{name}'s own rule takes the {item} the household holds back")
            continue
        q = _num(r.get("qty"))
        out += float(w.goods(cid).get(item, 0.0)) if q is None else q
    return out


def meal(w, name) -> dict:
    """The night's meal by the book (moment 4): {"first": [items in order], "ration": a share of the need}."""
    hh = w.household_of(name)
    node = w.at(name)
    first, ration = [], 1.0
    for r in own_rules(w, name) + household_rules(w, hh):
        if not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False, who=name):
            continue
        if r["rule"] == "first":
            first += [i for i in names(r) if i not in first and i != "*"]
        elif r["rule"] == "eat" and ration == 1.0:
            q = str(r.get("qty") or "full").lower()
            ration = 0.5 if "half" in q else (min(1.0, float(_num(q, 1.0))) if _num(q) is not None and _num(q) <= 1.0 else 1.0)
    return {"first": first, "ration": ration}


def _against(w, name, r, words) -> None:
    t = w.s.get("today")
    if t is not None:
        t.setdefault("book", {}).setdefault("against", []).append({"by": name, "rule": r.get("n"), "words": words})


# ---------------------------------------------------------------------------------------------------------------------- states
def holds(w, hh, node, r, st, empty, who=None) -> bool:
    """Whether a state holds for a household now (u6 §3), read only from what it knows: its own containers and stores, its members'
    acts, the calendar, and what its members noticed. `empty`: the answer for no state."""
    if not st:
        return empty
    from cybertron2.engine import process as PROC
    k = st.get("state")
    if k == "season":
        return w.calendar()["season"] == st.get("what")
    if k == "starving":
        ms = [who] if who else (w.members(hh) if hh else [])
        return any(w.s["people"][m]["alive"] and int(w.s["people"][m].get("hunger", 0)) <= -2 for m in ms if m in w.s["people"])
    if k == "seen":
        return seen(w, hh, st.get("set") or "run")
    if k in ("home", "away"):
        nm = next((m for m in (w.members(hh) if hh else []) if m.lower() in str(st.get("what", "")).lower()), None)
        if nm is None:
            return k == "home"
        return (w.at(nm) == node) == (k == "home")
    if k == "words":
        return False
    if st.get("of"):                                                          # the state of a named container or store
        tg = target(w, hh, node, st["of"], names(r))
    elif k in ("under", "over") and r["rule"] == "move":                      # a move's under n reads where it goes
        tg = target(w, hh, node, r.get("to"), names(r))
    else:
        tg = target(w, hh, node, r.get("from") or r.get("to") or r.get("in") or r.get("at"), names(r))
    bid = tg.get("bid")
    if r["rule"] == "tend" and bid is None:
        bid = next((x for x in sorted(w.s["buildings"]) if w.s["buildings"][x]["node"] == node and _holds(w, hh, x)
                    and (w.s["buildings"][x].get("fittings") or {}).get("smoke racks")), None)
    if k == "arrives":
        return any(_store_have(w, hh, node, i) > 1e-6 for i in names(r) if i != "*")
    if bid is None:
        return False
    if k in ("done", "in process", "room", "full", "fire out"):
        s = PROC.states(w, hh, bid)
        return {"done": s["done"] > 1e-6, "in process": s["in process"] > 1e-6, "room": s["room"] > 1e-6, "full": s["full"],
                "fire out": s["fire out"]}[k]
    if k in ("under", "over"):
        q = sum(float(w.goods(w.s["buildings"][bid]["stock"]).get(i, 0.0)) for i in names(r) if i != "*")
        return q < float(st.get("n") or 0) if k == "under" else q > float(st.get("n") or 0)
    return False


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


# ---------------------------------------------------------------------------------------------------------------------- standing fallback
def set_fallback(w, name, acts) -> None:
    """The reply's `fallback` field sets one's standing fallback, which stands until changed (L-142; u6 Departure 6): one's own
    `chore` rule. An empty field changes nothing."""
    acts = [x for x in (acts or []) if isinstance(x, dict) and str(x.get("do", "")).lower() not in FREE_OR_TRAVEL][:3]
    if not acts:
        return
    key = f"person:{name}"
    bk = book(w, key)
    old = next((r for r in bk["rules"] if r["rule"] == "chore" and r.get("standing")), None)
    if old and old.get("acts") == acts:
        return
    n = int(old["n"]) if old else int(bk.get("n", 1))
    r = {"n": n, "rule": "chore", "for": "me", "acts": acts, "standing": True, "set_day": w.d, "set_by": name}
    rs = [x for x in bk["rules"] if int(x["n"]) != n] + [r]
    _write(w, w.at(name) or next(iter(sorted(w.s["nodes"]))), key, {**bk, "rules": sorted(rs, key=lambda x: int(x["n"])),
                                                                    "n": max(int(bk.get("n", 1)), n + 1)})


# ---------------------------------------------------------------------------------------------------------------------- the spare units
class Day:
    """The spare-units phase's account of a day (u6 §5): each one's spare whole units, the chores' real fractions summed and charged
    as the walk is (a fraction carried until whole), what each rule did."""

    def __init__(self, w, names, budget, used, results):
        self.w, self.budget, self.used, self.results = w, budget, used, results
        self.work = {n: float(w.s["people"][n].get("chore_carry") or 0.0) for n in names}
        self.fired = set()
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


def spare_units(w, names, order, budget, used, results, replies=None, skip=()) -> dict:
    """Moment 5 (u6 §5; D2-301, D2-296): after every plan, person by person, their own book first (their own keeping rules, then their
    own standing fallback), then, with units still spare, the household's keeping chores (tend, then loads, the most perishable first,
    then the moves out of containers, then other moves), then the head's fallback chores for them. A chore never takes units from a
    plan; units left are rest. Returns the day's record (today["book"])."""
    from cybertron2.engine.here import Here, Mind
    d = Day(w, [n for n in names if n not in skip], budget, used, results)
    live = [n for n in order if n not in skip and w.s["people"][n]["alive"]]
    if replies:                                                               # the reply's field sets one's standing fallback (L-142)
        for n in live:
            set_fallback(w, n, (replies.get(n) or {}).get("fallback"))
    for n in live:                                                            # 1: one's own keeping rules, then one's own fallback
        mine = [r for r in own_rules(w, n) if r["rule"] in KEEPING]
        _keeping(w, d, mine, w.household_of(n), [n], own=n)
        _fallback(w, d, n, [r for r in own_rules(w, n) if r["rule"] == "chore"])
    for hh in sorted({w.household_of(n) for n in live if w.household_of(n)}):   # 2: the household's keeping chores
        members = [n for n in live if w.household_of(n) == hh]
        for _ in range(ROUNDS):
            before = len(d.fired)
            _keeping(w, d, [r for r in household_rules(w, hh) if r["rule"] in KEEPING], hh, members)
            if len(d.fired) == before:
                break
        for n in members:                                                     # 3: the head's fallback chores for each
            mine = [r for r in household_rules(w, hh) if r["rule"] == "chore" and _for_person(w, r, n)]
            _fallback(w, d, n, mine, household=True)
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


def _for_person(w, r, n) -> bool:
    who = str(r.get("who") or "").strip()
    return not who or who.lower() in ("everyone", "all", "the household", "whoever has time") or who == n


def _order(rs) -> list:
    """The keeping chores' order (u6 §5): tend, then loads (the most perishable goods first), then moves out of a container, then
    other moves; within each, the book's own order."""
    from cybertron2.engine.data import ITEMS

    def k(r):
        kind = KEEPING.index(r["rule"])
        spoil = -max([float(ITEMS.get(i, {}).get("spoil", 0.0)) for i in names(r) if i != "*"] or [0.0])
        out = 0 if r["rule"] == "move" and any(x in str(r.get("from") or "").lower() for x in ("rack", "smoke", "hearth")) else 1
        return (kind, spoil if r["rule"] == "go" else 0, out, int(r["n"]))
    return sorted(rs, key=k)


def _keeping(w, d, rs, hh, people, own=None) -> None:
    for r in _order(rs):
        rid = (own or hh, int(r["n"]))
        if rid in d.fired:
            continue
        node = w.at(people[0]) if people else None
        if node is None:
            continue
        if not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False):
            continue
        if own is None:
            cands = _who(w, d, r, people, node, hh)
        else:
            cands = [own] if d.can(own) and w.at(own) == node else []
        if not cands:
            if _pending(w, hh, node, r):
                d.rec["missed"].append({"rule": r["n"], "household": hh if own is None else None, "person": own,
                                        "what": reading(w, r), "why": "no one of the household with units left was there"})
            continue
        for n in cands:
            got = _do_chore(w, d, r, n, hh, node, own)
            if got:
                d.fired.add(rid)
                break


def _who(w, d, r, people, node, hh) -> list:
    """Who does a household chore (u6 §5): its `by`; or whoever has time: the members at the node with at least 1 spare unit, the most
    spare first, then by name. A member whose own rule says otherwise for the same goods is passed over, and that is recorded."""
    at = [n for n in people if w.at(n) == node and d.can(n)]
    out = []
    for n in at:
        if any(x["rule"] == r["rule"] and set(names(x)) & set(names(r)) for x in own_rules(w, n)):
            d.rec["against"].append({"by": n, "rule": r["n"], "words": f"{n}'s own rule for the same goods comes before the household's rule {r['n']}"})
            continue
        out.append(n)
    by = str(r.get("by") or "").strip()
    named = [n for n in out if n == by]
    if by and by.lower() not in ("whoever has time", "anyone", "everyone"):
        if named:
            return named
        if by in (w.members(hh) if hh else []):
            d.rec["against"].append({"by": by, "rule": r["n"], "words": f"rule {r['n']} had {by} do it, and {by} had no units left there"})
    return sorted(out, key=lambda n: (-d.spare(n), n))


def _pending(w, hh, node, r) -> bool:
    """Whether a keeping rule has work waiting (for the missed line): goods to load, a done lot to take down, a fire to keep."""
    from cybertron2.engine import process as PROC
    tg = target(w, hh, node, r.get("from") or r.get("to") or r.get("at") or r.get("in"), names(r))
    if r["rule"] == "tend":
        bid = tg.get("bid") if tg.get("kind") == "racks" else next((x for x in sorted(w.s["buildings"]) if w.s["buildings"][x]["node"] == node
                                                                   and _holds(w, hh, x) and PROC.is_smokehouse(w.s["buildings"][x])), None)
        return bool(bid) and any(PROC.PROCESSES[c["lot"]["process"]].get("fire") for c in PROC.lots(w, bid, done=False).values())
    if r["rule"] == "go":
        return any(_store_have(w, hh, node, i) > 1e-6 for i in names(r) if i != "*")
    if r["rule"] == "move" and tg.get("bid"):
        return PROC.states(w, hh, tg["bid"])["done"] > 1e-6 or any(float(w.goods(w.s["buildings"][tg["bid"]]["stock"]).get(i, 0.0)) > 1e-6
                                                               for i in names(r) if i != "*")
    return False


def _line(r, own, words) -> str:
    return (f"By your rule {r['n']}: " if own else f"By the household's rule {r['n']}: ") + words


def _do_chore(w, d, r, n, hh, node, own) -> bool:
    """One keeping chore by one person, at its real work (u6 §5: hanging 30 kg a unit, a salted lot 60, salting 40, a hearth's rack 8,
    taking down 120, tending 1; moving between buildings 1 unit per 800 kg a parcel step): as much as their spare units allow, the
    rest falling to the next rule or waiting. True if anything was done."""
    from cybertron2.engine import process as PROC, verbs as V
    from cybertron2.engine.here import Here, Mind
    from cybertron2.engine.world import Refused
    here, mind = Here(w, n), Mind(w, n)
    spare = d.spare(n)
    kind = r["rule"]
    try:
        if kind == "tend":
            tg = target(w, hh, node, r.get("at") or r.get("in") or r.get("to"), ())
            bid = tg["bid"] if tg.get("kind") == "racks" and tg.get("bid") else next(
                (x for x in sorted(w.s["buildings"]) if w.s["buildings"][x]["node"] == node and _holds(w, hh, x)
                 and PROC.is_smokehouse(w.s["buildings"][x]) and PROC.lots(w, x, done=False)), None)
            if bid is None or not any(PROC.PROCESSES[c["lot"]["process"]].get("fire") for c in PROC.lots(w, bid, done=False).values()):
                return False
            if (w.s["buildings"][bid].get("smoke") or {}).get("tended") == w.d:
                return False
            if spare < 1.0 - 1e-9:
                return False
            out = PROC.tend(here, bid)
            d.charge(n, 1.0)
            _record(d, r, n, own, out, 1.0)
            return True
        if kind == "go":
            tg = target(w, hh, node, r.get("to"), names(r))
            if tg["kind"] in ("racks", "tub", "hearth") and tg.get("bid"):
                return _load(w, d, r, n, hh, node, own, tg, here, mind, spare)
            return False
        if kind == "move":
            src = target(w, hh, node, r.get("from"), names(r))
            dst = target(w, hh, node, r.get("to"), names(r))
            if src["kind"] in ("racks", "hearth") and src.get("bid"):
                done = PROC.states(w, hh, src["bid"])["done"]
                if done <= 1e-6:
                    return False
                item = next((i for i in names(r) if i != "*"), None)
                cap = min(spare, float(_num(r.get("qty"), 1e9)) / PROC.WORK["take down"])
                if cap * PROC.WORK["take down"] < 0.5:
                    return False
                to = dst["bid"] if dst.get("bid") and dst["bid"] != src["bid"] else ("hands" if dst["kind"] == "hands" else None)
                got, words = PROC.take_down(here, src["bid"], item, None if r.get("qty") in (None, "all") else _num(r["qty"]), to, units=cap)
                f = got / PROC.WORK["take down"]
                if to not in (None, "hands"):
                    f += got * _steps(w, src["bid"], to) / MOVE_KG_STEP
                d.charge(n, f)
                _record(d, r, n, own, words, f, partly=done - got > 1e-6)
                return True
            if src.get("bid") and dst.get("bid") and src["bid"] != dst["bid"]:
                return _move_store(w, d, r, n, hh, node, own, src["bid"], dst["bid"], here, spare)
            return False
    except Refused as e:
        d.rec["missed"].append({"rule": r["n"], "person": n, "what": reading(w, r), "why": str(e)})
        return False
    return False


def _load(w, d, r, n, hh, node, own, tg, here, mind, spare) -> bool:
    """A `go` into a container (a load chore): the goods drawn from the household's stores here (not hands), as much as the room, the
    rule's qty and the doer's spare units allow, then loaded by the engine's own act."""
    from cybertron2.engine import process as PROC, verbs as V
    from cybertron2.engine.data import TECHNIQUES
    bid = tg["bid"]
    for item in [i for i in names(r) if i != "*"]:
        tech = _tech(tg["proc"], item)
        if tech is None:
            continue
        rate = float(PROC.PROCESSES[tg["proc"]]["load"])
        have = sum(float(w.goods(c).get(item, 0.0)) for c in _stock_cids(w, hh, node, item))
        kg = min(have, spare * rate, float(_num(r.get("qty"), 1e9)))
        if tg["proc"] != "salting":
            kg = min(kg, PROC.room(w, bid, tg["proc"]))
            why = PROC.refuse_load(here, tech, bid) if kg > 1e-6 else ""
            if why:
                continue
        else:
            kg = min(kg, sum(float(w.goods(c).get("salt", 0.0)) for c in _stock_cids(w, hh, node, "salt")) / float(PROC.PROCESSES["salting"]["salt"][item])
                     + float(here.carried().get("salt", 0.0)) / float(PROC.PROCESSES["salting"]["salt"][item]))
        kg = round(kg, 4)
        if kg < 0.5:
            if tg["proc"] == "salting" and have > 0.5:
                d.rec["missed"].append({"rule": r["n"], "person": n, "what": reading(w, r), "why": f"there is no salt in the household's stores here"})
            continue
        left = kg
        for c in _stock_cids(w, hh, node, item):                               # into the doer's hands, then loaded from them
            q = min(left, float(w.goods(c).get(item, 0.0)))
            if q > 1e-9:
                here.apply("transfer", src=c, dst=here.hands, item=item, qty=round(q, 6))
                left -= q
            if left <= 1e-9:
                break
        if tg["proc"] == "salting":
            here._chore = True
            out = PROC.salt(here, tech, bid, kg)
        else:
            out = V.do(here, Mind_(w, n), {"do": "make", "what": tech, "qty": max(1, math.ceil(kg / rate - 1e-9)),
                                           "at": w.s["buildings"][bid]["name"], "_kg": kg})
        if out.startswith("Refused"):
            back = float(here.carried().get(item, 0.0))
            d.rec["missed"].append({"rule": r["n"], "person": n, "what": reading(w, r), "why": out})
            return False
        f = kg / rate
        d.charge(n, f)
        rest = have - kg
        _record(d, r, n, own, out, f, partly=rest > 0.5)
        return True
    return False


def Mind_(w, n):
    from cybertron2.engine.here import Mind
    return Mind(w, n)


def _move_store(w, d, r, n, hh, node, own, src, dst, here, spare) -> bool:
    """Goods moved between two of the household's buildings here (u6 §5): 1 unit per 800 kg a parcel step (D2-274, provisional);
    within one building free."""
    from cybertron2.engine.world import show
    steps = _steps(w, src, dst)
    moved = []
    f = 0.0
    for item in [i for i in names(r) if i != "*"]:
        have = float(w.goods(w.s["buildings"][src]["stock"]).get(item, 0.0))
        q = min(have, float(_num(r.get("qty"), 1e9)))
        if steps:
            from cybertron2.engine.data import ITEMS
            wt = float(ITEMS.get(item, {}).get("weight", 1))
            q = min(q, (spare - f) * MOVE_KG_STEP / max(1e-9, steps * wt))
        if q <= 1e-6:
            continue
        from cybertron2.engine import buildings as BL
        q = min(q, BL.room_for(w.s["buildings"][dst], w.goods(w.s["buildings"][dst]["stock"]), item))
        if q <= 1e-6:
            continue
        w.apply("transfer", node, src=w.s["buildings"][src]["stock"], dst=w.s["buildings"][dst]["stock"], item=item, qty=round(q, 6))
        from cybertron2.engine.data import ITEMS
        f += q * float(ITEMS.get(item, {}).get("weight", 1)) * steps / MOVE_KG_STEP
        moved.append(f"{show(round(q, 1))} {item}")
    if not moved:
        return False
    d.charge(n, f)
    _record(d, r, n, own, f"You moved {', '.join(moved)} from {w.s['buildings'][src]['name']} into {w.s['buildings'][dst]['name']}.", f)
    return True


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


def _record(d, r, n, own, words, f, partly=False) -> None:
    rec = {"rule": r["n"], "person": n, "own": bool(own), "units": round(float(f), 2), "words": words}
    d.rec["partly" if partly else "fired"].append(rec)
    d.results.setdefault(n, []).append(_line(r, own, words) + (f" ({round(float(f), 2):g} units of work)" if "units of work" not in words else ""))


def _fallback(w, d, n, rs, household=False) -> None:
    """A standing fallback (u6 §6; D4-76's loop kept): its acts, in order and again, while the units allow and any can be done; `when`
    and `unless` let it follow need. Whole acts at their own units; travel and free acts never."""
    from cybertron2.engine import verbs as V
    from cybertron2.engine.here import Here, Mind
    for r in rs:
        hh = w.household_of(n)
        node = w.at(n)
        if node is None or not holds(w, hh, node, r, r.get("when"), True) or holds(w, hh, node, r, r.get("unless"), False):
            continue
        acts = [x for x in r.get("acts") or [] if isinstance(x, dict)][:3]
        for _ in range(int(d.budget[n]) + 1):
            if not d.can(n):
                return
            done = False
            for a in acts:
                here, mind = Here(w, n), Mind(w, n)
                c = V.cost(here, a)
                if c <= 0 or c > d.spare(n) + 1e-9 or str(a.get("do", "")).lower() in FREE_OR_TRAVEL:
                    continue
                res = V.do(here, mind, a)
                if res.startswith("Refused"):
                    continue
                d.used[n] += c
                d.results.setdefault(n, []).append(res + (" (your fallback)" if not household else f" (the household's rule {r['n']}: units left over)"))
                d.rec["fired"].append({"rule": r["n"], "person": n, "own": not household, "units": c, "words": res, "fallback": True})
                done = True
                if not d.can(n):
                    return
            if not done:
                break


# ---------------------------------------------------------------------------------------------------------------------- what each sees
GRAMMAR = ("A standing rule says, in your words: where goods go; where something is kept, or how much is held back; what is taken or "
           "eaten first; what is moved, hung, salted or tended, and by whom; what someone does with units left over. It may say "
           "\"when\" (a lot is done, a store is full or has room, a store holds under so much, something is seen, a season) or "
           "\"unless\" (someone is starving, it is winter, it is full). The most specific rule wins, yours before the household's. "
           "Setting, changing or dropping a rule costs nothing (\"rule\"), at any time or at the evening.")


def rules_block(w, name) -> list:
    """The rules block in the system prompt (u6 §9): the household's rules, one's own, the grammar."""
    hh = w.household_of(name)
    out = []
    hr = household_rules(w, hh)
    head = w.head(hh) if hh else None
    if hh:
        nm = w.s["institutions"][hh].get("name") or hh
        if hr:
            out.append(f"The {nm} household's standing rules ({head} sets them{'' if head == name else '; you may propose'}):")
            out += [f"{r['n']}. {reading(w, r)}" for r in hr]
        else:
            out.append(f"The {nm} household has no standing rules yet ({head} sets them{'' if head == name else '; you may propose'}).")
    mine = own_rules(w, name)
    if mine:
        out.append("Your own rules: " + "; ".join(f"{r['n']}. " + ("your fallback: " + "; else ".join(_act_words(x) for x in r.get("acts") or [])
                                                                     + " (it comes before the household's chores for you)" if r.get("standing")
                                                                     else reading(w, r)) for r in mine) + ".")
    else:
        out.append("You have no rules of your own.")
    out.append(GRAMMAR)
    return out


def morning_lines(w, name) -> list:
    """What waits today by the household's rules (u6 §9's record; facts only): a lasting state's rule not done is still pending."""
    hh = w.household_of(name)
    node = w.at(name)
    if not hh or node is None:
        return []
    out = []
    for r in household_rules(w, hh) + own_rules(w, name):
        if r["rule"] not in KEEPING:
            continue
        if holds(w, hh, node, r, r.get("when"), True) and not holds(w, hh, node, r, r.get("unless"), False) and _pending(w, hh, node, r):
            st = (r.get("when") or {}).get("state")
            if st in ("done", "room", "full", "under", "over", "fire out"):
                out.append(f"Waiting today: {reading(w, r)} (rule {r['n']}: {state_words(r.get('when'))}).")
    return out


def day_lines(w, rec, name) -> list:
    """The head's and the person's lines of what the book did yesterday that they did not do themselves: what was missed, who went
    against a rule (u6 §7, §9)."""
    if not rec:
        return []
    hh = w.household_of(name)
    head = hh and w.head(hh) == name
    out = []
    for m in rec.get("missed") or []:
        if (m.get("household") == hh and head) or m.get("person") == name:
            out.append(f"Not done by the rules yesterday: {m['what']} ({m['why']}).")
    for a in rec.get("against") or []:
        if head or a.get("by") == name:
            out.append(f"Against the household's rule {a.get('rule')}: {a['words']}.")
    return out
