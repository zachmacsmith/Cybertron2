"""How each stock on the land comes back, and how its take answers its density (D4-7; D4-103, proposals/process_model.md part 3):
one registry the engine's nights and any analysis both use.

A renewal rule is a pure function `rule(p, res, ctx) -> S`: tomorrow's stock from today's record {S, K, r, ...} and the night's
context {winter, slow, trees, year, grazed, season}. The engine calls it each night (night._grow, forests.night); the capacity model
calls the same function to find a stock's best steady take.

Which rule a stock follows is data, at two levels: the resource's row gives the default (RESOURCES[key]["renewal"]), and a stock's own
record may name another (`renewal` in the parcel's state), so an ecosystem (a chalk stream, a fen mere) decides how its own fish or
plants come back, with its own parameters (K, r, run_K, ...) in the same record.

The response is how much a unit of work takes as the stock thins: the take scales by (S/K) ** b. b = 1 is proportional (the catch
per unit falls with the stock); b < 1 is hyperstable (shoaling fish, a herd that bunches: the catch holds up until the stock is nearly
gone); b > 1 is hyperdepleted (the easy ones go first). Default 1; a resource's row or a stock's record may set `response` to a
number or a name in RESPONSES.

Clocks: r is a rate a night (the day clock) unless the rule says otherwise; the woods' rates are a share a year, kept by
forests.seed as a night's rate (proposals/process_model.md, "Clocks").
"""
from __future__ import annotations

RULES = {}
NIGHTLY = ("fast", "threshold", "periodic")          # regrown by night._grow; the woods' three by forests.night
RESPONSES = {"proportional": 1.0, "hyperstable": 0.4, "hyperdepleted": 2.0}     # calibrate


def rule(name):
    def wrap(fn):
        RULES[name] = fn
        return fn
    return wrap


@rule("fast")
def fast(p, res, ctx):
    from cybertron2.engine import night as NI
    return NI.regrow(p, "fast", res["S"], res["K"], res["r"], ctx.get("winter", False))


@rule("threshold")
def threshold(p, res, ctx):
    from cybertron2.engine import night as NI
    return NI.regrow(p, "threshold", res["S"], res["K"], res["r"], ctx.get("winter", False))


@rule("periodic")
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


@rule("slow")
def slow(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.trees_step(res["S"], res["K"], res["r"], ctx.get("slow", 1.0))


@rule("young")
def young(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.young_step(res["S"], res["K"], res["r"], ctx.get("slow", 1.0))


@rule("dead")
def dead(p, res, ctx):
    from cybertron2.engine import forests as FO
    return FO.dead_step(res["S"], ctx.get("trees", 0.0), ctx.get("year", 32.0))


@rule("finite")
def finite(p, res, ctx):
    return res["S"]


@rule("endless")
def endless(p, res, ctx):
    return res["S"]


@rule("accrues")
def accrues(p, res, ctx):
    return res["S"]                                        # dung: added by the beasts where they stand (farm.py), not by the night


def of(key, res=None) -> str | None:
    """The stock's renewal rule: its own record's, else its resource's."""
    from cybertron2.engine.data import RESOURCES
    return (res or {}).get("renewal") or (RESOURCES.get(key) or {}).get("renewal")


def step(p, key, res, ctx) -> float:
    return RULES[of(key, res)](p, res, ctx)


def response(key, res=None) -> float:
    """The exponent b of the take's answer to density, (S/K) ** b: the stock's own, else its resource's, else 1."""
    from cybertron2.engine.data import RESOURCES
    b = (res or {}).get("response")
    if b is None:
        b = (RESOURCES.get(key) or {}).get("response", 1.0)
    return float(RESPONSES.get(b, b)) if isinstance(b, str) else float(b)
