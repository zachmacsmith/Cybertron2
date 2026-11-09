"""Running wave 1: villages from generated worlds and the engine's weather, observers by level, the household's acts and their
costs. Inputs: inputs.pkl from ../wild/prep.py (five generated worlds; daily weather by era)."""
from __future__ import annotations

import os
import pickle
import re

import numpy as np

import kinds as K
from rules import Y, S, LEVELS, Drivers, pulse_series, season, sday
from village import Village, FOOD_NEED, WORK, CHILD_WORK

INPUTS = os.environ.get("WILD_INPUTS", "/tmp/claude-0/-home-user/7e098288-bcf5-5d91-98fd-74db17ae2c32/scratchpad/wild/inputs.pkl")
ERAS = ["steady", "cold", "wet", "warm", "dry"]
_IN = None


def inputs():
    global _IN
    if _IN is None:
        _IN = pickle.load(open(INPUTS, "rb"))
    return _IN


def runs(eras=ERAS, worlds=None, villages=None):
    for wi, (wname, W) in enumerate(inputs().items()):
        if worlds and wname not in worlds:
            continue
        normals = {k: Drivers(W["weather"]["steady"][k]).normals for k in W["villages"]}
        for ei, era in enumerate(ERAS):
            if era not in eras:
                continue
            drv = {k: Drivers(W["weather"][era][k], normals[k]) for k in W["villages"]}
            k0 = sorted(W["villages"])[0]
            rng = np.random.default_rng(1000 * wi + ei)
            pulses = {name: pulse_series(row, drv[k0].years, rng, getattr(drv[k0], row["spoiler"])) for name, row in K.PULSES.items()}
            for vi, (k, info) in enumerate(sorted(W["villages"].items())):
                if villages and (wname, k) not in villages:
                    continue
                yield {"world": wname, "era": era, "village": k, "name": info["name"], "land": info, "drv": drv[k],
                       "pulses": pulses, "seed": 100000 * wi + 1000 * ei + vi}


class Observer:
    """What a householder of one level notices and how they read it (common random numbers across levels)."""

    def __init__(self, level, rng, masked=False):
        self.level, self.rng, self.seen, self.masked = level, rng, {}, masked

    def see(self, v, d):
        out = []
        for sg in v.signs.get(d, []):
            row = K.SIGNS[sg["sign"]]
            u = self.rng.random()
            if u < row["notice"].get(self.level, 0.0) and self.level in row["read"]:
                f = sg["facts"]
                text = row["read"][self.level](v, f)
                feat = {k: f.get(k, True) for k in row["facts"][self.level]}
                out.append({"kind": sg["kind"], "sign": sg["sign"], "text": mask(text) if self.masked else text, "feat": feat})
        self.seen[d] = out
        return out

    def has(self, d, sign, **want):
        for x in self.seen.get(d, []):
            if x["sign"] == sign and all(x["feat"].get(k) == val for k, val in want.items()):
                return x
        return None


MASK = [(r"\bwild boar\b", "beasts"), (r"\bboar\b", "beasts"), (r"\bBoar\b", "Beasts"), (r"\bsounder\b", "group"),
        (r"\bdeer\b", "beasts"), (r"\bDeer\b", "Beasts"), (r", hinds and calves", ""), (r", sows and young", ""),
        (r"\bwoodpigeons and rooks\b", "birds"), (r"\bWoodpigeons\b", "Birds"), (r"\bplovers and redwings\b", "birds"),
        (r"\bplovers\b", "birds"), (r"\beels\b", "fish"), (r"\beel\b", "fish"), (r"\bRat runs\b", "Runs"), (r"\bhare\b", "beast")]


def mask(t):
    for a, b in MASK:
        t = re.sub(a, b, t)
    return t


def charge(v, acts):
    """The work of the night's acts (ACTS in kinds.py), booked to the act."""
    for a, val in acts.items():
        row = K.ACTS.get(a)
        if not row or not val:
            continue
        units = row["units"] * (len(val) if row.get("per") == "gap" else 1)
        v.work("act:" + a, units, who=row.get("who", "adults"))


def simulate(r, policy=None, level="expert", masked=False, rights=None, built=None, days=None, start=0, kinds=None):
    rng = np.random.default_rng(r["seed"])
    v = Village(r["land"], r["drv"], r["pulses"], kinds or K.KINDS, rng, rights=rights, built=built, food_value=K.FOOD_VALUE)
    obs = Observer(level, np.random.default_rng(r["seed"] + 7), masked)
    end = r["drv"].n if days is None else min(r["drv"].n, start + days)
    for d in range(0, end):
        v.morning(d)
        obs.see(v, d)
        acts = policy(v, d, obs) if (policy and d >= start) else {}
        acts = acts or {}
        if d >= start:
            charge(v, acts)
        v.night(d, acts)
    return v, obs


def totals(v, years=None, kinds=None):
    """Loss, food yield, adults' and children's work by kind (and acts), over the given years."""
    out = {}
    for (y, k), r in v.ledger.items():
        if years is not None and y not in years:
            continue
        o = out.setdefault(k, {"loss": 0.0, "yield": 0.0, "work": 0.0, "child": 0.0})
        for key in o:
            o[key] += r[key]
    return out


def net(v, years=None, unit_food=0.5, child_food=0.1):
    t = totals(v, years)
    return sum(r["yield"] - r["loss"] - r["work"] * unit_food - r["child"] * child_food for r in t.values())
