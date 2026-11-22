# The building clock's first stage, read with bots: do bots still build when works cost 1/15 and 1/7 of real hours?

22 to 23 Nov 2026, 37.2 (overnight testing subagent). Thread: reading the building clock's first stage with bots (W-82), under
fishing, hunting and their materials (W-73). A session note: bots only, no model calls, no live run, nothing published. The code is
on the worktree branch `w82-clock-bots` (at `/home/user/c2-w82`, committed there, not pushed, not merged); no file on `main` was
changed but this note.

**Read with:** the building clock proposal ([proposals/building_clock.md](../../../cybertron2/proposals/building_clock.md); the
redesign accepted in principle, D2-276; works raised in stages, D2-281), its audit ([building_clock.md](building_clock.md): which costs
move and by how much), `docs/cybertron2/spec/core/clocks.md`, and `docs/scenario_design.md` (the null arm and the end-state reading).

## In short

- **Bots build at 1/15 and at 1/7.** Every house was finished at every factor, at most two days later than today: a small wattle room
  is 6 units today, 13.5 at 1/15 and 29 at 1/7, and a couple with spare units does it in a week.
- **What stops being done is the big works on land:**
  - the fence round a 6-plot pasture: 24.5 units today, 88 at 1/15, 189 at 1/7;
  - clearing 3 plots of scrub: 30 today, 63 at 1/15, 135 at 1/7.
- **When those works got done:**
  - At 1/15 both were done, about two to three weeks later than today.
  - At 1/7 the scrub field was cleared only in the second autumn, or never, and the fence was unfinished at the end in two seeds of
    three.
  - The granaries and the rooms that had to be added to hold them, built in every seed today, were mostly never built at 1/7.
- **The share of all work spent building** rises from 7 to 12% today to 12 to 18% at 1/15 and 21 to 30% at 1/7. Food work falls by
  about as much, and food at the end falls with it.
- **Deaths did not follow the factor.** The deaths were the bots' food rules and their luck, not the price:
  - a blight on one household's crop;
  - a newcomer household that put its seed and labour into a poor field of its own instead of the harvest wages that kept it alive
    in the null arm.
- **The weir got cheaper, not dearer.** Sized to a large river's take, it costs at 1/7 what it costs today (23 units against 24),
  and less at 1/15 (11). It was built in two days in every arm. Its lifts and the traps' together brought in about a third more fish than the traps alone, but the middle runs world still
  starved: keeping the catch binds there, not capital.
- **The arithmetic says more than the bots.** At 1/15 the fence's yearly mending alone (22 units) costs more than the herding it
  saves (about 20 units a year in these runs), so the fence never pays, and at 1/7 (47 a year) still less. So the proposal's
  companions should come before works are raised: cheaper ways to protect crops, and clearing a plot at a time. The fence and the
  scrub field show why.
- **What bots cannot say:** whether agents will begin a 30-unit house or a 135-unit clearing at all. The bots always begin, never
  give up, and build whenever their stores hold a few nights' food. The live evidence so far, a weir asked for three times and
  never begun, is about beginning, and the bots cannot read it.

## 1. Method

### 1.1 The switch

`cybertron2/engine/capital_clock.py` (worktree), applied at the end of `data.py` when the environment variable `C2_CAPITAL_FACTOR`
is set:
- **The unit cost.** Each capital work's units become its real hours x the factor / 2 (a unit is 2 hours, D2-275), with a floor
  of 1 unit (the audit's issue 3).
- **Real hours** are the middle of the audit's range for each row (its §1.1).
- **What it reprices:** rooms by structure, fittings (beds, hearth, bins, granary, oven, cellar, smoke racks, brine pan, millstones,
  water wheel, vault and the rest), monuments, the weir's sections and footing, fences, clearing to field and clearing for
  building, ditching and terracing.
- **What it keeps:** gear and tools (`make` recipes, ITEMS lives) and every material.
- **Upkeep:** what is a share of the build (a fence's mend, a weir's mend) moves with the build. A house's repair is kept (the
  audit: it already sits at about the rule's figure).
- **Departures, named in the module:**
  - the weir is priced at a large river's take (325 real hours for a first wattle section, the audit's 150 to 500), keeping today's
    ratios between its parts. At the audit's research size (36 to 51 hours) it would fall to the floor at every factor;
  - clearing for building has no row in the audit: turf at the field-clearing row x 4/6 (today's ratio), scrub at scrub
    clearing's;
  - the camp is kept.

The arms:
- **null:** no building layer, today's prices;
- **today:** the engine's prices;
- **f40, f15 and f7:** real hours x 1/40, 1/15 and 1/7.

f40 is the proposal's "about today" on average, but **it is not today**:
- the light rooms are about the same;
- turf clearing and the small fittings are much cheaper (they fall to the floor);
- the fence is dearer.

What the works cost in each arm (units of work):

| Work | today | 1/40 | 1/15 | 1/7 |
|---|---|---|---|---|
| small room, wattle | 6 | 5.1 | 13.5 | 28.9 |
| small room, timber | 6 | 7.3 | 19.5 | 41.8 |
| a small room added to a timber house | 4.5 | 5.5 | 14.6 | 31.3 |
| medium room, timber | 15 | 12.9 | 34.5 | 73.9 |
| hearth / beds (each) / granary floor | 3 / 1 / 4 | 1 / 1 / 1 | 1 / 1 / 1.2 | 1 / 1 / 2.6 |
| cellar / oven / smoke racks | 6 / 12 / 2 | 6.2 / 1 / 1 | 16.5 / 1.8 / 1 | 35.4 / 3.9 / 1 |
| weir, first wattle section (large take) / an added wattle section | 24 / 16 | 4.1 / 2.7 | 10.8 / 7.2 | 23.2 / 15.5 |
| wood fence round a size-1 field / round a 6-plot pasture / round the 18-plot East Field | 10 / 24.5 / 42.4 | 13.5 / 33.1 / 57.3 | 36 / 88.2 / 152.7 | 77.1 / 189 / 327 |
| clearing 3 plots of meadow / of scrub to field | 18 / 30 | 3 / 23.6 | 7.2 / 63 | 15.4 / 135 |

**The `verbs.cost` truncation and the act.**
- `verbs.cost` takes `int(TECHNIQUES[tech]["units"])` (verbs.py:142), so a `make` recipe under 1 unit is free. Gear is kept here,
  so it did not bite.
- What does bite: a `build` act costs a flat 2 units (verbs.py:23, VERB build `cost: 2`) and puts in 2 x skill of work
  (verbs.py:1259, 1354, 1381). A fitting priced at the 1-unit floor still takes a whole 2-unit act from one person: the real floor
  is 2 units, not 1.
- Fences and clearing are `work` acts of 1 unit each, putting in the tool's and the skill's multiplier (bare hands 0.4 to 0.5), so
  they truncate nothing. But a household without tools needs 1.4 to 2 times their units: in one seed at 1/7, 260 units of
  fencing put up 174 of the fence's 189.

### 1.2 The bots

- **The engine's own livelihood bots** (`bots_livelihood.py`, W-69) have only the `runs` policy, and it never builds.
- **The smoke-test bot** (`run.bot_plan`) leaves `build` out of its options on purpose (knowledge.py:421).
- **So no bot in the repository builds.** I wrote, in the worktree:
  - **a farming policy, `farm`** (`bots_build.py`): plain rules, a fair player. Every member reaps the household's ripe crop.
    The head sows its empty plots in sowing time, only a crop that will ripen before winter stops it, and only seed above the food
    the household needs until that harvest. A growing crop is weeded up to 4 units a plot. The cows in milk are milked. The
    youngest herds a herd that no shut fence holds while a crop stands, and keeps the firewood up. Hay is cut in summer. What is
    in hand goes into the house's store. A household with no ripe crop of its own helps at a neighbour's harvest and gives the
    holder half: a custom of the fixture, without which the Millers, who hold no field, starved.
  - **a building layer** for any policy, between its food work and its fallback of wild food. Each household works down a fixed
    list of projects with the units left after the day's food work, while its stores hold 4 nights of food (a sensitivity arm:
    16). Timber short for a project is felled first. The list:
    - a house where it has only a camp: a small wattle room, a hearth, then a bed a member. This and the field take 2 units an
      adult a day even when food is short;
    - a field where it holds none (clearing);
    - a fence round its herd's pasture;
    - a granary when its grain is over what its bins hold by 60, adding a room first when the floor is full;
    - in the runs world, a weir by the Brooks with the Marsh head as crew, then its three added sections.
  - **an old-wild-food fallback** (`forage` and `hunt`) for worlds that predate the wild layer.

### 1.3 The worlds

Three worlds with building, 64 days each (two world years). Three seeds for each arm (the world's seed x 100 + 1, 2, 3).
`runs_w82/worlds/make_w82_worlds.py` writes them.

| World | From | What gets built | Fixture's changes |
|---|---|---|---|
| **frontier_w82** (farm, a founding) | `specs/frontier_camps.yaml` (Zach's 2 Nov world): three couples in camps that last to day 14, a scrub knoll, a meadow lea, a wood | a house each (room, hearth, beds), the lea cleared to a field, a granary and the room for it | the Gorm raiders removed; each couple carries 80 grain, 20 beans and 25 dried meat instead of 30, 10 and 10 (as written, every bot starved by day 20 in every arm: the world is on the old wild food, and its forage cannot feed six) |
| **brookend_w82** (farm, settled) | `specs/plenty/brookend.yaml`: three households, two fields, a herd on an unfenced pasture, a mill | the Crofts' fence round Long Pasture, granaries (with a room added where the floor is full); and a fourth household | a newcomer couple, the Wrights, in a camp on the Green (lasts to day 10) with seed, a little timber, stone and straw, and an unclaimed scrub parcel (the Brakes, 3 plots) to clear for their field |
| **runs_w82** (the runs world) | `specs/nutrition/runs_medium.yaml`, the middle arm (no weir seeded) | a weir across the Isel by the Brooks and the Marshes, then its three added wattle sections | the `runs` policy with the layer |

### 1.4 What is measured

- **Units.** The worktree's `run.py` writes every act done with its units to `actlog.jsonl` (`C2_W82_ACTLOG`). The journal's
  results cannot be lined up with the acts (fault 3).
- **Works.** What was begun and finished, and when, comes from the act log and the days' records. What was left unfinished comes
  from the end state.
- **Households housed:** a household holding a finished non-camp building with beds at the end.
- **Food at the end:** in all stores and hands, in food.
- **Where it is kept:** `runs_w82/batch.py` runs the batch; `measure.py` and `summary.py` make the tables. Every run is kept whole
  under `/home/user/c2-w82/runs_w82/<world>/<arm>_s<seed>/`, with `measure.json`, `arm.json` and `actlog.jsonl`. The batch's
  tables are in `runs_w82/summary.md`. 69 runs, 3.2 GB.

## 2. The tables

Columns:
- "build share": build units over all units of work.
- "food units": all food work (reaping, sowing, weeding, milking, herding, hay, fishing and its lifts, keeping, forage, hunting).
- "timber units": felling, kept apart: on the day clock in every arm.

### 2.1 frontier_w82 (a founding; 3 seeds, 64 days)

| arm | alive / people (each seed) | deaths (all seeds) | households housed at the end | food at the end | missed meals | build units | timber units | food units | build share of work |
|---|---|---|---|---|---|---|---|---|---|
| null | 0/0/0 of 6 | starvation 18 | 0of3/0of3/0of3 | 0 | 23.3 | 0 | 0 | 236 | 0% |
| today | 6/3/5 of 6 | old age 2, starvation 2 | 3of3/2of3/3of3 | 200 | 3.0 | 136 | 89 | 622 | 12% |
| f40 | 6/4/5 of 6 | old age 3 | 3of3/3of3/3of3 | 309 | 0.0 | 75 | 54 | 737 | 7% |
| f15 | 4/4/5 of 6 | old age 3, starvation 2 | 2of3/3of3/3of3 | 239 | 2.7 | 138 | 66 | 702 | 12% |
| f7 | 6/4/5 of 6 | old age 3 | 3of3/3of3/3of3 | 167 | 1.7 | 249 | 102 | 569 | 21% |

The 16-night arms gave the same runs as the 4-night ones: the provisioned couples always held more than 16 nights.

Days the works were finished: each seed, one entry for each household; `-` never.

| arm | houses (small room) | hearths | fields cleared | a room added | granaries |
|---|---|---|---|---|---|
| today | 3,3,3 / 3,3,3 / 3,3,3 | 5,5,5 / 5,5,5 / 5,5,5 | 3,3,3 / 3,3,3 / 3,3,3 | 17,17,17 / 17,17 / 17,17,17 | 20,20,20 / 20,20 / 20,20,20 |
| f40 | 4,4,4 / 4,4,4 / 4,4,4 | 5,5,5 / 5,5,5 / 5,5,5 | 1,1,1 / 1,1,1 / 1,1,1 | 9,9,9 / 9,9,9 / 9,9,9 | 15,15,15 / 15,15,15 / 15,15,15 |
| f15 | 4,4,4 / 5,5,5 / 5,5,5 | 5,5,5 / 6,6,6 / 6,6,6 | 2,2,2 / 2,2,2 / 2,2,2 | 15,15,15 / 16,16,16 / 16,16,16 | 19,19,19 / 20,20,20 / 20,20,20 |
| f7 | 5,5,5 / 5,5,5 / 5,5,5 | 7,7,7 / 7,7,7 / 7,7,7 | 5,5,5 / 5,5,5 / 5,5,5 | 23,23,23 / 23,23,23 / 23,23,23 | 27,27,30 / 27,29,29 / 27,27,27 |

Build units by work (mean over seeds):

| arm | small room | hearth | beds | clear | granary |
|---|---|---|---|---|---|
| today | 34 | 12 | 24 | 55 | 11 |
| f40 | 30 | 6 | 24 | 9 | 6 |
| f15 | 78 | 6 | 24 | 24 | 6 |
| f7 | 156 | 6 | 24 | 49 | 14 |

### 2.2 brookend_w82 (a settled village with a newcomer household; 3 seeds, 64 days)

| arm | alive / people | deaths (all seeds) | households housed at the end | food at the end | missed meals | build units | timber units | food units | build share |
|---|---|---|---|---|---|---|---|---|---|
| null | 7/10/9 of 10 | sudden illness 2, old age 1, starvation 1 | 3of4 (each) | 73 | 10.0 | 0 | 0 | 1024 | 0% |
| today | 4/8/5 | sudden illness 1, old age 1, starvation 11 | 2/3/3 of 4 | 111 | 15.0 | 116 | 56 | 1063 | 8% |
| f40 | 4/8/5 | sudden illness 1, old age 1, starvation 11 | 2/3/3 of 4 | 105 | 16.3 | 100 | 58 | 1046 | 7% |
| f15 | 5/8/4 | sudden illness 1, old age 1, starvation 11 | 3/3/2 of 4 | 84 | 16.3 | 291 | 58 | 982 | 18% |
| f7 | 5/8/5 | sudden illness 1, old age 1, starvation 10 | 3/3/3 of 4 | 79 | 14.7 | 553 | 27 | 961 | 30% |
| today, 16-night reserve | 6/8/5 | sudden illness 2, old age 1, starvation 8 | 3of4 (each) | 107 | 11.7 | 128 | 68 | 1038 | 8% |
| f15, 16-night reserve | 5/8/7 | sudden illness 2, old age 1, starvation 7 | 3of4 (each) | 90 | 12.0 | 300 | 51 | 982 | 18% |
| f7, 16-night reserve | 5/8/7 | sudden illness 2, old age 1, starvation 7 | 3of4 (each) | 87 | 9.7 | 503 | 25 | 998 | 28% |

Days the works were finished: each seed; `-` never; `(1 left)` begun and unfinished at day 64.

| arm | Wright House | Wright beds | the Brakes cleared (scrub, 3 plots) | fence round Long Pasture | granaries | rooms added (for a granary) |
|---|---|---|---|---|---|---|
| today | 3 / 3 / 3 | 5 / 5 / 5 | 8 / 8 / 7 | 8 / 8 / 13 | 16,21 / 15,21,34 / 15,21,34 | 17 / 17 / 18 |
| f40 | 3 / 3 / 3 | 5 / 5 / 5 | 6 / 6 / 6 | 12 / 14 / 18 | 15,21,28 / 15,21,35 / 15,21,34 | 18 / 18 / 18 |
| f15 | 4 / 4 / 4 | 6 / 6 / 6 | 20 / 19 / 18 | 22 / 23 / 26 | 15,27 / 34 / 15,31 | 27 / 25 / 25 |
| f7 | 5 / 5 / 5 | 7 / 7 / 7 | 38 / - (1 left) / 37 | - (1 left) / 34 / 39 | 16 / - / - | - / - / - |
| today, 16 nights | 3 / 3 / 3 | 5 / 5 / 5 | 8 / 8 / 7 | 23 / 21 / 23 | 16,21 / 21,35 / 17,21,34 | 17 / 17 / 18 |
| f15, 16 nights | 4 / 4 / 4 | 6 / 6 / 6 | 19 / 19 / 18 | 29 / 28 / 32 | 15,29 / 34 / - | 25 / 25 / 25 |
| f7, 16 nights | 5 / 5 / 5 | 7 / 7 / 7 | - (1 left) / - (1 left) / - (1 left) | - (1 left) / 42 / - (1 left) | 15 / 56 / - | - / - / - |

Build units by work (mean over seeds):

| arm | small room | hearth | beds | clear | fence | granary |
|---|---|---|---|---|---|---|
| today | 12 | 4 | 4 | 45 | 40 | 11 |
| f40 | 10 | 2 | 4 | 31 | 47 | 6 |
| f15 | 26 | 2 | 4 | 110 | 145 | 3 |
| f7 | 30 | 2 | 4 | 238 | 277 | 1 |

Who starved, every building arm:
- the Wrights, the newcomers, on days 37 to 46 (both of them in every seed of every building arm, today included);
- in some seeds the Crofts in the second winter (days 53 to 61).

In the null arm the Wrights lived, unhoused after day 10, on the harvests they helped bring in.

### 2.3 runs_w82 (the runs world's middle arm; 3 seeds, 64 days)

| arm | alive / people | deaths (all seeds) | food at the end | missed meals | build units | food units | build share | weir finished | its 3 sections finished |
|---|---|---|---|---|---|---|---|---|---|
| null | 2/0/1 of 12 | sudden illness 3, neglect 3, old age 6, starvation 21 | 10 | 35.7 | 0 | 1188 | 0% | - | - |
| today | 2/3/1 | sudden illness 3, neglect 3, old age 8, starvation 16 | 11 | 28.7 | 72 | 1273 | 5% | day 2 (each seed) | day 4 |
| f40 | 2/3/1 | sudden illness 3, neglect 3, old age 8, starvation 16 | 12 | 22.3 | 18 | 1259 | 1% | day 2 | day 4 |
| f15 | 2/3/1 | sudden illness 3, neglect 3, old age 7, starvation 17 | 14 | 27.3 | 36 | 1268 | 3% | day 2 | day 4 |
| f7 | 2/3/1 | sudden illness 3, neglect 3, old age 8, starvation 16 | 11 | 28.7 | 72 | 1273 | 5% | day 2 | day 4 |

- **Seed 1, null against today:** the lifts (traps and weir together) brought in about 1,380 kg of the catch against about 1,000
  from the traps alone, and the deaths came a few days later.
- **The bots' starvation in this arm** was known before the weir (02zzz: all dead by day 36 on 20 Nov): keeping the catch binds
  there.
- **The weir was built from the 28 timber seeded in each house.** No felling was needed.

## 3. Reading

**1. Do bots build at 1/15 and 1/7? Yes, the houses; the big works on land, late or not at all.**
- **Houses.** A wattle house with hearth and beds took the frontier couples days 2 to 6 at today's price and days 2 to 8 at 1/7 (the room
  finished on day 3 against day 5, the hearth on day 5 against day 7).
  The Wrights' house was done by day 5 at 1/7 in every seed. A house fits in the units a couple has left over, at any of the three
  factors.
- **The works priced by land, which the rule raises most:**
  - the Croft fence round Long Pasture (6 plots): built by day 8 to 13 today, by day 22 to 26 at 1/15. At 1/7 it was done by
    day 34 to 39 in two seeds and unfinished in the third;
  - the Wrights' scrub field (3 plots): cleared by day 8 today, by day 18 to 20 at 1/15. At 1/7 it was cleared only on day 37 or
    38, or never. That is the second year's autumn, so a household that came for a field had none to sow in its first year.
- **What the queue drops.** The granaries and the rooms added for them, at the end of the queue, are what the dearer works crowd
  out:
  - today: two or three granaries a seed;
  - at 1/15: one or two;
  - at 1/7: one in three seeds, and no added room.
- **The founding.** On the frontier, the field is meadow: turf clearing is cheap under the rule (2.4 a plot at 1/15 against 6
  today), so the founding's critical path gets shorter at 1/40 and 1/15 and only slightly longer at 1/7. That is why f40 did best
  there: its field was ready on day 1 and the seed went in two days sooner.

**2. What crowds building out (in these bots).**
- **The day's food work comes first, by the rule:**
  - the harvest crunch: reaping the 18-plot East Field takes 144 units in its two-day window;
  - the second year's winter.
- **Timber.** Its getting is on the day clock in every arm and is as large as the building at today's prices (frontier today: 89
  units of felling against 136 of building). The crude tool's 10 uses (data.py:102, with `fell` wearing 1 a use) run out during a
  founding's felling, and then felling is bare-handed at a quarter the rate (frontier, today, seed 1: 42 of 48 fellings bare-handed).
- **Tools and hands on fences and clearing.** Bare hands put in 0.4 to 0.5 of a unit's work, so a toolless household pays up to
  twice the price.
- **What the factor does.** It moves the big works across a seasonal line:
  - a field cleared after the sowing window is a year lost;
  - a fence finished in the second year protected nothing in the first.

**3. Deaths and food.**
- **Food at the end falls as works get dearer:**
  - frontier: 309 at 1/40, 239 at 1/15, 167 at 1/7;
  - Brookend: 105, 84, 79;
  - over the same range the build share of work rises from 7 to 21% (frontier) and from 7 to 30% (Brookend).
- **No death in these runs followed the factor.**
  - The frontier's starvation (two deaths in one seed of today and one of 1/15) was one household's crop failing to the blight
    draw (D2-53).
  - The Wrights starved in every building arm, today's included. This was the fixed rule, not the price:
    - a household with 4 nights' food in reach builds, clears and sows its own poor field (scrub-cleared, fertility 0.85, sown
      late with little seed);
    - and it gives up harvest wages at its neighbours';
    - in the null arm it never had a field, so it lived on those wages.
  - The 16-night reserve saved a few lives at every factor alike (starvation 11 to 7 or 8), and pushed the fence later.
- **Read against the null arm** (scenario_design.md), the building layer at today's prices already costs Brookend lives with this
  policy. So the bots say "the rule raises the share of work in building as the audit priced it", not "the rule kills".

**4. The arithmetic that matters more than the bots.**
- A fence needs mending at a quarter of its build a year (D4-114). Round Long Pasture that is 6 units a year today, 22 at 1/15 and
  47 at 1/7, against herding that cost the Crofts about 20 units a year in these runs.
- **At 1/15 the mend alone exceeds the herding the fence replaces.** No fence pays in Brookend at 1/15 or 1/7, before its build
  (88 or 189 units) is counted.
- The proposal's cheaper crop protections (herding by children, dead hedges, folds, a fence by its length) are therefore not
  optional for stage 3 (D2-281's raise to 1/15) where herds and crops share a node.
- Scrub clearing at 1/15 is 21 units a plot, a fortnight of a couple's spare units for a 3-plot field. Clearing a plot at a time
  (OPEN L-153) would let them sow the first plot that season.

**5. The weir.**
- At the large-take size the rule leaves it about where it is at 1/7 and halves it at 1/15. At the research size it would be at
  the floor.
- The bots built it in two days in every arm: a whole village's spare units, 12 timber in store.
- So the price is not what stops agents building weirs (crafts_evaluation.md §7). The size question (the weir sized to its take,
  D2-262) decides whether the rule raises or lowers it.

## 4. What bots cannot tell us

- **The bots follow a fixed list and always begin.** Whether a person begins a 30-unit house, a 135-unit clearing or a 189-unit
  fence depends on things the bots do not have:
  - whether they see the cost and the payback (the prompt shows a work's units);
  - their plans across days;
  - whether they trust a crew.
  The live evidence that matters (the weir asked for three times and never begun, the racks one unit short) is about beginning and
  keeping on, and no bot run reads it.
- **They never give up a half-built work, and never take one up because a neighbour has.**
- **They do not trade labour, hire a builder or pay in kind.** Builders as a trade, the proposal's first companion, is the obvious
  answer to dearer works, and bots cannot show it.
- **Their food rules are mine.** Every death here traces to one of them:
  - the 4-night reserve;
  - the half-share harvest custom;
  - sowing only seed above the food until harvest;
  - no hunting in the frontier fallback, because the old wild food's hunt is poor unarmed.
  Agents would do better at some of this and worse at some.
- **They know the year perfectly** (what ripens before winter) **and never misjudge a price.**
- So the bots give **the cost side** (units, days, what the queue drops, food left), **not the choice side.** D2-281's short live
  run is still needed for "does building still happen".

## 5. Faults and rough edges hit (engine and data)

1. **A work under 2 units costs 2 anyway.** A build act is a flat 2 units (verbs.py:23) and puts in 2 x skill (verbs.py:1259, 1354,
   1381). Under the rule about 25 rows fall to the 1-unit floor (the audit's issue 3), and each still takes a whole 2-unit act from
   whoever starts it. The floor is effectively 2. (`verbs.cost`'s `int()` at verbs.py:142 truncates `make` recipes under 1 to 0;
   that is not reached here, as gear was kept.)
2. **The weir's first-section cost is held twice.** MONUMENTS `weir` (data.py:345: 12 timber, 24 units) and WATER_WORKS
   `position.first` + `material.wattle` (data.py:376: 6 + 6 timber, 8 + 16 units) must agree by hand. A wattle first section is
   charged from MONUMENTS and a timber one from `gear.cost` (verbs.py:1007 to 1014). The switch had to set both.
3. **The journal's results do not line up with the acts.** A refused act repeated in a plan is skipped with no line
   (run.py:1008), and a refusal whose text repeats an earlier one adds none (run.py:1036). The units a person spent on each act
   cannot be read back from `turns.jsonl`. The worktree adds an act log in `run.py` (environment variable `C2_W82_ACTLOG`).
   Recording each act's units with its result would serve every bot and live reading.
4. **A build technique's shown units go stale if the table changes.** The `build` rows are copied from BLUEPRINTS, FITTINGS and
   MONUMENTS at import (data.py:721 to 724), so a later change to those tables leaves the units shown in prompts stale. The
   switch rewrites them. Any calibration tool that edits the tables after import would hit this.
5. **A dead parameter:** `PHYSICS.cattle.stray` (data.py:825, listed as a day rate in clocks.py:25). Nothing reads it; herds wander
   by `herds.wander`.
6. **Not engine faults, but they blocked a fair bot reading:**
   - `frontier_camps.yaml` (2 Nov) is on the old wild food (`forage`, `hunt`) and cannot feed six bots: as written, every arm
     starves by about day 20;
   - Brookend's Millers hold no field and live by the mill, which bots cannot trade with;
   - no farming or building livelihood bot exists, so farm worlds have no null arm of the W-69 kind.
7. **The crude tool's life of 10 uses** (data.py:102; the audit's 20 to 70 under the rule) wears out in a founding's felling. Then
   timber, unchanged by the rule, costs four times as much.

## 6. Questions for Zach

1. **Whether the first stage raises all works to 1/15 at once, or the houses and fittings first** (the staging, D2-281).
   - The bots build houses at 1/15 within a week.
   - The fence round a pasture and a scrub field slip by two to three weeks.
   - At 1/15 the fence's yearly mend alone costs more than the herding it replaces, so it never pays.
   Options:
   - (a) raise everything to 1/15 now;
   - (b) raise rooms, fittings, cellars and the weir now, and hold fences and scrub clearing at today's price until their
     companions are built;
   - (c) wait for all the companions.
   **Recommend (b):** it is what the proposal's stage 2 asks, and the bots show it is the fence and the clearing that break.
2. **Which cheaper crop protection to build first, before fences are raised** (the proposal's open question 5).
   - Options: (a) herding by children (the household's order exists; it needs only the children's work to count as herding);
     (b) a dead hedge, cheap and gappy, lasting 2 to 3 years; (c) a fence priced by its length, so a small close costs less than a
     field; (d) movable hurdle folds.
   - **Recommend (c) with (b):** the fence's price is the problem, and a dead hedge gives the cheap-and-worse choice. Herding
     already works in the engine.
3. **What size the weir is priced at** (the weir sized to its take, D2-262 and D2-210).
   - Options: (a) the research size (a 10 m section): the rule puts it at the 1-unit floor; (b) a large river's take (the
     switch's choice): at 1/7 it costs what it does today, at 1/15 about half; (c) sized by each river's flow.
   - **Recommend (b) now and (c) later:** it keeps the weir a real work, and the bots show its price is not what stops it.
4. **Whether a build act can cost less than 2 units when less work is left** (fault 1).
   - Options: (a) keep the 2-unit act; (b) an act costs what is left, rounded up to a whole unit; (c) small fittings made in
     batches with one act.
   - **Recommend (b), with (c) for beds and stalls (they already take `qty`):** without it the rule's 1-unit floor is a 2-unit
     floor.
5. **Whether to keep the farming bot and the building layer as test tools** (a null arm for farm worlds, as the runs bots are for
   the runs world, W-69).
   - Options: (a) merge them, under the W-69 seams, after review; (b) leave them on the branch for this reading only.
   - **Recommend (a):** with the act log (fault 3), they give every farm world a free null arm. The half-share harvest custom and
     the sowing rule are mine and would be named as the bots' own customs.
6. **What to do with the frontier world** (`frontier_camps.yaml`, Zach's 2 Nov world). It predates the wild layer and the food
   units of D2-258, and starves bots as written.
   - Options: (a) remake it on the current wild layer; (b) retire it; (c) keep it as written for live runs only.
   - **Recommend (a)** before any live founding run: it is the cleanest test of whether houses and fields still get made.
7. **The short live run D2-281 asks for: which world, and when.** It costs money.
   - Options: (a) Brookend with the newcomer household, at 1/15, about 20 days, against a bot null arm; (b) the remade frontier;
     (c) wait until the companions are in.
   - **Recommend (c) then (a):** at 1/15 the live run would mostly find out what the bots already show about fences and clearing.
8. **Whether tool lives move with this stage or before it** (the audit's tool and plough lives).
   - Options: (a) with this stage; (b) before it; (c) after.
   - **Recommend (b):** the crude tool's 10 uses wear out in a founding's felling, and the dearer works lean on felling.

## Files

- **The worktree** `/home/user/c2-w82`, branch `w82-clock-bots` (local, not pushed, not merged):
  - `cybertron2/engine/capital_clock.py` (the switch);
  - `cybertron2/engine/bots_build.py` (the farm policy and the building layer);
  - `cybertron2/engine/bots_livelihood.py` (the layer's hook and the old-wild-food fallback);
  - `cybertron2/engine/data.py` (the switch's hook, at the end);
  - `cybertron2/engine/run.py` (the act log).
- **`runs_w82/`:**
  - `worlds/make_w82_worlds.py` and the three worlds;
  - `batch.py`, `measure.py`, `summary.py`, `summary.md`;
  - every run's directory, kept whole.
