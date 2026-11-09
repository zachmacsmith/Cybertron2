"""The wild layer (proposals/wild_layer.md; D2-199, the ecology branch): the land summary the generator writes, kinds as RESOURCES
rows, the ecology step in the night with the `wild` pack only, and the bridge to crops and stores. Without the pack the engine is
as it was."""
import ast
import copy
import math
import re

import numpy as np
import pytest

from cybertron2.engine import night as N, schema as SC
from cybertron2.engine.data import RESOURCES
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


def build(world, packs=("wild",), era="steady", history=2):
    s = copy.deepcopy(world)
    s["packs"] = list(packs)
    s["climate"] = {"era": era}
    s.setdefault("wild", {})["history_years"] = history
    return World(s)


def test_no_kind_is_named_in_the_rule_code():
    """One registry, rules written once (wild_layer.md §3.2): the step, the engine's side and the land summary name no kind."""
    words = {w for name in WK.KINDS for w in re.findall(r"[a-z]+", name) if len(w) > 3 and w not in ("wild", "mice", "brown")}
    for path in ("cybertron2/wild/ecology.py", "cybertron2/engine/wild.py", "cybertron2/wild/areas.py"):
        tree = ast.parse(open(path).read())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                    and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
        code = ast.unparse(tree).lower()
        hits = [w for w in sorted(words) if re.search(r"\b" + w + r"s?\b", code)]
        assert not hits, (path, hits)


def test_kinds_are_resource_rows_in_the_wild_pack():
    for name in WK.KINDS:
        row = RESOURCES[name]
        assert row["pack"] == "wild" and row["renewal"] == "population" and row["population"]["mass"] > 0


def test_the_generator_writes_the_land_summary(generated):
    land = generated["wild"]["land"]
    kinds = {a["kind"] for a in land["areas"].values()}
    assert kinds == {"home", "ring", "wild"}
    for node, aid in land["home"].items():                                     # every node's parcels are its home area's windows
        assert set(land["areas"][aid]["parcels"]) == set(generated["nodes"][node]["parcels"])
    assert land["links"] and all(e > 0 for _, _, e in land["links"])
    ids = set(land["areas"])
    assert all(a in ids and b in ids for a, b, _ in land["links"])
    assert all(t == "out" or t in ids for t in land["down"].values())


def test_without_the_pack_the_world_is_as_it_was(generated):
    w = build(generated, packs=())
    assert "wild" not in w.s
    assert not any("ecosystem" in p for p in w.s["parcels"].values())
    assert "red deer" not in next(iter(w.s["parcels"].values()))["res"]
    rec = N.night(w)
    assert "wild" not in rec


def test_with_the_pack_the_ecology_runs_each_night_and_replays(generated):
    a, b = build(generated), build(generated)
    assert a.s["wild"]["state"]["pop"]["wild boar"] == b.s["wild"]["state"]["pop"]["wild boar"]
    for _ in range(4):
        N.night(a); a.s["day"] += 1
        N.night(b); b.s["day"] += 1
    assert a.s["wild"]["state"] == b.s["wild"]["state"]                       # keyed draws only: the same world runs the same
    st = a.s["wild"]["state"]
    for k, v in st["pop"].items():
        assert all(math.isfinite(x) and x >= 0 for x in v), k
    assert not SC.unknown(a.s)                                                 # the shape is declared (D4-100)
    assert any(p.get("ecosystem") for p in a.s["parcels"].values())


def test_wild_kinds_eat_from_the_crops_in_a_home_area(generated):
    w = build(generated)
    m = __import__("cybertron2.engine.wild", fromlist=["model"]).model(w)
    st = w.s["wild"]["state"]
    home = [i for i in range(m.n) if m.home[i]]
    st["pop"]["brown hare"] = [x * (40.0 if i in home else 1.0) for i, x in enumerate(st["pop"]["brown hare"])]
    st["pulse"]["crops"] = [max(x, 500.0) if i in home else x for i, x in enumerate(st["pulse"]["crops"])]
    lost = 0.0
    for _ in range(3):
        rec = N.night(w); w.s["day"] += 1
        lost += sum((rec.get("wild") or {}).get("crops", {}).values())
    assert lost > 0


def test_movement_keeps_the_count():
    """Shifting along the links moves animals between areas; it does not make or lose any."""
    land = {"km": 0.15, "areas": {}, "links": [["a0", "a1", 2.0], ["a1", "a2", 1.0]], "down": {}, "home": {}}
    for i, wood in enumerate((0.9, 0.2, 0.6)):
        land["areas"][f"a{i}"] = {"kind": "wild", "node": "n", "parcels": [], "km2": 10.0, "cover": {"forest": 10 * wood, "pasture": 10 * (1 - wood)},
                                  "eco": {"oak-ash wood": 10 * wood}, "old_wood_km2": 0.0, "wood_edge_km2": 0.0, "wet": 0.3,
                                  "elevation": 60.0, "temp": 9.0, "texture": {"loam": 1.0}, "rock": 0.0, "river_km": 0.0,
                                  "big_river_km": 0.0, "lake_km2": 0.0}
    kinds = {"roe deer": dict(WK.KINDS["roe deer"], b=0.0, m=0.0, people=0.0)}
    m = EC.Model(land, kinds=kinds, knobs={"disease": 0.0})
    st = m.initial()
    st["pop"]["roe deer"] = [5.0, 0.0, 0.0]
    before = sum(np.asarray(st["pop"]["roe deer"]) * m.km2)
    wx = {"n": {"temp": 12.0, "low": 6.0, "rain": 2.0, "snow": False}}
    for d in range(1, 4):                                                       # spring days 1-3: no breeding day, no deaths
        EC.step(m, st, d, wx, {"mast": 0.5})
    after = np.asarray(st["pop"]["roe deer"]) * m.km2
    imm = 3 * 0.002 / m.S * m.suit["roe deer"] * 15.0 * 10.0                  # the thin immigration from beyond
    assert abs(after.sum() - before - imm.sum()) < 0.01 * before
    assert after[1] > 0 or after[2] > 0


def _summer_world(generated, kind="wild boar"):
    """A wooded village in summer with a group of the kind near it and a standing crop on its fields."""
    w = build(generated, history=2)
    from cybertron2.engine import wild as WL
    m = WL.model(w)
    st = w.s["wild"]["state"]
    land = w.s["wild"]["land"]
    ring = next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == "s1")
    st["pop"][kind][ring] = 2.0 * 20.0 / m.km2[ring] * 3
    st["cond"][kind][ring] = 0.2                                                     # hungry
    from cybertron2.engine import farm as FM
    for pid, par in w.s["parcels"].items():
        if par["node"] == "s1" and par["cover"] == "field" and not FM.standing(par):
            par["crop"] = {"kind": "barley", "crop": "grain", "sown": -10, "ripe_day": 40, "window": 20, "seed": 1, "area": par["size"],
                           "area_left": par["size"], "broken": 0, "weeded": 0, "base": 10.0 * par["size"], "rot": 1.0, "left": 10.0 * par["size"]}
    return w, WL


def test_a_group_condenses_near_a_wooded_village_sets_out_leaves_traces_and_raids(generated):
    w, WL = _summer_world(generated)
    raids, edges = 0, 0
    for _ in range(12):
        rec = N.night(w); w.s["day"] += 1
        g = (rec.get("wild") or {}).get("groups", {})
        raids += sum(1 for v in g.values() if not v.get("turned"))
        edges += sum(1 for lst in (w.s["wild"].get("traces") or {}).values() for t in lst if t["what"] == "edge")
    assert "wild boar@s1" in w.s["wild"]["groups"]
    assert raids >= 1 and edges >= 1


def test_the_same_scare_wears_off_on_a_kind_that_gets_used_to_it(generated):
    """D2-198: boar get used to a harmless scare: night after night the same fire turns them less."""
    w, WL = _summer_world(generated)
    g = {"kind": "wild boar", "node": "s1", "pos": "home", "t": -1, "raid": -1, "found": -99, "habit": {}, "wary": -1, "rest": -1,
         "pref": None, "target": None}
    turned = []
    fields = WL._fields(w, "s1")
    for k in range(10):
        st = w.s["wild"]
        st.setdefault("groups", {})["wild boar@s1"] = dict(st.get("groups", {}).get("wild boar@s1") or g, pos="ready", raid=w.d, target=fields[0],
                                                           pref=fields[0], rest=-1, wary=-1)
        st.setdefault("watch", {})[fields[0]] = {"day": w.d, "by": "x", "scare": "fire"}
        rec = N.night(w); w.s["day"] += 1
        v = (rec.get("wild") or {}).get("groups", {}).get("wild boar@s1")
        if v:
            turned.append(bool(v.get("turned")))
    habit = w.s["wild"]["groups"]["wild boar@s1"]["habit"].get("fire", 0.0)
    assert habit > 0.5 and turned and sum(turned[:4]) >= sum(turned[-4:])


def test_a_trace_reads_one_way_to_a_practised_hunter_and_another_to_anyone_else(generated):
    """wild_layer.md §3.6: the same rooting is 'the turf turned over' to one who has not hunted, and 'fresh rooting: a sounder of
    about n' to one who has (the senses' knows/lay rows)."""
    from cybertron2.engine import here as HR, perceive as PC, run as R, signs as SG
    world = copy.deepcopy(generated)
    world["agents"] = {"Ann": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1", "knows": {"hunt": {"level": "known", "skill": 1.6}}},
                       "Tom": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}}}
    w, WL = _summer_world(world)
    edge = WL._edge_of(w, WL._fields(w, "s1")[0])
    w.apply("set_wild", "s1", path=["traces"], value={edge: [{"kind": "wild boar", "what": "edge", "day": w.d, "n": 9}]})
    w.s["day"] += 1
    w.s["today"] = R.blank_today()
    read = {}
    for who in ("Ann", "Tom"):
        pr = PC.practised(HR.Mind(w, who))
        read[who] = [f["text"] for f in PC.facts(HR.Here(w, who)) if (f.get("knows") or f.get("lay")) == "hunt" and SG.readable(f, pr)]
    assert any("sounder of about 9" in t for t in read["Ann"]) and not any("turf" in t for t in read["Ann"])
    assert any("turf" in t for t in read["Tom"]) and not any("sounder" in t for t in read["Tom"])


def _hunters(generated, n=30, knows=("hunt the wild", "boar hunt", "stalk deer")):
    world = copy.deepcopy(generated)
    world["agents"] = {f"H{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1",
                                 "knows": {t: {"level": "known", "skill": 1.4} for t in knows}} for i in range(n)}
    w, WL = _summer_world(world)
    from cybertron2.engine import run as R
    w.s["today"] = R.blank_today()
    wood = next(p["name"] for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] == "forest")
    return w, WL, wood


def _do(w, who, a):
    from cybertron2.engine import verbs as V
    from cybertron2.engine.here import Here, Mind
    from cybertron2.engine.world import Refused
    try:
        return V.do(Here(w, who), Mind(w, who), a)
    except Refused as e:
        return f"REFUSED {e}"


def test_a_kill_comes_off_the_population_and_gives_its_goods(generated):
    w, WL, wood = _hunters(generated)
    before = sum(np.asarray(w.s["wild"]["state"]["pop"]["roe deer"]) * WL.model(w).km2)
    took = [r for i in range(30) for r in [_do(w, f"H{i}", {"do": "gather", "what": "stalk deer", "at": wood, "range": "the wood around",
                                                              "looking for": "roe deer"})] if "took it" in r]
    after = sum(np.asarray(w.s["wild"]["state"]["pop"]["roe deer"]) * WL.model(w).km2)
    roe = sum(1 for r in took if "came on a roe deer" in r)                    # (not "instead of the roe deer you were after")
    assert roe >= 1 and abs((before - after) - roe) < 1e-6
    assert any(w.goods(w.s["people"][f"H{i}"]["hands"]).get("meat", 0) > 0 for i in range(30))


def test_looking_for_something_makes_it_likelier_but_not_certain(generated):
    """A hunter who names a quarry meets it more often than one taking what comes, and sometimes meets something else."""
    w, WL, wood = _hunters(generated, n=60)
    met = lambda r, k: f"came on a {k}" in r or f"came on an {k}" in r
    general = [_do(w, f"H{i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around"}) for i in range(30)]
    aimed = [_do(w, f"H{i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around", "looking for": "boar"})
             for i in range(30, 60)]
    g_boar = sum(met(r, "wild boar") for r in general) / max(1, sum("came on" in r for r in general))
    a_boar = sum(met(r, "wild boar") for r in aimed) / max(1, sum("came on" in r for r in aimed))
    assert a_boar > g_boar
    assert any("instead of the boar" in r for r in aimed) or a_boar < 1.0


def test_boar_hunted_alone_hurt_more_often_than_with_a_crew(generated):
    """D2-193: a boar hunt alone is dangerous; others hunting with you at the same place that day share the danger."""
    w, WL, wood = _hunters(generated, n=80)
    alone = [_do(w, f"H{i}", {"do": "gather", "what": "boar hunt", "at": wood, "looking for": "boar"}) for i in range(40)]
    w2, _, wood2 = _hunters(generated, n=80)
    together = []
    for i in range(40, 80):                                                     # hunters in fours, each four at the same wood
        together.append(_do(w2, f"H{i}", {"do": "gather", "what": "boar hunt", "at": wood2, "looking for": "boar"}))
    hurt = lambda rs: sum("turned on you" in r for r in rs) / max(1, sum("came on" in r for r in rs))
    assert hurt(alone) >= hurt(together[4:])


# ---------------------------------------------------------------------- wave 2: the fold and the hungry year
def _ring(w, WL, node="s1"):
    m = WL.model(w)
    land = w.s["wild"]["land"]
    return m, next(i for i, a in enumerate(m.ids) if land["areas"][a]["kind"] == "ring" and land["areas"][a]["node"] == node)


def test_a_hungry_pack_takes_a_beast_from_the_herd_and_leaves_its_carcass(generated):
    w, WL = _summer_world(generated)
    m, ri = _ring(w, WL)
    st = w.s["wild"]["state"]
    st["pop"]["wolf"][ri] = 8.0 / m.km2[ri]
    st["cond"]["wolf"][ri] = 0.0
    from cybertron2.engine import farm as FM
    herds = [hid for hid, h in w.s["herds"].items() if h["node"] == "s1"]
    assert herds
    before = sum(FM.head(w.s["herds"][h]) for h in herds)
    carcasses = lambda: sum(1 for c in w.s["containers"].values() if c.get("kind") == "carcass")
    c0 = carcasses()
    for _ in range(16):
        N.night(w); w.s["day"] += 1
    assert "wolf@s1" in w.s["wild"]["groups"]
    assert sum(FM.head(w.s["herds"][h]) for h in herds) < before and carcasses() > c0


def test_a_fox_takes_hens_left_out_and_fewer_shut_in(generated):
    from cybertron2.engine import run as R
    def lost(shut):
        w, WL = _summer_world(generated)
        m, ri = _ring(w, WL)
        w.s["wild"]["state"]["pop"]["fox"][ri] = 4.0 / m.km2[ri]
        houses = [b for b, x in w.s["buildings"].items() if x["node"] == "s1" and x.get("stock")
                  and w.s["containers"][x["stock"]]["goods"].get("hen")]
        hens = lambda: sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("hen", 0) for b in houses)
        h0 = hens()
        for _ in range(40):
            if shut:
                for b in houses:
                    w.apply("set_wild", "s1", path=["shut", b], value={"day": w.d, "by": "x"})
            N.night(w); w.s["day"] += 1
        return h0 - hens(), h0
    out, h0 = lost(False)
    inn, _ = lost(True)
    assert h0 > 0 and out > 0 and inn < out


def test_kept_hens_lay(generated):
    w, WL = _summer_world(generated)
    house = next(b for b, x in w.s["buildings"].items() if x.get("stock") and w.s["containers"][x["stock"]]["goods"].get("hen"))
    N.night(w)
    assert w.s["containers"][w.s["buildings"][house]["stock"]]["goods"].get("egg", 0) > 0


def test_the_voles_numbers_show_as_signs_read_two_ways(generated):
    from cybertron2.engine import here as HR, perceive as PC, run as R, signs as SG
    world = copy.deepcopy(generated)
    world["agents"] = {"Ann": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1", "knows": {"hunt": {"level": "known", "skill": 1.6}}},
                       "Tom": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}}}
    w, WL = _summer_world(world)
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["voles and mice"][ri] = 4000.0
    w.s["today"] = R.blank_today()
    read = {}
    for who in ("Ann", "Tom"):
        pr = PC.practised(HR.Mind(w, who))
        read[who] = [f["text"] for f in PC.facts(HR.Here(w, who)) if "#wildp" in (f.get("sign") or "") and SG.readable(f, pr)]
    assert any("thick with voles" in t for t in read["Ann"]) and any("kestrels" in t for t in read["Tom"])
