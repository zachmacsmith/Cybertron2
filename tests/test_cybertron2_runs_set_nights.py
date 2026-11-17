"""D2-231: a world with the climate on may run its runs on their windows' set nights (`runs_set_nights`), the rest of the weather
unchanged; without the setting the runs keep their weather cue."""
import copy

import yaml

from cybertron2.engine import night as N, wild as WL
from cybertron2.engine.world import World
from cybertron2.wild import runs as RU

RIVER = "cybertron2/specs/water/river.yaml"


def _cued_flags(monkeypatch, spec):
    seen = []
    real = RU.advance

    def spy(*a, **k):
        seen.append(k.get("weather"))
        return real(*a, **k)
    monkeypatch.setattr(RU, "advance", spy)
    w = World(copy.deepcopy(spec))
    N.night(w)
    return w, seen


def test_the_runs_keep_their_cue_by_default(monkeypatch):
    spec = yaml.safe_load(open(RIVER))
    w, seen = _cued_flags(monkeypatch, spec)
    assert WL._climate(w) and seen and all(seen)


def test_set_nights_with_the_climate_on(monkeypatch):
    spec = yaml.safe_load(open(RIVER))
    spec["runs_set_nights"] = True
    w, seen = _cued_flags(monkeypatch, spec)
    assert WL._climate(w)                                      # the weather is still drawn
    assert seen and not any(seen)                              # the runs go on set nights
