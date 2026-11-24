"""Stage 2 of the fishing, hunting and materials wave: taking and making (W-98; docs/cybertron2/proposals/w73_design/u1_water.md,
u2_taking.md, u3_making.md, each under its "Decisions since" table). One test (or a few) for each rule built: set from the hands and
tend (fault 12; D2-294, D2-304, D2-305), the set record, the gear's two lives and mending (D2-310, D2-329), recipes in kg by their
batch (u3 §2), what each level is shown (D2-263), the shallows by water type with their signs (D2-316, D2-317), the ice (u1 §4), the
fen's reach and wreck (u1 §6), the pinch (u1 §5), the willow (u3 §1.1), the flax strip (B35), the water-only runs world (D2-316,
D2-330 C5) and the making gate check (u3 §7)."""
import copy

import pytest

from cybertron2.engine import clocks as CK, gear as GE, knowledge as KN, night as N, run as R, verbs as V
from cybertron2.engine.data import ITEMS, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec
from cybertron2.wild import runs as RU, water as WT
from tests.test_cybertron2_water5_river import adults, do, fresh, morning, pulse, river, water   # noqa: F401


def _knows(w, who, tech, level="known"):
    w.s["know"].setdefault(who, {})[tech] = {"level": level, "skill": 1.0, "seen": 0, "wins": 0, "fails": 0, "source": "", "since": 0}


def _give(w, who, item, n):
    w.apply("create", w.s["people"][who]["at"], dst=w.s["people"][who]["hands"], item=item, qty=float(n), why="test")


def _setter(river_w, traps=6):
    w = fresh(river_w)
    node = "Saltwell"
    who = adults(w, node)[0]
    _knows(w, who, "trap in water")
    h = w.s["containers"][w.s["people"][who]["hands"]]                             # the world seeds six (Q-100): start from none
    h["goods"].pop("wicker trap", None)
    (h.get("pieces") or {}).pop("wicker trap", None)
    if traps:
        _give(w, who, "wicker trap", traps)
    return w, node, who, water(w, node), w.s["parcels"][water(w, node)]["name"]


def _sets(w, who):
    return [(k, c) for k, c in sorted(w.s["containers"].items()) if c.get("kind") == "set" and c.get("by") == who]


def _hands(w, who):
    return w.s["containers"][w.s["people"][who]["hands"]]


# ---------------------------------------------------------------------- set from the hands (u2 §3; fault 12)
def test_set_needs_gear_in_hand_and_lays_up_to_six_for_one_unit(river):
    w, node, who, pid, pn = _setter(river, traps=8)
    assert V.cost(Here(w, who), {"do": "set", "what": "wicker traps", "at": pn}) == 1
    r = do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    assert r.startswith("You set 6 wicker traps") and "You hold 2 more" in r, r
    (cid, c), = _sets(w, who)
    assert GE.laid(c) == {"wicker trap": 6} and len(GE.laid_pieces(c, "wicker trap")) == 6
    assert c["household"] == w.household_of(who) and c["set"]["state"] == "fishing"
    assert _hands(w, who)["goods"]["wicker trap"] == pytest.approx(2.0)        # gear moved from the hands into the thing
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    r = do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    assert r.startswith("Refused") and "no wicker traps in hand" in r and "tend T" in r, r   # names the gear standing


def test_a_set_with_nothing_in_hand_is_refused_and_points_to_none_standing(river):
    w, node, who, pid, pn = _setter(river, traps=0)
    r = do(w, who, {"do": "gather", "what": "trap in water", "at": pn})
    assert r.startswith("Refused") and "You have no wicker traps in hand" in r, r
    assert not _sets(w, who)                                                       # no set made from nothing (fault 12)


def test_tend_takes_all_of_ones_own_there_and_sets_them_again_and_up_brings_them_home(river):
    w, node, who, pid, pn = _setter(river, traps=12)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    for cid, _ in _sets(w, who):
        w.apply("create", node, dst=cid, item="fish", qty=2.0, why="test")
    assert V.cost(Here(w, who), {"do": "tend", "what": "traps", "at": pn}) == 1
    r = do(w, who, {"do": "tend", "what": "traps", "at": pn})
    assert r.count("You tended your wicker traps") == 2 and "You set them again" in r, r   # both of one's own, one act (D2-304)
    assert Here(w, who).carried()["fish"] == pytest.approx(4.0)
    tag = _sets(w, who)[0][1]["tag"]
    r = do(w, who, {"do": "tend", "thing": tag, "up": True})
    assert "You took them up: 6 wicker traps in hand" in r, r
    assert Here(w, who).sound_held("wicker trap") == 6
    assert _sets(w, who)[0][1]["set"]["state"] == "up" and _sets(w, who)[0][0] not in Here(w, who).sets()


def test_lift_check_empty_walk_and_collect_read_as_tend(river):
    w, node, who, pid, pn = _setter(river)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    for verb in ("lift", "check", "empty", "walk", "collect"):
        r = do(w, who, {"do": verb, "what": "traps"})
        assert r.startswith("You tended your wicker traps"), (verb, r)


def test_the_technique_named_alone_tends_sets_or_refuses(river):
    w, node, who, pid, pn = _setter(river)
    r = do(w, who, {"do": "gather", "what": "wicker traps", "at": pn})
    assert r.startswith("You set 6 wicker traps"), r                               # none standing, gear in hand: set
    r = do(w, who, {"do": "gather", "what": "wicker traps", "at": pn})
    assert r.startswith("You tended your wicker traps"), r                         # one's own standing: tended


def test_a_household_member_tends_the_households_gear_and_a_leaver_does_not(river):
    w, node, who, pid, pn = _setter(river)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    hh = w.household_of(who)
    mate = next(m for m in w.s["institutions"][hh]["members"] if m != who and w.s["people"][m]["stage"] == "adult"
                and w.s["people"][m].get("at") == node)
    r = do(w, mate, {"do": "tend", "what": "traps", "at": pn})
    assert r.startswith("You tended your wicker traps"), r                         # the household's things, every member's (D2-305)
    w.apply("leave", node, person=who, inst=hh)
    r = do(w, who, {"do": "tend", "what": "traps", "at": pn})
    assert r.startswith("Refused") and "no wicker traps" in r, r                   # the setter left: no longer theirs, unnamed


def test_anothers_gear_named_is_emptied_as_theft(river):
    w, node, who, pid, pn = _setter(river)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    (cid, c), = _sets(w, who)
    w.apply("create", node, dst=cid, item="fish", qty=3.0, why="test")
    thief = next(x for x in adults(w, node) if w.household_of(x) != w.household_of(who))
    r = do(w, thief, {"do": "tend", "what": "traps", "at": pn})
    assert r.startswith("Refused") and f"{c['tag']} there is {who}'s" in r, r      # unnamed: never another's
    from cybertron2.engine import things as TH
    TH.remember(w, thief, cid, "saw")                                              # one names what one has seen
    r = do(w, thief, {"do": "tend", "thing": c["tag"]})
    assert "not yours to take from" in r and "Whether anyone saw, you will learn" in r, r
    assert any(t.get("thing") == cid for t in w.s["today"]["thefts"])


def test_a_kill_on_several_of_ones_own_needs_its_target():
    """D2-304: slaughtering from a herd when several of one's own stand there is refused, naming them."""
    from cybertron2.engine import farm as FM
    w = World(load_spec("cybertron2/specs/valley_s5.yaml"))
    w.s["today"] = R.blank_today()
    hid, h = next((k, x) for k, x in sorted(w.s["herds"].items()) if FM.head(x) > 1)
    holder = next(c["claimant"] for c in w.s["claims"].values() if tuple(c["thing"]) == ("herd", hid))
    who = next(m for m in w.s["institutions"][holder]["members"] if w.s["people"][m]["stage"] == "adult") \
        if holder in w.s["institutions"] else holder
    new = w.apply("new_herd", h["node"], like=hid, parcel=h["parcel"])
    w.apply("set", h["node"], ref=("herd", new), field="cows", value=1)
    w.apply("set", h["node"], ref=("herd", new), field="count", value=1)
    w.apply("claim", h["node"], thing=("herd", new), claimant=holder, rights="all", grounds="seeded")
    w.s["people"][who]["at"] = h["node"]
    r = V.do(Here(w, who), Mind(w, who), {"do": "work", "what": "slaughter", "at": w.s["parcels"][h["parcel"]]["name"]})
    assert r.startswith("Refused") and "more than one herd" in r, r


# ---------------------------------------------------------------------- two lives and mending (u3 §3; D2-310, D2-329)
def test_lives_in_nights_at_the_calendar_and_in_acts_at_the_factor():
    assert GE.full_uses("wicker trap") == 20 and GE.full_uses("gill net") == 25 and GE.full_uses("set line") == 6
    assert GE.full_uses("fishing rod") == 14                                       # 210 real acts at 1/15
    assert GE.life_of("crude tool") == 19 and GE.life_of("copper tool") == 65 and GE.life_of("bedroll") == 30
    assert GE.LIVES["gill net"]["rot"][0] == 0.5                                   # about 16 nights in the water (D2-329)


def test_a_piece_wears_by_nights_set_breaks_and_is_brought_home_to_mend(river, monkeypatch):
    w, node, who, pid, pn = _setter(river)
    monkeypatch.setattr(WT, "iced", lambda *a, **k: False)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    (cid, c), = _sets(w, who)
    for _ in range(3):
        GE.worn_night(w, cid)
    assert all(p["life"] == 17.0 for p in GE.laid_pieces(w.s["containers"][cid], "wicker trap"))
    ps = [dict(p, life=0.0) if i < 2 else p for i, p in enumerate(GE.laid_pieces(w.s["containers"][cid], "wicker trap"))]
    w.apply("gear_night", node, cid=cid, field="pieces", value={"wicker trap": ps})
    assert GE.fishing(w.s["containers"][cid]) == 4                                 # a broken piece fishes no more
    r = do(w, who, {"do": "tend", "what": "traps", "at": pn})
    assert "2 are worn past use and want mending: you took them home" in r, r
    assert Here(w, who).sound_held("wicker trap") == 0 and _hands(w, who)["goods"]["wicker trap"] == pytest.approx(2.0)
    _knows(w, who, "wicker trap")
    _give(w, who, "withies", 1)
    r = do(w, who, {"do": "make", "what": "mend"})
    assert r.startswith("You mended your 2 wicker traps") and "10 more nights set" in r, r
    ps = GE.pieces(_hands(w, who), "wicker trap", w)
    assert [p["life"] for p in ps] == [10.0, 10.0]                                 # half the full uses back
    assert _hands(w, who)["goods"]["withies"] == pytest.approx(1 - 2 * 0.045)       # a tenth of the materials a piece


def test_mending_never_gives_back_rot_and_a_rough_failure_spoils_only_the_materials(river):
    w, node, who, pid, pn = _setter(river, traps=1)
    h = _hands(w, who)
    GE.wear(w, h, "wicker trap", 20)
    h["pieces"]["wicker trap"][0]["rot"] = 0.4
    _knows(w, who, "wicker trap")
    _give(w, who, "withies", 1)
    do(w, who, {"do": "make", "what": "mend"})
    assert h["pieces"]["wicker trap"][0]["rot"] == 0.4 and h["pieces"]["wicker trap"][0]["life"] == 10.0
    GE.wear(w, h, "wicker trap", 10)
    _knows(w, who, "wicker trap", "rough")
    outs = set()
    for d in range(12):                                                            # at rough, the class's odds
        w.s["day"] = 100 + d
        w.s["today"] = R.blank_today()
        r = do(w, who, {"do": "make", "what": "mend"})
        outs.add("went wrong" in r)
        if "went wrong" in r:
            assert h["pieces"]["wicker trap"][0]["life"] == 0.0                     # the thing as it was
            break
    assert True in outs


def test_gear_rots_wet_in_the_water_and_a_rotten_piece_is_gone(river):
    w, node, who, pid, pn = _setter(river)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    (cid, c), = _sets(w, who)
    for _ in range(3):
        GE.rot_night(w)
    rot = GE.laid_pieces(w.s["containers"][cid], "wicker trap")[0]["rot"]
    assert rot == pytest.approx(3 / (2.0 * w.year_days()), rel=1e-3)               # the wet rate: 2 world years
    ps = [dict(p, rot=0.999) for p in GE.laid_pieces(w.s["containers"][cid], "wicker trap")]
    w.apply("gear_night", node, cid=cid, field="pieces", value={"wicker trap": ps})
    GE.rot_night(w)
    assert GE.laid(w.s["containers"][cid]) == {} and w.s["containers"][cid]["set"]["lost"]["rotted"] == 6


def test_pieces_move_with_the_goods_most_worn_first(river):
    w, node, who, pid, pn = _setter(river, traps=3)
    h = _hands(w, who)
    GE.wear(w, h, "wicker trap", 5)
    other = adults(w, node)[1]
    w.apply("transfer", node, src=h and w.s["people"][who]["hands"], dst=w.s["people"][other]["hands"], item="wicker trap", qty=1)
    assert GE.pieces(_hands(w, other), "wicker trap", w)[0]["life"] == 15.0         # the most worn left first
    assert [p["life"] for p in GE.pieces(h, "wicker trap", w)] == [20.0, 20.0]


# ---------------------------------------------------------------------- the recipes in kg, by their batch (u3 §2)
@pytest.mark.parametrize("factor,trap,net", [("1/15", (1, 5), (2, 1)), ("1/7", (1, 2), (4, 1))])
def test_recipe_units_and_batches_follow_the_factor(factor, trap, net):
    class W:
        spec = {"capital_factor": factor}

        def year_days(self):
            return 32
    w = W()
    t, g = TECHNIQUES["wicker trap"], TECHNIQUES["gill nets"]
    assert (CK.act_units(t, w), CK.batch_of(t, w)) == trap
    assert (CK.act_units(g, w), CK.batch_of(g, w)) == net
    assert t["inputs"] == {"withies": 0.45} and ITEMS["wicker trap"]["weight"] == 2.5
    for k in GE.RECIPES:
        assert TECHNIQUES[k]["verb"] == "make" and CK.act_units(TECHNIQUES[k], w) >= 1   # no act is free


def test_a_make_of_n_pieces_costs_units_by_its_batch(river):
    w, node, who, pid, pn = _setter(river, traps=0)
    _knows(w, who, "wicker trap")
    _give(w, who, "withies", 5)
    assert V.cost(Here(w, who), {"do": "make", "what": "wicker trap", "qty": 6}) == 2
    r = do(w, who, {"do": "make", "what": "wicker trap", "qty": 2})
    assert r.startswith("You made 2 wicker traps (1 unit; the same unit would have made 5)") and "20 nights set" in r, r


# ---------------------------------------------------------------------- what each level is shown (D2-263; u3 §4)
def test_a_craft_line_renders_at_each_level():
    known = KN.craft_line("wicker trap", "known", {"skill": 1.0})
    assert "up to 5 wicker traps a unit, each from 0.45 withies" in known and "20 nights set" in known
    capable = KN.craft_line("wicker trap", "capable", {"skill": 1.0})
    assert "up to 5 wicker traps a unit" in capable and "times in 4" in capable and "20 nights" not in capable
    rough = KN.craft_line("gill nets", "rough", {})
    assert rough == "making a gill net (a rough idea: 1 cord and 0.1 stone, at a house)"
    assert KN.craft_line("gill nets", "aware", {"source": "you have seen one at the Marshs'"}) == \
        "making a gill net (you have seen one at the Marshs')"
    assert "up to 40 fish and 10 salt" in KN.craft_line("salt fish", "known", {"skill": 1.0})
    assert "best in winter" in KN.craft_line("cut withies", "known", {"skill": 1.0})


# ---------------------------------------------------------------------- the shallows (u1 §2; D2-316, D2-317)
def test_shallows_seeded_on_every_water_and_fen_parcel_by_water_type(river):
    w = fresh(river)
    for pid, p in w.s["parcels"].items():
        if p["cover"] in ("water", "fen"):
            t = WT.water_type(w, pid)
            assert p["res"]["shallows"]["K"] == pytest.approx(WT.SHALLOWS["K"][t] * p["size"]), (pid, t)
        else:
            assert "shallows" not in p["res"]


def test_shallows_renew_by_season_and_not_under_ice():
    r = {"S": 0.5, "K": 10.0}
    s = dict(r)
    for _ in range(20):
        s["S"] = WT.renew(s, "summer", False)
    assert s["S"] > 5.0                                                            # back above half in about 20 summer nights
    s = dict(r)
    for _ in range(15):
        s["S"] = WT.renew(s, "winter", False)
    assert s["S"] < 1.0
    assert WT.renew(r, "summer", True) == 0.5                                      # nothing under ice


def test_the_edge_draws_the_shallows_and_is_refused_only_when_stripped_with_no_run(river, monkeypatch):
    monkeypatch.setattr(WT, "iced", lambda *a, **k: False)
    monkeypatch.setattr(WT, "ice", lambda *a, **k: "open")
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    who = adults(w, node)[0]
    S0 = w.s["parcels"][pid]["res"]["shallows"]["S"]
    r = do(w, who, {"do": "gather", "what": "fish by hand", "at": w.s["parcels"][pid]["name"]})
    assert "shallows" in r and w.s["parcels"][pid]["res"]["shallows"]["S"] <= S0, r
    w.s["parcels"][pid]["res"]["shallows"]["S"] = 0.0
    r = do(w, who, {"do": "gather", "what": "fish by hand", "at": w.s["parcels"][pid]["name"]})
    assert r.startswith("Refused") and "fished out for now, and nothing is running" in r and "no fish" not in r, r
    assert KN.resolve("fish", "gather") is None                                    # "fish" names no one way (u2 §4.6)


def test_the_pinch_by_water(river):
    w = fresh(river)
    pid = water(w, "Saltwell")
    assert WT.pinch(w, pid) in (0.3, 0.1)
    from tests.test_cybertron2_water5_river import put_weir
    put_weir(w, "Saltwell", gap="shut")
    assert WT.pinch(w, pid) == 1.0                                                 # below a shut weir the fish crowd the gap


def test_shallows_signs_read_the_parcels_own_stock(river):
    from cybertron2.engine import signs as SG
    rows = [r for r in SG.WILD if "shallows" in str(r.get("land") or "")]
    assert len(rows) >= 3 and all("p" not in r for r in rows)                        # by the one rule (guides/senses.md)


# ---------------------------------------------------------------------- the ice (u1 §4)
@pytest.mark.parametrize("run,river_ice,big_ice", [(0, "open", "open"), (1, "edges", "open"), (2, "edges", "edges"),
                                                   (4, "over", "edges"), (5, "over", "over")])
def test_ice_by_water_type(river, monkeypatch, run, river_ice, big_ice):
    from cybertron2.engine import wild as WL
    w = fresh(river)
    monkeypatch.setattr(WL, "frozen_run", lambda w_, node, day=None, most=6: run)
    pid = water(w, "Saltwell")
    monkeypatch.setattr(WT, "_big_stretch", lambda w_, node: False)
    assert WT.ice(w, pid) == river_ice
    monkeypatch.setattr(WT, "_big_stretch", lambda w_, node: True)
    assert WT.ice(w, pid) == big_ice


def test_set_gear_is_idle_under_ice_and_setting_is_refused(river, monkeypatch):
    w, node, who, pid, pn = _setter(river, traps=12)
    do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    monkeypatch.setattr(WT, "iced", lambda w_, p, day=None: True)
    monkeypatch.setattr(WT, "ice", lambda w_, p, day=None: "edges")
    r = do(w, who, {"do": "set", "what": "wicker traps", "at": pn})
    assert r.startswith("Refused") and "are ice" in r, r
    (cid, c), = _sets(w, who)
    pulse(w, node, kind="eel", n=800.0)
    N.night(w)
    c = w.s["containers"][cid]
    assert c["set"]["state"] == "idle" and not any(q > 0 for q in c["goods"].values())
    assert all(p["life"] == 19.0 for p in GE.laid_pieces(c, "wicker trap"))       # its nights still run


def test_eels_are_held_at_an_iced_stretch_and_salmon_pass_under_edge_ice(river):
    w = fresh(river)
    from cybertron2.engine import wild as WL
    m = WL.model(w)
    st = copy.deepcopy(w.s["wild"]["state"])
    d = WL.eco_day(w)
    g = "v:Saltwell"
    st["runs"]["pulses"] = [{"k": "eel", "g": g, "d": d, "n": 50.0, "dir": "down"},
                            {"k": "salmon", "g": g, "d": d, "n": 20.0, "dir": "up", "to": g}]
    RU.advance(m, st, d, {}, None, iced={g: "edges"})
    held = [p for p in st["runs"]["pulses"] if p["g"] == g and p["d"] == d + 1]
    assert any(p["k"] == "eel" and p["n"] == 50.0 for p in held)                   # the eels wait for an open night
    assert not any(p["k"] == "salmon" and p["d"] == d + 1 and p["g"] == g for p in held)   # the salmon go on under the edges


# ---------------------------------------------------------------------- the fen (u1 §6)
def test_a_fen_beside_the_river_meets_half_the_run_and_one_away_none(river):
    w = fresh(river)
    from cybertron2.engine import wild as WL
    fens = [p for p, x in w.s["parcels"].items() if x["cover"] == "fen" and x["node"] == "Saltwell"]
    reach = {p: WT.run_reach(w, p) for p in fens}
    beside = [p for p in fens if any(WL._river_parcel(w, q) for q in w.s["parcels"][p]["adj"])]
    for p in fens:
        assert reach[p] == (0.5 if p in beside else 0.0)
    assert WT.run_reach(w, water(w, "Saltwell")) == 1.0
    assert WT.fen_wreck("flood") == 0.05 and WT.fen_wreck("spate") == 0.02


# ---------------------------------------------------------------------- the willow (u3 §1.1)
def test_willow_on_the_fen_and_the_banks_and_cut_withies_draws_it(river):
    w = fresh(river)
    fen = next(p for p, x in w.s["parcels"].items() if x["cover"] == "fen" and x["node"] == "Saltwell")
    assert w.s["parcels"][fen]["res"]["willow"]["K"] == 60.0 * w.s["parcels"][fen]["size"]
    who = adults(w, "Saltwell")[0]
    S0 = w.s["parcels"][fen]["res"]["willow"]["S"]
    r = do(w, who, {"do": "gather", "what": "cut withies", "at": w.s["parcels"][fen]["name"]})
    assert "withies" in r and w.s["parcels"][fen]["res"]["willow"]["S"] < S0, r
    from cybertron2.wild import willow as WI
    res = {"S": 2.0, "K": 50.0, "K0": 60.0}
    assert WI.renew(res, {"first_spring": False}) == 2.0
    assert WI.renew(res, {"first_spring": True}) == pytest.approx(51.0)            # back to K in spring, K mending a tenth


# ---------------------------------------------------------------------- the flax strip (u3 §1.3; B35)
def test_a_small_sowing_of_flax_is_a_strip_beside_the_main_crop():
    from cybertron2.engine import farm as FM, strips as STR
    w = World(load_spec("cybertron2/specs/valley_s5.yaml"))
    w.s["today"] = R.blank_today()
    pid, par = next((p, x) for p, x in sorted(w.s["parcels"].items()) if x["cover"] == "field" and FM.standing(x))
    h, rec, crop = FM.standing(par)[0]
    holder = h or next(c["claimant"] for c in w.s["claims"].values() if tuple(c["thing"]) == ("parcel", pid))
    who = next(m for m in w.s["institutions"][holder]["members"] if w.s["people"][m]["stage"] in ("adult", "elder")) \
        if holder in w.s["institutions"] else holder
    w.s["people"][who]["at"] = par["node"]
    _give(w, who, "flax seed", 1.0)
    before = copy.deepcopy(rec["crop"])
    r = V.do(Here(w, who), Mind(w, who), {"do": "work", "what": "sow", "item": "flax seed", "qty": 0.3, "at": par["name"]})
    assert "in a strip of" in r and "of a plot" in r, r
    rec = FM.record(w.s["parcels"][pid], h)
    assert rec["crop"]["kind"] == before["kind"] and rec["crop"]["seed"] == before["seed"]   # the main crop stands
    (s,) = STR.strips(w.s["parcels"][pid], h)
    assert s["crop"] == "flax" and s["area"] == pytest.approx(0.3 / 11, abs=1e-4)
    assert STR.is_strip("flax", 2.75) and not STR.is_strip("flax", 3.0)            # up to a quarter of a plot


# ---------------------------------------------------------------------- the water-only runs world (D2-316; D2-330 C5)
def test_the_runs_world_is_water_only_with_small_resident_fish_shallows_and_seeded_traps():
    w = World(load_spec("cybertron2/specs/nutrition/runs_high.yaml"))
    isel = next(p for p, x in w.s["parcels"].items() if x["name"] == "the Isel")
    assert 0 < w.s["parcels"][isel]["res"]["fish"]["K"] <= 10.0 and w.s["parcels"][isel]["res"]["shallows"]["K"] > 0
    fen = next(p for p, x in w.s["parcels"].items() if x["cover"] == "fen")
    assert w.s["parcels"][fen]["res"]["shallows"]["K"] == WT.SHALLOWS["K"]["fen"] * w.s["parcels"][fen]["size"]
    setters = [n for n, k in w.s["know"].items() if (k.get("trap in water") or {}).get("level") in ("capable", "known")
               and w.s["people"][n]["stage"] == "adult"]
    assert setters and all(w.goods(w.hands(n)).get("wicker trap") == 6 for n in setters)
    assert all("wicker trap" in w.s["know"][n] for n in setters)
    assert any(w.goods(w.hands(n)).get("gill net") == 1 for n in setters)          # the weir's expert's net


# ---------------------------------------------------------------------- the making gate check (u3 §7)
def test_the_making_gates_find_the_runs_worlds_missing_stone_and_can_be_switched_off():
    from cybertron2.landgen import gates as G
    w = World(load_spec("cybertron2/specs/nutrition/runs_high.yaml"))
    fs = G.making_gates(w)
    assert any(f.check == "M4" for f in fs)                                        # no rock within a day of Eelmouth
    assert not [f for f in fs if f.check == "M8" and "CRASH" in f.text]             # every make tried: no code gate
    assert G.making_gates(w, {"gates": {"making": False}}) == []
    assert not [f for f in G.making_gates(w, {"gates": {"M4": False}}) if f.check == "M4"]


def test_a_setter_with_no_gear_and_no_time_to_make_it_is_warned():
    from cybertron2.landgen import gates as G
    w = World(load_spec("cybertron2/specs/nutrition/runs_low.yaml"))
    assert any(f.check == "M3" for f in G.making_gates(w, {"gates": {"M8": False}}))   # the low arm holds no traps
