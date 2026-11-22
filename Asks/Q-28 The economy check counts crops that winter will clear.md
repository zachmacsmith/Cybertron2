---
id: Q-28
kind: ask
state: open
updated: "2026-11-22"
---

# The economy check counts crops that winter will clear (Q-28)

*open · 37.2*

## The question
landgen/economy.py counts every standing crop whose `ripe_day` falls within the run, but the engine clears unripe crops when winter begins. The takeover world (38.59) passed with food 881 of 720; its Bottom Field (oats, ripe day 34) was cleared on day 14, and both 60-day runs starved from day 20. Proposed: count a crop only if it ripens before the next winter's start; also count stores lost to spoilage out of doors. The same world's 881 also held 206 from 'fields after a year' (every field resown and reaped in full by day 60: in the run, three plots of 15 to 18 were sown and the last was cleared by the second winter a day before it ripened) and 131 from the woods' flow; store and reapable crops were 383, about 29 days for 13. A crop's `ripe_day` past the next winter should also be refused when the world is written: the engine recorded this one as sown on day 26, in the future. 7 Nov (37.4): cybertron2/capacity ([[D4-102 Carrying capacity is measured, by level, from the engine's own rules|D4-102]]) now gives the land's ratio by level, the buffer, the first own harvest and the crops the frost takes first, from the engine's own rules; proposed that the economy check call it (capacity.model.analyse, run_horizon) in place of its fixed numbers

**Where:** review 38.59 §5; cybertron2/landgen/economy.py


## Linked
- bears on: [[W-54 The twelve calibration worlds and an audit of the generator across…|The twelve calibration worlds and an audit of the generator across… (W-54)]]


## Mentioned by
- [[D4-102 Carrying capacity is measured, by level, from the engine's own rules|Carrying capacity is measured, by level, from the engine's own rules (D4-102)]]
- [[Carrying capacity what a world's land feeds and keeps warm, by…|Carrying capacity: what a world's land feeds and keeps warm, by…]]
- [[Proposal world generation as one history, with pins met in the loop|Proposal: world generation as one history, with pins met in the loop]]
- [[A declared process model the engine says what its economy is, as…|A declared process model: the engine says what its economy is, as…]]
- [[Audit of 37.2's replies, 9 to 19 Nov 2026 commitments and switches|Audit of 37.2's replies, 9 to 19 Nov 2026: commitments and switches]]
- [[38.59 Exploratory runs taking over a village, an Orwellian aim, and…|38.59: Exploratory runs: taking over a village, an Orwellian aim, and…]]
- *and 2 index or audit notes*
