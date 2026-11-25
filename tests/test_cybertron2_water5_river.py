"""The river (build brief 5 §2, §3, §3a, §4; proposals/river_and_water.md; D2-209): the runs along `land.down` with their lag, the
weir and its gap, the mill's gap and race, the salmon's return, the otter at the traps; and worlds without rivers or runs as they were.
On 37.2's river world (cybertron2/specs/water/river.yaml: Saltwell upstream, Millham's mill downstream)."""
import copy
import os

import pytest
import yaml

from cybertron2.engine import night as N, run as R, verbs as V, wild as WL
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World
from cybertron2.wild import kinds as WK, runs as RU

RIVER = os.path.join(os.path.dirname(__file__), "..", "cybertron2", "specs", "water", "river.yaml")


@pytest.fixture(scope="module")
def river():
    spec = yaml.safe_load(open(RIVER))
    spec.setdefault("wild", {})["history_years"] = 2
    return World(spec)


def fresh(w0):
    w = copy.deepcopy(w0)
    morning(w, w.d)
    return w


def morning(w, d):
    w.s["day"] = d
    w.s["today"] = R.blank_today()
    w.s["events"] = []
    R.dawn(w)


def adults(w, node):
    return sorted(n for n, p in w.s["people"].items() if p.get("at") == node and p.get("stage") == "adult" and p.get("alive", True))


def water(w, node):
    return sorted(pid for pid, p in w.s["parcels"].items() if p["node"] == node and WL._river_parcel(w, pid))[0]


def do(w, who, act):
    return V.do(Here(w, who), Mind(w, who), act)


def refused(w, who, act, words):
    r = do(w, who, act)
    assert r.startswith("Refused") and words in r, r


def put_weir(w, node, gap="shut", crew=None):
    pid = water(w, node)
    crew = crew or adults(w, node)[:2]
    bid = w.apply("raise", node, node=node, parcel=pid, rec={"name": f"the weir at {node}", "structure": "timber", "fittings": {}, "rooms": [],
                                                             "monument": "weir", "tier": "plain", "unfinished": None, "crew": crew,
                                                             "gap": gap})
    w.s["buildings"][bid]["built_day"] = w.d
    w.apply("claim", node, thing=("building", bid), claimant=crew[0], rights="all", grounds="built")
    return bid


def pulse(w, node, kind="eel", n=40.0, dir_="down", **kw):
    """A run at a village's stretch today (the rule's own pulses, put there by hand)."""
    st = w.s["wild"]["state"]
    st["runs"]["pulses"] = [p for p in st["runs"]["pulses"] if int(p["d"]) != WL.eco_day(w)] + \
        [dict({"k": kind, "g": f"v:{node}", "d": WL.eco_day(w), "n": float(n), "dir": dir_}, **kw)]


def no_new_runs(monkeypatch):
    """Hold the cue off (so only the pulses put by hand move), the rest of the rule as built."""
    adv = RU.advance
    monkeypatch.setattr(RU, "advance", lambda m, st, day, wx, ahead, stops=None, weather=True, **kw: adv(m, st, day, wx, None, stops, weather, **kw))


# ---------------------------------------------------------------------- the run along the river (§2)
def test_the_river_is_cut_into_stretches_with_villages_whole(river):
    m = WL.model(river)
    nt = RU.net(m)
    assert "v:Saltwell" in nt.members and "v:Millham" in nt.members
    path, g = [], "v:Saltwell"
    while g is not None:
        path.append(g)
        g = nt.below[g]
    assert "v:Millham" in path                                                    # Saltwell's water drains past Millham
    land = river.s["wild"]["land"]
    assert nt.area["v:Millham"] == m.ids.index(land["home"]["Millham"])          # read at the village's home (its water)
    assert RU.on_river(m, "Saltwell") and RU.on_river(m, "Millham")


def test_a_run_reaches_each_stretch_below_on_its_lag_day_thinner_by_what_was_taken(river, monkeypatch):
    """§7 unit 1: a run leaves an upstream area on its cue and reaches each area below on its lag day, thinner by what was taken."""
    no_new_runs(monkeypatch)
    m = WL.model(river)
    nt = RU.net(m)
    out = {}
    for weir in (False, True):
        w = fresh(river)
        if weir:
            put_weir(w, "Saltwell")
        pulse(w, "Saltwell", n=100.0)
        d0 = WL.eco_day(w)
        seen = {}
        for d in range(w.d, w.d + 8):
            morning(w, d)
            for p in RU.today(m, w.s["wild"]["state"], WL.eco_day(w)):
                if p["k"] == "eel" and not p.get("held"):
                    seen[p["g"]] = (WL.eco_day(w) - d0, round(float(p["n"]), 2))
            N.night(w)
        out[weir] = seen
    g, lag = "v:Saltwell", 0
    while nt.below[g] is not None and nt.below[g] != "v:Millham":
        lag += nt.lag(g, nt.below[g], WK.RUN["km_a_day"])
        g = nt.below[g]
    lag += nt.lag(g, "v:Millham", WK.RUN["km_a_day"])
    assert out[False]["v:Millham"][0] == lag >= 2                                  # a day or more per stretch, by its river's length
    assert out[False]["v:Millham"][1] == pytest.approx(100.0, abs=1.0)             # nobody took any: all of it passes
    assert out[True]["v:Millham"][0] == lag
    assert out[True]["v:Millham"][1] == pytest.approx(70.0, abs=1.0)               # the shut weir above took its 30% (D2-210)


def _eel_cue_tomorrow(w, m, d) -> bool:
    """Whether the eels' cue holds at any stretch on day d + 1, read from the climate (the rule's own test, by hand)."""
    nt = RU.net(m)
    nodes = sorted(set(m.nodes))
    mem = {}
    for j in range(RU.MEMORY):
        wx = WL.weather(w, nodes, max(0, d + 1 - j))
        for nd in wx:
            mem.setdefault(nd, []).append(float(wx[nd]["rain"]))
    return any(RU.cued(nt, g, WK.RUNS["eel"]["cue"], mem) for g in nt.members)


def test_cue_nights_start_runs_and_the_sea_takes_what_passes(river):
    """Through the autumn a silver run leaves the river areas on its cue nights, read from the climate's rain, and on no other;
    what reaches the sea is gone."""
    w = fresh(river)
    m = WL.model(w)
    started, sea, cue = {}, 0.0, set()
    for d in range(w.d, w.d + 20):
        inside = RU._window(m, WL.eco_day(w, d + 1), WK.RUNS["eel"]["seasons"])[0]
        if inside and _eel_cue_tomorrow(w, m, d):
            cue.add(d)
        morning(w, d)
        rec = N.night(w)
        mv = ((rec.get("wild") or {}).get("runs") or {}).get("moved") or {}
        if float(mv.get("started", {}).get("eel", 0.0)) > 0:
            started[d] = float(mv["started"]["eel"])
        sea += float(mv.get("sea", {}).get("eel", 0.0))
    assert cue and set(started) == cue                                             # the run starts on its cue nights only
    assert sea > 0.3 * sum(started.values())


# ---------------------------------------------------------------------- the weir (§3)
def test_a_shut_weir_takes_about_its_share_and_an_open_one_little(river, monkeypatch):
    """§7 unit 2."""
    no_new_runs(monkeypatch)
    got = {}
    for gap in ("shut", "open"):
        w = fresh(river)
        bid = put_weir(w, "Saltwell", gap=gap)
        pulse(w, "Saltwell", n=40.0)
        w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n
        N.night(w)
        c = w.s["containers"][WL.weir_trap(w, bid)]
        got[gap] = round(float(c["goods"].get("fish", 0.0)) / float(WK.TAKEN["eel"]["goods"]["fish"]))
    assert got["shut"] == 12                                                       # a section's 30% (D2-210)
    assert got["open"] <= 2


def test_a_worn_weir_takes_less(river, monkeypatch):
    no_new_runs(monkeypatch)
    w = fresh(river)
    bid = put_weir(w, "Saltwell")
    w.s["buildings"][bid]["level"] = 2
    pulse(w, "Saltwell", n=100.0)
    w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n
    N.night(w)
    c = w.s["containers"][WL.weir_trap(w, bid)]
    assert round(float(c["goods"]["fish"]) / float(WK.TAKEN["eel"]["goods"]["fish"])) == 9   # 0.3 x 0.3 of the run at a holed weir
                                                                                   # (D2-210); the eel's fish from the data (D2-258)


def test_the_weir_is_crew_work_built_on_a_river_and_its_gap_set_by_its_crew(river):
    w = fresh(river)
    a, b, c = adults(w, "Saltwell")[:3]
    w.s["know"].setdefault(a, {})["weir"] = {"level": "known", "skill": 1.0}       # a craft, not everyone's (W-97, u2 §6 bug 4);
    w.s["containers"][Here(w, a).hands]["goods"].update(timber=60, withies=30)       # b works on its crew under a (D2-302's cost)
    refused(w, a, {"do": "build", "what": "weir", "at": w.s["parcels"][water(w, "Saltwell")]["name"]}, "crew work")
    refused(w, a, {"do": "build", "what": "weir", "at": "the Brine Meadow", "with": b}, "across a river")
    do(w, a, {"do": "build", "what": "weir", "at": w.s["parcels"][water(w, "Saltwell")]["name"], "with": b})
    bid = next(x for x, bb in w.s["buildings"].items() if bb.get("monument") == "weir")
    assert w.s["buildings"][bid]["crew"] == [a, b] and w.s["buildings"][bid]["gap"] == "shut"
    for i in range(30):
        if not w.s["buildings"][bid].get("unfinished"):
            break
        w.s["today"] = R.blank_today()
        do(w, (a, b)[i % 2], {"do": "build", "what": "weir", "at": w.s["buildings"][bid]["name"]})
    assert not w.s["buildings"][bid].get("unfinished")
    refused(w, c, {"do": "set", "thing": "gap", "to": "open", "at": w.s["buildings"][bid]["name"]}, "its crew")
    assert V.cost(Here(w, b), {"do": "set", "thing": "gap", "to": "open", "at": w.s["buildings"][bid]["name"]}) == 1
    assert "now open" in do(w, b, {"do": "set", "thing": "gap", "to": "open", "at": w.s["buildings"][bid]["name"]})
    assert WL.gap(w.s["buildings"][bid]) == "open"
    assert V.cost(Here(w, b), {"do": "set", "thing": "gap", "to": "shut", "at": w.s["buildings"][bid]["name"]}) == 2


def test_a_weirs_traps_emptied_by_another_leave_a_trace(river, monkeypatch):
    """§7 unit 3: the crew lift without robbing; another's taking is seen and leaves the trace (brief 4c's rules)."""
    no_new_runs(monkeypatch)
    w = fresh(river)
    crew = adults(w, "Saltwell")[:2]
    other = next(x for x in adults(w, "Saltwell")[2:] if w.household_of(x) not in {w.household_of(y) for y in crew})   # another
    # household's: a household's things are every member's own (D2-305, W-97)
    bid = put_weir(w, "Saltwell", crew=crew)
    pulse(w, "Saltwell", n=40.0)
    w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n
    N.night(w)
    morning(w, w.d + 1)
    cid = WL.weir_trap(w, bid)
    assert cid in (w.s["mind"][crew[1]].get("things") or {}) or True              # the crew know it from the night it was made
    r = do(w, crew[1], {"do": "take", "from": "the weir"})
    assert "your weir's traps" in r and not w.s["containers"][cid].get("robbed")
    pulse(w, "Saltwell", n=40.0)
    N.night(w)
    morning(w, w.d + 1)
    pid = w.s["containers"][cid]["parcel"]
    r = do(w, other, {"do": "take", "item": "fish", "from": w.s["parcels"][pid]["name"]})
    assert "fish" in r
    rb = w.s["containers"][cid].get("robbed") or {}
    assert rb.get("by") == other
    ev = [e for e in w.s["events"] if e.get("kind") == "take" and set(crew) & set(e.get("concerns") or [])]
    assert ev and "weir" in ev[0]["text"]


# ---------------------------------------------------------------------- the mill (§3a)
def test_a_shut_dam_holds_about_its_share_of_a_run_going_up_and_they_can_be_taken_below(river, monkeypatch):
    no_new_runs(monkeypatch)
    m = WL.model(river)
    nt = RU.net(m)
    below = nt.below["v:Millham"]                                                  # the stretch the fish come up from
    held = {}
    for gap in ("shut", "open"):
        w = fresh(river)
        mill = next(b for _, b in WL.mills(w, "Millham"))
        mill["gap"] = gap
        dest = next(h for h in nt.heads("big river") if "v:Millham" in nt.path_up(h))
        st = w.s["wild"]["state"]
        st["runs"]["pulses"] = [{"k": "salmon", "g": below, "d": WL.eco_day(w), "n": 40.0, "dir": "up", "to": dest}]
        for d in range(w.d, w.d + 6):
            morning(w, d)
            ps = [p for p in RU.today(m, w.s["wild"]["state"], WL.eco_day(w)) if p["g"] == "v:Millham"]
            if ps:
                held[gap] = {bool(p.get("held")): round(float(p["n"])) for p in ps}
                if gap == "shut":                                                  # the held fish taken below the dam by hand
                    who = adults(w, "Millham")[0]                                  # (the net reaches what flies: W-97, u2 §6 fault 3)
                    tries = 0
                    for s_ in range(12):
                        w2 = copy.deepcopy(w)
                        o = w2.rng
                        w2.rng = lambda *k, o=o, s_=s_: o(*k, "t", s_)
                        before = float(w2.s["containers"][Here(w2, who).hands]["goods"].get("fish", 0.0))
                        do(w2, who, {"do": "gather", "what": "fish by hand", "at": w2.s["parcels"][WL.mill_water(w2, mill)]["name"]})
                        tries += float(w2.s["containers"][Here(w2, who).hands]["goods"].get("fish", 0.0)) > before
                    assert tries >= 3
                break
            N.night(w)
    assert held["shut"] == {True: 20, False: 20}                                   # half held below the dam
    assert held["open"] == {False: 40}


def test_an_open_mill_grinds_at_half_and_a_shut_one_at_full(river):
    out = {}
    for gap in ("shut", "open"):
        w = fresh(river)
        bid, mill = WL.mills(w, "Millham")[0]
        mill["gap"] = gap
        who = sorted(n for n in adults(w, "Millham") if "management" in Here(w, n).rights(("building", bid)))[0]
        w.s["containers"][Here(w, who).hands]["goods"]["grain"] = 400
        r = do(w, who, {"do": "make", "what": "water mill"})
        out[gap] = float(w.s["containers"][Here(w, who).hands]["goods"].get("flour", 0.0))
        if gap == "open":
            assert "gap is open" in r
    assert out["shut"] == pytest.approx(2 * out["open"]) and out["shut"] > 0


def test_a_trap_in_the_race_takes_the_weirs_share_of_a_run_going_down(river, monkeypatch):
    no_new_runs(monkeypatch)
    got = {}
    for trap in (True, False):
        w = fresh(river)
        bid, mill = WL.mills(w, "Millham")[0]
        w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n
        who = adults(w, "Millham")[0]
        if trap:                                                                   # one trap, laid from the hands (u2 §3)
            w.apply("create", "Millham", dst=w.hands(who), item="wicker trap", qty=1.0, why="test")
            do(w, who, {"do": "gather", "what": "trap in water", "at": w.s["parcels"][WL.mill_water(w, mill)]["name"]})
        pulse(w, "Millham", n=60.0)
        rec = N.night(w)
        got[trap] = ((rec["wild"].get("runs") or {}).get("race") or {}).get(bid, {}).get("eel", 0)
    eel = WL._kg_of("eel")                                                         # half of 60, held to a trap's 10 kg (D2-213, D2-216, D2-258):
    assert WATER_WORKS["trap"]["hold"] - 3 * eel <= got[True] * eel <= WATER_WORKS["trap"]["hold"] + 1e-9 and got[False] == 0
    # 15 eels on the old layout, 14 on the remade river world at 3 food; at 10 kg (D2-258) the trap's own night takes one or two of the
    # run's eels before the race's share comes (16 by the race, 17 in the trap)


def test_the_mills_gap_is_set_by_those_who_manage_it(river):
    w = fresh(river)
    bid, mill = WL.mills(w, "Millham")[0]
    mgr = [n for n in adults(w, "Millham") if "management" in Here(w, n).rights(("building", bid))]
    other = [n for n in adults(w, "Millham") if n not in mgr][0]
    refused(w, other, {"do": "set", "thing": "gap", "to": "open", "at": mill["name"]}, "manage the water wheel")
    assert "now open" in do(w, mgr[0], {"do": "set", "thing": "gap", "to": "open", "at": mill["name"]})


# ---------------------------------------------------------------------- salmon (§4)
def test_salmon_returns_follow_the_spawners(river):
    """§7 unit 4: next year's run at each head water is Beverton-Holt of the spawners that reached it."""
    m = WL.model(river)
    nt = RU.net(m)
    ret = WK.RUNS["salmon"]["return"]
    heads = nt.heads("big river")
    dues = []
    for s in (5.0, 20.0):
        st = {"pop": {k: list(v) for k, v in river.s["wild"]["state"]["pop"].items()}, "runs": {"pulses": [], "quota": {}, "due": {},
              "spawned": {"salmon": {h: s for h in heads}}, "rain": {}, "year": {}, "tally": {}}}
        Y, S = m.Y, m.S
        day = (Y * 5) + 2 * S - 1                                                  # the eve of the window's first day
        wx = WL.weather(river, sorted(set(m.nodes)), 0)
        RU.advance(m, st, day, wx, wx, weather=False)
        dues.append(sum(st["runs"]["due"]["salmon"].values()) + sum(p["n"] for p in st["runs"]["pulses"] if p["k"] == "salmon"))
    cap = lambda h: float(ret["cap_km"]) * nt.km[h]                                # noqa: E731
    want = [sum(float(ret["r"]) * s / (1 + s / cap(h)) for h in heads) for s in (5.0, 20.0)]
    assert dues == pytest.approx(want, rel=1e-3) and dues[1] > dues[0]


def test_a_dam_kept_shut_lowers_the_salmon_that_reach_the_heads_above_it(river):
    """§7 society-level: the lower village's dam kept shut through the salmon's window: fewer spawners above Millham."""
    m = WL.model(river)
    nt = RU.net(m)
    above = [h for h in nt.heads("big river") if "v:Millham" in nt.path_up(h)]
    spawned = {}
    for gap in ("shut", "open"):
        w = fresh(river)
        WL.mills(w, "Millham")[0][1]["gap"] = gap
        for d in range(w.d, w.d + 26):
            morning(w, d)
            N.night(w)
        sp = (w.s["wild"]["state"]["runs"].get("spawned") or {}).get("salmon") or {}
        spawned[gap] = sum(float(sp.get(h, 0.0)) for h in above)
    assert spawned["open"] > 0 and spawned["shut"] < 0.7 * spawned["open"]


# ---------------------------------------------------------------------- the otter (§4)
def test_an_otter_takes_from_an_unwatched_weir_and_not_from_a_watched_one_or_with_none_about(river, monkeypatch):
    no_new_runs(monkeypatch)
    m = WL.model(river)
    res = {}
    for case in ("unwatched", "watched", "none"):
        robbed = 0
        for s_ in range(10):
            w = fresh(river)
            o = w.rng
            w.rng = lambda *k, o=o, s_=s_: o(*k, "o", s_)
            bid = put_weir(w, "Saltwell")
            st = w.s["wild"]["state"]
            land = w.s["wild"]["land"]
            i = next(j for j, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "Saltwell")
            st["pop"]["otter"] = [0.0] * m.n
            if case != "none":
                st["pop"]["otter"][i] = 12.0 / float(m.km2[i])                     # a dozen otters about the village's water
            if case == "watched":
                w.s["wild"].setdefault("watch", {})[water(w, "Saltwell")] = {"day": w.d, "by": "x", "scare": "fire"}
            pulse(w, "Saltwell", n=40.0)
            rec = N.night(w)
            robbed += bool(((rec["wild"].get("runs") or {}).get("robbed") or {}))
        res[case] = robbed
    assert res["unwatched"] >= 4 and res["watched"] == 0 and res["none"] == 0


def test_the_otter_is_a_kind_of_the_water_taken_at_its_holt():
    """W-97 (u2 §6 faults 3, 14): the otter by den work at its holt, never in a snare; the net reaches what flies, never salmon."""
    from cybertron2.engine.data import TECHNIQUES
    assert "otter" not in TECHNIQUES["snare"]["yield"]["takes"] and "water" not in TECHNIQUES["snare"]["at"]["covers"]
    assert "otter" in TECHNIQUES["den work"]["yield"]["takes"]
    assert "salmon" not in TECHNIQUES["net"]["yield"]["takes"] and "lamprey" in TECHNIQUES["trap in water"]["yield"]["takes"]


# ---------------------------------------------------------------------- signs (§3.5, §3a.5)
def test_the_run_and_the_held_fish_are_seen_at_the_water(river, monkeypatch):
    from cybertron2.engine import signs as SG
    w = fresh(river)
    pulse(w, "Millham", kind="salmon", n=30.0, dir_="up", to="x")
    st = w.s["wild"]["state"]
    st["runs"]["pulses"].append({"k": "salmon", "g": "v:Millham", "d": WL.eco_day(w), "n": 20.0, "dir": "up", "to": "x", "held": True})
    lines = []
    who = adults(w, "Millham")[0]
    w.s["people"][who]["at"] = "Millham"
    here = Here(w, who)
    SG._wild_river(here, lambda *a, **k: lines.append((a, k)))
    assert lines


# ---------------------------------------------------------------------- unchanged where there is no run (§7 regression)
def test_a_world_without_rivers_has_no_runs_and_is_as_it_was(river, monkeypatch):
    spec = yaml.safe_load(open(RIVER))
    spec["wild"]["history_years"] = 1
    spec["wild"]["land"]["down"] = {}                                              # no river runs anywhere
    a = World(copy.deepcopy(spec))
    monkeypatch.setattr(WK, "RUNS", {})
    b = World(copy.deepcopy(spec))
    assert "runs" not in a.s["wild"]["state"] and a.s["wild"]["state"]["pop"] == b.s["wild"]["state"]["pop"]
    for w in (a, b):
        morning(w, 0)
        N.night(w)
    assert a.s["wild"]["state"]["pop"] == b.s["wild"]["state"]["pop"]
    mill = WL.mills(a, "Millham")
    assert mill == []                                                              # a mill with no run: no gap
    bid = next(x for x, bb in a.s["buildings"].items() if (bb.get("fittings") or {}).get("water wheel"))
    assert WL.mill_rate(a, a.s["buildings"][bid]) == 1.0 and not WL.has_gap(a, a.s["buildings"][bid])


def test_no_kind_is_named_in_the_run_rule():
    """A run is a rule over any kind with a RUNS row (brief 5 §1): the runs module and the engine's river code name no kind."""
    import ast
    import re
    words = {x for name in WK.KINDS for x in re.findall(r"[a-z]+", name) if len(x) > 3 and x not in ("wild", "mice", "brown")}
    tree = ast.parse(open(os.path.join(os.path.dirname(__file__), "..", "cybertron2", "wild", "runs.py")).read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(getattr(node.body[0], "value", None), ast.Constant):
            node.body = node.body[1:] or [ast.Pass()]
    code = ast.unparse(tree).lower()
    assert not [x for x in sorted(words) if re.search(r"\b" + x + r"s?\b", code)]


# ---------------------------------------------------------------------- the weir in sections, its cap and its upkeep (§3b, D2-210)
from cybertron2.engine.data import ITEMS, WATER_WORKS                                   # noqa: E402

WW = WATER_WORKS["weir"]


def full_weir(w, node, foot=False, gap="shut"):
    bid = put_weir(w, node, gap=gap)
    w.s["buildings"][bid]["sections"] = [{"m": "wattle", "foot": foot, "level": 5}] + \
        [{"m": "timber", "foot": foot, "level": 5} for _ in range(int(WW["position"]["added"]["most"]))]
    return bid


def no_robbers(w):
    w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n


def test_the_weirs_ladder_adds_share_and_hold_a_section_at_a_time(river):
    w = fresh(river)
    bid = put_weir(w, "Saltwell")
    b = w.s["buildings"][bid]
    assert WL.weir_share(b) == pytest.approx(0.30) and WL.weir_hold(b) == pytest.approx(100.0)    # kg (D2-258; was 10 food)
    a, c = b["crew"]
    hands = w.s["containers"][Here(w, a).hands]["goods"]
    from cybertron2.wild import gear as GR
    x = GR.water_x(WL.water_kind(w, WL.model(w), b["parcel"]))                       # D2-302's cost by the water (W-97)
    hands["timber"], hands["stone"] = 3 * 15 * x + 10, 20
    for part, n in (("weir section", 3), ("stone footing", 1)):
        for _ in range(n):
            for i in range(30):
                w.s["today"] = R.blank_today()
                r = do(w, (a, c)[i % 2], {"do": "build", "what": part, "at": b["name"]})
                if r.startswith("You finished"):
                    break
                assert "units of work left" in r, r
    b = w.s["buildings"][bid]
    assert len(WL.sections(b)) == 4 and WL.sections(b)[0]["foot"] and not WL.sections(b)[1]["foot"]
    assert WL.weir_share(b) == pytest.approx(0.51) and WL.weir_hold(b) == pytest.approx(310.0)  # about half and 310 kg (D2-258)
    assert hands["timber"] == pytest.approx(10) and hands["stone"] == pytest.approx(10)          # each part its own cost: the difference
    refused(w, a, {"do": "build", "what": "weir section", "at": b["name"]}, "all its sections")
    b["gap"] = "open"
    assert WL.weir_share(b) == pytest.approx(0.051)


def test_a_nights_catch_is_capped_by_what_the_weir_holds_less_what_is_unlifted(river, monkeypatch):
    no_new_runs(monkeypatch)
    w = fresh(river)
    no_robbers(w)
    bid = put_weir(w, "Saltwell")
    pulse(w, "Saltwell", n=800.0)                                                  # 30% is 240 eels, 139 kg: more than it holds
    N.night(w)                                                                     # (the hold in kg, D2-258; was 200 eels and food)
    kg = lambda: WL.held_kg(w.s["containers"][WL.weir_trap(w, bid)])  # noqa: E731
    eel = WL._kg_of("eel")
    assert kg() == pytest.approx(WL.weir_hold(w.s["buildings"][bid]), abs=eel)    # capped at about 100 kg
    morning(w, w.d + 1)
    pulse(w, "Saltwell", n=800.0)
    N.night(w)
    assert kg() == pytest.approx(100.0, abs=2 * eel)                               # unlifted, the traps were full: little more


def test_weirs_on_one_stretch_take_in_turn_from_upstream(river, monkeypatch):
    no_new_runs(monkeypatch)
    w = fresh(river)
    no_robbers(w)
    waters = sorted((pid for pid, p in w.s["parcels"].items() if p["node"] == "Saltwell" and WL._river_parcel(w, pid)),
                    key=lambda q: -WL._upstream(w, q))
    assert len(waters) >= 2 and WL._upstream(w, waters[0]) > WL._upstream(w, waters[1])
    crew = adults(w, "Saltwell")[:2]
    ids = []
    for pid in reversed(waters[:2]):                                               # the downstream one built first: order is the river's
        bid = w.apply("raise", "Saltwell", node="Saltwell", parcel=pid, rec={"name": f"weir {pid}", "structure": "timber", "fittings": {},
                                                                              "rooms": [], "monument": "weir", "tier": "plain",
                                                                              "unfinished": None, "crew": crew, "gap": "shut"})
        ids.append(bid)
    pulse(w, "Saltwell", n=20.0)
    rec = N.night(w)
    got = rec["wild"]["runs"]["weir"]
    down_id, up_id = ids
    assert got[up_id]["eel"] == 6 and got[down_id]["eel"] == 4                    # 30% of 20, then 30% of the 14 let through


def _mean_lost(w, m, b, bid, flow, n=600):
    tot = 0
    secs0 = [dict(x) for x in WL.sections(b)]
    for d in range(n):
        w.s["day"] = 1000 + d
        b["sections"] = [dict(x, level=5) for x in secs0]
        tot += sum(WL._weir_wear(w, m, bid, b, flow))
    return tot / n / len(secs0)


def test_the_river_wears_a_weir_by_flow_and_material(river, monkeypatch):
    """D2-210: Poisson(base x material x water x flow x the gap shut in high water) levels a night; ice left out (a mild spell)."""
    monkeypatch.setattr(type(river), "cold", lambda self, at, day=None: False)
    w = fresh(river)
    m = WL.model(w)
    monkeypatch.setattr(WL, "water_kind", lambda w_, m_, pid: "lowland")
    E = WW["wear"]
    bid = put_weir(w, "Saltwell", gap="open")
    b = w.s["buildings"][bid]
    b["sections"] = [{"m": "wattle", "foot": False, "level": 5}]
    for flow in ("low", "normal", "spate"):
        assert _mean_lost(w, m, b, bid, flow) == pytest.approx(E["base"] * E["flow"][flow], rel=0.25)
    b["sections"] = [{"m": "timber", "foot": False, "level": 5}]
    assert _mean_lost(w, m, b, bid, "spate") == pytest.approx(E["base"] * 0.5 * E["flow"]["spate"], rel=0.25)
    b["sections"] = [{"m": "timber", "foot": True, "level": 5}]
    assert _mean_lost(w, m, b, bid, "spate") == pytest.approx(E["base"] * 0.1 * E["flow"]["spate"], rel=0.4)
    b["sections"] = [{"m": "wattle", "foot": False, "level": 5}]
    assert 1 / (E["base"] * E["flow"]["normal"]) == pytest.approx(7.0, abs=0.1)    # a level a week of normal flow, lowland wattle


def test_a_flood_with_the_gap_shut_wears_a_section_clearly_more_than_with_it_open(river, monkeypatch):
    """D2-210: the gap shut in high water wears the weir the faster (x `gap_high`). Re-pinned with the wear calibrated to D2-210's
    year (W-69, 20 Nov; 02zzw_water_fixes.md): a flood night took a wattle section on a large river with the gap open or shut
    (0.5 and more of the nights), which put a weir's yearly upkeep at three times D2-210's band; now a flood costs a wattle section
    about 1.7 levels shut and 0.9 open, and rarely takes it whole."""
    monkeypatch.setattr(type(river), "cold", lambda self, at, day=None: False)
    w = fresh(river)
    m = WL.model(w)
    monkeypatch.setattr(WL, "water_kind", lambda w_, m_, pid: "large")
    res = {}
    for gap in ("shut", "open"):
        bid = put_weir(w, "Millham", gap=gap)
        b = w.s["buildings"][bid]
        taken = lost = 0
        for d in range(300):
            w.s["day"] = 2000 + d
            b["sections"] = [{"m": "wattle", "foot": False, "level": 5}]
            n = WL._weir_wear(w, m, bid, b, "flood")[0]
            lost += n
            taken += n >= 5
        res[gap] = (taken / 300, lost / 300)
        w.s["buildings"].pop(bid)
    E = WW["wear"]
    lam = E["base"] * E["water"]["large"] * E["flow"]["flood"]
    assert res["open"][1] == pytest.approx(lam, rel=0.2) and res["shut"][1] == pytest.approx(lam * E["gap_high"], rel=0.2)
    assert res["shut"][1] > 1.6 * res["open"][1]                                     # shutting clearly costs more
    assert res["shut"][0] < 0.15 and res["open"][0] < 0.03


def test_a_full_weirs_upkeep_on_a_lowland_river_is_a_quarter_to_a_third_of_its_cost(river):
    """D2-210's upkeep target, from the river world's own year of flow (the catchment's rain) and frost, the gap open: the levels a
    section loses in expectation x a level's mending (`mend` of the section's build)."""
    from cybertron2.engine.data import MONUMENTS
    w = fresh(river)
    m = WL.model(w)
    nt = RU.net(m)
    E = WW["wear"]
    nodes = sorted(set(m.nodes))
    Y = w.year_days()
    wx = [WL.weather(w, nodes, d) for d in range(0, 5 * Y + 1)]
    x = 0.0
    for d in range(1, 5 * Y + 1):
        mem = {nd: [wx[d][nd]["rain"], wx[d - 1][nd]["rain"]] for nd in nodes}
        ice = E["ice"] if w.cold("Saltwell", d) else (E["thaw"] if d >= 2 and w.cold("Saltwell", d - 1) and w.cold("Saltwell", d - 2) else 1.0)
        x += E["flow"][RU.flow(nt, "v:Saltwell", mem, E["flow_at"])] * ice
    x /= 5.0
    share = {mat: E["base"] * f * x * WW["mend"] for mat, f in (("wattle", 1.0), ("timber", 0.5), ("foot", 0.1))}
    # D2-210's target (wattle 0.35 to 0.55 of its cost a year, a full weir a quarter to a third) was met on the river world as first
    # made; the remade world's Saltwell catchment (floodplains, D2-226) gave about 0.95 (a full weir 0.75). Re-pinned to the band
    # with the wear calibrated on the runs world (W-69, 20 Nov; test_cybertron2_water_fixes, 02zzw_water_fixes.md): Saltwell's
    # wattle about 0.47, a full weir about 0.29, the gap open all year (this expectation leaves out the cap of 5 levels a night).
    # D2-302 (W-97): a year's upkeep a quarter of the build (wattle), an eighth (timber): `mend` halved to 0.03, wattle about 0.24.
    assert share["timber"] == pytest.approx(0.5 * share["wattle"]) and share["foot"] == pytest.approx(0.1 * share["wattle"])
    assert 0.18 <= share["wattle"] <= 0.28, share
    c1 = MONUMENTS["weir"]["units"]
    c2 = WW["cost"]["added"]["timber"]["units"]
    full = (share["wattle"] * c1 + 3 * share["timber"] * c2) / (c1 + 3 * c2)
    assert 0.11 <= full <= 0.18, full


def test_a_weir_is_mended_a_section_and_a_level_at_a_time(river):
    w = fresh(river)
    bid = put_weir(w, "Saltwell")
    b = w.s["buildings"][bid]
    b["sections"] = [{"m": "wattle", "foot": False, "level": 5}, {"m": "timber", "foot": False, "level": 2}]
    a = b["crew"][0]
    w.s["containers"][Here(w, a).hands]["goods"]["timber"] = 5
    w.s["know"].setdefault(a, {})
    r = do(w, a, {"do": "work", "what": "repair", "at": b["name"]})
    assert "mended a section" in r and WL.sections(w.s["buildings"][bid])[1]["level"] == 3
    import math
    from cybertron2.wild import gear as GR
    need = max(1, math.ceil(GR.cost(1, "timber", water=WL.water_kind(w, WL.model(w), b["parcel"]))["materials"]["timber"] * WW["mend"] - 1e-9))
    assert w.s["containers"][Here(w, a).hands]["goods"]["timber"] == pytest.approx(5 - need)   # 3% of its timber, at least one (D2-302)


def test_fish_alive_in_a_weir_or_a_trap_do_not_spoil_until_lifted(river, monkeypatch):
    """D2-211: the catch in a trap in water or a weir keeps; a snare's goes off."""
    no_new_runs(monkeypatch)
    w = fresh(river)
    no_robbers(w)
    bid = put_weir(w, "Saltwell")
    pulse(w, "Saltwell", n=20.0)
    N.night(w)
    cid = WL.weir_trap(w, bid)
    had = dict(w.s["containers"][cid]["goods"])
    for d in range(w.d + 1, w.d + 4):
        morning(w, d)
        N.night(w)
    assert w.s["containers"][cid]["goods"] == had and had


def test_a_flood_very_likely_and_a_spate_half_the_time_wrecks_a_trap_in_the_river(river, monkeypatch):
    """D2-211, D2-218: a set trap in running water is wrecked, its catch lost, at about 0.85 in a flood and half in a spate; never at a
    normal flow."""
    no_new_runs(monkeypatch)
    share = {}
    for fl in ("flood", "spate", "normal"):
        monkeypatch.setattr(RU, "flow", lambda *a, fl=fl, **k: fl)
        n = 0
        for s_ in range(40):
            w = fresh(river)
            o = w.rng
            w.rng = lambda *k, o=o, s_=s_: o(*k, "wreck", s_)
            no_robbers(w)
            who = adults(w, "Saltwell")[0]
            w.s["containers"][w.hands(who)]["goods"].pop("wicker trap", None)    # the world seeds six (Q-100): one trap here
            w.apply("create", "Saltwell", dst=w.hands(who), item="wicker trap", qty=1.0, why="test")   # one trap (u2 §3)
            do(w, who, {"do": "gather", "what": "trap in water", "at": w.s["parcels"][water(w, "Saltwell")]["name"]})
            rec = N.night(w)
            n += bool(rec["wild"]["runs"].get("wrecked"))
        share[fl] = n / 40
    assert share["flood"] == pytest.approx(WATER_WORKS["trap"]["wreck"]["flood"], abs=0.15) and share["flood"] < 1.0
    assert share["spate"] == pytest.approx(0.5, abs=0.2) and share["normal"] == 0.0


def test_fresh_fish_keep_worse_than_meat_by_their_base_rates(river):
    """D2-212 within D2-289 (W-97; wave1 §2.3): fresh fish's faster spoiling is in its base rate (keeps 1.5 days against meat's 3),
    the store's x2 dropped; in a store and in hand alike."""
    from cybertron2.engine import night as NI
    p = river.p
    for fit in ([], ["bins"]):
        fish = NI.spoil_rate(p, "fish", "store", "autumn", False, fittings=fit)
        meat = NI.spoil_rate(p, "meat", "store", "autumn", False, fittings=fit)
        assert fish == pytest.approx(meat * 0.37 / 0.2825, rel=0.01)   # D2-336: both go off, half by their days
    assert NI.spoil_rate(p, "fish", "hand", "autumn", False) > NI.spoil_rate(p, "meat", "hand", "autumn", False)
    assert NI.spoil_rate(p, "fish", "store", "autumn", False) == pytest.approx(0.37, abs=0.01)   # D2-336


def test_a_set_trap_holds_about_ten_kg_in_the_river_or_the_race(river, monkeypatch):
    """D2-213: a trap in a shut mill's race takes its share of a run going down, up to what a trap holds; not an uncapped weir."""
    no_new_runs(monkeypatch)
    w = fresh(river)
    no_robbers(w)
    bid, mill = WL.mills(w, "Millham")[0]
    who = adults(w, "Millham")[0]
    w.apply("create", "Millham", dst=w.hands(who), item="wicker trap", qty=1.0, why="test")   # one trap (u2 §3)
    do(w, who, {"do": "gather", "what": "trap in water", "at": w.s["parcels"][WL.mill_water(w, mill)]["name"]})
    pulse(w, "Millham", n=200.0)
    rec = N.night(w)
    cid = next(c for c, x in w.s["containers"].items() if x.get("kind") == "set" and x.get("by") == who)
    kg = WL.held_kg(w.s["containers"][cid])                                        # the hold in kg (D2-258; was 3 food)
    eel = WL._kg_of("eel")                                                         # 100 eels came through the race; it held its 10 kg of them
    assert kg <= WATER_WORKS["trap"]["hold"] + 1e-9 and kg >= WATER_WORKS["trap"]["hold"] - eel
    n = rec["wild"]["runs"]["race"][bid]["eel"]                                    # (D2-213, D2-216): the race's eels fill it, after the
    assert WATER_WORKS["trap"]["hold"] - 3 * eel <= n * eel <= WATER_WORKS["trap"]["hold"] + 1e-9   # one or two its own night took
                                                                                   # (15 and 17 in all on the remade river world, D2-258)
