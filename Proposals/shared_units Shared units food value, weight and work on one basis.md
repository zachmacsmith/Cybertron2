---
id: docs/cybertron2/proposals/shared_units.md
kind: proposal
state: discussion (19 Nov 2026). An analysis is asked of 37.2. Nothing has been changed
updated: "2026-11-19"
tags: [proposal, closed]
---
# Shared units: food value, weight and work on one basis

- **state**: discussion (19 Nov 2026). An analysis is asked of 37.2. Nothing has been changed
- **summary**: The engine's food values and yields were set one decision at a time, for balance. There is no common physical basis behind them. Zach (19 Nov): "I do think setting up shared units / rules for deciding is a good idea." The proposal is: - fix the units: a unit of a good is about 1 kg; one food is one 

## Text
# Shared units: food value, weight and work on one basis

**Status:** discussion (19 Nov 2026). An analysis is asked of 37.2. Nothing has been changed.

**Owner:** 37.4 (drafted). The analysis and the calibration are for 37.2, as the economy's owner and the owner of the calibration worlds ([[D2-228 Calibrate across a distribution of worlds|D2-228]]). The data tables are engine data (`engine/data.py` ITEMS, `wild/kinds.py` goods), so the change itself is 37.4's.

**Touches:** every food value and yield; the labour rule (work's food cost); the processing ladder ([[D2-60 The food ladder|D2-60]], [[D4-107 Processing keeps its food gain, for now|D4-107]]); spoilage rates; the capacity model; every world's food budget.

## Summary

The engine's food values and yields were set one decision at a time, for balance. There is no common physical basis behind them. Zach (19 Nov): "I do think setting up shared units / rules for deciding is a good idea." The proposal is:
- fix the units: a unit of a good is about 1 kg; one food is one adult's need for a day; one unit of work is a fixed share of a working day;
- derive food values from energy density, animal yields from real weights, and work's returns from historical return rates;
- keep the deliberate design choices, such as the milling ladder, as stated factors on top of these;
- re-check every world's food budget against the result.

## What prompted it (the runs world, 17 to 19 Nov)

- **The weir's case.** At Lowstrand, the best place on the river, a wattle weir would take about 5 food a run night (24 food over five run nights). At Middleham and Highpool it would take 1 to 2. Spending its 24 units fishing by hand gives about 12. So the weir pays only at Lowstrand, and the runs look poor everywhere. (Analysis in the session, from the run's own pulses: `runs/water_runs_models_r1`, days 6 to 10.)
- **The cause is the eel's value.** An eel is 0.2 food. Its value was chosen so that a full trap (3 food) would hold about 15 eels (brief 5 §3b, [[D2-216 Eels and salmon are fish|D2-216]]), not from what an eel weighs. A real silver eel is 0.5 to 1.5 kg and fatty: half a day's to a day and a half's food. A salmon is 2 food here against 3 to 5 real.

## The values now, and their implied bases

**Food a unit** (`engine/data.py` ITEMS; base ration 1.0 food a night):

| Group | Goods (food a unit) |
|---|---|
| Kept goods | dried and smoked meat 3.0; cheese 2.5; smoked and dried fish 2.0 |
| Wild | hazel nuts 1.6; roots and berries 0.8; greens 0.6; acorns 0.1 |
| Meat and fish | meat 1.5 (0.8 raw); fish 1.0 (0.6 raw) |
| Grain and bread | bread 1.3; meal and flour 1.0; grain 0.7 ([[D2-60 The food ladder|D2-60]], kept in [[D4-107 Processing keeps its food gain, for now|D4-107]]); beans 0.6 |
| Other | eggs 0.6; milk 0.5 |

**Animals' goods** (`wild/kinds.py`), taking 1 unit as about 1 kg:

| Animal | Engine | Real meat | Engine as a share of real |
|---|---|---|---|
| Cow | 40 meat | 150 to 250 kg | about 1/4 |
| Red deer | 20 meat | 50 to 60 kg | about 1/2 |
| Boar | 15 meat | 30 to 50 kg | about 1/2 |
| Roe deer | 4.5 meat | 10 to 15 kg | about 1/2 |
| Hare | 0.7 meat | 1.5 to 2 kg | about 1/2 |
| Salmon | 2 fish | 3 to 5 kg | about 1/2 |
| Eel | 0.2 fish | 0.5 to 1.5 kg | about 1/5 |
| Wildfowl | 0.3 meat | 1 to 1.5 kg | about 1/3 |

Most animals give about half their real meat; the eel and the cow are the outliers.

**Plant foods are off in both directions.** Taking about 2,000 kcal as a food:

| Good | Energy density | The rule gives | Now |
|---|---|---|---|
| Grain | about 3,300 kcal/kg | 1.6 | 0.7 |
| Beans | about 3,300 kcal/kg | 1.6 | 0.6 |
| Hazel nuts | about 6,000 kcal/kg | 3 | 1.6 |
| Greens | about 250 kcal/kg | 0.12 | 0.6 |
| Berries | about 500 kcal/kg | 0.25 | 0.8 |
| Milk | about 650 kcal/kg | 0.3 | 0.5 |

These energy densities are approximate, from memory, and are to be checked against a source table.

## The proposal: seven rules

1. **Units.**
   - 1 unit of a good is about 1 kg (each good already weighs 1 a unit).
   - 1 food is one adult's need for a day, about 2,000 kcal (fix the number); hard work adds through the labour rule.
   - 1 unit of work is a fixed share of a working day: about 1.5 hours if a summer day of 7 units is 10 to 12 hours. Fix it.
2. **Food value = kcal per kg ÷ kcal per food × the edible share,** by good, from a cited table of energy densities.
3. **Animals:** meat = live weight × the dressing share × the edible share, by kind, from cited weights. Each yield follows from the weight rather than being set alone.
4. **Work's returns = a return rate (kg or kcal an hour) × hours a unit,** by method, from cited historical and ethnographic sources. Sources to look at:
   - foraging return rates by resource (large and small game, seeds, nuts, roots, fish), as in Kelly, *The Lifeways of Hunter-Gatherers*;
   - medieval grain yields, seed ratios and work per acre;
   - fishing returns by method.

   The engine's multipliers (skill, tool, the stock's fullness, luck) stay as they are, so the ladder of methods comes from the rates.
5. **Processing conserves mass and energy.**
   - Drying and smoking remove water: the food a unit rises, but the total food can only fall, by losses.
   - Cooking and milling may raise the share that can be used, as a stated availability factor. That is the principled place for keeping the mill's food gain ([[D4-107 Processing keeps its food gain, for now|D4-107]]).
   - The work of processing is counted in units, so a mill pays through work saved.
6. **Spoilage from real shelf life,** by good and storage. The structure exists; only the rates need setting.
7. **The compressed year.** Keep returns an hour and the daily need real. Scale only growth, breeding and the runs' size to the 32-day year, as flows already are ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]] clocks). Food a day of work then stays honest.

## The analysis asked of 37.2

1. **The table.** Energy density and edible share for every food good; weight, dressing and edible share for every animal kind; return rates for every gathering, hunting, fishing and farming method. Each with a source, and a range where sources differ.
2. **Before and after.** Food a unit and food a unit of work for each good and method, now and under the rules. Mark where the order changes: for example greens against grain, eels against hand-fishing, the weir against traps.
3. **Design choices kept.** Name each place where the game deliberately departs from the physical basis, why, and as what factor: the mill's gain ([[D4-107 Processing keeps its food gain, for now|D4-107]]), whole grain against bread, anything else.
4. **The check for every world** (the capacity model): for every activity, food produced per unit of work against the food that unit of work costs. Flag activities that are absurdly rich or can never pay. Run it on the calibration worlds ([[D2-228 Calibrate across a distribution of worlds|D2-228]]) and the water worlds.
5. **The worlds re-checked.** The food budget of each world under the new numbers, and what each needs to stay viable: larders, field sizes, run sizes, stocks.
6. **The runs and the weir in particular.**
   - Eel and salmon values and run sizes against a real river.
   - The weir's share and what it holds a night.
   - Whether a weir pays at a middle station and not only at the lowest.

## Alternatives considered

- **Patch the outliers only** (the eel to about 0.6, the salmon to about 4). Quick, and it fixes the weir case. But it leaves greens, berries and grain off by 2 to 5 times, and gives no rule for the next good added.
- **Calibrate to real calories outright, with no design factors.** That is cleaner, but it loses deliberate choices Zach has made ([[D4-107 Processing keeps its food gain, for now|D4-107]]).

## Open questions

1. The kcal of a food (2,000? 2,400?), and whether children's and elders' needs are fractions of it.
2. Hours a unit of work.
3. Whether the edible-share and availability factors are shown to people, for example in a craft's manual.
4. Order and timing against runs in progress. None should change mid-run; the runs world's model run continues on today's values.

## Affects

- engine/data.py (ITEMS food, spoil); wild/kinds.py (goods); the yields and methods tables; the labour rule; the capacity model; every world builder's larders and stocks; the calibration worlds ([[D2-228 Calibrate across a distribution of worlds|D2-228]]).

## History

- **19 Nov 2026:** drafted by 37.4 at Zach's request, after the weir analysis on the runs world showed the eel at a fifth of its real value. Sent to 37.2 for the analysis.

## Sources

- The runs world's model run ([[W-58 The runs world with a model to each household (Zach, 17 Nov; prop|W-58]]), days 6 to 10 (the run pulses by village, the weir's share).
- engine/data.py ITEMS, WATER_WORKS.
- wild/kinds.py goods and RUNS.
- [[D2-41 Meat is a good|D2-41]], [[D2-60 The food ladder|D2-60]], [[D2-216 Eels and salmon are fish|D2-216]], [[D4-107 Processing keeps its food gain, for now|D4-107]].
- proposals/economic_calibration.md.

*Current as of 19 Nov 2026.*

