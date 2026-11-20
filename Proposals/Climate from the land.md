---
id: docs/cybertron2/proposals/climate_from_land.md
kind: proposal
updated: "2026-11-17"
---
# Climate from the land

*proposal · accepted in principle: D2-220 (16 Nov); the design in discussion (Q-56). · `docs/cybertron2/proposals/climate_from_land.md`*

> each place's weather works around its climate as the generated land holds it (temperature, rain a year, the sea, the prevailing wind)


**Status:** accepted in principle: [[D2-220 The weather takes each place's climate from the generated land|D2-220]] (16 Nov). The design below is in discussion (OPEN [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]).

**Owner:** 37.2 (the environment, [[D2-75 The environment spec area moves to 37.2|D2-75]]). The engine's `climate.py` is 37.4's to build; the generator's half is 37.2's.

## Summary

A place's weather is drawn from its climate, and its climate comes from its land. The climate has two levels.

- **The region's climate** is the weather machinery's own parameters, one set per world: the seasons' temperatures, how often each
  weather type comes and how long it holds, how much each type rains, how often storms come and from where, the base wind. Today
  these are the fixed CLIMATE constants (lowland England). They should come from the world's land: its temperature, its wetness,
  its prevailing wind and how near the sea is. The eras act on this level, as now.
- **The place's response** to each type: how much warmer or colder it runs, and how much of a westerly's rain it gets (a windward
  fell more, the lee less), how far its nights drop on a clear night (a frost hollow inland more, the coast less), how windy and
  foggy it is. These come from the place's own land (its height, its rain a year, the sea's distance, its exposure).

Which types come how often is regional: within one world (about 50 km) every village has the same westerly day. What differs
between villages is what that westerly does to each. Across worlds the type mix differs: a dry world has more settled days, not only
less rain on its wet ones.

The generator's fields set both levels, and the long-run statistics at each place must come out as the land says (its rain a
year, its mean temperature). The machinery that draws the day (types that hold, local fields alike between near places, storms)
does not change.

## The proposal

### What to build now (the smallest change that removes the contradictions)

1. **The generator writes the inputs** (37.2, about half a day). Per node, beside `rain_mm` and `elevation`: `temp_c` (its cells'
   mean), `sea_km`, `exposure` (its parcels' mean). Per world, in `generated`: the world's `temperature_c`, `rain_mm` and `wind`.
   Physical facts only; the engine derives the parameters, so a hand-made world can give the same fields.
2. **A climate profile, derived at build** (37.4, about one to two builder days). One function computes, from those fields:
   - *the region's parameters:* the seasons' temperatures centred on the world's `temperature_c`; the type weights tilted by the
     world's wetness (a dry world towards settled and easterly, a wet one towards westerly and cyclonic), with the rain amount
     scaled so the world's mean year meets its `rain_mm`; the storms' heading from the `wind`;
   - *each node's response:* its temperature offset (`temp_c` against the world's, which holds height and the north to south
     gradient); its rain factor (`rain_mm` against the world's), applied mostly to the onshore wet types, so the windward fells wet
     and the lee dries; its seasonal swing and night drop narrowed near the sea (about 0.75 and 0.6 at the shore, full by 20 and
     10 km); its wind by height, the sea and exposure; sea fog near the coast in spring and summer.
   It is computed once from fixed land and kept in the same cache as the weather. It is not state, and it adds no schema change.
   The scheduler reads these parameters where it now reads the global constants and the height terms. Without the fields
   (hand-made worlds), it falls back to today's lapse and height rules exactly, so old worlds replay the same.
3. **One check as a test:** 02zzo's script on generated worlds. It requires:
   - each node's rain a year within ±15% of its `rain_mm`, and its mean temperature within 0.5 °C of `temp_c`;
   - the coast with fewer winter frosts than inland at the same height;
   - the dry world with fewer wet days and more settled days than the wet one.

This removes the glaring faults: dry, cold and wet worlds now differ; the fells are wet and the lee dry; the coast is mild and
windy. Every reader of the weather follows without change, because `env(place, day)` ([[D4-111 Every weather query names its place|D4-111]]) is unchanged.

### What it leaves for later, and where each slots in

- **Weather per area or per cell** ([[Q-50 One grid or several|Q-50]]): the profile is a function of a place's land fields, so it applies unchanged to any
  group of cells once the grid is chosen.
- **Microclimate per parcel:** frost hollows, aspect, shelter by woods. A parcel-level response term, read by the night and the
  crops; the same shape as the node's response.
- **A coupled climate** ([[Q-48 The engine as feature packages|Q-48]] (7)): clearing, snow lying and soil moisture feeding back on the local weather. The profile
  recomputed at the year's turn from the slow layer. That turns the weather layer from driven to coupled, which is a decision of
  its own. Built now, the weather stays driven: every arm meets the same weather.
- **New regional regimes** (continental, maritime, upland, northern; lake effects; the sea's lag): more regional parameters, or
  type tables per regime, chosen from the world's settings.

### How it fits the feature packages ([[Q-48 The engine as feature packages|Q-48]])

The profile is the climate half of the `weather` package's data: one pure function from a space's land fields to the scheduler's
parameters. It adds no state, no new verbs and no new place kind, and keeps the query (`env`). It is written as its own function
with its inputs listed, so the package cut can move it whole, and nothing the migration does would need undoing.

## Why

Zach (16 Nov): "weather should DEFINITELY NOT be independent from the generator". The generator already decides each place's
climate, and the land's other fields follow from it: wetness, moors above the tree line, rain-shadow sand country. When the
engine's weather ignores it, the land and the weather contradict each other. A moor gets lowland weather. A dry world floods as
often as a wet one. A coastal village frosts as hard as an inland one.

## Alternatives considered

- **A world-level climate block set by hand** (overriding CLIMATE `temp`, `rain_mm`): possible today. But one value for the whole
  world loses the rain shadow and the coast, and repeats by hand what the generator already knows.
- **The engine reading the cells directly** ([[D2-208 The world keeps the land it runs on|D2-208]]'s engine half): finer, but the weather is drawn per node. A node's climate is
  the right grain until the weather is drawn per area.
- **Keeping height only:** right for temperature, wrong for rain, sea and a world's own warmth (02zzo §1).

## Open questions

1. The design as above ([[Q-56 How the weather should follow each place's climate from the generated…|Q-56]] (1)): two levels, the region's parameters and the place's response, both from the land; built as
   one derived profile now, the deep system later?
2. The constants: the type tilt by wetness, the onshore share of the rain factor, the sea's reach and shrink factors, the wind
   factors (calibrate, with 02zzo's check).

## Affects

- `cybertron2/landgen/write.py`: node `temp_c`, `sea_km`, `exposure`; the world's `temperature_c`, `rain_mm`, `wind` in `generated`.
- `cybertron2/engine/climate.py` and CLIMATE in `engine/data.py`.
- Every reader of the weather (crops, woods, decay, the night, signs, the ecology, the water on two clocks) follows without change.

## History

- 17 Nov 2026: revised after Zach: "surely the weather depends on the climate of a place? So like climate takes the land
  parameters as input to tune like the metaparameters for what weather is most common, alongside the macro eras". Now two levels:
  the region's parameters (the type mix, the seasons, the rain, the storms; eras act here) and each place's response to each type,
  both from the land; the smallest build (a derived profile) set apart from what waits, and fitted to the feature packages ([[Q-48 The engine as feature packages|Q-48]]).
- 16 Nov 2026: written by 37.2 after 02zzo's test across conditions, and Zach's statement ([[D2-220 The weather takes each place's climate from the generated land|D2-220]]).

## Sources

docs/review/37_growth/02zzo_weather_conditions.md and .py; 02zzl §1 (the unread fields); proposals/weather_scheduler.md ([[D4-109 The weather scheduler|D4-109]]
to [[D4-111 Every weather query names its place|D4-111]]); landgen/physical.py `climate()`; temperate_landscapes.md.
