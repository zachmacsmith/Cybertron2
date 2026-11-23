"""The prompt core (u9_people.md §1, §2; D2-301, D2-314, D2-319, D2-331): what is told to everyone (the engine's frame, what a run
needs to measure society rather than confusion, the facts of the body), the reply format with examples from each person's own crafts,
and the system prompt in u9 §2.1's order. The feature unit of the prompt core (D2-244): its data (`CORE`, `REPLY`, `GRAMMAR`, the
fixed lines), its builder (`system_prompt`) and the words the turn, the evening and memory take from it when it is on.

On in a world with `prompt: core`; `prompt: old` (and a world without the setting) keeps today's system prompt and its verb list
(D2-331: live run 1's comparison arm; D2-314: old worlds keep the 38). The options list is gone in both (D2-286).

No line of the core names a season, a food's worth, a fuel figure, that a store keeps food, that the land renews, that knowledge
dies unless taught, or an example act or good (u9 §1.2: those are lore, seeded or learnt). No intent line names a horizon
(steering.md §4): "what you mean to do, and why"; "Decide what to do." "Any units you do not use are wasted" stays until fatigue
(questions B40; scenario_design §3).
"""
from __future__ import annotations

CORE = [
    "Each day you plan in the morning and may talk with those here; then you work.",
    "Work is counted in units of about two hours, told each morning: fewer in winter, for the young and the old, and when you are "
    "hungry, hurt or worn out. Any units you do not use are wasted.",
    "Everyone eats each night, from what they carry, then from the stores they may use. Without enough you go hungry, then starving, "
    "and may die. Hard work, cold and nights out make you need more.",
    "A house needs a fire at its hearth each night to cook and keep warm, and far more fuel when it is cold.",
    "People are born, grow up, pair, have children, grow old and die. A child must be fed and cared for by someone, or it may die.",
    "Land, buildings, herds, stores and what someone made or set are held by claims that others know of. You can reach for anything, "
    "but others may see and remember. Taking what is another's is your choice, and theirs to answer.",
    "Your household shares its house and store. Its head keeps its standing rules, which may give you chores for units your plan "
    "leaves. Your own rules and fallback come before the household's; going against the household's is seen. What you set stays as "
    "you set it until you change it.",
    "You know only what you have learnt, by watching, trying and being taught; others know other things. A failed try shows you why, "
    "as far as you can see. What goes unpractised fades.",
    "Each morning you hear what concerned you and what stood out. Each day you look closely at one thing, free.",
    "You remember in your own words: a memory you rewrite every few days, lines you keep for good word for word, and notes. Nothing "
    "else of past days stays with you. What you cannot see, you know as you last saw it.",
    "Places lie apart, and only what is carried goes between them.",
    "An act names what it acts on. Unnamed, it touches only your own things; another's you must name.",
]
EVENING_CLAUSE = " In the evening you are with those under your roof: you talk freely and settle the night."
CHILDREN_OFF = "People are born, grow up, grow old and die."
VIEW_CLAUSE = " What you cannot see, you know as you last saw it."

# the rules block's grammar: book.GRAMMAR, the one statement of D2-339's kinds, fields and conditions
from cybertron2.engine.book import GRAMMAR  # noqa: E402

CLOSING = "Decide what to do. Reply with JSON only."               # u9 §1.4; steering F4 (was "Plan your day.")
OLD_CLOSING = "Plan your day. Reply with JSON only."
EVENING_WHY = "\"why\": what you make of the day and what you mean to do."      # steering F3 (the old line named tomorrow)
EVENING_STANDS = "What you set stands: a door stays as you left it, and you sleep at home unless you say otherwise."   # steering F8
MEMORY_APPEND = "what you want to remember of them"                 # steering §4 (was a content list steering toward ledgers)


def on(w) -> bool:
    """A world (or a Here, through its settings: D4-35) with `prompt: core`."""
    if hasattr(w, "setting"):
        return str(w.setting("prompt") or "old") == "core"
    return str(((getattr(w, "spec", None) or {}).get("prompt")) or "old") == "core"


def closing(w) -> str:
    return CLOSING if on(w) else OLD_CLOSING


def core_lines(spec) -> list:
    """The twelve lines with their world variants (u9 §1.2): no evening, no children, no households, a view other than beliefs."""
    spec = spec or {}
    lines = list(CORE)
    if spec.get("evening"):
        lines[0] += EVENING_CLAUSE
    if not ((spec.get("children") or {}).get("on") if isinstance(spec.get("children"), dict) else spec.get("children")):
        lines[4] = CHILDREN_OFF
    if (spec.get("view") or "") != "beliefs":
        lines[9] = lines[9].replace(VIEW_CLAUSE, "")
    if spec.get("households") is False:
        lines[6] = None
    return [x for x in lines if x]


def core_text(spec) -> str:
    return "How life goes:\n" + "\n".join(f"{i + 1}. {x}" for i, x in enumerate(core_lines(spec)))


def reply_text(here, mind, first=()) -> str:
    """The reply format (u9 §1.3), its example the person's own first craft at a place they know, and their own tag when they have
    set gear standing; offers in placeholders (steering F6)."""
    from cybertron2.engine import shapes as SH
    ex = SH.example(here, mind, first)
    mine = [c for _, c in sorted(here.sets().items()) if c.get("tag") and here.owns_set(c)]
    tend = f', or {{"do": "tend", "thing": "{mine[0]["tag"]}"}}' if mine else ""
    over = int((here.p.get("labour") or {}).get("over_units", 0) or 0)
    lines = ["Reply with JSON:",
             '- "why": what you mean to do, and why.',
             '- "actions": the day\'s acts in order, each {"do": a craft you know or an act, and what it acts on}, as ' + ex + tend
             + '. What goes past your units is not done. "for": a person or your household, on their behalf.',
             '- "fallback": acts for units your plan leaves, in the order to try them, every day until you change it; [] clears it. '
             'Send it only to change it.']
    if over:
        lines.append(f'- "overwork": 0 to {over}: units to push on past your day\'s.')
    lines += ['- "tell": [{"to", "text"}] to one person here, before work; only they hear it. "say": [{"to": "everyone" or a building, '
              '"text"}] aloud, a unit each.',
              '- "explain": [{"to", "what": a craft}] what you know of a craft (free).',
              '- "offers": [{"to": a person or "anyone", "give", "get"}], as "<n> <good>", "<n> <good> by day <d>" or "work <n> days"; '
              'done when accepted, both ways or not at all.',
              '- "attend": what or whom you look at closely (free).',
              '- "rules": [standing rules, as above] to set, change or drop (free).',
              '- "note": [{"title", "text"}], "pin", "open", "forget": your notes (up to 8).',
              '- "memory", "keep", "drop": only when asked for.']
    return "\n".join(lines)


def livelihood_line(person) -> str:
    """The person's livelihood line (u9 §2.2), written by the world's fill (livelihoods.py) into the person's record."""
    return str((person or {}).get("livelihood") or "").strip()


def system_prompt(here, mind) -> str:
    """The core system prompt (u9 §2.1): who you are and your living; the place; your people; how life goes; the rules; what you can
    do (the shapes, crafts under them); other places as you know them; the reply."""
    from cybertron2.engine import prompt as PR, shapes as SH
    a = mind.person
    stage = {"youth": "a youth, not yet grown", "adult": "a grown adult", "elder": "an elder"}.get(a["stage"], a["stage"])
    home = next((nid for nid, x in mind.places().items() if x["days"] == 0), here.node)
    hn = mind.places()[home]["name"]
    head = " You are its head." if mind.head == mind.name else (f" Its head is {mind.head}." if mind.head else "")
    liv = livelihood_line(a)
    lines = [f"You are {mind.name}, {stage}, of {mind.household_name or 'no household'} in {hn}.{head}" + (f" {liv}" if liv else "")]
    lines.append(f"{hn}: {str(mind.places()[home]['text']).split('; its people know')[0].rstrip('.')}.")   # without the list (u9 §2.1)
    lines += ["", "Your people:"] + PR._kin_lines(mind)
    lines += ["", core_text({k: here.setting(k) for k in ("evening", "children", "view", "households")})]
    rb = [x for x in here.rules_block()]
    from cybertron2.engine import book as BK
    rb = [GRAMMAR if x == BK.GRAMMAR else x for x in rb]
    lines += [""] + rb
    first = tuple(a.get("crafts_first") or ())
    lines += [""] + SH.lines(here, mind, first)
    if len(mind.places()) > 1:
        lines += ["", "Other places, as you know them:"] + PR._map_lines(mind)
    lines += ["", reply_text(here, mind, first)]
    return "\n".join(lines)


def rest_line(mind) -> str:
    """The morning's line on units left yesterday (u9 §1.5; D2-301): "You rested n units yesterday." only when n > 0, and no push for
    a fallback."""
    days = mind.store.get("days") or []
    if not days:
        return ""
    for x in days[-1].get("did") or []:
        if str(x).startswith("You rested "):
            n = str(x).removeprefix("You rested ").split(" ")[0]
            return f"You rested {n} unit{'s' if n != '1' else ''} yesterday."
    return ""
