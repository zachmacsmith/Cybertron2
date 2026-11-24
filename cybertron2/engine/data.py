"""The world's data (D4-24: the world grows by rows, not code). Numbers follow the spec where decided and recipes.md (a proposal)
where not, marked "calibrate" in the spec.

ITEMS       good -> {weight, food (meals a unit), spoil (share lost a night in hand), tool (grade), weapon (strength), life (uses
            before a tool or weapon is worn out), seen (noticed when carried), cook (eaten only at a lit hearth), fodder (a beast's
            day of feed a unit)}
CROPS       crop -> {seed (the good sown), gives, share (of the year it grows), hardy, takes and restores (the soil), names}
COVERS      cover -> {words, ground (spaces for buildings a unit of size: D2-154), ambient [(sense, text, salience)]}
RESOURCES   what a parcel can hold -> {renewal (D4-7, D4-103), words by level}
FITTINGS    fitting -> {label, materials, units, needs (another fitting), basic, does, spaces (of floor), holds (a store), heavy (ground floor)}
BLUEPRINTS  building -> {label, materials, units, structure, basic}: the rooms (ROOMS gives their costs by structure) and a camp
ROOMS       room -> {floor, places (lines), by structure: {materials, units, trade}} (D2-154, D2-166)
MONUMENTS, TIERS, LINES, SPACE, STORES   the rest of the building package (review 02zh; D2-154 to D2-171)
TECHNIQUES  name -> {verb, label, aliases, basic, at {covers | fittings | building}, draws (a resource), yield {kind, ...}, tools
            {grade: multiplier} (bare hands: "bare"; absent grade: refused), weapon, wear (a use), inputs, gives, units, tags}
PHYSICS     the numbers of the day and the night
"""
from __future__ import annotations

ITEMS = {
    # the grain ladder, kept under D2-259 (within 1% of FDC SR Legacy, 02zzu_lookup.md): bread is the grain's whole energy at
    # 2,500 kcal a food; boiled whole grain 0.54 and meal or flour 0.77 of it, design factors (D2-60, D4-107); raw grain 0.15 (D2-160)
    "grain": {"weight": 1, "food": 0.7, "spoil": 0.0167, "cook": True, "raw": 0.2, "decay": "grain"},  # boiled whole at a hearth (D2-60); seed (D2-17); spoils
                                                                       # 0.5% a day in a house, less in bins, a cellar, a granary (D2-58)
    "rye": {"weight": 1, "food": 0.7, "spoil": 0.0167, "cook": True, "raw": 0.2, "decay": "grain"},    # winter grain (D2-53)
    "beans": {"weight": 1, "food": 0.6, "spoil": 0.0167, "cook": True, "raw": 0.0, "decay": "grain"},  # legumes: less food, restore the soil (D2-53);
    # kept under D2-259: 0.6 is -20% of FDC's 0.75 on grain's rung (split peas, broad beans), a design factor of about 0.8 (D2-53's "less food")
    "flour": {"weight": 1, "food": 1.0, "spoil": 0.0167, "cook": True, "raw": 0.5, "decay": "grain"},  # mill flour: porridge, and bread (D2-60, D2-167)
    "meal": {"weight": 1, "food": 1.0, "spoil": 0.0167, "cook": True, "raw": 0.5, "decay": "grain"},   # hand-ground: porridge only, no bread (D2-167)
    "bread": {"weight": 1.4, "food": 1.3, "spoil": 0.05, "decay": "bread"},                # keeps, eaten without a hearth (D2-60)
    "dried meat": {"weight": 1, "food": 1.2, "spoil": 0.02, "decay": "dried meat"},           # meat dried to half its weight (D2-62): 2 x meat (D2-258)
    "cheese": {"weight": 1, "food": 1.61, "spoil": 0.02, "decay": "cheese"},              # 6 milk (D2-47, D2-56); a kg of hard cheese, FDC 403 kcal (D2-258)
    "salt": {"weight": 1, "food": 0.0, "spoil": 0.0},                  # D2-24, D2-56
    "hay": {"weight": 10, "food": 0.0, "spoil": 0.0, "fodder": 1.0},   # cut from pasture in summer (D4-42); 10 kg, a beast's day (D2-288)
    # A crop reaped green (D4-106): little food (the green ears roasted), good fodder; heats and spoils unless dried to hay
    # 0.24: no FDC figure for an immature cereal; 02zzu's estimate (40 to 90 kcal a 100 g) (D2-258)
    "green grain": {"pack": "farming", "weight": 1, "food": 0.24, "spoil": 0.2, "fodder": 0.8, "decay": "green crop"},
    "green rye": {"pack": "farming", "weight": 1, "food": 0.24, "spoil": 0.2, "fodder": 0.8, "decay": "green crop"},
    # green beans kept under D2-259 (-12% of FDC's young broad beans in the pod)
    "green beans": {"pack": "farming", "weight": 1, "food": 0.3, "spoil": 0.2, "fodder": 0.6, "decay": "green crop"},
    "straw": {"weight": 16, "food": 0.0, "spoil": 0.0, "fodder": 1.0},  # from the grain harvest (D4-42); a 16 kg truss (D2-288)
    "dung": {"weight": 1, "food": 0.0, "spoil": 0.0},                  # manure (D2-18, D4-39)
    "charcoal": {"weight": 20, "food": 0.0, "spoil": 0.0, "heat": 2.0},  # a 20 kg sack from 5 timber (D2-56, D2-288); heat by mass,
                                                                        # 29 MJ a kg against wood's 15 (wave1 §1.3; was 6)
    "firewood": {"weight": 10, "food": 0.0, "spoil": 0.0, "heat": 0.5},  # a 10 kg bundle of dead wood or young growth (D2-157, D2-288)
    "wild food": {"weight": 1, "food": 0.41, "spoil": 0.15},       # the legacy forage's mix: 02zzu's autumn mix on the checked values (D2-258)
    # fishing and salt (D4-103's acceptance test; content: proposals/water_and_preservation.md, calibrate)
    # fish: a unit is 1,150 kcal of flesh, about 1 kg gutted and headed (an eel's 0.63 kg, a pike's 1.3; 02zzu, D2-258); raw at the
    # game's raw/cooked 0.6 (fire matters: a design factor, kept)
    "fish": {"pack": "water", "weight": 1, "food": 0.46, "spoil": 0.30, "cook": True, "raw": 0.28, "decay": "fresh fish"},   # fresh: spoils as meat does
    "salt fish": {"pack": "water", "weight": 1, "food": 0.46, "spoil": 0.01, "cook": True, "raw": 0.28, "decay": "dried meat"},   # keeps for months
    "fishing rod": {"pack": "water", "weight": 0.8, "food": 0.0, "spoil": 0.0, "life": 30, "seen": True},              # a rod, a line of hair or gut
    # the smokehouse (brief 5 §4a; calibrate): a batch curing on its racks (as meat drying on a hearth's rack), then smoked: half the
    # weight, the same food, keeping four times as long as dried meat
    "smoking fish": {"pack": "water", "weight": 1, "food": 0.46, "spoil": 0.15, "cook": True, "raw": 0.28, "decay": "drying meat"},
    "smoked fish": {"pack": "water", "weight": 1, "food": 0.92, "spoil": 0.005, "decay": "dried meat"},   # 2 x fish (D2-258)
    # fish on a hearth's rack (D4-122): hung in the house's smoke as meat is, dried to half the weight; keeps as dried meat (calibrate)
    "drying fish": {"pack": "water", "weight": 1, "food": 0.46, "spoil": 0.15, "cook": True, "raw": 0.28, "decay": "drying meat"},
    "dried fish": {"pack": "water", "weight": 1, "food": 0.92, "spoil": 0.02, "decay": "dried meat"},   # 2 x fish (D2-258)
    # meat: a unit is 1,500 kcal of what is eaten (1.25 kg of venison, 0.76 kg of beef; 02zzu, D2-258); raw at the game's raw/cooked
    # 0.53 (fire matters: a design factor, kept)
    "meat": {"weight": 1, "food": 0.6, "spoil": 0.30, "cook": True, "raw": 0.32, "decay": "fresh meat"},                # dense, spoils fresh (D2-41)
    "milk": {"weight": 1, "food": 0.256, "spoil": 1.0},                # the same day (D2-42); a kg, FDC 64 kcal (D2-258)
    "hen": {"weight": 2, "food": 0.0, "spoil": 0.0, "pack": ["wild", "farming"]},
    "cat": {"weight": 3.5, "food": 0.0, "spoil": 0.0, "pack": "wild"},   # a cat in a store keeps the mice down (D2-206; brief 2 K1)   # kept hens in a house's store: they lay (wild_layer.md, wave 2)
    # a kg of eggs in shell (wild.EGG_KG an egg, D2-258): 0.6 kept under D2-259 (+19% of FDC's 0.50, borderline)
    "egg": {"weight": 1, "food": 0.6, "spoil": 0.05, "cook": True, "raw": 0.5, "pack": "wild"},
    # wild plants' goods (wild_plants.md §2, D2-200): fresh ones spoil fast, nuts keep for months; acorns are bitter until leached
    # the wild plants: a kg as gathered (in shell, unleached), on FDC SR Legacy (02zzu_lookup.md, D2-258); the raw values at the
    # game's raw/cooked ratio (a design factor, kept)
    "greens": {"weight": 1, "food": 0.098, "spoil": 0.3, "pack": "wild"},                                     # nettles and dock, 22 to 42 kcal
    "roots": {"weight": 1, "food": 0.263, "spoil": 0.05, "cook": True, "raw": 0.13, "pack": "wild"},          # on SR proxies (parsnip, burdock, salsify)
    "mushrooms": {"weight": 1, "food": 0.107, "spoil": 0.3, "cook": True, "raw": 0.053, "pack": "wild"},
    "watercress": {"weight": 1, "food": 0.041, "spoil": 0.3, "pack": "wild"},                                 # 11 kcal: water
    "samphire": {"weight": 1, "food": 0.061, "spoil": 0.2, "cook": True, "raw": 0.049, "pack": "wild"},       # on an SR proxy (purslane)
    "berries": {"weight": 1, "food": 0.167, "spoil": 0.25, "pack": "wild"},
    "hedge fruit": {"weight": 1, "food": 0.33, "spoil": 0.03, "cook": True, "raw": 0.165, "pack": "wild"},
    "hazel nuts": {"weight": 1, "food": 1.03, "spoil": 0.004, "pack": "wild"},                                # in shell: the kernel 0.41
    "beech nuts": {"weight": 1, "food": 1.2, "spoil": 0.006, "pack": "wild"},                                 # kept: -15% of FDC's 1.41
    # raw acorns: FDC's 0.96 x 0.035, a design factor for the tannin (inedible unleached), so leaching is the way in (02zzu)
    "acorns": {"weight": 1, "food": 0.034, "spoil": 0.01, "pack": "wild"},
    "acorn meal": {"weight": 1, "food": 1.0, "spoil": 0.02, "cook": True, "raw": 0.3, "pack": "wild"},       # kept: -18% of 1.22 (borderline)
    "antler": {"weight": 1.5, "food": 0.0, "spoil": 0.0, "pack": "wild"},   # a cast antler: horn for handles and combs
    "beaver pelt": {"weight": 0.7, "food": 0.0, "spoil": 0.0, "pack": "wild"},   # a fine fur for trade
    "clappers": {"weight": 0.5, "food": 0.0, "spoil": 0.0, "pack": "wild"},
    "horn": {"weight": 0.5, "food": 0.0, "spoil": 0.0, "pack": "wild"},
    "castoreum": {"weight": 0.2, "food": 0.0, "spoil": 0.0, "pack": "wild"},   # the beaver's scent glands: a physician's good
    "timber": {"weight": 25, "food": 0.0, "spoil": 0.0, "heat": 1.25},  # a 25 kg pole or hewn length (D2-288, D2-303); heat by mass
                                                                        # as firewood (wave1 §1.3; was 2 at "240 kg")
    "stone": {"weight": 25, "food": 0.0, "spoil": 0.0},                # a 25 kg building stone (D2-288; was 3)
    "withies": {"weight": 10, "food": 0.0, "spoil": 0.0085},            # a 10 kg bundle of green rods (D2-288; u3 §1.1: a quarter lost
                                                                        # by about 34 nights on the keeping curve, D2-289)
    "hide": {"weight": 3, "food": 0.0, "spoil": 0.0, "decay": "hide"},                  # a red deer's, dried (wave1 §1.5; D2-24)
    "tallow": {"weight": 1, "food": 0.0, "spoil": 0.0},                                  # a beast's fat, rendered or not (brief 3 §5);
    # food 0 against FDC's 3.6 a kg: a design choice, the lights' good (02zzu choice 6; whether it is famine food is for Zach)
    "drying meat": {"weight": 1, "food": 0.6, "spoil": 0.15, "cook": True, "raw": 0.32, "decay": "drying meat"},  # on a rack: the flies
    "salt meat": {"weight": 1, "food": 0.57, "spoil": 0.003, "cook": True, "raw": 0.24, "decay": "dried meat"},   # keeps for months; 0.95 x meat
    "smoking meat": {"weight": 1, "food": 0.6, "spoil": 0.15, "cook": True, "raw": 0.32, "decay": "drying meat"},  # brief 5 §4a
    "smoked meat": {"weight": 1, "food": 1.2, "spoil": 0.005, "decay": "dried meat"},                             # brief 5 §4a; 2 x meat
    "offal": {"weight": 1, "food": 0.0, "spoil": 0.0},                                   # what is left in a carcass taken from: the
                                                                                          # night's rot by its size (night.py, brief 3 §2)
    "tallow light": {"weight": 0.2, "food": 0.0, "spoil": 0.0},                          # a rush or rag dipped in tallow: night work by it
    "copper ore": {"weight": 3, "food": 0.0, "spoil": 0.0},
    "copper": {"weight": 1, "food": 0.0, "spoil": 0.0},                # D2-19, D2-24
    "coin": {"weight": 0, "food": 0.0, "spoil": 0.0},                  # copper coin, carried (D2-1, D2-28)
    "crude tool": {"weight": 1.5, "food": 0.0, "spoil": 0.0, "tool": "crude", "life": 10, "seen": True},      # D2-23; recipes.md §6
    "copper tool": {"weight": 1.5, "food": 0.0, "spoil": 0.0, "tool": "copper", "life": 40, "seen": True},
    "crude weapon": {"weight": 1.5, "food": 0.0, "spoil": 0.0, "weapon": 2.0, "life": 10, "seen": True},     # D2-46: about 3 fights
    "pack": {"weight": 2, "food": 0.0, "spoil": 0.0, "carry": 15, "seen": True},      # read as the withy pack basket: +15 kg (D2-281;
                                                                                       # basis §5; u3 §2.3: the pack's own rows stage 2)
    "handcart": {"weight": 0, "food": 0.0, "spoil": 0.0, "carry": 115, "track": True, "seen": True},   # 125 kg in all on a track
                                                                       # (basis §5: 100 to 150); its own 40 kg borne on its wheels
    "wooden plough": {"pack": "farming", "weight": 25, "food": 0.0, "spoil": 0.0, "life": 60, "seen": True},       # D2-23; recipes.md §2 (60 plots)
    "harness": {"weight": 12, "food": 0.0, "spoil": 0.0, "life": 80, "seen": True},             # D2-23; 80 days' use
    "bedroll": {"weight": 3, "food": 0.0, "spoil": 0.0, "life": 40, "seen": True, "camp": "bedroll"},    # D2-68: about 40 nights
    "tent": {"weight": 18, "food": 0.0, "spoil": 0.0, "life": 30, "seen": True, "camp": "tent"},          # D2-68: sleeps 2
    "rotting meat": {"weight": 1, "food": 0.0, "spoil": 0.3, "rot": True},  # what fresh meat becomes in the open (D2-87); signs, no health yet
}

# The cured depths as goods of their own (D2-295; u4 §3): food a kg conserved through the weight each loses; their processes are u4's
# (stage 3). Hard-cured meat keeps the salt meat's food: 0.57 / 0.85 = 0.67 a kg (salt meat is 0.57; u4, B10 as corrected).
ITEMS.update({
    "hot-smoked fish": {"pack": "water", "weight": 1, "food": 0.69, "spoil": 0.0, "decay": "dried meat"},    # 1 kg from 1.5 fresh
    "hard-cured fish": {"pack": "water", "weight": 1, "food": 1.15, "spoil": 0.0, "decay": "dried meat"},    # from 2.5 kg fresh, salted
    "hot-smoked meat": {"weight": 1, "food": 0.9, "spoil": 0.0, "decay": "dried meat"},
    "hard-cured meat": {"weight": 1, "food": 0.67, "spoil": 0.0, "decay": "dried meat"},                       # bacon, ham
})
# The wave's made gear and its materials in real kilograms (u3 §2.2, §10; the gear unit, engine/gear.py, D2-244)
from cybertron2.engine import gear as _GEAR                             # noqa: E402
_GEAR.register_items(ITEMS)
from cybertron2.engine import process as _PROC_I                        # noqa: E402
_PROC_I.register_items(ITEMS)
from cybertron2.engine import stores as _STORES_I                      # noqa: E402
_STORES_I.register_items(ITEMS)
# The keeping curve (D2-289; basis §3; wave1 §2.2): a food that keeps d real days well kept loses about a quarter by
# nights = min(d, 2) + (d - 2) / 11.4, so its base rate a night (`spoil`: well kept, D2-272) is 1 - 0.75 ** (1 / nights). The real
# days are wave1 §2.2's. A lot in the smoke or at the hearth spoils at 0.12 out of it, 0.03 in it (DECAY smoke 0.25; basis §3).
KEEP_DAYS = {
    "fish": 1.5, "offal": 1, "meat": 3, "green grain": 1.5, "green rye": 1.5, "green beans": 1.5, "greens": 2,
    "watercress": 2, "mushrooms": 2, "berries": 2, "samphire": 4, "hot-smoked fish": 7, "hot-smoked meat": 7, "bread": 5,
    "wild food": 14, "egg": 30, "hedge fruit": 30, "roots": 60, "flour": 90, "meal": 90, "smoked fish": 90, "smoked meat": 90,
    "cheese": 120, "acorn meal": 120, "beech nuts": 120, "acorns": 180, "hard-cured fish": 270, "salt fish": 365, "salt meat": 365,
    "hard-cured meat": 365, "hazel nuts": 365, "tallow": 365, "hide": 365, "withies": 365, "dried fish": 450, "dried meat": 450,
    "grain": 2500, "rye": 2500, "beans": 2500, "hay": 4900, "straw": 4900,
}
# A lot waiting in a container (u4 §3, §5): off its fire it keeps as its input (fresh fish 0.175, meat 0.129); in the smoke or at the
# hearth at its row's in-process base, 0.03 a night (process.PROCESSES `in_rate`; wave1 §2.2, est.)
IN_PROCESS_OF = {"smoking fish": "fish", "drying fish": "fish", "smoking meat": "meat", "drying meat": "meat"}


def keep_nights(d) -> float:
    """The keeping curve (D2-289): real days kept to nights, the first two whole, the rest at the calendar's 1/11.4."""
    return min(float(d), 2.0) + max(0.0, float(d) - 2.0) / 11.4


# "Keeps for d days" against "goes off after d days" (D2-336): a preserved good keeps for its days, about a quarter lost by then
# (D2-289); a fresh, perishable food goes off after its days, about half gone by then, so fresh fish and meat go off within a few
# nights as before the rebuild. GOES_OFF names the perishables.
GOES_OFF = {"fish", "offal", "meat", "green grain", "green rye", "green beans", "greens", "watercress", "mushrooms", "berries",
            "samphire", "bread", "hot-smoked fish", "hot-smoked meat"}


def base_spoil(d, goes_off=False) -> float:
    """A night's base rate from the curve's nights: a quarter lost by then for what keeps (D2-289), half for what goes off
    (D2-336)."""
    return round(1.0 - (0.5 if goes_off else 0.75) ** (1.0 / keep_nights(d)), 4)


for _i, _d in KEEP_DAYS.items():
    ITEMS[_i]["spoil"] = base_spoil(_d, _i in GOES_OFF)
# Milk is not on the curve: it is gone the same day (D2-273's floor, "milk the same day"; D2-42), its row's 1.0 kept.
for _i, _of in IN_PROCESS_OF.items():
    ITEMS[_i]["spoil"] = ITEMS[_of]["spoil"]

# Decay by condition (economy/goods.md "Decay", D2-87; calibrate): multipliers on an item's rate in a house, for a thing at a spot
# (open, dry or wet; buried), and for the season and the frost; `abs` is a share lost a day where the house rate is none (hides);
# `becomes` is what the lost share turns into in the open.
DECAY = {
    "green crop": {"open_dry": 1.0, "open_wet": 3, "buried": 2, "warm": 1.5, "frozen": 0.2},          # heats in a heap, wet (D4-106)
    "grain": {"open_dry": 4, "open_wet": 10, "buried": 2, "warm": 1.2, "frozen": 0.5},
    "bread": {"open_dry": 3, "open_wet": 8, "buried": 3, "warm": 1.5, "frozen": 0.2},
    "fresh meat": {"open_dry": 2, "open_wet": 2.5, "buried": 1, "warm": 1.5, "frozen": 0.1, "becomes": "rotting meat"},
    "dried meat": {"open_dry": 2, "open_wet": 6, "buried": 2, "warm": 1.2, "frozen": 0.5},
    "drying meat": {"open_dry": 1.0, "open_wet": 3.0, "buried": 1, "warm": 1.5, "frozen": 0.2},   # a lot waiting: its in-process base is u4's row (process.decay)
    "cheese": {"open_dry": 3, "open_wet": 5, "buried": 1, "warm": 1.5, "frozen": 0.3},
    "hide": {"abs": {"open_dry": 0.01, "open_wet": 0.03, "buried": 0.02}},
    "fresh fish": {"open_dry": 2, "open_wet": 2.5, "buried": 1, "warm": 1.5, "frozen": 0.1},       # as fresh meat; its base already
                                                                          # holds D2-212's faster store (wave1 §2.3: the x2 dropped)
    "default": {"open_dry": 2, "open_wet": 4, "buried": 1, "warm": 1.2, "frozen": 0.5},   # goods the table does not name (37.4; calibrate)
}

# Crops (D2-53, D4-38, D4-39; 02l §2-§3, calibrate). Since D4-106 (proposals/crop_growth.md): a crop grows by its `growth` rate in
# each season, `share` of the year at full rate; what it gives is scaled by the mean rate it grew at; a tender crop loses a share
# to each winter or cold night; sown seed lies until the season lets it come up, and is lost a little each night meanwhile;
# winter grain that meets no winter gives `needs_winter` of a crop. Reaped before it is ripe, a crop gives its `green` good.
# Before D4-106: grow for a share of the year from the day sown; the cold kills what is still
# growing unless it is hardy; each takes from the soil and restores it toward a level.
CROPS = {
    "grain": {"pack": "farming", "seed": "grain", "gives": "grain", "share": 0.25, "growth": {"spring": 1.0, "summer": 1.0, "autumn": 0.5, "winter": 0.0},
              "green": "green grain", "yield": 1.0, "hardy": False, "takes": 0.15, "restores": [0.10, 1.0], "straw": True,
              "names": ["barley", "oats", "wheat", "grain"]},
    "winter grain": {"pack": "farming", "seed": "rye", "gives": "rye", "share": 0.33, "growth": {"spring": 1.0, "summer": 1.0, "autumn": 0.6, "winter": 0.1},
                     "needs_winter": 0.4, "green": "green rye", "yield": 1.0, "hardy": True, "takes": 0.15, "restores": [0.10, 1.0], "straw": True,
                     "names": ["rye", "winter grain"]},
    "legumes": {"pack": "farming", "seed": "beans", "gives": "beans", "share": 0.17, "growth": {"spring": 0.8, "summer": 1.0, "autumn": 0.4, "winter": 0.0},
                "green": "green beans", "yield": 0.6, "hardy": False, "takes": 0.0, "restores": [0.40, 1.0], "straw": False,
                "names": ["beans", "peas", "legumes"]},
    # flax (u3 §1.2, §1.3; D2-264): sown in a strip of a holding (up to a quarter of a plot, B35) or as a whole plot's crop; pulled,
    # not reaped (engine/strips.py); its straw (kg) for retting and spinning, its seed rippled from it
    "flax": {"pack": "farming", "seed": "flax seed", "gives": "flax", "share": 0.27, "growth": {"spring": 1.0, "summer": 1.0, "autumn": 0.5, "winter": 0.0},
             "green": "flax", "yield": 5.5, "hardy": False, "takes": 0.15, "restores": [0.10, 1.0], "straw": False, "strip": 0.25,
             "seed_kg": 11, "names": ["flax", "linseed"]},
}
CROP_OF = {n: c for c, d in CROPS.items() for n in d["names"]}
TURF = ["meadow", "pasture", "heath", "scrub"]     # ground with turf: seed thrown on it takes poorly (D4-106: PHYSICS farming turf)

# Lore (D4-105): what a family knows from long practice and is never told by the rules: seeded as lines kept for good (D4-64) to
# those it fits, passed on as kept lines are. `to`: "farmers" (the adults of a household, or a person, holding a field). The text
# is made from the data (lore.py). A world turns one off with `lore: {sowing: false}`.
LORE = {"sowing": {"to": "farmers", "pack": "farming"}}
SEED_CROP = {d["seed"]: c for c, d in CROPS.items()}
EDIBLE = tuple(i for i, v in ITEMS.items() if v["food"] > 0)
TOOLS = tuple(sorted((i for i, v in ITEMS.items() if v.get("tool")), key=lambda i: -("crude", "copper").index(ITEMS[i]["tool"])))
WEAPONS = tuple(i for i, v in ITEMS.items() if v.get("weapon"))

COVERS = {
    "forest": {"words": "woodland", "ground": 0, "sight": 0.35, "sound": 0.7, "dig": "soft",
               "ambient": [("sound", "birdsong and the creak of trees from {name}", 0.2), ("smell", "leaf mould on the air from {name}", 0.15)]},
    "field": {"words": "fields", "ground": 0, "sight": 1.0, "sound": 1.0, "dig": "soft", "ambient": [("sight", "{name} stretching out beyond the houses", 0.1)]},
    "pasture": {"words": "pasture", "ground": 0, "sight": 1.0, "sound": 1.0, "dig": "soft",
                "ambient": [("sound", "cattle lowing on {name}", 0.35), ("smell", "dung and trodden grass from {name}", 0.15)]},
    "meadow": {"words": "meadow", "ground": 0, "sight": 1.0, "sound": 1.0, "dig": "soft", "ambient": [("sound", "insects in the long grass of {name}", 0.15)]},
    "water": {"words": "water", "ground": 0, "sight": 1.0, "sound": 1.0, "dig": "soft", "ambient": [("sound", "water running over stones in {name}", 0.3)]},
    "built": {"words": "built ground", "ground": 24, "sight": 0.7, "sound": 1.0, "dig": "soft", "ambient": [("sound", "voices and work about the houses", 0.2)]},
    "scrub": {"words": "scrub", "ground": 16, "sight": 0.5, "sound": 0.9, "dig": "stony", "ambient": []},
    "rock": {"words": "rock", "ground": 0, "sight": 0.5, "sound": 0.9, "dig": "stony", "ambient": [("sound", "the ring of picks from {name}", 0.25)]},
    # D2-185: heath, moor, fen and saltmarsh as covers (the landscape generator's waste land); their own crafts and changes come later
    "heath": {"words": "heath", "ground": 0, "sight": 0.8, "sound": 1.0, "dig": "soft", "ambient": [("smell", "warm gorse on the air from {name}", 0.12)]},
    "moor": {"words": "moor", "ground": 0, "sight": 0.9, "sound": 1.0, "dig": "soft", "ambient": [("sound", "curlews calling over {name}", 0.15)]},
    "fen": {"words": "fen", "ground": 0, "sight": 0.6, "sound": 1.0, "dig": "soft", "ambient": [("sound", "reeds hissing in the wind on {name}", 0.15)]},
    "saltmarsh": {"words": "saltmarsh", "ground": 0, "sight": 1.0, "sound": 1.0, "dig": "soft", "ambient": [("smell", "salt mud from {name}", 0.15)]},
}

# How each resource comes back (D4-7) and how it is seen (in words, never numbers: environment/resources.md).
RESOURCES = {
    "plants": {"renewal": "fast", "low": "{name} has been picked over: little wild food left", "high": "{name} is thick with berries, nuts and greens"},
    "game": {"renewal": "threshold", "off_with": ["wild"], "low": "few fresh tracks in {name}: the game is thin", "high": "fresh deer slots and droppings along the rides of {name}",
             # a spec counts its game in the old meat unit (1.5 food, 3,750 kcal): its K and S are x 2.5 into the meat unit (0.6 food)
             # when the world is built (D2-261), so the hand-made specs, the makers and the generator keep their woods' food unedited
             "spec_unit": 2.5},
    "wood": {"renewal": "slow", "low": "{name} is thinned out: stumps where the big trees stood", "high": "",     # the trees (D2-156)
             "spec_unit": 9.6},                                         # a world file's old 240 kg timber in 25 kg ones (D2-288)
    "young": {"renewal": "young", "low": "", "high": "", "spec_unit": 6.0},   # young growth: cut for firewood (D2-156); old 60 kg
    "dead": {"renewal": "dead", "low": "", "high": "", "spec_unit": 6.0},     # dead wood: gathered for firewood (D2-156)
    "seam": {"renewal": "finite", "low": "the seam at {name} is nearly worked out", "high": "a green-stained seam in {name}"},
    "quarry": {"renewal": "endless", "low": "", "high": "a face of good stone at {name}"},
    "grass": {"renewal": "fast", "low": "{name} is grazed bare", "high": "good grass on {name}"},             # D4-45
    # fish in a water parcel (D4-103; water_and_preservation.md §3): resident fish regrow; a river's run comes in its seasons
    "fish": {"pack": "water", "renewal": "periodic", "low": "the water at {name} is quiet: few fish rising", "high": "fish rising all along {name}"},
    # the shallows of a water or fen parcel (u1 §2; D2-317): small fish, crayfish and yellow eels at the edge, one stock a parcel; its
    # signs are its own rows (signs.WILD)
    "shallows": {"pack": "water", "renewal": "shallows", "low": "", "high": ""},
    # wild willow's rods on fen and bank parcels (u3 §1.1): cut as withies
    "willow": {"renewal": "willow", "low": "", "high": ""},
    "salt": {"pack": "water", "renewal": "endless", "low": "", "high": "white crusts of salt drying in the pans at {name}"},   # a saltmarsh's pans
    "brine": {"pack": "water", "renewal": "endless", "low": "", "high": "a spring at {name} whose water tastes of salt"},   # a brine spring (brief 5 §4b)
    "dung": {"renewal": "accrues", "low": "", "high": "dung lies thick where the beasts have been on {name}"},
}
# the wild kinds (wild_layer.md §3.2, D2-199): RESOURCES rows with population fields, in the `wild` pack; one registry
from cybertron2.wild import kinds as _WILD_KINDS                       # noqa: E402
RESOURCES.update(_WILD_KINDS.rows())
from cybertron2.wild import plants as _WILD_PLANTS                     # noqa: E402
RESOURCES.update({k: {"renewal": "seasonal", "pack": "wild", "plant": True, "low": f"{{name}} has been picked over: few {v['words']} left",
                      "high": f"{{name}} is thick with {v['words']}"} for k, v in _WILD_PLANTS.PLANTS.items()})   # wild plants (D2-200)

# Forests (environment/resources.md "Forests", D2-156): three stocks a unit of size, as timber (trees) and firewood (young growth,
# dead wood); yearly rates. A world file gives `wood: {kind, ...}` on a forest or scrub parcel; an older world's `wood` stock is
# read as its trees, with young growth and dead wood in a copse's proportions.
FORESTS = {
    "kinds": {
        # in the handling units (D2-288): the trees' timber x 9.6 of the count at the old 240 kg reading, young growth and dead wood
        # x 6 of the old 60 kg firewood (wave1 §1.8); a world file's counts are in the old units (RESOURCES spec_unit)
        "old forest": {"trees": 24000, "young": 300, "dead": 1800, "grow": 0.005, "regrow": 0.5},
        "managed wood": {"trees": 5760, "young": 2400, "dead": 600, "grow": 0.01, "regrow": 1.0},
        "copse": {"trees": 2880, "young": 240, "dead": 300, "grow": 0.01, "regrow": 0.6},
        "scrub": {"trees": 0, "young": 360, "dead": 60, "grow": 0.0, "regrow": 0.6},
    },
    "shed": 0.01,                  # of the trees' timber a year, as dead wood
    "per_timber": 2.5,             # firewood to a timber's mass (10 kg bundles to a 25 kg timber; was 4 at 60 and 240)
    "rot": 0.3,                    # of the dead wood a year
    "brash": 0.625,                # firewood left as dead wood for each timber felled: a quarter of its mass, as before
    "scrub_below": 0.4,            # under this share of its trees a forest's cover is scrub
    "gale": 0.002,                 # of the trees thrown in a gale (as dead wood: a windfall, D2-79)
}

CLEARING = {"meadow": 6.0, "pasture": 6.0, "scrub": 10.0,      # units of work a unit of size to make it a field (calibrate)
            "fertility": {"meadow": 1.1, "pasture": 1.0, "scrub": 0.85},   # what the new field starts at, unless the land says
            # clearing for building (02zh §8; proposed, calibrate): units a unit of size to make it built ground; farmland stops being
            # farmland; a wood must be felled to scrub first, and grubbing its roots out is the dearer work
            "built": {"field": 4.0, "pasture": 4.0, "meadow": 4.0, "scrub": 10.0}}

# Fittings and blueprints: recipes.md §3 (a proposal; calibrate). A building is its structure, its rooms and its fittings (D2-9).
# Every fitting takes floor (`spaces`; `per`: so many a bed or a stall), a store holds so much (`holds`: {kind: qty} a fitting, or
# `by`: a space of the building's footprint, or of the fitting's own floor); `heavy` ones stand on the ground floor (02zh §2); a
# woodshed is a lean-to taking `ground` from the parcel; a vault is a stone room of its own (`room`: its floor, on the ground floor).
# Spaces: D2-154 (decided; calibrate); stores: D2-155; the cellar's cost D2-155; beds, stalls, woodshed, vault: proposed (02zh §4);
# the water wheel's cost D2-166.
FITTINGS = {
    "beds": {"label": "beds", "materials": {"timber": 1, "straw": 1}, "units": 1, "per": "bed", "basic": True, "spaces": 1,
             "does": "housed when sleeping here, one a bed"},                                                  # D2-56; 02zh §4 (proposed)
    "hearth": {"label": "a hearth", "materials": {"stone": 20}, "units": 3, "basic": False, "trade": "mason", "fire": True, "spaces": 1,
               "does": "warmth (burns timber), porridge and baking"},
    "owl hole": {"label": "an owl hole (a gap left high in a barn's gable)", "materials": {"timber": 0.1}, "units": 1, "basic": True,
                 "spaces": 0, "pack": "wild", "does": "a way in for a barn owl, which keeps the mice in the store down"},   # brief 2 K1
    "bins": {"label": "bins", "materials": {"timber": 3}, "units": 1, "basic": True, "does": "a store for dry goods (300 kg), off the damp floor",
             "spaces": 1, "holds": {"food": 60}},
    "hand mill": {"label": "a hand mill", "materials": {"stone": 2}, "units": 2, "basic": True, "spaces": 1,
                  "does": "grinding grain by hand into meal (porridge, not bread)", "aliases": ["quern"]},          # D2-61, D2-167
    "granary": {"label": "a granary floor", "materials": {"timber": 20}, "units": 4, "basic": True, "spaces": 3,
                "holds": {"grain": 300}, "does": "grain, rye and beans raised and dry, off the damp (400 kg a space)"},                         # D2-58, D2-155
    "fire ring": {"label": "a fire ring", "materials": {"stone": 4}, "units": 1, "basic": True, "fire": True, "spaces": 1,
                  "does": "a fire in the open for warmth and cooking (burns timber)"},                              # D2-68: a camp's fire
    "oven": {"label": "a stone oven", "materials": {"stone": 60, "timber": 0.4}, "units": 12, "basic": False, "trade": "mason", "spaces": 2,
             "structure": "stone",                                                 # only in a stone building (D4-97)
             "wear": {"life": 10, "count": "act", "mend": "reline oven"},           # firings; then half a batch (D4-103 phase 2)
             "does": "baking bread in batches"},                                                             # D2-60
    "anvil": {"label": "an anvil and bellows", "materials": {"stone": 4, "hide": 2, "timber": 0.4}, "units": 4, "needs": "hearth",
              "basic": False, "trade": "smith", "spaces": 2, "heavy": True, "does": "a smithy: smelting and smithing"},
    "cellar": {"label": "a cellar", "materials": {"timber": 9}, "units": 6, "basic": False, "trade": "mason", "spaces": 0,
               "heavy": True, "holds": {"food": 40}, "by": "footprint",
               "does": "food kept cool below the floor, out of the summer's heat and the frost (30 kg a space of the building's ground); grain, meal and salt take its damp"},          # D2-45, D2-155
    "millstones": {"label": "dressed millstones", "materials": {"stone": 60}, "units": 10, "basic": False, "trade": "mason", "spaces": 3,
                   "heavy": True, "wear": {"life": 2000, "count": "inputs", "mend": "dress millstones"},  # grain ground, by an ox or the river (D4-105)
                   "does": "an ox mill: an ox turns them (D2-61)"},
    "water wheel": {"label": "a water wheel and leat", "materials": {"timber": 300, "stone": 140, "copper": 2}, "units": 250,
                    "needs": "millstones", "site": "water", "basic": False, "trade": "carpenter", "spaces": 0, "heavy": True,
                    "wear": {"years": 1.0, "mend": "clear the leat"},                   # silts in a year; then half as much (D4-105)
                    "does": "a water mill: the river turns the millstones (D2-61); where fish run the river, its hatches (the gap) "
                            "are set shut (full grinding, the fish held back) or open (half, the fish let past)"},                                  # D2-166
    "stalls": {"label": "stalls", "materials": {"timber": 2}, "units": 1, "per": "stall", "basic": True, "spaces": 2, "heavy": True,
               "fodder": 0.8, "dung": 1.5,
               "does": "beasts housed in winter, one a stall: less fodder, dung kept, not driven off without coming in"},   # D2-45
    "woodshed": {"label": "a woodshed", "materials": {"timber": 20, "straw": 15}, "units": 1, "basic": True, "spaces": 0, "ground": 2,
                 "holds": {"timber": 9600}, "does": "a lean-to against the building: about 9,600 kg of timber and firewood kept dry"},   # in kg (storage §3.13)
    # brief 5 §4a: a smokehouse is a building of its own (`apart`: no beds or hearth in it) with smoke racks, sets of 250 kg on a
    # space each, the building capping the sets (u4 §4; D2-284, D2-291; process.FITTINGS). Brief 5 §4b: a brine pan over a furnace at or beside a brine spring (`spring`), boiling
    # salt; it wears like other fittings (calibrate)
    "smoke racks": {"label": "smoke racks (hurdles over a smouldering fire)", "materials": {"withies": 2, "timber": 2}, "units": 2, "basic": True,
                    "spaces": 1, "apart": True, "aliases": ["smokehouse racks", "smoking racks"]},   # u4's fields: process.FITTINGS
    "brine pan": {"label": "a brine pan (a shallow pan over a furnace, for boiling salt)", "materials": {"copper": 10, "stone": 4},
                  "units": 4, "basic": False, "trade": "salter", "spaces": 2, "heavy": True, "spring": "brine",
                  "aliases": ["salt pan", "lead pan", "salt boiling pan"],
                  "wear": {"life": 60, "count": "act", "mend": "mend the brine pan"},     # boilings; then half (D4-103 phase 2)
                  "does": "boiling brine from the spring beside it into salt (about 1 firewood a salt)"},
    "vault": {"label": "a vault", "materials": {"stone": 3000}, "units": 30, "basic": False, "trade": "mason", "spaces": 4, "room": 4,
              "heavy": True, "holds": {"weight": 30}, "by": "space", "fireproof": True,
              "does": "a stone room of its own on the ground floor: 30 kg a space kept, safe from fire (D2-49)"},
}
FITTING_ALIAS = {a: f for f, d in FITTINGS.items() for a in d.get("aliases", [])}
# Rooms by structure (spec/economy/buildings.md "Rooms and structures"; D2-154 floors, D2-166 the large and stone ones; calibrate).
# Materials in real kilograms on the handling units (D2-288; u7 §2.1, wave1 §3.5); units held at today's (D2-309).
# A building's structure is one material for all its rooms; wattle takes a small room only; stone is a mason's work (D2-3).
ROOMS = {
    "small room": {"floor": 6, "places": 2,
                   "wattle": {"materials": {"timber": 36, "withies": 35}, "units": 6},   # roof at the site (D2-328)
                   "timber": {"materials": {"timber": 160, "stone": 60, "withies": 15, "straw": 75}, "units": 6},
                   "stone": {"materials": {"stone": 1600, "timber": 40, "straw": 75}, "units": 40, "trade": "mason"}},
    "medium room": {"floor": 12, "places": 4,
                    "timber": {"materials": {"timber": 270, "stone": 100, "withies": 25, "straw": 130}, "units": 15, "trade": "carpenter"},
                    "stone": {"materials": {"stone": 2700, "timber": 70, "straw": 130}, "units": 90, "trade": "mason"}},
    "hall": {"floor": 30, "places": 8,
             "timber": {"materials": {"timber": 560, "stone": 210, "withies": 50, "straw": 260}, "units": 200, "trade": "carpenter"},
             "stone": {"materials": {"stone": 5600, "timber": 140, "straw": 260}, "units": 250, "trade": "mason"}},
}
BLUEPRINTS = {
    "small room": {"label": "a small room (wattle, timber or stone)", "materials": dict(ROOMS["small room"]["wattle"]["materials"]),
                   "units": 6, "structure": "wattle", "basic": True},
    "medium room": {"label": "a medium room (timber on stone, or stone)", "materials": dict(ROOMS["medium room"]["timber"]["materials"]),
                    "units": 15, "structure": "timber", "basic": False, "trade": "carpenter"},
    "hall": {"label": "a hall (timber on stone, or stone)", "materials": dict(ROOMS["hall"]["timber"]["materials"]), "units": 200,
             "structure": "timber", "basic": False, "trade": "carpenter"},
    "camp": {"label": "a camp (a lean-to and a fire ring)", "materials": {"timber": 3}, "units": 1, "size": 4, "structure": "camp",
             "basic": True, "fittings": {"beds": 4, "fire ring": 1}, "lasts": 10},                                  # D2-68
}
# The building package (review 02zh; spec/economy/buildings.md; D2-154, D2-155, D2-165 to D2-171). All numbers calibrate.
SPACE = {
    "added": 0.75,                    # D2-154: a room added to a building costs a quarter less in materials and work
    "storeys": {2: 1.5, 3: 2.0},      # D2-154, D2-3: an upper storey's room costs this times the room alone; stone only
    "upgrade": 0.75,                  # 02zh §2: the new structure's materials for its rooms, less a quarter, and the work (proposed)
    "order": ["wattle", "timber", "stone"],
    "camp_floor": 4,                  # a camp's lean-to (D2-68): its ground on built ground or scrub
    "camp_store": 30,                 # D2-176, D4-84: what a lean-to keeps, in weight (a few days' food or fuel), under cover; 30 kg
                                      # in the handling units (a space's loose weight; was 10 when a tent weighed 6: W-97)
    "monument_ground": 1,             # building_lines.md §2 (proposed): on built ground or scrub; none elsewhere
    "seed_free": 3,                   # D4-85: free floor a seeded building is given beyond its contents, unless its file says (`free`)
    "seed_keep_ground": 6,            # D4-85: ...only while its parcel keeps this much ground for building (a small room)
}
# Storage (D2-155): what each kind of store takes, in the order goods are put away; free floor holds 30 weight a space of any goods.
STORES = {
    "kinds": {"grain": ["grain", "rye", "beans"], "timber": ["timber", "firewood", "charcoal"]},   # "food": every edible good; "weight": any good
    "by_weight": ["timber"],          # kinds whose stores hold kilograms, not counts (D2-288: timber and firewood alike by weight)
    "order": ["granary", "cellar", "bins", "woodshed", "vault"],
    "floor": 30,                      # weight a space of free floor
    # stacked by the wall, kg a space (W-97 default, with the handling units, D2-288): hay and straw to the roof (storage.md §3.10:
    # 1,000 kg); fuel and timber stacked, stone piled (est.)
    "stack": {"timber": 300, "firewood": 300, "charcoal": 300, "hay": 1000, "straw": 1000, "stone": 1000},
    "words": {"granary": ("the granary floor holds", "are on it"), "cellar": ("the cellar holds", "are in it"),
              "bins": ("the bins hold", "are in them"), "woodshed": ("the woodshed holds", "are in it"),
              "vault": ("the vault holds", "are in it"), "smoke loft": ("the smoke loft holds", "hang in it")},
}
# Monuments: a building with no room (building_lines.md §2; proposed): a description and 3 lines.
MONUMENTS = {
    "carved post": {"label": "a carved post", "materials": {"timber": 2}, "units": 2, "basic": True, "structure": "timber",
                    "aliases": ["post", "a post", "carved pole"]},
    "standing stone": {"label": "a standing stone", "materials": {"stone": 60}, "units": 4, "basic": False, "trade": "mason",   # about 1.5 t
                       "structure": "stone", "aliases": ["stone", "a stone", "menhir"]},
    "cairn": {"label": "a cairn", "materials": {"stone": 6}, "units": 3, "basic": True, "structure": "stone",   # 6 stone until site material is built (D2-306, stage 5; L-186)
              "aliases": ["a cairn", "heap of stones"]},
    # a fish weir (brief 5 §3, D2-209; calibrate): a standing work across a river at a water parcel, built by a declared crew
    # (`with`), with a condition (floods and ice wear it, mended like a building) and a gap set open or shut (WATER_WORKS); its
    # materials and units are its first section's in wattle (WATER_WORKS weir: position.first + material.wattle, W-69); built with
    # "structure": timber, the first section is timber and costs the difference more (wild/gear.py)
    "weir": {"label": "a fish weir (stakes and wattle across the river, wicker traps in its gap)",   # its cost: WATER_WORKS (D2-302)
             "basic": False, "structure": "timber", "site": "river", "crew": 2, "pack": "wild",   # a craft (u2 §6 bug 4)
             "aliases": ["fish weir", "a weir", "a fish weir", "eel weir", "build a weir", "build weir"]},
}
# The river's works (brief 5 §3, §3a, §3b; D2-209, D2-210; calibrate). A weir is built in sections (D2-210). **Position decides a
# section's share and hold; material decides its wear and cost** (W-69, 20 Nov: the material names had stood for position). The first
# section (index 0) takes `share` 0.30 of a run passing and holds `hold` 100 kg a night; each added one (up to `most`) 0.07 and 70 kg,
# less as it wears (`by_level`); open, `open` of that. Any section, the first included, is wattle (wear 1.0) or timber (wear 0.5);
# a stone footing under a section makes it wear at `footing` wear whatever it is. A section's cost is its material's, and the first's
# adds the weir's own stakes across the river and its trap (`position.first` materials and units): a wattle first section is the
# MONUMENTS row (12 timber, 24 units: 6 + 6, 8 + 16), a timber added one 10 timber and 25 units, as built before; a timber first
# section 16 timber and 33 units, a wattle added one 6 and 16 (a level's mend of any section stays at 1 timber and under 2 units). A wattle section upgraded to timber costs the difference (D2-210).
# A night's catch is the share, capped by what the weir holds less what is in its traps unlifted, and shared with the other gear in the
# same parcel in proportion to the shares (wild/gear.py). Each section wears a night by Poisson(`base` x its material x the water x the
# flow (from the catchment's rain today and half of yesterday's, over the mean, `flow_at`) x `gap_high` with the gap shut in high water
# or above x ice (`ice`, `thaw` the night the ice breaks)) levels; a level is mended at `mend` of the section's build. Setting the gap
# shut puts the traps in (`units`), opening takes them out. A trap in water on a running river is wrecked on a spate night at `wreck`
# (D2-211: fish alive in it until then). A water wheel on a river a run passes has a gap too (a new one shut): shut, it grinds at full
# and its dam stops `stop` of a run going up (held below it that night) and sends a run going down through the race, where a trap in
# water takes `race` of it; open, it grinds at `open_rate` (Q-51, default taken: half), the runs pass.
# The holds are in kg of the catch's goods (fish about 1 kg gutted a unit), not food (D2-258): a first section about 100 kg on a
# peak night (a real weir's traps; was 10 food, about 22 kg on the unit of D2-258: x 4.6), an added section 70 (in the old ratio
# 7/10), a set trap 10 kg (17 eels, 3 salmon; was 3 food, about 6.5 kg: x 1.5). What the holds do not bind, keeping the catch must
# (fresh fish's spoilage, salt, the racks and smokehouses, their fuel).
# The wear calibrated to D2-210's year (W-69, 20 Nov; docs/review/37_growth/02zzw_water_fixes.md), measured on the runs world's large,
# icy river (Eelmouth: about 12 low, 9 normal, 4 high, 4 spate and 3 flood nights and 6 frozen ones a year) with the gap kept right
# (open in high water without a run): a wattle section about 0.50 of its cost a year, timber 0.25, stone-footed 0.05, a full weir
# (wattle and three timber) 0.31. Was high 2, spate 5, flood 15, gap_high 1.5, ice 3, thaw 5, a large river 1.5: wattle 1.27 a
# year there, timber 0.67, a full weir 0.82, and a flood night took a wattle section with the gap open or shut. A level a week of
# normal flow on a lowland river (`base`) is kept. Now a spate costs a wattle section about 0.4 levels with the gap open and 0.9
# shut, a flood 0.9 and 1.7 (D2-210's "a flood with the gap shut usually takes the section" gives way to its year's upkeep).
# The weir's cost (D2-302, 23 Nov; calibrate in live runs): set directly, here and nowhere else (MONUMENTS["weir"] reads it), on a
# lowland river: a wattle first section 12 units, 20 timber (poles, D2-303), 10 withies; each added one (up to 3) 6 units, 8 timber,
# 5 withies; a timber first section 20 units, 40 timber, each added 10 units and 15 timber; a beck 0.3 times these, a large river
# 2.5 times (`water`); upgrading costs the difference. Upkeep a year a quarter of the build (wattle), an eighth (timber): the
# measured year's wear (wattle about 8 levels a year, timber about 4, on the runs world's river) at `mend` 0.03 of a section's build a
# level (was 0.06: half a wattle section's cost a year). Was: a wattle first section 12 timber and 24 units, a timber added one 10
# timber and 25 units (the old 2 kg timber).
WATER_WORKS = {"weir": {"position": {"first": {"share": 0.30, "hold": 100.0},
                                     "added": {"share": 0.07, "hold": 70.0, "most": 3}},
                        "material": {"wattle": {"wear": 1.0}, "timber": {"wear": 0.5}},
                        "cost": {"first": {"wattle": {"materials": {"timber": 20, "withies": 10}, "units": 12},
                                           "timber": {"materials": {"timber": 40}, "units": 20}},
                                 "added": {"wattle": {"materials": {"timber": 8, "withies": 5}, "units": 6},
                                           "timber": {"materials": {"timber": 15}, "units": 10}},
                                 "water": {"beck": 0.3, "lowland": 1.0, "large": 2.5}},
                        "footing": {"wear": 0.1, "materials": {"stone": 10}, "units": 15},
                        "open": 0.1, "by_level": {5: 1.0, 4: 0.8, 3: 0.6, 2: 0.3, 1: 0.1, 0: 0.0},
                        "wear": {"base": 0.143, "water": {"lowland": 1.0, "large": 1.2, "beck": 2.0}, "beck_m": 150.0,
                                 "flow": {"low": 0.5, "normal": 1.0, "high": 1.5, "spate": 2.5, "flood": 5.0},
                                 "flow_at": [[0.3, "low"], [1.5, "normal"], [3.0, "high"], [5.0, "spate"]], "gap_high": 2.0,
                                 "ice": 1.5, "thaw": 2.0},
                        "mend": 0.03, "units": {"shut": 2, "open": 1}},
               "trap": {"wreck": {"spate": 0.5, "flood": 0.85},           # a flood very likely, not always (D2-218)
                        "hold": 10.0},                      # a set trap in water, in the river or a race, holds this many kg (D2-213, D2-258)
               "mill": {"stop": 0.5, "race": 0.5, "open_rate": 0.5, "units": {"shut": 1, "open": 1}}}
MONUMENTS["weir"].update(materials=dict(WATER_WORKS["weir"]["cost"]["first"]["wattle"]["materials"]),   # read from the one copy
                         units=WATER_WORKS["weir"]["cost"]["first"]["wattle"]["units"])             # (D2-302), never held twice
# Extravagance in tiers (D2-171; calibrate): materials and work multiplied; noticed further (signs.BUILDING, layout, roads).
TIERS = {
    "plain": {"materials": 1.0, "work": 1.0, "words": ""},
    "fine": {"materials": 1.5, "work": 2.0, "words": "finely built"},
    "rich": {"materials": 2.5, "work": 4.0, "words": "richly built"},
    "grand": {"materials": 4.0, "work": 8.0, "words": "grand"},
}
TIER_ORDER = ("plain", "fine", "rich", "grand")
# What people write on buildings (D2-169, D2-170; building_lines.md, proposed; calibrate): places for lines by room, caps, the cost
# of each engraving, and where on a building each place is (a presentation choice, in order).
LINES = {
    "places": {"monument": 3},        # rooms: ROOMS[room]["places"]
    "words": {"description": 25, "line": 30}, "chars": 240,
    "units": {"paint": 2, "carve": 4, "stone": 6}, "other": 1,     # D2-170: changing or erasing another's: the same plus 1
    "carve_tools": {"crude": 1.0, "copper": 1.0}, "carve_wear": 1,
    "spots": {"building": ["over the door", "on the doorpost", "on the east wall", "on the west wall", "on the north wall",
                           "on the south wall", "on the roof beam", "on the hearthstone"],
              "monument": ["on its face", "on its back", "on its side"]},
    "how": {"paint": "Painted", "carve": "Carved", "stone": "Cut into the stone"},
}

# Techniques: one handler reads these (38.17 §5). Tool multipliers by grade (recipes.md §8); "bare" is bare hands; a grade missing
# from `tools` means the work cannot be done with it (no mining bare-handed).
TECHNIQUES = {
    "forage": {"verb": "gather", "label": "foraging (greens, roots, berries, nuts)", "aliases": ["foraging", "gather food"], "basic": True, "off_with": ["wild"],
               "at": {"covers": ["forest", "meadow", "pasture", "scrub", "heath", "moor", "fen", "saltmarsh"]}, "draws": "plants", "yield": {"kind": "stock", "base": 1.2},
               "units": 1, "gives": "wild food", "tags": ["food"]},
    "hunt": {"verb": "gather", "label": "hunting game", "aliases": ["hunting"], "basic": True, "at": {"covers": ["forest"]}, "off_with": ["wild"],
             "draws": "game", "yield": {"kind": "chance", "p": 0.35, "range": [5, 15], "by": {"hide": 0.25}},   # a kill's meat x 2.5 on the 1,500 kcal unit (D2-258), its stock
             # x 2.5 too (RESOURCES game spec_unit, D2-261): a kill takes the share of the wood's game it took, as often, for the food
             "weapon": {"none": 0.3, "armed": 1.0}, "wear": 0.3, "units": 2, "gives": "meat", "tags": ["food", "hunting", "animals"]},
    "fell": {"verb": "gather", "label": "felling timber", "aliases": ["felling", "chop timber", "cut wood"], "basic": True,
             "at": {"covers": ["forest"]}, "draws": "wood", "yield": {"kind": "fixed", "base": 8.0},   # 4 timber a unit with a crude tool
             "tools": {"bare": 0.25, "crude": 1.0, "copper": 2.0}, "wear": 1, "units": 2, "gives": "timber", "tags": ["timber", "woodland"]},   # (basis §1; was 3 an act)
    "firewood": {"verb": "gather", "label": "gathering firewood (dead wood, by hand)", "basic": True,
                 "aliases": ["gather firewood", "gathering firewood", "sticks", "dead wood", "kindling"],
                 "at": {"covers": ["forest", "scrub"]}, "draws": "dead", "yield": {"kind": "pool", "base": 3.0}, "units": 1,
                 "gives": "firewood", "tags": ["timber", "woodland", "fuel"]},                                   # D2-156, D2-157
    # clearing new ground for a field (Zach, 24 Oct: "Can they not clear land at all and make new plots?"): grass or scrub broken
    # up, stones and roots got out; a wood must be felled to scrub first. The whole parcel becomes a field when its work is done
    "clear": {"pack": "farming", "verb": "work", "label": "clearing new ground for a field (turf, roots and stones out)", "basic": True,
              "aliases": ["clear ground", "clear land", "clearing", "make a field", "break new ground", "grub up"],
              "at": {"covers": ["meadow", "pasture", "scrub"]}, "draws": "plot", "yield": {"kind": "clear"},
              "tools": {"bare": 0.4, "crude": 1.0, "copper": 1.5}, "wear": 1, "units": 1, "gives": "", "tags": ["farming", "building"]},
    "cut": {"verb": "gather", "label": "cutting young growth for firewood", "basic": True,
            "aliases": ["cut young growth", "coppice", "coppicing", "cut brush", "cut poles"],
            "at": {"covers": ["forest", "scrub"]}, "draws": "young", "yield": {"kind": "fixed", "base": 5.0},
            "tools": {"crude": 1.0, "copper": 1.5}, "wear": 0.5, "units": 1, "gives": "firewood", "tags": ["timber", "woodland", "fuel"]},
    # withies (u3 §1.1; D2-288: a 10 kg bundle of green rods): cut from the wild willow on the fen and the banks (wild/willow.py), or
    # where none grows from young growth in a wood or scrub (crooked rods), 1.5 bundles a unit with a crude tool, by the season
    "cut withies": {"verb": "gather", "label": "cutting withies (green rods for wattle and wicker)", "basic": True,
                    "aliases": ["withies", "cut rods", "cut wands", "cut osiers", "cut willow"],
                    "at": {"covers": ["fen", "meadow", "pasture", "forest", "scrub"]}, "draws": "willow", "draws_else": "young",
                    "yield": {"kind": "fixed", "base": 1.5}, "tools": {"bare": 0.33, "crude": 1.0, "copper": 1.33}, "wear": 0.25,
                    "by_season": {"winter": 1.0, "autumn": 0.8, "spring": 0.5, "summer": 0.3}, "units": 1, "gives": "withies",
                    "tags": ["timber", "woodland", "craft"]},
    # wild cord (u3 §1.2): nettle and bast twisted by hand, no stock; 0.04 kg a unit in summer and autumn, less in spring, little in
    # winter (stems retted standing)
    "twist cord": {"verb": "gather", "label": "twisting cord from nettle and bast", "basic": True,
                   "aliases": ["cord", "make cord", "twist nettles", "nettle cord", "gather nettles for cord"],
                   "at": {"covers": ["built", "forest", "scrub", "fen", "field", "meadow", "pasture"]}, "yield": {"kind": "fixed", "base": 0.04},
                   "by_season": {"summer": 1.0, "autumn": 1.0, "spring": 0.75, "winter": 0.25}, "units": 1, "gives": "cord",
                   "tags": ["craft"]},
    "mine": {"verb": "gather", "label": "mining copper ore", "aliases": ["mining", "dig ore"], "at": {"covers": ["rock"]}, "draws": "seam",
             "yield": {"kind": "fixed", "base": 2.0}, "tools": {"crude": 1.0, "copper": 1.5}, "wear": 2, "units": 2, "gives": "copper ore",
             "tags": ["mining", "craft"], "trade": "miner"},
    "quarry": {"verb": "gather", "label": "quarrying stone", "aliases": ["quarrying", "cut stone"], "at": {"covers": ["rock"]},
               "draws": "quarry", "yield": {"kind": "fixed", "base": 8.0}, "tools": {"crude": 1.0, "copper": 1.5}, "wear": 2, "units": 2,   # 4 a unit (basis §1)
               "gives": "stone", "tags": ["building", "craft"], "trade": "mason"},
    # Farming (D2-53, D2-54, D2-59, D4-38 to D4-40; 02l §2 scaled to the plot of about 16 seed, calibrate)
    "sow": {"pack": "farming", "verb": "work", "label": "sowing a field broadcast (seed thrown)", "aliases": ["sowing", "plant", "broadcast"], "basic": True,
            "at": {"covers": ["field", "meadow", "pasture", "heath", "scrub"]}, "draws": "plot", "yield": {"kind": "sow", "seed": 6.0, "worth": 1.0}, "units": 1, "gives": "",
            "tags": ["farming"]},
    "hoe": {"pack": "farming", "verb": "work", "label": "breaking the soil with a hoe", "aliases": ["hoeing", "dig", "break the soil"], "basic": True,
            "at": {"covers": ["field"]}, "draws": "plot", "yield": {"kind": "break", "plots": 0.0625, "stone": 1.0},
            "tools": {"bare": 0.5, "crude": 1.0, "copper": 1.5}, "wear": 0.5, "units": 1, "gives": "", "tags": ["farming"]},
    "plough": {"pack": "farming", "verb": "work", "label": "ploughing with a yoked pair of oxen", "aliases": ["ploughing", "plow"], "at": {"covers": ["field"]},
               "draws": "plot", "yield": {"kind": "break", "plots": 0.25, "stone": 1.0}, "animals": {"oxen": 2},
               "uses": {"wooden plough": 1, "harness": 2}, "units": 1, "gives": "", "tags": ["farming", "animals"], "trade": "farmer"},
    "ditch": {"pack": "farming", "verb": "work", "label": "ditching and banking wet ground", "aliases": ["ditches", "drain", "ditch and bank"],
              "at": {"covers": ["field"]}, "draws": "plot", "yield": {"kind": "works", "ground": "wet", "units": 40.0, "upkeep": 1.5},
              "tools": {"bare": 0.5, "crude": 1.0, "copper": 1.5}, "wear": 0.75, "units": 1, "gives": "", "tags": ["farming"],
              "trade": "farmer", "crew": True},                                     # D2-66: 40 units a plot by a crew led by one who knows how
    "terrace": {"pack": "farming", "verb": "work", "label": "terracing hill ground", "aliases": ["terraces", "terracing"], "at": {"covers": ["field"]},
                "draws": "plot", "yield": {"kind": "works", "ground": "hill", "units": 60.0, "upkeep": 1.5, "stone": 6.0},
                "tools": {"bare": 0.5, "crude": 1.0, "copper": 1.5}, "wear": 0.75, "units": 1, "gives": "", "tags": ["farming"],
                "trade": "farmer", "crew": True},                                   # D2-66: 60 units and 6 stone a plot
    "select seed": {"pack": "farming", "verb": "work", "label": "selecting seed from the best of a ripe crop", "aliases": ["seed selection"],
                    "at": {"covers": ["field"]}, "draws": "crop", "yield": {"kind": "select"}, "units": 1, "gives": "", "tags": ["farming"],
                    "trade": "farmer"},                               # D2-65: one who knows it sows crops that ripen 15% sooner
    "weed": {"pack": "farming", "verb": "work", "label": "weeding a growing crop", "aliases": ["weeding", "tend"], "basic": True,
             "at": {"covers": ["field", "meadow", "pasture", "heath", "scrub"]},
             "draws": "crop", "yield": {"kind": "tend"}, "units": 1, "gives": "", "tags": ["farming"]},
    "manure": {"pack": "farming", "verb": "work", "label": "manuring a field", "aliases": ["manuring", "spread dung"], "basic": True, "at": {"covers": ["field"]},
               "draws": "plot", "yield": {"kind": "manure", "plots": 0.1875}, "inputs": {"dung": 1.9}, "units": 1, "gives": "",
               "tags": ["farming", "animals"]},
    "reap": {"pack": "farming", "verb": "work", "label": "reaping a crop", "aliases": ["reaping", "harvest"], "basic": True,
             "at": {"covers": ["field", "meadow", "pasture", "heath", "scrub"]},
             "draws": "crop", "yield": {"kind": "crop", "plots": 0.125, "straw": 4.7}, "tools": {"bare": 0.6, "crude": 1.0, "copper": 1.5},
             "wear": 0.25, "units": 1, "gives": "grain", "tags": ["food", "farming", "harvest"]},
    "hay": {"pack": "farming", "verb": "gather", "label": "cutting hay", "aliases": ["cut hay", "haymaking", "mow"], "basic": True, "at": {"covers": ["pasture", "meadow"]},
                "draws": "grass", "yield": {"kind": "fixed", "base": 7.0}, "tools": {"bare": 0.3, "crude": 1.0, "copper": 1.5}, "wear": 0.5,   # 7 of 10 kg a unit (u3 §10)
                "by_season": {"spring": 0.5, "summer": 1.0, "autumn": 0.3, "winter": 0.0}, "units": 1, "gives": "hay", "tags": ["animals", "farming"]},
    # Cattle (D2-63, D4-41, D4-44, D4-45; 02o, calibrate)
    "herd": {"verb": "work", "label": "herding (watching the beasts)", "aliases": ["herding", "watch the herd", "tend the herd"], "basic": True,
             "at": {"covers": ["pasture", "meadow", "field", "heath", "moor", "fen", "saltmarsh"]}, "draws": "herd", "yield": {"kind": "herd"}, "units": 1, "gives": "",
             "tags": ["animals"]},
    "care": {"verb": "work", "label": "caring for a child (feeding, minding, keeping it warm)", "basic": True,
             "aliases": ["mind", "minding", "look after", "nurse", "tend the child"], "at": {"children": True}, "draws": "child",
             "yield": {"kind": "care"}, "units": 1, "gives": "", "tags": ["family"]},                                       # D2-142, D2-150
    # Fences round a parcel and gates (livestock.md "Fences and gates": D2-130, D2-132): a field work on the parcel; FENCES has the numbers
    "gather wild food": {"verb": "gather", "label": "gathering wild food (what is in season where you are: greens, berries, nuts, fungi, roots)",
                         "aliases": ["forage", "foraging", "gather food", "gather", "pick", "gather nuts", "gather berries", "gather mushrooms",
                                     "gather acorns", "pick berries", "pick mushrooms"], "basic": True, "pack": "wild",
                         "at": {"covers": ["forest", "meadow", "pasture", "scrub", "heath", "moor", "fen", "saltmarsh"]}, "draws": "wild plants",
                         "yield": {"kind": "wild_forage", "base": 1.2}, "units": 1, "gives": "", "tags": ["food"]},
    "make clappers": {"verb": "make", "label": "making clappers (two boards on a cord) for scaring beasts off a field", "basic": True, "pack": "wild",
                      "aliases": ["clappers", "make a clapper"], "inputs": {"timber": 0.04}, "units": 1, "gives": {"clappers": 1}, "tags": ["farming"]},   # two boards, 1 kg
    "make tallow lights": {"verb": "make", "label": "dipping rushes in tallow for lights to work by at night", "basic": True,
                           "aliases": ["tallow lights", "make lights", "make a light", "rushlights", "dip rushes"],
                           "inputs": {"tallow": 1}, "units": 1, "gives": {"tallow light": 4}, "tags": ["light"]},   # brief 3 §5
    "make a horn": {"verb": "make", "label": "making a horn to blow from a cast antler's base", "basic": True, "pack": "wild",
                    "aliases": ["horn", "make horn"], "inputs": {"antler": 1}, "units": 2, "gives": {"horn": 1}, "tags": ["farming"]},
    "leach acorns": {"verb": "make", "label": "boiling acorns in changes of water at a hearth till the bitterness is gone", "basic": True,
                     "aliases": ["leach", "leaching acorns", "acorn meal"], "pack": "wild", "at": {"fittings": ["hearth"]},
                     "inputs": {"acorns": 3}, "units": 1, "gives": {"acorn meal": 2}, "tags": ["food", "cooking"]},
    "burn the stubble": {"verb": "work", "label": "burning the stubble after the harvest", "basic": True, "pack": ["wild", "farming"],
                         "aliases": ["burn stubble", "fire the stubble"], "at": {"covers": ["field"]}, "draws": "guard",
                         "yield": {"kind": "wild_guard", "load": "slugs", "cut": 0.3, "days": 16, "thin": {"slugs": 0.3},
                                   "done": "You burned off the stubble in {place}."}, "units": 2, "gives": "", "tags": ["farming"]},
    "range: near": {"verb": "modifier", "label": "hunting on the village's own land", "aliases": [], "basic": True, "pack": "wild",
                     "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:snare", "gather:net", "gather:den work", "gather:trap in water"],
                     "key": "range", "value": "near", "untaught": "tryable", "changes": {"range": "near", "units": 0}, "units": 0,
                     "gives": "", "tags": ["hunting"]},
    "range: the wood around": {"verb": "modifier", "label": "hunting out through the woods and wastes around (about 2.5 km)", "aliases": [], "basic": True, "pack": "wild",
                     "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:snare", "gather:net", "gather:den work", "gather:trap in water"],
                     "key": "range", "value": "the wood around", "untaught": "tryable", "changes": {"range": "the wood around", "units": 1}, "units": 1,
                     "gives": "", "tags": ["hunting"]},
    "range: far": {"verb": "modifier", "label": "hunting far out into the wild land beyond (a long day)", "aliases": [], "basic": True, "pack": "wild",
                     "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:snare", "gather:net", "gather:den work", "gather:trap in water"],
                     "key": "range", "value": "far", "untaught": "tryable", "changes": {"range": "far", "units": 3}, "units": 3,
                     "gives": "", "tags": ["hunting"]},
    "hunt with": {"verb": "modifier", "label": "hunting in another's party: name who leads; you go their way, to their place and range, after what they are after", "aliases": [], "basic": True, "pack": "wild",
                  "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:net"], "key": "with", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["hunting"]},   # brief 4b §3.1
    "hunt alone": {"verb": "modifier", "label": "hunting alone: no one joins your hunt (others may join it unless you say so)", "aliases": [], "basic": True, "pack": "wild",
                   "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:net"], "key": "alone", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["hunting"]},
    "hunt only with": {"verb": "modifier", "label": "taking into your hunting party only those you name", "aliases": [], "basic": True, "pack": "wild",
                       "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:net"], "key": "only", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["hunting"]},
    "looking for": {"verb": "modifier", "label": "looking for one thing in particular: name it, a kind or a sort (boar, deer, hares, fowl, small game)", "aliases": [], "basic": True, "pack": "wild",
                    "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive", "gather:snare", "gather:net", "gather:den work", "gather:trap in water",
                                 "gather:gather wild food", "work:guard the field", "work:pest work"],
                    "key": "looking for", "value": "*", "untaught": "tryable", "changes": {}, "units": 0, "gives": "", "tags": ["hunting"]},
    "fence": {"verb": "work", "label": "fencing a parcel round (wattle or post and rail)", "basic": True,
              "aliases": ["fencing", "put up a fence", "wattle fence", "mend the fence", "build a fence", "a fence"],
              "at": {"covers": ["pasture", "meadow", "field", "scrub"]}, "draws": "plot", "yield": {"kind": "fence", "fence": "wood"},
              "tools": {"bare": 0.5, "crude": 1.0, "copper": 1.5}, "wear": 0.5, "units": 1, "gives": "", "tags": ["animals", "farming", "timber"]},
    "wall": {"verb": "work", "label": "walling a parcel round (a dry-stone wall)", "basic": False, "trade": "mason", "crew": True,
             "aliases": ["walling", "dry wall", "dry-stone wall", "stone wall", "build a wall", "mend the wall", "a wall"],
             "at": {"covers": ["pasture", "meadow", "field", "scrub"]}, "draws": "plot", "yield": {"kind": "fence", "fence": "stone"},
             "tools": {"bare": 0.5, "crude": 1.0, "copper": 1.5}, "wear": 0.75, "units": 1, "gives": "", "tags": ["animals", "farming", "building"]},
    "open the gate": {"verb": "work", "label": "opening a gate and leaving it open", "basic": True, "aliases": ["open gate", "leave the gate open"],
                      "at": {"covers": ["pasture", "meadow", "field", "scrub"]}, "draws": "plot", "yield": {"kind": "gate", "gate": "open"},
                      "units": 0, "gives": "", "tags": ["animals"]},
    "shut the gate": {"verb": "work", "label": "shutting a gate", "basic": True, "aliases": ["shut gate", "close the gate", "close gate"],
                      "at": {"covers": ["pasture", "meadow", "field", "scrub"]}, "draws": "plot", "yield": {"kind": "gate", "gate": "shut"},
                      "units": 0, "gives": "", "tags": ["animals"]},
    "dung": {"pack": "farming", "verb": "gather", "label": "gathering dung", "aliases": ["gather dung", "collect dung"], "basic": True,
                    "at": {"covers": ["pasture", "meadow", "field"]}, "draws": "dung", "yield": {"kind": "fixed", "base": 5.0}, "units": 1,
                    "gives": "dung", "tags": ["animals", "farming"]},
    "milk": {"pack": "farming", "verb": "work", "label": "milking (a cow in milk)", "aliases": ["milking"], "at": {"covers": ["pasture", "meadow", "field", "heath", "moor", "fen", "saltmarsh"]},
             "draws": "herd", "yield": {"kind": "milk", "cows": 6, "each": 3.0}, "units": 1, "gives": "milk", "tags": ["food", "animals"],
             "trade": "herder"},   # a medieval cow's 3 kg a day (Trow-Smith), six cows a unit by hand (D2-260; 02zzu): 4.6 food a unit
                                   # at milk's 0.256 a kg (was 3 cows at 1.6 milk; a cow's day 0.77 food, 0.8 on the old values)
    "pull flax": {"pack": "farming", "verb": "work", "label": "pulling flax by the root", "aliases": ["pull the flax", "pulling flax", "flax"],
                  "basic": True, "at": {"covers": ["field", "meadow", "pasture"]}, "draws": "crop", "yield": {"kind": "pull"}, "units": 1,
                  "gives": "flax", "tags": ["farming", "craft"]},
    "dig a strip": {"pack": "farming", "verb": "work", "label": "digging a strip of turf for flax", "aliases": ["dig a flax strip", "dig strip"],
                    "basic": True, "at": {"covers": ["meadow", "pasture"]}, "yield": {"kind": "dig_strip"}, "units": 1, "gives": "",
                    "tags": ["farming"]},
    "slaughter": {"verb": "work", "label": "slaughtering a beast", "aliases": ["butcher", "kill a cow"], "basic": True,
                  "at": {"covers": ["pasture", "meadow", "field", "heath", "moor", "fen", "saltmarsh", "built"]}, "draws": "herd",
                  # meat a head (D2-258; 02zzu): live weight x dressing x a medieval carcass's edible share 0.70 (Albarella), at 1,500
                  # kcal a unit: a cow 300 kg (91 food), an ox or bull 400 kg (126), a young beast 120 kg (29, the lookup's veal);
                  # USDA's modern carcass (20% bone) would give 12% more, within D2-259's 20%
                  "yield": {"kind": "slaughter", "gives": {"cows": {"meat": 150, "hide": 3.5, "tallow": 4}, "oxen": {"meat": 210, "hide": 4, "tallow": 4},
                                                          "bulls": {"meat": 210, "hide": 4, "tallow": 4},   # hide by weight (u3 §2.3)
                                                          "young": {"meat": 48, "hide": 1, "tallow": 1}}},   # tallow: brief 3 §5 (calibrate)
                  "units": 2, "gives": "meat", "tags": ["food", "animals"]},
    # Mending a worn fitting (D4-103 phase 2; building_risks.md: capital has upkeep): it works at full again (calibrate)
    "dress millstones": {"verb": "work", "label": "dressing worn millstones (recutting their furrows)", "aliases": ["dress the stones"],
                         "basic": True, "at": {"fittings": ["millstones"]}, "yield": {"kind": "mend", "fitting": "millstones"},
                         "units": 2, "gives": "", "tags": ["building", "food"]},
    "reline oven": {"verb": "work", "label": "relining a cracked oven", "aliases": ["mend the oven"], "basic": True,
                    "at": {"fittings": ["oven"]}, "yield": {"kind": "mend", "fitting": "oven", "inputs": {"stone": 4}}, "units": 2,
                    "gives": "", "tags": ["building", "food"]},
    "clear the leat": {"verb": "work", "label": "clearing the mill leat of silt and weed", "aliases": ["clear the mill race"],
                       "basic": True, "at": {"fittings": ["water wheel"]}, "yield": {"kind": "mend", "fitting": "water wheel"},
                       "units": 3, "gives": "", "tags": ["building", "food"]},
    "repair": {"verb": "work", "label": "repairing a building", "aliases": ["mend"], "basic": True, "at": {"building": True},
               "yield": {"kind": "repair"}, "units": 2, "gives": "", "tags": ["building", "shelter"]},
               # its materials and work by the building's size (D2-168: PHYSICS repair); each action does 2 units until it is mended
    "clear for building": {"verb": "work", "label": "clearing ground for building (turf, roots and stones out)", "basic": True,
                     "aliases": ["clear to build", "building ground", "clear a building plot", "make built ground", "grub out roots"],
                     "at": {"covers": ["field", "pasture", "meadow", "scrub"]}, "draws": "plot", "yield": {"kind": "clear_built"},
                     "tools": {"bare": 0.4, "crude": 1.0, "copper": 1.5}, "wear": 1, "units": 1, "gives": "",
                     "tags": ["building"]},                                             # 02zh §8: CLEARING["built"]
    # Grinding and the mill ladder (D2-60, D2-61; recipes.md §16, 02n §3, calibrate): a hand mill, an ox mill, a water mill
    "grind": {"verb": "make", "label": "grinding grain into meal at a hand mill", "aliases": ["grinding", "hand mill", "quern"], "basic": True,
              "at": {"fittings": ["hand mill"]}, "inputs": {"grain": 3}, "units": 1, "gives": {"meal": 3}, "tags": ["food", "cooking"]},
              # D2-167: about 3 grain a unit, and meal makes porridge, not bread (calibrate)
    "mill": {"verb": "make", "label": "milling grain at dressed millstones turned by an ox", "aliases": ["milling", "ox mill"], "basic": True,
             "at": {"fittings": ["millstones"]}, "animals": {"oxen": 1}, "inputs": {"grain": 64}, "units": 2, "gives": {"flour": 64},   # D4-97
             "tags": ["food", "cooking"]},
    "water mill": {"verb": "make", "label": "milling grain at a water mill", "aliases": ["water milling"], "basic": True,
                   "at": {"fittings": ["water wheel"]}, "inputs": {"grain": 200}, "units": 2, "gives": {"flour": 200}, "tags": ["food", "cooking"]},   # D4-97
    "dry fodder": {"pack": "farming", "verb": "make", "label": "drying a green crop into hay", "aliases": ["dry hay", "make hay of", "dry green crop"],
                   "basic": True, "inputs": {"green crop": {"green grain": 30, "green rye": 30, "green beans": 30}}, "units": 1,
                   "gives": {"hay": 1}, "tags": ["animals", "farming"]},       # D4-106; 30 kg green dries to a 10 kg hay (u3 §2.4; was 10 to 8)
    "pack": {"verb": "make", "label": "making a pack basket", "aliases": ["backpack", "pack basket"], "basic": True,
             "inputs": {"withies": 0.4, "hide": 0.1}, "units": 1, "gives": {"pack": 1}, "tags": ["travel"]},   # u3 §2.2: withies, rawhide straps
    "handcart": {"verb": "make", "label": "making a handcart", "aliases": ["cart"], "inputs": {"timber": 2}, "tools": {"crude": 1.0, "copper": 1.0},
                 "units": 3, "gives": {"handcart": 1}, "tags": ["travel", "craft"], "trade": "carpenter"},              # recipes.md §2
    "bread": {"verb": "make", "label": "baking bread at a hearth", "aliases": ["baking", "bake"], "basic": True, "at": {"fittings": ["hearth"]},
              "inputs": {"flour": 10, "firewood": 0.5}, "units": 2, "gives": {"bread": 10}, "tags": ["food", "cooking"]},   # D2-60; u3 §2.4
    "oven bread": {"verb": "make", "label": "baking bread in a stone oven", "aliases": ["oven baking"], "basic": True,
                   "at": {"fittings": ["oven"]}, "inputs": {"flour": 100, "firewood": 3}, "units": 4, "gives": {"bread": 100},   # a firing (D4-97; u3 §2.4)
                   "tags": ["food", "cooking"]},
    # Fishing and salt (D4-103's acceptance test; water_and_preservation.md §4, §5: the gear ladder's first rungs; calibrate)
    # the edge (u2 §4.6; u1 §2): the shallows of a water or fen parcel by hand (a dip net helps at a run's pinch), and a run passing
    # by the parcel's pinch (u1 §5); "fish" and "fishing" are no longer its aliases (a bare "fish" names no one way)
    "fish by hand": {"pack": "water", "verb": "gather", "label": "fishing at the edge (by hand, with a spear or a hand net)", "basic": True,
                     "aliases": ["fishing by hand", "hand fishing", "the edge", "fish the edge", "fish the shallows", "tickle trout",
                                 "catch fish by hand", "fishing at the edge"], "at": {"covers": ["water", "fen"]}, "draws": "shallows",
                     "draws_else": "fish", "yield": {"kind": "stock", "base": 0.6, "spread": 0.5}, "units": 1, "gives": "fish",
                     "tags": ["food", "fishing"], "run": True, "ice": "edge", "run_gear": {"dip net": 3.0}},
    # line fishing (u2 §4.5): the open water's fish with a hand line, a rod raising it x1.5 (today's 1.5 a unit is the rod's)
    "angle": {"pack": "water", "verb": "gather", "label": "fishing with a line (a hand line, or a rod and line)", "basic": True,
              "aliases": ["angling", "rod fishing", "fish with a rod", "fish with rod and line", "line fishing", "fish with a line"],
              "at": {"covers": ["water"]}, "draws": "fish", "yield": {"kind": "stock", "base": 1.0, "spread": 0.5},
              "gear_x": {"fishing rod": 1.5, "hand line": 1.0}, "units": 1, "gives": "fish", "tags": ["food", "fishing"], "ice": "bank"},
    "fishing rod": {"pack": "water", "verb": "make", "label": "making a fishing rod and line", "aliases": ["make a rod", "rod and line"], "basic": True,
                    "inputs": {"withies": 0.1}, "units": 1, "gives": {"fishing rod": 1}, "tags": ["fishing", "craft"]},   # a 1 kg pole (u3 §2.3)
    "salt pan": {"pack": "water", "verb": "gather", "label": "making salt in the saltmarsh pans (dried by the sun)", "basic": True,
                 "aliases": ["make salt", "salt pans", "gather salt"], "at": {"covers": ["saltmarsh"]}, "draws": "salt",
                 "yield": {"kind": "fixed", "base": 1.0}, "by_season": {"spring": 0.4, "summer": 1.0, "autumn": 0.2, "winter": 0.0}, "units": 1, "gives": "salt", "tags": ["salt"]},
    # inland salt (brief 5 §4b; D2-56, D2-209; calibrate, OPEN L-110): brine drawn at the pan's spring boiled with firewood, about 1
    # firewood a salt and a unit for 4, in any season; the salter's trade
    "boil salt": {"pack": "water", "verb": "make", "label": "boiling salt from brine over a fire", "aliases": ["boil brine", "boiling salt",
                  "salt boiling", "boil the brine"], "basic": False, "trade": "salter", "at": {"fittings": ["brine pan"]},
                  "inputs": {"firewood": 4}, "units": 1, "gives": {"salt": 4}, "tags": ["salt", "fuel"],
                  "manual": "brine drawn from the spring beside the pan and boiled dry over a fire: about 1 firewood a salt, in any "
                            "season; a pan burns through with use and is mended"},
    "mend the brine pan": {"pack": "water", "verb": "work", "label": "mending a burnt-through brine pan (patching and resetting it)",
                           "aliases": ["mend the pan", "patch the pan", "mend the salt pan"], "basic": True, "at": {"fittings": ["brine pan"]},
                           "yield": {"kind": "mend", "fitting": "brine pan", "inputs": {"copper": 0.25}}, "units": 2, "gives": "",
                           "tags": ["building", "salt"]},
    # the smokehouse's, the hearth rack's, the hard cure's, the hot smoke's and retting's acts are u4's (engine/process.py, registered below)
    "salt fish": {"pack": "water", "verb": "make", "label": "salting fish to keep", "aliases": ["salting", "salt the fish"], "basic": True,
                  "inputs": {"fish": 40, "salt": 10}, "units": 1, "gives": {"salt fish": 40}, "process": "salting", "tags": ["food", "cooking", "fishing"]},   # D2-283: 40 kg a unit, salt 1 to 4
    "salt meat": {"verb": "make", "label": "salting meat in a tub to keep", "aliases": ["salting meat", "salt the meat", "brine the meat"],
                  "basic": True, "inputs": {"meat": 40, "salt": 5}, "units": 1, "gives": {"salt meat": 40}, "process": "salting", "tags": ["food", "cooking"]},   # D2-283: 40 kg a unit, salt 1 to 8
    "cheese": {"pack": "farming", "verb": "make", "label": "making cheese", "aliases": ["cheesemaking"], "at": {"fittings": ["cellar"]},
               "inputs": {"milk": 20, "salt": 0.6}, "units": 1, "gives": {"cheese": 3.3}, "tags": ["food", "animals"], "trade": "herder"},   # u3 §2.4
    # 6 milk (1.54 food) make a cheese of 1.61, 5% more than went in, for a unit and 0.2 salt: kept, within D2-259's 20% (a real hard
    # cheese takes about 10, 02zzu; 1.2 food a unit of the chain against 1.1 on the old values)
    "charcoal": {"verb": "make", "label": "burning charcoal", "aliases": ["charcoal burning"], "at": {"covers": ["forest"]},
                 "inputs": {"timber": 5}, "units": 1, "gives": {"charcoal": 1}, "tags": ["timber", "craft"], "trade": "woodsman"},   # 125 kg to 20 (u3 §2.4)
    "wooden plough": {"pack": "farming", "verb": "make", "label": "making a plough", "aliases": ["make a plough"], "inputs": {"timber": 1.2, "copper": 1},
                      "tools": {"crude": 1.0, "copper": 1.0}, "units": 4, "gives": {"wooden plough": 1}, "tags": ["farming", "craft"],
                      "trade": "carpenter"},
    "dress and spin": {"verb": "make", "label": "dressing and spinning flax into cord", "aliases": ["spin flax", "spin", "spinning"],
                       "basic": False, "at": {"building": True}, "inputs": {"retted flax": 1}, "units": 1, "gives": {"cord": 0.125},
                       "batch": True, "tags": ["craft"]},                     # u3 §1.2: 8 units a kg; the retting is U4's (stage 3)
    "bedroll": {"verb": "make", "label": "making a bedroll", "aliases": ["blanket roll"], "basic": True, "inputs": {"hide": 0.5}, "units": 1,
                "gives": {"bedroll": 1}, "tags": ["travel"]},                                                           # D2-68
    "tent": {"verb": "make", "label": "making a tent", "aliases": [], "basic": True, "inputs": {"hide": 1.5, "timber": 0.4}, "units": 2,
             "gives": {"tent": 1}, "tags": ["travel"]},                                                                 # D2-68
    "harness": {"verb": "make", "label": "making a harness", "aliases": ["yoke"], "inputs": {"timber": 0.4, "hide": 0.5}, "units": 2,   # rawhide until tanning (D2-327)
                "gives": {"harness": 1}, "tags": ["animals", "craft"], "trade": "leatherworker"},
    "crude tool": {"verb": "make", "label": "making a crude hand tool", "aliases": ["tool"], "basic": True, "inputs": {"timber": 0.04, "stone": 0.04},
                   "units": 1, "gives": {"crude tool": 1}, "tags": ["craft"]},
    "crude weapon": {"verb": "make", "label": "making a crude weapon", "aliases": ["club", "spear", "weapon"], "basic": True,
                     "inputs": {"timber": 0.06}, "units": 1, "gives": {"crude weapon": 1}, "tags": ["weapons"]},
    "smelt": {"verb": "make", "label": "smelting copper", "aliases": ["smelting"], "at": {"fittings": ["anvil"]},
              "inputs": {"copper ore": 3, "fuel": {"charcoal": 1, "timber": 6}}, "units": 3, "gives": {"copper": 1}, "tags": ["mining", "craft"],   # 20 kg of charcoal, or 150 kg of wood
              "trade": "smelter"},                                  # one of the fuels (D4-46): charcoal, or timber as before
    "copper tool": {"verb": "make", "label": "making a copper hand tool", "aliases": ["hand tool", "metal tool"], "at": {"fittings": ["anvil"]},
                    "inputs": {"copper": 1, "timber": 0.02}, "units": 3, "gives": {"copper tool": 1}, "tags": ["craft", "smithing"], "trade": "smith"},
    "coin": {"verb": "make", "label": "striking coin", "aliases": ["strike coin", "minting"], "at": {"fittings": ["anvil"]},
             "inputs": {"copper": 1}, "units": 1, "gives": {"coin": 10}, "tags": ["craft", "smithing"], "trade": "smith"},
}
# Modifiers (agents/modifiers.md; D2-93, D2-94, D2-111, D2-112): techniques with `modifies` (verb, or verb:technique), the action
# argument they are written as (`key`: `value`; "*" any value), and what they change, read by the verb they modify. `untaught`:
# tryable (done worse, and one becomes aware of it) or no (refused, and one becomes aware it exists). Basic ones everyone knows.
TECHNIQUES.update({
    "for": {"verb": "modifier", "label": "doing it for someone (into their store, from it by right or agreement)", "aliases": [],
            "basic": True, "modifies": ["gather", "work", "make", "build", "give", "accept", "offer"], "key": "for", "value": "*",
            "changes": {"destination": "party"}, "units": 0, "gives": "", "tags": []},                                     # D2-37, D2-94
    "hidden: under brush": {"verb": "modifier", "label": "hiding something under brush", "aliases": ["hide", "under brush", "brush"],
                            "modifies": ["give:place"], "key": "hidden", "value": "under brush", "untaught": "tryable",
                            "changes": {"hidden": "under brush", "units": 1}, "units": 1, "gives": "", "tags": ["hiding"]},
    "hidden: buried": {"verb": "modifier", "label": "burying something to hide it", "aliases": ["bury it", "buried", "cache"],
                       "modifies": ["give:place"], "key": "hidden", "value": "buried", "untaught": "tryable",
                       "changes": {"hidden": "buried", "units": 2}, "units": 2, "gives": "", "tags": ["hiding"]},
    "method: dibble": {"pack": "farming", "verb": "modifier", "label": "dibbling seed (set by hand, seed by seed)", "aliases": ["dibble", "dibbling", "set seed"],
                       "modifies": ["work:sow"], "key": "method", "value": "dibble", "untaught": "no",
                       "changes": {"yield": {"seed": 2.0, "worth": 1.67}, "word": "dibbled"}, "units": 0, "gives": "",
                       "tags": ["farming"], "trade": "farmer"},                                      # D2-54, D2-94: 3x the work, 0.6x the seed
    "method: cairn": {"verb": "modifier", "label": "raising a cairn of stones over the dead", "aliases": ["cairn"], "basic": True,
                      "modifies": ["work:bury"], "key": "method", "value": "cairn", "changes": {"inputs": {"stone": 3}},
                      "units": 2, "gives": "", "tags": ["death"]},                                    # D2-96
    # extravagance in tiers (D2-171): a building or monument built finely, richly or grandly (TIERS: materials and work multiplied)
    "how: fine": {"verb": "modifier", "label": "building it finely (materials x1.5, work x2; seen from next door)", "aliases": ["finely"],
                  "basic": True, "modifies": ["build"], "key": "how", "value": "fine", "changes": {"tier": "fine"}, "units": 0,
                  "gives": "", "tags": ["building"]},
    "how: rich": {"verb": "modifier", "label": "building it richly (materials x2.5, work x4; named to all who come)", "aliases": ["richly"],
                  "basic": True, "modifies": ["build"], "key": "how", "value": "rich", "changes": {"tier": "rich"}, "units": 0,
                  "gives": "", "tags": ["building"]},
    "how: grand": {"verb": "modifier", "label": "building it grandly (materials x4, work x8; seen from the road coming in)",
                   "aliases": ["grandly"], "basic": True, "modifies": ["build"], "key": "how", "value": "grand", "changes": {"tier": "grand"},
                   "units": 0, "gives": "", "tags": ["building"]},
    "bury": {"verb": "work", "label": "burying the dead", "aliases": ["burial", "bury the dead", "bury the body"], "basic": True,
             "at": {"things": ["body", "carcass"]}, "yield": {"kind": "bury"}, "units": 2, "units_by": "bury", "gives": "",
             "tags": ["death"]},                                                  # D2-96; a dead beast too (brief 3 §4)
    "method: shallow": {"verb": "modifier", "label": "burying it shallow (half the digging; beasts may dig it up)", "aliases": ["shallow"],
                        "basic": True, "modifies": ["work:bury"], "key": "method", "value": "shallow", "changes": {}, "units": 0,
                        "gives": "", "tags": ["death"]},
    "burn": {"verb": "work", "label": "burning a carcass (firewood and work by its size)", "aliases": ["burn the carcass", "burn it",
             "burn the dead beast", "burn the beast"], "basic": True, "at": {"things": ["carcass"]}, "yield": {"kind": "burn"}, "units": 2,
             "units_by": "burn", "gives": "", "tags": ["death"]},                 # brief 3 §4
})
MODIFIERS = {t for t, d in TECHNIQUES.items() if d.get("modifies")}

# Gear's real hours a piece and its clock (u3 §2.2, wave1 §3.2; D2-276, D2-309: new things at the factor from the start): a piece
# takes hours x factor / 2 units, at least 1; under a unit, one act of 1 unit makes up to its batch (clocks.batch_of; O-2).
for _k, _h in {"fishing rod": 1.5, "crude tool": 7, "copper tool": 6, "crude weapon": 3, "bedroll": 3, "tent": 9,
               "wooden plough": 36, "handcart": 50, "harness": 13.5}.items():
    TECHNIQUES[_k].update(hours=_h, clock="capital")
# The bulk processes take up to their batch for their units (O-2; D2-247; u3 §2.4): less is less worth it, never refused for it.
for _k in ("grind", "mill", "water mill", "bread", "oven bread", "salt fish", "salt meat", "dry fodder", "leach acorns", "charcoal",
           "cheese"):
    TECHNIQUES[_k]["batch"] = True

# Capital rows (D2-276, D2-309; u7 §1, §2): each lasting thing's class and its real hours a piece (the middle of u7 §2's ranges);
# the classes in CAPITAL["hold"] keep their `units` until stage 5, read through clocks.capital_units. The weir's cost is set directly
# (D2-302), with no hours.
WORK_HOURS = {
    "rooms": {"small room": {"wattle": 405, "timber": 585, "stone": 945}, "medium room": {"timber": 1035, "stone": 1665},
              "hall": {"timber": 5850, "stone": 8100}},
    "fittings": {"beds": 6.5, "hearth": 13.5, "fire ring": 2.5, "owl hole": 2.5, "bins": 13.5, "granary": 36, "hand mill": 31.5,
                 "oven": 54, "anvil": 36, "cellar": 41, "millstones": 270, "water wheel": 3060, "stalls": 6.5, "woodshed": 27,
                 "smoke racks": 8, "brine pan": 27, "vault": 1350},
    "monuments": {"carved post": 31.5, "cairn": 9},
}
for _r, _d in ROOMS.items():
    for _st, _h in WORK_HOURS["rooms"].get(_r, {}).items():
        _d[_st].update(capital="rooms", hours=_h)
for _f, _d in FITTINGS.items():
    _d.update(capital="fittings", **({"hours": WORK_HOURS["fittings"][_f]} if _f in WORK_HOURS["fittings"] else {}))
for _m, _d in MONUMENTS.items():
    _d.update(capital="weir" if _m == "weir" else "monuments",
              **({"hours": WORK_HOURS["monuments"][_m]} if _m in WORK_HOURS["monuments"] else {}))
for _b, _d in BLUEPRINTS.items():
    _d["capital"] = "rooms"
BLUEPRINTS["camp"].update(clock="day", hours=4)                       # a camp lasts nights: the day clock, real hours / 2 (u7 §2.1)

# Building and fitting are techniques too, for knowledge (basic or a trade), with their costs in BLUEPRINTS and FITTINGS.
for _k, _b in list(BLUEPRINTS.items()) + list(FITTINGS.items()) + list(MONUMENTS.items()):
    TECHNIQUES.setdefault(_k, {"verb": "build", "label": "building " + _b["label"], "aliases": [], "basic": _b.get("basic", False),
                               "units": _b["units"], "gives": "", "tags": ["building", "shelter"], "trade": _b.get("trade"),
                               **({"pack": _b["pack"]} if _b.get("pack") else {})})

# Techniques at least one person in the world knows (D2-129): when no one in a world file does, one is chosen by a keyed draw among the
# adults whose trade has one of these words (else among all adults), and knows it from its upbringing.
KNOWN_SOMEWHERE = {"method: dibble": ["sow", "seed", "reap", "plough", "hoe", "field", "farm"]}
LEVELS = ("aware", "rough", "capable", "known")
TRY = {"rough": {"inputs": 1.7, "chance": 0.5}, "capable": {"inputs": 1.3, "chance": 0.75}, "known": {"inputs": 1.0, "chance": 1.0}}
SKILL_WORDS = ((0.85, "master"), (0.5, "skilled"), (0.2, "competent"), (0.0, "novice"))   # by the share of the way to a master
SKILL = {"trade": [0.5, 2.0], "basic": [1.0, 1.5], "tau": 50.0,     # D2-52 (02n §4): skill by practice, units of work; calibrate
         # the hunt (brief 4c §3.1, §3.3; calibrate): a multiplier on the bare-handed novice's chance, x1 to x8, rising geometrically
         # with practice (about x3 half way) to its top after `top_hard` units of practice at the default lifespan, scaled with the
         # lifespan (D2-153); a trip with a kill counts `kill_hard` times its units; a youth's practice counts `youth_hard` times; in a
         # party each member's counts x (1 + the leader's lead over them as a share of the leader's skill), at most `lead_hard`
         # above the capable (`capable_hard`), the party's best skill also finds more game: meetings x (skill / capable_hard)^find_hard
         # (0: as the brief has it; 4c's calibration, docs/review/37_growth/02zzd_ev/ev_region_4c.json: the near wood meets about one
         # beast a trip, so without it the master is held near the capable by meetings, not by the take)
         "hard": [1.0, 8.0], "top_hard": 50.0, "kill_hard": 1.5, "youth_hard": 2.0, "lead_hard": 2.0,
         "capable_hard": 3.0, "find_hard": 1.05}

# The capital factor (D2-276, D2-281, D2-309; u7 §1): one named lever for every lasting thing, read only through clocks.py. A
# capital row holds its real hours a piece (`hours`, the middle of the real range) and converts once: units = hours x factor / 2,
# at least `floor`; a class in `hold` keeps its row's `units` as written today until its companions are in (D2-309; u7 stage 5).
# "world" is the factor from the world's own numbers (units a year x 2 h / `real_year`: 1/7.03 in a 32-day world); a fraction
# ("1/15") is a stage or a sensitivity arm; a world spec's `capital_factor` wins.
CAPITAL = {
    "factor": "1/15",          # the stage before the target (D2-281): "1/15", then "world"
    "real_year": 2700,         # real working hours a year (D2-276)
    "hold": ["rooms", "fittings", "monuments", "weir", "fences", "clearing", "works"],   # at today's units until stage 5 (D2-309)
    "floor": 1,                # every act costs at least 1 unit (basis §1; O-2)
    "night": 32 / 365,         # the calendar's factor for a life counted in nights (D2-310)
}

PHYSICS = {
    "units": {"summer": 7, "autumn": 6, "winter": 5, "spring": 6},      # agents/work.md (calibrate)
    "youth_units": 4,
    "elder_units": 5,
    "ration": 1.0,
    # Labour (D4-103 phase 2; proposals/economic_calibration.md E, F, Q-2, L-35; first values, calibrate). Each at 0 (wear false) is
    # the engine before phase 2.
    "labour": {"work_food": 0.04,          # food a unit worked adds to the night's need
               "guard_food": 0.3,          # a night standing guard
               "over_units": 2,            # units one may push on past the day's (an agent's "overwork")
               "over_food": 2.0,           # their food, as units worked
               "fatigue": 1,               # units off tomorrow for each unit pushed past the day's
               "watch_tired": 2,           # units off tomorrow after a night on watch, its sleep given up (D2-21; calibrate)
               "fade_after": 0.5,          # years a craft goes unpractised before its skill fades (D4-105)
               "fade_rate": 0.5,           # then this share a year of what can still be lost
               "fade_keep": 0.6,           # the share of one's best gain over the craft's floor that is never lost
               "relearn": 3.0,             # practice counts this many times over while below one's best
               "step": 0.1,                # a unit's walk for each leg of the day's route past the free ones (carried until whole)
               "free_steps": 2,            # legs free: to the next parcel and back (D4-105)
               "wear": True},              # fittings wear with use and time (FITTINGS wear)
    "shelter": {"housed": 1.0, "worn": 1.05, "gappy": 1.1, "damaged": 1.2, "unsheltered": 1.5},     # D4-12, H-5; worn, gappy: brief 4 §3
    "shelter_cold": {"housed": 1.0, "worn": 1.1, "gappy": 1.2, "no_fuel": 1.3, "damaged": 1.5, "unsheltered": 2.0},
    "cold_starving": 0.3,                                                # H-5
    "fuel": {"normal": 0.4, "cold": 1.2, "camp": 0.8, "open": 1.2},     # in timber (heat / 1.25); in heat (D2-157): below
    "camping_fire": {"out": 1.6, "bedroll": 1.5, "tent": 1.25},            # in the cold by a fire in the open (D2-159)
    # a house burns its real weight a night (D2-290): a 10 kg bundle (0.5 heat) a normal night, about 30 kg (1.5) a cold one; a
    # camp twice a house's normal night, a fire in the open a cold night's (was 1, 4, 2 and 4: 20 to 80 kg at the new bundle)
    "heat": {"normal": 0.5, "cold": 1.5, "camp": 1.0, "open": 1.5, "order": ["firewood", "timber", "charcoal"],
             "share": 4, "hearth_spaces": 12, "ring_spaces": 6, "ring_cold": 1.15,
             # D4-83: the night's weather on a fire under no roof (a camp, or in the open): more fuel, and a chance it goes out in the
             # night, taking its warmth (a fire ring keeps it in a little better); a sound house's hearth is not touched (calibrate)
             "weather": {"rain": {"fuel": 1.5, "out": 0.0}, "heavy rain": {"fuel": 1.5, "out": 0.5}, "gale": {"fuel": 1.5, "out": 0.5},
                         "snow": {"fuel": 1.25, "out": 0.0}},
             "snow_lying_fuel": 1.15, "ring_keeps": 0.8},   # D2-157, D2-159     # D4-49: a camp's fire 1 a night; a fire in the open 2 (calibrate)
    "land_blind": 0.25,                                                  # D4-50: share with no eye for how bare a place is (calibrate)
    "breaks": {"p": 0.02, "cold": 0.08, "structure": {"wattle": 1.5, "timber": 1.0, "stone": 0.4, "camp": 1.0}},   # D2-168 (proposed)
    # shelter in levels (brief 4 §3; shelter_damage.md §1 to §4; calibrate), in worlds with the wild pack or `shelter_levels`:
    # 5 sound, 4 worn, 3 gappy, 2 holed, 1 failing, 0 ruined (a camp: 5 standing, 2 damaged, 0 down). Two chances a night by
    # structure, times the night's weather and the root of the floor over `size_ref`: minor wear takes a level; serious damage
    # as many as its cause is severe (`take`: the odds of 1, 2, 3 levels for wattle; timber one fewer, stone one, at most two)
    "wear": {"minor": {"wattle": 0.03, "timber": 0.015, "stone": 0.003, "camp": 0.08},
             "serious": {"wattle": 0.002, "timber": 0.001, "stone": 0.0002, "camp": 0.0},
             "camp_down": 0.05, "camp_flatten": 0.5,                    # a damaged camp falls; a gale flattens a standing one
             "weather": {"frost": [2.0, 1.0], "heavy rain": [1.5, 1.5], "strong wind": [3.0, 5.0], "gale": [6.0, 20.0],
                         "snow": [2.0, 8.0], "flood": [1.0, 20.0], "unmended": [1.0, 3.0],
                         "ice": [3.0, 4.0]},                         # ice on a weir (brief 5 §3.1; calibrate)
             "take": {"mild": [0.8, 0.2, 0.0], "gale": [0.4, 0.4, 0.2], "heavy": [0.2, 0.5, 0.3]},
             "strong_wind": 11.0, "storm": 0.5, "size_ref": 6, "unmended_days": 8,
             "mend": {"wattle": {}, "timber": {"timber": 1}, "stone": {"stone": 1}, "camp": {}}, "mend_per": 8,
             "damp": {"3": 1.5, "2": 3.0},                               # a store's spoiling, gappy and holed
             "camp_build": {"timber": 1}, "camp_fire": 1.5},             # a camp: poles and brush, cheap; its open fire wasteful
    # D2-165 (defaults for Zach to confirm): the beds each sleeper takes; without one, the floor, as in a damaged house
    "beds": {"infant": 0.0, "child": 0.5, "youth": 1.0, "adult": 1.0, "elder": 1.0, "floor": "damaged"},
    "hunger_yield": {"0": 1.0, "-1": 0.75, "-2": 0.5},
    "frailty": [0.25, 0.55],
    "hazard": {"step": 0.15, "max_rounds": 4},
    "refuge": 0.1,                                                       # the share of a stock foraging never takes
    "regrow_winter": 0.25,
    "game_threshold": 0.15,                                              # below this share of capacity game does not come back
    "combat": {"base": [0.5, 1.5], "guard": 2.0, "asleep": 0.5, "units": 3, "raid_share": 0.5, "fight_wear": 4},
    "teach": {"units_teacher": 2, "units_learner": 2, "skill_share": 0.3,
              "hunt_share": 0.15,    # the hunt's methods: a day closes this share of the gap to the teacher, x2 a youth (brief 4c §3.3)
              "any_craft_from_day": 0},   # from this day a lesson named differently by the learner is in the teacher's craft (D4-123)
    "watch": {"units": 4},
    "notes": {"max": 8, "words": 150, "open": 2},
    "felt_watched": 0.3,
    "glimpse": 3,
    "messages": {"per_day": 3, "jitter": {0: 37, 1: 37, 2: 18, 3: 8}, "max": 10},     # D4-31
    "say_units": 1,                                                                       # D4-31
    "carry": {"foot": 10},                                                                # transport.md (calibrate, OPEN C-1)
    "ground": {"wet": 0.75, "hill": 0.6},                                # D2-66: until weather exists; field works bring each to 1.0
    "master_yield": 0.2,                                                 # D2-64: a master farmer's crops yield x1.2
    "seed_selection": 0.85,                                              # D2-65: ripen 15% sooner
    "camping": {"out": [1.5, 2.0, 1.0], "bedroll": [1.35, 1.75, 0.5], "tent": [1.2, 1.4, 0.0], "camp": [1.2, 1.5, 0.0]},
                                                                         # D2-68: food a night, in the cold, the cold's fall (share)
    "farming": {"plot_seed": 16.0, "ratio": 3.0, "break_gain": 1.5, "weed_max": 0.5, "weed_tau": 8.0, "window": 2, "rot": 0.25,
                "lie_loss": 0.08, "frost_loss": 0.3, "green": [0.3, 0.7], "turned_under": 0.02, "turf": 0.1,   # D4-106 (calibrate)
                "vernal": 3,                                    # winter nights winter grain needs before it heads (D4-106)
                "fail": [0.05, 0.15], "fallow": 0.40, "grazed": [0.50, 1.15], "manure": [0.35, 1.15], "dung_per_plot": 10.0},
                # D2-59 (16 seed a plot), D4-38 (02l: harvest 3x the seed, +1.5 broken, weeding to +50% on a curve of tau 1.5 small
                # plots = 8 units a plot), D4-39 (soil), D2-53 (failure 5%, 15% the same crop twice); calibrate
    "cattle": {"births": 0.7, "survive": 0.85, "in_milk_share": 0.6, "dung": 20.0, "grass_per_plot": 25.0, "grass_r": 0.32,
               "stray": 0.2, "hungry_milk": 0.7, "starve_nights": 4,
               # D2-189 (L-41): grass on a cover, as a share of pasture's; rough grazing carries fewer head (calibrate)
               "grazing": {"pasture": 1.0, "meadow": 1.0, "saltmarsh": 0.7, "fen": 0.5, "heath": 0.4, "moor": 0.3}},
               # 02o (calibrate): births a cow a year, a cow in milk 0.6 of the year, dung for 2 plots a head a year, 2 head a plot of
               # pasture in summer, an unwatched herd strays
    "repair": {"per": 4, "min": 2},           # D2-168: 1 timber (stone for stone) and 1 unit for every 4 spaces of floor, at least 2 and 2
    "bury": {"soft": 2, "stony": 4, "frozen": 6},                        # D2-96: units of work by the ground and the cold (calibrate)
    # brief 5 §4a (calibrate): a smokehouse fire takes `fuel` heat a night it burns (1 firewood); while it burns, a chance a night
    # by its structure that it catches, and then each other building on its parcel catches by `spread`; a fire takes this share
    # of a burnt building's food (`food`) and other goods (`other`), and the batch on its racks
    "smokehouse": {"fire": {"wattle": 0.02, "timber": 0.008, "stone": 0.0003},
                   "spread": {"wattle": 0.5, "timber": 0.35, "stone": 0.03, "camp": 0.6}, "food": 0.85, "other": 0.5},
    "untaught": 0.5,                                                     # D2-93: an untaught try works half as well (calibrate)
}

# ---------------------------------------------------------------------------------------------------- the environment (37.2's spec)
# The day's weather by spell (environment/scheduler.md, D2-69, D2-99; calibrate): the chances of each kind of day within a spell.
# A spell comes from the world's spec (`spells`: [{kind, from, to}], days counted from 1); otherwise `normal`. Rain falls as snow in
# winter and on cold days. Each kind's effect on the senses (environment/visibility.md, D2-99) and whether it wets what lies out.
WEATHER = {
    "clear": {"sight": 1.0, "sound": 1.0, "wet": False, "words": "a clear day"},
    "rain": {"sight": 0.8, "sound": 0.7, "wet": True, "words": "rain all day"},
    "heavy rain": {"sight": 0.6, "sound": 0.5, "wet": True, "words": "heavy rain, the ground running with water"},
    "fog": {"sight": 0.3, "sound": 1.0, "wet": False, "words": "a thick fog lying on the land"},
    "snow": {"sight": 0.5, "sound": 0.7, "wet": True, "words": "snow falling"},
    "gale": {"sight": 0.9, "sound": 0.5, "wet": False, "words": "a gale tearing at the roofs", "loud": "loud"},
}
SPELLS = {
    "normal": {"clear": 0.55, "rain": 0.25, "heavy rain": 0.05, "fog": 0.10, "gale": 0.05},
    "wet": {"clear": 0.20, "rain": 0.45, "heavy rain": 0.20, "fog": 0.15},
    "dry": {"clear": 0.85, "rain": 0.03, "fog": 0.07, "gale": 0.05},
    "cold snap": {"clear": 0.50, "fog": 0.15, "snow": 0.30, "gale": 0.05},
    "storm": {"clear": 0.05, "rain": 0.25, "heavy rain": 0.40, "gale": 0.30},
}
# The weather scheduler (D4-109; engine/climate.py; proposals/weather_scheduler.md). A world with a `climate:` block draws its
# weather here; one without keeps the hand-written spells. Temperate lowland first values (calibrate), on the day clock.
CLIMATE = {
    # the seasons' means at a node at height 0: temperature (°C), the chance a day is wet, a wet day's rain (mm)
    "temp": {"spring": 9.0, "summer": 16.0, "autumn": 11.0, "winter": 4.0},
    "temp_sd": 2.5,                  # the day's spread about its type's mean
    "diurnal": {"clear": 6.0, "cloud": 3.0},    # how far the night falls below the day's mean: a clear night, a cloudy one
    "wet_p": {"spring": 0.45, "summer": 0.40, "autumn": 0.55, "winter": 0.55},
    "rain_mm": 4.5, "heavy_mm": 12.0,
    "wind": 5.0, "gale": 17.0, "gust": 0.45,   # m/s: a day's mean wind; a gale at or above; the wind field's spread
    "snow_below": 1.5,               # rain falls as snow at or below this temperature (or a little above it after a hard frost)
    "fog_p": {"spring": 0.15, "summer": 0.03, "autumn": 0.30, "winter": 0.30},   # a settled, still day: fog in the low ground
    "height_m": [20, 90, 200, 400],  # a parcel's height rank (0 to 3) as metres
    "lapse": 0.0065,                 # °C a metre
    "orographic": 0.0015,            # rain's chance x (1 + this x metres)
    "corr_km": 100.0,                # how far apart places stop sharing weather (e-folding distance)
    "km_a_day": 25.0,                # a day's travel on a road, as distance
    "persist": {"temp": 0.7, "rain": 0.3, "wind": 0.5},   # day-to-day persistence of each local field (AR(1))
    "year_sd": {"temp": 0.6, "wet": 0.12}, "year_persist": 0.4,   # a year's anomaly, and how much of it carries to the next
    # daily weather types (after Lamb's British types): how often (base), how long they hold, what they do to the day
    "types": {
        "settled":   {"base": 0.30, "hold": 0.75, "temp": {"summer": 2.0, "winter": -2.0}, "rain": 0.2, "wind": 0.5, "clear": True},
        "westerly":  {"base": 0.30, "hold": 0.60, "temp": {"summer": -0.5, "winter": 1.0}, "rain": 1.5, "wind": 1.2},
        "cyclonic":  {"base": 0.18, "hold": 0.55, "temp": {}, "rain": 2.1, "wind": 1.5},
        "northerly": {"base": 0.09, "hold": 0.50, "temp": {"spring": -3.0, "summer": -3.0, "autumn": -3.0, "winter": -3.5}, "rain": 0.8,
                      "wind": 1.3, "clear": True},
        "easterly":  {"base": 0.09, "hold": 0.60, "temp": {"summer": 1.5, "winter": -3.5}, "rain": 0.5, "wind": 1.0, "clear": True},
        "storm":     {"base": 0.05, "hold": 0.35, "temp": {}, "rain": 2.4, "wind": 2.0},
    },
    # moving storms: born upwind on stormy days, crossing the region on a track, adding wind and rain where they pass (D4-110)
    "storms": {"p": {"storm": 0.7, "cyclonic": 0.15, "westerly": 0.04}, "heading": 0.0, "heading_sd": 0.6,   # radians, 0 = toward the east
               "speed": [150.0, 400.0], "radius": [30.0, 80.0], "wind": [8.0, 16.0], "rain": 1.0},  # km a day, km, m/s added at the centre
    # eras: regimes of the climate over years (weather only: disease and ecology are other systems, D4-109)
    "eras": {
        "steady": {"temp": 0.0, "wet": 0.0, "spread": 1.0, "types": {}, "years": 20, "next": {"dry": 0.3, "wet": 0.3, "cold": 0.2, "warm": 0.2}},
        "warm":   {"temp": 0.5, "wet": 0.0, "spread": 1.0, "types": {"settled": 1.2}, "years": 25, "next": {"steady": 0.6, "dry": 0.4}},
        "cold":   {"temp": -0.7, "wet": 0.05, "spread": 1.3, "types": {"northerly": 1.6, "easterly": 1.4, "storm": 1.3}, "years": 30,
                   "next": {"steady": 0.6, "wet": 0.4}},
        "wet":    {"temp": 0.0, "wet": 0.13, "spread": 1.0, "types": {"cyclonic": 1.2, "westerly": 1.15, "settled": 0.85}, "years": 6,
                   "next": {"steady": 1.0}},
        "dry":    {"temp": 0.3, "wet": -0.15, "spread": 1.3, "types": {"settled": 1.35, "easterly": 1.2, "cyclonic": 0.8, "westerly": 0.85}, "years": 6,
                   "next": {"steady": 0.7, "warm": 0.3}},
        "stormy": {"temp": 0.0, "wet": 0.0, "spread": 1.0, "types": {"storm": 2.2, "cyclonic": 1.15, "settled": 0.9}, "years": 5, "next": {"steady": 1.0}},
    },
    # how much the day lets the senses through, from its values (D4-111): rain, falling snow and fog dim sight; wind and rain mask sound
    "vis": {"sight": {"rain_per_mm": 0.035, "rain_max": 0.5, "snow": 0.5, "fog": 0.3},
            "sound": {"wind_from": 4.0, "wind_per_ms": 0.03, "wind_max": 0.6, "rain_per_mm": 0.025, "rain_max": 0.3}},
    "shocks": {"dark year": {"p": 0.007, "temp": -1.5, "wet": 0.15, "years": [1, 2]}},     # a volcanic winter: rare, short
}

ENV = {
    "night": {"sight": 0.1, "moon": 0.25, "sound": 1.2},            # D2-99: light only for night events
    "snow_melt": 3,                                                 # snow lies until three days without frost
    "snow_ground": 0.5,                                             # things on the ground under lying snow
    "crop_high": 0.5,                                               # a grain crop standing high: that field's sight
    "crop_high_from": 0.6,                                          # ... from this share of its growing time until reaped
    "smoke": 0.7,                                                   # a parcel with smoke that day
    "felled": {"below": 0.3, "sight": 0.8},                         # a wood felled below this share of its timber is open ground
    "smoke_tags": ["smithing"], "smoke_techs": ["charcoal", "smelt", "dry meat", "dry fish", "smoke fish", "smoke meat", "tend the smoke", "boil salt"],
    "mask": {"very": 0.3, "loud": 0.6},                             # D2-100: quieter sounds near something very loud, or loud
    "loud_kinds": {"fight": "very", "raid": "very", "threat": "very"},
    "loud_tags": {"smithing": "loud"}, "loud_techs": {"mill": "loud", "water mill": "loud", "grind": "loud"},
    "inside_sound": 0.5,                                            # walls
    "ford_high_after": 2,                                           # a ford is high for 2 days after heavy rain (world/roads.md)
}

# ------------------------------------------------------------------------------------ things at a spot and noticing them (D2-85)
# Own conspicuousness (information/noticing.md; calibrate); hiding multiplies it (taught, untaught).
THINGS = {
    "body": 0.9, "body_built": 1.0, "heap": 0.9, "heap_min": 10, "pack": 0.4, "camp": 0.7, "trace": 0.3,
    # goods in the open (heap-sizes proposal): own = 1 - exp(-weight / heap_k), so 2 weight about 0.37 (the old pack), 10 about
    # 0.9 (the old heap), 40 and more about 1; a heap is "large" from 40 weight and "great" from 100; a close look judges each good
    # within a band of this ladder; one who attends to it counts it to about 1 (under 20) or 5 (calibrate)
    "heap_k": 4.34, "heap_large": 40, "heap_great": 100,
    "bands": [1, 2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 300, 500, 800, 1200, 2000],
    "body_days": 10,                                                # "dead some days", then bones to the season's end
    "rot_after": 2,                                                 # a body unburied this many days smells of rot
    # a beast that dies (D4-52): its carcass is as conspicuous as a body, a little less once only bones; edible the day after it died,
    # then the meat goes off; bones after some days. On a road it may leave nothing (it wandered off to die) or lie hidden off the
    # road. Meat by how it died, as a share of slaughter's (calibrate)
    "carcass": 0.9, "carcass_bones": 0.3, "carcass_bones_after": 6, "carcass_fresh_days": 1,
    "carcass_road": {"none": 0.3, "hidden": 0.3},
    "carcass_meat": {"starved": 0.25, "road": 0.5, "other": 0.5, "killed": 0.3, "sick": 0.6},
    # a carcass's stages by its size on the day's clock (brief 3 §2, calibrate): fresh this many days, then its rotting meat and offal
    # lose `rot` of themselves a night (x the season; nothing on a frozen night or under snow) until under `gone` of the first flesh,
    # when only bones are left. A person's body is a medium carcass for what comes to it (`body_mass` of flesh, D2-205)
    "carcass_size": {"cow": "large", "ox": "large", "bull": "large", "calf": "medium", "body": "medium", "hen": "small", "hare": "small"},
    "carcass_sizes": {"small": {"fresh": 1, "rot": 0.6, "burn": {"units": 1, "firewood": 2}},
                      "medium": {"fresh": 1, "rot": 0.4, "burn": {"units": 2, "firewood": 6}},
                      "large": {"fresh": 2, "rot": 0.3, "burn": {"units": 4, "firewood": 12}}},
    "carcass_rot_season": {"spring": 1.0, "summer": 1.5, "autumn": 1.0, "winter": 0.5}, "carcass_gone": 0.05,
    "carcass_offal": 0.25, "body_mass": 30, "carcass_kg": 3.0,      # offal as a share of the meat; a unit of meat as kg of carrion
                                                                   # (3: a red deer's 33 units about its 90 kg; was 5 at 20 units, D2-258)
    "hidden": {"under brush": [0.2, 0.4], "buried": [0.03, 0.06], "off the road": [0.2, 0.2]},
    # a set snare or trap, seen (brief 2 §4; brief 4c §4; calibrate): its own conspicuousness empty, spent (sprung), with a beast
    # caught in it (`caught`, while the catch is fresh: up to `fresh_days` after the night it was caught), and x`birds` once the birds
    # come to a catch with flesh on it (`birds_after` days after its night); for one who knows the line and is on its parcel, the look
    # it is given (`knows`, a close look); a line emptied by another shows it for `robbed_days`; a spent one is about for `spent_days`
    "set": {"own": 0.12, "sprung": 0.05, "caught": 0.4, "fresh_days": 1, "birds_after": 2, "birds": 1.5, "knows": 0.9,
            "robbed_days": 2, "spent_days": 6},
}
# Fences round a parcel (livestock.md, D2-130; calibrate): what a build takes for a parcel of size s (x the square root of s), the chance a
# day a herd gets through by its level (whole, gappy; down is no fence), and its upkeep: a wood fence loses a level each season unless
# a quarter of the build's work is spent mending it; a stone wall keeps.
FENCES = {
    # a wood fence loses a level a year unless mended a quarter of its build that year (D4-114: a year, not a season); one that
    # falls keeps `kept` of its build as posts and wattle to repair from
    "wood": {"inputs": {"timber": 4.0}, "units": 10.0, "through": {2: 0.3, 1: 0.6}, "decays": True, "mend": 0.25, "kept": 0.5,
             "words": ("fence", "a wattle fence")},
    "stone": {"inputs": {"stone": 8.0}, "units": 20.0, "through": {2: 0.05, 1: 0.2}, "decays": False, "mend": 0.25, "led": "wall",
              "words": ("wall", "a dry-stone wall")},
}

# Herds that are not held (livestock.md: D2-117, D2-123, D2-124, D2-128, D2-131; calibrate where the spec says so).
HERDS = {
    "gad": {"temp": 18.0, "wind": 3.0, "rain": 0.5, "through": 0.7},   # cattle gadding: a warm, still, dry summer day (the flies
                                                          # work in sun from about 18 degrees); a fence's odds at least this (brief 2 K1; calibrate)
    "steps": {"fed": 1, "drawn": 8},             # a day: a fed herd on good pasture 0 to 1 steps; hungry or drawn up to 8 (D2-123)
    "good_grass": 0.3,                           # grazing above this share of the pasture's best counts as good
    "draw": {"ripe": 1.0, "water": 0.3},         # beyond the food a parcel offers: a ripe crop's pull, water when hungry
    "dusk": {"milk": 0.8, "dry": 0.3, "fed_here": 0.7},   # D4-54: the chance a herd that wandered walks home at dusk (cows in milk,
                                                 # others), less by this share of how well it is feeding where it is (calibrate)
    "trample": 0.01,                             # of the standing crop, a head a day
    "onto_road": 0.1,                            # a step from a parcel where a road leaves
    "own": 0.95,                                 # a herd's own conspicuousness (information/noticing.md)
    "road": {"die": 0.15, "die_winter": 0.3, "gone": 0.15, "search": 5.0},   # D2-124, D2-125
    "capacity": {"drover": 10, "herder": 30, "unherded": 6},                 # D2-128
    "split": {"under": 0.01, "over": 0.1, "max": 0.6},                       # D2-128
    "share": {"centre": 0.25, "sd": 1.0, "max": 0.5},                        # D2-131: a quarter x 2^z, z Laplace (sd 1 doubling)
    "call": {"share": 0.25, "head": 3},          # a split while driving calls a drover who notices it, if this big (D2-127)
    # the pack ox (transport.md, D2-136; D2-135 capacity): led on a road by someone of its household, with a harness; it grazes on
    # stretches that pass grass, else eats hay from the load
    "pack_ox": {"carry": 100, "hay": 1.0, "graze": ["farmland", "plain", "river valley"], "graze_landmarks": ["meadow"]},
}

# The parcel graph (world/parcel_graph.md; D2-114 to D2-116): heights in words; the fittings that strike an arriving eye; the overview's
# length.
LAYOUT = {
    "height": ("down by the water", "on the valley floor", "on the slope", "up on the hilltop"),
    "seen": {"water wheel": "a water mill", "millstones": "a mill", "anvil": "a smithy", "oven": "a bake oven", "granary": "a granary"},
    "overview": (3, 5),
}

# How far an event reaches (D4-53): the whole node (everyone there can notice it), the parcel it happens on (noticed by the rule:
# presence, visibility, attention, the eye), or a building (those inside, and by the rule on its parcel). Kinds not listed: the parcel.
EVENT_EXTENT = {
    "node": ["death", "fire", "alarm", "fight", "threat", "raid", "sign", "arrive", "depart", "household", "claim", "grant", "release",
             "grown"],
    "building": ["store", "put", "left", "make", "host", "build", "birth"],
}

NOTICING = {"expert_at": 0.8,              # the share of a work's skill range past which one reads as an expert (L3; 02zq)
    # presence: where the observer was and what it did, by what its work draws on (D2-85); passing through 0.3 (D2-115), next door 0.3
    # (D4-98: was 0.1; a herd on the pasture beside one's house was seen about 1 day in 10)
    "presence": {"game": 1.0, "plants": 0.7, "herd": 0.5, "work": 0.5, "about": 0.5, "crossing": 0.3, "next door": 0.3,
                 "elsewhere": 0.05, "road": 1.0},
    "next_door_min": 0.5,                                           # only things this conspicuous are seen from next door
    "elsewhere_min": 0.8,                                           # only things this conspicuous are seen from elsewhere at the node
    "attention": {"place": 3.0, "search": 5.0,
                  # D4-75: a close look at what lies where one is (a sign's reach "near"); things in one's own house; a subject one
                  # attends to (a person, a house, a herd: one seeks it out, so presence is at least "about"); what one worked on
                  "close": 2.0, "own house": 3.0, "subject": 5.0, "working": 6.0},
    # D4-75: sound and smell carry beyond the parcel: presence by steps in the parcel graph from where one was today (0: the parcel
    # itself, 1: next door, ...; the last value for anything further), times the sense's visibility (weather, cover, night, masking)
    "carry": {"sound": [0.5, 0.45, 0.2, 0.1, 0.05], "smell": [0.5, 0.3, 0.12, 0.05, 0.0]},
    "within": {"touch": 0},                                         # a sense that reaches no further than this many steps
    "reach": {"near": 0, "around": 1},                              # a sign's reach: the furthest step it is read from
    "eye_senses": ["sight"],                                        # the eye for the land is an eye: it reads sight only
    "inside": 1.0,                                                  # those inside a house, or of a household: always there
    "loud": 1.0,                                                    # a sound this plain is not masked by louder ones (D2-100)
    "person": 2.0,                                                  # a person at work in the open: where they spent the day (glimpses)
    "theft": 0.4,                                                   # one slipping into a house and out with something
    "sky_weather": False,                                           # the weather is not seen through itself (signs about the sky)
    "eye": {"none": 0.5, "ordinary": 1.0, "keen": 3.0},             # D2-91 on things
    "eye_bare": {"none": 0.0, "ordinary": 1.0, "keen": 2.0},        # D4-50 on how bare a place is (none: only by failing)
    "eye_keen": 0.15,                                               # the share born keen (the share with none is `land_blind`)
    "eye_practice": {"techs": ["hunt", "forage"], "find": 5.0, "steps": [30.0, 120.0]},   # units of roaming work (and finds) to rise
}

# ---------------------------------------------------------------------------------------------- fuse events (conflict/fuse_events.md)
# Each kind: its sense, who can detect it and with what chance, how long the fuse is by the building's structure (acts in the call),
# the choices offered, and what happens with no call. Road kinds (meetings, finds, crossings) are added by the roads package.
FUSE = {
    "raid": {"sense": "sound", "label": "a break-in",
             "detect": {"watcher": 0.9, "dog": 0.6, "inside": {"wattle": 0.3, "timber": 0.3, "stone": 0.5, "camp": 0.3},
                        "neighbour": 0.3},                      # D4-75: own, read by the rule at night
             "acts": {"camp": 0, "wattle": 0, "timber": 1, "stone": 3},     # hut: none; timber: 1; stone: up to 3 (D2-81)
             "riders": {"detect": 0.5, "acts": 1},                          # D2-83
             "choices": ["defend", "flee", "hand over", "alarm", "stay"],
             "also": ["move", "take", "give"]},
}

# ---------------------------------------------------------------------------------------------------------- roads (world/roads.md)
# Terrain of a road's stretches (D2-104): sight and sound (environment/visibility.md) and the chance two parties on it meet (D2-110).
TERRAIN = {
    "plain": {"sight": 1.0, "sound": 1.0, "meet": 0.6}, "farmland": {"sight": 1.0, "sound": 1.0, "meet": 0.9},
    "woodland": {"sight": 0.35, "sound": 0.7, "meet": 0.7}, "marsh": {"sight": 0.6, "sound": 1.0, "meet": 0.6},
    "hills": {"sight": 0.5, "sound": 0.9, "meet": 0.6}, "mountain": {"sight": 0.5, "sound": 0.9, "meet": 0.6},
    "river valley": {"sight": 1.0, "sound": 1.0, "meet": 0.8},
}
# Landmarks (D2-107, D2-109): what each is, the trouble it can give (`challenge`: when, the default, what crossing anyway costs), the
# chance parties meet there, and good places' effect on a traveller. New kinds are rows here and, for a new kind of trouble, one
# function in roads.CHALLENGES.
LANDMARKS = {
    "ford": {"words": "a ford", "meet": 0.95, "challenge": "high", "default": "wait",
             "push": {"cart_loss": [0.3, 0.2], "herd_loss": 0.05, "foot": "soaked"}},
    "bridge": {"words": "a bridge", "meet": 0.95, "challenge": "down", "default": "go round"},
    "pass": {"words": "a pass", "meet": 0.95, "challenge": "snowed", "default": "turn back", "cold_night": True,
             "push": {"death": 0.1}},
    "narrows": {"words": "a narrows", "meet": 0.95, "sight": 0.2},
    "spring": {"words": "a spring", "meet": 0.8},
    "meadow": {"words": "a meadow by the road", "good": True, "seasons": ["summer", "autumn"]},
    "fruit trees": {"words": "wild fruit trees", "good": True, "seasons": ["autumn"]},
    "hollow": {"words": "a sheltered hollow", "good": True, "seasons": ["spring", "summer", "autumn", "winter"]},
}
ROADS = {
    "experience": 5.0,                      # crossings of a landmark that halve one's trouble there (D2-106)
    "call": {"death": 0.05, "loss": 0.5, "minor": 0.1},   # the thresholds for an urgent call (D2-105)
    "good": {"fed": 1.0, "gather": [1.0, 2.0], "known": 2.0, "camp": 1.2},   # D2-109
    "flee": 0.5,
    "waves": 3,                             # a meeting's conversation (D2-110)
    "notices": 5,                           # "On the way" lines on arrival (D2-97)
    "trace_days": {"tracks": 3, "ashes": 10, "ruts": 60, "fight": 2},   # D2-88; a fight's: that day and the next (signs pass)
    # hidden ways (D2-90, D2-92, D2-98): a hidden end shows only while its parcel's sight is this or less; its own conspicuousness, and
    # how much each party passing wears it; open land (or a wood felled below `felled` of its standing timber) shows it at `exposed`;
    # unused it grows back over about a season in forest or scrub; worn to `exposed` it is a path everyone at the node knows
    "hidden": {"hides": 0.5, "own": 0.03, "wear": 0.05, "exposed": 0.8, "regrows": ["forest", "scrub"]},
    "meet_landmark": 3.0,                   # crossing parties meet three times likelier on a stretch with a landmark (D2-121)
    "terrain": "farmland",                  # every road's terrain unless its world gives one (D2-122: a farm track)
}
FUSE.update({
    "meeting": {"sense": "sight", "label": "a meeting on the road", "acts": {"road": 3},
                "choices": ["go on", "turn back", "change course", "attack", "flee"], "also": ["give", "accept"]},
    "find": {"sense": "sight", "label": "something lying by the road", "acts": {"road": 2},
             "choices": ["take", "bury", "go on"], "also": []},
    "crossing": {"sense": "sight", "label": "trouble on the road", "acts": {"road": 1},
                 "choices": ["push on", "wait", "turn back", "go round"], "also": []},
    # a herd found loose on the road, and a group breaking off a herd one drives (livestock.md: D2-124, D2-127)
    "herd": {"sense": "sight", "label": "beasts loose on the road", "acts": {"road": 2},
             "choices": ["drive on", "drive back", "accompany", "leave"], "also": []},
    "split": {"sense": "sight", "label": "beasts breaking away", "acts": {"road": 1}, "choices": ["go after them", "let them go"], "also": []},
})
# Travel's choices at departure (D2-105, D2-109, D2-113) are modifiers known to all.
TECHNIQUES.update({
    "on trouble": {"verb": "modifier", "label": "what to do if the road gives trouble", "basic": True, "modifies": ["travel"],
                   "key": "on trouble", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel"],
                   "values": ["push on", "wait", "turn back", "go round"]},
    "stop at": {"verb": "modifier", "label": "stopping at a good place one knows on the way", "basic": True, "modifies": ["travel"],
                "key": "stop at", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel"]},
    "meeting": {"verb": "modifier", "label": "whether to stop for others met on the road", "basic": True, "modifies": ["travel"],
                "key": "meeting", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel"],
                "values": ["stop", "pass by"]},                                                                      # D4-51
    "gather on the way": {"verb": "modifier", "label": "gathering at good places one passes", "basic": True, "modifies": ["travel"],
                          "key": "gather", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel"]},
    "lead": {"verb": "modifier", "label": "leading a pack ox (an ox of your household's, with a harness)", "basic": True,
             "modifies": ["travel"], "key": "lead", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel", "animals"]},   # D2-136
    "lead on the hunt": {"verb": "modifier", "label": "leading a pack ox on the hunt, to carry the kill home (an ox here, a harness in hand)",
                         "basic": True, "pack": "wild", "aliases": [],
                         "modifies": ["gather:hunt the wild", "gather:stalk", "gather:drive"], "key": "lead", "value": "*",
                         "changes": {"units": 1, "lead": True}, "units": 1, "gives": "", "tags": ["hunting", "animals"]},   # brief 4b §3.2
    "searching": {"verb": "modifier", "label": "searching the road for a herd or a person", "basic": True, "modifies": ["travel"],
                  "key": "searching", "value": "*", "changes": {}, "units": 0, "gives": "", "tags": ["travel", "animals"]},   # D2-125
})
MODIFIERS = {t for t, d in TECHNIQUES.items() if d.get("modifies")}

# Gear's real hours a piece and its clock (u3 §2.2, wave1 §3.2; D2-276, D2-309: new things at the factor from the start): a piece
# takes hours x factor / 2 units, at least 1; under a unit, one act of 1 unit makes up to its batch (clocks.batch_of; O-2).
for _k, _h in {"fishing rod": 1.5, "crude tool": 7, "copper tool": 6, "crude weapon": 3, "bedroll": 3, "tent": 9,
               "wooden plough": 36, "handcart": 50, "harness": 13.5}.items():
    TECHNIQUES[_k].update(hours=_h, clock="capital")
# The bulk processes take up to their batch for their units (O-2; D2-247; u3 §2.4): less is less worth it, never refused for it.
for _k in ("grind", "mill", "water mill", "bread", "oven bread", "salt fish", "salt meat", "dry fodder", "leach acorns", "charcoal",
           "cheese"):
    TECHNIQUES[_k]["batch"] = True

# ---------------------------------------------------------------------------------------------------------------- life (spec/life)
# Birth and death (life/birth_and_death.md: D2-138 to D2-152; calibrate where the spec says so). Stages by days since birth (D2-139):
# infant 2, child 4, youth 12, adult 50, then elder. A world sets `children: {on: true, dial: low | high}`; off, nobody conceives.
LIFE = {
    # the lifespan (days to old age) is a world setting (D2-153); every stage is a share of it, and the spans marked "scaled" below
    # are at the default and scale with lifespan / 32
    "lifespan": 32,
    "shares": [["infant", 1 / 16], ["child", 1 / 8], ["youth", 3 / 16], ["adult", 5 / 8]],          # then elder
    "conceive": {"base": 0.8, "k": 0.5},                    # 0.8 x (1 - e^(-0.5 x units)) a night (D2-146, D2-162)
    # D2-141, D2-162; days, late, signs scaled. late (the last day) and signs_from (the day after conception) follow from 2 days
    # (proposals/fertility.md Q5, to confirm)
    "pregnancy": {"days": 2, "food": 0.3, "late": 1, "late_units": 1, "road_loss": 0.05, "signs_from": 1},
    "birth": {"housed": {"mother": 0.02, "infant": 0.03}, "camp": {"mother": 0.04, "infant": 0.065}, "out": {"mother": 0.06, "infant": 0.10},
              "helped": 0.5},                                                   # a camp: partly housed, between (D4-97; calibrate)
    "gap": 1,                                                               # scaled (D2-162)
    "infant": {"eats": 0.5, "dies": {"cared": 0.02, "not": 0.08}, "hungry": 2.0, "cold": 2.0, "weight": 2,
               "shelter": {"house": 1.0, "camp": 1.5, "out": 2.0}},             # a baby's night by where it sleeps (D4-97; calibrate)
    "child": {"dies": 0.005, "unminded": 4.0},
    "youth": {"eats": 0.8},                                                 # D2-330 (questions C6): between child and adult
    "dial": {"low": {"infant_care": 1, "child_eats": 0.7, "child_works": 1.0, "child_minding": 0},
             "high": {"infant_care": 3, "child_eats": 1.0, "child_works": 0.5, "child_minding": 1}},   # D2-145, D2-151
    "old_age": {"adult": 0.001, "elder": 0.01, "doubling": 20},            # D2-149; the doubling scaled
    "succession_days": 2,                                                           # D2-143
    "children_work": ["forage", "herd", "hay", "firewood"],   # D2-148, D2-156: what a head may set children to (the watch, D2-21, is not built)
    "child_skill": 0.5,                                                             # a child's skill at that work, to start
}


# The wave's recipes in kg at real hours (u3 §2.2), and mending (u3 §3.4): the gear unit's (engine/gear.py)
_GEAR.register_techniques(TECHNIQUES)
# The processing containers (u4; engine/process.py, D2-244): their acts, the racks' fields, the goods that wait in them
from cybertron2.engine import process as _PROC                          # noqa: E402
_PROC.register_techniques(TECHNIQUES)
_PROC.register_fittings(FITTINGS)
# Stores and containers (u5; engine/stores.py, D2-244): the spaces' real capacities, the containers, the vermin goods
from cybertron2.engine import stores as _STORES                         # noqa: E402
_STORES.register_fittings(FITTINGS)
_STORES.register_techniques(TECHNIQUES)
# The wild methods (D2-204, cybertron2/wild/methods.py): general rows whose take tables are generated from the kinds' traits.
from cybertron2.wild import methods as _WILD_METHODS                   # noqa: E402
_WILD_METHODS.build(TECHNIQUES, RESOURCES)
