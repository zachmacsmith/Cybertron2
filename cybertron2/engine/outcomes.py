"""Outcomes as distributions (D4-103; proposals/process_model.md part 2): one description of what an act can give, used two ways.

The act draws from it with the world's random stream (`sample`); an analysis takes its expectation (`mean`). Because both come from
the same object, the model of an act cannot drift from the act. Draws are made in a fixed order (an `If` draws its condition first,
then only the branch taken; a `Joint` draws its main part, then its by-products in order), so an act written this way consumes the
random stream exactly as the hand-written code it replaced.

A distribution's value is a number, or for a `Joint` a dict {"got": qty, "by": {good: qty}}.
"""
from __future__ import annotations


class Dist:
    def sample(self, rng):
        raise NotImplementedError

    def mean(self):
        raise NotImplementedError


class Const(Dist):
    def __init__(self, v):
        self.v = v

    def sample(self, rng):
        return self.v

    def mean(self):
        return self.v


class Uniform(Dist):
    def __init__(self, a, b):
        self.a, self.b = float(a), float(b)

    def sample(self, rng):
        return rng.uniform(self.a, self.b)

    def mean(self):
        return (self.a + self.b) / 2


class Scaled(Dist):
    """k x a draw, at most `cap` (None: no cap): the mean is exact for a uniform below."""
    def __init__(self, d, k=1.0, cap=None):
        self.d, self.k, self.cap = d, float(k), cap

    def sample(self, rng):
        v = self.d.sample(rng) * self.k
        return min(v, self.cap) if self.cap is not None else v

    def mean(self):
        if self.cap is None:
            return self.d.mean() * self.k
        if isinstance(self.d, Uniform) and self.k > 0:
            lo, hi, c = self.d.a * self.k, self.d.b * self.k, float(self.cap)
            if c >= hi:
                return (lo + hi) / 2
            if c <= lo:
                return c
            w = hi - lo                                                    # E[min(X, c)], X uniform on [lo, hi]
            return ((c * c - lo * lo) / 2 + c * (hi - c)) / w
        return min(self.d.mean() * self.k, float(self.cap))


class Bern(Dist):
    """1 with chance p, else 0 (draws one number)."""
    def __init__(self, p):
        self.p = float(p)

    def sample(self, rng):
        return 1 if rng.random() < self.p else 0

    def mean(self):
        return min(1.0, max(0.0, self.p))


class If(Dist):
    """With chance p, `then`; else `otherwise`. Draws the condition first, then only the branch taken."""
    def __init__(self, p, then, otherwise=None):
        self.p, self.then, self.otherwise = float(p), then, otherwise if otherwise is not None else Const(0.0)

    def sample(self, rng):
        return self.then.sample(rng) if rng.random() < self.p else self.otherwise.sample(rng)

    def mean(self):
        p = min(1.0, max(0.0, self.p))
        a, b = self.then.mean(), self.otherwise.mean()
        if isinstance(a, dict) or isinstance(b, dict):
            a, b = _as_joint(a), _as_joint(b)
            by = {g: p * a["by"].get(g, 0.0) + (1 - p) * b["by"].get(g, 0.0) for g in set(a["by"]) | set(b["by"])}
            return {"got": p * a["got"] + (1 - p) * b["got"], "by": by}
        return p * a + (1 - p) * b


class Joint(Dist):
    """A main quantity and by-products, drawn in that order: {"got": .., "by": {good: ..}}."""
    def __init__(self, got, by=None):
        self.got, self.by = got, dict(by or {})

    def sample(self, rng):
        g = self.got.sample(rng)
        return {"got": g, "by": {k: d.sample(rng) for k, d in self.by.items()}}

    def mean(self):
        return {"got": self.got.mean(), "by": {k: d.mean() for k, d in self.by.items()}}


def _as_joint(v):
    return v if isinstance(v, dict) else {"got": v, "by": {}}


def got(v) -> float:
    """The main quantity of a sample or a mean."""
    return float(v["got"]) if isinstance(v, dict) else float(v)


def by(v) -> dict:
    return dict(v.get("by") or {}) if isinstance(v, dict) else {}
