"""The weather scheduler (D4-109; engine/climate.py): weather from the seed only, alike between near places, by the season and the
era, read by the night and the land; off, the engine is as it was."""
import copy
import json

import numpy as np

from cybertron2.engine import climate as CL, environment as EV, night as N, run as R
from cybertron2.engine.data import WEATHER
from cybertron2.engine.world import World, load_spec

REGION = load_spec("cybertron2/specs/region_c_s27.yaml")


def world(era="steady", days=160, seed=None, **climate):
    s = copy.deepcopy(REGION)
    s["climate"] = {"era": era, **climate}
    s["days"] = days
    if seed is not None:
        s["seed"] = seed
    return World(s)


def home(w):
    """A place to read the weather at in a test: the node with most people (named here, never an engine default: D4-111)."""
    count = {}
    for a in w.s["people"].values():
        count[a.get("at")] = count.get(a.get("at"), 0) + 1
    return max(sorted(w.s["nodes"]), key=lambda n: count.get(n, 0))


def test_the_weather_is_the_seeds_alone_and_the_same_in_every_arm():
    a, b = world(), world()
    b.s["people"] = {}                                                           # an arm with nobody in it: the same weather
    assert [CL.env(a, n, d) for n in CL._nodes(a) for d in range(60)] == [CL.env(b, n, d) for n in CL._nodes(b) for d in range(60)]
    c = world(seed=REGION["seed"] + 1)
    assert [CL.label(a, home(a), d) for d in range(60)] != [CL.label(c, home(a), d) for d in range(60)]
    json.dumps([CL.env(a, n, d) for n in CL._nodes(a) for d in range(5)])     # plain values: they go into the record


def test_labels_are_the_engines_and_off_is_the_old_weather():
    w = world()
    assert {CL.label(w, n, d) for n in CL._nodes(w) for d in range(160)} <= set(WEATHER)
    s = copy.deepcopy(REGION)
    s.pop("climate", None)
    old = World(s)
    assert not CL.on(old) and EV.spell(old, 3) == "normal"
    assert all(old.cold(n, 0) == (old.calendar(0)["season"] == "winter") for n in old.s["nodes"])


def test_near_places_share_weather_more_than_far_ones():
    w = world(days=320)
    ns = CL._nodes(w)
    D = CL._distances(w, CL.params(w))
    wet = np.array([[CL.env(w, n, d)["rain"] > 0 for n in ns] for d in range(320)], dtype=float)
    pairs = sorted((D[i, j], np.corrcoef(wet[:, i], wet[:, j])[0, 1]) for i in range(len(ns)) for j in range(i + 1, len(ns)))
    near = [c for d, c in pairs if d <= 30]
    far = [c for d, c in pairs if d >= 70]
    assert near and far and np.mean(near) > np.mean(far) + 0.05 and np.mean(near) > 0.6


def test_the_seasons_and_the_height_shape_it():
    w = world(days=320)
    ref = home(w)
    frost = {s: [] for s in ("spring", "summer", "autumn", "winter")}
    for d in range(320):
        frost[w.calendar(d)["season"]].append(CL.frost(w, ref, d))
    assert sum(frost["winter"]) > 0.3 * len(frost["winter"]) and sum(frost["summer"]) == 0
    hi, lo = max(CL._nodes(w), key=lambda n: CL.state(w).height[n]), min(CL._nodes(w), key=lambda n: CL.state(w).height[n])
    assert np.mean([CL.env(w, hi, d)["temp"] for d in range(320)]) < np.mean([CL.env(w, lo, d)["temp"] for d in range(320)])


def test_eras_move_the_years_as_their_rows_say():
    def year(era, key):
        out = []
        for s in (1, 2, 3, 4):
            w = world(era, 160, seed=s)
            out.append(np.mean([CL.env(w, home(w), d)[key] for d in range(160)]))
        return np.mean(out)
    rain = lambda era: year(era, "rain")                                         # noqa: E731
    temp = lambda era: year(era, "temp")                                         # noqa: E731
    assert rain("dry") < rain("steady") < rain("wet")
    assert temp("cold") < temp("steady") - 0.4
    w = world("dry", days=640, moves=True, era_pace=16)
    assert len({CL.state(w).year(i)["era"] for i in range(20)}) > 1               # a long run's era moves on, fast at a high pace
    assert {CL.state(world("dry", 640)).year(i)["era"] for i in range(20)} == {"dry"}   # else it holds (D2-73)


def test_the_night_reads_each_places_own_weather_and_records_it():
    w = world()
    w.s["today"] = R.blank_today()
    rec = N.night(w)
    assert set(rec["weather"]) == set(w.s["nodes"]) and all(v["label"] in WEATHER for v in rec["weather"].values())
    days = [d for d in range(160) if len({CL.frost(w, n, d) for n in CL._nodes(w)}) > 1]
    assert days                                                                   # some nights freeze in one place and not another
    d = days[0]
    a, b = [n for n in CL._nodes(w) if CL.frost(w, n, d)][0], [n for n in CL._nodes(w) if not CL.frost(w, n, d)][0]
    assert w.cold(a, d) and not w.cold(b, d)


def test_what_the_senses_get_follows_the_days_values():
    """D4-111: rain dims sight by the mm, wind masks sound; the graded signs follow the values."""
    from cybertron2.engine import signs as SG
    from cybertron2.engine.here import Here
    w = world(days=320)
    ref = home(w)
    days = range(320)
    wet = [d for d in days if CL.env(w, ref, d)["rain"] >= 8 and CL.label(w, ref, d) != "snow"]
    dry = [d for d in days if CL.env(w, ref, d)["rain"] == 0 and not CL.env(w, ref, d)["fog"]]
    assert CL.vis(w, ref, "sight", wet[0]) < CL.vis(w, ref, "sight", dry[0]) == 1.0
    windy = max(days, key=lambda d: CL.env(w, ref, d)["wind"])
    calm = min(days, key=lambda d: CL.env(w, ref, d)["wind"])
    assert CL.vis(w, ref, "sound", windy) < CL.vis(w, ref, "sound", calm)
    w.s["day"] = wet[0]
    from cybertron2.engine.data import COVERS
    assert abs(EV.visibility(w, ref, None, "sight") - float(COVERS["built"]["sight"]) * CL.vis(w, ref, "sight", wet[0])) < 1e-9
    hot = [d for d in days if CL.env(w, ref, d)["temp"] >= 22]
    if hot:
        w.s["day"] = hot[0]
        name = next(n for n, a in w.s["people"].items() if a.get("at") == ref and a.get("alive", True))
        x = SG.sky_context(Here(w, name))
        assert any(r["when"](x) and "hot" in r["text"](x) for r in SG.SKY)


def test_every_weather_query_names_its_place():
    """D4-111: no region-wide default and no reference node; a road reads the mean of its ends; on or off the same rule."""
    import pytest
    for w in (world(days=40), World(REGION)):
        for call in (lambda: EV.weather(w, None), lambda: EV.wet(w, 3), lambda: w.cold(None), lambda: w.cold(0),
                     lambda: EV.snow_lying(w, None), lambda: EV.words(w, None)):
            with pytest.raises(ValueError):
                call()
    w = world(days=40)
    assert not hasattr(CL, "reference")
    rid, r = next(iter(w.s["roads"].items()))
    for d in range(10):
        a, b, m = CL.env(w, r["a"], d), CL.env(w, r["b"], d), CL.env(w, rid, d)
        assert abs(m["temp"] - (a["temp"] + b["temp"]) / 2) < 1e-2 and m["storm"] == max(a["storm"], b["storm"])
        assert EV.weather(w, rid, d) in WEATHER


def test_a_run_with_the_scheduler_reads_every_place_it_touches(tmp_path):
    """Bots for some days with the scheduler on: every call site the day and the night reach names a place (a missed one raises)."""
    import yaml
    s = copy.deepcopy(REGION)
    s["climate"] = {"era": "stormy"}
    s["days"] = 6
    p = tmp_path / "s.yaml"
    p.write_text(yaml.safe_dump(s))
    R.run(str(p), str(tmp_path / "out"), days=6, bots=True)                  # raises if any call site names no place


def test_renewal_rules_get_the_weather_where_the_stock_is():
    """D4-113: the night hands each stock's rule its parcel's weather (frost, snow, wet, values, the year's anomaly, the land); the
    rules that exist read none of it, so the stocks come back as before."""
    from cybertron2.engine import renewal as RN
    w = world(days=40)
    pid, par = next((k, p) for k, p in w.s["parcels"].items() if p["res"])
    c = RN.context(w, par, winter=False, season="spring")
    assert c["place"] == par["node"] and c["frost"] == w.cold(par["node"]) and c["weather"] == {
        k: CL.env(w, par["node"], w.d)[k] for k in ("temp", "low", "rain", "wind", "storm")}
    assert set(c["anomaly"]) == {"temp", "wet", "era"} and c["winter"] is False
    seen = []
    RN.RULES["_probe"] = lambda p, res, ctx: seen.append(ctx) or res["S"]
    try:
        key = next(iter(par["res"]))
        par["res"][key]["renewal"] = "_probe"
        RN.NIGHTLY += ("_probe",)
        N._grow(w)
        assert seen and seen[0]["place"] == par["node"] and "weather" in seen[0]
    finally:
        RN.RULES.pop("_probe")
        RN.NIGHTLY = tuple(x for x in RN.NIGHTLY if x != "_probe")
        par["res"][key].pop("renewal")
    off = World(REGION)
    assert RN.context(off, next(iter(off.s["parcels"].values())))["weather"] is None
