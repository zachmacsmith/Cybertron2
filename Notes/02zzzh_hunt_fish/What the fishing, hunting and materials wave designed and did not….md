---
id: docs/review/37_growth/02zzzh_hunt_fish/build_gaps.md
kind: note
updated: "2026-11-23"
---
# What the fishing, hunting and materials wave designed and did not build (W-73)

*note · `docs/review/37_growth/02zzzh_hunt_fish/build_gaps.md`*

> **Counts** (79 items, numbered G1 to G79 in the tables): 74 design gaps, of which **partly 11, later 16, nowhere 40, decided 7**; and 5 items from the runs and records (§13). Of the 79, **47 are untracked** (listed at the end with a proposed record each). While this audit was written, stage 5 and li


23 Nov 2026, 37.2 (audit subagent). Zach (23 Nov): what in the wave was designed but not built, dropped, or fell through the
cracks? Read: the design set `docs/cybertron2/proposals/w73_design/` (README, basis, u0 to u11, integration, build_plan,
questions), each under its "Decisions since" table; the stage 1 to 4 reports, `fix_shapes_report.md` ([[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]),
`after_run1_report.md` ([[W-104 Build the after-runs list from live run 1|W-104]]), `live1_report.md`; the code on `main` at 32b8c942; the open records in `docs/cybertron2/items/`
(state open, active, benched, waiting, paused, queued, discussion). Every status below is from the code (file:line) or a record,
not from a report's summary. Line numbers are on `cybertron2/` at 32b8c942.

Classes: **partly** (built partly: what is missing said); **later** (not built, planned in a build stage or in an open record that
names it); **nowhere** (not built, planned nowhere: at most a line in a report's "Not done" or a spec's own "Gaps"); **decided**
(deferred by a decision, cited). "Untracked" means no open record holds it; an item only in a closed thread's report counts as
untracked, and so does a stage that exists only in `build_plan.md` (stage 5 and live run 2 have no thread).

## Summary

**Counts** (79 items, numbered G1 to G79 in the tables): 74 design gaps, of which **partly 11, later 16, nowhere 40, decided 7**;
and 5 items from the runs and records (§13). Of the 79, **47 are untracked** (listed at the end with a proposed record each). While this audit
was written, stage 5 and live run 2 got their thread ([[W-106 Stage 5 of the wave, works|W-106]], after [[D2-345 Zach's go for stage 5|D2-345]]), [[O-4 Bridge the backward family-tree build into world generation as an…|O-4]] offered the backward tree into generation, and [[Q-89 Whether a water-only village should last the year, or the spring gap…|Q-89]]
(the spring gap) was opened and answered ([[D2-347 A water-only village should be able to last the year|D2-347]]); the tracking below counts them. [[W-106 Stage 5 of the wave, works|W-106]]'s `next` is to fold this audit's gaps into
its brief: G24, G45 to G49 are stage 5's own and not yet named on it. Stages 1 to 4 built the core of every unit they covered (u0 to u6, u8, u9's core,
shapes and learning record, u11's pinned fill, gate check and Eelmouth); what is missing is mostly what Eelmouth did not need.

**What matters most for running any world other than Eelmouth:**

1. **Generated worlds get no livelihoods and no seeded lines.** `livelihoods.fill` takes pinned households only and skips the rest
   ("not pinned (the generator's draw by village_mix is landgen's, step 3)", `engine/livelihoods.py:213-216`); `engine/generate.py`
   and `landgen/write.py:28-29` (`FARMING`, `TRADES`) are unchanged, and `fill` is called only by the Eelmouth makers
   (`specs/make_eelmouth.py:86`). u11's generator step 3 (G68) is untracked; steps 5 and 7 (G69) only in part by [[O-4 Bridge the backward family-tree build into world generation as an…|O-4]] (bridging the backward tree into
   generation, which keeps `fill` as is). Any world but a hand-pinned one runs
   on the old generation.
2. **The silent skip will recur after [[W-105 The founders' seeded lines for every built livelihood|W-105]].** Beyond the livelihood sets [[W-105 The founders' seeded lines for every built livelihood|W-105]] is building: HH2 (seed held back, every household
   with fields), HH4 (containers and vermin; its condition "U5 built" is now true) and PE3 (elders) are wanted but have no template
   (`engine/founders.py:572`, `:576`; G60 to G62), and `wanted` gives keeper lines only to a weir's, a smokehouse's or a brine
   pan's keeper (`founders.py:587-596`), so MI3, SM4, FA7 and the rest will not reach a mill's or a forge's keeper even once
   written (noted for [[W-105 The founders' seeded lines for every built livelihood|W-105]], G63). The check that would report it, **P4** ("a template whose condition is false here: report the
   skipped"), is not in `landgen/gate_check.py` (P ids present: 1 to 3, 5 to 8, 10 to 21), nor **P9** (capital within a day); and
   the gate check is not run at world build at all, only by the maker scripts (`make_eelmouth.py:113`, `make_eelmouth_small.py:53`)
   (G70, G71).
3. **Stage 5 (works) is unbuilt; its thread ([[W-106 Stage 5 of the wave, works|W-106]]) opened only while this was written.** Every existing work is still held at today's units
   (`engine/data.py:878`; `clocks.capital_units` is called nowhere outside `clocks.py`); fences only go round a whole parcel at the
   old √size cost (`engine/farm.py:867-871`, `data.py:1103-1110`); clearing is whole-parcel (`verbs.py:2806-2825`); [[D2-306 Material got at the site of a work|D2-306]]'s site
   material and [[D2-328 A wattle house's default roof is turf or brush got at the site|D2-328]]'s turf roof are only two data rows. A farm world (Hollinford, [[D2-330 The worlds' defaults as proposed|D2-330]] C4 and C7) depends on all of it, and
   Hollinford itself is not built (G38 to G49, G72, G73). [[W-106 Stage 5 of the wave, works|W-106]] names the hold, clearing, border fences, site material, roofs,
   Hollinford and live run 2; it does not yet name the smoke hut and smokehouses (G24), materials carried to the site (G45), the act
   log and `stray` (G46, G47), the straw check (G48) or mending several levels (G49). [[W-73 Fishing, hunting and their materials developed together|W-73]]'s own `next` still reads "Zach: the
   morning brief's 23 questions"; [[W-85 The wave's integrated design|W-85]]'s ends at live run 1.
4. **A member's proposed household rule goes nowhere.** `book._propose` stores it and tells the member "It stands once {head}
   takes it" (`engine/book.py:1127-1131`), but nothing shows `proposals` to the head and no act takes one (G35). Any world with
   households of more than a head.
5. **Things a farm, wood or hunting world will reach for and cannot make:** the withy bed (the basket maker's capital,
   `livelihoods.py:106`; no row anywhere, G18); a smoke hut or a new smokehouse (no hut room or smokehouse blueprint in `ROOMS`,
   `data.py:363-372`, though `process.py:625-629` reads a "hut" room; G24); dressing a kill (no bone, so no bone hooks, and lines
   need a smith's copper hooks; G15).
6. **Retting's fouling** is the one part of u10 kept in this wave (u10's header; README units table), and is built nowhere and
   tracked nowhere as a wave item (G79).
7. **Untracked learning:** lessons, failure lines, attention spent in units, children minded at home, capability points and
   aptitudes (u9 §4.5 to §4.8) are built nowhere; the only open record near them is [[Q-82 Trying and learning|Q-82]], an ask on the older proposal (G56, G21).

Record hygiene found on the way (§13): [[O-2 Make the eleven bulk processes take up to their batch|O-2]], [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]], [[Q-74 Whether a weir's first section costs a base of 6 timber and 8 units…|Q-74]] and [[Q-75 Whether D2-210's yearly upkeep band wins over the river proposal's…|Q-75]] are open though built or replaced; [[W-77 Design wave part 1, the physical basis|W-77]] to [[W-84 Behaviour steered by defaults, examples and wording|W-84]] wait though their
drafts are folded into the design; [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]'s four defaults taken are on no record.

## 1. U0, the basis in code (u0_basis.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | goods in handling units, recipes in kg; fuel a night; keeping curve; cured goods; clocks; floor and batches; options list gone; faults first | §1 to §6 | built | `data.py:43-88` (weights), `:138-163` (`KEEP_DAYS`, `keep_nights`, `base_spoil`), `:875-881` (`CAPITAL`), `:910` (heat 0.5 / 1.5); `clocks.py:81-143`; `verbs.py:187-209` (floor, batch), `data.py:819-822` ([[O-2 Make the eleven bulk processes take up to their batch|O-2]]'s batches); no "Today you could" in `engine/` | |
| G1 | units read through `capital_units`; build techniques no longer copy `units` at import | §4 | later (stage 5) | `data.py:847-851` copies `units`; `capital_units` used nowhere outside `clocks.py` | [[W-106 Stage 5 of the wave, works|W-106]] (the hold) |
| G2 | the wild's rates still on the day clock | §7 | decided | left as calibrated, `clocks.py:20-30` | [[D2-315 The wild's rates still on the day clock are left as calibrated for…|D2-315]] |

## 2. U1, water and wild stocks (u1_water.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | shallows per parcel by water type, renewal, ice states, held runs, run reach, fen wreck, thaw, pinch, a run's fish learn no wariness | §1 to §8 | built | `wild/water.py:21-29` (tables), `:79-104` (`shallows_K`, `seed_shallows`), `:116` (`ice`), `:176-195` (`run_reach`, `pinch`); `wild/runs.py:316-390` (`iced`); `renewal.py:66`; `wild.py:921`, `:3320-3335` | ice revisited: [[L-161 Ice and the freeze|L-161]] |
| G3 | shallows K by the parcel's margin (`land.margin_km`) | §2, code table | partly: K by size only | `water.py:79-83`; no `margin_km` in `landgen/write.py` | in part by [[W-96 Space unified everywhere|W-96]], [[L-162 Scale mismatches to check together|L-162]] (the area of a unit of size) |
| G4 | a brook's open water cut to a fifth | §3 | decided (not cut) | B3's default "not without your yes" stands (questions.md header) | [[L-162 Scale mismatches to check together|L-162]] (open water against real) |
| G5 | herons and otters taking from the shallows | Gaps | nowhere | fish-eaters read the body's `fish` only | in part by [[L-116 The wild layer's fish and a water body, two ways|L-116]] |
| G6 | a brook through a land parcel holding shallows | Gaps | nowhere | `water_type` reads bodies (`water.py:57`) | untracked (low) |

## 3. U2, taking (u2_taking.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | placed gear from the hands, tend, theft of another's set, [[D2-304 An unnamed act on several of one's own things at a place|D2-304]]'s several of one's own, set line, gill net, snare night (dead, freed, scavenged), the fishing faults | §2, §3, §4.1, §4.5, §6 | built | `placed.py:123` (`lay`), `:208` (`tend_one`), `:355` (`tend_weir`), `:378` (`named_alone`); `gear.py:45-46`; `wild.py:921-949` | |
| G7 | snares' good places by edges and tracks, strange ground at half, sprung-empty nooses set again, the cold-line words ("thin", "shy") | §4.2 | nowhere | no places count in `wild/methods.py` or `wild.py`; stage 2 §6 | untracked |
| G8 | a gill net fouled in a spate (no take that night) | §4.4 | partly: torn at 0.3 in a flood; a spate does nothing | `wild.py:3326-3327` | untracked |
| G9 | the weir's tend with the water axis ("crammed: about as much again went past the gap", the gap open) | §4.3 | partly: the tend gives kg only; the overflow is a sign | `placed.py:355-373`; `wild/river.py:246`, `signs.py:2531` | untracked |
| G10 | the hunt's results: thin ground against shy game; the leader's weapon wearing on a hunt | §4.7 | nowhere | `wild.py:2703` ("came on nothing" for any cause); no wear in the hunt | untracked |
| G11 | scale words past a dozen ("scores of", "a hundred and more") | §5 rule 5 | nowhere | `things.py:369` stops at "a dozen or more" | untracked |
| G12 | a spear or leister at the edge (x1.5) | §4.6 | later | `gear.py:72-74` ("the spear with the hunting build-out"); the dip net x3 is built, `data.py:715` | [[L-111 The hunting and resources build, a soon follow-up|L-111]] |
| G13 | lending gear by agreement; a snare line across parcels | Gaps | nowhere | | untracked (low) |
| G14 | fowling net and method; the kill as a thing; bait; the seine and boats | §4.4, Gaps | decided / later | the `net` method untouched | [[D2-318 Fowling is postponed from this wave to the hunting build-out|D2-318]], [[L-170 Fowling the methods|L-170]]; [[L-111 The hunting and resources build, a soon follow-up|L-111]]; [[L-145 Offal's uses bait for set lines and traps, dog food|L-145]]; [[W-92 Boats, barrels and the cooper|W-92]] |

## 4. U3, materials and making (u3_making.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | withies (wild willow, summer harm, grazing), twist cord, flax (pull, ret, dress and spin), the strip, gear in kg with batches, two lives, mending, craft lines by level, making gates M1 to M8 | §1.1 to §1.3, §2, §3, §4, §7 | built | `wild/willow.py:17-70`; `data.py:531-542`, `:654-657`, `:752`; `strips.py:53-220`; `gear.py:36-46`, `:412`, `:449`; `knowledge.py:459-469` | |
| G15 | dressing a kill: hide by weight, bone, tallow, antler, pelts; a novice's losses | §1.4 | later | no `dress` technique; stage 2 §5: "nothing gives bone yet, so bone hooks cannot be made" | [[L-111 The hunting and resources build, a soon follow-up|L-111]] (butchering, bone, fur), [[L-121 Wildlife pack K8 crafts and wild goods|L-121]] (pelts) |
| G16 | the strip's words in the field's line in "Here"; grazing beasts trampling a dug strip | §1.3 | nowhere | `strips.words` (`strips.py:220`) is called nowhere; `herds.trample` reads crops only (`herds.py:217-239`) | untracked |
| G17 | the older tools as pieces (broken and mended, not vanishing) | §3.2 | nowhere | `gear.py:20-22` (wear map kept) | untracked |
| G18 | the withy bed (cuttings on a wet held parcel; 30 bundles a year from its third) | §2.2; u7 §2.3 | nowhere: not in stage 2 (wild willow built instead) nor stage 5's list | only the name in `livelihoods.py:106` | untracked |
| G19 | the retting pit (a work by water, no fouling) | §2.2; u7 §2.3 | nowhere | retting on ground by cover, `process.py:51-53` | untracked (low) |
| G20 | the tiered set of smoke racks (3 withies, 3 timber) | §2.2; u4 §4 | nowhere | no row | untracked (low) |
| G21 | each craft's learning data: lessons, capability points, aptitude profile | §5 | nowhere | `gate_check.py:136-141` (P7 warns: no lesson rows) | untracked ([[Q-82 Trying and learning|Q-82]] is an older ask) |
| G22 | M5 for every process site; M7 for every material bound | §7 | partly: M5 retting water only, M7 a wattle weir's withies only | stage 2 §6 | untracked |
| G23 | the frame, harness and bellows in leather, shoes, barking nets, bark | §1.5, §1.6, §2.2, §3.4 | decided | harness in rawhide `data.py:758` | [[D2-327 Tanning and leather are deferred from this wave until the rest is…|D2-327]], [[D2-329 Until tanning comes back, nets have a middle life of about half a…|D2-329]]; [[L-171 Tanning and leather|L-171]], [[L-169 Shoes, with clothing in general, and their health effects|L-169]] |

## 5. U4, processing containers (u4_processing.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | keeping smoke, hard cure, hearth rack, retting, salting, hot smoke; lots, the fire, the night step, take down, house lines | §2 to §7 | built | `process.py:44-58` (rows), `:307` (`load`), `:370` (`tend`), `:406` (`take_down`), `:454` (`night`), `:534` (`finish`), `:640` (`house_lines`) | |
| G24 | the wattle smoke hut (a hut room of 2 spaces) and the timber and stone smokehouses as things one can build | §4; u7 §2.1 | later by stage 3's report ("U7's, stage 5"), but not named in build_plan's stage 5 or [[W-106 Stage 5 of the wave, works|W-106]] | no hut room or smokehouse in `ROOMS` (`data.py:363-372`); `process.py:625-629` reads a hut kind no room has | untracked |
| G25 | the hot smoke at a fire in the open | §2 | partly: hearth or fire ring only | stage 3 §5 | untracked (low) |
| G26 | process nights derived from real days through `clocks.RATES` | §2 | partly: written as compressed numbers | `process.py:44-58` | untracked (low) |
| G27 | the wind rack (stockfish) and its wet-night failure | Gaps 4 | nowhere (spec defers) | | untracked; waits on the coast ([[W-88 The coast and the sea|W-88]]) |
| G28 | a keeping curve by a lot's age, carried into the store | Gaps 7; u5 Gaps 4 | nowhere (spec defers) | stores hold one quantity a good | untracked |
| G29 | liming and tanning rows | §2 | decided | | [[D2-327 Tanning and leather are deferred from this wave until the rest is…|D2-327]]; [[L-171 Tanning and leather|L-171]] |

## 6. U5, stores and containers (u5_stores.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | spaces and containers in kg, named penalties, the sort, vermin by exposure, vermin's illness, the store line, the smoke loft, the chest | §1 to §6 | built | `stores.py:35-80`, `:188` (`portions`), `:250` (`rate`), `:312-356` (vermin, illness), `:370` (`store_line`) | |
| G30 | the granary on staddles, the sealed pit, the door pile as portions of the sort | §1 | nowhere | `stores.py:35`, `SPACE_ORDER` `:51` | untracked |
| G31 | attending to a store: each space and container, its fill, state and life, last night's spoiling by where, the rules acting on it | §7 | nowhere | no attend path in `stores.py` | untracked |
| G32 | the vermin signs' chances checked against intended values | §5; guides/senses.md item 4 | nowhere | stage 3 §6 | untracked (low) |
| G33 | the clamp, the rick and the barn | Gaps 5 | nowhere (spec defers) | | untracked |
| G34 | wet fuel; the locked chest; vermin with disease | Gaps 6, 7; §6 | later | | [[W-76 The timber economy|W-76]]; [[L-156 The locked chest and its key|L-156]]; [[L-155 Vermin fleshed out properly, with disease and sanitation|L-155]] |

## 7. U6, the household book (u6_book.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | one book a household and a person, [[D2-337 Standing rules are written in a stated grammar the prompt gives in…|D2-337]] and [[D2-339 The household book's grammar|D2-339]]'s grammar, named sets ([[D2-338 The household book has named sets as a primitive|D2-338]]), `when` and `unless`, the spare-units phase person by person ([[D2-301 A person's own rules and standing fallback come before every…|D2-301]]), standing fallback, rest, rules block, morning and day lines, an empty chore stopped ([[W-104 Build the after-runs list from live run 1|W-104]]), precedence | §1 to §9 | built | `book.py:281` (sets), `:378` (`cond`), `:562` (`read`), `:822` (`apply_rules`), `:834` (`act`), `:1057` (`_ranked`, [[D2-339 The household book's grammar|D2-339]]), `:1212` (`set_fallback`), `:1231` (`spare_units`), `:1401` (`rules_block`), `:1460` (`empty_lines`) | |
| G35 | a member's household rule as a proposal the head sees at the evening and takes | §1 | nowhere: stored and promised, never shown or taken | `book.py:1127-1131` ("It stands once {head} takes it"); no reader of `proposals` in `book.py`, `evening.py`, `prompt.py`, `view.py` | untracked |
| G36 | children's standing work as a household chore | Gaps 3 | nowhere (waits on live runs) | `data.py:1297` (the head's order) | untracked |
| G37 | the eating rules (who first, rations, guests); rules passed to a founded household; who may change them; a shared book, travel in the book | §3 moment 4, Gaps 4 to 6 | later | | [[W-37 Standing rules|W-37]] (37.4's, discussion); [[L-151 A household as a shared book of standing rules people subscribe to|L-151]]; [[L-152 Travel folded into the standing rules|L-152]] |

## 8. U7, works and the building clock (u7_works.md; build_plan stage 5)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | the capital lever and conversions; a build act costs what is left ([[D2-324 A build act costs what is left of the work|D2-324]]); practice every build act; the weir's cost in one place by its water ([[D2-302 The weir's cost for now, to calibrate in live runs, on a lowland river|D2-302]]); the watch act ([[D2-320 Crop protection stays as it is for now|D2-320]]) | §1, §3, §5.2, §5.4 | built | `clocks.py:81-143`; `verbs.py:155`, `:227-282`; `wild/gear.py:86-106`; `verbs.py:135`, `:2673` | |
| G38 | releasing the hold: rooms, fittings, monuments, the weir and stores to 1/15, then fences, clearing and field works (5b); the target factor (5c) | §4 | later (stage 5) | `data.py:878` holds all seven classes | [[W-106 Stage 5 of the wave, works|W-106]] |
| G39 | fences along one border, in sections one can target; attending shows where they stand | §6.3; [[D2-322 Fences can be built along one border between two parcels, in sections…|D2-322]] | later (stage 5) | `farm.py:867-871` round a parcel only; no border record | [[W-106 Stage 5 of the wave, works|W-106]]; [[L-24 Fences on the borders between parcels|L-24]] (older) |
| G40 | fences priced by their length (hours and materials a 100 m) | §6.3 | later (stage 5) | `data.py:1103-1110` (4 timber, 10 units x √size) | [[W-106 Stage 5 of the wave, works|W-106]] (border fences) |
| G41 | clearing a plot at a time, the cleared part a field while the rest is scrub | §7; [[D2-323 A cleared plot becomes a field part of its parcel, sown while the…|D2-323]] | later (stage 5) | `verbs.py:2806-2825` (whole parcel) | [[W-106 Stage 5 of the wave, works|W-106]]; [[L-153 Clearing a plot at a time|L-153]] (still a deferral) |
| G42 | material got at the site counted in the work (field stone, brush, daub) | [[D2-306 Material got at the site of a work|D2-306]] | partly: the cairn and the wattle room's roof only | `data.py:417`, `:365`; a wall still takes 8 stone x √size, `data.py:1108` | [[W-106 Stage 5 of the wave, works|W-106]] |
| G43 | a wattle house's roof of turf or brush by default, shorter-lived; straw thatch the better roof | [[D2-328 A wattle house's default roof is turf or brush got at the site|D2-328]] | partly: no straw in the wattle row; no roof kind, life or thatch option | `data.py:365` | [[W-106 Stage 5 of the wave, works|W-106]] |
| G44 | fittings' lives in uses (the oven's lining, the millstones' dressing, the brine pan's boilings) | §2.2, code table | later (stage 5) | no `uses` on any fitting in `data.py` | in part by [[W-106 Stage 5 of the wave, works|W-106]] (the hold) |
| G45 | materials carried from another parcel's store add moving units to the work | §8 (stage 5a) | nowhere: in u7's 5a, not in build_plan's stage 5 list | no moving units in `verbs._consume` | untracked |
| G46 | [[W-82 The building clock's first stage read with bots|W-82]]'s act log (each act with its units and result) | §4 stage 1, fault 3 | nowhere | not in `run.py`; stage 1 §6 | untracked |
| G47 | the dead `PHYSICS.cattle.stray` removed | §4 stage 1, fault 5 | nowhere | `data.py:965`, `clocks.py:26`; read nowhere | untracked (trivial) |
| G48 | the straw a world's houses need counted by the gate check (B23's default) | §2.3 | nowhere | no straw check in `gate_check.py` | untracked |
| G49 | one mending act mends as many levels as its work covers (the weir) | §3 | nowhere; its premise sat in the model [[D2-302 The weir's cost for now, to calibrate in live runs, on a lowland river|D2-302]] replaced | `verbs.py:1508-1541` (a level a section) | untracked (low) |
| G50 | one skill a trade (carpentry, masonry) | §5.1 | later | `verbs.py:1141` maps names only | [[W-76 The timber economy|W-76]] |
| G51 | soundness from craftsmanship; tiers needing a builder of skill; the dead hedge; children herding daily, a child's 15 head; moved folds | §5.3, §5.5, §6.1, §6.2, §6.4 | decided | | [[D2-321 Builders' craftsmanship setting a building's soundness is postponed|D2-321]], [[L-164 Builders' craftsmanship|L-164]]; [[D2-320 Crop protection stays as it is for now|D2-320]], [[L-167 The dead hedge and cheaper crop protection, thought through|L-167]], [[L-158 Daily herding as cheaper crop protection|L-158]], [[L-166 Herding for as long as it takes|L-166]]; folds [[L-24 Fences on the borders between parcels|L-24]] |

## 9. U8, signs and senses (u8_signs.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | the river's night record and bands, the four leads, signs for anyone ([[D2-325 Some river signs are for anyone|D2-325]]), the flow, slackening, ice, otters, the weir's overflow, the fen, the carried catch, directing rows reworded, the smokehouse's rows | §1 to §5 | built | `wild/river.py:31`, `:113`, `:167-260`, `:319`, `:429`, `:470`; `signs.py:853-861` | |
| G52 | the "quiet water" and "fish rising" rows on the open water's state and a run | §3.4 | partly: as before | `signs.py:687`, `:692` | untracked (low) |
| G53 | the moon (the eels' dark-of-the-moon cue) | Gaps | nowhere: u8 sends it to docs/engine_gaps.md, which this repository does not have | `environment.py:150` takes `moon` as an argument only | untracked |
| G54 | news of the run from a village upriver; the remembered good and thin years past two; smell's visibility in rain and wind | Gaps | nowhere | | untracked |
| G55 | a flood over the land; gulls at a run | Gaps | later | | [[W-49 Environment systems|W-49]]; [[L-149 Gulls and other coastal birds, with the coast|L-149]], [[W-88 The coast and the sea|W-88]] |

## 10. U9, people (u9_people.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | the core prompt and reply, the system prompt in order, the eleven shapes over 40 handlers, the old prompt as a setting ([[D2-331 Live run 1 has a comparison arm|D2-331]]), learning as one record with [[D2-307 Learning is scaled with the lifespan in every part|D2-307]] and [[D2-326 Practice alone can bring a person to known in any craft|D2-326]], the fallback as a setting, the rest line, the watch act, founders' BS, PE1, PE2, HH1, HH3, HH5 to HH10, FI, SA and four NB lines, the cap | §1 to §3, §4.1 to §4.3, §4.6, §5.1 to §5.6 | built | `core.py:16`, `:114`, `:138-151`; `shapes.py:23`, `:264`, `:457`; `learning.py:28-207`; `founders.py:91-531`, `:613-691` | |
| G56 | lessons and failure lines; attention spent in units (departure 21); children minded at home (B31); capability points; seven aptitudes and transfer (B30), the teacher's dealing | §4.4, §4.5, §4.7, §4.8 | nowhere (outside stage 4's brief) | `learning.py:24` ("Not built here"); `watch` still a day beside someone (stage 4 §5) | untracked ([[Q-81 Knowledge in their own words|Q-81]], [[Q-82 Trying and learning|Q-82]] are older asks); strength: [[L-168 Strength as an aptitude|L-168]] |
| G57 | goods shown by familiarity, with their uses; the carry line in kg in "## You" | §2.6 | nowhere | `prompt.py:493`, `:557` (the old weights phrase in the rules) | untracked |
| G58 | one's own things with their tags in "## You" | §2.7 | nowhere | no such line in `view.py` or `prompt.py` | untracked |
| G59 | the eleven other livelihoods' sets, FI13, FI14, an NB line each | §5.5 | later | `founders.py:484-487` (NB for four); ROWS name ids with no template | [[W-105 The founders' seeded lines for every built livelihood|W-105]] |
| G60 | HH2 (next year's seed, held back by rule) | §5.4 | nowhere: not written and not in a head's wanted list | `founders.py:576` (HH1, HH3, HH5 to HH9) | untracked; outside [[W-105 The founders' seeded lines for every built livelihood|W-105]]'s brief |
| G61 | HH4 (containers and vermin; condition "U5 built", now true) | §5.4 | nowhere | not in `founders.py` | untracked |
| G62 | PE3 (an elder's hard winters) | §5.3 | nowhere: wanted for elders, no template, so skipped | `founders.py:572`; u11 Gaps (the history's `year` unchecked) | untracked |
| G63 | keeper lines for every holding (mill, oven, forge, fields, ox pair, herd, withy bed) | §5.6 | partly: three kinds dispatched | `founders.py:530` (`KEEPER`), `:587-596` (weir, racks, pan only) | [[W-105 The founders' seeded lines for every built livelihood|W-105]] (its brief wires `KEEPER`, not `wanted`'s dispatch: noted) |
| G64 | cultural strands (BS8's variants; `culture.passing_on`) | §5.7 | nowhere | no `culture` in `founders.py` or `livelihoods.py` | untracked |
| G65 | a spouse's lines from their natal household; neighbours a day away | §5.7 | nowhere | NB lines for the same village only, `founders.py:604-606` | untracked (with G69) |
| G66 | the founders' lines rendered with any id lacking a template reported, never silent | §5.1; u11 departure 2 | partly: skipped ids kept in the fill's report only | `founders.py:613-631`, `:684`; `livelihoods.py:422`; nothing reads it (see G71) | untracked ([[W-105 The founders' seeded lines for every built livelihood|W-105]]'s brief adds a test for ROWS ids only) |

## 11. U10, tanning and pollution (u10_tanning_pollution.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| G67 | tanning, bark, lime from ash, the pits, leather's uses, shoes, tanning's fouling | §2, §3 | decided | | [[D2-327 Tanning and leather are deferred from this wave until the rest is…|D2-327]]; [[L-171 Tanning and leather|L-171]], [[L-169 Shoes, with clothing in general, and their health effects|L-169]], [[L-172 Limestone and lime|L-172]] |
| G79 | retting's fouling of the water: the state, the loads, fade and carry downstream, the harm to the shallows and traps, the stink and fouled-water signs | §3 (kept in this wave by u10's header and the README) | nowhere: in no build stage | no fouling state in `engine/` or `wild/` (the only "fouled" is a spent trap, `things.py:394`) | untracked as a wave item ([[W-49 Environment systems|W-49]] names fouling among missing environment interactions) |

## 12. U11, worlds and gates (u11_worlds.md)

| # | Mechanism | Section | Status | Evidence | Tracked by |
|---|---|---|---|---|---|
| | the fifteen rows, the holdings registry, pinned fill (experts, capable share, keepers raised, apprentices, second hands, gear, the cast, livelihood line), gate check P1 to P3, P5 to P8, P10 to P21, M1 to M8, Eelmouth remade with its arms | §1, §2, §3.1, §3.2, §4 steps 2, 4, 6, 8 to 11, §5, §7 | built | `livelihoods.py:17`, `:127`, `:197-422`, `:392-406`; `landgen/gate_check.py:20-141`; `specs/make_eelmouth.py`, `specs/nutrition/eelmouth.yaml` | |
| G68 | step 3: unpinned households' livelihoods drawn by `village_mix`, region quotas, the village rule | §4.2 | nowhere | `livelihoods.py:213-216` skips them; `write.py:28-29` unchanged | untracked |
| G69 | step 5 and 7: the family tree carrying livelihoods; what spouses and fosterlings carry; the PE lines in place of `generate.py`'s memories | §4.2, §9 | nowhere | no `skills` or livelihood in `engine/generate.py` | in part by [[O-4 Bridge the backward family-tree build into world generation as an…|O-4]] (the backward tree bridged into generation) |
| G70 | the gate check run at world build (a refused world not run; `<world>.report.json` for every world) | §5.1 | nowhere: stage 2 sent it to stage 4, stage 4 wrote a command line | called only by `make_eelmouth.py:113`, `make_eelmouth_small.py:53`; nothing in `world.py` or `run.py` | untracked |
| G71 | P4 (templates whose condition is false, or missing: report) and P9 (a craft at capable with no capital within a day: refuse or warn) | §5.2 | nowhere | P ids in `gate_check.py`: 1 to 3, 5 to 8, 10 to 21 | untracked |
| G72 | Hollinford, the mixed farm village without leather, and its maker | §8, §9; [[D2-330 The worlds' defaults as proposed|D2-330]] C4 | later (build_plan stage 5) | no Hollinford file in `specs/` | [[W-106 Stage 5 of the wave, works|W-106]] ([[D2-345 Zach's go for stage 5|D2-345]]) |
| G73 | live run 2: Hollinford with a newcomer household at 1/15 against its null arm | build_plan; [[D2-330 The worlds' defaults as proposed|D2-330]] C7 | later (Zach's go given, after stage 5: [[D2-345 Zach's go for stage 5|D2-345]]) | | [[W-106 Stage 5 of the wave, works|W-106]] |

## 13. Across the wave: reports, runs and records

| # | Item | Where | Status | Tracked by |
|---|---|---|---|---|
| G74 | the four defaults [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]] took (go to a building here at nightfall is sleeping there; `agree` with a craft teaches if known, else learns; [[D2-339 The household book's grammar|D2-339]]'s rule fields, three cascade rounds, an unreadable old record dropped; moving goods out of a store costs 1 unit) | `fix_shapes_report.md:250-257` | built; never asked | untracked (CLAUDE.md: a default taken is a row in OPEN) |
| G75 | live run 1's question: should a water-only village last the year, or is the spring gap the point | `live1_report.md` "For after the runs" | answered while this was written | [[Q-89 Whether a water-only village should last the year, or the spring gap…|Q-89]], closed by [[D2-347 A water-only village should be able to last the year|D2-347]] (a water-only village should be able to last the year): work implied, on no thread yet |
| G76 | the wording bugs ("the Marshs household", "which the Brooks holds", crumbs in the meal line) | `after_run1_report.md` "Seen in passing" | open | [[L-178 Wording bugs|L-178]] |
| G77 | noticing within the day; the signs survey and design | `live1_report.md` | open | [[L-176 Noticing in parts of the day, so what is seen at mid-morning can…|L-176]]; [[W-103 Signs and what people can know of the state of things|W-103]] |
| G78 | the A/B replay of a worked conditional rule | `live1_report.md`; [[D2-344 No worked example of a conditional rule is added to the rules block|D2-344]] | open | [[L-177 AB prompt replay|L-177]] |

**Stale records** (each hides what is left): **[[O-2 Make the eleven bulk processes take up to their batch|O-2]]** (the bulk processes up to their batch) is open, though built in stage 1
(`data.py:819-822`); **[[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]** (the fishing bugs) open though fixed in stage 1 with regression tests; **[[Q-74 Whether a weir's first section costs a base of 6 timber and 8 units…|Q-74]]** and **[[Q-75 Whether D2-210's yearly upkeep band wins over the river proposal's…|Q-75]]** (the
weir's first section and upkeep band) open though [[D2-302 The weir's cost for now, to calibrate in live runs, on a lowland river|D2-302]] set the weir's cost and upkeep; **[[Q-81 Knowledge in their own words|Q-81]]** and **[[Q-82 Trying and learning|Q-82]]** open though [[D2-307 Learning is scaled with the lifespan in every part|D2-307]] and
[[D2-326 Practice alone can bring a person to known in any craft|D2-326]] decided and stage 4 built parts of them; **[[W-73 Fishing, hunting and their materials developed together|W-73]]**'s `next` is the morning brief's questions (answered: [[D2-288 Bulk goods are counted in handling units of a stated weight and every…|D2-288]] to [[D2-330 The worlds' defaults as proposed|D2-330]]);
**[[W-85 The wave's integrated design|W-85]]**'s `next` ends at live run 1, with nothing for stage 5; **[[W-101 Live run 1 two sets of small runs|W-101]]**'s `next` lists the after-runs work [[W-104 Build the after-runs list from live run 1|W-104]] built;
**[[W-77 Design wave part 1, the physical basis|W-77]] to [[W-84 Behaviour steered by defaults, examples and wording|W-84]]** (the design wave's drafts) are `waiting` though the integrated design took them in. **[[L-153 Clearing a plot at a time|L-153]]** (clearing a plot at a
time) is still a deferral though [[D2-323 A cleared plot becomes a field part of its parcel, sown while the…|D2-323]] decided it.

## 14. The untracked gaps, with a proposed record each

Stage 5 first: its thread ([[W-106 Stage 5 of the wave, works|W-106]]) now exists, so its gaps go into [[W-106 Stage 5 of the wave, works|W-106]]'s brief; most of the rest attach to a stage or a deferral.

| Gaps | Proposed record |
|---|---|
| G24, G45, G46, G47, G48, G49 | **Into [[W-106 Stage 5 of the wave, works|W-106]]'s stage 5 brief** ([[W-106 Stage 5 of the wave, works|W-106]] already names G1, G38 to G44, G72, G73): the smoke hut and the timber and stone smokehouses as blueprints (G24), materials carried to the site (G45), the act log and the dead `stray` (G46, G47), the straw check in the gate (G48), mending several levels an act (G49); and on merge, close [[L-153 Clearing a plot at a time|L-153]] and [[L-24 Fences on the borders between parcels|L-24]]'s border part into it. Waits on: [[W-105 The founders' seeded lines for every built livelihood|W-105]]'s merge ([[D2-345 Zach's go for stage 5|D2-345]]) |
| G68, G65 | **A thread for u11's generator steps 3, 5 and 7** (step 5 and 7 in part with [[O-4 Bridge the backward family-tree build into world generation as an…|O-4]]) (unpinned households by `village_mix`, the tree carrying livelihoods, what spouses carry, PE lines in `generate.py`), so generated worlds get livelihoods and lines. Waits on: [[W-105 The founders' seeded lines for every built livelihood|W-105]] (the lines it would seed); the generation redesign [[Q-45 The generation redesign|Q-45]] bears on it |
| G70, G71, G66 | **Stage 4's gate check finished** (a thread, or a child of the generator thread): run at world build with the report written for every world; P4 reporting every skipped or missing template; P9. Waits on: nothing; best before any non-Eelmouth run |
| G60, G61, G62, G63 | **Add to [[W-105 The founders' seeded lines for every built livelihood|W-105]]** (or a follow-up row): HH2, HH4 and PE3, and `founders.wanted`'s keeper dispatch read from `HOLDINGS` (`founders.py:587-596`). PE3 waits on checking `generate.simulate`'s history `year` |
| G64 | **A deferred row: the cultural strands** (founders_knowledge Part 3's twelve; BS8 (a) against (c) first, a world's `culture.passing_on`). Waits on: [[W-105 The founders' seeded lines for every built livelihood|W-105]]'s lines and a second live run to compare against |
| G35 | **A deferred row (or a [[W-37 Standing rules|W-37]] item, 37.4's):** the head shown members' proposed household rules at the evening and an act to take or refuse one; until then the member's result should not promise it. Waits on: nothing |
| G56, G21 | **A deferred row: u9 §4's learning remainder** (lessons and failure lines with each craft's lesson rows, attention in units, children minded at home, capability points, aptitudes and transfer). Waits on: live run 1's reading of teaching and passing on; close or rewrite [[Q-81 Knowledge in their own words|Q-81]] and [[Q-82 Trying and learning|Q-82]] into it |
| G57, G58 | **A deferred row: "## You" as u9 §2.6 and §2.7 design it** (goods by familiarity with uses, the carry line in kg, one's own things with their tags). Waits on: [[W-103 Signs and what people can know of the state of things|W-103]]'s signs and attending design, which touches the same view |
| G79 | **A deferred row: retting's fouling (u10 §3, flax only)**, the state, loads, fade, carry, harm and signs. Waits on: a world that rets flax in water (Hollinford); belongs with [[W-49 Environment systems|W-49]] |
| G18, G19, G20 | **A deferred row: the wave's missing works and fittings for materials** (the withy bed, the retting pit, the tiered rack set). Waits on: stage 5's thread (priced on the lever there); the withy bed before any basket-maker or big-weir world |
| G7, G8, G9, G10, G11 | **A deferred row: taking's unbuilt wording and snares** (snare places and strange ground, sprung nooses, the cold line; the net fouled in a spate; the weir's water axis; thin against shy in the hunt and the weapon's wear; scale words). Waits on: the hunting build-out ([[L-111 The hunting and resources build, a soon follow-up|L-111]]) for the snares and the hunt; the rest needs nothing |
| G16, G17, G22 | **A deferred row: making's loose ends** (the strip's words and trampling, the older tools as pieces, M5 and M7 widened). Waits on: a world with flax strips and grazing (Hollinford) |
| G30, G31, G32, G33, G28 | **A deferred row: stores' remainder** (staddles, sealed pit, door pile; attending a store; the vermin signs' chances; clamp, rick and barn; dated lots). Waits on: the crops pack and a farm world's live run |
| G36 | **A deferred row:** children's standing work folded into the book. Waits on: live runs comparing [[D2-148 A child's menial work is set by the household head's standing order|D2-148]]'s dial |
| G27 | **A deferred row under [[W-88 The coast and the sea|W-88]] (the coast):** the wind rack and stockfish |
| G25, G26, G52 | **A deferred row: small keeping and sign rework** (hot smoke in the open, process nights from `RATES`, the open water's rising and quiet rows). Waits on: nothing |
| G53, G54 | **Add to [[W-103 Signs and what people can know of the state of things|W-103]]'s design questions** (the moon as state, news from upriver, remembered years past two, smell's visibility). Waits on: [[W-103 Signs and what people can know of the state of things|W-103]] |
| G6, G13 | **One low row**, or none: a brook through a land parcel, lending gear and a snare line across parcels. Waits on: the agreements (lending) |
| G74 | **An ask row (default taken)** listing [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]'s four defaults, to tell Zach |
| (G75) | Tracked now ([[Q-89 Whether a water-only village should last the year, or the spring gap…|Q-89]], [[D2-347 A water-only village should be able to last the year|D2-347]]). [[D2-347 A water-only village should be able to last the year|D2-347]] implies work on no thread: what Eelmouth lacks to carry a water-only village through the spring gap; a row under [[W-101 Live run 1 two sets of small runs|W-101]] or [[W-85 The wave's integrated design|W-85]], and [[W-101 Live run 1 two sets of small runs|W-101]]'s `next` updated |

## Sources

`docs/cybertron2/proposals/w73_design/` (all files); `docs/review/37_growth/02zzzh_hunt_fish/` stage1_report.md to stage4_report.md
(§5, §6), fix_shapes_report.md, after_run1_report.md, live1_report.md; `docs/cybertron2/items/` ([[W-73 Fishing, hunting and their materials developed together|W-73]], [[W-85 The wave's integrated design|W-85]], [[W-97 Build stage 1, the basis in code|W-97]] to [[W-105 The founders' seeded lines for every built livelihood|W-105]], the open
L, Q, O items, [[D2-302 The weir's cost for now, to calibrate in live runs, on a lowland river|D2-302]], [[D2-306 Material got at the site of a work|D2-306]], [[D2-309 One capital factor for every lasting thing|D2-309]], [[D2-320 Crop protection stays as it is for now|D2-320]] to [[D2-330 The worlds' defaults as proposed|D2-330]]); the [[W-105 The founders' seeded lines for every built livelihood|W-105]] brief (commit 2b993292); the code on `main` at 32b8c942 as cited.
