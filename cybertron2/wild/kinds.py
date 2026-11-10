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
    "woodpigeon": K(0.5, "gran", 3.0, 0.6, {"wood": 0.5, "farm": 0.5}, {"seeds": 2, "mast": 2, "crops": 1.5, "browse": 1}, people=0.2,   # crops 3 to 1.5: the flock takes the rest (brief 2 §3; calibrate)
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
    # the stoat (brief 2, pack K1): small enough for a wattle hen-house's gaps; voles its living, hens and eggs when it can
    "stoat": K(0.25, "carn", 3.0, 0.7, {"open": 0.4, "wood": 0.4, "farm": 0.3}, {"voles and mice": 4, "brown hare": 0.3, "livestock": 0.2,
               "inverts": 0.5}, terr=2, people=0.1, ref=4, wave=2, count="whole", group={"size": [1, 2]},
               uses="ermine in winter", damage="hens, eggs", shy=0.4),
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
                    {"what": "carcass", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.5, "stages": ["rotting"], "eat": 2.0},   # rooting at the dead (brief 3)
                    {"seasons": {0: (0, 5)}, "attr": 0.3, "trample": 0.006}],              # the sown corn
        "drive": {"base": 0.35, "hunger": 0.5}, "memory_days": 3, "return_p": 0.85, "lead_nights": 2, "lead_sign_p": 0.9,
        "answer": {"type": "habituate", "turn_p": 0.9, "gain": 0.3, "decay": 0.01, "rest": 2},
        "harm": {"dog": {"turn_p": 0.95, "harm_p": 0.25}}, "wary_after_harm": 8, "met_share": 0.5,
        "displace": True,                                                                # turned, the next field (D2-207)
    },
    "red deer": {
        "targets": [{"seasons": {0: (2, 7)}, "attr": 0.5, "trample": 0.006},                # the young corn
                    {"seasons": {1: (3, 7)}, "attr": 0.4, "trample": 0.004}],              # the ripening corn
        "drive": {"base": 0.2, "hunger": 0.5}, "memory_days": 3, "return_p": 0.6, "lead_nights": 2, "lead_sign_p": 0.8,
        "answer": {"type": "habituate", "turn_p": 0.85, "gain": 0.25, "decay": 0.01, "rest": 2},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 5, "met_share": 0.5, "fence": 2.0,   # deer leap fences
        "displace": True,
    },
    "wolf": {
        "gather": "far",                                                                     # a pack ranges far beyond one ring
        "targets": [{"what": "herd", "seasons": {3: (0, 7), 0: (0, 2)}, "attr": 1.0},          # late winter: hunger at the fold
                    {"what": "carcass", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 1.0, "stages": ["fresh", "rotting"], "eat": 3.0, "digs": True},
                    {"what": "herd", "seasons": {0: (3, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35}],
        "drive": {"base": 0.03, "hunger": 0.9}, "memory_days": 4, "return_p": 0.7, "lead_nights": 2, "lead_sign_p": 0.7,
        "answer": {"type": "scared_off", "turn_p": 0.8, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 10, "met_share": 1.0,
    },
    "brown bear": {
        "gather": "far", "targets": [{"what": "carcass", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 1.0, "stages": ["fresh"], "eat": 8.0, "cache": [2, 4]}],                                                    # only in a hungry spring (WHEN)
        "drive": {"base": 0.05, "hunger": 0.5}, "memory_days": 2, "return_p": 0.6, "lead_nights": 1, "lead_sign_p": 0.8,
        "answer": {"type": "scared_off", "turn_p": 0.7, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.8, "harm_p": 0.05}}, "wary_after_harm": 10, "met_share": 1.0,
    },
    # a flock of woodpigeons at the corn (brief 2 §3): counted by density, raiding as a flock; a still scare is soon a post
    "woodpigeon": {
        "flock": [20, 120],
        "targets": [{"seasons": {0: (0, 7)}, "attr": 0.6, "trample": 0.0004, "pick": "most"},     # the sowing and the young corn
                    {"seasons": {2: (0, 7)}, "attr": 0.3, "trample": 0.0003, "pick": "most"}],    # the autumn sowing
        "drive": {"base": 0.4, "hunger": 0.5}, "memory_days": 3, "return_p": 0.9, "lead_nights": 1, "lead_sign_p": 0.5,
        "answer": {"type": "habituate", "turn_p": 0.9, "gain": 0.35, "decay": 0.05, "rest": 1},
        "harm": {"dog": {"turn_p": 0.8, "harm_p": 0.0}}, "wary_after_harm": 2, "met_share": 0.5, "fence": 9.0,   # over any fence
        "displace": True,
    },
    "stoat": {
        "targets": [{"what": "items", "items": ["hen"], "door": True, "heads": 1, "all_p": 0.15, "attr": 0.6, "probe": 3,
                     "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}}],
        "drive": {"base": 0.08, "hunger": 0.4}, "memory_days": 2, "return_p": 0.7, "lead_nights": 1, "lead_sign_p": 0.3,
        "answer": {"type": "scared_off", "turn_p": 0.7, "off_days": 2},
        "harm": {"dog": {"turn_p": 0.8, "harm_p": 0.2}}, "wary_after_harm": 6, "met_share": 1.0,
    },
    "fox": {
        "targets": [{"what": "items", "items": ["hen"], "door": True, "heads": 2, "all_p": 0.3, "seasons": {0: (2, 7), 1: (0, 3)},
                     "attr": 1.0, "probe": 3},                                                    # cubs to feed; tries the doors (D2-207)
                    {"what": "items", "items": ["hen"], "door": True, "heads": 2, "all_p": 0.3,
                     "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35, "probe": 3},
                    {"what": "carcass", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.8,     # the dead (brief 3)
                     "stages": ["fresh", "rotting"], "eat": 0.6, "digs": True}],
        "drive": {"base": 0.1, "hunger": 0.4}, "memory_days": 2, "return_p": 0.8, "lead_nights": 2, "lead_sign_p": 0.6,
        "answer": {"type": "scared_off", "turn_p": 0.85, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.1}}, "wary_after_harm": 10, "met_share": 1.0,
    },
}

# the signs of what wild groups do (wild_layer.md §3.5-3.6; guides/senses.md): a bundle for each thing a group leaves, by the four
# kinds of sense (to the doer, nearby as it happens, lingering, conditional). Each row: read ("lay": one who has not practised
# hunting, "knows": one who has, "all": anyone), sense, own (how plain: the one noticing rule gives the chance), ages (days since,
# inclusive), cond ("snow", "night": sensed in the dark as it happens), who ("watcher": only the one who watched), knack, text ({n}
# heads, {place}, {scare}).
R = lambda read, sense, own, ages, text, cond=None, who=None, knack=None: {k: v for k, v in dict(read=read, sense=sense, own=own,
                                                                         ages=list(ages), text=text, cond=cond, who=who, knack=knack).items() if v is not None}
SIGNS = {
    "wild boar": {
        "edge": [R("lay", "sight", 0.7, (1, 3), "the turf by the wood's edge turned over in long strips"),
                 R("knows", "sight", 0.85, (1, 1), "fresh rooting at the wood's edge: a sounder of about {n}, nearer the corn each night"),
                 R("knows", "sight", 0.7, (2, 3), "old rooting at the wood's edge, two or three nights old"),
                 R("all", "sound", 1.2, (0, 0), "grunting and the crack of undergrowth at the wood's edge in the night", cond="night"),
                 R("all", "sight", 1.3, (1, 2), "the snow at the wood's edge ploughed up and full of deep slots", cond="snow")],
        "raid": [R("lay", "sight", 0.95, (1, 2), "the corn in {place} trampled and rooted in the night, a strip of it flattened"),
                 R("knows", "sight", 0.95, (1, 2), "a sounder of about {n} was in the corn of {place} in the night: rooted and trampled"),
                 R("all", "sound", 1.6, (0, 0), "a crashing and squealing in {place} in the night", cond="night"),
                 R("all", "smell", 1.0, (1, 1), "a rank pig-smell over the trampled corn in {place}")],
        "turned": [R("all", "sight", 0.6, (1, 1), "the ground churned at the edge of {place} where beasts turned back in the night"),
                   R("all", "sight", 2.0, (0, 0), "near midnight something heavy came crashing to the edge of {place} and broke away from the {scare}", who="watcher")],
    },
    "red deer": {
        "edge": [R("lay", "sight", 0.6, (1, 3), "deer slots in the soft ground along the hedge"),
                 R("knows", "sight", 0.8, (1, 1), "fresh slots along the hedge: a herd of about {n}, hinds and calves"),
                 R("knows", "sight", 0.6, (2, 3), "old slots along the hedge, rained on"),
                 R("all", "sound", 0.6, (0, 0), "hooves on the ride and a stag's cough in the dark", cond="night"),
                 R("all", "sight", 1.3, (1, 2), "a line of slots plain in the snow along the hedge", cond="snow")],
        "raid": [R("lay", "sight", 0.85, (1, 2), "something grazed and trod the corn in {place} in the night"),
                 R("knows", "sight", 0.9, (1, 2), "a herd of about {n} deer was at the corn in {place} in the night: tops bitten, slots between the rows")],
        "turned": [R("all", "sight", 2.0, (0, 0), "in the dark a herd of deer came to the edge of {place}; at the {scare} they wheeled and were gone", who="watcher")],
    },
    "wolf": {
        "edge": [R("lay", "sight", 0.6, (1, 3), "great tracks along the wood's edge, like a big dog's"),
                 R("knows", "sight", 0.8, (1, 2), "wolf tracks along the wood's edge, a pack of about {n}"),
                 R("all", "sound", 2.5, (0, 0), "howling in the night from the woods, nearer than before", cond="night"),
                 R("all", "sight", 0.6, (1, 1), "the cattle bunched and restless at dusk, heads up to the wood", knack="herd"),
                 R("all", "sight", 1.4, (1, 2), "a line of great tracks in the snow along the wood's edge, straight as a string", cond="snow")],
        "raid": [R("all", "sound", 2.2, (0, 0), "a beast bellowing in terror in the night, out on {place}, then silence", cond="night"),
                 R("lay", "sight", 0.95, (1, 2), "a beast of the herd on {place} killed and torn in the night"),
                 R("knows", "sight", 0.95, (1, 2), "wolves took a beast of the herd on {place} in the night: a pack of about {n}, by the tracks"),
                 R("all", "sight", 1.4, (1, 2), "blood and great tracks trodden into the snow of {place}", cond="snow")],
        "tried": [R("all", "sight", 0.6, (1, 1), "the herd on {place} scattered and bunched in the night, the ground cut up by hooves")],
        "turned": [R("all", "sight", 0.6, (1, 1), "the herd on {place} scattered and bunched in the night, the ground cut up by hooves"),
                   R("all", "sight", 2.0, (0, 0), "in the dark you saw eyes beyond the herd on {place}; the {scare} held them off", who="watcher")],
    },
    "fox": {
        "edge": [R("lay", "sound", 0.6, (1, 1), "the blackbirds chinking at the hedge at dusk"),
                 R("knows", "sound", 0.7, (1, 1), "a fox about the hedge at dusk: the blackbirds chinking at it"),
                 R("knows", "smell", 0.6, (1, 2), "a musky fox-smell along the path to the houses")],
        "raid": [R("all", "sound", 1.6, (0, 0), "the hens shrieking in the night at {place}", cond="night"),
                 R("lay", "sight", 0.95, (1, 2), "feathers and blood by the hen house at {place}"),
                 R("knows", "sight", 0.95, (1, 2), "a fox was at the hens at {place} in the night: feathers, and one dragged off"),
                 R("all", "sight", 1.3, (1, 1), "small neat tracks in the snow to the hen-house door at {place}", cond="snow")],
        "turned": [R("all", "sound", 1.5, (0, 0), "the dog barking hard at something by the hen house in the night", cond="night")],
        "tried": [R("all", "sound", 1.2, (0, 0), "the hens clucking in alarm at {place} in the night", cond="night"),
                  R("lay", "sight", 0.8, (1, 1), "the earth scraped away under the hen-house door at {place}"),
                  R("knows", "sight", 0.8, (1, 1), "a fox dug at the hen-house door at {place} in the night and did not get in")],
    },
}
# how one who has hunted reads a beast a wild kind killed (signs.CARCASS)
KILL_READINGS = {"wolf": "wolves killed the {beast} {at}: the throat bitten through from behind, great tracks trodden all round",
                 "fox": "a fox's kill {at}: the head bitten off, the rest dragged",
                 "brown bear": "a bear killed the {beast} {at}: the neck broken by one blow, the carcass half dragged toward the wood"}
EXPERT_KILL = {"wolf": "by the tracks a pack of four or five; they will be back to this herd within days unless it is watched or brought in",
               "brown bear": "a bear will come back to its kill; it is lying up near, and the carcass is best left or burned",
               "murrain": "the murrain: the beasts that live through it will not take it again; burn this one and keep the rest from it",
               "swine fever": "swine fever: the carcass keeps it; burn it, and keep the pigs from the wood"}
# ---------------------------------------------------------------------- the conditional layers (wild_systems.md §6, L0-L3; 02zq)
# Conditions (engine/wild.cond): seasons {si: (first day, last)}; frozen_run n (engine days frozen in a row); snow; mast [levels]
# (this autumn's; mast_last: last autumn's); hungry x (1 - condition in the ring); pressure x (hunting on the ring); hard_winter n
# (frozen days last winter); rain_after_dry; tomorrow {frozen | rain}; wet; not {...}. Effects while true: drive (x), bold (scares
# turn them that much less), danger and flee and detect (x, in a hunt), lone (a group of one may form), targets (more to raid,
# each a target row), and rows (the signs of it, shown the day it starts: the change).
AUT_WIN = {2: (0, 7), 3: (0, 7)}
DRY = "dry"                                                                                   # the engine's dry stores
WHEN = {
    "wild boar": [
        {"if": {"frozen_run": 1}, "drive": 1.6, "targets": [{"what": "items", "items": DRY, "door": True, "share": 0.004, "attr": 0.8,
                                                              "sign": "stores", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}}],
         "rows": [R("knows", "sight", 0.7, (0, 0), "the ground frozen hard: the boar can't root, and will come to the clamps and the stores")]},
        {"if": {"mast": ["fail", "poor"], "seasons": AUT_WIN}, "drive": 2.0,
         "targets": [{"what": "items", "items": DRY, "door": True, "share": 0.004, "attr": 0.7, "sign": "stores", "seasons": AUT_WIN},
                     {"what": "crop", "seasons": AUT_WIN, "attr": 0.8, "trample": 0.01}]},
        {"if": {"mast": ["heavy"], "seasons": {2: (0, 7)}}, "drive": 0.3},
        {"name": "tracked in snow", "if": {"snow": True}, "detect": 1.5},                  # found by their tracks (brief 4 §2.7)
        {"if": {"pressure": 0.5}, "drive": 0.3},
        {"name": "rut", "if": {"seasons": {2: (5, 7), 3: (0, 3)}}, "danger": 1.5,
         "rows": [R("knows", "sound", 0.6, (0, 0), "boars come in to the sounders now, fighting in the wood: dangerous to meet")]},
        {"name": "farrowing", "if": {"seasons": {0: (0, 5)}}, "danger": 1.5,
         "rows": [R("all", "sight", 0.6, (0, 0), "striped piglets trotting after a sow at the wood's edge"),
                  R("knows", "sight", 0.6, (0, 0), "the sows have farrowed: a sow with young will charge; more boar by the autumn")]},
    ],
    "woodpigeon": [
        {"if": {"mast": ["fail", "poor"], "seasons": AUT_WIN}, "drive": 1.5,
         "targets": [{"what": "crop", "seasons": AUT_WIN, "attr": 0.6, "trample": 0.0004, "pick": "most"}]},   # greens, winter corn
    ],
    "red deer": [
        {"if": {"snow": True}, "drive": 2.0, "targets": [{"what": "items", "items": ["hay"], "door": False, "share": 0.01, "attr": 1.0,
                                                          "sign": "hay", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}},
                                                         {"what": "res", "res": "young", "covers": ["forest", "scrub"], "share": 0.003,
                                                          "attr": 0.6, "sign": "bark", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}}],
         "rows": [R("knows", "sight", 0.7, (0, 0), "the first lying snow: the deer will be down at the ricks and the young trees")]},
        {"if": {"frozen_run": 2}, "drive": 1.5, "targets": [{"what": "res", "res": "young", "covers": ["forest", "scrub"], "share": 0.003,
                                                             "attr": 0.6, "sign": "bark", "seasons": {3: (0, 7), 0: (0, 2)}}]},
        {"if": {"pressure": 0.4}, "drive": 0.2},
        {"name": "rut", "if": {"seasons": {2: (0, 5)}}, "bold": 0.4, "detect": 1.5, "danger": 1.3,
         "rows": [R("all", "sound", 1.5, (0, 0), "stags roaring in the woods at dusk and through the night"),
                  R("knows", "sound", 0.8, (0, 0), "the rut is on: the stags are bold and careless, easier to come on, and a stag at bay is dangerous")]},
        {"name": "tracked in snow", "if": {"snow": True}, "detect": 1.5},                  # brief 4 §2.7 (calibrate)
        {"name": "summer leaf", "if": {"seasons": {1: (0, 7)}}, "detect": 0.8},             # lost in the full leaf
        {"name": "calving", "if": {"seasons": {1: (0, 3)}},
         "rows": [R("knows", "sight", 0.5, (0, 0), "hinds with new calves in the clearings")]},
        {"name": "antlers cast", "if": {"seasons": {0: (0, 3)}},
         "rows": [R("expert", "sight", 0.5, (0, 0), "the stags are casting their antlers: a cast antler in the wood is worth finding")]},
    ],
    "roe deer": [
        {"if": {"pressure": 0.4}, "drive": 0.2},
        {"name": "tracked in snow", "if": {"snow": True}, "detect": 1.5},                  # brief 4 §2.7 (calibrate)
        {"name": "summer leaf", "if": {"seasons": {1: (0, 7)}}, "detect": 0.8},
        {"name": "rut", "if": {"seasons": {1: (3, 7)}},
         "rows": [R("all", "sound", 0.8, (0, 0), "a roe barking hoarsely in the dusk"),
                  R("knows", "sight", 0.6, (0, 0), "roe rings trodden round the bushes in the meadow: the roe rut in summer, not autumn")]},
        {"name": "kids", "if": {"seasons": {0: (5, 7), 1: (0, 2)}},
         "rows": [R("expert", "sight", 0.5, (0, 0), "a roe doe hanging about the long grass: her kid lies hidden there, and the mower will find it")]},
    ],
    "wolf": [
        {"if": {"snow": True}, "bold": 0.4, "drive": 1.5},
        {"if": {"hungry": 0.5}, "bold": 0.3, "drive": 1.8},
        {"name": "dispersing", "if": {"seasons": {2: (4, 7), 3: (0, 7), 0: (0, 3)}}, "lone": True,
         "rows": [R("expert", "sight", 0.5, (0, 0), "the young wolves leave the packs now: a lone one crosses the farmland, and takes stock where none were taken")]},
        {"name": "howling", "if": {"seasons": {3: (0, 7)}},
         "rows": [R("all", "sound", 1.2, (0, 0), "wolves howling in the long nights, a chorus from the high wood")]},
        {"name": "pups", "if": {"seasons": {0: (2, 7)}},
         "rows": [R("expert", "sight", 0.4, (0, 0), "a worn path to a den under the roots in the high wood: the pack has pups, and will hunt hard all summer")]},
    ],
    "fox": [
        {"if": {"hungry": 0.5}, "drive": 1.6},
        {"name": "screaming", "if": {"seasons": {3: (2, 7)}},
         "rows": [R("all", "sound", 1.0, (0, 0), "a vixen screaming in the night, a sound like a woman's cry")]},
        {"name": "cubs", "if": {"seasons": {0: (0, 7)}}, "detect": 2.0, "flee": 0.3,                 # an earth is found by its signs
         "rows": [R("knows", "sight", 0.5, (0, 0), "an earth in the bank with fresh earth and feathers at its mouth: cubs"),
                  R("expert", "sight", 0.5, (0, 0), "a fox earth with cubs: dig it out now and there are fewer at the hens all year, more than any winter cull")]},
        {"name": "dispersing", "if": {"seasons": {2: (0, 7)}}, "lone": True},
    ],
    "brown bear": [
        {"name": "hungry spring", "if": {"seasons": {0: (2, 7)}, "hard_winter": 3, "mast_last": ["fail", "poor"]}, "drive": 1.0,
         "danger": 2.0, "targets": [{"what": "herd", "seasons": {0: (2, 7)}, "attr": 1.0}],
         "rows": [R("knows", "sight", 0.7, (0, 0), "great claw marks fresh on the beech by the ford, and stones rolled over"),
                  R("expert", "sight", 0.6, (0, 0), "a thin bear out of its den after a hard winter and a bare autumn: it will come for the calves")]},
    ],
    "wildfowl": [
        {"if": {"frozen_run": 2}, "flee": 0.5, "detect": 1.5,
         "rows": [R("all", "sight", 0.8, (0, 0), "the fowl crowded on the last open water, weak with the long frost"),
                  R("expert", "sight", 0.5, (0, 0), "birds so weak you could pick them up: take too many now and next winter's flocks are thin")]},
    ],
    "voles and mice": [
        {"if": {"mast": ["heavy"], "seasons": {3: (0, 7)}},
         "rows": [R("expert", "sight", 0.5, (0, 0), "mouse runs and gnawed nuts everywhere in the hedge bottoms after the mast: a mouse year coming")]},
    ],
}
# a group's target sort by what it raids, for the signs of a raid on it (kinds' SIGNS "raid:<sign>")
RAID_SIGNS = {
    "stores": {"wild boar": [R("all", "sound", 1.4, (0, 0), "a crashing and grunting at the store at {place} in the night", cond="night"),
                             R("all", "sight", 0.95, (1, 2), "the store at {place} broken into in the night: sacks torn, grain trampled into the mud")]},
    "hay": {"red deer": [R("all", "sight", 0.9, (1, 2), "the hay at {place} pulled out and trampled, deer slots all round it in the snow")]},
    "bark": {"red deer": [R("lay", "sight", 0.8, (1, 2), "the bark stripped from the young trees in {place}"),
                          R("knows", "sight", 0.8, (1, 2), "deer have stripped the young ash in {place}: the coppice regrowth will die back")]},
}
# the expert's readings (L3) of a group's traces, beyond the practised hunter's
EXPERT_SIGNS = {
    "wild boar": {"edge": [R("expert", "sight", 0.6, (1, 2), "the sounder's run comes out of {place} by one gap in the thorn: watch the gap and you meet them")],
                  "raid": [R("expert", "sight", 0.7, (1, 2), "the sounder will be back tonight, by the same gap: a new scare or a dog turns them; the same fire won't for long")],
                  "turned": [R("expert", "sight", 0.6, (1, 1), "turned once by the {scare}; they get used to the same scare in a few nights")]},
    "red deer": {"edge": [R("expert", "sight", 0.6, (1, 2), "the deer come through a rack broken in the hedge by {place}: hinds and calves by the slots, one big stag")],
                 "raid": [R("expert", "sight", 0.6, (1, 2), "they'll be back to the young corn while it's tender; hunting the wood by day keeps them off it")]},
    "wolf": {"edge": [R("lay", "sight", 0.5, (1, 2), "a big dog's tracks along the wood's edge"),
                      R("expert", "sight", 0.6, (1, 2), "wolf tracks, not a dog's: four toes in a straight line and the scat full of hair and bone")],
             "raid": [R("expert", "sight", 0.6, (1, 2), "the wolves will come back to the herd that fed them: watch it or bring it in")]},
    "fox": {"raid": [R("expert", "sight", 0.6, (1, 2), "a fox that found the hens will be back tomorrow night, to the same place")]},
}
# signs that lead the weather (the visible face of the climate's coming day; wild_systems.md §7: plovers before a freeze, swallows
# low before rain, the river rising dark after the dry weeks)
WEATHER_LEADS = [
    {"if": {"tomorrow": {"frozen": True}, "not": {"frozen_run": 1}, "seasons": {2: (4, 7), 3: (0, 7), 0: (0, 2)}},
     "rows": [R("all", "sight", 0.8, (0, 0), "lines of plovers going west all day, high and fast"),
              R("knows", "sight", 0.6, (0, 0), "plovers and redwings flying west ahead of hard weather: a freeze coming")], "read": "hunt"},
    {"if": {"tomorrow": {"rain": True}, "seasons": {1: (0, 7), 0: (4, 7)}},
     "rows": [R("all", "sight", 0.6, (0, 0), "the swallows flying low over the grass"),
              R("knows", "sight", 0.6, (0, 0), "the swallows low over the grass: the flies are down, and rain is coming")], "read": "sow"},
    {"if": {"rain_after_dry": 2, "seasons": {2: (0, 7)}}, "kind": "eel",
     "rows": [R("all", "sight", 0.6, (0, 0), "the first heavy rain after the dry weeks: the river rising and dark"),
              R("expert", "sight", 0.6, (0, 0), "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight")],
     "read": "trap in water"},
]
# what one notices while working, by the technique (the hunt's own are HUNT_NOTICES): each with the kind that must be about (in the
# village's ring), a condition, its rows, and a find (a good one may pick up)
WORK_NOTICES = {
    "hay": [{"kind": "roe deer", "if": {"seasons": {0: (5, 7), 1: (0, 3)}}, "find": None,
             "rows": [R("all", "sight", 0.6, (0, 0), "a roe kid lying flat in the long grass ahead of the scythe")]},
            {"kind": "voles and mice", "if": {}, "least": 2400, "rows": [R("all", "sight", 0.6, (0, 0), "voles running from the swathes as you mow")]}],
    "hunt": [{"kind": "red deer", "if": {"seasons": {0: (0, 4)}}, "find": {"item": "antler", "p": 0.15},
              "rows": [R("all", "sight", 0.5, (0, 0), "a cast antler lying in the leaves")]},
             {"kind": "fox", "if": {"seasons": {0: (0, 7)}}, "rows": [R("knows", "sight", 0.6, (0, 0), "a fox earth in the bank, fresh-dug, with feathers at its mouth")]},
             {"kind": "wild boar", "if": {"wounded": True}, "rows": [R("knows", "sight", 0.8, (0, 0), "a blood trail into the thicket"),
                                                                     R("expert", "sight", 0.8, (0, 0), "a wounded boar lying up in the thicket: the most dangerous beast in the wood; go in with others or not at all")]},
             {"kind": "wolf", "if": {}, "rows": [R("expert", "sight", 0.4, (0, 0), "ravens wheeling over the far wood: a kill there")]},
             {"kind": "voles and mice", "if": {}, "find": {"item": "cat", "p": 0.5},          # a stray to bring home (D2-206)
              "rows": [R("all", "sight", 0.08, (0, 0), "a lean half-wild cat hunting mice along the hedge; it came to your hand")]}],
    "gather wild food": [{"kind": None, "if": {"seasons": {1: (5, 7)}}, "mast_coming": True,
                          "rows": [R("expert", "sight", 0.5, (0, 0), "the acorns setting thick on the old oaks: a mast year this autumn")]},
                         {"kind": None, "if": {"seasons": {2: (0, 2)}}, "berries_heavy": True,
                          "rows": [R("all", "sight", 0.6, (0, 0), "the hedges red with haws and hips"),
                                   R("knows", "sight", 0.5, (0, 0), "berries thick on every hedge: a hard winter coming, they say")]},
                         {"kind": None, "if": {"seasons": {2: (0, 7)}}, "cover": ["pasture"],
                          "rows": [R("expert", "sight", 0.4, (0, 0), "a fairy ring of mushrooms on the pasture: old grass, never ploughed")]}],
}
# cyclers (wild_systems.md §5, rule 4): last year's crowding holds this year's breeding (a delayed density dependence), so numbers rise
# and crash over years; the strength by kind (calibrate: voles 3 to 4 years)
CYCLE = {"voles and mice": 0.0}     # off: tried 2 and 6 (9 Nov, 20 years): it lowers the level, does not cycle (cv 0.03-0.06; 02zq)
# a phase clock (02zp §23: the vole phase, a pulse shared by a world's villages, like the mast): a year in each phase, in order; a
# mast autumn sets it ahead (low to increase), a hard winter holds it (no step); each phase multiplies the kind's breeding and adds
# deaths a day (calibrate: peak to trough about tenfold, three to four years round)
PHASES = {"voles and mice": {"order": ["low", "increase", "peak", "crash"],
                             "breed": {"low": 0.4, "increase": 1.6, "peak": 1.0, "crash": 0.1},
                             "die": {"low": 0.08, "increase": 0.0, "peak": 0.04, "crash": 0.5},
                             "hard_winter": 3, "mast_ahead": True}}
# kinds that follow the harvest into the stores: how far a full barn can raise what they find there (engine/wild._follow_harvest)
FOLLOW_HARVEST = {"rats": 1.0, "voles and mice": 0.5}
# hunted kinds leaving a hunted area (a share a day for each unit of pressure); pressure added by a hunt, a kill, a crew; its fading
HUNTED = {"flee": {"red deer": 0.18, "roe deer": 0.12, "wild boar": 0.09}, "hunt": 0.25, "kill": 0.3, "crew": 0.5, "fade": 0.75}   # brief 4 §2.8
# the take as a search over time (brief 4 §2, calibrate): meetings a trip ~ Poisson(sum of density x detect x ... x ground x `meet`),
# at most `most`; a kill at `take_k` x skill x weapon x (1 - flee) x familiarity; the areas crossed on the way searched at `cross`;
# a method with no sweep of its own searches `sweep` km2 a unit; deer and boar keep off a village's own land (`home_shy`); game in
# the wild land, never hunted, is easier to come on (`wild_tame`)
HUNT = {"meet": 0.045, "wild_tame": 8.0, "take_k": 0.19, "cross": 0.2, "sweep": 0.5, "most": 8, "set_meet": 0.03,   # a set's night: Poisson, as before at low
        "home_shy": {"red deer": 0.3, "roe deer": 0.3, "wild boar": 0.3}}

# ---------------------------------------------------------------------- wave 5: sites, individuals, rare regimes (wild_layer.md §6 phase 9)
# Sites (wild_systems.md §5, colony and engineer): held on a parcel for generations, placed at world build where the land suits
# (a cover beside another, or on a river), seldom where it does not; a size (nests, a family) that grows toward its cap at the start
# of its season and crashes after a hard winter; `leaves`: worked or hunted on in its season it may go for good (D2-198); what it does
# to the village's land each night (eats a stock, harms a crop, floods and feeds through a dam); what may be taken from it, and when.
SPRING = {0: (0, 7)}
SITES = {
    "heronry": {"home": "colony", "where": {"covers": ["forest"], "beside": ["water"], "or_river": True}, "p": 0.6, "size": (6, 24), "cap": 24, "grow": 0.25,
                "season": SPRING, "leaves": 0.35, "hard_winter": {"frozen": 3, "crash": 0.5},
                "troubled_by": ["fell", "hunt the wild", "stalk", "drive", "gather young"],   # at the nests, not the quiet work (D2-204 names)
                "eats": {"res": "fish", "covers": ["water"], "share": 0.0004},
                "take": {"season": {0: (3, 7)}, "item": "meat", "each": 0.3, "most": 4, "words": "young herons from the nests"}},
    "rookery": {"home": "colony", "where": {"covers": ["forest", "scrub"], "beside": ["field"]}, "p": 0.8, "size": (20, 70), "cap": 80, "grow": 0.2,
                "season": SPRING, "leaves": 0.0, "hard_winter": {"frozen": 4, "crash": 0.2},
                "harm": {"crops": ["grain", "winter grain"], "age": (0, 6), "share": 0.00015, "beside": True, "watch_stops": True},
                "take": {"season": {0: (4, 7)}, "item": "meat", "each": 0.12, "most": 10, "words": "young rooks from the nests"}},
    "lodge": {"home": "lodge", "where": {"covers": ["forest", "scrub", "meadow"], "river": True}, "p": 0.15, "size": (2, 6), "cap": 6, "grow": 0.15,
              "season": {1: (0, 7)}, "leaves": 0.0, "rare": True,
              "dam": {"floods": {"covers": ["meadow", "pasture"], "res": "grass", "K": 0.6}, "fish": 1.3, "dead": 20.0, "rebuild_days": 3},
              "trap": {"item": "beaver pelt", "also": {"castoreum": 1}}},
}
SITE_SIGNS = {
    "heronry": {"back": [R("all", "sight", 0.9, (0, 0), "the herons are back at the tall trees in {place}, standing on their nests"),
                         R("expert", "sight", 0.6, (0, 0), "about {n} nests at the heronry in {place}, {change} than last year: {why}")],
                "gone": [R("all", "sight", 0.9, (0, 0), "the heronry in {place} stands empty this spring"),
                         R("knows", "sight", 0.6, (0, 0), "the herons have left {place}: they were troubled at the nests, and won't be back for years")],
                "here": [R("knows", "sight", 0.5, (0, 0), "grey herons standing in the shallows, a heronry near: a lord's feast in spring")]},
    "rookery": {"back": [R("all", "sound", 1.2, (0, 0), "the rooks building in the trees at {place}, cawing all day"),
                         R("expert", "sight", 0.5, (0, 0), "about {n} nests at the rookery in {place}: rooks mean grubs in the fields, and they pull the young corn")],
                "harm": [R("all", "sight", 0.8, (0, 1), "rooks pulling at the young corn in {place}, a black crowd of them")],
                "here": []},
    "lodge": {"back": [R("lay", "sight", 0.7, (0, 0), "trees cut to points by the water at {place}, chips all round them"),
                       R("knows", "sight", 0.7, (0, 0), "beaver: pencil-point stumps and a lodge of sticks on the brook at {place}"),
                       R("expert", "sight", 0.6, (0, 0), "a beaver family of about {n} at {place}: the pond holds fish and fowl, the dam floods the meadow; trap them and they're gone for good")],
              "dam": [R("all", "sight", 0.9, (0, 0), "the low meadow at {place} under water again behind a dam of sticks")],
              "broken": [R("all", "sight", 0.8, (0, 0), "the dam at {place} broken open, the water running out of the meadow")],
              "here": []},
}
# individuals (D2-195): a group's leader, named on demand when a group forms (`p`), with what it changes while it lives and when it
# dies; and the legendary beasts of a kind present in the world, seldom (`p` at world build), hard to find and dangerous
LEADERS = {"wild boar": {"name": "the old sow", "p": 0.6, "least": 5, "drive": 1.3, "return": 1.2, "kill_odds": 2.0,
                         "dead": {"drive": 0.4, "days": 16},
                         "rows": [R("expert", "sight", 0.6, (1, 2), "the old sow leads them, a torn ear and a great slot: she knows the gap and the fields")],
                         "dead_rows": [R("knows", "sight", 0.6, (0, 2), "the sounder without its old sow: they scatter and keep to the wood")]},
           "wolf": {"name": "the old dog-wolf", "p": 0.5, "least": 3, "drive": 1.2, "return": 1.2, "kill_odds": 1.5,
                    "dead": {"drive": 0.5, "days": 16},
                    "rows": [R("expert", "sight", 0.6, (1, 2), "the pack's leader is a big old dog-wolf: his track wider than the rest, and he takes the herds")],
                    "dead_rows": [R("knows", "sight", 0.6, (0, 2), "the pack has lost its old leader: they keep off now")]}}
LEGENDS = {"wild boar": {"name": "the great boar", "p": 0.15, "detect": 0.3, "flee": 1.3, "danger": 3.0, "goods": 2.0,
                         "rows": [R("expert", "sight", 0.5, (0, 0), "slots twice the size of any boar's in the deep wood: the great boar the old ones tell of")],
                         "tale": "the old ones tell of a great boar in the deep woods, that no hound will face"},
           "red deer": {"name": "the white hart", "p": 0.1, "detect": 0.3, "flee": 1.5, "danger": 1.0, "goods": 1.0,
                        "rows": [R("expert", "sight", 0.5, (0, 0), "a white hair caught on a thorn, and a great hart's slot: the white hart is real")],
                        "tale": "the old ones tell of a white hart in the far woods, and that ill luck follows its killer"},
           "wolf": {"name": "the great grey wolf", "p": 0.1, "detect": 0.4, "flee": 1.2, "danger": 2.5, "goods": 1.5,
                    "rows": [R("expert", "sight", 0.5, (0, 0), "a wolf's track as broad as a man's hand: the great grey wolf"),],
                    "tale": "the old ones tell of a great grey wolf that has taken beasts for twenty winters"},
           "brown bear": {"name": "the great bear", "p": 0.2, "detect": 0.4, "flee": 1.0, "danger": 2.0, "goods": 2.0,
                          "rows": [R("expert", "sight", 0.5, (0, 0), "claw marks higher than a man can reach: the great bear"),],
                          "tale": "the old ones tell of a great bear in the mountains that once came down to the village"}}
# rare regimes (L4): a condition held, its effects on the night (a share added to the stores' loss, a kill among a kind), and its
# signs, with the elders' memory of the last time (read by those of an elder's age)
REGIMES = {
    "great freeze": {"if": {"frozen_run": 4}, "kill": {"wildfowl": 0.15, "owls": 0.05}, "site_crash": {"heronry": 0.3},
                     "rows": [R("all", "sight", 1.2, (0, 0), "the river frozen from bank to bank; birds lying dead on the ice"),
                              R("elder", "sight", 0.9, (0, 0), "it was like this in the great freeze of your youth, when the fowl fell from the sky and the herons died")]},
    "vole plague": {"if": {}, "of": "voles and mice", "least": 6000, "stores": 1.0,
                    "rows": [R("all", "sight", 1.2, (0, 0), "voles everywhere: the stacks gnawed through and the grass clipped to the roots"),
                             R("elder", "sight", 0.9, (0, 0), "a vole plague, like the one the old ones remember: after it, owls and foxes everywhere, and then none")]},
    "bare years": {"if": {"mast": ["fail", "poor"], "mast_last": ["fail", "poor"], "seasons": {2: (0, 7), 3: (0, 7)}},
                   "rows": [R("all", "sight", 0.8, (0, 0), "a second bare autumn under the oaks; the boar thin and bold at the fields"),
                            R("elder", "sight", 0.9, (0, 0), "two bare years of mast: the old ones say in such years the boar came into the very houses")]},
}

# signs for a watch whatever the kind: the night passed quiet, or the scare did not turn what came
WATCH_SIGNS = {
    "watched": [R("all", "sight", 2.0, (0, 0), "you watched {place} through the night with the {scare}; nothing came near it", who="watcher")],
    "failed": [R("all", "sight", 2.0, (0, 0), "in the dark something came at {place} for all the {scare}, and you could not turn it", who="watcher")],
}
SCARE_WORDS = {"fire": "fire", "clapper": "clappers", "horn": "horn", "dog": "dog", "herding": "herders"}
# signs of what the wild kinds ate of the people's crops and stores (the bridge): on the fields and in the stores
EATEN_SIGNS = {
    "crops": [R("lay", "sight", 0.6, (0, 1), "the corn in {place} pecked and nibbled along its edges"),
              R("knows", "sight", 0.7, (0, 1), "pigeons, hares and mice at the corn in {place}: the edges thinned, ears stripped")],
    "stores": [R("lay", "sight", 0.7, (0, 1), "droppings and gnawed sacks in the store of {place}"),
               R("knows", "sight", 0.8, (0, 1), "rats in the store of {place}: the sacks gnawed through at the bottom, runs along the wall")],
}
# the oaks' mast in its seasons, on a village's woods: a reading, and for the practised a lore of what follows
MAST_SIGNS = {
    "flowering": {"heavy": [R("knows", "sight", 0.5, (0, 0), "the oaks in {place} hang heavy with catkins this spring: a mast year coming")],
                  "frost": [R("all", "sight", 0.6, (0, 0), "the oak flowers in {place} blackened by the late frost"),
                            R("knows", "sight", 0.6, (0, 0), "the frost has taken the oak flowers in {place}: there will be few acorns this autumn")]},
    "fallen": {"heavy": [R("all", "sight", 0.8, (0, 0), "acorns lie thick under the oaks in {place}; jays and pigeons everywhere"),
                         R("knows", "sight", 0.6, (0, 0), "a mast year in {place}: the swine could be turned into the wood, and the boar will stay in it")],
               "fail": [R("all", "sight", 0.6, (0, 0), "hardly an acorn under the oaks in {place} this autumn"),
                        R("knows", "sight", 0.6, (0, 0), "a bare year under the oaks in {place}: the boar will be out at the fields and the stores")]},
}
# the mast's windows, by season index and the season's days (a sign of a change: shown as it comes)
MAST_WINDOWS = {"flowering": (0, 5, 7), "fallen": (2, 0, 2)}
# what a hunter notices while hunting a range (a process of its own, as a traveller's notices on the road): the kinds there, by how
# many and how easy to read, whether or not one is met
HUNT_NOTICES = {
    "wild boar": [R("lay", "sight", 0.5, (0, 0), "rooted ground and a wallow in the wood"),
                  R("knows", "sight", 0.7, (0, 0), "boar sign through the wood: a fresh wallow, rubbed trees, a sounder's rooting"),
                  R("expert", "sight", 0.6, (0, 0), "by the lie-ups and the prints, about {n} boar use this ground, {fat}; they are {wary}")],
    "red deer": [R("lay", "sight", 0.4, (0, 0), "slots in the soft ground of the rides"),
                 R("knows", "sight", 0.6, (0, 0), "red deer slots on the rides and fraying on the young trees: a herd uses this wood"),
                 R("expert", "sight", 0.6, (0, 0), "about {n} red deer use this ground by the slots and the beds, {fat}; they are {wary}")],
    "roe deer": [R("knows", "sight", 0.5, (0, 0), "roe slots and browsed bramble tips: roe in the thicket"),
                 R("expert", "sight", 0.5, (0, 0), "about {n} roe hold the thickets here, each to its own patch, {fat}; they are {wary}")],
    "brown hare": [R("all", "sight", 0.25, (0, 0), "a hare going away over the open ground"),
                   R("expert", "sight", 0.4, (0, 0), "hares lying out in their forms on the open ground, about {n} on this land, {fat}")],
    "woodpigeon": [R("knows", "sight", 0.4, (0, 0), "woodpigeons in flocks along the wood's edge"),
                   R("expert", "sight", 0.4, (0, 0), "about {n} woodpigeons feeding here, {fat}: when the mast fails they go to the young corn")],
    "wolf": [R("lay", "sight", 0.4, (0, 0), "big dog-like tracks crossing the ride"),
             R("knows", "sight", 0.6, (0, 0), "wolf tracks crossing the ride, and an old kill picked clean"),
             R("expert", "sight", 0.6, (0, 0), "a pack of about {n} ranges this land, {fat}: {hunger}")],
    "fox": [R("knows", "smell", 0.4, (0, 0), "a fox's musk on a stile"),
            R("expert", "sight", 0.4, (0, 0), "about {n} foxes over this land by the earths and the scats, {fat}: {hunger}")],
    "wildfowl": [R("all", "sight", 0.6, (0, 0), "duck and geese on the open water"),
                 R("expert", "sight", 0.5, (0, 0), "about {n} fowl on the water, {fat}")],
    "eel": [R("expert", "sight", 0.4, (0, 0), "eels in the mud of the pools and the dykes, about {n}: they run on the dark wet nights of autumn")],
    "brown bear": [R("knows", "sight", 0.7, (0, 0), "great claw marks high on a beech, and a stone rolled over"),
                   R("expert", "sight", 0.7, (0, 0), "one bear ranges these woods, {fat}: {hunger}")],
}
# the state an expert reads in a hunt's notices: a kind's condition, its wariness, its hunger (engine/wild._notices)
FAT_WORDS = ((0.75, "fat and in good fettle"), (0.45, "in fair condition"), (0.25, "lean"), (0.0, "starving"))
WARY_WORDS = ((1.0, "wary from the hunting, lying up by day"), (0.3, "a little wary"), (0.0, "unwary"))
HUNGER_WORDS = ((0.5, "hungry enough to come in to the herds and the hens"), (0.0, "with game enough out here not to come near"))


# what a kind's numbers near a village show (wild_layer.md §3.6): the highest row its density reaches, read two ways. `where`: the
# village's own land or the ring around; `per`: density a km2 (`count` for heads in the ring and the land beyond, for packs).
PRESENCE = {
    "voles and mice": [{"where": "ring", "min": 2400, "lay": "kestrels hanging in the wind over the grass, owls calling at night",
                        "knows": "the long grass is thick with voles: runways everywhere, kestrels over every field",
                        "expert": "owl pellets thick with vole skulls under the barn beam: a vole year; the owls and foxes will breed well"},
                       {"where": "ring", "max": 900, "lay": "", "knows": "no owl calling these nights, and few runways in the grass: the voles are few",
                        "expert": "the voles have crashed: the owls are silent, and the foxes will turn to the hens and the nests"}],
    "owls": [{"where": "ring", "min": 1.2, "lay": "owls calling round the village at night", "knows": "owls calling all round at night: good hunting for them",
              "expert": "a barn owl working the rick-yard every dusk: it keeps the mice from the stores, worth its keep"}],
    "rats": [{"where": "home", "min": 60, "lay": "droppings along the walls and something scuttling in the thatch at night",
              "knows": "rat runs along the walls and gnawed holes at the foot of the doors",
              "expert": "rats breeding in the thatch and under the floors: full barns and a mild winter will double them by spring; a terrier or a raised floor"}],
    "wolf": [{"where": "far", "count": 3, "lay": "howling far off in the night", "knows": "wolves howling from the woods at night: a pack ranging near",
              "expert": "the howls come from two places and answer each other: one pack, its range taking in this valley"}],
    "wild boar": [{"where": "ring", "min": 1.0, "lay": "", "knows": "boar sign all through the wood: wallows, rubbed trees, rooted rides",
                   "expert": "the rubbing trees muddied to the height of a big boar: a sounder of sows and young, with a boar coming in for the rut"}],
    "red deer": [{"where": "ring", "min": 0.5, "lay": "", "knows": "deer slots along the rides and hinds with calves in the clearings",
                  "expert": "the deer keep to the far side of the wood by day and come to the edges at dusk"}],
    "raven": [{"where": "ring", "min": 0.15, "lay": "", "knows": "a raven pair croaking over the crags",
               "expert": "the ravens hold the crags all year; where they gather is where something lies dead"}],
}
RAVENS_OVER = {"min_carrion": 20.0, "lay": "ravens wheeling over the wood", "knows": "ravens over the wood: something lies dead there, a kill or a carcass"}


# how a kind is taken (wild_layer.md §3.7; D2-192, D2-193): detect, the chance a searcher in good habitat comes on one; flee, the
# chance it gets away once found; danger to the taker found alone (a crew or a dog divides it); family, the words people look for it
# by; goods, what a kill gives (engine food for meat: real content x Y/365, node_ecology.md).
TAKEN = {
    "red deer":   {"family": ["deer", "red deer", "stag", "hind", "venison", "big game", "game"], "detect": 0.35, "flee": 0.55,
                   "goods": {"meat": 20.0, "hide": 1},           # on the cow's scale, about 3 kg a meat (brief 4 §2.5)
                   "calibrate": {"drive": 0.15}},   # a drive is made for the sounder: deer break back through the beaters (D2-204 §4)
    "roe deer":   {"family": ["deer", "roe", "roe deer", "venison", "game"], "detect": 0.3, "flee": 0.5, "goods": {"meat": 4.5, "hide": 1},
                   "calibrate": {"snare": 0.03}},   # a hare's noose seldom holds a roe (D2-204 §4)
    "wild boar":  {"family": ["boar", "wild boar", "pig", "swine", "sounder", "big game", "game"], "detect": 0.3, "flee": 0.35,
                   "danger": {"wound": 0.3, "kill": 0.03}, "goods": {"meat": 15.0, "hide": 1},
                   "calibrate": {"stalk": 0.12}},   # a sounder in the thicket is not stalked as a deer is (D2-204 §4)
    "brown hare": {"family": ["hare", "hares", "small game", "game"], "detect": 0.5, "flee": 0.5, "goods": {"meat": 0.7}},
    "woodpigeon": {"family": ["pigeon", "pigeons", "birds", "small game"], "detect": 0.4, "flee": 0.75, "goods": {"meat": 0.1},
                   "calibrate": {"net": 0.1}},      # pigeons seldom come down to the fowler's nets and decoys (D2-204 §4)
    "wildfowl":   {"family": ["fowl", "duck", "ducks", "geese", "birds", "wildfowl"], "detect": 0.5, "flee": 0.6, "goods": {"meat": 0.3},
                   "calibrate": {"trap in water": 0.1}},   # a duck drowned in an eel trap now and then, no more (D2-204 §4)
    "stoat":      {"family": ["stoat", "stoats", "weasel", "ermine", "vermin"], "detect": 0.1, "flee": 0.7, "goods": {"hide": 1}},
    "fox":        {"family": ["fox", "foxes", "vermin"], "detect": 0.15, "flee": 0.6, "goods": {"hide": 1},
                   "litter": {"home": "den", "if": {"seasons": {0: (0, 7)}}, "n": 3}},       # cubs at the earth in spring (D2-204: on the kind)
    # D2-204 (brief 1): an eel trap took eels that gave nothing (no row); a night's lift is several eels (calibrate)
    "eel":        {"family": ["eel", "eels", "fish"], "detect": 0.4, "flee": 0.3, "goods": {"meat": 0.2}},
    "wolf":       {"family": ["wolf", "wolves", "big game"], "detect": 0.12, "flee": 0.5, "danger": {"wound": 0.25, "kill": 0.04},
                   "goods": {"hide": 1}},
    "brown bear": {"family": ["bear", "big game"], "detect": 0.1, "flee": 0.3, "danger": {"wound": 0.5, "kill": 0.12},
                   "goods": {"meat": 40.0, "hide": 2}},
}


# ---------------------------------------------------------------------- wave 3: loads, phenology (wild_layer.md §6 phase 7)
# Loads (02zp §23 "Load"): fast kinds counted as a level an area (1 an ordinary year), moving each day toward a target the weather
# sets on the area's ground, and following or eaten by another load; harm in windows to crops of a family at an age (days since
# sown), a share of the standing crop a day for each unit of the level over `over`; `cut` by a guard (a technique's wild_guard).
# hab: the ground (soil textures, covers: shares of the area); drivers: wet (soil wetness, 1 at the mean rain, to a power), warm (degrees
# over the season's mean), dry (the reverse of wet); frost: the share killed a frozen night; seasons: when it is active (else it
# falls to `rest`); base: the target's scale (1 if not given). Calibrate against: slugs 4% of need in a median year, 12% at the 90th, 27% at worst (02zp §24).
LOADS = {
    "slugs": {"hab": {"texture": {"clay": 1.3, "loam": 1.0, "chalk": 0.5, "sand": 0.4, "peat": 1.1},
                      "cover": {"field": 1.0, "pasture": 0.8, "meadow": 0.9, "forest": 0.6, "fen": 0.8}},
              "seasons": (0, 1, 2), "rest": 0.6, "rate": 0.3, "base": 1.4, "drivers": {"wet": 2.0, "warm": 0.03}, "frost": 0.15, "most": 4.0,
              "flush": 1.4, "flood": 0.3,
              "harm": [{"crops": ["grain", "winter grain", "legumes"], "age": (0, 5), "share": 0.02, "over": 0.5}],
              "on_crop": True, "guard": {"cut": 0.6, "days": 1, "night": True, "done": "You picked the slugs off the young crop in {place} at dusk as they came out."}},
    "aphids": {"hab": {"cover": {"field": 1.0, "meadow": 0.4, "pasture": 0.3, "scrub": 0.3}},
               "seasons": (0, 1), "rest": 0.3, "rate": 0.35, "drivers": {"warm": 0.12, "dry": 1.0}, "frost": 0.1, "most": 4.0,
               "eaten_by": {"ladybirds": 0.12},
               "harm": [{"crops": ["legumes"], "age": (3, 40), "share": 0.015, "over": 0.8},
                        {"crops": ["grain"], "age": (6, 40), "share": 0.004, "over": 1.2}],
               "on_crop": True, "guard": {"cut": 0.5, "days": 8, "done": "You pinched out the bean tops in {place}, where the fly gathers."}},
    "ladybirds": {"hab": {"cover": {"field": 0.8, "meadow": 0.8, "pasture": 0.6, "scrub": 1.0, "forest": 0.5}},
                  "seasons": (0, 1), "rest": 0.4, "rate": 0.2, "follows": {"aphids": 1.0}, "frost": 0.05, "most": 3.0, "cold_stall": 0.8,
                  "on_crop": True, "guard": {"cut": 0.0, "days": 1, "thin": {"ladybirds": 0.5},
                                             "done": "You picked the grey spiny grubs off the beans in {place}."}},
    # moles (brief 2 K1): in meadow and pasture, raised by a wet spring and autumn; they spoil the grass the hay is cut from; pest work
    # traps them in their runs
    "moles": {"hab": {"texture": {"loam": 1.0, "clay": 0.8, "sand": 0.9, "chalk": 0.7, "peat": 0.6},
                      "cover": {"meadow": 1.0, "pasture": 1.0, "field": 0.3}},
              "seasons": (0, 2), "rest": 0.7, "rate": 0.15, "drivers": {"wet": 1.0}, "frost": 0.02, "most": 3.0,
              "harm_res": [{"res": "grass", "covers": ["meadow", "pasture"], "share": 0.004, "over": 0.6}],
              "on_crop": True, "guard": {"cut": 0.7, "days": 8, "thin": {"moles": 0.3},          # traps kill moles (calibrate)
                                            "done": "You set traps in the mole runs in {place} and took the moles out."}},
    # the rooks' grubs (leatherjackets; brief 2 K1): in fields and pasture, raised by a wet autumn; they eat the young corn's roots; the
    # rookery's birds work them off the parcels within reach of the site
    "leatherjackets": {"hab": {"cover": {"field": 1.0, "pasture": 1.0, "meadow": 0.6}},
              "seasons": (2, 3, 0), "rest": 0.5, "rate": 0.2, "drivers": {"wet": 1.5}, "frost": 0.03, "most": 3.0,
              "harm": [{"crops": ["grain", "winter grain"], "age": (0, 8), "share": 0.008, "over": 0.8}],
              "site_eats": {"site": "rookery", "reach": 2, "share": 0.6},
              "on_crop": True, "guard": {"cut": 0.4, "days": 4, "done": "You turned the ground and picked the grey grubs out of {place}."}},
    "fungi": {"hab": {"cover": {"forest": 1.0, "scrub": 0.5, "pasture": 0.6, "meadow": 0.6, "heath": 0.4}},
              "seasons": (2,), "rest": 0.0, "start": 0.0, "rate": 0.4, "drivers": {"wet": 1.5, "warm": 0.08}, "frost": 0.5, "most": 3.0},                                                                  # the mushrooms' year (wild/plants.py)
}
# the signs of a load's level and of its harm, by the four kinds (the level: lingering, as it stands that morning; the harm: on the
# field where it fell). `level`: the least level a row needs (and `below` the most).
LOAD_SIGNS = {
    "slugs": {"level": [R("lay", "sight", 0.7, (0, 0), "silver slime trails across the paths in the morning, and slugs out on the wet grass", cond=None),
                        R("knows", "sight", 0.8, (0, 0), "slugs thick on the wet ground: a slug year, and the young corn will suffer where the ground is heavy"),
                        R("all", "sight", 0.5, (0, 0), "the thrushes' anvil stones littered with broken snail shells"),
                        R("expert", "sight", 0.6, (0, 0), "after a wet mild winter like this, sow later, when the ground dries, or burn the stubble first")],
              "harm": [R("all", "sight", 0.9, (0, 1), "the young corn in {place} grazed off to stumps in patches, slime on what is left")],
              "least": 1.6},
    "aphids": {"level": [R("lay", "sight", 0.6, (0, 0), "the bean tops black with fly"),
                         R("all", "sight", 0.4, (0, 0), "ants running up and down the bean stems"),
                         R("knows", "sight", 0.7, (0, 0), "blackfly thick on the bean tops: the beans will be poor unless the tops come off or the ladybirds come"),
                         R("expert", "sight", 0.6, (0, 0), "the fly is up with the warm spell; the ladybirds come a week behind it: top only the worst of the beans")],
               "harm": [R("all", "sight", 0.8, (0, 1), "the crop in {place} sticky and curled, black with fly")], "least": 1.5},
    "ladybirds": {"level": [R("all", "sight", 0.6, (0, 0), "ladybirds everywhere on the beans and the nettles"),
                            R("lay", "sight", 0.6, (0, 0), "grey spiny grubs crawling among the fly on the beans: some new pest"),
                            R("knows", "sight", 0.6, (0, 0), "the ladybirds are on the beans, their spiny grey grubs among the fly: leave them, the fly will be gone in a few days"),
                            R("expert", "sight", 0.5, (0, 0), "the ladybirds have caught up with the fly; a cold snap now would hold them back more than the fly")], "least": 1.2},
    "fungi": {"level": [R("all", "sight", 0.8, (0, 0), "mushrooms pushing up all through {place} after the rain"),
                        R("knows", "sight", 0.7, (0, 0), "a flush of ceps and field mushrooms in {place}: good picking for a few days"),
                        R("expert", "sight", 0.6, (0, 0), "among the good ones in {place} the pale caps with white gills and a cup at the foot: those kill")], "least": 1.3},
}
LOAD_READ = {"slugs": "sow", "aphids": "sow", "ladybirds": "sow", "fungi": "forage", "moles": "hay", "leatherjackets": "sow"}     # whose practice reads a load's `knows` rows
# phenology (calendar markers): each comes when the year's warmth (degree days over 5 C from the start of spring, real days) passes
# its mark, so a warm spring brings it early; `lore`, the practised reading, says whether it holds in this world ("holds") or is a
# saying with nothing behind it ("fails", D2-199: lore that fails). `after` for autumn markers: the first night below `low`.
# Measured on the steady, cold and wet climates (12 years, five villages): a frost after the blackthorn in 15-18 of 60 years, after
# the may in none, after oak-and-ash leafing in 1; oak before ash has no tie to the summer's rain here.
MARKERS = {
    "blackthorn": {"gdd": 60, "usual": 2, "rows": [R("expert", "sight", 0.6, (0, 0), "the blackthorn is {when} this year: the ground is warming {when2}"),R("all", "sight", 0.9, (0, 0), "the blackthorn white along the hedges"),
                                       R("knows", "sight", 0.7, (0, 0), "the blackthorn in flower: the ground is warming for the spring corn, but a cold snap often follows the blackthorn")],
                   "read": "sow", "lore": "holds", "times": "grain", "say": "the blackthorn's in flower: time to sow the {crop}"},
    "swallows": {"gdd": 140, "usual": 4, "rows": [R("all", "sight", 0.8, (0, 0), "the first swallows over the village"),
                                                  R("expert", "sight", 0.5, (0, 0), "the swallows are back {when}")], "read": "hunt", "lore": None},
    "cuckoo": {"gdd": 160, "usual": 5, "rows": [R("all", "sound", 1.0, (0, 0), "the first cuckoo calling from the wood"),
                                                R("expert", "sound", 0.5, (0, 0), "the cuckoo {when} this year")], "read": "sow", "lore": None,
               "times": "legumes", "say": "the cuckoo's calling: time to sow the {crop}"},
    "frogspawn": {"after": {"season": 0, "until": 0, "soil": 1.2, "temp": 6.0},
                  "rows": [R("all", "sight", 0.7, (0, 0), "frogspawn in the ditches after the first mild wet night"),
                           R("expert", "sight", 0.4, (0, 0), "the toads walking back to their own pond, the same one every year")],
                  "read": "sow", "lore": None},
    "oak and ash": {"gdd": 220, "usual": 7, "rows": [R("expert", "sight", 0.6, (0, 0), "oak before ash shows a warm spring, nothing more: it tells you nothing of the summer's rain"),R("all", "sight", 0.6, (0, 0), "the oaks in leaf before the ash this year"),
                                         R("knows", "sight", 0.6, (0, 0), "oak before ash: only a splash, they say; a dry summer to come")],
                    "read": "sow", "lore": "fails"},
    "may": {"gdd": 330, "usual": 8, "rows": [R("expert", "sight", 0.6, (0, 0), "the may is out {when} this year: the tender crops can go in"),R("all", "sight", 0.9, (0, 0), "the may in blossom on every hawthorn"),
                                 R("knows", "sight", 0.7, (0, 0), "the may is out: the frosts are done with, and the tender crops are safe")],
            "read": "sow", "lore": "holds"},
    "first frost": {"after": {"season": 2, "low": 0.0}, "usual": 24, "rows": [R("expert", "sight", 0.6, (0, 0), "the first frost has come {when}"),R("all", "sight", 0.9, (0, 0), "the first white frost on the grass this morning"),
                                                                 R("knows", "sight", 0.7, (0, 0), "the first frost: get in what is left in the fields before the hard ones")],
                    "read": "reap", "lore": "holds"},
}
GDD_BASE, REAL_DAYS = 5.0, 91.0                                                  # degree days over 5 C; real days a season


# ---------------------------------------------------------------------- wave 4: disease by host and area (wild_layer.md §6 phase 8)
# A disease's prevalence in each area among its wild hosts (a share infected), rising with the hosts' crowding (each host's density
# against its crowding level, weighted) among those not immune, and falling as the sick recover (immune, losing it at `wane` a
# day) or die; it spreads along the land's links (`mix`, a share a
# day of the difference) and is seeded in its season by a keyed draw (`seed`: the chance an area is seeded, times crowding squared).
# `kill`: the hosts' extra death rate a day at full prevalence. Kept hosts (a herd kind): infection a night from the sick in herds on
# the same parcel (`beta`, by the sick share), less from a parcel beside it (`near`) or the same village (`node`), from the wild
# hosts' prevalence on the village's land (`wild`), and from beyond the world (`arrive`: a chance a year at each village, a keyed
# draw); a beast sick for `course` days dies (`mortality`) or recovers, and is then immune. `milk`: what the sick share costs in milk.
# Kinds that are hosts to no disease here keep the ecology's background outbreak.
DISEASES = {
    "murrain": {"wild": {"red deer": 0.5, "roe deer": 0.3}, "kept": ["cattle"], "beta": 1.6, "near": 0.3, "node": 0.08,
                "wild_beta": 0.4, "arrive": 0.06, "course": 2, "mortality": 0.45, "milk": 0.8,
                "rise": 0.5, "recover": 0.3, "wane": 0.01, "kill": 0.03, "mix": 0.06, "seed": 0.04, "season": 1},
    "mange": {"wild": {"fox": 1.0, "wolf": 0.4}, "rise": 0.45, "recover": 0.2, "wane": 0.03, "kill": 0.08, "mix": 0.05, "seed": 0.15, "season": 2},
    "swine fever": {"wild": {"wild boar": 1.0}, "kept": ["pigs"], "beta": 1.4, "near": 0.3, "node": 0.08, "wild_beta": 0.4,
                    "arrive": 0.03, "course": 2, "mortality": 0.6, "rise": 0.5, "recover": 0.3, "wane": 0.01, "kill": 0.04, "mix": 0.05,
                    "seed": 0.03, "season": 3},
    "hare sickness": {"wild": {"brown hare": 1.0}, "rise": 0.6, "recover": 0.3, "wane": 0.02, "kill": 0.05, "mix": 0.04, "seed": 0.06, "season": 1},
}
# the signs of a disease: in a herd (`herd`), in the wild hosts on the village's land when the prevalence passes `least` (`wild`),
# and how one who knows herding reads a beast it killed (`carcass`)
DISEASE_SIGNS = {
    "murrain": {"herd": [R("lay", "sight", 0.9, (0, 0), "beasts of {herd} off their feed, running at the eyes and nose, their dung loose"),
                         R("knows", "sight", 0.9, (0, 0), "murrain in {herd}: keep them off the common grass and away from every other herd, or it will go through them all"),
                         R("expert", "sight", 0.8, (0, 0), "murrain in {herd}: a beast that lives through it won't take it again; it goes worst where herds share the grass")],
                "wild": [R("knows", "sight", 0.5, (0, 0), "a deer lying dead at the wood's edge, wasted and scoured: the murrain is among the deer")],
                "carcass": "the {beast} {at} died of the murrain: wasted, the mouth raw, filthy with scour; keep the others away from it",
                "least": 0.15, "read": "herd", "wild_read": "hunt"},
    "mange": {"wild": [R("lay", "sight", 0.5, (0, 0), "a thin fox seen by day near the houses, half its coat gone grey and bare"),
                       R("knows", "sight", 0.6, (0, 0), "mange among the foxes: a bare, scratching fox by day; there will be fewer of them at the hens"),
                       R("expert", "sight", 0.5, (0, 0), "mange sweeps the foxes when they are many; it burns out in a season and they stay fewer a year or two")],
              "least": 0.25, "read": "hunt"},
    "swine fever": {"wild": [R("all", "sight", 0.6, (0, 0), "a dead boar in the wood, untouched by the crows"),
                             R("knows", "sight", 0.6, (0, 0), "dead boar in the wood: a sickness in the sounders; keep any pigs out of the wood"),
                             R("expert", "sight", 0.5, (0, 0), "swine fever in the boar, worst in the cold: the sounders will be thin next year, and the fields quieter")],
                    "least": 0.15, "read": "hunt"},
    "hare sickness": {"wild": [R("all", "sight", 0.6, (0, 0), "hares lying dead in the open fields, untouched"),
                               R("knows", "sight", 0.5, (0, 0), "a sickness among the hares: dead ones in the open; leave them lie"),
                               R("expert", "sight", 0.4, (0, 0), "the hare sickness comes when they are thick; there will be few to snare till next spring")],
                      "least": 0.2, "read": "hunt"},
}


# what a technique the wild pack switches off was practice for (the old generic hunt): those who knew it know these
# A kind's body against barriers (brief 2 §4; calibrate): `gap`, the smallest gap it passes; `climbs`. Read by doors, stores, fences.
BODY = {"voles and mice": {"gap": "tiny", "climbs": True}, "rats": {"gap": "tiny", "climbs": True},
        "fox": {"gap": "medium", "climbs": False}, "stoat": {"gap": "small", "climbs": True}, "wolf": {"gap": "large", "climbs": False},
        "wild boar": {"gap": "large", "climbs": False}, "red deer": {"gap": "large", "climbs": False},
        "brown bear": {"gap": "large", "climbs": True}, "woodpigeon": {"gap": "small", "climbs": True}}
GAPS = {"structure": {"wattle": "small", "timber": "small", "stone": "tiny", "camp": "large"}, "damaged": 1}   # a building's own gaps
# What stops which kinds in a store (brief 2 §4): each fitting cuts the share the kinds it stops eat there (keep), by their body
STORE_STOPS = {"granary": {"keep": 0.3, "for": {"climbs": True, "gap": "tiny"}}, "bins": {"keep": 0.5, "for": {"gap": "tiny"}},
               "dog": {"keep": 0.5, "for": {}}, "cat": {"keep": 0.4, "for": {"gap": "tiny"}, "in_store": True},
               "owl": {"keep": 0.6, "for": {"gap": "tiny"}, "occupied": "nests"}}
# a cat comes by itself to a store with mice (D2-206): a chance each season (no dog), and leaves an empty store or a dog's house;
# a barn owl takes an owl hole in spring with a chance if nobody sleeps in that building (calibrate)
# The dead and what comes to them (brief 3 §3, calibrate): a carcass row's attraction is its attr times the most flesh at the node
# against `ref` (units of meat), a shallow grave `dig` of that; a group that fed at the dead there has, for `spill_nights` nights,
# its drive times `spill_drive` and may pick any of its rows (the fox at the dead calf tries the hens)
# a tallow light (brief 3 §5, calibrate): night work at a load by it does this much more, and burns the light down
LIGHT = {"item": "tallow light", "night_work": 1.3}
CARCASS_PULL = {"ref": 20.0, "dig": 0.1, "spill_nights": 3, "spill_drive": 1.5}
CAT = {"settle_p": 0.25, "prey": "voles and mice", "prey_least": 50.0, "stray_p": 0.08, "item": "cat"}
OWL = {"take_p": 0.4, "fitting": "owl hole", "season": "spring", "record": "nests"}

# What a kind is like to those who hunt it (D2-204, methods_and_encounters.md §2; calibrate): the methods' needs and favours are read
# against these at load to build each method's take table (engine/methods.py). A kind without traits is no method's target.
TRAITS = {
    "red deer":   {"size": "large", "runs": True, "social": "group", "home": "none", "water": False},
    "roe deer":   {"size": "medium", "runs": True, "social": "solitary", "home": "none", "water": False},
    "wild boar":  {"size": "large", "runs": True, "social": "group", "home": "none", "water": False},
    "brown hare": {"size": "small", "runs": True, "social": "solitary", "home": "form", "water": False},
    "woodpigeon": {"size": "small", "runs": False, "social": "flock", "home": "none", "water": False},
    "fox":        {"size": "medium", "runs": True, "social": "solitary", "home": "den", "water": False},
    "stoat":      {"size": "small", "runs": True, "social": "solitary", "home": "burrow", "water": False},
    "wolf":       {"size": "large", "runs": True, "social": "group", "home": "den", "water": False},
    "brown bear": {"size": "large", "runs": False, "social": "solitary", "home": "den", "water": False},
    "wildfowl":   {"size": "small", "runs": False, "social": "flock", "home": "none", "water": True},
    "eel":        {"size": "small", "runs": False, "social": "solitary", "home": "none", "water": True, "mover": "cue"},
}


def rows() -> dict:
    """The kinds as RESOURCES rows (merged into data.RESOURCES; pack "wild")."""
    return {name: {"renewal": "population", "pack": "wild", "population": k, **({"near_people": NEAR_PEOPLE[name]} if name in NEAR_PEOPLE else {}),
                   **({"taken": {**TAKEN[name], **({"traits": TRAITS[name]} if name in TRAITS else {})}} if name in TAKEN else {}),
                   **({"presence": PRESENCE[name]} if name in PRESENCE else {}), **({"body": BODY[name]} if name in BODY else {})}
            for name, k in KINDS.items()}
