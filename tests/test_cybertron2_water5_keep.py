"""Build brief 5 §4a, §4b, §4c (proposals/river_and_water.md; D2-209): the smokehouse, salt boiled from a brine spring, fuel drawn
from the same stores. The smokehouse on the valley world (meat) and the river world (fish); salt on the river world (37.2's, with
Saltwell's brine spring) and on a world with a spring placed by hand."""
import copy

from cybertron2.engine import agreements as AG, keeping as KP, knowledge as KN, night as N, prompt as PR, run as R, verbs as V
from cybertron2.engine.data import ITEMS, PHYSICS, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

VALLEY = load_spec("cybertron2/specs/valley_s5.yaml")
RIVER = load_spec("cybertron2/specs/water/river.yaml")
COAST = load_spec("cybertron2/specs/fishing/water.yaml")


def world(spec, buildings=None, **patch):
    s = copy.deepcopy(spec)
    s.update(patch)
    s["buildings"].update(buildings or {})
    w = World(s)
    w.s["today"] = R.blank_today()
    return w


def smokehouse(parcel="mb_green", household="Reed", structure="wattle", wood=10, **kw):
    return {"smokehouse": {"parcel": parcel, "household": household, "structure": structure, "name": "the Smokehouse",
                           "fittings": {"smoke racks": 1}, "stock": {"firewood": wood} if wood else {}, **kw}}


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def hand(w, who, **goods):
    w.s["containers"][w.hands(who)]["goods"].update({k.replace("_", " "): float(v) for k, v in goods.items()})


def store(w, bid):
    return w.s["containers"][w.s["buildings"][bid]["stock"]]["goods"]


def racks(w, bid=None):
    return {cid: c for cid, c in w.s["containers"].items() if c.get("rack") and (bid is None or c.get("in") == bid)}


def night(w):
    rec = N.night(w)
    w.s["day"] += 1
    w.s["today"] = R.blank_today()
    return rec


def fed(w, household):
    """Its people fed from their hands, so the night's meal leaves the stores and racks alone."""
    for who in w.living():
        if w.household_of(who) == household:
            hand(w, who, bread=30)


AUTUMN = {"season": "autumn", "day": 1, "season_days": 8}


def river_places():
    """The river world's spring and who is about it, found from the world (the generator places them): the spring's parcel and
    node, the household holding it, its first adult (the salter), its dwelling, and an adult of another household there."""
    w = World(copy.deepcopy(RIVER))
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if "brine" in x["res"])
    node = w.s["parcels"][pid]["node"]
    hh = next(c["claimant"] for c in w.claims_on(("parcel", pid)) if c["claimant"] in w.s["institutions"])
    adults = [n for n in sorted(w.living()) if w.s["people"][n]["stage"] == "adult" and w.s["people"][n]["at"] == node]
    house = next(b for b in w.homes(next(n for n in adults if w.household_of(n) == hh)) if w.s["buildings"][b]["fittings"].get("beds"))
    return {"spring": pid, "node": node, "household": hh, "salter": next(n for n in adults if w.household_of(n) == hh),
            "house": house, "house_name": w.s["buildings"][house]["name"], "house_parcel": w.s["buildings"][house]["parcel"],
            "neighbour": next(n for n in adults if w.household_of(n) != hh)}


RP = river_places()


# ---------------------------------------------------------------------- §4a.6: a glut kept, and not
def test_a_40_meat_glut_loses_under_10_percent_through_a_smokehouse():
    w = world(VALLEY, smokehouse(), calendar=AUTUMN)
    fed(w, "Reed")
    hand(w, "Odo", meat=40)
    r = do(w, "Odo", do="make", what="smoke meat")
    assert "40 smoking meat" in r and "smoke racks in the Smokehouse for 3 nights of fire" in r, r
    for d in range(3):
        if d:
            assert "You tended the fire" in do(w, "Odo", do="work", what="tend the smoke")
        night(w)
    smoked = store(w, "smokehouse").get("smoked meat", 0.0)
    assert 18.0 < smoked < 20.0, smoked                                        # half the weight, less the smoked rate's loss
    assert 1 - smoked / 20.0 < 0.10
    assert abs(store(w, "smokehouse").get("firewood", 0) - 7.0) < 1e-6        # 1 firewood a night of fire


def test_a_40_meat_glut_loses_far_more_with_only_the_hearth_rack():
    w = world(VALLEY, calendar=AUTUMN)
    fed(w, "Reed")
    store(w, "reed_house").update({"meat": 40.0})
    for d in range(12):                                                        # a batch of 8 every 3 nights, as the rack allows
        if KN.available(Here(w, "Odo"), "meat") > 1e-6:
            do(w, "Odo", do="make", what="dry meat")
        night(w)
    kept = sum(c["goods"].get("dried meat", 0) for c in racks(w).values()) + store(w, "reed_house").get("dried meat", 0)
    lost = 1 - 2 * kept / 40.0
    assert 0.18 < lost < 0.40, lost                                           # about 23% in autumn, 30% in summer: the store's
                                                                              # fresh rate (9% a night) as built, not the brief's half


def test_the_hearth_rack_holds_a_batch_at_a_time():
    w = world(VALLEY)
    w.s["buildings"]["hale_house"]["door"] = "barred"                         # no other hearth he may use
    hand(w, "Odo", meat=20)
    do(w, "Odo", do="make", what="dry meat")
    r = do(w, "Odo", do="make", what="dry meat")
    assert r.startswith("Refused") and "full" in r and "another batch goes up when this one is done" in r, r
    assert abs(w.goods(w.hands("Odo"))["meat"] - 12.0) < 1e-9


def test_fish_smoke_in_the_river_world_and_keep_four_times_as_long_as_dried_meat():
    w = world(RIVER, smokehouse(parcel=RP["house_parcel"], household=RP["household"]), calendar=AUTUMN)
    fed(w, RP["household"])
    hand(w, RP["salter"], fish=40)
    assert "40 smoking fish" in do(w, RP["salter"], do="make", what="smoke fish")
    for d in range(3):
        if d:
            do(w, RP["salter"], do="work", what="tend the smoke")
        night(w)
    assert 1 - store(w, "smokehouse").get("smoked fish", 0.0) / 20.0 < 0.10
    assert abs(ITEMS["smoked fish"]["spoil"] * 4 - ITEMS["dried meat"]["spoil"]) < 1e-12
    assert abs(ITEMS["smoked meat"]["spoil"] * 4 - ITEMS["dried meat"]["spoil"]) < 1e-12
    assert ITEMS["smoked fish"]["food"] == 2 * ITEMS["fish"]["food"] and ITEMS["smoked meat"]["food"] == 2 * ITEMS["meat"]["food"]


def test_a_day_untended_pauses_the_batch_and_it_spoils_that_night_at_the_open_rate():
    w = world(VALLEY, smokehouse(), calendar=AUTUMN)
    fed(w, "Reed")
    hand(w, "Odo", meat=40)
    do(w, "Odo", do="make", what="smoke meat")
    (cid, c), = racks(w).items()
    night(w)                                                                  # night 0: lit
    a = w.s["containers"][cid]["goods"]["smoking meat"]
    night(w)                                                                  # night 1: nobody tended it: out
    rk = w.s["containers"][cid]["rack"]
    b = w.s["containers"][cid]["goods"]["smoking meat"]
    assert rk["lit"] == 1 and rk.get("out") == 1
    assert (a - b) / a > 3 * (40 - a) / 40                                     # the open rate, well above the smoked
    kn = PR.house_known(Here(w, "Odo"), "smokehouse")
    assert any("the fire died last night" in x for x in kn), kn
    do(w, "Odo", do="work", what="tend the smoke")
    night(w)
    assert not w.s["containers"][cid]["rack"].get("done")                      # three nights gone, two of fire: not done
    do(w, "Odo", do="work", what="tend the smoke")
    night(w)
    assert w.s["containers"][cid]["rack"].get("done") == 3


def test_no_firewood_and_the_fire_dies_however_tended():
    w = world(VALLEY, smokehouse(wood=0), calendar=AUTUMN)
    fed(w, "Reed")
    hand(w, "Odo", meat=10)
    r = do(w, "Odo", do="make", what="smoke meat")
    assert "no firewood" in r, r
    rec = night(w)
    assert rec["smokehouse"]["smokehouse"]["lit"] is False
    hand(w, "Odo", firewood=3)                                                # tending with fuel in hand puts a night's worth in
    r = do(w, "Odo", do="work", what="tend the smoke")
    assert "you put 1 firewood from your hands on it" in r, r
    assert night(w)["smokehouse"]["smokehouse"]["lit"] is True


# ---------------------------------------------------------------------- §4a.1: fire
def _lit_nights(structure, nights=300):
    w = world(VALLEY, smokehouse(structure=structure, wood=0), calendar=AUTUMN)
    caught = 0
    for d in range(nights):
        w.s["day"] = d
        w.s["buildings"]["smokehouse"].update(condition=2, level=None, fire_hit=None)
        store(w, "smokehouse")["firewood"] = 5.0
        for cid in list(racks(w)):
            w.s["containers"].pop(cid)
        pile = w.apply("new_thing", "millbrook", node="millbrook", parcel="mb_green", kind="pile", by="Odo", **{"in": "smokehouse"},
                       rack={"day": d, "nights": 3, "into": "smoked meat", "ratio": 0.5, "smoke": True, "smokehouse": True, "lit": 0})
        w.s["containers"][pile]["goods"]["smoking meat"] = 10.0
        w.s["buildings"]["smokehouse"]["smoke"] = {"tended": d}
        rec = {}
        KP.night(w, rec)
        caught += len(rec.get("smokehouse_fires", []))
    return caught


def test_a_wattle_smokehouse_sometimes_catches_and_a_stone_one_almost_never():
    wattle, stone = _lit_nights("wattle"), _lit_nights("stone")
    assert 2 <= wattle <= 15, wattle                                          # about 2% a night of fire
    assert stone == 0, stone
    assert PHYSICS["smokehouse"]["fire"]["stone"] < PHYSICS["smokehouse"]["fire"]["wattle"] / 20


def test_a_fire_in_the_smokehouse_burns_its_batch_and_reaches_only_buildings_on_its_parcel():
    w = world(VALLEY, smokehouse(parcel="mb_green"), calendar=AUTUMN)       # beside Reed House and Hale House
    hand(w, "Odo", meat=40)
    do(w, "Odo", do="make", what="smoke meat")
    hit = set()
    for d in range(12):                                                      # the spread is keyed by the night: try several
        w.s["day"] = d
        hit |= set(KP.catch(w, "smokehouse")["burnt"])
    assert "smokehouse" in hit and hit & {"reed_house", "hale_house"}
    assert sum(c["goods"].get("smoking meat", 0) for c in racks(w).values()) < 40 * 0.2
    w2 = world(VALLEY, smokehouse(parcel="long_field"), calendar=AUTUMN)   # apart, on another parcel: no house reached
    for d in range(12):
        w2.s["day"] = d
        assert KP.catch(w2, "smokehouse")["burnt"] == ["smokehouse"]


# ---------------------------------------------------------------------- §4a.5: whose, by agreement, robbed, seen
def test_a_neighbour_pays_to_use_it_and_its_batch_waits_for_them():
    w = world(VALLEY, smokehouse(door="barred"), calendar=AUTUMN)
    fed(w, "Reed")
    fed(w, "Hale")
    hand(w, "Hamo", meat=40)
    r = do(w, "Hamo", do="make", what="smoke meat")
    assert r.startswith("Refused") and "smoke racks" in r, r                  # the door barred: no racks he can use
    oid_line = AG.make_offer(Here(w, "Odo"), Mind(w, "Odo"), {"to": "Hamo", "get": "4 meat"})   # the rent: 4 meat
    oid = next(o for o, x in w.s["offers"].items() if x["by"] == "Odo" and x["open"])
    assert "Refused" not in oid_line
    r = do(w, "Hamo", do="accept", offer=oid)
    assert not r.startswith("Refused"), r
    assert abs(w.goods(w.hands("Hamo"))["meat"] - 36.0) < 1e-9
    assert "may now use the Smokehouse" in do(w, "Odo", do="grant", to="Hamo", at="the Smokehouse", days=4)
    r = do(w, "Hamo", do="make", what="smoke meat")
    assert "36 smoking meat" in r, r
    kn = PR.house_known(Here(w, "Odo"), "smokehouse")
    assert any("36 meat curing" in x and "hung by Hamo" in x for x in kn), kn
    for d in range(3):
        if d:
            do(w, "Hamo", do="work", what="tend the smoke")
        night(w)
    assert store(w, "smokehouse").get("smoked meat", 0) < 1e-9               # not into the Reeds' store: it waits for Hamo
    kn = PR.house_known(Here(w, "Odo"), "smokehouse")
    assert any("for Hamo, who hung it" in x for x in kn), kn
    r = do(w, "Hamo", do="take", item="smoked meat", qty=17, **{"from": "the Smokehouse"})
    assert not r.startswith("Refused") and w.goods(w.hands("Hamo")).get("smoked meat", 0) > 16.5, r


def test_it_can_be_robbed_while_a_batch_is_in():
    w = world(VALLEY, smokehouse(), calendar=AUTUMN)
    hand(w, "Odo", meat=40)
    do(w, "Odo", do="make", what="smoke meat")
    (cid, c), = racks(w).items()
    Here(w, "Hamo").remember_thing(cid, "found")                             # Hamo has seen what hangs there
    r = do(w, "Hamo", do="take", item="smoking meat", qty=10, **{"from": "the Smokehouse"})
    assert not r.startswith("Refused") and abs(w.goods(w.hands("Hamo")).get("smoking meat", 0) - 10) < 1e-9, r


def test_its_household_sees_its_state_and_a_stranger_does_not():
    w = world(VALLEY, smokehouse(), calendar=AUTUMN)
    hand(w, "Odo", meat=30)
    do(w, "Odo", do="make", what="smoke meat")
    mine = "\n".join(PR._house_lines(Here(w, "Isolde"), Mind(w, "Isolde")))
    assert "on the smoke racks: 30 meat curing, 3 nights left" in mine and "the fire tended today" in mine, mine
    assert "firewood for 10 nights" in mine
    theirs = "\n".join(PR._house_lines(Here(w, "Hamo"), Mind(w, "Hamo")))
    assert "smoke racks" not in theirs and "curing" not in theirs, theirs
    night(w)
    mine = "\n".join(PR._house_lines(Here(w, "Isolde"), Mind(w, "Isolde")))
    assert "2 nights left" in mine and "the fire not tended today: it dies tonight unless someone tends it" in mine, mine


def test_a_smokehouse_stands_apart():
    w = world(VALLEY, smokehouse())
    hand(w, "Odo", timber=10)
    r = do(w, "Odo", do="build", what="smoke racks", at="Reed House")
    assert r.startswith("Refused") and "a building of their own" in r, r
    hand(w, "Odo", straw=10)
    r = do(w, "Odo", do="build", what="beds", at="the Smokehouse")
    assert r.startswith("Refused") and "is a smokehouse" in r, r


# ---------------------------------------------------------------------- §4b: salt inland
def salthouse(parcel, household, wood=20, structure="wattle"):
    return {"salthouse": {"parcel": parcel, "household": household, "structure": structure, "name": "the Salt House",
                          "fittings": {"brine pan": 1}, "stock": {"firewood": wood}}}


def salter(w, who):
    w.apply("learn", w.at(who), person=who, tech="boil salt", level="known", source="test")
    w.apply("learn", w.at(who), person=who, tech="brine pan", level="known", source="test")


def test_boiling_salt_burns_firewood_at_its_rate_at_saltwells_spring():
    w = world(RIVER, salthouse(RP["spring"], RP["household"]))                      # on the Brine Meadow, at the spring
    assert "brine" in w.s["parcels"][RP["spring"]]["res"]                   # the spring the generator pinned is live
    salter(w, RP["salter"])
    here = Here(w, RP["salter"])
    wood, salt = KN.available(here, "firewood"), KN.available(here, "salt")   # from the stores he may take from, as the hearth's
    r = do(w, RP["salter"], do="make", what="boil salt", qty=3)
    assert r.count("You made 4 salt") == 3, r
    assert abs(KN.available(here, "firewood") - (wood - 12)) < 1e-9          # 1 firewood a salt
    assert abs(KN.available(here, "salt") - (salt + 12)) < 1e-9
    assert w.s["parcels"][RP["spring"]]["res"]["brine"]["S"] == 1000         # endless
    assert TECHNIQUES["boil salt"]["units"] == 1 and TECHNIQUES["boil salt"]["trade"] == "salter"
    w.s["calendar"] = {"season": "winter", "day": 2, "season_days": 8}       # in any season, unlike the sun-dried pans
    for cid in here.takeable():
        w.s["containers"][cid]["goods"]["firewood"] = 0.0
    store(w, "salthouse")["firewood"] = 4.0
    assert "You made 4 salt" in do(w, RP["salter"], do="make", what="boil salt")
    assert "it needs 4 firewood" in do(w, RP["salter"], do="make", what="boil salt")   # no firewood, no salt


def _far_from_spring():
    """A parcel of the spring's village neither at the spring nor beside it (the remade river world puts the salter's house beside
    the Brine Meadow, so the test sets its own building away from it)."""
    w = World(copy.deepcopy(RIVER))
    near = {RP["spring"]} | set(w.s["parcels"][RP["spring"]]["adj"])
    return next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == RP["node"] and p not in near and x["cover"] != "water")


def test_a_brine_pan_is_set_only_at_or_beside_a_spring():
    far = _far_from_spring()
    bare = salthouse(far, RP["household"])
    bare["salthouse"]["fittings"] = {}
    w = world(RIVER, bare)
    salter(w, RP["salter"])
    hand(w, RP["salter"], copper=2, timber=4)
    r = do(w, RP["salter"], do="build", what="salt pan", at="the Salt House")      # "salt pan" names the brine pan when building
    assert r.startswith("Refused") and "brine spring" in r, r
    w2 = world(RIVER, salthouse(far, RP["household"]))                                     # a pan away from the spring: nothing to boil
    salter(w2, RP["salter"])
    r = do(w2, RP["salter"], do="make", what="boil salt")
    assert r.startswith("Refused") and "no brine spring" in r, r


def test_brine_works_wherever_a_world_puts_one():
    s = copy.deepcopy(VALLEY)
    s["packs"] = ["water"]
    w = world(s, salthouse("mb_green", "Reed"))
    w.apply("set_res", "millbrook", parcel="mb_brook", key="brine", fields={"S": 1000.0, "K": 1000.0, "r": 0.0})   # beside the Green
    salter(w, "Edric")
    assert "You made 4 salt" in do(w, "Edric", do="make", what="boil salt")
    sp = load_spec("cybertron2/specs/valley_s5.yaml")                       # or written in the world file, as a stock
    sp["packs"] = ["water"]
    sp["nodes"]["millbrook"]["parcels"]["mb_brook"].setdefault("state", {})["brine"] = {"S": 1000, "K": 1000, "r": 0.0}
    w2 = world(sp, salthouse("mb_green", "Reed"))
    assert "brine" in w2.s["parcels"]["mb_brook"]["res"]
    salter(w2, "Edric")
    assert "You made 4 salt" in do(w2, "Edric", do="make", what="boil salt")


def test_an_inland_village_without_a_spring_has_no_salt():
    w = world(RIVER)
    mill = [p for p, x in w.s["parcels"].items() if x["node"] == "Millham"]
    assert mill and not any({"brine", "salt"} & set(w.s["parcels"][p]["res"]) or w.s["parcels"][p]["cover"] == "saltmarsh" for p in mill)
    who = next(n for n, a in w.s["people"].items() if a["at"] == "Millham" and a["stage"] == "adult")
    salter(w, who)
    here, mind = Here(w, who), Mind(w, who)
    assert KN.shortfall(here, mind, "boil salt").startswith("there is no brine pan")
    assert KN.shortfall(here, mind, "salt pan").startswith("there is no saltmarsh")
    assert KN.available(here, "salt") < 1e-9
    hand(w, who, fish=8)
    r = do(w, who, do="make", what="salt fish")
    assert r.startswith("Refused") and "salt" in r, r


def test_salted_fish_keep_as_built():
    assert TECHNIQUES["salt fish"]["inputs"] == {"fish": 4, "salt": 1} and TECHNIQUES["salt fish"]["gives"] == {"salt fish": 4}
    assert ITEMS["salt fish"]["spoil"] == 0.01 and ITEMS["salt fish"]["decay"] == "dried meat"
    w = world(RIVER, salthouse(RP["spring"], RP["household"]), calendar=AUTUMN)       # salt boiled, then fish salted with it
    salter(w, RP["salter"])
    do(w, RP["salter"], do="make", what="boil salt")
    assert KN.available(Here(w, RP["salter"]), "salt") >= 4 - 1e-9
    hand(w, RP["salter"], fish=4)
    assert "You made 4 salt fish" in do(w, RP["salter"], do="make", what="salt fish")
    r = N.spoil_rate(w.p, "salt fish", "store", "autumn", False)
    assert abs(r - 0.01 * w.p["house_spoil"]) < 1e-12


def test_coastal_salt_is_unchanged():
    t = TECHNIQUES["salt pan"]
    assert t["verb"] == "gather" and t["at"] == {"covers": ["saltmarsh"]} and t["draws"] == "salt"
    assert t["by_season"] == {"spring": 0.4, "summer": 1.0, "autumn": 0.2, "winter": 0.0} and t["yield"] == {"kind": "fixed", "base": 1.0}
    w = world(COAST)
    who = next(n for n, a in w.s["people"].items() if a["stage"] == "adult" and any(
        p["node"] == a["at"] and p["cover"] == "saltmarsh" for p in w.s["parcels"].values()))
    r = do(w, who, do="gather", what="salt pan")
    assert "salt" in r and not r.startswith("Refused"), r


# ---------------------------------------------------------------------- §4c: the fuel harness runs on any world
def test_the_fuel_budget_harness_runs_on_the_river_world():
    from cybertron2 import fuel_budget as FB
    out = FB.run("cybertron2/specs/water/river.yaml", days=4, smokehouse=RP["node"], salter=RP["node"])
    assert set(out["burned"]) == {"hearths", "smokehouse", "salt pan"}
    assert out["burned"]["salt pan"] > 0 and out["burned"]["smokehouse"] > 0 and out["burned"]["hearths"] > 0
    assert out["woods"] and all({"standing", "start"} <= set(v) for v in out["woods"].values())


# ---------------------------------------------------------------------- the signs (§4a, §4b.5)
def _signs(w, who):
    from cybertron2.engine import signs as SG
    got = []
    SG.facts(Here(w, who), lambda about, text, p, tags, sense, **kw: got.append((text, round(float(p), 3), sense)))
    return got


def test_the_smokehouse_and_the_salt_pan_are_seen_and_smelt():
    w = world(VALLEY, smokehouse(), calendar=AUTUMN)
    hand(w, "Odo", meat=30)
    do(w, "Odo", do="make", what="smoke meat")
    night(w)
    got = _signs(w, "Hamo")
    assert any("the smell of smoking meat from the Smokehouse" == t for t, _, s in got), got
    assert any(t.startswith("smoke seeping through the thatch of the Smokehouse") for t, _, s in got), got
    night(w)                                                                  # untended: the fire out
    got = _signs(w, "Hamo")
    assert any("its fire has gone out" in t for t, _, s in got) and not any("smell of smoking" in t for t, _, s in got), got
    w = world(RIVER, salthouse(RP["spring"], RP["household"]))
    salter(w, RP["salter"])
    do(w, RP["salter"], do="make", what="boil salt", qty=3)
    got = _signs(w, RP["neighbour"])
    assert any(t.startswith("steam rising from the pan at the Salt House") for t, _, s in got), got
    assert any("has burned all day" in t for t, _, s in got), got
    w.s["day"] += 1
    w.s["events"] = []
    got = _signs(w, RP["neighbour"])
    assert any("white crusts of salt on the rim of the pan" in t for t, _, s in got) and not any("steam" in t for t, _, s in got), got
    assert any("a white rim of salt dried on the stones" in t for t, _, s in got), got
