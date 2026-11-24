"""How people answer the wild: general methods, not a technique per kind (D2-204; proposals/methods_and_encounters.md, brief 1).

Each method is a TECHNIQUES row of the engine's usual shape (verb, label, aliases, `at`, units, `crew`, `gear`, `untaught`,
`reads_as`, `yield`), with two fields read only here, at load: `needs` (traits a target must have) and `favours` (traits that raise
the match, by a factor). `build` writes each method's `yield.takes` from them against the kinds' traits (kinds.TRAITS), so
`wild.take` runs as before on a generated table. No method row names a kind; a kind's own row may carry `taken.calibrate:
{method: x}` (at most one, with a comment).

Who knows what (§6): the basic methods are known to all; the others by the land a household lives on (`seed_by_land`, at world
build): a kind or site within the village's ring that the method can take. Familiarity by kind (§5) is the second layer of skill:
`familiar(mind, kind)`, raised by taking the kind, noticing its signs and being taught; kept in the person's mind store.
"""
from __future__ import annotations

SIZES = ("tiny", "small", "medium", "large")
HUNT_COVERS = ["forest", "scrub", "heath", "moor", "fen", "pasture", "meadow"]
FIELD_COVERS = ["field", "pasture", "meadow", "forest", "scrub"]

# The scares a guard can hold, in the order it reaches for them unless `looking for` names one (D2-204: the four watches' rows).
SCARES = [
    {"scare": "fire", "with": "a fire", "uses": {"firewood": 2}, "burns": {"firewood": 2}, "names": ["fire", "a fire", "firewood"]},
    {"scare": "clapper", "with": "clappers", "uses": {"clappers": 1}, "names": ["clappers", "clapper"]},
    {"scare": "horn", "with": "a horn", "uses": {"horn": 1}, "names": ["horn", "a horn"]},
    {"scare": "dog", "with": "the dog", "home_fittings": ["dog"], "names": ["dog", "the dog"]},
]


def _take_row(label, aliases, covers, needs, favours, base, gear, units, note, basic=False, untaught=True, crew=False, when=None):
    row = {"verb": "gather", "label": label, "aliases": aliases, "basic": basic, "pack": "wild", "at": {"covers": covers},
           "draws": "wild", "reads_as": ["hunt"], "needs": needs, "favours": favours, "base": base,
           "yield": {"kind": "wild_take", **({"when": when} if when else {})}, "gear": gear, "wear": 0.3, "units": units,
           "gives": "meat", "tags": ["food", "hunting", "animals"], "note": note}
    if not basic and untaught:
        row["untaught"] = "tryable"
    if crew:
        row["crew"] = True
    return row


# the nights things run (brief 1), where no river runs at the village: where one does, the run itself is the take's density (brief 5 §2.4)
EEL_NIGHTS = [{"if": {"seasons": {2: (0, 7)}, "river_run": False}, "x": 2.0, "for": {"mover": "run"}},
              {"if": {"rain_after_dry": 2, "seasons": {2: (0, 7)}, "river_run": False}, "x": 3.0, "for": {"mover": "run"}}]

METHODS = {
    # the key is the old hunt's: "hunt" is the hunt of worlds without the wild pack (off_with wild), still read by older worlds
    "hunt the wild": _take_row(
        "hunting in the wild, taking what comes",
        ["hunt", "hunting", "go hunting", "hunt the wood", "hunting the wild", "hunt in the wild"],
        HUNT_COVERS, {"size": ("small", "large"), "water": False}, [({"runs": True}, 3.0)], 0.33, {"crude weapon": 2.0}, 2,
        "go out after whatever game the place holds; a weapon helps", basic=True),
    "stalk": _take_row(
        "stalking a beast that keeps to its paths (slow, downwind, close in for the shot)",
        ["stalking", "stalk deer", "stalk the deer", "still-hunting"],
        ["forest", "scrub", "heath", "moor"], {"size": ("medium", "large"), "runs": True, "home": "none"}, [],
        2.5, {"crude weapon": 5.0}, 3, "go quietly after a beast that keeps to its paths, and take it with a weapon"),
    "drive": _take_row(
        "a drive (beaters and spears; others with you; dangerous)",
        ["boar hunt", "hunt the boar", "hunting boar", "spear the boar", "boar hunting", "drive the wood", "a drive"],
        ["forest", "scrub", "fen"], {"size": ("medium", "large"), "social": "group"}, [], 3.0, {"crude weapon": 6.0}, 4,
        "beat a wood with others to drive a herd or sounder onto waiting spears; dangerous alone", untaught=False, crew=True),
    "snare": _take_row(
        "setting snares on the runs",
        ["snaring", "set snares", "snare hares", "snare the runs", "snares", "my snares", "the snares"],
        ["pasture", "meadow", "heath", "field", "scrub"], {"runs": True, "size": ("small", "medium"), "water": False},   # land only:
        [({"home": "form"}, 1.5)],                                                         # no otters in snares (u2 §6 fault 14)
        2.0, {}, 1, "set nooses where small beasts run, and come back for what is caught", basic=True),
    # set and left (brief 2 §4): a snare line catches by night for some nights; whoever finds it takes the catch
    "net": _take_row(
        "netting birds with nets and decoys",
        ["fowling", "fowl", "net fowl", "catch fowl", "wildfowling", "netting", "net birds"],
        ["fen", "water", "meadow", "saltmarsh"], {"size": ("small", "medium"), "flies": True}, [({"water": True}, 1.5)],   # what flies,
        2.0, {}, 2, "spread nets and decoys where flocks come down, best at the water"),   # never fish (u2 §6 fault 3)
    "trap in water": _take_row(
        "setting wicker traps in the water overnight",
        ["set eel traps", "eel traps", "trap eels", "set traps for eels", "eeling", "set traps in the water", "wicker traps", "traps",
         "my traps", "the traps"],
        ["water", "fen"], {"water": True, "size": ("small", "small")}, [], 3.0, {}, 1,
        "set wicker traps in the water overnight and lift them in the morning; best on the nights things run", when=EEL_NIGHTS),
    # set gear in the water (u2 §4.4, §4.5): a gill net meets what swims at a salmon's size in a run, and draws the water's own fish
    # (wild._set_night); a set line the eels at the edge, as a trap does, and the open water too
    "gill net": _take_row(
        "setting a gill net in open water overnight",
        ["gill net", "gill nets", "set a gill net", "set the net", "set nets", "a gill net"],
        ["water"], {"swims": True, "size": ("medium", "medium")}, [], 3.0, {}, 1,
        "set a gill net across open water at dusk; it takes the water's own fish and the bigger fish running, and stays until you take it up"),
    "set line": _take_row(
        "setting a line of baited hooks in the water overnight",
        ["set line", "set lines", "a set line", "long line", "set a line", "night lines"],
        ["water", "fen"], {"water": True, "swims": True, "size": ("small", "small")}, [], 3.0, {}, 1,
        "set a line of hooks in the water at dusk; it takes what feeds at the edge and the water's own fish by night, until you take it up"),
    "den work": _take_row(
        "digging out a den or trapping at a lodge (spades and a dog help)",
        ["dig out the fox earth", "dig out the earth", "dig out the foxes", "dig out the cubs", "earth stopping",
         "trap beavers", "trap the beavers", "trap beaver", "dig out the den"],
        ["forest", "scrub", "heath", "pasture", "meadow", "water", "fen"], {"home": ["den", "burrow", "lodge", "holt"]}, [], 4.0,
        {"crude weapon": 1.25},                                                   # the otter at its holt (u2 §6 fault 14)
        3, "dig out a beast's den, or trap at a lodge, where you know one to be", untaught=False),
}
METHODS["den work"]["yield"]["kind"] = "wild_den"
# nights a set lasts; its chance against a hunter's; how many sets one act lays (a snare line, brief 4 §2.10); what one set holds
SETS = {"snare": {"life": 4, "base": 0.5, "line": 5, "holds": 1, "meet": 0.08},
        "trap in water": {"life": 8, "base": 0.5, "line": 1, "holds": 20, "meet": 0.3},    # meet: a night's meetings (calibrate)
        "gill net": {"life": 16, "base": 0.5, "line": 1, "holds": 8, "meet": 0.3},         # placed gear never springs by age (u2 §2):
        "set line": {"life": 6, "base": 0.5, "line": 1, "holds": 6, "meet": 0.15}}          # `life` is read only by an older world's sets
# a wicker trap's heads: 20 (was 6), so its 10 kg (WATER_WORKS trap hold, D2-258) binds and not the count
for _k, _v in SETS.items():
    METHODS[_k]["set"] = dict(_v)
# the take as a search over time (brief 4 §2.2, §2.6; calibrate): km2 searched a unit of the method's own work, and the hunt's
# hard curve of skill; methods with no sweep search at SWEEP_DEFAULT
SWEEP = {"stalk": 0.4, "hunt the wild": 1.0, "drive": 2.0, "net": 0.3, "den work": 3.0}   # an earth one knows is soon found
for _k, _v in SWEEP.items():
    METHODS[_k]["sweep"] = _v
for _k in ("stalk", "hunt the wild", "drive"):
    METHODS[_k]["curve"] = "hard"
# a beast met is taken at 1 - e^(-take_base x gear x skill x familiarity x (1 - flee)) (brief 4c §3.1): `take_base` the bare-handed
# novice's, by method; `gear` (on each row above; calibrate (4c)) the multiplier of what one carries, by item, on the methods it
# serves; net and den work keep brief 4's chance (take_k x their old bare-handed factor; their weapon's ratio as gear)
TAKE_BASE = {"hunt the wild": 0.25, "stalk": 0.06, "drive": 0.1, "net": 0.25, "den work": 0.2}   # calibrate (4c), and the gear rows
for _k, _v in TAKE_BASE.items():
    METHODS[_k]["take_base"] = _v
METHODS["snare"]["note"] = ("set a line of nooses where small beasts run; it catches by night for a few nights: come back to your snares and "
                            "take what is in them, or it rots there or another finds it")       # brief 4c §4.4
METHODS["trap in water"]["note"] = ("set wicker traps in the water at dusk; they fish by night for some nights, best when things run: come back "
                                    "to your traps and take what is in them, or it rots there or another finds it")                      # at a den, a take; at a lodge, the site's trap (wild.den_work)

METHODS.update({
    "gather young": {"verb": "gather", "label": "taking the young from the nests of a colony", "basic": False, "pack": "wild",
                     "aliases": ["take the young herons", "take herons", "take the herons", "rob the heronry", "take the young rooks",
                                 "take rooks", "take the rooks", "rook shooting", "take the young", "rob the nests"],
                     "at": {"covers": ["forest", "scrub"]}, "draws": "site", "needs": {"site_home": "colony"},
                     "yield": {"kind": "wild_young"}, "units": 1, "gives": "", "tags": ["food", "hunting"],
                     "note": "take the young from a heronry or rookery in their season"},
    "pest work": {"verb": "work", "label": "working the pests off a crop (picking them off, pinching out the tops)", "basic": True,
                  "pack": ["wild", "farming"], "aliases": ["pick slugs at dusk", "pick slugs", "slug the field", "go slugging", "pick off the slugs",
                                              "pick slugs by lantern", "top the beans", "top beans", "pinch out the beans",
                                              "pinch the bean tops", "clear the grubs off the beans", "clear the grubs",
                                              "pick off the grubs", "kill the grubs", "pests", "pest the field"],
                  "at": {"covers": ["field", "meadow", "pasture"]}, "draws": "guard", "needs": {"on_crop": True}, "yield": {"kind": "wild_pest"},
                  "units": 1, "gives": "", "tags": ["farming"],
                  "note": "go over a crop and take off what is eating it; name the pest with \"looking for\", else the worst there"},
    "break a dam": {"verb": "work", "label": "breaking open a dam to drain a flooded meadow", "basic": False, "pack": "wild",
                    "aliases": ["break the beaver dam", "break the dam", "pull down the dam", "drain the meadow"],
                    "at": {"covers": ["forest", "scrub", "meadow"]}, "draws": "site",
                    "yield": {"kind": "wild_site", "site": "lodge", "do": "break"}, "units": 2, "gives": "", "tags": ["farming"],
                    "untaught": "tryable", "note": "pull open a dam that floods a meadow"},
    # the key is not "guard": that is the verb that stands guard over a building at night
    "guard the field": {"verb": "work", "label": "guarding a field by night against beasts", "basic": True, "pack": "wild",
                        "aliases": ["guard", "watch the field", "watch the corn", "a night watch", "watch the field (fire)",
                                    "watch the field with a fire", "watch the corn with a fire", "a fire watch",
                                    "watch the field (clapper)", "watch the field with clappers", "watch the corn with clappers",
                                    "clap them off", "watch the field (horn)", "watch the field with a horn",
                                    "watch the corn with a horn", "blow a horn at them", "watch the field (dog)",
                                    "watch the field with the dog", "watch the corn with the dog", "set the dog on them"],
                        "at": {"covers": FIELD_COVERS + ["water"]}, "draws": "watch", "yield": {"kind": "wild_watch", "scares": SCARES},
                        "units": 2, "gives": "", "tags": ["farming", "animals"],
                        "note": "sit up by a field all night to scare beasts off, with a fire, clappers, a horn or the dog; you lose the night's sleep"},
    "shut": {"verb": "work", "label": "shutting the hens and the store up for the night (the doors wedged, the gaps stopped)",
             "basic": True, "pack": "wild", "aliases": ["shut the hens in", "shut in the hens", "close up the hens", "shut the hens",
                                                        "shut up the store", "bar the doors", "shut the store", "shut up for the night",
                                                        "shut up"],
             "at": {"covers": ["built"]}, "draws": "hens", "yield": {"kind": "wild_shut"}, "units": 1, "gives": "", "tags": ["animals"],
             "note": "shut up your house, store and hens for the night against whatever comes"},
})

# What doing each does, in interface terms (W-109; D2-350, D5-2): what happens when one does it, never what the land holds or when
# (the `note` stays for the old prompt); the set ones take how many one act lays ("qty").
for _k, _v in {
    "hunt the wild": "go out after whatever game the place holds, and take what you meet",
    "stalk": "go quietly after a beast that keeps to its paths, and take it with a weapon",
    "drive": "beat a wood with others to drive beasts onto waiting spears: it needs others with you (a party you lead, or another's "
             "you join with \"with\")",
    "snare": "set a line of nooses from your hands; it stays where you set it and catches by night for a few nights: come back (tend) "
             "and take what is in them, or it rots there or another finds it",
    "net": "spread nets and decoys where birds come down, and take what you net",
    "trap in water": "set wicker traps from your hands in the water; they stay and fish by night: come back (tend) and take what is in "
                     "them, or it rots there or another finds it",
    "gill net": "set a gill net from your hands across open water at dusk; it fishes by night and stays until you take it up (tend)",
    "set line": "set a line of baited hooks from your hands in the water at dusk; it fishes by night and stays until you take it up "
                "(tend)",
    "den work": "dig out a beast's den, or trap at a lodge, where you know one to be",
    "gather young": "take the young from the nests of a colony",
    "pest work": "go over a crop and take off what is eating it; name the pest with \"looking for\", else the worst there",
    "break a dam": "pull open a dam that floods a meadow",
    "guard the field": "sit up by a field all night to scare beasts off, with a fire, clappers, a horn or the dog; you lose the "
                       "night's sleep",
    "shut": "shut up your house, store and hens for the night",
}.items():
    METHODS[_k]["does"] = _v
for _k in SETS:
    METHODS[_k]["args"] = [{"key": "qty", "is": "how many", "req": False, "opts": {}, "who": []}]

LOAD_NAMES = {"moles": ("moles", "mole", "molehills"), "leatherjackets": ("leatherjackets", "the rooks' grubs", "root grubs"),
              "slugs": ("slugs", "slug", "snails"), "aphids": ("aphids", "fly", "blackfly", "greenfly", "the fly", "bean fly"),
              "ladybirds": ("grubs", "the grubs", "spiny grubs", "grey grubs", "ladybirds", "ladybird grubs")}   # a pest's names (§7)

TAKE_METHODS = [m for m, r in METHODS.items() if (r.get("yield") or {}).get("kind") in ("wild_take", "wild_den")]
NOT_BY_LAND = ("gill net", "set line")          # the wave's set gear (u2 §4.4, §4.5): known as seeded or learned (D2-268), not by the land
OLD_NAMES = {a: m for m, r in METHODS.items() for a in r["aliases"]}           # for one release: recorded runs and older worlds


def _ok(trait_v, need) -> bool:
    if isinstance(need, tuple):                                               # a size range
        lo, hi = SIZES.index(need[0]), SIZES.index(need[1])
        return trait_v in SIZES and lo <= SIZES.index(trait_v) <= hi
    if isinstance(need, list):
        return trait_v in need
    return trait_v == need


def takes(method_row, kinds_traits, calibrate=None) -> dict:
    """A method's take table (§4): 0 where a need fails, else base x the favours met x the kind's calibration for the method."""
    out = {}
    for k, tr in sorted(kinds_traits.items()):
        if not all(_ok(tr.get(t), need) for t, need in (method_row.get("needs") or {}).items()):
            continue
        x = float(method_row.get("base", 1.0))
        for cond, f in method_row.get("favours") or []:
            if all(tr.get(t) == v for t, v in cond.items()):
                x *= float(f)
        x *= float(((calibrate or {}).get(k) or {}).get(method_row["_name"], 1.0))
        if x > 0:
            out[k] = round(x, 4)
    return out


def build(TECHNIQUES, RESOURCES) -> None:
    """At load: the methods into TECHNIQUES, each take method's `yield.takes` generated from the kinds' traits (§4)."""
    traits = {k: (r.get("taken") or {}).get("traits") for k, r in RESOURCES.items() if (r.get("taken") or {}).get("traits")}
    cal = {k: (r.get("taken") or {}).get("calibrate") for k, r in RESOURCES.items() if (r.get("taken") or {}).get("calibrate")}
    for name, row in METHODS.items():
        row = dict(row, _name=name)
        if name in TAKE_METHODS:
            row["yield"] = dict(row["yield"], takes=takes(row, traits, cal))
        row.pop("_name")
        TECHNIQUES[name] = row


# ---------------------------------------------------------------------- familiarity by kind (§5; calibrate)
FAMILIAR = {"take": 0.15, "notice": 0.03, "taught": 0.4, "carry": 0.5, "fade": 0.002, "factor": 0.35, "expert": 0.6,
            "start": {"youth": 0.3, "adult": 0.35, "elder": 0.5},
            "party": 0.5}   # a kill seen made by another of one's party: this share of `take` (brief 4c §3.3); calibrate (4c)


def familiar_of(store) -> dict:
    return dict((store or {}).get("familiar") or {})


def familiar(mind, kind) -> float:
    return float(familiar_of(getattr(mind, "store", None)).get(kind, 0.0))


def factor(mind, kind) -> float:
    """What familiarity gives a take of a kind: weight and chance x (1 + 0.5 x familiar) (§5)."""
    return 1.0 + float(FAMILIAR["factor"]) * familiar(mind, kind)


GENERIC = {"game", "big game", "small game", "birds", "vermin"}


def kin(method, kind) -> list:
    """Kinds familiarity carries to at half (§5): those the method takes that share a particular sort with this one (red deer and roe
    are both deer; a hare and a fox share no sort, so knowing hares does not make one better with foxes). By sort, not by the method's
    needed traits: those cannot carry red deer to roe without carrying hares to foxes (02zx, deviation 4)."""
    from cybertron2.engine.data import RESOURCES, TECHNIQUES
    takes = ((TECHNIQUES.get(method) or {}).get("yield") or {}).get("takes") or {}
    mine = set(((RESOURCES.get(kind) or {}).get("taken") or {}).get("family") or []) - GENERIC - {kind}
    return sorted(k for k in takes if k != kind
                  and mine & (set(((RESOURCES.get(k) or {}).get("taken") or {}).get("family") or []) - GENERIC - {k}))


def raise_familiar(here, mind, kind, by, method=None) -> None:
    """Familiarity with a kind rises (by `by`, to at most 1); it carries at half to the method's kin kinds (never to the whole method)."""
    f = familiar_of(mind.store)
    f[kind] = round(min(1.0, f.get(kind, 0.0) + float(by)), 4)
    for k in (kin(method, kind) if method else []):
        f[k] = round(min(1.0, f.get(k, 0.0) + float(by) * float(FAMILIAR["carry"])), 4)
    f["_day"] = here.day
    mind.store["familiar"] = f


def teach_familiar(w, teacher, learner, tech) -> None:
    """Being taught a method gives the learner at least `taught` familiarity with each kind it takes that the teacher knows as well."""
    from cybertron2.engine.data import TECHNIQUES
    kinds = ((TECHNIQUES.get(tech) or {}).get("yield") or {}).get("takes") or {}
    tf = familiar_of((w.s.get("mind") or {}).get(teacher))
    lm = w.s.setdefault("mind", {}).setdefault(learner, {})
    f = familiar_of(lm)
    for k in sorted(kinds):
        if float(tf.get(k, 0.0)) >= float(FAMILIAR["taught"]):
            f[k] = max(float(f.get(k, 0.0)), float(FAMILIAR["taught"]))
    if f:
        lm["familiar"] = f


def familiar_line(mind) -> str:
    """The kinds one knows, in words (§7), never as numbers."""
    f = familiar_of(getattr(mind, "store", None))
    good = sorted(k for k, x in f.items() if not k.startswith("_") and float(x) >= 0.6)
    some = sorted(k for k, x in f.items() if not k.startswith("_") and 0.3 <= float(x) < 0.6)
    if not good and not some:
        return ""
    words = lambda ks: ", ".join(ks[:-1]) + (" and " if len(ks) > 1 else "") + ks[-1]        # noqa: E731
    out = []
    if good:
        out.append(f"you know the {words(good)} of these parts well: their ways, their signs, where they lie")
    if some:
        out.append(f"you know something of the {words(some)}")
    return "- " + "; ".join(out) + "."


# ---------------------------------------------------------------------- who knows what (§6)
BASIC = ("hunt the wild", "gather wild food", "guard the field", "shut", "pest work", "burn the stubble")


def seed_by_land(w) -> None:
    """At world build (§6): each household knows the methods its land holds a target for (a kind with numbers in its village's home
    area or ring, or a site at the village), and its members start familiar with those kinds; `wild.methods_known` (a household to
    methods map) overrides it. The generator's experts keep their levels."""
    from cybertron2.engine import knowledge as KN, wild as WL
    from cybertron2.engine.data import TECHNIQUES
    st = (w.s.get("wild") or {}).get("state")
    land = (w.s.get("wild") or {}).get("land") or {}
    over = (w.spec.get("wild") or {}).get("methods_known")
    if not st and over is None:
        return
    m = WL.model(w) if st else None
    sites = (w.s["wild"].get("sites") or {}) if st else {}
    for hh, inst in sorted(w.s["institutions"].items()):
        if inst.get("kind") != "household":
            continue
        members = [n for n in inst["members"] if n in w.s["people"] and w.s["people"][n].get("alive", True)]
        if not members:
            continue
        node = w.s["people"][members[0]].get("at") or w.s["people"][members[0]].get("home")
        present = _present(w, m, st, land, node) if st else set()
        if over is not None:
            methods = set((over or {}).get(hh) or [])
        else:
            methods = set()
            here_covers = {p["cover"] for p in w.s["parcels"].values() if p.get("node") == node}
            for meth in [x for x in TAKE_METHODS if x not in NOT_BY_LAND]:     # a method its land holds: one of its main kinds
                tk = TECHNIQUES[meth]["yield"].get("takes") or {}              # (at least half its largest weight) about, and
                top = max(tk.values(), default=0.0)                            # ground of the kind it is worked on at the village
                main = {k for k, x in tk.items() if float(x) >= 0.5 * float(top) and float(x) > 0}
                covers = set((TECHNIQUES[meth].get("at") or {}).get("covers") or [])
                if main & present and (not covers or covers & here_covers):
                    methods.add(meth)
            if any(s.get("node") == node and s.get("gone") is None and s["kind"] in ("heronry", "rookery") for s in sites.values()):
                methods.add("gather young")
            if any(s.get("node") == node and s.get("gone") is None and s["kind"] == "lodge" for s in sites.values()):
                methods |= {"den work", "break a dam"}
        heads = {inst.get("head")} | set((inst.get("offices") or {}).values())
        for n in members:
            k = w.s["know"].setdefault(n, {})
            for meth in sorted(methods):
                if meth not in TECHNIQUES or KN.basic(meth):
                    continue
                if meth == "drive" and n not in heads and over is None:          # the drive is led by the household's head (§6)
                    continue
                if meth not in k:
                    k[meth] = {"level": "known", "skill": KN.curve(meth)[0], "seen": 0, "wins": 0, "fails": 0,
                               "source": "from your upbringing", "since": -1}
            start = float(FAMILIAR["start"].get(w.s["people"][n].get("stage", "adult"), 0.0))
            if start <= 0:
                continue
            mind = w.s.setdefault("mind", {}).setdefault(n, {})
            f = dict(mind.get("familiar") or {})
            for meth in sorted(methods):
                for kind in (TECHNIQUES.get(meth, {}).get("yield") or {}).get("takes") or {}:
                    if kind in present:
                        f[kind] = max(float(f.get(kind, 0.0)), start)
            if f:
                mind["familiar"] = f


def _present(w, m, st, land, node) -> set:
    """Kinds with at least one head in the village's home area or its ring."""
    out = set()
    if not node or m is None:
        return out
    areas = [i for i, a in enumerate(m.ids) if land.get("home", {}).get(node) == a
             or (land["areas"][a]["kind"] == "ring" and land["areas"][a].get("node") == node)]
    for k, pop in (st.get("pop") or {}).items():
        if sum(float(pop[i]) * float(m.km2[i]) for i in areas) >= 1.0:
            out.add(k)
    return out
