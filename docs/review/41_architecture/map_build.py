"""The map (W-112 step 3, first pass): every mechanism of the four patterns surveys (W-110) given its home in the target
(target.md §3 and §5), from the pattern each survey assigned it, with per-row overrides where a survey left none.

Run from the repository root: python3 docs/review/41_architecture/map_build.py > docs/review/41_architecture/map_table.md
It is mechanical: the homes follow the surveys' own pattern labels through TOKEN below; a row's first label decides unless
OVERRIDE names it. Read the output as a first pass, to be checked row by row in the migration (step 4)."""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import map_extract as MX  # noqa: E402

HOMES = {   # home -> (layer, what it is)
    "core.chokepoint": ("core", "state, primitives, hooks, the journal of changes"),
    "core.registry": ("core", "the registry form: rows with declared properties, links, load check"),
    "core.space": ("core", "space kinds: nodes, parcels, roads, groupings of places"),
    "core.time": ("core", "calendar, clocks, keyed draws"),
    "core.phases": ("core", "the day's steps and phases, declared order"),
    "core.conditions": ("core", "one condition grammar over registered predicates (and conditions derived from layers)"),
    "core.resolver": ("core", "one resolver over referent kinds and rows' aliases"),
    "core.prompt": ("core", "the prompt's frame and slots, the reply schema from the act registry"),
    "core.journal": ("core", "journal, replay, run views, infrastructure"),
    "M.acts": ("mechanism", "act effects: yield kinds, costs, sites, readiness"),
    "M.stocks": ("mechanism", "populations and stocks: renewal, habitat, takes, draw out and return, couplings, classes"),
    "M.pulses": ("mechanism", "pulses and hazards: a chance on declared conditions"),
    "M.processes": ("mechanism", "processes and transitions: a thing of one kind becoming another under conditions"),
    "M.setgear": ("mechanism", "placed gear sampling a stock or a run each night"),
    "M.lives": ("mechanism", "lives and wear on a clock, with mending"),
    "M.works": ("mechanism", "works: a change built up in units over days, then an effect"),
    "M.parts": ("mechanism", "bodies with parts, and capacity derived from them"),
    "M.keeping": ("mechanism", "keeping by risk and remedy"),
    "M.draws": ("mechanism", "drawing a need from ordered sources"),
    "M.records": ("mechanism", "records with terms and a settle step (agreements, offers, claims, offices, the book)"),
    "M.matching": ("mechanism", "matched intentions"),
    "M.familiarity": ("mechanism", "familiarity with a curve: crafts, places, kinds, landmarks"),
    "M.signs": ("mechanism", "signs: subject rows, act bundles, the observer gate, known and seeded lines"),
    "M.mind": ("mechanism", "the mind's dated records and 'as you last saw it'"),
    "F.wild": ("feature", "the wild food web's own dynamics"),
    "F.network": ("feature", "movement on a network: the runs, ranging, storms (one copy each)"),
    "F.climate": ("feature", "the climate as a driven layer"),
    "F.generator": ("feature", "the generator and its catalogue; worlds carried entire"),
    "F.memory": ("feature", "the agent's own text: memory, notes, speech"),
    "F.cast": ("feature", "run settings: which model plays whom"),
    "F.herds": ("feature", "the herd's own dynamics: wandering, gadding, a parcel's value to it"),
    "F.bots": ("feature", "the scripted bots' policies"),
}
TOKEN = [   # (survey or '*', label regex, home); first match wins
    ("*", r"chokepoint", "core.chokepoint"), ("*", r"calendar", "core.time"), ("*", r"^space", "core.space"),
    ("*", r"resolver", "core.resolver"), ("*", r"^conditions", "core.conditions"), ("*", r"phases", "core.phases"),
    ("*", r"infrastructure", "core.journal"), ("*", r"view\b", "core.prompt"), ("*", r"cast", "F.cast"),
    ("*", r"agent's own text|memory", "F.memory"), ("*", r"generator", "F.generator"), ("*", r"coupled populations", "F.wild"),
    ("*", r"bodies drawn out", "M.stocks"), ("*", r"record", "M.records"), ("*", r"matching", "M.matching"),
    ("*", r"familiarity", "M.familiarity"), ("*", r"seeded lines", "M.signs"), ("*", r"^signs", "M.signs"),
    ("*", r"keeping", "M.keeping"), ("*", r"works", "M.works"), ("*", r"parts|capacity", "M.parts"), ("*", r"^draw", "M.draws"),
    ("*", r"classes", "M.stocks"), ("*", r"^rows$", "core.registry"),
    ("A", r"^F1$|^F2|^F3$|^F8$", "M.stocks"), ("A", r"^F4$", "M.setgear"), ("A", r"^F5$", "M.pulses"), ("A", r"^F6$", "core.conditions"),
    ("A", r"^F7$", "M.processes"), ("A", r"^F9$", "F.network"), ("A", r"^F10$", "F.climate"), ("A", r"^F11$|^F12$", "core.registry"),
    ("*", r"^3a", "M.stocks"), ("*", r"^3b", "M.pulses"), ("*", r"^3c", "M.processes"), ("*", r"^3d", "M.setgear"),
    ("*", r"^3e", "M.lives"), ("*", r"^3f", "M.acts"), ("*", r"^3g", "M.signs"), ("*", r"^3h", "M.records"),
    ("*", r"^\(a\)", "core.registry"), ("*", r"^\(b\)", "M.pulses"), ("*", r"^\(c\)", "M.processes"), ("*", r"^\(d\)", "M.setgear"),
    ("*", r"^\(e\)", "M.lives"), ("*", r"^\(f\)", "M.acts"), ("*", r"^\(g\)", "M.signs"), ("*", r"^\(h\)", "M.records"),
    ("D", r"^1$|^2$", "core.prompt"),          # D's lines "as rows" are the prompt's lines rendered from rows
    ("*", r"^1$|^2$", "core.registry"), ("*", r"^4$", "core.resolver"), ("*", r"^5$", "F.generator"),
]
OVERRIDE = {   # rows whose survey gave no usable label (D's misfits, '-'), read from the mechanism's name
    ("D", "the readings one has"): "M.signs", ("D", "places, kin, beasts"): "M.mind", ("D", "lasting memory"): "M.mind",
    ("D", "beliefs, dated"): "M.mind", ("D", "the old system prompt"): "core.prompt", ("D", "one's beasts as last"): "M.mind",
    ("D", "one's house, known"): "M.signs", ("D", "family lines"): "M.signs", ("D", "things one knows"): "M.mind",
    ("D", "talk, meeting, road"): "core.prompt", ("D", "a person as seen"): "M.signs", ("D", "the core lines"): "core.prompt",
    ("D", "the core system prompt"): "core.prompt", ("D", "the belief view"): "M.mind", ("D", "roads from here"): "core.prompt",
    ("D", "a morning meeting"): "M.matching", ("C", "children do the household"): "M.records",
    # rows the surveys sent to another area, or marked none, placed by hand (24 Nov)
    ("A", "Familiarity by kind"): "M.familiarity", ("A", "Methods known by the land"): "M.familiarity",
    ("A", "A parcel's water type"): "core.registry", ("A", "Households, buildings and herds by trade"): "F.generator",
    ("B", "Writing on buildings"): "M.acts", ("B", "Things' own conspicuousness"): "M.signs", ("B", "Starvation"): "M.draws",
    ("B", "Driving a herd"): "M.acts", ("B", "Wandering, gadding"): "F.herds", ("C", "the bots' candidates"): "F.bots",
    ("C", "livelihood bots"): "F.bots", ("C", "where one spends the evening"): "core.phases",
    ("C", "speech at the hearth, a name heard"): "core.resolver",
    ("A", "Fuel in heat"): "M.draws", ("A", "Take tables built from traits"): "M.stocks", ("C", "whether a site is ready"): "M.acts",
    ("D", "how a tier looks"): "M.signs", ("D", "a place's repute"): "M.signs", ("D", "a processing container"): "M.acts",
}
GRADE = [("silent", r"\bS\b|silent"), ("words", r"\bW\b|words"), ("text", r"\bT\b|\bH\b|text"), ("named", r"\bN\b|named|\bB\b"),
         ("fitted", r"\bGF\b|\bF\b|fitted"), ("general", r"\bG\b|\bR\b|rows")]


def home(r):
    for (s, k), h in OVERRIDE.items():
        if r["survey"] == s and r["mech"].lower().startswith(k.lower()):
            return h
    labels = [t.strip() for t in re.split(r"[,;/]| and |\+", r["pattern"]) if t.strip() and t.strip() != "-"]
    for lab in labels:
        lab_ = re.sub(r"^none \((.*)\)$", r"\1", lab)
        for s, rx, h in TOKEN:
            if s in ("*", r["survey"]) and re.search(rx, lab_):
                return h
    return "unplaced"


def grade(r):
    f = re.sub(r"\(.*?\)|`.*?`", "", r["fit"])          # the grade letters, not the notes in brackets
    return next((g for g, rx in GRADE if re.search(rx, f)), "unknown")


def main():
    R = [r for r in MX.rows() if r["mech"]]
    by = defaultdict(list)
    for r in R:
        by[home(r)].append(r)
    print("# The map, first pass: the surveys' mechanisms by their home in the target (generated by map_build.py)\n")
    print(f"{len(R)} mechanisms (A {sum(r['survey']=='A' for r in R)}, B {sum(r['survey']=='B' for r in R)}, "
          f"C {sum(r['survey']=='C' for r in R)}, D {sum(r['survey']=='D' for r in R)}). 'Needs work' counts those whose worst "
          "grade is named, text, words or silent.\n")
    print("| Home | Layer | Mechanisms | A | B | C | D | general | fitted | needs work |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    order = list(HOMES) + ["unplaced"]
    for h in order:
        rs = by.get(h, [])
        if not rs:
            continue
        g = Counter(grade(r) for r in rs)
        s = Counter(r["survey"] for r in rs)
        work = sum(g[x] for x in ("named", "text", "words", "silent"))
        print(f"| `{h}` | {HOMES.get(h, ('?',))[0]} | {len(rs)} | {s['A']} | {s['B']} | {s['C']} | {s['D']} | {g['general']} | "
              f"{g['fitted']} | {work} |")
    print()
    for h in order:
        rs = by.get(h, [])
        if not rs:
            continue
        print(f"## `{h}`: {HOMES.get(h, ('', 'not placed by the labels'))[1]} ({len(rs)})\n")
        print("| Survey | # | Mechanism | Where | Fit today |")
        print("|---|---|---|---|---|")
        for r in rs:
            m = r["mech"].replace("|", "\\|")
            print(f"| {r['survey']} | {r['id']} | {m[:110]} | {r['where'][:60]} | {grade(r)} |")
        print()


if __name__ == "__main__":
    main()
