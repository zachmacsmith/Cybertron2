---
id: docs/review/37_growth/02zzzl_waters_calib/sweep.md
kind: note
updated: "2026-11-24"
---
# The waters swept across 51 generated environments (W-108, agent A)

*note · `docs/review/37_growth/02zzzl_waters_calib/sweep.md`*


Session 37.2, 23 to 24 Nov 2026, from brief.md sections 1 to 5. No model calls, no live runs, no engine change: the worlds are the land
generator's, the runs are the engine's own `wild/runs.py` stepped by the wild layer's night loop with no people, and every
experiment runs on copies of the data. Every number below comes from a script in `a_sweep/` run on 24 Nov; the data files named
beside each table hold it.

**The short answer to Zach's questions.**

- **The runs are probabilities under one condition, rain, inside fixed windows, but only in a world without `runs_set_nights`; every
  live world (the runs worlds, all four Eelmouth files) runs on set nights, and there the timing is a fixed date to the night.** On the
  cue, a run's start varies by a few nights a year (the first big night's spread across years: 1.2 nights for the eels, 3.9 for the
  salmon, 2.5 for the lampreys), the eels fail outright in 54% of village-years, a sixth of the salmon years and a third to two fifths of the lamprey years come mostly on the window's forced last day, and the salmon's size never changes from year to year (Beverton-Holt
  at its settled level with nothing taken). The cue reads one fixed mean rain (3.4 mm) and the engine's weather does not follow the
  generator's climate at all: a 500 mm world and a 1,400 mm world on the same seed get the same rain.
- **Resident fish are not in the generator.** As generated, 0 of 109 water bodies at villages hold any. With today's maker rule a
  river reach holds 35.2 fish units whatever its length (3.75 to 10.2 km), about 1.3 food a night at best (12% of a village of ten),
  and 59 of 167 villages on a river that runs hold no parcel that can reach a run at all. The food web holds its own fish in
  the same water, 200 to 500 times the people's stock, unconnected ([[L-116 The wild layer's fish and a water body, two ways|L-116]]).
- **There is one kind of resident fish everywhere** (`fish`), one kind of shallows creature, three run kinds told apart only by
  `where` (salmon on the 139 of 167 village stretches whose way to the sea holds big river; eels and lampreys on any river). The
  generator makes 119 lakes and puts a village on none of them; no village has a brook or a pool, so two of the six shallows types
  are never reached.
- **The water's food is set by how much river lies above the village** (elasticity 1.09: from 30 food a year at a head water to
  1,369 at the lowest big river), then by whether it is a salmon river, then by a dam below (the salmon above a shut mill fall to a
  fifth in five years); climate does not change it through the weather, only through the river sizes the land makes. Spring and summer carry about a fifth of need on a big or lowland river (mostly the maker's resident fish at their best, and late
  salmon at the upper villages), nearly nothing at a fen-only village; the longest run of nights with no run meal is 12 to 23.
- **At a real river's size, on the compression the runs already use, no extra run closes the spring gap at a typical village**
  (twaite shad, where they reach, about 6 food a spring at the median; elvers 1.5; lampreys sized as real 0.2), and real resident
  productivity gives 0.2 to 1.0 food a night: [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter of need is 3 to 10 times real productivity on that clock, and about
  real productivity on the year clock the shallows were calibrated on. The two clocks disagree by 365/32; that is the first thing to
  settle.

## 1. Method and the worlds

**Scripts** (all in `a_sweep/`; the world files are remade exactly from `data/worlds_index.json`'s specs and are not in git):

| Script | Does | Writes |
|---|---|---|
| `make_worlds.py --jobs 4` | 51 worlds by `landgen.write.generate`, no people, packs `wild` and `water`, climate `steady` | `worlds/*.yaml` (not in git), `data/worlds_index.json` |
| `sweep_world.py all --years 6` | per world: the census (resident fish three ways, shallows, the food web's fish) and the runs over six years, four arms | `data/worlds/*.json` (not in git) |
| `experiments_rows.py` | section 5 (a): RUNS rows changed as data, through the engine's `runs.advance` | `data/exp_rows/*.json` (not in git) |
| `analyse.py` | sections 1 to 4: the tables | `data/summary.json`, `worlds.tsv`, `villages.tsv`, `food.tsv` |
| `experiments.py` | section 5 (b) to (d) | `data/experiments_summary.json` |

**The run loop** (`sweep_world.runs`) is the engine's night with no people, in its order: `EC.step` (the food web), the ice at each
village's first river parcel (`water.ice`, as `stretch_ice`), `RU.advance` with tonight's and tomorrow's weather (`WL.weather`, the
climate scheduler), the dams' stops and the cue on or on set nights. What passed a village is counted as the engine's own tally
counts it (a pulse at its stretch on its day, once; held under ice until the night it moves on), before any take. Each start is
recorded with its cause (the cue, the window's last day, a set night) from the state's own quota and due. Four arms per world:
**cue** (as a generated world runs), **set** (`weather=False`, as every live world runs), **fix** (the cue, with the up-runs'
spawning stretches that the build left empty reseeded: section 7, bug 1) and **dam** (the laid worlds' generated mill, shut, stop 0.5).
The harness reproduces live run 1: Eelmouth on set nights gives 1,682 eels, 680 salmon and 23 lampreys in its first year (the live
run's 1,607, 662 and 23 before takes).

**The worlds** (`data/worlds.tsv`; 51 made, 3 refused):

| Family | Configurations (landgen/vocab.py CONFIGS) and settings | Seeds | Worlds |
|---|---|---|---|
| cal | the calibration suite's twelve (make_calibration_worlds.WORLDS: plain lowland 900 mm; dry east 500 mm, east wind; wet west coast 1,400; coast under mountains 1,200; upland and moor 950; high mountains (moor raised to 900 m, a summit) 1,100; cold north 6 C; fen with islands 600; estuary and fens 750; scarp and vale 800; sand country 650; lake country (upland with a laid mere) 1,400), three generator-placed villages each | 1, 2, 3 (fen: 4 for 3, refused "laid rivers run where laid") | 36 |
| cfg | the other configurations with rivers: confluence plain, river through a range, basin in a ring of hills, two valleys over a pass, gated valley, watershed divide, settled lowland and frontier; 900 mm | 1 | 7 |
| laid | make_water_worlds' river land (a laid river from northern fells to the southern edge, wild upland above), villages pinned high (0.74), middle (0.5, with the mill site) and low (0.26) on it: large at seeds 5 and 7, large dry (500 mm, 10 C) and wet (1,400 mm), medium and plain river at seed 5 | 5, 7 (medium s7 and plain-river dry s7 refused: no site for the mill pin 11 km from the others) | 6 |
| lake | make_water_worlds' lake world (Meresby on a laid mere) | 3 | 1 |
| Eelmouth | `specs/nutrition/eelmouth.yaml` as it stands (its own stocking, `runs_set_nights`) | 5 | 1 |

They hold 175 settled villages, 167 of them on a river a kind runs (plus 121 wild places, reported apart), with 0.6 to 153 km of river above them; 32 villages on big river, 76 on a lowland river, 40 whose only water is fen, 18 on a
river stretch with no water parcel, 1 on a lake, 8 on no river.

**What the generator cannot make** (findings): a village on a lake, except by a hand-laid mere and a pin (119 lake bodies made, one
with a village's parcel: Meresby); a village's brook or pool (no water body of kind `brook` or `pool` at any village: the water
parcels are always on a reach); a tidal estuary the runs know (a mouth is the window's edge or the sea alike; `estuary and fens`
makes the saltmarsh, but no run or stock reads tide); a dam except the mill site pin (no weir or beaver dam in a generated world
without people); a dry year's river (section 3: the engine's rain does not follow the generator's climate).

## 2. Resident fish and shallows

**Where the values come from** (`data/summary.json`, `villages.tsv`):

| Stock | As generated | Comes from |
|---|---|---|
| resident fish (`fish`, one a water body, [[D2-229 One fish stock per water body|D2-229]]) | **none**: 0 of the 109 bodies at villages hold fish (the one exception is Eelmouth's own file) | the makers only: make_water_worlds.water_stocks / make_peoples (K 8 x 2.2 = 17.6 a unit of size, r 0.3, `periodic`, so `fast` out of a run); a mere by its area (16,500 a km2, LAKE_TURNOVER 0.4, `threshold`); make_nutrition_runs' 0.25 of it for water-only worlds (Eelmouth's K 8.8) |
| shallows ([[D2-317 The shallows are one stock per parcel, distinct from the resident…|D2-317]]) | every water and fen parcel, K by water type x size (wild/water.py SHALLOWS) | the engine, at the world's making (`seed_shallows`) |
| the food web's fish | every area, kg a km2 by its water share (ecology.py: small streams 0.12 of a cell wide, the large river's channel 0.6, lakes by area; cap 40,000 x SCALE 1.21 kg a km2 of water) | the engine's land summary: the only stock the generator's physics sizes |

**By water kind and size, today's maker rule applied** (medians over villages; food a night at best = the renewal rule's most for
good, x 0.46 food a unit):

| Water at the village | Villages | River km (home and ring) | Resident fish K (units) | Food a night at best | Shallows K | Shallows, summer / winter | The food web's fish (kg) | Resident + shallows, share of 11 |
|---|---|---|---|---|---|---|---|---|
| big river | 32 | 6.6 | 35.2 | 1.30 | 4 a parcel | 0.40 / 0.04 | 19,005 | about 0.16 |
| lowland river | 76 | 6.5 | 35.2 | 1.30 | 8 a parcel | 0.47 / 0.05 | 7,886 | about 0.16 |
| fen only | 40 | 5.2 | 0 | 0 | 21 a parcel | 0.34 / 0.03 | 4,981 | 0.03 |
| river, no water parcel | 18 | 3.0 | 0 | 0 | 0 | 0 | 2,621 | 0 |
| lake (Meresby) | 1 | 2.3 | 21,179 | 10.67 | 2 a parcel | 0.40 / 0.04 | 64,224 | 1.0 |

- **K does not follow the water's size.** Of the 108 reaches at villages 103 hold exactly 35.2 (two units of water parcel); river km
  against K correlates at -0.07. A 10 km reach and a 4 km reach are the same stock; a big river's (by [[D2-229 One fish stock per water body|D2-229]], its reach) the same as
  a lowland river's. Only the lake's follows its area. The maker counts the village's water parcels, not the water.
- **Against [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter (2.75 food a night)**: resident fish and shallows together, at their best in summer, are a median 16%
  of a village of ten; 2 of 175 villages pass a quarter: Meresby on its mere, and Cragton (lake country, seed 3), whose reach parcel the maker stocked as a mere (K 24,874) because its village land holds lake (section 7, bug 10); Eelmouth's are 0.32 + 0.40 food a night (7%).
- **The shallows** are 0.03 to 0.47 food a night at a village in summer and a tenth of that in winter: a median 4% of need. By type
  (per parcel, `parcels_by_type_*`): river 8 (4 a unit), big river 4 (2 a unit), fen 21 (7 a unit), lake 2; brook (5) and pool (4)
  never occur.
- **Different fish in different places?** Today, no: one `fish` stock everywhere, one shallows stock, and the run kinds differ only by
  `where` (salmon: a river whose way to the sea holds big river; eels, lampreys: any river) and by window. What the data could hold
  without code: more run kinds (a `RUNS` row and a `KINDS` row each, `mover: run`); a stock's own renewal and parameters on its
  record (renewal.py: "an ecosystem decides how its own fish come back"). What needs code: several resident stocks on a body
  (waters.SHARED is the one key `fish`; the takes draw `fish`), per-kind shallows, and a water kind (chalk stream, mere, fen dyke,
  tidal reach) that the generator writes and the stocks read.

## 3. The runs: timing over six years on every world

`data/summary.json` `arms`, `cue_per_world`; settled villages only; a run year starts on its window's first day; "first night" is the
first night a tenth of the year's run passes, counted from the window's opening.

| Measure | Eel (down, autumn 0-7, `rain_after_dry` 2) | Salmon (up, autumn and winter 0-3, `spate` 1.2) | Lamprey (up, spring, `spate` 1.0) |
|---|---|---|---|
| Village stretches it reaches | 162 of 167 | 139 of 167 | **40 of 167** as built; 167 with the fix |
| Village-years with no run (cue) | **437 of 810 (54%)**, and 5 villages never in five years | 0 of 695 | 8 of 200 |
| All on one night (90% or more) | 187 | 81 | 57 (fix: 295 of 835) |
| More than half from the window's forced last day | (none: a down-run has no last day) | 109 of 695 (16%) | 67 of 200 (fix: 324 of 835, 39%) |
| First night: p10, median, p90 | 0, 3, 5 | 3, 7, 15 | 2, 5, 10 |
| First night's spread across years (sd, median village) | 1.2 nights | 3.9 | 2.7 |
| Heads' variation across years (cv, median village) | 1.23 | **0.00** | 0.20 |
| **On set nights** (the live worlds) | night 1, every year, sd 0, never fails | night 2 to 10 by the lag, sd 0 | night 2 to 9, sd 0 |

**How often the cue fires** (`cue_per_world`): an eel cue on 5% to 7% of window nights at a village's own stretch (0.2 to 0.7 cue
nights a window); a salmon spate on 25% of window nights at the mouth (2.0 to 3.8 a window, a year with none in 0% to 33% of
window-years); a lamprey spate on 23% (0.4 to 3.7 a window, none in 3% to 56%). P(no eel cue in an 8-night window) at 6% a night is
0.61: the measured 54%.

**What the timing varies with:**
- **Rain, and nothing else.** The cue is the catchment's rain against the fixed `RAIN_MEAN` 3.4. The engine's rain at the villages'
  catchments averages 0.60 to 0.69 of it on every seed-1 world, 0.94 to 1.00 on seed 2 and 1.05 to 1.10 on seed 3, **whatever the
  generator's rain_mm** (the 500 mm and 1,400 mm laid worlds: 0.95 and 0.97; dry east and wet west on seed 1: 0.64 and 0.65). The
  generator's node `rain_mm` (393 to 4,164 mm in these worlds) is never read by the weather. So the seed decides the cue: drier
  seed-1 weather gives more eel cues (42% of window-years with none, against 63% to 69% on seeds 2 and 3: rain after dry days needs dry
  days) and fewer spates (lampreys none in 47%, against 19% to 31%).
- **The village's place on the river**, for the up-runs only, by the lag from the mouth: the salmon's first big night is a median 4
  at 2 or fewer stretches from the mouth, 6 at 3 to 5, 10 at 6 or more. The eels' is 2.5 to 3 anywhere.
- **The spawners**, never: with nothing taken the salmon and the lampreys return at Beverton-Holt's settled level every year (cv 0
  for the salmon). A year's size varies only for the eels, by whether the cue fires (cv 1.2), and below a dam (cv 0.4).
- **Temperature, flow as a level, the season's warmth, the moon**: not read.

**So: a probability under one condition inside a fixed window, with a forced remainder for the up-runs.** On set nights, a fixed
date. Neither is the "probabilities with different conditions" Zach asked for: the eels' condition fails half the years; the
salmon's fires so often that it is close to a date (first night sd 3.9 of a 12-night window, then a forced rest).

## 4. Food passing in a year

`data/food.tsv` (fix arm; as built is within 1% except the lampreys); runs by kind passing, before any take; resident fish (maker) and
shallows at their best for good; need 88 a season (96 in winter); medians over villages.

| Water | Villages | A year's food passing | Runs | Resident | Shallows | Spring / summer / autumn / winter, share of need | Longest nights with no run meal |
|---|---|---|---|---|---|---|---|
| big river | 32 | 238 | 196 | 34 | 7 | 0.2 / 0.2 / 0.9 / 1.0 | 14.5 |
| lowland river | 76 | 127 | 84 | 34 | 9 | 0.2 / 0.2 / 0.5 / 0.4 | 16 |
| fen only | 40 | 71 | 65 (out of reach) | 0 | 6 | 0.0 / 0.1 / 0.3 / 0.2 | 16 |
| river, no water parcel | 18 | 42 | 42 (out of reach) | 0 | 0 | 0.0 / 0.0 / 0.1 / 0.2 | 16.5 |
| lake (Meresby) | 1 | 353 | 68 | 277 | 7 | 1.0 / 1.0 / 1.6 / 0.3 | 21 |
| Eelmouth (on the cue) | 1 | 1,218 | 1,203 | 8 | 7 | 0.07 / 0.09 / 8.1 / 5.1 | 12 |

**The gap is spring and summer everywhere on a river**: about a fifth of need passes on a big or lowland river, and most of it is the
maker's resident fish at their best (34 a year, 8.6 a season) with late salmon at the upper villages and a few lampreys; a fen-only or
parcel-less village passes a twentieth or less that it can reach. Eelmouth passes 3.4 times the year's need on the cue (4.0 times, 1,424, on its own set nights), all of it in autumn and winter; its spring and summer pass 6.0 and 8.3 food of 88 (5.7 and 6.7 on set nights).

**What changes the total most** (the fix arm's runs food a year, by setting):

| Setting | Effect |
|---|---|
| River above the village | 0-5 km: 30; 5-10: 70; 10-20: 126; 20-40: 280; 40-80: 757; 80 and more: 1,369 (34 to 7 villages a bin); elasticity 1.09 |
| A salmon river | 90 against 14 |
| The village's place | the stretch from the mouth matters through the river above it; at a given size, little |
| A dam below (laid worlds, the mill shut) | the salmon above it fall each year: Highpool 120 to 23 heads in five years, Middleham 224 to 75, Lowstrand 843 to 694; the eels unchanged |
| Climate (rain_mm) | none through the cue; through the land only: the dry and wet laid worlds' land makes different big rivers (Middleham's salmon 458 dry, 224 default, 239 wet) |
| Set nights against the cue | the eels 87 food an autumn against 30 (the cue fails half the years) |
| The seed | 63 to 85 at the median village by seed in the calibration worlds |

## 5. Experiments (on copies, never in the engine)

### (a) The runs' rows changed as data, through the engine (`experiments_rows.py`; fix arm as the base; 835 village-years)

| Variant | Eel years with no run | Eel food an autumn / winter | Other effect |
|---|---|---|---|
| base | 437 of 810 | 29.9 / 5.1 | |
| eel cue: 1 dry day | 341 | 38.9 / 12.0 | |
| eel cue: a spate of 1.2 | **167** | **73.0 / 13.4** | first night median 1, one-night years 49 |
| eel window into winter | 356 | 29.2 / 15.1 | |
| lampreys spawn along the river (no reseed) | | | lamprey years with no run 0; lamprey food a spring 4.5, a summer 7.7 (was 1.2, 2.9) |
| set nights | 0 | 86.9 / 9.6 | every date fixed |

The `spawn: river` row alone fixes the lamprey's extinction at long rivers (section 7, bug 1) and triples its food; it is still a mean of 4.5 food a spring.

### (b) Timing drawn from conditions (`experiments.py` HAZARD; each village's own rain and temperature)

Each night a share of what is still to run goes, by the conditions: eels in late summer to early winter, 0.45 on a rise of water
(rain 1.5 x the mean) with the water at 14 C or under, 0.06 on other cool nights; salmon late summer to winter, 0.35 on a fresh, 0.04
otherwise; lampreys spring into early summer, 0.35 above 8 C on a rise, 0.10 above 8 C. Water temperature is the air's over five
nights (a presentation choice).

| Measure | Eel | Salmon | Lamprey |
|---|---|---|---|
| Years with no night of a head or more | 20 of 810 (today 437) | 0 | 6 of 835 |
| Years with under half the run gone | 154 | 0 | 0 |
| All on one night | 0 (today 187) | 0 (today 81) | 46 (today 295) |
| First night: p10, median, p90 | 0, 6, 11 (today 0, 3, 5) | 0, 2, 9 | 3, 5, 11 |
| First night's spread across years (sd) | 3.2 (today 1.2) | 3.2 | 2.8 |
| Nights it runs, median | 8 | 10 | 6 |
| On the season's forced last night (up-runs) | | 10% | 31% |

A nightly chance under conditions keeps the year-to-year variety (a spread of about three nights) while almost never failing or
coming all at once, which is what a run should do; it also puts the run where the conditions put it (the lampreys wait for warm
water: a cold spring delays them). The moon is left out: under the year clock a lunar month is under three world nights.

### (c) Other runs of a temperate lowland river, at a real river's size (x 32/365 as [[D2-259 The food values are anchored on real values|D2-259]]; by each village's catchment)

| Run | Season | Real size (source) | Villages | Food a year, median (lo to hi) | Spring, median |
|---|---|---|---|---|---|
| twaite shad | late spring, early summer | Severn: "hundreds of thousands" before the weirs, 7,000 to 14,000 past Tewkesbury 2017-18 (Unlocking the Severn, Environment Agency): 10 to 30 a km2, 0.45 kg (est.) | 94 (salmon rivers, lower stretches) | 6.9 to 20.6 (max 302) | 5.9 |
| sea trout | summer | est. 5 to 20 a km2, 1.5 kg (the Tywi and Teifi named, not checked) | 167 | 3.2 to 12.6 (max 671) | 0 |
| elvers and glass eels | spring | Severn: about 40 t a year caught in the late 1970s, 10 t now (Cefas); the run 25 t (2020) to 76 t (2023) (glasseel.com); 1 to 4 kg a km2 | 120 | 0.6 to 2.4 (max 127) | 1.5 |
| smelt | late winter, early spring | est. 0.5 to 2 kg a km2, tidal reaches only | 6 | 1.1 to 4.5 | 1.2 |
| river lamprey, sized as real | winter into spring | est. 5 to 20 a km2, 0.06 kg (the Ouse fishery named: Masters et al. 2006; no run size found) | 167 | 0.2 to 0.7 (max 38) | 0.2 |
| sea lamprey | late spring | est. 0.2 to 1 a km2, 1 kg | 139 | 0.1 to 0.4 | 0.1 |
| spring salmon | late winter, spring | est. a fifth to two fifths of the salmon (the Tay's, the Dee's spring runs) | 139 | moves 25 to 50 of today's 126 an autumn and winter (a mean over village-years) into spring | 25 to 50 |
| coarse fish spawning in the shallows | spring (pike late winter; perch, roach spring; bream, tench early summer) | a share of the resident stock's year moved into the margins, not more fish | all | from (d): 0.2 to 0.4 food a night, 0.4 of the year's take in spring (est.) | 3 to 5 |

The check of today's sizes against the same rule (catchment heads a world year): eels 1.18 a km2 against Burrishoole's 1.75 to 4.38
(below: the cue fails half the years); salmon 1.03 against a real river's 0.44 to 1.75 (inside); lampreys 0.98 (fix arm).

**At real sizes no added run closes the spring gap at a typical village**: a village both reach gains about 7 food of a spring's 88 (shad and elvers, at the median), a big low village up to a few hundred. Spring salmon moved from the autumn would close more than any other on a
salmon river, and it is the one run here that needs no new kind (a second window on the salmon's row, a share).

### (d) Resident stocks from real productivity (`experiments.py` PRODUCTIVITY; the engine's own water widths)

Production of whole fish (kg a hectare a year): brook 20 to 170 (u1 section 2's stream studies), lowland river 50 to 100 (the River
Eden, Kent: chub 54 and dace 17 kg a ha a year, 191 and 43 kg a ha standing; Welcomme 1985, FAO 262: floodplain rivers' catch 5 to
143), big river 30 to 80 (est.), lake 20 to 100 (Downing and Plante 1993, 100 populations in 38 lakes), fen water 30 to 100 (est.);
half the production taken for good (est.); 0.53 fish units a kg of whole fish.

| Water | Villages | Maker (today), food a night | Real, x 32/365 (the runs' and harvests' clock) | Real, a real year in 32 nights (the shallows' clock, u1 section 2) | K units, real / maker |
|---|---|---|---|---|---|
| big river | 32 | 1.30 | 0.41 to 1.03 | 4.6 to 11.7 | 3,102 / 35 |
| lowland river | 76 | 1.30 | 0.21 to 0.42 | 2.3 to 4.7 | 1,317 / 35 |
| fen only | 40 | 0 | 0.17 to 0.35 | 1.9 to 3.9 | 1,088 / 0 |
| river, no water parcel | 18 | 0 | 0.12 to 0.24 | 1.4 to 2.7 | 759 / 0 |
| lake (a 38 km2 mere) | 1 | 10.67 | 25 to 127 | 290 to 1,448 | 352,557 / 21,179 |

[[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter (2.75 a night) is **3 to 13 times real productivity on the runs' clock** and about real productivity on the
shallows' clock; today's maker values sit between the two. The real stocks' standing K is 35 to 90 times the maker's at a much lower
r (about 0.002 a night for the compressed mid, against 0.3), which is the shape a resident stock should have: hard to fish out, slow to
produce. Today's small K at r 0.3 strips in a night or two and regrows in a week (spring_gap.md: Eelmouth's reach fished out in two days).

## 6. What changed most, and how general the waters are (from the sweep; B's generality.md is the code read)

- **General and working**: the river net from any generated land (all 51 built, none crashed), the lag, the ice, the dam's hold,
  the shallows by water type, the eels' stock-based run, the salmon's spawning along the river.
- **General in form, fitted in constants**: the cues (`RAIN_MEAN` 3.4 fixed; `spate` 1.0 and 1.2 and `rain_after_dry` 2 tuned so the
  runs fire "1 to 3 nights a year in the steady climate", [[D2-231 The runs world's runs on set nights|D2-231]]), the sizes (`cap_km`, `seed_km`, the eel's b 3.0 and `year` 0.6, sized
  on the runs and river worlds, [[D2-258 The food values are put on one physical basis|D2-258]]), the shallows' K (u1's estimates).
- **Fitted to the makers**: resident fish (none without a maker; K by parcel count), the lake's stock (by the village's own lake
  km2), the set nights every live world runs on.
- **Missing**: resident fish from the land; several fish kinds; any run but three; temperature, flow level or season's warmth as a
  condition; a climate the weather follows; a village on a lake, a brook or a pool from the generator.

## 7. What the sweep found broken

1. **The lampreys die out on every long river at the world's build, and never come back.** `wild.seed` ends the ten-year history by
   clearing the pulses in flight (`st["runs"]["pulses"] = []`, engine/wild.py:112) on the run's first day, which is in summer for
   every world here; the lampreys bound for head waters more than a few days up are still travelling, so those heads hold no spawners,
   and an up-run returns only from its own spawners (Beverton-Holt from 0 is 0; no straying). As built, the lampreys reach 40 of 167
   village stretches; reseeded, all 167. The salmon escape it only because their window (autumn) is empty at a summer start; a world
   starting in autumn or winter would lose them the same way.
2. **The lamprey's run is sized by its head-water stretches only** (`spawn` unset: `heads`), so a 100 km river's lampreys are those of
   its last 1 to 2 km of head water: 23 a year at Eelmouth, 11 to 13 at Middleham. `spawn: river` (as the salmon) gives 270 to 330 at
   Middleham.
3. **The eel cue fails half the years**: 437 of 810 village-years with no silver eel run, though the eels are there (they stay in the
   stock); with set nights the same villages get 2.9 times the autumn food. A real eel run varies, but does not fail one year in two.
4. **The weather does not follow the generator's climate** (engine rain at the villages 0.62 to 1.10 of `RAIN_MEAN` by seed, not by
   rain_mm), so a dry world's rivers spate as often as a wet world's, and `RAIN_MEAN` is not each world's mean (seed-1 worlds run at
   0.64 of it). Known for the weather (02zzt, OPEN [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]); here it means the runs' cue is not a condition of the world's climate.
5. **Resident fish: zero without a maker, and the maker's K ignores the water's size** (103 of 108 reaches at exactly 35.2).
6. **59 of 167 villages on a running river cannot reach the run**: no water parcel on the river (18), only fen with no river parcel beside it (40), or a lake's water (Meresby), so `run_reach` is 0 on every parcel. The run passes the village and is counted in its record and signs.
7. **The salmon never vary in size** with nothing taken (cv 0 across years at every village): the run's year-to-year variety is all
   in its timing.
8. **Two clocks for the water's food**: the runs ([[D2-259 The food values are anchored on real values|D2-259]]), the lake's turnover and the harvests put a real year's amount into the
   32-day year (x 32/365, so a night's food is a real night's); the shallows (u1 section 2) put a real year's production into the
   32 nights uncompressed (a real night's x 11.4); the maker's river fish run at r 0.3 a night where a real stock's production on the runs' clock gives about 0.002. They cannot all be right against one need a night.
9. **Three seeds refused**: fen s3 ("laid rivers run where laid"); the laid medium river at seed 7 and the plain river at seed 7
   (no site for the mill pin 11 km from the others).
10. **The maker stocks a mere by the village's lake land, not by the parcel's body**: make_water_worlds.water_stocks gives the
    village's largest water parcel the mere's stock when its home and ring hold 0.5 km2 of lake, though the parcel is on a reach
    (Cragton, lake country seed 3: a reach of K 24,874).

## 8. What the sweep recommends for stage 5b part 4 (the water's year)

In order; each is general (data from the land), not Eelmouth's:

1. **Fix the two lamprey faults first** (bugs 1, 2): keep the up-runs' pulses in flight at the history's end (or reseed the
   spawning stretches at the run's start, as the fix arm does), and give the lamprey `spawn: river`. Without this the spring lamprey
   run [[D2-348 A water-only village is made able to last the year by|D2-348]] asks for exists at 40 of 167 villages and is 23 heads at Eelmouth.
2. **Settle the clock for resident fish and shallows before sizing them** (bug 8; an ask for Zach): on the runs' clock, real
   productivity gives a river village 2% to 9% of need, and [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter needs a named lever of 3 to 13 ([[D2-259 The food values are anchored on real values|D2-259]]'s way); on the
   shallows' clock real productivity gives about a quarter already and a big river more. The sweep's recommendation: one clock for
   all the water's food, the runs' (x 32/365), with the quarter reached by a named lever written beside the data.
3. **Resident fish from the land, in the engine, not the makers** (bug 5): K from the water's area by the engine's own widths and a
   productivity by water kind (PRODUCTIVITY), at a low r, for every body including the wild reaches; the makers' rules retired. The
   lake's stock by the whole lake ([[D2-229 One fish stock per water body|D2-229]] already says so).
4. **Spring on the river by conditions, not dates**: run the up-runs and the eels on a nightly chance under conditions (section 5 b)
   in broad seasons: water temperature from the air's recent nights, the rise of water against the world's own mean rain. For live
   run 2, where `runs_set_nights` may stay, at least move the lamprey window's set nights onto the spring gap and add a spring share
   to the salmon (spring salmon: the largest spring food on a salmon river that needs no new kind).
5. **Coarse fish spawning in the shallows in spring** as a seasonal raise of the shallows' and the margin's catchable stock (a
   share of the resident stock's year moved into spring), not as new fish; with resident stocks from the land it gives a spring
   lift everywhere there is water, including fen and lake villages, where no run reaches.
6. **Then the other runs as data rows**, in the order of what they add where they reach: shad (lower big rivers), sea trout
   (summer, any river), elvers (spring, near the mouth); smelt only with tides. Each is a RUNS and KINDS row (the mechanism is
   general); a new cue kind (temperature) needs code.
7. **Give every village on a running river a water parcel the run reaches** (bug 6), or make a fen beside the river reach it, in the
   generator.
8. **The cue's mean from each world's own weather** (bug 4) once climate from the land ([[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]) is built; until then the cue is the
   seed's, not the world's.

Current as of 24 Nov 2026.
