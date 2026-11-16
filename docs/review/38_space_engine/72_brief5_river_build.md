# Brief 5, the river part: the runs, the weir, the mill's gap, salmon, lamprey and the otter, as built (37.4, 16 Nov)

Build notes for proposals/river_and_water.md §2, §3, §3a and §4's eel, salmon, lamprey and otter rows (D2-209), on branch `5-river`
(from `ecology-water`). The keeping (§4a to §4c) and the fowl, beaver and heron rows are built beside this by other sessions. Nothing
here is decided past D2-209: the numbers below are `calibrate`, and the deviations are for 37.2 and Zach.

## What was built

| Part | Where | As built |
|---|---|---|
| The river as stretches | `wild/runs.py` `Net` | Each river area of `land.down` is a stretch; a village's home and ring are one stretch (`v:<node>`), so a run at a village's water is the run in either (brief §2.4); the run's density is read at the home area (its water). Each stretch knows the one below, those above, its river km and its catchment's weather (nodes weighted by river km). A chain that comes back on itself is cut. |
| A run | `runs.advance` (called by the engine each night after the takes, and in the history) | A kind with a `RUNS` row (`kinds.RUNS`; `mover: run` in its traits). Pulses {kind, stretch, day, heads, dir}. A pulse at a stretch on its day is there that day and night; then it moves to the next stretch after max(1, round(mean river km / `km_a_day` 10)) days. Down: what reaches the sea is gone. Up: it climbs the path from the river's mouth to its head water and spawns there. |
| The cue | `runs.cued` | Read over the catchment with tomorrow's weather (the engine passes it), so the run is at its source on the cue's own day and night: `rain_after_dry` 2 (eels), `spate` x1.2 the mean rain (salmon), x1.0 (lamprey). **A world without the climate** (every day's rain the same; the river world has no `climate`) runs on set nights: the window's 2nd and 5th days (`RUN.no_weather`). |
| Silver eels | `RUNS.eel` | Autumn; at the window's first day each river area's runners for the year are `year` 0.2 of its eels (the brief's "about a fifth"); each cue night `night` 0.6 of those left run, leaving the area's count. The elvers are the ecology's own spring breeding (unchanged). History with runs: the river world's eels settle about 19% lower (9,000 against 11,100). |
| Salmon, lamprey | `KINDS` (migrants that arrive as no one: no resident stock), `RUNS` | Up-runners. Each head water (a stretch with none above; salmon: on a river whose way to the sea holds big river) returns next year (one world year, D2-209) `r` 2 x s / (1 + s / (`cap_km` x its river km)) from the s spawners that reached it; the return enters at the mouth, `night` 0.35 of what is due each cue night, the rest on the window's last day. Salmon: autumn and winter days 1 to 4, cap 1.5 a km, meat 2.0 a fish; lamprey: spring, any river, cap 3 a km, meat 0.3. Seeded at world build at `seed_km` (1.0, 2.0) a km of head water, then the history runs them. |
| The take | `engine/wild.py` `hunt`, `_set_night`, `run_take` | A run's heads at its stretch today, x `RUN.dense` 3 (the run thicker in the water fished), are added to the resident density by the take's rule (brief 4 stage A); one taken is the run's with the chance run / (run + resident), from the largest pulse there. The eel-night multipliers (brief 1) now apply only where no river runs at the village (`river_run: False`). `fish by hand` (`"run": True`) also takes from a run at a river parcel, by the take's rule over its unit (a fifth of a km2). Net takes salmon (its size range widened to medium: no other kind changes). |
| The weir | `data.MONUMENTS["weir"]`, `verbs._monument`, `wild._runs_night` | A monument-like work built at a water parcel on a river ("river" or "brook"), timber 12, 24 units; crew work: the first act names `with` (at least one other person at the place), recorded as its `crew`. A building with a condition, so brief 4's levels apply; `night._wear_night` wears a weir only by the river in flood (heavy rain) and ice (a frozen night: new cause `ice` [3, 4]); mended by `repair`. Its gap starts shut. Shut, it takes `shut` 0.5 of every run at its village tonight (up and down), x `by_level` (sound 1.0, worn 0.8, gappy 0.6, holed 0.3, failing 0.1, ruined 0); open, 0.05. The catch goes into the weir's own traps: a set thing at its parcel (`set.weir`), never sprung, known to its crew from its first night; lifted, robbed and remembered by brief 4c's rules; a non-crew taking leaves the `robbed` trace and an event that concerns the crew. |
| The gap | `verbs._set_gap` (`set` {"thing": "gap", "to": open | shut, "at"}) | A weir's by its crew or its managers; a mill's by those who manage the water wheel (D4-95 rights). Setting a weir shut takes 2 units (the traps put in), open 1; a mill's 1 either way (the verb's cost, `data.WATER_WORKS`). Each set is an event and a sign that day and the next. |
| The mill | `wild.has_gap`, `mill_water`, `mill_rate`, `_dam_stops`, `_runs_night` | A water wheel has a gap only where a run passes (its village's stretch is on the river): its water is the river parcel at or beside its building, else the village's river water (the river world's mill stands on the Green, not beside the water). Shut (the default): `water mill` at full; a run going up is split as it arrives: `stop` 0.5 held below the dam (present that day and night, takeable by net and by hand, then gone back to the sea); a run going down passes through the race, where a trap in water set at the mill's water takes `race` 0.5 of it (no trap: it passes). Open: `water mill` takes and gives `open_rate` 0.5 (Q-51, default taken), the runs pass. |
| The otter | `KINDS["otter"]`, `wild._robbers` | A resident kind of the water (8 kg, diet fish and eels, fidelity 0.6, about 3 near each river village after the history). Each night every set thing in water holding a catch at a village with otters about (home and ring, at least 0.5) and not watched tonight (`guard the field` now also at water) is robbed at 1 - e^(-0.1 x otters) of 0.3 of its heads (at most 4), leaving `robbed_by` for its signs. A snare can now be set at water, and takes otters (traits: medium, runs). |
| Signs | `signs._wild_river`, `kinds.RUN_SIGNS` | A run at the village's water (3 heads or more): "the water alive with eels in the dark" (anyone, at night) and the practised's "a run night"; salmon going up; salmon leaping at the dam and falling back (own 1.2, anyone at the mill's water), and the practised's "net them, or draw the hatches"; a gap set (that day and the next); the year's run against last year's at the village, the day after its window, for the practised ("thin this year ... about half of last year's"); an otter's spraint and scales by the robbed traps. The layout line of a weir or mill gives its gap as it stands, and a weir's crew. |

Worlds unchanged: no run without a river (`RU.active` false: no `runs` state at all, the history as before); a mill without a run has no
gap and grinds as before; a weir's and a mill's gap default shut, so a mill on a run's river grinds as before unless opened; coastal salt
untouched.

## Calibration (ev_river.py, 16 nights from the river world's start; trap, net, hand 6 tries a cell)

Food a unit on a run night. Weir: "shut that night" counts 2 units to shut and 1 to lift; "lift only" a weir kept shut through the
season and lifted each morning (1 unit).

| Village (autumn nights with an eel run) | Run there (eels) | Weir, shut that night | Weir, lift only | Wicker trap (1 unit) | By hand | Net |
|---|---|---|---|---|---|---|
| Saltwell (upstream) | 6 to 29 | 0.3 to 1.4 (mean about 0.7) | 0.9 to 4.2 | 0.05 to 0.3 | 0 to 0.15 | 0 (eels are not netted) |
| Millham (downstream) | 7 to 41 | 0.3 to 2.1 eels only; 4.5 to 5.5 with salmon | 0.9 to 6.3; 13 to 17 with salmon | 1.1 to 6.5 (its water is the mill race) | 0 to 0.7 | 0.25 to 0.75 on salmon nights |
| Either, no run | 0 | 0 | 0 | 0 to 0.1 | 0 | 0 |

So a sound shut weir pays about 1 to 2 food a unit on a run night downstream and a little under 1 upstream, and nothing on other nights
(Zach, D2-209: "about 1 to 2"); Saltwell's run is smaller (its catchment is five areas, Millham's thirteen). A salmon night at a weir
pays much more (a salmon is 2 meat). Millham's only river water is its mill's, so a trap set there is in the race whenever the mill is
shut: it takes half the run (up to 6.5 a unit). Without the climate the run comes on the window's 2nd and 5th days at every source, so
pulses from areas of different lags pass Millham on most autumn nights; with the climate the nights follow the rain.

## Society-level checks (river_society.py)

40 nights from the river world's start (late summer to the next summer's end, so the next year's salmon return is reckoned); a
sound weir at each village's water, lifted each morning; no one else acting (river_society.json beside the harness):

| Arm | Saltwell's weir took | Millham's weir took | Salmon passing Saltwell | Next year's salmon due at the heads above Millham (all heads) |
|---|---|---|---|---|
| Saltwell's weir shut, Millham's dam shut | 66 eels, 3 salmon, 3 lampreys | 68 eels, 4 salmon, 1 lamprey | 5.3 | 7.5 (91.5) |
| Saltwell's weir open, Millham's dam shut | 6 eels | 81 eels, 4 salmon, 1 lamprey | 5.3 | 11.4 (95.3) |
| Saltwell's weir open, Millham's dam open | 6 eels | 81 eels, 5 salmon, 4 lampreys | 11.3 | 18.1 (102.0) |

- **Upstream weir, downstream catch:** Millham's autumn eel catch is 16% lower with Saltwell's weir shut. On the nights Saltwell's own
  run passes Millham the fall is the weir's half (the unit test); over the autumn it is smaller because most of Millham's run comes from
  the eight other stretches above it that are not Saltwell's.
- **The dam and the salmon above it:** the shut dam halves the salmon that reach Saltwell (5.3 against 11.3) and lowers next year's
  return to the heads above Millham by 37% (11.4 against 18.1); with Saltwell's weir shut too, by 58% (7.5).

## Deviations and questions for 37.2 and Zach

1. **The crew is checked at the start only:** the first `build` of a weir must name `with` (one or more people at the place); the work
   is then carried on by anyone, as any building. Not a party settled at the day's end (brief 4b's hunting parties): a weir is not a
   hunt. The crew are its workers for the gap and the lift without robbing; the claim is the builder's (or `for` a household).
2. **One run per village stretch:** a village's weir or mill takes from every run through its stretch, whichever of its water parcels
   it stands on (the land does not say which river a parcel is on).
3. **The weir catch has no cap:** half of a run of 40 is 20 eels in one night; at Millham a shut weir with salmon passing takes about 15
   food a lift. Historically right (weirs were rich), above the 1 to 2 target there.
4. **The mill's water when the mill is not beside it:** the river world's mill stands on the Green; the fitting's own site rule
   (`site: water`) would refuse it there, but the generator placed it. Its water is read as the village's river water.
5. **No climate in the river world:** its runs come on set nights (`no_weather`). A climate in the world would make the run nights the
   rain's (the brief's cue).
6. **Wicker traps upstream stay poor on run nights** (0.05 to 0.3 a unit at Saltwell at `dense` 3): raise `dense` if traps should pay on
   run nights away from a race.
7. **The river world's remake differs:** `make_water_worlds.py river --seeds 9` here writes a different world from the committed
   river.yaml (people try 27 against 0, other land), the same on two hash seeds; the build used the committed yaml (the engine does not
   read the cells file).
8. **Fixed in passing:** `wild.hunt` overwrote its tally of each hunter's kills with the parcel's kill record when a near hunt killed on
   its own parcel, so `practise` crashed (a net at the village water taking salmon showed it).

*Current as of 16 Nov 2026.*
