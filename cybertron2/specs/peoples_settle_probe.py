"""Can a people settle each vacant place of a peoples world (review 38.69)? For each vacant place, on a fresh copy of the world: one
grown person of the first people walks in carrying what a settler would bring (timber, stone, straw, grain, a crude tool), then, as
acts through the engine's verbs, one after another (units are not counted: this tests the gates, not the time):
  clear ground to build on; build a room (wattle) and a hearth; found a household; claim the room and the ground; clear ground for a
  field; sow it; and the place's own work: fell, quarry, mine, the salt pan, fishing, forage, by its covers.
    python3 cybertron2/specs/peoples_settle_probe.py cybertron2/specs/peoples/w1.yaml"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys

sys.path.insert(0, __file__.rsplit("/cybertron2/", 1)[0])
from cybertron2.engine import run as R, verbs as V  # noqa: E402
from cybertron2.engine.here import Here, Mind  # noqa: E402
from cybertron2.engine.world import World, load_spec  # noqa: E402

KIT = {"timber": 30, "stone": 12, "straw": 6, "grain": 20, "crude tool": 1, "firewood": 10}
OWN = {"forest": [("gather", "fell")], "rock": [("gather", "quarry"), ("gather", "mine")], "saltmarsh": [("gather", "salt pan")],
       "water": [("gather", "angle"), ("gather", "fish by hand")], "meadow": [("gather", "hay")], "heath": [("gather", "forage")],
       "fen": [("gather", "forage")], "moor": [("gather", "forage")], "pasture": [("gather", "forage")]}


def act(w, who, a):
    try:
        return V.do(Here(w, who), Mind(w, who), a)
    except Exception as e:                                                 # noqa: BLE001 (a crash is a finding)
        return f"CRASH {type(e).__name__}: {e}"


def ok(r):
    return not str(r).startswith(("Refused", "CRASH", "Not done"))


def probe(spec):
    with contextlib.redirect_stdout(io.StringIO()):
        base = World(copy.deepcopy(spec))
    base.s["today"] = R.blank_today()
    settler = sorted(n for n, p in base.s["people"].items() if p.get("stage") == "adult")[0]
    homes = {b["node"] for b in base.s["buildings"].values()}
    out = {}
    for nid, node in sorted(base.s["nodes"].items()):
        if nid in homes or not str(node.get("text", "")).startswith("land no one"):
            continue
        w = copy.deepcopy(base)
        w.s["people"][settler]["at"] = nid
        for item, q in KIT.items():
            w.s["containers"][w.hands(settler)]["goods"][item] = q
        pars = {pid: p for pid, p in w.s["parcels"].items() if p["node"] == nid}
        name = lambda cover: next((p["name"] for p in pars.values() if p["cover"] == cover), None)
        clearing = min((p for p in pars.values() if p["cover"] in ("meadow", "pasture", "scrub")), key=lambda p: p["size"], default=None)
        site = clearing["name"] if clearing else None                      # the smallest open parcel: the clearing to build on
        open_ = next((p["name"] for p in sorted(pars.values(), key=lambda p: -p["size"]) if p["cover"] in ("pasture", "meadow", "scrub")), None)
        steps = []

        def step(label, a, times=1, done=None, who=None):
            """Repeat the act (a day's work at a time) until `done()` holds, or it refuses, or `times` runs out."""
            r, good = None, False
            if who:
                w.s["people"][who]["at"] = nid                             # one who knows the craft walks in too
            for _ in range(times):
                r = act(w, who or settler, a)
                if not ok(r):
                    break
                good = True
                if done is None or done():
                    break
            fine = (done() if done else ok(r)) if good else False
            steps.append((label, fine, str(r)[:160]))
            return fine
        knower = lambda tech: next((n for n, a in spec.get("agents", {}).items() if tech in (a.get("knows") or {})
                                    and n in w.s["people"]), settler)
        if site:
            key = next(k for k, p in pars.items() if p["name"] == site)
            step("clear to build", {"do": "work", "what": "clear for building", "at": site}, times=12,
                 done=lambda: w.s["parcels"][key]["cover"] == "built")
        built = name("built") or site
        house = lambda: next((b for b, x in w.s["buildings"].items() if x.get("node") == nid), None)
        first = act(w, settler, {"do": "build", "what": "small room", "at": built, "structure": "wattle"})   # set out, then carry on
        if ok(first) and house():
            step("build a room", {"do": "build", "what": "small room", "at": w.s["buildings"][house()]["name"]}, times=20,
                 done=lambda: not w.s["buildings"][house()].get("unfinished"))
        else:
            steps.append(("build a room", False, str(first)[:160]))
        bld = house()
        bname = w.s["buildings"][bld]["name"] if bld else None
        if bname:
            step("build a hearth", {"do": "build", "what": "hearth", "at": bname}, times=6,
                 done=lambda: bool((w.s["buildings"][bld].get("fittings") or {}).get("hearth")))
        step("found a household", {"do": "found", "name": "Newfold"})
        if bname:
            step("claim the room", {"do": "claim", "thing": bname})
        if open_:
            okey = next(k for k, p in pars.items() if p["name"] == open_)
            step("clear a field", {"do": "work", "what": "clear", "at": open_}, times=200,
                 done=lambda: w.s["parcels"][okey]["cover"] == "field")
            field = next((p["name"] for p in w.s["parcels"].values() if p["node"] == nid and p["cover"] == "field"), None)
            if field:
                step("claim the field", {"do": "claim", "thing": field})
                step("sow it", {"do": "work", "what": "sow", "at": field, "item": "grain", "qty": 2})
        for cover in sorted({p["cover"] for p in pars.values()}):
            for verb, tech in OWN.get(cover, []):
                at = name(cover)
                if tech == "mine":                                         # the rock with the seam
                    at = next((p["name"] for p in pars.values() if p["cover"] == "rock" and "seam" in (p.get("res") or {})), at)
                if tech in ("angle", "fish by hand"):                      # the water with fish in it, if any
                    at = next((p["name"] for p in pars.values() if p["cover"] == "water" and "fish" in (p.get("res") or {})), at)
                k = knower(tech)
                if k != settler:
                    w.s["containers"][w.hands(k)]["goods"]["crude tool"] = 1
                step(f"{tech} ({cover})", {"do": verb, "what": tech, "at": at}, who=k)
        out[node["name"]] = steps
    return out


if __name__ == "__main__":
    res = probe(load_spec(sys.argv[1]))
    bad = 0
    for place, steps in res.items():
        fails = [(l, r) for l, o, r in steps if not o]
        bad += len(fails)
        print(f"{place}: {sum(o for _, o, _ in steps)}/{len(steps)} ok" + ("".join(f"\n    NO {l}: {r}" for l, r in fails)))
    if len(sys.argv) > 2:
        json.dump(res, open(sys.argv[2], "w"), indent=1)
    print("refused or crashed:", bad)
