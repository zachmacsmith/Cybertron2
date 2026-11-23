"""Live run 1: a quick side-by-side of arms, to a common day (D2-335: qualitative, not significance).

    python3 compare.py <run dir> [<run dir> ...] [--to DAY]
"""
import collections
import json
import re
import sys
from pathlib import Path

FISH = re.compile(r"(\d+(?:\.\d+)?) (?:kg of )?(?:fish|eels?|salmon|lamprey)", re.I)


def arm(path, to):
    turns = [json.loads(l) for l in open(Path(path) / "turns.jsonl")]
    turns = [t for t in turns if t["day"] <= to]
    days = [json.loads(l) for l in open(Path(path) / "days.jsonl")]
    days = [d for d in days if d["day"] <= to]
    acts = collections.Counter()
    refused = collections.Counter()
    fallback = total = 0
    fish_got = 0.0
    rules = rested = 0
    sets = tends = 0
    lessons_ok = lessons_refused = 0
    for t in turns:
        for a in t.get("plan") or []:
            d = str(a.get("do", "?")).split()[0]
            acts[d] += 1
            if d == "rule":
                rules += 1
        for r in t.get("results") or []:
            total += 1
            if "(your fallback)" in r or "(the household's chore" in r:
                fallback += 1
            if r.startswith("Refused"):
                refused[r.split(":")[1].strip() if ":" in r else r[:30]] += 1
                if "learn" in r or "teach" in r:
                    lessons_refused += 1
            if re.search(r"\b(taught|learnt|learned)\b", r):
                lessons_ok += 1
            if re.search(r"^You (set|laid) ", r):
                sets += 1
            if re.search(r"^You (tended|lifted|emptied|checked)", r):
                tends += 1
            if re.search(r"^You (lifted|tended|emptied|took|caught|fished|netted|gathered)", r):
                for m in FISH.finditer(r):
                    fish_got += float(m.group(1))
            if "rested" in r:
                rested += 1
    deaths = [x for d in days for x in (d.get("deaths") or [])]
    return {"days": max([t["day"] for t in turns] or [0]), "turns": len(turns), "acts": dict(acts.most_common(8)),
            "refusals": sum(refused.values()), "top refusals": dict(refused.most_common(4)),
            "fallback share": round(fallback / max(1, total), 2), "fish named in takes (kg)": round(fish_got, 1),
            "sets": sets, "tends": tends, "rules set": rules, "lessons done": lessons_ok, "lessons refused": lessons_refused,
            "deaths": deaths}


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--to" in argv:
        i = argv.index("--to"); argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    to = int(sys.argv[sys.argv.index("--to") + 1]) if "--to" in sys.argv else 999
    for p in args:
        print(f"== {Path(p).name}")
        for k, v in arm(p, to).items():
            print(f"  {k}: {v}")
