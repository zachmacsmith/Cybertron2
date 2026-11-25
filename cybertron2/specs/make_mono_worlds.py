"""The monoculture worlds as generated worlds (W-203): Fallowmere (M1) and the Scattering (M5) from mono_design.py
(proposals/monoculture_five_worlds.md §2 and §6), realised with the land generator the way make_peoples.py realises the peoples
worlds (every place and road pinned; the design's features; fish and salt stocked), then:
- **the founders** of the design, in place of the generator's people: names, sexes, ages (mixed: founders turn elder from about day
  10 to day 32 at lifespan 64), households, partners, kin across groups (World 5's families are of one people);
- **livelihoods, capital and seeded lines** pinned and filled (livelihoods.fill, u11), as make_world0.py does;
- **unexplored land** (D4-47): only each group's home and the places a day from it are known (a person's `places`); everything else
  is found by going, by being told, or by a rumour line;
- **stores** at each home for FIRST days of its people's food (to the first harvest or catch at about 1.15 times need);
- **the graded goal** kept whole by every founder (D5-1), inside the 20-line cap;
- the rebuilt prompt, learning as one record, 200 days, spring day 1, a 32-day year; one model for everyone, an arm a model.

    python3 -m cybertron2.specs.make_mono_worlds [M1 M5] [--seed N] [--models claude-haiku-5-5,...]

Writes cybertron2/specs/mono/<m1|m5>.yaml (with .cells.npz and a picture), a check file (the gate, capacity, roads against the
design) and an arm file a model. Generated, not run.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import yaml  # noqa: E402

from cybertron2.specs import make_peoples as MP  # noqa: E402
from cybertron2.specs import mono_design as D  # noqa: E402
from cybertron2.specs.make_world0 import CAP, MEMORY, WORLD_GOAL as GOAL  # noqa: E402   (D5-7)
from cybertron2.landgen import write as W  # noqa: E402

MP.D = D                                   # the peoples maker's features and comparison read this design
OUT = os.path.join(HERE, "mono")
LIFESPAN = 64
FIRST = 16                                 # days of food in store at the start (spring day 1; the first harvest about day 16 to 20)
PLOT_SEED = 16                             # grain a plot sown (data.PHYSICS farming.plot_seed): next year's seed, in store (Q-220)
WORKED_MIN = 1.2                           # a home feeds at least this many times its people at good work (the design check, W-203)
MODELS = ["claude-haiku-5-5"]

# --------------------------------------------------------------------------- the founders (monoculture_five_worlds.md §2 and §6)
# (name, sex, age in days, partner); the first is the head
FOUNDERS = {
    "M1": {"Fallowmere": {
        "Ashby": [("Robert", "m", 54, "Agnes"), ("Agnes", "f", 44, "Robert"), ("Walter", "m", 18, None), ("Joan", "f", 9, None),
                  ("Hugh", "m", 2, None)],
        "Reeve": [("Maud", "f", 40, None), ("Simon", "m", 32, None), ("Alice", "f", 16, None), ("Tom", "m", 6, None)],
        "Colle": [("Geoffrey", "m", 50, "Emma"), ("Emma", "f", 44, "Geoffrey"), ("Roger", "m", 20, None)]}},
    "M5": {
        "Holtmouth": {"Strand": [("Stephen", "m", 46, "Margery"), ("Margery", "f", 40, "Stephen"), ("Nicholas", "m", 18, None),
                                 ("Isolda", "f", 15, None)]},
        "Highcairn": {"Fell": [("Avice", "f", 50, None), ("Ralph", "m", 26, "Beatrice"), ("Beatrice", "f", 24, "Ralph"),
                               ("Hob", "m", 13, None)]},
        "Lowbury": {"Meade": [("Henry", "m", 44, "Cecily"), ("Cecily", "f", 36, "Henry"), ("John", "m", 20, None), ("Rose", "f", 6, None)]},
        "Hartsmoot": {"Holt": [("Gilbert", "m", 38, None), ("Adam", "m", 34, "Sabina"), ("Sabina", "f", 30, "Adam"),
                               ("Lucy", "f", 10, None)]}},
}
KIN = {   # parents of the young; a widowed head's late spouse named (dead before the run: Wat, Osmund, Edith)
    "M1": {"Walter": ["Robert", "Agnes"], "Joan": ["Robert", "Agnes"], "Hugh": ["Robert", "Agnes"], "Alice": ["Maud", "Wat"],
           "Tom": ["Maud", "Wat"], "Roger": ["Geoffrey", "Emma"], "Simon": None},
    "M5": {"Nicholas": ["Stephen", "Margery"], "Isolda": ["Stephen", "Margery"], "Ralph": ["Avice", "Osmund"], "Hob": ["Avice", "Osmund"],
           "John": ["Henry", "Cecily"], "Rose": ["Henry", "Cecily"], "Lucy": ["Gilbert", "Edith"]},
}
SIBLINGS = {"M1": [("Maud", "Simon")], "M5": [("Gilbert", "Adam"), ("Stephen", "Avice"), ("Henry", "Gilbert")]}   # M5: the four
                                                                           # families are one people: heads are brothers and sisters
SKILLS = {
    "M1": {"Ashby": {"livelihoods": ["farmer"], "experts": ["ploughman", "seed_and_harvest"]},
           "Reeve": {"livelihoods": ["herder", "farmer"], "experts": ["dairy", "hay_and_winter"]},
           "Colle": {"livelihoods": ["builder", "woodsman"], "experts": ["wright"]}},
    "M5": {"Strand": {"livelihoods": ["fisher", "salter"], "experts": ["traps_and_runs", "the_pan"]},
           "Fell": {"livelihoods": ["herder", "smith"], "experts": ["stock", "smelting"]},
           "Meade": {"livelihoods": ["farmer"], "experts": ["seed_and_harvest"]},
           "Holt": {"livelihoods": ["hunter", "woodsman"], "experts": ["stalking", "snares"]}},
}
FOOD = {"Strand": "smoked fish", "Holt": "dried meat", "Fell": "cheese"}    # what a home's store holds (grain and beans otherwise)
NO_HOUSE = {"Holt"}                                                          # the wood's family: a tent, no house (design §6)
RUMOUR = {   # true but vague lines, inside the founders' 20 (monoculture_five_worlds.md §1)
    "M1": {"Robert": "The old men said there is good black land two days east, past the ford, where the river widens: they called "
                     "it Broadwater."},
    "M5": {"Stephen": "My sister Avice took her family north toward the high moors after the dark year; Henry went east to the "
                      "river country, and Gilbert into the great wood.",
           "Avice": "After the dark year my brother Stephen went west to the sea; Henry east to the river country; Gilbert into "
                    "the great wood.",
           "Henry": "We parted after the dark year: Stephen to the coast in the west, Avice north to the moors, my brother Gilbert "
                    "south into the wood.",
           "Gilbert": "My brother Henry went east to the river country after the dark year; Stephen to the western sea; Avice "
                      "north to the moors."},
}


KEEPER_LINE = {"forge": "I keep {name}: copper ore smelted with charcoal here makes the tools that wear; the hearth and bellows want "
                         "mending now and then.",
               "mill": "I keep {name}: it grinds grain to flour on the river's water; its stones want dressing and its leat clearing."}


def _stage(age: int) -> str:
    return "infant" if age < 4 else "child" if age < 12 else "youth" if age < 24 else "adult" if age < 64 else "elder"


def pin(key: str, p: dict) -> dict:
    out = {"at": [p["x"], p["y"]], "within": 3.0, "soil": p["soil"]}
    res = [x for x, r_ in (("copper", "seam"), ("stone", "quarry")) if r_ in p["res"]]
    if res:
        out["resources"] = res
    if "mill site" in p["res"]:
        out["has"] = ["mill site"]
    if "fish" in p["res"] or "runs" in p["res"]:
        out["fish"] = True
    if p["land"] == "coast":
        out["on"] = "sea"
    elif p["land"] == "lake":
        out["on"] = "river"
    elif p["land"] in ("rich vale", "farmland") and ("fish" in p["res"] or "mill site" in p["res"] or "runs" in p["res"]):
        out["on"] = "river"
    if out.get("on") == "river" and any(k == "river" and p["name"] in xs for k, xs in D.FEATURES.get(key, [])):
        out["on"] = "big river"                                            # the rivers are laid big (spec), and the generator's walk
                                                                           # never crosses a big river's cells, so a village pinned
                                                                           # "on river" by one got no water: Fallowmere (25 Nov)
    if p["kind"].startswith("home:"):
        hhs = FOUNDERS[key][p["name"]]
        out.update({"households": len(hhs), "food_share": MP.FOOD_SHARE, "heat_share": MP.HEAT_SHARE})
    else:
        out.update({"vacant": True, "room": max(1, int(p["room"])), "land": D.LAND[p["land"]][2]})
    return out


def _home_near(key: str, xy) -> bool:
    """Whether a river's laid point (normalised x, y) is one of the design's homes."""
    w = D.WORLDS[key]
    sz = float(w["size_km"])                                                # as make_peoples.features writes a laid point
    return any(p["kind"].startswith("home:") and abs(round(p["x"] / sz, 4) - xy[0]) < 1e-3 and abs(round(p["y"] / sz, 4) - xy[1]) < 1e-3
               for p in w["places"])


def spec(key: str, seed: int) -> dict:
    w = D.WORLDS[key]
    w["key"] = key
    return {
        "name": f"mono_{key.lower()}", "seed": seed, "days": 200, "lifespan": LIFESPAN,
        "calendar": {"season": "spring", "day": 1, "season_days": 8},
        "children": {"on": True, "dial": "low"},
        "memory": copy.deepcopy(MEMORY),
        "packs": ["wild", "water"],
        "view": "beliefs", "evening": True, "tags": True, "ages": True,
        "prompt": "core", "learning": "record",
        "llm": {"week_stop": 0.9}, "cold_days": [], "incidents": [], "customs": [],
        "gates": {"M6": False},             # everyone is raised to set a wicker trap; only fishers make them. A house that can set but
                                            # not make one is a dependence these worlds test (the Scattering: traps come from the coast),
                                            # not a fault (u3 §7's M6, off by the world's own setting, D2-270)
        "generate": {
            "seed": seed, "size_km": float(w["size_km"]), "settlements": len(w["places"]), "spacing_km": 7.0, "household_size": 4,
            "wild_nodes": 0, "warn_only": ["capacity", "dependence", "laid rivers run where laid"], "settled": "frontier",
            "bounds": {"per_min": 1, "per_spread": 10, "children_max": 40}, "sim": {"start": -10},
            "roads": [[a, b] for a, b, _, _ in w["roads"]],
            "features": [dict(f, flow="big") if f.get("kind") == "river" else f for f in MP.features(key, w)],   # a big river,
                                                                           # so the carved channel holds (M1's medium one ran off it)
            "places": {p["name"]: pin(key, p) for p in w["places"]}}}


def founders(world: dict, key: str) -> dict:
    """The design's founders in place of the generator's people; the generator's households (lines) at each home renamed to the
    design's, matched on land (the farmer to the fields, the herder to the meadows), with their houses, herds, fields and claims."""
    lines_at = {}
    for b in world["buildings"].values():
        if (b.get("fittings") or {}).get("beds") and b.get("household"):
            lines_at.setdefault(b["parcel"].rsplit("_", 1)[0], []).append(b["household"])
    land = {}                                                               # what the generator gave each of its households
    for n in world["nodes"].values():
        for p in n["parcels"].values():
            if p.get("holder"):
                c = land.setdefault(p["holder"], {"field": 0, "meadow": 0})
                if p.get("cover") in c:
                    c[p["cover"]] += int(p.get("size") or 1)
    for h in (world.get("herds") or {}).values():
        if h.get("holder"):
            land.setdefault(h["holder"], {"field": 0, "meadow": 0})["meadow"] += 1
    def wants(hh):                                                          # the farmer first to the fields, the herder to the meadows
        lv = (SKILLS[key].get(hh) or {}).get("livelihoods") or []
        return ("farmer" not in lv, lv.index("farmer") if "farmer" in lv else 9, "herder" not in lv)
    rename = {}
    for home, hhs in FOUNDERS[key].items():
        gen = sorted(set(lines_at.get(home, [])))
        if len(gen) < len(hhs):
            raise SystemExit(f"{key}: {home} has {len(gen)} households generated, the design wants {len(hhs)}")
        left = list(gen)                                                    # matched on land, not on the order of names: by name, the
        for hh in sorted(hhs, key=wants):                                   # Fallowmere field and plough went to the builders (25 Nov)
            lv = (SKILLS[key].get(hh) or {}).get("livelihoods") or []
            by = "field" if "farmer" in lv else "meadow" if "herder" in lv else None
            g = max(left, key=lambda g: ((land.get(g) or {}).get(by, 0), g)) if by else \
                min(left, key=lambda g: (sum((land.get(g) or {}).values()), g))
            rename[g] = hh
            left.remove(g)
    def rn(x):
        return rename.get(x, x)
    for b in world["buildings"].values():
        if b.get("household"):
            b["household"] = rn(b["household"])
            b["name"] = " ".join(rn(t[:-2]) + "'s" if t.endswith("'s") else rn(t) for t in b["name"].split(" "))   # "Hale's Forge"
    for h in (world.get("herds") or {}).values():
        if h.get("holder"):
            h["holder"] = rn(h["holder"])
            h["name"] = " ".join(rn(t) for t in h["name"].split(" "))
    for c in world.get("claims") or []:
        if isinstance(c, dict) and c.get("claimant"):
            c["claimant"] = rn(c["claimant"])
    for n in world["nodes"].values():
        for p in n["parcels"].values():
            if p.get("holder"):
                p["holder"] = rn(p["holder"])
    kin, sibs = KIN[key], SIBLINGS[key]
    everyone = {n: (home, hh, sex, age, partner) for home, hhs in FOUNDERS[key].items() for hh, ms in hhs.items()
                for n, sex, age, partner in ms}
    agents, tree, history = {}, [], []
    for n, (home, hh, sex, age, partner) in everyone.items():
        rel = {}
        for m, (h2, hh2, sx2, _, _) in everyone.items():
            if m == n:
                continue
            if m == partner:
                rel[m] = "your wife" if sex == "m" else "your husband"
            elif n in (kin.get(m) or []):
                rel[m] = "your son" if sx2 == "m" else "your daughter"
            elif m in (kin.get(n) or []):
                rel[m] = "your father" if sx2 == "m" else "your mother"
            elif (n, m) in sibs or (m, n) in sibs or (kin.get(n) and kin.get(n) == kin.get(m)):
                rel[m] = "your brother" if sx2 == "m" else "your sister"
            elif hh2 == hh or h2 == home:
                rel[m] = f"of the {hh2} household"
        agents[n] = {"household": hh, "born": -age, "stage": _stage(age), "sex": sex, "relations": rel, "memories": [],
                     "knows": {"hearth": {"level": "known", "skill": 1.2}}, "aware_of": {}, "holdings": {"crude tool": 1},
                     "concerns": ["food", "family"], "partner": partner, "born_line": hh, "trade": "", "aim": ""}
        tree.append({"name": n, "sex": sex, "born": -age, "died": None, "cause": None, "parents": kin.get(n) or [],
                     "partner": partner, "line": hh, "origin": None, "children": [], "left": None})
    for home, hhs in FOUNDERS[key].items():
        for hh, ms in hhs.items():
            pair = [ms[0][0], ms[0][3] or next(n for n, _, age, _ in ms[1:] if age >= 24)]   # the line's two founders (PE1 names two)
            history.append({"text": f"{pair[0]} and {pair[1]} {hh} came to {home} and built the {hh} house", "who": pair, "day": -20})
    world["agents"], world["tree"], world["history"] = agents, tree, history
    for b in list(world["buildings"]):                                      # a household with no house: a tent (design §6)
        if world["buildings"][b].get("household") in NO_HOUSE:
            del world["buildings"][b]
    for n, a in agents.items():
        if a["household"] in NO_HOUSE and a["stage"] not in ("infant", "child"):
            a["holdings"]["tent" if n == next(m for m, x in agents.items() if x["household"] == a["household"]) else "bedroll"] = 1
    for b in world["buildings"].values():                                   # stores: FIRST days of the household's food
        hh = b.get("household")
        if (b.get("fittings") or {}).get("beds") and hh:
            k = sum(1 for a in agents.values() if a["household"] == hh)
            b["size"] = b["fittings"]["beds"] = max(int(b["fittings"]["beds"]), k + 1)
            st = b.setdefault("stock", {})
            for f_ in ("grain", "beans", "smoked fish", "dried meat", "cheese"):
                st.pop(f_, None)
            if hh in FOOD:
                st[FOOD[hh]] = round(FIRST * k * 1.0)
            else:
                st["grain"], st["beans"] = round(FIRST * k * 0.8), round(FIRST * k * 0.2)
            st["firewood"] = max(int(st.get("firewood") or 0), 6 * k)
    for n, a in agents.items():                                             # the Holt's food in hand: no house to keep it in, and
        if a["household"] in NO_HOUSE:                                      # their place is their home (no house to place them by)
            a["at"] = everyone[n][0]
            if a["stage"] != "infant":                                       # every one past infancy carries a share: a child
                a["holdings"]["dried meat"] = FIRST                             # comes of age soon and then eats from its own hands
    for home, hhs in FOUNDERS[key].items():                                 # the salters' shore: a saltmarsh parcel if the land gave none
        if not any("salter" in (SKILLS[key].get(hh) or {}).get("livelihoods", []) for hh in hhs):
            continue
        parcels = world["nodes"][home]["parcels"]
        if any(p["cover"] == "saltmarsh" for p in parcels.values()):
            continue
        wet = {pid for pid, p in parcels.items() if p["cover"] == "water"}
        cand = sorted((pid for pid, p in parcels.items() if p["cover"] in ("pasture", "meadow", "scrub", "fen") and set(p.get("adj") or []) & wet),
                      key=lambda pid: (-int(parcels[pid].get("size", 1)), pid)) or \
               sorted(pid for pid, p in parcels.items() if p["cover"] in ("pasture", "meadow", "scrub", "fen"))
        if cand:
            p = parcels[cand[0]]
            p.update({"cover": "saltmarsh", "ecosystem": "saltmarsh", "terrain": "saltmarsh",
                      "text": "saltmarsh by the shore, its pools crusted white in summer"})
            p.setdefault("state", {})["salt"] = {"K": 1000, "S": 1000, "r": 0.0}
            world.setdefault("made_by_maker", []).append(f"{home}: {cand[0]} made saltmarsh (the generator gave the salters' shore none)")
    return world


HERD = {"herder": {"cows": 4, "bulls": 1, "young": 2, "in_milk": 2},     # the herders' stock: the most cows and a bull, so calves
         "farmer": {"oxen": 2}}                                              # the farmers' plough team (FA7's ox pair)


def by_livelihood(world: dict, key: str) -> dict:
    """Land, beasts and buildings by what each household lives by (W-203; the generator gives every household one template:
    field 2, meadow 1, pasture 2, forest 1, fen 2, and 2 cows, 2 oxen, a bull): only farmers hold fields and the plough team;
    herders hold the most stock and a bull; a household that neither farms nor herds keeps no beasts; the salters a salt house on
    their saltmarsh. And the start (Q-220, default taken at Zach's 'fix them', 25 Nov): fields bare, no standing crop; each farming
    household's store holds next year's seed (its plots at PLOT_SEED) beside its FIRST days of food."""
    sk = SKILLS[key]
    lv = {hh: (sk.get(hh) or {}).get("livelihoods") or [] for hh in sk}
    plots = {}
    for nid, n in world["nodes"].items():
        for pid, p in n["parcels"].items():
            st = p.get("state") or {}
            st.pop("crop", None)                                            # bare fields (Q-220)
            hh = p.get("holder")
            if hh in lv and p.get("cover") == "field":
                if {"farmer", "fisher"} & set(lv[hh]):                       # fishers keep a garden field: the fishing alone feeds a
                                                                            # household of 4 about 34 food a year (capacity, Holtmouth)
                    plots[hh] = plots.get(hh, 0) + int(p.get("size") or 1)
                else:
                    p.pop("holder", None)                                   # a field its holders cannot work, let go (unheld)
    for c in list(world.get("claims") or []):
        if isinstance(c, dict) and c.get("claimant") in lv and str(c.get("thing", "")).startswith("parcel:"):
            pid = str(c["thing"]).split(":", 1)[1]
            par = next((n["parcels"][pid] for n in world["nodes"].values() if pid in n["parcels"]), None)
            if par is not None and par.get("cover") == "field" and "farmer" not in lv[c["claimant"]]:
                world["claims"].remove(c)
    for hid, h in list((world.get("herds") or {}).items()):
        hh = h.get("holder")
        if hh not in lv:
            continue
        want = {}
        for k in ("herder", "farmer"):
            if k in lv[hh]:
                for a, q in HERD[k].items():
                    want[a] = max(want.get(a, 0), q)
        if not want:
            del world["herds"][hid]                                         # neither farmers nor herders: no beasts
            continue
        for a in ("cows", "oxen", "bulls", "young", "in_milk"):
            h[a] = int(want.get(a, 0))
        h["name"] = f"the {hh} " + ("cattle" if h["cows"] else "oxen")
    held = {h.get("holder") for h in (world.get("herds") or {}).values()}
    for hh, ls in lv.items():                                               # a herder or farmer the template left without beasts
        if hh in held or not ({"herder", "farmer"} & set(ls)):
            continue
        home = next(hm for hm, hhs in FOUNDERS[key].items() if hh in hhs)
        past = next((pid for pid, p in world["nodes"][home]["parcels"].items() if p.get("cover") in ("pasture", "meadow")), None)
        if past:
            want = {}
            for k in ("herder", "farmer"):
                if k in ls:
                    for a, q in HERD[k].items():
                        want[a] = max(want.get(a, 0), q)
            world["herds"][f"{hh.lower()}_cattle"] = {"name": f"the {hh} " + ("cattle" if want.get("cows") else "oxen"), "kind": "cattle",
                                                     "parcel": past, "holder": hh, **{a: int(want.get(a, 0)) for a in ("cows", "oxen", "bulls", "young", "in_milk")}}
    for bid, b in world["buildings"].items():                               # the plough and harness only where a farmer ploughs
        hh = b.get("household")
        if hh in lv and "farmer" not in lv[hh]:
            for g in ("wooden plough", "harness"):
                (b.get("stock") or {}).pop(g, None)
    for hh, ls in lv.items():                                               # the salters' salt house, on their saltmarsh (World 0b's
        if "salter" not in ls or any(b.get("household") == hh and (b.get("fittings") or {}).get("brine pan")   # Salt House)
                                     for b in world["buildings"].values()):
            continue
        home = next(hm for hm, hhs in FOUNDERS[key].items() if hh in hhs)
        marsh = next((pid for pid, p in world["nodes"][home]["parcels"].items() if p.get("cover") == "saltmarsh"), None)
        head = next(n for n, a in world["agents"].items() if a["household"] == hh)
        if marsh:
            world["buildings"][f"{hh.lower()}_salthouse"] = {"parcel": marsh, "household": hh, "structure": "wattle", "name": "the Salt House",
                                                             "fittings": {"brine pan": 1}, "stock": {"firewood": 20}, "keeper": head}
    for b in world["buildings"].values():                                   # next year's seed in the farmers' store (Q-220)
        hh = b.get("household")
        if hh in plots and (b.get("fittings") or {}).get("beds"):
            st = b.setdefault("stock", {})
            st["grain"] = int(st.get("grain") or 0) + plots[hh] * PLOT_SEED
    world.setdefault("made_by_maker", []).append("land, beasts and buildings by livelihood; bare fields and next year's seed (W-203, Q-220)")
    return world


WEIR = {"M1": {"household": "Colle", "home": "Fallowmere", "sections": ["wattle"], "knows": "rough"}}   # Zach, 25 Nov: one section,
# the lowest level: one wattle section, sound (level 5), on the village's river, held by the builders and woodsmen, who know the
# weir only roughly (the lowest working level, data.LEVELS); its crew the household's grown people who know it


def weir(world: dict, key: str) -> dict:
    """The design's weir, if any (WEIR): a monument on the home's largest water parcel, as make_nutrition_runs seeds one."""
    wd = WEIR.get(key)
    if not wd:
        return world
    hh, home = wd["household"], wd["home"]
    pars = world["nodes"][home]["parcels"]
    wet = sorted((pid for pid, p in pars.items() if p.get("cover") == "water"), key=lambda pid: (-int(pars[pid].get("size") or 1), pid))
    if not wet:
        raise DesignRefused(f"{key}: {home} has no water for its weir")
    crew = []
    for n, a in world["agents"].items():
        if a.get("household") == hh and a.get("stage") in ("youth", "adult", "elder"):
            a.setdefault("knows", {})["weir"] = {"level": wd["knows"], "skill": 0.6}
            if a.get("stage") != "youth":
                crew.append(n)
    head = next(n for n, a in world["agents"].items() if a.get("household") == hh)
    world["buildings"][f"{hh.lower()}_weir"] = {
        "parcel": wet[0], "node": home, "household": hh, "name": "the weir", "structure": wd["sections"][0], "monument": "weir",
        "tier": "plain", "fittings": {}, "rooms": [], "gap": "shut", "crew": sorted(crew), "keeper": head,
        "sections": [{"m": m, "foot": False, "level": 5} for m in wd["sections"]]}
    world.setdefault("made_by_maker", []).append(f"{home}: a weir of {len(wd['sections'])} {wd['sections'][0]} section, the {hh}s' (Zach)")
    return world


GEAR = {   # Zach, 25 Nov: "I would give out some snares / nets and maybe a smoke rack" (D5-6)
    "M1": {"Colle": {"each": {"gill net": 1}, "who": "weir", "knows": {"gill net": "rough"}}},          # a net to the weir's keepers
    "M5": {"Holt": {"each": {"snare": 4}, "knows": {}},                                                 # the hunters' snares
           "Strand": {"each": {"gill net": 1}, "knows": {"gill net": "capable"}, "smokehouse": True}},  # the fishers' nets and racks
}
SKILL_AT = {"rough": 0.6, "capable": 1.0, "known": 1.6}


def gear(world: dict, key: str) -> dict:
    """The design's starting gear (GEAR, D5-6): so much of each in the hands of each grown person of the household (or of the weir's
    crew), the craft to use it, and the fishers' smokehouse (a wattle building with smoke racks, apart from the houses, as
    make_nutrition_runs builds one; the racks must stand apart, FITTINGS)."""
    for hh, g in (GEAR.get(key) or {}).items():
        who = [n for n, a in world["agents"].items() if a.get("household") == hh and a.get("stage") in ("adult", "elder")]
        if g.get("who") == "weir":
            weir_ = next((b for b in world["buildings"].values() if b.get("monument") == "weir" and b.get("household") == hh), None)
            who = [n for n in who if weir_ and n in (weir_.get("crew") or [])][:1]
        for n in who:
            a = world["agents"][n]
            for item, q in g["each"].items():
                a.setdefault("holdings", {})[item] = a["holdings"].get(item, 0) + q
            for craft, lvl in g["knows"].items():
                if (a.get("knows") or {}).get(craft, {}).get("level") not in ("capable", "known"):
                    a.setdefault("knows", {})[craft] = {"level": lvl, "skill": SKILL_AT[lvl]}
        if g.get("smokehouse"):
            home = next(hm for hm, hhs in FOUNDERS[key].items() if hh in hhs)
            pars = world["nodes"][home]["parcels"]
            housed = {b["parcel"] for b in world["buildings"].values() if (b.get("fittings") or {}).get("beds")}
            ground = sorted((pid for pid, p in pars.items() if p.get("cover") in ("scrub", "pasture", "meadow", "heath") and pid not in housed),
                            key=lambda q: (pars[q].get("cover") != "scrub", -int(pars[q].get("size") or 1), q))
            if not ground:
                raise DesignRefused(f"{key}: no ground away from the houses for the {hh} smokehouse")
            world["buildings"][f"{hh.lower()}_smokehouse"] = {"parcel": ground[0], "household": hh, "structure": "wattle",
                                                              "name": f"the {hh} Smokehouse", "fittings": {"smoke racks": 1},
                                                              "stock": {"firewood": 12}}
    world.setdefault("made_by_maker", []).append("starting gear: snares, nets, a smokehouse (D5-6)")
    return world


def design_check(world: dict, key: str, cap: dict) -> list:
    """What the design says each home and household has, read from the built world: [failures] (W-203). A build with any is refused."""
    bad = []
    w = D.WORLDS[key]
    sk = SKILLS[key]
    for p in w["places"]:
        if not p["kind"].startswith("home:"):
            continue
        home = p["name"]
        pars = world["nodes"][home]["parcels"]
        fishy = [pid for pid, x in pars.items() if x.get("cover") == "water" and float(((x.get("state") or {}).get("fish") or {}).get("K", 0)) > 0]
        hhs = FOUNDERS[key][home]
        if ("fish" in p["res"] or "runs" in p["res"] or p["land"] == "coast" or
                any("fisher" in (sk.get(hh) or {}).get("livelihoods", []) for hh in hhs)) and not fishy:
            bad.append(f"{home}: no water with fish (its design: {p['land']}, {p['res']})")
        c = (cap or {}).get(home) or {}
        if c.get("people") and float(c.get("worked", 0)) < WORKED_MIN * float(c["people"]):
            bad.append(f"{home}: feeds {c.get('worked')} at good work, under {WORKED_MIN}x its {c['people']}")
        for hh in hhs:
            ls = (sk.get(hh) or {}).get("livelihoods") or []
            herd = [h for h in (world.get("herds") or {}).values() if h.get("holder") == hh]
            fields = sum(int(x.get("size") or 1) for x in pars.values() if x.get("holder") == hh and x.get("cover") == "field")
            if ls[:1] == ["farmer"] and fields < 2:                         # farming the main livelihood (a herder who also farms,
                bad.append(f"{hh}: farmers with {fields} plots of field")   # Reeve, clears his own: Fallowmere has one field)
            if not ({"farmer", "fisher"} & set(ls)) and fields:
                bad.append(f"{hh}: {fields} plots of field and neither farmers nor fishers")
            if "herder" in ls and not any(int(h.get("cows", 0)) >= 3 and int(h.get("bulls", 0)) >= 1 for h in herd):
                bad.append(f"{hh}: herders without 3 cows and a bull")
            if not ({"herder", "farmer"} & set(ls)) and herd:
                bad.append(f"{hh}: beasts and neither farmers nor herders")
            if "salter" in ls and not any(b.get("household") == hh and (b.get("fittings") or {}).get("brine pan") for b in world["buildings"].values()):
                bad.append(f"{hh}: salters without a salt house")
            if "salter" in ls and not any(x.get("cover") in ("saltmarsh",) for x in pars.values()):
                bad.append(f"{hh}: salters without a saltmarsh")
            if "farmer" in ls:
                seed = sum(float((b.get("stock") or {}).get("grain", 0)) for b in world["buildings"].values() if b.get("household") == hh)
                if seed < fields * PLOT_SEED:
                    bad.append(f"{hh}: {seed:g} grain for {fields} plots' seed ({fields * PLOT_SEED})")
        for x in pars.values():
            if (x.get("state") or {}).get("crop"):
                bad.append(f"{home}: a standing crop at the start (Q-220: bare fields)")
                break
    from cybertron2.capacity import model as CM                             # the first 64 days at good work: no home short
    with contextlib.redirect_stdout(io.StringIO()):
        r = CM.analyse(copy.deepcopy(world), levels=("worked",), horizon=64)
    for home in FOUNDERS[key]:
        h = ((r["nodes"].get(home) or {}).get("horizon") or {}).get("worked") or {}
        if h.get("first_short") is not None:
            bad.append(f"{home}: short from day {h['first_short']} for {h.get('short_days')} days in the first 64 at good work")
    return bad


def explore(world: dict, key: str) -> dict:
    """Every place unexplored but each group's home and the places a day from it (D4-47), which its people know (`places`)."""
    w = D.WORLDS[key]
    near = {}
    for a, b, d, _ in w["roads"]:
        if d == 1:
            near.setdefault(a, set()).add(b)
            near.setdefault(b, set()).add(a)
    homes = {p["name"] for p in w["places"] if p["kind"].startswith("home:")}
    for nid, n in world["nodes"].items():
        n["unexplored"] = True
    for a in world["agents"].values():
        home = next(h for h, hhs in FOUNDERS[key].items() if a["household"] in hhs)
        a["places"] = sorted({home} | near.get(home, set()))
    if len(homes) == 1:                                                    # one group: its known places need no mark at all
        for nid in next(iter(world["agents"].values()))["places"]:
            world["nodes"][nid].pop("unexplored", None)
    return world


def seed_lines(world: dict, key: str) -> dict:
    from cybertron2.engine import livelihoods as LV
    world["skills"] = {"depth": "full", "households": copy.deepcopy(SKILLS[key]),
                       "couple": {"capital_knowledge": True, "livelihood_land": True, "crafts_capital": True, "gates": True}}
    report = LV.fill(world)
    for n, a in world["agents"].items():                                    # trap-setting without a maker in reach (gate): only fishers
        if "fisher" not in (SKILLS[key].get(a["household"]) or {}).get("livelihoods", []):
            for c in ("trap in water", "wicker trap", "wicker traps"):
                (a.get("knows") or {}).pop(c, None)
    home_of = {hh: home for home, hhs in FOUNDERS[key].items() for hh in hhs}
    if len(FOUNDERS[key]) > 1:                                              # groups lost to each other (World 5): the fill seeds every
        for n, a in world["agents"].items():                                # household as a neighbour of every other (u11 step 8); here no
            far = [hh for hh, home in home_of.items() if home != home_of[a["household"]]]   # group knows another's crafts or place but by
            a["aware_of"] = {c: v for c, v in (a.get("aware_of") or {}).items() if not any(h in str(v) for h in far)}   # the
            a["kept"] = [k for k in a.get("kept") or [] if not any(h in k.get("text", "") for h in far)]              # rumour lines
            for c in ("trap in water", "wicker trap", "wicker traps"):
                if c in (a.get("aware_of") or {}) and "fisher" not in (SKILLS[key].get(a["household"]) or {}).get("livelihoods", []):
                    a["aware_of"].pop(c, None)
    keeper_of = {b.get("keeper"): b for b in world["buildings"].values() if b.get("keeper")}
    for n, b in keeper_of.items():                                          # a holding's keeper line where founders.py has no template
        a = world["agents"].get(n)                                          # (smith, miller, farmer: L-201)
        if a is None or any(k.get("source") == "a holding" for k in a.get("kept") or []):
            continue
        kind = next((k for k in KEEPER_LINE if k in b["name"].lower() or (b.get("fittings") or {}).get(k)), None)
        if kind:
            a.setdefault("kept", []).insert(0, {"text": KEEPER_LINE[kind].format(name=b["name"]), "source": "a holding"})
    for n, a in world["agents"].items():
        a.pop("memories", None)
        extra = [{"text": RUMOUR[key][n], "source": "family lore"}] if n in RUMOUR.get(key, {}) else []
        a["kept"] = [{"text": GOAL, "fixed": True, "tag": "goal"}] + extra + [k for k in (a.get("kept") or []) if k.get("text") != GOAL]
        while len(a["kept"]) > CAP:
            a["kept"].pop()
    return report


def arm(world: dict, model: str) -> dict:
    w = copy.deepcopy(world)
    w["name"] = f"{world['name']}_{model.replace('claude-', '').replace('-', '')}"
    hhs = sorted({a["household"] for a in w["agents"].values()})
    w["household_models"] = {h: model for h in hhs}
    w["cast"] = {"head": model, "middle": model, "rest": model, "youth": model}
    for a in w["agents"].values():
        if a["stage"] in ("youth", "adult", "elder"):
            a["model"] = model
    return w


class DesignRefused(Exception):
    """The built world does not meet its design (design_check)."""


def make(key: str, seed: int, models) -> dict:
    from cybertron2.landgen.settle import Refused
    s = spec(key, seed)
    relaxed = []
    for _ in range(40):                                                    # a place no site meets: its pins eased one step at a time,
        try:                                                               # each step reported (the design against what the land allows)
            with contextlib.redirect_stdout(io.StringIO()):
                world, cells, report = W.generate(copy.deepcopy(s), people=True)
            if "laid rivers run where laid" in (report.get("refused") or []):
                rivers = [f for f in s["generate"]["features"] if f.get("kind") == "river" and len(f["through"]) > 2]
                if rivers:
                    for f in rivers:                                       # from the end farther from a home: cut from the source, a
                        homes_at = [i for i, xy in enumerate(f["through"]) if _home_near(key, xy)]   # home by the source lost its river
                        tail = bool(homes_at) and min(homes_at) <= len(f["through"]) - 1 - max(homes_at)  # (Fallowmere, 25 Nov)
                        f["through"] = f["through"][:-1] if tail else f["through"][1:]
                    relaxed.append("rivers shortened by a place at the end away from the homes: the land turned the laid channel aside")
                    continue
            break
        except Refused as e:
            name = str(e).split(":", 1)[0]
            p = s["generate"]["places"].get(name)
            if p is None:
                raise
            if p.get("within", 3.0) < 9.0:
                p["within"] = p.get("within", 3.0) + 3.0
                relaxed.append(f"{name}: within {p['within']} km")
            elif p.get("soil") in ("rich", "poor"):
                relaxed.append(f"{name}: soil {p.pop('soil')} not required")
            elif p.get("has"):
                relaxed.append(f"{name}: {p.pop('has')} not required")
            elif p.get("on") and not p.get("households"):                 # a home's water is its livelihood: never eased away (the
                relaxed.append(f"{name}: on {p.pop('on')} not required")    # design check refuses the build instead)
            elif p.get("resources"):
                relaxed.append(f"{name}: {p.pop('resources')} not required")
            else:
                raise
    else:
        raise SystemExit(f"{key}: still refused after easing {relaxed}")
    if report.get("refused"):
        raise SystemExit(f"{key}: refused: {report['refused']}")
    print(key, "pins eased:", relaxed or "none", flush=True)
    world = gear(weir(by_livelihood(MP.water_stocks(founders(world, key)), key), key), key)
    world = explore(world, key)
    fill = seed_lines(world, key)
    from cybertron2.landgen import gate_check as GC
    gate = GC.check(world)
    try:
        cap = MP.capacity(world)
    except Exception as e:  # noqa: BLE001
        cap = {"error": str(e)[:300]}
    bad_design = design_check(world, key, cap)                              # W-203: refused, never written, if the design is not met
    if bad_design:
        raise DesignRefused(f"{key} (seed {seed}): " + "; ".join(bad_design))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{key.lower()}.yaml")
    W.write(world, cells, report, path, picture=os.path.join(OUT, f"{key.lower()}.png"))
    cmp_ = MP.compare(key, world)
    bad = [x for x in cmp_["roads"] if x["generated"] != x["designed"]]
    json.dump({"refused": report.get("refused"), "pins_eased": relaxed, "gate": gate, "fill": fill, "capacity": cap, "roads_off": bad, "compare": cmp_},
              open(os.path.join(OUT, f"{key.lower()}.check.json"), "w"), indent=1, default=str)
    for m in models:
        a = arm(world, m)
        with open(os.path.join(OUT, f"{a['name']}.yaml"), "w") as f:
            f.write(f"# {a['name']}: {D.WORLDS[key]['title']}; every person {m}; made by cybertron2/specs/make_mono_worlds.py. "
                    "Do not edit.\n")
            yaml.safe_dump(a, f, sort_keys=False, allow_unicode=True, width=200)
    real = [x["text"][:140] for x in gate["refuse"] if "YOUR GOAL" not in x["text"]]
    print(key, "| roads off design:", len(bad), "of", len(cmp_["roads"]), "| gate refusals beyond the goal line:", len(real),
          "| capacity:", json.dumps(cap, default=str)[:400], flush=True)
    for x in real[:12]:
        print("   ", x)
    for x in bad[:12]:
        print("   ", x)
    return {"world": world, "gate": gate, "capacity": cap, "bad": bad}


if __name__ == "__main__":
    argv = sys.argv[1:]
    seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else 2311
    models = argv[argv.index("--models") + 1].split(",") if "--models" in argv else MODELS
    keys = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in ("--seed", "--models", "--tries"))]
    tries = int(argv[argv.index("--tries") + 1]) if "--tries" in argv else 6
    for k in keys or ["M1", "M5"]:
        for i in range(tries):                                              # a seed whose land misses the design: the next seed
            try:
                make(k, seed + i, models)
                break
            except DesignRefused as e:
                print("design refused:", e, flush=True)
        else:
            raise SystemExit(f"{k}: no seed of {tries} from {seed} meets the design")
