"""The eleven act shapes (u9_people.md §3; D2-314): go, gather, set, tend, make, work, build, move, change, agree, force. The feature
unit of the act shapes (D2-244): its data (`SHAPES`: each shape's arguments, its grammar line, its faces and the handlers under it),
its one act (`normalize`: a free `do` to one of the 40 registry handlers of verbs.py, which stay as code) and its lines (`lines`,
the "What you can do" section of the core prompt, prompt.CORE).

A world turns the shapes on with `prompt: core` (u9 §1; the old system prompt and its verb list stay as `prompt: old`, D2-331;
a world without the setting keeps the old one, so old worlds replay: D2-314 "old worlds keep the 38"). With the shapes on:

- **the agent names the craft or the act in "do", and what it acts on** (`{"do": "wicker traps", "at": "the Isel"}`); the engine
  knows its shape. A shape word is read with its face or craft in "what" (`{"do": "make", "what": "smoke fish"}`), and the old
  verbs are still read as they were, so old replies and scripts run;
- **a technique is resolved preferring one the person knows** (u9 §3.2), and a set technique named alone resolves by what stands
  (tend one's own there, else set from the hands, else refused: placed.named_alone, basis §6);
- **a word that is no craft and no act** is refused with the person's own nearest crafts ("You know no craft called 'fish'. Your
  ways of fishing: ...").
"""
from __future__ import annotations

from cybertron2.engine.here import Refused

# Each shape: its arguments, the grammar line, the registry handlers its faces map to (face word -> verb), and which technique verbs
# sit under it (u9 §3.1). The order is the prompt's.
SHAPES = {
    "go": {"args": '{"to": a place or a way, "when"?: morning | nightfall, "on trouble"?: go round | push on | turn back | wait}',
           "line": 'travel; "sleep" at a place; "come" to a meeting called here; a "fire" on the road',
           "faces": {"travel": "travel", "go": "travel", "sleep": "sleep", "sleep at": "sleep", "come": "come", "fire": "fire"}},
    "gather": {"args": '{"do", "at": a place here}', "line": "take from the land and water into your hands", "techs": ("gather",)},
    "set": {"args": '{"do": gear you carry, "at": a place, "qty"?}',
            "line": "lay gear from your hands where it catches by night; it stays, yours, until you take it up (1 unit; up to 6 traps "
                    "or 25 snares)", "faces": {"set": "set", "lay": "set"}},
    "tend": {"args": '{"thing"?: a tag, "at"?: a place, "up"?: true}',
             "line": 'go back to your gear: take what it caught and set again what was sprung; "up" brings it home. Unnamed, all of '
                     'yours of that kind at the place, 1 unit a place; or keep a smokehouse\'s fire for tonight',
             "faces": {"tend": "tend", "lift": "tend", "check": "tend", "empty": "tend", "walk": "tend", "collect": "tend"}},
    "make": {"args": '{"do", "qty"?}',
             "line": "goods into goods, from your hands, then stores here you may use; or a lot laid in a container that becomes the "
                     "next good over nights", "techs": ("make",)},
    "work": {"args": '{"do", "at"?: a thing or a place}', "line": "labour on what stays where it is", "techs": ("work",),
             "faces": {"write": "write", "erase": "erase"}},
    "build": {"args": '{"do", "at", "structure"?: wattle | timber | stone}', "line": "its materials at the start, the work over days",
              "techs": ("build",)},
    "move": {"args": '{"do": take | give | put | drive, "item", "qty", "from" | "to"}',
             "line": 'goods between your hands, stores, people and places, or left in the open ("hidden": buried | under brush); a done '
                     'lot taken down; beasts driven. Taking from a store not yours is theft',
             "faces": {"take": "take", "give": "give", "put": "move", "move": "move", "drive": "drive", "leave": "leave",
                       "hide": "hide", "bury": "bury", "put down": "put down"}},
    "change": {"args": '{"do", "thing"?, "to"?}',
               "line": 'what you control: a door or a weir\'s gap ("set", "thing", "to"); who may sleep or eat at a house you may let '
                       'people into (host, grant, revoke); a claim; a name, the heir; your household (leave, found), a partnership '
                       '(part), a debt (release); a standing rule (rule)',
               "faces": {"host": "host", "grant": "grant", "revoke": "revoke", "claim": "claim", "name": "name", "order": "order",
                         "leave": "leave_household", "leave household": "leave_household", "leave_household": "leave_household",
                         "found": "found", "part": "part", "release": "release", "rule": "rule", "withdraw": "withdraw",
                         "door": "set", "gap": "set"}},
    "agree": {"args": '{"do", "with"?}',
              "line": "what both must choose: an offer accepted, a lesson (teach or learn, the same day, 2 units each), partnering, "
                      "joining a household or admitting someone, trying for a child",
              "faces": {"accept": "accept", "teach": "teach", "learn": "learn", "partner": "partner", "join": "join", "admit": "admit",
                        "try": "try"}},
    "force": {"args": '{"do": attack | guard, "target"?, "aim"?: rob | hurt, "at"?, "when"?: day | night}',
              "line": 'settled tonight: attack (rob, hurt); guard a building, a field or a herd, by night (the default) or by day '
                      '("when": "day": you spend the units you give it watching there)',
              "faces": {"attack": "attack", "guard": "guard", "watch over": "guard", "keep watch": "guard"}},
}
FACE = {f: v for s in SHAPES.values() for f, v in (s.get("faces") or {}).items()}
# words that are kept as they were (the old verbs are still read: D2-314, old replies replay); "rest" is an empty plan
KEEP = ("rest", "watch", "meet", "give", "take", "travel", "sleep", "come", "fire", "accept", "withdraw", "release", "host", "grant",
        "revoke", "join", "admit", "leave_household", "found", "claim", "drive", "partner", "part", "try", "name", "order", "write", "erase",
        "attack", "guard", "teach", "learn", "rule", "move", "set", "tend")


def on(w_or_here) -> bool:
    """The shapes and the core prompt are on in a world with `prompt: core` (u9; D2-314, D2-331)."""
    spec = getattr(w_or_here, "spec", None)
    if spec is None:
        spec = getattr(getattr(w_or_here, "_w", None), "spec", None) or {}
    return str((spec or {}).get("prompt") or "old") == "core"


def _known_first(mind, cands) -> str | None:
    from cybertron2.engine import knowledge as KN
    order = {"known": 0, "capable": 1, "rough": 2, "aware": 3}
    best = sorted(cands, key=lambda t: (order.get(KN.level(mind, t), 9) if KN.level(mind, t) else 9, cands.index(t)))
    return best[0] if best else None


def resolve(mind, word, verb=None) -> str | None:
    """A technique from a word (u9 §3.2): by name, alias, label or its short label, preferring one the person knows, then one done by
    `verb` (a shape named with its craft)."""
    from cybertron2.engine import knowledge as KN, packs as PK
    from cybertron2.engine.data import TECHNIQUES
    x = str(word or "").strip().lower()
    if not x:
        return None
    live = PK.techniques()
    cands = [t for t in live if (verb is None or TECHNIQUES[t]["verb"] == verb)
             and (x == t or x in [y.lower() for y in TECHNIQUES[t].get("aliases", [])] or x == TECHNIQUES[t]["label"].lower()
                  or x == KN.label(t).lower())]
    if not cands and verb is None:
        return None
    return _known_first(mind, cands) if cands else None


def _nearest(mind, word) -> str:
    """The person's own crafts nearest a word that named none: those sharing a word with it, else their crafts (u9 §3.2)."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    mine = [t for t, r in sorted(mind.know.items()) if t in TECHNIQUES and isinstance(r, dict) and r.get("level") in ("rough", "capable", "known")
            and not TECHNIQUES[t].get("modifies")]
    ws = {y for y in str(word).lower().replace("ing", "").split() if len(y) > 2}
    near = [t for t in mine if ws & set((t + " " + KN.label(t) + " " + " ".join(TECHNIQUES[t].get("tags", []))).lower().split())]
    return ", ".join(KN.label(t) for t in (near or mine)[:8])


def normalize(here, mind, a) -> dict:
    """A free act (u9 §3.2) as a registry act: {"do": verb, ...}. Old verbs pass as they are; a shape word reads its face or craft
    from "what"; a craft named alone takes its handler's verb (a set technique named alone: by what stands, through the gather
    handler, placed.named_alone). Raises Refused for a word that is neither, naming the person's nearest crafts."""
    from cybertron2.engine import placed as PL
    from cybertron2.engine.data import TECHNIQUES
    a = dict(a or {})
    do = str(a.get("do") or "").strip().lower()
    if not do:
        raise Refused('name the craft or the act in "do"')
    what = str(a.get("what") or "").strip().lower()
    if do in SHAPES:                                                         # a shape named: its face, else its craft, in "what"
        if do == "set" and a.get("thing"):
            return {**a, "do": "set"}
        if do == "tend":
            return {**a, "do": "tend"}
        if do == "set":
            return {**a, "do": "set"}
        if what in FACE and FACE[what] in ("travel", "sleep", "come", "fire") and do != "go":
            pass
        if what and what in (SHAPES[do].get("faces") or {}):
            v = SHAPES[do]["faces"][what]
            rest = {k: x for k, x in a.items() if k != "what"}
            if v == "set" and what in ("door", "gap"):
                rest.setdefault("thing", what)
            return {**rest, "do": v}
        if do == "go":
            return {**a, "do": "sleep" if a.get("at") and not a.get("to") else "travel"}
        if do == "move":
            return {**a, "do": "move"}
        if do == "force":
            return {**a, "do": "guard" if not a.get("target") else "attack"}
        verbs = SHAPES[do].get("techs") or ()
        if what:
            t = resolve(mind, what, verbs[0]) if verbs else None
            if t is None and verbs and verbs[0] == "gather":
                t = PL.method_of(what)
            if t is None:
                raise Refused(f"you know no way to {do} called {a.get('what')!r}. Yours: {_nearest(mind, what) or 'none yet'}")
            return {**a, "do": TECHNIQUES[t]["verb"], "what": t}
        raise Refused(f'say what to {do} in "what" (a craft you know)')
    if do in FACE and do not in KEEP:                                        # a face word on its own: lift, check, lay, put ...
        v = FACE[do]
        out = {**a, "do": v}
        if v == "set" and do in ("door", "gap"):
            out.setdefault("thing", do)
        return out
    if do in KEEP:
        return a
    from cybertron2.engine import verbs as V
    if do in V.VERB:                                                         # the old registry verbs: as they were
        return a
    m = PL.method_of(do)                                                     # a set technique named alone: by what stands
    if m is not None:
        return {**a, "do": "gather", "what": m}
    t = resolve(mind, do)
    if t is None:
        raise Refused(f"you know no craft called {a.get('do')!r}. Your crafts: {_nearest(mind, do) or 'none yet'}")
    v = TECHNIQUES[t]["verb"]
    if v == "modifier":
        raise Refused(f"{a.get('do')!r} is a way of doing another craft: name the craft, with this as its way")
    return {**a, "do": v, "what": t}


def quiet(here, a) -> dict:
    """normalize, or the act as it was when it is refused (the refusal is said when it is done)."""
    try:
        return normalize(here, here.mind(), a)
    except Refused:
        return dict(a or {})


# ---------------------------------------------------------------------- the lines (u9 §2.3, §2.4)
def shape_of(tech) -> str | None:
    from cybertron2.engine.data import TECHNIQUES
    t = TECHNIQUES[tech]
    if t.get("modifies") or t["verb"] == "modifier":
        return None
    if t.get("set"):
        return "set"
    return {"gather": "gather", "make": "make", "work": "work", "build": "build"}.get(t["verb"])


LEVEL_ORDER = {"known": 0, "capable": 1, "rough": 2, "aware": 3}


def _universal(tech, stage) -> bool:
    """A craft every person of the time can do (u9 §2.3: `universal`, read from `basic` until the rows carry the field)."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    t = TECHNIQUES[tech]
    if not KN.basic(tech) or t.get("modifies"):
        return False
    u = t.get("universal")
    if isinstance(u, dict) and stage not in (u.get("stages") or []):
        return False
    return not (t["verb"] == "build" and stage == "youth")


def _holds_gear(here, tech) -> bool:
    from cybertron2.engine import gear as GE
    item = (getattr(GE, "SET_GEAR", {}) or {}).get(tech)
    return bool(item) and here.sound_held(item) > 0


def crafts_by_shape(here, mind, first=()) -> dict:
    """{shape: [(tech, level)]}: the person's crafts at aware or above, and the universal ones of their stage, in u9 §2.3's order:
    their household's livelihood crafts first (`first`), by level, then universal ones."""
    from cybertron2.engine import knowledge as KN, packs as PK
    from cybertron2.engine.data import TECHNIQUES
    stage = (mind.person or {}).get("stage", "adult")
    first = tuple(first or (mind.person or {}).get("crafts_first") or ())
    out = {}
    for t in TECHNIQUES:
        if not PK.on(TECHNIQUES[t], getattr(mind, "packs", None)):
            continue
        sh = shape_of(t)
        if sh is None:
            continue
        r = mind.know.get(t)
        lvl = r.get("level") if isinstance(r, dict) else None
        uni = _universal(t, stage)
        if lvl is None and not uni:
            continue
        if sh == "build" and stage == "youth" and not lvl:
            continue
        if sh == "set" and (lvl in (None, "aware") and not _holds_gear(here, t)):
            continue
        out.setdefault(sh, []).append((t, "known" if uni and not lvl else lvl, uni and not r))
    for sh, xs in out.items():
        xs.sort(key=lambda x: (x[2], 0 if x[0] in first else 1, LEVEL_ORDER.get(x[1], 9), x[0]))
    return out


def lines(here, mind, first=()) -> list:
    """The "What you can do" section (u9 §2.3): one entry per shape the person has something to do with, its grammar line and the
    crafts under it at their level (D2-263); the free shapes always."""
    from cybertron2.engine import knowledge as KN
    by = crafts_by_shape(here, mind, first)
    stage = (mind.person or {}).get("stage", "adult")
    head = here.head(here.household()) == here.name if here.household() else False
    out = ['What you can do. Name the craft or the act in "do", and what it acts on:']
    for sh, row in SHAPES.items():
        xs = by.get(sh) or []
        if sh in ("gather", "make", "work", "build") and not xs:
            continue
        if sh == "set" and not xs:
            continue
        if sh == "tend" and not (by.get("set") or _containers(here)):
            continue
        yours = []
        named = []
        for t, lvl, uni in xs:
            if uni:
                if not KN.where(here, t):                                      # a universal craft with nowhere to do it here
                    continue
                season = KN.craft_line(t, "known", None, here).split("best in ", 1)
                named.append(t + (f" (best in {season[1].split(';')[0].rstrip(')')})" if len(season) > 1 else ""))
            else:
                line_ = KN.craft_line(t, lvl, mind.know.get(t), here)
                lab = KN.label(t)
                from cybertron2.engine import placed as PL
                name = PL.NOUN[t][1] if sh == "set" and t in PL.NOUN else t
                yours.append(name + line_[len(lab):] if line_.startswith(lab) else line_)
        line = f"- {sh} {row['args']}: {row['line']}."
        if sh == "change" and head:
            line = line[:-1] + "; as head, the household's rules and chores, your heir (name), the children's work (order)."
        if sh == "force" and stage == "youth":
            line = f"- {sh} " + '{"do": "guard", "at"?, "when"?: day | night}' + ": guard a building, a field or a herd, by night or by day."
        if yours or named:
            line += " Yours: " + "; ".join(yours + named) + "."
        out.append(line)
    return out


def _containers(here) -> bool:
    """Whether one's household holds a processing container here (a smokehouse's racks): tend keeps its fire (B41)."""
    from cybertron2.engine.data import FITTINGS
    return any(any((FITTINGS.get(f) or {}).get("process") or f == "smoke racks" for f, n in (here.buildings()[b].get("fittings") or {}).items() if n)
               for b in here.homes_here())


def example(here, mind, first=()) -> str:
    """The reply's example act (u9 §1.3): the person's own first craft that is not universal and is done at a place they know, with
    that place; else their first universal craft; never a craft of another's living by construction."""
    from cybertron2.engine import knowledge as KN
    by = crafts_by_shape(here, mind, first)
    first = tuple(first or (mind.person or {}).get("crafts_first") or ())
    cands = [(sh, t, lvl) for sh in ("set", "gather", "make", "work") for t, lvl, uni in by.get(sh) or [] if not uni and lvl != "aware"
             and not KN.basic(t)]
    cands.sort(key=lambda x: (first.index(x[1]) if x[1] in first else len(first), LEVEL_ORDER.get(x[2], 9)))   # one's own living first
    for sh, t, lvl in cands:
        if t:
            sites = [s for s in KN.where(here, t) if s[0] in ("parcel", "building")]
            from cybertron2.engine import placed as PL
            name = PL.NOUN[t][1] if sh == "set" and t in PL.NOUN else t
            if sites:
                return '{"do": "%s", "at": "%s"}' % (name, sites[0][2])
            return '{"do": "%s"}' % name
    wood = next((s for s in KN.where(here, "firewood") if s[0] == "parcel"), None) if "firewood" in KN.TECHNIQUES else None
    return '{"do": "firewood", "at": "%s"}' % (wood[2] if wood else "a wood you know")
