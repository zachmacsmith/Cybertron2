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


def test_the_weather_is_the_seeds_alone_and_the_same_in_every_arm():
    a, b = world(), world()
    b.s["people"] = {}                                                           # an arm with nobody in it: the same weather
    assert [CL.env(a, n, d) for n in CL._nodes(a) for d in range(60)] == [CL.env(b, n, d) for n in CL._nodes(b) for d in range(60)]
    c = world(seed=REGION["seed"] + 1)
    assert [CL.label(a, None, d) for d in range(60)] != [CL.label(c, None, d) for d in range(60)]
    json.dumps([CL.env(a, n, d) for n in CL._nodes(a) for d in range(5)])     # plain values: they go into the record


def test_labels_are_the_engines_and_off_is_the_old_weather():
    w = world()
    assert {CL.label(w, n, d) for n in CL._nodes(w) for d in range(160)} <= set(WEATHER)
    s = copy.deepcopy(REGION)
    s.pop("climate", None)
    old = World(s)
    assert not CL.on(old) and EV.spell(old, 3) == "normal"
    assert old.cold(0) == (old.calendar(0)["season"] == "winter")


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
    ref = CL.reference(w)
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
            out.append(np.mean([CL.env(w, None, d)[key] for d in range(160)]))
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
    assert w.cold(d, a) and not w.cold(d, b)
