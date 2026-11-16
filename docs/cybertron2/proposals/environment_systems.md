# Environment systems: the land the engine reads, a few physical stocks, and the events and interactions they give

**Status:** discussion (16 Nov 2026). Nothing decided, nothing to build yet.
**Owner:** 37.2 (design, the generator, the wild layer); 37.4 (the engine).
**Affects:** spec/environment/ (scheduler.md, resources.md, a new file for the stocks); spec/world/generation.md; on the code side
`engine/climate.py`, `engine/renewal.py`, `engine/night.py`, `engine/farm.py`, `engine/roads.py`, `engine/forests.py`,
`engine/signs.py`, `wild/areas.py`, `wild/ecology.py`, `landgen/write.py`.

## Summary

Zach (16 Nov): "What are the general gaps between what the engine sees and the world generated, and what interactions between the
environment are currently missed. This should aim for general systems, like can we support floods etc, and the interactions."

The gaps (02zzl, an inventory of the code on `main`, 16 Nov):
1. **The generator makes a land the engine barely reads.** Rain shadows, which way water runs, height above the river, how much
   water a soil holds and how fast it drains, exposure, slope, springs and wet ground are all in the world file, and no process
   reads them. The engine rains from one global number, and the cells (D2-208) are never loaded.
2. **The weather touches things directly, never through the land.** Frost, snow, gale and heavy rain act on crops, houses and
   fords as labels for the day. Nothing accumulates. There is no soil water outside the wild layer, no river level, no ice, no
   fuel dryness, no loose soil, no water quality. So there are no floods, droughts, wildfires, erosion or winterkill, and the
   decided hazards (D2-77: drought, river flood, wildfire and others) have nothing to read.

The proposal:
- **Read the land the generator already makes** (§2). Small changes, and every later system rests on them.
- **Add a few physical stocks** that the weather fills and drains each day, and that run over the land's own graph (§3): soil
  water, snow, river level, standing flood water, ice, fuel dryness, loose soil, and the river's silt and cleanness.
- **Make floods, droughts, freezes, wildfires and erosion thresholds of those stocks** (§4), so they emerge from the drawn weather
  and from what people did to the land, as D2-71 allows ("incidents also emerge from the systems"). The scheduler keeps drawing
  the weather and the truly external events.
- **Name the interactions as one graph** (§5), with people's works (ditches, banks, felling, ploughing, dams, middens) writing the
  same stocks.
- **Give waters a short list of types** (§6), as woods have, with the fish groups, freezing and floods that follow from each.
- **Build it in phases** (§8), water first, alongside brief 5.

This is the physical-process half of environment_state.md (shared hidden variables that interact; flagged L-23). That proposal's
variables for buildings, herds and people stay there.

## The proposal

### 1. Principles

1. **The land is the substrate.** A process reads the land's fixed properties (D4-112, D4-113's hook) before it reads the day's
   weather. Two places under the same sky differ because their land differs.
2. **Few stocks, each with one rule.** A stock is a number on a place with sources, sinks and a rate. Its rule runs once a day in a
   fixed order, reading yesterday's values (environment_state.md §3), so effects travel one step a day and there are no same-day
   loops.
3. **Events are thresholds, not dice.** A flood is the river above its banks; a drought is soil and river low for long enough; a
   freeze is ice thick enough. The scheduler draws the weather (D4-4: the same in every arm) and the few truly external events
   (lightning, hail, pestilence). What follows is physics, and people's acts change it (clearing, draining, damming).
4. **Kinds are short lists; state is continuous.** A water's type, a soil's texture and a parcel's position are named kinds.
   Levels are numbers, and people see them in graded bands through signs, never as numbers.
5. **Every effect is something to act on.** Agents ignored forecasts they could do nothing about (guides/senses.md). A rising river
   matters when there is hay to move, a gap to open or a bank to raise.
6. **The grids already there are enough.** Parcels hold ground stocks (soil water, cover, fuel); river reaches are the wild
   layer's areas strung on `down`; still waters are their water parcels; snow lies by node. The cells stay with the generator and
   c2viz, except where a world needs them loaded (D2-208). This is one answer to Q-50 for the environment.

### 2. Reading the land the generator makes (no new stock)

| The land holds | Written now as | Read for |
|---|---|---|
| Rain by place (wind and rain shadow) | node `rain_mm`, parcel `land.rain_factor` | the climate's rain at a node scaled by its normal (now one global number, climate.py:251); a parcel's share of it |
| Which way water runs | parcel `land.down`, areas `down` | river reaches (§3.3); downstream fouling and silt; the runs (brief 5 reads `down` already) |
| Height above the river | the cells' `f`, only as parcel `height` 0 | a new parcel `land.above_river_m`, so a flood's reach is a height, not a rank |
| Soil's water: how much it holds, how fast it drains | `land.held_mm`, `land.drain_rate`, `land.depth`, `land.texture` | the soil water bucket (§3.1) |
| Wet ground | words only ("wet underfoot", landgen/write.py:141) | the parcel key `ground: wet` that farming already reads (D2-66, farm.ground_mult), written by the generator |
| Exposure, position (hollow, ridge, slope) | `land.exposure`, `land.position` | frost pockets in hollows and wind on exposed ground: the climate's night low and wind by parcel |
| Slope | `height` 2 over 5°; area `rock` | erosion (§3.7); the work cost of ploughing |
| Springs, falls, fords | words; fords as road features | water sources that hold in a drought; falls as a fishing site and a barrier; fords that close in spate |
| A water's type | (not made) | §6 |

Most of these are a few lines each in the generator or the engine. Two change existing worlds' behaviour (rain by place, `ground`),
so they come behind a world setting, and older worlds and replays stay exact.

### 3. The stocks

Each is updated once a day, after the weather and before people act; sources and sinks are from the day before.

| # | Stock | On | Fills from | Empties by | Read by |
|---|---|---|---|---|---|
| 1 | **Soil water** (0 to its `held_mm`) | parcel | rain × `rain_factor`; snowmelt; flood water | evaporation by warmth and season; drainage at `drain_rate` (faster with ditches); what overflows runs off to the parcel's reach | crops' growth and stress (L-68), grass growth (the renewal hook), wild plants, mud and work on wet ground, fuel dryness, waterlogging |
| 2 | **Snow** (depth) | node, and its hill parcels | snow days | melt by warmth and rain | the existing "snow lies" rules by depth; melt into soil water and runoff (spring floods) |
| 3 | **River level** (against its normal) | reach: each river-bearing area on `down` | its area's runoff, plus the reach above's outflow a day later (one day for each 10 to 20 km; calibrate) | outflow downstream; seepage in a drought | bands **dry, low, normal, high, spate, flood**; fords, the mill's power and gap, weirs, the runs' cues, fishing, floods (§4) |
| 4 | **Standing water** (days under water) | low parcels on a reach | a flood over the parcel's `above_river_m` | falls with the river; soaks into soil water | hay, crops and stores lost; houses damaged (replacing the label rule at night.py:593); silt laid (fertility up); fish spread onto meadows |
| 5 | **Ice** (thickness) | still waters first, then slow rivers; big rivers rarely | frost degree-days, faster on shallow and still water (§6) | thaw degree-days, rain, a spate breaking it | fishing access (traps, nets and weirs shut; a hole can be cut), fords and crossings (thick ice carries), fowl driven to open water, winterkill in shallow water under long ice |
| 6 | **Fuel dryness** | wood, scrub, heath, grass and ripe crops | dry days, warmth, wind | rain, snow, green growth in spring | wildfire's spread and odds (§4); heath burning by people; how well cut wood and stubble burn |
| 7 | **Loose soil** (bare and loosened ground) | parcels | ploughing, clearing, burning, overgrazing, a flood's scour | growth of cover over the season | erosion in heavy rain on a slope: fertility and depth lost from the parcel, silt sent to its reach |
| 8 | **Silt and cleanness** | reach, and its water parcels | erosion; floods; fouling trades (tanning, retting, offal, middens; later) | flushed by flow; settles in still water | fish (silt chokes spawning gravel; fouling kills), the leat silting faster, the mill's upkeep; later, people's health (L-9, L-23) |

A water table and wells (environment_state.md §2, §8) would be a ninth stock, deeper and slower than soil water. They wait on water
as a need (L-23).

### 4. Events as thresholds of the stocks

| Event | When | Effect | Its place in the scheduler |
|---|---|---|---|
| **Spate** | a reach's level in its spate band | fords shut; fishing poor in muddy water; a weir's and a set trap's wear; the runs' cues (rain after dry) | emerges (D2-71) |
| **Flood** | a reach above its banks | standing water (§3.4) on parcels below the excess height; low houses damaged; silt laid; a mill or weir damaged by force | D2-77's "river flood" and the windfall "flood silt", now emerging from rain and land |
| **Low water and drought** | a reach low, or parcels' soil water low, for several days | crops stressed, pasture fails, the mill's power falls, brooks dry, fish crowd into pools, fords easy | D2-77's "drought", emerging |
| **Freeze** | ice past a thickness | §3.5; the great freeze regime reads the ice, not only the run of frozen nights | emerges; it replaces the frozen-run proxy where water is concerned |
| **Wildfire** | an ignition (lightning, drawn by the scheduler; a hearth or burning by people) where fuel is dry | the parcel's vegetation and fuel burnt; spreads to neighbours by dryness and wind, and along edges as D2-72 allows | D2-77's "wildfire": the ignition is drawn, the spread is physics |
| **Erosion** | heavy rain on loose soil on a slope | §3.7 | emerges |
| **Winterkill** | long ice on shallow still water | the water's fish mostly dead, found at the thaw | emerges |

Hail, lightning, late frost, blizzard, blight, murrain and pestilence stay drawn by the scheduler as D2-77 has them, with these
stocks as their exposure (D2-69's term).

### 5. The interactions, as one graph

Each arrow runs at most one day. People's acts are in bold.

| From | Through | To |
|---|---|---|
| rain on a catchment | soil water full, runoff, reaches downstream | spate, flood, standing water on the meadows a day or two later downstream |
| snow, then a thaw with rain | melt into runoff | the spring flood |
| dry weeks | soil water and river low | crops and grass stressed; the mill slows; fish crowd; brooks dry; fords easy |
| dry weeks and wind | fuel dryness | wildfire; then loose soil on burnt slopes; then silt in the next heavy rain |
| frost nights | ice | fishing shut or through holes; crossings over the ice; fowl to the open water; winterkill |
| **felling a slope, ploughing, overgrazing** | loose soil | erosion; silt downstream; the leat silts, spawning gravel choked, the salmon run thins years later |
| **clearing woods upstream** | more runoff, faster (less soil water held) | higher spates downstream: an externality between villages (02zzj part 18 §2.5) |
| **ditching a field** (built, D2-66) | faster drainage | less waterlogging; more runoff downstream |
| **a flood bank** (new work) | standing water held off a parcel | the water goes elsewhere: a quarrel |
| **a mill dam or weir** (brief 5) | level held above, flow below | flooding above in spate; less below in drought; the gap decides |
| beaver dam (built) | level held | the meadow flooded, fish up |
| a flood | silt (fertility up), mud | a better crop next year, a fouled well (later) |
| **tanning, retting, a midden by the water** (later) | cleanness down | fish lost downstream; later, flux |
| **burning heath for grazing** | fuel and cover reset | better grass next spring; a fire that runs if the wind turns |
| abandoned field or clearing | cover grows back | weeds, then scrub, then wood (succession, ecosystems.md) |

### 6. Water types (a short list, as woods have)

The generator writes each water parcel's type from what it already knows: river class, slope, lake, fen and sea. Each type is a row
of data:

| Type | From the land | Fish groups (§6.1) | Freezes | Floods | Weir or mill |
|---|---|---|---|---|---|
| brook | stream, a spring above | shallows | fast | flashy, short | no |
| upland beck | small or medium river, steep | shallows, resident (trout), the runs at falls | edges | flashy; scours | falls as a fishing site |
| lowland river | small or medium, gentle | resident (coarse fish), eels, the runs | in long frost | slow, wide, the meadows | yes |
| large river | large class | the runs, resident in deep water | rarely bank to bank | slow, long, wide | a weir; too big for a village mill |
| lake or mere | lowland or fen lake | resident (pike, perch), eels, fowl | slowly; holes can be cut | rises slowly | no |
| tarn | upland lake | few fish | early and long | little | no |
| fen water | fen system | eels, pike, fowl | fast (shallow) | spreads widely | no |
| pond | a feature or made (mill pond, beaver pond, later fishpond) | shallows, eels | fast; winterkill | little | the mill pond is the mill's |

Estuary and coast come with boats. **Features** sit on a water parcel as sites: falls or rapids (where salmon leap: a fishing place
and a barrier), a ford, a spring.

#### 6.1 Fish groups and what reaches them

Each water holds up to four stocks instead of one `fish`, so the gear ladder reaches different fish rather than the same fish faster:
- **shallows** (crayfish, small fish, trout tickled under the bank): by hand and small traps;
- **resident** (the water type's fish): rod, net, spear;
- **runs** (eels down; salmon and lamprey up): brief 5's kinds, at weirs, the mill's race, below a dam, by net;
- **competitors** (otter, heron, pike): the wild layer's kinds, eating from the same stocks.

The village's fish and the wild layer's area fish become one stock, so people, herons and otters compete for the same fish
(02zzl §2: they are separate now). Cold lowers every catch; ice closes the shallows and set gear; low water crowds fish into
pools (easy, then fewer); silt and fouling lower the stocks.

### 7. What people see, and what they can do

- **Signs by band, as bundles** (guides/senses.md): the river "up and brown, over the lower stones" (high), "over the meadow at
  dusk" (flood), "the brook down to a trickle between stones" (low), "ice at the edges, thin" and "ice you could walk on" (freeze),
  "the bracken brittle, the grass white" (dry fuel), "the plough lands washed into the hollow" (erosion). Changes, not standing
  facts; a skilled eye reads the low bands first.
- **Upstream is a warning.** A spate reaches the village below a day or two after the one above, so a traveller or a watcher
  upstream brings warning: information worth carrying.
- **Acts that answer them** (most exist already): move hay and stores to high ground; reap early; open a mill's or weir's gap in
  spate; ditch; raise a bank (new); cut a firebreak or put out a fire (new: the fire acts of L-21); cross on thick ice; cut a hole and
  fish; stint the grazing on a slope; coppice instead of clear.

### 8. Phases

| Phase | What | Needs | Tests |
|---|---|---|---|
| **0: the land read** | §2: rain by place, `ground`, height above the river, exposure into frost and wind, water types written | the generator (37.2) and small engine reads (37.4), behind a world setting | worlds unchanged with it off; with it on, rain shadows and wet ground show in yields |
| **1: water** | soil water, snow depth and melt, river level on reaches, spate, flood, standing water, low water, ice, winterkill; fish groups by water type | phase 0; brief 5's reaches and runs | a wet week floods the lower village's meadows a day after the upper's; a dry month stops the mill; a hard freeze closes the traps and opens the crossing |
| **2: fire and cover** | fuel dryness, wildfire with drawn ignitions and spread, heath burning, succession of abandoned ground | phase 1's soil water; L-21's fire acts | a dry windy spell carries a fire across the heath and not over the river |
| **3: soil and silt** | loose soil, erosion, silt and cleanness on reaches, fouling trades | phases 1 and 2; the materials stage for tanning and retting | clearing the slope above a river thins its salmon run and silts the mill's leat downstream |
| **later** | water table and wells; people's water and health (environment_state.md, L-23, L-9) | water as a need | |

Each phase is gated by dry runs and a null arm (the same world with the phase off), and read against the stocks' signs in the
agents' reasoning: is it acted on?

### 9. What keeps it small

- Eight stocks in all, each one number on a place; the rules are a few lines each, cheap beside the ecology.
- No hydraulics: a reach's level is a bucket with a lag, not a flow model. A flood's reach is a height, not a simulation of water
  over the cells.
- Compressed time is stated, as the lifespan is (D2-153): a spate in a few days, a season's drought in a week or two of the
  compressed year (calibrate against 32-day years).
- Nothing new reaches the prompt except signs and the acts that already exist, plus a bank and the fire acts.
- The border holds (02zzk): all of this is inside the medieval village and its river.

## Why

- Zach (16 Nov): general systems, floods and their interactions; the gaps between the generated world and what the engine sees.
- The generator's land is mostly unused (02zzl §1), so much of the realism already paid for is lost.
- The decided hazards (D2-77) have no state to read, and D2-71 already says incidents emerge from the systems.
- Shared shocks make leverage and dependence (scenario_design §1): who holds high ground, stores, the mill and the crossing; who
  upstream makes floods or silt for those below; a commons in the river and the woods.

## Alternatives considered

- **Floods and droughts as drawn incidents** (D2-77 as it stands): cheap, but they would not depend on the land or on people's
  acts, so clearing, ditching and damming would change nothing, and the same rain would flood a hill village and a river village alike.
- **Simulate water on the cells** (a flow model at 150 m): realistic, but costly, hard to calibrate, and finer than anything an
  agent can see or act on. Reaches and parcels carry what matters.
- **One "wetness" number per node**: too coarse to put the flood on the meadow and not the hill field, or the drought on the sand
  and not the clay.
- **Leave it to environment_state.md**: that proposal holds the variables of buildings, herds and people; the land's physics needs
  its own design, so the two are split here and cross-referenced.

## Open questions (for Zach)

1. **Emerging or drawn:** should floods, droughts, freezes and wildfire's spread emerge from the stocks (proposed), with the
   scheduler drawing only the weather and true externals (ignitions, hail, pestilence)? This amends how D2-77's flood and drought
   are reached, not that they exist.
2. **The grids:** parcels for ground, reaches (areas on `down`) for rivers, water parcels for still water, nodes for snow; cells
   stay generator-side (proposed). This answers Q-50 for the environment only.
3. **Older worlds:** phase 0 changes the weather and yields of worlds that read it (rain by place, wet ground). Proposed: behind a
   world setting, on for new worlds.
4. **The order:** phase 0 now with brief 5, phase 1 next (water, with the fish groups), then fire, then soil (proposed).
5. **Water types:** the eight in §6, from the generator, with estuary and coast later?
6. **How often:** under the compressed year, about one or two spates a year in a wet lowland, a flood on the meadows every year or
   two, a hard freeze every few years, a dry spell most summers (calibrate)?

## History

- 16 Nov 2026: written by 37.2 at Zach's request, after the waters discussion (water types and fish groups, ice, seasons), widened
  at his ask to the whole environment. Built on two read-only passes over `main` (02zzl).

## Sources

docs/review/37_growth/02zzl_environment_gaps.md (the inventory); spec/environment/scheduler.md (D2-69 to D2-79), resources.md;
proposals/environment_state.md, environment_catalogue.md, ecosystems.md, crop_growth.md, building_risks.md,
phase3_variance_and_risk.md, weather_scheduler.md, land_kept.md (D2-208), river_and_water.md (D2-209), temperate_landscapes.md,
water_and_preservation.md, wild_layer.md; OPEN L-10, L-21, L-23, L-34, L-48, L-68, L-71, L-73, L-100, Q-50; guides/senses.md;
docs/scenario_design.md §1; 02zzj part 18 §2 (depletion and pollution), 02zzk (the border).
