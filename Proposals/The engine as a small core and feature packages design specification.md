---
id: docs/cybertron2/proposals/feature_packages.md
kind: proposal
updated: "2026-11-16"
---
# The engine as a small core and feature packages: design specification

*proposal · ready for a decision (16 Nov). Nothing decided, nothing built. · `docs/cybertron2/proposals/feature_packages.md`*

> the engine as a small core and one folder per feature, each registering its data, kinds, primitives, phases, verbs, signs and prompt lines in a manifest; the object model (six categories); `requires` on every registration; the work estimated


**Status:** ready for a decision (16 Nov 2026). Nothing decided, nothing built. This is written as a specification so that it can be
decided part by part. Once a part is decided, its rules move to `spec/core/` (architecture.md and new files) with decision numbers.
Until then they are proposals, not spec.

**Owner:** lead session (C1 wrap-up), for 37.4 (the code under `cybertron2/` is 37.4's) and Zach.

## Summary

Today a feature is spread across the engine. The clearest case is the wild layer: it has its own folder (`cybertron2/wild/`, on
the `ecology` branches) and still edits 19 existing engine files, including 400 lines of `signs.py`.

This specification turns the engine into four things:
- **A small core,** which holds only what every world has.
- **Packages:** one folder per feature, each declaring in one manifest everything it adds.
- **One rule for combinations:** everything registered carries `requires` and `unless`, so a row or a step that belongs to two
  packages exists only when both are on, whichever folder holds it.
- **An object model of six categories** (space, layers, bodies, populations, records, minds), each with a base shape that every
  kind in it shares.

**The work is large:**
- **Size:** about 14,000 lines moved, 7,000 to 9,000 rewritten and 3,000 new, from an engine of 20,400.
- **Time:** about 26 to 39 builder-days for the whole migration (§10), against the 12 active days it took to build the engine.
- **The cheaper path:** phases 0 to 3 (about 13 to 21 days) give most of the benefit; the rest moves when it is next touched.

The inventory behind it is in [docs/review/40_feature_packages/](../../review/40_feature_packages/) (five files, A to E).

## The proposal

### 1. Principles

- **P1. The core never imports a package.** Packages import the core and the packages they declare. A test enforces this.
- **P2. Every change of state is a primitive applied through the chokepoint** ([[D4-34 Rebuild the M1 engine on the designed general core|D4-34]], kept). The only exception is a driven layer
  (§2.2), which is computed and never written.
- **P3. Features are data on the core's primitives.** A package adds code only for:
  - a new kind of thing;
  - a new kind of change (a yield kind);
  - a process with its own dynamics;
  - the context its signs read.
  Everything else is rows.
- **P4. Everything a package registers is declared in its manifest.** That covers rows, kinds, primitives, hooks, phases, verbs,
  signs, prompt lines, terms and tests. The core assembles the world from the manifests of the packages that are on.
- **P5. A registration exists only when its `requires` are all on and none of its `unless` is.** The package that defines it is
  always required.
- **P6. Nothing depends on position.** Rows, phases and prompt lines have stable names; order is declared, never implied by where
  something sits in a list.
- **P7. A package off is a clean null arm.** The world without a package differs from the world with it only by what that package
  registers. Draws are keyed by stable names, so other things are not perturbed.
- **P8. Code beside data is visible.** A manifest page shows each package's lines of code against its rows of data.

### 2. The object model

Everything in a world belongs to one of six categories. A **kind** is registered within a category, by the core or a package, and
inherits the category's base shape.

| Category | What it is | Base shape every kind has | Kinds today (and from packages) |
|---|---|---|---|
| **Space** | where things are | id, name, size, neighbours, position (height, coordinates), cover | node, parcel, road with stretches; the wild layer's areas (§2.6) |
| **Layer** | a value at every place of a space, changing over time | name, space it is defined on, values per cell, clock, rule of change, *driven* or *coupled*, how it is sensed | weather, snow lying, stocks, soil fertility, crop growth on a holding |
| **Body** | a located physical thing | id, kind, place, exists (alive, built, ended), condition, contents or make-up, name or tag, claimable, sense subject, mobility | person, container (hands, store, pile, remains, carcass), building, storm; from packages herd group, wild group, legend beast |
| **Population** | counts, not individuals | kind (a species row), where (parcel or area), counts by class, capacity, condition, rule of change, how one individual is drawn out and put back | plant and game stocks, herds, wild kinds by area |
| **Record** | a social fact with no body | id, kind, parties, where and when made, since and until, status, terms | claim, group (household), offer, agreement; later law |
| **Mind** | private to one person | owner, subject, day last seen, source (saw, heard, seeded) | knowledge and skill, beliefs, memory, places and kin known |

Outside the world proper:
- **Happenings:** events and acts. Short-lived, at a place, with an actor, sense and salience; the input to the senses.
- **Types:** data rows that instances point to (species, items, techniques, covers, crops, fittings, ecosystems).

#### 2.1 The kind registry

A kind declares the fields below. The registry replaces three hard-coded chains (`place_of`, `p_set`'s table map, the claim refs)
and the single closed `schema.FIELDS`.

| Field | Meaning |
|---|---|
| `name`, `category`, `table` | the kind and where its records live in `World.s` |
| `place` | how its place is found: a node and parcel, a road and stretch, an area, or "origin" for records |
| `fields` | its schema fragment: name, type, unit, clock; joined into the world schema with a version ([[D4-100 The world record's shape is declared and versioned|D4-100]]) |
| `claimable`, `container`, `subject` | whether it can be held; whether it holds goods; whether signs can be about it (and under what subject key) |
| `named` | how agents refer to it: name, tag ([[D4-68 Short tags, and names given|D4-68]]), household name |
| `rule` | for layers and populations: its rule of change and what steps it |
| `requires` | as for every registration |

Packages may add fields to core kinds (`person.stage` from life, `parcel.crop` from farming). Those fields are part of that
package's schema fragment and exist only when it is on.

#### 2.2 Layers: driven or coupled

- **A driven layer** is a pure function of the seed, the spec and the day. It is computed, never written, so every arm of an
  experiment meets it the same ([[D4-4 External change is separate from internal consequences|D4-4]]).
- **A coupled layer** is state, written by primitives.

The weather is driven today. `climate.py` computes it from day 0 and keeps it in a cache on the world object, outside `World.s`. It
has three scales:
- **for the region:** era, the year's anomaly, the weather type;
- **at each node:** fields of temperature, low, rain and wind, alike between near nodes and carried from day to day;
- **storms:** bodies with a birth day, start, velocity, radius and wind.

Stocks, snow, soil and crop growth are coupled.

**Rule:** a layer declares which it is. A driven layer cannot be changed by any act or by a fork's intervention; making the weather
answer to the world (fires, cleared forest), or letting a fork set a storm, means making it coupled (open question 7).

#### 2.3 Populations, and drawing individuals out

The engine has three incompatible forms of population today:
- parcel stocks `{S, K, r}`;
- herd role counts;
- the wild layer's density arrays by area.

**Proposed:** one base shape for all three, and **one rule for individuals.** Where people meet a population, the package draws
concrete individuals from it as bodies: a hunted beast, a wild group near a field, a legend. While they exist they leave the count,
and what remains of them returns to it. A kind registers its draw and return functions. A test checks that counts are kept across a
draw and a return.

#### 2.4 Wildlife

Wildlife is a population by area (the food web's step), groups near people, and legends: §2.3's rule applied. It is in the `wild`
package. Kept herds are the `animals` package's population kind, and the two share species rows (02zv C1's traits). Individual beasts
with their own record (a trained ox, a dog; 02zv C8) are a body kind for later.

#### 2.5 Ecosystems

An ecosystem is a **type**: a row saying which stocks and foods a piece of land has, at what rates, and which kinds find habitat
there. The generator writes it on the parcel (`parcels.ecosystem`, on the ecology branch). It has no state of its own: its state is
the state of its layers and populations. Succession (forest to scrub and back) is a slow coupled layer.

#### 2.6 Two grids

The engine's places are nodes and parcels. The wild layer runs on the generator's areas, with a bridge between the two. [[D2-208 The world keeps the land it runs on|D2-208]] now
keeps the generator's 150 m cells with every world. There are two choices (open question 6):
- **(a)** the cells become the base space, and parcels and areas are groupings of cells;
- **(b)** each layer keeps its own grid and declares how it maps to the others.

This specification does not depend on the choice. The kind registry's `place` field carries either.

### 3. The core

Modules (indicative):
- `core/world.py`: state, chokepoint, hooks, causes, events, acts;
- `core/kinds.py`;
- `core/primitives.py`;
- `core/places.py`: the graph and routes (today's `layout.py` parcel graph);
- `core/goods.py`: containers, the base columns of items, carrying;
- `core/rights.py`: claims, groups, may-take, may-enter;
- `core/time.py`: calendar, clocks, keyed draws;
- `core/phases.py`;
- `core/call/`: decide, responders, conversations, tally, usage stops;
- `core/record/`: journal, branching, views, schema assembly;
- `core/view/`: `Here`, `Mind`, memory, knowledge levels and skill;
- `core/techniques.py`: resolve, site, readiness, shortfall, tools, skill, inputs and outputs, wear, with registries for yield kinds,
  site kinds and readiness by `draws`;
- `core/senses/`: the noticing rule, subject tables, emit and roll as one code path;
- `core/prompt/`: slots, the reply-schema assembly;
- `core/fuse.py`: the registry of urgent calls;
- `core/work.py`: the generic work loop;
- `core/packages.py`: the loader, the manifest, the `requires` filter, the manifest page.

**Primitives in the core** (from today's 36, of which about 14 are already generic):

| Primitive | Does |
|---|---|
| `spawn(kind, place, record)`, `retire(ref)` | a new entity of a registered kind; its end |
| `set(ref, field, value)` | any declared field of any registered kind |
| `transfer`, `create`, `destroy` | goods between containers, into being, out of being |
| `draw`, `add`, `set_stock` | a population or a coupled layer's cell |
| `move(ref, to)` | a person or a mobile body between places (today's `depart`, `arrive`, `transit`) |
| `claim`, `end_claim` | rights over a claimable kind |
| `join`, `leave` | group membership |
| `harm`, `die` | a body |
| `wear` | uses on a tool |
| `learn` | a level in a technique |

**Compound primitives** are registered by packages: named compositions of core primitives, whose inner calls the journal marks
`within`. Examples are `split_herd`, `plots` and `born`. Every compound primitive is listed on the manifest page.

**Hooks** replace the nine places where a core primitive calls a feature today:
- `farm.sync` after `claim`, `end_claim` and `plots`;
- `life.on_death` and things' remains after `die`;
- tags after `spawn`;
- the crop branch of `draw` becomes farming's population kind.

### 4. Packages

#### 4.1 A folder

```
cybertron2/packages/animals/
  __init__.py        PACKAGE = Package(...)          the manifest (below)
  data.py            species rows; items, techniques, fittings rows it adds
  kinds.py           the herd kind and its fields
  prims.py           split_herd, merge_herd
  phases.py          wander, graze and feed, the herd's night on a road
  yields.py          herd, milk, slaughter
  signs.py           rows for the herd, parcel and person subject tables
  prompt.py          "Leading:", the beast lines
  seed.py            the spec's `herds:`; grass on grazing covers
  with_farming.py    trampling, the grazed field's soil   (requires animals, farming)
  with_roads.py      the pack ox, herds lost on roads      (requires animals, roads)
  capacity.py        declarations for the capacity model
  tests/
```

#### 4.2 The manifest

```python
PACKAGE = Package(
    name="animals", requires=("land",), optional=("farming", "roads", "enclosure"), standard=False,
    kinds=[Kind("herd", category="population", table="herds", place="parcel|road", claimable=True,
                subject="herd", named="tag", fields=HERD_FIELDS, rule="animals.feed")],
    fields={"person": {"led": ...}},
    data={"SPECIES": SPECIES, "ITEMS": ITEM_ROWS, "TECHNIQUES": TECH_ROWS},
    physics={"animals": {...}},
    primitives={"split_herd": split_herd, "merge_herd": merge_herd},
    hooks=[],
    seed=[Seed("animals.herds", after=("core.places", "core.claims"), fn=seed_herds)],
    phases=[Phase("animals.wander", in_="night", after=("farming.crops", "enclosure.fences"), fn=wander),
            Phase("animals.feed", in_="night", after=("land.regrow", "animals.wander", "food.spoil"), fn=feed)],
    today={"driven": dict},
    verbs={"drive": Verb(args=..., cost=1, doc=..., when=has_herds, handler=drive)},
    yields={"milk": Yield(apply=milk, ready=milk_ready), "slaughter": ..., "herd": ...},
    terms={"carry": pack_ox_carry},
    here={"animals": HerdView},
    signs=SIGN_ROWS, prompt=PROMPT_LINES, fuse=[], incidents={"stray": stray},
    capacity=CAPACITY, bot=bot_rows, views=VIEW_TABLES,
)
```

Rows in `with_farming.py` and `with_roads.py` carry `requires=("farming",)` or `("roads",)`. The loader adds the package's own
name.

#### 4.3 The slots

| Slot | Registers | Replaces today |
|---|---|---|
| `requires`, `optional`, `standard` | hard dependencies; packages it works with; on by default | implicit imports; the water pack's switch |
| `kinds`, `fields` | new kinds (§2.1); fields on other kinds | the hard-coded kind chains; one `schema.FIELDS` |
| `data` | its tables; rows added to shared tables | one `data.py`; `pack` on three tables |
| `physics` | its section of the world's numbers, with clocks for its rates | one `PHYSICS`; one `clocks.RATES` |
| `primitives`, `hooks` | compound primitives; hooks before and after any primitive | nine core primitives calling features; installs in `World.__init__` |
| `seed` | spec sections it reads, as ordered steps; its filter for `variants.one_node` | 27 inline steps in `World.__init__` |
| `phases` | steps of the day, named, with `in_`, `after`, `before`, and what they read and write | the night written in three places; the settle step naming every feature |
| `today` | day keys it owns, kept under its name | the shared blackboard |
| `verbs`, `yields`, `sites`, `ready` | verbs for new kinds of act; yield kinds; site kinds; readiness by `draws` | one `VERB`; the `_technique` hub; `knowledge.ready`'s switch |
| `renewal` | rules, and what steps each | `NIGHTLY` as names |
| `terms` | terms in the core's named sums: food need, units, carrying, load, cold, visibility, food sources, company | closed formulas in `needs.food`, `units_for`, `capacity`, `load`, `cold`, `visibility` |
| `here` | a namespaced view (`here.animals`); mind stores it keeps | 45 wrappers in `Here` |
| `signs` | rows for subject tables; its context namespace; its walker; event kinds; ambient lines | `signs.facts`; the shared `context()`; lasting memory by keyword |
| `prompt` | lines into named slots; reply-schema fragments and their handlers; urgent-call words; night narration; record keys | `prompt.py`'s prose; the string splice; `night_lines` |
| `fuse`, `incidents` | urgent-call kinds; spec incident kinds | fuse.py holding the raid; `run.dawn`'s if-chain |
| `capacity`, `bot`, `views` | capacity declarations; its part of the scripted bot; its exported tables | the capacity model importing internals; `bot_plan`; `exchange.view_tables` |
| `tests` | its tests and fixtures | 39 test files at the root |

#### 4.4 `requires` and `unless`

Every registration may carry `requires` (all must be on) and `unless` (none may be on): rows, kinds' fields, phases, prompt lines,
verbs, yield kinds, terms, hooks and fuse kinds. The loader adds the defining package to `requires` and drops what fails. A
package's own `requires` is different: a hard dependency, without which the world does not build.

Integration files (`with_farming.py`) are where combined registrations are kept for maintenance. Correctness comes from `requires`,
not from where the file is.

**Packs become packages.** Today's `pack` on a row is `requires` with one name. A package that is off has none of its rows, phases,
signs, prompt lines or verbs. Today a pack only switches rows.

### 5. Senses

**Subject tables.** Sign tables are kept by subject kind (person, parcel, building, herd, thing, sky, road), owned by the core.
Packages add rows to them. A row lives in the folder of the most specific package that gives it meaning; that is a rule for
maintenance, not for correctness.

**The row** (fields added to today's rows):

| Field | Meaning |
|---|---|
| `name` | stable within the table; the sign id becomes `<subject>#<table>.<name>` (today `#<table><index>`) |
| `requires`, `unless` | §4.4 |
| `replaces` | names a row this one takes the place of when both hold (on a grazed pasture, "grazed bare" replaces "bare") |
| `rank` | precedence among rows that hold together; replaces today's lowest-index rule (`perceive.py:516`) and `HOLDING_ROWS = range(3, 10)` |
| today's keys | `when`, `text`, `sense`, `own`, `tags`, `knack`, `knows`, `lay`, `reach`, `night`, `who`, `eye`, `land`, `peek`, `gate` |

**Contexts by namespace.** A row reads `x.<package>.<field>` (`x.animals.slaughter`, `x.farming.crop`). Each package provides its
namespace for a subject. Namespaces are computed on first read, so a row that is never evaluated costs nothing.

**The declaration test.** Every row is evaluated against fixture contexts that contain only the namespaces its `requires` names.
Touching any other namespace fails the test, so a missing `requires` cannot pass silently.

**One code path for chance.** The road's `roll` with `mult=1`, the traces' own multiplier and `least=True` become parameters of the
one noticing rule ([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]), or rows declared as exempt with a reason.

**Keyed draws.** Each sign's notice draw is keyed by its id: `rng("notice", day, person, sign_id)`. Today one sequence per person
per day is consumed in candidate order (`perceive.py:370`, 383 to 428), so any added or removed row shifts every later draw. This
changes behaviour, so existing runs do not replay under the new code; it needs a decision (open question 4).

### 6. The day

- **One phase list.** The scheduler, branching and the spec read it.
  - Steps that commit (dawn, decide, talk, work, evening, settle, night, memory) are core phases.
  - Packages add sub-phases with `in_`, `after` and `before`, and declare the `today` keys and fields they read and write.
  - The order is resolved once per world by a topological sort, with ties broken by package order, and written into the
    journal's meta.
  - A test fails on a cycle, or on a phase that reads what another phase in the same step writes without declaring the order.
  - The night's 22 dependencies (inventory C §2.4) become `after` lines.
- **`today` by package:** `today["roads"]["travel"]`. This is a schema change ([[D4-100 The world record's shape is declared and versioned|D4-100]]).
- **The runner is an object,** not `locals()` through `CARRY`.
- **Structured results.** An act's result is `{kind, text, data}`. Budget, the lighten call, offer ids and the exported views read
  `data`, never the wording.
- **Request keys keep today's scheme.** A call that moves to another phase keeps its key, or a mapping is kept, so that runs started
  before the change can still resume.

### 7. The packages

About 22. "Standard" means on by default, so older world files load as they do now.

| Package | Holds | Standard |
|---|---|---|
| `land` | covers' words and ambient lines; wild stocks; gathering (forage, hunt, mine, quarry); WILD and HUNTED signs; land memory | yes |
| `weather` | the climate scheduler (a driven layer), environment queries, SKY signs, the cold and visibility terms | yes |
| `woods` | forests, felling, firewood; their renewal rules | yes |
| `fire` | hearths and fires at night, heat, fuel order, open fires; warmth terms | yes |
| `food` | eating, hunger, starvation, cooking, spoilage | yes |
| `shelter` | sleeping places, beds, gear, camps; `sleep`, `host`, `grant`; shelter terms | yes |
| `buildings` | structures, rooms, fittings, stores and overflow, tiers, monuments, repair, breaks | yes |
| `writing` | lines on buildings | no |
| `making` | recipes, fitting wear, mending | yes |
| `farming` | crops, holdings, soil, field works, sowing lore | per world |
| `enclosure` | fences and gates | per world |
| `animals` | herds (§2.3, §4) | per world |
| `wild` | the ecology branch's populations, groups, legends, methods, carcass decay | per world |
| `water` | fish and salt (the existing pack) | per world |
| `things` | piles, remains, carcasses, hiding, searching | yes |
| `burial` | graves, cairns | yes |
| `life` | stages, partners, birth, children, care, death, succession, inheritance | per world |
| `households` | group rules, `join`, `admit`, `found`, offices | yes |
| `exchange` | offers, agreements, settlement, debts | yes |
| `conflict` | attack, guard, fights, raids, thefts | yes |
| `roads` | travel, landmarks, traces, encounters, hidden ways | per world |
| `teaching` | watch, teach, learn, crafts heard | yes |
| `labour` | fatigue, work's food, skill fading | yes |
| `evening` | the evening step and meeting | per world |
| `tags` | referent tags | per world |

### 8. Tests and guards

| Test | Guards |
|---|---|
| Golden journals | each scripted world's journal before and after a change is byte-identical, except where a decided change says otherwise (today's `test_bot_run_is_deterministic` only checks a run repeats under the same code) |
| Prompt snapshot | the system and turn prompts of the scripted worlds |
| Import layers | P1; packages import only the core and their declared packages |
| Declaration | §5's namespace test; the same for phases' reads and writes |
| Null arm | a world with a package off has none of its registrations (from the manifest page) |
| Acceptance 1 | a new species (sheep) is rows in `packages/animals/` only |
| Acceptance 2 | a new feature with its own kind, phase, verb and signs (bees and a hive) is one new folder, no file outside it changed |
| Populations | counts kept across a draw of individuals and their return |

### 9. Order of work

| Phase | Work | Behaviour |
|---|---|---|
| 0 | Fix OPEN [[Q-49 Engine bugs found by the package inventory|Q-49]]'s bugs, the evening branching bug first; golden journals, prompt snapshot, import-layer test (reporting) | unchanged, except the bugs |
| 1 | Core registries with no code moved: kinds, schema fragments, phase list (with `branch.STEPS` from it), `today` keys with owners, hooks for the nine callouts, the runner object, the loader and `requires` filter generalising packs. Breaks the 26-module import loop | unchanged |
| 1b | Stable sign names, `rank`, `replaces`; keyed notice draws; structured results | changes noticing draws (decision) |
| 2 | The wild layer lands as `packages/wild/` (its 19 engine edits re-expressed as registrations) | as the branch |
| 3 | `animals` moved out as the pilot; acceptance test 1 | unchanged |
| 4 | The rest, least coupled first: water, writing, tags, burial, teaching, labour, roads, evening; then farming, enclosure; then buildings, shelter, fire, food, life, with the signs and prompt split | unchanged |
| 5 (separate decisions) | Populations in one form; layers first-class; the grid choice (§2.6); weather coupled if wanted | behaviour changes |

#### 9.1 Alongside other work: in parallel, but not on a long-lived branch

**Proposed:** content goes on during the refactor, but the refactor merges into `main` in small steps, not on one branch that is
folded in at the end.

**Why not one long branch.**
- **Most engine commits would need porting by hand.** Since 23 Oct, 165 of the 208 commits touching the engine touched at least
  one of the six files the refactor splits (`data.py`, `verbs.py`, `run.py`, `prompt.py`, `signs.py`, `world.py`). On a branch
  where those files are split up, about four in five of `main`'s engine commits would have to be re-expressed by hand.
- **The golden baseline moves.** Calibration briefs change behaviour on `main` all the time, so the branch's golden journals must
  be re-taken at every sync.
- **The branch chases a moving target.** Porting debt grows at about 1 to 1.5 builder-days a week for each session building
  content, against a refactor pace of about 3 to 4 active days a week.
  - With one content session, that roughly doubles the calendar time.
  - With two, the branch may not catch up at all.
- **Everything lands at once.** The fold-in becomes one large, risky merge at the end.

**How it runs instead:**
1. **A spike branch, 3 to 5 builder-days, run beside content.** Build the core registries and the animals pilot roughly, to test
   the design: the manifest, the phase sort, `requires`, lazy sign contexts and their speed. Kept for reference or thrown away;
   never merged as it is.
2. **Phases 0, 1 and 1b on `main`, in small commits,** each checked against the golden journals.
   - Phase 1 adds the registries beside the old paths and moves no code, so it barely conflicts with content work.
   - Phase 1b changes the notice draws once, on a named day, so content sessions re-take their baselines together.
3. **From the end of phase 1, new features are written as packages.** The migration's cost stops growing. The wild layer lands as
   the first package.
4. **Each package moves on a short branch** of 1 to 3 days, with a freeze on that package's files announced on the board. Content
   work on other packages goes on meanwhile.

### 10. Estimate

From the inventory and the engine's size by file. A **builder-day** is one active day of a building session, the unit in which
the engine was built: it took about 23,800 lines added over 12 active days (23 Oct to 12 Nov), and the wild branch 8,200 over 4.
A refactor is slower per line than new code, because every step is checked against the golden journals and the full suite. The
ranges carry that uncertainty.

| Phase | Lines moved | Lines rewritten | Lines new (code and tests) | Builder-days |
|---|---|---|---|---|
| 0 Guards and bugs | 0 | about 100 | about 600 | 1 to 2 |
| 1 Core registries | 0 | about 1,500 (`world.py`, `run.py`, `branch.py`, `schema.py`, `here.py`, farm, life and tags callouts) | about 1,500 (loader, kinds, phases, `requires`, runner object) | 4 to 6 |
| 1b Sign names, draws, results | 0 | about 900 (names on about 490 rows, mostly generated; perceive; result readers in run, evening, exchange) | about 200 | 2 to 3 |
| 2 Wild as a package | about 5,000 (its own modules) | about 1,800 (its edits to 21 engine files on `ecology-hunt3`, as registrations) | about 300 | 4 to 7 |
| 3 Animals | about 2,000 | about 500 | about 400 | 3 to 4 |
| 4 The rest | about 12,000 | about 5,000 (signs walker and contexts about 1,000; prompt into slots about 700; view about 200; the technique hub about 600; night into phases about 500; run's feature logic about 700; `Here` namespaces about 400; needs terms about 300; the rest) | about 800 | 12 to 17 |
| Tests (across phases) | 39 files move into packages | about 2,500 (37 files import engine modules; about 625 references by module alias) | (above) | included |
| **Total, phases 0 to 4** | **about 14,000 of the engine's 20,400** | **about 7,000 to 9,000** | **about 3,000 to 4,000** | **about 26 to 39** |
| 5 Object model | | about 2,500 and up (populations about 1,500; layers about 1,000; the grid choice could double this) | | 5 to 15 |

**What it comes to:**
- **Diff size:** the git diff for phases 0 to 4 is about 35,000 to 45,000 lines, since moves count twice.
- **Net size:** the engine grows by about 1,500 to 3,000 lines: the registries add code, and removing the special cases and the
  duplicates takes some away.
- **Calendar time:** at the engine's own pace (12 active days in three and a half weeks), 26 to 39 builder-days is about five to
  nine weeks for one session. After phase 1, phase 4's packages can be split between two sessions, since they no longer share
  files, which brings it to about four to six weeks.
- **Conflicts:** 37.2 and 37.4 keep building content on branches during this. Each package's move needs a short freeze on the
  files it takes, and work in flight has to be rebased.

**The cheaper path** is phases 0, 1, 1b, 2 and 3: about 13 to 21 builder-days and 7,000 to 9,000 lines of diff.
- **What it gets:** the dependency inversion, the `requires` rule, the phase list, stable sign names, the wild layer as a package
  and a proven pilot.
- **After that:** new features are written as packages, and old code moves into packages when it is next substantially edited, the
  strangler pattern. The whole migration then costs little extra, but it never finishes on a date, and the core carries both forms
  for a while.

### 11. What packages save, and what waiting costs

**What building looks like today** (measured from git, 23 Oct to 16 Nov):
- **The hub files.** Of 208 commits touching the engine, `data.py` is in 75, `verbs.py` in 63, `run.py` in 50, `prompt.py` in 48
  and `signs.py` in 47. These five files are where concurrent sessions meet.
- **The spread of a feature.** Across the wild briefs, the lines written into existing engine files (not the feature's own files)
  were:

  | Branch (in order) | Existing engine files edited | Lines there | Lines in its own files |
  |---|---|---|---|
  | `ecology` | 13 | 651 | 3,098 |
  | `ecology-raiders` | 17 | 692 | 3,834 |
  | `ecology-carcass` | 18 | 963 | 3,994 |
  | `ecology-hunt3` | 21 | 1,835 | 4,982 |

  So about a quarter of a feature's code lands in files other features share, and that share grew with each brief.

**What packages save.**
- The integration share moves into the feature's own folder as registrations. The lines are still written, but:
  - they no longer collide with other sessions' work in the hub files;
  - they need only the core's interface, not the internals of the 20 files they touch today;
  - they cannot break another feature through a shared hub.
- They do not save design, calibration, runs or analysis. Those dominate content-heavy work: the hunt took briefs 4, 4b and 4c,
  mostly calibration.
- **A judgement, not a measurement:** about 10 to 20% less building time per feature, more for features that cross many others.
- Two larger effects follow:
  - two or three sessions can build different packages at once without meeting in `data.py` and `signs.py`;
  - the cost of a feature stops growing with the size of the engine.

**What waiting costs.** Every feature built the old way joins the migration:
- **Its own files** move cheaply: on the order of 2,000 lines a builder-day.
- **Its edits to shared files** must be re-expressed as registrations and checked against the golden journals: on the order of
  300 to 400 lines a builder-day, the pace phases 1 and 4 assume.
- **The couplings built on top of it** must be untangled. This is the part that grows faster than linearly, since each new feature
  can touch every one already there.

Measured: the wild layer's shared-file edits went from 651 to 1,835 lines in five days of briefs, which took its own move from about
3 to about 6 builder-days. On the order of 10,000 more lines built the old way, at today's quarter in shared files, would add about
10 to 15 builder-days to the full migration.

**Phase 1's value grows with every feature built after it, and its cost hardly grows** (about 4 to 6 days, unchanged). Once the
registries exist, new features can be written as packages before any old code moves. That is why phase 1 is the part worth doing
soon, whatever is decided about the rest.

**Is it worth it?** It depends on how long C2 keeps growing.
- **Phases 0, 1 and 1b: worth it on any horizon** (about 7 to 11 builder-days).
  - They fix bugs that are live now: branching fails on evening worlds.
  - They fix two faults in experiment design, whatever the build pace:
    - a pack switched off leaves its signs and prompt prose live, so a null arm is not clean;
    - one shared sequence of noticing draws means any added row changes what people notice about unrelated things.
  - They stop the migration's cost from growing.
- **The cheaper path (13 to 21): worth it if building continues at about today's pace for two months or more,** with more than one
  session at once.
  - At about 10 to 20% saved per feature, plus avoided conflicts, it pays back in roughly two to four months of building.
  - Waiting adds about 1 to 1.5 builder-days a week of building to the eventual move.
- **The full migration in one push (26 to 39): worth it only if C2 is a long project.** Otherwise the strangler path gets most of
  the value: old code moves into packages when it is next edited.
- **If C2 is near its last big features, it is not worth it beyond phase 1b.**

## What the inventory found

| Layer | Today | What matters here |
|---|---|---|
| Size | `engine/` 20,449 lines in 46 files | nine files hold 55%: `verbs.py` 2,009, `signs.py` 1,969, `farm.py` 1,519, `run.py` 1,306, `world.py` 1,075 |
| Imports | 26 of the 44 engine modules form one import loop | 162 function-level imports hide it; with them taken out there is no loop at module level |
| State | 25 top-level keys | about 20 of a parcel's 29 fields belong to one feature; `schema.FIELDS` is one closed list |
| Primitives | 36 | about 14 generic; nine call into features |
| Hooks | 3 after-hooks registered, no before-hooks | the core calls features directly instead |
| Data | 47 tables in `data.py` | `TECHNIQUES`, `FUSE`, `MODIFIERS` added to by hand; `pack` on three tables; derived tables ignore packs; one `PHYSICS` bag |
| World build | 27 ordered steps in `World.__init__` | woods, grass, fences, works, crops, herds, rooms, households, claims, minds seeded inline |
| Agent's view | about 80 methods on `Here` | about 45 thin wrappers importing features |
| Verbs | 38 verbs, 21 yield kinds | one if/elif hub; 4 kinds with distributions; farm kinds listed three times; about 30 special cases keyed on names |
| Senses | 34 sign tables | one walker over eight features; one shared context; rows picked by position; tables mixing features; three chance paths on the road |
| Prompt | 8 system blocks, 13 turn sections | prose of about ten features in `prompt.py`; `view.py` zips lines by position; blocks spliced by string replace |
| The day | 8 steps | the night written by hand in three places with 22 dependencies; `today` with about 40 keys and no owner; result lines used as a message bus |

The bugs found on the way are in OPEN [[Q-49 Engine bugs found by the package inventory|Q-49]].

## Why

- **Growth.** 02zv's ledger and 02zzj's economy research queue hundreds of content items. At the wild layer's rate (19 engine files
  for one feature), each feature raises the cost of the next. A package confines it to a folder.
- **The design rules point here:**
  - [[D4-24 The world grows by data, and agents explore and learn it|D4-24]] (the world grows by data on a few verbs);
  - [[D4-34 Rebuild the M1 engine on the designed general core|D4-34]] (one chokepoint with hooks);
  - [[D4-103 The engine overhaul goes ahead, in phases|D4-103]] (each process declared once, beside its code);
  - [[D2-203 Each wild kind's behaviour is designed first, then built as a module…|D2-203]] (a wild kind as a module acting only through primitives).

  Packages are where those declarations live.
- **Clarity.** One feature is one folder and one manifest.
- **Clean null arms** (scenario_design.md). P7 makes "the world without X" exactly the world minus X's registrations.

## What is weak about this design

- **Indirection.** The night becomes a sorted list, not a sequence on the page. The manifest page and the resolved order in the
  journal answer this only in part.
- **Twenty-two packages may be too fine;** about 12 is a reasonable alternative.
- **Sign contexts must be lazy,** or the cost of perception grows with every package.
- **It does not make content into data by itself;** 02zv's C1 to C3 do that. This is where that content would live.
- **The estimate is uncertain.** No refactor of this size has been done on this engine. The pace figures come from new code, and
  the full suite is slow to run, which sets the pace of checking.

## Alternatives considered

1. **Break the cycles only:** phase 1 alone. Cheap, and most of the dependency gain; but a feature still edits the shared signs,
   prompt and data files.
2. **Folders by technical role** (`signs/`, `prompt/`, `verbs/`, each split by feature). Closer to today, but a feature still spans
   five folders.
3. **A full entity-component system.** The JSON state, primitives and journal already give its benefits for replay; rewriting to one
   costs a great deal for little here.
4. **Integration only by file loading** (this proposal's first draft). Replaced by `requires` on every registration (History, 16 Nov).

## Open questions

1. **How fine to cut:** about 22 packages, or about 12?
2. **Food, shelter and fire:** standard packages, or core?
3. **`today` by package:** a [[D4-100 The world record's shape is declared and versioned|D4-100]] schema change. Acceptable?
4. **Keyed notice draws (§5):** they change what people notice in existing worlds, so runs from before do not replay under the new
   code. Accept, as phase 1b?
5. **Scope and pace:**
   - the whole migration (26 to 39 builder-days);
   - the cheaper path (13 to 21), then packages as features are touched;
   - phase 1 only.
6. **The grid (§2.6):** the 150 m cells as the base space, or one grid per layer with mappings? This is a decision of its own,
   outside the estimate.
7. **Weather (§2.2):** keep it driven (every arm meets the same weather, and no fork can set a storm), or allow a coupled weather
   later?
8. **Order against the wild layer,** and who builds: phase 1 before the wild branch merges, then the wild layer as the first package
   (recommended)? Is it 37.4's to build?

## Affects

On decision:
- spec/core/architecture.md (principles, core, packages);
- a new spec/core/objects.md (the six categories, the kind registry, layers, populations);
- spec/core/round.md and spec/record/execution.md (the phase list; the evening step);
- spec/core/world_schema.md (fragments; `today` by package);
- spec/core/processes.md (packs become packages);
- guides/senses.md and spec/information/ (subject tables, row names, keyed draws).

## History

- **16 Nov 2026: proposed.** Zach: "do a deeper dive to think about a cleaner way to separate each package into an actual package
  of related features and data etc. the code should be a clear set of primitives to exist with the world, with features mostly
  being labelled data on these primitives ... if each package had everything relevant, what would be all the things it would need to
  register. I like the idea of each being its own folder." Built on a read of every engine module (docs/review/40_feature_packages/).
- **16 Nov 2026: revised into a design specification,** with an estimate.
  - **The object model added (§2).** Zach asked what each object type has and what almost everything requires, what kind of object
    weather is, and what wildlife and ecosystems are. The answer: six categories with base shapes; layers driven or coupled;
    populations with the rule for drawing individuals out; ecosystems as types.
  - **Integration by loading files replaced by `requires` and `unless` on every registration.** Zach: "each sign can register which
    other packages it requires ... we only include the subset where all package requirements are fulfilled". Added with it: subject
    tables, stable row names, `rank` and `replaces`, the namespace declaration test, and keyed notice draws.
  - Zach asked for it as a spec with the work estimated (§9, §10). It is kept as a proposal until decided, per the folder's rules.
- **16 Nov 2026: §11 added.** Zach asked how much easier building becomes and how the cost grows if more is built first. The
  answer is measured from git: hub-file commits, and the wild briefs' spread from 651 to 1,835 lines in 21 files. Phase 2's estimate
  is raised to 4 to 7 days to match `ecology-hunt3`.
- **16 Nov 2026: §9.1 added.** Zach asked whether to refactor on one branch while development goes on and fold the later features in.
  The answer: in parallel, but merged into `main` in small steps after a short spike, since about four in five engine commits touch
  the files the refactor splits.

## Sources

- docs/review/40_feature_packages/inventory_A.md to inventory_E.md;
- spec/core/architecture.md, processes.md, world_schema.md;
- proposals/engine_overhaul.md, process_model.md, wild_layer.md;
- docs/review/37_growth/02zv_wild_consolidation.md (C1 to C5, C8, §4);
- `engine/climate.py`;
- the `ecology-hunt3` branch (`cybertron2/wild/ecology.py`, `engine/wild.py`, schema 5);
- git history of `cybertron2/engine/` (pace);
- WORK [[W-43 The engine as feature packages|W-43]]; OPEN [[Q-48 The engine as feature packages|Q-48]] to [[Q-50 One grid or several|Q-50]].
