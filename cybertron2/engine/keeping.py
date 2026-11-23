"""Salt inland (build brief 5 §4b; proposals/river_and_water.md; D2-209).

The smokehouse, the hearth's rack and every other processing container are u4's unit now (engine/process.py, stage 3, W-99); the
names older callers use are kept here as its aliases. What stays here is salt, not processing (u4 code table, keeping.py:247-252):
the brine spring, a `brine` stock on a parcel (endless). A brine pan is fitted only in a building at or beside one; `boil salt` is
done at it (TECHNIQUES `spring` via the fitting).
"""
from __future__ import annotations

from cybertron2.engine.process import burn_building, catch, fuel_cids, is_smokehouse  # noqa: F401  (u4's, kept for older callers)


def near_spring(w, pid, kind="brine") -> bool:
    """A spring of `kind` on a parcel or one beside it (brief 5 §4b.2)."""
    ps = w.s["parcels"]
    return any(x in ps and kind in (ps[x].get("res") or {}) and float(ps[x]["res"][kind].get("S", 0.0)) > 1e-9
               for x in [pid] + list(ps[pid].get("adj") or []))
