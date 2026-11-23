"""Brief 4c §6 (proposals/hunt_calibration.md): drying any batch up to 8, the rack inside at a hearth, a dry batch into the store,
one's own house known without a roll, and the store line counting the door."""
import copy
import random

from cybertron2.engine import night as N, process as PROC, prompt as PR, run as R, verbs as V, view as VW, wild as WL
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

from tests.test_cybertron2_wild import build, generated  # noqa: F401
from tests.test_cybertron2_wild_calibrate import _with_people

SPEC = load_spec("cybertron2/specs/valley_s5.yaml")


def world(**patch):
    s = copy.deepcopy(SPEC)
    s.update(patch)
    w = World(s)
    w.s["today"] = R.blank_today()
    return w


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def hand(w, who, **goods):
    w.s["containers"][w.hands(who)]["goods"].update({k.replace("_", " "): float(v) for k, v in goods.items()})


def store(w, bid):
    return w.s["containers"][w.s["buildings"][bid]["stock"]]["goods"]


def racks(w):
    """The lots on the racks (u4, W-99: a lot record in place of the rack)."""
    return PROC.lots(w)


def night(w):
    rec = N.night(w)
    w.s["day"] += 1
    w.s["today"] = R.blank_today()
    return rec


def _fed(w, bid="reed_house"):
    """A store with plenty of bread, so the night's meal does not reach the rack."""
    store(w, bid).update({"bread": 40.0, "grain": 0.0})


# ---------------------------------------------------------------------- §6.1, §6.2, §6.3: any batch, inside, into the store
def test_dry_meat_hangs_3_meat_and_gives_about_1_5_dried_meat_on_the_rack_the_next_morning():
    # u4 (W-99): the hearth's rack a night of its fire (Basis rows needed, 6); a done lot stays on its rack until taken down (B8)
    w = world()
    _fed(w)
    hand(w, "Odo", meat=3)
    r = do(w, "Odo", do="make", what="dry meat")
    assert "3 kg of meat on the rack in the smoke of the hearth inside Reed House" in r and "dry after 1 night of its fire" in r, r
    (cid, c), = racks(w).items()
    assert c.get("in") == "reed_house" and c.get("door") is None                # part of the house, not a pile at its door
    assert abs(c["goods"]["drying meat"] - 3.0) < 1e-9 and w.goods(w.hands("Odo")).get("meat", 0) < 1e-9
    night(w)
    lt = w.s["containers"][cid]["lot"]
    assert lt["done"] == 0 and 1.5 * 0.95 < lt["got"] < 1.5                     # half its weight, less a night at 0.03
    assert w.s["containers"][cid]["goods"]["dried meat"] == lt["got"] and store(w, "reed_house").get("dried meat", 0) < 1e-9


def test_the_smoked_rate_is_about_3_percent_a_night():
    w = world(calendar={"season": "autumn", "day": 1, "season_days": 6})
    _fed(w)
    hand(w, "Odo", meat=8)
    do(w, "Odo", do="make", what="dry meat")
    (cid, c), = racks(w).items()
    night(w)
    lost = 1 - w.s["containers"][cid]["lot"]["got"] / 4.0
    assert abs(lost - 0.03) < 1e-6, lost                                       # the row's in-process base (u4 §5 step 4)


def test_any_batch_up_to_8_and_refused_only_with_no_meat():
    w = world()
    hand(w, "Odo", meat=0.7)                                                   # a hare's meat
    assert "0.7 kg of meat on the rack" in do(w, "Odo", do="make", what="dry meat")
    hand(w, "Isolde", meat=11)                                                 # more than the rack's room: 7.3 hang, 3.7 are left
    do(w, "Isolde", do="make", what="dry meat")                                # (the hearth's rack holds 8 kg: u4 §2)
    assert abs(sum(c["goods"].get("drying meat", 0) for c in racks(w).values()) - 8.0) < 1e-9
    assert abs(w.goods(w.hands("Isolde")).get("meat", 0) - 3.7) < 1e-9
    w2 = world()
    hand(w2, "Isolde", meat=11)                                                # more than a batch: 8 hang, 3 are left
    do(w2, "Isolde", do="make", what="dry meat")
    assert max(c["goods"].get("drying meat", 0) for c in racks(w2).values()) == 8.0
    assert abs(w2.goods(w2.hands("Isolde")).get("meat", 0) - 3.0) < 1e-9
    w.s["containers"][w.hands("Hamo")]["goods"]["meat"] = 0.0
    store(w, "hale_house")["meat"] = 0.0
    r = do(w, "Hamo", do="make", what="dry meat")
    assert r.startswith("Refused") and "no meat to hand" in r, r


def test_a_dry_batch_stays_on_the_rack_until_taken_and_a_full_store_leaves_the_rest_on_it():
    w = world()
    hand(w, "Odo", meat=8)
    do(w, "Odo", do="make", what="dry meat")
    (cid, c), = racks(w).items()
    from cybertron2.engine import buildings as BL
    b = w.s["buildings"]["reed_house"]
    b["fittings"].pop("bins")
    for who in w.living():                                                     # fed from their own hands, the store left alone
        if w.household_of(who) == "Reed":
            hand(w, who, bread=20)
    store(w, "reed_house").update({"bread": 0.0, "grain": 0.0, "timber": 0.0})
    wood = w.apply("new_thing", "millbrook", node="millbrook", parcel=b["parcel"], kind="pile", by="Odo", door="reed_house")
    w.apply("create", "millbrook", dst=wood, item="timber", qty=10.0)          # the fire burns its woodpile at the door
    night(w)
    assert w.s["containers"][cid]["goods"].get("dried meat", 0) > 3.8          # on the rack (u4 Departure 6)
    kn = PR.house_known(Here(w, "Odo"), "reed_house")
    assert any("on the rack by the hearth: 3.9 kg of dried meat, done last night, waiting to be taken down" in x for x in kn), kn
    store(w, "reed_house")["stone"] = round(BL.room_for(b, store(w, "reed_house"), "stone") - 1e-3, 3)   # its floor full
    r = do(w, "Odo", do="take", item="dried meat", **{"from": "Reed House"})   # known without a roll: taken from the rack
    assert "dried meat" in r and not r.startswith("Refused"), r


def test_at_a_fire_ring_in_the_open_the_batch_hangs_outside_as_a_pile():
    w = world()
    w.s["buildings"]["reed_house"]["fittings"].pop("hearth")
    w.s["buildings"]["reed_house"]["fittings"]["fire ring"] = 1
    hand(w, "Odo", meat=4)
    r = do(w, "Odo", do="make", what="dry meat")
    (cid, c), = racks(w).items()
    assert c.get("door") == "reed_house" and c.get("in") is None and "outside Reed House" in r, r
    assert "if it stays dry" in r, r                                           # outside, a dry night (u4 §2)


# ---------------------------------------------------------------------- §6.2: the fox and the rats
def test_at_a_hearth_a_fox_at_the_door_does_not_reach_the_rack_unless_it_gets_into_the_house(generated):  # noqa: F811
    w = build(_with_people(generated))
    w.s["today"] = R.blank_today()
    bid = next(bid for bid, b in w.s["buildings"].items() if b["node"] == "s1" and (b.get("fittings") or {}).get("hearth"))
    w.s["containers"][w.hands("P0")]["goods"]["meat"] = 8.0
    do(w, "P0", do="make", what="dry meat", at=w.s["buildings"][bid]["name"])
    (cid, c), = racks(w).items()
    assert c.get("in") == bid
    assert cid not in dict(WL._left_out(w, "s1"))                              # not food left out at the door
    door = w.apply("new_thing", "s1", node="s1", parcel=w.s["buildings"][bid]["parcel"], kind="pile", by="P0", door=bid)
    w.apply("create", "s1", dst=door, item="meat", qty=2.0)
    g = {"kind": "fox", "node": "s1", "n": 1, "found": -99, "habit": {}}
    np_ = WL._near("fox")
    row = {"what": "left out", "share": 0.6}
    took = WL._raid(w, g, np_, "fox", row, door, w.s["buildings"][bid]["parcel"], None, random.Random(1))
    assert took["took"] > 0 and abs(c["goods"]["drying meat"] - 8.0) < 1e-9     # what lay at the door taken; the rack untouched
    w.s["wild"].setdefault("shut", {})[bid] = {"day": w.d}                     # shut up for the night, the house sound
    w.s["buildings"][bid]["level"] = 5
    assert WL._raid(w, g, np_, "fox", row, cid, w.s["buildings"][bid]["parcel"], None, random.Random(1))["took"] == 0
    w.s["buildings"][bid]["level"] = 2                                         # holed: the fox gets in, as to the store
    assert WL._raid(w, g, np_, "fox", row, cid, w.s["buildings"][bid]["parcel"], None, random.Random(1))["took"] > 0


# ---------------------------------------------------------------------- §6.4: one's own house known without a roll
def test_a_household_member_sees_the_racks_state_each_morning_and_a_stranger_does_not():
    w = world()
    _fed(w)
    hand(w, "Odo", meat=6)
    do(w, "Odo", do="make", what="dry meat")
    seen = []
    for _ in range(2):
        night(w)
        seen.append(PR.turn_prompt(Here(w, "Isolde"), Mind(w, "Isolde")))     # of the household, not the maker
        assert "rack" not in PR.turn_prompt(Here(w, "Hamo"), Mind(w, "Hamo"))  # of the village, another house
    assert "On the rack by the hearth: 2.9 kg of dried meat, done last night, waiting to be taken down." in seen[0], seen[0]   # u4 §7
    assert "done 2 nights ago, waiting to be taken down." in seen[1], seen[1]


def test_the_belief_view_shows_the_house_every_day_to_its_household_only():
    w = world(view="beliefs")
    _fed(w)
    hand(w, "Odo", meat=6)
    do(w, "Odo", do="make", what="dry meat")
    for who in ("Isolde", "Hamo"):                                             # the opening: the whole house
        VW.turn(Here(w, who), Mind(w, who))
        m = Mind(w, who)
        m.store["view"] = m.store["view_next"]
    night(w)
    mine = VW.turn(Here(w, "Isolde"), Mind(w, "Isolde"), opening=False)
    assert "Reed House this morning: the fire lit last night; on the rack by the hearth: 2.9 kg of dried meat, done last night" in mine, mine
    assert "rack" not in VW.turn(Here(w, "Hamo"), Mind(w, "Hamo"), opening=False)


def test_goods_at_the_door_and_a_new_building_without_beds_are_in_the_house_lines():
    w = world()
    pid = w.s["buildings"]["reed_house"]["parcel"]
    cid = w.apply("new_thing", "millbrook", node="millbrook", parcel=pid, kind="pile", by="Odo", door="reed_house")
    w.apply("create", "millbrook", dst=cid, item="dried meat", qty=7.5)        # 9 meals at dried meat's 1.2 (D2-258; was 3 at 3.0)
    w.apply("create", "millbrook", dst=cid, item="timber", qty=2.0)
    lines = PR.house_known(Here(w, "Odo"), "reed_house")
    assert "left at its door: 7.5 dried meat, 2 timber (food worth 9 meals)" in lines, lines
    w.s["buildings"]["hale_house"]["fittings"] = {"bins": 1}                   # built in the run, no beds, no hearth
    w.s["buildings"]["hale_house"]["built_day"] = 0
    assert "Hale House has no beds or hearth: no one can sleep there yet" in PR.house_known(Here(w, "Hamo"), "hale_house")
    assert "it has no beds or hearth: no one can sleep there yet" in PR.turn_prompt(Here(w, "Hamo"), Mind(w, "Hamo"))
    assert "left at its door" not in "\n".join(PR._house_lines(Here(w, "Hamo"), Mind(w, "Hamo")))


# ---------------------------------------------------------------------- §6.5: the store line counts the door
def test_the_store_line_counts_food_at_the_door_as_the_nights_meal_reaches_it():
    w = world()
    from cybertron2.engine.data import ITEMS
    store(w, "reed_house").update({"grain": 0.0, "bread": 14.0 / float(ITEMS["bread"]["food"])})   # 14 meals in the store
    pid = w.s["buildings"]["reed_house"]["parcel"]
    cid = w.apply("new_thing", "millbrook", node="millbrook", parcel=pid, kind="pile", by="Odo", door="reed_house")
    w.apply("create", "millbrook", dst=cid, item="dried meat", qty=7.5)        # 9 meals at the door (dried meat 1.2, D2-258)
    other = w.apply("new_thing", "millbrook", node="millbrook", parcel=pid, kind="pile", by="Hamo", door="hale_house")
    w.apply("create", "millbrook", dst=other, item="dried meat", qty=5.0)      # another house's door: not ours to eat
    h = Here(w, "Odo")
    st, door, rack = PR.house_food(h, "reed_house")
    assert abs(st - 14.0) < 1e-6 and abs(door - 9.0) < 1e-6 and rack == 0
    reach = [c for c in w.takeable("Odo") if c != w.hands("Odo")]              # what the night's meal eats from
    meal = sum(PR._meals(w.goods(c)) for c in reach)
    assert abs(meal - (st + door + rack)) < 1e-6
    assert "food worth 14 meals, and 9 more at its door" in "\n".join(PR._house_lines(h, Mind(w, "Odo")))
    store(w, "reed_house")["bread"] = 0.0                                       # nothing in the store: the meal eats from the door
    rec = night(w)
    assert rec["ate"].get("Odo", 0) > 0 and w.goods(cid).get("dried meat", 0) < 7.5
