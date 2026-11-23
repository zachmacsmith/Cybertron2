"""The five designed worlds moved to cybertron2/specs/mono_design.py (W-107); this name kept for draw.py and topology.py."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from cybertron2.specs.mono_design import *  # noqa: E402,F401,F403
from cybertron2.specs.mono_design import CROSS, FEATURES, LAND, ROOM_BY_LAND, ROOM_SET, TREE_BY_DESIGN, WORLDS  # noqa: E402,F401
