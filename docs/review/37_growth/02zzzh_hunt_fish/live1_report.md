# Live run 1: the rebuilt fishing world against the old prompt and the engine before the rebuild

Session 37.2, 23 Nov 2026 (thread W-101; plan live1_plan.md; D2-333 to D2-335). Read qualitatively, one seed each (D2-335). Every
arm is published to the Hugging Face dataset; the run directories are /home/user/live1/<arm>; the readings come from
live1_worlds/compare.py and food_ledger.py.

## The arms

| Set | Arm | World and engine | Days | Alive at the end |
|---|---|---|---|---|
| A (8 play) | pre | the engine before the rebuild (f728a3b7), the old runs world | 18 | 11 (a child died) |
| A | old | rebuilt engine and Eelmouth, the old prompt, no new seeded lines | 18 | 13 (a birth) |
| A | new | rebuilt engine and Eelmouth, the new core, shapes and seeded lines (after the W-102 fixes) | 18 | 12 |
| B (6 play) | pre | the engine before the rebuild, two households | 40 | 6 |
| B | new | rebuilt, new prompt, two households (the weir; the salt) | 40 | 6 |
| A, B | bots | each world with bots (interfaces only, D2-298) | 18, 40 | |

A first new-prompt arm was stopped at day 10 for interface faults (213 refusals; no rule ever set; lessons and sleep dropping
their arguments; free acts refused after work); fixed in W-102, then rerun.

## What changed

**Taking.** Before the rebuild traps were set and almost never tended (set A: 46 sets, 10 tends in 18 days; set B: 230 kg of fish
lay in one un-lifted set on day 16). Rebuilt: tends outnumber sets (old prompt 27 / 90; new prompt to day 8, 15 / 48); fish named
in takes to day 8: 61 kg before, 118 kg old prompt, 159 kg new prompt.

**Keeping.** Before the rebuild fresh fish barely spoiled in stores (77 food of fresh fish still held on day 17). Rebuilt, fish goes
off (D2-336) and they preserve: set A by day 17, 207 food of preserved fish (old prompt), 172 (new prompt); about 530 kg hung to
smoke, 83 kg salted, 77 kg dried at the hearth (old prompt). The glut cost them: 41 food spoiled on day 9 (old prompt), 24 (new).

**Signs.** The run's leads fired and were acted on: the dawn cue "the dark nights of the autumn come, and the river full: an eel
night" (Peter, day 6: "Tonight is an eel night ... the weir and the traps matter most"); the news then spread by talk at the hearth
("The silver eels are running down the Isel. These are our winter food"). "dark eels" 28, "silver eels" 30, "eel night" 36 in the
old-prompt arm's prompts; none before the rebuild.

**Households.** Rebuilt, each plays its holding: the Brooks treat salt as their currency ("The Marshs' fish is spoiling for want of
salt, which is my chance to trade salt for their eels"); the Marshes trade fish for it; the Shepherds set traps in the fen dykes
"which hold in a spate" and dry at the hearth. Before the rebuild they raced each other to the traps ("before Oliver or the otter
gets there") and took from each other's weir.

**Teaching.** Set B rebuilt: 10 lessons, two across households (Peter, of the weir, taught the Brooks' Katherine and Margery the
wicker traps); set B before the rebuild: 1 in 40 days. Passing a line on in care was almost unused (0 to 2 an arm, and none of
the seeded lore).

**Rules.** New prompt: 29 and 32 rules, mostly meal orders and members' chores; revised from what they saw ("change rule 2 to eat
the salt fish first"); talked over at the evening once (Basilia asks, Oliver sets it, she follows "as your rule sets"). No rule
used "when" or "unless", "share" or a named set. A chore that yields nothing fires on ("twist cord: 0" 130 times in set B).

**Building.** Nothing new built in any arm: repairs (weir sections, houses, the Salt House), owl holes against rats; no more racks
after the glut, no store when the houses filled.

## The spring gap (set B)

Before the rebuild the salt household starved during the run (Petronel day 17, Oliver 21, Margery 23) beside the un-lifted fish.
Rebuilt, both households lived through the run and the winter on traded and preserved fish (118 food on day 18); the stores ran
down through spring (47 on day 30, 6 on day 37) and the salt household starved at the end of the gap (Basilia and Margery day 33,
Petronel 34, Katherine 37), while Marsh House held 67, 39, 23 food on days 26, 30, 33 and rationed its own ("only about 2.5 nights
of smoked fish"). The salt-for-fish trade that carried them in autumn failed in spring: with no catch to salt, salt bought nothing
("we have plenty of those and nothing else"). The next run began about day 38. Water alone did not carry ten people to it.

## For after the runs (flagged)

Passing on through care made plain, seeded and kept for every carer (D2-340); a chore or fallback that yields nothing stops and is
shown; one worked example of a conditional rule in the rules block; lessons settled before the evening (L-175); the signs survey
and design (W-103); noticing within the day (L-176, with timed acts). For Zach: whether a water-only village should last the year,
or the spring gap is the point.
