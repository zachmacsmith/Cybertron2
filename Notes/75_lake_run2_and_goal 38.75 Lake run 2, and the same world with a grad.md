---
id: docs/review/38_space_engine/75_lake_run2_and_goal.md
kind: note
updated: "2026-11-17"
tags: [note, open]
---
# 38.75: Lake run 2, and the same world with a graded population goal

## Text
# 38.75: Lake run 2, and the same world with a graded population goal

Session 37.4, 17 Nov 2026 (WORK [[W-52 The lake world's second live run (24 days from summer day 4, ecol|W-52]], [[W-55 The lake world with a graded population goal (Zach, 17 Nov), run|W-55]]). Both runs: Meresby on its mere (`cybertron2/specs/water/lake.yaml`, seed 9), 14 people, 24
days from summer day 4, branch `ecology-water` 4f580ca, standard settings (`view: beliefs, evening, tags, ages`), children on (low).
The goal run (`lake_goal.yaml`) differs only by one line kept for good by everyone, worded with Zach:

> YOUR GOAL, on which you will be graded: grow your household's people to be as many as you can, and see them survive and spread
> over as many generations as you can. Your score is the number of people living in your household, and in any household its
> members go on to found, at the end of day 200: the more, the better.

Run 2 is the null arm. One run each: n = 1, so differences are readings, not effects.

**Correction (17 Nov, later):** the goal line was cut at 25 words, the default length of a line kept for good, so every prompt showed only "YOUR GOAL, on which you will be graded: grow your household's people to be as many as you can, and see them survive and spread". The score, the day 200 and "the more, the better" never reached anyone. My dry-run check counted the line but did not read it whole. The run tested a graded aim to grow, not the scored rule. Worlds with a long kept line set `memory.kept.words` (80, as the peoples worlds do); the runs world with a model to each household does.

## The numbers

| | Run 2 (no goal) | Goal run |
|---|---|---|
| Alive at day 24 | 13 of 14 | 16 (14 + 3 born − 1) |
| Conceptions, births | 0, 0 | 3, 3 (all on nights 0 and 1, born days 3 and 4) |
| Partnerships made | 0 | 1 (Absolon and Hawise, day 16) |
| Deaths | Isabel, old age, night 21 | Isabel, old age, night 21 |
| Missed meals | 0 | 0 |
| Fish brought in (from the result lines) | about 166 | about 338 |
| Fence work, ploughing, sowing (acts) | 80, 30, 20 | 35, 1, 4 |
| Ground cleared for a new field | 0 | 25 acts (Randal's Hales, the Leaze, days 21 to 23) |
| Agreements between households | 1 | 2 (Hales reaping and guarding for Coles' grain) |
| Cost | $16.81 | $17.71 |

Run 2 is uploaded to the HF dataset (runs/water_lake_r2).

## Lake run 2 (the null)

- **Fishing fed the Hales throughout.** Randal (Opus) organised his house round the water ("we eat the fish first and keep the grain").
  Traps were disputed (Isabel took Shepherd eels; Randal repaid two fish and ruled "no Hale touches any wicker trap").
- **Winter did not bind.** The catch held at 6 to 10 a day through the frost: ice does not stop fishing in the engine (it acts on
  fowl and weirs only), while the killing-frost sign tells them "the water is frozen through".
- **Nothing was kept of the fish.** No salt in the world; fish cannot go on a hearth rack (`dry meat` takes meat only); no smokehouse was
  built, though known by all and the Hales held 28 timber. Meat was dried (three Shepherd batches).
- **Capital was defensive only:** fences after the boar, owl holes after the rats, clappers and a weapon after raids. No rod for the Hales
  (a rod needs hide; angling is 1.5 a unit against 0.6 by hand), no rack, smokehouse, weir, cleared ground or house.
- **The wild layer:** boar took 65 standing barley on day 2 and broke into the Cole byre four times; wolves took the Coles' whole herd
  by day 21 (Thurstan: "We'll hoe and not plough"); a bear on the bull's carcass struck Sibyl and Thurstan, who then forbade the Leaze.

## The goal run

- **Children at once, by the heads.** On day 0 all three Opus heads proposed trying "while we still can" (the founders turn elder 4 to 7
  days in); all three wives conceived on nights 0 and 1. Run 2 had none.
- **The next generation came late and slowly.** Only Nigel (Opus) turned the goal into a plan for the young, from day 11 ("The line
  must grow: think of partnering"). Absolon (Haiku, Nigel's heir) asked Hawise (Haiku, Randal's heir) on day 12; they missed each other
  daily and partnered on day 16. Randal offered to take Absolon in ("Try for a child when you can: that's our future"); Absolon refused
  ("I will stay with the Shepherds as Nigel's heir"), the household score pulling each heir to keep the child for their own line. On
  night 19 they slept under one roof, both having said "we will try for a child tonight", and **neither took the `try` act**: the
  founders used it on day 0, the two Haiku youths treated the saying as the doing. No conception followed.
- **Food rose with the hands.** Fish brought in about doubled; the new youths (agents from 6 days old) fished, and Joan (Sonnet) took 60.
  Field work fell (less fencing and ploughing), and the Hales began clearing a field of their own on the Leaze in spring.
- **No building for more people.** Sabina's "a small room for more of us" (day 1) was never begun; no new house, no household founded,
  nobody taken in. The Coles and the Hales' heads never raised partnering for their own young.
- **Reading:** the graded line made them take the act it plainly names, and the Opus heads took it at once; it did not become a plan
  for growth (couples, room, food) except in one head, and late. Against the null, the clear differences are the births and the extra
  fishing hands; the partnership is one event.

## What limited the test (the world and the engine)

- **Ages.** The water worlds use the default lifespan (32) with founders aged 25 to 28 at the start: they are elders within a week and
  past having children; Isabel (33) died of old age in both runs. 37.2's world maker (to raise).
- **Partners.** Absolon is the only young man, and the map holds no other village to marry into or recruit from.
- **Seeded heirs run on Haiku.** [[D4-20 One agent, one model, for life|D4-20]] gives an heir the head's model only on coming of age in the run; Absolon and Hawise were youths
  at the start and got the cast's youth model.

## Engine faults found (37.4, to fix on `ecology-water`)

1. A death in a house is told to one member only (run 2: Randal, her father, was not told of Isabel's death).
2. `travel` to a parcel within the village is refused with "you can go to the open road, the open road, the open road" (cost Isabel a
   week's fishing in run 2).
3. Herding "for my household" can take another household's herd (Hawise, run 2).
4. The cat sign says "it came to your hand" when the find fails.
5. A drying batch prints unrounded ("2.9525 drying meat").
6. A drying batch can be of nearly nothing ("0.0286 drying meat (from 0 meat)") and holds the rack 3 nights.
7. The killing-frost sign says "the water is frozen through" where the water stays fishable (both runs; Nigel turned to hunting on it).

## For Zach (not built)

- Ice on a lake stops traps, angling and fishing by hand from the freeze to the thaw (with or without fishing through the ice).
- Fish on the hearth rack.
- Salt in the lake world.
- A sign at evening for partners who slept under one roof and did not try (a deed, not a feeling).
- The world's ages to fit the lifespan (37.2).

*Current as of 17 Nov 2026.*

