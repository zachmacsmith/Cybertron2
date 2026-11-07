"""What a unit of gathering gives, as an outcome distribution (D4-103; proposals/process_model.md part 2).

One function per yield kind takes the technique's yield record, the stock it draws on {S, K}, the worker's multipliers (skill m,
tool tm) and the weapon's, and returns a distribution (outcomes.py). verbs._gather draws from it with the day's random stream; the
capacity model takes its mean at a stock's steady level. So the analysis reads the act itself.
"""
from __future__ import annotations

from cybertron2.engine.outcomes import Bern, Const, If, Joint, Scaled, Uniform

KINDS = ("stock", "chance", "fixed", "pool")


def density(r, b=1.0) -> float:
    """How the take answers the stock's density: (S/K) ** b (renewal.response)."""
    return r["S"] / r["K"] if b == 1.0 else (r["S"] / r["K"]) ** b


def dist(y, r, m=1.0, tm=1.0, weapon=1.0, refuge=0.1, b=1.0):
    """The outcome of one act of this yield kind. r: the stock drawn on {S, K} (None for a kind that draws on none); b: the stock's
    response to density (renewal.response)."""
    k = y["kind"]
    if k == "stock":                                                   # a share of a renewable stock, less as it thins (D4-7)
        want = y["base"] * density(r, b) * m * tm if b != 1.0 else y["base"] * r["S"] / r["K"] * m * tm
        return Const(round(max(0.0, min(want, r["S"] - refuge * r["K"])), 2))
    if k == "chance":                                                  # a hunt: a chance by the stock, a size by luck and the weapon
        catch = Scaled(Uniform(*y["range"]), m * weapon, cap=r["S"])
        return If(y["p"] * r["S"] / r["K"] if b == 1.0 else y["p"] * density(r, b), Joint(catch, {g: Bern(pr) for g, pr in (y.get("by") or {}).items()}))
    if k == "fixed":
        return Const(y["base"] * m * tm)
    if k == "pool":                                                    # dead wood: less to find as it thins (D2-156)
        q = y["base"] * m * min(1.0, r["S"] / max(r["K"], 1e-9)) ** 0.5
        return Const(min(q, r["S"]))
    raise KeyError(k)
