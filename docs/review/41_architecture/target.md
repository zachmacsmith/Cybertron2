# The target architecture: one registry form, three layers, and a lifecycle for mechanisms (W-112, draft 1)

Session arch, 24 Nov 2026. For Zach's approval; nothing here is decided and no engine code is changed until he approves it. It
answers step 2 of [architecture_overhaul.md](../../cybertron2/proposals/architecture_overhaul.md) (the target architecture),
reconciling the patterns survey (W-110: [A](../37_growth/02zzzm_patterns/A_physics.md), [B](../37_growth/02zzzm_patterns/B_making.md),
[C](../37_growth/02zzzm_patterns/C_people.md), [D](../37_growth/02zzzm_patterns/D_senses.md)) with
[feature_packages.md](../../cybertron2/proposals/feature_packages.md) and [engine_overhaul.md](../../cybertron2/proposals/engine_overhaul.md)
(D4-103). Steps 3 (the map of every mechanism to its home) and 4 (the migration, with estimates) follow once the shape is agreed.
Code read on `main` at 82f8b92c; line numbers are there.

Zach's framing (24 Nov): design, not build; "a data-central way that is more extensible but simultaneously fluid"; new things
"built and isolated in their new features", working "through existing shared primitives, or introduce some new basic mechanism or
specifics if necessary, that may later be generalised into core primitives".

## Summary

- **What the code shows.** The engine already has one shape that works, in five places: a registry of named behaviours, written as
  code, which rows choose by name and give parameters to, reading a declared context and returning a declared result (the
  primitives, the renewal rules, packs, the process rows, the act table). Most of the breakage comes from four other shapes. The
  first is a hub that switches on a row field (`verbs._technique`, 22 `elif` branches on the yield kind). The second is a special
  case by name inside a general path (`tech == "fell"`). The third is a feature that registers by editing another module's tables
  at import. The fourth is a long procedure, ordered by hand, that names every feature (`night()`, `World.__init__`).
- **The target.** One registry form, used at every place the engine is meant to be extended, and checked when it loads. Three
  layers of code: the **core** (state, the chokepoint, time and phases, registries, the noticing rule, the frame of the prompt, the
  journal); **shared mechanisms**, each owning one registry; and **features**, each a folder of rows and the specific code it
  registers. One rule for code: no branch compares a row's name to a literal. Rows may link to other rows by name, and the load
  check verifies every link.
- **The lifecycle.** A new feature uses an existing registry if one fits. If none fits, it may bring its own mechanism, kept inside
  its folder with its own small registry. When a second feature needs the same shape, that mechanism is **promoted** to the shared
  layer. A list of local mechanisms keeps the candidates for promotion in view. So the general set does not have to be predicted in
  advance; it grows from what features prove they need. That is the answer to "general architectures that break": the past plans
  fixed the general set first, and content that did not fit was built around it, with nothing to mark or contain the work-around.
- **What changes from the earlier plans.** feature_packages.md's principles P1 to P8, its six categories, its manifests and its
  `requires` and `unless` all stay. What changes is the order and one added layer. The registry form and its load check come first,
  over the existing tables, with no code moved. The hubs become registries next. Folders move only when a feature is touched (the
  strangler path). The surveys' 25 or so "missing patterns" become candidates for promotion, ordered by how many copies exist today
  and what content needs next. They are not a list to build up front.
- **Honest limits.** This fixes only half of what went wrong. Survey A §7.3 and D §8 split the ad hoc code into two groups: what
  went ad hoc because the primitives could not be extended, and what went ad hoc though they could have been (built in a day
  against one world, with no check). The second group needs the guards and the review rules (proposal step 5), not a new shape. The
  engine also grew from 24,941 lines (6190b4d, 16 Nov) to 36,293 (today): feature_packages.md's estimates were made on 20,400 and
  are out of date.

## 1. How the engine actually works today

### 1.1 The shape that works (keep and generalise)

| Where | What it is | Code |
|---|---|---|
| **The chokepoint** | every change is a named primitive applied through `World.apply`: a place check, before-hooks that may refuse, the change, after-hooks, the journal | `world.py:461-481`; the table `world.py:1109-1147` |
| **Renewal rules** | a rule is a function registered by name (`@rule("fast")`); a stock's row or its own record names its rule; the night and the capacity model call the same function | `renewal.py:23-33`, `:162-169` |
| **Packs** | a row's `pack` is `requires`, its `off_with` is `unless`; a world with a pack off has none of its rows | `packs.py:40-52` |
| **Process rows** | a way of keeping is a row (input, waiting good, output, nights, fuel, condition, fittings); one module runs them all | `process.py:39-56` |
| **The act table** | 38 acts in `VERB`, with arguments, cost and description; the old prompt rendered from it (the rebuild on `w109-interface` restores that, with a load check raising `RegistryError`, D §9) | `verbs.py:20-105` |

They share a form: **a registry of named kinds of behaviour (code), rows that choose one by name and carry its parameters, a
declared context the behaviour reads, a declared result it returns.** Where the engine has kept to this form, the surveys grade it
"general over rows" (A's renewal and food web, B's processes and stores, D's noticing rule).

### 1.2 The shapes that break (what the target removes)

| Shape | Example | Why it breaks |
|---|---|---|
| **A hub switching on a row field** | `verbs._technique` (`verbs.py:687-910`): 22 `elif y["kind"] == ...` branches, each calling into a feature module | every new kind of act edits the hub; an unknown kind matches no branch and the act reports a yield of nothing, silently (`verbs.py:860-862`) |
| **A special case by name inside a general path** | `if dk == "willow"` (`verbs.py:776`), `if tech == "fell"` (`:779`) in the `fixed` yield; `b["structure"] == "camp"` four times in the night's fires (`night.py:55-67`) | the general path now carries one feature's rule; the next feature copies the pattern |
| **Registering by editing another's table at import** | `process.register_fittings` overwrites fields on `data.FITTINGS` rows (`process.py:141-148`); `data.py:129-134`, `:1303-1313` import feature modules to let them add rows; `PRIMITIVES.update(...)` after the table (`world.py:1148-1157`) | order of imports decides the result; nothing says which module owns which field; no check that a row is whole |
| **A procedure ordered by hand, naming every feature** | `night()` (`night.py:20-`: fights, departures, sleeping, shelter levels, fires by fitting name, processes, care, meals); `World.__init__`'s seeders (`world.py:255-278`: agreements, knowledge, things, buildings, the book, waters, wild, shallows, willow) | a feature is added by inserting lines in the right place; the order is implicit; the null arm of an experiment is not clean |

And beside them, the **signs**: rows with a `when` and a `text` lambda over a context (good, and fluid), but read by one walker
naming each subject (`signs.py:1221-1300`), identified by position (`f"{about[0]}#{names[id(rows)]}{i}"`, `:1239`), and dropped
without a word when a condition raises (`:1235`). Because a sign has no stable name, the household book matches words in the text
instead (C §1: "few fish rising" satisfies a rule on "the river rising").

## 2. The registry form (the shared core's one idea)

Every place the engine is meant to be extended is a **registry**: the act's yield kinds, renewal rules, sign subjects, conditions,
referent kinds for the resolver, phases of the day, seed steps, record term kinds, and so on. A registry declares:

| Field | Meaning |
|---|---|
| `name`, `owner` | the registry, and the layer or package that owns it |
| `schema` | the fields a row must and may carry: type, unit, clock, and **links** (a field naming a row of another registry); a package may add optional fields to another's rows through its own schema fragment (feature_packages §2.1) |
| `behaviours` | the named functions a row may choose (`renewal: "fast"`), each declaring the **context** it reads (namespaced: `x.water.flow`) and the **result** it returns (`{S, K}`, `{got, word, data}`) |
| `requires`, `unless` | on every row and behaviour (feature_packages §4.4; today's `pack` and `off_with`) |
| `check` | the load check: required fields present, types right, links resolve, behaviours exist, names unique, aliases unique; it **fails the world build** with the row and field named |

What a row may hold: **properties** (quantities, rates with clocks, words), **links** to other rows by name, and **a choice of a
named behaviour with its parameters**. Code may read any of these. Code may not compare a row's own name to a literal (`== "camp"`,
`in ("hearth", "fire ring")`). That is the rule D2-353 states, made checkable: the named-branch guard lists today's sites and may
only shrink.

**Fluid, not rigid.** A behaviour is ordinary Python code. Rows do not become a small language. The registry adds three things: a
name for the behaviour, a declared context, and a check. A new feature that needs a new behaviour registers one, in its own
folder, in a few lines. The rigid end that D2-354 warns against would be making every behaviour a row interpreted by a generic
engine. The target does not do that.

**One open choice, conditions (question 2 below).** Sign rows today hold lambdas (`when`, `text`). They are fluid, and nothing
else can read them: the book can only match their words, and the load check can only see that they are callable. Recommended
split:
- a condition that another system reads (the book reads signs; the founders' lines read the world; pulses, landmark trouble and
  the evening read state) is written in the **one condition grammar**: `and`, `or`, `not` over registered predicates with
  arguments, each predicate a behaviour declaring what it reads (C §7: the book's B7 and B8 are its first half);
- a condition read only by its own package's rows may stay a lambda over that package's own context namespace, named and flagged.

## 3. Three layers

| Layer | Holds | May import | Today, roughly |
|---|---|---|---|
| **Core** | the state (`World.s`) and its schema from fragments; the chokepoint and its primitives; hooks; time, the calendar and keyed draws; the **phase list**; the **registry form** and its load check; the **resolver** (referent kinds with aliases on rows); the **condition grammar**; the **noticing rule**; the prompt's frame and slots; the journal, branching and replay | nothing above it | `world.py`'s core half, `journal.py`, `branch.py`, `perceive.py`'s rule, `prompt.py`'s frame |
| **Shared mechanisms** | general behaviour used by more than one feature, each owning a registry with named extension points: stocks and renewal; takes from a population; works; lives and wear; processes (a thing becoming another under conditions); keeping by risk and remedy; draws from ordered sources; records with terms; matched intentions; familiarity; signs (subject rows, act bundles, the observer gate); the mind's dated records | the core, and other mechanisms it declares | `renewal.py`, `process.py`, `stores.py`, `gear.py`'s lives, `agreements.py`, the noticing step; most of the rest is still spread inside features |
| **Features** | one folder each: rows for the registries above; the specific code it registers (its yield kinds, renewal rules, sign context namespace, walker, phases, seed steps); its own **local mechanisms** where nothing shared fits; its tests | the core, the mechanisms, and features it declares as `requires` | water, wild, farming, herds, buildings, the book, the founders, roads, life, teaching, ... |

feature_packages.md's six categories (space, layer, body, population, record, mind; plus happenings and types) hold up against the
surveys. The surveys' misfits are mostly missing **mechanisms**, not missing categories:

| Survey misfit | Its home in the target |
|---|---|
| works (B: 9 copies) | a record kind with terms `{target, units_left, effect}`, run by the works mechanism |
| bodies with parts (B) | the body base shape gains `parts` (rows of a parts registry); capacity, cost and wear derive from them |
| places that group places (A §4.7) | a space kind whose record lists its members (a water body, a wild area, a stretch) |
| habitat, couplings (A) | fields of the population's species row (`habitat`, `effects`), read by the stocks mechanism |
| driven layers and conditions from their memory (A §4.5) | layers (core category) whose derived conditions are registered predicates of the condition grammar |
| type transitions (A §4.6) | the processes mechanism widened: a thing of one kind becomes another under conditions, for lots, parcels, ice, sites |
| records with terms, matching, familiarity (C) | mechanisms over the record, happening and mind categories |
| the observer, the mind record, subjects and walkers, the reply schema (D) | the signs mechanism and the core's resolver and prompt slots |
| movement along a network (A §4.4) | legitimately owned by its systems for now (the runs, the ranging packs, storms): three different dynamics, one copy each; promoted if a fourth looks alike |

## 4. The lifecycle of a mechanism

This is the part that makes the architecture fluid. It replaces "decide the general set first".

1. **Use what exists.** A new feature first looks for a registry that takes it: a new yield kind, a renewal rule, a process row, a
   sign subject. It adds rows and, where needed, a behaviour registered from its own folder. No shared module is edited.
2. **Bring your own, locally.** If no registry fits, the feature may build its own mechanism **inside its folder**, in the
   registry form, with its own small registry. It may not branch inside a shared module or inside another feature to get it. The
   mechanism is entered in a **list of local mechanisms** (name, feature, what it does, the shared mechanism it resembles if any),
   kept beside the guard.
3. **Promote at the second user.** When a second feature needs the same shape, the mechanism is promoted to the shared layer:
   its registry moves, both features register into it, and the first feature's copy goes. Promotion is its own small piece of work
   with its own record, done before the second feature is built, not after.
4. **Promote to the core** only what every world needs (a referent kind for the resolver, a condition predicate everyone reads).

Why "the second user" and not the textbook third: here a copy spreads within a day (the wave built four stages in one day, A §7.4),
so waiting for a third copy means cleaning up two.

What this changes in practice:
- A brief says, for each new behaviour, which of the three it is: an existing registry, a local mechanism, or a promotion.
- A review checks that a local mechanism touches no shared file, and that no second copy of a listed local mechanism is being
  built.
- The surveys' list of missing patterns becomes the first promotion queue. Every entry already has two or more copies today, so by
  the rule each is a promotion that is due. They are not all built at once. They are ordered by which content waits on them (§5).
  Said plainly, since it can read as a contradiction: **for the code that exists, the lifecycle does not reduce the work; it reduces to
  a priority queue** of overdue promotions. Its real effect is on what is built from here on: no general mechanism is designed
  before a feature needs it, and a feature that needs one it does not find builds it locally, inside its folder, not as a branch in a
  hub.

## 5. The shared mechanisms: which first

All of these have two or more copies today (the surveys' counts). The order is by what the frozen content needs next (stage 5's
works, W-106; stage 5b, W-107; the interface, W-109), and by risk to calibrated behaviour.

| Mechanism | Copies today | Its registry and extension points | Content waiting on it | Risk |
|---|---|---|---|---|
| **Act effects** (yield kinds) | 1 hub, 22 branches, 21 kinds | yield kind: `apply(here, mind, tech, site, a) -> {got, word, data}`, `ready`, `site`, its practice rule | every new act; the capacity model reading every kind | low: byte-identical journals |
| **Resolver** | 12 (B) + 9 (C) + 5 (D), overlapping | referent kinds (person, building, parcel, good, craft, set, act face, option) with `aliases` on rows | W-109's parse; World 0b's refusals (L-189) | medium: parses agents' text; live replies as a fixture |
| **Conditions** | 4+ (book, pulses, landmarks, founders, signs' `if`) | predicates, each declaring what it reads and its words | the book's "seen" rules; the founders' lines; 5b's runs on conditions | medium |
| **Sign names and subjects** | 5 row formats, ~20 walkers | subject kind: walker, context namespace, tables; rows named, `rank`, `replaces`; act bundles on the act or craft row | W-103's signs design; the book reading signs by name | high for the stimulus: needs prompt snapshots and the keyed-draw decision |
| **Works** | 9 | work kind: target, units, who may join, effect at the end, in-flight state | stage 5 (u7, works in sections, site material, D2-357) | medium: schema change, in-flight works migrated |
| **Lives and wear** | 9 | wear kind: clock (uses, nights, seasons), what wears it, mending inputs | the oven, millstones, weir, house and fence mended by one act | medium to high: weir wear (D2-210) and shelter levels are calibrated |
| **Keeping by risk and remedy** | 7 loss rules | risk rows (damp, flies, frost, vermin, fire); a place's remedies | 5b part 1 (taking, making and stores) | low to medium |
| **Draws from ordered sources** | 6 loops | a need, an order of containers, holds, the shortfall | the meal order (D2-339), fuel, inputs | medium |
| **Stocks: habitat and couplings** | 9 seeders, 6 coupling readers | species row `habitat`, `effects`; the renewal rule returns changed fields and declares its context (A §8) | W-108's general waters (resident fish from the generator) | medium to high: calibrated takes |
| **Records with terms, matching, familiarity, the mind record** | 5, 7, 3, 7 | term kinds with settle hooks; match rules; curve classes and ways in; one writer and renderer of dated records | people's systems; less urgent for the experiments | medium; the old learning path stays for replay |

## 6. What a system owns (D2-354)

Taken from the four surveys' verdicts, and consistent across them:

| System | Owns, inside its folder | Meets the rest only through |
|---|---|---|
| The wild food web | its eating, condition and breeding; its kinds' and foods' specifics as row fields | draw out and return; coupling rows; its sign subject |
| The runs | movement on the river network, the cue | the take mechanism; `share_run`; condition predicates it registers (`spate`) |
| The climate | a driven layer with its own tables | condition predicates; never its internals |
| The generator | its catalogue, terrain to ecosystem to cover, by name (legitimately) | writing rows' values the engine reads; never parallel numbers |
| The founders' lines | their prose (D2-268) | template rows with declared conditions and fills; numbers from rows |
| The bots, memory, the journal | their own policies and infrastructure | reading rows and signs' thresholds; never copying a constant |
| Buildings, farming, life | tiers and rooms, holdings and shares, stages | properties on their rows; known-line rows; their context namespaces |

## 7. What this does not fix, and what does

- **Speed and one test world** (A §7.4, B §7, C §6). Four stages built in one day against Eelmouth. A branch on a name passes every
  test on one world. The fixes are process: the named-branch guard (a list that only shrinks), the load check failing the world
  build, a world-variety test (every feature run on at least one generated world besides its own), and a "built generally?"
  column in every audit (B §7). Proposal step 5 writes these into `how_we_work.md` on Zach's word.
- **Replay.** Old paths are kept alive for replay with no rule for when they may go (C §6). A replay policy is needed, or every
  promotion leaves its old copy behind (question 3).
- **Experiments.** Every change to a rendered line changes the stimulus (D §10). The migration runs after W-111's tag, never under
  a running experiment.
- **Visibility: a diagnostics stream** (Zach, 24 Nov: "there is no unified error logging or logging stream at all"). True: the
  journal (`journal.py:21-36`) records steps, requests, events and state changes, but nothing about the engine itself; the code has
  21 broad `except` sites in `engine/` and `wild/`, and only `infra/llm.py` logs. Every regression this week was found by hand
  (wave_regressions.md, build_gaps.md, World 0b's refusals, L-189). Proposed: one journal table, `diagnostics`, written by one call
  (`w.note(kind, where, detail)`), with a small fixed vocabulary: `load_error`, `skip` (a row or step dropped), `fallback` (a default
  used), `refused` (an act refused, with a reason code). Constraints so it is safe for experiments: written to the journal only, never
  to `World.s` or a checkpoint (replay's checkpoint comparison is untouched); no randomness and never shown in a prompt; left out of
  golden-journal comparisons; old journals load without it. It is the same change as two others in this target: the load check
  writes its failures there, and structured act results (`{kind, text, data}`) give each refusal its code, so refusals counted by
  code would have found L-189's faults with a query. "No silent failure" is already W-111's scope (stable_engine_for_runs.md), so
  the stream belongs there, before the tag; W-112's load check writes into it. Posted on the board; not built.

## 8. The first build (outline; step 4 gives it in full)

In small merges to `main`, after W-111's tag, each checked against golden journals and prompt snapshots (feature_packages §8):

1. **The registry form and its load check** over the existing tables (`ITEMS`, `TECHNIQUES`, `FITTINGS`, `COVERS`, `RESOURCES`,
   `PROCESSES`, the wild kinds, `VERB`), with every side table keyed by names declared as a field of its rows' schema. No behaviour
   change; it will find errors at once (B: `"oats"` in `KIND_GOODS` is no item).
2. **The named-branch guard** (reporting first, then failing on growth) and the list of local mechanisms.
3. **Registrations replace import-time edits**: `register_*` into declared fields; the primitives table assembled from
   registrations.
4. **The hubs become registries**: yield kinds; seed steps; the night as phases (feature_packages §6); sign subjects and walkers.
5. **Promotions in the order of §5**, each with its content: works before stage 5 resumes; conditions and sign names before the
   book's fixes; keeping and draws with 5b.
6. **Folders move when a feature is next touched** (feature_packages §9's strangler path), not as a phase of their own.

## 11. A feature's folder (exploration, from Zach's question, 24 Nov)

Zach: "what [does] the structure of [a] feature folder look like? Would it be good to make them all require things [written] up in
a certain way, like they have any registered data and then X folder with private mechanisms etc?"

Yes: a fixed layout of **known names, each optional**. The loader reads a package only from these names, so where a thing lives
says what it is. A package without local mechanisms simply has no `local/`.

```
cybertron2/packages/water/
  __init__.py      the manifest: name, requires, optional, standard; its summary and the decisions it builds (§12)
  schema.py        fields it adds to other registries' rows (`in_water` on gear), and the schemas of registries it owns
  rows/            its data, one file per registry it adds to: items.py, techniques.py, gear.py, covers.py, signs.py, lines.py
  behaviours/      what it registers into shared registries: yields.py, renewal.py, phases.py, seed.py, context.py (its sign
                   namespace and walker), conditions.py (predicates it adds: `spate`, `iced`)
  local/           its private mechanisms, each one module in the registry form, each declared in the manifest as local, with
                   what it does and which shared mechanism it resembles; no other package may import from here
  with_wild.py     registrations that need another package too (`requires: [water, wild]`)
  tests/           its tests and fixtures
```

Three rules make it hold:
1. **A package imports only the core, the shared mechanisms, and the packages it declares.** A test enforces it (feature_packages P1).
2. **Nothing outside a package imports its `local/`.** A second package that wants a local mechanism fails that test. That
   failure is the promotion signal (§4), made mechanical.
3. **Rows never hold code beyond a behaviour's name and parameters**, except a package's own sign and line conditions where Q-103
   allows lambdas.

The shared mechanisms have the same layout under `cybertron2/mechanisms/<name>/`, without `with_*`. The core has its own folders
(feature_packages §3).

## 12. Documentation as data (exploration, from Zach's idea, 24 Nov)

Zach: "working in the documentation into part of the data as requirements ... a thing's type can also declare certain types of
required documentation to accompany [it]. This means we [can] do the whole wiki generated from the current code because any private
mechanism or thing etc has the required descriptions, and these must match how things actually work, and this also bridges the
translation of spec / proposal into code ... completion audits could compare all of this."

It extends a rule he has already decided for acts. D2-350: every act and technique has required descriptions, and "an act or
technique without them is a build error". The registry form (§2) is the place for it: each registry's schema names its required
documentation fields, and the load check enforces them.

**How it would work.** A page has two parts. The first is **generated from what the engine uses**, so it cannot drift. The second
is **written**, kept short, and required:

| On every... | Generated (true by construction) | Written (required) |
|---|---|---|
| registry | its schema, behaviours, and the rows in it; who owns it | `doc`: what it is for, in a few lines |
| row | its fields, its links both ways (what it names; what names it), `requires`/`unless`, its package | `doc` for kinds whose rows are not self-explaining (a process, a set method, a work kind); none for a plain good |
| behaviour (shared or local) | the context it declares it reads (enforced: reading outside it fails the declaration test, feature_packages §5), the result it returns, which rows choose it, its phase and order | `doc`: what it does and the rule it follows (a formula, a threshold) |
| package | its registrations by registry, its local mechanisms, lines of code beside rows of data (P8) | `summary` |
| all of them | `decided: [D2-210, ...]`: the decisions it builds | |

**The bridge to the spec.** `decided` gives a trace in both directions, which `records.py` can check:
- **a live decision that nothing cites** is unbuilt, or built and not marked;
- **a registration that cites nothing** was built without a decision (the retrospective-proposal rule, README 3a);
- **a citation of a replaced decision** is stale code, or a stale citation.

That is the completion audit that build_gaps.md did by hand ("designed against built"), as a query.

**The wiki.** A generator walks the registries after load (with every package on) and writes one page per registry, row kind,
behaviour and package, with the links. It writes into the Obsidian vault (D2-240), beside the spec and the records, so a page about
the weir links to D2-210's spec text and back.

**What could go wrong:**
- **Written text drifts.** The prose can be wrong, and no check can read prose against code. Mitigations:
  - keep the written part small, and make the generated part carry the facts: what a behaviour reads and changes, its parameters
    with their units and clocks;
  - review each `doc` with its code (step 5's checklist);
  - let the generated "reads, writes, chosen by" sit next to the prose on every page, so a reader sees a mismatch.
- **Boilerplate.** Required fields filled with "This does X". Required prose is limited to kinds that need it (above), never on
  every row.
- **Stimulus leak.** D2-350's descriptions are shown to agents. Engineers' documentation must be a **separate field**. Otherwise
  engine terms reach the prompt, or editing a doc changes the experiment. Proposed: `does` and `args` are agent-facing, in the
  world's words; `doc` is engineer-facing, never rendered into a prompt (a test checks no `doc` text appears in prompt snapshots).
- **Backfill cost.** 96 items, 161 techniques, 40 acts, 536 sign rows, plus every behaviour. The generated half costs nothing. The
  written half is required for new registrations at once, and reported (not failed) for old ones until each is next touched.
- **False completeness.** A cited decision proves intent, not behaviour. Behaviour is still proven by tests and golden journals.
  The trace shows where to look, not that it is right.

**Assessment.** A good idea, and cheap once the registry form exists: most of a page is the registry's own data. Its strongest
part is the `decided` trace, which turns the spec-to-code audit into a query. Its weakest is the prose, and it is safe only if the
written part stays small and separate from agent-facing text. It belongs in phase 1 of the migration (the registry form and its
load check), at about 1 to 2 more builder-days for the generator and the trace check.

## 9. Open questions for Zach

1. **The shape.** Is the target right: one registry form, three layers, the lifecycle with promotion at the second user, folders
   moved when touched? *Recommend: yes.* If not, say which part feels wrong.
2. **Conditions.** Should a condition another system reads be written in the one grammar, with lambdas kept only for a package's
   own rows (§2)? *Recommend: yes.* The alternative is lambdas everywhere: more fluid, but nothing can read them and the load check
   cannot see inside them.
3. **Replay.** When a mechanism is promoted, may old runs stop replaying under the new code, provided each such run is recorded with
   the last commit that replays it? *Recommend: yes, with that record.* The alternative keeps every old path alive.
4. **Content against the core.** Should new content wait only for the promotion it needs (works before stage 5), or for all of
   steps 1 to 4 in §8? *Recommend: only for the promotion it needs, plus steps 1 and 2 first,* since they are cheap and stop the
   growth.
5. **How strict D2-354 is.** Is §6's table of what systems own right? In particular: does the generator keep its catalogue by
   name, and do the founders keep hand prose?

## 10. What this draft rests on, and what is not yet checked

- Read in the code: the chokepoint and primitives, `World.__init__`'s seeders, `verbs._technique`, the sign walker and row format,
  the night's opening, `process.py`'s rows and registration, `packs.py`, `renewal.py`, `data.py`'s tables and imports.
- Taken from the surveys and not re-checked here: their counts of mechanisms, branches and copies. Their method is stated in each
  (AST walks with stated under- and over-counts). Survey A notes the counts were read through by hand per file.
- Not yet done: the map of every mechanism to its home (proposal step 3); estimates against today's 36,293 lines (step 4);
  the interface rebuild's registry (`w109-interface`, not on `origin`), which is the nearest model of the registry form and
  should be read before step 1 is briefed.

*Current as of 24 Nov 2026 (82f8b92c).*
