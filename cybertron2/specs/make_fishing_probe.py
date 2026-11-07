"""The water system's acceptance world (D4-103, phase 1; content: proposals/water_and_preservation.md). Writes
cybertron2/specs/fishing/{water,dry}.yaml:

    python cybertron2/specs/make_fishing_probe.py

Ferrybank: a river hamlet of three households (eight people) on a short summer's stores. The river has resident fish and a salmon
run in autumn; a mere holds fish; the saltmarsh has pans that dry salt in summer; a small field, a meadow, a copse. The two arms
are the same world: `water` turns the water system on (fishing, rods, salt pans, salting), `dry` leaves it off, so the null arm
differs only in what the water gives. 14 days from summer's first day, so the run reaches the autumn run (season 8 days).
"""
from __future__ import annotations

import copy
import os

import yaml

KNOWS = {t: {"level": "known", "skill": 1.0} for t in ("sow", "reap", "hoe", "weed")}


def person(hh, born, sex, model, rel=None, partner=None, memories=(), holdings=None, stage="adult"):
    return {"household": hh, "born": born, "stage": stage, "sex": sex, "relations": rel or {}, "memories": list(memories),
            "knows": copy.deepcopy(KNOWS), "aware_of": {}, "holdings": holdings or {}, "concerns": ["food", "family"], "parents": [],
            "partner": partner, "model": model, "born_line": hh, "kept": []}


def world(arm: str) -> dict:
    p = {
        "fb_green": {"name": "the Green", "cover": "built", "size": 2, "side": "centre", "height": 1,
                     "text": "a green above the ferry with three houses on it", "adj": ["fb_river", "fb_field", "fb_mead", "fb_copse"]},
        "fb_river": {"name": "the Wen", "cover": "water", "size": 1, "side": "west", "height": 0,
                     "text": "a broad slow river; in autumn the salmon come up it",
                     "state": {"fish": {"K": 10, "S": 10, "r": 0.3, "run_K": 40, "run_r": 0.35, "run_seasons": ["autumn"]}},
                     "adj": ["fb_marsh", "fb_mead"]},
        "fb_mere": {"name": "Black Mere", "cover": "water", "size": 1, "side": "north", "height": 0,
                    "text": "a dark mere among the reeds", "state": {"fish": {"K": 8, "S": 8, "r": 0.3}}, "adj": ["fb_copse"]},
        "fb_marsh": {"name": "the Saltings", "cover": "saltmarsh", "size": 2, "side": "south", "height": 0,
                     "text": "saltmarsh by the river's mouth, with old salt pans", "state": {"salt": {"K": 1000, "S": 1000, "r": 0.0}},
                     "adj": ["fb_river"]},
        "fb_field": {"name": "the Ferry Field", "cover": "field", "size": 2, "side": "east", "height": 1, "text": "a field in strips",
                     "state": {"crop": {"kind": "barley", "left": 40, "ripe_day": 12}}, "adj": ["fb_mead"]},
        "fb_mead": {"name": "the Mead", "cover": "meadow", "size": 2, "side": "east", "height": 0, "text": "a meadow by the river",
                    "state": {"plants": {"K": 4, "S": 4, "r": 0.3}, "grass": {"K": 40, "S": 40, "r": 0.3}}},
        "fb_copse": {"name": "Ferry Copse", "cover": "forest", "size": 1, "side": "north", "height": 1, "text": "a hazel copse",
                     "state": {"wood": {"kind": "copse"}}},
    }
    house = lambda name, hh, grain: {"name": name, "parcel": "fb_green", "household": hh, "structure": "timber",
                                     "rooms": [{"kind": "medium room"}], "fittings": {"beds": 3, "hearth": 1, "bins": 1},
                                     "stock": {"grain": grain, "firewood": 30, "timber": 4, "hide": 1}}
    w = {
        "name": f"fishing_{arm}", "seed": 811, "days": 14, "calendar": {"season": "summer", "day": 1, "season_days": 8},
        "children": {"on": False}, "lifespan": 96, "view": "beliefs", "evening": True, "tags": True, "ages": True,
        "llm": {"week_stop": 0.9}, "cold_days": [], "incidents": [], "herds": {}, "claims": [], "customs": [],
        "memory": {"kept": {"words": 50}},
        "nodes": {"ferrybank": {"name": "Ferrybank", "parcels": p}},
        "roads": [],
        "buildings": {"tanner_house": house("the Tanner house", "Tanner", 30), "reeve_house": house("the Reeve house", "Reeve", 30),
                      "ferry_house": house("the Ferry house", "Ferry", 20)},
        "agents": {
            "Roger": person("Reeve", -40, "m", "claude-opus-5-5", {"Maud": "your wife"}, "Maud",
                            ["The Reeves hold the Ferry Field.", "The Wen runs below the green; Black Mere lies past the copse."]),
            "Maud": person("Reeve", -38, "f", "claude-sonnet-5-5", {"Roger": "your husband"}, "Roger", ["You keep the Reeve house."]),
            "Wat": person("Reeve", -16, "m", "claude-haiku-5-5", {"Roger": "your father"}, None, ["You are the Reeves' son."], stage="youth"),
            "Simon": person("Tanner", -35, "m", "claude-sonnet-5-5", {"Avice": "your wife"}, "Avice",
                            ["The Tanners work hides and keep a strip of the Ferry Field."]),
            "Avice": person("Tanner", -33, "f", "claude-haiku-5-5", {"Simon": "your husband"}, "Simon", ["You keep the Tanner house."]),
            "Ivo": person("Ferry", -30, "m", "claude-opus-5-5", {"Joan": "your wife"}, "Joan",
                          ["The Ferrys work the ferry across the Wen; few cross now."]),
            "Joan": person("Ferry", -28, "f", "claude-haiku-5-5", {"Ivo": "your husband"}, "Ivo", ["You keep the Ferry house."]),
            "Agnes": person("Ferry", -15, "f", "claude-sonnet-5-5", {"Ivo": "your father"}, None, ["You are the Ferrys' daughter."],
                            stage="youth"),
        },
    }
    if arm == "water":
        w["systems"] = ["water"]
    return w


if __name__ == "__main__":
    os.makedirs("cybertron2/specs/fishing", exist_ok=True)
    for arm in ("water", "dry"):
        with open(f"cybertron2/specs/fishing/{arm}.yaml", "w") as f:
            f.write(f"# Written by cybertron2/specs/make_fishing_probe.py (D4-103 phase 1): the {arm} arm.\n")
            yaml.safe_dump(world(arm), f, sort_keys=False)
        print(f"cybertron2/specs/fishing/{arm}.yaml")
