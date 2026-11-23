# Stage 3 of the fishing, hunting and materials wave: keeping, stores and the household book (report)

23 Nov 2026, 37.2 (build subagent). Thread W-99, under the wave's integrated design (W-85). Branch `w85-s3-keeping` (from `main` at
21530516, after stage 2 merged), not pushed, not merged. Specs: `docs/cybertron2/proposals/w73_design/u4_processing.md`,
`u5_stores.md`, `u6_book.md`, each read under its "Decisions since" table (u6 §5 as rewritten to D2-301); basis.md, integration.md,
build_plan.md stage 3; stage 1's and stage 2's reports; 37.4's standing_rules.md and spec agents/standing_orders.md (D2-313);
guides/senses.md; feature_packages.md §9.1 and §10. No model calls, no live runs, no Hugging Face; bots for interfaces only (D2-298).

## In brief

- **Built, as three feature units in new modules (D2-244):** `engine/process.py` (u4: the rows, lots in containers by the kg, one
  night step in place of `keeping.night` and the rack code, loading, `tend` on a container's fire, taking down, the racks' work
  floor, the house lines and the book's states); `engine/stores.py` (u5: every good sorted into a space and a container in real
  kilograms, the penalties each place leaves on the base rate, vermin by exposure, vermin's illness); `engine/book.py` (u6: one book
  a household and a person, the `rule` act, `when` and `unless` on states the household knows, the spare-units phase person by
  person, units left as rest, the rules block, the morning's and the evening's lines). The old files are touched at their seams.
- **Out, as decided:** tanning, liming and their rows (D2-327). Retting stays, since u3's flax is built.
- **Tests:** before (21530516) 784 passed, 2 skipped; after (the branch head) 814 passed, 2 skipped (30 new in
  `tests/test_cybertron2_stage3_keeping.py`). Twelve test files pinned the rack, the stores' multipliers or
  the keeper by hand; each is listed in §4.
- **Bots:** `runs_high` with `--bots runs` for 40 days runs with no errors, and its replay has no mismatches (320 steps checked).
  Every household's head set five rules on day 0, and the spare-units phase did the keeping by them: 30 hangings on the racks, 20
  fires tended, 20 lots taken down, 2 saltings, 7 loads of firewood carried to the smokehouses (§7).

## 1. What was built, by file

| File | What changed |
|---|---|
| `engine/process.py` (new; u4) | data: `PROCESSES` (keeping smoke, hard cure, hearth rack, retting, salting, hot smoke), the techniques that load them, the fittings' `process` and `holds_kg`, the waiting goods; reads: `lots`, `room`, `capacity`, `fuel_tonight`, `fuel_have`, `states`; acts: `load`, `lay_ground` (retting), `tend`, `take_down`, `salt`, `refuse_load`, `full_words`; the night: `night` (each container's condition, the fire's fuel all or none, the keyed chance it catches), `finish` (a lot become its output, staying in its container), `decay` (a lot's goods); `catch` and `burn_building` moved from keeping.py; `work_floor`, `sets_fit`; `house_lines` |
| `engine/stores.py` (new; u5) | data: `SPACES`, `CONTAINERS`, the goods' classes and `PENALTY`, `VERMIN`, `ILLNESS`, the chest and the smoke loft; `portions` (the sort), `factor`, `rate`, `rates` (a store's night by portion), `in_hand_rate`, `exposure`, `vermin_portions`, `exposed`, `household_exposure`, `illness`, `rats_at`, `store_line` |
| `engine/book.py` (new; u6) | the records (`s["books"]`, the `book` primitive), `act` (the `rule` act: set, change, drop, propose), `reading`, `state_of`, `holds`, `seen`, `target`; the store moments `install`/`_arrive` (go, moment 1), `keeps` (moment 2), `held` (moments 3, 4), `meal`; `set_fallback`; `spare_units` (moment 5) with the keeping chores (`_load`, take down, `_move_store`, tend) and the fallbacks; `rules_block`, `morning_lines`, `day_lines`, `GRAMMAR` |
| `engine/keeping.py` | the brine spring only (`near_spring`); `catch`, `burn_building`, `fuel_cids`, `is_smokehouse` re-exported from process.py for older callers |
| `engine/data.py` | the smokehouse's, hearth rack's and drying rows removed (process.py registers them); salting rows name their process; `racks` off the fittings; smoke racks 1 space; the waiting goods spoil at their input's base; hard-cured meat 0.71; DECAY's `smoke` gone; `house_spoil`, `cellar_spoil`, PHYSICS smokehouse `fuel`, every fitting's `spoil` gone; bins, granary, cellar, vault and woodshed in kg; the units registered |
| `engine/night.py` | `PROC.night` after the hearths' fires; `PROC.finish` after the spoiling; `_dried` gone; `decay_rate` reads a lot's row, a store by portion (one read a store a night), in hand by u5; `spoil_rate` well kept for "store" and "hand"; the meal by the book (`first`, the ration, what is held back); the night's record carries the day's book |
| `engine/verbs.py` | `_load_lot` (a loading in kg, its units by what will hang, a chore's `_kg`), salting through `process.salt`; the rack branch gone; `tend` on a container (`_container_at`); `move` with `from` takes a done lot down (`_take_down`, its cost at 120 kg a unit); the racks' cap at building; VERB `rule` (free); what is held back is not drawn; the full store's words |
| `engine/buildings.py` | `stores`, `alloc`, `fits`, `room_for`, `full_words`, `vaulted` on the sort; `overflow` to the household's next store at the place before the door |
| `engine/wild.py`, `wild/kinds.py` | `DRY_STORES` is u5's `VERMIN`; `_store_food` the exposed store; `_stops` by kind (cat, owl, dog: `STORE_STOPS`, `STORE_KIND`); `_stores` by portion, hung lots at 0.3, door piles at 1.5 with dry goods, the building's `vermin` record; EATEN_SIGNS by where (floor, sacks, chest, door, hung); `_racks_in` reads lots |
| `engine/signs.py` | the smokehouse's context reads last night's lots; the eaten-store rows by where; the outdoor rack reads its lot |
| `engine/life.py` | the adult's sudden illness x vermin's factor |
| `engine/here.py` | `lot_room`, `smoke_fuel`, `held_back`, `rules_block`, `book_lines`, `take_down_units` (verbs and prompts read through Here, D4-35); `rack_room`, `rack_full`, `smoke_fuel_nights`, `hung_by_household` gone |
| `engine/knowledge.py` | `ready` refuses a loading by the row (room, structure); `available` less what the book holds back |
| `engine/prompt.py` | `house_known` from `process.house_lines`; the store line by portion; the book's morning lines; the rules block in the system prompt; the `fallback` field's text (stands until changed, no example); the "3 times better" branch gone |
| `engine/run.py` | the fallback loop replaced by `book.spare_units`; units left: "You rested 2 units." |
| `engine/evening.py` | `rule` among the evening's acts (D2-319); the standing rules and what they did, at the hearth |
| `engine/world.py` | the `book` primitive; the book's arrival hook installed |
| `engine/things.py` | a lot's line (racks, the hearth, flax retting) |
| `engine/schema.py`, `spec/core/world_schema.md` | version 14: containers `lot` (for `rack`), buildings `smoke`, `boiled`, `vermin`, top-level `books`, people `chore_carry`, `today.book` |
| `engine/bots_livelihood.py` | the keeper sets the household's book (`book_rules`, `_book`) and leaves units for its chores (`reserve`); drying at the hearth and boiling salt by hand as before; `_smokehouse_keep` and `_smokehouse_fuel` gone |
| `fuel_budget.py` | the harness on lots (a done lot taken down, the fuel by the kg) |

## 2. Each change, with its test

All new tests are in `tests/test_cybertron2_stage3_keeping.py`.

| Change | Test |
|---|---|
| a lot counts a night only tended and fuelled; untended, `out` and the input's base; done at 0.5, staying on the racks (B8) | `test_a_lot_counts_a_night_only_when_tended_and_fuelled_and_stays_on_the_racks_when_done` |
| 250 kg a set; a done lot holds its room until taken down; loading over room says the rest; taking down at 120 kg a unit | `test_room_is_250_kg_a_set_and_a_done_lot_holds_it_until_taken_down` |
| fuel by the kg loaded (37.5 bundles for 250 kg), all or none; the house lines say it | `test_the_fuel_is_by_the_kg_loaded_and_short_fuel_kills_the_night` |
| the building caps the sets, keeping its work floor | `test_the_building_caps_the_sets_of_racks_keeping_its_work_floor` |
| a hard cure refused in wattle (u4 §6's words); 60 kg of salt fish to 24 after 3 nights in timber | `test_a_hard_cure_is_refused_in_wattle_and_in_timber_turns_60_kg_of_salt_fish_into_24_after_3_nights` |
| salting into a tub with room, else packed in the store, 1 salt to 4 fish, short of salt said | `test_salting_lands_in_a_tub_with_room_else_packed_in_the_store_at_1_salt_to_4_fish` |
| the hot smoke: two thirds, cooked | `test_the_hot_smoke_gives_two_thirds_cooked_to_eat_without_a_fire` |
| a fire caught burns the lots inside | `test_a_fire_caught_destroys_the_lots_inside` |
| the same draws give the same lots | `test_the_same_lots_come_from_the_same_draws` (and the bot run's replay, §7) |
| the containers' states for the book | `test_the_containers_states_read_true_and_false_on_the_right_nights` |
| retting in water a night, on the grass three | `test_flax_rets_in_water_a_night_and_on_the_grass_three` |
| the sort: chest, bins, sacks, then loose; nothing below its base; the store line by portion | `test_the_sort_puts_grain_in_the_bins_the_chest_the_sacks_and_then_loose_and_nothing_keeps_below_its_base` |
| fresh fish at its base in a store (the x2 gone), x1.5 in hand, a creel removes it | `test_fresh_fish_keeps_at_its_base_in_a_store_worse_in_hand_and_in_a_creel_at_base` |
| a cellar takes the summer off fresh meat, gives grain its damp | `test_a_cellar_takes_the_summer_off_fresh_meat_and_gives_grain_its_damp` |
| salt fish at base in a tub, x1.5 out of brine | `test_salt_fish_keeps_at_its_base_in_a_tub_and_worse_out_of_brine` |
| vermin by where the grain lies (five times loose against a chest); a cat cuts mice more than rats | `test_vermin_take_by_where_the_grain_lies_and_a_cat_cuts_mice_more_than_rats` |
| the exposed store: chests lower it | `test_a_village_of_chests_shows_less_exposed_store_than_one_of_floors` |
| vermin's illness: 1, 3 at R 120 and E 1, 1.4 at E 0.2 | `test_vermins_illness_factor_by_rats_and_the_households_exposure` |
| the night's loss by portion | `test_the_store_line_and_the_nights_loss_read_the_portions` |
| a sack rots over its life | `test_a_sack_rots_over_its_life` |
| a rule read back; the refusals of u6 §9; a member's household rule a proposal; free | `test_a_rule_is_read_back_refused_where_it_must_be_and_a_members_is_a_proposal` |
| the spare-units phase hangs by rule what the day brought, in a member's spare units | `test_the_spare_units_phase_hangs_by_rule_what_the_day_brought_in_a_members_spare_units` |
| a lasting state's rule missed is recorded, waits, and fires the next day | `test_a_rule_on_a_lasting_state_waits_when_no_one_has_units_and_fires_the_next_day` |
| one's own standing fallback before the household's chore (D2-301); nothing set, all rest | `test_ones_own_standing_fallback_comes_before_the_households_chore_and_unset_units_are_rest` |
| a chore's fraction carried until whole; never more than the spare | `test_a_chores_fraction_is_carried_until_whole_and_never_takes_more_than_the_spare` |
| each rule once a day | `test_each_rule_fires_once_a_day_and_cascades_stop` |
| `seen` only from what a member noticed | `test_a_rule_when_the_run_is_seen_fires_only_on_a_day_a_member_noticed_it` |
| a `go` rule sends goods arriving to its store | `test_a_go_rule_sends_goods_arriving_to_its_store` |
| what is held back is not eaten; `first` orders the meal | `test_what_the_book_holds_back_is_not_eaten_and_first_goes_first` |
| the rules block in the system prompt, the field's example gone, `rule` at the evening | `test_the_rules_block_and_the_evening_carry_the_book` |
| the keeper by rules (bots) | `test_a_surplus_is_smoked_at_the_racks_and_the_fire_tended_after`, `test_a_smokehouse_fire_reaches_no_house_and_its_smoked_fish_is_brought_home`, `test_fish_beyond_the_racks_are_salted_with_the_salt_houses_salt` (`test_bots_livelihood.py`, rewritten) |
| the next store before the door | `test_a_farm_households_200_grain_...` (`test_cybertron2_buildings.py`, rewritten) |

## 3. The numbers changed

- **The processes (u4 §2).** A keeping smoke 1 night (was 3), hung at 30 kg a unit (a batch of 40 a unit before), a set of racks 250 kg
  on 1 space (40 on 3), fuel 0.15 bundles a kg loaded over its nights (0.5 heat a night whatever hung, about 1 bundle); a hard cure 3
  nights, 60 kg a unit, 0.25 bundles a kg, 0.4 of salt fish and 0.85 of salt meat, timber or stone only; the hearth's rack 1 night
  (3), 8 kg, the hearth lit tonight (outside, a dry night) rather than the calendar; salting 40 kg a unit at once, salt 1 to 4 and 1
  to 8 (as stage 1); the hot smoke 10 kg to 6.7, 1.5 bundles; retting 50 kg a unit, 0.8 retted, water 1 night, the grass 3, half
  washed away by a spate on a river parcel; taking down 120 kg a unit; the work floor 1 space in a hut room, 2 in any other.
- **The goods waiting.** Smoking and drying fish and meat at their input's base off the fire (fresh fish 0.175, meat 0.129; were
  0.12) and at 0.03 in it; a salted lot on the racks at its own base. Hard-cured meat 0.71 food a kg (data had 0.67; B10).
- **Stores (u5 §1 to §3).** The bins 300 kg of dry goods (were 60 food), a granary floor 400 kg a space, 1,200 a fitting (300 grain),
  a cellar 30 kg a space of the footprint (40 food), the vault 30 kg a space, the woodshed 9,600 kg as stage 1; a sack 50 kg at 12 a
  space, a basket 25 at 10, a chest 400 on a space, a salting tub 120 at 3, a barrel 120 at 4; a smoke loft 40 kg a space of the floor.
  The stores' multipliers gone (D2-272): bins x0.5, the granary x0.2, the cellar x0.25, the house rate; what keeps a good is its base
  times the penalties its place leaves, composed on the hazard (r' = 1 - (1 - r)^k): floor damp x2 dry goods and x3 cured ones (x1.5
  in sacks or baskets), flies x1.5 in summer, out of brine x1.5, the heap x1.5 for loose roots, frost x3 for roots, the warm season
  off what a cellar keeps, in hand x1.5 for foods that keep 4 days or less (a creel or basket removes it).
- **Vermin (u5 §5, §6).** Exposure loose 1.0, sacks and baskets 0.8 and 0.7, bins 0.5 and 0.4, a chest 0.2 and 0.15, tubs and barrels
  0.05, hung 0.3, a granary floor 0.6, a door pile 1.5 with dry goods too; stops a cat 0.7 and 0.4, an owl 0.9 and 0.6, a dog 0.5 and
  0.8 (the granary's 0.3 and the bins' 0.7 as stops gone); the adult's sudden illness x (1 + 2 x min(1, rats a km² / 120) x E_h).
- **The book (u6 §5).** Chores at their real fractions, carried until whole; at least 1 spare unit to start; three rounds; each rule
  once a day; "whoever has time" the most spare first.

## 4. Tests updated, and why

| File | What and why |
|---|---|
| `test_cybertron2_water5_keep.py` | the rack's 40 a batch and 3 nights, done into the store, 1 firewood a night, `rack` and `keeping.night`: now u4's 30 kg a unit, 1 night, the lot on the racks, the fuel by the kg, `lot` and `process.night`; a neighbour's lot taken down by them, refused to the house's people unnamed (Q-80); the house lines' words; salted fish at their base in a store (`house_spoil` gone); the smoke's sign the morning after a lot finished |
| `test_cybertron2_dry4c.py` | the hearth's rack 1 night (3), its lot staying on the rack (into the store before), the in-process rate a night, the morning lines' words |
| `test_cybertron2_lake_fixes.py` | the hearth rack's row in PROCESSES (the technique's `rack` gone), u4's words, an outdoor rack's `lot` |
| `test_cybertron2_wild_calibrate.py` | the bins as an exposure, not a stop; the hearth's rack counts a night only when its fire burned (nobody slept by it there) |
| `test_cybertron2_wild_raiders.py` | the granary as an exposure, not a stop |
| `test_bots_livelihood.py` | the keeper's hanging, tending, taking down and salting by the household's rules in the spare-units phase, not by hand |
| `test_cybertron2_buildings.py` | the bins' 300 kg; the rest into the household's next store at the place before the door |
| `test_cybertron2_act_fixes.py` | a store full at 900 grain (real capacities), the full store's words |
| `test_cybertron2_fittings_ground.py` | the cellar read on fresh meat in summer: it no longer slows grain below its base (D2-272) |
| `test_cybertron2_capacity.py` | the cured goods' sources from PROCESSES (was the techniques' `rack`) |
| `test_cybertron2_stage1_basis.py` | hard-cured meat 0.71 (B10) |
| `test_cybertron2_wild_range4c.py` | the golden digest re-pinned (vermin by exposure, the exposed store the ecology draws, the stores by portion) |

## 5. Spec drift found

- **Lines moved, intent followed:** u4's `night.py:176-207` and `:286-308` (the spoiling loop and `_dried`) were near 176-210 and
  289-312; `verbs.py:760-845` (`_make`) near 915-1050 after stages 1 and 2; `:669-672` (`smoke_tend`) near 759; `data.py:117-130`
  (DECAY) near 164; the fittings at 296, 308 and 335; the techniques at 725-760; PHYSICS smokehouse at 990; `here.py:466` at 567.
  u5's `buildings.py:412-439` (`overflow`) at 425; `data.py:325-332` (STORES) at 387; `:776-777` (`house_spoil`) at 931;
  `wild.py:2716`, `:2747-2763`, `:2839-2860` at 2846, 2877, 2969. u6's `here.py:378-386` at 383; `verbs.py:1569-1595` (`_move`)
  near 1808. The rest matched.
- **Hard-cured meat:** 0.71 (B10, the build plan) is built; with salt meat at 0.57 in the data, 0.85 kg of hard-cured meat carries
  0.60 food against the salt meat's 0.57, so food is not quite conserved. Worth Zach's word on which goes.
- **A salted lot's base on the racks:** u4 §5 gives every lot in process the row's 0.03; for a hard cure that is faster than salt
  fish's own 0.0085, so a salted lot keeps at its own base (`in_rate` None).
- **No hut room:** the "wattle smoke hut" of 2 spaces is U7's (stage 5); the seeded wattle smokehouses are small rooms of 6 spaces,
  so their work floor is 2 and they take up to 4 sets. The runs worlds seed one set each.
- **Taking down as an act:** u4 §6's "(0.5 units)" cannot be an act's cost under the 1-unit floor (O-2): the act costs ceil(kg / 120),
  at least 1; a chore is charged its real fraction (u6 §5).
- **A load chore** draws its goods from the household's stores at the place, not the doer's hands (a supper kept in hand stays there).
- **The hot smoke** is done at a hearth or a fire ring, not yet at a fire in the open.
- **Retting** is built as u3 §1.2 gives it (0.8 retted, 50 kg a unit); its fouling (G3) is not.
- **Process nights** are written as the compressed numbers; `clocks.RATES` does not yet derive them from real days.
- **States in words:** a `when` or `unless` is read by keywords into a state; one naming a container ("the racks in X are full")
  reads that container; one nobody can read is shown back as such and never fires. `seen` matches a member's held lines of the day
  to a named set of words (the run, frost, the river rising, rats), not yet to U8's sign rows (stage 4).
- **The rules block** is in every world's system prompt: with no rules set, two short lines and the grammar (105 words), u6 §9's
  "about 60 words" being the block's own lines; the prompt sizes are stage 4's to measure (u9).
- **Arriving goods (moment 1)** are moved by a hook after any good is created into a household's store, so a gift, a purchase or
  salting is covered as well as work; a catch tended into one's hands is not (no default puts carried goods away, D2-274).

## 6. Not done, and why

- **u5's spaces left for later:** the granary on staddles, the sealed pit and the door pile as portions of the sort (the door pile is
  read at 1.5 by the vermin); the attending view of a store (each space and container, its fill, state and life) beyond the store
  line; the vermin signs' chances checked against intended values by the noticing rule (guides/senses.md item 4).
- **u6's eating rules:** `eat` reads a ration share and `first` an order; who eats first and guests (standing_rules item 2, 37.4's
  W-37) are not built. The head taking a member's proposal is not an act yet (proposals are stored). The "most specific rule wins"
  is read as one's own before the household's and a `when` before none, not by item over kind.
- **The children's standing work** stays the head's order (u6 Gaps, 3).
- **u4's smoke loft and chest** are data rows with estimated costs (U7 prices them).
- **The keeping signs of u8** (smoke rising, the smell, a wet outdoor rack) read the new state but are not reworked; that is stage 4.
- **The records:** the W-99 row, the decisions built (`records commit --builds`) and hygiene are the calling session's.

## 7. Results

**Tests (`python3 -m pytest -q`, six shards):** before (21530516) 784 passed, 2 skipped; after (the branch head) 814 passed, 2 skipped.

**Bots:** `python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml --bots runs --days 40`: 40 days, no errors;
the same seeded death on day 1, deaths on days 24 to 26 and on day 39, 4 alive on day 40 (stage 2: deaths from day 24 to 32, 5 alive).
The replay checks 320 steps with no mismatch. From the run's turns: each head set five household rules on day 0 (hang the fish that
comes in on the racks while they have room; salt what they have no room for; tend the fire while anything is smoking; take a done
lot down into the house; carry firewood to the smokehouse when it runs low); by them, 30 hangings, 20 fires tended, 20 lots taken
down, 2 saltings (38 kg with the Salt House's salt), 7 loads of firewood carried; "You rested n units." on 206 person-days. Of the
smokehouses' 47 nights with a lot in, 24 fires died, nearly all for want of wood: a full set wants 37.5 bundles a night, and the
bots' rule carries 25 when under 15 (the bots' rule, not the engine's; u4 §8 found the wood binds). The medium arm (`runs_medium`), 40
days, no errors: 17 hangings, 13 lots taken down, 3 loads of firewood; the village dies out from day 18 to day 25 (stage 2: day 20 to 25). These read the interfaces, not the world (D2-298).

**The making gate check (M1 to M8) on the current worlds** (`landgen/gates.making_gates` and `probe_making`): the same findings as
stage 2 on every world (runs_low M3 x3, M4 x3, M6 x3; runs_medium M4 x3; runs_high M4 x3, M6 x1; water/runs M3 x9, M6 x9, M4 x3;
water/river M3 x6, M4 x6, M6 x6; water/lake M3 x3, M4 x3, M6 x3; fishing/water M4 x3; valley_s5 M4 x2; hollins_s7 M4 x5;
hollins2_s8 M4 x3; region_c_s27 none; two_valleys_s1 M1 x1; wide_s7 M4 x3, M1 x2; wenbridge none; combe M4 x1; frontier_camps M4 x4).
No M8 finding: the new make techniques (smoke fish and meat, hard cure fish and meat, hot smoke, dry fish and meat, ret flax, the chest)
run with their inputs in hand at every village whose packs switch them on.
