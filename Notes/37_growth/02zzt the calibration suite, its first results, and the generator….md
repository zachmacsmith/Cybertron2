---
id: docs/review/37_growth/02zzt_calibration_suite.md
kind: note
updated: "2026-11-20"
---
# 02zzt: the calibration suite, its first results, and the generator audit

*note · `docs/review/37_growth/02zzt_calibration_suite.md`*


37.2, 20 Nov 2026. WORK [[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]]. Proposal `docs/cybertron2/proposals/calibration_worlds.md` ([[D2-228 Calibrate across a distribution of worlds|D2-228]]; all twelve worlds, [[D2-245 The calibration suite is all twelve worlds of…|D2-245]]). Zach
(17 Nov): "a distribution of different core test worlds covering a diverse range of potential environments not to remove diversity
but see that our calibrations generalize in relatively expected ways ... Don't expect them to be the same."

- **The worlds:** `cybertron2/specs/calibration/make_calibration_worlds.py` makes the twelve at seeds 1 and 2, no people (no check
  here needs them). The worlds stay out of git (`worlds/`, remade exactly from the seed); a land summary per world and an index are
  in `summary/`.
- **The expectations:** `cybertron2/specs/calibration/expectations.yaml`, written from the real places each world stands for (its
  `sources`), before reading the results; the orderings are at its end.
- **This report:** `02zzt_calibration_suite.py` (`python3 docs/review/37_growth/02zzt_calibration_suite.py`, about 2.5 minutes on
  4 cores). It writes `02zzt_calibration_suite.json` and the tables below between the markers. The text outside the markers is
  written by hand from those tables.
- **No model calls, no runs with people, no uploads.** The engine is used offline, as 02zzn and 02zzo do: its world (with the wild
  layer's 10-year history), its weather (`climate.py`) over 20 engine years, 02zzn's water on two clocks, and the ecology
  (`wild/ecology.py`) stepped on for 60 more years.

## At a glance

A row per world: the best food a unit of work by seed (seed 1; seed 2), the rest the mean of the two seeds (section 7 has each
in full). Measured. The reading is in section 8.

<!-- overview:begin (written by 02zzt_calibration_suite.py) -->

| World | best food a unit of work (master where a skill) | share of land good arable | commonest kinds by mass a km² | wet days (engine) | frost nights (engine) | flood years (water) | rain mm, mean °C (generator) |
|---|---|---|---|---|---|---|---|
| w01 Lowland river country | angling (master) 2.33; angling (master) 2.43 | 0.958 | red deer, brown hare, roe deer | 140 | 70 | 0.675 | 750, 8.55 |
| w02 Dry east | hunting the wood around (master) 3.02; hunting the wood around (master) 2.73 | 0.976 | red deer, brown hare, roe deer | 139 | 69 | 0.675 | 414, 9.46 |
| w03 Wet west, maritime | hunting the wood around (master) 2.47; hunting the wood around (master) 3.06 | 0.932 | red deer, brown hare, roe deer | 140 | 69 | 0.683 | 1178, 9.51 |
| w04 Coast under mountains | angling (master) 2.33; hunting the wood around (master) 2.69 | 0.775 | red deer, roe deer, brown hare | 142 | 70 | 0.65 | 1018, 8.56 |
| w05 Upland and moor | hunting the wood around (master) 2.62; hunting the wood around (master) 2.60 | 0.774 | red deer, roe deer, brown hare | 144 | 71 | 0.558 | 936, 8.58 |
| w06 High mountains | hunting the wood around (master) 2.89; hunting the wood around (master) 2.87 | 0.691 | red deer, roe deer, brown hare | 141 | 70 | 0.666 | 909, 8.3 |
| w07 Cold north | hunting the wood around (master) 2.55; hunting the wood around (master) 2.88 | 0.959 | red deer, brown hare, roe deer | 140 | 70 | 0.667 | 712, 5.57 |
| w08 Fen basin | hunting the wood around (master) 2.91; hunting the wood around (master) 2.93 | 0.806 | red deer, roe deer, brown hare | 136 | 67 | 0.692 | 490, 9.88 |
| w09 Estuary and saltmarsh | hunting the wood around (master) 2.66; hunting the wood around (master) 3.19 | 0.863 | red deer, brown hare, roe deer | 137 | 68 | 0.666 | 652, 9.73 |
| w10 Chalk and clay | hunting the wood around (master) 2.89; hunting the wood around (master) 2.89 | 0.968 | brown hare, red deer, roe deer | 143 | 71 | 0.542 | 724, 9.67 |
| w11 Sand and heath | angling (master) 2.30; hunting the wood around (master) 2.72 | 0.976 | red deer, brown hare, roe deer | 140 | 70 | 0.675 | 533, 9.47 |
| w12 Lake country | angling (master) 2.33; hunting the wood around (master) 2.76 | 0.752 | red deer, roe deer, brown hare | 143 | 71 | 0.584 | 1168, 8.64 |

<!-- overview:end -->

## 1. What was made

All 24 worlds generate at their first seeds; none was refused and none crashed (measured). The settings each world uses, and why,
are in the maker's `WORLDS` table. Three needed more than the proposal's table gives:

- **High mountains:** `upland and moor` with its moor raised from 560 to 900 m and a 300 m summit laid on it. The tops reach
  1,563 and 1,620 m. (1,150 and 450 gave 1,950 m.)
- **Lake country:** `upland and moor` with a laid mere at the fells' foot. The mere would not hold on the fells' flank (the land
  falls 200 m across it). It needed one small generator fix (commit `fix [[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]]: a laid lake is kept outside the lake cap`): ten
  larger upland hollows had taken the lake cap and drained the mere on both seeds. The maker also refuses a seed whose mere holds
  under 1 km². Seeds 1 and 2 pass, at 1.5 and 37 km².
- **Climates:** the proposal names rain and warmth only for rows 1, 2, 3 and 7. The rest take the rain and mean of the place each
  stands for, from the Met Office normals: 600 mm for the Fens, 1,400 for the Lakes, and so on.

Each world places three villages, whose land the water reads as reaches. The generator's own design checks warn as expected with
no people: capacity, and in the flat worlds dependence and chokepoint.

## 2. Reading the results

**Measured** (the tables below):

- **Ranges:**

  | Group | In range | Out of range |
  |---|---|---|
  | The generator's climate | 43 | 5 |
  | The engine's weather | 142 | 74 |
  | Land | 191 | 23 |
  | Water | 87 | 33 |
  | Ecosystems | 252 | 26 |
  | Wildlife present | 120 | 0 |

- **Orderings:**
  - The generator passes 15 of the 16 it can be read on. The one it fails is "the fen floods more than the chalk", read at the
    villages; the same pair read on the whole land passes.
  - The engine passes 3 of the 13 it can be read on. All three are height-driven: the fells wetter than the lee, the high tops
    colder than the upland's, and snow lying longer on the high tops.
- **Collapse:** none.
  - No system refuses or crashes on any world: the generator, the engine's world and its wild history, the weather, the water and
    the ecology.
  - No water store drifts: ten years of weather run four times give the same flows the second and fourth time, within 0.1%.
  - No kind runs away, and none dies out where its range includes the land.
  - The brown bear is still rising after the 10-year history on every world. It levels off after about 50 years, at 4 to 6 times
    its reference density (section 4).

**The known gap: the engine's weather.**
- It reads only a node's height (02zzo), so every world of a seed gets the same weather. The dry east, the wet west, the cold
  north and the coast all get the lowland's, within a few per cent.
- So it misses each dry, cold and coastal expectation, and the water, which runs on it, misses with it. The dry east spates and
  floods as often as the wet west: 1.6 a year both.
- This is the gap that climate from the land (OPEN [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]) closes. It is not a fault of the suite.
- The suite is built to show the change: once climate from the land is built, its engine column should move toward the
  generator's.

## 3. The engine's weather beyond the known gap (measured; inference marked)

Read against the lowland's own expectations, where height is not the issue:

- **Gales:**
  - Measured: 11 to 20 days a year at lowland villages with wind of 17 m/s or more, against 0 to 5 for the midlands. The engine's
    own `gale` label gives 10 to 17.
  - Inference: the wind field's gusts (`gust` × the field) are too wide for lowland Britain, or the day's `wind` is a gust, not a
    mean. Which one it is decides the fix.
- **Winter and frost:**
  - Winter is a little cold: 2.2 to 2.9 °C against 3.5 to 5.
  - Frost nights are 65 to 74 against the midlands' 45 or so. The diurnal range on clear nights is the likely cause.
- **Rain between years:**
  - Measured: the coefficient of variation of rain between engine years is 0.46 to 0.56; Britain's is about 0.15.
  - The two seeds differ by 30%: about 850 mm a year against 1,100 at the same villages. This is the 32-day year: a year is one
    month's sample of a weather chain.
  - On two clocks the seasonal stores read that month as a season, so one dry engine year is a drought year.
  - This belongs with climate from the land: the year's anomaly ([[D4-109 The weather scheduler|D4-109]]'s `year` layer) should carry the year's variance, and the
    days should only spread it.
- **Low water:** the river is low or dry 40 to 43% of the year at every village of every world. This is 02zzn's soil left too
  dry on two clocks (02zzn §3, finding 2). It masks the dry east, chalk and sand expectations and needs its evaporation curve
  calibrated.

## 4. The ecology (measured)

- Every kind expected present is present on every world.
- No kind runs away or dies out.
- **The brown bear:**
  - It settles at 0.086 to 0.114 a km² over the whole land. That is 4 to 6 times its reference density of 0.02, which is meant as
    a good habitat's.
  - The 10-year history leaves it at about a quarter of where it settles, on all 24 worlds.
  - Inference: European brown bear densities run about 0.01 to 0.05 a km² in good habitat, so it settles too high.
  - Two separate fixes, for the wild layer's owner: a longer history, or a start nearer equilibrium, for slow breeders; and its
    crowding or food limit.
- **Wolf and raven:** they settle at 1.5 to 1.8 and 1.2 times their reference, over the whole land. Inference: a little high,
  for the same reason.
- **Little difference between worlds, as expected:**
  - The kinds' densities differ only a little between worlds: red deer 2.1 to 2.4 a km² everywhere, from the Fens to the
    Highlands.
  - The wild layer reads cover and water, and the covers come out much alike (section 5, fault 7). The weather is the same by
    seed.
  - So the ecology's own calibration cannot be judged across the suite until both differ by world. Wildfowl (4 to 52 a km²) and
    eel (3 to 39) do follow the water.

<!-- suite:begin (written by 02zzt_calibration_suite.py) -->

### Counts

| Group (column) | in range | out of range | missing | no expectation |
|---|---|---|---|---|
| weather (the generator's climate) | 43 | 5 | 0 | 0 |
| weather (the engine's) | 142 | 74 | 0 | 0 |
| land | 191 | 23 | 0 | 2 |
| water (two clocks, on the engine's weather) | 87 | 33 | 0 | 0 |
| ecosystems | 252 | 26 | 0 | 0 |
| wildlife | 120 | 0 | 0 | 0 |

### Weather

At the villages. Each cell: the generator's value / the engine's (the generator holds only rain and the mean); the range below the name. **Bold** is out of range; the engine's misses on dry, cold and coastal worlds are the known gap (it reads only height, 02zzo; climate from the land, OPEN [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]).

| World | seed | rain_mm | wet_days | mean_temp_c | winter_c | summer_c | frost_nights | snow_lying_days | wind_ms | gale_days |
|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country (range) | | 600 to 1000 | 100 to 150 | 8.5 to 11 | 2.5 to 6 | 14 to 18 | 25 to 70 | 0 to 20 | 3 to 6 | 0 to 5 |
| | 1 | 747 / 846 | 129 | 8.68 / 9.24 | **2.43** | 16 | **71** | 10 | 5.62 | **13** |
| | 2 | 752 / **1108** | **150** | **8.43** / 9.48 | 2.65 | 16 | 68 | 13 | **6.39** | **17** |
| w02 Dry east (range) | | 450 to 700 | 85 to 125 | 9 to 12 | 2.5 to 6 | 15 to 19 | 25 to 70 | 0 to 20 | 3 to 6 | 0 to 5 |
| | 1 | **400** / **847** | **129** | 9.32 / 9.23 | **2.43** | 16 | **70** | 9.87 | 5.6 | **13** |
| | 2 | **428** / **1096** | **148** | 9.61 / 9.54 | 2.7 | 16 | 68 | 13 | **6.23** | **16** |
| w03 Wet west, maritime (range) | | 850 to 2000 | 140 to 200 | 9.5 to 12 | 5 to 9 | 14 to 18 | 0 to 30 | 0 to 5 | 5 to 8.5 | 2 to 30 |
| | 1 | 1244 / **844** | **129** | 9.57 / **9.24** | **2.44** | 16 | **71** | **10** | 5.57 | 12 |
| | 2 | 1112 / 1110 | 151 | **9.45** / 9.52 | **2.69** | 16 | **68** | **12** | 6.36 | 17 |
| w04 Coast under mountains (range) | | 900 to 2200 | 150 to 230 | 8 to 11 | 3 to 7 | 12 to 16 | 5 to 50 | 0 to 15 | 5 to 9 | 5 to 50 |
| | 1 | 971 / **846** | **131** | 8.7 / 9.23 | **2.43** | 16 | **71** | 10 | 5.59 | 12 |
| | 2 | 1064 / 1121 | 152 | 8.42 / 9.46 | **2.63** | 16 | **69** | 13 | 6.45 | 18 |
| w05 Upland and moor (range) | | 800 to 1600 | 140 to 210 | 7 to 10 | 1.5 to 5 | 13 to 16 | 35 to 100 | 3 to 40 | 4 to 8 | 1 to 25 |
| | 1 | **755** / 859 | **132** | 8.6 / 9.07 | 2.26 | 16 | 73 | 12 | 5.81 | 13 |
| | 2 | 1118 / 1136 | 155 | 8.56 / 9.3 | 2.48 | 16 | 70 | 15 | 6.69 | 20 |
| w06 High mountains (range) | | 800 to 2200 | 150 to 230 | 5.5 to 9 | -1 to 4 | 12 to 16 | 60 to 150 | 10 to 80 | 4 to 9 | 2 to 40 |
| | 1 | 897 / 847 | **130** | 8.45 / **9.28** | 2.47 | **16** | 70 | 10 | 5.59 | 13 |
| | 2 | 921 / 1113 | 152 | 8.16 / **9.38** | 2.57 | **16** | 70 | 14 | 6.52 | 18 |
| w07 Cold north (range) | | 550 to 950 | 100 to 160 | 4.5 to 7.5 | -5 to 1.5 | 13 to 18 | 80 to 170 | 30 to 120 | 3 to 6 | 0 to 8 |
| | 1 | 774 / 841 | 128 | 5.44 / **9.29** | **2.49** | 16 | **71** | **10** | 5.55 | **14** |
| | 2 | 649 / **1110** | 151 | 5.69 / **9.44** | **2.61** | 16 | **69** | **13** | **6.46** | **19** |
| w08 Fen basin (range) | | 480 to 750 | 90 to 130 | 9 to 12 | 2.5 to 6 | 15 to 18 | 25 to 75 | 0 to 20 | 3.5 to 6.5 | 0 to 8 |
| | 1 | 499 / **819** | 127 | 9.94 / 9.42 | 2.63 | 16 | 69 | 9.13 | 5.35 | **12** |
| | 2 | 481 / **1083** | **146** | 9.82 / 9.76 | 2.93 | 16 | 65 | 12 | 6.03 | **16** |
| w09 Estuary and saltmarsh (range) | | 550 to 950 | 100 to 150 | 9 to 12 | 3 to 7 | 15 to 18 | 15 to 60 | 0 to 15 | 4 to 7 | 0 to 10 |
| | 1 | 666 / 812 | 126 | 9.62 / 9.39 | **2.57** | 16 | **68** | 10 | 5.4 | **11** |
| | 2 | 638 / **1091** | 148 | 9.85 / 9.62 | **2.8** | 16 | **68** | 11 | 6.17 | **16** |
| w10 Chalk and clay (range) | | 650 to 1000 | 105 to 150 | 9 to 12 | 2.5 to 6 | 15 to 18 | 30 to 75 | 0 to 20 | 3.5 to 6.5 | 0 to 8 |
| | 1 | 762 / 868 | 133 | 9.47 / 9.05 | **2.25** | 16 | 74 | 12 | 5.85 | **15** |
| | 2 | 685 / **1125** | **152** | 9.87 / 9.54 | 2.72 | 16 | 68 | 13 | 6.39 | **17** |
| w11 Sand and heath (range) | | 500 to 900 | 90 to 140 | 9 to 12 | 2 to 6 | 15 to 18 | 40 to 110 | 0 to 20 | 3 to 6 | 0 to 6 |
| | 1 | 518 / 851 | 130 | 9.33 / 9.19 | 2.37 | 16 | 71 | 12 | 5.68 | **13** |
| | 2 | 548 / **1095** | **149** | 9.62 / 9.54 | 2.72 | 16 | 68 | 13 | **6.21** | **16** |
| w12 Lake country (range) | | 1000 to 2500 | 160 to 230 | 7.5 to 10 | 2 to 5.5 | 13 to 16 | 25 to 80 | 2 to 30 | 4 to 8 | 1 to 30 |
| | 1 | 1126 / **859** | **132** | 8.61 / 9.07 | 2.26 | 16 | 73 | 12 | 5.81 | 13 |
| | 2 | 1209 / 1123 | **154** | 8.67 / 9.32 | 2.5 | 16 | 70 | 16 | 6.65 | 20 |

### Land

| World | seed | max_height_m | share_over_500m | share_over_10deg | floodplain_share | terrace_share | low_ground_share | wet_ground_share | treeline_m | above_treeline_share |
|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country (range) | | 80 to 350 | 0 to 0 | 0 to 0.08 | 0.04 to 0.2 | 0.02 to 0.2 | 0.04 to 0.3 | 0.03 to 0.25 | none | 0 to 0 |
| | 1 | 144 | 0 | 0 | 0.121 | 0.0999 | 0.138 | 0.0573 | - | 0 |
| | 2 | 140 | 0 | 0 | 0.167 | 0.0696 | 0.192 | 0.0675 | - | 0 |
| w02 Dry east (range) | | 50 to 300 | 0 to 0 | 0 to 0.06 | 0.03 to 0.18 | 0.02 to 0.2 | 0.03 to 0.3 | 0.01 to 0.15 | none | 0 to 0 |
| | 1 | 151 | 0 | 0 | 0.114 | 0.0757 | 0.127 | 0.0299 | - | 0 |
| | 2 | 143 | 0 | 0 | 0.168 | 0.0776 | 0.186 | 0.0372 | - | 0 |
| w03 Wet west, maritime (range) | | 60 to 450 | 0 to 0.02 | 0 to 0.2 | 0.02 to 0.15 | 0.01 to 0.15 | 0.02 to 0.25 | 0.05 to 0.35 | none | 0 to 0 |
| | 1 | 144 | 0 | 0.0038 | 0.13 | 0.131 | 0.149 | 0.0855 | - | 0 |
| | 2 | 140 | 0 | 0.0039 | **0.159** | 0.103 | 0.175 | 0.0956 | - | 0 |
| w04 Coast under mountains (range) | | 500 to 1100 | 0.02 to 0.3 | 0.08 to 0.5 | 0.01 to 0.12 | 0 to 0.12 | 0.01 to 0.2 | 0.05 to 0.4 | 350 to 700 | 0 to 0.25 |
| | 1 | 801 | 0.0661 | 0.0955 | 0.111 | 0.086 | 0.128 | 0.0711 | 588 | 0.018 |
| | 2 | 788 | 0.0693 | 0.0935 | **0.143** | 0.0815 | 0.159 | 0.0772 | 592 | 0.0142 |
| w05 Upland and moor (range) | | 450 to 950 | 0.02 to 0.3 | 0.06 to 0.4 | 0.01 to 0.1 | 0 to 0.12 | 0.01 to 0.2 | 0.08 to 0.45 | 400 to 650 | 0.02 to 0.3 |
| | 1 | **1064** | 0.0841 | 0.0932 | 0.0852 | 0.0756 | 0.121 | **0.0504** | 624 | 0.0429 |
| | 2 | **1131** | 0.0931 | 0.0985 | **0.112** | 0.0653 | 0.147 | **0.0543** | 620 | 0.0459 |
| w06 High mountains (range) | | 1100 to 1600 | 0.1 to 0.55 | 0.15 to 0.65 | 0 to 0.08 | 0 to 0.1 | 0 to 0.15 | 0.05 to 0.4 | 450 to 700 | 0.1 to 0.5 |
| | 1 | 1563 | 0.171 | 0.153 | **0.0969** | 0.0831 | 0.133 | 0.0589 | 550 | 0.147 |
| | 2 | **1620** | 0.165 | 0.161 | **0.124** | 0.0729 | **0.159** | 0.0622 | 558 | 0.146 |
| w07 Cold north (range) | | 80 to 350 | 0 to 0 | 0 to 0.08 | 0.04 to 0.2 | 0.02 to 0.2 | 0.04 to 0.3 | 0.05 to 0.3 | none | 0 to 0 |
| | 1 | 144 | 0 | 0 | 0.12 | 0.0939 | 0.138 | 0.0568 | 104 | **0.0074** |
| | 2 | 140 | 0 | 0 | 0.165 | 0.0684 | 0.192 | 0.0665 | 103 | **0.011** |
| w08 Fen basin (range) | | 5 to 150 | 0 to 0 | 0 to 0.03 | 0 to 0.2 | 0 to 0.15 | 0.15 to 0.9 | 0.3 to 0.9 | none | 0 to 0 |
| | 1 | 114 | 0 | 0.0013 | 0.0771 | 0.0972 | 0.241 | **0.153** | - | 0 |
| | 2 | 124 | 0 | 0.003 | 0.0972 | 0.102 | 0.273 | **0.154** | - | 0 |
| w09 Estuary and saltmarsh (range) | | 20 to 250 | 0 to 0 | 0 to 0.05 | 0.03 to 0.25 | 0.01 to 0.2 | 0.08 to 0.6 | 0.12 to 0.6 | none | 0 to 0 |
| | 1 | 130 | 0 | 0.0058 | 0.0704 | 0.0807 | 0.162 | 0.13 | - | 0 |
| | 2 | 140 | 0 | 0.0051 | 0.13 | 0.0924 | 0.228 | 0.126 | - | 0 |
| w10 Chalk and clay (range) | | 150 to 350 | 0 to 0 | 0 to 0.12 | 0.02 to 0.15 | 0.01 to 0.15 | 0.02 to 0.25 | 0.03 to 0.3 | none | 0 to 0 |
| | 1 | 307 | 0 | 0 | 0.121 | 0.0347 | 0.146 | 0.0441 | - | 0 |
| | 2 | 309 | 0 | 0.0001 | **0.151** | 0.0408 | 0.204 | 0.0503 | - | 0 |
| w11 Sand and heath (range) | | 40 to 220 | 0 to 0 | 0 to 0.05 | 0.01 to 0.12 | 0.01 to 0.15 | 0.01 to 0.2 | 0 to 0.12 | none | 0 to 0 |
| | 1 | 195 | 0 | 0 | 0.106 | 0.0852 | 0.12 | 0.0319 | - | 0 |
| | 2 | **237** | 0 | 0 | **0.158** | 0.071 | 0.181 | 0.0383 | - | 0 |
| w12 Lake country (range) | | 500 to 1000 | 0.02 to 0.3 | 0.08 to 0.5 | 0.01 to 0.1 | 0 to 0.12 | 0.01 to 0.2 | 0.08 to 0.45 | 400 to 650 | 0 to 0.3 |
| | 1 | **1064** | 0.0841 | 0.0922 | 0.0955 | 0.101 | 0.133 | **0.0765** | 622 | 0.0429 |
| | 2 | **1131** | 0.094 | 0.1 | **0.113** | 0.0835 | 0.154 | **0.0768** | 619 | 0.0467 |

### Water

| World | seed | spates_a_year | floods_a_year | flood_years | low_water_share | ice_days |
|---|---|---|---|---|---|---|
| w01 Lowland river country (range) | | 0.3 to 3 | 0.1 to 1 | 0.2 to 0.8 | 0.05 to 0.35 | 0 to 10 |
| | 1 | 1.67 | 0.85 | 0.7 | **0.428** | 8.73 |
| | 2 | 1.75 | 0.75 | 0.65 | **0.404** | 9.13 |
| w02 Dry east (range) | | 0.1 to 1.5 | 0 to 0.5 | 0.05 to 0.5 | 0.15 to 0.6 | 0 to 15 |
| | 1 | **1.58** | **0.9** | **0.683** | 0.423 | 8.93 |
| | 2 | **1.68** | **0.8** | **0.667** | 0.405 | 8.57 |
| w03 Wet west, maritime (range) | | 1 to 6 | 0.2 to 2 | 0.4 to 1 | 0 to 0.25 | 0 to 2 |
| | 1 | 1.6 | 0.933 | 0.717 | **0.416** | **9.13** |
| | 2 | 1.6 | 0.767 | 0.65 | **0.406** | **9.13** |
| w04 Coast under mountains (range) | | 1 to 8 | 0.3 to 3 | 0.4 to 1 | 0 to 0.25 | 0 to 10 |
| | 1 | 1.77 | 0.867 | 0.717 | **0.418** | 9.3 |
| | 2 | 1.5 | 0.55 | 0.583 | **0.405** | 9.9 |
| w05 Upland and moor (range) | | 0.5 to 6 | 0.1 to 2 | 0.3 to 1 | 0 to 0.3 | 0 to 30 |
| | 1 | 1.55 | 0.95 | 0.7 | **0.421** | 11 |
| | 2 | 0.967 | 0.3 | 0.417 | **0.4** | 9.7 |
| w06 High mountains (range) | | 0.5 to 6 | 0.1 to 2 | 0.3 to 1 | 0 to 0.3 | 5 to 90 |
| | 1 | 1.57 | 0.917 | 0.7 | **0.42** | 8.57 |
| | 2 | 1.78 | 0.667 | 0.633 | **0.417** | 9.7 |
| w07 Cold north (range) | | 0.3 to 3 | 0.1 to 1 | 0.2 to 0.8 | 0.05 to 0.4 | 20 to 120 |
| | 1 | 1.78 | 0.9 | 0.683 | **0.434** | **8.93** |
| | 2 | 1.75 | 0.817 | 0.65 | **0.408** | **8.97** |
| w08 Fen basin (range) | | 0.2 to 3 | 0.1 to 1.5 | 0.3 to 1 | 0.05 to 0.4 | 0 to 15 |
| | 1 | 1.75 | 0.867 | 0.683 | **0.421** | 8.53 |
| | 2 | 1.57 | 0.633 | 0.7 | **0.402** | 7.2 |
| w09 Estuary and saltmarsh (range) | | 0.2 to 3 | 0.1 to 1.5 | 0.2 to 1 | 0.05 to 0.4 | 0 to 10 |
| | 1 | 1.62 | 0.917 | 0.7 | **0.424** | 7.97 |
| | 2 | 1.62 | 0.667 | 0.633 | **0.41** | 7.63 |
| w10 Chalk and clay (range) | | 0.05 to 2 | 0 to 0.6 | 0 to 0.6 | 0.1 to 0.5 | 0 to 10 |
| | 1 | 1.32 | 0.583 | 0.567 | 0.418 | **10** |
| | 2 | 1.58 | 0.45 | 0.517 | 0.405 | 7.8 |
| w11 Sand and heath (range) | | 0.05 to 1.5 | 0 to 0.5 | 0 to 0.5 | 0.15 to 0.6 | 0 to 15 |
| | 1 | 1.45 | **0.917** | **0.733** | 0.42 | 9.33 |
| | 2 | 1.5 | **0.617** | **0.617** | 0.413 | 8.37 |
| w12 Lake country (range) | | 0.3 to 5 | 0.1 to 2 | 0.3 to 1 | 0 to 0.3 | 0 to 30 |
| | 1 | 1.53 | 0.95 | 0.7 | **0.422** | 11 |
| | 2 | 0.983 | 0.317 | 0.467 | **0.397** | 9.7 |

### Ecosystems

| World | seed | woodland_share | heath_share | moor_share | wetland_share | saltmarsh_share | lake_share |
|---|---|---|---|---|---|---|---|
| w01 Lowland river country (range) | | 0.15 to 0.4 | 0 to 0.05 | 0 to 0.01 | 0.02 to 0.15 | 0 to 0 | 0 to 0.005 |
| | 1 | 0.299 | 0.0118 | 0.0002 | 0.048 | 0 | 0 |
| | 2 | 0.299 | 0.0047 | 0 | 0.0558 | 0 | 0 |
| w02 Dry east (range) | | 0.1 to 0.4 | 0 to 0.15 | 0 to 0.01 | 0 to 0.12 | 0 to 0 | 0 to 0.005 |
| | 1 | 0.299 | 0.0102 | 0 | 0.0253 | 0 | 0 |
| | 2 | 0.299 | 0.0027 | 0 | 0.0303 | 0 | 0 |
| w03 Wet west, maritime (range) | | 0.15 to 0.45 | 0 to 0.08 | 0 to 0.05 | 0.02 to 0.2 | 0.0005 to 0.03 | 0 to 0.005 |
| | 1 | 0.299 | 0.0102 | 0 | 0.0711 | **0.0002** | 0 |
| | 2 | 0.299 | 0.0021 | 0 | 0.0777 | **0.0002** | 0 |
| w04 Coast under mountains (range) | | 0.1 to 0.45 | 0 to 0.05 | 0.05 to 0.45 | 0.01 to 0.15 | 0 to 0.02 | 0 to 0.02 |
| | 1 | 0.299 | 0.0122 | 0.0891 | 0.0569 | 0.0002 | 0 |
| | 2 | 0.299 | 0.0037 | 0.0966 | 0.0604 | 0.0002 | 0 |
| w05 Upland and moor (range) | | 0.05 to 0.35 | 0 to 0.05 | 0.1 to 0.55 | 0.01 to 0.15 | 0 to 0 | 0 to 0.02 |
| | 1 | 0.296 | 0.0125 | 0.106 | 0.0398 | 0 | 0.0102 |
| | 2 | 0.292 | 0.001 | 0.111 | 0.0405 | 0 | **0.0242** |
| w06 High mountains (range) | | 0.05 to 0.35 | 0 to 0.05 | 0.15 to 0.6 | 0 to 0.12 | 0 to 0 | 0 to 0.03 |
| | 1 | 0.295 | 0.0086 | 0.184 | 0.0424 | 0 | 0.0117 |
| | 2 | 0.292 | 0.0036 | 0.167 | 0.0439 | 0 | 0.0241 |
| w07 Cold north (range) | | 0.15 to 0.45 | 0 to 0.08 | 0 to 0.05 | 0.02 to 0.2 | 0 to 0 | 0 to 0.005 |
| | 1 | 0.299 | 0.0069 | 0.0075 | 0.0477 | 0 | 0 |
| | 2 | 0.299 | 0.0047 | 0.0109 | 0.0555 | 0 | 0 |
| w08 Fen basin (range) | | 0.02 to 0.35 | 0 to 0.05 | 0 to 0.01 | 0.3 to 0.9 | 0 to 0.05 | 0 to 0.05 |
| | 1 | 0.299 | 0.0048 | 0 | 0.32 | 0.0011 | 0 |
| | 2 | 0.298 | 0.0017 | 0 | 0.35 | 0.0073 | 0.0022 |
| w09 Estuary and saltmarsh (range) | | 0.05 to 0.35 | 0 to 0.05 | 0 to 0.01 | 0.1 to 0.6 | 0.003 to 0.08 | 0 to 0.03 |
| | 1 | 0.299 | 0.0138 | 0.0001 | 0.187 | 0.0077 | 0 |
| | 2 | 0.298 | 0.0104 | 0 | 0.173 | 0.0069 | 0 |
| w10 Chalk and clay (range) | | 0.1 to 0.4 | 0 to 0.05 | 0 to 0.01 | 0.01 to 0.15 | 0 to 0 | 0 to 0.005 |
| | 1 | 0.299 | 0.0029 | 0 | 0.0356 | 0 | 0 |
| | 2 | 0.299 | 0.0029 | 0 | 0.0403 | 0 | 0 |
| w11 Sand and heath (range) | | 0.1 to 0.45 | 0.12 to 0.6 | 0 to 0.01 | 0 to 0.1 | 0 to 0 | 0 to 0.005 |
| | 1 | 0.299 | 0.133 | 0 | 0.0264 | 0 | 0 |
| | 2 | 0.299 | **0.109** | 0 | 0.0302 | 0 | 0 |
| w12 Lake country (range) | | 0.1 to 0.4 | 0 to 0.05 | 0.05 to 0.45 | 0.01 to 0.15 | 0 to 0 | 0.01 to 0.08 |
| | 1 | 0.296 | 0.0062 | 0.11 | 0.0595 | 0 | 0.0108 |
| | 2 | 0.287 | 0.0014 | 0.114 | 0.0553 | 0 | 0.0399 |

### Kinds present and absent

Ecosystems expected present (on at least 0.1% of the land) or absent, and wild kinds expected present (0.01 a km² or more in the year's highest season, the mean over the suite's years after the wild layer's history; the runs' salmon and lamprey live in the runs' own store and are not counted here). Only the misses are listed.

| World | seed | missed |
|---|---|---|
| w01 Lowland river country | 1 | absent: moor (present, 0.0001); absent: blanket bog (present, 0.0001) |
| w01 Lowland river country | 2 | none |
| w02 Dry east | 1 | none |
| w02 Dry east | 2 | none |
| w03 Wet west, maritime | 1 | present: saltmarsh (absent, 0.0002); absent: chalk grassland (present, 0.0191) |
| w03 Wet west, maritime | 2 | present: saltmarsh (absent, 0.0002); absent: chalk grassland (present, 0.0346) |
| w04 Coast under mountains | 1 | absent: chalk grassland (present, 0.0235); absent: beech wood (present, 0.0421) |
| w04 Coast under mountains | 2 | absent: chalk grassland (present, 0.0293); absent: beech wood (present, 0.0218) |
| w05 Upland and moor | 1 | present: blanket bog (absent, 0.0009); absent: chalk grassland (present, 0.0106) |
| w05 Upland and moor | 2 | absent: chalk grassland (present, 0.0166) |
| w06 High mountains | 1 | absent: chalk grassland (present, 0.0153) |
| w06 High mountains | 2 | absent: chalk grassland (present, 0.0111) |
| w07 Cold north | 1 | absent: beech wood (present, 0.0385) |
| w07 Cold north | 2 | absent: beech wood (present, 0.0197) |
| w08 Fen basin | 1 | absent: chalk grassland (present, 0.0009) |
| w08 Fen basin | 2 | absent: chalk grassland (present, 0.0001) |
| w09 Estuary and saltmarsh | 1 | absent: blanket bog (present, 0.0001) |
| w09 Estuary and saltmarsh | 2 | none |
| w10 Chalk and clay | 1 | none |
| w10 Chalk and clay | 2 | none |
| w11 Sand and heath | 1 | none |
| w11 Sand and heath | 2 | none |
| w12 Lake country | 1 | absent: chalk grassland (present, 0.0106) |
| w12 Lake country | 2 | absent: chalk grassland (present, 0.0128) |

### The ordering checks

Each pair must come out a < b on both seeds (seed 1 against seed 1, seed 2 against seed 2), apart by more than 5% of the larger (a tie fails). Values a / b. Rain at a probe is its mean (the catchment's), not its median.

| Ordering | from | the generator | the engine |
|---|---|---|---|
| the dry east is drier than the lowland | proposal | passes: 400 / 747; 428 / 752 | **fails**: 847 / 846; 1096 / 1108 |
| the wet west's coast frosts less than the cold north | proposal | passes: 9.58 / 5.44; 9.64 / 5.69 (stand-in: mean_temp_c, more (the generator has no frost)) | **fails**: 71 / 71; 66 / 69 |
| the fells are wetter than the lee | proposal | passes: 1023 / 2185; 1010 / 2028 | passes: 844 / 1063; 1096 / 1209 |
| the fells' slopes facing the wind are wetter than the slopes facing away | row 4 (it should pass; the gap's size is read in the audit) | passes: 1155 / 3349; 1246 / 2925 | n/a |
| the fen floods more than the chalk | proposal | **fails**: 0.204 / 0.307; 0.417 / 0.382 | **fails**: 0.094 / 0.126; 0.171 / 0.175 |
| the fen's land lies nearer its rivers than the chalk's | proposal (the fen floods more than the chalk), read on the whole land | passes: 0.146 / 0.241; 0.204 / 0.273 | n/a |
| the sand holds less water than the clay | proposal | passes: 79 / 171; 79 / 171 | n/a |
| the wet west is wetter than the lowland | rows 1 and 3 | passes: 747 / 1244; 752 / 1112 | **fails**: 846 / 844; 1108 / 1110 |
| the wet west has more wet days than the dry east | rows 2 and 3 | n/a | **fails**: 129 / 129; 148 / 151 |
| the cold north is colder than the lowland | rows 1 and 7 | passes: 5.44 / 8.68; 5.69 / 8.43 | **fails**: 9.29 / 9.24; 9.44 / 9.48 |
| the cold north has more ice than the lowland | row 7: frozen still water | n/a | **fails**: 8.73 / 8.93; 9.13 / 8.97 |
| the wet west's coast is windier than the lowland | row 3: windy | n/a | **fails**: 5.62 / 5.65; 6.39 / 6.29 |
| the high mountains' tops are colder than the upland's | rows 5 and 6 | passes: 0.98 / 4; 0.84 / 3.93 | passes: 2.8 / 5.1; 2.92 / 5.44 |
| snow lies longer on the mountains' tops than in the lowland | row 6: long snow | n/a | passes: 10 / 123; 13 / 127 |
| the wet west's rivers are flashier than the dry east's | rows 2 and 3 | n/a | **fails**: 1.58 / 1.6; 1.68 / 1.6 |
| the dry east has more low water than the wet west | rows 2 and 3 | n/a | **fails**: 0.416 / 0.423; 0.406 / 0.405 |
| the fen has more wet ground than the lowland | row 8 | passes: 0.0573 / 0.153; 0.0675 / 0.154 | n/a |
| the estuary has more saltmarsh than the lowland | row 9 | passes: 0 / 0.0077; 0 / 0.0069 | n/a |
| the sand has more heath than the lowland | row 11 | passes: 0.0118 / 0.133; 0.0047 / 0.109 | n/a |
| the downs lie drier than the vale | row 10 | passes: 0.167 / 0.33; 0.2 / 0.337 | n/a |
| the lake country has more lake than the upland | row 12 | passes: 0.0102 / 0.0108; 0.0242 / 0.0399 | n/a |
| the mountains have less arable ground than the lowland | row 6: little arable | passes: 0.89 / 0.996; 0.871 / 0.997 | n/a |

### Collapse

| World | seed | generator | engine world, weather, water, ecology | kinds died out where their range includes the land |
|---|---|---|---|---|
| w01 Lowland river country | 1 | made | none | none |
| w01 Lowland river country | 2 | made | none | none |
| w02 Dry east | 1 | made | none | none |
| w02 Dry east | 2 | made | none | none |
| w03 Wet west, maritime | 1 | made | none | none |
| w03 Wet west, maritime | 2 | made | none | none |
| w04 Coast under mountains | 1 | made | none | none |
| w04 Coast under mountains | 2 | made | none | none |
| w05 Upland and moor | 1 | made | none | none |
| w05 Upland and moor | 2 | made | none | none |
| w06 High mountains | 1 | made | none | none |
| w06 High mountains | 2 | made | none | none |
| w07 Cold north | 1 | made | none | none |
| w07 Cold north | 2 | made | none | none |
| w08 Fen basin | 1 | made | none | none |
| w08 Fen basin | 2 | made | none | none |
| w09 Estuary and saltmarsh | 1 | made | none | none |
| w09 Estuary and saltmarsh | 2 | made | none | none |
| w10 Chalk and clay | 1 | made | none | none |
| w10 Chalk and clay | 2 | made | none | none |
| w11 Sand and heath | 1 | made | none | none |
| w11 Sand and heath | 2 | made | none | none |
| w12 Lake country | 1 | made | none | none |
| w12 Lake country | 2 | made | none | none |

### The ecology settling

Not collapses: each kind's numbers stepped on for the suite's ecology years after the wild layer's 10-year history (engine/wild.py HISTORY_YEARS). `slow` counts world-seeds where a kind settles at more than twice where the history left it (the history is too short for it); `high` where its settled density over the whole land is over three times its reference density (kinds.py `ref` x `d0`, a density of good habitat, so the whole land should be under it).

| Kind | reference a km2 | settled a km2 over the land (min to max) | slow | high |
|---|---|---|---|---|
| red deer | 8 | 2.11 to 2.35 | 0 of 24 | 0 of 24 |
| roe deer | 15 | 6.16 to 8.06 | 0 of 24 | 0 of 24 |
| wild boar | 4 | 1.12 to 1.69 | 0 of 24 | 0 of 24 |
| brown hare | 25 | 29 to 57 | 0 of 24 | 0 of 24 |
| woodpigeon | 50 | 45 to 120 | 0 of 24 | 0 of 24 |
| rats | 100 | 2.57 to 4.55 | 0 of 24 | 0 of 24 |
| wildfowl | 150 | 4.18 to 52 | 0 of 24 | 0 of 24 |
| eel | 150 | 3.39 to 39 | 0 of 24 | 0 of 24 |
| salmon | runs | 0 to 0 | 0 of 24 | 0 of 24 |
| lamprey | runs | 0 to 0 | 0 of 24 | 0 of 24 |
| otter | 0.3 | 0.164 to 0.233 | 0 of 24 | 0 of 24 |
| voles and mice | 3000 | 270 to 4211 | 0 of 24 | 0 of 24 |
| owls | 1 | 0.539 to 0.952 | 0 of 24 | 0 of 24 |
| fox | 2 | 1.09 to 1.28 | 0 of 24 | 0 of 24 |
| stoat | 4 | 2.22 to 2.38 | 0 of 24 | 0 of 24 |
| wolf | 0.025 | 0.0372 to 0.0452 | 0 of 24 | 0 of 24 |
| raven | 0.2 | 0.229 to 0.242 | 0 of 24 | 0 of 24 |
| brown bear | 0.02 | 0.0856 to 0.114 | 24 of 24 | 24 of 24 |

<!-- suite:end -->

## 5. The generator audit ([[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]]): what the land gets wrong, world by world

Each fault has its evidence (measured, from the tables and the summaries) and a proposed fix. Proposed fixes are proposals, not
built: only fault 9's small fix was built (section 1).

**1. The water allocator gives a village at most two cells of water, whatever the land has.**
- **Evidence:**
  - Over the 72 villages of the suite, a village's water parcels hold at most 2 cells (4.5 ha): 50 have 2, 3 have 1, and 19
    have none.
  - Those 19 have 0.6 to 10.8 km of stream (class 1 and up) within their 2.5 km reach, and up to 3.1 km of river of class 2 and
    up. The median village has 6.6 km of stream and 3.3 km of river in reach.
  - `settle.allocate` takes `near_water[:2]`: the first two river (class 2 and up) or lake cells in travel order, and none from
    the sea. A brook (class 1) never counts.
- **Fix proposed:** water parcels in proportion to the water in reach:
  - one parcel per stretch of river (class 1 and up), about a km of bank each, up to the river length within `field_km`;
  - a lake's shore within reach;
  - the sea's shore where the village is within reach of it.
  The sizes follow the river's class. The water measure ([[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]]) and the fishing calibration need it: today a village on 6 km of
  river fishes 4.5 ha at most.

**2. No village sits on the coast, and none in the fen.**
- **Evidence:**
  - In the four coastal worlds (wet west, coast under mountains, fen, estuary), no village's land comes nearer the sea than
    1.9 km.
  - In the fen basin no village stands on fen ground: all six stand on river floodplain, clay vale or terrace beside it. Fen is in
    `settle.FORBIDDEN` and the site score counts the sea as water only within 0.4 km.
  - So the villages' land in the fen world lies higher above its rivers than the chalk world's (0.20 against 0.31 within 1 m on
    seed 1). The proposal's "the fen floods more than the chalk" fails at the villages, and passes only on the whole land.
- **Fix proposed:**
  - a configuration's sites follow its landscape: on a coast, at least one village by the sea (a landing, saltmarsh grazing);
  - in a fen, on its islands and its edge, with fen in reach;
  - the sea counted as water in the site score.

**3. The rain sweep spends the sea's moisture on the first 3 km of coast, and rains only on slopes that face the wind.**
- **Evidence (coast under mountains; coast and strip as medians, the range's faces as means):**
  - the land within 3 km of the sea takes 2,750 to 2,840 mm;
  - the windward strip beyond it 1,210 to 1,480;
  - the range's slopes facing the wind 2,930 to 3,350;
  - its slopes facing away 1,155 to 1,246 (median 943: most of their cells sit at the sweep's floor, the same as the lee's
    940 to 980).
  - On the wet west the coast takes 3,280 against 1,130 inland.
- **Cause:** the sweep takes 0.35 of each cell's rain from the air's moisture (`physical.climate`). On 150 m cells the air loses
  most of it within about 2.5 km of land, a scale set by the cell size. Lift reads only a rise along the wind, so a cell just past
  a crest gets the floor.
- **Real:** the windward coast takes 1,100 to 1,600 mm and the fells 2,500 to 4,000, wet on the tops and on the lee side of the
  crest (spillover), with the shadow beginning a few km downwind.
- **Fix proposed:**
  - depletion per km, not per cell, with an e-folding length of tens of km for the background rain;
  - lift spread downwind by a few km;
  - RAIN_MEAN and the mm bounds re-measured.
  This changes every world's rain, so it is reported, not built.

**4. Chalk, and with it beech wood and chalk grassland, turns up in every world.**
- **Evidence:** chalk grassland covers 1 to 3.5% of the land in the wet west, the coast under mountains, the upland, the high
  mountains and the lake country, and beech wood 2 to 4% in the coast under mountains and the cold north.
- **Cause:** `physical.build` lays chalk wherever a second geology noise passes `chalk_n` on ground over 80 m, in any
  configuration.
- **Real:** the Pennines are gritstone and limestone, the Highlands granite and schist, Devon slate and sandstone, west Scotland
  gneiss: none is chalk.
- **Fix proposed:** the geology noise by landscape system: chalk only in scarp and vale, or where a world allows it; upland and
  coast systems draw from their own rocks (gritstone, granite, slate). Today no texture code exists for any of these, so the fix is
  a texture or a "rock" field the soils read.

**5. The ecosystems read the climate only at the tree line, and the tree line reads only the year's mean.**
- **Evidence:**
  - The cold north (6 °C) grows oak-ash wood and beech wood (2 to 4%) like the lowland. It has birch and pine only where the sand
    noise falls.
  - Its tree line comes out at 103 to 104 m, with 0.7 to 1.1% of a flat lowland above it, because `treeline_c` is a year's mean
    of 4.6 °C.
  - In the uplands the tree line comes out at 550 to 625 m, which is right for Britain.
- **Real:** at a 6 °C mean the trees grow to 900 m and more. The tree line follows summer warmth (about the 10 °C July isotherm),
  not the year's mean, which works only in oceanic Britain. The beech's northern limit and the boreal mix follow winter cold and
  the growing season.
- **Fix proposed:**
  - the tree line by the warmest season's mean (it needs the seasonal temperatures climate from the land will carry);
  - the forest type by warmth (birch and pine below a threshold, no beech in a cold climate).

**6. The uplands are too high, and the high mountains are mostly lowland.**
- **Evidence:**
  - `upland and moor` (the Pennines) reaches 1,064 and 1,131 m; Cross Fell is 893.
  - The high mountains' land is 17% above 500 m, with a median of 126 to 136 m.
  - Their villages all stand under about 150 m, and no node of the four upland worlds stands above 454 m (the high mountains'
    highest node is 376 m). [[D2-227 Some places are harsher|D2-227]] wants nodes above 500 m.
- **Cause:** the massif's height is multiplied by the ridged roughness and the spurs (up to about 1.8 together), and the upland
  system covers the north-east two-thirds of the window only.
- **Fix proposed:**
  - the massif's peak normalised so `height` is its top;
  - for a mountain world, the upland box over the whole window, or a configuration of its own;
  - sites allowed on upland pasture when a world asks for high nodes.

**7. Many land shares are the same from world to world.**
- **Evidence:**
  - Wood is 0.29 to 0.30 of the land in all 24 worlds, the Fens' and the Highlands' alike. `settled` sets the wood share and
    clearing cuts to it.
  - The floodplain share runs 0.08 to 0.17 everywhere: 0.10 to 0.12 in the high mountains, above their 0.08, and 0.08 to 0.10 in
    the fen, where floodplain gives way to fen.
- **Inference:** the wood share by how long settled is a design choice ([[D2-184 People in a generated world|D2-184]]'s era). But a region's share should also follow
  what its land can be cleared for. Upland and fen country kept more wood, or more open waste, than the lowland: Domesday's wood
  ran from under 5% in the Fens to over 20% in the Weald.
- **Fix proposed:** the target as a regional mean, and the share by land suitability around it.

**8. Wet ground and blanket bog are too scarce in the wet places.**
- **Evidence:**
  - The upland's wet ground (wetness 0.75 or more) is 5.0 to 5.4% against 8 to 45%. Blanket bog covers 0.09% on seed 1 against
    the Pennines' dominant cover on the tops.
  - The fen basin's wet ground is 15% against 30 to 90%. Its wetland ecosystems are 32 to 35%, just over its promise of 0.3.
  - The wet west's saltmarsh is 0.02%, under its 0.05%.
- **Cause:**
  - wetness is the flow index plus a small rain-surplus term, and the tops are steep after the roughness, so bog's `slope < 4` is
    seldom met;
  - the fen is wet only within its disc;
  - saltmarsh needs land under 3 m within 1 km of the sea, which a cliffy western coast rarely gives.
- **Fix proposed:**
  - wetness with a rain-surplus term that grows on the wet tops (peat forms where rain exceeds evaporation by about 1,000 mm,
    whatever the slope up to about 15°);
  - a fen's wetness over its whole basin;
  - saltmarsh in the coast's sheltered bays (the coast's `ragged` inlets).

**9. A laid lake comes out any size.**
- **Evidence:**
  - The same lake primitive (r 0.06) at the same place held 0, 0.9, 1.2, 1.4, 1.5, 31.5 and 37.2 km² on different seeds and
    placements.
  - On the fells' flank it never held: the land falls 200 m across it, and the primitive only digs a 25 m bump.
- **Built:** the laid lake is now kept outside the lake cap (section 1).
- **Fix proposed (not built):** a lake primitive that sets a water level and a rim, so the file says how big the lake is.

**10. Upland lakes are too many and too large.**
- **Evidence:**
  - Every upland world reaches the lake cap: 10 lakes of 1.3 to 17 km², 1.0 to 2.4% of the land. The Pennines have a few natural
    tarns, mostly under 0.1 km².
  - The cap is per 1,000 km² of land that makes lakes, and the largest hollows win.
- **Fix proposed:** a tarn's size limited by the hollow's catchment and depth (`lake_m` by area), and the cap's share lower in
  the uplands than in a fen or a lake district.

**11. Every village farms the same plots of floodplain clay.**
- **Evidence:**
  - 69 of the suite's 72 villages farm river floodplain only, and 66 farm clay. Their fertility is 1.09 to 1.37, on the sand
    country, on the chalk and in the fen alike.
  - Each village has 6 plots, or 10 for the one village a seed draws more households for: the same village, seed 2's `s1`, in
    every world.
  - In the capacity model's `worked` level, 426 of the suite's 480 field plots are clay floodplain.
- **Cause:**
  - the site score weighs fertility (3.0) and water (2.0);
  - the fields are taken by cost less twice the fertility, and the floodplain's silt (x 1.25) on clay (x 1.1) is the most
    fertile ground anywhere;
  - the plot count is fixed by the households (three of three people), not by the land.
- **So:** the soils the suite varies never reach the arable. Sand, chalk and peat show only in the wild land; the arable's food a
  plot does not tell the Brecks from the Midlands.
- **Fix proposed:**
  - sites spread over the land's kinds (a village of the downs on the chalk, of the sand on the sand);
  - fields taken by a farmer's preference (a light soil that drains, near the village) rather than the most fertile ground;
  - plots sized by the land's fertility.

**Not a fault, for the record:**
- The tree line in the uplands (550 to 625 m), the cold north's and the mountains' mean temperatures, and the sand's water held
  (79 mm against the clay's 171) all come out as expected.
- So do heath on the sand (11 to 13%), the estuary's saltmarsh (0.7 to 0.8%), the downs drier than the vale, and the
  mountains' arable ground under the lowland's.

## 6. What the suite could not check yet

- **Frost, snow, wind and wet days in the generator's column:** the generator has a year's mean temperature and a year's rain,
  nothing seasonal or daily. Its column carries only those two. The frost ordering reads the mean as a stand-in.
- **Ice on a large lake that freezes last (row 12):** 02zzn's ice has no depth or size of water. Ice days are read on the
  villages' weather.
- **The runs (salmon, lamprey):** they live in the runs' own store (`wild/runs.py`), not in the populations read here.
- **Densities of the kinds against real places:** only presence and the settling against `ref` are read. The ecology's densities
  wait until the weather and the covers differ by world.

## 7. Across the twelve: nutrition, wildlife, weather and its likelihood, environments

Zach (20 Nov): "The calibration should look how different sources of nutrition, different wildlife, different weather conditions
and likelihood, different world environments (e.g. soil types etc.) all vary across these worlds." Measured with the engine's own
models offline (`02zzt_nutrition.py`: the capacity model, [[D4-102 Carrying capacity is measured, by level, from the engine's own rules|D4-102]], and 02zzd's harness of the acts); the reading is in section 8.

<!-- widened:begin (written by 02zzt_calibration_suite.py) -->

### Sources of nutrition: the land's year at the villages (the capacity model)

The mean over each world's three villages. People supported by level (bare: wild food only, raw; standing: the fields as they are; worked: the best crops and fallow, broken, weeded, manured; best: all the world's techniques reach). Food a unit of work and people fed by that source alone a year, at `worked` (the village's land is sized for nine people: [[D2-161 Seed nodes below what they sustain|D2-161]]'s 60 to 70% of capacity). The share lost in store is preserving's effect, from the house store (standing) to the best store the world reaches.

| World | seed | supported: bare / standing / worked / best | fields | herds | wild plants | game | fish | lost in store: standing → best |
|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country | 1 | 0.78 / 6.04 / 23 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.65 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0493 → 0.0107 |
| w01 Lowland river country | 2 | 0.953 / 7.28 / 23 / 31 | 0.77 a unit, 21.5 fed | 1.60 a unit, 1.7 fed | 0.61 a unit, 0.7 fed | 0.16 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0453 → 0.00967 |
| w02 Dry east | 1 | 0.71 / 5.87 / 22 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.83 a unit, 0.8 fed | 0.05 → 0.0107 |
| w02 Dry east | 2 | 0.803 / 7.09 / 24 / 32 | 0.80 a unit, 22.2 fed | 1.60 a unit, 1.7 fed | 0.64 a unit, 0.7 fed | 0.14 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0487 → 0.0103 |
| w03 Wet west, maritime | 1 | 0.78 / 6.04 / 23 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.049 → 0.0107 |
| w03 Wet west, maritime | 2 | 0.883 / 7.28 / 24 / 32 | 0.80 a unit, 22.2 fed | 1.60 a unit, 1.7 fed | 0.61 a unit, 0.7 fed | 0.16 a unit, 0.2 fed | 0.83 a unit, 0.9 fed | 0.0477 → 0.0103 |
| w04 Coast under mountains | 1 | 0.857 / 6.25 / 31 / 43 | 1.17 a unit, 30.2 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.17 a unit, 0.2 fed | 0.83 a unit, 0.9 fed | 0.0477 → 0.01 |
| w04 Coast under mountains | 2 | 0.953 / 7.5 / 33 / 45 | 1.09 a unit, 31.7 fed | 1.60 a unit, 1.7 fed | 0.64 a unit, 0.7 fed | 0.20 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0463 → 0.00967 |
| w05 Upland and moor | 1 | 0.78 / 6.09 / 31 / 42 | 1.17 a unit, 30.2 fed | 1.65 a unit, 1.5 fed | 0.63 a unit, 0.7 fed | 0.17 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0487 → 0.01 |
| w05 Upland and moor | 2 | 0.803 / 7.07 / 32 / 44 | 1.07 a unit, 31.2 fed | 1.60 a unit, 1.7 fed | 0.63 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.83 a unit, 1.1 fed | 0.0483 → 0.01 |
| w06 High mountains | 1 | 0.93 / 6.17 / 30 / 41 | 1.13 a unit, 28.7 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.17 a unit, 0.2 fed | 0.83 a unit, 1.1 fed | 0.0453 → 0.01 |
| w06 High mountains | 2 | 0.803 / 7.16 / 33 / 45 | 1.09 a unit, 31.7 fed | 1.60 a unit, 1.7 fed | 0.62 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.83 a unit, 1.1 fed | 0.0487 → 0.01 |
| w07 Cold north | 1 | 0.63 / 5.7 / 22 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.65 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0513 → 0.0107 |
| w07 Cold north | 2 | 0.813 / 7.11 / 24 / 32 | 0.80 a unit, 22.2 fed | 1.60 a unit, 1.7 fed | 0.63 a unit, 0.7 fed | 0.16 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.049 → 0.0103 |
| w08 Fen basin | 1 | 0.78 / 6.04 / 23 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.65 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.049 → 0.0107 |
| w08 Fen basin | 2 | 0.807 / 7.01 / 25 / 33 | 0.82 a unit, 23.3 fed | 1.60 a unit, 1.7 fed | 0.64 a unit, 0.7 fed | 0.16 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.048 → 0.01 |
| w09 Estuary and saltmarsh | 1 | 0.93 / 6.37 / 23 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0467 → 0.0107 |
| w09 Estuary and saltmarsh | 2 | 0.803 / 7.04 / 23 / 31 | 0.79 a unit, 22.0 fed | 1.60 a unit, 1.7 fed | 0.62 a unit, 0.7 fed | 0.14 a unit, 0.2 fed | 0.83 a unit, 1.1 fed | 0.0483 → 0.0103 |
| w10 Chalk and clay | 1 | 0.93 / 6.37 / 23 / 30 | 0.89 a unit, 21.2 fed | 1.65 a unit, 1.5 fed | 0.65 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0467 → 0.0107 |
| w10 Chalk and clay | 2 | 0.953 / 7.44 / 24 / 32 | 0.80 a unit, 22.2 fed | 1.60 a unit, 1.7 fed | 0.62 a unit, 0.7 fed | 0.16 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0463 → 0.01 |
| w11 Sand and heath | 1 | 0.62 / 5.61 / 22 / 29 | 0.87 a unit, 20.8 fed | 1.65 a unit, 1.5 fed | 0.63 a unit, 0.7 fed | 0.15 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0513 → 0.0107 |
| w11 Sand and heath | 2 | 0.783 / 7.01 / 23 / 31 | 0.79 a unit, 22.0 fed | 1.60 a unit, 1.7 fed | 0.59 a unit, 0.7 fed | 0.14 a unit, 0.2 fed | 0.83 a unit, 1.1 fed | 0.0487 → 0.0103 |
| w12 Lake country | 1 | 0.78 / 6.05 / 31 / 42 | 1.17 a unit, 30.1 fed | 1.65 a unit, 1.5 fed | 0.64 a unit, 0.7 fed | 0.17 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.049 → 0.01 |
| w12 Lake country | 2 | 0.67 / 6.75 / 32 / 44 | 1.07 a unit, 31.2 fed | 1.60 a unit, 1.7 fed | 0.64 a unit, 0.7 fed | 0.20 a unit, 0.2 fed | 0.82 a unit, 1.1 fed | 0.0507 → 0.01 |

### Sources of nutrition: the acts, food a unit of work (02zzd's harness, autumn, a probe person, fresh copies)

At one village a world (the one with the most water). Hunting the wild armed, at the hunt's curve: novice x1, capable x3, master x8 (20 tries a cell); gathering, fishing and the water traps at the basic curve's novice, middle and top (12 tries). n / c / m: novice / capable / master. `-`: no such ground at the village. The break-even is the food a unit that keeps a household (1.5 eaters a worker).

| World | seed | village | hunt near | hunt the wood around | hunt far | gather (wood) | gather (open) | eel traps | nets | fish by hand | angle | break-even |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country | 1 | s2 | 0.172 / 0.131 / 0.986 | 0.34 / 0.672 / 2.25 | 0.62 / 1.66 / 1.9 | 1.13 / 1.64 / 1.8 | 1.17 / 1.51 / 1.69 | 0.033 / 0.067 / 0.067 | 0.019 / 0 / 0.056 | 0.58 / 0.735 / 0.861 | 1.58 / 2.22 / 2.33 | 0.25 |
| w01 Lowland river country | 2 | s1 | 0.079 / 0.172 / 0.949 | 0.14 / 0.622 / 2.42 | 0.897 / 1.39 / 1.85 | 1.17 / 1.39 / 1.95 | 1.19 / 1.41 / 1.69 | 0.017 / 0.1 / 0.05 | 0 / 0.037 / 0.025 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w02 Dry east | 1 | s1 | 0.03 / 0.109 / 0.656 | 0.855 / 0.728 / 3.02 | 0.364 / 1.31 / 1.58 | 1.23 / 1.42 / 1.84 | 1.19 / 1.5 / 1.71 | 0 / 0.05 / 0.067 | 0.006 / 0.037 / 0.006 | 0.614 / 0.8 / 1.03 | 1.47 / 1.75 / 2.26 | 0.25 |
| w02 Dry east | 2 | s1 | 0.131 / 0.229 / 1.03 | 0.157 / 0.66 / 2.73 | 0.657 / 1.08 / 1.72 | 1.17 / 1.39 / 1.95 | 1.19 / 1.41 / 1.7 | 0.017 / 0.067 / 0.05 | 0.006 / 0.037 / 0.05 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w03 Wet west, maritime | 1 | s2 | 0.195 / 0.131 / 0.821 | 0.452 / 0.515 / 2.47 | 0.219 / 1.25 / 2.11 | 1.13 / 1.63 / 1.8 | 1.05 / 1.41 / 1.69 | 0.05 / 0.117 / 0.104 | 0.019 / 0 / 0.056 | 0.58 / 0.735 / 0.861 | 1.58 / 2.22 / 2.33 | 0.25 |
| w03 Wet west, maritime | 2 | s1 | 0.131 / 0.199 / 0.983 | 0.14 / 0.415 / 3.06 | 0.882 / 1.39 / 1.81 | 1.17 / 1.39 / 1.95 | 1.19 / 1.41 / 1.69 | 0.033 / 0.083 / 0.05 | 0.006 / 0.037 / 0.05 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w04 Coast under mountains | 1 | s2 | 0.008 / 0.131 / 1.12 | 0.375 / 0.84 / 2.23 | 0.42 / 1.36 / 1.8 | 1.13 / 1.63 / 1.8 | 1.05 / 1.41 / 1.68 | 0.033 / 0.067 / 0.067 | 0.019 / 0.006 / 0.081 | 0.58 / 0.735 / 0.861 | 1.58 / 2.22 / 2.33 | 0.25 |
| w04 Coast under mountains | 2 | s1 | 0.079 / 0.172 / 0.949 | 0.157 / 0.467 / 2.69 | 0.986 / 1.34 / 1.81 | 1.17 / 1.39 / 1.95 | 1.19 / 1.41 / 1.69 | 0.017 / 0.033 / 0.067 | 0 / 0.037 / 0.025 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w05 Upland and moor | 1 | s1 | 0.026 / 0.082 / 0.634 | 0.647 / 0.735 / 2.62 | 0.306 / 0.594 / 1.59 | 1.22 / 1.42 / 1.84 | 1.19 / 1.51 / 1.71 | 0.067 / 0.017 / 0 | 0.006 / 0.037 / 0.006 | 0.614 / 0.8 / 1.03 | 1.47 / 1.75 / 2.26 | 0.25 |
| w05 Upland and moor | 2 | s1 | 0.105 / 0.086 / 1.04 | 0.07 / 0.682 / 2.6 | 0.621 / 1.33 / 1.77 | 1.21 / 1.5 / 1.75 | 1.18 / 1.4 / 1.68 | 0.033 / 0.017 / 0.05 | 0.031 / 0.037 / 0.05 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w06 High mountains | 1 | s1 | 0.199 / 0.109 / 0.656 | 0.985 / 0.925 / 2.89 | 0.34 / 0.402 / 1.24 | 1.21 / 1.61 / 1.83 | 1.01 / 1.5 / 1.57 | 0.05 / 0.05 / 0.104 | 0.019 / 0 / 0.044 | 0.703 / 0.782 / 0.971 | 1.48 / 1.93 / 1.88 | 0.25 |
| w06 High mountains | 2 | s1 | 0.03 / 0.382 / 1.34 | 0.525 / 1.11 / 2.87 | 0.469 / 1.22 / 1.73 | 1.12 / 1.41 / 1.72 | 1.17 / 1.36 / 1.46 | 0.017 / 0.017 / 0.05 | 0 / 0.037 / 0.038 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w07 Cold north | 1 | s3 | 0.221 / 0.056 / 0.664 | 0.152 / 0.485 / 2.55 | 0.312 / 0.922 / 1.79 | 1.22 / 1.58 / 1.69 | 1.14 / 1.39 / 1.8 | 0.017 / 0.083 / 0.033 | 0.019 / 0.019 / 0.056 | 0.477 / 0.68 / 0.99 | 1.66 / 1.64 / 2.22 | 0.25 |
| w07 Cold north | 2 | s1 | 0.079 / 0.416 / 1.35 | 0.182 / 0.868 / 2.88 | 0.368 / 1.22 / 2.12 | 1.2 / 1.55 / 1.72 | 1.23 / 1.42 / 1.68 | 0 / 0.033 / 0.033 | 0 / 0 / 0.044 | 0.623 / 0.771 / 1.13 | 1.44 / 1.92 / 2.31 | 0.25 |
| w08 Fen basin | 1 | s1 | 0.199 / 0.082 / 0.817 | 0.647 / 0.612 / 2.91 | 0.471 / 0.913 / 1.67 | 1.23 / 1.42 / 1.84 | 1.19 / 1.51 / 1.71 | 0 / 0.05 / 0.067 | 0.006 / 0.037 / 0.006 | 0.614 / 0.8 / 1.03 | 1.47 / 1.75 / 2.26 | 0.25 |
| w08 Fen basin | 2 | s2 | 0.026 / 0.101 / 0.945 | 0.393 / 0.835 / 2.93 | 0.412 / 0.975 / 1.79 | 1.14 / 1.53 / 1.94 | 1.11 / 1.28 / 1.73 | 0.133 / 0.133 / 0.2 | 0 / 0.025 / 0.081 | 0.546 / 0.819 / 0.792 | 1.64 / 2.2 / 2.03 | 0.25 |
| w09 Estuary and saltmarsh | 1 | s1 | 0.026 / 0.109 / 0.656 | 0.665 / 1.04 / 2.66 | 0.344 / 1.06 / 1.34 | 1.23 / 1.42 / 1.84 | 1.19 / 1.51 / 1.71 | 0 / 0.05 / 0.087 | 0.006 / 0.056 / 0.006 | 0.614 / 0.8 / 1.03 | 1.47 / 1.75 / 2.26 | 0.25 |
| w09 Estuary and saltmarsh | 2 | s1 | 0.079 / 0.131 / 0.818 | 0.07 / 0.652 / 3.19 | 0.46 / 1.35 / 1.67 | 1.2 / 1.55 / 1.98 | 1.11 / 1.3 / 1.56 | 0 / 0.033 / 0.017 | 0 / 0 / 0.019 | 0.631 / 0.703 / 0.811 | 1.56 / 1.97 / 2.22 | 0.25 |
| w10 Chalk and clay | 1 | s1 | 0.052 / 0.165 / 0.96 | 0.95 / 0.807 / 2.89 | 0.375 / 1.36 / 1.99 | 1.23 / 1.42 / 1.84 | 1.19 / 1.51 / 1.71 | 0 / 0.033 / 0.05 | 0.006 / 0.006 / 0 | 0.614 / 0.8 / 1.03 | 1.47 / 1.75 / 2.26 | 0.25 |
| w10 Chalk and clay | 2 | s1 | 0.03 / 0.33 / 0.836 | 0.395 / 0.83 / 2.89 | 0.508 / 1.09 / 1.82 | 1.11 / 1.41 / 1.71 | 1.17 / 1.42 / 1.73 | 0.017 / 0.067 / 0.05 | 0.006 / 0.037 / 0.044 | 0.611 / 0.866 / 0.848 | 1.73 / 1.45 / 2.43 | 0.25 |
| w11 Sand and heath | 1 | s2 | 0.034 / 0.187 / 0.679 | 0.357 / 0.862 / 2.15 | 0.463 / 1.09 / 1.89 | 1.13 / 1.63 / 1.8 | 1.02 / 1.36 / 1.62 | 0.033 / 0.05 / 0.05 | 0 / 0.037 / 0.075 | 0.537 / 0.856 / 0.958 | 1.56 / 1.92 / 2.3 | 0.25 |
| w11 Sand and heath | 2 | s1 | 0 / 0.412 / 1.32 | 0.68 / 0.75 / 2.72 | 0.538 / 1.16 / 2.18 | 1.28 / 1.47 / 1.76 | 1.19 / 1.34 / 1.45 | 0.017 / 0.067 / 0.067 | 0 / 0.044 / 0.062 | 0.574 / 0.547 / 0.98 | 1.39 / 1.81 / 1.95 | 0.25 |
| w12 Lake country | 1 | s2 | 0.008 / 0.157 / 0.836 | 0.305 / 0.652 / 2.33 | 0.364 / 0.973 / 1.87 | 1.13 / 1.63 / 1.79 | 1.01 / 1.36 / 1.62 | 0.017 / 0.05 / 0.117 | 0.019 / 0.006 / 0.081 | 0.58 / 0.735 / 0.861 | 1.58 / 2.22 / 2.33 | 0.25 |
| w12 Lake country | 2 | s1 | 0.086 / 0.094 / 1.15 | 0.18 / 0.822 / 2.76 | 0.235 / 1.44 / 1.59 | 1.16 / 1.37 / 1.74 | 1.16 / 1.4 / 1.72 | 0.05 / 0.017 / 0.05 | 0 / 0.044 / 0.075 | 0.574 / 0.547 / 0.98 | 1.39 / 1.81 / 1.95 | 0.25 |

### Sources of nutrition: what could feed a village alone, and the runs

A source that returns the break-even or more and gives the village's nine people a year, for good: the land's sources at `worked`; hunting from the wild land's yearly growth in reach (each hunted kind's heads after the history x a quarter of its b - m x its food a head: the logistic's most sustainable take r K / 4, an upper bound) at the master's return there; the runs from the food that passes the villages. The runs: heads at the villages' water a year (the sum over the days a run stands there, `wild/runs.py`) and the food they are worth (salmon 2 fish, lamprey 0.3 meat, an eel 0.2 fish a head: `wild/kinds.py` TAKEN; ITEMS food: meat 1.5, fish 1), the mean over the villages.

| World | seed | could feed a village of nine alone | hunting a year in reach, people fed (the wood around / far) | the runs at the villages a year |
|---|---|---|---|---|
| w01 Lowland river country | 1 | fields (21 fed), hunting the wood around (28 fed), hunting far (446 fed) | 28 / 446 | eel 27 heads, 5 food; salmon 6 heads, 13 food |
| w01 Lowland river country | 2 | fields (21 fed), hunting the wood around (34 fed), hunting far (336 fed) | 34 / 336 | eel 9 heads, 2 food; lamprey 18 heads, 8 food; salmon 6 heads, 13 food |
| w02 Dry east | 1 | fields (21 fed), hunting the wood around (29 fed), hunting far (444 fed) | 29 / 444 | eel 8 heads, 2 food; salmon 3 heads, 7 food |
| w02 Dry east | 2 | fields (22 fed), hunting the wood around (35 fed), hunting far (367 fed) | 35 / 367 | eel 9 heads, 2 food; lamprey 14 heads, 6 food; salmon 6 heads, 12 food |
| w03 Wet west, maritime | 1 | fields (21 fed), hunting the wood around (29 fed), hunting far (406 fed) | 29 / 406 | eel 19 heads, 4 food; salmon 7 heads, 14 food |
| w03 Wet west, maritime | 2 | fields (22 fed), hunting the wood around (34 fed), hunting far (413 fed) | 34 / 413 | eel 11 heads, 2 food; lamprey 21 heads, 10 food; salmon 7 heads, 14 food |
| w04 Coast under mountains | 1 | fields (30 fed), hunting the wood around (28 fed), hunting far (316 fed) | 28 / 316 | eel 18 heads, 4 food; lamprey 9 heads, 4 food; salmon 9 heads, 17 food |
| w04 Coast under mountains | 2 | fields (32 fed), hunting the wood around (31 fed), hunting far (321 fed) | 31 / 321 | eel 18 heads, 4 food; lamprey 16 heads, 7 food; salmon 7 heads, 15 food |
| w05 Upland and moor | 1 | fields (30 fed), hunting the wood around (37 fed), hunting far (395 fed) | 37 / 395 | eel 13 heads, 3 food; salmon 4 heads, 9 food |
| w05 Upland and moor | 2 | fields (31 fed), hunting the wood around (33 fed), hunting far (416 fed) | 33 / 416 | eel 141 heads, 28 food; lamprey 7 heads, 3 food; salmon 2 heads, 4 food |
| w06 High mountains | 1 | fields (29 fed), hunting the wood around (29 fed), hunting far (357 fed) | 29 / 357 | eel 14 heads, 3 food; salmon 8 heads, 17 food |
| w06 High mountains | 2 | fields (32 fed), hunting the wood around (33 fed), hunting far (401 fed) | 33 / 401 | eel 10 heads, 2 food; lamprey 14 heads, 6 food; salmon 7 heads, 14 food |
| w07 Cold north | 1 | fields (21 fed), hunting the wood around (28 fed), hunting far (300 fed) | 28 / 300 | eel 17 heads, 3 food; salmon 9 heads, 17 food |
| w07 Cold north | 2 | fields (22 fed), hunting the wood around (34 fed), hunting far (326 fed) | 34 / 326 | eel 10 heads, 2 food; lamprey 22 heads, 10 food; salmon 9 heads, 17 food |
| w08 Fen basin | 1 | fields (21 fed), hunting the wood around (30 fed), hunting far (381 fed) | 30 / 381 | eel 9 heads, 2 food; lamprey 1 heads, 0 food; salmon 3 heads, 6 food |
| w08 Fen basin | 2 | fields (23 fed), hunting the wood around (37 fed), hunting far (374 fed) | 37 / 374 | eel 95 heads, 19 food; lamprey 10 heads, 4 food; salmon 10 heads, 20 food |
| w09 Estuary and saltmarsh | 1 | fields (21 fed), hunting the wood around (30 fed), hunting far (336 fed) | 30 / 336 | eel 13 heads, 3 food; salmon 4 heads, 8 food |
| w09 Estuary and saltmarsh | 2 | fields (22 fed), hunting the wood around (34 fed), hunting far (347 fed) | 34 / 347 | eel 12 heads, 2 food; lamprey 6 heads, 3 food; salmon 6 heads, 13 food |
| w10 Chalk and clay | 1 | fields (21 fed), hunting the wood around (28 fed), hunting far (310 fed) | 28 / 310 | eel 32 heads, 6 food; salmon 7 heads, 14 food |
| w10 Chalk and clay | 2 | fields (22 fed), hunting the wood around (35 fed), hunting far (393 fed) | 35 / 393 | eel 22 heads, 4 food; lamprey 13 heads, 6 food; salmon 7 heads, 13 food |
| w11 Sand and heath | 1 | fields (21 fed), hunting the wood around (29 fed), hunting far (268 fed) | 29 / 268 | eel 7 heads, 1 food; salmon 6 heads, 13 food |
| w11 Sand and heath | 2 | fields (22 fed), hunting the wood around (34 fed), hunting far (317 fed) | 34 / 317 | eel 11 heads, 2 food; lamprey 19 heads, 8 food; salmon 6 heads, 13 food |
| w12 Lake country | 1 | fields (30 fed), hunting the wood around (27 fed), hunting far (361 fed) | 27 / 361 | eel 18 heads, 4 food; salmon 11 heads, 22 food |
| w12 Lake country | 2 | fields (31 fed), hunting the wood around (33 fed), hunting far (478 fed) | 33 / 478 | eel 148 heads, 30 food; lamprey 5 heads, 2 food; salmon 2 heads, 5 food |

### Arable by soil and ground, pooled over the suite (the capacity model, `worked`)

| Soil / ground | plots in the suite | food a plot a year | worlds |
|---|---|---|---|
| clay / clay vale | 18 | 132.9 | w01, w06 |
| loam / river floodplain | 36 | 122.5 | w05, w08, w09, w11, w12 |
| clay / river floodplain | 426 | 117.3 | w01, w02, w03, w04, w05, w06, w07, w08, w09, w10, w11, w12 |

### Wildlife: densities a km² over the whole land (each year's highest season, the mean over the suite's years)

Where: the share of a kind's heads (after the history) on wood, grass, heath, wet ground and water, by its areas' features (pooled over the suite in the last table). Flags: a kind absent where its range includes the land, or one running away (section Collapse and the ecology settling above).

| World | seed | red deer | roe deer | wild boar | brown hare | wildfowl | eel | otter | fox | wolf | brown bear | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country | 1 | 2.33 | 8.03 | 1.27 | 55 | 7.59 | 5.72 | 0.183 | 1.28 | 0.0392 | 0.0636 | none |
| w01 Lowland river country | 2 | 2.2 | 7.56 | 1.2 | 57 | 8.31 | 6.22 | 0.175 | 1.24 | 0.0372 | 0.0483 | none |
| w02 Dry east | 1 | 2.29 | 7.86 | 1.2 | 57 | 4.28 | 3.27 | 0.181 | 1.26 | 0.0385 | 0.0579 | none |
| w02 Dry east | 2 | 2.27 | 7.8 | 1.21 | 58 | 5.19 | 3.97 | 0.183 | 1.26 | 0.0382 | 0.0608 | none |
| w03 Wet west, maritime | 1 | 2.25 | 7.76 | 1.25 | 55 | 10 | 7.87 | 0.178 | 1.25 | 0.0379 | 0.0571 | none |
| w03 Wet west, maritime | 2 | 2.21 | 7.67 | 1.25 | 57 | 11 | 8.44 | 0.197 | 1.24 | 0.0374 | 0.0499 | none |
| w04 Coast under mountains | 1 | 2.28 | 7.31 | 1.21 | 45 | 8.28 | 6.27 | 0.164 | 1.23 | 0.0408 | 0.0566 | none |
| w04 Coast under mountains | 2 | 2.25 | 7.18 | 1.2 | 46 | 9.13 | 6.86 | 0.18 | 1.22 | 0.0405 | 0.049 | none |
| w05 Upland and moor | 1 | 2.25 | 6.98 | 1.17 | 45 | 8.87 | 7.26 | 0.194 | 1.21 | 0.0412 | 0.0557 | none |
| w05 Upland and moor | 2 | 2.31 | 7.26 | 1.21 | 44 | 13 | 11 | 0.209 | 1.23 | 0.0418 | 0.0606 | none |
| w06 High mountains | 1 | 2.36 | 6.76 | 1.21 | 39 | 10 | 8.17 | 0.199 | 1.22 | 0.0453 | 0.0602 | none |
| w06 High mountains | 2 | 2.33 | 6.96 | 1.2 | 38 | 14 | 11 | 0.223 | 1.21 | 0.044 | 0.0605 | none |
| w07 Cold north | 1 | 2.31 | 7.94 | 1.25 | 56 | 7.44 | 5.65 | 0.18 | 1.27 | 0.039 | 0.0604 | none |
| w07 Cold north | 2 | 2.21 | 7.59 | 1.2 | 56 | 8.19 | 6.15 | 0.174 | 1.24 | 0.0377 | 0.0472 | none |
| w08 Fen basin | 1 | 2.15 | 6.9 | 1.65 | 41 | 48 | 36 | 0.221 | 1.21 | 0.038 | 0.0556 | none |
| w08 Fen basin | 2 | 2.17 | 7.19 | 1.71 | 43 | 52 | 39 | 0.231 | 1.23 | 0.0382 | 0.0587 | none |
| w09 Estuary and saltmarsh | 1 | 2.23 | 7.49 | 1.48 | 47 | 29 | 22 | 0.204 | 1.24 | 0.0389 | 0.0629 | none |
| w09 Estuary and saltmarsh | 2 | 2.17 | 7.35 | 1.4 | 48 | 28 | 21 | 0.197 | 1.22 | 0.0372 | 0.0502 | none |
| w10 Chalk and clay | 1 | 2.12 | 7.47 | 1.19 | 60 | 5.62 | 4.29 | 0.189 | 1.25 | 0.038 | 0.0645 | none |
| w10 Chalk and clay | 2 | 2.18 | 7.67 | 1.22 | 60 | 6.48 | 4.89 | 0.185 | 1.26 | 0.0382 | 0.065 | none |
| w11 Sand and heath | 1 | 2.18 | 7.14 | 1.12 | 48 | 4.18 | 3.23 | 0.172 | 1.23 | 0.0417 | 0.0525 | none |
| w11 Sand and heath | 2 | 2.16 | 7.31 | 1.18 | 52 | 4.97 | 3.71 | 0.18 | 1.25 | 0.0419 | 0.0674 | none |
| w12 Lake country | 1 | 2.26 | 7 | 1.2 | 44 | 12 | 9.33 | 0.209 | 1.21 | 0.0411 | 0.0562 | none |
| w12 Lake country | 2 | 2.27 | 7.07 | 1.21 | 44 | 20 | 16 | 0.233 | 1.2 | 0.0412 | 0.0592 | none |

| Kind | where its heads are (wood / grass / heath / wet / water / farmed), the mean over the suite |
|---|---|
| red deer | 0.293 / 0.579 / 0.0524 / 0.078 / 0.0168 / 0.0622 |
| roe deer | 0.372 / 0.533 / 0.0303 / 0.0657 / 0.0134 / 0.0497 |
| wild boar | 0.493 / 0.424 / 0.0322 / 0.082 / 0.0122 / 0.021 |
| brown hare | 0.17 / 0.717 / 0.0157 / 0.0831 / 0.019 / 0.113 |
| woodpigeon | 0.369 / 0.477 / 0.0208 / 0.0789 / 0.0224 / 0.179 |
| rats | 0.103 / 0.51 / 0.00254 / 0.128 / 0.0467 / 0.686 |
| wildfowl | 0 / 0 / 0 / 0 / 0 / 0 |
| eel | 0.204 / 0.491 / 0.0407 / 0.193 / 0.0556 / 0.186 |
| salmon | 0 / 0 / 0 / 0 / 0 / 0 |
| lamprey | 0 / 0 / 0 / 0 / 0 / 0 |
| otter | 0.264 / 0.578 / 0.0337 / 0.126 / 0.0314 / 0.0848 |
| voles and mice | 0.255 / 0.577 / 0.0374 / 0.0899 / 0.0204 / 0.151 |
| owls | 0.303 / 0.525 / 0.0317 / 0.0868 / 0.0212 / 0.183 |
| fox | 0.294 / 0.58 / 0.0392 / 0.0824 / 0.017 / 0.0877 |
| stoat | 0.289 / 0.568 / 0.0393 / 0.0855 / 0.0184 / 0.113 |
| wolf | 0.366 / 0.518 / 0.0598 / 0.0721 / 0.016 / 0.0388 |
| raven | 0.247 / 0.612 / 0.0455 / 0.0889 / 0.018 / 0.0853 |
| brown bear | 0.663 / 0.301 / 0.0247 / 0.0302 / 0.00854 / 0.0621 |

### Weather and its likelihood, a real year at the villages

The engine's weather (`climate.py`): the share of days of each weather type (Lamb's), the days a year of each label it gives, and the storms. The water on the engine's weather (02zzn, two clocks). The generator's climate holds a year's rain and mean only. The engine reads only height, so the rows of one seed differ only by the villages' heights (the known gap, OPEN [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]]).

| World | seed | types: settled / westerly / cyclonic / northerly / easterly / storm | clear / rain / heavy rain / fog / snow / gale days | wet days | frost nights | storm days | snow lying | rain between years (CV) | spates / floods a year | flood years | low water | ice days | generator: rain mm, mean °C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 187 / 123 / 12 / 18 / 13 / 12 | 129 | 71 | 17 | 10 | 0.47 | 1.67 / 0.85 | 0.7 | 0.428 | 8.73 | 747, 8.68 |
| w01 Lowland river country | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 155 / 137 / 20 / 22 / 17 / 15 | 150 | 68 | 26 | 13 | 0.54 | 1.75 / 0.75 | 0.65 | 0.404 | 9.13 | 752, 8.43 |
| w02 Dry east | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 188 / 122 / 11 / 17 / 14 / 13 | 129 | 70 | 17 | 9.87 | 0.46 | 1.58 / 0.9 | 0.683 | 0.423 | 8.93 | 400, 9.32 |
| w02 Dry east | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 156 / 136 / 20 / 22 / 16 / 15 | 148 | 68 | 26 | 13 | 0.54 | 1.68 / 0.8 | 0.667 | 0.405 | 8.57 | 428, 9.61 |
| w03 Wet west, maritime | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 187 / 122 / 12 / 18 / 14 / 12 | 129 | 71 | 16 | 10 | 0.47 | 1.6 / 0.933 | 0.717 | 0.416 | 9.13 | 1244, 9.57 |
| w03 Wet west, maritime | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 155 / 137 / 20 / 22 / 16 / 15 | 151 | 68 | 26 | 12 | 0.54 | 1.6 / 0.767 | 0.65 | 0.406 | 9.13 | 1112, 9.45 |
| w04 Coast under mountains | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 185 / 125 / 13 / 18 / 13 / 11 | 131 | 71 | 17 | 10 | 0.46 | 1.77 / 0.867 | 0.717 | 0.418 | 9.3 | 971, 8.7 |
| w04 Coast under mountains | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 156 / 137 / 20 / 20 / 17 / 16 | 152 | 69 | 26 | 13 | 0.55 | 1.5 / 0.55 | 0.583 | 0.405 | 9.9 | 1064, 8.42 |
| w05 Upland and moor | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 184 / 124 / 12 / 17 / 16 / 12 | 132 | 73 | 17 | 12 | 0.46 | 1.55 / 0.95 | 0.7 | 0.421 | 11 | 755, 8.6 |
| w05 Upland and moor | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 155 / 140 / 19 / 16 / 18 / 17 | 155 | 70 | 26 | 15 | 0.55 | 0.967 / 0.3 | 0.417 | 0.4 | 9.7 | 1118, 8.56 |
| w06 High mountains | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 181 / 122 / 12 / 24 / 14 / 13 | 130 | 70 | 17 | 10 | 0.46 | 1.57 / 0.917 | 0.7 | 0.42 | 8.57 | 897, 8.45 |
| w06 High mountains | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 154 / 138 / 20 / 20 / 17 / 15 | 152 | 70 | 26 | 14 | 0.53 | 1.78 / 0.667 | 0.633 | 0.417 | 9.7 | 921, 8.16 |
| w07 Cold north | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 183 / 122 / 12 / 23 / 12 / 13 | 128 | 71 | 17 | 10 | 0.47 | 1.78 / 0.9 | 0.683 | 0.434 | 8.93 | 774, 5.44 |
| w07 Cold north | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 160 / 137 / 20 / 15 / 17 / 16 | 151 | 69 | 27 | 13 | 0.54 | 1.75 / 0.817 | 0.65 | 0.408 | 8.97 | 649, 5.69 |
| w08 Fen basin | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 171 / 119 / 14 / 39 / 11 / 11 | 127 | 69 | 16 | 9.13 | 0.47 | 1.75 / 0.867 | 0.683 | 0.421 | 8.53 | 499, 9.94 |
| w08 Fen basin | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 148 / 134 / 19 / 35 / 15 / 14 | 146 | 65 | 27 | 12 | 0.54 | 1.57 / 0.633 | 0.7 | 0.402 | 7.2 | 481, 9.82 |
| w09 Estuary and saltmarsh | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 183 / 122 / 11 / 26 / 14 / 10 | 126 | 68 | 17 | 10 | 0.47 | 1.62 / 0.917 | 0.7 | 0.424 | 7.97 | 666, 9.62 |
| w09 Estuary and saltmarsh | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 149 / 135 / 20 / 32 / 16 / 14 | 148 | 68 | 26 | 11 | 0.55 | 1.62 / 0.667 | 0.633 | 0.41 | 7.63 | 638, 9.85 |
| w10 Chalk and clay | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 178 / 124 / 12 / 22 / 15 / 14 | 133 | 74 | 17 | 12 | 0.47 | 1.32 / 0.583 | 0.567 | 0.418 | 10 | 762, 9.47 |
| w10 Chalk and clay | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 157 / 137 / 19 / 20 / 17 / 15 | 152 | 68 | 26 | 13 | 0.56 | 1.58 / 0.45 | 0.517 | 0.405 | 7.8 | 685, 9.87 |
| w11 Sand and heath | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 186 / 123 / 11 / 18 / 15 / 12 | 130 | 71 | 17 | 12 | 0.46 | 1.45 / 0.917 | 0.733 | 0.42 | 9.33 | 518, 9.33 |
| w11 Sand and heath | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 151 / 137 / 20 / 27 / 16 / 14 | 149 | 68 | 25 | 13 | 0.54 | 1.5 / 0.617 | 0.617 | 0.413 | 8.37 | 548, 9.62 |
| w12 Lake country | 1 | 0.463 / 0.261 / 0.089 / 0.058 / 0.094 / 0.036 | 184 / 124 / 12 / 17 / 15 / 12 | 132 | 73 | 17 | 12 | 0.46 | 1.53 / 0.95 | 0.7 | 0.422 | 11 | 1126, 8.61 |
| w12 Lake country | 2 | 0.4 / 0.28 / 0.183 / 0.066 / 0.036 / 0.036 | 151 / 139 / 19 / 21 / 18 / 17 | 154 | 70 | 26 | 16 | 0.54 | 0.983 / 0.317 | 0.467 | 0.397 | 9.7 | 1209, 8.67 |

At named places of the land (the engine's weather at each place's height; the generator's rain and mean there):

| World | seed | place | generator rain mm (mean), mean °C | engine rain mm, wet days, frost nights, snow lying, wind m/s, ice days |
|---|---|---|---|---|
| w01 Lowland river country | 1 | tops | 764, 8.15 | 870, 134, 76, 18, 6.15, 16 |
| w01 Lowland river country | 2 | tops | 762, 8.33 | 1184, 157, 70, 18, 7.09, 12 |
| w02 Dry east | 1 | tops | 420, 9.36 | 864, 134, 76, 18, 6.18, 16 |
| w02 Dry east | 2 | tops | 420, 9.11 | 1169, 157, 70, 18, 7, 12 |
| w03 Wet west, maritime | 1 | coast | 3506, 9.58 | 821, 127, 71, 16, 5.65, 12 |
| w03 Wet west, maritime | 1 | tops | 1188, 9.14 | 938, 140, 78, 11, 6.07, 11 |
| w03 Wet west, maritime | 2 | coast | 3595, 9.64 | 1140, 152, 66, 14, 6.29, 8.6 |
| w03 Wet west, maritime | 2 | tops | 1184, 9.33 | 1127, 162, 78, 16, 7.03, 12 |
| w04 Coast under mountains | 1 | coast | 2985, 8.56 | 832, 127, 71, 16, 5.71, 12 |
| w04 Coast under mountains | 1 | fells | 2185, 5.8 | 1063, 163, 119, 43, 9.27, 50 |
| w04 Coast under mountains | 1 | lee | 1023, 8.39 | 844, 130, 71, 5.7, 5.79, 8.6 |
| w04 Coast under mountains | 1 | tops | 1924, 4.84 | 1074, 166, 137, 56, 10, 71 |
| w04 Coast under mountains | 1 | windward | 1939, 8.57 | 848, 129, 71, 12, 5.7, 11 |
| w04 Coast under mountains | 2 | coast | 3079, 8.65 | 1140, 152, 66, 14, 6.32, 8.6 |
| w04 Coast under mountains | 2 | fells | 2028, 5.85 | 1209, 180, 114, 40, 10, 34 |
| w04 Coast under mountains | 2 | lee | 1010, 8.4 | 1096, 145, 70, 12, 6.63, 9.1 |
| w04 Coast under mountains | 2 | tops | 1794, 4.95 | 1235, 187, 133, 69, 12, 62 |
| w04 Coast under mountains | 2 | windward | 2117, 8.55 | 1148, 155, 66, 18, 6.49, 8 |
| w05 Upland and moor | 1 | tops | 1159, 4 | 1033, 168, 156, 68, 11, 81 |
| w05 Upland and moor | 2 | tops | 1234, 3.93 | 1292, 180, 138, 70, 13, 70 |
| w06 High mountains | 1 | tops | 1678, 0.98 | 1076, 178, 216, 123, 14, 161 |
| w06 High mountains | 2 | tops | 1712, 0.84 | 1341, 192, 199, 127, 17, 165 |
| w07 Cold north | 1 | tops | 679, 5.15 | 869, 134, 76, 18, 6.15, 16 |
| w07 Cold north | 2 | tops | 678, 5.33 | 1178, 157, 70, 18, 7.04, 12 |
| w08 Fen basin | 1 | coast | 515, 9.72 | 803, 122, 70, 14, 5.47, 11 |
| w08 Fen basin | 1 | tops | 586, 9.54 | 922, 135, 74, 11, 5.84, 8 |
| w08 Fen basin | 2 | coast | 531, 9.79 | 1134, 149, 63, 14, 6.13, 6.8 |
| w08 Fen basin | 2 | tops | 519, 9.43 | 1124, 159, 73, 14, 6.81, 12 |
| w09 Estuary and saltmarsh | 1 | coast | 637, 9.63 | 833, 128, 72, 16, 5.71, 12 |
| w09 Estuary and saltmarsh | 1 | tops | 640, 9.43 | 918, 137, 75, 14, 5.97, 8.6 |
| w09 Estuary and saltmarsh | 2 | coast | 624, 9.65 | 1158, 153, 66, 15, 6.46, 8.6 |
| w09 Estuary and saltmarsh | 2 | tops | 641, 9.36 | 1136, 160, 73, 15, 6.98, 14 |
| w10 Chalk and clay | 1 | tops | 686, 7.74 | 934, 148, 92, 23, 7.38, 28 |
| w10 Chalk and clay | 2 | tops | 684, 7.7 | 1217, 165, 84, 26, 8.47, 24 |
| w11 Sand and heath | 1 | tops | 556, 8.97 | 885, 137, 78, 19, 6.42, 20 |
| w11 Sand and heath | 2 | tops | 563, 8.87 | 1204, 160, 70, 21, 7.39, 15 |
| w12 Lake country | 1 | tops | 1704, 4 | 1033, 168, 155, 67, 11, 81 |
| w12 Lake country | 2 | tops | 1820, 3.92 | 1291, 180, 139, 70, 13, 72 |

### Environments: soils, ground and cover

Over the whole land, from the cells. Soil depth and water held as `landgen/write.py` gives a parcel (`depth` x 1.2, AWC by texture); drainage the texture's share a day; fertility the cells' multiplier.

| World | seed | sand / loam / clay / chalk / peat | depth m | held mm | drain | fertility | slope p95° | over 10° | wet ground | floodplain / terrace | good arable | tree line m | commonest ecosystems |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w01 Lowland river country | 1 | 0.124 / 0.665 / 0.148 / 0.0631 / 0 | 1.14 | 174 | 0.265 | 0.975 | 2.5 | 0 | 0.0573 | 0.121 / 0.0999 | 0.962 | above the land | grassland 0.58, oak-ash wood 0.17, birch and pine wood 0.07, hay meadow 0.05 |
| w01 Lowland river country | 2 | 0.0875 / 0.673 / 0.177 / 0.0623 / 0 | 1.14 | 178 | 0.251 | 0.998 | 2.5 | 0 | 0.0675 | 0.167 / 0.0696 | 0.954 | above the land | grassland 0.54, oak-ash wood 0.21, hay meadow 0.08, birch and pine wood 0.05 |
| w02 Dry east | 1 | 0.124 / 0.702 / 0.141 / 0.0333 / 0 | 1.14 | 175 | 0.262 | 0.983 | 2.5 | 0 | 0.0299 | 0.114 / 0.0757 | 0.979 | above the land | grassland 0.60, oak-ash wood 0.19, birch and pine wood 0.09, hay meadow 0.05 |
| w02 Dry east | 2 | 0.088 / 0.714 / 0.127 / 0.0714 / 0 | 1.14 | 179 | 0.261 | 0.995 | 2.5 | 0 | 0.0372 | 0.168 / 0.0776 | 0.974 | above the land | grassland 0.58, oak-ash wood 0.18, hay meadow 0.08, beech wood 0.06 |
| w03 Wet west, maritime | 1 | 0.0964 / 0.598 / 0.234 / 0.0718 / 0 | 1.14 | 174 | 0.245 | 0.988 | 2.7 | 0.0038 | 0.0855 | 0.13 / 0.131 | 0.935 | above the land | grassland 0.57, oak-ash wood 0.22, hay meadow 0.05, beech wood 0.04 |
| w03 Wet west, maritime | 2 | 0.0888 / 0.592 / 0.263 / 0.0571 / 0 | 1.14 | 175 | 0.236 | 1 | 2.8 | 0.0039 | 0.0956 | 0.159 / 0.103 | 0.929 | above the land | grassland 0.53, oak-ash wood 0.24, hay meadow 0.07, chalk grassland 0.03 |
| w04 Coast under mountains | 1 | 0.0967 / 0.643 / 0.182 / 0.0782 / 0 | 1.04 | 160 | 0.255 | 0.927 | 13 | 0.0955 | 0.0711 | 0.111 / 0.086 | 0.785 | 588 | grassland 0.46, oak-ash wood 0.15, moor 0.09, upland oak wood 0.07 |
| w04 Coast under mountains | 2 | 0.088 / 0.644 / 0.205 / 0.0625 / 0 | 1.04 | 161 | 0.247 | 0.936 | 13 | 0.0935 | 0.0772 | 0.143 / 0.0815 | 0.765 | 592 | grassland 0.42, oak-ash wood 0.16, moor 0.10, hay meadow 0.08 |
| w05 Upland and moor | 1 | 0.125 / 0.694 / 0.106 / 0.0758 / 0 | 1.01 | 156 | 0.275 | 0.894 | 13 | 0.0932 | 0.0504 | 0.0852 / 0.0756 | 0.78 | 624 | grassland 0.31, upland oak wood 0.19, hill pasture 0.19, moor 0.11 |
| w05 Upland and moor | 2 | 0.0881 / 0.683 / 0.161 / 0.0676 / 0 | 1.01 | 158 | 0.255 | 0.916 | 14 | 0.0985 | 0.0543 | 0.112 / 0.0653 | 0.769 | 620 | grassland 0.27, upland oak wood 0.19, hill pasture 0.18, moor 0.11 |
| w06 High mountains | 1 | 0.124 / 0.691 / 0.108 / 0.0768 / 0 | 0.96 | 148 | 0.274 | 0.852 | 18 | 0.153 | 0.0589 | 0.0969 / 0.0831 | 0.687 | 550 | grassland 0.30, upland oak wood 0.20, moor 0.18, hill pasture 0.10 |
| w06 High mountains | 2 | 0.0878 / 0.684 / 0.16 / 0.0683 / 0 | 0.96 | 149 | 0.255 | 0.878 | 20 | 0.161 | 0.0622 | 0.124 / 0.0729 | 0.695 | 558 | grassland 0.27, upland oak wood 0.18, moor 0.16, hill pasture 0.12 |
| w07 Cold north | 1 | 0.124 / 0.676 / 0.137 / 0.0631 / 0 | 1.14 | 175 | 0.267 | 0.974 | 2.5 | 0 | 0.0568 | 0.12 / 0.0939 | 0.963 | 104 | grassland 0.58, oak-ash wood 0.17, birch and pine wood 0.08, hay meadow 0.05 |
| w07 Cold north | 2 | 0.0875 / 0.697 / 0.153 / 0.0623 / 0 | 1.14 | 179 | 0.255 | 0.995 | 2.5 | 0 | 0.0665 | 0.165 / 0.0684 | 0.955 | 103 | grassland 0.55, oak-ash wood 0.21, hay meadow 0.06, birch and pine wood 0.05 |
| w08 Fen basin | 1 | 0.105 / 0.537 / 0.19 / 0.0018 / 0.167 | 1.15 | 206 | 0.211 | 1.04 | 2.2 | 0.0013 | 0.153 | 0.0771 / 0.0972 | 0.803 | above the land | grassland 0.37, oak-ash wood 0.23, fen 0.12, wet grassland 0.11 |
| w08 Fen basin | 2 | 0.0814 / 0.522 / 0.222 / 0.0147 / 0.16 | 1.16 | 206 | 0.203 | 1.05 | 2.1 | 0.003 | 0.154 | 0.0972 / 0.102 | 0.81 | above the land | grassland 0.32, oak-ash wood 0.24, wet grassland 0.16, fen 0.10 |
| w09 Estuary and saltmarsh | 1 | 0.113 / 0.591 / 0.183 / 0.0183 / 0.0951 | 1.14 | 191 | 0.231 | 1 | 2.7 | 0.0058 | 0.13 | 0.0704 / 0.0807 | 0.858 | above the land | grassland 0.47, oak-ash wood 0.20, birch and pine wood 0.06, reedbed 0.06 |
| w09 Estuary and saltmarsh | 2 | 0.089 / 0.595 / 0.194 / 0.0336 / 0.0889 | 1.14 | 192 | 0.227 | 1.02 | 2.6 | 0.0051 | 0.126 | 0.13 / 0.0924 | 0.868 | above the land | grassland 0.45, oak-ash wood 0.22, hay meadow 0.06, reedbed 0.06 |
| w10 Chalk and clay | 1 | 0.0098 / 0.0518 / 0.502 / 0.437 / 0 | 1.13 | 165 | 0.233 | 0.953 | 2.9 | 0 | 0.0441 | 0.121 / 0.0347 | 0.971 | above the land | chalk grassland 0.34, oak-ash wood 0.27, grassland 0.22, hay meadow 0.10 |
| w10 Chalk and clay | 2 | 0.0067 / 0.0674 / 0.495 / 0.431 / 0 | 1.14 | 166 | 0.232 | 0.959 | 2.9 | 0.0001 | 0.0503 | 0.151 / 0.0408 | 0.965 | above the land | grassland 0.28, chalk grassland 0.25, oak-ash wood 0.21, hay meadow 0.13 |
| w11 Sand and heath | 1 | 0.459 / 0.432 / 0.0848 / 0.0243 / 0 | 1.14 | 138 | 0.354 | 0.875 | 2.8 | 0 | 0.0319 | 0.106 / 0.0852 | 0.978 | above the land | grassland 0.44, birch and pine wood 0.23, lowland heath 0.13, hay meadow 0.09 |
| w11 Sand and heath | 2 | 0.459 / 0.403 / 0.0909 / 0.0475 / 0 | 1.14 | 138 | 0.356 | 0.88 | 2.8 | 0 | 0.0383 | 0.158 / 0.071 | 0.973 | above the land | grassland 0.39, birch and pine wood 0.24, hay meadow 0.14, lowland heath 0.11 |
| w12 Lake country | 1 | 0.125 / 0.681 / 0.119 / 0.0758 / 0 | 1.02 | 155 | 0.272 | 0.895 | 13 | 0.0922 | 0.0765 | 0.0955 / 0.101 | 0.755 | 622 | grassland 0.30, upland oak wood 0.19, hill pasture 0.18, moor 0.11 |
| w12 Lake country | 2 | 0.0891 / 0.666 / 0.186 / 0.0584 / 0 | 1.01 | 157 | 0.249 | 0.919 | 14 | 0.1 | 0.0768 | 0.113 / 0.0835 | 0.75 | 619 | grassland 0.27, upland oak wood 0.19, hill pasture 0.17, moor 0.11 |

<!-- widened:end -->


## 8. Reading section 7 (measured, then inference)

**Sources of nutrition.**

- **The land's year is nearly the same everywhere:**
  - At `worked` the fields feed 21 to 23 people a village in the lowland, dry, wet, cold, fen, estuary, chalk and sand worlds,
    and 29 to 32 in the four upland worlds. The plots and soils are the same in all of them (fault 11); the upland's higher
    figure is measured, but its cause is not traced.
  - Herds return 1.6 a unit and feed 1.5 to 1.7; wild plants 0.6 a unit, 0.7 fed; the parcels' old game stock 0.14 to 0.20 a
    unit, 0.2 fed; resident fish 0.82 a unit, about 1 fed.
  - Fish are the same everywhere because the stocking is 8 a unit of water parcel in every world (brief 5's `water_stocks`),
    not by the water body.
  - The store loses 4.5 to 5% of food from the house store, and 1% in the best store the world reaches.
  - Inference: the land's sources differ so little because a village's land is sized to its people ([[D2-161 Seed nodes below what they sustain|D2-161]]), the parcels'
    stocks are set per unit of cover (vocab `PER_UNIT`), and the fields are always on floodplain clay. None of it reads the
    climate.
- **The acts (autumn, fresh ground):**
  - **Hunting near:** novice 0 to 0.22, master 0.63 to 1.35. That is on 02zzd's targets (0.1 to 0.2 and 1 to 1.5).
  - **The wood around:** master 2.2 to 3.2.
  - **Far:** master 1.2 to 2.2, under the wood around's and well under the target of 4 to 5. Hunting far is no better than the
    wood around on any world (the open finding of 02zzd, still open).
  - **Gathering:** 1.0 to 2.0. **Angling:** 1.4 to 2.4. **By hand:** 0.5 to 1.1.
  - **Eel traps (a night) and nets:** 0 to 0.2 at best, so the water's take is a rod's, not a trap's.
  - **Break-even:** 0.25 a unit (a ration a day over 192 units a year, at 1.5 eaters a worker). Every master clears it four to
    twelve times over, so return never limits a source here: its yearly yield does.
- **What could feed a village of nine alone:**
  - **The fields:** in every world.
  - **Hunting, by the wild land's growth:** an upper bound (r K / 4, each hunted kind's births less deaths over four). It gives
    27 to 37 people from the wood around and 270 to 480 from the land within 8 km, in every world. The brown hare is two-thirds
    of it.
  - **Inference:** that is ten times or more a temperate hunter's density (about 0.05 to 0.2 people a km² over the 20 km²
    around a village and the 200 km² within 8 km). Two things inflate it:
    - the hare stands at 38 to 60 a km² over the whole land, twice its reference of 25;
    - a head's food is generous for the compressed year. A red deer gives 20 meat, 30 food, and an engine food is 365/32 real
      person-days, so a deer is about 340 person-days; a real red deer's 50 to 60 kg of meat is about 40 to 50.
    The wild layer's owner should check `TAKEN` goods against the year's compression before a hunting-only world ([[D2-242 Subsistence test worlds|D2-242]]).
  - **The runs:** 2 to 11 salmon, 0 to 22 lamprey and 7 to 148 eels at a village's water a year: 1 to 33 food, at most one
    person's year. In no world can a village live off the runs. [[D2-242 Subsistence test worlds|D2-242]]'s runs-only world needs runs far larger, or a world
    built for them (brief 5's runs world). The suite's villages sit on rivers of every class, and the runs are counted only
    where a village's own stretch has them.

**Wildlife.**
- Red deer 2.1 to 2.4 a km² in every world, roe 6.8 to 8.0, boar 1.1 to 1.7, fox 1.2 to 1.3, wolf 0.037 to 0.045: flat across
  the suite.
- Hare is lower in the uplands (38 to 46) than the lowland (55 to 60).
- Wildfowl and eel follow the water: fen 41 to 52 and 36 to 39, estuary 28 to 29 and 21 to 22, lake country 12 to 20 and 9 to
  16, against the dry east's and the sand's 4 to 5 and 3 to 4.
- Inference: the Highlands' red deer on the open hill run 5 to 15 a km², and a lowland's woods under 1. The deer read wood and
  grass, not the hill, so the uplands get the lowland's deer.
- The heads' "where" for migrant kinds (wildfowl) reads 0: they are measured at the run's start season, before they arrive.

**Weather and its likelihood.**
- The weather types and labels are the same in every world of a seed: seed 1 settled 46%, westerly 26%, cyclonic 9%; seed 2
  settled 40%, cyclonic 18%.
- Each year at the villages: clear 155 to 188 days, rain 122 to 137, heavy rain 11 to 20, fog 17 to 22, snow 13 to 17, gale 12
  to 15. Storms touch a village on 17 to 26 days a year.
- The generator's climate spans 400 to 1,250 mm and 5.4 to 9.9 °C over the same villages. The engine's column does not move
  with it: the known gap.

**Environments.**
- The soils follow the configurations:
  - the sand country is 46% sand and holds 138 mm;
  - the chalk and clay is 43 to 44% chalk and 50% clay;
  - the fen is 16 to 17% peat and holds 206 mm;
  - every other world is about two-thirds loam.
- Fertility runs from 0.85 (the high mountains) to 1.05 (the fen). Slopes: a p95 of 2 to 3° in the lowlands and 13 to 20° in the
  uplands.
- Good arable (the arable terrains under 8° and not waterlogged, a generous reading) is 0.69 to 0.98 of the land. The villages'
  fields stand on none of the difference (fault 11).
- The cold north's ecosystems are the lowland's (fault 5).

## 9. What the widened sections could not measure

- **Hunting's yearly yield as the engine takes it:** a hunter working a wood down day after day (02zzd's depletion test) was
  not run on the suite. The yield above is an upper bound from the ecology's own rates.
- **The acts in other seasons:** autumn only, to keep the suite at about 20 minutes.
- **Preserving beyond the store:** smoking, salting and drying (`smoke racks`, `salt fish`) are not in the capacity model's
  levels. Their effect is not measured.
- **Expectations for the widened measures:** not written. A real place gives few numbers for food a unit of work; the 02zzd
  targets are quoted where they apply.
