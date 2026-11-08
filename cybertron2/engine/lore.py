"""Lore (D4-105): what families know from long practice, which the rules never tell anyone. Each LORE row is seeded at the start as
a line kept for good (memory.seed_line, D4-64) to those it fits; it passes on as any kept line does (a carer to a child, talk).
Those without it learn by trying, by being told, or by watching others.

- sowing: the season each crop does best sown in, read from the engine's own growth (farm.season_run, D4-106), and that winter
  grain wants a winter. Sown at another time a crop grows as the season lets it, and nobody is told why.
"""
from __future__ import annotations

from cybertron2.engine.data import CROPS, LORE


def text(key) -> str:
    if key == "sowing":
        bits = [f"{CROPS[fam]['names'][0]} in {' or '.join(s)}" for fam, s in best_seasons().items()]
        wants = [d["names"][0] for d in CROPS.values() if d.get("needs_winter") is not None]
        return ("Sow " + ", ".join(bits) + (f"; {' and '.join(wants)} wants a winter" if wants else "")
                + "; sown late, crops come up poor.")
    raise KeyError(key)


def best_seasons(season_days=8) -> dict:
    """Each crop's best season to sow in: the seasons whose sowings give within 5% of its best, by the engine's own nights over a
    year of `season_days` seasons (farm.season_run). The lore is the engine, as a family has learnt it."""
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import PHYSICS
    order = ("spring", "summer", "autumn", "winter")
    year = 4 * season_days
    season_of = lambda d: order[(d // season_days) % 4]                 # noqa: E731
    out = {}
    for fam in CROPS:
        g = FM.grow_days(year, fam)
        mean = {s: sum(FM.season_run(fam, i * season_days + k, season_of, g, PHYSICS["farming"],
                                     cold_of=lambda d: season_of(d) == "winter")[1] for k in range(season_days)) / season_days
                for i, s in enumerate(order)}
        top = max(mean.values())
        out[fam] = [s for s in order if mean[s] >= 0.95 * top]
    return out


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
