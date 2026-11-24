# The waters' mechanisms: general, or fitted to the test worlds? (W-108, agent B)

Session 37.2, 24 Nov 2026. Brief: [brief.md](brief.md) §6. An independent read of the code (agent A's sweep was not read). Every claim
cites the code at `file:line` on main at 260593fb; where a constant was tuned to a world, the comment or commit that shows it. One
small check was run (the cue nights a year in Eelmouth's climate, appendix A); everything else is read from the code.

**Grades:** *general* (works from what any generated world holds); *general with fitted constants* (the rule is general, its numbers
were set on one world or by hand and do not follow the world); *fitted* (the behaviour depends on a hand-written maker, a named kind
or a test world's shape); *missing* (not there at all).

## Summary

| Mechanism | Grade | The key evidence |
|---|---|---|
| Water bodies (D2-229) | general, two kinds missing | every lake, reach and small water the generator makes becomes a body (`wild/areas.py:135-181`); no fen body, no sea or estuary body (sea cells are outside the land, `areas.py:30`; a sea parcel types as a "pool", `areas.py:174-177`) |
| Resident fish (the body's `fish`) | **fitted** (generator: **missing**) | the generator writes no fish stock (no `fish` in `landgen/write.py`); K, r and renewal come only from three makers with three different rules (`make_peoples.py:273-293`, `make_water_worlds.py:130-172`, `make_nutrition_runs.py:127-145`); K scales with the water cells a village is given (at most two, `landgen/settle.py:335`), not the water's size; one generic kind |
| The shallows (D2-317) | general with fitted constants | seeded by the engine on every water and fen parcel (`engine/world.py:276`, `wild/water.py:86-102`), K by water type x parcel size (`water.py:21`, est.); size is the cells allotted, not the margin |
| The river network the runs use | general | built from the land summary's `down` for any world (`wild/runs.py:48-147`); but a lake cell is not river (`landgen/physical.py:311`), and the sea and the window's edge are one "out" (`areas.py:121-129`) |
| Run kinds as data | general with fitted constants, vocabulary limited | any kind with a `RUNS` row runs (`runs.py:37-39`); sizes tuned on the test worlds (`wild/kinds.py:878-884`, commit cd4f3912); only two cues, two directions, one source of recruitment per direction |
| Run timing | **fitted** | windows in absolute days of an 8-day season (`kinds.py:886-890`, `runs.py:170-186`); every runs world and Eelmouth runs on set nights (`runs_set_nights`, `make_nutrition_runs.py:67`, `make_water_worlds.py:102`; D2-231) on window days 1 and 4 (`kinds.py:895`, `runs.py:306-313`); the weather cue's thresholds are absolute (`runs.py:33`, `runs.py:195-203`) and in Eelmouth's climate the eel cue holds 0.36 nights a year (appendix A) |
| The river's record (u8 §1) | general | `river.record` iterates the kinds that passed and bands them against the station's own year (`wild/river.py:113-159`, `river.py:31-73`) |
| The flow | general with fitted constants | flow classes from the catchment's rain over a fixed mean, the same bounds for a beck and a big river, held in the weir's wear row (`runs.py:282-289`, `engine/data.py:473`); no level in state (D2-215, L-114) |
| The weir and the gear sharing a run | general with fitted constants | `wild/gear.py` is a rule over pulses and gear by direction; a weir's share ignores the river's size (`gear.py:66-70`, `data.py:461-462`); only on a river parcel (`engine/wild.py:3248`) |
| The dam (a mill) | general with fitted constants | a shut mill stops `stop` of an up-run at its stretch (`wild.py:3178-3186`, `runs.py:428-435`); a weir or a beaver dam never stops one (`wild.py:738-767`) |
| Ice | general with fitted constants | by water type and the night's frost (`water.py:24-25`, `water.py:116-135`); a sea parcel freezes as a pond |
| The run's reach and the pinch | general with fitted constants | by parcel (`water.py:176-206`); a lake parcel meets no run; the ford's pinch reads a field the generator never writes |
| The river's signs (u8) | **fitted** | the rows name eel, salmon and lamprey (`river.py:193-253`, `river.py:416-426`); the eel's window is read by name (`river.py:290-301`); the generic run rows are skipped (`engine/signs.py:2476`), so a new run kind passes unseen |
| The fisher's lore (u9) | **fitted**, partly unreachable | named kinds (`engine/founders.py:273-341`); the salmon and lamprey lines read `river_class` and `world["lampreys"]`, which nothing writes (`founders.py:331-334`) |
| The wild layer's fish against the body's | **missing** link (L-116) | the food web's fish is about 48,500 kg a km2 of water (`kinds.py:104`, `kinds.py:121`, `wild/ecology.py:65`), a body about 780 units a km2 (`make_peoples.py:288`): about 60 times apart, linked one way (`engine/waters.py:79-93`) |

The rules are mostly written as general rules (over `RUNS` rows, water types, the land's `down`), and the code says so
(`runs.py:1-2`). What is fitted is the data the rules read and the worlds that fed them: the resident fish are a maker's hand
stocking, the run timing is a window tuned to an 8-day season with the test worlds on set nights, the sizes were tuned on the runs
and river worlds, and the signs and lore name the three kinds. A generated world with none of the makers' edits has runs and
shallows and no open-water fish at all.

## 1. Water bodies

- **What is general.** `areas.waters` (`wild/areas.py:135-181`) makes a body of each lake (by connected lake cells, `:142-151`), a
  reach of each river-bearing area with a village's home and ring as one (`:152-161`), and a small body of any water parcel on
  neither (`:174-177`: "brook" if it touches a river cell or wet ground below 0.9, else "pool"). `engine/waters.py:24-49` gives each
  body with parcels one shared record. Nothing names a world.
- **Missing: a fen.** A fen is a land cover, never a body (`wild/water.py:62-63`; `areas.py:164` skips non-water parcels), so a fen
  holds shallows (K 7, `water.py:21`) and resident eels (the wild layer's `eel`, `kinds.py:58`, habitat `wet` 0.8) and no open water
  of its own. Its meres are lakes where the fen system allows one (`physical.py:292-297`, `macro.py:238`).
- **Missing: the sea and an estuary.** The wild land is `~L.sea` (`areas.py:30`), so sea cells hold no area and no body. A water
  parcel on sea cells (only a vacant place pinned `on: sea`, `settle.py:395`) falls to `areas.py:174-177`; the sea's wetness is 1
  (`physical.py:332`) and its river class 0, so it becomes a **"pool"** body: shallows K 4 a unit, frozen over after 2 nights of hard
  frost (`water.py:21-25`).
- **A reach is the village's land, not the river's shape.** A reach's resident K is the sum of its parcels' own K (`waters.py:41-44`),
  and a home village takes at most two water cells (`settle.py:328-336`), so a village on a 5 km class-3 reach and one on a short
  medium river hold the same stock if their cells match. The reach's `river_km` and `big_river_km` are recorded (`areas.py:158-161`)
  and read by nothing that sizes a stock.

## 2. Resident fish (open water)

Grade **fitted**; from the generator **missing**.

- **No generated stock.** `landgen/write.py` writes no `fish` (the parcel's land block, `write.py:66-87`, and state, `write.py:108-130`,
  have none); `world.py:131` loads a parcel's stocks from its spec state only. The engine seeds the shallows (`world.py:276`) but not
  fish. Every generated world's fish come from a maker after generation, as their docstrings say ("fish are stocked after
  generation as the peoples worlds do (OPEN L-75)", `make_water_worlds.py:17`; "which the land generator does not yet stock",
  `make_peoples.py:279-280`).
- **Three makers, three rules.**
  - `make_peoples.water_stocks` (`make_peoples.py:278-293`): K 8 x `RESIDENT_FISH` 2.2 x size, 12 x 2.2 if the parcel's terrain text
    holds "sea" or "coast" (`:288`), r 0.3 a night, no `renewal` key (so the resource's default `periodic`, `data.py:259`), and a
    `run_K` of 4 K in autumn on a big river, chosen by `river_class >= 3` or the word "river" in the parcel's text (`:290-291`).
    `RESIDENT_FISH` is "a named lever ... not checked against a real standing biomass" (`make_peoples.py:273-275`; commit cd4f3912,
    W-64).
  - `make_water_worlds.water_stocks` (`make_water_worlds.py:141-172`): the same 17.6 a unit with r 0.3, except a village's largest
    water parcel with 0.5 km2 or more of lake in its home and ring, which holds `LAKE_FISH` 16,500 a km2 x that lake area, renewal
    `threshold`, r on the year clock from `LAKE_TURNOVER` 0.4 (`:130-166`). The constant was set on Meresby: "Zach, 17 Nov: it's a
    pretty big lake" (`:134-135`), commit 4f580ca8 ("19,575 at Meresby").
  - `make_nutrition_runs.water_only` (`make_nutrition_runs.py:134-145`): a quarter of that (`RESIDENT_SHARE` 0.25, `:127`), renewal
    `fast`, on river or brook parcels of the one village; commit bb628e29 (W-98, "the runs world water-only (D2-316)"). Eelmouth's
    reach holds K 8.8 r 0.3 `fast` (`specs/nutrition/eelmouth.yaml:357-361`).
- **Clocks disagree.** The rivers' r 0.3 is a night (`engine/night.py:620-628`; u1 Gaps: "fish regrows at r 0.3 a night on the day
  clock ... against D2-273"); the lake's r is derived from a year's turnover; the shallows are on the year clock (`water.py:22`). The
  best yield r K / 4 of a river parcel is then 1.3 units a night a unit of size, of the lake's mere about 0.001 K a night (r = 1.6 / 365).
- **One kind.** The body holds one `fish` record (`waters.py:21`, `SHARED = ("fish",)`); no kind, no habitat, no temperature or
  productivity term. The renewal context offers the weather and the land (`renewal.py:134-159`), and "the rules that exist read none
  of these" (`renewal.py:143`).
- **The second stock.** The wild layer's own `fish` food (eaten by otters, herons, eels) is `cap` 40,000 x `SCALE` 1.2136 kg a km2 of
  full water cover (`kinds.py:104`, `kinds.py:121`, `ecology.py:65`, `ecology.py:174-175`): about 48,500 kg a km2, against a maker's
  17.6 units a 2.25 ha cell (about 780 a km2). The body sets the wild fish's fullness each night (`waters.py:79-93`) and the food
  web's take is not written back (`waters.py:9-12`; L-116, default taken). Without a body record (every generated world without a
  maker) `to_wild` returns at once (`waters.py:82-83`) and the wild fish run on their own.
- **Paths that need the record:** angling and the bank line (`data.py:717-720`, `draws: fish`), the gill net's and set line's
  open-water draw (`engine/wild.py:1098-1109`), the fish signs (`signs.py:686-692`), the beaver pond's raise (`wild.py:749`), the
  heronry's take (`kinds.py:480`), the river row "few fish of {water}'s own" (`river.py:251-252`). All silent in a generated world.

## 3. The shallows

Grade **general with fitted constants**.

- **General:** every water and fen parcel of a world with the water pack, at making (`world.py:276`, `water.py:86-102`); K a unit of
  size by type (`water.py:21`), the type read from the body and the land (`water.py:57-76`); renewal by season on the year clock,
  none under ice (`water.py:105-112`, `night.py:645-647`). Signs read the parcel's own stock (`signs.py:695-708`).
- **Fitted:** the K table is "est., calibrate" from fishing_ladder's brook anchors; only the brook's is sourced (u1 §2 table: pool,
  fen, river, big river and lake "none sourced"). "A unit of size read as the generator's cell" (`water.py:19-20`): a lake's shallows
  are 2 a cell on the one or two cells a village holds, whatever the lake's shore. The season rates are one table for every water and
  latitude (`water.py:22`); nothing reads warmth, flow or a dry year.

## 4. The runs

### 4.1 The network (general)

`Net` (`runs.py:48-147`) needs only the land summary: stretches by area, `below` from `down`, cycles cut, the catchment's nodes
weighted by river km. Heads and spawning stretches follow `where` and `spawn` (`runs.py:127-144`). Nothing names a river.

Two physical gaps:
- **A lake breaks the river.** Lake cells carry river class 0 (`physical.py:311`: `* ~lake`), so a lake parcel's `land.river` is
  "none" (`write.py:84`) and `_river_parcel` is false for it (`wild.py:3038-3040`). An area wholly lake has `river_km` 0 and is not a
  member (`runs.py:59`), so a stretch draining into it finds no member below and becomes a mouth (`runs.py:72-79`): an up-run for the
  river above enters there, and a down-run reaches "the sea" there. (Most lakes share an 8 km block with river cells, `areas.py:56`,
  so this bites only where a lake fills its area.)
- **The sea and the window's edge are one outlet.** `recv` is -1 at "the sea and the window's edge" (`physical.py:143`), and an area's
  water leaving by either is `down: out` (`areas.py:121-129`). A river leaving the window inland is treated as reaching the sea there;
  the river world's maker says so ("leaves the window to the south (the sea beyond)", `make_water_worlds.py:7`).

### 4.2 A run kind as data (general with fitted constants; vocabulary limited)

`runners` takes every kind with a `RUNS` row (`runs.py:37-39`); `advance` reads only the row (`runs.py:316-437`). The kind needs a
`KINDS` row (as a migrant that arrives as no one, `kinds.py:60-65`), a `TRAITS` row with `mover: run` (`kinds.py:867-869`) and a
`TAKEN` row whose goods give its kg (`kinds.py:657-659`, `wild.py:3127-3132`). The gear meets it by traits (`wild/methods.py:73-90`:
`water`, `swims`, `size`), the gear shares it by direction (`gear.py:20-24`), the weir's hold counts its kg, the bots plan by
`RUNS` (`engine/bots_livelihood.py:327-345`).

**Fitted constants:**
- **Sizes, tuned on the test worlds.** `kinds.py:878-884`: the eel's `year` 0.6 "(was 0.2)", the salmon's `cap_km` 6 "(was 1.5)",
  "measured, the runs world: Highpool 46, Middleham 99, Lowstrand 848 a year ... the river world: Saltwell 124, Millham 387", the
  lamprey "x 3 (cap 9)"; the eel's recruitment `b` 3.0 "(was 1.0) ... at 1.0 that run emptied the stock to a fifth" (`kinds.py:55-58`).
  Commit cd4f3912 (W-64, "runs at a real river's size"). The rule scales with river km and the eel stock, so the sizes travel; the
  levels were chosen where the measurements were.
- **One speed and one thickness for every kind:** `km_a_day` 10 and `dense` 3.0 (`kinds.py:895`), read from `RUN`, not the kind's row
  (`runs.py:363`, `wild.py:3439`). A day is about 11 real days in the 32-day year, so the run moves about 1 km a real day; set so a run
  crosses the 50 km window inside its window.

**The vocabulary is code:**
- **Cues:** `rain_after_dry` and `spate` only (`runs.py:195-203`). **An unknown key is ignored and the run is cued every night**: the
  loop returns False only for the two names it knows, then True. A row with `{"temp": 10}` would run on every night of its window.
- **Directions:** `down` draws its year from a resident stock of the same kind (`runs.py:373-386`: `st["pop"][k]`); `up` returns from
  last year's spawners in this world (Beverton-Holt, `runs.py:407-417`). A run recruited from the sea independently of local spawners
  (elvers and glass eels going up) is neither; a run that is a spawning gathering in place (pike, perch, bream in the spring shallows)
  is not a movement along the river at all.
- **Where:** "river" or "big river" (`runs.py:133`, `:143-144`); no lake, fen or brook-only spawning.

### 4.3 Timing: windows, set nights and a cue that seldom holds (fitted)

- **The window is in absolute days of an 8-day season.** Eel `{2: (0, 7)}`, salmon `{2: (0, 7), 3: (0, 3)}`, lamprey `{0: (0, 7)}`
  (`kinds.py:886-890`), read as season days (`runs.py:170-186`). The engine's default season is 6 days (`engine/world.py:105`), and
  most world files use 10 (109 of the 160 `season_days` settings under `cybertron2/specs/`; 8 in 36, 6 in 11). With 10 the window skips the season's last two
  days; with 6 (or 4, 5) the day `hi` 7 never comes, so `last` never fires: the up-runs' last-day entry never happens (their dues are
  cleared next year, `runs.py:411`) and `ended` never reports a run over (`runs.py:211-213`; the "run is over" sign, `river.py:238`;
  the year's thin or good run, `signs.py:2484-2496`).
- **The test worlds run on set nights.** `runs_set_nights: true` in the runs world, its models arm, the three nutrition arms and all
  four Eelmouth files (`make_water_worlds.py:102`, `make_nutrition_runs.py:67`; `specs/nutrition/eelmouth.yaml:32`). Then
  `_runs_cued` is false (`wild.py:3032-3035`) and a run starts on window days 1 and 4 (`RUN.no_weather`, `kinds.py:895`;
  `_calendar_cue`, `runs.py:306-313`), the up-runs' rest on the last day (`runs.py:421-423`). A world without the climate does the
  same (`wild.py:56-59` gives every day 2.0 mm). So in every world the runs were measured on, **the runs come on fixed dates**:
  D2-231 took this because "the runs on the rain cue ... fires 1 to 3 nights a year in the steady climate" (`docs/cybertron2/DECISIONS.md:375`, D2-231).
- **The weather cue's thresholds are absolute.** `rain_after_dry` wants the catchment's rain at least 1.5 x `RAIN_MEAN` with each of
  the days before under 0.5 x (`runs.py:198`); `spate` at least v x `RAIN_MEAN` (`runs.py:200-202`). `RAIN_MEAN` is a fixed 3.4
  (`runs.py:33`, `ecology.py:27`: "calibrate with the climate, task P0"; the wild audit: "RAIN_MEAN repeats the climate's own mean",
  `docs/review/37_growth/02zq_wild_audit.md:134`). The climate's own mean is about 2.6 a day (Eelmouth 2.61, the lake world 2.71: the
  script in appendix A). In Eelmouth's climate the eel's cue holds on **0.36 nights a year** (none in 25 of 39 years), the salmon's
  2.8 and the lamprey's 2.2 (none in 9 of 39 each).
- **What a year without a cue does.** Eels start only on a cue (`runs.py:388-390`), even on the window's last day; a year with none
  leaves the silver eels in the stock. An up-run's remainder enters on the last day whatever the weather (`runs.py:421`), so a
  dry autumn brings the whole salmon run on one forced night.
- **The cue is read in two places, two ways.** The runs read the catchment's rain (`runs.py:189-203`); the eel-night signs and the
  trap's eel-night multiplier read the village's own rain (`wild.py:1439-1441`, `methods.py:41-42`, `kinds.py:410`), with the same
  thresholds copied and the eel's window copied as `{2: (0, 7)}` three more times.
- **What it does not read.** No water temperature or the season's warmth (the climate has it per node, `climate.py:241-242`), no day
  length, no flow falling after a spate, no moon. The generator's rain for a place (`node["rain_mm"]`, `write.py:362`) is read by
  nothing in the engine; the daily rain comes from the climate's one table (`climate.py:245-252`, `data.py:1006-1007`) and the node's
  height, so a wet and a dry generated climate cue alike.

### 4.4 Ice, dams and the night (general with fitted constants)

- Ice holds a run by direction (eels at any ice, the up-runs when frozen over, `runs.py:335-338`), from the frost and the water type
  (`water.py:116-135`).
- A shut mill holds `stop` 0.5 of an up-run arriving at its stretch (`wild.py:3178-3186`, `data.py:478`, `runs.py:428-435`); the held
  fish go back to the sea the next night (`runs.py:344`), so the spawners above fall year on year through Beverton-Holt. General. Only
  a mill is a dam: a shut weir only takes its share, and a beaver's dam changes stocks' K (`wild.py:738-767`) and never a run. One
  lodge's dam raises the whole reach's fish K x 1.3 (`kinds.py:488`; the record is the body's, `waters.py:52-59`).

## 5. The river's record, the flow, the weir and the gear

- **The record (general).** `river.record` (`river.py:113-159`) writes, for every village on a river, what passed by kind, the band
  against the station's own year (`river.py:31-73`: last year's tally, else this year's so far with what is still to come), the best
  night, the takes, what the weir turned away, the ice, the first and ended runs over every `RUNS` row (`river.py:152`). A new kind
  is recorded with no change.
- **The flow (general with fitted constants).** The catchment's rain today and half of yesterday's over `RAIN_MEAN`, banded by
  `flow_at` (`runs.py:282-289`), which lives in the weir's wear row (`data.py:471-474`) and is read from there by the runs, the record
  and the signs (`wild.py:3309`, `river.py:94`, `wild.py:3486`). A beck and a big river answer the same rain the same way: no flash,
  no lag, no damping by the catchment's size, no level kept (D2-215, L-114). The trap's wreck is by that class (`data.py:476`).
- **The weir (general with fitted constants).** Sections, shares, holds and wear are data (`gear.py`, `data.py:461-478`). The share is
  0.30 for the first section whatever the water (`data.py:461`): a beck and a big river spanned alike; only the cost (`data.py:468`)
  and the wear (`data.py:471`) know the water. "Beck" is a brook parcel at 150 m or more (`wild.py:3122`, `beck_m`, `data.py:471`), a
  fixed height. A weir on a lake parcel takes nothing (`wild.py:3248`).
- **Gear sharing a run (general).** `gear.share_run` orders gear by the parcels' `down` and the run's direction (`gear.py:20-24`,
  `wild.py:3106-3114`); nothing names a kind.
- **Reach and pinch (general with fitted constants).** A trap meets a run on a river parcel in full, in a fen beside one at half
  (`water.py:26`, `:176-184`); the edge's share by type (`water.py:29`, `:191-206`), with lake, pool and fen falling to the river's 0.3
  (`water.py:206`). The ford's pinch reads `land.ford` (`water.py:196`), which the generator never writes (it is a node fact for names,
  `write.py:234-235`).

## 6. The signs and the lore

- **The river's rows name the kinds (fitted).** `day_context` builds fields `eel`, `salmon`, `lamprey`, `eel_n` and the rest
  (`river.py:416-426`); the `DAY` rows are written for them (`river.py:193-219`, `:236-238`); the dawn rows `eel_night_rain` and
  `eel_night_set` fire on eels (`river.py:176-177`, `:348-352`); "the nights drawing in" reads `RUNS["eel"]` (`river.py:290-295`);
  `eel_window` reads the eel by default (`river.py:298-301`). The generic rows that would serve any kind (`RUN_SIGNS` `down` and `up`,
  `kinds.py:903-906`) are skipped: "the run's own rows are u8's" (`signs.py:2476`). **A new run kind is recorded and fished but nobody
  sees it run.** Its "held below the dam" and "thin or good year" rows still work (`signs.py:2479-2496`).
- **Chances tuned to a measured run.** The rows' `own` "were raised to land from the Street (stage 4 report §3)" (`river.py:163-166`;
  commit ada5c3a4, W-100).
- **The resident fish and shallows signs (general).** Read the stock's fullness (`signs.py:686-708`).
- **The fisher's lore (fitted, partly unreachable).** FI1 and FI2 are eel lines (`founders.py:279-290`); FI6 (salmon) needs
  `land.river_class` in ("large", "big") or `land.river == "big river"` (`founders.py:331-332`), FI7 (lamprey) `world["lampreys"]`
  (`founders.py:333-334`). The generator writes `land.river` as "river", "brook" or "none" (`write.py:84`) and no `river_class`, and no
  maker sets `lampreys` (grep finds none). **The salmon and lamprey lines are never given in a generated world.**

## 7. Constants tuned to one world

| Constant | Where | Tuned on | Evidence |
|---|---|---|---|
| Run windows `(0, 7)` | `kinds.py:886-890` | the 8-day season of the water worlds | `runs.py:170-186` reads season days; `make_water_worlds.py:35` `season_days: 8` |
| Set nights 1 and 4 | `kinds.py:895` | the runs world, Eelmouth | D2-231; `make_water_worlds.py:102`, `make_nutrition_runs.py:67` |
| `RAIN_MEAN` 3.4 | `runs.py:33`, `ecology.py:27` | none (the climate's mean is about 2.6) | `02zq_wild_audit.md:134`; appendix A |
| Eel `year` 0.6, eel `b` 3.0 | `kinds.py:886`, `kinds.py:55-58` | Highpool, Saltwell | `kinds.py:878-881`, commit cd4f3912 |
| Salmon `cap_km` 6, lamprey 9 | `kinds.py:887-890` | Highpool, Middleham, Lowstrand, Saltwell, Millham | `kinds.py:881-884`, commit cd4f3912 |
| `km_a_day` 10 | `kinds.py:895` | the 50 km window and the compressed year | `kinds.py:892` ("about a day a 10 km, brief 5 §2.2") |
| `RESIDENT_FISH` 2.2 | `make_peoples.py:273` | the peoples worlds' food | `make_peoples.py:273-275`, commit cd4f3912 |
| `LAKE_FISH`, `LAKE_TURNOVER` | `make_water_worlds.py:131-138` | Meresby | `:134-135`, commit 4f580ca8 |
| `RESIDENT_SHARE` 0.25 | `make_nutrition_runs.py:127` | the runs world, Eelmouth | commit bb628e29 |
| Sign chances `own` | `river.py:173-253` | the Street (stage 4) | `river.py:163-166`, commit ada5c3a4 |
| `SHALLOWS`, `ICE`, `PINCH`, `RUN_REACH` | `water.py:21-29` | estimates from one brook anchor | u1 §2, §4, §5 tables; commit 07eec413 |
| `beck_m` 150 | `data.py:471` | none stated | `wild.py:3122` |
| The fish food's `SCALE` 1.2136 | `kinds.py:121` | the food web's calibration (02zp part two) | `kinds.py:121` |

## 8. Behaviour only a maker supplies, and paths a generated world never reaches

**Only a maker supplies:** every resident fish stock (§2); the big river under a village (`river_sites` pins `at` onto the laid large
river, `make_water_worlds.py:40`, `:431-450`; the seed kept only if the village has big river, weir water and a spring,
`make_nutrition_runs.py:267`); a lake big enough (the calibration world refuses a seed whose mere holds under 1 km2,
`make_calibration_worlds.py:95-99`); the spring and the mill (`make_water_worlds.py:198`); set nights (§4.3); the trap stock and nets
(`make_nutrition_runs.py:146-160`).

**Never reached by a generated world:**
- **A home village on a brook, a shore or the sea.** A home village's water cells are only class 2 or 3 river or lake
  (`settle.py:328`), though it may be sited by a brook, a spring or the sea (`settle.py:74`). Only a vacant place with `fish` takes a
  brook, wet ground or (pinned `on: sea`) sea cells (`settle.py:394-398`). So the brook's shallows K 5 and ice rows, the weir's "beck"
  (cost 0.3, wear 2.0, `data.py:468`, `:471`), the "pool" type, and the sea are reached only by vacant places and hand-made worlds.
  (u1's Gaps assume "the generator's brooks are mostly their own water parcels", which this contradicts for homes.)
- **A run at a lake** (§4.1), the ford's pinch (§5), the salmon and lamprey lore (§6), the old `periodic` parcel run (`renewal.py:47-63`,
  set only by `make_peoples.py:290-291`), every path that needs a resident fish record (§2).

## 9. A new run kind, a new resident kind: what each needs

**A new run along the river (shad, sea trout, smelt, a spring salmon, a bigger lamprey):**
- *Data only:* a `KINDS` row (migrant, `arrive` 0, `kinds.py:62-65`), `TRAITS` (`mover: run`, `swims`, `size`, `kinds.py:867-869`), `TAKEN`
  goods (`kinds.py:657-659`), a `RUNS` row with `dir: up`, `seasons`, `cue` from the two known, `night`, `where`, `spawn`, `return`. The
  gear, the weir, the dam, ice, the record, the bots and the tally take it as it is.
- *Code:* any cue but the two (and today an unknown cue silently means "every night", `runs.py:195-203`); its own speed
  (`runs.py:363`); its sign rows (`river.py` and `signs.py:2476`); its lore (`founders.py`); a window in season shares if the world's
  season is not 8 days.

**Elvers and glass eels (up from the sea, not from local spawners):** code: a third direction whose dues come from the sea, sized by
the catchment, feeding the eel's resident stock (today stood for by `b` 3.0, `kinds.py:55-58`).

**Coarse fish spawning in the shallows (pike, perch, bream, roach, tench in spring):** code. It is not a run along the river. The
nearest existing rule is `periodic` (`renewal.py:47-63`: a stock drawn to `run_K` in its seasons), which already exists, but its
season is a window and its `run_K` is a maker's number. A gathering on the shallows or the body's fish, by water type and the
water's warmth, is new.

**A new resident kind (pike in a mere, trout in a beck, tench in a fen):**
- *As the body's fish:* code. The body holds one `fish` record (`waters.py:21`); the take, the signs and the renewal read that one key.
- *As a wild population (as the yellow eels are):* data for the wild layer (a `KINDS` row with a water habitat, `TAKEN`, `TRAITS`), and
  the set gear meets it by traits (`wild.py:1040-1056`); but angling and the edge never draw a wild population (they draw `fish` and
  `shallows`, `data.py:711-720`), and the generator places no kind by water type. Which kinds live where is the habitat weights only.

## 10. What breaks or goes silent

**A lake.** A lake parcel is not river (`physical.py:311`, `write.py:84`, `wild.py:3038-3040`): no run reaches it (`water.py:181`),
no weir fishes it (`wild.py:3248`), no river record or river signs (`river.py:275-282`: the village's "water" is a river parcel; with
none, `day_signs` returns, `river.py:434-435`). The lake's eels never run out of it unless its area also holds river cells
(`runs.py:380-386`). Its open-water fish exist only where `make_water_worlds` stocked it. Its shallows are 2 a cell on one or two cells
(`water.py:21`, `settle.py:335`). Lakes are rare where they do not belong (`physical.py:292-297`; L-75).

**A fen.** No body and no open-water fish (§1); shallows K 7; a trap meets a run at half only if the fen touches a river parcel
(`water.py:182-183`); its small streams sink (`physical.py:312`), so a fen's drains are not rivers and hold no run. Its eels are the
wild layer's, and run only from areas with river cells. The fen's own rows ("the fen's dykes brim", `river.py:248-250`) need that river
beside it.

**A beck.** A home village never gets a brook water parcel (`settle.py:328`), so a village on a beck alone has no water to fish. Where
a brook parcel exists, it is typed "river" if its body is a reach (`water.py:71`). Its flow answers rain as a big river's does
(`runs.py:282-289`). Lampreys reach its head waters (`runs.py:127-136`); the beck's weir row is reached only above 150 m.

**An estuary.** The generator can lay one (a tidal inlet, `macro.py:115-121`), but the sea is outside the wild land: no area, no body,
no stock, no tide; the river's mouth is "out" as at the window's edge (`areas.py:121-129`). A place on its water types it as a pool
and freezes it (`areas.py:174-177`, `water.py:24-25`). Every up-run does pass the mouth stretch on its first day (`runs.py:420-425`), so
a village at the head of the estuary sees the whole run: that part works.

**A dry year.** The cues fire less (absolute thresholds, `runs.py:198-202`); eels may not run at all, the up-runs come on one forced
night (§4.3). The flow reads "low" (`data.py:473`), which only signs read (`river.py:221-224`). The shallows, the resident fish and
the ice do not notice (`water.py:105-112`, `renewal.py:143`): no fish crowded into pools, no stranding, no low-water kill. A dry
generated climate is drier only through smaller rivers (the flow accumulation is rain-weighted, `physical.py:29`), not its days
(§4.3, `write.py:362` unread).

**A dam.** A mill's shut gap holds half an up-run a mill (§4.4) and the rest goes on; general and visible ("held" rows,
`signs.py:2479-2483`). A weir is never a barrier, a beaver's dam never touches a run, and the held fish never wait for the gap to open:
they are gone the next night (`runs.py:344`). Eels going down pass every dam; the race takes its share (`wild.py:3254-3267`).

## 11. The changes that would make it general, ranked by what they matter for worlds other than Eelmouth

1. **Resident fish from the land, in the engine, for every body.** Seed each body's `fish` from its own size and kind (lake km2, the
   reach's river km and class, a brook's or pool's area, a fen's water; later the sea's) times a productivity a hectare by water kind
   and warmth, r on the year clock, one renewal rule; drop the three makers' rules (`make_peoples.py:278-293`,
   `make_water_worlds.py:141-172`, `make_nutrition_runs.py:134-145`) to arms that scale it. Without this a generated world has no open
   water fish (§2). With it, tie the food web's fish to the body by one conversion (L-116).
2. **Timing from conditions, not windows and set nights.** Make the cue a probability that rises with conditions: thresholds against
   the climate's own rain (read its mean, not 3.4) or the catchment's flow (the level, D2-215), warmth and day length for the spring
   runs, a hazard that grows through the season instead of a last-day dump; windows as shares of the season, not days of an 8-day
   one. Then retire `runs_set_nights`. Fix that an unknown cue key means "every night" (`runs.py:195-203`). One cue function for the runs
   and the signs (`wild.py:1439-1441`).
3. **Water where the land has it.** Let a home village take a brook, a lake shore or the sea as its water (`settle.py:328`); size a
   parcel's shallows and its share of the body by its margin, not its cell count; mark lake cells on the river's course as a run's
   water at the outlet (`physical.py:311`, `_river_parcel`); give the sea and an estuary a body type with its own ice row; keep the
   window's edge apart from the sea.
4. **Signs and lore from the `RUNS` rows.** Rows by direction, size and the kind's plural (the generic `RUN_SIGNS` already exist,
   `kinds.py:902-917`), each run's own window and cue; the lore lines from the rows and the land (and write `river_class`, or read
   what the generator writes, `founders.py:327-335`). Then a new run kind is seen.
5. **The runs' vocabulary.** Per-kind speed; a sea-recruited direction (elvers); a spawning gathering in place (coarse fish in the
   shallows) as a seasonal rule on the shallows or the body, driven by warmth; spawning in lakes and becks as `where` values.
6. **Hydrology as its own data.** Flow classes out of the weir's wear row, answering the catchment's size (a beck flashy, a big river
   slow); the climate reading the generator's rain for the place (`write.py:362`), so a wet and a dry world differ in their days.
7. **Dry-year and flow effects on the stocks.** Low water crowds the resident fish and the shallows (easier taken, later a loss); a
   spate scatters them (L-150).
8. **The works by the water's size.** A weir's share by the river's width, a beaver's dam as a partial barrier, held fish waiting
   below a shut gap for some nights.

Items 1 to 3 change every generated world; 4 and 5 are what stage 5b's spring calendar (a lamprey run, coarse fish spawning) needs
to be data rather than code; 6 to 8 refine what already works.

## Appendix A: the one check run

A short script (kept out of the commit, which is this file only), run as `python3 cues.py cybertron2/specs/nutrition/eelmouth.yaml 40`:
40 world years of `WL.weather` at the world's one node (days from 1,000 years ahead, as the history does), counting the nights inside
each `RUNS` window on which `runs.cued` holds with a one-node catchment (Eelmouth's catchment is its own node):

```python
w = World(load_spec(path)); m = WL.model(w); Y, S = m.Y, m.S; node = sorted(set(m.nodes))[0]
rain = [WL.weather(w, [node], 1000 * Y + d)[node]["rain"] for d in range(years * Y + 8)]
for y in range(1, years):
    for k, r in WK.RUNS.items():
        n = sum(RU.cued(nt, "g", r["cue"], {node: [rain[d - j] for j in range(RU.MEMORY)]})      # nt.catch = {"g": {node: 1.0}}
                for d in range(y * Y, (y + 1) * Y) if RU._in(r["seasons"], d % Y, Y, S))
```

| Kind | Window nights | Cue nights a year (mean, min, max) | Years with none |
|---|---|---|---|
| eel (`rain_after_dry` 2) | 8 | 0.36, 0, 1 | 25 of 39 |
| salmon (`spate` 1.2) | 12 | 2.79, 0, 8 | 9 of 39 |
| lamprey (`spate` 1.0) | 8 | 2.15, 0, 5 | 9 of 39 |

The climate's mean rain over 20 years: 2.61 a day (Eelmouth), 2.71 (`specs/water/lake.yaml`); 2.0 every day where the climate is off
(`wild.py:56-59`). A catchment over several nodes averages their rain (`runs.py:189-192`), which makes the threshold rarer still.
