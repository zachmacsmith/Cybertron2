"""Brief 5 §7's society-level checks on the river world (dry, scripted; no one acts but the works' gaps):
1. Millham's (downstream) weir catch over the autumn's run nights with Saltwell's (upstream) weir shut, against open;
2. a year with Millham's mill dam kept shut, against open: the salmon that pass Saltwell, the spawners that reach the heads above
   Millham, and the next year's return to them (one world year, D2-209).
CYB_ROOT = the branch checkout (default: this repository).

    python3 river_society.py [WORLD.yaml] [DAYS]          default: cybertron2/specs/water/river.yaml, 40 days
"""
import copy
import json
import os
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
import yaml  # noqa: E402

from cybertron2.engine import night as NI, run as R, wild as WL  # noqa: E402
from cybertron2.engine.world import World  # noqa: E402
from cybertron2.wild import runs as RU  # noqa: E402

SPEC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "cybertron2/specs/water/river.yaml")
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 40


def weir(w, node, gap):
    pid = sorted(q for q, p in w.s["parcels"].items() if p["node"] == node and WL._river_parcel(w, q))[0]
    crew = sorted(n for n, p in w.s["people"].items() if p.get("at") == node)[:2]
    bid = w.apply("raise", node, node=node, parcel=pid, rec={"name": f"the weir at {node}", "structure": "timber", "fittings": {},
                                                             "rooms": [], "monument": "weir", "tier": "plain", "unfinished": None,
                                                             "crew": crew, "gap": gap})
    w.s["buildings"][bid]["built_day"] = 0
    return bid


def arm(w0, salt_weir, dam):
    w = copy.deepcopy(w0)
    up = weir(w, "Saltwell", salt_weir)
    down = weir(w, "Millham", "shut")
    WL.mills(w, "Millham")[0][1]["gap"] = dam
    m = WL.model(w)
    nt = RU.net(m)
    above = [h for h in nt.heads("big river") if "v:Millham" in nt.path_up(h)]
    out = {"millham_weir": {}, "saltwell_weir": {}, "salmon_past_saltwell": 0.0, "spawned_above": 0.0, "nights": []}
    for d in range(DAYS):
        w.s["day"], w.s["today"], w.s["events"] = d, R.blank_today(), []
        R.dawn(w)
        st = w.s["wild"]["state"]
        out["salmon_past_saltwell"] += sum(float(p["n"]) for p in RU.today(m, st, WL.eco_day(w)) if p["g"] == "v:Saltwell" and p["k"] == "salmon")
        rec = NI.night(w)
        got = ((rec.get("wild") or {}).get("runs") or {}).get("weir") or {}
        for key, bid in (("millham_weir", down), ("saltwell_weir", up)):
            for k, q in (got.get(bid) or {}).items():
                out[key][k] = out[key].get(k, 0) + q
        for c in w.s["containers"].values():                             # the catch lifted each morning (kept from the robbers)
            if (c.get("set") or {}).get("weir"):
                c["goods"] = {}
                c["catch"] = []
        sp = ((w.s["wild"]["state"]["runs"].get("spawned") or {}).get("salmon") or {})
        out["spawned_above"] = round(sum(float(sp.get(h, 0.0)) for h in above), 2)
        out["nights"].append({"day": d, "season": w.calendar()["season"], "millham": dict(got.get(down) or {})})
        due = (w.s["wild"]["state"]["runs"].get("due") or {}).get("salmon") or {}
        if d > 20 and sum(float(x) for x in due.values()) > 0 and "return_due_above" not in out:              # next year's return, as it is reckoned at its window
            out["return_due_above"] = round(sum(float(due.get(h, 0.0)) for h in above), 2)
            out["return_due_all"] = round(sum(float(x) for x in due.values()), 2)
    out["salmon_past_saltwell"] = round(out["salmon_past_saltwell"], 1)
    return out


def main():
    spec = yaml.safe_load(open(SPEC))
    w0 = World(spec)
    res = {}
    for name, sw, dam in (("saltwell weir shut, dam shut", "shut", "shut"), ("saltwell weir open, dam shut", "open", "shut"),
                          ("saltwell weir open, dam open", "open", "open")):
        r = arm(w0, sw, dam)
        res[name] = {k: v for k, v in r.items() if k != "nights"}
        print(name, json.dumps(res[name]), flush=True)
    json.dump(res, open(os.environ.get("EV_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "river_society.json")), "w"),
              indent=1)


if __name__ == "__main__":
    main()
