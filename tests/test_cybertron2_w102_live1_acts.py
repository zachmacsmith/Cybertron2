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


# ---------------------------------------------------------------------- fault 1: rules, in the stated grammar (D2-337)
def test_a_rule_without_its_kind_in_rule_is_refused_naming_the_field():
    """The run's own rules (none carried "rule"): each refused saying which field, its form, and what was written."""
    w = at(NEW, "d0.work")
    a = the(0, "Hamon", {"do": "rule", "text": "Eat fresh fish and meat first, before roots, dried meat or anything that keeps."}, "evening")
    r = evening(w, "Hamon", a)
    assert r.startswith('Refused: rule: a rule names its kind in "rule": go | keep | hold back | first') and "you wrote" in r, r
    assert '"rule": "first", "goods": "fish"' in r                             # with the example
    w = at(NEW, "d4.talk.0")
    a = the(4, "Oliver", {"do": "change", "what": "rule", "line": "first: roots, then egg, then salt fish; keep dried meat for winter"})
    r, c = work(w, "Oliver", a)
    assert c == 0 and r.startswith('Refused: rule: a rule names its kind in "rule"'), r
    assert BK.household_rules(w, w.household_of("Oliver")) == []


def test_a_rule_in_its_fields_is_set_with_its_words_beside_the_reading():
    w = at(NEW, "d0.work")
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "goods": "fresh fish and fresh meat", "before": "roots, dried meat",
                             "words": "Eat fresh fish and meat first, before roots, dried meat or anything that keeps."})
    assert r.startswith("Rule 1 (the household): take or eat fish and meat first, before roots and dried meat (your words: "), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "go", "goods": "fish", "to": "the racks in the Shepherd Smokehouse",
                             "when": "the racks have room", "words": "fresh fish goes to the racks to be smoked"})
    assert r.startswith("Rule 2 (the household): fish that comes in goes to the racks in the Shepherd Smokehouse, when"), r
    assert BK.meal(w, "Gunnild")["first"] == ["fish", "meat"]                 # the household eats by it tonight
    w = at(NEW, "d2.work")
    r = evening(w, "Oliver", the(2, "Oliver", {"do": "first", "item": "fish"}, "evening"))   # the kind in "do", the good in "item"
    assert r.startswith("Rule 1 (the household): take or eat fish first"), r
    r = evening(w, "Oliver", {"do": "rule", "rule": "hold back", "goods": "salted fish", "unless": "someone is starving"})
    assert "hold back salt fish" in r, r                                       # a field's value to its canonical name


def test_a_rule_missing_a_field_or_with_an_unreadable_value_says_which():
    w = at(NEW, "d0.work")
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "words": "eat the fish first"})
    assert r.startswith("Refused: rule: 'first' needs \"goods\" (an item or a kind: fish"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "go", "goods": "fish"})
    assert r.startswith("Refused: rule: 'go' needs \"to\" (a building here, a store, a container"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "go", "goods": "fish", "to": "the moon"})
    assert r.startswith("Refused: rule: could not read \"to\": 'the moon' names no building"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "goods": "moonbeams"})
    assert r.startswith("Refused: rule: could not read \"goods\": 'moonbeams'"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "goods": "fish", "when": "the neighbours are kind"})
    assert r.startswith("Refused: rule: could not read \"when\": 'the neighbours are kind' is not a state"), r
    a = the(2, "Katherine", {"do": "rule", "thing": "fallback",
                             "to": "angle the Isel; firewood the Spinney only when the house store runs short"}, "evening")
    assert evening(at(NEW, "d2.work"), "Katherine", a).startswith('Refused: rule: a rule names its kind in "rule"')


def test_the_rules_block_shows_a_rules_fields():
    """The rules paragraph ends with one example of a rule's fields (its final grammar, D2-337 and D2-338, follows)."""
    from cybertron2.engine import core as CORE
    assert '{"do": "rule", "rule": "first", "goods": "fish", "words": "we eat the fresh fish first"}' in CORE.GRAMMAR


# ---------------------------------------------------------------------- fault 2: free acts at the evening
def test_free_acts_run_at_the_evening_whatever_their_shape_word():
    w = at(NEW, "d1.work")
    r = evening(w, "Hamon", the(1, "Hamon", {"do": "change", "thing": "door", "to": "shut"}, "evening answer"), left=0)
    assert r == "Shepherd House's door is now barred.", r
    r = evening(w, "Nigel", the(1, "Nigel", {"do": "put", "item": "firewood", "qty": 7.9, "to": "Marsh House"}, "evening"), left=0)
    assert r.startswith("You put 7.9 firewood into Marsh House"), r
    r = evening(w, "Hamon", {"do": "rule", "rule": "first", "goods": "fish"}, left=0)
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
    assert r.startswith("You carried 5 firewood from Marsh House to the Marsh Smokehouse"), r


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
