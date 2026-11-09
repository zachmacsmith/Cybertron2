"""The population store and the ecology step (wild_layer.md §3.3, D2-199): every kind's numbers in every area of the land summary,
stepped one engine day at a time on the food web's rules (02zp part two, W2, §11 there). Pure functions of the state, the land, the
day and the weather: no randomness except keyed draws handed in, so the engine replays exactly.

Each day, for every area:
1. **foods grow** (stocks toward their cap, by season and the day's warmth; pulses produced in their seasons, mast by the trees'
   rhythm), and rot;
2. **every kind eats** what its body needs (Kleiber), choosing what is worth most where it stands (fine and coarse food by body
   size), from foods, other kinds (prey), beasts and carrion, never eating anything to the ground; snow buries forage;
3. **condition** follows what it got against what it needed; hunger beyond its reserves kills; crowding and disease kill more;
4. **breeding** at the start of its seasons, by condition and crowding;
5. **movement** along the links between areas toward better land, a share a day; migrants arrive and leave with their seasons; a
   thin immigration from beyond keeps nothing empty for ever.

Densities are a km2 of land, as in the food web; counts are density x area. A season of the food web is S engine days.
"""
from __future__ import annotations

import math

import numpy as np

from cybertron2.wild import kinds as WK

SEASON_T = (9.0, 16.0, 10.0, 3.0)        # the climate's seasonal means (02zp §15): warmth beyond them speeds plant growth
SEASON_DAYS_REAL = 91.0
RAIN_MEAN = 3.4                          # the climate's mean rain a day (calibrate with the climate, task P0)


# ------------------------------------------------------------------ the land as the food web sees it
def features(land: dict) -> tuple:
    """Each area's features (shares of its land, 0 to 1) and food resources (shares of full cover), from the land summary."""
    ids = sorted(land["areas"], key=lambda a: int(a[1:]))
    A = [land["areas"][a] for a in ids]
    km = float(land.get("km", 0.15))
    km2 = np.array([max(a["km2"], 1e-6) for a in A])
    cov = lambda *names: np.array([sum(a["cover"].get(n, 0.0) for n in names) for a in A]) / km2
    eco = lambda *names: np.array([sum(a["eco"].get(n, 0.0) for n in names) for a in A]) / km2
    home = np.array([a["kind"] == "home" for a in A], float)
    ring = np.array([a["kind"] == "ring" for a in A], float)
    wood = cov("forest")
    shrub = cov("scrub")
    grassy = cov("pasture", "meadow")
    heath = cov("heath", "moor")
    field = cov("field")
    wet = np.clip(cov("fen", "saltmarsh") + eco("alder carr", "wet grassland", "reedbed"), 0, 1)
    water = np.clip(cov("water") + np.array([a["lake_km2"] + 0.12 * a["river_km"] * km + 0.6 * a["big_river_km"] * km for a in A]) / km2,
                    0, 1)
    farm = np.clip(home * (field + grassy + cov("built")) + ring * 0.4 * (grassy + field), 0, 1)
    f = {"wood": wood, "shrub": shrub, "open": np.clip(1 - wood - cov("water"), 0, 1), "grassy": grassy, "heath": heath, "wet": wet,
         "water": water, "rock": np.array([a["rock"] for a in A]), "old": np.array([a["old_wood_km2"] for a in A]) / km2,
         "oakbeech": eco("oak-ash wood", "beech wood", "upland oak wood"), "conifer": eco("birch and pine wood") * 0.5, "farm": farm,
         "h": np.array([a["elevation"] for a in A]), "temp": np.array([a["temp"] for a in A]),
         "river": np.clip(np.array([a["river_km"] for a in A]) / np.sqrt(km2), 0, 1),
         "bigriver": np.clip(np.array([a["big_river_km"] for a in A]) / np.sqrt(km2), 0, 1), "land": np.ones(len(A))}
    r = {"grass": grassy * 0.9 + 0.2 * heath, "sward": grassy * 0.6 + 0.3 * farm, "browse": shrub + wood * (1 - wood) + 0.05 * wood,
         "heather": heath, "mast": f["oakbeech"], "nuts": 0.3 * f["oakbeech"] + 0.3 * shrub, "fruit": 0.5 * shrub + 0.1 * wood,
         "roots": 0.3 * wood + 0.5 * grassy, "inverts": (1 - wood) * 0.8 + wood * 0.6, "seeds": grassy + 0.3 * farm,
         "aquatic": wet + 0.5 * water, "fish": water, "crops": home * field, "livestock": home * (grassy + field) * 0.5,
         "stores": home.copy()}
    return ids, km2, f, r


def links(land: dict, ids: list):
    ix = {a: i for i, a in enumerate(ids)}
    L = [(ix[a], ix[b], float(e)) for a, b, e in land["links"] if a in ix and b in ix]
    if not L:
        return np.zeros(0, int), np.zeros(0, int), np.zeros(0)
    a, b, e = (np.array(x) for x in zip(*L))
    return a.astype(int), b.astype(int), e


# ------------------------------------------------------------------ biology (the food web's functions)
def selectivity(mass):
    return float(np.clip(1 - np.log10(max(mass, 1.0) / 2.0) / 2.5, 0, 1))


def expand(diet, mass):
    s = selectivity(mass); out = {}
    for it, p in diet.items():
        if it in WK.SPLIT:
            out[it] = p * (0.3 + 0.7 * s)
            out[it + "~coarse"] = p * (1.05 - s)
        else:
            out[it] = p
    return out


def damuth(mass, cls):
    d = 10 ** (4.23 - 0.75 * np.log10(max(mass, 0.001) * 1000.0))
    return d / 30.0 if cls == "carn" else (d / 3.0 if cls == "omni" else d)


def value(q, mass):
    lift = np.clip(np.log10(max(mass, 1.0) / 20.0) / 1.5, 0, 1) * 0.6
    small = np.clip(1 - np.log10(max(mass, 0.01) / 0.5) / 2.0, 0, 1)
    return (q + (1 - q) * lift) * (1 - 0.8 * small) if q < 0.5 else q


def reserve_seasons(mass, hibernate):
    return (0.12 * mass ** 0.33) * (2.0 if hibernate else 1.0)


def suitability(f, k):
    s = np.zeros(len(f["land"]))
    for fe, w in k["hab"].items():
        s = s + w * f.get(fe, 0.0)
    s = np.clip(s, 0, 1)
    for lim, (lo, hi) in (k.get("limits") or {}).items():
        x = f[lim]; w = 0.15 * abs(hi - lo) + 1e-9
        s = s * np.clip((x - lo) / w, 0, 1) * np.clip((hi - x) / w, 0, 1)
    return s


# ------------------------------------------------------------------ the model of one world's land
class Model:
    """What does not change: the areas, their features and foods, the kinds compiled."""

    def __init__(self, land: dict, kinds: dict | None = None, Y: int = 32, knobs: dict | None = None):
        self.land, self.Y, self.S = land, Y, Y // 4
        self.knobs = knobs or {}
        self.ids, self.km2, self.f, self.res = features(land)
        self.la, self.lb, self.le = links(land, self.ids)
        self.res.update({x + "~coarse": self.res[x] for x in WK.SPLIT})
        self.kinds = {n: dict(k, diet=expand(k["diet"], k["mass"])) for n, k in (kinds or WK.KINDS).items()}
        self.names = list(self.kinds)
        self.suit = {n: suitability(self.f, self.kinds[n]) for n in self.names}
        self.crowd_at = {n: 3.0 * damuth(self.kinds[n]["mass"], self.kinds[n]["cls"]) * self.knobs.get("crowd", 1.0) for n in self.names}
        self.nodes = [land["areas"][a]["node"] for a in self.ids]
        self.home = np.array([land["areas"][a]["kind"] == "home" for a in self.ids])
        self.n = len(self.ids)
        self.cap_stock = 1 - (1 - 0.6) ** (1.0 / self.S)                    # a season's share never eaten (0.6, 0.8), as a day's
        self.cap_other = 1 - (1 - 0.8) ** (1.0 / self.S)
        self.provided = set(self.knobs.get("provided") or ())              # foods the engine supplies (its crops, its stores)
        kind_of = np.array([land["areas"][a]["kind"] for a in self.ids])
        near = {"home": 1.0, "ring": 0.4, "wild": 0.0}                     # people's presence (living_populations §2a: busy land)
        self.busy = np.array([near.get(k, 0.0) for k in kind_of])
        for n_ in self.names:                                              # a shy kind finds busy land worth less
            shy = float(self.kinds[n_].get("shy", 0.8))
            self.suit[n_] = self.suit[n_] * (1 - 0.75 * shy * self.busy)

    def cap(self, food):
        return self.res[food] * WK.FOOD[food]["cap"] * WK.SCALE.get(food.split("~")[0], 1.0)

    def initial(self, seed: int = 0) -> dict:
        """A starting state: each kind at half a real density where its habitat is good, foods at 60% of their caps."""
        st = {"pop": {}, "cond": {}, "stock": {}, "pulse": {}, "carrion": [0.0] * self.n, "mast": {"budget": 0, "th": 3, "years": {}},
              "flower_frost": [False] * self.n, "day": -1}
        for n in self.names:
            k = self.kinds[n]
            st["pop"][n] = list((k["ref"] or 1.0) * k["d0"] * 0.5 * self.suit[n] * (0.0 if k["migrant"] else 1.0))
            st["cond"][n] = [0.6] * self.n
        for fd, sp in WK.FOOD.items():
            if sp["type"] == "stock":
                st["stock"][fd] = list(self.cap(fd) * 0.6)
            elif sp["type"] == "pulse":
                st["pulse"][fd] = [0.0] * self.n
        return st


def mast_level(st: dict, year: int, frost: bool, draw: float) -> float:
    """The year's mast: the trees' budget builds a year at a time; at its threshold the mast comes unless frost spoiled the
    flowering; the year after a heavy mast fails. draw is a keyed uniform number for the year (0 to 1)."""
    M, L = st["mast"], WK.MAST["levels"]
    key = str(year)
    if key in M["years"]:
        return M["years"][key]
    prev = M["years"].get(str(year - 1))
    M["budget"] += 1
    if prev == L["heavy"]:
        lvl = L["fail"]
    elif M["budget"] >= M["th"]:
        lvl = L["fail"] if frost else L["heavy"]
        if lvl == L["heavy"]:
            lo, hi = WK.MAST["every"]
            M["budget"], M["th"] = 0, lo + int((draw * 7.31) % 1.0 * (hi - lo + 1))
    else:
        lvl = L["fail"] if frost else (L["ordinary"] if (draw * 3.7) % 1.0 < WK.MAST["ordinary_p"] else L["poor"])
    M["years"][key] = lvl
    return lvl


def step(m: Model, st: dict, day: int, weather: dict, draws: dict, take: dict | None = None) -> dict:
    """One engine day. weather: {node: {temp, low, rain, snow}} for this day; draws: keyed uniform numbers {"mast": u for the year};
    take: {kind: [per-area share taken today by people]} (the acts), or None for the background take. Returns the day's effects:
    {"eaten": {food: [kg per area]}, "killed": {kind: [head per area]}, "dead": {...}} for the engine's bridge."""
    Y, S, n = m.Y, m.S, m.n
    si, sd = (day % Y) // S, day % S
    year = day // Y
    knobs = m.knobs
    N = {k: np.asarray(v, float) for k, v in st["pop"].items()}
    E = {k: np.asarray(v, float) for k, v in st["cond"].items()}
    stock = {k: np.asarray(v, float) for k, v in st["stock"].items()}
    pulse = {k: np.asarray(v, float) for k, v in st["pulse"].items()}
    carrion = np.asarray(st["carrion"], float)
    temp = np.array([weather[nd]["temp"] for nd in m.nodes]); low = np.array([weather[nd]["low"] for nd in m.nodes])
    snow = np.array([1.0 if weather[nd].get("snow") else 0.0 for nd in m.nodes])
    frozen = (low < -3.0) & (temp < 3.0)
    if si == 0 and 5 <= sd <= 7:                                          # frost at the oaks' flowering spoils the year's mast
        st["flower_frost"] = [bool(x) for x in (np.asarray(st["flower_frost"], bool) | (low < -1.5))]
    if si == 0 and sd == 0:
        st["flower_frost"] = [False] * n
    mast = mast_level(st, year, bool(np.mean(st["flower_frost"]) > 0.3) if si >= 2 else False, draws.get("mast", 0.5)) if si >= 2 else 1.0
    # 1. foods grow and rot: warmth beyond the season's mean speeds growth, frost stops it, a dry ground holds grass back
    rain = np.array([weather[nd].get("rain", 1.0) for nd in m.nodes])
    soil = 0.75 * np.asarray(st.get("soil", [1.0] * n), float) + 0.25 * np.clip(rain / RAIN_MEAN, 0, 3)   # a slow bucket (an
                                                                          # engine day is about 11 real days): 1 at the mean rain
    st["soil"] = [round(float(x), 3) for x in soil]
    from cybertron2.wild import loads as LD
    LD.step(m, st, day, temp, low, frozen, soil)                          # the fast kinds and the year's warmth (wave 3)
    warm = np.clip(1 + 0.08 * (temp - SEASON_T[si]), 0.4, 1.6) * np.where(frozen, 0.3, 1.0)
    dry = np.clip(0.35 + 0.65 * np.minimum(soil / 0.8, 1.2), 0.3, 1.25)
    WATERED = ("grass", "grass~coarse", "sward", "browse", "browse~coarse", "inverts", "roots")
    for fd, B in stock.items():
        cap = m.cap(fd)
        g = WK.FOOD[fd]["grow"][si] / S * warm * (dry if fd in WATERED else 1.0)
        stock[fd] = B + g * cap * np.clip(1 - B / np.maximum(cap, 1e-9), 0, 1) + 0.02 / S * cap * (B < 0.05 * cap)
    for fd, P in pulse.items():
        sp = WK.FOOD[fd]
        boost = mast if fd == "mast" else (np.clip(1 + 0.12 * (temp - SEASON_T[si]), 0.4, 1.8) if fd in ("fruit", "nuts", "seeds") else 1.0)
        if fd == "seeds":
            boost = boost * np.clip(1.25 - 0.25 * soil, 0.6, 1.2)            # a wet summer spoils seed
        prod = m.res[fd] * sp["prod"] * WK.SCALE.get(fd, 1.0) * sp["season"][si] / S * boost * (0.0 if fd in m.provided else 1.0)
        pulse[fd] = P * (1 - sp["rot"]) ** (1.0 / S) + prod * np.where(frozen, 0.4, 1.0)
    avail = {**stock, **pulse, "carrion": carrion}
    present = {k: m.kinds[k]["migrant"] is None or SEASONS_OF[si] in m.kinds[k]["migrant"] for k in m.names}
    if sd == 0:                                                            # migrants come and go with their seasons
        for k in m.names:
            kd = m.kinds[k]
            if kd["migrant"] is not None:
                if not present[k]:
                    N[k] = N[k] * 0.0
                elif SEASONS_OF[si] == kd["migrant"][0]:
                    N[k] = kd["arrive"] * m.suit[k] * knobs.get("arrive", 1.0)
    for k in m.names:
        kd = m.kinds[k]
        refuge = 0.1 * m.crowd_at[k] / 3.0 * m.suit[k]
        avail["kind:" + k] = np.maximum(N[k] - refuge, 0) * kd["mass"] * kd["vuln"] if present[k] else np.zeros(n)
    # 2. eating
    want, need = {}, {}
    for k in m.names:
        kd = m.kinds[k]
        if not present[k] or (kd["hibernate"] and si == 3):
            continue
        base = N[k] * WK.KLEIBER[kd["cls"]] * kd["mass"] ** 0.75 * SEASON_DAYS_REAL / S
        need[k] = base
        hungry = base * (1.0 + 0.4 * np.clip(1 - E[k], 0, 1))
        if kd["cls"] == "carn":
            hungry = hungry / (1.0 + N[k] / np.maximum(m.crowd_at[k] * m.suit[k], 1e-9))
        items = [(it, p) for it, p in kd["diet"].items() if it in WK.FOOD or it in m.kinds]
        if not items:
            continue
        sw = kd["switch"] if kd["switch"] is not None else (1.5 if any(x not in WK.FOOD for x in kd["diet"]) else 1.0)
        worth = lambda it: value(WK.FOOD[it]["q"], kd["mass"]) if it in WK.FOOD else 0.95
        w = np.stack([p * worth(it) ** 2 * np.power(np.maximum(avail.get(it if it in WK.FOOD else "kind:" + it, np.zeros(n)), 0) + 1e-6, sw)
                      for it, p in items])
        sh = w / w.sum(0)
        for (it, p), s_ in zip(items, sh):
            key = it if it in WK.FOOD else "kind:" + it
            want.setdefault(key, []).append((k, hungry * s_))
    got = {k: np.zeros(n) for k in need}
    eff = {"eaten": {}, "killed": {}, "dead": {}}
    for key, lst in want.items():
        tot = sum(x for _, x in lst)
        cap_ = np.maximum(avail.get(key, 0.0), 0) * (m.cap_stock if key in stock else m.cap_other)   # a season's 0.6 or 0.8, a day at a time
        if si == 3 and key.split("~")[0] in ("grass", "sward", "heather", "seeds", "roots", "inverts", "browse"):
            cap_ = cap_ * (1 - (0.8 if key.split("~")[0] != "browse" else 0.4) * snow)
        f_ = np.where(tot > cap_, cap_ / np.maximum(tot, 1e-12), 1.0)
        for k, x in lst:
            g = x * f_
            item = key[5:] if key.startswith("kind:") else key
            q = WK.FOOD[item]["q"] if item in WK.FOOD else 0.95
            got[k] += g * value(q, m.kinds[k]["mass"]) / 0.6
            if key.startswith("kind:"):
                prey = key[5:]
                head = g / m.kinds[prey]["mass"] * 1.2
                N[prey] = np.maximum(N[prey] - head, 0)
                eff["killed"][prey] = eff["killed"].get(prey, 0) + head * m.km2
                carrion = carrion + 0.2 * g
            elif key in stock:
                stock[key] = np.maximum(stock[key] - g, 0)
            elif key in pulse:
                pulse[key] = np.maximum(pulse[key] - g, 0)
                if key in ("crops", "stores", "livestock"):
                    eff["eaten"][key] = eff["eaten"].get(key, 0) + g * m.km2
            elif key == "carrion":
                carrion = np.maximum(carrion - g, 0)
    carrion = carrion * 0.5 ** (1.0 / S)
    # 3-4. condition, death, birth, people's take
    dis = knobs.get("disease", 0.15)
    from cybertron2.wild import diseases as DS
    extra = DS.step(m, st, day, N, draws)                                 # named diseases spreading by host and area (wave 4)
    named = DS.hosts_of()
    for k in m.names:
        kd = m.kinds[k]
        if not present[k]:
            continue
        R = reserve_seasons(kd["mass"], kd["hibernate"]) * S
        s_ = np.where(need[k] > 1e-12, got[k] / np.maximum(need[k], 1e-12), 1.0) if k in need else np.zeros(n)
        E[k] = E[k] + (s_ - 1.0) / R
        short = np.clip(-E[k], 0, None) * R / S
        E[k] = np.clip(E[k], 0, 1)
        crowd = N[k] / np.maximum(m.crowd_at[k] * m.suit[k], 1e-9)
        surv = np.exp(-kd["m"] / 4 / S - kd["starve"] * short - dis * crowd ** 2 / S)
        if k in extra:
            surv = surv * np.exp(-extra[k])
        if si == 1 and sd == 0 and kd["migrant"] is None and "epi" in draws and k not in named:   # a background outbreak (02zp §11)
            p_out = np.clip(knobs.get("epi_p0", 0.12) * crowd ** 2, 0, 0.5)
            u = np.asarray(draws["epi"].get(k, np.ones(n)), float)
            surv = np.where(u < p_out, surv * (1 - knobs.get("epi_kill", 0.4)), surv)
        if kd["terr"]:
            tc = N[k] / np.maximum(kd["terr"] * m.suit[k], 1e-9)
            surv = surv * np.exp(-0.5 / S * np.clip(tc - 1, 0, None))
        dead = N[k] * (1 - surv)
        carrion = carrion + dead * kd["mass"] * 0.6
        eff["dead"][k] = dead * m.km2
        N[k] = N[k] - dead
        if sd == 0 and SEASONS_OF[si] in kd["breed"] and kd["migrant"] is None:
            cond = np.clip(0.2 + 0.8 * E[k], 0, 1) / (1.0 + (dis / 0.15) * crowd ** 2)
            N[k] = N[k] * (1 + kd["b"] / len(kd["breed"]) * cond)
        if take is None:
            if kd["people"] > 0:
                t = N[k] * kd["people"] / 4 / S * m.f["farm"]
                N[k] = N[k] - t
        elif k in take:
            N[k] = N[k] * (1 - np.clip(np.asarray(take[k], float), 0, 1))
    # 5. movement along the links, migrants excepted; a thin immigration from beyond
    if len(m.la):
        for k in m.names:
            kd = m.kinds[k]
            if kd["migrant"] is not None or kd["move"] <= 0:
                continue
            att = m.suit[k] * (0.3 + E[k]) + 1e-9
            C = N[k] * m.km2
            mv = min(0.6, kd["move"] * knobs.get("move_scale", 1.0)) / S * C
            wa = att[m.lb] * m.le; wb = att[m.la] * m.le               # a to b drawn by b's attraction, b to a by a's
            tot = np.zeros(n); np.add.at(tot, m.la, wa); np.add.at(tot, m.lb, wb)
            out_ = np.zeros(n); inn = np.zeros(n)
            fa = mv[m.la] * wa / np.maximum(tot[m.la], 1e-12); fb = mv[m.lb] * wb / np.maximum(tot[m.lb], 1e-12)
            np.add.at(out_, m.la, fa); np.add.at(inn, m.lb, fa)
            np.add.at(out_, m.lb, fb); np.add.at(inn, m.la, fb)
            C = C - out_ + inn
            N[k] = np.maximum(C / m.km2, 0)
    for k in m.names:
        kd = m.kinds[k]
        if kd["migrant"] is None:
            N[k] = N[k] + 0.002 / S * m.suit[k] * (kd["ref"] or 1.0) * (~m.home)
    st["pop"] = {k: [round(float(x), 6) for x in v] for k, v in N.items()}
    st["cond"] = {k: [round(float(x), 4) for x in v] for k, v in E.items()}
    st["stock"] = {k: [round(float(x), 2) for x in v] for k, v in stock.items()}
    st["pulse"] = {k: [round(float(x), 2) for x in v] for k, v in pulse.items()}
    st["carrion"] = [round(float(x), 2) for x in carrion]
    st["day"] = day
    st["mast_now"] = mast
    return eff


SEASONS_OF = WK.SEASONS
