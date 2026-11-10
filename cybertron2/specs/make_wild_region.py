"""A wild region for testing the wild layer across villages (WORK W-29; docs/review/37_growth/02zze_wild_region.md).

Four generated villages on different land in "settled lowland and frontier":
- Corneby, a farming village whose land feeds far more than its people (food_share 0.4);
- Weirford, on a river (eels; weirs once brief 5 is built), feeding about its own;
- Holtham, at the frontier's woods (deer, boar, wolves), short of food;
- Stanmoor, in the frontier hills with the only stone and copper, far short of food.
The region as a whole feeds its starting people with room to spare. The dependence runs both ways: food from Corneby (and some
from Weirford), stone and copper only from Stanmoor, timber and game most at Holtham.

    CYB_ROOT=<checkout of the branch to run on> python3 cybertron2/specs/make_wild_region.py [--seeds 3,5,7,...] [--out DIR]

Generated, not run: a live run needs Zach's go (and comes after brief 4b). The world is written with its land (D2-208) as
`wild_region.yaml` and `wild_region.cells.npz`.
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

DAYS = 14
PLOT_SEED = 16                              # seed a plot (data.PHYSICS["farming"]["plot_seed"], D2-59)
PLACES = {                                  # food_share is the generator's measure, which counts broken and weeded fields; the engine's
                                            # capacity ladder at "standing" (the fields as they are) comes to about 0.6 of it, so the pins
                                            # are set to give, at standing: Corneby about 2.5, the rest 0.5 to 0.8, the region about 1.2
    "Corneby": {"households": 3, "food_share": 0.17, "heat_share": 0.3, "soil": "rich"},
    "Weirford": {"households": 2, "food_share": 0.75, "on": "river"},
    "Holtham": {"households": 2, "food_share": 0.85, "plenty_of": ["wood"], "at": [38.0, 10.0]},   # the frontier's woods, north of the hills
    "Stanmoor": {"households": 2, "food_share": 1.2, "resources": ["stone", "copper"], "at": "frontier_hills"},
}


def spec(seed: int) -> dict:
    return {
        "name": "wild_region", "seed": seed, "days": DAYS,
        "calendar": {"season": "winter", "day": 1, "season_days": 8},
        "children": {"on": True, "dial": "low"},
        "lifespan": 96,
        "packs": ["wild"],
        "bot_travel": False, "bot_reap": "ripe",    # dry runs only: scripted bots stay at home and reap only ripe corn (OPEN Q-35)
        "cast": {"head": "claude-opus-5-5", "middle": "claude-sonnet-5-5", "rest": "claude-haiku-5-5", "youth": "claude-haiku-5-5",
                 "sonnet_extra": 6},           # scenario_design: Opus at every head, a Sonnet middle tier, Haiku in the bulk
        "generate": {
            "seed": seed, "configuration": "settled lowland and frontier", "settlements": 4,
            "features": [{"kind": "ore", "name": "lode", "box": [0.7, 0.45, 0.98, 0.8]}],
            "places": copy.deepcopy(PLACES)}}


def wild_summary(world: dict) -> dict:
    """Each village's game and fish where the wild pack is on the branch: heads in its home area and ring, and its water."""
    try:
        from cybertron2.engine.world import World
        from cybertron2.engine import wild as WD
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    w = World(copy.deepcopy(world))
    if not (w.s.get("wild") or {}).get("state"):
        return {"error": "no wild pack on this branch"}
    m = WD.model(w)
    land, st = w.s["wild"]["land"], w.s["wild"]["state"]
    out = {}
    for node in sorted(PLACES):
        nid = next((k for k, v in w.s["nodes"].items() if v.get("name") == node or k == node), node)
        idx = [i for i, a in enumerate(m.ids) if land["areas"][a].get("node") == nid and land["areas"][a]["kind"] in ("home", "ring")]
        row = {}
        for k in ("red deer", "roe deer", "wild boar", "wolf", "fox", "brown hare", "eel", "wildfowl", "rats"):
            if k in st["pop"]:
                row[k] = round(sum(float(st["pop"][k][i]) * float(m.km2[i]) for i in idx))
        row["river_km"] = round(sum(float(land["areas"][m.ids[i]].get("river_km") or 0) for i in idx), 1)
        ring = {m.ids[i] for i in idx if land["areas"][m.ids[i]]["kind"] == "ring"}
        wild = sorted({b if a in ring else a for a, b, _ in land["links"] if (a in ring) != (b in ring)
                       and land["areas"][b if a in ring else a]["kind"] == "wild"})
        ix = {a: i for i, a in enumerate(m.ids)}
        row["wild beyond"] = {k: round(sum(float(st["pop"][k][ix[a]]) * float(m.km2[ix[a]]) for a in wild))
                              for k in ("red deer", "wild boar", "wolf") if k in st["pop"]}
        out[node] = row
    return out


def capacity(world: dict) -> dict:
    """The capacity ladder (cybertron2/capacity, D4-102): people supported and the ratio to the people there, by node and region."""
    from cybertron2.capacity import model as CM
    r = CM.analyse(copy.deepcopy(world), levels=("standing", "worked", "best"))
    return {nid: {"people": v.get("people"), **{lvl: {"supported": round(float(x.get("supported", 0)), 1), "ratio": round(float(x.get("ratio", 0)), 2)}
                                               for lvl, x in (v.get("levels") or {}).items()}}
            for nid, v in r["nodes"].items() if v.get("people") or nid == "(region)"}


def stores_by_land(world: dict) -> dict:
    """An edit after generation, said here: each village's stores hold what its land gives a day as it stands (the capacity
    ladder's "standing") times the days to its next harvest, so a village that feeds more has more in store, and one that feeds
    less runs short before the harvest (the generator gives every village about a week's stores, D2-13). Added as grain to the
    village's houses by their beds; the seed for the next sowing is in it, so eating it all leaves nothing to sow."""
    from cybertron2.capacity import model as CM
    from cybertron2.capacity import food as FD
    r = CM.analyse(copy.deepcopy(world), levels=("standing",))
    worth = FD.worth("grain", "boiled", None)[0]
    out = {}
    for node, v in r["nodes"].items():
        if node == "(region)" or not v.get("people"):
            continue
        sup = float(v["levels"]["standing"]["supported"])
        days = int((v.get("first_harvest") or {}).get("first") or 0)
        want = sup * days                                                   # food to eat until the harvest
        seed = float(PLOT_SEED) * sum(float(p_.get("size", 1)) for p_ in world["nodes"][node]["parcels"].values()
                                      if p_.get("cover") == "field")         # and the next sowing's seed, kept back
        houses = [b for b in world["buildings"].values() if b.get("stock") is not None and (b.get("fittings") or {}).get("beds")
                  and str(b.get("parcel", "")).startswith(node + "_")]
        beds = sum(int(b["fittings"]["beds"]) for b in houses) or 1
        g0 = sum(float(b["stock"].get("grain", 0)) for b in houses)
        add = max(0.0, want / worth + seed - g0)
        for b in houses:
            b["stock"]["grain"] = round(float(b["stock"].get("grain", 0)) + add * int(b["fittings"]["beds"]) / beds, 1)
        have = want
        out[node] = {"supported": round(sup, 1), "days_to_harvest": days, "food_to_harvest": round(want, 1), "seed_grain": round(seed, 1),
                     "grain_in_store": round(g0 + add, 1), "people": v["people"]}
    return out


def horizon(world: dict) -> dict:
    """The run's food horizon by village at standing practice, from the stores (the capacity tool's run_horizon)."""
    from cybertron2.capacity import model as CM
    r = CM.analyse(copy.deepcopy(world), levels=("standing",), horizon=DAYS)
    return {k: {kk: v["horizon"]["standing"].get(kk) for kk in ("first_short", "short_days", "short_meals", "store_food")}
            for k, v in r["nodes"].items() if v.get("people") and (v.get("horizon") or {}).get("standing")}


def make(seed: int):
    s = spec(seed)
    with contextlib.redirect_stdout(io.StringIO()):
        world, cells, report = W.generate(copy.deepcopy(s), people=True)
    if world.get("agents") and not report.get("refused"):
        report["stores_by_land"] = stores_by_land(world)
    return s, world, cells, report


def main():
    seeds = [3, 5, 7, 9, 11, 13, 17, 19, 23, 29]
    if "--seeds" in sys.argv:
        seeds = [int(x) for x in sys.argv[sys.argv.index("--seeds") + 1].split(",")]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(__file__), "wild_region")
    for seed in seeds:
        try:
            s, world, cells, report = make(seed)
        except Exception as e:  # noqa: BLE001
            print(seed, "refused:", str(e)[:200], flush=True)
            continue
        if report.get("refused") or not world.get("agents"):
            print(seed, "refused:", report.get("refused"), json.dumps(report["checks"].get("capacity", {}).get("detail"))[:200], flush=True)
            continue
        print(seed, "made: people", len(world["agents"]), json.dumps(report["checks"].get("capacity, people as generated", {}).get("detail")),
              flush=True)
        os.makedirs(out, exist_ok=True)
        W.write(world, cells, report, os.path.join(out, "wild_region.yaml"))
        json.dump({"seed": seed, "capacity": capacity(world), "stores": report.get("stores_by_land"), "horizon": horizon(world),
                   "wild": wild_summary(world),
                   "checks": {k: v for k, v in report["checks"].items()}}, open(os.path.join(out, "wild_region.summary.json"), "w"),
                  indent=1, default=str)
        print("written to", out)
        return
    print("no seed passed")


if __name__ == "__main__":
    main()
