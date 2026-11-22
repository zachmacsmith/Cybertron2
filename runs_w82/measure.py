"""W-82: read a bot run's building and food from its files (state.json, days.jsonl, turns.jsonl). Bots only.

    python3 runs_w82/measure.py RUN_DIR [RUN_DIR ...]      -> one JSON line a run (and runs_w82/<run>/measure.json)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cybertron2.engine.data import ITEMS, TECHNIQUES  # noqa: E402

BUILD_WORK = {"fence", "wall", "clear", "clear for building", "ditch", "terrace"}
FOOD_TAGS = {"food", "farming", "animals", "hunting", "fishing", "harvest"}


def units_of(a):
    d = str(a.get("do", ""))
    if d == "build":
        return 2
    if d in ("gather", "work", "make"):
        t = TECHNIQUES.get(str(a.get("what", "")))
        if t is None:
            return 1
        n = int(t.get("units", 1) or 0)
        if d == "make":
            n *= max(1, int(a.get("qty") or 1))
        return n
    if d == "set":
        return 1
    if d == "take":
        return 1
    return 0


def kind_of(a):
    d, w = str(a.get("do", "")), str(a.get("what", ""))
    if d == "build":
        return "build"
    if d == "work" and w in BUILD_WORK:
        return "build"
    if d == "work" and w == "repair":
        return "upkeep"
    if w == "fell":
        return "timber"
    if w in ("firewood", "cut"):
        return "fuel"
    t = TECHNIQUES.get(w) or {}
    if set(t.get("tags") or []) & FOOD_TAGS or d == "set" or d == "take":
        return "food"
    if d in ("gather", "work", "make"):
        return "other"
    return None


def measure(run):
    s = json.load(open(os.path.join(run, "state.json")))
    days = [json.loads(l) for l in open(os.path.join(run, "days.jsonl"))]
    turns = [json.loads(l) for l in open(os.path.join(run, "turns.jsonl"))]
    rj = json.load(open(os.path.join(run, "run.json"))) if os.path.exists(os.path.join(run, "run.json")) else {}
    units = {"build": 0, "timber": 0, "food": 0, "fuel": 0, "upkeep": 0, "other": 0}
    by_what = {}
    started, finished = {}, {}
    refused = 0
    for x in (json.loads(l) for l in open(os.path.join(run, "actlog.jsonl"))):
        a, r = x, x["res"]
        k = kind_of(a)
        if k:
            u = int(x["units"])
            units[k] += u
            if k == "build":
                key = f"{a.get('do')} {a.get('what')}"
                by_what[key] = by_what.get(key, 0) + u
        if a.get("do") not in ("build", "work"):
            continue
        m = re.match(r"You began (.+?):", str(r))
        if m:
            started.setdefault(m.group(1), x["day"] + 1)
        m = re.match(r"You (?:finished|made) ([^:.]+)", str(r))
        if m and not str(r).startswith("You finished clearing"):
            finished.setdefault(m.group(1), x["day"] + 1)
        m = re.match(r"You put (.+?) into (.+?)\.", str(r))
        if m:
            finished.setdefault(f"{m.group(1)} in {m.group(2)}", x["day"] + 1)
        m = re.match(r"You finished clearing (.+?)[:,]", str(r))
        if m:
            finished.setdefault(f"field cleared: {m.group(1)}", x["day"] + 1)
        m = re.match(r"You worked on an? (?:fence|wall|wattle fence) round (.+?): about (\d+) parts", str(r))
        if m:
            started.setdefault(f"fence round {m.group(1)}", x["day"] + 1)
    for x in turns:
        refused += sum(1 for r in x.get("results") or [] if str(r).startswith("Refused"))
    # fences finished (the night settles them: days.jsonl farm.herds ["fence", pid, kind])
    for d in days:
        for e in ((d.get("farm") or {}).get("herds") or []):
            if isinstance(e, list) and e and e[0] == "fence":
                finished.setdefault(f"fence round {s['parcels'][e[1]]['name']}", d["day"] + 1)
    for pid, p in s["parcels"].items():
        fc = p.get("fence") or {}
        if fc.get("built"):
            finished.setdefault(f"fence round {p['name']}", None)
    unfinished = {}
    for bid, b in s["buildings"].items():
        if b.get("unfinished"):
            unfinished[b["name"]] = b["unfinished"]["units_left"]
        for f, u in (b.get("fitting_work") or {}).items():
            unfinished[f"{f} in {b['name']}"] = u["units_left"]
        if b.get("works"):
            unfinished[f"{b['works'].get('kind')} at {b['name']}"] = b["works"].get("units_left")
    for pid, p in s["parcels"].items():
        fc = p.get("fence") or {}
        if fc and not fc.get("built"):
            unfinished[f"fence round {p['name']}"] = round(float(fc.get("units", 0)), 1)
        if p.get("clearing"):
            unfinished[f"clearing {p['name']}"] = p["clearing"]
    people = s["people"]
    alive = [n for n, p in people.items() if p["alive"]]
    deaths = {}
    for n, p in people.items():
        if not p["alive"]:
            c = p.get("cause") or "?"
            deaths[c] = deaths.get(c, 0) + 1
    # households and whether housed (a finished non-camp building of theirs with beds)
    hh = {}
    for iid, h in s["institutions"].items():
        if h.get("kind") != "household":
            continue
        mem = [m for m in h["members"] if people.get(m, {}).get("alive")]
        if not mem:
            hh[iid] = "gone"
            continue
        held = [bid for bid, b in s["buildings"].items() if not b.get("unfinished") and b["structure"] != "camp"
                and (b.get("fittings") or {}).get("beds") and any(c["claimant"] in [iid] + mem for c in s["claims"].values()
                                                                  if c["thing"] == ["building", bid])]
        hh[iid] = "housed" if held else "unhoused"
    food_end = 0.0
    for bid, b in s["buildings"].items():
        g = s["containers"][b["stock"]]["goods"]
        food_end += sum(float(q) * ITEMS[i]["food"] for i, q in g.items() if i in ITEMS)
    for n in alive:
        g = s["containers"][people[n]["hands"]]["goods"]
        food_end += sum(float(q) * ITEMS[i]["food"] for i, q in g.items() if i in ITEMS)
    missed = sum(len(d.get("missed") or []) for d in days)
    first_missed = next((d["day"] + 1 for d in days if d.get("missed")), None)
    fields = sum(1 for p in s["parcels"].values() if p["cover"] == "field")
    out = {"run": os.path.basename(run.rstrip("/")), "days": len(days), "alive": len(alive), "people": len(people),
           "deaths": deaths, "households": hh, "food_end": round(food_end, 1), "missed_meals": missed, "first_missed": first_missed,
           "units": units, "build_units_by": by_what, "started": started, "finished": finished, "unfinished": unfinished,
           "fields": fields, "refused": refused}
    json.dump(out, open(os.path.join(run, "measure.json"), "w"), indent=1)
    return out


if __name__ == "__main__":
    for r in sys.argv[1:]:
        print(json.dumps(measure(r)))
