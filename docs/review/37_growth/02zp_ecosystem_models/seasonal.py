"""M4: the wild food a village's land gives, by season, from real yields; against its need and against the engine's forage now.

Units: person-days (pd) of food (3,000 kcal), real, per hectare of the kind's cover a year, in a normal year, after what animals
take and what people can reach (first values from the foraging and agronomy literature, approximate: the note §M4). The
engine's time compression cancels when both sides are shares of the village's need.
"""
from __future__ import annotations

import numpy as np

import niche as NI

SEASONS = ("spring", "summer", "autumn", "winter")
# kind or group -> (pd/ha/yr on full cover, season shares, keeps?, note). "cover" is read from M1's layers (share of a cell).
FOOD = {
    "hazel nuts":   (63.0, (0, 0, 1.0, 0), True, "100 kg kernels/ha in a normal year, 30% reached before squirrels and mice"),
    "acorns, mast": (40.0, (0, 0, 0.9, 0.1), True, "only after leaching (a knack); mast years x4, busts x0.1"),
    "brambles":     (24.0, (0, 0.5, 0.5, 0), False, "400 kg/ha, 40% reached"),
    "bilberries":   (12.0, (0, 1.0, 0, 0), False, ""),
    "hedge fruit":  (12.0, (0, 0, 0.8, 0.2), True, "haws, sloes, crab apples, hips: some keep"),
    "roots":        (1.0, (0.4, 0.3, 0.3, 0), False, "pignut, silverweed: hard work for little"),
    "fungi":        (2.0, (0, 0.1, 0.9, 0), False, "low in food; some poisonous"),
    "greens":       (0.0, (0.6, 0.4, 0, 0), False, "nettle, ramsons, sorrel, watercress: health, not calories (capped)"),
    "deer, boar":   (0.6, (0.15, 0.15, 0.4, 0.3), False, "M3: ~0.15 pd/ha from deer, ~0.5 from boar, on wood"),
    "hares":        (0.16, (0.25, 0.25, 0.25, 0.25), False, "M3, on open land"),
    "trout":        (25.0, (0.2, 0.4, 0.3, 0.1), False, "per ha of brook or small river"),
    "eels":         (30.0, (0.1, 0.3, 0.6, 0.0), True, "per ha of fen water or river; the autumn run; smoked they keep"),
    "fowl":         (3.0, (0.1, 0, 0.2, 0.7), False, "per ha of fen, reedbed or saltmarsh: winter flocks"),
    "shellfish":    (50.0, (0.3, 0.1, 0.2, 0.4), False, "per ha of shore and saltmarsh creek: the coast's spring food"),
}
GREENS_CAP = 0.10   # greens give at most this share of a season's need in calories


def cover_by_kind(v, d):
    """Hectares-equivalent cover of each food source on each cell (share of the cell)."""
    ci, cs = v["canopy"]; si, ss = v["shrub"]; fi, fs = v["field"]
    T, B = v["T"], v["B"]
    def share(idx, sh, names):
        out = np.zeros(sh.shape[1])
        for n in names:
            if NI.NAMES.index(n) in idx:
                out += sh[list(idx).index(NI.NAMES.index(n))]
        return out
    sh_share = lambda names: share(si, ss, names) * B
    can_share = lambda names: share(ci, cs, names) * T
    fld = lambda names: share(fi, fs, names) * (1 - 0.5 * T)
    eco = d["eco"].ravel()
    water = (d["river"].ravel() >= 1) | d["lake"].ravel()
    fen = np.isin(eco, ["fen", "reedbed", "wet grassland"])
    salt = eco == "saltmarsh"
    shore = (d["c"].ravel() < 0.3) & ~d["sea"].ravel()
    open_ = 1 - T
    return {
        "hazel nuts": sh_share(["hazel"]) + 0.3 * can_share(["oak", "ash"]),       # hazel under oak and ash, and in hedges
        "acorns, mast": can_share(["oak", "sessile oak", "beech"]),
        "brambles": sh_share(["bramble"]) + 0.2 * T,                                  # and along wood edges and rides
        "bilberries": fld(["bilberry"]) + 0.3 * fld(["heather"]),
        "hedge fruit": sh_share(["hawthorn", "blackthorn", "crab apple", "dog rose"]) + 0.05 * open_,   # hedges in farmland
        "roots": fld(["rich grasses", "fine grasses", "meadow herbs"]),
        "fungi": T + 0.3 * fld(["rich grasses", "fine grasses"]),
        "greens": fld(["nettle", "dock", "wild garlic", "watercress", "meadow herbs"]),
        "deer, boar": T,
        "hares": open_,
        "trout": water * 0.15,                                                         # a stream is a sliver of its cell
        "eels": (fen * 0.3 + water * 0.15),
        "fowl": (fen | salt).astype(float),
        "shellfish": (salt * 0.3 + shore * 0.2),
    }


def village_calendar(v, d, site, radius_km=2.5, field_share=0.35, people=12.0, km=0.15):
    """Food by season from the land within reach of a site, as shares of the village's need; fields take field_share of the
    open land near the village (not foraged)."""
    ny, nx = d["h"].shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    r, c = site
    m = (np.hypot(yy - r, xx - c) * km <= radius_km).ravel() & ~d["sea"].ravel()
    ha = km ** 2 * 100.0                                  # hectares a cell (0.15 km: 2.25 ha)
    cov = cover_by_kind(v, d)
    need = people * 365 / 4                               # pd a season
    by = {}
    for k, (pd, seas, keeps, _) in FOOD.items():
        tot = float((cov[k][m]).sum() * ha * pd)
        if k not in ("trout", "eels", "fowl", "shellfish"):
            tot *= (1 - field_share * (k in ("roots", "hares", "hedge fruit")))
        by[k] = [tot * s / need for s in seas]
    # greens: capped
    gcov = float(cov["greens"][m].sum() * ha)
    by["greens"] = [min(GREENS_CAP * s / 0.6, gcov * 50 * s / need) for s in FOOD["greens"][1]]
    season = [sum(by[k][i] for k in by) for i in range(4)]
    keeps = sum(sum(by[k]) for k in by if FOOD[k][2]) / 4
    return {"by": by, "season": season, "year": sum(season) / 4, "storable_year": keeps,
            "area_ha": float(m.sum() * ha), "wood_share": float(v["T"][m].mean())}


ENGINE_PLANTS = {"pasture": 1.0, "meadow": 1.3, "scrub": 1.0, "heath": 0.6, "moor": 0.5, "fen": 1.0, "saltmarsh": 0.5, "forest": 1.2}
ENGINE_MSY = 2.07      # food a unit of K a year (engine_flows.py), a year of 32 days


def engine_forage(d, site, radius_km=2.5, field_share=0.35, people=12.0, km=0.15, year_days=32):
    """The engine's forage now from the same land, as a share of the same village's need (both in the engine's own year)."""
    from cybertron2.landgen.ecology import ECOSYSTEMS
    ny, nx = d["h"].shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    r, c = site
    m = (np.hypot(yy - r, xx - c) * km <= radius_km) & ~d["sea"]
    cover = np.vectorize(lambda e: ECOSYSTEMS.get(e, ("water",))[0])(d["eco"])
    units = km ** 2 * 100.0 / 2.0                          # units of size a cell (a unit is about 2 ha)
    K = sum(float(((cover == cv) & m).sum()) * units * k for cv, k in ENGINE_PLANTS.items())
    K *= (1 - field_share * 0.7)                           # fields take part of the open land
    food = K * ENGINE_MSY
    return food / (people * year_days)
