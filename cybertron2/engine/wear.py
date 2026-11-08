"""Fittings wear (D4-103 phase 2; proposals/economic_calibration.md G; building_risks.md: capital has upkeep).

A fitting's row may carry `wear`: {life, count, mend} for wear by use (count "act": each act done at it; "inputs": the quantity of
inputs it works) or {years, mend} for wear by time (a share of the year, on the year clock). A worn fitting works at half: an act
there takes and gives half (a worn millstone grinds half the grain in the same work). Its mending technique (TECHNIQUES, yield kind
"mend") sets it right. The record is the building's `worn`: {fitting: {"used": n, "since": day mended}}. PHYSICS labour.wear false
turns it off (the engine before phase 2).
"""
from __future__ import annotations

from cybertron2.engine.data import FITTINGS


def on(p) -> bool:
    return bool((p.get("labour") or {}).get("wear"))


def _rec(b, f) -> dict:
    return (b.get("worn") or {}).get(f) or {}


def is_worn(p, b, f, day, year) -> bool:
    wr = (FITTINGS.get(f) or {}).get("wear")
    if not wr or not on(p):
        return False
    r = _rec(b, f)
    if wr.get("life") is not None and float(r.get("used", 0.0)) >= float(wr["life"]):
        return True
    if wr.get("years") is not None and day - int(r.get("since", b.get("built_day") or 0)) >= float(wr["years"]) * year:
        return True
    return False


def factor(p, b, fittings, day, year) -> float:
    """What an act at these fittings of building b gives, as a share: half if any is worn."""
    return 0.5 if b is not None and any(is_worn(p, b, f, day, year) for f in fittings) else 1.0


def worn_words(p, b, fittings, day, year) -> str:
    bad = [f for f in fittings if is_worn(p, b, f, day, year)]
    if not bad:
        return ""
    return "; ".join(f"the {FITTINGS[f]['label'].replace('a ', '', 1).replace('an ', '', 1)} worn: half as much until mended "
                     f"({FITTINGS[f]['wear']['mend']})" for f in bad)


def use(here, bid, fittings, inputs_qty) -> None:
    """An act done at these fittings: each fitting that wears by use counts it."""
    if not on(here.p):
        return
    b = here.buildings()[bid]
    worn = dict(b.get("worn") or {})
    changed = False
    for f in fittings:
        wr = (FITTINGS.get(f) or {}).get("wear") or {}
        if wr.get("life") is None:
            continue
        r = dict(worn.get(f) or {})
        r["used"] = round(float(r.get("used", 0.0)) + (float(inputs_qty) if wr.get("count") == "inputs" else 1.0), 4)
        worn[f] = r
        changed = True
    if changed:
        here.apply("set", ref=("building", bid), field="worn", value=worn)


def mend(here, bid, f) -> str:
    b = here.buildings()[bid]
    worn = dict(b.get("worn") or {})
    was = is_worn(here.p, b, f, here.day, here.year_days())
    worn[f] = {"used": 0.0, "since": here.day}
    here.apply("set", ref=("building", bid), field="worn", value=worn)
    return "set right" if was else "seen to, though it was not yet worn"
