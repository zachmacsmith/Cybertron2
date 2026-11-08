# Proposal: phase 3 of the engine overhaul, variance and risk (the scheduler, building risks, the woods, bad years)

**Status:** discussion (8 Nov); an exploration of what phase 3 builds, nothing built. **Owner:** 37.4 (the engine); the rules it
builds are 37.2's decided design (spec/environment/scheduler.md, D2-69 to D2-79; proposals/environment.md,
environment_catalogue.md, building_risks.md). **Affects:** engine (a new scheduler.py; environment.py, night.py, farm.py,
forests.py, buildings, fuse.py, signs.py), data (a KINDS table, RISKS on structures and fittings), the capacity model (bad years),
spec/environment/scheduler.md (37.2's: "as built" lines only).

## Summary

Phase 3 gives the world **variance that is the same in every arm and consequences that are not**:
- the scheduler's years and spells;
- incidents drawn against hazards;
- things that carry their own risks.

It also gives the capacity model what real analysis says it lacks: **the bad year**. Most of the design is decided (D2-69 to
D2-79); what is new here is:
- how it sits on the declared process model (D4-103), as data plus registered rules;
- how it meets crops that grow by the season (D4-106) and labour (phase 2);
- the signs;
- the experiment E3.

## 1. Where things stand

| Piece | Decided | Built |
|---|---|---|
| layers: eras, years, spells, incidents, spreads (D2-69) | yes | only the day's weather within a hand-written spell |
| draws keyed by kind, place, day; exposure from local state (D2-70) | yes | the weather draw only |
| risks on things, raised by neglect (D2-71) | yes | nightly breaks by structure and cold (D2-168), wear (phase 2) |
| fires spreading, signs across edges (D2-72, D2-74) | yes | no |
| eras as starting conditions; four families (D2-73, D2-76) | yes | no |
| the first-world kinds, every kind as data (D2-77) | yes | the stray herd (hand-placed, dawn) |
| six spreading patterns (D2-78); windfalls by possession (D2-79) | yes | no |
| hidden state of places (environment_state.md) | discussion; L-23 flagged later | soil, stocks, condition only |
| crops by the weather (L-68) | flagged later | by the season (D4-106) |

## 2. The shape: one scheduler, data plus registered rules

**engine/scheduler.py**, in the pattern of renewal.py and yields.py.

**At generation, read from the seed only:**
- the era: a starting condition (D2-73), pinned or drawn;
- each year's moisture and temperature: the era's anomaly plus the year's own draw;
- every day's spell: a semi-Markov chain by season and year: dry, wet, normal, cold snap, storm.

These go into the record (`s["env"]`) on day 0, so a run's weather is its own and a replay reads it back. The day's weather keeps
its keyed draw within the spell (environment.weather, as now).

**Conditions: pure functions of the record and the land, not stored state** (`scheduler.conditions(w, place, day)`):

| Condition | Read from |
|---|---|
| dryness | the run of dry days |
| wetness | rain in the last days, against the parcel's height and ground |
| river level | rain upstream and the season |
| fuel dryness | dry days, cover, season |
| a cold night | a cold snap or winter; it replaces the hand-written `cold_days` |

Being derived, they need no update loop and cannot run away. This takes the minimal part of environment_state.md (its hazards'
exposure terms) and leaves its stored variables (water table, damp, vermin, filth) for later.

**Kinds: one row of data each** (KINDS, by the catalogue's vocabulary):

```
"house fire": {at: building with a lit hearth or oven,
               hazard: {base, by_spell: {dry: 3, storm: 2, wet: 0.3}, by_structure: {wattle: 2, timber: 1, stone: 0.2},
                        exposure: "fire_load"},        # registered: hearth, oven firings today, thatch, a woodpile at the door
               spread: {pattern: adjacency, to: buildings next door, hazard: {...}},
               effects: [{rule: "burn", share: [0.3, 1.0]}],    # an outcome distribution (outcomes.py): the act samples, analysis takes the mean
               fuse: "fire",                                    # those near are woken: fight it, save goods, flee (fuse.py, as raids)
               signs: "HOUSE_FIRE"}                             # a bundle (signs.py)
```

- **Hazard:** base × the spell × the season × the land kind × exposure, as D2-69. Exposure is a registered function of local state.
- **The draw:** U(seed, kind, place, day), paired (D2-70). Two arms meet the same draws; they differ only where their exposure
  differs. One arm's thatch catches; the other, built in stone, does not.
- **Effects:**
  - They go through World.apply primitives, with the scheduler as their cause.
  - Each is an outcome distribution, so the capacity model can take expected losses from the same rows (D4-103 part 2).
  - A new effect is one function registered by name, as a renewal rule is.
- **Spreads:** the six patterns (D2-78) as six registered neighbour functions:
  - adjacency: parcels, buildings;
  - contact: people, herds together;
  - carriage: goods and travellers on edges;
  - flow: downstream;
  - track: a line;
  - place-bound.
- **A world file** may pin, scale or turn off any kind (`environment: {kinds: {...}, off: [...]}`). `environment: off` is the
  engine before phase 3. At zero it writes nothing, so phase 2's runs replay, as phase 2's labour table did.

## 3. What phase 3 builds (the plan's four items, cut into steps)

| Step | What | Reads | Writes | Notes |
|---|---|---|---|---|
| **3a** | the scheduler: era, years, spells drawn; conditions | the seed, the land | `s["env"]` | the hand-written `spells` and `cold_days` stay as overrides |
| **3b** | the weather into what grows (L-68, the season part kept) | conditions | growth rates | drought slows growth on dry ground and thins forage and pasture; a cold snap in spring gives cold nights, so D4-106's frost rule thins young tender crops with no new code; wet spells raise blight |
| **3c** | incidents and spreads, the economic kinds: drought (a spell, 3b), river flood, gale, hail, late frost (3b), blizzard on hills, house fire, wildfire, blight (moved from the sowing's draw into a spreading kind), smut in seed, rats in stores, murrain and wolves (with cattle) | conditions, exposure | primitives | disease kinds (fen fever, winter cough, pox) as rows with no effects yet (OPEN Q-16) |
| **3d** | windfalls (D2-79): a bumper year on a holding, flood silt (fertility), storm-felled oaks (timber lying), a mast year (game and forage up), a stray herd | the same | the same | no rule of their own: whoever finds one takes it |
| **3e** | risks on things (D2-71; building_risks.md): RISKS rows on structures and fittings | the spell, snow lying, height, condition, neglect | condition, contents | D2-168's nightly breaks become the first row; snow load on wattle; thatch in a gale; a cellar flooding on low ground; rats in bins (less in a granary); damp fuel (§4) |
| **3f** | the woods feeding game and forage; drought drying dead wood | trees, young growth, conditions | game and plants K | game's K follows the wood's trees and young growth (felling and grazing lower it); a dry spell dries dead wood (more heat, and fuel for wildfire) |
| **3g** | bad-year capacity | the scheduler's years, drawn for many seeds | capacity reports | §5 |
| **3h** | the signs of all of it | the incidents, conditions | facts | §6 |

**Damp fuel** (from building_risks.md and the resources spec):
- fuel lying out in the rain (a woodpile at the door, D4-89) is wet;
- wet fuel gives half its heat until a dry day dries it, or until it is moved into a woodshed;
- the woodshed, now only a store, then pays.

**How it meets phase 2:**
- An incident makes work: a roof to mend, a fire to fight, sheaves to save before the storm.
- Pushing on (the reply's overwork) then has its natural use.
- The capacity model's work and upkeep gain expected repairs.

**How it meets D4-106: can apart from works.**
- Weather refuses nothing except what is physically impossible: a ford is high (exists), deep snow closes a pass (exists).
- It changes how well things work: a crop in a drought, hay in the rain, a fire on a wet day.

## 4. Variance as a measure: the same draws, different consequences

- **Common random numbers.** Arms with the same seed meet the same weather and the same draws. They differ only by exposure: what
  people did. So an arm's losses against its null arm are the consequences of its choices, not luck. Bad luck in one arm and not
  in the other cannot happen at the same seed.
- **Era as an experimental factor.** The same world under a steady era and a dry or stormy one, same seeds: what a society does
  when its world turns against it.
- **Truth log.** Every condition, hazard, draw and incident goes to the run's truth (the journal), never to an agent: analysis
  reads what happened, agents read signs.

## 5. Bad-year capacity

38.61's hole 2:
- Halstead and O'Shea: societies plan for the bad year, not the mean.
- MSY under variance: a take that is steady in the mean year collapses a stock in a run of bad ones.

What the model gains:
- **The capacity becomes a distribution.**
  - For K draws of the year (from the world's era: the scheduler's own draw for seeds 1 to K), the model runs:
    - crop growth under each day's conditions (the same grow_night with 3b's rates);
    - forage and pasture;
    - the expected losses of each kind at the land's exposure.
  - It reports the people supported in the median year, the 1-in-10 year and the 1-in-20 year.
- **The buffer that bridges a bad year:**
  - the stores needed so that the 1-in-10 year starves nobody;
  - against what the world holds;
  - and against the granary space to keep it (spoilage by store).

  This is the measure of storage that E2 asks about.
- **Diversification shows.** Plots in two places, two crops, a herd and a field: their correlated losses are lower, and the
  1-in-10 year improves without the mean moving. This is the real logic of scattered strips.
- **Wild stocks under variance.** The steady take that holds a stock in a mean year can collapse it in a run of dry ones; the model
  reports the take that survives the 1-in-10 sequence.

The same report sets a world's difficulty in two numbers, the mean and the bad year, rather than one.

## 6. Signs

Every kind gets a bundle in the four kinds of guides/senses.md. The guide's evidence decides the shape:
- **Forecasts** were never acted on.
- **Changes that bear on today** almost always were.

So a precursor is written as a change one can act on now, not a forecast:
- "the river is rising, brown and fast";
- "smoke on the ridge above the Coppice";
- "the thatch on the Hearne hut is lifting at the eaves";
- "droppings in the bins, the sacks gnawed".

| Kind | Before (a change) | During | After (lingering) | Conditional |
|---|---|---|---|---|
| drought | "nine days without rain: the ruts are dust"; "the stream is low"; crops "short and pale" (D4-106 signs) | the wheel turning slowly | cracked ground | the meadow "browning" |
| river flood | "the river is rising, brown and fast" (a fuse for those on low ground) | water over the low field | silt and drowned crop; "the water mark on the wall" | night: its roar |
| gale | "the wind is rising, the trees roaring" | thatch torn, a tree down | a fallen oak across the ride (timber) | ripe crop "beaten flat" (exists) |
| house fire | smoke at the eaves (those inside, near) | flames, the roar, the glow (exists in signs for fires) | burnt rafters (exists) | rain |
| wildfire | smoke on the ridge | the wood burning | the wood black and open | dry: fast |
| rats | droppings, gnawed sacks | rats seen by day | the store's loss | warm and wet |
| blight | "the barley is spotting black" (exists in part) | withering (exists) | | wet spell |
| murrain, wolves | the cows off their feed; tracks at dawn | | a carcass, a missing calf | snow: tracks |
| windfalls | | a fallen oak, a stray herd, a heavy crop ("the ears bow the stalks") | silt dark on the field | |

**Plainness follows Zach's rule (8 Nov):** very bad states are plain; slight ones need a close look or a knack (a farmer reads
blight early, a herder murrain). Each bundle is calibrated through the noticing rule (the guide's step 4).

**Slow change** (the era) has no sign of its own. It reaches people only by accumulation:
- memory ("the third dry summer");
- the lore (D4-105's mechanism can hold "a red sky at dawn: the wind will rise");
- records.

So writing and keeping records gain a value they lack in a steady world.

## 7. What agents meet: the fuse

- **House fire, flood on low ground and a wildfire at a wood's edge** call those near through the fuse system that raids use
  (fuse.py: woken in the night or the day, one choice from a short list).
- The choices:
  - fight it: a bucket line, by numbers;
  - save what one can;
  - drive the beasts out;
  - flee.
- The outcome: an outcome distribution over the fighters, the structure and the weather.
- **Mutual aid and insurance need no new rule:** helping is a choice; a fire club is an agreement whose pay-out leg is conditioned on
  the incident (environment_catalogue.md §5). Whether one is made is a result.

## 8. Checks and E3

**Checks:**
- With `environment: off`, phase 2's bot runs replay exactly. The same inertness test as phase 2's labour table.
- The scheduler's draws are a pure function of the seed: arms with one seed meet the same weather and draws (a test).
- Every kind's hazard and effect has a test of its mean against its samples (as the hunt's).
- The capacity model's bad year agrees with the engine run over the same seeds, scripted.

**E3**, after phase 3:
- **E3a: bad-year capacity on every world, K = 50 seeds** (free). The spread of each world, and the stores each needs for a
  1-in-10 year.
- **E3b: one LLM probe, paired by seed.** A village under a steady era against the same village under a dry or stormy one, 32
  days, one seed each, about $40 to $60.

  What to read:
  - deaths and missed meals against the null;
  - stores kept;
  - whether they build a granary or woodshed, or mend roofs before the storm;
  - fires fought together, aid given, agreements made;
  - read with the end state, as scenario_design asks.

## 9. Size

| Part | Lines (about) |
|---|---|
| scheduler (layers, conditions, kinds, spreads, effects registry) | 500 to 700 |
| kinds and risks as data (the first set) | 300 to 400 |
| weather into growth, forage, fuel; woods feeding game | 150 |
| fuse calls for fire and flood | 150 |
| signs (about 12 bundles) | 300 |
| bad-year capacity | 200 |
| tests | 400 |

**About 2,000 lines**: phase 2's size and a half. Ordered so that each step is usable alone:
- 3a, then 3b (crops feel the weather), then 3c and 3e together (incidents and risks share the hazard machinery);
- then 3f, 3d and 3g, with 3h written alongside each.

## Open questions (for Zach)

1. **Scope.** All of 3a to 3h, or a first cut? My suggestion for the first cut:
   - the scheduler;
   - weather into growth;
   - drought, flood, gale, house fire, rats;
   - risks on wattle, thatch and damp fuel;
   - the woods feeding game;
   - bad-year capacity.

   The rest as rows later.
2. **The era in a run.** A run is about one compressed year, so the year's severity is the lever that matters within a run. Eras
   matter across continued runs. Draw one year per run from the era, as decided (D2-73)?
3. **Stored hidden state** (environment_state.md: water table, damp, vermin): leave it for later and use derived conditions
   (recommended), or build a first variable or two (a store's vermin, a building's damp)?
4. **Wolves:** an incident now (catalogue), or wait for living_populations.md (37.2, discussion), which makes them a population
   that moves? Recommended: an incident row now, replaced when populations are decided.
5. **Harshness targets** for calibration: how far should a 1-in-10 year cut capacity (30%? 50%?), and how often should a house burn
   in a year in a wattle village?
6. **Growth by the weather (L-68):** take its first part here (drought and cold snaps through 3b), leaving warmth day by day for
   later?

## Alternatives considered

- **Hand-written incidents per scenario** (as now): exact, but no variance, no bad year, and no common random numbers across
  seeds. Kept as overrides.
- **A full hidden-state cascade** (environment_state.md): richer couplings, but runaway loops and calibration cost. Its exposure
  terms are kept as derived conditions; stored variables later.
- **Bespoke code per incident:** the pattern D4-103 replaced; every kind is a row with registered rules.

## History

- 8 Nov: written (37.4) at Zach's request, while E2 runs: "explore what you will build for phase 3. Don't build it yet."

## Sources

spec/environment/scheduler.md (D2-69 to D2-79); proposals/environment.md (§3 to §8, §11, §12), environment_catalogue.md,
building_risks.md, environment_state.md, living_populations.md, engine_overhaul.md (phase 3), crop_growth.md (D4-106, L-68);
guides/senses.md; review 38.61 (holes 2 and 6); engine/environment.py, fuse.py, night.py (breaks).
