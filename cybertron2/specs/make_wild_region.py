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
    "Corneby": {"households": 3, "food_share": 0.17, "soil": "rich"},
    "Weirford": {"households": 2, "food_share": 0.55, "on": "river"},
    "Holtham": {"households": 2, "food_share": 0.6, "plenty_of": ["wood"], "at": [38.0, 10.0]},   # the frontier's woods, north of the hills
    "Stanmoor": {"households": 2, "food_share": 0.65, "resources": ["stone", "copper"], "at": "frontier_hills"},
}


def spec(seed: int) -> dict:
    return {
        "name": "wild_region", "seed": seed, "days": DAYS,
        "calendar": {"season": "winter", "day": 1, "season_days": 8},
        "children": {"on": True, "dial": "low"},
        "packs": ["wild"],
        "bot_travel": False, "bot_reap": "ripe",    # dry runs only: scripted bots stay at home and reap only ripe corn (OPEN Q-35)
        "cast": {"head": "claude-opus-5-5", "middle": "claude-sonnet-5-5", "rest": "claude-haiku-5-5", "youth": "claude-haiku-5-5",
                 "sonnet_extra": 6},           # scenario_design: Opus at every head, a Sonnet middle tier, Haiku in the bulk
        "generate": {
            "seed": seed, "configuration": "settled lowland and frontier", "settlements": 4, "wild_shore": True,
            "household_size": 3, "warn_only": ["capacity"],   # the capacity ladder (D4-102), run below, is this world's check                               # small households, nearly all working adults (Zach, 10 Nov)
            "bounds": {"per_min": 2, "per_spread": 3, "children_max": 5}, "sim": {"start": -26},   # a shorter past: few elders; children as they come
            "features": [
                {"kind": "ore", "name": "lode", "box": [0.7, 0.45, 0.98, 0.8]},              # copper in the east's hills only
                # the south-west: a wild coast of saltmarsh and fen round a tidal inlet (the region's only salt)
                {"kind": "coast", "name": "west_coast", "side": "west", "at": 0.08},
                {"kind": "inlet", "name": "saltings", "from": [0.0, 0.18], "to": [0.2, 0.2], "width": 0.04, "tidal": True},
                {"kind": "system", "name": "marsh", "system": "fen", "box": [0.06, 0.04, 0.32, 0.34]},
                {"kind": "wild", "name": "southwest_marsh", "box": [0.0, 0.0, 0.34, 0.36]},
                # the north-west: wild upland moor and fells (red deer, hill grazing, stone; no ore)
                {"kind": "system", "name": "fells", "system": "upland", "box": [0.0, 0.7, 0.45, 1.0]},
                {"kind": "massif", "name": "north_fells", "at": [0.2, 0.86], "r": 0.15, "height": 520},
                {"kind": "wild", "name": "northwest_moor", "box": [0.0, 0.68, 0.46, 1.0]}],
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


def _households(world: dict, node: str) -> dict:
    """{household: [its people]} for a village, by its houses."""
    hh = sorted({b["household"] for b in world["buildings"].values() if (b.get("fittings") or {}).get("beds")
                 and str(b.get("parcel", "")).startswith(node + "_")})
    return {h: sorted(n for n, a in world["agents"].items() if a.get("household") == h) for h in hh}


CARRIER_MEMORY = ("You have lived by the roads since you were young, carrying goods between the villages and the wild places with your "
                  "oxen, buying where a thing is plentiful and selling where it is wanted. It is the life you chose, and you mean to do well "
                  "at it.")
TRADER_AIM = ("Keep your household by carrying goods along the roads between the villages and the wild places and trading them; "
              "the oxen are your living.")
def trader_knows(world: dict) -> list:
    """What years on the roads taught a carrier: true of this world, with its own names."""
    wild = {k: v for k, v in world["nodes"].items() if k.startswith("w")}
    def named(cover):
        return [v["name"] for v in wild.values() if any(p.get("cover") == cover for p in v["parcels"].values())]
    salt, rock, wood = named("saltmarsh"), named("rock"), named("forest")
    out = [
        "From years on the roads: Corneby's barns hold more grain than its people eat, and every road in the region runs through it.",
        "From years on the roads: Stanmoor in the eastern hills has copper and stone and a forge, but its fields are poor.",
        "From years on the roads: Holtham, in the south-eastern woods, has timber, hides and game, and little grain to spare.",
        "From years on the roads: Weirford, on the river below the fells, has fish, eels and wildfowl, and the only water mill.",
        "From years on the roads: a pack ox carries 60 on any road and eats hay where there is no grass on the way.",
    ]
    if salt:
        out.append(f"From years on the roads: salt is panned only on the saltmarsh at {salt[0]}, on the coast beyond Weirford; no one "
                   "lives there, and the way is little known.")
    if rock:
        out.append(f"From years on the roads: there is open rock for stone at {', '.join(rock)}, up in the fells; no one lives there.")
    if wood:
        out.append(f"From years on the roads: the deep woods at {', '.join(wood)} hold the most game; no one lives there.")
    return out


def seed_traders_and_mill(world: dict) -> dict:
    """Edits after generation, said here (Zach, 10 Nov: "seed a few people that have the pack oxes etc. to travel around and trade
    things"; "did you seed one of the villages with a mill?"):
    - a carrier household at Corneby (the crossroads) and one at Weirford (on the way to the coast): each the village's smallest
      household, with pack oxen and harness, goods to start on, the carrier's trade and aim, and what years on the roads taught them
      (memories, all true of the world);
    - a water mill at Weirford (millstones and a water wheel on its green, beside the river), held by its largest household, whose
      people know how to work and keep it."""
    out = {}
    for node, oxen, goods in (("Corneby", 2, {"coin": 30, "hide": 4}), ("Weirford", 1, {"coin": 10, "salt": 10, "salt fish": 12})):
        hhs = _households(world, node)
        hh = min(hhs, key=lambda h: (len(hhs[h]), h))
        pasture = next(pid for pid, p in sorted(world["nodes"][node]["parcels"].items()) if p.get("cover") in ("pasture", "meadow"))
        world["herds"][f"{hh.lower()}_oxen"] = {"name": f"the {hh} oxen", "kind": "cattle", "parcel": pasture, "cows": 0, "oxen": oxen,
                                                "bulls": 0, "young": 0, "in_milk": 0, "holder": hh}
        house = next(b for b in world["buildings"].values() if b.get("household") == hh and (b.get("fittings") or {}).get("beds"))
        for g_, q in {"harness": oxen, **goods}.items():
            house["stock"][g_] = house["stock"].get(g_, 0) + q
        for n in hhs[hh]:
            a = world["agents"][n]
            if a.get("stage") in ("adult", "youth", "elder"):
                a["trade"] = "carrying goods along the roads with a pack ox, and trading them"
                a["concerns"] = sorted(set(a.get("concerns") or []) | {"trade", "travel", "animals"})
                a["memories"] = list(a.get("memories") or []) + trader_knows(world)
                pl = a.setdefault("places", [])                   # the ways to the wild places: carriers know them all
                for k in sorted(world["nodes"]):
                    if world["nodes"][k].get("unexplored") and k not in pl:
                        pl.append(k)
                a["memories"].append(CARRIER_MEMORY)
        out[node] = {"carriers": hh, "people": hhs[hh], "oxen": oxen, "goods": goods}
    hhs = _households(world, "Weirford")
    miller = max((h for h in hhs if h != out["Weirford"]["carriers"]), key=lambda h: (len(hhs[h]), h))
    green = next(pid for pid, p in sorted(world["nodes"]["Weirford"]["parcels"].items()) if p.get("cover") == "built")
    world["buildings"]["weirford_mill"] = {"name": "Weirford Mill", "parcel": green, "household": miller, "structure": "timber",
                                           "size": 4, "fittings": {"millstones": 1, "water wheel": 1}, "stock": {}}
    for n in hhs[miller]:
        a = world["agents"][n]
        if a.get("stage") in ("adult", "youth", "elder"):
            k = a.setdefault("knows", {})
            for t in ("water mill", "dress millstones", "clear the leat"):
                k.setdefault(t, {"level": "known", "skill": 1.5})
            a["memories"] = list(a.get("memories") or []) + ["Your household keeps the water mill on the river at Weirford: it grinds "
                                                              "200 of grain to flour in two units' work, where a hand mill grinds 3."]
    out["mill"] = {"at": "Weirford", "held_by": miller}
    return out


GROWTH_MEMORY = ("Your grandmother bore nine children and outlived half the village, and she raised you to believe that a family which "
                 "does not grow dies out. You want a large family: many children, and their children after them. You mean to see your "
                 "blood spread out beyond the village and settle new land, more of you every year.")
MODELS = {"opus": "claude-opus-5-5", "haiku": "claude-haiku-5-5", "fable": "claude-fable-5-2"}


def cast_and_memories(world: dict) -> dict:
    """Edits after generation, said here (Zach, 10 Nov):
    - the frontier household with the youngest couple is given a planted long-term memory of wanting a large family spreading
      onto new land (a memory, as every seeded line is; aims are not shown to agents, D4-29);
    - the other Holtham household is played by Haiku alone; Corneby's largest farming household by Opus alone; the Corneby carriers'
      head by Fable 5.2;
    - each person's stated trade names what they actually know of their village's own work (mining at Stanmoor, the woods at
      Holtham, the water at Weirford), where they know it."""
    out = {}
    hol = _households(world, "Holtham")
    def youngest_couple(h):
        ages = [-world["agents"][n]["born"] for n in hol[h] if world["agents"][n].get("partner") and world["agents"][n]["stage"] == "adult"]
        return min(ages) if ages else 999
    grow = min(hol, key=lambda h: (youngest_couple(h), h))
    for n in hol[grow]:
        if world["agents"][n]["stage"] in ("adult", "youth", "elder"):
            world["agents"][n]["memories"] = list(world["agents"][n].get("memories") or []) + [GROWTH_MEMORY]
    out["growth"] = {"household": grow, "people": hol[grow]}
    haiku = next((h for h in sorted(hol) if h != grow), None)
    if haiku:
        for n in hol[haiku]:
            if world["agents"][n].get("model"):
                world["agents"][n]["model"] = MODELS["haiku"]
        out["haiku_only"] = {"household": haiku, "people": hol[haiku]}
    cor = _households(world, "Corneby")
    carriers = next(h for h, ps in cor.items() if any("carrying goods" in (world["agents"][n].get("trade") or "") for n in ps))
    opus = max((h for h in cor if h != carriers), key=lambda h: (len(cor[h]), h))
    for n in cor[opus]:
        if world["agents"][n].get("model"):
            world["agents"][n]["model"] = MODELS["opus"]
    out["opus_only"] = {"household": opus, "people": cor[opus]}
    head = next((n for n in cor[carriers] if world["agents"][n].get("role") == "head"),
                max(cor[carriers], key=lambda n: -world["agents"][n]["born"]))
    world["agents"][head]["model"] = MODELS["fable"]
    out["fable"] = head
    work = {"Stanmoor": ["mine", "smelt", "quarry"], "Holtham": ["hunt the wild", "fell", "stalk"], "Weirford": ["fish by hand", "net", "angle"]}
    from cybertron2.engine.data import TECHNIQUES
    for node, techs in work.items():
        for h, ps in _households(world, node).items():
            for n in ps:
                a = world["agents"][n]
                if a["stage"] not in ("adult", "elder") or "carrying goods" in (a.get("trade") or ""):
                    continue
                own = [t for t in techs if t in (a.get("knows") or {})]
                if own:
                    a["trade"] = " and ".join(TECHNIQUES[t]["label"].split(" (")[0] for t in own[:2])
    return out


def make(seed: int):
    s = spec(seed)
    with contextlib.redirect_stdout(io.StringIO()):
        world, cells, report = W.generate(copy.deepcopy(s), people=True)
    if world.get("agents") and not report.get("refused"):
        report["traders_and_mill"] = seed_traders_and_mill(world)
        report["cast"] = cast_and_memories(world)
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
        W.write(world, cells, report, os.path.join(out, "wild_region.yaml"), picture=os.path.join(out, "wild_region.png"))
        json.dump({"seed": seed, "capacity": capacity(world), "stores": report.get("stores_by_land"), "horizon": horizon(world),
                   "traders_and_mill": report.get("traders_and_mill"), "cast": report.get("cast"),
                   "wild": wild_summary(world),
                   "checks": {k: v for k, v in report["checks"].items()}}, open(os.path.join(out, "wild_region.summary.json"), "w"),
                  indent=1, default=str)
        print("written to", out)
        return
    print("no seed passed")


if __name__ == "__main__":
    main()
