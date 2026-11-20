"""Livelihood bots (W-69, D2-256; cybertron2/engine/bots_livelihood.py): the runs bot sets traps through a run window and not out of
it, lifts its own traps (and no one else's), keeps the catch in the house's store where the night eats the most perishable first,
smokes, dries and salts a surplus, works the weir's gap, and a run without `--bots runs` keeps run.bot_plan's smoke-test bot."""
import copy
import os

import pytest

from cybertron2.engine import bots_livelihood as BLV, keeping as KP, night as N, run as R, verbs as V, wild as WL
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

DIR = os.path.join(os.path.dirname(__file__), "..", "cybertron2", "specs", "nutrition")
AUTUMN = 4                                  # the arms start on summer's 4th day: day 4 is autumn's first, the eels' window


def world(arm, policy="runs"):
    """An arm of the runs world as `--bots <policy>` plays it (run.run writes the setting into the run's spec)."""
    spec = load_spec(os.path.join(DIR, f"runs_{arm}.yaml"))
    if policy:
        spec["bot_livelihood"] = policy
    return World(spec)


@pytest.fixture(scope="module")
def arms():
    return {a: world(a) for a in ("low", "medium", "high")}


def at_day(w0, d):
    w = copy.deepcopy(w0)
    w.s["day"] = d
    w.s["today"] = R.blank_today()
    w.s["events"] = []
    R.dawn(w)
    return w


def plan(w, who):
    return R.bot_plan(w, who)["actions"]


def play(w, names):
    """The day's work as run.py plays it: everyone's first act, then everyone's second, ...; the fallback not played."""
    plans = {n: plan(w, n) for n in names}
    used = {n: 0 for n in names}
    out = {n: [] for n in names}
    for i in range(max(len(p) for p in plans.values())):
        for n in names:
            if i < len(plans[n]):
                c = V.cost(Here(w, n), plans[n][i])
                if used[n] + c > w.units_for(n):
                    continue
                r = V.do(Here(w, n), Mind(w, n), plans[n][i])
                if not r.startswith("Refused"):
                    used[n] += c
                out[n].append(r)
    return out


def household(w, hh):
    return [m for m in w.members(hh) if m in w.agents_acting()]


def fisher(w, hh="Brook"):
    return [m for m in household(w, hh) if m != w.head(hh)][0]


def put_fish(w, cid, q):
    w.apply("create", "Eelmouth", dst=cid, item="fish", qty=q, why="test")


def test_the_flag_selects_the_policy_and_a_run_without_it_keeps_the_smoke_test_bot(arms):
    w = arms["low"]
    assert BLV.setting(w)["policy"] == "runs"
    old = world("low", None)
    assert not BLV.on(old) and "bot_livelihood" not in old.spec                         # the world file carries nothing
    with pytest.raises(SystemExit):
        BLV.check("farming")
    assert R.bot_plan(old, "Oliver")["why"] == "bot" and "fallback" not in R.bot_plan(old, "Oliver")
    assert R.bot_plan(w, "Oliver", kind="evening")["actions"] == []                     # nothing at the hearth


def test_traps_are_set_on_the_rivers_water_in_a_run_window_and_not_before(arms):
    w = at_day(arms["low"], 0)                                                          # summer: no run due
    assert not any(a.get("what") == "trap in water" for a in plan(w, fisher(w)))
    w = at_day(arms["low"], AUTUMN)
    assert "eel" in BLV.run_season(BLV.Day(w, fisher(w), BLV.setting(w)))
    acts = [a for a in plan(w, fisher(w)) if a.get("what") == "trap in water"]
    assert 0 < len(acts) <= min(BLV.setting(w)["traps"], w.units_for(fisher(w)))          # as many as her units allow
    river = {w.s["parcels"][p]["name"] for p in w.s["parcels"] if WL._river_parcel(w, p)}
    assert {a["at"] for a in acts} <= river
    res = play(w, household(w, "Brook"))
    assert sum("You set traps in the water" in r for r in res[fisher(w)]) == len(acts)


def test_the_morning_lifts_ones_own_traps_into_the_store_and_not_a_neighbours(arms):
    w = at_day(arms["low"], AUTUMN)
    play(w, w.agents_acting())
    w = at_day(w, AUTUMN + 1)
    me, other = fisher(w, "Brook"), fisher(w, "Shepherd")
    mine = [cid for cid, _ in BLV.traps(BLV.Day(w, me, BLV.setting(w)))]
    theirs = [cid for cid, _ in BLV.traps(BLV.Day(w, other, BLV.setting(w)))]
    for cid in mine[:2] + theirs[:1]:
        put_fish(w, cid, 0.4)
    from cybertron2.engine import things as TH
    for cid in theirs[:1]:
        TH.remember(w, me, cid, "found")                                           # seen, but not hers to lift
    acts = plan(w, me)
    assert [a["do"] for a in acts[:2]] == ["take", "take"]
    home = w.s["buildings"][w.dwellings(me)[0]]
    before = w.goods(home["stock"]).get("fish", 0.0)
    play(w, [me])
    assert all(w.goods(cid).get("fish", 0.0) < 1e-9 for cid in mine[:2])
    assert w.goods(theirs[0]).get("fish", 0.0) == pytest.approx(0.4)
    kept = w.goods(w.hands(me)).get("fish", 0.0)
    assert kept + w.goods(home["stock"]).get("fish", 0.0) - before == pytest.approx(0.8)
    assert kept <= BLV.Day(w, me, BLV.setting(w)).ration(me) + 1e-6                  # her supper in hand, the rest in store


def test_the_night_eats_the_fresh_fish_before_the_larder():
    order = N.eat_order(["dried meat", "roots", "fish", "smoked fish", "salt fish"])
    assert order.index("fish") < min(order.index("dried meat"), order.index("roots"), order.index("smoked fish"))


def test_a_surplus_is_smoked_at_the_racks_and_the_fire_tended_after(arms):
    w = at_day(arms["medium"], AUTUMN)
    head = w.head("Brook")
    bid = w.dwellings(head)[0]
    put_fish(w, w.s["buildings"][bid]["stock"], 30)
    assert {"do": "make", "what": "smoke fish"} in plan(w, head)
    play(w, [head])
    racks = KP.active_racks(w, bid)
    assert racks and sum(KP.curing(c) for c in racks.values()) == pytest.approx(30, abs=0.5)
    w = at_day(w, AUTUMN + 1)
    assert {"do": "work", "what": "tend the smoke", "at": w.s["buildings"][bid]["name"]} in plan(w, head)
    assert any("You tended the fire" in r for r in play(w, [head])[head])


def supper(w, head):
    return BLV._suppers(BLV.Day(w, head, BLV.setting(w)))


def test_fish_the_house_eats_tonight_are_not_kept(arms):
    w = at_day(arms["medium"], AUTUMN)
    head = w.head("Brook")
    put_fish(w, w.s["buildings"][w.dwellings(head)[0]]["stock"], supper(w, head) + 2)      # tonight's suppers and a little over
    assert not any(a.get("what") in ("smoke fish", "dry fish", "salt fish") for a in plan(w, head))


def test_with_no_racks_fish_are_dried_at_the_hearth(arms):
    w = at_day(arms["low"], AUTUMN)
    head = w.head("Marsh")
    bid = w.dwellings(head)[0]
    put_fish(w, w.s["buildings"][bid]["stock"], supper(w, head) + 6)
    assert {"do": "make", "what": "dry fish"} in plan(w, head)
    assert any("drying fish" in r for r in play(w, [head])[head])


def test_fish_beyond_the_racks_are_salted_with_the_salt_houses_salt(arms):
    w = at_day(arms["high"], AUTUMN)
    head = w.head("Marsh")
    bid = w.dwellings(head)[0]
    put_fish(w, w.s["buildings"][bid]["stock"], supper(w, head) + 60)
    acts = plan(w, head)
    salt = next(a for a in acts if a.get("what") == "salt fish")
    assert salt["qty"] >= 1
    res = " ".join(play(w, [head])[head])
    assert "smoking fish" in res and "drying fish" in res and "salt fish" in res


def gap_acts(w, who):
    return [a["to"] for a in plan(w, who) if a.get("thing") == "gap"]


def test_the_weirs_gap_is_shut_on_a_run_night_whatever_the_river_and_opened_only_in_high_water_without_one(arms, monkeypatch):
    w = at_day(arms["high"], 0)
    head = w.head("Marsh")
    assert gap_acts(w, head) == ["open"]                                                  # out of the windows
    w.s["buildings"]["marsh_weir"]["gap"] = "open"
    w = at_day(w, AUTUMN)
    monkeypatch.setattr(BLV, "run_here", lambda day: {})
    monkeypatch.setattr(BLV, "river_tonight", lambda day: "normal")
    assert gap_acts(w, head) == ["shut"]                                                  # the window, the river as usual
    w.s["buildings"]["marsh_weir"]["gap"] = "shut"
    monkeypatch.setattr(BLV, "river_tonight", lambda day: "flood")
    assert gap_acts(w, head) == ["open"]                                                  # high water and no run: spare the weir
    monkeypatch.setattr(BLV, "run_here", lambda day: {"eel": 40.0})
    assert gap_acts(w, head) == []                                                        # the run is here: it stays shut
    assert not gap_acts(w, fisher(w, "Brook"))                                            # only the weir's holder sets it


def test_a_run_is_seen_at_the_water_only_at_three_heads_or_more(arms):
    w = at_day(arms["high"], AUTUMN)
    st = w.s["wild"]["state"]
    day = BLV.Day(w, w.head("Marsh"), BLV.setting(w))
    d = WL.eco_day(w)
    st["runs"]["pulses"] = [{"k": "eel", "g": "v:Eelmouth", "d": d, "n": 2.5, "dir": "down"},
                            {"k": "salmon", "g": "v:Eelmouth", "d": d, "n": 4.0, "dir": "up"}]
    assert BLV.run_here(day) == {"salmon": 4.0}


def test_a_worn_weir_is_mended_by_its_household_split_among_them_and_not_on_a_spate_night(arms, monkeypatch):
    w = at_day(arms["high"], AUTUMN)
    b = w.s["buildings"]["marsh_weir"]
    b["sections"] = [dict(sc, level=3) for sc in WL.sections(b)]                          # six levels short
    monkeypatch.setattr(BLV, "river_tonight", lambda day: "normal")
    marsh = household(w, "Marsh")
    mends = {m: sum(a.get("what") == "repair" for a in plan(w, m)) for m in marsh}
    most = BLV.setting(w)["mend_most"]
    assert 0 < sum(mends.values()) <= 6 and max(mends.values()) <= most
    assert mends[w.head("Marsh")] <= min(mends[m] for m in marsh if m != w.head("Marsh") and w.s["people"][m]["stage"] == "adult")
    assert not any(a.get("what") == "repair" for a in plan(w, fisher(w, "Brook")))        # another household's weir
    play(w, marsh)
    assert sum(int(sc["level"]) for sc in WL.sections(w.s["buildings"]["marsh_weir"])) == 9 + sum(mends.values())
    monkeypatch.setattr(BLV, "river_tonight", lambda day: "spate")
    assert not any(a.get("what") == "repair" for m in marsh for a in plan(w, m))


def test_the_weirs_traps_are_lifted_once_by_its_household(arms):
    from cybertron2.engine import things as TH
    w = at_day(arms["high"], AUTUMN)
    cid = WL._weir_trap_make(w, "marsh_weir", w.s["buildings"]["marsh_weir"])       # made the first night the weir stands
    put_fish(w, cid, 2.0)
    marsh = household(w, "Marsh")
    for m in marsh:
        TH.remember(w, m, cid, "found")
    lifts = [m for m in marsh for a in plan(w, m) if a.get("do") == "take" and a.get("from") == w.s["containers"][cid].get("tag")]
    assert len(lifts) == 1
    assert not any(a.get("do") == "take" for a in plan(w, fisher(w, "Brook")))            # not another household's


def test_traps_are_set_whatever_the_river_unless_the_knob_says(arms, monkeypatch):
    w = at_day(arms["low"], AUTUMN)
    monkeypatch.setattr(BLV, "river_tonight", lambda day: "flood")
    assert any(a.get("what") == "trap in water" for m in w.agents_acting() for a in plan(w, m))
    w.spec = dict(w.spec, bot_livelihood={"policy": "runs", "trap_stop": ["spate", "flood"]})
    assert not any(a.get("what") == "trap in water" for m in w.agents_acting() for a in plan(w, m))


def test_wild_food_is_gathered_only_where_it_is_worth_the_work(arms):
    w = at_day(arms["low"], AUTUMN)
    who = fisher(w)
    day = BLV.Day(w, who, BLV.setting(w))
    acts = BLV._forage_plan(day, 6)
    assert acts and all(f >= day.s["forage_least"] for _, f in acts)
    assert all(a["what"] == "gather wild food" and a.get("looking for") for a, _ in acts)
    for pid in w.s["parcels"]:                                                            # the land stripped bare
        for r in w.s["parcels"][pid]["res"].values():
            if "S" in r:
                r["S"] = 0.0
    assert BLV._forage_plan(BLV.Day(w, who, BLV.setting(w)), 6) == []


@pytest.mark.slow
def test_a_week_of_the_run_played_by_the_engine(tmp_path):
    """The engine's own day (run.run with --bots) through the eels' first nights: traps set and lifted, no one else's taken."""
    import json
    R.run(os.path.join(DIR, "runs_medium.yaml"), str(tmp_path), days=7, workers=1, bots="runs")
    lines = [r for x in map(json.loads, open(tmp_path / "turns.jsonl")) for r in x["results"]]
    assert sum("You set traps in the water" in r for r in lines) >= 10
    assert any(r.startswith("You took") and "from your wicker traps" in r for r in lines)
    assert not any("from the wicker traps" in r for r in lines)                       # nobody's traps but one's own
