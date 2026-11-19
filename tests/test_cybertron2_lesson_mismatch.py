"""A lesson where teacher and learner named different crafts (Zach, 19 Nov; D4-123): the runs world's Lambert taught 'boil salt' three
days running while Saer asked for 'salt pan' (another craft), and nothing took. Now the lesson is in what the teacher teaches, and both
are told what was taught and what was asked for; a learn with no teacher names the craft it was for."""
from cybertron2.engine import run as R, settle as ST
from cybertron2.engine.world import World, load_spec


def _world():
    w = World(load_spec("cybertron2/specs/barleyfield_a.yaml"))
    a, b = [n for n in w.living() if w.s["people"][n]["stage"] == "adult"][:2]
    assert w.at(a) == w.at(b)
    w.s["know"].setdefault(a, {})["boil salt"] = {"level": "known", "skill": 1.2}
    w.s["know"].setdefault(b, {}).pop("boil salt", None)
    w.s["know"][b].pop("salt pan", None)
    w.s["today"] = R.blank_today()
    return w, a, b


def test_a_learner_who_named_another_craft_gets_the_teachers_lesson_and_both_are_told():
    w, a, b = _world()
    w.s["today"]["teach"].append({"by": a, "to": b, "tech": "boil salt"})
    w.s["today"]["learn"].append({"by": b, "from": a, "tech": "salt pan"})
    out = ST.settle_teaching(w, w.s["today"])
    assert w.s["know"][b]["boil salt"]["level"] == "capable"
    assert "salt pan" not in w.s["know"][b]
    assert any("wanted to learn" in x and "so they learnt boiling salt" in x for x in out[a])
    assert any(x.startswith("You wanted to learn") and "so you learnt boiling salt" in x for x in out[b])
    assert not any("did not set aside" in x for x in out[a] + out[b])


def test_a_matching_lesson_is_as_before_and_an_unanswered_learn_names_its_craft():
    w, a, b = _world()
    w.s["today"]["teach"].append({"by": a, "to": b, "tech": "boil salt"})
    w.s["today"]["learn"].append({"by": b, "from": a, "tech": "boil salt"})
    out = ST.settle_teaching(w, w.s["today"])
    assert w.s["know"][b]["boil salt"]["level"] == "capable"
    assert not any("wanted to learn" in x for x in out[a] + out[b])
    w.s["today"] = R.blank_today()
    w.s["today"]["learn"].append({"by": a, "from": b, "tech": "salt pan"})
    out = ST.settle_teaching(w, w.s["today"])
    assert out[a] == [f"You meant to learn making salt in the saltmarsh pans from {b}, but {b} did not set aside "
                      "time to teach you."]


def test_before_the_day_set_in_physics_the_crafts_must_match_as_they_did():
    w, a, b = _world()
    w.p["teach"]["any_craft_from_day"] = int(w.s["day"]) + 1
    w.s["today"]["teach"].append({"by": a, "to": b, "tech": "boil salt"})
    w.s["today"]["learn"].append({"by": b, "from": a, "tech": "salt pan"})
    out = ST.settle_teaching(w, w.s["today"])
    assert "boil salt" not in w.s["know"][b]
    assert out[b] == [f"You meant to learn from {a}, but {a} did not set aside time to teach you."]
