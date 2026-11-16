"""Brief 4c §4 (proposals/hunt_calibration.md): set things, a catch found by going to it. One who set a line, or has seen it, and is
on its parcel looks it over (a close look at THINGS set `knows`); a catch raises the line's own conspicuousness, and the birds at it
after a day more, so a stranger finds a line with a catch more often than an empty one; the remembered line never says "empty"
unless seen so, and says when it was seen; lifting or checking the snares is taking what is in them; the catch's chance is
1 - exp(-x) (§3.1)."""
import math

from cybertron2.engine import night as N, perceive as PC, run as R, signs as SG, things as TH, wild as WL
from cybertron2.engine.data import THINGS
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

from tests.test_cybertron2_wild import _do, _ring, _summer_world, _two, generated  # noqa: F401

SPEC = "cybertron2/specs/wenbridge.yaml"
MEAD = "wb_mead"                                       # Mill Mead: the line's parcel
SETTER, STRANGER = "Ellen", "Wat"                      # both an ordinary eye; Hearne and Mason households


def _w():
    w = World(load_spec(SPEC))
    w.s["today"] = R.blank_today()
    return w


def _line(w, by=SETTER, parcel=MEAD, method="snare", set_day=None):
    """A snare line set as wild.set_work sets it, known to its setter."""
    set_day = w.d - 3 if set_day is None else set_day
    cid = w.apply("new_thing", "wenbridge", node="wenbridge", parcel=parcel, kind="set", by=by,
                  set={"method": method, "life": 8, "base": 0.5, "set_day": set_day, "line": 5, "holds": 5})
    TH.remember(w, by, cid, "put")
    return cid


def _catch(w, cid, kind="brown hare", day=None, goods=None):
    """A beast caught as wild._set_night catches it: its goods in the line and the catch recorded with its night."""
    day = w.d - 1 if day is None else day
    for item, q in (goods or {"meat": 0.7}).items():
        w.apply("create", "wenbridge", dst=cid, item=item, qty=q, why="caught in a set")
    c = w.s["containers"][cid]
    w.apply("set_thing", "wenbridge", cid=cid, field="catch", value=list(c.get("catch") or []) + [{"kind": kind, "day": day}])


def _facts(w, cid, who=None):
    F = [f for f in PC.facts(Here(w, SETTER)) if f.get("thing") == cid]
    if who is None:
        return F
    knows = TH.known_here(w, who, "wenbridge")
    return [f for f in F if PC.for_me(w, who, f, knows)]


def _day(w, d, worked):
    w.s["day"] = d
    w.s["today"] = t = R.blank_today()
    for name, pid in worked.items():
        t["worked"][name] = [pid]
    return t


def _evening(w, today):
    PC.evening(w, {}, today)
    return {n: w.s["mind"][n]["today"]["notice"] for n in w.living()}


# ---------------------------------------------------------------------- the setter's look (§4.1)
def test_the_setter_working_its_parcel_sees_the_catch_the_morning_after_at_the_calibrated_chance():
    w = _w()
    cid = _line(w)
    _catch(w, cid)
    look = next(f for f in _facts(w, cid, SETTER) if f.get("who") == "setter")
    assert look["text"] == "a brown hare hangs in your snares at Mill Mead" and look["reach"] == "near"
    _day(w, w.d, {SETTER: MEAD})
    p = PC.chance_of(w, SETTER, look)
    assert abs(p - THINGS["set"]["knows"] * 0.5 * 2.0 * TH.EV.visibility(w, "wenbridge", MEAD, "sight")) < 1e-6
    seen = 0
    for d in range(20):                                                         # the morning after the catch, many days
        w2 = _w()
        cid2 = _line(w2, set_day=d - 3)
        t = _day(w2, d, {SETTER: MEAD})
        _catch(w2, cid2, day=d - 1)
        seen += "a brown hare hangs in your snares at Mill Mead" in _evening(w2, t)[SETTER]
    assert seen >= 14                                                           # about 0.9 in clear weather, less in fog


def test_one_not_at_the_parcel_sees_nothing_new():
    w = _w()
    cid = _line(w)
    _catch(w, cid)
    look = next(f for f in _facts(w, cid, SETTER) if f.get("who") == "setter")
    for d in range(12):
        t = _day(w, d, {SETTER: "wb_quarry"})                                   # at work on the Quarry, four steps off
        assert PC.chance_of(w, SETTER, look) == 0.0
        notice = _evening(w, t)[SETTER]
        assert not any("hare" in x or "snare" in x for x in notice)
    r = TH.known(Mind(w, SETTER))[cid]
    assert "set_seen" not in r                                                  # never told of a catch one is not at


def test_an_empty_line_shows_as_nothing_caught_only_after_a_night_and_once():
    w = _w()
    cid = _line(w, set_day=0)
    assert not [f for f in _facts(w, cid, SETTER) if f.get("who") == "setter"]  # set today: the result line said so
    w.s["day"] = 1
    look = [f for f in _facts(w, cid, SETTER) if f.get("who") == "setter"]
    assert [f["text"] for f in look] == ["nothing caught in your snares at Mill Mead"]
    shown = []
    for d in range(1, 9):
        shown.append(sum("nothing caught in your snares" in x for x in _evening(w, _day(w, d, {SETTER: MEAD}))[SETTER]))
    assert sum(shown) == 1                                                       # a change, not a standing fact
    r = TH.known(Mind(w, SETTER))[cid]
    assert r["set_seen"]["words"] == "nothing caught in them" and r["set_seen"]["day"] > shown.index(1) + 1   # its day kept up


# ---------------------------------------------------------------------- a catch shows itself (§4.2)
def test_a_stranger_finds_a_line_with_a_catch_more_often_than_an_empty_one_and_the_birds_raise_that():
    w = _w()
    _day(w, 5, {STRANGER: MEAD})
    empty, fresh, birds = _line(w, set_day=1), _line(w, set_day=1), _line(w, set_day=1)
    _catch(w, fresh, day=4)
    _catch(w, birds, day=5 - THINGS["set"]["birds_after"])
    own = [TH.own(w, w.s["containers"][c]) for c in (empty, fresh, birds)]
    assert own[0] < own[1] < own[2] and abs(own[1] - THINGS["set"]["caught"]) < 0.05
    ch = [TH.chance(w, STRANGER, w.s["containers"][c]) for c in (empty, fresh, birds)]
    assert ch[0] < ch[1] < ch[2]
    rows = {c: [f for f in _facts(w, c, STRANGER)] for c in (empty, fresh, birds)}
    assert all(f.get("who") in (None, "stranger") for fs in rows.values() for f in fs)
    assert any(f["text"].startswith("a brown hare caught in a snare at Mill Mead") for f in rows[fresh])
    assert any(f["text"].startswith("crows and magpies going down at Mill Mead") for f in rows[birds])
    assert not any("crows" in f["text"] for f in rows[fresh])
    found = {c: 0 for c in rows}
    for d in range(40):                                                         # over days, the stranger at work on the mead
        t = _day(w, 5, {STRANGER: MEAD})
        w.s["mind"][STRANGER]["things"] = {}
        rng = Here(w, STRANGER).rng("probe", d)
        for c, fs in rows.items():
            if any(rng.random() < PC.chance_of(w, STRANGER, f) for f in fs if f.get("reach") != "count"):
                found[c] += 1
    assert found[empty] < found[fresh] < found[birds]


def test_a_stranger_who_takes_the_catch_leaves_a_trace_for_the_setter():
    w = _w()
    cid = _line(w)
    _catch(w, cid)
    w.s["mind"][STRANGER].setdefault("things", {})
    TH.remember(w, STRANGER, cid, "saw", text="a brown hare caught in a snare at Mill Mead")
    r = _do(w, STRANGER, {"do": "take", "item": "meat", "from": "Mill Mead"})
    assert "took 0.7 meat from the snares at Mill Mead" in r
    assert w.s["containers"][cid]["robbed"]["by"] == STRANGER and not w.s["containers"][cid]["catch"]
    look = [f["text"] for f in _facts(w, cid, SETTER) if f.get("who") == "setter"]
    assert look == ["your snares at Mill Mead have been emptied by someone: a noose pulled open, the grass trodden round it"]
    w.s["day"] += THINGS["set"]["robbed_days"] + 1
    assert [f["text"] for f in _facts(w, cid, SETTER) if f.get("who") == "setter"] == ["nothing caught in your snares at Mill Mead"]


# ---------------------------------------------------------------------- the remembered line (§4.3)
def _lying(w, who):
    from cybertron2.engine import prompt as P
    return P._things_lines(Here(w, who), Mind(w, who))


def test_a_remembered_set_thing_never_says_empty_unless_seen_so_and_says_when_it_was_seen():
    w = _w()
    w.s["day"] = 4
    cid = _line(w, set_day=4)
    day = lambda d: f"{w.calendar(d)['season']} day {w.calendar(d)['day']}"     # noqa: E731
    assert _lying(w, SETTER) == [f"a line of snares you set at Mill Mead ({day(4)})"]
    w.s["day"] = 6
    _catch(w, cid, day=5)
    assert _lying(w, SETTER) == [f"a line of snares you set at Mill Mead ({day(4)})"]   # caught, unseen: no word of it
    TH.look(w, SETTER, cid)                                                     # seen on day 6
    assert _lying(w, SETTER) == [f"a line of snares you set at Mill Mead, with a brown hare caught in them (as you saw it on {day(6)})"]
    w.s["day"] = 7
    _do(w, SETTER, {"do": "take", "from": "the snares at Mill Mead"})
    assert _lying(w, SETTER) == [f"a line of snares you set at Mill Mead, nothing caught in them (as you saw it on {day(7)})"]
    _catch(w, cid, day=7)
    w.s["day"] = 8
    assert "nothing caught in them" in _lying(w, SETTER)[0]                    # as it was then, not as it is
    assert all("empty" not in x for x in _lying(w, SETTER))
    assert "empty" not in TH.describe(w, w.s["containers"][_line(w)])
    traps = _line(w, method="trap in water", parcel="wb_wen", set_day=8)
    _catch(w, traps, kind="eel", day=8, goods={"fish": 0.2})                    # eels are fish goods (D2-216)
    _catch(w, traps, kind="eel", day=8, goods={"fish": 0.2})
    w.s["day"] = 9
    texts = [f["text"] for f in _facts(w, traps, SETTER) if f.get("who") == "setter"]
    assert texts == ["two eels in your wicker traps at the Wen"]


# ---------------------------------------------------------------------- lifting (§4.4)
def test_lift_the_snares_at_the_parcel_takes_the_catch_into_hand_and_its_aliases():
    for act in ({"do": "lift the snares"}, {"do": "check the snares", "at": "Mill Mead"}, {"do": "lift", "from": "my snares"},
                {"do": "take", "from": "the snares at Mill Mead"}, {"do": "take", "from": "the snares at the Mead"},
                {"do": "take", "from": "snares"}, {"do": "gather", "what": "check the snares", "at": "Mill Mead"},
                {"do": "work", "what": "lift snares"}):
        w = _w()
        cid = _line(w)
        _catch(w, cid, goods={"meat": 0.7})
        hands = w.s["people"][SETTER]["hands"]
        before = w.s["containers"][hands]["goods"].get("meat", 0.0)
        r = _do(w, SETTER, act)
        assert "You took 0.7 meat from your snares at Mill Mead" in r, (act, r)
        assert abs(w.s["containers"][hands]["goods"].get("meat", 0.0) - before - 0.7) < 1e-6
        assert not any(q > 1e-9 for q in w.s["containers"][cid]["goods"].values()) and w.s["containers"][cid]["catch"] == []
    w = _w()
    _line(w)
    r = _do(w, SETTER, {"do": "check the snares"})
    assert r == "You looked over your snares at Mill Mead: nothing is caught in them."
    assert "Refused" in _do(w, STRANGER, {"do": "lift the snares"})              # one who knows of no snares here


def test_a_stranger_may_lift_a_line_found_by_naming_its_place():
    w = _w()
    cid = _line(w)
    _catch(w, cid, goods={"meat": 0.7})
    _catch(w, cid, goods={"meat": 0.7})
    r = _do(w, STRANGER, {"do": "take", "from": "the snares at Mill Mead"})     # a search, a catch plain to find (own 0.4 x 5)
    assert "took 1.4 meat from the snares at Mill Mead" in r
    assert w.s["containers"][cid]["robbed"]["by"] == STRANGER


def test_the_manual_says_come_back_and_take_what_is_in_them():
    from cybertron2.engine.data import TECHNIQUES
    assert "come back to your snares and take what is in them" in TECHNIQUES["snare"]["note"]
    assert "come back to your traps and take what is in them" in TECHNIQUES["trap in water"]["note"]
    assert "whoever's finds" not in TECHNIQUES["snare"]["note"]


# ---------------------------------------------------------------------- the catch by night (§3.1's form)
def test_a_night_catch_is_recorded_with_its_night_and_its_chance_has_no_clip(generated):  # noqa: F811
    import inspect
    src = inspect.getsource(WL._set_night)
    assert "chance(" in src and "min(0.95" not in src                         # 1 - e^(-x) (wild.chance), no clip
    world = _two(generated)
    w, _ = _summer_world(world)
    w.s["today"] = R.blank_today()
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["brown hare"][ri] = 400.0 / m.km2[ri]
    par = next(pid for pid, p in sorted(w.s["parcels"].items()) if p["node"] == "s1" and p["cover"] in ("pasture", "meadow", "field"))
    _do(w, "Ann", {"do": "gather", "what": "snare", "at": w.s["parcels"][par]["name"]})
    cid = next(c for c, x in w.s["containers"].items() if x.get("kind") == "set")
    for _ in range(8):
        night = w.d
        N.night(w)
        w.s["day"] += 1
        w.s["today"] = R.blank_today()
        c = w.s["containers"][cid]
        if c.get("catch"):
            assert all(k["day"] == night for k in c["catch"]) and len(c["catch"]) == int(c["caught"])
            st = TH.set_state(w, c)
            assert st["fresh"] and not st["birds"] and TH.catch_words(w, c)
            assert TH.own(w, c) >= THINGS["set"]["caught"]
            return
    raise AssertionError("no catch in eight nights with hares thick on the ground")


def test_the_one_rule_unchanged_for_things_that_are_not_set():
    w = _w()
    cid = w.apply("new_thing", "wenbridge", node="wenbridge", parcel="wb_green", kind="pile", by=None)
    w.apply("create", "wenbridge", dst=cid, item="grain", qty=3, why="test")
    rows, x = SG.bundle(w, w.s["containers"][cid])
    assert any(r.get("text")(x).startswith("a bundle lies at the Green") for _, r in SG.true_rows(rows, x))
    assert all(not r.get("who") for _, r in SG.true_rows(rows, x))
    assert abs(TH.own(w, w.s["containers"][cid]) - (1 - math.exp(-3 / THINGS["heap_k"]))) < 1e-9
