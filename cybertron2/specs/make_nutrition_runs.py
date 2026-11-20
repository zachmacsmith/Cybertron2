"""The runs-only nutrition world (proposals/subsistence_worlds.md, D2-242, D2-256; WORK W-69): can a village live off the runs alone?

One fishing village on a large river with strong runs (the eels' run down in autumn, the salmon's up), the river rising in wild
upland where the salmon spawn. Nothing is farmed: no fields, seed or herds (farming carries no pack, so the world makes it impossible,
OPEN L-112). Resident fish are left out, so the runs are the fish. Game and wild plants stay at the land's own thin level, and the
people know their crafts only roughly, so the runs and what is kept of them decide the winter. (An exact arm needs per-world
switches for game and fish, 37.4's prerequisite in D2-256.)

Three arms on the same land and people, differing only in skill and capital (D2-256: seeded skill):
- low: novices; hand fishing and traps in the water known roughly; no weir, no smoke racks, no salt: nothing can be kept but by
  eating it, so the test is whether a run's glut carries a winter (it should not);
- medium: capable; traps and nets known; smoke racks at each house; no weir and no salt;
- high: masters; traps, nets, the weir, smoking and salting known well; a weir of a wattle and two timber sections built on the
  village's river water; smoke racks at each house; a salt house with a brine pan at the village's brine spring, and salt in store.

    python3 cybertron2/specs/make_nutrition_runs.py [--seeds 5,7,9] [--out DIR]

Generated, not run: a live run needs Zach's go. Two compressed years (64 days at 32 a year), from late summer, so two autumn runs
and two winters. The run sizes, the weir's hold and the food values are today's (OPEN Q-70 would raise the runs and the holds and
correct the food values); the arms are remade when it is answered.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

from cybertron2.landgen import write as W  # noqa: E402
from cybertron2.specs import make_water_worlds as WW  # noqa: E402

DAYS = 64                                     # two world years of 32 days (D2-209), two winters
PLACE = {"Eelmouth": {"households": 3, "on": "big river", "has": ["brine spring"], "within": 1.5, "food_share": 0.6}}
AT_Y = {"Eelmouth": 0.3}                       # low on the river: every eel of the catchment passes, the salmon come up past it
# the arms (D2-256): skill a craft is known at, and the capital each household holds
ARMS = {
    "low": {"level": "rough", "skill": 0.6, "crafts": ["trap in water"], "weir": None, "racks": False, "salt": False},
    "medium": {"level": "known", "skill": 1.0, "crafts": ["trap in water", "net", "smoke fish", "tend the smoke"],
               "weir": None, "racks": True, "salt": False},
    "high": {"level": "known", "skill": 1.6, "crafts": ["trap in water", "net", "weir", "smoke fish", "tend the smoke", "salt fish",
                                                        "boil salt"],
             "weir": ["wattle", "timber", "timber"], "racks": True, "salt": True},
}
SALT_STORE = 10                               # the high arm's salt house: salt for about 40 fish (salt fish: 4 fish to 1 salt)


def spec(seed: int) -> dict:
    s = WW.base("nutrition_runs", seed)
    s["days"] = DAYS
    s["lifespan"] = WW.RUNS_LIFESPAN
    s["runs_set_nights"] = True                # the runs on their windows' set nights (D2-231; the level cue, D2-215, not built)
    s["generate"] = {
        "seed": seed, "settlements": 1, "household_size": 4, "warn_only": ["capacity", "dependence", "chokepoint"],
        "bounds": {"per_min": 2, "per_spread": 3, "children_max": 18}, "sim": {"start": WW.RUNS_HISTORY},
        "features": copy.deepcopy(WW.river_spec(seed)["generate"]["features"]),
        "places": copy.deepcopy(PLACE)}
    return s


def _node(world):
    return WW.node_of(world, "Eelmouth")


def _river_water(world, nid):
    """The village's largest water parcel on the large river (where a weir stands): by river class, then size."""
    ps = [(pid, p) for pid, p in world["nodes"][nid]["parcels"].items() if p["cover"] == "water"]
    ps.sort(key=lambda x: ((x[1].get("land") or {}).get("river_class") in ("large", "big"), x[1]["size"]), reverse=True)
    return ps[0][0] if ps else None


def apply_arm(world: dict, arm: str) -> dict:
    """The arm's skill and capital, on a copy of the generated world (the land and people are shared by the arms)."""
    a = ARMS[arm]
    nid = _node(world)
    hhs = WW._households(world, nid)
    out = {"arm": arm, "households": len(hhs), "people": sum(len(v) for v in hhs.values())}
    for hh, members in hhs.items():
        for n in members:
            p = world["agents"][n]
            if p.get("stage") not in ("adult", "elder"):
                continue
            knows = p.setdefault("knows", {})
            for t in ("net", "trap in water", "weir", "smoke fish", "tend the smoke", "salt fish", "boil salt"):
                knows.pop(t, None)                                     # the arm sets these, not the generator's draw
            for t in a["crafts"]:
                knows[t] = {"level": a["level"], "skill": a["skill"]}
    houses = {hh: next((k for k, b in world["buildings"].items() if b.get("household") == hh and (b.get("fittings") or {}).get("beds")
                        and str(b.get("parcel", "")).startswith(nid + "_")), None) for hh in hhs}
    if a["racks"]:
        for hh, bid in houses.items():
            if bid:
                world["buildings"][bid].setdefault("fittings", {})["smoke racks"] = 1
        out["smoke racks"] = sum(1 for b in houses.values() if b)
    lead = max(hhs, key=lambda h: (len(hhs[h]), h))
    if a["weir"]:
        pid = _river_water(world, nid)
        if pid is None:
            raise RuntimeError("no water parcel for the weir")
        world["buildings"][f"{lead.lower()}_weir"] = {
            "parcel": pid, "node": nid, "household": lead, "name": "the weir", "structure": "timber", "monument": "weir",
            "tier": "plain", "fittings": {}, "rooms": [], "gap": "shut", "crew": [],
            "sections": [{"m": m, "foot": False, "level": 5} for m in a["weir"]]}
        out["weir"] = {"parcel": pid, "sections": a["weir"], "held_by": lead}
    if a["salt"]:
        out["salt"] = _salt_house(world, nid, lead)
    else:
        for bid in [k for k, b in world["buildings"].items() if (b.get("fittings") or {}).get("brine pan")]:
            world["buildings"].pop(bid)                                # no pan in the low and medium arms
    return out


def _salt_house(world, nid, hh):
    spring = next((pid for pid, p in world["nodes"][nid]["parcels"].items() if p.get("spring") == "brine"), None)
    if spring is None:
        return {"spring": None}
    world["nodes"][nid]["parcels"][spring]["holder"] = hh
    bid = f"{hh.lower()}_salthouse"
    world["buildings"][bid] = {"parcel": spring, "household": hh, "structure": "wattle", "name": "the Salt House",
                               "fittings": {"brine pan": 1}, "stock": {"firewood": 20, "salt": SALT_STORE}}
    return {"spring": spring, "salt_house": bid, "salt": SALT_STORE}


def check(world: dict) -> dict:
    """The village is on the large river, its water has a parcel for a weir, and the runs pass it."""
    from cybertron2.engine.world import World
    w = World(copy.deepcopy(world))
    land = w.s["wild"]["land"]
    nid = _node(world)
    home = land["areas"][land["home"][nid]]
    return {"big_river_km": round(float(home.get("big_river_km") or 0), 1), "weir_water": _river_water(world, nid),
            "spring": any(p.get("spring") == "brine" for p in world["nodes"][nid]["parcels"].values()),
            "wild_upstream": sum(1 for a in land["areas"].values() if a["kind"] == "wild" and (a.get("big_river_km") or 0) > 0)}


def make(seed: int):
    s = spec(seed)
    at = WW.river_sites(s, AT_Y)
    if "Eelmouth" not in at:
        raise RuntimeError("no large river near the village's place")
    s["generate"]["places"]["Eelmouth"]["at"] = at["Eelmouth"]
    with contextlib.redirect_stdout(io.StringIO()):
        world, cells, report = W.generate(copy.deepcopy(s), people=True)
    if not world.get("agents") or report.get("refused"):
        return s, None, None, report
    report["fuel"] = WW.stock_fuel(world)
    report["no_farming"] = WW.no_farming(world)
    report["design"] = check(world)
    return s, world, cells, report


def main():
    seeds = [5, 7, 9, 11, 13, 17]
    if "--seeds" in sys.argv:
        seeds = [int(x) for x in sys.argv[sys.argv.index("--seeds") + 1].split(",")]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(__file__), "nutrition")
    for seed in seeds:
        try:
            s, world, cells, report = make(seed)
        except Exception as e:  # noqa: BLE001
            print(seed, "refused:", str(e)[:240], flush=True)
            continue
        if world is None:
            print(seed, "refused by checks:", report.get("refused"), flush=True)
            continue
        d = report["design"]
        print(seed, "people", len(world["agents"]), json.dumps(d), flush=True)
        if not (d["big_river_km"] > 0 and d["weir_water"] and d["spring"]):
            continue
        os.makedirs(out, exist_ok=True)
        for arm in ARMS:
            wa = copy.deepcopy(world)
            ra = copy.deepcopy(report)
            ra["arm"] = apply_arm(wa, arm)
            ra["craft_gates"] = WW.craft_gates(wa)
            wa["name"] = f"nutrition_runs_{arm}"
            W.write(wa, cells, ra, os.path.join(out, f"runs_{arm}.yaml"), picture=os.path.join(out, f"runs_{arm}.png") if arm == "low" else None)
            print(" ", arm, json.dumps(ra["arm"]), "gates:", ra["craft_gates"], flush=True)
        print("written:", out, "seed", seed, flush=True)
        break


if __name__ == "__main__":
    main()
