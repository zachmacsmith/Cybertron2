"""Seed the water worlds made before the wave with wicker traps and their making (Q-100, Zach 24 Nov; W-111).

Since the wave, setting traps lays wicker traps from the hands and making them is a craft (W-98), and these worlds seeded neither,
so nobody in them could trap (wave_regressions.md finding 1). This applies D2-330's C5 as the runs arms do
(make_nutrition_runs.seed_traps): each trap-setter knows the making at the setting's level; each capable or known setter holds six.
Idempotent; the rest of each file is written back unchanged.

    python3 -m cybertron2.specs.seed_water_traps cybertron2/specs/water/{river,lake,lake_goal,runs,runs_models}.yaml
"""
from __future__ import annotations

import sys

import yaml

from cybertron2.specs.make_nutrition_runs import seed_traps

NOTE = "# Wicker traps and their making seeded by cybertron2/specs/seed_water_traps.py (Q-100, W-111, 24 Nov 2026).\n"


def seed_file(path: str) -> dict:
    text = open(path).read()
    lines = text.splitlines(True)
    head = "".join(x for x in lines[:next(i for i, x in enumerate(lines) if not x.startswith("#"))] if x != NOTE)
    world = yaml.safe_load(text)
    out = seed_traps(world)
    with open(path, "w") as f:
        f.write(head + NOTE)
        yaml.safe_dump(world, f, sort_keys=False, allow_unicode=True, width=140)
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, seed_file(p))
