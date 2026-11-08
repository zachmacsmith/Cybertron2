"""W2: the food web rebuilt as consumers and resources, without per-kind fitting (02zp §W2).

What changed from W, and why (Zach, 8 Nov: "it seems unlikely there would be literally no grass left for them"):
- Plant food is a standing stock that grows and is eaten down (by season, with weather), not a fixed slice; animals rarely eat it
  all, and what limits them comes from grazing pressure against growth and the winter, not from an arbitrary share.
- Each kind eats what its body needs (Kleiber, by diet class): physiology is known, so nothing per kind is fitted. What is
  uncertain (how much each food grows, and how much of it wild animals can reach) is calibrated once per food, for all kinds.
- Food quality depends on body size (Jarman-Bell): big grazers live on coarse grass, reed and heather that small ones cannot.
- Body reserves: fat covers a lean season in proportion to body size; hibernators (bear) need nothing in winter and live on fat;
  breeding follows condition, not that season's food.
- Self-limits only where the biology has them (territories, setts, lodges), as a density a km2 of habitat, not a share of a target.
- Weather years hit foods differently (a mast year, a drought on grass, a wet year on seeds), so kinds on different foods are
  favoured in different years.
Kinds are rows (KINDS2); a world is the patch features and resources from web.features.
"""
from __future__ import annotations

import numpy as np

SEASONS = ("spring", "summer", "autumn", "winter")

# ---- foods. kind: "stock" grows logistically toward cap (kg a km2 of full cover), "pulse" is produced in its seasons and rots.
# grow: share of cap produced a season at full growth (by season); q: quality (0-1); rot: share of a pulse lost a season.
FOOD = {
    "grass":   {"type": "stock", "cap": 60000, "grow": (0.45, 0.55, 0.30, 0.05), "q": 0.55},    # coarse grass and herbs
    "sward":   {"type": "stock", "cap": 25000, "grow": (0.45, 0.50, 0.35, 0.08), "q": 0.75},    # short turf
    "browse":  {"type": "stock", "cap": 30000, "grow": (0.40, 0.45, 0.15, 0.02), "q": 0.60},
    "heather": {"type": "stock", "cap": 80000, "grow": (0.20, 0.25, 0.15, 0.03), "q": 0.35},
    "aquatic": {"type": "stock", "cap": 60000, "grow": (0.40, 0.50, 0.25, 0.05), "q": 0.45},    # reed, sedge, pondweed
    "roots":   {"type": "stock", "cap": 20000, "grow": (0.20, 0.20, 0.20, 0.05), "q": 0.60},
    "inverts": {"type": "stock", "cap": 8000,  "grow": (0.60, 0.70, 0.60, 0.10), "q": 0.85},
    "fish":    {"type": "stock", "cap": 40000, "grow": (0.20, 0.30, 0.25, 0.10), "q": 0.95},
    "seafish": {"type": "stock", "cap": 30000, "grow": (0.25, 0.30, 0.25, 0.15), "q": 0.95},
    "mast":    {"type": "pulse", "prod": 50000, "season": (0, 0, 0.8, 0.2), "rot": 0.4, "q": 0.85},
    "nuts":    {"type": "pulse", "prod": 12000, "season": (0, 0, 0.8, 0.2), "rot": 0.3, "q": 0.90},
    "fruit":   {"type": "pulse", "prod": 20000, "season": (0, 0.4, 0.6, 0), "rot": 0.6, "q": 0.70},
    "seeds":   {"type": "pulse", "prod": 30000, "season": (0.05, 0.3, 0.5, 0.15), "rot": 0.3, "q": 0.85},
    "conifer seed": {"type": "pulse", "prod": 8000, "season": (0.2, 0.1, 0.3, 0.4), "rot": 0.2, "q": 0.85},
    "crops":   {"type": "pulse", "prod": 120000, "season": (0.1, 0.4, 0.45, 0.05), "rot": 0.5, "q": 0.80},
    "livestock": {"type": "pulse", "prod": 3000, "season": (0.35, 0.2, 0.2, 0.25), "rot": 0.9, "q": 1.0},
    "stores":  {"type": "pulse", "prod": 15000, "season": (0.2, 0.1, 0.3, 0.4), "rot": 0.5, "q": 0.85},
    "carrion": {"type": "carrion", "q": 0.9},
}
# Jarman-Bell (02zp §W2): bulk plant stocks have a fine part (buds, young leaves, herbs: high quality, what small and medium
# animals select) and a coarse part (stems, old leaves, rank grass, reed: low quality, what only big guts can live on)
SPLIT = {"grass": (0.30, 0.80, 0.35), "browse": (0.30, 0.80, 0.35), "heather": (0.25, 0.65, 0.30), "aquatic": (0.30, 0.75, 0.30)}
for _f, (_share, _qf, _qc) in SPLIT.items():
    _base = FOOD.pop(_f)
    FOOD[_f] = dict(_base, cap=_base["cap"] * _share, q=_qf)
    FOOD[_f + "~coarse"] = dict(_base, cap=_base["cap"] * (1 - _share), q=_qc)


def selectivity(mass):
    """How well an animal picks the fine part: 1 for a hare, about 0.4 for a red deer, 0 for an aurochs."""
    return float(np.clip(1 - np.log10(max(mass, 1.0) / 2.0) / 2.5, 0, 1))


def expand(diet, mass):
    """A diet over bulk foods becomes a diet over their fine and coarse parts, by selectivity."""
    s = selectivity(mass); out = {}
    for it, p in diet.items():
        if it in SPLIT:
            out[it] = p * (0.3 + 0.7 * s)
            out[it + "~coarse"] = p * (1.05 - s)
        else:
            out[it] = p
    return out


# weather: which foods a year's draws touch (drought on grass, a wet year on seeds and fruit, mast and nut years)
YEAR = {"mast": (0.25, 3.0, 0.25, 0.1), "nuts": (0.3, 2.0, 0.2, 0.3), "fruit": (0.3, 1.6, 0.2, 0.4), "conifer seed": (0.3, 2.5, 0.2, 0.2)}
GROWTH_SD = {"grass": 0.2, "sward": 0.2, "browse": 0.12, "heather": 0.1, "aquatic": 0.15, "seeds": 0.25, "inverts": 0.2, "roots": 0.1}
GROWTH_SD.update({f + "~coarse": GROWTH_SD[f] for f in SPLIT})
KLEIBER = {"herb": 0.075, "gran": 0.065, "omni": 0.07, "carn": 0.11}      # kg dry-equivalent a day per kg^0.75 (carnivores: meat)


def kind(mass, cls, b, m, hab, diet, breed=("spring",), terr=None, hibernate=False, starve=1.0, move=0.1, limits=None,
         migrant=None, arrive=None, people=0.0, vuln=0.4, switch=None, d0=1.0, ref=None, uses="", damage="", notes=""):
    """mass kg; cls: herb, gran, omni or carn; b young a head a year in good condition; m death a year; hab: weights over features;
    diet: {food or kind: preference}; terr: a territorial ceiling a km2 of full habitat; ref: a real density a km2 of good habitat,
    used only to report, never to fit."""
    return dict(mass=mass, cls=cls, b=b, m=m, hab=hab, diet=diet, breed=breed, terr=terr, hibernate=hibernate, starve=starve,
                move=move, limits=limits or {}, migrant=migrant, arrive=arrive, people=people, vuln=vuln,
                switch=switch if switch is not None else (1.5 if any(x not in FOOD for x in diet) else 1.0), d0=d0, ref=ref,
                uses=uses, damage=damage, notes=notes)


def damuth(mass, cls):
    """A typical density a km2 for this body size (Damuth 1981: about 10^4.23 x grams^-0.75 for plant-eating mammals;
    meat-eaters about a thirtieth): the scale crowding is measured on, from biology, not from any target."""
    d = 10 ** (4.23 - 0.75 * np.log10(max(mass, 0.001) * 1000.0))
    return d / 30.0 if cls == "carn" else (d / 3.0 if cls == "omni" else d)


def value(q, mass):
    """What a kg of food of quality q is worth to an animal of this mass (big guts get more from coarse food)."""
    lift = np.clip(np.log10(max(mass, 1.0) / 20.0) / 1.5, 0, 1) * 0.6
    small = np.clip(1 - np.log10(max(mass, 0.01) / 0.5) / 2.0, 0, 1)          # tiny guts cannot use coarse food at all
    return (q + (1 - q) * lift) * (1 - 0.8 * small) if q < 0.5 else q


def reserve_seasons(mass, hibernate):
    return (0.12 * mass ** 0.33) * (2.0 if hibernate else 1.0)


def suitability(feat, k):
    s = np.zeros(feat["land"].shape)
    for fe, w in k["hab"].items():
        s = s + w * feat[fe]
    s = np.clip(s, 0, 1)
    for lim, (lo, hi) in k["limits"].items():
        x = feat[lim]; w = 0.15 * abs(hi - lo) + 1e-9
        s = s * np.clip((x - lo) / w, 0, 1) * np.clip((hi - x) / w, 0, 1)
    return s * feat["land"]


def run(feat, res, kinds, years=60, seed=0, scale=None, people=True, policy=None, dens0=None, knobs=None, flux=False):
    """scale: {food: multiplier on its cap or production} (the calibration). Returns per-year means a km2 of land, and records."""
    rng = np.random.default_rng(seed)
    scale = scale or {}; knobs = knobs or {}
    res = dict(res); res.update({f + "~coarse": res[f] for f in SPLIT})
    kinds = {n: dict(k, diet=expand(k["diet"], k["mass"])) for n, k in kinds.items()}
    names = list(kinds); shape = feat["land"].shape; land = feat["land"]; L = land.sum()
    suit = {n: suitability(feat, kinds[n]) for n in names}
    crowd_at = {n: 3.0 * damuth(kinds[n]["mass"], kinds[n]["cls"]) * knobs.get("crowd", 1.0) for n in names}
    N = {n: (dens0[n].copy() if dens0 and n in dens0 else (kinds[n]["ref"] or 1.0) * kinds[n]["d0"] * 0.5 * suit[n]) for n in names}
    E = {n: np.full(shape, 0.6) for n in names}                             # reserves, 0 to 1
    stock = {f: res[f] * FOOD[f]["cap"] * scale.get(f.split("~")[0], 1.0) * 0.6 for f, s in FOOD.items() if s["type"] == "stock"}
    pulse = {f: np.zeros(shape) for f, s in FOOD.items() if s["type"] == "pulse"}
    carrion = np.zeros(shape)
    near = feat["farm"] > 0.05
    out = {n: [] for n in names}
    rec = {"crop_damage": [], "stock_killed": [], "store_loss": [], "take": {n: [] for n in names}, "mast": [], "flux": {}}
    for y in range(years):
        draw = {}
        for f, (pg, xg, pb, xb) in YEAR.items():
            u = rng.random(); draw[f] = xg if u < pg else (xb if u > 1 - pb else 1.0)
        wx = {f: float(np.exp(rng.normal(0, sd * knobs.get("weather", 1.0)))) for f, sd in GROWTH_SD.items()}
        hard = rng.random() < 0.15 * knobs.get("weather", 1.0)
        if knobs.get("weather_fn"):                                   # an external weather system drives the year (02zp:
            ext = knobs["weather_fn"](y)                              # 37.4's, when it arrives): {growth: {food: x}, hard: bool}
            wx.update(ext.get("growth", {})); hard = bool(ext.get("hard", hard))
        rec["mast"].append(draw["mast"])
        dmg = stk = sto = 0.0; taken = {n: 0.0 for n in names}; mig_seen = {}
        for si, season in enumerate(SEASONS):
            # plants grow; pulses come and rot
            for f, B in stock.items():
                cap = res[f] * FOOD[f]["cap"] * scale.get(f.split("~")[0], 1.0)
                g = FOOD[f]["grow"][si] * wx.get(f, 1.0) * (0.3 if hard and season == "winter" else 1.0)
                stock[f] = B + g * cap * np.clip(1 - B / np.maximum(cap, 1e-9), 0, 1) + 0.02 * cap * (B < 0.05 * cap)
            for f in pulse:
                sp = FOOD[f]
                pulse[f] = pulse[f] * (1 - sp["rot"]) + res[f] * sp["prod"] * scale.get(f, 1.0) * sp["season"][si] * draw.get(f, 1.0) \
                    * wx.get(f, 1.0) * (0.4 if hard and season == "winter" else 1.0)
            avail = {**stock, **pulse, "carrion": carrion}
            present = {n: kinds[n]["migrant"] is None or season in kinds[n]["migrant"] for n in names}
            for n in names:
                k = kinds[n]
                if k["migrant"] is not None:
                    if season == k["migrant"][0]:
                        N[n] = k["arrive"] * suit[n] * knobs.get("arrive_" + n, 1.0)
                    elif not present[n]:
                        N[n] = np.zeros(shape)
                    if present[n]:
                        mig_seen[n] = max(mig_seen.get(n, 0.0), float((N[n] * land).sum() / L))
            for n in names:
                refuge = 0.1 * crowd_at[n] / 3.0 * suit[n]                        # always some out of reach
                avail["kind:" + n] = np.maximum(N[n] - refuge, 0) * kinds[n]["mass"] * kinds[n]["vuln"] if present[n] else np.zeros(shape)
            # demand: what each body needs this season (more when fattening), nothing while hibernating
            want = {}; need = {}
            for n in names:
                k = kinds[n]
                if not present[n] or (k["hibernate"] and season == "winter"):
                    continue
                base = N[n] * KLEIBER[k["cls"]] * k["mass"] ** 0.75 * 91.0
                need[n] = base
                hungry = base * (1.0 + 0.4 * np.clip(1 - E[n], 0, 1))           # eats more to fatten when lean
                if k["cls"] == "carn":                                            # predators get in each other's way
                    hungry = hungry / (1.0 + N[n] / np.maximum(crowd_at[n] * suit[n], 1e-9))
                items = [(it, p) for it, p in k["diet"].items() if it in FOOD or it in kinds]
                if not items:                                                     # does not feed here (a salmon on its run)
                    continue
                def worth(it):                                                    # energy to this animal of a kg of it
                    return value(FOOD[it]["q"], k["mass"]) if it in FOOD else 0.95
                # foraging for energy: take what is worth most first (value squared), in proportion to what stands
                w = np.stack([p * worth(it) ** 2 * np.power(np.maximum(avail.get(it if it in FOOD else "kind:" + it, np.zeros(shape)), 0) + 1e-6, k["switch"])
                              for it, p in items])
                sh = w / w.sum(0)
                for (it, p), s_ in zip(items, sh):
                    key = it if it in FOOD else "kind:" + it
                    want.setdefault(key, []).append((n, hungry * s_))
            got = {n: np.zeros(shape) for n in need}
            for key, lst in want.items():
                tot = sum(x for _, x in lst)
                cap_ = np.maximum(avail.get(key, 0.0), 0) * (0.6 if key in stock else 0.8)   # never eaten to the ground
                f_ = np.where(tot > cap_, cap_ / np.maximum(tot, 1e-12), 1.0)
                for n, x in lst:
                    g = x * f_
                    item = key[5:] if key.startswith("kind:") else key
                    q = FOOD[item]["q"] if item in FOOD else 0.95
                    got[n] += g * value(q, kinds[n]["mass"]) / 0.6              # worth, against ordinary forage (0.6 digestible)
                    if flux and y >= years - 10:
                        rec["flux"][(n, key)] = rec["flux"].get((n, key), 0.0) + float((g * land).sum()) / 10.0
                    if key.startswith("kind:"):
                        prey = key[5:]
                        N[prey] = np.maximum(N[prey] - g / kinds[prey]["mass"] * 1.2, 0)
                        carrion = carrion + 0.2 * g
                    elif key in stock:
                        stock[key] = np.maximum(stock[key] - g, 0)
                    elif key in pulse:
                        pulse[key] = np.maximum(pulse[key] - g, 0)
                        if key == "crops": dmg += float((g * land).sum()) * 3
                        if key == "livestock": stk += float((g * land).sum())
                        if key == "stores": sto += float((g * land).sum())
                    elif key == "carrion":
                        carrion = np.maximum(carrion - g, 0)
            carrion = carrion * 0.5
            # condition, death and birth
            for n in names:
                k = kinds[n]
                if not present[n]:
                    continue
                R = reserve_seasons(k["mass"], k["hibernate"])
                if n in need:
                    s = np.where(need[n] > 1e-12, got[n] / np.maximum(need[n], 1e-12), 1.0)
                else:                                                            # hibernating: living on fat
                    s = np.zeros(shape)
                E[n] = E[n] + (s - 1.0) / R
                short = np.clip(-E[n], 0, None) * R                                # need not covered by fat
                E[n] = np.clip(E[n], 0, 1)
                crowd = N[n] / np.maximum(crowd_at[n] * suit[n], 1e-9)
                surv = np.exp(-k["m"] / 4 - k["starve"] * short - 0.15 * crowd ** 2)     # disease and parasites
                if k["terr"]:
                    tc = N[n] / np.maximum(k["terr"] * suit[n], 1e-9)
                    surv = surv * np.exp(-0.5 * np.clip(tc - 1, 0, None))
                dead = N[n] * (1 - surv)
                if knobs.get("debug") and n == knobs["debug"]:
                    wts = N[n] * land; W_ = max(float(wts.sum()), 1e-12)
                    rec.setdefault("dbg", []).append((y, season, round(float((s * wts).sum() / W_), 2), round(float((E[n] * wts).sum() / W_), 2),
                                                     round(float((short * wts).sum() / W_), 2), round(float(((1 - surv) * wts).sum() / W_), 3)))
                carrion = carrion + dead * k["mass"] * 0.6
                N[n] = N[n] - dead
                if season in k["breed"] and k["migrant"] is None:
                    cond = np.clip(0.2 + 0.8 * E[n], 0, 1) / (1.0 + crowd ** 2)
                    N[n] = N[n] * (1 + k["b"] / len(k["breed"]) * cond)
                if people and k["people"] > 0:
                    t = N[n] * k["people"] / 4 * near * (policy.get(n, 1.0) if policy else 1.0)
                    N[n] = N[n] - t; taken[n] += float(t.sum())
                if k["move"] > 0 and k["migrant"] is None:
                    att = suit[n] * (0.3 + E[n])
                    N[n] = _disperse(N[n], att, k["move"])
                N[n] = N[n] + 0.002 * suit[n] * (k["ref"] or 1.0) * _edge(shape)
        for n in names:
            out[n].append(mig_seen.get(n, 0.0) if kinds[n]["migrant"] is not None else float((N[n] * land).sum() / L))
            rec["take"][n].append(taken[n])
        rec["crop_damage"].append(dmg); rec["stock_killed"].append(stk); rec["store_loss"].append(sto)
    rec["final"] = {n: N[n] for n in names}; rec["suit"] = suit; rec["stock_end"] = stock
    return out, rec


def _disperse(N, att, m):
    mov = m * N; out = N - mov; tot = np.zeros_like(N); parts = []
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a = np.roll(att, (dy, dx), (0, 1)) + 1e-9; parts.append((dy, dx, a)); tot += a
    for dy, dx, a in parts:
        out += np.roll(mov * a / tot, (-dy, -dx), (0, 1))
    return out


def _edge(shape):
    e = np.zeros(shape); e[0, :] = e[-1, :] = e[:, 0] = e[:, -1] = 1.0
    return e
