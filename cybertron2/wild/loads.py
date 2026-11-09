"""Loads and phenology (wild_layer.md §6 phase 7, wave 3): fast kinds counted as a level an area, and the calendar markers the year's
warmth brings. Pure functions of the ecology's state, the land and the day's weather, called from the ecology step, so the history
before a run and the run itself step them alike.

A load's level (1 an ordinary year) moves each day toward a target: its ground (`hab`, from the area's soils and covers) times its
weather drivers (wet soil, warmth over the season's mean, dryness), in its seasons; out of them it falls toward `rest`. A load that
`follows` another moves toward that one's level (ladybirds after the fly); one `eaten_by` another loses a share a day for each unit
of the eater's level. A frozen night kills a share. The harm a load does (to crops of a family at an age) and what it feeds (a
parcel resource) are the engine's side (engine/wild.py). Every number is the kinds' data (kinds.LOADS, kinds.MARKERS).
"""
from __future__ import annotations

import numpy as np

from cybertron2.wild import kinds as WK


def habitat(land: dict, ids: list, spec: dict) -> np.ndarray:
    """A load's ground in each area: its soils' weights by the area's soil shares, times its covers' by the area's cover shares."""
    out = []
    for a in ids:
        ar = land["areas"][a]
        km2 = max(float(ar["km2"]), 1e-9)
        tex = (spec["hab"].get("texture"))
        t = sum(float(w) * float((ar.get("texture") or {}).get(k, 0.0)) for k, w in tex.items()) if tex else 1.0
        cov = spec["hab"].get("cover") or {}
        c = sum(float(w) * float(ar["cover"].get(k, 0.0)) for k, w in cov.items()) / km2 if cov else 1.0
        out.append(t * min(1.0, c))
    h = np.array(out)
    home = np.array([land["areas"][a]["kind"] == "home" for a in ids])
    ref = float(np.median(h[home & (h > 0)])) if (home & (h > 0)).any() else 1.0
    return np.clip(h / max(ref, 1e-9), 0, 2.0)                                # a village's ordinary ground near 1


def initial(m) -> dict:
    return {"level": {k: [float(v.get("start", 1.0))] * m.n for k, v in WK.LOADS.items()}, "gdd": [0.0] * m.n, "marks": {}}


def step(m, st: dict, day: int, temp: np.ndarray, low: np.ndarray, frozen: np.ndarray, soil: np.ndarray) -> None:
    """One engine day of the loads and the year's warmth (in place on st["loads"])."""
    from cybertron2.wild.ecology import SEASON_T
    L = st.setdefault("loads", initial(m))
    if not hasattr(m, "load_hab"):
        m.load_hab = {k: habitat(m.land, m.ids, v) for k, v in WK.LOADS.items()}
    Y, S = m.Y, m.S
    si, sd = (day % Y) // S, day % S
    lv = {k: np.asarray(L["level"].get(k, [1.0] * m.n), float) for k in WK.LOADS}
    wetf = np.clip(soil, 0.3, 2.5)                                             # soil wetness, 1 at the mean rain
    warm = temp - SEASON_T[si]
    new = {}
    for k, spec in WK.LOADS.items():
        x = lv[k]
        if si in spec["seasons"]:
            if spec.get("follows"):
                target = sum(float(w) * lv[o] for o, w in spec["follows"].items()) * np.clip(m.load_hab[k], 0, 1.5)
            else:
                d = spec.get("drivers") or {}
                f = np.ones(m.n)
                if "wet" in d:
                    f = f * wetf ** float(d["wet"])
                if "dry" in d:
                    f = f * (1.0 / wetf) ** float(d["dry"])
                if "warm" in d:
                    f = f * np.clip(1 + float(d["warm"]) * warm, 0.3, 2.5)
                target = float(spec.get("base", 1.0)) * m.load_hab[k] * f
            x = x + float(spec["rate"]) * (target - x)
        else:
            x = x + float(spec["rate"]) * (float(spec["rest"]) * np.minimum(m.load_hab[k], 1.0) - x)
        for eater, rate in (spec.get("eaten_by") or {}).items():
            x = x * np.clip(1 - float(rate) * lv[eater], 0.3, 1.0)
        x = np.where(frozen, x * (1 - float(spec.get("frost", 0.0))), x)
        new[k] = np.clip(x, 0.0, float(spec.get("most", 4.0)))
    L["prev"] = L.get("level") or {}                                           # yesterday's, for the signs of a change
    L["level"] = {k: [round(float(v), 4) for v in x] for k, x in new.items()}
    # the year's warmth and the markers it passes (reset at the start of spring)
    if si == 0 and sd == 0:
        L["gdd"], L["marks"] = [0.0] * m.n, {}
    gdd = np.asarray(L["gdd"], float) + np.maximum(0.0, temp - WK.GDD_BASE) * (WK.REAL_DAYS / S)
    L["gdd"] = [round(float(v), 1) for v in gdd]
    if si == 1 and sd == 0:
        L["spring_gdd"] = list(L["gdd"])                                     # the spring's warmth, for what it sets (berries)
    for name, mk in WK.MARKERS.items():
        got = L["marks"].get(name) or [None] * m.n
        if "gdd" in mk:
            hit = gdd >= float(mk["gdd"])
        else:
            a = mk["after"]
            hit = (si >= int(a["season"])) & (low < float(a["low"]))
        L["marks"][name] = [g if g is not None else (day if bool(h) else None) for g, h in zip(got, hit)]
