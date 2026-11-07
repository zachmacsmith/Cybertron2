# Economic calibration: one time scale, and mechanics that make economic sense

**Status:** discussion
**Owner:** 37.4 (engine), with 37.2 (economy)

## Summary

The capacity model (D4-102) and its comparison with real analysis (38.61) exposed mechanics that do not make economic sense. They
would make any measure of agent ability partly a measure of who finds an exploit. The largest is time. The year is compressed to 32
nights for crops and seasons, but regrowth, spoilage and eating stay at nightly rates set for a longer year. The proposal is:
- one time scale, set once;
- calibration to a short list of real stylised facts;
- each world's capacity report written into the run at its start, so measures compare within an engine version.

## The proposal

**A. One time scale.**
- Every rate in the data is declared per year (or per season): regrowth, tree growth, spoilage, breaks, birth intervals.
- The engine converts to a night by the world's year length.
- The compression is then one dial, and changing it leaves all ratios between annual quantities intact.
- Today:
  - wild plants regrow at r = 0.3 a night, so a meadow gives about twice its standing stock each 32-day year;
  - grain spoils 0.5% a night in a house (about 15% a year), while a winter is 8 nights. Storage barely matters (38.60: 39 to 43
    people across all store kinds), though it is central to every real farming economy.

**B. Crops: one main harvest per crop a year, by sowing windows.**
- Grain is sown in spring and rye in autumn. A second, catch crop is allowed only where a season remains, at a lower yield.
- Today a grain crop grows 8 days in a 24-day frost-free year and may be resown at once, and legumes take 5 days:
  - four to five harvests a plot a year;
  - this alone makes "worked" 3 to 4 times "as it stands";
  - it is an artefact of compressed growth with uncompressed resowing.

**C. Legumes not dominant.**
- Today beans grow fastest, take nothing from the soil, restore it, and yield 3 times their seed like grain. The best rotation is
  mostly beans, so grinding grain ends up adding nothing (38.60 §8).
- Real pulses yield about half to two thirds of cereals by weight. Set their ratio lower (calibrate), keep the soil benefit, and the
  rotation becomes a real trade-off.

**D. Processing does not create food.**
- Today 1 grain becomes 1 flour (food 1.0) and then bread (1.3), against boiled grain at 0.7: milling and baking add 86% to the food a
  grain gives.
- Real milling loses mass (extraction 75 to 95%), and bread and porridge give about the same energy a unit of grain.
- Proposed:
  - boiled grain, meal and flour give about the same food a grain;
  - processing pays in work saved a meal, keeping (bread and flour spoil differently), carrying, and eating away from a hearth.
- Cooking against raw stays: raw grain is barely digestible, so 0.2 against 0.7 is defensible.

**E. Work costs food.**
- Today the ration is fixed: a person eats the same idle or at heavy work. So "food a unit of work" is not an energy return, and
  idleness is free.
- Proposed: heavy work raises the night's need. For example, each unit of field, building or carrying work over a base adds a share
  of a meal (calibrate). Hunger and hard work then trade off as they do in life, and a labour-saving mill is worth food, not only
  time.

**F. Fittings wear.**
- Today mills, ovens, granaries and hearths never wear; buildings break and are repaired; tools wear.
- Proposed: a fitting's use wears it toward a repair (TECHNIQUES wear, as tools), so capital has upkeep and can decay if neglected.
  Whether agents maintain what they inherit then becomes testable.

**G. The run writes its own capacity at the start.**
- The journal stores day 0's capacity report (levels, the ladder, buffer, first own harvest) computed by the run's own engine
  version, as the run already records its provenance (run_data_interface.md item 7's idea).
- Comparisons across runs then use each run's own numbers, and a later engine change cannot rewrite a past run's baseline.

## Why

Zach, 7 Nov: "Does it raise any weird questions about how the current mechanics are currently setup, anything that seem to not
economically make sense and so should maybe be changed? ... Would there be ways to make these measures more robust across runs /
specific implementation details you think we should update that would make more sense?"

Review 38.62 sets out the reasoning; 38.60 and 38.61 have the evidence.

## Alternatives considered

- **Leave the mechanics, measure only within the engine.** Valid for relative comparisons, but the measures would then reward finding
  exploits: rapid recropping, all-bean rotations, milling as a food multiplier.
- **Calibrate everything to history.** Too much. Only the stylised facts that decide incentives matter (A to F).

## Open questions

1. The compression factor (32 days a year now) against run lengths and lifespans (96 days): what should a run of 60 days mean?
2. How large a catch crop, and in which seasons?
3. The work-food rate: its size, and whether it applies to all work or heavy work only.
4. Whether to change these before or with the process model (proposals/process_model.md). Proposed: with it, since both rewrite the
   same rules and each needs the replay checks.

## Affects

data.py (CROPS, ITEMS, PHYSICS, TECHNIQUES); farm.py; night.py; spec/economy/production.md, goods.md;
spec/environment/resources.md, calendar.md; the capacity model (no change: it follows the engine).

## History

- 7 Nov: proposed (37.4), from the capacity model's comparison with real analysis.

## Sources

review 38.60, 38.61, 38.62.
