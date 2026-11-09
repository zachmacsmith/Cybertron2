"""Disease by host and area (wild_layer.md §6 phase 8, wave 4): each disease's prevalence among its wild hosts in every area,
rising with the hosts' crowding among those not immune, falling as the sick recover (immune a while: `wane`) or die, spreading along the land's links, seeded in its season by
keyed draws. Pure, called from the ecology step: it returns each host's extra death rate for the day. The kept hosts (herds) are
the engine's side (engine/wild.py), infected from the sick herds near them and from the wild hosts on their village's land.
Every number is the diseases' data (kinds.DISEASES).
"""
from __future__ import annotations

import numpy as np

from cybertron2.wild import kinds as WK


def hosts_of() -> set:
    """Every wild kind some disease here has as a host (they leave the ecology's background outbreak to it)."""
    return {k for d in WK.DISEASES.values() for k in (d.get("wild") or {})}


def step(m, st: dict, day: int, N: dict, draws: dict) -> dict:
    """One engine day of every disease in the wild (in place on st["dis"]); returns {kind: extra death rate a day per area}."""
    Y, S = m.Y, m.S
    si, sd = (day % Y) // S, day % S
    D = st.setdefault("dis", {})
    st["dis_prev"] = {k: list(v) for k, v in D.items()}
    extra = {}
    R_ = st.setdefault("dis_immune", {})
    for name, d in WK.DISEASES.items():
        I = np.asarray(D.get(name, [0.0] * m.n), float)
        R = np.asarray(R_.get(name, [0.0] * m.n), float)
        crowd = np.zeros(m.n)
        for k, wgt in (d.get("wild") or {}).items():
            if k in N:
                crowd = crowd + float(wgt) * N[k] / np.maximum(m.crowd_at[k] * m.suit[k], 1e-9)
        crowd = np.clip(crowd, 0, 3)
        rec = float(d["recover"]) * I
        I, R = I + float(d["rise"]) * crowd * I * np.clip(1 - I - R, 0, 1) - rec, R + rec - float(d["wane"]) * R   # the recovered are
        R = np.clip(R, 0, 1)                                                                                     # immune a while
        if len(m.la):
            dI = float(d["mix"]) * (I[m.lb] - I[m.la])
            out = np.zeros(m.n)
            np.add.at(out, m.la, dI)
            np.add.at(out, m.lb, -dI)
            I = I + out
        if si == int(d.get("season", 1)) and sd == 0 and name in (draws.get("dis") or {}):
            u = np.asarray(draws["dis"][name], float)
            I = np.where(u < float(d["seed"]) * crowd ** 2, np.maximum(I, 0.05), I)
        I = np.where(I < 1e-4, 0.0, np.clip(I, 0, 1))
        D[name] = [round(float(x), 5) for x in I]
        R_[name] = [round(float(x), 5) for x in np.where(R < 1e-4, 0.0, R)]
        for k, wgt in (d.get("wild") or {}).items():
            extra[k] = extra.get(k, 0.0) + float(d["kill"]) * float(wgt) * I
    return extra
