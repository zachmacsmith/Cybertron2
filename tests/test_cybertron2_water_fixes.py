"""The water fixes (W-69, 20 Nov; proposals/river_and_water.md History; docs/review/37_growth/02zzw_water_fixes.md): a weir's
sections by position and material, the gear sharing a run within a parcel and in turn between parcels, and the weir's wear
calibrated to D2-210's year on the runs world."""
import copy
import math
import os

import pytest
import yaml

from cybertron2.engine import night as N, wild as WL
from cybertron2.engine.data import MONUMENTS, WATER_WORKS
from cybertron2.engine.here import Here
from cybertron2.wild import gear as GR, runs as RU

from tests.test_cybertron2_water5_river import (adults, do, fresh, no_new_runs, no_robbers, pulse, put_weir, refused, river,  # noqa: F401
                                                water)

WW = WATER_WORKS["weir"]
RUNS_HIGH = os.path.join(os.path.dirname(__file__), "..", "cybertron2", "specs", "nutrition", "runs_high.yaml")


# ---------------------------------------------------------------------- 1. position decides share and hold, material wear and cost
def test_position_decides_share_and_hold_and_material_decides_wear():
    timber_first = [{"m": "timber", "foot": False, "level": 5}]
    wattle_first = [{"m": "wattle", "foot": False, "level": 5}]
    assert GR.share(timber_first) == pytest.approx(0.30) and GR.hold(timber_first) == pytest.approx(100.0)
    assert GR.share(wattle_first) == GR.share(timber_first) and GR.hold(wattle_first) == GR.hold(timber_first)
    assert GR.wear_of(timber_first[0]) == pytest.approx(0.5) and GR.wear_of(wattle_first[0]) == pytest.approx(1.0)
    two_wattle = wattle_first + [{"m": "wattle", "foot": False, "level": 5}]
    assert GR.share(two_wattle) == pytest.approx(0.37) and GR.hold(two_wattle) == pytest.approx(170.0)
    assert GR.wear_of(two_wattle[1]) == pytest.approx(1.0)                              # an added wattle section wears as wattle
    assert GR.wear_of({"m": "timber", "foot": True, "level": 5}) == pytest.approx(0.1)  # a footing's rate, whatever stands on it


def test_an_old_list_of_sections_means_what_it_did():
    """Before 20 Nov the first section was always wattle and the added ones timber; the same list keeps its share, hold and wear, and
    a list of the materials' names alone loads as sound sections at the building's level."""
    old = [{"m": "wattle", "foot": False, "level": 5}] + [{"m": "timber", "foot": False, "level": 5}] * 3
    assert GR.share(old) == pytest.approx(0.51) and GR.hold(old) == pytest.approx(310.0)
    assert [GR.wear_of(sc) for sc in old] == [1.0, 0.5, 0.5, 0.5]
    b = {"monument": "weir", "level": 4, "condition": 2, "sections": ["wattle", "timber", "timber"]}
    secs = WL.sections(b)
    assert secs == [{"m": "wattle", "foot": False, "level": 4}, {"m": "timber", "foot": False, "level": 4},
                    {"m": "timber", "foot": False, "level": 4}]
    assert WL.weir_share(b) == pytest.approx(0.8 * 0.44) and WL.weir_hold(b) == pytest.approx(0.8 * 240.0)
    assert WL.sections({"monument": "weir", "level": 3, "condition": 1}) == [{"m": "wattle", "foot": False, "level": 3}]


def test_a_sections_cost_is_its_materials_and_the_firsts_adds_the_weirs_stakes():
    assert GR.cost(0, "wattle") == {"materials": MONUMENTS["weir"]["materials"], "units": MONUMENTS["weir"]["units"]}   # as built
    assert GR.cost(1, "timber") == {"materials": {"timber": 10}, "units": 25}                                              # as before
    assert GR.cost(0, "timber")["materials"]["timber"] > GR.cost(0, "wattle")["materials"]["timber"]                      # timber dearer
    assert GR.cost(2, "wattle")["materials"]["timber"] < GR.cost(2, "timber")["materials"]["timber"]
    up = GR.upgrade_cost("wattle", "timber")
    assert up == {"materials": {"timber": 4.0}, "units": 9.0}
    assert up["materials"]["timber"] == GR.cost(0, "timber")["materials"]["timber"] - GR.cost(0, "wattle")["materials"]["timber"]
    foot = GR.cost(1, "timber", foot=True)
    assert foot["materials"] == {"timber": 10, "stone": 10} and foot["units"] == 40


def _work_until_done(w, who, act, most=40):
    from cybertron2.engine import run as R
    for i in range(most):
        w.s["today"] = R.blank_today()
        r = do(w, who[i % len(who)], act)
        if r.startswith("You finished") or "now" in r and "section" in r:
            return r
        assert "units of work left" in r or r.startswith("You began") or "began" in r, r
    raise AssertionError("not finished")


def test_a_weir_built_in_timber_and_a_wattle_section_upgraded_for_the_difference(river):
    w = fresh(river)
    node = "Saltwell"
    a, c = adults(w, node)[:2]
    hands = w.s["containers"][Here(w, a).hands]["goods"]
    hands["timber"] = 60
    pid = water(w, node)
    r = do(w, a, {"do": "build", "what": "weir", "at": w.s["parcels"][pid]["name"], "with": c, "structure": "timber"})
    assert not r.startswith("Refused"), r
    assert hands["timber"] == pytest.approx(60 - 16)                                   # the first section in timber: 6 + 10
    bid = next(x for x, b in w.s["buildings"].items() if WL.is_weir(b) and b["parcel"] == pid)
    b = w.s["buildings"][bid]
    assert MONUMENTS["weir"]["units"] < b["unfinished"]["units_left"] <= 33.0          # 33 units, less the first action's work
    b["unfinished"] = None
    assert WL.sections(b)[0]["m"] == "timber" and WL.weir_share(b) == pytest.approx(0.30)
    r = _work_until_done(w, (a, c), {"do": "build", "what": "wattle section", "at": b["name"]})
    assert hands["timber"] == pytest.approx(44 - 6)                                    # an added wattle section: 6 timber
    assert [sc["m"] for sc in WL.sections(w.s["buildings"][bid])] == ["timber", "wattle"]
    w.s["buildings"][bid]["sections"][1]["level"] = 3
    r = _work_until_done(w, (a, c), {"do": "build", "what": "section upgrade", "at": b["name"]})
    assert hands["timber"] == pytest.approx(38 - 4)                                    # the difference: 10 - 6
    secs = WL.sections(w.s["buildings"][bid])
    assert [sc["m"] for sc in secs] == ["timber", "timber"] and secs[1]["level"] == 3   # rebuilt in timber, its wear kept
    refused(w, a, {"do": "build", "what": "section upgrade", "at": b["name"]}, "timber already")
    w.s["buildings"][bid]["sections"] += [{"m": "timber", "foot": False, "level": 5}] * 2
    refused(w, a, {"do": "build", "what": "weir section", "at": b["name"]}, "all its sections")


def test_the_upgrade_verb_rebuilds_a_weirs_wattle_section_in_timber(river):
    w = fresh(river)
    bid = put_weir(w, "Saltwell")
    b = w.s["buildings"][bid]
    a, c = b["crew"]
    w.s["containers"][Here(w, a).hands]["goods"]["timber"] = 10
    _work_until_done(w, (a, c), {"do": "build", "what": "upgrade", "at": b["name"], "to": "timber"})
    assert WL.sections(w.s["buildings"][bid])[0]["m"] == "timber"
    assert w.s["containers"][Here(w, a).hands]["goods"]["timber"] == pytest.approx(6)


# ---------------------------------------------------------------------- 2. gear sharing a run
def _p(n, k="eel", d="down"):
    return {"k": k, "g": "v:X", "d": 0, "n": float(n), "dir": d}


def _g(gid, parcel, pos, share, room=None, dirs=("down", "up")):
    return {"id": gid, "parcel": parcel, "pos": pos, "share": share, "dirs": dirs, "room": room, "worth": {"eel": 0.58, "salmon": 3.06}}


def test_gear_in_one_parcel_shares_the_run_in_proportion_not_first_come():
    for order in (0, 1):
        ps = [_p(300)]
        gear = [_g("weir", "P", 1, 0.30, room=100.0), _g("trap", "P", 1, {"eel": 17 / 300})]
        got = GR.share_run(ps, gear if order == 0 else gear[::-1])
        assert got == {"trap": {"eel": 17}, "weir": {"eel": 90}}                       # each its share of the run as it passed
        assert ps[0]["n"] == pytest.approx(300 - 107)
    ps = [_p(100)]                                                                      # shares past the whole run: scaled together
    got = GR.share_run(ps, [_g("a", "P", 1, 0.8), _g("b", "P", 1, 0.4)])
    assert got["a"]["eel"] == pytest.approx(67, abs=1) and got["b"]["eel"] == pytest.approx(33, abs=1)
    assert sum(x["eel"] for x in got.values()) <= 100


def test_a_full_hold_cuts_only_its_own_gear():
    ps = [_p(800)]                                                                      # 30% is 240 eels, 139 kg: more than it holds
    got = GR.share_run(ps, [_g("weir", "P", 1, 0.30, room=100.0), _g("trap", "P", 1, {"eel": 17 / 800})])
    assert got["weir"]["eel"] * 0.58 <= 100.0 + 1e-9 and got["weir"]["eel"] * 0.58 > 100.0 - 0.58
    assert got["trap"]["eel"] == 17


def test_between_parcels_a_run_down_meets_the_upstream_gear_first_and_a_run_up_the_downstream():
    gear = [_g("up", "U", 3, 0.30), _g("down", "D", 1, 0.30)]
    got = GR.share_run([_p(20)], gear)
    assert got["up"]["eel"] == 6 and got["down"]["eel"] == 4                           # 30% of 20, then of the 14 let through
    got = GR.share_run([_p(20, "salmon", "up")], gear)
    assert got["down"]["salmon"] == 6 and got["up"]["salmon"] == 4                     # the salmon meet the lower weir first
    got = GR.share_run([_p(20), _p(20, "salmon", "up")], [_g("up", "U", 3, 0.30), _g("down", "D", 1, 0.30, dirs=("down",))])
    assert got["down"] == {"eel": 4} and got["up"] == {"eel": 6, "salmon": 6}         # the race's way: a run going down only


def test_on_the_river_a_trap_beside_the_weir_does_not_take_before_it(river, monkeypatch):
    """The weir takes its 30% of the run that passes its parcel whether or not traps are set there; before 20 Nov the traps took
    first and the weir its share of what they left."""
    no_new_runs(monkeypatch)
    took = {}
    for traps in (False, True):
        w = fresh(river)
        no_robbers(w)
        bid = put_weir(w, "Saltwell")
        if traps:
            for who in adults(w, "Saltwell")[:3]:
                for _ in range(3):
                    do(w, who, {"do": "gather", "what": "trap in water", "at": w.s["parcels"][w.s["buildings"][bid]["parcel"]]["name"]})
        pulse(w, "Saltwell", n=200.0)
        rec = N.night(w)
        runs = rec["wild"]["runs"]
        took[traps] = (runs["weir"][bid]["eel"], sum(x.get("eel", 0) for x in (runs.get("trap") or {}).values()))
    assert took[False][0] == 60 and took[True][0] == 60
    assert took[True][1] > 0                                                            # the traps had their share of the same run


# ---------------------------------------------------------------------- 3. a year's upkeep in D2-210's band
def _emin(lam, cap=5):
    """E[min(Poisson(lam), cap)]: a night's levels lost, at most `cap` (wild._weir_wear)."""
    p, s, tail = math.exp(-lam), 0.0, 1.0
    for k in range(cap):
        tail -= p
        s += tail
        p *= lam / (k + 1)
    return s


@pytest.fixture(scope="module")
def runs_world():
    return __import__("cybertron2.engine.world", fromlist=["World"]).World(yaml.safe_load(open(RUNS_HIGH)))


def test_a_full_weirs_yearly_upkeep_on_the_runs_world_is_in_d2_210s_band(runs_world):
    """D2-210: a full weir costs a quarter to a third of its building a year to keep (wattle about 40 to 50%, timber 20 to 25%,
    stone-footed 5 to 10%), on Eelmouth's large river and its own weather, frost and floods, the gap kept right (open in high water);
    with it shut in high water the year costs clearly more."""
    w = copy.deepcopy(runs_world)
    m = WL.model(w)
    nt = RU.net(m)
    E = WW["wear"]
    nodes = sorted(set(m.nodes))
    Y, yrs = w.year_days(), 6
    wx = [WL.weather(w, nodes, d) for d in range(0, yrs * Y + 1)]
    pid = WL.weirs(w, "Eelmouth")[0][1]["parcel"]
    kind = WL.water_kind(w, m, pid)
    assert kind == "large"

    def year(mat, shut_high):
        tot = 0.0
        for d in range(1, yrs * Y + 1):
            fl = RU.flow(nt, "v:Eelmouth", {nd: [wx[d][nd]["rain"], wx[d - 1][nd]["rain"]] for nd in nodes}, E["flow_at"])
            ice = E["ice"] if w.cold("Eelmouth", d) else (E["thaw"] if w.cold("Eelmouth", d - 1) and d >= 2 and w.cold("Eelmouth", d - 2) else 1.0)
            high = fl in ("high", "spate", "flood")
            tot += _emin(E["base"] * E["water"][kind] * E["flow"][fl] * ice * mat * (E["gap_high"] if high and shut_high else 1.0))
        return tot / yrs * WW["mend"]

    wattle, timber, foot = year(1.0, False), year(0.5, False), year(0.1, False)
    assert 0.40 <= wattle <= 0.55 and 0.20 <= timber <= 0.28 and foot <= 0.10, (wattle, timber, foot)
    c1, c2 = GR.cost(0, "wattle")["units"], GR.cost(1, "timber")["units"]
    full = (wattle * c1 + 3 * timber * c2) / (c1 + 3 * c2)
    assert 0.25 <= full <= 0.34, full
    shut = (year(1.0, True) * c1 + 3 * year(0.5, True) * c2) / (c1 + 3 * c2)
    assert shut > 1.4 * full, (shut, full)
