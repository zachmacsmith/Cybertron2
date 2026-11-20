"""02zzu: shared units for food, weight and work (proposals/shared_units.md, "The analysis asked of 37.2"; OPEN Q-69; WORK W-64).

The table (goods, animals, methods, each with a source), the basis as parameters, and the three measurements the note uses:

    python3 02zzu_shared_units.py table                 the table, before and after, the checks; writes 02zzu_shared_units.json
    python3 02zzu_shared_units.py sens                  how the results move with kcal a food (2,000 / 2,500 / 3,000) and hours a unit
    CYB_ROOT=/home/user/c2-units python3 02zzu_shared_units.py engine
                                                        reads the engine's ITEMS, TAKEN, TECHNIQUES and checks the "now" columns
    CYB_ROOT=... python3 02zzu_shared_units.py runs WORLD.yaml V1,V2,.. [DAYS]
                                                        steps a water world night by night with no one acting and records each
                                                        village's run pulses (heads by kind, direction, night); merged into the JSON
    CYB_ROOT=... python3 02zzu_shared_units.py capacity WORLD.yaml ...
                                                        the capacity model (cybertron2.capacity) on each world, with today's values
                                                        and with the recommended set patched in memory (nothing on disk changes)

Measured facts and inference are kept apart in the note (02zzu_shared_units.md). Every value in the table carries a source key
(SOURCES) and a confidence: "checked" (looked up this session), "standard" (a standard table's value, recalled from the named
source; to be checked against it when the data change is written), "estimate" (no table gives it; a reasoned range).
No model calls, no agents: the `runs` and `capacity` modes only step the engine's physics.
"""
from __future__ import annotations

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "02zzu_shared_units.json")

# ------------------------------------------------------------------------------------------------------------- the basis
# OPEN Q-69: not decided. The recommended defaults (the brief): a food is a working adult's day, about 2,500 kcal; children 0.6,
# elders 0.8; a unit of work about 2 hours. Everything below is in kcal and hours and converted only here.
BASIS = {
    "kcal_food": 2500.0,            # kcal in one food
    "hours_unit": 2.0,              # hours in one unit of work
    "year_days": 32,                # the engine's year (D2-209's compression: Y/365 for growth, breeding and run sizes)
    "base_kcal": 2100.0,            # a day with no work: PAL 1.4 x BMR 1,500 (a 60 to 65 kg adult; FAO-WHO 2004)
    "work_kcal_h": 100.0,           # manual work's cost above that, averaged over a working day with its rests (about 3 METs
                                    # against 1.5: Compendium 2011, farm and hand-tool rows 3 to 6 METs)
    "shares": {"infant": 0.4, "child": 0.6, "youth": 1.0, "adult": 1.0, "elder": 0.8, "pregnant_add": 0.1, "nursing_add": 0.2},
}
COMPRESS = BASIS["year_days"] / 365.0

SOURCES = {
    "USDA": "USDA ARS, FoodData Central, SR Legacy (2019): energy a 100 g edible portion, raw unless stated; NDB number given",
    "MW": "McCance and Widdowson's The Composition of Foods, 7th summary ed. (PHE/RSC 2015; CoFID 2021): edible portions",
    "FAO-fish": "FAO Fisheries Technical Paper 309 (1989), Yield and nutritional value of the commercially more important fish species",
    "FAO-WHO": "FAO/WHO/UNU, Human energy requirements, FAO Food and Nutrition Technical Report 1 (2004)",
    "Compendium": "Ainsworth et al., 2011 Compendium of Physical Activities (METs for farming, hand tools, hunting, fishing)",
    "Titow": "J. Z. Titow, Winchester Yields (1972): seed ratios and yields an acre on the bishop's estates, 1209 to 1349",
    "Campbell": "B. M. S. Campbell, English Seigniorial Agriculture 1250-1450 (2000): yields, seeding rates, crop mixes",
    "Clark": "G. Clark, 'Labour productivity in English agriculture, 1300-1860', in Campbell and Overton (eds), Land, Labour and "
             "Livestock (1991): days an acre by task",
    "Henley": "Walter of Henley's Husbandry and the Seneschaucy (c. 1280; ed. Oschinsky 1971): a plough's acre a day; dairy yields",
    "Langdon": "J. Langdon, Horses, Oxen and Technological Innovation (1986): plough teams and their work",
    "Kelly": "R. L. Kelly, The Lifeways of Hunter-Gatherers (2nd ed. 2013), ch. 3, return rates by resource (post-encounter, "
             "kcal an hour)",
    "Simms": "S. R. Simms, Behavioral Ecology and Hunter-Gatherer Foraging (BAR S381, 1987): Great Basin return rates",
    "Hill": "Hill, Kaplan, Hawkes and Hurtado, 'Foraging decisions among Ache hunter-gatherers', Ethology and Sociobiology 8 (1987)",
    "Holst": "D. Holst, 'Hazelnut economy of early Holocene hunter-gatherers', Journal of Archaeological Science 37 (2010)",
    "Mitchell": "Mitchell, Staines and Welch, Ecology of Red Deer (1977); BDS larder weights; carcass yields of red and roe deer",
    "Albarella": "U. Albarella, 'Size, power, wool and veal: zooarchaeological evidence for late medieval innovations' (1997); "
                 "medieval cattle withers heights, so live weights of about 250 to 350 kg",
    "Trow-Smith": "R. Trow-Smith, A History of British Livestock Husbandry to 1700 (1957): medieval milk yields",
    "Poole": "Poole et al., 'Long-term variation in numbers and biomass of silver eels being produced in two European river "
             "systems', ICES J. Mar. Sci. 75 (2018): Burrishoole over 4,000 silver eels a year before 1982, about 2,000 after; "
             "1.1 to 1.2 kg/ha a year",
    "Tesch": "F.-W. Tesch, The Eel (5th ed. 2003): silver eel sizes (males about 0.1 kg, females 0.3 to 1.5 kg)",
    "WGEEL": "ICES WGEEL reports: glass eel recruitment since 1980 at a few to ten per cent of 1960-79 levels",
    "Darby": "H. C. Darby, The Domesday Geography of Eastern England (1952, 1971): eel renders in sticks of 25; mills and fisheries "
             "rendering hundreds to thousands of eels a year",
    "Bush": "River Bush salmon station (AFBI, Northern Ireland; Hansard written answers 1990-95): wild smolts 17,000 to 23,000 a "
            "year (1987-91), sea catch of Bush fish about 4,800 to 5,900 (1987-89); catchment about 340 km2 (recalled)",
    "quern": "ethnographic and experimental quern rates: about 1 to 2 kg of grain an hour by rotary quern (estimate from the "
             "experimental literature; check)",
    "est": "estimate (no table gives it): the reasoning is in the note",
}

# ------------------------------------------------------------------------------------------------------------- the goods
# kcal: a 100 g edible portion (low, mid, high); edible: the share of the good as a unit that is eaten; unit: what one unit is.
# now: the engine's food a unit (ITEMS, runs-models b3013b98), raw where it has one. design: a factor the game keeps on purpose
# (part 3); rec: the recommended food a unit (physical x design, at the default basis), None where it follows a rule below.
G = lambda kcal, edible, unit, src, conf, now, now_raw=None, design=1.0, note="": dict(
    kcal=kcal, edible=edible, unit=unit, src=src, conf=conf, now=now, now_raw=now_raw, design=design, note=note)
GOODS = {
    # grain and bread: the units are grain-equivalents (1 grain -> 1 meal or flour -> 1 bread, as the engine's techniques have it);
    # the energy is the grain's, the ladder is the design factor (D2-60, D4-107: whole grain boiled 0.53 of the full value)
    "grain":  G((327, 340, 389), 0.92, "1 kg threshed grain (barley, oats, wheat)", "USDA 20004 barley hulled 354, 20072 wheat "
                "hard red winter 327, 20038 oats 389; edible 0.92 (oat and barley husk)", "standard", 0.7, 0.2, 0.56,
                "boiled whole: the ladder's bottom rung (D2-60)"),
    "rye":    G((325, 338, 345), 1.0, "1 kg threshed rye", "USDA 20062 rye grain 338", "standard", 0.7, 0.2, 0.52, "as grain"),
    "beans":  G((330, 341, 350), 1.0, "1 kg dried shelled beans or peas", "USDA 16052 broad beans mature 341; 16085 split peas 341",
                "standard", 0.6, 0.0, 0.53, "boiled: the same rung as whole grain; D2-53 'less food' kept or not (part 3)"),
    "meal":   G((330, 340, 350), 1.0, "the meal of 1 kg grain (hand-ground, unsifted)", "USDA 20080 whole-wheat flour 340", "standard",
                1.0, 0.5, 0.74, "porridge (D2-167): the middle rung"),
    "flour":  G((340, 350, 364), 0.97, "the flour of 1 kg grain (mill, lightly sifted)", "USDA 20080 340, 20481 white 364",
                "standard", 1.0, 0.5, 0.74, "porridge or bread: the middle rung"),
    "bread":  G((247, 252, 266), 1.40, "the bread of 1 kg flour (about 1.4 kg of loaves)", "USDA 18075 whole-wheat bread 252; 1 kg "
                "flour bakes about 1.4 kg", "standard", 1.3, None, 1.0, "the top rung: the grain's whole energy (no gain past it)"),
    "green grain": G((40, 60, 90), 1.0, "1 kg of green ears and straw", "est (green cereal forage, mostly water)", "estimate", 0.15),
    "green rye": G((40, 60, 90), 1.0, "as green grain", "est", "estimate", 0.15),
    "green beans": G((60, 90, 120), 0.6, "1 kg green pods", "USDA 11052 snap beans 31; broad beans immature 11088 72", "estimate", 0.3),
    # meat and fish: the unit is a kcal-standard kg of edible meat (1,500 kcal) or fish (1,150 kcal), so each kill's food is its
    # own and the weight is within about a quarter of the real (lean venison heavier than its units, fat beef lighter)
    "meat":   G((114, 150, 250), 1.0, "1,500 kcal of edible meat (about 1 kg: 1.25 kg venison, 0.6 kg fat beef)",
                "USDA 17164 deer 120, 17165 wild boar 122, 13000s beef composite 200-290, 17178 rabbit wild 114", "standard",
                1.5, 0.8, 1.0, "cooked; raw 0.53 of cooked kept as a design factor (fire matters)"),
    "drying meat": G(None, None, "meat on the rack", "rule 5", "rule", 1.5, 0.8),
    "smoking meat": G(None, None, "meat in the smoke", "rule 5", "rule", 1.5, 0.8),
    "dried meat": G(None, None, "half the weight of the meat that made it", "rule 5 (D2-62)", "rule", 3.0),
    "smoked meat": G(None, None, "half the weight of the meat that made it", "rule 5", "rule", 3.0),
    "salt meat": G(None, None, "meat salted in a tub, the same weight", "rule 5", "rule", 1.4, 0.6),
    "fish":   G((88, 115, 184), 1.0, "1,150 kcal of edible fish (about 1 kg gutted and headed river fish)", "USDA 15xxx trout "
                "rainbow wild 119, pike 88, perch 91, carp 127, eel 15025 184, Atlantic salmon wild 15076 142", "standard",
                1.0, 0.6, 1.0, "cooked; raw 0.6 of cooked kept"),
    "salt fish": G(None, None, "fish salted, the same weight", "rule 5", "rule", 1.0, 0.6),
    "drying fish": G(None, None, "fish on the rack", "rule 5", "rule", 1.0, 0.6),
    "smoking fish": G(None, None, "fish in the smoke", "rule 5", "rule", 1.0, 0.6),
    "dried fish": G(None, None, "half the weight", "rule 5", "rule", 2.0),
    "smoked fish": G(None, None, "half the weight", "rule 5", "rule", 2.0),
    # dairy and eggs
    "milk":   G((61, 64, 70), 1.0, "1 kg whole cow's milk", "USDA 01077 whole milk 61; medieval milk fatter (Trow-Smith)", "standard", 0.5),
    "cheese": G((330, 400, 410), 1.0, "1 kg hard cheese (from about 10 kg milk)", "USDA 01009 cheddar 403; skim-milk hard cheese "
                "about 330", "standard", 2.5, None, 1.0, "the engine's 6 milk to a cheese becomes 10 (part 2)"),
    "egg":    G((143, 143, 150), 0.88, "1 kg eggs in shell (about 20 medieval eggs)", "USDA 01123 egg whole raw 143; shell 0.12 (MW)",
                "standard", 0.6, 0.5, 1.0, "the engine's egg unit is on the old compressed clock (part 2)"),
    # wild plants (the unit is 1 kg as gathered)
    "greens": G((22, 35, 42), 0.8, "1 kg nettle tops, sorrel, ramsons", "USDA 35205 nettles blanched 42; 11616 dock 22", "standard", 0.6),
    "roots":  G((50, 80, 110), 0.8, "1 kg pignut and silverweed roots", "est: no table; comparable roots USDA 11298 parsnip 75, "
                "11104 burdock 72", "estimate", 0.8, 0.4),
    "mushrooms": G((22, 32, 38), 0.9, "1 kg ceps, chanterelles, field mushrooms", "USDA 11239 chanterelle 32 (38 in some "
                   "releases), 11260 white mushroom 22", "standard", 0.6, 0.3),
    "watercress": G((11, 11, 20), 0.85, "1 kg watercress and brooklime", "USDA 11591 watercress 11", "standard", 0.4),
    "samphire": G((15, 22, 30), 0.85, "1 kg marsh samphire", "est: no USDA row; about 20 to 25 kcal (glasswort composition)",
                  "estimate", 0.5, 0.4),
    "berries": G((32, 45, 57), 0.95, "1 kg brambles, bilberries, wild strawberries", "USDA 09042 blackberries 43, 09050 "
                 "blueberries 57, 09316 strawberries 32", "standard", 0.8),
    "hedge fruit": G((50, 75, 162), 0.7, "1 kg crab apples, sloes, haws, hips", "USDA 09003 apple 52 (crab 76), 09136 rose hips "
                     "162; stones and cores 0.3", "standard", 0.6, 0.3),
    "hazel nuts": G((628, 628, 646), 0.43, "1 kg hazel nuts in shell", "USDA 12120 hazelnuts 628; kernel 0.40 to 0.45 of the "
                    "nut in shell", "standard", 1.6),
    "beech nuts": G((576, 576, 576), 0.6, "1 kg beech mast in husk", "USDA 12014 beechnuts dried 576; kernel about 0.6", "standard", 1.2),
    "acorns": G((387, 387, 387), 0.75, "1 kg acorns in shell, unleached", "USDA 12058 acorns raw 387; bitter until leached", "standard",
                0.1, None, 0.035, "raw acorns kept almost inedible (tannin): a physical fact, stated as a factor"),
    "acorn meal": G(None, None, "the leached meal of 1.5 kg acorns (3 acorns make 2)", "USDA 12060 acorn flour 501; leaching "
                    "loses about 15%", "estimate", 1.0),
    "wild food": G(None, None, "a legacy gathered mix (older worlds)", "the autumn mix below", "rule", 1.0),
    "tallow": G((900, 900, 902), 1.0, "1 kg rendered or raw fat", "USDA 04001 beef tallow 902", "standard", 0.0, None, 0.0,
                "kept inedible on purpose: it is the lights' good (brief 3 §5); real fat is the densest food there is"),
    "offal":  G(None, None, "what is left of a carcass", "engine", "rule", 0.0),
}


def phys(name, b=BASIS) -> float | None:
    """Food a unit on the physical basis alone (kcal a kg x the edible share / kcal a food), mid value."""
    g = GOODS[name]
    if not g["kcal"]:
        return None
    return g["kcal"][1] * 10.0 * g["edible"] / b["kcal_food"]


def rec(name, b=BASIS) -> float:
    """The recommended food a unit: the physical value x the design factor, or the processing rule (rule 5) for kept goods."""
    rule = {"drying meat": ("meat", 1.0), "smoking meat": ("meat", 1.0), "dried meat": ("meat", 2.0), "smoked meat": ("meat", 2.0),
            "salt meat": ("meat", 0.95), "salt fish": ("fish", 1.0), "drying fish": ("fish", 1.0), "smoking fish": ("fish", 1.0),
            "dried fish": ("fish", 2.0), "smoked fish": ("fish", 2.0), "offal": (None, 0.0)}
    if name in rule:
        base, k = rule[name]
        return round(rec(base, b) * k, 3) if base else 0.0
    if name == "acorn meal":                          # 3 kg acorns -> 2 units: 3 x 0.75 x 3,870 kcal x 0.85 kept, over 2
        return round(3 * 0.75 * 3870 * 0.85 / 2 / b["kcal_food"], 3)
    if name == "wild food":
        return round(sum(w * rec(k, b) for k, w in AUTUMN_MIX.items()), 3)
    if name in ("grain", "rye", "beans", "meal", "flour"):     # the ladder (D2-60, D4-107) on the bread rung's physical value
        top = rec("bread", b)                                  # the grain's whole energy, a grain-equivalent unit
        return round(top * {"grain": 0.7, "rye": 0.7, "beans": 0.6, "meal": 1.0, "flour": 1.0}[name] / 1.3, 3) \
            if name != "beans" else round(phys("beans", b) * 0.53, 3)
    if name == "bread":                                        # the flour's energy, less about 2% in the baking
        return round(phys("flour", b) * 0.98, 3)
    if name in ("meat", "fish"):                               # the kcal-standard units
        return round({"meat": 1500.0, "fish": 1150.0}[name] / b["kcal_food"], 3)
    p = phys(name, b)
    return round(p * GOODS[name]["design"], 3)


def rec_raw(name, b=BASIS):
    g = GOODS[name]
    if g["now_raw"] is None:
        return None
    return round(rec(name, b) * g["now_raw"] / g["now"], 3) if g["now"] else None


# ------------------------------------------------------------------------------------------------------------- the animals
# live kg (low, mid, high), the dressing share (carcass of live), the edible share of the carcass (boneless meat and fat), edible
# offal (share of live), kcal a kg of what is eaten; goods_now: the engine's goods a head (wild/kinds.py TAKEN, TECHNIQUES slaughter)
A = lambda live, dress, edible, offal, kcal, good, now, src, conf, note="": dict(live=live, dress=dress, edible=edible, offal=offal,
                                                                                  kcal=kcal, good=good, now=now, src=src, conf=conf,
                                                                                  note=note)
ANIMALS = {
    "red deer":   A((60, 90, 150), 0.57, 0.75, 0.03, 1200, "meat", 20.0, "Mitchell; USDA 17164", "standard",
                    "engine mass 90 (a hind to a woodland stag); larder weight about 0.7 of live, carcass 0.55 to 0.6"),
    "roe deer":   A((18, 22, 30), 0.60, 0.72, 0.03, 1200, "meat", 4.5, "Mitchell (roe); USDA 17164", "standard"),
    "wild boar":  A((50, 70, 120), 0.68, 0.70, 0.03, 1600, "meat", 15.0, "USDA 17165 wild boar 122 lean; autumn fat raises it",
                    "standard"),
    "brown hare": A((3.0, 3.5, 4.5), 0.60, 0.75, 0.02, 1140, "meat", 0.7, "USDA 17178 rabbit wild 114", "standard"),
    "woodpigeon": A((0.45, 0.5, 0.55), 0.50, 0.70, 0.0, 1420, "meat", 0.1, "USDA 05153 squab meat 142", "standard"),
    "wildfowl":   A((0.9, 1.1, 1.3), 0.60, 0.70, 0.0, 1700, "meat", 0.3, "USDA 05141 duck wild meat 123, with skin 211",
                    "standard", "a mallard; geese are four times as much"),
    "brown bear": A((150, 250, 350), 0.60, 0.70, 0.03, 1610, "meat", 40.0, "USDA 17146 bear 161", "standard"),
    "eel":        A((0.1, 0.5, 1.5), 1.0, 0.72, 0.0, 1840, "fish", 0.2, "Tesch (sizes); USDA 15025 eel 184 (checked); FAO-fish "
                    "edible about 0.7", "checked",
                    "engine mass 0.5; a run's mean is nearer 0.2 to 0.4 kg where males are many (Tesch)"),
    "salmon":     A((2.0, 4.0, 8.0), 1.0, 0.62, 0.0, 1420, "fish", 2.0, "USDA 15076 Atlantic salmon wild 142; FAO-fish edible "
                    "0.6 to 0.65", "standard", "grilse 2 to 3.5 kg, multi-sea-winter 4 to 8"),
    "lamprey":    A((0.05, 0.15, 1.5), 1.0, 0.8, 0.0, 2000, "fish", 0.3, "est (lampreys are fatty; no USDA row)", "estimate",
                    "the engine gives it meat 0.3; river lamprey 0.05 to 0.15 kg, sea lamprey 1 to 2"),
    "cow":        A((250, 300, 350), 0.50, 0.70, 0.03, 2000, "meat", 40.0, "Albarella (size); beef carcass yields; USDA beef "
                    "composite", "standard", "slaughter gives 40 meat, 2 hide, 4 tallow"),
    "ox":         A((350, 400, 500), 0.52, 0.70, 0.03, 2000, "meat", 50.0, "as cow", "standard"),
    "young":      A((80, 120, 160), 0.55, 0.70, 0.04, 1500, "meat", 10.0, "as cow (a calf or yearling)", "estimate"),
}


def kill_kcal(kind, which=1) -> float:
    a = ANIMALS[kind]
    live = a["live"][which]
    return live * (a["dress"] * a["edible"] + a["offal"]) * a["kcal"]


def kill_food(kind, b=BASIS, which=1) -> float:
    return kill_kcal(kind, which) / b["kcal_food"]


def kill_goods_rec(kind) -> float:
    """The recommended goods a head, in the kcal-standard units (meat 1,500 kcal, fish 1,150)."""
    a = ANIMALS[kind]
    return kill_kcal(kind) / {"meat": 1500.0, "fish": 1150.0}[a["good"]]


def kill_food_now(kind) -> float:
    a = ANIMALS[kind]
    v = {"meat": 1.5, "fish": 1.0}[a["good"]]
    if kind == "lamprey":
        v = 1.5                                     # the engine's lamprey gives meat
    return a["now"] * v


# ------------------------------------------------------------------------------------------------------------- the methods
# now: the engine's food a unit of work, measured (02zzd 9 Nov; hunt_calibration 4c targets and gate; 38.73 the river gate) or from
# its data; goods: what it yields, so "after" = now x (food a unit of those goods after / before) at the same kg a unit; real:
# kcal an hour (low, high) from the source; rate_fix: a kg-a-unit change recommended where the real rate is far from the engine's.
M = lambda now, goods, real, src, conf, note="", rate_fix=None: dict(now=now, goods=goods, real=real, src=src, conf=conf, note=note,
                                                                    rate_fix=rate_fix)
AUTUMN_MIX = {"hazel nuts": 0.30, "acorns": 0.25, "mushrooms": 0.15, "hedge fruit": 0.12, "berries": 0.10, "roots": 0.08}
SPRING_MIX = {"greens": 0.55, "roots": 0.25, "watercress": 0.10, "mushrooms": 0.10}
WINTER_MIX = {"roots": 0.5, "hedge fruit": 0.3, "hazel nuts": 0.1, "acorns": 0.1}
METHODS = {
    "farming, unbroken ground, crude reap": M((1.77, 1.77), {"grain": 1}, (2000, 4500), "Titow; Campbell; Clark", "standard",
        "seed ratio 3.5 to 4; 10 to 11 person-days an acre with the plough; the hoe 25 to 30"),
    "farming, hoe-broken": M((1.37, 1.37), {"grain": 1}, (1500, 3000), "Clark; est (spade or hoe 1/20 to 1/10 acre a day)", "estimate"),
    "farming, plough-broken": M((2.35, 2.35), {"grain": 1}, (4000, 7000), "Titow; Clark; Henley (an acre a day a team)", "standard"),
    "farming, plough and copper reap": M((2.80, 2.80), {"grain": 1}, (4500, 7500), "as above", "standard"),
    "milking (3 cows a unit)": M((2.4, 2.4), {"milk": 1}, (8000, 14000), "Trow-Smith (about 3 kg a cow a day); hand milking 6 to "
        "10 cows an hour", "estimate", "milking alone, not the herd's keep", rate_fix={"milk_each": 3.0, "cows_a_unit": 6}),
    "gathering, autumn": M((1.07, 1.72), AUTUMN_MIX, (1000, 3000), "Holst (hazel); Kelly (nuts, acorns 1,000 to 1,500 with "
        "leaching)", "standard", "novice to skilled; mostly nuts"),
    "gathering, spring and summer": M((0.28, 0.77), SPRING_MIX, (300, 1400), "est: greens 2 to 4 kg an hour at 300 kcal/kg; "
        "berries 1 to 3 kg an hour at 450", "estimate", "", rate_fix={"ease": 2.5}),
    "gathering, winter": M((0.19, 0.43), WINTER_MIX, (150, 800), "est", "estimate"),
    "leach acorns (3 -> 2 meal, 1 unit)": M((1.7, 1.7), {"acorn meal": 2, "acorns": -3}, (1000, 1800), "Kelly (acorns with "
        "processing)", "standard", "the gain a unit of leaching"),
    "hunting, novice armed, near": M((0.2, 0.3), {"meat": 1}, (100, 400), "Hill (Ache: misses most trips); Kelly", "standard",
        "4c target"),
    "hunting, capable armed, near": M((0.7, 0.7), {"meat": 1}, (500, 1500), "Hill; Kelly", "standard", "4c target"),
    "hunting, master armed, near": M((2.5, 2.5), {"meat": 1}, (1500, 4000), "Hill (Ache men about 1,300 kcal an hour hunting, "
        "best hunters more); Kelly (deer post-encounter 18,000 to 31,000)", "standard", "4c target (D2-255)"),
    "snares, lifted (hares)": M((0.9, 0.9), {"meat": 1}, (500, 1500), "Simms (jackrabbit 13,500 post-encounter; snaring by "
        "line)", "estimate", "the wild region run"),
    "netting fowl (2 units)": M((0.11, 0.70), {"meat": 1}, (300, 2700), "Simms (ducks 1,975 to 2,700 post-encounter)", "standard",
        "38.73's 0.15 to 0.93 meat an act"),
    "fish by hand (full stock)": M((0.6, 0.6), {"fish": 1}, (200, 900), "est (groping, tickling: 0.2 to 0.8 kg an hour)", "estimate"),
    "angling (rod and line)": M((1.5, 1.5), {"fish": 1}, (300, 1800), "Kelly (hook and line, wide range)", "standard"),
    "eel trap, resident (a night)": M((0.02, 0.08), {"fish": 1}, (200, 1500), "est", "estimate", "02zzd; eels 0.1 then"),
    "trap in a mill race, run night": M((1.1, 6.5), {"eel": 1}, (5000, 40000), "Darby (a mill's eels); est", "estimate", "38.73"),
    "weir, eel run night (3 units)": M((0.3, 1.4), {"eel": 1}, (5000, 40000), "Darby; Poole; est", "estimate", "38.73 Saltwell"),
    "weir, salmon run night (3 units)": M((4.5, 5.5), {"salmon": 1}, (5000, 60000), "Bush; est", "estimate",
        "38.73 Millham, before D2-210's hold"),
    "hand mill (3 grain -> 3 meal)": M((0.9, 0.9), {"meal": 3, "grain": -3}, (0, 0), "quern: 1 to 2 kg an hour", "estimate",
        "physically no food is made: the work saved is the mill's worth"),
    "ox mill (64 grain, 2 units)": M((9.6, 9.6), {"flour": 32, "grain": -32}, (0, 0), "D4-97, D4-107", "rule"),
    "water mill (200 grain, 2 units)": M((30.0, 30.0), {"flour": 100, "grain": -100}, (0, 0), "D4-97, D4-107", "rule"),
    "baking at a hearth (10 flour, 1 unit)": M((3.0, 3.0), {"bread": 10, "flour": -10}, (0, 0), "D2-60", "rule"),
    "oven bread (100 flour, 3 units)": M((10.0, 10.0), {"bread": 33.3, "flour": -33.3}, (0, 0), "D4-97", "rule"),
}


def per_kg_now(goods) -> float:
    return sum(w * {"eel": 1.0, "salmon": 1.0}.get(k, GOODS[k]["now"] if k in GOODS else 0.0) for k, w in goods.items())


def per_kg_rec(goods, b=BASIS) -> float:
    out = 0.0
    for k, w in goods.items():
        if k == "eel":
            out += w * kill_food("eel", b) / kill_food_now("eel")
        elif k == "salmon":
            out += w * kill_food("salmon", b) / kill_food_now("salmon")
        else:
            out += w * rec(k, b)
    return out


def method_after(name, b=BASIS) -> tuple:
    """(now low, now high, after low, after high, real low, real high, after with the rate fix) in food a unit of work."""
    m = METHODS[name]
    goods = m["goods"]
    if name.startswith("hunting") or name.startswith("snares") or name.startswith("netting"):
        f = _hunt_factor(HUNT_MIX[name], b)
    else:
        n = per_kg_now(goods)
        f = per_kg_rec(goods, b) / n if n else 1.0
    lo, hi = m["now"]
    real = tuple(r * b["hours_unit"] / b["kcal_food"] for r in m["real"])
    fix = None
    if m.get("rate_fix") and "ease" in m["rate_fix"]:
        fix = (lo * f * m["rate_fix"]["ease"], hi * f * m["rate_fix"]["ease"])
    if m.get("rate_fix") and "milk_each" in m["rate_fix"]:
        k = m["rate_fix"]["milk_each"] * m["rate_fix"]["cows_a_unit"] / (1.6 * 3)
        fix = (lo * f * k, hi * f * k)
    return lo, hi, lo * f, hi * f, real[0], real[1], fix


# the hunt: food a kill moves by kind; the near hunt's take is mostly roe and hares for the capable, deer for the master (4c)
def _hunt_factor(mix, b=BASIS) -> float:
    now = sum(w * kill_food_now(k) for k, w in mix.items())
    new = sum(w * kill_food(k, b) for k, w in mix.items())
    return new / now


HUNT_MIX = {                                   # what each hunter's take is, by food (4c's targets; an assumption)
    "hunting, novice armed, near": {"brown hare": 0.7, "woodpigeon": 0.2, "roe deer": 0.1},
    "hunting, capable armed, near": {"roe deer": 0.5, "brown hare": 0.4, "woodpigeon": 0.1},
    "hunting, master armed, near": {"red deer": 0.4, "roe deer": 0.4, "wild boar": 0.2},
    "snares, lifted (hares)": {"brown hare": 1.0},
    "netting fowl (2 units)": {"wildfowl": 1.0},
}


# ------------------------------------------------------------------------------------------------------------- the check
def breakeven(b=BASIS, units=6) -> dict:
    """The food a unit of work must give: the worker alone, and a household of five with two workers (two adults, an elder,
    two children), each working `units` a day."""
    fk = b["kcal_food"]
    base = b["base_kcal"] / fk
    w = b["work_kcal_h"] * b["hours_unit"] / fk
    sh = b["shares"]
    self_ = base / units + w
    hh = (2 * base + sh["elder"] * base + 2 * sh["child"] * base) / (2 * units) + w
    return {"ration": round(base, 3), "work_food": round(w, 3), "self": round(self_, 3), "household": round(hh, 3),
            "day_6_units": round(base + 6 * w, 3)}


def verdict(after, real, be) -> str:
    lo, hi = after
    rlo, rhi = real
    out = []
    if hi < be["self"]:
        out.append("never pays (below the worker's own need)")
    elif hi < be["household"]:
        out.append("feeds the worker, not a household")
    if rhi > 0 and lo > 2.0 * rhi:
        out.append("absurdly rich (over twice the real top)")
    if rhi > 0 and hi < 0.5 * rlo:
        out.append("far below the real rate")
    if rhi == 0 and lo > 0:
        out.append("a design gain: physically no food is made")
    return "; ".join(out) or "pays, within the real range"


# ------------------------------------------------------------------------------------------------------------- the runs
REAL_RUNS = {   # a real river's yearly runs a km2 of catchment (low, mid, high), before compression
    "eel": {"heads_km2": (20, 50, 150), "src": "Poole (Burrishoole about 2,000 to 4,000+ a year from about 90 km2: 22 to 45); "
            "WGEEL (pre-1980 recruitment several times today's)", "conf": "standard (Burrishoole); estimate (the high end)"},
    "salmon": {"heads_km2": (5, 10, 20), "src": "Bush (about 20,000 smolts and 5,000+ adults taken at sea from about 340 km2)",
               "conf": "estimate"},
}
WEIR = {"share": 0.30, "hold_food": 10.0, "build_units": 24, "timber": 12, "fell_units_a_timber": 2 / 3.0, "upkeep_share": 0.45,
        "shut_units": 2, "open_units": 1, "lift_units": 1, "hold_kg_rec": 30.0}


def weir_year(heads, nights, value, b=BASIS, hold_food=None) -> dict:
    """A one-section wattle weir's year at a station from its run heads by night {kind: [heads a night]}: the catch (the share,
    capped by the hold each night), the work (upkeep 45% of its build a year, shut and opened once, lifted each run night)."""
    hold = WEIR["hold_food"] if hold_food is None else hold_food
    food = 0.0
    n_nights = 0
    for d in range(nights):
        want = sum(WEIR["share"] * heads[k][d] * value[k] for k in heads)
        if want > 1e-9:
            n_nights += 1
        food += min(want, hold if hold else want)
    build = WEIR["build_units"] + WEIR["timber"] * WEIR["fell_units_a_timber"]
    work = WEIR["upkeep_share"] * build + WEIR["shut_units"] + WEIR["open_units"] + WEIR["lift_units"] * n_nights
    return {"food": round(food, 1), "run_nights": n_nights, "work": round(work, 1), "food_a_unit": round(food / work, 2),
            "first_year_food_a_unit": round(food / (work + (1 - WEIR["upkeep_share"]) * build), 2)}


def runs_mode(world, villages, days=36):
    """Step a world night by night with no one acting; record each village's run pulses (heads) by kind and direction."""
    root = os.environ.get("CYB_ROOT")
    sys.path.insert(0, root)
    import numpy as np  # noqa: F401
    import yaml
    from cybertron2.engine import night as NI, run as R, wild as WL
    from cybertron2.engine.world import World
    from cybertron2.wild import runs as RU
    w = World(yaml.safe_load(open(world)))
    m = WL.model(w)
    nt = RU.net(m)
    info = {}
    for v in villages:
        g = f"v:{v}"
        up = nt.upstream(g)
        info[v] = {"river_km_here": round(nt.km[g], 2), "stretches_above": len(up), "river_km_above": round(sum(nt.km[h] for h in up), 1),
                   "catchment_km2": round(sum(float(m.km2[nt.ix[a]]) for h in up for a in nt.members[h]), 1)}
    nights = []
    for d in range(days):
        w.s["day"] = d
        w.s["today"] = R.blank_today()
        w.s["events"] = []
        R.dawn(w)
        st = w.s["wild"]["state"]
        run = {}
        for p in RU.today(m, st, WL.eco_day(w)):
            if p["g"][2:] in villages:
                key = f"{p['g'][2:]}|{p['k']}|{'held' if p.get('held') else p['dir']}"
                run[key] = round(run.get(key, 0.0) + float(p["n"]), 2)
        cal = w.calendar()
        nights.append({"d": d, "cal": f"{cal['season']} {cal['day']}", "run": run})
        NI.night(w)
    return {"world": os.path.basename(world), "villages": info, "nights": nights}


def weir_analysis(rec_runs, b=BASIS) -> list:
    """Each station's weir year: as built, with the eel and salmon values on the basis, with the hold in kilograms, and with
    the run sizes of a real river of its catchment (compressed to the engine's year, the nights as the engine has them)."""
    rows = []
    for v, inf in rec_runs["villages"].items():
        N = len(rec_runs["nights"])
        heads = {"eel": [0.0] * N, "salmon": [0.0] * N}
        for i, n in enumerate(rec_runs["nights"]):
            for key, q in n["run"].items():
                vv, k, how = key.split("|")
                if vv == v and k in heads and how != "held":    # a weir below a dam does not see the held fish twice
                    heads[k][i] += q
        tot = {k: round(sum(x), 1) for k, x in heads.items()}
        now_v = {"eel": kill_food_now("eel"), "salmon": kill_food_now("salmon")}
        new_v = {"eel": kill_food("eel", b), "salmon": kill_food("salmon", b)}
        kg = {"eel": ANIMALS["eel"]["live"][1], "salmon": ANIMALS["salmon"]["live"][1]}
        hold_kg_food = None                                        # the hold in kg: what 30 kg of the night's mix is worth
        r = {"village": v, **inf, "heads_year": tot,
             "now": weir_year(heads, N, now_v, b),
             "values on the basis": weir_year(heads, N, new_v, b)}
        mix_eel = WEIR["hold_kg_rec"] / kg["eel"] * new_v["eel"]
        mix_sal = WEIR["hold_kg_rec"] / kg["salmon"] * new_v["salmon"]
        hold_kg_food = min(mix_eel, mix_sal) if tot["salmon"] > 0 else mix_eel
        r["values and a 30 kg hold"] = weir_year(heads, N, new_v, b, hold_food=hold_kg_food)
        for lab, ix in (("real run, low", 0), ("real run, mid", 1), ("real run, high", 2)):
            sc = {}
            for k in heads:
                want = REAL_RUNS[k]["heads_km2"][ix] * inf["catchment_km2"] * COMPRESS
                have = sum(heads[k])
                f = want / have if have > 0.5 else 0.0
                sc[k] = [x * f for x in heads[k]]
                if have <= 0.5 and want > 0 and k == "salmon":       # no salmon reach it in the engine: spread over the eel nights
                    en = [i for i, x in enumerate(heads["eel"]) if x > 0] or [0]
                    sc[k] = [want / len(en) if i in en else 0.0 for i in range(N)]
            r[lab] = {"heads_year": {k: round(sum(x), 0) for k, x in sc.items()},
                      **weir_year(sc, N, new_v, b, hold_food=hold_kg_food)}
        rows.append(r)
    return rows


# ------------------------------------------------------------------------------------------------------------- capacity
REC_PATCH = {                     # the recommended set (part 2's last column), for the capacity model, in memory only
    "items": None,                # filled from rec() at run time
    "taken": {"red deer", "roe deer", "wild boar", "brown hare", "woodpigeon", "wildfowl", "brown bear", "eel", "salmon", "lamprey"},
    "slaughter": {"cows": "cow", "oxen": "ox", "bulls": "ox", "young": "young"},
    "milk_each": 3.0, "milk_cows": 6, "cheese_milk": 10,
}


def patch_engine(level="goods"):
    """Write the recommended values into the engine's tables in memory: goods ('goods'), or goods and needs ('needs')."""
    from cybertron2.engine import data as D
    for name, row in D.ITEMS.items():
        if name in GOODS and float(row.get("food", 0) or 0) > 0:
            row["food"] = rec(name)
            if "raw" in row and rec_raw(name) is not None:
                row["raw"] = rec_raw(name)
    for kind in REC_PATCH["taken"]:
        r = (D.RESOURCES.get(kind) or {}).get("taken")
        if r:
            good = "fish" if ANIMALS[kind]["good"] == "fish" else "meat"
            r["goods"] = {**{k: v for k, v in r["goods"].items() if k not in ("meat", "fish")}, good: round(kill_goods_rec(kind), 3)}
    sl = D.TECHNIQUES["slaughter"]["yield"]["gives"]
    for herd, kind in REC_PATCH["slaughter"].items():
        sl[herd]["meat"] = round(kill_goods_rec(kind), 1)
    D.TECHNIQUES["milk"]["yield"]["each"] = REC_PATCH["milk_each"]
    D.TECHNIQUES["milk"]["yield"]["cows"] = REC_PATCH["milk_cows"]
    D.TECHNIQUES["cheese"]["inputs"]["milk"] = REC_PATCH["cheese_milk"]
    if level == "needs":
        be = breakeven()
        D.PHYSICS["ration"] = be["ration"]
        D.PHYSICS["labour"]["work_food"] = be["work_food"]
        D.LIFE["dial"]["low"]["child_eats"] = BASIS["shares"]["child"]
        D.LIFE["infant"]["eats"] = BASIS["shares"]["infant"]
        D.LIFE["pregnancy"]["food"] = BASIS["shares"]["pregnant_add"]


def capacity_one(path, level):
    """One world's capacity in a fresh interpreter state (the tables are patched in memory before the world is built)."""
    root = os.environ.get("CYB_ROOT")
    sys.path.insert(0, root)
    if level != "now":
        patch_engine(level)
    from cybertron2.capacity import __main__ as CM, model as M
    name, spec = CM.load(path)
    if not spec.get("nodes") or not spec.get("agents"):
        return {"world": name, "skipped": True}
    w = M.world_of(spec)
    rep = M.analyse(w)
    out = {"world": name, "people": sum(int(n["people"]) for k, n in rep["nodes"].items() if k != "(region)"), "levels": {}, "nodes": {}}
    reg = rep["nodes"]["(region)"]
    for l, v in reg["levels"].items():
        out["levels"][l] = {"supported": v["supported"], "ratio": v["ratio"], "food_a_unit": v["at_supported"]["recurring"]["food_a_unit"],
                            "food_a_plot": v["at_supported"]["land"]["field_food_a_plot"], "food_a_year": v.get("food_a_year")}
    for nid, n in rep["nodes"].items():
        if nid == "(region)" or not n["people"]:
            continue
        out["nodes"][nid] = {"people": n["people"], **{l: {"supported": v["supported"], "ratio": v["ratio"], "food_a_year": v.get("food_a_year")}
                                                        for l, v in n["levels"].items() if l in ("standing", "worked", "best")}}
    return out


# ------------------------------------------------------------------------------------------------------------- output
def table(b=BASIS) -> dict:
    goods = {}
    for k, g in GOODS.items():
        p = phys(k, b)
        r = rec(k, b)
        goods[k] = {"unit": g["unit"], "kcal_100g": g["kcal"], "edible": g["edible"], "kcal_a_unit": round(p * b["kcal_food"]) if p else None,
                    "now": g["now"], "now_raw": g["now_raw"], "physical": round(p, 3) if p is not None else None,
                    "design_factor": g["design"], "recommended": r, "recommended_raw": rec_raw(k, b),
                    "factor": round(r / g["now"], 2) if g["now"] else None, "source": g["src"], "confidence": g["conf"], "note": g["note"]}
    animals = {}
    for k, a in ANIMALS.items():
        animals[k] = {"live_kg": a["live"], "dressing": a["dress"], "edible_of_carcass": a["edible"], "offal_of_live": a["offal"],
                      "kcal_a_kg_eaten": a["kcal"], "edible_kg": round(a["live"][1] * (a["dress"] * a["edible"] + a["offal"]), 2),
                      "food_a_head_now": round(kill_food_now(k), 3), "food_a_head_basis": round(kill_food(k, b), 3),
                      "food_a_head_range": [round(kill_food(k, b, 0), 3), round(kill_food(k, b, 2), 3)],
                      "factor": round(kill_food(k, b) / kill_food_now(k), 2), "good": a["good"], "goods_now": a["now"],
                      "goods_recommended": round(kill_goods_rec(k), 2), "source": a["src"], "confidence": a["conf"], "note": a["note"]}
    be = breakeven(b)
    methods = {}
    for k, m in METHODS.items():
        lo, hi, alo, ahi, rlo, rhi, fix = method_after(k, b)
        methods[k] = {"now": [round(lo, 2), round(hi, 2)], "after": [round(alo, 2), round(ahi, 2)],
                      "after_with_rate_fix": [round(fix[0], 2), round(fix[1], 2)] if fix else None,
                      "real_kcal_an_hour": list(m["real"]), "real_food_a_unit": [round(rlo, 2), round(rhi, 2)],
                      "verdict_after": verdict((alo, ahi) if not fix else fix, (rlo, rhi), be),
                      "source": m["src"], "confidence": m["conf"], "note": m["note"]}
    return {"basis": b, "breakeven": be, "goods": goods, "animals": animals, "methods": methods, "sources": SOURCES,
            "real_runs": REAL_RUNS, "weir": WEIR, "compress": round(COMPRESS, 4)}


def load_out() -> dict:
    return json.load(open(OUT)) if os.path.exists(OUT) else {}


def save(d):
    with open(OUT, "w") as f:
        json.dump(d, f, indent=1, default=str)


def md_goods(t):
    print("| Good | Unit | kcal/100 g | Edible | Now | Physical | Design | Recommended | Factor | Confidence |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for k, g in t["goods"].items():
        kc = "-" if not g["kcal_100g"] else f"{g['kcal_100g'][1]} ({g['kcal_100g'][0]}-{g['kcal_100g'][2]})"
        print(f"| {k} | {g['unit']} | {kc} | {g['edible'] or '-'} | {g['now']} | {g['physical'] if g['physical'] is not None else '-'} | "
              f"{g['design_factor']} | {g['recommended']} | {g['factor'] or '-'} | {g['confidence']} |")


def md_animals(t):
    print("| Kind | Live kg | Dressing | Edible of carcass | kcal/kg | Edible kg | Food now | Food on the basis (range) | Factor |"
          " Goods now | Goods rec. |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for k, a in t["animals"].items():
        print(f"| {k} | {a['live_kg'][1]} ({a['live_kg'][0]}-{a['live_kg'][2]}) | {a['dressing']} | {a['edible_of_carcass']} | "
              f"{a['kcal_a_kg_eaten']} | {a['edible_kg']} | {a['food_a_head_now']} | {a['food_a_head_basis']} "
              f"({a['food_a_head_range'][0]}-{a['food_a_head_range'][1]}) | {a['factor']} | {a['goods_now']} {a['good']} | "
              f"{a['goods_recommended']} |")


def md_methods(t):
    print("| Method | Now | After (values) | After with the rate fix | Real | Verdict after |")
    print("|---|---|---|---|---|---|")
    for k, m in t["methods"].items():
        f = lambda x: f"{x[0]:g}" if x[0] == x[1] else f"{x[0]:g} to {x[1]:g}"
        print(f"| {k} | {f(m['now'])} | {f(m['after'])} | {f(m['after_with_rate_fix']) if m['after_with_rate_fix'] else '-'} | "
              f"{f(m['real_food_a_unit']) if m['real_kcal_an_hour'][1] else 'none'} | {m['verdict_after']} |")


def main(argv):
    mode = argv[1] if len(argv) > 1 else "table"
    if mode == "table":
        d = load_out()
        d["table"] = table()
        save(d)
        t = d["table"]
        print("breakeven", t["breakeven"])
        md_goods(t)
        print()
        md_animals(t)
        print()
        md_methods(t)
    elif mode == "sens":
        rows = {}
        for kc in (2000.0, 2500.0, 3000.0):
            for h in (1.5, 2.0):
                b = dict(BASIS, kcal_food=kc, hours_unit=h)
                t = table(b)
                rows[f"{int(kc)} kcal, {h} h"] = {
                    "breakeven": t["breakeven"],
                    "goods": {k: t["goods"][k]["recommended"] for k in ("grain", "bread", "meat", "fish", "milk", "greens", "berries",
                                                                        "hazel nuts", "acorn meal")},
                    "animals": {k: t["animals"][k]["food_a_head_basis"] for k in ("red deer", "roe deer", "brown hare", "eel", "salmon",
                                                                                  "cow")},
                    "methods": {k: t["methods"][k]["after"] for k in ("farming, plough-broken", "gathering, autumn",
                                                                      "hunting, master armed, near", "angling (rod and line)")},
                    "real": {k: t["methods"][k]["real_food_a_unit"] for k in ("farming, plough-broken", "gathering, autumn",
                                                                              "hunting, master armed, near", "angling (rod and line)")}}
        d = load_out()
        d["sensitivity"] = rows
        save(d)
        print(json.dumps(rows, indent=1))
    elif mode == "engine":
        sys.path.insert(0, os.environ.get("CYB_ROOT", "."))
        from cybertron2.engine import data as D
        bad = [(k, D.ITEMS[k]["food"], g["now"]) for k, g in GOODS.items() if k in D.ITEMS and float(D.ITEMS[k]["food"]) != g["now"]]
        bad += [(k, D.RESOURCES[k]["taken"]["goods"], a["now"]) for k, a in ANIMALS.items()
                if k in D.RESOURCES and (D.RESOURCES[k].get("taken") or {}).get("goods")
                and float(sum(v for g_, v in D.RESOURCES[k]["taken"]["goods"].items() if g_ in ("meat", "fish"))) != a["now"]]
        missing = [k for k, v in D.ITEMS.items() if float(v.get("food", 0) or 0) > 0 and k not in GOODS]
        print("differences from the engine:", bad or "none")
        print("edible goods not in the table:", missing or "none")
    elif mode == "runs":
        world, villages = argv[2], argv[3].split(",")
        days = int(argv[4]) if len(argv) > 4 else 36
        r = runs_mode(world, villages, days)
        d = load_out()
        d.setdefault("runs", {})[r["world"]] = {**r, "weir": weir_analysis(r)}
        save(d)
        print(json.dumps(d["runs"][r["world"]]["weir"], indent=1))
    elif mode == "weir":                       # recompute the weir from the recorded pulses (no engine needed)
        d = load_out()
        for k, r in (d.get("runs") or {}).items():
            r["weir"] = weir_analysis(r)
        save(d)
        print(json.dumps({k: r["weir"] for k, r in d.get("runs", {}).items()}, indent=1))
    elif mode == "capacity1":                  # one world, one level (called by `capacity` in a fresh interpreter)
        print(json.dumps(capacity_one(argv[2], argv[3])))
    elif mode == "capacity":
        import subprocess
        d = load_out()
        cap = d.setdefault("capacity", {})
        for path in argv[2:]:
            for level in ("now", "goods", "needs"):
                p = subprocess.run([sys.executable, os.path.abspath(__file__), "capacity1", path, level], capture_output=True, text=True,
                                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
                line = [x for x in p.stdout.splitlines() if x.startswith("{")]
                if not line:
                    print(path, level, "failed", p.stderr[-800:])
                    continue
                r = json.loads(line[-1])
                cap.setdefault(r["world"], {})[level] = r
                print(r["world"], level, {l: v["supported"] for l, v in r.get("levels", {}).items()}, flush=True)
                save(d)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
