# Proposal: world generation as one history, with pins met in the loop

**Status:** discussion. **Owner:** the c2viz session (analysis at Zach's request, 14 Nov). It would be built by 37.2 (the land) and
37.4 (`engine/generate.py`, the lineage); nothing here changes code.

**Affects:**
- `cybertron2/landgen/` (settle.py, write.py, the checks);
- `cybertron2/engine/generate.py`;
- spec/world/generation.md (not yet written: OPEN L-101), seeding/populations.md;
- proposals generator.md, generator_stage1.md, temperate_landscapes.md, land_kept.md, peoples_benchmark.md.

## Summary

Zach, 14 Nov: "Look at the generator for how a world is specced. Can you compare the original idea (pinning things and everything
building around that) to how it currently works. What are the main flaws of (a) the current environment generation system and (b)
the current lineage generator ... see if you can think of a better design or what should be restructured."

**The finding in one line:** the original design was constraint-led (pin anything, fill in around it, meet targets by adjusting what
is free, no seed searches). What was built is a one-way pipeline that checks at the end and refuses, with the people generated last
and apart from the land. Most of the problems Zach has hit come from those two choices, not from any one bug.

**Measured on main today (`45ea678`), 14 Nov:**
- **The land:** 36 worlds (18 configurations, 2 seeds each, 4 villages): **31 refused**, all by the capacity check.
  - The 124 refused villages sit at 0.59 to 0.84 of their scarcest flow (median 0.69) against a band of 0.6 to 0.7.
  - In a refused world (plain, seed 3) every village got exactly the fields and woods the allocator wanted (14 of 14 plots, 5 of 5
    wood units), and the engine's capacity still reads 0.75 against a target of 0.69. **The allocator and the check use two models
    of the same quantity**, and they drift whenever the engine's rules change (D4-103, D4-112).
- **The lineage:**
  - A four-line place meets its bounds in **7 of 400 simulated histories**; the tree is found by rejection.
  - In a generated world that passed (upland and moor, seed 3, 39 people):
    - **0 of 148 kin ties cross villages**;
    - 13 spouses came from "Ashby", a place that is not in the world;
    - 21 people "left for Ashby";
    - every line was founded within one lifetime: every village is new;
    - 4 children and 3 youths among 39 people.

## 1. The original idea against what was built

| D2-173 and generator.md said | As built |
|---|---|
| **Pin anything at any layer:** "a river from the hills through Barleyfield", "a ford at Millford", "a pass between Hollins and Wenmoor", a height at a place, "short of wood", "a feud" | Pins are mostly **about places**: `at` an anchor, `terrain`, `on`, `has`, `soil`, `resources`, `short_of`, `vacant`. Shapes come from 18 named configuration templates. Words that should place a feature are special cases in write.py (`on: sea` with no sea adds a coast). There are no pins on roads, rivers or fords by name (peoples-worlds adds pinned roads), and none on people beyond `food_share`. |
| **Targets met by monotone adjustment** of what is unpinned; "reproducibly, **without seed searches**" | Land is sized **once**, open loop, by settle.py's own formula; the engine's capacity is checked **afterwards**, and the world is refused. Getting a world means searching seeds (on 8 Nov, 1 of 16 tries passed). |
| **Pins win where physics allows;** a pin it can't meet is refused **with the reason** | Pins that fail are refused with a reason (good). Targets that fail refuse the whole world. A refused world is not written, so it cannot be looked at. |
| **Land first, people second, the same keyed way;** founders settle by the siting scores | People are generated **after** the land, by a separate generator that knows nothing of it; the land is then sized **again** for the people it got (two passes). |
| **A world under the graph**, the graph derived from it | Built (cells, parcels from cells, roads from cells). The engine does not keep the cells in a run (D2-177; W-25 is adding it). |

## 2. Flaws of the environment generator

1. **Open loop against a moving target.** settle.allocate computes plots and wood units from its own constants (CAP.PLOT, WILD,
   wood_flow, the year). The check reads `engine.capacity.node` on the written world. Two models of one quantity will disagree
   whenever either changes. This is why most seeds are refused today and why it got worse after the engine's overhaul. The design
   said "adjust"; the build says "compute, then check".
2. **Refusal instead of repair.** One village 0.04 outside its band refuses the whole world, so the only remedy is another seed:
   the seed search D2-173 ruled out. The band itself (0.6 to 0.7) is narrower than the allocator's rounding: a plot or a wood unit
   moves a 10-person village by more than 0.05.
3. **Shapes from templates, not from pins and process.** Variety between worlds comes from choosing one of 18 configurations. Inside
   one, the land is fixed by global dials. Temperate landscapes (D2-191) set every world's woodland to 30% (17 of 18 on 3 Nov) and
   most cleared land to one "grassland". Circles (G-34) came from the same source: geometric primitives standing in for processes.
4. **No time.** The present landscape (how much is cleared, where the fields are, which village is older and bigger) is set
   directly, not as the result of a history. "Cleared by how long settled" is one dial for the whole region, not each village's
   own past.
5. **The human layer is written by hand-coded templates.** write.py gives every household the same 2-room house, 2 cows, a byre for
   the first, the same stocks; trades by a few rules. Buildings are not sized to the built parcel's ground: all 75 villages in the
   3 Nov gallery were overfull. Households differ only by name.
6. **One 600-line writer does everything:** names, descriptions, households, buildings, herds, claims, people, ways, checks, economy.
   Stage boundaries are unclear, so a failure (or a new pin) has no obvious home, and each new need is a special case in it
   (vacant places, pinned roads, soils set "instead").

## 3. Flaws of the lineage generator (`engine/generate.py`)

1. **Rejection sampling at two levels.** A place's history is simulated whole and thrown away unless every bound holds (1.75% pass
   for four lines); then the region is restarted if any place never fits. It is slow, it fails with "widen the bounds", and the
   reported `try: 0` hides the inner retries. It cannot hit a specific target ("a household of seven", "an old head and no heir");
   it can only hope for one.
2. **A line is a household.** Sons marry and stay in their father's household for ever, so households are lines, not families.
   Real households split at marriage, and the split is where land, houses and inheritance come from.
3. **Each village is its own island.** Lines are simulated per place. Marriages are only between lines of one place, or with a fixed
   off-map "Ashby". There is no kin between villages, which is the strongest real tie between them (and the dependence the scenario
   rules ask for). Ashby is not in the world: people remember kin in a place they cannot go to.
4. **Every village is newly founded, at once.** One founding couple per line, all starting within a few years of each other, about one
   lifetime ago. There are no old villages, daughter settlements or extinct lines: no frontier, no history of growth.
5. **Demography ignores the land and the weather.** Births and deaths are fixed rates by age. The hard winters are three random years,
   not the world's own climate (D4-109 can draw the past from the same seed, as the wild layer's history already does). How well a
   village is fed never touches its history, so the history cannot explain why a place is the size it is.
6. **The age structure is shaped by bounds, not by demography.** Bounds ask for mostly working adults (Zach, 10 Nov), and rejection
   finds trees with few children (4 children and 3 youths in 39). That may be the right world for a benchmark, but it should be a
   stated choice, not what survives rejection.
7. **It runs after the land and makes the land run twice.** The land is sized for planned households, people are generated, and the
   land is regenerated for the people made. The dependency is the wrong way round: in a history, land and people shape each other
   over time.

## 4. The proposal

**Revised 14 Nov (Zach):** the present population is pinned and the history is filled in behind it; and generation fills to
the conditions and repairs what a change touches, instead of building, rejecting and building again. Zach: "the current population
mix is something we should be able to pin, with the history backfilling ... the history etc. is all downstream of that even though
happening before"; "fill to suit the conditions and if you adjust the conditions it can backtrack or use some subset ... and then
regenerate to fill the new conditions." §4a and §4b below replace the forward history of stage 2 as the frame.

**One generator, four stages, each with its own pins, its own checks and a written result.**

| Stage | Makes | Pins it meets | How it meets them |
|---|---|---|---|
| **1. Land** | the physical layers, as now (macro, elevation, climate, water, soil, terrain, natural cover) | shapes, rivers, fords, passes, heights, soil, resources, by name or place | control points the fields pass through (as rivers are laid now); a pin's shape from a declared table of words to primitives, not special cases |
| **2. People, then their past** | the present population (households, members, ages, roles), pinned or drawn from a pinned mix; then the genealogy and events behind it, built backward (§4a) | the household mix, any person, kin, feuds, founding dates, a famine | the present is given or drawn; the past is chosen to fit it, never simulated and rejected |
| **3. The present** | the graph and the state: nodes, parcels, holdings, houses, herds, stores, trades, from the end of the history | capacity bands, a village short of wood, food_share, vacant places | closed-loop adjustment with the engine's own measures |
| **4. Checks** | the report, always written | physics refuses; design warns unless required | after every stage, so a failure points at its stage |

### 4a. The present first, the past filled in behind it

**The order of generation is not the order of time.** Generation starts from what the run needs (the people now) and works back to
what explains it. The forward model is kept, as the judge of what is likely: it scores choices, it does not filter whole worlds.

1. **The present population is an input.** A world gives any of:
   - an explicit list: households with members, ages, sexes, roles;
   - a mix: "4 villages; households of 3 to 7; most a couple with young children; two widows living alone; one household of three
     generations; about two in five under 15";
   - nothing: the default mix, drawn.

   A mix is drawn into an explicit list by keyed draws (per village, per household), so the list is reproducible and editable.
2. **Each household's inner ties are inferred** from its members' ages and roles: the couple, their children (each born when the
   mother was 16 to 45 and at least two years apart), a widowed parent.
   - A member who does not fit is reinterpreted, not rejected: a grandchild, a nephew taken in, a second wife's child, a lodger.
   - The choice among readings is weighted by the forward model's likelihood.
3. **The genealogy is built backward,** a generation at a time, as a population geneticist builds a coalescent:
   - each living adult gets parents, with birth years drawn given the child's;
   - parents are merged into sibships across households and villages, by an assignment that respects ages and nearness. Two heads
     can be brothers; a wife can be the sister of a man in the next village. This is where kin between villages comes from, chosen
     to fit, not hoped for;
   - each ancestor's death is placed after their last child and, where it fits, in the world's own hard years (the climate
     scheduler's past, D4-109);
   - siblings not living now are given fates (died young, left, married away to a named place).
   - This goes back to the founders, as far as the history's span or a pinned founding date says.
4. **Events are written from the genealogy:**
   - foundings: the oldest line's arrival; a daughter village where its founders' parents lived elsewhere;
   - marriages, deaths, departures, feuds and debts;
   - each person's memories, from their own age at each event.
5. **What is worked follows the people, not the land itself** (corrected 14 Nov: §4c). The physical land is generated and
   pinned on its own; how much of it is cleared and worked is backfilled, within what the land affords.

**What this gives:** exact control for test conditions (the household mix is what was asked for, every time), and a past that is
consistent with it by construction. **What it costs:** a backward-built past is consistent, but not automatically likely. That is why
every choice is weighted by the forward model, and the report says where a pin forced an unlikely past (a woman with nine living
children, a village of one generation).

### 4c. Land, its use and capacity: three things, not one (Zach, 14 Nov)

Zach: "deciding the different environmental conditions themselves are important, e.g. deciding which nodes have what types of
resources ... it shouldn't just automatically change the landscape to fit the carrying capacity ... done badly this could just
overoptimise specific features ... like giving really big fields, rather than being able to holistically create places that can
richly support people in different ways."

**That is what the generator does today.** settle.allocate meets the target with two levers: plots to the food target and managed
wood to the heat target. Every village gets the same recipe in the same order (built ground, fields, meadow, pasture, wood, waste),
and the target is met by field count. Separating three things fixes it:

| Layer | What it is | Who sets it | Fitted to people? |
|---|---|---|---|
| **The land** | terrain, water, soil, climate, resources: a river, a seam, the downs, a fen | pins and the generator (stage 1); a world says which node has what | **never** |
| **Its use** | what has been cleared and how it is worked: fields, meadow, pasture, managed wood, a weir, a mill, a fold | the history, backfilled | **yes, within what the land affords** |
| **Capacity** | how many the land, as used, feeds and warms, by every way it can | measured, never a knob | it is the comparison |

**Capacity is measured with the full model.** 37.4's capacity package (D4-102: `cybertron2/capacity/`) already counts every food
source in the registry (fields under rotation, herds, wild food, fish), processing and spoilage, the lean season, the work people can
give, levels of practice (bare, standing, worked, best, ceiling), and what a short node can draw from a neighbour (space.py). The
generator's check uses the narrow `engine/capacity.node` (fields x grain + woods x wild food), a third model. The generator should
read the package.

**Approaches, from least to most automatic:**
1. **Measure only.** Land and people are generated apart; capacity is reported by source and level; the designer changes pins.
   Honest and never over-fitted, but every mismatch is the designer's to fix.
2. **Fit one lever** (today): resize fields until the ratio is in band. Over-fits and makes every place alike. Rejected.
3. **Choose where, not what** (siting as matching). The land is generated whole and unchanged. A village's people are placed where
   the land affords them: a pinned village of seven households takes a site whose affordances (soil, water, grazing, wood, fish)
   support seven. Good for "which node has what" pins: the land is pinned, and the people are put where it works.
4. **Livelihoods by affordance.** Each village's use is drawn as a mix of ways of living, weighted by what its land affords: a river
   village fishes and mills, a downland village keeps sheep, a fen village takes eels and reeds, a wood-edge village keeps pigs and
   cuts timber. Each pathway is developed only as far as is plausible for its ground, with bounds a rule sets (a household's
   holding in field strips, the share of a node that can be meadow, a weir's catch). So capacity comes from several sources in
   proportions the land suggests, not from the cheapest one stretched.
5. **Dependence by design.** Capacity is not balanced per village. A world states a profile across the region: Corneby feeds
   itself twice over, the hill village is short of grain and has copper, the region as a whole at 70% (D2-161). Shortfalls are met
   by neighbours and trade, which is the dependence the scenario rules ask for. The target is a profile, not a band per village.

**The recommendation: 3, 4 and 5 together, with 1 as the fallback.**
- The land is pinned or generated and is never changed to fit the people.
- Villages are sited where the land affords them (3); each develops a mix of livelihoods within plausible bounds (4); the region
  meets a stated dependence profile (5), measured with the full capacity model.
- **Which side is free is the world's choice:** people fixed and use fills; land and use fixed and people fill; or both fixed and
  the report shows the gap.
- **When the conditions conflict** (seven households pinned on a node pinned as poor heath, with no trade allowed), nothing is
  stretched past its bounds. The report names the gap by source and the levers that would close it, most plausible first: more
  cleared land within bounds, a pathway the land affords but has not been developed, a trade dependence, fewer people.

### 4d. Richness: one tunable measure that feeds every food source (Zach, 14 Nov)

Zach: "there should be some ways to in general adjust the carrying capacity of land ... richer or sparser ... a holistic measure ...
so that when generating the land, whatever food sources are introduced are scaled based on that ... bigger rivers with more fish or
more forests ... a metaparameter for the generation, tunable for the whole world or specific places, that feeds into a bunch of
things ... Otherwise ... I can only tweak population size."

**The pattern: drive the cause, not the effects.** In ecology the holistic measure is the land's productivity, how much grows on
it in a year: net primary productivity, set by warmth, water and soil. Every food source downstream (crops, grass and the beasts on
it, woods and their mast and game, fish in the water fed by the land) is a function of it. So make one quantity the generator's
upstream driver, and let each food source read it through its own rule. Do not give each source its own knob.

1. **A richness field** `r` over the map, 1.0 by default.
   - **Set by:** a world's level (`richness: 0.8`); places and areas as control points the field passes through (`Northby: 1.3`, "the
     fen: rich", "the eastern moor: poor"); optionally a gradient.
   - **Blending:** like the other fields, with a reach, so a richer valley shades into its neighbours instead of stopping at a line.
   - **Words** map to values, as the vocabulary does now (D2-173: "rich bottomland", "poor stony soil").
2. **Each food source reads `r` through a declared transfer function,** in one registry beside the sources (one row a source, as the
   capacity package registers its sources), so the coupling is defined once and can be inspected:
   - soil: base fertility (D4-112: the engine's own multiplier, `land.base_fertility`) and depth;
   - grass: its stock and regrowth on pasture and meadow;
   - woods: standing wood, regrowth, mast, wild plants;
   - water: rivers' flow, as rain over the catchment, so richer land gives bigger rivers and more fish; a lake's fish;
   - the wild layer: each kind's habitat capacity per area (D2-199), through the food it eats;
   - not stone or ore: richness is about what grows.
3. **Two depths of effect,** so tuning one place never rearranges the map:
   - **World or region richness may move the physical drivers:** more rain, a longer growing season, deeper soils. That can change
     geography (bigger rivers, more wood, more fen) and happens before the land is laid out.
   - **A place's richness scales only yields and stocks** on the land as laid out: the same river, but more fish in it; the same
     wood, denser; the same fields, more fertile.
4. **Within each terrain's range.** A rich heath is the best heath, not loam. Richness moves each terrain's numbers within the
   bounds its kind allows, and never changes a cover or a terrain into another. That is the guard against over-optimising: the land
   stays the kind it is.
5. **Monotone by construction,** and tested: raising `r` never lowers any source's yield. So capacity, measured with the full model
   (§4c), rises monotonically with richness, which makes it tunable:
   - **Tune by richness:** set `r` and read the capacity.
   - **Tune by capacity:** ask for a capacity ("Northby feeds about 40 at the worked level", "the region at 0.7") and the generator
     finds the place's `r` by bisection on that one number. Which sources carry the gain is decided by the land's affordances, never
     by the target.
6. **Three knobs that stay apart:**
   - **richness:** what the land grows by nature;
   - **use:** what has been cleared and worked (§4c, from the history);
   - **level:** how well it is farmed (the capacity package's bare to ceiling).

   A place can be rich and little worked (a frontier), or poor and worked hard (an old upland village).
7. **How it fits the rest:**
   - with people pinned and a target ratio, `r` per place is the free value;
   - with `r` pinned, people or use fill;
   - a dependence profile (§4c item 5) is a richness profile over the region, met by bisection per place.

**What is new and what exists:**
- **Exists:** the engine's per-parcel fertility multiplier (D4-112); the generator's soil fertility; the wild layer's habitat
  capacities.
- **New:** the field, the registry of transfer functions, the monotone guard test, and the bisection.

**Size:** medium, mostly in the generator; nothing in the engine beyond fields it already reads.

### 4b. Generation as a graph of keyed decisions, repaired, never rejected

**Each decision is a node:** a village's site, a parcel's cells, a household's members, a person's parents, an ancestor's death year,
a road's path. Each node has:
- its **inputs:** the pins that bear on it and the upstream decisions it reads;
- its **candidates,** in a keyed order (D2-70: the order is a hash of the world's seed and the node's id, so it is the same every
  time);
- its **constraints:** what its choice must satisfy, given its inputs.

**The rule:** take the first candidate that satisfies the constraints.

1. **Filling, not filtering.** A node that has no fitting candidate backtracks to the nearest upstream decision that is not pinned and
   tries that node's next candidate (conflict-directed backjumping, as in a constraint solver). The world is never thrown away; only
   the decisions in conflict move.
2. **Idempotent.** The same pins and seed give the same world, byte for byte: candidate orders are keyed, and the first fit is taken.
3. **Incremental.** Each node records the inputs it read. When a pin changes, only the nodes whose inputs changed are made again,
   and then their dependants, as a build system rebuilds only what a changed file touches.
4. **Stable under edits.** On a change, the previous world's choices are tried first, as soft pins. Making Northby's third household
   a family of seven changes that household's genealogy and the kin who must now fit; the map, the other villages and their people
   stay as they were, unless a constraint forces them to move. The report lists what moved and why.
5. **Refusal is the last resort,** and only of a pin. When backtracking exhausts every unpinned choice, the pin that cannot be met is
   named, with the pins it conflicts with.

**Where it will not be perfectly local:**
- **The land's continuous fields** (noise and shapes) are global: moving a range moves heights everywhere. Pins there act as local
  control points with a limited reach, so most land edits stay local. A new configuration remakes the land.
- **Claimed land is first come, first served** between villages: a village that grows can push a neighbour's fields, so it moves too.
- Both are reported as moved; neither needs a seed search.

### Stage 2 as first proposed (forward, superseded by §4a as the frame; its parts are kept as the forward model that scores choices)

- **The unit is the household,** not the line:
  - a couple founds a household; sons (or daughters, by the custom) found their own on marrying, if there is a plot and a house to
    be had, else they stay;
  - holdings, houses and herds pass by the custom's inheritance rule;
  - lines become surnames over households.
- **One marriage market for the region,** by distance. Spouses come from the nearest villages with someone of age, so kin crosses
  villages in proportion to nearness. An off-map origin is allowed only as a named node of the world (a market town beyond the map
  edge), never as a bare name.
- **Villages are founded at different times.** An old village fills its land; when its holdings run out, a household founds a daughter
  village on the best unclaimed site (stage 1's siting scores, in order). So there are old and new places, a frontier, and sizes
  that differ for a reason.
- **Births and deaths read the land and the weather.** Each year's food per head comes from the village's cleared land and its
  yields, under the climate scheduler's own years (the same draw the wild layer uses for its history, at days far ahead of the run).
  Hard years are the world's hard years, remembered by those who lived them. Fertility and mortality are tables (calibrate), with
  starvation, disease and fever as named causes.
- **Clearing is part of the history:** each household clears and works land as it needs and can, so the present cleared share, the
  fields' place and the woods left are the history's result, per village. That replaces the region-wide 30% woodland dial and the
  rings set directly.
- **Pins on people and places become conditions on the history,** met in order of cost:
  1. **chosen:** a pin that is a start state (a village founded 120 years ago, a line of smiths) is simply the start;
  2. **aimed:** a size or a band (Northby about 30 people, mostly adults) sets the founding date and rates from a fitted table, so the
     expected end lands near it;
  3. **repaired:** what is still off is fixed by small written events at the end (a death, a marriage, a departure, a household
     taking in a widow), each recorded in the history as what happened;
  4. **resampled locally:** if a repair is too large, only the household or village concerned is run again, never the region.
- **The age structure is a pin, not an accident:** realistic by default (about two in five under 15), or "mostly working adults" as
  a world's stated choice, met by the start date and repair.

### Stage 3, the present

- **The graph from the end state:** nodes from settlements and their reach, parcels from land in one use (as now), wild land as the
  waste left.
- **Houses, herds and stores from each household's history:**
  - rooms by its size and wealth;
  - cattle by what it bred and inherited;
  - stores by its last harvest;
  - all placed on the built parcel's ground (D2-154), with the parcel sized to them.
- **Capacity in the loop:** after the graph is made, read `engine.capacity.node` (the engine's own function, never a copy) for each
  village. Adjust what is unpinned (a plot more or less, a wood managed or wild) by bisection until the village is in band; refuse
  only if the unpinned land cannot do it, naming the pin that stops it. The band should be wider than one plot's step for small
  villages, or set in plots, not shares.
- **A history in equilibrium gives the band naturally:** a village that has lived through hard years sits below what its land feeds.
  If stage 2 runs on the land's real yields, the 60 to 70% target becomes a check on the history's calibration, not a number forced
  onto the present.

### What stays

- Stage 1 as built: the mesh, water, soil, terrain, ecosystems, keyed draws, roads by least cost, the vocabulary.
- The checks' kinds (D2-180), the economy checks, descriptions written once.
- `generate.py`'s good parts: years mapped to days by stage knots (D2-153), memories written from each person's position, ties.

## 5. Order of work (each a step that pays on its own)

*Revised 14 Nov:* step 2 becomes the present population as an input (an explicit list or a mix) with the genealogy built backward
(§4a), before any forward history. Step 3 becomes the decision graph (§4b), starting with the people: households, parents and
sibships are the decisions most often edited for test conditions.

1. **Capacity in the loop** (stage 3's bisection, with the engine's `capacity.node`) and **write refused worlds with their report.**
   Small, in settle.py and write.py. It should end the seed search today (31 of 36 refused).
2. **Households, not lines, and one regional marriage market** in generate.py; no bare off-map places. Medium.
3. **The history loop with the climate's years and land-fed demography,** founding dates per village, daughter villages. Medium to
   large: stage 2.
4. **Clearing from the history,** replacing the rings and the woodland dial; houses, herds and stores from households. Large.
5. **Split write.py by stage;** a declared table of words to primitives; pins on rivers, fords and roads by name.

## Why

- Every refusal or seed search Zach has hit in the land traces to item 2.1 or 2.2; every complaint about samey worlds to 2.3 or 2.4.
- In people: villages with no kin between them, everyone newly arrived, kin in places that do not exist. Those are the lineage's
  structure (3.2 to 3.5), not its numbers.
- A history makes the present explain itself: why this village is big, why that one is short of wood, why these two families feud
  and those two intermarry. That is what agents read as their world's past, and what the scenario rules ask for (dependence between
  villages, leverage from history).

## Alternatives considered

- **Keep the pipeline, widen the band and retry seeds automatically.** Cheapest, but it hides the two-model drift and is the seed
  search D2-173 rejected. It also does nothing for the lineage.
- **A constraint solver** (answer set programming, as generator.md §9 lists) for the discrete layout: good for small combinatorial
  pins (which household holds which field), poor for stochastic demography and continuous land. Worth it later inside stage 3, not
  as the frame.
- **Full Dwarf Fortress style history** (centuries, cultures, wars): more than the runs need. The proposal keeps to households,
  land and weather over one to two centuries.
- **Generate people first, then land around them** (each household's needs set its land). Simple, but it loses the land's say in
  where and how big villages are: the reverse of the original idea.

## Open questions (for Zach)

*Answered 14 Nov in conversation, not yet decided:* the present population is pinned and the past is backfilled (it replaces
question 2's framing: the age mix is part of the pinned present).

1. **How long a history:** 80 years (two to three generations, cheap) or 200 (old villages, extinct lines, daughter villages)?
2. **Age structure:** realistic by default with "mostly working adults" as a world's choice, or the other way round?
3. **Kin between villages:** wanted as the default (it creates ties and dependence), or only when a world asks?
4. **Off-map places:** should a world that wants outside spouses or migrants have a named off-map node they come from, or should all
   marriages stay within the map?
5. **Who builds what:** stage 1 and 3 are 37.2's (the generator), stage 2 sits between 37.2 and 37.4 (generate.py is 37.4's). One
   owner for the history loop would keep it from being split across two sessions.

## History

- **14 Nov 2026:** proposed by the c2viz session at Zach's request, from a reading of `landgen/` and `engine/generate.py` on main
  (`45ea678`) and the peoples-worlds branch. Measured: 36 worlds generated (31 refused); the allocator and the engine's capacity
  compared on a refused world; 400 lineage histories; kin and origins in a passing world.

- **14 Nov 2026 (later):** revised with Zach: the present population is an input and the past is built backward to fit it (§4a);
  generation is a graph of keyed decisions that fills to the conditions, backtracks on conflict and remakes only what a change
  touches (§4b). The forward history of stage 2 is kept as the model that weighs choices.

- **14 Nov 2026 (third):** §4c with Zach: the land, its use and capacity kept apart; the land is never fitted to people; capacity is
  measured with the full capacity package (D4-102), not fitted by one lever; approaches compared (measure only, one lever, siting as
  matching, livelihoods by affordance, dependence by design); recommended siting, livelihoods and a dependence profile, with
  measure-only as the fallback.

- **14 Nov 2026 (fourth):** §4d with Zach: richness, one upstream productivity field (world and places) that every food source reads
  through a declared, monotone transfer function within its terrain's range; tunable by value or by a target capacity (bisection on
  one number); kept apart from use and from the level of practice.

## Sources

- generator.md (D2-173 to D2-175, §2 to §5, §9), generator_stage1.md, temperate_landscapes.md (D2-191), land_kept.md (W-25).
- Code: `cybertron2/landgen/settle.py` (allocate, targets), `cybertron2/landgen/write.py` (_generate, checks),
  `cybertron2/engine/capacity.py` (node), `cybertron2/engine/generate.py` (simulate, build).
- OPEN L-75 (lakes and the heat target), L-101 (the generator's spec), Q-28 (the economy check); WORK W-9, W-11, W-25, W-34.
- c2viz notes: 3 Nov gallery (75 of 75 built parcels overfull; 17 of 18 worlds at 30% wood), 8 Nov (1 of 16 seeds passed).
