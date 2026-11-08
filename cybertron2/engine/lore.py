"""Lore (D4-105): what families know from long practice, which the rules never tell anyone. Each LORE row is seeded at the start as
a line kept for good (memory.seed_line, D4-64) to those it fits; it passes on as any kept line does (a carer to a child, talk).
Those without it learn by trying, by being told, or by watching others.

- sowing: when each crop goes in (CROPS sow_seasons) and which stands the winter. Sown out of its season a crop does not come up
  (farm._sow), and nobody is told why.
"""
from __future__ import annotations

from cybertron2.engine.data import CROPS, LORE


def text(key) -> str:
    if key == "sowing":
        bits = [f"{d['names'][0]} in {' or '.join(d['sow_seasons'])}" for d in CROPS.values() if d.get("sow_seasons")]
        hardy = [d["names"][0] for d in CROPS.values() if d.get("hardy")]
        return ("Sow " + ", ".join(bits) + (f"; {' and '.join(hardy)} stands the winter" if hardy else "")
                + "; sown out of season, nothing comes up.")
    raise KeyError(key)


def farmers(w) -> set:
    """Who holds a field: households (their adult members) and people, by their claims."""
    out = set()
    for pid, p in w.s["parcels"].items():
        if p["cover"] != "field":
            continue
        for c in w.claims_on(("parcel", pid)):
            out.add(c["claimant"])
    return out


def fits(w, name, to, holders) -> bool:
    if to == "farmers":
        return name in holders or w.household_of(name) in holders
    return False


def seed(w, name) -> None:
    from cybertron2.engine import life as LF, memory as MEM
    off = w.spec.get("lore")
    if off is False:
        return
    a = w.s["people"][name]
    if a.get("stage") in LF.MINOR:
        return
    holders = None
    for key, row in LORE.items():
        if isinstance(off, dict) and off.get(key) is False:
            continue
        holders = farmers(w) if holders is None else holders
        if fits(w, name, row["to"], holders):
            MEM.seed_line(w, name, text(key), "family lore")
