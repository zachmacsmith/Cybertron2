"""Brookend: a small, well-provided village for a survival check (8 Nov; Zach: "ensure the carrying capacity is FAR above the
population and see if the small population actually survives"). Writes cybertron2/specs/plenty/brookend.yaml:

    python cybertron2/specs/make_plenty.py

Eight people in three households, each holding something the others need (docs/scenario_design.md):
- the Thornes: the East Field and the main grain store;
- the Crofts: the herd (cows and the only oxen), the pasture and the small West Field;
- the Millers: the stone mill house, with millstones and the village's only oven, and the meadow; no field, and an ox to turn the
  stones is the Crofts'.

So bread needs the Thornes' grain, the Millers' stones and the Crofts' ox. The wood and its game are common. A spring start, 32 days (a
year), the weather scheduler in a steady era (D4-109). Its capacity is checked before any run (cybertron2/capacity): as it stands it
must feed at least three times its people, and the run's own days must show no short day.
"""
from __future__ import annotations

import copy
import os

import yaml

FARM = {t: {"level": "known", "skill": 1.0} for t in ("sow", "reap", "hoe", "weed")}


def person(hh, born, sex, model, rel, partner=None, memories=(), aim=None, knows=None, holdings=None, stage="adult", role=None,
           concerns=("food", "family")):
    a = {"household": hh, "born": born, "stage": stage, "sex": sex, "relations": rel, "memories": list(memories),
         "knows": copy.deepcopy(knows if knows is not None else FARM), "aware_of": {}, "holdings": holdings or {},
         "concerns": list(concerns), "parents": [], "partner": partner, "model": model, "born_line": hh, "kept": []}
    if aim:
        a["aim"] = aim
    if role:
        a["role"] = role
    return a


def world() -> dict:
    p = {
        "bk_green": {"name": "the Green", "cover": "built", "size": 2, "side": "centre", "height": 1,
                     "text": "a green with three houses about it and the mill house at its foot",
                     "adj": ["bk_east", "bk_west", "bk_mead", "bk_wood", "bk_pasture", "bk_brook"]},
        "bk_east": {"name": "the East Field", "cover": "field", "size": 18, "side": "east", "height": 1, "holder": "Thorne",
                    "text": "a long open field in strips, the Thornes' since anyone can remember",
                    "state": {"crop": {"kind": "barley", "left": 760, "ripe_day": 9}, "last_crop": "beans"}},
        "bk_west": {"name": "the West Field", "cover": "field", "size": 8, "side": "west", "height": 1, "holder": "Croft",
                    "text": "a smaller field under the wood", "state": {"crop": {"kind": "beans", "left": 200, "ripe_day": 6}}},
        "bk_mead": {"name": "Brook Mead", "cover": "meadow", "size": 3, "side": "south", "height": 0, "holder": "Miller",
                    "text": "a hay meadow along the brook", "state": {"plants": {"K": 5, "S": 5, "r": 0.3}, "grass": {"K": 80, "S": 80, "r": 0.32}}},
        "bk_pasture": {"name": "Long Pasture", "cover": "pasture", "size": 6, "side": "north", "height": 1, "holder": "Croft",
                       "text": "the cattle's pasture, rising to the wood", "state": {"grass": {"K": 180, "S": 180, "r": 0.32},
                                                                                     "plants": {"K": 3, "S": 3, "r": 0.3}}},
        "bk_wood": {"name": "Brookend Wood", "cover": "forest", "size": 8, "side": "north", "height": 2,
                    "text": "an oak and hazel wood, common to all; deer in it",
                    "state": {"wood": {"kind": "managed wood"}, "plants": {"K": 24, "S": 24, "r": 0.3},
                              "game": {"K": 24, "S": 24, "r": 0.25}}},
        "bk_brook": {"name": "the Brook", "cover": "water", "size": 1, "side": "south", "height": 0, "text": "a clear, quick brook"},
    }
    house = lambda name, hh, structure, fittings, stock, rooms=None: {   # noqa: E731
        "name": name, "parcel": "bk_green", "household": hh, "structure": structure, "rooms": rooms or [{"kind": "medium room"}],
        "fittings": fittings, "stock": stock}
    w = {
        "name": "brookend", "seed": 4401, "days": 32, "calendar": {"season": "spring", "day": 2, "season_days": 8},
        "climate": {"era": "steady"},
        "children": {"on": False}, "lifespan": 96, "view": "beliefs", "evening": True, "tags": True, "ages": True,
        "llm": {"week_stop": 0.9}, "cold_days": [], "incidents": [], "claims": [], "memory": {"kept": {"words": 50}},
        "customs": [{"text": "In Brookend the Thornes hold the East Field, the Crofts the West Field, the pasture and the herd, and the "
                             "Millers the mill and the meadow; the wood is common to all.", "nodes": "all"}],
        "nodes": {"brookend": {"name": "Brookend", "parcels": p}},
        "roads": [],
        "herds": {"croft_herd": {"name": "the Croft cattle", "kind": "cattle", "parcel": "bk_pasture", "holder": "Croft", "cows": 10,
                                 "oxen": 2, "bulls": 1, "in_milk": 7}},
        "buildings": {
            "thorne_house": house("Thorne House", "Thorne", "timber", {"beds": 3, "hearth": 1, "bins": 2},
                                  {"grain": 170, "beans": 30, "firewood": 40, "timber": 6, "crude tool": 2}),
            "croft_house": house("Croft House", "Croft", "timber", {"beds": 3, "hearth": 1, "bins": 1},
                                 {"grain": 45, "cheese": 10, "hay": 30, "firewood": 30, "timber": 4, "hide": 2}),
            "mill_house": house("the Mill House", "Miller", "stone", {"beds": 2, "hearth": 1, "bins": 1, "millstones": 1, "oven": 1},
                                {"grain": 50, "flour": 40, "firewood": 40, "timber": 8, "stone": 6}, rooms=[{"kind": "hall"}]),
        },
        "agents": {
            "Edwin": person("Thorne", -42, "m", "claude-opus-5-5", {"Agnes": "your wife", "Tom": "your son"}, "Agnes",
                            ["The Thornes have farmed the East Field for four generations.",
                             "Last year's harvest was good; the store is full enough to see you to this one."],
                            aim="See the Thornes through the year with grain to spare, and leave the East Field in better heart than you found it.",
                            role="head", holdings={"crude tool": 1}),
            "Agnes": person("Thorne", -39, "f", "claude-sonnet-5-5", {"Edwin": "your husband", "Tom": "your son"}, "Edwin",
                            ["You keep Thorne House and its store."]),
            "Tom": person("Thorne", -17, "m", "claude-haiku-5-5", {"Edwin": "your father", "Agnes": "your mother"}, None,
                          ["You are the Thornes' son."], stage="youth"),
            "Hugh": person("Croft", -38, "m", "claude-opus-5-5", {"Mabel": "your wife", "Kit": "your son"}, "Mabel",
                           ["The Crofts' cattle are the only beasts in Brookend; the Millers' stones want an ox to turn them."],
                           aim="Raise the Croft herd and the Crofts' standing in Brookend, so the village cannot do without you.",
                           role="head", knows={**FARM, "milk": {"level": "known", "skill": 1.2}}, holdings={"crude tool": 1}),
            "Mabel": person("Croft", -35, "f", "claude-haiku-5-5", {"Hugh": "your husband", "Kit": "your son"}, "Hugh",
                            ["You keep Croft House and make the cheese."], knows={**FARM, "milk": {"level": "known", "skill": 1.2}}),
            "Kit": person("Croft", -15, "m", "claude-haiku-5-5", {"Hugh": "your father", "Mabel": "your mother"}, None,
                          ["You mind the Crofts' cattle."], stage="youth"),
            "Walter": person("Miller", -45, "m", "claude-opus-5-5", {"Joan": "your wife"}, "Joan",
                             ["Your family has kept the mill and the oven for as long as there has been a mill.",
                              "The stones are turned by an ox, and the only oxen are the Crofts'."],
                             aim="Have all Brookend grind at your mill and bake at your oven, and keep the Millers' house the first in the village.",
                             role="head", holdings={"crude tool": 1}),
            "Joan": person("Miller", -41, "f", "claude-sonnet-5-5", {"Walter": "your husband"}, "Walter",
                           ["You bake at the Mill House oven."]),
        },
    }
    return w


if __name__ == "__main__":
    os.makedirs("cybertron2/specs/plenty", exist_ok=True)
    with open("cybertron2/specs/plenty/brookend.yaml", "w") as f:
        f.write("# Written by cybertron2/specs/make_plenty.py: Brookend, a small well-provided village (a survival check).\n")
        yaml.safe_dump(world(), f, sort_keys=False)
    print("cybertron2/specs/plenty/brookend.yaml")
