---
id: docs/cybertron2/proposals/environment_systems.md
kind: proposal
state: discussion (16 Nov). Nothing decided, nothing to build.
owner: "37.2"
updated: "2026-11-17"
tags: [proposal, closed]
---
# Environment systems: the land at three speeds, on the places the engine already has

- **state**: discussion (16 Nov). Nothing decided, nothing to build.
- **owner**: 37.2
- **summary**: the land the engine reads (rain by place, wet ground, height above the river, soil water, exposure, slope, water types), eight physical stocks (soil water, snow, river level on reaches, standing water, ice, fuel dryness, loose soil, silt and cleanness), floods, droughts, freezes, wildfire and erosion as thresholds of them, the interactions as one graph, fish groups by water type; in four phases

## Text
# Environment systems: the land at three speeds, on the places the engine already has

**Status:** partly accepted: [[D2-221 The land in three speeds|D2-221]] (three speeds), [[D2-222 The environment's places|D2-222]] (places), [[D2-223 Spread only through defined spread functions|D2-223]] (spread functions), [[D2-224 Events emerge from the stocks|D2-224]] (events from stocks), [[D2-225 The environment's order|D2-225]] (order), [[D2-226 Floodplains in the generator, now|D2-226]] (floodplains now), [[D2-227 Some places are harsher|D2-227]] (harsher places), [[D2-228 Calibrate across a distribution of worlds|D2-228]] (calibration across worlds), with [[D2-214 Two clocks|D2-214]] (two clocks); (6) the frequencies still open (17 Nov). Nothing built yet.
**Owner:** 37.2 (design, the generator, the wild layer); 37.4 (the engine).
**Affects:** spec/environment/ (scheduler.md, resources.md, a new file for the land's stocks); spec/world/generation.md;
`engine/climate.py`, `engine/renewal.py`, `engine/night.py`, `engine/farm.py`, `engine/roads.py`, `engine/forests.py`,
`engine/signs.py`, `wild/areas.py`, `wild/ecology.py`, `landgen/write.py`.

## Summary

Zach (16 Nov): "What are the general gaps between what the engine sees and the world generated, and what interactions between the
environment are currently missed ... general systems, like can we support floods etc, and the interactions"; then: "do a
consolidation for what you think is the best combination of them, considering that there should be slow and fast loops, and how
things will interact. Will some things spread or average across adjacent parcels? What is the relationship between land points and
parcels? And nodes?"

Several designs have touched this, and none is built beyond the fixed land fields and fertility:
- **the land at three speeds** (37.2 to 37.4, 8 Nov, agreed by Zach in principle, never recorded as a decision): fixed, slow, fast;
- **five layers on four clocks** (02zp §4): ground, conditions, vegetation, populations, uses; day, season, year, decades;
- **shared hidden state** (environment_state.md, [[L-23 Water as a need, and the land's hidden state (water table, wells,|L-23]]): variables that relax to a baseline, move one step a day, and cascade;
- **the scheduler** (spec/environment/scheduler.md, [[D2-69 The scheduler's layers|D2-69]] to [[D2-79 Windfalls have no rule of their own|D2-79]]): external change drawn from the seed; hazards and incidents;
- **the engine's clocks** (process_model.md, [[D4-103 The engine overhaul goes ahead, in phases|D4-103]]): every rate names its clock (day, year, life);
- **the land fields** ([[D4-112 The land's base fertility, multiplicative|D4-112]], [[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]): written to every generated world, and a hook that hands each stock's rule the weather and
  the land. Only base fertility is read;
- and, before all of these, **environment_state.md's layers below people's reach** (23 Oct: groundwater per node, the river on its
  water parcels, floods spreading from them lowest first), **generator.md's world under the graph** (3 Nov: the mesh as ground truth,
  floods by height, each cell's exposure to hazards, only physics that ends in leverage), **38.04's hidden quality and signs** (22 Oct),
  and the engine overhaul's **hooks** (7 Nov: hazards read named state variables). The whole history is in 02zzl §4.

**The consolidation:**
1. **Three speeds** are the spine: fixed land, slow stocks (years), fast stocks (days). Each speed reads the slower ones as its
   parameters and writes to them by small amounts, so there are fast loops (a wet week, a flood) and slow loops (a cleared valley
   floods worse for years) and the coupling between them (§2, §3).
2. **The places the engine has are enough, each with one job** (§1): the cells hold only fixed land and feed everything else
   when a world is made; parcels hold the stocks of the land people work; the wild layer's areas hold the stocks of land no one
   holds, and string the rivers into reaches; nodes hold the weather and the snow. Nothing new is stepped on the cells.
3. **Nothing spreads by default** (§4). Things move between neighbours only along three named channels: downhill and
   downstream (water, silt, fouling), adjacency (fire, colonisation by plants, pests), and the areas' links (animals, disease).
   Nothing averages across parcels.
4. **Events are thresholds of the stocks** (§5): floods, droughts, freezes, wildfire's spread and erosion emerge; the scheduler
   draws the weather and the true externals (ignitions, hail, pestilence), as [[D2-71 Risks attach to things|D2-71]] allows.
5. **People's acts write the same stocks** (§6), and **people see bands through signs**, never numbers (§7).
6. **Built in phases** (§9): read the fixed land; then the water; then cover and fire; then soil, silt and conditions.

## The proposal

### 1. The places, and how they relate

| Place | What it is | Size | Holds |
|---|---|---|---|
| **Cell** (a land point) | the generator's grid, kept with the world ([[D2-208 The world keeps the land it runs on|D2-208]]) | 150 m, about 2 ha; one unit of parcel size ([[D2-181 (Roads and region amended by D2-182.)|D2-181]]); about 110,000 in a 50 km window | **fixed land only**: height, slope, flow direction and area drained, river class, height above the river, soil texture and depth, rain, wetness, exposure, temperature |
| **Parcel** | a connected group of cells of one use, held and worked by a node's people | a few to a few dozen cells (`size` = its cells) | the land's **slow and fast stocks** for worked land; claims, works, buildings |
| **Node** | a place one can reach and return from in a day ([[D4-2 A node is a village, a valley or a camp|D4-2]]): its parcels, its people, its roads | worked land within 2.5 km (`field_km`) | the **weather** (climate.py by node), **snow**; signs and people |
| **Area** (the wild layer) | every cell is in exactly one: a node's **home** (its parcels' cells), its **ring** (unheld land within 2.5 km), or a **wild** block (about 8 km) | home: the parcels; ring: a few km²; wild: tens of km² | the slow and fast stocks of **land no one holds**; wild populations; **rivers as reaches** (river-bearing areas strung on `down`) |

**How they relate:**
- **Cells to parcels and areas:** each cell is in one area; a held cell is also in one parcel. When a world is made, a parcel's
  and an area's fixed values are summaries of their cells (means, shares, the lowest point, the length of river). This already
  happens for most fields (`land:` per parcel, area fields in wild/areas.py).
- **Parcels to nodes:** each parcel belongs to one node and lists its neighbours there (`adj`); a node's parcels make its home area.
- **Nodes to nodes:** roads in days (edges); the weather is correlated between near nodes ([[D4-111 Every weather query names its place; the senses read the day's|D4-111]]).
- **Areas to areas:** shared edges (`links`, with their length) and the downstream link (`down`).
- **Parcels to areas:** a node's parcels touch its ring (the unheld land around them), and through it the wild. Fire, plants and
  beasts cross there.

**Only physics that ends in leverage** (generator.md §7, 3 Nov): every stock here must end in a difference people feel and can
act on (who floods, whose well fails, which field dries), or it is left out.

**Why the cells are not stepped.** Every stock an agent can see or act on is about a parcel, a stretch of river, a node or a
stretch of wild. Stepping 110,000 cells adds detail no one can see and a much larger daily state to save and replay. The cells
stay the source of the fixed land, are loaded when a world needs a new summary (a parcel cleared out of the ring, a new field,
[[D2-208 The world keeps the land it runs on|D2-208]]), and drive c2viz. This is the environment's answer to [[Q-50 One grid or several|Q-50]]: parcels and areas as the grids, cells as their source.

### 2. The three speeds

Each row is a quantity, on the place that holds it, with its clock (process_model.md: every rate names its clock).

**Fixed** (generations; changed only by works and by the slow stocks' rare large events):

| Quantity | Where it comes from | Status |
|---|---|---|
| elevation, exposure, position (hollow, slope, ridge) | cells | written (`land:`), unread |
| slope | cells | in text and ranks only; to write as `land.slope_deg` |
| soil texture as water held (`held_mm`) and drainage (`drain_rate`), soil depth | cells | written, unread |
| base fertility (nutrients) | cells: texture × silt × height | written, read ([[D4-112 The land's base fertility, multiplicative|D4-112]]) |
| rain factor (the parcel's rain over its node's), node normal rain (`rain_mm`) | the wind sweep | written, unread (the climate rains from one number) |
| flow direction (`down`), river class, sea distance | cells | written; `down` unread (brief 5 reads it) |
| height above the river | cells' `f` | to write as `land.above_river_m` |
| water type (§8), springs, falls, fords | cells | to write |

**Slow** (the year clock, stepped at the season's turn; moved by use, by the ecology and by the fast stocks' events):

| Quantity | On | Moved by | Read by | Status |
|---|---|---|---|---|
| **fertility** (base × offset) | parcel | crops and hay take; dung, fallow and grazed stubble give; flood silt gives; erosion takes | yields | built ([[D4-112 The land's base fertility, multiplicative|D4-112]], farm.py) |
| **wetness offset** | parcel, area | drains and ditches lower it; dams, weirs, beavers and silted channels raise it | soil water's capacity and drainage; flood depth; which plants and covers suit | agreed 8 Nov; not built |
| **vegetation** (canopy, shrub, field-layer shares; the cover follows from it) | parcel, area | growth toward what the conditions suit (succession), grazing, mowing, felling, burning, colonisation from neighbours (§4) | forage, fuel load, runoff and erosion, sight, the wild kinds' habitat | agreed 8 Nov as `vegetation`; covers and woods built (forests.py); the shares not built |
| **soil depth** | parcel, area | erosion takes; nothing adds within a run | water held (`held_mm` scales with depth), yields | not built |
| **channel silt** | reach, leat | erosion upstream adds; spates scour | spawning gravel (the salmon's return), the mill's leat, flood height | not built (the leat silts on a fixed one-year clock) |
| **conditions** (nitrogen, acidity, light; 02zp layer 2) | parcel, area | dung and folding, burning, canopy | which field-layer plants come | proposed in 02zp; optional, last |

**Fast** (the day clock; one stock, one rule each, in the parcel's or the area's `state`, read through [[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]'s hook):

| Quantity | On | Fills from | Empties by | Status |
|---|---|---|---|---|
| **soil water** | parcel, area | rain × rain factor, snowmelt, standing water | evaporation by warmth and season; drainage at `drain_rate` (ditches faster); overflow runs off downhill (§4) | agreed 8 Nov; the wild layer has a bucket from rain alone |
| **snow** (depth) | node, adjusted by a parcel's height and exposure | snow days | melt by warmth and rain, into soil water and runoff | agreed 8 Nov; built as a flag ("snow lies") |
| **river level** (river flow) | reach | its area's runoff, plus the reach above's outflow a day or so later | outflow downstream | agreed 8 Nov; not built |
| **fuel dryness** | vegetated parcels and areas | dry days, warmth, wind | rain, snow, spring growth | agreed 8 Nov; not built |
| **standing water** | low parcels and areas on a reach | a flood over their height above the river | the falling river; soaking in | new |
| **ice** | still water, slow reaches | frost degree-days (faster when shallow and still) | thaw, rain, a spate | new (the wild layer counts frozen nights) |
| **loose soil** | parcels, areas | ploughing, clearing, burning, overgrazing, a flood's scour | cover growing back over the season | new |
| **cleanness and turbidity** | reach | erosion, floods, fouling trades and middens (later) | flushed by flow | new |

Buildings, herds and people keep their own hidden variables (damp, condition, sickness, filth) in environment_state.md, with the
same mechanics: a baseline, a rate, one step a day.

### 3. The loops: fast, slow, and between them

**The update order each day** (after the weather, before people act; environment_state.md §3): fixed land is read; fast stocks
step from yesterday's values; events are tested (§5); at the season's turn the slow stocks step from the season's fast history (its
sums and extremes). So a fast change reaches a slow stock at the next season's turn, and a slow change reaches the fast stocks the
next day. No loop closes within a day.

**Fast loops** (days to weeks):
- rain → soil water → runoff → the reach's level → spate and flood → standing water → soil water;
- dry days → soil water and river low → crops and grass stressed, the mill slow, fish crowded → fuel dry → fire → bare ground;
- frost nights → ice → fishing shut, crossings open → thaw and rain → spate.

**Slow loops** (years):
- **clearing and ploughing a slope** → vegetation down → more runoff and loose soil → erosion → soil depth and fertility down
  here, channel silt up below → floods higher and spawning gravel choked → fewer salmon a year on;
- **draining a wet meadow** → wetness offset down → pasture up, eels and fowl down;
- **dung and folding** → fertility and nitrogen up on the arable, down on the down (the sheep-corn system, 02zp L2);
- **abandonment** → vegetation succeeds (weeds, scrub, wood) → fuel and game change, a ruin read in the plants (02zp L12);
- **grazing and burning heath** → vegetation held open (02zp L1, L9).

**Between the speeds:**
- a **flood** (fast) lays silt (fertility up, slow) and scours (loose soil, fast; soil depth, slow); a **big fire** (fast) resets
  vegetation (slow); a **drought year** (a season of fast lows) sets back vegetation and raises dead fuel;
- the slow stocks set the fast stocks' parameters: vegetation sets interception, runoff and fuel load; the wetness offset sets
  soil water's capacity and drainage; soil depth sets the water held; channel silt sets the river's flood height.

### 4. What moves between neighbours (and what does not)

Nothing spreads or averages across parcels by default. Lateral effects travel only along three named channels, one step a day:

| Channel | Along | What travels | Rule |
|---|---|---|---|
| **Down** | the land's flow (`land.down` for parcels; areas' `down`; reaches) | runoff, flood water, silt, fouling, ice breaking up | directed, never back up; a parcel's overflow goes to its `down`, a reach's outflow to the next reach after its lag |
| **Adjacency** | parcels' `adj`, a node's parcels to its ring, areas' `links`; between nodes along edges as [[D2-72 Fires spread with the node's conditions, and between nodes|D2-72]] allows | fire (by dryness, wind, cover), colonisation by plants (scrub and wood seed into a neighbour; an old field next to a wood goes to wood faster), pests | a chance per neighbour per day, by the shared edge's length and the receiver's state; spreads, never averages |
| **Links** | the wild layer's area links | beasts, disease (built: wild/ecology.py, diseases.py) | as built |

**Floods, lowest first.** environment_state.md (23 Oct) had floods spread from the water parcels by adjacency, lowest neighbours
first (the meadow, then the fields, then the houses on the bank). Height above the river (§2) makes that exact: a flood reaches
every parcel on the reach lower than its excess, so the order is the land's own, and no adjacency walk is needed.

**Groundwater** (23 Oct: one aquifer per node, parcels higher or lower on it, wells failing before the river in a drought) is a
slow stock on the node when wells come (§9, later), fed by its parcels' soil water and drained by its springs and the river.

**Not lateral:** fertility (it moves only with dung, hay, silt and erosion, all carried), soil water (only by runoff down),
snow (by height and exposure, not by drift), frost (a hollow's colder night is a fixed property of its position, not a flow of
cold air). This keeps the model directed, cheap and traceable: each lateral effect is a flow with a source and a route.

### 5. Events as thresholds of the stocks

| Event | When | Effect | Scheduler ([[D2-77 The first-world set|D2-77]]) |
|---|---|---|---|
| spate | a reach's level in its spate band | fords shut; fishing poor; gear worn; the runs' cue | emerges |
| flood | a reach over its banks (raised by channel silt) | standing water on parcels lower than the excess; low houses damaged (replacing night.py:593's label rule); hay, crops and stores lost; silt laid; mills and weirs damaged | "river flood" and "flood silt", emerging |
| low water, drought | a reach low, or soil water low, for some days | crops and pasture stressed; the mill slows; brooks dry; fish crowd; fords easy | "drought", emerging |
| freeze | ice past a thickness | fishing through holes only; crossings on the ice; fowl to open water; long ice: winterkill | emerges (replaces the frozen-night proxy for water) |
| wildfire | a drawn ignition (lightning) or a hearth or a burning by people, on dry fuel | vegetation and fuel burnt; spreads by adjacency (§4) | "wildfire": ignition drawn, spread physical |
| erosion | heavy rain on loose soil on a slope | soil depth and fertility down; silt down the flow | emerges |

Hail, late frost, blizzard, lightning, blight, murrain and pestilence stay drawn by the scheduler, with these stocks as their
exposure term ([[D2-69 The scheduler's layers|D2-69]]).

### 6. What people do to the land (the uses layer)

Most acts exist; each writes a stock: **felling and clearing** (vegetation, loose soil), **ploughing** (loose soil), **grazing and
folding** (vegetation, fertility, dung), **mowing hay** (vegetation, fertility), **ditching** (built, [[D2-66 Field works in the first worlds, before weather exists|D2-66]]: drainage, the wetness
offset), **burning heath** (vegetation, fuel), **dams, weirs and the mill** (brief 5: a reach's level above and below; the wetness
offset above), **coppicing** instead of clearing (vegetation kept), and later **banks** (standing water held off a parcel and sent
elsewhere), **firebreaks**, **wells** and **middens** (cleanness; environment_state.md §8, §9).

### 7. What people see

Signs by band, as bundles of senses (guides/senses.md), for changes: "the river up and brown, over the lower stones"; "over the
meadow at dusk"; "the brook down to a trickle"; "ice you could walk on"; "the bracken brittle, the grass white"; "the plough lands
washed into the hollow"; "the leat choked with silt". Skill reads the low bands first. Upstream warns downstream: a spate reaches
the village below a day or two after the one above, so a traveller's word is worth carrying. Every band has an act that answers it
(move hay and stores, reap early, open a gap, ditch, bank, cut a firebreak, cross on the ice, cut a hole and fish).

### 8. Waters (one part of the fixed land)

The generator writes each water parcel's **type** from its cells: brook, upland beck, lowland river, large river, lake or mere,
tarn, fen water, pond (estuary and coast later, with boats). The type sets how fast it freezes, how it floods (flashy or slow and
wide), whether a weir or a mill fits, and which **fish groups** it holds: the shallows (by hand, small traps), the resident fish
(rod, net, spear), the runs (brief 5's kinds), and competitors (otter, heron, pike, eating from the same stocks). The village's
fish and the wild layer's fish become one stock. Falls, fords and springs sit on water parcels as sites.

### 9. Phases

| Phase | What | Tests |
|---|---|---|
| **0: the fixed land read** | rain by place; `ground` from the generator's wet ground (farming reads it, [[D2-66 Field works in the first worlds, before weather exists|D2-66]]); exposure and position into frost and wind; slope, height above the river and water type written. Behind a world setting, so older worlds and replays stay exact | rain shadows and wet ground show in yields; nothing changes with the setting off |
| **1: water** | soil water, snow depth and melt, river level on reaches, spate, flood, standing water, low water, ice, winterkill; the wetness offset; fish groups by water type | a wet week floods the lower village's meadows a day after the upper's; a dry month stops the mill; a freeze closes the traps and opens the crossing; draining raises a meadow's grass |
| **2: cover and fire** | the vegetation shares and succession, colonisation by adjacency, fuel dryness, wildfire with drawn ignitions and spread, heath burning | a dry windy spell carries fire across the heath and not over the river; an old field beside a wood goes to scrub |
| **3: soil and silt** | loose soil, erosion, soil depth, channel silt, cleanness and turbidity; then the conditions layer if it earns its place | clearing the slope above a river thins its salmon and silts the leat downstream within a few years |
| **later** | water table and wells; buildings', herds' and people's hidden variables (environment_state.md, [[L-23 Water as a need, and the land's hidden state (water table, wells,|L-23]], [[L-9 Disease (mortality, the sick, immunity, nursing, a healer); rot's|L-9]]) | |

Each phase passes dry runs and a null arm (the same world with the phase off), and its signs are read in agents' reasoning: are
they acted on?

### 10. What keeps it small

- About fourteen quantities in all, each one number on a parcel, an area, a reach or a node; a few lines of rule each.
- No hydraulics and no cell stepping: a reach is a bucket with a lag; a flood's reach is a height.
- Slow stocks step at the season's turn; fast stocks once a day; nothing loops within a day.
- Compressed time is stated as such (a 32-day year): a spate in a few days, a dry spell in a week or two (calibrate).
- The prompt gains only signs, plus a bank and the fire acts.
- Inside the border (02zzk): the medieval village and its river.

## Why

- Zach (16 Nov): general systems, floods and their interactions; then a consolidation with slow and fast loops and the spatial
  relations.
- The generator's land is mostly unused (02zzl §1), and the agreed fast stocks (8 Nov, [[L-71 The land's fast stocks|L-71]]) and slow stocks were never built.
- The decided hazards ([[D2-77 The first-world set|D2-77]]) have no state to read; [[D2-71 Risks attach to things|D2-71]] says incidents also emerge from the systems.
- Shared shocks and slow degradation make dependence and quarrels (scenario_design §1): who holds the high ground, the stores, the
  mill and the crossing; who upstream sends floods and silt to those below; the woods and the river as commons.

## Alternatives considered

- **Step the cells** (a fast stock on each of 110,000 cells, water routed cell to cell): finer floods and fires, but detail no agent
  sees, and a much larger state to save and replay. The cells stay the source.
- **Floods and droughts as drawn incidents** ([[D2-77 The first-world set|D2-77]] as it stands): cheap, but blind to the land and to people's acts.
- **Diffusion between all neighbours** (averaging soil water, fertility or snow): simpler to write, but it smears the differences
  the land makes and hides cause; directed flows along named channels keep cause traceable.
- **One wetness number per node:** too coarse to put the flood on the meadow and not the hill field.
- **Leave it to environment_state.md:** kept for buildings, herds and people; the land needs its own design.

## Open questions (for Zach)

1. **Record the three speeds** (fixed, slow, fast; 8 Nov) as a decision, with this proposal's list as their content?
2. **The places:** cells only as the fixed source; parcels and areas hold the stocks; reaches are areas on `down`; nodes hold the
   weather and snow (the environment's answer to [[Q-50 One grid or several|Q-50]])?
3. **Spreading:** only along down, adjacency and links; nothing averages?
4. **Emerging events:** floods, droughts, freezes, erosion and fire's spread from the stocks; the scheduler draws the weather and
   true externals?
5. **Order:** phase 0 now with brief 5; then water; then cover and fire; then soil and silt?
6. **How often** under the compressed year: spates once or twice a year in a wet lowland, a meadow flood every year or two, a hard
   freeze every few years, a dry spell most summers? (Measured in 02zzn: on two clocks, close to this except the freeze.)
7. **Two clocks:** decided, [[D2-214 Two clocks|D2-214]].
8. **Floodplains** (02zzn §3.1): fix the generator's valley floors now, which remakes brief 5's worlds while 37.4 builds on them,
   or after brief 5's build?
9. **Ice** (02zzn §3.3): frozen waterways need a colder base climate in the generator (upland or northern worlds); is that wanted?

## History

- 17 Nov 2026: Zach answered [[Q-52 Environment systems|Q-52]]: (1) to (5) yes ([[D2-221 The land in three speeds|D2-221]] to [[D2-225 The environment's order|D2-225]]; spreading "through defined spread functions"); (8) fix the
  floodplains now ([[D2-226 Floodplains in the generator, now|D2-226]]); (9) some places harsher ([[D2-227 Some places are harsher|D2-227]]); and calibrate across a distribution of core test worlds, expected to
  differ ([[D2-228 Calibrate across a distribution of worlds|D2-228]]). (6), the frequencies, explained and still open.
- 16 Nov 2026 (night, later): Zach decided two clocks ([[D2-214 Two clocks|D2-214]]): day schedules on the engine day, the seasonal stocks scaled by
  the year's length. [[Q-52 Environment systems|Q-52]] (7) closed. He asked for the weather tested across conditions (dry, mountains, floodplains, coast).
- 16 Nov 2026 (night): the water half prototyped offline on brief 5's river world (02zzn, script and results beside it). Findings:
  - the generator makes no floodplains (rivers lie in a cut one cell wide, 14 to 24 m deep), so floods by height reach no parcel;
  - on one clock the seasonal loops never happen;
  - on two clocks (seasonal stores at 365 ÷ year days a day, the weather's events at one day) the river has a year;
  - ice comes only from cold snaps and hardly at all in lowland worlds;
  - clearing upstream is a weak loop at the scale of a large river;
  - a weir's yearly wear is about 1.25 × normal flow on one clock and 2 to 3 × on two.
  Added [[Q-52 Environment systems|Q-52]] (7) to (9).
- 16 Nov 2026: written by 37.2 at Zach's request, after the waters discussion, widened to the whole environment (02zzl's
  inventory).
- 16 Nov 2026 (later still): Zach asked for a survey of every earlier consideration of hidden state ("we first considered hidden
  state ages ago, with water level"). Surveyed both repositories' histories back to 22 Oct (02zzl §4). Added what the consolidation
  had missed: floods lowest first (environment_state.md, 23 Oct) made exact by height; groundwater per node for wells; only physics
  that ends in leverage (generator.md §7, 3 Nov); the earlier designs named in the summary.
- 16 Nov 2026 (later): rewritten as a consolidation, after Zach asked whether the land's quantities at different speeds had been
  specced before. They had: the three speeds agreed on 8 Nov (37.2's message to 37.4; cited in base_fertility.md, [[L-71 The land's fast stocks|L-71]]), 02zp's five
  layers and four clocks, environment_state.md, the scheduler spec, process_model.md's clocks. The first draft had re-derived the
  agreed fast stocks and left out the slow layer. Added: the three speeds as the spine with each quantity's status and clock (§2);
  the loops within and between speeds (§3); the places and how they relate (§1); what moves between neighbours (§4).

## Sources

37.2's message to 37.4 of 8 Nov (the three speeds; this session's record); docs/review/37_growth/02zzl_environment_gaps.md (§4, the history); review 38.04 (places design); generator.md (§2, §7; [[D2-173 The generator fills in around what a world file gives|D2-173]], [[D2-174 A world under the graph|D2-174]]); 02q_environment_model.py; engine_overhaul.md;
02zp_ecosystems_deep_dive.md §4 (layers and clocks), §15 (the land fields), §16; proposals/environment_state.md, base_fertility.md
([[D4-112 The land's base fertility, multiplicative|D4-112]]), weather_scheduler.md ([[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]), process_model.md ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]] clocks), ecosystems.md, wild_systems.md, wild_layer.md §3.10,
land_kept.md ([[D2-208 The world keeps the land it runs on|D2-208]]), river_and_water.md ([[D2-209 Brief 5 (river and water) is built|D2-209]]), environment_catalogue.md, crop_growth.md, building_risks.md;
spec/environment/scheduler.md ([[D2-69 The scheduler's layers|D2-69]] to [[D2-79 Windfalls have no rule of their own|D2-79]], [[D4-5 Three time scales|D4-5]]); landgen/vocab.py (the cell, [[D2-181 (Roads and region amended by D2-182.)|D2-181]]); wild/areas.py (home, ring, wild,
links, down); OPEN [[L-21 Fire house fire and wildfire in the scheduler, spreading along th|L-21]], [[L-23 Water as a need, and the land's hidden state (water table, wells,|L-23]], [[L-48 What can happen to buildings and fittings, by weather and use|L-48]], [[L-68 Crops grow by the weather, not only the season|L-68]], [[L-71 The land's fast stocks|L-71]], [[Q-50 One grid or several|Q-50]]; guides/senses.md; docs/scenario_design.md §1; 02zzk (the border).

