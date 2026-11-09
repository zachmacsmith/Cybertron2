"""Test worlds for the wild layer's build briefs 1 and 2 (proposals/methods_and_encounters.md, wild_raiders_and_works.md;
docs/review/37_growth/02zy_wild_test_worlds.md says what each tests, what to read and what passes).

Every world is the generated village of live run 6 (wild_probe6.json: Meadcombe and Brookford, a wood between Middle Field and
East Field, water at Brookford, 19 people) with a few changes, and arms that differ in one thing only. Named people do scripted
acts (`script`, done first each day); everyone else is a scripted bot in dry runs (`run.run(spec, out, days=..., bots=True,
seed=...)`). The worlds use the method names of brief 1 and the fittings of brief 2, so they run only once those are built.

    python3 cybertron2/specs/make_wild_tests.py            # writes cybertron2/specs/wild_tests/*.json
"""
from __future__ import annotations

import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "wild_probe6.json")
OUT = os.path.join(HERE, "wild_tests")
# Found by 37.4 running these arms after brief 2 (9 Nov; 02zx, brief 2): T3's stoat goes for neither village on seeds 7 to 9;
# T5's owl takes a hole only in spring (T5 runs late summer into autumn); T6's boar live near neither village in this land
# (T6 tests gadding only); these need another world or season to test.
SEEDS = [7, 8, 9]                   # run each arm on each seed: the wild layer's nights depend mostly on the seed (run 6)
EEL_GOOD = "meat"                   # an eel trap's catch (37.4: the eel's taken goods are meat, 0.1 a lift)

MEADCOMBE_HEADS = {"Holt": "Ivy", "Wood": "Osric", "Carter": "Petronel"}
BROOKFORD_HEADS = {"Moor": "Everard", "Dyer": "Alys", "Cotter": "Matthew"}
HOUSES = {"Holt": "Holt House", "Wood": "Wood House", "Carter": "Carter House",
          "Moor": "Moor House", "Dyer": "Dyer House", "Cotter": "Cotter House"}


def base(name, season="spring", day=2, days=8):
    w = json.load(open(BASE))
    w["name"] = name
    w["days"] = days
    w["calendar"] = {"season": season, "day": day, "season_days": 8}
    w["script"] = []
    w["bot_reap"] = "ripe"               # test bots leave green corn standing (37.4, brief 2 gate)
    return w


def every_day(w, who, act, days=None, start=1):
    for d in range(start, (days or w["days"]) + 1):
        w["script"].append({"day": d, "who": who, "do": dict(act)})


def write(w, arm):
    os.makedirs(OUT, exist_ok=True)
    w = copy.deepcopy(w)
    w["name"] = f"{w['name']}_{arm}"
    path = os.path.join(OUT, f"{w['name']}.json")
    with open(path, "w") as f:
        json.dump(w, f, indent=1)
    return path


# ---------------------------------------------------------------------- T1: displacement at the fields (brief 2 §2, §3)
def t1_displacement():
    """Middle Field and East Field both border East Wood. Arm `none`: nobody watches. Arm `watch_middle`: Middle Field is guarded
    every night. Arm `watch_both`: both are. Expect: with only Middle watched, East loses more than in `none` (the raiders and the
    pigeon flock turned at Middle go to East); with both watched, both lose less (the shared problem has a shared answer)."""
    out = []
    for arm in ("none", "watch_middle", "watch_east", "watch_both"):
        w = base("t1_displacement")
        crop = {"kind": "barley", "left": 240, "ripe_day": 20}          # both fields young corn through the test (37.4)
        for pid in ("s1_1", "s1_8"):
            w["nodes"]["s1"]["parcels"][pid]["state"] = {"crop": dict(crop)}
        if arm in ("watch_middle", "watch_both"):
            every_day(w, "Thomasin", {"do": "work", "what": "guard the field", "at": "Middle Field"})
        if arm in ("watch_east", "watch_both"):
            every_day(w, "Osric", {"do": "work", "what": "guard the field", "at": "East Field"})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T2: the fox's lapse probe (brief 2 §2)
def t2_lapse_probe():
    """Three houses on the Green keep hens. Arm `all_shut`: every head shuts their house each evening. Arm `one_lax`: all but the
    Carters. Arm `none_shut`. Expect: in `one_lax` the Carters lose most, and the Holts and Woods are tried more often (and lose
    more) than in `all_shut`; the fox comes back to the house it fed at."""
    out = []
    for arm in ("all_shut", "one_lax", "none_shut"):
        w = base("t2_lapse_probe")
        w["physics"] = {"breaks": {"p": 0, "cold": 0}}   # D2-168 breaks most wattle houses in a frosty spring (Q-37)
        shut = {"all_shut": ["Holt", "Wood", "Carter"], "one_lax": ["Holt", "Wood"], "none_shut": []}[arm]
        for hh in shut:
            every_day(w, MEADCOMBE_HEADS[hh], {"do": "work", "what": "shut", "at": HOUSES[hh]})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T3: doors and gaps (brief 2 §4, K1 stoat)
def t3_gaps():
    """The same three houses, all shut every evening. Arm `wattle`: as generated. Arm `stone`: the Holt and Wood houses built of
    stone. Arm `damaged`: the Holt house damaged (condition 1). Expect: the fox is kept out of every shut sound house; the stoat
    gets into shut wattle houses and not stone ones; a damaged house lets the fox in though shut; rats and mice get into all."""
    out = []
    for arm in ("wattle", "stone", "damaged"):
        w = base("t3_gaps")
        w["physics"] = {"breaks": {"p": 0, "cold": 0}}
        if arm == "stone":
            for b in ("holt_house", "wood_house"):
                w["buildings"][b]["structure"] = "stone"
        if arm == "damaged":
            w["buildings"]["holt_house"]["condition"] = 1
        for hh in ("Holt", "Wood", "Carter"):
            every_day(w, MEADCOMBE_HEADS[hh], {"do": "work", "what": "shut", "at": HOUSES[hh]})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T4: set works (brief 2 §4)
def t4_set_works():
    """Thomasin sets snares on Meadcombe Common on days 1, 3 and 5 and checks them on days 2, 4 and 6; Everard sets eel traps in
    Brookford Water every evening and empties them each morning. Arm `robbed`: Osric (another household) tries to take from the
    Common on day 4 (he may find and take what is in a snare). Arm `unchecked`: Thomasin sets and never checks. Expect: snares catch with nobody
    there; the catch waits in the snare; Osric sometimes finds and takes it (seen as using what others hold); unchecked catches
    spoil; a snare ends after its life; the eel traps take more on eel nights."""
    out = []
    for arm in ("checked", "robbed", "unchecked"):
        w = base("t4_set_works", season="autumn", day=1)            # autumn: the eel run and the hares
        for d in (1, 3, 5):
            w["script"].append({"day": d, "who": "Thomasin", "do": {"do": "gather", "what": "snare", "at": "Meadcombe Common"}})
            if arm != "unchecked":
                w["script"].append({"day": d + 1, "who": "Thomasin", "do": {"do": "take", "item": "meat", "from": "Meadcombe Common"}})
        if arm == "robbed":
            w["script"].append({"day": 4, "who": "Osric", "do": {"do": "take", "item": "meat", "from": "Meadcombe Common"}})
        for d in range(1, w["days"] + 1):
            w["script"].append({"day": d, "who": "Everard", "do": {"do": "take", "item": EEL_GOOD, "from": "Brookford Water"}})
            w["script"].append({"day": d, "who": "Everard", "do": {"do": "gather", "what": "trap in water", "at": "Brookford Water"}})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T5: stores, the cat and the owl (brief 2 §4, K1)
def t5_stores_allies():
    """Sixteen days from late summer into autumn, so the harvest comes in and rats and mice follow it into the stores. Arm `bare`:
    as generated. Arm `kept`: Wood House has a granary, Carter House a cat, the Holt byre an owl hole. Expect: each kept store
    loses less to rats and mice than the same store in `bare`; in `bare`, a cat may settle by itself at a store with mice (D2-206)
    over the two seasons; an owl takes the hole only if no one works in the byre at night."""
    out = []
    for arm in ("bare", "kept"):
        w = base("t5_stores_allies", season="summer", day=5, days=16)
        if arm == "kept":
            w["buildings"]["wood_house"]["fittings"]["granary"] = 1
            w["buildings"]["carter_house"]["stock"]["cat"] = 1         # the cat is goods in the store (37.4, brief 2)
            w["buildings"]["holt_byre"]["fittings"]["owl hole"] = 1
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T6: summer: boar at the corn, and cattle gadding (brief 2 K1)
def t6_summer():
    """Summer, when boar raid the ripening corn and hot still days set cattle gadding. The Holt cattle graze Cow Close (no water,
    no wood beside it; East Field next door); the Wood and Carter cattle the Leaze (Hazel Copse beside it). Arm `open`: nobody
    watches. Arm `herded`: Lettice herds the Holt cattle every day. Expect: boar loss to unwatched corn in about 3 to 10% of need
    (the brief's calibration); on hot still days the Holt herd breaks into East Field and the Leaze herds do not; herded, it does
    not. Run all three seeds: hot still days depend on the weather."""
    out = []
    for arm in ("open", "herded"):
        w = base("t6_summer", season="summer", day=1)
        if arm == "herded":
            every_day(w, "Lettice", {"do": "work", "what": "herd", "at": "Cow Close"})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T7: methods, familiarity and who knows what (brief 1)
def t7_methods():
    """Brief 1's regression in play. Petronel stalks in East Wood looking for deer every day; Denise snares on the Leaze every day;
    Alys nets on Brookford Water every day. Arm `as_seeded`: knowledge as the land seeds it. Arm `taught`: on day 1 Petronel is
    taught to snare by Denise. Expect: takes by method follow the generated tables (brief 1 §4); Petronel's familiarity with red
    and roe deer rises and with it her take; the Brookford households know `net` and `trap in water` and the Meadcombe ones do not
    (unless taught); no one's system text lists a kind or a tool multiplier."""
    out = []
    for arm in ("as_seeded", "taught"):
        w = base("t7_methods")
        every_day(w, "Petronel", {"do": "gather", "what": "stalk", "at": "East Wood", "looking for": "deer"})
        every_day(w, "Denise", {"do": "gather", "what": "snare", "at": "the Leaze"})
        every_day(w, "Alys", {"do": "gather", "what": "net", "at": "Brookford Water"})
        if arm == "taught":
            w["script"].insert(0, {"day": 1, "who": "Denise", "do": {"do": "teach", "what": "snare", "to": "Petronel"}})
            w["script"].insert(1, {"day": 1, "who": "Petronel", "do": {"do": "learn", "what": "snare", "from": "Denise"}})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- T8: moles, the rooks' grubs and markers (brief 2 K1)
def t8_soil_and_markers():
    """Sixteen days of spring into summer at Brookford (spring: rook young and the marker signs; 37.4 found autumn has neither), whose Middle Wood holds a rookery on seeds 7 and 9 (seed 8 seeds none:
    run this test on 7 and 9 only). Arm `left`: nobody works Leven Meadow (beside Middle Wood) for moles; the rookery as seeded.
    Arm `worked`: Gilbert does pest work on Leven Meadow every other day; Jordan takes the young rooks (gather young) at Middle Wood
    on days 1 to 4. Expect: the meadow's mole load rises when left and falls when worked; parcels within the rookery's reach carry
    fewer grubs in `left` than in `worked` (where the rooks were taken); marker signs that name a sowing window appear to those with
    family lore."""
    out = []
    for arm in ("left", "worked"):
        w = base("t8_soil_and_markers", season="spring", day=1, days=16)
        w["seeds"] = [7, 9]
        if arm == "worked":
            for d in range(1, 17, 2):
                w["script"].append({"day": d, "who": "Gilbert", "do": {"do": "work", "what": "pest work", "at": "Leven Meadow"}})
            for d in range(1, 5):
                w["script"].append({"day": d, "who": "Jordan", "do": {"do": "gather", "what": "gather young", "at": "Middle Wood"}})
        out.append(write(w, arm))
    return out


# ---------------------------------------------------------------------- the live run (after brief 2's gate; D2-207)
def live():
    """The LLM worlds (D2-207 allows one after brief 2's gate; the second needs Zach's go). About $10 each (19 agents, 8 days).
    - `live_spring`: run 6's village and season, unchanged and unscripted, its seed (7) and cast, so it reads against run 6 (the same
      world before briefs 1 and 2): deer and the pigeon flock at the young corn, the fox at the hens, the stoat, snares, the cat.
    - `live_late_summer`: the same village from late summer into autumn: boar at the ripening corn, cattle gadding on hot still
      days (the Holt herd on Cow Close, with no water or shade), the eel run at Brookford, the harvest drawing rats and mice into the
      stores. Read what people do with the new methods, a raider moving to the neighbour's field, the fox's tries, set snares and eel
      traps, shut doors, the cat and the new kinds' signs, and whether anyone acts on a neighbour's loss (never forced)."""
    a = base("live_spring")
    a.pop("script")
    b = base("live_late_summer", season="summer", day=5)
    b.pop("script")
    return [write(a, "seed7"), write(b, "seed7")]


def main():
    paths = []
    for f in (t1_displacement, t2_lapse_probe, t3_gaps, t4_set_works, t5_stores_allies, t6_summer, t7_methods,
              t8_soil_and_markers, live):
        paths += f()
    for p in paths:
        print(os.path.relpath(p, HERE))
    print(f"{len(paths)} worlds; run each dry arm on seeds {SEEDS}")


if __name__ == "__main__":
    main()
