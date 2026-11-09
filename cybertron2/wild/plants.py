"""Wild plant kinds (wild_plants.md §2 and §6a; D2-200): the food plants as stocks on parcels, each in its season, swinging between
years, placed on the land by conditions. Data and pure functions; the engine seeds them (engine/wild.py) and their renewal is the
`seasonal` rule (engine/renewal.py). The wild kinds and the people draw the same stocks (D2-202): `SHARED` maps the ecology's foods
to them.

Where each grows (§6a): a parcel's plant food (the generator's single `plants` capacity, its total) is split into layers by the
cover (canopy, shrub, ground), and each layer among the kinds that suit the parcel's conditions (its cover, its ecosystem, wetness,
fertility, the coast), the best-suited dominating (shares by suitability squared). A kind's capacity is its peak in season, scaled so
that a year's mean over all kinds keeps the parcel's total.
"""
from __future__ import annotations

SEASONS = ("spring", "summer", "autumn", "winter")

# the parcel's plant food in layers, by cover (shares of its total)
LAYERS = {
    "forest": {"canopy": 0.35, "shrub": 0.50, "ground": 0.50},           # the canopy's mast on top: it mostly feeds the beasts
    "scrub": {"shrub": 0.70, "ground": 0.30},
    "meadow": {"shrub": 0.15, "ground": 0.85},
    "pasture": {"shrub": 0.20, "ground": 0.80},
    "heath": {"shrub": 0.70, "ground": 0.30},
    "moor": {"shrub": 0.70, "ground": 0.30},
    "fen": {"ground": 1.00},
    "saltmarsh": {"ground": 1.00},
}

# each kind: its layer; the good it gives; its seasons (share of its peak); how fast it comes (r a night toward its season's level)
# and goes after (rot); where it grows (covers, ecosystems as multipliers; needs: wet ground, the coast); its year (swing: a keyed
# draw, "mast" (the trees' mast), ("load", name) (a load's level) or "spring" (the spring's warmth)); ease (how much a unit of
# gathering gets of it); poison (the share of a take an untaught gatherer may come to harm by).
PLANTS = {
    "wild greens": {"layer": "ground", "item": "greens", "seasons": {"spring": 1.0, "summer": 0.5, "autumn": 0.3, "winter": 0.1},
                    "r": 0.4, "rot": 0.3, "covers": {"forest": 0.6, "scrub": 0.9, "meadow": 0.9, "pasture": 0.6, "fen": 0.7},
                    "eco": {"oak-ash wood": 1.3, "alder carr": 1.4, "wet grassland": 1.2}, "fertile": 1.0, "swing": ("draw", 0.15), "ease": 1.0,
                    "words": "nettles, sorrel and wild garlic"},
    "roots": {"layer": "ground", "item": "roots", "seasons": {"spring": 0.6, "summer": 0.6, "autumn": 0.8, "winter": 0.4},
              "r": 0.2, "rot": 0.1, "covers": {"pasture": 1.0, "meadow": 0.8, "heath": 0.5, "moor": 0.3, "fen": 0.6},
              "eco": {"wet grassland": 1.2}, "swing": ("draw", 0.1), "ease": 0.5, "words": "pignut and silverweed"},
    "mushrooms": {"layer": "ground", "item": "mushrooms", "seasons": {"summer": 0.2, "autumn": 1.0}, "r": 0.6, "rot": 0.5,
                  "covers": {"forest": 1.0, "pasture": 0.7, "meadow": 0.6, "scrub": 0.5}, "eco": {"beech wood": 1.3, "oak-ash wood": 1.0},
                  "swing": ("load", "fungi"), "ease": 1.0, "poison": 0.12, "words": "ceps, chanterelles and field mushrooms"},
    "watercress": {"layer": "ground", "item": "watercress", "seasons": {"spring": 0.8, "summer": 1.0, "autumn": 0.4}, "r": 0.4,
                   "rot": 0.3, "covers": {"meadow": 1.0, "fen": 1.0, "pasture": 0.6, "forest": 0.4}, "eco": {"alder carr": 1.5},
                   "needs": "wet", "swing": ("draw", 0.15), "ease": 1.0, "words": "watercress and brooklime"},
    "samphire": {"layer": "ground", "item": "samphire", "seasons": {"summer": 1.0, "autumn": 0.5}, "r": 0.4, "rot": 0.3,
                 "covers": {"saltmarsh": 1.0}, "needs": "coast", "swing": ("draw", 0.1), "ease": 1.0, "words": "samphire"},
    "berries": {"layer": "shrub", "item": "berries", "seasons": {"summer": 1.0, "autumn": 0.5}, "r": 0.4, "rot": 0.35,
                "covers": {"scrub": 1.0, "forest": 0.5, "heath": 0.8, "moor": 0.8, "pasture": 0.3, "meadow": 0.3},
                "swing": ("spring", 0.5), "ease": 1.0, "words": "brambles, bilberries and wild strawberries"},
    "hedge fruit": {"layer": "shrub", "item": "hedge fruit", "seasons": {"autumn": 1.0, "winter": 0.4}, "r": 0.4, "rot": 0.2,
                    "covers": {"scrub": 1.0, "pasture": 0.6, "meadow": 0.5, "forest": 0.3}, "swing": ("draw", 0.3), "ease": 1.0,
                    "words": "crab apples, sloes, haws and hips"},
    "hazel nuts": {"layer": "shrub", "item": "hazel nuts", "seasons": {"autumn": 1.0, "winter": 0.15}, "r": 0.5, "rot": 0.3,
                   "covers": {"forest": 1.0, "scrub": 0.6}, "eco": {"oak-ash wood": 1.3, "upland oak wood": 1.1, "beech wood": 0.3},
                   "coppice": 1.5, "swing": ("draw", 0.45), "ease": 0.8, "words": "hazel nuts"},
    "acorns": {"layer": "canopy", "item": "acorns", "seasons": {"autumn": 1.0, "winter": 0.2}, "r": 0.5, "rot": 0.25,
               "covers": {"forest": 1.0}, "eco": {"oak-ash wood": 1.0, "upland oak wood": 1.0, "beech wood": 0.1, "alder carr": 0.1,
                                                    "birch and pine wood": 0.1}, "swing": ("mast", 1.0), "ease": 1.0, "words": "acorns"},
    "beech mast": {"layer": "canopy", "item": "beech nuts", "seasons": {"autumn": 1.0, "winter": 0.2}, "r": 0.5, "rot": 0.25,
                   "covers": {"forest": 1.0}, "eco": {"beech wood": 1.0, "oak-ash wood": 0.05, "upland oak wood": 0.05,
                                                        "alder carr": 0.0, "birch and pine wood": 0.0}, "swing": ("mast", 1.0), "ease": 0.8,
                   "words": "beech nuts"},
}
# the ecology's foods that are these stocks on a village's own land (D2-202): what the wild kinds eat there is drawn from them, and
# what people take leaves less for the wild kinds; "young" and "grass" are the engine's own stocks (young growth; grazing)
SHARED = {"mast": ["acorns", "beech mast"], "nuts": ["hazel nuts"], "fruit": ["berries", "hedge fruit"], "roots": ["roots"],
          "browse": ["young"], "grass": ["grass"], "sward": ["grass"]}
SPRING_GDD = 350.0                     # degree days by the end of an ordinary spring (calibrate on the climate: loads_check)
WET_POSITIONS = {"hollow"}
WET_ECOS = {"alder carr", "hay meadow", "wet grassland", "fen", "reedbed", "blanket bog"}


def mean_season(kind: str) -> float:
    return sum(PLANTS[kind]["seasons"].get(s, 0.0) for s in SEASONS) / 4.0


def suit(kind: str, par: dict) -> float:
    """How well a kind grows on a parcel (0 to about 2): its cover, its ecosystem, what it needs (wet ground, the coast), fertility."""
    k = PLANTS[kind]
    s = float(k["covers"].get(par.get("cover"), 0.0))
    if s <= 0:
        return 0.0
    eco = par.get("ecosystem")
    if eco in (k.get("eco") or {}):
        s *= float(k["eco"][eco])
    land = par.get("land") or {}
    wet = land.get("position") in WET_POSITIONS or eco in WET_ECOS or (land.get("river") not in (None, "none")) \
        or float(land.get("held_mm", 0) or 0) >= 260
    if k.get("needs") == "wet" and not wet:
        return 0.0
    if k.get("needs") == "coast" and float(land.get("sea_km", 99) or 99) > 3.0:
        return 0.0
    if k.get("coppice") and ((par.get("res") or {}).get("wood") or {}).get("kind") == "managed wood":
        s *= float(k["coppice"])
    if k.get("fertile"):
        s *= max(0.3, float(par.get("fertility", 1.0) or 1.0)) ** float(k["fertile"])
    return s


def niche(par: dict, total: float, food=None) -> dict:
    """The parcel's plant kinds and their peak capacities (K), from its total plant food: layers by cover, kinds within a layer by
    suitability squared, each scaled by its seasons and by its good's food so a year's mean keeps the total as food (the canopy's mast
    on top); `food`: a good's food a unit (ITEMS)."""
    out = {}
    for layer, share in (LAYERS.get(par.get("cover")) or {}).items():
        s = {k: suit(k, par) for k, v in PLANTS.items() if v["layer"] == layer}
        s = {k: v for k, v in s.items() if v > 0}
        tot = sum(v * v for v in s.values())
        for k, v in s.items():
            fv = float((food or {}).get(PLANTS[k]["item"], 1.0)) if layer != "canopy" else 1.0
            K = total * share * (v * v / tot) / max(mean_season(k), 0.1) / max(fv, 0.3)
            if K > 1e-3:
                out[k] = round(K, 4)
    return out
