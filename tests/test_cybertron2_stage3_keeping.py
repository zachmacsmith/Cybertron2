"""Stage 3 of the fishing, hunting and materials wave (W-99): keeping, stores and the household book. Interface tests (D2-298): u4's
processing containers (process.py), u5's stores and containers (stores.py), u6's book (book.py). Behaviour is read in live runs."""
import copy

import pytest

from cybertron2.engine import book as BK, buildings as BL, night as N, process as PROC, prompt as PR, run as R, stores as SR, verbs as V
from cybertron2.engine.data import ITEMS, PHYSICS
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

VALLEY = load_spec("cybertron2/specs/valley_s5.yaml")
RIVER = load_spec("cybertron2/specs/water/river.yaml")
AUTUMN = {"season": "autumn", "day": 1, "season_days": 8}
SUMMER = {"season": "summer", "day": 1, "season_days": 8}


def world(spec, buildings=None, **patch):
    s = copy.deepcopy(spec)
    s.update(patch)
    s["buildings"].update(buildings or {})
    w = World(s)
    w.s["today"] = R.blank_today()
    return w


def smokehouse(parcel="mb_green", household="Reed", structure="wattle", wood=60, sets=1, name="the Smokehouse", key="smokehouse", **kw):
    return {key: {"parcel": parcel, "household": household, "structure": structure, "name": name,
                  "fittings": {"smoke racks": sets}, "stock": {"firewood": wood} if wood else {}, **kw}}


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def hand(w, who, **goods):
    w.s["containers"][w.hands(who)]["goods"].update({k.replace("_", " "): float(v) for k, v in goods.items()})


def store(w, bid):
    return w.s["containers"][w.s["buildings"][bid]["stock"]]["goods"]


def lots(w, bid=None):
    return PROC.lots(w, bid)


def night(w):
    rec = N.night(w)
    w.s["day"] += 1
    w.s["today"] = R.blank_today()
    return rec


def fed(w, household):
    for who in w.living():
        if w.household_of(who) == household:
            hand(w, who, bread=30)


def river_places():
    w = World(copy.deepcopy(RIVER))
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if "brine" in x["res"])
    node = w.s["parcels"][pid]["node"]
    hh = next(c["claimant"] for c in w.claims_on(("parcel", pid)) if c["claimant"] in w.s["institutions"])
    adults = sorted(n for n in w.living() if w.s["people"][n]["stage"] == "adult" and w.s["people"][n]["at"] == node)
    me = next(n for n in adults if w.household_of(n) == hh)
    house = next(b for b in w.homes(me) if w.s["buildings"][b]["fittings"].get("beds"))
    return {"node": node, "household": hh, "me": me, "house": house, "parcel": w.s["buildings"][house]["parcel"],
            "other": next(n for n in adults if w.household_of(n) != hh), "mates": [n for n in adults if w.household_of(n) == hh]}


RP = river_places()


def fish_world(**kw):
    w = world(RIVER, smokehouse(parcel=RP["parcel"], household=RP["household"], **kw), calendar=AUTUMN)
    fed(w, RP["household"])
    return w


# ---------------------------------------------------------------------------------------------------------------------- u4
def test_a_lot_counts_a_night_only_when_tended_and_fuelled_and_stays_on_the_racks_when_done():
    w = fish_world()
    me = RP["me"]
    hand(w, me, fish=90)
    r = do(w, me, do="make", what="smoke fish", qty=3)
    assert r.startswith("You hung 90 kg of fish on the smoke racks in the Smokehouse (3 units): a keeping smoke, done after 1 night of fire."), r
    assert "wants about 13.5 bundles of firewood (60 there)" in r and "room for 160 kg more" in r, r
    (cid, c), = lots(w, "smokehouse").items()
    night(w)
    lt = w.s["containers"][cid]["lot"]
    assert lt["had"] == 1 and lt["done"] == 0 and lt["out"] is None
    got = w.s["containers"][cid]["goods"]["smoked fish"]
    assert abs(got - 90 * (1 - 0.03) * 0.5) < 1e-6                              # the in-process base, then half the weight
    assert store(w, "smokehouse").get("smoked fish", 0.0) < 1e-9                # a done lot stays in its container (B8)
    assert abs(store(w, "smokehouse")["firewood"] - (60 - 13.5)) < 1e-6         # fuel by the kg loaded
    # untended: the night is not counted, and the lot keeps at fresh fish's base that night
    hand(w, me, fish=30)
    do(w, me, do="make", what="smoke fish")
    (cid2, _), = [(k, x) for k, x in lots(w, "smokehouse").items() if x["lot"]["done"] is None]
    w.s["buildings"]["smokehouse"]["smoke"]["tended"] = -1
    night(w)
    lt = w.s["containers"][cid2]["lot"]
    assert lt["had"] == 0 and lt["out"] == 1 and lt["done"] is None
    assert abs(w.s["containers"][cid2]["goods"]["smoking fish"] - 30 * (1 - ITEMS["fish"]["spoil"])) < 1e-3


def test_room_is_250_kg_a_set_and_a_done_lot_holds_it_until_taken_down():
    w = fish_world(wood=100)
    me = RP["me"]
    hand(w, me, fish=300)
    r = do(w, me, do="make", what="smoke fish", qty=10)
    assert "You hung 250 kg of fish" in r and "(9 units)" in r and "The rest (50 kg) is still to hand" in r, r
    assert V.cost(Here(w, me), {"do": "make", "what": "smoke fish", "qty": 5}) == 1     # the room left takes nothing: the floor
    night(w)
    assert PROC.room(w, "smokehouse", "keeping smoke") < 1e-6                   # done, still on the racks
    r = do(w, me, do="make", what="smoke fish")
    assert r.startswith("Refused") and "the smoke racks in the Smokehouse are full" in r and "waiting to be taken down" in r, r
    assert V.cost(Here(w, me), {"do": "move", "from": "the Smokehouse", "item": "smoked fish"}) == 2   # 121 kg at 120 a unit
    r = do(w, me, do="move", item="smoked fish", **{"from": "the Smokehouse"})
    assert r.startswith("You took down 121.2 kg of smoked fish from the racks in the Smokehouse into its store"), r
    assert PROC.room(w, "smokehouse", "keeping smoke") > 249.9


def test_the_fuel_is_by_the_kg_loaded_and_short_fuel_kills_the_night():
    w = fish_world(wood=10)
    me = RP["me"]
    hand(w, me, fish=250)
    r = do(w, me, do="make", what="smoke fish", qty=9)
    assert "only 10 bundles of firewood are there of about 37.5 it wants" in r, r
    assert abs(PROC.fuel_tonight(w, "smokehouse") - 37.5 * 0.5) < 1e-9
    rec = night(w)
    assert rec["smokehouse"]["smokehouse"]["lit"] is False
    assert store(w, "smokehouse")["firewood"] == 10.0                           # all or none
    c = next(iter(lots(w, "smokehouse").values()))
    assert c["lot"]["out"] == 0 and c["lot"]["had"] == 0
    kn = PR.house_known(Here(w, me), "smokehouse")
    assert any("the fire died last night" in x for x in kn) and any("not enough firewood for tonight's fire (37.5 bundles needed, 10 there)" in x for x in kn), kn


def test_the_building_caps_the_sets_of_racks_keeping_its_work_floor():
    w = fish_world(sets=1, wood=0)
    me = RP["me"]
    b = w.s["buildings"]["smokehouse"]
    assert BL.floor(b) == 6 and PROC.work_floor(b) == 2
    hand(w, me, withies=20, timber=20)
    w.apply("learn", w.at(me), person=me, tech="smoke racks", level="known", source="test")
    r = do(w, me, do="build", what="smoke racks", at="the Smokehouse", qty=5)
    assert not r.startswith("Refused") and "3 smoke racks" in r, r              # 6 spaces: 1 set, 3 more, 2 kept free
    b["fitting_work"] = None
    b["fittings"]["smoke racks"] = 4
    r = do(w, me, do="build", what="smoke racks", at="the Smokehouse")
    assert r.startswith("Refused") and "needs 2 spaces free to work and keep the fire" in r, r
    assert PROC.capacity(b, "keeping smoke") == 1000


def test_a_hard_cure_is_refused_in_wattle_and_in_timber_turns_60_kg_of_salt_fish_into_24_after_3_nights():
    w = fish_world()
    me = RP["me"]
    hand(w, me, salt_fish=60)
    r = do(w, me, do="make", what="hard cure fish")
    assert r.startswith("Refused") and "a hard cure needs the long cool smoke of a timber or stone smokehouse" in r, r
    w = fish_world(structure="timber", wood=40)
    hand(w, me, salt_fish=60)
    r = do(w, me, do="make", what="hard cure fish")
    assert r.startswith("You hung 60 kg of salt fish on the smoke racks") and "done after 3 nights of fire" in r and "5 bundles" in r, r
    for d in range(3):
        if d:
            assert do(w, me, do="tend", what="the fire").startswith("You tended the fire in the Smokehouse")
        night(w)
    c = next(iter(lots(w, "smokehouse").values()))
    assert c["lot"]["done"] == 2
    assert 23.0 < c["goods"]["hard-cured fish"] <= 24.0, c["goods"]              # 0.4 of the salt fish, less its own base a night


def test_salting_lands_in_a_tub_with_room_else_packed_in_the_store_at_1_salt_to_4_fish():
    w = fish_world()
    me = RP["me"]
    hand(w, me, fish=60, salt=10)
    r = do(w, me, do="make", what="salt fish", qty=2)
    assert r.startswith("You salted 40 kg of fish with the 10 kg of salt you had (1 unit): 40 kg of salt fish, packed in its salt in"), r
    assert "It takes 1 kg of salt to 4 of fish." in r
    store(w, RP["house"])["salting tub"] = 1.0
    hand(w, me, fish=40, salt=10)
    r = do(w, me, do="make", what="salt fish")
    assert "in brine in the salting tub at" in r and "room there for 40 kg more" in r, r


def test_the_hot_smoke_gives_two_thirds_cooked_to_eat_without_a_fire():
    w = fish_world()
    me = RP["me"]
    hand(w, me, fish=10, firewood=2)
    r = do(w, me, do="make", what="hot smoke fish")
    assert "6.7 hot-smoked fish" in r, r
    assert not ITEMS["hot-smoked fish"].get("cook") and abs(ITEMS["hot-smoked fish"]["food"] * 6.7 - 0.46 * 10) < 0.05


def test_a_fire_caught_destroys_the_lots_inside(monkeypatch):
    w = fish_world()
    me = RP["me"]
    hand(w, me, fish=60)
    do(w, me, do="make", what="smoke fish", qty=2)
    monkeypatch.setitem(PHYSICS["smokehouse"]["fire"], "wattle", 1.0)
    rec = night(w)
    assert rec.get("smokehouse_fires") and rec["smokehouse_fires"][0]["smokehouse"] == "smokehouse"
    c = next(iter(lots(w, "smokehouse").values()))
    assert sum(c["goods"].values()) < 60 * 0.5 * 0.2
    assert w.s["buildings"]["smokehouse"].get("fire_hit")


def test_the_same_lots_come_from_the_same_draws():
    def go():
        w = fish_world()
        hand(w, RP["me"], fish=70)
        do(w, RP["me"], do="make", what="smoke fish", qty=3)
        night(w)
        return {k: (dict(c["goods"]), dict(c["lot"])) for k, c in lots(w).items()}
    assert go() == go()


def test_the_containers_states_read_true_and_false_on_the_right_nights():
    w = fish_world(wood=0)
    me = RP["me"]
    hh = RP["household"]
    s0 = PROC.states(w, hh, "smokehouse")
    assert s0["room"] == 250 and not s0["full"] and s0["done"] == 0
    hand(w, me, fish=250)
    do(w, me, do="make", what="smoke fish", qty=9)
    s1 = PROC.states(w, hh, "smokehouse")
    assert s1["full"] and s1["in process"] > 249 and not s1["fire out"]
    night(w)                                                                   # no wood: the fire dies
    assert PROC.states(w, hh, "smokehouse")["fire out"]
    store(w, "smokehouse")["firewood"] = 50
    do(w, me, do="tend", at="the Smokehouse")
    night(w)
    s3 = PROC.states(w, hh, "smokehouse")
    assert 60 < s3["done"] < 100 and not s3["fire out"] and s3["in process"] == 0   # a dead fire's night at the fresh rate (D2-336)


def test_flax_rets_in_water_a_night_and_on_the_grass_three():
    w = world(RIVER, calendar=AUTUMN)
    me = RP["me"]
    hand(w, me, flax=60)
    water = next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == RP["node"] and x["cover"] == "water")
    r = do(w, me, do="make", what="ret flax", at=w.s["parcels"][water]["name"])
    assert "50 kg of flax to ret: done after 1 night" in r and "(1 unit)" in r, r
    night(w)
    c = next(iter(PROC.lots(w, pid=water).values()))
    assert c["lot"]["done"] == 0 and abs(c["goods"]["retted flax"] - 40.0) < 1e-6 or c["lot"]["out"] == 0


# ---------------------------------------------------------------------------------------------------------------------- u5
def house(spec_world, fittings=None, goods=None):
    b = {"structure": "wattle", "fittings": fittings or {}, "rooms": [{"kind": "small room", "floor": 6, "storey": 1},
                                                                      {"kind": "small room", "floor": 6, "storey": 1}]}
    return b, dict(goods or {})


def test_the_sort_puts_grain_in_the_bins_the_chest_the_sacks_and_then_loose_and_nothing_keeps_below_its_base():
    b, g = house(None, {"bins": 1}, {"grain": 1170, "chest": 1, "sack": 4})   # 12 spaces: the bins 1, the chest and sacks 2, 9 free
    pt = SR.portions(b, g)
    where = {}
    for x in pt["portions"]:
        if x["item"] == "grain":
            where[x["kind"]] = where.get(x["kind"], 0.0) + x["qty"]
    assert where == {"chest": 400.0, "bins": 300.0, "sack": 200.0, "floor": 270.0}, where
    base = ITEMS["grain"]["spoil"]
    for k in where:
        assert SR.rate(PHYSICS, "grain", k, "autumn", False) >= base - 1e-12
    assert SR.rate(PHYSICS, "grain", "chest", "autumn", False) == pytest.approx(base)
    assert SR.factor("grain", "sack") == 1.5 and SR.factor("grain", "floor") == 2.0
    assert "1170 grain (400 in the chest, 300 in the bins, 200 in 4 sacks, 270 loose on the floor)" in SR.store_line(b, g), SR.store_line(b, g)
    assert SR.store_line(b, {"timber": 3}) == "3 timber"
    assert not SR.portions(b, {**g, "grain": 1200})["left"] == {}                # 30 more find no room


def test_fresh_fish_keeps_at_its_base_in_a_store_worse_in_hand_and_in_a_creel_at_base():
    assert SR.rate(PHYSICS, "fish", "floor", "autumn", False) == pytest.approx(ITEMS["fish"]["spoil"])   # no x2 (u5 Departure 1)
    w = world(RIVER, calendar=AUTUMN)
    me = RP["me"]
    hand(w, me, fish=10)
    r_hand = SR.in_hand_rate(w, me, "fish", "autumn", False)
    assert r_hand == pytest.approx(1 - (1 - ITEMS["fish"]["spoil"]) ** 1.5)
    hand(w, me, creel=1)
    assert SR.in_hand_rate(w, me, "fish", "autumn", False) == pytest.approx(ITEMS["fish"]["spoil"])


def test_a_cellar_takes_the_summer_off_fresh_meat_and_gives_grain_its_damp():
    assert SR.rate(PHYSICS, "meat", "cellar", "summer", False) < SR.rate(PHYSICS, "meat", "floor", "summer", False)
    assert SR.rate(PHYSICS, "meat", "cellar", "summer", False) == pytest.approx(1 - (1 - ITEMS["meat"]["spoil"]) ** 1.5)   # the flies stay
    assert SR.factor("grain", "cellar") == 2.0 and SR.factor("grain", "upper floor") == 1.0


def test_salt_fish_keeps_at_its_base_in_a_tub_and_worse_out_of_brine():
    assert SR.rate(PHYSICS, "salt fish", "salting tub", "autumn", False) == pytest.approx(ITEMS["salt fish"]["spoil"])
    assert SR.factor("salt fish", "floor") == 1.5


def test_vermin_take_by_where_the_grain_lies_and_a_cat_cuts_mice_more_than_rats():
    assert SR.exposure("floor", "rats") / SR.exposure("chest", "rats") == pytest.approx(5.0)
    from cybertron2.engine import wild as WL
    b = {"stock": "x", "fittings": {}}

    class _W:
        s = {"containers": {"x": {"goods": {"cat": 1}}}, "wild": {}}
    assert WL._stops(b, "voles and mice", _W) < WL._stops(b, "rats", _W)


def test_a_village_of_chests_shows_less_exposed_store_than_one_of_floors():
    w = world(VALLEY)
    bid = "reed_house"
    st = store(w, bid)
    for k in list(st):
        st.pop(k)
    st["grain"] = 200.0
    w.s["buildings"][bid]["fittings"]["bins"] = 0
    loose = SR.exposed(w, bid)
    st["chest"] = 1.0
    chest = SR.exposed(w, bid)
    assert loose > 3 * chest > 0


def test_vermins_illness_factor_by_rats_and_the_households_exposure(monkeypatch):
    w = world(VALLEY)
    name = "Odo"
    assert SR.illness(w, name) == 1.0                                          # no rats
    monkeypatch.setattr(SR, "rats_at", lambda w_, node: 120.0)
    monkeypatch.setattr(SR, "household_exposure", lambda w_, hh: 1.0)
    assert SR.illness(w, name) == pytest.approx(3.0)
    monkeypatch.setattr(SR, "household_exposure", lambda w_, hh: 0.2)
    assert SR.illness(w, name) == pytest.approx(1.4)


def test_the_store_line_and_the_nights_loss_read_the_portions():
    w = world(VALLEY, calendar=AUTUMN)
    st = store(w, "reed_house")
    for k in list(st):
        st.pop(k)
    st.update({"grain": 100.0, "chest": 1.0, "bread": 30.0})
    r = SR.rates(w, "reed_house")
    assert r["grain"] == pytest.approx(ITEMS["grain"]["spoil"])                  # all in the chest
    st["grain"] = 900.0                                                         # 200 now loose on the floor at x2
    r2 = SR.rates(w, "reed_house")["grain"]
    assert ITEMS["grain"]["spoil"] < r2 < SR.rate(PHYSICS, "grain", "floor", "autumn", False)


def test_a_sack_rots_over_its_life():
    from cybertron2.engine import gear as GE
    w = world(VALLEY)
    store(w, "reed_house")["sack"] = 1.0
    w.s["containers"][w.s["buildings"]["reed_house"]["stock"]].setdefault("pieces", {})
    GE.rot_night(w)
    pcs = (w.s["containers"][w.s["buildings"]["reed_house"]["stock"]].get("pieces") or {}).get("sack") or []
    assert pcs and float(pcs[0]["rot"]) == pytest.approx(1 / (3.0 * w.year_days()), rel=1e-3)


# ---------------------------------------------------------------------------------------------------------------------- u6
def book_world(**kw):
    w = fish_world(**kw)
    return w


def head_of(w):
    return w.head(RP["household"])


def test_a_rule_is_read_back_refused_where_it_must_be_and_a_members_is_a_proposal():
    w = book_world()
    head = head_of(w)
    r = do(w, head, do="rule", rule="go", goods="fish", to="the racks in the Smokehouse", when="when they have room",
           words="the fish that comes in goes to the racks")
    assert r.startswith("Rule 1 (the household): fish that comes in goes to the racks in the Smokehouse, when they have room; whoever has time"), r
    assert '(your words: "the fish that comes in goes to the racks")' in r
    r = do(w, head, do="rule", rule="chore", acts=[{"do": "travel", "to": "anywhere"}])
    assert r.startswith("Refused") and "travel and free acts cannot be one" in r, r
    other = RP["other"]
    ob = next(b for b in w.homes(other) if w.s["buildings"][b]["fittings"].get("beds"))
    r = do(w, head, do="rule", rule="move", goods="fish", to=w.s["buildings"][ob]["name"])
    assert r.startswith("Refused") and "is not your household's" in r, r
    r = do(w, head, do="rule", rule="go", goods="salt fish", to="hard cure in the Smokehouse")
    assert r.startswith("Refused") and "a hard cure needs the long cool smoke" in r, r
    mate = next(n for n in RP["mates"] if n != head)
    r = do(w, mate, do="rule", rule="tend", at="the Smokehouse", **{"for": "household"})
    assert r.startswith(f"Proposed to {head}, who heads the household"), r
    r = do(w, mate, do="rule", rule="chore", acts=[{"do": "gather", "what": "firewood"}])
    assert r.startswith("Rule 1 (yours)"), r
    assert V.cost(Here(w, head), {"do": "rule", "rule": "drop", "n": 1}) == 0


def _day(w, plans_used=None):
    names = [n for n in w.living() if w.at(n) is not None]
    budget = {n: w.units_for(n) for n in names}
    used = {n: (plans_used or {}).get(n, budget[n]) for n in names}
    results = {n: [] for n in names}
    rec = BK.spare_units(w, names, sorted(names), budget, used, results)
    return rec, used, results, budget


def test_the_spare_units_phase_hangs_by_rule_what_the_day_brought_in_a_members_spare_units():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="go", goods="fish", to="the racks in the Smokehouse", when="when they have room")
    store(w, RP["house"])["fish"] = 120.0                                      # brought home at midday
    agnes = next(n for n in RP["mates"] if n != head)
    rec, used, results, budget = _day(w, {agnes: 2})                            # she planned 2 of her units; the rest planned all
    assert any(x.startswith("By the household's rule 1: You hung 120 kg of fish") and "(4 units of work)" in x for x in results[agnes]), results[agnes]
    assert used[agnes] == 6 and store(w, RP["house"]).get("fish", 0.0) < 1e-6


def test_a_rule_on_a_lasting_state_waits_when_no_one_has_units_and_fires_the_next_day():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="move", goods="smoked fish", **{"from": "the racks in the Smokehouse"}, to=w.s["buildings"][RP["house"]]["name"],
       when="when a lot is done")
    hand(w, head, fish=60)
    do(w, head, do="make", what="smoke fish", qty=2)
    night(w)
    rec, *_ = _day(w)                                                          # everyone planned every unit
    assert any(m["rule"] == 1 for m in rec["missed"]), rec
    assert any("Waiting today:" in x for x in BK.morning_lines(w, head))
    rec, used, results, _ = _day(w, {head: 0})
    assert any("You took down" in x for x in results[head]), results[head]


def test_ones_own_standing_fallback_comes_before_the_households_chore_and_unset_units_are_rest():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="tend", at="the Smokehouse", when="while anything is smoking")
    hand(w, head, fish=30)
    do(w, head, do="make", what="smoke fish")
    w.s["buildings"]["smokehouse"]["smoke"]["tended"] = -1                     # wants tending today
    joan = next(n for n in RP["mates"] if n != head)
    BK.set_fallback(w, joan, [{"do": "gather", "what": "firewood"}])
    names = [n for n in w.living() if w.at(n) is not None]
    budget = {n: w.units_for(n) for n in names}
    used = {n: (budget[n] if n not in (joan, head) else 0) for n in names}
    results = {n: [] for n in names}
    BK.spare_units(w, names, sorted(names), budget, used, results)
    assert any("(your fallback)" in x for x in results[joan])                   # her own fallback first (D2-301)
    assert any("By the household's rule 1: You tended the fire" in x for x in results[head]), results[head]
    assert not any("tended" in x for x in results[joan])
    w2 = book_world()
    names = [n for n in w2.living() if w2.at(n) is not None]
    budget = {n: w2.units_for(n) for n in names}
    used = {n: 0 for n in names}
    rec = BK.spare_units(w2, names, sorted(names), budget, used, {n: [] for n in names})
    assert rec["rest"] and all(v == budget[n] for n, v in rec["rest"].items())  # nothing set: all of it rest


def test_a_chores_fraction_is_carried_until_whole_and_never_takes_more_than_the_spare():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="go", goods="fish", to="the racks in the Smokehouse")
    store(w, RP["house"])["fish"] = 45.0                                       # 1.5 units of hanging
    names = [n for n in w.living() if w.at(n) is not None]
    budget = {n: w.units_for(n) for n in names}
    used = {n: (budget[n] - 2 if n == head else budget[n]) for n in names}
    BK.spare_units(w, names, sorted(names), budget, used, {n: [] for n in names})
    assert used[head] == budget[head] - 1 and w.s["people"][head]["chore_carry"] == pytest.approx(0.5)
    store(w, RP["house"])["fish"] = 300.0
    used = {n: (budget[n] - 1 if n == head else budget[n]) for n in names}
    BK.spare_units(w, names, sorted(names), budget, used, {n: [] for n in names})
    assert used[head] <= budget[head]


def test_each_rule_fires_once_a_day_and_cascades_stop():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="go", goods="fish", to="the racks in the Smokehouse")
    store(w, RP["house"])["fish"] = 300.0
    rec, used, results, _ = _day(w, {n: 0 for n in RP["mates"]})
    fired = [x for x in rec["fired"] + rec["partly"] if x["rule"] == 1]
    assert len(fired) == 1, rec


def test_a_rule_when_the_run_is_seen_fires_only_on_a_day_a_member_noticed_it():
    w = book_world()
    hh = RP["household"]
    st = BK.state_of("when the eels start running")
    assert st["state"] == "seen" and st["set"] == "run"
    assert not BK.seen(w, hh, "run")
    m = RP["mates"][0]
    w.s["mind"][m]["today"]["concerned"] = ["eels running thick at the weir in the dusk"]
    assert BK.seen(w, hh, "run")


def test_a_go_rule_sends_goods_arriving_to_its_store():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="go", goods="firewood", to="the Smokehouse store")
    w.apply("create", w.at(head), dst=w.s["buildings"][RP["house"]]["stock"], item="firewood", qty=5.0)
    assert store(w, "smokehouse")["firewood"] == pytest.approx(65.0)


def test_what_the_book_holds_back_is_not_eaten_and_first_goes_first():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="hold back", goods="salt fish", qty=20, unless="someone is starving")
    stk = w.s["buildings"][RP["house"]]["stock"]
    store(w, RP["house"])["salt fish"] = 25.0
    assert BK.held(w, head, stk, "salt fish") == 20.0
    assert N._eat(w, w.at(head), [stk], 10.0, True, who=head) <= 5 * ITEMS["salt fish"]["food"] + 1e-9 + 10
    left = store(w, RP["house"]).get("salt fish", 0.0)
    assert left >= 20.0 - 1e-9
    do(w, head, do="rule", rule="first", goods="salt fish")
    assert BK.meal(w, head)["first"] == ["salt fish"]


def test_the_rules_block_and_the_evening_carry_the_book():
    w = book_world()
    head = head_of(w)
    do(w, head, do="rule", rule="tend", at="the Smokehouse", when="while anything is smoking")
    sys_ = PR.system_prompt(Here(w, head), Mind(w, head))
    assert "standing rules" in sys_ and "1. tend the fire in the Smokehouse" in sys_ and BK.GRAMMAR in sys_
    assert "(say, gather firewood)" not in sys_
    from cybertron2.engine import evening as EV
    assert "rule" in EV.NIGHT_VERBS
