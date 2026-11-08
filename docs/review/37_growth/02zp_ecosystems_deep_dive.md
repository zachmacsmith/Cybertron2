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
