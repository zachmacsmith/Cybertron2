"""Eelmouth small: the remade Eelmouth with two households (the Marshes at the weir, the Brooks at the salt), for live run 1's
"longer and smaller" set (D2-335). Made from the files make_eelmouth.py writes: the Shepherds, their house and smokehouse are
taken out, and every mention of them; everything else is as in eelmouth.yaml and eelmouth_old.yaml. Six people play (Peter and
Oliver on Opus at the two poles, Nichola on Sonnet, three on Haiku); the four children are the world's.

    python3 cybertron2/specs/make_eelmouth_small.py [--days 40] [--old-days 40]
"""
from __future__ import annotations

import os
import sys

import yaml

HERE = os.path.join(os.path.dirname(__file__), "nutrition")
GONE_HOUSEHOLD = "Shepherd"


def shrink(w: dict, name: str, days: int) -> dict:
    gone = {n for n, a in w["agents"].items() if a.get("household") == GONE_HOUSEHOLD}
    w["name"] = name
    w["days"] = days
    w["agents"] = {n: a for n, a in w["agents"].items() if n not in gone}
    for a in w["agents"].values():
        for k in ("relations", "aware_of"):
            if isinstance(a.get(k), dict):
                a[k] = {kk: vv for kk, vv in a[k].items() if kk not in gone}
        for k in ("memories", "kept"):                                   # lines that name the gone household
            if isinstance(a.get(k), list):
                a[k] = [m for m in a[k] if not any(g in yaml.safe_dump(m) for g in gone | {GONE_HOUSEHOLD})]
        if isinstance(a.get("aware_of"), dict):                          # a source that names the gone household
            a["aware_of"] = {kk: (vv.replace("the Shepherds", "the Marshs") if isinstance(vv, str) else vv)
                             for kk, vv in a["aware_of"].items()}
    if isinstance((w.get("skills") or {}).get("households"), dict):
        w["skills"]["households"].pop(GONE_HOUSEHOLD, None)
    w["buildings"] = {b: d for b, d in w["buildings"].items() if d.get("household") != GONE_HOUSEHOLD}
    if isinstance(w.get("tree"), list):
        w["tree"] = [t for t in w["tree"] if not (isinstance(t, dict) and t.get("name") in gone)]
    if isinstance(w.get("history"), list):
        w["history"] = [h for h in w["history"] if not any(g in yaml.safe_dump(h) for g in gone | {GONE_HOUSEHOLD})]
    if isinstance(w.get("claims"), list):
        w["claims"] = [c for c in w["claims"] if not any(g in yaml.safe_dump(c) for g in gone | {GONE_HOUSEHOLD})]
    left = yaml.safe_dump(w)
    for g in gone | {GONE_HOUSEHOLD}:
        if g in left:
            print(f"warning: {name} still mentions {g}", flush=True)
    return w


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 40
    old_days = int(sys.argv[sys.argv.index("--old-days") + 1]) if "--old-days" in sys.argv else days
    from cybertron2.landgen import gate_check as GC
    for src, name, d in (("eelmouth", "eelmouth_small", days), ("eelmouth_old", "eelmouth_small_old", old_days)):
        with open(os.path.join(HERE, f"{src}.yaml")) as f:
            w = yaml.safe_load(f)
        w = shrink(w, name, d)
        with open(os.path.join(HERE, f"{name}.yaml"), "w") as f:
            f.write(f"# {name}: Eelmouth small (two households), made by cybertron2/specs/make_eelmouth_small.py from {src}.yaml.\n")
            yaml.safe_dump(w, f, sort_keys=False, allow_unicode=True, width=200)
        g = GC.check(w)
        print(name, "gate:", g["verdict"], "refusals", len(g["refuse"]), "warnings", len(g["warn"]),
              [r.get("id") if isinstance(r, dict) else r for r in g["refuse"]][:6], flush=True)


if __name__ == "__main__":
    main()
