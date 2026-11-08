"""Node-first ecology (02zp part three): what the land does for and to a village, at the village's own scale.

The scaling principle (an assumption, and the year-length question 37.4 has put to Zach): an engine year of Y days stands for a real
year, so an engine day is 365/Y real days for the land and for people alike. One engine food is then 365/Y real person-days of food;
animals and harvests count in food at real content x Y/365; work returns (food per unit of work) keep their real ratios (a unit is a
sixth of an engine day). With Y = 32: a food is 11.4 real person-days; a hare 0.18 food; a roe 1.1; a red deer 3.9; a cow 12.

For each village of a generated world: its own parcels (cover, size), and its reservoir (the generator's land within 5 km, by
ecosystem) at real densities. Each element's year, in food and in units of work, against the village's need (people x Y food) and
its work (people x 6 units x Y), under household choices. An element is relevant if it moves the village's food or work by 10% or
more in some year or some choice.
"""
from __future__ import annotations

import numpy as np

Y = 32                       # days a year
FOOD_PD = 365.0 / Y          # real person-days in one engine food
UNIT_DAYS = (365.0 / Y) / 6  # real days of work in one unit
HA = 2.0                     # hectares in a unit of size


def to_food(pd):
    return pd / FOOD_PD


def ret(pd_per_work_day):
    """Food a unit of work, from a real return (person-days of food per day of work)."""
    return pd_per_work_day * UNIT_DAYS / FOOD_PD


# real yields (person-days of food a hectare of the parcel's cover a year, harvestable; approximate, 02zp §M4) and returns
PLANT = {   # name: (covers, pd/ha/yr, season shares (sp, su, au, wi), keeps, real return pd food per day of work)
    "hazel nuts": (("forest",), 20.0, (0, 0, 1, 0), True, 4.0),
    "brambles and hedge fruit": (("forest", "scrub", "pasture"), 6.0, (0, 0.4, 0.6, 0), False, 1.5),
    "fungi": (("forest", "pasture"), 2.0, (0, 0.1, 0.9, 0), False, 1.0),
    "roots": (("pasture", "meadow", "scrub"), 1.0, (0.4, 0.3, 0.3, 0), False, 0.6),
    "acorns (leached)": (("forest",), 15.0, (0, 0, 0.9, 0.1), True, 2.0),
}
ANIMAL = {  # name: real food per head (pd), density a km2 of its habitat (real), habitat covers, real return when present
    "hare": (2.0, 25.0, ("pasture", "field", "meadow"), 1.0),
    "roe deer": (12.0, 15.0, ("forest", "scrub"), 1.5),
    "red deer": (45.0, 8.0, ("forest", "heath", "moor"), 2.0),
    "wild boar": (40.0, 4.0, ("forest",), 2.0),
}
WATER = {"fish": (25.0, (0.2, 0.4, 0.3, 0.1), 1.0), "eels": (30.0, (0.1, 0.2, 0.7, 0.0), 2.0)}     # pd/ha of water a year


def village(world, nid):
    pars = world["nodes"][nid]["parcels"]
    area = {}
    for p in pars.values():
        area[p["cover"]] = area.get(p["cover"], 0.0) + p["size"] * HA
    return area


def budget(area, people, around, choices, rng, mast=1.0, hard=False):
    """A year's budget for one village. around: the reservoir {cover: km2} within 5 km. choices: what the households do.
    Returns {element: {"food": food a year, "work": units a year, "loss": food lost}} and the need and work available."""
    need = people * Y
    work = people * 6 * Y * 0.8                     # adults' units (children and elders work less)
    out = {}
    # plant food: what the village's own land gives, taken at the household's effort (gather in season or not)
    for n, (covers, pd, seas, keeps, R) in PLANT.items():
        ha = sum(area.get(c, 0.0) for c in covers)
        if n == "acorns (leached)" and not choices.get("leach"):
            continue
        avail = to_food(pd * ha * (mast if n in ("hazel nuts", "acorns (leached)") else 1.0))
        take = avail * choices.get("gather", 0.6)
        units = take / max(ret(R), 1e-9)
        out[n] = {"food": take, "work": units, "loss": 0.0, "season": seas, "keeps": keeps}
    # animals: residents on the village's own land plus visitors from around (the reservoir)
    for n, (pd, dens, covers, R) in ANIMAL.items():
        own_km2 = sum(area.get(c, 0.0) for c in covers) / 100.0
        res_km2 = sum(around.get(c, 0.0) for c in covers)
        resident = dens * own_km2
        visits = dens * res_km2 * 0.02 * choices.get("hunt_reach", 1.0)        # a share of the surrounding animals come within reach
        r = {"hare": 1.0, "roe deer": 0.4, "red deer": 0.25, "wild boar": 0.9}[n]
        sustain = (resident + visits) * r                                       # head a year the land and its surroundings can give
        effort = choices.get("hunt", 0.0)
        heads = sustain * min(1.0, effort) + resident * max(0.0, effort - 1.0) * 0.5   # beyond the sustainable: mining the residents
        if choices.get("rights") == "lord" and n in ("red deer", "roe deer", "wild boar"):
            heads *= 0.1                                                         # the forest is the lord's: poaching only
        food = to_food(heads * pd)
        out[n] = {"food": food, "work": food / max(ret(R), 1e-9), "loss": 0.0, "season": (0.2, 0.2, 0.35, 0.25), "keeps": False}
    # water
    wha = area.get("water", 0.0)
    for n, (pd, seas, R) in WATER.items():
        food = to_food(pd * wha) * choices.get("fish", 0.6)
        out[n] = {"food": food, "work": food / max(ret(R), 1e-9), "loss": 0.0, "season": seas, "keeps": n == "eels"}
    # damage: what the land takes from the village
    crop_food = to_food(area.get("field", 0.0) / HA * 64 * FOOD_PD / 1.0) if False else area.get("field", 0.0) / HA * 48.0   # engine net food a plot-year
    wood_edge = min(1.0, around.get("forest", 0.0) / 5.0)                      # how much wood lies near the fields (0 to 1)
    boar_raid = (0.03 + 0.25 * wood_edge * (1.0 if mast < 0.5 else 0.3)) * crop_food   # worst after a mast year, near big woods
    deer_graze = 0.04 * wood_edge * crop_food
    pigeons = 0.03 * crop_food
    watched = choices.get("watch", 0.0)                                         # nights watched in the ripening weeks
    out["boar in the crops"] = {"food": 0.0, "work": watched * 8 * 1.0, "loss": boar_raid * (1 - 0.8 * watched), "season": (0, 0.3, 0.7, 0), "keeps": False}
    out["deer in the crops"] = {"food": 0.0, "work": 0.0, "loss": deer_graze * (1 - 0.5 * choices.get("fence", 0.0)), "season": (0.4, 0.4, 0.2, 0), "keeps": False}
    out["pigeons and birds"] = {"food": 0.0, "work": choices.get("scare", 0.0) * 16, "loss": pigeons * (1 - 0.6 * choices.get("scare", 0.0)), "season": (0.5, 0.3, 0.2, 0), "keeps": False}
    stores = people * Y * 0.6                                                   # food in store over a year
    out["rats in the stores"] = {"food": 0.0, "work": 0.0, "loss": stores * (0.08 if not choices.get("cats") else 0.03), "season": (0.2, 0.2, 0.2, 0.4), "keeps": False}
    beasts_food = choices.get("beasts", 6) * 12.0                              # a cow is about 12 food at real content
    wolf = (0.3 if hard else 0.08) * min(1.0, around.get("forest", 0.0) / 20.0) * choices.get("wolves", 1.0)   # beasts a year
    out["wolves at the beasts"] = {"food": 0.0, "work": choices.get("fold", 0.0) * Y * 2, "loss": wolf * (1 - 0.8 * choices.get("fold", 0.0)) * 12.0, "season": (0.2, 0, 0.1, 0.7), "keeps": False}
    return out, need, work, crop_food, beasts_food
