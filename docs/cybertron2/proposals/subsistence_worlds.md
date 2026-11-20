# Subsistence worlds: can each livelihood keep a village on its own?

**Status:** discussion (20 Nov 2026). Decided in principle: D2-242; hunting's return D2-255. The design below is for Zach's choices
(OPEN Q-66). Revised 20 Nov: live runs are the test and bots the comparison; the surplus ceilings raised and measured as people fed
per food worker; skill seeded by arm.

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

The test is a small set of live runs: villages seeded at chosen skill levels (a village of capable hunters; one master hunter
among novices), with the cast scenario_design asks for. Scripted bots that are good at each livelihood run the same worlds beside
them, at no model cost. The bots show what the world allows; the models show what agents make of it.

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

- **Skill is seeded,** not learned in the run. Each arm starts its people at a chosen level, so "a village of capable hunters" and
  "one master hunter among novices" are two arms, and the value of one master shows directly.
- **Village size:** small, two or three households (about 8 to 12 people), and large, six (about 30), on the same land, so density
  shows. It matters most for hunting, fishing and the runs.
- **Live runs, the test.** For each livelihood, three arms on its small village:
  - everyone capable, with medium capital;
  - one master among novices, with medium capital;
  - masters, with high capital.

  That is 7 × 3 = 21 runs. A run lasts about two compressed years (two winters). Each household head is Opus, the middle Sonnet,
  the rest Haiku (scenario_design §2). Past runs cost about $0.04 to $0.07 a person-day, so a small village over about 48 days
  costs about $20 to $35, and the 21 runs about $400 to $700. A first cut of 12 runs (the low and high arms of each, without
  gathering alone) costs about $250 to $400. Each needs Zach's go.
- **Bots, the comparison.** Scripted bots that do each livelihood competently run the full grid of skill × capital × size on the
  same worlds, with two seeds and a bad year, at no cost. They are the ceiling the models are read against.

### What is measured

For each livelihood, level and size:
- **survival:** deaths, nights hungry, the worst month;
- **food per unit of work, by season,** against the 02zzd numbers;
- **the share of working time spent on food;**
- **the year's surplus:** food beyond need, and how much of it can be kept (spoiled, salted, dried, smoked, stored);
- **the stocks:** game, fish and runs over two years, fished or hunted down and recovering, the sustainability test;
- **the stores at winter's end,** the binding constraint for runs, hunting and herding.

### The targets (calibrate; wide on purpose)

**Measured as people fed per food worker,** over a year with its winter. A household of five with two workers needs about 2.5 to
live off itself. Anything above that feeds someone else: a specialist, a lord, a town. That surplus is what makes specialisation
and a complex society possible (D2-242), so the high ceilings sit well above subsistence (Zach, 20 Nov: "should the ceiling for
surplus be able to be even higher").

| Livelihood | Low (novice, little capital) | Medium (capable; must survive) | High (master, capital) | What bounds the high end |
|---|---|---|---|---|
| Arable | 1.5 to 2.5: thin | 2.5 to 4 | 5 to 8 (plough, oxen, manure, mill, good land) | land, seed, draught beasts, the harvest's labour peak |
| Herding | 1.5 to 2.5 | 2.5 to 3.5 | 4 to 6 (a dairy, hay made) | grazing, winter fodder |
| Hunting | under 1.5: fails | 2.5 to 3, small village only | 4 to 8 per master, more on trips out to other nodes (D2-255) | the game (territory, wariness, a wood hunted down), the carry home, the learning (about half a life) |
| Resident fishing | 1.5 to 2.5 | 2.5 to 4 | 4 to 6 | the stock and its recovery |
| Runs, with preserving | fails in winter (nothing kept) | 2.5 to 4 | 6 to 15 in a good year (weir, salt, smokehouse) | the run's size and the preserving capacity |
| Foraging | 1.5 to 2.5 | 2.5 to 3.5, low density | 3.5 to 5 | the seasons and the territory |
| Gathering alone | fails in winter | fails in winter, except a mast year | — | the winter |

**A note on history.** Medieval farming fed about one other household in every four or five. That supported lords, towns and
crafts at about 10 to 20% of the people. The ceilings here are deliberately higher, so that specialisation can show within a run
of weeks. They are bought with skill, capital and work, and bounded by the land and the stocks, so food still binds
(scenario_design: capacity at least 1.25 times demand, and food at most about 30% of actions in a mixed world).

The first draft's bands follow, kept for reference.

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
5. **Hunting trips out to wild nodes** (D2-255, D2-256): travel to a wild node, camp, hunt there, carry the food back. Every piece is
   built; whether they chain well (the carry, spoilage over days, drying at the camp) is untested, and the bots test it first.
6. **A wood that runs down** (Q-46 (c), now in W-69). Daily hunting of one wood should fall to about half its return within a
   season, or the master's return has no limit.
5. **The engine's weather reads only height** (Q-56) until climate from the land is built. Worlds differ in land and wild life
   now; their weather will differ later.

### The stages

1. **The bots' grid** first, since it is free: it shows whether the world can do it at all, and the fixes for what misses its row.
2. **The live runs:** the 21 (or 12) arms above, each read against the bots on the same world and against the targets.
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
2. The live arms: three per livelihood (all capable; one master among novices; masters with capital), 21 runs at about $400 to
   $700, or a first 12 at about $250 to $400?
3. The bots as the comparison, running the full grid free?
4. The targets as people fed per food worker, with the high ceilings in the table (arable 5 to 8, the runs 6 to 15, a master
   hunter 4 to 8)?
5. The prerequisites in order: shared units (W-64), the switches (37.4), a wood running down (Q-46 c), the bots, then the live
   runs, with forays later for the hunting trips?
6. Stage 3, specialists side by side, as the goal of the series?

## Affects

`cybertron2/specs/` (a subsistence maker beside the calibration suite), the bots (`cybertron2/` null-arm agents), one small engine
change (the switches, 37.4), the data rows that miss their targets, W-64 and W-67.

## History

- 20 Nov 2026: the runs bots built (W-69, branch w69-bots): `cybertron2/engine/bots_livelihood.py`, chosen per run by
  `--bots runs`, its own unit (D2-244). Each household fishes by plain rules from what it can see: traps through the run windows,
  lifted each morning; a net when a shoal is at the water; the weir's gap shut whenever a run is there, mended on any night short
  of a spate; the surplus over the night's suppers smoked, dried or salted; wild food where a gather is worth its work, else rest.
  On today's food values (the eel at 0.2) no arm keeps the village over 64 days: the bots' villages starve in the first winter
  (median death day 19 to 20, the generic bots' 13); traps land 68 to 87 food in the first autumn, the high arm's weir 3 (the traps
  thin the run before it), the nets none (the salmon run is a few heads); fishing returns about 0.17 food a unit, a person fed per
  full-time fisher, no better than wild food; nothing is ever smoked, dried or salted, as the catch never passes the suppers. To be
  read again on D2-259's values.
- 20 Nov 2026: accepted in part: D2-258 (The food values are put on one physical basis (proposals/shared_units.md; 02zzu)).
- 20 Nov 2026: Zach's answers. Decided as D2-257: seven livelihoods, the first 12 live runs on small villages, bots as the comparison,
  the food values fixed first. A hunting trip is travelling to a wild node, camping, hunting and carrying the food back, built
  from what exists (D2-256), so forays are no prerequisite. The high ceilings become later technology's; the medieval worlds take a
  lower band, "lower ... but still not too low" (Q-68). "The runs can be relatively small" is read as small live runs (fewer people,
  cheaper).
- 20 Nov 2026: accepted in part: D2-257 (The nutrition worlds: seven livelihoods tested alone (arable, herding, hunting a).
- 20 Nov 2026: revised after Zach.
  - Hunting: a master brings in a disproportionate amount, more on trips out to other nodes (D2-255), so hunting can keep a small
    group. The first draft's cap of 1.2 times was wrong.
  - Surplus: the ceilings were raised and measured as people fed per food worker, since the surplus is what supports
    specialists and a complex society.
  - Skill is seeded by arm.
  - Live runs are the test (Zach: "I meant a smaller number of actual llm runs"), with competent bots as the comparison, and
    the cost estimated.
  - The hunting trips and a wood running down were added as prerequisites.
- 20 Nov 2026: accepted in part: D2-255 (A very skilled hunter brings in a disproportionate amount of food, more still on).
- 20 Nov 2026: written by 37.2 at Zach's request, from D2-242, 02zzd's measurements, brief 5 §8's runs-only world and L-112.

## Sources

docs/review/37_growth/02zzd_hunting_farming_ev.md; docs/cybertron2/proposals/river_and_water.md §8; proposals/calibration_worlds.md;
proposals/shared_units.md; docs/scenario_design.md; docs/review/37_growth/02zzs_wild_region_run.md.
