"""Brief 5's test worlds (proposals/river_and_water.md §1; D2-209; WORK W-47), generated with their land kept (D2-208):

- **river**: two villages on one large river, inland, pinned so each holds what the other needs (§1):
  - Saltwell, upstream: the brine spring (§4b), and the first take of the eels' run down;
  - Millham, downstream: the water mill on the river (§3a), whose dam stands between the salmon running up and Saltwell's water
    and the upland spawning water above it;
  - the river rises in wild upland to the north (the salmon's spawning areas) and leaves the window to the south (the sea beyond).
- **lake**: a lowland village on a lake (the fowl and the freeze).
- **runs**: the runs-only world (§8), to run after the gate: three fishing stations on one large river (upper, middle, lower),
  no farming (no fields, no seed, no herds: farming rows carry no pack, so it is made impossible, not switched off), stores of
  dried meat and gathered food for late summer only, so the autumn runs and what is kept of them decide the winter.

    python3 cybertron2/specs/make_water_worlds.py [river|lake|runs ...] [--seeds 3,5,7] [--out DIR]

Generated, not run: a live run needs Zach's go. Each world starts late in summer, so a 14-day run holds the autumn run. The
brine spring is written as a parcel stock (`brine`), which the engine reads once brief 5 gives it a row (world.py loads only
known resources); fish are stocked after generation as the peoples worlds do (OPEN L-75), resident only: the runs are brief 5's
kinds (salmon, lamprey, the eel's run), not the parcel's old autumn `run_K`.
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
CALENDAR = {"season": "summer", "day": 4, "season_days": 8}     # late summer: 4 days of summer, the autumn run, the turn of winter
CAST = {"head": "claude-opus-5-5", "middle": "claude-sonnet-5-5", "rest": "claude-haiku-5-5", "youth": "claude-haiku-5-5",
        "sonnet_extra": 2}                                       # scenario_design §2: Opus at every head, Sonnet in the middle, Haiku the bulk
S = 50.0                                                         # the window's side, km (vocab DEFAULTS size_km)

RIVER_PLACES = {                            # `at` is set on the generated land's large river (river_sites), not guessed: the laid river meanders
    "Saltwell": {"households": 3, "on": "big river", "has": ["brine spring"], "within": 1.5, "food_share": 0.6},
    "Millham": {"households": 3, "on": "big river", "has": ["mill site"], "within": 1.5, "food_share": 0.6},
}
RIVER_AT_Y = {"Saltwell": 0.68, "Millham": 0.3}     # where along the river (share of the window's side, south to north)
RUNS_PLACES = {                             # three stations on the large river, `at` set on it as for the river world
    "Highpool": {"households": 3, "on": "big river", "within": 1.5, "food_share": 0.6},
    "Middleham": {"households": 3, "on": "big river", "within": 1.5, "food_share": 0.6},
    "Lowstrand": {"households": 3, "on": "big river", "within": 1.5, "food_share": 0.6},
}
RUNS_AT_Y = {"Highpool": 0.74, "Middleham": 0.5, "Lowstrand": 0.26}
RUNS_DAYS = 60                              # past a salmon return under the compressed year (D2-209: one world year, 32 days)
LAKE_PLACES = {
    "Meresby": {"households": 3, "on": "lake", "lake_km2": 2.0, "at": [25.0, 21.0], "within": 6.0, "food_share": 0.6},   # on the mere
}


def base(name: str, seed: int) -> dict:
    return {"name": name, "seed": seed, "days": DAYS, "calendar": dict(CALENDAR), "climate": {"era": "steady"},   # the weather scheduler
                                                                                       # (D4-109): rain by place, so the runs' rain cue fires
            "children": {"on": True, "dial": "low"}, "packs": ["wild", "water"],
            # the standard settings every current world carries (38.70 flaw 5; run.py's settings_line warns when one is off)
            "view": "beliefs", "evening": True, "tags": True, "ages": True, "llm": {"week_stop": 0.95},   # the weekly stop at 95% (Zach, 16 Nov; 39c1a6d)
            "bot_travel": False, "bot_reap": "ripe", "cast": dict(CAST)}


def river_spec(seed: int) -> dict:
    s = base("water_river", seed)
    s["generate"] = {
        "seed": seed, "settlements": 2, "household_size": 3, "warn_only": ["capacity"],
        "bounds": {"per_min": 2, "per_spread": 3, "children_max": 4}, "sim": {"start": -26},
        "features": [
            # one large river from the northern fells to the southern edge (the sea beyond the window)
            {"kind": "river", "name": "the_river", "through": [[0.46, 1.0], [0.5, 0.82], [0.5, 0.5], [0.52, 0.18], [0.5, 0.0]],
             "flow": "large"},
            {"kind": "system", "name": "fells", "system": "upland", "box": [0.15, 0.78, 0.85, 1.0]},
            {"kind": "massif", "name": "north_fells", "at": [0.5, 0.95], "r": 0.2, "height": 380},
            {"kind": "wild", "name": "upper_waters", "box": [0.2, 0.8, 0.8, 1.0]},        # the spawning water: no one lives there
        ],
        "places": copy.deepcopy(RIVER_PLACES)}
    return s


def runs_spec(seed: int) -> dict:
    s = base("water_runs", seed)
    s["days"] = RUNS_DAYS
    s["cast"] = {"head": "claude-sonnet-5-5", "middle": "claude-sonnet-5-5", "rest": "claude-haiku-5-5", "youth": "claude-haiku-5-5"}
    s["generate"] = {
        "seed": seed, "settlements": 3, "household_size": 3, "spacing_km": 11.0, "warn_only": ["capacity"],
        "bounds": {"per_min": 1, "per_spread": 5, "children_max": 8}, "sim": {"start": -26},   # wider than the river world's: nine
                                                                                              # households need a looser people tree
        "features": copy.deepcopy(river_spec(seed)["generate"]["features"]),
        "places": copy.deepcopy(RUNS_PLACES)}
    return s


def lake_spec(seed: int) -> dict:
    s = base("water_lake", seed)
    s["generate"] = {
        "seed": seed, "settlements": 1, "household_size": 3, "warn_only": ["capacity"],
        "bounds": {"per_min": 2, "per_spread": 3, "children_max": 4}, "sim": {"start": -26},
        "features": [
            {"kind": "lake", "name": "the_mere", "at": [0.5, 0.5], "r": 0.07},
            {"kind": "river", "name": "the_brook", "through": [[0.5, 0.9], [0.5, 0.56]], "flow": "medium"},   # feeds the mere
            {"kind": "river", "name": "the_outflow", "through": [[0.5, 0.44], [0.5, 0.0]], "flow": "medium"},
            {"kind": "system", "name": "carr", "system": "fen", "at": [0.5, 0.5], "r": 0.12},       # reed and carr round the mere
        ],
        "places": copy.deepcopy(LAKE_PLACES)}
    return s


# ---------------------------------------------------------------------- edits after generation, said here
LAKE_FISH = 7500.0    # a lake's standing stock, fish a km² (calibrate): about 150 kg a hectare at about 2 kg a fish unit (an eel 0.2, a
                      # salmon 2); a stock is not scaled by the short year (Zach, 17 Nov: "it's a pretty big lake")
LAKE_TURNOVER = 0.4   # a lake's yearly production as a share of its stock (calibrate); the flow is scaled by the 32-day year, as harvests
                      # are: r a night = 4 x production a world year / K / year_days, so the most it can give for good is about
                      # LAKE_TURNOVER x K x 32/365 a world year


def water_stocks(world: dict, year_days: int = 32) -> dict:
    """Resident fish in every water parcel (K 8 a unit of size, r 0.3, the peoples worlds' value, make_peoples.water_stocks; OPEN
    L-75); a village's largest water parcel on a lake (at least 0.5 km² in its home and ring) holds the lake's stock by area, with a
    slow regrowth (LAKE_FISH, LAKE_TURNOVER). No parcel run: brief 5's runs are kinds along the river."""
    areas = (((world.get("wild") or {}).get("land") or {}).get("areas") or {})
    lake = {}
    for a in areas.values():
        if a.get("node") and a.get("kind") in ("home", "ring"):
            lake[a["node"]] = lake.get(a["node"], 0.0) + float(a.get("lake_km2") or 0.0)
    n, lakes = 0, {}
    for nid, node in world["nodes"].items():
        water = [pid for pid, p in node["parcels"].items() if p["cover"] == "water"]
        mere = max(water, key=lambda pid: (float(node["parcels"][pid].get("size", 1)), pid)) \
            if water and lake.get(nid, 0.0) >= 0.5 else None
        for pid in water:
            p = node["parcels"][pid]
            st = p.setdefault("state", {})
            if "fish" in st:
                continue
            if pid == mere:
                k = round(LAKE_FISH * lake[nid], 0)
                prod = LAKE_TURNOVER * k * year_days / 365.0                 # a world year's most, for good
                r = round(4.0 * prod / k / year_days, 5)
                st["fish"] = {"K": k, "S": k, "r": r, "renewal": "threshold"}   # plain regrowth, no 1% refill of the gap (a "fast"
                                                                             # stock's); below 15% of K it does not come back
                lakes[node.get("name", nid)] = {"parcel": pid, "lake_km2": round(lake[nid], 2), "fish_K": k, "r": r,
                                                "most_a_year": round(prod, 0)}
            else:
                k = round(8.0 * float(p.get("size", 1)), 1)
                st["fish"] = {"K": k, "S": k, "r": 0.3}
            n += 1
    return {"water parcels stocked": n, "lakes": lakes}


FUEL = {"firewood": 30, "timber": 20}       # a house's autumn nights and the turn of winter (make_wild_region.stock_fuel)


def stock_fuel(world: dict) -> dict:
    n = 0
    for b in world["buildings"].values():
        if (b.get("fittings") or {}).get("hearth") and (b.get("fittings") or {}).get("beds") and b.get("stock") is not None:
            for g_, q in FUEL.items():
                b["stock"][g_] = b["stock"].get(g_, 0) + q
            n += 1
    return {"houses": n, **FUEL}


def _households(world: dict, node: str) -> dict:
    hh = sorted({b["household"] for b in world["buildings"].values() if (b.get("fittings") or {}).get("beds")
                 and str(b.get("parcel", "")).startswith(node + "_")})
    return {h: sorted(n for n, a in world["agents"].items() if a.get("household") == h) for h in hh}


def node_of(world: dict, name: str) -> str:
    return next(k for k, v in world["nodes"].items() if v.get("name") == name)


def spring_and_mill(world: dict) -> dict:
    """Who holds the spring and the mill. The spring's parcel goes to Saltwell's smallest household (a claim, as fields are held);
    the salter's craft is given once the engine has `boil salt` (brief 5 §4b), so the world stands on either branch. The mill is
    the generator's (pin `mill site`: millstones and a water wheel, held by the miller's household)."""
    from cybertron2.engine.data import TECHNIQUES
    out = {}
    up = node_of(world, "Saltwell")
    spring = next((pid for pid, p in world["nodes"][up]["parcels"].items() if p.get("spring") == "brine"), None)
    if spring:
        hhs = _households(world, up)
        salter = min(hhs, key=lambda h: (len(hhs[h]), h))
        world["nodes"][up]["parcels"][spring]["holder"] = salter
        world["nodes"][up]["parcels"][spring]["name"] = "the Brine Meadow"   # the generator's name may borrow another's (a "Mill Meadow")
        out["spring"] = {"parcel": spring, "name": world["nodes"][up]["parcels"][spring]["name"], "held_by": salter}
        if "boil salt" in TECHNIQUES:
            for n in hhs[salter]:
                a = world["agents"][n]
                if a.get("stage") in ("adult", "elder"):
                    a.setdefault("knows", {}).setdefault("boil salt", {"level": "known", "skill": 1.2})
            out["spring"]["salter_craft"] = True
    low = node_of(world, "Millham")
    mill = next((k for k, b in world["buildings"].items() if (b.get("fittings") or {}).get("water wheel")
                 and str(b.get("parcel", "")).startswith(low + "_")), None)
    out["mill"] = {"building": mill, "held_by": world["buildings"][mill]["household"]} if mill else None
    return out


FISHER = {"net": 1.2, "trap in water": 1.2}            # a fishing household's crafts (Zach, 16 Nov: "let a fishing household know nets and
                                                          # traps"), a stopgap for proposals/livelihood_archetypes.md


def _fish(p: dict) -> float:
    f = (p.get("state") or {}).get("fish", 0)
    return float(f.get("K", 0) if isinstance(f, dict) else f or 0)


def fishers(world: dict, every: bool = False) -> dict:
    """At each village with fish in its water, one household (its largest; `every`: all, for the runs-only world) knows nets and
    wicker traps: its adults and elders. Returns {village: [households]}."""
    out = {}
    for node, nd in world["nodes"].items():
        if not any(p["cover"] == "water" and _fish(p) > 0 for p in nd["parcels"].values()):
            continue
        hhs = _households(world, node)
        if not hhs:
            continue
        pick = sorted(hhs) if every else [max(hhs, key=lambda h: (len(hhs[h]), h))]
        for h in pick:
            for n in hhs[h]:
                a = world["agents"][n]
                if a.get("stage") in ("adult", "elder"):
                    for t, sk in FISHER.items():
                        a.setdefault("knows", {}).setdefault(t, {"level": "known", "skill": sk})
        out[nd.get("name", node)] = pick
    return out


RUNS_STORE = {"dried meat": 4, "roots": 6, "acorns": 6, "berries": 4}   # a household's late-summer larder: weeks, not a winter


def no_farming(world: dict) -> dict:
    """The runs-only world's edits after generation (§8): fields become rough ground (scrub), herds are gone, and no grain, beans,
    flour or bread is stored anywhere, so nothing can be sown or eaten from a harvest; each house holds a late-summer larder
    (RUNS_STORE) and the stocked fuel. The farming crafts stay known (they are basic and carry no pack), but with no seed, field
    or beast they lead nowhere: an engine `farming` pack would make the arm exact (handed to the building session)."""
    fields = 0
    for node in world["nodes"].values():
        for p in node["parcels"].values():
            if p["cover"] == "field":
                p["cover"] = "scrub"
                p.pop("fertility", None)
                p.pop("holder", None)
                st = p.get("state") or {}
                for k in [k for k in st if k not in ("plants", "grass", "game")]:
                    st.pop(k)
                p["text"] = "rough ground by the river: thorn, bramble and coarse grass, never ploughed"
                fields += 1
    herds = len(world.get("herds") or {})
    world["herds"] = {}
    food = 0
    for b in world["buildings"].values():
        stock = b.get("stock")
        if stock is None:
            continue
        for g_ in ("grain", "rye", "beans", "flour", "meal", "bread", "hay", "straw", "wooden plough", "harness"):
            if g_ in stock:
                food += 1
                stock.pop(g_)
        if (b.get("fittings") or {}).get("beds"):
            for g_, q in RUNS_STORE.items():
                stock[g_] = stock.get(g_, 0) + q
    for a in world["agents"].values():
        for k in ("sow", "reap", "hoe", "weed", "milk", "select seed", "plough"):
            (a.get("knows") or {}).pop(k, None)
    return {"fields to scrub": fields, "herds removed": herds, "farm goods removed": food, "larder a house": RUNS_STORE}


def runs_cast(world: dict) -> dict:
    """Opus at each station's largest household (scenario_design §2: the poles of leverage are the stations), the rest as cast."""
    out = {}
    for name in RUNS_PLACES:
        node = node_of(world, name)
        hhs = _households(world, node)
        lead = max(hhs, key=lambda h: (len(hhs[h]), h))
        for n in hhs[lead]:
            if world["agents"][n].get("model") and world["agents"][n].get("stage") in ("adult", "elder"):
                world["agents"][n]["model"] = "claude-opus-5-5"
        out[name] = lead
    return out


def runs_check(world: dict) -> dict:
    """Each station's water on the large river and the chain of areas from each station down to the next (the runs' path)."""
    from cybertron2.engine.world import World
    w = World(copy.deepcopy(world))
    land = w.s["wild"]["land"]
    names = list(RUNS_PLACES)
    out = {"big_river_km": {n: round(float(land["areas"][land["home"][node_of(world, n)]].get("big_river_km") or 0), 1) for n in names}}
    for up, low in zip(names, names[1:]):
        mine = {a for a, v in land["areas"].items() if v.get("node") == node_of(world, low) and v["kind"] in ("home", "ring")}
        x, km, n = land["home"][node_of(world, up)], 0.0, 0
        while x in land["down"] and land["down"][x] in land["areas"] and x not in mine and n < 60:
            x = land["down"][x]
            km += float(land["areas"][x].get("river_km") or 0)
            n += 1
        out[f"{up} above {low}"] = {"reached": x in mine, "river_km": round(km, 1)}
    return out


def river_check(world: dict) -> dict:
    """The river world's design, checked on the generated land: both villages on water of the large river, Saltwell's home area
    upstream of Millham's on `land.down`, the km of river between them (the run's lag, brief 5 §2), and wild water above."""
    try:
        from cybertron2.engine.world import World
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    w = World(copy.deepcopy(world))
    land = (w.s.get("wild") or {}).get("land")
    if not land:
        return {"error": "no wild land on this branch"}
    up, low = node_of(world, "Saltwell"), node_of(world, "Millham")
    a_up, a_low = land["home"][up], land["home"][low]
    down = land["down"]
    chain, x, km = [a_up], a_up, 0.0
    mine = {a for a, v in land["areas"].items() if v.get("node") == low and v["kind"] in ("home", "ring")}
    while x in down and down[x] in land["areas"] and x not in mine and len(chain) < 60:   # "out": the water leaves the window
        x = down[x]                                                          # the chain follows each area's largest river cell, so it
        chain.append(x)                                                      # passes a village's ring, beside its small home area
        km += float(land["areas"][x].get("river_km") or 0)
    a_low = x if x in mine else a_low
    above = [a for a, v in land["areas"].items() if v["kind"] == "wild" and float(v.get("big_river_km") or 0) > 0]
    big = lambda a: round(float(land["areas"][a].get("big_river_km") or 0), 1)
    return {"saltwell_area": a_up, "millham_area": a_low, "saltwell_above_millham": x in mine, "chain": chain, "areas_between": len(chain) - 2,
            "river_km_between": round(km, 1), "big_river_km": {"Saltwell": big(a_up), "Millham": big(a_low)},
            "wild_areas_on_the_big_river": len(above)}


def lake_check(world: dict) -> dict:
    node = node_of(world, "Meresby")
    water = {pid: p["size"] for pid, p in world["nodes"][node]["parcels"].items() if p["cover"] == "water"}
    try:
        from cybertron2.engine.world import World
        w = World(copy.deepcopy(world))
        land = (w.s.get("wild") or {}).get("land") or {}
        lake_km2 = round(sum(float(v.get("lake_km2") or 0) for v in land.get("areas", {}).values()     # the village's own land
                             if v.get("node") == node and v.get("kind") in ("home", "ring")), 2)                   # (home and ring), not
                                                                                                                  # the wild beyond
    except Exception as e:  # noqa: BLE001
        lake_km2 = f"error: {e}"
    return {"water_parcels": water, "lake_km2_at_home": lake_km2}


def river_sites(s: dict, at_y: dict = None) -> dict:
    """A first pass over the land alone: for each village, a cell of the main large river near its latitude (of the class-3 cells
    there, the one draining the most land); the village is pinned within 1.5 km of it, so its water parcels are on the large river
    (§1)."""
    import numpy as np
    with contextlib.redirect_stdout(io.StringIO()):
        _, cells, _ = W.generate(copy.deepcopy(s), people=False)
    x, y, r, acc = np.asarray(cells["x"]), np.asarray(cells["y"]), np.asarray(cells["river"]), np.asarray(cells["acc"])
    big = r >= 3
    out = {}
    for name, fy in (at_y or RIVER_AT_Y).items():
        for band in (1.0, 2.0, 3.0, 4.0):
            m = big & (np.abs(y - fy * S) <= band)
            if m.any():                                                    # the main river: at this latitude the one carrying the
                i = int(np.flatnonzero(m.ravel())[np.argmax(acc.ravel()[m.ravel()])])   # most water (a large tributary may be beside it)
                out[name] = [round(float(x.ravel()[i]), 2), round(float(y.ravel()[i]), 2)]
                break
    return out


def make(which: str, seed: int):
    s = {"river": river_spec, "lake": lake_spec, "runs": runs_spec}[which](seed)
    if which in ("river", "runs"):
        want = RIVER_AT_Y if which == "river" else RUNS_AT_Y
        at = river_sites(s, want)
        if len(at) < len(want):
            raise RuntimeError(f"no large river near {sorted(set(want) - set(at))}")
        for name, xy in at.items():
            s["generate"]["places"][name]["at"] = xy
    with contextlib.redirect_stdout(io.StringIO()):
        world, cells, report = W.generate(copy.deepcopy(s), people=True)
    if world.get("agents") and not report.get("refused"):
        report["water_stocks"] = water_stocks(world)
        report["fuel"] = stock_fuel(world)
        report["fishers"] = fishers(world, every=(which == "runs"))
        if which == "river":
            report["spring_and_mill"] = spring_and_mill(world)
            report["design"] = river_check(world)
        elif which == "runs":
            report["no_farming"] = no_farming(world)
            report["cast_opus"] = runs_cast(world)
            report["design"] = runs_check(world)
        else:
            report["design"] = lake_check(world)
    return s, world, cells, report


def ok(which: str, report: dict) -> bool:
    d = report.get("design") or {}
    if which == "runs":
        return all(v["reached"] for k, v in d.items() if " above " in k) and all(x > 0 for x in d["big_river_km"].values())
    if which == "river":
        sm = report.get("spring_and_mill") or {}
        return bool(d.get("saltwell_above_millham") and sm.get("spring") and sm.get("mill") and d.get("wild_areas_on_the_big_river"))
    return isinstance(d.get("lake_km2_at_home"), float) and d["lake_km2_at_home"] >= 1.0   # the mere reaches the village's land


def main():
    which = [a for a in sys.argv[1:] if a in ("river", "lake", "runs")] or ["river", "lake"]
    seeds = [3, 5, 7, 9, 11, 13, 17, 19, 23, 29]
    if "--seeds" in sys.argv:
        seeds = [int(x) for x in sys.argv[sys.argv.index("--seeds") + 1].split(",")]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(__file__), "water")
    for wh in which:
        for seed in seeds:
            try:
                s, world, cells, report = make(wh, seed)
            except Exception as e:  # noqa: BLE001
                print(wh, seed, "refused:", str(e)[:240], flush=True)
                continue
            if report.get("refused") or not world.get("agents"):
                print(wh, seed, "refused by checks:", report.get("refused"), flush=True)
                continue
            print(wh, seed, "people", len(world["agents"]), json.dumps(report.get("design")), json.dumps(report.get("spring_and_mill")),
                  flush=True)
            if not ok(wh, report):
                continue
            os.makedirs(out, exist_ok=True)
            W.write(world, cells, report, os.path.join(out, f"{wh}.yaml"), picture=os.path.join(out, f"{wh}.png"))
            print(wh, "written:", os.path.join(out, f"{wh}.yaml"), "seed", seed, flush=True)
            break


if __name__ == "__main__":
    main()
