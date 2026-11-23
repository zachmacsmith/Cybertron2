"""The survey's other counts, each from the run directories or the code (W-103). No model calls.

1. Ambient lines shown, against what the state holds (herds; quarrying days).
2. Gear's remaining life in the morning prompts ("more nights set", "wanting mending").
3. Chores that yielded nothing ("You took 0 cord") fired by the book.
4. The glut: fresh fish spoiled by day, and which smokehouses had a lot that night.
5. The meal that read as vanishing: set B new, day 2, what each of Brook House's sleepers ate, in roots.
6. The river's rows (wild/river.py DAWN and DAY).

Usage: python3 -I live1_checks.py [/home/user/live1] [/home/user/cybertron2] > live1_checks.txt
"""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/user/live1")
REPO = Path(sys.argv[2] if len(sys.argv) > 2 else "/home/user/cybertron2")
ARMS = ["live1_A_pre", "live1_A_old", "live1_A_new", "live1_B_pre", "live1_B_new"]
AMBIENT = ("cattle lowing", "dung and trodden grass", "ring of picks", "voices and work about the houses", "water running over stones",
           "nothing out of the ordinary")


def lines_of(state):
    for m in state["mind"].values():
        for d in m.get("days") or []:
            for x in (d.get("saw_day") or []) + (d.get("saw") or []):
                yield x


def main() -> None:
    out = []
    out.append("## 1. Ambient lines shown, against the state")
    for a in ARMS:
        st = json.load(open(ROOT / a / "state.json"))
        c = collections.Counter()
        for x in lines_of(st):
            for k in AMBIENT:
                if k in x:
                    c[k] += 1
        db = sqlite3.connect(ROOT / a / "run.db")
        q = db.execute("select distinct day from events where kind='work' and text like '%quarrying%'").fetchall()
        out.append(f"{a}: herds in the state {len(st['herds'])}; days anyone quarried {sorted(r[0] for r in q)}; "
                   + ", ".join(f"{k!r} {c[k]}" for k in AMBIENT))
    out.append("\n## 2. Gear's remaining life in the morning prompts")
    for a in ARMS:
        n = sum(len(re.findall(r"more nights set|wanting mending", json.loads(l).get("prompt") or "")) for l in open(ROOT / a / "turns.jsonl"))
        out.append(f"{a}: {n} lines")
    out.append("\n## 3. Book firings that yielded nothing")
    for a in ARMS:
        c = collections.Counter()
        for l in open(ROOT / a / "days.jsonl"):
            for f in ((json.loads(l).get("book") or {}).get("fired") or []):
                if re.search(r"took 0 ", f.get("words", "")):
                    c[re.sub(r" at .*", "", f["words"])] += 1
        out.append(f"{a}: " + (", ".join(f"{k!r} x{v}" for k, v in c.most_common()) or "none"))
    out.append("\n## 4. Fresh fish spoiled by night (kg), and the smokehouses with a lot that night")
    for a in ARMS:
        rows = []
        for l in open(ROOT / a / "days.jsonl"):
            d = json.loads(l)
            fish = float((d.get("spoiled") or {}).get("fish", 0.0))
            if fish >= 10:
                rows.append(f"day {d['day']} {fish:.1f} kg (food {fish * 0.46:.1f}); smoking: {sorted((d.get('smokehouse') or {}).keys())}")
        out.append(f"{a}: " + ("; ".join(rows) or "no night over 10 kg"))
    out.append("\n## 5. Set B new, night of day 2: what Brook House's sleepers ate")
    for l in open(ROOT / "live1_B_new" / "days.jsonl"):
        d = json.loads(l)
        if d["day"] == 2:
            who = [n for n, b in d["slept"].items() if b == "Brook House"]
            tot = sum(float(d["ate"].get(n, 0.0)) for n in who)
            out.append(f"sleepers {who}; ate {tot:.2f} food = {tot / 0.263:.1f} roots at 0.263 a root (data.py roots); "
                       f"roots spoiled that night, both houses: {float(d['spoiled'].get('roots', 0)):.2f}")
    out.append("\n## 6. The river's rows")
    src = (REPO / "cybertron2" / "wild" / "river.py").read_text()
    dawn = src[src.index("DAWN = {"):src.index("# the run itself")]
    day = src[src.index("DAY = ["):src.index("CARRIED = {")]
    out.append(f"DAWN keys {len(re.findall(r'^    \"[a-z_]+\": _row', dawn, re.M))}; DAY rows {len(re.findall(r'^    _row\(', day, re.M))}")
    print("\n".join(out))


if __name__ == "__main__":
    main()
