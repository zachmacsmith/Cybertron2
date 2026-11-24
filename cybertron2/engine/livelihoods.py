"""Livelihoods as data, holdings, and pin and fill (u11_worlds.md §1 to §4; D2-268, D2-270, D2-279, D2-311, D2-330): the feature
units of livelihoods (the rows, their keeper and household lines' ids, the fill steps that read them) and holdings (the capital and
knowledge registry, filled both ways). The founders' lines are founders.py's (U9's templates); the gate check is
landgen/gate_check.py.

A world file's `skills` block says what is pinned; `fill(world)` fills the rest on the world as written (spec form), keyed by what
each draw is about (landgen/keyed.py's rule: pinning one household leaves every other draw as it was). A world without `skills`
keeps today's generation (old worlds replay).

Technique names are the engine's (TECHNIQUES keys); `wicker traps (set)` is "trap in water" and `(make)` "wicker trap" (u2, u3).
"""
from __future__ import annotations

import hashlib

# ---------------------------------------------------------------------- the rows (u11 §1.2; ★ crafts of this wave named by key)
ROWS = {
    "fisher": {
        "status": "built", "fits": {"covers": ["water"], "best": "a river with runs"}, "words": {"lives": "fishing"},
        "broad": ["fish by hand", "angle", "fishing rod", "trap in water", "dry fish"],
        "capable": ["salt fish", "smoke fish", "tend the smoke", "wicker trap", "hand line"],
        "specialisms": {
            "weir_and_nets": {"words": "the weir and its nets", "crafts": ["weir", "gill nets", "gill net", "twist cord", "mend gear"],
                              "capital": ["weir"], "lines": ["FI9", "FI10", "FI11", "FI12"]},
            "traps_and_runs": {"words": "the traps and the runs", "crafts": ["trap in water", "wicker trap", "cut withies"],
                               "lines": ["FI4", "FI6", "FI7", "FI8"]},
            "hand_rod_dressing": {"words": "the hand, the rod and the line", "crafts": ["fish by hand", "angle", "fishing rod", "dip net",
                                                                                        "set line", "set lines"],
                                  "lines": ["FI5", "FI13", "FI14", "FI15"]},
            "keeping": {"words": "keeping the catch", "crafts": ["smoke fish", "tend the smoke", "smoke racks", "salt fish", "dry fish",
                                                                 "hard cure fish"],
                        "capital": ["smokehouse"], "lines": ["FI16", "FI17", "FI18", "FI19"]}},
        "lines": {"broad": ["FI1", "FI2", "FI3"], "capable": ["FI4", "FI5"], "youth": ["FI1", "FI2"], "second": ["FI1", "FI2", "FI3", "FI5"]},
        "capital": {"likely": ["wicker traps", "smoke racks"], "sometimes": ["weir", "smokehouse", "gill net"]},
        "keeper_lines": {"weir": "FI12", "smokehouse": "FI17"}, "depends": {"needs": ["salt", "withies", "cord"], "gives": ["fish"]},
        "neighbour_line": "NB-FI", "apprentice": True},
    "salter": {
        "status": "built", "fits": {"spring": "brine", "covers": ["saltmarsh"]}, "words": {"lives": "boiling salt at the spring"},
        "broad": ["boil salt", "salt meat", "salt fish", "firewood", "cut"], "capable": ["mend the brine pan", "salt pan"],
        "specialisms": {"the_pan": {"words": "the pan", "crafts": ["boil salt", "mend the brine pan"], "capital": ["salt house"],
                                    "lines": ["SA2", "SA3", "SA4"]},
                        "salting": {"words": "salting for keeping", "crafts": ["salt fish", "salt meat"], "lines": ["SA5"]},
                        "carrying": {"words": "carrying salt", "crafts": [], "lines": ["SA6"]}},
        "lines": {"broad": ["SA1"], "capable": ["SA2"], "youth": ["SA1"], "second": ["SA1"]},
        "capital": {"likely": ["salt house"], "sometimes": []}, "keeper_lines": {"salt house": "SA4"},
        "depends": {"needs": ["copper", "firewood"], "gives": ["salt"]}, "neighbour_line": "NB-SA", "apprentice": True},
    "farmer": {"status": "built", "fits": {"covers": ["field"]}, "words": {"lives": "the land"},
               "broad": ["sow", "hoe", "weed", "reap", "manure", "dung", "clear", "pest work", "guard the field"], "capable": ["plough", "dry fodder", "bread"],
               "specialisms": {"ploughman": {"words": "the plough and the oxen", "crafts": ["plough"], "capital": ["ox pair"], "lines": ["FA6", "FA7"]},
                               "seed_and_harvest": {"words": "seed and harvest", "crafts": ["sow", "reap"], "capital": ["fields"], "lines": ["FA5", "FA8", "FA9", "FA10"]},
                               "hedge_and_field": {"words": "hedge and field", "crafts": ["fence", "guard the field"], "lines": ["FA11"]}},
               "lines": {"broad": ["FA1", "FA2", "FA3"], "capable": ["FA4", "FA5"], "youth": ["FA1", "FA2"], "second": ["FA1", "FA3"]},
               "capital": {"likely": ["fields", "bins"], "sometimes": ["ox pair", "byre"]}, "keeper_lines": {"ox pair": "FA7", "fields": "FA9"},
               "depends": {"needs": ["copper", "flour"], "gives": ["grain"]}, "neighbour_line": "NB-FA"},
    "herder": {"status": "built", "fits": {"covers": ["pasture", "meadow", "fen"]}, "words": {"lives": "the herd"},
               "broad": ["herd", "milk", "fence", "hay", "dung"], "capable": ["slaughter", "dry fodder"],
               "specialisms": {"dairy": {"words": "the dairy", "crafts": ["milk", "cheese"], "capital": ["cellar"], "lines": ["HE5"]},
                               "stock": {"words": "stock and breeding", "crafts": ["herd", "slaughter"], "capital": ["herd"], "lines": ["HE4", "HE6", "HE7"]},
                               "hay_and_winter": {"words": "hay and winter", "crafts": ["hay", "dry fodder"], "lines": ["HE8"]}},
               "lines": {"broad": ["HE1", "HE2"], "capable": ["HE3", "HE4"], "youth": ["HE1", "HE2"], "second": ["HE1", "HE2"]},
               "capital": {"likely": ["herd"], "sometimes": ["cellar", "byre"]}, "keeper_lines": {"herd": "HE7"},
               "depends": {"needs": ["salt", "hay"], "gives": ["milk", "cheese"]}, "neighbour_line": "NB-HE"},
    "hunter": {"status": "built", "fits": {"covers": ["forest", "scrub", "heath"]}, "words": {"lives": "hunting and trapping"},
               "broad": ["hunt the wild", "snare", "dry meat", "crude weapon"], "capable": ["stalk", "den work", "salt meat", "tent", "bedroll", "snares"],
               "specialisms": {"stalking": {"words": "stalking and drives", "crafts": ["stalk", "drive"], "lines": ["HU5", "HU6"]},
                               "snares": {"words": "snares and small game", "crafts": ["snare", "snares"], "lines": ["HU7"]}},
               "lines": {"broad": ["HU1", "HU2"], "capable": ["HU3", "HU4"], "youth": ["HU1"], "second": ["HU1", "HU2"]},
               "capital": {"likely": ["crude weapon", "snares"], "sometimes": ["tent"]}, "keeper_lines": {},
               "depends": {"needs": ["salt"], "gives": ["meat", "hide"]}, "neighbour_line": "NB-HU"},
    "fowler": {"status": "later", "fits": {"covers": ["fen", "water"]}, "words": {"lives": "fowling"}, "broad": [], "capable": [],
               "specialisms": {}, "lines": {}, "capital": {}, "keeper_lines": {}, "depends": {"needs": ["cord"], "gives": ["fowl"]},
               "neighbour_line": "NB-FO"},                                            # D2-318: postponed with the hunting build-out
    "smith": {"status": "built", "fits": {"covers": ["rock"]}, "words": {"lives": "copper work at the forge"},
              "broad": ["charcoal", "firewood"], "capable": ["mine", "copper tool"],
              "specialisms": {"smelting": {"words": "smelting and tools", "crafts": ["smelt", "copper tool", "copper hook"], "capital": ["forge"],
                                           "lines": ["SM3", "SM4"]}},
              "lines": {"broad": ["SM1"], "capable": ["SM2"], "youth": ["SM1"], "second": ["SM1"]},
              "capital": {"likely": ["forge"], "sometimes": []}, "keeper_lines": {"forge": "SM4"},
              "depends": {"needs": ["charcoal"], "gives": ["copper"]}, "neighbour_line": "NB-SM"},
    "miller": {"status": "built", "fits": {"mill_site": True}, "words": {"lives": "the mill"},
               "broad": ["grind", "bread"], "capable": ["mill", "oven bread", "dress millstones"],
               "specialisms": {"the_mill": {"words": "the mill", "crafts": ["mill", "water mill", "dress millstones", "clear the leat"],
                                            "capital": ["mill"], "lines": ["MI3", "MI4"]},
                               "the_oven": {"words": "the oven", "crafts": ["oven bread", "reline oven"], "capital": ["oven"], "lines": ["MI5"]}},
               "lines": {"broad": ["MI1"], "capable": ["MI2"], "youth": ["MI1"], "second": ["MI1"]},
               "capital": {"likely": ["mill"], "sometimes": ["oven"]}, "keeper_lines": {"mill": "MI3", "oven": "MI5"},
               "depends": {"needs": ["grain"], "gives": ["flour", "bread"]}, "neighbour_line": "NB-MI"},
    "builder": {"status": "built", "fits": {"covers": ["forest", "rock"]}, "words": {"lives": "building"},
                "broad": ["fell", "small room", "beds", "bins", "repair", "clear for building", "woodshed"],
                "capable": ["medium room", "granary", "hearth", "smoke racks"],
                "specialisms": {"wright": {"words": "the wright's work", "crafts": ["medium room", "hall"], "lines": ["BU5", "BU6"]},
                                "mason": {"words": "the mason's work", "crafts": ["quarry", "hearth", "wall"], "lines": ["BU7", "BU8"]}},
                "lines": {"broad": ["BU1", "BU2"], "capable": ["BU3"], "youth": ["BU1"], "second": ["BU1"]},
                "capital": {"likely": ["timber", "woodshed"], "sometimes": []}, "keeper_lines": {},
                "depends": {"needs": ["timber", "stone"], "gives": ["rooms", "hearths"]}, "neighbour_line": "NB-BU"},
    "woodsman": {"status": "built", "fits": {"covers": ["forest"]}, "words": {"lives": "the wood"},
                 "broad": ["fell", "cut", "firewood"], "capable": ["charcoal", "cut withies"],
                 "specialisms": {"charcoal": {"words": "charcoal", "crafts": ["charcoal"], "lines": ["WO2"]}},
                 "lines": {"broad": ["WO1"], "capable": ["WO2"], "youth": ["WO1"], "second": ["WO1"]},
                 "capital": {"likely": [], "sometimes": []}, "keeper_lines": {}, "depends": {"needs": [], "gives": ["charcoal", "firewood"]},
                 "neighbour_line": "NB-WO"},
    "basket maker": {"status": "built", "fits": {"covers": ["fen"]}, "words": {"lives": "the willow"},
                     "broad": ["cut withies", "hurdle"], "capable": ["wicker trap", "creel", "pack basket"],
                     "specialisms": {"traps_and_creels": {"words": "traps and creels", "crafts": ["wicker trap", "creel"], "lines": ["BA3"]}},
                     "lines": {"broad": ["BA1", "BA2"], "capable": ["BA3"], "youth": ["BA1"], "second": ["BA1"]},
                     "capital": {"likely": [], "sometimes": ["withy bed"]}, "keeper_lines": {"withy bed": "BA5"},
                     "depends": {"needs": [], "gives": ["traps", "creels", "hurdles"]}, "neighbour_line": "NB-BA"},
    "cord and nets": {"status": "built", "fits": {"covers": ["field", "meadow"]}, "words": {"lives": "cord and nets"},
                      "broad": ["twist cord"], "capable": ["pull flax", "ret flax", "dress and spin"],
                      "specialisms": {"nets": {"words": "nets", "crafts": ["gill nets", "dip net"], "lines": ["CO5"]}},
                      "lines": {"broad": ["CO1"], "capable": ["CO2"], "youth": ["CO1"], "second": ["CO1"]},
                      "capital": {"likely": [], "sometimes": ["flax close"]}, "keeper_lines": {},
                      "depends": {"needs": [], "gives": ["cord", "nets"]}, "neighbour_line": "NB-CO"},
    "tanner": {"status": "later", "fits": {"covers": ["water"]}, "words": {"lives": "tanning"}, "broad": [], "capable": [],
               "specialisms": {}, "lines": {}, "capital": {}, "keeper_lines": {"tan pits": "TA5"},
               "depends": {"needs": ["hides", "bark"], "gives": ["leather"]}, "neighbour_line": "NB-TA"},   # D2-327: deferred
    "trader": {"status": "built", "fits": {"track": True}, "words": {"lives": "carrying between villages"},
               "broad": [], "capable": [], "specialisms": {}, "lines": {"broad": ["TR1"], "capable": ["TR2"], "second": ["TR1"]},
               "capital": {"likely": [], "sometimes": ["handcart"]}, "keeper_lines": {}, "depends": {"needs": [], "gives": ["carrying"]},
               "neighbour_line": "NB-TR"},
    "cottager": {"status": "built", "fits": {}, "words": {"lives": "work for others and your garden"}, "broad": ["gather wild food", "firewood"],
                 "capable": [], "specialisms": {}, "lines": {"broad": ["CT1", "CT2"], "capable": ["CT3"], "youth": ["CT1"]},
                 "capital": {"likely": [], "sometimes": []}, "keeper_lines": {}, "depends": {"needs": [], "gives": ["labour"]},
                 "neighbour_line": "NB-CT"},
}
# the holdings registry (u11 §2.1): the kind of building or capital, its working craft, its mending craft, its keeper line
HOLDINGS = {
    "weir": {"working": ["weir"], "band": "weir_and_nets", "mending": "weir", "keeper_line": "FI12", "chokepoint": True,
             "of": lambda b: b.get("monument") == "weir"},
    "smokehouse": {"working": ["smoke fish", "tend the smoke"], "band": "keeping", "mending": "repair", "keeper_line": "FI17",
                   "chokepoint": False, "of": lambda b: bool((b.get("fittings") or {}).get("smoke racks"))},
    "salt house": {"working": ["boil salt"], "band": "the_pan", "mending": "mend the brine pan", "keeper_line": "SA4", "chokepoint": True,
                   "of": lambda b: bool((b.get("fittings") or {}).get("brine pan"))},
    "mill": {"working": ["water mill", "mill"], "band": "the_mill", "mending": "dress millstones", "keeper_line": "MI3", "chokepoint": True,
             "of": lambda b: bool((b.get("fittings") or {}).get("water wheel") or (b.get("fittings") or {}).get("millstones"))},
    "oven": {"working": ["oven bread"], "band": "the_oven", "mending": "reline oven", "keeper_line": "MI5", "chokepoint": False,
             "of": lambda b: bool((b.get("fittings") or {}).get("oven"))},
    "forge": {"working": ["smelt", "copper tool"], "band": "smelting", "mending": "repair", "keeper_line": "SM4", "chokepoint": True,
              "of": lambda b: bool((b.get("fittings") or {}).get("anvil"))},
}
SIZE_RULE = ((5, 2), (2, 1))          # D2-270: two experts for 5 or more working members, one for 2 to 4
CAPABLE_SHARE = 1.0 / 3.0             # u11 §3.1 (B11-3)
APPRENTICE = 0.5                      # D2-270, B11-2: a keyed draw
SEEDED_TRAPS = 6                      # D2-330 C5 (B11-4): six wicker traps a capable or expert setter; a gill net to the weir expert
YOUTH_DAYS = (12, 24)                 # D2-153 at lifespan 64: a youth is 12 to 24 days old; the older half is 18 to 24
CAST = {"head": "claude-opus-5-5", "middle": "claude-sonnet-5-5", "rest": "claude-haiku-5-5"}   # u11 §3.2; scenario_design §2


def keyed(*parts) -> float:
    """A draw in [0, 1) keyed by what it is about (landgen/keyed.py's rule): the same for the same parts, whatever else is pinned."""
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:12], 16) / float(16 ** 12)


def experts_for(working: int) -> int:
    for n, k in SIZE_RULE:
        if working >= n:
            return k
    return 0


def class_range(tech) -> tuple:
    from cybertron2.engine import learning as LR
    return LR.curve_range(tech)


def skill_for(tech, band, key) -> float:
    """A founder's skill in a craft by band (u11 §3.1): an expert the top half of the class's range, a capable member the middle, the
    broad band the low end; keyed."""
    lo, hi = class_range(tech)
    x = keyed(*key)
    if band == "expert":
        a, b = lo + 0.55 * (hi - lo), hi
    elif band == "capable":
        a, b = lo + 0.3 * (hi - lo), lo + 0.55 * (hi - lo)
    else:
        a, b = lo, lo + 0.25 * (hi - lo)
    return round(a + x * (b - a), 3)


def level_for(tech, band, in_band) -> str:
    """The level a band gives a craft (u11 §3.1): experts know broad, capable and their specialism; a capable member knows the broad
    band and is capable in the capable band; the broad band knows its simple crafts, a rough idea of its practised ones."""
    from cybertron2.engine import learning as LR
    c = LR.cls(tech)
    if band == "expert":
        return "known"
    if band == "capable":
        return "known" if in_band == "broad" else ("capable" if in_band == "capable" else "rough")
    return "known" if c == "simple" else "rough"


def _age(a, day0=0) -> int:
    return int(day0) - int(a.get("born") or 0)


def fill(world: dict, skills: dict | None = None, seed=None, lines=True) -> dict:
    """Pin and fill (u11 §4.2) on a world as written: steps 2 (pinned livelihoods and capital), 4 (capital from livelihoods: gear), 6
    (bands, specialisms, levels, skills, keepers, apprentices), 8 (neighbours aware), 9 (the seeded lines, founders.py) and 11 (the
    cast and the livelihood line). Steps 1, 3, 5, 7 are the generator's (landgen; unpinned households are not drawn here: report).
    Returns the fill's report (u11 §5's P4 skips, the cap's steps, the keepers)."""
    from cybertron2.engine.data import TECHNIQUES
    skills = skills if skills is not None else (world.get("skills") or {})
    seed = world.get("seed", 0) if seed is None else seed
    agents = world["agents"]
    report = {"households": {}, "people": {}, "skipped": [], "refused": [], "capital": {}}
    hhs = {}
    for n, a in agents.items():
        if a.get("household"):
            hhs.setdefault(a["household"], []).append(n)
    pins = skills.get("households") or {}
    for hh in sorted(hhs):
        pin = pins.get(hh)
        if not pin:
            report["skipped"].append(f"{hh}: not pinned (the generator's draw by village_mix is landgen's, step 3)")
            continue
        livs = list(pin.get("livelihoods") or [])
        for lv in livs:
            if ROWS.get(lv, {}).get("status") != "built":
                report["refused"].append(f"P15: {hh}'s livelihood {lv!r} is not built")
        livs = [lv for lv in livs if ROWS.get(lv, {}).get("status") == "built"]
        core, second = livs[:1], livs[1:2]
        members = sorted(hhs[hh], key=lambda n: (_age(agents[n]) * -1, n))
        working = [n for n in members if agents[n].get("stage") in ("youth", "adult", "elder")]
        prime = [n for n in working if agents[n].get("stage") in ("adult", "elder")]
        holds = {kind: [bid for bid, b in (world.get("buildings") or {}).items() if b.get("household") == hh and r["of"](b)]
                 for kind, r in HOLDINGS.items()}
        holds = {k: v for k, v in holds.items() if v}
        n_exp = int(pin.get("experts_n") or experts_for(len(working)))
        specs = list(pin.get("experts") or [])
        row = ROWS[core[0]] if core else None
        if row and len(specs) < n_exp:                                        # the specialism working its most valuable holding
            for kind in sorted(holds, key=lambda k: (not HOLDINGS[k]["chokepoint"], k)):
                sp = next((s for s, d in row["specialisms"].items() if kind in (d.get("capital") or [])), None)
                if sp and sp not in specs:
                    specs.append(sp)
            for s in row["specialisms"]:
                if len(specs) >= n_exp:
                    break
                if s not in specs:
                    specs.append(s)
        specs = specs[:n_exp]
        bands = {}
        pinned_agents = skills.get("agents") or {}
        order = sorted(prime, key=lambda n: (0 if agents[n].get("role") == "head" else 1, -_age(agents[n]), n))
        experts = {}
        for s in specs:
            who = next((n for n in order if n not in experts.values() and (pinned_agents.get(n) or {}).get("band") in (None, "expert")), None)
            if who:
                experts[s] = who
                bands[who] = "expert"
        rest = [n for n in order if n not in bands]
        n_cap = int(round(CAPABLE_SHARE * len(rest) + 1e-9)) if rest else 0
        for n in rest:
            want = (pinned_agents.get(n) or {}).get("band")
            if want:
                bands[n] = want
        for n in rest:
            if n not in bands and sum(1 for x in bands.values() if x == "capable") < n_cap:
                bands[n] = "capable"
        for n in working:
            bands.setdefault(n, "broad")
        second_hands = []
        if second:                                                             # a second trade: 1 to 2 adults, one at capable (u11 §3.1)
            cands = [n for n in order if n not in experts.values()] + [n for n in order if n in experts.values()]
            second_hands = cands[:2]
        for kind, bids in sorted(holds.items()):                               # a holding no expert keeps needs a capable hand (P1): the
            sp = next((s for s in experts if kind in (row["specialisms"][s].get("capital") or [])), None) if row else None
            if sp:                                                             # second trade's capable member, else the first broad
                continue                                                       # adult raised to capable (reported)
            works = HOLDINGS[kind]["working"]
            if any(t in ROWS[lv]["capable"] + ROWS[lv]["broad"] for lv in second for t in works) and second_hands:
                continue
            if any(bands.get(n) == "capable" for n in order):
                continue
            up = next((n for n in order if bands.get(n) == "broad"), None)
            if up:
                bands[up] = "capable"
                report["skipped"].append(f"{hh}: {up} raised to capable to keep the {kind} (u11 §2.3)")
        helps = {}
        for n, b in bands.items():                                            # a capable member helps an expert (rough in it)
            if b == "capable" and experts:
                helps[n] = next(iter(experts))
        appr = {}
        for n in working:
            a = agents[n]
            if a.get("stage") != "youth" or not experts or not row or not row.get("apprentice"):
                continue
            age = _age(a)
            if age >= (YOUTH_DAYS[0] + YOUTH_DAYS[1]) / 2 and keyed(seed, "apprentice", n) < APPRENTICE:
                appr[n] = next(iter(experts))                                   # the specialism; its expert is experts[it]
        # knows
        for n in members:
            a = agents[n]
            a.setdefault("knows", {})
            if a.get("stage") not in ("youth", "adult", "elder"):
                continue
            k = {}
            b = bands.get(n, "broad")
            for lv in core:
                r = ROWS[lv]
                for t in r["broad"]:
                    k[t] = level_for(t, b, "broad")
                if b in ("expert", "capable") and a.get("stage") != "youth":
                    for t in r["capable"]:
                        k[t] = level_for(t, b, "capable")
                for s, who in experts.items():
                    if who == n and s in r["specialisms"]:                 # a specialism is its own living's (two core livings:
                        for t in r["specialisms"][s]["crafts"]:          # a wright is the builder's, not the woodsman's; W-107)
                            k[t] = "known"
                if n in helps and helps[n] in r["specialisms"]:
                    for t in r["specialisms"][helps[n]]["crafts"]:
                        k.setdefault(t, "rough")
                if n in appr and appr[n] in r["specialisms"]:
                    for t in r["specialisms"][appr[n]]["crafts"]:
                        k.setdefault(t, "rough")
            for lv in second:
                if n in second_hands:
                    r = ROWS[lv]
                    for t in r["broad"]:
                        k.setdefault(t, level_for(t, "broad", "broad"))
                    if n == second_hands[0] and a.get("stage") != "youth":
                        for t in r["capable"] + r["broad"]:
                            if k.get(t) in (None, "rough"):
                                k[t] = "capable"
            new = {}
            for t, lvl in k.items():
                if t not in TECHNIQUES:
                    report["skipped"].append(f"{n}: craft {t!r} is not in this engine")
                    continue
                band_for = "expert" if lvl == "known" and b == "expert" else ("capable" if lvl in ("known", "capable") and b != "broad" else "broad")
                new[t] = {"level": lvl, "skill": skill_for(t, band_for, (seed, "skill", n, t))}
            for t in list(a["knows"]):                                         # the fill sets the livelihood crafts; others stay
                if t in new or t in ("trap in water", "net", "weir", "smoke fish", "tend the smoke", "salt fish", "boil salt",
                                     "wicker trap", "gill net"):
                    a["knows"].pop(t, None)
            a["knows"].update(new)
            a["band"] = b
            if b == "expert":
                a["specialism"] = next(s for s, who in experts.items() if who == n)
            elif n in appr:
                a["apprentice"] = {"to": experts[appr[n]], "specialism": appr[n]}
        # keepers (u11 §2.3)
        keepers = {}
        expert_kept = lambda k: bool(core) and any(k in (ROWS[core[0]]["specialisms"][s].get("capital") or []) for s in experts)  # noqa: E731
        for kind, bids in sorted(holds.items(), key=lambda kv: (not expert_kept(kv[0]), kv[0])):
            H = HOLDINGS[kind]
            for bid in bids:
                sp = next((s for s, who in experts.items() if kind in (ROWS[core[0]]["specialisms"][s].get("capital") or [])), None) if core else None
                if not sp and second:
                    sp2 = next((s for s, d in ROWS[second[0]]["specialisms"].items() if kind in (d.get("capital") or [])), None)
                    sp = None
                who = experts.get(sp) if sp else None
                if who is None:
                    able = [n for n in order if any((agents[n]["knows"].get(t) or {}).get("level") in ("capable", "known") for t in H["working"])
                            and n not in keepers.values()]
                    who = able[0] if able else None
                if who is None:
                    able = [n for n in order if any((agents[n]["knows"].get(t) or {}).get("level") in ("capable", "known") for t in H["working"])]
                    who = able[0] if able else (order[0] if order else None)
                    if who:
                        report["skipped"].append(f"{hh}: {kind} {bid} kept by {who}, its only able hand")
                if who:
                    keepers[bid] = who
                    (world["buildings"][bid]).setdefault("keeper", who)
                    world["buildings"][bid]["keeper"] = who
        # gear (u11 §2.2, B11-4; D2-330 C5): six traps a capable or expert setter, a gill net to the weir's expert, a hand line to each
        # who fishes by line, copper hooks to mend them (stage 2's gate: nothing gives bone)
        for n in working:
            a = agents[n]
            kn = a.get("knows") or {}
            h = a.setdefault("holdings", {})
            for g in ("wicker trap", "gill net", "hand line"):                 # the fill places the gear
                h.pop(g, None)
            if (kn.get("trap in water") or {}).get("level") in ("capable", "known") and a.get("stage") != "youth":
                h["wicker trap"] = SEEDED_TRAPS
            if (kn.get("angle") or {}) and a.get("stage") != "youth" and core and core[0] == "fisher":
                h["hand line"] = 1
            if experts.get("weir_and_nets") == n:
                h["gill net"] = 1
        if core and core[0] == "fisher":
            house = next((bid for bid, b in world["buildings"].items() if b.get("household") == hh and (b.get("fittings") or {}).get("beds")), None)
            if house:
                world["buildings"][house].setdefault("stock", {})["copper hook"] = 4
        report["households"][hh] = {"livelihoods": livs, "experts": experts, "bands": {n: bands.get(n) for n in working},
                                    "apprentices": appr, "keepers": keepers, "holds": holds, "second_hands": second_hands}
        for n in members:
            a = agents[n]
            a["livelihoods"] = livs
            a["crafts_first"] = [t for lv in livs for t in ROWS[lv]["broad"] + ROWS[lv]["capable"]]
            a["livelihood"] = livelihood_line(world, hh, n, livs, bands, experts, keepers, appr, second_hands)
    # the cast (u11 §3.2): heads and chokepoint keepers Opus, a capable adult a household Sonnet, the rest Haiku
    cast = {**CAST, **(skills.get("cast") or {})}
    for hh, rep in report["households"].items():
        mid = 0
        for n in sorted(rep["bands"], key=lambda x: (0 if agents[x].get("role") == "head" else 1, x)):
            a = agents[n]
            choke = any(who == n and HOLDINGS[k]["chokepoint"] for k, bids in rep["holds"].items() for bid in bids
                        for who in [rep["keepers"].get(bid)])
            if a.get("role") == "head" or choke:
                a["model"] = cast["head"]
            elif rep["bands"].get(n) in ("capable", "expert") and a.get("stage") == "adult" and mid < 1:
                a["model"] = cast["middle"]
                mid += 1
            else:
                a["model"] = cast["rest"]
    # neighbours (u11 §3.3): aware of each other household's broad band
    for n, a in agents.items():
        if a.get("stage") not in ("youth", "adult", "elder") or not a.get("household"):
            continue
        for hh, rep in report["households"].items():
            if hh == a["household"]:
                continue
            for lv in rep["livelihoods"][:1]:
                for t in ROWS[lv]["broad"]:
                    if t in TECHNIQUES and t not in (a.get("knows") or {}):
                        if (TECHNIQUES[t].get("basic")):
                            continue                                             # everyone's crafts need no seeing
                        a.setdefault("aware_of", {})[t] = f"you have seen the {hh}s at it all your life"
    if lines:
        from cybertron2.engine import founders as FD
        report["lines"] = FD.seed_world(world, report, seed)
    return report


def livelihood_line(world, hh, n, livs, bands, experts, keepers, appr, second_hands=()) -> str:
    """u9 §2.2: "You live by <words>" + the specialism + the holding kept + a second living; a youth's and a child's forms."""
    a = world["agents"][n]
    if a.get("stage") in ("child", "infant") or not livs:
        return ""
    words = [ROWS[lv]["words"]["lives"] for lv in livs]
    if a.get("stage") == "youth":
        if n in appr:
            sp = ROWS[livs[0]]["specialisms"][appr[n]]["words"]
            return f"You are learning your household's living from {experts[appr[n]]}, at {sp}."
        return "You are learning your household's living."
    out = f"You live by {words[0]}"
    if len(words) > 1 and n in second_hands:
        out += f", and by {words[1]} beside it"
    sp = next((s for s, who in experts.items() if who == n), None)
    if sp:
        out += f", and you are best at {ROWS[livs[0]]['specialisms'][sp]['words']}"
    kept = [bid for bid, who in keepers.items() if who == n]
    for bid in kept[:1]:
        b = world["buildings"][bid]
        name = b.get("name") or bid
        if b.get("monument") == "weir":
            water = (world["nodes"].get(b.get("node") or "", {}).get("parcels") or {}).get(b["parcel"], {}).get("name")
            if water is None:
                water = next((p["name"] for nd in world["nodes"].values() for pid, p in (nd.get("parcels") or {}).items() if pid == b["parcel"]), "the river")
            out += f", and you keep the weir on {water}"
        else:
            out += f", and you keep {name}"
    return out + "."
