"""Buildings in spaces (spec/economy/buildings.md; review 02zh; D2-154, D2-155, D2-165 to D2-171).

One unit of space at every level: a parcel's ground for buildings (built ground 24 a unit of size, scrub 16), a building's rooms and
their floor (small 6, medium 12, hall 30; upper storeys in stone take no ground), and every fitting and store taking floor. People
housed are the beds. A store holds so much by its kind (bins 60 food, a granary floor 300 grain, a cellar 40 food a space of the
building's footprint, a woodshed about 9,600 kg of timber and fuel, a vault 30 weight a space); what is left over lies on free floor, 30 weight a space.

The functions here read records (a building, a parcel, its goods), never the world, so the agent-facing modules (verbs, prompts) may
call them with what `Here` gives them (D4-35). The engine side (`overflow`, `read`, `seed_rooms`) takes the world.

A building's record (beyond world.py's): rooms [{kind, floor, storey}], tier, description {text, by, day}, lines [{slot, text, by,
day, how, was}], changes [{day, text, by}] (what its people will notice), works {kind, ...} (a room, a storey, an upgrade, a tier
raised: under way), mending {units_left}, monument (its kind).
"""
from __future__ import annotations

import math

from cybertron2.engine.data import COVERS, EDIBLE, FITTINGS, ITEMS, LINES, MONUMENTS, ROOMS, SPACE, STORES, TIERS, TIER_ORDER


# ---------------------------------------------------------------------- rooms and floor
def exempt(b) -> bool:
    """A camp (a lean-to: what lies in it is not counted) and a monument (no room) keep no floor."""
    return b.get("structure") == "camp" or bool(b.get("monument"))


def rooms(b) -> list:
    return list(b.get("rooms") or [])


def floor(b, storey=None) -> int:
    return sum(int(r["floor"]) for r in rooms(b) if storey is None or int(r.get("storey", 1)) == storey)


def footprint(b) -> int:
    """Its ground-floor rooms (D2-154), and a ground-floor room under way (its ground is taken when the work starts)."""
    n = floor(b, 1)
    wk = b.get("works") or {}
    if wk.get("kind") == "room" and int(wk.get("storey", 1)) == 1:
        n += int(wk["floor"])
    for f, u in (b.get("fitting_work") or {}).items():
        if FITTINGS.get(f, {}).get("room"):
            n += int(FITTINGS[f]["room"]) * int(u.get("n", 1))
    return n


def storeys(b) -> int:
    return max([int(r.get("storey", 1)) for r in rooms(b)] or [1])


def places(b) -> int:
    if b.get("monument"):
        return int(LINES["places"]["monument"])
    return sum(int(ROOMS.get(r["kind"], {}).get("places", 0)) for r in rooms(b))


def tier(b) -> str:
    return b.get("tier") or "plain"


def fitting_spaces(b, heavy=False) -> int:
    """The floor its fittings take, with those under way (02zg): beds and stalls so many each."""
    n = 0
    have = dict(b.get("fittings") or {})
    for f, u in (b.get("fitting_work") or {}).items():
        have[f] = int(have.get(f, 0)) + int(u.get("n", 1))
    for f, k in have.items():
        d = FITTINGS.get(f)
        if d and k and (not heavy or d.get("heavy")):
            n += int(d.get("spaces", 0)) * int(k)
    return n


def room_words(b) -> str:
    kinds = {}
    for r in rooms(b):
        if r["kind"] in ROOMS:
            key = r["kind"] + (f" on storey {r['storey']}" if int(r.get("storey", 1)) > 1 else "")
            kinds[key] = kinds.get(key, 0) + 1
    from cybertron2.engine.layout import _count
    return ", ".join(_count(n, k) for k, n in kinds.items())


# ---------------------------------------------------------------------- ground (D2-154, D2-164)
def ground_total(p) -> int:
    return int(COVERS.get(p["cover"], {}).get("ground", 0)) * int(p.get("size", 1))


def ground_of(b, cover) -> int:
    """What a building takes of its parcel's ground: its footprint and any woodshed; a camp its lean-to and a monument one space, on
    ground that takes buildings (none elsewhere)."""
    builds = int(COVERS.get(cover, {}).get("ground", 0)) > 0
    if b.get("monument"):
        return int(SPACE["monument_ground"]) if builds else 0
    if b.get("structure") == "camp":
        return int(SPACE["camp_floor"]) if builds else 0
    sheds = int((b.get("fittings") or {}).get("woodshed", 0)) + sum(int(u.get("n", 1)) for f, u in (b.get("fitting_work") or {}).items()
                                                                     if f == "woodshed")
    return footprint(b) + sheds * int(FITTINGS["woodshed"]["ground"])


def ground_used(pid, p, buildings) -> int:
    return sum(ground_of(b, p["cover"]) for b in buildings.values() if b["parcel"] == pid)     # a ruin keeps its ground


def ground_free(pid, p, buildings) -> int:
    return ground_total(p) - ground_used(pid, p, buildings)


# ---------------------------------------------------------------------- storage (D2-155; u5: stores.py)
def _weight(item) -> float:
    return float(ITEMS.get(item, {}).get("weight", 1))


def _floor_weight(item) -> float:
    """What a unit of a good takes of free floor, as loose weight: goods stacked by the wall (fuel, straw, hay, stone) take less than
    their kilograms (STORES `stack`: kg a space stacked, against `floor` loose; D2-288's handling units, W-97)."""
    st = (STORES.get("stack") or {}).get(item)
    return _weight(item) * (float(STORES["floor"]) / float(st) if st else 1.0)


def stores(b) -> list:
    """[(store, kind, capacity kg)] of a building's fitted stores (u5 §1: real capacities in kg, D2-279)."""
    from cybertron2.engine import stores as SR
    if exempt(b):
        return []
    fit = b.get("fittings") or {}
    return [(name, "kg", SR._cap(name, b, int(fit[name]))) for name in SR.SPACE_ORDER if int(fit.get(name, 0) or 0) and name in FITTINGS]


def alloc(b, goods, book=None) -> dict:
    """Where its goods lie (u5 §4: stores.portions): {"stores": {store or container: kg}, "floor_weight": kg loose and what found no
    room, "floor_spaces": the floor that takes (with the containers' own), "on_floor": {item: qty}, "portions": the sort}."""
    from cybertron2.engine import stores as SR
    pt = SR.portions(b, goods, book)
    used = {k: v for k, v in pt["used"].items() if k not in ("floor", "upper floor")}
    on = {}
    for x in pt["portions"]:
        if x["kind"] in ("floor", "upper floor"):
            on[x["item"]] = on.get(x["item"], 0.0) + x["qty"]
    for i, q in pt["left"].items():
        on[i] = on.get(i, 0.0) + q
    weight = pt["floor_kg"] + sum(q * _floor_weight(i) for i, q in pt["left"].items())
    spaces = int(math.ceil(weight / float(STORES["floor"]) - 1e-9)) + int(math.ceil(SR.container_spaces(goods) - 1e-9))
    return {"stores": used, "floor_weight": round(weight, 6), "floor_spaces": spaces, "on_floor": on, "portions": pt,
            "left": pt["left"]}


def free_floor(b, goods=None) -> int:
    """Floor neither fitted nor taken by goods lying on it (or by the containers they are kept in)."""
    if exempt(b):
        return 0
    return floor(b) - fitting_spaces(b) - (alloc(b, goods)["floor_spaces"] if goods else 0)


def camp_weight(goods) -> float:
    return sum(float(q) * _floor_weight(i) for i, q in (goods or {}).items() if q > 1e-9)


def fits(b, goods) -> bool:
    if b.get("structure") == "camp":                                        # a lean-to keeps little (D4-84)
        return camp_weight(goods) <= float(SPACE["camp_store"]) + 1e-6
    if exempt(b):
        return True
    return not alloc(b, goods)["left"]


def room_for(b, goods, item) -> float:
    """How much more of a good its stores and free floor can take."""
    if b.get("structure") == "camp":                                        # D4-84
        wt = _floor_weight(item)
        return max(0.0, float(SPACE["camp_store"]) - camp_weight(goods)) / wt if wt > 0 else float("inf")
    if exempt(b):
        return float("inf")
    if not fits(b, goods):
        return 0.0
    lo, hi = 0.0, 1.0
    g = dict(goods)
    while fits(b, {**g, item: float(g.get(item, 0.0)) + hi}) and hi < 1e7:
        lo, hi = hi, hi * 2
    for _ in range(40):
        mid = (lo + hi) / 2
        if fits(b, {**g, item: float(g.get(item, 0.0)) + mid}):
            lo = mid
        else:
            hi = mid
    return math.floor(lo * 100 + 1e-6) / 100


def full_words(b, goods, item) -> str:
    """What is full, for a refusal: "the bins hold 300 kg; 298 are in them; the free floor (2 spaces) holds 60 kg; 55 lie on it"."""
    from cybertron2.engine.world import show
    from cybertron2.engine import stores as SR
    if b.get("structure") == "camp":                                        # D4-84
        return f"a camp keeps {show(float(SPACE['camp_store']))} weight; {show(camp_weight(goods))} lie in it"
    a = alloc(b, goods)
    bits = []
    for name, kind, cap in stores(b):
        if not SR.suits(SR.SPACES[name], item):
            continue
        say, where = STORES["words"][name]
        bits.append(f"{say} {show(cap)} kg; {show(round(a['stores'].get(name, 0.0), 1))} {where}")
    for k, n in SR.containers_in(goods).items():
        if SR.suits(SR.CONTAINERS[k], item):
            bits.append(f"{n} {SR.WORDS[k][1] if n != 1 else k} hold{'s' if n == 1 else ''} {show(n * SR.CONTAINERS[k]['holds'])} kg; "
                        f"{show(round(a['stores'].get(k, 0.0), 1))} in {'it' if n == 1 else 'them'}")
    open_ = floor(b) - fitting_spaces(b) - int(math.ceil(SR.container_spaces(goods) - 1e-9))
    if open_ > 0:
        bits.append(f"the free floor ({open_} space{'s' if open_ != 1 else ''}) holds {show(open_ * float(STORES['floor']))} kg; "
                    f"{show(round(a['floor_weight'], 1))} lie on it")
    else:
        bits.append("no floor is free: the fittings take it all")
    return "; ".join(bits)


def space_words(b, goods) -> str:
    """"12 spaces, 9 used: 6 beds, a hearth, bins, a hand mill; 3 free" (02zh §9)."""
    if b.get("monument"):
        return ""
    if b.get("structure") == "camp":
        return f"a lean-to for {int((b.get('fittings') or {}).get('beds', 0))}"
    fl = floor(b)
    fit = []
    for f, n in (b.get("fittings") or {}).items():
        if f in FITTINGS and n:
            fit.append(f"{n} beds" if f == "beds" else f"{n} stalls" if f == "stalls" else FITTINGS[f]["label"])
    for f, u in (b.get("fitting_work") or {}).items():                        # a fitting begun: seen, with its work left (wheel fix)
        if f in FITTINGS:
            n = int(u.get("n", 1))
            fit.append(f"{FITTINGS[f]['label'] if n == 1 else f'{n} {f}'} begun, its materials in "
                       f"(about {float(u['units_left']):.0f} units of work left)")
    a = alloc(b, goods)
    used = fitting_spaces(b) + a["floor_spaces"]
    if a["floor_spaces"]:
        fit.append(f"goods on the floor ({a['floor_spaces']} space{'s' if a['floor_spaces'] != 1 else ''})")
    return f"{fl} spaces, {used} used" + (f": {', '.join(fit)}" if fit else "") + f"; {max(0, fl - used)} free"


# ---------------------------------------------------------------------- costs (the room table, D2-154, D2-166, D2-171)
def room_cost(kind, structure, added=False, storey=1, how="plain") -> dict:
    """{materials, units, trade} of a room: alone, added to a building (a quarter less), or on an upper storey (1.5x, 2x)."""
    r = ROOMS[kind].get(structure)
    if r is None:
        return {}
    m = 1.0
    if storey > 1:
        m *= float(SPACE["storeys"][storey])
    elif added:
        m *= float(SPACE["added"])
    t = TIERS[how]
    return {"materials": {i: round(q * m * float(t["materials"]), 2) for i, q in r["materials"].items()},
            "units": round(float(r["units"]) * m * float(t["work"]), 2), "trade": r.get("trade")}


def upgrade_cost(b, to) -> dict:
    """A building's structure raised (wattle to timber, timber to stone): the new structure's materials for its rooms less a quarter,
    and the work (02zh §2), at its tier."""
    mats, units = {}, 0.0
    t = TIERS[tier(b)]
    for r in rooms(b):
        rc = ROOMS.get(r["kind"], {}).get(to)
        if rc is None:
            continue
        m = float(SPACE["storeys"].get(int(r.get("storey", 1)), 1.0))
        for i, q in rc["materials"].items():
            mats[i] = round(mats.get(i, 0.0) + q * m * float(SPACE["upgrade"]) * float(t["materials"]), 2)
        units += float(rc["units"]) * m * float(t["work"])
    return {"materials": mats, "units": round(units, 2), "trade": "mason" if to == "stone" else ("carpenter" if any(
        ROOMS.get(r["kind"], {}).get(to, {}).get("trade") == "carpenter" for r in rooms(b)) else None)}


def base_cost(b) -> dict:
    """What its rooms (or its monument) cost plain: for raising its tier by the difference (D2-171)."""
    if b.get("monument"):
        d = MONUMENTS[b["monument"]]
        return {"materials": dict(d["materials"]), "units": float(d["units"])}
    mats, units = {}, 0.0
    for r in rooms(b):
        rc = ROOMS.get(r["kind"], {}).get(b["structure"])
        if rc is None:
            continue
        for i, q in rc["materials"].items():
            mats[i] = mats.get(i, 0.0) + q
        units += float(rc["units"])
    return {"materials": mats, "units": units}


def tier_cost(b, to) -> dict:
    """Raising its tier: the difference in materials and work (D2-171)."""
    base = base_cost(b)
    d = float(TIERS[to]["materials"]) - float(TIERS[tier(b)]["materials"])
    k = float(TIERS[to]["work"]) - float(TIERS[tier(b)]["work"])
    return {"materials": {i: round(q * d, 2) for i, q in base["materials"].items()}, "units": round(base["units"] * k, 2)}


def tier_up(a, b) -> bool:
    return TIER_ORDER.index(a) > TIER_ORDER.index(b)


LEVELS = {5: "sound", 4: "worn", 3: "gappy", 2: "holed", 1: "failing", 0: "ruined"}
CAMP_LEVELS = {5: "standing", 2: "damaged", 0: "down"}
COND_OF_LEVEL = {5: 2, 4: 2, 3: 2, 2: 1, 1: 1, 0: 0}
LEVEL_OF_COND = {2: 5, 1: 2, 0: 0}


def levels_on(w) -> bool:
    """Shelter in levels (brief 4 §3): worlds with the wild pack, or a world's `shelter_levels`; older worlds as before."""
    sp = getattr(w, "spec", None) or {}
    return bool(sp.get("shelter_levels", "wild" in (sp.get("packs") or [])))


def level(b) -> int:
    """A building's level of condition: its own, else read from its coarse condition (2 sound, 1 holed, 0 ruined)."""
    return int(b["level"]) if b.get("level") is not None else LEVEL_OF_COND.get(int(b.get("condition", 2)), 5)


def level_word(b) -> str:
    return (CAMP_LEVELS if b.get("structure") == "camp" else LEVELS).get(level(b), "damaged")


def set_level(w, node, bid, lv, why=None) -> None:
    """Set a building's level, and its coarse condition with it (2 sound to gappy, 1 holed and failing, 0 ruined)."""
    lv = max(0, min(5, int(lv)))
    b = w.s["buildings"][bid]
    if b.get("structure") == "camp":
        lv = 5 if lv >= 5 else (2 if lv >= 1 else 0)
    w.apply("set", node, ref=("building", bid), field="level", value=lv)
    w.apply("set", node, ref=("building", bid), field="level_since", value=w.d)
    if COND_OF_LEVEL[lv] != int(b["condition"]):
        w.apply("set", node, ref=("building", bid), field="condition", value=COND_OF_LEVEL[lv])


def repair_need(b) -> dict:
    """D2-168: 1 timber (stone for a stone building) and 1 unit for every 4 spaces of floor, at least 2 and 2."""
    from cybertron2.engine.data import PHYSICS
    rp = PHYSICS["repair"]
    n = max(int(rp["min"]), int((floor(b) or (4 if b.get("structure") == "camp" else 0)) // int(rp["per"])))
    return {"materials": {("stone" if b.get("structure") == "stone" else "timber"): n}, "units": n}


# ---------------------------------------------------------------------- seeding (02zh §1, §8: floor enough for what is in it)
def best_rooms(need, structure) -> list:
    """The rooms with the least floor that cover `need` spaces (fewest rooms among equals); wattle takes small rooms only."""
    kinds = [k for k in ("hall", "medium room", "small room") if structure in ROOMS[k]] or ["small room"]
    if need <= 0:
        return ["small room"]
    best = None
    sizes = {k: int(ROOMS[k]["floor"]) for k in kinds}
    lim = {k: int(math.ceil(need / sizes[k])) + 1 for k in kinds}
    import itertools
    for counts in itertools.product(*[range(lim[k] + 1) for k in kinds]):
        tot = sum(c * sizes[k] for c, k in zip(counts, kinds))
        if tot < need or sum(counts) == 0:
            continue
        key = (tot, sum(counts))
        if best is None or key < best[0]:
            best = (key, counts)
    return [k for c, k in zip(best[1], kinds) for _ in range(c)]


def seed_rooms(spec_b, fittings, goods) -> list:
    """A seeded building's rooms: as its file gives them, or the fewest that hold its fittings and its stores and any free space it
    gives (`free`), all on the ground floor."""
    structure = spec_b.get("structure", "wattle")
    if structure == "camp":
        return [{"kind": "camp", "floor": int(SPACE["camp_floor"]), "storey": 1}]
    if spec_b.get("monument"):
        return []
    given = spec_b.get("rooms")
    if given:
        out = []
        for r in given:
            r = {"kind": r} if isinstance(r, str) else dict(r)
            out.append({"kind": r["kind"], "floor": int(r.get("floor", ROOMS.get(r["kind"], {}).get("floor", 6))),
                        "storey": int(r.get("storey", 1))})
        return out
    free = int(spec_b.get("free", SPACE["seed_free"]))
    b = {"structure": structure, "fittings": fittings, "rooms": []}
    need = fitting_spaces(b) + free
    picked = best_rooms(need, structure)
    for _ in range(6):                                                         # stores that hold by footprint grow with the rooms
        b["rooms"] = [{"kind": k, "floor": int(ROOMS[k]["floor"]), "storey": 1} for k in picked]
        total = fitting_spaces(b) + alloc(b, goods)["floor_spaces"] + free
        if total <= floor(b):
            break
        picked = best_rooms(total, structure)
    return [{"kind": k, "floor": int(ROOMS[k]["floor"]), "storey": 1} for k in picked]


# ---------------------------------------------------------------------- the engine side: what does not fit, reading the lines
def install(w) -> None:
    """What does not fit in a store is left outside its door (02zh §3): after any good comes into a building's store."""
    w.hook("after", "create", lambda w_, call, out: overflow(w_, call["kw"]["dst"], call["kw"]["item"]))
    w.hook("after", "transfer", lambda w_, call, out: overflow(w_, call["kw"]["dst"], call["kw"]["item"]))


def overflow(w, cid, item) -> float:
    c = w.s["containers"].get(cid)
    if not c or c["kind"] != "stock" or c["of"] not in w.s["buildings"]:
        return 0.0
    b = w.s["buildings"][c["of"]]
    if exempt(b) or fits(b, c["goods"]):
        return 0.0
    rest = {i: q for i, q in c["goods"].items() if i != item}
    keep = room_for(b, rest, item) if fits(b, rest) else 0.0
    out = round(float(c["goods"].get(item, 0.0)) - keep, 6)
    if out <= 1e-6:
        return 0.0
    hh = next((cl["claimant"] for cl in w.claims_on(("building", c["of"])) if cl["claimant"] in w.s["institutions"]
               and "withdrawal" in cl["rights"]), None)
    for oid, o in sorted(w.s["buildings"].items()):                          # the household's next store at the place, then the
        if out <= 1e-6 or not hh or oid == c["of"] or o["node"] != b["node"] or o.get("unfinished") or exempt(o):   # door (u5 §4;
            continue                                                                                           # store_rules D3)
        if not o.get("stock") or o["stock"] not in w.s["containers"] or not any(
                cl["claimant"] == hh and "withdrawal" in cl["rights"] for cl in w.claims_on(("building", oid))):
            continue
        k = round(min(out, room_for(o, w.goods(o["stock"]), item)), 6)
        if k > 1e-6:
            w.apply("transfer", b["node"], src=cid, dst=o["stock"], item=item, qty=k)
            out = round(out - k, 6)
    if out <= 1e-6:
        return 0.0
    pile = next((k for k, x in w.s["containers"].items() if x.get("kind") == "pile" and x.get("door") == c["of"] and not x.get("hidden")
                 and x.get("day") == w.d and not x.get("lot")), None)                 # not onto a rack's lot (u4)
    if pile is None:
        pile = w.apply("new_thing", b["node"], node=b["node"], parcel=b["parcel"], kind="pile", by=None, door=c["of"])
    w.apply("transfer", b["node"], src=cid, dst=pile, item=item, qty=out)
    live = [m for m in w.living() if c["of"] in w.homes(m)]
    w.event(b["node"], "left", f"{show_q(out)} {item} would not fit in {b['name']} and lies outside its door", about=[f"building:{c['of']}"],
            salience=0.5, tags=["food"] if item in EDIBLE else [], concerns=live)
    return out


def show_q(q) -> str:
    from cybertron2.engine.world import show
    return show(q)


def spot_words(b, slot) -> str:
    spots = LINES["spots"]["monument" if b.get("monument") else "building"]
    return spots[slot] if slot < len(spots) else f"on the wall ({slot + 1})"


def line_words(b, ln) -> str:
    """'Carved over the door: "..."' (building_lines.md §1): writing in the world, quoted and capped."""
    how = LINES["how"].get(ln.get("how", "paint"), "Written")
    return f"{how} {spot_words(b, int(ln['slot']))} of {b['name']}: “{cap_text(ln['text'], 'line')}”"


def cap_text(text, kind="line") -> str:
    t = " ".join(str(text or "").replace("“", "'").replace("”", "'").replace('"', "'").split())
    words = t.split(" ")
    if len(words) > int(LINES["words"][kind]):
        t = " ".join(words[: int(LINES["words"][kind])])
    return t[: int(LINES["chars"])]


def people_of(w, bid) -> list:
    """Its people: those who hold it, and their households."""
    out = []
    for c in w.claims_on(("building", bid)):
        if c["claimant"] in w.s["institutions"]:
            out += [m for m in w.members(c["claimant"])]
        elif c["claimant"] in w.s["people"]:
            out.append(c["claimant"])
    return sorted(set(out))


def read(w, name, bid, how) -> None:
    """Whoever enters a building (sleeps, works or speaks inside) or attends to it reads its lines that day (D2-169); its people
    notice what was changed since they last read it. Shown in the next morning's message (prompt.written_lines)."""
    b = w.s["buildings"].get(bid)
    if not b or b.get("unfinished") or b.get("condition", 2) <= 0:            # a ruin cannot be read
        return
    m = w.s["mind"][name]
    out = []
    if name in people_of(w, bid):                                              # each change once, the next time they see it
        done = set(m.get("read_changes") or [])
        new = [ch for ch in b.get("changes") or [] if ch.get("by") != name and f"{bid}|{ch['day']}|{ch['text']}" not in done]
        out += [ch["text"] for ch in new]
        m["read_changes"] = (list(m.get("read_changes") or []) + [f"{bid}|{ch['day']}|{ch['text']}" for ch in new])[-40:]
    out += [line_words(b, ln) for ln in sorted(b.get("lines") or [], key=lambda x: int(x["slot"]))]
    if not out:
        return
    log = [x for x in m.get("read") or [] if int(x["day"]) >= w.d - 1]
    have = {(x["day"], x["text"]) for x in log}
    for t in out:
        if (w.d, t) not in have:
            log.append({"day": w.d, "building": bid, "how": how, "text": t})
            have.add((w.d, t))
    m["read"] = log


def entered(w, name) -> set:
    """The buildings one went into or worked at today (D2-169): one's work, making, building, storing or speaking there."""
    out = set()
    for e in w.s.get("events", []):
        if e.get("actor") != name or e.get("day", w.d) != w.d:
            continue
        if e.get("kind") in ("work", "make", "build", "store", "give", "speech", "write"):
            out |= {s[9:] for s in e.get("about") or [] if s.startswith("building:") and s[9:] in w.s["buildings"]}
    return out


def vaulted(b, goods) -> dict:
    """What lies in its vault: safe from fire (D2-49)."""
    out = {}
    for x in alloc(b, goods)["portions"]["portions"]:
        if x["kind"] == "vault":
            out[x["item"]] = out.get(x["item"], 0.0) + x["qty"]
    return out


def stall_share(h, held, head) -> tuple:
    """Beasts housed in winter (D2-45; 02zh §4): the share of a herd its holders' stalls on its parcel take, and the building."""
    best, n = None, 0
    for bid, b in sorted(held.items()):
        if b.get("parcel") != h.get("parcel") or b.get("unfinished") or b.get("condition", 2) <= 0:
            continue
        k = int((b.get("fittings") or {}).get("stalls", 0))
        if k:
            n += k
            best = best or bid
    return (min(1.0, n / float(head)) if head > 0 else 0.0), best
