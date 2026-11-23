---
id: docs/review/37_growth/02zzzh_hunt_fish/spring_gap.md
kind: note
updated: "2026-11-23"
---
# Where live run 1's spring gap lies (set B, the rebuilt arm)

*note · `docs/review/37_growth/02zzzh_hunt_fish/spring_gap.md`*


Session 37.2, 23 Nov 2026, at Zach's question after [[D2-347 A water-only village should be able to last the year|D2-347]] ("It should be possible for a water only village to last the year. Where
does the gap currently lie?"). Read from /home/user/live1/live1_B_new: the checkpoints (`run.db`, the river's nightly record
`wild.river.Eelmouth.passed`, the reach's resident stock `waters["reach:Eelmouth"].fish`), `days.jsonl` and `turns.jsonl`;
food by `live1_worlds/food_ledger.py`. Ten people need about 11 food a night (12 in winter).

## The year as it ran (run day 0 is summer day 4; a season is 8 days)

| Days | Season | What passed the village (heads) | Stored food (day's end) |
|---|---|---|---|
| 0 to 6 | late summer | nothing | 91 falling to 43 (the founders' stores) |
| 7 to 18 | autumn, early winter | eels 1,607; salmon 375 (days 9, 12) | 55 rising to 193 (day 12), 118 (day 18) |
| 19 | winter | salmon 287 | 152 (day 20) |
| 20 to 38 | late winter, spring, summer | lampreys 23 in all (days 25, 28, 31) | 124 (day 22), 60 (28), 34 (32), 10 (36), 4 (38) |
| 39 | autumn | eels 79: the next run begins | |

Deaths: two on day 34, one on day 35, one on day 38 (the salt household).

## Four parts of the gap

1. **The river's calendar leaves 19 days with no run.** After the winter salmon (day 19) nothing ran until the eels of the next
   autumn (day 39), save 23 lampreys. A real lowland river's spring has a lamprey run, and coarse fish spawning in the shallows.
2. **The resident fish are about 9 kg a reach.** The reach's stock is K 8.8, r 0.3, in kilograms (Margery's 4.1 kg on day 29 took it
   from 7.6 to 3.5). Its best sustained yield is r K / 4, about 0.66 kg a night, or 0.3 food: about 3% of the village's need. The
   shallows gave 0 to 0.3 kg a take. [[D2-316 A runs world means a water-only world|D2-316]] asks for "small" stocks, "not enough to support the population sustainably"; at this
   size they are effectively nothing. They also recovered untouched through spring (S 3.8 to 7.6, days 21 to 28) while the
   stores ran down, then were fished out in two days.
3. **What was taken was not kept long enough.** At the peak (day 12) the stores held 193 food; reaching day 39 needed about 300. The
   glut spoiled about 170 kg of fish (about 78 food) on days 10 to 12. Most of what was kept was smoked (about 530 kg hung), which
   loses a quarter in about ten nights (keeping smoke) and cannot carry 27 nights; salt fish (about 34 nights) and dried fish
   (about 41) would, and need salt, racks and hands.
4. **Most of the run went past.** About 1,030 kg of fish is named in takes during the run, of roughly 3,100 kg passing (eels about
   0.6 kg a head, salmon about 3.3, from the trap rows in data.py); the weir's "more came down than its traps would hold" was shown
   19 times in set A's new arm.

So the water carried far more than the year's need (about 1,400 food passed against about 350 a year), but it all came in one
autumn and winter, and the village has nothing to fall back on in spring when its keeping falls short. Shortfall: roughly 100 to 150
food, five to seven days of the village.

## A wording fault found on the way

Every take says "(food worth about 1 meal)" at the least (`placed.py:224`, `placed.py:374`, `verbs.py:900`: `max(1, round(food))`),
so 0.1 kg of small fish (0.05 food) reads as a meal: 80 times in this arm. It tells people the shallows feed them when they do not.
