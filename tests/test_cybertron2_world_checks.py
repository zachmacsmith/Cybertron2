"""A craft someone is given can be done where they live (world_checks.gates, W-58)."""
import copy
from pathlib import Path

import yaml

from cybertron2 import world_checks as WC

RUNS = yaml.safe_load((Path(__file__).resolve().parents[1] / "cybertron2/specs/water/runs_models.yaml").read_text())


def test_the_salter_without_a_pan_is_caught():
    bad = WC.gates(RUNS)
    assert any(hh == "Brook" and craft == "boil salt" for hh, _, craft, _ in bad)


def test_a_pan_in_the_village_opens_the_gate():
    w = copy.deepcopy(RUNS)
    w["buildings"]["salthouse"] = {"parcel": "Highpool_7", "household": "Brook", "structure": "wattle", "fittings": {"brine pan": 1}}
    assert not any(craft == "boil salt" for _, _, craft, _ in WC.gates(w))
