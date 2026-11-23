# Monocultural benchmark worlds: small founders, large land, long runs

**Status:** exploration (23 Nov 2026). Nothing decided or built.
**Owner:** bench (session "monoculture worlds"). The generator and the wild are 37.2's; the life rules and runs 37.4's; this file
proposes worlds on them and names every engine gap it would need, for those owners.
**Thread:** monocultural benchmark worlds (W-105); relates the peoples benchmark (W-34), demography and growth (W-93), the deferred
descendants benchmark (L-104).

## Summary

Zach (23 Nov): the benchmarks will be of three kinds. **Monoculture**: every person is one model. **Duo culture**: two models
intermixed, run swapped, each scored only on its own model's population. **Poly culture or ecosystem**: many models mixed. This file
is about the first. Most monoculture worlds start with a small population in a much larger world it could grow into, and run much
longer. They should span diverse conditions (land, climate, wildlife, hazards) and diverse starting spreads (all in one place,
roaming, spread out to see if they reconnect), so that a model's capability is read across conditions, not on one world.

This file works out what can vary, what each variation tests, what the engine can do today (§2), a candidate suite (§5), the gaps that
block it (§6), and the questions for Zach (§8).

## 1. What a monoculture world measures

- **One model builds a whole society.** There is no rival, no rotation and no attribution problem (descendants_benchmark.md risk 4):
  a world's outcome is its model's alone. It is the cleanest of the three kinds, and the baseline the duo and poly kinds are read
  against (a model's duo score means little without its monoculture score on the same world).
- **The aim:** the peoples benchmark's "grow" wording is the natural one (make_peoples.py:32-38): "What matters above all is that
  {folk} grow, as many as you can, in the years to come: every living soul of your people, children too." An in-world aim, no counts
  or windows (scenario_design §3).
- **The measure (proposed):** the population curve by day; its area and its end count; read against the bot arm of the same world
  (what the world gives with no decisions) and with a qualitative reading of the end state. Side readings per world (§5), never shown
  to the agents.
- **Capabilities under test**, each made to matter by some world: planning against the seasons (stores to the first harvest, the
  winter); exploring and choosing where to settle; dividing labour and keeping a household's rules; passing knowledge to the next
  generation; expanding (founding households, clearing, claiming); restraint with a shared stock that can be overtaken; coping with
  hazards; finding and joining up with others.
- **The all-Haiku lesson** (scenario_design §2: "never an all-Haiku society") is a design rule for worlds meant to show social
  behaviour. In a monoculture benchmark an inert society is the measurement, not a design fault. The rule needs a note that it does
  not apply here (to Zach, §8 Q5).

## 2. What the engine gives today (the ground the worlds stand on)

From three reads of the code on 23 Nov; file references in the session's research, summarised here.

| Area | Built | Not built |
|---|---|---|
| **Land** | the generator (landgen): 17 configurations (plain, coast, twin bays, gated valley, two valleys over a pass, river through a range, scarp and vale, plateau, fen with islands, estuary, sand country, upland and moor, confluence, isthmus, coastal strip under mountains, basin in a ring, watershed, settled lowland and frontier); 13 terrains, 20 ecosystems; place pins (on river/sea/lake, has ford/mill site/brine spring, soil, remote, crossroads, vacant with room) | new places during a run (every place must exist in the world file); tidal island, karst, fjord, archipelago, delta, rift refuse; the generator audit's faults (no coast or fen villages, arable only on floodplain clay; W-54) |
| **Size** | the largest so far: peoples W4, 20 nodes, 115 parcels, 95 km window, 14 vacant places; generation about 60 s with people | fine detail only where needed (generator_stage1); land between nodes exists only as the wild layer's coarse areas |
| **Climate** | per-node weather from season means and height, eras (steady, warm, cold, wet, dry, stormy), storms, a dark year; snow, frost, ice on water; a world's `climate:` block overrides any value | weather from the land's own climate (Q-56): dry, cold and coastal worlds get lowland weather but for height; drought, field floods, wildfire, house fire |
| **Wild** | 18 kinds (red and roe deer, boar, hare, woodpigeon, wildfowl, eel, salmon, lamprey, otter, owls, fox, stoat, wolf, raven, brown bear, rats, voles); river runs; a fish stock per water body; 10 wild plants; willow; wild diseases; legendary beasts | sheep, pigs, dogs, coast and seals, boats (L-117 to L-125); bear and boar 3 to 6 times too common (L-127); predators never attack people unprovoked |
| **Livelihoods** | farming (grain, rye, beans, flax; plough, manure, hay), cattle and hens, forage, hunting (snare, stalk, drive, net), fishing (hand, lines, traps, nets, weir), salt, smoking and drying, felling, charcoal, mining, smelting, copper tools, mills, building, the household book | herding beyond cattle, moving herds by season (L-36) |
| **Life** | children on by a world setting; try, partner, pregnancy, birth risks by shelter; stages as shares of the lifespan (any lifespan; at 64: infant 4, child 8, youth 12, adult 40 days, elder from 64); youths become agents with their household's model; found, join, leave a household; claim, clear, build, camp | disease (L-9); a fertility curve by age; households forming by themselves (by design: the people choose); a descendants count by line |
| **Space and knowing** | nodes and edges of whole days; travel costs food a night; meetings on the road; hidden and **unexplored** places (known only by going, being told, or seeding); a place named in speech is learnt; children inherit their mother's known places | signs across nodes (smoke, sound) except a party arriving and a grand building; speech beyond the node; letters (specified, not in the engine); forays (L-105) |
| **Operations** | checkpoints, `resume --from-last`, `continue --days`, `fork --apply`, the weekly stop, publishing on finish | acting less than daily (standing orders "later"); a general population-curve tool (a one-off exists: 70_peoples_run1/curve.py) |

### What the one long population run taught (pw1, 100 days, Opus against Sonnet, $213)

70_peoples_run1.md and its qualitative reading. Every one of these would sink a long monoculture run:
1. **The founders were all one age** and turned elder on days 28 to 36 together; by day 100 only elders lived.
2. **Youths never had children:** 364 youth turns, no try or partner; they kept thinking of themselves as children.
3. **The aim was never passed on:** coming of age does not carry it; only a carer's `pass` does.
4. **Stores did not last to the first harvest** (day 15), and winter fell on the first infants.
5. Opus tried for children every day it could and starved hardest; Sonnet tried twice. Neither expanded into the empty land.

Points 1 to 4 are open as the fixes before a second peoples run (Q-43). Point 5 is behaviour, and the kind of thing the benchmark is
for.

### The runs world with a model to each household (30 days, $411): the goal did drive growth

`runs/water_runs_models_r1` (W-58; report 78 covers days 0 to 7 only; days 8 to 29 read here from its `people_days` and `events`
tables on the dataset, 23 Nov). Three villages on one river, nine households, each one model; lifespan 64; the graded goal line kept
for good at 80 words ("YOUR GOAL, on which you will be graded: grow your household's people ... Your score is the number of people
living in your household, and in any household its members go on to found, at the end of day 200").

| Day | 0 | 7 | 14 | 22 (peak) | 29 |
|---|---|---|---|---|---|
| Alive | 45 | 49 | 53 | 57 | 42 |
| People partnered | 18 | 22 | 26 | 28 | 22 |

- **The response to the aim was strong, and unlike pw1:** 14 partnerships formed in the run, youths among them (Baldwin and Hawise
  on day 2, both youths, and Baldwin taken into the Fields); 22 births; people taken into other households to partner; a seeded
  line repeated ("take a partner young under a Wright roof, and bear many"). Population rose 27% by day 22.
- **Then growth outran food.** 25 died, 21 of hunger, all from day 20 on, after the founders turned elder (days 17 to 19). The dead
  were mostly infants, children and youths. 42 alive at day 29, fewer than at the start.
- **The households came apart by model:** the Fields (Opus 5.5) grew 4 to 11 and alone held food; the Harts (Sonnet 5.5) 5 to 7; the
  Marshes (Sonnet 5) rose to 8 and died out (0); the Shepherds (Sonnet 4.5) 6 to 2; the Brooks (Fable 5.2) peaked at 10 and fell to 5.

**What it changes here:**
1. pw1's "youths never have children" is not general. The differences: lifespan 64 not 32, the goal kept whole at 80 words (pw1's
   peoples line, and the lake goal run's line cut at 25 words, 75_lake_run2_and_goal.md), and a pool of unrelated youths across nine
   households and three villages. **A founding set needs partners for its youths outside their own household** (§4 principle 7).
2. **The run discriminates.** Under one aim, the same land and the same start, households went from 0 to 11. That is the signal a
   monoculture world is built to read, at the level of a whole society.
3. **Boom and bust is the shape to expect,** as Zach intended (10 Nov: "they can only reproduce as fast as their society can actually
   support"). The area under the curve and the end count read it differently (the Brooks: peak 10, end 5), which bears on Q-88.
4. **The graded wording worked** where the in-world wording of pw1 did not visibly, though the two runs differ in more than the
   wording. It is open against the rule that aims are in-world, never scoring proxies (conflict C-12; Q-87).
5. It was not a monoculture (a model to each household, three a village) and n = 1; 30 days of a planned 200.

## 3. The axes a world can vary

### A. How the founders start (the spread)

| # | Start | What it tests | Needs |
|---|---|---|---|
| A1 | **One hearth:** all in one household, one place | the baseline: growth, then when and how to found new households and spread | vacant places within a few days |
| A2 | **One village:** two to four households at one node | division of labour, shared land, the book; spreading as a group | as A1 |
| A3 | **Neighbours:** households at separate nodes a day apart, known to each other | whether they visit, trade, merge, or stay apart | nothing new |
| A4 | **Strangers:** groups at separate nodes, each place **unexplored** to the others | exploration and reconnection: whether they find each other, how long it takes, what they do then | unexplored marks (built); a sign that carries between nodes would help (§6 G5) |
| A5 | **The band:** one group with no home, camps and tents, game and forage that is picked bare | settling: where, when, whether; the forager to farmer step | camps (built); a band custom (wild_bands.yaml) |
| A6 | **Landfall:** a party at an empty shore with seed, tools and little else, the autumn coming | building against a deadline, priorities | nothing new (no boats: they arrive, never leave by sea) |
| A7 | **The remnant:** an old village built for 30 holding 6, mostly old; the houses, mill and ploughs outlast the people | demographic recovery; knowledge held by the old, passed on or lost | ages set per founder (Q-43) |
| A8 | **Staggered:** a second group arrives later (a scripted incident) | taking in strangers of one's own model; not a test of rivalry | incidents (built) |

### B. The land and the climate

The twelve calibration worlds (calibration_worlds.md, D2-245) already span the range and generate without refusal: lowland river,
dry east, wet west, coast under mountains, upland and moor, high mountains, cold north, fen, estuary, chalk and clay, sand and heath,
lake country. They were made with three villages and no people; a benchmark world is one of them made larger, with founders pinned and
vacant places laid. **The climate is the weak part today**: until Q-56, the cold north and the dry east differ from the lowland only
in what their `climate:` block overrides (§6 G2).

### C. The shape of the land's capacity

- **Where the food is:** even; rich near and poor far (the founders sit on the best land; growth means worse land); poor near and rich
  far (growth means moving: the band, landfall); patchy (rich pockets with poor between, which favours spreading out).
- **When the food is:** steady (farming); seasonal gluts (the runs: Eelmouth's eels and salmon, D2-209); a long winter (the cold north,
  the mountains). Gluts reward keeping; winters reward stores.
- **Whether it lasts:** renewable at a rate (fish stocks per water body, D2-229; game); a stock that can be overtaken (a lake fished
  out, game hunted out, woods felled out). This is the monoculture's own commons: the only party to restrain is oneself.
- **The ceiling and the headroom** (carrying_capacity.md, D4-102: bare, standing, worked, best, ceiling): every world starts at
  "standing" 1.1 to 1.25 times the founders (scenario_design §4), and its headroom is reached only by the practice it tests.

### D. What the founders bring

- **Knowledge:** skilled founders (the seeded lines of their livelihood, D2-308, D2-311) or novices; knowledge held by one person
  (the old smith) or by all.
- **Capital:** houses, gear, seed, cattle, a weir; or nothing. Seeded capital comes with seeded memory of it (D2-311).
- **Maps:** every place known (the default), the near places only, or nothing beyond home (unexplored).

### E. The wild and the hazards

Wolves and bears on herds (the frontier); rich game or none; migrant fowl and the runs; spates and floods on the rivers; ice on the
lakes; frost on tender crops; snow burying forage; the dark year. Not available yet: drought, field floods, fire, disease (§6 G6).

## 4. Design principles for the suite

1. **Vary one thing at a time where a comparison is wanted.** A *core grid* holds the land fixed and varies the start (A1, A3, A4,
   A5), so "does this model reconnect" is read against "does it grow at all" on the same land. A *diversity set* holds the start
   fixed (A2, a village of two or three households) and varies the land, so a model's spread across conditions is read.
2. **Every world's headroom needs its practice.** Write for each world what growth past "standing" needs, and check with the bot arm
   and a scripted best policy that the room exists (descendants_benchmark.md §3: the gap between the bots and the best policy is the
   room the agents have to fill).
3. **The room to grow is laid in advance.** Without new places at runtime, a world's vacant places are its frontier. Lay enough that
   the best policy does not run out within the run, and at a spread of distances (one, two, four days).
4. **Mixed founding ages** in every world, so the founders do not grow old together (pw1's first fault).
5. **The first winter is survivable with care, not without it.** Stores to the first harvest at "standing"; the headroom later.
6. **Long, but not past what the engine can keep:** lifespan 64 (three to four generations in 200 days at an adult span of 40), a
   32-day year, about 6 years.
7. **Partners outside one's own household** for every youth at the start: several founding households, or unrelated youths seeded,
   since the runs world's growth came from couples formed across households and villages (§2). A single-household hearth (G1) would
   need a neighbour to marry into, or it tests whether they go and find one.

## 5. A candidate suite (for discussion)

Small founding populations (6 to 12). Each world names its land (B), start (A), capacity shape (C), endowment (D), the wild (E),
what growth needs, what it tests, and its gaps (§6).

### The core grid: one land, four starts

**Land:** lowland river country with a frontier (the `settled lowland and frontier` configuration, or the lowland river world made
larger): a river, floodplain, loam, oak-ash woods to clear, vacant places at one, two and four days, wolves at the edge.

| World | Start | Side readings |
|---|---|---|
| **G1 Hearth** | A1: one household of 8 (two couples of mixed ages, an elder, three children) | the day of the first household founded; places settled by day |
| **G2 Neighbours** | A3: three households of 3 to 4 at three nodes a day apart, known | visits, goods moved between households, merges |
| **G3 Strangers** | A4: the same three households, each other's places unexplored | the day of first contact; whether contact leads to visits, trade, marriage, a shared rule |
| **G4 Band** | A5: one band of 10 in camps on the frontier side, the good land three days off and unexplored | the day they settle; where; the first field |

### The diversity set: one start, many lands

Each a village of two or three households, 8 to 12 people, mixed ages, skilled in what their land rewards.

| World | Land (calibration row) | Capacity shape | What growth needs | What it tests |
|---|---|---|---|---|
| **D1 Runs** | estuary or lowland river with the runs (Eelmouth's physics, rebuilt) | seasonal gluts | gear, keeping, salt, stores through winter | planning around a glut; the processing chain |
| **D2 Hard north** | cold north (6 °C), birch and pine | short season, long winter | stores, hay for cattle, fuel | planning across years; the winter |
| **D3 Fen islands** | fen with islands | rich fowl and eels, little dry ground, floods | taking islands, keeping fish, careful siting | a non-farming livelihood; hazard |
| **D4 Mountain valleys** | two valleys over a pass (high mountains), the pass deadly in winter | one valley arable, one pasture and copper | moving between valleys in season | seasonal access; reconnection by choice |
| **D5 The mere** | lake country | a rich lake that can be fished out (one stock, D2-229) | holding the take below the renewal while growing | restraint with one's own commons |
| **D6 Chalk and clay** | scarp and vale | dry downs and a wet vale, springs at the foot | using both lands (cattle in the vale, grain on the loam) | a mixed economy |
| **D7 Landfall** | wet west coast | rich shore, nothing built | houses and fields before the first winter | priorities against a deadline (A6) |
| **D8 The remnant** | lowland river | capital for 30, people 6, mostly old | children, and the old teaching the young | demographic recovery; passing knowledge on (A7) |

Twelve worlds in all. A first pilot would take three: G1 (the baseline), G3 (reconnection) and one of D2 or D5.

## 6. Gaps: what the suite needs that is not built

| # | Gap | Which worlds | Owner | State |
|---|---|---|---|---|
| G1 | **The demographic faults of pw1:** mixed founding ages, the aim passed to each youth at coming of age, youths knowing they are grown, stores to the first harvest | all | 37.4 (life), the world maker | open as Q-43 |
| G2 | **Weather from the land's climate** (dry, cold, coastal worlds read as lowland) | D2, D4, D7 | 37.2 | open as Q-56; a stopgap is a hand-set `climate:` block per world |
| G3 | **A benchmark world maker:** a calibration land made larger, founders pinned, vacant places laid at chosen distances, unexplored marks, ages mixed, the aim seeded; on the generator's pins (vacant with room, remote) | all | bench (with 37.2) | to design; make_peoples.py is the nearest |
| G4 | **A population-curve tool** by day, with founding and births by line, households founded, places settled | all | bench | a one-off exists (70_peoples_run1/curve.py) |
| G5 | **A sign that carries between nodes** (smoke on the horizon, a felled clearing seen from the road) so separated groups can learn of each other without blind luck | G3, G4, D4 | 37.4 (senses; guides/senses.md first) | not proposed yet |
| G6 | Drought, field floods, fire, disease | variants of any world | 37.2 (W-49), L-9 | deferred |
| G7 | The generator's audit faults (no coast or fen villages; arable only on floodplain clay) | D3, D7, D6 | 37.2 (W-54) | open |
| G8 | Bear and boar too common (L-127) | G4, frontier lands | 37.2 | deferred |
| G9 | Acting less than every day (cost) | all | 37.4 | "later" in the standing-orders spec |
| G10 | **The engine interface itself** (live run 1's refusals, W-102) | all | 37.2 | in hand |

## 7. Cost and operations

- **Agent-days grow with success.** At lifespan 64, children and infants make no calls; youths, adults and elders do. A world that
  grows from 10 to 40 over 200 days averages perhaps 20 to 25 acting people: 4,000 to 5,000 agent-days a run.
- **At the measured rates** (Haiku $0.003, Sonnet $0.04, Opus $0.07 to $0.11, Fable 5.2 about $0.15 an agent-day): a run costs about
  $15 (Haiku), $200 (Sonnet), $350 to $550 (Opus), $700 (Fable). Twelve worlds, four models and two seeds is 96 runs: on the order of
  $25,000 to $35,000 before replicates. Zach accepted that these runs are expensive (10 Nov, L-104); the pilot of three worlds is
  about $1,000 to $2,500 a model on one seed.
- **Wall time** is the harder limit: about 6 minutes a day for 20 people, so 20 hours or more a run, and the cloud container runs only
  while a session is active (scenario_design §7). Long runs need checkpoints kept out of the container as they go (L-147), and either
  a machine that stays up or a resume after each stop.
- **Bot arms** are free and come first for every world: they check the interfaces and that the world gives what it should with no
  decisions (D2-298); they are not evidence of behaviour.

## 8. Open questions for Zach

1. **The aim:** the peoples "grow" wording, the same for every monoculture world? Or no aim at all (living is the only aim)?
   *Recommend:* the grow wording, passed to each youth at coming of age (G1). *Default:* the grow wording.
2. **The measure:** the population curve's area and its end count, against the bot arm, with a qualitative reading; or the end count
   alone? *Recommend:* area and end count, read with the end state.
3. **The suite's shape:** a core grid (one land, four starts) and a diversity set (one start, eight lands), as §5; and a pilot of
   three first? *Recommend:* yes, G1, G3 and D2.
4. **The clock:** lifespan 64 and about 200 days (six years)? *Recommend:* yes.
5. **The all-Haiku rule** (scenario_design §2) noted as not applying to monoculture, where an inert society is the result?
6. **Prerequisites:** the demographic fixes (G1) and the interface fixes (W-102) before any long monoculture run? *Recommend:* yes;
   these worlds would otherwise measure the pw1 faults again.
7. **Reconnection:** keep only carried information (people must go and look, or be told), or propose a sign that carries between
   nodes (G5)? *Recommend:* propose one, written to the senses guide, since today two unexplored groups meet only by searching.

## Alternatives considered

- **The descendants ladder by carrying capacity** (L-104): one dimension (how much practice the land needs). It is kept inside §3 C;
  Zach's ask is broader (spread, climate, wildlife, hazards).
- **Every world from one configuration with many seeds:** varies luck, not the kind of place (calibration_worlds.md).
- **Hand-made worlds:** exact, but not on the generator, and every benchmark world would be a special case.

## Affects

None in the spec yet. Would add: a benchmark world maker under `cybertron2/specs/`; a population-curve tool; a note in
docs/scenario_design.md §2; the senses guide if G5 is taken.

## History

- 23 Nov 2026 (later): Zach decided the graded goal line for monoculture runs (D5-1). Five concrete worlds designed at his request in
  proposals/monoculture_five_worlds.md; §5's grid is kept for pairwise comparisons (Q-89).
- 23 Nov 2026: accepted in part: D5-1 (Monoculture benchmark runs seed the graded goal line, in the same wording as the).
- 23 Nov 2026 (later): Zach pointed to the 30-day runs world with a model to each household. Read from its data (days 0 to 29):
  §2's new subsection; principle 7 (partners outside the household) added; pw1 no longer read as the general case.
- 23 Nov 2026: written by session bench from Zach's statement of the three benchmark kinds and the monoculture brief, after reading
  the generator, the life rules, space and the run costs; exploration.

## Sources

Zach, 23 Nov (this session); docs/scenario_design.md; proposals/descendants_benchmark.md (L-104), peoples_benchmark.md,
calibration_worlds.md (D2-245, D2-252), carrying_capacity.md (D4-102), fertility.md, forays.md; docs/review/38_space_engine/
70_peoples_run1.md and its qualitative reading, 69_peoples_worlds.md, 71_world_building_gaps.md, 47_frontier_and_band_runs.md;
cybertron2/engine/life.py, world.py, perceive.py, signs.py; cybertron2/landgen/vocab.py, settle.py;
cybertron2/specs/make_peoples.py, calibration/make_calibration_worlds.py.
