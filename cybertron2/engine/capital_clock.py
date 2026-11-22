"""The building clock's experiment switch (W-82; D2-276, D2-281): capital works priced at their real hours x a factor.

Worktree only (branch w82-clock-bots, never merged). Set the environment variable C2_CAPITAL_FACTOR to a factor ("1/40", "1/15",
"1/7", or a number); unset, the engine's prices are untouched. data.py calls `apply` at the end of its import, so every module
that imports a table sees the new units (the tables are mutated in place).

The rule (proposals/building_clock.md; audit docs/review/37_growth/02zzzh_hunt_fish/building_clock.md, its section 1.1): a work's
units = real hours x factor / 2 (a unit is 2 hours, D2-275), with a floor of 1 unit (the audit's floor; issue 3). Real hours are the
middle of the audit's range for each row. Gear and tools (ITEMS, `make` techniques) are kept as they are. Materials are kept.
Upkeep that is a share of the build (a fence's mend, a weir's mend) moves with it; a house's repair (PHYSICS repair) is kept
(the audit: already about the rule's figure).

Departures named here (not in the audit's table):
  - the weir is priced at the large river's take (the audit: 150 to 500 real hours for a first section that takes 30% of a large
    run, mid 325), with today's internal ratios kept (an added wattle section 16/24 of a first, a timber one 25/24, a footing
    15/24), as the audit and the proposal say the weir must be sized to its take before it is repriced. At the research size
    (36 to 51 real hours) it would fall to the 1-unit floor at every factor;
  - clearing for building (CLEARING built) has no row: turf at the field-clearing row's real hours x 4/6 (today's ratio), scrub at
    scrub clearing's;
  - the camp is kept (1 unit either way).
"""
from __future__ import annotations

from fractions import Fraction

# real hours, the middle of the audit's range (section 1.1)
ROOM_HOURS = {("small room", "wattle"): 405, ("small room", "timber"): 585, ("small room", "stone"): 945,
              ("medium room", "timber"): 1035, ("medium room", "stone"): 1665,
              ("hall", "timber"): 5850, ("hall", "stone"): 8100}
FITTING_HOURS = {"beds": 6.5, "hearth": 13.5, "owl hole": 2.5, "bins": 13.5, "hand mill": 31.5, "granary": 36, "fire ring": 2.5,
                 "oven": 54, "anvil": 36, "cellar": 495, "millstones": 270, "water wheel": 3060, "stalls": 6.5, "woodshed": 27,
                 "smoke racks": 8, "brine pan": 27, "vault": 1350}
MONUMENT_HOURS = {"carved post": 31.5, "standing stone": 31.5, "cairn": 9}
WEIR_FIRST_HOURS = 325                    # a wattle first section at a large river's take (departure, above)
FENCE_HOURS = {"wood": 1080, "stone": 1275}            # round a field of size 1 (about 2 ha); x the square root of the size (fence_need)
CLEARING_HOURS = {"meadow": 72, "pasture": 72, "scrub": 630}   # a unit of size
WORKS_HOURS = {"ditch": 270, "terrace": 2700}          # a unit of size


def factor(x) -> float:
    return float(Fraction(str(x).strip()))


def units(hours, f) -> float:
    return round(max(1.0, float(hours) * f / 2.0), 2)


def apply(x) -> dict:
    """Reprice every capital row at real hours x factor; returns {row: (before, after)} for the record."""
    from cybertron2.engine import data as D
    f = factor(x)
    log = {}

    def put(name, d, key, new):
        log[name] = (d[key], new)
        d[key] = new

    for (room, st), h in ROOM_HOURS.items():
        put(f"room {room} {st}", D.ROOMS[room][st], "units", units(h, f))
    for room, bp in D.BLUEPRINTS.items():
        if room in D.ROOMS:
            put(f"blueprint {room}", bp, "units", D.ROOMS[room][bp["structure"]]["units"])
    for k, h in FITTING_HOURS.items():
        put(f"fitting {k}", D.FITTINGS[k], "units", units(h, f))
    for k, h in MONUMENT_HOURS.items():
        put(f"monument {k}", D.MONUMENTS[k], "units", units(h, f))
    W = D.WATER_WORKS["weir"]
    first = units(WEIR_FIRST_HOURS, f)
    k = first / float(D.MONUMENTS["weir"]["units"])        # today's 24 for a wattle first section (8 of its own + 16 the wattle)
    put("weir first section (wattle)", D.MONUMENTS["weir"], "units", first)
    put("weir position first (its own)", W["position"]["first"], "units", round(float(W["position"]["first"]["units"]) * k, 2))
    for m in ("wattle", "timber"):
        put(f"weir section {m}", W["material"][m], "units", round(float(W["material"][m]["units"]) * k, 2))
    put("weir footing", W["footing"], "units", round(float(W["footing"]["units"]) * k, 2))
    for kind, h in FENCE_HOURS.items():
        put(f"fence {kind} (a size-1 field)", D.FENCES[kind], "units", units(h, f))
    for cover, h in CLEARING_HOURS.items():
        put(f"clearing {cover}", D.CLEARING, cover, units(h, f))
    for cover in list(D.CLEARING["built"]):
        h = CLEARING_HOURS["scrub"] if cover == "scrub" else CLEARING_HOURS["meadow"] * 4.0 / 6.0
        put(f"clearing for building {cover}", D.CLEARING["built"], cover, units(h, f))
    for tech, h in WORKS_HOURS.items():
        put(f"works {tech}", D.TECHNIQUES[tech]["yield"], "units", units(h, f))
    for name, src in list(D.BLUEPRINTS.items()) + list(D.FITTINGS.items()) + list(D.MONUMENTS.items()):
        if D.TECHNIQUES.get(name, {}).get("verb") == "build":
            D.TECHNIQUES[name]["units"] = src["units"]        # the build techniques' shown units follow
    D.CAPITAL_CLOCK = {"factor": str(x), "rows": log}
    return log
