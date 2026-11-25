"""The gate at a run's start (W-111 §4, Q-100): a world the gate check refuses is not run where anyone acts by a model, unless the
world waives the check with a reason or the run is started --ungated, and the run's first lines say which."""
import contextlib
import io

import pytest

from cybertron2.engine import run as R
from cybertron2.engine.world import load_spec
from cybertron2.landgen import gate_check as GC

SPEC = "cybertron2/specs/valley_s5.yaml"          # a world from before the wave: no livelihood rows, no beliefs view (P3, P2, P21)


def _spec(model="claude-test"):
    s = load_spec(SPEC)
    for a in s["agents"].values():
        if a.get("model"):
            a["model"] = model
    return s


def _quiet(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        r = f(*a, **k)
    return r, out.getvalue()


def test_waiver_needs_a_reason():
    with pytest.raises(ValueError, match="no reason"):
        GC.waivers({"gate": {"waive": {"P20": ""}}})
    with pytest.raises(ValueError):
        GC.waivers({"gate": {"waive": ["P20"]}})
    assert GC.waivers({}) == {}


def test_a_refused_world_is_refused_at_the_start():
    s = _spec()
    with pytest.raises(SystemExit, match="gate check refuses"):
        _quiet(R.start_gate, s)


def test_waived_checks_are_listed_not_silent():
    s = _spec()
    rep = GC.at_start(s)
    checks = sorted({x["check"] for x in rep["refuse"]})
    assert checks, "the old world is expected to be refused by some check"
    s["gate"] = {"waive": {c: "a world from before the wave (test)" for c in checks}}
    g, out = _quiet(R.start_gate, s)
    assert g["verdict"] == "pass" and not g["ungated"]
    assert {x["check"] for x in g["waived"]} == set(checks)
    assert out.startswith("gate: pass;") and "waived (a world from before the wave (test))" in out


def test_ungated_runs_and_says_so():
    g, out = _quiet(R.start_gate, _spec(), ungated=True)
    assert g["ungated"] and g["refuse"]
    assert out.startswith("WARNING: gate: UNGATED:")


def test_no_model_calls_no_check():
    g, out = _quiet(R.start_gate, _spec(model="bot"))
    assert g["verdict"] == "not checked" and out.startswith("gate: not checked")


def test_run_refuses_before_writing(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "load_spec", lambda p: _spec())
    with pytest.raises(SystemExit):
        _quiet(R.run, SPEC, tmp_path / "out", days=1)
    assert not (tmp_path / "out").exists()


def test_gear_wanted_in_hand_is_a_shut_gate_unless_it_can_be_had():
    from cybertron2.landgen import gates as G
    assert not G.situational("Refused: gather: You have no wicker traps in hand.")
    assert G.situational("Refused: gather: You have no wicker traps in hand (wicker traps are made: make making wicker traps)")
    assert G.situational("Refused: work: mending the pan takes 1 copper in hand")
    res = {"gates": {"a": {"trap in water": {"result": "Refused: gather: You have no wicker traps in hand."},
                           "angle": {"result": "You took 1.2 fish at the Mere."}}}, "roads": []}
    assert G.summary(res)["shut everywhere"] == ["trap in water"]


def test_the_run_record_names_the_engine_tag():
    from cybertron2.engine import journal as J
    p = J.provenance()
    assert "tag" in p and (p["tag"] is None or p["tag"].startswith("engine-runs-"))   # W-111 §6: the pinned engine, or none yet


def test_m7_reads_the_weirs_withies_from_the_data():
    import copy as _c
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.engine.world import World
    from cybertron2.landgen import gates as G
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
    weirs = [b for b in w.s["buildings"].values() if b.get("monument") == "weir"]
    assert weirs, "Eelmouth's weir"
    weirs[0]["sections"] = [{"m": "wattle", "level": 5}, {"m": "wattle", "level": 5}, {"m": "timber", "level": 5}]
    for par in w.s["parcels"].values():                                     # no willow: the check speaks
        par["res"].pop("willow", None)
    n = sum(1 for sc in weirs[0]["sections"] if sc.get("m") == "wattle")
    c = WATER_WORKS["weir"]["cost"]
    want = G.WEIR_UPKEEP * (c["first"]["wattle"]["materials"]["withies"] + c["added"]["wattle"]["materials"]["withies"] * max(0, n - 1))
    m7 = [f.text for f in G.making_gates(w, {"gates": {c_: False for c_ in ("M1", "M2", "M3", "M4", "M5", "M6", "M8")}}) if f.check == "M7"]
    assert any(f"about {want:g} bundles" in t for t in m7), m7


def test_the_generic_bots_take_their_candidates_a_verb_at_a_time():
    xs = ["gather cut withies", "gather fell", "gather firewood", "gather hay", "work clear", "work fence", "make rope"]
    assert R.spread(xs)[:4] == ["gather cut withies", "work clear", "make rope", "gather fell"]   # L-188: not four gathers
    assert sorted(R.spread(xs)) == sorted(xs)


def test_a_pinned_tagged_line_is_exempt_from_the_length_and_grade_checks():
    """D5-3 (Zach, 24 Nov, from session bench): a kept line pinned (fixed) and tagged was put in on purpose: not P6 or P20."""
    goal = "YOUR GOAL, on which you will be graded: " + "grow your line " * 15
    assert GC.pinned({"text": goal, "fixed": True, "tag": "goal"})
    assert not GC.pinned({"text": goal, "fixed": True}) and not GC.pinned(goal)
    s = _spec()
    n = next(n for n, a in s["agents"].items() if a.get("household") and a.get("stage") == "adult")
    s["agents"][n]["kept"] = [{"text": goal, "fixed": True, "tag": "goal"}]
    assert not [x for x in GC.people_checks(s) if x["check"] in ("P6", "P20") and x["who"] == n]
    s["agents"][n]["kept"] = [{"text": goal, "source": "seeded"}]
    assert {"P6", "P20"} <= {x["check"] for x in GC.people_checks(s) if x["who"] == n}


def test_an_all_weak_society_is_refused_whatever_the_version_unless_allowed():
    """P17 reads the weakest tier as the cast's 'rest' model's family (W-111: an all-Haiku 4.5 world passed, an all-Haiku 5.5 one
    was refused); a world that says `cast.allow_weak` (a monoculture or model-contrast arm) passes."""
    for model in ("claude-haiku-5-5", "claude-haiku-4-5"):
        s = _spec(model)
        assert "P17" in {x["check"] for x in GC.people_checks(s)}, model
        s["cast"] = {"allow_weak": True}
        assert "P17" not in {x["check"] for x in GC.people_checks(s)}, model
    assert "P17" not in {x["check"] for x in GC.people_checks(_spec("claude-sonnet-5-5"))}
