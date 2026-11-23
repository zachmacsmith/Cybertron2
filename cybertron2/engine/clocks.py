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
import math

RATES = [
    # the day clock: a night's share or chance
    ("ITEMS.*.spoil", "day"), ("DECAY.*.abs.*", "day"), ("PHYSICS.breaks.p", "day"), ("PHYSICS.breaks.cold", "day"),
    ("PHYSICS.farming.rot", "day"), ("PHYSICS.farming.window", "day"), ("PHYSICS.cattle.grass_r", "day"),
    ("TECHNIQUES.*.set.life", "day"),                                     # a set snare or trap lasts so many nights (brief 2)
    ("TECHNIQUES.*.rack.nights", "day"),                                  # meat dries on a rack so many nights (brief 4)
    ("PHYSICS.cattle.stray", "day"), ("PHYSICS.cattle.starve_nights", "day"), ("PHYSICS.fuel.*", "day"), ("PHYSICS.heat.*", "day"),
    ("RESOURCES.*.r", "day"), ("PHYSICS.smokehouse.fire.*", "day"),      # a smokehouse's fire a night (brief 5 §4a)
    # the year clock
    ("CROPS.*.share", "year"), ("FORESTS.kinds.*.grow", "year"), ("FORESTS.kinds.*.regrow", "year"), ("FORESTS.shed", "year"),
    ("FORESTS.rot", "year"), ("PHYSICS.cattle.births", "year"), ("PHYSICS.cattle.dung", "year"),
    ("PHYSICS.cattle.in_milk_share", "year"), ("PHYSICS.farming.fallow", "year"),
    ("FENCES.*.mend", "year"),                                          # a fence's mending a year (D4-114)
    # occasions and uses
    ("FORESTS.gale", "event"), ("PHYSICS.smokehouse.spread.*", "event"), ("PHYSICS.cattle.survive", "event"), ("PHYSICS.cattle.hungry_milk", "event"),
    ("PHYSICS.labour.work_food", "use"), ("PHYSICS.labour.over_food", "use"), ("PHYSICS.labour.step", "use"),
    ("PHYSICS.labour.guard_food", "event"), ("PHYSICS.labour.fade_rate", "year"), ("PHYSICS.labour.fade_after", "year"),
    ("FITTINGS.*.wear.life", "use"), ("FITTINGS.*.wear.years", "year"),
    ("FITTINGS.*.spoil", "day"), ("FITTINGS.*.dung", "year"),           # multipliers of a day's spoiling and a year's dung
    ("ITEMS.*.life", "use"), ("TECHNIQUES.*.wear", "use"), ("TECHNIQUES.*.yield.p", "use"), ("TECHNIQUES.*.inputs.*", "use"),
    # capital: real hours a piece and real uses, converted by the capital factor (D2-276, D2-309; u7 §1)
    ("*.hours", "capital"), ("*.*.hours", "capital"), ("*.*.*.hours", "capital"), ("*.uses", "capital"), ("*.*.uses", "capital"),
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


# ---------------------------------------------------------------------- the capital factor (D2-276, D2-281, D2-309; u7 §1; u3 §2.1)
def _fraction(x) -> float:
    if isinstance(x, (int, float)):
        return float(x)
    a, _, b = str(x).partition("/")
    return float(a) / float(b) if b else float(a)


def capital_factor(w=None) -> float:
    """The world's capital factor: a world spec's `capital_factor`, else CAPITAL's; "world" is units a year x 2 hours over a real
    working year (1/7.03 in a 32-day world with PHYSICS' units)."""
    from cybertron2.engine.data import CAPITAL, PHYSICS
    if w is None:
        f = None
    elif hasattr(w, "setting"):                                           # a Here: the world's setting, read through it (D4-35)
        f = w.setting("capital_factor")
    else:
        f = (getattr(w, "spec", None) or {}).get("capital_factor")
    f = f or CAPITAL["factor"]
    if str(f).strip().lower() == "world":
        year = w.year_days() if w is not None else 32
        units = sum(float(v) for v in PHYSICS["units"].values()) / len(PHYSICS["units"]) * year
        return units * 2.0 / float(CAPITAL["real_year"])
    return _fraction(f)


def held(row) -> bool:
    """A capital row whose class is held at today's units (D2-309), or one with no real hours yet."""
    from cybertron2.engine.data import CAPITAL
    return not row.get("hours") or row.get("capital") in CAPITAL["hold"]


def piece_units(row, w=None) -> float:
    """The unrounded units one piece takes: hours x factor / 2 on the capital clock, hours / 2 on the day clock (u3 §2.1)."""
    h = float(row.get("hours") or 0.0)
    return h / 2.0 if row.get("clock") == "day" else h * capital_factor(w) / 2.0


def capital_units(row, w=None, n=1) -> float:
    """The units of work a capital row takes for n pieces (u7 §1): a held class its `units` x n; else at least the floor,
    hours x n x factor / 2, rounded to a tenth."""
    from cybertron2.engine.data import CAPITAL
    if held(row):
        return float(row.get("units", 0)) * n
    return max(float(CAPITAL["floor"]), round(piece_units(row, w) * n, 1))


def batch_of(row, w=None) -> int:
    """The most pieces one act of the floor's unit makes (u3 §2.1): floor(1 / u) where a piece takes u under 1 unit, else 1. A row
    with no real hours makes `batch` pieces as written (1 unless it says)."""
    if not row.get("hours"):
        return 1
    u = piece_units(row, w)
    return max(1, int(math.floor(1.0 / u + 1e-9))) if u < 1.0 else 1


def act_units(row, w=None) -> int:
    """The units one act takes: at least the floor; round(u) for a piece of u at or over 1 (u3 §2.1)."""
    from cybertron2.engine.data import CAPITAL
    if not row.get("hours"):
        return max(int(CAPITAL["floor"]), int(row.get("units", 1)))
    u = piece_units(row, w)
    return max(int(CAPITAL["floor"]), int(round(u)) if u >= 1.0 else 1)


def capital_life(uses, w=None) -> int:
    """A life counted in acts of work (D2-310): real uses x the factor, at least 1, so a use costs the same at every stage."""
    return max(1, int(round(float(uses) * capital_factor(w))))


def night_life(nights) -> int:
    """A life counted in nights (D2-310): real nights x the calendar's 32 / 365, at least 1."""
    from cybertron2.engine.data import CAPITAL
    return max(1, int(round(float(nights) * float(CAPITAL["night"]))))
