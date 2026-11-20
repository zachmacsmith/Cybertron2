# Calibration worlds: a suite of diverse places to calibrate against

**Status:** accepted in principle: D2-228 (17 Nov). The suite below is in discussion.

**Owner:** 37.2 (the generator, the environment, the ecology).

## Summary

Weather, the environmental systems and the ecosystems are calibrated on a fixed suite of generated worlds that spans the range of
places the generator can make. These are not the worlds of the brief at hand. Each world has written expectations: how it should
differ from the others, and the ranges its numbers should fall in. A calibration passes when every world stays in its own range and
none collapses at an extreme. It never passes by making the worlds alike.

## The proposal

### The suite (twelve worlds; small, no people unless a check needs them)

| # | World | Made from | Stands for | Expected to show |
|---|---|---|---|---|
| 1 | Lowland river country | `plain`, 900 mm, 9 °C | the English midlands | mixed farming land; floodplain meadows; spates about yearly; mild winters, some frost |
| 2 | Dry east | `plain`, 500 mm, 10 °C, east wind | East Anglia, a rain shadow | fewer wet days, more settled; low summer rivers and dry soils; heath on sand; fewer floods |
| 3 | Wet west, maritime | `coast` west, 1,400 mm, 10 °C | Devon, west Wales | many wet days; mild coast, few frosts; windy; flashy rivers; oak woods; saltmarsh |
| 4 | Coast under mountains | `coastal strip under mountains`, west wind | west Scotland's coast, the Lakes' west side | a wet windward strip, very wet fells, a dry lee behind; sea fog |
| 5 | Upland and moor | `upland and moor` | the Pennines | moor above the tree line; snow lying weeks a year on the tops; peat, becks, tarns |
| 6 | High mountains | uplands raised to about 1,200 to 1,500 m | the Highlands, a cold extreme | long snow; ice; little arable; nodes above 500 m; harsh winters (D2-227) |
| 7 | Cold north | `plain`, 6 °C | a northern lowland | short growing season; frozen still water in hard winters; birch and pine; fewer warm-loving kinds |
| 8 | Fen basin | `fen with islands` | the Fens | flat wet peat; wide floods; reeds and carr; fowl and eels; islands as the dry ground |
| 9 | Estuary and saltmarsh | `estuary and fens` | the Severn, the Humber | tidal water, saltmarsh, fowl in winter; a large river's floodplain |
| 10 | Chalk and clay | `scarp and vale` | the downs and their vale | dry downs (sheep, beech), a wet clay vale (oak, cattle); springs at the scarp foot; winterbournes |
| 11 | Sand and heath | `sand country` | the Brecks, the New Forest | poor dry soils; heath and pine; rabbits; little standing water |
| 12 | Lake country | a laid mere or several tarns, `upland and moor` | the Lakes, a mere district | a large lake that freezes last; lake fish and fowl; outflows |

Two seeds of each, so a seed's luck is not read as the world's nature.

### The expectations

Each world gets a short table of expected ranges, written before calibrating and drawn from real places of its kind (named in the
table's sources):
- weather: rain a year, wet days, mean and season temperatures, frost nights, snow lying, wind;
- land: floodplain and terrace shares, wet ground, slopes, the tree line;
- water: spates, floods, low water, ice;
- ecosystems: the covers' and the ecosystems' shares; which kinds are present and absent; rough densities of the kinds we
  calibrate.

Ranges are wide on purpose. They say a place of this kind looks like this, not a number to hit.

### The checks

1. **The suite report** (one script): every world's numbers against its ranges, a row per world and a column per check, out of
   range marked. Run before and after any calibration change; the diff is the review.
2. **The ordering checks:** pairs that must come out in a known order whatever the constants. The dry east is drier than the
   lowland. The wet west's coast frosts less than the cold north. The fells are wetter than the lee. The fen floods more than the
   chalk. The sand holds less water than the clay.
3. **Collapse checks at the extremes:** no kind goes extinct in a world its range includes, no stock runs away, and no system
   refuses or crashes on any world.
4. **No tuning to one world:** a constant changed for one world's sake must not move another world out of its range. If it does,
   the model is missing a mechanism, and that is written down rather than patched.

### How it is used

- **The generator audit** (W-54): generate the suite and read the land checks first. The trench (02zzn) and the unread climate
  (02zzo) were found this way, one world at a time.
- **Weather:** climate from the land (Q-56) is calibrated on rows 1 to 7 and 12.
- **Water:** the two-clock river model (02zzn) and the flow levels (D2-218) on every world with rivers.
- **Ecosystems:** the wild layer's calibration backlog (02zp §16) and the water measure's fish-eaters (W-60) across all twelve.

## Why

Zach (17 Nov): "a distribution of different core test worlds covering a diverse range of potential environments not to remove
diversity but see that our calibrations generalize in relatively expected ways ... I don't want to overfit to the few worlds we set,
if it might completely break things elsewhere in more extremes ... Don't expect them to be the same."

## Alternatives considered

- **The brief's own worlds:** what was done until now. They are made to test a mechanic, not to span the range, and they hid both
  generator faults (02zzn, 02zzo).
- **Random seeds of one configuration:** they vary the luck, not the kind of place.
- **Hand-made worlds:** exact, but they do not test the generator, and the generator is where the faults were.

## Open questions

1. The twelve worlds as listed, or fewer to start (1, 2, 4, 5, 6, 8, 10)?
2. People in the suite: none for weather, land and ecosystems, and a small cast only where a check needs them (the capacity
   checks)?

## Affects

`cybertron2/specs/calibration/` (the suite's maker and its expectations); a suite-report script under `docs/review/37_growth/`;
every calibration of weather, water and the wild layer.

## History

- 20 Nov 2026: accepted in part: D2-252 (The calibration suite measures how the worlds differ, world by world and side by).
- 20 Nov 2026: accepted in part: D2-245 (The calibration suite is all twelve worlds of proposals/calibration_worlds.md (l).
- 17 Nov 2026: written by 37.2 after Zach's statement (D2-228).

## Sources

docs/review/37_growth/02zzn_environment_prototype.md, 02zzo_weather_conditions.md; landgen/vocab.py CONFIGS; 02zp §15 and §16.
