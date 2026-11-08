"""M5: does ecological variety make villages need each other?

For each village (the generator's sites), the goods its land within reach gives, from M1's vegetation and the generator's soils and
waters; a village "has" a good when its land gives it enough to cover its own use with room to spare. Needs are what every village
uses (fuel, building, thatch, winter fodder, salt, and the later chains). A need a village lacks and a neighbour has is a dependence;
a good few villages have is a specialty (a chokepoint someone can hold).
Two worlds are compared: the engine's goods now (by cover) and the proposal's (by kinds and conditions).
"""
from __future__ import annotations

import numpy as np

import niche as NI
import seasonal as SE

# good -> (needed by every village?, ha of its source a village of 12 needs, how to read the source cover a cell, what for)
GOODS = {
    # needs
    "firewood":   (True, 40.0, "wood", "heat (D2-157): ~0.5 ha of wood a hearth-year as coppice"),
    "timber":     (True, 20.0, "tall wood", "building, tools"),
    "winter fodder (hay)": (True, 15.0, "hay meadow", "keeping beasts through winter"),
    "grazing":    (True, 40.0, "grass", "beasts"),
    "thatch":     (True, 3.0, "reed|heather|straw", "roofs: reed best, heather on moors, straw where grain grows"),
    "salt":       (True, 0.5, "saltmarsh", "keeping meat and fish (water_and_preservation)"),
    "wattle rods": (True, 2.0, "hazel|sallow", "wattle walls, hurdles, baskets (husbandry: withies)"),
    "daub clay":  (True, 1.0, "clay", "walls (with wattle), pots"),
    # specialties (wanted, not needed by every village)
    "peat":       (False, 5.0, "bog|fen peat", "fuel where wood is short (turbary)"),
    "furze fuel": (False, 5.0, "gorse", "oven fuel"),
    "oak bark":   (False, 5.0, "oak", "tanning hides"),
    "eels":       (False, 2.0, "eels", "food that keeps smoked; rent"),
    "fowl, down": (False, 20.0, "fowl", "winter food; bedding"),
    "shellfish":  (False, 2.0, "shellfish", "the coast's spring food"),
    "nuts":       (False, 10.0, "hazel nuts", "food that keeps"),
    "pannage":    (False, 30.0, "mast", "pigs fattened in autumn"),
    "venison":    (False, 200.0, "deer", "meat, hides; the noble's beast"),
    "honey, wax": (False, 100.0, "old wood", "sweet that keeps; wax for seals and candles"),
    "rushes":     (False, 2.0, "rushes", "rushlights, strewing, mats"),
    "lime":       (False, 1.0, "chalk", "mortar, liming acid fields"),
    "stone":      (False, 1.0, "rock", "building"),
    "ore":        (False, 0.2, "ore", "copper (built)"),
    "fish":       (False, 2.0, "fish", "food"),
}


def sources(v, d):
    """Hectare-shares of each source on each cell."""
    ci, cs = v["canopy"]; si, ss = v["shrub"]; fi, fs = v["field"]
    T, B = v["T"], v["B"]
    def sh(idx, share, names):
        out = np.zeros(share.shape[1])
        for n in names:
            j = NI.NAMES.index(n)
            if j in idx:
                out += share[list(idx).index(j)]
        return out
    cov = SE.cover_by_kind(v, d)
    eco = d["eco"].ravel(); tex = d["tex"].ravel()
    water = (d["river"].ravel() >= 1) | d["lake"].ravel()
    open_ = 1 - T
    grassy = sh(fi, fs, ["rich grasses", "fine grasses", "chalk turf", "meadow herbs", "salt grasses"]) * open_
    return {
        "wood": T, "tall wood": T * (d["band"].ravel() >= 1),
        "hay meadow": sh(fi, fs, ["meadow herbs"]) * open_ * ((d["f"].ravel() < 3) | (eco == "hay meadow")),
        "grass": grassy,
        "reed|heather|straw": sh(fi, fs, ["reed", "heather"]) + 0.15 * open_ * np.isin(d["terrain"].ravel(), list(__import__("cybertron2.landgen.vocab", fromlist=["x"]).FIELD_OK)),
        "saltmarsh": (eco == "saltmarsh").astype(float),
        "hazel|sallow": sh(si, ss, ["hazel", "sallow"]) * B + 0.02 * open_,          # and hedges
        "clay": (tex == 2).astype(float) * 0.05,
        "bog|fen peat": np.isin(eco, ["blanket bog", "fen", "reedbed"]).astype(float) * 0.5 + (tex == 4) * 0.5,
        "gorse": sh(si, ss, ["gorse"]) * B,
        "oak": sh(ci, cs, ["oak", "sessile oak"]) * T,
        "eels": cov["eels"], "fowl": cov["fowl"], "shellfish": cov["shellfish"], "hazel nuts": cov["hazel nuts"],
        "mast": cov["acorns, mast"], "deer": T, "old wood": T * (d["band"].ravel() >= 3),
        "rushes": sh(fi, fs, ["rushes"]) * open_,
        "chalk": (tex == 3).astype(float) * 0.05, "rock": (d["slope"].ravel() >= 30).astype(float),
        "ore": np.zeros(T.size), "fish": water * 0.15,
    }


def engine_sources(d):
    """The goods the engine has now, by cover: forage and grass on open covers; game, timber and firewood in forest; fish and salt
    with the water pack; stone in rock; copper in seams. Thatch, wattle rods, peat and the rest do not exist as goods."""
    from cybertron2.landgen.ecology import ECOSYSTEMS
    cover = np.vectorize(lambda e: ECOSYSTEMS.get(e, ("water",))[0])(d["eco"]).ravel()
    f = (cover == "forest").astype(float)
    water = (d["river"].ravel() >= 1) | d["lake"].ravel()
    grass_cov = np.isin(cover, ["pasture", "meadow", "heath", "moor", "fen", "saltmarsh", "scrub"]).astype(float)
    return {"wood": f, "tall wood": f, "grass": grass_cov, "saltmarsh": (cover == "saltmarsh").astype(float),
            "deer": f, "rock": (cover == "rock").astype(float), "fish": water * 0.15}


ENGINE_GOODS = {"firewood": "wood", "timber": "tall wood", "grazing": "grass", "salt": "saltmarsh", "venison": "deer",
                "stone": "rock", "fish": "fish"}


def village_goods(src, d, site, radius_km, km, goods=GOODS, people=12):
    ny, nx = d["h"].shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    m = (np.hypot(yy - site[0], xx - site[1]) * km <= radius_km).ravel() & ~d["sea"].ravel()
    ha = km ** 2 * 100.0
    have = {}
    for g, (need, ha_need, s, _) in goods.items():
        if s not in src:
            continue
        have[g] = float(src[s][m].sum() * ha) / (ha_need * people / 12)
    return have
