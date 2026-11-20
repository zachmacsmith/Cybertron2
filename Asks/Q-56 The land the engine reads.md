---
id: Q-56
kind: ask
state: open
owner: Zach (37.2, 37.4)
updated: "2026-11-20"
tags: [ask, open]
---
# The land the engine reads

- **state**: open
- **owner**: Zach (37.2, 37.4)
- **where**: docs/cybertron2/proposals/climate_from_land.md; docs/review/37_growth/02zzo_weather_conditions.md

## Text
**The land the engine reads** (16 Nov; 02zzo): (1) climate from the land as revised 17 Nov ([[D2-220 The weather takes each place's climate from the generated land|D2-220]] in principle): two levels, the region's parameters (type mix, seasons, rain, storms; eras act here) and each place's response to each type, both from the land; built now as one derived profile (the generator writes node `temp_c`, `sea_km`, `exposure` and the world's climate; the scheduler reads the profile where it reads constants now; old worlds replay the same), the deep weather later in the same seams?; (2) the order for the rest of what the generator makes and the engine leaves unread (02zzo §2): 37.2 recommends climate first, then the soil's water from `held_mm`, `drain_rate`, `depth` and texture on the two clocks ([[D2-214 Two clocks|D2-214]]), then farming reading texture, depth and wet ground ([[D2-66 Field works in the first worlds, before weather exists|D2-66]]'s `ground`, never written), then exposure and slope, then the cells file loaded ([[D2-208 The world keeps the land it runs on|D2-208]]); parcel `terrain` as words only?

## Mentioned by
- [[D2-220 The weather takes each place's climate from the generated land|D2-220: The weather takes each place's climate from the generated land]]
- [[W-49 Environment systems (Zach, 16 Nov) the gaps between what the gene|W-49: Environment systems (Zach, 16 Nov): the gaps between what the generato]]
- [[W-51 The weather across conditions (Zach, 16 Nov try test the weather|W-51: The weather across conditions (Zach, 16 Nov: "try test the weather in ]]
- [[calibration_worlds Calibration worlds a suite of diverse places to cal|Calibration worlds: a suite of diverse places to calibrate a]]
- [[climate_from_land Climate from the land|Climate from the land]]
- [[02zzo_weather_conditions 02zzo the weather across conditions, and what|02zzo: the weather across conditions, and what the engine le]]
- [[period_c Period C audit 12 to 19 Nov 2026 (session 37.2)|Period C audit: 12 to 19 Nov 2026 (session 37.2)]]
- [[records Records audit what the documents say against what is true (19|Records audit: what the documents say against what is true (]]
- [[replies_2_audit Audit of 37.2's replies, 9 to 19 Nov 2026 commitments|Audit of 37.2's replies, 9 to 19 Nov 2026: commitments and s]]
