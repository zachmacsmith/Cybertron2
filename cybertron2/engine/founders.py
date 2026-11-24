"""The founders' seeded lines (u9_people.md §5; D2-266, D2-268, D2-279, D2-308, D2-311, D2-319): templates by hand, each at most 40
words once filled, in the person's voice, filled from the world's state at world build; a condition drops a line where it would be
false or useless (never a stand-in); sets by role, band and age; the cap of 20 lines with its protected lines and its drop order; the
holdings' lines inside the budget, written with the livelihood they belong to (D2-311). The feature unit of the founders' knowledge
(D2-244): its data (`TEMPLATES`, `BUDGET`, `DROP`), its renderer (`render`) and its seeding (`seed_world`, called by
livelihoods.fill: the lines go to each founder's `kept` with their source, ordinary kept lines, droppable and passable: D2-268).

No line states a price, a yield a unit, the best number of traps, a run's date (the cue instead), what lies at an unexplored place or
a mechanic of an act (founders_knowledge Part 4.1); a line may give a scale and a season and may advise (questions B32). Keeping is
said in the world's own nights and seasons from the keeping curve read as a quarter lost (D2-289; B9-1).
"""
from __future__ import annotations

import re

CAP_LINES = 20                                    # B9-2; D2-308
CAP_WORDS = 800
LINE_WORDS = 40                                   # D2-266


def keep_words(nights) -> str:
    """B9-1: nights kept, in words (a season is 8 days, a year 32: D2-273)."""
    n = float(nights)
    for bound, words in ((2.5, "a night or two"), (5, "a few nights"), (10, "about a season"), (20, "two seasons"),
                         (28, "most of a year"), (40, "about a year")):
        if n <= bound:
            return words
    return "more than a year"


def _keep(good) -> str:
    from cybertron2.engine.data import KEEP_DAYS, keep_nights
    return keep_words(keep_nights(KEEP_DAYS[good]))


def _words(text) -> int:
    return len(str(text).split())


class Ctx:
    """What a template reads: the world as written, the person, their household's fill and the village."""

    def __init__(self, world, name, rep, hrep):
        self.world, self.name, self.rep, self.h = world, name, rep, hrep
        self.a = world["agents"][name]
        self.hh = self.a.get("household")
        self.node = next((nid for nid, n in world["nodes"].items() if nid == self.a.get("at") or True), None)
        self.node = self._home_node()
        self.parcels = (world["nodes"].get(self.node) or {}).get("parcels") or {}

    def _home_node(self):
        for b in self.world["buildings"].values():
            if b.get("household") == self.hh and (b.get("fittings") or {}).get("beds"):
                for nid, n in self.world["nodes"].items():
                    if b["parcel"] in (n.get("parcels") or {}):
                        return nid
        return next(iter(self.world["nodes"]))

    def water(self):
        ws = [(pid, p) for pid, p in self.parcels.items() if p["cover"] == "water"]
        ws.sort(key=lambda x: (-int(x[1].get("size", 1)), x[0]))
        return ws[0][1]["name"] if ws else None

    def village(self):
        return self.world["nodes"][self.node].get("name") or self.node

    def line_name(self, hh=None):
        """The household as the engine names it ("the Brooks": world.py), without its article."""
        hh = hh or self.hh
        return str((self.world.get("institutions") or {}).get(hh, {}).get("name") or f"{hh}s").removeprefix("the ")

    def members(self, hh=None):
        hh = hh or self.hh
        return [n for n, a in self.world["agents"].items() if a.get("household") == hh and a.get("alive", True) is not False]

    def house(self):
        return next((bid for bid, b in self.world["buildings"].items() if b.get("household") == self.hh and (b.get("fittings") or {}).get("beds")), None)

    def holdings(self, hh=None):
        hr = self.rep["households"].get(hh or self.hh) or {}
        return hr.get("holds") or {}, hr.get("keepers") or {}

    def ration(self, n):
        """D2-292 and D2-330 C6: an adult 1, a youth 0.8, an elder 0.8, a child by the dial (0.7 low), an infant 0.5."""
        from cybertron2.engine.data import LIFE
        st = self.world["agents"][n].get("stage")
        dial = (self.world.get("children") or {}).get("dial", "low")
        return {"infant": float(LIFE["infant"]["eats"]), "child": float(LIFE["dial"][dial]["child_eats"]), "youth": 0.8,
                "elder": 0.8}.get(st, 1.0)


# ---------------------------------------------------------------------- the templates (u9 §5.3 to §5.6)
def BS1(c):
    d = (c.world.get("calendar") or {}).get("season_days", 8)
    return (f"The year turns in four seasons of {d} days: spring, summer, autumn, winter. Summer days are longest for work, winter's "
            "shortest. What land and water give changes each season; one season's emptiness says nothing of the next.")


def _has_fields(c):
    return any(p["cover"] == "field" for p in c.parcels.values())


def _wolves(c):
    return any(k == "wolf" for k in ((c.world.get("wild") or {}).get("kinds") or []))


def BS2(c):
    t = ("Winter is the hungry time: " + ("the fields give nothing, " if _has_fields(c) else "") + "the wild little, a cold night "
         "burns about three times the fuel" + (", and wolves come to the herds" if _wolves(c) else "") + ". What a house eats and burns "
         "through winter must be in by autumn's end.")
    return t if _words(t) <= LINE_WORDS else t.replace(" through winter must", " must")   # both clauses held: within 40 (W-105)


def BS3(c):
    from cybertron2.engine.data import ITEMS
    raw = ITEMS["fish"]["raw"] / ITEMS["fish"]["food"]
    share = "half" if 0.4 <= raw < 0.67 else ("two thirds" if raw >= 0.67 else "a third")
    return (f"Fresh meat and fish go off in {_keep('fish')}, faster in the hand; dry grain and beans keep {_keep('grain')}. Dried, "
            f"smoked or salted, food keeps for seasons. Raw food feeds about {share} what cooked does.")


def BS4(c):
    return ("A wood, a water or a heath gives less the more it is worked, and comes back when it is rested; game grows wary where it is "
            "hunted. Young growth cut comes again; dead wood gathered does not.")


def BS5(c):
    n = len(c.members())
    days = (c.world.get("calendar") or {}).get("season_days", 8)
    m = round(sum(c.ration(x) for x in c.members()) * days)
    return (f"A grown person eats about one food a night, more after a hard day or a night in the cold. A household of {n} wants about "
            f"{m} food to see a winter through, and more if the frost comes early.")


def BS6(c):
    others = [hh for hh in c.rep["households"] if hh != c.hh]
    if not others:
        return None
    return ("Our household eats from one store and keeps one hearth. Other houses hold their own land, beasts and stores and live by other "
            "crafts than ours: what we lack, a neighbour may make, and what they lack, we may.")


def BS7(c):
    bits = ["Heavy rain raises the rivers and a flood carries off what is set in them"]
    if _has_fields(c):
        bits.append("a hard frost kills tender crops")
    if _wolves(c):
        bits.append("the bear and the wolf come to a kill left lying in the open")
    return "; ".join(bits) + "."


def BS8(c):
    return ("What I know of a craft I got by watching, by trying and failing, and by being taught; a day beside one who knows is worth "
            "many tries alone.")                                         # its passing-on half is HH10's (D2-340)


def BS9(c):
    return ("What is made wears: gear with use, fittings with work, houses with the weather. Mended in time it costs a little; left, it "
            "costs the whole.")


def _tree(c, n):
    return next((t for t in c.world.get("tree") or [] if t.get("name") == n), {})


def PE1(c):
    t = _tree(c, c.name)
    if t.get("origin") and t.get("partner"):
        return f"I came to {c.village()} from {t['origin']} when I married {t['partner']}."
    founding = next((h for h in c.world.get("history") or [] if c.name in (h.get("who") or []) and "came to" in h.get("text", "")), None)
    if founding:
        who = founding["who"]
        line = c.line_name()
        if c.name in who:
            return f"Our line's founders, {who[0]} and {who[1]} {c.hh}, came to {c.village()} and built the first {c.hh} house."
    par = t.get("parents") or []
    if par:
        return f"My parents, {par[0]} and {par[1]}, built our house at {c.village()}, and I was born in it."
    return None


def PE2(c):
    """A feud or a debt from the person's relations (generate's history; the seeded agreements)."""
    import re
    for x, r in sorted((c.a.get("relations") or {}).items()):
        m = re.search(r"bad blood between your households since last winter, over (.+)$", str(r))
        if m:
            return f"{x} and I came to blows last winter over {m.group(1)}; it was never settled."
    for x, r in sorted((c.a.get("relations") or {}).items()):
        m = re.search(r"you owe them (\d+) (\w+) from last winter", str(r))
        if m:
            return f"{x} lent me {m.group(1)} {m.group(2)} last winter; I have not paid it back."
        m = re.search(r"they owe you (\d+) (\w+) from last winter", str(r))
        if m:
            return f"I lent {x} {m.group(1)} {m.group(2)} last winter; it is still owed."
    return None


def PE3(c):
    """An elder's hard winters (u9 §5.3): the history's `winter` rows within the person's life, counted in the world's years (a year
    of four seasons). The generator dates them from its tree's years (generate.simulate), so two can fall in one world year; then the
    history does not give the line's facts and it drops (u11 Gaps)."""
    year = 4 * int((c.world.get("calendar") or {}).get("season_days", 8))
    born = c.a.get("born")
    if c.a.get("stage") != "elder" or born is None:
        return None
    ago = [max(1, -(int(h["day"]) // year)) for h in c.world.get("history") or []
           if h.get("kind") == "winter" and h.get("day") is not None and int(h["day"]) >= int(born) and int(h["day"]) < 0]
    if not ago or len(set(ago)) != len(ago):
        return None
    k = len(ago)
    when = "last winter" if min(ago) == 1 else f"{min(ago)} winters ago"
    many = "a hard winter" if k == 1 else f"{k} hard winters"
    return f"I have seen {many}, {'the last of them ' if k > 1 else ''}{when}: the frost came early and the stores ran out."


def _store_food(c):
    from cybertron2.engine.data import ITEMS
    b = c.world["buildings"].get(c.house() or "") or {}
    return sum(float(q) * float((ITEMS.get(i) or {}).get("food", 0.0)) for i, q in (b.get("stock") or {}).items())


def HH1(c):
    need = sum(c.ration(x) for x in c.members())
    nights = int(round(_store_food(c) / max(need, 1e-9)))
    days = (c.world.get("calendar") or {}).get("season_days", 8)
    house = c.world["buildings"][c.house()]["name"] if c.house() else "home"
    return (f"Our store at {house} holds about {nights} nights' food for the {len(c.members())} of us as it stands; winter is {days} "
            "nights, and the hungry time is its end and the first days of spring.")


def HH2(c):
    """Next year's seed (u9 §5.4): the plots of the fields the household holds (a field's size in plots, farm.plots_of) at `plot_seed`;
    the book's keep rule that holds goods back and its `first` rule (book.py, D2-339)."""
    from cybertron2.engine.data import PHYSICS
    fields = _held(c, c.hh, "field")
    if not fields:
        return None
    plots = sum(int(p.get("size", 1)) for _, p in fields)
    seed = plots * float(PHYSICS["farming"]["plot_seed"])
    return (f"Next year's {plots} plots want about {seed:g} kilos of seed. A rule can keep it back from the pot, and say what may be "
            "eaten first instead.")


def HH3(c):
    return ("Fresh fish and meat go first or go off; what is dried, smoked, salted or in grain keeps. In a hungry spring the keeping food "
            "is what is left: eat the soft first, by rule if need be.")


def HH4(c):
    """Stores and vermin (u9 §5.4, U5 built: stores.py): grain loose on a floor or in sacks draws the mice more than bins or a granary
    floor (SPACES and CONTAINERS vermin), a cat or an owl keeps them down (kinds.STORE_STOPS); what the house's own store holds
    (stores._cap)."""
    from cybertron2.engine import stores as SR
    from cybertron2.wild.kinds import STORE_STOPS
    sp, ct = SR.SPACES, SR.CONTAINERS
    mice = lambda r: r["vermin"]["mice"] if isinstance(r["vermin"], dict) else float(r["vermin"])   # noqa: E731
    if not (min(mice(sp["floor"]), mice(ct["sack"])) > max(mice(sp["bins"]), mice(sp["granary"]))):
        return None
    if not (STORE_STOPS["cat"]["keep"]["mice"] < 1 and STORE_STOPS["owl"]["keep"]["mice"] < 1):
        return None
    head = ("Grain on a floor or in sacks draws mice; in bins or on a granary floor fewer, and a cat or a barn owl keeps them down.")
    hid = c.house()
    b = c.world["buildings"].get(hid or "") or {}
    for f in ("granary", "bins"):
        n = int((b.get("fittings") or {}).get(f, 0))
        if n:
            return head + f" The {'granary floor' if f == 'granary' else 'bins'} at {b.get('name', 'home')} hold about {SR._cap(f, b, n):g} kilos."
    return head


def HH5(c):
    return ("What we carry home stays in our hands at night unless we put it away or a rule does; a full store takes no more, and what will "
            "not go in lies at the door, where anyone may take it.")


def HH6(c):
    d = (c.world.get("calendar") or {}).get("season_days", 8)
    return (f"The hearth burns about a bundle of firewood a night and three on a cold one: a winter wants about {d} to {3 * d} bundles in "
            "by autumn's end. Timber burns longer than firewood.")


def HH7(c):
    return ("The household's rules and stores pass to whoever heads it after me. I should name an heir, and tell them where things are "
            "kept, and why.")


def HH8(c):
    return ("When the others' plans leave units over, our rules can give them chores: who tends the fire, who hangs the catch, who fetches "
            "wood. Each of us may set our own fallback instead, and theirs comes first.")


def HH9(c):
    """D2-319: the evening as a time to revisit the household's rules (a seeded custom, tried)."""
    return ("In the evening, under one roof, we look again at the household's rules: what goes where, what is eaten first, who sees to "
            "which chore. What no longer serves we change then.")


def HH10(c):
    """D2-340: passing on through care, for heads and parents: children know only what they are told; a line given while minding a
    child is kept for good; what is never passed on is lost. The things to pass are filled from the household's own water and living,
    in order, while the line stays within 40 words."""
    head = "Our children know only what we tell them. A child I mind keeps for good a line I give it: "
    tail = " What I never pass on dies with me."
    water = c.water()
    fisher = "fisher" in ((c.h or {}).get("livelihoods") or [])
    bits = []
    if water and fisher and _runs_here(c, "eel"):
        bits.append(f"when the eels run in {water}")
    elif water:
        bits.append(f"where we fish on {water}")
    bits += ["what keeps", "who to trust"] + (["where we fish"] if water and fisher else [])
    got = []
    for b in bits:
        if _words(head + ", ".join(got + [b]) + "." + tail) <= LINE_WORDS:
            got.append(b)
    return head + ", ".join(got) + "." + tail


def _parent(world, name) -> bool:
    """One with a living child or youth among the world's people (the family tree, else the children's parents)."""
    t = next((x for x in world.get("tree") or [] if x.get("name") == name), {})
    kids = set(t.get("children") or []) | {n for n, a in world["agents"].items() if name in (a.get("parents") or [])}
    return any((world["agents"].get(k) or {}).get("stage") in ("infant", "child", "youth") and world["agents"][k].get("alive", True)
               is not False for k in kids)


# the fisher (u9 §5.5.1)
def _eel_season(c):
    from cybertron2.wild.kinds import RUNS
    names = ("spring", "summer", "autumn", "winter")
    return " and ".join(names[int(k)] for k in sorted(RUNS["eel"]["seasons"]))


def FI1(c):
    river = c.water()
    if not river or not _runs_here(c, "eel"):
        return None
    cue = ("on the dark nights of the season" if c.world.get("runs_set_nights") else "on dark wet nights, most on the first rain after dry days")
    return f"The eels go down to the sea in {_eel_season(c)}, {cue}. {river[:1].upper() + river[1:]} can look empty all summer and still run thick then."


def FI2(c):
    from cybertron2.engine.data import WATER_WORKS
    if not _runs_here(c, "eel"):
        return None
    return (f"One wicker trap takes a few eels on a run night and holds no more than about {WATER_WORKS['trap']['hold']:g} kilos. A house "
            "that means to eat from the run sets many before the nights come, and tends every one each morning.")


def _rack_kg():
    from cybertron2.engine import process as PROC
    return PROC.PROCESSES["hearth rack"]["load"]


def FI3(c):
    return (f"Fresh fish goes off in {_keep('fish')} in the hand. Dry it at the hearth, up to {_rack_kg():g} kilos at a time, or salt it "
            "the day it is caught, a kilo of salt to four of fish.")


def FI4(c):
    from cybertron2.engine.data import WATER_WORKS
    w = WATER_WORKS["trap"]["wreck"]
    half = "about half" if 0.4 <= float(w["spate"]) <= 0.6 else f"about {round(float(w['spate']) * 10)} in 10"
    from cybertron2.wild.kinds import RUNS
    run = any(_runs_here(c, k) for k in RUNS)
    return (f"A spate smashes {half} the traps in the water, and a flood nearly all; an otter that finds full traps comes back each night. "
            "When the water drops, set again" + (": the run is not over." if run else "."))


def FI5(c):
    return ("In summer the fish lie in the warm shallows and pools, where a hand or a rod takes them. A water fished hard thins in days and "
            "comes back when it is rested.")


def FI6(c):
    from cybertron2.wild.kinds import RUNS
    river = c.water()
    if not river or not _runs_here(c, "salmon"):
        return None
    names = ("spring", "summer", "autumn", "winter")
    seas = " and ".join(names[int(k)] for k in sorted(RUNS["salmon"]["seasons"]))
    return (f"Salmon come up {river} after a flood, in {seas}, leaping at the shallows. Those that get past go up to spawn, and their "
            "young come back as a run in later years.")


_NETS = {}


def _run_net(land):
    """The world's river as the runs read it (wild.runs.Net from the land summary), built once a land."""
    from cybertron2.wild import ecology as EC, runs as RU
    k = id(land)
    if k not in _NETS:
        _NETS[k] = (land, RU.Net(land, EC.features(land)[0]))
    return _NETS[k][1]


def _runs_at(world, node, kind) -> bool:
    """Whether a kind's run passes a village's water, read as the engine runs it (wild.runs; W-111, wave_regressions finding 8): the
    world has the wild land, the kind runs there (not switched off), and the village's stretch is on its river: a down-run anywhere
    on a river, an up-run where the village lies below one of its spawning stretches (salmon only up a big river)."""
    from cybertron2.wild import kinds as WK, switches as SW
    land = (world.get("wild") or {}).get("land")
    r = WK.RUNS.get(kind)
    if not land or not r or node is None or kind not in WK.KINDS or kind in SW.runs_off(world) or kind in SW.kinds_off(world):
        return False
    ps = ((world["nodes"].get(node) or {}).get("parcels") or {}).values()     # a water parcel on the river, where a run is reached
    if not any(p.get("cover") == "water" and (p.get("land") or {}).get("river") not in (None, "none") for p in ps):
        return False                                                       # (wild.water.run_reach; a lake's water is not)
    nt = _run_net(land)
    g = f"v:{node}"
    if g not in nt.members:
        return False
    if r["dir"] == "down":
        return True
    return any(g in nt.path_up(x) for x in nt.spawns(r.get("where", "river"), r.get("spawn")))


def _up_run_here(c):
    """Whether any run going up passes the founder's village (the mill's hatches hold the fish going up)."""
    from cybertron2.wild.kinds import RUNS
    return any(_runs_here(c, k) for k, r in RUNS.items() if r["dir"] == "up")


def _runs_here(c, kind):
    """Whether a kind's run passes the founder's village (`_runs_at`)."""
    return bool(c.water()) and _runs_at(c.world, c.node, kind)


def FI7(c):
    if not _runs_here(c, "lamprey"):
        return None
    return "Lampreys come up in spring when the river runs high after rain: a smaller run, but the first fresh fish of the year."


def FI8(c):
    willow = next((p["name"] for p in c.parcels.values() if p["cover"] == "fen"), None)
    if not willow:
        return None
    return ("A trap wants willow rods cut in winter and soaked supple; cut in summer they give a third as much. Make and mend the traps "
            f"before the runs; the nearest willow is at {willow}.")


def _weir(c):
    holds, keepers = c.holdings()
    bid = (holds.get("weir") or [None])[0]
    return bid, (c.world["buildings"].get(bid) if bid else None)


def FI9(c):
    if not c.water():
        return None
    return ("A weir across the river takes a share of every run that passes, more at the first place than below. With its gap shut through "
            "the salmon nights it takes the most now, and leaves fewer to come back.")


def FI10(c):
    from cybertron2.engine.data import WATER_WORKS
    cost = WATER_WORKS["weir"]["cost"]                                   # D2-302: upkeep a quarter of a wattle section's build a year
    t = ((cost.get("first") or {}).get("timber") or {}).get("materials", {}).get("timber")
    w = ((cost.get("first") or {}).get("wattle") or {}).get("materials", {}).get("withies")
    if t is None or w is None:
        return None
    return (f"A wattle section wants about {max(1, round(float(w) / 4)):g} bundles of withies a year to keep, and a spate wears it twice "
            f"as fast; a timber one lasts longer and costs {t:g} loads of timber.")


def FI11(c):
    from cybertron2.engine import gear as GE
    life = GE.LIVES.get("gill net", {}).get("wet") or 16
    return ("A net of a kilo of cord, set overnight in open water, takes fish the traps miss. Mend it before it rots: it lasts about "
            f"{int(life) if isinstance(life, (int, float)) else 16} nights in the water.")


def FI12(c):
    bid, b = _weir(c)
    if not b or c.holdings()[1].get(bid) != c.name:                     # the keeper's line (W-105: read the keeper, as FI17 does)
        return None
    secs = b.get("sections") or []
    mats = sorted({s["m"] for s in secs})
    sound = all(int(s.get("level", 5)) >= 5 for s in secs)
    water = c.parcels.get(b["parcel"], {}).get("name") or c.water()
    return (f"Our weir stands on {water}: {len(secs)} sections of {' and '.join(mats)}, " + ("all of them sound" if sound else "some of them worn")
            + ". Nothing else stands below it on our water.")


def FI15(c):
    return ("In a run, a net dipped at the edge takes more than any rod; when the runs are done, a line in the deep water under the bank takes "
            "fish at dusk and dawn.")


def FI16(c):
    from cybertron2.engine.data import FITTINGS
    return (f"A hearth's rack dries {_rack_kg():g} kilos at a time over a night; a set of smoke racks takes about "
            f"{FITTINGS['smoke racks']['holds_kg']:g} kilos for a night's keeping smoke; a kilo of salt keeps four of fish.")


def _smokehouse_kept(c):
    holds, keepers = c.holdings()
    for bid in holds.get("smokehouse") or []:
        if keepers.get(bid) == c.name:
            return bid
    return None


def FI17(c, bid=None):
    from cybertron2.engine.data import FITTINGS
    bid = bid or _smokehouse_kept(c)
    if not bid:
        return None
    b = c.world["buildings"][bid]
    sets = int((b.get("fittings") or {}).get("smoke racks", 1))
    cap = sets * float(FITTINGS["smoke racks"]["holds_kg"])
    parcel = c.parcels.get(b["parcel"], {}).get("name", "")
    hard = b.get("structure") in ("timber", "stone")
    return (f"Our smokehouse on {parcel} holds {sets} set{'s' if sets != 1 else ''} of racks, about {cap:g} kilos of fish; a keeping smoke "
            "takes a night" + (", a hard cure 3 more after salting" if hard else "") + ". Its fire wants tending each night it holds fish"
            + (", and a wattle hut can catch and burn." if b.get("structure") == "wattle" else "."))


def FI18(c):
    return (f"Hot-smoked at the hearth, fish keeps {_keep('hot-smoked fish')}; a night's keeping smoke in a hut keeps it "
            f"{_keep('smoked fish')}; salted, then smoked hard three nights in a timber smokehouse, {_keep('hard-cured fish')}.")


def FI19(c):
    for hh, rep in c.rep["households"].items():
        if hh == c.hh:
            continue
        sh = (rep.get("holds") or {}).get("salt house")
        if sh:
            b = c.world["buildings"][sh[0]]
            parcel = c.parcels.get(b["parcel"], {}).get("name", "")
            return f"Salt comes from the {c.line_name(hh)}' {b.get('name', 'salt house').removeprefix('the ')} on {parcel}; the salter there wants firewood for the pan."
    return None


# the salter (u9 §5.5.6)
def SA1(c):
    return (f"A kilo of salt keeps four of fish or eight of meat for {_keep('salt fish')}. Every house that kills, fishes or makes cheese "
            "needs it, and few can make it.")


def SA2(c):
    from cybertron2.engine.data import FITTINGS, TECHNIQUES
    t = TECHNIQUES["boil salt"]
    fw = (t.get("inputs") or {}).get("firewood")
    salt = (t.get("gives") or {}).get("salt")
    life = (FITTINGS["brine pan"].get("wear") or {}).get("life")
    if fw is None or salt is None or life is None:
        return None
    return (f"{fw:g} bundles of firewood boil {salt:g} kilos of salt at the pan; the pan wears through after about {life:g} boilings and "
            "must be mended.")


def SA3(c):
    return "The pan wants copper, which only the smith makes; our fuel is the wood about us, which thins as we cut it."


def SA4(c):
    holds, keepers = c.holdings()
    bid = next((b for b in holds.get("salt house") or [] if keepers.get(b) == c.name), None)
    if not bid:
        return None
    b = c.world["buildings"][bid]
    salt = float((b.get("stock") or {}).get("salt", 0.0))
    return (f"The pan at {b.get('name', 'the salt house')} is sound, not boiled since it was last mended; the salt house holds about "
            f"{salt:g} kilos of salt as it stands.")


def SA5(c):
    return (f"Meat salted in a tub keeps {_keep('salt meat')}; salt fish keeps its year only in brine; a cheese takes a little salt and a "
            "cellar.")


def SA6(c):
    """Carrying salt (u9 §5.5.6): the carry on foot and with a pack basket (PHYSICS carry, ITEMS pack); a village within 2 days that
    makes no salt, and what it has (its households' livelihoods' gives)."""
    from cybertron2.engine.data import ITEMS, PHYSICS
    foot = float(PHYSICS["carry"]["foot"])
    for nid, d in _reach(c, 2):
        hhs = _hhs_at(c, nid)
        if not hhs or any("salter" in (c.rep["households"][h].get("livelihoods") or []) for h in hhs):
            continue
        has = _gives_words(c, hhs)
        if not has:
            continue
        return (f"Salt is heavy only in bulk: one carries about {foot:g} kilos a day's walk on foot, {foot + float(ITEMS['pack']['carry']):g} "
                f"with a pack basket; {_node_name(c, nid)}, {_days_words(d)} off, has {has} and no salt.")
    return None


def SA7(c):
    """The saltmarsh pans (u9 §5.5.6): `salt pan`'s season, on a saltmarsh the household holds."""
    from cybertron2.engine.data import TECHNIQUES
    marsh = next((p["name"] for _, p in _held(c, c.hh, "saltmarsh")), None)
    if not marsh:
        return None
    by = TECHNIQUES["salt pan"]["by_season"]
    return f"The pans on {marsh} make salt in the sun: {_by_season_words(by)}."


# ---------------------------------------------------------------------- shared reads for the livelihoods' lines (u9 §5.5.2 to §5.5.15)
SEASON_NAMES = ("spring", "summer", "autumn", "winter")


def _season_days(c) -> int:
    return int((c.world.get("calendar") or {}).get("season_days", 8))


def _share_words(x) -> str:
    """A share in words: a quarter, a third, half, two thirds, three quarters; else so many in ten."""
    for v, w in ((0.2, "a fifth"), (0.25, "a quarter"), (1 / 3, "a third"), (0.5, "half"), (2 / 3, "two thirds"), (0.75, "three quarters"), (1.0, "all")):
        if abs(float(x) - v) < 0.04:
            return w
    return f"about {round(float(x) * 10)} in 10"


def _times_words(r) -> str:
    r = float(r)
    for v, w in ((1.5, "half as much again"), (2.0, "twice as much"), (3.0, "three times as much"), (4.0, "four times as much")):
        if abs(r - v) < 0.05:
            return w
    return f"{r:g} times as much"


def _by_season_words(by) -> str:
    """A season table (`by_season`) in words, the best season first: 'most in summer, less in spring, none in winter'."""
    best = max(by.values())
    most = [s for s in SEASON_NAMES if float(by.get(s, 0.0)) >= best - 1e-9]
    none = [s for s in SEASON_NAMES if float(by.get(s, 0.0)) <= 1e-9]
    rest = [s for s in sorted(SEASON_NAMES, key=lambda s: -float(by.get(s, 0.0))) if s not in most and s not in none]
    bits = [f"most in {' and '.join(most)}"]
    for s in rest:
        bits.append(f"{_share_words(float(by[s]) / best)} as much in {s}")
    if none:
        bits.append(f"none in {' or '.join(none)}")
    return ", ".join(bits)


def _num(x) -> str:
    """A small whole number in words (a line's figure at the head of a sentence reads as speech); others as digits."""
    words = ("nought", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
    x = float(x)
    return words[int(x)] if x.is_integer() and 0 <= x <= 12 else f"{x:g}"


def _days_words(d) -> str:
    d = int(d)
    return "a day" if d == 1 else f"{d} days"


def _node_of_parcel(world, pid):
    return next((nid for nid, n in world["nodes"].items() if pid in (n.get("parcels") or {})), None)


def _node_name(c, nid) -> str:
    return (c.world["nodes"].get(nid) or {}).get("name") or nid


def _road_days(world) -> dict:
    """{node: {node: days}} by the roads' days (world spec `roads`: [a, b, days, {...}]), shortest ways."""
    import heapq
    adj = {}
    for r in world.get("roads") or []:
        a, b, d = r[0], r[1], int(r[2])
        adj.setdefault(a, []).append((b, d))
        adj.setdefault(b, []).append((a, d))
    out = {}
    for src in world["nodes"]:
        dist, todo = {src: 0}, [(0, src)]
        while todo:
            d, x = heapq.heappop(todo)
            if d > dist.get(x, 1e9):
                continue
            for y, k in adj.get(x, []):
                if d + k < dist.get(y, 1e9):
                    dist[y] = d + k
                    heapq.heappush(todo, (d + k, y))
        out[src] = dist
    return out


def _reach(c, most) -> list:
    """The other places within `most` days of home, nearest first: [(node, days)]."""
    dist = _road_days(c.world).get(c.node) or {}
    return sorted(((n, d) for n, d in dist.items() if n != c.node and d <= most), key=lambda x: (x[1], x[0]))


def _hh_node(c, hh):
    for b in c.world["buildings"].values():
        if b.get("household") == hh and (b.get("fittings") or {}).get("beds"):
            return _node_of_parcel(c.world, b["parcel"])
    return None


def _hhs_at(c, nid) -> list:
    """The filled households living at a place (their house there), in the fill's order."""
    return [hh for hh in c.rep["households"] if _hh_node(c, hh) == nid]


def _held(c, hh, cover) -> list:
    """The parcels of a cover a household holds (its `holder`, or a parcel claim), in any place: [(pid, parcel)]."""
    from cybertron2.engine.livelihoods import _held_parcels
    return _held_parcels(c.world, hh, cover)


def _herds_of(c, hh) -> list:
    return [(hid, h) for hid, h in sorted((c.world.get("herds") or {}).items()) if h.get("holder") == hh]


def _hh_buildings(c, hh) -> list:
    return [(bid, b) for bid, b in c.world["buildings"].items() if b.get("household") == hh]


def _livs(c, hh) -> list:
    return list((c.rep["households"].get(hh) or {}).get("livelihoods") or [])


def _gives_words(c, hhs) -> str:
    """What some households have to spare: their core livelihoods' gives (ROWS depends), joined."""
    from cybertron2.engine.livelihoods import ROWS
    got = []
    for hh in hhs:
        for lv in _livs(c, hh)[:1]:
            for g in ROWS[lv]["depends"]["gives"]:
                if g not in got and g not in ("labour", "carrying", "rooms", "hearths"):
                    got.append(g)
    return _and(got)


def _and(xs) -> str:
    xs = list(xs)
    return "" if not xs else xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _kept_refs(c, kind) -> list:
    holds, keepers = c.holdings()
    return [ref for ref in holds.get(kind) or [] if keepers.get(ref) == c.name]


def _wild_kind(c, kind) -> bool:
    """A wild kind in the region, as the world file names its kinds (`wild.kinds`; `_wolves` reads the same)."""
    return kind in ((c.world.get("wild") or {}).get("kinds") or [])


def _built_bone() -> bool:
    """Whether anything in the engine gives bone (a technique's gives or yield goods, a wild kind's goods)."""
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.wild.kinds import TAKEN
    for t in TECHNIQUES.values():
        gv = t.get("gives")
        if (isinstance(gv, dict) and "bone" in gv) or gv == "bone" or "'bone'" in str((t.get("yield") or {}).get("gives") or ""):
            return True
    return any("bone" in ((r or {}).get("goods") or {}) for r in TAKEN.values())


def _built_technique(*names) -> bool:
    from cybertron2.engine.data import TECHNIQUES
    return any(n in TECHNIQUES for n in names)


# the farmer (u9 §5.5.2)
def _sowing(c):
    from cybertron2.engine import lore as LO
    return LO.sowing_times(_season_days(c))


def _sow_bit(c, fam) -> str:
    from cybertron2.engine import lore as LO
    from cybertron2.engine.data import CROPS
    best, well = _sowing(c)[fam]
    name = CROPS[fam]["names"][0]
    bit = f"{name} {'do' if name.endswith('s') else 'does'} best sown {LO._when(best)}"
    return bit + (f", and well {LO._when(well)}" if well else "")


def FA1(c):
    """The sowing lore for barley (lore.sowing_times, D4-105, D4-114), split from the rye and beans so no cap cuts it."""
    if not _has_fields(c):
        return None
    t = _sow_bit(c, "grain")
    return t[:1].upper() + t[1:] + "; sown at other times it comes up poor or not at all."


def FA2(c):
    """The sowing lore for rye and beans; rye's winter from CROPS needs_winter."""
    from cybertron2.engine.data import CROPS
    if not _has_fields(c):
        return None
    rye, beans = _sow_bit(c, "winter grain"), _sow_bit(c, "legumes")
    wants = ", and wants a winter in the ground" if CROPS["winter grain"].get("needs_winter") is not None else ""
    return rye[:1].upper() + rye[1:] + wants + "; " + beans + "."


def FA3(c):
    """`plot_seed` (kg of seed a plot: grain weighs 1 kg a unit) and `select seed` (D2-65: seed chosen from the best of a ripe crop
    ripens sooner)."""
    from cybertron2.engine.data import PHYSICS, TECHNIQUES
    seed = float(PHYSICS["farming"]["plot_seed"])
    sel = ("; seed chosen from the best ears of a ripe crop ripens sooner" if "select seed" in TECHNIQUES
           and float(PHYSICS.get("seed_selection", 1.0)) < 1.0 else "")
    return f"A plot wants about {seed:g} kilos of seed{sel}. Seed eaten in a hungry spring is next year's harvest gone."


def FA4(c):
    """CROPS needs_winter and hardy; the farming frost loss a cold night (frost_loss) and seed lost lying in cold ground (lie_loss)."""
    from cybertron2.engine.data import CROPS, PHYSICS
    f = PHYSICS["farming"]
    tender = [CROPS[k]["names"][0] for k in ("grain", "legumes") if not CROPS[k]["hardy"]]
    rye = CROPS["winter grain"]
    if not tender or rye.get("needs_winter") is None:
        return None
    return (f"Rye wants a winter in the ground and bears poor without one; {_and(tender)} are tender: each frosty night takes "
            f"{_share_words(f['frost_loss'])} of what is growing. Seed sown in cold ground lies, and is lost a little each night.")


def FA5(c):
    """The farming window (days ripe before it rots), the rot a night past it, and the green good a crop reaped unripe gives."""
    from cybertron2.engine.data import CROPS, PHYSICS
    f = PHYSICS["farming"]
    return (f"Ripe corn will not wait: left standing more than {int(f['window'])} days it sheds and rots, {_share_words(f['rot'])} "
            f"each night, and ears reaped too soon give only {CROPS['grain']['green']}, fit for fodder.")


def FA6(c):
    """The tool grades of `reap` and `fell`, and `plough`'s plots a unit against `hoe`'s with a crude tool."""
    from cybertron2.engine.data import TECHNIQUES as T
    reap = T["reap"]["tools"]["copper"] / T["reap"]["tools"]["crude"]
    fell = T["fell"]["tools"]["copper"] / T["fell"]["tools"]["crude"]
    plough = T["plough"]["yield"]["plots"] / (T["hoe"]["yield"]["plots"] * T["hoe"]["tools"]["crude"])
    fast = {4: "four times", 3: "three times", 2: "twice"}.get(int(round(plough)), f"{plough:g} times")
    return (f"A crude tool reaps and fells; a copper one from the smith reaps {_times_words(reap)} and fells {_times_words(fell)}. "
            f"Oxen and a plough break the ground {fast} as fast as a hoe.")


def _ox_pair(c, ref):
    hid = ref.split(":", 1)[1]
    return (c.world.get("herds") or {}).get(hid)


def FA7(c):
    """The ox pair's keeper (u9 §5.6): a plot's units at the plough against the hoe; the beasts' winter fodder (stalls: FITTINGS)."""
    from cybertron2.engine.data import FITTINGS, TECHNIQUES as T
    refs = _kept_refs(c, "ox pair")
    if not refs:
        return None
    plough = 1.0 / float(T["plough"]["yield"]["plots"])
    hoe = 1.0 / (float(T["hoe"]["yield"]["plots"]) * float(T["hoe"]["tools"]["crude"]))
    less = _share_words(1 - float(FITTINGS["stalls"]["fodder"]))
    return (f"Our oxen plough a plot in {plough:g} units where a hoe takes {hoe:g}; they eat hay when the grass is gone, {less} less "
            "in stalls, and the plough and harness wear with use.")


def FA8(c):
    """CROPS takes and restores: the crops that tire the ground and the one that gives it back; fallow and manure (PHYSICS farming)."""
    from cybertron2.engine.data import CROPS
    tire = [CROPS[k]["names"][0] for k in ("grain", "winter grain") if float(CROPS[k]["takes"]) > 0]
    give = [CROPS[k]["names"][0] for k in ("legumes",) if float(CROPS[k]["takes"]) <= 0 and float(CROPS[k]["restores"][0]) > 0]
    if not tire or not give:
        return None
    return (f"{_and(tire).capitalize()} sown year on year tires the ground; {_and(give)} give it back. A field rested, or dunged, "
            "bears better.")


def FA9(c):
    """The fields' keeper (u9 §5.6): each field the household holds, its crop standing or its last, its soil (farm.soil_word)."""
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import CROP_OF, CROPS
    refs = _kept_refs(c, "fields")
    if not refs:
        return None
    bits = []
    for ref in refs[:2]:
        pid = ref.split(":", 1)[1]
        p = next(n["parcels"][pid] for n in c.world["nodes"].values() if pid in (n.get("parcels") or {}))
        st = p.get("state") or {}
        crop = (st.get("crop") or {}).get("kind")
        last = st.get("last_crop")
        last = CROPS[last]["names"][0] if last in CROPS else last
        soil = FM.soil_word(float(p.get("fertility", 1.0)))
        if crop:
            fam = CROP_OF.get(crop, crop)
            bit = f"{p['name']} stands in {CROPS[fam]['names'][0] if fam in CROPS else crop}"
        else:
            bit = f"{p['name']} lies empty"
        if last:
            bit += f", {last} last year" if last != "fallow" else ", rested last year"
        bits.append(bit + f", its soil {soil}")
    t = "; ".join(bits) + "."
    return t[:1].upper() + t[1:]


def _mills_within(c, most):
    """Mills (a water wheel or millstones) at home or within `most` days: [(bid, building, days)]."""
    reach = dict([(c.node, 0)] + _reach(c, most))
    out = []
    for bid, b in sorted(c.world["buildings"].items()):
        f = b.get("fittings") or {}
        if f.get("water wheel") or f.get("millstones"):
            nid = _node_of_parcel(c.world, b["parcel"])
            if nid in reach:
                out.append((bid, b, reach[nid]))
    return sorted(out, key=lambda x: (x[2], x[0]))


def FA10(c):
    """The food rows: flour against boiled grain, bread against flour (ITEMS food; `bread` gives as much as it takes); a mill within a
    day."""
    from cybertron2.engine.data import ITEMS
    mills = _mills_within(c, 1)
    if not mills:
        return None
    up = ITEMS["flour"]["food"] / ITEMS["grain"]["food"]
    more = "about half as far again" if 1.35 <= up <= 1.65 else f"{up:.1f} times as far"
    bread = ITEMS["bread"]["food"] > ITEMS["flour"]["food"]
    name = mills[0][1].get("name") or "the mill"
    return (f"Grain ground to flour feeds {more} as boiled grain{', and bread further' if bread else ''}; {name} grinds for those "
            "who bring it grain.")


def FA11(c):
    """The woodpigeon's seasons at the corn (kinds.NEAR_PEOPLE targets); the scares (methods.SCARES); herds drawn to a ripe crop and
    trampling it (HERDS draw, trample)."""
    from cybertron2.wild.kinds import NEAR_PEOPLE
    rows = (NEAR_PEOPLE.get("woodpigeon") or {}).get("targets") or []
    seas = sorted({int(k) for r in rows for k in (r.get("seasons") or {})})
    if not seas:
        return None
    when = " and again in ".join(SEASON_NAMES[s] for s in seas)
    return (f"Woodpigeons come down on the sowing in {when}; clappers or a watch keep them off. Beasts through an open gate are "
            "drawn to a ripe crop and trample it.")


# the herder (u9 §5.5.3)
def HE1(c):
    """`hay`'s season; cattle hungry `starve_nights` nights running begin to die (farm._herds)."""
    from cybertron2.engine.data import PHYSICS, TECHNIQUES
    by = TECHNIQUES["hay"]["by_season"]
    return (f"Hay is cut {_by_season_words(by)}; beasts on bare winter grass without it begin to die after about "
            f"{int(PHYSICS['cattle']['starve_nights'])} hungry nights.")


def HE2(c):
    """Herds stray (PHYSICS cattle stray), walk home at dusk (HERDS dusk), and are lost on the road (HERDS road)."""
    return ("Cattle stray through an open gate, and most walk home at dusk; a beast that strays onto the road may die there or be "
            "lost.")


def HE3(c):
    """The wolf's seasons at the herds (kinds.NEAR_PEOPLE: all winter and the first days of spring at full draw) and what turns it (a
    fence round the herd's ground, a watch over it: wild.attempt)."""
    from cybertron2.wild.kinds import NEAR_PEOPLE
    if not _wolves(c):
        return None
    row = next((r for r in NEAR_PEOPLE["wolf"]["targets"] if r.get("what") == "herd" and float(r.get("attr", 0)) >= 1.0), None)
    if not row:
        return None
    seas = row["seasons"]
    sd = _season_days(c)
    bits = []
    for k in sorted(seas, key=lambda s: (int(s) - 3) % 4):
        lo, hi = seas[k]
        name = SEASON_NAMES[int(k)]
        bits.append(f"all {name}" if hi - lo + 1 >= sd else f"the first days of {name}")
    return (f"The wolves come to the herds {' and into '.join(bits)}; a fence round the beasts' ground, or a watch over them by night, "
            "turns most.")


def HE4(c):
    """Grazing by cover (PHYSICS cattle grazing); the murrain's spread on shared grass and from the deer (kinds.DISEASES)."""
    from cybertron2.engine.data import PHYSICS
    from cybertron2.wild.kinds import DISEASES
    g = PHYSICS["cattle"]["grazing"]
    best = [k for k in ("pasture", "meadow") if float(g.get(k, 0)) >= 1.0]
    less = [k for k in ("heath", "moor") if float(g.get(k, 1)) < float(g.get("fen", 0))]
    m = DISEASES.get("murrain") or {}
    tail = ("; the murrain goes worst where herds share the grass, and comes from the deer" if m.get("beta") and m.get("wild") else "")
    return (f"{_and(best).capitalize()} feed beasts best, fen {_share_words(g['fen'])} as well, {_and(less)} less{tail}.")


def _cellar(c):
    return next((b for _, b in _hh_buildings(c, c.hh) if (b.get("fittings") or {}).get("cellar")), None)


def HE5(c):
    """`milk` keeps the day (ITEMS spoil 1.0); `cheese`'s inputs and gives at a cellar; cheese's keeping in words."""
    from cybertron2.engine.data import TECHNIQUES
    if not _cellar(c):
        return None
    t = TECHNIQUES["cheese"]
    milk, out = float(t["inputs"]["milk"]), float(t["gives"]["cheese"])
    return (f"Milk will not keep past the day it is drawn; {milk:g} kilos of it with a little salt make about {round(out):g} of cheese "
            f"in a cellar, and cheese keeps {_keep('cheese')}.")


def HE6(c):
    """`plough` wants two oxen; breeding wants a bull with the cows (farm._herds)."""
    from cybertron2.engine.data import TECHNIQUES
    hs = [h for _, h in _herds_of(c, c.hh)]
    if not any(int(h.get("oxen", 0)) > 0 or int(h.get("bulls", 0)) > 0 for h in hs):
        return None
    n = int(TECHNIQUES["plough"]["animals"]["oxen"])
    return (f"Without the plough oxen, {n} to a yoke, there is no ploughing, and without the bull no calves; meat from them is eaten "
            "once.")


def HE7(c):
    """The herd's keeper (u9 §5.6): the herd's beasts by kind, where it grazes, the cows in milk."""
    refs = _kept_refs(c, "herd")
    if not refs:
        return None
    h = (c.world.get("herds") or {})[refs[0].split(":", 1)[1]]
    p = next((n["parcels"][h["parcel"]] for n in c.world["nodes"].values() if h.get("parcel") in (n.get("parcels") or {})), {})
    parts = []
    for k, one, many in (("cows", "cow", "cows"), ("oxen", "ox", "oxen"), ("bulls", "bull", "bulls"), ("young", "calf", "calves")):
        n = int(h.get(k, 0))
        if n:
            parts.append(f"a {one}" if n == 1 else f"{n} {many}")
    milk = int(round(float(h.get("in_milk", 0))))
    tail = f"; {milk} of the cows are in milk" if milk > 1 else ("; one cow is in milk" if milk == 1 else "; no cow is in milk")
    return f"Our herd is {_and(parts)}, kept on {p.get('name', 'the common')}{tail if int(h.get('cows', 0)) else ''}."


def HE8(c):
    """Fodder a head a night (farm._herds: a beast's need is 1, a bundle of hay is 1 fodder: ITEMS hay); stalls' saving; the herd's
    head and winter's nights."""
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import FITTINGS, ITEMS
    hs = [h for _, h in _herds_of(c, c.hh)]
    n = sum(FM.head(h) if "count" not in h else int(h["count"]) for h in hs) if hs else 0
    if not n:
        return None
    d = _season_days(c)
    per = 1.0 / float(ITEMS["hay"]["fodder"])
    less = _share_words(1 - float(FITTINGS["stalls"]["fodder"]))
    return (f"A beast eats about {'a bundle' if per == 1 else f'{per:g} bundles'} of hay a night when there is no grass, {less} less in "
            f"stalls: our {n} beasts want about {round(n * per * d)} bundles for the {d} nights of winter.")


# the hunter and trapper (u9 §5.5.4)
def HU1(c):
    """`snare`'s covers; a catch left a night untended breaks free or is scavenged (wild.SNARE_NIGHT)."""
    from cybertron2.engine.data import TECHNIQUES
    from cybertron2.engine.wild import SNARE_NIGHT
    cov = [x for x in TECHNIQUES["snare"]["at"]["covers"]]
    wood = "forest" not in cov
    if not SNARE_NIGHT.get("scavenged") or not SNARE_NIGHT.get("free"):
        return None
    return (f"Snares go on the runs in {_and(cov)}{', never in the wood' if wood else ''}; a hare snared in the night is best taken "
            "at first light, before it breaks free or a fox or the crows take it.")


def HU2(c):
    """Wariness where hunted (kinds.WARY); the carry on foot (PHYSICS carry)."""
    from cybertron2.engine.data import PHYSICS
    return (f"Game near home grows wary when it is hunted hard; fresh ground a day or two out gives far more, but one carries home only "
            f"about {float(PHYSICS['carry']['foot']):g} kilos.")


def _half_words(c, lo, hi, season) -> str:
    sd = _season_days(c)
    if hi < sd // 2:
        return f"early in {season}"
    if lo >= sd // 2:
        return f"late in {season}"
    return f"in {season}"


def HU3(c):
    """The red deer's rut and calving (kinds.WHEN rows: their seasons and halves)."""
    from cybertron2.wild.kinds import WHEN
    if not _wild_kind(c, "red deer"):
        return None
    rows = {r.get("name"): r for r in WHEN.get("red deer") or []}
    rut, calf = rows.get("rut"), rows.get("calving")
    if not rut or not calf:
        return None
    (rk, (rlo, rhi)), = rut["if"]["seasons"].items()
    (ck, (clo, chi)), = calf["if"]["seasons"].items()
    return (f"{_half_words(c, rlo, rhi, SEASON_NAMES[int(rk)]).capitalize()} the stags roar at dusk in the rut, bold and careless and "
            f"easier to come on; {_half_words(c, clo, chi, SEASON_NAMES[int(ck)])} the hinds drop their calves.")


def HU4(c):
    """A carcass draws the wolf and (in a hungry spring) the bear (kinds.NEAR_PEOPLE carcass targets); fresh, dried and salted meat's
    keeping in words."""
    who = "the wolf and, in a hungry spring, the bear" if _wolves(c) and _wild_kind(c, "brown bear") else (
        "the wolf" if _wolves(c) else "the fox and the crows")
    return (f"A kill left lying draws {who}: dress it and carry it in the same day. Fresh meat goes off in {_keep('meat')}; dried it "
            f"keeps {_keep('dried meat')}.")


def HU5(c):
    """`stalk` (slow: its units; wood and heath: its covers; a weapon), `drive` (a crew; dangerous), `hunt the wild` (what comes)."""
    from cybertron2.engine.data import TECHNIQUES as T
    if not T["drive"].get("crew") or T["stalk"]["units"] <= T["hunt the wild"]["units"]:
        return None
    return ("Stalking is slow work in wood and heath, downwind and close; a drive wants beaters and spears and is dangerous; one "
            "alone with a weapon takes what comes.")


def HU6(c):
    """A wood within 2 days that holds game (a forest parcel with a game stock at another place), and the camp (BLUEPRINTS camp)."""
    for nid, d in _reach(c, 2):
        for pid, p in sorted((c.world["nodes"][nid].get("parcels") or {}).items()):
            if p.get("cover") == "forest" and ((p.get("state") or {}).get("game") or {}).get("K"):
                t = f"{p['name']}, {_days_words(d)} off, holds game; a camp there saves the walk home each night."
                return t[:1].upper() + t[1:]
    return None


def HU7(c):
    """`snares`' cord a snare (gear.RECIPES), a set snare's loss a night (gear.LIVES snare torn), wariness on a run snared hard."""
    from cybertron2.engine import gear as GE
    cord = float(GE.RECIPES["snares"]["inputs"]["cord"])
    torn = float(GE.LIVES["snare"]["torn"])
    return (f"Snares are twisted from a little cord, about {round(1 / cord)} to a kilo; a set snare is lost or torn about one night in "
            f"{_num(round(1 / torn))}, and a run snared hard goes cold.")


def HU8(c):
    """[built: dressing the kill] (u3): no technique dresses a kill yet, so the line waits."""
    if not _built_technique("dress the kill", "dress a kill"):
        return None
    return ("A kill gives more than meat: the hide, the tallow of a fat beast, and bone; a careful hand takes all of it, a careless "
            "one wastes meat.")


# the smith and miner (u9 §5.5.7)
def SM1(c):
    """`charcoal`'s timber a sack; `smelt`'s fuel (a sack of charcoal or so many loads of timber)."""
    from cybertron2.engine.data import TECHNIQUES as T
    t = float(T["charcoal"]["inputs"]["timber"])
    fuel = T["smelt"]["inputs"]["fuel"]
    return (f"{_num(t).capitalize()} loads of timber burnt slow in the wood make one sack of charcoal; at the anvil a sack of it smelts "
            f"as much as {_num(float(fuel['timber']) / float(fuel['charcoal']))} loads of timber.")


def SM2(c):
    """Tool grades (`hoe`, `reap`, `fell`), tool lives (ITEMS life), and what wants copper (`wooden plough`'s inputs, the brine pan's
    materials, `copper hook`)."""
    from cybertron2.engine.data import FITTINGS, ITEMS, TECHNIQUES as T
    most = T["reap"]["tools"]["copper"] / T["reap"]["tools"]["crude"]
    fell = T["fell"]["tools"]["copper"] / T["fell"]["tools"]["crude"]
    life = float(ITEMS["copper tool"]["life"]) / float(ITEMS["crude tool"]["life"])
    want = []
    if (T.get("wooden plough") or {}).get("inputs", {}).get("copper"):
        want.append("the plough")
    if FITTINGS["brine pan"]["materials"].get("copper"):
        want.append("the salter's pan")
    if "copper hook" in T:
        want.append("the fishers' hooks")
    lasts = {4: "four times", 3: "three times", 2: "twice"}.get(int(round(life)), f"{life:g} times")
    return (f"A copper tool does {_times_words(most)} as a crude one, {_times_words(fell)} at felling, and lasts {lasts} as long; "
            f"{_and(want)} all want copper.")


def SM3(c):
    """The skilled class (learning.cls) and practice alone against teaching (learning.ALONE, D2-326)."""
    from cybertron2.engine import learning as LR
    if LR.cls("smelt") != "skilled":
        return None
    k = {2: "twice", 3: "three times"}.get(int(round(LR.ALONE)), f"{LR.ALONE:g} times")
    return f"Smithing is skilled work: tries alone get one there in time, but take {k} as many as with a teacher at the anvil."


def SM4(c):
    """The forge's keeper (u9 §5.6): its anvil and bellows on a hearth (FITTINGS anvil needs hearth), its charcoal now."""
    from cybertron2.engine.data import FITTINGS
    bid = next(iter(_kept_refs(c, "forge")), None)
    if not bid:
        return None
    b = c.world["buildings"][bid]
    n = float((b.get("stock") or {}).get("charcoal", 0.0))
    has = f"{n:g} sack{'s' if n != 1 else ''}" if n else "none"
    on = " on its hearth" if FITTINGS["anvil"].get("needs") == "hearth" else ""
    return f"Our forge at {b.get('name', 'the forge')} has an anvil and bellows{on}; it burns charcoal by the sack, and holds {has} now."


def _rock_within(c, most, res):
    """A rock parcel with a stock of `res` (seam, quarry) at home or within `most` days: (name, days) or None."""
    for nid, d in [(c.node, 0)] + _reach(c, most):
        for pid, p in sorted((c.world["nodes"][nid].get("parcels") or {}).items()):
            if p.get("cover") == "rock" and ((p.get("state") or {}).get(res) or {}).get("K"):
                return p["name"], d
    return None


def SM5(c):
    """`mine` at rock with a seam; `smelt`'s ore and charcoal for one copper (ITEMS weights: kilos)."""
    from cybertron2.engine.data import ITEMS, TECHNIQUES as T
    got = _rock_within(c, 2, "seam")
    if not got:
        return None
    place, d = got
    ore = float(T["smelt"]["inputs"]["copper ore"]) * float(ITEMS["copper ore"]["weight"])
    out = float(T["smelt"]["gives"]["copper"]) * float(ITEMS["copper"]["weight"])
    where = f"at {place}" + (f", {_days_words(d)} off" if d else "")
    return (f"Ore is dug where the rock shows it, {where}, and wants a tool; {ore:g} kilos of ore and a sack of charcoal smelt to "
            f"{'a kilo' if out == 1 else f'{out:g} kilos'} of copper at the anvil.")


def SM6(c):
    """The households in reach whose holdings want copper work: a brine pan (its materials and mending), a plough (its inputs), a water
    wheel (its materials), and the fishers' hooks."""
    from cybertron2.engine.data import FITTINGS
    near = [c.node] + [n for n, _ in _reach(c, 1)]
    bits = []
    for hh in c.rep["households"]:
        if hh == c.hh or _hh_node(c, hh) not in near:
            continue
        holds, _ = c.holdings(hh)
        if holds.get("salt house") and FITTINGS["brine pan"]["materials"].get("copper"):
            bits.append(f"the {c.line_name(hh)}' pan")
        if holds.get("ox pair"):
            bits.append(f"the {c.line_name(hh)}' plough")
        if holds.get("mill") and any((c.world["buildings"][b].get("fittings") or {}).get("water wheel") for b in holds["mill"]):
            bits.append(f"the {c.line_name(hh)}' mill wheel")
    if any("fisher" in _livs(c, hh)[:1] for hh in c.rep["households"] if hh != c.hh and _hh_node(c, hh) in near):
        bits.append("the fishers' hooks")
    if not bits:
        return None
    tail = " are copper work: those who need them come to us."
    got = []
    for b in bits:
        if _words(_and(got + [b]) + tail) <= LINE_WORDS:
            got.append(b)
    t = _and(got) + tail
    return t[:1].upper() + t[1:]


# the miller and baker (u9 §5.5.8)
def MI1(c):
    """The food rows (flour against boiled grain, bread); flour's, grain's and bread's keeping in words."""
    from cybertron2.engine.data import ITEMS
    up = ITEMS["flour"]["food"] / ITEMS["grain"]["food"]
    more = "about half as far again" if 1.35 <= up <= 1.65 else f"{up:.1f} times as far"
    return (f"Grain ground to flour feeds {more} as boiled grain, and bread further still; flour keeps {_keep('flour')}, grain "
            f"{_keep('grain')}, and bread goes off in {_keep('bread')}.")


def _harvest_seasons(c) -> list:
    """The seasons the field grain ripens in when sown at its best time (farm.season_run on lore.sowing_times)."""
    from cybertron2.engine import farm as FM
    from cybertron2.engine.data import PHYSICS
    sd = _season_days(c)

    def season_of(d):
        return SEASON_NAMES[(d // sd) % 4]
    out = []
    for fam in ("grain", "winter grain"):
        best, _ = _sowing(c)[fam]
        h, s = best[0]
        start = SEASON_NAMES.index(s) * sd + (0 if h == "early" else sd // 2)
        n, _, _ = FM.season_run(fam, start, season_of, FM.grow_days(4 * sd, fam), PHYSICS["farming"],
                                cold_of=lambda d: season_of(d) == "winter")
        if n and season_of(start + n) not in out:
            out.append(season_of(start + n))
    return out


def MI2(c):
    """The crop calendar: when the field grain ripens (farm.season_run at its best sowing)."""
    seas = _harvest_seasons(c)
    if not seas:
        return None
    return f"The farm houses bring grain after the harvest, in {_and(seas)}; the mill is busiest then."


def _mill_kept(c):
    return next(iter(_kept_refs(c, "mill")), None)


def MI3(c):
    """The mill's keeper (u9 §5.6): its batch (`water mill` or `mill`'s grain), the wheel's wear by the year (FITTINGS water wheel
    years), the stones' wear by grain ground (millstones life), their state now (the building's `worn`, wear.py)."""
    from cybertron2.engine.data import FITTINGS, TECHNIQUES as T
    bid = _mill_kept(c)
    if not bid:
        return None
    b = c.world["buildings"][bid]
    f = b.get("fittings") or {}
    worn = b.get("worn") or {}
    life = float(FITTINGS["millstones"]["wear"]["life"])
    used = float((worn.get("millstones") or {}).get("used", 0.0))
    if f.get("water wheel"):
        yrs = float(FITTINGS["water wheel"]["wear"]["years"])
        each = "once a year" if yrs == 1 else f"every {yrs:g} years"
        return (f"Our mill grinds up to {float(T['water mill']['inputs']['grain']):g} kilos of grain at a turn; the leat silts and wants "
                f"clearing {each}, the stones dressing after about {life:g} kilos ground. "
                + ("Both are sound as it stands." if used < life else "The stones want dressing now."))
    return (f"Our mill grinds up to {float(T['mill']['inputs']['grain']):g} kilos of grain at a turn with an ox at the stones; they want "
            f"dressing after about {life:g} kilos ground" + (", and are sound as it stands." if used < life else ", and want it now."))


def MI4(c):
    """The water wheel's gap (WATER_WORKS mill: shut, full and half a run going up held; open, `open_rate`), on a river a run passes."""
    from cybertron2.engine.data import WATER_WORKS
    bid = _mill_kept(c)
    if not bid or not (c.world["buildings"][bid].get("fittings") or {}).get("water wheel") or not c.water() or not _up_run_here(c):
        return None
    m = WATER_WORKS["mill"]
    return (f"Shut, the hatches hold the river: the wheel turns full, and {_share_words(m['stop'])} the fish going up are held below. "
            f"Drawn, they let the fish by, and the wheel turns at {_share_words(m['open_rate'])}.")


def MI5(c):
    """The oven's keeper (u9 §5.6): `oven bread`'s batch and fuel, the oven's wear (FITTINGS oven life) and its relining's stone."""
    from cybertron2.engine.data import FITTINGS, TECHNIQUES as T
    bid = next(iter(_kept_refs(c, "oven")), None)
    if not bid:
        return None
    t = T["oven bread"]
    life = int(FITTINGS["oven"]["wear"]["life"])
    stone = (T["reline oven"]["yield"].get("inputs") or {}).get("stone")
    return (f"Our oven bakes up to {float(t['inputs']['flour']):g} kilos of flour into bread at a firing, with "
            f"{float(t['inputs']['firewood']):g} bundles of firewood, and wants relining{' with stone' if stone else ''} after about "
            f"{life} firings.")


# the builder: wright and mason (u9 §5.5.9)
def BU1(c):
    """Building wear by structure (PHYSICS wear minor) and weather (frost, wind, snow); repair's materials (buildings.repair_need)."""
    from cybertron2.engine.data import PHYSICS
    m = PHYSICS["wear"]["minor"]
    if not (m["wattle"] > m["timber"] > m["stone"]):
        return None
    return ("Every house wears with the weather, wattle fastest, and worst in frost, wind and snow; unmended it falls to ruin. "
            "Mending wants timber, or stone for a stone house: keep some back from the fire.")


def BU2(c):
    """`fell` (timber a unit, with a tool) against `firewood` (dead wood by hand); `crude tool`'s inputs."""
    from cybertron2.engine.data import TECHNIQUES as T
    if not T["crude tool"]["inputs"].get("stone"):
        return None
    return ("Felling with a tool gives far more than gathering dead wood by hand; a crude tool wants only a little wood and stone.")


def BU3(c):
    """U5's stores (stores.SPACES, stores._cap): what the household's house holds in its stores; a full store takes no more."""
    from cybertron2.engine import stores as SR
    from cybertron2.engine.data import STORES
    hid = c.house()
    if not hid:
        return None
    b = c.world["buildings"][hid]
    bits = []
    for f, n in (b.get("fittings") or {}).items():
        if f in SR.SPACES and f in STORES["order"]:
            try:
                cap = SR._cap(f, b, int(n))
            except Exception:
                continue
            bits.append(f"{STORES['words'][f][0].removeprefix('the ')} about {cap:g} kilos")
    if not bits:
        return None
    return (f"A full store takes no more, and what will not go in lies at the door; at {b.get('name', 'home')} the "
            f"{_and(bits)}.")


def BU4(c):
    """D2-324: building work is units times skill (verbs._build_act); an expert's skill against a beginner's (livelihoods.skill_for's
    bands on the class range of a timber room)."""
    from cybertron2.engine import livelihoods as LV
    lo, hi = LV.class_range("medium room")
    expert, beginner = lo + 0.775 * (hi - lo), lo + 0.125 * (hi - lo)
    r = expert / beginner
    if r < 1.6:
        return None
    k = "about half the days" if r < 2.4 else "about a third of the days"
    return f"One who knows the work raises a room in {k} one new to it takes."


def BU5(c):
    """[built: seasoning] (W-76): timber does not season in the engine yet, so the line waits."""
    from cybertron2.engine.data import ITEMS
    if "seasoned timber" not in ITEMS:
        return None
    return "Timber felled in winter and seasoned before it is worked splits less and lasts longer; green timber warps in the frame."


def BU6(c):
    """The wright's work (the carpenter's trade on the water wheel, the plough, the handcart) and who in reach holds or needs which:
    a mill with a wheel, an ox team, a carrier."""
    from cybertron2.engine.data import FITTINGS, TECHNIQUES as T
    works = []
    if FITTINGS["water wheel"].get("trade") == "carpenter":
        works.append(("the mill's wheel", lambda hh, holds: any((c.world["buildings"][b].get("fittings") or {}).get("water wheel")
                                                                for b in holds.get("mill") or [])))
    if (T.get("wooden plough") or {}).get("trade") == "carpenter":
        works.append(("the plough", lambda hh, holds: bool(holds.get("ox pair"))))
    if (T.get("handcart") or {}).get("trade") == "carpenter":
        works.append(("the handcart", lambda hh, holds: "trader" in _livs(c, hh)))
    near = [c.node] + [n for n, _ in _reach(c, 1)]
    need, who = [], []
    for hh in c.rep["households"]:
        if hh == c.hh or _hh_node(c, hh) not in near:
            continue
        holds, _ = c.holdings(hh)
        got = [name for name, f in works if f(hh, holds)]
        if got:
            who.append(f"the {c.line_name(hh)}")
            need += [g for g in got if g not in need]
    if not need:
        return None
    need = [name for name, _ in works if name in need]
    return f"{_and(need).capitalize()} {'are' if len(need) > 1 else 'is'} a wright's work; {_and(who[:3])} need {'them' if len(need) > 1 else 'it'}."


def BU7(c):
    """`quarry` at rock with a quarry stock (needs a tool: no bare hands in its tools)."""
    from cybertron2.engine.data import TECHNIQUES as T
    got = _rock_within(c, 2, "quarry")
    if not got:
        return None
    place, d = got
    tool = "; quarrying wants a tool" if "bare" not in (T["quarry"].get("tools") or {}) else ""
    return f"Stone lies only where the rock shows, at {place}" + (f", {_days_words(d)} off" if d else "") + tool + "."


def BU8(c):
    """The hearth's and the oven's stone (FITTINGS materials); the oven only in a stone house (its structure); stone's wear against
    wattle's (PHYSICS wear minor)."""
    from cybertron2.engine.data import FITTINGS, PHYSICS
    m = PHYSICS["wear"]["minor"]
    r = float(m["wattle"]) / float(m["stone"])
    frac = "a tenth" if 8 <= r <= 12 else f"1 in {round(r)}"
    stone_only = ", and an oven stands only in a stone house" if FITTINGS["oven"].get("structure") == "stone" else ""
    return (f"A hearth wants {FITTINGS['hearth']['materials']['stone']:g} stones and an oven {FITTINGS['oven']['materials']['stone']:g}"
            f"{stone_only}; stone walls wear about {frac} as fast as wattle.")


# the woodsman (u9 §5.5.10)
def _home_wood(c):
    return next(((pid, p) for pid, p in sorted(c.parcels.items()) if p.get("cover") == "forest"), (None, None))


def WO1(c):
    """Young growth's regrowth (FORESTS kinds regrow, a year's rate: logistic back from a twentieth to most of it) and dead wood's
    coming back only as the trees shed it (FORESTS shed)."""
    import math
    from cybertron2.engine.data import FORESTS
    pid, p = _home_wood(c)
    if not p:
        return None
    kind = ((p.get("state") or {}).get("wood") or {}).get("kind") or "copse"
    r = float((FORESTS["kinds"].get(kind) or FORESTS["kinds"]["copse"])["regrow"])
    if r <= 0:
        return None
    years = math.log(0.9 / 0.1 * (1 / 0.05 - 1)) / r
    when = "a few years" if years <= 6 else "many years"
    return (f"Young growth cut in {p['name']} comes again in {when}; dead wood once gathered comes back only slowly, as the old trees "
            "shed it.")


def WO2(c):
    """`charcoal`'s timber a sack; the smith's anvil (`smelt`'s fuel); a hearth burns it last, by heat (ITEMS heat, PHYSICS heat
    order)."""
    from cybertron2.engine.data import ITEMS, TECHNIQUES as T
    t = float(T["charcoal"]["inputs"]["timber"])
    k = float(ITEMS["charcoal"]["heat"]) / float(ITEMS["firewood"]["heat"])
    return (f"{_num(t).capitalize()} loads of timber burnt slow in the wood make a sack of charcoal; the smith wants it at the anvil, "
            f"and a hearth burns a sack as long as {_num(k)} bundles of firewood.")


def WO3(c):
    """[built: the burn as a process] (U4 or W-76): charcoal is made in one act, not watched over nights, so the line waits."""
    from cybertron2.engine import process as PROC
    if "charcoal" not in PROC.PROCESSES:
        return None
    return "A burn takes nights of watching; left, it flares to ash."


def WO4(c):
    """[built: coppice] (W-76): no coppice cycle in the woods yet, so the line waits."""
    from cybertron2.engine.data import FORESTS
    if "coppice" not in FORESTS["kinds"]:
        return None
    return "A coppice cut over in its turn gives poles and withies again; the standards left to grow give timber for building."


def WO5(c):
    """A fuel-hungry household within 2 days: a salt house (`boil salt` burns firewood) or a forge (`smelt` burns charcoal)."""
    from cybertron2.engine.data import TECHNIQUES as T
    near = dict([(c.node, 0)] + _reach(c, 2))
    for hh in c.rep["households"]:
        if hh == c.hh or _hh_node(c, hh) not in near:
            continue
        holds, _ = c.holdings(hh)
        want = []
        if holds.get("salt house") and T["boil salt"]["inputs"].get("firewood"):
            want.append("firewood for the pan")
        if holds.get("forge") and T["smelt"]["inputs"]["fuel"].get("charcoal"):
            want.append("charcoal for the forge")
        if want:
            d = near[_hh_node(c, hh)]
            at = " here" if not d else f", {_days_words(d)} off,"
            return f"The {c.line_name(hh)}{at} want {_and(want)}."
    return None


# the basket maker (u9 §5.5.11)
def BA1(c):
    """`cut withies`' season and willow's summer harm (wild/willow.py WILLOW summer_harm)."""
    from cybertron2.engine.data import TECHNIQUES as T
    from cybertron2.wild.willow import WILLOW
    by = T["cut withies"]["by_season"]
    harm = ", and summer cutting harms the stools" if float(WILLOW.get("summer_harm", 0)) > 0 else ""
    return f"Willow rods cut in winter, when the sap is down, give the most: {_by_season_words(by).split(', ', 1)[1]}{harm}."


def BA2(c):
    """[built: hurdles' uses]: hurdles are made (gear.RECIPES) but nothing folds beasts or fences with them yet, so the line waits."""
    from cybertron2.engine.data import TECHNIQUES as T
    if not any("hurdle" in str(t.get("inputs") or {}) or "hurdle" in str((t.get("yield") or {}).get("fence", "")) for t in T.values()):
        return None
    return "Hurdles of withies fold beasts and fence a garden, and are lighter to move than posts and rails."


def BA3(c):
    """The creel's and the pack basket's carry (gear ITEMS creel carry; ITEMS pack carry) over the carry on foot."""
    from cybertron2.engine import gear as GE
    from cybertron2.engine.data import ITEMS, PHYSICS
    foot = float(PHYSICS["carry"]["foot"])
    return (f"A creel carries the catch on the back, {float(GE.ITEMS['creel']['carry']):g} kilos more than the hands; a pack basket "
            f"carries about {foot + float(ITEMS['pack']['carry']):g} kilos where hands carry {foot:g}.")


def BA4(c):
    """[built: the withy bed] (U7): a planted bed is stage 5's (wild/willow.py), so the line waits."""
    from cybertron2.engine.data import FITTINGS, MONUMENTS, TECHNIQUES
    if not any("withy bed" in t for t in (MONUMENTS, FITTINGS, TECHNIQUES)):
        return None
    return "A withy bed takes three years to bear and then gives for thirty, if beasts are kept off it."


def BA5(c):
    """[keeps a withy bed] (protected): the bed's year and fence are its record (U7), which does not exist yet; waits with BA4."""
    if BA4(c) is None or not _kept_refs(c, "withy bed"):
        return None
    return None                                                          # the bed's record (its year, its fence) is U7's, not built


# cord and nets (u9 §5.5.12)
def CO1(c):
    """`twist cord`'s rate a unit and season; a summer day's units (PHYSICS units)."""
    from cybertron2.engine.data import PHYSICS, TECHNIQUES as T
    t = T["twist cord"]
    days = 1.0 / (float(t["yield"]["base"]) * float(PHYSICS["units"]["summer"]))
    return (f"Nettle and bast twisted into cord give {_by_season_words(t['by_season'])}; it is slow work, a kilo in about "
            f"{round(days)} days.")


def CO2(c):
    """Flax as a strip crop (CROPS flax strip, takes against grain's), pulled by the root (`pull flax`)."""
    from cybertron2.engine.data import CROPS
    fx = CROPS.get("flax")
    if not fx or not _has_fields(c):
        return None
    like = " as barley does" if abs(float(fx["takes"]) - float(CROPS["grain"]["takes"])) < 1e-9 else ""
    return (f"Flax is sown in a strip of a field, up to {_share_words(fx['strip'])} of a plot, and pulled by the root; it tires the "
            f"ground{like}, and gives the fibre for cord.")


def CO3(c):
    """[built: pollution from retting] (U10): retting fouls no water in the engine yet, so the line waits."""
    from cybertron2.engine import process as PROC
    if not any(k in (PROC.PROCESSES.get("retting") or {}) for k in ("fouls", "pollution", "foul")):
        return None
    return "Retted in the river, flax fouls the water for the fishers below; retted on the grass or in a pit, it fouls nothing."


def CO4(c):
    """Retting's nights in water and on the grass (process.PROCESSES retting), `dress and spin` under a roof, its retted flax a kilo of
    cord."""
    from cybertron2.engine import process as PROC
    from cybertron2.engine.data import TECHNIQUES as T
    r = PROC.PROCESSES.get("retting")
    if not r:
        return None
    n = r["nights"]
    per = 1.0 / float(T["dress and spin"]["gives"]["cord"])
    roof = " under a roof" if (T["dress and spin"].get("at") or {}).get("building") else ""
    return (f"Pulled flax is retted {_days_words(n['water']).replace('day', 'night')} in still water or {n['dew']} on the grass, then "
            f"dressed and spun{roof}; about {per:g} kilos of retted flax make a kilo of cord.")


def CO5(c):
    """`gill nets`' cord (gear.RECIPES) and the net's rot in the water (gear.LIVES gill net: world years wet, a year of 32 nights)."""
    from cybertron2.engine import gear as GE
    cord = float(GE.RECIPES["gill nets"]["inputs"]["cord"])
    wet = (GE.LIVES["gill net"].get("rot") or (None, None))[0]
    if not wet:
        return None
    nights = round(float(wet) * 4 * _season_days(c))
    return (f"A gill net wants {'a kilo' if cord == 1 else f'{cord:g} kilos'} of cord and many evenings' knotting; in the water it rots "
            f"in about {nights} nights, so the fishers want nets again and again.")


# the trader or carrier (u9 §5.5.14)
def TR1(c):
    """The villages within 2 days: what their households' livelihoods give and need (ROWS depends), up to three while within 40
    words."""
    from cybertron2.engine.livelihoods import ROWS
    bits = []
    for nid, d in _reach(c, 2):
        hhs = _hhs_at(c, nid)
        if not hhs:
            continue
        gives = [g for hh in hhs for lv in _livs(c, hh)[:1] for g in ROWS[lv]["depends"]["gives"]
                 if g not in ("labour", "carrying", "rooms", "hearths")]
        needs = [g for hh in hhs for lv in _livs(c, hh)[:1] for g in ROWS[lv]["depends"]["needs"] if g not in gives]
        gives, needs = list(dict.fromkeys(gives)), list(dict.fromkeys(needs))
        if not gives and not needs:
            continue
        bit = f"{_node_name(c, nid)}, {_days_words(d)} off, has {_and(gives) or 'little'}" + (f", and lacks {_and(needs)}" if needs else "")
        if _words("; ".join(bits + [bit]) + ".") <= LINE_WORDS and len(bits) < 3:
            bits.append(bit)
    return ("; ".join(bits) + ".") if bits else None


def TR2(c):
    """The pack ox's carry and its grazing (HERDS pack_ox), the carry on foot, the handcart's carry on a track (ITEMS handcart)."""
    from cybertron2.engine.data import HERDS, ITEMS, PHYSICS
    foot = float(PHYSICS["carry"]["foot"])
    ox = float(HERDS["pack_ox"]["carry"])
    cart = foot + float(ITEMS["handcart"]["carry"])
    track = ITEMS["handcart"].get("track")
    return (f"A pack ox carries about {ox:g} kilos where one on foot carries {foot:g}, but wants grazing on the way; a handcart carries "
            f"about {cart:g}" + (" on a road with a track, and is no use off one." if track else "."))


def TR3(c):
    """The roads from home: their days, their way and a landmark on them (world `roads`)."""
    bits = []
    for r in c.world.get("roads") or []:
        if c.node not in (r[0], r[1]):
            continue
        other = r[1] if r[0] == c.node else r[0]
        info = r[3] if len(r) > 3 else {}
        lm = [x for st in (info.get("stretches") or {}).values() for x in st.get("landmarks") or []]
        bit = f"the road to {_node_name(c, other)} is {_days_words(r[2])}" + (f", {info['way']}" if info.get("way") else "")
        bit += f", with a {lm[0]} on it" if lm else ""
        if _words("; ".join(bits + [bit]) + ".") <= LINE_WORDS:
            bits.append(bit)
    if not bits:
        return None
    t = "; ".join(bits) + "."
    return t[:1].upper() + t[1:]


def TR4(c):
    """The region's chokepoints: where salt (a brine spring or saltmarsh), copper ore (a seam) and stone (a quarry) come from."""
    srcs = {"salt": [], "copper ore": [], "stone": []}
    for nid, n in c.world["nodes"].items():
        for pid, p in (n.get("parcels") or {}).items():
            st = p.get("state") or {}
            if p.get("cover") == "saltmarsh" or "brine" in st or p.get("spring") == "brine":
                srcs["salt"].append(_node_name(c, nid))
            if (st.get("seam") or {}).get("K"):
                srcs["copper ore"].append(_node_name(c, nid))
            if (st.get("quarry") or {}).get("K"):
                srcs["stone"].append(_node_name(c, nid))
    by = {}
    for g, v in srcs.items():                                            # goods that come from the same places said together
        if v:
            by.setdefault(tuple(sorted(set(v))), []).append(g)
    bits = [f"{_and(gs)} only at {_and(list(places))}" for places, gs in by.items()]
    if not bits:
        return None
    return f"Some goods are made in few places and wanted in all: {'; '.join(bits)}."


# the cottager (u9 §5.5.15)
def _common(c):
    return next((p["name"] for p in c.parcels.values() if p.get("cover") == "pasture" and not p.get("holder")), None)


def CT1(c):
    """The household's holdings: no field held; the common (unheld pasture) and the wild."""
    if _held(c, c.hh, "field"):
        return None
    common = _common(c)
    return ("We hold a cottage and no field; we live by work for others, for food or coin, and by what "
            + (f"{common} and the wild give." if common else "the wild gives."))


def _water_of(c, hh):
    nid = _hh_node(c, hh)
    return next((p["name"] for p in ((c.world["nodes"].get(nid) or {}).get("parcels") or {}).values() if p.get("cover") == "water"), None)


_BUSY = {"farmer": "reaping", "herder": "haymaking", "fisher": "the eel run", "miller": "the milling"}


def _busy_season(c, lv, hh):
    """The season a livelihood wants hands (engine reads): the harvest (farm), hay's best season (`hay` by_season), the eel run
    (RUNS eel), the milling after the harvest."""
    from cybertron2.engine.data import TECHNIQUES as T
    holds, _ = c.holdings(hh)
    if lv == "farmer" and not holds.get("fields") or lv == "miller" and not holds.get("mill") or lv == "herder" and not holds.get("herd"):
        return None
    if lv in ("farmer", "miller"):
        s = _harvest_seasons(c)
        return s[0] if s else None
    if lv == "herder":
        by = T["hay"]["by_season"]
        return max(SEASON_NAMES, key=lambda s: float(by.get(s, 0)))
    if lv == "fisher":
        return _eel_season(c) if _water_of(c, hh) and _runs_at(c.world, _hh_node(c, hh), "eel") else None
    return None


def CT2(c):
    """The neighbours' busy seasons (by their core livelihood), up to two."""
    bits = []
    for hh in c.rep["households"]:
        if hh == c.hh or _hh_node(c, hh) not in [c.node] + [n for n, _ in _reach(c, 1)]:
            continue
        lv = (_livs(c, hh) or [None])[0]
        s = _busy_season(c, lv, hh) if lv in _BUSY else None
        if s and len(bits) < 2:
            bits.append(f"the {c.line_name(hh)} at {_BUSY[lv]} in {s}")
    if not bits:
        return None
    return f"Hands are wanted at the busy times: {_and(bits)}."


def CT3(c):
    """The common's grazing (an unheld pasture: PHYSICS cattle grazing) and its wild food (`gather wild food`'s covers)."""
    common = _common(c)
    if not common:
        return None
    return f"What {common} gives, grass for a beast and wild food at its edges, sees us through when the work fails."


def CT4(c):
    """[built: spinning, baskets]: `dress and spin` and the basket (gear.RECIPES); winter's fewer units (PHYSICS units)."""
    from cybertron2.engine import gear as GE
    from cybertron2.engine.data import PHYSICS
    u = PHYSICS["units"]
    if not _built_technique("dress and spin") or "basket" not in GE.RECIPES or not u["winter"] < u["summer"]:
        return None
    return "In winter, when the days are short and work is thin, we spin and make baskets for those who will take them."


def FI13(c):
    """[built: withies, cord, bone]: nothing gives bone yet (bone hooks), so the line waits."""
    if not _built_bone():
        return None
    return ("A rod wants a straight withy, and takes more than a hand line. Bone hooks serve; copper hooks come from the smith.")


def FI14(c):
    """[built: dressing, bait]: no technique dresses the catch or baits the traps with its guts yet, so the line waits."""
    if not _built_technique("dress fish", "gut fish", "dress the catch"):
        return None
    return "A fish gutted and split the day it is caught dries in the rack; one left whole goes soft. The guts bait the traps."


# the neighbours' lines (u9 §5.5, §5.7): one a livelihood, read from the household's own holdings where it names them
def _nb_farmer(c, hh):
    f = next((p["name"] for _, p in _held(c, hh, "field")), None)
    return f"The {c.line_name(hh)} sow and reap {f or 'their fields'}; they have grain after harvest and want hands at reaping."


def _nb_herder(c, hh):
    hs = _herds_of(c, hh)
    if not hs:
        return f"The {c.line_name(hh)} keep cattle; they have milk."
    hid, h = hs[0]
    p = next((n["parcels"][h["parcel"]] for n in c.world["nodes"].values() if h.get("parcel") in (n.get("parcels") or {})), {})
    oxen = ", and oxen for the plough" if any(int(x.get("oxen", 0)) > 0 for _, x in hs) else ""
    return f"The {c.line_name(hh)} keep their cattle on {p.get('name', 'the common')}; they have milk{oxen}."


def _nb_hunter(c, hh):
    nid = _hh_node(c, hh)
    wood = next((p["name"] for p in (c.world["nodes"].get(nid) or {}).get("parcels", {}).values() if p.get("cover") == "forest"), None)
    return f"The {c.line_name(hh)} hunt {wood or 'the woods'}; they bring home meat and hides."


def _nb_smith(c, hh):
    return f"The {c.line_name(hh)} work copper at their forge; they make tools and hooks, and want charcoal."


def _nb_miller(c, hh):
    holds, _ = c.holdings(hh)
    m = next((c.world["buildings"][b].get("name") for b in holds.get("mill") or []), None)
    return f"The {c.line_name(hh)} keep {m or 'the mill'}; bring them grain after harvest and they grind it."


def _nb_trader(c, hh):
    hr = c.rep["households"].get(hh) or {}
    who = next(iter(hr.get("second_hands") or []), None) or next((n for n in c.members(hh) if c.world["agents"][n].get("role") == "head"), None)
    home = _hh_node(c, hh)
    dist = _road_days(c.world).get(home) or {}
    other = next((n for n, d in sorted(dist.items(), key=lambda x: (x[1], x[0])) if n != home and d <= 2), None)
    if not who or not other:
        return None
    return (f"{who} of the {c.line_name(hh)} carries between {_node_name(c, home)} and {_node_name(c, other)}; ask them for what is not "
            "made here.")


def _nb_fisher(c, hh):
    """A fisher neighbour: their own water, and the eel run only where it passes them (`_runs_at`)."""
    water = _water_of(c, hh) or "the water"
    if _runs_at(c.world, _hh_node(c, hh), "eel"):
        return (f"The {c.line_name(hh)} live by {water}: they know when the eels run, and dry and salt the catch; in "
                f"late {_eel_season(c)} they have fish to spare.")
    return f"The {c.line_name(hh)} live by {water}: they fish it, and dry and salt the catch."


def _knows_village(c, nid) -> bool:
    """Whether the founder's household knows of a place (D4-47, as World.knows_place): it is not unexplored, or one of the household
    has it among their places."""
    if not (c.world["nodes"].get(nid) or {}).get("unexplored"):
        return True
    return any(nid in (c.world["agents"][m].get("places") or []) for m in c.members())


def NV(c, lv, hh):
    """D2-349: a household in another village one's household knows of: that village, how far, and what they live by; only for a
    living that gives others something (its row's `depends.gives`), since that is why a household far off is worth knowing."""
    from cybertron2.engine.livelihoods import ROWS
    r = ROWS.get(lv) or {}
    on = _hh_node(c, hh)
    if not (r.get("depends") or {}).get("gives") or on is None:
        return None
    d = (_road_days(c.world).get(c.node) or {}).get(on)
    away = "" if d is None else (", a day away" if d <= 1 else f", {d:g} days away")
    lives = re.sub(r"\byour\b", "their", r["words"]["lives"])            # the row's words are the person's own ("your garden")
    return f"In {_node_name(c, on)}{away}, the {c.line_name(hh)} live by {lives}."


NB = {"fisher": _nb_fisher,
      "salter": lambda c, hh: f"The {c.line_name(hh)} boil salt at the spring; they want firewood for the pan.",
      "farmer": _nb_farmer,
      "herder": _nb_herder,
      "hunter": _nb_hunter,
      "smith": _nb_smith,
      "miller": _nb_miller,
      "builder": lambda c, hh: f"The {c.line_name(hh)} build: a frame, a wheel or a hearth is their work.",
      "woodsman": lambda c, hh: f"The {c.line_name(hh)} work the wood; they have charcoal, timber and firewood.",
      "basket maker": lambda c, hh: f"The {c.line_name(hh)} cut the willow; they make traps, creels and baskets for those who need them.",
      "cord and nets": lambda c, hh: f"The {c.line_name(hh)} twist cord and knot nets; the fishers get their nets from them.",
      "trader": _nb_trader,
      "cottager": lambda c, hh: f"The {c.line_name(hh)} work for whoever needs hands."}


def HL(c):
    """The household's holdings line (u9 §5.6): every holding and its keeper, then a fact clause each while within 40 words."""
    holds, keepers = c.holdings()
    if not holds:
        return None
    names, facts = [], []
    from cybertron2.engine.data import FITTINGS
    for kind in ("weir", "salt house", "smokehouse", "mill", "oven", "forge"):
        for bid in holds.get(kind) or []:
            b = c.world["buildings"][bid]
            who = keepers.get(bid)
            parcel = c.parcels.get(b["parcel"], {}).get("name", "")
            if kind == "weir":
                names.append(f"the weir on {parcel}, which {who} keeps")
                facts.append("its traps take the run when its gap is shut")
            elif kind == "smokehouse":
                cap = int((b.get("fittings") or {}).get("smoke racks", 1)) * float(FITTINGS["smoke racks"]["holds_kg"])
                names.append(f"{b.get('name', 'the smokehouse')} on {parcel}, which {who} keeps")
                facts.append(f"it holds about {cap:g} kilos of fish at a time")
            elif kind == "salt house":
                names.append(f"{b.get('name', 'the salt house')} on {parcel}, where {who} boils salt")
                facts.append("the pan wants copper when it wears through")
            elif kind == "mill":
                names.append(f"{b.get('name', 'the mill')} on {parcel}, which {who} keeps")
                facts.append("it grinds the grain brought to it; its stones and leat want care")
            elif kind == "oven":
                names.append(f"{b.get('name', 'the oven')}, where {who} bakes")
                facts.append("it wants firewood at each firing and relining in time")
            elif kind == "forge":
                names.append(f"{b.get('name', 'the forge')}, where {who} works copper")
                facts.append("it burns charcoal")
            else:
                names.append(f"{b.get('name', kind)}, which {who} keeps")
    fields = holds.get("fields") or []                                   # the holdings that are not buildings (u9 §5.6; u11 §2.1)
    if fields:
        fp = [next(n["parcels"][r.split(":", 1)[1]] for n in c.world["nodes"].values() if r.split(":", 1)[1] in (n.get("parcels") or {}))
              for r in fields]
        who = _and(sorted({keepers.get(r) for r in fields if keepers.get(r)}))
        names.append(f"{_and([p['name'] for p in fp])}, which {who} sees to")
        facts.append("seed must be kept back for them")
    for ref in holds.get("ox pair") or []:
        names.append(f"the ox team and plough, which {keepers.get(ref)} keeps")
        facts.append("they break the ground far faster than a hoe")
    for ref in holds.get("herd") or []:
        from cybertron2.engine import farm as FM
        h = (c.world.get("herds") or {})[ref.split(":", 1)[1]]
        p = next((n["parcels"][h["parcel"]] for n in c.world["nodes"].values() if h.get("parcel") in (n.get("parcels") or {})), {})
        names.append(f"{FM.head(h)} beasts on {p.get('name', 'the common')}, which {keepers.get(ref)} herds")
        facts.append("they want hay through the winter")
    if all(keepers.get(bid) == c.name for bids in holds.values() for bid in bids):
        return None                                                      # the keeper of all of them has their keeper lines
    head = "We hold " + (", and ".join([", ".join(names[:-1]), names[-1]]) if len(names) > 1 else names[0]) + "."
    got = []
    for f in facts:                                                      # one fact clause a holding while the line stays in 40 words
        cand = head + " " + "; ".join(got + [f]) + "."
        if _words(cand) <= LINE_WORDS:
            got.append(f)
    text = head + (" " + "; ".join(got) + "." if got else "")
    return text[:len(head) + 1] + text[len(head) + 1:len(head) + 2].upper() + text[len(head) + 2:] if got else text


PREFIXES = ("BS", "PE", "HH", "FI", "SA", "FA", "HE", "HU", "SM", "MI", "BU", "WO", "BA", "CO", "TR", "CT")   # FO, TA deferred
TEMPLATES = {k: v for k, v in globals().items() if k[:2] in PREFIXES and callable(v) and k[2:].isdigit()}
TEMPLATES["HL"] = HL
SOURCE = {**{p: "family lore" for p in PREFIXES}, "NB": "family lore", "NV": "family lore", "HL": "a holding"}
KEEPER = {"FI12", "FI17", "SA4", "FA7", "FA9", "HE7", "SM4", "MI3", "MI5", "BA5"}     # each holding's keeper line (livelihoods.HOLDINGS)
# u9 §5.2's drop order: each step taken whole, stopping as soon as the set fits
DROP = [("other villages' households", lambda ids: [i for i in ids if i.startswith("NV")]),     # D2-349: before any neighbour
        ("neighbours beyond one", lambda ids: [i for i in ids if i.startswith("NB")][1:]),
        ("PE2", lambda ids: [i for i in ids if i == "PE2"]),
        ("HH5", lambda ids: [i for i in ids if i == "HH5"]),
        ("HH4", lambda ids: [i for i in ids if i == "HH4"]),                 # W-105 default: the stores line goes with the book's (Q)
        ("HH8", lambda ids: [i for i in ids if i == "HH8"]),
        ("capable lines a specialism repeats", lambda ids: (["FI3"] if "FI16" in ids and "FI3" in ids else [])
         + (["FA3"] if "HH2" in ids and "FA3" in ids else [])),             # W-105 default: HH2 gives the house's own seed (Q)
        ("broad lines of a second living beyond its first", None),
        ("BS9", lambda ids: [i for i in ids if i == "BS9"]),
        ("BS7", lambda ids: [i for i in ids if i == "BS7"]),
        ("BS6", lambda ids: [i for i in ids if i == "BS6"]),
        ("the last neighbour line", lambda ids: [i for i in ids if i.startswith("NB")]),
        ("BS8, when HH10 is held", lambda ids: ["BS8"] if "HH10" in ids and "BS8" in ids else [])]   # D2-340: the line split in two


def keeper_line(kind, livs=()):
    """The keeper line of a kind of holding (u9 §5.6; u11 §2.1): the first of the household's livelihood rows that names one
    (`keeper_lines`), else the holdings registry's (`HOLDINGS[kind]["keeper_line"]`); None for a holding with none."""
    from cybertron2.engine.livelihoods import HOLDINGS, ROWS
    if not kind:
        return None
    for lv in livs:
        kl = ((ROWS.get(lv) or {}).get("keeper_lines") or {}).get(kind)
        if kl:
            return kl
    return (HOLDINGS.get(kind) or {}).get("keeper_line")


def wanted(world, name, rep) -> list:
    """The ids a founder is given before the cap (u9 §5.2; u11 §7 step 9): base, people, head's, the livelihood's by band, the
    specialism's, the keeper's, the household's holdings line, a second living's, neighbours."""
    from cybertron2.engine.livelihoods import ROWS
    a = world["agents"][name]
    st = a.get("stage")
    if st in ("infant",):
        return []
    hh = a.get("household")
    hr = rep["households"].get(hh) or {}
    livs = hr.get("livelihoods") or []
    band = hr.get("bands", {}).get(name, "broad")
    ids = []
    if st == "child":                                                     # as if passed by a carer: the first broad line and HL
        if livs:
            ids += (ROWS[livs[0]]["lines"].get("youth") or [])[:1]
        return ids + ["HL"]
    if st == "youth":
        ids += ["BS1", "BS2", "BS3", "BS5", "BS8", "PE1"]
        if livs:
            ids += ROWS[livs[0]]["lines"].get("youth") or []
        sp = (hr.get("apprentices") or {}).get(name)
        if sp and livs:
            if sp in ROWS[livs[0]]["specialisms"]:
                ids += ROWS[livs[0]]["specialisms"][sp]["lines"][:1]
        return ids + ["HL"]
    ids += ["BS%d" % i for i in range(1, 10)] + ["PE1", "PE2"]
    if st == "elder":
        ids.append("PE3")
    head = a.get("role") == "head"
    partner = any(world["agents"].get(x, {}).get("role") == "head" and world["agents"][x].get("partner") == name for x in world["agents"])
    if head:
        ids += ["HH1", "HH2", "HH3", "HH4", "HH5", "HH6", "HH7", "HH8", "HH9"]
    elif partner:
        ids += ["HH1", "HH3"]
    if head or _parent(world, name):                                      # passing on through care (D2-340)
        ids.append("HH10")
    for j, lv in enumerate(livs[:1]):
        r = ROWS[lv]
        ids += r["lines"].get("broad") or []
        if band == "capable":                                             # u9 §5.5.1 by role: an expert has the broad lines and
            ids += r["lines"].get("capable") or []                        # their specialism's
        sp = next((s for s, who in (hr.get("experts") or {}).items() if who == name), None)
        if sp:
            ids += r["specialisms"][sp]["lines"]
        elif band == "capable" and hr.get("experts"):
            s0 = next(iter(hr["experts"]))
            ids += r["specialisms"][s0]["lines"][:1]
    keepers = hr.get("keepers") or {}
    holds = hr.get("holds") or {}
    for bid, who in keepers.items():                                      # each holding's keeper line: the household's livelihood
        if who == name:                                                   # row's `keeper_lines`, else the holdings registry's
            kl = keeper_line(next((k for k in holds if bid in (holds.get(k) or [])), None), livs)
            if kl:
                ids.append(kl)
    for lv in livs[1:2]:
        if name in (hr.get("second_hands") or []):
            ids += ROWS[lv]["lines"].get("second") or []
    ids.append("HL")
    c = Ctx(world, name, rep, rep["households"].get(hh) or {})
    for oh, orep in rep["households"].items():                            # D2-349: by where the other household lives
        if oh == hh or not orep.get("livelihoods"):
            continue
        on = _hh_node(c, oh)
        if on == c.node:
            ids.append(f"NB-{orep['livelihoods'][0]}:{oh}")                # a neighbour, in one's own village
        elif on is not None and _knows_village(c, on) and ((ROWS.get(orep["livelihoods"][0]) or {}).get("depends") or {}).get("gives"):
            ids.append(f"NV-{orep['livelihoods'][0]}:{oh}")                # in another village the household knows of
    return list(dict.fromkeys(ids))


def render(world, name, rep, ids=None) -> dict:
    """{id: text} for a founder's wanted ids, each filled from the state; a false condition drops the line (reported), never a
    stand-in (D2-268; u11 departure 2)."""
    c = Ctx(world, name, rep, rep["households"].get(world["agents"][name].get("household")) or {})
    out, skipped = {}, []
    for i in ids if ids is not None else wanted(world, name, rep):
        if i.startswith("NB-"):
            lv, _, hh = i[3:].partition(":")
            f = NB.get(lv)
            t = f(c, hh) if f else None
        elif i.startswith("NV-"):
            lv, _, hh = i[3:].partition(":")
            t = NV(c, lv, hh)
        elif i in TEMPLATES:
            t = TEMPLATES[i](c)
        else:
            t = None
        if t:
            out[i] = t
        else:
            skipped.append(i)
    return {"lines": out, "skipped": skipped}


def protected(world, name, ids) -> set:
    a = world["agents"][name]
    keep = {"PE1", "HL"} | (KEEPER & set(ids)) | ({"HH10"} & set(ids))       # D2-340
    if a.get("role") == "head":
        keep |= {"HH1", "HH3", "HH7", "HH9"}
    else:
        keep |= {"HH1", "HH3"} & set(ids)
    return keep


def cap(world, name, lines: dict) -> tuple:
    """u9 §5.2's cap: 20 lines and about 800 words; the drop order taken step by step, each whole, stopping when the set fits; the
    protected lines never dropped. Returns (kept ids, the steps taken, over: still over the cap after the last step: P5)."""
    from cybertron2.engine.livelihoods import ROWS
    ids = list(lines)
    prot = protected(world, name, ids)
    steps = []

    def fits():
        return len(ids) <= CAP_LINES and sum(_words(lines[i]) for i in ids) <= CAP_WORDS
    for label, pick in DROP:
        if fits():
            break
        if pick is None:                                                  # a second living's broad lines beyond its first, when one
            a = world["agents"][name]                                     # holds a deeper band in the core living
            livs = a.get("livelihoods") or []
            if len(livs) > 1:
                sec = ROWS[livs[1]]["lines"].get("second") or []
                drop = [i for i in sec[1:] if i in ids and i not in prot and i not in (ROWS[livs[0]]["lines"].get("broad") or [])]
            else:
                drop = []
        else:
            drop = [i for i in pick(ids) if i not in prot]
        if drop:
            ids = [i for i in ids if i not in drop]
            steps.append(label)
    return ids, steps, not fits()


def seed_world(world, rep, seed=0) -> dict:
    """Step 9 (u11 §4.2): each founder's lines rendered, capped and written to their `kept` with their sources, unless the world turns
    the seeded lines off (`skills.depth: none`, D2-331's comparison arm)."""
    depth = (world.get("skills") or {}).get("depth", "full")
    out = {}
    for name, a in sorted(world["agents"].items()):
        if a.get("household") not in rep["households"]:
            continue
        r = render(world, name, rep)
        ids, steps, over = cap(world, name, r["lines"])
        long = [i for i in ids if _words(r["lines"][i]) > LINE_WORDS]
        out[name] = {"wanted": len(r["lines"]) + len(r["skipped"]), "rendered": len(r["lines"]), "skipped": r["skipped"],
                     "steps": steps, "seeded": len(ids), "words": sum(_words(r["lines"][i]) for i in ids), "over": over, "long": long,
                     "ids": ids}
        if depth == "none":
            continue
        a["kept"] = [{"text": r["lines"][i], "source": "a holding" if i == "HL" or i in KEEPER else SOURCE.get(i[:2], "family lore")}
                     for i in ids]
    return out
