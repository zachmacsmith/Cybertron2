"""W-82's three test worlds (bots only; worktree only). Writes runs_w82/worlds/{frontier,brookend,runs}_w82.yaml.

- frontier_w82: frontier_camps.yaml (Zach's 2 Nov world: three couples in camps that last to day 14, a scrub knoll to build on, a
  meadow to clear) without the Gorm raiders (bots do not fight; the raid is not what is read here), run for 64 days.
- brookend_w82: plenty/brookend.yaml (a settled farm village: two fields, a herd on an unfenced pasture, a mill) with a fourth
  household arrived in a camp on the Green (a couple with seed, tools and a little timber, stone and straw) and an unclaimed scrub
  parcel to clear for their field: the bot test's own fixture, for housing and clearing in a settled village. 64 days.
- runs_w82: nutrition/runs_medium.yaml (the runs world's middle arm, no weir seeded), the Brooks and Marshes able to build a weir
  together. 64 days.
"""
import copy
import sys
import yaml

SPECS = "cybertron2/specs/"


def load(p):
    return yaml.safe_load(open(SPECS + p))


def frontier():
    w = load("frontier_camps.yaml")
    w["name"], w["days"] = "frontier_w82", 64
    for n in [n for n, a in w["agents"].items() if a["household"] == "Gorm"]:
        del w["agents"][n]
    w["buildings"].pop("gorm_hall", None)
    w["customs"] = [c for c in w["customs"] if "Gorm" not in c.get("households", [])]
    for a in w["agents"].values():                     # provisioned (the fixture's departure): a season's food for the couple
        h = a["holdings"]
        if "grain" in h:
            h["grain"], h["beans"], h["dried meat"] = 80, 20, 25
    w["bot_livelihood"] = {"policy": "farm", "build": True}
    w["bot_travel"] = False
    return w


def brookend():
    w = load("plenty/brookend.yaml")
    w["name"], w["days"] = "brookend_w82", 64
    P = w["nodes"]["brookend"]["parcels"]
    P["bk_brakes"] = {"name": "the Brakes", "cover": "scrub", "size": 3, "side": "west", "height": 1,
                      "text": "thorn and bramble on the slope past the West Field, never broken",
                      "adj": ["bk_green", "bk_west", "bk_wood"],
                      "state": {"wood": {"kind": "scrub"}, "plants": {"K": 3, "S": 3, "r": 0.3}, "grass": {"K": 30, "S": 30, "r": 0.3}}}
    P["bk_green"]["adj"].append("bk_brakes")
    w["buildings"]["wright_camp"] = {"name": "the Wright camp", "parcel": "bk_green", "household": "Wright", "structure": "camp",
                                     "size": 4, "fittings": {"beds": 4, "fire ring": 1}, "lasts_until": 10,
                                     "stock": {"dried meat": 6, "firewood": 6}}
    knows = {"sow": {"level": "known", "skill": 1.0}, "reap": {"level": "known", "skill": 1.0}, "hoe": {"level": "known", "skill": 1.0},
             "weed": {"level": "known", "skill": 1.0}, "small room": {"level": "known", "skill": 1.0}, "hearth": {"level": "known", "skill": 1.0}}
    base = next(iter(w["agents"].values()))
    for who, sex, partner, born, hold in (("Robin", "m", "Alys", -36, {"crude tool": 1, "timber": 6, "stone": 4, "straw": 10}),
                                          ("Alys", "f", "Robin", -34, {"crude tool": 1, "grain": 80, "beans": 20, "dried meat": 25})):
        a = copy.deepcopy(base)
        a.update({"household": "Wright", "sex": sex, "born": born, "stage": "adult", "partner": partner, "parents": [],
                  "relations": {partner: "your wife" if sex == "m" else "your husband"}, "holdings": hold, "knows": knows,
                  "born_line": "Wright", "memories": ["The Wrights came to Brookend this spring, a young couple with seed and a few tools."]})
        w["agents"][who] = a
    w["bot_livelihood"] = {"policy": "farm", "build": True, "field_for": ["Wright"]}
    w["bot_travel"] = False
    return w


def runs():
    w = load("nutrition/runs_medium.yaml")
    w["name"], w["days"] = "runs_w82", 64
    w["bot_livelihood"] = {"policy": "runs", "build": True, "weir_by": "Brook", "weir_with": "Marsh", "projects": ["weir", "weir sections"]}
    return w


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "runs_w82/worlds/"
    for fn in (frontier, brookend, runs):
        w = fn()
        with open(out + w["name"] + ".yaml", "w") as f:
            f.write("# Written by runs_w82/worlds/make_w82_worlds.py (W-82, bots only)\n")
            yaml.safe_dump(w, f, sort_keys=False, width=140, allow_unicode=True)
        print("wrote", out + w["name"] + ".yaml")
