"""What each person knows how to do (proposals/knowledge.md; D4-24, D4-33): technique records with four levels, how they rise,
cards by level, today's options with near misses, and refusals that name the shortfall.

Mind.know[tech] = {level: aware|rough|capable|known, skill, seen, wins, fails, source, since}. Basic techniques need no record.
The views take `Here` and `Mind` only (D4-35); changing a level goes through the `learn` primitive.
"""
from __future__ import annotations

import math

from cybertron2.engine.data import RESOURCES, BLUEPRINTS, FITTINGS, ITEMS, LEVELS, SKILL, SKILL_WORDS, TECHNIQUES, TRY


def basic(tech) -> bool:
    """Known to everyone: a basic craft of a pack the world has on (D4-103)."""
    from cybertron2.engine import packs as PK
    return bool(TECHNIQUES[tech].get("basic")) and PK.on(TECHNIQUES[tech])


def label(tech) -> str:
    return TECHNIQUES[tech]["label"].split(" (")[0]


def resolve(x, verb=None):
    """A technique from what an agent wrote: its name, an alias, or a word of its label (one done by `verb` first); only those of
    the world's packs (D4-103)."""
    from cybertron2.engine import packs as PK
    x = str(x or "").strip().lower()
    live = PK.techniques()
    order = sorted(live, key=lambda t: TECHNIQUES[t]["verb"] != verb) if verb else list(live)
    if x in live and (verb is None or TECHNIQUES[x]["verb"] == verb):
        return x
    for t in order:
        d = TECHNIQUES[t]
        if x == t or x in d.get("aliases", []) or x == d["label"].lower() or x == label(t).lower():
            return t
    return None


# ---------------------------------------------------------------------- skill by practice (D2-52; 02n §4: calibrate)
def curve(tech):
    if (TECHNIQUES.get(tech) or {}).get("curve") == "hard":                    # the hunt's own curve (brief 4 §2.6)
        lo, hi = SKILL["hard"]
        return float(lo), float(hi)
    lo, hi = SKILL["basic" if basic(tech) else "trade"]
    return float(lo), float(hi)


def hard(tech) -> bool:
    """The hunt's curve (brief 4 §2.6; brief 4c §3.1): a multiplier on the bare-handed novice's chance."""
    return (TECHNIQUES.get(tech) or {}).get("curve") == "hard"


def tau(tech) -> float:
    return float(SKILL["tau"])


def skill_of_practice(tech, p) -> float:
    """Skill from units of practice: work at large rises toward its top as 1 - e^(-p / tau) (D2-52); the hunt geometrically, from x1
    to its top in `top_hard` units (brief 4c §3.3: about x3 half way)."""
    lo, hi = curve(tech)
    if hard(tech):
        return round(lo * (hi / lo) ** min(1.0, max(0.0, p) / float(SKILL["top_hard"])), 4)
    return round(lo + (hi - lo) * (1 - math.exp(-max(0.0, p) / tau(tech))), 4)


def practice_of_skill(tech, sk) -> float:
    lo, hi = curve(tech)
    if hard(tech):
        return float(SKILL["top_hard"]) * min(1.0, max(0.0, math.log(max(float(sk), lo) / lo) / math.log(hi / lo)))
    share = min(0.999, max(0.0, (sk - lo) / (hi - lo)))
    return -tau(tech) * math.log(1 - share)


def practice_x(here, tech) -> float:
    """How much a unit of practice counts for this person (brief 4c §3.3): the hunt's pace is set at the default lifespan and scales
    with the world's (D2-153), and a youth learns it `youth_hard` times as fast; other work counts as it is."""
    if not hard(tech):
        return 1.0
    from cybertron2.engine.data import LIFE
    x = float(LIFE["lifespan"]) / float(here.life()["lifespan"])
    if here.me.get("stage") == "youth":
        x *= float(SKILL["youth_hard"])
    return x


# ---------------------------------------------------------------------- the store (engine side: seeding and the learn primitive)
def seed(w, name, spec_agent) -> None:
    k = w.s["know"].setdefault(name, {})
    for tech, v in (spec_agent.get("knows") or {}).items():
        if tech in TECHNIQUES:                                                  # basic work too, for its practice (D2-52)
            lvl, sk = (v, None) if isinstance(v, str) else (v.get("level", "known"), v.get("skill"))
            sk = float(sk) if sk is not None else curve(tech)[0]
            k[tech] = {"level": "known" if basic(tech) else lvl, "skill": sk, "seen": 0, "wins": 0, "fails": 0,
                       "source": "from your upbringing", "since": -1}
    for tech, src in (spec_agent.get("aware_of") or {}).items():
        if tech in TECHNIQUES and not basic(tech):
            k.setdefault(tech, {"level": "aware", "skill": 0.6, "seen": 0, "wins": 0, "fails": 0, "source": src, "since": -1})
    lv = ("rough", "capable", "known")                                         # a seeded mason walls (D4-97): worlds written before
    mason = [r for t, r in k.items() if TECHNIQUES[t].get("trade") == "mason" and t != "wall" and r["level"] in lv]   # walling gated stone
    if mason and "wall" not in k:
        best = max(mason, key=lambda r: lv.index(r["level"]))
        k["wall"] = {**best, "source": "from your upbringing", "since": -1}


def seed_world(w) -> list:
    """D2-129: each technique in KNOWN_SOMEWHERE that nobody knows is given to one person, chosen by a keyed draw among the adults whose
    trade fits (else any adult). Returns [(tech, person)] seeded."""
    from cybertron2.engine.data import KNOWN_SOMEWHERE
    from cybertron2.engine import packs as PK
    out = []
    for tech, words in KNOWN_SOMEWHERE.items():
        if not PK.on(TECHNIQUES[tech], PK.of(w)):                              # a craft of a pack off (W-69: dibbling, with farming)
            continue
        if any((w.s["know"].get(n) or {}).get(tech, {}).get("level") == "known" for n in w.living()):
            continue
        adults = [n for n in w.living() if w.s["people"][n]["stage"] == "adult"]
        fit = [n for n in adults if any(x in str(w.s["people"][n].get("trade") or "").lower() for x in words)] or adults
        if not fit:
            continue
        who = sorted(fit)[int(w.rng("known-somewhere", tech).random() * len(fit))]
        w.s["know"].setdefault(who, {})[tech] = {"level": "known", "skill": curve(tech)[0], "seen": 0, "wins": 0, "fails": 0,
                                                 "source": "from your upbringing", "since": -1}
        out.append((tech, who))
    return out


def _set(w, name, tech, lvl, source) -> bool:
    k = w.s["know"].setdefault(name, {})
    r = k.get(tech)
    if r is None:
        k[tech] = {"level": lvl, "skill": 0.6, "seen": 0, "wins": 0, "fails": 0, "source": source, "since": w.d}
        return True
    if LEVELS.index(lvl) > LEVELS.index(r["level"]):
        r.update(level=lvl, since=w.d, source=source)
        return True
    return False


# ---------------------------------------------------------------------- views
def rec(mind, tech):
    return mind.know.get(tech)


def level(mind, tech):
    if tech not in TECHNIQUES:
        return None
    from cybertron2.engine import packs as PK
    if not PK.on(TECHNIQUES[tech], getattr(mind, "packs", None)):          # not a craft of this world (D4-103)
        return None
    if basic(tech):
        return "known"
    r = rec(mind, tech)
    return r["level"] if r else None


def skill(mind, tech) -> float:
    """The multiplier one's practice gives (D2-52): basic work 1.0 to 1.5, a trade 0.5 to 2.0, the hunt 1 to 8 (brief 4c §3.1)."""
    r = rec(mind, tech)
    sk = float(r.get("skill", curve(tech)[0])) if r else (curve(tech)[0] if basic(tech) else 1.0)
    return max(curve(tech)[0], sk) if hard(tech) else sk                    # never below the bare-handed novice (brief 4c §3.1)


def skill_word(x, tech=None) -> str:
    lo, hi = curve(tech) if tech else SKILL["trade"]
    share = (x - lo) / (hi - lo)
    word = next(word for t, word in SKILL_WORDS if share >= t)
    return "ordinary" if word == "novice" and tech and basic(tech) else word


def where(here, tech, graves=False) -> list:
    """The sites here where a technique can be done: [(kind, id, label)]; with `graves`, graves without a cairn as well (D4-99)."""
    at = TECHNIQUES[tech].get("at")
    if not at:
        return [("anywhere", None, "anywhere")]
    out = []
    if at.get("things"):                                                       # work on a thing at a spot: the dead (D2-96), a dead
        kinds = at["things"] if isinstance(at["things"], list) else [at["things"]]   # beast (brief 3 §4)
        out = [("thing", cid, f"the body of {c['of']} at {here.spot_name(c)}") for cid, c in here.bodies().items()] if "body" in kinds else []
        if "carcass" in kinds:
            out += [("thing", cid, f"the dead {c['beast']} at {here.spot_name(c)}") for cid, c in here.carcasses().items()]
        if graves:                                                             # a cairn over a grave already dug (D4-99)
            out += [("thing", cid, f"the grave of {c['of']} at {here.spot_name(c)}") for cid, c in here.graves().items()]
        return out
    for c in at.get("covers", []):
        out += [("parcel", pid, p["name"]) for pid, p in here.parcels().items() if p["cover"] == c]
    for f in at.get("fittings", []):
        out += [("building", bid, here.buildings()[bid]["name"]) for bid in here.fittings(f)]
    if at.get("building"):
        out += [("building", bid, b["name"]) for bid, b in here.buildings().items() if not b.get("unfinished")]
    return out


def draws_at(here, tech, pid) -> str | None:
    """The stock a technique draws at a parcel: its own, else its `draws_else` where its own is not there (withies: the willow, else
    young growth, u3 §1.1); the edge draws the shallows where they are, else the water's fish (u1 §2)."""
    t = TECHNIQUES[tech]
    d = t.get("draws")
    res = (here.parcels().get(pid) or {}).get("res") or {}
    if d not in res and t.get("draws_else") and t["draws_else"] in res:
        return t["draws_else"]
    return d


def ready(here, tech, kind, key, a=None) -> str:
    """'' if the site can be worked by this technique now, else why not (what it draws on, in its state)."""
    t = TECHNIQUES[tech]
    y = (t.get("yield") or {}).get("kind")
    if t.get("seasons") and here.calendar()["season"] not in t["seasons"]:
        return f"{label(tech)} is done in {' and '.join(t['seasons'])}"
    if kind == "parcel" and y in ("sow", "break", "tend", "manure", "crop", "herd", "milk", "slaughter", "works", "select", "fence", "gate",
                                  "pull", "dig_strip"):
        from cybertron2.engine import farm as FM
        return FM.ready(here, tech, key, a)                                  # on whose holding (D2-172)
    if kind == "parcel":
        p = here.parcels()[key]
        d = draws_at(here, tech, key)
        if t.get("ice") and here.ice(key) != "open":                          # a freeze (u1 §4; D2-265)
            return (f"the edges of {p['name']} are ice" if t["ice"] == "edge" else
                    f"{p['name']} is frozen at its edges: there is no open water to fish from the bank")
        if t.get("run") and here.run_here(key) and here.pinch(key) > 0:      # a run passing there today (Q-79 bug 1; u1 §5)
            return ""
        if d in RESOURCES and d not in p["res"]:                              # any stock the data names (D4-103)
            return f"there is no {({'plants': 'wild food', 'grass': 'grass to cut', 'dead': 'dead wood', 'young': 'young growth', 'willow': 'willow to cut', 'shallows': 'shallow water to fish'}).get(d, d)} at {p['name']}"
        if d == "willow" and p["res"][d]["S"] < 0.5:
            return f"the willow at {p['name']} is cut back: no rods left worth cutting until spring"
        if d in ("dead", "young") and p["res"][d]["S"] < 0.5:
            return f"there is no {'dead wood' if d == 'dead' else 'young growth'} left to take at {p['name']}"
        if d == "grass" and p["res"][d]["S"] <= 0.2 * p["res"][d]["K"]:
            return f"{p['name']} is grazed too short to cut"
        if d == "dung" and p["res"][d]["S"] < 1:
            return f"there is little dung on {p['name']}"
        if d in ("seam",) and p["res"][d]["S"] <= 1e-9:
            return f"the seam at {p['name']} is worked out"
        if d == "wild plants":                                                # the wild plants in season here (D2-200)
            from cybertron2.engine import wild as WL
            if not WL.in_season(here, key):
                return f"there is nothing in season to gather at {p['name']}"
        if d == "plants" and p["res"][d]["S"] <= (here.p["refuge"] + 0.02) * p["res"][d]["K"]:
            return f"{p['name']} is picked bare"
        if d == "fish" and p["res"][d]["S"] <= (here.p["refuge"] + 0.02) * p["res"][d]["K"]:
            return f"the fish at {p['name']} are fished out for now"
        if d == "shallows" and p["res"][d]["S"] <= (here.p["refuge"] + 0.02) * p["res"][d]["K"]:   # never "no fish" (u2 §4.6)
            return f"the shallows of {p['name']} are fished out for now, and nothing is running"
        if d == "wood" and p["res"][d]["S"] <= 0.5:
            return f"there is no standing timber left in {p['name']}"
        if y == "sow" and p.get("crop") and p["crop"].get("left", 0) > 1e-9:
            return f"{p['name']} already has a crop in it"
        if y in ("crop", "tend"):
            c = p.get("crop")
            if not c or c.get("left", 0) <= 1e-9:
                return f"there is no crop in {p['name']}"
            if y == "crop" and here.day < int(c.get("ripe_day", 0)):
                return f"the {c.get('kind', 'crop')} in {p['name']} is not ripe yet"
            if y == "tend" and here.day >= int(c.get("ripe_day", 0)):
                return f"the {c.get('kind', 'crop')} in {p['name']} is ripe: past weeding"
            if y == "tend" and c.get("weeded", 0) >= here.p["farming"]["weed_max"] - 1e-9:
                return f"the {c.get('kind', 'crop')} in {p['name']} is as clean as weeding makes it"
        if d == "herd":
            hs = [h for h in here.herds().values() if h["parcel"] == key]
            if not hs:
                return f"there are no beasts on {p['name']}"
            if y == "milk":
                h = hs[0]
                if int(h.get("in_milk", 0)) <= 0:
                    return "no cow there is in milk"
                if h["milked"]["day"] == here.day and h["milked"]["n"] >= int(h["in_milk"]):
                    by = h["milked"].get("by") or []
                    return f"the cows in milk have all been milked today ({h['in_milk']} of them)" + (f", by {', '.join(by)}" if by else "")
            if y == "slaughter" and hs[0]["count"] <= 0:
                return "there are no beasts left"
    if kind == "thing":
        c = here.thing(key)
        if not c or not (c.get("body") or c.get("beast")):                    # a body, or a dead beast (brief 3 §4)
            return "there is no body there"
        if c.get("burnt") is not None:
            return "it has been burned; ash and bone are left"
        if c.get("buried") is not None:
            if str((a or {}).get("method", "")).lower() == "cairn":            # a cairn over the grave, after the burial (D4-99)
                return f"the grave of {c['of']} already has a cairn" if c.get("cairn") else ""
            return f"{c['of']} is already buried" + ("" if c.get("cairn") else "; a cairn of stones can still be raised over the grave "
                                                      "(method cairn, 3 stone)")
        return ""
    if kind == "building" and t.get("process") and t["process"] in ("keeping smoke", "hard cure", "hearth rack"):   # u4: the room,
        from cybertron2.engine import process as PROC                                                              # the structure
        why = PROC.refuse_load(here, tech, key)
        if why:
            return why
    if kind == "building" and any(FITTINGS[f].get("spring") for f in (t.get("at") or {}).get("fittings") or [] if f in FITTINGS):
        sp = next(FITTINGS[f]["spring"] for f in t["at"]["fittings"] if FITTINGS.get(f, {}).get("spring"))   # brine drawn there (5 §4b.3)
        if not here.near_spring(here.buildings()[key]["parcel"], sp):
            return f"there is no {sp} spring at or beside {here.buildings()[key]['name']} to draw from"
    if kind == "building" and y == "repair" and here.buildings()[key].get("monument") == "weir":   # a weir: by its sections (D2-210)
        from cybertron2.engine import wild as WL
        if all(int(sc["level"]) >= 5 for sc in WL.sections(here.buildings()[key])) and not here.buildings()[key].get("mending"):
            return f"{here.buildings()[key]['name']} is sound"
    elif kind == "building" and y == "repair" and (here.buildings()[key]["level"] >= 5 if here.buildings()[key].get("level") is not None
                                                    else here.buildings()[key]["condition"] >= 2):
        return f"{here.buildings()[key]['name']} is sound"
    from cybertron2.engine import farm as FM
    if kind == "parcel" and y == "clear_built" and any(c.get("left", 0) > 1e-9 for _, _, c in FM.standing(here.parcels()[key])):
        return f"{here.parcels()[key]['name']} has a crop standing in it"
    return ""


def available(here, item, who=None, extra=None) -> float:
    """How much of a good one can use here: what one carries and the stores here one may take from (and a party's, acting for it)."""
    cids = here.takeable(who) + ([extra] if extra and extra not in here.takeable(who) else [])
    return sum(max(0.0, here.contents(cid).get(item, 0.0) - here.held_back(cid, item)) for cid in cids)   # whose ever they are, less
                                                                              # what the household's book holds back (u6 §4)


def pick_inputs(here, needs: dict, mult=1.0, extra=None) -> dict:
    """The inputs as goods: an entry whose value is a table means one of these (the first one at hand in full: D4-46's fuel)."""
    out = {}
    for item, q in (needs or {}).items():
        if isinstance(q, dict):
            item, q = next(((i, n) for i, n in q.items() if available(here, i, extra=extra) + 1e-9 >= n * mult), next(iter(q.items())))
        out[item] = out.get(item, 0.0) + q
    return out


def inputs_words(needs: dict, batch=False) -> str:
    return ", ".join(" or ".join(f"{n:g} {i}" for i, n in q.items()) if isinstance(q, dict) else ("up to " if batch else "") + f"{q:g} {item}"
                     for item, q in (needs or {}).items())


def batch_share(here, tech, mult=1.0, extra=None) -> float:
    """The share of a full batch one makes (brief 4c §6.1): 1 for a recipe that takes its inputs whole; for one that takes whatever
    one has up to its batch (`batch`), the least share of any input to hand, at most 1 (0 with none of an input)."""
    t = TECHNIQUES[tech]
    if not t.get("batch"):
        return 1.0
    share = 1.0
    for item, q in (t.get("inputs") or {}).items():
        alts = q if isinstance(q, dict) else {item: q}
        share = min(share, max(available(here, i, extra=extra) / max(1e-12, n * mult) for i, n in alts.items()))
    return max(0.0, min(1.0, share))


def shortfall(here, mind, tech, mult=1.0, at=None, extra=None, a=None) -> str:
    """'' if the technique can be done here now, else what is short."""
    t = TECHNIQUES[tech]
    sites = where(here, tech, graves=str((a or {}).get("method", "")).lower() == "cairn")
    if not sites:
        need = t.get("at", {})
        what = need.get("covers") or [FITTINGS[f]["label"] for f in need.get("fittings", [])] or ["building"]
        what = [x[2:] if x.startswith("a ") else x[3:] if x.startswith("an ") else x for x in what]   # "no hand mill", not "no a hand mill"
        return f"there is no {' or '.join(what)} here you can use"
    if at is not None and t.get("at"):
        if not any(s[1] == at for s in sites):
            return f"{label(tech)} is done at {', '.join(s[2] for s in sites)}, not there"
        sites = [s for s in sites if s[1] == at]
    if t.get("tools"):
        tool, m = here.best_tool(t["tools"])
        if m is None:
            from cybertron2.engine.data import TOOLS
            near = next((cid for cid in here.takeable() if cid != here.hands and any(here.contents(cid).get(x, 0) >= 1 for x in TOOLS)), None)
            return f"you need a tool in your hands for {label(tech)}" + (
                f"; there is one in {here.buildings()[near[len('stock:'):]]['name']}'s store: take it into your hands (move)" if near else "; you have none")
    for f_ in t.get("home_fittings") or []:                                   # kept at one's home (a dog for a watch)
        if not any((here.buildings()[b].get("fittings") or {}).get(f_) for b in here.homes_here() if b in here.buildings()):
            return f"you keep no {f_} at your home here"
    if t.get("gear_x") and not any(here.sound_held(g) > 0 for g in t["gear_x"]):   # a line to fish with (u2 §4.5)
        return "you have no line to fish with (a hand line, or a rod and line)"
    if t.get("animals") or t.get("uses"):
        from cybertron2.engine import farm as FM
        why = FM.team_shortfall(here, t)
        if why:
            return why
    for item, q in (t.get("inputs") or {}).items():
        alts = q if isinstance(q, dict) else {item: q}
        if t.get("batch") and not any(available(here, i, extra=extra) > 1e-6 for i in alts):    # any amount, up to the batch (4c §6.1)
            i, n = next(iter(alts.items()))
            from cybertron2.engine.verbs import _short_note
            return f"it takes up to {round(n * mult, 2):g} {i}, and you have none to hand" + _short_note(here, i)
        if t.get("batch"):
            continue
        if not any(available(here, i, extra=extra) + 1e-9 >= round(n * mult, 2) for i, n in alts.items()):
            i, n = next(iter(alts.items()))
            more = "".join(f" or {round(n2 * mult, 2):g} {i2}" for i2, n2 in list(alts.items())[1:])
            from cybertron2.engine.verbs import _short_note                    # who took it today; where it comes from (D4-95)
            return f"it needs {round(n * mult, 2):g} {i}{more}; you have " + " and ".join(
                f"{available(here, i2, extra=extra):.1f} {i2}" if len(alts) > 1 else f"{available(here, i2, extra=extra):.1f}" for i2 in alts) \
                + " to hand" + _short_note(here, i)
    if sites[0][0] != "anywhere":
        why = [ready(here, tech, k, key, a) for k, key, _ in sites]
        if all(why):
            return why[0]
    return ""


def card(here, mind, tech) -> str:
    """What one is told about a technique, by one's level of it."""
    t = TECHNIQUES[tech]
    lvl = level(mind, tech)
    if lvl is None:
        return f"{t['label']}: you know nothing of it"
    r = rec(mind, tech)
    src = f" ({r['source']})" if r and r.get("source") else ""
    places = ", ".join(sorted({x[2] for x in where(here, tech)})) or "nowhere here"
    if lvl == "aware":
        return f"{t['label']}: you know of it{src}, but not how it is done"
    ins = inputs_words(t.get("inputs"), t.get("batch")) or "no materials"
    if lvl == "rough":
        return f"{t['label']}: you have a rough idea{src}: {ins}, done at {places}. You could try (about half the time it works, and it takes more)"
    gives = t["gives"] if isinstance(t["gives"], str) else ", ".join(f"{q:g} {i}" for i, q in t["gives"].items())
    line = f"{t['label']} (`{t['verb']} {tech}`): {ins}, at {places}; {t['units']} units" + (f"; gives {gives}" if gives else "")
    if lvl == "capable":
        line += f". At your level you use about {TRY['capable']['inputs']:g} times the materials and it works about 3 times in 4"
    return line


def _place_words(t) -> str:
    """Where a craft is done, from the data (u3 §4.1): 'at a smoke racks', 'at a house', 'on water or fen', 'anywhere'."""
    at = t.get("at") or {}
    if at.get("fittings"):
        labs = [FITTINGS.get(f, {}).get("label", f).split(" (")[0].removeprefix("a ").removeprefix("an ").removeprefix("the ")
                for f in at["fittings"]]
        return "at " + " or ".join(("an " if x[:1] in "aeiou" else "a ") + x for x in labs)
    if at.get("building"):
        return "at a house"
    if at.get("covers"):
        return "on " + " or ".join(at["covers"])
    if at.get("things"):
        return "at " + " or ".join(at["things"])
    return "anywhere"


def _ins_words(ins, mult=1.0) -> str:
    return " and ".join(" or ".join(f"{round(float(n) * mult, 3):g} {i}" for i, n in q.items()) if isinstance(q, dict)
                        else f"{round(float(q) * mult, 3):g} {item}" for item, q in (ins or {}).items())


def _gives_words(t) -> str:
    g = t.get("gives")
    if not g:
        return ""
    return g if isinstance(g, str) else " and ".join(f"{q:g} {i}" for i, q in g.items())


def craft_line(tech, lvl, rec=None, w=None) -> str:
    """A craft as one at `lvl` is shown it (D2-263; u3 §4): at known and capable its inputs with their batch, what it gives, its units
    and where; at known also its life and its season (D2-251); at capable the odds and the extra materials; at rough its inputs as
    the card has them; aware, its name and where one heard of it. Numbers come from the data at the world's factor (`w`)."""
    from cybertron2.engine import clocks as CK, gear as GE
    t = TECHNIQUES[tech]
    lab = label(tech)
    rec = rec or {}
    if lvl == "aware":
        return f"{lab} ({rec.get('source') or 'you know of it'})"
    ins = t.get("inputs") or {}
    place = _place_words(t)
    gives = _gives_words(t)
    hours = bool(t.get("hours"))
    units = CK.act_units(t, w) if hours else int(t.get("units", 1) or 0)
    season = ""
    if t.get("by_season"):
        best = max(t["by_season"].items(), key=lambda kv: (kv[1], kv[0]))[0]
        season = f"best in {best}"
    if lvl == "rough":
        body = _ins_words(ins) or "no materials"
        return f"{lab} (a rough idea: {body}" + (f", {place}" if place != "anywhere" or ins else "") + ")"
    if hours and isinstance(t.get("gives"), dict) and len(t["gives"]) == 1:
        item = next(iter(t["gives"]))
        b = CK.batch_of(t, w)
        thing = GE.plural(item) if b != 1 else item
        body = (f"up to {b} {thing} a unit, each from {_ins_words(ins)}" if b > 1 else
                f"{_ins_words(ins) or 'no materials'}, {units} unit{'s' if units != 1 else ''}; gives a {item}") if ins else \
            f"{units} unit{'s' if units != 1 else ''}; gives {gives}"
        life = GE.life_words(item, w) if lvl == "known" else ""
    elif t.get("batch") and ins:
        body = f"up to {_ins_words(ins)}, {units} unit{'s' if units != 1 else ''}" + (f"; gives as much {gives.split(' ', 1)[-1]}" if gives else "")
        life = ""
    elif ins:
        body = f"{_ins_words(ins)}, {units} unit{'s' if units != 1 else ''}" + (f"; gives {gives}" if gives else "")
        life = ""
    else:
        body = f"{units} unit{'s' if units != 1 else ''}" if units else ""
        life = ""
    bits = [x for x in (body, place if place != "anywhere" or ins else "", life, season if lvl == "known" else "") if x]
    head = "known" if lvl == "known" else "capable"
    if lvl == "known" and rec.get("skill") is not None:
        head += f", {skill_word(float(rec['skill']), tech)}"
    if lvl == "capable":
        bits.append(f"works about {int(round(TRY['capable']['chance'] * 4))} times in 4, with about "
                    f"{'a third' if abs(TRY['capable']['inputs'] - 1.3) < 0.05 else str(round((TRY['capable']['inputs'] - 1) * 100)) + '%'} more materials")
    return f"{lab} ({head}" + (": " + "; ".join(bits) if bits else "") + ")"


def crafts_lines(mind, here=None) -> list:
    """The crafts one knows, each as one's level shows it (D2-263; u3 §4). `here` gives the world's capital factor for the units."""
    k = mind.know
    w = here
    known = [craft_line(t, "known", r, w) for t, r in sorted(k.items()) if r["level"] == "known" and not basic(t)]
    practised = [f"{label(t)} ({skill_word(r['skill'], t)})" for t, r in sorted(k.items()) if basic(t) and r.get("skill", 1.0) >= 1.1]
    capable = [craft_line(t, "capable", r, w) for t, r in sorted(k.items()) if r["level"] == "capable"]
    rough = [craft_line(t, "rough", r, w) for t, r in sorted(k.items()) if r["level"] == "rough"]
    aware = [f"{TECHNIQUES[t]['label']} ({r['source']})" for t, r in sorted(k.items()) if r["level"] == "aware"]
    basics = ", ".join(label(t) for t in TECHNIQUES if basic(t) and not TECHNIQUES[t].get("modifies"))
    makes = [craft_line(t, "known", None, w) for t in TECHNIQUES if basic(t) and TECHNIQUES[t]["verb"] == "make"
             and (TECHNIQUES[t].get("inputs") or TECHNIQUES[t].get("hours")) and not TECHNIQUES[t].get("modifies")]
    out = [f"- Everyone knows: {basics}."]
    if makes:
        out.append("- Everyone's makings: " + "; ".join(makes) + ".")
    if practised:
        out.append("- Long practice has made you better than most at: " + "; ".join(practised) + ".")
    if known:
        out.append("- You know: " + "; ".join(known) + ".")
    if capable:
        out.append("- You are capable of (not yet sure of hand): " + "; ".join(capable) + ".")
    if rough:
        out.append("- You have a rough idea of: " + "; ".join(rough) + ". You could try these, at a cost in materials and a risk of failing.")
    if aware:
        out.append("- You know of, but not how: " + "; ".join(aware) + ".")
    return out


def doable(here, mind) -> list:
    """The scripted bots' candidates: "verb technique" for each technique one could do here now (smoke tests only). Never shown to a
    person: the list of what one could do today is gone from every prompt (D2-286)."""
    out = []
    for tech, t in TECHNIQUES.items():
        if t.get("modifies"):
            continue
        lvl = level(mind, tech)
        from cybertron2.engine import packs as PK
        if t.get("crew") and lvl not in ("rough", "capable", "known") and PK.on(t, getattr(mind, "packs", None)):
            lvl = "known"                                                     # anyone can work on a crew (D2-66), of this world's packs
        if lvl not in ("rough", "capable", "known") or t["verb"] == "build" or (t.get("yield") or {}).get("kind") == "clear_built":
            continue
        if not shortfall(here, mind, tech, TRY[lvl]["inputs"]):
            out.append(f"{t['verb']} {tech}")
    return out[:10]


def mentions(text) -> list:
    """Techniques named in a text (speech makes one aware of them: knowledge.md)."""
    low = f" {str(text).lower()} "
    out = []
    for tech, t in TECHNIQUES.items():
        if t["verb"] == "build":
            continue
        words = [tech] + t.get("aliases", [])
        if any(f" {x} " in low or f" {x}," in low or f" {x}." in low for x in words):
            out.append(tech)
    return out


# ---------------------------------------------------------------------- rising (through the learn primitive)
def tried(here, mind, tech, ok, units=1) -> str:
    """Practice: two successes a level (a failure counts half) from rough to capable to known; skill grows with the units of work
    spent at it, on all work (D2-52)."""
    r = rec(mind, tech)
    if r is None and basic(tech):
        mind.know[tech] = r = {"level": "known", "skill": curve(tech)[0], "seen": 0, "wins": 0, "fails": 0, "source": "", "since": here.day}
    if r is None:
        return ""
    r["wins" if ok else "fails"] = r.get("wins" if ok else "fails", 0) + 1
    lb = here.p.get("labour") or {}
    sk0 = float(r.get("skill", curve(tech)[0]))
    if float(lb.get("fade_rate", 0) or 0):
        r["practised"] = here.day                                              # for skill's fading (D4-103 phase 2)
        if r.get("peak") is not None and sk0 < float(r["peak"]) - 1e-9:         # coming back to a skill once held (D4-105)
            units = float(units) * float(lb.get("relearn", 1.0))
    r["skill"] = skill_of_practice(tech, practice_of_skill(tech, sk0) + float(units) * practice_x(here, tech))
    if r.get("peak") is not None and r["skill"] > float(r["peak"]):
        r["peak"] = r["skill"]
    if r["level"] == "known":
        return ""
    score = r.get("wins", 0) + 0.5 * r.get("fails", 0)
    nxt = {"rough": "capable", "capable": "known"}.get(r["level"])
    if nxt and score >= 2:
        r["wins"] = r["fails"] = 0
        here.apply("learn", person=mind.name, tech=tech, level=nxt, source="from practice")
        return nxt
    return ""


def saw(here, mind, tech, actor, k=1) -> bool:
    """Seeing it done: three sightings (watching counts double) give a rough idea."""
    if basic(tech):
        return False
    r = rec(mind, tech)
    if r is None:
        here.apply("learn", person=mind.name, tech=tech, level="aware", source=f"you saw {actor} at it")
        r = rec(mind, tech)
    r["seen"] = r.get("seen", 0) + k
    if r["level"] == "aware" and r["seen"] >= 3:
        return bool(here.apply("learn", person=mind.name, tech=tech, level="rough", source=f"from watching {actor}"))
    return False
