---
id: docs/cybertron2/proposals/w73_design/build_plan.md
kind: proposal
updated: "2026-11-23"
---
# The build plan

*proposal · ready (23 Nov 2026). **Owner:** 37.2 builds every stage, in 37.4's files too (D2 · `docs/cybertron2/proposals/w73_design/build_plan.md`*


**Status:** ready (23 Nov 2026). **Owner:** 37.2 builds every stage, in 37.4's files too ([[D2-313 For this wave|D2-313]]). **Thread:** [[W-85 The wave's integrated design|W-85]]; each stage its own
child thread, named on its branch and commits ([[D2-237 Code changes live under a thread|D2-237]]).

## How it is built

- **Small branches merged to `main` stage by stage**, not one long branch (feature_packages.md §9.1): each stage on a branch
  `w85-s<n>-<name>`, merged when its tests pass, so the other sessions' work on `main` is not left behind.
- **Each unit written as its own feature unit** ([[D2-244 The engine's reworking into feature packages|D2-244]]): its data, acts, signs and processes together, so the later cut into
  packages can move it whole. New code goes in new modules where the spec says (`process.py`, `shapes.py`, `book.py`); edits to the
  old files are kept to the seams the specs name.
- **Each spec's "Decisions since" table binds over its text.** Every file:line a spec cites is checked against the code before the
  change; where the code has moved, the spec's intent is followed and the drift noted in the stage's report.
- **Tests:** unit tests and bot runs for interfaces and basic functioning only ([[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]); the golden journals and prompt snapshots
  re-taken at the end of each stage, with the differences listed; behaviour is read only in the live runs.
- **Records:** each stage starts with `records surface [[W-85 The wave's integrated design|W-85]]` and a row in WORK (CLAUDE.md), and ends with its
  report, its decisions built (`records commit --builds`), and hygiene.

## The stages

| Stage | Branch | Builds | Tests (interfaces) | Done when |
|---|---|---|---|---|
| **1. The basis** | `w85-s1-basis` | u0: goods in handling units and every recipe in kg; fuel a night; the keeping curve's base rates; the capital factor and its conversions (`clocks.py`); the 1-unit floor and batches (`verbs.cost`); the faults first: the options list removed ([[D2-286 The list of what one could do today|D2-286]]), the five fishing bugs ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]), a run's fish learning no wariness, the weir's cost in one place at [[D2-302 The weir's cost for now, to calibrate in live runs, on a lowland river|D2-302]]'s numbers, practice for every build act, the five signs that direct acts reworded | every recipe resolves; no act costs 0; batches as u0 §5; spoil rates as basis §3; no prompt has "Today you could"; one regression test per fixed fault | tests pass; journals re-taken; the runs world still runs with bots |
| **2. Taking and making** | `w85-s2-taking` | u1: the shallows per parcel with their signs, the water-only world, ice states (as designed, to revisit); u2: set and tend on held, tagged, household-owned gear, every taking act's wording, theft of another's set, [[D2-304 An unnamed act on several of one's own things at a place|D2-304]]'s several-of-one's-own; u3: recipes in kg shown by level ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]), two lives and mending, nets at 16 nights ([[D2-329 Until tanning comes back, nets have a middle life of about half a…|D2-329]]), the flax strip, the making gate check; fowling out ([[D2-318 Fowling is postponed from this wave to the hunting build-out|D2-318]]) | set needs gear in hand; tend takes all one's own; a consuming act without a target is refused; a craft line renders at each level; a piece wears and is mended | as above, and a bot fisher sets, tends and remakes gear through a run |
| **3. Keeping, stores, the book** | `w85-s3-keeping` | u4: processing containers (racks, salting tub, drying), each depth a good, the smokehouse's capacity and fire, hard-cured meat at 0.71 food a kg; u5: stores as spaces and containers, named penalties, vermin and sudden illness; u6: the household and personal book with `when`, chores and fallbacks (own first, [[D2-301 A person's own rules and standing fallback come before every…|D2-301]]), rest, rules changed any time and in the evening ([[D2-319 Rules can be changed at any time by a free act and also in the…|D2-319]]), visibility | a lot becomes the next good after its nights; a store removes only its risks; a rule fires on a state and a missed chore waits; own fallback beats a household chore | as above; the rules block and morning lines render |
| **4. Signs, people, worlds** | `w85-s4-people` | the old core prompt and verb list kept as a world setting for the comparison arm ([[D2-331 Live run 1 has a comparison arm|D2-331]]); u8: the river's record and four leads, signs for anyone ([[D2-325 Some river signs are for anyone|D2-325]]), the carried catch, shallows signs; u9: the core prompt and reply, the eleven shapes ([[D2-314 The eleven act shapes are the verb list|D2-314]]) with crafts under them, learning as one record ([[D2-307 Learning is scaled with the lifespan in every part|D2-307]], [[D2-326 Practice alone can bring a person to known in any craft|D2-326]]), founders' seeded lines with capital inside the budget ([[D2-311 Seeded memory of a household's capital is part of the founders'…|D2-311]]), the evening rules line, the watch act ([[D2-320 Crop protection stays as it is for now|D2-320]]); u11: livelihood rows, holdings, pin and fill, the gate check; Eelmouth remade ([[D2-330 The worlds' defaults as proposed|D2-330]]) | each sign reads state and lands on its intended chance; prompts render at the sizes estimated; every founder's lines fit 20; the gate check passes Eelmouth and fails today's runs world for the reasons u11 gives | as above |
| **Live run 1** | | the remade Eelmouth (water-only), Opus at the poles (the weir keeper, the salter), Sonnet the middle, Haiku the bulk, about 36 to 40 days; its bot null arm; a comparison arm with the old system prompt and no new seeded memories, shorter, through the first autumn run ([[D2-331 Live run 1 has a comparison arm|D2-331]]); a qualitative end-state reading; the catch, keeping, signs, rules and passing-on read together ([[D2-297 The catch stays as calibrated|D2-297]]); each arm published to Hugging Face as soon as it finishes ([[D2-332 Live run 1 (each of its arms) is published to the Hugging Face…|D2-332]]) | | **on Zach's go** |
| **5. Works** | `w85-s5-works` | u7: the hold released in stages (rooms, fittings, the weir first; fences and clearing last); clearing a plot at a time ([[D2-323 A cleared plot becomes a field part of its parcel, sown while the…|D2-323]]); fences along a border in sections ([[D2-322 Fences can be built along one border between two parcels, in sections…|D2-322]]); site material in the work ([[D2-306 Material got at the site of a work|D2-306]]); roofs of turf or brush ([[D2-328 A wattle house's default roof is turf or brush got at the site|D2-328]]); a build act costs what is left ([[D2-324 A build act costs what is left of the work|D2-324]]); Hollinford built without leather | units at each stage as u7's tables; a plot cleared and sown while the rest is scrub; a border fence section built and seen | as above |
| **Live run 2** | | Hollinford with a newcomer household at 1/15, against its null arm ([[D2-330 The worlds' defaults as proposed|D2-330]] C7) | | **on Zach's go** |

## Not in this build

Fowling; tanning, leather, lime and barking; shoes; builders' craftsmanship; the dead hedge; daily herding and timed acts; ice
fishing; strength; poles as a good (basis.md "Not in this wave"). Each is a deferred item tagged to the thread it returns with.

## What could go wrong

- **Stage 1 touches everything.** The goods' resize changes every recipe and ration; the keeping curve changes how long every food
  lasts. Old worlds will behave differently; the journals' differences are listed, not hidden. A world spec flag keeps the old
  basis only if Zach asks for it.
- **The specs are drafts at line level.** About 100,000 words, written by five agents and integrated by reading; the build will find
  places where a cited line has moved or a field is named two ways. Each is fixed to the basis sheet and noted.
- **The prompt changes at once** (stage 4: the core, the shapes, the seeded lines). Live run 1 reads all of it together, as Zach
  asked; a single bad line will be hard to isolate. The told-knowledge comparison arm ([[D2-266 Knowledge in their own words|D2-266]]) is the check if needed.
