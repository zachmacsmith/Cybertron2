"""World 0b, the same world and model on the broken prompt (w0b_*, the rebuilt prompt with acts hidden) and the fixed one (w0c_*, after
W-109 restored them and D2-304/305 made kills name their beast): behaviour side by side over the days both reached (W-202).

What is read, all from the run's own records (turns.jsonl, days.jsonl, run.db events):
- effort: turns, acts planned a turn, the share of acts refused, the acts most planned;
- family: tries for a child, conceptions, births, partnerings, care given, teaching;
- food: missed meals a person-night, meals eaten, food spoiled; deaths and their causes;
- others: talk, offers, agreements, gifts, travel (departures);
- population by day: the outcome the goal grades.

    python3 docs/review/39_monoculture/w0_compare.py /home/user/mono1 haiku55 sonnet55 haiku45 [--day N]
"""
from __future__ import annotations

import collections
import json
import os
import sqlite3
import sys


def load(run: str, upto: int | None) -> dict:
    turns = [json.loads(x) for x in open(os.path.join(run, "turns.jsonl"))]
    days = [json.loads(x) for x in open(os.path.join(run, "days.jsonl"))]
    if upto is not None:
        turns = [t for t in turns if t["day"] <= upto]
        days = [d for d in days if d["day"] <= upto]
    c = sqlite3.connect(f"file:{os.path.join(run, 'run.db')}?mode=ro", uri=True)
    q = "select day, kind, actor, target, text from events" + (f" where day <= {int(upto)}" if upto is not None else "")
    ev = list(c.execute(q))
    return {"turns": turns, "days": days, "events": ev}


def measure(r: dict) -> dict:
    T, D, E = r["turns"], r["days"], r["events"]
    acts = [p for t in T for p in (t.get("plan") or []) if isinstance(p, dict)]
    results = [x for t in T for x in (t.get("results") or []) if isinstance(x, str)]
    refused = [x for x in results if x.startswith("Refused")]
    verbs = collections.Counter(str(p.get("do")) for p in acts)
    life = collections.Counter()
    for d in D:
        for k, v in (d.get("life") or {}).items():
            life[k] += len(v)
    nights = sum(len(d.get("ate") or {}) for d in D)
    missed = sum(len(d.get("missed") or []) for d in D)
    kinds = collections.Counter(e[1] for e in E)
    refusal_kinds = collections.Counter(x.split(":")[1].strip() if x.count(":") >= 2 else x[:40] for x in refused)
    first = (set(D[0].get("ate") or {}) | set(D[0].get("slept") or {})) if D else set()
    return {
        "days": D[-1]["day"] if D else None,
        "turns": len(T),
        "acts/turn": round(len(acts) / max(1, len(T)), 2),
        "refused %": round(100 * len(refused) / max(1, len(results)), 1),
        "refused by": refusal_kinds.most_common(6),
        "top acts": verbs.most_common(12),
        "tries": verbs.get("try", 0) + verbs.get("try for a child", 0),
        "conceived": life["conceived"], "births": life["births"], "deaths": sum(len(d.get("deaths") or []) for d in D),
        "missed meals / person-night": round(missed / max(1, nights), 2),
        "care given (fed)": sum(len((d.get("care") or {}).get("fed") or {}) for d in D),
        "taught": sum(len(d.get("teaching") or []) for d in D), "learned": sum(len(d.get("learning") or []) for d in D),
        "talked (person-days)": sum(len(d.get("talked") or []) for d in D),
        "offers": len({o for d in D for o in (d.get("offers") or {})}),
        "agreements": sum(len(d.get("agreements_made") or []) for d in D),
        "joins/admits": sum(len(d.get("joins") or []) + len(d.get("admits") or []) for d in D),
        "departures": kinds.get("depart", 0), "gifts": kinds.get("give", 0), "trades": kinds.get("trade", 0),
        "kills": verbs.get("slaughter", 0),
        "book rules fired": sum(len((d.get("book") or {}).get("fired") or []) for d in D),
        "alive by day": [len(set(d.get("ate") or {}) | set(d.get("slept") or {})) for d in D],
        "people at start": len(first),
    }


def main(argv):
    root = argv[0]
    arms = [a for a in argv[1:] if not a.startswith("--") and not a.isdigit()]
    upto = int(argv[argv.index("--day") + 1]) if "--day" in argv else None
    out = {}
    for a in arms:
        b, c = os.path.join(root, f"w0b_{a}"), os.path.join(root, f"w0c_{a}")
        rb, rc = load(b, None), load(c, None)
        n = min(rb["days"][-1]["day"], rc["days"][-1]["day"]) if upto is None else upto    # the days both reached
        out[a] = {"to day": n, "broken (w0b)": measure(load(b, n)), "fixed (w0c)": measure(load(c, n))}
    keys = [k for k in next(iter(out.values()))["broken (w0b)"] if k not in ("top acts", "refused by", "alive by day")]
    for a, v in out.items():
        print(f"\n== {a}, days 0 to {v['to day']}")
        print(f"{'':32}{'broken':>14}{'fixed':>14}")
        for k in keys:
            print(f"{k:32}{str(v['broken (w0b)'][k]):>14}{str(v['fixed (w0c)'][k]):>14}")
        for side in ("broken (w0b)", "fixed (w0c)"):
            m = v[side]
            print(f"  {side} top acts: {m['top acts']}")
            print(f"  {side} refused by: {m['refused by']}")
            print(f"  {side} alive by day: {m['alive by day']}")
    json.dump(out, open(os.path.join(root, "w0_compare.json"), "w"), indent=1, default=str)


if __name__ == "__main__":
    main(sys.argv[1:])
