"""Processing containers (u4; D2-271, D2-284, D2-291, D2-295; the build's stage 3, W-99): lots that become the next good over nights.

Every way of keeping a glut or working a material has one shape: goods go into a container, wait some nights while a condition holds,
fail a night when it does not, and come out as a different good. This module is that shape as one feature unit (D2-244, the cut into
packages kept in mind: feature_packages.md §9.1, §10):

  - data: PROCESSES (the rows, u4 §2), the techniques that load them (`TECHNIQUES`), the fittings' fields (`FITTINGS`: `process`,
    `holds_kg`), the goods waiting in them (`ITEMS`); each registered into the engine's tables at load (data.py), as gear.py's are;
  - verbs: loading is the `make` act (verbs._make calls `load`); `tend` keeps a container's fire (basis §6: one act on a placed thing,
    with set gear); `move` with `from` a container takes a done lot down (`take_down`);
  - signs: none of its own here (the smokehouse's rows in signs.py read `lots` and the fire's record);
  - processes: `night` (each container's condition tonight, the fire's fuel and its chance of catching) before the night's spoiling,
    and `finish` (a lot that has had its nights becomes its output, in its container) after it; `decay` is the spoiling of a lot's
    goods, read by night.decay_rate;
  - what the household knows: `house_lines` (u4 §7) and the book's states (`states`, u6 §3).

A **process** is a row of PROCESSES; a **container** is a fitting with `process` and `holds_kg` (smoke racks, a hearth's or a fire
ring's rack), or ground of a cover (retting); a **lot** is one loading: a thing (kind `pile`) inside the container's building (`in`),
at its door (`door`, a fire ring outside), or on a parcel (retting), with its record in `lot`:

    {"process", "item" (what went in), "wait" (the good while it waits), "into" (the good it becomes), "ratio", "by", "household",
     "day", "kg" (loaded: counts against the room), "nights", "had" (nights counted), "out" (the last night failed), "done" (the night
     it was done), "got" (kg of its output then)}

A done lot stays in its container (u4 Departure 6, default taken Q-U4-2) until it is taken down by an act or a rule; it counts against
the room by the share of its output still on it. Salting and the hot smoke make no lot: they turn the goods at once (u4 §2 notes).
"""
from __future__ import annotations

import math

# ---------------------------------------------------------------------------------------------------------------------- data
# The rows (u4 §2; basis.md §1, §3; D2-271, D2-283, D2-284, D2-291, D2-295). `in`: input good -> (waiting good, output good, ratio);
# `nights` whole nights (D2-273); `fuel` bundles of firewood a kg loaded, burned evenly over the lot's nights (u4 Departure 11);
# `load` kg a unit of the act that loads it (hanging 30 a unit, a salted lot 60, a hearth's rack 8; D2-263's "up to"); `fire`: the
# condition is a tended fire burning its fuel; `cond` otherwise (the hearth lit inside, a dry night outside; water without a spate;
# none); `in_rate` the share lost a night while the condition holds (0.03 in the smoke or at the hearth, wave1 §2.2, est.; None: the
# waiting good's own base, for a salted lot whose base is lower); `structures` the buildings whose smoke it takes (D2-271).
PROCESSES = {
    "keeping smoke": {"label": "a keeping smoke", "in": {"fish": ("smoking fish", "smoked fish", 0.5), "meat": ("smoking meat", "smoked meat", 0.5)},
                      "nights": 1, "fuel": 0.15, "load": 30, "fire": True, "in_rate": 0.03, "fittings": ["smoke racks"],
                      "word": "smoked", "lot": True},
    "hard cure": {"label": "a hard cure", "in": {"salt fish": ("salt fish", "hard-cured fish", 0.4), "salt meat": ("salt meat", "hard-cured meat", 0.85)},
                  "nights": 3, "fuel": 0.25, "load": 60, "fire": True, "in_rate": None, "fittings": ["smoke racks"],
                  "structures": ["timber", "stone"], "word": "hard-cured", "lot": True},
    "hearth rack": {"label": "drying at the fire", "in": {"fish": ("drying fish", "dried fish", 0.5), "meat": ("drying meat", "dried meat", 0.5)},
                    "nights": 1, "load": 8, "fire": False, "cond": "hearth", "in_rate": 0.03, "fittings": ["hearth", "fire ring"],
                    "word": "dry", "lot": True},
    "retting": {"label": "retting", "in": {"flax": ("retting flax", "retted flax", 0.8)}, "nights": {"water": 1, "dew": 3}, "load": 50,
                "fire": False, "cond": "ground", "in_rate": 0.0, "covers": {"water": "water", "fen": "water", "meadow": "dew", "pasture": "dew"},
                "wash": 0.5, "word": "retted", "lot": True},
    # no lot: at once (u4 §2 notes; Departure 7)
    "salting": {"label": "salting", "in": {"fish": (None, "salt fish", 1.0), "meat": (None, "salt meat", 1.0)}, "nights": 0, "load": 40,
                "salt": {"fish": 0.25, "meat": 0.125}, "container": "salting tub", "lot": False},
    "hot smoke": {"label": "a hot smoke", "in": {"fish": (None, "hot-smoked fish", 0.67), "meat": (None, "hot-smoked meat", 0.67)},
                  "nights": 0, "fuel": 0.15, "load": 10, "lot": False},
}
WORK = {"take down": 120.0}                 # kg a unit taking a done lot down (u4 Basis rows needed, 4; est.)
WORK_FLOOR = {"hut": 1, "other": 2}         # floor a smokehouse keeps free to work and keep the fire (u4 §4; Basis rows needed, 8)
FIRE_HEAT = 0.5                             # a bundle of firewood's heat (data ITEMS firewood): fuel in bundles is heat x 2

# The goods while they wait (u4 §3): an in-process good keeps its input's food; its base off the fire is its input's (fresh fish
# 0.175, meat 0.129: data.py sets it from the curve) and in the smoke the row's `in_rate`
ITEMS = {
    "retting flax": {"weight": 1, "food": 0.0, "spoil": 0.0},
}

# The acts that load the containers, and the hot smoke (u4 §6; D2-263's recipes shown at capable and known: `manual` from the rows)
_KS = ("hung on the smoke racks for a keeping smoke: done after 1 night of a tended fire, half the weight, keeping about a season; "
       "up to 30 kg a unit, as the racks have room; the fire wants about 0.15 bundles of firewood a kg hung, from the smokehouse's store "
       "or the woodpile at its door, and tending once a day; a lot that misses its fire that night keeps as fresh and waits")
_HC = ("salted goods hung for a hard cure in a timber or stone smokehouse: done after 3 nights of a tended fire, keeping most of a "
       "year out of brine and light to carry; up to 60 kg a unit; about 0.25 bundles of firewood a kg over its nights")
TECHNIQUES = {
    "smoke fish": {"pack": "water", "verb": "make", "label": "hanging fish for a keeping smoke in a smokehouse",
                   "aliases": ["smoking fish", "smoke the fish", "cure fish", "hang fish", "hang fish to smoke", "keeping smoke"],
                   "basic": True, "at": {"fittings": ["smoke racks"]}, "inputs": {"fish": 30}, "units": 1, "gives": {"smoking fish": 30},
                   "batch": True, "process": "keeping smoke", "tags": ["food", "cooking", "fishing"], "manual": _KS},
    "smoke meat": {"verb": "make", "label": "hanging meat for a keeping smoke in a smokehouse", "aliases": ["smoking meat", "smoke the meat",
                   "hang meat to smoke"], "basic": True, "at": {"fittings": ["smoke racks"]}, "inputs": {"meat": 30}, "units": 1,
                   "gives": {"smoking meat": 30}, "batch": True, "process": "keeping smoke", "tags": ["food", "cooking"], "manual": _KS},
    "hard cure fish": {"pack": "water", "verb": "make", "label": "hanging salt fish for a hard cure in a timber or stone smokehouse",
                       "aliases": ["hard cure", "hard-cure fish", "hang salt fish", "hard cure the fish", "hard cure salt fish"],
                       "basic": True, "at": {"fittings": ["smoke racks"]}, "inputs": {"salt fish": 60}, "units": 1,
                       "gives": {"salt fish": 60}, "batch": True, "process": "hard cure", "tags": ["food", "cooking", "fishing"],
                       "manual": _HC},
    "hard cure meat": {"verb": "make", "label": "hanging salt meat for a hard cure in a timber or stone smokehouse", "world": "bacon, ham",
                       "aliases": ["hard-cure meat", "hang salt meat", "cure bacon", "make bacon", "hard cure salt meat"], "basic": True,
                       "at": {"fittings": ["smoke racks"]}, "inputs": {"salt meat": 60}, "units": 1, "gives": {"salt meat": 60},
                       "batch": True, "process": "hard cure", "tags": ["food", "cooking"], "manual": _HC},
    "hot smoke fish": {"pack": "water", "verb": "make", "label": "hot-smoking fish over a fire", "hint": "cooked, to eat cold or carry",
                       "aliases": ["hot smoke", "hot-smoke fish", "hot smoking"], "basic": True,
                       "at": {"fittings": ["hearth", "fire ring"]}, "inputs": {"fish": 10, "firewood": 0.15}, "units": 1,
                       "gives": {"hot-smoked fish": 6.7}, "batch": True, "process": "hot smoke", "tags": ["food", "cooking", "fishing"],
                       "manual": "fish hot-smoked over a fire in one go: 10 kg a unit gives 6.7 kg, cooked, eaten cold, keeping about a week; "
                                 "about 1.5 bundles of firewood for 10 kg"},
    "hot smoke meat": {"verb": "make", "label": "hot-smoking meat over a fire", "hint": "cooked, to eat cold or carry",
                       "aliases": ["hot-smoke meat"], "basic": True, "at": {"fittings": ["hearth", "fire ring"]},
                       "inputs": {"meat": 10, "firewood": 0.15}, "units": 1, "gives": {"hot-smoked meat": 6.7}, "batch": True,
                       "process": "hot smoke", "tags": ["food", "cooking"],
                       "manual": "meat hot-smoked over a fire in one go: 10 kg a unit gives 6.7 kg, cooked, keeping about a week"},
    "dry meat": {"verb": "make", "label": "drying meat over a fire", "aliases": ["drying meat", "cure meat"], "basic": True,
                 "at": {"fittings": ["hearth", "fire ring"]}, "inputs": {"meat": 8}, "units": 1, "gives": {"drying meat": 8}, "batch": True,
                 "process": "hearth rack", "tags": ["food", "cooking"],
                 "manual": "hung on the rack at a hearth or a fire ring: up to 8 kg a unit, dry after a night of the hearth's fire (outside, a "
                           "dry night), half the weight, keeping a year and more kept dry"},
    "dry fish": {"pack": "water", "verb": "make", "label": "drying fish over a fire", "aliases": ["drying fish", "dry the fish", "hang fish to dry"],
                 "basic": True, "at": {"fittings": ["hearth", "fire ring"]}, "inputs": {"fish": 8}, "units": 1, "gives": {"drying fish": 8},
                 "batch": True, "process": "hearth rack", "tags": ["food", "cooking", "fishing"],
                 "manual": "hung on the rack at a hearth or a fire ring: up to 8 kg a unit, dry after a night of the hearth's fire (outside, a "
                           "dry night), half the weight, keeping a year and more kept dry"},
    "tend the smoke": {"verb": "work", "label": "tending a smokehouse fire", "hint": "feeding and banking it for the night",
                       "aliases": ["tend the smokehouse", "tend smokehouse", "tend the fire", "bank the fire", "tend smoke"], "basic": True,
                       "at": {"fittings": ["smoke racks"]}, "yield": {"kind": "smoke_tend"}, "units": 1, "gives": "", "tags": ["food", "fuel"]},
    "ret flax": {"verb": "make", "label": "retting flax", "hint": "laid in still water, or spread on the grass", "aliases": ["retting", "ret the flax",
                 "rett flax", "lay flax to ret"], "basic": True, "at": {"covers": ["water", "fen", "meadow", "pasture"]},
                 "inputs": {"flax": 50}, "units": 1, "gives": {"retting flax": 50}, "batch": True, "process": "retting", "tags": ["craft"],
                 "manual": "pulled flax laid in still water for a night, or spread on the grass for 3, until the stems part from the fibre: "
                           "up to 50 kg a unit, 8 kg retted from 10; a spate on the river washes half away; lift it with a take"},
}
# What doing each does, in interface terms (W-109; D2-350): the world's figures (keeping times, firewood a kg) stay in `manual` for
# the old prompt and in the engine's own results ("the fire ... wants about 0.6 bundles of firewood"), never in the interface.
_KS_DOES = ("hang it on the racks of a smokehouse: done after 1 night of a tended fire (tend it daily; it burns firewood from the "
            "smokehouse's store or the woodpile at its door); a lot that misses its fire waits; take the done lot down with move")
_HC_DOES = ("hang salted goods in a timber or stone smokehouse: done after 3 nights of a tended fire; take the done lot down with move")
for _k, _v in {"smoke fish": _KS_DOES, "smoke meat": _KS_DOES, "hard cure fish": _HC_DOES, "hard cure meat": _HC_DOES,
               "hot smoke fish": "smoke it over a fire in one go: done in the act, cooked",
               "hot smoke meat": "smoke it over a fire in one go: done in the act, cooked",
               "dry meat": "hang it on the rack at a hearth or a fire ring: dry after a night of the fire (outside, a dry night), at half "
                           "the weight",
               "dry fish": "hang it on the rack at a hearth or a fire ring: dry after a night of the fire (outside, a dry night), at half "
                           "the weight",
               "ret flax": "lay pulled flax in still water for a night, or spread on the grass for 3, until the stems part from the "
                           "fibre; lift it with a take"}.items():
    TECHNIQUES[_k]["does"] = _v
# the containers (u4 §4; D2-284, D2-291): a set of racks holds 250 kg on 1 space; the building caps the sets (`per`, `work floor`)
FITTINGS = {
    "smoke racks": {"process": ["keeping smoke", "hard cure"], "holds_kg": 250, "spaces": 1, "per": "set", "racks": None,
                    "does": "a smokehouse: a set of racks holds about 250 kg hung over a smouldering fire, tended daily (a keeping smoke a "
                            "night; a hard cure 3 nights in timber or stone)"},
    "hearth": {"process": ["hearth rack"], "holds_kg": 8, "racks": None},
    "fire ring": {"process": ["hearth rack"], "holds_kg": 8, "racks": None},
}


def register_items(items) -> None:
    for k, v in ITEMS.items():
        items.setdefault(k, dict(v))


def register_techniques(techniques) -> None:
    for k, v in TECHNIQUES.items():
        techniques[k] = {kk: (list(vv) if isinstance(vv, list) else dict(vv) if isinstance(vv, dict) else vv) for kk, vv in v.items()}


def register_fittings(fittings) -> None:
    for k, v in FITTINGS.items():
        row = fittings[k]
        for kk, vv in v.items():
            if vv is None:
                row.pop(kk, None)
            else:
                row[kk] = vv


# ---------------------------------------------------------------------------------------------------------------------- reads
def row(proc) -> dict:
    return PROCESSES[proc]


def process_of(tech) -> str | None:
    from cybertron2.engine.data import TECHNIQUES as T
    return (T.get(tech) or {}).get("process")


def nights_of(proc, kind=None) -> int:
    n = PROCESSES[proc]["nights"]
    return int(n[kind] if isinstance(n, dict) else n)


def waiting(item) -> bool:
    """Whether a good is one that only waits in a container (smoking fish, drying meat, retting flax)."""
    return any(x[0] == item for r in PROCESSES.values() for x in r["in"].values())


def lots(w, bid=None, pid=None, done=None) -> dict:
    """The lots in or at a building (or on a parcel), not hidden: {thing id: thing}; `done` True or False to choose."""
    out = {}
    for cid, c in w.s["containers"].items():
        lt = c.get("lot")
        if not lt or c.get("hidden") or c.get("kind") != "pile":
            continue
        if bid is not None and not (c.get("in") == bid or c.get("door") == bid):
            continue
        if pid is not None and (c.get("in") or c.get("door") or c.get("parcel") != pid):
            continue
        if done is not None and bool(lt.get("done") is not None) != done:
            continue
        out[cid] = c
    return dict(sorted(out.items()))


def waiting_kg(c) -> float:
    lt = c["lot"]
    return float(c["goods"].get(lt["wait"], 0.0))


def done_kg(c) -> float:
    lt = c["lot"]
    return float(c["goods"].get(lt["into"], 0.0)) if lt.get("done") is not None else 0.0


def held_kg(c) -> float:
    """What a lot holds of its room: the kg loaded while it waits; once done, that kg in the share of its output still on it."""
    lt = c["lot"]
    if lt.get("done") is None:
        return float(lt["kg"])
    got = float(lt.get("got") or 0.0)
    return float(lt["kg"]) * (min(1.0, done_kg(c) / got) if got > 1e-9 else 0.0)


def capacity(b, proc) -> float:
    """A building's kg of room for a process: its fittings that run it, `holds_kg` each (u4 §4)."""
    from cybertron2.engine.data import FITTINGS as F
    fit = b.get("fittings") or {}
    return sum(float(F[f].get("holds_kg", 0)) * int(fit.get(f) or 0) for f in F if proc in (F[f].get("process") or []))


def room(w, bid, proc) -> float:
    """kg more the containers of a building take for a process: their capacity less what every lot there holds (one set of racks is
    shared by a keeping smoke and a hard cure)."""
    b = w.s["buildings"][bid]
    cap = capacity(b, proc)
    if cap <= 0:
        return 0.0
    from cybertron2.engine.data import FITTINGS as F
    procs = {p for f in F if proc in (F[f].get("process") or []) and (b.get("fittings") or {}).get(f) for p in F[f]["process"]}
    used = sum(held_kg(c) for c in lots(w, bid).values() if c["lot"]["process"] in procs)
    return max(0.0, cap - used)


def is_smokehouse(b) -> bool:
    return bool((b.get("fittings") or {}).get("smoke racks"))


def fuel_cids(w, bid) -> list:
    """Where a smokehouse's fire takes its wood: its store, then the woodpile at its door (as a hearth's, D4-89)."""
    b = w.s["buildings"][bid]
    return [b["stock"]] + [cid for cid, c in sorted(w.s["containers"].items()) if c.get("kind") == "pile" and c.get("door") == bid
                           and not c.get("hidden") and not c.get("lot")]


def fuel_tonight(w, bid) -> float:
    """The heat tonight's fire wants: over the building's lots of a fire row still waiting, kg loaded x the row's fuel / its nights,
    in bundles of firewood at their heat (u4 §4, Departure 11)."""
    out = 0.0
    for c in lots(w, bid, done=False).values():
        r = PROCESSES[c["lot"]["process"]]
        if r.get("fire"):
            out += float(c["lot"]["kg"]) * float(r["fuel"]) / max(1, int(c["lot"]["nights"]))
    return round(out * FIRE_HEAT, 4)


def fuel_have(w, bid) -> float:
    from cybertron2.engine import forests as FO
    return sum(FO.heat_of(w.goods(cid)) for cid in fuel_cids(w, bid))


def bundles(heat) -> float:
    return round(float(heat) / FIRE_HEAT, 1)


def _n(q) -> str:
    from cybertron2.engine.world import show
    return show(round(float(q), 1))


def _nights(n) -> str:
    return f"{n} night{'s' if n != 1 else ''}"


def _left_words(c, day) -> str:
    lt = c["lot"]
    left = max(1, int(lt["nights"]) - int(lt.get("had", 0)))
    return "done tomorrow" if left == 1 else f"{left} nights left"


def what_of(cs) -> str:
    """What waits in some lots, as people say it ('fish', 'fish and meat')."""
    return " and ".join(sorted({c["lot"]["item"] for c in cs})) or "nothing"


# ---------------------------------------------------------------------------------------------------------------------- acts
def refuse_load(here, tech, bid) -> str:
    """Why a building cannot take this loading: '' if it can (the structure a hard cure needs, D2-271; the room)."""
    r = PROCESSES[process_of(tech)]
    b = here.buildings()[bid]
    if r.get("structures") and b.get("structure") not in r["structures"]:
        return (f"a hard cure needs the long cool smoke of a timber or stone smokehouse; the fire in {b['name']} hangs too close and "
                "hot")
    if room(here._w, bid, process_of(tech)) <= 1e-6:
        return full_words(here._w, bid, process_of(tech))
    return ""


def full_words(w, bid, proc) -> str:
    """'the smoke racks in the Smoke Hut are full: 160 kg of fish smoking, done tomorrow; 90 kg smoked, waiting to be taken down'."""
    b = w.s["buildings"][bid]
    on = lots(w, bid)
    wait = [c for c in on.values() if c["lot"].get("done") is None]
    done = [c for c in on.values() if c["lot"].get("done") is not None and done_kg(c) > 1e-6]
    what = "smoke racks" if is_smokehouse(b) else "rack at its fire"
    bits = []
    if wait:
        bits.append(f"{_n(sum(waiting_kg(c) for c in wait))} kg of {what_of(wait)} {'smoking' if is_smokehouse(b) else 'drying'}, "
                    f"{min((_left_words(c, w.d) for c in wait), key=len)}")
    if done:
        bits.append(f"{_n(sum(done_kg(c) for c in done))} kg {PROCESSES[done[0]['lot']['process']]['word']}, waiting to be taken down")
    return f"the {what} in {b['name']} {'are' if what.endswith('s') else 'is'} full" + (": " + "; ".join(bits) if bits else "")


def load(here, tech, bid, gives, site_name) -> tuple:
    """A loading (u4 §6): the goods `gives` (the waiting good, kg) hung as one lot in the building's container; the fire lit for
    tonight for a fire row. Returns (thing id, head, tail): "You hung {head} (n units){tail}"."""
    w = here._w
    proc = process_of(tech)
    r = PROCESSES[proc]
    b = here.buildings()[bid]
    item = next(i for i, x in r["in"].items() if x[0] in gives)
    wait, into, ratio = r["in"][item]
    kg = round(float(gives[wait]), 4)
    inside = bool(r.get("fire")) or bool((b.get("fittings") or {}).get("hearth"))   # a fire ring's rack hangs outside the door
    nights = nights_of(proc)
    dst = here.apply("new_thing", node=here.node, parcel=b["parcel"], kind="pile", by=here.name, **({"in": bid} if inside else {"door": bid}),
                     lot={"process": proc, "item": item, "wait": wait, "into": into, "ratio": ratio, "by": here.name,
                          "household": here.household(), "day": here.day, "kg": kg, "nights": nights, "had": 0, "out": None,
                          "done": None, "got": None})
    if bid not in here.homes_here():                                           # one's own house is known without it (4c §6.4)
        here.remember_thing(dst, "put")
    here.apply("create", dst=dst, item=wait, qty=kg, why=tech)
    left = room(w, bid, proc)
    if r.get("fire"):
        light(here, bid)
        need, have = fuel_tonight(w, bid), fuel_have(w, bid)
        fuel = (f"The fire is lit for tonight and wants about {_n(bundles(need))} bundles of firewood ({_n(bundles(have))} there)."
                if have + 1e-9 >= need else
                f"The fire is lit for tonight, but {'there is no firewood in it or at its door' if have <= 1e-9 else f'only {_n(bundles(have))} bundles of firewood are there of about {_n(bundles(need))} it wants'}: "
                "it will die tonight unless some is brought.")
        head, tail = (f"{_n(kg)} kg of {item} on the smoke racks in {b['name']}",
                      f": {r['label']}, done after {_nights(nights)} of fire. {fuel} The racks have room for {_n(left)} kg more.")
    elif inside:
        head, tail = f"{_n(kg)} kg of {item} on the rack in the smoke of the hearth inside {b['name']}", f", dry after {_nights(nights)} of its fire."
    else:
        head, tail = f"{_n(kg)} kg of {item} on a rack by the fire outside {b['name']}", f", dry after {_nights(nights)} if it stays dry."
    return dst, head, tail


def lay_ground(here, tech, pid, gives) -> str:
    """Retting (u4 §2; u3 §1.2): a lot laid on a parcel, in its water (a night) or on its grass (3 nights)."""
    proc = process_of(tech)
    r = PROCESSES[proc]
    par = here.parcels()[pid]
    kind = r["covers"].get(par["cover"])
    item = next(i for i, x in r["in"].items() if x[0] in gives)
    wait, into, ratio = r["in"][item]
    kg = round(float(gives[wait]), 4)
    nights = nights_of(proc, kind)
    dst = here.apply("new_thing", node=here.node, parcel=pid, kind="pile", by=here.name,
                     lot={"process": proc, "item": item, "wait": wait, "into": into, "ratio": ratio, "by": here.name, "ground": kind,
                          "household": here.household(), "day": here.day, "kg": kg, "nights": nights, "had": 0, "out": None,
                          "done": None, "got": None})
    here.remember_thing(dst, "put")
    here.apply("create", dst=dst, item=wait, qty=kg, why=tech)
    how = "laid in the water of" if kind == "water" else "spread on the grass of"
    return (f"You {how} {par['name']} {_n(kg)} kg of {item} to ret: done after {_nights(nights)}; lift it then with a take "
            f"(about {_n(kg * ratio)} kg of {into}).")


def light(here, bid) -> None:
    """Loading a fire row or tending its fire: it burns tonight."""
    b = here.buildings()[bid]
    here.apply("set", ref=("building", bid), field="smoke", value={**(b.get("smoke") or {}), "tended": here.day, "by": here.name})


def tend(here, bid) -> str:
    """Keeping a container's fire (`tend` on a smokehouse; `work tend the smoke`): fed and banked for tonight. One who carries fuel
    and finds too little there for tonight puts what is short in from their hands (u4 §6)."""
    from cybertron2.engine import forests as FO
    from cybertron2.engine.world import Refused
    w = here._w
    b = here.buildings()[bid]
    wait = [c for c in lots(w, bid, done=False).values() if PROCESSES[c["lot"]["process"]].get("fire")]
    if not wait:
        if lots(w, bid):
            raise Refused(f"nothing is smoking in {b['name']}: what hangs there is done, and needs no fire")
        raise Refused(f"nothing is hanging in the smoke in {b['name']}: hang a lot first (make smoke fish, or smoke meat)")
    if (b.get("smoke") or {}).get("tended") == here.day:
        raise Refused(f"the fire in {b['name']} is already tended for tonight")
    need, fed = fuel_tonight(w, bid), ""
    short = need - fuel_have(w, bid)
    if short > 1e-9:
        for item in FO.fuel_order():
            have = float(here.carried().get(item, 0.0))
            from cybertron2.engine.data import ITEMS as I
            q = round(min(have, short / float(I[item]["heat"])), 4)
            if q > 1e-9:
                here.apply("transfer", src=here.hands, dst=b["stock"], item=item, qty=q)
                fed += f"; you put {_n(q)} {item} from your hands on it"
                short -= q * float(I[item]["heat"])
                if short <= 1e-9:
                    break
    light(here, bid)
    have = fuel_have(w, bid)
    fuel = (f"firewood there for tonight ({_n(bundles(need))} bundles of {_n(bundles(have))})" if have + 1e-9 >= need else
            f"but not enough firewood there for tonight ({_n(bundles(need))} bundles needed, {_n(bundles(have))} there): the fire will "
            "die unless some is brought")
    return (f"You tended the fire in {b['name']} and banked it for the night{fed}: {_n(sum(waiting_kg(c) for c in wait))} kg of "
            f"{what_of(wait)} smoking, {min((_left_words(c, here.day) for c in wait), key=len)}; {fuel}.")


def take_down(here, bid, item=None, qty=None, to=None, units=None) -> tuple:
    """Taking a done lot down (u4 §6): its output from the container into the building's store (or one's hands, or another of one's
    household's buildings here), at 120 kg a unit. Only one's household's lots, unless named (Q-80: then it is taking).
    Returns (kg taken down, words). `units`: at most so much work (a chore's spare), else all."""
    from cybertron2.engine.world import Refused
    w = here._w
    b = here.buildings()[bid]
    mine = here.household()
    on = [(cid, c) for cid, c in lots(w, bid, done=True).items() if done_kg(c) > 1e-6 and (item is None or c["lot"]["into"] == item)]
    if not on:
        raise Refused(f"nothing done hangs in {b['name']} to take down" + (f" ({item})" if item else ""))
    own = [(cid, c) for cid, c in on if c["lot"].get("household") == mine or c["lot"].get("by") == here.name]
    if not own:
        c = on[0][1]
        who = c["lot"].get("by")
        raise Refused(f"the {c['lot']['into']} on the racks in {b['name']} is {who}'s" + (f", of {c['lot']['household']}" if c["lot"].get("household") else "")
                      + ": take it by name (take) if you mean to")
    if to is None:
        dst = b["stock"]
        dname = f"into its store"
    elif to == "hands":
        dst, dname = here.hands, "into your hands"
    else:
        dst, dname = here.buildings()[to]["stock"], f"into {here.buildings()[to]['name']}"
    want = float("inf") if qty is None else float(qty)
    cap = float("inf") if units is None else float(units) * WORK["take down"]
    got = 0.0
    for cid, c in own:
        q = round(min(done_kg(c), want - got, cap - got), 6)
        if q <= 1e-9:
            break
        here.apply("transfer", src=cid, dst=dst, item=c["lot"]["into"], qty=q)
        got += q
    if got <= 1e-9:
        raise Refused("nothing taken down")
    what = " and ".join(sorted({c["lot"]["into"] for _, c in own}))
    return got, f"You took down {_n(got)} kg of {what} from the racks in {b['name']} {dname} ({round(got / WORK['take down'], 2):g} units of work)."


def take_down_units(w, bid, item=None, qty=None) -> int:
    """The act's units (the 1-unit floor, O-2): ceil(kg / 120)."""
    kg = sum(done_kg(c) for c in lots(w, bid, done=True).values() if item is None or c["lot"]["into"] == item)
    if qty is not None:
        kg = min(kg, float(qty))
    return max(1, int(math.ceil(kg / WORK["take down"] - 1e-9)))


# ---------------------------------------------------------------------------------------------------------------------- the night
def night(w, rec) -> None:
    """Each container's condition tonight (u4 §5 steps 1 to 3), after the hearths' fires are set and before the night's spoiling: a
    fire row's lots count a night when the fire was tended today and its fuel burns (all or none), and the building's keyed chance
    that it catches is rolled; a hearth's rack when the hearth was lit tonight (outside, a dry night); retting in water unless a spate
    washes a share away. A night not met is marked `out` (the lot spoils at its input's base: `decay`)."""
    from cybertron2.engine import environment as EV, forests as FO
    from cybertron2.engine.data import PHYSICS
    P = PHYSICS["smokehouse"]
    by_b = {}
    for cid, c in lots(w, done=False).items():
        by_b.setdefault(c.get("in") or c.get("door") or ("parcel", c.get("parcel")), []).append(cid)
    for key in sorted(by_b, key=str):
        cids = by_b[key]
        if isinstance(key, tuple):                                             # on a parcel: retting
            _ground_night(w, rec, key[1], cids)
            continue
        bid = key
        b = w.s["buildings"].get(bid)
        if b is None:
            continue
        node = b["node"]
        fire = [x for x in cids if PROCESSES[w.s["containers"][x]["lot"]["process"]].get("fire")]
        rest = [x for x in cids if x not in fire]
        if fire and not b.get("unfinished"):
            sm = dict(b.get("smoke") or {})
            need = fuel_tonight(w, bid)
            have = fuel_have(w, bid)
            lit = sm.get("tended") == w.d and have + 1e-9 >= need
            if lit:                                                           # its store first, then the woodpile at its door
                left = need
                for fc in fuel_cids(w, bid):
                    h = min(left, FO.heat_of(w.goods(fc)))
                    if h > 1e-9:
                        FO.burn(w, node, fc, round(h, 6), why="smoke fire")
                        left -= h
                    if left <= 1e-9:
                        break
            w.apply("set", node, ref=("building", bid), field="smoke", value={**sm, "night": w.d, "lit": bool(lit), "had": True,
                                                                             "fuel": round(need, 4)})
            for x in fire:
                _count(w, node, x, lit)
            rec.setdefault("smokehouse", {})[bid] = {"lit": bool(lit), "lots": len(fire), "fuel": bundles(need)}
            if lit and w.rng("smokehouse fire", w.d, bid).random() < float(P["fire"].get(b["structure"], P["fire"]["wattle"])):
                rec.setdefault("smokehouse_fires", []).append(catch(w, bid))
        for x in rest:
            c = w.s["containers"][x]
            ok = bool(b.get("fire")) if c.get("in") == bid else not EV.wet(w, node)   # the hearth lit; outside, a dry night
            _count(w, node, x, ok)
        if rest:
            rec.setdefault("racks", {})[bid] = {"lots": len(rest)}


def _ground_night(w, rec, pid, cids) -> None:
    """Retting on a parcel: in water a spate or flood at the river washes a share away (the night not counted); on the grass none."""
    from cybertron2.engine import wild as WL
    par = w.s["parcels"][pid]
    node = par["node"]
    spate = WL.flow_tonight(w, node) in ("spate", "flood") and bool(WL._river_parcel(w, pid))
    for x in cids:
        c = w.s["containers"][x]
        lt = c["lot"]
        if lt.get("ground") == "water" and spate:
            q = waiting_kg(c) * float(PROCESSES[lt["process"]].get("wash", 0.5))
            if q > 1e-9:
                w.apply("destroy", node, src=x, item=lt["wait"], qty=round(q, 6), why="washed away")
            _count(w, node, x, False)
        else:
            _count(w, node, x, True)
    rec.setdefault("retting", {})[pid] = {"lots": len(cids), "spate": bool(spate)}


def _count(w, node, cid, ok) -> None:
    lt = dict(w.s["containers"][cid]["lot"])
    if ok:
        lt["had"] = int(lt.get("had", 0)) + 1
    else:
        lt["out"] = w.d
    w.apply("set_thing", node, cid=cid, field="lot", value=lt)


def finish(w, rec) -> None:
    """A lot that has had its nights becomes its output (u4 §5 step 5), after the night's loss: its waiting good destroyed and the
    output created at the row's ratio; it stays in its container (Departure 6); `done` and `got` recorded for the book's states and the
    morning lines; rec["lots"] for the record."""
    for cid, c in lots(w, done=False).items():
        lt = c["lot"]
        if int(lt.get("had", 0)) < int(lt["nights"]):
            continue
        node = c["node"]
        q = waiting_kg(c)
        got = 0.0
        if q > 1e-9:
            w.apply("destroy", node, src=cid, item=lt["wait"], qty=q, why=PROCESSES[lt["process"]].get("word", "done"))
            got = w.apply("create", node, dst=cid, item=lt["into"], qty=round(q * float(lt["ratio"]), 4),
                          why=PROCESSES[lt["process"]].get("word", "done"))
        w.apply("set_thing", node, cid=cid, field="lot", value={**lt, "done": w.d, "got": round(float(got or 0.0), 4)})
        where = c.get("in") or c.get("door") or c.get("parcel")
        rec.setdefault("lots", {}).setdefault(where, {})[cid] = {"process": lt["process"], "had": lt["had"], "nights": lt["nights"],
                                                                 "done": w.d, "out": lt.get("out"), "got": round(float(got or 0.0), 4)}


def decay(w, c, item, cond, season, cold) -> tuple | None:
    """A lot's goods tonight (u4 §5 step 4): waiting and its night met, the row's in-process base (0.03; a salted lot its own base);
    a night failed, its input good's base, in the open's penalties outside; done, its output hung (U5: the racks keep off the flies
    and the floor's damp: the good's base and the season), or in the open's outside. None: not a lot's good."""
    from cybertron2.engine import night as N
    lt = c.get("lot")
    if not lt:
        return None
    r = PROCESSES[lt["process"]]
    outside = not c.get("in")
    if lt.get("done") is None and item == lt["wait"]:
        if lt.get("out") == w.d:                                              # its fire died, or the hearth was cold
            return (N.spoil_rate(w.p, lt["item"], cond, season, cold) if outside else N.spoil_rate(w.p, lt["item"], "hand", season, cold)), None
        if r.get("in_rate") is None:
            return N.spoil_rate(w.p, item, "hand", season, cold), None
        return float(r["in_rate"]), None
    if outside and not c.get("door"):                                         # retted flax on the ground: no loss
        return 0.0, None
    if outside:
        return N.spoil_rate(w.p, item, cond, season, cold), None
    return N.spoil_rate(w.p, item, "hand", season, cold), None               # hung inside: base and the season


# ---------------------------------------------------------------------------------------------------------------------- fire
def catch(w, bid) -> dict:
    """A smokehouse's fire catches in the night (brief 5 §4a.1): it burns, its lots with it, and each other building on its parcel
    catches by its structure's `spread` chance."""
    from cybertron2.engine.data import PHYSICS
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
                if c.get("lot") and c["lot"].get("done") is None:
                    w.apply("set_thing", node, cid=cid, field="lot", value={**c["lot"], "out": w.d})
    if b.get("level") is not None:                                         # in levels: a fire takes it to holed or worse (brief 4 §3)
        BL.set_level(w, node, bid, min(BL.level(b), 2) - (int(damage) - 1))
    else:
        w.apply("set", node, ref=("building", bid), field="condition", value=max(0, b["condition"] - int(damage)))
    w.apply("set", node, ref=("building", bid), field="fire_hit", value={"day": day})   # for its signs (D4-74)
    live = [m for m in w.living() if bid in w.homes(m)]
    w.event(node, "fire", f"fire broke out in {b['name']} in the night: the store is burnt, most of its food is gone and the roof "
            "is damaged", about=[f"building:{bid}"], salience=0.95, tags=["danger", "food", "shelter"], concerns=live, dawn=True)


# ---------------------------------------------------------------------------------------------------------------------- the floor
def work_floor(b) -> int:
    """The floor a smokehouse keeps free to work and keep the fire (u4 §4): a hut room 1, any other 2; none without racks."""
    rs = b.get("rooms") or []
    if not rs:
        return 0
    return WORK_FLOOR["hut"] if all(r.get("kind") == "hut" for r in rs) else WORK_FLOOR["other"]


def sets_fit(b, free) -> int:
    """How many more sets of racks a building's free floor takes, keeping its work floor (u4 §4)."""
    from cybertron2.engine.data import FITTINGS as F
    keep = work_floor(b)
    return max(0, (int(free) - keep) // max(1, int(F["smoke racks"]["spaces"])))


# ---------------------------------------------------------------------------------------------------------------------- what is known
def house_lines(here, bid) -> list:
    """What a household knows of its containers in a building without a roll (u4 §7; brief 4c §6.4): what waits and its nights, what is
    done and waiting to be taken down, the fire tended today and its fuel, a night it died; the room. Facts, never advice; lower case,
    without a full stop."""
    w = here._w
    b = here.buildings()[bid]
    on = lots(w, bid)
    out = []
    smoke = is_smokehouse(b)
    at = "on the smoke racks" if smoke else "on the rack by the hearth" if (b.get("fittings") or {}).get("hearth") else "on the rack by the fire at its door"
    for cid, c in on.items():
        lt = c["lot"]
        mine = lt.get("household") == here.household() or lt.get("by") == here.name
        by = "" if mine or not lt.get("by") else f" (hung by {lt['by']})"
        if lt.get("done") is None:
            q = waiting_kg(c)
            if q > 1e-6:
                what = f"{lt['item']} smoking" if lt["process"] == "keeping smoke" else (
                    f"{lt['item']} on the racks for a hard cure" if lt["process"] == "hard cure" else f"{lt['item']} drying")
                out.append(f"{at}: {_n(q)} kg of {what}, {_left_words(c, here.day)}{by}")
        else:
            q = done_kg(c)
            if q > 1e-6:
                ago = here.day - 1 - int(lt["done"])
                when = "done last night" if ago <= 0 else f"done {ago + 1} nights ago"
                out.append(f"{at}: {_n(q)} kg of {lt['into']}, {when}, waiting to be taken down{by}")
    sm = b.get("smoke") or {}
    wait = [c for c in on.values() if c["lot"].get("done") is None and PROCESSES[c["lot"]["process"]].get("fire")]
    if smoke and sm.get("night") == here.day - 1 and not sm.get("lit") and sm.get("had"):
        if any(c["lot"].get("out") == here.day - 1 for c in on.values()):
            out.append("the fire died last night: what hung there lost a night's smoke and spoiled a little")
    if smoke and wait:
        out.append("the fire tended today" if sm.get("tended") == here.day else
                   "the fire not tended today: it dies tonight unless someone tends it")
        need, have = fuel_tonight(w, bid), fuel_have(w, bid)
        out.append(f"firewood for tonight's fire ({_n(bundles(need))} bundles needed, {_n(bundles(have))} there)" if have + 1e-9 >= need else
                   f"not enough firewood for tonight's fire ({_n(bundles(need))} bundles needed, {_n(bundles(have))} there)")
    elif smoke and on and sm.get("tended") == here.day:
        out.append("the fish on the racks have had their smoke: more fire does them no good")
    if smoke:
        left = room(w, bid, "keeping smoke")
        cap = capacity(b, "keeping smoke")
        out.append("the racks are empty" if left >= cap - 1e-6 else "the racks are full" if left <= 1e-6 else f"room on the racks for {_n(left)} kg more")
    return out


def states(w, household, bid) -> dict:
    """The lasting states of a building's containers for the book (u6 §3; read only from what the household knows: its own):
    {"done": kg done waiting, "in process": kg waiting, "room": kg of room on its racks, "full": bool, "fire out": the fire died last
    night with something waiting}."""
    b = w.s["buildings"][bid]
    on = lots(w, bid)
    wait = sum(waiting_kg(c) for c in on.values() if c["lot"].get("done") is None)
    done = sum(done_kg(c) for c in on.values() if c["lot"].get("done") is not None and c["lot"].get("household") == household)
    procs = sorted({p for f, d in __import__("cybertron2.engine.data", fromlist=["FITTINGS"]).FITTINGS.items()
                    if (b.get("fittings") or {}).get(f) for p in (d.get("process") or [])})
    rm = max([room(w, bid, p) for p in procs] or [0.0])
    sm = b.get("smoke") or {}
    return {"done": round(done, 4), "in process": round(wait, 4), "room": round(rm, 4), "full": bool(procs) and rm <= 1e-6,
            "fire out": bool(sm.get("night") == w.d - 1 and not sm.get("lit") and any(c["lot"].get("out") == w.d - 1 for c in on.values()))}


# ---------------------------------------------------------------------------------------------------------------------- salting
def salt(here, tech, bid, kg) -> str:
    """Salting at once (u4 §2, §6; D2-283; Departure 7): fish or meat with salt at 1 to 4 (meat 1 to 8), gutting included, into the
    building's store, where the sort puts it in a salting tub or a barrel if one has room (in brine), else packed in its salt on the
    floor (u5: out of brine it keeps worse). As much as the salt to hand allows."""
    from cybertron2.engine import knowledge as KN, stores as SR, verbs as V
    from cybertron2.engine.data import TECHNIQUES as T
    from cybertron2.engine.world import Refused
    r = PROCESSES["salting"]
    item = next(i for i in T[tech]["inputs"] if i != "salt")
    into = r["in"][item][1]
    per = float(r["salt"][item])
    have_s, have_i = KN.available(here, "salt"), KN.available(here, item)
    want = float(kg)
    kg = round(min(want, have_i, have_s / per), 4)
    if kg <= 1e-6:
        raise Refused(f"there is no {item} to hand" if have_i <= 1e-9 else f"there is no salt to hand: it takes 1 kg of salt to {1 / per:g} of {item}")
    b = here.buildings()[bid] if bid else None
    start = V._drew_reset(here)
    V._consume(here, {item: kg, "salt": round(kg * per, 4)}, 1.0, None)
    dst = b["stock"] if b is not None else here.hands
    here.apply("create", dst=dst, item=into, qty=kg, why=tech)
    units = max(1, int(math.ceil(kg / float(r["load"]) - 1e-9)))
    work = f"{units} unit{'s' if units != 1 else ''}" if not getattr(here, "_chore", False) else f"{round(kg / float(r['load']), 2):g} units of work"
    short = f" with the {_n(kg * per)} kg of salt you had" if kg + 1e-6 < min(want, have_i) else f" with {_n(kg * per)} kg of salt"
    head = f"You salted {_n(kg)} kg of {item}{short} ({work}): {_n(kg)} kg of {into}"
    if b is None:
        return head + ", in your hands, packed in its salt." + V._drew_words(here, start)
    pt = SR.portions(b, here._w.goods(b["stock"]))
    tub = sum(x["qty"] for x in pt["portions"] if x["item"] == into and x["kind"] in ("salting tub", "barrel"))
    if tub > 1e-6:
        cs = SR.containers_in(here._w.goods(b["stock"]))
        cap = sum(SR.CONTAINERS[k]["holds"] * n for k, n in cs.items() if k in ("salting tub", "barrel"))
        used = sum(x["qty"] * float(__import__("cybertron2.engine.data", fromlist=["ITEMS"]).ITEMS.get(x["item"], {}).get("weight", 1))
                   for x in pt["portions"] if x["kind"] in ("salting tub", "barrel"))
        where = f", in brine in the salting tub at {b['name']} (room there for {_n(max(0.0, cap - used))} kg more)"
    else:
        where = f", packed in its salt in {b['name']}'s store"
    tail = f" It takes 1 kg of salt to {1 / per:g} of {item}." if "you had" in short else ""
    return head + where + "." + tail + V._drew_words(here, start)
