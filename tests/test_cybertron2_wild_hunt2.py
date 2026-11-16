"""Brief 4b of the wild layer (proposals/hunt_followups.md §6): game that remembers (wariness learned and slow to fade, the history's
take by distance from the villages), recovery with a lag from the woods around, births through the season for fast breeders, carrion
drawing its eaters; and bringing a kill home: declared hunting parties, the catch split by carry, a led beast."""
import copy

import numpy as np

from cybertron2.engine import parties as HP, verbs as V, wild as WL
from cybertron2.engine.data import TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.wild import ecology as EC, kinds as WK

from tests.test_cybertron2_wild import _do, _hunters, build, generated  # noqa: F401


_CACHE = {}


def _built(generated):
    if "w" not in _CACHE:
        _CACHE["w"] = build(generated)
    return copy.deepcopy(_CACHE["w"])


def _land_step(w, st, days, day0=None, history=False):
    m = WL.model(w)
    k0 = WL.eco_day(w) if day0 is None else day0
    for d in range(days):
        EC.step(m, st, k0 + d, WL.weather(w, sorted(set(m.nodes)), w.d + d), WL.draws(w, k0 + d), history=history)


# ---------------------------------------------------------------------------------------------------------------- stage A
def test_peoples_presence_falls_with_distance_not_by_the_areas_kind(generated):  # noqa: F811
    w = _built(generated)
    m = WL.model(w)
    land = w.s["wild"]["land"]
    homes = [i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "home"]
    assert min(m.busy[i] for i in homes) > 0.8
    import math
    hx = [land["areas"][m.ids[i]]["xy_km"] for i in homes]
    d = [min(math.dist(land["areas"][a]["xy_km"], h) for h in hx) for a in m.ids]
    wild = [i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "wild"]
    near = [i for i in wild if d[i] < 4]
    far = [i for i in wild if d[i] > 12]
    assert near and far and min(m.busy[i] for i in near) > max(m.busy[i] for i in far)   # the wild near a village is busier


def test_at_day_0_game_near_a_village_is_thinner_and_warier_than_a_days_walk_out(generated):  # noqa: F811
    w = _built(generated)
    m = WL.model(w)
    st = w.s["wild"]["state"]
    near = [i for i in range(m.n) if m.busy[i] > 0.3]
    out = [i for i in range(m.n) if m.busy[i] < 0.05]
    for k in ("roe deer", "red deer"):
        hab = EC.suitability(m.f, m.kinds[k])                                       # the land's own habitat, before people
        per = lambda idx: sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in idx) / max(1e-9, sum(float(hab[i]) * float(m.km2[i]) for i in idx))
        wary = lambda idx: sum(float(st["wary"][k][i]) * float(m.km2[i]) for i in idx) / sum(float(m.km2[i]) for i in idx)
        assert per(near) < per(out), k                                             # thinner for the habitat there
        assert wary(near) > 5 * max(wary(out), 0.01), k                             # and warier


def test_wariness_fades_with_a_half_life_of_about_a_year(generated):  # noqa: F811
    w = _built(generated)
    st = copy.deepcopy(w.s["wild"]["state"])
    st["wary"]["roe deer"] = [2.0] * WL.model(w).n
    _land_step(w, st, w.year_days())
    assert 0.8 <= float(np.mean(st["wary"]["roe deer"])) <= 1.2                  # about half after 32 days, no take in the run


def test_daily_hunting_raises_wariness(generated):  # noqa: F811
    w, WL_, wood = _hunters(generated, n=1, knows=("stalk",))
    m = WL.model(w)
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")
    before = float(w.s["wild"]["state"]["wary"]["roe deer"][ring])
    for _ in range(4):
        _do(w, "H0", {"do": "gather", "what": "stalk", "at": wood, "range": "the wood around"})
    assert float(w.s["wild"]["state"]["wary"]["roe deer"][ring]) > before


def test_a_kind_that_keeps_a_home_range_refills_a_halved_wood_slowly_at_first(generated):  # noqa: F811
    w = _built(generated)
    m = WL.model(w)
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")

    def inflow(fidelity, days):
        kinds = copy.deepcopy(WK.KINDS)
        kinds["roe deer"]["fidelity"] = fidelity
        mm = EC.Model(land, kinds=kinds, Y=w.year_days(), knobs=m.knobs)
        st = copy.deepcopy(w.s["wild"]["state"])
        st0 = float(st["pop"]["roe deer"][ring])
        p = list(st["pop"]["roe deer"]); p[ring] *= 0.5; st["pop"]["roe deer"] = p
        k0 = WL.eco_day(w)
        for d in range(days):
            EC.step(mm, st, k0 + d, WL.weather(w, sorted(set(mm.nodes)), w.d + d), WL.draws(w, k0 + d))
        return float(st["pop"]["roe deer"][ring]) / st0
    assert inflow(0.8, 3) < inflow(0.0, 3)                                        # few come in in the first days


def test_fast_breeders_give_birth_through_the_season_and_once_a_year_breeders_in_a_burst():
    assert WK.KINDS["rats"]["litters"] == "through" and WK.KINDS["roe deer"]["litters"] == "burst"
    land = {"km": 0.15, "areas": {"a0": {"kind": "wild", "node": "s1", "km2": 10.0, "xy_km": [0, 0], "cover": {"pasture": 5.0, "forest": 5.0},
                                         "eco": {}, "old_wood_km2": 0, "wet": 0.2, "elevation": 50, "temp": 9, "rock": 0, "river_km": 0,
                                         "big_river_km": 0, "lake_km2": 0}}, "links": [], "home": {}}
    m = EC.Model(land, Y=32)
    st = m.initial()
    wx = {"s1": {"temp": 10.0, "low": 4.0, "rain": 3.0, "snow": False}}
    seen = {"brown hare": [], "roe deer": []}
    for d in range(4):                                                           # the first days of spring
        before = {k: float(st["pop"][k][0]) for k in seen}
        EC.step(m, st, d, wx, {"mast": 0.5})
        for k in seen:
            seen[k].append(float(st["pop"][k][0]) / max(before[k], 1e-12))
    assert all(x > 1.0 for x in seen["brown hare"])                            # born each day
    assert seen["roe deer"][0] > 1.2 and all(x < 1.0 for x in seen["roe deer"][1:])   # born on the first day only


def test_carrion_lying_in_an_area_draws_its_eaters(generated):  # noqa: F811
    w = _built(generated)
    m = WL.model(w)
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")

    def after(extra):
        st = copy.deepcopy(w.s["wild"]["state"])
        c = list(st["carrion"]); c[ring] += extra; st["carrion"] = c
        _land_step(w, st, 1)
        return float(st["pop"]["raven"][ring]), float(st["pop"]["wolf"][ring])
    r0, w0 = after(0.0)
    r1, w1 = after(2000.0)
    assert r1 > r0 and w1 > w0


def test_no_kind_is_named_in_the_party_code():
    src = open("cybertron2/engine/parties.py").read().lower()
    assert not any(k in src for k in WK.KINDS if len(k) > 3)


# ---------------------------------------------------------------------------------------------------------------- stage B
def _party_world(generated, n=3):
    w, WL_, wood = _hunters(generated, n=n, knows=("stalk", "drive", "hunt the wild"))
    for i in range(n):
        w.s["containers"][w.s["people"][f"H{i}"]["hands"]]["goods"]["crude weapon"] = 1
        w.s["know"][f"H{i}"]["stalk"]["skill"] = 3.0
    return w, wood


def _deer_hunt(w, names, ox=None, day=0):
    """One red-deer stalk far out by these hunters (a wood thick with naive red deer), as a party led by the first."""
    st = w.s["wild"]["state"]
    st["pop"]["red deer"] = [float(x) * 40 for x in st["pop"]["red deer"]]
    st["wary"]["red deer"] = [0.0] * len(st["wary"]["red deer"])
    w.s["day"] = day
    wood = next(p for p, x in w.s["parcels"].items() if x["node"] == "s1" and x["cover"] == "forest")
    y = dict(TECHNIQUES["stalk"]["yield"], takes={"red deer": 1.0})
    ms = [WL.member(Here(w, n), Mind(w, n), Here(w, n).hands, 3.0, float(TECHNIQUES["stalk"]["units"]), ox if j == 0 else None)
          for j, n in enumerate(names)]
    a = {"do": "gather", "what": "stalk", "range": "far", "_mods": {"range": "far", "_ox": ox}}
    return WL.hunt(Here(w, names[0]), ms, "stalk", wood, "the wood", y, a)


def test_a_party_of_three_brings_a_red_deer_home_whole_and_one_alone_leaves_most_of_it(generated):  # noqa: F811
    w0, _ = _party_world(generated)
    whole = alone = None
    for day in range(30):
        r = _deer_hunt(copy.deepcopy(w0), ["H0", "H1", "H2"], day=day)
        if "took it" in r["lines"]["H0"] and whole is None:
            whole = r
        r1 = _deer_hunt(copy.deepcopy(w0), ["H0"], day=day)
        if "took it" in r1["lines"]["H0"] and alone is None:
            alone = r1
        if whole and alone:
            break
    assert whole and alone
    first = whole["lines"]["H0"].split("took it: ")[1].split(";")[0]
    assert "20 meat" in first, whole["lines"]["H0"]                              # three hands carry it all
    assert sum(whole["food"].values()) >= 20 - 1e-6
    assert 8 <= alone["food"]["H0"] <= 10 and "left" in alone["lines"]["H0"], alone["lines"]["H0"]


def test_hunting_the_same_wood_without_a_party_makes_no_crew_and_the_second_finds_it_harder(generated):  # noqa: F811
    w, wood = _party_world(generated, n=2)
    plans = {n: [{"do": "gather", "what": "stalk", "at": wood, "range": "the wood around"}] for n in ("H0", "H1")}
    assert HP.resolve(w, plans) == {} and not w.s["today"].get("parties")
    m = WL.model(w)
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")
    p0 = float(((w.s["wild"]["state"].get("pressure") or {}).get("roe deer") or [0.0] * m.n)[ring])
    _do(w, "H0", plans["H0"][0])
    assert float(w.s["wild"]["state"]["pressure"]["roe deer"][ring]) > p0      # the first disturbs the game the second hunts


def test_hunt_with_follows_the_leaders_way_and_with_no_leader_one_hunts_alone(generated):  # noqa: F811
    w, wood = _party_world(generated, n=4)
    lead = {"do": "gather", "what": "stalk", "at": wood, "range": "far", "looking for": "deer"}
    plans = {"H0": [dict(lead)], "H1": [{"do": "gather", "what": "hunt the wild", "at": wood, "with": "H0"}],
             "H2": [{"do": "gather", "what": "hunt the wild", "at": wood, "with": "H9"}]}
    HP.resolve(w, plans)
    f = plans["H1"][0]
    assert f["what"] == "stalk" and f["range"] == "far" and f["looking for"] == "deer" and f["_party"] == "H0"
    assert f["_own"]["what"] == "hunt the wild"                                 # its own settings kept as the fallback
    assert "_party" not in plans["H2"][0] and "H2" not in w.s["today"]["parties"]   # nobody of that name hunting: alone


def test_a_chain_follows_to_its_leader_and_a_circle_to_its_better_hunter(generated):  # noqa: F811
    w, wood = _party_world(generated, n=4)
    act = lambda x=None, what="stalk": {"do": "gather", "what": what, "at": wood, **({"with": x} if x else {})}
    plans = {"H0": [act("H1")], "H1": [act("H2")], "H2": [act()]}
    HP.resolve(w, plans)
    assert w.s["today"]["parties"] == {"H0": "H2", "H1": "H2", "H2": "H2"}
    w.s["know"]["H1"]["stalk"]["skill"] = 3.0
    w.s["know"]["H0"]["stalk"]["skill"] = 1.0
    plans = {"H0": [act("H1")], "H1": [act("H0")]}
    HP.resolve(w, plans)
    assert w.s["today"]["parties"] == {"H0": "H1", "H1": "H1"}


def test_a_leader_takes_followers_unless_it_hunts_alone_or_names_only_some(generated):  # noqa: F811
    w, wood = _party_world(generated, n=3)
    act = lambda **k: {"do": "gather", "what": "stalk", "at": wood, **k}
    HP.resolve(w, {"H0": [act(alone=True)], "H1": [act(**{"with": "H0"})]})
    assert not w.s["today"].get("parties")
    HP.resolve(w, {"H0": [act(only="H2")], "H1": [act(**{"with": "H0"})], "H2": [act(**{"with": "H0"})]})
    assert w.s["today"]["parties"] == {"H0": "H0", "H2": "H0"}


def test_a_party_hunt_is_settled_once_after_the_acts_and_replays_exactly(generated):  # noqa: F811
    w0, wood = _party_world(generated, n=2)

    def day(w):
        plans = {"H0": [{"do": "gather", "what": "stalk", "at": wood, "range": "the wood around"}],
                 "H1": [{"do": "gather", "what": "stalk", "at": wood, "with": "H0"}]}
        HP.resolve(w, plans)
        words = {n: V.do(Here(w, n), Mind(w, n), plans[n][0]) for n in ("H0", "H1")}
        return words, HP.settle(w)
    w1, w2 = copy.deepcopy(w0), copy.deepcopy(w0)
    words, res = day(w1)
    assert all("day's end" in x for x in words.values())                        # nothing known until the day's end
    assert set(res) == {"H0", "H1"} and "with H1" in res["H0"][0] and "with H0" in res["H1"][0]
    assert day(w2)[1] == res and w1.s["wild"]["state"] == w2.s["wild"]["state"]


def test_a_follower_with_fewer_units_turns_back_and_knows_only_what_came_before(generated):  # noqa: F811
    w0, _ = _party_world(generated, n=2)
    found = None
    for d in range(40):
        w = copy.deepcopy(w0)
        st = w.s["wild"]["state"]
        st["pop"]["red deer"] = [float(x) * 40 for x in st["pop"]["red deer"]]
        w.s["day"] = d
        wood = next(p for p, x in w.s["parcels"].items() if x["node"] == "s1" and x["cover"] == "forest")
        y = dict(TECHNIQUES["stalk"]["yield"], takes={"red deer": 1.0})
        ms = [WL.member(Here(w, "H0"), Mind(w, "H0"), Here(w, "H0").hands, 3.0, 3.0),
              WL.member(Here(w, "H1"), Mind(w, "H1"), Here(w, "H1").hands, 3.0, 1.0)]
        r = WL.hunt(Here(w, "H0"), ms, "stalk", wood, "the wood", y, {"do": "gather", "what": "stalk", "_mods": {"range": "far"}})
        if "H1 turned back" in r["lines"]["H0"] and r["lines"]["H0"].count("came on") > r["lines"]["H1"].count("came on"):
            found = r
            break
    assert found, "no trip with meetings after the follower turned back"
    assert "you turned back for home" in found["lines"]["H1"]
    assert HP.cost(Here(w0, "H1"), {"do": "gather", "what": "stalk", "range": "far", "_party": "H0"}, 6, 4) == 4   # the walk and a unit


def test_a_drive_needs_a_party(generated):  # noqa: F811
    w, wood = _party_world(generated, n=1)
    r = _do(w, "H0", {"do": "gather", "what": "drive", "at": wood})
    assert r.startswith("Refused") and "others" in r


def test_a_led_ox_lets_one_hunter_bring_a_red_deer_home_and_costs_a_unit(generated):  # noqa: F811
    w0, wood = _party_world(generated, n=1)
    a = {"do": "gather", "what": "stalk", "at": wood, "range": "far"}
    assert V.cost(Here(w0, "H0"), dict(a, lead="the ox")) == V.cost(Here(w0, "H0"), a) + 1
    got = None
    for day in range(30):
        r = _deer_hunt(copy.deepcopy(w0), ["H0"], ox="an ox", day=day)
        if "took it" in r["lines"]["H0"]:
            got = r
            break
    assert got and got["food"]["H0"] >= 20 - 1e-6, got
    assert float(WK.LEAD["seen"]) < 1.0 and float(WK.LEAD["flee"]) > 0.0       # the game knows the party sooner
