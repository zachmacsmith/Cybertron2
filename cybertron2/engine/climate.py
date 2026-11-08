"""The weather scheduler (D4-109; proposals/weather_scheduler.md, phase3_variance_and_risk.md §10): weather that varies in space and
time, drawn from the seed only, so every arm of an experiment meets the same weather (D4-4).

Layers, each setting the odds of the next:
- **era**: a regime of the climate over years (CLIMATE eras: steady, warm, cold, wet, dry, stormy), a starting condition (D2-73) that
  may move by its chain across a long run; rare shocks (the dark year) on top;
- **year**: the year's anomaly of temperature and wetness, from its era, carrying partly into the next year;
- **type**: the day's weather type for the region (after Lamb's types: settled, westerly, cyclonic, northerly, easterly, storm), a
  chain that holds for days, weighted by the season and the era;
- **local**: at each node, the season's climate there (height: colder, wetter) plus the year's and the type's shifts plus fields of
  temperature, rain and wind that are alike between near nodes (by the road distance between them) and carry from day to day.

Out come physical values a node and day ({temp, low, rain, wind, type}) and, from them, the label the rest of the engine knows
(clear, rain, heavy rain, fog, snow, gale) and whether the night freezes. Everything is a pure function of the seed, the spec and the
day: computed in order from day 0 and kept in a cache on the World (not its state), so a replay draws the same.

A world turns it on with a `climate:` block (`{era: steady}`; `era: draw` draws one; `moves: true` lets the era move by its chain in
a long run, else it holds as a starting condition, D2-73; `era_pace: 4` makes eras last a quarter as long; `shocks: true`; any
CLIMATE value overridden, e.g. `types: {settled: {hold: 0.85}}` for longer spells, `eras: {dry: {years: 2}}`).
Without one the engine keeps its hand-written spells (environment.py), exactly as before.
"""
from __future__ import annotations

import math

import numpy as np

from cybertron2.engine.data import CLIMATE

SEASONS = ("spring", "summer", "autumn", "winter")


def on(w) -> bool:
    return bool((getattr(w, "spec", None) or {}).get("climate"))


def params(w) -> dict:
    from cybertron2.engine.world import merge
    over = dict((w.spec.get("climate") or {}))
    for k in ("era", "shocks", "reference", "moves", "era_pace"):
        over.pop(k, None)
    return merge(CLIMATE, over)


# ---------------------------------------------------------------------- the land: where nodes are, how high
def _nodes(w) -> list:
    return sorted(w.s["nodes"])


def _heights(w, P) -> dict:
    """A node's height in metres: the spec's `elevation` if it gives one, else its parcels' mean height rank."""
    out = {}
    hm = P["height_m"]
    for nid in _nodes(w):
        spec_n = ((w.spec.get("nodes") or {}).get(nid) or {})
        if spec_n.get("elevation") is not None:
            out[nid] = float(spec_n["elevation"])
            continue
        hs = [int(p.get("height", 0) or 0) for p in w.s["parcels"].values() if p["node"] == nid]
        r = sum(hs) / len(hs) if hs else 0.0
        lo = int(math.floor(r))
        hi = min(lo + 1, len(hm) - 1)
        out[nid] = float(hm[min(lo, len(hm) - 1)] + (hm[hi] - hm[min(lo, len(hm) - 1)]) * (r - lo))
    return out


def _distances(w, P) -> np.ndarray:
    """Distance between nodes in km: the spec's node `xy` (km) if every node has one, else days along the roads x km_a_day."""
    ns = _nodes(w)
    spec_n = w.spec.get("nodes") or {}
    if ns and all((spec_n.get(n) or {}).get("xy") for n in ns):
        xy = np.array([spec_n[n]["xy"] for n in ns], dtype=float)
        return np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    idx = {n: i for i, n in enumerate(ns)}
    d = np.full((len(ns), len(ns)), np.inf)
    np.fill_diagonal(d, 0.0)
    for r in w.s["roads"].values():
        a, b = idx.get(r["a"]), idx.get(r["b"])
        if a is not None and b is not None:
            d[a, b] = d[b, a] = min(d[a, b], float(r.get("days", 1)))
    for k in range(len(ns)):                                                # shortest paths (Floyd)
        d = np.minimum(d, d[:, k:k + 1] + d[k:k + 1, :])
    d[np.isinf(d)] = 10.0                                                   # unconnected: far apart
    return d * float(P["km_a_day"])


# ---------------------------------------------------------------------- the draws
class _State:
    """The scheduler's draws for one world, computed day by day from day 0 and cached (never in the world's state)."""

    def __init__(self, w):
        self.w = w
        P = self.P = params(w)
        self.nodes = _nodes(w)
        self.height = _heights(w, P)
        dist = _distances(w, P)
        cov = np.exp(-dist / float(P["corr_km"]))
        self.chol = np.linalg.cholesky(cov + 1e-9 * np.eye(len(self.nodes)))
        self.days = []                                                      # [{type, nodes: {nid: values}}]
        self.fields = {k: np.zeros(len(self.nodes)) for k in ("temp", "rain", "wind", "amount", "fog")}
        self.type = None
        self.years = {}

    def rng(self, *key):
        """A keyed stream from the seed alone (stable in every process; no replicate's salt: the weather is exogenous, D4-4)."""
        import random
        return np.random.default_rng(random.Random("|".join([str(self.w.seed), "climate"] + [str(k) for k in key])).getrandbits(63))

    # -- years and eras
    def year(self, i) -> dict:
        if i in self.years:
            return self.years[i]
        P = self.P
        spec = self.w.spec.get("climate") or {}
        if i == 0:
            era = spec.get("era", "steady")
            if era == "draw":
                eras = sorted(P["eras"])
                era = eras[int(self.rng("era", 0).integers(len(eras)))]
            prev = {"temp": 0.0, "wet": 0.0, "era": era, "shock": None, "shock_left": 0}
        else:
            prev = self.year(i - 1)
            era = prev["era"]
            row = P["eras"][era]
            dwell = float(row["years"]) / max(1e-6, float(spec.get("era_pace", 1.0)))     # era_pace 2: eras last half as long
            if spec.get("moves") and self.rng("era", i).random() < 1.0 / max(1.0, dwell):   # the era moves on (long runs)
                nxt = row.get("next") or {"steady": 1.0}
                u, acc = self.rng("era-next", i).random() * sum(nxt.values()), 0.0
                for k, p in sorted(nxt.items()):
                    acc += p
                    if u < acc:
                        era = k
                        break
        row = P["eras"][era]
        g = self.rng("year", i).standard_normal(2)
        rho = float(P["year_persist"])
        sd = P["year_sd"]
        temp = rho * prev["temp"] + math.sqrt(1 - rho ** 2) * g[0] * float(sd["temp"]) * float(row["spread"])
        wet = rho * prev["wet"] + math.sqrt(1 - rho ** 2) * g[1] * float(sd["wet"]) * float(row["spread"])
        shock, left = prev.get("shock"), max(0, int(prev.get("shock_left", 0)) - 1)
        if not left:
            shock = None
        if not shock and spec.get("shocks"):
            for name, sh in sorted(P["shocks"].items()):
                if self.rng("shock", name, i).random() < float(sh["p"]):
                    lo, hi = sh["years"]
                    shock, left = name, int(self.rng("shock-len", name, i).integers(lo, hi + 1))
                    break
        y = {"era": era, "temp": temp, "wet": wet, "shock": shock, "shock_left": left,
             "temp_total": float(row["temp"]) + temp + (float(P["shocks"][shock]["temp"]) if shock else 0.0),
             "wet_total": float(row["wet"]) + wet + (float(P["shocks"][shock]["wet"]) if shock else 0.0)}
        self.years[i] = y
        return y

    # -- days
    def day(self, d) -> dict:
        while len(self.days) <= d:
            self.days.append(self._next(len(self.days)))
        return self.days[d]

    def _next(self, d) -> dict:
        w, P = self.w, self.P
        cal = w.calendar(d)
        season = cal["season"]
        yi = int(cal["year_day"]) // max(1, w.year_days())
        y = self.year(yi)
        era = P["eras"][y["era"]]
        types = P["types"]
        # the day's type: it holds, or a new one by base x the era's weighting
        u = self.rng("type", d).random()
        if self.type is not None and u < float(types[self.type]["hold"]):
            t = self.type
        else:
            wts = {k: float(v["base"]) * float(era["types"].get(k, 1.0)) for k, v in types.items()}
            tot = sum(wts.values())
            v, acc, t = self.rng("type-new", d).random() * tot, 0.0, None
            for k in sorted(wts):
                acc += wts[k]
                if v < acc:
                    t = k
                    break
            t = t or sorted(wts)[0]
        self.type = t
        T = types[t]
        n = len(self.nodes)
        for k in self.fields:                                               # the local fields: alike when near, carried a while
            rho = float(P["persist"].get(k, 0.0))
            e = self.chol @ self.rng("field", k, d).standard_normal(n)
            self.fields[k] = rho * self.fields[k] + math.sqrt(1 - rho ** 2) * e
        out = {}
        for i, nid in enumerate(self.nodes):
            h = self.height[nid]
            temp = (float(P["temp"][season]) + y["temp_total"] + float(T["temp"].get(season, 0.0)) - float(P["lapse"]) * h
                    + float(P["temp_sd"]) * self.fields["temp"][i])
            half = max(0.2, 1.0 + 0.5 * y["wet_total"])                          # wetness: half in how often, half in how much
            p_wet = min(0.97, float(P["wet_p"][season]) * float(T["rain"]) * half * (1.0 + float(P["orographic"]) * h))
            uz = 0.5 * (1.0 + math.erf(self.fields["rain"][i] / math.sqrt(2.0)))   # the rain field as a share: wet where it is low
            rain = 0.0
            if uz < p_wet:
                ua = 0.5 * (1.0 + math.erf(self.fields["amount"][i] / math.sqrt(2.0)))
                rain = round(-float(P["rain_mm"]) * float(T["rain"]) ** 0.5 * half * math.log(max(1e-6, 1.0 - ua)), 2)
            wind = round(max(0.0, float(P["wind"]) * float(T["wind"]) * (1.0 + h / 600.0) * (1.0 + float(P["gust"]) * self.fields["wind"][i])), 2)
            clear = bool(T.get("clear")) and rain <= 0
            low = round(temp - float(P["diurnal"]["clear" if clear else "cloud"]), 2)
            uf = 0.5 * (1.0 + math.erf(self.fields["fog"][i] / math.sqrt(2.0)))
            fog = rain <= 0 and wind < 0.7 * float(P["wind"]) and uf < float(P["fog_p"][season]) * (1.5 if h < 50 else 0.7)
            out[nid] = {"temp": round(float(temp), 2), "low": round(float(low), 2), "rain": round(float(rain), 2),
                        "wind": round(float(wind), 2), "fog": bool(fog)}
        return {"type": t, "season": season, "year": yi, "era": y["era"], "shock": y["shock"], "nodes": out}


def state(w) -> _State:
    st = getattr(w, "_climate", None)
    if st is None or st.w is not w:
        st = w._climate = _State(w)
    return st


def reference(w) -> str:
    """The node read when a caller names none: the spec's `climate.reference`, else the node with most people, else the first."""
    ref = (w.spec.get("climate") or {}).get("reference")
    if ref in w.s["nodes"]:
        return ref
    count = {}
    for n, a in (w.s.get("people") or {}).items():
        if a.get("alive", True) and a.get("at") in w.s["nodes"]:
            count[a["at"]] = count.get(a["at"], 0) + 1
    homes = [nid for nid in sorted(w.s["nodes"]) if not w.s["nodes"][nid].get("unexplored")]
    return max(homes or sorted(w.s["nodes"]), key=lambda nid: (count.get(nid, 0), -sorted(w.s["nodes"]).index(nid)))


# ---------------------------------------------------------------------- what the engine reads
def env(w, node=None, day=None) -> dict:
    """The physical weather at a node on a day: {temp, low, rain, wind, fog, type, season, era}."""
    day = w.d if day is None else day
    node = node if node in w.s["nodes"] else reference(w)
    dd = state(w).day(max(0, int(day)))
    return {**dd["nodes"][node], "type": dd["type"], "season": dd["season"], "era": dd["era"], "shock": dd["shock"]}


def label(w, node=None, day=None) -> str:
    """The day's weather as the engine names it (environment.WEATHER): snow, gale, heavy rain, rain, fog, clear."""
    P = state(w).P
    e = env(w, node, day)
    if e["rain"] > 0 and (e["temp"] <= float(P["snow_below"]) or (e["low"] < -1.0 and e["temp"] <= float(P["snow_below"]) + 1.5)):
        return "snow"
    if e["wind"] >= float(P["gale"]):
        return "gale"
    if e["rain"] >= float(P["heavy_mm"]):
        return "heavy rain"
    if e["rain"] > 0:
        return "rain"
    if e["fog"]:
        return "fog"
    return "clear"


def frost(w, node=None, day=None) -> bool:
    """Whether the night freezes at a node: the night's low below zero."""
    return env(w, node, day)["low"] < 0.0


SPELL_OF = {"settled": "dry", "easterly": "dry", "westerly": "wet", "cyclonic": "wet", "northerly": "cold snap", "storm": "storm"}


def spell(w, day=None) -> str:
    """The day's spell in the old words (environment.spell's callers): from the region's type; a dry type in winter's cold is a cold
    snap, a settled day out of summer with no run of dry days is normal."""
    e = env(w, None, day)
    s = SPELL_OF.get(e["type"], "normal")
    if s == "dry" and e["season"] == "winter" and e["low"] < 0:
        return "cold snap"
    if s == "wet" and e["rain"] <= 0:
        return "normal"
    return s


def summary(w, days) -> dict:
    """A run's weather, for analysis: labels and values per node per day, and counts."""
    out = {"days": [], "counts": {}}
    for d in range(days):
        row = {"day": d, "type": env(w, None, d)["type"], "nodes": {}}
        for nid in _nodes(w):
            lab = label(w, nid, d)
            row["nodes"][nid] = {**{k: v for k, v in env(w, nid, d).items() if k in ("temp", "low", "rain", "wind")}, "label": lab,
                                 "frost": frost(w, nid, d)}
            out["counts"][lab] = out["counts"].get(lab, 0) + 1
        out["days"].append(row)
    return out
