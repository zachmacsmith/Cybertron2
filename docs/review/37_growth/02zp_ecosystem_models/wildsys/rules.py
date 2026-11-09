"""The general rules of the wild systems (proposals/wild_systems.md §10; 02zp part six). No kind is named in this file: every kind
is a data row in kinds.py, and these rules read only the row's fields (checked by check.py).

Time is the engine's: Y days a year, four seasons of S days (Y = 32). Weather comes from the engine's climate (D4-109) at the
village's node. Leads and creature memory are in engine days, at least one (D2-197): a sign seen on day t leads an event on night
t+1 or later. Answers to scares by kind (D2-198): "habituate" (gets used to it), "scared_off", "leaves" (for good), "none".

Rules:
  Pulse  a yearly resource with a rhythm and a spoiler (mast), shared by a world's villages
  Group  a group near the village that sets out toward a target on a drive, with a lead stage that leaves signs, memory of a
         success, an answer to scares, and harm from people (a dog, a kill)
  Load   an area-level number (rats, birds) active in windows, with levers that cut it and an answer to scares
  Run    a seasonal run on conditions, taken at a weir
  Flock  visitors that come with a driver (a freeze), weaken as it runs, and are scared off by disturbance
A rule emits moments (set out, at the edge, raid, turned, active ...); the kind's row maps a moment to a sign (SIGNS in kinds.py),
which an observer reads at its level (observe.py).
"""
from __future__ import annotations

import numpy as np

Y, S = 32, 8
LEVELS = ("novice", "systematic", "expert")


def season(d):
    return (d % Y) // S


def sday(d):
    return d % S


def in_windows(d, windows):
    """windows: [(season, first day, last day), ...]."""
    s, sd = season(d), sday(d)
    return any(s == a and b <= sd <= c for a, b, c in windows)


# ------------------------------------------------------------------ drivers
class Drivers:
    def __init__(self, wx, normals=None):
        n = len(wx)
        self.n = n
        self.temp = np.array([x["temp"] for x in wx]); self.low = np.array([x["low"] for x in wx])
        self.rain = np.array([x["rain"] for x in wx])
        self.frozen = (self.low < -3.0) & (self.temp < 3.0)              # a hard frost: the ground sealed
        self.snow = np.zeros(n, bool)
        self.frun = np.zeros(n, int); self.dry = np.zeros(n, int); self.river = np.zeros(n)
        for d in range(n):
            self.frun[d] = (self.frun[d - 1] + 1) if (d and self.frozen[d]) else int(self.frozen[d])
            self.dry[d] = (self.dry[d - 1] + 1) if (d and self.rain[d] < 2.0) else int(self.rain[d] < 2.0)
            self.river[d] = (0.5 * self.river[d - 1] + self.rain[d - 1]) if d else 0.0
            self.snow[d] = (self.low[d] < 0 and self.rain[d] > 1) or bool(d and self.snow[d - 1] and self.temp[d] < 3)
        self.rising = np.r_[False, np.diff(self.river) > 2.0]
        real = np.arange(n) * 365.0 / Y / 29.53
        ph = real - np.floor(real)
        self.dark = np.minimum(ph, 1 - ph) < 0.2
        self.years = n // Y
        seg = lambda a, y, s: a[y * Y + s * S: y * Y + (s + 1) * S]
        self.seas = [{s: {"T": float(seg(self.temp, y, s).mean()), "wet": float((seg(self.rain, y, s) > 2).mean()),
                          "maxrun": int(seg(self.frun, y, s).max())} for s in range(4)} for y in range(self.years)]
        self.normals = normals or {s: {k: float(np.mean([r[s][k] for r in self.seas])) for k in ("T", "wet")} for s in range(4)}
        self.flower_frost = [bool((self.low[y * Y + 5: y * Y + 8] < -1.5).any()) for y in range(self.years)]

    def anom(self, y, s, k):
        y = max(0, min(self.years - 1, y))
        return self.seas[y][s][k] - self.normals[s][k]

    def hard_winter(self, y):
        return self.seas[max(0, min(self.years - 1, y))][3]["maxrun"] >= 2


# ------------------------------------------------------------------ Pulse
def pulse_series(row, years, rng, spoiled):
    """A budget builds a year at a time; when it reaches its threshold the pulse comes, unless spoiled; the year after a pulse fails
    (spent). row["levels"]: {"heavy", "ordinary", "poor", "fail"}; returns (levels, budget_full)."""
    L = row["levels"]
    out, full, B, th = [], [], 0, int(rng.integers(*row["every"]))
    for y in range(years):
        B += 1
        spent = bool(out) and out[-1] == L["heavy"]
        full.append(B >= th and not spent)
        if spent:
            lvl = L["fail"]
        elif B >= th:
            lvl = L["fail"] if spoiled[y] else L["heavy"]
            if lvl == L["heavy"]:
                B, th = 0, int(rng.integers(*row["every"]))
        else:
            lvl = L["ordinary"] if rng.random() < row["ordinary_p"] else L["poor"]
            if spoiled[y]:
                lvl = L["fail"]
        out.append(lvl)
    return out, full


# ------------------------------------------------------------------ the shared context a rule sees
class Ctx:
    """What a rule may read: the village (land, stocks, ledger, signs), the drivers, the pulses, the day, the household's acts."""

    def __init__(self, village, d, acts):
        self.v, self.d, self.acts = village, d, acts
        self.D = village.drv
        self.y, self.s, self.sd = d // Y, season(d), sday(d)

    def pulse(self, name, y=None):
        return self.v.pulses[name][0][self.y if y is None else y]

    def pulse_full(self, name, y=None):
        return self.v.pulses[name][1][self.y if y is None else y]

    @property
    def frozen(self):
        return bool(self.D.frun[self.d] >= 1)


def _answer_scare(st, ans, scare, rng, d):
    """D2-198: the chance a harmless scare turns the kind tonight, and what it learns. Returns (turned, off_until)."""
    t = ans["type"]
    if t == "none" or scare is None:
        return False, d
    if t == "habituate":
        p = ans["turn_p"] * (1 - st["habit"].get(scare, 0.0))
        turned = rng.random() < p
        if turned:
            g = ans["gain"].get(scare, ans["gain"].get("other", 0.3)) if isinstance(ans["gain"], dict) else ans["gain"]
            st["habit"][scare] = min(1.0, st["habit"].get(scare, 0.0) + g)
        return turned, d + ans.get("rest", 2)
    if t == "scared_off":
        return rng.random() < ans["turn_p"], d + ans["off_days"]
    if t == "leaves":
        if rng.random() < ans["turn_p"]:
            st["gone"] = True
            return True, 10 ** 9
        return False, d
    raise KeyError(t)


def _decay(st, ans):
    if ans["type"] == "habituate":
        for k in list(st["habit"]):
            st["habit"][k] = max(0.0, st["habit"][k] - ans["decay"])


# ------------------------------------------------------------------ Group
class Group:
    def __init__(self, name, row, village, rng):
        self.name, self.row, self.v, self.rng = name, row, village, rng
        self.st = None
        self.density = row["density"]["start"]

    def new_year(self, c):
        R = self.row["density"]
        prev = c.pulse(R["pulse"], c.y - 1) if (c.y and R.get("pulse")) else R.get("neutral")
        grow = R["grow"][prev] if R.get("pulse") else R["grow"]
        K = R["K"] * (R.get("K_heavy", 1.0) if R.get("pulse") and prev == max(R["grow"]) else 1.0)
        b = self.density + grow * self.density * (1 - self.density / K)
        if c.y and c.D.hard_winter(c.y - 1) and R.get("hard_winter_loss") and prev in R.get("hard_winter_if", ()):
            b *= R["hard_winter_loss"]
        self.density = max(R["floor"], b * R["survive"])
        n = self.row["place"]["size"](self.v.land, self.density)
        if n:
            st = self.st or {"pos": "home", "t": 0, "found": -99, "habit": {}, "wary_until": -1, "rest_until": -1,
                             "gap": int(self.rng.integers(self.v.gaps)), "gone": False}
            st["n"] = n
            self.st = st if not st.get("gone") else st
        else:
            self.st = None

    def present(self):
        return self.st is not None and not self.st.get("gone")

    def _target(self, c):
        R = self.row
        if c.frozen and R.get("frozen"):
            return R["frozen"]
        for w in R["targets"]:
            if in_windows(c.d, w["windows"]):
                return w
        return R["otherwise"]

    def _home_food(self, c):
        hf = self.row["home_food"]
        if c.frozen:
            return hf["frozen"]
        f = hf["by_season"].get(c.s)
        return f(c) if callable(f) else (hf["otherwise"] if f is None else f)

    def step(self, c):
        if not self.present():
            return
        st, R, rng = self.st, self.row, self.rng
        _decay(st, R["answer"])
        tg = self._target(c)
        if st["pos"] == "ready" and c.d == st["raid"]:
            self._raid(c, tg)
        elif st["pos"] == "edge":
            self._edge(c)
        elif st["pos"] == "home" and c.d >= st["rest_until"] and c.d >= st["wary_until"]:
            p = tg["attr"] * (R["drive"]["base"] + R["drive"]["hunger"] * (1 - self._home_food(c)))
            knows = 1 <= c.d - st["found"] <= R["memory_days"]
            if knows:
                p = max(p, R["return_p"] * tg["attr"])
            if rng.random() < p:
                st["gap_tonight"] = st["gap"] if rng.random() < R["gap_loyalty"] else int(rng.integers(self.v.gaps))
                if knows:
                    st["pos"], st["raid"] = "ready", c.d + 1
                else:
                    st["pos"], st["t"] = "edge", c.d
                    self._edge(c)
        tk = R.get("take")
        if tk and c.acts.get(tk["act"]) and st["pos"] == "home":
            self._take(c, tk)

    def _edge(self, c):
        st, R = self.st, self.row
        if self.rng.random() < R["lead_sign_p"]:
            self.v.emit(c.d + 1, self.name, R["moments"]["edge"], n=st["n"], gap=st["gap_tonight"], fresh=True)
        if c.d - st["t"] >= R["lead_nights"] - 1:
            st["pos"], st["raid"] = "ready", c.d + 1

    def _raid(self, c, tg):
        st, R, v = self.st, self.row, self.v
        v.event(c.d, self.name, "raid", 1)
        gap = st["gap_tonight"]
        base = v.stock(tg["target"]) * tg["loss"] * (st["n"] if R.get("per_head") else 1)
        watch = c.acts.get("watch", {})
        scare = watch.get(gap)
        st["pos"] = "home"
        for k in range(1, R.get("trace_days", 0) + 1):
            v.emit(c.d + k, self.name, R["moments"]["edge"], n=st["n"], gap=gap, fresh=False)
        watched_elsewhere = [g for g in watch if g != gap]
        if scare is not None:
            v.event(c.d, self.name, "scare", scare)
            if scare in R.get("harm_scares", {}):
                hp = R["harm_scares"][scare]
                if self.rng.random() < hp["turn_p"]:
                    if self.rng.random() < hp["harm_p"]:
                        st["wary_until"], st["habit"] = c.d + R["wary_after_harm"], {}
                        v.event(c.d, self.name, "harmed", 1)
                    st["rest_until"] = c.d + R["answer"].get("rest", 2)
                    v.event(c.d, self.name, "turned", 1)
                    v.emit(c.d + 1, self.name, R["moments"]["turned"], gap=gap, scare=scare)
                    return
            else:
                turned, until = _answer_scare(st, R["answer"], scare, self.rng, c.d)
                if turned:
                    st["rest_until"] = until
                    v.event(c.d, self.name, "turned", 1)
                    v.emit(c.d + 1, self.name, R["moments"]["turned"], gap=gap, scare=scare)
                    return
            loss = R["met_share"] * base
            v.emit(c.d + 1, self.name, R["moments"]["not_turned"], gap=gap, scare=scare, n=st["n"])
        else:
            loss = base
            if watched_elsewhere:
                v.emit(c.d + 1, self.name, R["moments"]["missed"], gap=gap, watched=watched_elsewhere, n=st["n"])
        v.lose(self.name, tg["target"], loss)
        v.event(c.d, self.name, "loss", loss)
        st["found"] = c.d
        v.emit(c.d + 1, self.name, R["moments"]["raid"], n=st["n"], gap=gap, share=loss / max(v.stock(tg["target"]), 1e-9))

    def _take(self, c, tk):
        st, v = self.st, self.v
        pass                                                           # the act's work is booked once, by the act (sim.charge)
        sk = c.acts.get("skill", "novice")
        if self.rng.random() < tk["p"][sk]:
            st["n"] -= 1
            self.density = max(self.row["density"]["floor"], self.density - 1 / max(self.row["place"]["habitat"](v.land), 0.1))
            for g, q in tk["goods"].items():
                v.gain(self.name, g, q)
            st["wary_until"], st["habit"] = c.d + self.row["wary_after_harm"], {}
            v.event(c.d, self.name, "taken", 1)
            if st["n"] < self.row["place"]["min_n"]:
                self.st = None
        if tk.get("rights") and v.rights.get(self.name) == "lord":
            v.event(c.d, self.name, "poached", 1)


# ------------------------------------------------------------------ Load
class Load:
    def __init__(self, name, row, village, rng):
        self.name, self.row, self.v, self.rng = name, row, village, rng
        self.scale = row["place"](village.land)
        self.st = {"habit": {}, "off_until": -1}
        self.level = 1.0

    def present(self):
        return self.scale > 0

    def new_year(self, c):
        self.level = self.row["level"](c)

    def step(self, c):
        if not self.present():
            return
        R, v, st = self.row, self.v, self.st
        _decay(st, R["answer"])
        for w in R["windows"]:
            if not in_windows(c.d, w["windows"]):
                continue
            a = self.scale * self.level * w.get("activity", lambda c: 1.0)(c)
            for lever, mult in R.get("levers", {}).items():
                if c.acts.get(lever) or v.built.get(lever):
                    a *= mult
            scare = None
            for sc in R.get("scares", ()):
                if c.acts.get(sc):
                    scare = sc
                    pass                                                           # the act's work is booked once, by the act (sim.charge)
            if scare is not None:
                if c.d < st["off_until"]:
                    a *= R["answer"].get("while_off", 0.2)
                else:
                    turned, until = _answer_scare(st, R["answer"], scare, self.rng, c.d)
                    if turned:
                        a *= R["answer"].get("turned_share", 0.2)
                        if R["answer"]["type"] == "scared_off":
                            st["off_until"] = until
                    v.event(c.d, self.name, "scare", scare)
                    v.event(c.d, self.name, "turned", int(turned))
                    ms = R.get("scare_moments")
                    if ms:
                        v.emit(c.d + 1, self.name, ms["worked" if turned else "failed"], scare=scare)
            loss = w["rate"] * a * v.stock(w["target"])
            v.lose(self.name, w["target"], loss)
            v.event(c.d, self.name, "loss", loss)
            v.event(c.d, self.name, "active", a)
            for m in R.get("moments", []):
                if m["when"](a, c):
                    v.emit(c.d + 1, self.name, m["sign"], level=a)
        tk = R.get("take")
        if tk and c.acts.get(tk["act"]):
            pass                                                           # the act's work is booked once, by the act (sim.charge)
            got = tk["yield"](self.scale * self.level, c)
            for g, q in tk["goods"].items():
                v.gain(self.name, g, q * got)
            self.level *= tk.get("depletes", 1.0)
            if R["answer"]["type"] == "scared_off":
                st["off_until"] = c.d + R["answer"]["off_days"]


# ------------------------------------------------------------------ Run
class Run:
    def __init__(self, name, row, village, rng):
        self.name, self.row, self.v, self.rng = name, row, village, rng
        self.stock0 = row["place"](village.land)
        self.left = 0.0

    def present(self):
        return self.stock0 > 0

    def new_year(self, c):
        self.left = self.stock0

    def morning(self, c):
        if not self.present():
            return
        for m in self.row.get("day_moments", []):                      # signs of the drivers themselves (rain after dry weeks)
            if m["when"](c):
                self.v.emit(c.d, self.name, m["sign"])

    def step(self, c):
        if not self.present():
            return
        R, D, d, v = self.row, c.D, c.d, self.v
        if not in_windows(d, R["windows"]):
            return
        f = R["base"] * R["night"](c)
        run = self.left * min(R["cap"], f)
        self.left -= run
        v.event(d, self.name, "run", run)
        v.event(d, self.name, "big", int(f >= R["big"]))
        tk = R["take"]
        if c.acts.get(tk["act"]):
            crew = c.acts.get(tk["crew_act"])
            share = tk["crew_share"] if crew else tk["share"]
            pass                                                           # the act's work is booked once, by the act (sim.charge)
            for g, q in tk["goods"].items():
                v.gain(self.name, g, q * run * share)
            if run * share >= tk["full_at"]:
                v.emit(d + 1, self.name, R["moments"]["full"], n=int(run * share))
            else:
                v.emit(d + 1, self.name, R["moments"]["few"], n=int(run * share))


# ------------------------------------------------------------------ Flock
class Flock:
    def __init__(self, name, row, village, rng):
        self.name, self.row, self.v, self.rng = name, row, village, rng
        self.size = row["place"](village.land)
        self.off_until = -1
        self.nets = -9
        self.taken = 0.0

    def present(self):
        return self.size > 0

    def new_year(self, c):
        if self.taken > self.row["restraint"] * self.size:
            self.size *= max(0.4, 1 - 0.8 * (self.taken / self.size - self.row["restraint"]))
        self.taken = 0.0

    def morning(self, c):
        if not self.present():
            return
        R, D, d, v = self.row, c.D, c.d, self.v
        # the driver's leading sign: tomorrow's freeze shows today (the cold air ahead of it)
        if d + 1 < D.n and D.frozen[d + 1] and not D.frozen[d] and in_windows(d + 1, R["windows"]):
            v.event(d + 1, self.name, "freeze", 1)
            if self.rng.random() < R["lead_sign_p"]:
                v.emit(d, self.name, R["moments"]["lead"])
        elif in_windows(d, R["windows"]) and not D.frozen[d] and self.rng.random() < R["false_sign_p"]:
            v.emit(d, self.name, R["moments"]["lead"])
        if in_windows(d, R["windows"]) and self.rng.random() < R["background_p"]:
            v.emit(d, self.name, R["moments"]["background"])
        if D.frozen[d] and in_windows(d, R["windows"]):
            v.emit(d, self.name, R["moments"]["crowded"] if D.frun[d] == 1 else R["moments"]["weak"])

    def step(self, c):
        if not self.present():
            return
        R, D, d, v = self.row, c.D, c.d, self.v
        ready = d - 3 <= self.nets < d
        if c.acts.get(R["prepare_act"]) and not ready:
            pass                                                           # the act's work is booked once, by the act (sim.charge)
            self.nets = d
        if c.acts.get(R["take_act"]) and ready:
            self.nets = d
            fr = min(2, int(D.frun[d]))
            present = self.size * (R["while_off"] if d < self.off_until else 1.0) * (1.0 if in_windows(d, R["windows"]) else 0.1)
            got = present * R["rate"][fr]
            self.taken += got
            pass                                                           # the act's work is booked once, by the act (sim.charge)
            for g, q in R["goods"].items():
                v.gain(self.name, g, q * got)
            v.event(d, self.name, "taken", got)
            if self.rng.random() < R["answer"]["off_p"]:
                self.off_until = d + 1 + R["answer"]["off_days"]


RULES = {"Group": Group, "Load": Load, "Run": Run, "Flock": Flock}
