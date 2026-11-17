# 38.76: One fish stock per water body, the engine half (D2-229), as built

Session 37.4, 17 Nov 2026 (WORK W-56). Branch `water-bodies` (from 37.2's `floodplains` d69b525), not merged. Full suite: 650 pass,
2 skipped.

## What was built

| Part | Where | What |
|---|---|---|
| The body's stock | `cybertron2/engine/waters.py`, `world.py` | At a world's making, each body in `wild.land.waters` with water parcels in the world gets one record a stock in `s["waters"][body]` = {kind, parcels, areas, fish}. Its K and S are its parcels' summed; r, renewal and the rest come from the parcel with the largest K. Every parcel on the body holds that same record as its `res["fish"]`: one object, so every reader and every primitive through the parcel (draw, set_res, add_res) changes the body's stock. |
| Restored worlds | `run.py` (continue mode), `waters.link` | A checkpoint keeps the values on both; `link` makes them one object again. |
| Counted once | `night._grow`, `capacity/sources.py`, `wild._site_stock`, `wild._dam` | The night renews a record once. The capacity model, a site's share of the village's stock (the heronry) and a dam's raise take a body's stock at its lead parcel only (`waters.lead`). |
| The wild layer's fish | `waters.to_wild`, called before the night's food web | Each area on a body holds fish at its cap times the body's fullness (S/K): what people take thins the fish the wild kinds find there. |
| The record's shape | `schema.py`, `spec/core/world_schema.md` | Top-level `waters`; world schema version 11. |

Worlds without a waters list (every world before D2-229) hold no `s["waters"]` and are unchanged, so their replays stay exact.

## Defaults taken (OPEN L-116)

- **One-way link to the wild layer.** The body is the one source of truth; the food web reads its fullness each night. The food web's
  own take of fish is not written back to the body. The fish-eaters that take from the parcels (the heronry's eats, the otter's
  robbing) already draw on the body's record. A two-way link would need the food web's fish units (kg a km² of water) tied to the
  people's fish, a conversion to calibrate (D2-228).
- **The body's r and renewal** come from its largest parcel's record. On Meresby the parcels differed (the Pool's threshold record,
  K 9,619; the Mere's fast record, K 8); the body follows the Pool's.
- **An area on two bodies** (none in the three water worlds among bodies with parcels) takes the last body's fullness in id order.

## The numbers (the remade worlds, 37.2's LAKE_FISH unchanged)

| World | Body | Parcels | K | Rule |
|---|---|---|---|---|
| Lake | lake:L1 (38 km²) | Meresby_10, Meresby_11 | 9,627 (8 + 9,619) | threshold, r 0.00438 |
| River | reach:Saltwell, reach:Millham | two each | 16 each (8 + 8) | fast, r 0.3 |
| Runs | reach:Highpool (one parcel), reach:Middleham, reach:Lowstrand | | 16 (or 8 + 8) | fast, r 0.3 |

The lake's K is still the per-parcel stock D4-120 sized from the village's own land. By D2-229 it should be sized from the whole lake
(at 7,500 a km², 38 km² is about 285,000): 37.2's calibration across worlds (D2-228). The river reaches are the small-water default.

## The tests

- **New** (`tests/test_cybertron2_water_bodies.py`, 7): two parcels share one record sized by the lake; fishing at either lowers it;
  it regrows once a night; the capacity model counts it once; a restored world is linked again; a world without waters is unchanged;
  the wild fish on a body follow its stock.
- **The 15 on the old layouts:**
  - **water5_fowl (10):** the lodge set by hand beside the mere, which has only fen beside it now; the frost order checked for a big
    river only where the ring has one; s1's floodplain meadow by water.
  - **water5_river (2):** the flood-gap ratio and the weir's upkeep bounds widened, citing D2-228. The upkeep is 0.95 of a wattle
    weir's cost a year on the remade Saltwell catchment, against the target of 0.35 to 0.55 (37.2's calibration).
  - **water5_keep (1):** the brine pan refused at a house set away from the spring.
  - **wild (1):** the old sow's boar set again after the night; the night's movement had left the ring empty.
  - **wild_range4c (2):** a seed-3 layout, where a pack's range reaches two villages; seed 7's villages are now 23.6 km apart at
    the nearest.

## Left

- 37.2: the lake's K from the whole lake (LAKE_FISH), the weir's upkeep, across the calibration worlds (D2-228).
- Zach: the merge of `water-bodies` (with `floodplains` under it) and of `ecology-water`.
- The two-way link to the food web, if wanted (OPEN L-116).

*Current as of 17 Nov 2026.*
