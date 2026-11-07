"""The world's year as the engine's calendar gives it (D4-102): nothing about seasons is assumed here.

A year day is world.calendar(d)["year_day"] mod year_days (0 at the first day of the calendar's first season). For each year day the
season and the frost come from world.calendar and world.cold at a day that falls on it, so a world with other seasons, other
lengths or cold days set by its file is read as it is.
"""
from __future__ import annotations

def table(w) -> list:
    """[(season, cold)] for each year day."""
    year = w.year_days()
    now = int(w.calendar()["year_day"]) % year
    out = []
    for yd in range(year):
        d = w.d + (yd - now) % year
        out.append((w.calendar(d)["season"], bool(w.cold(d))))
    return out


def frost_days(w, crop=None) -> set:
    """Year days on which the frost kills a growing crop that is not hardy (farm.frost_kills)."""
    from cybertron2.engine import farm as FM
    c = crop or {"hardy": False}
    return {yd for yd, (season, _) in enumerate(table(w)) if FM.frost_kills(c, season)}


def growing_window(w) -> tuple:
    """(start year day, length): the longest run of days, round the year, on which no frost kills a tender crop."""
    year = w.year_days()
    frost = frost_days(w)
    if not frost:
        return 0, year
    best_n, best_s = 0, 0
    for s in range(year):
        if s in frost or (s - 1) % year not in frost:          # a run starts the day after a frost
            continue
        n = 0
        while n < year and (s + n) % year not in frost:
            n += 1
        if n > best_n:
            best_n, best_s = n, s
    return best_s, best_n


def year_day_of(w, d) -> int:
    return int(w.calendar(d)["year_day"]) % w.year_days()
