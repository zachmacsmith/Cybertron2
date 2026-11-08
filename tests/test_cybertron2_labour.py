"""Phase 2 of the engine overhaul (D4-103): work costs food, pushing on and fatigue, the walk, skill fading, fittings' wear."""
import copy

from cybertron2.engine import knowledge as KN, labour as LA, needs as NE, night as N, run as R, verbs as V, wear as WE
from cybertron2.engine.data import PHYSICS
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import SEASONS, World, load_spec

SPEC = load_spec("cybertron2/specs/valley_s5.yaml")
ZERO = {"work_food": 0, "guard_food": 0, "over_units": 0, "fade_rate": 0, "step": 0, "wear": False}


def world(labour=None):
    s = copy.deepcopy(SPEC)
    if labour is not None:
        s["physics"] = {"labour": labour}
    w = World(s)
    w.s["today"] = R.blank_today()
    return w


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def test_work_raises_the_nights_need_and_the_least_one_must_eat():
    w = world()
    w.s["today"]["units"] = {"Edric": {"used": 7, "over": 2}}
    w.s["today"]["guards"] = {"Edric": None}
    L = PHYSICS["labour"]
    want = L["work_food"] * (5 + 2 * L["over_food"]) + L["guard_food"]
    assert abs(LA.work_need(w.p, w.s["today"], "Edric") - want) < 1e-9
    base, _ = NE.food(w.p, {"state": "housed", "cold": False})
    more, _ = NE.food(w.p, {"state": "housed", "cold": False, "work": want})
    assert abs(more - base - want) < 1e-9
    assert LA.work_need(world(ZERO).p, w.s["today"], "Edric") == 0.0             # off: the engine before phase 2


def test_eating_the_ration_but_not_the_works_share_is_a_missed_meal():
    w = world()
    n = "Edric"
    for c in w.takeable(n, w.place_of(("person", n))):
        w.s["containers"][c]["goods"] = {}
    w.s["containers"][w.hands(n)]["goods"] = {"bread": 1.05}                     # a ration and a little over
    w.s["today"]["units"] = {n: {"used": 7, "over": 0}}
    rec = N.night(w)
    assert n in rec["missed"]


def test_pushing_on_tires_the_next_day_and_the_walk_adds_up():
    w = world()
    n = "Edric"
    L = PHYSICS["labour"]
    base = w.units_for(n)
    legs = L["free_steps"] + round(1 / L["step"])                               # enough legs past the free ones for a whole unit
    w.s["today"]["route"] = {n: ["p%d" % i for i in range(legs + 1)]}
    LA.close_day(w, w.s["today"], {n: base + 2}, {n: base}, [n])
    assert w.s["people"][n]["tired"] == {"day": w.d + 1, "units": 2 * L["fatigue"] + 1}
    w.s["day"] += 1
    assert w.units_for(n) == max(1, base - 3)
    w2 = world()
    w2.s["today"]["route"] = {n: ["a", "b", "a"]}                                  # to the next parcel and back: free
    LA.close_day(w2, w2.s["today"], {n: base}, {n: base}, [n])
    assert "tired" not in w2.s["people"][n] and "walked" not in w2.s["people"][n]
    w3 = world()
    w3.s["today"]["route"] = {n: ["a", "b", "a", "c", "a"]}                        # two jobs next door: two legs past the free
    LA.close_day(w3, w3.s["today"], {n: base}, {n: base}, [n])
    assert abs(w3.s["people"][n]["walked"] - 2 * L["step"]) < 1e-9
    w0 = world(ZERO)
    w0.s["today"]["route"] = {n: ["p%d" % i for i in range(legs + 1)]}
    LA.close_day(w0, w0.s["today"], {n: base}, {n: base}, [n])
    assert "tired" not in w0.s["people"][n] and "units" not in w0.s["today"] and "walked" not in w0.s["people"][n]


def test_an_unpractised_craft_fades_partly_and_comes_back_quickly():
    w = world()
    n = "Edric"
    L = PHYSICS["labour"]
    k = w.s["know"][n]
    tech = next(t for t, r in k.items() if isinstance(r, dict) and r.get("skill") and r["skill"] > KN.curve(t)[0] + 0.1)
    lo, best = KN.curve(tech)[0], k[tech]["skill"]
    k[tech]["practised"] = 0
    w.s["day"] = int(L["fade_after"] * w.year_days()) - 1
    LA.fade(w)
    assert k[tech]["skill"] == best                                              # not yet: half a year unpractised
    for d in range(int(L["fade_after"] * w.year_days()), 40 * w.year_days()):    # forty years away from it
        w.s["day"] = d
        LA.fade(w)
    floor = lo + L["fade_keep"] * (best - lo)
    assert abs(k[tech]["skill"] - floor) < 0.01 and k[tech]["peak"] == best      # some is lost, never all
    here, mind = Here(w, n), Mind(w, n)
    faded = k[tech]["skill"]
    KN.tried(here, mind, tech, True, units=5)
    back = k[tech]["skill"] - faded
    w2 = world()
    r2 = w2.s["know"][n][tech]
    r2["skill"] = faded                                                           # the same skill, never higher before
    KN.tried(Here(w2, n), Mind(w2, n), tech, True, units=5)
    assert back > (r2["skill"] - faded) * 2                                       # relearning is quicker than learning


def test_a_worn_mill_grinds_half_until_dressed():
    w = world()
    bid = "reed_house"
    b = w.s["buildings"][bid]
    b["fittings"]["millstones"] = 1
    life = WE.FITTINGS["millstones"]["wear"]["life"]
    assert WE.worked(["water wheel"]) == ["water wheel", "millstones"]            # the river turns the same stones
    b["worn"] = {"millstones": {"used": life, "since": 0}}
    assert WE.is_worn(w.p, b, "millstones", w.d, w.year_days())
    assert WE.factor(w.p, b, ["millstones"], w.d, w.year_days()) == 0.5
    assert not WE.is_worn(world(ZERO).p, b, "millstones", w.d, w.year_days())   # off: no wear
    here = Here(w, "Edric")
    WE.mend(here, bid, "millstones")
    assert not WE.is_worn(w.p, w.s["buildings"][bid], "millstones", w.d, w.year_days())


def test_a_leat_silts_with_time():
    w = world()
    b = {"built_day": 0}
    year = w.year_days()
    days = WE.FITTINGS["water wheel"]["wear"]["years"] * year
    assert not WE.is_worn(w.p, b, "water wheel", int(days) - 1, year)
    assert WE.is_worn(w.p, b, "water wheel", int(days) + 1, year)


def test_farming_families_start_with_the_sowing_lore_and_others_do_not():
    from cybertron2.engine import lore as LO, memory as MEM
    w = World(load_spec("cybertron2/specs/wenbridge.yaml"))
    have = {n for n in w.living() if any(x["source"] == "family lore" for x in MEM.kept(w, n)["lines"])}
    holders = LO.farmers(w)
    assert have and all(w.household_of(n) in holders or n in holders for n in have)
    assert {n for n in w.living() if w.household_of(n) not in holders and n not in holders} & have == set()
    s = load_spec("cybertron2/specs/wenbridge.yaml")
    s["lore"] = {"sowing": False}
    w2 = World(s)
    assert not any(x["source"] == "family lore" for n in w2.living() for x in MEM.kept(w2, n)["lines"])
    from cybertron2.engine import prompt as PR
    assert "sown in spring" not in PR.system_prompt(Here(w, "Tom"), Mind(w, "Tom"))   # the rules do not tell it (D4-105)
