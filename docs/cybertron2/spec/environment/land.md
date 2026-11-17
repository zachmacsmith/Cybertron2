# The land and its stocks

## Summary

The land is held in three speeds, on the places that hold them; lateral effects travel only by defined spread functions; floods,
droughts, freezes, erosion and a fire's spread emerge from the stocks. Weather is drawn around each place's own climate from the
land. Calibration is across a distribution of worlds.

## Decided

- D2-221: three speeds. **Fixed** (generations): elevation, exposure, position, slope, soil texture as water held and drainage,
  depth, base fertility, rain factor and normal rain, flow direction, river class, sea distance, height above the river, water
  type, springs, falls, fords. **Slow** (the year clock, stepped at the season's turn): fertility, the wetness offset, vegetation,
  soil depth, channel silt; conditions last. **Fast** (the day clock, one stock and one rule each): soil water, snow, river level,
  fuel dryness, standing water, ice, loose soil, cleanness.
- D2-214: two clocks (calendar.md): fast stocks on the engine day; seasonal stocks at about 365 ÷ the year's days real days a day.
- D2-222: the 150 m cells are the fixed land's source and are not stepped. Parcels and areas (home, ring, wild) hold the slow and
  fast stocks. A river's reaches are its river-bearing areas strung on `down`. Nodes hold the weather and snow.
- D2-223: nothing averages across neighbours. A lateral effect travels only along a named channel, by its own spread function,
  one step a day: down (water, silt, fouling, ice), adjacency (fire, colonisation, pests), links (beasts, disease).
- D2-224: floods, spates, low water and drought, freezes, erosion and a fire's spread are thresholds of the stocks. The scheduler
  draws the weather and the true externals (ignitions, hail, blight, murrain, pestilence), with the stocks as their exposure.
- D2-225: the order: phase 0 (the fixed land read) with brief 5; then water; then cover and fire; then soil and silt. Each behind
  a world setting, with dry runs and a null arm.
- D2-220: the weather at a place works around that place's climate as the land holds it (scheduler.md).
- D2-226: the generator's valleys have floors that widen with the river (a few cells for a beck, about 0.5 to 1 km for a medium
  river, 1 to 2 km for a large one), 0.5 to 3 m above the river, with the valley sides beyond.
- D2-227: frozen waterways and hard winters come from a place's own climate (colder worlds, uplands, the north), not the cold era.
- D2-228: weather, environmental systems and ecosystems are calibrated on a set of core test worlds covering diverse environments
  (mountains, coasts, floodplains, dry and wet, cold and mild, and others). The worlds are expected to differ; a calibration passes
  when it generalises in the expected ways and breaks nothing in the extremes.

## Parameters

Every rate is `calibrate` (docs/review/37_growth/02zzn_environment_prototype.py holds the first values).

## Sources

proposals/environment_systems.md; proposals/climate_from_land.md; docs/review/37_growth/02zzl_environment_gaps.md, 02zzn, 02zzo.

*Current as of 17 Nov 2026: D2-214, D2-220 to D2-228.*
