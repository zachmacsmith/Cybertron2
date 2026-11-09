"""A village and its year for the wild systems: land, stocks at risk, the ledger, signs and events. Holds no kind-specific code."""
from __future__ import annotations

import numpy as np

from rules import Y, S, Ctx, RULES, pulse_series, season, sday

FOOD_NEED = 12 * Y                   # 12 people, one food a day
WORK = 12 * 6 * Y * 0.8              # adults' units a year
CHILD_WORK = 4 * 6 * Y * 0.5         # four children's units a year
GAP_NAMES = ["the thorn gap", "the ford gap", "the lane gap"]


class Village:
    def __init__(self, land, drv, pulses, kinds, rng, rights=None, built=None, names=None, food_value=None):
        self.land, self.drv, self.pulses, self.rng = land, drv, pulses, rng
        self.food_value = food_value or {}
        self.rights, self.built = rights or {}, built or {}
        self.gaps, self.gap_names = 3, GAP_NAMES
        self.names = names or {}
        crop = land["own_ha"].get("field", 0) / 2 * 48.0
        self.base = {"crop": crop, "seed_spring": 0.4 * crop * 0.25, "seed_autumn": 0.6 * crop * 0.25,
                     "stores": 0.6 * FOOD_NEED, "ricks": 0.15 * crop}
        self.stocks = dict(self.base)
        self.ledger, self.goods, self.events, self.signs = {}, {}, {}, {}
        self.year = 0
        self.kinds = {k: RULES[row["rule"]](k, row, self, np.random.default_rng(rng.integers(1 << 32))) for k, row in kinds.items()}

    # -- what rules call
    def stock(self, k):
        return self.stocks.get(k, 0.0)

    def lose(self, kind, target, food):
        food = min(food, self.stocks.get(target, 0.0))
        self.stocks[target] = self.stocks.get(target, 0.0) - food
        r = self.ledger.setdefault((self.year, kind), {"loss": 0.0, "yield": 0.0, "work": 0.0, "child": 0.0})
        r["loss"] += food

    def gain(self, kind, good, q):
        self.goods[(self.year, good)] = self.goods.get((self.year, good), 0.0) + q
        if good in self.food_value:
            r = self.ledger.setdefault((self.year, kind), {"loss": 0.0, "yield": 0.0, "work": 0.0, "child": 0.0})
            r["yield"] += q * self.food_value[good]

    def work(self, kind, units, who="adults"):
        r = self.ledger.setdefault((self.year, kind), {"loss": 0.0, "yield": 0.0, "work": 0.0, "child": 0.0})
        r["child" if who == "children" else "work"] += units

    def event(self, d, kind, key, val):
        self.events.setdefault(d, {}).setdefault(kind, {})[key] = val

    def emit(self, d, kind, sign, **facts):
        self.signs.setdefault(d, []).append({"kind": kind, "sign": sign, "facts": facts})

    # -- the day: morning (signs of the day), then the night (the rules act, given the household's acts)
    def morning(self, d):
        c = Ctx(self, d, {})
        if d % Y == 0:
            self.year = d // Y
            self.stocks = dict(self.base)
            for k in self.kinds.values():
                k.new_year(c)
        for k in self.kinds.values():
            if hasattr(k, "morning"):
                k.morning(c)

    def night(self, d, acts):
        c = Ctx(self, d, acts)
        for k in self.kinds.values():
            k.step(c)
        for name, units in acts.get("_work", {}).items():
            self.work(name, units)

    def present(self):
        return {k: r.present() for k, r in self.kinds.items()}

