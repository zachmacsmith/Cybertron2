---
id: docs/review/37_growth/02zzzm_patterns/brief.md
kind: note
updated: "2026-11-24"
---
# Brief: the engine's design patterns surveyed (thread W-110)

*note · `docs/review/37_growth/02zzzm_patterns/brief.md`*


Session 37.2, 24 Nov 2026. Four survey agents (A to D), each one area of the engine. None edits engine code, specs, tests or design
files; each writes `docs/review/37_growth/02zzzm_patterns/<letter>_<area>.md` (and small scripts beside it) and commits only its own
files with `git add <files>` and a plain `git commit` whose last paragraph is exactly:

```
Agent: 37.2
Thread: [[W-110 The engine's design patterns surveyed against the whole engine and…|W-110]]
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

(no other trailers; never `records.py commit`). Then `git pull --rebase` (with `--autostash` only if others' uncommitted files block
it) and `git push origin main`. No model calls, no live runs.

## The question (Zach, 24 Nov)

"Can you do a survey of both the new wave and the full engine to compare these set of patterns: is this actually enough patterns
to capture all of this? Now does seem like a relevant point for the restructuring now." Decided with it ([[D2-353 Everything new in the engine is built within the agreed architecture…|D2-353]]): everything new is
built within the agreed architecture (feature_packages.md P3: features are data on the core's general mechanisms; code only for a
new kind of thing, a new kind of change, a process with its own dynamics, or the context its signs read; everything else is rows),
behaviour attaches to declared properties and never to a thing's name, interface and signs are rendered from data, every registry
is checked when it loads.

## The hypothesis to test (try hard to break it)

A small set of patterns captures nearly every mechanic:
1. **Typed rows with declared properties, checked at load** (every good, craft, act, fitting, gear, beast, kind, ecosystem, run,
   cover, building part is a row of its category, with required fields).
2. **Behaviour attaches to properties, never names** (a good's "smelt when going off", a fitting's "rack", gear's "rots in water").
3. **General mechanisms reading those properties:** (a) **stocks**: anything counted, S, K, r on a declared clock, individuals drawn
   out and returned (fish, shallows, game, wood, grass, herds?); (b) **pulses**: a nightly chance from declared conditions (runs,
   spawning, floods, frost, vermin, illness?); (c) **processes**: a lot in a container becoming another good over nights under
   conditions (smoking, drying, salting, retting, curing, baking?); (d) **set gear**: a placed thing sampling a stock or a pulse each
   night, with hold, catch rule, decay, wear, theft (snares, traps, nets, lines, the weir); (e) **lives and wear** on a clock, with
   mending; (f) **acts**: shapes, arguments, costs and needs from the registry; (g) **signs**: rows bound to a state property and a
   sense, rendered from data; (h) **the book**: structured fields only.
4. **One name resolver** from rows' aliases, used by acts, rules and attending.
5. **Generated worlds carry the physical world entire**; makers only pin people and scale named levers.

Context: feature_packages.md (§1 principles, §2 the object model of six categories: space, layer, body, population, record, mind;
§2.1 the kind registry; §4 packages and manifests); the [[W-73 Fishing, hunting and their materials developed together|W-73]] wave's design set (docs/cybertron2/proposals/w73_design/); the findings
of this week: prompt_compare.md and iface_brief.md (the act table no longer rendered), docs/review/37_growth/02zzzl_waters_calib/
generality.md (the waters), build_gaps.md. The wave's baseline is commit f728a3b7 (the engine before it).

## Each agent, in its area

1. **Every mechanism** (a behaviour that reads or changes state: a rule of change, an act's effect, a night step, a sign, a
   renderer, a generator step): name it, cite file:line, and say which pattern(s) it is or should be, how well it fits today
   (general over rows; general with fitted constants; a special case by name; hand-written text; a word-list parse; a silent skip),
   and whether it came in the wave (`git log -S`, `git blame` against f728a3b7).
2. **Every branch on a named thing in function code** (a good, craft, fitting, gear, kind, cover or building part named in an `==`,
   an `in (...)`, a dict of names): what property of which row it should become, under which mechanism; or why it is legitimately
   by name (a core default). A count by file.
3. **What does not fit:** every mechanic none of the patterns captures, with what a further pattern would need to be (candidates to
   test: agreements and debts, claims and holding, households and offices, learning and fading, care and children, travel and
   roads, weather and the calendar, buildings with rooms and floors, fire and heat, eating and hunger, theft and witness,
   evenings and talk, notes and memory, the journal and replay). Say plainly whether the hypothesis's set is enough, too few, or
   wrongly cut.
4. **The restructuring:** for the area, what moving to the patterns costs (lines touched, risk) and what it would save, in the
   terms of feature_packages.md §9 and §10.

## The areas

- **A, the world's physics:** `engine/world.py`, `data.py` (the tables), `renewal.py`, `waters.py`, `wild.py`, `cybertron2/wild/`
  (all), `climate.py`, `environment.py`, `forests.py`, `capacity.py`, `cybertron2/landgen/` (all), `generate.py`.
- **B, making, taking and keeping:** `engine/verbs.py` (the handlers' effects), `gear.py`, `placed.py`, `process.py`, `stores.py`,
  `buildings.py`, `things.py`, `farm.py`, `herds.py`, `night.py`, `strips.py`, `fuse.py`, `yields.py` and any module they call.
- **C, people and society:** `life.py`, `learning.py`, `knowledge.py`, `memory.py`, `founders.py`, `livelihoods.py`, `book.py`,
  `agreements.py`, `exchange.py`, `settle.py`, `parties.py`, `roads.py`, `here.py`, `run.py` (the day's order), `evening.py`,
  `journal.py`, `bots_livelihood.py`.
- **D, senses and interface:** `signs.py`, `perceive.py`, `prompt.py`, `core.py`, `shapes.py`, `view.py`, `views.py`, `layout.py`,
  `wild/river.py`'s signs, the evening prompt; and how a person's knowledge selects what they see ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]], [[D2-350 Every act and every technique a person can take is registered with…|D2-350]] to [[D2-352 Familiarity and the interface|D2-352]]).

## Output

`<letter>_<area>.md`: a summary first (mechanisms counted by fit; the named branches counted; what does not fit; the verdict on the
hypothesis for the area); then the table of mechanisms; the table of branches with the property each becomes; the misfits with a
proposed pattern; the restructuring's cost for the area. Every claim from the code with file:line. Report back with the summary.

## Added 24 Nov (Zach: "what are all the different types of things, the different types of properties, and the different types of mechanisms or families of mechanisms or processes ... that could be generalised ... and how have things been built in over time? ... What processes can we follow to ensure this does happen?")

5. **A taxonomy for the area:** every type of thing (categories and kinds of row or record); every type of property rows carry or code
   reads off them, grouped (quantities; rates and clocks; conditions; capabilities; links to other rows; words); every family of
   mechanisms or processes that could be generalised (its members today, what they share, what a general version would read).
6. **History:** from git log on the area's files (dates, threads, sessions), whether each mechanism came as a new ad hoc system,
   was built into an existing general one, or generalised and extended one; dated examples of each; whether the trend is improving.
7. **What in the process let ad hoc systems in** (briefs, reviews, missing checks), with evidence.
