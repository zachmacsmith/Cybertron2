# The world keeps the land it runs on

**Status:** accepted: D2-208 (10 Nov), the principle. How it is kept (below) is 37.2's proposal, for Zach and 37.4.
**Owner:**
- 37.2: the generator writes the land with the world;
- 37.4: the engine loads it and keeps the run's changes; the run record and publishing keep it.

**Affects:**
- spec/world/generation.md;
- spec/record/ (the run's files; D1-1 to D1-5);
- `cybertron2/landgen/write.py`;
- `cybertron2/engine/world.py` and `run.py`;
- `cybertron2/publish_hf.py` (FILES);
- the capacity tool;
- every later design that needs the land at a fine grain: forays' route module (forays.md History, 10 Nov), animals placed on the
  land, clearing and draining.

## Summary

The generator draws a region on a grid of cells about 150 m apart: 334 x 334 for a 50 km world. Each cell has height, slope, sea,
lake, temperature, moisture, flow, river, spring, wetness, soil texture, fertility, terrain, cover, ecosystem, wood band, system and
place.

From those it makes the world file's summaries: nodes, parcels, roads, and the ecology's areas. Today the cells are then:
- **dropped** when the world is made in memory (tests, harnesses);
- **saved beside the world file** (`<name>.cells.npz`) when it is written to disk, but never loaded by the engine;
- **never part of a run.** A run's directory and its published record (`publish_hf.py` FILES: run.json, turns, rounds, days,
  perception, memory, state) hold no land.

So the engine runs on a sketch of the world. A run cannot be rebuilt from what it kept, only regenerated from the seed, and that
holds only while the generator's code is unchanged. Nothing that needs the land at its grain (a route over it, animals placed by it,
a wood cleared cell by cell) has anything to stand on.

37.2 built the generator this way and did not press for the land to be kept. Zach's call corrects it.

## The proposal

1. **The land is a file of the world.**
   - The generator writes `land.npz`: every cell field at full grain, plus the grid's spacing and origin. It writes it always, in
     memory as well as on disk.
   - The world file records its content hash and the generator's version.
   - A world made by hand has none. The engine then runs on its parcels as now, and says so in the run's record.
2. **The engine loads it at build,** read-only, as `World.land`, kept apart from the day's state so the journal does not copy it
   each day.
   - The coarser tiles a route needs (about 500 m) are derived from it at load, never stored.
   - The parcels and areas are tied to their cells, so each can be read at its grain.
3. **The run's changes are kept on top.** Clearing, draining, felling, ploughing out new fields, a path worn, a weir built: each is a
   change to cells, journaled like any other state change. The land at any day is the land file plus the changes up to that day.
4. **Every run keeps it.**
   - The run directory gets a copy of `land.npz`, and run.json records its hash.
   - Resume and replay refuse a land whose hash differs.
   - Publishing adds `land.npz` to FILES, so the dataset holds the land of every run. It is a few MB compressed.
5. **Old runs.** For past generated runs whose world file names its seed and configuration, the land can be regenerated once and
   checked against the run's parcels and areas. Runs that fail the check are marked "land not kept".

## Why

- Zach (10 Nov): "The world file from the engine just definitely had to actually keep the world it is running on ... let's actually
  store and build upon the world we are running in. Even just for reproducibility purposes WTF would we throw it away?"
- **Reproducibility.** A run should be rebuilt from its own record (D1-1, D1-3), not from a generator that keeps changing.
- **The designs now waiting on the land:**
  - the route module for forays;
  - animals placed by habitat inside an area;
  - signs that show where game really is;
  - clearing and draining at the grain they happen;
  - settling new land (OPEN L-104).

## Alternatives considered

- **Regenerate from the seed when needed.** It breaks whenever the generator changes, which it does often.
- **Keep only coarse tiles.** Cheaper, but it throws away grain that later designs may need, for a saving of a few MB a run.

## Open questions

1. The tile size for routes (about 500 m), and whether some fields are kept at a coarser grain to save space.
2. Whether to regenerate the land of past runs (item 5), and which runs.
3. Whether hand-made worlds should get a land drawn from their layout.

## History

- 10 Nov 2026: Zach decided the principle (D2-208). Written by 37.2 with the current state checked in the code (`landgen/write.py`
  `write`; `publish_hf.py` FILES; the engine loads no cells).

## Sources

DECISIONS D2-208, D1-1, D1-3, D4-22; spec/world/generation.md; forays.md History (10 Nov); hunt_and_forays.md.
