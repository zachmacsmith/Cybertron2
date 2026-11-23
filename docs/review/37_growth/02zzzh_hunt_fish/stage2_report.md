# Stage 2 of the fishing, hunting and materials wave: taking and making (report)

23 Nov 2026, 37.2 (build subagent). Thread W-98, under the wave's integrated design (W-85). Branch `w85-s2-taking` (from `main` at
26cc29aa, after stage 1 merged), not pushed, not merged. Specs: `docs/cybertron2/proposals/w73_design/u1_water.md`, `u2_taking.md`,
`u3_making.md`, each read under its "Decisions since" table; basis.md, integration.md, build_plan.md stage 2; stage 1's report. No
model calls, no live runs, no Hugging Face; bots for interfaces only (D2-298).

## In brief

- **Built:** gear as goods with two lives, one piece record for made and placed gear (u3 §3; basis §6); set from the hands and tend
  (u2 §3; fault 12; D2-294, D2-304, D2-305); the gill net and the set line as set gear; the wave's recipes in real kilograms at real
  hours with their batch (u3 §2.2); mending; lives in nights at 32/365 and in acts at the factor (D2-310), nets about 16 nights in
  the water (D2-329); the craft lines by level (D2-263); the shallows per parcel by water type with their own signs (D2-316,
  D2-317); the ice (u1 §4, to revisit with the environment, L-161); the fen's reach and wreck, the pinch, the edge on the shallows
  (u1 §5, §6); wild willow in place of stage 1's bridging `cut withies` (u3 §1.1); twist cord; the flax strip (B35, default: up to a
  quarter of a plot); D2-304's named target for a consuming act; the water-only runs world (D2-316) with D2-330's C5 gear; the
  making gate check M1 to M8 as a function, run on the current worlds.
- **Out, as decided:** fowling (D2-318: the `net` method untouched); leather, tanning, bark and barking (D2-327, D2-329).
- **Tests:** before (26cc29aa) 748 passed, 2 skipped; after 784 passed, 2 skipped (35 new in
  `tests/test_cybertron2_stage2_taking.py`, one new in `tests/test_bots_livelihood.py`). Eleven test files pinned the replaced
  interface or numbers; each is listed in §4.
- **Bots:** `runs_high` with `--bots runs` for 40 days runs with no errors; the fishers set 33 settings of traps from their hands,
  tended 97 times, made traps 23 times and cut withies 35 times as floods tore traps away (30 losses reported in the tends), the
  weir's expert set and tended the gill net, and pieces wore by the nights to broken and were brought home to mend (§7).

## 1. What was built, by file

Each piece sits with its feature unit (D2-244): new code in new modules, the old files touched at the seams.

| File | What changed |
|---|---|
| `engine/gear.py` (new; the gear unit) | data: the wave's goods and gear in kg (`ITEMS`), the recipes at real hours and their class (`RECIPES`), lives by thing (`LIVES`), the older tools' lives (`TOOL_LIVES`); `register_items` / `register_techniques` (called from data.py, as wild/methods.py is); the piece record and the primitives' hooks (`on_create`, `on_transfer`, `on_destroy`, `wear`), the new primitives `lay`, `unlay`, `gear_night`, `rot`, `mend`; `worn_night`, `tear`, `rot_night`; the mending's cost, units and result; the words (`life_words`, `state_words`, `held_words`) |
| `engine/placed.py` (new; the placed-gear acts) | `lay` (set from the hands, up to 6 traps, 25 snares, a net, a set line; refused naming one's gear standing; ice, land), `tend_one` (catch into hand, the night's losses said, broken pieces home, set again or `up`, snares moved with `to`; another's named as theft), `tend_verb` (by tag; all one's own of a kind at a place; the weir's traps), `named_alone`, `method_of`, the water clause |
| `engine/strips.py` (new; the flax strip) | a strip crop record on a holding (`strips`), `sow`, `pull`, `dig`, `ready`, `night`, `words` |
| `wild/water.py` (new; the water's stocks) | `SHALLOWS`, `ICE`, `RUN_REACH`, `FEN_WRECK`, `THAW_WRECK`, `PINCH`; `water_type`, `seed_shallows`, `renew`, `ice`, `thawing`, `froze_over`, `iced`, `thaw_wreck`, `run_reach`, `fen_wreck`, `pinch`, `stretch_ice` |
| `wild/willow.py` (new; the withies' stock) | `WILLOW` (fen 60, bank 20 bundles a unit of size), `seed`, `renew`, `spring_K`, `harm` (summer cutting) |
| `engine/world.py` | the primitives move pieces with goods; `p_wear` wears a piece (broken at 0, kept) and reads the older tools' converted lives; the five gear primitives registered; the shallows and willow seeded at a world's making, after the wild layer |
| `engine/data.py` | the gear unit registered; RESOURCES `shallows`, `willow`; `cut withies` on the willow (fen and banks), else young growth; `twist cord`; `pull flax`, `dig a strip`, `dress and spin`; CROPS `flax`; the edge (`fish by hand`) on the shallows, relabelled, the aliases "fish" and "fishing" dropped, a dip net at a run's pinch; line fishing (`angle`) with a hand line or a rod |
| `engine/verbs.py` | VERB `set` (gear by `what`) and a new `tend`; `cost` for both; a set technique named alone through `placed`; lift, check, empty, walk and collect read as tend (D2-294); `_mend_gear`; the make result in pieces with its batch and life; the stock draw by `draws_at` (shallows, willow); the run's take by the pinch; a line worn by use; D2-304 on a take from several of one's own piles |
| `engine/wild.py` | `set_work` through `placed.lay`; `_set_night` rewritten for placed gear (no spring by age; `line` the sound pieces; idle under ice; a run by the parcel's reach; the gill net's and set line's draw on the water's fish; the snares' night: dead 4 in 5, scavenged, freed; the night's record for the tend's words; a night of wear); the wreck piece by piece in the river and the fen; the thaw's crush; the runs held at an iced stretch, the weir alone at edge ice for the fish going up; otters skip gear frozen in; `run_kinds`, `flow_tonight`; `run_take` by the pinch |
| `wild/runs.py` | `advance(..., iced=)`: eels held at any ice, salmon and lampreys when frozen over, tallied once; no eel start at an iced stretch |
| `wild/methods.py` | `gill net` and `set line` set methods (`SETS`), not known by the land; "wicker traps", "snares" and the like as the methods' aliases |
| `engine/things.py` | `owns_set` by the set's household (a leaver owns it no more); nouns and lines for the gill net and set line; one's own placed gear listed with its count; a taken-up set lies nowhere |
| `engine/here.py` | reads for the acts (D4-35): `sets`, `sound_held`, `pieces`, `ice`, `water_type`, `pinch`, `day_words`, `catch_words`, `plural`, `run_kinds`, `flow_tonight`, `owns_thing`, `gear_words` |
| `engine/knowledge.py` | `draws_at`; `ready`: the edge refused under ice, at a run only by its pinch, at the shallows' refuge with "fished out for now, and nothing is running"; line fishing needs a line; `craft_line` and `crafts_lines` by level (D2-263); the flax kinds to the farm |
| `engine/farm.py` | the strip in `_sow`, `_sow_why`, `act`, `ready`, `night`; whole-plot flax by its kg a plot; `_herd_on(consume=True)` for slaughter (D2-304) |
| `engine/renewal.py`, `engine/night.py` | rules `shallows` (none under ice) and `willow` (back in spring, K mending); `gear.rot_night` after the wild |
| `engine/signs.py`, `engine/perceive.py` | five shallows rows (stripped, fished over, fry back, the cold margins still, ice on the margins), by the one rule; `shallows` a land draw |
| `engine/prompt.py` | the craft lines by level; "Of your gear: ..." for one's worn gear in hand |
| `engine/bots_livelihood.py` | traps laid from the hands (six a setting), tended by tag, the household's tended when the setter is gone (D2-305), mended, made, withies cut; the gill net set in a run window |
| `engine/schema.py`, `spec/core/world_schema.md` | version 13: containers `pieces`, `household` (and the set fields already used); parcels `strips`, `strip_dug` |
| `landgen/gates.py` | `Finding`, `making_gates`, `probe_making`, `making_report` (u3 §7) |
| `capacity/graph.py`, `engine/lore.py` | the strip's kinds placed; the sowing lore of the field crops only |
| `specs/make_nutrition_runs.py`, `specs/nutrition/runs_*.yaml` | `water_only`: the Isel's small resident fish (8.8), the trap-making craft at the setting's level, six traps for each capable or known setter, a gill net to the weir's expert |

## 2. Each change, with its test

All new tests are in `tests/test_cybertron2_stage2_taking.py` unless named.

| Change | Test |
|---|---|
| set lays held gear, up to six an act, 1 unit, refused naming the standing gear (fault 12) | `test_set_needs_gear_in_hand_and_lays_up_to_six_for_one_unit`, `test_a_set_with_nothing_in_hand_is_refused_and_points_to_none_standing` |
| tend takes all one's own of the kind at the place, sets again; `up` brings it home with its pieces | `test_tend_takes_all_of_ones_own_there_and_sets_them_again_and_up_brings_them_home` |
| lift, check, empty, walk, collect read as tend (D2-294) | `test_lift_check_empty_walk_and_collect_read_as_tend` |
| a technique named alone tends, sets or refuses | `test_the_technique_named_alone_tends_sets_or_refuses` |
| household gear every member's, a leaver's no more (D2-305) | `test_a_household_member_tends_the_households_gear_and_a_leaver_does_not` |
| another's gear: unnamed never touched, named emptied as theft and recorded | `test_anothers_gear_named_is_emptied_as_theft` |
| a consuming act on several of one's own needs its target (D2-304) | `test_a_kill_on_several_of_ones_own_needs_its_target` |
| lives in nights and acts (D2-310), nets' wet life (D2-329), the tools converted | `test_lives_in_nights_at_the_calendar_and_in_acts_at_the_factor` |
| a piece wears by nights, breaks, is brought home, is mended for half its uses at a tenth of its materials | `test_a_piece_wears_by_nights_set_breaks_and_is_brought_home_to_mend` |
| mending gives back no rot; a rough failure spoils only the materials | `test_mending_never_gives_back_rot_and_a_rough_failure_spoils_only_the_materials` |
| rot wet in the water, gone at 1 | `test_gear_rots_wet_in_the_water_and_a_rotten_piece_is_gone` |
| pieces move with goods, most worn first | `test_pieces_move_with_the_goods_most_worn_first` |
| units and batches by the factor (1/15 and 1/7); no recipe free | `test_recipe_units_and_batches_follow_the_factor` |
| a make of n pieces by its batch, its words | `test_a_make_of_n_pieces_costs_units_by_its_batch` |
| a craft line at each level (D2-263) | `test_a_craft_line_renders_at_each_level` |
| the shallows on every water and fen parcel by type | `test_shallows_seeded_on_every_water_and_fen_parcel_by_water_type` |
| the shallows' renewal by season, none under ice | `test_shallows_renew_by_season_and_not_under_ice` |
| the edge on the shallows, refused only stripped with no run; "fish" no alias | `test_the_edge_draws_the_shallows_and_is_refused_only_when_stripped_with_no_run` |
| the pinch | `test_the_pinch_by_water` |
| the shallows' signs by the one rule | `test_shallows_signs_read_the_parcels_own_stock` |
| ice by water type | `test_ice_by_water_type` (five cases) |
| set gear idle under ice, its nights still run; setting refused | `test_set_gear_is_idle_under_ice_and_setting_is_refused` |
| eels held at an iced stretch, salmon pass under edge ice | `test_eels_are_held_at_an_iced_stretch_and_salmon_pass_under_edge_ice` |
| the fen's reach and wreck | `test_a_fen_beside_the_river_meets_half_the_run_and_one_away_none` |
| willow on the fen and banks; cut withies draws it; spring | `test_willow_on_the_fen_and_the_banks_and_cut_withies_draws_it` |
| a small sowing of flax is a strip beside the main crop | `test_a_small_sowing_of_flax_is_a_strip_beside_the_main_crop` |
| the water-only runs world | `test_the_runs_world_is_water_only_with_small_resident_fish_shallows_and_seeded_traps` |
| the making gates: M4 on Eelmouth, M8 crash-free, switched off | `test_the_making_gates_find_the_runs_worlds_missing_stone_and_can_be_switched_off`, `test_a_setter_with_no_gear_and_no_time_to_make_it_is_warned` |
| the bots make and cut when short of traps | `test_a_fisher_short_of_traps_makes_them_and_cuts_withies_for_them` (`test_bots_livelihood.py`) |

## 3. The numbers changed

- **Lives (D2-310; u3 §3.3).** Set gear in nights at 32/365: wicker trap 20 (real 228), gill net 25 (real 285) with a wet rot of half
  a world year, 16 nights in the water (D2-329), set line 6; snares lost 1 in 6 a night set. In acts at the factor (1/15): fishing
  rod 14 (was 30, never worn), hand line 4, dip net 12. Rot in world years, wet / dry: trap 2 / 5, net and set line 0.5 / 5, keep box
  2 / 5, rod 3, hand line 2, creel 4, basket 2, pack 2.5, hurdle 7, sack 3, salting tub 5, barrel 10. The older tools on their wear
  map, converted: crude tool 19 uses (was 10), copper tool 65 (40), crude weapon 7 (10), harness 47 (80), plough 18 (60), bedroll 30
  (40), tent 30 (30).
- **Mending (u3 §3.4).** Half the full uses, never above full, no rot; a tenth of the making's materials a piece (a set line 0.03
  cord and 15 hooks, a hand line a hook); 1 unit for the lot.
- **Recipes (u3 §2.2), units and batch at 1/15.** Wicker trap 0.45 withies, 6 h: 1 unit, up to 5; creel 0.25 withies, up to 5;
  basket 0.3, up to 5; keep box 1, up to 3; hurdle 1, up to 10; hand line 0.02 cord and 2 hooks, up to 20; set line 0.3 cord and 30
  hooks, up to 3; bone hook 0.005 bone (day clock), up to 5; copper hook 0.005 copper at an anvil, up to 75; snares 0.005 cord (day
  clock), up to 12; gill net 1 cord and 0.1 stone at a house, 2 units; dip net 0.1 cord and 0.2 withies, up to 8; sack 0.6 cord, up
  to 7; salting tub 2 timber and 0.1 withies, up to 5; barrel 7 timber and 0.3 withies (the cooper's), up to 3. Weights as u3 §2.2.
  Goods: cord 1 kg, flax 1, retted flax 1, flax seed 1, bone 1.
- **Taking.** A set lays up to 6 traps, 25 snares, 1 net, 1 set line for 1 unit; a tend 1 unit for all of one's own of the kind
  at the place; a trap holds 10 kg (WATER_WORKS, unchanged) a trap laid; the gill net up to 6 kg a night of the water's own fish at
  full stock, 15 kg in a run; the set line 1 kg and 3 kg. Line fishing: base 1.0 with a hand line, x1.5 with a rod (was 1.5 with a
  rod). The edge: the shallows at its old base 0.6; a run's take x the pinch (1.0 below a shut weir or dam, 0.3 a brook or river,
  0.1 a big river) x3 with a dip net.
- **The water (u1).** Shallows K a unit of size: brook 5, pool 4, fen 7, river 4, big river 2, lake 2; r a night spring 0.06,
  summer 0.10, autumn 0.06, winter 0.01, 0 under ice. Ice: edges at 1 night of hard frost (a big river 2), over at 2 (river 4, big
  river 5, lake 6); the thaw crushes 0.1 of the traps in a small water that froze over, tears 0.3 in a river. A fen trap beside the
  river meets half a run, wrecked at 0.02 in spate and 0.05 in flood.
- **Willow (u3 §1.1).** 60 bundles a unit of size of fen, 20 of a bank parcel, back each spring (half where beasts graze); a bundle
  cut in summer lowers K by 0.1, a tenth of the loss mended a year. Cut withies 1.5 a unit, by the season, on either stock.
- **Cord and flax.** Twist cord 0.04 kg a unit in summer and autumn (0.03 spring, 0.01 winter); flax 11 kg of seed a plot, a strip
  up to a quarter of a plot, yield 5.5, seed back 0.1 kg a kg pulled, pulling 0.05 plot a unit; dress and spin 1 retted flax to
  0.125 cord a unit.
- **The runs world (D2-316, D2-330 C5).** The Isel's resident fish 8.8 (a quarter of a river's 17.6 a unit of size, size 2),
  regrowing fast; six wicker traps for each capable or known setter (six adults in the medium and high arms, none in the low); a
  gill net to the weir's expert (Nichola, high arm). With the shallows (the Isel 4, Eelmouth Fen 21) the water's own stocks give
  about 1.5 fish units a night at best against the village's need of about 20.

## 4. Tests updated, and why

| File | What and why |
|---|---|
| `test_bots_livelihood.py` | four tests pinned traps laid from nothing (`set what: trap in water` from empty hands), the lift as `take` and "You set traps in the water": now on the medium arm, whose setters hold six traps (D2-330 C5), sets of `wicker traps` with a qty, the lift a `tend` (D2-294), the result words u2's; a new test that a fisher with no traps makes them or cuts withies |
| `test_cybertron2_stage1_basis.py` | the edge's refusal at a run now reads the shallows (u1 §2: "fished out for now, and nothing is running"); the named-alone test gives the traps into hand (fault 12) and reads the tend's kg |
| `test_cybertron2_water5_river.py` | three tests give one trap into hand before setting (fault 12); the `no_new_runs` helper passes `advance`'s new `iced` |
| `test_cybertron2_water_fixes.py` | the traps beside the weir laid from the hands, three a setter |
| `test_cybertron2_switches.py` | the trap of the resident-fish test laid from the hands each day |
| `test_cybertron2_wild_sets4c.py` | lift and check read as tend (D2-294): the tend's words for those acts, `take` unchanged; the catch test gives a line of five snares into hand |
| `test_cybertron2_wild_raiders.py` | five snares into hand; the set's words are u2's ("You set 5 snares on the runs of ...") |
| `test_cybertron2_water_bodies.py` | the body's one stock is lowered by a line (u2 §4.5), the edge now drawing the parcel's shallows (D2-317) |
| `test_cybertron2_package_b.py` | the bots travel unladen in both arms of the equivalence test (`World.capacity` patched in both): since u3's willow they gather withies and timber first and were too heavy to set off |

## 5. Spec drift found

- **Key collisions:** the make rows for snares, the gill net and the set line cannot share their item's name with the set methods
  `snare`, `gill net`, `set line` in TECHNIQUES; the recipes are `snares`, `gill nets` and `set lines` (each with its item's name as an
  alias, resolved by the verb first). `make wicker trap` keeps its name.
- **Lines moved, intent followed:** verbs.py's `_technique` set branch (u2 cites 678-681) is near 760 after stage 1; `_set` 1992 is
  near 2210; `_lift`/`_take` 1608-1698 near 1840-1950; `things.owns_set` 289 is 289 to 307; `wild._set_night` 921-1016 was 928-1022
  before this stage; the wreck loop 3155-3168 near 3170; `run_take` 3242 near 3330; `knowledge.ready` 206 near 207. world.py's seed
  (u1 cites :261 after `WA.seed`) moved after `WL.seed`, since a big river's type needs the wild layer's river network.
- **u1 §2's recovery claim:** "back to half in about 10 to 15 nights" from the refuge; the spec's own formula takes about 18 to 20
  summer nights from 5%. The formula is built; the test reads 20 nights.
- **D2-316 against u1 question 4:** the "no resident fish" switch no longer touches the shallows (they are seeded on every water
  and fen parcel of a world with the water pack); the switch itself stays for the test arms that use it (no world sets it).
- **u3 §7's materials pack:** the engine has none, so the gate check runs on every world (and `willow` is seeded in every world).
- **Bone and hooks:** nothing gives bone yet (dressing a kill is not built), so bone hooks cannot be made, and a hand line or set line
  needs copper hooks from a smith.
- **The runs world's youths and children** carry seeded knowledge of the setting; only adults hold traps (C5's "capable setter").
- **`gather {what: "wicker traps"}`** resolved to the make row before this stage; the trap method now takes "wicker traps", "traps"
  and "the traps" as its aliases, so the gather and make verbs each find their own.
- **The bots' deaths:** in the 40-day bot run the late-winter deaths come about a week earlier than stage 1's (from day 24 against
  day 31): traps are now finite and torn away by floods, where stage 1's bots laid a new trap from nothing each act (286 settings
  against 33). Read as the interface working, not as evidence about the world (D2-298).

## 6. Not done, and why

- **Snare places and sprung nooses (u2 §4.2):** the parcel's good places (edges, tracks), strange ground's half and sprung-empty
  nooses are not built; the snares' dead, scavenged and freed night is. The cold-line words ("thin", "shy") wait with them.
- **The gill net in a spate:** it is torn at 0.3 in a flood; the spate's fouling (no take that night) is not built.
- **Dressing a kill, bone, tallow, pelts (u3 §1.4), the spear, bait (L-145), summer rods' brittleness (u3 §5):** not built; the
  brief did not list them, and bone hooks wait on them.
- **The older tools as pieces:** they keep D2-46's wear map, now with converted lives, and still vanish at the end of their life;
  broken-and-mended tools wait for a piece record there (u3 §3.2), which touches `best_tool` and every tool use.
- **Retting and spinning in the flax chain:** retting is a processing container (U4, stage 3); `dress and spin` exists but nothing
  makes retted flax yet. The strip's holding words (`strips.words`) are not yet in the field's line in "Here"; trampling of a dug
  strip by grazing beasts is not built.
- **The gate check at world build** (a refused world raising in `World`, `out/<world>/gates.json`): U11's, stage 4. M5 checks only
  retting water; M7 only a wattle weir's withies. Livelihood rows (household_skills §1) do not exist yet, so a household's crafts are
  its members' known crafts.
- **The weir's traps** are tended through `tend` by their crew; the bots still take from them as before.
- **Mending in a bot run:** the bots mend broken traps in hand, but in the 40-day runs the traps were torn away before they wore out,
  and the one fisher who brought broken traps home died the next day; mending is covered by the unit tests.
- **The craft cards** (`knowledge.card`, shown on request in run.py) keep their old form; the prompt's craft lines are D2-263's.
- **The make of more than a batch** reports each act's line (two lines for 6 traps), not one line for all.

## 7. Results

**Tests (`python3 -m pytest -q`, six shards):** before (26cc29aa) 748 passed, 2 skipped; after (the branch head) 784 passed, 2
skipped.

**Bots:** `python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml --bots runs --days 40`, after: 40 days, no
errors; the same seeded death on day 1, then deaths from day 24 to day 32, 5 alive on day 40 (before, at 26cc29aa: deaths from day
31 to 35, 5 alive). After, from the run's journal and turns: 34 `lay` changes (33 settings of wicker traps from the hands, one of
the gill net), 97 tends, 23 makes of wicker traps, 35 cuttings of withies, 30 tends reporting traps torn in floods and spates, 4
settings refused at the ice's edges, pieces worn by the nights to broken (a trap's least life 0, the net's 22), one tend bringing
broken traps home to mend, 86 nights of dry rot on gear in hand. Before: 286 settings from nothing and 225 takes from traps.

The medium arm (`runs_medium`, no weir), 40 days, no errors: after, 31 settings, 73 tends, 24 makes of traps, 32 cuttings of
withies, 21 tends reporting traps torn; the village dies out from day 20 to day 25. Before (26cc29aa) its deaths ran from day 26 to
day 39, one alive at day 40. The bots' fixed policy keeps setting traps into floods (`trap_stop` empty) and now loses them, where
before a trap cost nothing; that is the interface doing what fault 12 asks, not a reading of the world (D2-298). Whether live
players lose their gear the same way is for live run 1.

**The making gate check (M1 to M8) on the current worlds** (`landgen/gates.making_report`):

| World | Findings |
|---|---|
| nutrition/runs_low | M3 x3 (each household: 12 traps needed by the first run in 5 days, about 47 units at a rough hand with summer rods), M4 x3 (no stone within a day), M6 x3 (no one capable of making wicker traps: the arm's skill is rough) |
| nutrition/runs_medium | M4 x3 |
| nutrition/runs_high | M4 x3; M6 x1 (the Marshes: no one can make a gill net, so the expert's net cannot be remade) |
| water/runs | M3 x9, M6 x9, M4 x3 (the older nine-household runs world seeds no traps and no trap-making) |
| water/river | M3 x6, M4 x6, M6 x6 |
| water/lake | M3 x3, M4 x3, M6 x3 |
| fishing/water | M4 x3 |
| valley_s5 | M4 x2 |
| hollins_s7 | M4 x5 |
| hollins2_s8 | M4 x3 |
| region_c_s27 | none (after charcoal's "no forest here" was read as the place's, not the code's) |
| two_valleys_s1 | M1 x1 (refuse: the Craggs' harness needs hide, none within a day) |
| wide_s7 | M4 x3, M1 x2 |
| wenbridge | none |
| combe | M4 x1 |
| frontier_camps | M4 x4 |

No M8 crash anywhere: every make technique the worlds switch on ran with its inputs in hand. The M4 findings are the reading u3 §7 and
C2 expected (Eelmouth has no rock; D2-330's rock source comes with U11's remake); the M6 findings on the older water worlds are their
missing making crafts, which U11's livelihood rows will seed.
