"""A field's year under a level (D4-102): the sequence of crops and rest, its steady-state soil, harvests and work.

Everything about the year comes from the engine: each sowing is run night by night through farm.grow_night (D4-106) by the
world's calendar, so when a crop ripens, how much a late sowing gives and whether the cold takes it are the engine's own; a crop's
growing days are farm.grow_days (seed selection: x seed_selection); a hardy crop (rye) may stand through the winter. The soil follows the engine's rules a crop and a night
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
    q = FM.crop_base(F, float(F["plot_seed"]), 1.0 if level.broken else 0.0, fert, ground, skill) * float(CROPS[fam].get("yield", 1.0))
    if level.weed > 0:
        q *= 1 + FM.weed_gain(F, level.weed)
    return q * (1 - FM.fail_chance(F, prev, fam))


def _steady(plan, year, level, ground, mults=None, base=1.0):
    slot = FM.grow_days(year, "grain")
    fert, prev = float(base), None
    mults = mults or {}
    for _ in range(80):
        start = fert
        harvests, gross = [], {}
        for j, (kind, s, days) in enumerate(plan):
            if kind == "rest":
                for _ in range(int(days)):
                    fert = FM.fallow_gain(F, fert, slot, base)
                continue
            if level.manure:
                fert = FM.manure_gain(F, fert, base=base)
            q = _sowing(kind, fert, level, ground, prev) * mults.get(j, 1.0)
            good = CROPS[kind]["gives"]
            harvests.append(((s + days) % year, good, q - float(F["plot_seed"])))
            gross[good] = gross.get(good, 0.0) + q
            fert = FM.soil_step(F, fert, kind, base)
            prev = kind
        if abs(fert - start) < 1e-6:
            break
    return harvests, gross, start


def outcome(fam, start, year, level, cal) -> tuple | None:
    """A sowing of `fam` on year day `start`, by the engine's own nights (farm.season_run, D4-106): (nights to ripe, what it gives
    as a share of a full crop). None if it never ripens within the year."""
    g = grow(year, fam, level)
    days, mult, _ = FM.season_run(fam, start, lambda d: cal[d % year][0], g, F, cold_of=lambda d: cal[d % year][1], horizon=year)
    return (days, mult) if days is not None and days <= year and mult > 0.05 else None


def best_year(window, year, level, ground=1.0, worth=lambda g: 1.0, oxen_ok=False, crops_ok=("grain",), cal=None, base=1.0) -> Year:
    """The level's field year for one plot. `cal` is the world's year ([(season, cold)] a year day: cal.table). Each sowing is run
    through the engine's own growth (D4-106), so when to sow, and how much a late or early sowing gives, come from the engine: no
    sowing window is assumed. "once": one grain crop at its best day; "best": the sequence of sowings and rest that gives most food
    a plot a year at steady state."""
    if cal is None:                                                     # a year of seasons in order, from spring (tests, old callers)
        sl = max(1, year // 4)
        cal = [(("spring", "summer", "autumn", "winter")[min(3, d // sl)], d // sl >= 3) for d in range(year)]
    work_crop, dung_crop = crop_work(level, oxen_ok)
    step = max(1, year // 16)
    starts = list(range(0, year, step))
    fams = [fam for fam in CROPS if CROPS[fam]["seed"] in crops_ok and (level.winter_crop or not CROPS[fam]["hardy"])]
    if level.rotation == "once":
        fams = [f_ for f_ in fams if f_ == "grain"] or fams[:1]
    memo = {}

    def oc(fam, s):
        if (fam, s) not in memo:
            memo[(fam, s)] = outcome(fam, s, year, level, cal)
        return memo[(fam, s)]

    seqs = [[]]
    most = 1 if level.rotation == "once" else 4

    def extend(seq, first, free_from):
        for s in starts:
            if s < free_from:
                continue
            for fam in fams:
                o = oc(fam, s)
                if o is None or s + o[0] > first + year:
                    continue
                new = seq + [(fam, s, o[0], o[1])]
                seqs.append(new)
                if len(new) < most:
                    extend(new, first, s + o[0])

    for s in starts:
        for fam in fams:
            o = oc(fam, s)
            if o is not None:
                seqs.append([(fam, s, o[0], o[1])])
                if most > 1:
                    extend([(fam, s, o[0], o[1])], s, s + o[0])
    rough = sorted(seqs, key=lambda q: -sum(worth(CROPS[k]["gives"]) * m for k, _, _, m in q))[:40]
    best = None
    for seq in rough:
        plan, mults = [], {}
        for j, (kind, s, d, m) in enumerate(seq):
            nxt = seq[j + 1][1] if j + 1 < len(seq) else (seq[0][1] + year if seq else year)
            mults[len(plan)] = m
            plan.append((kind, s % year, d))
            if nxt - (s + d) > 0:
                plan.append(("rest", (s + d) % year, nxt - (s + d)))
        if not plan:
            plan = [("rest", 0, year)]
        harvests, gross, fert = _steady(plan, year, level, ground, mults, base)
        food = sum(q * worth(g) for _, g, q in harvests)
        if best is None or food > best[0] + 1e-9:
            best = (food, plan, harvests, gross, fert)
    food, plan, harvests, gross, fert = best
    n = len(harvests)
    return Year(plan=plan, harvests=harvests, gross=gross, work=n * work_crop, fertility=round(fert, 4), dung=n * dung_crop)
