"""Wave 1 of the wild systems (proposals/wild_systems.md §13): the wood's edge, the river and the barn. Every kind is a data row on
the general rules in rules.py; signs are data rows with a reading per level (novice, systematic, expert); acts are named in the
rows. Lambdas in rows read a context, as the engine's own sign rows do (signs.py).

Numbers are first values (calibrate). Foods are engine food (a food is 365/Y real person-days, node_ecology.md).
"""
from __future__ import annotations

import numpy as np

from rules import in_windows


# ------------------------------------------------------------------ the land, read the same way for every kind
def wood(l):
    return l["ring_km2"].get("forest", 0.0) + l["own_ha"].get("forest", 0.0) / 100


def open_land(l):
    return sum(l["ring_km2"].get(c, 0.0) for c in ("pasture", "meadow", "heath"))


def fen(l):
    return l["ring_km2"].get("fen", 0.0) + l["own_ha"].get("fen", 0.0) / 100


def river(l):
    rv = l.get("rivers") or []
    return "river" if "river" in rv else ("brook" if rv else None)


def fields(l):
    return l["own_ha"].get("field", 0.0)


# ------------------------------------------------------------------ pulses
PULSES = {"mast": {"levels": {"heavy": 3.0, "ordinary": 1.0, "poor": 0.4, "fail": 0.15}, "every": (2, 5), "ordinary_p": 0.6,
                   "spoiler": "flower_frost"}}

RUN_SEASON = [(1, 7, 7), (2, 0, 7), (3, 0, 1)]

# ------------------------------------------------------------------ the kinds
KINDS = {
    "wild boar": {
        "rule": "Group", "archetype": "resident group", "depth": "deep",
        "place": {"habitat": wood, "min_n": 2,
                  "size": lambda l, dens: int(np.clip(round(3 + 0.06 * dens * wood(l)), 3, 14)) if dens * wood(l) >= 4 else 0},
        "density": {"start": 3.0, "pulse": "mast", "neutral": 1.0, "grow": {3.0: 1.0, 1.0: 0.45, 0.4: 0.25, 0.15: 0.12},
                    "K": 5.0, "K_heavy": 1.3, "hard_winter_loss": 0.6, "hard_winter_if": (0.15, 0.4), "survive": 0.9, "floor": 0.2},
        "targets": [{"windows": [(1, 3, 7), (2, 0, 1)], "target": "crop", "attr": 1.0, "loss": 0.005},
                    {"windows": [(0, 0, 5)], "target": "seed_spring", "attr": 0.3, "loss": 0.02},
                    {"windows": [(2, 2, 7), (3, 0, 7)], "target": "stores", "attr": 0.4, "loss": 0.004}],
        "otherwise": {"target": "crop", "attr": 0.1, "loss": 0.002},
        "frozen": {"target": "stores", "attr": 0.5, "loss": 0.004},
        "home_food": {"by_season": {2: lambda c: min(1.0, c.pulse("mast") / 2), 3: lambda c: min(1.0, c.pulse("mast") / 2)},
                      "otherwise": 0.6, "frozen": 0.1},
        "drive": {"base": 0.12, "hunger": 0.6}, "memory_days": 3, "return_p": 0.85,
        "lead_nights": 2, "lead_sign_p": 0.9, "gap_loyalty": 0.75, "per_head": True, "trace_days": 2, "met_share": 0.5,
        "answer": {"type": "habituate", "turn_p": 0.9, "gain": 0.3, "decay": 0.01, "rest": 2},
        "harm_scares": {"dog": {"turn_p": 0.95, "harm_p": 0.25}}, "wary_after_harm": 8,
        "take": {"act": "hunt_boar", "technique": "a boar hunt", "crew": 2, "units": 6, "danger": True,
                 "p": {"novice": 0.2, "systematic": 0.3, "expert": 0.5}, "goods": {"meat": 3.5, "fat": 0.5, "hide": 1}},
        "moments": {"edge": "boar.rooting", "raid": "boar.trampled", "turned": "watch.turned", "not_turned": "watch.not_turned",
                    "missed": "watch.missed"},
    },
    "red deer": {
        "rule": "Group", "archetype": "resident group", "depth": "middling",
        "place": {"habitat": wood, "min_n": 3,
                  "size": lambda l, dens: int(np.clip(round(4 + 0.04 * dens * wood(l)), 4, 15)) if dens * wood(l) >= 5 else 0},
        "density": {"start": 4.0, "pulse": None, "neutral": None, "grow": 0.25, "K": 8.0, "hard_winter_loss": 0.85,
                    "hard_winter_if": (None,), "survive": 0.95, "floor": 0.5},
        "targets": [{"windows": [(0, 2, 7)], "target": "seed_spring", "attr": 0.5, "loss": 0.012},
                    {"windows": [(1, 3, 7)], "target": "crop", "attr": 0.4, "loss": 0.0015}],
        "otherwise": {"target": "crop", "attr": 0.05, "loss": 0.001},
        "frozen": {"target": "ricks", "attr": 0.7, "loss": 0.01},
        "home_food": {"by_season": {3: 0.3}, "otherwise": 0.7, "frozen": 0.1},
        "drive": {"base": 0.08, "hunger": 0.5}, "memory_days": 3, "return_p": 0.6,
        "lead_nights": 2, "lead_sign_p": 0.8, "gap_loyalty": 0.8, "per_head": True, "trace_days": 1, "met_share": 0.5,
        "answer": {"type": "habituate", "turn_p": 0.85, "gain": 0.25, "decay": 0.01, "rest": 2},
        "harm_scares": {"dog": {"turn_p": 0.9, "harm_p": 0.15}}, "wary_after_harm": 5,
        "take": {"act": "stalk_deer", "technique": "stalking", "crew": 1, "units": 3, "rights": True,
                 "p": {"novice": 0.15, "systematic": 0.3, "expert": 0.5}, "goods": {"meat": 3.9, "hide": 1, "antler": 0.3}},
        "moments": {"edge": "deer.slots", "raid": "deer.grazed", "turned": "watch.turned", "not_turned": "watch.not_turned",
                    "missed": "watch.missed"},
    },
    "hare": {
        "rule": "Load", "archetype": "resident (many)", "depth": "simple",
        "place": lambda l: min(1.0, open_land(l) / 15.0),
        "level": lambda c: 0.6 if c.D.hard_winter(c.y - 1) else 1.0,
        "windows": [{"windows": [(0, 0, 7)], "target": "seed_spring", "rate": 0.004},
                    {"windows": [(2, 2, 7)], "target": "seed_autumn", "rate": 0.003}],
        "scares": ("scarecrow", "children_scare"), "scare_units": {"scarecrow": 0.1, "children_scare": 2.0},
        "scare_by": {"children_scare": "children"},
        "answer": {"type": "scared_off", "turn_p": 0.9, "off_days": 3, "turned_share": 0.2, "while_off": 0.2},
        "take": {"act": "snare", "technique": "snaring", "units": 1, "yield": lambda lvl, c: 1.5 * lvl, "goods": {"meat": 0.18, "pelt": 1},
                 "depletes": 0.97},
        "moments": [{"when": lambda a, c: a > 0.4 and c.sd in (1, 4), "sign": "hare.nibbled"}],
        "scare_moments": {"worked": "hare.scare_worked", "failed": "hare.scare_failed"},
    },
    "birds at the corn": {
        "rule": "Load", "archetype": "follower of people", "depth": "simple",
        "place": lambda l: 1.0 if fields(l) > 0 else 0.0,
        "level": lambda c: 1.0,
        "windows": [{"windows": [(0, 0, 3)], "target": "seed_spring", "rate": 0.012},
                    {"windows": [(1, 4, 7)], "target": "crop", "rate": 0.0015},
                    {"windows": [(2, 2, 5)], "target": "seed_autumn", "rate": 0.01,
                     "activity": lambda c: 1.8 if c.pulse("mast") <= 0.4 else 1.0}],      # woodpigeons onto the winter corn
        "scares": ("scarecrow", "children_scare"), "scare_units": {"scarecrow": 0.1, "children_scare": 2.0},
        "scare_by": {"children_scare": "children"},
        "answer": {"type": "habituate", "turn_p": 0.85, "gain": {"scarecrow": 0.35, "children_scare": 0.08}, "decay": 0.03,
                   "turned_share": 0.25},
        "moments": [{"when": lambda a, c: a > 1.0, "sign": "birds.flocks"}],
        "scare_moments": {"worked": "birds.scare_worked", "failed": "birds.scare_failed"},
    },
    "rats and mice": {
        "rule": "Load", "archetype": "follower of people", "depth": "simple",
        "place": lambda l: 1.0,
        "level": lambda c: (1.4 if c.D.anom(c.y - 1, 3, "T") > 0.5 else 1.0) * (1.3 if c.y and c.pulse("mast", c.y - 1) >= 3 else 1.0),
        "windows": [{"windows": [(2, 2, 7), (3, 0, 7), (0, 0, 7)], "target": "stores", "rate": 0.0015,
                     "activity": lambda c: 1.3 if c.s == 3 else 1.0}],
        "levers": {"cats": 0.4, "staddles": 0.3},
        "scares": (), "scare_units": {},
        "answer": {"type": "none"},
        "take": {"act": "trap_rats", "technique": "rat-catching", "units": 1, "yield": lambda lvl, c: 0.0, "goods": {}, "depletes": 0.9},
        "moments": [{"when": lambda a, c: a > 0.9 and c.sd in (0, 4), "sign": "rats.gnawed"}],
    },
    "eels": {
        "rule": "Run", "archetype": "run", "depth": "middling",
        "place": lambda l: {"river": 800, "brook": 120}.get(river(l), 0),
        "windows": [(2, 0, 7), (3, 0, 1)], "base": 0.04, "cap": 0.6, "big": 0.15,
        "night": lambda c: ((6.0 if c.D.rising[c.d] and c.D.dark[c.d] else (2.5 if c.D.rising[c.d] else 1.0))
                            * (1.8 if c.D.rising[c.d] and c.d and c.D.dry[c.d - 1] >= 3 else 1.0)
                            * (1.0 if c.D.dark[c.d] else 0.4)),
        "day_moments": [
            {"when": lambda c: in_windows(c.d, RUN_SEASON) and c.D.rain[c.d] >= 4 and c.d and c.D.dry[c.d - 1] >= 3,
             "sign": "sky.rain_after_dry"},
            {"when": lambda c: in_windows(c.d, RUN_SEASON) and c.D.rain[c.d] >= 4 and not (c.d and c.D.dry[c.d - 1] >= 3),
             "sign": "sky.heavy_rain"},
            {"when": lambda c: in_windows(c.d, RUN_SEASON) and c.D.dark[c.d], "sign": "sky.moon_dark"},          # tonight's moon
            {"when": lambda c: in_windows(c.d, RUN_SEASON) and not c.D.dark[c.d], "sign": "sky.moon_bright"},
        ],
        "take": {"act": "eel_traps", "crew_act": "weir_crew", "technique": "eel trapping", "share": 0.4, "crew_share": 0.8,
                 "units": 2, "crew_units": 4, "goods": {"eels": 0.22}, "full_at": 30},
        "answer": {"type": "none"},
        "moments": {"full": "eels.traps_full", "few": "eels.traps_few"},
    },
    "wildfowl": {
        "rule": "Flock", "archetype": "migrant", "depth": "middling",
        "place": lambda l: (150 + 400 * min(fen(l), 3.0)) if fen(l) > 0.5 else (80 if river(l) else 0),
        "windows": [(2, 0, 7), (3, 0, 7), (0, 0, 3)],
        "lead_sign_p": 0.75, "false_sign_p": 0.1, "background_p": 0.3,
        "prepare_act": "set_nets", "prepare_units": 1, "take_act": "fowl", "take_units": 2, "technique": "fowling",
        "rate": {0: 0.01, 1: 0.04, 2: 0.12}, "while_off": 0.3, "goods": {"fowl": 0.2, "feathers": 1}, "restraint": 0.2,
        "answer": {"type": "scared_off", "off_p": 0.4, "off_days": 1},
        "moments": {"lead": "fowl.plovers", "background": "fowl.overhead", "crowded": "fowl.crowded", "weak": "fowl.weak"},
    },
}


# ------------------------------------------------------------------ signs: notice by level, and a reading per level
def _nband(n):
    return "a few" if n <= 4 else ("five or six" if n <= 7 else ("eight or ten" if n <= 11 else "a dozen or more"))


def _scare(f):
    return {"scarecrow": "scarecrow", "children_scare": "children's scaring"}.get(f.get("scare"), f.get("scare"))


def _gap(v, f):
    return v.gap_names[f["gap"]] if "gap" in f else "the field"


ALL = {"novice": 1.0, "systematic": 1.0, "expert": 1.0}

SIGNS = {
    "boar.rooting": {
        "notice": {"novice": 0.6, "systematic": 0.8, "expert": 0.95},
        "read": {
            "novice": lambda v, f: "The turf by the wood's edge is turned over in long strips.",
            "systematic": lambda v, f: (f"Fresh rooting at the wood's edge, the turned earth still dark and wet: {_nband(f['n'])} beasts by "
                                        "the prints." if f["fresh"] else "Old rooting at the wood's edge, the earth dried and crusted."),
            "expert": lambda v, f: (f"Fresh rooting at the wood's edge, last night's: a sounder of about {f['n']}, sows and young; their "
                                    f"trail runs toward {_gap(v, f)}." if f["fresh"] else
                                    "Old rooting at the wood's edge, two or three nights old; nothing has been there since."),
        },
        "facts": {"novice": ("rooting",), "systematic": ("rooting", "fresh", "n"), "expert": ("rooting", "fresh", "n", "gap")},
    },
    "boar.trampled": {
        "notice": ALL,
        "read": {
            "novice": lambda v, f: f"The corn is trampled and rooted at {_gap(v, f)}: a strip of it flattened in the night.",
            "systematic": lambda v, f: f"Boar were in the corn at {_gap(v, f)} in the night, {_nband(f['n'])} of them by the tracks; a strip flattened.",
            "expert": lambda v, f: (f"The sounder of {f['n']} came through {_gap(v, f)} in the night and spoiled about "
                                    f"{max(1, round(100 * f['share']))} in a hundred of the field."),
        },
        "facts": {"novice": ("damage", "gap"), "systematic": ("damage", "gap", "n"), "expert": ("damage", "gap", "n", "share")},
    },
    "deer.slots": {
        "notice": {"novice": 0.5, "systematic": 0.75, "expert": 0.9},
        "read": {
            "novice": lambda v, f: "Deer slots in the soft ground along the hedge.",
            "systematic": lambda v, f: (f"Fresh deer slots along the hedge, a herd of {_nband(f['n'])}." if f["fresh"] else
                                        "Old deer slots along the hedge, rained on."),
            "expert": lambda v, f: (f"Fresh slots of a herd of about {f['n']}, hinds and calves, at the rack through {_gap(v, f)}."
                                    if f["fresh"] else "Old slots along the hedge, from some nights ago."),
        },
        "facts": {"novice": ("slots",), "systematic": ("slots", "fresh", "n"), "expert": ("slots", "fresh", "n", "gap")},
    },
    "deer.grazed": {
        "notice": ALL,
        "read": {
            "novice": lambda v, f: f"Something has grazed and trodden the crop at {_gap(v, f)} in the night.",
            "systematic": lambda v, f: f"Deer were at the crop by {_gap(v, f)} in the night, {_nband(f['n'])} of them.",
            "expert": lambda v, f: f"The herd of {f['n']} came through {_gap(v, f)} and took about {max(1, round(100 * f['share']))} in a hundred.",
        },
        "facts": {"novice": ("damage", "gap"), "systematic": ("damage", "gap", "n"), "expert": ("damage", "gap", "n", "share")},
    },
    "watch.turned": {"notice": ALL, "read": {lv: (lambda v, f: f"The watch at {_gap(v, f)} turned beasts back in the night with the {f['scare']}.")
                                              for lv in ALL}, "facts": {lv: ("turned", "gap", "scare") for lv in ALL}},
    "watch.not_turned": {"notice": ALL, "read": {lv: (lambda v, f: f"The watch at {_gap(v, f)} could not turn them: they came on through "
                                                   f"the {f['scare']} and did damage before they went.") for lv in ALL},
                         "facts": {lv: ("not_turned", "gap", "scare") for lv in ALL}},
    "watch.missed": {"notice": ALL, "read": {lv: (lambda v, f: f"Beasts came in through {_gap(v, f)}; the watch at "
                                               f"{', '.join(v.gap_names[g] for g in f['watched'])} saw nothing.") for lv in ALL},
                     "facts": {lv: ("missed", "gap") for lv in ALL}},
    "hare.nibbled": {"notice": {"novice": 0.6, "systematic": 0.8, "expert": 0.9},
                     "read": {lv: (lambda v, f: "The young corn is nibbled at the field's edge, with hare droppings.") for lv in ALL},
                     "facts": {lv: ("nibbled",) for lv in ALL}},
    "birds.flocks": {"notice": {"novice": 0.8, "systematic": 0.9, "expert": 1.0},
                     "read": {"novice": lambda v, f: "Birds all over the sown strip.",
                              "systematic": lambda v, f: "Woodpigeons and rooks in flocks on the new-sown strip.",
                              "expert": lambda v, f: f"Woodpigeons in flocks on the sown strip, {'more than' if f['level'] > 1.5 else 'about as many as'} usual."},
                     "facts": {"novice": ("birds",), "systematic": ("birds",), "expert": ("birds", "level")}},
    "birds.scare_worked": {"notice": ALL, "read": {lv: (lambda v, f: f"The {_scare(f)} kept the birds off the sown strip yesterday.") for lv in ALL},
                           "facts": {lv: ("birds_kept_off", "scare") for lv in ALL}},
    "birds.scare_failed": {"notice": ALL, "read": {lv: (lambda v, f: f"The birds came down on the sown strip yesterday in spite of the {_scare(f)}.") for lv in ALL},
                           "facts": {lv: ("birds_came", "scare") for lv in ALL}},
    "hare.scare_worked": {"notice": {"novice": 0.7, "systematic": 0.9, "expert": 1.0},
                          "read": {lv: (lambda v, f: f"No fresh hare nibbling on the young corn since the {_scare(f)}.") for lv in ALL},
                          "facts": {lv: ("hares_kept_off", "scare") for lv in ALL}},
    "hare.scare_failed": {"notice": {"novice": 0.7, "systematic": 0.9, "expert": 1.0},
                          "read": {lv: (lambda v, f: f"Fresh hare nibbling on the young corn in spite of the {_scare(f)}.") for lv in ALL},
                          "facts": {lv: ("hares_came", "scare") for lv in ALL}},
    "rats.gnawed": {"notice": {"novice": 0.6, "systematic": 0.8, "expert": 0.95},
                    "read": {"novice": lambda v, f: "Droppings in the granary.",
                             "systematic": lambda v, f: "Droppings and gnawed sacks in the granary.",
                             "expert": lambda v, f: f"Rat runs greasy along the granary wall, sacks gnawed at the bottom: {'more' if f['level'] > 1.2 else 'no more'} than last month."},
                    "facts": {"novice": ("rats",), "systematic": ("rats",), "expert": ("rats", "level")}},
    "sky.rain_after_dry": {"notice": ALL, "read": {lv: (lambda v, f: "Heavy rain today, the first after weeks of dry weather.") for lv in ALL},
                           "facts": {lv: ("rain", "after_dry") for lv in ALL}},
    "sky.heavy_rain": {"notice": ALL, "read": {lv: (lambda v, f: "Heavy rain today.") for lv in ALL}, "facts": {lv: ("rain",) for lv in ALL}},
    "sky.moon_dark": {"notice": ALL, "read": {lv: (lambda v, f: "The moon is near new: tonight will be dark.") for lv in ALL},
                      "facts": {lv: ("dark",) for lv in ALL}},
    "sky.moon_bright": {"notice": ALL, "read": {lv: (lambda v, f: "The moon is up and bright tonight.") for lv in ALL},
                        "facts": {lv: ("bright",) for lv in ALL}},
    "eels.traps_full": {"notice": ALL, "read": {lv: (lambda v, f: f"The eel traps at the weir were full this morning: about {f['n']} eels.") for lv in ALL},
                        "facts": {lv: ("full", "n") for lv in ALL}},
    "eels.traps_few": {"notice": ALL, "read": {lv: (lambda v, f: f"Only {f['n']} eels in the traps this morning.") for lv in ALL},
                       "facts": {lv: ("few", "n") for lv in ALL}},
    "fowl.plovers": {"notice": {"novice": 0.6, "systematic": 0.8, "expert": 0.9},
                     "read": {"novice": lambda v, f: "Birds flying over all day.",
                              "systematic": lambda v, f: "Lines of plovers going west all day, high and fast.",
                              "expert": lambda v, f: "Lines of plovers and redwings going west all day, high and fast, ahead of the cold."},
                     "facts": {"novice": ("birds",), "systematic": ("plovers",), "expert": ("plovers", "cold_ahead")}},
    "fowl.overhead": {"notice": {"novice": 0.8}, "read": {"novice": lambda v, f: "Birds flying over all day."}, "facts": {"novice": ("birds",)}},
    "fowl.crowded": {"notice": ALL, "read": {lv: (lambda v, f: "Hard frost: the fowl crowd on the last open water of the fen and the river.") for lv in ALL},
                     "facts": {lv: ("frost", "crowded") for lv in ALL}},
    "fowl.weak": {"notice": ALL, "read": {lv: (lambda v, f: "The freeze holds: the fowl are weak, slow to fly, some could be picked up.") for lv in ALL},
                  "facts": {lv: ("frost", "weak") for lv in ALL}},
}

# goods: which count as food when taken (each good's quantity in the rows is already in engine food); the rest are materials
GOODS = {"meat": {"food": 1.0}, "fat": {"food": 1.5}, "eels": {"food": 1.0, "keeps": "smoked"}, "fowl": {"food": 1.0},
         "hide": {"use": "bedrolls, tents, packs, harness (built)"}, "pelt": {"use": "trade"}, "antler": {"use": "waits for tools"},
         "feathers": {"use": "bedding; arrows later"}}
FOOD_VALUE = {g: r["food"] for g, r in GOODS.items() if "food" in r}

# acts the household can choose (costs in units of work; children's units for bird-scaring)
ACTS = {
    "watch": {"label": "watch a gap of the field by night, with a scare (fire, clapper, horn or dog)", "units": 2.0, "per": "gap",
              "scares": ("fire", "clapper", "horn", "dog")},
    "hunt_boar": {"label": "hunt the boar in the wood (a crew of two or more; dangerous)", "units": 6.0},
    "stalk_deer": {"label": "stalk the deer in the wood", "units": 3.0},
    "scarecrow": {"label": "keep a scarecrow on the sown field", "units": 0.1},
    "children_scare": {"label": "send the children to scare birds and hares off the sown field all day", "units": 2.0, "who": "children"},
    "snare": {"label": "set snares for hares", "units": 1.0},
    "cats": {"label": "keep cats in the granary (a little food each day)", "units": 0.0},
    "trap_rats": {"label": "trap rats in the granary", "units": 1.0},
    "eel_traps": {"label": "set the eel traps at the weir tonight", "units": 2.0},
    "weir_crew": {"label": "put a crew at the weir tonight to empty the traps through the night", "units": 4.0},
    "set_nets": {"label": "set the fowling nets and decoys (ready the next day)", "units": 1.0},
    "fowl": {"label": "go fowling on the fen and river with the nets", "units": 2.0},
}
