"""Stage 1 of the fishing, hunting and materials wave: the basis in code (W-97; docs/cybertron2/proposals/w73_design/u0_basis.md).
One test (or a few) for each fault fixed and each rule built: the options list gone (D2-286), the fishing faults (u2 §6), a run's fish
learning no wariness (u1 §7a), the weir's cost in one place (D2-302), practice for every build act (u7 §5.2), the signs reworded
(D2-269), the clocks (u0 §4), the floor and batches (u0 §5), the keeping curve (D2-289), fuel a night (D2-290) and the handling units
(D2-288)."""
import copy

import pytest

from cybertron2.engine import knowledge as KN, prompt as PR, run as R
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec


@pytest.fixture(scope="module")
def hamlet():
    w = World(load_spec("cybertron2/specs/valley_s5.yaml"))
    w.s["today"] = R.blank_today()
    return w


# ---------------------------------------------------------------------- the options list (D2-286)
def test_no_prompt_contains_the_options_list(hamlet):
    w = copy.deepcopy(hamlet)
    assert not hasattr(KN, "options")                                            # gone from the code, not only hidden
    for name, p in sorted(w.s["people"].items()):
        if not p.get("alive", True) or p.get("stage") != "adult":
            continue
        for opening in (True, False):
            text = PR.turn_prompt(Here(w, name), Mind(w, name), opening)
            assert "Today you could" not in text and "Not yet:" not in text


# ---------------------------------------------------------------------- the fishing faults (u2 §6)
from cybertron2.engine import verbs as V, wild as WL                                     # noqa: E402
from tests.test_cybertron2_water5_river import adults, do, fresh, no_new_runs, pulse, river, water   # noqa: E402,F401


def test_the_edge_reaches_a_run_where_the_water_holds_no_resident_fish(river, monkeypatch):
    """Q-79 bug 1: hand fishing was refused at a run with no resident fish ("there is no fish at ...")."""
    no_new_runs(monkeypatch)
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    w.s["parcels"][pid]["res"].pop("fish", None)
    who = adults(w, node)[0]
    r = do(w, who, {"do": "gather", "what": "fish by hand", "at": w.s["parcels"][pid]["name"]})
    assert r.startswith("Refused") and "no fish" in r                            # no run: the water's own reason
    pulse(w, node, kind="eel", n=400.0)
    assert WL.run_here(w, node, pid)
    r = do(w, who, {"do": "gather", "what": "fish by hand", "at": w.s["parcels"][pid]["name"]})
    assert not r.startswith("Refused"), r


def test_the_fowling_net_meets_no_fish():
    """u2 §6 fault 3: the net's table held salmon at 3.0 by `social: flock`; it reaches what flies."""
    from cybertron2.engine.data import TECHNIQUES
    takes = TECHNIQUES["net"]["yield"]["takes"]
    assert "salmon" not in takes and "eel" not in takes and "lamprey" not in takes and "wildfowl" in takes


def test_snares_meet_no_otters_and_den_work_reaches_the_holt():
    """u2 §6 fault 14: snare covers included water, and the otter was taken in snares."""
    from cybertron2.engine.data import TECHNIQUES
    assert "otter" not in TECHNIQUES["snare"]["yield"]["takes"] and "water" not in TECHNIQUES["snare"]["at"]["covers"]
    assert "otter" in TECHNIQUES["den work"]["yield"]["takes"]


def test_a_runs_fish_learn_no_wariness(river, monkeypatch):
    """u1 §7a: a hunt-path method meeting a run's eels on several days; their learned wariness and pressure stay 0, and the take does
    not fall off; a resident kind's wariness still rises."""
    from cybertron2.engine.data import TECHNIQUES
    no_new_runs(monkeypatch)
    monkeypatch.setitem(TECHNIQUES["net"]["yield"], "takes", {"eel": 3.0, "wildfowl": 3.0})   # a guard: no method meets a run now
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    st = w.s["wild"]["state"]
    st["pop"]["eel"] = [0.0 for _ in st["pop"]["eel"]]                         # no resident eels: the run's only
    who = adults(w, node)
    for x in who:
        w.s["know"].setdefault(x, {})["net"] = {"level": "known", "skill": 1.0, "seen": 0, "wins": 0, "fails": 0, "source": "", "since": 0}
    wary0 = {k: list(v) for k, v in (st.get("wary") or {}).items()}
    press0 = {k: list(v) for k, v in (st.get("pressure") or {}).items()}
    got = 0
    for n in range(6):
        pulse(w, node, kind="eel", n=2000.0)
        r = do(w, who[n % len(who)], {"do": "gather", "what": "net", "at": w.s["parcels"][pid]["name"]})
        assert not r.startswith("Refused"), r
        assert not r.startswith(("You hunted", "Hunting")), r                     # the net's own words (u2 §6 fault 11)
        got += r.count("eel")
    assert got > 0
    zero = [0.0] * len(st["pop"]["eel"])
    assert ((st.get("wary") or {}).get("eel") or zero) == (wary0.get("eel") or zero)        # nothing learned from the run
    assert ((st.get("pressure") or {}).get("eel") or zero) == (press0.get("eel") or zero)
    assert (st.get("wary") or {}).get("wildfowl") != wary0.get("wildfowl")         # a resident kind learns as before


def _knows(w, who, tech):
    w.s["know"].setdefault(who, {})[tech] = {"level": "known", "skill": 1.0, "seen": 0, "wins": 0, "fails": 0, "source": "", "since": 0}


def _trap_at(w, who, pid, goods=None):
    cid = w.apply("new_thing", w.s["people"][who]["at"], node=w.s["people"][who]["at"], parcel=pid, kind="set", by=who,
                  set={"method": "trap in water", "life": 8, "base": 0.5, "set_day": w.d, "line": 1, "holds": 20})
    from cybertron2.engine import things as TH
    TH.remember(w, who, cid, "put")
    for it, q in (goods or {}).items():
        w.apply("create", w.s["people"][who]["at"], dst=cid, item=it, qty=q, why="test")
    return cid


def test_the_technique_named_alone_tends_what_stands(river):
    """u2 §6 fault 2: naming the traps again laid a new set beside the first; now it tends one's own standing there."""
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    who = adults(w, node)[0]
    _knows(w, who, "trap in water")
    pname = w.s["parcels"][pid]["name"]
    r = do(w, who, {"do": "gather", "what": "trap in water", "at": pname})
    assert r.startswith("You set"), r
    sets = [c for c in w.s["containers"].values() if c.get("kind") == "set" and c.get("by") == who]
    assert len(sets) == 1
    cid = next(k for k, c in w.s["containers"].items() if c is sets[0])
    w.apply("create", node, dst=cid, item="fish", qty=2.0, why="test")
    r = do(w, who, {"do": "gather", "what": "trap in water", "at": pname})
    assert r.startswith("You tended your wicker traps") and "2 fish" in r, r
    assert len([c for c in w.s["containers"].values() if c.get("kind") == "set" and c.get("by") == who]) == 1
    assert Here(w, who).carried().get("fish", 0) >= 2


def test_the_weir_is_not_everyones_craft():
    """u2 §6 bug 4: the weir was basic, known to everyone in every arm."""
    from cybertron2.engine.data import MONUMENTS, TECHNIQUES
    assert not MONUMENTS["weir"]["basic"] and not TECHNIQUES["weir"]["basic"]


def test_a_place_named_like_a_household_is_the_place(hamlet):
    """u2 §6 bug 5: "the Brook" was read as Brook House by the household's name."""
    w = copy.deepcopy(hamlet)
    name = sorted(n for n, p in w.s["people"].items() if p.get("stage") == "adult")[0]
    here = Here(w, name)
    pid, par = sorted(here.parcels().items())[0]
    word = par["name"].lower().removeprefix("the ")
    bid = sorted(here.buildings())[0]
    w.s["institutions"][word] = {"kind": "household", "name": f"the {word}s", "members": [], "offices": {}, "rules": {}}
    w.apply("claim", here.node, thing=("building", bid), claimant=word, rights="all", grounds="built")
    assert here.building(par["name"]) is None and here.parcel(par["name"]) == pid
    assert here.building(f"the {word}s") == bid and here.building(f"{word}'s") == bid


def test_unnamed_acts_touch_only_ones_own_and_anothers_set_is_named_theft(river):
    """u2 §6 faults 6 and 7: "take from the traps" emptied a neighbour's; a take from another's set had no theft words."""
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    a, b = [x for x in adults(w, node) if w.household_of(x)][:1] + \
        [x for x in adults(w, node) if w.household_of(x) != w.household_of(adults(w, node)[0])][:1]
    theirs = _trap_at(w, b, pid, {"fish": 3.0})
    from cybertron2.engine import things as TH
    TH.remember(w, a, theirs, "saw")
    r = do(w, a, {"do": "take", "item": "fish", "from": "the traps"})
    assert r.startswith("Refused"), r                                           # unnamed: one's own only
    r = do(w, a, {"do": "take", "item": "fish", "from": f"the traps {b} set"})
    assert "not yours to take from" in r, r                                     # named: that thing, and named theft
    assert any(t.get("thing") == theirs for t in w.s["today"]["thefts"])


def test_ones_own_sets_are_listed_with_their_tags(river):
    """u2 §6 fault 8: tags given to sets were not shown."""
    w = fresh(river)
    node = "Saltwell"
    who = adults(w, node)[0]
    cid = _trap_at(w, who, water(w, node))
    tag = w.s["containers"][cid].get("tag")
    assert tag
    from cybertron2.engine import things as TH
    r = (w.s["mind"][who].get("things") or {}).get(cid) or {"day": w.d}
    assert f"({tag})" in TH.set_line(w, who, w.s["containers"][cid], r, lambda d: f"day {d}")


def test_a_trap_set_turns_up_no_antler(river):
    """u2 §6 fault 15: water acts read the hunt's finds (antler, a cat); set gear in water reads the water's own rows."""
    w = fresh(river)
    node = "Saltwell"
    pid = water(w, node)
    who = adults(w, node)[0]
    for n in range(30):
        out = WL.work_notices(Here(w, who), Mind(w, who), "trap in water", pid)
        assert "antler" not in out and "cat" not in out


# ---------------------------------------------------------------------- signs as observations (D2-269; u8 §4)
def test_the_five_signs_that_directed_acts_are_observations():
    import inspect
    from cybertron2.engine import signs as SG
    from cybertron2.wild import kinds as WK
    text = inspect.getsource(WK) + inspect.getsource(SG)
    for order in ("set the traps tonight", "net them, or draw the hatches", "the traps and the weirs on the river will fill",
                  "watch it or bring it in", "it must be cut tomorrow or lost"):
        assert order not in text
    assert "an eel night" in text and "unable to get up past it" in text and "a day or two more and it will be lost" in text
