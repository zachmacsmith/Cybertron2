# 38.63: The engine overhaul, phases 1 and 2: what was built, the checks, and the experiments

Session 37.4, 7 Nov 2026. D4-103. The plan: proposals/engine_overhaul.md. Phase 1's rules: spec/core/processes.md.

## 1. Phase 1: the format (built)

| Part | Where | Behaviour |
|---|---|---|
| The regime registry: how each stock comes back, as a registered function; the night and the woods call it; a new **periodic** regime (a run in its seasons) | engine/regimes.py | unchanged |
| Outcomes as distributions: what gathering and a sowing's blight give, one object that the act draws from and an analysis averages | engine/outcomes.py, yields.py | unchanged (a test checks the draws match the old code's) |
| The night's food need as one pure function | engine/needs.py | unchanged |
| Every rate in the data names its clock (day, year, life, use, event) | engine/clocks.py | none (a test) |
| **Systems as switchable data packs:** a row with `"system": "water"` exists only in a world with `systems: [water]` | engine/systems.py | unchanged (added because new rows otherwise changed every prompt) |
| The capacity model's wild source is generic: the engine's regime for the steady take, the act's own distribution for the yield | capacity/sources.py | capacity numbers unchanged |
| A stock missing from a parcel is refused for any resource; an endless stock is never drawn down | knowledge.py, verbs.py | unchanged |
| Each run stores its day-0 capacity in its journal | run.py | adds meta |
| **The water system** (acceptance test): fishing by hand and with a rod, the rod, salt pans, salting fish; fish with a periodic run; salt | data.py (rows) | new, only where switched on |

**Checks.**
- Every step replayed the overhaul's baseline exactly:
  - 8 bot runs recorded at the starting commit, in eight worlds;
  - the 4 runs made on 7 Nov's engine.
  Together, 12 strict replays with 0 mismatches.
- The 56 older journaled runs' replay reports are identical to the baseline. They already diverged from day 0 because of engine changes
  since they ran.
- 366 quick tests pass.
- The acceptance test passes: Ferrybank's capacity, as it stands, is 0.77 of its people with water and 0.16 without, read with no
  capacity code for fish.

## 2. E1: the experiments after phase 1

**E1b, a scripted farm** (free). A bot farmer plays the capacity model's "worked" year for one plot through the real engine: sow,
hoe, weed, reap, resow, with the night's growth, frost and soil. Two years, 30 seeds.

| | Model | Engine (30 seeds) |
|---|---|---|
| Soil fertility at steady state | 0.916 | 0.917 |
| Net yield a plot-year | 262 | 305 (sd 52, from blight) |

- The 17% gap is the farmer's skill by practice: sowing, hoeing and weeding rise to 1.2 to 1.5 in two years (D2-52). "Worked"
  leaves it out; it is "best"'s master farmers in part.
- So the model's composite year agrees with the engine, and practice is worth a rung of its own on the ladder.
- The 38.60 caution ("worked" untested end to end) is answered.

**E1a, the water system with agents** (Ferrybank, 8 people, water against dry, 14 days, one seed): section 5.

## 3. Phase 2: calibration and labour (the design)

Each item is data or a small rule; each is a behaviour change, so phase 2 is version 2 of the engine for comparisons. Values are
first values (calibrate), set against the capacity model and E2.

| Item | Rule | First value | Why |
|---|---|---|---|
| A. The woods' clock | forests.seed converts the woods' yearly rates by the world's year, not a fixed 24 days | the world's year (32) | a hidden year length in one place (clocks.py KNOWN_LATER) |
| B. Sowing windows | a crop is sown only in its seasons (CROPS `sow_seasons`): one main harvest a crop a year | grain: spring; legumes: spring and summer; rye: autumn | resowing at once gave four or five harvests a plot a year (38.62) |
| C. Pulses below cereals | a crop's yield factor (CROPS `yield`) multiplies what a sowing gives | legumes 0.6 | beans dominated every best rotation |
| D. Processing makes no food | boiled grain, meal, flour and bread give about the same food a grain; processing pays in fuel (bread needs no fire), keeping and carrying | grain and rye 0.85 boiled (raw 0.2); meal and flour 0.95; bread 1.0; beans 0.8 | milling and baking added 86% to a grain's food |
| E. Work costs food | each unit worked adds to the night's need; a guard's night costs more | 0.04 a unit (7 units: +0.28); a guard +0.3 | work was free in food, so there was no break-even (38.61 hole 6) |
| F. Skill fades | a craft unpractised for some days loses skill toward its floor | after 8 days, 1% a day | practice raised skill for good (production.md) |
| G. Fittings wear | millstones dressed after so much grain, an oven relined after so many firings, the leat cleared each season, or their output halves until mended | millstones 300 grain; oven 10 firings; water wheel a season | capital had no upkeep (building_risks.md) |
| H. Overexertion and fatigue (Q-2) | up to 2 units past the day's budget, at double the food cost, each leaving fatigue that takes a unit from the next day | 2 units; ×2 food; 1 unit of fatigue each | labour had no cost in time to come |
| I. Distance inside a node (L-35) | the day's route (D4-62) costs walking: each parcel past the first two on the route costs a quarter unit | 0.25 a step | outfields cost nothing more than infields |
| J. The fallback's limit (D4-97) | with work costing 0.04 a unit, a fallback costs at most 0.12 a day; kept as it is, and measured in E2 | none | the risk is small at this rate; E2 will show it |

**E2 (after phase 2):**
- capacity and the invariance checks on every world (free);
- the scripted farm again under the windows (free);
- Wenbridge, 12 people, a full year (32 days), one seed, about $35: does work's food cost change who works, does storage now matter,
  does fatigue appear.

*Current as of 7 Nov 2026 (phase 1 built; phase 2 designed, E1 under way).*
