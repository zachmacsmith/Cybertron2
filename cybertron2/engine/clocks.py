"""Every rate names its clock (D4-103; proposals/process_model.md, "Clocks").

Days are the tick and the unit agents live in. Three clocks:
- day:  a rate a night (eating, spoiling, breaks, a fire's fuel, a stock's nightly regrowth r);
- year: a share of the year or a rate a year (crops' growing share, the woods' growth, beasts' births and dung, milk's share of the
        year, a fallow slot's restoring);
- life: a share of a lifespan (life.py scales its ages and durations by the lifespan);
and `use` and `event` for what counts uses or occasions, not time.

The two exchange rates are world settings: days a year (World.year_days) and the lifespan in days (life.lifespan). RATES lists every
rate in the data with its clock; tests/test_cybertron2_clocks.py fails on a rate-like field the list does not name. Phase 1 names
the clocks as the engine already uses them; phase 2 (calibration) converts year rates through the year's length where the engine
now assumes one (forests.seed's 24).
"""
from __future__ import annotations

import fnmatch

RATES = [
    # the day clock: a night's share or chance
    ("ITEMS.*.spoil", "day"), ("DECAY.*.abs.*", "day"), ("PHYSICS.breaks.p", "day"), ("PHYSICS.breaks.cold", "day"),
    ("PHYSICS.farming.rot", "day"), ("PHYSICS.farming.window", "day"), ("PHYSICS.cattle.grass_r", "day"),
    ("TECHNIQUES.*.set.life", "day"),                                     # a set snare or trap lasts so many nights (brief 2)
    ("PHYSICS.cattle.stray", "day"), ("PHYSICS.cattle.starve_nights", "day"), ("PHYSICS.fuel.*", "day"), ("PHYSICS.heat.*", "day"),
    ("RESOURCES.*.r", "day"),
    # the year clock
    ("CROPS.*.share", "year"), ("FORESTS.kinds.*.grow", "year"), ("FORESTS.kinds.*.regrow", "year"), ("FORESTS.shed", "year"),
    ("FORESTS.rot", "year"), ("PHYSICS.cattle.births", "year"), ("PHYSICS.cattle.dung", "year"),
    ("PHYSICS.cattle.in_milk_share", "year"), ("PHYSICS.farming.fallow", "year"),
    ("FENCES.*.mend", "year"),                                          # a fence's mending a year (D4-114)
    # occasions and uses
    ("FORESTS.gale", "event"), ("PHYSICS.cattle.survive", "event"), ("PHYSICS.cattle.hungry_milk", "event"),
    ("PHYSICS.labour.work_food", "use"), ("PHYSICS.labour.over_food", "use"), ("PHYSICS.labour.step", "use"),
    ("PHYSICS.labour.guard_food", "event"), ("PHYSICS.labour.fade_rate", "year"), ("PHYSICS.labour.fade_after", "year"),
    ("FITTINGS.*.wear.life", "use"), ("FITTINGS.*.wear.years", "year"),
    ("FITTINGS.*.spoil", "day"), ("FITTINGS.*.dung", "year"),           # multipliers of a day's spoiling and a year's dung
    ("ITEMS.*.life", "use"), ("TECHNIQUES.*.wear", "use"), ("TECHNIQUES.*.yield.p", "use"), ("TECHNIQUES.*.inputs.*", "use"),
]
KNOWN_LATER: set = set()             # forests.seed's fixed year of 24: converted by the world's year since phase 2 (A)


def clock_of(path) -> str | None:
    for pat, c in RATES:
        if fnmatch.fnmatchcase(path, pat):
            return c
    return None


def days_a_year(w) -> int:
    return w.year_days()


def lifespan_days(w) -> float:
    from cybertron2.engine import life as LF
    return float(LF.lifespan(w))


def per_night(value, clock, w) -> float:
    """A rate on its clock as a rate a night."""
    if clock == "day":
        return float(value)
    if clock == "year":
        return float(value) / days_a_year(w)
    if clock == "life":
        return float(value) / lifespan_days(w)
    raise ValueError(clock)
