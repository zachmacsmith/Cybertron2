# The declared process model

How the engine states what its economy is: stocks and how they come back, what acts give, what people need, clocks, and packs
that a world switches on. The engine's nights and acts and any analysis (the carrying capacity model, D4-102) call the same
declarations. Phase 1 of the engine overhaul (D4-103; proposals/process_model.md, engine_overhaul.md).

## Decided

- D4-103: the declared process model, built in phases; phase 1 changes no behaviour of any existing world.
- D4-104: the names renewal and packs; a stock's own record may name its renewal rule and its response to density.
- D4-103, phase 2: calibration and labour (below). Behaviour changes; the engine before it is commit 92cfdbf. All values calibrate.

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

## Calibration and labour (phase 2, D4-103)

- **The woods' clock.** forests.seed converts the woods' yearly rates by the world's year.
- **Sowing windows** (CROPS `sow_seasons`): grain in spring, legumes in spring and summer, rye in autumn; a sowing out of its window is
  refused. The agents' rules list the windows and growing days.
- **Pulses below cereals:** a crop's `yield` factor multiplies what a sowing gives (legumes 0.6).
- **Processing makes no food:** grain and rye 0.85 boiled, beans 0.8, meal and flour 0.95, bread 1.0 (raw as before).
- **Labour** (engine/labour.py; PHYSICS `labour`; each at 0, `wear` false, is the engine before phase 2, and then nothing is written):
  - **Work costs food:** `work_food` (0.04) a unit worked, a unit pushed on counting `over_food` (2) units, a night on guard
    `guard_food` (0.3). It adds to the night's need and to the least one must eat not to go hungry.
  - **Pushing on:** a reply's `overwork` (0 to `over_units`, 2) lets the plan run that many units past the day's; each leaves
    `fatigue` (1) unit off the next day. The fallback never pushes on.
  - **The walk:** each parcel on the day's route past the first `free_steps` (2) costs `step` (0.25) of a unit, carried until it
    makes a whole unit, which comes off the next day.
  - **Skill fades:** a craft unpractised for `fade_after` (8) days loses `fade_rate` (1%) a night of its skill above its floor.
- **Fittings wear** (engine/wear.py; FITTINGS `wear`): millstones after 600 grain ground, an oven after 10 firings, a water wheel's
  leat after a quarter year; a worn fitting works at half (an act there takes and gives half) until its mending craft (dress
  millstones, reline oven with 2 stone, clear the leat; all basic) sets it right.
- **The fallback's limit** (D4-97) is unchanged.
- **The capacity model** counts work's food at the work its allocation gives, and finds the people supported by a scan, as fed is
  not monotone in the people (a small people's work all goes to one seasonal flow).

## Checks

- Phase 2: bot runs recorded after its first four changes with the labour table at zero replay with identical state after the
  rest (9 worlds; three differ only in the prompt's list of crafts, which names the three mending crafts).
- Every refactor step of phase 1 replays the overhaul's baseline exactly:
  - 8 bot runs recorded at the starting commit;
  - the 4 runs made on the engine of 7 Nov;
  - the replay reports of the 56 older journaled runs, unchanged.
- tests/test_cybertron2_capacity.py: fishing appears in the capacity model with no capacity code of its own; a stock's own renewal
  rule and response are followed by the night, the act and the capacity model.

## Open

- Delayed processes in one generic form (crops' timing is data and their hazards engine functions, but eel traps need the general
  form).
- The heat need as a pure function beside food.

*Current as of 8 Nov 2026 (D4-103 phase 2, D4-104).*
