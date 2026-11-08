# Economic calibration: one time scale, and mechanics that make economic sense

**Status:** accepted in part: D4-103 (A to F built 8 Nov as phase 2 of the engine overhaul; G with phase 1); D4-105 (lore, fading, wear values)
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
- Today the ration is fixed: a person eats the same idle or at heavy work. So work has no food cost, "food a unit of work" is
  not a net return, and there is no break-even below which work does not pay: foraging a picked-over meadow for 0.1 a unit is
  still worth it.
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

## How these fit one redesign of labour (added 7 Nov)

**Labour in the engine today:**
- a time budget: units a day by season, age and hunger (D4-17);
- acts cost units by technique;
- unused units are lost, or filled by the agent's fallback (D4-97);
- skill by practice raises yield (D2-52);
- hunger cuts units and yield.

**Missing:** what work costs in food (E), when work stops paying (overexertion, Q-2, deferred "to revisit with fatigue"), what
distance costs inside a village (L-35), and work by several at once.

**One redesign would hold them together:**

| Part | From | What it does |
|---|---|---|
| A time scale | A above | every rate a year; the year's compression one dial |
| Energy | E above, with Q-2 | a day's work raises the night's need; work past a day's units costs more (×1.5, ×2) and builds fatigue that lowers tomorrow's units; rest restores |
| The worker as input | process model, mechanism 2 | skill, hunger, fatigue and being untaught enter every yield; practice is an effect |
| Distance | L-35, process model mechanism 6 | work on a far parcel costs walking units from where one slept; carrying costs units and food a load |
| Crews and occupancy | process model, mechanisms 1 and 4 | ditching, ploughing and harvest as work by several; a fitting or ground held while used |
| Outcomes as distributions | process model, part 2 | yield, blight and a hunt's luck from one function: the act draws, analysis averages |
| Calibration | B, C, D, F above | harvest windows, pulses, processing, wear |

**D4-97's fallback needs rethinking with energy.** If work costs food, filling every spare unit by default could starve a hungry
household. The fallback should respect a limit the agent sets, or stop when the work's yield is below its food cost.

**Order of work (each stage replay-verified; the stages that change behaviour raise the world schema and mark an engine version for
comparisons):**
1. Invariance checks with the capacity model. No engine change: find which measures move with the compression and the plot size.
2. The time scale (A).
3. Process model parts 3 and 2: regimes, and outcomes as distributions. No change in behaviour.
4. Labour: energy and fatigue (E, Q-2); the worker as input; distance (L-35); crews and occupancy; the fallback.
5. Calibration (B, C, D, F); the worlds re-checked with the capacity model.
6. The needs table: food, heat, shelter, beasts' feed.

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

- 8 Nov (later): **D4-105**, from Zach's reading of phase 2: the sowing windows are not told (a crop sown out of season does not come
  up; farming households start with the windows as kept lore, lore.py); skill fades after half a year, partly (60% of one's best gain
  kept) and comes back three times faster; millstones wear after 2000 grain from either mill (600 was 9 ox-mill acts, about 16
  months of a 12-person village's grain; the water mill grinds 200 an act and in phase 2's build did not wear the stones at all,
  which was wrong, and counted against them would have been 3 acts), the leat in a year. E2 (stopped at day 14) is rerun on these rules.
  The walk: E2's first 14 days lost 83 units to it (about 0.6 of a unit a person a day). I first read this as the route going home
  between jobs and changed the rule to distance from home; that was wrong. The route is the shortest path joining one's jobs in
  order (D4-62), and Wenbridge's parcels meet only at the green, so three jobs beside the green really are six legs. Zach: "They
  should be finding the shortest path that joins them in order." Reverted to the route; what was off was the price: now 0.1 of a
  unit a leg past the first two (about 0.13 a person a day on the same routes), from 0.25 a parcel past two.

- 8 Nov: **phase 2 built** (spec/core/processes.md, "Calibration and labour"; review 38.63 §6). A to F of this proposal, with
  Q-2 (pushing on and fatigue), L-35 (the walk) and wear (G, from phase 1's list). Choices made in building, against the design table
  of 38.63 §3:
  - the food for work also raises the least one must eat not to go hungry (else a famine's workers would work for nothing extra);
  - pushing on is chosen (a reply's "overwork"), not taken from any plan longer than the day, and the fallback never pushes on;
  - the walk is carried as a fraction until it makes a whole unit off a later day (the day's units are whole);
  - millstones wear after 600 grain, not 300 (300 was dressing every one and a half water-mill acts); a worn fitting takes and gives
    half, so no grain is lost to wear; the three mending crafts are basic (a miller dresses his own stones);
  - beans are still sown twice a year (spring and summer, 5 days to ripen in a 32-day year): the windows give grain and rye one
    harvest a year, not beans.
  Verified: bot runs at A to D with the labour table at zero replay with identical state after E to J. Not done: fishing's yields
  (E1a's caution) are unchanged.

- 7 Nov (later): accepted in the engine overhaul's plan (D4-103).

- 7 Nov (later): how the changes fit one redesign of labour, with Q-2, L-35 and D4-97, and the order of work.

- 7 Nov: proposed (37.4), from the capacity model's comparison with real analysis.

## Sources

review 38.60, 38.61, 38.62.
