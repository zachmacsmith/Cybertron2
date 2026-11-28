"""Gear as goods with two lives (u3_making.md §2, §3; u2_taking.md §2; basis.md §6 "A piece of gear"; D2-276, D2-288, D2-309,
D2-310, D2-312, D2-329): the feature unit of made gear (D2-244), its data, its acts' helpers, its night and its words together.

- **data:** `ITEMS` (the wave's made things and materials in real kilograms, basis §2), `RECIPES` (each piece's inputs in the handling
  units, its real hours and clock, its class; u3 §2.2), `LIVES` (each thing's count of use, its real uses, its rot wet and dry in
  world years; u3 §3.3). `register` writes them into the engine's ITEMS and TECHNIQUES at load, as wild/methods.py does.
- **the record:** a container keeps `pieces` = {item: [piece]} for every pieced item it holds, one piece a whole unit of the good;
  a piece is {"life": uses left, "rot": share of its rot life used, "of": what it was made of, "barked": None, "torn": False}
  (one record for made gear (u3) and placed gear (u2): basis §6). The primitives that move goods move pieces with them
  (`on_create`, `on_transfer`, `on_destroy`), the most worn first out; a container that holds a pieced good with no pieces
  (a seeded world) holds it at full life. A set thing (u2 §2) keeps its laid gear apart from its catch, in `set.gear` and
  `set.pieces`, moved by the `lay` and `unlay` primitives.
- **lives (D2-310):** a life counted in nights (set gear) at the calendar's 32/365; in acts (tools, rods, lines) at the world's
  capital factor; things used up (snares) at their real rate; rot by time and condition, real years as world years (D2-276), wet in
  the water and dry elsewhere. At 0 uses a piece is broken: it stays, unusable, until mended or rotten; at rot 1 it is gone.
  Nets: about 16 nights in the water until barking returns with tanning (D2-329).
- **mending (u3 §3.4):** half the full uses back, never above full, never any rot; a tenth of the piece's materials each; a fifth of
  the making's units for the lot, at the floor of 1.
- **process:** `rot_night(w)`, once a night after the wild (night.py).
- **words:** `held_words` (one's own gear and its state), `life_words` (what a made piece is good for).

The tools of the older engine (crude and copper tools, the crude weapon, the plough, the harness, bedrolls, tents) keep their wear
map (D2-46) with their lives converted by `life_of` (D2-310); they are not pieced in this stage.
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------------------------------------------------- data
# Goods and gear of the wave (basis §2; u3 §2.2, §2.3, §10): weight in kg a unit; keeping in real days (D2-289's curve), where it
# keeps less than for ever. `carry`: kg more one carries (basis §5: a creel +5). Packs: the water's gear with the water pack, snares
# with the wild pack's snaring; materials everywhere.
ITEMS = {
    "cord": {"weight": 1, "keep": 2000, "note": "cord, twine or light line, by the kg (basis §2)"},
    "flax": {"weight": 1, "keep": 365, "note": "pulled flax straw, by the kg (u3 §1.2)"},
    "retted flax": {"weight": 1, "keep": 365},
    "flax seed": {"weight": 1, "keep": 2500},
    "bone": {"weight": 1},
    "wicker trap": {"weight": 2.5, "seen": True, "pack": "water"},
    "creel": {"weight": 1, "seen": True, "carry": 5, "pack": "water"},
    "basket": {"weight": 1.5, "seen": True},
    "keep box": {"weight": 8, "pack": "water"},
    "hurdle": {"weight": 10},
    "hand line": {"weight": 0.05, "seen": True, "pack": "water"},
    "set line": {"weight": 0.5, "seen": True, "pack": "water"},
    "bone hook": {"weight": 0.005, "pack": "water"},
    "copper hook": {"weight": 0.005, "pack": "water"},
    "snare": {"weight": 0.008, "seen": True, "pack": "wild"},
    "gill net": {"weight": 4, "seen": True, "pack": "water"},
    "dip net": {"weight": 1, "seen": True, "pack": "water"},
    "sack": {"weight": 0.6},
    "salting tub": {"weight": 30},
    "barrel": {"weight": 25},
}

# The recipes (u3 §2.2): each piece's inputs in the handling units (withies a 10 kg bundle, timber a 25 kg load, cord a kg), its
# real hours a piece and its clock (capital: at the world's factor; day: real hours, things used up in a few uses, D2-276), its class
# (simple: everyone knows it; practised, skilled: a craft learned), where it is made. Leather, the frame and the fowling net wait
# (D2-327, D2-318); the spear with the hunting build-out.
RECIPES = {
    "wicker trap": {"label": "making wicker traps", "aliases": ["wicker traps", "make traps", "make wicker traps", "weave traps", "traps"],
                    "inputs": {"withies": 0.45}, "hours": 6, "class": "practised", "pack": "water", "tags": ["fishing", "craft"]},
    "creel": {"label": "making a creel", "hint": "a fish basket on the back", "aliases": ["creels"], "inputs": {"withies": 0.25}, "hours": 6,
              "class": "practised", "pack": "water", "tags": ["fishing", "craft"]},
    "basket": {"label": "making a basket", "aliases": ["baskets"], "inputs": {"withies": 0.3}, "hours": 6, "class": "practised",
               "tags": ["craft"]},
    "keep box": {"label": "making a keep box", "hint": "a wicker box to hold fish alive in the water", "aliases": ["keep boxes"],
                 "inputs": {"withies": 1}, "hours": 9, "class": "practised", "pack": "water", "tags": ["fishing", "craft"]},
    "hurdle": {"label": "making hurdles", "hint": "woven wattle panels", "aliases": ["hurdles", "wattle hurdles"], "inputs": {"withies": 1},
               "hours": 2.8, "class": "practised", "tags": ["craft", "building"]},
    "hand line": {"label": "making a hand line", "aliases": ["hand lines", "a line"], "inputs": {"cord": 0.02, "hooks": {"bone hook": 2, "copper hook": 2}},
                  "hours": 1.5, "class": "simple", "pack": "water", "tags": ["fishing", "craft"]},
    "set lines": {"label": "making a set line", "hint": "a line of about 30 hooks", "gives": "set line", "aliases": ["set line", "a set line", "long line"],
                 "inputs": {"cord": 0.3, "hooks": {"bone hook": 30, "copper hook": 30}}, "hours": 9, "class": "simple", "pack": "water",
                 "tags": ["fishing", "craft"]},
    "bone hook": {"label": "making bone hooks", "aliases": ["bone hooks"], "inputs": {"bone": 0.005}, "hours": 0.4, "clock": "day",
                  "class": "simple", "pack": "water", "tags": ["fishing", "craft"]},
    "copper hook": {"label": "making copper hooks", "aliases": ["copper hooks", "hooks"], "inputs": {"copper": 0.005}, "hours": 0.4,
                    "class": "skilled", "trade": "smith", "at": {"fittings": ["anvil"]}, "pack": "water", "tags": ["fishing", "smithing"]},
    "snares": {"label": "making snares", "hint": "a noose and tether of cord", "gives": "snare", "aliases": ["snare", "make snares", "nooses"],
              "inputs": {"cord": 0.005}, "hours": 0.165, "clock": "day", "class": "simple", "pack": "wild", "tags": ["hunting", "craft"]},
    "gill nets": {"label": "making a gill net", "hint": "netting twine, with sinkers", "gives": "gill net", "aliases": ["gill net", "a gill net", "fish net"],
                 "inputs": {"cord": 1, "stone": 0.1}, "hours": 50, "class": "practised", "at": {"building": True}, "pack": "water",
                 "tags": ["fishing", "craft"]},
    "dip net": {"label": "making a dip net", "hint": "a hoop net on a pole", "aliases": ["dip nets", "hoop net", "hand net"],
                "inputs": {"cord": 0.1, "withies": 0.2}, "hours": 3.5, "class": "practised", "pack": "water", "tags": ["fishing", "craft"]},
    "sack": {"label": "making a sack", "hint": "woven of cord", "aliases": ["sacks"], "inputs": {"cord": 0.6}, "hours": 4, "class": "practised",
             "tags": ["craft"]},
    "salting tub": {"label": "making a salting tub", "hint": "a hollowed log or boards, hooped", "aliases": ["salting tubs", "a tub"],
                    "inputs": {"timber": 2, "withies": 0.1}, "hours": 6, "class": "practised", "tags": ["craft", "food"]},
    "barrel": {"label": "making a barrel", "hint": "staves and hoops", "aliases": ["barrels"], "inputs": {"timber": 7, "withies": 0.3},
               "hours": 9.5, "class": "skilled", "trade": "cooper", "tags": ["craft"]},
}

# Lives (u3 §3.3; D2-310, D2-329): `count` how a use is counted (nights set, acts of work, used up by the night, or none: it only
# rots); `uses` real uses (nights or acts), converted by the clock; `rot` (wet, dry) in world years, or None for no rot; `mend` the
# mending's own inputs a piece where they are not a tenth of the making's; `torn` a used-up thing's chance a night set of being lost.
LIVES = {
    "wicker trap": {"count": "nights", "uses": 228, "rot": (2.0, 5.0), "mends": True},           # 20 nights set (real 200 to 300)
    "gill net": {"count": "nights", "uses": 285, "rot": (0.5, 5.0), "mends": True},              # 25 set; about 16 nights in the
                                                                                                 # water until barking (D2-329)
    "set line": {"count": "nights", "uses": 68, "rot": (0.5, 5.0), "mends": True,               # 6 nights set (real 50 to 100)
                 "mend": {"cord": 0.03, "hooks": {"bone hook": 15, "copper hook": 15}}},          # its cord as the nets' (D2-329)
    "hand line": {"count": "acts", "uses": 56, "rot": (None, 2.0), "mends": True, "mend": {"hooks": {"bone hook": 1, "copper hook": 1}}},
    "fishing rod": {"count": "acts", "uses": 210, "rot": (None, 3.0), "mends": False},          # 14 acts at 1/15, remade
    "dip net": {"count": "acts", "uses": 175, "rot": (None, 2.0), "mends": True},
    "snare": {"count": "used", "torn": 1 / 6},                                                 # lost or torn 1 in 6 a night set
    "creel": {"count": None, "rot": (None, 4.0)},
    "basket": {"count": None, "rot": (None, 2.0)},
    "pack": {"count": None, "rot": (None, 2.5)},
    "keep box": {"count": None, "rot": (2.0, 5.0)},
    "hurdle": {"count": None, "rot": (None, 7.0)},
    "sack": {"count": None, "rot": (None, 3.0)},
    "salting tub": {"count": None, "rot": (None, 5.0)},
    "barrel": {"count": None, "rot": (None, 10.0)},
}
# the older engine's tools on their wear map, their lives converted (D2-310): real uses in acts at the capital factor (u3 §3.3: at
# 1/7 a crude tool 40, a copper tool 140, a crude weapon 14, a harness 100; the plough 18 plots at every stage); nights slept at the
# calendar's (a bedroll and a tent 30 nights)
TOOL_LIVES = {"crude tool": ("acts", 280), "copper tool": ("acts", 980), "crude weapon": ("acts", 98), "harness": ("acts", 700),
              "wooden plough": ("fixed", 18), "bedroll": ("nights", 342), "tent": ("nights", 342)}
MEND = {"share": 0.1, "uses": 0.5, "units": 0.2}           # a tenth of the materials, half the uses back, a fifth of the units
PIECED = tuple(k for k, v in LIVES.items() if v.get("count") != "used")     # snares are a count, used up; the rest are pieces
SET_GEAR = {"trap in water": "wicker trap", "gill net": "gill net", "set line": "set line", "snare": "snare"}   # a set method's gear
SET_MOST = {"wicker trap": 6, "snare": 25, "gill net": 1, "set line": 1}       # one setting lays at most (u2 §3; D2-264)


def _keep_spoil(d) -> float:
    n = min(float(d), 2.0) + max(0.0, float(d) - 2.0) / 11.4                    # the keeping curve (D2-289), as data.base_spoil
    return round(1.0 - 0.75 ** (1.0 / n), 4)


def register_items(items) -> None:
    """The wave's goods and gear into the engine's ITEMS (at load)."""
    for k, v in ITEMS.items():
        row = {"weight": v["weight"], "food": 0.0, "spoil": _keep_spoil(v["keep"]) if v.get("keep") else 0.0}
        for f in ("seen", "carry", "pack"):
            if f in v:
                row[f] = v[f]
        items.setdefault(k, row)


def register_techniques(techniques) -> None:
    """The recipes into the engine's TECHNIQUES (at load), and the mending act."""
    for k, r in RECIPES.items():
        row = {"verb": "make", "label": r["label"], "aliases": list(r.get("aliases", [])), "basic": r["class"] == "simple",
               "inputs": dict(r["inputs"]), "units": 1, "gives": {r.get("gives", k): 1}, "tags": list(r.get("tags", ["craft"])),
               "hours": r["hours"], "clock": r.get("clock", "capital"), "class": r["class"]}
        for f in ("pack", "trade", "at", "hint", "requires"):
            if f in r:
                row[f] = r[f]
        techniques[k] = row
    mended = [plural(i) for i, x in sorted(LIVES.items()) if x.get("mends")]      # what mends and what is made again, from LIVES
    remade = [plural(i) for i, x in sorted(LIVES.items()) if x.get("count") and not x.get("mends")]   # the taking gear that wears out
    techniques["mend gear"] = {"verb": "make", "label": "mending gear", "basic": True,                 # and is made again (W-111: rods
                                                                                                       # read as lines, mended)
                               "hint": ", ".join(mended) + ("; " + " and ".join(remade) + " are made again, not mended" if remade else ""),
                               "aliases": ["mend", "mend traps", "mend the traps", "mend nets", "mend the net", "mend the nets", "mend lines"],
                               "mend_gear": True, "units": 1, "gives": "", "inputs": {}, "tags": ["craft", "fishing"],
                               "does": "mend the worn gear in your hands, one kind an act: half its full uses back, a tenth of its "
                                       "materials a piece",
                               "args": [{"key": "item", "is": "the gear to mend (else the most worn in your hands)", "req": False,
                                         "opts": {}, "who": []}]}


def craft_of(item) -> str | None:
    """The making craft of a pieced good (the mending craft too, u3 §3.4)."""
    from cybertron2.engine.data import TECHNIQUES
    return item if item in TECHNIQUES and TECHNIQUES[item].get("gives") == {item: 1} else \
        next((t for t, d in TECHNIQUES.items() if d.get("verb") == "make" and isinstance(d.get("gives"), dict)
              and item in d["gives"]), None)


# ---------------------------------------------------------------------------------------------------------------------- lives
def full_uses(item, w=None) -> float | None:
    """A new piece's uses in the engine (D2-310): nights at the calendar's 32/365, acts at the world's capital factor."""
    from cybertron2.engine import clocks as CK
    lv = LIVES.get(item) or {}
    if lv.get("count") == "nights":
        return float(CK.night_life(lv["uses"]))
    if lv.get("count") == "acts":
        return float(CK.capital_life(lv["uses"], w))
    return None


def life_of(item, w=None) -> float:
    """The wear-map life of an older tool (D2-46), converted (D2-310); the item's own `life` where it has no row here."""
    from cybertron2.engine import clocks as CK
    from cybertron2.engine.data import ITEMS as _I
    kind, n = TOOL_LIVES.get(item, (None, None))
    if kind == "acts":
        return float(CK.capital_life(n, w))
    if kind == "nights":
        return float(CK.night_life(n))
    if kind == "fixed":
        return float(n)
    return float(_I[item]["life"])


def pieced(item) -> bool:
    return item in PIECED


def new_piece(item, w=None, of=None) -> dict:
    u = full_uses(item, w)
    return {"life": u, "rot": 0.0, "of": of, "barked": None, "torn": False}


def _wear_key(p) -> tuple:
    """Most worn first: least life left, then most rot (deterministic)."""
    life = p.get("life")
    return (float(life) if life is not None else 1e9, -float(p.get("rot", 0.0)))


def count(c, item) -> int:
    return int(float((c.get("goods") or {}).get(item, 0.0)) + 1e-6)


def pieces(c, item, w=None) -> list:
    """The pieces a container holds of a pieced good, as many as its whole units: those it keeps, the rest at full life (a seeded
    world's gear). A read: nothing is written."""
    have = list(((c.get("pieces") or {}).get(item)) or [])
    n = count(c, item)
    if len(have) < n:
        have += [new_piece(item, w) for _ in range(n - len(have))]
    return sorted(have, key=_wear_key)[len(have) - n:] if len(have) > n else have


def sound(p) -> bool:
    return p.get("life") is None or float(p["life"]) > 1e-9


def sound_count(c, item, w=None) -> int:
    """Whole pieces of a good fit to use (a good with no pieces: its count)."""
    if not pieced(item):
        return count(c, item)
    return sum(1 for p in pieces(c, item, w) if sound(p))


def _store(c, item, ps) -> None:
    pc = c.setdefault("pieces", {})
    if ps:
        pc[item] = sorted(ps, key=_wear_key)
    else:
        pc.pop(item, None)
    if not pc:
        c.pop("pieces", None)


# ---------------------------------------------------------------------------------------------------------------------- primitives
def on_create(w, c, item, before, after, given=None) -> None:
    """Goods created in a container (made, or taken up into it): new pieces at full life, or the pieces `given`."""
    if not pieced(item):
        return
    ps = pieces(dict(c, goods={item: before}), item, w)
    add = int(after + 1e-6) - int(before + 1e-6)
    new = list(given or [])[:max(0, add)]
    new += [new_piece(item, w) for _ in range(max(0, add - len(new)))]
    _store(c, item, ps + new)


def on_destroy(w, c, item, before, after) -> list:
    """Goods gone from a container: the most worn pieces go first. Returns the pieces gone."""
    if not pieced(item):
        return []
    ps = sorted(pieces(dict(c, goods={item: before}), item, w), key=_wear_key)
    k = max(0, int(before + 1e-6) - int(after + 1e-6))
    _store(c, item, ps[k:])
    return ps[:k]


def on_transfer(w, src, dst, item, before_src, before_dst, qty, sound_first=False) -> None:
    """Goods moved between containers: their pieces with them, the most worn first (sound ones first when laying gear)."""
    if not pieced(item):
        return
    ps = sorted(pieces(dict(src, goods={item: before_src}), item, w), key=_wear_key)
    k = max(0, int(before_src + 1e-6) - int(before_src - qty + 1e-6))
    if sound_first:
        ps = [p for p in ps if sound(p)] + [p for p in ps if not sound(p)]
    gone, keep = ps[:k], ps[k:]
    _store(src, item, keep)
    on_create(w, dst, item, before_dst, before_dst + qty, given=gone)


def wear(w, c, item, uses) -> bool:
    """A use's wear on a pieced good (the piece in use: the most worn sound one). Returns True if it broke."""
    ps = sorted(pieces(c, item, w), key=_wear_key)
    use = next((p for p in ps if sound(p)), None)
    if use is None or use.get("life") is None:
        return False
    use["life"] = round(max(0.0, float(use["life"]) - float(uses)), 4)
    _store(c, item, ps)
    return use["life"] <= 1e-9


def p_lay(w, src, dst, item, qty):
    """Gear laid from hands into a set thing (u2 §3, fault 12): `qty` sound pieces of `item` (snares a count) leave `src`'s goods for
    the set's `gear` and `pieces`. Returns the number laid."""
    from cybertron2.engine.here import Refused
    s, d = w.s["containers"][src], w.s["containers"][dst]
    n = int(qty)
    if sound_count(s, item, w) < n:
        raise Refused(f"there are only {sound_count(s, item, w)} sound {item} there")
    sp = dict(d.get("set") or {})
    gear = dict(sp.get("gear") or {})
    pcs = {k: list(v) for k, v in (sp.get("pieces") or {}).items()}
    if pieced(item):
        ps = sorted(pieces(s, item, w), key=_wear_key)
        good = [p for p in ps if sound(p)]
        laid, rest = good[:n], [p for p in ps if p not in good[:n]]
        g = s["goods"]
        g[item] = round(g.get(item, 0.0) - n, 6)
        _store(s, item, rest)
        pcs[item] = pcs.get(item, []) + [dict(p, torn=False) for p in laid]
    else:
        s["goods"][item] = round(s["goods"].get(item, 0.0) - n, 6)
    gear[item] = int(gear.get(item, 0)) + n
    sp["gear"], sp["pieces"] = gear, pcs
    d["set"] = sp
    return n


def p_unlay(w, src, dst, item, qty, broken=False):
    """Gear taken up from a set thing into a container (u2 §3: `up`; broken pieces brought home to mend). `broken`: the broken
    pieces only; else sound ones first. Returns the number taken up."""
    s, d = w.s["containers"][src], w.s["containers"][dst]
    sp = dict(s.get("set") or {})
    gear = dict(sp.get("gear") or {})
    pcs = {k: list(v) for k, v in (sp.get("pieces") or {}).items()}
    n = min(int(qty), int(gear.get(item, 0)))
    if n <= 0:
        return 0
    before = float(d["goods"].get(item, 0.0))
    if pieced(item):
        ps = sorted(pcs.get(item, []), key=_wear_key)
        pick = [p for p in ps if not sound(p)] if broken else [p for p in ps if sound(p)] + [p for p in ps if not sound(p)]
        took = pick[:n]
        n = len(took)
        left = list(ps)
        for p in took:
            left.remove(p)
        pcs[item] = left
        if not left:
            pcs.pop(item, None)
        d["goods"][item] = round(before + n, 6)
        on_create(w, d, item, before, before + n, given=[{k: v for k, v in p.items() if k != "torn"} | {"torn": False} for p in took])
    else:
        d["goods"][item] = round(before + n, 6)
    gear[item] = int(gear.get(item, 0)) - n
    if gear[item] <= 0:
        gear.pop(item)
    sp["gear"], sp["pieces"] = gear, pcs
    s["set"] = sp
    return n


def p_gear_night(w, cid, field, value):
    """A set thing's laid gear changed by the night (worn, torn, rotted): `field` "pieces" or "gear" of its `set`."""
    c = w.s["containers"][cid]
    sp = dict(c.get("set") or {})
    sp[field] = value
    c["set"] = sp
    return value


# ---------------------------------------------------------------------------------------------------------------------- set gear
def laid(c) -> dict:
    """{item: n} of gear laid in a set thing."""
    return dict(((c.get("set") or {}).get("gear")) or {})


def laid_pieces(c, item) -> list:
    return list((((c.get("set") or {}).get("pieces")) or {}).get(item) or [])


def fishing(c) -> int:
    """The sound pieces of a set thing still at work (its `line`): sound pieces of its gear; a set with no gear record (an older
    world's, or a weir's traps) its own line."""
    sp = c.get("set") or {}
    if "gear" not in sp:
        return int(sp.get("line", 1))
    out = 0
    for item, n in sp["gear"].items():
        out += sum(1 for p in laid_pieces(c, item) if sound(p)) if pieced(item) else int(n)
    return out


def worn_night(w, cid) -> dict:
    """A night set (u3 §3.2): each sound piece of a set thing's gear takes a use; a used-up thing (snares) is torn at its rate.
    Returns {"broken": n, "torn": n}."""
    c = w.s["containers"][cid]
    sp = c.get("set") or {}
    out = {"broken": 0, "torn": 0}
    node = c["node"]
    for item, n in sorted((sp.get("gear") or {}).items()):
        lv = LIVES.get(item) or {}
        if pieced(item) and lv.get("count") == "nights":
            ps = []
            for p in laid_pieces(c, item):
                if sound(p) and p.get("life") is not None:
                    p = dict(p, life=round(max(0.0, float(p["life"]) - 1.0), 4))
                    out["broken"] += 1 if float(p["life"]) <= 1e-9 else 0
                ps.append(p)
            w.apply("gear_night", node, cid=cid, field="pieces", value={**(sp.get("pieces") or {}), item: ps})
            sp = w.s["containers"][cid]["set"]
        elif lv.get("count") == "used":
            rng = w.rng("gear-torn", w.d, cid, item)
            k = sum(1 for _ in range(int(n)) if rng.random() < float(lv["torn"]))
            if k:
                gear = dict(sp.get("gear") or {})
                gear[item] = int(gear[item]) - k
                if gear[item] <= 0:
                    gear.pop(item)
                w.apply("gear_night", node, cid=cid, field="gear", value=gear)
                sp = w.s["containers"][cid]["set"]
                out["torn"] += k
    return out


def tear(w, cid, share_or_rng, why) -> int:
    """Pieces of a set thing torn away (a spate, a flood, the thaw's ice): each piece at the given chance, drawn by its own key;
    `share_or_rng` is (chance, rng). Returns the pieces lost."""
    chance, rng = share_or_rng
    c = w.s["containers"][cid]
    sp = c.get("set") or {}
    node = c["node"]
    lost = 0
    gear = dict(sp.get("gear") or {})
    pcs = {k: list(v) for k, v in (sp.get("pieces") or {}).items()}
    for item in sorted(gear):
        if pieced(item):
            keep = []
            for p in pcs.get(item, []):
                if rng.random() < chance:
                    lost += 1
                else:
                    keep.append(p)
            pcs[item] = keep
            gear[item] = len(keep)
        else:
            k = sum(1 for _ in range(int(gear[item])) if rng.random() < chance)
            gear[item] = int(gear[item]) - k
            lost += k
        if gear[item] <= 0:
            gear.pop(item)
            pcs.pop(item, None)
    if lost:
        w.apply("gear_night", node, cid=cid, field="pieces", value=pcs)
        w.apply("gear_night", node, cid=cid, field="gear", value=gear)
        note = dict(w.s["containers"][cid]["set"].get("lost") or {})
        note[why] = int(note.get(why, 0)) + lost
        w.apply("gear_night", node, cid=cid, field="lost", value=note)
    return lost


# ---------------------------------------------------------------------------------------------------------------------- the night
def rot_night(w) -> dict:
    """Rot, the second life (u3 §3.2; D2-276: real years as world years): each piece's `rot` rises by 1 / (its rot years x the year's
    days), at the wet rate while it is set in water and the dry rate elsewhere; at 1 it is gone. Returns {cid: {item: n gone}}."""
    from cybertron2.engine.data import COVERS  # noqa: F401  (the covers a set thing lies in)
    Y = float(w.year_days())
    out = {}
    for cid in sorted(w.s["containers"]):
        c = w.s["containers"][cid]
        place = None
        if c.get("kind") == "set" and (c.get("set") or {}).get("gear"):
            wet = (w.s["parcels"].get(c.get("parcel")) or {}).get("cover") in ("water", "fen", "saltmarsh")
            pcs = {k: list(v) for k, v in ((c["set"].get("pieces")) or {}).items()}
            gone_any = False
            gear = dict(c["set"]["gear"])
            for item in sorted(pcs):
                rate = _rot_rate(item, wet)
                if rate <= 0:
                    continue
                keep = []
                for p in pcs[item]:
                    p = dict(p, rot=round(float(p.get("rot", 0.0)) + rate / Y, 6))
                    if p["rot"] >= 1.0 - 1e-9:
                        gone_any = True
                        out.setdefault(cid, {})[item] = out.get(cid, {}).get(item, 0) + 1
                    else:
                        keep.append(p)
                pcs[item] = keep
                gear[item] = len(keep)
                if not keep:
                    gear.pop(item, None)
                    pcs.pop(item, None)
            place = c["node"]
            w.apply("gear_night", place, cid=cid, field="pieces", value=pcs)
            if gone_any:
                w.apply("gear_night", place, cid=cid, field="gear", value=gear)
                note = dict(w.s["containers"][cid]["set"].get("lost") or {})
                note["rotted"] = int(note.get("rotted", 0)) + sum(out[cid].values())
                w.apply("gear_night", place, cid=cid, field="lost", value=note)
            continue
        held = [i for i in sorted(c.get("goods") or {}) if pieced(i) and count(c, i) > 0]
        if not held:
            continue
        place = w.place_of(("container", cid))
        if place is None:
            continue
        w.apply("rot", place, container=cid, nights=1.0)
        for item, n in (getattr(w, "_rot_gone", {}) or {}).items():
            out.setdefault(cid, {})[item] = n
    return out


def _rot_rate(item, wet) -> float:
    r = (LIVES.get(item) or {}).get("rot")
    if not r:
        return 0.0
    yrs = r[0] if wet else r[1]
    if yrs is None:
        yrs = r[1]
    return 1.0 / float(yrs) if yrs else 0.0


def p_rot(w, container, nights=1.0):
    """A night's dry rot on the pieced goods a container holds (hands, a store, a pile); a piece rotted through is gone."""
    c = w.s["containers"][container]
    Y = float(w.year_days())
    gone = {}
    for item in sorted(c.get("goods") or {}):
        if not pieced(item) or count(c, item) <= 0:
            continue
        rate = _rot_rate(item, False)
        if rate <= 0:
            continue
        ps = pieces(c, item, w)
        keep = []
        for p in ps:
            p = dict(p, rot=round(float(p.get("rot", 0.0)) + rate * float(nights) / Y, 6))
            if p["rot"] >= 1.0 - 1e-9:
                gone[item] = gone.get(item, 0) + 1
            else:
                keep.append(p)
        if gone.get(item):
            c["goods"][item] = round(float(c["goods"][item]) - gone[item], 6)
        _store(c, item, keep)
    w._rot_gone = gone
    return gone


# ---------------------------------------------------------------------------------------------------------------------- mending
def mend_cost(item) -> dict:
    """The mending's materials a piece: the row's own `mend`, else a tenth of the making's inputs (u3 §3.4)."""
    from cybertron2.engine.data import TECHNIQUES
    lv = LIVES.get(item) or {}
    if lv.get("mend"):
        return dict(lv["mend"])
    t = TECHNIQUES.get(craft_of(item) or "") or {}
    out = {}
    for i, q in (t.get("inputs") or {}).items():
        out[i] = {a: round(float(b) * MEND["share"], 4) for a, b in q.items()} if isinstance(q, dict) else round(float(q) * MEND["share"], 4)
    return out


def mend_units(item, w=None) -> int:
    """A fifth of the making's units for the lot, at the floor of 1 (u3 §3.4)."""
    from cybertron2.engine import clocks as CK
    from cybertron2.engine.data import CAPITAL, TECHNIQUES
    t = TECHNIQUES.get(craft_of(item) or "") or {}
    u = CK.piece_units(t, w) if t.get("hours") else float(t.get("units", 1))
    return max(int(CAPITAL["floor"]), int(math.ceil(u * MEND["units"] - 1e-9)))


def mended(p, item, w=None) -> dict:
    """A piece mended: half its full uses back, never above full, never any rot back."""
    full = full_uses(item, w)
    if full is None or p.get("life") is None:
        return dict(p)
    return dict(p, life=round(min(full, float(p["life"]) + full * MEND["uses"]), 4))


def p_mend(w, container, item, n):
    """`n` pieces of `item` in a container mended, the most worn first (u3 §3.4). Returns their lives after."""
    c = w.s["containers"][container]
    ps = sorted(pieces(c, item, w), key=_wear_key)
    full = full_uses(item, w) or 0.0
    out = []
    k = 0
    for i, p in enumerate(ps):
        if k < int(n) and p.get("life") is not None and float(p["life"]) < full - 1e-9:
            ps[i] = mended(p, item, w)
            out.append(ps[i]["life"])
            k += 1
    _store(c, item, ps)
    return out


# ---------------------------------------------------------------------------------------------------------------------- words
def life_words(item, w=None) -> str:
    """What a new piece is good for (u3 §3.5): 'good for about 20 nights set before it wants mending'."""
    lv = LIVES.get(item) or {}
    u = full_uses(item, w)
    if lv.get("count") == "nights":
        return f"good for about {int(u)} nights set before it wants mending" if lv.get("mends") else f"good for about {int(u)} nights set"
    if lv.get("count") == "acts":
        return f"good for about {int(u)} days' use" + (" before it wants mending" if lv.get("mends") else "")
    return ""


def state_words(ps, item, w=None) -> str:
    """'2 broken, wanting mending; the rest good for about 8 more nights set' (u3 §3.5), '' for a good with no uses."""
    lv = LIVES.get(item) or {}
    if lv.get("count") not in ("nights", "acts") or not ps:
        return ""
    broken = sum(1 for p in ps if not sound(p))
    good = [float(p["life"]) for p in ps if sound(p) and p.get("life") is not None]
    unit = "nights set" if lv["count"] == "nights" else "days' use"
    bits = []
    if broken:
        bits.append(f"{broken} broken, wanting mending")
    if good:
        least = int(min(good))
        bits.append(("the rest " if broken else "") + f"good for about {least} more {unit}" if least < (full_uses(item, w) or 0) - 1e-9
                    else ("the rest " if broken else "") + "new")
    rot = max((float(p.get("rot", 0.0)) for p in ps), default=0.0)
    if rot >= 0.75:
        bits.append("rotting" if item in ("gill net", "set line") else "old and rotting")
    return "; ".join(bits)


def held_words(w, cid) -> list:
    """One's pieced gear and its state, for one's own things: ['6 wicker traps: 2 broken, wanting mending; ...']."""
    c = w.s["containers"][cid]
    out = []
    for item in sorted(c.get("goods") or {}):
        if pieced(item) and count(c, item) > 0:
            sw = state_words(pieces(c, item, w), item, w)
            if sw and ("broken" in sw or "more" in sw or "rotting" in sw):
                out.append(f"{count(c, item)} {item if count(c, item) == 1 else plural(item)}: {sw}")
    return out


def plural(item) -> str:
    return {"gill net": "gill nets", "dip net": "dip nets", "set line": "set lines", "hand line": "hand lines", "keep box": "keep boxes",
            "salting tub": "salting tubs", "fishing rod": "fishing rods", "bone hook": "bone hooks", "copper hook": "copper hooks",
            "wicker trap": "wicker traps", "snare": "snares"}.get(item, item + "s")


def named(item, n) -> str:
    return f"{'a' if n == 1 else n} {item if n == 1 else plural(item)}" if n == 1 else f"{n} {plural(item)}"
