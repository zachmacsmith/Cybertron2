# Five monoculture worlds for 200-day runs

**Status:** discussion (23 Nov 2026). Designs only: nothing generated or built.
**Owner:** bench. Generation and the wild are 37.2's; the life rules are 37.4's.
**Thread:** monocultural benchmark worlds (W-103); the frame is proposals/monoculture_worlds.md; the aim is D5-1.

## Summary

Zach (23 Nov): "design one or two monoculture worlds ... each should have a large prebuilt world most of it unexplored so there is
more to expand into if they want and get different resources etc, but the different types of geography / topology of the worlds or
which resources are accessible or which livelihoods start (eg largely fishing or farming or mixed start, which capital and techniques
they start with). Design maybe 3-5 of varying complexity of which different types of mechanics start in or how the villages are
distributed across it etc. designed aiming to run for like 200 days".

Five worlds, simplest first. Each is one people under one model, starting small (9 to 15) in a prebuilt land of 16 to 26 places,
most of them unexplored.

| # | World | Land | Start | Livelihoods at the start | Spread | What it mainly tests |
|---|---|---|---|---|---|---|
| 1 | **Fallowmere** | lowland river and frontier wood | spring | farming, cattle, woodcraft | one village | the baseline: farm well, survive the first winter, found households, choose new land |
| 2 | **Eelmouth Reach** | estuary with river runs | late summer | fishing (weir, traps), salt; no fields, no cattle | one village | a glut and its keeping; leaving a capped livelihood for the land upriver |
| 3 | **Highfold** | two mountain valleys over a pass | early summer | cattle and hay; a smith and quarry | two hamlets a day apart | the long winter; seasonal travel; going down to better land |
| 4 | **Oldbury** | chalk downs and a clay vale | spring | mixed: mill, smithy, plough, herd, all inherited | one village built for 30, holding 9 | recovery; knowledge held by the old, passed on or lost |
| 5 | **The Scattering** | a region: coast, great wood, moor, river vale | spring | one livelihood per group: fishing and salt, hunting, herding and copper, farming | four groups, unexplored to each other | exploration, reconnection, trade and marriage between groups |

## 1. What every world shares

**The settings.**
- `days: 200`; `life.lifespan: 64`; `calendar.season_days: 8`. The year is 32 days and the run is about six years. The calendar must
  be set explicitly, since the engine's fallback is 6 days a season (`world.py:97`).
- `children: {on: true, dial: low}`; `ages: true`; `view: beliefs`; `evening: true`; `tags: true`.
- `memory.kept.words: 80`, so the goal line is kept whole.

**The aim (D5-1).** Every founder keeps the runs world's line for good (`make_runs_models.py` GOAL):

> YOUR GOAL, on which you will be graded: grow your line, everyone descended from your household's founders, to be as many as you
> can, and see them survive and spread over as many generations as you can. Your score is the number of people descended from your
> household's founders who are living at the end of day 200, in whatever household or place they live: the more, the better.

**The cast.** Every person is played by one model:
- `household_models` sets every household to it;
- `cast` sets head, middle, rest and youth to it;
- so no youth or household founded in the run falls back to Haiku (the pitfall in `generate.py:372-395`).

**Founders' ages.** Ages are mixed, so the founders do not all turn elder together, as they did in pw1.

| At lifespan 64 | Infant | Child | Youth | Adult | Elder |
|---|---|---|---|---|---|
| Age in days | 0 to 4 | 4 to 12 | 12 to 24 | 24 to 64 | 64 on |

- Founding adults are aged 28 to 56, so they turn elder from about day 8 to day 36.
- Every world seeds youths and children who come of age in the first 20 days.
- By day 200 every founder will most likely be dead. The score is the people born in the run, about three generations.

**Partners.** Every founding youth has at least one possible partner of the other sex outside their household (monoculture_worlds.md
§4 principle 7). World 5 is the exception, and that is deliberate.

**Explored and unexplored.**
- Home and the places within a day are known. Places beyond them are `unexplored: true` (D4-47): they are known only by going there
  (anyone may walk an unexplored way), by being told, or by a seeded line.
- **Rumour lines** are part of the founders' 20-line budget (D2-308, D2-311). A few founders carry a line about a place they have
  never seen, true but vague: "the old men said there is good black land two days up the river, where it bends." A place named in
  speech is learnt by those who hear it (`run.py:338-349`), so rumours spread by talk.

**The room to grow.**
- No place can be made in a run, so every world lays its vacant places in advance (`vacant: true` with `room`, `settle.py:572`).
- There is enough room that a well-run people does not run out before day 200. Each world's ceiling is at least five to eight times
  its founders.
- A place's land is about 12 cells of about 2 ha for each household of room (`VACANT_CELLS`).

**Starting stores.**
- Food in store lasts to the first harvest or catch at about 1.15 times the founders' need (scenario_design §4). The first winter can
  be survived with care, not without it.
- Every world starts so that the first lean season comes after its first chance to put food by.

**Checks before any run.**
- the gate check (`landgen/gate_check.py`);
- the settle probe on every vacant place (`specs/peoples_settle_probe.py`);
- the capacity ladder per place (`cybertron2/capacity/`: bare, standing, worked, best, ceiling);
- a 200-day bot arm, which is the null arm and tests the interfaces (D2-298).

**Size.** Roads are in whole days, at about 18 km a day on the flat and 15 over hills (peoples_design.py).
- Worlds 1 to 4 fit a window of 100 to 120 km. World 5 needs about 140 km.
- The largest world generated so far was 95 km, and generation took about 60 s (02zzf). A 140 km window has about twice the cells.
  It is untested and may need cells of 0.2 to 0.3 km.

## 1a. World 0: Highpool and Middleham, the first run (two villages, fishing and farming)

Zach (23 Nov): "Can the first one we do be relatively small, but two connected villages with both fishing and farming since I haven't
[tested] the dependencies yet". This world goes before the five. Its point is the dependence between a fishing village and a farming
village, a day apart, under one model. That has not been run on the rebuilt engine: live run 1 is water-only (D2-316).

**Reading taken:** one village fishes and boils salt, the other farms and mills. Each can do a little of the other's work (the
fishers can clear scrub to a plot; the farmers can fish the shallows), so the dependence binds without being absolute (scenario_design
§4). The other reading, both villages mixed, would test less dependence; it is kept as a later mirror arm.

**Land.** The runs world's land (`specs/water/runs.yaml`; generated, its seed kept): one river with eel, salmon and lamprey runs, a
brine spring, a mill. It is small, known and already run (pw1's runs world; W-58's 30 days). Ten places:

| Place | Roads | Land | What it holds | At the start |
|---|---|---|---|---|
| **Highpool** | Middleham 1; Thornholt 1; Stanwood 1; w4 1 | fen, meadow, pasture, scrub, forest, water; **no field** | the brine spring and the Salt House; Brook's Forge; the river's runs | the fishing village, known |
| **Middleham** | Highpool 1; Lowstrand 1; Hartcliffe 1 | field, meadow, pasture, fen, forest, water | three fields; the water mill | the farming village, known |
| Lowstrand | Middleham 1 | field, meadow, pasture, fen, forest, water | two fields and three houses, empty | **unexplored**; an empty village to take over |
| Stanwood | Highpool 1; w2 1; w3 1 | river flats: forest, heath, meadow, pasture, rock | rock (stone), wood | unexplored, vacant |
| Hartcliffe | Middleham 1 | river flats: forest, meadow, rock | rock, wood | unexplored, vacant |
| Thornholt | Highpool 1; w1 1; w4 1 | clay vale: forest, meadow, pasture, rock | wood, pasture | unexplored, vacant |
| w1 to w3 | 1 day beyond Thornholt and Stanwood | old forest | game, timber | unexplored (as generated) |
| w4 | Highpool 1, Thornholt 1 | broken hill country: rock, scrub | stone | unexplored (as generated) |

The land is small (two villages, an empty one, three vacant places, four wild). Its ceiling may bind before day 200. In a first run
that is a finding about the dependence, not a fault; the five larger worlds are where room to expand is the test.

**Founders: 14 in 4 households, all one model.**

| Village | Household | People (age in days) | Livelihoods (u11 rows) | Capital | Holds the chokepoint |
|---|---|---|---|---|---|
| Highpool | Brook | head 50 (m), wife 40, son 20 (youth), daughter 9 | salter (the pan); fisher (hand, rod) | the Salt House and brine pan, salting tub, Brook's Forge, copper tools | **salt**, the forge |
| Highpool | Marsh | head 44 (m), wife 36, daughter 18 (youth) | fisher (weir and nets; keeping) | the weir (wattle), gill net, wicker traps, smokehouse | **the weir** |
| Middleham | Field | head 46 (f, widowed), brother 34, son 21 (youth), daughter 15 (youth) | farmer (ploughman; seed and harvest); herder | 2 fields, bins, ox pair and plough, the Field Byre, 4 cows and a bull, hay | **the plough team**, the cattle |
| Middleham | Fletcher | head 56 (m, elder about day 8), daughter 30, her son 6 | miller; farmer (broad) | the mill, oven, 1 field | **the mill** |

- Partners cross the villages: Brook's son with Field's daughter, Field's son with Marsh's daughter.
- Within each village the two households are rough in each other's broad crafts (u11 §5.7's neighbours).
- Across the villages, each knows the other's trade by name only, plus one seeded line each of the old exchange ("Middleham sends
  grain at harvest for salt and smoked eels"). This seeds that trade has happened, not what to do now.
- The miller is old: the mill's knowledge passes to his daughter or is lost.

**The dependencies under test.**

| Flow | From | To | Why it matters |
|---|---|---|---|
| Salt | Highpool (the pan) | Middleham | salting beef and the farmers' share of the fish; without it meat keeps days, not a season |
| Grain and flour | Middleham (fields, mill) | Highpool | food between the runs; shallows alone do not feed the fishers (D2-316) |
| Smoked and salted fish | Highpool (the weir, the runs) | Middleham | the farmers' winter and their lean spring |
| Hides | Middleham (cattle) | Highpool | rods and leather; angling is 1.5 a unit against 0.6 by hand (75_lake_run2 §run 2) |
| Tools mended | Highpool (the forge) | Middleham | copper tools and the plough wear |
| Oxen hired | Middleham | Highpool | carrying (a pack ox), clearing scrub to a first plot |

Each village can survive the first year alone, poorly: the fishers on the runs and the shallows, the farmers on grain and milk. The
headroom (more children, a third household, taking Lowstrand) needs the exchange. Every link has a person who can withhold it, so
terms, debts and agreements are possible but not seeded.

**Start and length.** Summer day 4 of the runs world, with grain standing and the harvest soon. The eel run comes in autumn, so both
villages put food by before the first winter. Stores at home last to the harvest and the run at about 1.15 times need. 200 days.

**What it reads.**
- Whether the flows above happen, how often, and on what terms (the agreements, gives and trades in `days.jsonl`).
- The population of each village and in all; who holds food at the end.
- Whether the empty village (Lowstrand) is found and taken, and by whom.
- The share of acts on food.
- The mill's and the forge's knowledge after their keepers die.

**Arms.** This model's run, plus:
- the 200-day bot arm, the null arm;
- a cut arm with the road between the villages closed. It is free with bots, and with a model it is the cleanest test that the
  dependence binds. *Recommend:* run it with bots only at first.

**How it would be built.** A maker beside `make_eelmouth.py` and `make_runs_models.py`:
1. Start from `water/runs.yaml`.
2. Keep two households a village and trim them to the table. Take Lowstrand's people out and leave its houses and fields empty.
3. Mark the other places unexplored, and pin the skills by u11 (`skills.households`).
4. Couple capital with memory (D2-311), set the cast to one model, and seed the goal line (D5-1).
5. Settings: `memory.kept.words` 80 so the goal is whole, `days: 200`, `calendar.season_days: 8`.

**Gaps.**
- **The farming half has not run on the rebuilt engine.** Live run 1 is water-only. The eleven act shapes, the household book and
  the core prompt must be checked on farming work (sow, reap, plough, herd, mill, bake) with bots first.
- The goal line needs 80 words; the rebuilt worlds keep lines at 40 (D2-308). Either the goal is a protected line of its own length,
  or the cap is raised for this world.
- Where the weir stands against the runs (D2-210: weirs take in order up the river) is to be checked in the land, so that Highpool's
  weir is not left with what Middleham's shallows take first.
- The action fixes (W-102) first, as for every world.

## 2. World 1: Fallowmere (the baseline; the fewest systems)

**Idea.** A farming village of three households on a river, at the edge of wild wood. The land at home feeds them with a little to
spare. Everything beyond a day is unexplored, and most of it is better than home. The plainest test of the long run: farm well, keep
food through winter, have children, found households and settle new land.

**Land.**
- Lowland river country (calibration w01: `plain`, 900 mm, 9 °C) under `settled lowland and frontier`, with `settled: frontier`
  (wood share 0.6).
- Mild winters, some frost, spates about once a year.
- Packs: farming (the default), wild (game, wolves, boar, forage), water (shallows only; no runs, no salt).

**Founders: 13 in 3 households.**

| Household | People (age in days) | Livelihood | Capital | Specialism |
|---|---|---|---|---|
| Ashby | head 52 (m), wife 40, son 20 (youth), daughter 9, infant | farmer | 2 fields, bins, ox pair, wooden plough, byre | ploughman; seed and harvest |
| Reeve | head 36 (f, widowed), brother 30, daughter 18 (youth), son 6 | farmer and herder | 1 field, 4 cows, a bull, hay meadow, hens | dairy; hay and winter |
| Colle | head 44 (m), wife 34, son 22 (youth) | woodsman and builder | axe, saw, timber, woodshed | felling; building |

- Youths: Ashby's son and Reeve's daughter could pair; Colle's son needs Reeve's daughter or must look further, which is a reason to go.
- Seed grain is held: one field's worth spare at Ashby.

**Map: 18 places, 3 known.**

| Place | Days from home | Land | Resources | Room (households) | Note |
|---|---|---|---|---|---|
| **Fallowmere** (home) | 0 | farmland | grass, wood, fish (shallows) | 3 | known |
| Fallow Wood | 1 | forest | wood, game | 1 | known |
| Southmead | 1 | rich vale | grass, fish | 2 | known; vacant meadow, the first easy step |
| The Ford | 1 | farmland | grass | 1 | known; the way across the river |
| Broadwater | 2 | rich vale | grass, fish, mill site | 4 | the best land; a rumour line to Ashby's head |
| Hollins | 2 | farmland | grass, wood | 3 | |
| Greenhythe | 2 | fen | fish, grass | 1 | eels and withies; wet |
| Hartwood | 2 | old forest | wood, game | 1 | wolves and boar; the legendary boar |
| Thornheath | 2 | heath | grass | 1 | poor |
| Longmere | 3 | lake | fish, grass | 2 | a lake stock that can be fished down |
| Stonebarrow | 3 | rock hills | quarry, grass | 1 | stone |
| Upper Hollins | 3 | farmland | grass | 3 | |
| Kingsmead | 3 | rich vale | grass, fish | 3 | |
| Ashen Down | 3 | chalk down | grass | 2 | sheep country without sheep: pasture for cattle |
| Wolfcombe | 4 | forest | wood, game | 1 | the wolves' ground |
| Far Meadows | 4 | rich vale | grass, fish | 4 | |
| Highbarrow | 4 | moor | grass | 1 | |
| Eastmarch | 4 | farmland | grass, wood | 3 | |

**Capacity (to check with the ladder).**
- Home at "standing" feeds about 15, and "worked" (manure, rotation, the plough) about 25.
- The whole map at "worked" holds about 130, about 10 times the founders.

**Growth needs:** good farming; hay and stores for winter; clearing (wood must be felled first, D4-60); founding households (`found`,
then `claim` or build); carrying seed and food to a new place. In c2_combe, a family that resettled starved for want of carried food.

**Readings:** the population curve; the day of the first household founded; places held by day; the share of acts on food; whether
the best land (Broadwater, the rumour) is found and taken.

**Gaps:** none beyond the shared prerequisites (§7). This is the world that tests the 200-day machinery first.

## 3. World 2: Eelmouth Reach (fishing start; the wave's systems)

**Idea.** The rebuilt Eelmouth people, a water-only village at the mouth of a big river (D2-316), made into a long run in a large
land. The runs give a glut each autumn, and fish feed them if they keep the catch through winter. But the fishery has a ceiling (the
weir's nightly cap, D2-210; the stocks, D2-229), and the land upriver is unexplored. Growth past the fishery's ceiling means learning to
farm, which one founder knows from her childhood, and finding cattle.

**Land.**
- Estuary and fens (calibration w09) with a big river carrying eel, salmon and lamprey runs.
- Saltmarsh with a brine spring at home. Little arable at the mouth.
- Packs: water (shallows, runs, the weir), wild, farming (on, but no fields held at the start).

**Founders: 12 in 3 households.**

| Household | People | Livelihood | Capital | Note |
|---|---|---|---|---|
| Marsh | head 48 (m), wife 38, son 19 (youth), daughter 8 | fisher (weir and nets; keeping) | the weir (wattle), gill net, smokehouse, smoke racks | |
| Brook | head 44 (f), husband 46, daughter 21 (youth), son 14 (youth) | salter; fisher (hand, rod) | salt house, brine pan, salting tub | the wife was born inland: farmer at **broad** level, with 2 lines (FA1, FA2) and a rumour line upriver |
| Shepherd | head 34 (m), wife 30, son 5 | fisher (traps and runs); basket maker | wicker traps, withy bed | the name is old; they keep no sheep |

- Seed: a small sack of grain and beans in the Brook store (enough for one plot), kept "against the day".
- No cattle at home.
- **A feral herd** stands at Barrow Down (3 days, unexplored): cows and a bull, no holder, claimable (`claim` on a herd, built).

**Map: 20 places, 3 known.**

| Place | Days from home | Land | Resources | Room | Note |
|---|---|---|---|---|---|
| **Eelmouth** (home) | 0 | coast | salt (brine spring), fish (runs, shallows) | 3 | known; the weir's reach |
| The Saltings | 1 | coast | salt, fish | 1 | known |
| Withy Holt | 1 | fen | fish, grass | 1 | known; willow |
| Kingsford | 2 | farmland | grass, fish | 3 | the first good field land; the Brook wife's rumour |
| Reedmere | 2 | fen | fish, grass | 1 | fowl and eels |
| Middlemere | 2 | lake | fish, grass | 2 | a second fishery, its own stock (one stock per water body) |
| Oakhanger | 2 | forest | wood, game | 1 | timber for the weir's sections |
| Upper Reach | 3 | rich vale | grass, fish, mill site | 4 | the best farm land, on the river; runs pass it |
| Barrow Down | 3 | chalk down | grass | 2 | the feral herd |
| Ashcombe | 3 | forest | wood, game | 1 | |
| Greyhythe | 3 | coast | fish, salt | 1 | a second salt shore along the coast |
| Long Acre | 3 | farmland | grass | 3 | |
| Fernhill | 4 | heath | grass | 1 | |
| Highreach | 4 | rich vale | grass, fish | 3 | the salmon's spawning reach |
| Coldstone | 4 | rock hills | quarry, seam | 1 | copper; nobody knows smelting |
| Mere End | 4 | lake | fish | 1 | |
| (four stops and wild nodes on the long roads) | 1 to 3 | mixed | | 0 | |

**Capacity.**
- Home's fishery at "standing" feeds about 14 in a fair run year, more in a good one.
- The fishery's ceiling (the weir full, the traps, Middlemere) is about 30.
- With farming at Kingsford and Upper Reach, and the herd, the whole map holds about 110.

**Growth needs:** setting and tending gear right; keeping the glut (smoke, salt, dry); stores through the gap between runs; then the
move upriver: learning and teaching farming from one broad-level founder, carrying seed, claiming the herd.

**What it tests that the others do not:** a seasonal, capped livelihood against a slow, expandable one; whether a knowledge held by
one person is used and taught before she dies (she turns elder about day 18); restraint on a lake stock that a growing people can fish
down.

**Gaps:**
- the action fixes (W-102), since this world uses the eleven act shapes and the household book most heavily;
- the run's calibration (the surplus band, Q-68);
- the generator's coast villages (W-54 audit: "no coast or fen villages"). Eelmouth was built by `make_eelmouth.py`, not wholly
  generated, so this world may need the same route.

## 4. World 3: Highfold (mountains, cattle and the long winter)

**Idea.** A herding people in two hamlets a day apart, one each side of a pass, high in the hills. The weather follows height, which
the engine already does, so winters here are long and hard and snow lies. Summer is short: hay made in it is what the cattle live on.
Down the valleys, three to four days off and unexplored, lies the lowland.

**Land.**
- `two valleys over a pass`, with the uplands raised as in calibration w06 (tops about 1,200 to 1,500 m; the hamlets at about 400 to
  500 m).
- The pass road crosses mountain stretches, where a winter crossing risks "the cold on the pass" (`roads.py:294`).
- Packs: farming, wild (deer, wolves, bear, hare), water (becks and a tarn).

**Founders: 15 in 4 households over 2 hamlets.**

| Hamlet | Household | People | Livelihood | Capital |
|---|---|---|---|---|
| Highfold | Fell | head 50 (m), wife 42, daughter 20 (youth), son 10 | herder (stock; hay and winter) | 6 cattle (cows, a bull, 2 young), byre, hay meadow, hay in store |
| Highfold | Dale | head 38 (m), wife 32, son 17 (youth), infant | herder (dairy) and farmer | 3 cows, cellar (cheese), 1 small field (oats as grain), hens |
| Coldwell | Smith | head 54 (m), wife 40, son 22 (youth) | smith; builder (mason) | forge, copper tools, a copper seam a day off |
| Coldwell | Quarry | head 30 (f), brother 28, daughter 15 (youth) | builder; hunter | quarry, timber, snares, crude weapon |

- Married between the hamlets, so each knows the other.
- Youths across the hamlets can pair; travel over the pass is how they meet.
- Coldwell has tools and stone but little grazing. Highfold has cattle but buys its tools. A small exchange already exists (a seeded
  line on each side).

**Map: 16 places, 6 known.**

| Place | Days | Land | Resources | Room | Note |
|---|---|---|---|---|---|
| **Highfold** (home A) | 0 | upland pasture | grass | 2 | known |
| **Coldwell** (home B) | 1 over the pass | rock hills | quarry, grass | 2 | known |
| The Pass | between them | mountain | | 0 | known; dangerous in winter |
| High Shieling | 1 from Highfold | moor | grass | 1 | known; summer grazing |
| Copper Gill | 1 from Coldwell | rock hills | seam | 0 | known |
| Tarn Beck | 1 | lake | fish | 1 | known |
| Lower Fold | 2 down valley A | hills | grass, wood | 2 | |
| Birkdale | 2 down valley B | forest | wood, game | 1 | wolves, bear |
| Wolf Scar | 2 | rock hills | game | 0 | |
| Greendale | 3 down valley A | rich vale | grass, fish | 3 | the first good farm land; rumour line to Fell |
| Mill Foss | 3 down valley B | river terrace | grass, fish, mill site | 3 | |
| Oak Clough | 3 | forest | wood, game | 1 | |
| Lowdale | 4 | rich vale | grass, fish | 4 | where both valleys' rivers meet: the lowland's heart |
| Fordham | 4 | farmland | grass | 3 | |
| Mosslake | 4 | lake | fish, grass | 2 | |
| Southmoss | 4 | fen | fish | 1 | |

**Capacity.**
- The two hamlets at "standing" feed about 17, if the hay is made.
- The uplands' ceiling is low, about 30. The lowland adds about 80.

**Growth needs:** hay and stores before each winter; winter fuel; the herd bred and kept from wolves; the hamlets' exchange; then
leaving: driving cattle down a valley three or four days (herds can be led, D4-58), with the timing right (not into the first snow).

**What it tests:** planning across a long winter year after year; timing travel by season; whether a people splits or moves wholesale.

**Gaps:**
- the climate from the land (Q-56): height carries most of this world's climate, so it suffers least from the gap;
- moving herds by season is not built (L-36), but leading cattle is;
- whether snow covers cattle grazing or only the wild's forage is unknown, and must be checked before calibrating the hay need;
- the bear is too common (L-127).

## 5. World 4: Oldbury (the remnant; mixed, capital-rich, people-poor)

**Idea.** A village built for 30 holds 9. A fever years ago took the rest; no disease is simulated, so this is story only. The mill,
the smithy, the plough team and the herd remain, and so do houses with no one in them. The two who know the mill and the forge are old.
The young know the land only in broad strokes. The elders know the empty hamlets beyond the downs; the young do not. Everything the
elders know dies with them unless they pass it on.

**Land.**
- Chalk and clay (calibration w10, `scarp and vale`): dry downs for cattle, a wet clay vale with oak, springs at the scarp foot, a
  river with a mill site.
- Packs: farming, wild, water (shallows).

**Founders: 9 in 3 households, with capital for many more.**

| Household | People | Livelihood | Capital |
|---|---|---|---|
| Mill | the miller 60 (m, elder about day 4), his daughter 34, her son 16 (youth), her daughter 7 | miller (expert, the old man); farmer (broad) | the water mill, oven, 3 fields, bins |
| Forge | the smith 58 (f, elder about day 6), her nephew 23 (youth) | smith (expert, the old woman); builder | the smithy and forge, copper tools, charcoal |
| Downs | a herder 40 (m), his wife 36, their daughter 14 (youth) | herder; ploughman | 8 cattle, ox pair and plough, byre, hay barn |

- Partners: the Mill boy and the Downs girl; the Forge nephew and the Mill daughter's line later; and see Westcot below.
- **Empty capital at home:** 4 empty houses (claimable), 3 fields gone to scrub (cleared again more cheaply than wood), a second
  byre.
- **Knowledge by age:**
  - The elders carry the expert lines (the mill, the forge) and the map lines of the empty hamlets.
  - The young carry broad lines and know home and its immediate places only.
  - Teaching is built: `watch` costs a day beside them; a lesson is in the teacher's craft (D4-123).

**Map: 17 places; 4 known to all, 4 more known only to the elders.**

| Place | Days | Land | Resources | Room | Known to |
|---|---|---|---|---|---|
| **Oldbury** (home) | 0 | farmland | grass, fish, mill site | 8 (4 held, 4 empty houses) | all |
| Oldbury Down | 1 | chalk down | grass | 1 | all |
| Clay Wood | 1 | forest | wood, game | 1 | all |
| Springhead | 1 | rich vale | grass, fish | 2 | all |
| Netherby | 2 | farmland | grass | 3 | elders: an empty hamlet, two standing houses |
| Chalkpit | 2 | chalk down | quarry | 0 | elders |
| Hamwell | 3 | farmland | grass, fish | 3 | elders: empty, a ruined mill |
| Coldharbour | 3 | heath | grass | 1 | elders |
| **Westcot** | 3 | river terrace | grass, fish | 2 | **nobody**: a second remnant family of 3 (a couple and a youth son) survives here, the same people under the same model, unexplored to Oldbury and Oldbury to them |
| (8 more vacant places at 2 to 4 days) | | vale, wood, down, fen | | 1 to 3 | nobody |

**Capacity.**
- At "standing" home feeds about 12, because the fields have gone to scrub.
- Home's "worked" with the mill and plough feeds about 35, and the map about 120.
- The headroom is reached by using capital that already exists, not by building it.

**Growth needs:** children early, while the founders can still have them; the mill and forge kept working by teaching before the
elders die; claiming empty houses rather than building; finding Westcot for partners (and Westcot finding them).

**What it tests:** demographic recovery with abundant capital; the transmission of craft and of the map; the use of inherited capital.

**Gaps:**
- disease does not exist, which is fine for this world (its past is told, not simulated);
- the empty houses' state (what becomes of an emptied house is open; seed them as sound or worn);
- capital whose keeper dies: the household book and claims must carry on (life.py's succession by household rules, built).

## 6. World 5: The Scattering (the most systems; four groups unexplored to each other)

**Idea.** One people, scattered. Four families went four ways after a dark year: one to the coast, one into the great wood, one to the
moor, one to the river vale. Each knows the others went somewhere ("your sister's family went toward the sunrise, to the river
country"), not where. Each home can feed its family and little more. Each lacks what another has: salt, metal, grain, timber, cattle.
Each family is small and mostly kin, so its children have few partners but cousins. Growing past one generation means finding the
others.

**Land.**
- A region of about 140 km, following peoples W5 ("Three Countries", designed and generated once, `peoples_design.py`) with a
  fourth country added.
- A wet west coast with saltmarsh; a great wood in the centre; moor and rock hills to the north with copper; a rich river vale to
  the east.
- A ford crossroads, Threeways, sits about two days from each home and three to five from each other.
- Packs: everything built: farming, wild, water (the coast's shallows and a river run in the vale's river, smaller than Eelmouth's).

**Founders: 15 in 4 households.**

| Group | Home | People | Livelihood | Capital | Lacks |
|---|---|---|---|---|---|
| Strand | Holtmouth (coast) | head 46 (m), wife 40, son 18 (youth), daughter 15 (youth) | fisher (hand, traps); salter | salt pan, wicker traps, smoke racks | grain, metal, timber in quantity |
| Holt | Deepwood (wood) | head 38 (m), brother 34, his wife 30, girl 10 | hunter; woodsman | snares, crude weapons, a **tent only, no house** | salt, grain; must build or stay camped |
| Fell | Highcairn (moor) | head 50 (f), son 26, his wife 24, boy 13 (youth) | herder; smith | 5 cattle, byre, forge, copper seam nearby | grain (cold poor fields), salt |
| Meade | Lowbury (vale) | head 44 (m), wife 36, son 20 (youth), daughter 6 | farmer | 2 fields, seed, bins, wooden plough, no oxen | salt, metal (tools wear), cattle |

- Every home is at "standing" about 1.15 times its people.
- Partners within a group are siblings or cousins. Youths across groups (Strand's son and Meade's daughter later, Meade's son and
  Strand's daughter, Fell's boy) are each other's only unrelated partners.
- **This lever depends on a rule the engine does not have** (§8 Q-b): today siblings can partner and try. Without the rule it rests
  on the models' own norms, which may be fine but is untested.

**Map: 26 places; each group knows its home and the places within a day of it (3 to 4), and nothing of the others.**

| Country | Places | Note |
|---|---|---|
| Coast | Holtmouth (home), Saltings, Cove, Greyhaven (vacant, 2 days), a cliff stop | salt and fish; little field land |
| Wood | Deepwood (home), Oakhurst, Border Wood, Hartsmoot (vacant clearing, 2 days) | game, timber; wolves and bear |
| Moor | Highcairn (home), Coppermount, Stonefell, Highmoor, Tarn | copper, stone, grazing; cold; poor fields |
| Vale | Lowbury (home), Millbrook (mill site), Wheatley, Southmere (fen), Longacre | rich soil, mill sites, fish; no stone, little wood |
| Between | Threeways (the ford, rich vale, room 4), Marchmead, Midwold, two stops | the meeting ground; the best vacant land in the middle |

- Roads run as peoples W5: each home is 2 days from Threeways and 4 from each other home by the roads.
- Every way out of a home's country is unexplored but walkable.

**Capacity.**
- Each home at "standing" feeds its 3 to 4.
- Home "worked" without trade feeds about 6 to 8 each. With salt (keeping), metal (tools) and grain moving between them, about
  twice that.
- The whole region's ceiling is about 150.

**Growth needs:** exploring out of one's own country; recognising kin when met (seeded kin lines name the others' heads); exchanges
(salt and fish, copper tools, grain, timber, cattle); marriages between groups; settling the middle land.

**What it tests:** exploration under uncertainty; first contact and what follows; a whole dependence web (scenario_design §1) built by
one model with itself; whether four small groups become one people or stay four.

**Readings:** the day of each first contact (6 pairs); goods moved between groups; marriages across groups; places held; the curve by
group and in all.

**Gaps:**
- **G5, a sign that carries between places** (smoke on the horizon). Without it first contact comes only by searching or by luck on
  the road, which may be the right test, but should be chosen (monoculture_worlds.md Q-91);
- the kin rule (Q-b);
- the generator at 140 km (§1 Size);
- coast villages in the generator (W-54);
- peoples W5 was "generated once, to finish".

## 7. Prerequisites (all five)

1. **The action fixes from live run 1** (W-102): 213 refusals in the rebuilt arm. A 200-day run would spend its first days on them.
2. **Live run 1's reading** (W-101): whether the new prompt and the household book work at all before they carry 200 days.
3. **The fixes for the next peoples run** that these worlds still need (Q-43): stores to the first harvest (set per world here);
   founders' ages (set here); the aim passed to youths (§8 Q-a).
4. **Long-run operations:** checkpoints copied out as the run goes (L-147); resume after each stop (`resume --from-last`); a
   population-curve tool (monoculture_worlds.md G4).

## 8. Cost

At lifespan 64 the acting people (youths, adults and elders) are about 70% of the living.

| World | Founders | Acting people averaged over 200 days if they grow well | Agent-days | Haiku | Sonnet | Opus |
|---|---|---|---|---|---|---|
| 1 Fallowmere | 13 | 25 to 35 | 5,000 to 7,000 | $15 to $20 | $200 to $280 | $350 to $750 |
| 2 Eelmouth Reach | 12 | 20 to 30 | 4,000 to 6,000 | $12 to $18 | $160 to $240 | $280 to $650 |
| 3 Highfold | 15 | 20 to 30 | 4,000 to 6,000 | $12 to $18 | $160 to $240 | $280 to $650 |
| 4 Oldbury | 9 (+3) | 15 to 25 | 3,000 to 5,000 | $9 to $15 | $120 to $200 | $210 to $540 |
| 5 The Scattering | 15 | 20 to 35 | 4,000 to 7,000 | $12 to $20 | $160 to $280 | $280 to $750 |

- Rates are $0.003, $0.04 and $0.07 to $0.11 an agent-day (65_goal_probe_3_design, 02zzc).
- A society that collapses costs little; one that grows to 100 costs far more than the table.
- Wall time is about 6 minutes a day at 20 people, so 20 to 40 hours a run.

## 9. Questions for Zach

- **Q-a (Q-93): the aim for those born in the run.** D5-1 gives the line to founders; children get it only if someone passes it (70 of 134
  lines passed in the runs world were the goal, founders_knowledge.md).
  - *Recommend:* give it to each youth at coming of age as well, so the score measures growth, not whether the aim was handed on.
  - *Default:* founders only, as the runs world did.
- **Q-b (Q-94): a kin rule.** No partnering or trying between parent and child or siblings. It is not in the engine, and World 5 rests on it.
  - *Recommend:* yes, a small rule.
  - *Default:* none (the models' own norms).
- **Q-c (Q-95): which first.**
  - *Recommend:* World 1 first, to prove the 200-day machinery; then World 5 (the most distinct test) or World 2 (the wave's own
    systems).
  - *Default:* World 1.

## Alternatives considered

- **The grid of monoculture_worlds.md §5** (one land, four starts; one start, eight lands): it reads one axis at a time. Zach asked
  for worlds that each vary several axes, at several levels of complexity. The grid is kept open (Q-89) for when a pairwise
  comparison is wanted.
- **Generated worlds without hand-designed maps:** the generator would choose the vacant places, but would not make the specific
  levers each world tests (the rumour, the feral herd, the empty hamlets, the four countries).

## History

- 23 Nov 2026 (later): Zach asked that the first world be small, with two connected villages, fishing and farming, to test the
  dependencies (Q-95 answered). World 0, Highpool and Middleham, added in §1a, on the runs world's land.
- 23 Nov 2026: written by session bench at Zach's request; five worlds, after D5-1 (the graded line).

## Sources

proposals/monoculture_worlds.md; proposals/peoples_benchmark.md and cybertron2/specs/peoples_design.py (the map form, W5);
cybertron2/specs/make_runs_models.py (the goal, the cast); cybertron2/engine/livelihoods.py (the rows); landgen/settle.py (vacant
places), landgen/write.py:356 (unexplored wild nodes); docs/review/38_space_engine/70_peoples_run1.md, 75_lake_run2_and_goal.md;
runs/water_runs_models_r1 (days 0 to 29); spec/life/birth_and_death.md.
