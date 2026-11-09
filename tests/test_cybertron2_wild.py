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
