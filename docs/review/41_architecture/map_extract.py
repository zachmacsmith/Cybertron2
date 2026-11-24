"""Extract the four patterns surveys' mechanism tables (W-110) into one list: survey, id, mechanism, where, pattern, fit.

Run from the repository root: python3 docs/review/41_architecture/map_extract.py [--labels]"""
import re
import sys
from pathlib import Path

ROOT = Path("docs/review/37_growth/02zzzm_patterns")
SURVEYS = {"A": "A_physics.md", "B": "B_making.md", "C": "C_people.md", "D": "D_senses.md"}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def rows():
    out = []
    for s, f in SURVEYS.items():
        head = None
        for line in (ROOT / f).read_text().splitlines():
            if line.startswith("| #"):
                head = [h.lower() for h in cells(line)]
                continue
            if head and line.startswith("|") and not line.startswith("|---"):
                c = cells(line)
                if len(c) < 5 or not re.match(r"^[A-Z]{0,2}\d+[a-z]?$", c[0]):
                    continue
                d = dict(zip(head, c))
                pat = next((d[k] for k in d if k.startswith("pattern")), "")
                out.append({"survey": s, "id": c[0], "mech": d.get("mechanism", ""), "where": d.get("where", ""),
                            "pattern": pat, "fit": d.get("fit", "")})
            elif head and not line.startswith("|"):
                head = None if line.startswith("#") else head
    return out


if __name__ == "__main__":
    R = rows()
    if "--labels" in sys.argv:
        from collections import Counter
        c = Counter()
        for r in R:
            for t in re.split(r"[,;/+]| and ", re.sub(r"\(.*?\)", "", r["pattern"])):
                t = t.strip()
                if t:
                    c[(r["survey"], t)] += 1
        for (s, t), n in sorted(c.items()):
            print(s, n, t)
    else:
        from collections import Counter
        print(Counter(r["survey"] for r in R))
