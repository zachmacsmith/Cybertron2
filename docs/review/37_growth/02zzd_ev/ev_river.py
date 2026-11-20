"""Food a unit on the river's nights (build brief 5 §7, "Food a unit"; proposals/river_and_water.md): wicker traps, a net and fishing
by hand at a village's water, a sound shut weir, and a trap in a shut mill's race, on each night of a run through the autumn, against
the nights with no run. Beside ev_region.py (brief 4c's hunting harness); CYB_ROOT = the branch checkout (default: this repository).

    python3 ev_river.py [WORLD.yaml] [DAYS] [TRIES] [noclimate]   default: cybertron2/specs/water/river.yaml, 14 days, 12 tries a cell

The world is stepped night by night as it is (no one acting), each morning kept; each cell is tried on a copy of that morning:
- `trap`: wicker traps set at the village's river water (1 unit), what is in them after the night;
- `net`: a net at the water (2 units), what is taken;
- `hand`: fishing by hand (1 unit), from the run only (the resident fish left out);
- `weir`, `weir full`: a sound weir of one section, and of four (D2-210), at the water with its gap shut, its traps after the night: a unit a night if it is kept shut through the
  season and lifted each morning ("lift only"), three if it is shut for that night alone (2 units) and lifted (1);
- `race`: a trap set in the race of a shut water mill (1 unit; Millham only), what is in it after the night.
Each row: day, village, the run there that day (heads by kind and direction), cell, tries, food a unit (mean), food a try. The skill is
the method's known level, familiarity 0.6. Written to EV_OUT (default ev_river.json beside this)."""
import copy
import json
import os
import statistics
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
import yaml  # noqa: E402

from cybertron2.engine import night as NI, run as R, verbs as V, wild as WL  # noqa: E402
from cybertron2.engine.data import ITEMS  # noqa: E402
from cybertron2.engine.here import Here, Mind  # noqa: E402
from cybertron2.engine.world import Refused, World  # noqa: E402
from cybertron2.wild import runs as RU  # noqa: E402

SPEC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "cybertron2/specs/water/river.yaml")
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 14
TRIES = int(sys.argv[3]) if len(sys.argv) > 3 else 12
VILLAGES = ("Saltwell", "Millham")


def food(goods):
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0)) for i, q in (goods or {}).items())


def morning(w, d):
    w.s["day"] = d
    w.s["today"] = R.blank_today()
    w.s["events"] = []
    R.dawn(w)


def who(w, node):
    """The village's adults (anyone alive there, if the stepped world has lost them: nobody acts in it, so some go hungry)."""
    out = sorted(n for n, p in w.s["people"].items() if p.get("at") == node and p.get("stage") == "adult" and p.get("alive", True))
    return out or sorted(n for n, p in w.s["people"].items() if p.get("home") == node or p.get("at") == node)


def water(w, node):
    return sorted(pid for pid, p in w.s["parcels"].items() if p["node"] == node and WL._river_parcel(w, pid))[0]


def salted(w, salt):
    orig = w.rng
    w.rng = lambda *k: orig(*k, "ev", salt)
    return w


def setup(w, p, tech):
    w.s["know"].setdefault(p, {})[tech] = {"level": "known", "skill": 1.0}
    Mind(w, p).store["familiar"] = {k: 0.6 for k in ("eel", "salmon", "lamprey", "wildfowl")}


def try_set(w0, node, salt, mill=False):
    w = salted(copy.deepcopy(w0), salt)
    p = who(w, node)[0]
    setup(w, p, "trap in water")
    at = WL.mill_water(w, next(b for _, b in WL.mills(w, node))) if mill else water(w, node)
    if mill:
        for bid, b in WL.mills(w, node):
            b["gap"] = "shut"
    V.do(Here(w, p), Mind(w, p), {"do": "gather", "what": "trap in water", "at": w.s["parcels"][at]["name"]})
    NI.night(w)
    return sum(food(c["goods"]) for c in w.s["containers"].values() if c.get("kind") == "set" and c.get("by") == p
               and not (c.get("set") or {}).get("weir")) / 1.0


def try_hunt(w0, node, salt, tech, units):
    w = salted(copy.deepcopy(w0), salt)
    p = who(w, node)[0]
    setup(w, p, tech)
    h = Here(w, p)
    before = food(w.s["containers"][h.hands]["goods"])
    fish0 = float(w.s["containers"][h.hands]["goods"].get("fish", 0.0))
    try:
        V.do(h, Mind(w, p), {"do": "gather", "what": tech, "at": w.s["parcels"][water(w, node)]["name"]})
    except Refused:
        return None
    g = w.s["containers"][Here(w, p).hands]["goods"]
    got = food(g) - before - (float(g.get("fish", 0.0)) - fish0 if tech == "fish by hand" else 0.0)   # the run only
    return got / units


def try_weir(w0, node, salt, full=False):
    w = salted(copy.deepcopy(w0), salt)
    crew = who(w, node)[:2]
    pid = water(w, node)
    bid = w.apply("raise", node, node=node, parcel=pid, rec={"name": f"the weir at {node}", "structure": "timber", "fittings": {},
                                                             "rooms": [], "monument": "weir", "tier": "plain", "unfinished": None,
                                                             "crew": crew, "gap": "shut"})
    w.s["buildings"][bid]["built_day"] = w.d
    if full:                                                                 # a full weir (D2-210): the first section and three timber
        w.s["buildings"][bid]["sections"] = [{"m": "wattle", "foot": False, "level": 5}] + \
            [{"m": "timber", "foot": False, "level": 5} for _ in range(3)]
    NI.night(w)
    cid = WL.weir_trap(w, bid)
    return food(w.s["containers"][cid]["goods"])                             # a night's catch: a unit to lift, 2 to shut


def main():
    spec = yaml.safe_load(open(SPEC))
    if "noclimate" in sys.argv[4:]:                                          # the runs on the window's set nights (RUN.no_weather)
        spec.pop("climate", None)
    w = World(spec)
    m = WL.model(w)
    out = []
    for d in range(DAYS):
        morning(w, d)
        st = w.s["wild"]["state"]
        cal = w.calendar()
        for node in VILLAGES:
            g = f"v:{node}"
            run = {}
            for p in RU.today(m, st, WL.eco_day(w)):
                if p["g"] == g:
                    key = f"{p['k']} {'held' if p.get('held') else p['dir']}"
                    run[key] = round(run.get(key, 0.0) + float(p["n"]), 1)
            cells = {"trap": lambda s: try_set(w, node, s), "net": lambda s: try_hunt(w, node, s, "net", 2.0),
                     "hand": lambda s: try_hunt(w, node, s, "fish by hand", 1.0), "weir": lambda s: try_weir(w, node, s),
                     "weir full": lambda s: try_weir(w, node, s, True)}
            if WL.mills(w, node):
                cells["race"] = lambda s: try_set(w, node, s, mill=True)
            for cell, f in cells.items():
                n = 1 if cell.startswith("weir") else TRIES
                got = [x for x in (f(f"{d}{node}{cell}{i}") for i in range(n)) if x is not None]
                if not got:
                    continue
                fu = statistics.mean(got)
                if cell.startswith("weir"):                                # a run night counts 3 units (D2-219); and kept shut, 1
                    out.append((d, f"{cal['season']} {cal['day']}", node, run, f"{cell} (3 units: D2-219)", 1, round(fu / 3.0, 3)))
                    print(*out[-1], flush=True)
                    cell, fu = f"{cell} (lift only)", fu / 1.0
                out.append((d, f"{cal['season']} {cal['day']}", node, run, cell, len(got), round(fu, 3)))
                print(*out[-1], flush=True)
        NI.night(w)
    json.dump(out, open(os.environ.get("EV_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ev_river.json")), "w"))


if __name__ == "__main__":
    main()
