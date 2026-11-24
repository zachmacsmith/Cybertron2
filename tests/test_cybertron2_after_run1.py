"""After live run 1 (W-104): the morning's meal line (D2-342), rules not attendable (D2-341), a chore or fallback that yields
nothing stopped for the day and shown, and the article in a mended line."""
import contextlib
import copy
import io

from cybertron2.engine import book as BK, night as N, perceive as PC, prompt as PR, run as R, view as VW
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

with contextlib.redirect_stdout(io.StringIO()):
    EEL = load_spec("cybertron2/specs/nutrition/eelmouth.yaml")


def eel():
    with contextlib.redirect_stdout(io.StringIO()):
        w = World(copy.deepcopy(EEL))
    w.s["today"] = R.blank_today()
    return w


def night(w):
    rec = N.night(w)
    w.s["day"] += 1
    w.s["today"] = R.blank_today()
    return rec


def stock(w, bid):
    return w.s["containers"][w.s["buildings"][bid]["stock"]]["goods"]


# ---------------------------------------------------------------------------------------------------------------------- D2-342
def test_the_morning_tells_what_was_eaten_from_where_by_which_rule_and_how_well():
    w = eel()
    BK.act(Here(w, "Peter"), {"rule": "first", "goods": ["roots"], "words": "we eat the roots first"})
    rec = night(w)
    got = Here(w, "Peter").meal_lines()
    assert len(got) == 2
    assert got[0].startswith("Last night you ate ") and "roots from Marsh House's store" in got[0]
    assert "by the household's rule 1 (“we eat the roots first”)" in got[0] and got[0].endswith("you ate your fill.")
    drawn = rec["drawn"]["stock:marsh_house"]["roots"]                        # the store's draw, not the night's spoilage
    eaten = sum(q for n, m in rec["meal"].items() if w.household_of(n) == "Marsh" for cid, i, q in m["ate"] if cid == "stock:marsh_house")
    assert abs(drawn - eaten) < 1e-6
    assert got[1] == f"For the whole household's meal, Marsh House's store gave {N.show_fine(drawn)} roots in all."
    oliver = Here(w, "Oliver").meal_lines()                                   # no rule: the usual order
    assert "in the usual order" in oliver[0] and "Brook House's store" in oliver[0]


def test_a_short_meal_says_there_was_not_enough_for_everyone():
    w = eel()
    g = stock(w, "marsh_house")
    for i in list(g):
        if i in ("dried meat", "roots"):
            g[i] = 0.6 if i == "roots" else 0.0
    night(w)
    lines = {n: Here(w, n).meal_lines() for n in ("Peter", "Nichola", "Nigel")}
    hungry = [x[0] for x in lines.values() if "still hungry" in x[0]]
    assert hungry and any("there was not enough for everyone" in x or "nothing more you could eat" in x for x in hungry), lines


def test_the_meal_line_is_in_the_beliefs_morning_and_the_old_morning():
    w = eel()
    night(w)
    PC.dawn(w)
    msg = VW.turn(Here(w, "Peter"), Mind(w, "Peter"), opening=False)
    assert "Last night you ate " in msg.split("## You", 1)[1]
    old = PR.turn_prompt(Here(w, "Peter"), Mind(w, "Peter"), opening=False)
    assert "Last night you ate " in old.split("## You", 1)[1]
    assert Here(w, "Peter").meal_lines()[0] in old


# ---------------------------------------------------------------------------------------------------------------------- D2-341
def test_a_rule_or_the_book_cannot_be_attended_and_falls_back_as_any_unreadable_target():
    w = eel()
    BK.act(Here(w, "Peter"), {"rule": "first", "goods": ["roots"]})
    here = Here(w, "Peter")
    for x in ("rule 1", "the household's rules", "Marsh House's rules", "the book", "my fallback", {"rule": "first", "n": 1}):
        sub, label = PC.resolve_target(here, x)
        assert sub == "nothing", (x, sub, label)                                 # nothing found, nothing shown (D2-346)
    assert PC.resolve_target(here, "Marsh House")[0].startswith("building:")    # a building is still a building


# ---------------------------------------------------------------------------------------------------------------------- W-104 item 5
def _spare(w, who, free):
    names = [n for n in w.living() if w.at(n) is not None]
    budget = {n: w.units_for(n) for n in names}
    used = {n: (budget[n] - free if n == who else budget[n]) for n in names}
    results = {n: [] for n in names}
    rec = BK.spare_units(w, names, sorted(names), budget, used, results)
    return rec, results, used, budget


def test_a_fallback_that_gives_nothing_stops_after_one_try_and_the_morning_says_so(monkeypatch):
    from cybertron2.engine import verbs as V
    w = eel()
    BK.set_fallback(w, "Gunnild", [{"do": "twist cord", "at": "Eelmouth Fen"}])
    real = V.do

    def nothing(here, mind, a):                                               # the act runs and gives nothing
        if a.get("do") == "twist cord":
            return "You took 0 cord at Eelmouth Fen."
        return real(here, mind, a)
    monkeypatch.setattr(V, "do", nothing)
    rec, results, used, budget = _spare(w, "Gunnild", 4)
    tries = [x for x in results["Gunnild"] if x.startswith("You took 0 cord")]
    assert len(tries) == 1 and tries[0].endswith("It gave nothing, so it was not tried again today."), results["Gunnild"]
    assert rec["empty"] and rec["empty"][0]["person"] == "Gunnild" and rec["empty"][0]["fallback"]
    lines = BK.day_lines(w, rec, "Gunnild")
    assert "Your fallback, twist cord at Eelmouth Fen, gave nothing yesterday; it stopped after one try." in lines
    assert BK.day_lines(w, rec, "Gunnild", when="today")[0].endswith("gave nothing today; it stopped after one try.")
    w.s["log"].append({"day": w.d, "book": rec})                              # the morning after, in the beliefs view
    w.s["day"] += 1
    assert Here(w, "Gunnild").book_empty_lines() == [lines[0]]


def test_a_chore_that_gives_even_a_little_goes_on_as_before():
    w = eel()
    BK.set_fallback(w, "Gunnild", [{"do": "twist cord", "at": "Eelmouth Fen"}])
    rec, results, used, budget = _spare(w, "Gunnild", 3)
    tries = [x for x in results["Gunnild"] if "cord" in x]
    assert len(tries) == 3 and not rec.get("empty"), results["Gunnild"]
    assert all("0.04 cord" in x or "0.03 cord" in x for x in tries), tries          # shown as taken, not "0" (show_fine)


def test_a_household_chore_that_gives_nothing_is_told_to_its_doer_and_the_head(monkeypatch):
    from cybertron2.engine import verbs as V
    w = eel()
    BK.act(Here(w, "Peter"), {"rule": "do", "who": "Nigel", "act": {"do": "twist cord", "at": "Eelmouth Fen"}})
    real = V.do
    monkeypatch.setattr(V, "do", lambda here, mind, a: "You took 0 cord at Eelmouth Fen." if "twist cord" in (a.get("do"), a.get("what"))
                        else real(here, mind, a))
    rec, results, *_ = _spare(w, "Nigel", 3)
    assert len([x for x in results["Nigel"] if "0 cord" in x]) == 1
    assert BK.day_lines(w, rec, "Nigel") == ["The household's rule 1, gather twist cord at Eelmouth Fen, gave nothing yesterday; it stopped after one try."]
    assert "The household's rule 1, gather twist cord at Eelmouth Fen, gave Nigel nothing yesterday; it stopped after one try." in BK.day_lines(w, rec, "Peter")


# ---------------------------------------------------------------------------------------------------------------------- W-104 item 7
def test_mending_one_piece_says_your_hand_line_not_your_a_hand_line():
    from cybertron2.engine import gear as GE, verbs as V
    w = eel()
    h = w.s["containers"][w.hands("Peter")]
    p = GE.pieces(h, "hand line", w)
    h["pieces"] = {**(h.get("pieces") or {}), "hand line": [dict(x, life=1.0) for x in p]}
    h["goods"]["copper hook"] = 2.0
    r = V.do(Here(w, "Peter"), Mind(w, "Peter"), {"do": "make", "what": "mend"})
    assert r.startswith("You mended your hand line with ") and "your a " not in r and ": it is good for about" in r, r
