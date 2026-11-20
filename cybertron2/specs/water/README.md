# Brief 5's worlds (proposals/river_and_water.md §1, §8; D2-209; WORK W-47)

Made by `cybertron2/specs/make_water_worlds.py` on main's generator (after the wild layer's merge, with ties broken by first occurrence so a world is the same whatever PYTHONHASHSEED: 80e66b6), with two new pins (below). Remade 16 Nov (branch `water-worlds-2`): the first versions (cc6f38d) were made on peoples-worlds' generator and did not remake on main. Generated, not run with models: a live
run needs Zach's go. The fine land (`<world>.cells.npz`, D2-208) is not committed, as for the peoples worlds: the maker remakes it
exactly from the seed. Each world ran two days with scripted bots on `ecology-water` (469d7f7) with no errors; each remakes byte for byte under hash seeds 0 and 1 (river, lake checked).

| World | Seed | Days | People | What it holds |
|---|---|---|---|---|
| `river.yaml` | 9 | 14 | 23 | Saltwell (upstream) with the brine spring on "the Brine Meadow", held by its smallest household; Millham (downstream) with the water mill (the generator's `mill site`). Both villages' water is on the large river. Saltwell's water drains through three areas to Millham's ring: 34.6 km of river, so about three and a half days' lag at §2's first rate (calibrate). The river rises in unpeopled upland (17 wild areas on the large river). |
| `lake.yaml` | 3 | 14 | 14 | Meresby on a laid mere (about 12.9 km² of lake in its areas), fed by a brook, with fen carr round it. |
| `runs.yaml` | 5 | 60 | 36 | §8, to run after the gate: Highpool, Middleham and Lowstrand on one large river, three households each (the people generator's bounds widened to fit nine); 23.5 km of river from Highpool to Middleham and 36.5 km on to Lowstrand. No farming (below). Opus at each station's largest household, Sonnet heads, Haiku the rest. |

## Common settings

A climate (`climate: {era: steady}`, the weather scheduler, D4-109), so rain falls by place and the runs' rain cue can fire; late summer start (summer day 4, 8-day seasons), so a 14-day run holds the autumn run; `packs: [wild, water]`; children on (low);
houses stocked with 30 firewood and 20 timber; resident fish in every water parcel (K 8 a unit of size, as the peoples worlds,
OPEN L-75), and no parcel `run_K`: the runs are brief 5's kinds along the river.

## The generator's new pins (this branch)

- `has: brine spring`: a `brine` stock (S and K 1000, r 0: `vocab.BRINE`) on the place's lowest open ground (meadow, pasture or
  waste), with `spring: brine` and a line in its text. The engine reads the stock once it has a `brine` row (world.py loads only
  known resources), so the world runs on either branch.
- `on: big river`: the site within reach of the large river (class 3), and the village's water parcels cut from the large river's
  own cells, nearest first. Needed because the travel costs skip class-3 cells (`settle._cost_from`), so `on: river` gives a side
  channel or no water at all. Opt-in, so no older world changes.

## For the building session

- **Where a run meets a village:** the chain of areas (`land.down`) follows each area's largest river cell, so it passes a
  village's **ring**, beside its small home area (the home holds only the village's two water cells). Read "a run at a village's
  water" as the run's density in the village's home or ring area, or the run never reaches Millham's water in this world.
- **Farming cannot be switched off:** farming's rows carry no pack, so the runs-only world removes fields (to scrub), seed grain,
  beans, flour, bread, hay and herds, and the farming crafts from people's knowledge. Basic farming acts still exist. An engine
  `farming` pack would make it an exact arm.
- **The salter's craft:** given only where the engine has `boil salt`; these worlds were made on main, which does not, so remake the river world on `ecology-water` after merging main (80e66b6), or add `boil salt` to the spring household's adults.
- **Deaths in the dry run:** an elder at the lifespan's end and a small child in the river world: the generated people's own
  ages, not the edits.
- **The null arm for §8:** the same world with the runs replaced by a resident stock of the same yearly food; it needs brief 5's
  runs as kinds, so it is made when they exist.
