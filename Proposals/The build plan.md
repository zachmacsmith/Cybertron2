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
| **3. Keeping, stores, the book** | `w85-s3-keeping` | u4: processing containers (racks, salting tub, drying), each depth a good, the smokehouse's capacity and fire, hard-cured meat at 0.67 food a kg; u5: stores as spaces and containers, named penalties, vermin and sudden illness; u6: the household and personal book with `when`, chores and fallbacks (own first, [[D2-301 A person's own rules and standing fallback come before every…|D2-301]]), rest, rules changed any time and in the evening ([[D2-319 Rules can be changed at any time by a free act and also in the…|D2-319]]), visibility | a lot becomes the next good after its nights; a store removes only its risks; a rule fires on a state and a missed chore waits; own fallback beats a household chore | as above; the rules block and morning lines render |
| **4. Signs, people, worlds** | `w85-s4-people` | the old core prompt and verb list kept as a world setting for the comparison arm ([[D2-331 Live run 1 has a comparison arm|D2-331]]); u8: the river's record and four leads, signs for anyone ([[D2-325 Some river signs are for anyone|D2-325]]), the carried catch, shallows signs; u9: the core prompt and reply, the eleven shapes ([[D2-314 The eleven act shapes are the verb list|D2-314]]) with crafts under them, learning as one record ([[D2-307 Learning is scaled with the lifespan in every part|D2-307]], [[D2-326 Practice alone can bring a person to known in any craft|D2-326]]), founders' seeded lines with capital inside the budget ([[D2-311 Seeded memory of a household's capital is part of the founders'…|D2-311]]), the evening rules line, the watch act ([[D2-320 Crop protection stays as it is for now|D2-320]]); u11: livelihood rows, holdings, pin and fill, the gate check; Eelmouth remade ([[D2-330 The worlds' defaults as proposed|D2-330]]) | each sign reads state and lands on its intended chance; prompts render at the sizes estimated; every founder's lines fit 20; the gate check passes Eelmouth and fails today's runs world for the reasons u11 gives | as above |
| **Live run 1** | | the remade Eelmouth (water-only), Opus at the poles (the weir keeper, the salter), Sonnet the middle, Haiku the bulk, about 36 to 40 days; its bot null arm; a comparison arm with the old system prompt and no new seeded memories, shorter, through the first autumn run ([[D2-331 Live run 1 has a comparison arm|D2-331]]); a qualitative end-state reading; the catch, keeping, signs, rules and passing-on read together ([[D2-297 The catch stays as calibrated|D2-297]]); each arm published to Hugging Face as soon as it finishes ([[D2-332 Live run 1 (each of its arms) is published to the Hugging Face…|D2-332]]) | | **on Zach's go** |
| **5. Works** | `w85-s5-works` | u7: the hold released in stages (rooms, fittings, the weir first; fences and clearing last); clearing a plot at a time ([[D2-323 A cleared plot becomes a field part of its parcel, sown while the…|D2-323]]); fences along a border in sections ([[D2-322 Fences can be built along one border between two parcels, in sections…|D2-322]]); site material in the work ([[D2-306 Material got at the site of a work|D2-306]]); roofs of turf or brush ([[D2-328 A wattle house's default roof is turf or brush got at the site|D2-328]]); a build act costs what is left ([[D2-324 A build act costs what is left of the work|D2-324]]); Hollinford built without leather. Also from the build gaps audit (build_gaps.md): the wattle smoke hut and the timber and stone smokehouses as things to build (G24), materials carried from another parcel adding moving units (G45), the act log (G46), the dead `PHYSICS.cattle.stray` removed (G47), the straw a world's houses need counted by the gate (G48), one mending act mending as many levels as its work covers (G49). | units at each stage as u7's tables; a plot cleared and sown while the rest is scrub; a border fence section built and seen | as above |
| **5b. The gaps closed** | `w85-s5b-*` (four parts) | everything the build gaps audit (docs/review/37_growth/02zzzh_hunt_fish/build_gaps.md) found designed and unbuilt, except what a decision defers; see "Stage 5b" below | each part's mechanisms by the test rule of its unit; a world other than Eelmouth (Hollinford) passes the gate check run at world build with no silent skip | before live run 2 (Zach, 23 Nov) |
| **Live run 2** | | Hollinford with a newcomer household at 1/15, against its null arm ([[D2-330 The worlds' defaults as proposed|D2-330]] C7), after stage 5b ([[D2-345 Zach's go for stage 5|D2-345]]) | | **go given ([[D2-345 Zach's go for stage 5|D2-345]])** |

## Stage 5b: the gaps closed (Zach, 23 Nov: "a stage 5b that closes all these gaps before the live run")

From the build gaps audit (build_gaps.md, G1 to G79), each gap checked in the code. Four parts, each its own branch and builder,
run after stage 5 merges; parts 1 to 3 touch different files and may run side by side; part 4 last, since it reads the others.

1. **Taking, making and stores** (`w85-s5b-making`): dressing a kill (hide by weight, bone, tallow, antler, pelts; a novice's
   losses) and so bone hooks (G15, from [[L-111 The hunting and resources build, a soon follow-up|L-111]]'s butchering part); snares' good places by edges and tracks, strange ground at half,
   sprung-empty nooses and the cold line (G7); a gill net fouled in a spate (G8); the weir's tend with the water axis (G9); the
   hunt's thin ground against shy game and the weapon's wear (G10); scale words past a dozen (G11); the flax strip's words in the
   field's line and trampling by beasts (G16); older tools as pieces, broken and mended (G17); the withy bed, the retting pit, the
   tiered rack set (G18 to G20); the flax chain end to end (retted flax made); retting's fouling of the water (G79, u10 §3, flax
   only); M5 for every process site and M7 for every material bound (G22); the hot smoke in the open (G25); process nights from
   `clocks.RATES` (G26); the granary on staddles, the sealed pit and the door pile (G30); attending a store (G31); the vermin signs'
   chances checked (G32); herons and otters taking from the shallows (G5); a brook through a land parcel (G6); lending gear by
   agreement and a snare line across parcels (G13).
2. **People** (`w85-s5b-people`): u9 §4's learning: each craft's lessons, failure lines, capability points and aptitude profile;
   attention spent in units; children minded at home (G21, G56; [[Q-81 Knowledge in their own words|Q-81]] and [[Q-82 Trying and learning|Q-82]] rewritten into it); "## You" as u9 §2.6 and §2.7
   (goods by familiarity with their uses, the carry line in kg, one's own things with their tags: G57, G58); the cultural strands
   (G64); a member's proposed household rule shown to the head at the evening, with an act to take or refuse it (G35).
3. **Worlds** (`w85-s5b-worlds`): u11's generator steps 3, 5 and 7 (unpinned households drawn by `village_mix`, the tree carrying
   livelihoods, what spouses and fosterlings carry, neighbours a day away: G65, G68, G69, with [[O-4 Bridge the backward family-tree build into world generation as an…|O-4]]'s bridge); the gate check run at
   world build, a report for every world, P4 and P9 (G70, G71); the founders' skipped ids reported, never silent (G66).
4. **The water's year and the wording** (`w85-s5b-water`): the spring gap closed ([[D2-347 A water-only village should be able to last the year|D2-347]]; [[Q-91 How a water-only village is made able to last the year|Q-91]]: a spring lamprey run, coarse fish
   spawning in the shallows in spring, resident fish and shallows sized to about a quarter of the village at their best); the
   signs design's bug fixes ([[D2-346 The signs design|D2-346]]: the covers' false background lines removed, an attend finding what it names or showing
   nothing); every take's food in true amounts, never "about 1 meal" at the least ([[L-179 Every take's line says 'food worth about 1 meal' at the least|L-179]]); the wording bugs ([[L-178 Wording bugs|L-178]]); the open
   water's "quiet water" and "fish rising" rows on its state and a run (G52).

**Out of 5b, with their records:** what a decision defers (G2, G4, G14, G23, G29, G51, G67: fowling, tanning and leather, the wild's
rates, the brook's water, craftsmanship and the dead hedge); what the design itself sends later (G27 the wind rack, with the coast;
G28 a keeping curve by a lot's age; G33 the clamp, rick and barn; G36 the children's work in the book, after live runs); what has its
own thread or owner (G12 the spear and G15's fur trade with [[L-111 The hunting and resources build, a soon follow-up|L-111]]; G34 wet fuel [[W-76 The timber economy|W-76]], the chest [[L-156 The locked chest and its key|L-156]], vermin with disease [[L-155 Vermin fleshed out properly, with disease and sanitation|L-155]];
G37 the eating rules, 37.4's [[W-37 Standing rules|W-37]]; G50 one skill a trade, [[W-76 The timber economy|W-76]]; G55 floods and gulls, [[W-49 Environment systems|W-49]] and [[W-88 The coast and the sea|W-88]]); what needs design first (G53,
G54: the moon, news from upriver, remembered years, smell's visibility, added to the signs design's questions).

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
