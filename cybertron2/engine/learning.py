"""Learning as one record (u9_people.md §4; D2-267, D2-307, D2-326): the feature unit of knowing and learning (D2-244). Its data
(`CLASSES`, `CLASS_OF`), its scale (`scale`: every increment x 64 / lifespan, every share 1 - (1 - f)^s, every time / s), its events
(`tried`: a try or practice; `taught`: a lesson session; `fade_params`: fading on the life clock) and the try's odds and materials by
class (`try_row`).

On in a world with `learning: record`; a world without it keeps knowledge.py's rules (two successes a level, one day's teaching to
capable, fading on the year clock), so old worlds replay.

The record (knowledge.py's `Mind.know[tech]`, widened): level, score (toward the next level), practice (the curve's x, stored),
skill, peak, tries {ok, failed}, taught (lesson sessions had), with seen, source, since and practised as before.

- **Classes** (u9 §4.2, at lifespan 64; calibrate): simple, practised, skilled: the chance a try works and the materials it takes by
  level, the score to rise, tau and the skill range.
- **Practice alone reaches known** (D2-326), more slowly: never taught, the score to known is `ALONE` times the class's mark, and in
  a skilled craft skill past half the range grows at `ALONE_BEYOND` of the rate (u9 §4.2's untaught ceiling, made a slope).
- **Teaching is far more efficient** (D2-326; u9 §4.6): a session gives +2 score (scaled), lifts a simple or practised craft to
  capable at once (a skilled one to rough, then capable at the second), and moves skill toward the teacher's peak by
  f' = 1 - (1 - f)^s, f = 0.25 (x1.3 when the teacher is at their peak); the learner never passes the teacher's peak by teaching.
- **Fading on the life clock** (D2-273, D2-307): unpractised `fade_after` 16 days at lifespan 64, then `fade_rate` of what can still
  be lost each `fade_span` 32 days, each divided by s.

Not built here (u9 §4): lessons and failure lines, capability points, aptitudes, attention spent in units, children minded at home.
"""
from __future__ import annotations

import math

LEARN_BASE = 64                                   # u9 §4.3: the lifespan the learning numbers are set at (D2-267)
CLASSES = {                                       # u9 §4.2 (calibrate)
    "simple": {"chance": {"aware": 0.6, "rough": 0.8, "capable": 0.95, "known": 1.0},
               "inputs": {"aware": 1.3, "rough": 1.15, "capable": 1.05, "known": 1.0},
               "mark": {"aware": 1, "rough": 2, "capable": 2}, "tau": 7.0, "range": (0.8, 1.3), "shape": (1.0, 1.0, 1.0)},
    "practised": {"chance": {"aware": 0.35, "rough": 0.55, "capable": 0.8, "known": 1.0},
                  "inputs": {"aware": 1.8, "rough": 1.5, "capable": 1.2, "known": 1.0},
                  "mark": {"aware": 2, "rough": 3, "capable": 4}, "tau": 17.0, "range": (0.6, 1.6), "shape": (1.0, 1.0, 1.0)},
    "skilled": {"chance": {"aware": 0.15, "rough": 0.35, "capable": 0.65, "known": 1.0},
                "inputs": {"aware": 2.0, "rough": 1.8, "capable": 1.4, "known": 1.0},
                "mark": {"aware": 3, "rough": 4, "capable": 4}, "tau": 33.0, "range": (0.5, 2.0), "shape": (0.2, 0.5, 2.0)},
}
ALONE = 2.0                                       # D2-326: the score to known by practice alone, as a multiple of the class's mark
ALONE_BEYOND = 0.25                               # a skilled craft's practice past half its range, untaught and not beside a master
TEACH = {"f": 0.25, "at_peak": 1.3, "score": 2.0}  # u9 §4.6 (calibrate)
FADE = {"after": 16.0, "span": 32.0, "rate": 0.5}   # u9 §4.3 at lifespan 64 (D4-105's half a year and a year at a 32-day year)
# the wave's crafts by class (u3 writes the rows; these are the defaults until a row carries `class`): the rest by basic (simple) or
# trade (practised)
CLASS_OF = {
    "snares": "simple", "snare": "simple", "salt fish": "simple", "salt meat": "simple", "cut withies": "simple", "twist cord": "simple",
    "dry fish": "simple", "dry meat": "simple", "hand line": "simple", "fish by hand": "simple",
    "wicker trap": "practised", "trap in water": "practised", "smoke fish": "practised", "smoke meat": "practised",
    "tend the smoke": "practised", "angle": "practised", "gill net": "practised", "set line": "practised", "set lines": "practised",
    "boil salt": "practised", "fishing rod": "practised", "dip net": "practised", "mend gear": "practised",
    "weir": "skilled", "gill nets": "skilled", "copper hook": "skilled", "hard cure fish": "skilled", "hard cure meat": "skilled",
    "mend the brine pan": "skilled", "smelt": "skilled", "copper tool": "skilled",
}


def on(w) -> bool:
    spec = getattr(w, "spec", None)
    if spec is None:
        spec = getattr(getattr(w, "_w", None), "spec", None) or {}
    return str((spec or {}).get("learning") or "") == "record"


def scale(lifespan) -> float:
    """s = 64 / lifespan (u9 §4.3; D2-307)."""
    return float(LEARN_BASE) / max(1.0, float(lifespan))


def share(f, s) -> float:
    """A learning share scaled: 1 - (1 - f)^s."""
    return 1.0 - (1.0 - float(f)) ** float(s)


def cls(tech) -> str:
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.engine import knowledge as KN
    t = TECHNIQUES.get(tech) or {}
    if t.get("class") in CLASSES:
        return t["class"]
    if tech in CLASS_OF:
        return CLASS_OF[tech]
    return "simple" if KN.basic(tech) else "practised"


def curve_range(tech) -> tuple:
    return CLASSES[cls(tech)]["range"]


def skill_of(tech, p) -> float:
    """u9 §4.2's one formula: lo + (hi - lo) [s (1 - e^(-p/t1)) + (1 - s)(1 - e^(-p/t2))]."""
    c = CLASSES[cls(tech)]
    lo, hi = c["range"]
    s_, a, b = c["shape"]
    tau = c["tau"]
    p = max(0.0, float(p))
    f = s_ * (1 - math.exp(-p / (tau * a))) + (1 - s_) * (1 - math.exp(-p / (tau * b)))
    return round(lo + (hi - lo) * f, 4)


def practice_of(tech, sk) -> float:
    """The practice that gives a skill (inverted by bisection: the two-part curves have no closed form)."""
    lo, hi = curve_range(tech)
    sk = min(max(float(sk), lo), hi - 1e-6)
    a, b = 0.0, 1.0
    while skill_of(tech, b) < sk and b < 1e5:
        b *= 2
    for _ in range(60):
        m = (a + b) / 2
        if skill_of(tech, m) < sk:
            a = m
        else:
            b = m
    return round(b, 4)


def try_row(w, tech, lvl) -> dict:
    """The odds and the materials of a try at `lvl` (u9 §4.2), or knowledge's TRY where learning is not on."""
    from cybertron2.engine.data import TRY
    if not on(w):
        return TRY[lvl]
    c = CLASSES[cls(tech)]
    return {"chance": c["chance"].get(lvl, 1.0), "inputs": c["inputs"].get(lvl, 1.0)}


def _mark(tech, lvl, r) -> float:
    m = float(CLASSES[cls(tech)]["mark"].get(lvl, 99))
    if lvl == "capable" and not int(r.get("taught", 0) or 0):
        m *= ALONE                                                          # practice alone reaches known, more slowly (D2-326)
    return m


def tried(here, mind, tech, ok, units=1) -> str:
    """A try or practice of a craft (u9 §4.4): score by the outcome, practice by the units, both x s; a level rises at its class's
    mark (score carried to 0). Returns the new level, or ''."""
    from cybertron2.engine import knowledge as KN
    r = mind.know.get(tech)
    if r is None and KN.basic(tech):
        lo = curve_range(tech)[0]
        mind.know[tech] = r = {"level": "known", "skill": lo, "seen": 0, "source": "", "since": here.day}
    if r is None:
        return ""
    s = scale(here.life()["lifespan"])
    t = r.setdefault("tries", {"ok": 0, "failed": 0})
    t["ok" if ok else "failed"] = int(t.get("ok" if ok else "failed", 0)) + 1
    lb = here.p.get("labour") or {}
    lo, hi = curve_range(tech)
    sk0 = float(r.get("skill", lo))
    p0 = float(r["practice"]) if r.get("practice") is not None else practice_of(tech, sk0)
    gain = float(units) * s * (1.0 if ok else 0.5)
    if float(lb.get("fade_rate", 0) or 0):
        r["practised"] = here.day
        if r.get("peak") is not None and sk0 < float(r["peak"]) - 1e-9:     # coming back to a skill once held (D4-105)
            gain *= float(lb.get("relearn", 1.0))
    if cls(tech) == "skilled" and not int(r.get("taught", 0) or 0) and sk0 >= lo + 0.5 * (hi - lo):
        gain *= ALONE_BEYOND                                               # past half the range alone: slower (D2-326)
    r["practice"] = round(p0 + gain, 4)
    r["skill"] = max(sk0, skill_of(tech, r["practice"]))
    if r.get("peak") is not None and r["skill"] > float(r["peak"]):
        r["peak"] = r["skill"]
    if r["level"] == "known":
        return ""
    lvl = r["level"]
    r["score"] = round(float(r.get("score", 0.0)) + s * (1.0 if ok or lvl == "aware" else 0.5), 4)
    nxt = {"aware": "rough", "rough": "capable", "capable": "known"}.get(lvl)
    if nxt and r["score"] + 1e-9 >= _mark(tech, lvl, r):
        r["score"] = 0.0
        here.apply("learn", person=mind.name, tech=tech, level=nxt, source="from practice")
        return nxt
    return ""


def taught(w, teacher, learner, tech) -> dict:
    """One lesson session (u9 §4.6): score +2 x s; a simple or practised craft to capable at once, a skilled one to rough, then capable
    at the second; skill toward the teacher's peak by f'. Returns {before, after, skill, gain} for the words."""
    from cybertron2.engine.data import LEVELS
    from cybertron2.engine import knowledge as KN
    s = scale(__import__("cybertron2.engine.life", fromlist=["lifespan"]).lifespan(w))
    k = w.s["know"].setdefault(learner, {})
    lo, hi = curve_range(tech)
    r = k.get(tech)
    before = (r or {}).get("level") or "aware"
    tr = (w.s["know"].get(teacher) or {}).get(tech) or {}
    peak = max(float(tr.get("peak") or 0.0), float(tr.get("skill", lo)))
    c = cls(tech)
    n = int((r or {}).get("taught", 0) or 0) + 1
    target = "capable" if c in ("simple", "practised") or n >= 2 else "rough"
    after = before if LEVELS.index(before) >= LEVELS.index(target) else target
    node = w.at(teacher)
    if after != before:
        w.apply("learn", node, person=learner, tech=tech, level=after, source=f"taught by {teacher}")
    r = k[tech]
    r["taught"] = n
    if after == before and before != "known":
        r["score"] = round(float(r.get("score", 0.0)) + float(TEACH["score"]) * s, 4)
        if r["score"] + 1e-9 >= _mark(tech, before, r):
            nxt = {"aware": "rough", "rough": "capable", "capable": "known"}[before]
            r["score"] = 0.0
            w.apply("learn", node, person=learner, tech=tech, level=nxt, source=f"taught by {teacher}")
            after = nxt
    f = float(TEACH["f"]) * (float(TEACH["at_peak"]) if float(tr.get("skill", lo)) >= peak - 0.1 * (hi - lo) else 1.0)
    sk = float(r.get("skill", lo))
    gain = max(0.0, share(min(0.95, f), s) * (peak - sk))
    r["skill"] = round(min(max(sk, peak), sk + gain), 4)
    r["practice"] = practice_of(tech, r["skill"])
    return {"before": before, "after": after, "skill": r["skill"], "gain": gain}


def fade_params(w) -> tuple:
    """(after, rate a night) on the life clock (u9 §4.3): 16 days and half of what can be lost each 32, at lifespan 64; / s."""
    from cybertron2.engine import life as LF
    s = scale(LF.lifespan(w))
    return FADE["after"] / s, FADE["rate"] / (FADE["span"] / s)
