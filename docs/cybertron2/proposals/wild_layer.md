# Proposal: the wild layer, one general system for ecosystems and wildlife, built from the generated land into the engine

**Status:** accepted to build on the `ecology` branch: D2-199 (9 Nov); open questions 2 to 7 still open. Nothing on main. **Owner:** 37.2 (the layer's design, the generator
side, the kinds' data); the engine changes are 37.4's (CLAUDE.md), so §8 names who would build what.

**Affects:**
- the generator (`cybertron2/landgen`): a land summary written with each world (§3.1), starting populations and history (§3.9);
- engine data: RESOURCES rows with population fields, TECHNIQUES, ITEMS, sign rows, packs (D4-104);
- the engine: a population store and an ecology step, beasts generalised from herds, traces, readings by skill, acts (§4);
- spec/environment/wildlife.md, resources.md; spec/economy/livestock.md; spec/information/signs.md;
- proposals: living_populations.md (the base of this), wild_systems.md, node_ecology.md, wildlife.md, husbandry.md, wild_plants.md.

**Builds on, and reconciles:**
- **living_populations.md** (8 Nov, reviewed by 37.4):
  - kinds as optional fields on RESOURCES rows (one registry, one guard test);
  - one night step (grow, eat, move);
  - observation as the collapse;
  - whole-counted groups with an actual place each night;
- **02zp part two:** the food web's rules (W2, §11 there);
- **node_ecology.md and 02zp parts three and four:** the village's scale, losses as the lever, the area graph;
- **wild_systems.md:** drivers, layered kinds, signs read by skill, lore as tested belief, creature memory, D2-197, D2-198, the waves
  (§13).

## Summary

Zach, 9 Nov:
- "You were supposed to design general systems. Go through each of the waves, considering the different ecosystem mechanisms, and
  how to build the general system to support them that bridges that with the actual engine itself."
- "Everything should build up from the environment that is generated."

**What went wrong in wave 1 (02zp part six).**
- I built per-kind machines and called them rules: a boar-shaped "group", an eel-shaped "run", a fowl-shaped "flock".
- I built them in a parallel village beside the engine.
- I made a separate kinds table, which 37.4's review of living_populations.md had already ruled out.
- I dropped the coarse ecosystem: a number per village took the place of the food web, so kinds never ate each other.
- The tests mostly measured my own scripted readings, on real species the models already knew.

**This proposal starts from the mechanisms instead.**
1. It lists what every wave needs (§2).
2. It factors that into ten general systems (§3).
3. It maps each onto the engine's own places, primitives, senses and verbs (§4).
4. It builds everything up from the generated land: habitats, capacities, starting numbers and history all come from the
   generator's world, not from hand-set numbers.

**The shape in one paragraph.** The generator writes a coarse summary of its land (areas, fine near villages and coarse away, as the
interface experiments found). Each kind is a RESOURCES row whose habitat, diet, clock, movement and behaviour are read against that
land. One ecology step moves the population of every kind in every area each night, on the food web's rules (grow, eat, move); kinds
interact by eating each other and the parcels' stocks. Near people, whole-counted kinds condense into beast groups on the engine's
parcels: the same entity as the cattle, generalised. Those groups raid, remember and answer scares, and leave traces that people
read by their skill. Everything they do to the world goes through `w.apply`, so it replays exactly. The world's history is the same
step run with no people before the run starts.

## 1. The constraints it must meet

| Constraint | From |
|---|---|
| Everything builds from the generated land and climate | Zach, 9 Nov; living_populations §2a ("the animals live on the land") |
| One registry: RESOURCES rows with optional fields, one guard test; no parallel kinds table | 37.4's review of living_populations (8 Nov) |
| Every change through `w.apply` and the journal; replays exact; a pack off leaves old worlds unchanged | core/architecture.md; D4-104 |
| Whole-counted groups hold one actual place a night | 37.4's review (two people must not meet the same pack in two places) |
| The village's scale decides what matters: losses and threats, not wild food | node_ecology.md; 02zp parts three and five |
| A coarse ecosystem for odds and emergence, discrete groups near people ("between rain world and a full proper ecosystem") | Zach, 8 Nov |
| Mechanics before realistic dynamics, but real tempo and real interactions | Zach, 8 Nov; W2 |
| Leads and memory in engine days (D2-197); answers to scares by kind (D2-198) | decided |
| Signs for every hidden thing, read by skill, with an act that pays for each leading sign | wild_systems.md §2; guides/senses.md |
| Domestic beasts are special cases of the wild system | Zach, earlier; husbandry.md ("husbandry generalises herds.py") |
| Runs carry little of their land (G-33) | living_populations §7 |

## 2. What each wave needs: the mechanisms

| Mechanism | W1 (wood's edge, river, barn) | W2 (fold, hungry year) | W3 (weather year) | W4 (what travels) | W5 (prestige, furs, the land that changes) |
|---|---|---|---|---|---|
| **M1 habitat and capacity from the land** | boar and deer by wood, hares by open land, eels by river, fowl by fen and water | wolves by deep wood; voles by rough grass | slugs by heavy wet soil; wasps by warmth and banks; bees by old wood, heather, lime | wet ground for fluke snails | slow brooks (beaver), cliffs (falcon), wildwood (bear) |
| **M2 numbers by area, with clocks** (breeding season, condition, winter deaths, real maximum rates) | all | all | fast clocks (insects, slugs) | hosts | slow breeders (beaver, bear) |
| **M3 feeding: a diet over sources** (parcel stocks, other kinds, beasts by role, carcasses, stores), with intake and reserves | boar on mast, roots and crops; deer on browse, crops and ricks; rats on stores; birds on seed | wolves on deer, then calves and sheep; fox on voles, then hens and lambs; owls on voles; ravens on carcasses | slugs and wasps on crops and fruit; aphids on beans, ladybirds on aphids | | otters at the weir; bears at hives |
| **M4 movement** (toward the best land, with home fidelity; seasons; dispersal; an edge reservoir) | herds shift from a hunted wood; fowl come with a freeze; eels run down river chains | dispersing young wolves cross farmland | | spread between villages | |
| **M5 groups condense near people** (count kept, an actual place a night, individuals on demand) | sounder, deer herd | pack, fox pair | | | bear, legendary individuals (D2-195) |
| **M6 behaviour near people** (a drive toward targets; a lead with traces; memory; answers to scares; wariness after harm) | the learned field; habituation; the dog | the fold that fed them; the open henhouse | | | hungry bear at the hives |
| **M7 shared drivers** (weather by place; pulses; cycles; cohorts) | mast; frost runs; rising water; dark nights | the rodent phase | warmth sums, wet spells, chafer cohorts | disease load | |
| **M8 phenology** (by accumulated warmth and day length, with offsets by place) | | | calendar markers, flowering, swarming, hatching, chafer flights, ergot at flowering | | |
| **M9 outbreaks** (fast density kinds on crops, under weather) | | | slugs, aphids with ladybirds, leatherjackets, wireworm after ploughing | | |
| **M10 disease** (load by host and area; contact, carcass, wetness; between kinds and villages) | | | ergot (a plant disease) | murrain and swine fever (boar and pigs), fluke, mange | rabies |
| **M11 colonies and sites** (an all-or-nothing site; founded or abandoned on conditions; leaving for good) | | | wild bee colonies | | heronry, rookery, warren |
| **M12 engineering** (a kind changes the land) | boar rooting turf | | | | beaver dams: water, flooded meadow, fish, deadwood |
| **M13 people's acts** (takes with skill, gear, crew and danger; deterrence; restraint; keeping) | watch with a scare, dog, boar hunt, stalking, snares, traps and a crew at the weir, nets, cats, staddles, bird-scaring | fold, pen, hounds, drives and bounties (work by several) | sow later, roll the seed bed, take nests, narrow the hives | quarantine, burning carcasses | trapping, claims on swans and herons |
| **M14 traces, signs and readings by skill** | rooting, slots, trampled corn, plovers, the moon and rain | tracks, howling, ravens over a kill, owls silent | catkins, queens, slime, black spurs | sick beasts, carcasses | stumps cut to points, dams |
| **M15 beasts kept and wild as one** | boar is the pig's kin | sheep, poultry, dogs and hounds as rows | hives as held colonies | disease shared by boar and pigs | warrens, dovecotes, fishponds |
| **M16 goods and chains** | meat, fat, hide (into built goods), eels and fowl to store, feathers | pelts | honey; wax waiting for documents and light | | furs, castoreum, a trained hawk |
| **M17 history before the run** | woods cleared by settlement; the boar's last mast years | wolves gone a generation ago | | | the beaver trapped out |

**Two findings from this table:**
1. **Most of the archetypes in wild_systems.md §5 are not separate mechanisms.**
   - A run, a flock and an outbreak are numbers by area (M2) with a diet (M3) and movement with triggers (M4).
   - A cycle is mostly predators eating prey with a lag (M3); a pulse is a driver (M7).
   - Only groups near people (M5, M6), colonies (M11) and engineering (M12) need machinery of their own.

   That is why wave 1's five "rules" were wrong.
2. **The engine already has half of it under other names:** stocks with renewal rules, herds that wander and trample, fences, crops,
   spoilage, techniques, sign rows, packs (§4).

## 3. The general systems

Ten systems. Each is written once; kinds are rows on them.

### 3.1 The land summary (from the generator)
- **Areas:** the generated land cut into areas, about 300 m blocks on each village's own land, 1 km out to a ring around it, and
  5 to 8 km across the wild land between. Each area holds what its land cells say:
  - cover and ecosystem shares;
  - soil texture, wetness, held water, fertility;
  - water, and the river chain with its direction;
  - elevation and exposure;
  - the nearest node (for the climate, D4-111);
  - the parcels that are windows onto it.
- **Links** between areas carry the length of their shared edge; river areas are chained downstream.
- **The interface experiments (02zp part four) back this cut:** resolution away from villages changes nothing; what matters is a
  small ring around each village; about 60 areas for four villages run about 30× faster than a 1 km grid.
- **Written with the world,** so a run carries it (a few kilobytes). That meets G-33 for the wild layer without the full land.

### 3.2 The kinds registry (data)
RESOURCES rows with optional population fields (living_populations §2b), extended:

| Field | Holds |
|---|---|
| `count` | `density` or `whole` (groups of whole animals), with group sizes |
| `habitat` | K per km², as a function of the area's land: covers, ecosystem, soil, wetness, water, elevation, warmth |
| `body` | mass, from which intake and the maximum rates follow (Kleiber; W2) |
| `clock` | breeding season and litter, maturity, lifespan; or phenology by warmth for fast kinds (M8) |
| `diet` | sources, each a parcel stock key, a kind, a beast role, carcasses or stores, with a preference and a functional response |
| `moves` | home fidelity, speed, seasonal targets, triggers (a freeze; dark nights with rising water), dispersal |
| `near_people` | targets with seasons (crops, stores, ricks, folds, hives), drive, lead nights (D2-197), memory, answer to scares (D2-198), harm |
| `site` | for colonies: what a site needs, founding and abandonment |
| `engineers` | what it writes to the land (water level, turf, deadwood) |
| `hosts` | diseases it carries and spreads |
| `signs` | its sign rows (§3.6) |
| `taken_by` | the techniques that take it; `goods` it gives |
| `pack` | the wave's pack |

The guard test, as living_populations asked: each row's fields name only known mechanisms, and no code names a kind.

### 3.3 The population store and the ecology step (the macro layer)
- **State:** for every area and kind, a count and a condition (reserves); for every area, its drivers (the mast's budget and fall,
  cohorts, disease loads). Weather is not stored: it is read from the climate by place and day.
- **The step,** each night, for every area and kind, in a fixed order:
  1. **Clock:** breeding in its season, by condition; deaths by age, cold and hunger.
  2. **Eat:** intake by body and food. Food comes from parcel stocks (through the primitives), from prey kinds (their counts fall),
     from beasts (§3.4), carcasses and stores. A consumer short of food loses condition, then numbers.
  3. **Move:** toward the best areas with home fidelity, crowding counted; seasonal targets; triggered runs; the edge reservoir.
- **The rules are W2's** (02zp part two §11):
  - food as stock, intake by body size, coarse and fine food;
  - reserves and hibernation;
  - foraging by value;
  - crowding scaled by body size;
  - predator interference, refuges;
  - episodes for variation;
  - real maximum growth rates;
  - one calibration anchor per food.
- **Kinds set:** about 12 to 15 kinds over waves 1 to 3, not W2's 37.
- **Chains between kinds come out of it, not out of scripts:** the mast cascade, the vole cycle with predators lagging, wolves
  following deer, a hunted-out wood sending wolves to the herds.
- **A pure function of the state and the day,** so the capacity model can run it forward under a harvest (living_populations step 2a).

### 3.4 Beasts: one entity for kept and wild (the meso layer)
- **In two steps** (§4: cattle are hard-coded through farm.py, herds.py and two primitives):
  1. first, wild groups in a table of their own, using herds' movement, fence and trampling functions made to read a kind's row, so
     cattle are untouched;
  2. then, with husbandry (sheep, pigs, poultry, dogs; L-36), cattle move onto the same entity.
- **Generalise herds into beast groups:** a kind (a RESOURCES row), a count by role, a node and parcel, a home, an owner or none,
  and memory fields. Cows are rows on it, behaving exactly as today. The sounder, the deer herd, the wolf pack, later sheep, pigs,
  poultry and hounds are rows on it too.
- **Condensing:** where people are near and a whole-counted kind is in the area, a group forms from the area's count: its head is
  taken out of the count while it exists and returned when it dissolves. It holds one actual place each night.
- **Behaviour near people,** one step for every group:
  - **the drive:** a target's value comes from the kind's diet and seasons, and its hunger from the macro layer's food per head in
    the area. A mast failure in the area web is what sends the sounder out; no table says so.
  - **the lead:** groups setting out pass through the parcels between, leaving traces (D2-197).
  - **fences:** the engine's existing odds of getting through.
  - **eating and trampling:** the engine's existing primitives.
  - **watches:** resolved by the kind's answer to scares, with memory (D2-198).
  - **after harm:** wariness.
  - **individuals on demand** (D2-195).
- This is what husbandry.md says: kept is when the habitat is a held place and the food a need someone meets. Domestic and wild
  share one mechanism.

### 3.5 Traces
- Marks on parcels with a kind, what left them, an age, and facts: rooting, slots, droppings, a trampled strip, feathers, a kill.
- They age each night and fade by the weather (rain erases, snow shows all).
- They are what the senses read for animals that have passed (wild_systems §9.3).

### 3.6 Signs read by skill
- **Sign rows,** in the engine's existing format, read the population store (as density signs, like today's `game` rows), the beast
  groups, the traces and the drivers (catkins, plovers ahead of a freeze, queens at the wall).
- **One engine improvement: a reading per level** of the matching knack (novice, systematic, expert). Today the knack changes only
  the chance of noticing. A row may also carry a likely misread for the untaught.
- **Lore as tested belief** (wild_systems §9.5) comes later, on the engine's lore lines (D4-105).

### 3.7 Acts
- **Takes** are techniques: draws from the population store or from a group, with skill, gear, crew and danger outcomes (D2-193).
  They replace the one generic `game` stock and the `hunt` technique.
- **Deterrence and keeping** are acts that set what the night reads: a watch at a parcel with a scare, a fold, a pen, cats in a
  granary, scaring birds, a crew at the weir. These are like herding marking a herd as watched today.
- **Work by several** (D4-103 mechanism 1) carries hunts, drives and crews.

### 3.8 Effects on the world (the bridge out)
Every effect is one of the engine's own changes, through `w.apply`:
- crops eaten or trampled (as herds do now);
- stores lost (a pest term on a container's spoilage);
- beasts killed (a herd's head);
- carcasses left (things);
- stocks drawn (fish, grass, young growth, mast);
- land changed by engineers.

Events are raised from what happened, never scripted ("a wolf raid" is a group eating at a fold, written up as an event).

### 3.9 History before the run (from the generator)
- The same ecology step, run with no people for some decades over the world's land and era, under its settlement history (woods
  cleared by how long settled, D2-191), sets the starting counts, the groups by the villages, the traces, and the drivers' phases.
- The record of that history seeds the world's lore: what the elders say happened, true or not (wild_systems §9.5).
- A hand-made world without land gets areas from its parcels (the graph fallback, living_populations §2).

### 3.10 The climate and the fast stocks (the foundation)
- Everything reads the climate by place. Wave 1's work showed it needs calibration first:
  - long freezes in 40 to 70% of winters, against real lowland winters that have one perhaps every five to ten years;
  - era effects modest;
  - a year's totals about a tenth of a real year's.
- Spell lengths in engine days must be set against compressed time.
- The fast stocks (soil water, snow, river flow), agreed in principle with 37.4, are what slugs, eel runs and frozen ground read.

## 4. The bridge to the engine

From a survey of the engine's code (9 Nov, main). Paths are under `cybertron2/engine/` unless stated.

**What the layer reads and writes through:**

| System | Engine mechanism it uses | Where | Additive or a change |
|---|---|---|---|
| 3.1 land summary | the generator's world file; the parcel's `land` and `ecosystem` | `landgen/write.py`; `World.__init__` (world.py:113-136) | **change:** init drops `ecosystem`, `terrain`, `soil`, `depth` and any stock parameter beyond five; main's generator writes no `land` or node `xy` (those are on `climate-calibration`, 5ef36fe, unmerged); a new top-level key bumps `WORLD_SCHEMA` (schema.py; D4-100) |
| 3.2 kinds | RESOURCES rows with optional fields; packs | data.py:128-141; packs.py | additive (rows with `"pack": "wild"`); the guard test is new |
| 3.3 store and step | keyed `w.rng`; `w.apply`; the journal; renewal rules with `context` (weather, anomaly, land, D4-113) | world.py:335, 422-442; renewal.py:23-137 | additive module (`wild.py`), with a one-line call after `FM.night` (night.py:202), output in `rec["wild"]`, pack-checked |
| 3.3 eating stocks | `draw`, `set_res`, `add_res` on parcel stocks (grass, young growth, fish); the trees for mast | world.py:1038-1075; forests.py | additive; tying mast and game to the trees closes an existing gap (resources.md:48) |
| 3.3 capacity | the capacity model reads every declared stock | capacity/ | **change (37.4):** moving, coupled stocks need capacity as a regional simulation under a harvest (living_populations step 2a) |
| 3.4 groups | herds' `through`, `target`, `wander`, `trample`; claims (none for wild) | herds.py:52-217 | additive at first (a wild-groups table using those functions on kind rows); **change** later (cattle onto one entity: ROLES, `head`, split, merge, `_herds`, `PHYSICS.cattle`, `new_herd`/`split_herd`) |
| 3.4 a group from nothing | — | world.py PRIMITIVES | **change:** no primitive makes a herd or group from nothing, or removes one |
| 3.5 traces | parcel records read for N days, aged (`_aftermath`); `trace_context` (rained, snowed over) | signs.py:1749-1819, 1849 | additive (traces on parcels); road traces' `trace_days` raises on an unknown kind |
| 3.6 signs | sign rows through `spot_rows`; `knows`/`lay` pairs for readers who have and have not practised a craft; `knack`; the eye; presence | signs.py:1662, 1877, 1903; perceive.py:215-292; things.py:239-347 | mostly additive: the `knows`/`lay` pairs already give texts by skill (two levels); a third level and misreads are a small change; `LAND_DRAWS`, `presence`, `eye_practice` gain keys |
| 3.6 lore | lore lines seeded at world build | lore.py:89-103 | **change:** `text` and `fits` know only sowing and farmers |
| 3.7 takes | techniques (`chance`, `stock` yields; skill by practice; weapon; wear) | data.py:289-466; verbs.py:491-613; yields.py | additive for plain takes; **change** for a drive or crew (work by several has no general form, D4-103 mechanism 1) and for danger outcomes, with the capacity graph |
| 3.7 deterrence | a flag an act sets and the night reads (herding sets `watched`) | farm.py:786-793; herds.py:92 | additive (a watch at a parcel with a scare, a fold, a pen) |
| 3.8 crops | `draw(key="crop", holder)` plus a `set_share` mark, as herds trample | herds.py:194-217; farm.py:282-300 | additive |
| 3.8 stores | spoilage over containers | night.py:163-179, 248-277 | additive as a separate `destroy` step; a true multiplier is a change to `decay_rate` |
| 3.8 carcasses | carcass things (made only by herd deaths today) | things.py:173-191 | additive (scavengers, kills) |
| 3.8 events | `w.event(place, kind, text, ...)` | world.py:444-455 | additive |
| rare events | keyed hazards (D2-69, D2-70) | not built (scheduler.md:38-43) | waits for phase 3 |

**What exists already and is replaced or extended:**
- the `game` stock (a threshold stock in meat units, forest parcels only) and the `hunt` technique: replaced in worlds with the wild
  pack; worlds without it keep them;
- fish and eels (phase 1's water pack): extended, as density kinds on the store, not duplicated (wave 1 duplicated them);
- dogs (a building fitting read by raids and signs): kept until dogs are beasts;
- the wolves incident row (37.4's phase 3 exploration): replaced.

## 4a. Where it fits with the other work

**With the engine overhaul (D4-103; engine_overhaul.md):**
- **Phase 3 (variance and risk, next) plans** "woods feeding game and forage", "rats in stores" and a wolves incident. These are the
  wild layer's.
- **Proposed:** phase 3 builds the scheduler, the building risks and bad-year capacity, and leaves those three to the wild layer,
  so nothing is built twice.
- **The overhaul lists ecosystems as "hooks only",** and living_populations said "after phase 3". The wild layer is its own work after
  phase 3. Whether it goes before or after phase 4 (the larger experiment) is Zach's call.
- **Fits the format:** stocks with renewal rules, yields as distributions, the capacity model reading declared rows, packs.

**With other proposals:**
- **living_populations.md:** this is its design carried out, with the land as areas from the generator (its step 4 made cheap) and
  W2's rules for eating.
- **environment_state.md and phase 3:** conditions are derived, not stored. The store keeps only what must persist (counts,
  condition, the mast's budget, memory, traces); frost runs and wetness are read from the climate.
- **The ecology era** (D2-76, the scheduler): the era sets the odds of mast years; the trees' budget sets each year.
- **wildlife.md (D2-192 to D2-198)** gives the kinds and their techniques and rights; wild_systems.md gives their layers, signs,
  lore and the waves (§13, to confirm); husbandry.md and wild_plants.md give keeping and the plants. Their mechanism sections would
  point here.
- **node_ecology.md** gives the relevance test this must pass.

## 5. Experiments: what was wrong with wave 1's, and how they should be designed

| Wave 1 did | Instead |
|---|---|
| a standalone village with my own acts and costs | **engine runs:** real agents in worlds generated with the pack on, the work of a watch felt in the next day's hunger (D4-108) |
| hand-written kinds with no web | kinds on the ecology step; tests that the chains appear under their conditions and not otherwise |
| scripted readers over features I chose | the information in the signs measured from the state (what a reader could know), separately from what agents do with it |
| real species the models already knew | an arm with **invented kinds and rules** (renamed, with rules unlike any real animal's), so learning is separated from knowing |
| no null arm | the same world with the pack off (D4-104) |
| two villages, one weather draw | several generated worlds and seeds per arm, sized for the effect |

**The tests of the system itself, before any agent:**
1. **No kind in code** (the guard test).
2. **Replays exact,** with the pack on and off; cattle behave exactly as before.
3. **Counts conserved** between areas, groups and takes.
4. **Calibration** on generated worlds: densities near real anchors; years and eras varying as real ones do (W2's tests).
5. **Chains appear only under their conditions:** a mast failure after a heavy mast sends boar to the fields; a hunted-out wood
   sends wolves to the herds.
6. **Responds to people within a run:** a watch, a hunt or a felling changes what happens within 12 days (wild_systems §8).
7. **Relevance by village:** each kind moves some household's food or work by about 10% somewhere (node_ecology.md).
8. **Variety by land:** villages differ in which kinds matter to them.

## 6. Scope

**Phases** (sizes: S under 300 lines, M 300 to 1,000, L over 1,000; each phase with its tests):

| Phase | What | Who | Size | Shows |
|---|---|---|---|---|
| **0. Foundations** | merge the generator's land fields and node `xy` (`climate-calibration`); the engine keeps `ecosystem`, `land` and stock parameters (schema bump); the land summary (areas) written with each world; **the climate calibrated** against real spell lengths, frost runs and seasons under compressed time, with its eras | 37.2 (generator, calibration); 37.4 (init, schema, climate) | M | the environment the rest builds on |
| **1. The ecology, offline** | the store and the step as pure functions (W2's rules) on 12 to 15 kinds; history before the run; calibrated on generated worlds (densities, years, eras, chains) | 37.2 | M | the coarse ecosystem, varying by land and era, with the chains appearing under their conditions |
| **2. The ecology in the engine** | the step in the night (pack `wild`); eating parcel stocks; mast from the trees; fish and eels extended; takes from the store in place of `game`; capacity under a harvest | 37.4 (hooks, capacity); 37.2 (rows) | M | replays exact; pack off unchanged; counts conserved |
| **3. Groups near people** | the wild-groups table; condensing; the drive, lead, memory and answers (D2-197, D2-198); fences and trampling through herds' functions; traces; signs with readings by skill; watches, scares, hunts, crews at the weir; the stores' pest step | 37.4 and 37.2 | M-L | wave 1 as a system |
| **4. Wave 1 tested** | the system tests (§5); an engine experiment with agents: generated worlds, the pack on and off, an arm with invented kinds; Haiku, Sonnet and Opus | 37.2 | S + runs | whether it matters to a society and can be learned |
| **5. Husbandry** | cattle onto the beasts entity; sheep, pigs, poultry, dogs and hounds as rows; beasts' needs (D4-103 mechanism 8; L-36) | 37.4 | L | kept and wild as one |
| **6. Wave 2** | wolves, the fox with the lambs and hens, voles with owls, ravens on carcasses, hounds; drives and bounties (work by several) | both | M | chains between kinds reaching the fold |
| **7. Wave 3** | phenology; fast kinds on crops; bees and wasps; ergot; fungi; calendar markers; lore lines for every trade (lore.py) | both | M | the weather year; lore that fails |
| **8. Wave 4** | disease by host and area, between kinds and villages | both, after phase 3's hazards | M | what travels |
| **9. Wave 5** | colonies, engineers, rare kinds, individuals | both | M | the land that changes |

**The first slice worth building** is phases 0 and 1. They touch almost nothing of 37.4's (one schema change and the generator
merge), and they settle whether the coarse ecosystem behaves on the generated land before any engine work.

**What happens to wave 1 as built (02zp part six):** it stays as a prototype of the micro layer (raids, memory, answers, signs by
skill). Its tests are read as tests of that layer only.

## 6a. As built on the `ecology` branch (9 Nov; D2-199)

Code on the branch, not on main. All 433 tests pass there, including 35 for the layer.

| Phase | Built | Where | Not yet |
|---|---|---|---|
| **0** | the generator's land fields merged in; a **land summary** written with every world (59 areas for four villages and a wild node, 104 links, rivers' flow, about 33 kB); world schema 5: `s.wild` and a parcel's `ecosystem`, held only with the `wild` pack; the `set_wild` primitive | `cybertron2/wild/areas.py`, `landgen/write.py`, `engine/schema.py`, `engine/world.py` | **the climate's calibration** (spell lengths and frost runs under compressed time, the eras) |
| **1** | 14 kinds as RESOURCES rows (pack `wild`, renewal `population`); the **ecology step** on the food web's rules, a day at a time, with the climate by place, soil wetness, summer warmth, an irregular mast and keyed outbreaks; a history before the run; an offline runner on five generated worlds | `cybertron2/wild/kinds.py`, `ecology.py`; `docs/review/.../wildlayer/offline.py` | calibration backlog (below) |
| **2** | the step in the engine's night, with the pack only; the **bridge**: wild kinds eat a real-yield crop and store, and the year's share eaten is drawn from the engine's crops and stores (4 to 10% of the standing crop and 3 to 5% of dry stores over 16 nights); shyness near people (busy land lowers a kind's habitat, by the kind's data) | `engine/wild.py`, `engine/night.py` | takes from the store in place of `game` and `hunt`; capacity under a harvest (37.4) |
| **3** | **groups near people** for whole-counted kinds (boar, red deer): condensed from their ring's count; a drive from the area's hunger; a lead of engine days leaving traces (D2-197); raids on a field; a **night watch with a scare** (fire, clapper, horn, the dog) answered by the kind, getting used to it or harmed by the dog (D2-198); memory of a field. **Traces** on parcels, read by the senses two ways: a practised hunter reads "fresh rooting at the wood's edge: a sounder of about 14", anyone else "the turf by the wood's edge turned over" | `engine/wild.py`, `engine/signs.py`, `engine/verbs.py`, data rows | deer at the ricks in frost; raids on stores; the fox and the wolves at the fold (wave 2, after husbandry) |
| **4** | three small agent runs on one generated world (17 people, Opus at each household's head, Sonnet and Haiku); see History | scratchpad runs, not committed | the experiment proper: the pack on and off, invented kinds, several worlds |
| **6 (wave 2)** | wolves (a pack gathered from the land beyond the ring) at the herds, leaving a carcass read as a kill; the fox at the **hens, kept as a house's stock** (six a house with beds; they lay); shutting the hens in; ravens over carrion; voles' numbers as signs | `engine/wild.py`, `wild/kinds.py`, data rows | sheep, pigs, poultry and hounds as beasts (husbandry, 37.4) |
| **signs** | every mechanism with its bundle by the four kinds of sense, from the kinds' data: a group's edge, raid, try (a raid that took nothing) and turn; a watch's own night (to the watcher only); what the kinds ate, on the fields and in the stores; the mast in flower and fallen; a kill by a wild kind; **a hunt as a noticing process of its own** (as the road's), remembered of the place; a technique's `reads_as`, so every way of hunting reads a hunter's signs | `engine/signs.py`, `wild/kinds.py`, `engine/perceive.py` | calibration of `own` against the guide's evidence |
| **7 (wave 3)** | **loads**: slugs, aphids with ladybirds following, fungi, as a level an area moved by the weather on the area's ground (`wild/loads.py`); harm to crops of a family at an age, cut by a guard (picking slugs by lantern, topping the beans); a fungus flush filling the woods' wild food. **The year's markers** from degree days (blackthorn, swallows, oak and ash, the may, the first frost), with lore that holds and lore that fails, measured on the climate | `wild/loads.py`, `engine/wild.py`, `engine/signs.py` | wasps (with bees, after husbandry); ergot (needs a grain's quality and illness from eating it, engine gaps) |
| **8 (wave 4)** | **disease by host and area** (`wild/diseases.py`): each disease's prevalence among its wild hosts by area, rising with crowding among the not immune, spreading along the land's links, burning out into immunity; murrain in the deer, mange in foxes and wolves, a hare sickness. **Murrain in kept cattle**: caught from sick herds on the same parcel (most), beside it, in the village, from the deer, now and then from beyond; carried between villages by a herd driven there; carcasses read as a sickness, and by a herder as murrain | `wild/diseases.py`, `engine/wild.py`, `engine/signs.py` | rabies (bites need illness in people); a disease of people; milk lost to sickness (the herd's milk is set by farm.py) |

**Calibration backlog** (offline, five worlds, 24 years):
- **boar barely follow the mast:** 3% variation between years, because crowding holds them below the food limit;
- **voles do not cycle;**
- **densities off:**
  - red deer at 0.2 to 0.3 of real;
  - foxes about 0.3;
  - bears 4 to 6 times too many;
- **eels and wildfowl live only in the fen world** (the others' water is small rivers);
- **what does vary:** deer 4 to 13% between years, hares about 12%, woodpigeons 10 to 18%.

## 7. Alternatives considered

- **A separate wild world beside the engine** (wave 1 as built). Fast to try, but the society can only reach it through bridges, and
  it drifts from the real world. Rejected.
- **Kinds spread across parcels, herds, renewal, spoilage and forests, each where it touches.** Chains between kinds have no home,
  and adding a kind means edits in five places. Rejected; this is how the generic `game` stock grew.
- **The full W2 web of 37 kinds.** It was built for regional realism; a run needs the 12 to 15 kinds that the waves use.
- **The field on a uniform 1 km grid** (living_populations §2a). The interface experiments show the area cut gives the same answers
  far more cheaply.
- **No coarse ecosystem, groups only** (pure Rain World). It loses the chains between kinds and the odds that make a group appear,
  leave or return.

## Open questions (for Zach)

1. **The design:** ten systems; areas from the generated land; kinds as RESOURCES rows; one ecology step on W2's rules for 12 to 15
   kinds; groups near people; everything through the engine's primitives, senses and verbs. Right?
2. **Beasts:** wild groups in their own table first (cattle untouched), and one entity with husbandry later? Or one entity from the
   start (a large change to tested code)?
3. **Where in the overhaul:** after phase 3, and before or after phase 4? Should phase 3 leave "woods feeding game", "rats in
   stores" and the wolves incident to this?
4. **Who builds what:**
   - 37.2: the generator, the ecology's pure functions and the rows;
   - 37.4: the engine hooks, schema, herds and capacity.

   This needs agreement with 37.4, so it needs the board, which is closed to me for now.
5. **Phase 0 now:** merge the generator's land fields into main, and calibrate the climate (with 37.4)?
6. **The merged waves** (wild_systems.md §13), amending D2-192's order?
7. **Consolidate the proposals:** the mechanism sections of living_populations, wild_systems, node_ecology, husbandry and
   wild_plants point here, and they keep their content?

## History

- 9 Nov: proposed after Zach's points that wave 1 was not built as general systems and that everything should build up from the
  generated environment; reconciles living_populations.md (and 37.4's review of it), W2, node_ecology.md, the interface experiments
  and wild_systems.md.
- 9 Nov: Zach: "build it on your own ecology branch" (D2-199). Building there, engine code included, for review before main.
- 9 Nov (later): phases 0 to 3 built on the branch (§6a), with the climate's calibration, the takes from the store, capacity under a
  harvest and the engine experiment still to do. Three fixes on the way:
  - the food web's seasonal eating caps taken a day at a time;
  - shyness near people;
  - the bridge measured against the model's year of crop, not its day's standing pulse (first versions ate half the crop in 16
    nights).
- 9 Nov (later): Zach: "hunting could vary: they could look specifically for something, or just hunt in general ... sometimes find
  something they weren't expecting ... hunts should be able to target some things, a range". Built on the branch as the general
  taking system, not a wave:
  - five ways of hunting as technique rows (taking what comes, stalking deer, a boar hunt, snaring hares, fowling);
  - a range (near, the wood around, far) and a quarry to look for, as modifiers;
  - what is met is drawn from the areas covered, by numbers, how easy each kind is to find, and focus;
  - flight, danger divided by a crew (D2-193), a kill off its area's count and its group.

  Wave 2 waits: its fox and wolves at the fold need sheep and poultry (husbandry).
- 9 Nov (later): wave 2 built without waiting for husbandry: the hens as a house's stock (an item) and the wolves at the cattle
  herds the engine already has. Sheep, pigs and hounds still wait.
- 9 Nov (later): agent runs 1 and 2 (8 days each, about $8 and $11). Run 1: the agents kept to the old generic hunt (fixed: the pack
  turns it off, `off_with`) and no raid came (the drive raised). Run 2: 30 hunts taking what comes, 16 deer stalks and 17 snarings,
  ranges used, a quarry named twice; five night watches; raids by the fox (three, none took a hen), the wolves (two calves) and the
  deer (one field); the boar turned once by the dog. Opus heads read the signs and acted on them in words ("a wolf pack, about four,
  prowling the edge of South Wood ... bring them in nearer the Green at dusk"; "Feathers and blood by the hen house ... shut the hens
  in at dusk"), but no one shut the hens in.
- 9 Nov (later): Zach: "do a sweep of all the various wildlife and other systems added and if all the relevant mechanisms have
  appropriately accompanying bundles of signs ... There may be new types: just as seeing signs on the road is a specific process so
  too might be going out to hunt". The sweep (above, "signs") found and fixed four signs not grounded in state:
  - a fox raid that took no hen still read "feathers and blood" (now a try's signs: the earth scraped under the door);
  - a beast the wolves killed read "no mark on it: it went down where it stood" (now torn and half eaten, and to a hunter, wolves);
  - every wild sign was gated on the old hunt, which the pack turns off, so a deer stalker read them as a layperson (`reads_as`);
  - the ecology stepped its seasons from day 0 while the calendar began in summer: one season apart in every run so far.
- 9 Nov (later): wave 3 built (above). Calibrated offline on the steady, cold and wet climates over 12 years: slugs take 1 to 2% of a
  young crop in a median year, 11 to 15% at the 90th percentile and up to 26% (02zp §24: 4%, 12%, 27%); blackfly 2 to 3% of the beans
  (9% at the 90th); fungi flush in about 40% of autumns, more in the wet era. The markers' lore measured: a frost after the
  blackthorn in 15 to 18 of 60 village-years (so its reading says a cold snap often follows), after the may in none, so "the frosts
  are done" holds; "oak before ash" has no tie to the summer's rain and is kept as lore that fails. On the way, the ecology's soil
  wetness became a slow bucket (it halved on every dry day, so grass "drought" came every few days).
- 9 Nov (later): agent run 3 (spring start, 8 days, about $11), after the sweep and wave 3. Slugs grazed four fields; one head of
  household (Opus) read "the young corn grazed off to stumps" and picked slugs by lantern on two evenings, and asked her father to
  "keep the slugs off the barley"; another (Opus) asked his herdsman (Haiku) to watch the barley against the boar, the fire watch
  set that night turned the sounder; the wolves took a calf and a cow; a fox took all six of one house's hens (no one shut them in,
  in this run either); a herd of 13 deer raided one field twice. The run's own trouble is not the wild layer's: two elders die of old
  age by day 5 in every run (bots too), and others starve in a cold spring.
- 9 Nov (later): wave 4 built (above). Calibrated offline (16 years; the land of a four-village world): murrain in the deer in 2
  years of 16, local; mange one wave across the land, foxes 15% down in its year and about 8% below the disease-free run after;
  the hare sickness local in 7 years of 16. In the herds (3 years, four villages of 12 beasts): outbreaks in three villages, 5
  beasts dead, milder than the great murrains (calibrate). A fix on the way: without immunity every disease that spread faster
  than it cleared stayed in every area for ever.
- 9 Nov (later): Zach asked for an audit against wild_systems.md, every specced layer for the kinds built so far, the plants
  ("Yes to all build this": D2-200 to D2-202) and an audit of one-offs. Audit and results: `docs/review/37_growth/02zq_wild_audit.md`.
  Built on the branch: the plant kinds with one stock for the wild kinds and people; the animals' layers by general rules
  (conditions and effects, targets as data, fences, the gap, hunting pressure, wounds, the expert's reading, the layers' signs as
  they begin, weather leads, notices while working, litters, a take's nights, the harvest's vermin, migrants' return). Not built,
  with the reason: the vole cycle (the rule does not cycle them), individuals (wave 5), what needs husbandry or illness in people.
- 9 Nov (later): agent run 4 (autumn start, 8 days, $11.63). Gathering wild food was the most common act (84): 27 acorns, 26
  mushrooms, 23 hazel nuts, 9 hedge fruit. One untaught gatherer (Opus) was made ill by mushrooms; the same head of household then
  leached acorns into meal twice. Agents moved between woods as one was "picked clean" ("try Hazelden Moor: berries, hedge fruit,
  roots"). The wolves took a calf and a cow; the night's sign ("something bellowed on West Pasture last night and then went quiet")
  and the tracks ("about two of them") had heads of household telling their herders to count the beasts and bring them in at dusk.
  One shut the hens in "because there are foxes and wolves about". Murrain came from beyond on the last night. The rut, plovers
  before the freeze and the first frost reached three agent-days each and drew no comment.
- 9 to 10 Nov (overnight, Zach: "Then the filling out of the expert details for all the wildlife. Then continue the phases as you
  see fit adding a test (you can do two live runs at appropriate times) to investigate"):
  - **expert readings (L3) for every kind, load, marker, disease and plant**, read from the state: in a hunt, about how many, their
    condition, their wariness and hunger; owl pellets in a vole year; rats breeding in the thatch; what a kill means for the herd;
    markers early or late; oak before ash as a warm spring only (the lore's truth); a heavy or light year in the plant gathered.
  - **live run 5** (winter into spring, 8 days, $9.35; six heads of household given expert skill): the experts used what only an
    expert reads. Gervase (Opus): "hunt the woods around for the unwary red deer"; Jocelin (Opus): "About 20 roe hold South Wood
    ... I'll stalk a roe", later "Hares are fat and plentiful on our land ... I'll hunt them all day"; Susanna (Opus) to her
    household: "There are fat hares lying out on the open ground, about 7 of them. Try for them today". Deer took hay from the ricks
    in the snow twice; the wolves again took a calf and a cow (the same keyed nights as run 4: the wild layer's nights depend on the
    world's seed far more than on the agents).
  - **wave 5 built**: sites (heronries, rookeries, beaver lodges) placed where the land suits them, back each season grown or crashed,
    a heronry troubled in spring leaving for good, herons at the fish, rooks at the young corn unless watched, a beaver dam flooding
    the meadow and raising the fish, the young taken, beavers trapped; individuals (D2-195): leaders named on demand (the old sow,
    the old dog-wolf), a group scattering when its leader is killed, legendary beasts seldom (the great boar, the white hart);
    rare regimes (a great freeze, a vole plague, two bare masts) with what the elders remember, read by the old.
  - **one-off 2 done**: a watch's scare is made of what is there (a fire burns firewood; clappers and a horn are made and carried; a
    dog watch needs a dog at home); picking slugs moved to dusk so it claims no lantern. The night itself (one-off 1) waits for D2-21.
  - **the vole cycle, built as the design specced it** (02zp §23: the vole phase, a pulse shared by a world's villages, like the
    mast): a phase clock, low, increase, peak, crash a year each, set ahead by a mast, held once by a hard winter. Voles now cycle
    three to four years, sevenfold peak to trough, the owls a year behind (0.7 down to 0.37). The emergent route failed: a specialist
    predator (weasels and stoats, tried offline) and a delayed crowding both leave the voles flat (cv 0.01 to 0.06), because the food
    web's stabilisers (a day's eating capped, prey refuges, crowding) damp any predator-prey swing.
  - **live run 6** (spring, 8 days, $11.56; a generated world with a heronry and a rookery, 19 people, legends made likely for the
    run by an experiment's knob): the heronry left on night 1, troubled by people gathering firewood in its wood; a head of household
    went for the young herons on day 3 and found it gone. Fixed: only felling, hunting and robbing at the nests trouble it. The rooks
    took about 2.5 a night of the young corn for four nights; one head of household made clappers and watched the field. Hens shut
    in nine times (once in earlier runs), after "wolf tracks by the wood's edge" and rats in the store ("shut the hens and the store
    in tonight": a door does not keep rats out, a misbelief the world can correct). An expert herder read "about 40 red deer by
    Hazel Copse" and made a weapon to go after one; another reaped a field early "or the deer will finish it" (the lever "reap
    early"). No one hunted far enough to meet a legend. Three deaths of old age again (the life model, not the wild layer).

## Sources

- living_populations.md, wild_systems.md, node_ecology.md, wildlife.md, husbandry.md, wild_plants.md;
- 02zp parts two to six;
- the engine's code (§4).
