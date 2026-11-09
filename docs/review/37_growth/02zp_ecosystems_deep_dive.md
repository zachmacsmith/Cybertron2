# 02zp · Ecosystems that interact: a deep dive, with models on generated land

Current as of 8 Nov 2026 (37.2). Reading page: https://claude.ai/artifact/GcjZVEgWVz5ZL1TchnJTKH (private; source in 02zp_ecosystem_models/ecosystems_page.html). Session note: analysis only. Nothing here is decided; no proposal or spec is changed by it, and
nothing was posted on the board (Zach, 8 Nov: "don't post anything more on the board for now"). Models, results and the probe:
[02zp_ecosystem_models/](02zp_ecosystem_models/README.md).

Zach, 8 Nov: "lay out the different potential ecosystems, all the systems we have explored and proposed, and write out how they
could interact, how they connect back into ecosystems, economics, the purpose of the simulation ... Design ecosystems that don't
just exist but interact, have interdependencies, interesting behaviour across the different core goals ... explore calibrating
different numbers ... Run models, calibrate, have hypotheses, design interconnected systems." Scope agreed: the temperate envelope,
deepened; all four horizons (a year, 3 to 10 years, decades, generations); standalone models, engine checks, and a small LLM probe
costed first.

## 0. What I found, in short

1. **The engine's wild food is flat, uniform and too fast, and that matters more than how many kinds there are.**
   - **Forage:** about 4× need in every village, in every season. Real yields would give 0.25× (winter) to 1.9× (autumn) in farm
     country, and very different amounts in fens and woods (M4).
   - **Game:** it regrows at 0.25 a night, which is roughly what red deer manage in a year. Its sustainable take is therefore about
     25× a real deer population's (M3b, M6).
   - **The cost:** villages can live off the wild, which is the inertia scenario_design §1 warns about. It also hides the seasonal
     and regional differences that would make people store, trade and hold rights.
2. **The seasonal wild year is data only.** The built `periodic` rule gives a spring gap with the same yearly take (M6b). One catch:
   gathering yield scales with stock over the *resident* capacity, so a pulse multiplies the yield a unit of work gives (up to 14×
   in my first try). It has to be calibrated around, or capped (§6c).
3. **Placing plants by conditions works.** About 40 kinds with Ellenberg-style values reproduce 69% of the generator's settled map
   and 64% of its natural map, from soil, water and height alone (M1). The disagreements are mostly informative: the generator's
   "natural" open fen and low moor would really be carr and wood. Within a label, 14 to 38% of cells are mixes.
4. **Succession is real but slow.** Calibrated against Broadbalk, Geescroft, heath, chalk downland after myxomatosis, Wicken Fen and
   deer exclosures, it takes 10 to 45 years (M2). On the engine's clock that is 300 to 1,500 days, so it will never show in an LLM
   run. Its value is in the generator (the land as its history left it) and in long cheap runs. Only the fast parts (bracken
   creeping, nettles on enriched ground, scrub in 5 to 10 years) reach run length.
5. **The animal web gives the effects you described, at decade scale** (M3):
   - **Felling half a big wood** raises wolf kills of stock 4 to 5× for a decade.
   - **Open-access hunting** empties the woods near villages (0.7 deer a km² against 9 farther out), while refuges keep the
     region's catch going.
   - **Wolves hold deer about 25% below food limit.** That slows the woods' loss to browsing from −20% to −6% a century.
   - **Mast years** drive boar booms, and crops are damaged most in the bust year after one.
6. **Variety alone does not make villages need each other** (M5).
   - Goods in a region rise from 5 to 16, but dependence links only from 3 to 5, and specialties from 1 to 2.
   - Dependence comes from a few scarce needs: salt (96% of villages lack it), hay (62%), wood (40 to 48%). It also comes from
     seasonal surpluses that keep: smoked eels and fowl in the fen winter, nuts and mast from wooded land.
   - A second cause: the generator puts 121 of 144 villages in "river country", so they see the same land.
7. **Use decides who wins.** Draining a fen around a village doubles its grazing. It cuts its eels, fowl and rushes about tenfold,
   and its lean-season wild food to a quarter (M7). The cattle-keeper gains and the fowler, eel-trapper and reed-cutter lose. That is
   the Fens' 17th-century fight, produced by the model rather than scripted.

The design that follows from this: **five state layers, four clocks, one general rule per interaction.** The work worth doing first
is calibration, not more kinds:
- real per-hectare yields;
- seasons and yearly draws;
- game on the year clock, with movement from the land around;
- a few scarce needs.

## 1. What ecosystems are for here

The goals, and the test each implies for anything proposed:

| Goal | Where it comes from | Test |
|---|---|---|
| **G1 Leverage and dependence** | scenario_design §1 | Does it make some people need others: a store, a right, a chokepoint, a conversion chain? |
| **G2 Partial observability** | Zach, 8 Nov ("compel. partially observable environment") | Is there hidden state that people read through signs, and lore worth having? |
| **G3 Capacity as a trajectory** | Zach, 8 Nov: seasonal and long-term shifts and how they are managed | Does what the land gives change over time with use? |
| **G4 Food binds without dominating** | scenario_design §4: capacity ≥ 1.25×, food ≤ 30% of actions | Does it keep food a real constraint without famine or plenty? |
| **G5 Commons and collective action** | wildlife §1, water_and_preservation | Does someone's take harm others, and can rules help? |
| **G6 Richness at the bottom of the economy** | husbandry §6 | Are there trades and goods with uses now? |
| **G7 Cost** | README rule 10; the prompt; calibration | Lines of engine, words in the prompt, numbers to calibrate |

## 2. Every system so far, compared

| System | Status | G1 | G2 | G3 | G4 | G5 | G6 | Cost | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Engine stocks now: plants, grass, game, three wood stocks, fish, salt, dung | built | weak (everyone forages) | signs of low and high | regrowth only | **too generous, flat** (M4, M6) | weak | low | — | the base; recalibrate (§6) |
| Generator ecosystems (20) and wood depth (D2-191) | built | weak | descriptions | none | sets stocks | — | — | — | good substrate; settled layer too uniform (§5) |
| Water pack: fish runs, rods, salt (D4-103) | built | salt is scarce (M5) | runs come and go | seasonal | adds food | **upstream and downstream** | medium | small | keep; the template for seasons |
| living_populations (field, movement, observation) | proposal | refuges, halos | **strong** (signs, a collapse) | strong | ties game to land | **strong** (M3) | — | M, then L for the field | step 1 is worth it *for depletion and refill* (M3b) |
| wildlife (17 kinds, waves, D2-192 to 196) | partly decided | rights, hounds, a crew | legend, signs | seasons | small food | wolves, beaver | furs, wax, feathers | data plus 7 mechanisms | keep the waves; the food side is small in reality (M4) |
| wild_plants (20 kinds, succession, §6 conditions) | proposal | patches as lore | patch lore | **strong but slow** (M2) | seasons (M4) | heath and fen use | materials | generator M, engine S | do the generator side and seasons; succession only in the generator and long runs |
| husbandry (keeping, trades, rights, lineages) | proposal | **rights, gear, skills** | — | herd size | — | pannage, turbary | **strong** | M | the economy's link; needs §6's scarce needs |
| environment_state (hidden variables) | proposal, flagged later | — | strong | cascades | — | — | — | M-L | later; overlaps the conditions layer (§4a) |
| ecosystems.md (the wide design: zones, a planet) | kept for later | — | — | — | — | — | — | L | stays deferred; this note works inside D2-191 |

## 3. The models and what they showed

All are run on the generator's own land: 18 configurations × 3 seeds, a 50 km window in 150 m cells (`land.py`, `dump.py`).

### M1. Plants by conditions, not labels (`niche.py`)

- **Conditions,** on Ellenberg-style indicator scales, from the generator's fields:
  - moisture F from the wetness index, drier on chalk and sand and wetter under high rain;
  - reaction R from texture, leached with height and rain;
  - nitrogen N from texture, with silt on floodplains and less with height;
  - salt S on tidal ground and dunes;
  - light L from today's canopy;
  - a tree line from about 560 m.
- **40 kinds** in three layers. Indicator values are approximately Hill et al. (1999) for Britain, from memory: they must be checked
  against the published table before anything is built. Each kind also has a competitive weight, a grazing tolerance and a fire
  tolerance.
- **Allocation:** within a layer, shares are `(C × suitability × use factors)^3`, normalised with bare ground.
- **The test:** read the generator's label back from the dominant kinds.

| | Agreement | Read |
|---|---|---|
| Settled land (grazed, mown, burnt where the generator says) | **69%** (54 worlds) | saltmarsh, bog, rock 100%; reedbed 90%; chalk grassland 90%; moor 88%; beech 88%; birch-and-pine 95%; grassland 75% |
| Natural land (no use) | **64%** | oak-ash 61%; most disagreements below |

Disagreements, and which side is right:

| Generator says | Niche model says | Who is right |
|---|---|---|
| natural **fen** | alder carr (81%) | **the model.** Open fen persists only where wettest or cut: Wicken Fen went to carr when cutting stopped. |
| natural **moor** below about 500 m | birch, pine, upland oak | **the model.** British moors below the tree line are cultural: clearance, grazing and burning. |
| **lowland heath** (settled) | acid grassland (62%) or heather (27%) | **a real knife-edge:** the boundary moves with grazing pressure. Treat it as a management lever, not an error. |
| **hay meadow** | rich grassland (47%) | the model gives meadow only where mowing is applied; the generator labels by place |
| **oak-ash wood** | beech (18%), carr (16%) | real variety: beech on drier soils, wet woods in hollows |
| **dune grassland** | grassland | marram needs mobile sand, which is not modelled |

**Within-label variety.** Each label hides several real communities:
- Grassland: 73% rich grasses, 16% rushes (wet hollows), 4% reed.
- Oak-ash wood: 56% dog's mercury floor, 34% wild garlic.
- Birch-and-pine wood: 86% bracken floor.
- Mixes (two kinds within 30% of each other): 14% of grassland cells, 38% of oak-ash and wet grassland, 33% of heath. This is the
  "weird mix where one plant dominates" Zach asked about, and it comes from conditions with no extra rule.

### M2. Succession on the year clock (`succession.py`)

- **The state per cell:** canopy, shrubs, field-layer shares, and fertility and moisture offsets that use moves.
- **Each year,** the niche model gives the steady vegetation under this year's use, and the state moves toward it at rates limited
  by:
  - seed: near canopy, plus jays and wind from far;
  - light;
  - browsing, with thorny shrubs sheltering seedlings;
  - fire and scythes, which kill seedlings.
- **Fertility:** dung adds, hay and crops take. Its equilibrium is about +2.5 × grazing.

Calibration against real timescales (fitted rates: recruit 0.025, seed from far 0.04, canopy closing 0.05, shrubs 0.12):

| Case | Real | Model | |
|---|---|---|---|
| Abandoned field, base-rich, wood beside it (Broadbalk wilderness) | wood in 25 to 40 years | **26** | ✓ |
| Abandoned field, acid, no wood near (Geescroft) | mostly grass at 30; wood at 60 to 80 | 19% canopy at 30; wood at **46** | too fast |
| Lowland heath, grazing and burning stop | birch in 10 to 15 years; wood in 20 to 40 | gorse and scrub first, birch from **21**, wood at **43** | slow, right order |
| Chalk grassland, grazing stops (after myxomatosis) | hawthorn scrub in 10 to 20 years | scrub at **7**, beech wood at 45 | slightly fast |
| Fen, cutting stops (Wicken) | carr in 20 to 40 years | reed, then sallow scrub, then carr at **45** | slightly slow |
| Wood pasture with no recruitment | thins over a century or more | canopy below 50% at **104** years | ✓ |
| Felled wood regrowing, deer a km² 0 / 3 / 6 / 10 / 15 | regeneration fails above about 5 to 10 | wood at 44 / 51 / 71 / never / never | ✓ |

**What this means for the simulation:**
- An engine year is 24 to 40 days, so every one of these transitions takes 300 to 1,800 days.
- No LLM run (6 to 48 days) will see succession happen.
- Within a run you see only:
  - the start state, which is history as the generator wrote it;
  - fast components: a hay meadow unmown for a season is rank and worth less; nettles come up on enriched ground in a year;
    bracken creeps.
- Succession pays where the generator spins up history, and in cheap long runs (a decade is 320 days).

### M3. Animals on 1 km patches (`populations.py`)

- **Kinds:**
  - red deer: r 0.25 a year, food-limited at 12 a km² of wood;
  - boar: mast-driven; +0.9 in a mast year, +0.25 normal, −0.35 in a bust; up to 6 a km² of oak and beech wood;
  - hares;
  - wolves: Holling II, up to 25 deer-equivalents a wolf a year, half at 4 a km²; a numerical response; at most 3 a 100 km² far
    from villages; switching to stock when short.
- **The wood** loses old trees at 0.8% a year. They are replaced only where browsing lets a few saplings through: about 10 deer a
  km² stops it, and 30% survival is enough to refill gaps.
- **People** hunt within 8 km: light, regulated or open-access (effort follows profit).
- **The run:** the settled-lowland-and-frontier world (2,428 km², 1,878 km² of wood), 100 years.

| Experiment | Deer a km² of wood | Wolves | Wood after 100 years | Stock killed by wolves a year | People's deer a year |
|---|---|---|---|---|---|
| X1 wolves, light hunting | 9.0 | 51 | −6% | 3 | 126 |
| X2 wolves killed off (bounty from year 10) | 11.1 | 0 | −18% | 0 | 144 |
| X2b no wolves, no hunting | 11.6 | 0 | −20% | 0 | 0 |
| X3 half the big wood felled in years 30 to 34 | 8.3 in years 41 to 50 | 47 | regrows to −10% | **18 in years 41 to 50 (3 to 5 before)** | 85 |
| X4 open-access hunting | **0.7 near villages, 9.1 far** | 50 | −4% | 7 to 9 | 107 to 138 |
| X4b regulated | 7.9 near, 9.2 far | 51 | −6% | 3 | 103 to 110 |

**Sensitivity** (`m3_sens.py`, 72 combinations):
- Whether the woods hold depends on deer food capacity against the browsing threshold. Wolves shift the deer by 2 to 3 a km².
- The woods are stable at K 9; they lose 10 to 20% at K 12 and 13 to 32% at K 15.
- The cascade is a lever with a threshold near natural deer densities. Small changes in hunting or wolves tip it either way, but
  only over decades.

**M3b: what a run sees** (`m3b_inrun.py`). A village wood holds about 9 deer, taken at 0.05 to 0.2 a day for 64 days (2 years):

| Rule | Take 0.2 a day: stock at day 64 | Deer taken |
|---|---|---|
| Engine now (threshold, r 0.25 a night) | 0.83 K | 11.7 |
| r 0.25 a year, no movement | **0.30 K** | 7.3 |
| r 0.25 a year, mixing with land 20× its size at 2 a year | 0.75 K | 10.2 |
| ... mixing at 6 a year | 0.88 K | 11.6 |

So the engine now behaves like a wood in a large, well-connected forest, everywhere. On the year clock, an isolated copse is hunted
out within a run and a wood joined to a large forest is not. **This is the case for living_populations step 1:** depletion and
refill become real and depend on the land. Without it, a year-clock rate would simply make hunting useless.

### M4. The wild year, by season, from real yields (`seasonal.py`)

**Yields:** real person-days a hectare of each source's cover a year, after animals' share and what people reach:
- hazel 63;
- acorns and mast 40 (after leaching);
- brambles 24;
- bilberries 12;
- hedge fruit 12;
- roots 1;
- fungi 2;
- greens capped at 10% of need (health, not calories);
- game 0.15 to 0.6 a hectare of wood (from M3);
- trout 25 a hectare of water, eels 30, fowl 3, shellfish 50.

**Reach:** a 12-person village, the land within 2.5 km, fields excluded. Shares are of the village's need, so the engine's time
compression cancels.

| Villages (144, by landscape system) | Spring | Summer | Autumn | Winter | Year | That keeps | Engine now |
|---|---|---|---|---|---|---|---|
| River country (121) | 0.55 | 0.88 | 1.87 | **0.26** | 0.92 | 0.32 | **4.0, flat** |
| Scarp and vale (8) | 0.57 | 0.68 | 1.73 | 0.22 | 0.79 | 0.25 | 4.0 |
| Upland, in its valleys (2) | 0.55 | 0.68 | 1.66 | 0.24 | 0.78 | 0.28 | 4.0 |
| Fen (7) | 2.47 | 5.24 | 11.8 | **3.99** | 5.87 | 4.29 | 5.0 |
| Wildwood (5) | **0.36** | 6.72 | **73** | 3.55 | 21 | 16.8 | 4.8 |
| Coast (1) | 0.59 | 0.72 | 6.14 | 0.77 | 2.06 | 1.32 | 2.3 |

**What it shows:**
- **Farm country** has a real lean season (winter and spring, a quarter to a half of need). Wild food is a supplement there.
- **Fens are rich in exactly the lean season** (fowl, smoked eels): natural exporters.
- **Wooded land is a feast in autumn and famine in spring.** Everything turns on storing nuts and mast, and on the knack of
  leaching acorns.
- **The engine gives every village about 4× its need, flat across seasons and places.** It removes all of this.
- **A caveat on the engine's generosity:** generated villages are about 12 people on land that fed 100 to 200 in reality. Even real
  yields over-supply rich places, so the binding must come from seasons, storage, labour and rights, not annual totals.

### M5. Goods and dependence between villages (`trade.py`)

**The method:** per village, a 4 km reach; 23 goods (8 that every village needs, 15 specialties); a village "has" a good when its
land covers its own use.

| | Goods in a region | Specialties (a third of villages or fewer) | Dependence links (lacks a need, a neighbour has it) | Unmet in the region |
|---|---|---|---|---|
| Engine goods now (by cover) | 5 | 1 | 3 | — |
| Proposal (kinds and conditions) | 16 | 2 | 5 | 4 |

- **Needs most often lacked:** salt 96%, hay 62%, firewood 48%, timber 40%.
- **Specialties most often:** pannage, venison, oak bark, lime, hay, fowl and down, nuts, furze.
- **Rejected:** "more kinds means more dependence". Most new goods are common to every village (thatch, rods, grazing), so they
  enrich the economy without making anyone need anyone.
- **Supported:** a few scarce needs, plus seasonal surpluses that keep, create the links.
- **A generator finding:** sites are scored the same way everywhere, so 84% of villages sit in river country, and an upland or fen
  world's distinctive land lies beyond the villages' reach.
- **Caveat:** the generator's parcels give villages woods the cell map does not show (`natural_forest`), so the firewood and
  timber shortfalls here are overstated.

### M6. The engine's own rules (`engine_flows.py`, `m6_periodic.py`)

- **Best steady take a unit of capacity a year** (32-day year):
  - plants 2.07 (fast, r 0.3 a night);
  - game 1.59 (threshold, r 0.25);
  - grass 2.19.
- **Against reality:**
  - Fields (48 net food a plot-year) and pasture (2 head a unit) are close to real medieval yields.
  - Wild food is 2 to 4× real potential, and flat.
  - Game is about 25× a real deer population's flow, because its r is a real rate a year applied every night.
- **The periodic rule as a seasonal wild year:**
  - resident K 0.15, a run to 2.2 in summer and autumn;
  - take by season: spring 0.04, summer 0.55, autumn 0.84, winter 0.81. The winter figure is the autumn run leaving slowly; a
    faster `run_r` sharpens it;
  - flat now: 0.43, 0.56, 0.61, 0.47;
  - the same year's take (2.24 against 2.07).

### M7. Interactions through the economy (`m7_drain.py`)

Each run uses M2 on an 8 km window around a village, then reads M4 and M5:

| Change (20 to 30 years) | Land | Wild food: spring / winter (× need) | Goods that changed (× own use) |
|---|---|---|---|
| **Drain the fen** (fen with islands) | fen 40% → 5%; wet grassland and reedbed gone; grassland 23% → 86% | 4.9 / 7.9 → **1.3 / 1.2** | grazing 31 → 69; eels 588 → 48; fowl 192 → 12; rushes 733 → 28; peat 375 → 139; hay 15 → 5 |
| **Heath management lapses** (sand country) | heath gone; scrub 0 → 21% | 1.9 / 2.0 → 1.6 / 2.1 | furze 35 → 139; grazing 84 → 59; wattle rods, nuts and oak bark up |
| **Village abandoned** (plain) | grassland 81% → scrub 95% | 2.2 / 2.1 → 1.0 / 4.4 | grazing 94 → 25; wattle rods 56 → 660; nuts 1 → 101; eels and fowl down |

The "× own use" figures depend on arbitrary needs a village; the direction and size of the change is what matters.

## 4. The design: five layers, four clocks, one rule each

### 4a. The layers

| Layer | State | Moved by | Clock | Built today |
|---|---|---|---|---|
| **1. Ground** | height, water, soil texture, depth (the generator) | almost nothing; draining and damming move moisture | generations | yes (physical.py) |
| **2. Conditions** | moisture, reaction, nitrogen, salt, light (Ellenberg scales) on each parcel | dung, hay and crops, burning, drains, dams, ruins; canopy for light | years | no: M1's mapping is the proposal |
| **3. Vegetation** | canopy, shrubs, field-layer shares (kinds), and the cover the engine sees | niche allocation (M1), with succession toward it (M2) | years to decades | covers and woods only |
| **4. Populations** | stocks and wild kinds: density or whole groups, with diet and movement | growth, eating, movement, people's take | days to years | stocks only |
| **5. Uses and rights** | grazing, mowing, cutting, burning, felling, draining, hunting; who may | people's acts and law | days | acts and claims, yes |

**One rule each:**
- Layer 2 is a sum of pressures with decay.
- Layer 3 is soft dominance plus rates.
- Layer 4 is grow, eat, move, take (living_populations §2d).
- Layer 5 is techniques and claims.

Nothing is per-kind code. A kind is a row: indicator values, layer, weight, tolerances, what it gives and when.

### 4b. The four clocks, and what belongs on each

| Clock | Lengths | What lives here | Who sees it |
|---|---|---|---|
| Day | nights | takes, spoilage, movement within a range, a run's arrival, a wolf's visit | every run |
| Season | 6 to 10 days | the wild calendar (M4), sowing and harvest, fish runs and fowl flocks, the lean season | every run of a year |
| Year | 24 to 40 days | mast and berry years (a draw per kind per year), boar booms, births, hay stocks, coppice regrowth | runs of 1 to 2 years: once or twice |
| Decades | hundreds of days | succession, the wolf-deer-wood cascade, beaver ponds, wood pasture fading, bracken spreading | cheap long runs, and the generator's history |

**The rule:** put each piece of richness where a run will see it. Seasons and years first. Decades go in the generator (as start
state) and in long cheap runs.

### 4c. The interactions (loops), each with its evidence

| # | Loop | Real basis | Goals | Clock | Evidence here | Mechanism |
|---|---|---|---|---|---|---|
| L1 | **Grazing holds grassland**: stopping lets scrub in; dung raises fertility; heavy grazing turns heath to acid grass | downland, commons | G3, G5 | years to decades | M2 E4; M1 heath knife-edge | use pressures (layer 5 → 2, 3) |
| L2 | **The fold moves fertility**: sheep graze the down by day and are folded on the arable by night (the sheep-corn system) | Wessex chalk | G1, G6 | years | M2's dung balance (chalk N stays low only if dung leaves) | dung as a stock that moves with the herd (built: dung accrues where beasts stand) |
| L3 | **Hay is the winter's limit**: floodplain meadow is scarce, so it limits how many beasts survive winter and is worth 2 to 3× arable | Domesday meadow values | **G1**, G4 | seasons, years | M5: 62% of villages lack enough hay | hay as a good from meadow parcels (built: the "hay" technique) plus winter feeding |
| L4 | **Mast, boar, crops**: a mast year booms the boar; the next bust year sends them into the fields | European boar damage records | G3, G5 | years | M3: damage peaks in bust years | a yearly draw per kind (new, small) |
| L5 | **Wolves, deer, wood**: wolves hold deer down and let woods regenerate; killing wolves raises deer and the woods slowly fail | Białowieża; the deer-threshold literature | G3, G5 | decades | M3 X1, X2; sensitivity | diet, plus browsing as a pressure on layer 3 |
| L6 | **Felling, then wolves at the village**: losing wood cuts wild prey and wolves switch to stock | Zach's example | **G5**, G1 | years | M3 X3: ×4 to 5 for a decade | diet with a second choice (living_populations §2b) |
| L7 | **Hunting halos and refuges**: open access empties the near woods; refuges keep the catch; rights decide who may take | forest law, poaching | **G1**, G5 | days to years | M3 X4; M3b | living_populations step 1 plus claims (D2-194) |
| L8 | **The fen's water level**: reed, sedge, eels and fowl against drained grazing | the 17th-century Fens | **G1**, **G5**, G6 | years | M7 drain | moisture as a condition that drains move; goods from kinds |
| L9 | **Heath kept by use**: grazing, burning and cutting bracken (litter) and gorse (oven fuel) hold heath; stop and scrub, bracken and birch come | lowland heath history | G3, G6 | years to decades | M7 heath; M2 E3 | cut pressures per kind (the "cut_" uses) |
| L10 | **Coppice, browse, hurdles**: coppice regrowth feeds deer; deer stop regrowth unless fenced; the fence is hurdles woven from the coppice's own rods | coppice history | G6, G3 | years | M2 E7 (deer thresholds) | fences (built) plus withies (husbandry) plus browsing |
| L11 | **The seasonal pulse and the store**: autumn gives several times need, spring a fraction; storing, guarding, theft and rationing follow | foraging ecology (the lean season binds, not the annual total) | **G1**, **G4**, G2 | seasons | M4; M6b | the periodic rule (built) plus spoilage (built) |
| L12 | **Abandonment reads in the land**: nettles and elder on old house sites, scrub on old fields; people read history from plants | archaeology (phosphate, nettles) | G2 | years to generations | M7 abandoned; M2 dung | fertility offsets that last; signs |
| L13 | **The river is shared**: a weir or heavy take downstream starves the run upstream | weirs and fish rights | G5 | seasons | (water_and_preservation; not modelled here) | living_populations step 2 |
| L14 | **Fuel substitutes**: where wood is short, peat (turbary), furze or dung; each with its own land and right | upland and fen fuel | G1, G6 | years | M5: wood lacked by 40 to 48% | goods from kinds plus common rights |
| L15 | **Bees follow flowers**: honey's yield and taste follow heather, lime and clover; wax for seals and candles | medieval honey and wax | G6 | seasons | (not modelled) | a kind with a diet over field-layer kinds |
| L16 | **Rats follow stores**: big stores breed rats and lose more; cats and staddle stones answer | stored-grain losses | G4, G6 | seasons | (not modelled) | a pest as a population with a diet of stores |

**Which loops reach each goal:**
- G1 (dependence): L3, L7, L8, L11, L14. These are the ones to build first for the society.
- G2 (observability): L11, L12, and the signs of every population.
- G3 (trajectory): L1, L4, L5, L9, L10.
- G5 (commons): L5 to L8, L13.

### 4d. The key ecosystems, as complexes

What each landscape system gives, lacks and fights over (M1 composition, M4 calendar, M5 goods, M7 tensions):

| System | Vegetation (M1) | Wild year (M4) | Gives others | Lacks | Tension |
|---|---|---|---|---|---|
| **River country** (most villages) | rich grassland, rushy hollows, oak-ash and wet woods, scarce floodplain meadow | lean winter and spring; a supplement | grain, hay where it has meadow, timber | salt, often hay and wood | meadow and wood rights; boar in the crops |
| **Fen** | reed, sedge, meadowsweet; carr at the edges | **rich all year, best in the lean season** | smoked eels, fowl and down, reed thatch, peat, rushes | timber, firewood, grain | **draining** (L8): grazing against fowling, eels and reed |
| **Wildwood frontier** | oak, beech, hazel under them; wild garlic and bluebell floors | feast in autumn, famine in spring | venison, nuts, pannage, bark, honey and wax, timber | grain, grazing, salt | wolves (L5, L6); clearing; who owns the forest |
| **Sand country and heath** | heather against acid grass (knife-edge); gorse, bracken, birch and pine | lean | furze, bracken litter, rabbits (when warrens exist) | hay, fertility | burning and cutting rights; bracken creep |
| **Scarp and vale** | chalk turf, beech hangers, clay vale grassland | lean | sheep's dung (the fold), lime, flint | wood on the down, water on the top | the fold (L2); scrub when grazing stops |
| **Upland and moor** | heather moor, blanket bog, hill pasture, upland oak in the valleys | lean | wool, peat, hill grazing | grain, hay | burning; overgrazing to grass; peat cutting |
| **Coast and estuary** | saltmarsh, dunes | shellfish in spring, fowl in winter | **salt**, shellfish, samphire | timber, sometimes grain | salt pans; the shore's rights |

## 5. The terrains and ecosystems: what to add or shift

1. **Split the settled layer's "grassland" (about 60% of land in most worlds) by use, not by plant.** These would be ecosystem labels
   in data; covers stay as they are.
   - **Open field** (arable in strips, with fallow grazing).
   - **Common pasture.**
   - **Hay meadow,** floodplain only. It is less than 1% of land now; keep it scarce, since that scarcity is L3's lever.
   - **Wood pasture:** pollards over grazing, the forests and parks. Missing today, and the most typical medieval habitat.
   - **Waste:** scrub, bracken, gorse.
   - **Hedges** as a parcel attribute: hedge fruit, rods, birds.
   - **Old settlement ground:** nettles, elder.
2. **Correct the natural layer where M1 shows it wrong:**
   - fen drier than about F 10 is carr unless cut;
   - moor below about 450 to 500 m is wood unless grazed and burnt.
   - That makes the generator's open fen and moor *held open by history*. They need management to persist, which is L1 and L9's
     lever.
3. **Water ecosystems** as stock records on water parcels (D4-104 already allows it):
   - chalk stream (trout);
   - lowland river (eels, coarse fish);
   - large river to the sea (salmon run);
   - mere;
   - estuary mudflat (shellfish, fowl).
4. **Site choice:** let a world spread its villages across systems (a pin, or a diversity term in site_score), so a fen or upland
   world's villages differ (M5's 84% river country).
5. **Equilibrium at day 0:** a generated land must be stable under its assumed use. M3's first version drifted at day 0, because the
   map's woods were not an equilibrium of its deer. The check: run the stocks 1 to 3 years with no people and with the assumed use,
   and confirm no drift beyond a threshold. That is the same kind of check as landgen's existing `landscape_checks`.
6. **No new biomes:** none of this needs to leave the temperate envelope (D2-191).

## 6. Calibration: the numbers

### 6a. Wild food (engine units are a share of need, so it carries to any year length)

| Stock | Now | Proposed (first values) | Source |
|---|---|---|---|
| plants (forage) | K 0.5 to 1.3 a unit, fast, r 0.3 a night; about 4× need, flat | by kind (M4's table), seasonal via `periodic` (resident K about 0.15 of today's, a run in its seasons), year draws for nuts, mast and berries | foraging and agronomy yields (§M4; approximate) |
| game | K 0.5 to 5 a unit, r 0.25 a night (threshold) | r on the year clock (deer 0.25, boar by mast, hares 1.0) **with movement from neighbours** (living_populations step 1); no threshold where there is immigration | M3, M3b |
| fish | periodic (built) | by water ecosystem (§5.3) | water_and_preservation |

**Order:**
1. Seasons first. They are data only.
2. Then game on the year clock, but only together with step 1. Alone it makes hunting pointless (M3b).
3. Then the per-ecosystem yields that differentiate villages.

### 6b. Plants and succession (generator, then the year clock)

M1's mapping and kind values (`niche.py`), and M2's rates (`succession.py`). Two weak spots to recalibrate:
- **Seed limitation:** Geescroft closes too fast.
- **Heath versus acid grass:** a knife-edge on grazing; set it deliberately.

### 6c. An engine subtlety to fix or work around (for 37.4, once Zach agrees)

- **The problem:** under `periodic`, the gather yield is `base × (S/K)^b` with K the resident capacity. During a run S ≫ K, so a
  unit of work takes many times its normal yield. My first seasonal arm fed 3.5× the people of the flat arm for the same year.
  For a fish run this is intended (fish crowd), but it should be bounded.
- **Two options:**
  - measure density against `max(K, run_K)` in season;
  - cap `S/K` at a ceiling a stock's record may set.
- **The probe below is tuned around it** (resident K 0.15, run 0.66 of today's K), so it needs no engine change.

### 6d. The animal web (M3; first values)

| Parameter | Value | Range tried | Sensitivity |
|---|---|---|---|
| deer food capacity a km² of wood | 12 | 9 to 15 | **high:** sets whether woods hold |
| browsing that stops regeneration | 10 deer a km² | 6 to 12 | **high** |
| wolf half-saturation | 4 deer a km² | 2 to 6 | medium: deer 8.0 to 9.6 |
| wolf ceiling | 3 a 100 km² | — | sets wolves at about 50 in a frontier window |
| boar r by mast | +0.9 / +0.25 / −0.35 | — | drives damage cycles |
| mast frequency | 1 year in 4 | — | data per wood type (oak 2 to 4 years, beech 5 to 10) |

## 7. Hypotheses, and what happened to them

| # | Hypothesis | Result |
|---|---|---|
| H1 | Plant kinds placed by conditions reproduce the generator's labels and add variety within them | **supported:** 69% / 64%; mixes 14 to 38% |
| H2 | About 8 rates reproduce real succession timescales | **mostly:** 5 of 7 within or near target; seed limitation too weak |
| H3 | Succession matters within LLM runs | **rejected:** 300 to 1,800 days; only its fast parts do |
| H4 | Wolves, deer and woods form a cascade that matters | **supported at decades,** modest: deer −25%, woods −6% against −20% a century; threshold-sensitive |
| H5 | Felling raises wolf attacks on stock | **supported:** ×4 to 5 for a decade |
| H6 | Open-access hunting empties the woods | **supported locally** (a halo); the regional catch holds by spillover |
| H7 | A seasonal wild year makes storage matter; the engine is flat | **supported:** lean seasons at 0.25 to 0.55× against autumn at 1.8× (farm) to 73× (wildwood); data only via `periodic` |
| H8 | Ecological variety makes villages depend on each other | **partly:** goods ×3, dependence links +2; dependence comes from scarce needs and seasonal surpluses |
| H9 | The engine's wild food is far too generous | **partly:** forage 2 to 4× (and flat, the bigger problem); game about 25× (the clock) |
| H10 | Management changes make winners and losers | **supported:** fen drainage, heath lapse, abandonment (M7) |

## 8. What to build, in order, and what not to

| Rank | What | Goals | Cost | Why now |
|---|---|---|---|---|
| 1 | **Seasonal wild year, by kind and ecosystem** (data: periodic stocks, real yields, a yearly draw for mast, nuts and berries) | G1, G2, G4, G6 | S (data; the yearly draw is a small mechanism; §6c's cap) | the biggest effect found, and visible in every run |
| 2 | **Scarce needs that make links:** hay through winter, salt for keeping, fuel substitutes (peat, furze) | G1, G6 | S-M (goods, techniques; husbandry) | M5: dependence comes from these |
| 3 | **living_populations step 1** (graph movement, immigration) with game on the year clock | G2, G3, G5 | M (37.4's) | M3b: makes depletion and refuges real; needed before game's clock is fixed |
| 4 | **Conditions and kinds in the generator** (M1), splitting "grassland" by use, wood pasture, hedges, water ecosystems; site diversity; the equilibrium check | G1, G2, G6 | M (generator, mine) | variety, patches as lore, and the land villages differ by |
| 5 | **Use pressures that hold vegetation** (grazing, mowing, cutting, burning, draining) as yearly parcel state, with the generator spinning up history | G3, G5 | M | long runs; L1, L8, L9 |
| 6 | **Mast and boar** (L4) | G3, G5 | S, given 1 and 3 | a yearly cycle a 2-year run sees |
| 7 | **Wolves, deer, wood** (L5, L6) | G3, G5 | M, given 3 | decades, except L6's switching, which a run can see after a felling |

**Not worth it:**
- competition dynamics between plant species (the allocation is enough);
- seed dispersal maps;
- soil formation;
- food webs deeper than plants, eaters and predators;
- succession inside LLM runs.

None ends in leverage within affordable runs.

## 9. The LLM probe (prepared, not run)

**What it asks:** does a hungry gap change what people do? It is the cheapest test of rank 1.

- **The world:** Ferrybank (the water acceptance world, D4-103), without the water pack. The field is enlarged so worked land feeds
  them (1.67×); a 16-unit copse and a scrub parcel are added; 28 days from late summer, in seasons of 7.
- **The two arms differ only in the wild food's timing:**
  - flat (`fast`, today's K);
  - seasonal (`periodic`: resident 0.15 of K, a run of 0.66 of K in summer and autumn).
- **Checked with the engine's own capacity model:** wild food feeds 1.67 against 1.85 people (0.21× against 0.23×); worked land
  1.67× against 1.83×.
- **Bots:** both arms run 28 days with no engine errors. The bots starve, as in 02zn, so this checks only that the world runs.
- **What to read:** food stored before winter; wild food gathered by season; hunger in spring; food given or traded; the share of
  actions on food (≤ 30%); the end-state reading against the flat arm.
- **Cost:**
  - cast: 2 Opus, 3 Sonnet, 3 Haiku;
  - per agent-day, from 38.21's figures × 1.35: about $0.135 Opus, $0.04 Sonnet, $0.004 Haiku;
  - about $0.40 a day, so **about $11 a run**;
  - two arms on one seed: **about $23**; two seeds each: **about $45**.
- **Blocked on:** this container has no Anthropic API key. Running it needs Zach's approval of the spend and a key given through the
  environment's credentials.
- **Files:** `02zp_ecosystem_models/probe/`.

## 10. Decisions for Zach

1. **Calibration first:** recalibrate wild food to real per-hectare yields with seasons (data only, via `periodic`), before adding
   kinds?
2. **Game on the year clock,** only together with living_populations step 1 (movement and immigration)?
3. **Scarce needs as the source of dependence:** hay through winter, salt for keeping, peat and furze as fuel. Which first?
4. **Generator:** place plants by conditions (M1); split the settled grassland by use; add wood pasture, hedges and water
   ecosystems; spread villages across systems; check day-0 equilibrium?
5. **Succession** only in the generator's history and in long cheap runs, not as an in-run mechanism?
6. **The probe:** run it (about $23, or $45 with two seeds), once a key is available?
7. **§6c,** the periodic rule's density response: raise it with 37.4 (when board posting resumes)?

## Limits of this analysis

- **Indicator values and yields are from memory and the general literature, approximate.** The Ellenberg values must be checked
  against Hill et al. (1999), and the yields against sources, before anything is built.
- **M3 is annual and uses 1 km patches.** It has no roe deer, no seasons within a year, and no individual packs. M3b covers the
  in-run question separately.
- **M4 and M5 read the cell map,** not the generator's parcels, which add village woods. "Has" thresholds in M5 and the "× own use"
  figures in M7 depend on assumed needs.
- **The probe's world inherits the water world's people and stores;** it is a small-world test, not a scenario.

## Sources

- Engine: data.py (RESOURCES, PHYSICS, TECHNIQUES, FORESTS), renewal.py, night.regrow, capacity/, clocks.py; landgen physical.py,
  ecology.py, vocab.py, settle.py, write.py.
- Proposals: living_populations.md, wildlife.md, wild_plants.md, husbandry.md, water_and_preservation.md, ecosystems.md,
  environment_state.md, forests.md, carrying_capacity.md; docs/scenario_design.md.
- Ecology, approximate and from memory, to be checked:
  - Hill, Mountford, Roy and Bunce (1999), Ellenberg's indicator values for British plants;
  - Grime's CSR strategies;
  - Rothamsted's Broadbalk and Geescroft wildernesses;
  - Wicken Fen's history;
  - downland after myxomatosis (1954);
  - deer-density thresholds for regeneration (Scottish pinewood and lowland woodland guidance);
  - Jędrzejewski et al. on Białowieża's wolves and red deer;
  - Vera (2000) on wood pasture;
  - Rackham on woodland history and Domesday meadow values.

---

# Part two (8 Nov, later): wildlife and plant webs designed by iteration

Zach's brief:
- explore different webs of animals and plants, and see which work well, which are too fragile or not worth it, and which give
  interesting behaviour;
- expand the first ideas, test them, cut them down;
- treat fixing the land generator as part of the loop;
- test on normal and deliberately extreme worlds.

Part one had modelled only four animals and designed no webs. This part does that work. Models, results and logs are in
`02zp_ecosystem_models/web/`. The generator work is on the branch `climate-calibration` (b4fb26c, 5ef36fe), as Zach asked, so it
can be compared with 37.4's version.

## 10. The loop, round by round

| Round | Tried | What broke | What it taught |
|---|---|---|---|
| 0 | 40 candidates in one web (W), every kind's intake fitted to a real density | about half died out whatever their food | generalist predators eat rare prey out unless prey get harder to find as they thin (a refuge); small mammals need several broods a year |
| 1 | a core of 15 | roe drove red deer out (both set as browsers); boar held badgers down 12× | each kind needs a food or place it is best at; territorial kinds (grouse, beaver) show up as intakes fitted 30 to 60× too high |
| 1b | a soft self-limit on every kind; weather | without weather, populations barely moved | weather years and hard winters are what make populations vary |
| 2 | each candidate group added to the core | aurochs, bison, horse, bear, fallow and bustard died out; small predators unsettled each other | (wrongly) "cut the slow breeders"; Zach: this is the model's weakness, not the animals' |
| 3 | the refined list | red deer at 4% of target; rabbits grazed their sward; one grass for every grazer | grazers divide the sward: short turf (hares, rabbits, geese) against coarse grass (deer) |
| W2 | rebuilt as consumers and resources | first aurochs dominated; then deer stalled at 97% of need | food as a standing crop; intake from body mass (Kleiber, nothing fitted per kind); fine and coarse food by body size (Jarman-Bell); reserves and hibernation; foraging for energy; need measured against ordinary 0.6-digestible forage, not 0.8 (my error) |
| W2 calibration | one number per food, fitted against every eater | diverged; kinds that had died out had no say | calibrate one food against one well-known anchor (grass to red deer, sward to hare, browse to roe, heather to mountain hare, mast to boar, nuts to squirrel, seeds to voles, wetland plants to water vole, fish to eel) |
| W2 levels | no stabilisers | red deer 36×, boar 22× | the standard stabilisers: disease and parasites with crowding (crowding measured by Damuth's body-size law), interference among predators, prey refuges, softer choice rules |
| Round 4 | stabilisers as first set | frozen: no variation, nothing moved anything | stabilisers set too strong and too low make the crowding ceiling do all the work (over-correction) |
| Sweep | weaker crowding, disease outbreaks, 37.4's climate | the stand-in weather gave 16% swings in small mammals | the climate brings deer and boar to 15% (real 10 to 30%) and small mammals to 25%; patch-level outbreaks average out |
| Growth check | each kind's maximum growth against real | bears 33×; eagles, cranes, ravens, beaver grew 2 to 5× too fast | Zach: "wouldn't bears also just not have that many children?" Breeding set so each kind's maximum growth is real; bears get a spacing ceiling |
| Final | the last pass (colonies, leks, store-bounded rats, flocking pigeons) | woodpigeons collapsed after their change | see §13 |

## 11. Rules for a food web that come out of it

1. **Food is a stock, not a slice.** It grows and is eaten down; shortage comes from grazing against growth and from the winter.
2. **Intake comes from the body (Kleiber), not from fitting.** Calibrate what is truly uncertain (how much food grows and can be
   reached) once per food, against one well-known eater.
3. **Coexistence comes from mechanisms, not hand-separated diets:**
   - fine and coarse food by body size;
   - each kind limiting itself (territory, disease);
   - predators that switch to what is common, with refuges for the rare;
   - weather that favours different foods in different years.
4. **Breeding must match real maximum growth.** Long-lived kinds are the ones that go wrong; check every kind.
5. **Reserves and hibernation** decide who survives a lean season, so breeding follows condition, not that season's food.
6. **Stabilisers are needed but easy to overdo.** Too strong, and every kind sits frozen under its own ceiling and nothing affects
   anything. Calibrate the dynamics (year-to-year swings, responses to removals and introductions), not only the levels.
7. **Variation comes from episodes:** hard winters, snow over the forage, disease outbreaks, mast years. Smooth rules never give it.
8. **Fragility comes in two kinds:**
   - fragile to our guesses: a ±25% change in numbers nobody can measure decides survival. That is a fault.
   - fragile to pressure in the world: overhunting or draining wipes the kind out. That is the point; crane and beaver are the
     examples.
9. **Displacement is an outcome,** not an error, when the world or people cause it (rabbits brought in, megafauna in a wildwood).
10. **Resolution by kind:** regional averages of common kinds do not depend on patch size (450 m to 2.25 km gave the same), but
    edges, depletion near villages and rare patchy kinds do. Small kinds belong on parcels, deer and boar on about 1 km, wolves,
    lynx, bears and eagles as regional groups or individuals.
11. **A world should normally start at its ecology's settled state** (Zach), with named exceptions that give a run a trajectory:
    wolves gone a generation ago, land abandoned after a plague.

## 12. The model as it stands (W2)

- **Foods:**
  - standing stocks: coarse grass, sward, browse, heather, wetland plants (the bulk ones split into fine and coarse), roots, soil
    animals, fish, sea fish;
  - pulses in their seasons that rot: mast, nuts, fruit, seeds, cones;
  - people's foods: crops, beasts, stores;
  - carrion from deaths and kills.
- **Kinds:** 42 rows (mass, diet class, breeding, deaths, habitat, diet, limits, territory, uses, damage). Nothing fitted per kind.
- **The season's rule:**
  1. foods grow by the weather;
  2. animals ask for what their bodies need (more when lean), taking the food worth most to them in proportion to what stands;
  3. reserves fill or drain;
  4. death rises with hunger, crowding and outbreaks; breeding follows condition;
  5. animals move toward better ground;
  6. migrants come and go.
- **Weather:** 37.4's climate (D4-109) through a bridge (`climate_bridge.py`). Season means of temperature, wet days, frost and
  snow become:
  - growth by food (drought cuts grass hardest);
  - snow cover over the winter forage;
  - mast odds from the previous summer.
- **Calibration:** nine food scales against nine anchors, in the steady era, on reference worlds. Everything else emerges.

## 13. The designed ecosystems: the kinds and how they came out

Final run: 48 worlds (36 normal, 12 extreme), 70 years, steady era. Density is shown against a real density in good habitat; year
variation is the median coefficient of variation.

| Group | Kind | Density × real | Year variation | Limited by | Status |
|---|---|---|---|---|---|
| Deer and boar | red deer | 1.15 | 15% | coarse grass and heather; wolves a little | **keep** |
| | roe deer | 1.17 | 16% | browse and fruit | **keep** |
| | wild boar | 3.4 | 11% | mast, roots, crops | keep; too high (backlog) |
| Big omnivore | brown bear | 0.93 | 3% | spacing; real slow breeding | **keep** (rare; also as legendary individuals) |
| Small plant-eaters | brown hare | 1.06 | 20% | sward and crops; fox | **keep** |
| | mountain hare | 1.12 | 23% | heather (uplands) | **keep** |
| | voles and mice | 1.6 | 33% | seeds and grass; every small predator | **keep** (the prey base) |
| | water vole | 1.0 | 32% | wetland plants; heron, otter | keep (fragile to herons) |
| | red squirrel | 3.4 | 37% | nuts and cones | keep; too high (backlog) |
| Moor and forest birds | red grouse | 0.67 | 22% | heather; fox | **keep** |
| | black grouse | 0.26 | 17% | moor edge | keep, fragile |
| | capercaillie | 0.86 | 27% | pine, bilberry; fox, lynx | keep, fragile |
| Wetland and coast | wildfowl, grey geese, salmon | 1.0 | migrants | set by arrivals | **keep** |
| | grey heron | 1.4 | 1% | colony sites | **keep** |
| | otter | 0.51 | 8% | fish and eels | **keep** |
| | eel | 0.52 | 12% | soil animals and fish | **keep** |
| | beaver | 0.05 (dies in 58% of its worlds) | — | slow breeding against hunting | keep as **fragile by design**; its default hunting is too high |
| | crane | dies over decades | — | slow breeding against hunting | **fragile by design**, hunted out (as in history) |
| | seabirds, seal | 0.07, 0.26 | — | inshore sea food (thin in the model) | backlog: the sea's food |
| Predators | wolf | 1.08 | ~0 | territory | **keep** |
| | lynx | 0.91 | 2% | territory; roe | **keep** |
| | fox | 0.78 | 12% | voles, hares, grouse | **keep** |
| | wildcat, pine marten, stoat and polecat, buzzard, owls | 0.7 to 1.2 | 5 to 14% | voles | keep one or two; they are redundant on one prey |
| | golden eagle, sea eagle | 1.24, 1.25 | ~0 | territory | **keep** (rare) |
| | raven | 1.38 | 4% | carrion | keep (signs) |
| Around people | rats | 0.93 | 2% | store size | **keep** |
| | woodpigeon | collapsed (0.02) | — | lost to boar on shared seed and mast | backlog: the last change made it worse |
| | badger | 1.84 | 17% | soil animals | keep |
| Era packs | aurochs, bison, elk, wild horse | 1.5, 1.3–1.6, 1.0 (cold), 0.1–0.3 | — | grass and wetland; they push red deer out | a **wildwood era pack**, not a default |
| Introduced packs | rabbit | about 0.13 where brought in | — | sward | a **pack**: displaces hares to 0.4–0.6, grouse to 0.75 |
| | fallow deer | fails to establish | — | red and roe already there | cut as a population; a park beast for husbandry |
| Cut | great bustard | dies | — | needs wider open country than exists | cut |

## 14. How they interact (measured)

| Change | What moved |
|---|---|
| **Rabbits introduced** | brown hare to 0.42–0.59; grouse 0.75; mountain hare 0.57 on the chalk |
| **Fox removed** | capercaillie 1.44 (ground-nesters benefit, as under real predator control). Hares did not respond (backlog: real hares do) |
| **Wolves and lynx removed** | capercaillie fell to 0.27–0.68 and black grouse to 0.6–0.7. More deer take the bilberry and browse they need, a cascade seen in Scottish pinewoods |
| **Wildwood megafauna, no people** | aurochs 1.5×, bison 1.3–1.6×, elk 1.0 (cold); red deer driven out; roe and lynx up |
| **Wildwood megafauna, hunted hard near villages** | barely changed: they live far from the villages. Real extirpation came with settlement spreading, not from hunting at home (and red deer coexisted with aurochs, so their exclusion is a remaining flaw) |
| **Heavy hunting near villages for 15 years, then stop** | near the villages: hares 1–2% of before, beaver 0, otter 8–14%, eel 10–28%, grouse 15–50%, deer 28–53%. Regionally 0.2–0.8. Recovery: most within a year (immigration from refuges), hares 5 years, otter 2–4, **crane 24–26 years** |
| **Eras** (steady, warm, cold, wet, dry, stormy) | little: year variation 11% in every era; a dry era lowers water voles, capercaillie and bears by 15–25% and raises beaver and cranes. The eras' climates differ modestly (dry: wet days 0.30 against 0.39), and the bridge's responses are modest. One to calibrate with 37.4 |

## 15. The land and the climate (on `climate-calibration`)

**What was wrong:**
- Raising the sea drowned nothing: the shapes held every land cell 2 m above it.
- Wetness and moisture were ranked within each world, so no world could be wetter or drier than another.
- The ecosystem labels ignored temperature.
- My first fixes (offsets) were patches. Zach: "these feel like patched over fixes"; they are kept unapplied in
  `generator_interim.patch`.

**Rebuilt (b4fb26c):**
- **Rain** in millimetres (`rain_mm`, 900 a year on the windward lowland), raised on hills by the wind sweep.
- **Moisture and wetness** on fixed bounds measured from the default worlds, plus the climate's water surplus and soil drainage.
- **Sea from elevation:** land is held above a datum, so raising `sea_level` drowns low ground joined to the sea.
- **A tree line set by warmth.**
- **Wet ground anywhere** becomes carr or wet grassland.
- **Laid river channels** fall along their own course (an old bug, hidden by a check that sampled the wrong place).

Default worlds come out much as before. 1,600 mm of rain or a flat wet basin now give real wetland; a 60 m sea drowns 16% of a
plain; a 4 °C world is moor above the tree line.

**The land's fields (5ef36fe; names agreed with 37.4, D4-112, D4-113):**
- each parcel's `land:` {elevation, exposure, texture, held_mm, drain_rate, depth, base_fertility (nutrients only), position,
  rain_factor, sea_km, river, down};
- each node's `xy`, `elevation` and `rain_mm`.

37.4 builds the fast stocks (soil water, snow, river flow, fuel dryness) once Zach confirms with them.

**The climate as calibrated so far:**
- **Seasons:** spring 9 °C, summer 16, autumn 10, winter 2.7; wet days 33 to 51%; winter frost on 62% of nights and snow on 11% of
  days.
- **One issue for Zach** (37.4 has raised it as 38.64 §6.7): totals per engine year (rain, frost-night counts) are about a tenth of
  a real year's, because an engine year is 24 to 40 days. Daily rates and seasonal shares are real, and the ecology reads only
  those.

## 16. Calibration backlog (for when the fast stocks exist)

- **Too high:** boar 3.4× and squirrels 3.4× (mast and nut scales hit their floor, so something other than food holds them).
- **Woodpigeons collapse:** shared seed and mast with boar. They forage over far wider ground than one patch.
- **Hares ignore fox removal;** real hares rise when foxes are controlled.
- **Small mammals** vary 33% against a real 30–70%; vole cycles need a predator lag.
- **Outbreaks** need a regional footprint.
- **Megafauna exclude red deer,** but they coexisted in reality (aurochs on coarse grass and fen, red deer on heather and edges).
- **Beaver's default hunting** is too high for a slow breeder; cranes likewise. Fragile by design, but not lost by default.
- **The sea's food** for seabirds and seals.
- **Eras:** their effect on the ecology is small; calibrate the climate's eras and the bridge's responses together.
- **Crowding by body size** gives omnivores a loose ceiling; keep the spacing limits from biology.

## 17. Decisions for Zach

1. **The kinds list in §13:**
   - a default temperate web of about 30;
   - wildwood megafauna as an era pack;
   - rabbits and fallow deer as introduced packs;
   - bustard cut;
   - crane and beaver kept as fragile by design;
   - bears as rare populations and legendary individuals.
2. **The rules in §11** as the design rules for the live populations (living_populations.md).
3. **Resolution by kind** (§11 rule 10) for the live engine: parcels for small kinds, about 1 km for deer and boar, regional groups
   for the great predators.
4. **The year-length question** (§15), with 37.4.
5. **Next:** the backlog against the fast stocks once built, or the write-up into living_populations.md and wildlife.md as
   proposals.

---

# Part three (8 Nov, later): the node first

Zach: "maybe we should have designed everything first and foremost for the nodes ... you seemed to focus everything on [the land]
without considering how it actually fits into the society." He was right.

**The scale gap.** A generated village holds about 0.55 km², and the society about 0.1% of the window the web modelled. In a
village's 10 ha wood, real densities give under one red deer and 0.002 wolves. The web's regional dynamics play out at a scale and
over decades the society cannot touch.

**A first model at village scale** ([02zp_ecosystem_models/node/](02zp_ecosystem_models/node/)):
- villages from five generated worlds, with their own parcels and their reservoir (the land within 5 km);
- 12 people;
- real yields under one scaling principle: an engine day is 365/Y real days, and a food is 365/Y real person-days;
- three kinds of year and five household choices.

**Findings:**
- **Wild food** is about 7 to 11% of a village's need in all, none of it 10% alone. Nuts are the most, about 11% of autumn's need.
- **Losses are the lever:**
  - boar in the crops about 19% of need, and up to 52% after a mast year near big woods;
  - deer, pigeons and rats about 5% each;
  - together 16 to 38%, and up to 70% in bad years.
- **Guarding** costs about 4% of the village's work and cuts losses about four-fold.
- **The damage figures are first values and probably high.** They still pass the test at a third.

**Proposal:** [proposals/node_ecology.md](../../cybertron2/proposals/node_ecology.md).
- parcel stocks people can change;
- a reservoir per node that sets refill and visitor odds;
- visitors as events with signs;
- people's levers (watch, scare, fence, dogs, cats, fold, hunt where allowed, keep);
- forest rights as the conflict between the lord's game and the villagers' crops;
- the regional web offline;
- a relevance test before anything is built.

# Part four (8 Nov, later): the interface between villages and the land, and the research behind wild_systems.md

Superseded as design by [wild_systems.md](../../cybertron2/proposals/wild_systems.md) (partly accepted: D2-197, D2-198). This part
keeps the experiments and the sources. Models: [02zp_ecosystem_models/iface/](02zp_ecosystem_models/iface/).

## 18. The question

Zach asked two things:
- whether the ecology could keep a proper regional level and only make the villages' footprint and exposure outsized;
- what the best overlap of coarse and fine would be (coarse away from villages, finer near them), and what the system is for in the
  world.

## 19. The experiment

One lean ecology (hares, deer, boar with mast, wolves on deer; real rates; four seasons) on the generator's land, laid on five
structures:

| Structure | Zones | What it is |
|---|---|---|
| S1 grid 1 km | about 2,300 | uniform 1 km blocks |
| S2 grid 1 km, × k | about 2,300 | the same, with the village's take (footprint) and the raids it meets (exposure) multiplied by k = 5, 15, 30 |
| S3 nested | 1,150 to 1,700 | 300 m blocks within 2 km of a village, 1 km to 6 km, 5 km beyond |
| S4 graph, ring 5 km | about 60 | per village: its own land, a ring out to 5 km, the rest in wild regions of about 8 km; links by shared edge |
| S5 graph, ring 2.5 km | about 60 | the same with a 2.5 km ring |

**Three worlds:**
- settled lowland and frontier (villages 17 km apart);
- plain at 17 km;
- plain at 8 km.

**The tests:**
- one village hunts hard (effort 3) for two years, then stops;
- what is left near it after one and two years, as a share of the steady stock;
- whether its neighbour feels it;
- crop losses;
- meat as a share of need;
- every village hunting hard for 40 years.

## 20. What it showed

| Finding | Evidence |
|---|---|
| **Resolution alone changes nothing.** | S1 and S3 give the same depletion, losses and meat to two decimals; S3 has half the zones. |
| **Footprint multipliers are blunt.** | At × 5, local deer fall to 0.3 of steady in a year. At × 15 to × 30, every hunted kind near the village is gone within a year, and crop losses fall to nothing because the raiders are gone. There is no setting between "no effect" and "nothing left". |
| **A node graph with a small ring gives natural depletion, and it is cheap.** | S5 (2.5 km ring) on the plain: deer near a hard-hunting village fall to 0.25 of steady in a year, and those near its neighbour 8 km away to 0.8. About 60 zones, 0.2 s against 7 s for the grid (about 30× cheaper). |
| **A wide ring dilutes the village into its surroundings.** | S4 (5 km ring): deer stay at 0.93 to 0.97 of steady; the village's take is spread over too much land. |
| **Regional collapse never happens.** | With every village hunting hard for 40 years, regional deer, boar and wolves stay at 0.9 to 1.1 of steady in every structure. Four to six villages take too little from 2,500 km². |
| **Villages far apart share nothing locally.** | At 17 km, a neighbour's deer are at 0.97 to 1.0 after two years of hard hunting next door. Only at 8 km with the small ring does the neighbour feel it. |
| **Boar follow the mast, not the hunting.** | Local boar run above steady (1.0 to 1.6) through the hard years in most structures: the mast pulse outweighs the take. |
| **Losses come where the woods meet the fields.** | Crop losses are 4.6 to 5% (90th percentile about 6%) in the wooded frontier, and near 0 on the open plain. |

## 21. What it means for the design

- **A regional ecology at real scale cannot be what people affect.** Four villages hold about 0.1% of the land. Any multiplier large
  enough to make them matter destroys the local kinds outright. This confirms part three.
- **The cheap structure with the right local behaviour is a graph:** each village's own land, a small ring, and coarse wild regions.
  It becomes the two-layer representation of wild_systems.md §10: a coarse layer per area for numbers and drivers, with discrete
  groups near people.
- **Zach on purpose** (8 Nov):
  - "beyond partial observability, it is also something to observe, model and make inferences about ... something that pushes back,
    but also responds";
  - "treating populations of things as rarer, but more sensitive/discrete things might make more sense";
  - "somewhere between rain world and a full proper ecosystem".

  The experiment shows why. The smooth regional numbers neither respond to people nor give them anything to read. Discrete groups
  (this sounder, this pack, this herd in this wood) do both. The coarse layer only sets the odds of groups appearing, leaving and
  returning.
- **The design that followed is wild_systems.md:**
  - shared hidden drivers;
  - kinds as layered rule machines of differing depth;
  - signs with readings by skill;
  - lore as tested belief;
  - creature memory;
  - lags mostly inside a year (Zach: "I want some lags less than years");
  - D2-197: lead times in engine days;
  - D2-198: answers to scares differ by kind.

## 22. The research note behind wild_systems.md

A research pass covered three fields: games with ecological or learnable systems, folk ecological knowledge, and real phenomena with
triggers, lags and signs. Its conclusions are in wild_systems.md §12; the sources follow. A search agent gathered them, and the URLs
are as it reported them; each has not been re-read.

**Games:**
- Breath of the Wild's chemistry engine (GDC 2017): https://www.thumbsticks.com/gdc-17-breath-of-the-wild-science-lies
- Rain World's ecosystem:
  - https://gamedeveloper.com/design/crafting-the-complex-chaotic-ecosystem-of-i-rain-world-i-
  - https://unity.com/blog/exploring-procedural-design-rain-world
- Dwarf Fortress (the drunk cats):
  https://www.pcgamer.com/how-cats-get-drunk-in-dwarf-fortress-and-why-its-creators-havent-figured-out-time-travel-yet
- RimWorld and Dwarf Fortress on generated story:
  https://gamedeveloper.com/design/rimworld-dwarf-fortress-and-procedurally-generated-story-telling
- Caves of Qud's histories (Grinblat and Bucklew 2017): https://pcgworkshop.com/archive/grinblat2017subverting.pdf
- Outer Wilds: https://www.gdconf.com/news/attend-gdc-and-learn-how-outer-wilds-nailed-curiosity-driven-game-design
- Return of the Obra Dinn: https://en.wikipedia.org/wiki/Return_of_the_Obra_Dinn

**Folk knowledge and expertise:**
- Liebenberg, tracking and the origin of science:
  https://archive.cybertracker.org/downloads/tracking/Liebenberg-2013-The-Origin-of-Science.pdf
- Stander et al. 1998, spoor counts by Ju/'hoan trackers:
  https://www.originalwisdom.com/wp-content/uploads/bsk-pdf-manager/2019/03/Stander_1998_SpoorCountsAsIndicesOfLargeCarnivorePopulations.pdf
- Berkes, Colding and Folke, lore learned in crises: https://www.ecologyandsociety.org/vol8/iss1/art5/main.html
- Lore that works unexplained (Mercier on Henrich): https://cognitionandculture.net/blogs/hugo-mercier/a-matter-of-taste/index.html
- Weather lore: https://www.wikipedia.org/wiki/Weather_lore
- Oak before ash:
  - https://www.rmets.org/metmatters/oak-and-ash-can-trees-predict-weather
  - https://naturescalendar.woodlandtrust.org.uk/blog/2019/oak-before-ash-in-for-a-splash/
  - https://www.yorkshirepost.co.uk/news/uk-news/warm-days-end-race-trees-1934346

**Real phenomena:**
- Mast, mice and the cascade (Cary Institute, 35-year study):
  https://www.caryinstitute.org/news-insights/press-release/35-year-study-reshapes-our-understanding-lyme-disease-ecology
- Vole cycles and their predators:
  - https://abdn.elsevierpure.com/files/40433014/Dampening_Prey_Cycle_overrides.pdf
  - https://www.frontiersin.org/articles/10.3389/fevo.2022.783027
- Cockchafers:
  - https://woodlandtrust.org.uk/trees-woods-and-wildlife/animals/beetles/cockchafer-beetle
  - https://www.ages.at/en/plant/plant-health/pests-from-a-to-z/cockchafer
  - https://library.hungaricana.hu/en/view/MEGY_VASM_Sk_2003_Zoological/?pg=113
- Wasp years:
  - https://www.countryfile.com/wildlife/insects-invertebrates/what-is-causing-the-wasp-boom
  - https://www.ucl.ac.uk/news/2022/aug/opinion-plagues-wasps-why-you-shouldnt-panic-about-rumours-rising-populations
- Slugs (AHDB): https://archive.ahdb.org.uk/knowledge-library/what-conditions-favour-slugs
- Ladybirds: https://www.countryfile.com/wildlife/insects-invertebrates/ladybird-swarms-uk
- Eel migration timing:
  - https://energiforsk.se/media/18395/understanding-downstream-migration-timing-of-european-eel-energiforskrapport-2014-51.pdf
  - https://openpolar.no/Record/crwiley:10.1111%2Feff.12346
- Salmon and river flow: https://openpolar.no/Record/crcansciencepubl:10.1139%2Ff86-236
- Hard-weather birds:
  - https://hub.jncc.gov.uk/our-work/severe-weather-scheme
  - https://gwct.org.uk/blogs/news/2018/march/using-science-to-inform-shooting-policy-during-adverse-weather-conditions/
- Wolves and livestock: https://pmc.ncbi.nlm.nih.gov/articles/PMC4497731
- The red deer's year on Rum: https://biology.ed.ac.uk/rumdeer/deer-year
- Bee swarming triggers:
  - https://bjb211.github.io/bee-study-guide/journeyman/swarming/signs-and-triggers.html
  - https://extension.umaine.edu/publications/wp-content/uploads/sites/52/2020/03/1014.pdf
- Fox predation and mange: https://publish.csiro.au/wr/WR02060 ; PubMed 10955890
- Beavers (Exeter, the River Otter trial): https://www.exeter.ac.uk/v8media/research/creww/ROBT_Chapter_3_-_Ecosystem_services.pdf
- Ergot: https://cropwatch.unl.edu/2017/has-ergot-altered-events-world-history
- Wireworm after grass:
  - https://cotswoldseeds.com/articles/628/considering-a-grass-reseed-beware-of-wireworms
  - https://archive.rhass.org.uk/archive/transactions-of-rhass-1790-1969/transactions-of-rhass-1940-1949/transactions-of-rhass-volume-1940/609072-transactions-of-rhass-volume-1940-page-053
- Wild boar crop damage, liver fluke, and the aphid predator lag: from general sources; to be checked against the primary literature
  before calibration.

# Part five (9 Nov): a prototype of the layered wild systems at village scale

The design is [wild_systems.md](../../cybertron2/proposals/wild_systems.md) (partly accepted: D2-197, D2-198). Models:
[02zp_ecosystem_models/wild/](02zp_ecosystem_models/wild/):
- `prep.py`: the worlds and the weather;
- `wild.py`: the general rules and the kinds;
- `run_wild.py`: observers, readers and the inference test;
- `tests.py`: actions, scares, relevance, lags and conditions;
- `results.json` and `tests.log`.

## 23. What was built

**Land and weather:**
- five generated worlds (settled lowland and frontier, fen with islands, upland and moor, plain, sand country) at 8 km spacing, four
  villages each;
- each village's own parcels and the land within 2.5 km by cover;
- ten years of daily weather from the engine's climate (D4-109) at the village's node, under five eras (steady, cold, wet, warm,
  dry);
- Y = 32.

**Drivers** (from the weather): hard frost and its run, the dry spell, soil wetness, the river a day behind the rain, moonless
nights, and anomalies by season. Two pulses are shared by a world's villages: the oak mast (a budget that builds over 2 to 4 years,
spoiled by frost at flowering, with failure the year after a heavy mast) and the vole phase (low, increase, peak, crash).

**General rules, with the kinds as data on them:**

| Rule | Kinds | What it does |
|---|---|---|
| Group | boar (a sounder), fox | sets out on a drive; a lead stage of two nights leaves signs; a raid at the target; remembers a success and comes back; answers scares by its kind (D2-198) |
| Flock | hard-weather birds | come with a freeze, weaken as it runs, scared off by fowling for a day and back; over-taking thins next winter's flock |
| Run | silver eels | an autumn run, heavy on dark nights with rising water after a dry spell; taken at a weir |
| Load | slugs, wasps, voles | an area-level number set by the season's weather; active on conditions; damage in windows |
| Pulse | mast, the vole phase | yearly, with a lag |

**Signs:**
- Each sign has a chance of being noticed and a reading per level: novice, systematic, expert.
- Traces age. Old rooting reads to the novice exactly like fresh (a misread); the systematic reader tells old from fresh; the expert
  also reads the gap the sounder uses.
- Every lead is at least one engine day (D2-197).

**Readers:** at each level, a tally learner over the features that level attends to (what it can notice and read, plus the lore it
holds). It is trained on half the villages and scored on the other half. This tests whether the signs carry information and what it
is worth. It does not test whether agents learn it: the features each level attends to are chosen by hand, so part of the gradient
is built in.

**Households** act on their reader's forecasts. The policies:
- none;
- calendar (by the season alone);
- novice, systematic and expert, each acting on its reader's forecasts.

## 24. What it showed

**Inference by skill** (Brier skill against a reader using the calendar alone; AUC in brackets; scored on the test villages):

| Event | Rate | Novice | Systematic | Expert |
|---|---|---|---|---|
| boar at the field tonight | 0.20 | 0.16 (0.78) | 0.19 (0.78) | 0.20 (0.79) |
| fox at the hens tonight | 0.39 | 0.42 (0.82) | 0.44 (0.83) | 0.45 (0.84) |
| a freeze starts tonight | 0.06 | 0.05 (0.89) | 0.25 (0.92) | 0.26 (0.93) |
| an eel night | 0.09 | 0.11 (0.80) | 0.16 (0.81) | **0.58 (0.94)** |
| a slug night at the seedlings | 0.24 | 0.00 (0.60) | 0.36 (0.88) | 0.43 (0.91) |
| a wasp year (asked in summer) | 0.37 | 0.00 (0.53) | 0.49 (0.87) | 0.54 (0.90) |
| a vole peak (asked in autumn) | 0.22 | 0.38 (0.86) | 0.57 (0.94) | 0.76 (0.97) |
| a heavy mast (asked at the start of summer) | 0.31 | 0 | 0 | **0.92 (1.00)** |

- Every reader beats the calendar, and the expert beats the novice on every event.
- The gap is large where the expert's lore joins two signs: eels (rain after the dry weeks, and the dark of the moon) and the mast
  read from the catkins a season ahead.
- The gap is small for boar and the fox. For both, the strongest sign is visible to everyone: yesterday's damage means they come
  back. That is their L1 rule.

**What reading is worth** (net for the kind as a share of a village's food need a year; work at 0.5 food a unit; villages where the
kind applies):

| Kind | None | Calendar | Novice | Systematic | Expert |
|---|---|---|---|---|---|
| boar (wooded villages) | −21.7% | −14.4% | −16.9% | −15.8% | **−9.2%** |
| eels (river villages) | 0 | +4.5% | +6.6% | +6.5% | +6.7% |
| slugs | −5.8% | −5.8% | −5.8% | −5.3% | −4.9% |
| wasps | −2.8% | −2.6% | −2.7% | −2.7% | −2.1% |
| voles | −1.8% | −1.8% | −1.9% | −0.9% | −1.1% |
| fox | −2.9% | −1.0% | −0.7% | −0.5% | −0.5% |
| hard-weather birds | 0 | +0.2% | +0.2% | +0.2% | +0.2% |

- **Boar: the expert's edge is the answer to scares, more than the reading.**
  - The novice and the systematic reader watch with one scare, which the sounder gets used to. Both do worse than a calendar watch
    at every gap.
  - The expert varies the scare, brings a dog after two turns, and watches the gap it read: about 9% of need against 22% unwatched.
  - The real lesson people would learn: "they got used to the fire".
- **Eels: reading pays** (+2% of need over the calendar), but the levels barely differ. The act that pays is a crew at the weir on
  big nights; even a novice's forecast is good enough to call it.
- **Fox: shutting the hens is everything.** Reading adds nothing beyond it.

**Answers to scares** (D2-198; the same scare every night, or varied; share of encounters turned away, by the encounter's order
within the year):

| | 1st | 2nd | 3rd | 4th | 5th+ |
|---|---|---|---|---|---|
| boar, the same scare | 0.35 | 0.26 | 0.29 | 0.23 | 0.25 |
| boar, varied | 0.72 | 0.75 | 0.80 | 0.71 | 0.58 |
| fox, the same scare | 0.83 | 0.87 | 0.91 | 0.83 | |

- Boar get used to a scare; habituation fades at 0.01 a day, so it carries into the next year.
- The fox is scared off and comes back, and the same scare works again.

**Relevance** (loss or yield as a share of need in a village-year; the test is about 10% in some year or choice):

| Kind | Median | 90th percentile | Max | Passes? |
|---|---|---|---|---|
| boar, unwatched | 22% | 31% | 42% | yes; probably high against real damage (1–10% near woods, 20–50% locally in bad years) |
| eels, with a river | 11% | 12% | 17% | yes, where there is a river |
| slugs, nothing done | 4% | 12% | 27% | yes, in wet years |
| hard-weather birds | 0.3% | 1% | 22% | yes, but only in the fen in a hard winter |
| wasps, nothing done | 1.6% | 4% | 11% | barely, in a wasp year with hives and fruit |
| voles, nothing done | 1.3% | 4% | 10% | barely |
| fox, nothing done | 3% | 3% | 3% | no |

**Lags a run can see** (12-day windows on the test villages under steady, cold and wet eras):
- On average, 2.8 kinds show a sign followed by its event within one to three days (10th percentile 2; some windows show none).
- By kind, the share of windows: fox 94%, voles 67%, wasps 55%, fowl 22%, boar 17% (only 3 of the 20 villages have a sounder),
  eels 15% (an autumn run), slugs 12% (the sowing windows).
- Acting within the window changes the outcome within the window in this share of windows: boar 91%, eels 74%, fowl 69%, fox 43%.

**Conditions** (share of years, five worlds, ten years each):

| Condition | Steady | Cold | Wet | Warm | Dry |
|---|---|---|---|---|---|
| heavy mast | 0.30 | 0.28 | 0.32 | 0.38 | 0.26 |
| the bust (fail after heavy) | 0.28 | 0.26 | 0.26 | 0.32 | 0.24 |
| bust then a hard winter | 0.10 | 0.14 | 0.14 | 0.22 | 0.14 |
| hard winter | 0.50 | 0.50 | 0.40 | 0.50 | 0.70 |
| frost at flowering | 0.02 | **0.28** | 0.02 | 0 | 0.02 |
| vole peak / crash | 0.22 / 0.24 | 0.22 / 0.26 | 0.22 / 0.26 | 0.22 / 0.24 | 0.22 / 0.26 |
| wet winter (slugs) | 0.40 | 0.40 | 0.40 | 0.40 | 0.20 |
| warm spring (wasps) | 0.40 | 0.40 | 0.40 | 0.60 | 0.60 |

The conditional layers all show within ten years. The eras move the temperature conditions (frost at flowering in the cold era,
warm springs) more than the wet ones.

## 25. What it means for wild_systems.md

1. **The kinds that pass the relevance test at village scale:**
   - boar: by far the strongest; its expert layer is mostly D2-198's answer to scares;
   - eels where there is a river;
   - slugs in wet years;
   - fowl in the fen in a hard winter;
   - wasps and voles barely;
   - the fox fails.

   This matches node_ecology.md (the land matters as threat more than food). The fox could stay a simple kind (L1: shut the hens; L3:
   den control in a hungry spring) or be joined to the lambs at lambing to matter.
2. **The reading gradient is real where a kind's lore joins signs** (eels, the mast, voles, freezes, slugs). It is thin where yesterday's
   damage tells everyone (boar, fox). For those, the depth must sit in the acts (which gap, which scare, a dog), not the forecast.
3. **Principle 4 holds only with the right act.** The eel forecast was worthless until the act it pays for was named: hands at the
   weir on the big night. Each leading sign needs its act designed with it.
4. **The fast arms carry a run.** About three kinds show a lead-and-event pair in any 12-day window, and acting changes the outcome
   within the window for boar, eels and fowl in most windows.
5. **D2-198 works as intended in the model:**
   - against boar, a steady scare fails and variety or harm works;
   - against the fox, a steady watch is enough;
   - which kind is which is itself learnable.

## 26. Problems found on the way

- **The engine's winters freeze too long.** With a hard frost taken as a night below −3 °C on a day below 3 °C, a run of two or
  more frozen engine days (three weeks or more of real time) comes in 40–70% of winters. Long freezes in a temperate lowland come
  perhaps once in five to ten years.
  - The cause looks structural: a weather type holds for some engine days, and each engine day stands for about 11 real days, so a
    spell of three days is a month.
  - This belongs to the climate's calibration (37.4, D4-109), and it is part of the year-length question.
- **Boar damage is probably high** (22% of need unwatched in wooded villages). It is kept at that level to show the mechanics.
- **The generated land is mostly cleared.** Only 3 of 20 villages have a big wood within 2.5 km (frontier, upland), so boar matter in
  few places. This follows from the generator's settled land, and it is consistent with node_ecology.md.
- **The engine's calendar breaks on `day: 0`.** A spec with `calendar: {day: 0}` gives a year index of −1, and the climate's
  `year()` then recurses without end. The calendar's days start at 1, so this is a malformed spec, but the failure is a hang rather
  than an error. For 37.4 when convenient.
- **The readers are tally learners over hand-chosen features.** Part of the skill gradient is built in. The test shows that the
  signs carry the information and what acting on it is worth, not that agents will learn it. That needs the LLM probe.

# Part six (9 Nov): the general wild system, wave 1, and targeted LLM tests

Design: [wild_systems.md](../../cybertron2/proposals/wild_systems.md) §13 (the merged waves) and §14 (how it fits the engine).
Models: [02zp_ecosystem_models/wildsys/](02zp_ecosystem_models/wildsys/) (README there).

## 27. What was built

**The general system** (`rules.py`, `village.py`): five rules, Pulse, Group, Load, Run and Flock. `check.py` confirms that no kind is
named anywhere in the rule code.

**Wave 1 as data** (`kinds.py`): seven kinds; each kind's signs (a reading per level); goods (meat, fat, hide, pelt, antler, eels,
fowl, feathers); and acts with their costs.

| Kind | Rule | Answer to scares (D2-198) | Lives in (of 20 villages) |
|---|---|---|---|
| wild boar (with the mast) | Group | gets used to them | 3 |
| red deer | Group | gets used to them | 3 |
| hare | Load | scared off | 18 |
| birds at the corn | Load | gets used to them (a scarecrow fast, children slowly) | 20 |
| rats and mice | Load | does not answer | 20 |
| eels | Run | does not answer | 13 |
| wildfowl | Flock | scared off | 14 |

**Scripted households, as a share of food need, across all villages and eras** (`survey.py`; work valued at 0.5 food a unit):
- doing nothing costs 9.8%;
- watching by the calendar costs 4.9%;
- the scripted expert costs 2.5%.

## 28. The targeted LLM tests

**Setup:**
- A model plays one household, morning by morning. Each morning it gets the day and stage, the weather, what it noticed (signs at
  its level, as prose), what happened in the night, its losses or catches so far, the last three days, and its own notes. It then
  chooses tonight's acts.
- Models: Haiku and Sonnet (5.5) through `claude -p`.
- Villages: two per test, from the generated worlds, with the steady era's weather from the engine's climate.
- Scoring: net food (yield − loss − work at 0.5 food a unit, children's units at 0.1), against three scripted households on the same
  land, weather and draws.
- Size: 28 runs, 704 calls.

| Test | Days | Arms |
|---|---|---|
| T1 boar and deer at the field | summer to harvest, two years (20 decisions) | novice or expert readings; names real or masked |
| T2 eels at the weir | autumn, three years (30) | no lore, or a wrong saying: "the eels run on bright moonlit nights" |
| T3 birds and hares at the sowing | spring and autumn sowings, two years (28) | no lore, or a wrong saying: "a good scarecrow keeps every bird and beast off the corn" |

**The first run was withdrawn, and all of it was rerun.** It had two faults:
- each act's work was booked twice, once by the rule and once by the act;
- commits made during the run cut its logs short.

The rerun's logs are complete: `replay.py` replays every call's acts and reproduces the scores.

## 29. Results (rerun; net food, the mean of two villages)

**T1, boar and deer at the field.** Scripted households: doing nothing −132, the calendar watch −79, the scripted expert −59.

| Arm | Haiku | Sonnet | Raids met at the right gap | Nights watched (of 20) / with no raid |
|---|---|---|---|---|
| expert readings, named | −70 | −66 | 4 of 4.5 | 15–20 / 11–16 |
| expert readings, masked | −69 | −77 | 4 of 4.5 | 14–20 / 9–16 |
| novice readings | −95 | −88 | 3–4 of 4.5 | 16–20 / 12–15 |

- **The models read the expert signs and meet the raids:** about 4 of 4.5 raids met at the gap the sign pointed to, with names masked
  as well as named.
- **Reading pays:**
  - expert readings beat novice readings by about 20 to 25 food;
  - every arm beats doing nothing by 40 to 65;
  - the expert arms are a little better than the calendar watch.
- **They over-watch.** Most nights they watch, and most watched nights have no raid. Haiku, for example, covered all three gaps "while
  the sounder is near" even when the trail pointed to one. Work was 56–85 units, against 21 for the scripted expert, and that gap is
  why none reached it.
- **They vary the scare** (5 to 10 changes), though partly by habit. Their notes rarely state that the boar got used to a scare.
- **Noise:** the villages differ by more than the arms. At s3 the expert arms ran −78 to −103; at s1, −37 to −54. With two villages
  and one weather draw each, differences under about 15 food are noise.

**T2, eels at the weir.** Scripted households: doing nothing 0, traps every night +55, the scripted expert +80.

| Arm | Haiku | Sonnet | Crews on the 3 big nights | Crews on bright nights (first half → second half) |
|---|---|---|---|---|
| no lore | +79 | **+87** | 2 / 2.5 | 0 → 0.5 / 1 → 0.5 |
| wrong lore | +63 | +56 | 1 / 0.5 | 3.5 → 3 / 4.5 → 3.5 |

- **Without lore, both models do as well as the scripted expert;** Sonnet does better. They already know that eels run on dark nights
  after rain: prior knowledge, not learning.
- **The wrong saying costs 16 to 31 food** and pulls Sonnet down to the calendar's level. The feedback corrects it only slowly.
  - Crews on bright nights fall a little between the first and second half.
  - In the third autumn Sonnet writes "the moon lore is unreliable", and sets its own reactive rule instead: "if the traps ever show
    30 or more, send the crew". That rule acts on the day after a run starts, not on the leading signs.
- This is the behaviour wild_systems.md §9 wanted: wrong lore survives weak feedback, and a careful reader overturns it slowly.

**T3, birds and hares at the sowing.** Scripted households: doing nothing −32.5, a scarecrow always −25.1, the scripted expert −22.9.

| Arm | Haiku | Sonnet | Children on bird days (of 16) | Children on hare-only days (of 12) |
|---|---|---|---|---|
| no lore | −29.3 | −30.1 | 6 / 8.5 | 5 / 8.5 |
| wrong lore | −29.1 | −28.1 | 8.5 / 9.5 | 9 / 9 |

- **All arms beat doing nothing but lose to a plain scarecrow.** The losses are about the same as the scarecrow's (18–19 against 24);
  the extra cost is children's days and snares.
- **The models do not learn the split between the kinds.**
  - The design's lesson: birds get used to the scarecrow, so send the children on the bird days; hares are scared off by it, so a
    scarecrow is enough on the hare days.
  - The models send the children on about as many hare-only days as bird days. Their notes say "the scarecrow alone failed on day 4"
    without telling which kind came. The feedback signs do name the kind ("the birds came down ..."; "fresh hare nibbling ..."), but
    the models generalise across kinds.
- **The wrong saying did not make them trust the scarecrow.** They used more children with it, not fewer.

## 30. What the tests say about the design

1. **Readings by skill matter to real models.** With expert readings, models meet raids at the right gap; with novice readings they
   lose 20 to 25 food more. The skill gradient is not only built in by hand.
2. **Prior knowledge carries the real-world rules** (eels on dark nights after rain; boar coming back to a field). Masking names did
   not change T1, because the expert reading itself says where the trail goes. To test learning rather than knowing, the kinds or
   rules must differ from what the models already know: invented kinds, or rules that change by place.
3. **Seeded wrong lore persists and is overturned only slowly.** That makes lore as tested belief (§9) a working mechanic with real
   models. It also argues for keeping wrong lore rare and costly enough to matter.
4. **Models over-act on threats.** They watch most nights and use children and snares freely. A real work budget is needed, with the
   cost of tonight's watch felt in tomorrow's day's work, not stated in units. Otherwise "watch everything" is a safe default and
   reading the signs is worth less than it should be.
5. **Telling kinds apart by their answer to scares (D2-198) is not learned in two seasons.** If that is to be learnable, either the
   feedback must be sharper (a sign that says which kind ignored which scare, put plainly), or the lesson must come through lore and
   teaching.

## 31. Limits

- Two villages per test, one weather draw each: small samples.
- Each arm was run once per village.
- No Opus.
- No arm that reads the signs with no notes.
- The models' cost per call was not reported by the CLI path.
