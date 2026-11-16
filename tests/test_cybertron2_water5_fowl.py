"""Brief 5 §4 (proposals/river_and_water.md, D2-209): the wildfowl pushed by cold onto open water, the beaver's dam and the heronry's
take, on 37.2's lake world (cybertron2/specs/water/lake.yaml: Meresby, its brook and the mere in its ring), with the frost, the sites
and the stocks set by hand where a test needs them; and the generated fixture (no water at s1) for worlds the push leaves as before."""
import copy

import pytest
import yaml

from cybertron2.engine import night as N, run as R, signs as SG, wild as WL
from cybertron2.engine.data import TECHNIQUES
from cybertron2.engine.world import World
from cybertron2.wild.kinds import OPEN_WATER, PUSHED, SITES
from tests.test_cybertron2_wild import _do, build, generated  # noqa: F401

NODE = "Meresby"
WINTER = 14                                                     # the lake world starts on summer's 4th day of 8: day 14 is winter


@pytest.fixture(scope="module")
def lake():
    return yaml.safe_load(open("cybertron2/specs/water/lake.yaml"))


def _world(lake, netters=0, skill=5.0, keep=1):
    s = copy.deepcopy(lake)
    hh = next(a["household"] for a in s["agents"].values())
    s["agents"] = dict(list(sorted(s["agents"].items()))[:keep])
    s["agents"].update({f"N{i}": {"household": hh, "stage": "adult", "sex": "m", "at": NODE,
                                  "knows": {"net": {"level": "known", "skill": skill}}} for i in range(netters)})
    return World(s)


def _places(w):
    """The places a test needs, found in the world: the village's fish water, a wood off the water, a lodge's parcel beside the
    water (of the lodge's covers) and the meadow and pasture its dam would flood."""
    P = w.s["parcels"]
    ours = sorted(pid for pid, p in P.items() if p["node"] == NODE)
    brook = next(pid for pid in ours if P[pid]["cover"] == "water" and "fish" in P[pid]["res"])
    wood = next(pid for pid in ours if P[pid]["cover"] == "forest" and WL.at_water(w, pid) is None)
    grassy = lambda q: P[q]["cover"] in SITES["lodge"]["dam"]["floods"]["covers"] and "grass" in P[q]["res"]
    lodge = next(q for q in sorted(P[brook]["adj"]) if q in ours and P[q]["cover"] in SITES["lodge"]["where"]["covers"]
                 and any(grassy(x) for x in [q] + list(P[q]["adj"])))
    flooded = sorted(x for x in [lodge] + list(P[lodge]["adj"]) if x in P and grassy(x))
    return {"brook": brook, "wood": wood, "lodge": lodge, "flooded": flooded, "name": P[brook]["name"]}


def _no_frost(monkeypatch):
    """The real weather pinned mild: no hard night anywhere (no hard winter, no great freeze)."""
    monkeypatch.setattr(WL, "_frozen_day", lambda w, node, d: False)


def _frost(monkeypatch, day, n):
    """The last n days up to `day` frozen hard at every node, and no others."""
    monkeypatch.setattr(WL, "_frozen_day", lambda w, node, d: day - n < d <= day)


def _areas(w):
    m = WL.model(w)
    land = w.s["wild"]["land"]
    hi = WL._home_i(w, m, NODE)
    ri = next(i for i, a in enumerate(m.ids) if land["areas"][a].get("node") == NODE and land["areas"][a]["kind"] == "ring")
    return m, hi, ri


def _fowl(w, density=60.0):
    m = WL.model(w)
    for i, a in enumerate(m.ids):
        if w.s["wild"]["land"]["areas"][a].get("node") == NODE:
            w.s["wild"]["state"]["pop"]["wildfowl"][i] = density


# ---------------------------------------------------------------------------------------------------------- the fowl and the freeze
def test_the_lake_world_holds_small_water_at_home_and_the_mere_in_its_ring(lake):
    w = _world(lake)
    m, hi, ri = _areas(w)
    home, ring = WL._water_parts(m, hi), WL._water_parts(m, ri)
    assert home["small"] > 0 and home["lake"] == home["big river"] == 0
    assert ring["lake"] > 0 and ring["small"] > 0
    pl = _places(w)
    assert WL.at_water(w, pl["brook"]) == "water" and WL.at_water(w, pl["wood"]) is None


def test_frost_freezes_the_small_waters_first_and_the_lake_last(lake, monkeypatch):
    w = _world(lake)
    w.s["day"] = WINTER
    m, hi, ri = _areas(w)
    h = OPEN_WATER["hold"]
    most = PUSHED["wildfowl"]["most"]
    got = {}
    for n in range(0, h["lake"] + 2):
        _frost(monkeypatch, WINTER, n)
        got[n] = (WL.open_water(w, m, hi, NODE, kind="wildfowl"), WL.open_water(w, m, ri, NODE, kind="wildfowl"))
    assert got[0] == (1.0, 1.0)                                                     # no frost: as before
    assert 1.0 < got[1][0] <= most and 1.0 < got[1][1] <= most                     # the first hard night: crowded on the water
    for n in range(h["small"] + 1, h["lake"] + 1):
        assert got[n][0] == 0.0 and 1.0 < got[n][1] <= most                        # the brook frozen over; the mere still open
    assert got[h["lake"] + 1] == (0.0, 0.0)                                         # a long freeze: all of it frozen over


def test_only_a_pushed_kind_at_the_water_is_crowded(lake, monkeypatch):
    w = _world(lake)
    w.s["day"] = WINTER
    m, hi, ri = _areas(w)
    _frost(monkeypatch, WINTER, 1)
    pl = _places(w)
    assert WL.pushed(w, m, NODE, pl["brook"], "wildfowl", hi) > 1.0
    assert WL.pushed(w, m, NODE, pl["wood"], "wildfowl", hi) == 1.0                 # off the water: as before
    assert WL.pushed(w, m, NODE, pl["brook"], "eel", hi) == 1.0                     # not a kind the cold pushes


def test_worlds_without_water_are_as_before(generated, monkeypatch):  # noqa: F811
    w = build(generated, history=1)
    m = WL.model(w)
    land = w.s["wild"]["land"]
    dry = [i for i, a in enumerate(m.ids) if land["areas"][a].get("node") == "s1" and float(m.f["water"][i]) <= 1e-9]
    assert dry
    for n in (1, 3, 7):
        _frost(monkeypatch, w.d, n)
        assert all(WL.open_water(w, m, i, "s1", kind="wildfowl") == 1.0 for i in dry)
        assert all(WL.pushed(w, m, "s1", pid, "wildfowl", i) == 1.0 for i in dry for pid, p in w.s["parcels"].items() if p["node"] == "s1")
    assert not any(WL.at_water(w, pid) for pid, p in w.s["parcels"].items() if p["node"] == "s1")


def _nets(lake, monkeypatch, n, rng_word=None, netters=20):
    """Meat taken by 20 practised fowlers netting at the brook on a winter day after n hard nights."""
    w = _world(lake, netters=netters)
    w.s["day"] = WINTER
    _fowl(w)
    _frost(monkeypatch, WINTER, n)
    meat, lines = 0.0, []
    at = _places(w)["name"]
    for i in range(netters):
        w.s["today"] = R.blank_today()
        lines.append(_do(w, f"N{i}", {"do": "gather", "what": "net", "at": at, **({"range": rng_word} if rng_word else {})}))
        meat += w.goods(w.s["people"][f"N{i}"]["hands"]).get("meat", 0.0)
    return meat, lines


def test_a_freeze_crowds_the_open_water_and_makes_nets_pay(lake, monkeypatch):
    thaw, _ = _nets(lake, monkeypatch, 0)
    frost, lines = _nets(lake, monkeypatch, 1)
    assert frost > 1.5 * thaw > 0, (thaw, frost)
    shut, lines = _nets(lake, monkeypatch, OPEN_WATER["hold"]["small"] + 1)          # the brook frozen over: no fowl on it
    assert not any("wildfowl" in r for r in lines)
    mere0, _ = _nets(lake, monkeypatch, 0, "the wood around")
    mere, _ = _nets(lake, monkeypatch, OPEN_WATER["hold"]["small"] + 1, "the wood around")   # out to the mere, still open
    assert mere > 1.5 * mere0 > 0, (mere0, mere)


def test_a_long_freeze_empties_the_water_and_the_survivors_return(lake, monkeypatch):
    def winter(n_frost):
        w = _world(lake, keep=0)
        w.s["day"] = WINTER - 8
        _fowl(w)
        days = set(range(WINTER - 8, WINTER - 8 + n_frost))
        monkeypatch.setattr(WL, "_frozen_day", lambda w_, node, d: d in days)
        m, hi, ri = _areas(w)
        for _ in range(8):
            N.night(w)
            w.s["day"] += 1
        w.s["day"] -= 1                                                              # the last frozen day
        empty = WL.open_water(w, m, ri, NODE, kind="wildfowl")
        w.s["day"] += 1
        return w, m, ri, empty
    cold, m, ri, empty = winter(8)
    mild, _, _, _ = winter(0)
    assert empty == 0.0                                                              # the mere frozen over: none on the water
    left = float(cold.s["wild"]["state"]["pop"]["wildfowl"][ri])
    assert 0 < left < 0.7 * float(mild.s["wild"]["state"]["pop"]["wildfowl"][ri])     # the great freeze took many
    assert WL.open_water(cold, m, ri, NODE, kind="wildfowl") == 1.0                  # the thaw: the survivors back on the water


def test_the_push_shows_at_the_water_the_day_it_begins(lake, monkeypatch):
    w = _world(lake)
    who = next(iter(w.s["people"]))
    _fowl(w)
    from cybertron2.engine.here import Here

    def seen(n):
        w.s["day"] = WINTER
        _frost(monkeypatch, WINTER, n)
        out = []
        SG._wild_when(Here(w, who), lambda about, text, *a, **k: out.append((text, k["spot"]["parcel"])))
        return out
    pl = _places(w)
    crowd = seen(1)
    assert any(f"packed thick on the open water at {pl['name']}" in t and pid == pl["brook"] for t, pid in crowd)
    assert any("nets at the water's edge" in t for t, _ in crowd)
    froze = seen(OPEN_WATER["hold"]["small"] + 1)
    assert any(f"the water at {pl['name']} frozen over" in t for t, _ in froze)
    assert not any("packed thick" in t for t, _ in froze)


# ---------------------------------------------------------------------------------------------------------- the beaver's dam
def _site(w, kind, pid, size):
    sid = f"{kind}@{pid}"
    w.s["wild"].setdefault("sites", {})[sid] = {"kind": kind, "node": NODE, "parcel": pid, "size": float(size), "last": None, "gone": None,
                                                "back": None, "dam": False, "k0": {}}
    return sid


def test_the_dam_cuts_the_meadows_hay_and_raises_the_fish_and_breaking_it_reverses_both(lake, monkeypatch):
    _no_frost(monkeypatch)
    w = _world(lake)
    pl = _places(w)
    BROOK, LODGE, LEAZE = pl["brook"], pl["lodge"], pl["flooded"][0]
    sid = _site(w, "lodge", LODGE, 3)
    hay0, fish0 = (dict(w.s["parcels"][LEAZE]["res"]["grass"]), dict(w.s["parcels"][BROOK]["res"]["fish"]))
    WL._dam(w, sid, w.s["wild"]["sites"][sid], True, direct=True)
    d = SITES["lodge"]["dam"]
    assert TECHNIQUES["hay"]["draws"] == "grass"                                     # hay is cut from the grass the flood drowns
    g, f = w.s["parcels"][LEAZE]["res"]["grass"], w.s["parcels"][BROOK]["res"]["fish"]
    assert abs(g["K"] - hay0["K"] * d["floods"]["K"]) < 1e-6 and g["S"] <= g["K"]
    assert abs(f["K"] - fish0["K"] * d["fish"]) < 1e-6
    out = []
    from cybertron2.engine.here import Here
    SG._wild_sites(Here(w, next(iter(w.s["people"]))), lambda about, text, *a, **k: out.append((text, k["spot"]["parcel"])))
    assert any("lies drowned behind the beavers' dam" in t and pid in pl["flooded"] for t, pid in out)
    assert any("backed up the water" in t and pid == BROOK for t, pid in out)
    for _ in range(6):                                                               # the pond fills with fish
        N.night(w)
        w.s["day"] += 1
    assert w.s["parcels"][BROOK]["res"]["fish"]["S"] > fish0["K"] * 1.1
    w.s["today"] = R.blank_today()
    who = next(iter(w.s["people"]))
    w.s["know"].setdefault(who, {})["break a dam"] = {"level": "known", "skill": 1.0}     # a village with a lodge knows it (methods)
    r = _do(w, who, {"do": "work", "what": "break a dam", "at": w.s["parcels"][LODGE]["name"]})
    assert "broke open" in r, r
    g, f = w.s["parcels"][LEAZE]["res"]["grass"], w.s["parcels"][BROOK]["res"]["fish"]
    assert abs(g["K"] - hay0["K"]) < 1e-6 and abs(f["K"] - fish0["K"]) < 1e-6 and f["S"] <= fish0["K"] + 1e-6
    for _ in range(w.season_len - 1):                                                # down for a season
        N.night(w)
        w.s["day"] += 1
        assert not w.s["wild"]["sites"][sid]["dam"]
        assert abs(w.s["parcels"][LEAZE]["res"]["grass"]["K"] - hay0["K"]) < 1e-6


# ---------------------------------------------------------------------------------------------------------- the heronry
def _herons(lake, nests, fish_k=None, nights=8):
    w = _world(lake, keep=0)
    pl = _places(w)
    BROOK = pl["brook"]
    _site(w, "heronry", pl["wood"], nests)
    if fish_k is not None:
        w.s["parcels"][BROOK]["res"]["fish"].update(K=float(fish_k), S=float(fish_k))
    for _ in range(nights):
        N.night(w)
        w.s["day"] += 1
    f = w.s["parcels"][BROOK]["res"]["fish"]
    return f["S"] / f["K"], w


def test_a_big_heronry_lowers_a_small_waters_fish(lake, monkeypatch):
    _no_frost(monkeypatch)
    small_big, _ = _herons(lake, 24)
    small_few, _ = _herons(lake, 2)
    big_big, _ = _herons(lake, 24, fish_k=160)
    assert small_big < 0.92 and small_few > 0.98 and big_big > 0.98, (small_big, small_few, big_big)


def test_the_heronry_follows_the_fish(lake, monkeypatch):
    _no_frost(monkeypatch)                                                           # a mild winter before: no crash

    def spring(fish_k):
        w = _world(lake, keep=0)
        pl = _places(w)
        sid = _site(w, "heronry", pl["wood"], 20)
        w.s["parcels"][pl["brook"]]["res"]["fish"].update(K=float(fish_k), S=float(fish_k))
        w.s["day"] = next(d for d in range(1, 40) if w.calendar(d)["season"] == "spring" and w.calendar(d)["day"] == 1)
        WL._sites_night(w, WL.model(w), w.s["wild"]["state"])
        return w.s["wild"]["sites"][sid]
    few, many = spring(8), spring(200)
    assert few["size"] < 20 and few["why"] == "few"                                  # 8 fish keep 8 nests: it falls toward them
    assert many["size"] > 20 and many["why"] == "grew"
