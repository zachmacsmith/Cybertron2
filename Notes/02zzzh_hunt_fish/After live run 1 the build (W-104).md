---
id: docs/review/37_growth/02zzzh_hunt_fish/after_run1_report.md
kind: note
updated: "2026-11-23"
---
# After live run 1: the build (W-104)

*note · `docs/review/37_growth/02zzzh_hunt_fish/after_run1_report.md`*


Session 37.2, 23 Nov 2026, branch `w85-after-run1` (from main). What live run 1 flagged for after the runs
(`live1_report.md` "For after the runs"; `sign_timing.md` gap 2), built with tests. No model calls, no live runs.

Item 6 (a worked example of a conditional rule in the rules block) is dropped by Zach ([[D2-344 No worked example of a conditional rule is added to the rules block|D2-344]]: examples anchor agents); the
rules block's examples are as on main.

## 1. Passing on through care ([[D2-340 Passing on through care|D2-340]])

- **The care paragraph** (`engine/prompt.py` `_family_lines`), shown in the beliefs view at the opening and in the old prompt each
  morning: *While caring for a child you may give it food from your hands, "item" and "qty" (whoever gives the most food that day
  feeds it all of theirs), and pass a sentence on, "pass": "a sentence". What you pass on while caring for a child becomes theirs to
  keep for good, word for word, for life, as one of their kept lines, while they have room.* Each child's line ends with the room
  left: *(Henry has room for 2 more).* / *(Henry has no room for more).*
- **Every carer's pass is kept** while the child has room (`engine/life.py` `care_gifts`), the most food's first (a tie by the keyed
  draw); a pass beyond the room is told "holds as much as a child can"; a line the child already holds is told so
  (`engine/run.py` `night_lines`). The food rule is as before (the largest care feeds).
- **The seeded line for heads and parents** (`engine/founders.py`): BS8 keeps only its craft half (*What I know of a craft I got by
  watching, by trying and failing, and by being taught; a day beside one who knows is worth many tries alone.*); a new template HH10,
  for a head and for anyone with a living child or youth, filled from the household's own water and living while it stays within
  40 words. For every Eelmouth head and parent:
  *Our children know only what we tell them. A child I mind keeps for good a line I give it: when the eels run in the Isel, what
  keeps, who to trust. What I never pass on dies with me.* (40 words; "where we fish" is the next thing it would name, beyond 40.)
- **The cap:** HH10 is protected for those who hold it, and the drop order gains one step at its end: (9) BS8, when HH10 is held.
  Peter (20 lines, the drop order exhausted before) now drops BS8 at step 9 and holds HH10; Nichola, Hamon and Oliver drop one
  more base line (BS7 or BS6) by the order as it stood; Katherine's next step was (6) taken whole, three lines of her second
  living, so she holds 18. Every founder is within 20 lines and 40 words; the gate passes (`eelmouth.report.json`).
  **Default taken** (for Zach): the new drop step and HH10's protection are mine, written into the code only; u9 §5.2 (37.2's
  proposal) does not yet say so.
- Regenerated: `specs/nutrition/eelmouth.yaml`, `eelmouth_small.yaml` and both reports (`make_eelmouth.py`,
  `make_eelmouth_small.py`; regeneration was checked reproducible first: byte-identical before the change).
- Tests: `tests/test_cybertron2_kept.py` (every carer's pass kept, a pass beyond the room, the care paragraph and the room left);
  `tests/test_cybertron2_stage4_people.py::test_heads_and_parents_hold_the_passing_on_line_and_bs8_is_the_craft_half_alone`.

## 2. The morning's meal line ([[D2-342 Each morning a person is told what they ate the night before|D2-342]])

- `engine/night.py`: the meal records what each ate (`_eat`'s `log`: store, good, quantity), and `_meal_record` writes
  `rec["meal"][name]` (the goods, the rules that shaped the meal, how well it fed: full, short or hungry, and why when hungry: the
  rule's share, the rest kept back, not enough for everyone, nothing more to eat) and `rec["drawn"][store]` (what each store gave
  the whole meal, by good). `meal_lines` renders two lines; `engine/book.py` `meal` now names the rules that shaped it (its number,
  whose, its words or its reading), counted only when it named a good that was eaten or set the share.
- `engine/here.py` `meal_lines`; shown in "You" in the beliefs view (`engine/view.py` `_self`) and the old prompt
  (`engine/prompt.py` `turn_prompt`). Day 1 of the bot run:
  > Last night you ate 3.8 roots from Marsh House's store, in the usual order (what needs no fire, then what spoils soonest): you
  > ate your fill.
  > For the whole household's meal, Marsh House's store gave 12.7 roots and 1 egg in all.

  With a rule (tested): *... by the household's rule 1 (“we eat the roots first”): you ate your fill.*; on half shares: *...: you
  were still hungry; the rule gave you a half share.*
- `engine/world.py` `show_fine`: amounts under a tenth to their first figure (0.04), used by the meal line.
- The night lines' "a missed meal" and "less than a cold night asks" stay in "What happened yesterday", as before.
- Tests: `tests/test_cybertron2_after_run1.py` (the line, its rule and store; the store's draw equal to what was eaten from it, not
  the night's spoilage; a short store "not enough for everyone"; both mornings).

## 3. Rules are not attendable ([[D2-341 Rules are not something one attends to|D2-341]])

- `engine/perceive.py` `resolve_target`: a target naming a rule, the rules, the book, standing orders or a fallback, or given as a
  rule's fields, falls back to the place in general "(you could not find ... to attend to)", as any unreadable target; a building,
  parcel or person of that name is still itself. (Live run 1 had no attend target naming a rule; this makes it so by rule.)
- Test: `test_a_rule_or_the_book_cannot_be_attended_and_falls_back_as_any_unreadable_target`.

## 4. Teaching before the evening ([[D2-343 Teaching is settled before the evening, so a lesson's outcome can be…|D2-343]])

- `engine/run.py`: `ST.settle_teaching` moves from the settle step to the day's step, after the hunts are settled and before the
  evening, so "You taught ..." and "... taught you ..." are in that evening's "Your day"; partnerships, children's work,
  agreements, joins and thefts stay in the settle step after the evening.
- Test: `tests/test_cybertron2_evening.py::test_a_lesson_is_settled_before_the_evening_and_its_outcome_is_in_that_evenings_day`
  (fails on the old order; replays with no mismatch). The journal and replay tests pass.

## 5. A chore or fallback that gives nothing stops and is shown

- `engine/book.py`: each act of the spare-units phase is watched (`_Watch`: the primitives applied during it, and the day's record
  outside its bookkeeping). An act that moved no goods, changed nothing but its doer (practice, a tool's wear, a stock drawn) and
  left the day's record as it was gave nothing: it is not tried again that day by that person, its result line ends "It gave
  nothing, so it was not tried again today.", and the book's record keeps it (`today["book"]["empty"]`). `day_lines` tells it as a
  fact: *Your fallback, twist cord at Eelmouth Fen, gave nothing yesterday; it stopped after one try.* (the head also hears a
  household rule's: *The household's rule 1, gather twist cord at Eelmouth Fen, gave Nigel nothing yesterday; ...*). The old
  prompt's morning carries it with the book's lines; the beliefs view's later mornings show it (`Here.book_empty_lines`); the
  evening says "today" (`engine/evening.py`).
- **What live run 1's "You took 0 cord" was:** twist cord gives 0.04 kg a unit (0.01 in winter), shown as "0" by `show`'s tenths.
  It gives something, so by the brief it goes on as before; the gather line now shows it (`engine/verbs.py`: "You took 0.04 cord at
  Eelmouth Fen"). Whether that slow a yield should be a fallback at all is the agents' to see now that it is shown.
- Care, teaching and hunting parties write the day's record, not goods, so they count as giving something.
- Tests: `test_a_fallback_that_gives_nothing_stops_after_one_try_and_the_morning_says_so`,
  `test_a_chore_that_gives_even_a_little_goes_on_as_before`, `test_a_household_chore_that_gives_nothing_is_told_to_its_doer_and_the_head`.

## 6. (Dropped: [[D2-344 No worked example of a conditional rule is added to the rules block|D2-344]].)

## 7. The article

- `engine/verbs.py` mend: "You mended your hand line with 1 copper hook (1 unit): it is good for about ..." (was "your a hand line"
  ... "each is good"); two or more as before ("your 2 wicker traps ... each is good").
- Test: `test_mending_one_piece_says_your_hand_line_not_your_a_hand_line`.

## Checks

- **The suite**, in six shards (`timeout 1700 python3 -m pytest -q <files>` each): 861 passed, 2 skipped, none failed (169 + 2 skipped, 149, 114, 122,
  145, 162; the longest shard 8 min 14 s). One test pinned replaced behaviour and was updated:
  `tests/test_cybertron2_kept.py::test_the_most_food_feeds_the_child_and_its_giver_passes_on_the_line`, now
  `..._and_every_carer_passes_on_a_line_while_it_has_room` (the smaller carer's line is now kept, [[D2-340 Passing on through care|D2-340]]). No other test changed;
  the new tests are listed by item above.
- **Eelmouth with bots, 6 days** (`run cybertron2/specs/nutrition/eelmouth.yaml --bots runs --days 6`): runs in 10 s; days 1 to 6
  as live run 1's bot arm (alive 11, Basilia's death on day 1 as there); the meal lines in every morning from day 1.
- **Renders** (`render_eelmouth.py --out <scratch>`): Peter's day-0 system prompt carries the rules block unchanged and HH10 among
  his kept lines; his first morning the care paragraph and each child's room. The old arm's morning (a night run, then
  `turn_prompt`): *You are fed. You carry: ... / Last night you ate 3.8 roots from Marsh House's store, in the usual order (what
  needs no fire, then what spoils soonest): you ate your fill. / For the whole household's meal, Marsh House's store gave 15.2
  roots in all.*

## Seen in passing (not changed)

- "The Marshs household has no standing rules yet" (`book.rules_block`: the household's name with an "s" added).
- "at Eelmouth Fen (which the Brooks holds)": "hold".
