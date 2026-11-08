"""A probe of the seasonal wild year (02zp §M4, M6b): does a hungry gap change what people do? Data only, no engine change.

Ferrybank (the water acceptance world) without the water pack, its grain cut so wild food matters, run for a whole year of 28 days
from late summer (seasons of 7). Two arms differ only in how the copse's and meadow's wild food comes back:
- flat: today's `fast` stock (K as now), the same in every season;
- seasonal: the built `periodic` rule (D4-104), a small resident stock with a run in summer and autumn; the same steady take a year
  (M6b), but almost nothing in spring.
Read: food stored before winter, wild food gathered by season, hunger in spring, gifts and trades of food, the share of actions on
food (scenario_design §4), against the flat arm."""
import copy, os, sys, yaml
sys.path.insert(0, "/home/user/cybertron2")
sys.path.insert(0, "/home/user/cybertron2/cybertron2/specs")
import make_fishing_probe as FP

def world(arm):
    w = FP.world("dry")
    w["name"] = f"wild_year_{arm}"
    w["seed"] = 913
    w["days"] = 28
    w["calendar"] = {"season": "summer", "day": 5, "season_days": 7}
    w.pop("packs", None)
    p = w["nodes"]["ferrybank"]["parcels"]
    p["fb_field"]["size"] = 6                           # enough field that worked land feeds them (scenario_design §4: 1.25x)
    p["fb_field"]["state"]["crop"]["left"] = 120
    p["fb_copse"]["text"] = "a hazel copse with brambles along its edge"
    # stores as in the water world (30, 30 and 20 grain): a summer's worth, so the year turns on the harvest and the wild year
    p["fb_copse"]["size"] = 16
    p["fb_brakes"] = {"name": "the Brakes", "cover": "scrub", "size": 8, "side": "north", "height": 1,
                      "text": "bramble and thorn brakes on the slope above the copse", "adj": ["fb_copse"]}
    p["fb_copse"].setdefault("adj", []).append("fb_brakes")
    flat = {"fb_copse": 19.0, "fb_mead": 5.0, "fb_brakes": 8.0}          # plants K as the generator would give (vocab.PER_UNIT)
    for k, K in flat.items():
        p[k].setdefault("state", {})
        if arm == "flat":
            p[k]["state"]["plants"] = {"K": K, "S": K, "r": 0.3}
        else:                                                              # the same year's take (capacity model: 0.46 vs 0.49)
            p[k]["state"]["plants"] = {"renewal": "periodic", "r": 0.3, "run_r": 0.3, "run_seasons": ["summer", "autumn"],
                                       "K": round(0.15 * K, 2), "S": round(0.26 * K, 2), "run_K": round(0.66 * K, 2)}
    return w

if __name__ == "__main__":
    for arm in ("flat", "seasonal"):
        with open(f"wild_year_{arm}.yaml", "w") as f:
            f.write(f"# A probe of the seasonal wild year (02zp): the {arm} arm. Written by make_wild_year_probe.py.\n")
            yaml.safe_dump(world(arm), f, sort_keys=False)
        print(f"wild_year_{arm}.yaml")
