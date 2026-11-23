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
