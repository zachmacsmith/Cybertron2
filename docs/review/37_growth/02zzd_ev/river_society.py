"""Brief 5 §7's society-level checks and §3b's yearly targets on the river world (dry, scripted; no one acts but the works):
1. a year's take of a weir at each village, one section against a full weir (four sections; D2-210: about 60 to 70 food and 180
   to 200), with the run nights it saw, and its wear in the year (the levels each section lost, and what mending them would cost as a
   share of the weir's build);
2. Millham's (downstream) weir catch with Saltwell's (upstream) weir shut, against open;
3. Millham's mill dam kept shut against open: the salmon that pass Saltwell, and next year's return to the heads above Millham.
Each weir's traps are lifted each morning (the catch counted, then taken away), the gap kept shut all year, nothing mended.
CYB_ROOT = the branch checkout (default: this repository).

    python3 river_society.py [WORLD.yaml] [DAYS] [noclimate]      default: cybertron2/specs/water/river.yaml, 40 days

`noclimate` drops the world's climate, so the runs come on the window's set nights (RUN.no_weather): a sensitivity check of the yearly
take when the rain gives few cue nights.
"""
import copy
import json
import os
import sys

ROOT = os.environ.get("CYB_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
import yaml  # noqa: E402

from cybertron2.engine import night as NI, run as R, wild as WL  # noqa: E402
from cybertron2.engine.data import ITEMS, MONUMENTS, WATER_WORKS  # noqa: E402
from cybertron2.engine.world import World  # noqa: E402
from cybertron2.wild import runs as RU  # noqa: E402

SPEC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "cybertron2/specs/water/river.yaml")
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 40
NOCLIMATE = "noclimate" in sys.argv[3:]


def weir(w, node, gap, full):
    pid = sorted(q for q, p in w.s["parcels"].items() if p["node"] == node and WL._river_parcel(w, q))[0]
    crew = sorted(n for n, p in w.s["people"].items() if p.get("at") == node)[:2]
    bid = w.apply("raise", node, node=node, parcel=pid, rec={"name": f"the weir at {node}", "structure": "timber", "fittings": {},
                                                             "rooms": [], "monument": "weir", "tier": "plain", "unfinished": None,
                                                             "crew": crew, "gap": gap})
    w.s["buildings"][bid]["built_day"] = 0
    secs = [{"m": "wattle", "foot": False, "level": 5}]
    if full:
        secs += [{"m": "timber", "foot": False, "level": 5} for _ in range(int(WATER_WORKS["weir"]["sections"]["timber"]["most"]))]
    w.s["buildings"][bid]["sections"] = secs
    return bid


def food(goods):
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0)) for i, q in (goods or {}).items())


def build_cost(secs):
    """A weir's build, in units of work and timber (the first section's and each further one's)."""
    W = WATER_WORKS["weir"]["sections"]
    units = sum(float(MONUMENTS["weir"]["units"] if s["m"] == "wattle" else W["timber"]["units"]) for s in secs)
    return units


def arm(w0, salt_weir, dam, full, days=DAYS):
    w = copy.deepcopy(w0)
    ws = {"Saltwell": weir(w, "Saltwell", salt_weir, full), "Millham": weir(w, "Millham", "shut", full)}
    WL.mills(w, "Millham")[0][1]["gap"] = dam
    m = WL.model(w)
    nt = RU.net(m)
    above = [h for h in nt.heads("big river") if "v:Millham" in nt.path_up(h)]
    out = {v: {"food": 0.0, "heads": {}, "run_nights": 0, "lost": [0] * len(w.s["buildings"][b]["sections"]), "flows": {}}
           for v, b in ws.items()}
    out["salmon_past_saltwell"] = 0.0
    for d in range(days):
        w.s["day"], w.s["today"], w.s["events"] = d, R.blank_today(), []
        R.dawn(w)
        st = w.s["wild"]["state"]
        out["salmon_past_saltwell"] += sum(float(p["n"]) for p in RU.today(m, st, WL.eco_day(w)) if p["g"] == "v:Saltwell" and p["k"] == "salmon")
        for v in ws:
            if d < w.year_days() and any(p["g"] == f"v:{v}" and float(p["n"]) >= 3 for p in RU.today(m, st, WL.eco_day(w))):
                out[v]["run_nights"] += 1
        rec = NI.night(w)
        runs = (rec.get("wild") or {}).get("runs") or {}
        year = d < w.year_days()                                         # the year's take: the first world year only
        for v, bid in ws.items():
            if not year:
                continue
            for k, q in ((runs.get("weir") or {}).get(bid) or {}).items():
                out[v]["heads"][k] = out[v]["heads"].get(k, 0) + q
            for j, n in enumerate(((runs.get("wear") or {}).get(bid) or {}).get("lost") or []):
                out[v]["lost"][j] += n
            fl = (runs.get("flow") or {}).get(v)
            if fl:
                out[v]["flows"][fl] = out[v]["flows"].get(fl, 0) + 1
        for v, bid in ws.items():
            cid = WL.weir_trap(w, bid)
            if cid and year:                                             # lifted each morning
                c = w.s["containers"][cid]
                out[v]["food"] += food(c["goods"])
                c["goods"], c["catch"] = {}, []
            elif cid:
                w.s["containers"][cid]["goods"], w.s["containers"][cid]["catch"] = {}, []
            b = w.s["buildings"][bid]                                    # kept standing for the year's count: the levels lost are
            b["sections"] = [dict(s, level=5) for s in b["sections"]]    # counted, the weir put back sound each night
        due = (w.s["wild"]["state"]["runs"].get("due") or {}).get("salmon") or {}
        if d > 20 and sum(float(x) for x in due.values()) > 0 and "return_due_above" not in out:   # next year's return
            out["return_due_above"] = round(sum(float(due.get(h, 0.0)) for h in above), 2)
    W = WATER_WORKS["weir"]
    for v, bid in ws.items():
        secs = w.s["buildings"][bid]["sections"]
        o = out[v]
        o["food"] = round(o["food"], 1)
        cost = build_cost(secs)
        mend = sum(n * float(W["mend"]) * float(MONUMENTS["weir"]["units"] if s["m"] == "wattle" else W["sections"]["timber"]["units"])
                   for n, s in zip(o["lost"], secs))
        o["upkeep_share"] = round(mend / cost, 3)                              # a year's mending (by its work) over the build's work
        o["water"] = WL.water_kind(w, m, w.s["buildings"][bid]["parcel"])
    out["salmon_past_saltwell"] = round(out["salmon_past_saltwell"], 1)
    return out


def main():
    spec = yaml.safe_load(open(SPEC))
    if NOCLIMATE:
        spec.pop("climate", None)
    w0 = World(spec)
    res = {}
    for name, sw, dam, full in (("one section each, both shut, dam shut", "shut", "shut", False),
                                ("full weirs, both shut, dam shut", "shut", "shut", True),
                                ("one section, Saltwell's open, dam shut", "open", "shut", False),
                                ("one section, Saltwell's open, dam open", "open", "open", False)):
        res[name] = arm(w0, sw, dam, full)
        print(name, json.dumps(res[name]), flush=True)
    json.dump(res, open(os.environ.get("EV_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "river_society.json")), "w"),
              indent=1)


if __name__ == "__main__":
    main()
