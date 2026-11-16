"""The fuel budget (build brief 5 §4c; proposals/river_and_water.md; D2-209): a dry run with bots over a year on any world, reporting
the firewood burned by use (the hearths, the smokehouse, the salt pan) and the woods' standing stock, what was taken and their
regrowth, by village and by wood.

    python3 -m cybertron2.fuel_budget WORLD.yaml [--days N] [--smokehouse NODE] [--salter NODE] [--glut 40] [--every 8]
                                     [--boils 1] [--fell] [--out FILE.json]

Everyone is a scripted bot (run.bot_plan), without travel and (unless `--fell`) without felling, cutting or charcoal, so the woods'
draw is the fuel's; each household's first adult keeps its hearth in firewood (gathering it when the house has under 5 cold
nights' worth). Two roles are scripted on top:
- **the smoker** (`--smokehouse NODE`): a wattle smokehouse is put up for the first household with a house at NODE (not the
  salter's, where there is another), on another
  parcel than its houses where there is one; every `--every` days a glut of `--glut` fish (meat where the water pack is off) comes
  into the smoker's hands at dawn, standing in for a run (brief 5's runs are 37.2's); the smoker hangs it, tends the fire daily,
  and keeps the smokehouse in firewood (gathering it, and putting it in its store);
- **the salter** (`--salter NODE`): a salt house with a brine pan is put on NODE's brine spring for the household that holds it (else
  the first there), its first adult taught `boil salt`; it boils `--boils` times a day (4 salt for 4 firewood each) and gathers
  firewood when the household's stores run short.

Fuel is counted as it is burned (a hook on `destroy`): `fire` (house hearths, camps and fires in the open), `smoke fire` (smokehouses),
and fuel used by a make (the salt pan: a make at a fitting with a `spring`; other makes listed apart by make, since timber is
a material there as often as a fuel). Firewood-equivalent is heat / 0.5.
Woods: each forest or scrub parcel's trees (timber), young growth and dead wood (firewood) at the start and end, what was taken
by people (an act) and by the wild (browsing, at night; a hook on `draw`), and regrowth = end - start + taken (growth, and dead
wood shed by the trees, less its rot).
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys

from cybertron2.engine import agreements as AG, keeping as KP, labour as LA, night as N, run as R, verbs as V
from cybertron2.engine.data import FITTINGS, ITEMS, TECHNIQUES
from cybertron2.engine.here import Here, Mind
from cybertron2.engine.world import World, load_spec

FUELS = ("firewood", "timber", "charcoal")
WOOD = ("wood", "young", "dead")


def _fw(item, q) -> float:
    """Firewood-equivalent of a fuel: its heat over firewood's."""
    return float(q) * float(ITEMS[item]["heat"]) / float(ITEMS["firewood"]["heat"])


def _households_at(w, node) -> list:
    out = []
    for bid, b in sorted(w.s["buildings"].items()):
        if b["node"] == node and b["fittings"].get("beds"):
            for c in w.claims_on(("building", bid)):
                if c["claimant"] in w.s["institutions"] and c["claimant"] not in out and c["grounds"] != "granted":
                    out.append(c["claimant"])
    return out


def _adult(w, household, node):
    ms = [n for n in sorted(w.living()) if w.household_of(n) == household and w.s["people"][n]["stage"] == "adult"
          and w.s["people"][n]["at"] == node]
    return ms[0] if ms else None


def place_smokehouse(spec, w, node, avoid=None):
    """A wattle smokehouse for the first household with a house at `node` (other than `avoid`, where there is one): on a parcel with
    ground and no houses, else beside them."""
    hs = _households_at(w, node)
    hh = next((h for h in hs if h != avoid and _adult(w, h, node)), hs[0])
    homes = {b["parcel"] for b in w.s["buildings"].values() if b["node"] == node and b["fittings"].get("beds")}
    from cybertron2.engine import buildings as BL
    lots = [p for p, x in sorted(w.s["parcels"].items()) if x["node"] == node and BL.ground_total(x) > 0]
    pid = next((p for p in lots if p not in homes), None) or next(iter(sorted(homes)))
    spec["buildings"]["fb_smokehouse"] = {"parcel": pid, "household": hh, "structure": "wattle", "name": f"the {hh} Smokehouse",
                                          "fittings": {"smoke racks": 1}, "stock": {"firewood": 6}}
    return "fb_smokehouse", hh


def place_salthouse(spec, w, node):
    """A salt house with a brine pan on `node`'s brine spring, for the household holding the spring's parcel, else the first there."""
    pid = next(p for p, x in sorted(w.s["parcels"].items()) if x["node"] == node and "brine" in x["res"])
    held = [c["claimant"] for c in w.claims_on(("parcel", pid)) if c["claimant"] in w.s["institutions"]]
    hh = held[0] if held else _households_at(w, node)[0]
    spec["buildings"]["fb_salthouse"] = {"parcel": pid, "household": hh, "structure": "wattle", "name": f"the {hh} Salt House",
                                         "fittings": {"brine pan": 1}, "stock": {"firewood": 10}}
    return "fb_salthouse", hh


def _woods(w) -> dict:
    out = {}
    for pid, p in sorted(w.s["parcels"].items()):
        if p["node"] in w.s["nodes"] and any(k in p["res"] for k in WOOD):
            out[pid] = {k: round(float(p["res"][k]["S"]), 2) for k in WOOD if k in p["res"]}
    return out


def _house_fuel(w, bid) -> float:
    """A house's fuel, in firewood, in its store and its woodpile at the door."""
    b = w.s["buildings"][bid]
    cids = [b["stock"]] + [cid for cid, c in w.s["containers"].items() if c.get("kind") == "pile" and c.get("door") == bid and not c.get("rack")]
    return sum(_fw(i, w.goods(cid).get(i, 0.0)) for cid in cids for i in FUELS)


def run(world_path, days=None, smokehouse=None, salter=None, glut=40.0, every=8, boils=1, seed=None, fell=False) -> dict:
    spec = load_spec(world_path)
    if seed is not None:
        spec["seed"] = int(seed)
    spec["bot_travel"] = False
    w0 = World(copy.deepcopy(spec))
    roles = {}
    if salter:
        bid, hh = place_salthouse(spec, w0, salter)
        roles["salter"] = {"bid": bid, "household": hh, "who": _adult(w0, hh, salter)}
    if smokehouse:                                                             # another household than the salter's, where there is one
        bid, hh = place_smokehouse(spec, w0, smokehouse, avoid=(roles.get("salter") or {}).get("household"))
        roles["smoker"] = {"bid": bid, "household": hh, "who": _adult(w0, hh, smokehouse)}
    w = World(spec)
    if "salter" in roles:
        who = roles["salter"]["who"]
        for t in ("boil salt", "brine pan"):
            w.apply("learn", w.at(who), person=who, tech=t, level="known", source="the fuel budget's salter")
    days = int(days or w.year_days())
    water = "smoke fish" in __import__("cybertron2.engine.packs", fromlist=["techniques"]).techniques()
    catch = "fish" if water else "meat"

    burned = {"hearths": 0.0, "smokehouse": 0.0, "salt pan": 0.0}
    other = {}                                                                 # fuel goods used by other makes, by make
    raw = {}
    pending = {}
    taken = {}

    def on_destroy(w_, call, out):
        kw = call["kw"]
        item, q = kw.get("item"), float(out or 0.0)
        if item not in FUELS or q <= 0:
            return
        why = kw.get("why")
        actor = (call.get("cause") or {}).get("actor")
        if why == "fire":
            use = "hearths"
        elif why == "smoke fire":
            use = "smokehouse"
        elif why == "used" and (call.get("cause") or {}).get("verb") == "make":
            pending.setdefault(actor, []).append((item, q))
            return
        else:
            return
        burned[use] += _fw(item, q)
        raw.setdefault(use, {})[item] = raw.setdefault(use, {}).get(item, 0.0) + q

    def on_create(w_, call, out):
        why = call["kw"].get("why")
        actor = (call.get("cause") or {}).get("actor")
        if actor in pending and why in TECHNIQUES:
            fits = (TECHNIQUES[why].get("at") or {}).get("fittings") or []
            spring = any(FITTINGS.get(f, {}).get("spring") for f in fits)
            for item, q in pending.pop(actor):
                if spring:
                    burned["salt pan"] += _fw(item, q)
                    raw.setdefault("salt pan", {})[item] = raw.setdefault("salt pan", {}).get(item, 0.0) + q
                else:                                                          # fuel or material: told apart by the reader
                    k = f"{why}: {item}"
                    other[k] = round(other.get(k, 0.0) + q, 4)

    def on_draw(w_, call, out):
        kw = call["kw"]
        if kw.get("key") in WOOD:                                             # by people (an act), or the wild (browsing, at night)
            t = taken.setdefault(kw["parcel"], {}).setdefault("people" if (call.get("cause") or {}).get("actor") else "wild", {})
            t[kw["key"]] = round(t.get(kw["key"], 0.0) + float(out or 0.0), 4)

    w.hook("after", "destroy", on_destroy)
    w.hook("after", "create", on_create)
    w.hook("after", "draw", on_draw)
    start = _woods(w)
    made = {"salt": 0.0, "smoked": 0.0, "gluts": 0, "batches": 0, "tended": 0, "fire_out": 0, "fires": 0}
    log = []
    d0 = int(w.s.get("day", 0))
    for d in range(d0, d0 + days):
        w.s["day"] = d
        w.s["events"] = []
        today = w.s["today"] = R.blank_today()
        R.dawn(w)
        names = w.agents_acting()
        plans = {n: [x for x in (R.bot_plan(w, n).get("actions") or []) if str(x.get("do")) != "travel"
                     and (fell or str(x.get("what")) not in ("fell", "cut", "charcoal"))] for n in names}
        for bid, b in sorted(w.s["buildings"].items()):                       # each household keeps its hearth in firewood
            if not (b["fittings"].get("hearth") and b["fittings"].get("beds")) or b.get("unfinished"):
                continue
            hh = next((c["claimant"] for c in w.claims_on(("building", bid)) if c["claimant"] in w.s["institutions"]), None)
            keeper = _adult(w, hh, b["node"]) if hh else None
            if keeper in plans and keeper not in [r["who"] for r in roles.values()] and _house_fuel(w, bid) < 5 * 8:
                plans[keeper] = [{"do": "gather", "what": "firewood"}, {"do": "gather", "what": "firewood"},
                                 {"do": "move", "item": "firewood", "to": "store", "at": b["name"]}] + plans[keeper]
        sm = roles.get("smoker")
        if sm and sm["who"] in names:
            who, bid = sm["who"], sm["bid"]
            if (d - d0) % int(every) == 0:
                w.s["containers"][w.hands(who)]["goods"][catch] = w.s["containers"][w.hands(who)]["goods"].get(catch, 0.0) + float(glut)
                made["gluts"] += 1
            name = w.s["buildings"][bid]["name"]
            acts = []
            if KP.active_racks(w, bid):
                acts.append({"do": "work", "what": "tend the smoke"})
            elif w.goods(w.hands(who)).get(catch, 0.0) > 1e-6:
                acts.append({"do": "make", "what": f"smoke {catch}"})
            if KP.fuel_nights(w, bid) < 4:
                acts += [{"do": "gather", "what": "firewood"}, {"do": "gather", "what": "firewood"},
                         {"do": "move", "item": "firewood", "to": "store", "at": name}]
            plans[who] = acts + plans[who]
        st = roles.get("salter")
        if st and st["who"] in names:
            who = st["who"]
            here = Here(w, who)
            from cybertron2.engine import knowledge as KN
            acts = [{"do": "make", "what": "boil salt"} for _ in range(int(boils))]
            if KN.available(here, "firewood") < 4 * int(boils) * 2:
                acts += [{"do": "gather", "what": "firewood"}] * 3 + [{"do": "move", "item": "firewood", "to": "store",
                                                                        "at": w.s["buildings"][st["bid"]]["name"]}]
            plans[who] = acts + plans[who]
        used = {n: 0 for n in names}
        budget = {n: w.units_for(n) for n in names}
        order = list(names)
        w.rng("order", d).shuffle(order)
        for i in range(max((len(p) for p in plans.values()), default=0)):
            for n in order:
                if i >= len(plans[n]) or not w.s["people"][n]["alive"]:
                    continue
                here, mind = Here(w, n), Mind(w, n)
                a = plans[n][i]
                c = V.cost(here, a)
                if used[n] + c > budget[n]:
                    continue
                res = V.do(here, mind, a)
                if not res.startswith("Refused"):
                    used[n] += c
                    if n == (sm or {}).get("who") and a.get("what") == f"smoke {catch}":
                        made["batches"] += 1
                    if n == (sm or {}).get("who") and a.get("what") == "tend the smoke":
                        made["tended"] += 1
                    if n == (st or {}).get("who") and a.get("what") == "boil salt":
                        made["salt"] += sum(float(x.split(" salt")[0].split()[-1]) for x in res.split("You made ")[1:] if " salt" in x)
        LA.close_day(w, today, used, budget, names)
        AG.settle(w)
        rec = N.night(w)
        for bid_, x in (rec.get("smokehouse") or {}).items():
            made["fire_out"] += 0 if x["lit"] else 1
        made["fires"] += len(rec.get("smokehouse_fires") or [])
        for c in w.s["containers"].values():
            rk = c.get("rack") or {}
            if rk.get("smokehouse") and rk.get("done") == d:
                made["smoked"] += float(rk.get("dried", 0.0))
        log.append({"day": d, **{k: round(v, 2) for k, v in burned.items()}})
    for actor, xs in pending.items():                                          # a make that failed: its goods spoilt
        for item, q in xs:
            other[f"(failed makes): {item}"] = round(other.get(f"(failed makes): {item}", 0.0) + q, 4)
    end = _woods(w)
    woods = {}
    for pid in sorted(set(start) | set(end)):
        p = w.s["parcels"][pid]
        s0, s1 = start.get(pid, {}), end.get(pid, {})
        tp, tw = (taken.get(pid) or {}).get("people", {}), (taken.get(pid) or {}).get("wild", {})
        woods[pid] = {"name": p["name"], "node": p["node"], "cover": p["cover"], "start": s0, "standing": s1, "taken by people": tp,
                      "taken by the wild": tw,
                      "regrowth": {k: round(s1.get(k, 0.0) - s0.get(k, 0.0) + tp.get(k, 0.0) + tw.get(k, 0.0), 2) for k in WOOD
                                   if k in s0 or k in s1}}
    by_node = {}
    for v in woods.values():
        n = by_node.setdefault(v["node"], {"start": {}, "standing": {}, "taken by people": {}, "taken by the wild": {}, "regrowth": {}})
        for part in ("start", "standing", "taken by people", "taken by the wild", "regrowth"):
            for k, q in v[part].items():
                n[part][k] = round(n[part].get(k, 0.0) + q, 2)
    stores = {}
    for b in w.s["buildings"].values():
        g = w.goods(b["stock"])
        stores[b["node"]] = round(stores.get(b["node"], 0.0) + sum(_fw(i, g.get(i, 0.0)) for i in FUELS if i in g), 2)
    return {"world": os.path.basename(world_path), "days": days, "year_days": w.year_days(), "catch": catch, "roles": roles,
            "burned": {k: round(v, 2) for k, v in burned.items()}, "burned_items": {k: {i: round(q, 2) for i, q in v.items()} for k, v in raw.items()},
            "made": {k: (round(v, 2) if isinstance(v, float) else v) for k, v in made.items()}, "other makes": other,
            "woods_by_node": by_node, "woods": woods, "fuel_in_stores_end": stores, "daily": log}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("world")
    ap.add_argument("--days", type=int)
    ap.add_argument("--smokehouse")
    ap.add_argument("--salter")
    ap.add_argument("--glut", type=float, default=40.0)
    ap.add_argument("--every", type=int, default=8)
    ap.add_argument("--boils", type=int, default=1)
    ap.add_argument("--fell", action="store_true", help="let the bots fell timber, cut young growth and burn charcoal as they choose")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    out = run(a.world, a.days, a.smokehouse, a.salter, a.glut, a.every, a.boils, a.seed, a.fell)
    txt = json.dumps(out, indent=1)
    if a.out:
        open(a.out, "w").write(txt)
    print(json.dumps({k: out[k] for k in ("world", "days", "burned", "made", "woods_by_node", "fuel_in_stores_end")}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
