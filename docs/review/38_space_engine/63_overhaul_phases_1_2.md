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

## 5. E1a: the water system with agents (Ferrybank, 8 people, 14 days, one seed each; about $9.50 in all)

| Arm | Deaths | Missed meals | What they did |
|---|---|---|---|
| water | 0 | 5 (all by day 9) | 95 fishing acts (50 with a rod, 45 by hand), 3 rods made, 10 days at the salt pans, one salting; spoke of the Wen being "crowded" and of resting Black Mere |
| dry | 4 (Joan d8, Ivo d10, Avice and Wat d12) | 37 | foraging, hunting, weeding; the river gave nothing |

**What it shows:**
- The system works with agents: they found the new crafts, made the gear, and managed the commons in talk.
- The capacity model's forecast held. "As it stands", the village fed 0.77 of its people with water and 0.16 without. The water arm
  was short until the salmon run (autumn, day 8) and then fed; the dry arm starved from its poorest household (the Ferrys, 20
  grain) outward.
- **A caution for calibration:** fishing turned a famine into no deaths at all. It is a strong food source at these first values
  (water_and_preservation.md's warning). Phase 2 should look at its yields beside the new grain values.

## 6. Between the phases: names, and each stock its own rule (D4-104)

- **regime → renewal** (engine/renewal.py; RESOURCES `renewal`): "regime" already meant societies, eras and health in this project.
- **systems → packs** (engine/packs.py; a row's `"pack": "water"`, a world's `packs: [water]`; `systems:` still read):
  "system" already meant landgen's landscape systems and the agents' system prompts. The world's own switches (`children.on`,
  `evening`, `tags`, `ages`, `view`) existed before and are a different thing: they turn rules on, packs turn data on.
- **Each stock may carry its own rule.** A parcel's `state.<key>` may name `renewal` (any registered rule) and `response`: the take
  scales by (S/K) ** b (proportional 1, hyperstable 0.4, hyperdepleted 2, or a number). So the generator's ecosystem layer (37.2) can
  give a chalk stream and a fen mere different fish. Night, act and capacity model all read it; a test checks each.
- Checks: 12 strict replays and the 56 fingerprints unchanged, both E1a runs replay exactly, 367 tests.

## 7. Phase 2: built

All ten items of §3 are built (E to I in engine/labour.py and wear.py; their values in PHYSICS `labour` and FITTINGS `wear`). The
engine before phase 2 is commit 92cfdbf. Where building changed the design of §3:

| Item | As built | Why it differs from §3 |
|---|---|---|
| E. Work costs food | as designed, and the work's share also raises the least one must eat not to go hungry | otherwise a starving worker's extra need was forgiven as a "short meal", and work was free again in a famine |
| H. Pushing on | chosen by the reply's `overwork` (0 to 2); the fallback never pushes on | taking it from any plan longer than the day would overwork agents who list too much, by accident |
| I. The walk | a quarter unit a parcel past two, carried until it makes a whole unit off a later day | the day's units are whole numbers |
| G. Wear | millstones 600 grain (not 300); worn = takes and gives half; mending crafts basic (oven: 2 stone) | 300 meant dressing every 1.5 water-mill acts; halving both sides loses no grain |
| B. Windows | grain and rye once a year; beans still twice (spring and summer, 5 days to ripen) | §3's "one main harvest a crop a year" holds for cereals only |

**Checks.**
- **Inert at zero.** 9 bot runs recorded after A to D, with the labour table at zero, replay on E to J with identical state. Three of
  them differ in the prompt only: its "Everyone knows" list names the three mending crafts.
- 373 tests pass (6 new: tests/test_cybertron2_labour.py).
- A milling act through the real engine: 64 flour an act to 600 grain, then 32, and dressing sets it right.
- **Found on the way:** the capacity model assumed that being fed rises and falls once with the people. It does not. A small people
  puts all its work on the flow that gives most a unit (Ferrybank's river, whose catch comes with the run), and goes short out of
  season. The search now scans before refining. Separately: **Wenbridge cannot mill at all.** It has millstones and no oxen.

**Capacity, three engines** (people supported, region; v1 = before phase 2, AD = after A to D, EJ = after E to J):

| World | People | As it stands | Worked | Best | Bare |
|---|---|---|---|---|---|
| Wenbridge | 12 | 4.07 / 4.46 / 4.26 | 25.1 / 16.5 / 15.7 | 44.6 / 27.6 / 26.6 | 1.23 / 1.23 / 0.90 |
| Combe | 3 | 8.42 / 9.32 / 8.96 | 57.3 / 39.6 / 38.4 | 117 / 71.8 / 69.7 | 1.91 / 1.91 / 1.52 |
| Hollins 2 | 20 | 28.3 / 30.1 / 28.5 | 137 / 93.8 / 89.9 | 224 / 149 / 143 | 8.12 / 8.12 / 6.28 |
| Region C | 58 | 28.9 / 31.9 / 30.7 | 217 / 141 / 136 | 454 / 327 / 319 | 5.81 / 5.81 / 4.55 |
| Two valleys | 26 | 14.0 / 15.4 / 14.8 | 119 / 72.6 / 69.5 | 286 / 196 / 192 | 2.22 / 2.22 / 1.75 |
| Frontier camps | 10 | 18.0 / 18.0 / 16.7 | 18.1 / 18.1 / 16.8 | 18.2 / 18.2 / 16.9 | 9.16 / 9.16 / 6.46 |
| Takeover | 12 | 5.48 / 6.19 / 5.94 | 42.3 / 27.2 / 25.9 | 76.3 / 46.7 / 45.0 | 1.23 / 1.23 / 0.90 |
| Ferrybank, water | 8 | 6.14 / 6.37 / 6.13 | 10.4 / 8.55 / 8.20 | 12.8 / 9.97 / 9.60 | 1.53 / 1.53 / 1.39 |
| Ferrybank, dry | 8 | 1.30 / 1.51 / 1.45 | 5.59 / 3.69 / 3.52 | 7.98 / 5.12 / 4.92 | 0.22 / 0.22 / 0.20 |
| Valley s5 | 17 | 16.2 / 16.8 / 16.0 | 45.0 / 24.4 / 23.1 | 57.5 / 28.7 / 27.4 | 7.44 / 7.44 / 6.15 |
| Goal probe | 8 | 2.26 / 2.57 / 2.49 | 16.5 / 11.4 / 11.0 | 22.8 / 16.1 / 15.5 | 0.56 / 0.56 / 0.52 |

**What it shows:**
- **A to D took a third to a half off the upper levels.** The inflation 38.62 found is gone: recropping in short years, beans, and
  processing that made food. "As it stands" rose 5 to 15%, because boiled grain is now 0.85 a unit, not 0.7.
- **E to J took 3 to 5% more off the farming levels.** It took 10 to 30% off "bare": foraging and hunting give little food a unit,
  so the work's own food is a large share of what they give. That is the break-even 38.61 said was missing.
- **The spread is now narrower.** Worked is about 3.7 times "as it stands" in Wenbridge, against 6.2 before. Best is 6.2 times,
  against 11. Below "as it stands", every world but the frontier is still short of its people. That is the scenario's choice, not
  the engine's.

**E2b, the scripted farm under the windows** (30 seeds, two years): the model's worked year is beans in spring, grain, then beans
in summer, 132 a plot-year. The engine gives 148 (sd 26). The gap is the same +12 to 17% from practice skill as in E1b, so the
model still agrees with the engine.

*Current as of 8 Nov 2026 (phase 1 built; E1 done; renames and per-stock rules, D4-104; phase 2 built; E2b done; E2 running).*
