"""The backward people build as a world's people stage (W-107; generation_redesign.md §6): the forward build unchanged, the
backward one opt-in, its present met, its tree consistent, written in generate.py's form, and the pipeline around it (landgen,
livelihoods.fill, the engine) running on it."""
import copy
import os
import sys

import pytest
import yaml

from cybertron2.engine import generate as GEN
from cybertron2.engine import livelihoods as LV
from cybertron2.peoplegen import world as PW

SPECS = os.path.join(os.path.dirname(__file__), "..", "cybertron2", "specs")


def base(name):
    return yaml.safe_load(open(os.path.join(SPECS, name)))


def backward(name, **pop):
    b = base(name)
    b["population"] = {"build": "backward", **pop}
    return b


def h(x):
    import hashlib
    import json
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------- the forward build is unchanged
@pytest.mark.parametrize("name,seed,want", [("hamlet.yaml", 1, "51aa163ca9313055"), ("hamlet.yaml", 3, "85516b41677ef679"),
                                            ("two_valleys.yaml", 1, "f84ce3a3345c6980"), ("valley.yaml", 2, "f05f613dad49db61")])
def test_the_forward_build_writes_what_it_wrote_before_the_split(name, seed, want):
    """Hashes taken on main before generate.build was split (W-107): the split changes no world."""
    assert h(GEN.build(base(name), seed)) == want


def test_a_world_without_population_is_built_forward():
    assert GEN.build(base("hamlet.yaml"), 1)["generated"].get("build") is None


# ---------------------------------------------------------------------- the backward build
@pytest.fixture(scope="module")
def region():
    return GEN.build(backward("region.yaml"), 1)


def test_the_backward_build_gives_every_household_people_and_a_head(region):
    lines = set(base("region.yaml")["lines"])
    A = region["agents"]
    assert {a["household"] for a in A.values()} == lines
    heads = [a["household"] for a in A.values() if a.get("role") == "head"]
    assert sorted(heads) == sorted(lines)
    assert region["generated"]["build"] == "backward"


def test_the_same_world_and_seed_give_the_same_people(region):
    assert h(GEN.build(backward("region.yaml"), 1)) == h(region)
    assert h(GEN.build(backward("region.yaml"), 2)) != h(region)


def test_the_tree_is_consistent(region):
    T = {t["name"]: t for t in region["tree"]}
    for n, t in T.items():
        for p in t["parents"]:
            assert p in T and T[p]["born"] < t["born"], (n, p)
            if T[p]["sex"] == "f" and T[p]["died"] is not None:
                assert T[p]["died"] >= t["born"], (n, p)
        for k in t["children"]:
            assert n in T[k]["parents"]
    for n, a in region["agents"].items():
        assert T[n]["died"] is None and T[n].get("left") is None
        assert a["household"] == T[n]["line"]


def test_an_agents_partner_is_living_and_a_dead_one_is_widowed_of(region):
    A = region["agents"]
    T = {t["name"]: t for t in region["tree"]}
    for n, a in A.items():
        if a.get("partner"):
            assert a["partner"] in A and A[a["partner"]].get("partner") == n
        if a.get("widowed_of"):
            assert a["widowed_of"] not in A and T[a["widowed_of"]]["died"] is not None


def test_villages_are_founded_in_an_order_each_daughter_from_an_older_one(region):
    g = region["generated"]
    for v, m in g["budded_from"].items():
        assert g["foundings"][m] <= g["foundings"][v]
    names = {n["name"] for n in base("region.yaml")["nodes"].values()}
    assert set(g["foundings"]) <= names                                      # told by the villages' names, not their ids
    assert all(" s1 " not in f" {x['text']} " for x in region["history"])


def test_a_pinned_household_is_met_exactly():
    pin = {"Reed": {"members": [{"age": 46, "sex": "m", "role": "head", "name": "Osric"}, {"age": 44, "sex": "f", "role": "spouse"}] +
                    [{"age": a, "sex": "mf"[k % 2]} for k, a in enumerate([24, 22, 20, 18, 16, 13, 11, 8, 5])]},
           "Cole": {"form": "widow_alone"}}
    b = backward("region.yaml", households=pin)
    if "Reed" not in b["lines"]:
        pytest.skip("region.yaml has no Reed line")
    w = GEN.build(b, 1)
    reed = sorted((-a["born"], a["sex"]) for a in w["agents"].values() if a["household"] == "Reed")
    assert len(reed) == 11 and w["agents"]["Osric"]["role"] == "head"
    cole = [n for n, a in w["agents"].items() if a["household"] == "Cole"]
    assert len(cole) == 1 and w["agents"][cole[0]].get("partner") is None


def test_an_impossible_pin_is_refused_by_name():
    pin = {"Reed": {"members": [{"age": 25, "sex": "m", "role": "head"}, {"age": 15, "sex": "f", "role": "child"}]}}
    b = backward("region.yaml", households=pin)
    if "Reed" not in b["lines"]:
        pytest.skip("region.yaml has no Reed line")
    with pytest.raises(RuntimeError, match="pin:role"):
        GEN.build(b, 1)


def test_spouses_who_married_in_carry_where_they_came_from(region):
    origins = {t.get("origin") for t in region["tree"]} - {None}
    assert origins and "Ashby" not in origins                               # no bare made-up place (generation_redesign §3)


def test_roads_give_the_distances():
    b = base("region.yaml")
    home = PW.homes(b)
    d = PW.road_days(b, sorted(set(home.values())))
    assert d and all(v > 0 for v in d.values())
    for k, v in d.items():
        x, y = k.split("|")
        assert d[f"{y}|{x}"] == v


# ---------------------------------------------------------------------- the pipeline around it
@pytest.fixture(scope="module")
def generated():
    sys.path.insert(0, os.path.dirname(__file__))
    import test_cybertron2_landgen as TL
    from cybertron2.landgen import write as W
    s = TL.spec(households=[3, 3])
    s["population"] = {"build": "backward"}
    return W.generate(copy.deepcopy(s), people=True)


def test_landgen_builds_a_world_with_backward_people(generated):
    w, _, report = generated
    assert not report["refused"]
    assert report["checks"]["capacity, people as generated"]["ok"]
    assert (w["generated"]["people"] or {}).get("build") == "backward"
    for b in w["buildings"].values():                                        # a bed each and one spare (D4-86)
        n = sum(1 for a in w["agents"].values() if a["household"] == b.get("household"))
        if (b.get("fittings") or {}).get("beds") and n:
            assert b["fittings"]["beds"] >= n


def test_the_livelihoods_fill_runs_on_it(generated):
    w = copy.deepcopy(generated[0])
    hh = sorted({a["household"] for a in w["agents"].values()})
    w["skills"] = {"depth": "full", "households": {x: {"livelihoods": ["farmer"]} for x in hh}}
    rep = LV.fill(w)
    assert not rep["refused"]
    grown = [a for a in w["agents"].values() if a["stage"] in ("youth", "adult", "elder")]
    assert grown and all(a.get("band") for a in grown) and any(a.get("kept") for a in grown)
    assert not any("came to blows" in k["text"] and "founders" in k["text"] for a in w["agents"].values() for k in a.get("kept") or [])


def test_the_engine_runs_it(generated, tmp_path):
    from cybertron2.engine import run as R
    from cybertron2.engine.world import World
    w = copy.deepcopy(generated[0])
    widows = [n for n, a in w["agents"].items() if a.get("widowed_of")]
    world = World(copy.deepcopy(w))
    for n in widows:
        assert world.s["people"][n]["widowed_of"] == w["agents"][n]["widowed_of"]
    p = tmp_path / "w.yaml"
    yaml.safe_dump(w, open(p, "w"), sort_keys=False, allow_unicode=True)
    R.run(str(p), str(tmp_path / "out"), days=2, bots=True)


def test_a_craft_brought_by_marriage_warns_at_the_making_check_and_never_refuses(generated):
    """D2-350: smelting known only by a wife born into another house, with no ore within a day, warns; the same craft known by one
    born into the house refuses as before."""
    from cybertron2.engine.world import World
    from cybertron2.landgen import gates as G
    w = copy.deepcopy(generated[0])
    A = w["agents"]
    wife = next((n for n, a in A.items() if a.get("born_line") and a["born_line"] != a["household"] and a["stage"] == "adult"), None)
    if wife is None:
        pytest.skip("no spouse married in from another house in this world")
    hh = A[wife]["household"]
    A[wife].setdefault("knows", {})["smelt"] = {"level": "known", "skill": 1.0}
    world = World(copy.deepcopy(w))
    m1 = [f for f in G.making_gates(world) if f.check == "M1" and f.household == hh and "smelt" in f.text.lower()]
    assert m1 and all(f.level == "warn" and "brought by marriage" in f.text for f in m1)
    native = next(n for n, a in A.items() if a["household"] == hh and (a.get("born_line") or hh) == hh and a["stage"] == "adult")
    A[native].setdefault("knows", {})["smelt"] = {"level": "known", "skill": 1.0}
    world = World(copy.deepcopy(w))
    m1 = [f for f in G.making_gates(world) if f.check == "M1" and f.household == hh and "smelt" in f.text.lower()]
    assert m1 and all(f.level == "refuse" for f in m1)
