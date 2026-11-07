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
    yr = RO.best_year(ctx.window, ctx.year, lv, ground=ground, worth=ctx.worth_of, oxen_ok=ctx.reach.oxen >= 2
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


def _regrow(ctx, key, K, r):
    from cybertron2.engine import night as NI
    reg = NI.REGIMES[key]
    def at(season, cold):
        return msy(lambda S: NI.regrow(ctx.w.p, reg, S, K, r, NI.slow_season(season)), K)
    return at


@source("wild plants")
def plants(ctx, par):
    res = (par.get("res") or {}).get("plants")
    if not res or float(res.get("K", 0)) <= 0 or par["id"] in ctx.as_field:
        return []
    K, r = float(res["K"]), float(res.get("r", 0.3))
    at = _regrow(ctx, "plants", K, r)
    S = max((at(s_, c_) for s_, c_ in set(ctx.cal)), key=lambda x: x[0])[1]
    per_unit = float(TECHNIQUES["forage"]["yield"]["base"]) * S / K
    prof = _daily(ctx, lambda s_, c_: at(s_, c_)[0])
    return [Flow("wild plants", par["node"], par["id"], "wild food", prof, sum(prof) / max(1e-9, per_unit),
                 note=f"K {K:g}, kept at {S / K:.0%}", extra={"standing": float(res.get("S", K)) - S})]


@source("game")
def game(ctx, par):
    res = (par.get("res") or {}).get("game")
    if not res or float(res.get("K", 0)) <= 0 or not ctx.level.hunt or par["id"] in ctx.as_field:
        return []
    K, r = float(res["K"]), float(res.get("r", 0.25))
    at = _regrow(ctx, "game", K, r)
    S = max((at(s_, c_) for s_, c_ in set(ctx.cal)), key=lambda x: x[0])[1]
    y = TECHNIQUES["hunt"]["yield"]
    armed = ctx.reach.tool("crude") and ("crude weapon" in ctx.reach.goods or "timber" in ctx.reach.goods)
    mult = float(TECHNIQUES["hunt"]["weapon"]["armed" if armed and ctx.level.tools != "bare" else "none"])
    per_unit = float(y["p"]) * S / K * (sum(y["range"]) / 2) * mult / float(TECHNIQUES["hunt"]["units"])
    prof = _daily(ctx, lambda s_, c_: at(s_, c_)[0])
    return [Flow("game", par["node"], par["id"], "meat", prof, sum(prof) / max(1e-9, per_unit),
                 note=f"K {K:g}, kept at {S / K:.0%}; {'armed' if mult >= 1 else 'unarmed'}", extra={"standing": float(res.get("S", K)) - S})]


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
