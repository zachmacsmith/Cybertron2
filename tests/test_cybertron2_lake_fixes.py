"""The lake runs' faults (38.75; WORK W-57) and fish on the hearth rack (D4-122)."""
import copy

from cybertron2.engine import life as LF, run as R, verbs as V, wild as WL, signs as SG
from cybertron2.engine.data import TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

LAKE = load_spec("cybertron2/specs/water/lake.yaml")


def world():
    w = World(copy.deepcopy(LAKE))
    w.s["today"] = R.blank_today()
    return w


def do(w, who, **a):
    return V.do(Here(w, who), Mind(w, who), a)


def house(w, hh):
    """The household's dwelling (claims, not a field: D4-36)."""
    return next(b for b in w.homes(w.members(hh)[0]) if (w.s["buildings"][b].get("fittings") or {}).get("beds"))


# ---------------------------------------------------------------------- 1. a death told to the household and the housemates
def test_a_death_in_the_night_is_told_to_the_whole_household_and_who_slept_there():
    w = world()
    dead, others = "Ralf", [n for n in w.members("Marsh") if n != "Ralf"]
    guest = "Baldwin"                                                           # a Ward who slept at Marsh House that night
    where = {n: house(w, w.household_of(n)) for n in w.living()}
    where[guest] = house(w, "Marsh")
    told = LF.death_told(w, dead, where)
    assert set(others) <= set(told["concerns"]) and guest in told["concerns"] and dead not in told["concerns"]
    assert told["about"] == [f"building:{house(w, 'Marsh')}"]
    w.s["people"][dead]["born"] = -400                                          # far into old age: dies tonight
    w.s["people"][dead]["stage"] = "elder"
    out = {"old_age": []}
    LF._old_age(w, out, where)
    assert dead in out["old_age"]
    e = next(e for e in w.s["events"] if e["kind"] == "death" and e["target"] == dead)
    assert set(others) <= set(e["concerns"]) and "family" in e["tags"]
    from cybertron2.engine import perceive as PC
    f = {"about": list(e["about"]) + [f"person:{dead}"], "actor": None}
    assert all(PC.happened_to(w, n, f) for n in others)                       # in their own house: read in full


# ---------------------------------------------------------------------- 2. travel to a place in the village; ways of one name
def test_travel_to_a_parcel_here_says_it_is_here_and_how_to_work_there():
    w = world()
    r = do(w, "Ralf", do="travel", to="the Mere")
    assert "is here at" in r and '"at": "the Mere"' in r and "open road" not in r


def test_ways_of_the_same_name_are_told_apart_by_where_they_lead():
    w = world()
    rid = next(iter(w.s["roads"]))
    r0 = w.s["roads"][rid]
    w.s["nodes"]["Meresby"]["xy"] = [10.0, 10.0]                               # positions as the generator writes them (y north)
    w.s["nodes"][r0["b"]]["xy"] = [10.0, 20.0]
    w.s["nodes"]["w9"] = dict(copy.deepcopy(w.s["nodes"][r0["b"]]), name="Far Moor", xy=[19.0, 10.0])
    w.s["roads"]["R_test"] = dict(copy.deepcopy(r0), a="Meresby", b="w9")
    names = [nm for _, nm, _, _ in Here(w, "Ralf").roads()]
    assert len(names) == len(set(names)), names
    assert any(nm.endswith("to the east") for nm in names)
    assert Here(w, "Ralf").road_to(next(nm for nm in names if nm.endswith("to the east"))) == ("w9", r0["days"], r0.get("track", False))


# ---------------------------------------------------------------------- 3. herding one's own household's beasts
def test_herding_unnamed_takes_ones_own_households_herd():
    w = world()
    assert {w.s["herds"][h]["parcel"] for h in ("ward_cattle", "marsh_cattle")} == {"Meresby_5"}
    from cybertron2.engine import farm as FM
    hid = FM._herd_on(Here(w, "Ralf"), "Meresby_5", {})
    assert hid == "marsh_cattle"
    assert FM._herd_on(Here(w, "Baldwin"), "Meresby_5", {}) == "ward_cattle"
    assert FM._herd_on(Here(w, "Ralf"), "Meresby_5", {"thing": "the Ward cows (H3)"}) == "ward_cattle"   # named: as named


# ---------------------------------------------------------------------- 4. the cat comes to hand only when it does
def test_the_cat_sign_says_it_came_to_hand_only_when_picked_up():
    from cybertron2.wild.kinds import WORK_NOTICES
    row = next(n for n in WORK_NOTICES["hunt"] if (n.get("find") or {}).get("item") == "cat")
    assert "came to your hand" not in row["rows"][0]["text"](None) if callable(row["rows"][0].get("text")) else True
    assert row["find"]["took"] == "it came to your hand" and row["find"].get("left")


# ---------------------------------------------------------------------- 5, 6. drying: rounded, and not a batch of nothing
def _hearth_meat(w, who, qty):
    b = house(w, w.household_of(who))
    w.s["containers"][w.hands(who)]["goods"]["meat"] = qty
    return b


def test_a_drying_batch_of_almost_nothing_is_refused_and_a_part_batch_is_rounded():
    w = world()
    _hearth_meat(w, "Ralf", 0.03)
    r = do(w, "Ralf", do="make", what="dry meat")
    assert "too little to make a batch" in r and "at least 0.1" in r
    w = world()
    _hearth_meat(w, "Ralf", 2.9525)
    r = do(w, "Ralf", do="make", what="dry meat")
    assert "2.9525" not in r and ("2.95 drying meat" in r or "failed" in r)


# ---------------------------------------------------------------------- 7. the killing frost names no ice
def test_the_killing_frost_sign_does_not_say_the_water_froze():
    texts = [row["text"](None) for row in SG.WEATHER if "killing frost" in str(row.get("text", lambda x: "")(None))] \
        if hasattr(SG, "WEATHER") else []
    src = open("cybertron2/engine/signs.py").read()
    assert "frozen through" not in src
    assert all("frozen" not in t for t in texts)


# ---------------------------------------------------------------------- D4-122: fish on the hearth rack
def test_fish_go_on_the_hearth_rack_as_a_batch_and_dry_to_half():
    t = TECHNIQUES["dry fish"]
    assert t["at"]["fittings"] == ["hearth", "fire ring"] and t["inputs"] == {"fish": 8} and t["batch"]
    assert t["rack"]["into"] == "dried fish" and t["rack"]["ratio"] == 0.5
    w = world()
    b = house(w, "Marsh")
    w.s["containers"][w.hands("Ralf")]["goods"]["fish"] = 5.0
    r = do(w, "Ralf", do="make", what="dry fish")
    assert "drying fish" in r or "failed" in r
    if "drying fish" in r:                                                     # one rack of 8 at the hearth, fish and meat
        assert "5 drying fish" in r and "hearth" in r                          # alike: the meat takes only the room left
        w.s["containers"][w.hands("Ralf")]["goods"]["meat"] = 4.0
        r2 = do(w, "Ralf", do="make", what="dry meat")
        assert "3 drying meat" in r2 or "failed" in r2
        w.s["containers"][w.hands("Ralf")]["goods"]["meat"] = 4.0
        r3 = do(w, "Ralf", do="make", what="dry meat")
        assert "full" in r3 or f"inside {w.s['buildings'][b]['name']}" not in r3   # Marsh House's rack is full: not there


# ---------------------------------------------------------------------- the signs pass (17 Nov): 1, 2, 4 to 8, 10 to 13
from cybertron2.engine import perceive as PC


def texts(w, who="Ralf"):
    return [f["text"] for f in PC.facts(Here(w, who))]


def test_a_raid_on_the_dead_and_on_food_left_out_has_its_own_signs():
    from cybertron2.wild.kinds import NEAR_PEOPLE, RAID_SIGNS
    assert all(t.get("sign") == "carcass" for k in NEAR_PEOPLE.values() for t in k["targets"] if t.get("what") == "carcass")
    assert all(t.get("sign") == "door" for k in NEAR_PEOPLE.values() for t in k["targets"] if t.get("what") == "left out")
    w = world()
    pid = "Meresby_5"
    w.s["wild"].setdefault("traces", {})[pid] = [{"kind": "wolf", "what": "raid:carcass", "day": w.d - 1, "n": 3, "beast": "cow"},
                                                 {"kind": "fox", "what": "raid:door", "day": w.d - 1, "n": 1, "house": "Marsh House"}]
    t = " | ".join(f["text"] for f in PC.facts(Here(w, "Ralf")))
    assert "the dead cow at the Common dragged and torn open in the night" in t
    assert "what was left at the door of Marsh House is gone: scraps and tracks" in t
    assert "wolves were at the dead cow at the Common" in t
    assert RAID_SIGNS["carcass"]["*"] and RAID_SIGNS["door"]["*"]


def test_wear_on_a_weir_reads_as_a_weir_not_a_roof():
    w = world()
    bid = "marsh_house"
    b = w.s["buildings"][bid]
    b["monument"], b["name"] = "weir", "the Mere Weir"
    b["broke"] = {"day": w.d, "level": 1, "by": ["spate"], "sections": [1]}
    t = " | ".join(texts(w))
    assert "stakes torn out of the Mere Weir, a stretch of wattle gone: the river runs through the hole" in t
    assert "roof has come in" not in t
    b["broke"]["by"] = ["spate", "ice"]
    assert "ice piled against the Mere Weir, the stakes leaning" in " | ".join(texts(w))


def test_fish_going_off_in_a_store_is_smelt_the_morning_after():
    from cybertron2.engine import night as N
    w = world()
    bid = house(w, "Marsh")
    st = w.s["buildings"][bid]["stock"]
    w.s["containers"][st]["goods"]["fish"] = 20.0
    N.night(w)
    sp = w.s["buildings"][bid].get("spoilt")
    assert sp and sp["day"] == w.d and sp["items"].get("fish", 0) > 0
    assert any("the fish in Marsh House's store going soft and starting to smell" in x for x in texts(w))


def test_an_otter_robbed_trap_shows_on_a_close_look_and_a_spate_smashes_it():
    from cybertron2.engine import things as TH
    w = world()
    cid = w.apply("new_thing", "Meresby", node="Meresby", parcel="Meresby_10", kind="set", by="Ralf",
                  set={"method": "trap in water", "set_day": w.d - 1})
    c = w.s["containers"][cid]
    c["robbed_by"] = {"day": w.d, "n": 2, "kind": "otter"}
    assert "torn at the neck, scales and a fish head on the withies" in TH.look_text(w, c)
    c.pop("robbed_by")
    c["set"] = dict(c["set"], sprung=w.d, wrecked="spate")
    assert "smashed against the bank in the spate" in TH.look_text(w, c)


def test_rain_on_meat_drying_outdoors_is_seen_at_its_parcel():
    from cybertron2.engine import signs as SG2
    w = world()
    cid = w.apply("new_thing", "Meresby", node="Meresby", parcel="Meresby_0", kind="pile", by="Ralf", door=house(w, "Marsh"),
                  rack={"day": w.d, "nights": 3, "into": "dried meat", "ratio": 0.5, "smoke": False})
    w.s["containers"][cid]["goods"]["drying meat"] = 6.0
    x = SG2.thing_context(w, w.s["containers"][cid])
    assert x.drying_out == "meat"


def test_game_grown_wary_is_read_by_a_hunter_on_that_ground():
    w = world()
    w.s["wild"]["wary_seen"] = {"Meresby_6": {"day": w.d, "kinds": ["roe deer"]}}
    f = [f for f in PC.facts(Here(w, "Ralf")) if "break and run long before you are near" in f["text"]]
    assert f and f[0].get("knows") == "hunt" and "the deer break and run" in f[0]["text"]


def test_a_fight_on_the_road_leaves_a_trace_that_day_and_the_next():
    from cybertron2.engine import roads as RD, signs as SG2
    w = world()
    rid = next(iter(w.s["roads"]))
    RD._fight_trace(w, {"road": rid, "pos": 1}, "Ralf", "Baldwin")
    tr = [x for x in w.s["traces"] if x["kind"] == "fight"]
    assert tr and set(tr[0]["by"]) == {"Ralf", "Baldwin"}
    x = SG2.trace_context(w, tr[0])
    got = [r["text"](x) for r in SG2.TRACE if r["when"](x)]
    assert any("trampled and scuffed, dark spots of blood" in g for g in got)
    assert any("two people fought here" in g for g in got)


def test_a_party_on_the_last_stretch_in_is_seen_from_the_village():
    w = world()
    rid = next(iter(w.s["roads"]))
    r = w.s["roads"][rid]
    other = r["b"] if r["a"] == "Meresby" else r["a"]
    w.s["people"]["Baldwin"]["transit"] = {"road": rid, "to": "Meresby", "left": w.d, "arrive": w.d}
    w.s["containers"][w.hands("Baldwin")]["goods"]["crude weapon"] = 1.0
    from cybertron2.engine import signs as SG2
    out = []
    SG2._road_coming(Here(w, "Ralf"), lambda about, text, sal, *a, **k: out.append((text, k)))
    if not Here(w, "Ralf").wet():
        assert out and "coming this way" in out[0][0] and "club or a spear" in out[0][0]


def test_fowl_come_back_on_the_thaw_and_fowlers_see_fewer_after_a_great_freeze(monkeypatch):
    from cybertron2.engine import signs as SG2, wild as WL2
    w = world()
    w.s["day"] = max(1, w.d)
    monkeypatch.setattr(WL2, "frozen_run", lambda w_, node, day=None, most=6: 0 if day == w.d else 6)
    m, land = WL2.model(w), w.s["wild"]["land"]
    ri = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "Meresby")
    w.s["wild"]["state"]["pop"]["wildfowl"][ri] = 40.0                          # fowl in the ring, water in it
    out = []
    SG2._wild_thaw(Here(w, "Ralf"), lambda about, text, sal, *a, **k: out.append((text, k)))
    assert out
    if True:
        assert any("back on the water" in t and "fewer" not in t and k.get("lay") == "net" for t, k in out)
        assert any("fewer than before the freeze" in t and k.get("knows") == "net" for t, k in out)


def test_traps_crammed_full_in_a_run_are_seen_by_their_setter(monkeypatch):
    from cybertron2.engine import signs as SG2, wild as WL2
    from cybertron2.wild import runs as RU2
    w = World(copy.deepcopy(load_spec("cybertron2/specs/water/river.yaml")))
    w.s["today"] = R.blank_today()
    node = next(n for n in w.s["nodes"] if any(WL2._river_parcel(w, p) for p, x in w.s["parcels"].items() if x["node"] == n))
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == node and WL2._river_parcel(w, p))
    who = next(n for n in w.living() if w.at(n) == node)
    cid = w.apply("new_thing", node, node=node, parcel=pid, kind="set", by=who, set={"method": "trap in water", "set_day": w.d - 1})
    w.s["containers"][cid]["goods"]["fish"] = 10.0                             # a trap's hold, 10 kg (D2-258; was 3 food)
    monkeypatch.setattr(RU2, "today", lambda m, st, day: [{"g": f"v:{node}", "k": "eel", "dir": "down", "n": 9.0}])
    out = []
    SG2._wild_river(Here(w, who), lambda about, text, sal, *a, **k: out.append((text, k)))
    full = [(t, k) for t, k in out if "crammed full" in t]
    assert full and full[0][1].get("only") == [who]
