"""The wild kinds as data (wild_layer.md §3.2, D2-199): one row each, registered in the engine's RESOURCES with `"pack": "wild"` and
`"renewal": "population"` (one registry, as 37.4 asked in living_populations.md's review). The population fields are the food web's
(02zp part two, W2, §11 there): biology, not fitted numbers.

  mass kg; cls herb, gran, omni or carn (intake by Kleiber); b young a head a year in good condition; m deaths a year in good
  condition; hab weights over an area's features; diet {food or kind: preference}; breed seasons; terr a territorial ceiling a km2
  of full habitat; hibernate; starve (how hard hunger kills); move (share that shifts a season toward better land); migrant
  (seasons present) and arrive (a km2 of habitat on arrival); people (a take a season where people are); vuln (share reachable by a
  predator); ref a real density a km2 of good habitat, to compare only, never to fit; shy (0 to 1) how much people's busy land
  (a village's own land, less its ring) lowers the kind's habitat: rats follow people (0), deer and boar keep away (0.8).

The foods (FOOD) and their calibration (SCALE) are the food web's final values (02zp_ecosystem_models/web/final.json): each food
calibrated once, for every kind that eats it.
"""
from __future__ import annotations

SEASONS = ("spring", "summer", "autumn", "winter")


def K(mass, cls, b, m, hab, diet, breed=("spring",), terr=None, hibernate=False, starve=1.0, move=0.1, limits=None, migrant=None,
      arrive=None, people=0.0, vuln=0.4, switch=None, d0=1.0, ref=None, wave=1, count="density", uses="", damage="", group=None,
      shy=0.8):
    return {"shy": shy, "mass": mass, "cls": cls, "b": b, "m": m, "hab": hab, "diet": diet, "breed": list(breed), "terr": terr,
            "hibernate": hibernate, "starve": starve, "move": move, "limits": limits or {}, "migrant": list(migrant) if migrant else None,
            "arrive": arrive, "people": people, "vuln": vuln, "switch": switch, "d0": d0, "ref": ref, "wave": wave, "count": count,
            "uses": uses, "damage": damage, "group": group}


# wave 1: the wood's edge, the river and the barn; wave 2: the fold and the hungry year (wild_systems.md §13)
KINDS = {
    "red deer": K(90, "herb", 0.4, 0.10, {"wood": 0.45, "shrub": 0.2, "open": 0.4, "heath": 0.4},
                  {"grass": 3, "heather": 2, "browse": 2, "mast": 1, "crops": 1, "aquatic": 0.3}, people=0.08, move=0.15, ref=8, wave=1,
                  count="whole", group={"size": [4, 15]}, uses="venison, hide, antler; the noble's beast", damage="crops, young trees"),
    "roe deer": K(22, "herb", 0.9, 0.20, {"wood": 0.6, "shrub": 0.6, "open": 0.2},
                  {"browse": 4, "fruit": 1.5, "roots": 0.5, "grass": 0.5, "crops": 0.5}, people=0.1, ref=15, wave=1,
                  uses="venison, hide", damage="young trees"),
    "wild boar": K(70, "omni", 1.6, 0.30, {"wood": 0.8, "shrub": 0.3, "wet": 0.3},
                   {"mast": 4, "roots": 2, "nuts": 1, "fruit": 1, "crops": 2, "inverts": 0.3, "seeds": 0.5, "carrion": 0.5},
                   people=0.15, ref=4, wave=1, count="whole", group={"size": [3, 14]}, uses="pork, fat, hide", damage="roots up crops"),
    "brown hare": K(3.5, "herb", 4.0, 0.9, {"grassy": 1.0, "farm": 0.4, "open": 0.2}, {"sward": 3, "seeds": 1, "crops": 2},
                    breed=("spring", "summer"), people=0.3, ref=25, wave=1, uses="meat; coursing", damage="young crops", shy=0.6),
    "woodpigeon": K(0.5, "gran", 3.0, 0.6, {"wood": 0.5, "farm": 0.5}, {"seeds": 2, "mast": 2, "crops": 3, "browse": 1}, people=0.2,
                    ref=50, wave=1, damage="seed and young corn", shy=0.5),
    "rats": K(0.25, "omni", 10.0, 2.0, {"farm": 1.0}, {"stores": 3, "crops": 2, "seeds": 1, "carrion": 1},
              breed=("spring", "summer", "autumn"), move=0.05, ref=100, wave=1, damage="stores", shy=0.0),
    "wildfowl": K(1.0, "gran", 0, 0, {"wet": 1.0, "water": 1.0}, {"aquatic": 4, "seeds": 1, "inverts": 1},
                  migrant=("autumn", "winter"), arrive=150, people=0.3, ref=150, wave=1, uses="meat, feathers, down", shy=0.9),
    "eel": K(0.5, "omni", 1.0, 0.3, {"water": 1.0, "wet": 0.8}, {"inverts": 1, "fish": 1, "aquatic": 1}, people=0.3, move=0.05,
             ref=150, wave=1, uses="food that keeps smoked; rent", shy=0.2),
    "voles and mice": K(0.025, "gran", 16.0, 2.5, {"open": 0.6, "wood": 0.4, "farm": 0.3},
                        {"seeds": 3, "grass": 2, "roots": 1, "inverts": 1, "crops": 1}, breed=("spring", "summer", "autumn"),
                        starve=1.5, move=0.2, ref=3000, wave=2, damage="crops, stores", shy=0.3),
    "owls": K(0.4, "carn", 2.0, 0.45, {"wood": 0.5, "farm": 0.5, "open": 0.2}, {"voles and mice": 5, "rats": 1}, terr=1.5, ref=1,
              wave=2, shy=0.3),
    "fox": K(6, "carn", 2.0, 0.6, {"open": 0.5, "wood": 0.5, "farm": 0.3},
             {"voles and mice": 3, "brown hare": 2, "wildfowl": 1, "livestock": 0.5, "carrion": 1, "fruit": 1, "inverts": 1}, terr=3,
             people=0.2, ref=2, wave=2, count="whole", group={"size": [1, 2]}, uses="pelt; a hunt", damage="hens, lambs", shy=0.5),
    "wolf": K(40, "carn", 1.5, 0.30, {"wood": 0.5, "open": 0.2, "heath": 0.3},
              {"red deer": 3, "roe deer": 2, "wild boar": 2, "brown hare": 0.5, "livestock": 1, "carrion": 1}, terr=0.03, people=0.05,
              move=0.25, ref=0.025, wave=2, count="whole", group={"size": [3, 8]}, uses="pelt; bounty", damage="herds; fear"),
    "raven": K(1.2, "omni", 1.0, 0.15, {"open": 0.5, "rock": 0.4, "wood": 0.2}, {"carrion": 4, "inverts": 1, "seeds": 1}, terr=0.3,
               ref=0.2, wave=2, uses="signs: circling over carrion", shy=0.6),
    "brown bear": K(250, "omni", 0.3, 0.05, {"wood": 0.7, "rock": 0.3, "old": 0.3},
                    {"fruit": 3, "nuts": 2, "mast": 2, "roots": 2, "inverts": 1, "carrion": 2, "fish": 1, "red deer": 0.3, "roe deer": 0.3,
                     "wild boar": 0.2, "livestock": 1}, hibernate=True, people=0.02, move=0.2, ref=0.02, wave=5, count="whole",
                    group={"size": [1, 1]}, uses="great pelt, fat; legend", damage="beasts, hives"),
}

# foods: "stock" grows logistically toward cap (kg a km2 of full cover); "pulse" is produced in its seasons and rots
FOOD = {
    "grass":   {"type": "stock", "cap": 60000, "grow": (0.45, 0.55, 0.30, 0.05), "q": 0.55},
    "sward":   {"type": "stock", "cap": 25000, "grow": (0.45, 0.50, 0.35, 0.08), "q": 0.75},
    "browse":  {"type": "stock", "cap": 30000, "grow": (0.40, 0.45, 0.15, 0.02), "q": 0.60},
    "heather": {"type": "stock", "cap": 80000, "grow": (0.20, 0.25, 0.15, 0.03), "q": 0.35},
    "aquatic": {"type": "stock", "cap": 60000, "grow": (0.40, 0.50, 0.25, 0.05), "q": 0.45},
    "roots":   {"type": "stock", "cap": 20000, "grow": (0.20, 0.20, 0.20, 0.05), "q": 0.60},
    "inverts": {"type": "stock", "cap": 8000,  "grow": (0.60, 0.70, 0.60, 0.10), "q": 0.85},
    "fish":    {"type": "stock", "cap": 40000, "grow": (0.20, 0.30, 0.25, 0.10), "q": 0.95},
    "mast":    {"type": "pulse", "prod": 50000, "season": (0, 0, 0.8, 0.2), "rot": 0.4, "q": 0.85},
    "nuts":    {"type": "pulse", "prod": 12000, "season": (0, 0, 0.8, 0.2), "rot": 0.3, "q": 0.90},
    "fruit":   {"type": "pulse", "prod": 20000, "season": (0, 0.4, 0.6, 0), "rot": 0.6, "q": 0.70},
    "seeds":   {"type": "pulse", "prod": 30000, "season": (0.05, 0.3, 0.5, 0.15), "rot": 0.3, "q": 0.85},
    "crops":   {"type": "pulse", "prod": 120000, "season": (0.1, 0.4, 0.45, 0.05), "rot": 0.5, "q": 0.80},
    "livestock": {"type": "pulse", "prod": 3000, "season": (0.35, 0.2, 0.2, 0.25), "rot": 0.9, "q": 1.0},
    "stores":  {"type": "pulse", "prod": 15000, "season": (0.2, 0.1, 0.3, 0.4), "rot": 0.5, "q": 0.85},
    "carrion": {"type": "carrion", "q": 0.9},
}
# Jarman-Bell: bulk plant stocks have a fine part (what small and medium animals select) and a coarse part (what only big guts use)
SPLIT = {"grass": (0.30, 0.80, 0.35), "browse": (0.30, 0.80, 0.35), "heather": (0.25, 0.65, 0.30), "aquatic": (0.30, 0.75, 0.30)}
for _f, (_share, _qf, _qc) in SPLIT.items():
    _base = FOOD.pop(_f)
    FOOD[_f] = dict(_base, cap=_base["cap"] * _share, q=_qf)
    FOOD[_f + "~coarse"] = dict(_base, cap=_base["cap"] * (1 - _share), q=_qc)
SCALE = {"grass": 0.2335, "sward": 0.0553, "browse": 0.4566, "heather": 0.2434, "mast": 0.0201, "nuts": 0.02, "seeds": 0.1726,
         "aquatic": 0.0468, "fish": 1.2136}                                  # the food web's calibration (02zp part two)
KLEIBER = {"herb": 0.075, "gran": 0.065, "omni": 0.07, "carn": 0.11}        # kg a day per kg^0.75 (carnivores: meat)
# the mast: the trees' rhythm (a budget that builds over 2 to 4 years) spoiled by frost at flowering; the year after a heavy mast
# fails (wild_systems.md §6); the scheduler's ecology era (D2-76) may set the odds
MAST = {"every": (2, 5), "ordinary_p": 0.6, "levels": {"heavy": 3.0, "ordinary": 1.0, "poor": 0.4, "fail": 0.15}}


# near people (wild_layer.md §3.4; wild_systems.md §6): how a whole-counted kind's group behaves by a village. The drive is a chance
# an engine day (about 11 real nights) of setting out toward a target in season: a sounder works ripening corn most such stretches. Seasons are
# {season index: (first day, last day)}; trample is the share of a field's standing crop a head takes in a raid; the answer to a
# harmless scare is D2-198's; leads are in engine days (D2-197). Traces name what a group leaves where, read by the senses with a
# reading for the practised hunter and one for anyone else.
NEAR_PEOPLE = {
    "wild boar": {
        "targets": [{"seasons": {1: (3, 7), 2: (0, 1)}, "attr": 1.0, "trample": 0.012},     # milk-ripe to harvest
                    {"seasons": {0: (0, 5)}, "attr": 0.3, "trample": 0.006}],              # the sown corn
        "drive": {"base": 0.35, "hunger": 0.5}, "memory_days": 3, "return_p": 0.85, "lead_nights": 2, "lead_sign_p": 0.9,
        "answer": {"type": "habituate", "turn_p": 0.9, "gain": 0.3, "decay": 0.01, "rest": 2},
        "harm": {"dog": {"turn_p": 0.95, "harm_p": 0.25}}, "wary_after_harm": 8, "met_share": 0.5,
        "traces": {"edge": {"lay": "the turf by the wood's edge turned over in long strips",
                            "knows": "fresh rooting at the wood's edge: a sounder of about {n}, nearer the corn each night",
                            "knows_old": "old rooting at the wood's edge, two or three nights old"},
                   "raid": {"lay": "the corn in {place} trampled and rooted in the night, a strip of it flattened",
                            "knows": "a sounder of about {n} was in the corn of {place} in the night: rooted and trampled"},
                   "turned": {"lay": "beasts turned back from {place} in the night", "knows": "the sounder turned back from {place}"}},
    },
    "red deer": {
        "targets": [{"seasons": {0: (2, 7)}, "attr": 0.5, "trample": 0.006},                # the young corn
                    {"seasons": {1: (3, 7)}, "attr": 0.4, "trample": 0.004}],              # the ripening corn
        "drive": {"base": 0.2, "hunger": 0.5}, "memory_days": 3, "return_p": 0.6, "lead_nights": 2, "lead_sign_p": 0.8,
        "answer": {"type": "habituate", "turn_p": 0.85, "gain": 0.25, "decay": 0.01, "rest": 2},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 5, "met_share": 0.5,
        "traces": {"edge": {"lay": "deer slots in the soft ground along the hedge",
                            "knows": "fresh slots along the hedge: a herd of about {n}, hinds and calves",
                            "knows_old": "old slots along the hedge, rained on"},
                   "raid": {"lay": "something grazed and trod the corn in {place} in the night",
                            "knows": "a herd of about {n} deer was at the corn in {place} in the night"},
                   "turned": {"lay": "beasts turned back from {place} in the night", "knows": "the deer turned back from {place}"}},
    },
    "wolf": {
        "gather": "far",                                                                     # a pack ranges far beyond one ring
        "targets": [{"what": "herd", "seasons": {3: (0, 7), 0: (0, 2)}, "attr": 1.0},          # late winter: hunger at the fold
                    {"what": "herd", "seasons": {0: (3, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35}],
        "drive": {"base": 0.03, "hunger": 0.9}, "memory_days": 4, "return_p": 0.7, "lead_nights": 2, "lead_sign_p": 0.7,
        "answer": {"type": "scared_off", "turn_p": 0.8, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 10, "met_share": 1.0,
        "traces": {"edge": {"lay": "great tracks along the wood's edge, like a big dog's",
                            "knows": "wolf tracks along the wood's edge, a pack of about {n}, and the beasts restless at dusk",
                            "knows_old": "old wolf tracks along the wood's edge"},
                   "raid": {"lay": "a beast of the herd on {place} killed and torn in the night",
                            "knows": "wolves took a beast of the herd on {place} in the night: a pack of about {n}"},
                   "turned": {"lay": "something drove at the herd on {place} in the night and was driven off",
                              "knows": "the watch drove wolves off the herd on {place}"}},
    },
    "fox": {
        "targets": [{"what": "hens", "seasons": {0: (2, 7), 1: (0, 3)}, "attr": 1.0},           # cubs to feed
                    {"what": "hens", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35}],
        "drive": {"base": 0.1, "hunger": 0.4}, "memory_days": 2, "return_p": 0.8, "lead_nights": 2, "lead_sign_p": 0.6,
        "answer": {"type": "scared_off", "turn_p": 0.85, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.1}}, "wary_after_harm": 10, "met_share": 1.0,
        "traces": {"edge": {"lay": "the blackbirds chinking at the hedge at dusk",
                            "knows": "a fox about the hedge at dusk: the blackbirds chinking at it, a musky smell on the path"},
                   "raid": {"lay": "feathers and blood by the hen house at {place}", "knows": "a fox was at the hens at {place} in the night"},
                   "turned": {"lay": "the dog barked at something by the hen house in the night",
                              "knows": "the dog drove a fox off the hens in the night"}},
    },
}

# what a kind's numbers near a village show (wild_layer.md §3.6): the highest row its density reaches, read two ways. `where`: the
# village's own land or the ring around; `per`: density a km2 (`count` for heads in the ring and the land beyond, for packs).
PRESENCE = {
    "voles and mice": [{"where": "ring", "min": 2400, "lay": "kestrels hanging in the wind over the grass, owls calling at night",
                        "knows": "the long grass is thick with voles: runways everywhere, kestrels over every field"},
                       {"where": "ring", "max": 900, "lay": "", "knows": "no owl calling these nights, and few runways in the grass: the voles are few"}],
    "owls": [{"where": "ring", "min": 1.2, "lay": "owls calling round the village at night", "knows": "owls calling all round at night: good hunting for them"}],
    "wolf": [{"where": "far", "count": 3, "lay": "howling far off in the night", "knows": "wolves howling from the woods at night: a pack ranging near"}],
    "wild boar": [{"where": "ring", "min": 1.0, "lay": "", "knows": "boar sign all through the wood: wallows, rubbed trees, rooted rides"}],
    "red deer": [{"where": "ring", "min": 0.5, "lay": "", "knows": "deer slots along the rides and hinds with calves in the clearings"}],
}
RAVENS_OVER = {"min_carrion": 20.0, "lay": "ravens wheeling over the wood", "knows": "ravens over the wood: something lies dead there, a kill or a carcass"}


# how a kind is taken (wild_layer.md §3.7; D2-192, D2-193): detect, the chance a searcher in good habitat comes on one; flee, the
# chance it gets away once found; danger to the taker found alone (a crew or a dog divides it); family, the words people look for it
# by; goods, what a kill gives (engine food for meat: real content x Y/365, node_ecology.md).
TAKEN = {
    "red deer":   {"family": ["deer", "red deer", "stag", "hind", "venison", "big game", "game"], "detect": 0.35, "flee": 0.55,
                   "goods": {"meat": 3.9, "hide": 1}},
    "roe deer":   {"family": ["deer", "roe", "roe deer", "venison", "game"], "detect": 0.3, "flee": 0.5, "goods": {"meat": 1.1, "hide": 1}},
    "wild boar":  {"family": ["boar", "wild boar", "pig", "swine", "sounder", "big game", "game"], "detect": 0.3, "flee": 0.35,
                   "danger": {"wound": 0.3, "kill": 0.03}, "goods": {"meat": 3.5, "hide": 1}},
    "brown hare": {"family": ["hare", "hares", "small game", "game"], "detect": 0.5, "flee": 0.5, "goods": {"meat": 0.18}},
    "woodpigeon": {"family": ["pigeon", "pigeons", "birds", "small game"], "detect": 0.4, "flee": 0.75, "goods": {"meat": 0.05}},
    "wildfowl":   {"family": ["fowl", "duck", "ducks", "geese", "birds", "wildfowl"], "detect": 0.5, "flee": 0.6, "goods": {"meat": 0.2}},
    "fox":        {"family": ["fox", "foxes", "vermin"], "detect": 0.15, "flee": 0.6, "goods": {"hide": 1}},
    "wolf":       {"family": ["wolf", "wolves", "big game"], "detect": 0.12, "flee": 0.5, "danger": {"wound": 0.25, "kill": 0.04},
                   "goods": {"hide": 1}},
    "brown bear": {"family": ["bear", "big game"], "detect": 0.1, "flee": 0.3, "danger": {"wound": 0.5, "kill": 0.12},
                   "goods": {"meat": 6.0, "hide": 2}},
}


# what a technique the wild pack switches off was practice for (the old generic hunt): those who knew it know these
SKILL_CARRY = {"hunt": ["hunt the wild", "snare hares"]}


def rows() -> dict:
    """The kinds as RESOURCES rows (merged into data.RESOURCES; pack "wild")."""
    return {name: {"renewal": "population", "pack": "wild", "population": k, **({"near_people": NEAR_PEOPLE[name]} if name in NEAR_PEOPLE else {}),
                   **({"taken": TAKEN[name]} if name in TAKEN else {}), **({"presence": PRESENCE[name]} if name in PRESENCE else {})}
            for name, k in KINDS.items()}
