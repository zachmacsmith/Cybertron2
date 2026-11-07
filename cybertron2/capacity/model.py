"""Food capacity (D4-102): the year simulated, people supported, the labour share, the buffer and a run's horizon.

For a level and a set of flows (sources.py), each flow's good is kept in the form that loses least between harvest and eating
(food.keeping_forms) and eaten through its best route (food.worth). The year is simulated day by day for five years from empty
stores: each day's flows come in, the day's need is eaten most perishable first (as night._eat), what is kept spoils at its night's
rate. A population is fed for good when the last two years run no shortfall. People supported is the largest such population of the
world's own mix (its eaters' rations and its workers' units), with its work going first to the flows that give most food a unit.

`analyse(w)` gives, for every level and node and the whole region: people supported, the ratio to people there, the labour share
food takes at the people there, the buffer (days the stores feed them) and the days to their first own harvest.
"""
from __future__ import annotations

import copy
import io
import contextlib
import math
from dataclasses import dataclass, field

from cybertron2.engine import farm as FM, life as LF
from cybertron2.engine.data import CROPS, PHYSICS
from cybertron2.capacity import food as FD, levels as LV, sources as SO

YEARS = 5


# ---------------------------------------------------------------------------------------------------------------- context
@dataclass
class Ctx:
    w: object
    level: LV.Level
    reach: LV.Reach
    year: int
    season_len: int
    as_field: set = field(default_factory=set)
    cal: list = field(default_factory=list)          # [(season, cold)] a year day (cal.table)
    window: tuple = (0, 0)                           # the frost-free run (cal.growing_window)

    def worth_of(self, good) -> float:
        return FD.worth(good, self.level.cook, self.reach)[0]


def world_of(spec_or_world):
    """A World from a spec dict, a world record dict ({'world': ...} or the state) or a World."""
    from cybertron2.engine.world import World
    if hasattr(spec_or_world, "s"):
        return spec_or_world
    with contextlib.redirect_stdout(io.StringIO()):
        return World(copy.deepcopy(spec_or_world))


def context(w, level, as_field=()) -> Ctx:
    r = LV.reach(w)
    lv = (LV.LEVELS[level] if isinstance(level, str) else level).within(r)
    from cybertron2.capacity import cal as CL
    return Ctx(w=w, level=lv, reach=r, year=w.year_days(), season_len=w.season_len, as_field=set(as_field), cal=CL.table(w),
               window=CL.growing_window(w))


def flows(ctx, nodes=None) -> list:
    out = []
    for name, over, fn in SO.SOURCES:
        if over == "parcel":
            for pid, par in ctx.w.s["parcels"].items():
                if nodes is None or par["node"] in nodes:
                    out += fn(ctx, {**par, "id": pid})
        else:
            for hid, h in ctx.w.s["herds"].items():
                fl = fn(ctx, {**h, "id": hid})
                out += [f for f in fl if nodes is None or f.node in nodes]
    return _dung(out)


def _dung(fl) -> list:
    """Manure needs dung: where the herds give less than the fields would spread, the manured fields' work and gain scale down (the
    fields were evaluated with full manure; this is an upper bound on manure's reach, stated in the note)."""
    need = sum(f.dung for f in fl)
    have = sum(f.dung_out for f in fl)
    if need > have + 1e-9:
        for f in fl:
            if f.dung:
                f.note += f"; dung for {min(1.0, have / need):.0%} of its manuring"
    return fl


# ---------------------------------------------------------------------------------------------------------------- the year
@dataclass
class Lot:
    flow: SO.Flow
    form: str
    value: float              # food a unit of the flow's good, kept in its form and eaten by its best route
    rates: list               # share lost each year day in its form
    work: float               # units a year at full take, with processing


def _season_of(ctx, d):
    return ctx.cal[d % len(ctx.cal)][0]


def _cold_of(ctx, d):
    return ctx.cal[d % len(ctx.cal)][1]


def _hold(profile) -> float:
    """The mean gap in days between a flow's arrivals (a daily flow: 1)."""
    days = [i for i, q in enumerate(profile) if q > 1e-9]
    if len(days) <= 1:
        return float(len(profile))
    gaps = [b - a for a, b in zip(days, days[1:])] + [len(profile) - days[-1] + days[0]]
    return sum(gaps) / len(gaps)


def lots(ctx, fl) -> list:
    out = []
    store = ctx.level.store
    for f in fl:
        if f.qty <= 1e-9:
            continue
        gap = _hold(f.profile)
        best = None
        for form, k, v, u in FD.keeping_forms(f.good, ctx.level.cook, ctx.reach):
            rates = [FD.rate(form, store, _season_of(ctx, d), _cold_of(ctx, d)) for d in range(ctx.year)]
            r = sum(rates) / len(rates)
            keep = 1.0 if r * gap < 1e-9 else (1 - math.exp(-r * gap)) / (r * gap)
            score = k * v * keep
            if best is None or score > best[0]:
                proc = FD.worth(f.good, ctx.level.cook, ctx.reach)[1] if form == f.good else u
                best = (score, form, k * v, rates, proc)
        _, form, value, rates, proc = best
        out.append(Lot(f, form, value, rates, f.work + proc * f.qty))
    return out


def simulate(ctx, ls, scale, need, years=YEARS, start=None, horizon=None, people_food=None) -> dict:
    """Days of the year simulated; returns {short: shortfall in the last two years, short_days, waste, eaten}."""
    stock = {}                                                    # lot index -> food value kept
    short, short_days, waste, eaten, peak = 0.0, 0, 0.0, 0.0, {}
    first_short = None
    if start:
        for k, v in start.items():
            stock[k] = stock.get(k, 0.0) + v
    days = horizon if horizon is not None else years * ctx.year
    y0 = 0 if horizon is not None else (years - 2) * ctx.year
    for t in range(days):
        d = t % ctx.year
        for i, (l, s) in enumerate(zip(ls, scale)):
            if s > 0:
                q = l.flow.profile[d] * s * l.value
                if q:
                    stock[i] = stock.get(i, 0.0) + q
        want = need
        order = sorted(stock, key=lambda i: -(ls[i].rates[d] if i in range(len(ls)) else 0.0))
        for i in order:
            take = min(stock[i], want)
            stock[i] -= take
            want -= take
            if want <= 1e-12:
                break
        if t >= y0:
            eaten += need - want
            if want > 1e-6 * max(need, 1e-9):
                short += want
                short_days += 1
                if first_short is None:
                    first_short = t
        if t >= y0:
            for i, v in stock.items():
                peak[i] = max(peak.get(i, 0.0), v)
        for i in stock:
            r = ls[i].rates[d] if i < len(ls) else start_rate(ctx, d)
            loss = stock[i] * r
            stock[i] -= loss
            if t >= y0:
                waste += loss
    return {"short": short, "short_days": short_days, "waste": waste, "eaten": eaten, "first_short": first_short, "peak": peak}


def start_rate(ctx, d):
    return FD.rate("grain", ctx.level.store, _season_of(ctx, d), _cold_of(ctx, d))


def allocate(ls, budget) -> list:
    """Work to the lots that give most food a unit; free flows (no work) are taken whole."""
    scale = [0.0] * len(ls)
    left = budget
    order = sorted(range(len(ls)), key=lambda i: -(ls[i].flow.qty * ls[i].value / ls[i].work if ls[i].work > 1e-9 else float("inf")))
    for i in order:
        l = ls[i]
        if l.work <= 1e-9:
            scale[i] = 1.0
            continue
        s = min(1.0, max(0.0, left / l.work))
        scale[i] = s
        left -= s * l.work
        if left <= 1e-9:
            left = 0.0
    return scale


# ---------------------------------------------------------------------------------------------------------------- people
def mix(w, names=None) -> dict:
    """Food and work of the world's own people a head: {eats: a day, units: a year, n}. Units by the engine's calendar (PHYSICS
    units by season, youth and elder caps; children and infants none). With nobody, an adult's."""
    from cybertron2.capacity import cal as CL
    names = [n for n in (names if names is not None else w.living())]
    seasons = [s_ for s_, _ in CL.table(w)]
    def units(stage):
        if stage in ("infant", "child"):
            return 0.0
        cap = {"youth": PHYSICS["youth_units"], "elder": PHYSICS["elder_units"]}.get(stage)
        return sum(min(float(PHYSICS["units"][s_]), float(cap)) if cap else float(PHYSICS["units"][s_]) for s_ in seasons)
    if not names:
        return {"eats": float(PHYSICS["ration"]), "units": units("adult"), "n": 0}
    eats, u = 0.0, 0.0
    for n in names:
        m, extra = LF.ration_factor(w, n)
        eats += float(PHYSICS["ration"]) * m + extra
        u += units(w.s["people"][n]["stage"])
    return {"eats": eats / len(names), "units": u / len(names), "n": len(names)}


def fed(ctx, ls, P, m, share=1.0) -> bool:
    scale = allocate(ls, P * m["units"] * share)
    r = simulate(ctx, ls, scale, P * m["eats"])
    return r["short"] <= 1e-6 * max(1.0, P * m["eats"] * ctx.year)


def people_supported(ctx, ls, m, share=None) -> float:
    share = ctx.level.labour_share if share is None else share
    total = sum(l.flow.qty * l.value for l in ls)
    hi = max(1.0, total / max(1e-9, m["eats"] * ctx.year) * 1.5)
    if not fed(ctx, ls, 0.01, m, share):
        return 0.0
    lo = 0.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if fed(ctx, ls, mid, m, share):
            lo = mid
        else:
            hi = mid
        if hi - lo < 0.02:
            break
    return round(lo, 2)


def labour_share(ctx, ls, P, m) -> float | None:
    """The least share of the people's work that feeds them for good (None: not even all of it)."""
    if P <= 0:
        return 0.0
    if not fed(ctx, ls, P, m, 1.0):
        return None
    lo, hi = 0.0, 1.0
    for _ in range(20):
        mid = (lo + hi) / 2
        if fed(ctx, ls, P, m, mid):
            hi = mid
        else:
            lo = mid
    return round(hi, 3)


# ---------------------------------------------------------------------------------------------------------------- stores and timing
def stores_food(w, nodes=None, cook="boiled", r=None) -> float:
    """Food value of what is in store and in hand (of these nodes), eaten by the cook level's best route."""
    from cybertron2.landgen import economy as E
    tot = 0.0
    for c in w.s["containers"].values():
        if nodes is not None and E._container_node(w, c) not in nodes:
            continue
        for g, q in (c.get("goods") or {}).items():
            if g in FD.EDIBLE and q > 0:
                tot += float(q) * FD.worth(g, cook, r)[0]
    return tot


def first_harvest(w, nodes=None, level=None) -> dict:
    """Days from now to the first crop the people bring in: a standing crop that ripens before the frost, or the next sowing's."""
    sl, year = w.season_len, w.year_days()
    cal = w.calendar()
    best, lost = None, []
    for pid, par in w.s["parcels"].items():
        if nodes is not None and par["node"] not in nodes:
            continue
        for _, _, c in FM.standing(par):
            ripe = int(c.get("ripe_day", w.d)) - w.d
            frost = next((k for k in range(0, max(ripe, 0) + 1) if FM.frost_kills(c, w.calendar(w.d + k)["season"])), None)
            if frost is not None and frost < ripe:
                lost.append({"parcel": pid, "ripe_in": ripe, "frost_in": frost, "left": round(float(c.get("left", 0)), 1)})
                continue
            if c.get("left", 0) > 0 and (best is None or max(0, ripe) < best):
                best = max(0, ripe)
    g = FM.grow_days(year, "grain")
    tender = {"hardy": False}
    k = 0
    while k < 2 * year and any(FM.frost_kills(tender, w.calendar(w.d + k + j)["season"]) for j in range(g + 1)):
        k += 1
    sown = k + g
    return {"standing": best, "sown": sown, "first": min(x for x in (best, sown) if x is not None), "lost_to_frost": lost}


def run_horizon(w, level, days, nodes=None) -> dict:
    """From the world's day, with its stores and its people: the day food first runs short, if it does within `days`. Standing
    crops come in on their day unless the frost takes them first; the level's own sowing begins today (its harvests come no sooner
    than a crop sown today ripens), as far as the seed in store allows; the wild and the herds give from the first day. The seed
    is kept back from the store."""
    ctx = context(w, level)
    hb = homes_by_node(w)
    names = [n for k, v in hb.items() if nodes is None or k in nodes for n in v]
    m = mix(w, names)
    P = len(names)
    year = ctx.year
    yd0 = int(w.calendar()["year_day"]) % year
    fl = flows(ctx, nodes)
    seed_need = sum(float(PHYSICS["farming"]["plot_seed"]) * float(par["size"]) for par in w.s["parcels"].values()
                    if par["cover"] == "field" and (nodes is None or par["node"] in nodes)) if ctx.level.fields else 0.0
    from cybertron2.landgen import economy as E
    seed_have = sum(float(q) for c in w.s["containers"].values() if nodes is None or E._container_node(w, c) in nodes
                    for g_, q in (c.get("goods") or {}).items() if g_ in ("grain", "rye", "beans"))
    seed_share = min(1.0, seed_have / seed_need) if seed_need else 1.0
    out_fl = []
    for f in fl:
        dur = max([d for k, s_, d in (f.extra.get("plan") or []) if k != "rest"] or [0])
        prof = []
        for t in range(days):
            q = f.profile[(yd0 + t) % year]
            if f.source == "fields":
                q = q * seed_share if t >= dur else 0.0
            prof.append(q)
        out_fl.append(SO.Flow(f.source, f.node, f.where, f.good, prof, f.work * days / year, extra=f.extra))
    for pid, par in w.s["parcels"].items():
        if nodes is not None and par["node"] not in nodes:
            continue
        for _, _, c in FM.standing(par):
            ripe = int(c.get("ripe_day", w.d)) - w.d
            frost = next((k for k in range(0, max(ripe, 0) + 1) if FM.frost_kills(c, w.calendar(w.d + k)["season"])), None)
            if (frost is not None and frost < ripe) or ripe >= days:
                continue
            prof = [0.0] * days
            prof[max(0, ripe)] = float(c.get("left", 0))
            out_fl.append(SO.Flow("standing crop", par["node"], pid, CROPS.get(c.get("crop"), CROPS["grain"])["gives"], prof, 0.0))
    ctx_h = Ctx(w=w, level=ctx.level, reach=ctx.reach, year=days, season_len=ctx.season_len, cal=ctx.cal, window=ctx.window)
    ls = []
    for f in out_fl:
        probe = SO.Flow(f.source, f.node, f.where, f.good, (f.profile + [0.0] * year)[:year], f.work)
        for l in lots(ctx, [probe]):
            rates = [FD.rate(l.form, ctx.level.store, w.calendar(w.d + t)["season"], w.cold(w.d + t)) for t in range(days)]
            ls.append(Lot(f, l.form, l.value, rates, l.work))
    reserve, left = 0.0, seed_need                      # the seed kept back, taken grain first, at each good's own worth
    for g_ in ("grain", "beans", "rye"):
        have_g = sum(float((c.get("goods") or {}).get(g_, 0.0)) for c in w.s["containers"].values()
                     if nodes is None or E._container_node(w, c) in nodes)
        k = min(have_g, left)
        reserve += k * ctx.worth_of(g_)
        left -= k
    store = max(0.0, stores_food(w, nodes, ctx.level.cook, ctx.reach) - reserve)
    ls.append(Lot(SO.Flow("store", "", "", "grain", [0.0] * days, 0.0), "grain", 1.0,
                  [FD.rate("grain", "house", w.calendar(w.d + t)["season"], w.cold(w.d + t)) for t in range(days)], 0.0))
    scale = allocate(ls, P * m["units"] * ctx.level.labour_share * days / year)
    r = simulate(ctx_h, ls, scale, P * m["eats"], horizon=days, start={len(ls) - 1: store})
    return {"level": ctx.level.name, "people": P, "days": days, "first_short": r["first_short"], "short_days": r["short_days"],
            "short_meals": round(r["short"], 1), "seed_share": round(seed_share, 2), "store_food": round(store, 1)}


# ---------------------------------------------------------------------------------------------------------------- the ceiling
def ceiling_fields(w, nodes=None) -> tuple:
    """Ground turned to field for the ceiling: meadow, pasture and scrub (CLEARING), and forest (felled, then cleared as scrub), the
    parcels losing least firewood first, while the region's woods (fuel can be carried) still keep warm the people the food would
    feed; ground that gives no fuel is always turned. Grazing lost to the herds is not counted (stated). Returns (turned, note)."""
    from cybertron2.capacity import fuel as FU
    from cybertron2.engine.data import CLEARING
    cands = [pid for pid, par in w.s["parcels"].items() if (nodes is None or par["node"] in nodes)
             and (par["cover"] in CLEARING and par["cover"] not in ("fertility", "built") or par["cover"] == "forest")]
    cands.sort(key=lambda pid: FU.parcel_heat(w, w.s["parcels"][pid]))
    m = mix(w)
    turned = set()
    npp = FU.need_per_person(w)
    ctx = context(w, "best")
    P = people_supported(ctx, lots(ctx, flows(ctx, nodes)), m)
    for pid in cands:
        trial = turned | {pid}
        ctx_t = context(w, "best", as_field=trial)
        P_t = people_supported(ctx_t, lots(ctx_t, flows(ctx_t, nodes)), m)
        heat = FU.supply(w, None, exclude=trial)["sustained"]
        if P_t > P and (FU.parcel_heat(w, w.s["parcels"][pid]) <= 0 or heat >= npp * P_t):
            turned, P = trial, P_t
    return turned, f"turned to field: {', '.join(sorted(turned)) or 'none'}"


# ---------------------------------------------------------------------------------------------------------------- the report
def homes_by_node(w) -> dict:
    out = {nid: [] for nid in w.s["nodes"]}
    for n in w.living():
        h = w.homes(n)
        nid = w.s["buildings"][h[0]]["node"] if h else w.s["people"][n].get("at")
        if nid in out:
            out[nid].append(n)
    return out


def analyse(spec_or_world, levels=LV.ORDER, horizon=None) -> dict:
    """The capacity report: by level, for each node and the region (all nodes pooled, no carrying cost)."""
    from cybertron2.capacity import fuel as FU
    w = world_of(spec_or_world)
    people = homes_by_node(w)
    groups = {nid: {nid} for nid in w.s["nodes"]}
    groups["(region)"] = set(w.s["nodes"])
    turned, tnote = ceiling_fields(w) if "ceiling" in levels else (set(), "")
    out = {"year": w.year_days(), "season_len": w.season_len, "day": w.d, "calendar": w.calendar(), "levels": {}, "nodes": {},
           "people": {k: len(v) for k, v in people.items()}, "ceiling": tnote}
    out["people"]["(region)"] = len(w.living())
    for nid, ns in groups.items():
        names = [n for k in ns for n in people.get(k, [])]
        m_here = mix(w, names) if names else mix(w)
        P_here = len(names)
        rec = {"people": P_here, "levels": {}, "stores_food": round(stores_food(w, ns), 1)}
        fh = first_harvest(w, ns)
        rec["first_harvest"] = fh
        rec["buffer_days"] = round(rec["stores_food"] / max(1e-9, P_here * m_here["eats"]), 1) if P_here else None
        for lvl in levels:
            ctx = context(w, lvl, as_field=turned if lvl == "ceiling" else ())
            fl = flows(ctx, ns)
            ls = lots(ctx, fl)
            sup = people_supported(ctx, ls, m_here)
            share = labour_share(ctx, ls, P_here, m_here) if P_here else None
            by_src, by_par = {}, {}
            for l in ls:
                by_src[l.flow.source] = by_src.get(l.flow.source, 0.0) + l.flow.qty * l.value
                by_par[l.flow.where] = round(by_par.get(l.flow.where, 0.0) + l.flow.qty * l.value, 1)
            from cybertron2.capacity import costs as CO
            at = sup if sup > 0 else 0.0
            scale = allocate(ls, at * m_here["units"] * ctx.level.labour_share)
            sim = simulate(ctx, ls, scale, at * m_here["eats"])
            plots = sum(float(p_["size"]) for pid, p_ in w.s["parcels"].items() if p_["node"] in ns
                        and (p_["cover"] == "field" or pid in ctx.as_field))
            rec["levels"][lvl] = {"supported": sup, "ratio": round(sup / P_here, 2) if P_here else None, "labour_share": share,
                                  "food_a_year": {k: round(v, 1) for k, v in by_src.items()}, "gave_up": list(ctx.level.gave_up),
                                  "at_supported": {"recurring": CO.recurring(ctx, ls, scale, at, m_here),
                                                   "capital": CO.capital(ctx, ls, scale, at, sim),
                                                   "land": CO.land(ctx, ls, scale, plots),
                                                   "waste_share": round(sim["waste"] / max(1e-9, sim["eaten"] + sim["waste"]), 3)},
                                  "plan": sorted({l.flow.note for l in ls if l.flow.source == "fields"}), "by_parcel": by_par}
        rec["fuel"] = FU.report(w, ns, P_here)
        if horizon:
            rec["horizon"] = {lvl: run_horizon(w, lvl, horizon, ns) for lvl in ("standing", "worked")}
        out["nodes"][nid] = rec
    for lvl in levels:
        out["levels"][lvl] = LV.LEVELS[lvl].words
    return out
