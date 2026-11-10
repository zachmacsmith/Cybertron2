"""Food a unit of work from wild takes, in generated worlds (02zzd). Point CYB_ROOT at a checkout of the branch to measure
(default: this repository). Each try runs on a fresh copy of the world at its start, so nothing depletes between tries."""
import os, sys, copy
ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
from cybertron2.landgen import write as W
from cybertron2.engine.world import World, Refused
from cybertron2.engine.here import Here, Mind
from cybertron2.engine import verbs as V, run as R, night as NI, knowledge as KN
from cybertron2.engine.data import TECHNIQUES as T, ITEMS

RANGE_UNITS = {r: int(T[f"range: {r}"]["units"]) for r in ("near", "the wood around", "far") if f"range: {r}" in T}
KINDS = ("red deer", "roe deer", "wild boar", "brown hare", "woodpigeon", "wildfowl", "eel", "fox")


def gen(seed, cfg, season, settlements=3):
    """A generated world with people (the generator refuses people when its capacity check fails: then 'agents' is missing)."""
    g = {"seed": seed, "configuration": cfg, "settlements": settlements}
    world, _, _ = W.generate({"name": f"ev_{seed}", "seed": seed, "days": 4,
                              "calendar": {"season": season, "day": 2, "season_days": 8}, "generate": g}, people=True)
    world["packs"] = ["wild"]
    return world


def food(goods):
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0)) for i, q in (goods or {}).items())


def setup(w, who, method, skill, fam, armed=False):
    w.s["know"].setdefault(who, {})[method] = {"level": "known", "skill": skill}
    Mind(w, who).store["familiar"] = {k: fam for k in KINDS}
    if armed:
        g = w.s["containers"][Here(w, who).hands]["goods"]
        g["crude weapon"] = g.get("crude weapon", 0) + 1


def attempt(w0, who, act, method, skill, fam, salt, setwork=False, armed=False):
    """One try on a fresh copy: food gained in hand (and, for a set work, in the set things after a night). None if refused."""
    w = copy.deepcopy(w0)
    w.s["today"] = R.blank_today()
    orig = w.rng
    w.rng = lambda *k: orig(*k, "ev", salt)
    setup(w, who, method, skill, fam, armed)
    before = food(w.s["containers"][Here(w, who).hands]["goods"])
    try:
        V.do(Here(w, who), Mind(w, who), dict(act))
    except Refused:
        return None
    got = food(w.s["containers"][Here(w, who).hands]["goods"]) - before
    if setwork:
        NI.night(w)
        got += sum(food(c.get("goods")) for c in w.s["containers"].values() if c.get("kind") == "set" and c.get("by", c.get("setter")) == who)
    return got


def units(method, rng_):
    return int(T[method]["units"]) + RANGE_UNITS.get(rng_, 0)
