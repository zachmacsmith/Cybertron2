"""The wild kinds as data (wild_layer.md §3.2, D2-199): one row each, registered in the engine's RESOURCES with `"pack": "wild"` and
`"renewal": "population"` (one registry, as 37.4 asked in living_populations.md's review). The population fields are the food web's
(02zp part two, W2, §11 there): biology, not fitted numbers.

  mass kg; cls herb, gran, omni or carn (intake by Kleiber); b young a head a year in good condition; m deaths a year in good
  condition; hab weights over an area's features; diet {food or kind: preference}; breed seasons; terr a territorial ceiling a km2
  of full habitat; hibernate; starve (how hard hunger kills); move (share that shifts a season toward better land); migrant
  (seasons present) and arrive (a km2 of habitat on arrival); people (a take a season where people are); vuln (share reachable by a
  predator); ref a real density a km2 of good habitat, to compare only, never to fit.

The foods (FOOD) and their calibration (SCALE) are the food web's final values (02zp_ecosystem_models/web/final.json): each food
calibrated once, for every kind that eats it.
"""
from __future__ import annotations

SEASONS = ("spring", "summer", "autumn", "winter")


def K(mass, cls, b, m, hab, diet, breed=("spring",), terr=None, hibernate=False, starve=1.0, move=0.1, limits=None, migrant=None,
      arrive=None, people=0.0, vuln=0.4, switch=None, d0=1.0, ref=None, wave=1, count="density", uses="", damage="", group=None):
    return {"mass": mass, "cls": cls, "b": b, "m": m, "hab": hab, "diet": diet, "breed": list(breed), "terr": terr,
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
                    breed=("spring", "summer"), people=0.3, ref=25, wave=1, uses="meat; coursing", damage="young crops"),
    "woodpigeon": K(0.5, "gran", 3.0, 0.6, {"wood": 0.5, "farm": 0.5}, {"seeds": 2, "mast": 2, "crops": 3, "browse": 1}, people=0.2,
                    ref=50, wave=1, damage="seed and young corn"),
    "rats": K(0.25, "omni", 10.0, 2.0, {"farm": 1.0}, {"stores": 3, "crops": 2, "seeds": 1, "carrion": 1},
              breed=("spring", "summer", "autumn"), move=0.05, ref=100, wave=1, damage="stores"),
    "wildfowl": K(1.0, "gran", 0, 0, {"wet": 1.0, "water": 1.0}, {"aquatic": 4, "seeds": 1, "inverts": 1},
                  migrant=("autumn", "winter"), arrive=150, people=0.3, ref=150, wave=1, uses="meat, feathers, down"),
    "eel": K(0.5, "omni", 1.0, 0.3, {"water": 1.0, "wet": 0.8}, {"inverts": 1, "fish": 1, "aquatic": 1}, people=0.3, move=0.05,
             ref=150, wave=1, uses="food that keeps smoked; rent"),
    "voles and mice": K(0.025, "gran", 16.0, 2.5, {"open": 0.6, "wood": 0.4, "farm": 0.3},
                        {"seeds": 3, "grass": 2, "roots": 1, "inverts": 1, "crops": 1}, breed=("spring", "summer", "autumn"),
                        starve=1.5, move=0.2, ref=3000, wave=2, damage="crops, stores"),
    "owls": K(0.4, "carn", 2.0, 0.45, {"wood": 0.5, "farm": 0.5, "open": 0.2}, {"voles and mice": 5, "rats": 1}, terr=1.5, ref=1,
              wave=2),
    "fox": K(6, "carn", 2.0, 0.6, {"open": 0.5, "wood": 0.5, "farm": 0.3},
             {"voles and mice": 3, "brown hare": 2, "wildfowl": 1, "livestock": 0.5, "carrion": 1, "fruit": 1, "inverts": 1}, terr=3,
             people=0.2, ref=2, wave=2, count="whole", group={"size": [1, 2]}, uses="pelt; a hunt", damage="hens, lambs"),
    "wolf": K(40, "carn", 1.5, 0.30, {"wood": 0.5, "open": 0.2, "heath": 0.3},
              {"red deer": 3, "roe deer": 2, "wild boar": 2, "brown hare": 0.5, "livestock": 1, "carrion": 1}, terr=0.03, people=0.05,
              move=0.25, ref=0.025, wave=2, count="whole", group={"size": [3, 8]}, uses="pelt; bounty", damage="herds; fear"),
    "raven": K(1.2, "omni", 1.0, 0.15, {"open": 0.5, "rock": 0.4, "wood": 0.2}, {"carrion": 4, "inverts": 1, "seeds": 1}, terr=0.3,
               ref=0.2, wave=2, uses="signs: circling over carrion"),
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


def rows() -> dict:
    """The kinds as RESOURCES rows (merged into data.RESOURCES; pack "wild")."""
    return {name: {"renewal": "population", "pack": "wild", "population": k} for name, k in KINDS.items()}
