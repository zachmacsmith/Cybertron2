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
    words = {w for name in list(WK.KINDS) + list(WK.LOADS) + list(WK.MARKERS) for w in re.findall(r"[a-z]+", name)
             if len(w) > 3 and w not in ("wild", "mice", "brown", "first", "frost")}
    for path in ("cybertron2/wild/ecology.py", "cybertron2/engine/wild.py", "cybertron2/wild/areas.py", "cybertron2/wild/loads.py"):
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
    world.setdefault("wild", {})["methods_known"] = {}                              # nobody raised to the wild methods (D2-204 §6)
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


def _hunters(generated, n=30, knows=("hunt the wild", "drive", "stalk")):
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
    took = [r for i in range(30) for r in [_do(w, f"H{i}", {"do": "gather", "what": "stalk", "at": wood, "range": "the wood around",
                                                              "looking for": "roe deer"})] if "took it" in r]
    after = sum(np.asarray(w.s["wild"]["state"]["pop"]["roe deer"]) * WL.model(w).km2)
    roe = sum(r.count("roe deer and took it") for r in took)                    # every roe taken on a trip (brief 4: several met)
    assert roe >= 1 and abs((before - after) - roe) < 1e-6
    assert any(w.goods(w.s["people"][f"H{i}"]["hands"]).get("meat", 0) > 0 for i in range(30))


def test_looking_for_something_makes_it_likelier_but_not_certain(generated):
    """A hunter who names a quarry meets it more often than one taking what comes, and sometimes meets something else."""
    w, WL, wood = _hunters(generated, n=60)
    met = lambda r, k: f"came on a {k}" in r or f"came on an {k}" in r
    general, aimed = [], []
    for i in range(30):                                                         # in turn: the wood grows wary of both alike
        general.append(_do(w, f"H{i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around"}))
        aimed.append(_do(w, f"H{30 + i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around",
                                          "looking for": "boar"}))
    g_boar = sum(met(r, "wild boar") for r in general) / max(1, sum("came on" in r for r in general))
    a_boar = sum(met(r, "wild boar") for r in aimed) / max(1, sum("came on" in r for r in aimed))
    assert a_boar > g_boar
    assert any("instead of the boar" in r for r in aimed) or a_boar < 1.0


def test_boar_hunted_alone_hurt_more_often_than_with_a_crew(generated):
    """D2-193: a boar hunt alone is dangerous; others hunting with you at the same place that day share the danger."""
    w, WL, wood = _hunters(generated, n=80)
    alone = [_do(w, f"H{i}", {"do": "gather", "what": "drive", "at": wood, "looking for": "boar"}) for i in range(40)]
    w2, _, wood2 = _hunters(generated, n=80)
    together = []
    for i in range(40, 80):                                                     # hunters in fours, each four at the same wood
        together.append(_do(w2, f"H{i}", {"do": "gather", "what": "drive", "at": wood2, "looking for": "boar"}))
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
    from cybertron2.engine import signs as SG
    formed, true = False, None
    for _ in range(16):
        N.night(w)
        formed |= "wolf@s1" in w.s["wild"]["groups"]
        c = next((c for c in w.s["containers"].values() if c.get("kind") == "carcass" and c.get("cause") == "killed"), None)
        if c is not None and true is None:                                         # the morning after the kill
            w.s["day"] += 1
            rows, x = SG.bundle(w, c)
            true = [r["text"](x) for _, r in SG.true_rows(rows, x)]
        else:
            w.s["day"] += 1
    assert formed
    assert sum(FM.head(w.s["herds"][h]) for h in herds) < before and carcasses() > c0
    assert any("torn at the throat" in t for t in true) and not any("no mark" in t for t in true)
    assert any("wolves killed" in t for t in true)                                  # the hunter's reading, from the kinds' data


def test_a_fox_takes_hens_left_out_and_fewer_shut_in(generated):
    from cybertron2.engine import run as R
    def lost(shut):
        w, WL = _summer_world(generated)
        m, ri = _ring(w, WL)
        w.s["wild"]["state"]["pop"]["fox"][ri] = 4.0 / m.km2[ri]
        w.s["wild"]["state"]["pop"]["stoat"] = [0.0] * len(w.s["wild"]["state"]["pop"]["stoat"])   # the fox alone (brief 2: a
        houses = [b for b, x in w.s["buildings"].items() if x["node"] == "s1" and x.get("stock")             # stoat's gaps are not shut)
                  and w.s["containers"][x["stock"]]["goods"].get("hen")]
        hens = lambda: sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("hen", 0) for b in houses)
        h0 = hens()
        for _ in range(40):
            for b in houses:                                                     # kept sound: a damaged house's gaps let a fox in
                w.s["buildings"][b]["condition"] = 2                             # shut or not (brief 2 §4)
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


# ---------------------------------------------------------------------- the signs sweep (wild_layer.md §3.6, guides/senses.md)
def _two(generated):
    world = copy.deepcopy(generated)
    world["agents"] = {"Ann": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1", "knows": {"hunt": {"level": "known", "skill": 1.6}}},
                       "Tom": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}}}
    return world


def _read(w, who, mark):
    from cybertron2.engine import here as HR, perceive as PC, run as R, signs as SG
    w.s["today"] = R.blank_today()
    pr = PC.practised(HR.Mind(w, who))
    return [f["text"] for f in PC.facts(HR.Here(w, who)) if mark in (f.get("sign") or "") and SG.readable(f, pr)
            and (not f.get("only") or who in f["only"])]


def test_the_ecology_keeps_the_calendars_seasons(generated):
    """A world that starts in summer steps the ecology in summer (its seasons begin with spring)."""
    w, WL = _summer_world(generated)
    Y, S = w.year_days(), w.year_days() // 4
    assert (WL.eco_day(w) % Y) // S == ["spring", "summer", "autumn", "winter"].index(w.calendar()["season"])


def test_a_raid_that_took_nothing_leaves_the_signs_of_a_try_not_of_a_kill(generated):
    w, WL = _summer_world(_two(generated))
    house = next(b for b, x in w.s["buildings"].items() if x["node"] == "s1" and x.get("stock"))
    pid = w.s["buildings"][house]["parcel"]
    w.apply("set_wild", "s1", path=["traces"], value={pid: [{"kind": "fox", "what": "tried", "day": w.d, "n": 2}]})
    w.s["day"] += 1
    seen = _read(w, "Ann", "#wild") + _read(w, "Tom", "#wild")
    assert any("did not get in" in t or "scraped away" in t for t in seen) and not any("feathers" in t for t in seen)


def test_a_quiet_watch_is_known_to_the_watcher_only(generated):
    from cybertron2.engine import night as N
    w, WL = _summer_world(_two(generated))
    for k in ("wild boar", "red deer", "wolf", "fox"):                                # nothing comes tonight
        w.s["wild"]["state"]["pop"][k] = [0.0] * len(w.s["wild"]["state"]["pop"][k])
    field = WL._fields(w, "s1")[0]
    w.apply("set_wild", "s1", path=["watch", field], value={"day": w.d, "by": "Tom", "scare": "fire"})
    N.night(w)
    assert any(t["what"] == "watched" and t.get("by") == "Tom" for t in w.s["wild"]["traces"][field])
    assert any("nothing came near" in t and "fire" in t for t in _read(w, "Tom", "#wild"))
    assert not any("nothing came near" in t for t in _read(w, "Ann", "#wild"))


def test_hunting_a_range_shows_its_kinds_signs_read_two_ways_and_remembered(generated):
    """A hunt is a noticing process of its own: the kinds in the range show their signs, met or not; one practised in any way of
    hunting (`reads_as`) reads them as a hunter, the rest as anyone; what was seen is remembered of the place."""
    from cybertron2.engine.here import Mind
    from cybertron2.wild.kinds import HUNT_NOTICES
    w, WL, wood = _hunters(generated, n=80, knows=("stalk",))
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["wild boar"][ri] = 60.0 / m.km2[ri]
    for i in range(40, 80):                                                           # half have never hunted
        w.s["know"][f"H{i}"] = {}
    go = lambda i: _do(w, f"H{i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around"})
    known, lay = [go(i) for i in range(40)], [go(i) for i in range(40, 80)]
    texts = lambda read: [r["text"] for rs in HUNT_NOTICES.values() for r in rs if r["read"] == read]
    hit = lambda rs, read: sum(any(t in r for t in texts(read)) for r in rs)
    assert hit(known, "knows") > 0 and hit(known, "lay") == 0
    assert hit(lay, "lay") > 0 and hit(lay, "knows") == 0
    pid = next(p for p, x in w.s["parcels"].items() if x["name"] == wood)
    assert any(k.startswith(pid) and v["how"] == "hunted" for i in range(80) for k, v in (Mind(w, f"H{i}").store.get("land") or {}).items())


def test_what_the_wild_kinds_ate_shows_on_the_fields_and_in_the_stores(generated):
    w, WL = _summer_world(_two(generated))
    w.apply("set_wild", "s1", path=["eaten"], value={"s1": {"crops": 0.02, "stores": 0.02, "day": w.d}})
    seen = _read(w, "Tom", "#wildeat") + _read(w, "Ann", "#wildeat")
    assert any("nibbled" in t or "ears stripped" in t for t in seen)


def test_a_mast_year_shows_under_the_oaks_in_the_autumn(generated):
    from cybertron2.wild.kinds import MAST
    w, WL = _summer_world(_two(generated))
    if not any(p["node"] == "s1" and p["cover"] == "forest" for p in w.s["parcels"].values()):
        pytest.skip("no wood at s1")
    w.s["day"] += next(d for d in range(40) if w.calendar(w.d + d)["season"] == "autumn" and w.calendar(w.d + d)["day"] == 1)
    w.s["wild"]["state"]["mast_now"] = MAST["levels"]["heavy"]
    seen = _read(w, "Tom", "#wildmast") + _read(w, "Ann", "#wildmast")
    assert any("acorns lie thick" in t for t in seen)


# ---------------------------------------------------------------------- wave 3: loads and the year's markers
def _home_i(w, WL, node="s1"):
    m = WL.model(w)
    return m, m.ids.index(w.s["wild"]["land"]["home"][node])


def _young_field(w, fam="grain", age=1):
    from cybertron2.engine import farm as FM
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == "s1" and x["cover"] == "field")
    par = w.s["parcels"][pid]
    for _, _, c in FM.standing(par):
        c.update(crop=fam, sown=w.d - age, left=10.0 * par["size"], area_left=par["size"])
    return pid, par


def test_a_slug_year_grazes_the_young_corn_and_picking_by_lantern_saves_some(generated):
    from cybertron2.engine import farm as FM, night as N
    from cybertron2.wild.kinds import LOADS
    lost = {}
    for guarded in (False, True):
        w, WL = _summer_world(generated)
        m, i = _home_i(w, WL)
        pid, par = _young_field(w)
        st = w.s["wild"]["state"]
        st["loads"]["level"]["slugs"][i] = 3.5
        st["soil"] = [2.5] * m.n                                                    # wet
        if guarded:
            w.apply("set_wild", "s1", path=["guard", pid], value={"load": "slugs", "cut": 0.6, "until": w.d, "by": "x"})
        rec = N.night(w)
        assert "slugs" in rec["wild"]["loads"]["hits"][pid] and "slugs" in w.s["wild"]["hits"][pid]
        lost[guarded] = rec["wild"]["loads"]["hits"][pid]["slugs"]["lost"]
    assert lost[False] > 0 and 0 < lost[True] < 0.6 * lost[False]


def test_an_old_crop_is_out_of_the_slugs_window(generated):
    from cybertron2.engine import farm as FM, night as N
    w, WL = _summer_world(generated)
    m, i = _home_i(w, WL)
    pid, par = _young_field(w, age=20)
    w.s["wild"]["state"]["loads"]["level"]["slugs"][i] = 3.5
    w.s["wild"]["state"]["loads"]["level"]["aphids"][i] = 0.0
    rec = N.night(w)
    assert "slugs" not in rec["wild"]["loads"]["hits"].get(pid, {})


def test_a_flush_of_fungi_brings_up_the_mushrooms_in_the_woods(generated):
    from cybertron2.engine import night as N
    w, WL = _summer_world(generated)
    m, i = _home_i(w, WL)
    woods = [p for p, x in w.s["parcels"].items() if x["node"] == "s1" and "mushrooms" in x["res"]]
    assert woods
    w.s["wild"]["state"]["loads"]["level"]["fungi"][i] = 2.2
    N.night(w)
    assert all(w.s["parcels"][p]["res"]["mushrooms"]["f"] > 1.0 for p in woods)        # the load out of its season falls; still above


def test_a_rising_slug_load_reads_two_ways_by_the_practice_of_sowing(generated):
    world = _two(generated)
    world["agents"]["Ann"]["knows"] = {"sow": {"level": "known", "skill": 1.6}}
    w, WL = _summer_world(world)
    m, i = _home_i(w, WL)
    L = w.s["wild"]["state"]["loads"]
    L["prev"] = {k: list(v) for k, v in L["level"].items()}
    L["prev"]["slugs"][i], L["level"]["slugs"][i] = 0.8, 2.5
    ann, tom = _read(w, "Ann", "#wildload"), _read(w, "Tom", "#wildload")
    assert any("a slug year" in t for t in ann) and not any("silver slime" in t for t in ann)
    assert any("silver slime" in t for t in tom) and not any("a slug year" in t for t in tom)
    L["prev"]["slugs"][i] = 2.5                                                      # a standing level is not a change
    assert not _read(w, "Tom", "#wildload")


def test_the_years_markers_come_earlier_in_a_warm_spring():
    from cybertron2.wild import loads as LD, kinds as K
    from types import SimpleNamespace
    m = SimpleNamespace(n=1, Y=32, S=8, land={"areas": {"a0": {"kind": "home", "km2": 1.0, "cover": {"field": 1.0}, "texture": {"loam": 1.0}}}},
                        ids=["a0"])
    def day_of(t):
        st = {}
        for d in range(16):
            LD.step(m, st, d, np.array([t]), np.array([t - 5]), np.array([False]), np.array([1.0]))
        return st["loads"]["marks"]["blackthorn"][0], st["loads"]["marks"]["may"][0]
    cool, warm = day_of(8.0), day_of(12.0)
    assert warm[0] < cool[0] and warm[1] < cool[1]


def test_the_harm_of_a_load_shows_on_the_field_it_fell_on(generated):
    w, WL = _summer_world(_two(generated))
    pid, par = _young_field(w)
    w.apply("set_wild", "s1", path=["hits"], value={pid: {"slugs": {"day": w.d, "share": 0.05, "lost": 1.0}}})
    w.s["day"] += 1
    assert any("grazed off to stumps" in t and par["name"] in t for t in _read(w, "Tom", "#wildhit") + _read(w, "Ann", "#wildhit"))


def test_a_marker_shows_on_the_day_it_comes_with_the_sowers_lore(generated):
    world = _two(generated)
    world["agents"]["Ann"]["knows"] = {"sow": {"level": "known", "skill": 1.6}}
    w, WL = _summer_world(world)
    m, i = _home_i(w, WL)
    L = w.s["wild"]["state"]["loads"]
    L["marks"] = {"may": [None] * m.n}
    L["marks"]["may"][i] = WL.eco_day(w)
    ann, tom = _read(w, "Ann", "#wildmark"), _read(w, "Tom", "#wildmark")
    assert any("may in blossom" in t for t in tom) and not any("frosts are done" in t for t in tom)
    assert any("frosts are done" in t for t in ann)
    w.s["day"] += 1                                                                  # gone the next day: a change, not a fact
    assert not _read(w, "Tom", "#wildmark")


# ---------------------------------------------------------------------- wave 4: disease by host and area
def _sicken(w, hid, name="murrain"):
    from cybertron2.engine import farm as FM
    h = w.s["herds"][hid]
    w.apply("set", h["node"], ref=("herd", hid), field="ill", value={name: {"sick": [{"day": w.d, "n": FM.head(h)}], "immune": 0, "new": w.d}})


def _sick_n(w, hid, name="murrain"):
    return sum(int(c["n"]) for c in ((w.s["herds"][hid].get("ill") or {}).get(name) or {}).get("sick", []))


def _herd_world(generated):
    w, WL = _summer_world(generated)
    hs = {h["parcel"]: [] for h in w.s["herds"].values() if h["node"] == "s4"}
    for hid, h in sorted(w.s["herds"].items()):
        if h["node"] == "s4":
            hs[h["parcel"]].append(hid)
    shared = next(p for p, l in sorted(hs.items()) if len(l) >= 2)
    other = next(hid for p, l in sorted(hs.items()) if p != shared and p not in w.s["parcels"][shared]["adj"] for hid in l)
    return w, WL, hs[shared][0], hs[shared][1], other


def test_murrain_goes_through_a_shared_pasture_far_more_than_to_a_herd_kept_apart(generated):
    from cybertron2.engine import night as N
    w, WL, sick, mate, apart = _herd_world(generated)
    _sicken(w, sick)
    N.night(w); w.s["day"] += 1
    assert _sick_n(w, mate) > _sick_n(w, apart)


def test_a_herd_carries_its_sickness_to_another_village(generated):
    from cybertron2.engine import night as N
    w, WL, sick, mate, apart = _herd_world(generated)
    there = next(h for h in w.s["herds"].values() if h["node"] == "s3")
    _sicken(w, sick)
    w.s["herds"][sick].update(node="s3", parcel=there["parcel"], home=there["parcel"])           # driven there
    N.night(w); w.s["day"] += 1
    assert any(_sick_n(w, hid) for hid, h in w.s["herds"].items() if h["node"] == "s3" and hid != sick)


def test_beasts_dead_of_the_murrain_leave_carcasses_read_as_sickness_and_by_a_herder_as_murrain(generated, monkeypatch):
    from cybertron2.engine import night as N, signs as SG
    from cybertron2.wild import kinds as K
    monkeypatch.setitem(K.DISEASES["murrain"], "mortality", 1.0)
    w, WL, sick, mate, apart = _herd_world(generated)
    _sicken(w, sick)
    w.s["herds"][sick]["ill"]["murrain"]["sick"][0]["day"] = w.d - 2                    # its course run
    before = sum(1 for c in w.s["containers"].values() if c.get("kind") == "carcass")
    N.night(w); w.s["day"] += 1
    cs = [c for c in w.s["containers"].values() if c.get("kind") == "carcass" and c.get("cause") == "sick"]
    assert len(cs) >= 1 and sum(1 for c in w.s["containers"].values() if c.get("kind") == "carcass") > before
    rows, x = SG.bundle(w, cs[0])
    true = [r["text"](x) for _, r in SG.true_rows(rows, x)]
    assert any("a sickness took it" in t for t in true) and any("died of the murrain" in t for t in true)
    assert not any("no mark" in t for t in true)


def test_a_sick_herd_reads_two_ways_by_the_practice_of_herding(generated):
    world = _two(generated)
    for a in world["agents"].values():
        a["at"] = "s4"
    world["agents"]["Ann"]["knows"] = {"herd": {"level": "known", "skill": 1.6}}
    w, WL, sick, mate, apart = _herd_world(world)
    _sicken(w, sick)
    ann, tom = _read(w, "Ann", "#wildsick"), _read(w, "Tom", "#wildsick")
    assert any("murrain in" in t for t in ann) and not any("off their feed" in t for t in ann)
    assert any("off their feed" in t for t in tom) and not any("murrain" in t for t in tom)


def test_a_wild_disease_spreads_along_the_lands_links_and_burns_out_into_immunity(generated):
    from cybertron2.wild import diseases as DS
    w, WL = _summer_world(generated)
    m = WL.model(w)
    st = {"dis": {"mange": [0.0] * m.n}}
    a = int(m.la[0])
    st["dis"]["mange"][a] = 0.3
    N_ = {k: np.asarray(v, float) * 3 for k, v in w.s["wild"]["state"]["pop"].items()}       # crowded
    seen = set()
    for d in range(40):
        DS.step(m, st, 40 + d, N_, {})
        seen |= {i for i, x in enumerate(st["dis"]["mange"]) if x > 0.01}
    assert len(seen) > 1                                                             # it travelled
    assert max(st["dis_immune"]["mange"]) > 0                                       # and left immunity behind


# ---------------------------------------------------------------------- wild plants (D2-200 to D2-202)
def test_plant_kinds_take_the_place_of_plants_where_their_conditions_are(generated):
    from cybertron2.wild import plants as PL
    w, WL = _summer_world(generated)
    pars = w.s["parcels"].values()
    assert not any("plants" in p["res"] and p["cover"] in PL.LAYERS for p in pars)        # replaced wherever a kind suits
    oak = [p for p in pars if p.get("ecosystem") == "oak-ash wood" and p["cover"] == "forest"]
    beech = [p for p in pars if p.get("ecosystem") == "beech wood" and p["cover"] == "forest"]
    assert oak and all("acorns" in p["res"] and "hazel nuts" in p["res"] for p in oak)
    if beech:
        b = beech[0]["res"]
        assert b.get("beech mast", {}).get("K", 0) > b.get("acorns", {}).get("K", 0)
    for p in pars:
        if "watercress" in p["res"]:
            assert PL.suit("watercress", p) > 0
        assert "samphire" not in p["res"] or float((p.get("land") or {}).get("sea_km", 99)) <= 3.0
    w2 = build(generated, packs=())
    assert any("plants" in p["res"] for p in w2.s["parcels"].values())                   # without the pack, as before


def test_a_plant_comes_in_its_season_and_goes_after():
    from cybertron2.engine import renewal as RN
    r = {"S": 0.0, "K": 2.0, "r": 0.4, "rot": 0.3, "seasons": {"spring": 1.0, "summer": 0.5}, "f": 1.0}
    for _ in range(8):
        r["S"] = RN.RULES["seasonal"]({}, r, {"season": "spring"})
    assert r["S"] > 1.8
    for _ in range(8):
        r["S"] = RN.RULES["seasonal"]({}, r, {"season": "winter"})
    assert r["S"] < 0.2


def _autumn_wood(generated, people=6, knows=None):
    world = copy.deepcopy(generated)
    world["calendar"] = {"season": "autumn", "day": 2, "season_days": 8}
    world["agents"] = {f"G{i}": {"household": "Ash", "stage": "adult", "sex": "f", "at": "s1", "knows": dict(knows or {})} for i in range(people)}
    w = build(world, history=2)
    from cybertron2.engine import run as R, wild as WL
    w.s["today"] = R.blank_today()
    wood = next(p for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] == "forest" and "hazel nuts" in p["res"])
    return w, WL, wood


def test_gathering_in_autumn_takes_whats_in_season_and_more_of_what_one_looks_for(generated):
    w, WL, wood = _autumn_wood(generated, people=8)
    any_ = [_do(w, f"G{i}", {"do": "gather", "what": "gather wild food", "at": wood["name"]}) for i in range(4)]
    nuts = [_do(w, f"G{i}", {"do": "gather", "what": "gather wild food", "at": wood["name"], "looking for": "nuts"}) for i in range(4, 8)]
    assert all("You gathered" in r for r in any_), any_
    assert not any("greens" in r and "hazel" not in r for r in any_)
    def share(rs):
        tot = sum(float(x) for r in rs for x in re.findall(r"([\d.]+) [a-z]", r.split(" at ")[0]))
        nut = sum(float(x) for r in rs for x in re.findall(r"([\d.]+) hazel nuts", r))
        return nut / max(tot, 1e-9)
    assert share(nuts) > share(any_)


def test_mushrooms_harm_the_gatherer_who_does_not_know_them_and_never_the_expert(generated, monkeypatch):
    from cybertron2.wild import plants as PL
    monkeypatch.setitem(PL.PLANTS["mushrooms"], "poison", 1.0)
    w, WL, wood = _autumn_wood(generated, people=12)
    for p in w.s["parcels"].values():
        if "mushrooms" in p["res"]:
            p["res"]["mushrooms"]["S"] = p["res"]["mushrooms"]["K"]
    for i in range(6, 12):
        w.s["know"][f"G{i}"] = {"gather wild food": {"level": "known", "skill": 1.5}}             # the top of basic work: expert
    lay = [_do(w, f"G{i}", {"do": "gather", "what": "gather wild food", "at": wood["name"], "looking for": "mushrooms"}) for i in range(6)]
    exp = [_do(w, f"G{i}", {"do": "gather", "what": "gather wild food", "at": wood["name"], "looking for": "mushrooms"}) for i in range(6, 12)]
    assert any("bad" in r or "deadly" in r for r in lay)
    assert not any("bad" in r or "deadly" in r for r in exp)


def test_the_wild_kinds_eat_the_same_acorns_people_gather(generated):
    """D2-202: boar on a village's land eat its woods' acorns; what they eat is gone from the parcels' stocks."""
    from cybertron2.engine import night as N
    def acorns_after(boar):
        w, WL, wood = _autumn_wood(generated, people=1)
        m = WL.model(w)
        i = m.ids.index(w.s["wild"]["land"]["home"]["s1"])
        w.s["wild"]["state"]["pop"]["wild boar"][i] = boar / m.km2[i]
        for p in w.s["parcels"].values():
            if "acorns" in p["res"]:
                p["res"]["acorns"].update(S=p["res"]["acorns"]["K"], f=1.0)
        before = sum(p["res"]["acorns"]["S"] for p in w.s["parcels"].values() if p["node"] == "s1" and "acorns" in p["res"])
        rec = N.night(w)
        after = sum(p["res"]["acorns"]["S"] for p in w.s["parcels"].values() if p["node"] == "s1" and "acorns" in p["res"])
        return before - after, rec
    none_, _ = acorns_after(0.0)
    many, rec = acorns_after(40.0)
    assert many > none_ and "mast" in (rec["wild"]["shared"].get("s1") or {})


def test_acorns_are_leached_into_meal_at_a_hearth(generated):
    w, WL, wood = _autumn_wood(generated, people=1)
    hearth = next((b for b, x in w.s["buildings"].items() if x["node"] == "s1" and (x.get("fittings") or {}).get("hearth")), None)
    if hearth is None:
        pytest.skip("no hearth at s1")
    w.apply("create", "s1", dst=w.hands("G0"), item="acorns", qty=6)
    r = _do(w, "G0", {"do": "make", "what": "leach acorns", "at": w.s["buildings"][hearth]["name"]})
    assert "acorn meal" in r, r


# ---------------------------------------------------------------------- the full layers (02zq): conditions, phases, the hunted wood
def _group_ready(w, WL, kind, node="s1"):
    from cybertron2.engine import night as N
    for _ in range(12):
        g = (w.s["wild"].get("groups") or {}).get(f"{kind}@{node}")
        if g and g["pos"] == "ready":
            return g
        N.night(w); w.s["day"] += 1
    return (w.s["wild"].get("groups") or {}).get(f"{kind}@{node}")


def test_a_hard_frost_sends_the_boar_to_the_stores_and_a_shut_door_keeps_most_out(generated, monkeypatch):
    from cybertron2.engine import night as N
    def store_lost(shut):
        w, WL = _summer_world(generated)
        monkeypatch.setattr(WL, "frozen_run", lambda w_, node, day=None, most=6: 3)
        for pid, par in w.s["parcels"].items():                                      # no field to go to: only the stores
            for _, _, c in __import__("cybertron2.engine.farm", fromlist=["x"]).standing(par):
                c["left"], c["area_left"] = 0.0, 0.0
        houses = [b for b, x in w.s["buildings"].items() if x["node"] == "s1" and x.get("stock")]
        for b in houses:
            w.s["containers"][w.s["buildings"][b]["stock"]]["goods"]["grain"] = 50.0
        before = sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("grain", 0) for b in houses)
        for _ in range(16):
            if shut:
                for b in houses:
                    w.apply("set_wild", "s1", path=["shut", b], value={"day": w.d, "by": "x"})
            N.night(w); w.s["day"] += 1
        return before - sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("grain", 0) for b in houses)
    open_, shut_ = store_lost(False), store_lost(True)
    assert open_ > 0 and shut_ < open_


def test_the_rut_makes_red_deer_bold_and_easier_to_come_on(generated):
    w, WL = _summer_world(generated)
    m, ri = _ring(w, WL)
    st = w.s["wild"]["state"]
    autumn = next(d for d in range(40) if w.calendar(w.d + d)["season"] == "autumn")
    e0 = WL.effects(w, "s1", "red deer", m, st, ri)
    e1 = WL.effects(w, "s1", "red deer", m, st, ri, day=w.d + autumn)
    assert e1["bold"] > e0["bold"] and e1["detect"] > e0["detect"]


def test_a_hunted_wood_empties_of_deer_and_keeps_their_group_off_the_fields(generated):
    from cybertron2.engine import night as N
    w, WL, wood = _hunters(generated, n=12)
    m, ri = _ring(w, WL)
    for i in range(12):
        _do(w, f"H{i}", {"do": "gather", "what": "stalk", "at": wood, "range": "the wood around"})
    p = w.s["wild"]["state"]["pressure"]["red deer"][ri]
    assert p > 1.0
    before = float(w.s["wild"]["state"]["pop"]["red deer"][ri])
    N.night(w)
    assert float(w.s["wild"]["state"]["pop"]["red deer"][ri]) < before                   # they moved out
    assert WL.effects(w, "s1", "red deer", m, w.s["wild"]["state"], ri)["drive"] < 1.0       # and keep off the fields


def test_a_watch_at_the_gap_meets_the_sounder_before_it_reaches_the_field(generated):
    from cybertron2.engine import night as N
    w, WL = _summer_world(generated)
    g = _group_ready(w, WL, "wild boar")
    assert g and g["pos"] == "ready"
    gap = WL._edge_of(w, g["parcel"])
    assert gap != g["parcel"]
    w.apply("set_wild", "s1", path=["watch", gap], value={"day": w.d, "by": "x", "scare": "fire"})
    w.s["groups_raid_day"] = None
    g["raid"] = w.d
    rec = N.night(w)
    r = rec["wild"]["groups"].get("wild boar@s1") or {}
    assert r.get("turned") and r.get("gap")


def test_a_fence_round_the_field_keeps_a_group_out(generated):
    from cybertron2.engine import night as N
    w, WL = _summer_world(generated)
    g = _group_ready(w, WL, "wild boar")
    assert g
    w.s["parcels"][g["parcel"]]["fence"] = {"kind": "stone", "level": 2, "built": True, "units": 20, "gate": "shut", "mend": 0, "pending": {}}
    g["raid"] = w.d
    rec = N.night(w)
    r = rec["wild"]["groups"].get("wild boar@s1") or {}
    assert r.get("turned") and r.get("scare") == "fence" or not r.get("lost")


def test_an_expert_reads_the_gap_the_practised_reads_the_sounder(generated):
    world = _two(generated)
    world["agents"]["Ann"]["knows"] = {"hunt the wild": {"level": "known", "skill": 2.6}}             # expert on the hunt's curve             # expert in basic work
    world["agents"]["Tom"]["knows"] = {"hunt the wild": {"level": "known", "skill": 1.2}}             # practised
    w, WL = _summer_world(world)
    edge = WL._edge_of(w, WL._fields(w, "s1")[0])
    w.apply("set_wild", "s1", path=["traces"], value={edge: [{"kind": "wild boar", "what": "edge", "day": w.d, "n": 9}]})
    w.s["day"] += 1
    ann, tom = _read(w, "Ann", "#wild"), _read(w, "Tom", "#wild")
    assert any("gap in the thorn" in t for t in ann) and not any("gap in the thorn" in t for t in tom)
    assert any("sounder of about 9" in t for t in tom)


def test_a_phase_shows_the_day_it_begins(generated):
    world = _two(generated)
    w, WL = _summer_world(world)
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["red deer"][ri] = 20.0 / m.km2[ri]
    w.s["day"] += next(d for d in range(40) if w.calendar(w.d + d)["season"] == "autumn" and w.calendar(w.d + d)["day"] == 1)
    assert any("stags roaring" in t for t in _read(w, "Tom", "#wildwhen"))
    w.s["day"] += 1
    assert not any("stags roaring" in t for t in _read(w, "Tom", "#wildwhen"))


def test_digging_out_the_earth_in_spring_takes_the_cubs(generated):
    world = copy.deepcopy(generated)
    world["calendar"] = {"season": "spring", "day": 3, "season_days": 8}
    world["agents"] = {f"D{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}} for i in range(20)}
    w = build(world, history=2)
    from cybertron2.engine import run as R, wild as WL
    w.s["today"] = R.blank_today()
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["fox"][ri] = 30.0 / m.km2[ri]
    wood = next(p["name"] for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] in ("forest", "scrub"))
    before = sum(np.asarray(w.s["wild"]["state"]["pop"]["fox"]) * m.km2)
    took = [r for i in range(20) for r in [_do(w, f"D{i}", {"do": "gather", "what": "den work", "at": wood, "range": "the wood around"})]
            if "took it" in r]
    after = sum(np.asarray(w.s["wild"]["state"]["pop"]["fox"]) * m.km2)
    assert took and before - after >= 4 * len(took) - 1e-6                                       # the vixen and her cubs


def test_mowing_in_early_summer_may_turn_up_a_roe_kid(generated):
    from cybertron2.engine import wild as WL0
    world = copy.deepcopy(generated)
    world["calendar"] = {"season": "spring", "day": 7, "season_days": 8}
    world["agents"] = {f"M{i}": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s1", "knows": {}} for i in range(30)}
    w = build(world, history=2)
    from cybertron2.engine import run as R, wild as WL
    w.s["today"] = R.blank_today()
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["roe deer"][ri] = 60.0 / m.km2[ri]
    meadow = next((p["name"] for p in w.s["parcels"].values() if p["node"] == "s1" and p["cover"] in ("meadow", "pasture")), None)
    if meadow is None:
        pytest.skip("no grass to mow at s1")
    rs = [_do(w, f"M{i}", {"do": "gather", "what": "hay", "at": meadow}) for i in range(30)]
    assert any("roe kid" in r for r in rs)


def test_the_vermin_follow_the_harvest_in_and_a_terrier_keeps_the_store(generated):
    from cybertron2.engine import night as N
    def share(harvest, dog):
        w, WL = _summer_world(generated)
        houses = [b for b, x in w.s["buildings"].items() if x["node"] == "s1" and x.get("stock")]
        for b in houses:
            w.s["containers"][w.s["buildings"][b]["stock"]]["goods"]["grain"] = 40.0
            if dog:
                w.s["buildings"][b]["fittings"]["dog"] = 1
        for _ in range(3):
            N.night(w); w.s["day"] += 1
        if harvest:
            for b in houses:
                w.s["containers"][w.s["buildings"][b]["stock"]]["goods"]["grain"] = 160.0
        have = sum(w.s["containers"][w.s["buildings"][b]["stock"]]["goods"].get("grain", 0) for b in houses)
        rec = N.night(w)
        return float((rec["wild"].get("stores") or {}).get("s1", 0.0)) / have
    assert share(True, False) > share(False, False)
    assert share(True, True) < share(True, False)


def test_the_ladybird_grubs_misread_and_picked_off_leave_the_fly(generated):
    from cybertron2.engine import run as R
    w, WL = _summer_world(_two(generated))
    w.s["today"] = R.blank_today()
    m, i = _home_i(w, WL)
    L = w.s["wild"]["state"]["loads"]
    L["level"]["ladybirds"][i] = 2.0
    pid, par = _young_field(w, fam="legumes", age=6)
    _do(w, "Tom", {"do": "work", "what": "pest work", "looking for": "grubs", "at": par["name"]})
    assert w.s["wild"]["state"]["loads"]["level"]["ladybirds"][i] < 2.0


def test_the_first_rain_after_a_dry_spell_brings_the_slugs_out():
    from cybertron2.wild import loads as LD
    from types import SimpleNamespace
    m = SimpleNamespace(n=1, Y=32, S=8, land={"areas": {"a0": {"kind": "home", "km2": 1.0, "cover": {"field": 1.0}, "texture": {"clay": 1.0}}}},
                        ids=["a0"])
    def run(jump):
        st = {}
        for d in range(4):
            LD.step(m, st, d, np.array([10.0]), np.array([5.0]), np.array([False]), np.array([0.6]), np.array([0.6]))
        LD.step(m, st, 4, np.array([10.0]), np.array([5.0]), np.array([False]), np.array([1.2]), np.array([1.2 - jump]))
        return st["loads"]["level"]["slugs"][0]
    assert run(0.6) > run(0.0)


# ---------------------------------------------------------------------- the expert's readings (L3) for every kind
TAKEN_KINDS = ("red deer", "roe deer", "wild boar", "brown hare", "woodpigeon", "fox", "wolf", "brown bear", "wildfowl", "eel")
def test_an_expert_hunter_reads_how_many_and_in_what_condition(generated):
    w, WL, wood = _hunters(generated, n=60, knows=())
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["wild boar"][ri] = 40.0 / m.km2[ri]
    for i in range(30):
        w.s["know"][f"H{i}"] = {"hunt the wild": {"level": "known", "skill": 1.5}}                 # experts: they know the
        w.s["mind"].setdefault(f"H{i}", {})["familiar"] = {k: 0.8 for k in TAKEN_KINDS}           # kinds well (D2-204 §5)
    for i in range(30, 60):
        w.s["know"][f"H{i}"] = {"hunt the wild": {"level": "known", "skill": 1.2}}                 # practised
        w.s["mind"].setdefault(f"H{i}", {})["familiar"] = {k: 0.3 for k in TAKEN_KINDS}
    go = lambda i: _do(w, f"H{i}", {"do": "gather", "what": "hunt the wild", "at": wood, "range": "the wood around"})
    exp, prac = [go(i) for i in range(30)], [go(i) for i in range(30, 60)]
    pat = re.compile(r"about \d+ [a-z ]+?(use this ground|hold the thickets|on this land|over this land|ranges this land)[^.;]*?(fat|fair|lean|starving)")
    assert any(pat.search(r) for r in exp) and not any(pat.search(r) for r in prac)


def test_an_expert_reads_the_voles_in_the_owl_pellets(generated):
    world = _two(generated)
    world["agents"]["Ann"]["knows"] = {"hunt the wild": {"level": "known", "skill": 2.6}}             # expert on the hunt's curve
    world["agents"]["Tom"]["knows"] = {"hunt the wild": {"level": "known", "skill": 1.2}}
    w, WL = _summer_world(world)
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["voles and mice"][ri] = 4000.0
    assert any("pellets" in t for t in _read(w, "Ann", "#wildp")) and not any("pellets" in t for t in _read(w, "Tom", "#wildp"))


def test_an_expert_reads_what_a_kill_means_for_the_herd(generated):
    from cybertron2.engine import signs as SG, things as TH
    w, WL = _summer_world(generated)
    pid = next(p for p, x in w.s["parcels"].items() if x["node"] == "s1" and x["cover"] == "pasture")
    cid = TH.leave_carcass(w, "s1", "cow", "the Ash cattle", [], "killed", {"meat": 4.0, "hide": 1}, parcel=pid, by="wolf")
    rows, x = SG.bundle(w, w.s["containers"][cid])
    exp = [r for _, r in SG.true_rows(rows, x) if r.get("knows") == "expert:hunt"]
    assert exp and "back to this herd" in exp[0]["text"](x)


def test_an_expert_knows_oak_before_ash_says_nothing_of_the_summer(generated):
    world = _two(generated)
    world["agents"]["Ann"]["knows"] = {"sow": {"level": "known", "skill": 1.5}}
    world["agents"]["Tom"]["knows"] = {"sow": {"level": "known", "skill": 1.2}}
    w, WL = _summer_world(world)
    m, i = _home_i(w, WL)
    L = w.s["wild"]["state"]["loads"]
    L["marks"] = {"oak and ash": [None] * m.n}
    L["marks"]["oak and ash"][i] = WL.eco_day(w)
    ann, tom = _read(w, "Ann", "#wildmark"), _read(w, "Tom", "#wildmark")
    assert any("nothing of the summer" in t for t in ann) and not any("nothing of the summer" in t for t in tom)
    assert any("only a splash" in t for t in tom)                                               # the practised hold the saying


def test_an_expert_gatherer_reads_a_heavy_year_in_the_hazels(generated):
    w, WL, wood = _autumn_wood(generated, people=30, knows={"gather wild food": {"level": "known", "skill": 1.5}})
    for p in w.s["parcels"].values():
        if "hazel nuts" in p["res"]:
            p["res"]["hazel nuts"].update(f=1.6, S=p["res"]["hazel nuts"]["K"])
    rs = [_do(w, f"G{i}", {"do": "gather", "what": "gather wild food", "at": wood["name"]}) for i in range(30)]
    assert any("hazels here are heavy" in r for r in rs)


# ---------------------------------------------------------------------- wave 5: sites, individuals, rare regimes
def test_sites_are_placed_where_the_land_suits_them(generated):
    w, WL = _summer_world(generated)
    sites = w.s["wild"]["sites"]
    assert sites
    for sid, st_ in sites.items():
        par = w.s["parcels"][st_["parcel"]]
        if st_["kind"] == "rookery":
            assert any(w.s["parcels"][q]["cover"] == "field" for q in par["adj"])
        if st_["kind"] == "lodge":
            assert (par.get("land") or {}).get("river") not in (None, "none")


def _a_site(w, kind, node="s1"):
    from cybertron2.wild.kinds import SITES
    cover = SITES[kind]["where"]["covers"][0]
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == node and x["cover"] == cover)
    w.s["wild"].setdefault("sites", {})[f"{kind}@{pid}"] = {"kind": kind, "node": node, "parcel": pid, "size": 20.0, "last": None, "gone": None,
                                                           "back": None, "dam": False, "k0": {}}
    return f"{kind}@{pid}", pid


def test_a_heronry_troubled_in_spring_leaves_for_good_and_a_hard_winter_halves_it(generated, monkeypatch):
    from cybertron2.engine import night as N
    world = copy.deepcopy(generated)
    world["calendar"] = {"season": "spring", "day": 2, "season_days": 8}
    world["agents"] = {}
    w = build(world, history=2)
    from cybertron2.engine import wild as WL
    sid, pid = _a_site(w, "heronry")
    for _ in range(6):                                                                 # quiet work: they stay
        w.s["events"] = [{"kind": "work", "actor": "x", "about": [f"parcel:{pid}"], "tech": "firewood"}]
        N.night(w); w.s["day"] += 1
    assert w.s["wild"]["sites"][sid].get("gone") is None
    w.s["day"] -= 6
    for _ in range(8):                                                                 # felling at the nests: they go
        w.s["events"] = [{"kind": "work", "actor": "x", "about": [f"parcel:{pid}"], "tech": "fell"}]
        N.night(w); w.s["day"] += 1
        if w.s["wild"]["sites"][sid].get("gone") is not None:
            break
    assert w.s["wild"]["sites"][sid].get("gone") is not None
    w2 = build(world, history=2)
    sid2, pid2 = _a_site(w2, "heronry")
    real = WL.cond
    monkeypatch.setattr(WL, "cond", lambda w_, node, c, *a, **k: True if "hard_winter" in (c or {}) else real(w_, node, c, *a, **k))
    w2.s["day"] = next(d for d in range(1, 40) if w2.calendar(d)["season"] == "spring" and w2.calendar(d)["day"] == 1)
    WL._sites_night(w2, WL.model(w2), w2.s["wild"]["state"])
    assert w2.s["wild"]["sites"][sid2]["size"] < 20.0 and w2.s["wild"]["sites"][sid2]["why"] == "crash"


def test_rooks_pull_the_young_corn_beside_the_rookery_and_a_watch_keeps_them_off(generated):
    from cybertron2.engine import farm as FM
    def lost(watched):
        world = copy.deepcopy(generated)
        world["calendar"] = {"season": "spring", "day": 2, "season_days": 8}
        world["agents"] = {}
        w = build(world, history=2)
        from cybertron2.engine import wild as WL
        sid, site = next((k, v) for k, v in w.s["wild"]["sites"].items() if v["kind"] == "rookery")
        field = next(q for q in w.s["parcels"][site["parcel"]]["adj"] if w.s["parcels"][q]["cover"] == "field")
        par = w.s["parcels"][field]
        par["crop"] = {"kind": "barley", "crop": "grain", "sown": w.d - 1, "ripe_day": w.d + 8, "window": 4, "seed": 1, "area": par["size"],
                       "area_left": par["size"], "broken": 0, "weeded": 0, "base": 10.0 * par["size"], "rot": 1.0, "left": 10.0 * par["size"]}
        if watched:
            w.apply("set_wild", site["node"], path=["watch", field], value={"day": w.d, "by": "x", "scare": "clapper"})
        out = WL._sites_night(w, WL.model(w), w.s["wild"]["state"])
        return (out.get(sid) or {}).get("harm", 0.0)
    assert lost(False) > 0 and lost(True) == 0


def test_a_beaver_dam_floods_the_meadow_breaking_it_drains_it_and_the_beavers_rebuild(generated):
    from cybertron2.engine import run as R
    world = copy.deepcopy(generated)
    world["agents"] = {"Bo": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s4", "knows": {}}}
    w = build(world, history=2)
    from cybertron2.engine import wild as WL, night as N
    w.s["today"] = R.blank_today()
    sid, site = next(((k, v) for k, v in w.s["wild"]["sites"].items() if v["kind"] == "lodge"), (None, None))
    if sid is None:
        pytest.skip("no lodge in this world")
    flooded = {k.split("|")[0]: v for k, v in site["k0"].items() if k.endswith("|grass")}
    assert flooded and all(w.s["parcels"][q]["res"]["grass"]["K"] < v for q, v in flooded.items())
    r = _do(w, "Bo", {"do": "work", "what": "break a dam", "at": w.s["parcels"][site["parcel"]]["name"]})
    assert "broke open" in r, r
    assert all(abs(w.s["parcels"][q]["res"]["grass"]["K"] - v) < 1e-6 for q, v in flooded.items())
    for _ in range(4):
        N.night(w); w.s["day"] += 1
    assert w.s["wild"]["sites"][sid]["dam"]                                                    # rebuilt while the family lives


def test_trapping_the_last_beaver_ends_the_lodge_for_good(generated):
    from cybertron2.engine import run as R
    world = copy.deepcopy(generated)
    world["agents"] = {"Bo": {"household": "Ash", "stage": "adult", "sex": "m", "at": "s4", "knows": {}}}
    w = build(world, history=2)
    w.s["today"] = R.blank_today()
    sid, site = next(((k, v) for k, v in w.s["wild"]["sites"].items() if v["kind"] == "lodge"), (None, None))
    if sid is None:
        pytest.skip("no lodge in this world")
    name = w.s["parcels"][site["parcel"]]["name"]
    rs = [_do(w, "Bo", {"do": "gather", "what": "den work", "at": name}) for _ in range(int(site["size"]) + 1)]
    assert any("last of them" in r for r in rs) and w.s["wild"]["sites"][sid]["gone"] is not None
    assert w.goods(w.s["people"]["Bo"]["hands"]).get("beaver pelt", 0) >= 1


def test_killing_the_old_sow_scatters_the_sounder(generated):
    """A kill from a group with a leader may be the leader (odds by the group's size); the group then drives less for a while."""
    w, WL, wood = _hunters(generated, n=60, knows=("drive",))
    from cybertron2.engine import night as N
    m, ri = _ring(w, WL)
    w.s["wild"]["state"]["pop"]["wild boar"][ri] = 60.0 / m.km2[ri]
    N.night(w)
    gid = "wild boar@s1"
    g = w.s["wild"]["groups"][gid]
    w.s["wild"]["groups"][gid] = dict(g, n=1, leader={"name": "the old sow", "alive": True})      # one beast: the kill is she
    rs = []
    for i in range(60):
        rs.append(_do(w, f"H{i}", {"do": "gather", "what": "drive", "at": wood, "range": "the wood around", "looking for": "boar"}))
        if (w.s["wild"]["groups"][gid].get("leader") or {}).get("died") is not None:
            break
    assert any("the old sow that led them" in r for r in rs)
    assert w.s["wild"]["groups"][gid]["leader"]["died"] is not None


def test_a_legend_is_rare_hard_to_take_and_told_of_by_the_old(generated, monkeypatch):
    from cybertron2.wild import kinds as K
    monkeypatch.setitem(K.LEGENDS["wild boar"], "p", 1.0)
    world = _two(generated)
    world["agents"]["Tom"]["stage"] = "elder"
    w, WL = _summer_world(world)
    assert (w.s["wild"].get("legends") or {}).get("wild boar", {}).get("alive")
    w.s["day"] = 0
    assert any("great boar" in t for t in _read(w, "Tom", "#wildtale")) and not _read(w, "Ann", "#wildtale")


def test_a_great_freeze_kills_the_fowl_and_the_old_remember_the_last(generated, monkeypatch):
    world = _two(generated)
    world["agents"]["Tom"]["stage"] = "elder"
    w, WL = _summer_world(world)
    monkeypatch.setattr(WL, "frozen_run", lambda w_, node, day=None, most=6: 5)
    m = WL.model(w)
    st = w.s["wild"]["state"]
    st["pop"]["wildfowl"] = [10.0] * m.n
    WL._regime_kills(w, m, st)
    assert max(st["pop"]["wildfowl"]) < 10.0
    w.s["day"] = 0
    tom, ann = _read(w, "Tom", "#wildrare"), _read(w, "Ann", "#wildrare")
    assert any("great freeze of your youth" in t for t in tom) and not any("great freeze of your youth" in t for t in ann)
    assert any("frozen from bank to bank" in t for t in ann)


def test_a_watchs_scare_is_made_of_what_is_there(generated):
    """One-off 2 (02zq): a fire watch burns firewood, clappers and a horn must be in hand, a dog watch needs a dog at home."""
    from cybertron2.engine import run as R
    w, WL = _summer_world(_two(generated))
    w.s["today"] = R.blank_today()
    field = w.s["parcels"][WL._fields(w, "s1")[0]]["name"]
    assert "needs 1 clappers" in _do(w, "Tom", {"do": "work", "what": "guard the field", "looking for": "clappers", "at": field})
    assert "keep no dog" in _do(w, "Tom", {"do": "work", "what": "guard the field", "looking for": "dog", "at": field}) or any(
        (b.get("fittings") or {}).get("dog") for b in w.s["buildings"].values())
    w.apply("create", "s1", dst=w.hands("Tom"), item="firewood", qty=3)
    r = _do(w, "Tom", {"do": "work", "what": "guard the field", "looking for": "fire", "at": field})
    assert "efused" not in r and w.goods(w.hands("Tom")).get("firewood", 0) < 3


def test_the_vole_phase_clock_steps_a_year_at_a_time_in_order():
    from cybertron2.wild import ecology as EC, kinds as K
    from cybertron2.landgen import write as W_
    world = W_.generate({"name": "t", "seed": 7, "days": 10, "calendar": {"season": "spring", "day": 1, "season_days": 8},
                         "generate": {"seed": 7, "configuration": "settled lowland and frontier", "spacing_km": 8.0, "settlements": 4}})[0]
    world.setdefault("agents", {})
    w = build(world, history=1)
    from cybertron2.engine import wild as WL
    m = WL.model(w)
    st = copy.deepcopy(w.s["wild"]["state"])
    Y = w.year_days()
    seen = []
    for y in range(6):
        for d in range(Y):
            EC.step(m, st, y * Y + d, WL.weather(w, sorted(set(m.nodes)), 300 * Y + y * Y + d), WL.draws(w, y * Y + d, "t"))
        seen.append(st["phase"]["voles and mice"])
    order = K.PHASES["voles and mice"]["order"]
    steps = [(order.index(b) - order.index(a)) % len(order) for a, b in zip(seen, seen[1:])]
    assert all(s_ in (0, 1, 2) for s_ in steps) and len(set(seen)) >= 3


def test_a_night_on_watch_costs_food_and_tomorrows_work(generated):
    """D2-21: a field watch gives up the night's sleep: it eats the guard's food and leaves one tired tomorrow."""
    from cybertron2.engine import run as R, labour as LB
    w, WL = _summer_world(_two(generated))
    w.s["today"] = R.blank_today()
    field = w.s["parcels"][WL._fields(w, "s1")[0]]["name"]
    w.apply("create", "s1", dst=w.hands("Tom"), item="firewood", qty=3)
    _do(w, "Tom", {"do": "work", "what": "guard the field", "looking for": "fire", "at": field})
    assert "Tom" in w.s["today"]["night_watch"]
    assert LB.work_need(w.p, w.s["today"], "Tom") >= float(w.p["labour"]["guard_food"])
    LB.close_day(w, w.s["today"], {"Tom": 2}, {"Tom": 6}, ["Tom"])
    assert (w.s["people"]["Tom"].get("tired") or {}).get("units", 0) >= int(w.p["labour"]["watch_tired"])
