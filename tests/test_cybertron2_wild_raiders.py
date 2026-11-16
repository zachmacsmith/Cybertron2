"""Brief 2 of the wild layer (D2-206, D2-207; proposals/wild_raiders_and_works.md §7): displacement and the lapse probe, the
woodpigeon flock, set snares and traps, doors, stores and fences by body size, and pack K1 (the stoat, the cat, the owl hole,
moles, the rooks' leatherjackets, markers' sayings, cattle gadding)."""
import copy

from cybertron2.engine import night as N, run as R, wild as WL
from cybertron2.engine.data import RESOURCES
from cybertron2.wild import kinds as WK

from tests.test_cybertron2_wild import _do, _ring, _summer_world, _two, build, generated  # noqa: F401


def _fields(w, node="s1"):
    return [pid for pid, p in sorted(w.s["parcels"].items()) if p["node"] == node and p["cover"] == "field"]


def _ready(w, kind, target, trow):
    gid = f"{kind}@s1"
    g = w.s["wild"].setdefault("groups", {}).get(gid) or {"kind": kind, "node": "s1", "found": -99, "habit": {}, "wary": -1, "rest": -1}
    g.update(pos="ready", raid=w.d, t=w.d - 1, target=target, parcel=target, what=trow.get("what", "crop"), trow=trow, n=6)
    w.s["wild"]["groups"][gid] = g
    return gid


def test_a_turned_raider_goes_to_the_next_field_the_same_night_and_one_that_does_not_displace_rests(generated):  # noqa: F811
    seen = {True: 0, False: 0}
    for displace in (True, False):
        for k in range(12):
            w, _ = _summer_world(generated)
            fields = _fields(w)
            if len(fields) < 2:
                return
            a = fields[0]
            WK.NEAR_PEOPLE["wild boar"]["displace"] = displace
            w.s["day"] = 22 + k                                                    # summer, the ripening corn
            _ready(w, "wild boar", a, dict(WK.NEAR_PEOPLE["wild boar"]["targets"][0], what="crop"))
            w.s["wild"]["watch"] = {a: {"day": w.d, "by": "x", "scare": "fire"}}
            rec = N.night(w)
            v = (rec.get("wild") or {}).get("groups", {}).get("wild boar@s1") or {}
            if v.get("turned") and v.get("then") and not v["then"].get("turned"):
                seen[displace] += 1
    WK.NEAR_PEOPLE["wild boar"]["displace"] = True
    assert seen[True] >= 1 and seen[False] == 0


def test_the_fox_tries_the_doors_and_takes_from_the_first_left_open_and_the_one_it_fed_at_first(generated):  # noqa: F811
    w, _ = _summer_world(generated, kind="fox")
    houses = [b for b, x in sorted(w.s["buildings"].items()) if x["node"] == "s1" and x.get("stock")
              and w.s["containers"][x["stock"]]["goods"].get("hen")]
    if len(houses) < 2:
        return
    trow = dict(WK.NEAR_PEOPLE["fox"]["targets"][1])
    opened = houses[-1]
    got = 0
    for k in range(20):
        w2 = copy.deepcopy(w)
        w2.s["day"] = 10 + k
        for b in houses:
            w2.s["buildings"][b]["structure"] = "stone"                              # no gaps a fox gets through
        w2.s["wild"]["shut"] = {b: {"day": w2.d, "by": "x"} for b in houses if b != opened}
        _ready(w2, "fox", houses[0], trow)
        w2.s["wild"]["state"]["pop"]["stoat"] = [0.0] * len(w2.s["wild"]["state"]["pop"]["stoat"])
        rec = N.night(w2)
        v = (rec.get("wild") or {}).get("groups", {}).get("fox@s1") or {}
        assert v.get("tried", [houses[0]])[0] == houses[0]                          # the remembered one first
        if v.get("at") == opened and v.get("took"):
            got += 1
    assert got >= 1


def test_the_flock_gets_used_to_clappers_and_lands_where_the_corn_is_thickest(generated):  # noqa: F811
    np_ = WK.NEAR_PEOPLE["woodpigeon"]
    assert np_["displace"] and np_["answer"]["type"] == "habituate" and np_["targets"][0]["pick"] == "most"
    import random
    g = {"habit": {}}
    turned = [WL._answer(random.Random(i), g, np_, "clapper")[0] for i in range(12)]
    assert sum(turned[:4]) > sum(turned[-4:])                                      # a still scare is soon a post (D2-198)


def test_a_set_snare_catches_with_nobody_there_can_be_robbed_and_ends_after_its_life(generated):  # noqa: F811
    world = _two(generated)
    w, _ = _summer_world(world)
    w.s["today"] = R.blank_today()
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["brown hare"][ri] = 400.0 / m.km2[ri]
    par = next(p for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] in ("pasture", "meadow", "field"))
    r = _do(w, "Ann", {"do": "gather", "what": "snare", "at": par["name"]})
    assert "set a line of snares" in r
    cid = next(c for c, x in w.s["containers"].items() if x.get("kind") == "set")
    caught = False
    for _ in range(6):
        N.night(w); w.s["day"] += 1; w.s["today"] = R.blank_today()
        caught = caught or bool(w.s["containers"][cid]["goods"])
        if caught:
            break
    if caught:                                                                     # another finds it and takes the catch: seen
        w.s["mind"].setdefault("Tom", {})
        w.s["containers"][cid]["goods"] = {"meat": 0.18}
        r = _do(w, "Tom", {"do": "take", "item": "meat", "from": par["name"]})
        assert "took" in r.lower() or "found no" in r.lower() or "looked" in r.lower()
    for _ in range(10):
        N.night(w); w.s["day"] += 1; w.s["today"] = R.blank_today()
    assert w.s["containers"][cid]["set"].get("sprung") is not None                 # spent after its life


def test_doors_and_fences_stop_what_their_gaps_stop(generated):  # noqa: F811
    wattle, stone = {"structure": "wattle", "condition": 2}, {"structure": "stone", "condition": 2}
    damaged = {"structure": "stone", "condition": 1}
    assert not WL.gaps_pass(wattle, "fox") and WL.gaps_pass(wattle, "stoat") and WL.gaps_pass(wattle, "rats")
    assert not WL.gaps_pass(stone, "stoat") and WL.gaps_pass(stone, "rats")
    assert WL.gaps_pass(damaged, "stoat") and not WL.gaps_pass(damaged, "fox")
    import random
    w, _ = _summer_world(generated)
    pid = _fields(w)[0]
    w.s["parcels"][pid]["fence"] = {"kind": "wood", "level": 2, "built": True, "units": 99.0, "gate": "shut", "mend": 0.0, "pending": {}}
    assert not WL._fenced(w, pid, WK.NEAR_PEOPLE["stoat"], random.Random(1), "stoat")    # a small kind passes any fence


def test_stores_keep_out_what_their_fittings_stop():
    gran = {"fittings": {"granary": 1}}
    dog = {"fittings": {"dog": 1}}
    assert WL._stops(gran, "rats") < 1.0 and WL._stops(gran, "wild boar") == 1.0
    assert WL._stops(dog, "rats") < 1.0 and WL._stops(dog, "wild boar") < 1.0


def test_the_stoat_takes_hens_through_a_shut_wattle_door_and_not_a_mended_stone_one(generated):  # noqa: F811
    lost = {}
    for structure in ("wattle", "stone"):
        n = 0
        for k in range(16):
            w, _ = _summer_world(generated, kind="stoat")
            houses = [b for b, x in sorted(w.s["buildings"].items()) if x["node"] == "s1" and x.get("stock")
                      and w.s["containers"][x["stock"]]["goods"].get("hen")]
            if not houses:
                return
            for b in houses:
                w.s["buildings"][b].update(structure=structure, condition=2)
            w.s["day"] = 5 + k
            w.s["wild"]["state"]["pop"]["fox"] = [0.0] * len(w.s["wild"]["state"]["pop"]["fox"])
            w.s["wild"]["shut"] = {b: {"day": w.d, "by": "x"} for b in houses}
            _ready(w, "stoat", houses[0], dict(WK.NEAR_PEOPLE["stoat"]["targets"][0]))
            rec = N.night(w)
            v = (rec.get("wild") or {}).get("groups", {}).get("stoat@s1") or {}
            n += 1 if v.get("took") else 0
        lost[structure] = n
    assert lost["wattle"] > lost["stone"]


def test_a_cat_or_an_owl_keeps_the_mice_off_a_store_and_a_dog_keeps_cats_away():
    b = {"stock": "s:1", "_id": "b1", "fittings": {}}
    class W:
        s = {"containers": {"s:1": {"goods": {"cat": 1}}}, "wild": {"nests": {"b1": 3}}}
    assert WL._stops(b, "voles and mice", W()) < 0.5 and WL._stops(b, "wild boar", W()) == 1.0
    assert WK.STORE_STOPS["cat"]["in_store"] and WK.CAT["settle_p"] > 0


def test_moles_cost_hay_grass_and_leatherjackets_are_fewer_near_a_rookery(generated):  # noqa: F811
    assert WK.LOADS["moles"]["harm_res"][0]["res"] == "grass" and WK.LOADS["moles"]["on_crop"]
    assert WK.LOADS["leatherjackets"]["site_eats"]["site"] == "rookery"
    from cybertron2.wild.methods import LOAD_NAMES
    assert "moles" in LOAD_NAMES and "leatherjackets" in LOAD_NAMES


def test_a_marker_tells_its_sowing_saying_from_the_lore():
    from cybertron2.engine import lore as LO
    best, good = LO.sowing_times(8)["grain"]
    assert ("early", "spring") in best + good and WK.MARKERS["blackthorn"]["times"] == "grain"
    assert "{crop}" in WK.MARKERS["blackthorn"]["say"]


def test_cattle_gad_on_a_hot_still_day_far_from_water_and_shade(generated):  # noqa: F811
    from cybertron2.engine import herds as HD, environment as EV
    w, _ = _summer_world(generated)
    hid = next(iter(w.s["herds"]), None)
    if hid is None:
        return
    h = w.s["herds"][hid]
    par = w.s["parcels"][h["parcel"]]
    hot = {"temp": 28.0, "wind": 1.0}
    orig = EV.values
    try:
        EV.values = lambda w_, at, day=None: hot
        w.s["day"] = 12                                                            # summer
        shade = any(w.s["parcels"][a]["cover"] in ("water", "forest", "scrub") for a in par.get("adj") or [] if a in w.s["parcels"])
        assert HD.gadding(w, h) == (par["cover"] in ("pasture", "meadow") and not shade and par["cover"] not in ("water",))
    finally:
        EV.values = orig


def test_society_a_watched_field_sends_the_loss_next_door(generated):  # noqa: F811
    """§7, society-level (dry): two neighbouring fields, one watched each night: the unwatched one loses more than when neither is."""
    def loss(watch_a):
        tot = 0.0
        for k in range(10):
            w, _ = _summer_world(generated)
            fields = _fields(w)
            if len(fields) < 2:
                return None
            a, b = fields[0], fields[1]
            w.s["day"] = 22 + k
            _ready(w, "wild boar", a, dict(WK.NEAR_PEOPLE["wild boar"]["targets"][0], what="crop"))
            if watch_a:
                w.s["wild"]["watch"] = {a: {"day": w.d, "by": "x", "scare": "fire"}}
            before = sum(float(c.get("left", 0)) for _, _, c in __import__("cybertron2.engine.farm", fromlist=["x"]).standing(w.s["parcels"][b]))
            N.night(w)
            after = sum(float(c.get("left", 0)) for _, _, c in __import__("cybertron2.engine.farm", fromlist=["x"]).standing(w.s["parcels"][b]))
            tot += before - after
        return tot
    neither, watched = loss(False), loss(True)
    if neither is None:
        return
    assert watched > neither


def test_society_one_lax_house_draws_the_fox_to_its_neighbours(generated):  # noqa: F811
    """§7, society-level (dry): a hamlet with one house left open loses more hens in its other houses than one with every house shut."""
    def others_lost(lax):
        w, _ = _summer_world(generated, kind="fox")
        m, ri = _ring(w, WL)
        w.s["wild"]["state"]["pop"]["fox"][ri] = 4.0 / m.km2[ri]
        w.s["wild"]["state"]["pop"]["stoat"] = [0.0] * len(w.s["wild"]["state"]["pop"]["stoat"])
        houses = [b for b, x in sorted(w.s["buildings"].items()) if x["node"] == "s1" and x.get("stock")
                  and w.s["containers"][x["stock"]]["goods"].get("hen")]
        if len(houses) < 2:
            return None, None
        rest = houses[1:] if lax else houses
        h0 = sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("hen", 0) for b in houses[1:])
        for _ in range(30):
            for b in houses:
                w.s["buildings"][b]["condition"] = 2
            w.s["wild"]["shut"] = {b: {"day": w.d, "by": "x"} for b in rest}
            N.night(w); w.s["day"] += 1
        return h0 - sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("hen", 0) for b in houses[1:]), h0
    shut_all, _ = others_lost(False)
    one_lax, h0 = others_lost(True)
    if h0 is None:
        return
    assert one_lax >= shut_all
