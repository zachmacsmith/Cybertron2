"""M2: succession on the year clock, held back or pushed by use.

State per cell: canopy cover T, shrub cover B, the field layer's shares, and offsets to fertility (dN) and moisture (dF) that use
moves. Each year the niche model (M1) gives the steady vegetation under this year's pressures; the state moves toward it at rates
limited by what really limits each change:
- trees: recruitment needs seed (canopy within ~300 m, plus jays and birds from farther), light, and freedom from browsing; thorny
  shrubs shelter seedlings from grazers (the wood-pasture cycle); a canopy then closes at its own rate;
- shrubs: spread from neighbours and seed, shaded out under a closing canopy;
- the field layer: relaxes toward its steady shares (perennials: a few years; bracken advances slowly);
- fertility: dung adds, hay and crops take, burning takes a little, a ruin's ground is rich for centuries;
- moisture: drains lower it over years; dams (beaver or people) raise it.
Rates are first values, calibrated against the real timescales in TARGETS.
"""
from __future__ import annotations

import numpy as np

import niche as NI

R = {   # calibrate (per year)
    "recruit": 0.025,     # share of the gap to the steady canopy filled a year, with full seed and no browsing
    "seed_far": 0.04,     # seed from far away (jays carry acorns kilometres; birch blows in) as a share of full seed
    "seed_cells": 2,      # the neighbourhood that counts as near seed (cells of 150 m each side)
    "close": 0.05,        # a young canopy's own closing toward the steady cover
    "shrub": 0.12,        # shrubs' spread toward their steady cover
    "shrub_seed_far": 0.1,
    "field": 0.35,        # the field layer's relaxation a year
    "bracken": 0.06,      # bracken advances slowly (rhizomes)
    "die": 0.008,         # old trees dying a year where none recruit (a wood pasture fades over ~80 to 150 years)
    "browse_trees": 0.35, # grazing pressure (0-1) that stops tree recruitment in the open
    "nurse": 2.5,         # thorny shrub cover multiplies recruitment under grazing
    "dN_dung": 0.25, "dN_hay": -0.08, "dN_burn": -0.05, "dN_crop": -0.15, "dN_decay": 0.1,
    "drain_rate": 0.4,    # moisture units a year a drained cell falls, to its drain depth
}

TARGETS = {   # the real timescales the rates must reproduce (sources in the note, §M2)
    "abandoned field, base-rich, seed near (Broadbalk wilderness)": "closed wood in 25 to 40 years",
    "abandoned field, acid, little seed (Geescroft wilderness)": "still mostly grass at 30 years; wood by 60 to 80",
    "ungrazed, unburnt lowland heath": "birch and pine invade in 10 to 15 years; birch wood in 20 to 40",
    "chalk grassland when grazing stops (after myxomatosis, 1954)": "hawthorn scrub in 10 to 20 years",
    "fen left uncut (Wicken Fen after cutting stopped)": "carr spreads within 20 to 40 years",
    "wood pasture with no recruitment": "canopy thins over a century or more",
    "deer above about 5 to 10 red deer a km2": "woodland regeneration fails",
}


def nb_mean(x, r):
    """Mean over a (2r+1)-square neighbourhood, with edges padded."""
    p = np.pad(x, r, mode="edge")
    c = np.cumsum(np.cumsum(p, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    n = 2 * r + 1
    s = c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]
    return s / (n * n)


class Land:
    def __init__(self, d, window=None):
        if window:
            (r0, r1), (c0, c1) = window
            d = {k: (v[r0:r1, c0:c1] if isinstance(v, np.ndarray) and v.ndim == 2 else v) for k, v in d.items()}
        self.d = d
        self.shape = d["h"].shape
        self.cond0 = NI.conditions(d)
        self.dN = np.zeros(self.shape)
        self.dF = np.zeros(self.shape)
        self.water = d["sea"] | d["lake"] | (d["river"] >= 3)

    def cond(self):
        c = dict(self.cond0)
        c["N"] = np.clip(c["N"] + self.dN, 1, 9)
        c["F"] = np.clip(c["F"] + self.dF, 1, 12)
        return c


def start(land, v):
    """The state from a vegetation (M1 output)."""
    fi, fs = v["field"]
    return {"T": v["T"].reshape(land.shape).copy(), "B": v["B"].reshape(land.shape).copy(), "field": fs.copy(), "fi": fi}


def step(land, st, use, deer=None):
    """One year. use: dict of 0-1 pressure arrays (graze, mow, burn, crop, fell, cut_<kind>, drain) on the land's shape.
    deer: red deer a km2 (array or number), browsing young trees and shrubs in woods and at their edges."""
    sh = land.shape
    gz = np.broadcast_to(use.get("graze", 0.0), sh).astype(float)
    if deer is not None:                                     # deer browse: about 8 a km2 is as hard on seedlings as 0.35 grazing
        gz = np.clip(gz + np.broadcast_to(deer, sh) / 8.0 * R["browse_trees"], 0, 1)
    burn = np.broadcast_to(use.get("burn", 0.0), sh).astype(float)
    mow = np.broadcast_to(use.get("mow", 0.0), sh).astype(float)
    crop = np.broadcast_to(use.get("crop", 0.0), sh).astype(float)
    drain = np.broadcast_to(use.get("drain", 0.0), sh).astype(float)
    # conditions move with use
    land.dN = land.dN + R["dN_dung"] * gz - R["dN_dung"] * 0.5 * gz * (gz > 0.8) + R["dN_hay"] * mow + R["dN_burn"] * burn \
        + R["dN_crop"] * crop - R["dN_decay"] * land.dN
    land.dF = np.maximum(land.dF - R["drain_rate"] * drain, -2.5 * drain) if drain.any() else land.dF
    cond = land.cond()
    cuts = {k[4:]: v for k, v in use.items() if k.startswith("cut_")}
    kept_open = (crop > 0) | (np.broadcast_to(use.get("open", False), sh))
    v = NI.vegetation(cond, graze=gz, burn=burn, mow=mow, canopy_open=kept_open, cut=cuts or None, T_now=st["T"], B_now=st["B"])
    Tst, Bst = v["T"].reshape(sh), v["B"].reshape(sh)
    T, B = st["T"], st["B"]
    # trees
    seed = np.clip(nb_mean(T, R["seed_cells"]) * 3.0, 0, 1) * (1 - R["seed_far"]) + R["seed_far"]
    thorny = B * 0.6                                          # a share of the shrub layer is thorny (hawthorn, blackthorn, bramble, gorse)
    browse = np.clip(gz / R["browse_trees"], 0, 1)
    shelter = np.clip(1 - browse + browse * np.clip(thorny * R["nurse"], 0, 1), 0, 1)
    light = np.clip(1 - T, 0, 1)
    gain = np.where(Tst > T, R["recruit"] * seed * shelter * light * (Tst - T) / np.maximum(Tst, 1e-3) + R["close"] * T * (Tst - T), 0.0)
    young = T < 0.3                                           # fire and the scythe kill seedlings and saplings
    kill = (burn * 0.8 + mow * 0.9) * young * T
    loss = np.where(Tst < T, R["die"] * T * (1 - shelter * 0.5), 0.0) + kill
    fell = np.broadcast_to(use.get("fell", 0.0), sh)
    T = np.clip(T + gain - loss - fell * T, 0, 1)
    T = np.where(kept_open | land.water, 0.0, T)
    # shrubs
    sseed = np.clip(nb_mean(B, 1) * 3, 0, 1) * (1 - R["shrub_seed_far"]) + R["shrub_seed_far"]
    est = 1 - 0.8 * np.clip(gz / 0.5, 0, 1) - 0.8 * np.clip(mow + burn, 0, 1)    # grazers, scythes and fire take seedling shrubs
    B = B + np.where(Bst > B, R["shrub"] * sseed * np.clip(est, 0, 1) * (Bst - B), (Bst - B) * 0.25)
    B = np.clip(np.where(kept_open | land.water, 0.0, B), 0, 1)
    # field layer: toward the steady shares; bracken slower
    fi, fs = v["field"]
    rate = np.full(len(fi), R["field"])
    rate[list(fi).index(NI.NAMES.index("bracken"))] = R["bracken"]
    F = st["field"]
    up = fs > F
    F = F + np.where(up, rate[:, None], R["field"]) * (fs - F)
    st.update(T=T, B=B, field=F, fi=fi)
    st["v"] = v
    return st


def classify(land, st):
    """Labels of the state, by the same reading as M1."""
    fi, fs = st["fi"], st["field"]
    v = {"T": st["T"].ravel(), "B": st["B"].ravel(), "field": (fi, fs), "canopy": st["v"]["canopy"], "shrub": st["v"]["shrub"]}
    return NI.label(v, land.cond(), land.d["h"], land.d["terrain"]).reshape(land.shape)
