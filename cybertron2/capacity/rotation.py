"""A field's year under a level (D4-102): the sequence of crops and rest, its steady-state soil, harvests and work.

Everything about the year comes from the engine: the growing window is the longest run of days on which farm.frost_kills spares a
tender crop (cal.growing_window, from world.calendar); a crop grows farm.grow_days (seed selection: x seed_selection); a hardy
crop (rye) may stand through the frost, sown to ripen as the window opens. The soil follows the engine's rules a crop and a night
(farm.soil_step, farm.fallow_gain, farm.manure_gain); a sowing gives farm.crop_base x (1 + farm.weed_gain) x (1 - farm.fail_chance),
net of its seed. "once" sows one grain crop as the window opens and rests the rest of the year; "best" searches every sequence of
crops and rest that fits the window for the most food a plot a year at steady state.

Work a plot a crop: sowing (TECHNIQUES sow: seed a unit), breaking (hoe, or plough with oxen), weeding, manuring and gathering its
dung, reaping (TECHNIQUES reap: plots a unit), each by the level's tool multiplier.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass

from cybertron2.engine import farm as FM
from cybertron2.engine.data import CROPS, PHYSICS, TECHNIQUES

F = PHYSICS["farming"]


@dataclass
class Year:
    plan: list            # [(kind, start year day, days)]
    harvests: list        # [(year day, good, net qty a plot)]
    gross: dict
    work: float           # units a plot a year
    fertility: float
    dung: float


def tool_mult(tech, tools) -> float:
    t = TECHNIQUES[tech].get("tools") or {}
    if not t:
        return 1.0
    for g in (tools, "crude", "bare"):
        if g in t:
            return float(t[g])
    return 1.0


def crop_work(level, oxen_ok) -> tuple:
    sow = float(F["plot_seed"]) / float(TECHNIQUES["sow"]["yield"]["seed"])
    reap = 1.0 / (float(TECHNIQUES["reap"]["yield"]["plots"]) * tool_mult("reap", level.tools))
    brk = 0.0
    if level.broken:
        brk = 1.0 / float(TECHNIQUES["plough"]["yield"]["plots"]) if oxen_ok else \
            1.0 / (float(TECHNIQUES["hoe"]["yield"]["plots"]) * tool_mult("hoe", level.tools))
    man = dung = 0.0
    if level.manure:
        man = 1.0 / float(TECHNIQUES["manure"]["yield"]["plots"])
        dung = float(TECHNIQUES["manure"]["inputs"]["dung"]) * man
        man += dung / float(TECHNIQUES["dung"]["yield"]["base"])
    return sow + reap + brk + level.weed + man, dung


def grow(year, fam, level) -> int:
    g = FM.grow_days(year, fam)
    return max(2, round(g * float(PHYSICS["seed_selection"]))) if level.selection else g


def _sowing(fam, fert, level, ground, prev) -> float:
    skill = 1.0 + (float(PHYSICS["master_yield"]) if level.master else 0.0)
    q = FM.crop_base(F, float(F["plot_seed"]), 1.0 if level.broken else 0.0, fert, ground, skill)
    if level.weed > 0:
        q *= 1 + FM.weed_gain(F, level.weed)
    return q * (1 - FM.fail_chance(F, prev, fam))


def _steady(plan, year, level, ground):
    slot = FM.grow_days(year, "grain")
    fert, prev = 1.0, None
    for _ in range(80):
        start = fert
        harvests, gross = [], {}
        for kind, s, days in plan:
            if kind == "rest":
                for _ in range(int(days)):
                    fert = FM.fallow_gain(F, fert, slot)
                continue
            if level.manure:
                fert = FM.manure_gain(F, fert)
            q = _sowing(kind, fert, level, ground, prev)
            good = CROPS[kind]["gives"]
            harvests.append(((s + days) % year, good, q - float(F["plot_seed"])))
            gross[good] = gross.get(good, 0.0) + q
            fert = FM.soil_step(F, fert, kind)
            prev = kind
        if abs(fert - start) < 1e-6:
            break
    return harvests, gross, start


def best_year(window, year, level, ground=1.0, worth=lambda g: 1.0, oxen_ok=False, crops_ok=("grain",)) -> Year:
    """The level's field year for one plot; `window` is (start year day, length) of the frost-free run."""
    s0, L = window
    frost_len = year - L
    work_crop, dung_crop = crop_work(level, oxen_ok)
    cands = []
    if level.rotation == "once":
        cands.append(([("grain", grow(year, "grain", level))], False))
    else:
        opts = [(fam, grow(year, fam, level)) for fam in CROPS if not CROPS[fam]["hardy"] and CROPS[fam]["seed"] in crops_ok]
        opts.append(("rest", FM.grow_days(year, "grain")))
        hardy = [fam for fam in CROPS if CROPS[fam]["hardy"] and CROPS[fam]["seed"] in crops_ok] if level.winter_crop else []
        for over in [None] + hardy:
            room = L - (max(0, grow(year, over, level) - frost_len) if over else 0)
            for n in range(0, 8):
                for seq in itertools.product(opts, repeat=n):
                    if sum(d for _, d in seq) <= room and (not seq or seq[-1][0] != "rest"):
                        cands.append((list(seq), over))
    best = None
    for seq, over in cands:
        plan, t = [], 0
        for kind, days in seq:
            plan.append((kind, (s0 + t) % year, days))
            t += days
        if over:
            g = grow(year, over, level)
            plan.append(("rest", (s0 + t) % year, max(0, year - g - t)))
            plan.append((over, (s0 - g) % year, g))
        else:
            plan.append(("rest", (s0 + t) % year, year - t))
        harvests, gross, fert = _steady(plan, year, level, ground)
        food = sum(q * worth(g) for _, g, q in harvests)
        if best is None or food > best[0] + 1e-9:
            best = (food, plan, harvests, gross, fert)
    food, plan, harvests, gross, fert = best
    n = len(harvests)
    return Year(plan=plan, harvests=harvests, gross=gross, work=n * work_crop, fertility=round(fert, 4), dung=n * dung_crop)
