"""Tests of the layered wild systems prototype (02zp part five)."""
import sys, pickle, json, itertools, collections, numpy as np
sys.path.insert(0, ".")
import wild as Wd
from wild import Y, S, LEVELS, FOOD_NEED, WORK, season, sday

IN = pickle.load(open("inputs.pkl", "rb"))
ERAS = ["steady", "cold", "wet", "warm", "dry"]
UNIT_FOOD = 0.5          # a unit of work against food, for one combined figure (an assumption)


def runs():
    """Every (world, era, village) with its drivers and the world's pulses."""
    for wi, (wname, W) in enumerate(IN.items()):
        normals = {k: Wd.Drivers(W["weather"]["steady"][k]).normals for k in W["villages"]}
        for ei, era in enumerate(ERAS):
            drv = {k: Wd.Drivers(W["weather"][era][k], normals[k]) for k in W["villages"]}
            k0 = sorted(W["villages"])[0]
            rng = np.random.default_rng(1000 * wi + ei)
            mast, full = Wd.mast_series(drv[k0].years, rng, drv[k0].flower_frost)
            voles = Wd.vole_phases(drv[k0].years, rng, mast, [drv[k0].hard_winter(y) for y in range(drv[k0].years)])
            for vi, (k, info) in enumerate(sorted(W["villages"].items())):
                yield {"world": wname, "era": era, "village": k, "name": info["name"], "info": info, "drv": drv[k],
                       "mast": mast, "full": full, "voles": voles, "seed": 100000 * wi + 1000 * ei + vi}


def simulate(r, policy=None, level=None, model=None, seed_add=0):
    rng = np.random.default_rng(r["seed"] + seed_add)
    v = Wd.Village(r["info"], r["drv"], r["mast"], r["voles"], rng, r["full"])
    obs = Observer(level, np.random.default_rng(r["seed"] + 7)) if level else None
    for d in range(r["drv"].n):
        acts = policy(v, d, obs, model) if policy else {}
        v.day(d, acts)
        if obs is not None:
            obs.see(v, d)
    return v, obs


# ------------------------------------------------------------------ observers and readers
class Observer:
    """What a reader of one level notices and reads, day by day (common random numbers across levels by seed)."""

    def __init__(self, level, rng):
        self.level, self.rng, self.seen = level, rng, {}

    def see(self, v, d):
        out = []
        for sg in v.signs.get(d, []):
            u = self.rng.random()
            if u < sg["notice"].get(self.level, 0.0):
                rd = sg["read"].get(self.level)
                if rd is not None:
                    out.append((sg["kind"], sg["name"], rd))
        self.seen[d] = out

    def got(self, d, kind, key=None, val=None):
        for k, n, rd in self.seen.get(d, []):
            if k == kind and (key is None or (key in rd and (val is None or rd[key] == val))):
                return rd
        return None

    def named(self, d, name):
        return any(n == name for k, n, rd in self.seen.get(d, []))

    def season_reading(self, d, kind, key):
        """The latest reading of `key` for `kind` this year, up to day d."""
        y0 = (d // Y) * Y
        for t in range(d, y0 - 1, -1):
            rd = self.got(t, kind, key)
            if rd is not None:
                return rd[key]
        return None


def ctx(d):
    s, sd = season(d), sday(d)
    return (s, sd // 2)


def features(ev, obs, d, v):
    """The tuple a reader of obs.level uses to predict event `ev` on night d, from what it saw up to day d-1 (D2-197)."""
    L = obs.level
    p = d - 1
    if ev == "boar_raid":
        if L == "novice":
            return (ctx(d), obs.got(p, "boar", "rooting") is not None, obs.got(p, "boar", "trampled") is not None)
        fresh = obs.got(p, "boar", "rooting", "fresh") is not None
        if L == "systematic":
            return (ctx(d), fresh, obs.got(p, "boar", "trampled") is not None, obs.season_reading(p, "mast", "fallen"))
        return (ctx(d), fresh, obs.got(p - 1, "boar", "rooting", "fresh") is not None, obs.got(p, "boar", "trampled") is not None,
                obs.season_reading(p, "mast", "fallen") or obs.season_reading(p, "mast", "set") or obs.season_reading(p, "mast", "catkins"),
                v.drv.frozen[p])
    if ev == "fox_visit":
        base = (ctx(d), obs.got(p, "fox", "fox_kill") is not None)
        if L == "novice":
            return base
        if L == "systematic":
            return base + (obs.got(p, "fox", "alarm") is not None,)
        return base + (obs.got(p, "fox", "alarm", "fox") is not None, obs.season_reading(p, "voles", "owls") == "silent")
    if ev == "freeze_start":
        if L == "novice":
            return (season(d), obs.got(p, "fowl", "birds") is not None)
        return (season(d), obs.got(p, "fowl", "plovers") is not None) + ((v.drv.temp[p] < 4,) if L == "expert" else ())
    if ev == "eel_night":
        if L == "novice":
            return (ctx(d), obs.got(p, "eels", "rain") is not None)
        if L == "systematic":
            return (ctx(d), obs.got(p, "eels", "rain_after_dry") is not None, obs.got(p, "eels", "rain") is not None)
        return (ctx(d), obs.got(p, "eels", "rain_after_dry") is not None, obs.got(p, "eels", "rain") is not None, bool(v.drv.dark[d]))
    if ev == "slug_night":
        if L == "novice":
            return (ctx(d), obs.got(p, "slugs", "slime") is not None)
        wet = v.drv.rain[p] >= 2
        if L == "systematic":
            return (ctx(d), obs.got(p, "slugs", "slime") is not None, wet)
        return (ctx(d), wet, v.drv.dry[p - 1] >= 3 if p >= 1 else False, v.L > 1.3)
    if ev == "wasp_year":
        if L == "novice":
            return (obs.season_reading(p, "wasps", "wasps") is not None,)
        return (obs.season_reading(p, "wasps", "queens"),)
    if ev == "vole_peak":
        y0 = (p // Y) * Y
        cnt = lambda name: min(3, sum(obs.named(t, name) for t in range(y0, p + 1)))
        if L == "novice":
            return (cnt("kestrels hovering"),)
        if L == "systematic":
            return (cnt("kestrels hovering"), cnt("runways in the long grass"))
        return (cnt("kestrels hovering"), cnt("runways in the long grass"), cnt("pellets thick with little skulls under the barn beam") > 0)
    if ev == "mast_heavy":
        if L == "novice":
            return ()
        if L == "systematic":
            return (obs.season_reading(p, "mast", "set"),)
        return (obs.season_reading(p, "mast", "set"), obs.season_reading(p, "mast", "catkins"), bool(v.drv.flower_frost[p // Y]))
    raise KeyError(ev)


def base_features(ev, d):
    if ev in ("freeze_start",):
        return (season(d),)
    if ev in ("wasp_year", "vole_peak", "mast_heavy"):
        return ()
    return (ctx(d),)


EVENTS = {   # event: (days it is scored on, a function of the village giving the truth)
    "boar_raid": (lambda v, d: v.sounder is not None or "boar_raid" in v.events.get(d, {}), lambda v, d: v.events.get(d, {}).get("boar_raid", 0)),
    "fox_visit": (lambda v, d: True, lambda v, d: v.events.get(d, {}).get("fox_visit", 0)),
    "freeze_start": (lambda v, d: season(d) in (2, 3, 0) and not v.drv.frozen[d - 1], lambda v, d: v.events.get(d, {}).get("freeze_start", 0)),
    "eel_night": (lambda v, d: v.river is not None and (season(d) == 2 or (season(d) == 3 and sday(d) <= 1)), lambda v, d: v.events.get(d, {}).get("eel_night", 0)),
    "slug_night": (lambda v, d: "slug_night" in v.events.get(d, {}), lambda v, d: v.events.get(d, {}).get("slug_night", 0)),
    "wasp_year": (lambda v, d: d % Y == S + 5, lambda v, d: v.events.get(d, {}).get("wasp_year", 0)),
    "vole_peak": (lambda v, d: d % Y == 2 * S + 6, lambda v, d: int(v.voles[d // Y] == "peak")),
    "mast_heavy": (lambda v, d: d % Y == S + 1 and v.wood_km2 > 0.05, lambda v, d: int(v.mast[d // Y] >= 3)),
}


def collect(split):
    """Rows (event, level, features, truth) from passive runs; split: 'train' or 'test' by village parity."""
    rows = collections.defaultdict(list)
    for r in runs():
        par = (hash((r["world"], r["village"])) % 2 == 0) if False else (int(r["village"][1:]) % 2 == 0)
        if (split == "train") != par:
            continue
        vs = {}
        for L in LEVELS:
            v, obs = simulate(r, level=L)
            vs[L] = (v, obs)
        v0 = vs["novice"][0]
        for ev, (when, truth) in EVENTS.items():
            for d in range(2, v0.drv.n):
                if not when(v0, d):
                    continue
                t = truth(v0, d)
                rows[(ev, "base")].append((base_features(ev, d), t))
                for L in LEVELS:
                    rows[(ev, L)].append((features(ev, vs[L][1], d, vs[L][0]), t))
    return rows


def fit(rows):
    cnt = collections.defaultdict(lambda: [0, 0])
    for f, t in rows:
        c = cnt[f]; c[0] += 1; c[1] += int(t > 0)
    prior = sum(int(t > 0) for _, t in rows) / max(1, len(rows))
    return {f: (c[1] + 2 * prior) / (c[0] + 2) for f, c in cnt.items()}, prior


def auc(p, t):
    p, t = np.asarray(p), np.asarray(t) > 0
    if t.all() or (~t).all():
        return float("nan")
    order = np.argsort(p); ranks = np.empty(len(p)); ranks[order] = np.arange(1, len(p) + 1)
    # average ranks for ties
    for val in np.unique(p):
        m = p == val; ranks[m] = ranks[m].mean()
    n1 = t.sum(); n0 = len(t) - n1
    return float((ranks[t].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def inference():
    tr, te = collect("train"), collect("test")
    out = {}
    for ev in EVENTS:
        res = {}
        mb, prior = fit(tr[(ev, "base")])
        tb = [t for _, t in te[(ev, "base")]]
        pb = [mb.get(f, prior) for f, _ in te[(ev, "base")]]
        brier_b = float(np.mean([(p - (t > 0)) ** 2 for p, t in zip(pb, tb)]))
        res["base"] = {"brier": brier_b, "auc": auc(pb, tb), "n": len(tb), "rate": float(np.mean([t > 0 for t in tb]))}
        for L in LEVELS:
            m, pr = fit(tr[(ev, L)])
            pl = [m.get(f, pr) for f, _ in te[(ev, L)]]
            tl = [t for _, t in te[(ev, L)]]
            b = float(np.mean([(p - (t > 0)) ** 2 for p, t in zip(pl, tl)]))
            res[L] = {"brier": b, "skill": 1 - b / brier_b if brier_b > 0 else 0.0, "auc": auc(pl, tl)}
        out[ev] = res
    return out, tr


if __name__ == "__main__":
    import time
    t = time.time()
    out, _ = inference()
    for ev, r in out.items():
        print(f"{ev:13s} n {r['base']['n']:6d} rate {r['base']['rate']:.3f} | base auc {r['base']['auc']:.2f} | " +
              " | ".join(f"{L[:3]} skill {r[L]['skill']:+.2f} auc {r[L]['auc']:.2f}" for L in LEVELS))
    print("seconds", round(time.time() - t))
    json.dump(out, open("inference.json", "w"), indent=1)
