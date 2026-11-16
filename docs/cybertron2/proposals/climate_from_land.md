# Climate from the land

**Status:** accepted in principle: D2-220 (16 Nov). The design below is in discussion (OPEN Q-56).

**Owner:** 37.2 (the environment, D2-75). The engine's `climate.py` is 37.4's to build; the generator's half is 37.2's.

## Summary

The weather keeps the engine's regional machinery: eras, the year's anomaly, the day's weather type, moving storms, and local
fields that are alike between near places. What changes is that each place's climate, the level that machinery works around,
comes from the generated land:
- its mean temperature;
- its rain a year, with the rain shadow and the wet fells;
- the sea's nearness, for milder winters, fewer frosts, more wind and sea fog;
- the prevailing wind, for where storms come from.

Today the engine reads only a node's height (02zzo §1). A dry world, a cold world and a wet coast all get the same weather.

## The proposal

1. **The generator writes each node's climate.** Next to `rain_mm` (already written) and `elevation`:
   - `temp_c`: the mean of the node's cells' temperature (the world's `temperature_c`, the lapse, the north to south gradient);
   - `sea_km`: the nearest sea from the node's land;
   - the world's `wind` (the prevailing side) at the world's top level.
   Additive: worlds without these fall back as today.
2. **Temperature.** At a node with `temp_c`, a season's mean is the engine's seasonal shape around the node's level:
   `temp_c + (CLIMATE temp[season] − mean of CLIMATE temp)`. The lapse is not applied again, since `temp_c` already holds the
   height. A hand-made world that gives only `elevation` keeps today's lapse.
3. **The sea.**
   - **Seasons:** the swing between summer and winter shrinks near the sea, to about 0.75 of inland at the shore, rising to full
     by about 20 km (calibrate).
   - **Nights:** the gap between day and night shrinks to about 0.6 at the shore, full by about 10 km.
   - So coastal winters are milder and coastal frosts fewer.
   - **Wind** is about 1.25 × within 2 km of the sea.
   - **Fog:** sea fog adds to the chance in spring and summer within 3 km.
4. **Rain.** At a node with `rain_mm`, its real year's rain is about `rain_mm`. The ratio k = `rain_mm` ÷ the engine's own
   sea-level year (about 1,000 mm by 02zzo; measured once and kept as a constant) is split half into how often (wet-day odds ×
   √k, capped) and half into how much (amount × √k), as the year's wetness already is. The height term in the wet-day odds
   (`orographic`) is dropped where `rain_mm` is given, since the generator's sweep already wets the fells and dries the lee.
5. **The wind.** The world's prevailing side sets the storms' heading (CLIMATE `storms.heading`), so storms come from the wet side.
6. **Unchanged:** the regional type of the day, the year's anomaly and eras, the local fields and their correlation by distance,
   and the storms' tracks. Weather stays regional and changes day to day; the climate is the place's own.
7. **The check** (02zzo's script, rerun):
   - each node's engine rain a year within ±15% of its `rain_mm`, and its mean temperature within 0.5 °C of `temp_c`;
   - coastal nodes have fewer winter frost nights than inland nodes at the same height;
   - the dry, lowland and cold worlds differ as their settings say;
   - the two-clock water then differs too: the dry world's rivers spate less, and its soil dries longer.

## Why

Zach (16 Nov): "weather should DEFINITELY NOT be independent from the generator". The generator already decides each place's
climate, and the land's other fields follow from it: wetness, moors above the tree line, rain-shadow sand country. When the
engine's weather ignores it, the land and the weather contradict each other. A moor gets lowland weather. A dry world floods as
often as a wet one. A coastal village frosts as hard as an inland one.

## Alternatives considered

- **A world-level climate block set by hand** (overriding CLIMATE `temp`, `rain_mm`): possible today. But one value for the whole
  world loses the rain shadow and the coast, and repeats by hand what the generator already knows.
- **The engine reading the cells directly** (D2-208's engine half): finer, but the weather is drawn per node. A node's climate is
  the right grain until the weather is drawn per area.
- **Keeping height only:** right for temperature, wrong for rain, sea and a world's own warmth (02zzo §1).

## Open questions

1. The design as above (Q-56 (1))?
2. The constants: the sea's reach, the shrink factors, the wind factor, the reference year's rain (calibrate).

## Affects

- `cybertron2/landgen/write.py`: node `temp_c`, `sea_km`; world `wind`.
- `cybertron2/engine/climate.py` and CLIMATE in `engine/data.py`.
- Every reader of the weather (crops, woods, decay, the night, signs, the ecology, the water on two clocks) follows without change.

## History

- 16 Nov 2026: written by 37.2 after 02zzo's test across conditions, and Zach's statement (D2-220).

## Sources

docs/review/37_growth/02zzo_weather_conditions.md and .py; 02zzl §1 (the unread fields); proposals/weather_scheduler.md (D4-109
to D4-111); landgen/physical.py `climate()`; temperate_landscapes.md.
