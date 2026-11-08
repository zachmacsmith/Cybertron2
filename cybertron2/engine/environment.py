"""The environment of a day (environment/scheduler.md "The day's weather", environment/visibility.md; D2-69, D2-99 to D2-103): the
day's weather drawn within its spell, snow lying, and how much each place lets the senses through. Nothing here is stored: every value
is computed from the seed, the spec and the state of the land (D2-103), so it repeats for the same seed and day.

Other systems read it: perception and noticing (visibility), decay (wet or dry, frozen, warm), fuse events (sound at night), roads
(a ford high after heavy rain).
"""
from __future__ import annotations

from cybertron2.engine.data import COVERS, ENV, SPELLS, TERRAIN, WEATHER

WET = tuple(k for k, v in WEATHER.items() if v["wet"])


def spell(w, day=None) -> str:
    """The spell a day falls in: from the world's spec (`spells`, days counted from 1), else the weather scheduler's (climate.py,
    D4-109) where the world has one, else normal."""
    day = w.d if day is None else day
    for sp in w.spec.get("spells") or []:
        if int(sp["from"]) - 1 <= day <= int(sp["to"]) - 1:
            return sp["kind"]
    from cybertron2.engine import climate as CL
    if CL.on(w):
        return CL.spell(w, day)
    return "normal"


def _fixed(w, day):
    return (w.spec.get("weather") or {}).get(day + 1) or (w.spec.get("weather") or {}).get(str(day + 1))


def scheduled(w, day=None) -> bool:
    """Whether a day's weather comes from the weather scheduler (climate.py, D4-109): the world has one, and neither a fixed day
    nor a hand-written spell overrides it."""
    from cybertron2.engine import climate as CL
    day = w.d if day is None else day
    return CL.on(w) and not _fixed(w, day) and not any(int(sp["from"]) - 1 <= day <= int(sp["to"]) - 1 for sp in w.spec.get("spells") or [])


def place(w, at):
    """Every weather query names its place (D4-111): a node or a road. There is no region-wide default; a caller with a place of its
    own (an agent's Here, a building, a container, a field, a traveller) passes it. Checked with the scheduler on or off."""
    if at in w.s["nodes"] or (isinstance(at, str) and at in (w.s.get("roads") or {})):
        return at
    raise ValueError(f"the weather is read at a place (a node or a road), not {at!r}")


def weather(w, at, day=None) -> str:
    """The day's weather at a place (keyed: weather, day). With the weather scheduler (climate.py, D4-109) it is the place's own;
    without, one draw for the region within the hand-written spell. A spec may fix a day's weather (`weather`: {day: kind}) for a
    scripted run. Rain falls as snow in winter and on cold days."""
    place(w, at)
    day = w.d if day is None else day
    fixed = _fixed(w, day)
    if fixed:
        return fixed
    from cybertron2.engine import climate as CL
    if scheduled(w, day):
        return CL.label(w, at, day)
    table = SPELLS[spell(w, day)]
    u = w.rng("weather", day).random()
    kind = next(iter(table))
    acc = 0.0
    for k, p in table.items():
        acc += p
        if u < acc:
            kind = k
            break
    if kind in ("rain", "heavy rain") and w.cold(at, day):
        kind = "snow"
    return kind


def values(w, at, day=None) -> dict | None:
    """The day's physical weather at a place (temp, low, rain, wind, fog, storm) where the scheduler gives it, else None."""
    from cybertron2.engine import climate as CL
    place(w, at)
    return CL.env(w, at, day) if scheduled(w, day) else None


def wet(w, at, day=None) -> bool:
    return weather(w, at, day) in WET


def snow_lying(w, at, day=None) -> bool:
    """Snow lies at a place after a snow day there until three days without frost there."""
    day = w.d if day is None else day
    thaw = 0
    for d in range(day, -1, -1):
        if weather(w, at, d) == "snow":
            return thaw < int(ENV["snow_melt"])
        if not w.cold(at, d):
            thaw += 1
            if thaw >= int(ENV["snow_melt"]):
                return False
    return False


def since_heavy_rain(w, at, day=None, horizon=10):
    """Days since the last heavy rain at a place, or None within the horizon (a ford is high for a while after: world/roads.md)."""
    day = w.d if day is None else day
    for d in range(day, max(-1, day - horizon), -1):
        if weather(w, at, d) == "heavy rain":
            return day - d
    return None


# ---------------------------------------------------------------------- visibility (computed per place and day: D2-103)
def _today_events(w, node):
    return [e for e in w.s.get("events", []) if e.get("place") == node and e.get("day", w.d) == w.d]


def _worked_techs(w, node, parcel) -> set:
    return {e.get("tech") for e in _today_events(w, node) if e.get("kind") == "work" and f"parcel:{parcel}" in (e.get("about") or [])}


def crop_high(w, parcel) -> bool:
    p = w.s["parcels"][parcel]
    from cybertron2.engine import farm as FM
    c = FM.main_crop(p)                                                        # the field's largest standing crop (D2-172)
    if not c or c.get("area_left", 0) <= 1e-6 or p["cover"] != "field":
        return False
    sown, ripe = int(c.get("sown", c.get("day", 0)) or 0), int(c.get("ripe_day", 0))
    return w.d >= sown + float(ENV["crop_high_from"]) * max(1, ripe - sown)


def smoky(w, node, parcel) -> bool:
    for e in _today_events(w, node):
        if f"parcel:{parcel}" not in (e.get("about") or []):
            continue
        if e.get("tech") in ENV["smoke_techs"] or set(e.get("tags") or []) & set(ENV["smoke_tags"]) or e.get("kind") == "fire":
            return True
    return False


def loudness(w, node, parcel=None) -> str:
    """'very', 'loud' or '' for what is making noise at a place today (D2-100)."""
    level = WEATHER[weather(w, node)].get("loud", "")
    for e in _today_events(w, node):
        if parcel and e.get("about") and f"parcel:{parcel}" not in e["about"] and e.get("kind") not in ENV["loud_kinds"]:
            continue
        x = ENV["loud_kinds"].get(e.get("kind")) or ENV["loud_techs"].get(e.get("tech")) or next(
            (ENV["loud_tags"][t] for t in e.get("tags") or [] if t in ENV["loud_tags"]), "")
        if x == "very":
            return "very"
        level = level or x
    return level


def visibility(w, node, parcel=None, sense="sight", night=False, moon=False, quiet=True, cover=None) -> float:
    """How much a place lets a sense through today (D2-99): the cover's base x the land's state x the day's weather (x night).
    `node` is the place (a node, or a road for one on it); `cover` names a cover or road terrain directly (roads); `quiet` applies
    masking to a quiet sound (D2-100)."""
    if sense not in ("sight", "sound"):
        return 1.0                                                          # smell: its own salience, no multipliers (D2-101)
    cov = cover or (w.s["parcels"][parcel]["cover"] if parcel else "built")
    base = float((COVERS.get(cov) or TERRAIN.get(cov) or {}).get(sense, 1.0))
    if sense == "sight" and parcel and not cover and felled(w, parcel):
        base = max(base, float(ENV["felled"]["sight"]))
    v = base * weather_lets(w, node, sense)
    if sense == "sight" and parcel and not cover:
        if crop_high(w, parcel):
            v *= float(ENV["crop_high"])
        if smoky(w, node, parcel):
            v *= float(ENV["smoke"])
    if night:
        v *= float(ENV["night"]["moon"] if moon else ENV["night"]["sight"]) if sense == "sight" else float(ENV["night"]["sound"])
    if sense == "sound" and quiet and node in w.s["nodes"]:
        m = loudness(w, node, parcel)
        if m:
            v *= float(ENV["mask"][m])
    return round(v, 4)


def weather_lets(w, at, sense="sight") -> float:
    """How much the day's weather at a place lets a sense through: from its values with the scheduler (rain by the mm, falling snow,
    fog; wind and rain masking sound: D4-111), else from the day's label."""
    from cybertron2.engine import climate as CL
    if sense not in ("sight", "sound"):
        return 1.0
    place(w, at)
    if scheduled(w):
        return CL.vis(w, at, sense)
    return float(WEATHER[weather(w, at)][sense])


def open_air(w, at, sense="sight", night=False) -> float:
    """What the day's weather (and the dark) let a sense through anywhere at a place (D4-75): for signs open to everyone there."""
    if sense not in ("sight", "sound"):
        return 1.0
    v = weather_lets(w, at, sense)
    if night:
        v *= float(ENV["night"]["sight"]) if sense == "sight" else float(ENV["night"]["sound"])
    return round(v, 4)


def felled(w, parcel) -> bool:
    """A wood cut down below a share of its timber is open ground: one sees through it (D2-92)."""
    wood = w.s["parcels"][parcel]["res"].get("wood")
    return bool(wood and wood["K"] > 0 and wood["S"] / wood["K"] < float(ENV["felled"]["below"]))


def ground_factor(w, at) -> float:
    """Things lying on the ground under snow at a place (D2-99)."""
    return float(ENV["snow_ground"]) if snow_lying(w, at) else 1.0


def words(w, at, day=None) -> str:
    wx = weather(w, at, day)
    return WEATHER[wx]["words"] + ("; snow lies on the ground" if wx != "snow" and snow_lying(w, at, day) else "")
