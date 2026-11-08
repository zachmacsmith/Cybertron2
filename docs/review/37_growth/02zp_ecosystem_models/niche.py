"""M1: plants placed by conditions, not by labels.

Each cell's conditions are put on the Ellenberg indicator scales (light L 1-9, moisture F 1-12, reaction R 1-9, nitrogen N 1-9,
salt S 0-9). Each plant kind has its indicator values (approximately the British values of Hill et al. 1999, from memory: to be checked
against the published table before anything is built), a layer, a competitive weight, and its tolerance of grazing and of burning.
Suitability is the product of tolerance curves; within a layer the shares are soft dominance: (C * suit) ** k, normalised with bare
ground. The canopy sets the light below it. Labels are then read back from the dominant kinds and compared with the generator's.
"""
from __future__ import annotations

import numpy as np

# kind: layer, L, F, R, N, S, C (competitive weight), graze (tolerance 0-1), burn (tolerance 0-1), cast (canopy shade 0-1), group
# groups name what a label is read from. Uses are in kinds_uses (economy.py).
K = {
    # canopy
    "oak":         ("canopy", 6, 5.5, 5.0, 4.5, 0, 1.0, 0.0, 0.0, 0.70, "oak"),
    "sessile oak": ("canopy", 6, 6.0, 3.5, 3.0, 0, 0.9, 0.0, 0.0, 0.70, "upland oak"),
    "ash":         ("canopy", 5, 6.0, 7.0, 6.5, 0, 0.9, 0.0, 0.0, 0.60, "oak"),
    "beech":       ("canopy", 3, 4.5, 6.5, 5.0, 0, 1.15, 0.0, 0.0, 0.95, "beech"),
    "alder":       ("canopy", 5, 8.5, 6.0, 6.0, 0, 1.0, 0.0, 0.0, 0.70, "carr"),
    "tree willow": ("canopy", 7, 8.5, 7.0, 6.5, 0, 0.6, 0.0, 0.0, 0.50, "carr"),
    "birch":       ("canopy", 7, 6.0, 3.0, 3.0, 0, 0.7, 0.0, 0.1, 0.45, "birch"),
    "pine":        ("canopy", 7, 4.5, 2.0, 2.0, 0, 0.8, 0.0, 0.0, 0.60, "birch"),
    "yew":         ("canopy", 4, 5.0, 7.5, 5.0, 0, 0.3, 0.0, 0.0, 0.95, "beech"),
    # shrubs
    "hazel":       ("shrub", 5, 5.5, 6.5, 5.5, 0, 1.0, 0.1, 0.1, 0.0, "shrub"),
    "hawthorn":    ("shrub", 6, 5.0, 7.0, 6.0, 0, 1.0, 0.3, 0.1, 0.0, "shrub"),
    "blackthorn":  ("shrub", 6, 5.0, 7.0, 6.0, 0, 0.9, 0.3, 0.2, 0.0, "shrub"),
    "bramble":     ("shrub", 6, 6.0, 6.0, 6.0, 0, 1.2, 0.25, 0.3, 0.0, "shrub"),
    "gorse":       ("shrub", 8, 5.0, 4.0, 3.0, 0, 1.1, 0.35, 0.6, 0.0, "shrub"),
    "elder":       ("shrub", 7, 5.0, 7.0, 7.5, 0, 0.8, 0.2, 0.1, 0.0, "shrub"),
    "sallow":      ("shrub", 7, 8.0, 6.0, 5.0, 0, 0.9, 0.2, 0.1, 0.0, "carr"),
    "crab apple":  ("shrub", 7, 5.0, 6.0, 5.0, 0, 0.4, 0.2, 0.1, 0.0, "shrub"),
    "dog rose":    ("shrub", 7, 5.0, 6.0, 5.0, 0, 0.4, 0.4, 0.2, 0.0, "shrub"),
    # field layer
    "rich grasses":   ("field", 8, 5.5, 6.0, 6.0, 0, 1.0, 0.95, 0.5, 0.0, "grass"),
    "fine grasses":   ("field", 7, 5.0, 4.0, 3.0, 0, 0.9, 0.95, 0.6, 0.0, "acid grass"),
    "chalk turf":     ("field", 8, 3.5, 8.0, 2.5, 0, 0.9, 0.95, 0.5, 0.0, "chalk"),
    "meadow herbs":   ("field", 7, 6.5, 6.0, 5.0, 0, 1.0, 0.3, 0.4, 0.0, "meadow"),
    "heather":        ("field", 7, 6.0, 2.0, 2.0, 0, 1.0, 0.6, 0.9, 0.0, "heath"),
    "bilberry":       ("field", 5, 6.0, 2.0, 2.0, 0, 0.6, 0.5, 0.6, 0.0, "heath"),
    "bracken":        ("field", 6, 5.0, 3.0, 3.5, 0, 1.15, 0.7, 0.8, 0.0, "bracken"),
    "moor grass":     ("field", 7, 8.0, 3.0, 2.0, 0, 1.0, 0.8, 0.8, 0.0, "wet heath"),
    "cotton-grass":   ("field", 8, 9.5, 2.0, 1.5, 0, 1.0, 0.7, 0.6, 0.0, "bog"),
    "sphagnum":       ("field", 7, 9.5, 1.5, 1.0, 0, 1.0, 0.6, 0.5, 0.0, "bog"),
    "rushes":         ("field", 7, 8.0, 5.0, 4.5, 0, 1.0, 0.9, 0.5, 0.0, "rush"),
    "reed":           ("field", 7, 10.5, 7.0, 6.0, 0, 1.6, 0.3, 0.7, 0.0, "reed"),
    "sedge":          ("field", 8, 9.5, 7.0, 4.0, 0, 1.2, 0.4, 0.6, 0.0, "fen"),
    "meadowsweet":    ("field", 7, 8.0, 6.5, 5.5, 0, 1.0, 0.2, 0.4, 0.0, "fen"),
    "nettle":         ("field", 6, 6.0, 7.0, 8.0, 0, 1.4, 0.6, 0.5, 0.0, "nettle"),
    "dock":           ("field", 7, 6.0, 7.0, 8.0, 0, 0.8, 0.9, 0.5, 0.0, "nettle"),
    "wild garlic":    ("field", 4, 6.5, 7.0, 7.0, 0, 1.0, 0.2, 0.3, 0.0, "wood floor"),
    "bluebell":       ("field", 5, 5.5, 5.0, 6.0, 0, 0.8, 0.2, 0.3, 0.0, "wood floor"),
    "dog's mercury":  ("field", 3, 6.0, 7.0, 7.0, 0, 1.0, 0.2, 0.3, 0.0, "wood floor"),
    "watercress":     ("field", 7, 10.5, 7.0, 7.0, 0, 0.6, 0.5, 0.5, 0.0, "reed"),
    "salt grasses":   ("field", 8, 8.0, 7.0, 6.0, 7.0, 1.2, 0.9, 0.5, 0.0, "salt"),
    "samphire":       ("field", 9, 9.0, 7.0, 6.0, 8.0, 0.7, 0.5, 0.5, 0.0, "salt"),
    "marram":         ("field", 9, 3.5, 7.0, 3.0, 2.5, 1.2, 0.6, 0.5, 0.0, "dune"),
}
WIDTH = {"beech": (0.8, 1.0, 1.0), "alder": (0.7, 1.0, 1.0), "hawthorn": (1.0, 1.0, 1.4), "blackthorn": (1.0, 1.0, 1.4), "pine": (0.8, 0.8, 0.8), "reed": (0.8, 1.2, 1.2), "chalk turf": (1.2, 0.6, 0.8),
         "heather": (1.3, 0.8, 0.8), "salt grasses": (1.4, 1.5, 1.5), "samphire": (1.2, 1.5, 1.5)}
HMAX = {"bracken": 450.0, "beech": 300.0, "ash": 400.0, "hazel": 450.0, "oak": 350.0, "gorse": 400.0, "bramble": 400.0,
        "nettle": 500.0, "hawthorn": 450.0, "blackthorn": 300.0}     # frost and exposure: fading over the next 100 m
NAMES = list(K)
LAYER = np.array([K[n][0] for n in NAMES])
IND = np.array([[K[n][i] for i in range(1, 6)] for n in NAMES], dtype=float)     # L F R N S
C = np.array([K[n][6] for n in NAMES])
GRAZE = np.array([K[n][7] for n in NAMES])
BURN = np.array([K[n][8] for n in NAMES])
CAST = np.array([K[n][9] for n in NAMES])
GROUP = np.array([K[n][10] for n in NAMES])

P = {   # calibrate
    "wF": 1.5, "wR": 1.8, "wN": 1.8, "wL": 1.3, "k": 3.0, "bare": {"canopy": 0.2, "shrub": 0.35, "field": 0.05},
    "treeline_m": 560.0, "treeline_w": 140.0, "salt_w": 1.3,
}


def conditions(d, use=None):
    """Ellenberg-scale conditions of each land cell from the generator's fields. `use` adds the land's use (grazing, mowing, dung)."""
    wet, h, tex, moist, slope = d["wet"], d["h"], d["tex"], d["moist"], d["slope"]
    terrain, system = d["terrain"], d["system"]
    # moisture: the wetness index, drier on free-draining chalk and sand, wetter under high rain
    F = 4.5 + 6.5 * np.clip(wet, 0, 1) - np.select([tex == 3, tex == 0], [1.5, 1.0], 0.0) \
        + 1.5 * np.clip(moist - 0.55, 0, 0.35) / 0.35
    F = np.where(d["lake"] | (d["river"] >= 3), 12.0, F)
    # reaction: by texture, leached by height and rain; a fen's peat is base-rich, a bog's acid
    R = np.select([tex == 3, tex == 2, tex == 1, tex == 0, tex == 4], [8.0, 6.5, 6.0, 3.0, 6.5], 6.0)
    R = R - 3.5 * np.clip((h - 180) / 300, 0, 1) - 1.5 * np.clip(moist - 0.55, 0, 0.35) / 0.35
    R = np.where((tex == 3), np.maximum(R, 7.0), R)
    # nitrogen: by texture (chalk and sand are poor), silt on floodplains, less with height
    N = np.select([tex == 3, tex == 2, tex == 1, tex == 0, tex == 4], [3.5, 6.0, 5.5, 2.5, 5.0], 5.0)
    N = N + 1.0 * ((d["f"] < 2) & (d["near_river"] >= 2)) - 3.5 * np.clip((h - 150) / 300, 0, 1)
    N = np.where((F > 9) & (R < 4), np.minimum(N, 1.5), N)                  # waterlogged acid peat: a bog
    S = np.where(terrain == "saltmarsh", 7.5, 0.0)
    tidal = (h < 3) & (d["c"] < 1.0) & ~d["sea"] & ((wet >= 0.6) | (system == "fen"))
    S = np.where(tidal, 7.5, S)
    S = np.where((terrain == "coast") & (d["c"] < 0.6), np.maximum(S, 2.5), S)
    alt = np.clip((P["treeline_m"] - h) / P["treeline_w"], 0, 1)          # trees thin out toward the tree line
    rock = slope >= 30
    if use:
        N = N + use.get("dN", 0)
    return {"F": F, "R": np.clip(R, 1, 9), "N": np.clip(N, 1, 9), "S": S, "alt": alt, "rock": rock, "h": h}


def _g(x, mu, w):
    return np.exp(-0.5 * ((x - mu) / w) ** 2)


def suit(cond, L):
    """Suitability of every kind on every cell (kinds x cells), given the light L reaching that layer."""
    F, R, N, S = (cond[k].ravel() for k in ("F", "R", "N", "S"))
    out = np.empty((len(NAMES), F.size))
    for i, n in enumerate(NAMES):
        Lk, Fk, Rk, Nk, Sk = IND[i]
        mF, mR, mN = WIDTH.get(n, (1.0, 1.0, 1.0))
        s = _g(F, Fk, P["wF"] * mF) * _g(R, Rk, P["wR"] * mR) * _g(N, Nk, P["wN"] * mN)
        if n in HMAX:
            s = s * np.clip((HMAX[n] + 100 - cond["h"].ravel()) / 100.0, 0, 1)
        if Sk > 0:
            s = s * _g(S, Sk, P["salt_w"] * 1.5)                         # halophytes need salt
        else:
            s = s * np.exp(-np.clip(S - 1.0, 0, None) / P["salt_w"])        # others fall away with it
        Li = L.ravel() if np.ndim(L) else np.full(F.size, float(L))
        s = s * np.where(Li >= Lk, 1.0, _g(Li, Lk, P["wL"]))               # shade: below its need it fades
        if LAYER[i] == "field":                                            # shade plants are short: in full light they are overtopped
            s = s * np.exp(-np.clip(Li - Lk - 2.0, 0, None) / 1.5)
        if LAYER[i] == "canopy":
            s = s * cond["alt"].ravel() * (F <= 11.0)
        out[i] = s
    return out


def allocate(s, layer, extra=None):
    """Soft dominance within a layer: shares of each kind and of bare ground."""
    idx = np.flatnonzero(LAYER == layer)
    x = C[idx, None] * s[idx]
    if extra is not None:
        x = x * extra[idx]
    w = x ** P["k"]
    bare = P["bare"][layer] ** P["k"]
    tot = w.sum(0) + bare
    return idx, w / tot


def vegetation(cond, graze=0.0, burn=0.0, mow=0.0, canopy_open=None, cut=None, T_now=None, B_now=None):
    """The steady vegetation of each cell: canopy cover and the shares in each layer.
    graze/burn/mow are 0-1 pressures (arrays or numbers); canopy_open marks cells kept open (cleared and used)."""
    n = cond["F"].size
    gz = np.broadcast_to(np.asarray(graze, dtype=float), cond["F"].shape).ravel()
    bn = np.broadcast_to(np.asarray(burn, dtype=float), cond["F"].shape).ravel()
    mw = np.broadcast_to(np.asarray(mow, dtype=float), cond["F"].shape).ravel()
    # canopy: woody kinds recruit only where grazing and burning let them
    s9 = suit(cond, 9.0)
    ci, cshare = allocate(s9, "canopy")
    keep_woody = (1 - np.clip(gz * 1.6, 0, 1)) * (1 - bn) * (1 - mw)
    T = (1 - (P["bare"]["canopy"] ** P["k"]) / ((C[ci, None] * s9[ci]) ** P["k"]).sum(0).clip(1e-12) ) .clip(0, 1)
    T = np.clip(cshare.sum(0), 0, 1) * keep_woody
    T = np.where(cond["rock"].ravel(), 0.0, T)
    if canopy_open is not None:
        T = np.where(canopy_open.ravel(), 0.0, T)
    cast = (cshare * CAST[ci, None]).sum(0) / np.clip(cshare.sum(0), 1e-9, None)
    Tl = T if T_now is None else np.asarray(T_now, dtype=float).ravel()     # the light under today's canopy, not the steady one
    L_below = 9.0 - 6.0 * Tl * cast
    # shrub layer under the canopy's light; grazing spares the thorny
    s_sh = suit(cond, L_below)
    graze_f = 1 - gz[None, :] * (1 - GRAZE[:, None])
    burn_f = 1 - bn[None, :] * (1 - BURN[:, None])
    mow_f = 1 - mw[None, :] * (1 - np.where(LAYER == "field", np.where(GROUP == "meadow", 1.3, GRAZE), 0.0))[:, None]
    if cut:                                                               # people cutting one kind (bracken for litter, reeds)
        for kname, pressure in cut.items():
            pr = np.broadcast_to(np.asarray(pressure, dtype=float), cond["F"].shape).ravel()
            mow_f[NAMES.index(kname)] *= (1 - 0.8 * pr)
    si, sshare = allocate(s_sh, "shrub", extra=graze_f * burn_f * mow_f)
    if canopy_open is not None:
        sshare = sshare * np.where(canopy_open.ravel(), np.clip(1 - 2 * gz, 0, 1) * (1 - mw), 1.0)
    B = np.clip(sshare.sum(0), 0, 1) * (1 - 0.6 * Tl)
    Bl = B if B_now is None else np.asarray(B_now, dtype=float).ravel()
    L_field = L_below - 2.5 * Bl
    s_f = suit(cond, L_field)
    fi, fshare = allocate(s_f, "field", extra=graze_f * burn_f * mow_f)
    return {"T": T, "B": B, "canopy": (ci, cshare), "shrub": (si, sshare), "field": (fi, fshare), "L_field": L_field}


def dominant(v):
    """The dominant kind in each layer, by index into NAMES, and its share."""
    out = {}
    for layer in ("canopy", "shrub", "field"):
        idx, sh = v[layer]
        j = sh.argmax(0)
        out[layer] = (idx[j], sh.max(0))
    return out


def label(v, cond, h, terrain):
    """Read a generator label back from the vegetation (the test of the niches)."""
    dom = dominant(v)
    T, B = v["T"], v["B"]
    n = T.size
    lab = np.full(n, "grassland", dtype=object)
    grp_f = GROUP[dom["field"][0]]
    grp_c = GROUP[dom["canopy"][0]]
    h = h.ravel()
    wood = T >= 0.5
    open_ = ~wood
    m = {"heath": np.where(h >= 250, "moor", "lowland heath"), "wet heath": np.where(h >= 250, "moor", "wet grassland"),
         "bog": "blanket bog", "reed": "reedbed", "fen": "fen", "salt": "saltmarsh", "dune": "dune grassland",
         "chalk": "chalk grassland", "meadow": "hay meadow", "rush": "wet grassland",
         "acid grass": np.where(h >= 250, "hill pasture", "grassland"), "grass": "grassland", "bracken": "bracken",
         "nettle": "nettle bed", "wood floor": "grassland"}
    for g_, l_ in m.items():
        sel = open_ & (grp_f == g_)
        lab[sel] = l_[sel] if isinstance(l_, np.ndarray) else l_
    lab[open_ & (B >= 0.45)] = "scrub"
    wl = {"oak": "oak-ash wood", "upland oak": "upland oak wood", "beech": "beech wood", "carr": "alder carr", "birch": "birch and pine wood"}
    for g_, l_ in wl.items():
        lab[wood & (grp_c == g_)] = l_
    lab[wood & (grp_c == "upland oak") & (h < 150)] = "birch and pine wood"
    lab[cond["rock"].ravel()] = "bare rock"
    return lab
