---
id: docs/review/38_space_engine/73_brief5_gate.md
kind: note
updated: "2026-11-16"
tags: [note, open]
---
# 38.73: Brief 5 (river and water) as built: the dry-run report for the gate

## Text
# 38.73: Brief 5 (river and water) as built: the dry-run report for the gate

Session 37.4, 16 Nov 2026 (WORK [[W-48 Build brief 5, river and water (D2-209; proposalsriver_and_water|W-48]]; [[D2-209 Brief 5 (river and water) is built|D2-209]]; proposals/river_and_water.md). Built on branch `ecology-water` (5033573), in three
parts merged together: 5-river, 5-keep and 5-fowl. The worlds are 37.2's (`cybertron2/specs/water/`, [[W-47 Brief 5's worlds and the runs-only world (Zach, 16 Nov design the|W-47]]). The full suite passes,
629 tests. Not merged to main. Dry runs only. Build notes for each part:
- the river: `docs/review/38_space_engine/72_brief5_river_build.md`, with harnesses `docs/review/37_growth/02zzd_ev/ev_river.py` and
  `river_society.py`;
- the fuel budget: `docs/review/38_space_engine/72_fuel_budget/`;
- all on the branch.

## What was built

| Part | Built | Calibrated numbers (all `calibrate`) |
|---|---|---|
| **Runs (§2)** | A rule over any kind with `mover: run`. The cue is read over the catchment, and the lag is a day per 10 km of river. A village's home and ring are one stretch (§2.4). The run thins as it is taken and is gone at the sea. | eels: 0.2 of each area's stock run in a year, 0.6 of those left on each cue night; run heads ×3 to the take's density |
| **Salmon, lamprey (§4)** | Run-only kinds. The return one world year later is 2s/(1 + s/(cap × river km)) from the s spawners that reached the head waters. | salmon cap 1.5 a km, meat 2.0, autumn and early winter; lamprey cap 3, meat 0.3, spring |
| **The weir (§3)** | A crew work (`with` on the first build), worn by floods and ice, mended. Its gap is set by its crew or its managers. The catch goes into its own set thing (brief 4c's finding, lifting, robbing). | timber 12, 24 units; shut takes 0.5 of each run passing × condition (sound 1.0 to holed 0.3); open takes 0.05; shutting costs 2 units, opening 1 |
| **The mill's gap (§3a)** | Only where a run passes; starts shut. Shut: half of a run going up is held below the dam, takeable that night; a run going down goes through the race, where a trap takes the weir's share. Open: half grinding rate ([[Q-51 Brief 5 (river and water)|Q-51]] default), and the runs pass. | |
| **Otter (§4)** | A resident water kind. It robs unwatched set things in water. A watch now covers water; a snare at water takes otters. | robs at 1 − e^(−0.1 × otters) a night, 0.3 of the catch, at most 4 |
| **Wildfowl (§4)** | Frost pushes them onto the water that is still open: small waters freeze after 1 hard night, big rivers after 3, lakes after 5. They weaken (built), and die in the great freeze (built). Survivors return on the thaw. | crowding ×(wet + water)/(open water), at most ×4 |
| **Beaver (§4)** | The dam drowns the meadow beside the lodge and raises the fish in the pond. Breaking it reverses both, and the dam stays down a season. | meadow hay ×0.6, pond fish ×1.3 |
| **Heron (§4)** | Herons take the village's fish, and the heronry grows or falls with the fish it can keep. | 0.02 fish a nest a night; 1 fish standing a nest |
| **Smokehouse (§4a)** | A building of its own with smoke racks. Batches up to 40, 3 nights of fire, tended daily. Untended, the fire dies, the batch pauses and spoils that night. Wattle can catch fire, and the fire spreads only on its own parcel. Owned by its household; rented by agreement; can be robbed. | 1 firewood a night; fire chance a night wattle 0.02, timber 0.008, stone 0.0003; smoked goods keep 4× as long as dried meat |
| **Salt inland (§4b)** | `brine` springs (pinned by the generator) and a `brine pan` fitting at or beside one. `boil salt` works in any season, as the salter's trade. | 1 firewood a salt, 1 unit for 4 salt (OPEN [[L-110 Salt's fuel, to recalibrate|L-110]]) |
| **Fuel (§4c)** | No new mechanic. A harness (`python3 -m cybertron2.fuel_budget`) reports firewood by use and the woods by village. | |

## The dry runs

**Run-night food a unit** (`ev_river.py`, river.yaml, 16 nights):

| Village | Weir shut that night | Weir kept shut | Wicker trap | No run |
|---|---|---|---|---|
| Saltwell (upstream), eels | 0.3 to 1.4, mean about 0.7 | 0.9 to 4.2 | 0.05 to 0.3 | 0 |
| Millham (downstream), eels | 0.3 to 2.1 | 0.9 to 6.3 | 1.1 to 6.5 (in the race) | 0 |
| Millham, salmon | **4.5 to 5.5** | **13 to 17** | | |

Eels meet the target (about 1 to 2 a unit on a run night, nothing otherwise). **Salmon are far over it**, and the weir's catch has no
cap. That is 37.2's data to bring down: cap, meat, `dense`, or a cap on the catch.

**Between the villages** (`river_society.py`, 40 nights):
- **Upstream weir:** Saltwell's weir shut lowers Millham's autumn eel catch by 16% (68 against 81). Most of Millham's run comes from
  eight other stretches above it.
- **Mill dam:** Millham's dam kept shut halves the salmon reaching Saltwell (5.3 against 11.3). It cuts next year's return above
  Millham by 37%, or by 58% with Saltwell's weir also shut.

**Keeping a glut:**
- **Smokehouse:** a 40-meat glut loses 3 to 5% through the smokehouse, tended.
- **Hearth rack alone:** it loses 23% (autumn) to 30% (summer), not the brief's "about half". That follows from fresh meat's store
  rate as built (9% a night).

**Fuel over a year** (river.yaml, bots, 32 days):
- **Hearths:** they burn about 335 firewood a village.
- **Smoking and boiling:** they add 25 to 45% to Saltwell's draw.
- **The near woods:** their dead wood falls to about a third in a year on hearths alone, against about 48 a year of regrowth. Fuel
  binds within a year or two, and no hearth went short in the year.

**The freeze** (lake.yaml):
- **Nets:** they pay about 0.15 to 0.93 meat an act on the open water through 1 to 5 hard nights, then nothing once the lake freezes.
- **The ring's fowl:** they are under 70% of a mild winter's after 8 frozen nights.
- **How often:** frost spells longer than 5 nights came once in 10 years of the steady climate.

## Choices made while building (for Zach)

1. **One rack batch at a time** per hearth, fire ring or smoke racks. This is new. Without it a household hangs five batches at its
   hearth and never needs a smokehouse.
2. **The salt fitting is keyed `brine pan`,** because `salt pan` is the shore's sun-dried technique. "build salt pan" resolves to it.
3. **The weir's crew** is checked on the first build act only.
4. **A village's weir or mill takes from every run through its stretch,** whichever water parcel it stands on: the land does not say
   which river a parcel is on.

## World issues (37.2's worlds, 37.4's generator)

- **No climate in river.yaml:** the rain cue never fires, and runs come on days 2 and 5 of their window (`RUN.no_weather`).
- **The worlds do not remake exactly:** `make_water_worlds.py` gives a different river and lake world from the committed ones, under
  fixed hash seeds too. The committed files were used. This is likely the generator's process dependence, found earlier in brief 4c's
  predator build.

## Before a live run or the merge

- **37.2:** salmon's numbers; a climate in river.yaml; the remake.
- **Zach:**
  - the one-batch rule;
  - the merge of `ecology-water` to main;
  - a small live run on the river world, read against the pack off: crews on run nights, weirs built and kept, the gaps disputed,
    salt traded.

*Current as of 16 Nov 2026.*

