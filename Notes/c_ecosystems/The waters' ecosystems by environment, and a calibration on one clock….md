---
id: docs/review/37_growth/02zzzl_waters_calib/c_ecosystems/ecosystems.md
kind: note
updated: "2026-11-24"
---
# The waters' ecosystems by environment, and a calibration on one clock (W-108)

*note · `docs/review/37_growth/02zzzl_waters_calib/c_ecosystems/ecosystems.md`*


Session 37.2, 24 Nov 2026, at Zach's ask ("go and do the different ecosystems that should be in the different environments
yourself and play around with getting the calibration"). Worked by 37.2 on the sweep's 167 river villages (51 generated worlds,
`../a_sweep/data`); every number from `calib.py` in this folder. Productivities are literature ranges from memory, named where
the source is known and marked est. where not: good to a factor of about two, not better.

## 1. The clock (why water food must not run on its own)

[[D2-273 Three clocks, each system on one|D2-273]] puts every food source on the year clock "so food sources and keeping are calibrated against each other". People eat on
the day clock: a real night's food each night, so 32 nights' food in a world year, 32/365 of a real year's. A food source that gives
its real year's production in the 32-night world year therefore feeds 11.4 times as many people as it really would. The runs,
the lake stock and the harvests take a real year's quantity x 32/365 ([[D2-259 The food values are anchored on real values|D2-259]]'s compressed year) and so stay in real balance with
eating. The shallows (u1 §2, written by 37.2) read the year clock as "a real year's production in 32 nights", which is the error:
they are 11.4 times too rich a night against everything else. The makers' resident fish (r 0.3 a night) sit off any clock. One
clock is already decided ([[D2-273 Three clocks, each system on one|D2-273]]); the fix is to bring the shallows and resident fish onto it, not a new choice ([[Q-98 One clock for the water's food before anything is sized|Q-98]] answered).

## 2. The ecosystems

A village's water is split by kind, and a river by its size above the village and its country's steepness (a Huet 1959 zonation,
by proxy: river km upstream and the landscape), each with a production of whole fish a hectare a real year and the share of a
year's take that falls in each season (spawning gatherings in spring, eels and summer feeding, autumn, the winter's torpor).

| Ecosystem | Where the generator would place it | Fish | Production kg/ha/yr | Season shares (spr, sum, aut, win) | Basis |
|---|---|---|---|---|---|
| trout beck | a river under 5 km above the village; upland brooks | brown trout, bullhead, minnow, stone loach, eel; salmon and sea trout parr | 20 to 80 | .25 .35 .25 .15 | trout stream studies (u1 §2's 20 to 168) |
| chalk stream | chalk and clay country, under 30 km above | brown trout, grayling, dace, eel, bullhead | 100 to 300 | .25 .35 .25 .15 | est.: chalk streams' known richness (Test, Itchen) |
| mixed river | uplands under 40 km; lowlands under 8 km | trout and grayling above, chub, dace, gudgeon, eel below | 40 to 120 | .25 .35 .25 .15 | est. between the two zones |
| lowland river | the rest of a single river | chub, dace, roach, perch, pike, gudgeon, barbel, eel | 50 to 150 | .30 .30 .25 .15 | Mann on the Stour and Thames, the Eden (sweep §5d); Welcomme 1985 |
| big river | a big river's stretch | bream, roach, pike, perch, ruffe, eel; flounder near the tide | 40 to 100 | .30 .30 .25 .15 | est.: lower a hectare than the margins, much larger area |
| fen dykes | fen parcels' open water (10% of their area) | eel above all, pike, tench, rudd, bream, perch | 60 to 200 | .25 .40 .25 .10 | est.; the fens' eel renders (Domesday) |
| lowland mere | a lake in lowland country | pike, perch, roach, bream, tench, eel | 30 to 120 | .30 .30 .25 .15 | Downing and Plante 1993 |
| upland tarn | a lake in upland country | brown trout, char, perch, minnow | 5 to 25 | .20 .40 .30 .10 | est.: oligotrophic lakes (Windermere's perch and char studies) |
| estuary | the river's area at a village by the tide | flounder, grey mullet, bass, smelt, eel | 30 to 100 (added) | .35 .25 .25 .15 | est. |

Half the production is taken for good (est., Welcomme's heavily fished rivers); whole fish 0.46 food a kg. Every village's
water area is the engine's own (river 18 m wide, big river 90 m, the village's home and ring stretch; fen 10% open water).

## 3. What it gives, by the world's landscape (medians, food a night; need 11)

| Landscape | Villages | Resident fish spr / sum / aut / win | Runs passing spr / sum / aut / win | A 30% spring salmon share, passing |
|---|---|---|---|---|
| Lowland river country | 10 | 0.77 / 0.93 / 0.71 / 0.41 | 0.2 / 0.2 / 3.6 / 4.7 | 2.0 |
| Chalk and clay | 9 | 1.65 / 2.24 / 1.59 / 0.95 | 0.2 / 0.2 / 3.5 / 5.4 | 2.7 |
| Fen basin | 11 | 0.63 / 0.70 / 0.57 / 0.33 | 2.5 / 0.2 / 1.0 / 2.5 | 0.8 |
| Estuary and saltmarsh | 11 | 0.85 / 0.89 / 0.72 / 0.42 | 2.0 / 0.3 / 2.0 / 3.8 | 1.6 |
| Upland and moor | 11 | 0.52 / 0.74 / 0.52 / 0.30 | 0.1 / 0.3 / 8.7 / 6.2 | 3.6 |
| Wet west, maritime | 10 | 0.79 / 1.11 / 0.79 / 0.46 | 0.5 / 0.4 / 3.0 / 4.2 | 1.9 |
| Dry east | 10 | 0.68 / 0.78 / 0.63 / 0.37 | 0.2 / 0.3 / 1.8 / 2.5 | 0.9 |
| Laid large river (the runs worlds) | 12 | 2.34 / 2.37 / 1.95 / 1.16 | 1.7 / 0.5 / 22.7 / 16.0 | 9.5 |
| Eelmouth (big river, 42 ha) | 1 | 2.99 / 3.03 / 2.50 / 1.49 | 0.2 / 0.3 / 88.4 / 61.5 | 35.9 |
| Meresby (a 38 km2 mere) | 1 | 215 / 216 / 180 / 108 | 0.1 / 0.1 / 7.0 / 1.3 | 0.7 |

(the other configurations in `calib.py`'s output.) Against today's makers: 1.3 a night on every river reach whatever its size,
and Eelmouth's 0.3.

## 4. What the calibration says

1. **On one clock and real productivity, a typical village's own water gives 5 to 10% of its need** (resident fish 0.5 to 1 a night);
   chalk streams and big rivers 15 to 27%. [[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter needs a lever of median 2.8 over these (quartiles 1.6 to 3.9): within
   the productivities' own uncertainty for many villages, generous for a small river. **Eelmouth's big river already gives about a
   quarter at real productivity** (3 a night against today's maker 0.3): real resident fish alone would close about 57 food of its
   19-day spring gap.
2. **A water-only village is only possible on a big river with runs** (or a large mere). With a third of the runs taken, 9 of 167
   generated river villages get a year's food from their water (12 of 167 with the lever 2.8); the median village's water gives 60
   of the 352 a year it needs. That is real: whole fishing communities lived on great runs, estuaries and meres, not on brooks. So
   [[D2-347 A water-only village should be able to last the year|D2-347]] holds for the worlds it is meant for (Eelmouth's kind), and water-only worlds must be placed there; elsewhere water is a
   supplement, as it was.
3. **The spring is carried by keeping, not by spring fish.** Even with a spring salmon share and the lamprey fixed, spring water
   food passing is 1 to 4 a night at a typical salmon-river village; the autumn passes 3 to 20 or more. Eelmouth's autumn passes 88
   a night. Closing the spring gap is keeping the autumn (salt, drying, hard cure) plus real resident fish, with the spring salmon
   on big salmon rivers.
4. **The fens are under-represented.** A fen parcel holds 10% open water and is not a water body, so a fen village's dykes are about
   0.6 ha and give almost nothing; real fen country (meres, dykes, the eel renders) was among the richest fisheries. Fens as water
   bodies with their meres and a real share of open water would change fen villages most.
5. **Different fish in different places matter little for the food total** (it is area x production) but a lot for what people do:
   trout and grayling by line in becks, pike and eels by trap and spear in fens, bream and roach by net in big rivers, spawning
   gatherings in spring shallows. One stock with a community label and its methods is the cheap first step; separate species
   stocks are a later one.

## 5. What this asks of stage 5b part 4 (into waters_general.md)

- Resident fish seeded by the engine: each village's water by ecosystem (the zonation above, from the land), K and r from the
  production and standing biomass, on the year clock (x 32/365), with one named lever beside the data ([[D2-348 A water-only village is made able to last the year by|D2-348]]'s quarter: about 2.8,
  calibrate; written with its reason).
- The shallows folded into the same accounting (their K and r brought onto the clock: today 11.4 times too rich), as the margin's
  share of the body's fish reachable by hand and basket, rising in the spring spawning season.
- Fens as water bodies with meres and a real open-water share; the season profile per ecosystem (catchability by season).
- Water-only worlds placed on big run rivers or meres (a gate check row: a water-only world's village must pass a year's need at
  real productivity with a third of its runs).
