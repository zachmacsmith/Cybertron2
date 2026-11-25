"""World 0b: the models against each other and the prompts against each other, on equal windows (W-202).

Runs: w0b_<model> (the broken prompt, acts hidden) and w0c_<model> (the fixed one, W-109 and D2-304/305). Every rate is per
person-day or per adult-day so runs of different sizes compare; every window is one every run in the row reached.

    python3 docs/review/39_monoculture/w0_matrix.py /home/user/mono1 --upto 5 15 25
"""
from __future__ import annotations

import collections
import json
import os
import re
import sqlite3
import sys

MODELS = ["sonnet55", "haiku55", "haiku45"]
NAME = {"sonnet55": "Sonnet 5.5", "haiku55": "Haiku 5.5", "haiku45": "Haiku 4.5"}
VILLAGE = {"Brook": "Highpool", "Marsh": "Highpool", "Field": "Middleham", "Fletcher": "Middleham"}
SOCIAL = {"teach", "learn", "agree", "give", "accept", "meet"}
TRAVEL = {"move", "go"}


def runs(root):
    out = {}
    for m in MODELS:
        for p, tag in (("broken", "w0b"), ("fixed", "w0c")):
            d = os.path.join(root, f"{tag}_{m}")
            if os.path.exists(os.path.join(d, "days.jsonl")):
                out[(m, p)] = d
    return out


def reached(d):
    return sum(1 for _ in open(os.path.join(d, "days.jsonl"))) - 1


def measure(d, upto):
    T = [t for t in map(json.loads, open(os.path.join(d, "turns.jsonl"))) if t["day"] <= upto]
    D = [x for x in map(json.loads, open(os.path.join(d, "days.jsonl"))) if x["day"] <= upto]
    c = sqlite3.connect(f"file:{os.path.join(d, 'run.db')}?mode=ro", uri=True)
    ev = collections.Counter(k for (k,) in c.execute(f"select kind from events where day <= {int(upto)}"))
    alive = [len(set(x.get("ate") or {}) | set(x.get("slept") or {})) for x in D]
    pdays = sum(alive)
    adult_turns = len(T)                                                # a turn is a person who acts (youth and up) on a day
    acts = [p for t in T for p in (t.get("plan") or []) if isinstance(p, dict)]
    res = [r for t in T for r in (t.get("results") or []) if isinstance(r, str)]
    verbs = collections.Counter(str(p.get("do")) for p in acts)
    life = collections.Counter()
    for x in D:
        for k, v in (x.get("life") or {}).items():
            life[k] += len(v)
    deaths = sum(len(x.get("deaths") or []) for x in D)
    offers = set()
    for t in T:
        for src in [t.get("reply")] + [x.get("reply") for x in (t.get("talk") or []) if isinstance(x, dict)]:
            if isinstance(src, dict) and src.get("offers"):
                offers.add((t["day"], t["agent"], json.dumps(src["offers"], sort_keys=True)))
    why = [str((t.get("reply") or {}).get("why") or "") for t in T]
    talk_words = [str((x.get("reply") or {}).get("say") or "") for t in T for x in (t.get("talk") or [])
                  if isinstance(x, dict) and isinstance(x.get("reply"), dict)]
    said = [s for s in talk_words if s.strip()]
    winter = sum(1 for w in why if re.search(r"\bwinter|\bfrost|\bcold\b|lay in|store (up|for)|smok|salt(ed|ing)? (fish|meat)", w, re.I))
    return {
        "days": f"0-{upto}",
        "alive at end": alive[-1] if alive else None,
        "births": life["births"], "deaths": deaths,
        "tries / 10 adult-days": round(10 * (verbs.get("try", 0) + verbs.get("try for a child", 0)) / max(1, adult_turns), 2),
        "conceptions": life["conceived"],
        "acts a turn": round(len(acts) / max(1, adult_turns), 2),
        "refused %": round(100 * sum(1 for r in res if r.startswith("Refused")) / max(1, len(res)), 1),
        "missed meals / person-night": round(sum(len(x.get("missed") or []) for x in D) / max(1, pdays), 3),
        "care acts / 10 adult-days": round(10 * verbs.get("care", 0) / max(1, adult_turns), 1),
        "spoken lines / adult-day": round(len(said) / max(1, adult_turns), 2),
        "offers made": len(offers), "agreements": sum(len(x.get("agreements_made") or []) for x in D),
        "lessons (taught)": sum(len(x.get("teaching") or []) for x in D),
        "gifts": ev.get("give", 0), "departures": ev.get("depart", 0),
        "reasoning on winter %": round(100 * winter / max(1, len(why)), 1),
        "cost $": round(sum(float(x.get("cost_usd") or 0) for x in D[-1:]), 2),
    }


def main(argv):
    root = argv[0]
    ups = [int(x) for x in argv[argv.index("--upto") + 1:]] if "--upto" in argv else [5, 15, 25]
    R = runs(root)
    out = {}
    for u in ups:
        cols = [(m, p) for (m, p), d in sorted(R.items(), key=lambda kv: (MODELS.index(kv[0][0]), kv[0][1])) if reached(d) >= u]
        if not cols:
            continue
        rows = {f"{NAME[m]} {p}": measure(R[(m, p)], u) for m, p in cols}
        out[u] = rows
        keys = list(next(iter(rows.values())))
        print(f"\n== days 0 to {u} ({len(cols)} runs reached it)")
        print(f"{'':30}" + "".join(f"{k:>20}" for k in rows))
        for k in keys[1:]:
            print(f"{k:30}" + "".join(f"{str(v[k]):>20}" for v in rows.values()))
    json.dump(out, open(os.path.join(root, "w0_matrix.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
