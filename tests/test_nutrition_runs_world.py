"""The runs-only nutrition world (W-69, D2-256): a seeded weir keeps its sections, and the three arms load."""
import os
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from cybertron2.engine import wild as WL  # noqa: E402
from cybertron2.engine.world import World  # noqa: E402

DIR = os.path.join(ROOT, "cybertron2", "specs", "nutrition")


def _world(arm):
    with open(os.path.join(DIR, f"runs_{arm}.yaml")) as f:
        return World(yaml.safe_load(f))


def test_seeded_weir_keeps_its_sections():
    w = _world("high")
    weirs = [b for b in w.s["buildings"].values() if b.get("monument") == "weir"]
    assert len(weirs) == 1
    assert [s["m"] for s in WL.sections(weirs[0])] == ["timber", "timber", "timber"]   # the first in timber too (W-69, 20 Nov)
    crew = weirs[0]["crew"]                                                              # its crew: the holders' adults who know it
    assert crew and all(w.s["know"][n].get("weir") and w.s["people"][n]["stage"] == "adult" for n in crew)


def test_arms_differ_only_in_skill_and_capital():
    lo, hi = _world("low"), _world("high")
    assert sorted(lo.s["people"]) == sorted(hi.s["people"])
    assert not any(b.get("monument") == "weir" for b in lo.s["buildings"].values())
    assert not any((b.get("fittings") or {}).get("brine pan") for b in lo.s["buildings"].values())
    assert any((b.get("fittings") or {}).get("brine pan") for b in hi.s["buildings"].values())


def test_nothing_farmed():
    w = _world("medium")
    assert not any(p["cover"] == "field" for p in w.s["parcels"].values())
    assert not w.s["herds"]
