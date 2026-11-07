"""How each stock on the land comes back (D4-7; D4-103, proposals/process_model.md part 3): one registry the engine's nights and
any analysis both use.

A regime is a pure function `step(p, res, ctx) -> S`: tomorrow's stock from today's record {S, K, r, ...} and the night's context
{winter, slow, trees, year, grazed, season}. The engine calls it each night (night._grow, forests.night); the capacity model calls the
same function to find a stock's best steady take. Which regime a stock has is data (RESOURCES[key]["regime"]).

Clocks: r is a rate a night (the day clock) unless the regime says otherwise; the woods' rates are a share a year, kept by
forests.seed as a night's rate (proposals/process_model.md, "Clocks").
"""
from __future__ import annotations

REGIMES = {}
NIGHTLY = ("fast", "threshold", "periodic")          # regrown by night._grow; the woods' three by forests.night


def regime(name):
    def wrap(fn):
        REGIMES[name] = fn
        return fn
    return wrap


@regime("fast")
def fast(p, res, ctx):
    from cybertron2.engine import night as NI
    return NI.regrow(p, "fast", res["S"], res["K"], res["r"], ctx.get("winter", False))


@regime("threshold")
def threshold(p, res, ctx):
    from cybertron2.engine import night as NI
    return NI.regrow(p, "threshold", res["S"], res["K"], res["r"], ctx.get("winter", False))


@regime("periodic")
def periodic(p, res, ctx):
    """A stock that comes at its time (a fish run, D4-7): in its seasons the stock is drawn toward its run's capacity (`run_K`) at
    `run_r` a night; out of them the run leaves at the same rate, back toward the resident stock, which itself regrows as a fast
    stock toward K."""
    from cybertron2.engine import night as NI
    S, K = float(res["S"]), float(res["K"])
    if ctx.get("season") in (res.get("run_seasons") or []):
        target = float(res.get("run_K", K))
    else:
        target = K
    rr = float(res.get("run_r", 0.3))
    if S > target:                                         # the run moving on
        return round(max(target, S - rr * (S - target)), 4)
    if target > K:                                         # the run arriving
        return round(min(target, S + rr * (target - S)), 4)
    return NI.regrow(p, "fast", S, K, float(res.get("r", 0.3)), ctx.get("winter", False))


@regime("slow")
def slow(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.trees_step(res["S"], res["K"], res["r"], ctx.get("slow", 1.0))


@regime("young")
def young(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.young_step(res["S"], res["K"], res["r"], ctx.get("slow", 1.0))


@regime("dead")
def dead(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.dead_step(res["S"], ctx.get("trees", 0.0), ctx.get("year", 32.0))


@regime("finite")
def finite(p, res, ctx):
    return res["S"]


@regime("endless")
def endless(p, res, ctx):
    return res["S"]


@regime("accrues")
def accrues(p, res, ctx):
    return res["S"]                                        # dung: added by the beasts where they stand (farm.py), not by the night


def of(key) -> str | None:
    from cybertron2.engine.data import RESOURCES
    return (RESOURCES.get(key) or {}).get("regime")


def step(p, key, res, ctx) -> float:
    return REGIMES[of(key)](p, res, ctx)
