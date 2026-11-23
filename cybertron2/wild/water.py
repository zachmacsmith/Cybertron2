"""The water's own stocks and states (u1_water.md; D2-264, D2-265, D2-316, D2-317): the shallows by water type, the ice, a run's reach
into the fen, the pinch where the edge meets a run, and the fen's and the thaw's wrecks. The feature unit of the water's stocks
(D2-244): its data and its pure functions are here; the night's steps that read them are in engine/wild.py (`_set_night`,
`_runs_night`) and engine/night.py (the shallows' renewal); the world's making calls `seed_shallows`.

- **The shallows** (u1 §2; D2-317): one stock per water and fen parcel (`res["shallows"]`), distinct from the body's resident fish:
  small fish, crayfish and yellow eels at the edge, K a unit of size by the parcel's water type (`SHALLOWS`), regrowing on the year
  clock by the season, nothing under ice. Every world with the water pack has them; no switch takes them away (D2-316). The edge
  (hands, a dip net) draws them.
- **Ice** (u1 §4; D2-265, the detail a default to revisit with the environment, L-161): `ice(w, pid)` is `open`, `edges` or `over` by
  the nights of hard frost in a row at the node and the water type (`ICE`); the first day after a freeze of two nights or more is the
  thaw, read as `edges`.
- **A run's reach** (u1 §6): a trap in a water parcel on the river meets the run in full; in a fen beside it half; anywhere else none.
- **The pinch** (u1 §5): the edge's share of a run passing: full below a shut weir or dam, 0.3 on a brook or a lowland river, 0.1 on a
  big river.
"""
from __future__ import annotations

# K a unit of size of each water type (u1 §2, from fishing_ladder's anchors; default, calibrate); a unit of size read as the
# generator's cell (basis §2, A7's default)
SHALLOWS = {"K": {"brook": 5.0, "pool": 4.0, "fen": 7.0, "river": 4.0, "big river": 2.0, "lake": 2.0},
            "r": {"spring": 0.06, "summer": 0.10, "autumn": 0.06, "winter": 0.01}}     # a night, on the year clock (D2-273)
# nights of hard frost in a row at which a water's edges are ice, and at which it is frozen over (u1 §4)
ICE = {"edges": {"brook": 1, "pool": 1, "fen": 1, "river": 1, "big river": 2, "lake": 1},
       "over": {"brook": 2, "pool": 2, "fen": 2, "river": 4, "big river": 5, "lake": 6}}
RUN_REACH = {"river": 1.0, "fen": 0.5}                 # a run's density where the gear stands: on the river, a fen beside it (u1 §6)
FEN_WRECK = {"spate": 0.02, "flood": 0.05}             # a trap in the fen torn away (u1 §6; est., calibrate)
THAW_WRECK = {"small": 0.1, "river": 0.3}              # a trap crushed or torn by the ice going out (u1 §4; est., calibrate)
PINCH = {"held": 1.0, "ford": 1.0, "brook": 0.3, "river": 0.3, "big river": 0.1}   # the edge's share of a run (u1 §5; calibrate)
SMALL = ("brook", "pool", "fen")


def _parcel(w, pid) -> dict:
    return (w.s["parcels"].get(pid) or {})


def _body(w, pid):
    from cybertron2.engine import waters as WA
    bid = WA.body_of(w, pid) or (_parcel(w, pid).get("land") or {}).get("water_body")
    if bid is None:
        return None, {}
    land = ((w.spec or {}).get("wild") or {}).get("land") or {}
    return bid, ((land.get("waters") or {}).get(bid) or (w.s.get("waters") or {}).get(bid) or {})


def _big_stretch(w, node) -> bool:
    from cybertron2.engine import wild as WL
    try:
        if not WL.on(w) or not (w.s.get("wild") or {}).get("land"):
            return False
        from cybertron2.wild import runs as RU
        return float(RU.net(WL.model(w)).big.get(f"v:{node}", 0.0)) > 0
    except Exception:
        return False


def water_type(w, pid) -> str | None:
    """A parcel's water type (u1 §2): brook, pool, river, big river, lake or fen; None for dry land. A hand-made world with no bodies
    falls back on the land's river ("brook", "river"), else a pool."""
    par = _parcel(w, pid)
    cover = par.get("cover")
    if cover == "fen":
        return "fen"
    if cover != "water":
        return None
    bid, b = _body(w, pid)
    kind = (b or {}).get("kind")
    if kind in ("brook", "pool", "lake"):
        return kind
    river = (par.get("land") or {}).get("river")
    if kind == "reach" or river == "river":
        big = float((b or {}).get("big_river_km") or 0.0) > 0 and _big_stretch(w, par.get("node"))
        return "big river" if big else "river"
    if river == "brook":
        return "brook"
    return "pool"


def shallows_K(w, pid) -> float:
    t = water_type(w, pid)
    if t is None:
        return 0.0
    return round(float(SHALLOWS["K"][t]) * max(1, int(_parcel(w, pid).get("size", 1))), 4)


def seed_shallows(w) -> int:
    """At a world's making (D2-316, D2-317): every water and fen parcel of a world with the water pack gets its shallows, full; no
    switch takes them away. A parcel whose spec gives `shallows` keeps its own. Returns the parcels seeded."""
    from cybertron2.engine import packs as PK
    if "water" not in PK.of(w):
        return 0
    n = 0
    for pid in sorted(w.s["parcels"]):
        par = w.s["parcels"][pid]
        if par.get("cover") not in ("water", "fen") or "shallows" in par["res"]:
            continue
        K = shallows_K(w, pid)
        if K <= 0:
            continue
        par["res"]["shallows"] = {"S": K, "K": K, "r": float(SHALLOWS["r"]["summer"]), "renewal": "shallows"}
        n += 1
    return n


def renew(res, season, iced) -> float:
    """The shallows' night (u1 §2): logistic toward K at the season's rate, with a stripped margin's refill from fish moving in; none
    on a night the parcel is iced. S' = S + r S (1 - S/K) + 0.01 K r / 0.10."""
    S, K = float(res["S"]), float(res["K"])
    if K <= 0 or iced:
        return round(S, 4)
    r = float(SHALLOWS["r"].get(season, 0.06))
    return round(min(K, S + r * S * (1.0 - S / K) + 0.01 * K * r / 0.10), 4)


# ---------------------------------------------------------------------------------------------------------------------- ice
def ice(w, pid, day=None) -> str:
    """The ice on a water or fen parcel (u1 §4): `open`, `edges` or `over`; the thaw's day reads `edges`. Dry land and a world without
    the wild layer's weather: `open`."""
    from cybertron2.engine import wild as WL
    t = water_type(w, pid)
    if t is None or not WL.on(w):
        return "open"
    node = _parcel(w, pid).get("node")
    day = w.d if day is None else day
    try:
        fr = WL.frozen_run(w, node, day, most=max(ICE["over"].values()) + 1)
    except Exception:
        return "open"
    if fr >= int(ICE["over"][t]):
        return "over"
    if fr >= int(ICE["edges"][t]):
        return "edges"
    if fr == 0 and day >= 1 and thawing(w, pid, day):
        return "edges"
    return "open"


def thawing(w, pid, day=None) -> bool:
    """The first day not frozen after a freeze of two nights or more: the ice going out (u1 §4)."""
    from cybertron2.engine import wild as WL
    node = _parcel(w, pid).get("node")
    day = w.d if day is None else day
    try:
        return day >= 1 and WL.frozen_run(w, node, day) == 0 and WL.frozen_run(w, node, day - 1) >= 2
    except Exception:
        return False


def froze_over(w, pid, day=None) -> bool:
    """The freeze before today's thaw had frozen this water over."""
    from cybertron2.engine import wild as WL
    t = water_type(w, pid)
    if t is None:
        return False
    node = _parcel(w, pid).get("node")
    day = w.d if day is None else day
    try:
        return WL.frozen_run(w, node, day - 1, most=max(ICE["over"].values()) + 1) >= int(ICE["over"][t])
    except Exception:
        return False


def iced(w, pid, day=None) -> bool:
    return ice(w, pid, day) != "open"


def thaw_wreck(w, pid) -> float:
    """A trap's chance of being crushed or torn at the thaw (u1 §4): in a small water that froze over 0.1, in a river 0.3."""
    t = water_type(w, pid)
    if t is None or not thawing(w, pid) or not froze_over(w, pid):
        return 0.0
    return float(THAW_WRECK["small" if t in SMALL else "river"])


# ---------------------------------------------------------------------------------------------------------------------- runs
def run_reach(w, pid) -> float:
    """A trap's share of a run's density where it stands (u1 §6): a water parcel on the river 1.0; a fen beside one 0.5; else 0."""
    from cybertron2.engine import wild as WL
    par = _parcel(w, pid)
    if par.get("cover") == "water":
        return float(RUN_REACH["river"]) if WL._river_parcel(w, pid) else 0.0
    if par.get("cover") == "fen":
        return float(RUN_REACH["fen"]) if any(WL._river_parcel(w, q) for q in par.get("adj") or []) else 0.0
    return 0.0


def fen_wreck(flow) -> float:
    return float(FEN_WRECK.get(flow, 0.0))


def pinch(w, pid) -> float:
    """The edge's share of a run passing a parcel (u1 §5): full below a shut weir or dam (the fish held, crowding the gap) or at a ford;
    0.3 on a brook or a lowland river; 0.1 on a big river."""
    from cybertron2.engine import wild as WL
    par = _parcel(w, pid)
    if (par.get("land") or {}).get("ford"):
        return float(PINCH["ford"])
    node = par.get("node")
    for _, b in WL.weirs(w, node):
        if WL.gap(b) == "shut" and b.get("parcel") == pid:
            return float(PINCH["held"])
    for _, b in WL.mills(w, node):
        if WL.gap(b) == "shut" and WL.mill_water(w, b) == pid:
            return float(PINCH["held"])
    t = water_type(w, pid)
    return float(PINCH.get(t or "river", PINCH["river"]))


def stretch_ice(w, node) -> str:
    """The ice where a village's runs pass: at its first river water parcel (u1 §4), else `open`."""
    from cybertron2.engine import wild as WL
    for pid in sorted(w.s["parcels"]):
        par = w.s["parcels"][pid]
        if par.get("node") == node and par.get("cover") == "water" and WL._river_parcel(w, pid):
            return ice(w, pid)
    return "open"
