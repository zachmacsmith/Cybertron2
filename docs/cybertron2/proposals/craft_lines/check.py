"""Merge the five drafted parts into craft_lines.json and check them against the engine's crafts (W-205).

    python3 docs/cybertron2/proposals/craft_lines/check.py

Checks: every TECHNIQUES key present once; every shown craft has does, aware, rough, capable and known; the word limits of
BRIEF.md; no em dashes; an existing `does` copied unchanged unless marked new; numbers flagged (the generated recipe gives them).
Prints a report and writes craft_lines.json beside this file.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
from cybertron2.engine.data import TECHNIQUES  # noqa: E402

LIMITS = {"aware": 10, "rough": 25, "capable": 30, "known": 30}
LEVELS = ("aware", "rough", "capable", "known")


def words(s) -> int:
    return len(str(s or "").split())


def main():
    merged, dupes = {}, []
    for p in sorted(glob.glob(os.path.join(HERE, "part_*.json"))):
        for k, v in json.load(open(p)).items():
            if k in merged:
                dupes.append(k)
            merged[k] = v
    missing = [k for k in TECHNIQUES if k not in merged]
    extra = [k for k in merged if k not in TECHNIQUES]
    problems = []
    for k, v in merged.items():
        if k not in TECHNIQUES or not v.get("shown", True):
            continue
        for f in ("does",) + LEVELS:
            if not str(v.get(f) or "").strip():
                problems.append(f"{k}: no {f}")
        for f, n in LIMITS.items():
            if words(v.get(f)) > n:
                problems.append(f"{k}: {f} has {words(v.get(f))} words (limit {n})")
        for f in ("does",) + LEVELS:
            if "—" in str(v.get(f) or ""):
                problems.append(f"{k}: em dash in {f}")
        old = TECHNIQUES[k].get("does")
        if old and not v.get("does_is_new") and v.get("does") != old:
            problems.append(f"{k}: existing does changed without does_is_new")
        for f in LEVELS:
            if re.search(r"\d", str(v.get(f) or "")):
                problems.append(f"{k}: a number in {f} (check it is not a generated one): {v.get(f)!r}")
    shown = [k for k, v in merged.items() if v.get("shown", True)]
    new = [k for k in shown if merged[k].get("does_is_new")]
    doubts = {k: v["doubts"] for k, v in merged.items() if str(v.get("doubts") or "").strip()}
    json.dump(dict(sorted(merged.items())), open(os.path.join(HERE, "craft_lines.json"), "w"), indent=1, ensure_ascii=False)
    print(f"crafts {len(merged)} of {len(TECHNIQUES)}; shown {len(shown)}; new does {len(new)}; with doubts {len(doubts)}")
    print(f"missing {missing}\nextra {extra}\nduplicates {dupes}")
    print(f"problems ({len(problems)}):")
    for p in problems:
        print("  " + p)
    return 1 if missing or extra or [p for p in problems if "a number" not in p] else 0


if __name__ == "__main__":
    sys.exit(main())
