"""Scripted households for comparison with the LLM households: none, calendar (by the season alone), and a scripted expert that
acts on the expert's readings with the lore of wild_systems.md (vary the scare; the read gap; dark nights after rain; plovers)."""
from __future__ import annotations

from rules import Y, S, season, sday, in_windows

RIPENING = [(1, 3, 7), (2, 0, 1)]
SEED = [(0, 0, 3), (2, 2, 5)]
RUN = [(2, 0, 7), (3, 0, 1)]


def has(v, k):
    return k in v.kinds and v.kinds[k].present()


def none(v, d, obs):
    return {}


def calendar(v, d, obs):
    a = {"cats": True}
    if in_windows(d, RIPENING) and (has(v, "wild boar") or has(v, "red deer")):
        a["watch"] = {g: "fire" for g in range(3)}
    if in_windows(d, SEED):
        a["scarecrow"] = True
    if has(v, "eels") and in_windows(d, RUN):
        a["eel_traps"] = True
    if has(v, "wildfowl") and d and v.drv.frozen[d - 1]:
        a["set_nets"] = True; a["fowl"] = True
    return a


def expert():
    st = {"i": 0, "turned": 0}
    scares = ["fire", "clapper", "horn"]

    def pol(v, d, obs):
        a = {"cats": True}
        gap = None
        fresh = False
        for t in (d, d - 1):
            for sg in ("boar.rooting", "deer.slots"):
                x = obs.has(t, sg, fresh=True)
                if x:
                    fresh = True; gap = x["feat"].get("gap", gap)
            for sg in ("boar.trampled", "deer.grazed"):
                x = obs.has(t, sg)
                if x:
                    fresh = True; gap = x["feat"].get("gap", gap)
        if fresh:
            st["i"] += 1
            sc = "dog" if st["i"] % 4 == 0 else scares[st["i"] % 3]
            a["watch"] = {g: sc for g in ([gap] if gap is not None else range(3))}
        if in_windows(d, SEED):
            a["children_scare"] = d % 2 == 0
            a["scarecrow"] = d % 2 == 1
        if has(v, "eels") and in_windows(d, RUN):
            a["eel_traps"] = True
            rain_after = obs.has(d, "sky.rain_after_dry") or obs.has(d, "sky.heavy_rain")
            dark = obs.has(d, "sky.moon_dark")
            a["weir_crew"] = bool(rain_after and dark) or bool(obs.has(d - 1, "sky.rain_after_dry") and dark)
        if has(v, "wildfowl"):
            if obs.has(d, "fowl.plovers"):
                a["set_nets"] = True
            if v.drv.frozen[d - 1] if d else False:
                a["set_nets"] = True
                fl = v.kinds["wildfowl"]
                a["fowl"] = fl.taken < 0.2 * fl.size
        return a
    return pol
