"""The interface from one registry (W-109; D2-350, D2-351, D2-352, D5-2 "interface is not world"). The feature unit of the
interface (D2-244): its check (`check`, run at load: an act, a technique or a way without its interface fields cannot be built),
who is shown what (`WHO`, the conditions an act's face names; `familiar`, a craft by the person's familiarity) and the renderer
(`lines`, the "What you can do" section of the core prompt), which reads only the registry:

- the acts: `verbs.VERB[v]["iface"]`, each face with its shape, the word said in "do", its arguments and options, what it does,
  what it needs, its cost and who is shown it; `verbs.EVERYONE`, the acts everyone knows (D2-351);
- the crafts: `data.TECHNIQUES`, each with its shape (from `verb` and `set`), its label, `does` where the label does not say what
  happens, `args` where the craft takes more than its shape's, and the recipe fields the level shows (D2-263);
- the ways: the modifier rows of `data.TECHNIQUES` (`key`, `value` or `values`, `takes`, `label`, `changes.units`).

What each person is shown (D2-351, D2-352): an act or craft once they are familiar with it at all, never otherwise. Aware: its name
and who does it, kept apart from what one can do. A rough idea: how it is said and what it must be told, what it needs and a rough
recipe. Known or capable, and everything everyone knows: the full line (every argument and option, the cost, the full recipe and
batch, what a tool does to it, the ways learnt). No list of what one could do today (D2-286); rules are written in "rules" (D2-339).
"""
from __future__ import annotations

import re

LEVEL_ORDER = {"known": 0, "capable": 1, "rough": 2, "aware": 3}


class RegistryError(ValueError):
    """An act, craft or way without the interface fields the renderer needs (D2-350: a build error)."""


# ---------------------------------------------------------------------- who is shown an act's face (the names a face's `who` lists)
def _stage(here) -> str:
    return (here.body(here.name) or {}).get("stage", "adult")


def _head(here) -> bool:
    hh = here.household()
    return bool(hh) and here.head(hh) == here.name


def _gap(here) -> bool:
    return any(not b.get("unfinished") and here.has_gap(b) for b in here.buildings().values())


def _sets(here) -> bool:
    """Whether one has gear to go back to: a set craft one can do, set gear standing, or a household's processing container here."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    mind = here.mind()
    if any(t.get("set") and KN.level(mind, k) in ("rough", "capable", "known") for k, t in TECHNIQUES.items()):
        return True
    if any(here.owns_set(c) for c in here.sets().values()):
        return True
    from cybertron2.engine import shapes as SH
    return SH._containers(here)


WHO = {
    "grown": lambda here: _stage(here) in ("adult", "elder"),
    "not youth": lambda here: _stage(here) not in ("youth", "child"),
    "head": _head,
    "household": lambda here: here.household() is not None,
    "children": lambda here: bool(here.children_on()),
    "roads": lambda here: bool(here.roads()),
    "herds": lambda here: __import__("cybertron2.engine.verbs", fromlist=["when_holds"]).when_holds(here, "herds"),
    "evening": lambda here: bool(here.setting("evening")),
    "tags": lambda here: bool(here.setting("tags")),
    "gap": _gap,
    "sets": _sets,
    "never": lambda here: False,
}


def allowed(here, who) -> bool:
    return all(WHO[w](here) for w in (who or []))


# ---------------------------------------------------------------------- the check at load
def _check_args(where, args) -> None:
    if not isinstance(args, list):
        raise RegistryError(f"{where}: args must be a list")
    for a in args:
        if not isinstance(a, dict) or not a.get("key") or "req" not in a or not isinstance(a.get("opts"), dict):
            raise RegistryError(f"{where}: an argument without its key, whether it is required, or its options: {a!r}")
        if not a.get("is") and not a["opts"]:
            raise RegistryError(f"{where}: argument {a['key']!r} says neither what it is nor its options")
        for w in a.get("who") or []:
            if w not in WHO:
                raise RegistryError(f"{where}: argument {a['key']!r} names an unknown condition {w!r}")


def check(verbs=None, techniques=None, shapes=None) -> None:
    """Every act, craft and way carries its interface fields (D2-350): raises RegistryError naming the first one that does not."""
    if verbs is None:
        from cybertron2.engine.verbs import VERB as verbs
    if techniques is None:
        from cybertron2.engine.data import TECHNIQUES as techniques
    if shapes is None:
        from cybertron2.engine.shapes import SHAPES as shapes
    for sh, row in shapes.items():
        if not row.get("args") or not row.get("line"):
            raise RegistryError(f"shape {sh!r}: no grammar line")
    for v, d in verbs.items():
        faces = d.get("iface")
        if not faces:
            raise RegistryError(f"act {v!r}: no interface (iface)")
        for f in faces:
            where = f"act {v!r}"
            if f.get("shape") not in shapes:
                raise RegistryError(f"{where}: no shape, or one that is not among the eleven: {f.get('shape')!r}")
            if f.get("via") == "techniques" or f.get("retired"):
                continue
            for k in ("word", "does"):
                if not isinstance(f.get(k), str) or not f[k].strip():
                    raise RegistryError(f"{where}: no {k!r}")
            for k in ("needs", "args", "who"):
                if k not in f:
                    raise RegistryError(f"{where}: no {k!r}")
            _check_args(where, f["args"])
            for w in f["who"]:
                if w not in WHO:
                    raise RegistryError(f"{where}: unknown condition {w!r} in who")
            if d["cost"] in ("craft", "units", "write") and not f.get("cost"):
                raise RegistryError(f"{where}: its cost is not a number, and the face says none")
    for t, d in techniques.items():
        where = f"technique {t!r}"
        if not str(d.get("label") or "").strip():
            raise RegistryError(f"{where}: no label")
        if "(" in d["label"]:                                     # its name only: needs, hints, world are fields (D2-356)
            raise RegistryError(f"{where}: a label with a bracket; put what it needs in 'requires', its hints in 'hint', "
                                "the world's words in 'world'")
        if d.get("modifies") or d.get("verb") == "modifier":
            for k in ("key", "value", "modifies"):
                if not d.get(k):
                    raise RegistryError(f"{where}: a way without {k!r}")
            if d["value"] == "*" and not d.get("shown_in") and not d.get("values") and not d.get("takes"):
                raise RegistryError(f"{where}: a way taking any value says neither its values nor what it takes (takes)")
            continue
        if d.get("verb") not in ("gather", "work", "make", "build"):
            raise RegistryError(f"{where}: no verb a shape lists")
        if "units" not in d and "hours" not in d:
            raise RegistryError(f"{where}: no cost (units)")
        if any(d.get(k) for k in ("set", "process", "crew", "note", "manual")) and not str(d.get("does") or "").strip():
            raise RegistryError(f"{where}: set, processed, crew or noted, but no 'does' saying what doing it does")
        _check_args(where, d.get("args") or [])
        for w in d.get("who") or []:
            if w not in WHO:
                raise RegistryError(f"{where}: unknown condition {w!r} in who")


# ---------------------------------------------------------------------- words
def _units(n) -> str:
    return "free" if n == 0 else f"{n:g} unit{'s' if n != 1 else ''}"


def _opt_words(opts) -> str:
    return " | ".join(f"{o} ({w})" if w else o for o, w in opts.items())


def args_words(here, args, required_only=False, do=None) -> str:
    """{"do": word, "key": what it is, "key"?: a | b (what b does)}: an act's or a craft's arguments as said (D2-350)."""
    bits = [f'"do": "{do}"'] if do else []
    for a in args:
        if required_only and not a["req"]:
            continue
        if a.get("who") and not allowed(here, a["who"]):
            continue
        val = _opt_words(a["opts"]) if a["opts"] else a["is"]
        if a["opts"] and a.get("is"):
            val = f"{a['is']}: {val}"
        bits.append(f'"{a["key"]}"{"" if a["req"] else "?"}: {val}')
    return "{" + ", ".join(bits) + "}" if bits else ""


def _way_value(d) -> str:
    if d["value"] != "*":
        return d["value"]
    if d.get("values"):
        return " | ".join(d["values"])
    return d["takes"]


def way_shown(mind, m) -> bool:
    """A way is shown to one who knows it (a rough idea or more; everyone's are known) or who may try it untaught."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    d = TECHNIQUES[m]
    return not d.get("shown_in") and (KN.level(mind, m) in ("rough", "capable", "known") or d.get("untaught") == "tryable")


def ways_words(here, mind, mods) -> list:
    """The ways one knows, grouped by their key: '"range"?: near (on the village's own land) | far (a long day, 3 units more)'."""
    from cybertron2.engine import knowledge as KN
    from cybertron2.engine.data import TECHNIQUES
    by = {}
    for m in mods:
        d = TECHNIQUES[m]
        lvl = KN.level(mind, m)
        if not way_shown(mind, m):
            continue
        u = int((d.get("changes") or {}).get("units", 0) or 0)
        extra = f", {u} unit{'s' if u != 1 else ''} more" if u else ""
        if lvl in (None, "aware", "rough") and d.get("untaught") == "tryable" and not KN.basic(m):
            extra += "; untaught, done worse until learnt"
        by.setdefault(d["key"], []).append(f"{_way_value(d)} ({d.get('does') or d['label']}{extra})")
    return [f'"{k}"?: ' + " | ".join(dict.fromkeys(v)) for k, v in by.items()]


def _tools_words(t) -> str:
    """What a tool or gear does to a craft (known and capable only, D2-352): 'bare hands x0.25, a copper tool x2'."""
    bits = []
    tools = t.get("tools") or {}
    if tools:
        bits.append("bare hands cannot" if "bare" not in tools else f"bare hands x{tools['bare']:g}")
        bits += [f"a {g} tool x{x:g}" for g, x in tools.items() if g != "bare"]
    for g, x in (t.get("gear") or {}).items():
        bits.append(f"with a {g} x{float(x):g}")
    for g, x in (t.get("gear_x") or {}).items():
        bits.append(f"with a {g} x{float(x):g}")
    return ", ".join(bits)


def _needs_words(t) -> str:
    """What a craft needs beyond its place and materials (from a rough idea up): its row's `requires` (D2-356: "a cow in milk"), a
    tool, others with you."""
    bits = [t["requires"]] if t.get("requires") else []
    if t.get("tools") and "bare" not in t["tools"]:
        bits.append("a tool")
    if t.get("crew"):
        bits.append("others with you")
    return ", ".join(dict.fromkeys(bits))


# ---------------------------------------------------------------------- the crafts by familiarity
def craft_name(tech) -> str:
    from cybertron2.engine import placed as PL
    from cybertron2.engine.data import TECHNIQUES
    return PL.NOUN[tech][1] if TECHNIQUES[tech].get("set") and tech in PL.NOUN else tech


def familiar(here, mind) -> dict:
    """{shape: [(tech, level, everyone's)]}: the crafts the person is familiar with (D2-351: aware or above, never otherwise), and the
    crafts everyone knows of their stage (`basic`), their household's livelihood crafts first, by level, then everyone's."""
    from cybertron2.engine import packs as PK, shapes as SH
    from cybertron2.engine.data import TECHNIQUES
    stage = (mind.person or {}).get("stage", "adult")
    first = tuple((mind.person or {}).get("crafts_first") or ())
    out = {}
    for t, d in TECHNIQUES.items():
        if not PK.on(d, getattr(mind, "packs", None)):
            continue
        sh = SH.shape_of(t)
        if sh is None:
            continue
        r = mind.know.get(t)
        lvl = r.get("level") if isinstance(r, dict) else None
        uni = SH._universal(t, stage)
        if lvl is None and not uni:
            continue
        if not allowed(here, d.get("who")):
            continue
        out.setdefault(sh, []).append((t, "known" if uni and not lvl else lvl, uni))
    for xs in out.values():
        xs.sort(key=lambda x: (x[2] and x[0] not in first, 0 if x[0] in first else 1, LEVEL_ORDER.get(x[1], 9), x[0]))
    return out


def craft_line(here, mind, tech, lvl, uni) -> str:
    """One craft on its own line, at the detail the person's familiarity gives (D2-352). Aware crafts are not lines: `known_of`."""
    from cybertron2.engine import knowledge as KN, shapes as SH
    from cybertron2.engine.data import TECHNIQUES
    t = TECHNIQUES[tech]
    name = craft_name(tech)
    does = KN.doing(tech, iface=True)
    args = t.get("args") or []
    if lvl == "rough":
        inner = KN.craft_parts(tech, "rough", mind.know.get(tech), here, iface=True)[1]
        need = _needs_words(t)
        a = args_words(here, args, required_only=True)
        return (f"- {name}{' ' + a if a else ''}: {does} ({inner}" + (f", needs {need}" if need else "")
                + "; you could try: about half the time it works, and it takes more)")
    rec = mind.know.get(tech) if isinstance(mind.know.get(tech), dict) else None
    if SH.SHAPES[SH.shape_of(tech)].get("recipe") == "blueprint":             # a build's recipe: its materials and work (D2-263)
        from cybertron2.engine import prompt as PR
        head = ("known" + (f", {KN.skill_word(float(rec['skill']), tech, here)}" if rec and rec.get("skill") is not None else "")
                if lvl == "known" else "capable") if rec else ""
        inner = PR.craft_note_words(tech)
        body = "; ".join(x for x in (head, inner, t.get("hint")) if x)
        return f"- {name}: {does}" + (f" ({body})" if body else "")
    inner = KN.craft_parts(tech, "capable" if lvl == "capable" else "known", rec, here, iface=True)[1]
    if uni and not rec:
        inner = inner.replace("known: ", "", 1).replace("known", "", 1).strip(" :") or ""
    extra = [x for x in (_needs_words(t), _tools_words(t), t.get("hint")) if x]          # its hints: know-how (D2-356)
    a = args_words(here, args)
    body = "; ".join(x for x in [inner] + extra if x)
    return f"- {name}{' ' + a if a else ''}: {does}" + (f" ({body})" if body else "")


def known_of(mind, techs) -> str:
    """Crafts and ways only known of (D2-352): their names and who does them, nothing more."""
    from cybertron2.engine.data import TECHNIQUES
    out = []
    for t in techs:
        r = mind.know.get(t) or {}
        src = r.get("source") if isinstance(r, dict) else None
        name = TECHNIQUES[t]["label"] if TECHNIQUES[t].get("modifies") else craft_name(t)
        out.append(f"{name} ({src})" if src else name)
    return "; ".join(out)


def ways_for(targets) -> list:
    """The ways (modifiers) whose `modifies` names one of the targets a face or a shape row declares ("travel", "give:place")."""
    from cybertron2.engine.data import MODIFIERS, TECHNIQUES
    return [m for m in sorted(MODIFIERS) if set(TECHNIQUES[m]["modifies"]) & set(targets)]


def _craft_ways(here, mind, full, stated) -> list:
    """The ways one knows for the crafts one does in full (known, capable or everyone's): one line for the shape, each way's key
    once with the crafts it is said on; a key stated under an earlier shape is named, not said again (`stated`: key -> shape)."""
    from cybertron2.engine.data import TECHNIQUES
    keys = {}
    for t in full:
        tag = f"{TECHNIQUES[t]['verb']}:{t}"
        for m in ways_for([tag]):
            if way_shown(mind, m):
                keys.setdefault(TECHNIQUES[m]["key"], {"mods": [], "crafts": []})
                if m not in keys[TECHNIQUES[m]["key"]]["mods"]:
                    keys[TECHNIQUES[m]["key"]]["mods"].append(m)
                if t not in keys[TECHNIQUES[m]["key"]]["crafts"]:
                    keys[TECHNIQUES[m]["key"]]["crafts"].append(t)
    bits = []
    for k, g in keys.items():
        w = ways_words(here, mind, sorted(g["mods"]))
        if not w:
            continue
        on = ", ".join(craft_name(t) for t in g["crafts"])
        if k in stated:
            bits.append(f'"{k}"?: as under {stated[k]} (with {on})')
        else:
            bits.append(f"{w[0]} (with {on})")
    return bits


# ---------------------------------------------------------------------- the acts
def act_cost(here, v, face) -> str:
    from cybertron2.engine import verbs as V
    if face.get("cost"):
        return face["cost"]
    n = V.verb_units(here.p, v)
    if n is None:
        raise RegistryError(f"act {v!r}: no cost to show")
    return _units(n)


def act_line(here, mind, v, face) -> str:
    """An act on its own line (D2-350), in full: how it is said with every argument and option, what it does, what it needs, its
    cost, and the ways it takes that one knows (D2-351: the acts everyone knows are shown in full)."""
    what = [{"key": "what", "is": None, "req": True, "opts": {face["what"]: ""}}] if face.get("what") else []   # a face said with
    say = args_words(here, what + face["args"], do=face["word"])                                               # its "what"
    bits = [face["does"]] + ([f"needs {face['needs']}"] if face.get("needs") else [])
    cost = act_cost(here, v, face)
    line = f"- {face.get('what') or face['word']} {say}: " + "; ".join(bits) + (f" ({cost})" if cost else "")
    w = ways_words(here, mind, ways_for(face.get("ways") or []))
    if w:
        line += "\n  ways: " + "; ".join(w)
    return line


def acts_of(here, shape) -> list:
    """The faces of the acts listed under a shape that the person is shown: [(verb, face)], in the registry's order."""
    from cybertron2.engine import verbs as V
    out = []
    for v, d in V.VERB.items():
        if v not in V.EVERYONE:
            continue
        for f in d["iface"]:
            if f.get("shape") != shape or f.get("via") or f.get("retired"):
                continue
            if allowed(here, f.get("who")):
                out.append((v, f))
    return out


# ---------------------------------------------------------------------- the section
def lines(here, mind, first=()) -> list:
    """The "What you can do" section (D2-350): each of the eleven shapes with its grammar line, then each act and each of the
    person's crafts on a line of its own at their familiarity's detail; crafts only known of apart, by name."""
    from cybertron2.engine import knowledge as KN, shapes as SH
    from cybertron2.engine.data import MODIFIERS, TECHNIQUES
    by = familiar(here, mind)
    stated = {}
    out = ['What you can do. Name the craft or the act in "do", and what it acts on ("?": you may leave it out):']
    for sh, row in SH.SHAPES.items():
        xs = by.get(sh) or []
        doable = [x for x in xs if x[1] != "aware"]
        aware = [x[0] for x in xs if x[1] == "aware"]
        acts = acts_of(here, sh)
        body = [act_line(here, mind, v, f) for v, f in acts]
        body += [craft_line(here, mind, t, lvl, uni) for t, lvl, uni in doable]
        full = [t for t, lvl, uni in doable if lvl in ("known", "capable")]
        ways = _craft_ways(here, mind, full, stated)
        if full and row.get("ways"):                                          # the shape's own ways (build: how fine)
            ways += ways_words(here, mind, ways_for(row["ways"]))
        for k in re.findall(r'^"([^"]+)"\?: ', "\n".join(ways), flags=re.M):
            stated.setdefault(k, sh)
        if ways:
            body.append("  ways: " + "; ".join(ways))
        verb = (row.get("techs") or (None,))[0]
        mods_aware = [m for m in MODIFIERS if KN.level(mind, m) == "aware" and verb
                      and any(x.split(":")[0] == verb for x in TECHNIQUES[m]["modifies"])]
        if aware or mods_aware:
            body.append("  known of, not how (watch someone at it, or be taught): " + known_of(mind, aware + sorted(mods_aware)))
        if not body:
            continue
        out.append(f"{sh} {row['args']}: {row['line']}.")
        out += body
    return out
