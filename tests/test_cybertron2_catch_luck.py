"""A catch by hand or by rod has luck in it (Zach, 17 Nov): a draw about the same mean as before, at most what the stock can give;
other stock yields are unchanged; a lake's fish are sized by its area with a slow regrowth (make_water_worlds.water_stocks)."""
import random
import statistics

from cybertron2.engine import yields as YD
from cybertron2.engine.data import TECHNIQUES


def test_hand_fishing_varies_about_the_same_mean():
    y = TECHNIQUES["fish by hand"]["yield"]
    r = {"S": 50.0, "K": 100.0}
    rng = random.Random(3)
    d = YD.dist(y, r, 1.0, 1.0)
    xs = [d.sample(rng) for _ in range(4000)]
    want = y["base"] * 0.5
    assert abs(statistics.mean(xs) - want) < 0.02 * want + 0.01
    assert min(xs) < 0.8 * want and max(xs) > 1.2 * want           # luck either way
    assert abs(d.mean() - want) < 1e-9                              # the capacity model reads the same mean


def test_the_catch_never_takes_the_stock_below_its_refuge():
    y = TECHNIQUES["angle"]["yield"]
    r = {"S": 10.4, "K": 100.0}
    rng = random.Random(1)
    assert max(YD.dist(y, r, 3.0, 1.0, refuge=0.1).sample(rng) for _ in range(500)) <= 0.4 + 1e-9


def test_gathering_wild_food_is_unchanged():
    y = TECHNIQUES["forage"]["yield"] if "forage" in TECHNIQUES and TECHNIQUES["forage"]["yield"]["kind"] == "stock" else \
        next(t["yield"] for t in TECHNIQUES.values() if t.get("yield", {}).get("kind") == "stock" and not t["yield"].get("spread"))
    d = YD.dist(y, {"S": 5.0, "K": 10.0}, 1.0, 1.0)
    assert d.sample(random.Random(0)) == d.sample(random.Random(9))   # a fixed amount


def test_a_lake_holds_fish_by_area_and_regrows_slowly():
    import yaml
    d = yaml.safe_load(open("cybertron2/specs/water/lake.yaml"))
    fish = [p["state"]["fish"] for nd in d["nodes"].values() for p in nd["parcels"].values() if p["cover"] == "water"]
    mere = max(fish, key=lambda f: f["K"])
    assert mere["K"] > 5000 and mere["r"] < 0.01 and mere.get("renewal") == "threshold"
