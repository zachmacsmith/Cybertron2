"""Layered wild systems at village scale: a prototype of proposals/wild_systems.md (02zp part five).

Time is the engine's: a year of Y = 32 days, four seasons of 8. Weather is the engine's climate (D4-109) at the village's node. Lead
times and creature memory are in engine days, never less than one (D2-197): a sign seen on day t leads an event on night t+1 or
later. Kinds answer scares in four ways (D2-198): get used to them, scared off, leave for good, do not answer.

The design's two layers:
- a coarse layer per village's surroundings: each kind's numbers (boar per km2 of wood, the fox family, the winter flock, the eels
  that pass the weir) and the shared drivers;
- near people, groups condensed from it with places, habits and memory (a sounder, a fox), and area-level kinds with signs (voles,
  wasps, slugs).

General rules, each written once and used by several kinds:
  Group       a group that sets out toward a target (field, stores, hens) on a drive, with a lead stage that leaves signs, memory of
              success, and an answer to scares (D2-198)
  Flock       visitors that come with a driver (a freeze), weaken with its run, and are scared off by disturbance
  Run         a seasonal run on conditions (dark, rising water, after a dry spell), taken at a weir
  Load        an area-level number set by the drivers by season (slugs, wasps, voles), active on conditions, with damage in windows
  Pulse       a yearly resource with a lag (mast, the vole phase)
Kinds are data rows on these (KINDS below). Signs carry a reading per skill level: novice, systematic, expert (Liebenberg).
"""
from __future__ import annotations

import math
import numpy as np

Y, S = 32, 8
LEVELS = ("novice", "systematic", "expert")
FOOD_NEED = 12 * Y              # 12 people, one food a day
WORK = 12 * 6 * Y * 0.8         # adults' units a year


def season(d):
    return (d % Y) // S


def sday(d):
    return d % S


# ------------------------------------------------------------------ drivers from the engine's weather
class Drivers:
    """Daily drivers at one village from the engine's weather list, plus yearly anomalies against normals."""

    def __init__(self, wx, normals=None):
        n = len(wx)
        self.n = n
        self.temp = np.array([x["temp"] for x in wx]); self.low = np.array([x["low"] for x in wx])
        self.rain = np.array([x["rain"] for x in wx])
        self.frozen = (self.low < -3.0) & (self.temp < 3.0)                 # a hard frost: the ground sealed (see 02zp §26)
        self.frun = np.zeros(n, int); self.dry = np.zeros(n, int); self.snow = np.zeros(n, bool)
        self.river = np.zeros(n); self.wet = np.zeros(n)
        for d in range(n):
            self.frun[d] = (self.frun[d - 1] + 1) if (d and self.frozen[d]) else int(self.frozen[d])
            self.dry[d] = (self.dry[d - 1] + 1) if (d and self.rain[d] < 2.0) else int(self.rain[d] < 2.0)
            self.snow[d] = (self.low[d] < 0 and self.rain[d] > 1) or (d and self.snow[d - 1] and self.temp[d] < 3)
            self.river[d] = (0.5 * self.river[d - 1] + self.rain[d - 1]) if d else 0.0       # the river answers a day late
            self.wet[d] = min(2.0, (0.55 * self.wet[d - 1] if d else 0.0) + self.rain[d] / 5)
        self.rising = np.r_[False, np.diff(self.river) > 2.0]
        real = np.arange(n) * 365.0 / Y / 29.53
        ph = real - np.floor(real)
        self.dark = np.minimum(ph, 1 - ph) < 0.2                      # a moonless stretch of nights in this engine day
        self.years = n // Y
        sea = lambda arr, y, s: arr[y * Y + s * S: y * Y + (s + 1) * S]
        self.seas = [{s: {"T": float(sea(self.temp, y, s).mean()), "wet": float((sea(self.rain, y, s) > 2).mean()),
                          "frost": float(sea(self.frozen, y, s).mean()), "maxrun": int(sea(self.frun, y, s).max())}
                      for s in range(4)} for y in range(self.years)]
        self.normals = normals or {s: {k: float(np.mean([r[s][k] for r in self.seas])) for k in ("T", "wet", "frost")} for s in range(4)}
        self.flower_frost = [bool((self.low[y * Y + 5: y * Y + 8] < -1.5).any()) for y in range(self.years)]

    def anom(self, y, s, k):
        y = max(0, min(self.years - 1, y))
        return self.seas[y][s][k] - self.normals[s][k]

    def hard_winter(self, y):
        return self.seas[max(0, y)][3]["maxrun"] >= 2


# ------------------------------------------------------------------ pulses (world-level, shared by villages)
def mast_series(years, rng, flower_frost):
    """Oak mast by year: the trees' rhythm (a budget that builds) and frost at flowering. heavy 3, ordinary 1, poor 0.4, fail 0.15.
    The year after a heavy mast fails (the trees are spent): the bust."""
    out, full, B, th = [], [], 0, int(rng.integers(2, 5))
    for y in range(years):
        B += 1
        full.append(B >= th and not (out and out[-1] == 3.0))
        if out and out[-1] == 3.0:
            lvl = 0.15
        elif B >= th:
            lvl = 0.15 if flower_frost[y] else 3.0
            if lvl == 3.0:
                B, th = 0, int(rng.integers(2, 5))
        else:
            lvl = 1.0 if rng.random() < 0.6 else 0.4
            if flower_frost[y]:
                lvl = 0.15
        out.append(lvl)
    return out, full


def vole_phases(years, rng, mast, hard):
    """The vole cycle: low, increase, peak, crash (about 4 years); a heavy mast lifts a low year; a hard winter holds an increase."""
    order = ["low", "increase", "peak", "crash"]
    i = int(rng.integers(4)); out = []
    for y in range(years):
        out.append(order[i])
        if order[i] == "increase" and hard[y]:
            continue
        if order[i] == "low" and y and mast[y - 1] >= 3:
            i = 1; continue
        i = (i + 1) % 4
    return out


VOLE_BASE = {"low": 0.3, "increase": 1.0, "peak": 2.6, "crash": 0.6}


# ------------------------------------------------------------------ the kinds as data on the general rules
KINDS = {
    "boar": {"rule": "Group", "depth": "deep", "answer": "habituate", "lead_nights": 2, "lead_sign_p": 0.9, "gaps": 3,
             "turn_p": 0.9, "habit_gain": 0.3, "habit_decay": 0.01, "rest_after_turn": 2, "wary_after_harm": 8,
             "return_p": 0.85, "loss": {"crop": 0.005, "seed": 0.002, "stores": 0.004}},
    "fox": {"rule": "Group", "depth": "middling", "answer": "scared_off", "lead_nights": 2, "lead_sign_p": 0.8, "gaps": 1,
            "turn_p": 0.85, "off_days": 3, "wary_after_harm": 10, "return_p": 0.8, "hens_per_visit": 2, "surplus": 8},
    "fowl": {"rule": "Flock", "depth": "middling", "answer": "scared_off", "off_days": 1, "off_p": 0.4,
             "rate": {0: 0.01, 1: 0.04, 2: 0.12}, "bird_food": 0.2, "lead_sign_p": 0.75, "false_sign_p": 0.12},
    "eels": {"rule": "Run", "depth": "middling", "answer": "none", "stock": {"brook": 120, "river": 800}, "eel_food": 0.22,
             "base": 0.04, "dark_rising": 6.0, "rising": 2.5, "after_dry": 1.8, "moonlit": 0.4, "trap_share": 0.4},
    "voles": {"rule": "Load", "depth": "deep", "answer": "none", "store_rate": 0.0012, "hay_rate": 0.02, "cats": 0.4, "owls": 0.7},
    "wasps": {"rule": "Load", "depth": "middling", "answer": "none", "fruit_rate": 0.035, "honey_rate": 0.03, "sting_units": 0.4},
    "slugs": {"rule": "Load", "depth": "simple", "answer": "none", "rate": 0.012},
}


# ------------------------------------------------------------------ a village and its year
class Village:
    def __init__(self, info, drv, mast, voles, rng, mast_full=None):
        self.info, self.drv, self.mast, self.voles, self.rng = info, drv, mast, voles, rng
        self.mast_full = mast_full or [m >= 3 for m in mast]
        own, ring = info["own_ha"], info["ring_km2"]
        self.crop = own.get("field", 0) / 2 * 48.0                        # engine net food a year from the fields
        self.stores = 0.6 * FOOD_NEED
        self.hens, self.hen_food = 24, 0.5
        self.fruit, self.honey = 12.0, 6.0
        self.hay = 10.0
        self.wood_km2 = ring.get("forest", 0.0) + own.get("forest", 0.0) / 100
        self.fen_km2 = ring.get("fen", 0.0) + own.get("fen", 0.0) / 100
        self.river = "river" if "river" in info["rivers"] else ("brook" if info["rivers"] else None)
        self.boar_density = 3.0
        # groups condensed near the village
        self.sounder = None
        self.fox = {"pos": "away", "t": 0, "found": -99, "off_until": -1, "wary_until": -1, "present": True}
        self.flock = 150 + 400 * min(self.fen_km2, 3.0) if self.fen_km2 > 0.5 else (80 if self.river else 30)
        self.flock_off_until = -1
        self.eel_left = 0.0
        self.Q = 1.0; self.L = 1.0
        self.nests_taken = False; self.fruit_picked = False
        self.ledger = {}
        self.year = 0
        self.events = {}              # day -> {event: value} (the truth, for scoring readers)
        self.signs = {}               # day -> list of signs seen that day (traces of the night before, and the day's own)

    # -- bookkeeping
    def add(self, kind, food=0.0, work=0.0):
        r = self.ledger.setdefault((self.year, kind), {"loss": 0.0, "yield": 0.0, "work": 0.0})
        if food < 0:
            r["loss"] += -food
        else:
            r["yield"] += food
        r["work"] += work

    def ev(self, d, k, v=1):
        self.events.setdefault(d, {})[k] = v

    def sign(self, d, kind, name, notice, read):
        """notice: {level: chance of noticing}; read: {level: the reading's content (a dict), the most a level can take from it}."""
        self.signs.setdefault(d, []).append({"kind": kind, "name": name, "notice": notice, "read": read})

    # -- the year's turn (spring, day 0 of the year)
    def new_year(self, y):
        D = self.drv
        mprev = self.mast[y - 1] if y else 1.0
        # boar: farrowing by last autumn's mast, held by the wood's room; winter deaths in a hard winter without mast
        K = 5.0 * (1.3 if mprev >= 3 else 1.0)
        farrow = {3.0: 1.0, 1.0: 0.45, 0.4: 0.25, 0.15: 0.12}[mprev]
        b = self.boar_density
        b = b + farrow * b * (1 - b / K)
        if y and D.hard_winter(y - 1) and mprev < 0.5:
            b *= 0.6
        self.boar_density = max(0.2, b * 0.9)
        boar_ring = self.boar_density * self.wood_km2
        if boar_ring >= 4:
            n = int(np.clip(round(3 + 0.06 * boar_ring), 3, 14))
            s = self.sounder or {"pos": "wood", "t": 0, "found": -99, "habit": {}, "wary_until": -1, "rest_until": -1,
                                 "gap": int(self.rng.integers(KINDS["boar"]["gaps"]))}
            s["n"] = n
            self.sounder = s
        else:
            self.sounder = None
        # wasps: queens from the spring (set at its end); slugs: the load from the winter just past
        self.L = float(np.exp(0.30 * D.anom(y - 1, 3, "T") + 1.5 * D.anom(y - 1, 3, "wet") - 0.6 * D.anom(y - 1, 3, "frost")))
        self.eel_left = KINDS["eels"]["stock"].get(self.river, 0) if self.river else 0.0
        self.nests_taken = False; self.fruit_picked = False
        self.flock_taken = 0.0
        self.fox["present"] = True
        self.year = y

    # -- one day and its night; acts are the household's for this day and night
    def day(self, d, acts):
        D, y, s, sd = self.drv, d // Y, season(d), sday(d)
        if d % Y == 0:
            self.new_year(y)
        if d % Y == 4:                                               # mid-spring: the wasp queens out of hibernation
            self.Q = float(np.exp(0.35 * D.anom(y, 0, "T") - 1.2 * D.anom(y, 0, "wet") + 0.25 * self.rng.standard_normal()))
        if d % Y == S + 4:                                             # the summer's slug load
            self.L = float(np.exp(1.2 * D.anom(y, 1, "wet") - 0.25 * D.anom(y, 1, "T")))
        mast = self.mast[y]
        self._signs_of_drivers(d, y, s, sd, mast)
        self._boar(d, y, s, sd, mast, acts)
        self._fox(d, y, s, sd, acts)
        self._fowl(d, y, s, sd, acts)
        self._eels(d, y, s, sd, acts)
        self._voles(d, y, s, sd, acts)
        self._wasps(d, y, s, sd, acts)
        self._slugs(d, y, s, sd, acts)

    # ---------------------------------------------------------- drivers' own signs (the mast, the voles)
    def _signs_of_drivers(self, d, y, s, sd, mast):
        if self.wood_km2 > 0.05:
            if s == 0 and sd in (5, 6):                               # catkins on the oaks: the trees' budget (a season ahead)
                heavy = self.mast_full[y]
                self.sign(d, "mast", "catkins", {"expert": 0.8},
                          {"expert": {"catkins": "heavy" if heavy else "light"}})
            if s == 1 and sd in (5, 6, 7):                            # acorns setting
                self.sign(d, "mast", "acorns setting", {"systematic": 0.6, "expert": 0.9},
                          {"systematic": {"set": "thick" if mast >= 3 else ("some" if mast >= 1 else "few")},
                           "expert": {"set": "thick" if mast >= 3 else ("some" if mast >= 1 else "few")}})
            if s == 2 and sd >= 2:
                self.sign(d, "mast", "acorns on the ground", {"novice": 0.9, "systematic": 0.95, "expert": 1.0},
                          {lv: {"fallen": "thick" if mast >= 3 else ("some" if mast >= 1 else "none")} for lv in LEVELS})
        ph = self.voles[y]
        if d % Y == 0:
            self._vnoise = float(np.exp(0.35 * self.rng.standard_normal()))      # the village's own year: patchy voles
        V = VOLE_BASE[ph] * (0.5, 0.75, 1.0, 0.7)[s] * getattr(self, "_vnoise", 1.0)
        self.V = V
        if s in (1, 2) and V > 1.6:
            self.sign(d, "voles", "pellets thick with little skulls under the barn beam", {"expert": 0.7}, {"expert": {"pellets": "thick"}})
        if s in (1, 2) and (V > 1.5 or self.rng.random() < 0.2):
            self.sign(d, "voles", "kestrels hovering", {"novice": 0.5, "systematic": 0.8, "expert": 0.9},
                      {"novice": {"kestrels": True}, "systematic": {"voles": "many"}, "expert": {"kestrels": True}})
        if s in (1, 2) and V > 0.9:
            self.sign(d, "voles", "runways in the long grass", {"systematic": 0.5, "expert": 0.8},
                      {"systematic": {"voles": "some"}, "expert": {"voles": "thick" if V > 1.6 else "some"}})
        if s in (2, 3) and ph == "crash":
            self.sign(d, "voles", "the owls silent", {"systematic": 0.4, "expert": 0.8},
                      {"systematic": {"owls": "silent"}, "expert": {"owls": "silent", "hungry": True}})

    # ---------------------------------------------------------- Group: the sounder
    def _boar(self, d, y, s, sd, mast, acts):
        g, K = self.sounder, KINDS["boar"]
        if g is None:
            return
        frozen = self.drv.frun[d] >= 1
        if (s == 1 and sd >= 3) or (s == 2 and sd <= 1):
            attr, target = 1.0, "crop"                                # milk-ripe to harvest
        elif s == 0 and sd <= 5:
            attr, target = 0.3, "seed"                                # the sown corn
        elif s in (2, 3):
            attr, target = 0.4, "stores"                              # stubbles, clamps and ricks
        else:
            attr, target = 0.1, "crop"
        food = min(1.0, mast / 2.0) if s in (2, 3) else 0.6           # mast in autumn and winter; roots otherwise
        if frozen:
            food, attr, target = 0.1, max(attr, 0.5), "stores"        # the ground sealed: no rooting
        for k in list(g["habit"]):
            g["habit"][k] = max(0.0, g["habit"][k] - K["habit_decay"])
        if g["pos"] == "ready" and d == g["raid"]:
            self._boar_raid(d, g, K, target, acts)
        elif g["pos"] == "edge":
            self._boar_edge(d, g, K)
        elif g["pos"] == "wood" and d >= g["rest_until"] and d >= g["wary_until"]:
            p = attr * (0.12 + 0.6 * (1 - food))
            knows = 1 <= d - g["found"] <= 3
            if knows:
                p = max(p, K["return_p"] * attr)
            if self.rng.random() < p:
                g["gap_tonight"] = g["gap"] if self.rng.random() < 0.75 else int(self.rng.integers(K["gaps"]))
                if knows:                                             # a field it knows: back the next night; the damage is the sign
                    g["pos"], g["raid"] = "ready", d + 1
                else:
                    g["pos"], g["t"] = "edge", d
                    self._boar_edge(d, g, K)
        if acts.get("hunt_boar") and g["pos"] == "wood" and self.sounder is not None:
            self.add("boar", 0.0, 6.0)
            if self.rng.random() < (0.5 if acts.get("hunt_skill") == "expert" else 0.25):
                g["n"] -= 1
                self.boar_density = max(0.2, self.boar_density - 1 / max(self.wood_km2, 0.1))
                self.add("boar", 3.5)                                  # a boar: 40 person-days, about 3.5 food
                g["wary_until"], g["habit"] = d + K["wary_after_harm"], {}
                self.ev(d, "boar_harmed", 1)
                if g["n"] < 2:
                    self.sounder = None

    def _old_rooting(self, d):
        for k in (1, 2):                                               # the trace ages: still there, no longer fresh
            self.sign(d + k, "boar", "rooting at the wood's edge", {"novice": 0.6, "systematic": 0.8, "expert": 0.95},
                      {"novice": {"rooting": True}, "systematic": {"rooting": "old"}, "expert": {"rooting": "old"}})

    def _boar_edge(self, d, g, K):
        if self.rng.random() < K["lead_sign_p"]:
            self.sign(d + 1, "boar", "rooting at the wood's edge", {"novice": 0.6, "systematic": 0.8, "expert": 0.95},
                      {"novice": {"rooting": True}, "systematic": {"rooting": "fresh", "n": g["n"]},
                       "expert": {"rooting": "fresh", "n": g["n"], "gap": g["gap_tonight"]}})
        if d - g["t"] >= K["lead_nights"] - 1:
            g["pos"], g["raid"] = "ready", d + 1                      # at the field tomorrow night

    def _boar_raid(self, d, g, K, target, acts):
        self.ev(d, "boar_raid", 1)
        gap = g["gap_tonight"]
        watch = acts.get("watch", {})
        base = (self.crop if target in ("crop", "seed") else self.stores) * K["loss"][target] * g["n"]
        sc = watch.get(gap)
        g["pos"] = "wood"
        self._old_rooting(d)
        if sc is not None:
            p = 0.95 if sc == "dog" else K["turn_p"] * (1 - g["habit"].get(sc, 0.0))
            self.ev(d, "boar_scare", sc)
            if self.rng.random() < p:
                if sc == "dog" and self.rng.random() < 0.25:            # the dog bit: real harm
                    g["wary_until"], g["habit"] = d + K["wary_after_harm"], {}
                    self.ev(d, "boar_harmed", 1)
                else:
                    g["habit"][sc] = min(1.0, g["habit"].get(sc, 0.0) + K["habit_gain"])
                g["rest_until"] = d + K["rest_after_turn"]
                self.ev(d, "boar_turned", 1)
                return
            self.add("boar", -0.5 * base)
        else:
            self.add("boar", -base)
        g["found"] = d
        self.ev(d, "boar_loss", base if sc is None else 0.5 * base)
        self.sign(d + 1, "boar", "the corn trampled at the corner", {lv: 0.9 for lv in LEVELS},
                  {"novice": {"trampled": True}, "systematic": {"trampled": True, "n": g["n"]},
                   "expert": {"trampled": True, "n": g["n"], "gap": gap}})

    # ---------------------------------------------------------- Group: the fox
    def _fox(self, d, y, s, sd, acts):
        f, K = self.fox, KINDS["fox"]
        if not f["present"]:
            if s == 2 and sd == 3:
                f["present"] = True                                   # the young disperse in autumn: a fox comes back
            return
        if acts.get("den_control") and s == 0 and sd in (3, 4):
            self.add("fox", 0.0, 4.0)
            if self.rng.random() < 0.6:
                f["present"] = False; f["pos"] = "away"
                return
        day_raid = (s == 0 and sd >= 2) or (s == 1 and sd <= 3)       # cubs to feed: by day, the hens out foraging
        mult = 2.5 if day_raid else (1.5 if s == 2 and sd >= 2 else 1.0)
        ph = self.voles[y]
        mult *= 2.0 if ph == "crash" else (0.6 if ph == "peak" else 1.0)
        if f["pos"] == "away":
            if d < f["off_until"] or d < f["wary_until"]:
                return
            p = min(0.9, 0.08 * mult) if self.hens > 0 else 0.0
            knows = 1 <= d - f["found"] <= 2
            if knows:
                p = K["return_p"]
            if self.rng.random() < p:
                if knows:
                    f["pos"], f["t"] = "target", d                    # back tomorrow night; the feathers were the sign
                elif self.rng.random() > K["lead_sign_p"]:
                    f["pos"], f["t"] = "target", d - 1                # straight in tonight, no sign before
                else:
                    f["pos"], f["t"] = "about", d
                    self.sign(d + 1, "fox", "blackbirds chinking at the hedge at dusk",
                              {"novice": 0.3, "systematic": 0.5, "expert": 0.8},
                              {"systematic": {"alarm": "something low"}, "expert": {"alarm": "fox"}})
        if f["pos"] == "about":
            if d - f["t"] >= K["lead_nights"] - 1:
                f["pos"], f["t"] = "target", d
            return
        if f["pos"] == "target" and d > f["t"]:
            self.ev(d, "fox_visit", 1)
            self.ev(d, "fox_day", int(day_raid))
            f["pos"] = "away"
            safe = acts.get("pen_hens") if day_raid else acts.get("shut_hens")
            if acts.get("dog") or acts.get("geese"):
                if self.rng.random() < K["turn_p"]:
                    f["off_until"] = d + K["off_days"]                 # scared off; the same scare works again (D2-198)
                    self.ev(d, "fox_turned", 1)
                    if acts.get("dog") and self.rng.random() < 0.1:
                        f["wary_until"] = d + K["wary_after_harm"]
                    return
            if safe:
                if self.rng.random() < 0.05:                          # a door left open
                    k = min(self.hens, K["surplus"])
                else:
                    return
            else:
                k = min(self.hens, K["hens_per_visit"])
            self.hens -= k
            self.add("fox", -k * self.hen_food)
            f["found"] = d
            self.sign(d + 1, "fox", "feathers and a musky stink by the hen house", {lv: 0.95 for lv in LEVELS},
                      {lv: {"fox_kill": True} for lv in LEVELS})
        if d % Y == Y - 1:
            self.hens = 24

    # ---------------------------------------------------------- Flock: the hard-weather birds
    def _fowl(self, d, y, s, sd, acts):
        K, D = KINDS["fowl"], self.drv
        if d + 1 < D.n and D.frozen[d + 1] and not D.frozen[d]:
            self.ev(d + 1, "freeze_start", 1)
            if self.rng.random() < K["lead_sign_p"]:
                self.sign(d, "fowl", "lines of plovers going west all day, high and fast",
                          {"novice": 0.6, "systematic": 0.8, "expert": 0.9},
                          {"novice": {"birds": "flying over"}, "systematic": {"plovers": "west"}, "expert": {"plovers": "west"}})
        elif s in (2, 3, 0) and not D.frozen[d] and self.rng.random() < K["false_sign_p"]:
            self.sign(d, "fowl", "lines of plovers going west all day, high and fast",
                      {"novice": 0.6, "systematic": 0.8, "expert": 0.9},
                      {"novice": {"birds": "flying over"}, "systematic": {"plovers": "west"}, "expert": {"plovers": "west"}})
        if s in (2, 3, 0) and self.rng.random() < 0.3:
            self.sign(d, "fowl", "birds overhead", {"novice": 0.8}, {"novice": {"birds": "flying over"}})
        nets_ready = d - 3 <= getattr(self, "_nets", -9) < d            # nets and decoys set on an earlier day
        if acts.get("set_nets") and not nets_ready:
            self.add("fowl", 0.0, 1.0)
            self._nets = d
        if acts.get("fowl") and nets_ready:
            self._nets = d
            fr = min(2, int(D.frun[d]))
            present = self.flock * (0.3 if d < self.flock_off_until else 1.0) * (1.0 if s in (2, 3, 0) else 0.1)
            birds = present * K["rate"][fr]
            self.flock_taken += birds
            self.add("fowl", birds * K["bird_food"], 2.0)
            if self.rng.random() < K["off_p"]:
                self.flock_off_until = d + 1 + K["off_days"]           # scared off for a day; back after (D2-198)
        if d % Y == Y - 1 and self.flock_taken > 0.2 * self.flock:     # restraint: over-taking in a freeze thins next winter's flock
            self.flock *= max(0.4, 1 - 0.8 * (self.flock_taken / self.flock - 0.2))

    # ---------------------------------------------------------- Run: the silver eels
    def _eels(self, d, y, s, sd, acts):
        K, D = KINDS["eels"], self.drv
        if not self.river or not (s == 2 or (s == 3 and sd <= 1)):
            return
        f = K["base"]
        if D.rising[d] and D.dark[d]:
            f *= K["dark_rising"]
        elif D.rising[d]:
            f *= K["rising"]
        if D.rising[d] and d and D.dry[d - 1] >= 3:
            f *= K["after_dry"]
        if not D.dark[d]:
            f *= K["moonlit"]
        run = self.eel_left * min(0.6, f)
        self.eel_left -= run
        self.ev(d, "eel_night", int(f >= 0.15))
        self.ev(d, "eel_run", run)
        if acts.get("traps"):
            crew = acts.get("weir_crew")                               # hands at the weir to empty the traps through the night
            self.add("eels", run * (0.8 if crew else K["trap_share"]) * K["eel_food"], 2.0 + (4.0 if crew else 0.0))
        if D.rain[d] >= 4 and d and D.dry[d - 1] >= 3:
            self.sign(d, "eels", "the first heavy rain after the dry weeks", {lv: 1.0 for lv in LEVELS},
                      {"novice": {"rain": "heavy"}, "systematic": {"rain_after_dry": True}, "expert": {"rain_after_dry": True}})
        elif D.rain[d] >= 4:
            self.sign(d, "eels", "heavy rain", {lv: 1.0 for lv in LEVELS},
                      {"novice": {"rain": "heavy"}, "systematic": {"rain": "heavy"}, "expert": {"rain": "heavy"}})
        if acts.get("traps") and run * K["trap_share"] > 3:
            self.sign(d + 1, "eels", "the traps full at the weir this morning", {lv: 1.0 for lv in LEVELS},
                      {lv: {"traps_full": True} for lv in LEVELS})

    # ---------------------------------------------------------- Load: voles in the stores and the hay
    def _voles(self, d, y, s, sd, acts):
        K = KINDS["voles"]
        V = self.V
        if s == 1 and sd == 3 and acts.get("mow", True):  # noqa              # haymaking drives the voles to the ricks for two days
            self._mow_until = d + 2
        bump = 2.0 if d <= getattr(self, "_mow_until", -1) else 1.0
        if s in (1, 2, 3):
            rate = K["store_rate"] * V * bump * (K["cats"] if acts.get("cats") else 1.0) * (K["owls"] if acts.get("owls") else 1.0)
            self.add("voles", -rate * self.stores)
            if s == 3:
                self.add("voles", -K["hay_rate"] * max(0, V - 1) * self.hay / S)
        if self.voles[y] == "peak" and s == 2 and sd == 6:
            self.ev(d, "vole_peak", 1)

    # ---------------------------------------------------------- Load: wasps at the fruit and the hives
    def _wasps(self, d, y, s, sd, acts):
        K, D = KINDS["wasps"], self.drv
        if s == 0 and sd in (4, 5, 6):
            hi = self.Q * float(np.exp(0.3 * self.rng.standard_normal()))      # a count of queens is a sample
            self.sign(d, "wasps", "queen wasps at every sunny wall", {"novice": 0.4, "systematic": 0.6, "expert": 0.85},
                      {"novice": {"wasps": True}, "systematic": {"queens": "many" if hi > 1.3 else "few"},
                       "expert": {"queens": "many" if hi > 1.3 else ("some" if hi > 0.8 else "few")}})
        active = (s == 1 and sd >= 4) or (s == 2 and sd <= 5)
        if s == 2 and D.low[d] < 0:
            self._wasp_frost = y
        if not active or getattr(self, "_wasp_frost", -1) == y:
            return
        if s == 1 and sd == 4:                                         # the summer decides how far the nests grow
            dry_hot = D.anom(y, 1, "T") > 1.0 and D.anom(y, 1, "wet") < -0.1
            self.Wn = self.Q * float(np.exp(0.5 * D.anom(y, 1, "T") / 2 - (0.4 if dry_hot else 0.0) + 0.2 * self.rng.standard_normal()))
        Wn = getattr(self, "Wn", self.Q)
        a = Wn * (1.5 if D.temp[d] > 17 else 1.0) * (0.5 if self.nests_taken else 1.0)
        if s == 1 and sd == 5:
            self.ev(d, "wasp_year", int(Wn > 1.3))
        if acts.get("take_nests") and not self.nests_taken:
            self.nests_taken = True
            self.add("wasps", 0.0, 3.0)
        if acts.get("pick_early") and not self.fruit_picked:
            self.fruit_picked = True
            self.add("wasps", -0.15 * self.fruit)
        if not self.fruit_picked:
            self.add("wasps", -K["fruit_rate"] * a * self.fruit)
        self.add("wasps", -K["honey_rate"] * a * self.honey * (0.3 if acts.get("narrow_hives") else 1.0), K["sting_units"] * a)
        if a > 1.2:
            self.sign(d + 1, "wasps", "the fallen apples crawling with wasps", {lv: 0.9 for lv in LEVELS},
                      {lv: {"wasps_at_fruit": True} for lv in LEVELS})

    # ---------------------------------------------------------- Load: slugs at the seedlings
    def _slugs(self, d, y, s, sd, acts):
        K, D = KINDS["slugs"], self.drv
        shift = acts.get("sow_later", 0) if s == 0 else 0
        span = 1 if shift else 3
        window = (s == 0 and shift <= sd <= shift + span) or (s == 2 and 2 <= sd <= 5)
        if not d:
            return
        if acts.get("ducks"):
            pass
        a = 0.0
        if D.rain[d - 1] >= 2.0:
            a = 2.0 if (d >= 2 and D.dry[d - 2] >= 3) else 1.0
        a *= self.L
        if window:
            self.ev(d, "slug_night", int(a >= 1.2))
        if s == 2 and sd == 2 and acts.get("roll"):
            self.add("slugs", 0.0, 4.0); self._rolled = y
        if window and a > 0:
            share = 0.4 if s == 0 else 0.6
            self.add("slugs", -K["rate"] * a * share * self.crop * (0.5 if s == 2 and getattr(self, "_rolled", -1) == y else 1.0))
            self.sign(d + 1, "slugs", "slime trails silver across the seed bed", {lv: 0.7 for lv in LEVELS},
                      {lv: {"slime": True} for lv in LEVELS})
        if window and shift and sd == shift:
            self.add("slugs", -0.03 * (0.4 if s == 0 else 0.6) * self.crop)   # sowing late costs some yield
