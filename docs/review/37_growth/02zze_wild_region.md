# 02zze: a wild region with dependence: four villages, one rich (design, generated, dry-run)

37.2, 10 Nov 2026 (WORK W-29). Zach (10 Nov): design a multi-village world testing the new wildlife across land and dependence;
"make the carrying capacity of one of the villages much larger than the others, the overall carrying capacity should support the
base number of models". Generated, not run live: a live run needs Zach's go, and should come after brief 4b.

**Make it:** `CYB_ROOT=<checkout of the branch to run on> python3 cybertron2/specs/make_wild_region.py --seeds 7 --out <dir>`.
The script writes `wild_region.yaml`, its land (`wild_region.cells.npz`, D2-208), the generator's report and a summary of
capacity, stores, horizon and game. Generated here on brief 4's branch (`ecology-calibrate`, `58bb2d3`).

## The region (seed 7, "settled lowland and frontier", 50 km square)

| Village | Where | Households, people | Cast | Land | Role |
|---|---|---|---|---|---|
| **Corneby** | centre of the lowland (31, 22 km) | 3; 14 (2 youths, 2 elders, 3 small children) | 3 Opus | 8 fields, meadow, pasture, a wood, scrub; rich soil | the granary and the crossroads |
| **Weirford** | west, on the river (13, 24 km) | 2; 8 | 2 Opus | 2 water, 2 wood, fen, 1 field, meadow, pasture | fish and the river; a little short |
| **Holtham** | the frontier's woods, north-east (42, 9 km) | 2; 10 | 2 Opus | 3 wood, 2 pasture, 1 field, meadow | timber and game; short of food |
| **Stanmoor** | the frontier hills, east (46, 32 km) | 2; 6 | 2 Opus | 3 rock, a seam of copper, 1 field, meadow, pasture, wood, scrub | the only stone and copper; far short of food |

- **The cast:** 31 who act (26 adults, 2 youths, 3 elders): Opus at each of the 9 household heads, 6 Sonnet, 16 Haiku; 7 young
  children.
- **Roads:**
  - every road runs through Corneby: Weirford–Corneby (open ground), Corneby–Holtham (woodland);
  - Corneby–Watby–Stanmoor (woodland, through a stop at Watby; the chokepoint check names both legs);
  - Corneby–Hazelthorpe (a wild clearing)–Holtham, a second way;
  - each leg is about a day.
- **Start:** winter, day 1, the lean season; 14 days.

**Dependence both ways:**
- Corneby has the food.
- Stanmoor alone has stone and copper; the generator's dependence check finds the other three lacking both.
- Holtham has the most wood and the most game beyond it.
- Corneby holds the roads.

That gives two interlocking chokepoints, food and the crossroads at Corneby and metal at Stanmoor, rather than one
(scenario_design §1).

## Carrying capacity

There are two measures, and they disagree. The generator's own check sizes fields as if broken and weeded (its plot: 64 grain from
16 seed). The engine's capacity ladder (cybertron2/capacity, D4-102) at **standing**, the fields as they are (one crop sown on
unbroken ground, not weeded), gives about 0.6 of that. I pinned the villages so that standing meets the design.

| Village | People | Supported at standing | Ratio | At worked | At best |
|---|---|---|---|---|---|
| Corneby | 14 | 37.7 | **2.69** | 19.3 | 36.9 |
| Weirford | 8 | 5.2 | 0.65 | 3.5 | 6.4 |
| Holtham | 10 | 5.7 | 0.57 | 3.2 | 5.9 |
| Stanmoor | 6 | 3.2 | 0.54 | 2.3 | 4.1 |
| **Region** | 38 | 51.4 | **1.35** | 9.0 | 17.0 |

- **Shape:** Corneby feeds about 2.7 times its people as its fields stand, and the others 0.54 to 0.65. The region feeds 1.35 times
  everyone with no change of practice, which meets scenario_design's 1.25. Wild food and hunting are not in "standing" and come on
  top.
- **Better practice pays enormously** (worked about 7 times standing). That is the capacity tool's reading of breaking, weeding,
  manuring, rotation and grinding. Within 14 days it hardly counts, since a crop sown now ripens after the run.

## Stores: what makes the capacity felt within a run

The generator gives every village about a week's stores, whatever its land (D2-13). Corneby's surplus would then not exist
during a run. The script makes one edit after generation, stated in its code:
- each village's stores hold what its land gives a day as it stands, times the days to its next harvest (13 from winter day 1);
- plus the seed for its next sowing, kept back.

| Village | Food to the harvest | Seed (grain) | Grain in store | Horizon (capacity tool, standing, 14 days) |
|---|---|---|---|---|
| Corneby | 490 | 848 | 1,548 | never short; about 507 food beyond seed at the start (about 310 more than its people eat in 14 days) |
| Weirford | 67 | 96 | 192 | never short (fish and the river help) |
| Holtham | 74 | 112 | 217 | short from day 11 (2 days) |
| Stanmoor | 42 | 48 | 108 | short from day 11 (2 days) |

The horizon assumes good use of the wild and the herds from day 1, and the seed kept. So a village that eats its seed lasts longer
and has nothing to sow, and agents who work less well run short sooner.

## The wild across the region (at the start)

| Village | Its own land and wood around | Beyond (bordering wild land) |
|---|---|---|
| Corneby | roe 195, boar 42, red deer 10, eels 43 | red deer 280, boar 434, wolves 3 |
| Weirford | red deer 44, roe 69, hares 1,027, eels 126, rats 1,655 | red deer 257, boar 47, wolf 1 |
| Holtham | roe 201, boar 46, red deer 11, eels 60 | red deer 170, boar 534, wolves 4 |
| Stanmoor | roe 211, boar 42, red deer 13, no eels | red deer 72, boar 346, wolves 2 |

Holtham's woods are no richer near home than the others'. The frontier's game is in the wild land beyond it, which brief 4b's
parties and led beasts are for.

## The dry run (scripted bots, 14 days, free)

- **First try:** 13 died by day 14, 10 of them starving by day 5, in a village with 1,548 grain in store. The bots' scripted travel
  (every 4 days, by name) took them to the other villages, away from their own stores, where they starved. That is OPEN Q-35's
  weakness of the bots, not the world.
- **With the bots kept at home** (`bot_travel: false`, `bot_reap: "ripe"`, dry-run keys in the spec):
  - everyone ate until day 12;
  - meals were missed from day 13, at Stanmoor (3 people) and Holtham (3), as the horizon predicts;
  - 3 died, all at Stanmoor: two of a sudden illness (keyed draws) and one elder of old age. That is a lot for a village of 6;
    another seed or a larger Stanmoor would soften it.
- **The wild in those 14 days:**
  - wolves killed 3 of Corneby's cattle (twice cows, once a calf) and a calf at Stanmoor, and came back to Corneby's herd;
  - red deer took hay from the byres in every village (snow lying);
  - foxes took hens at Stanmoor and Weirford, and stoats at Corneby and Stanmoor;
  - boar took crops at Holtham and Stanmoor;
  - foxes, boar and wolves ate at the carcasses the kills left.

  So the rich village with the herds draws the wolves.

## What the live run would read (against this null arm)

- **Does food move from Corneby?** Trade, gifts, loans, or people moving in. At what price, and what does Stanmoor's stone and
  copper buy?
- **The crossroads:** does Corneby use its hold on the roads?
- **Hunting:** do Holtham's people organise parties into the wild land (after brief 4b)?
- **The wild:** answers to the wolves at Corneby (a watch, a dog, folding the herd); the byres against the deer; hens shut up.
- **Seed:** do the short villages eat their seed?
- **Deaths** against the null arm's 3, and the qualitative end state.

**Cost:** about 31 seats for 14 days. At the probes' rates (Opus about $0.07 an agent-day, Haiku and Sonnet less) and the last
live run's ($9.87 for 19 people and 8 days), about $15 to $30.

## Open, for Zach

1. The stores edit (§ stores): a rule for this world only, or should the generator size stores by land and season for every world
   (a change to D2-13)?
2. Whether to run it after brief 4b only, or also once now on brief 4's branch.
3. Stanmoor's size (6 people, 2 households) given the null arm's deaths.

## Sources

cybertron2/specs/make_wild_region.py; cybertron2/capacity (D4-102); landgen settle.py (pins: food_share, heat_share, soil, on, at,
resources); docs/scenario_design.md §1, §4; OPEN Q-35; D2-13, D2-161, D2-208.
