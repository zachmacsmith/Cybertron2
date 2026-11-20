---
id: docs/review/37_growth/02zzp_audit/records.md
kind: note
updated: "2026-11-19"
tags: [note, open]
---
# Records audit: what the documents say against what is true (19 Nov 2026)

## Text
# Records audit: what the documents say against what is true (19 Nov 2026)

Read-only audit of /home/user/cybertron2 at `origin/main` a38b1c7 (19 Nov 05:20). Nothing was edited. Rules checked against:
CLAUDE.md, docs/cybertron2/README.md. "On main" means `git merge-base --is-ancestor <hash> origin/main`.

Counts: **1. proposals** 38 files mismatched (17 "not built/not merged" but on main; 14 built without a decision, branch-only, or unindexed; 7 "Design only" but built); **2. notes** 15 plan items or lists
that exist only in a note; **3. branches** 13 ahead of main (of 30 refs), 2 with no record, 4 holding commits found nowhere else;
**4. WORK.md** 21 rows contradicting the repository, 4 duplicate numbers; **5. hygiene** 11 sections, 285 listed items.

---

## 1. Proposals: status against the repository

138 files read (137 proposals and README.md). The wild layer (briefs 1 to 4c) and the peoples worlds were merged to main on 16 Nov
(7ddc1c8, 6190b4d; WORK [[W-36 Build brief 4c, then the merge of the wild layer (briefs 1 to 4c,|W-36]], [[W-6 Merging the wild layer into main|W-6]]). The water work (brief 5 onward) is on unmerged branches only (section 3).

### 1a. "Not built", "to be built" or "not merged", but on main

| Path (docs/cybertron2/proposals/) | Status as written | What is true | Evidence |
|---|---|---|---|
| hunt_and_fixes.md | built and gated on `ecology-calibrate` (58bb2d3) ... "Not merged: waits on Zach. No DECISIONS row yet" | merged to main 16 Nov; **still no DECISIONS row** | 58bb2d3 on main; [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]] (Zach: "still merge"); `grep hunt_and_fixes DECISIONS.md` = 0 |
| hunt_followups.md | built on `ecology-hunt2` (8158674) ... "Not merged: waits on Zach" | merged; no DECISIONS row; no outcome-log row | 8158674 on main; grep DECISIONS = 0 |
| hunt_calibration.md | built on `ecology-hunt3` (e98d893, "merge f58764f"), merged into `peoples-worlds`; "Not merged into main; no DECISIONS rows yet" | on main; no DECISIONS row ([[Q-46 Brief 4c as built|Q-46]] a still open); no outcome-log row; **f58764f does not exist** in the repository | e98d893 on main; `git cat-file -t f58764f` fails |
| methods_and_encounters.md | accepted [[D2-204 People answer the wild by general methods, not a technique per|D2-204]], [[D2-207 The three wild build briefs are built|D2-207]]; "to be built" | built (brief 1) and on main | [[D2-207 The three wild build briefs are built|D2-207]]'s own text says "are built"; WORK [[W-1 Build brief 1 general methods (D2-204, D2-207); branch ecology-met|W-1]] done; ecology-methods merged |
| wild_raiders_and_works.md | accepted; "to be built after brief 1's gate" | built and on main | f290e2c (ecology-raiders) on main |
| carcass_and_decay.md | accepted; "to be built after brief 2's gate" | built and on main | cc4d342 (ecology-carcass) on main |
| shelter_damage.md | "discussion (9 Nov). Nothing decided or built." | built as brief 4 stage B, on main; its own History (10 Nov) says so; no decision row | engine/buildings.py:328, engine/data.py:648 cite "shelter_damage.md §1 to §4" |
| cats.md | "discussion (9 Nov). Nothing decided or built." | built as brief 4 stage C, on main; no decision row | History 10 Nov; wild/kinds.py:393 (the stray cat, [[D2-206 The cat comes by itself or is found|D2-206]]); engine/wild.py cites cats.md |
| wildlife.md | partly accepted [[D2-192 The first wild kinds come in four waves|D2-192]] to [[D2-196 Hounds in wave 2, with the wolves; hawks in wave 3, with the fa|D2-196]]; "Not built" (README index the same) | 15 kinds on main (waves 1, 2 and the bear) | `wild.kinds.KINDS`: red deer, roe, hare, eel, wildfowl, raven, wolf, boar, fox, brown bear, ... |
| wild_systems.md | "the rest discussion (8 Nov). Nothing built." | its own History (9 Nov): "wave 1 built on the general rules"; on main | History; wild/ecology.py on main |
| living_populations.md | "Nothing decided, nothing to build" | the live populations it designs are built (wild layer, [[D2-199 The wild layer is built on 37.2's own ecology branch|D2-199]], wild/ecology.py) and [[D2-192 The first wild kinds come in four waves|D2-192]] is built "on the mechanism of" it | [[D2-192 The first wild kinds come in four waves|D2-192]] row; 7ddc1c8 |
| node_ecology.md | "Nothing decided, nothing built" | [[D2-197 Lead times and creature memory are set in engine days, never le|D2-197]] decides its scaling principle ("stocks and rates keep the scaling principle (proposals/node_ecology.md)"); the layer runs on village areas | DECISIONS [[D2-197 Lead times and creature memory are set in engine days, never le|D2-197]]; wild/areas.py |
| phase3_variance_and_risk.md | "an exploration of what phase 3 builds, nothing built" | the weather scheduler, moving storms, weather by place, base fertility and the renewal hook ([[D4-109 The weather scheduler|D4-109]] to [[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]) are built | WORK [[W-16 The engine overhaul phase 2's open decisions and phase 3's rest (|W-16]]; weather_scheduler.md "built"; engine/climate.py |
| environment.md | "Not built: eras, years and spells drawn by a scheduler ... The scheduler itself is still design only" | eras, years and spells are drawn ([[D4-109 The weather scheduler|D4-109]]) | engine/climate.py lines 5-18 (`era`, `year`, spells) |
| recipes.md | "Not built: making salt, salted meat, traps, ..." | salt making, salt meat and set traps built (brief 4 §5.2, brief 2) | engine/data.py:72, 513, 517 |
| water_and_preservation.md | "Nothing decided, nothing to build" (README index the same) | [[D4-103 The engine overhaul goes ahead, in phases|D4-103]] makes it phase 1's acceptance content; brief 5 built its fishing, weir, smoking and brine salt ([[D2-209 Brief 5 (river and water) is built|D2-209]] to [[D2-219 A run night's work counts shutting|D2-219]]) on `ecology-water`; [[D4-122 Fish on the hearth rack|D4-122]] fish drying | DECISIONS [[D4-103 The engine overhaul goes ahead, in phases|D4-103]] ("content: water_and_preservation.md"); [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]] |
| peoples_benchmark.md | "Built at Zach's request on branch `peoples-worlds`" | on main | e54c722 on main; [[W-36 Build brief 4c, then the merge of the wild layer (briefs 1 to 4c,|W-36]] |

### 1b. Accepted or built with no decision, or built only on a branch with the status silent

| Path | Status as written | What is true | Evidence |
|---|---|---|---|
| model_households.md | "accepted in conversation, to build (17 Nov): one run, **24 days**"; History "Nothing built" | built on `runs-models` and running ([[W-58 The runs world with a model to each household (Zach, 17 Nov; prop|W-58]], 38.78); the world is **100 days** (a2ad706); no DECISIONS row; not in the README index or outcome log | a2ad706, c8c6481, 64ab312 (runs-models only); hygiene §4 |
| signs_pass_17nov.md | "retrospective, accepted in conversation" (no D-n); "11 built" | built only on `lake-fixes`/`runs-models`, not on main; no DECISIONS row (CLAUDE.md step 3a needs one) | 47774a0, b30abc0 not on main |
| river_and_water.md | "accepted for building: [[D2-209 Brief 5 (river and water) is built|D2-209]] ... the merge left to the building session" | built and gated on `ecology-water` (5033573; 38.73), not merged; [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] to [[D2-219 A run night's work counts shutting|D2-219]] not in the status | [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]]; 5033573 not on main |
| environment_systems.md | partly accepted [[D2-221 The land in three speeds|D2-221]] to [[D2-228 Calibrate across a distribution of worlds|D2-228]]; "Nothing built yet" | floodplains ([[D2-226 Floodplains in the generator, now|D2-226]]) built on `floodplains` (d69b525); one stock per water body ([[D2-229 One fish stock per water body|D2-229]]) on `water-bodies` (594ba09); neither on main | [[W-53 Floodplains in the generator now (D2-226) valley floors widening|W-53]], [[W-56 One fish stock per water body, the engine half (D2-229; 37.2's ha|W-56]] |
| generator.md | status as of 5 Nov | since then: [[D2-208 The world keeps the land it runs on|D2-208]] (land kept), [[D4-118 The land generator takes a designed world|D4-118]] (designed worlds, on main), [[D2-226 Floodplains in the generator, now|D2-226]] floodplains and the `has: brine spring` / `on: big river` pins (branches only) | DECISIONS; cc6f38d, d69b525 |
| catch_and_lakes.md | "accepted: [[D4-119 Luck in a catch by hand or by rod|D4-119]], [[D4-120 A lake's fish by its size|D4-120]], [[D4-121 A fishing household in the water worlds (a stopgap)|D4-121]] ... Built on `ecology-water`" | [[D4-120 A lake's fish by its size|D4-120]] is replaced by [[D2-229 One fish stock per water body|D2-229]] (its History says so; the status does not); not on main | DECISIONS [[D4-120 A lake's fish by its size|D4-120]] "replaced by [[D2-229 One fish stock per water body|D2-229]]" |
| fish_on_the_rack.md | "retrospective, accepted: [[D4-122 Fish on the hearth rack|D4-122]]" | built only on `lake-fixes`; the status does not say it is off main; [[L-115 Dried fish in the economy spec|L-115]] (spec row) open | 47774a0 not on main |
| economy_web.md | "discussion (15 Nov). Nothing decided or built." | Zach flagged its stages 1 and 2 as "a soon follow up" ([[L-111 The hunting and resources build, a soon follow-up|L-111]], 16 Nov); no outcome-log row | OPEN [[L-111 The hunting and resources build, a soon follow-up|L-111]] |
| livelihood_archetypes.md | discussion (16 Nov), Zach's answers in History | not in the README index or log, no WORK row, no OPEN row: an initiative with no record outside its file | hygiene §4; grep WORK/OPEN = 0 |
| standing_rules.md | "discussion (13 Nov 2026)." | not in the README index or log, no OPEN ask for its questions; WORK [[W-37 Standing rules how a household eats and what it keeps back, with|W-37]] uses the non-state "discussion" | hygiene §4 |
| descendants_benchmark.md | "deferred ... Nothing decided or built" | its peoples variant was decided ([[D4-115 The peoples benchmark's worlds|D4-115]]) and built and run ([[W-34 Worlds for the peoples benchmark (Zach, 13 Nov their goal is the|W-34]], [[W-35 The first peoples run Twin Hollows, Opus against Sonnet, 100 days|W-35]]) | DECISIONS [[D4-115 The peoples benchmark's worlds|D4-115]] cites it |
| feature_packages.md, generation_redesign.md, calibration_worlds.md | statuses accurate | no row in the outcome log (the README requires one per idea) | outcome log, lines 165-456 |

### 1c. "Design only" while built (statuses untouched since 23 to 29 Oct)

| Path | Decisions | Built in |
|---|---|---|
| forests.md | [[D2-156 A forest is three stocks|D2-156]] to [[D2-159 Shelter and fire are separate|D2-159]] | engine/forests.py, night.py, yields.py |
| visibility.md | [[D2-99 Visibility per place and sense|D2-99]] to [[D2-103 Visibility is computed, not stored|D2-103]] | engine/environment.py, fuse.py |
| children.md | [[D2-138 A child only by choice|D2-138]] to [[D2-152 Any two people of opposite sex at the same node can try for a c|D2-152]] | engine/life.py, night.py, verbs.py |
| verb_modifiers.md | [[D2-93 Modifiers on verbs|D2-93]], [[D2-94 for (D2-37) and the sowing method (D2-54) are modifiers|D2-94]], [[D2-111 leave folds into give|D2-111]], [[D2-112 Modifiers are techniques|D2-112]] | engine/modifiers.py (spec written) |
| hidden_ways.md | [[D2-90 Each edge end is tied to a side of the node and one or more parc|D2-90]] to [[D2-92 How hidden a way is follows its land|D2-92]], [[D2-98 Hidden ways are found by the noticing rule|D2-98]] | engine/here.py, layout.py, roads.py |
| journeys.md | [[D2-88 Traces left by passers|D2-88]], [[D2-97 Daily notices on the road|D2-97]] | engine/roads.py, signs.py |
| road_encounters.md | [[D2-81 Which events have a fuse in the first worlds|D2-81]], [[D2-104 Roads have stretches (one per day of the edge) and landmarks, k|D2-104]], [[D2-110 A meeting on the road is a fuse event with a short conversation|D2-110]] | engine/roads.py, fuse.py, settle.py |

Also: the outcome log lacks [[D2-229 One fish stock per water body|D2-229]] and a row for 9 proposals (calibration_worlds, economy_web, feature_packages,
generation_redesign, hunt_calibration, hunt_followups, livelihood_archetypes, model_households, standing_rules).

---

## 2. Session notes with plans: items that exist only in a note

Plans checked: 02zv §4-§6 (packs K0 to K12, W, X), 02zp §16-§17, 02zzl §1-§2, engine_overhaul.md phases with 38.64 §6 and §8,
feature_packages.md, 38.70 flaws, 38.71 §4, 38.76 Left, 38.78 §5, 38.79, 02zze, 02zzf, 02zzk, 02zzo §3, 02zzn, 38.50, 38.62, 38.68.

**Recorded (no action):** 02zv K3, K5 to K11 (OPEN [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] to [[L-124 Wildlife pack K11 lodgers of buildings|L-124]]), K4's rest ([[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]), core mechanisms ([[L-126 The wildlife's core mechanisms not built|L-126]]), K12 ([[L-103 Crafting and discovering new things|L-103]]),
§3.9 cuts and §6 ([[Q-32 02zv §6's decisions still open|Q-32]]); 02zp §16 ([[L-127 The ecology's calibration backlog|L-127]], mostly); 02zzl (environment_systems.md, [[D2-221 The land in three speeds|D2-221]] to [[D2-228 Calibrate across a distribution of worlds|D2-228]]); 38.64 §8 ([[L-72 Phase 2's open decisions|L-72]]) and phase
3's rest ([[L-73 Phase 3's rest|L-73]]); feature_packages ([[W-43 The engine as feature packages (Zach, 16 Nov) a dig into every co|W-43]], [[Q-48 The engine as feature packages|Q-48]] to [[Q-50 One grid or several|Q-50]]); 38.70 flaws ([[Q-43 Before the second peoples run|Q-43]]); 38.76 ([[W-56 One fish stock per water body, the engine half (D2-229; 37.2's ha|W-56]], [[L-116 The wild layer's fish and a water body, two ways|L-116]]); 02zzo §3 ([[Q-56 The land the engine reads|Q-56]]); 02zzk's "next"
rows ([[Q-47 The border for now|Q-47]] b, as one ask); 38.50 ([[D4-95 What a refusal says|D4-95]], [[D4-96 Using the store at home|D4-96]]); 38.62 §1 (phase 2, [[D4-103 The engine overhaul goes ahead, in phases|D4-103]]).

| # | Note | Planned item | Built? | Row? | Evidence |
|---|---|---|---|---|---|
| 1 | 38_space_engine/71_world_building_gaps.md §4 | 12 features for building worlds: a world brief with checks, a standard base profile, a first-year timeline check, a peoples cast generator, stores to the first harvest by default, calibration solved not searched, a competent-bot long dry run, a legibility check, a pre-run sheet for Zach | one part (1d3ee5c: a run warns when a standard setting is off) | none: [[W-38 Generation redesign the original pinned design against the built|W-38]] (Done) records only that the note was written | the same flaw recurred 16 Nov: e2fdee2 "the standard settings ... were missing, as in the first peoples run (38.70 flaw 5)" |
| 2 | 38_space_engine/78_runs_models_days0_7.md §5 | 16 engine and world issues: partnering open to youths and the already married; "grown" meaning 12 and 24 days; newcomers with no parentage; "a child called None"; Haiku 5.5 turns priced at $0.005; teaching log against results; Brook / Brook House collision; hide gating the rod; message and note caps; a perception glitch; thinking withheld | no | none in OPEN, WORK or BOARD | grep OPEN for parentage, already partnered, cost, teaching log = 0 |
| 3 | 38_space_engine/79_wording_probe.md | neutral wording ("Decide what to do") lengthens horizons in words, not acts; "only a paired run would show it" | no | no WORK row for the probe, no ask on the wording | 4fa3987 (17 Nov); grep WORK/OPEN "wording" = 0 |
| 4 | 37_growth/02zze_wild_region.md + [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]] | the live run's write-up against the null arm; engine gaps "no loans of goods", "hunting never killed"; publishing; "Open, for Zach" (3 questions) | run done ($75.01) | only [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]]'s text; no OPEN rows; the run lives in "37.2's scratchpad (live_region/)", not in the repository or the Hub | WORK [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]] |
| 5 | 37_growth/02zzf_generator_speed.md | six fixes, largest first (land and roads once, cheap tree sampling, coarser road grid, cheap checks first, parallel seeds, ladder once) | no | only a clause in [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]] | no commit on landgen since |
| 6 | proposals/engine_overhaul.md phase 4 (38.60 §6) | the larger experiment: the sophistication experiment, a fishing village against a farming village | no | none | grep OPEN/WORK "sophistication" = 0 |
| 7 | engine_overhaul.md phase 5; 02zzk "Fodder and draught" | beasts' feed (oats and hay for oxen and horses) | no | none (levels of fire [[L-46 Levels of fire|L-46]], needs [[L-23 Water as a need, and the land's hidden state (water table, wells,|L-23]], carts [[L-53 Transport and traders, built out|L-53]] are recorded) | grep "fodder" OPEN = 0 |
| 8 | engine_overhaul.md "Decided, unbuilt: fold in" | the periodic regime as one declared form; woods feeding game and forage ([[D2-156 A forest is three stocks|D2-156]]); drought drying dead wood | not as written | none | grep OPEN "periodic regime", "feeding game" = 0 |
| 9 | 38_space_engine/64_overhaul_breakdown.md §6 | where the engine is not general: crops and herds bespoke; the woods' three stocks by name; yield kinds a closed registry; work's food the same for every task; the walk not priced in choices | no | none (feature_packages touches the registry) | grep OPEN "registry", "work's food" = 0 |
| 10 | 37_growth/02zp_ecosystems_deep_dive.md §16 | two backlog items dropped from [[L-127 The ecology's calibration backlog|L-127]]: eras' effect on the ecology; crowding by body size | no | not in [[L-127 The ecology's calibration backlog|L-127]] | [[L-127 The ecology's calibration backlog|L-127]] text |
| 11 | 37_growth/02zv_wild_consolidation.md §4 X | the learning problems as coding categories (214); society-level tests (215) | no | none | grep OPEN = 0 |
| 12 | 02zv §4 W | world options W.1 to W.7 (forest law, rights in kinds, emparking, whales and swans, seeded structures, method-seeding arms, masked kinds) | no | only as "C14 world options" inside [[L-126 The wildlife's core mechanisms not built|L-126]] | [[L-126 The wildlife's core mechanisms not built|L-126]] |
| 13 | 37_growth/02zzl_environment_gaps.md §2 | mud slowing travel; human disease | no | not in environment_systems.md (disease only as old [[L-9 Disease (mortality, the sick, immunity, nursing, a healer); rot's|L-9]]) | grep environment_systems "mud" = 0 |
| 14 | docs/cybertron2/README.md, Files | `BUILD_PLAN.md` "to move here from 38.08"; `ARCHITECTURE.md` "when building starts" | never created | none | ls docs/cybertron2 |
| 15 | docs/fellows/projects.md ([[W-61 An introduction for the Vanderbilt AI Safety fellows' final proje|W-61]]) | the kit it promises: a pinned branch, templates, a world-file reference, a key checker, a starter notebook | no | only [[W-61 An introduction for the Vanderbilt AI Safety fellows' final proje|W-61]]'s text, a row marked "done" | WORK [[W-61 An introduction for the Vanderbilt AI Safety fellows' final proje|W-61]] |

---

## 3. Branches with commits not on main

30 refs on origin; 17 have nothing off main (4c-dry, 4c-hunt, 4c-pred, 4c-sets, climate-calibration, ecology, ecology-calibrate,
ecology-carcass, ecology-hunt2, ecology-hunt3, ecology-methods, ecology-raiders, peoples-worlds, use-by-physics, weather-by-place:
merged, never deleted). "Unique" counts commits on no other unmerged branch.

| Branch | Ahead | Unique | Last commit | WORK | OPEN | BOARD | Reading |
|---|---|---|---|---|---|---|---|
| runs-models | 59 | 9 | 64ab312, 17 Nov: world_checks: every craft a world gives can be done where its knower lives | [[W-58 The runs world with a model to each household (Zach, 17 Nov; prop|W-58]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 0 | 0 | the live run's engine; **lacks water-measure's fix (4a0a98f) and floodplains' salt house (1863003)**, so the paid run plays the double-counted water measure [[W-60 The ecology's water measure counted each lake and the large river|W-60]] said must not merge |
| floodplains | 46 | 1 | 1863003, 17 Nov: the salter gets a salt house with a brine pan | [[W-53 Floodplains in the generator now (D2-226) valley floors widening|W-53]], [[W-59 The runs world for the model-per-household run (Zach via 37.4, 17|W-59]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 3 | 1 | recorded |
| water-bodies | 44 | 0 | 594ba09, 17 Nov: the wild layer's fish follow the body's stock | [[W-56 One fish stock per water body, the engine half (D2-229; 37.2's ha|W-56]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 0 | 1 | in runs-models |
| lake-fixes | 42 | 0 | 47774a0, 17 Nov: the seven faults, fish on the rack, the signs pass | [[W-57 The lake runs' seven engine faults (38.75 a death told to one mem|W-57]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 0 | 0 | in runs-models; [[D4-122 Fish on the hearth rack|D4-122]] and the signs pass live only here |
| ecology-water | 36 | 1 | aae63d4, 17 Nov: the lake world with a graded population goal | [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]], [[W-55 The lake world with a graded population goal (Zach, 17 Nov), run|W-55]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 2 | 2 | recorded |
| water-measure | 34 | 1 | 4a0a98f, 16 Nov: the water measure counts each water once | [[W-60 The ecology's water measure counted each lake and the large river|W-60]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 0 | 0 | the fix is on this branch only |
| 5-fowl | 33 | 0 | 3e05709, 16 Nov | [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]], [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 0 | 0 | folded in |
| lake-on-mere | 32 | 0 | eda31a5, 16 Nov | [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] | 1 | 0 | folded in |
| 5-river | 29 | 0 | fe2c59b, 16 Nov | [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]] | 0 | 0 | folded in; not in [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]]'s list |
| 5-keep | 4 | 0 | c102502, 16 Nov | [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]] | 0 | 0 | folded in; not in [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]]'s list |
| water-worlds-2 | 3 | 3 | f15c41c, 16 Nov: land files out of git | **0** | **0** | 1 | **no WORK/OPEN record**; superseded (content taken into ecology-water as eb48f0f); not in [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] |
| water-worlds | 1 | 1 | cc6f38d, 16 Nov: brief 5's worlds | [[W-47 Brief 5's worlds and the runs-only world (Zach, 16 Nov design the|W-47]] | 0 | 2 | superseded (re-made as ed3069a); not in [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] |
| wip-weather-senses | 1 | 1 | cc43df4, 8 Nov: WIP (untested) weather read by the senses | **0** | **0** | **0** | **no record anywhere**; `git cherry` shows its patch is on main (graded sky signs, signs.py:587-595): stale |

---

## 4. WORK.md rows that contradict the repository

| Row | State as written | What is true | Evidence |
|---|---|---|---|
| [[W-2 Build briefs 2 and 3, the 20 dry test arms, the spring live run (w|W-2]] (37.4) | active, last 9 Nov; "Left: ... merging to `ecology` (Zach's go)" | merged to main 16 Nov; untouched 10 days | f290e2c, cc4d342 on main; [[W-36 Build brief 4c, then the merge of the wild layer (briefs 1 to 4c,|W-36]] |
| [[W-27 Build brief 4 (hunt_and_fixes.md, W-24) stage A the hunt over tim|W-27]] (37.4) | active, 10 Nov; "Left: Zach on [[Q-40 Brief 4 as built, and its gate|Q-40]]; merging" | merged; deviations deferred as [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]] | 58bb2d3 on main |
| [[W-30 Build brief 4b (hunt_followups.md) stage A wariness, the history|W-30]] (37.4) | waiting, 10 Nov; "Left: Zach on [[Q-41 Brief 4b as built, and its gate|Q-41]], the merge" | merged; [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]] | 8158674 on main |
| [[W-21 Proposals for Q-37 (a) and (d) graded damage to houses and camps|W-21]] (37.2) | waiting on [[Q-37 Brief 2 as built, and what its gate found|Q-37]] (a, d) | both proposals built in brief 4 stages B, C, on main | shelter_damage.md, cats.md History |
| [[W-22 Hunting against farming and gathering in generated worlds food pe|W-22]] (37.2) | waiting on Zach's go on 02zzd's changes | brief 4 was built on 02zzd's harness and merged | [[W-27 Build brief 4 (hunt_and_fixes.md, W-24) stage A the hunt over tim|W-27]] text; hunt_and_fixes.md History |
| [[W-34 Worlds for the peoples benchmark (Zach, 13 Nov their goal is the|W-34]] (37.4), first row | active, 13 Nov; "Left: Zach's go and models for the first runs" | the first run is done ([[W-35 The first peoples run Twin Hollows, Opus against Sonnet, 100 days|W-35]], 13 Nov); worlds on main (e54c722) | [[W-35 The first peoples run Twin Hollows, Opus against Sonnet, 100 days|W-35]], [[W-36 Build brief 4c, then the merge of the wild layer (briefs 1 to 4c,|W-36]] |
| [[W-34 Worlds for the peoples benchmark (Zach, 13 Nov their goal is the|W-34]] (37.4), second row | active, "started"; file "69_peoples_benchmark.md (to come)" | a stale duplicate; the note is 69_peoples_worlds.md | ls 38_space_engine |
| [[W-61 An introduction for the Vanderbilt AI Safety fellows' final proje|W-61]] (lead) | "done", in the In progress table | should be in Done; the kit it promises is unbuilt | WORK.md line 29 |
| [[W-28 The Cybertron 2 website home, runs page, run explorer with each d|W-28]] (site) | waiting, last touched 10 Nov | c2viz site commits 13 to 17 Nov (7851f07, af13642, 1bdb2a2, 4478365) | git log c2viz |
| [[W-58 The runs world with a model to each household (Zach, 17 Nov; prop|W-58]] (37.4) | the run "24 days" | the world is 100 days (a2ad706); runs on a branch without [[W-60 The ecology's water measure counted each lake and the large river|W-60]]'s fix | section 3 |
| [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]] (37.4) | active, 16 Nov | built and gated; left only Zach's answers ([[Q-53 Brief 5 as built|Q-53]]): waiting | its own text |
| [[W-56 One fish stock per water body, the engine half (D2-229; 37.2's ha|W-56]], [[W-57 The lake runs' seven engine faults (38.75 a death told to one mem|W-57]] (37.4) | active, 17 Nov | built and pushed; left only "Zach's merge": waiting (now [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]]) | their own text |
| [[W-4 wild_behaviour.md v3 (the per-kind designs, from 02zv, 02zw and th|W-4]] (37.2) | waiting on [[Q-32 02zv §6's decisions still open|Q-32]] | [[Q-32 02zv §6's decisions still open|Q-32]] (1), (2) overtaken: brief 5 built K4, later packs deferred 19 Nov (69c0023) | OPEN [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] to [[L-126 The wildlife's core mechanisms not built|L-126]] |
| [[W-5 37.2's own hygiene items D2-199 to D2-203 into the spec; the scrat|W-5]] (37.2) | queued 9 Nov | not begun 10 days; [[D2-200 Wild plant kinds replace the single plants stock in worlds with|D2-200]] to [[D2-203 Each wild kind's behaviour is designed first, then built as a m|D2-203]] still in no spec file | hygiene §1 |
| [[W-3 Records restructure WORK.md, OPEN.md's kinds, CLAUDE.md's rule, hy|W-3]] (37.2) | active 9 Nov | untouched 10 days | hygiene §10 |
| [[W-31 Goal probe, round 3 (Zach, 12 Nov) resource (salt, copper, timber|W-31]] (37.4) | active 12 Nov | untouched 7 days | hygiene §10 |
| [[W-8 Couple the food web to 37.4's weather and climate|W-8]] (37.2) | paused; "check after [[W-2 Build briefs 2 and 3, the 20 dry test arms, the spring live run (w|W-2]]" | [[W-2 Build briefs 2 and 3, the 20 dry test arms, the spring live run (w|W-2]] has merged | above |
| [[W-12 Forays (proposalsforays.md) the design's open questions; building|W-12]] (37.2) | paused | deferred by Zach ([[L-105 Forays as their own track|L-105]]): belongs in Done as deferred | WORK rules |
| [[W-14 Claims and ownership by physics, part 2 (proposalsuse_by_physics|W-14]] (37.4) | "waiting", in the Paused table | a state that contradicts its table | WORK.md |
| [[W-37 Standing rules how a household eats and what it keeps back, with|W-37]], [[W-38 Generation redesign the original pinned design against the built|W-38]] | states "discussion", "ready for a decision" | not states WORK.md allows (active, waiting, queued, paused) | WORK.md header |
| [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]] (37.2) | waiting | the run's data is in a scratchpad, not the repository or the Hub | its own text |

**Duplicate numbers:** [[W-28 The Cybertron 2 website home, runs page, run explorer with each d|W-28]] (website, in progress; brief 4b written, done), [[W-34 Worlds for the peoples benchmark (Zach, 13 Nov their goal is the|W-34]] (two in-progress rows), [[W-38 Generation redesign the original pinned design against the built|W-38]] (generation redesign,
c2viz; world-building gaps, 37.4, done), [[W-39 The economy's layers and trees of dependence across the domains (|W-39]] (economy layers, 37.2; peoplegen prototype, c2viz, done). [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]] was reused once and
repaired (6702cd7, 752209a). No gaps in [[W-1 Build brief 1 general methods (D2-204, D2-207); branch ecology-met|W-1]] to [[W-63 An audit of what was started and left (Zach, 19 Nov what differen|W-63]].

**Initiatives with no WORK row:** livelihood_archetypes.md (37.4, 16 Nov), the 38.79 wording probe (37.4, 17 Nov).

---

## 5. Hygiene (`python3 tools/hygiene.py --all`, 19 Nov; 358 decisions)

Header: 31 in progress, 9 paused, 50 asks, 88 deferred, 176 chores. Its size log was last recorded 16 Nov (26 in progress).

| § | Check | Count | By session |
|---|---|---|---|
| 1 | Decisions cited in no spec file | 51 | 37.2: 33 ([[D2-44 Bread|D2-44]] to [[D2-231 The runs world's runs on set nights|D2-231]]; the generator's [[D2-173 The generator fills in around what a world file gives|D2-173]] to [[D2-191 The generator designs within one envelope temperate oceanic, lo|D2-191]] alone 17, = [[W-9 Compile the generator into specworldgeneration.md (OPEN L-101)|W-9]]/[[L-101 Compile the generator into specworldgeneration.md|L-101]]); 37.4: 18 ([[D4-38 The farming stages' work and returns are 02l §2's|D4-38]] to [[D4-121 A fishing household in the water worlds (a stopgap)|D4-121]]) |
| 2 | Replaced decisions not marked | 26 | older row is D2: 14, D4: 12 (DECISIONS' editor is 37.4) |
| 3 | Spec files behind or old (14 to 27 days) | 42 | 37.4 areas 26 (agents 6, information 6, world 5, conflict 3, core 2, institutions, life, measurement, seeding 1 each); 37.2 10 (economy 8, environment 2); 37.1 6 (record) |
| 4 | Proposals stale or unindexed | 18 | 37.2: 9 (cats, economy_web, ecosystems, environment_state, husbandry, living_populations, node_ecology, shelter_damage, water_and_preservation); 37.4: 7 (law, phase3, livelihood_archetypes x2, model_households, standing_rules x2); lead: feature_packages; c2viz: generation_redesign |
| 5 | OPEN.md | 90 | 23 done but not struck; 28 deferred with no date; 35 dated and still open; 4 spec write-ups owed ([[L-31 D4-79's rules (the weekly usage stop, llm.week_stop, STOPPED.md;|L-31]], [[L-32 D4-83 (a fire under no roof in the night's weather fuel by weathe|L-32]], [[L-44 D4-93 (one room, one fire a hearth and a ring burn as one; the he|L-44]], [[L-101 Compile the generator into specworldgeneration.md|L-101]]). Owners: 37.4 about 36, 37.2 about 37, joint the rest |
| 6 | Paths into a scratchpad | 5 | 37.2: 3 (02zp sim.py, 02zzd eco_trace_note.py, 02zzj RESEARCH_BRIEF.md); 37.4: 2 (79_wording_probe) |
| 7 | Dates after today | 1 | 37.4: model_households.md:114 ("30 Nov") |
| 8 | Links to missing files | 4 | 37.2: spec/economy/agreements.md, proposals/agreements.md, exchange_and_money.md (x2) |
| 9 | Board | 1 | last post 17 Nov, though [[W-62 The water work is on eight unmerged branches, none on main ecolog|W-62]] (19 Nov) is a cross-session merge |
| 10 | WORK rows stale | 18 | 37.2: 10 ([[W-3 Records restructure WORK.md, OPEN.md's kinds, CLAUDE.md's rule, hy|W-3]], [[W-4 wild_behaviour.md v3 (the per-kind designs, from 02zv, 02zw and th|W-4]], [[W-5 37.2's own hygiene items D2-199 to D2-203 into the spec; the scrat|W-5]], [[W-9 Compile the generator into specworldgeneration.md (OPEN L-101)|W-9]], [[W-10 37.2's spec write-ups owed since 2 and 3 Nov (OPEN L-32, L-44, L-|W-10]], [[W-11 Landscapes still to tune (OPEN L-100); the generator's _spread re|W-11]], [[W-21 Proposals for Q-37 (a) and (d) graded damage to houses and camps|W-21]], [[W-22 Hunting against farming and gathering in generated worlds food pe|W-22]], [[W-29 A multi-village wild region and its live run (Zach, 10 Nov) four|W-29]], [[W-39 The economy's layers and trees of dependence across the domains (|W-39]]); 37.4: 6 ([[W-2 Build briefs 2 and 3, the 20 dry test arms, the spring live run (w|W-2]], [[W-27 Build brief 4 (hunt_and_fixes.md, W-24) stage A the hunt over tim|W-27]], [[W-30 Build brief 4b (hunt_followups.md) stage A wariness, the history|W-30]], [[W-31 Goal probe, round 3 (Zach, 12 Nov) resource (salt, copper, timber|W-31]], [[W-34 Worlds for the peoples benchmark (Zach, 13 Nov their goal is the|W-34]] x2); joint: [[W-25 The world keeps its land (D2-208) the generator writes land.npz w|W-25]]; site: [[W-28 The Cybertron 2 website home, runs page, run explorer with each d|W-28]] |
| 11 | Asks unanswered, deferred rows with no trigger | 29 | 17 asks 4 to 27 days old ([[Q-18 D2-74 amends D4-35 informationsigns.md and perception need the cr|Q-18]] to [[Q-47 The border for now|Q-47]]), 16 undated asks, 11 deferred rows with no "waits on" |

**What hygiene does not see** (found above): proposals saying "not built" while the code is on main (17); built work with no
decision row (briefs 4, 4b, 4c, the signs pass, model_households, shelter_damage, cats); branches ahead of main with no record;
a live run on a branch missing a known fix; duplicate W numbers; "done" rows in progress; non-states; WORK "last touched" older
than the commits; plan lists in session notes; deferred rows whose trigger has arrived ([[L-2 Scavengers, with wild animals that attack herds and hunters and ar|L-2]] "waits on wild animals as a system"
and [[L-37 Wildlife by terrain|L-37]] "wildlife by terrain", both built on main since 16 Nov; [[L-100 Landscapes still to tune|L-100]]'s floodplains, built on `floodplains`); citations of
commits that do not exist (f58764f).

