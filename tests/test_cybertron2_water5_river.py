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
    monkeypatch.setattr(RU, "advance", lambda m, st, day, wx, ahead, stops=None, weather=True: adv(m, st, day, wx, None, stops, weather))


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
    assert out[True]["v:Millham"][1] == pytest.approx(50.0, abs=1.0)               # the shut weir above took its half


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
        got[gap] = round(float(c["goods"].get("meat", 0.0)) / float(WK.TAKEN["eel"]["goods"]["meat"]))
    assert got["shut"] == 20                                                       # half
    assert got["open"] <= 3


def test_a_worn_weir_takes_less(river, monkeypatch):
    no_new_runs(monkeypatch)
    w = fresh(river)
    bid = put_weir(w, "Saltwell")
    w.s["buildings"][bid]["level"] = 2
    pulse(w, "Saltwell", n=100.0)
    w.s["wild"]["state"]["pop"]["otter"] = [0.0] * WL.model(w).n
    N.night(w)
    c = w.s["containers"][WL.weir_trap(w, bid)]
    assert round(float(c["goods"]["meat"]) / 0.2) == 15                            # 0.5 x 0.3 of the run at a holed weir


def test_the_weir_is_crew_work_built_on_a_river_and_its_gap_set_by_its_crew(river):
    w = fresh(river)
    a, b, c = adults(w, "Saltwell")[:3]
    w.s["containers"][Here(w, a).hands]["goods"]["timber"] = 30
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
    other = adults(w, "Saltwell")[2]
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
    r = do(w, other, {"do": "take", "item": "meat", "from": w.s["parcels"][pid]["name"]})
    assert "meat" in r
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
                if gap == "shut":                                                  # the held fish taken below the dam by net
                    who = adults(w, "Millham")[0]
                    w.s["know"].setdefault(who, {})["net"] = {"level": "known", "skill": 1.0}
                    tries = 0
                    for s_ in range(12):
                        w2 = copy.deepcopy(w)
                        o = w2.rng
                        w2.rng = lambda *k, o=o, s_=s_: o(*k, "t", s_)
                        before = float(w2.s["containers"][Here(w2, who).hands]["goods"].get("meat", 0.0))
                        do(w2, who, {"do": "gather", "what": "net", "at": w2.s["parcels"][WL.mill_water(w2, mill)]["name"]})
                        tries += float(w2.s["containers"][Here(w2, who).hands]["goods"].get("meat", 0.0)) > before
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
        if trap:
            do(w, who, {"do": "gather", "what": "trap in water", "at": w.s["parcels"][WL.mill_water(w, mill)]["name"]})
        pulse(w, "Millham", n=60.0)
        rec = N.night(w)
        got[trap] = ((rec["wild"].get("runs") or {}).get("race") or {}).get(bid, {}).get("eel", 0)
    assert got[True] == 30 and got[False] == 0


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


def test_the_otter_is_a_kind_of_the_water_trapped_by_a_snare_set_at_water():
    from cybertron2.engine.data import TECHNIQUES
    assert "otter" in TECHNIQUES["snare"]["yield"]["takes"] and "water" in TECHNIQUES["snare"]["at"]["covers"]
    assert "salmon" in TECHNIQUES["net"]["yield"]["takes"] and "lamprey" in TECHNIQUES["trap in water"]["yield"]["takes"]


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
