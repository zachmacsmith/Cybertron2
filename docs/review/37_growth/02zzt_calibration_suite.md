# 02zzt: the calibration suite, its first results, and the generator audit

37.2, 20 Nov 2026. WORK W-54. Proposal `docs/cybertron2/proposals/calibration_worlds.md` (D2-228; all twelve worlds, D2-245). Zach
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

A row per world, the two seeds side by side where they differ (section 7 has each in full). Measured.

<!-- overview:begin (written by 02zzt_calibration_suite.py) -->
<!-- overview:end -->

## 1. What was made

All 24 worlds generate at their first seeds; none was refused and none crashed (measured). The settings each world uses, and why,
are in the maker's `WORLDS` table. Three needed more than the proposal's table gives:

- **High mountains:** `upland and moor` with its moor raised from 560 to 900 m and a 300 m summit laid on it. The tops reach
  1,563 and 1,620 m. (1,150 and 450 gave 1,950 m.)
- **Lake country:** `upland and moor` with a laid mere at the fells' foot. The mere would not hold on the fells' flank (the land
  falls 200 m across it). It needed one small generator fix (commit `fix W-54: a laid lake is kept outside the lake cap`): ten
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
- This is the gap that climate from the land (OPEN Q-56) closes. It is not a fault of the suite.
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
  - This belongs with climate from the land: the year's anomaly (D4-109's `year` layer) should carry the year's variance, and the
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

At the villages. Each cell: the generator's value / the engine's (the generator holds only rain and the mean); the range below the name. **Bold** is out of range; the engine's misses on dry, cold and coastal worlds are the known gap (it reads only height, 02zzo; climate from the land, OPEN Q-56).

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

## 5. The generator audit (W-54): what the land gets wrong, world by world

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
  The sizes follow the river's class. The water measure (W-60) and the fishing calibration need it: today a village on 6 km of
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
    highest node is 376 m). D2-227 wants nodes above 500 m.
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
- **Inference:** the wood share by how long settled is a design choice (D2-184's era). But a region's share should also follow
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
models offline (`02zzt_nutrition.py`: the capacity model, D4-102, and 02zzd's harness of the acts); the reading is in section 8.

<!-- widened:begin (written by 02zzt_calibration_suite.py) -->
<!-- widened:end -->
