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


def test_food_in_meals_is_said_as_it_is():
    """L-179 (W-111): a small take is a mouthful or a part of a meal, never 'about 1 meal' at the least."""
    from cybertron2.engine.placed import meals
    assert meals(0.02) == "hardly a mouthful" and meals(0.2) == "about a quarter of a meal"
    assert meals(0.5) == "about half a meal" and meals(1.2) == "about 1 meal" and meals(3.6) == "about 4 meals"


def test_household_names_and_crumbs_read_right():
    """L-178 (W-111): the Marshes, not the Marshs; 'which the Brooks hold'; crumbs in hand said as crumbs."""
    from cybertron2.engine import night as N
    from cybertron2.engine.world import plural
    assert plural("Marsh") == "Marshes" and plural("Brook") == "Brooks" and plural("Fox") == "Foxes"
    assert N._goods_words([("roots", 1.2), ("greens", 0.05), ("berries", 0.04)]) == "1.2 roots and crumbs of greens and berries"


def test_the_rules_block_names_the_household_by_its_surname(eel):
    assert any(x.startswith("The Marsh household") for x in BK.rules_block(eel, "Peter"))


def test_the_smokehouse_fire_is_told_and_what_hangs_is_named():
    """wave_regressions findings 6 and 7 (W-111): the old prompt's manual tells the smokehouse's fire, from PHYSICS; the racks'
    description says it can catch; a done smokehouse names what hangs, not 'the fish'."""
    import inspect
    from cybertron2.engine import process as PROC
    from cybertron2.engine.data import FITTINGS, PHYSICS, TECHNIQUES
    p = PHYSICS["smokehouse"]["fire"]["wattle"]
    assert f"wattle about 1 night in {round(1 / p):,}" in TECHNIQUES["smoke meat"]["manual"]
    assert "can catch" in FITTINGS["smoke racks"]["does"]
    assert "the fish on the racks" not in inspect.getsource(PROC)
