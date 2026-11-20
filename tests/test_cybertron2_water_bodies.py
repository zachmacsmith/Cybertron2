"""One fish stock a water body (D2-229; cybertron2/engine/waters.py): a lake's resident fish held once, fished from every water parcel
on it, renewed once a night, counted once by the capacity model; a world without a waters list unchanged."""
import copy
import json

import pytest
import yaml

from cybertron2.capacity import model as CM
from cybertron2.engine import night as N, renewal as RN, run as R, verbs as V, waters as WA
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

LAKE = "cybertron2/specs/water/lake.yaml"


@pytest.fixture(scope="module")
def lake():
    return yaml.safe_load(open(LAKE))


def _world(spec):
    w = World(copy.deepcopy(spec))
    w.s["today"] = R.blank_today()
    return w


def _mere(w):
    bid, b = next((k, v) for k, v in w.s["waters"].items() if v["kind"] == "lake" and "fish" in v)
    return bid, b, b["parcels"]


def test_two_parcels_on_one_lake_share_one_stock(lake):
    w = _world(lake)
    bid, b, pids = _mere(w)
    assert len(pids) >= 2
    own = [lake["nodes"][w.s["parcels"][p]["node"]]["parcels"][p]["state"]["fish"] for p in pids]
    assert b["fish"]["K"] == pytest.approx(sum(float(x["K"]) for x in own))            # sized by the whole lake's parcels
    assert all(w.s["parcels"][p]["res"]["fish"] is b["fish"] for p in pids)            # one record, not copies
    assert [p for p in pids if WA.lead(w, p, "fish")] == [pids[0]]


def test_fishing_at_either_parcel_lowers_the_one_stock(lake):
    w = _world(lake)
    bid, b, pids = _mere(w)
    who = next(n for n in sorted(w.living()) if w.s["people"][n]["stage"] == "adult" and w.s["people"][n]["at"] == w.s["parcels"][pids[0]]["node"])
    before = b["fish"]["S"]
    for p in pids:
        r = V.do(Here(w, who), Mind(w, who), {"do": "gather", "what": "fish by hand", "at": w.s["parcels"][p]["name"]})
        assert "fish" in r, r
    assert b["fish"]["S"] < before
    assert all(w.s["parcels"][p]["res"]["fish"]["S"] == b["fish"]["S"] for p in pids)


def test_the_body_regrows_once_a_night(lake):
    w = _world(lake)
    bid, b, pids = _mere(w)
    b["fish"]["S"] = round(b["fish"]["K"] * 0.5, 4)
    par = w.s["parcels"][pids[0]]
    ctx = RN.context(w, par, winter=N.slow_season(w.calendar()["season"]), season=w.calendar()["season"])
    once = RN.RULES[RN.of("fish", b["fish"])](w.p, dict(b["fish"]), ctx)
    N._grow(w) if hasattr(N, "_grow") else N.night(w)
    assert b["fish"]["S"] == pytest.approx(once)                                        # one step, not one per parcel


def test_the_capacity_model_counts_a_body_once(lake):
    w = _world(lake)
    bid, b, pids = _mere(w)
    ctx = CM.context(w, "standing")
    fish = [f for f in CM.flows(ctx) if f.where in pids and f.note.startswith("fish")]
    assert len({f.where for f in fish}) == 1 and fish[0].where == pids[0]


def test_a_restored_world_holds_one_record_again(lake):
    w = _world(lake)
    bid, b, pids = _mere(w)
    w.s = json.loads(json.dumps(w.s))                                                   # as a checkpoint gives it back
    assert w.s["parcels"][pids[0]]["res"]["fish"] is not w.s["parcels"][pids[1]]["res"]["fish"]
    WA.link(w)
    assert all(w.s["parcels"][p]["res"]["fish"] is w.s["waters"][bid]["fish"] for p in pids)


def test_a_world_without_waters_is_unchanged():
    spec = load_spec("cybertron2/specs/fishing/water.yaml")
    assert not ((spec.get("wild") or {}).get("land") or {}).get("waters")
    w = World(copy.deepcopy(spec))
    assert "waters" not in w.s
    fishy = [p for p, x in w.s["parcels"].items() if "fish" in x["res"]]
    assert fishy and len({id(w.s["parcels"][p]["res"]["fish"]) for p in fishy}) == len(fishy)
    assert all(WA.lead(w, p, "fish") for p in fishy)


def test_the_wild_fish_on_a_body_follow_its_stock(lake):
    """The default taken (OPEN L-116): before the night's food web, each area on the body holds fish at its cap x the body's
    fullness, so people's fishing thins the fish the wild kinds find there."""
    from cybertron2.engine import wild as WL
    w = _world(lake)
    bid, b, pids = _mere(w)
    m = WL.model(w)
    st = copy.deepcopy(w.s["wild"]["state"])
    b["fish"]["S"] = round(b["fish"]["K"] * 0.25, 4)
    WA.to_wild(w, m, st)
    cap = m.cap("fish")
    for a in b["areas"]:
        i = m.ids.index(a)
        assert st["stock"]["fish"][i] == pytest.approx(float(cap[i]) * 0.25, abs=0.01)
