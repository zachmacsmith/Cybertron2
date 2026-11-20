---
id: docs/review/37_growth/02zzo_weather_conditions.md
kind: note
updated: "2026-11-16"
---
# 02zzo: the weather across conditions, and what the engine leaves unread

*note · `docs/review/37_growth/02zzo_weather_conditions.md`*


37.2, 16 Nov 2026. WORK [[W-51 The weather across conditions|W-51]]. Zach: "try test the weather in different conditions, like dry places, high mountains, flood plains,
the coast etc to see that it makes sense across these". Then, on seeing the first result: "weather should DEFINITELY NOT be
independent from the generator? How many other things are generated but not used?" ([[D2-220 The weather takes each place's climate from the generated land|D2-220]].)

- **Script:** `02zzo_weather_conditions.py`. It generates six worlds without people and compares the generator's climate at each
  node with the engine's weather there over 20 engine years, put per real year. It then runs 02zzn's water on the two clocks
  ([[D2-214 Two clocks|D2-214]]) at each settlement, and the engine's weather at set heights.
- **Results:** `02zzo_weather_conditions.json`.

## 1. What the test shows

The engine's weather (`climate.py`, [[D4-109 The weather scheduler|D4-109]]) reads one thing about a place: its height. That sets a lapse of 6.5 °C a km, wet days
that grow more frequent uphill (+0.15% a metre), and more wind uphill. It does not read:
- the generator's rain at the node (`rain_mm`, written to every node, rain shadows included);
- the world's temperature (`temperature_c`, its north to south gradient);
- the prevailing wind;
- the sea's distance.

So every condition gets the same lowland weather:

| Condition | A settlement: the generator's climate | The engine's weather there |
|---|---|---|
| Lowland (default) | 730 to 890 mm, 8.3 to 9.0 °C | about 1,000 mm, 9.4 °C; winter 3.2 °C, summer 15.8 °C; frost on 60% of winter nights |
| Dry (500 mm, 10 °C) | 390 to 480 mm, 9.0 to 10.1 °C | the same: about 1,000 mm, 9.4 °C |
| Cold north (6 °C) | 630 to 650 mm, 5.0 to 6.0 °C | the same: 9.4 °C; winter 3.2 °C |
| Coast, 3 km from the sea | 730 to 920 mm | the same as 99 km inland: no milder winter, no fewer frosts, no more wind |
| The range's wet windward fells, 440 to 500 m | 2,270 to 3,470 mm, 5.5 to 6.4 °C | 1,150 to 1,210 mm, 6.7 °C: temperature right (both lapse), rain a third to a half |
| Fen floodplain | 707 mm, 8.8 °C | about 1,000 mm, 9.6 °C |

- **Water follows the weather, not the climate.** On the two clocks, the dry world's rivers spate and flood as often as the wet
  world's: spates 4.6 days a year, floods 2.3 at the first settlement in both. Its soil dries on the same 12 days.
- **The same seed means the same weather,** whatever the world says its climate is.
- **Even the default is off.** The engine's lowland rain is about 1,000 mm a real year, against the generator's 730 to 890.

**By height alone** (the lowland world, its nodes set to 0, 250, 500, 1,000 and 1,500 m):

| | 0 m | 500 m | 1,000 m | 1,500 m | A real check |
|---|---|---|---|---|---|
| Mean temp | 9.7 | 6.4 | 3.2 | −0.2 | Great Dun Fell (847 m) about 4 °C; Cairngorm summit (1,245 m) about 1 °C: right |
| Winter frost nights | 56% | 83% | 97% | 100% | plausible |
| Snow among days | 2% | 10% | 28% | 42% | plausible |
| Rain a real year | 990 | 1,190 | 1,220 | 1,310 mm | British fells 2,000 to 4,000 mm: far too little; the generator gives 2,300 to 3,500 |
| Mean wind | 5.2 | 9.7 | 14.1 | 18.6 m/s | high summits 10 to 16 m/s: a little high at the top |

- **What height gets right:** temperature, frost, snow and wind.
- **What it gets wrong:** rain. Height raises only how often it rains, and that odds cap is reached early, so hill rain never
  builds.

**Floodplains:**
- In the fen world, which the generator does not cut into valleys, 56% of Mosswick's land is within 2 m of its river. The river
  stands a metre up on about 6 days a year there, so the meadows would flood.
- In river country (lowland, dry, cold, mountains), at most 0 to 48% of a settlement's land is near the river's level, and mostly
  none. This is 02zzn's trench, still open ([[Q-52 Environment systems|Q-52]] (8)).

**Ice:** as 02zzn found. Cold enough for ice only above about 500 m, or in a world that is really colder. The cold north is not
colder in the engine until the weather reads the land.

## 2. What else is generated and not used

Checked against the engine, `wild/` and `capacity/` on main and on `ecology-water` (48e418e), at the places each field is read.
02zzl §1 had most of this; it has changed only where brief 5 now reads `down` and river lengths.

**Never read:**
1. The node's rain a year (`rain_mm`), with its rain shadows and wet fells.
2. The world's temperature, its north to south gradient, and the prevailing wind. These are not written to the node at all.
3. The sea's distance, for weather. It is read only by coastal plants (`wild/plants.py`).
4. A parcel's `land.drain_rate`, `land.exposure` and `land.rain_factor`.
5. A parcel's `land.depth` (soil depth) and `land.elevation`. Weather takes the node's height; nothing takes the parcel's.
6. A parcel's `terrain` (river floodplain, clay vale, chalk down, moor, and so on). Roads have their own.
7. The cells file (`.cells.npz`, the land at 150 m; [[D2-208 The world keeps the land it runs on|D2-208]] decided the world keeps it). The engine never loads it. With it go
   moisture, slope, springs, height above the river, area drained and the cell-level soil.
8. Farming's wet ground ([[D2-66 Field works in the first worlds, before weather exists|D2-66]]) reads a parcel key `ground` that the generator never writes.

**Read only thinly:**
- `land.texture`: only by slugs and moles, through areas. Farming reads fertility, not the soil's kind.
- `land.held_mm`: only as "wet" (260 mm or more) for wild plants.
- `land.position`: wild plants, and the night's damage to low houses.
- An area's `temp`, `elevation`, `wet`, `rock` and `old_wood_km2`: the ecology's habitat features only.
- Height above the river: only as the rank that lets heavy rain damage low houses.

**Read as meant:** base fertility ([[D4-112 The land's base fertility, multiplicative|D4-112]]), cover and ecosystem, river class, the drainage `down` and river lengths (brief 5),
node height (temperature) and position (storms).

**So the engine does not know, though the land holds it:** where it rains more and less; how warm the world is; where the coast
is; which way the wind blows; how much water a soil holds and how fast it drains; how deep it is; how exposed or steep the
ground is; where springs rise; and how high ground stands above its river.

## 3. What follows

- **Climate from the land ([[D2-220 The weather takes each place's climate from the generated land|D2-220]]):** design in `docs/cybertron2/proposals/climate_from_land.md`.
- **The rest of the list:** this is environment_systems.md's phase 0 (the engine reads the land's fields). Its order is OPEN [[Q-56 The land the engine reads|Q-56]].
