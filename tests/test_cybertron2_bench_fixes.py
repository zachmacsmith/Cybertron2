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


def test_an_act_word_that_is_a_craft_one_knows_is_read_as_the_craft(eel):
    """W-111 (Eelmouth's live check): {"do": "drive", "at": ..., "looking for": "deer"} is the hunting drive Peter knows and is shown,
    not the herd act, which this world has not; a herd driven ("thing": a herd) stays the herd act."""
    from cybertron2.engine import shapes as SH
    here, mind = Here(eel, "Peter"), Mind(eel, "Peter")
    n = SH.normalize(here, mind, {"do": "drive", "at": "Clay Field", "only": ["Nigel"], "looking for": "deer"})
    assert n["do"] == "gather" and n["what"] == "drive", n
    assert SH.normalize(here, mind, {"do": "drive", "thing": "the cattle", "to": "Clay Field"})["do"] == "drive"


def test_an_empty_pin_written_as_quotes_is_no_pin(eel):
    """W-111 (Eelmouth's live check): "pin": '""' was refused as a note called “""”; it means no pin."""
    from cybertron2.engine import perceive as PC
    out = PC.apply_notes(Mind(eel, "Peter"), {"pin": '""'})
    assert not any("pin:" in x for x in out)


def test_a_say_among_a_talk_waves_actions_is_moved_to_say(tmp_path, monkeypatch):
    """W-111 (World 0b's live check): a reply in the day's talk waves with "say" among its actions was refused at work as a craft
    ("you know no craft called 'say'"); it is moved to "say" as the morning's reply is (L-189)."""
    import json as _j
    import yaml
    from cybertron2.infra import llm

    def fake_call(backend, model, system, user, schema, **kw):
        text = str(getattr(user, "fallback", user))
        if "## Before the day's work" in text:                                 # a talk wave
            return {"why": "x", "actions": [{"do": "say", "to": "everyone", "text": "the cattle are sick"}]}, None, {"cc_equiv_usd": 0.0}
        return {"why": "x", "actions": [], "tell": [{"to": "Nichola", "text": "Nichola, the cattle"}]}, None, {"cc_equiv_usd": 0.0}
    monkeypatch.setattr(llm, "call", fake_call)
    spec = load_spec("cybertron2/specs/nutrition/eelmouth.yaml")
    spec["days"] = 1
    for n, a in spec["agents"].items():
        if a.get("model"):
            a["model"] = "bot"
    spec["agents"]["Peter"]["model"] = spec["agents"]["Nichola"]["model"] = "claude-haiku-5-5"
    p = tmp_path / "s.yaml"
    p.write_text(yaml.safe_dump(spec))
    with contextlib.redirect_stdout(io.StringIO()):
        R.run(str(p), str(tmp_path / "out"), backend="api", workers=2)
    rows = [_j.loads(x) for x in open(tmp_path / "out" / "turns.jsonl")]
    res = [x for r in rows if r["agent"] == "Nichola" for x in r["results"]]
    assert not any("craft called 'say'" in x for x in res), res


def test_a_rules_who_in_ones_own_words(eel):
    """W-111 (World 0b's live check): "who": "my household" is the household's members, as "for" already read it."""
    ms = sorted(m for m in eel.members("Marsh") if eel.s["people"][m].get("alive", True))
    assert sorted(BK.people_of(eel, "Peter", "my household")) == ms
    assert BK.people_of(eel, "Peter", "only me") == ["Peter"]


def test_caring_with_food_not_in_hand_says_where_it_is(eel):
    """W-111 (World 0b's live check, 16 refusals): care feeds a child from one's hands; the refusal says where the food is."""
    here = Here(eel, "Peter")
    kids = [n for n in here.people(me=False) if here.body(n)["stage"] in ("infant", "child")]
    if not kids:
        pytest.skip("no child at Eelmouth on day 0")
    home = next(b for b in here.homes_here())
    eel.s["containers"][eel.s["buildings"][home]["stock"]]["goods"]["smoked fish"] = 5.0
    eel.s["containers"][eel.hands("Peter")]["goods"].pop("smoked fish", None)
    with pytest.raises(Refused) as e:
        V._care(here, Mind(eel, "Peter"), {"do": "care", "at": kids[0], "item": "smoked fish"})
    assert "fed from your hands" in str(e.value) and "holds 5" in str(e.value) and "move smoked fish to your hands" in str(e.value)
