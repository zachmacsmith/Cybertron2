"""The world's year as the engine's calendar gives it (D4-102): nothing about seasons is assumed here.

A year day is world.calendar(d)["year_day"] mod year_days (0 at the first day of the calendar's first season). For each year day the
season and the frost come from world.calendar and world.cold at a day that falls on it, so a world with other seasons, other
lengths or cold days set by its file is read as it is.
"""
from __future__ import annotations

def _day(w, yd) -> int:
    year = w.year_days()
    return w.d + (yd - int(w.calendar()["year_day"]) % year) % year


def table(w, at) -> list:
    """[(season, cold)] for each year day at a place (D4-111: the cold is a place's, as world.cold)."""
    return [(w.calendar(_day(w, yd))["season"], bool(w.cold(at, _day(w, yd)))) for yd in range(w.year_days())]


def seasons(w) -> list:
    """The season of each year day: the calendar's, the same everywhere."""
    return [w.calendar(_day(w, yd))["season"] for yd in range(w.year_days())]


def homes(w, nodes=None) -> dict:
    """{node: weight} for a model over several places at once (stores, fuel, upkeep): the living people at each node in scope, or
    the nodes equally where nobody is. A weighting over named places, never a default place (D4-111)."""
    scope = [n for n in sorted(w.s["nodes"]) if nodes is None or n in nodes]
    count = {n: sum(1 for a in w.s["people"].values() if a.get("alive", True) and a.get("at") == n) for n in scope}
    tot = sum(count.values())
    return {n: c / tot for n, c in count.items() if c} if tot else {n: 1 / len(scope) for n in scope}


def cold_share(w, day, nodes=None) -> float:
    """The share of the people in scope (homes) whose night is cold on a day."""
    return sum(k for n, k in homes(w, nodes).items() if w.cold(n, day))


def cold_shares(w, nodes=None) -> list:
    """cold_share for each year day."""
    return [cold_share(w, _day(w, yd), nodes) for yd in range(w.year_days())]


def frost_days(w, crop=None) -> set:
    """Year days on which the frost kills a growing crop that is not hardy (farm.frost_kills: by the season)."""
    from cybertron2.engine import farm as FM
    c = crop or {"hardy": False}
    return {yd for yd, season in enumerate(seasons(w)) if FM.frost_kills(c, season)}


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
