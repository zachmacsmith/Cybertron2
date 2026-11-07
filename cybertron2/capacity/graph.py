"""The production graph (D4-102): every technique as a process, and the work every good embodies, read from the engine's tables.

A process turns inputs into outputs for a number of units of work, needing fittings, a cover, beasts, a tool (whose wear is a share
of a tool worn a use: ITEMS life) or a trade. Processes come from TECHNIQUES:
- make: inputs (TECHNIQUES inputs; a fuel choice is its cheapest) to gives;
- gather by a yield kind: fixed and pool (base a unit), stock (base x the stock's share: by default the share its best steady take
  keeps), chance (p x the stock's share x the mean of its range x the weapon), each by the tool multiplier, from a resource on the
  land (no input);
- milk (each a cow x cows a unit);
- the fields: a plot's year under a level (rotation.py) as one process, its seed as input.
The embodied work of a good is the least, over the processes that give it, of the process's units plus its inputs' embodied work
plus its tool's wear, a unit of output: solved by repeated relaxation, so cycles (a tool made of timber felled with a tool) settle
at their fixed point. Capital (a fitting, a room) is its units plus its materials' embodied work.

New techniques join without a change here, provided their yield kind is one this module reads (`KINDS`); the capacity test fails
when the engine gains a kind no reader covers (proposals/process_model.md, part 2: each kind should declare its own expectation).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from cybertron2.engine.data import FITTINGS, ITEMS, ROOMS, TECHNIQUES

KINDS = ("fixed", "pool", "stock", "chance", "milk", "break")     # yield kinds read here as processes
ELSEWHERE = {"crop": "rotation.py (a plot's year)", "sow": "rotation.py", "tend": "rotation.py (weeding)",
             "manure": "rotation.py", "select": "levels (seed selection)", "slaughter": "sources.herds (calves)",
             "herd": "no goods (watching)", "care": "no goods (children)", "works": "ground (rotation: best levels assume done)",
             "clear": "model.ceiling_fields", "clear_built": "no food", "fence": "no food", "gate": "no food",
             "repair": "costs (upkeep, not yet)", "bury": "no goods"}


@dataclass
class Process:
    name: str
    inputs: dict
    outputs: dict
    units: float
    fittings: list = field(default_factory=list)
    covers: list = field(default_factory=list)
    animals: dict = field(default_factory=dict)
    tool: str | None = None          # the tool good worn, if any
    wear: float = 0.0                # share of a use a unit
    trade: str | None = None
    draws: str | None = None         # a resource on the land


GRADES = ("bare", "crude", "copper")


def _tools(d, tools):
    """[(tool good or None, multiplier)] for each grade the technique allows, up to the level's: the relaxation picks the cheapest."""
    t = d.get("tools") or {}
    if not t:
        return [(None, 1.0)]
    top = GRADES.index(tools) if tools in GRADES else 1
    return [((None if g == "bare" else f"{g} tool"), float(t[g])) for g in GRADES[:top + 1] if g in t and float(t[g]) > 0]


def processes(tools="crude", stock_share=0.5, armed=True, level=None, window=None, year=None) -> list:
    out = []
    for name, d in TECHNIQUES.items():
        verb, y = d.get("verb"), d.get("yield") or {}
        at = d.get("at") or {}
        units = float(d.get("units", 1) or 1)
        for tool, mult in _tools(d, tools):
            tag = f"{name}" + (f" [{tool}]" if tool else "")
            common = dict(fittings=list(at.get("fittings") or []), covers=list(at.get("covers") or []),
                          animals=dict(d.get("animals") or {}), tool=tool, wear=float(d.get("wear", 0) or 0) if tool else 0.0,
                          trade=d.get("trade"), draws=d.get("draws"))
            if verb == "make" and isinstance(d.get("gives"), dict):
                ins = {i: float(q) for i, q in (d.get("inputs") or {}).items() if not isinstance(q, dict)}
                choices = [(i, q) for i, q in (d.get("inputs") or {}).items() if isinstance(q, dict)]
                gives = {g: float(q) for g, q in d["gives"].items() if g in ITEMS}
                for opt, q in (choices[0][1].items() if choices else [(None, None)]):
                    extra = {opt: float(q)} if opt else {}
                    out.append(Process(tag + (f" ({opt})" if opt else ""), {**ins, **extra}, gives, units / max(mult, 1e-9), **common))
            elif verb == "gather" and y.get("kind") in ("fixed", "pool", "stock", "chance") and d.get("gives") in ITEMS:
                if y["kind"] in ("fixed", "pool"):
                    per = float(y["base"]) * mult
                elif y["kind"] == "stock":
                    per = float(y["base"]) * stock_share * mult
                else:
                    wpn = d.get("weapon") or {}
                    per = float(y["p"]) * stock_share * sum(y["range"]) / 2 * float(wpn.get("armed" if armed else "none", 1.0))
                if per > 0:
                    out.append(Process(tag, {}, {d["gives"]: per * units}, units, **common))
            elif verb == "work" and y.get("kind") == "milk":
                out.append(Process(tag, {}, {"milk": float(y["cows"]) * float(y["each"])}, units, **common))
            elif verb == "work" and y.get("kind") == "break" and float(y.get("stone", 0)) > 0:
                out.append(Process(tag + " (fieldstone)", {}, {"stone": float(y["plots"]) * mult * float(y["stone"]) * units}, units,
                                   **common))
    if level is not None and window is not None and year is not None:
        from cybertron2.capacity import rotation as RO
        yr = RO.best_year(window, year, level)
        net = {}
        for _, g, q in yr.harvests:
            net[g] = net.get(g, 0.0) + q
        out.append(Process(f"a plot's year ({level.name}), net of its seed", {}, {g: q for g, q in net.items() if q > 0}, yr.work,
                           covers=["field"],
                           tool=f"{level.tools} tool" if level.tools != "bare" else None, wear=0.3 if level.tools != "bare" else 0.0))
    return out


def embodied(procs, rounds=60) -> dict:
    """{good: (units of work a unit, the process)} at the least."""
    best = {}
    for _ in range(rounds):
        changed = False
        for p in procs:
            cost = p.units
            ok = True
            for i, q in p.inputs.items():
                if i not in best:
                    ok = False
                    break
                cost += q * best[i][0]
            if not ok:
                continue
            if p.tool:
                if p.tool not in best:
                    continue
                life = float(ITEMS.get(p.tool, {}).get("life", 10) or 10)
                cost += p.wear * p.units * best[p.tool][0] / life
            total_out = sum(p.outputs.values()) or 1.0
            for g, q in p.outputs.items():
                share = q / total_out                                  # joint outputs share the cost by quantity
                c = cost * share / q
                if g not in best or c < best[g][0] - 1e-9:
                    best[g] = (c, p.name)
                    changed = True
        if not changed:
            break
    return best


def capital_work(costs, kind, name, structure="timber") -> float | None:
    """Units of work a fitting or a room embodies: its own units and its materials' (and what it needs, for a fitting)."""
    if kind == "fitting":
        d = FITTINGS[name]
        mats, units = d.get("materials") or {}, float(d.get("units", 0))
        extra = capital_work(costs, "fitting", d["needs"]) if d.get("needs") else 0.0
    else:
        r = ROOMS[name].get(structure) or {}
        mats, units, extra = r.get("materials") or {}, float(r.get("units", 0)), 0.0
    tot = units + (extra or 0.0)
    for m, q in mats.items():
        if m not in costs:
            return None
        tot += float(q) * costs[m][0]
    return round(tot, 1)
