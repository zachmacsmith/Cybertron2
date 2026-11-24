"""Session bench's fixes from World 0b, taken to main by W-111: trying for a child reads "target" as the partner and, with no one
named, one's partner if here (0ac5d2e9, ffe0f9de); a household's rules read through its eldest living member while its head's office
is empty (25d77a28). The herd lookup (D2-304, D2-305) and livelihoods.fill's specialism have their tests in their own modules."""
import contextlib
import io

import pytest

from cybertron2.engine import book as BK, run as R, verbs as V
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import Refused, World, load_spec


@pytest.fixture()
def eel():
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
    w.s["today"] = R.blank_today()
    return w


def _try(w, who, a):
    return V._try(Here(w, who), Mind(w, who), {"do": "try", **a}, None)


def test_trying_for_a_child_reads_target_and_defaults_to_ones_partner(eel):
    assert "trying for a child with Nichola" in _try(eel, "Peter", {"target": "Nichola"})
    assert "trying for a child with Nichola" in _try(eel, "Peter", {})            # no one named: the partner, here
    eel.s["people"]["Oliver"]["partner"] = None
    with pytest.raises(Refused, match="say who with"):
        _try(eel, "Oliver", {})


def test_a_households_rules_read_through_its_eldest_while_no_head(eel):
    assert BK._voice(eel, "Marsh") == "Peter"
    eel.s["people"]["Peter"]["alive"] = False                                     # the head dead, none named yet
    assert eel.head("Marsh") is None
    alive = [m for m in eel.members("Marsh") if eel.s["people"][m].get("alive", True)]
    assert BK._voice(eel, "Marsh") == min(alive, key=lambda m: eel.s["people"][m].get("born", 0))
