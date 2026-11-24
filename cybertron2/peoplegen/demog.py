"""The forward model's tables (calibrate: values in the range of pre-industrial English and medieval reconstructions, not fitted).
Both the forward simulation (the reference) and the backward build read these and nothing else, so a difference between them is
the backward build's own doing."""
from __future__ import annotations

import math

from .keyed import u

FAR = 6.0               # villages with no road between them: this many days apart (W-107, a default taken)
LAMBDA = 0.8            # the marriage market's reach: a spouse d road-days away is weighted exp(-d / LAMBDA)
GAP = (3.5, 4.5)        # husband's age minus wife's: mean, sd
OFF_RATE = 0.8          # the off-map node's weight as a source of parents, as if this many unseen couples
CAME_RATE = 1.0         # founders of a village who came from outside the record
HARD_EVERY = 12         # one hard year in about this many (a stand-in for the climate scheduler's past, D4-109)
LEAVE = 0.02            # an unmarried person of 16 to 30 leaves for the off-map node, a year
KFRAC = 0.5              # fertile couples per household, in a village's past (measured on the forward run: 0.5 to 0.7)
OUT = 2.0               # a wife's parents in another village, beyond the distance kernel: kin at home are barred (forward: 64%)
MOVE = 0.5              # a man (or an unmarried woman) living in another village than his parents', relative to staying
CO = 20.0               # a grown son or unmarried daughter living with an elder: the likelihood ratio that the elder is a parent
FILL = 0.6              # the k-th village founded at span x (1 - share of today's households in the villages before it) ** FILL
FOUND_SD = 10           # a founding year about the plan (years)
THIRD = (12.0, 0.58, 14.0)  # a village A years old: its third-oldest resident about 12 + 0.58 A, sd 14 falling with age (forward fit)
FILL_YEARS = 35         # its households about 1 - exp(-A / 35) of the largest village's (forward fit)
SHARE_SD = 0.22
UNRECORDED = 0.3        # the chance a child who grew up and married is not in the record: it left, or its line died out
BUD = 20.0               # a daughter village's founders' parents lived in its mother village
CAME_DAUGHTER = 0.1     # from outside the record, for a daughter village's people
SHARP = 3.0             # a household's couples and children take the likeliest reading (weights to this power); the rest is drawn
SIBLIKE = 0.2           # a young man and woman in a house with a woman who could have borne both: likelier siblings (forward: odds / 5)
AWAY = 0.0015           # a child living apart from a living parent (forward: 1.5% of such children, spread over a village's couples)
FOSTER = 0.1            # a child with both parents dead, living in another's house (forward: 0.7% of children; calibrate)
FLOOR = 0.03             # a village's unseen couples when the ones already made fill its estimate (calibrate)
FOUND = 0.5             # a couple with no house to be had founds a new village, if a site is left


def fert(a) -> float:
    """Marital fertility: births a year to a married woman of age a."""
    if a < 15 or a > 47:
        return 0.0
    return {15: .15, 16: .25, 17: .3, 18: .35, 19: .4}.get(a) or (.42 if a < 25 else .40 if a < 30 else .36 if a < 35
                                                                  else .29 if a < 40 else .15 if a < 45 else .03)


def hazard(a, hard=False) -> float:
    """The chance of dying within the year at age a; a hard year multiplies it (most for the very young and the old)."""
    h = .18 if a < 1 else .035 if a < 5 else .008 if a < 15 else .010 if a < 50 else min(.6, .01 + .006 * math.exp(.1 * (a - 50)))
    if hard:
        h = min(.8, h * (3 if a < 5 or a >= 60 else 2))
    return h


_S = [1.0]
for _a in range(130):
    _S.append(_S[-1] * (1 - hazard(_a)))


def S(a) -> float:
    """Survival from birth to age a (no hard years)."""
    return _S[max(0, min(int(a), 130))]


def survive(a0, a1) -> float:
    """The chance that someone alive at age a0 is alive at a1."""
    return S(a1) / S(a0) if S(a0) > 0 else 0.0


def first_marriage(a, sex="f") -> float:
    """The yearly chance an unmarried woman (or man, four years later) marries, if a partner is to be had."""
    a = a if sex == "f" else a - 4
    return 0 if a < 16 else .1 if a < 20 else .25 if a < 30 else .12 if a < 40 else .03


def married_share(a, sex="f") -> float:
    """The share of the living of age a who have married: from first_marriage."""
    p = 1.0
    for x in range(int(a)):
        p *= 1 - first_marriage(x, sex)
    return 1 - p


_G = {a: married_share(a) * S(a) for a in range(15, 48)}
_GT = sum(_G[a] * fert(a) for a in _G)


def g(a) -> float:
    """The age of a mother at a birth, among the married women of a place: married share x survival x fertility, normalised."""
    return _G.get(a, 0) * fert(a) / _GT


FBAR = _GT / sum(_G.values())   # a fertile couple's mean births a year


def unwed_death(a_now, sex="f") -> float:
    """The chance someone born a_now years ago died before marrying: the hazard at each age while still unmarried."""
    return sum(hazard(a) * S(a) * (1 - married_share(a, sex)) for a in range(int(a_now)))


def gap_w(gap) -> float:
    m, s = GAP
    return math.exp(-((gap - m) ** 2) / (2 * s * s))


def hard_years(seed, span) -> set:
    """The world's hard years (a stand-in for the climate scheduler's past, D4-109: the same years for every village)."""
    return {y for y in range(-span, 0) if u(seed, "hard", y) < 1.0 / HARD_EVERY}


def death_w(age, year, hard) -> float:
    """The weight of dying in a given year at a given age, for someone alive at the start of the window (the hazard times the
    survival to that age; the caller divides by the survival at the window's start)."""
    return hazard(age, year in hard) * S(age)


def cause(age, year, hard, childbed=False) -> str:
    if age < 1:
        return "in the cradle"
    if age < 5:
        return "a childhood fever"
    if childbed:
        return "in childbed"
    if year in hard:
        return "the hard winter"
    if age >= 60:
        return "old age"
    return "a fever"
