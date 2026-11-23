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
    return ("Winter is the hungry time: " + ("the fields give nothing, " if _has_fields(c) else "") + "the wild little, a cold night "
            "burns about three times the fuel" + (", and wolves come to the herds" if _wolves(c) else "") + ". What a house eats and burns "
            "through winter must be in by autumn's end.")


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


def HH3(c):
    return ("Fresh fish and meat go first or go off; what is dried, smoked, salted or in grain keeps. In a hungry spring the keeping food "
            "is what is left: eat the soft first, by rule if need be.")


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
    if water and fisher:
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
    if not river:
        return None
    cue = ("on the dark nights of the season" if c.world.get("runs_set_nights") else "on dark wet nights, most on the first rain after dry days")
    return f"The eels go down to the sea in {_eel_season(c)}, {cue}. {river[:1].upper() + river[1:]} can look empty all summer and still run thick then."


def FI2(c):
    from cybertron2.engine.data import WATER_WORKS
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
    return (f"A spate smashes {half} the traps in the water, and a flood nearly all; an otter that finds full traps comes back each night. "
            "When the water drops, set again: the run is not over.")


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


def _runs_here(c, kind):
    """Whether a run passes the village (read from the world's land: the river class; salmon only on a big river)."""
    p = next((p for p in c.parcels.values() if p["cover"] == "water"), None)
    land = (p or {}).get("land") or {}
    if kind == "salmon":
        return land.get("river_class") in ("large", "big") or land.get("river") == "big river"
    if kind == "lamprey":
        return bool(c.world.get("lampreys"))
    return True


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
    if not b:
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


NB = {"fisher": lambda c, hh: f"The {c.line_name(hh)} live by {c.water() or 'the water'}: they know when the eels run, and dry and salt the catch; in late autumn they have fish to spare.",
      "salter": lambda c, hh: f"The {c.line_name(hh)} boil salt at the spring; they want firewood for the pan.",
      "farmer": lambda c, hh: f"The {c.line_name(hh)} sow and reap the big field; they have grain after harvest and want hands at reaping.",
      "herder": lambda c, hh: f"The {c.line_name(hh)} keep the cattle on the common; they have milk in summer and oxen to lend for the plough."}


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
            else:
                names.append(f"{b.get('name', kind)}, which {who} keeps")
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


TEMPLATES = {k: v for k, v in globals().items() if k[:2] in ("BS", "PE", "HH", "FI", "SA") and callable(v) and k[2:].isdigit()}
TEMPLATES["HL"] = HL
SOURCE = {"BS": "family lore", "PE": "family lore", "HH": "family lore", "FI": "family lore", "SA": "family lore", "NB": "family lore",
          "HL": "a holding"}
KEEPER = {"FI12", "FI17", "SA4"}
# u9 §5.2's drop order: each step taken whole, stopping as soon as the set fits
DROP = [("neighbours beyond one", lambda ids: [i for i in ids if i.startswith("NB")][1:]),
        ("PE2", lambda ids: [i for i in ids if i == "PE2"]),
        ("HH5", lambda ids: [i for i in ids if i == "HH5"]),
        ("HH8", lambda ids: [i for i in ids if i == "HH8"]),
        ("capable lines a specialism repeats", lambda ids: ["FI3"] if "FI16" in ids and "FI3" in ids else []),
        ("broad lines of a second living beyond its first", None),
        ("BS9", lambda ids: [i for i in ids if i == "BS9"]),
        ("BS7", lambda ids: [i for i in ids if i == "BS7"]),
        ("BS6", lambda ids: [i for i in ids if i == "BS6"]),
        ("the last neighbour line", lambda ids: [i for i in ids if i.startswith("NB")]),
        ("BS8, when HH10 is held", lambda ids: ["BS8"] if "HH10" in ids and "BS8" in ids else [])]   # D2-340: the line split in two


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
        ids += ["HH1", "HH3", "HH5", "HH6", "HH7", "HH8", "HH9"]
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
    for bid, who in keepers.items():
        if who == name:
            b = world["buildings"][bid]
            if b.get("monument") == "weir":
                ids.append("FI12")
            elif (b.get("fittings") or {}).get("smoke racks"):
                ids.append("FI17")
            elif (b.get("fittings") or {}).get("brine pan"):
                ids.append("SA4")
    for lv in livs[1:2]:
        if name in (hr.get("second_hands") or []):
            ids += ROWS[lv]["lines"].get("second") or []
    ids.append("HL")
    for oh, orep in rep["households"].items():
        if oh != hh and orep.get("livelihoods"):
            ids.append(f"NB-{orep['livelihoods'][0]}:{oh}")
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
