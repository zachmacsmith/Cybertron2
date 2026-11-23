"""Stores and containers (u5; D2-272, D2-279; the build's stage 3, W-99): a store is a space and the containers in it, each holding real
kilograms and removing named risks; a good keeps at its base rate (well kept) times the penalties its place leaves, never below it.

One feature unit (D2-244; feature_packages.md §9.1, §10):
  - data: SPACES (fittings and floors as spaces: what each holds and removes, its vermin factor), CONTAINERS (sacks, baskets, chests,
    salting tubs, barrels: counted goods of a building's store), PENALTIES (what each good meets where it lies), VERMIN (the goods the
    wild kinds take); registered into ITEMS (`vermin`, `container`) and FITTINGS (`holds`, the smoke loft) at load (data.py);
  - the sort: `portions(b, goods, book)`, every good in a building in a space and, inside it, a container or loose, computed each
    time from the goods, the fittings, the containers and the book's `keep` rules (deterministic; nothing stored); buildings.alloc
    reads it for room, the night for spoiling, the wild layer for vermin;
  - processes: `rates` (a store's goods spoiled by portion, night.decay_rate), `exposure` and `take` (vermin by where the goods lie,
    wild._stores), `illness` (vermin's first magnitude on the adult's sudden illness, life._old_age);
  - what a person sees: `store_line` (the store by portion, u5 §7).

Moving within a building is free, so the sort costs nothing; taking down a hung lot is u4's quantity work (process.take_down).
"""
from __future__ import annotations

# ---------------------------------------------------------------------------------------------------------------------- data
# The goods by what they meet (u5 §3; wave1 §2.3, est.)
DRY = ("grain", "rye", "oats", "beans", "meal", "flour", "salt", "bread")                    # floor damp x2, x1.5 in sacks or baskets
CURED = ("dried fish", "dried meat", "smoked fish", "smoked meat", "hard-cured fish", "hard-cured meat")   # floor damp x3, x1.5 baskets
SALTED = ("salt fish", "salt meat")                                                          # out of brine x1.5
FLIES = ("fish", "meat", "smoking fish", "smoking meat", "drying fish", "drying meat", "cheese")   # flies in the warm season x1.5
WARM = ("fish", "meat", "milk", "cheese", "egg")                                             # the warm season, removed by a cellar
ROOTS = ("roots",)                                                                            # the heap x1.5 loose; frost x3
NUTS = ("hazel nuts", "beech nuts", "acorns", "acorn meal")
FRUIT = ("hedge fruit", "berries")
# what the wild kinds take from stores (u5 §5: ITEMS `vermin`, in place of wild.DRY_STORES)
VERMIN = DRY + NUTS + ROOTS + ("cheese", "egg") + CURED + SALTED
PENALTY = {"floor damp": {"dry": 2.0, "cured": 3.0}, "flies": 1.5, "brine": 1.5, "heap": 1.5, "frost": 3.0, "in hand": 1.5}

# Spaces (u5 §1): `holds` kg (`by`: a space of the building's footprint, of the fitting's own floor, of the whole floor), what goods
# it takes (`suits`: None any), what it removes (`removes`) and adds (`adds`), its vermin factor (`vermin`). The loose floor of a
# ground-floor room and of an upper storey are spaces of their own; the door pile is outside (wild._left_out, at 1.5).
SPACES = {
    "granary": {"holds": 400, "by": "space", "suits": ("grain", "rye", "beans", "oats"), "removes": ("floor damp",), "vermin": 0.6,
                "words": "on the granary floor"},
    "cellar": {"holds": 30, "by": "footprint", "suits": None, "removes": ("warm", "frost"), "adds": ("cellar damp",), "vermin": 1.0,
               "words": "in the cellar"},
    "bins": {"holds": 300, "by": None, "suits": DRY + NUTS + CURED, "removes": ("floor damp",), "vermin": {"rats": 0.5, "mice": 0.4},
             "words": "in the bins"},
    "smoke loft": {"holds": 40, "by": "floor", "suits": CURED + SALTED, "removes": ("floor damp", "flies"), "vermin": 0.3,
                   "words": "hung in the smoke loft"},
    "woodshed": {"holds": 9600, "by": None, "suits": ("timber", "firewood", "charcoal"), "removes": ("rain",), "vermin": 0.0,
                 "words": "in the woodshed"},
    "vault": {"holds": 30, "by": "space", "suits": None, "removes": ("fire",), "vermin": 1.0, "words": "in the vault"},
    "upper floor": {"holds": 30, "by": None, "suits": None, "removes": ("floor damp",), "vermin": 1.0, "words": "on the upper floor"},
    "floor": {"holds": 30, "by": None, "suits": None, "removes": (), "vermin": 1.0, "words": "loose on the floor"},
}
SPACE_ORDER = ("granary", "cellar", "bins", "smoke loft", "woodshed", "vault")

# Containers (u5 §2): counted goods of a building's store, each taking floor (`per_space` to a space), holding some goods up to its
# kg, removing named risks (`half`: floor damp at x1.5 in place of x2 or x3), its exposure to rats and mice; lives and making are
# u3's (gear.py: rot by the year)
CONTAINERS = {
    "sack": {"holds": 50, "per_space": 12, "suits": DRY + NUTS, "removes": (), "half": ("floor damp",), "vermin": {"rats": 0.8, "mice": 0.7}},
    "basket": {"holds": 25, "per_space": 10, "suits": ROOTS + NUTS + FRUIT + ("egg", "cheese") + CURED, "removes": ("heap",),
               "half": ("floor damp",), "vermin": {"rats": 0.8, "mice": 0.7}},
    "chest": {"holds": 400, "per_space": 1, "suits": DRY + NUTS + CURED, "removes": ("floor damp",), "vermin": {"rats": 0.2, "mice": 0.15}},
    "salting tub": {"holds": 120, "per_space": 3, "suits": SALTED, "removes": ("brine", "flies"), "vermin": {"rats": 0.05, "mice": 0.05}},
    "barrel": {"holds": 120, "per_space": 4, "suits": SALTED + DRY, "removes": ("brine", "flies", "floor damp"),
               "vermin": {"rats": 0.05, "mice": 0.05}},
}
CONTAINER_ORDER = ("salting tub", "barrel", "chest", "basket", "sack")
WORDS = {"sack": ("sack", "sacks"), "basket": ("basket", "baskets"), "chest": ("the chest", "chests"),
         "salting tub": ("the salting tub", "salting tubs"), "barrel": ("a barrel", "barrels")}

# the new goods and the smoke loft (u5 §1, §2): a chest made by a carpenter of 4 timber (wave1 §3.3; its making is u3's to price)
ITEMS = {"chest": {"weight": 40, "food": 0.0, "spoil": 0.0}}
FITTINGS = {
    "smoke loft": {"label": "a smoke loft (hooks in the roof over the hearth)", "materials": {"timber": 2}, "units": 1, "basic": True,
                   "spaces": 0, "needs": "hearth", "does": "hooks in the roof over the hearth: cured, salt and dried goods hung out of the "
                   "damp and the flies (40 kg a space of the room's floor)"},
}
TECHNIQUES = {
    "chest": {"verb": "make", "label": "making a chest (an ark of boards)", "aliases": ["chests", "an ark", "make a chest"], "basic": False,
              "trade": "carpenter", "inputs": {"timber": 4}, "units": 2, "gives": {"chest": 1}, "tags": ["craft"]},
}
# vermin's sudden illness (u5 §6; G11): the adult's chance x (1 + `most` x min(1, rats a km2 / `rats`) x the household's exposure)
ILLNESS = {"most": 2.0, "rats": 120.0}


def register_items(items) -> None:
    for k, v in ITEMS.items():
        items.setdefault(k, dict(v))
    for k in VERMIN:
        if k in items:
            items[k]["vermin"] = True
    for k, v in CONTAINERS.items():
        if k in items:
            items[k]["container"] = {"holds_kg": v["holds"], "per_space": v["per_space"]}


def register_fittings(fittings) -> None:
    for k, v in FITTINGS.items():
        fittings.setdefault(k, dict(v))
    for k, v in SPACES.items():
        if k in fittings:
            fittings[k].pop("spoil", None)                              # no store slows a food below its base (D2-272)
            fittings[k]["holds"] = {"kg": v["holds"]}
            if v["by"] in ("footprint", "space", "floor"):
                fittings[k]["by"] = v["by"]


def register_techniques(techniques) -> None:
    for k, v in TECHNIQUES.items():
        techniques.setdefault(k, dict(v))


# ---------------------------------------------------------------------------------------------------------------------- the sort
def _weight(item) -> float:
    from cybertron2.engine.data import ITEMS as I
    return float(I.get(item, {}).get("weight", 1))


def _kg_floor(item) -> float:
    """Loose kg a unit takes of free floor: goods stacked by the wall (fuel, straw, hay, stone) take less (STORES `stack`, W-97)."""
    from cybertron2.engine.data import STORES
    st = (STORES.get("stack") or {}).get(item)
    return _weight(item) * (float(STORES["floor"]) / float(st) if st else 1.0)


def suits(row, item) -> bool:
    s = row.get("suits")
    return s is None or item in s


def _cap(name, b, n) -> float:
    from cybertron2.engine import buildings as BL
    from cybertron2.engine.data import FITTINGS as F
    r = SPACES[name]
    if r["by"] == "footprint":
        return float(r["holds"]) * BL.footprint(b)
    if r["by"] == "space":
        return float(r["holds"]) * int(F[name].get("spaces", 1)) * n
    if r["by"] == "floor":
        return float(r["holds"]) * BL.floor(b)
    return float(r["holds"]) * n


def containers_in(goods) -> dict:
    """The containers a store holds, counted: {kind: n}."""
    return {k: int(float(goods.get(k, 0.0)) + 1e-9) for k in CONTAINER_ORDER if float(goods.get(k, 0.0)) >= 1 - 1e-9}


def container_spaces(goods) -> float:
    import math
    return sum(math.ceil(n / CONTAINERS[k]["per_space"] - 1e-9) for k, n in containers_in(goods).items())


def factor(item, kind, season=None, cold=False) -> float:
    """The penalties a good keeps at in a portion of `kind` (a space or a container), multiplied (u5 §3): what its place leaves."""
    if kind in CONTAINERS:
        row, half, base = CONTAINERS[kind], CONTAINERS[kind].get("half", ()), "floor"
    else:
        row, half, base = SPACES.get(kind, SPACES["floor"]), (), kind
    rm = set(row.get("removes", ()))
    k = 1.0
    damp = "cellar damp" in (row.get("adds") or ()) or "floor damp" not in rm
    if damp:
        cls = "dry" if item in DRY else "cured" if item in CURED else None
        if cls:
            f = PENALTY["floor damp"][cls]
            k *= 1.5 if "floor damp" in half else f
    if item in FLIES and season == "summer" and "flies" not in rm:
        k *= PENALTY["flies"]
    if item in SALTED and "brine" not in rm:
        k *= PENALTY["brine"]
    if item in ROOTS and "heap" not in rm and kind in ("floor", "upper floor", "cellar", "vault"):
        k *= PENALTY["heap"]
    return k


def exposure(kind, beast="rats") -> float:
    """A portion's exposure to a kind of vermin (u5 §2, §5): loose 1.0, hung 0.3, in sacks 0.8 and 0.7, in a chest 0.2 and 0.15; the
    space's factor with it (a granary floor 0.6)."""
    col = "mice" if "mice" in str(beast) else "rats"
    row = CONTAINERS.get(kind) or SPACES.get(kind) or SPACES["floor"]
    v = row.get("vermin", 1.0)
    return float(v.get(col, 1.0) if isinstance(v, dict) else v)


def _rank(item, kind, season, cold):
    return (factor(item, kind, season, cold), exposure(kind), (CONTAINER_ORDER + SPACE_ORDER + ("upper floor", "floor")).index(kind))


def portions(b, goods, book=None, season=None, cold=False) -> dict:
    """Where every good in a building lies (u5 §4): {"portions": [{"space", "container", "kind", "item", "qty"}], "left": {item: qty}
    (what found no room), "floor_kg", "floor_spaces", "used": {kind: kg}}. The book's `keep` rules first (u6: [(item, kind, qty)]),
    then for each good the place with room it keeps best in (fewest penalties, then the least exposure, then a fixed order), the most
    perishable first, then by name; then loose on the free floor (the upper storey first for what the damp spoils); what does not fit
    is `left`."""
    import math
    from cybertron2.engine import buildings as BL
    from cybertron2.engine.data import FITTINGS as F, ITEMS as I
    fit = b.get("fittings") or {}
    room = {}
    for name in SPACE_ORDER:
        n = int(fit.get(name, 0) or 0)
        if n and name in F:
            room[name] = _cap(name, b, n)
    for k, n in containers_in(goods).items():
        room[k] = float(CONTAINERS[k]["holds"]) * n
    free = max(0, BL.floor(b) - BL.fitting_spaces(b) - int(math.ceil(container_spaces(goods) - 1e-9)))
    upper = min(free, max(0, BL.floor(b) - BL.floor(b, 1)))
    room["upper floor"] = upper * 30.0
    room["floor"] = (free - upper) * 30.0
    left = {i: float(q) for i, q in goods.items() if q > 1e-9 and i not in CONTAINERS}   # the containers are counted, not kept in one
    out = []
    used = {}

    def put(item, kind, q):
        floor_like = kind in ("floor", "upper floor")
        wt = _kg_floor(item) if floor_like else _weight(item)
        take = min(q, room[kind] / wt) if wt > 0 else q
        if take <= 1e-9:
            return 0.0
        room[kind] -= take * wt
        used[kind] = used.get(kind, 0.0) + take * wt
        out.append({"kind": kind, "item": item, "qty": round(take, 6)})
        return take

    for item, kind, q in (book or []):                                        # the book's keep rules (u6 §4 moment 2)
        if item in left and kind in room and (kind in ("floor", "upper floor") or suits(CONTAINERS.get(kind) or SPACES[kind], item)):
            left[item] -= put(item, kind, min(left[item], float(q) if q is not None else left[item]))
    order = sorted(left, key=lambda i: (-float(I.get(i, {}).get("spoil", 0.0)), i))
    for item in order:
        cands = [k for k in room if k not in ("floor", "upper floor") and suits(CONTAINERS.get(k) or SPACES[k], item)]
        cands += ["upper floor", "floor"]
        for kind in sorted(cands, key=lambda k: _rank(item, k, season, cold)):
            if left.get(item, 0.0) <= 1e-9:
                break
            if room.get(kind, 0.0) <= 1e-9:
                continue
            left[item] -= put(item, kind, left[item])
    left = {i: round(q, 6) for i, q in left.items() if q > 1e-6}
    fl = used.get("floor", 0.0) + used.get("upper floor", 0.0)
    return {"portions": out, "left": left, "floor_kg": round(fl, 6), "used": {k: round(v, 6) for k, v in used.items()},
            "free_spaces": free, "floor_spaces": int(math.ceil(fl / 30.0 - 1e-9)) + int(math.ceil(container_spaces(goods) - 1e-9))}


# ---------------------------------------------------------------------------------------------------------------------- keeping
def _hazard(r, k) -> float:
    """A penalty multiplies the hazard, never the share (wave1 §2.1): r' = 1 - (1 - r)^k."""
    r = min(1.0, max(0.0, float(r)))
    return 1.0 - (1.0 - r) ** float(k) if r < 1.0 else 1.0


def rate(p, item, kind, season, cold) -> float:
    """A good's share lost a night in a portion (u5 §3): its base (well kept, D2-272) with the season (the warm and the frost,
    removed by a cellar for the goods they ruin) and every penalty its place leaves."""
    from cybertron2.engine.data import DECAY, ITEMS as I
    base = float(I.get(item, {}).get("spoil", 0.0))
    if base <= 0:
        return 0.0
    table = DECAY.get(I.get(item, {}).get("decay") or "default", DECAY["default"])
    s = 1.0
    cellar = kind == "cellar"
    if cold:
        s = PENALTY["frost"] if item in ROOTS and not cellar else (1.0 if item in ROOTS else float(table.get("frozen", 1.0)))
    elif season == "summer" and not (cellar and item in WARM):
        s = float(table.get("warm", 1.0))
    return _hazard(base * s, factor(item, kind, season, cold))


def book_keeps(w, bid) -> list:
    """The `keep` rules of the household that holds a building, as the sort reads them: [(item, kind, qty)]."""
    try:
        from cybertron2.engine import book as BK
    except ImportError:                                                       # pragma: no cover
        return []
    return BK.keeps(w, bid)


def rates(w, bid) -> dict:
    """A store's goods tonight, spoiled by portion (u5 §3): {item: the share lost over all of it}."""
    from cybertron2.engine import environment as EV, night as N
    b = w.s["buildings"][bid]
    goods = w.goods(b["stock"])
    season, cold = w.calendar()["season"], w.cold(b["node"])
    lv = b.get("level")
    if lv is not None and int(lv) <= 1:                                       # a failing store is the open (brief 4 §3)
        where = "open_wet" if EV.wet(w, b["node"]) else "open_dry"
        return {i: N.spoil_rate(w.p, i, where, season, cold) for i in goods}
    damp = float(w.p["wear"]["damp"].get(str(int(lv)), 1.0)) if lv is not None else 1.0
    pt = portions(b, goods, book_keeps(w, bid), season, cold)
    lost, have = {}, {}
    for x in pt["portions"]:
        r = rate(w.p, x["item"], x["kind"], season, cold)
        lost[x["item"]] = lost.get(x["item"], 0.0) + x["qty"] * min(1.0, r * damp)
        have[x["item"]] = have.get(x["item"], 0.0) + x["qty"]
    for i, q in pt["left"].items():                                           # no room: loose on the floor at its worst
        r = rate(w.p, i, "floor", season, cold)
        lost[i] = lost.get(i, 0.0) + q * min(1.0, r * damp)
        have[i] = have.get(i, 0.0) + q
    return {i: (lost[i] / have[i] if have[i] > 1e-12 else 0.0) for i in lost}


def in_hand_rate(w, name, item, season, cold) -> float:
    """In hand (u5 §3): fresh foods x1.5, unless carried in a creel or basket."""
    from cybertron2.engine import night as N
    from cybertron2.engine.data import ITEMS as I, KEEP_DAYS
    r = N.spoil_rate(w.p, item, "hand", season, cold)
    fresh = float(KEEP_DAYS.get(item, 99)) <= 4 and float(I.get(item, {}).get("food", 0.0)) > 0
    if fresh and not any(float(w.goods(w.hands(name)).get(x, 0.0)) >= 1 for x in ("creel", "basket")):
        return _hazard(r, PENALTY["in hand"])
    return r


# ---------------------------------------------------------------------------------------------------------------------- vermin
def vermin_portions(w, bid) -> list:
    """[(item, qty, kind)] of a building's vermin goods by where they lie, and its lots hung inside (0.3)."""
    from cybertron2.engine import process as PROC
    b = w.s["buildings"][bid]
    goods = w.goods(b["stock"])
    pt = portions(b, goods, book_keeps(w, bid), w.calendar()["season"], w.cold(b["node"]))
    out = [(x["item"], x["qty"], x["kind"]) for x in pt["portions"] if x["item"] in VERMIN]
    out += [(i, q, "floor") for i, q in pt["left"].items() if i in VERMIN]
    for cid, c in PROC.lots(w, bid).items():
        if c.get("in") == bid:
            out += [(i, float(q), "smoke loft") for i, q in sorted(c["goods"].items()) if i in VERMIN and q > 1e-9]
    return out


def exposed(w, bid) -> float:
    """A building's exposed store (u5 §5): sum of its vermin goods by their exposure (rats and mice alike, their mean)."""
    return sum(q * 0.5 * (exposure(k, "rats") + exposure(k, "mice")) for _, q, k in vermin_portions(w, bid))


def household_exposure(w, hh) -> float:
    """E_h (u5 §6): the exposure-weighted share of a household's vermin goods, sum q x exposure / sum q over its buildings, at most 1;
    0 with none."""
    tot = ex = 0.0
    for bid, b in sorted(w.s["buildings"].items()):
        if not b.get("stock") or b.get("monument") or not any(c["claimant"] == hh for c in w.claims_on(("building", bid))):
            continue
        for _, q, k in vermin_portions(w, bid):
            tot += q
            ex += q * 0.5 * (exposure(k, "rats") + exposure(k, "mice"))
    return min(1.0, ex / tot) if tot > 1e-9 else 0.0


def illness(w, name) -> float:
    """Vermin's factor on an adult's sudden illness (u5 §6; G11, a first magnitude, est.): 1 + 2 x min(1, R / 120) x E_h, R the rats a
    km2 in the household's home area, E_h its exposure. 1 without the wild layer, rats or a household."""
    hh = w.household_of(name)
    if not hh:
        return 1.0
    R = rats_at(w, w.at(name))
    if R <= 0:
        return 1.0
    return 1.0 + float(ILLNESS["most"]) * min(1.0, R / float(ILLNESS["rats"])) * household_exposure(w, hh)


def rats_at(w, node) -> float:
    wild = w.s.get("wild") or {}
    st = wild.get("state") or {}
    if node is None or "rats" not in (st.get("pop") or {}):
        return 0.0
    from cybertron2.engine import wild as WL
    m = WL.model(w)
    home = (wild.get("land") or {}).get("home", {}).get(node)
    if home not in m.ids:
        return 0.0
    return float(st["pop"]["rats"][m.ids.index(home)])


# ---------------------------------------------------------------------------------------------------------------------- words
def store_line(b, goods, book=None) -> str:
    """The store by portion (u5 §7): '735 grain (400 in the chest, 300 in 6 sacks, 35 loose on the floor), 80 salt fish in brine in
    the salting tub'. Facts, never advice."""
    from cybertron2.engine.world import show
    pt = portions(b, goods, book)
    by = {}
    for x in pt["portions"]:
        by.setdefault(x["item"], []).append(x)
    for i, q in pt["left"].items():
        by.setdefault(i, []).append({"kind": "none", "item": i, "qty": q})
    cs = containers_in(goods)
    bits = []
    for item in sorted(by, key=lambda i: -sum(x["qty"] for x in by[i])):
        tot = sum(x["qty"] for x in by[item])
        if tot <= 0.05:
            continue
        parts = []
        for x in by[item]:
            k = x["kind"]
            if k in CONTAINERS:
                n = cs.get(k, 0)
                where = (f"in brine in {WORDS[k][0]}" if k in ("salting tub", "barrel") and item in SALTED else
                         f"in {WORDS[k][0]}" if n == 1 and k in ("chest", "salting tub") else
                         f"in a {k}" if n == 1 else f"in {n} {WORDS[k][1]}")
            elif k == "none":
                where = "with no room for it"
            else:
                where = SPACES[k]["words"]
            parts.append((x["qty"], where))
        if len(parts) == 1:
            bits.append(f"{show(round(tot, 1))} {item} {parts[0][1]}")
        else:
            bits.append(f"{show(round(tot, 1))} {item} (" + ", ".join(f"{show(round(q, 1))} {wh}" for q, wh in parts) + ")")
    return ", ".join(bits)
