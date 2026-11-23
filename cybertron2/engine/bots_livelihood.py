"""Livelihood bots (W-69; D2-256): scripted players that live off a livelihood competently and plainly, by rules, not search, so a
world's live model runs can be read against what the world allows.

A run selects one with `--bots POLICY` (`python3 -m cybertron2.engine run WORLD --bots runs ...`): run.run writes the run's spec
`bot_livelihood` (a policy name, or {"policy": name, ...knobs}), so a resume or a replay keeps it, and every bot then plays by it
instead of run.bot_plan's smoke-test rules. The world files carry nothing for it. Unit seams (D2-244, feature_packages.md §9):
this module is the whole feature.
  - data: POLICIES (name -> the policy), KNOBS (each policy's defaults); nothing is written to the world;
  - verbs: only the engine's own acts, as a model would send them (gather, take, move, make, work, set, order, rest);
  - signs: none of its own; it reads the state a person there could see (its traps, the stores, the racks, the weir's sections,
    the run at the village's water when its sign would show, the river's height tonight, what wild food stands);
  - processes: none; run.bot_plan calls `plan` when `on(w)`.

A fair player, not an optimiser: it knows the year (the run windows, as a fisher knows the seasons), sees what is at hand, and
plays by plain rules; it never reads a draw before it is made (a catch, a wreck, tomorrow's weather). Where its read is wider than
the engine's signs, it says so (`river_tonight`: the flow from the catchment's rain, where the signs show only local rain).

How a day is planned. Each person's plan is a list of acts; the engine plays everyone's first act, then everyone's second, and so
on, so a plan is written in phases by index: phase A (lifting what was caught, the catch into the house's store) for everyone,
then phase B (what is done with it: preserving at the racks, salting), each person's phase B starting after the longest phase A of
their household (padded with `rest`, which costs nothing). Every person of a household computes the same household plan from the
same morning state and takes their own part (roles by rank: the head is the household's keeper), so no message is needed. Units
left go to wild food where a gather is worth its work, else are rested (work costs food: labour.work_need).

The rules shared by every livelihood (`_common`): the catch and hand food moved into the house's store (the night eats the most
perishable first: night.eat_order), firewood kept for the hearth and the smoke, the children set to gather firewood, wild food
worth the work with what is left. A livelihood adds its own acts: `runs` (the river's runs: traps in the water, nets, the weir and its gap,
smoking, drying at the hearth, salting, boiling salt, mending the weir).

Adding a livelihood (farming, herding, hunting with trips to wild nodes, gathering, foraging): write a function
`(view: Day) -> Plan` that adds its phase A and phase B acts and its fallback, with its knobs in KNOBS, and register it with
`@policy("<name>")`; a run selects it with `--bots <name>`. The Day view (the household, its store and fittings, the
calendar) and `_common` (food into store, firewood, children, wild food) are shared. A trip away (hunting at a wild node, droving)
is a `travel` act at the end of a plan, after the day's work at home, as run.bot_plan's own travel; the policy keeps its own
schedule by the calendar, so a bot needs no memory beyond the state.
"""
from __future__ import annotations

import math

from cybertron2.engine.data import EDIBLE, ITEMS, RESOURCES, TECHNIQUES, WATER_WORKS

WATER_WORKS_UNITS = WATER_WORKS["weir"]["units"]                     # a gap shut (2 units) or opened (1)

POLICIES = {}
KNOBS = {}
# rules shared by every livelihood (calibrate): a person's ration in food, kept in hand from the catch; firewood a hearth burns on
# a normal night and a cold one, the nights of it a household keeps in store, the least it keeps; firewood a unit of gathering;
# the children's standing work; the least food a gather of wild food must look to give to be worth its work
COMMON = {"ration": 1.3, "hearth_fuel": 1.0, "hearth_fuel_cold": 4.0, "fuel_nights": 6, "fuel_least": 15, "wood_a_unit": 3.0,
          "children": "firewood", "forage_least": 0.12}
FOODS = tuple(sorted(i for i in EDIBLE))


def policy(name, **knobs):
    """Register a livelihood policy under `name`, with its knobs' defaults."""
    def reg(fn):
        POLICIES[name] = fn
        KNOBS[name] = dict(knobs)
        return fn
    return reg


def setting(w) -> dict | None:
    """The world's `bot_livelihood`, as {"policy": name, ...knobs} with the policy's defaults; None when it has none."""
    x = (getattr(w, "spec", None) or {}).get("bot_livelihood")
    if not x:
        return None
    s = {"policy": str(x)} if isinstance(x, str) else dict(x)
    if s.get("policy") not in POLICIES:
        raise ValueError(f"bot_livelihood: no policy {s.get('policy')!r} (policies: {', '.join(sorted(POLICIES))})")
    return {**COMMON, **KNOBS[s["policy"]], **s}


def check(name: str) -> str:
    """A policy's name as `--bots` gives it, checked."""
    if name not in POLICIES:
        raise SystemExit(f"--bots {name}: no livelihood policy of that name (policies: {', '.join(sorted(POLICIES))})")
    return name


def on(w) -> bool:
    return setting(w) is not None


def plan(w, name, talk=None, kind="decision") -> dict:
    """A person's answer: the day's plan in the morning, nothing at the evening's hearth or in talk (bots do not talk)."""
    if kind != "decision":
        return {"why": "bot", "actions": []}
    s = setting(w)
    day = Day(w, name, s)
    p = Plan(day)
    _common_a(day, p)
    POLICIES[s["policy"]](day, p)
    _common_b(day, p)
    return p.answer()


# ---------------------------------------------------------------------- the day's view
class Day:
    """What a person of a household sees this morning, read once from the state (nothing is written)."""

    def __init__(self, w, name, s):
        from cybertron2.engine.here import Here, Mind
        self.w, self.name, self.s = w, name, s
        self.here, self.mind = Here(w, name), Mind(w, name)
        self.node = w.at(name)
        self.hh = w.household_of(name)
        acting = set(w.agents_acting())
        mem = [m for m in (w.members(self.hh) if self.hh else [name]) if m in acting and w.at(m) == self.node]
        head = w.head(self.hh) if self.hh else None
        self.members = sorted(mem, key=lambda m: (m != head, w.s["people"][m]["stage"] != "adult", m))
        self.role = self.members.index(name) if name in self.members else 0
        self.home = next(iter(w.dwellings(name)), None)
        self.home_b = w.s["buildings"].get(self.home) if self.home else None
        cal = w.calendar()
        self.season, self.cold = cal["season"], w.cold(self.node)
        self.units = {m: int(w.units_for(m)) for m in self.members}

    # the household's house and store
    def store(self) -> dict:
        return dict(self.w.goods(self.home_b["stock"])) if self.home_b else {}

    def reach(self, item) -> float:
        """What of an item a person can draw on here: hands and the stores they may take from."""
        return sum(float(self.w.goods(c).get(item, 0.0)) for c in self.w.takeable(self.name, self.node))

    def fits(self, f) -> int:
        return int(((self.home_b or {}).get("fittings") or {}).get(f) or 0)

    def smokehouse(self):
        """The household's smoke racks here: its smokehouse, a building of its own apart from the houses (brief 5 §4a), else racks
        in the house itself (an older world); None without."""
        from cybertron2.engine import process as PROC
        own = [b for b in self.w.homes(self.name) if self.w.s["buildings"][b]["node"] == self.node
               and PROC.is_smokehouse(self.w.s["buildings"][b])]
        return sorted(own, key=lambda b: (b == self.home, b))[0] if own else None

    def knows(self, tech, who=None) -> bool:
        k = ((self.w.s["know"].get(who or self.name) or {}).get(tech) or {})
        if k:
            return k.get("level") not in (None, "aware")
        return bool(TECHNIQUES.get(tech, {}).get("basic"))

    def parcels(self, covers) -> list:
        return sorted(pid for pid, p in self.here.parcels().items() if p["cover"] in covers)

    def pname(self, pid) -> str:
        return self.w.s["parcels"][pid]["name"]

    def bname(self, bid) -> str:
        return self.w.s["buildings"][bid]["name"]

    def hearth_fuel(self) -> float:
        n = self.fits("hearth")
        return n * float(self.s["hearth_fuel_cold"] if self.season == "winter" or self.cold else self.s["hearth_fuel"])

    def ration(self, who) -> float:
        st = self.w.s["people"][who]["stage"]
        return float(self.s["ration"]) * (0.6 if st == "youth" else 1.0)


class Plan:
    """A person's plan in phases: `a` (lifts and stores, first), `b` (after the household's longest phase a), `fallback`."""

    def __init__(self, day):
        self.day = day
        self.a, self.b, self.fallback = [], [], []
        self.reserve = 0                                  # units left unplanned for the household's chores (u6 §5)
        self.a_len = {}                                   # phase a's length for each member of the household (to align b)
        self.cost = 0
        self.made = {}                                    # gear made earlier in the plan, to be laid later in it

    def left(self) -> int:
        return self.day.units[self.day.name] - self.cost - self.reserve

    def add(self, phase, act, units=0) -> bool:
        if units and self.cost + units > self.day.units[self.day.name] - (self.reserve if phase == "b" else 0):
            return False
        getattr(self, phase).append(act)
        self.cost += units
        return True

    def answer(self) -> dict:
        start = max([len(self.a)] + list(self.a_len.values()))
        acts = self.a + [{"do": "rest"}] * (start - len(self.a)) + self.b if self.b else list(self.a)
        if len(acts) > 10:                                # run.MAX_ACTIONS: the padding goes first
            acts = [x for x in acts if x.get("do") != "rest"][:10]
        return {"why": "bot", "actions": acts, "attend": "the place in general", "say": [], "fallback": self.fallback[:3]}


# ---------------------------------------------------------------------- the rules every livelihood shares
def _common_a(day, p) -> None:
    """The head sets the children to a standing work (the head's order, D2-148)."""
    w = day.w
    if day.role == 0 and day.hh and w.s["people"][day.name]["stage"] == "adult":
        order = (w.s["institutions"].get(day.hh) or {}).get("order")
        want = day.s.get("children")
        if want and (not order or order.get("what") != want) and any(
                w.s["people"][m]["stage"] == "child" and w.s["people"][m]["alive"] for m in w.members(day.hh)):
            p.add("a", {"do": "order", "what": want})


def _store_moves(day, who, coming: dict, keep: float = 0.0) -> list:
    """Into the house's store: the food in a person's hands and what their lifts bring (`coming`), less `keep` of fish left in hand
    for their own supper; firewood and salt in hand too. Moving costs nothing (verbs.VERB move)."""
    if not day.home_b:
        return []
    hands = {i: float(q) for i, q in day.w.goods(day.w.hands(who)).items()}
    for i, q in coming.items():
        hands[i] = hands.get(i, 0.0) + float(q)
    out = []
    for item in sorted(hands):
        q = hands[item] - (keep if item == "fish" else 0.0)
        if q > 1e-6 and (item in EDIBLE or item in ("firewood", "salt")):
            out.append({"do": "move", "item": item, "qty": round(q + 1e-4, 4), "to": "store", "at": day.bname(day.home)})
    return out


def _firewood_need(day) -> float:
    """Firewood the household wants in store: its hearths' nights (cold nights burn four times as much) and a smoke fire's."""
    nights = float(day.s["fuel_nights"])
    smoke = 1.0 if day.smokehouse() else 0.0                               # carried to a smokehouse apart (the book's rule 4)
    return max(float(day.s["fuel_least"]), nights * (day.hearth_fuel() + smoke))


def _wood_units(day) -> int:
    """Units of gathering firewood the household wants today (one person's share), from its store's shortfall."""
    have = float(day.store().get("firewood", 0.0))
    short = _firewood_need(day) - have
    return 0 if short <= 0 else min(4, math.ceil(short / float(day.s["wood_a_unit"])))


def _gather_wood(day, p, units) -> None:
    """Firewood: cut young growth with a tool in hand (5 a unit), else dead wood by hand (3 a unit), at the richest wood; then into
    the store (that move is in phase b, after the gathering)."""
    if units <= 0 or not day.home_b:
        return
    tool = day.here.carried().get("crude tool", 0.0) >= 1
    tech = "cut" if tool and day.knows("cut") else "firewood"
    key = "young" if tech == "cut" else "dead"
    ps = [pid for pid in day.parcels(TECHNIQUES[tech]["at"]["covers"]) if float((day.w.s["parcels"][pid]["res"].get(key) or {}).get("S", 0)) > 5]
    if not ps:
        return
    pid = max(ps, key=lambda q: (float(day.w.s["parcels"][q]["res"][key]["S"]), q))
    n = 0
    for _ in range(units):
        if p.add("b", {"do": "gather", "what": tech, "at": day.pname(pid)}, 1):
            n += 1
    if n:
        p.add("b", {"do": "move", "item": "firewood", "qty": 999, "to": "store", "at": day.bname(day.home)})


def _forage_plan(day, units) -> list:
    """Wild food near home worth the work: up to `units` gathers, each at the parcel whose next gather looks best, looking for the
    plant there that gives the most food, while a gather looks to give at least `forage_least` in food (a unit's work costs about
    0.04 in food tonight, labour.work_need, so scraping a bare common is worse than resting). What one sees standing is read as
    wild.forage takes it (half of what stands at most, more where it stands thick), its own gathers drawing it down; the household's
    members start at different parcels of the best few, so they spread. [(act, food it looks to give)]."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import plants as PL
    t = TECHNIQUES.get("gather wild food") or {}
    if units <= 0 or not t or not day.knows("gather wild food"):
        return []
    floor = float(day.here.p["refuge"])
    base = float((t.get("yield") or {}).get("base", 1.2))
    stands = {}
    for pid in day.parcels((t.get("at") or {}).get("covers") or []):
        if not WL.in_season(day.here, pid):
            continue
        res = day.w.s["parcels"][pid]["res"]
        kinds = {k: r for k, r in sorted(res.items()) if (RESOURCES.get(k) or {}).get("plant") and k in PL.PLANTS}
        avail = {k: max(0.0, float(r.get("S", 0.0)) - floor * float(r.get("K", 0.0)) * float((r.get("seasons") or {}).get(day.season, 0.0)))
                 for k, r in kinds.items()}
        budget = sum(float(r.get("K", 0.0)) * PL.mean_season(k) for k, r in kinds.items())
        if sum(avail.values()) > 1e-6 and budget > 1e-9:
            stands[pid] = (avail, budget)

    def gather(avail, budget, want):
        total = sum(avail.values())
        if total <= 1e-6:
            return 0.0, {}
        q = min(0.5 * total, base * min(1.5, total / budget))
        wt = {k: v * float(PL.PLANTS[k]["ease"]) * ((3.0 if k == want else 0.4) if want else 1.0) for k, v in avail.items()}
        tw = sum(wt.values()) or 1.0
        take = {k: min(avail[k], q * v / tw) for k, v in wt.items()}
        return sum(x * float((ITEMS.get(PL.PLANTS[k]["item"]) or {}).get("food", 0.0)) for k, x in take.items()), take

    def best(pid):
        avail, budget = stands[pid]
        opts = [(gather(avail, budget, k), k) for k in sorted(avail) if avail[k] > 1e-6]
        return max(opts, key=lambda x: (x[0][0], x[1])) if opts else ((0.0, {}), None)

    order = sorted(stands, key=lambda q: (-best(q)[0][0], q))[:4]
    hh = sorted(day.here.households()).index(day.hh) if day.hh in day.here.households() else 0
    k0 = (day.role + hh) % len(order) if order else 0
    order = order[k0:] + order[:k0]
    out = []
    for _ in range(units):
        if not order:
            break
        pid = max(order, key=lambda q: (best(q)[0][0] * (1.15 if q == order[0] else 1.0), q))   # one's own start a little first
        (food, take), want = best(pid)
        if food < float(day.s["forage_least"]):
            break
        for k, x in take.items():
            stands[pid][0][k] = max(0.0, stands[pid][0][k] - x)
        act = {"do": "gather", "what": "gather wild food", "at": day.pname(pid)}
        if want:
            act["looking for"] = PL.PLANTS[want]["item"]
        out.append((act, food))
    return out


def _common_b(day, p) -> None:
    """Units left: wild food near home where a gather is worth its work (`_forage_plan`); else rest, which costs no food (with the
    knob `fallback: hunt`, hunting the woods near home first: a reading of what the land's game gives, not the runs livelihood)."""
    if day.s.get("fallback") == "hunt" and day.knows("hunt the wild"):
        ps = day.parcels(TECHNIQUES["hunt the wild"]["at"]["covers"])
        if ps:
            p.fallback.append({"do": "gather", "what": "hunt the wild", "at": day.pname(ps[(day.role + len(day.name)) % len(ps)])})
    for act, _ in _forage_plan(day, p.left()):
        p.add("b", act, 1)


# ---------------------------------------------------------------------- the runs (fishing the river)
def _runners(day) -> dict:
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU
    if not WL.on(day.w) or not (day.w.s.get("wild") or {}).get("state"):
        return {}
    m = WL.model(day.w)
    return RU.runners(m.kinds) if RU.on_river(m, day.node) else {}


def run_season(day, ahead=1) -> list:
    """The kinds whose run window is open today or within `ahead` days (what a fisher knows of the year: D2-231's set nights fall
    inside the windows)."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU
    out = []
    m = WL.model(day.w)
    d = WL.eco_day(day.w)
    for k, r in _runners(day).items():
        if any(RU._window(m, d + j, r["seasons"])[0] for j in range(ahead + 1)):
            out.append(k)
    return out


def _shoals(day) -> list:
    """The running kinds a net takes (a shoal: wild.methods `net` needs a flock)."""
    from cybertron2.wild.kinds import TRAITS
    return [k for k in _runners(day) if (TRAITS.get(k) or {}).get("social") == "flock"]


RUN_SEEN = 3.0                                    # a run at the water is seen at 3 heads or more (signs._wild_river: "a few fish are no run")


def run_here(day) -> dict:
    """The run at the village's water today and tonight, {kind: heads}, as its sign shows it (signs._wild_river, brief 5 §3.5): only a
    kind there in 3 heads or more. A pulse at the village at dawn stays through the night (wild/runs.py), so a fisher who sees the
    run at the water in the morning knows it is there tonight."""
    from cybertron2.engine import wild as WL
    from cybertron2.wild import runs as RU
    if not _runners(day):
        return {}
    st = day.w.s["wild"]["state"]
    out = {}
    for pl in RU.today(WL.model(day.w), st, WL.eco_day(day.w)):
        if pl["g"] == f"v:{day.node}":
            out[pl["k"]] = out.get(pl["k"], 0.0) + float(pl["n"])
    return {k: n for k, n in out.items() if n >= RUN_SEEN}


def river_tonight(day) -> str:
    """How high the river runs tonight at the village (low, normal, high, spate, flood): what one sees of it rising through the day,
    from the catchment's rain today and yesterday (as wild._runs_night reads it)."""
    from cybertron2.engine import wild as WL
    from cybertron2.engine.data import WATER_WORKS
    from cybertron2.wild import runs as RU
    if not _runners(day):
        return "normal"
    m = WL.model(day.w)
    st = day.w.s["wild"]["state"]
    nodes = sorted(set(m.nodes))
    wx = WL.weather(day.w, nodes, day.w.d)
    rain = (st.get("runs") or {}).get("rain") or {}
    mem = {nd: [float((wx.get(nd) or {}).get("rain", 0.0))] + list(rain.get(nd) or []) for nd in sorted(set(nodes) | set(rain))}
    return RU.flow(RU.net(m), f"v:{day.node}", mem, WATER_WORKS["weir"]["wear"]["flow_at"])


def spate(day) -> bool:
    """The river in spate or flood tonight: traps set in it are likely wrecked, and a weir with its gap shut wears the faster."""
    return river_tonight(day) in ("spate", "flood")


def river_parcels(day) -> list:
    from cybertron2.engine import wild as WL
    return [pid for pid in sorted(day.here.parcels()) if WL._river_parcel(day.w, pid)]


def traps(day, who=None, live=False) -> list:
    """A person's traps in the water here (not a weir's), [(cid, thing)]; `live`: those still fishing tonight (placed gear: with a
    sound piece standing, u2 §3; an older world's set: within its life)."""
    from cybertron2.engine import gear as GE
    who = who or day.name
    out = []
    for cid, c in sorted(day.w.s["containers"].items()):
        sp = c.get("set") or {}
        if c.get("kind") != "set" or c.get("by") != who or c.get("node") != day.node or sp.get("method") != "trap in water" or sp.get("weir"):
            continue
        if live and (sp.get("sprung") is not None or sp.get("state") in ("up", "spent") or GE.fishing(c) <= 0
                     or ("gear" not in sp and day.w.d - int(sp["set_day"]) >= int(sp.get("life", 8)))):
            continue
        out.append((cid, c))
    return out


def traps_standing(day, who=None) -> int:
    """The sound wicker traps a person has standing in the water here."""
    from cybertron2.engine import gear as GE
    return sum(GE.fishing(c) for _, c in traps(day, who, live=True))


def known_sets(day, who) -> list:
    """The set things here a person may lift without robbing anyone: their own, and a weir's they know of. [(cid, thing)]."""
    from cybertron2.engine import things as TH
    known = TH.known_here(day.w, who, day.node)
    out = []
    for cid, c in sorted(day.w.s["containers"].items()):
        if c.get("kind") != "set" or c.get("node") != day.node:
            continue
        if c.get("by") == who or (TH.is_weir(c) and cid in known and (TH.owns_set(c, who) or not c.get("by"))):
            out.append((cid, c))
        elif not TH.is_weir(c) and c.get("household") and TH.owns_set(c, who, day.w) and c.get("by") not in day.members \
                and who == next((m for m in day.members if TH.owns_set(c, m, day.w)), None):
            out.append((cid, c))                                               # the household's, its setter gone: tended by the first
                                                                               # of the household here (D2-305)
    return out


def _lifts(day, who) -> list:
    """The takes that lift a person's catch this morning: one for each set thing and food item in it, named by its tag where the
    world has tags (so it is that thing, not a neighbour's at the same place); a weir's traps by the first of the household who
    knows them. [(act, item, qty)]."""
    from cybertron2.engine import gear as GE, tags as TG, things as TH
    out = []
    before = day.members[:day.members.index(who)] if who in day.members else []
    for cid, c in known_sets(day, who):
        if TH.is_weir(c) and any(c.get("by") != m and cid in TH.known_here(day.w, m, day.node) for m in before):
            continue
        sp = c.get("set") or {}
        if "gear" in sp and not TH.is_weir(c):                                  # placed gear: tended, one act for all it holds, the
            if sp.get("state") == "up":                                         # broken brought home, the rest set again (u2 §3)
                continue
            q = sum(float(x) for i, x in c["goods"].items() if i in EDIBLE)
            fresh = sp.get("state") == "spent" and int(sp.get("tended", -1)) < int(sp.get("sprung", -1) or -1)
            if q > 1e-6 or fresh or any(not GE.sound(x) for x in GE.laid_pieces(c, "wicker trap")):
                act = {"do": "tend", "thing": c["tag"]} if TG.on(day.w) and c.get("tag") else \
                    {"do": "tend", "what": "wicker traps", "at": day.pname(c["parcel"])}
                out.append((act, "fish", q))
            continue
        for item, q in sorted(c["goods"].items()):
            if float(q) > 1e-6 and item in EDIBLE:
                src = c["tag"] if TG.on(day.w) and c.get("tag") else f"the traps at {day.pname(c['parcel'])}"
                out.append(({"do": "take", "item": item, "from": src}, item, float(q)))
    return out


def _pan(day):
    """A brine pan in a building of the household's own (its salt house), or None."""
    return next((bid for bid in day.w.homes(day.name) if (day.w.s["buildings"][bid].get("fittings") or {}).get("brine pan")
                 and day.w.s["buildings"][bid]["node"] == day.node), None)


def _weir(day, who=None):
    """The finished weir at the village's water whose gap a person may set (its holder's head manages it), or (None, None)."""
    from cybertron2.engine import wild as WL
    for bid, b in WL.weirs(day.w, day.node):
        if "management" in day.here.rights(("building", bid), who or day.name):
            return bid, b
    return None, None


def _weir_search(day, who):
    """A lift of the weir's traps by the one who manages it but has not found them yet (a weir whose crew is no one knows no traps):
    a take of fish from its water, which looks the place over (things.search). Returns (act, qty) or None."""
    from cybertron2.engine import things as TH, wild as WL
    bid, b = _weir(day, who)
    if bid is None:
        return None
    cid = WL.weir_trap(day.w, bid)
    if cid is None or cid in TH.known_here(day.w, who, day.node):
        return None
    q = float(day.w.s["containers"][cid]["goods"].get("fish", 0.0))
    return ({"do": "take", "item": "fish", "from": day.pname(b["parcel"])}, q) if q > 1e-6 else None


def phase_a(day, who, search_at=0) -> tuple:
    """A member's morning: their lifts, the weir looked for (after everyone's lifts, at `search_at`, so no one else's traps are
    found full), then the catch into the store, their own supper of fish kept in hand (the keeper keeps none: the store feeds
    them). Returns (acts, {item: qty brought in to the store}, units, fish kept in hand)."""
    acts, coming = [], {}
    for act, item, q in _lifts(day, who):
        acts.append(act)
        coming[item] = coming.get(item, 0.0) + q
    units = len(acts)
    sr = _weir_search(day, who)
    if sr:
        acts += [{"do": "rest"}] * max(0, search_at - len(acts)) + [sr[0]]
        coming["fish"] = coming.get("fish", 0.0) + sr[1]
        units += 1
    keep = 0.0 if who == day.members[0] else min(coming.get("fish", 0.0), day.ration(who))
    acts += _store_moves(day, who, coming, keep)
    return acts, {i: q - (keep if i == "fish" else 0.0) for i, q in coming.items()}, units, keep


# the runs' knobs (calibrate): traps kept in the water by each fisher and by the keeper; the least surplus worth a batch at the smoke
# racks, at a hearth's rack, in the salt tub; the salt a household keeps before it boils more, and the firewood it must have to;
# nets on a shoal's night; the weir's gap worked; a member's most mends a day; traps out of the windows; the river's heights no trap
# is set into (none: the eels run on the rain, and in the measured runs traps set into spates and floods still paid, W-69); the traps
# each fisher of a household that holds a weir keeps (its keeper none): since the gear shares a run (wild/gear.py, 20 Nov) the weir
# takes its share whatever the traps beside it, and its lift is one act for its whole catch where each trap's is an act for a kg or
# two, so the weir's household keeps its work for keeping the catch (measured: with 8 traps a fisher its members spent whole days
# lifting traps and its keeper had no units left to salt)
@policy("runs", traps=8, keeper_traps=3, weir_traps=2, smoke_least=6.0, dry_least=3.0, salt_least=4.0, salt_keep=8.0, boil_wood=12.0, net=True,
        gap=True, mend_most=2, off_season_traps=0, trap_stop=(), smoke_fuel_nights=3)
def runs(day, p) -> None:
    """Fishing the river's runs (W-69). The run windows are the fisher's year; the run at the water and the river's height are read
    each morning (their signs); the weir is the household's main gear where it has one.
      - phase a (everyone): the traps and the weir's traps lifted, the catch into the house's store, a supper kept in hand;
      - the weir's household: the gap shut whenever a run is at the water, and through the windows while the river is not high;
        opened only on a high night with no run at the water, and outside the windows; the weir mended a level an act (2 units, a
        timber) on any night the river is not in spate, its members first and the keeper after, at most `mend_most` acts each;
      - the keeper (the head): the surplus over tonight's suppers smoked at the house's racks (the fire tended while a batch hangs),
        dried at the hearth, salted with salt to hand; salt boiled at the household's pan when it runs low; their own few traps;
      - the others: a net on a night a shoal is at the water; traps in the river through the windows (`traps` each, `keeper_traps`
        the keeper's; in the weir's household `weir_traps` each and none the keeper's), set whatever the river (a spate smashes half of them, a flood most, but the run comes with the water);
        the first of them firewood when the store is short;
      - then wild food where it is worth the work (`_common_b`), else rest."""
    season = run_season(day)
    run = run_here(day)
    flow = river_tonight(day)
    # phase a: everyone's lifts, the weir's looked for after them all, the catch into the store
    search_at = max([0] + [len(_lifts(day, m)) for m in day.w.agents_acting() if day.w.at(m) == day.node])
    coming_all, kept = {}, 0.0
    for m in day.members:
        acts, coming, units, keep = phase_a(day, m, search_at)
        p.a_len[m] = len(acts)
        kept += keep
        for i, q in coming.items():
            coming_all[i] = coming_all.get(i, 0.0) + q
        if m == day.name:
            for act in acts:
                p.add("a", act, 1 if act.get("do") in ("take", "tend") else 0)
    # phase b
    if day.role == 0:
        _gap(day, p, season, run, flow)
    _mend_weir(day, p, flow)
    if day.role == 0:
        _keeper(day, p, coming_all, season, flow, max(0.0, _suppers(day) - kept))
    else:
        _fisher(day, p, season, run, flow)


def high_water(flow) -> bool:
    return flow in ("high", "spate", "flood")


def _gap(day, p, season, run, flow) -> None:
    """The weir's gap, by its holder's head: shut when a run is at the water today (the weir takes a share of every run passing,
    a tenth of it with the gap open), and through a window while the river is not high; opened on a high night with no run at the
    water (a shut gap in high water wears the weir half as fast again, D2-210) and outside the windows."""
    from cybertron2.engine import wild as WL
    bid, b = _weir(day)
    if bid is None or not day.s.get("gap"):
        return
    if run:
        want = "shut"
    elif high_water(flow) or not season:
        want = "open"
    else:
        want = "shut"
    if WL.gap(b) != want:
        p.add("b", {"do": "set", "thing": "gap", "to": want, "at": day.bname(bid)}, int(WATER_WORKS_UNITS[want]))


def _suppers(day) -> float:
    """What the household eats tonight: `ration` (a ration and a working day's share) for each living member, an infant's and a
    child's less (life.ration_factor)."""
    from cybertron2.engine import life as LF
    out = 0.0
    for m in (day.w.members(day.hh) if day.hh else [day.name]):
        if day.w.s["people"][m].get("alive", True):
            mult, extra = LF.ration_factor(day.w, m)
            out += float(day.s["ration"]) * float(mult) + float(extra)
    return out


def _keeper(day, p, coming, season, flow, supper) -> None:
    """The head: the household's keeping is set in its book (u6; `_book`): fish that comes in is hung on the smokehouse's racks while
    they have room, the rest salted while there is salt; the fire tended while anything is smoking; a done lot taken down into the
    house; firewood carried to the smokehouse when it runs low. The spare-units phase does that work after everyone's plans, so the
    keeper leaves units unplanned for it (`reserve`). By hand still: drying at the hearth, boiling salt at the household's pan, a few
    traps of their own, firewood alone."""
    s, w = day.s, day.w
    fish = float(day.store().get("fish", 0.0)) + float(day.here.carried().get("fish", 0.0)) + float(coming.get("fish", 0.0))
    meat = float(day.store().get("meat", 0.0)) + float(day.here.carried().get("meat", 0.0)) + float(coming.get("meat", 0.0))
    fish -= supper
    if day.home_b:
        from cybertron2.engine import process as PROC
        home = day.home
        sh = day.smokehouse()
        _book(day, p, sh)
        work = 0.0
        if sh:
            room = PROC.room(w, sh, "keeping smoke")
            hang = min(max(0.0, fish), room)
            work += hang / 30.0 + (1.0 if hang > 1e-6 or PROC.lots(w, sh, done=False) else 0.0)
            work += sum(PROC.done_kg(c) for c in PROC.lots(w, sh, done=True).values()) / 120.0
            fish -= hang
        salt = day.reach("salt")
        if fish >= float(s["salt_least"]) and salt >= 1:
            work += min(fish, salt * 4) / 40.0
            fish -= min(fish, salt * 4)
        p.reserve = int(math.ceil(work - 1e-9))
        if day.fits("hearth"):
            room = PROC.room(w, home, "hearth rack")
            if fish >= float(s["dry_least"]) and room >= float(s["dry_least"]) and day.knows("dry fish"):
                p.add("b", {"do": "make", "what": "dry fish"}, 1)
                fish -= min(fish, room)
            elif meat >= float(s["dry_least"]) and room >= float(s["dry_least"]) and day.knows("dry meat"):
                p.add("b", {"do": "make", "what": "dry meat"}, 1)
        if (season or fish > 0) and _pan(day) and day.knows("boil salt") and salt < float(s["salt_keep"]) \
                and day.reach("firewood") >= float(s["boil_wood"]):
            p.add("b", {"do": "make", "what": "boil salt"}, 1)               # salt for the run's surplus, at the household's pan
            p.add("b", {"do": "move", "item": "salt", "qty": 999, "to": "store", "at": day.bname(home)})
    _set_traps(day, p, season, 0 if _weir(day, day.members[0])[0] else int(s["keeper_traps"]), flow)
    if len(day.members) == 1:
        _gather_wood(day, p, _wood_units(day))


KEPT = ("smoked fish", "smoked meat")


def book_rules(day, sh) -> list:
    """The keeper's household rules (u6 §10's worked sentences, as the bot keeps them); each rule's words are its key."""
    house = day.bname(day.home)
    out = []
    if sh:
        hut = day.bname(sh)
        out += [{"rule": "go", "goods": "fish", "to": f"the racks in {hut}", "when": f"the racks in {hut} have room",
                 "words": f"fish that comes in goes to the racks in {hut} when they have room"},
                {"rule": "tend", "at": hut, "when": "while anything is smoking", "words": f"keep the fire in {hut} going while anything hangs"},
                {"rule": "move", "goods": "smoked fish", "from": f"the racks in {hut}", "to": house, "when": "a lot is done",
                 "words": f"when the fish are smoked, take them down into {house}"},
                {"rule": "move", "goods": "firewood", "from": house, "to": hut, "qty": 25, "when": f"{hut} holds under 15",
                 "words": f"carry firewood to {hut} when it runs low"}]
    if day.knows("salt fish"):
        out.append({"rule": "go", "goods": "fish", "to": "the salting tub", "when": f"the racks in {day.bname(sh)} are full" if sh else None,
                    "words": "salt the fish the racks have no room for, while there is salt"})
    return [{k: v for k, v in r.items() if v is not None} for r in out]


def _book(day, p, sh) -> None:
    """The head sets the household's rules once (a free act, u6 §2); a rule already in the book with the same words is left alone."""
    from cybertron2.engine import book as BK
    if day.role != 0 or not day.hh or day.w.head(day.hh) != day.name:
        return
    have = {r.get("words") for r in BK.household_rules(day.w, day.hh)}
    for r in book_rules(day, sh):
        if r["words"] not in have:
            p.add("a", {"do": "rule", "for": "household", **r}, 0)


def _fisher(day, p, season, run, flow) -> None:
    """Another member: a net when a shoal is at the water, traps through the windows, firewood when the store is short (the first of
    them who is not the head)."""
    s = day.s
    if s.get("net") and day.knows("net") and any(k in run for k in _shoals(day)):
        for pid in river_parcels(day)[:1]:
            p.add("b", {"do": "gather", "what": "net", "at": day.pname(pid)}, 2)
    _set_traps(day, p, season, int(s["weir_traps"] if _weir(day, day.members[0])[0] else s["traps"]), flow)
    _set_net(day, p, season, flow)
    if day.role == 1:
        _gather_wood(day, p, _wood_units(day))


def _set_net(day, p, season, flow) -> None:
    """A gill net held is set in the river's water while a run's window is open and the river is not in flood (a flood tears it,
    u2 §4.4); tended with the traps (`_lifts`)."""
    if not season or flow == "flood" or not day.knows("gill net") or day.here.sound_held("gill net") <= 0:
        return
    ps = river_parcels(day)
    if ps:
        p.add("b", {"do": "set", "what": "gill net", "at": day.pname(ps[0])}, 1)


def _mend_weir(day, p, flow) -> None:
    """The weir mended, a level of its worst section an act (2 units and a timber, verbs._weir_mend), by the household that holds it,
    on any night the river is not in spate or flood (a mend torn out tonight is work lost): the members after the head first, then
    the head, at most `mend_most` acts each, until it is sound or the timber to hand runs out. Every member reckons the same split."""
    from cybertron2.engine import wild as WL
    bid, b = _weir(day, day.members[0])
    if bid is None or flow in ("spate", "flood"):
        return
    short = sum(5 - int(sc["level"]) for sc in WL.sections(b))
    short = min(short, int(day.reach("timber")) + (1 if b.get("mending") else 0))
    if short <= 0:
        return
    most = int(day.s["mend_most"])
    order = [m for m in day.members[1:] if day.w.s["people"][m]["stage"] in ("adult", "youth")] + day.members[:1]
    mine = 0
    for m in order:
        n = min(most, short, day.units[m] // 2)
        if m == day.name:
            mine = n
        short -= n
    for _ in range(mine):
        if not p.add("b", {"do": "work", "what": "repair", "at": day.bname(bid)}, 2):
            break


def _set_traps(day, p, season, want, flow) -> None:
    """Traps kept in the river's water through the windows (and the day before), `want` a person, spread over its river parcels; none
    set on a night the river runs as `trap_stop` says (a spate smashes half the traps in the river with their catch, a flood most:
    WATER_WORKS trap wreck; but the eels run on the rain, so a trap set into the rising water still fishes the run: by default
    they are set whatever the river). Traps are laid from the hands, up to six a setting (u2 §3; fault 12); short of them, the
    fisher mends the broken, makes more from withies, and cuts withies (`_trap_gear`)."""
    if not day.knows("trap in water"):
        return
    want = want if season else int(day.s.get("off_season_traps") or 0)
    if want <= 0:
        return
    _trap_gear(day, p, want, ahead=season or bool(run_season(day, ahead=3)))
    if flow in (day.s.get("trap_stop") or ()):
        return
    have = traps_standing(day)
    held = day.here.sound_held("wicker trap") + p.made.get("wicker trap", 0)
    ps = river_parcels(day)
    j = 0
    while have < want and held > 0 and ps:
        n = min(6, want - have, held)
        if not p.add("b", {"do": "set", "what": "wicker traps", "qty": n, "at": day.pname(ps[j % len(ps)])}, 1):
            break
        have += n
        held -= n
        j += 1


def _trap_gear(day, p, want, ahead=True) -> None:
    """A fisher's traps kept in repair (u3 §3.4) and made (u3 §2.2): the broken in hand mended when withies are to hand; more traps
    made, up to the batch a unit, while those standing and in hand fall short of `want` and the run is near; withies cut on the
    willow when short (wild/willow.py), else from young growth."""
    from cybertron2.engine import gear as GE
    hands = day.w.s["containers"][day.here.hands]
    broken = sum(1 for x in GE.pieces(hands, "wicker trap", day.w) if not GE.sound(x))
    withies = day.reach("withies")
    if broken and withies >= 0.05 * broken and day.knows("wicker trap"):
        p.add("b", {"do": "make", "what": "mend", "item": "wicker trap"}, 1)
        withies -= 0.045 * broken
    if not ahead or not day.knows("wicker trap"):
        return
    short = want - traps_standing(day) - day.here.sound_held("wicker trap") - broken
    if short <= 0:
        return
    from cybertron2.engine import clocks as CK
    batch = CK.batch_of(TECHNIQUES["wicker trap"], day.here)
    lvl = ((day.w.s["know"].get(day.name) or {}).get("wicker trap") or {}).get("level", "known")
    need = 0.45 * (1.7 if lvl == "rough" else 1.3 if lvl == "capable" else 1.0)
    k = int(min(short, batch, withies // need))
    if k >= 1:
        if p.add("b", {"do": "make", "what": "wicker trap", "qty": k}, 1):
            p.made["wicker trap"] = p.made.get("wicker trap", 0) + k
        return
    cut = _willow_parcel(day)
    if cut:
        p.add("b", {"do": "gather", "what": "cut withies", "at": day.pname(cut)}, 1)


def _willow_parcel(day):
    """The parcel here with the most willow to cut, else a wood or scrub with young growth."""
    best = sorted(((float(par["res"]["willow"]["S"]), pid) for pid, par in day.here.parcels().items() if "willow" in par["res"]
                   and float(par["res"]["willow"]["S"]) >= 1.0), reverse=True)
    if best:
        return best[0][1]
    young = sorted(((float(par["res"]["young"]["S"]), pid) for pid, par in day.here.parcels().items() if "young" in par["res"]
                    and par["cover"] in ("forest", "scrub") and float(par["res"]["young"]["S"]) >= 1.0), reverse=True)
    return young[0][1] if young else None
