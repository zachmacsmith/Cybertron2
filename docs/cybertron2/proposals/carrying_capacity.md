# Carrying capacity: what a world's land feeds and keeps warm, by level, from the engine's own rules

**Status:** retrospective, accepted: D4-102
**Owner:** 37.4 (37.2 for its use in the economy check and the generator)

## Summary

`cybertron2/capacity/` measures how many people a world's land feeds for good, and keeps warm, at five levels of practice and
technology. It reports a ratio to the people there, by node and for the region. With it come:
- the buffer that stores give, the days to the first own harvest, and the crops the frost takes first;
- a run's horizon (the day food first runs short);
- each level's yearly work and up-front capital;
- figures (bounds, costs, region and node maps, sensitivity, expansion).

It reads the engine's tables and calls the engine's own rule functions, so it changes when the physics does.

## What was built

- **levels.py:** bare, as it stands, worked, best, ceiling, as knobs, each lowered to what the world reaches.
- **food.py:** a good's worth eaten, by a search over the food techniques; spoilage by night.spoil_rate.
- **rotation.py:** a field's best year (crops, rest, rye over the frost) on the engine's soil and yield rules.
- **sources.py:** a registry of food sources (fields, wild plants, game, herds), whose steady takes are found on the engine's own
  regrowth steps.
- **model.py:** the year simulated (spoilage, the lean season, eating order); people supported; the labour share; buffer and first
  harvest; the run's horizon; the ceiling's clearing.
- **fuel.py:** fuel as its own need.
- **graph.py:** every technique as a process; the work each good embodies (relaxation over the graph); capital in work.
- **costs.py:** recurring work, capital, land productivity.
- **space.py:** node reach over roads; expansion outward.
- **figures.py:** SVG and PNG.
- **retro.py:** past runs against their land.
- **Engine refactor (no change to any result):** the night's rules as pure functions both call (regrow, slow_season,
  spoil_rate, eaten_worth, eat_order, crop_base, fail_chance, frost_kills, fallow_gain, manure_gain, trees_step, young_step,
  shed_a_night, dead_step).
- **tests/test_cybertron2_capacity.py:** guards (edible goods, yield kinds, resources) and agreement with the engine run on a real
  world. The wild-take test found the model's first steady stock wrong (the engine takes by day and regrows at night); fixed.

## Why

Zach, 7 Nov, after the takeover runs (38.59) starved on a field the frost took and an economy check that counted it:
- "Is there already a built in engine module that analyses the lands carrying capacity etc.? If not, build this (as an
  abstracted, well modularised system that can improve easily as we grow new systems / mechanics) and run this on the worlds and
  past worlds";
- "different levels of carrying capacity depending on: is the food eaten raw, cooked ..., what percentage spoils ..., and I guess
  if everything is overharvested";
- "it should be about ratio of food generated vs consumed for survival for given population sizes ... starting stores as ... a
  buffer";
- "consider what other necessary needs there are ... fuel";
- "the labour accounting should also be a generic module";
- "The simulator should be cleanly designed so if the underlying physics and environment of the simulation changes, the carrying
  capacity changes to reflect that";
- "over multiple nodes ... with expansion ... travel costs ... up front capital costs ... and also total labour per turn intensity".

engine/capacity.py had fixed numbers (64 grain a plot, 10 wild food a unit of wood); the checker built on them counted the frost-
killed crop and resowing within the run as food (OPEN Q-28).

## Alternatives considered

- **Extend engine/capacity.py's constants.** Quick, but drifts from the engine.
- **Measure with scripted bot runs.** Exact, but slow and policy-bound. Kept as agreement tests.
- **A linear program over land uses.** Cleaner for the ceiling, but needs a solver and a linear model of non-linear rules; the
  greedy turning of parcels is enough for now.

## Open questions

1. **Shelter as a third need** (beds, rooms, fuel for a house's size), and **beasts' needs** (grass, hay) as limits on herds. Not
   built: herds are taken as they are.
2. **Distribution:** capacity is the land's; who holds the food (38.59: the poor died first) needs households as units. A household
   view is the next step.
3. **Labour beyond food and fuel** (building, upkeep, care of children) as fixed shares a head.
4. **The ceiling** ignores grazing lost to clearing and the work of field works (ditching, terracing).
5. **37.2:** whether the economy check (landgen/economy.py) should call this model (Q-28).
6. **Overharvest in a run** (standing stocks drawn down) is in the run horizon only through the stores and standing crops; drawing
   down the wild is not yet a level.

7. **From the comparison with real analysis (review 38.61).**
   - **Must fix before the measures are trusted:** entitlement by household (Sen); capacity in a bad year, not the mean, with wild
     stocks taken below MSY (Halstead and O'Shea; fisheries); a least-drudgery ladder beside the frontier (Chayanov, Boserup).
   - **Would sharpen:** shadow prices by linear programming; capital's payback and the subsistence fund; land-time beside work-time;
     organisational axes beside metabolic ones (Seshat).
   - **Engine choices it exposed, for Zach:** work costs no food; fittings do not wear; births too slow for a population to meet its
     capacity within a run.

## Affects

spec/measurement/capacity.md (new); engine: night.py, farm.py, forests.py (pure functions, no change in behaviour); 37.2: Q-28.

## History

- 7 Nov (later): the ladder of practice; capital kept apart from ongoing work (running, tools worn, houses' upkeep); compared with
  real societal and economic analysis (38.61), and the holes it found added as open question 7.

- 7 Nov: built at Zach's request (retrospective). The engine refactor first (commit 5a85a95), then the package, tests, figures, the
  run over every world and past run (review 38.60).

## Sources

review 38.59, 38.60; proposals/process_model.md (the engine side of the same idea).
