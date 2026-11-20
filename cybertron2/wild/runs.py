"""The runs along the river (build brief 5 §2, §3, §3a, §4; proposals/river_and_water.md; D2-209): a rule over any kind with a
`RUNS` row (`mover: run` in its traits), never naming one.

**The river as the runs see it.** The land summary's `down` gives each river area the area its water flows to. A village's home area
and its ring are one stretch of river (`v:<node>`): the chain of areas follows each area's largest river cell, so it passes the
ring beside the small home area (brief §2.4), and a run at a village's water is the run in either. Every other river area is a
stretch of its own. Each stretch knows the stretch below it, the stretches above it, its river length and its catchment (the nodes
whose weather falls on it and every stretch above, weighted by river length).

**A run** is a list of pulses, each {k: kind, g: stretch, d: the ecology day it is at that stretch, n: heads, dir, to: an up-run's
spawning stretch, held: stopped below a dam}. A pulse at a stretch on day d is there that day and night: people take from it (the
engine reads its density), weirs and the race trap take their share in the night (the engine), and then `advance` moves it on.

- **The cue** (the kind's `cue`, read over the catchment): `rain_after_dry` (a heavy rain after dry days) or `spate` (the catchment's
  rain over its mean). The run starts on its cue night: the engine calls `advance` in the night before with tomorrow's weather.
- **Down** (the silver eels): at the window's first day each river area's runners for the year are `year` of its stock; each cue
  night `night` of those left run, leaving the area's count as they go, so the run thins as it is taken and what reaches the sea is
  gone. The stock is made up by the ecology's own breeding (the elvers in spring).
- **Up** (salmon, lamprey): the run of each head-water stretch returns from the spawners that reached it a year before (Beverton-Holt:
  `r` a spawner, at most `cap_km` a km of its river), entering at its river's mouth a share each cue night and the rest on the
  window's last day, and travelling up the stretches to it. A shut dam stops `stop` of it as it arrives below (held there that day
  and night, then gone back to the sea).
- **The lag:** a pulse moves to the next stretch after max(1, round(km / `km_a_day`)) days, km the mean of the two stretches' river.

Pure functions of the state, the land and the weather: the engine replays exactly.
"""
from __future__ import annotations

import math

from cybertron2.wild import kinds as WK

RAIN_MEAN = 3.4                                   # the climate's mean rain a day (as ecology.RAIN_MEAN)
MEMORY = 4                                        # days of rain kept by node


def runners(kinds=None, off=()) -> dict:
    """The kinds that run, with their rows; none of those a world switches off (`off`: the model's runs_off, W-69)."""
    return {k: r for k, r in sorted(WK.RUNS.items()) if k in (kinds if kinds is not None else WK.KINDS) and k not in off}


def runners_of(m) -> dict:
    """The kinds that run in a model's world."""
    return runners(m.kinds, getattr(m, "runs_off", ()))


# ---------------------------------------------------------------------- the river as stretches
class Net:
    """The stretches of river of one world's land (built once from the land summary; not state)."""

    def __init__(self, land: dict, ids: list):
        A = land["areas"]
        self.ix = {a: i for i, a in enumerate(ids)}
        down = land.get("down") or {}
        self.group = {}
        for a in ids:
            x = A[a]
            self.group[a] = f"v:{x['node']}" if x.get("kind") in ("home", "ring") and x.get("node") else a
        river = [a for a in ids if float(A[a].get("river_km", 0.0)) > 0 and a in down]
        self.members = {}
        for a in river:
            self.members.setdefault(self.group[a], []).append(a)
        for g, ms in self.members.items():                                  # a village's whole stretch: its home and ring
            if g.startswith("v:"):
                for a in ids:
                    if self.group[a] == g and a not in ms:
                        ms.append(a)
                ms.sort(key=lambda a: int(a[1:]) if a[1:].isdigit() else 0)
        self.km = {g: sum(float(A[a].get("river_km", 0.0)) for a in ms) for g, ms in self.members.items()}
        self.big = {g: sum(float(A[a].get("big_river_km", 0.0)) for a in ms) for g, ms in self.members.items()}
        self.below = {}
        for g, ms in sorted(self.members.items()):
            outs = [down[a] for a in ms if a in down and (down[a] == "out" or self.group.get(down[a]) != g)]
            to = None
            for o in sorted(outs, key=lambda o: (o == "out", o)):              # a stretch's own way down (the ring's, for a village)
                if o != "out" and self.group.get(o) in self.members:
                    to = self.group[o]
                    break
            self.below[g] = to
        for g in sorted(self.below):                                        # a chain that comes back on itself is cut
            seen, x = [], g
            while x is not None and x not in seen:
                seen.append(x)
                x = self.below.get(x)
            if x is not None:
                self.below[seen[-1]] = None
        self.above = {g: sorted(h for h, t in self.below.items() if t == g) for g in self.members}
        # where each stretch's density is read by the engine: a village's home area (its water), else the area itself
        self.area = {}
        for g, ms in self.members.items():
            home = [a for a in ms if A[a].get("kind") == "home"]
            self.area[g] = self.ix[home[0] if home else ms[0]]
        self.node = {g: A[self.members[g][0]].get("node") for g in self.members}
        self.catch = {}                                                     # the catchment's weather, by node and river length
        for g in self.members:
            wts = {}
            for h in self.upstream(g):
                for a in self.members[h]:
                    nd = A[a].get("node")
                    wts[nd] = wts.get(nd, 0.0) + max(float(A[a].get("river_km", 0.0)), 1e-3)
            tot = sum(wts.values()) or 1.0
            self.catch[g] = {nd: x / tot for nd, x in sorted(wts.items())}

    def upstream(self, g) -> list:
        """The stretch and every stretch above it."""
        out, todo = [], [g]
        while todo:
            x = todo.pop()
            if x in out:
                continue
            out.append(x)
            todo += self.above.get(x, [])
        return out

    def mouth(self, g) -> str:
        while self.below.get(g) is not None:
            g = self.below[g]
        return g

    def path_up(self, dest) -> list:
        """The stretches from the mouth up to `dest`."""
        p = [dest]
        while self.below.get(p[-1]) is not None:
            p.append(self.below[p[-1]])
        return p[::-1]

    def heads(self, where) -> list:
        """The head-water stretches (none above) of the rivers a kind runs: any river, or a river whose mouth stretch holds big river."""
        out = []
        for g in sorted(self.members):
            if self.above.get(g) or self.km[g] <= 0:
                continue
            if where == "big river" and not any(self.big[h] > 0 for h in self.path_up(g)):
                continue
            out.append(g)
        return out

    def lag(self, a, b, km_a_day) -> int:
        return max(1, int(round((self.km.get(a, 0.0) + self.km.get(b, 0.0)) / 2.0 / float(km_a_day))))


def net(m):
    """The model's river (cached on it: rebuilt from the land summary)."""
    n = m.__dict__.get("_runs_net")
    if n is None:
        n = Net(m.land, m.ids)
        m.__dict__["_runs_net"] = n
    return n


def active(m) -> bool:
    """Whether the land has a river that a kind runs (a world without rivers, or without a running kind, is as it was)."""
    return bool(net(m).members) and bool(runners_of(m))


def on_river(m, node) -> bool:
    """Whether a village's water lies on a river that runs (its stretch is part of the river)."""
    return f"v:{node}" in net(m).members


# ---------------------------------------------------------------------- the cue and the window
def _window(m, day, seasons) -> tuple:
    Y, S = m.Y, m.S
    si, sd = (day % Y) // S, day % S
    w = seasons.get(si) if isinstance(seasons, dict) else None
    if w is None:
        w = seasons.get(str(si)) if isinstance(seasons, dict) else None
    if w is None:
        return False, False, False
    lo, hi = int(w[0]), int(w[1])
    first = all(not _in(seasons, (day - 1) % Y, Y, S) for _ in [0]) and lo <= sd <= hi
    return lo <= sd <= hi, first, sd == hi and not _in(seasons, (day + 1) % Y, Y, S)


def _in(seasons, yd, Y, S) -> bool:
    si, sd = yd // S, yd % S
    w = seasons.get(si, seasons.get(str(si)))
    return w is not None and int(w[0]) <= sd <= int(w[1])


def catch_rain(nt, g, mem, lag) -> float:
    """The catchment's rain `lag` days back (0: the cue's own day)."""
    return sum(x * float((mem.get(nd) or [0.0] * MEMORY)[lag] if lag < len(mem.get(nd) or []) else 0.0)
               for nd, x in nt.catch[g].items())


def cued(nt, g, cue, mem) -> bool:
    for key, v in (cue or {}).items():
        if key == "rain_after_dry":
            if catch_rain(nt, g, mem, 0) < 1.5 * RAIN_MEAN or any(catch_rain(nt, g, mem, j) >= 0.5 * RAIN_MEAN for j in range(1, int(v) + 1)):
                return False
        elif key == "spate":
            if catch_rain(nt, g, mem, 0) < float(v) * RAIN_MEAN:
                return False
    return True


# ---------------------------------------------------------------------- the state
def state(st) -> dict:
    return st.setdefault("runs", {"pulses": [], "quota": {}, "due": {}, "spawned": {}, "rain": {}, "year": {}, "tally": {}})


def ended(m, day, seasons) -> bool:
    """Whether a kind's window ended yesterday (its year's run is over)."""
    return _window(m, day - 1, seasons)[2]


def seed(m, st) -> None:
    """At world build: each head water's spawners for the first return (`seed_km` a km of its river)."""
    nt = net(m)
    R = state(st)
    for k, r in runners_of(m).items():
        if r["dir"] != "up":
            continue
        ret = r["return"]
        R["spawned"][k] = {g: round(float(ret["seed_km"]) * nt.km[g], 4) for g in nt.heads(r.get("where", "river"))}


def today(m, st, day) -> list:
    """The pulses at a stretch on this ecology day."""
    return [p for p in (st.get("runs") or {}).get("pulses") or [] if int(p["d"]) == int(day) and float(p["n"]) > 1e-9]


def density(m, st, day) -> dict:
    """{kind: [heads a km2 by area]} of the runs there today, at each stretch's area (a village's home)."""
    nt = net(m)
    out = {}
    for p in today(m, st, day):
        i = nt.area.get(p["g"])
        if i is None:
            continue
        out.setdefault(p["k"], [0.0] * m.n)[i] += float(p["n"]) / float(m.km2[i])
    return out


def take_one(m, st, day, kind, i) -> bool:
    """One head of a run taken at area i today (the largest pulse there first). Returns whether there was one."""
    nt = net(m)
    ps = [p for p in today(m, st, day) if p["k"] == kind and nt.area.get(p["g"]) == i and float(p["n"]) >= 1.0 - 1e-9]
    if not ps:
        return False
    p = sorted(ps, key=lambda p: (-float(p["n"]), bool(p.get("held")), p["g"]))[0]
    p["n"] = round(float(p["n"]) - 1.0, 4)
    return True


def take_share(st, day, g, share, dirs=("down", "up"), kinds=None, room=None, worth=None) -> dict:
    """A share of every pulse at stretch g today (a weir, the race): {kind: heads taken}, the pulses thinned. With `room` (food) and
    `worth` ({kind: food a head}), the take is cut, kind by kind in proportion, to what there is room for (a weir's hold, D2-210)."""
    want = []
    for p in today(None, st, day):
        if p["g"] != g or p["dir"] not in dirs or (kinds is not None and p["k"] not in kinds):
            continue
        n = float(p["n"])
        q = math.floor(n * float(share) + 0.5) if n >= 1 else 0
        if q > 0:
            want.append([p, q])
    if room is not None and want:
        food = sum(q * float((worth or {}).get(p["k"], 0.0)) for p, q in want)
        if food > float(room) + 1e-9:
            f = max(0.0, float(room)) / food
            for x in want:
                x[1] = math.floor(x[1] * f + 1e-9)
    out = {}
    for p, q in want:
        if q <= 0:
            continue
        p["n"] = round(float(p["n"]) - q, 4)
        out[p["k"]] = out.get(p["k"], 0) + int(q)
    return out


def flow(nt, g, mem, flow_at) -> str:
    """The river's flow at a stretch tonight, from its catchment's rain (today and half of yesterday's, over the mean; until a river
    level exists, D2-210): the first class whose bound it is under, else the last ("flood")."""
    r = (catch_rain(nt, g, mem, 0) + 0.5 * catch_rain(nt, g, mem, 1)) / RAIN_MEAN
    for bound, name in flow_at:
        if r < float(bound):
            return name
    return "flood"


# ---------------------------------------------------------------------- the night
def _merge(pulses) -> list:
    keyed = {}
    for p in pulses:
        if float(p["n"]) <= 1e-6:
            continue
        key = (p["k"], p["g"], int(p["d"]), p["dir"], p.get("to"), bool(p.get("held")))
        if key in keyed:
            keyed[key]["n"] = round(float(keyed[key]["n"]) + float(p["n"]), 4)
        else:
            keyed[key] = dict(p, n=round(float(p["n"]), 4))
    return [keyed[k] for k in sorted(keyed, key=lambda t: (t[0], t[1], t[2], t[3], str(t[4]), t[5]))]


def _calendar_cue(m, day, seasons) -> bool:
    """Without the climate (every day's rain the same), a run goes on set nights of its window: `no_weather` days from its start."""
    Y, S = m.Y, m.S
    yd = day % Y
    k = 0
    while k < Y and _in(seasons, (yd - k - 1) % Y, Y, S):
        k += 1
    return k in tuple(WK.RUN.get("no_weather", (1, 4)))


def advance(m, st, day, wx, ahead, stops=None, weather=True) -> dict:
    """The night of ecology day `day`, after the day's takes: the pulses there today move on (or reach the sea, or spawn); the cue on
    `day + 1` (`ahead`, tomorrow's weather by node; `weather` False: a world without the climate, on set nights) starts new pulses; a shut dam (`stops`: {stretch: share}) holds its share of an
    up-run arriving tomorrow. Returns what happened, for the engine: {"sea": {k: n}, "spawned": {k: n}, "started": {k: n}}."""
    eff = {"sea": {}, "spawned": {}, "started": {}}
    if not active(m):
        return eff
    nt = net(m)
    R = state(st)
    K = runners_of(m)
    mem = R.setdefault("rain", {})
    for nd in sorted({n_ for g in nt.catch for n_ in nt.catch[g]}):        # today's rain into the memory
        mem[nd] = [round(float((wx.get(nd) or {}).get("rain", 0.0)), 3)] + list(mem.get(nd) or [])[:MEMORY - 1]
    keep = []
    for p in R["pulses"]:
        if int(p["d"]) > day:
            keep.append(p)
            continue
        if int(p["d"]) == day and float(p["n"]) > 1e-6:                     # what passed the stretch this year (its signs)
            ty = R.setdefault("tally", {}).setdefault(p["k"], {}).setdefault(p["g"], {})
            ty[str(day // m.Y)] = round(float(ty.get(str(day // m.Y), 0.0)) + float(p["n"]), 4)
            for y_ in [y_ for y_ in ty if int(y_) < day // m.Y - 1]:
                ty.pop(y_)
        if int(p["d"]) < day or p.get("held") or float(p["n"]) < 1e-6:     # held below a dam: back to the sea
            continue
        r = K.get(p["k"]) or {}
        g = p["g"]
        if p["dir"] == "down":
            nxt = nt.below.get(g)
            if nxt is None:
                eff["sea"][p["k"]] = round(eff["sea"].get(p["k"], 0.0) + float(p["n"]), 4)
                continue
        else:
            if g == p.get("to"):
                sp = R["spawned"].setdefault(p["k"], {})
                sp[g] = round(float(sp.get(g, 0.0)) + float(p["n"]), 4)
                eff["spawned"][p["k"]] = round(eff["spawned"].get(p["k"], 0.0) + float(p["n"]), 4)
                continue
            path = nt.path_up(p["to"])
            nxt = path[path.index(g) + 1] if g in path and path.index(g) + 1 < len(path) else None
            if nxt is None:
                continue
        keep.append(dict(p, g=nxt, d=day + nt.lag(g, nxt, float(WK.RUN["km_a_day"]))))
    new = []
    if ahead is not None:                                                   # tomorrow's cue: the runs start
        cue_mem = {nd: [round(float((ahead.get(nd) or {}).get("rain", 0.0)), 3)] + list(mem.get(nd) or [])[:MEMORY - 1] for nd in mem}
        d1 = day + 1
        yr = d1 // m.Y
        for k, r in K.items():
            inside, first, last = _window(m, d1, r["seasons"])
            if not inside:
                continue
            if r["dir"] == "down":
                q = R["quota"].setdefault(k, {})
                if first or R["year"].get(k) != yr:                         # the year's runners, by area
                    R["year"][k] = yr
                    pop = st["pop"].get(k)
                    q.clear()
                    if pop is not None:
                        for g, ms in sorted(nt.members.items()):
                            for a in ms:
                                i = nt.ix[a]
                                if float(m.land["areas"][a].get("river_km", 0.0)) > 0 or a in m.land.get("down", {}):
                                    c = float(pop[i]) * float(m.km2[i]) * float(r["year"])
                                    if c > 1e-6:
                                        q[a] = round(c, 4)
                pop = st["pop"].get(k)
                cal = _calendar_cue(m, d1, r["seasons"]) if not weather else False
                for g in sorted(nt.members):
                    if not (cal if not weather else cued(nt, g, r["cue"], cue_mem)):
                        continue
                    for a in nt.members[g]:
                        left = float(q.get(a, 0.0))
                        if left <= 1e-6 or pop is None:
                            continue
                        i = nt.ix[a]
                        have = float(pop[i]) * float(m.km2[i])
                        n = min(have, left * float(r["night"]) if not last else left)
                        if n < 1e-6:
                            continue
                        pop[i] = max(0.0, (have - n) / float(m.km2[i]))
                        q[a] = round(left - n, 4)
                        new.append({"k": k, "g": g, "d": d1, "n": round(n, 4), "dir": "down"})
                        eff["started"][k] = round(eff["started"].get(k, 0.0) + n, 4)
                st["pop"][k] = [round(float(x), 6) for x in pop] if pop is not None else st["pop"].get(k)
            else:
                due = R["due"].setdefault(k, {})
                if first or R["year"].get(k) != yr:                         # the return: from last year's spawners
                    R["year"][k] = yr
                    ret = r["return"]
                    due.clear()
                    for g, s in sorted((R["spawned"].get(k) or {}).items()):
                        cap = float(ret["cap_km"]) * max(nt.km.get(g, 0.0), 1e-6)
                        n = float(ret["r"]) * float(s) / (1.0 + float(s) / cap)
                        if n > 1e-6:
                            due[g] = round(n, 4)
                    R["spawned"][k] = {}
                for dest in sorted(due):
                    left = float(due[dest])
                    mouth = nt.mouth(dest)
                    if left <= 1e-6 or not (last or (cued(nt, mouth, r["cue"], cue_mem) if weather else _calendar_cue(m, d1, r["seasons"]))):
                        continue
                    n = left if last else left * float(r["night"])
                    due[dest] = round(left - n, 4)
                    new.append({"k": k, "g": mouth, "d": d1, "n": round(n, 4), "dir": "up", "to": dest})
                    eff["started"][k] = round(eff["started"].get(k, 0.0) + n, 4)
    out = []
    for p in keep + new:                                                    # tomorrow's arrivals: a shut dam holds its share
        s_ = float((stops or {}).get(p["g"], 0.0)) if p["dir"] == "up" and int(p["d"]) == day + 1 and not p.get("held") else 0.0
        n = float(p["n"])
        held = math.floor(n * s_ + 0.5) if s_ > 0 else 0
        if held > 0:
            out.append(dict(p, n=float(held), held=True))
            n -= held
        out.append(dict(p, n=round(n, 4)))
    R["pulses"] = _merge(out)
    return eff
