# The engine as a small core and feature packages

**Status:** discussion (16 Nov 2026). Nothing decided, nothing built.
**Owner:** lead session (C1 wrap-up), for 37.4 (the code under `cybertron2/` is 37.4's) and Zach.

## Summary

Today a feature is spread across the engine. The wild layer is the clearest case: it has its own folder (`cybertron2/wild/`,
on the `ecology` branches), yet it also edits 19 existing engine files: `signs.py` +400 lines, `data.py`, `verbs.py`, `world.py`,
`schema.py`, `renewal.py`, `perceive.py`, `prompt.py`, `run.py`, `night.py`, `settle.py` and more. It also edits four
land-generator files and the capacity model.

The proposal has three parts:
- **A core** that holds only what every world has: places, people, goods in containers, rights, time and chance, the chokepoint,
  the day's scheduler, the model calls, the record, the agent's view, the technique engine and the machinery of the senses and
  the prompt.
- **Packages.** Everything else becomes a package: one folder per feature. Each package declares, in one manifest, everything it
  adds to the core: entity kinds and fields, data rows, primitives and hooks, seeding, steps of the day, verbs and yield kinds,
  signs, prompt lines, urgent calls, capacity declarations and tests.
- **One direction of dependency.** The core never imports a package; a test enforces it.

A feature is then mostly labelled data on the core's primitives. Code is needed only for:
- a new kind of thing in the world (a herd);
- a new kind of change (a yield kind);
- a process with its own dynamics (a night step);
- the context its signs read.

A package that needs a new primitive names it in its manifest.

The inventory behind this note is in [docs/review/40_feature_packages/](../../review/40_feature_packages/) (five files, A to E,
with line numbers).

## What the engine is made of today (the inventory, in brief)

| Layer | Today | Findings that matter here |
|---|---|---|
| Size | `engine/` 20,449 lines in 46 files | Nine files hold 55%: `verbs.py` 2,009, `signs.py` 1,969, `farm.py` 1,519, `run.py` 1,306, `world.py` 1,075 |
| Imports | 26 of the 44 engine modules form one import loop | Function-level imports hide it: 162 of them; with them taken out there is no loop at module level |
| State (`World.s`) | 25 top-level keys; records of node, road, parcel, building, herd, container, person, institution, claim, offer and agreement | About 20 of a parcel's 29 fields belong to one feature (farming, fences, combat, forests, meetings); people and buildings are the same. `schema.FIELDS` is one closed list |
| Primitives | 36 in `PRIMITIVES` | About 14 are generic: transfer, create, destroy, draw, add_res, set_res, set, set_thing, new_thing, depart, arrive, transit, harm, wear. Nine call into features: `draw`, `claim`, `end_claim`, `plots`, `shares`, `set_share` call farm; `new_herd`, `split_herd`, `new_thing` call tags; `die` calls things, life and roads; `born` calls generate, knowledge and perceive |
| Hooks | The mechanism exists; 3 after-hooks are registered (agreements' credit on transfer; buildings' overflow on create and transfer); no before-hooks | The core calls features directly where a hook would do |
| Entity kinds | Hard-coded in `place_of`, `p_set` and the claim refs | Adding a kind means editing all three |
| Data | 47 tables in `data.py`, already roughly in feature order | `TECHNIQUES`, `FUSE` and `MODIFIERS` are added to by later sections (features already "register" rows, by hand). Only `ITEMS`, `RESOURCES` and `TECHNIQUES` carry `pack`. Derived tables (EDIBLE, TOOLS, WEAPONS, CROP_OF) ignore packs. `PHYSICS` is one bag of every feature's numbers |
| World build | `World.__init__` runs 27 ordered steps | It seeds woods, grass, fences, field works, crops, herds, rooms, households, claims, knowledge, minds and things inline |
| Agent's view | `Here` has about 80 methods | About 45 of them are thin wrappers that import a feature (weather 7, things 12, life 5, herds 4, tags 3, layout 3) |
| Verbs | 38 verbs | `gather`, `work` and `make` are generic over data. 21 yield kinds dispatch through one if/elif hub (`verbs._technique`); 4 have outcome distributions for the capacity model; farm's yield kinds are listed in three places. About 30 special cases keyed on a name hide features in generic code (`tech == "fell"`, `"method: cairn"`, stone building gated on knowing the fencing technique `wall`) |
| Senses | 34 sign tables | `signs.facts` is one walker over eight features. `signs.context()` is one context shared by six tables. FIELD's per-holding rows are picked by position (`range(3, 10)`). Tables mix features (PERSON has rows from slaughter, hunting, leading a beast, guarding, care). On the road the "one noticing rule" is three code paths |
| Prompt | 8 system blocks, 13 turn sections | `prompt.py` imports about ten features and holds their prose. `view.py` zips prompt lines against a subject list built separately, so one added line breaks it. Blocks are spliced in by replacing the text "Reply with JSON only." |
| The day | Steps dawn, decide, talk, work, evening, settle, night, memory | The night's order is written by hand in three places (`run.py`, `night.night` with 22 steps, `farm.night`), with 22 ordering dependencies between steps. `today` is a shared blackboard: 19 keys set at dawn, about 20 more added by verbs, farm, labour, roads, fuse, night and the evening |
| Between features | | Result lines are a message bus: "You said (" counts units, "Refused: travel: you carry" triggers the lighten call, "You offered " is parsed for the offer id, and the published views re-parse "You told". A rewording breaks budget, lighten and the views |

**Bugs found on the way.** They are worth fixing whatever is decided here; listed for 37.4 in OPEN.md.
1. **The evening step breaks branching.** `branch.STEPS` has no "evening", so `rewind`, `fork` and `continue` raise `ValueError`
   on any world with `evening:` (for example `specs/fishing/water.yaml` and the goal probes). Checked in Python.
2. **A change journaled under the wrong step.** `labour.close_day` runs between two steps, so its changes are journaled under a
   step that is already committed.
3. **A dangling reference.** `data.py` names a `roads.CHALLENGES` that does not exist.
4. **Dead or out-of-date code:**
   - `knowledge.ready` lines 185-209 cannot be reached;
   - `chronicle.py` is imported nowhere and parses prompt headers;
   - `farm.frost_kills` is the rule from before D4-106 and is still used by `capacity/cal.py`, so the capacity model can differ
     from the engine;
   - `farm._f_default` and `forests.fuel_order` read the global `PHYSICS`, so a world's own physics is ignored there.
5. **Young beasts never grow** into cows, oxen or bulls.

## The proposal

### 1. The core: what every world has

The core is the object model, the primitives, and the machinery that runs them. It holds no feature's nouns.

**Entity kinds in the core:**
- **Node** and **parcel**: the parcel graph, cover, size, adjacency and stocks by resource key.
- **Road**: an edge with days and stretches.
- **Person**: alive, where, transit, hands.
- **Container**: goods with a place: hands, a store, something left at a spot.
- **Group**: members and offices, kind-free.
- **Claim**: rights over any claimable kind.
- **Event** and **act**.

Building, herd, offer and agreement become kinds that packages register.

**Core primitives,** generic over kinds (about 14, close to the generic set that exists now):

| Primitive | Does |
|---|---|
| `spawn(kind, place, record)` / `retire(ref)` | a new entity of a registered kind; its end. The new form of `new_thing`, `raise`, `new_herd`, `offer`, `agree` and `born`'s record |
| `set(ref, field, value)` | any declared field of any registered kind; replaces the hard-coded kind table in `p_set` |
| `transfer`, `create`, `destroy` | goods between containers, into being, out of being |
| `draw`, `add`, `set_stock` | a stock on a parcel (today `draw`, `add_res`, `set_res`, without the crop branch) |
| `move(ref, to)` | a person or a mobile entity between places (`depart`, `arrive` and `transit` unified, with the road stretch) |
| `claim`, `end_claim` | rights; packages hook them (farming's holdings follow claims) |
| `join`, `leave` | group membership |
| `harm`, `die` | a body; packages hook `die` (life's succession and inheritance; things' remains) |
| `wear` | uses on a carried tool |
| `learn` | a person's level in a technique |

A package may register a **compound primitive** (`split_herd`, `plots`, `born`). It is a named composition of core primitives
applied inside it, and the journal marks those inner calls `within`, as nested applies are marked today. Each compound primitive is
listed with its package in the manifest page (below).

**Machinery in the core:**
- the chokepoint (`apply`, hooks before and after, causes, the journal);
- the entity-kind registry (place rule, fields, claimable, container, subject of senses, how it is named);
- seeding by registered steps;
- the scheduler (a phase list, below);
- model calls (decide, responders, conversations, tally, usage stops);
- the record (journal, branching, views, schema assembled from fragments);
- time (calendar, clocks, keyed randomness);
- `Here` and `Mind` (place-scoped, extended by namespaced package views);
- the technique engine (resolve, site, readiness, shortfall, tools, skill, inputs and outputs, wear) with registries for yield kinds,
  site kinds and readiness checks;
- knowledge levels and skill;
- memory;
- the noticing rule and the sign machinery (rows, `when`/`text`, `own`, `reach`, `knows`/`lay`, bundles, emit, roll), as one code
  path;
- prompt assembly from slots, and reply-schema assembly from fragments;
- the urgent-call (fuse) registry;
- the generic work loop (interleaving, budget, cost, refused-dedupe, fallback);
- structured results in place of result strings.

### 2. A package: one folder, one manifest

Each package is a folder under `cybertron2/packages/`. Its `__init__.py` holds one `Package(...)` manifest, a literal so that
it can be searched. The slots below cover everything the five inventories found the engine doing; most packages use few of them.

| Slot | What it registers | Replaces today |
|---|---|---|
| `requires`, `optional` | other packages it needs, or works with when on | implicit imports |
| `kinds` | new entity kinds (table, place rule, fields, claimable, container, tag namer), and fields added to core kinds (`person.stage`, `parcel.crop`) | the kind chains in `place_of`, `p_set`, claim refs; `schema.FIELDS` as one list |
| `data` | its own tables, and rows added to shared tables (ITEMS, TECHNIQUES, RESOURCES, FITTINGS, COVERS' ambient lines, EVENT_EXTENT, NOTICING presence); rows are tagged with the package's name automatically | one `data.py`; `pack` on three tables only |
| `physics` | its section of the world's numbers (`p.animals`, `p.farming`), with the clocks of its rates | one `PHYSICS` bag; `clocks.RATES` as one list |
| `primitives`, `hooks` | compound primitives; before and after hooks on any primitive | the nine core primitives that call features; `AG.install` and `BL.install` called from `World.__init__` |
| `seed` | spec sections it reads, as ordered steps (`after=`), and its filter for `variants.one_node` | 27 inline steps in `World.__init__` |
| `phases` | steps of the day it adds, each named, with `after=` and `before=` | the night written in three places; the settle step naming every feature; `run.dawn`'s incidents |
| `today` | day keys it owns, with their start value, kept under its own name (`today["roads"]`) | the shared blackboard |
| `verbs` | verb rows (args, cost, doc, `when`, handler) only for new kinds of act; otherwise technique rows on `gather`, `work`, `make` | one `VERB` and `HANDLERS` |
| `yields`, `sites`, `ready` | yield kinds (apply, optional distribution for capacity, readiness, counts as practice, result words); site kinds (`at` keys); readiness by `draws` | the `_technique` if/elif hub; `knowledge.ready`'s string switch; three copies of the farm kinds |
| `renewal` | renewal rules, each with what steps it (night, or its own process) | `NIGHTLY` as a tuple of names |
| `terms` | terms added to the core's named sums: needs (food), units, carrying capacity, load, cold, visibility, food sources, company | closed formulas in `needs.food`, `World.units_for`, `capacity`, `load`, `cold`, `environment.visibility` |
| `here` | a namespaced view (`here.animals.herd(x)`) and mind stores it keeps (`beasts`, `land`) | 45 thin wrappers in `Here` |
| `signs` | sign tables by subject kind, a context provider for its own state, a walker that names the subjects it speaks about, event kinds (extent, dawn, routine, witness-only, lasting), ambient lines; rows it adds to another package's subject table | `signs.facts`; the shared `context()`; keyword-matched lasting memory |
| `prompt` | lines into named slots (system "how life works", Here's place line, a building's line, You, sections of its own); reply-schema fragments and their handlers in the talk step; urgent-call words; night narration from its night record keys; record keys for the day log | `prompt.py`'s prose; the string splice; `night_lines`; the day print |
| `fuse` | urgent-call kinds (source, detector, choices, words, bot answer) | `fuse.py` holding the raid; road kinds registered as an import side effect |
| `incidents` | spec incident kinds (`stray`, `fire`, `death`) | the if-chain in `run.dawn` |
| `capacity` | the pure functions and distributions the carrying-capacity model reads | the capacity model importing feature internals |
| `bot` | its part of the scripted bot's plan and urgent answers | `bot_plan` and `bot_fuse` knowing every feature |
| `views` | its tables in the exported record | `exchange.view_tables` |
| `tests` | its own tests and fixtures, in the folder | 40 test files at the root |

**Integrations** sit in the package that arrives later, in a file named for the other package. For example
`animals/with_farming.py` holds trampling and the grazed field's soil; it is loaded only when both packages are on. This is where
today's couplings go: `h.ate` passed from trampling to feeding; pack oxen on roads; dogs at a slaughter; stalls in buildings.

**Packs become packages.** A package that is off has none of its rows, and none of its phases, signs, prompt lines or verbs. Today
a pack only switches rows, so a world with the water pack off still carries its sign rows and prompt prose. A set of standard
packages is on by default, so older world files load as before.

**The manifest page.** `python -m cybertron2.engine manifest` prints, for a world, every package with its registrations, the phase
order as resolved, and each package's lines of code against its rows of data. The registry makes "where does X happen" a lookup
rather than a grep, and it keeps the growth of code beside data in sight.

### 3. The day as a phase list

There is one list of phases. The scheduler, branching (`branch.STEPS`) and the spec read it, so the evening bug cannot recur. A
step that commits is a phase with `commit=True`. Packages add sub-phases with `after=` and `before=`.
- The order is resolved once per world: a topological sort, with ties broken by package order.
- It is written into the journal's meta.
- A test fails on a cycle or on a dependency that is not declared: a phase reading a `today` key or a field that another package
  writes in the same step must declare it.

The night's 22 dependencies (inventory C §2.4) become `after=` lines next to the steps they constrain. For example:
- `food.eat` comes after `fire.house_fires` and `life.care_gifts`;
- `animals.feed` comes after `land.regrow`, `farming.crops` and `animals.wander`.

The runner's state becomes an explicit object, not `locals()` through `CARRY`.

### 4. Animals: a new kind of thing, not one primitive

**A herd is already its own kind of entity:**
- It has a place: a parcel, or a road with a stretch.
- It has claims, tags and signs, and its own primitives (`new_herd`, `split_herd`).
- It is a count of beasts by role, not individual animals.

**An `animals` package registers:**
- **The kind:** `herd` (fields, the place rule including roads, claimable, tag namer).
- **A species table:** roles, breeding, milk, dung, fodder need per head, nights to starve, what slaughter gives. Today only
  cattle exists, partly as `PHYSICS.cattle` and partly as code.
- **Compound primitives:** `split_herd` and `merge_herd`.
- **Phases:** wander and graze and feed (after the land's regrowth, the crops and the fences), plus the herd's night on a road.
- **Techniques and yield kinds:** herd, milk, slaughter, gather dung; and the `drive` verb.
- **Signs:** HERD, ASTRAY, EMPTY, DRIVEN, SLAUGHTER, and the rows it adds to PERSON (leading a beast, blood from a slaughter).
- **Prompt and capacity:** its prompt lines and its capacity declarations.
- **Integrations:** `with_farming` (trampling, grazing), `with_roads` (the pack ox, herds lost on roads, urgent calls about found and
  split herds) and `with_enclosure`.

**The wild layer's kinds are a second kind of the same family.** The `ecology` branches keep wild populations by area, not at a
place. Kept herds and wild populations should share the species rows: the traits of 02zv's C1. That makes a sheep or a goat a
species row. A wild kind is a row on the other kind, with D2-203's module for its behaviour inside its package. Individual beasts
(a trained ox with a bond, a dog; 02zv C8) would be a third kind, registered when needed.

The same test answers when something needs a new kind of entity: does it have a place and state of its own that changes over
time? A herd, a building and an agreement do. A crop does not; it is fields on a parcel's holding.

### 5. The packages, as cut from the inventories

About 22. Each name says what the folder holds. "Standard" means it is on by default.

| Package | Holds (from today's modules) | Standard |
|---|---|---|
| `land` | covers' words and ambient lines; wild stocks (plants, game, seam, quarry); gathering techniques (forage, hunt, mine, quarry); WILD and HUNTED signs; land memory | yes |
| `weather` | climate scheduler, environment queries, SKY signs, the cold and visibility terms | yes |
| `woods` | forests (trees, young, dead), felling, firewood; their renewal rules | yes |
| `fire` | hearths and fires at night, heat, fuel order, open fires; the warmth terms in needs | yes |
| `food` | eating, hunger, starvation, cooking, spoilage | yes |
| `shelter` | sleeping places, beds, gear (tent, bedroll), camps; `sleep`, `host`, `grant`; the shelter terms | yes |
| `buildings` | structures, rooms, fittings, stores and overflow, tiers, monuments, repair, breaks | yes |
| `writing` | lines on buildings, `write`, `erase`, reading | no |
| `making` | recipes, fitting wear, mending | yes |
| `farming` | crops, holdings, soil, field works, sowing lore; `plots`, `shares` | per world |
| `enclosure` | fences and gates | per world |
| `animals` | herds (above) | per world |
| `wild` | the ecology branch's populations, methods and carcass decay | per world |
| `water` | fish and salt (the existing pack) | per world |
| `things` | piles, remains, carcasses, hiding, searching | yes |
| `burial` | graves, cairns, the `bury` technique | yes |
| `life` | stages, partners, birth, children, care, death, succession, inheritance | per world (`children:`) |
| `households` | group rules, `join`, `admit`, `found`, offices | yes |
| `exchange` | offers, agreements, settlement, debts | yes |
| `conflict` | attack, guard, fights, raids, thefts | yes |
| `roads` | travel, landmarks, traces, encounters, hidden ways | per world (with roads) |
| `teaching` | watch, teach, learn, crafts heard | yes |
| `labour` | fatigue, work's food, skill fading | yes |
| `evening` | the evening step and meeting | per world |
| `tags` | referent tags and naming | per world |

There are two cut lines to decide (open questions 1 and 2): whether `food`, `shelter` and `fire` are packages or core, and whether
`writing` and `burial` stand alone.

### 6. Order of work

Each step must leave every scripted (bot) run byte-identical to the same run before the step. Today's test
(`test_bot_run_is_deterministic`) only checks that a run repeats under the same code, so step 0 adds two tests:
- a golden comparison of the scripted worlds' journals before and after a change;
- a prompt snapshot, so that a moved prompt line is caught.

0. **Guards and fixes, no change of behaviour:**
   - the bugs above, the evening branching bug first;
   - a prompt-snapshot test over the scripted worlds;
   - the import-layer test, reporting only.
1. **Registries in the core, with no code moved:**
   - the kind registry, replacing the chains in `place_of`, `p_set` and the claim refs;
   - schema fragments;
   - the phase list, with `branch.STEPS` read from it;
   - `today` keys declared with owners;
   - hooks in place of the nine core-to-feature calls (`farm.sync` on claim, `life.on_death` on die, tags on spawn).

   This breaks the 26-module loop. It is the largest gain for its size, and it is worth doing even if nothing else here is
   accepted.
2. **The wild layer lands as the first package.** It is new code that is not merged yet, so it is the cheapest to place well, and
   it is the acceptance test: merged as `packages/wild/` with no edit to `signs.py`, `prompt.py`, `verbs.py` or `world.py` beyond a
   registry the core already has.
3. **`animals` as the first package moved out of the engine.** It touches every slot, and it is the example asked about.
   Acceptance: a second species (sheep) is added as data rows in `packages/animals/` only.
4. **The rest, the least coupled first:** water, writing, tags, burial, teaching, labour, roads, evening; then farming and
   enclosure; then buildings, shelter, fire, food, life.

### Acceptance tests

Like fishing for the process model (D4-103), each acceptance test is a feature added with a limit on what it may touch:
1. A new species: rows in one folder.
2. A new feature with its own entity kind, process, verb and signs, for example bees and a hive: one new folder, and no file
   outside it changed.
3. The import-layer test passes: no core module imports a package, and packages import only the core and the packages they
   declare.
4. A world with a package off has none of its rows, phases, signs or prompt lines; checked by the manifest page.

## Why

- **Growth.** Hundreds of content items are queued (02zv's ledger, 02zzj's economy research). At the wild layer's rate of 19
  engine files for one feature, each feature raises the cost of the next. A package confines the cost to its folder.
- **The design rules already point here:**
  - D4-24 (the world grows by data on a small set of verbs);
  - D4-34 (one chokepoint with hooks);
  - D4-103 (each process declared once, beside its code);
  - D2-203 (a wild kind's behaviour as a module of its own, acting only through primitives).

  Packages are where those declarations live. The process model says what the economy is; packages say where each part of it is
  kept.
- **Clarity.** "What does farming do?" is answered by one folder and one manifest, not by a grep across 20 files.
- **Null arms.** A package off is the clean null arm of an experiment (scenario_design.md). That holds only if code, signs and
  prompt lines switch off with the rows, which packs do not do today.

## What is weak about this design

- **Indirection.** Registries make control flow harder to follow by reading one function: the night becomes a sorted list, not a
  sequence on the page. The manifest page and the resolved phase order in the journal answer this only in part.
- **Twenty-two folders may be too many.** Some packages (writing, burial) are a few hundred lines. Fewer, larger packages are a
  reasonable alternative (open question 1).
- **The context of signs is the hardest part to split.** Today one context per parcel is computed for six tables. Per-package
  context providers need to be lazy (computed on first read), or the cost of perception rises with every package.
- **Replays across the change.** Iteration order of registries can change the order of events and applies, so the package order
  must be fixed and recorded. Request keys must keep their scheme: the meeting's calls are keyed under the last talk step today. Old
  runs replay under their own code (the journal records the code sha); new code promises only that scripted runs stay identical
  step by step.
- **It does not by itself make content data.** 02zv's C1 to C3 (traits, consolidated verbs, methods as data) do that. This
  proposal is where that content would live; it is not a substitute for it.

## Alternatives considered

1. **Keep the layout; break the cycles only.** That is step 1 alone: hooks and registries, with no folders. It is cheap and gets
   most of the dependency gain, but a feature still edits `signs.py`, `prompt.py` and `data.py`.
2. **Folders by technical role** (`signs/`, `prompt/`, `verbs/`, each split by feature inside). It is closer to today and needs less
   registry, but a feature still spans five folders.
3. **A full entity-component-system.** The plain-JSON state, the primitives and the journal already give what a component-system
   gives for replay. Rewriting to one is a large cost for little gain here.

## Open questions

1. **How fine to cut:** about 22 packages, or about 12 (merging writing into buildings, burial into things, teaching and labour
   into the core, fire and shelter into one)?
2. **Food, shelter and fire:** packages that are on by default, or core? Every world eats and sleeps, but treating them as packages
   keeps the core free of nouns.
3. **`today` kept under each package's name:** a schema change (D4-100 bump). Acceptable?
4. **Order against the wild layer:** step 1 before the wild branch is merged, then the wild layer lands as a package (recommended);
   or merge the wild layer as it is, then move it?
5. **Who builds it:** this is 37.4's code. Step 1 blocks nothing else; its size is a guess until 37.4 looks (perhaps a few
   days).

## Affects

- spec/core/architecture.md (the core and packages);
- spec/core/round.md and spec/record/execution.md (the phase list; the evening step);
- spec/core/world_schema.md (fragments; `today` by package);
- spec/core/processes.md (packs become packages);
- guides/senses.md (sign tables by subject kind; one noticing code path on the road).

## History

- **16 Nov 2026:** proposed. Zach: "do a deeper dive to think about a cleaner way to separate each package into an actual package of
  related features and data etc. the code should be a clear set of primitives to exist with the world, with features mostly being
  labelled data on these primitives ... if each package had everything relevant, what would be all the things it would need to
  register. I like the idea of each being its own folder." Built on a read of every engine module (docs/review/40_feature_packages/).

## Sources

- docs/review/40_feature_packages/inventory_A.md to inventory_E.md;
- spec/core/architecture.md, processes.md;
- proposals/engine_overhaul.md, process_model.md;
- docs/review/37_growth/02zv_wild_consolidation.md (C1 to C5, §4 packs);
- the `ecology` branches (`cybertron2/wild/`, `engine/wild.py`);
- WORK W-43.
