"""W-102: the act interface's faults in live run 1's rebuilt arm (`prompt: core`, the eleven shapes), each tested with the run's own
replies, read from its turns file and played on the run's own checkpoint before that phase (the work's: talk.0; the evening's: work).
Also the river's carried catch after a weir is emptied, on the comparison arm's day 9. Skipped where the run's files are not here."""
import copy
import json
from pathlib import Path

import pytest

from cybertron2.engine import book as BK, evening as EVN, journal as JN, shapes as SH, verbs as V, waters as WA
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World

NEW = Path("/home/user/live1/void2_live1_A_new")
OLD = Path("/home/user/live1/live1_A_old")
pytestmark = pytest.mark.skipif(not (NEW / "run.db").exists(), reason="live run 1's record is not on this machine")

_W, _CP = {}, {}


def at(run, step):
    """The run's world at the end of a committed step (its checkpoint), one World built a run."""
    if run not in _W:
        spec = json.loads(dict(JN.read(run / "run.db", "SELECT key, value FROM meta"))["spec"])
        _W[run] = World(spec)
    if (run, step) not in _CP:
        _CP[(run, step)] = JN.checkpoint(run / "run.db", step)["world"]
    w = _W[run]
    w.s = copy.deepcopy(_CP[(run, step)])
    w._cause, w._depth = [], 0
    WA.link(w)
    return w


def acts(day, agent, wave=None):
    """The acts of a turn of the run: the day's plan, or a talk wave's ("evening", "evening answer")."""
    for line in open(NEW / "turns.jsonl"):
        d = json.loads(line)
        if d["day"] == day and d["agent"] == agent:
            if wave is None:
                return d["plan"]
            return next(t["reply"].get("actions") or [] for t in d["talk"] if t["wave"] == wave)
    raise KeyError((day, agent, wave))


def the(day, agent, want, wave=None):
    """The act of the run's turn equal to `want` (the test says what the agent wrote; the turns file proves they wrote it)."""
    xs = acts(day, agent, wave)
    assert want in xs, (want, xs)
    return want


def work(w, who, a):
    here, mind = Here(w, who), Mind(w, who)
    a2 = SH.quiet(here, a)
    return V.do(here, mind, a2), V.cost(here, a2)


def evening(w, who, a, left=4):
    out = []
    EVN.apply(w, who, {"actions": [a]}, {who: "x"}, [who], out, left, {})
    return out[-1]


# ---------------------------------------------------------------------- fault 1: rules, D2-339's grammar (fields, not words)
def rules(w, who, *xs):
    """Rules as the reply's own field sets them (D2-339), at the evening."""
    out = []
    EVN.apply(w, who, {"rules": list(xs)}, {who: "x"}, [who], out, 0, {})
    return out


def test_the_runs_rule_attempts_are_refused_naming_the_field():
    """The run's own rules (none carried its kind in "rule"): each refused saying which field, its form, and what was written."""
    w = at(NEW, "d0.work")
    a = the(0, "Hamon", {"do": "rule", "text": "Eat fresh fish and meat first, before roots, dried meat or anything that keeps."}, "evening")
    r = evening(w, "Hamon", a)
    assert r.startswith('Refused: rule: a rule names its kind in "rule": set | keep | first | share | do | drop') and "you wrote" in r, r
    w = at(NEW, "d4.talk.0")
    a = the(4, "Oliver", {"do": "change", "what": "rule", "line": "first: roots, then egg, then salt fish; keep dried meat for winter"})
    r, c = work(w, "Oliver", a)
    assert c == 0 and r.startswith('Refused: rule: a rule names its kind in "rule"'), r
    assert BK.household_rules(w, w.household_of("Oliver")) == []


def test_each_kind_set_in_the_rules_field_with_its_words_beside_the_reading():
    w = at(NEW, "d0.work")
    out = rules(w, "Hamon",
                {"rule": "set", "name": "the catch", "goods": ["fish", "meat"], "words": "what we catch"},
                {"rule": "first", "goods": ["the catch", "roots", "keeping food"], "words": "eat the catch first, then roots"},
                {"rule": "keep", "goods": "salted fish", "at least": 10, "unless": {"starving": "anyone"}},
                {"rule": "do", "act": {"do": "smoke fish", "at": "the Shepherd Smokehouse"}, "when": {"arrives": "fish"},
                 "unless": {"in": "the Shepherd Smokehouse", "full": True}, "words": "fresh fish goes to the racks"},
                {"rule": "share", "order": ["children", "Hamon"], "qty": "full"})
    assert out[0].startswith('Rule 1 (the household): the set "the catch": fish and meat (your words: "what we catch")'), out
    assert out[1].startswith("Rule 2 (the household): take or eat the catch, then roots, then keeping food first"), out
    assert out[2].startswith("Rule 3 (the household): at least 10 salt fish not eaten, drawn or used, unless someone is starving"), out
    assert out[3].startswith("Rule 4 (the household): whoever has time: make smoke fish at the Shepherd Smokehouse, when fish comes in, "
                             "unless the Shepherd Smokehouse is full"), out
    assert out[4].startswith("Rule 5 (the household): when food is short, children and Hamon are fed first"), out
    assert BK.meal(w, "Gunnild")["first"][:3] == ["fish", "meat", "roots"]    # the set expanded, in order
    r = rules(w, "Hamon", {"rule": "drop", "n": 5})
    assert r[0].startswith("Rule 5 (the household) dropped"), r


def test_the_meal_goes_by_the_shares_order_its_rations_and_its_goods():
    w = at(NEW, "d0.work")
    hh = w.household_of("Oliver")
    kids = [m for m in w.members(hh) if w.s["people"][m]["stage"] in ("infant", "child", "youth")]
    rules(w, "Oliver", {"rule": "share", "order": ["children"]},
          {"rule": "share", "who": "Oliver", "qty": "half"},
          {"rule": "share", "who": "children", "goods": "fish"})
    from cybertron2.engine import night as N
    order = BK.meal_order(w, w.living())
    assert kids and all(order.index(k) < order.index("Oliver") for k in kids)   # the children fed first
    assert BK.meal(w, "Oliver")["ration"] == 0.5 and "fish" in BK.meal(w, "Oliver")["skip"]   # fish kept for the children
    assert BK.meal(w, kids[0])["first"][0] == "fish"
    stk = w.s["buildings"][w.dwellings("Oliver")[0]]["stock"]
    w.s["containers"][stk]["goods"] = {"fish": 5.0, "roots": 5.0}
    N._eat(w, w.at("Oliver"), [stk], 0.5, True, who="Oliver", skip=BK.meal(w, "Oliver")["skip"])
    assert w.s["containers"][stk]["goods"]["fish"] == pytest.approx(5.0)       # he ate the roots, not the children's fish


def test_a_rule_missing_a_field_or_with_an_unreadable_value_says_which():
    w = at(NEW, "d0.work")
    r = rules(w, "Hamon", {"rule": "first", "words": "eat the fish first"},
              {"rule": "do", "when": {"arrives": "fish"}},
              {"rule": "keep", "goods": "fish", "in": "the moon"},
              {"rule": "first", "goods": ["moonbeams"]},
              {"rule": "do", "act": {"do": "tend", "at": "the Shepherd Smokehouse"}, "when": "the eels are fat"},
              {"rule": "do", "act": {"do": "tend", "at": "the Shepherd Smokehouse"}, "when": {"state": "smoking", "in": "the Shepherd Smokehouse"}},
              {"rule": "share", "qty": "lots"})
    assert r[0].startswith("Refused: rule: 'first' needs \"goods\" (an item, a kind"), r
    assert r[1].startswith("Refused: rule: 'do' needs \"act\""), r
    assert r[2].startswith("Refused: rule: could not read \"in\": 'the moon'"), r
    assert r[3].startswith("Refused: rule: could not read \"goods\": 'moonbeams'"), r
    assert r[4].startswith("Refused: rule: could not read") and "the eels are fat" in r[4] or "a rule names" in r[4], r
    assert r[5].startswith("Refused: rule: could not read \"when\"") and "done, in process or fire out" in r[5], r
    assert r[6].startswith("Refused: rule: could not read \"qty\": 'lots'"), r


def test_a_do_rule_runs_in_the_spare_units_own_first_and_while_its_condition_holds():
    w = at(NEW, "d0.talk.0")
    head = w.head(w.household_of("Hamon"))
    rules(w, head, {"rule": "do", "act": {"do": "tend", "at": "the Shepherd Smokehouse"},
                    "when": {"in": "the Shepherd Smokehouse", "state": "in process"}})
    rules(w, "Gunnild", {"rule": "do", "act": {"do": "firewood", "at": "the Spinney"}})   # her own: a fallback
    rec = BK.spare_units(w, ["Gunnild", "Hamon"], ["Gunnild", "Hamon"], {"Gunnild": 3, "Hamon": 3}, {"Gunnild": 0, "Hamon": 3},
                         {"Gunnild": [], "Hamon": []})
    mine = [x for x in rec["fired"] if x["person"] == "Gunnild"]
    assert mine and all(x["own"] for x in mine)                               # her own fallback took her units first (D2-301)


def test_old_records_on_the_book_are_converted_or_dropped():
    w = at(NEW, "d0.work")
    hh = w.household_of("Hamon")
    old = [{"n": 1, "rule": "hold back", "goods": "salt fish", "qty": 20, "unless": {"state": "starving", "text": "unless someone is starving"}},
           {"n": 2, "rule": "tend", "at": "the Shepherd Smokehouse", "when": {"state": "in process", "text": "while anything is smoking"}},
           {"n": 3, "rule": "go", "goods": "fish", "to": "the racks in the Shepherd Smokehouse", "when": {"state": "room", "text": "when they have room"}},
           {"n": 4, "rule": "eat", "qty": "half"},
           {"n": 5, "rule": "first", "goods": "fish", "before": "dried meat"},
           {"n": 6, "rule": "go", "goods": "fish", "to": "the moon"}]
    w.s.setdefault("books", {})[f"household:{hh}"] = {"rules": old, "n": 7, "proposals": []}
    got = {r["n"]: r for r in BK.household_rules(w, hh)}
    assert got[1]["rule"] == "keep" and got[1]["at least"] == 20.0 and got[1]["unless"] == {"starving": "anyone"}
    assert got[2] == {**got[2], "rule": "do", "act": {"do": "tend", "at": "the Shepherd Smokehouse"},
                      "when": {"in": "the Shepherd Smokehouse", "state": "in process"}}
    assert got[3]["rule"] == "do" and got[3]["act"]["what"] == "smoke fish" and got[3]["when"] == {"in": "the Shepherd Smokehouse", "room": True}
    assert got[4]["rule"] == "share" and got[4]["qty"] == 0.5
    assert got[5]["rule"] == "first" and got[5]["goods"] == ["fish", "dried meat"]
    assert 6 not in got                                                        # nowhere to read it as: dropped


def test_the_rules_block_gives_the_grammar_and_two_examples():
    from cybertron2.engine import core as CORE
    for x in ('"rules": [...]', "set {", "keep {", "first {", "share {", "do {", 'drop {"n"}', '"state": done | in process | fire out',
              '{"rule": "set", "name": "the young"', '{"rule": "do", "act": {"do": "tend"'):
        assert x in CORE.GRAMMAR, x
    assert 90 <= len(CORE.GRAMMAR.split()) <= 160


# ---------------------------------------------------------------------- fault 2: free acts at the evening
def test_free_acts_run_at_the_evening_whatever_their_shape_word():
    w = at(NEW, "d1.work")
    r = evening(w, "Hamon", the(1, "Hamon", {"do": "change", "thing": "door", "to": "shut"}, "evening answer"), left=0)
    assert r == "Shepherd House's door is now barred.", r
    r = evening(w, "Nigel", the(1, "Nigel", {"do": "put", "item": "firewood", "qty": 7.9, "to": "Marsh House"}, "evening"), left=0)
    assert r.startswith("You put 7.9 firewood into Marsh House"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "goods": ["fish"]}, left=0)
    assert r.startswith("Rule 1 (the household): take or eat fish first"), r
    w = at(NEW, "d1.work")
    r = evening(w, "Hamon", {"do": "set the door", "thing": "shut"}, left=0)      # Gunnild's words, by the one who manages it
    assert r == "Shepherd House's door is now barred.", r
    assert evening(w, "Hamon", {"do": "boil salt", "at": "the Salt House"}).startswith("Refused: make: the day's work is done")


# ---------------------------------------------------------------------- fault 3: go to a part of one's own place
def test_go_to_a_parcel_here_is_no_move_no_refusal_and_no_units():
    w = at(NEW, "d0.talk.0")
    r, c = work(w, "Gunnild", the(0, "Gunnild", {"do": "go", "to": "the Isel"}))
    assert c == 0 and not r.startswith("Refused") and '"at": "the Isel"' in r, r
    assert "Gunnild" not in w.s["today"]["travel"] and "Gunnild" not in w.s["today"].get("travel_morning", {})
    r, c = work(w, "Gunnild", {"do": "go", "to": "Shepherd House"})            # a building here too (day 3's)
    assert c == 0 and r.startswith("Shepherd House is here at Eelmouth"), r
    assert "travel to another place along a road" in SH.SHAPES["go"]["line"]


def test_go_to_ones_house_at_nightfall_is_where_one_sleeps():
    w = at(NEW, "d4.talk.0")
    r, _ = work(w, "Petronel", the(4, "Petronel", {"do": "go", "to": "Brook House", "when": "nightfall"}))
    assert r.startswith("You mean to sleep at Brook House"), r


# ---------------------------------------------------------------------- fault 4: arguments the handlers dropped
def test_sleep_reads_to_and_a_lesson_reads_with_what_and_line():
    w = at(NEW, "d3.work")
    r = evening(w, "Gunnild", the(3, "Gunnild", {"do": "sleep", "to": "Shepherd House"}, "evening"))
    assert r.startswith("You mean to sleep at Shepherd House"), r
    w = at(NEW, "d7.talk.0")
    r, _ = work(w, "Gunnild", the(7, "Gunnild", {"do": "agree", "with": "Hamon", "what": "learn", "line": "wicker trap"}))
    assert r.startswith("You set aside time to learn making wicker traps from Hamon"), r
    r, _ = work(w, "Hamon", the(7, "Hamon", {"do": "agree", "what": "teach wicker trap", "with": "Gunnild"}))
    assert r.startswith("You set aside time to teach Gunnild making wicker traps"), r
    assert {"by": "Gunnild", "from": "Hamon", "tech": "wicker trap"} in w.s["today"]["learn"]
    w = at(NEW, "d3.talk.0")
    r, _ = work(w, "Petronel", the(3, "Petronel", {"do": "learn", "with": "Oliver", "thing": "boiling salt from brine over a fire"}))
    assert r.startswith("You set aside time to learn boiling salt"), r
    w = at(NEW, "d2.talk.0")
    r, _ = work(w, "Gunnild", the(2, "Gunnild", {"do": "agree", "with": "Hamon", "describe": "lesson: teach me to cut withies at the fen, same day"}))
    assert r.startswith("You set aside time to learn cutting withies from Hamon"), r


def test_the_move_shape_reads_from_and_to_a_store_and_a_rack_by_its_words():
    w = at(NEW, "d0.talk.0")
    r, c = work(w, "Oliver", the(0, "Oliver", {"do": "move", "item": "salt", "qty": 4, "from": "the Salt House"}))
    assert r.startswith("You took 4 salt from the Salt House") and c == 1, r
    w = at(NEW, "d2.talk.0")
    r, _ = work(w, "Oliver", the(2, "Oliver", {"do": "move", "what": "put", "item": "salt", "qty": 16, "to": "the Salt House"}))
    assert r.startswith("You put 16 salt into the Salt House"), r              # was put into Brook House: "to" dropped
    w = at(NEW, "d1.talk.0")
    r, _ = work(w, "Peter", the(1, "Peter", {"do": "move", "item": "dried fish", "qty": 0.5, "from": "rack", "to": "Marsh House"}))
    assert r.startswith("You took down 0.5 kg of dried fish"), r
    w = at(NEW, "d8.talk.0")
    r, _ = work(w, "Peter", the(8, "Peter", {"do": "move", "item": "firewood", "qty": 5, "from": "Marsh House", "to": "the Marsh Smokehouse"}))
    assert r.startswith("You moved 5 firewood from Marsh House to the Marsh Smokehouse"), r


def test_other_arguments_read_where_the_reply_put_them():
    w = at(NEW, "d0.talk.0")
    r, _ = work(w, "Nichola", the(0, "Nichola", {"do": "gather", "do ": "angle"}))          # a key with a space after it
    assert r.startswith("You took") and "fish" in r, r
    r, _ = work(w, "Katherine", the(0, "Katherine", {"do": "set", "at": "the Isel", "qty": 6, "for": "my household"}))
    assert r.startswith("You set 6 wicker traps in the Isel"), r               # the one set gear in hand
    r, _ = work(w, "Hamon", the(0, "Hamon", {"do": "change", "thing": "heir", "heir": "Gunnild"}))
    assert r.startswith("You named Gunnild"), r
    w = at(NEW, "d3.work")
    r = evening(w, "Oliver", the(3, "Oliver", {"do": "accept", "what": "O142"}, "evening"))
    assert r.startswith("You accepted Hamon's offer O142"), r
    w = at(NEW, "d4.talk.0")
    r, _ = work(w, "Gunnild", the(4, "Gunnild", {"do": "wicker trap", "at": "Shepherd House", "qty": 4}))
    assert r.startswith("You made 4 wicker traps"), r                          # at a house: the making, not the setting


# ---------------------------------------------------------------------- fault 5: a verb word inside "do"
def test_a_shape_or_verb_word_first_in_do_is_read_as_the_shape():
    w = at(NEW, "d1.talk.0")
    r, _ = work(w, "Petronel", the(1, "Petronel", {"do": "learn boil salt", "with": "Oliver"}))
    assert r.startswith("You set aside time to learn boiling salt from brine over a fire from Oliver"), r
    r, _ = work(w, "Gunnild", the(1, "Gunnild", {"do": "cut firewood", "at": "the Spinney"}))
    assert r.startswith("You took") and "firewood" in r, r
    w = at(NEW, "d9.talk.0")
    r, _ = work(w, "Katherine", the(9, "Katherine", {"do": "set wicker trap", "at": "Eelmouth Fen", "qty": 6}))
    assert r.startswith("You set") and "wicker trap" in r, r
    with pytest.raises(Exception):
        SH.normalize(Here(w, "Katherine"), Mind(w, "Katherine"), {"do": "eel dancing"})


# ---------------------------------------------------------------------- the river: the carried catch after a weir is emptied
@pytest.mark.skipif(not (OLD / "run.db").exists(), reason="live run 1's comparison arm is not on this machine")
def test_day_9s_run_offers_the_run_rows_and_the_weirs_catch_is_seen_carried_home():
    from cybertron2.engine import signs as SG
    w = at(OLD, "d9.evening")
    rec = w.s["wild"]["river"]["Eelmouth"]
    assert rec["band"] == {"eel": "thick", "salmon": "glut"} and rec["day"] == 8       # last night's run, in its bands
    got = []
    SG._wild_river(Here(w, "Peter"), lambda about, text, p, tags, sense, **kw: got.append(text))
    assert any(t.startswith("dark eels moving in the slack water under the banks of the Isel") for t in got), got
    assert any(t.startswith("an eel run in the Isel") for t in got), got
    w = at(OLD, "d9.talk.0")                                                    # Peter empties the weir (his day 9), then is seen
    r = V.do(Here(w, "Peter"), Mind(w, "Peter"), {"do": "tend", "what": "weir", "at": "the Isel"})
    assert r.startswith("You emptied the weir's traps at the Isel"), r
    from cybertron2.wild import river as RV
    seen = []
    RV.carried(Here(w, "Peter"), lambda about, text, p, tags, sense, **kw: seen.append((text, kw.get("only"))))
    assert seen and seen[0][0] == "Peter came up from the Isel with as much fresh fish as they can carry", seen
    assert "Peter" not in seen[0][1]
