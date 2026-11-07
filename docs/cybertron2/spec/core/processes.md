# The declared process model

How the engine states what its economy is: stocks and how they come back, what acts give, what people need, clocks, and packs
that a world switches on. The engine's nights and acts and any analysis (the carrying capacity model, D4-102) call the same
declarations. Phase 1 of the engine overhaul (D4-103; proposals/process_model.md, engine_overhaul.md).

## Decided

- D4-103: the declared process model, built in phases; phase 1 changes no behaviour of any existing world.
- D4-104: the names renewal and packs; a stock's own record may name its renewal rule and its response to density.

## Mechanics

- **Renewal** (engine/renewal.py; D4-103, D4-104). How a stock comes back is a registered rule, a function of its record and the
  night (`step(p, key, res, ctx)`).
  - The rules: fast, threshold, periodic, slow, young, dead, finite, endless, accrues.
  - Which rule a stock follows is data at two levels: the resource's row gives the default (`RESOURCES[key]["renewal"]`), and the
    stock's own record may name another (`renewal`), with its own parameters in the same record (D4-104).
  - night._grow regrows the nightly ones; forests.night the woods' (by their fixed rules).
  - **Periodic** (new): a run comes in its seasons (`run_seasons`) toward `run_K` at `run_r` a night, leaves at the same rate, and
    the resident stock regrows as a fast one.
- **Response to density** (engine/renewal.py, yields.py; D4-104). A take from a stock (the stock and chance yield kinds) scales by
  (S/K) ** b. b is the stock record's `response`, else the resource row's, else 1 (proportional); a number or a name: proportional
  1, hyperstable 0.4, hyperdepleted 2 (calibrate).
- **Outcomes** (engine/outcomes.py, yields.py). What an act gives is one distribution: the act draws from it with the day's random
  stream, and an analysis takes its mean.
  - Built for gathering (stock, chance, fixed, pool) and for a sowing's blight.
  - A distribution draws in a fixed order, so it consumes the random stream as the code it replaced.
- **Needs** (engine/needs.py). A person's food a night is one pure function of the night: shelter, cold, warmth, gear, fires, the
  road, the ration's factors, care.
- **Clocks** (engine/clocks.py).
  - Every rate in the data names its clock: day, year, life, or use or event for what counts uses or occasions.
  - The exchange rates are the world's days a year and its lifespan.
  - A test fails on a rate with no clock.
- **Packs** (engine/packs.py; D4-103, D4-104). A data row may carry `"pack": "<name>"`, and a world turns packs on with
  `packs: [...]` (a file's `systems: [...]` is read the same way).
  - Rows of a pack that is off do not exist for that world: no technique, good or stock, nothing listed.
  - Rows with no pack are always on.
  - The water pack (fishing by hand and with a rod, a fishing rod, salt pans, salting fish; fish and salt stocks) is the first.
- **A missing stock is refused for any resource the data names**, and an endless stock is never drawn down.
- **The run's own baseline:** each run stores its day-0 carrying capacity, by its own engine, in its journal (meta `capacity`).

## Checks

- Every refactor step replays the overhaul's baseline exactly:
  - 8 bot runs recorded at the starting commit;
  - the 4 runs made on the engine of 7 Nov;
  - the replay reports of the 56 older journaled runs, unchanged.
- tests/test_cybertron2_capacity.py: fishing appears in the capacity model with no capacity code of its own; a stock's own renewal
  rule and response are followed by the night, the act and the capacity model.

## Open

- Delayed processes in one generic form (crops' timing is data and their hazards engine functions, but eel traps need the general
  form).
- The heat need as a pure function beside food.
- Fittings' wear (phase 2).

*Current as of 7 Nov 2026 (D4-104).*
