"""Past runs against their land's capacity (D4-102): what each run's world could feed, set beside what happened in it.

For each run: the world it started from (the journal's spec, or a pre-journal run's run.json), analysed at day 0; and its outcome
from its final state (the last checkpoint, or state.json): the people at the start, births, deaths by cause, the people at the end,
the days run. Worlds today's engine cannot build are listed with the reason.

    python -m cybertron2.capacity.retro RUNS_DIR ... --out FILE.json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sqlite3
import zlib
from concurrent.futures import ProcessPoolExecutor


def _final_state(d):
    db = os.path.join(d, "run.db")
    if os.path.exists(db):
        c = sqlite3.connect(db)
        row = c.execute("SELECT z FROM checkpoints ORDER BY rowid DESC LIMIT 1").fetchone()
        spec = json.loads(c.execute("SELECT value FROM meta WHERE key = 'spec'").fetchone()[0])
        st = json.loads(zlib.decompress(row[0]))["world"] if row else None
        return spec, st
    rj = os.path.join(d, "run.json")
    if not os.path.exists(rj):
        return None, None
    spec = json.load(open(rj)).get("spec")
    sp = os.path.join(d, "state.json")
    st = json.load(open(sp)) if os.path.exists(sp) else None
    if st and "world" in st:
        st = st["world"]
    return spec, st


def outcome_from_days(spec, d) -> dict:
    """For a run with no final state: deaths and births from days.jsonl; a death is old age if the day says so, hunger if the person
    missed a meal in the three days before, cold if a cold fall, else unknown."""
    start = set((spec.get("agents") or {}).keys())
    p = os.path.join(d, "days.jsonl")
    if not os.path.exists(p):
        return {"start": len(start)}
    L = [json.loads(x) for x in open(p)]
    causes, born, dead = {}, 0, set()
    for i, day in enumerate(L):
        life = day.get("life") or {}
        born += len(life.get("births") or [])
        for n in day.get("deaths") or []:
            n = n if isinstance(n, str) else (n.get("name") if isinstance(n, dict) else str(n))
            dead.add(n)
            missed = set()
            for back in L[max(0, i - 3):i + 1]:
                missed |= set(back.get("missed") or []) | set(back.get("short") or [])
            key = "old age" if n in (life.get("old_age") or []) else "hunger" if n in missed else \
                "cold" if n in (day.get("cold_falls") or []) else "unknown"
            causes[key] = causes.get(key, 0) + 1
    return {"start": len(start), "births": born, "deaths": causes, "dead": sum(causes.values()),
            "end": len(start) + born - len(dead), "days": int(L[-1].get("day", len(L) - 1)) + 1 if L else 0, "from": "days.jsonl"}


def outcome(spec, st) -> dict:
    start = set((spec.get("agents") or {}).keys())
    if not st:
        return {"start": len(start)}
    ppl = st.get("people") or {}
    causes = {}
    for n, a in ppl.items():
        if not a.get("alive", True):
            c = str(a.get("cause") or "unknown")
            key = "hunger" if "hunger" in c or "starv" in c else "cold" if "cold" in c else "illness" if "ill" in c else \
                "old age" if "old" in c or "age" in c else "killed" if any(k in c for k in ("kill", "wound", "fight", "attack")) else c
            causes[key] = causes.get(key, 0) + 1
    born = [n for n in ppl if n not in start]
    return {"start": len(start), "births": len(born), "deaths": causes, "dead": sum(causes.values()),
            "end": sum(1 for a in ppl.values() if a.get("alive", True)), "days": int(st.get("day", 0))}


def one(d) -> dict:
    name = os.path.basename(os.path.normpath(d))
    try:
        spec, st = _final_state(d)
        if not spec:
            return {"run": name, "error": "no spec"}
        out = {"run": name, "outcome": outcome(spec, st) if st else outcome_from_days(spec, d), "days_planned": spec.get("days")}
        from cybertron2.capacity import model as M
        w = M.world_of(spec)
        days = int(spec.get("days") or 0) or 30
        rep = M.analyse(w, horizon=days)
        reg = rep["nodes"]["(region)"]
        out["capacity"] = {l: {"supported": v["supported"], "ratio": v["ratio"], "labour_share": v["labour_share"]}
                           for l, v in reg["levels"].items()}
        out["fuel"] = {l: v["ratio"] for l, v in reg["fuel"]["levels"].items()}
        out["fuel_standing_years"] = reg["fuel"]["standing_years"]
        out["buffer_days"] = reg["buffer_days"]
        out["first_harvest"] = reg["first_harvest"]["first"]
        out["lost_to_frost"] = len(reg["first_harvest"]["lost_to_frost"])
        out["horizon"] = {l: {k: v[k] for k in ("first_short", "short_days", "seed_share")} for l, v in (reg.get("horizon") or {}).items()}
        worst = [(k, v["levels"]["standing"]["ratio"]) for k, v in rep["nodes"].items() if k != "(region)" and v["people"]]
        out["worst_node_standing"] = min(worst, key=lambda x: x[1]) if worst else None
        out["year"] = rep["year"]
        return out
    except Exception as e:                                                   # an old world today's engine cannot build
        return {"run": name, "error": f"{type(e).__name__}: {str(e)[:120]}"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--out", default="retro.json")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args(argv)
    runs = []
    for d in a.dirs:
        runs += sorted(x for x in glob.glob(os.path.join(d, "*/")) if os.path.exists(os.path.join(x, "run.db")) or
                       os.path.exists(os.path.join(x, "run.json")))
    with ProcessPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, runs))
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, default=str)
    ok = [r for r in res if "error" not in r]
    print(f"{len(ok)} of {len(res)} runs analysed; {a.out}")


if __name__ == "__main__":
    main()
