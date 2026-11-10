"""Brief 4 of the wild layer (proposals/hunt_and_fixes.md §7): the take as a search over time, shelter in levels, the fixes the
gates of briefs 2 and 3 found, and keeping meat at the new scale."""
import copy

from cybertron2.engine import buildings as BL, knowledge as KN, night as N, run as R, things as TH, wild as WL
from cybertron2.engine.data import ITEMS, PHYSICS, TECHNIQUES
from cybertron2.wild import kinds as WK

from tests.test_cybertron2_wild import _do, _hunters, _summer_world, build, generated  # noqa: F401
from tests.test_cybertron2_wild_raiders import _ready


_CACHE = {}


def _built(generated, packs=("wild",)):
    """One built world per pack set, copied for each use (building runs two years of the ecology)."""
    key = tuple(packs)
    if key not in _CACHE:
        _CACHE[key] = build(generated, packs=packs)
    return copy.deepcopy(_CACHE[key])


def _with_people(generated, n=3):
    world = copy.deepcopy(generated)
    world["agents"] = {f"P{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}} for i in range(n)}
    return world


# ---------------------------------------------------------------------------------------------------------------- stage A
def test_the_hunt_has_its_own_hard_curve_and_the_meat_is_on_the_cows_scale():
    assert KN.curve("stalk") == (0.4, 3.0) and KN.curve("hunt the wild") == (0.4, 3.0) and KN.curve("snare") != (0.4, 3.0)
    assert KN.skill_of_practice("stalk", 50) < KN.skill_of_practice("snare", 50) + 1.0      # slower to climb (tau x3)
    goods = {k: (WK.TAKEN[k].get("goods") or {}).get("meat") for k in ("red deer", "roe deer", "wild boar", "brown hare", "eel")}
    assert goods == {"red deer": 20.0, "roe deer": 4.5, "wild boar": 15.0, "brown hare": 0.7, "eel": 0.2}
    assert TECHNIQUES["stalk"]["sweep"] == 0.4 and TECHNIQUES["drive"]["sweep"] == 2.0


def test_a_trip_can_meet_more_than_one_beast_and_ends_when_the_hunter_can_carry_no_more(generated):  # noqa: F811
    w, WL_, wood = _hunters(generated, knows=("stalk",))
    st = w.s["wild"]["state"]
    m = WL.model(w)
    for k in ("roe deer", "red deer"):
        st["pop"][k] = [float(x) * 20 for x in st["pop"][k]]                    # a wood full of deer: several met a trip
    def load(i):
        hands = w.s["containers"][w.s["people"][f"H{i}"]["hands"]]["goods"]
        return sum(float(q) * float((ITEMS.get(it) or {}).get("weight", 1)) for it, q in hands.items() if it in ("meat", "hide"))
    for i in range(30):
        w.s["know"][f"H{i}"]["stalk"]["skill"] = 3.0
    before = {i: load(i) for i in range(30)}
    lines = [_do(w, f"H{i}", {"do": "gather", "what": "stalk", "at": wood, "range": "far", "looking for": "deer"}) for i in range(30)]
    assert any("; then " in r for r in lines)                                  # more than one met on a trip
    for i in range(30):                                                         # nobody brings home more than the foot's carry
        assert load(i) - before[i] <= float(PHYSICS["carry"]["foot"]) + 1e-6
    assert any("could carry no more" in r for r in lines)                      # a red deer ends a lone trip: the rest is left


def test_snow_and_the_summer_leaf_change_finding_deer():
    snow = {r.get("name"): r for r in WK.WHEN["roe deer"]}
    assert snow["tracked in snow"]["detect"] == 1.5 and snow["summer leaf"]["detect"] == 0.8


def test_the_ground_hunted_sets_the_pressure_not_a_flat_share(generated):  # noqa: F811
    w, WL_, wood = _hunters(generated, n=1, knows=("stalk",))
    _do(w, "H0", {"do": "gather", "what": "stalk", "at": wood, "range": "the wood around", "looking for": "deer"})
    m = WL.model(w)
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")
    p = float(((w.s["wild"]["state"].get("pressure") or {}).get("roe deer") or [0] * m.n)[ring])
    ground = float(TECHNIQUES["stalk"]["units"]) * float(TECHNIQUES["stalk"]["sweep"])
    assert p <= float(WK.HUNTED["hunt"]) * ground / float(m.km2[ring]) + float(WK.HUNTED["kill"]) * ground / float(m.km2[ring]) + 1e-6


def test_a_snare_line_is_five_snares_and_an_eel_trap_holds_several(generated):  # noqa: F811
    assert TECHNIQUES["snare"]["set"]["line"] == 5 and TECHNIQUES["snare"]["set"]["holds"] == 1
    assert TECHNIQUES["trap in water"]["set"]["holds"] > 1


def test_a_poisson_draw_has_the_mean_it_is_given():
    import random
    rng = random.Random(3)
    xs = [WL._poisson(rng, 2.0, 50) for _ in range(4000)]
    assert abs(sum(xs) / len(xs) - 2.0) < 0.1 and WL._poisson(rng, 0.0, 5) == 0


# ---------------------------------------------------------------------------------------------------------------- stage B
def _house(w, node="s1"):
    return next(bid for bid, b in sorted(w.s["buildings"].items()) if b["node"] == node and b.get("structure") == "wattle"
                and b.get("stock"))


def test_levels_are_on_with_the_wild_pack_and_off_without(generated):  # noqa: F811
    w = _built(generated)
    assert BL.levels_on(w) and all(b.get("level") is not None for b in w.s["buildings"].values())
    w2 = _built(generated, packs=())
    assert not BL.levels_on(w2) and all(b.get("level") is None for b in w2.s["buildings"].values())


def test_a_wattle_house_wears_in_frost_and_a_gale_can_hole_it(generated):  # noqa: F811
    from cybertron2.engine import environment as EV
    worn = 0
    for k in range(40):
        w = _built(generated)
        bid = _house(w)
        w.cold = lambda at, day=None: True
        for d in range(8):                                                     # a frosty season
            w.s["day"] = 100 * k + d
            N._wear_night(w, bid, w.s["buildings"][bid], w.p)
        worn += BL.level(w.s["buildings"][bid]) <= 4
    assert worn >= 10                                                          # a frosty season wears most wattle a level or so
    holed = 0
    orig = EV.weather
    try:
        EV.weather = lambda w_, at, day=None: "gale"
        for k in range(200):
            w = _built(generated)
            bid = _house(w)
            w.s["day"] = k
            N._wear_night(w, bid, w.s["buildings"][bid], w.p)
            holed += BL.level(w.s["buildings"][bid]) <= 2
    finally:
        EV.weather = orig
    assert holed >= 1                                                          # a gale now and then holes sound wattle in a night


def test_a_shut_worn_house_keeps_the_fox_out_and_a_holed_one_does_not():
    b = {"structure": "wattle", "condition": 2, "level": 4}
    assert not WL.gaps_pass(b, "fox")
    b["level"] = 3
    assert not WL.gaps_pass(b, "fox") and WL.gaps_pass(b, "stoat")             # gappy: the stoat through, not the fox
    b["level"] = 2
    assert WL.gaps_pass(b, "fox")                                              # holed: a hole a fox can use


def test_a_camp_is_flattened_by_a_gale_about_half_the_time(generated):  # noqa: F811
    from cybertron2.engine import environment as EV
    orig = EV.weather
    down = 0
    try:
        EV.weather = lambda w_, at, day=None: "gale"
        for k in range(60):
            w = _built(generated)
            bid = _house(w)
            w.s["buildings"][bid]["structure"] = "camp"
            w.s["buildings"][bid]["level"] = 5
            w.s["day"] = k
            N._wear_night(w, bid, w.s["buildings"][bid], w.p)
            down += BL.level(w.s["buildings"][bid]) == 0
    finally:
        EV.weather = orig
    assert 15 <= down <= 45


def test_mending_raises_a_level(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    bid = next(bid for bid, b in w.s["buildings"].items() if b["node"] == "s1" and b.get("stock"))
    BL.set_level(w, "s1", bid, 3)
    r = _do(w, "P0", {"do": "work", "what": "repair", "at": w.s["buildings"][bid]["name"]})
    for _ in range(4):
        if BL.level(w.s["buildings"][bid]) == 4:
            break
        r = _do(w, "P0", {"do": "work", "what": "repair", "at": w.s["buildings"][bid]["name"]})
    assert BL.level(w.s["buildings"][bid]) == 4, r


# ---------------------------------------------------------------------------------------------------------------- stage C
def test_bins_cut_store_losses_by_about_a_third():
    assert abs(float(WK.STORE_STOPS["bins"]["keep"]) - 0.7) < 1e-9


def test_food_left_out_draws_the_fox_and_rats(generated):  # noqa: F811
    w, _ = _summer_world(generated, kind="fox")
    bid = _house(w)
    cid = w.apply("new_thing", "s1", node="s1", parcel=w.s["buildings"][bid]["parcel"], kind="pile", door=bid, by="x")
    w.apply("create", "s1", dst=cid, item="meat", qty=4.0, why="test")
    row = next(t for t in WK.NEAR_PEOPLE["fox"]["targets"] if t.get("what") == "left out")
    assert [c for c, _ in WL._targets(w, "s1", row)] == [cid]
    WL._food_out_night(w)
    assert (w.s["wild"].get(WK.LEFT_OUT["record"]) or {}).get(bid) == w.d
    before = w.s["containers"][cid]["goods"]["meat"]
    WL._stores(w, "s1", {"rats": 0.05})
    assert w.s["containers"][cid]["goods"]["meat"] < before                   # rats at the door, nothing stopping them


def test_cats_settle_at_a_lower_rate_and_likelier_where_fed():
    assert WK.CAT["settle_p"] == 0.15 and WK.CAT["fed_p"] == 0.4


def test_a_group_fed_at_the_dead_remembers_the_herd_it_saw(generated):  # noqa: F811
    w, _ = _summer_world(generated, kind="wolf")
    m = WL.model(w)
    reach = WL._reach(m, w.s["wild"]["land"], "s1", "far")                     # a pack spread over its range, not crowded into the
    w.s["wild"]["state"]["pop"]["wolf"] = [float(x) * (3.0 if i in reach else 1.0) if float(x) < 1.0 else 0.04   # ring, where the
                                           for i, x in enumerate(w.s["wild"]["state"]["pop"]["wolf"])]          # step kills it off
    herds = [hid for hid, h in w.s["herds"].items() if h.get("node") == "s1" and h.get("parcel")]
    if not herds:
        return
    pid = w.s["herds"][herds[0]]["parcel"]
    cid = TH.leave_carcass(w, "s1", "cow", "the Test herd", [], "other", TECHNIQUES["slaughter"]["yield"]["gives"]["cows"], parcel=pid)
    trow = next(t for t in WK.NEAR_PEOPLE["wolf"]["targets"] if t.get("what") == "carcass")
    _ready(w, "wolf", cid, dict(trow))
    w.s["wild"]["groups"]["wolf@s1"]["parcel"] = pid
    N.night(w)
    g = w.s["wild"]["groups"].get("wolf@s1") or {}
    assert (g.get("seen_herd") or {}).get("hid") in herds


def test_the_carrion_pool_is_a_flow_of_days():
    assert float(WK.CARRION["half_life_days"]) <= 3.0


def test_the_pigeons_raid_takes_their_grazing_not_on_top(generated):  # noqa: F811
    w, _ = _summer_world(generated, kind="woodpigeon")
    field = next(pid for pid, p in sorted(w.s["parcels"].items()) if p["node"] == "s1" and p["cover"] == "field")
    w._flock_budget = {"s1": {"qty": 0.5, "standing": 100.0}}
    g = {"kind": "woodpigeon", "node": "s1", "n": 120, "found": -99, "habit": {}}
    np_ = WL._near("woodpigeon")
    res = WL._raid(w, g, np_, "woodpigeon", {"what": "crop", "trample": 0.0004}, field, field, None, __import__("random").Random(1))
    assert res["lost"] <= 0.5 + 1e-6 and w._flock_budget["s1"]["qty"] >= -1e-9


# ---------------------------------------------------------------------------------------------------------------- stage D
def test_meat_hung_on_a_rack_dries_in_three_nights_and_salt_meat_needs_salt(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    bid = next(bid for bid, b in w.s["buildings"].items() if b["node"] == "s1" and (b.get("fittings") or {}).get("hearth"))
    from cybertron2.engine.here import Here
    h = Here(w, "P0")
    w.s["containers"][h.hands]["goods"]["meat"] = 8.0
    r = _do(w, "P0", {"do": "make", "what": "dry meat", "at": w.s["buildings"][bid]["name"]})
    racks = [cid for cid, c in w.s["containers"].items() if c.get("rack")]
    assert racks and "rack" in r, r
    c = w.s["containers"][racks[0]]
    assert abs(c["goods"].get("drying meat", 0) - 8.0) < 1e-6
    for _ in range(3):
        N.night(w)
        w.s["day"] += 1
    N.night(w)
    assert c["goods"].get("dried meat", 0) > 2.5 and c["goods"].get("drying meat", 0) < 1e-6   # about 4 from 8, less what spoiled
    assert TECHNIQUES["salt meat"]["inputs"] == {"meat": 4, "salt": 1}
