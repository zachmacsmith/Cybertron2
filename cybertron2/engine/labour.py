"""Labour's costs (D4-103 phase 2; proposals/economic_calibration.md E, F; OPEN Q-2, L-35). PHYSICS["labour"]:

- **Work costs food:** each unit worked today adds `work_food` to the night's need, a unit pushed past the day's counts `over_food`
  units, a night on guard adds `guard_food`. The part for work also raises the least one must eat not to go hungry (night.py), so a
  famine's last workers pay for their work.
- **Pushing on (Q-2):** one may work up to `over_units` past the day's units (the reply's "overwork"); each leaves `fatigue` units
  off tomorrow.
- **The walk (L-35; D4-105):** the day's route (layout.route, D4-62: the shortest path joining where one slept, each parcel worked
  in order, and where one sleeps) costs `step` of a unit for each leg past the first `free_steps`, carried until it makes a whole
  unit, which comes off a later day.
- **Skill fades (F; D4-105):** a craft unpractised for `fade_after` of a year loses `fade_rate` a year of what can still be lost,
  but never more than (1 - `fade_keep`) of its best gain over the craft's floor; below one's best, practice counts `relearn` times
  over (knowledge.tried), so a skill once held comes back quickly.

Every value at 0 is the engine before phase 2, and then nothing here writes to the world.
"""
from __future__ import annotations


def L(p) -> dict:
    return p.get("labour") or {}


def work_need(p, today, name) -> float:
    """The food tonight's need gains for today's work and watch."""
    lb = L(p)
    u = (today.get("units") or {}).get(name)
    need = 0.0
    if u and float(lb.get("work_food", 0) or 0):
        over = int(u.get("over", 0))
        need += float(lb["work_food"]) * (int(u["used"]) - over + over * float(lb.get("over_food", 1.0)))
    if float(lb.get("guard_food", 0) or 0) and (name in (today.get("guards") or {}) or name in (today.get("night_watch") or {})):
        need += float(lb["guard_food"])                                         # a night on guard or on watch (D2-21)
    return round(need, 4)


def close_day(w, today, used, budget, names) -> None:
    """After the day's acts: each one's units worked (for the night's food), fatigue for tomorrow from pushing on and from the walk."""
    lb = L(w.p)
    eat = float(lb.get("work_food", 0) or 0) > 0
    fatigue = int(lb.get("fatigue", 0) or 0)
    step = float(lb.get("step", 0) or 0)
    units = {}
    for n in names:
        a = w.s["people"].get(n) or {}
        if not a.get("alive", True):
            continue
        over = max(0, int(used.get(n, 0)) - int(budget.get(n, 0)))
        if eat:
            units[n] = {"used": int(used.get(n, 0)), "over": over}
        off = over * fatigue + (int(lb.get("watch_tired", 0) or 0) if n in (today.get("night_watch") or {}) else 0)   # D2-21
        if step:
            r = (today.get("route") or {}).get(n) or []
            extra = max(0, len(r) - 1 - int(lb.get("free_steps", 2)))           # legs walked past the free ones
            walked = round(float(a.get("walked", 0.0)) + extra * step, 4)
            whole = int(walked + 1e-9)
            if whole:
                off += whole
                walked = round(walked - whole, 4)
            if walked != float(a.get("walked", 0.0)):
                w.apply("set", w.place_of(("person", n)), ref=("person", n), field="walked", value=walked)
        if off:
            w.apply("set", w.place_of(("person", n)), ref=("person", n), field="tired", value={"day": w.d + 1, "units": off})
    if eat:
        today["units"] = units


def tired_units(w, name) -> int:
    t = w.s["people"][name].get("tired")
    return int(t["units"]) if t and t.get("day") == w.d else 0


def fade(w) -> None:
    """Each night: crafts unpractised for long lose some skill, toward a floor that keeps most of one's best (F; D4-105)."""
    lb = L(w.p)
    rate = float(lb.get("fade_rate", 0) or 0)
    if not rate:
        return
    from cybertron2.engine import knowledge as KN
    year = float(w.year_days())
    after = float(lb.get("fade_after", 0.5)) * year
    keep = float(lb.get("fade_keep", 0.6))
    for name in w.living():
        for tech, r in sorted((w.s["know"].get(name) or {}).items()):
            if not isinstance(r, dict) or r.get("skill") is None:
                continue
            lo = KN.curve(tech)[0]
            sk = float(r["skill"])
            best = max(float(r.get("peak", sk)), sk)
            floor = lo + keep * (best - lo)
            if sk <= floor + 1e-6:
                continue
            last = int(r.get("practised", max(0, int(r.get("since", 0) or 0))))
            if w.d - last >= after:
                r["peak"] = round(best, 4)
                r["skill"] = round(floor + (sk - floor) * (1 - rate / year), 4)
