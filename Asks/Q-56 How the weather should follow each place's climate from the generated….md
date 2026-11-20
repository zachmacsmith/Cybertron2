---
id: Q-56
kind: ask
state: open
updated: "2026-11-20"
---

# How the weather should follow each place's climate from the generated… (Q-56)

*open · Zach (37.2, 37.4)*

## The question
**The land the engine reads** (16 Nov; 02zzo)
1. climate from the land as revised 17 Nov ([[D2-220 The weather takes each place's climate from the generated land|D2-220]] in principle): two levels, the region's parameters (type mix, seasons, rain, storms; eras act here) and each place's response to each type, both from the land; built now as one derived profile (the generator writes node `temp_c`, `sea_km`, `exposure` and the world's climate; the scheduler reads the profile where it reads constants now; old worlds replay the same), the deep weather later in the same seams?
2. the order for the rest of what the generator makes and the engine leaves unread (02zzo §2): 37.2 recommends climate first, then the soil's water from `held_mm`, `drain_rate`, `depth` and texture on the two clocks ([[D2-214 Two clocks|D2-214]]), then farming reading texture, depth and wet ground ([[D2-66 Field works in the first worlds, before weather exists|D2-66]]'s `ground`, never written), then exposure and slope, then the cells file loaded ([[D2-208 The world keeps the land it runs on|D2-208]]); parcel `terrain` as words only?

**Where:** docs/cybertron2/proposals/climate_from_land.md; docs/review/37_growth/02zzo_weather_conditions.md


## Mentioned by
- [[D2-220 The weather takes each place's climate from the generated land|The weather takes each place's climate from the generated land (D2-220)]]
- [[W-49 Environment systems|Environment systems (W-49)]]
- [[W-51 Testing the weather across dry, cold, coastal and mountain worlds…|Testing the weather across dry, cold, coastal and mountain worlds… (W-51)]]
- [[Calibration worlds a suite of diverse places to calibrate against|Calibration worlds: a suite of diverse places to calibrate against]]
- [[Climate from the land|Climate from the land]]
- [[Subsistence worlds can each livelihood keep a village on its own|Subsistence worlds: can each livelihood keep a village on its own?]]
- [[02zzo the weather across conditions, and what the engine leaves…|02zzo: the weather across conditions, and what the engine leaves…]]
- [[Audit of 37.2's replies, 9 to 19 Nov 2026 commitments and switches|Audit of 37.2's replies, 9 to 19 Nov 2026: commitments and switches]]
- *and 3 index or audit notes*
