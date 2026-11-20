---
id: docs/review/37_growth/02zzn_environment_prototype.md
kind: note
updated: "2026-11-16"
tags: [note, open]
---
# 02zzn: the water half of the environment, prototyped on the river world

## Text
# 02zzn: the water half of the environment, prototyped on the river world

37.2, 16 Nov 2026. WORK [[W-49 Environment systems (Zach, 16 Nov) the gaps between what the gene|W-49]], OPEN [[Q-52 Environment systems|Q-52]], proposal `docs/cybertron2/proposals/environment_systems.md`. Not engine code.

- **Script:** `02zzn_environment_prototype.py` (`python3 02zzn_environment_prototype.py <world.yaml> [years] [era]`).
- **Results:**
  - `02zzn_environment_prototype.steady.json` (the world's own steady era, 20 engine years);
  - `.cold.json` (the cold era, same seed).
- **World:** brief 5's river world (`cybertron2/specs/water/river.yaml`, seed 9). Saltwell sits 34.6 km of river above Millham, with
  three small wild settlements (w1 to w3).

## 1. What it runs

The prototype reads only what the generator already writes and what the engine already makes:
- the areas, links and `down`;
- the parcels' `land`;
- the cells' height above the river (`f`);
- the engine's weather by place (`climate.py`, [[D4-109 The weather scheduler|D4-109]]).

On these it runs the fast stocks agreed on 8 Nov:

- **Soil water:** one bucket per area. Its capacity comes from the texture shares × the generator's AWC × depth. Rain comes in and
  evaporation goes out (0.15 mm a day per degree). The share leaving for the river stores rises with wetness, as (soil / capacity)³
  (the HBV form). Rain over 12 mm a day on loam (scaled by drain rate) runs straight off. Woods hold back 15% of rain and 30% of
  the fast store's outflow.
- **Snow** lies at or below 1 °C and melts at 3 mm a day per degree.
- **Two river stores:** fast (0.35 a day) and slow groundwater (0.01 a day).
- **Reaches:**
  - each village's home and ring together form one reach, and each wild area is one reach;
  - runoff goes down `down`, arriving after (river km ÷ 15) days, at least one;
  - stage above normal water = 1 m × ((flow / median)^0.4 − 1);
  - bands relative to the median flow: dry < 0.3, low < 0.6, normal < 2, high < 4, spate < 8, flood above.
- **Floods by height:** a parcel's land is under water when the stage is above its cells' `f`.
- **Ice** on still water by Stefan's law, 2.7 √(frost degree-days) cm.

Every rate is a first value (calibrate).

**Two clocks.** An engine year is 32 days, while daily rates are real (02zp §15; 37.4's 38.64 §6.7). So the prototype runs twice:

- **One clock:** every rate is real per engine day.
- **Two clocks:** the seasonal stores (evaporation, soil, groundwater, snowmelt) move 11.4 days per engine day on the season's mean
  rain, and the day's rain above that mean runs through the fast store at real rates. 11.4 is 365 ÷ 32. A storm is still one day;
  a summer is still a summer.

## 2. What it shows (steady era, 20 engine years)

| | Millham, 1 clock | Millham, 2 clocks | Saltwell, 1 clock | Saltwell, 2 clocks |
|---|---|---|---|---|
| Days a year dry / low | 0 / 1.6 | 7.5 / 4.3 | 0 / 1.6 | 8.2 / 3.9 |
| Days a year high / spate / flood | 3.7 / 1.3 / 0 | 5.8 / 2.6 / 1.4 | 2.5 / 1.4 / 0 | 5.0 / 2.9 / 1.9 |
| Spates, floods begun a year | 0.25, 0 | 0.8, 0.25 | 0.3, 0 | 1.05, 0.35 |
| Days a year the river stands 1 m / 1.5 m above normal | 0.2 / 0 | 2.7 / 0.8 | 0.45 / 0 | 2.8 / 1.4 |
| Years with the river ≥ 1 m up at least once | 1 in 10 | 1 in 2 | 1 in 7 | 1 in 2 |
| Soil under a quarter full, days a year | 0 | 13 | 0 | 12 |
| A weir's wear a year, × a year of normal flow ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] factors) | 1.25 | 1.96 | 1.24 | 2.14 |
| Ice over 5 cm / over 15 cm on still water, days a year | 0.3 / 0 | (weather clock) | 0.6 / 0 | (weather clock) |

- **The beck at w2** (no reach above it) is the flashiest:
  - spates 1.2 and floods 0.55 a year on one clock; 1.35 and 0.75 on two;
  - weir wear ×1.9 and ×2.9.
- **Attenuation:** peaks flatten down the chain. Highest flow / median under two clocks:
  - Saltwell 18.7;
  - Millham 14.5, 35 km below.
- **The cold era** changes little:
  - ice over 5 cm on 0.7 to 2 days a year; over 15 cm on at most 0.1 days a year, at w1 only;
  - snow lying on 0.6 to 1.9 days a year.

## 3. Findings

**1. The generator makes no floodplains (a fault in 37.2's own code, landgen).**
- The valley cut (`physical.py`, `incision_m` 5 × √(flow / river_km2), up to 40 m) lowers each river cell and lowers its eight
  neighbours by 0.4 of that. The result is a V-notch one cell (150 m) wide: a large river lies about 14 to 24 m below the land
  beside it, with no flat floor.
- Beside rivers of class 2 and above:
  - the median height above the river is 19 m on the river world, 16 m on the lake and runs worlds;
  - 0.3 to 3% of riverside cells lie within 2 m of the river.
- At Millham, the Brook Meadow and the Carr (a fen) sit 23 m above the river, and the village's land 23 to 33 m.
- So floods by height never reach a parcel: the highest stage in any run is 3.1 m.
- The rest of the design rests on floodplains too: the "river floodplain" terrain, silt, wet meadows, the mill leat, fords. All of
  it is mostly missing from generated land.
- **The fix:** a valley floor whose width grows with the river:
  - a few cells for a beck;
  - 0.5 to 1 km for a medium river;
  - 1 to 2 km for a large one.
  The floor sits 0.5 to 3 m above the river, rising gently away from it, with the valley sides beyond.
- The fix remakes every generated world, including brief 5's, which 37.4 is building on. Its timing is a question for Zach ([[Q-52 Environment systems|Q-52]]).

**2. The year's length decides what the fast stocks can do.**
- **On one clock:**
  - the soil never dries and summer brings no low water;
  - a village sees a spate every three or four years and almost never a flood;
  - the river passes a metre above normal in one year in ten.
  - Daily weather is real, but an 8-day summer cannot draw down a soil or an aquifer. The seasonal loops (summer drought, winter
    recharge, a wet winter's floods) simply do not happen.
- **On two clocks:**
  - the river has a year: about 12 days of low or dry water;
  - a spate most years, a flood every three or four years;
  - the river a metre up in half of years.
  - These match the frequencies asked for in [[Q-52 Environment systems|Q-52]] #6 at a lowland village. The beck floods more often.
- The two-clock soil is too dry: under a quarter full on 12 to 13 of 32 days. The evaporation-reduction curve needs calibrating.
- **Recommendation:** two clocks.
  - The slow and seasonal stocks (soil water, groundwater and wells, snowpack, the slow layer) move at about 365 ÷ year days per
    engine day.
  - The weather's own events (a storm's rain, a cold snap, wind) stay one day.
  - This is 38.64 §6.7's question made concrete; it is Zach's to decide.

**3. Ice belongs to the weather clock, and in these worlds it hardly comes.**
- The season's mean temperature never goes below 0 °C here (winter mean about 2.7 °C), so ice comes only from cold snaps.
- The engine's snaps are short (at most 3 to 8 days below 0 °C mean) and mild (the coldest day −4 to −5 °C).
- Still water skins over on about 1 day a year. Walkable ice (10 to 15 cm) essentially never forms, even in the cold era, which
  shifts the year by only about 1 °C.
- That is right for lowland southern England. But brief 5's frozen waterways and fishing through ice need a colder base climate
  (the generator's temperature: upland or northern worlds), not the cold era.

**4. The clearing loop is real but weak at this scale.**
- Clearing the woods above Saltwell (19% of 5 reaches) raises Millham's highest flow by 3 to 5% and its spate days by 5 to 10%.
- If the same land were 80% wooded, clearing it would raise the highest flow by about 17 to 22% and the spate days by 20 to 50%,
  with fewer low-water days.
- That matches the evidence that a forest's effect fades as the catchment grows. "Clearing upstream floods us" is a loop for a
  beck and its own village, not for a large river 35 km down. It is not a leverage chokepoint to build a world around.

**5. A weir's wear depends on the clock.**
- On one clock a year's wear is about 1.25 × a year of normal flow; on two clocks about 2 (a beck about 3). Floods dominate:
  at ×15, 1.4 flood days cost as much as 21 normal days.
- [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]'s upkeep, a quarter to a third of the build cost a year, was set against normal flow. Under two clocks, a weir on a beck
  would cost about three times that. 37.4 will want this number when calibrating the weir.

**6. Spreading along `down` works as designed.** Water from upstream arrives a day or two later, and peaks flatten as they go.
- No averaging between neighbours was needed: each reach's flow is its own runoff plus what arrives from above.

## 4. What it leaves out

- Lakes and meres are not stores: the lake world was not run.
- One bank height everywhere, and a generic stage curve.
- No channel capacity or overbank storage.
- Weather by node: a wild area takes its node's weather.
- Soil depth is 1 m everywhere, since areas carry none.
- The trench (finding 1) means the parcel-flooding columns are empty. Read the table's "river stands above" rows against a
  floodplain's heights instead: a meadow 1 m up, a field 2 to 3 m up.

