"""Checks a world file before a run: every craft someone is given can be done where they live (W-58, 17 Nov).

The runs world gave the Brooks the salter's craft ("boil salt") and a brine spring, but no brine pan and no one who knew how to build
one, so the salt was shut away from the start; a bot dry run never tries the craft, so it passed. This walks every person's known
crafts: a craft done at a fitting needs that fitting in a building in the person's village, or someone in their household who knows
how to build it (the fitting's own technique, or a basic one), with its materials somewhere in the world; a craft done on a cover
needs that cover in the village. It reports what fails; it changes nothing.

    python3 -m cybertron2.world_checks WORLD.yaml
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

from cybertron2.engine.data import FITTINGS, TECHNIQUES


def _villages(w) -> dict:
    """{household: node} from where each household's buildings stand."""
    p2n = {pid: nid for nid, n in w["nodes"].items() for pid in (n.get("parcels") or {})}
    out = {}
    for b in w["buildings"].values():
        if b.get("household"):
            out.setdefault(b["household"], p2n.get(b.get("parcel")))
    return out


def gates(w) -> list:
    """[(household, person, craft, why)] for every known craft that cannot be done where its knower lives."""
    p2n = {pid: nid for nid, n in w["nodes"].items() for pid in (n.get("parcels") or {})}
    home = _villages(w)
    fitted = {}                                              # node: the fittings in its buildings
    for b in w["buildings"].values():
        fitted.setdefault(p2n.get(b.get("parcel")), set()).update((b.get("fittings") or {}).keys())
    covers = {nid: {p["cover"] for p in (n.get("parcels") or {}).values()} for nid, n in w["nodes"].items()}
    knows_hh = {}
    for a in w["agents"].values():
        knows_hh.setdefault(a["household"], set()).update((a.get("knows") or {}).keys())
    out, seen = [], set()
    for name, a in w["agents"].items():
        hh, node = a["household"], home.get(a["household"])
        for craft in (a.get("knows") or {}):
            d = TECHNIQUES.get(craft) or {}
            at = d.get("at") or {}
            for f in at.get("fittings") or []:
                if f in fitted.get(node, set()):
                    continue
                fd = FITTINGS.get(f) or {}
                can_build = fd.get("basic") or f in knows_hh.get(hh, set())
                key = (hh, craft, f)
                if not can_build and key not in seen:
                    seen.add(key)
                    out.append((hh, name, craft, f"needs {f}: none in {node}, and nobody in the household knows how to build one"))
            want = at.get("covers") or []
            if want and not (set(want) & covers.get(node, set())) and (hh, craft) not in seen:
                seen.add((hh, craft))
                where = sorted(n for n, cs in covers.items() if set(want) & cs)
                if not where:                                # elsewhere in the world is a journey, not a shut gate
                    out.append((hh, name, craft, f"is done on {', '.join(want)}: none anywhere in the world"))
    return out


def main(argv=None):
    path = (argv or sys.argv[1:])[0]
    w = yaml.safe_load(Path(path).read_text())
    bad = gates(w)
    for hh, name, craft, why in bad:
        print(f"{hh} ({name}): {craft} {why}")
    print(f"{len(bad)} gate(s) shut")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
