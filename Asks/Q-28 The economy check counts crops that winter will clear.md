---
id: Q-28
kind: ask
state: open
owner: "37.2"
updated: "2026-11-20"
tags: [ask, open]
---
# The economy check counts crops that winter will clear.

- **state**: open
- **owner**: 37.2
- **where**: review 38.59 §5; cybertron2/landgen/economy.py

## Text
**The economy check counts crops that winter will clear.** landgen/economy.py counts every standing crop whose `ripe_day` falls within the run, but the engine clears unripe crops when winter begins. The takeover world (38.59) passed with food 881 of 720; its Bottom Field (oats, ripe day 34) was cleared on day 14, and both 60-day runs starved from day 20. Proposed: count a crop only if it ripens before the next winter's start; also count stores lost to spoilage out of doors. The same world's 881 also held 206 from 'fields after a year' (every field resown and reaped in full by day 60: in the run, three plots of 15 to 18 were sown and the last was cleared by the second winter a day before it ripened) and 131 from the woods' flow; store and reapable crops were 383, about 29 days for 13. A crop's `ripe_day` past the next winter should also be refused when the world is written: the engine recorded this one as sown on day 26, in the future. 7 Nov (37.4): cybertron2/capacity ([[D4-102 Carrying capacity is measured, by level, from the engine's own|D4-102]]) now gives the land's ratio by level, the buffer, the first own harvest and the crops the frost takes first, from the engine's own rules; proposed that the economy check call it (capacity.model.analyse, run_horizon) in place of its fixed numbers

## Mentioned by
- [[D4-102 Carrying capacity is measured, by level, from the engine's own|D4-102: Carrying capacity is measured, by level, from the engine's own rules:]]
- [[carrying_capacity Carrying capacity what a world's land feeds and keep|Carrying capacity: what a world's land feeds and keeps warm,]]
- [[generation_redesign Proposal world generation as one history, with pin|Proposal: world generation as one history, with pins met in ]]
- [[process_model A declared process model the engine says what its econom|A declared process model: the engine says what its economy i]]
- [[02zz_open_sorting 02zz sorting OPEN.md's open rows into the new kinds|02zz: sorting OPEN.md's open rows into the new kinds (draft,]]
- [[replies_2_audit Audit of 37.2's replies, 9 to 19 Nov 2026 commitments|Audit of 37.2's replies, 9 to 19 Nov 2026: commitments and s]]
- [[59_lordship_and_violence_design 38.59 Exploratory runs taking over a v|38.59: Exploratory runs: taking over a village, an Orwellian]]
