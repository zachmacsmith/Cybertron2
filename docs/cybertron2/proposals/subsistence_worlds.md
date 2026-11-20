# Subsistence worlds: can each livelihood keep a village on its own?

**Status:** discussion (20 Nov 2026). Decided in principle: D2-242. The design below is for Zach's choices (OPEN Q-66).

**Owner:** 37.2 (the worlds, the targets, the report); 37.4 for any engine switch they need. WORK W-69.

## Summary

These are nutrition calibration worlds. Each world feeds its village from one livelihood only. Every livelihood is measured on a
grid of skill and capital (and village size), and must meet three tests:
- **survival:** at medium skill and capital, the village gets through two years;
- **surplus:** with more skill or capital, it makes a surplus up to a bound;
- **real differences:** the livelihoods differ as real ones do. Hunting needs territory, the runs need preserving, farming needs
  seed and draught beasts.

The surplus in isolation matters because it is what makes specialisation and trade possible (D2-242). So a third stage puts
specialists side by side, to check that trade makes both better off.

The first two stages are measured with scripted bots, at no model cost, so the numbers describe the world, not a model. A few live
runs follow only where a livelihood works on paper.

## The proposal

### The livelihoods

| # | Livelihood | Its world (from the calibration suite) | What it tests | New? |
|---|---|---|---|---|
| 1 | **Arable farming** (grain) | lowland river country; chalk and clay vale | the reference: seed kept back, draught beasts, storage through winter | |
| 2 | **Herding** (milk, cheese, meat, hides) | upland and moor; chalk downs (sheep) | living off beasts: grazing, winter fodder, dairy as the store | **added** |
| 3 | **Hunting and trapping** | a frontier of wood and wild land | territory: a hunting village lives at low density, or not at all | |
| 4 | **Resident fishing** (lake and river stocks) | lake country | a steady stock, fished down and recovering | |
| 5 | **The runs** (salmon, eels) with preserving | the river world (`runs.yaml`, made for brief 5 §8) | a seasonal glut: without salting, smoking and stores, winter kills | |
| 6 | **Foraging** (gathering, hunting and fishing together, nothing kept or sown) | wood and water frontier | the realistic way people lived before farming: no single source, the seasons covered by switching | **added** |
| 7 | **Gathering alone** | broadleaf woodland | a control: it should fail in winter, except in a mast year | **added (control)** |

**Later:**
- the coast (shellfish, seabirds; pack K9, not built);
- mixed farming, the ordinary village, as the anchor every other result is read against.

### The levels

| Level | Skill (the engine's familiarity and craft levels) | Capital: what the household holds |
|---|---|---|
| **Low** | a novice: has a rough idea of the craft | bare hands and the simplest tools: a hoe, a crude weapon, a hand line; no store beyond the house |
| **Medium** | capable | the ordinary kit of the livelihood: a weapon and snares; a rod and traps; a granary or bins; a drying rack |
| **High** | a master | developed capital: an ox plough and a mill; a weir with a smokehouse and salt; a herd with a dairy; nets and a boat once built |

- **Village size** is a third axis: two households and six, on the same land, so density shows. It matters most for hunting.
- **The grid:**
  - all nine of skill × capital at two sizes, two seeds and two years: 7 livelihoods × 9 × 2 × 2 = 252 bot runs;
  - or a cheaper cut: the diagonal (low-low, medium-medium, high-high) plus the two corners (high skill with low capital, and the
    reverse), which is 140 runs.
- **A bad year** at medium-medium for each, using the eras' hard winter or a dry year, shows the risk as well as the mean.

### What is measured

For each livelihood, level and size:
- **survival:** deaths, nights hungry, the worst month;
- **food per unit of work, by season,** against the 02zzd numbers;
- **the share of working time spent on food;**
- **the year's surplus:** food beyond need, and how much of it can be kept (spoiled, salted, dried, smoked, stored);
- **the stocks:** game, fish and runs over two years, fished or hunted down and recovering, the sustainability test;
- **the stores at winter's end,** the binding constraint for runs, hunting and herding.

### The targets (calibrate; wide on purpose)

| Livelihood | Low skill, low capital | Medium, medium (must survive) | High, high (surplus) | Density it allows |
|---|---|---|---|---|
| Arable | survives thinly, no surplus | survives; food under about half of working time | about 1.5 to 2.5 times need | high |
| Herding | thin in winter without fodder | survives with hay made | about 1.2 to 1.6 times | medium |
| Hunting | fails | survives only at low density (the small village) | at most about 1.2 times, small village only | low: about 0.1 to 0.5 people per km² hunted |
| Resident fishing | thin | survives | about 1.2 to 2 times, if the stock holds | medium, by the water's size |
| Runs | fails in winter (nothing kept) | survives with drying and stores | 2 to 4 times in season; the kept part bounded by preserving | high where the run is strong |
| Foraging | thin | survives at low to medium density | about 1.1 to 1.3 times | low to medium |
| Gathering alone | fails in winter | fails in winter, except in a mast year | — | — |

These encode D2-242:
- each real livelihood keeps a village at medium;
- each makes a surplus at high;
- the differences are the ones history shows: hunting needs territory, and the runs are only as good as their preserving.

A livelihood that fails its row means a calibration to fix, or a missing piece, which is then named.

### What it needs first

1. **Food on one basis** (W-64, shared units). Fish food values are wrong: an eel gives a fifth of its real food. Until the
   units are right, the fishing and runs rows measure the bug.
2. **A switch for each food source.** Farming cannot be switched off (OPEN L-112): its rows carry no pack, so a world can only
   remove fields, seed and beasts. Each world must also be able to lack game, fish or a run. The clean way is a `farming` pack
   and per-world switches for game and fish (37.4, a small engine change kept to the feature-package seams, D2-244). The
   fallback is that the world removes them, as `runs.yaml` does.
3. **Bots that do each livelihood competently**, or the grid measures the bot. Scripted bots exist for the null arms. Each
   livelihood needs a plan: sow and keep seed; graze and make hay; hunt and set snares; fish and trap; mind the run and preserve.
4. **The high tiers that are not built:** nets and bows (pack K3), dogs and husbandry (K6), boats (brief 5's fen half). Until
   then the high rows use what exists, and the report says which tier is missing (W-67).
5. **The engine's weather reads only height** (Q-56) until climate from the land is built. Worlds differ in land and wild life
   now; their weather will differ later.

### The stages

1. **Isolation, with bots:** the grid above, free. It gives a table per livelihood, and fixes for what misses its row.
2. **A few live runs** where stage 1 says a livelihood works: does a cast of models find it? Each is read against its bot null
   arm, as scenario_design asks.
3. **Specialists side by side:** two or three villages, each with one livelihood (a runs village, a farming village, a herding
   one) and a road between them. Does trade make both better off than isolation, and do they find it? This is the point of D2-242.

## Why

Zach (20 Nov): "can a village survive off just runs (should be possible?) can a village survive off just hunting (should be
possible). Each of these should be possible for relatively skilled / medium skill / capital and able to produce surplus up to
some amount if there is greater capital / skill ... which is necessary in isolation for specialisation and trade to be possible";
"Can we work now on those worlds where (these are like nutrition calibration worlds) societies are supposed to survive solely of
just each of hunting, fishing, vs farming etc. comparing at different levels. What should these look like, and should we add any?"

Past runs starved or nearly so (02zzp; the wild region run's Holtham, 02zzs). The model-per-household runs world was meant to test
the runs but got fields instead (Q-60 (c)). Measured on 9 Nov, hunting was far below its targets (02zzd). Nothing yet says whether
any one livelihood can carry a village, so nothing says whether specialising could pay.

## Alternatives considered

- **Live runs from the start:** they measure the models as much as the world, and cost money for each of hundreds of cells.
- **The capacity model alone** (cybertron2/capacity/): fast, but it gives yearly carrying capacity, not whether a village gets
  through a winter with real work, seasons, spoilage and depletion.
- **One mixed world with sources turned off one at a time:** cheaper to make, but each livelihood then sits in land that was not
  chosen for it, so a failure cannot be told from a poor match of land.

## Open questions

OPEN Q-66:
1. The livelihoods: the five plus herding, foraging and gathering alone as a control? Add the coast and mixed farming later?
2. The grid: all nine skill × capital cells, or the diagonal and the two corners?
3. Bots first (free), then a few live runs only where a livelihood works on paper?
4. The prerequisites in this order: shared units (W-64), the switches (37.4), the bots, then the grid?
5. The target bands above, as a first cut to calibrate against?
6. Stage 3, specialists side by side, as the goal of the series?

## Affects

`cybertron2/specs/` (a subsistence maker beside the calibration suite), the bots (`cybertron2/` null-arm agents), one small engine
change (the switches, 37.4), the data rows that miss their targets, W-64 and W-67.

## History

- 20 Nov 2026: written by 37.2 at Zach's request, from D2-242, 02zzd's measurements, brief 5 §8's runs-only world and L-112.

## Sources

docs/review/37_growth/02zzd_hunting_farming_ev.md; docs/cybertron2/proposals/river_and_water.md §8; proposals/calibration_worlds.md;
proposals/shared_units.md; docs/scenario_design.md; docs/review/37_growth/02zzs_wild_region_run.md.
