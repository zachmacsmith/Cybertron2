"""Food sources (D4-102): each turns a parcel or a herd into flows of food goods across the year, with the work they take.

A source is a function registered with @source(name, over="parcel"|"herd"); it gets the context (the world, the level, the reach,
the calendar) and one parcel or herd, and returns Flows. A Flow's profile is the net quantity of its good on each day of the year
(year day 0 = spring's first day); its work is the units a year it needs at full take. The model scales a flow by the share of its
work it is given, so a source says only what the land gives and what it costs.

To add a source (fishing, an orchard, bees): write one function here and register it. Its numbers come from the engine's tables.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from cybertron2.engine import farm as FM
from cybertron2.engine.data import PHYSICS, TECHNIQUES
from cybertron2.capacity import rotation as RO

SOURCES = []                     # [(name, over, fn)]


def source(name, over="parcel"):
    def wrap(fn):
        SOURCES.append((name, over, fn))
        return fn
    return wrap


@dataclass
class Flow:
    source: str
    node: str
    where: str                   # parcel or herd id
    good: str
    profile: list                # net qty on each year day
    work: float                  # units a year at full take
    dung: float = 0.0            # dung a year it uses (manure)
    dung_out: float = 0.0        # dung a year it gives (herds)
    note: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def qty(self) -> float:
        return sum(self.profile)


def _daily(ctx, by_season) -> list:
    """A daily flow by the engine's calendar: by_season(season, cold) for each year day."""
    return [by_season(season, cold) for season, cold in ctx.cal]


# ---------------------------------------------------------------------------------------------------------------- fields
@source("fields")
def fields(ctx, par):
    """A field's year under the level (rotation.py), for each plot. Under `clear`, ground the model has turned to field too."""
    lv = ctx.level
    is_field = par["cover"] == "field" or par["id"] in ctx.as_field
    if not is_field or not lv.fields:
        return []
    plots = float(par["size"])
    ground = 1.0 if lv.name in ("best", "ceiling") else FM.ground_mult(ctx.w.p, par)
    if par["id"] in ctx.as_field:
        from cybertron2.engine.data import CLEARING
        ground = float(CLEARING.get("fertility", {}).get(par["cover"], 1.0))
    yr = RO.best_year(ctx.window, ctx.year, lv, ground=ground, cal=list(ctx.cal), worth=ctx.worth_of, oxen_ok=ctx.reach.oxen >= 2
                      and ctx.reach.knows("plough"), crops_ok=tuple(ctx.reach.seed) or ("grain",))
    out = {}
    for day, good, q in yr.harvests:
        prof = out.setdefault(good, [0.0] * ctx.year)
        prof[day % ctx.year] += q * plots
    flows = []
    total = sum(sum(p) for p in out.values()) or 1.0
    for good, prof in out.items():
        share = sum(prof) / total
        flows.append(Flow("fields", par["node"], par["id"], good, prof, yr.work * plots * share, dung=yr.dung * plots * share,
                          note=", ".join(f"{k} {d}d" for k, s, d in yr.plan if d and k != "rest"),
                          extra={"fertility": yr.fertility, "plan": yr.plan}))
    return flows


# ---------------------------------------------------------------------------------------------------------------- the wild
def msy(step, K) -> tuple:
    """The best steady take a night of a stock whose night is `step(S)` (an engine function), and the stock it stands at when the
    day's take begins. The engine takes by day and regrows at night, so the cycle is: stand at step(y), take step(y) - y, regrow from
    y; the best y gives the most."""
    best = (0.0, K)
    for i in range(1, 400):
        y = K * i / 400
        g = step(y) - y
        if g > best[0]:
            best = (g, step(y))
    return best


def _gatherers(key):
    """The gathering techniques that take this stock and give a food (TECHNIQUES: draws, gives, a yield kind yields.py reads)."""
    from cybertron2.engine import yields as YD
    from cybertron2.capacity.food import EDIBLE
    return [(t, d) for t, d in TECHNIQUES.items() if d.get("verb") == "gather" and d.get("draws") == key
            and (d.get("yield") or {}).get("kind") in YD.KINDS and d.get("gives") in EDIBLE]


def _per_unit(ctx, t, d, S, K, b=1.0):
    """Food a unit of work at stock S: the mean of the act's own outcome (yields.dist), with the best tool and weapon the level and
    the world reach."""
    from cybertron2.engine import yields as YD, outcomes as OC
    from cybertron2.capacity import rotation as RO
    tm = RO.tool_mult(t, ctx.level.tools) if d.get("tools") else 1.0
    wpn = d.get("weapon") or {}
    armed = ctx.reach.tool("crude") and ("crude weapon" in ctx.reach.goods or "timber" in ctx.reach.goods) and ctx.level.tools != "bare"
    weapon = float(wpn.get("armed" if armed else "none", 1.0)) if wpn else 1.0
    v = YD.dist(d["yield"], {"S": S, "K": K}, 1.0, tm, weapon=weapon, refuge=float(PHYSICS["refuge"]), b=b).mean()
    return OC.got(v) / float(d.get("units", 1) or 1)


def _usable(ctx, t, d) -> bool:
    if not ctx.reach.knows(t):
        return False
    if t == "hunt" and not ctx.level.hunt:
        return False
    tools = d.get("tools") or {}
    return not (tools and "bare" not in tools and not any(ctx.reach.tool(g) for g in tools if g != "bare"))


def _steady(ctx, key, res):
    """The best steady take a night, and the stock it stands at, by the engine's own renewal step, for each year day."""
    from cybertron2.engine import renewal as RN, night as NI
    top = max(float(res["K"]), float(res.get("run_K", 0) or 0))
    out, memo = [], {}
    for season, cold in ctx.cal:
        if (season, cold) not in memo:
            c = {"winter": NI.slow_season(season), "season": season}
            memo[(season, cold)] = msy(lambda S: RN.step(ctx.w.p, key, {**res, "S": S}, c), top)
        out.append(memo[(season, cold)])
    return out


@source("the wild")
def wild(ctx, par):
    """Every renewable stock on the parcel that a known gathering technique takes for food: plants, game, fish and whatever the data
    adds. Its steady take comes from the stock's own renewal rule (renewal.py), its yield a unit of work from the act's own outcome
    (yields.py), at the stock it stands at each day. Nothing here is particular to a stock."""
    from cybertron2.engine import renewal as RN
    if par["id"] in ctx.as_field:
        return []
    out = []
    for key, res in (par.get("res") or {}).items():
        if RN.of(key, res) not in RN.NIGHTLY or float(res.get("K", 0)) <= 0:
            continue
        gs = [(t, d) for t, d in _gatherers(key) if _usable(ctx, t, d)]
        if not gs:
            continue
        K = float(res["K"])
        b = RN.response(key, res)
        steady = _steady(ctx, key, res)
        prof = [g for g, _ in steady]
        units = 0.0
        best_t = None
        for take, S in steady:                                  # each day's take at that day's stock, by the best gatherer then
            t, d = max(gs, key=lambda td: _per_unit(ctx, td[0], td[1], S, K, b))
            pu = _per_unit(ctx, t, d, S, K, b)
            units += take / pu if pu > 0 else 0.0
            best_t = best_t or (t, d)
        if units <= 0:
            continue
        S0 = max(steady, key=lambda x: x[0])[1]
        name = {"plants": "wild plants", "game": "game"}.get(key, key)
        out.append(Flow(name, par["node"], par["id"], best_t[1]["gives"], prof, units,
                        note=f"{key}: K {K:g}, kept at {S0 / max(K, 1e-9):.0%}, by {best_t[0]}",
                        extra={"standing": float(res.get("S", K)) - S0}))
    return out


# ---------------------------------------------------------------------------------------------------------------- herds
@source("herds", over="herd")
def herds(ctx, h):
    lv = ctx.level
    cows = int(h.get("cows", 0) or 0)
    head = int(h.get("count", 0) or 0) or cows + int(h.get("oxen", 0) or 0) + int(h.get("bulls", 0) or 0) + int(h.get("young", 0) or 0)
    c = PHYSICS["cattle"]
    node = h.get("node") or (ctx.w.s["parcels"].get(h.get("parcel")) or {}).get("node")
    out = []
    if lv.herds != "none" and cows:
        y = TECHNIQUES["milk"]["yield"]
        known = ctx.reach.knows("milk")
        m = 1.0 if known else float(PHYSICS["untaught"])
        day = cows * float(c["in_milk_share"]) * float(y["each"]) * m
        prof = [day] * ctx.year
        work = cows * float(c["in_milk_share"]) / float(y["cows"]) * ctx.year
        out.append(Flow("herds", node, h["id"], "milk", prof, work, dung_out=head * float(c["dung"]) * ctx.year / ctx.w.year_days(),
                        note=f"{cows} cows" + ("" if known else ", milked untaught")))
    if lv.herds == "milk+offtake" and cows and int(h.get("bulls", 0) or 0):
        meat = float(TECHNIQUES["slaughter"]["yield"]["gives"]["young"]["meat"])
        a_year = cows * float(c["births"]) * float(c["survive"]) * meat
        prof = [a_year / ctx.year] * ctx.year
        out.append(Flow("herds", node, h["id"], "meat", prof, a_year / meat * float(TECHNIQUES["slaughter"]["units"]),
                        note="calves slaughtered as the herd breeds"))
    elif not out and head:
        out.append(Flow("herds", node, h["id"], "milk", [0.0] * ctx.year, 0.0, dung_out=head * float(c["dung"]), note="no cows"))
    return out
