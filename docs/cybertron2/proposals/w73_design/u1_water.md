# U1. Water and wild stocks: the shallows by water type, the runs, the freeze, the run's fixes

**Status:** discussion (component spec of the integrated design, W-85). Nothing here is decided beyond the decisions it cites; nothing
built. **Owner:** 37.2 (the wild, the water). 37.4 is named on the merge of the core files listed under "Code changes" (world.py,
renewal.py, knowledge.py). **Thread:** the wave's integrated design (W-85), under the network (W-73) and the nutrition worlds (W-69).


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-315:** wild rates still on the day clock stay as calibrated, read in live runs.
> - **D2-316:** a runs world is water-only: small resident and shallows stocks always present, the runs the main part (no 'no resident fish' switch).
> - **D2-317:** shallows one stock per parcel, with their own signs for their own creatures.
> - **D2-318:** fowling postponed to the hunting build-out (no fowling net, no fowling method in this wave).

## Extends

Read in full for this spec, not only their summaries:

- **proposals/river_and_water.md** (D2-209, D2-210 and the brief 5 decisions D2-211 to D2-219): the runs as pulses along the river,
  the weir in sections, the trap's hold, the wreck in spate and flood, the kinds on the water, the otter.
- **D2-229**: one resident fish stock per water body (a lake's one stock; a river's one stock a reach), held in `s["waters"]`
  (engine/waters.py).
- **D2-264**: the water holds a shallows stock of its own; the relative stocks of shallows, open water and runs vary with the kind of
  water the world generates, the signs following; a trap set lays up to about 6.
- **D2-265**: a freeze stops fishing, to be refined with the other environmental effects (OPEN L-150).
- **D2-273**: the wild's production and regrowth are on the year clock.
- **D2-258, D2-259** (the runs at a real river's size, real values or named levers), **D2-262**, **D2-293** and **D2-297** (the catch
  basis kept as calibrated; calibrated in live runs with the rest of the wave), **D2-298** (bots test interfaces only).
- **proposals/hunt_fish_materials.md** §2 (the land and water the network draws on), §7.1 (three stocks, five methods), §7.8 (the
  shallows by water type and the fen's traps).
- The drafts: docs/review/37_growth/02zzzh_hunt_fish/wave3_taking.md §1.2, §3 (bug 1, bug 3, faults 10 and 13), §4.5 (the freeze),
  §7 rows 6, 13 and 17; catch_basis.md §1 to §5; wave_conflicts.md C12, G1, G6, E5; fishing_ladder.md §1, §2, §4, §5 (the real
  anchors for the shallows).
- Records read: OPEN L-150 (freezes, floods and the fen traps refined later), Q-77 (spate and flood frequency, default: wait for the
  river level), L-116 (the wild layer's fish and a water body), L-75 (the generator's lakes), Q-57 (the Brook fished out in ten days),
  Q-79 (the fishing bugs), W-72 and W-81 (threads waiting).

## Departures

| From | What it said | This spec | Why |
|---|---|---|---|
| wave3_taking §2.1 | a wicker trap takes from the shallows and from a run | a trap's resident take stays on the wild layer's eels (the yellow eels, `KINDS.eel`, as built in `_set_night`) and the run; it does not also draw the shallows | the eels at the edge are already the trap's resident stock; drawing the shallows as well would count the edge twice. The shallows is the hand's, the dip net's and the spear's |
| wave3_taking §2.1, §5.1 | a trap's run reach "about 0.006 of the eels passing" (and §5's worked nights on it, and on the replaced half-lost keeping curve) | the trap's take of a run is the code's, unchanged (`SETS["trap in water"]` `meet` 0.3, `base` 0.5; `RUN.dense` 3.0), measured by the bots at about 1.1 units landed a trap-night (catch_basis §1) | D2-297 keeps the catch as calibrated; the 0.006 was an estimate made to fit an invented walk. §5's figures are not used here |
| catch_basis §5 | cut the set trap's take of a passing run by about 3 | not taken | D2-297: no recalibration now |
| D2-229 (one stock per body) | the resident fish are one stock on the body | the shallows are one stock **per parcel** (a margin is local); the open water stays one stock per body | small fish, crayfish and edge eels are sedentary and strip in days where they are fished; a lake's whole rim fished from one parcel would be wrong. Question 5 |
| river_signs §2.6, open question 6 ("the engine fishes on under ice; reword the frozen signs") | reword now, change the engine later | the engine changes: a freeze stops set gear, the edge and bank lines, holds the eels' run, and lets salmon pass under edge ice | D2-265 decided a freeze stops fishing; river_signs was written before it |
| wave3_taking §4.5, question 10 | a hard-frost night holds "the run" | eels are held at any ice on their stretch; salmon and lampreys pass under edge ice and are held only when the stretch is frozen over; the weir alone takes at edge ice | the morning brief's default (morning_23nov §C 16: "checking that a big river's open stream still lets a run pass"); the record has salmon running under ice. Question 2 |
| D2-218 and the code (wild.py:3160) | a set trap in the fen meets the run in full and is never wrecked | a trap in a fen beside the run's water meets half a river trap's share of the run, and is wrecked at about a twentieth of the river's rate; a fen not beside the run's water meets no run | the fen as a loophole (river_signs question 5, L-150, hunt_fish §7.8); the change touches only traps in the fen. Question 1 |
| basis.md §4 ("a set trap holds 10 units") | units | the trap's hold is **10 kg** (WATER_WORKS trap `hold`, data.py:388) and the weir's holds 100 and 70 **kg** | the code and D2-258 ("a trap about 10 kg, a weir section about 100 kg") count kg; the basis row is a slip (Basis rows needed) |
| hunt_fish §2 (eels "speared through ice in winter", fishing_ladder §2a, §2e: ice fishing) | real | not now: through-ice spearing and ice fishing wait (Gaps) | D2-265's base rule; L-150 refines |

## Purpose

The water is three foods, not one (fishing_ladder §1): **the shallows** (small fish, crayfish, yellow eels at the edge: small, quick to
strip, quick to come back in summer, nothing in winter); **the open water** (the body's resident fish, D2-229: pike, roach, perch,
trout in the pools, reached by a line or a net); and **the runs** (silver eels down, salmon and lampreys up: huge brief pulses, as
built). Which of the three a water holds most of follows the kind of water (D2-264), so that a brook feeds a hand, a lake a net and a
big river its weir. A freeze stops most of it (D2-265). And the run's take is made honest in two places the live runs exposed: a run's
fish never learn wariness, and the fen is no longer a place where a trap meets the run in full and is never wrecked.

## The design

### 1. The three stocks, and what reaches each

| Stock | State (engine terms) | Where it is held | Clock | Reached by (U2's acts) |
|---|---|---|---|---|
| **shallows** (new) | a parcel stock `res["shallows"]` = {S, K, r_by_season, renewal: "shallows"} | every parcel with cover `water` or `fen` (§2) | year clock (D2-273) | the edge (hands, a dip net, a spear) |
| **open water** | the body's `fish` record, one object shared by every parcel on it (waters.py, D2-229) | each water body (lake, reach, brook, pool) | as built (r a night; see Gaps on its clock) | line fishing, a set line, a gill net |
| **resident eels** | the wild layer's `eel` population by area (`st["pop"]["eel"]`, `KINDS.eel`), times `SW.resident` | the village's home area and ring | the food web (year clock) | wicker traps, a baited set line (as built in `_set_night`) |
| **the runs** | pulses by kind, stretch and day (`st["runs"]["pulses"]`, wild/runs.py) | the river's stretches | the year clock (D2-209, D2-273) | the weir, the race, traps, a gill net (salmon), the edge at a pinch (§5) |

The resident eels and the run are the same kind in two stocks: the yellow eels are resident all year, and the silver eels that run are
`RUNS.eel.year` (0.6) of each river area's eels at the window's start (runs.py `advance`), as built.

### 2. The shallows by water type (D2-264; gap G6, designed here)

**The water type of a parcel** (one function, `wild.water_type(w, pid)`), read from what the land already holds:

| Type | Read from | Notes |
|---|---|---|
| `brook` | the parcel's body has kind `brook` (wild/areas.py `waters`), or `land.river == "brook"` | a small stream: nearly all margin |
| `pool` | body kind `pool` | a still pond or wet hollow |
| `river` | body kind `reach` and the village's stretch holds no big river (`RU.net(m).big[f"v:{node}"] == 0`) | a lowland river |
| `big river` | body kind `reach` and the stretch holds big river | thin, steep margins |
| `lake` | body kind `lake` | a rim of a large body |
| `fen` | cover `fen` (a land parcel: dykes and pools) | eels and shallows |

A hand-made world with no bodies falls back on `land.river` ("brook", "river") and, for a water parcel with neither, `pool`.

**The real anchors** (fishing_ladder §1 and §4, all search summaries or estimates there): a trout brook holds about 100 to 200 kg of
fish a hectare; a 3 m brook is about 0.3 ha a km, so **about 30 to 60 kg standing a km**; it yields **about 10 to 45 kg a km a year**
to take (production 20 to 168 kg a hectare a year in the stream studies; P/B 0.6 to 1.1). Small whole fish are about **0.75 fish
units a kg** [est.: the unit is 1,150 kcal, about 1 kg gutted and headed (data.py:47-49); small fish are about three quarters edible].
A unit of size is one 150 m cell, **about 2.25 ha** (D2-181; landgen/vocab.py:9), so a water parcel holds about 0.15 km of channel a
unit of size.

**K, a unit of size** (the generator's margin, when written, replaces "a unit of size" by the parcel's own margin in km: §7):

| Type | Margin a unit of size [est.] | Density along it [est., from the anchors] | **K, units a unit of size** | Real check |
|---|---|---|---|---|
| brook | 0.15 km of channel | 22 to 45 units a km (the brook's 30 to 60 kg) | **5** | 3.4 to 6.8 by the anchor |
| pool | the whole pond is margin | about 2 units a hectare of pond [est.] | **4** | none sourced |
| fen | about 0.2 km of dyke and pool edge | a brook's density | **7** | none sourced; "a fen: eels and shallows" (hunt_fish §7.8) |
| river | 0.15 km of river, two banks | about half a brook's a km of bank (deeper, silted banks) | **4** | none sourced |
| big river | 0.15 km, two banks | about a quarter of a brook's a km of bank (steep, fast, deep margins) | **2** | "thin shallows" (fishing_ladder §5) |
| lake | its rim cells, about a third of a mere parcel's cells | a brook's density a km of shore | **2** | none sourced |

**Renewal** (a new renewal rule `shallows`, engine/renewal.py): logistic toward K at the season's rate, on the year clock:
`S' = S + r_s × S × (1 − S/K) + 0.01 × K × r_s / 0.10` (the last term lets a stripped margin come back from fish moving in, as the
existing `fast` rule's 1% refill does), with **r_s a night: spring 0.06, summer 0.10, autumn 0.06, winter 0.01, and 0 on any night
the parcel is iced (§4)** [est.]. Check: the mean r of about 0.058 gives a most-sustained take of r × K / 4 × 32 nights ≈ 0.46 K a
world year, against the anchor's 10 to 45 kg taken from 30 to 60 kg standing (0.33 to 0.75 of K) in a real year, which the year
clock puts into the 32-day year (D2-273). Stripped to its refuge in summer, a margin is back to half in about 10 to 15 nights; in
winter it barely moves.

**What it gives:** `fish` (fresh fish, data.py:49), as the edge's goods. What it holds is small: a brook parcel of size 2 holds 10
units (about 4.6 food); four people at the edge strip it in a day or two, and it then gives about a quarter of a unit a night. That is
the floor fishing_ladder §1 asks for ("It is the floor, and it should be a meagre one").

**The edge's refuge:** the shallows go to the parcel stocks' `refuge` (here.p["refuge"], as `fish` and `plants` do in
knowledge.py:222), below which the edge is refused unless a run passes at a pinch (U2 §2.6).

### 3. The relative stocks by water type (D2-264)

What a person meets at each kind of water, once the shallows are in. Open water K a unit of size is today's (`8 × RESIDENT_FISH` =
17.6, make_peoples.py:276, make_water_worlds.py:170; a lake's mere by area, make_water_worlds.py:131-166), with one change proposed
for brooks (question 3).

| Water | Shallows K a unit | Open water K a unit (today → proposed) | Runs | The water's character |
|---|---|---|---|---|
| brook | 5 | 17.6 → **3.5** (×0.2) | lampreys where the brook is on a river that runs (`RUNS.lamprey.where` "river") | a hand's water; little for a line |
| pool | 4 | 17.6 → **8.8** (×0.5) | none | a little of both |
| fen | 7 | none (a land parcel) | eels where the fen is beside the run's water (§6) | eels and shallows |
| river | 4 | 17.6 | eels, lampreys; salmon only on a big river's system (`RUNS.salmon.where` "big river") | some of each |
| big river | 2 | 17.6 | eels, salmon, lampreys | the runs and the weir |
| lake | 2 | the mere's stock by area (up to about 370 a unit) | none (no run enters a lake in the engine) | a net's and a line's water |

**The brook's open water** is cut because the anchor puts a brook's whole stock at 3.4 to 6.8 units a unit of size and today's 17.6 is
2.6 to 5 times it (the Brook fished out in ten days, Q-57c, was fished down from that). With the shallows its total is 8.5, still
above the anchor; the rest is left to the calibration suite. **The river's open water** looks low by the same anchors (about 10 kg of
whole fish a hectare against a real lowland river's 20 to 100 and more) and is **not** changed here: re-anchoring it is the
calibration suite's (D2-245, D2-252; Gaps).

### 4. The freeze (D2-265; gap G1, designed here; basis §4 default, detailed)

**The ice on a parcel** (a pure function, `wild.ice(w, pid, day)` → `open`, `edges` or `over`), from the nights of hard frost in a row
at the node (`wild.frozen_run`, wild.py:1207: a low under −3 °C and a day under 3 °C) and the water type (§2). A new data row beside
`OPEN_WATER` (kinds.py:399):

```
ICE = {"edges": {"brook": 1, "pool": 1, "fen": 1, "river": 1, "big river": 2, "lake": 1},     # nights in a row: its edges are ice
       "over":  {"brook": 2, "pool": 2, "fen": 2, "river": 4, "big river": 5, "lake": 6}}     # nights in a row: frozen over
```

[default; consistent with `OPEN_WATER.hold` (small waters open 1 night, a big river 3, a lake 5, then the fowl leave) and with the
great freeze at 4 nights (`REGIMES`, kinds.py:534), when a lowland river is frozen bank to bank and a big river still has a lane]. The
first day not frozen after a run of 2 or more is **the thaw**: the ice going out; for fishing it counts as `edges` that day.

**What a freeze does**, by act and stock (each reads `ice` at the parcel, or for the runs at the village's first river parcel):

| What | At `edges` | At `over` | Wording (U2 results, U8 signs) |
|---|---|---|---|
| set gear in water (wicker traps, a set line, a gill net) | **idle**: takes nothing, no draw on the resident eels or the run, not wrecked, not robbed by otters; fish already in it stay alive (D2-211); its life runs as any night it stands (U3's rule for lives in nights, basis §1) | the same | U2 §2.1 "frozen in" |
| setting new gear | refused | refused | U2 §2.1 |
| the edge (hands, dip net, spear) | refused | refused | U2 §2.6 |
| line fishing from the bank | refused | refused | U2 §2.5 |
| the shallows' renewal | 0 that night | 0 | |
| the weir | **takes its share** of what passes (its gap is in the main stream, the last water to freeze); wears ×1.5 as built (`WATER_WORKS.weir.wear.ice`, `_weir_wear` wild.py:2991) | takes nothing (nothing passes, below) | U8 §2.6 |
| eels running down | **held**: no eel pulse moves on from or starts at the stretch that night; it waits to the next open night (eels do not move in the cold) | held | U8: none (nothing passes) |
| salmon and lampreys running up | **pass** (they go up the open stream under the edge ice) | held at the stretch to the next open night | U8 §2.2 rows read only `passed` |
| fowling | the fowl crowd onto the last open water (`PUSHED`, `open_water`, wild.py:1232: as built): the best fowling of the year | gone to open water further off (as built) | as built (kinds.py:357-361) |
| snares | work as usual (land) | the same | U2 §2.2 |
| the thaw | set traps in a small water (brook, pool, fen) that froze over are crushed by the ice at **0.1** a trap; in a river or a big river torn by the ice going out at **0.3** a trap [est.; calibrate]; the weir wears ×2 (`thaw`, as built) | | U2 §2.1, U8 §2.6 |

**A held run**: a pulse at a stretch on day d whose stretch is iced for its direction stays at the stretch with d + 1, is not taken by
gear that night (except the weir at `edges`, for up-runs only), and is not counted again in the year's tally (`runs.tally` counts a
pulse once, the night it moves on). A down-run's cue is not met at an iced stretch (no new eel pulse starts there).

### 5. The edge in a run: the pinch (wave3_taking question 6)

Today the edge (`fish by hand` with `run: True`) takes from a run on any river parcel (`run_take`, wild.py:3242) and is never reached
where no resident fish live (Q-79 bug 1, `knowledge.ready`, knowledge.py:206). The hand is not the tool in a run on open shallows
(fishing_ladder §2d: a dip net at falls and below weirs, "near nothing elsewhere"). **The run's density for the edge is multiplied by
the parcel's pinch factor** (a new `wild.pinch(w, pid)`):

| Parcel | Pinch | Why |
|---|---|---|
| below a weir with its gap shut, or below a shut mill's dam (fish held, `RU.today` pulses with `held`) | **1.0** | the fish crowd the pool and the gap |
| a ford (where the land records one) | **1.0** | the run crosses shallows |
| a brook or a lowland river | **0.3** | the run fills a small channel |
| a big river | **0.1** | "a few heads at best" (hunt_fish §7.1) |

[default; calibrate. The edge's take of a run has never been measured: bug 1 blocked it.]

### 6. The fen and the run (river_signs question 5; L-150; hunt_fish §7.8)

A trap's draws on a run (`_set_night`, wild.py:1000: one of the run's when `rng < r_ / (r_ + resident)`) read the run's density times
**the parcel's run reach**: a water parcel on the river 1.0 (as now); a `fen` parcel next to (`adj`) a river parcel of the stretch
**0.5**; any other parcel (a fen not beside the river, a pool, a lake) **0** (it meets no run; its traps take the resident eels only).
The wreck in spate and flood (wild.py:3155-3168, today river parcels only) applies to a fen trap at **0.02 in spate and 0.05 in
flood** [est.]. Default taken, question 1.

### 7. The runs and their fixes

The runs are kept as built and calibrated (D2-297): their sizes (`RUNS`, kinds.py:872; a real river x 32/365), the lag, the weir's
shares and holds (WATER_WORKS, data.py:376), the trap's hold and its wreck in the river (data.py:387). Two fixes, both faults that
mislead any reading (README stage 1):

**(a) A run's fish learn no wariness** (Q-79 bug 3, wave3_taking fault 10; default taken as a bug fix: W-81 question 5 is not
answered). Today `hunt` adds `WARY["take"] / max(1, resident heads)` to a kind's learned wariness for every head taken, run or not
(wild.py:2436), and `WARY["hunt"] × share` to every kind in the method's table each act (wild.py:2345); a run's salmon have no
resident heads, so one netted salmon adds 30 and the run all but vanishes to nets for weeks. The rule, in the take itself so any later
method that meets a run on the hunt's path keeps it:

1. **Wariness and pressure act on the resident share only.** A meeting's rate is
   `(resident_density / (shy × press) + run_density) × detect × ...`, with `shy = 1 + detect × learned(wary)` and
   `press = 1 + 0.5 × min(4, pressure)` (today both divide the whole density, wild.py:2358-2359).
2. **A head met is drawn as resident or of the run first** (the ratio at wild.py:2438, moved before the flight), and a head of the run
   flees at the kind's own `flee` (no learned wariness, wild.py:2423).
3. **Only a resident head taken adds wariness and pressure** (wild.py:2434-2436); the act's own increment (wild.py:2345) is scaled by
   the kind's resident share of the density at that area, so a kind with no resident heads there learns nothing.

After the fowling split (U2 §2.4), no method on the hunt's path meets a run; the rule stands as a guard.

**(b) The fen** (§6).

### 8. The night step, in order

Each night, in `wild.night` (wild.py:132), for each village on the water:

1. `ice` read for each water and fen parcel (§4).
2. The shallows renewed (renewal rule `shallows`; r 0 where iced) with the other parcel stocks (night._grow).
3. `_set_night` (wild.py:921): iced set things skipped (idle); a trap's run draws by the parcel's run reach (§6).
4. `_runs_night` (wild.py:3072): the run's pulses at an iced stretch held (§4); the weir takes at `edges` (up-runs) and in open water;
   the otters skip iced parcels; the wreck by flow, the fen at its own rate (§6); the thaw's crush and tear (§4); the river's record
   for U8's signs (U8 §1); `RU.advance` with the ice of each stretch passed in.

## Code changes

| File, line | Change | Owner |
|---|---|---|
| wild/kinds.py:399 (beside `OPEN_WATER`) | `SHALLOWS` (K a unit of size by type; r by season), `ICE`, `RUN_REACH` (river 1.0, fen beside the river 0.5, else 0), `FEN_WRECK` (spate 0.02, flood 0.05), `THAW_WRECK` (small 0.1, river 0.3), `PINCH` | 37.2 |
| engine/data.py:192 | a RESOURCES row `shallows` (pack water, renewal `shallows`, low and high words left to U8) | 37.2 |
| engine/renewal.py:47 (beside `periodic`) | the rule `shallows` (§2), reading the season and the parcel's ice from ctx | 37.2 writes, 37.4 named |
| engine/waters.py (new function beside `seed`) | `seed_shallows(w)`: each water and fen parcel without a `shallows` record gets K by type and size (or margin), S = K; `water_type(w, pid)` | 37.2 |
| engine/world.py:261 (after `WA.seed`) | call `seed_shallows` at a world's making; a saved world without the records is unchanged (as D2-229's bodies) | 37.2 writes, 37.4 named |
| specs/make_peoples.py:276-292, specs/make_water_worlds.py:141-171 | open water K by type (brook ×0.2, pool ×0.5) if question 3 is answered yes | 37.2 |
| landgen/write.py:84 (in `_land`) | `land.margin_km` for each water parcel: its cells' edges facing land × the cell size | 37.2 |
| wild/switches.py:16-19 (`resident_fish`) | `resident_fish: false` also leaves the shallows unstocked; a world may set `shallows: true` to keep them (question 4) | 37.2 |
| engine/wild.py:1207 (beside `frozen_run`) | `ice(w, pid, day)`, `water_type`, `pinch(w, pid)`, `run_reach(w, pid)` | 37.2 |
| engine/wild.py:942, :1000 (`_set_night`) | skip iced set things; the run draw by `run_reach` | 37.2 |
| engine/wild.py:2341-2345, :2358-2359, :2423, :2434-2438 (`hunt`) | the wariness fix (§7a) | 37.2 |
| engine/wild.py:3137 (`_robbers`), :3155-3168 (the wreck loop), :3171 (`RU.advance`) | otters skip iced parcels; the fen's wreck; the thaw; the ice passed to `advance` | 37.2 |
| engine/wild.py:3242-3286 (`run_take`) | the run's density × `pinch`; up-runs only at `edges`; none at `over` | 37.2 |
| wild/runs.py:316 (`advance`), :336-341 (the tally) | `iced={stretch: "edges" or "over"}`: down pulses held at any ice, up pulses at `over`; a held pulse tallied once | 37.2 |
| engine/knowledge.py:206, :222 (`ready`) | the edge draws `shallows`; refused only when the shallows are at their refuge and no run passes at a pinch; never "there is no fish" (U2 §2.6 words) | 37.4 (37.2 writes the words) |

Every piece is one feature unit (D2-244): the water's stocks (data: SHALLOWS, ICE, RUN_REACH, PINCH; process: the renewal rule, the
night's steps; signs: U8; verbs: none of its own).

## Tests

Unit and interface tests (bots for interfaces only, D2-298), in the style of tests/test_cybertron2_water5_river.py:

- `test_shallows_seeded_by_water_type`: a world with a brook, a pool, a fen, a river, a big river and a lake parcel; each `shallows.K`
  is the table's × size; a world without the water pack has none; `resident_fish: false` has none.
- `test_shallows_renew_by_season_and_not_under_ice`: stripped to its refuge in summer it is above half K by night 15; in winter
  under a tenth of that; a frozen night adds nothing.
- `test_ice_by_water_type`: with `frozen_run` 1, 2, 4, 5 the brook, the river and the big river read `edges`/`over` as `ICE` says;
  the thaw day reads `edges`.
- `test_set_gear_idle_under_ice`: a line of traps in a frozen fen takes nothing for three nights, is not wrecked or robbed, keeps the
  fish it held.
- `test_eels_held_salmon_pass_under_edge_ice`: an eel pulse and a salmon pulse at a stretch at `edges`; the eels are there the next
  day and taken by nothing; the salmon move on; the weir takes its share of the salmon; at `over` both are held; the tally counts each
  once.
- `test_the_thaw_crushes_traps_in_small_waters`: over many seeds about 0.1 of traps in a fen that froze over are lost at the thaw.
- `test_a_runs_fish_learn_no_wariness`: a hunt-path method meeting run salmon on ten days; `state.wary.salmon` stays 0 and the
  meeting rate does not fall; a resident kind's wariness still rises.
- `test_the_fen_meets_half_the_run_and_seldom_wrecks`: traps in the river and in the fen beside it on the same pulses; the fen's run
  draws are about half; a flood wrecks about 0.85 of river traps and about 0.05 of fen traps; a fen not beside the river meets no run.
- `test_the_edge_reaches_a_run_by_the_pinch`: a pulse below a shut weir, at a brook and at a big river; the edge's take of it is in
  the ratio 1 : 0.3 : 0.1.
- The whole cybertron2 suite; a bot run of the remade runs world and its replay with no mismatches.

**What live runs should read** (D2-297, each against the null arm and an end-state reading): how often the edge is used and what it
yields at brooks against rivers; whether households move traps to the fen on a spate dawn; what the winter's freezes cost the trap
households against the weir's; whether any hand fishing happens in the runs world once the refusal tells the truth.

## Basis rows needed

| Row | Value | Mark |
|---|---|---|
| The trap's and the weir's holds | a set trap 10 **kg** a night; a weir's first section 100 kg, each added 70 kg (correcting basis §4's "units") | default (the code, D2-258) |
| The shallows' K a unit of size by water type | brook 5, pool 4, fen 7, river 4, big river 2, lake 2 (or the generator's margin × density) | default, est. from fishing_ladder §4's anchors; calibrate |
| The shallows' renewal | r a night: spring 0.06, summer 0.10, autumn 0.06, winter 0.01, 0 under ice; year clock | default, est.; calibrate |
| Open water by type | brook ×0.2, pool ×0.5 of today's 17.6 a unit; rivers and lakes as today | open (question 3) |
| Ice by water type | `ICE` table (§4) | default (D2-265's detail; L-150 refines) |
| What a freeze stops | §4's table | default (basis §4's default, detailed) |
| The thaw's wreck | 0.1 a trap in small waters, 0.3 in rivers | default, est.; calibrate |
| The fen and the run | run reach 0.5 beside the river, 0 elsewhere; wreck 0.02 spate, 0.05 flood | open (question 1) |
| The pinch | 1.0 below a weir or dam, or at a ford; 0.3 brook or river; 0.1 big river | default; calibrate |
| A run's fish learn no wariness | wariness and pressure on the resident share only | default taken as a bug fix (W-81 question 5 unanswered) |

## Gaps

- **G6 (the shallows by water type)** and **G1 (what a freeze stops)**: designed here (§2, §4).
- **The open water on the year clock.** `fish` regrows at r 0.3 a night on the day clock (renewal `fast`/`threshold`, make_*.py), against
  D2-273 (wave_conflicts E1). Deferred to the clocks build (stage 1, U0), which re-derives every RESOURCES `r` from a year-clock value.
- **Re-anchoring the river's open water** (about 10 kg a hectare against a real 20 to 100 and more): deferred to the calibration
  suite (D2-245, D2-252), which measures sources of nutrition world by world.
- **Herons and otters on the shallows**: the food web's fish-eaters take from the body's `fish` (waters.py `to_wild`), not from the
  shallows. Deferred: it waits on the shallows existing and on L-116.
- **Ice fishing and spearing eels through the ice** (fishing_ladder §2a, §2e): deferred to L-150's refinement; they need a hole cut as
  an act, and a winter eel stock to spear.
- **A brook through a land parcel** (`land.river == "brook"` on a meadow) holds no shallows here: deferred; small, and the generator's
  brooks are mostly their own water parcels (`water:<pid>` bodies).
- **The river's level** (D2-215) replaces the flow class behind `river_now` (U8 §1) when built; not this unit.
- **Spate and flood frequency** (Q-77, default: wait for the level): unchanged.

## Open questions for Zach

1. **Whether a trap in the fen meets a run, and how often a flood tears it away** (river_signs question 5; W-81 question 7, not yet
   filed; L-150). Today a trap in Eelmouth Fen meets the eel run as fully as one in the river and is never wrecked, so the fen is
   strictly better on every run night. Options: (a) a fen beside the river meets half a river trap's share of the run and is torn
   away at about a twentieth of the river's rate (0.05 in flood, 0.02 in spate); a fen away from the river meets no run; (b) keep it
   as it is; (c) the fen meets no run at all. Recommended: (a): it makes moving traps to the fen on a flood dawn a real choice with a
   cost. Default taken: (a). Blocks: the fen's numbers and its signs (U8).
2. **What a freeze does to the runs and the weir** (D2-265, L-150; W-81 question 10). Options: (a) eels held at any ice on their
   stretch, salmon and lampreys passing under edge ice and held only when the river freezes over, the weir alone fishing under edge
   ice; (b) every run held at any ice and the weir idle too (the literal "a freeze stops fishing"); (c) runs pass under all ice and
   only set gear stops. Recommended: (a): eels stop moving in the cold, salmon run under ice, and the weir's gap is the last water to
   freeze, which makes the weir the winter's fishery as it was. Default taken: (a). Blocks: the ice rule in the runs and the weir.
3. **Whether to cut a brook's own fish now** (D2-264's relative stocks; Q-57). A brook holds 17.6 fish units of open water a unit of
   size today, two and a half to five times what a real brook holds in all; with the new shallows (5 a unit) its total would be 22.6.
   Options: (a) cut a brook's open water to a fifth and a pool's to a half now, so a brook is mostly shallows; (b) leave every water's
   open water as it is until the calibration suite measures it. Recommended: (a) for brooks and pools only; the river's open water,
   which looks low, waits for the suite. Default taken: (b) until answered (nothing changes without a yes). Blocks: the brook's
   character and angling there.
4. **Whether the runs world's "no resident fish" switch also turns off the new shallows** (D2-256, D2-257's isolated livelihoods;
   wave3_taking §7 row 17). Options: (a) yes, `resident_fish: false` leaves no shallows, so the runs arm stays the runs alone, with a
   separate `shallows: true` to keep them; (b) no, the shallows are everywhere water is (D2-264), and the runs arm gains a small edge
   stock, stated in its README. Recommended: (a): clean isolation is the point of those arms. Default taken: (a). Blocks: the remade
   runs world (U11).
5. **Whether the shallows are one stock per parcel or per water body** (D2-229 put a lake's resident fish on the lake). Options: (a)
   per parcel: a margin is local and strips in days where it is fished; (b) per body, like the open water. Recommended: (a). Default
   taken: (a). Blocks: the shallows' seeding.

## Sources

- Code (main, 22 Nov): `cybertron2/engine/wild.py` (132, 921-1016, 1196-1275, 2214-2219, 2285-2470, 2876-2990, 2991-3019, 3072-3183,
  3185-3228, 3231-3286), `wild/runs.py` (195-300, 316-432), `wild/gear.py`, `wild/kinds.py` (55-67, 399-413, 534, 826, 854-857,
  860-902), `wild/methods.py` (44-120), `wild/switches.py`, `wild/areas.py` (135-182), `engine/waters.py`, `engine/renewal.py`,
  `engine/knowledge.py` (195-240), `engine/data.py` (47-49, 185-195, 340-390, 597-606), `specs/make_peoples.py` (270-292),
  `specs/make_water_worlds.py` (128-171), `landgen/write.py` (66-86, 436-442), `landgen/vocab.py:9`; the runs world
  `specs/nutrition/runs_medium.yaml` (the Isel, size 2).
- docs/cybertron2/proposals/river_and_water.md, hunt_fish_materials.md (§2, §7.1, §7.8), river_signs.md (§2.6, §2.10, open questions 5,
  6), w73_design/README.md, w73_design/basis.md.
- docs/review/37_growth/02zzzh_hunt_fish/wave3_taking.md (§1.2, §3, §4.5, §7, §8 questions 5, 6, 7, 10), catch_basis.md,
  fishing_ladder.md (§1, §2, §4, §5), wave_conflicts.md (C12, E1, E5, G1, G6), morning_23nov.md (§C 16).
- DECISIONS D2-181, D2-209 to D2-219, D2-229, D2-245, D2-252, D2-256 to D2-259, D2-264, D2-265, D2-273, D2-293, D2-297, D2-298; OPEN
  L-150, Q-77, L-116, L-75, Q-57, Q-79; WORK W-69, W-72, W-81, W-85.

*Current as of 22 Nov 2026.*
