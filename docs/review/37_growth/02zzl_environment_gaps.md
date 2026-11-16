# 02zzl: the environment as the engine runs it, and as the generator makes it: an inventory of gaps (16 Nov 2026)

Supporting notes for `docs/cybertron2/proposals/environment_systems.md` (WORK W-49). Zach (16 Nov): "What are the general gaps
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
| wet | 0 to 1 | area `wet`; `land.position` hollow; parcel `height`=0 over 0.8; words ("wet underfoot", `landgen/write.py:141`) | area `wet` NOT READ; hollow by wild plants only. Farming's wet ground (`farm.ground_mult`, D2-66) reads a parcel key `ground` the generator never writes |
| tex | sand, loam, clay, chalk, peat | parcel `soil`; `land.texture`; area texture shares | area shares by slugs and moles (`wild/loads.py:24`); parcel `soil` and `land.texture` NOT READ |
| depth | soil depth | `land.depth`; `land.held_mm` | `held_mm` ≥ 260 as "wet" for wild plants only; `depth` NOT READ |
| fert | fertility | field `fertility`; `land.base_fertility` | read (farm, capacity: D4-112) |
| f | height above the nearest river of class 2+ | silt in `base_fertility`; parcel `height`=0 under 2 m | only as the rank: heavy rain damages low houses (`engine/night.py:593`) |
| c | distance to the sea | `land.sea_km` | coastal plants |
| terrain, system, band | land kind, landscape system, wood depth | parcel `terrain`, `depth` | NOT READ ("data for stage 2", `landgen/write.py:311`); the band shows only through stock sizes |
| eco | ecosystem | parcel `ecosystem`, area `eco` | wild plants and the ecology |
| exposure, drain_rate, position, rain_factor | parcel `land` keys (write.py:57-88) | as named | exposure, drain_rate, rain_factor NOT READ; position by wild plants only |
| the cells (`.cells.npz`, D2-208) | the land at 150 m | written beside the world | NOT LOADED by the engine (only c2viz reads them); D2-208's engine half is not built |

**What the engine does not know, though the land holds it:** where rain falls more and less; which way water runs; how high a
parcel stands above its river; how much water its soil holds and how fast it drains; how exposed it is; how steep; where springs
rise; which ground is wet. Every one is in the world file or the cells already.

## 2. The environment as processes in the engine

| Phenomenon | Status | Where | Driven by | Affects |
|---|---|---|---|---|
| Weather by node and day (temperature, rain, wind, fog, storms) | built | `climate.py` (D4-109 to 111) | seed, season, height, era | everything below |
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
| Fertility | built | `farm.soil_step`, fallow, manure, stubble (D4-112) | cropping, rest, dung | yield |
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
- dry weeks → low rivers and dry brooks → fish, the mill's power, wells; drought stress on crops (L-68) and grass (the renewal
  hook is unused);
- dry weeks and wind → fuel dryness → wildfire, heath burning;
- bare ground on a slope and heavy rain → erosion → silt in the river, the leat, the spawning gravels;
- snow lying → depth → melt → spring floods;
- frozen nights → ice on still water and slow rivers → fishing, fords, fowl, winterkill;
- abandoned field or clearing → weeds → scrub → wood;
- fouling (tanning, retting, middens, carcasses) → water cleanness → fish, and later people's health;
- the generator's rain shadows, wet ground, exposure, slope and soil water → farming, grazing, frost and work.

## 3. What is already decided or proposed (read before designing)

- **Decided, not built:** the scheduler's incidents, hazards and spreads (spec/environment/scheduler.md: D2-69 to D2-79; the kinds
  include drought, river flood, gale, hail, late frost, blizzard, lightning, house fire, wildfire, blight, murrain and the windfall
  flood silt); D2-71 says incidents "also emerge from the systems"; D2-208 (the engine loads the cells).
- **Built:** the climate (D4-109 to 111); fire weather (D4-83); fertility (D4-112); the renewal hook with the land and the weather
  (D4-113), read by no rule.
- **Proposed or flagged:** environment_state.md (shared hidden variables that interact; L-23); environment_catalogue.md;
  ecosystems.md (disturbance and succession); crop_growth.md §2 (L-68); building_risks.md (L-48); phase3_variance_and_risk.md (L-73);
  L-10 irrigation, L-21 fire, L-34 works on physical facts, L-71 the land's fast stocks, L-100 landscapes; Q-50 one grid or several;
  river_and_water.md (D2-209, being built).
