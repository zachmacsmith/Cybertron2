# The declared process model

How the engine states what its economy is: stocks and how they come back, what acts give, what people need, clocks, and packs
that a world switches on. The engine's nights and acts and any analysis (the carrying capacity model, D4-102) call the same
declarations. Phase 1 of the engine overhaul (D4-103; proposals/process_model.md, engine_overhaul.md).

## Decided

- D4-103: the declared process model, built in phases; phase 1 changes no behaviour of any existing world.
- D4-104: the names renewal and packs; a stock's own record may name its renewal rule and its response to density.
- D4-103, phase 2: calibration and labour (below). Behaviour changes; the engine before it is commit 92cfdbf. All values calibrate.
- D4-105: sowing windows are lore, not rules; skill fades slowly and partly; wear in a village's terms.
- D4-106: can apart from works; crops grow by the season; removing a crop; seed on turf; a crop's signs.
- D4-107: processing keeps its food gain (phase 2's D rejected); food values as before phase 2.
- D4-108: work and its hunger are felt.
- D4-109: the weather scheduler.
- D4-110: moving storms.
- D4-111: every weather query names its place; the senses read the day's values.
- D4-112: the land's base fertility scales every soil level.
- D4-113: renewal rules are handed the weather where the stock is.

## Mechanics

- **Renewal** (engine/renewal.py; D4-103, D4-104). How a stock comes back is a registered rule, a function of its record and the
  night (`step(p, key, res, ctx)`).
  - The rules: fast, threshold, periodic, slow, young, dead, finite, endless, accrues.
  - Which rule a stock follows is data at two levels: the resource's row gives the default (`RESOURCES[key]["renewal"]`), and the
    stock's own record may name another (`renewal`), with its own parameters in the same record (D4-104).
  - Each night a rule is handed, besides its own keys, the weather where the stock is (renewal.context, D4-113): the parcel's
    node (`place`), whether the night freezes there (`frost`), snow lying, a wet day, the day's values there (`weather`: temp,
    low, rain, wind, storm) and the year's anomaly (`anomaly`: temp, wet, era), each None without the weather scheduler, and the
    parcel's `land`. The rules as built read none of them.
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
- **Can apart from works** (D4-106): an act is refused only when it cannot be done (no seed, no soil, no room, no beasts, no idea
  how); otherwise it is done, costs its units and works by its conditions.
- **Crops grow by the season** (D4-106; farm.grow_night, one pure night step the engine and the capacity model call; CROPS
  `growth`, `needs_winter`; PHYSICS farming `lie_loss`, `frost_loss`, `vernal`, `green`, `turned_under`, `turf`; all calibrate):
  - a crop grows each night by its rate for the season (barley 1, 1, 0.5, 0 from spring; beans 0.8, 1, 0.4, 0; rye 1, 1, 0.6,
    0.1), ripening when its growth reaches its growing days at full rate; what it gives is scaled by the mean rate it grew at (a
    hardy crop's winter rest not counted);
  - seed lies in ground too cold to sprout, losing `lie_loss` (8%) a night, and comes up when it can;
  - a tender crop loses `frost_loss` (30%) of its stand each winter or cold night, and is killed when under 2% is left;
  - winter grain will not head until it has had `vernal` (3) winter nights; after a whole growing time without them it heads,
    at `needs_winter` (0.4) of a crop;
  - the crop's ripe day is its own projection, renewed each night.
- **Removing a crop** (D4-106): reaping before ripe gives the crop's green good (`green grain`, `green rye`, `green beans`: little
  food, good fodder, quick to spoil; "dry fodder" makes hay of it) at 0.3 + 0.7 x its growth of the ripe weight, and frees the
  ground; a hoe or plough over a standing crop turns it under (the soil gains 0.02 x its growth; the ground is broken). A plot
  holding another crop refuses a sowing, saying how to clear it.
- **Seed on turf** (D4-106): meadow, pasture, heath and scrub take seed at `turf` (0.1) of a field's yield; the ground stays as
  it is. Clearing is what makes a field.
- **By the season, never refused** (D4-106): weeding a clean or ripe crop gains nothing; hay and salt pans give by the season
  (`by_season`).
- **Lore** (engine/lore.py, data LORE; D4-105, D4-106): what families know from long practice, seeded at the start as a line kept
  for good (D4-64) and passed on as kept lines are. The sowing lore goes to the adults of each household (or person) holding a
  field; its text is read from the engine's growth (each crop's best season to sow). A world turns a lore off with
  `lore: {sowing: false}`, or all with `lore: false`. The agents' rules state no sowing times.
- **Pulses below cereals:** a crop's `yield` factor multiplies what a sowing gives (legumes 0.6).
- **Processing keeps its food gain** (D4-107; phase 2's D rejected): grain and rye 0.7 boiled, beans 0.6, meal and flour 1.0, bread
  1.3.
- **Labour** (engine/labour.py; PHYSICS `labour`; each at 0, `wear` false, is the engine before phase 2, and then nothing is written):
  - **Work costs food:** `work_food` (0.04) a unit worked, a unit pushed on counting `over_food` (2) units, a night on guard
    `guard_food` (0.3). It adds to the night's need and to the least one must eat not to go hungry.
  - **Pushing on:** a reply's `overwork` (0 to `over_units`, 2) lets the plan run that many units past the day's; each leaves
    `fatigue` (1) unit off the next day. The fallback never pushes on.
  - **The walk** (D4-105): the day's route (the shortest path joining where one slept, each parcel worked in order, and where one
    sleeps; D4-62) costs `step` (0.1) of a unit for each leg past the first `free_steps` (2), carried until it makes a whole unit,
    which comes off the next day.
  - **Felt** (D4-108): the night lines tell when the day's work made a ration a missed meal, when a hard day (6 units or more)
    or pushing on left one ravenous (what one ate against a lighter day's need), and the morning tells the units yesterday's work
    took from today.
  - **Skill fades** (D4-105): a craft unpractised for `fade_after` (half a year) loses `fade_rate` (half a year) of what can
    still be lost, and never more than 1 - `fade_keep` (40%) of its best gain over the craft's floor. Below one's best, practice
    counts `relearn` (3) times over.
- **Fittings wear** (engine/wear.py; FITTINGS `wear`; values D4-105): millstones after 2000 grain ground (by an ox or a water
  wheel: an act wears its fitting and what that fitting needs), an oven after 10 firings, a water wheel's leat after a year; a worn
  fitting works at half (an act there takes and gives half) until its mending craft (dress
  millstones, reline oven with 2 stone, clear the leat; all basic) sets it right.
- **The fallback's limit** (D4-97) is unchanged.
- **The capacity model** counts work's food at the work its allocation gives, and finds the people supported by a scan, as fed is
  not monotone in the people (a small people's work all goes to one seasonal flow).

## The land's base fertility (D4-112)

- A parcel may carry `land: {base_fertility: b}` (default 1.0; calibrate). Every level a plot's fertility comes back toward (rest,
  grazing, dung, a crop's restoring) and a new clearing's starting fertility are the table's level times b. Dung raises a soil by
  a share of what that ground can be, never past its ceiling: poor ground stays poor relative to rich ground.
- The capacity model's field year starts from b and runs the same rules.
- Base fertility is the soil's nutrients only; the water a soil holds is a separate property.

## Weather (D4-109)

- **A world with `climate:`** draws its weather from its seed (engine/climate.py; data CLIMATE; all values calibrate):
  - an era: climate only (steady, warm, cold, wet, dry, stormy), held through the run unless `moves: true`, at `era_pace`, with
    rare shocks if `shocks: true`;
  - the year's anomaly of temperature and wetness;
  - a daily weather type (settled, westerly, cyclonic, northerly, easterly, storm) that holds for days;
  - at each node: the season's mean plus those shifts, less a lapse with height, plus local fields correlated between nodes by
    distance and persistent in time.
- **Out come** temperature, the night's low, rain, wind and fog at each node. The labels (snow, gale, heavy rain, rain, fog, clear)
  and frost (a low below 0 °C) are derived.
- **Every query names its place** (D4-111): the weather, wet, snow lying, days since heavy rain, the cold, the senses' share
  and the words are read at a node or a road, never by default. One acting reads where they are (Here: their node, or the road
  they are on); the night reads each house's, sleeper's and fire's place; crops, woods and decay read their field's, parcel's and
  container's; signs read the place of what they show. A road reads the mean of its two ends' values. There is no reference node.
  A model over several places at once (the capacity model's stores, fuel and upkeep) weights the places by who lives there. A
  call without a place is an error, with the scheduler on or off.
- **The senses read the values** (D4-111; CLIMATE vis, calibrate): with the scheduler, sight dims with rain by the mm (0.035 a
  mm, at most 0.5), falling snow (x0.5) and fog (x0.3); sound is masked by wind above 4 m/s (0.03 a m/s, at most 0.6) and by
  rain. Without it, by the day's label as before.
- **Moving storms** (D4-110): on stormy days a storm is born upwind and crosses the region on a track (CLIMATE storms: frequency
  by type and era, heading, speed, radius, wind), adding wind and rain to nodes near its track on the day it passes. Nodes are
  placed from the spec's `xy`, else from road distances.
- **The truth:** each night's record holds every node's values.
- **The same in every arm:** a pure function of the seed.
- **Without the block,** the hand-written spells stay (D2-69 as built on 5 Nov).

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

*Current as of 8 Nov 2026 (D4-103 phase 2, D4-104 to D4-113).*
