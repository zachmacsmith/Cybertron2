"""The monoculture worlds as generated worlds (W-107): Fallowmere (M1) and the Scattering (M5) from mono_design.py
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
from cybertron2.specs.make_world0 import CAP, GOAL, MEMORY  # noqa: E402
from cybertron2.landgen import write as W  # noqa: E402

MP.D = D                                   # the peoples maker's features and comparison read this design
OUT = os.path.join(HERE, "mono")
LIFESPAN = 64
FIRST = 16                                 # days of food in store at the start (spring day 1; the first harvest about day 16 to 20)
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
KIN = {   # who is whose child, sibling (within a household, by position): parents of the young
    "M1": {"Walter": ["Robert", "Agnes"], "Joan": ["Robert", "Agnes"], "Hugh": ["Robert", "Agnes"], "Alice": ["Maud"], "Tom": ["Maud"],
           "Roger": ["Geoffrey", "Emma"], "Simon": None},
    "M5": {"Nicholas": ["Stephen", "Margery"], "Isolda": ["Stephen", "Margery"], "Ralph": ["Avice"], "Hob": ["Avice"],
           "John": ["Henry", "Cecily"], "Rose": ["Henry", "Cecily"], "Lucy": ["Gilbert"]},
}
SIBLINGS = {"M1": [("Maud", "Simon")], "M5": [("Gilbert", "Adam"), ("Stephen", "Avice"), ("Henry", "Gilbert")]}   # M5: the four
                                                                           # families are one people: heads are brothers and sisters
SKILLS = {
    "M1": {"Ashby": {"livelihoods": ["farmer"], "experts": ["ploughman", "seed_and_harvest"]},
           "Reeve": {"livelihoods": ["farmer", "herder"], "experts": ["dairy", "hay_and_winter"]},
           "Colle": {"livelihoods": ["woodsman", "builder"], "experts": ["wright"]}},
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
    if p["kind"].startswith("home:"):
        hhs = FOUNDERS[key][p["name"]]
        out.update({"households": len(hhs), "food_share": MP.FOOD_SHARE, "heat_share": MP.HEAT_SHARE})
    else:
        out.update({"vacant": True, "room": max(1, int(p["room"])), "land": D.LAND[p["land"]][2]})
    return out


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
        "generate": {
            "seed": seed, "size_km": float(w["size_km"]), "settlements": len(w["places"]), "spacing_km": 7.0, "household_size": 4,
            "wild_nodes": 0, "warn_only": ["capacity", "dependence"], "settled": "frontier",
            "bounds": {"per_min": 3, "per_spread": 2, "children_max": 2}, "sim": {"start": -10},
            "roads": [[a, b] for a, b, _, _ in w["roads"]],
            "features": MP.features(key, w),
            "places": {p["name"]: pin(key, p) for p in w["places"]}}}


def founders(world: dict, key: str) -> dict:
    """The design's founders in place of the generator's people; the generator's households (lines) at each home renamed to the
    design's, in order, with their houses, herds, fields and claims."""
    lines_at = {}
    for b in world["buildings"].values():
        if (b.get("fittings") or {}).get("beds") and b.get("household"):
            lines_at.setdefault(b["parcel"].rsplit("_", 1)[0], []).append(b["household"])
    rename = {}
    for home, hhs in FOUNDERS[key].items():
        gen = sorted(set(lines_at.get(home, [])))
        if len(gen) < len(hhs):
            raise SystemExit(f"{key}: {home} has {len(gen)} households generated, the design wants {len(hhs)}")
        rename.update(dict(zip(gen, hhs)))
    def rn(x):
        return rename.get(x, x)
    for b in world["buildings"].values():
        if b.get("household"):
            b["household"] = rn(b["household"])
            b["name"] = " ".join(rn(t) for t in b["name"].split(" "))
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
            history.append({"text": f"{ms[0][0]} {hh} came to {home} and built the {hh} household", "who": [ms[0][0]], "day": -20})
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
    for n, a in agents.items():                                             # the Holt's food in hand: no house to keep it in
        if a["household"] in NO_HOUSE and a["stage"] not in ("infant", "child"):
            a["holdings"]["dried meat"] = FIRST
    return world


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
    for n, a in world["agents"].items():
        a.pop("memories", None)
        extra = [{"text": RUMOUR[key][n], "source": "family lore"}] if n in RUMOUR.get(key, {}) else []
        a["kept"] = [{"text": GOAL, "fixed": True}] + extra + [k for k in (a.get("kept") or []) if k.get("text") != GOAL]
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


def make(key: str, seed: int, models) -> dict:
    from cybertron2.landgen.settle import Refused
    s = spec(key, seed)
    relaxed = []
    for _ in range(40):                                                    # a place no site meets: its pins eased one step at a time,
        try:                                                               # each step reported (the design against what the land allows)
            with contextlib.redirect_stdout(io.StringIO()):
                world, cells, report = W.generate(copy.deepcopy(s), people=True)
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
            elif p.get("on"):
                relaxed.append(f"{name}: on {p.pop('on')} not required")
            elif p.get("resources"):
                relaxed.append(f"{name}: {p.pop('resources')} not required")
            else:
                raise
    else:
        raise SystemExit(f"{key}: still refused after easing {relaxed}")
    if report.get("refused"):
        raise SystemExit(f"{key}: refused: {report['refused']}")
    print(key, "pins eased:", relaxed or "none", flush=True)
    world = MP.water_stocks(founders(world, key))
    world = explore(world, key)
    fill = seed_lines(world, key)
    from cybertron2.landgen import gate_check as GC
    gate = GC.check(world)
    try:
        cap = MP.capacity(world)
    except Exception as e:  # noqa: BLE001
        cap = {"error": str(e)[:300]}
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
    keys = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in ("--seed", "--models"))]
    for k in keys or ["M1", "M5"]:
        make(k, seed, models)
