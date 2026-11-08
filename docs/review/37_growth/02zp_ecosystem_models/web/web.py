"""W: a general food web on 1 km patches of generated land, by season.

Everything a kind is, is a row (KINDS): body mass, breeding, survival, a habitat vector over the patch's features, a diet over food
resources and over other kinds (prey), switching, movement, a season of presence (migrants), what people take and what it damages.
Plant food comes from M1's vegetation (the kinds in each layer), by season, with yearly draws (mast, fruit). One rule for all:
each season every consumer asks for its intake (Kleiber: k x mass^0.75), split over its diet by preference x availability
(switching), capped by what the food can give (access x amount); satisfaction drives starvation and next spring's births;
a share moves toward better patches; migrants arrive from beyond the map. Engineers change the land (beaver: wetness).
"""
from __future__ import annotations

import numpy as np

import niche as NI

SEASONS = ("spring", "summer", "autumn", "winter")

# ---- food resources: production a km2 of full cover a year (kg, edible dry matter), access (share wild consumers can take),
# season profile (shares of the year's production by season), and what supplies it (computed in features())
RES = {
    "grass":   {"prod": 300000, "access": 0.10, "season": (0.30, 0.40, 0.22, 0.08)},     # coarse grass and herbs: deer, elk, voles
    "sward":   {"prod": 300000, "access": 0.06, "season": (0.30, 0.35, 0.25, 0.10)},     # short turf: hares, rabbits, geese
    "browse":  {"prod": 60000,  "access": 0.30, "season": (0.25, 0.35, 0.25, 0.15)},
    "heather": {"prod": 120000, "access": 0.15, "season": (0.20, 0.30, 0.25, 0.25)},
    "mast":    {"prod": 60000,  "access": 0.50, "season": (0.05, 0.0, 0.55, 0.40)},
    "nuts":    {"prod": 15000,  "access": 0.50, "season": (0.0, 0.0, 0.7, 0.3)},
    "fruit":   {"prod": 25000,  "access": 0.40, "season": (0.0, 0.40, 0.55, 0.05)},
    "roots":   {"prod": 40000,  "access": 0.10, "season": (0.30, 0.20, 0.25, 0.25)},
    "inverts": {"prod": 40000,  "access": 0.10, "season": (0.30, 0.30, 0.30, 0.10)},
    "seeds":   {"prod": 30000,  "access": 0.20, "season": (0.05, 0.25, 0.50, 0.20)},
    "aquatic": {"prod": 80000,  "access": 0.20, "season": (0.20, 0.35, 0.30, 0.15)},
    "fish":    {"prod": 12000,  "access": 0.25, "season": (0.20, 0.30, 0.30, 0.20)},
    "shore":   {"prod": 30000,  "access": 0.25, "season": (0.25, 0.25, 0.25, 0.25)},
    "seafish": {"prod": 15000,  "access": 0.20, "season": (0.25, 0.30, 0.25, 0.20)},     # inshore sea within reach of the coast
    "conifer seed": {"prod": 8000, "access": 0.5, "season": (0.2, 0.1, 0.3, 0.4)},
    "crops":   {"prod": 150000, "access": 0.04, "season": (0.10, 0.40, 0.45, 0.05)},
    "livestock": {"prod": 4000, "access": 0.15, "season": (0.35, 0.20, 0.20, 0.25)},    # young and weak beasts at risk, kg a km2 farm
    "stores":  {"prod": 20000,  "access": 0.05, "season": (0.20, 0.10, 0.30, 0.40)},
    "carrion": {"prod": 0, "access": 0.6, "season": (0.25, 0.25, 0.25, 0.25)},
}
RNAMES = list(RES)
YEAR_DRAW = {"mast": (0.25, 3.0, 0.25, 0.1), "nuts": (0.3, 2.0, 0.2, 0.3), "fruit": (0.3, 1.6, 0.2, 0.4), "conifer seed": (0.3, 2.5, 0.2, 0.2)}
# (p good, x good, p bad, x bad): oak and beech mast, hazel, fruit and cone years (calibrate)


def features(d, v, block=7):
    """Patch features (share of the patch) and food resources a year (kg a km2), from the land and M1's vegetation."""
    h = d["h"]; ny, nx = h.shape[0] // block, h.shape[1] // block
    def agg(a):
        a = np.asarray(a, dtype=float).reshape(h.shape)[: ny * block, : nx * block]
        return a.reshape(ny, block, nx, block).mean((1, 3))
    ci, cs = v["canopy"]; si, ss = v["shrub"]; fi, fs = v["field"]
    T, B = v["T"], v["B"]
    def share(idx, sh, names):
        out = np.zeros(sh.shape[1])
        for n in names:
            j = NI.NAMES.index(n)
            if j in idx:
                out += sh[list(idx).index(j)]
        return out
    can = lambda names: share(ci, cs, names) * T
    shr = lambda names: share(si, ss, names) * B
    fld = lambda names: share(fi, fs, names) * (1 - 0.7 * T)
    land = (~d["sea"]).ravel().astype(float)
    water = ((d["river"].ravel() >= 1) * 0.12 + d["lake"].ravel() * 1.0 + (d["river"].ravel() >= 3) * 0.6).clip(0, 1)
    eco = d["eco"].ravel()
    wetl = fld(["reed", "sedge", "meadowsweet", "rushes", "watercress"]) + np.isin(eco, ["fen", "reedbed", "saltmarsh"]) * 0.3
    shore = ((d["c"].ravel() < 0.4) & ~d["sea"].ravel()).astype(float) + (eco == "saltmarsh") * 0.5
    sea = d["sea"].ravel().astype(float)
    rock = (d["slope"].ravel() >= 25).astype(float)
    grassy = fld(["rich grasses", "fine grasses", "chalk turf", "meadow herbs", "salt grasses", "marram"])
    heath = fld(["heather", "bilberry", "moor grass", "cotton-grass", "sphagnum"])
    sites = [(int(r), int(c)) for r, c in d["sites"]] if len(d["sites"]) else []
    yy, xx = np.mgrid[0:h.shape[0], 0:h.shape[1]]
    farm = np.zeros(h.shape)
    for r, c in sites:
        farm = np.maximum(farm, (np.hypot(yy - r, xx - c) * float(d["km"]) <= 2.5).astype(float))
    farm = farm.ravel() * (1 - T) * land
    f = {
        "wood": agg(T * land), "shrub": agg(B * land), "open": agg((1 - T) * land), "grassy": agg(grassy * land), "heath": agg(heath * land),
        "wet": agg(wetl * land), "water": agg(water), "shore": agg(shore * land), "sea": agg(sea), "rock": agg(rock * land),
        "conifer": agg(can(["pine"]) * land), "oakbeech": agg(can(["oak", "sessile oak", "beech"]) * land),
        "old": agg(T * (d["band"].ravel() >= 3)), "farm": agg(farm), "land": agg(land),
        "h": agg(h.ravel()), "temp": agg(d["temp"].ravel()), "river": agg((d["river"].ravel() >= 2).astype(float)),
        "bigriver": agg((d["river"].ravel() >= 3).astype(float)), "N": agg(np.asarray(v.get("N", np.full(T.size, 5.0)))),
    }
    nq = np.clip(f["N"] / 6.0, 0.3, 1.3)
    r = {
        "grass": agg(grassy * land) * nq, "sward": agg((fld(["rich grasses", "fine grasses", "chalk turf", "salt grasses"]) + 0.3 * farm) * land),
        "browse": agg((B + 0.25 * T * (1 - T) * 4 + 0.05 * T) * land),
        "heather": f["heath"], "mast": f["oakbeech"], "nuts": agg((shr(["hazel"]) + 0.3 * can(["oak", "ash"])) * land),
        "fruit": agg((shr(["bramble", "hawthorn", "blackthorn", "crab apple", "dog rose", "elder"]) + 0.1 * T + fld(["bilberry"])) * land),
        "roots": agg((fld(["bracken", "bluebell", "rich grasses", "meadow herbs", "wild garlic"]) + 0.3 * T) * land),
        "inverts": agg(((1 - T) * 0.8 + T * 0.6) * land) * nq, "seeds": agg((grassy + 0.3 * farm) * land),
        "aquatic": f["wet"] + f["water"] * 0.5, "fish": f["water"] + 0.02 * f["sea"], "shore": f["shore"] + 0.1 * f["sea"],
        "seafish": f["sea"] * _near(f["land"] > 0.02, 3),
        "conifer seed": f["conifer"], "crops": f["farm"] * 0.4, "livestock": f["farm"], "stores": np.zeros_like(f["farm"]),
        "carrion": np.zeros_like(f["farm"]),
    }
    for (rr, cc) in sites:
        f_r, f_c = min(rr // block, ny - 1), min(cc // block, nx - 1)
        r["stores"][f_r, f_c] = 1.0
    return f, r


# ---- kinds. habitat: weights over features (summed, then clipped 0-1, times hard limits); diet: {resource or kind: preference}
# b: births a female-equivalent a year at full food; m: yearly death at full food; starve: extra death a season at no food;
# move: share redistributed a season; migrant: seasons present; people: share taken a year near villages (light hunting);
# cap: territorial ceiling a km2; k: intake factor (Kleiber, kg a day = k * mass^0.75)
def K(mass, b, m, hab, diet, starve=0.35, move=0.1, k=0.08, cap=None, limits=None, migrant=None, people=0.0, switch=None,
      prey_vuln=0.5, breed=("spring",), notes="", uses="", damage=""):
    """b: young a head a year at full food (split over the breeding seasons); m: yearly death rate at full food (survival e^-m);
    switch: how sharply a consumer turns from scarce food to plentiful (1 proportional; 2 a prey refuge, the default for predators);
    prey_vuln: the share of this kind's biomass a predator can catch."""
    if switch is None:
        switch = 2.0 if any(x not in RES for x in diet) else 1.0          # predators turn away from scarce prey (a refuge)
    return dict(mass=mass, b=b, m=m, hab=hab, diet=diet, starve=starve, move=move, k=k, cap=cap, limits=limits or {},
                migrant=migrant, people=people, switch=switch, vuln=prey_vuln, breed=breed, notes=notes, uses=uses, damage=damage)


def run(feat, res, kinds, years=60, seed=0, people=True, policy=None, dens0=None, record=True, knobs=None, events=None):
    """Simulate; returns per-year mean densities (a km2 of the window's land) per kind, and records."""
    rng = np.random.default_rng(seed)
    knobs = knobs or {}
    names = list(kinds)
    shape = feat["land"].shape
    land = feat["land"]
    # habitat suitability per kind (0-1)
    suit = {}
    for n, k in kinds.items():
        s = np.zeros(shape)
        for fe, w in k["hab"].items():
            s = s + w * feat[fe]
        s = np.clip(s, 0, 1)
        for lim, (lo, hi) in k["limits"].items():
            x = feat[lim]
            s = s * np.clip((x - lo) / max(1e-9, 0.15 * abs(hi - lo) + 1e-9), 0, 1) * np.clip((hi - x) / max(1e-9, 0.15 * abs(hi - lo) + 1e-9), 0, 1)
        suit[n] = s * land
    N = {n: (dens0[n] if dens0 and n in dens0 else 0.3 * kinds[n].get("d0", 1.0) * suit[n]) for n in names}
    wet_add = np.zeros(shape)
    out = {n: [] for n in names}
    rec = {"crop_damage": [], "stock_killed": [], "store_loss": [], "people_take": {n: [] for n in names}, "year_type": []}
    hunted_near = feat["farm"] > 0.05
    mig_seen = {}
    for y in range(years):
        draws = {}
        for rname, (pg, xg, pb, xb) in YEAR_DRAW.items():
            u = rng.random()
            draws[rname] = xg if u < pg else (xb if u > 1 - pb else 1.0)
        rec["year_type"].append(draws.get("mast", 1.0))
        growth = float(np.exp(rng.normal(0, knobs.get("weather_sd", 0.18))))          # a good or poor growing year
        hard = rng.random() < knobs.get("p_hard_winter", 0.15)                          # snow lies: winter food buried
        rec.setdefault("hard", []).append(hard)
        taken = {n: 0.0 for n in names}; dmg = sto = stk = 0.0
        sat_year = {n: np.zeros(shape) for n in names}
        carrion = np.zeros(shape)
        for si, season in enumerate(SEASONS):
            # supply this season (kg a km2) by resource
            A = {}
            for rname, spec in RES.items():
                base = res[rname] * spec["prod"] * spec["season"][si] * draws.get(rname, 1.0) * knobs.get("prod_" + rname, 1.0)
                if rname in ("grass", "browse", "heather", "seeds", "fruit", "aquatic", "inverts", "crops", "roots"):
                    base = base * growth * (0.35 if (hard and season == "winter") else 1.0)
                if rname == "aquatic":
                    base = base + wet_add * spec["prod"] * spec["season"][si]
                if rname == "carrion":
                    base = carrion
                A[rname] = base * spec["access"]
            present = {n: (kinds[n]["migrant"] is None or season in kinds[n]["migrant"]) for n in names}
            # migrants arrive from beyond the map
            for n in names:
                if kinds[n]["migrant"] is not None:
                    if season == kinds[n]["migrant"][0]:
                        N[n] = kinds[n]["arrive"] * suit[n] * knobs.get("arrive_" + n, 1.0)
                    elif not present[n]:
                        N[n] = np.zeros(shape)
            for n in names:
                if kinds[n]["migrant"] is not None and present[n]:
                    mig_seen[n] = max(mig_seen.get(n, 0.0), float((N[n] * land).sum() / land.sum()))
            # prey as food: biomass at risk
            for n in names:
                A["kind:" + n] = N[n] * kinds[n]["mass"] * kinds[n]["vuln"] if present[n] else np.zeros(shape)
            # demand and allocation
            want = {}
            for n in names:
                if not present[n]:
                    continue
                kk = kinds[n]
                need = N[n] * kk["k"] * knobs.get("k_" + n, 1.0) * kk["mass"] ** 0.75 * 91.0
                items = list(kk["diet"].items())
                items = [(it, p) for it, p in items if it in RES or it in kinds]
                w = np.stack([p * np.power(np.maximum(A.get(it if it in RES else "kind:" + it, np.zeros(shape)), 0.0) + 1e-9, kk["switch"]) for it, p in items])
                share_ = w / w.sum(0)
                for (it, p), sh in zip(items, share_):
                    key = it if it in RES else "kind:" + it
                    want.setdefault(key, []).append((n, need * sh))
                kk["_need"] = need
            got = {n: np.zeros(shape) for n in names}
            for key, lst in want.items():
                tot = sum(x for _, x in lst)
                cap = np.maximum(A.get(key, 0.0), 0.0)
                f_ = np.where(tot > cap, cap / np.maximum(tot, 1e-12), 1.0)
                for n, x in lst:
                    g = x * f_
                    got[n] += g
                    if knobs.get("flux") and y >= years - 10:
                        fl = rec.setdefault("flux", {})
                        fl[(n, key)] = fl.get((n, key), 0.0) + float((g * land).sum()) / 10.0
                    if key.startswith("kind:"):
                        prey = key[5:]
                        killed = g / kinds[prey]["mass"] * 1.3            # whole animals killed; ~30% left as carrion
                        N[prey] = np.maximum(N[prey] - killed, 0.0)
                        carrion = carrion + 0.3 * g
                    elif key == "crops":
                        dmg += float((g * 3).sum())                        # trampled and spoilt besides what is eaten
                    elif key == "livestock":
                        stk += float(g.sum())
                    elif key == "stores":
                        sto += float(g.sum())
                    elif key == "carrion":
                        carrion = np.maximum(carrion - g, 0)
            # vital rates
            for n in names:
                if not present[n]:
                    continue
                kk = kinds[n]
                s = np.where(kk["_need"] > 1e-12, got[n] / np.maximum(kk["_need"], 1e-12), 1.0)
                s = np.clip(s, 0, 1)
                sat_year[n] += s / 4
                surv = np.exp(-kk["m"] / 4 - kk["starve"] * 2.0 * (1 - s))
                sc = knobs.get("selfcap", None)
                if sc and kk.get("target") and kk["migrant"] is None:
                    crowd = N[n] / np.maximum(sc * kk["target"] * suit[n], 1e-9)
                    surv = surv * np.exp(-0.25 * np.clip(crowd - 1, 0, None) ** 2)
                dead = N[n] * (1 - surv)
                carrion = carrion + dead * kk["mass"] * 0.5
                N[n] = N[n] - dead
                if season in kk["breed"] and kk["migrant"] is None:
                    N[n] = N[n] * (1 + kk["b"] / len(kk["breed"]) * np.clip(s, 0, 1) ** 2 * knobs.get("b_" + n, 1.0))
                if kk["cap"]:
                    N[n] = np.minimum(N[n], kk["cap"] * suit[n] + 1e-9)
                # people's take (light hunting near villages), spread over the year
                if people and kk["people"] > 0:
                    tk = N[n] * kk["people"] / 4 * hunted_near * (policy.get(n, 1.0) if policy else 1.0)
                    N[n] = N[n] - tk; taken[n] += float(tk.sum())
                # movement toward suitable, fed patches
                if kk["move"] > 0 and kk["migrant"] is None:
                    att = suit[n] * (0.3 + s)
                    N[n] = _disperse(N[n], att, kk["move"])
                # the edge: a trickle from beyond the map where suitable
                N[n] = N[n] + 0.002 * suit[n] * kk.get("d0", 1.0) * _edge(shape)
            # engineers: beaver dams raise wetness along rivers
            if "beaver" in N:
                wet_add = np.clip(wet_add * 0.98 + 0.02 * np.clip(N["beaver"] / 0.5, 0, 1) * feat["river"], 0, 0.5)
            # events (felling, draining, culls) by year and season
            if events:
                for ev in events:
                    if ev[0] == y and ev[1] == si:
                        ev[2](feat, res, N)
        for n in names:
            if kinds[n]["migrant"] is not None:                              # a migrant's density while it is here
                out[n].append(float(mig_seen.get(n, 0.0)))
            else:
                out[n].append(float((N[n] * land).sum() / land.sum()))
            rec["people_take"][n].append(taken[n])
        mig_seen = {}
        rec["crop_damage"].append(dmg); rec["stock_killed"].append(stk); rec["store_loss"].append(sto)
    rec["final"] = {n: N[n] for n in names}
    rec["suit"] = suit
    return out, rec


def _near(mask, r):
    """1 where a patch is within r patches of the mask."""
    m = mask.astype(float)
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out = np.maximum(out, np.roll(m, (dy, dx), (0, 1)))
    return out


def _disperse(N, att, m):
    mov = m * N
    out = N - mov
    tot = np.zeros_like(N); parts = []
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a = np.roll(att, (dy, dx), (0, 1)) + 1e-9
        parts.append((dy, dx, a)); tot += a
    for dy, dx, a in parts:
        out += np.roll(mov * a / tot, (-dy, -dx), (0, 1))
    return out


def _edge(shape):
    e = np.zeros(shape); e[0, :] = e[-1, :] = e[:, 0] = e[:, -1] = 1.0
    return e
