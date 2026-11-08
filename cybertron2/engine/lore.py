"""Lore (D4-105): what families know from long practice, which the rules never tell anyone. Each LORE row is seeded at the start as
a line kept for good (memory.seed_line, D4-64) to those it fits; it passes on as any kept line does (a carer to a child, talk).
Those without it learn by trying, by being told, or by watching others.

- sowing: when each crop does best sown, and when it still does well, by halves of the seasons, read from the engine's own growth
  (farm.season_run, D4-106; D4-114), and that winter grain wants a winter. Sown at another time a crop grows as the season lets it, and nobody is told why.
"""
from __future__ import annotations

from cybertron2.engine.data import CROPS, LORE


def text(key) -> str:
    if key == "sowing":
        bits = []
        for fam, (best, well) in sowing_times().items():
            name = CROPS[fam]["names"][0]
            bit = f"{name} {'do' if name.endswith('s') else 'does'} best sown {_when(best)}"
            if well:
                bit += f", and well {_when(well)}"
            bits.append(bit)
        wants = [d["names"][0] for d in CROPS.values() if d.get("needs_winter") is not None]
        return ("; ".join(bits).capitalize() + (f"; {' and '.join(wants)} wants a winter" if wants else "")
                + "; sown at other times, crops come up poor or not at all.")
    raise KeyError(key)


ORDER = ("spring", "summer", "autumn", "winter")
HALVES = [(h, s) for s in ORDER for h in ("early", "late")]


def _when(halves) -> str:
    """Halves of seasons in words: both halves of a season are the season ('in spring'), one is 'early in summer'."""
    out = []
    for s in ORDER:
        hs = [h for h, s_ in halves if s_ == s]
        if len(hs) == 2:
            out.append(f"in {s}")
        elif hs:
            out.append(f"{hs[0]} in {s}")
    return " or ".join(out) if len(out) <= 2 else ", ".join(out[:-1]) + " or " + out[-1]


def sowing_times(season_days=8, well=0.75) -> dict:
    """Each crop's best and good times to sow, by halves of the seasons (D4-114): what a sowing then gives by the engine's own nights
    over a year of `season_days` seasons (farm.season_run). Best: within 5% of its best half; well: at least `well` of a full crop.
    A family knows more than one window: barley in spring, and well early in summer; beans best early in summer. The lore is the
    engine, as a family has learnt it."""
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import PHYSICS
    year = 4 * season_days
    season_of = lambda d: ORDER[(d // season_days) % 4]                # noqa: E731
    out = {}
    for fam in CROPS:
        g = FM.grow_days(year, fam)
        mean = {}
        for i, s in enumerate(ORDER):
            for h, ks in (("early", range(0, season_days // 2)), ("late", range(season_days // 2, season_days))):
                mean[(h, s)] = sum(FM.season_run(fam, i * season_days + k, season_of, g, PHYSICS["farming"],
                                                 cold_of=lambda d: season_of(d) == "winter")[1] for k in ks) / len(ks)
        top = max(mean.values())
        best = [x for x in HALVES if mean[x] >= 0.95 * top]
        out[fam] = (best, [x for x in HALVES if x not in best and mean[x] >= well])
    return out


def best_seasons(season_days=8) -> dict:
    """The seasons in which a crop's best sowing half falls (for callers that want seasons)."""
    return {fam: sorted({s for _, s in best}, key=ORDER.index) for fam, (best, _) in sowing_times(season_days).items()}


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
