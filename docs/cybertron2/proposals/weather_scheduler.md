# Proposal: the weather scheduler (eras, years, daily types, weather that varies in space)

**Status:** retrospective, accepted: D4-109, D4-110 (8 Nov; built). **Owner:** 37.4 (the engine). The scheduler's rules are 37.2's decided
design (spec/environment/scheduler.md, D2-69 to D2-79); this builds its weather part, with two changes Zach made in conversation
(daily types in place of drawn spells; weather in space). **Affects:** engine/climate.py (new), environment.py, world.py, night.py,
farm.py, forests.py, signs.py, here.py; data CLIMATE; spec/environment/scheduler.md ("as built" only); spec/core/processes.md.

## Summary

A world with a `climate:` block draws its weather from its seed in four layers:
- **an era:** a regime of the climate over years;
- **the year's anomaly:** of temperature and wetness;
- **the day's weather type:** after Lamb's British types;
- **local fields:** temperature, rain and wind, alike between near villages and carried a while from day to day.

Out come physical values at each node (temperature, the night's low, rain, wind, fog) and, from them, the labels the engine already
knows and whether the night freezes. The night, crops, the woods, decay and the signs read the weather of their own place. A world
without the block keeps the hand-written spells exactly, so older runs replay.

## Why (Zach, 8 Nov)

- "weather can vary regionally, no? How were you considering the weather would relate to space?"
- "How should that actually function on top? Should we have a simulated evolving climate?"
- "And what would the higher level eras look like?"
- "I think diseases and ecology should not be in the same system as weather? anyway, can you build out this base weather
  scheduler?"
- "are we able to change the scale of weather changes to quicker if we want as a parameter?"

## What was built

| Layer | Rule | Data (CLIMATE; first values, calibrate) |
|---|---|---|
| era | a starting condition (D2-73), held through the run unless `moves: true`; then its chain moves at year ends, dwell `years` / `era_pace`; rare shocks (the dark year) with `shocks: true` | steady, warm, cold, wet, dry, stormy: temperature, wetness, year-to-year spread, weights on the weather types, dwell, next |
| year | the year's temperature and wetness anomaly: the era's, plus a draw that carries 0.4 into the next year | `year_sd`, `year_persist` |
| type | settled, westerly, cyclonic, northerly, easterly, storm; a type holds for days (`hold`), else a new one is drawn by base x the era's weight | each type's frequency, hold, temperature shift by season, rain factor, wind factor, clear nights |
| local | at each node: the season's mean, plus the year's and the type's shifts, less a lapse with height, plus fields of temperature, rain, rain amount, wind and fog that are correlated between nodes by distance (exp(-d/100 km); roads' days x 25 km, or the nodes' `xy`) and persistent in time (AR(1)) | seasons' means, wet-day chances, rain amounts, wind, gale, snow line, fog chances, lapse 6.5 °C a km, orographic factor, correlation length, persistence |

- **The labels** are derived from the values: snow, gale, heavy rain, rain, fog, clear. A night freezes when its low is below 0 °C
  (the night falls 6 °C below the day's mean on a clear night, 3 °C under cloud).
- **Pure in the seed:** keyed draws, computed in order from day 0 and cached on the World, not in its state. Arms with one seed meet
  the same weather (D4-4), whatever their people do; a replicate's salt does not touch it. The day's values at every node go into
  the night's record (`weather`): the truth, never shown to agents.
- **Read by place:**
  - `environment.weather(w, day, node)`, `wet`, `snow_lying` and `World.cold(day, node)` take a node;
  - the night reads each house's and each sleeper's own;
  - crops read their field's, woods their parcel's for a gale, decay its container's place;
  - the signs of fields, buildings, people, the sky and things read where they are.

  A caller that names no node reads the reference node: the world's `climate.reference`, else the node with most people.
- **Pace:**
  - `era_pace` sets how fast eras turn over;
  - any CLIMATE value can be overridden per world, e.g. `types: {settled: {hold: 0.85}}` for longer settled spells;
  - the year's length is the world's own (24 to 40 days), so ten years is 240 to 400 days.
- **Disease and ecology are not in it** (Zach): they are separate systems; the era families of D2-76 are now climate only here.

**Measured** (Region C, the reference node, 6 seeds x 10 years each):

| Era | Rain | Temperature | Gales | Frost nights |
|---|---|---|---|---|
| steady | — | 9.3 °C | 6.8 | 65 |
| dry | −30% | +0.3 °C | ×0.7 | 66 |
| wet | +24% | 0 | ×1.0 | 61 |
| cold | −1% | −0.8 °C | ×0.8 | 77 |
| stormy | +11% | 0 | ×1.9 | 62 |
| warm | −8% | +0.5 °C | ×0.7 | 60 |

- About 45% of days are wet; winter freezes on 40 to 45% of nights, summer on none.
- Weather types hold about 4 days.
- Wet days are correlated about 0.8 between villages 25 km apart, and 0.64 to 0.73 at 50 to 75 km.

## Checks

- tests/test_cybertron2_climate.py:
  - the same seed, the same weather in every arm;
  - the labels are the engine's;
  - off is the old weather;
  - near places share weather more than far ones;
  - the seasons and height shape it;
  - eras move it as their rows say, and hold unless `moves`;
  - the night reads each place's own.
- With the scheduler off, a bot run made just before replays exactly.
- A 20-day bot run of Region C with it on replays exactly.
- 391 tests.

## Not built (next, in phase 3's order)

- **The climate map from the land:** a pass of moist air along the prevailing wind for rain shadows, coasts and the sea's distance.
  For now a node's height (from its parcels, or `elevation`) is the only land term.
- **The land's response as stocks:** soil water, snow, rivers routed down the river parcels, fuel dryness.
- **Crops by the weather** (L-68): crops still grow by the season, only feeling the cold nights, which now differ by place.
- **Turning it on in existing worlds,** and calibrating them under it. No world file has a `climate:` block yet.

## Alternatives considered

- **A simulated atmosphere** (pressure, moisture moving on a grid): emergent but hard to calibrate, hard to control for experiments,
  and coupled to land use in ways that would break paired arms. Rejected for the daily weather; the land's response stays physical.
- **Independent draws per village:** variance without correlation.
- **One regional weather felt by the land** (the design of phase3_variance_and_risk.md §2): no spatial variance, so villages cannot
  insure each other.

## Open questions

1. Turn it on by default for new worlds, and which era for each existing scenario?
2. The correlation length (100 km): the main number for how far villages share bad years.
3. Moving storms and the land's climate map: next, or after the land's response stocks?

## History

- 8 Nov (later): **moving storms built (D4-110).** Zach: "Add moving storms."
  - **What a storm is:** an object with a heading (toward the east, ±0.6 rad), a speed (150 to 400 km a day), a radius (30 to 80
    km) and a wind (8 to 16 m/s at its centre).
  - **Birth:** it is born upwind of the region, on a storm day with chance 0.7, a cyclonic day 0.15, a westerly 0.04; a stormy era
    weights these.
  - **What it does:** each day it moves along its track. Every node within its radius of the day's stretch of track gains wind and
    rain, by nearness.
  - **Where the nodes are:** from the spec's `xy`, else from their road distances (multidimensional scaling).
  - **What it gives:** at real speeds a storm crosses a region of a day's walk between villages within a day or two. At a slow
    setting (40 to 80 km a day) it takes 3 to 12 days, west first. The storm type's own regional wind was lowered (3.6 to 2.0), so
    gales come mostly from the storms themselves.
  - **Signs:** "the sky to windward is black and the wind is rising in gusts: a storm is coming", plain, for those it reaches
    tomorrow. The sky's forecast, visibility and "days since heavy rain" now read the node's own weather.
  - **Measured** (Region C, 10 years): 7 storms in a steady era, 19 in a stormy one; gale days by node 7 to 16 (steady) and 18 to 36
    (stormy), most on the high ground.

- 8 Nov: built at Zach's request after the discussion above (D4-109).

## Sources

spec/environment/scheduler.md (D2-69 to D2-79); proposals/environment.md §3 to §8, phase3_variance_and_risk.md §10; Lamb's British
weather types; Richardson (1981) and Wilks (1998) on stochastic weather generators.
