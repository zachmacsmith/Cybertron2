# Stage 1 of the fishing, hunting and materials wave: the basis in code (report)

23 Nov 2026, 37.2 (build subagent). Thread W-97, under the wave's integrated design (W-85). Branch `w85-s1-basis` (from `main` at
f6b31459), not pushed, not merged. Spec: `docs/cybertron2/proposals/w73_design/u0_basis.md`, with the parts of u1, u2, u3, u7 and u8
it points to, each read under its "Decisions since" table. No model calls, no live runs, no Hugging Face; bots for interfaces only
(D2-298).

## In brief

- **Built, in the spec's order:** the faults that mislead (the options list gone, the fishing faults of u2 §6 but fault 12, a run's
  fish learning no wariness, the weir's cost in one place at D2-302's numbers, practice for every build act, the five directing
  signs reworded); the clocks (`CAPITAL` and the conversions); the 1-unit floor and the batches; a build act costing what is left
  (D2-324); the keeping curve's base rates and the cured depths as goods; fuel a night at its real weight; the goods in handling
  units with the recipes, rooms and fittings in kilograms.
- **Tests:** before, 727 passed and 2 skipped; after, 748 passed and 2 skipped (21 new, in `tests/test_cybertron2_stage1_basis.py`).
  Twenty test files had numbers or words the decisions replaced; each is listed below with why.
- **Bots:** the runs world (`runs_high`) runs with `--bots runs` for 12 days before and after, no errors; a 40-day run after the
  change reaches the autumn run (below).
- **Not done, and why:** fault 12 (set gear held in hand) and the full set and tend waits for u3's gear (stage 2); the stores'
  multipliers and named penalties are u5's (stage 3); fences, walls, clearing and terraces keep today's materials until their
  stage-5 companions. Each is listed under "Not done".

## 1. What was built, by file

| File | What changed |
|---|---|
| `engine/prompt.py` | the "Your crafts today" block no longer computes or shows "Today you could" or "Not yet" (D2-286); the crafts known stay, after the opening. The rule line on stores reads the new base rate |
| `engine/knowledge.py` | `options` removed; `doable` gives the scripted bots their candidates (never shown to a person); `ready` lets a run technique take a run where no resident fish live (Q-79 bug 1) |
| `engine/run.py` | `bot_plan` reads `knowledge.doable` |
| `engine/verbs.py` | the run's take where the stock is missing or fished out; a set technique named alone tends one's own standing gear, and `set {"what": snares | trap in water, "at"}` lays a new set; another's set emptied is theft (worded, recorded); the weir's crew may build under one who knows it; the weir's cost read from `wild/gear.py` by its water; `cost`: no act under the floor is free, a make of `qty` pieces costs act units x ceil(qty / batch); `_make` makes up to its batch an act; a build act costs what is left at one's skill, 1 or 2 units, and practises its units (`build_units`, `_build_act`); the fell's brash a quarter of its mass |
| `engine/here.py` | a place's own name never reaches a house; a household's house only as "the Brooks", "Brooks", "Brook's" or "Brook House"; new reads for the verbs (`run_here`, `owns_set`, `own_set_at`, `weir_water`, `mind`) so verbs and knowledge read no world state (D4-35) |
| `engine/things.py` | `owns_set` counts the household's (D2-305); unnamed set words reach only one's own; set lines carry their tag |
| `engine/settle.py` | a theft from a set is seen or not by the one rule (`_set_theft_seen`) |
| `engine/wild.py` | `run_here`; the hunt's wariness and pressure on the resident share only, a head met drawn as resident or of the run before its flight (u1 §7a); the net's own words; set gear and the edge on water read the water's notice rows, never the wood's; the set line names its tag and how it is tended |
| `wild/kinds.py` | `flies` and `swims` traits; the water's (empty) notice group; four sign rows reworded |
| `wild/methods.py` | the net needs `flies`; snares land only; den work reaches the otter's holt |
| `wild/gear.py` | `cost(j, material, foot, water)` and `upgrade_cost` from D2-302's table; `water_x` |
| `engine/signs.py` | the crop row reworded |
| `engine/clocks.py` | `capital_factor`, `held`, `piece_units`, `capital_units(row, w, n=1)`, `batch_of`, `act_units`, `capital_life`, `night_life`; RATES names `hours` and `uses` as the capital clock |
| `engine/data.py` | `CAPITAL`; `WORK_HOURS` (u7 §2's real hours) and a class on every room, fitting and monument row; gear rows' `hours`; the bulk processes' `batch`; the weir's cost in `WATER_WORKS`, MONUMENTS reading it; `withies` and `cut withies`; `KEEP_DAYS` and the keeping curve; the four cured goods; weights, heats, recipes, rooms, fittings, forests, stores, carrying and fuel in the handling units |
| `engine/buildings.py` | stores of a kind in `STORES["by_weight"]` hold kilograms (the woodshed); goods in `STORES["stack"]` take less free floor (`_floor_weight`) |
| `engine/forests.py` | an older world's trees read in the new unit |
| `engine/bots_livelihood.py` | the trap setter lays each trap with `set` |

Each piece sits with its unit (D2-244): placed gear (verbs `_tend`, `_own_set_at`, `set {what}`; things; settle's theft; wild's set
line), the run's take (wild `run_here`, knowledge `ready`, verbs), the clocks (`clocks.py`, data `CAPITAL`), the keeping curve
(data `KEEP_DAYS`, `keep_nights`, `base_spoil`).

## 2. Each fault fixed, with its test

All new tests are in `tests/test_cybertron2_stage1_basis.py` unless named.

| Fault | Fix | Test |
|---|---|---|
| the options list (D2-286) | removed from `prompt.turn_prompt` and `knowledge`; the beliefs view's fallback at no place calls that prompt, so no world shows it | `test_no_prompt_contains_the_options_list` (and `test_cybertron2_view.py` as before) |
| 1: the edge refused at a run with no resident fish | `ready` passes a run technique where a run passes today; the act takes the run alone and says so | `test_the_edge_reaches_a_run_where_the_water_holds_no_resident_fish` |
| 2: setting mistaken for lifting | a set technique named alone tends one's own standing there (catch to hand, set again); `set {"what"}` lays anew | `test_the_technique_named_alone_tends_what_stands` |
| 3: nets met 48 salmon and took none | the net needs `flies`; a run's fish learn no wariness (u1 §7a) | `test_the_fowling_net_meets_no_fish`, `test_a_runs_fish_learn_no_wariness` (fails on the old `wild.py`) |
| 4: the weir known to everyone | MONUMENTS weir not basic; its crew may work on it, and on its parts, under one who knows it | `test_the_weir_is_not_everyones_craft`; `test_the_weir_is_crew_work...` (updated) |
| 5: "the Brook" read as Brook House | a parcel's own name returns no building; a household's house only by plural, possessive or "House" | `test_a_place_named_like_a_household_is_the_place` |
| 6: "take from my snares" emptied a neighbour's | unnamed set words reach only one's own (the household's included) | `test_unnamed_acts_touch_only_ones_own_and_anothers_set_is_named_theft` |
| 7: no theft wording on another's set | worded as theft, recorded in `today["thefts"]` with the thing, seen or not by the one rule | the same test |
| 8: tags not shown | the set line carries its tag | `test_ones_own_sets_are_listed_with_their_tags` |
| 11: the net's result "You hunted" | the net's own words ("You spread your nets ...") | in `test_a_runs_fish_learn_no_wariness` |
| 14: snares at the water took otters | snares land only (`water: False`); den work at the holt | `test_snares_meet_no_otters_and_den_work_reaches_the_holt` |
| 15: water acts turned up wood finds | the hunt's group becomes the water's (no rows yet) on water, fen and saltmarsh | `test_a_trap_set_turns_up_no_antler` |
| the weir's cost held twice | one copy in `WATER_WORKS["weir"]["cost"]` at D2-302's numbers | `test_a_sections_cost_is_its_materials...` (`test_cybertron2_water_fixes.py`, rewritten) |
| sub-unit recipes free | the floor in `cost`; batches | `test_a_make_of_n_pieces_costs_units_by_its_batch_and_no_act_is_free` |
| the five directing signs | reworded as u8 §4 gives | `test_the_five_signs_that_directed_acts_are_observations` |
| the build's practice counted once a work | every build act (new building, room, rebuild, tier, fitting, weir part) practises its units | `test_a_build_act_costs_what_is_left_and_every_act_practises` |

## 3. The numbers changed

**The clocks.** `CAPITAL`: factor "1/15", real year 2,700 h, `hold` rooms, fittings, monuments, weir, fences, clearing, works; floor
1. "world" is 1/7.03 in a 32-day world. Real hours on the rooms (wattle small room 405, timber 585, stone 945; medium 1,035 and
1,665; hall 5,850 and 8,100), the fittings (u7 §2.2's middles) and the carved post and cairn; all held at today's units (D2-309).
Gear at the factor from the start: fishing rod 1.5 h (up to 20 a unit at 1/15), crude tool 7 (up to 4), copper tool 6 (4), crude
weapon 3 (10), bedroll 3 (10), tent 9 (3), plough 36 (1 unit), handcart 50 (2 units), harness 13.5 (2 units at 1/15: 1).

**The floor and the batches.** Every act at least 1 unit; a build act 1 or 2 by what is left (D2-324). Up to their batch: grind,
mill, water mill (the 200-grain least gone), bread, oven bread, salting, dry fodder, leaching, charcoal, cheese. Salt fish 40 fish
and 10 salt a unit (was 4 and 1), salt meat 40 and 5 (D2-283); dry fodder 30 green to 1 hay (was 10 to 8); cheese 20 milk and 0.6
salt to 3.3 (was 6 and 0.2 to 1); charcoal 1 unit (was 2); bread 10 flour and 0.5 firewood in 2 units (was 1 timber, 1 unit); oven
bread 100 flour and 3 firewood in 4 units (was 4 timber, 3 units).

**The weir (D2-302).** Wattle first section 20 timber, 10 withies, 12 units (was 12 timber, 24 units); added wattle 8, 5, 6 (was
6 timber, 16); timber first 40 timber, 20 units (was 16, 33); added timber 15, 10 (was 10, 25); x0.3 on a beck, x2.5 on a large
river; a level's mend 0.03 of the section's build (was 0.06), which puts the measured year's upkeep on the runs world's river at
0.23 of a wattle section and 0.12 of a timber one: D2-302's quarter and eighth.

**The keeping curve (D2-289).** A quarter lost by min(d, 2) + (d − 2) / 11.4 nights: fresh fish 0.175 (was 0.30), fresh meat 0.129
(0.30), hot-smoked fish and meat 0.111 (new), bread 0.119 (0.05), milk 0.25 (1.0), smoked fish and meat 0.029 (0.005), cheese 0.023
(0.02), hard-cured fish 0.011 (new), salt fish and meat 0.0085 (0.01, 0.003), hard-cured meat 0.0085 (new), dried fish and meat
0.0069 (0.02), grain, rye and beans 0.0013 (0.0167), hay and straw 0.0007 (0); the rest by wave1 §2.2's real days. Lots in the smoke
0.12 out of it, 0.03 in it (was 0.15, and 0.011 in the smoke). `house_spoil` 1.0 (was 0.3): the base is the well-kept rate
(D2-272). Fresh fish's store x2 dropped (its base holds it, wave1 §2.3).

**The cured goods (D2-295).** Hot-smoked fish 0.69 food a kg, hot-smoked meat 0.9, hard-cured fish 1.15, hard-cured meat 0.71.

**Fuel a night (D2-290).** A house 0.5 heat a normal night (a 10 kg bundle) and 1.5 a cold one (was 1 and 4); a camp 1.0 (2), the
open 1.5 (4). Timber 1.25 heat (was 2), charcoal 2.0 (6), firewood 0.5.

**Weights (D2-288; wave1 §1).** Timber 25 (was 2), stone 25 (3), firewood 10 (1), straw 16 (1), hay 10 (1), charcoal 20 (2),
withies 10 (new), bread 1.4 (1); hide 3, crude and copper tools and the crude weapon 1.5, fishing rod 0.8, plough 25 (4), harness 12
(1), bedroll 3 (1), tent 18 (6), antler 1.5, beaver pelt 0.7, hen 2, cat 3.5. The pack read as the pack basket: +15 kg (was +10);
the handcart 125 kg in all on a track (was 40); a pack ox 100 (60).

**Recipes in kg.** Crude tool 0.04 timber and 0.04 stone (was 1 and 0.5); crude weapon 0.06 timber (1); copper tool 1 copper and
0.02 timber (0.5); fishing rod 0.1 withies (0.5 timber, 0.1 hide); pack basket 0.4 withies and 0.1 hide (1 hide, 1 timber);
handcart 2 timber (6); plough 1.2 timber and 1 copper (4 timber); harness 0.4 timber and 0.5 hide as rawhide (2 and 1); bedroll 0.5
hide (1); tent 1.5 hide and 0.4 timber (3 and 2); clappers 0.04 timber (0.5); smelting 1 charcoal or 6 timber (4); relining an oven 4
stone (2); a slaughtered cow 3.5 hide, an ox or bull 4 (2).

**Rooms and fittings (u7 §2).** Small room: wattle 36 timber and 35 withies (was 8 timber; the roof at the site, D2-328), timber 160
timber, 60 stone, 15 withies, 75 straw (8 and 2), stone 1,600 stone, 40 timber, 75 straw (30 and 4); medium room: timber 270, 100,
25, 130 (15 and 4), stone 2,700, 70, 130 (60 and 8); hall: timber 560, 210, 50, 260 (80 and 20), stone 5,600, 140, 260 (150 and
20). Fittings: beds 1 timber and 1 straw (1 and 2), hearth 20 stone (4), fire ring 4 stone (1), owl hole 0.1 timber (1), granary 20
timber (6), oven 60 stone and 0.4 timber (20 and 2), anvil 4 stone, 2 hide, 0.4 timber (6, 2, 1), cellar 9 timber, timber-lined
(was 4 stone), millstones 60 stone (10), water wheel 300 timber, 140 stone, 2 copper (60, 20, 2), stalls 2 timber (1), woodshed 20
timber and 15 straw (2 timber), smoke racks 2 withies and 2 timber (2 timber), brine pan 10 copper and 4 stone (1 copper and 2
timber), vault 3,000 stone (40). Standing stone 60 stone (4); the cairn's stones got on the spot (D2-306). Units held.

**Getting (basis §1).** Fell 8 timber an act of 2 units, 4 a unit (was 3 an act); quarry 8 an act (2); hay 7 a unit (3); cut
withies 1.5 a unit with a crude tool, by the season (new).

**Forests and stores.** Forest kinds' trees x9.6, young growth and dead wood x6 (wave1 §1.8); a world file's old counts converted
by `spec_unit` (wood 9.6, young and dead 6); per timber 2.5 bundles (4); brash 0.625 (1). The woodshed holds 9,600 kg of timber,
firewood and charcoal by weight (was 40 timber). Free floor stays 30 kg a space loose; fuel, timber and charcoal stack at 300 kg a
space, hay, straw and stone at 1,000 (STORES `stack`, W-97's default; storage.md §3.10 for hay). A lean-to keeps 30 (was 10).

## 4. Tests updated, and why

| File | What and why |
|---|---|
| `test_cybertron2_package_a.py` | the bury test reads `knowledge.doable` (the options list gone); grain in the open wet at ten times its new base |
| `test_cybertron2_wild_sets4c.py` | a stranger's take from another's snares is worded as theft (fault 7); the set line carries its tag (fault 8) |
| `test_cybertron2_water5_river.py` | the weir's builder knows it (fault 4); another household's member robs the weir (D2-305); the held salmon taken by hand, not net (fault 3); the otter at its holt, not in snares (fault 14); the weir's parts and mend at D2-302's cost by the water; the year's upkeep band a quarter and an eighth; fresh fish against meat by their base rates (the store's x2 dropped) |
| `test_cybertron2_water_fixes.py` | the weir's cost table rewritten to D2-302; a section built and upgraded at the new cost by the water; the full weir's year between an eighth and a quarter |
| `test_cybertron2_buildings.py` | the test stock in the new units; an added room's kg; a fine tier's 54 timber; bread "takes up to 10 flour" (a batch); the hall and the water mill in D2-166's 300 to 500 units in all (renamed); 9.9 units left after the first act's practice |
| `test_cybertron2_engine.py` | a wattle room's 36 timber and 35 withies; travel refused with one 25 kg timber |
| `test_cybertron2_switches.py` | traps laid anew with `set` each day (named alone they are tended) |
| `test_cybertron2_water5_keep.py` | the keeping order by the curve (was smoke x4 dried meat); a smoked batch's loss at 0.03 a night; salting at 40 kg a unit and the salt fish's new base |
| `test_cybertron2_wild_hunt2.py` | a lone hunter carries 6 to 10 food with a 3 kg hide |
| `test_cybertron2_hollins.py`, `test_cybertron2_region_c.py` | the woods' timber felled to the end, x9.6; the merchant without his cart is refused 80 grain and carries it with the ox (100) |
| `test_cybertron2_hollins2.py` | Ockley's woods now keep far more than its people (food binds; was heat at about two thirds) |
| `test_cybertron2_package_c.py` | the pack ox carries 100 (renamed) |
| `test_cybertron2_act_fixes.py`, `test_cybertron2_farm.py`, `test_cybertron2_heap_senses.py`, `test_cybertron2_package_f.py` | fuel a night and heat by mass (1.5 heat in the open, 0.5 a house's night, charcoal 2, timber 1.25); smelting on 6 timber; the oven's materials; the copse's stocks, its year's firewood (108 bundles) and fell's 8 timber; the small village's heat bound (199.5 people, from 14) |
| `test_cybertron2_fittings_ground.py` | the Green's spaces: Hobb House is seeded a room larger, its fuel and timber now weighing what they do |
| `test_cybertron2_capacity.py` | the four cured goods have no source until u4's processes (stage 3) |
| `test_cybertron2_dry4c.py` | the rack's loss at 0.03 a night (summer x1.5) and the morning lines' quantities that follow |
| `test_cybertron2_wild_calibrate.py` | salt meat's batch |
| `test_cybertron2_wild_range4c.py` | the golden digest re-pinned (the stores and the dead hold different goods; the hunt itself is unchanged for kinds with no run) |

## 5. Spec drift found

- **Lines moved, intent followed:** `data.py:346` (the weir's `basic`) is now near 364; WATER_WORKS 376 to 390 near 367 to 400;
  `things.py:394-411` (`set_line`) is 386 to 402; `verbs.py:1670-1676` (the store's theft path) near 1690; `kinds.py:890` and `:894`
  are 892 and 896; `wild.py:2341-2438` (the hunt) a few lines on. The rest matched.
- **The free sub-unit recipes (E6):** no technique in today's data has fractional units, so `int()` in `cost` made nothing free yet;
  the floor matters for the rows with real hours, which this stage adds.
- **Milk:** the curve gives 0.25 a night (keeps a day); D2-42 had it gone the same day (1.0). D2-289 reads as replacing it; worth
  Zach's word.
- **Hard-cured meat:** u4's table says 0.67 food a kg, its binding table 0.71; 0.71 is built.
- **The brine pan:** today's 1 copper and 2 timber against u7 §2.2's 10 copper and 4 stone (wave1 contradiction 23); u7's built.
- **The weir's withies:** D2-302 needs withies, and nothing in the engine made them. A bridge, `cut withies` from young growth at
  u3 §1.1's wild rate, stands until u3's willow stock and withy bed (stage 2). Mending a wattle section now takes a withy too.
- **The shown recipe in the travel line** said the pack ox carries 60: now 100. The world generators' lore lines
  (`specs/make_ladder.py`, `specs/make_wild_region.py`) still say 60; not regenerated.
- **Stores below base:** with `house_spoil` 1.0 the fittings' spoil multipliers (bins 0.5, granary 0.2, cellar 0.25) still slow
  food below its base rate, against D2-272, until u5 takes them out (stage 3).
- **Golden journals and prompt snapshots:** none are kept in the repository's tests to re-take; the one golden digest
  (`test_cybertron2_wild_range4c.py`) is re-pinned.

## 6. Not done, and why

- **Fault 12 (set gear from hands) and the rest of set and tend on held gear:** it needs the wicker trap, snares and nets as goods,
  made (u3) and seeded (u11); the build plan puts it in stage 2. This stage tends one's own gear when the technique is named alone and
  lays more with `set {"what"}`, so a person's capacity of traps is as before.
- **Stores' named penalties and the removal of their multipliers (u5):** stage 3.
- **Fences, walls, clearing, terraces, the burial cairn:** their materials stay in today's counts. Their kilograms come by length
  along a border (D2-322) with material got at the site (D2-306), both stage 5; at u7 §2.3's figures for a round fence (317 withies,
  74 timber) or a wall (4,000 to 8,000 stone a 100 m) fields could not be fenced before those companions (D2-309's reason for the hold).
- **Lives:** `capital_life` and `night_life` exist; the items' lives are not yet converted (u3 §3, stage 2).
- **Build techniques' units** are still copied at import (`data.py`); `buildings.room_cost` and the rest do not yet read
  `capital_units`. Every class is held, so the units are the same; the switch belongs with the release of the hold (stage 5).
- **u7's other stage-1 items** (the act log, removing the dead `PHYSICS.cattle.stray`) are not built.
- **The wild's day-clock rates** stay as calibrated (D2-315); **the kill's hide by weight** waits for `dress a kill` (u3, stage 2);
  bins and cellar holds in kilograms wait for u5; coin's weight is left at 0.

## 7. Results

**Tests (`python3 -m pytest -q tests`, run in four shards):** before (f6b31459) 727 passed, 2 skipped; after (7904f6a3, then this
report) 748 passed, 2 skipped.

**Bots:** `python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml --bots runs --days 12` before and after: 11
alive each day, no errors, the same seeded death on day 1; the refusals seen are the salters' salt short ("it takes up to 10
salt": the batch's words). Forty days, before and after, to take in the autumn run and the winter: no errors in either; after, the
bots laid 572 sets with `set {"what": "trap in water"}` and lifted the weir's traps 30 times; the refusals are the season's (nothing in
season to gather), the salters' salt, and a repair short of timber. Both arms end at 5 alive on day 40 with the deaths in the late
winter (before from day 34, after from day 31). The bots decide nothing beyond their policy, so this is read as the interfaces working,
not as evidence about the world (D2-298); the live runs carry that signal.
