"""Session bench's fixes from World 0b, taken to main by W-111: trying for a child reads "target" as the partner and, with no one
named, one's partner if here (0ac5d2e9, ffe0f9de); a household's rules read through its eldest living member while its head's office
is empty (25d77a28). The herd lookup (D2-304, D2-305) and livelihoods.fill's specialism have their tests in their own modules."""
import contextlib
import io

import pytest

from cybertron2.engine import book as BK, run as R, verbs as V
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.data import EDIBLE
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


def test_no_act_and_craft_share_a_name_and_the_hunting_drive_is_its_own():
    """Q-109 (W-111): the hunting method was 'drive', the herd act's name; where a craft is named alone in "do" the act won (Eelmouth
    refused a hunting drive; the Scattering drove a household's cattle into a wood). It is 'hunting drive', and the registries are
    checked for a shared name when they load."""
    from cybertron2.engine import shapes as SH
    from cybertron2.engine.data import TECHNIQUES
    assert not set(V.VERB) & set(TECHNIQUES)
    assert TECHNIQUES["hunting drive"]["label"] == "a hunting drive"
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(load_spec("cybertron2/specs/nutrition/eelmouth.yaml"))
    w.s["today"] = R.blank_today()
    w.s["know"]["Peter"]["hunting drive"] = {"level": "known", "skill": 1.0}
    n = SH.normalize(Here(w, "Peter"), Mind(w, "Peter"), {"do": "hunting drive", "at": "the Spinney", "looking for": "deer"})
    assert (n["do"], n["what"]) == ("gather", "hunting drive"), n


def test_a_world_made_before_the_rename_reads_drive_as_the_hunting_drive():
    from cybertron2.engine.world import renamed
    spec = {"agents": {"Gilbert": {"knows": {"drive": {"level": "known", "skill": 1.0}}, "aware_of": {"drive": "seen"}}}}
    renamed(spec)
    assert "hunting drive" in spec["agents"]["Gilbert"]["knows"] and "drive" not in spec["agents"]["Gilbert"]["knows"]
    assert "hunting drive" in spec["agents"]["Gilbert"]["aware_of"]



def _short_marsh(w, food=1.0):
    """The Marshes with `food` of salt fish in all, in their house's store, and nothing in hand."""
    for m in w.members("Marsh"):
        w.s["containers"][w.hands(m)]["goods"] = {k: v for k, v in w.goods(w.hands(m)).items() if k not in EDIBLE}
    for bid in Here(w, "Peter").homes_here():
        st = w.s["buildings"][bid]["stock"]
        w.s["containers"][st]["goods"] = {k: v for k, v in w.goods(st).items() if k not in EDIBLE}
    home = Here(w, "Peter").homes_here()[0]
    w.s["containers"][w.s["buildings"][home]["stock"]]["goods"]["salt fish"] = food


def test_a_short_household_with_no_share_rule_splits_the_meal_evenly(eel):
    """W-111 (bench's World 0b reruns): fed in name order, the last of a short household got nothing night after night. With no
    share rule, each member eats the same share."""
    from cybertron2.engine import night as N
    _short_marsh(eel, food=2.0)
    shares = N.even_shares(eel, {m: Here(eel, m).homes_here()[0] for m in eel.members("Marsh") if Here(eel, m).homes_here()})
    assert 0 < shares["Marsh"] < 1
    rec = N.night(eel)
    ms = [m for m in eel.members("Marsh") if eel.s["people"][m].get("alive", True)]
    ate = {m: (rec["meal"].get(m) or {}).get("ate_total", rec["ate"].get(m, 0.0)) or 0.0 for m in ms}
    assert all(m not in rec["missed"] or ate[m] > 0 for m in ms), ate          # nobody left with nothing while others eat
    assert max(ate.values()) - min(ate.values()) < 0.6, ate


def test_a_share_rule_keeps_its_own_order(eel):
    from cybertron2.engine import night as N
    BK.act(Here(eel, "Peter"), {"rule": "share", "order": ["Peter"]})
    _short_marsh(eel, food=2.0)
    assert "Marsh" not in N.even_shares(eel, {})


def test_the_registries_refuse_a_shared_name_and_a_way_of_no_craft(monkeypatch):
    """D2-353 (W-111): checked when they load. The drive's rename left eight hunting ways naming 'gather:drive', silently unapplied."""
    from cybertron2.engine import data as D
    V._check_names()
    monkeypatch.setitem(D.TECHNIQUES, "a test way", {"verb": "modifier", "modifies": ["gather:no such craft"]})
    with pytest.raises(RuntimeError, match="ways that name no craft"):
        V._check_names()
    monkeypatch.delitem(D.TECHNIQUES, "a test way")
    monkeypatch.setitem(D.TECHNIQUES, "travel", {"verb": "gather"})
    with pytest.raises(RuntimeError, match="share a name"):
        V._check_names()


def test_the_arrival_view_counts_the_others_not_oneself(eel):
    """W-111 (bench's 200-day runs): a lone traveller at an empty place read "one person about the place" while "Here today: nobody
    else" stood beside it; the count is of the others there."""
    from cybertron2.engine import layout as LY
    node = eel.s["people"]["Peter"]["at"]
    for n in list(eel.present(node)):
        if n != "Peter":
            eel.s["people"][n]["at"] = None
    assert not any("about the place" in x for x in LY.overview(eel, node, viewer="Peter"))
    assert not any("about the place" in x for x in Here(eel, "Peter").overview())


def test_a_hungry_meal_names_the_rule_that_kept_the_food_back(eel):
    """W-111 (bench's Scattering arm): the Meades starved behind "keep at least 50 grain" with 48 in the bins, told each morning
    "nothing more"; the meal line names the household's rule and what it kept back, at or under its floor too."""
    from cybertron2.engine import night as N
    _short_marsh(eel, food=0.0)
    home = Here(eel, "Peter").homes_here()[0]
    eel.s["containers"][eel.s["buildings"][home]["stock"]]["goods"]["grain"] = 40.0
    BK.act(Here(eel, "Peter"), {"rule": "keep", "goods": "grain", "at least": 50, "words": "keep the seed grain"})
    N.night(eel)
    eel.s["day"] += 1
    eel.s["today"] = R.blank_today()
    line = Here(eel, "Peter").meal_lines()[0]
    assert "still hungry" in line and "kept back 40 grain" in line and "keep the seed grain" in line, line


def test_a_second_weir_where_one_stands_says_how_to_add_to_it(eel):
    """W-111 (bench's Fallowmere runs): "build weir" where one stands was refused without saying a weir grows by sections."""
    b = next(b for b in eel.s["buildings"].values() if b.get("monument") == "weir")
    place = eel.s["parcels"][b["parcel"]]["name"]
    who = sorted(n for n, k in eel.s["know"].items() if "weir" in k)[0]
    out = V.do(Here(eel, who), Mind(eel, who), {"do": "build", "what": "weir", "at": place, "with": ["Nigel"]})
    assert "already" in out and "a wattle section" in out and "a timber section" in out, out


def test_a_too_heavy_reply_that_says_go_sets_off(eel):
    """W-111 (bench's monoculture runs, 0 departures from 108 lighten calls): the interface's travel word is "go"; the lighten
    reply's acts are read as the interface writes them, so {"do": "go", "to": ...} is the setting off, and a give stays a give."""
    road = Here(eel, "Peter").roads()[0][1]
    acts = R.lighten_acts(eel, "Peter", [{"do": "give", "to": "Nichola", "item": "timber", "qty": 5},
                                         {"do": "go", "to": road}, {"do": "rest"}, "not an act"])
    assert [v for _, v in acts] == ["give", "travel"], acts


def test_the_carry_limits_and_what_a_pack_does_are_shown(eel):
    """W-111 (bench's monoculture runs, D5-2): no arm made a pack basket in 60 days, its line saying only what it took, and the carry
    limit reached no model. The go act's line and the carrying gear's lines say them, from the data."""
    from cybertron2.engine import prompt as PR
    from cybertron2.engine.data import ITEMS, PHYSICS
    s = PR.system_prompt(Here(eel, "Peter"), Mind(eel, "Peter"))
    assert f"On foot you carry at most {PHYSICS['carry']['foot']:g} kg" in s
    assert f"make a pack basket: you carry {ITEMS['pack']['carry']:g} kg more on the road" in s
