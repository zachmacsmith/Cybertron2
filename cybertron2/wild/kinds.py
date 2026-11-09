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
    },
    "red deer": {
        "targets": [{"seasons": {0: (2, 7)}, "attr": 0.5, "trample": 0.006},                # the young corn
                    {"seasons": {1: (3, 7)}, "attr": 0.4, "trample": 0.004}],              # the ripening corn
        "drive": {"base": 0.2, "hunger": 0.5}, "memory_days": 3, "return_p": 0.6, "lead_nights": 2, "lead_sign_p": 0.8,
        "answer": {"type": "habituate", "turn_p": 0.85, "gain": 0.25, "decay": 0.01, "rest": 2},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 5, "met_share": 0.5,
    },
    "wolf": {
        "gather": "far",                                                                     # a pack ranges far beyond one ring
        "targets": [{"what": "herd", "seasons": {3: (0, 7), 0: (0, 2)}, "attr": 1.0},          # late winter: hunger at the fold
                    {"what": "herd", "seasons": {0: (3, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35}],
        "drive": {"base": 0.03, "hunger": 0.9}, "memory_days": 4, "return_p": 0.7, "lead_nights": 2, "lead_sign_p": 0.7,
        "answer": {"type": "scared_off", "turn_p": 0.8, "off_days": 3},
        "harm": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 10, "met_share": 1.0,
    },
    "fox": {
        "targets": [{"what": "hens", "seasons": {0: (2, 7), 1: (0, 3)}, "attr": 1.0},           # cubs to feed
                    {"what": "hens", "seasons": {0: (0, 7), 1: (0, 7), 2: (0, 7), 3: (0, 7)}, "attr": 0.35}],
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
                 "fox": "a fox's kill {at}: the head bitten off, the rest dragged"}
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
                  R("knows", "sight", 0.7, (0, 0), "boar sign through the wood: a fresh wallow, rubbed trees, a sounder's rooting")],
    "red deer": [R("lay", "sight", 0.4, (0, 0), "slots in the soft ground of the rides"),
                 R("knows", "sight", 0.6, (0, 0), "red deer slots on the rides and fraying on the young trees: a herd uses this wood")],
    "roe deer": [R("knows", "sight", 0.5, (0, 0), "roe slots and browsed bramble tips: roe in the thicket")],
    "brown hare": [R("all", "sight", 0.5, (0, 0), "a hare going away over the open ground")],
    "wolf": [R("lay", "sight", 0.4, (0, 0), "big dog-like tracks crossing the ride"),
             R("knows", "sight", 0.6, (0, 0), "wolf tracks crossing the ride, and an old kill picked clean")],
    "fox": [R("knows", "smell", 0.4, (0, 0), "a fox's musk on a stile")],
    "wildfowl": [R("all", "sight", 0.6, (0, 0), "duck and geese on the open water")],
    "brown bear": [R("knows", "sight", 0.7, (0, 0), "great claw marks high on a beech, and a stone rolled over")],
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
              "harm": [{"crops": ["grain", "winter grain", "legumes"], "age": (0, 5), "share": 0.02, "over": 0.5}]},
    "aphids": {"hab": {"cover": {"field": 1.0, "meadow": 0.4, "pasture": 0.3, "scrub": 0.3}},
               "seasons": (0, 1), "rest": 0.3, "rate": 0.35, "drivers": {"warm": 0.12, "dry": 1.0}, "frost": 0.3, "most": 4.0,
               "eaten_by": {"ladybirds": 0.12},
               "harm": [{"crops": ["legumes"], "age": (3, 40), "share": 0.015, "over": 0.8},
                        {"crops": ["grain"], "age": (6, 40), "share": 0.004, "over": 1.2}]},
    "ladybirds": {"hab": {"cover": {"field": 0.8, "meadow": 0.8, "pasture": 0.6, "scrub": 1.0, "forest": 0.5}},
                  "seasons": (0, 1), "rest": 0.4, "rate": 0.2, "follows": {"aphids": 1.0}, "frost": 0.05, "most": 3.0},
    "fungi": {"hab": {"cover": {"forest": 1.0, "scrub": 0.5, "pasture": 0.6, "meadow": 0.6, "heath": 0.4}},
              "seasons": (2,), "rest": 0.0, "start": 0.0, "rate": 0.4, "drivers": {"wet": 1.5, "warm": 0.08}, "frost": 0.5, "most": 3.0,
              "feeds": {"res": "plants", "covers": ["forest", "scrub", "pasture", "meadow"], "over": 1.0, "share": 0.12}},
}
# the signs of a load's level and of its harm, by the four kinds (the level: lingering, as it stands that morning; the harm: on the
# field where it fell). `level`: the least level a row needs (and `below` the most).
LOAD_SIGNS = {
    "slugs": {"level": [R("lay", "sight", 0.7, (0, 0), "silver slime trails across the paths in the morning, and slugs out on the wet grass", cond=None),
                        R("knows", "sight", 0.8, (0, 0), "slugs thick on the wet ground: a slug year, and the young corn will suffer where the ground is heavy")],
              "harm": [R("all", "sight", 0.9, (0, 1), "the young corn in {place} grazed off to stumps in patches, slime on what is left")],
              "least": 1.6},
    "aphids": {"level": [R("lay", "sight", 0.6, (0, 0), "the bean tops black with fly"),
                         R("knows", "sight", 0.7, (0, 0), "blackfly thick on the bean tops: the beans will be poor unless the tops come off or the ladybirds come")],
               "harm": [R("all", "sight", 0.8, (0, 1), "the crop in {place} sticky and curled, black with fly")], "least": 1.5},
    "ladybirds": {"level": [R("all", "sight", 0.6, (0, 0), "ladybirds everywhere on the beans and the nettles"),
                            R("knows", "sight", 0.6, (0, 0), "the ladybirds are on the beans: the fly will be gone in a few days")], "least": 1.2},
    "fungi": {"level": [R("all", "sight", 0.8, (0, 0), "mushrooms pushing up all through {place} after the rain"),
                        R("knows", "sight", 0.7, (0, 0), "a flush of ceps and field mushrooms in {place}: good picking for a few days")], "least": 1.3},
}
LOAD_READ = {"slugs": "sow", "aphids": "sow", "ladybirds": "sow", "fungi": "forage"}     # whose practice reads a load's `knows` rows
# phenology (calendar markers): each comes when the year's warmth (degree days over 5 C from the start of spring, real days) passes
# its mark, so a warm spring brings it early; `lore`, the practised reading, says whether it holds in this world ("holds") or is a
# saying with nothing behind it ("fails", D2-199: lore that fails). `after` for autumn markers: the first night below `low`.
# Measured on the steady, cold and wet climates (12 years, five villages): a frost after the blackthorn in 15-18 of 60 years, after
# the may in none, after oak-and-ash leafing in 1; oak before ash has no tie to the summer's rain here.
MARKERS = {
    "blackthorn": {"gdd": 60, "rows": [R("all", "sight", 0.9, (0, 0), "the blackthorn white along the hedges"),
                                       R("knows", "sight", 0.7, (0, 0), "the blackthorn in flower: the ground is warming for the spring corn, but a cold snap often follows the blackthorn")],
                   "read": "sow", "lore": "holds"},
    "swallows": {"gdd": 140, "rows": [R("all", "sight", 0.8, (0, 0), "the first swallows over the village")], "lore": None},
    "oak and ash": {"gdd": 220, "rows": [R("all", "sight", 0.6, (0, 0), "the oaks in leaf before the ash this year"),
                                         R("knows", "sight", 0.6, (0, 0), "oak before ash: only a splash, they say; a dry summer to come")],
                    "read": "sow", "lore": "fails"},
    "may": {"gdd": 330, "rows": [R("all", "sight", 0.9, (0, 0), "the may in blossom on every hawthorn"),
                                 R("knows", "sight", 0.7, (0, 0), "the may is out: the frosts are done with, and the tender crops are safe")],
            "read": "sow", "lore": "holds"},
    "first frost": {"after": {"season": 2, "low": 0.0}, "rows": [R("all", "sight", 0.9, (0, 0), "the first white frost on the grass this morning"),
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
    "hare sickness": {"wild": {"brown hare": 1.0}, "rise": 0.6, "recover": 0.3, "wane": 0.02, "kill": 0.05, "mix": 0.04, "seed": 0.06, "season": 1},
}
# the signs of a disease: in a herd (`herd`), in the wild hosts on the village's land when the prevalence passes `least` (`wild`),
# and how one who knows herding reads a beast it killed (`carcass`)
DISEASE_SIGNS = {
    "murrain": {"herd": [R("lay", "sight", 0.9, (0, 0), "beasts of {herd} off their feed, running at the eyes and nose, their dung loose"),
                         R("knows", "sight", 0.9, (0, 0), "murrain in {herd}: keep them off the common grass and away from every other herd, or it will go through them all")],
                "wild": [R("knows", "sight", 0.5, (0, 0), "a deer lying dead at the wood's edge, wasted and scoured: the murrain is among the deer")],
                "carcass": "the {beast} {at} died of the murrain: wasted, the mouth raw, filthy with scour; keep the others away from it",
                "least": 0.15, "read": "herd", "wild_read": "hunt"},
    "mange": {"wild": [R("lay", "sight", 0.5, (0, 0), "a thin fox seen by day near the houses, half its coat gone grey and bare"),
                       R("knows", "sight", 0.6, (0, 0), "mange among the foxes: a bare, scratching fox by day; there will be fewer of them at the hens")],
              "least": 0.25, "read": "hunt"},
    "hare sickness": {"wild": [R("all", "sight", 0.6, (0, 0), "hares lying dead in the open fields, untouched"),
                               R("knows", "sight", 0.5, (0, 0), "a sickness among the hares: dead ones in the open; leave them lie")],
                      "least": 0.2, "read": "hunt"},
}


# what a technique the wild pack switches off was practice for (the old generic hunt): those who knew it know these
SKILL_CARRY = {"hunt": ["hunt the wild", "snare hares"]}


def rows() -> dict:
    """The kinds as RESOURCES rows (merged into data.RESOURCES; pack "wild")."""
    return {name: {"renewal": "population", "pack": "wild", "population": k, **({"near_people": NEAR_PEOPLE[name]} if name in NEAR_PEOPLE else {}),
                   **({"taken": TAKEN[name]} if name in TAKEN else {}), **({"presence": PRESENCE[name]} if name in PRESENCE else {})}
            for name, k in KINDS.items()}
