---
id: docs/review/37_growth/02zzl_environment_gaps.md
kind: note
updated: "2026-11-16"
---
# 02zzl: the environment as the engine runs it, and as the generator makes it: an inventory of gaps (16 Nov 2026)

*note · `docs/review/37_growth/02zzl_environment_gaps.md`*


Supporting notes for `docs/cybertron2/proposals/environment_systems.md` (WORK [[W-49 Environment systems|W-49]]). Zach (16 Nov): "What are the general gaps
between what the engine sees and the world generated, and what interactions between the environment are currently missed. This
should aim for general systems, like can we support floods etc, and the interactions."

How this was made: two read-only passes over `main` after the wild layer's merge (6190b4d, 16 Nov), one tracing every land field
from the generator to the engine, one listing every environmental process in the engine. Their file and line references were
spot-checked by 37.2 (rain from one global parameter, `climate.py:251`; renewal rules reading none of the context they are given,
`renewal.py:127`; the generator's wet ground going only into words, `landgen/write.py:141`).

## 1. What the generator makes and whether the engine reads it

All paths under `cybertron2/`. "NOT READ" means no file in `engine/`, `wild/` or `capacity/` reads it.

| Field (landgen/physical.py `Land`) | Meaning | Reaches the world as | Read by the engine |
|---|---|---|---|
| h | height, m | node `elevation`; parcel `land.elevation`; area `elevation`; parcel `height` rank | node elevation in the temperature lapse (`engine/climate.py:56`); parcel `land.elevation` NOT READ; area elevation a feature no kind uses |
| slope | degrees | parcel `height`=2 over 5°; area `rock` (share at 25° or more); words | `rock` (raven, bear); slope itself NOT READ |
| temp | mean yearly temperature | area `temp` | a feature no kind uses (weather comes from climate.py by node) |
| moist | moisture 0 to 1 | cells only | NOT READ |
| rain_mm | yearly rain from the wind sweep (rain shadows) | node `rain_mm`; parcel `land.rain_factor` | NOT READ: the climate rains from one global parameter (`climate.py:251`, `data.py:729` rain_mm 4.5) |
| acc, recv | area drained; the cell each drains to | parcel `land.down` (water parcels); areas `down` | NOT READ (brief 5 will read areas `down`) |
| river (0 to 3) | river class | parcel `land.river`; area `river_km`, `big_river_km` | where heronries and lodges go (`engine/wild.py:672`); wet plants (`wild/plants.py:101`); the ecology's water feature |
| spring | a stream's head | words only | NOT READ |
| wet | 0 to 1 | area `wet`; `land.position` hollow; parcel `height`=0 over 0.8; words ("wet underfoot", `landgen/write.py:141`) | area `wet` NOT READ; hollow by wild plants only. Farming's wet ground (`farm.ground_mult`, [[D2-66 Field works in the first worlds, before weather exists|D2-66]]) reads a parcel key `ground` the generator never writes |
| tex | sand, loam, clay, chalk, peat | parcel `soil`; `land.texture`; area texture shares | area shares by slugs and moles (`wild/loads.py:24`); parcel `soil` and `land.texture` NOT READ |
| depth | soil depth | `land.depth`; `land.held_mm` | `held_mm` ≥ 260 as "wet" for wild plants only; `depth` NOT READ |
| fert | fertility | field `fertility`; `land.base_fertility` | read (farm, capacity: [[D4-112 The land's base fertility, multiplicative|D4-112]]) |
| f | height above the nearest river of class 2+ | silt in `base_fertility`; parcel `height`=0 under 2 m | only as the rank: heavy rain damages low houses (`engine/night.py:593`) |
| c | distance to the sea | `land.sea_km` | coastal plants |
| terrain, system, band | land kind, landscape system, wood depth | parcel `terrain`, `depth` | NOT READ ("data for stage 2", `landgen/write.py:311`); the band shows only through stock sizes |
| eco | ecosystem | parcel `ecosystem`, area `eco` | wild plants and the ecology |
| exposure, drain_rate, position, rain_factor | parcel `land` keys (write.py:57-88) | as named | exposure, drain_rate, rain_factor NOT READ; position by wild plants only |
| the cells (`.cells.npz`, [[D2-208 The world keeps the land it runs on|D2-208]]) | the land at 150 m | written beside the world | NOT LOADED by the engine (only c2viz reads them); [[D2-208 The world keeps the land it runs on|D2-208]]'s engine half is not built |

**What the engine does not know, though the land holds it:** where rain falls more and less; which way water runs; how high a
parcel stands above its river; how much water its soil holds and how fast it drains; how exposed it is; how steep; where springs
rise; which ground is wet. Every one is in the world file or the cells already.

## 2. The environment as processes in the engine

| Phenomenon | Status | Where | Driven by | Affects |
|---|---|---|---|---|
| Weather by node and day (temperature, rain, wind, fog, storms) | built | `climate.py` ([[D4-109 The weather scheduler|D4-109]] to 111) | seed, season, height, era | everything below |
| Frost | built | `climate.frost`; `world.cold` | the night's low | crops, decay, fuel, wear, cold deaths, graves |
| Snow lying | built (a flag) | `environment.snow_lying` | snow days, 3 days without frost to clear | sight, tracks, rot, wear, the pass, deer, wolves |
| Gale | built | the weather label | wind, storms | windfall, wear, fires out |
| Soil water | partial: the wild layer only | `wild/ecology.py:237` (an area bucket from rain alone) | rain | wild grass and roots, slugs, moles, fungi |
| Waterlogging | partial | `farm.ground_mult` (a fixed ×0.75 until ditched) | static land key, never written by the generator | yield |
| Drought | partial: signs and the wild layer | "no rain for days"; the ecology's dry factor | rain | wild forage only; crops, engine grass, fish, mills unaffected |
| Floods | partial | heavy rain wears low houses (`night.py:593`); fords high for 2 days (`roads.challenge`); signs; the beaver's dam | the heavy-rain label | buildings, fords. No river level, no meadow or crop loss, no silt |
| Ice | partial | runs of frozen days in the wild layer; the great freeze; frozen graves; seed lost in cold ground | frozen nights | fowl, herons, stores, burial. Ice on water is only a sign |
| House fire | partial (scripted only) | `run.dawn` incident | the world file | the house |
| Wildfire, heath burning | absent | | | |
| Fertility | built | `farm.soil_step`, fallow, manure, stubble ([[D4-112 The land's base fertility, multiplicative|D4-112]]) | cropping, rest, dung | yield |
| Erosion, silt | absent (signs; silt only at generation) | | | |
| Woods | built | `forests.night` | felling, grazing, gale | fuel, sight, deer |
| Grass | built, weather-blind | `RESOURCES.grass`, winter ×0.25 | season, grazing | herds |
| Wild plants | built | `renewal.seasonal`, the plant year | season, mast, warmth | forage |
| Succession of abandoned ground | absent (forest to scrub only) | | | |
| Water quality, wells | absent | | | |
| Wild populations, animal disease, pests | built | the ecology, `wild/diseases.py`, the loads | food, warmth, frost, snow, mast, crowding, people | crops, stores, herds |
| Human disease | absent (a background illness) | `life.py:452, 478` | | |
| Decay of goods | built | `night.decay_rate`, `spoil_rate` | wet, cold, season, store | food |
| Mud and roads | partial (signs; fog; a soaking at a ford) | | weather | no slowing of travel |

**Couplings that exist:** frost (crops, decay, fuel, wear, graves); frost at the oaks' flowering (the mast, and through it boar,
pigeons, voles, bears); runs of frozen days (fowl crowd, the great freeze); rain after dry (the eel night); rain to the wild soil
bucket (slugs, moles, fungi, wild grass); snow (deer, wolves, tracks, forage buried, the pass); a wet day (spoilage, fuel); heavy
rain (a high ford, low houses); gale (windfall, wear, fires out); warmth (berries, aphids, ladybirds); grazing (young growth,
fertility, dung); felling (scrub, sight); the beaver's dam (meadow, fish); wild crowding (murrain in herds); full stores (rats).

**Couplings that are absent** (the gaps this proposal answers):
- rain over a catchment → river level → spate, flood on low parcels → hay and crops lost, fords shut, the mill stopped, a weir
  damaged, silt laid;
- dry weeks → low rivers and dry brooks → fish, the mill's power, wells; drought stress on crops ([[L-68 Crops grow by the weather, not only the season|L-68]]) and grass (the renewal
  hook is unused);
- dry weeks and wind → fuel dryness → wildfire, heath burning;
- bare ground on a slope and heavy rain → erosion → silt in the river, the leat, the spawning gravels;
- snow lying → depth → melt → spring floods;
- frozen nights → ice on still water and slow rivers → fishing, fords, fowl, winterkill;
- abandoned field or clearing → weeds → scrub → wood;
- fouling (tanning, retting, middens, carcasses) → water cleanness → fish, and later people's health;
- the generator's rain shadows, wet ground, exposure, slope and soil water → farming, grazing, frost and work.

## 3. What is already decided or proposed (read before designing)

- **Decided, not built:** the scheduler's incidents, hazards and spreads (spec/environment/scheduler.md: [[D2-69 The scheduler's layers|D2-69]] to [[D2-79 Windfalls have no rule of their own|D2-79]]; the kinds
  include drought, river flood, gale, hail, late frost, blizzard, lightning, house fire, wildfire, blight, murrain and the windfall
  flood silt); [[D2-71 Risks attach to things|D2-71]] says incidents "also emerge from the systems"; [[D2-208 The world keeps the land it runs on|D2-208]] (the engine loads the cells).
- **Built:** the climate ([[D4-109 The weather scheduler|D4-109]] to 111); fire weather ([[D4-83 A fire under no roof in the night's weather|D4-83]]); fertility ([[D4-112 The land's base fertility, multiplicative|D4-112]]); the renewal hook with the land and the weather
  ([[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]), read by no rule.
- **Proposed or flagged:** environment_state.md (shared hidden variables that interact; [[L-23 Water as a need, and the land's hidden state|L-23]]); environment_catalogue.md;
  ecosystems.md (disturbance and succession); crop_growth.md §2 ([[L-68 Crops grow by the weather, not only the season|L-68]]); building_risks.md ([[L-48 What can happen to buildings and fittings, by weather and use|L-48]]); phase3_variance_and_risk.md ([[L-73 Phase 3's rest|L-73]]);
  [[L-10 Irrigation|L-10]] irrigation, [[L-21 Fire house fire and wildfire in the scheduler, spreading along the…|L-21]] fire, [[L-34 Works on the land's physical facts wait for the landscape generator|L-34]] works on physical facts, [[L-71 The land's fast stocks|L-71]] the land's fast stocks, [[L-100 Landscapes still to tune|L-100]] landscapes; [[Q-50 One grid or several|Q-50]] one grid or several;
  river_and_water.md ([[D2-209 Brief 5 (river and water) is built|D2-209]], being built).

## 4. Every earlier consideration of the land's hidden state, in order (surveyed 16 Nov, at Zach's request)

Found by searching both repositories' histories (Cybertron 1 before the split, this one after) for hidden state, hidden variables,
water table, water level, river level or reach, groundwater, soil moisture or water, wetness, floods, fast and slow stocks, and
reading each hit. Two senses run through it: the land's **physical** hidden state (water, soil, fuel), and hidden state as
**information** people must infer through signs.

| Date | Where | What it said | What became of it |
|---|---|---|---|
| 22 Oct | review 38.04 places design (`docs/review/38_space_engine/04_places_design.md`) | each kind of land draws a **hidden quality** within its ranges; a **hidden climate** of two axes (temperature, moisture); incident base rates by kind (floods, fire, fever); **signs** of the hidden state, local ("the river is running high for spring") | the climate axes became the weather scheduler ([[D4-109 The weather scheduler|D4-109]]); kinds of land became the generator's terrains |
| 23 Oct | proposals/environment.md and the model `02q_environment_model.py` | one scheduler: eras, years, spells, incidents and spreads; **hazard = base × drivers × exposure (local state)**; paired draws | decided [[D2-69 The scheduler's layers|D2-69]] to [[D2-79 Windfalls have no rule of their own|D2-79]] (spec/environment/scheduler.md); only the weather built |
| 23 Oct | proposals/environment_state.md (first version), 02q's cascade demo | Zach: "risks should draw on shared state that can interact (a flood raising water levels, contamination, infection)", "many often-invisible parameters"; **hidden variables** on parcels, waters, buildings, herds, people, nodes, each relaxing to a baseline, one step a day; hazards read them; cascades (a wet spell, the water table, a latrine, the well, flux) | discussion; flagged [[L-23 Water as a need, and the land's hidden state|L-23]] (24 Oct); none of its new variables built |
| 23 Oct | environment_state.md §7 to §10 | **layers below people's reach**: the sky, **groundwater per node** (water table, recharge, cleanness), **the river on its water parcels** (level, flow, silt, cleanness), wetland, soil (moisture, fertility, depth, salt, spores), living things (vegetation, fuel dryness, pests); cross-layer paths (wells fail before the river; clearing raises floods downstream; draining a fen floods below; a tanner upstream fouls the river); **water as a need**; latrines and middens; the first sixteen variables | as above, [[L-23 Water as a need, and the land's hidden state|L-23]] |
| 23 Oct | environment_state.md (Zach: rivers use up parcels) | **rivers take land** as water parcels, a brook a feature; **floods spread from them by adjacency, lowest neighbours first** (meadow, then fields, then houses); the same river continues downstream | water parcels built; floods not |
| 23 Oct | visibility ([[D2-99 Visibility per place and sense|D2-99]] to [[D2-103 Visibility is computed, not stored|D2-103]]) | sight read each day from the land's state (vegetation, crop, snow, smoke); **computed, not stored** | built |
| 24 Oct | [[D2-114 A node's parcels form a graph of neighbours, shaped by the…|D2-114]] to [[D2-117 Herds can wander far|D2-117]] (parcel_graph.md) | parcels as a graph of neighbours with a side and a height | built (`adj`, `side`, `height`) |
| 1 to 3 Nov | proposals/generator.md ([[D2-173 The generator fills in around what a world file gives|D2-173]], [[D2-174 A world under the graph|D2-174]]), generator_stage1.md | **a world under the graph**: a mesh of cells kept as ground truth, carrying water, soil, groundwater depth and each cell's **exposure to hazards** (flood plain, fire-prone heath); systems that can read it later: **floods by height**, sight across ridges, bridges by width, water by groundwater depth. **§7: only physics that bottoms out in leverage.** Stage 1 left "the tier 1 environment (year severity, soil moisture, floods, river level)" to stage 2 | the mesh built and kept ([[D2-208 The world keeps the land it runs on|D2-208]]), not loaded by the engine; stage 2 not begun |
| 5 Nov | 02zo (proposals swept) | environment_state's six questions parked in [[L-23 Water as a need, and the land's hidden state|L-23]]; rivers as water parcels and visibility built | |
| 7 Nov | proposals/engine_overhaul.md, process_model.md ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]]) | hidden state benched as **"hooks only"**: hazards' triggers read named state variables; water as a need folded in minimally; every rate names its **clock** (day, year, life) | the clocks built; the hooks partly ([[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]) |
| 7 Nov | proposals/water_and_preservation.md | water ecosystems by type (brook, river, mere, fen, coast), the gear ladder, fixed works | discussion; brief 5 builds part |
| 7 Nov | proposals/living_populations.md §0 | **populations are hidden state; people infer them** through signs, never numbers | the principle for the wild layer (built) |
| 8 Nov | **37.2 to 37.4, agreed by Zach in principle**: the land at **three speeds** | **fixed** (elevation, exposure, texture as water held and drainage, depth, base fertility, position, rain factor, sea distance, river class, the downstream link); **slow** (a fertility offset, a **wetness offset** moved by drains and dams, a **vegetation state**); **fast** (**soil water, snow, river flow, fuel dryness**, one stock and one rule each, in the parcel's `state`) | fixed fields written ([[D4-112 The land's base fertility, multiplicative|D4-112]] reads base fertility); fertility built as the slow offset; wetness offset, vegetation, fast stocks not built; never recorded as a decision |
| 8 Nov | 02zp ecosystems deep dive §4, §15, §16 | **five layers** (ground, conditions, vegetation, populations, uses) on **four clocks** (day, season, year, decades); sixteen loops; the land fields as written; "37.4 builds the fast stocks"; a calibration backlog waiting on them | the land fields built; the rest not |
| 8 Nov | proposals/base_fertility.md ([[D4-112 The land's base fertility, multiplicative|D4-112]]), weather_scheduler.md ([[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]) | base fertility, multiplicative; **the renewal hook** hands each stock's rule the weather and the land | built; the hook unused by any rule |
| 8 Nov | proposals/phase3_variance_and_risk.md | the scheduler as data; exposure as a registered function of local state; damp fuel; prior work: **a land-surface bucket per place** (Manabe) for soil water, snow and river flow routed downstream | discussion; [[L-73 Phase 3's rest|L-73]] |
| 9 Nov | wild_layer.md §3.10; OPEN [[L-71 The land's fast stocks|L-71]] | the fast stocks as **the foundation** the wild layer reads (slugs, eel runs, frozen ground); flagged | not built; the wild layer runs its own soil bucket from rain alone |
| 9 Nov | 02zr critique and purpose brief §3.3 | **hidden state and an information economy**: lags, quirks and false lore people must read | principle for the wild layer |
| 16 Nov | this note and proposals/environment_systems.md | the gaps inventoried; the consolidation | discussion (OPEN [[Q-52 Environment systems|Q-52]]) |

**What the consolidation must keep from these and had not:** floods reaching parcels lowest first (23 Oct), which "floods by
height" (3 Nov) makes exact; groundwater per node as a carrier with wells failing before the river (23 Oct); each cell's exposure
to hazards (3 Nov); only physics that ends in leverage (3 Nov); hazards reading named variables through registered exposure
functions (7 and 8 Nov); and hidden state as something people infer (7 and 9 Nov).
