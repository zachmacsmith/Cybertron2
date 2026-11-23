"""Stage 1 of the fishing, hunting and materials wave: the basis in code (W-97; docs/cybertron2/proposals/w73_design/u0_basis.md).
One test (or a few) for each fault fixed and each rule built: the options list gone (D2-286), the fishing faults (u2 §6), a run's fish
learning no wariness (u1 §7a), the weir's cost in one place (D2-302), practice for every build act (u7 §5.2), the signs reworded
(D2-269), the clocks (u0 §4), the floor and batches (u0 §5), the keeping curve (D2-289), fuel a night (D2-290) and the handling units
(D2-288)."""
import copy

import pytest

from cybertron2.engine import knowledge as KN, prompt as PR, run as R
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec


@pytest.fixture(scope="module")
def hamlet():
    w = World(load_spec("cybertron2/specs/valley_s5.yaml"))
    w.s["today"] = R.blank_today()
    return w


# ---------------------------------------------------------------------- the options list (D2-286)
def test_no_prompt_contains_the_options_list(hamlet):
    w = copy.deepcopy(hamlet)
    assert not hasattr(KN, "options")                                            # gone from the code, not only hidden
    for name, p in sorted(w.s["people"].items()):
        if not p.get("alive", True) or p.get("stage") != "adult":
            continue
        for opening in (True, False):
            text = PR.turn_prompt(Here(w, name), Mind(w, name), opening)
            assert "Today you could" not in text and "Not yet:" not in text
