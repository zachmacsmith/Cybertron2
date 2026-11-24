---
id: docs/cybertron2/proposals/waters_general.md
kind: proposal
updated: "2026-11-24"
---
# The waters made general: resident fish from the land, runs on conditions, a spring river (stage 5b part 4)

*proposal · discussion (24 Nov 2026). **Owner:** 37.2. **Thread:** W-108 (the waters calibra · `docs/cybertron2/proposals/waters_general.md`*

> Two independent reads of the waters (docs/review/37_growth/02zzzl_waters_calib/: `sweep.md`, 51 generated worlds and 296 villages, every number from its scripts; `generality.md`, the code read for what is general and what fitted) agree: the rules are written generally (they run over `RUNS` rows, wat


**Status:** discussion (24 Nov 2026). **Owner:** 37.2. **Thread:** [[W-108 The waters calibrated across many generated environments|W-108]] (the waters calibrated), for stage 5b part 4 ([[W-107 Stage 5b of the wave, the gaps closed|W-107]]).
**Decided around it:** [[D2-347 A water-only village should be able to last the year|D2-347]] (a water-only village can last the year), [[D2-348 A water-only village is made able to last the year by|D2-348]] (a spring calendar; resident fish and shallows at
their best about a quarter of the village; [[D2-316 A runs world means a water-only world|D2-316]] still holds), [[D2-231 The runs world's runs on set nights|D2-231]] (set nights for the runs worlds, to be retired here).

## Summary

Two independent reads of the waters (docs/review/37_growth/02zzzl_waters_calib/: `sweep.md`, 51 generated worlds and 296 villages,
every number from its scripts; `generality.md`, the code read for what is general and what fitted) agree: the rules are written
generally (they run over `RUNS` rows, water types and the land's river network), but the data they read and the worlds that fed
them are fitted, and three things a generated world needs are missing. This proposal makes them general, in the order the
evidence ranks them.

## What the reads found (checked by 37.2 in the code and the data)

- **No resident fish without a maker.** The generator writes none: 0 of 109 water bodies (`villages.tsv`: 295 of 296 villages K 0
  as generated). Three maker scripts stock them by three rules on three clocks (`make_peoples.py:273`, `make_water_worlds.py:130`,
  `make_nutrition_runs.py:127`); 103 of 108 reaches get exactly 35.2 whatever their length (correlation with length -0.07). The
  wild layer's fish in the same water is 200 to 500 times the people's stock, linked one way ([[L-116 The wild layer's fish and a water body, two ways|L-116]]).
- **Runs on set nights in every live world** (`runs_set_nights`, [[D2-231 The runs world's runs on set nights|D2-231]]): fixed dates. On the weather cue, timing is a probability
  under rain alone inside fixed windows: the eels have no run in 54% of years (437 of 810 village-years), the lampreys come more
  than half on the window's forced last day in 34%, the salmon's size never varies. The cue's mean rain is fixed at 3.4 (runs.py)
  while the engine's weather is set by the seed, and the generator's rain (393 to 4,164 mm here) is never read. Windows are absolute
  days of an 8-day season, wrong for worlds of 6 or 10.
- **The lamprey dies out on long rivers at world build:** the history's end clears the pulses in flight (`engine/wild.py:111-112`)
  and an up-run returns only from its own spawners; the run reaches 40 of 167 villages (all 167 with spawners reseeded), and is
  sized by the head-water stretches only (23 a year at Eelmouth).
- **Spring and summer are the gap on every river** (sweep: medians, share of a season's need: big river 0.2 / 0.2 / 0.9 / 1.0,
  lowland river 0.2 / 0.2 / 0.5 / 0.4, spring / summer / autumn / winter); the longest stretch with no run meal is 12 to 23
  nights. River km above the village moves the year's food most (elasticity 1.09).
- **One kind of fish everywhere** (one `fish` stock, `waters.SHARED`; one shallows stock); the three run kinds differ only by
  `where`. A new up-run is mostly data; a new cue, elvers (recruited from the sea), coarse fish spawning in place and a second
  resident kind need code. The river's signs name the three kinds in code (`river.py:193-253`), so a new run would be fished and
  never seen.
- **Water food runs on two clocks:** the runs, the lake stock and the harvests compressed x32/365; the shallows uncompressed (a real
  year's production in 32 nights, about 11.4 times richer a night); the makers' resident fish at r 0.3 a night.
- **Water where villages cannot reach it:** 59 of 167 villages on a running river have no parcel the run can reach; a home
  village never gets a brook parcel (`settle.py:328`); fens are not water bodies; the sea has no body, stock or tide.

## The proposal

0. **The river's size carried from the land to the world** (found 24 Nov, Zach: "why is every river the same?"): the generator computes each cell's rain-weighted area drained (`landgen/physical.py:305-311`), its three river classes (15, 45 and 150 km2, `vocab.py:24-27`), floodplains and channel depth growing with the root of the area; the writer keeps only a word, "river" or "brook" (`landgen/write.py:84`), the wild layer fixes every channel at 0.12 or 0.6 of a 150 m cell (18 m or 90 m, `wild/ecology.py:48-53`), and a village takes at most two water cells (`settle.py:335`). Carry each water parcel's and body's area drained, discharge, width (by hydraulic geometry, width growing with the root of discharge), depth and slope into the world, and derive from them every water quantity: area, ecosystem zone, resident fish, the shallows' margin, the weir's share, the flow's answer to rain, a run's reach. Everything below reads these.
1. **One clock for the water's food** ([[D2-273 Three clocks, each system on one|D2-273]] already decides it; [[Q-98 One clock for the water's food before anything is sized|Q-98]] answered): the runs' clock (x32/365, [[D2-259 The food values are anchored on real values|D2-259]]'s compression), and [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter
   reached through one named lever written beside the data (`WATER_RICHNESS`, about 3 to 13 times real productivity by the
   sweep's experiment d), so the fitting is in one visible place instead of three makers.
2. **Resident fish seeded by the engine from the land** at world build: each body's area by the engine's water widths, times
   productivity by water kind (river, big river, lake, fen water; sources in sweep.md §5d) and warmth, a low r on the year clock;
   the makers' rules retired (a maker may scale, never stock). Fens become water bodies; the wild layer's fish tied to the body
   ([[L-116 The wild layer's fish and a water body, two ways|L-116]]).
3. **The lamprey's two faults fixed:** the up-runs' pulses kept at the history's end (or the spawning stretches reseeded), and
   `spawn: river`.
4. **Run timing on conditions:** a nightly chance in broad seasons (windows as shares of the season) that rises with rising water
   and water temperature (taken from recent air temperature), never a forced last-day dump; the cue read against each world's own
   weather, one cue function shared by the runs and the signs, an unknown cue key an error; set nights retired ([[D2-231 The runs world's runs on set nights|D2-231]] replaced).
   On the sweep's copies (experiment b): years with no eel run fall from 437 to 20 of 810, no year comes all on one night, the
   spread across years stays about 3 nights.
5. **The spring river:** a spring share of the salmon run on salmon rivers (25 to 50 food a spring on the copies, no new kind); coarse
   fish spawning as a spring rise in what the shallows and margins yield (not a new fish); the lamprey as fixed in 3.
6. **Signs and lore from the rows:** the river's signs by direction and kind, each run's own window, the fisher's lore read from the
   land (FI6 and FI7 read fields nothing writes, `founders.py:331-334`).
7. **Water where the land has it:** every village on a running river gets a parcel the run can reach; home villages may take
   brooks and lake shores; shallows and a parcel's share of the body by margin.

**Later, after live run 2** (the finer additions): shad, sea trout and elvers as rows (on the copies each adds 1 to 21 food a year,
none closes a spring gap alone); a second resident kind and fish by water kind; the sea and estuary as bodies with tides; the
cue's mean from climate from the land ([[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]); dry-year and flood effects on the stocks ([[L-150 Environmental effects on fishing refined after the rest works|L-150]]); weirs sized by river width, beaver
dams as partial barriers.

## Why

[[D2-347 A water-only village should be able to last the year|D2-347]] and [[D2-348 A water-only village is made able to last the year by|D2-348]] ask for a spring river and resident fish that matter; built as constants on Eelmouth they would be the fourth
fitted rule. Built from the land, every generated world (Hollinford first) gets waters that follow its rivers, and the fitting
sits in one lever Zach can see.

## Alternatives considered

- **Tune the makers and move the lamprey's set nights into spring** (the sweep's minimum for live run 2): fast, and keeps the fit.
- **Real productivity with no lever:** resident fish 3 to 13 times below [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter on the runs' clock; the quarter would not
  hold.
- **The shallows' clock for everything:** the water 11 times richer than the land's harvests.

## Open questions

1. The clock ([[Q-98 One clock for the water's food before anything is sized|Q-98]]).
2. Whether all of 1 to 7 come before live run 2, or 1 to 5 before and 6 and 7 with the later list.

## Affects

`engine/waters.py`, `engine/wild.py` (history's end, the runs' night), `wild/runs.py`, `wild/kinds.py` (RUNS), `wild/river.py`,
`wild/water.py` (shallows), `landgen/settle.py` (village water), `engine/founders.py` (FI6, FI7), the three makers; u1_water.md.

## History

- **24 Nov 2026:** item 0 added: the land's river size is lost at the land-to-world write and replaced by fixed widths and two words; carried through, it is what makes every later item general.

- **24 Nov 2026:** 37.2's ecosystems and calibration (docs/review/37_growth/02zzzl_waters_calib/c_ecosystems/ecosystems.md): the clock is already decided ([[D2-273 Three clocks, each system on one|D2-273]]: all food on the year clock, real quantities x 32/365); the shallows' rates were u1's misreading (a real year in 32 nights, 11.4 times too rich) and come onto it; resident fish by ecosystem from the land (a Huet-style zonation, nine ecosystems); [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter needs a lever of median 2.8 over real productivity; water-only worlds only on big run rivers or meres; fens as water bodies.

- **24 Nov 2026:** written by 37.2 from the sweep and the generality read ([[W-108 The waters calibrated across many generated environments|W-108]]), at Zach's ask for a calibration across generated
  waterways and a read of how general the system is (23 Nov).

## Sources

docs/review/37_growth/02zzzl_waters_calib/brief.md, sweep.md, generality.md, a_sweep/data/*.tsv; spring_gap.md.
