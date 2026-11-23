"""Live run 1: food over time, from a run's own checkpoints (stored, by kind), and its days (eaten, spoiled).

    python3 food_ledger.py <code dir> <run dir>
The code dir is the engine the run was made with (its ITEMS give each good's food). Prints one row a day, food in food units.
"""
import json
import sqlite3
import sys
import zlib
from pathlib import Path

code, run = sys.argv[1], Path(sys.argv[2])
sys.path.insert(0, code)
from cybertron2.engine.data import ITEMS  # noqa: E402

KINDS = {"fresh fish": {"fish", "eel", "salmon", "lamprey"},
         "kept fish": {"smoked fish", "salt fish", "dried fish", "hard-cured fish", "hot-smoked fish", "smoking fish", "drying fish"},
         "meat": {"meat", "dried meat", "salt meat", "smoked meat", "hard-cured meat", "hot-smoked meat", "drying meat", "smoking meat"}}


def food(g, q):
    return float(ITEMS.get(g, {}).get("food", 0.0) or 0.0) * float(q or 0.0)


def kind(g):
    for k, s in KINDS.items():
        if g in s:
            return k
    return "other"


db = sqlite3.connect(run / "run.db")
steps = {r[0]: r[1] for r in db.execute("select step, z from checkpoints")}
days = {json.loads(l)["day"]: json.loads(l) for l in open(run / "days.jsonl")}
print("day | stored food: total (fresh fish / kept fish / meat / other) | eaten | spoiled (food) | alive")
for d in sorted(days):
    key = next((k for k in (f"d{d}.evening", f"d{d}.night", f"d{d}.work") if k in steps), None)
    if not key:
        continue
    s = json.loads(zlib.decompress(steps[key]))["world"]
    by = {"fresh fish": 0.0, "kept fish": 0.0, "meat": 0.0, "other": 0.0}
    for c in s.get("containers", {}).values():
        for g, q in (c.get("goods") or {}).items():
            if isinstance(q, (int, float)):
                by[kind(g)] += food(g, q)
    ate = sum((days[d].get("ate") or {}).values())
    sp = sum(food(g, q) for g, q in (days[d].get("spoiled") or {}).items() if isinstance(q, (int, float)))
    alive = sum(1 for p in s.get("people", {}).values() if p.get("alive", True) and not p.get("dead"))
    tot = sum(by.values())
    print(f"{d:3d} | {tot:7.1f} ({by['fresh fish']:6.1f} / {by['kept fish']:6.1f} / {by['meat']:6.1f} / {by['other']:6.1f}) |"
          f" {ate:5.1f} | {sp:5.1f} | {alive}")
