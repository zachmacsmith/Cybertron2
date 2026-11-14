"""Groups that range (build brief 4c §7.2, proposals/hunt_calibration.md): a kind with `range_km2` on its group condenses its grown
heads over the range of its densest area, one group wherever it raids, and sets out for a village in its range; a kind without it
keeps the rule it had. The year's young are left out of a ranging group's count until the next births (§7.1). The generator's
report names the predators within range of each village (§7.3)."""
import copy
import hashlib
import json
import math

import numpy as np
import pytest

from cybertron2.engine import farm as FM, night as N, wild as WL
from cybertron2.engine.world import World
from cybertron2.landgen import write as W
from cybertron2.wild import ecology as EC, kinds as WK


@pytest.fixture(scope="module")
def generated():
    world, cells, report = W.generate({"name": "t", "seed": 7, "days": 10, "calendar": {"season": "summer", "day": 4, "season_days": 8},
                                       "generate": {"seed": 7, "configuration": "settled lowland and frontier", "spacing_km": 8.0,
                                                    "settlements": 4}})
    world.setdefault("agents", {})
    return world


def build(world, history=2):
    s = copy.deepcopy(world)
    s["packs"], s["climate"] = ["wild"], {"era": "steady"}
    s.setdefault("wild", {})["history_years"] = history
    return World(s)


def _held_pack(monkeypatch, w, kind, where, heads):
    """`heads` grown beasts of a kind in one area and none elsewhere, hungry, held there night after night (the ecology's own
    dynamics are §7.1's; this is the group's rule alone)."""
    m = WL.model(w)
    i = m.ids.index(where)
    pop = [0.0] * m.n
    pop[i] = heads / float(m.km2[i])
    step = EC.step

    def held(m_, st, *a, **k):
        eff = step(m_, st, *a, **k)
        st["pop"][kind] = list(pop)
        st["cond"][kind] = [0.0] * m_.n
        st.setdefault("yearling", {})[kind] = [0.0] * m_.n
        return eff
    monkeypatch.setattr(EC, "step", held)


def _areas(w):
    m, land = WL.model(w), w.s["wild"]["land"]
    home = {nd: land["areas"][a]["xy_km"] for nd, a in land["home"].items()}
    return m, land, home


def _nights(w, n=16):
    """The wolves' kills over n nights, and the parcels their traces were left on."""
    raids, traced = [], set()
    for _ in range(n):
        rec = N.night(w)
        raids += [(gid, r) for gid, r in ((rec.get("wild") or {}).get("groups") or {}).items() if gid.startswith("wolf") and r.get("killed")]
        traced |= {pid for pid, lst in (w.s["wild"].get("traces") or {}).items() if any(t.get("kind") == "wolf" for t in lst)}
        w.s["day"] += 1
    return raids, traced


def _s1_herds(w):
    return {h: FM.head(x) for h, x in w.s["herds"].items() if x.get("node") == "s1"}


def test_a_pack_next_to_a_village_with_it_in_range_raids_its_unwatched_herd(generated, monkeypatch):
    w = build(generated)
    m, land, home = _areas(w)
    R = math.sqrt(WL._range_km2(m, "wolf") / math.pi)
    near = [a for a in m.ids if land["areas"][a]["kind"] == "wild" and land["areas"][a]["node"] != "s1"
            and math.dist(land["areas"][a]["xy_km"], home["s1"]) < R - 1.0]           # beside the village, nearer another node
    assert near
    where = min(near, key=lambda a: math.dist(land["areas"][a]["xy_km"], home["s1"]))
    _held_pack(monkeypatch, w, "wolf", where, 6.0)
    before = _s1_herds(w)
    assert sum(before.values()) > 0
    raids, traced = _nights(w)
    after = _s1_herds(w)
    assert sum(after.values()) < sum(before.values())                                  # a beast of the unwatched herd taken
    assert raids and len({gid for gid, _ in raids}) == 1                               # one pack, wherever it raids
    gid = raids[0][0]
    g = w.s["wild"]["groups"][gid]
    assert g["range"] == where and "s1" in g["villages"]
    at = {w.s["parcels"][pid]["node"] for pid in traced}                               # its traces at the villages it came to
    assert "s1" in at and at <= set(g["villages"])
    assert WL.group_at(w, "wolf", "s1")[0] == gid                                      # the hunter's and the signs' lookup finds it


def test_a_pack_at_a_node_out_of_range_does_not_raid_the_village(generated, monkeypatch):
    w = build(generated)
    m, land, home = _areas(w)
    R = math.sqrt(WL._range_km2(m, "wolf") / math.pi)
    rings = [a for a in m.ids if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] != "s1"
             and math.dist(land["areas"][a]["xy_km"], home["s1"]) > R + 0.5]
    where = min(rings, key=lambda a: math.dist(land["areas"][a]["xy_km"], home["s1"]))   # the next node, just beyond the range
    _held_pack(monkeypatch, w, "wolf", where, 6.0)
    before = _s1_herds(w)
    raids, traced = _nights(w)
    assert sum(_s1_herds(w).values()) == sum(before.values()) and not any(w.s["parcels"][pid]["node"] == "s1" for pid in traced)
    packs = {gid: g for gid, g in w.s["wild"]["groups"].items() if g["kind"] == "wolf"}
    assert packs and all("s1" not in g["villages"] for g in packs.values())


def _scenario(monkeypatch):
    """A fixed-seed run of the committed probe world in summer: boar, wolves, a fox and deer held by a village with standing corn
    and herds, 12 nights."""
    from cybertron2.engine.world import load_spec
    s = copy.deepcopy(load_spec("cybertron2/specs/wild_probe6.json"))
    s["climate"], s["calendar"] = {"era": "steady"}, {"season": "summer", "day": 4, "season_days": 8}
    s.setdefault("wild", {})["history_years"] = 2
    w = World(s)
    m, st, land = WL.model(w), w.s["wild"]["state"], w.s["wild"]["land"]
    ri = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")
    held = {kind: (heads / m.km2[ri], cond) for kind, heads, cond in (("wild boar", 12.0, 0.2), ("wolf", 8.0, 0.0), ("fox", 4.0, 0.5),
                                                                      ("red deer", 15.0, 0.3))}
    step = EC.step

    def hold(m_, st_, *a, **k):
        eff = step(m_, st_, *a, **k)
        for kind, (d, c) in held.items():
            st_["pop"][kind][ri], st_["cond"][kind][ri] = d, c
        return eff
    monkeypatch.setattr(EC, "step", hold)
    for kind, (d, c) in held.items():
        st["pop"][kind][ri], st["cond"][kind][ri] = d, c
    for pid, par in sorted(w.s["parcels"].items()):
        if par["node"] == "s1" and par["cover"] == "field" and not FM.standing(par):
            par["crop"] = {"kind": "barley", "crop": "grain", "sown": -10, "ripe_day": 40, "window": 20, "seed": 1, "area": par["size"],
                           "area_left": par["size"], "broken": 0, "weeded": 0, "base": 10.0 * par["size"], "rot": 1.0, "left": 10.0 * par["size"]}
    log = []
    for _ in range(12):
        rec = N.night(w)
        log.append([w.d, sorted([g, v["n"], v["pos"], v.get("target")] for g, v in w.s["wild"]["groups"].items()),
                    (rec.get("wild") or {}).get("groups") or {}])
        w.s["day"] += 1
    log.append(sorted([h, FM.head(x)] for h, x in w.s["herds"].items()))
    log.append(round(sum(float(c.get("left", 0)) for p in w.s["parcels"].values() for _, _, c in FM.standing(p)), 3))
    return log


# the scenario's digest on the code before brief 4c (8158674, ecology-hunt3): 16 raids in 12 nights by boar, wolves (two cows, a calf,
# the dead), the fox, deer, stoats and the flock. Regenerate it on that commit if the ecology's data change (kinds.py, methods.py).
BEFORE_4C = "a8dada811634fe2f"


def test_kinds_without_a_range_keep_the_rule_they_had_exactly(monkeypatch):
    """With no kind ranging (and the wolves' territorial limit as it was), the same groups and raids on a fixed seed as before 4c:
    replays of older worlds stay identical."""
    for k, row in WK.KINDS.items():
        if "range_km2" in (row.get("group") or {}):
            monkeypatch.delitem(row["group"], "range_km2")
    monkeypatch.setitem(WK.KINDS["wolf"], "terr", 0.03)
    log = _scenario(monkeypatch)
    raids = [(g, r) for d in log[:12] for g, r in d[2].items() if isinstance(r, dict) and not r.get("turned")]
    assert len(raids) >= 10 and {g.split("@")[0] for g, _ in raids} >= {"wolf", "wild boar", "fox"}
    assert hashlib.sha256(json.dumps(log, sort_keys=True, default=str).encode()).hexdigest()[:16] == BEFORE_4C


def test_a_ranging_group_counts_its_grown_beasts_and_the_years_young_die_first(generated):
    w = build(generated)
    m, st = WL.model(w), copy.deepcopy(w.s["wild"]["state"])
    kind = next(k for k in m.names if WL._range_km2(m, k) > 0 and m.kinds[k]["count"] == "whole"
                and m.kinds[k].get("litters") != "through" and float(m.kinds[k]["b"]) >= 1.0)
    Y = w.year_days()
    nodes = sorted(set(m.nodes))
    heads = lambda s: float((np.asarray(s["pop"][kind]) * np.asarray(m.km2)).sum())
    k0 = Y * 3                                                                      # a spring's first day: the births
    grown0 = heads(st)
    EC.step(m, st, k0, WL.weather(w, nodes, k0), WL.draws(w, k0, "t"))
    born = float((np.asarray(st["yearling"][kind]) * np.asarray(m.km2)).sum())
    assert born > 0.2 * grown0 and heads(st) > grown0 + 0.5 * born
    assert abs(float(WL._adults(m, st, kind).sum()) - (heads(st) - born)) < 1e-6 * max(1.0, heads(st))
    assert float(WL._adults(m, st, kind).sum()) <= grown0 + 1e-6                     # the young left out of the group's count
    at_births = float(WL._adults(m, st, kind).sum())
    for d in range(1, 6):                                                           # the cull falls on the young first
        EC.step(m, st, k0 + d, WL.weather(w, nodes, k0 + d), WL.draws(w, k0 + d, "t"))
    young = float((np.asarray(st["yearling"][kind]) * np.asarray(m.km2)).sum())
    grown = float(WL._adults(m, st, kind).sum())
    assert young < born and grown >= 0.9 * at_births                                 # the grown hold while the young die
    i = int(np.argmax(m.km2))
    st["pop"][kind][i] = float(st["pop"][kind][i]) + 5.0 / float(m.km2[i])          # beasts that come in are grown
    assert abs(float(WL._adults(m, st, kind).sum()) - grown - 5.0) < 1e-6
    k1 = k0 + Y                                                                     # the next births: last year's young are grown
    before = heads(st)
    EC.step(m, st, k1, WL.weather(w, nodes, k1), WL.draws(w, k1, "t"))
    assert float(WL._adults(m, st, kind).sum()) <= before + 1e-6 and float(WL._adults(m, st, kind).sum()) > 0.8 * before


def test_the_generators_report_names_the_predators_within_range_of_each_village():
    world, cells, report = W.generate({"name": "t", "seed": 7, "days": 10, "packs": ["wild"],
                                       "generate": {"seed": 7, "configuration": "settled lowland and frontier", "spacing_km": 8.0,
                                                    "settlements": 2, "households": [2, 2]}}, people=True)
    chk = report["checks"]["predators within range"]
    assert chk["kind"] == "wild" and chk["ok"] and "predators within range" not in report["refused"]   # a check, not a refusal
    rows = chk["detail"]["by village"]
    assert rows and set(chk["detail"]["said"]) == set(rows)
    for row in rows.values():
        ranging = {k for k, x in row.items() if "range_km2" in x}
        assert ranging and all(row[k]["heads"] >= 0 and row[k]["least"] >= 1 for k in row)
        assert not any(all(t.get("what", "crop") in ("crop", "res") for t in WK.NEAR_PEOPLE[k]["targets"]) for k in row)   # predators
