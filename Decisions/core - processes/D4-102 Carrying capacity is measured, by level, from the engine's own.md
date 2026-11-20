---
id: D4-102
kind: decision
state: live
updated: "2026-11-20"
tags: [decision, open]
---
# Carrying capacity is measured, by level, from the engine's own rules:

- **state**: live
- **source**: conversation ("Is there already a built in engine module that analyses the lands carrying capacity etc.? If not, build this (as an abstracted, well modularised system that can improve easily as we grow new systems / mechanics) and run this on the worlds and past worlds"; and the follow-ups on fuel, labour, capital, expansion and "the underlying physics ... the carrying capacity changes to reflect that")
- **replaces_text**: the economy check's fixed numbers (engine/capacity.py PLOT and WILD, landgen/economy.py) stay for 37.2 to replace (OPEN [[Q-28 The economy check counts crops that winter will clear|Q-28]])

## Text
**Carrying capacity is measured, by level, from the engine's own rules:** cybertron2/capacity reports, for each node and the region, the people the land feeds for good at five levels (bare, as it stands, worked, best, ceiling) as a ratio to the people there; fuel as its own need; stores as a buffer with the days to the first own harvest and the crops the frost takes first; a run's horizon; each level's work and capital (a production graph of every technique); space (reach, expansion outward). The night's rules become pure engine functions both call (regrow, spoil_rate, crop_base, frost_kills and others), with agreement and guard tests (spec/measurement/capacity.md)

## Mentioned by
- [[Q-28 The economy check counts crops that winter will clear|Q-28: The economy check counts crops that winter will clear.]]
- [[carrying_capacity Carrying capacity what a world's land feeds and keep|Carrying capacity: what a world's land feeds and keeps warm,]]
- [[descendants_benchmark A benchmark by living descendants, on a ladder o|A benchmark by living descendants, on a ladder of worlds]]
- [[economic_calibration Economic calibration one time scale, and mechanic|Economic calibration: one time scale, and mechanics that mak]]
- [[generation_redesign Proposal world generation as one history, with pin|Proposal: world generation as one history, with pins met in ]]
- [[living_populations Proposal living populations on the land (a generali|Proposal: living populations on the land (a generalised ecol]]
- [[process_model A declared process model the engine says what its econom|A declared process model: the engine says what its economy i]]
- [[processes The declared process model|The declared process model]]
- [[capacity Carrying capacity|Carrying capacity]]
- [[02zze_wild_region 02zze a wild region with dependence four villages, o|02zze: a wild region with dependence: four villages, one ric]]
- [[02zzh_economy_layers 02zzh the economy's layers and trees of dependenc|02zzh: the economy's layers and trees of dependence, across ]]
- [[02zzi_economies_scaling 02zzi how an economy could scale beyond the me|02zzi: how an economy could scale beyond the medieval villag]]
- [[08_later_paradigms 08 the technology paradigms after the first industr|08: the technology paradigms after the first industrial revo]]
- [[09_engine_mapping 09 Mapping economic layers onto the engine, from for|09: Mapping economic layers onto the engine, from foragers t]]
- [[60_capacity_model 38.60 Carrying capacity the model, the worlds, and e|38.60: Carrying capacity: the model, the worlds, and every p]]
- [[69_peoples_worlds 38.69 Worlds for the peoples benchmark (design, for|38.69: Worlds for the peoples benchmark (design, for discuss]]
