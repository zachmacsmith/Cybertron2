"""The refusals of a run, by kind, for reading (W-111 acceptance 1): every refused act in turns.jsonl, its text with the numbers and
the names of people, places, buildings and goods put in angle brackets, counted, with one example each and who met it.

    python3 tools/refusals.py <run dir> [<run dir> ...] [--top 40]

A kind is read as explained when its text tells the person what is wrong and what would do instead; the rest are the faults to fix.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path


def _names(run: Path) -> list:
    spec = json.loads((run / "run.json").read_text()).get("spec") or {}
    names = set(spec.get("agents") or {})
    for nd in (spec.get("nodes") or {}).values():
        names.add(nd.get("name") or "")
        names |= {p.get("name") or "" for p in (nd.get("parcels") or {}).values()}
    names |= {b.get("name") or "" for b in (spec.get("buildings") or {}).values()}
    names |= {i.get("name") or "" for i in (spec.get("institutions") or {}).values()}
    return sorted((n for n in names if len(n) > 2), key=len, reverse=True)


def kind(text: str, names: list) -> str:
    t = text
    for n in names:
        t = t.replace(n, "<name>")
    t = re.sub(r"\b\d+(\.\d+)?\b", "<n>", t)
    t = re.sub(r"'[^']{1,60}'", "<said>", t)
    return t[:220]


def read(run: Path) -> dict:
    names = _names(run)
    out = collections.OrderedDict()
    for line in open(run / "turns.jsonl"):
        t = json.loads(line)
        for r in t.get("results") or []:
            r = str(r)
            if not r.startswith(("Refused", "CRASH", "Not done")):
                continue
            k = kind(r, names)
            e = out.setdefault(k, {"n": 0, "example": r[:300], "who": set(), "days": set()})
            e["n"] += 1
            e["who"].add(t.get("agent"))
            e["days"].add(t.get("day"))
    return out


def main(argv) -> int:
    top = 40
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
        argv = [a for i, a in enumerate(argv) if a != "--top" and (i == 0 or argv[i - 1] != "--top")]
    for a in argv:
        run = Path(a)
        rs = read(run)
        total = sum(e["n"] for e in rs.values())
        print(f"# {run}: {total} refusals in {len(rs)} kinds")
        for k, e in sorted(rs.items(), key=lambda x: -x[1]["n"])[:top]:
            print(f"{e['n']:5}  {len(e['who']):3} people  days {min(e['days'])}-{max(e['days'])}  {k}")
            print(f"        e.g. {e['example']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
