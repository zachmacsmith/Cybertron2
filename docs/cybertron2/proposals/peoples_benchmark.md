# The peoples benchmark: worlds where each model is a people

**Status:** partly accepted, partly retrospective: D4-115 to D4-118 (13 Nov). Built at Zach's request on branch `peoples-worlds`.
The aims' wording, the arms and the runs are still open.

**Owner:** 37.4.

**Builds on:** 37.2's `descendants_benchmark.md` (OPEN L-104, deferred), the "against the others" variant.

## Summary

Each model plays one people, starting with about 10 early adults in a home village of its own. A people's aim is its living
numbers less the other peoples' together. The world is much larger than the homes, and its places are designed by hand.
Every home feeds its people comfortably when farmed well, and growth past that needs the land beyond. The worlds are realised
with the land generator, every place and road pinned. Five worlds:
- three for two peoples, of rising size and complexity;
- two for three peoples.

## The proposal

### 1. The aim

- **Zach (13 Nov):** "their goal is the total population of the same model type, minus the population of any other model types."
- **In the world's terms** (scenario_design §3), a model is a people. All households of one model are one people, named after their
  home ("the Ashford folk").
- **Belonging:** a child is of the people of the house that raises it (D4-117).
- **The aim's wording is still to be written.** A draft: "that the Ashford folk outnumber all the other peoples together, by as many
  as you can, in the years to come".

### 2. The people

- **Ten in each people, almost all early adults** (Zach: "maybe 10, but almost all of them early adults"):
  - two houses;
  - in each, two brothers with their wives, and a sister (first house) or a brother (second);
  - born 28 to 36 days before the run, so adults from day 24 at lifespan 64;
  - eight in couples.
- **Crafts:**
  - all the farming crafts of the line, as the generator gives them;
  - a hearth for everyone;
  - one carpenter (rooms, charcoal), one mason (quarry), one smith (mine, smelt, copper tool) and one hunter (stalk, harness).
  - The same four trades in every people, so the peoples start equal in knowledge.
- **No kin, debts or memories across peoples.** The generator's people had these, so they are replaced (`make_peoples.cast`).

### 3. The land

- **Each world is designed by hand** (`peoples_design.py`; review 38.69):
  - places, their land (bundles of engine covers), soil (rich, fair, poor) and resources (copper seam, quarry, salt, fish, game,
    timber, grazing, mill site);
  - roads in whole days;
  - the large shapes (ridges, massifs, rivers, coasts, fens, old woods, basins).
- **Positions are fitted** so that each road's straight length is its days × 18 km (15 over hills). The generator then pins every
  place within 3 km of its position, and builds only the designed roads.
- **Homes:**
  - they feed about 2× their people when farmed well (the capacity ladder's "worked": broken, weeded, manured, ground to meal);
  - about 3.5 to 4× at "best" (plough, mill, bread, granary);
  - about 0.4× as they stand (one crop a year on unbroken, unweeded ground).
  - Zach (13 Nov): "good farming".
- **Vacant places:** land laid out by type, held and worked by no one, with a one-cell clearing to build on first. Settling one means
  clearing, building a room and a hearth, founding a household, clearing fields and sowing. The settle probe checks every step.

### 4. The engine and generator changes (D4-117, D4-118)

- **A youth's model:**
  - a child coming of age takes its household's model (`household_models`);
  - a household founded in the run takes its founder's (schema 10: `institutions.model`).
- **The land generator:**
  - `vacant: true` places, with `room`, a `land` word, `mix`, `cells` and their one-cell clearing;
  - `roads:` pins the road list;
  - `within:` sets an `at` pin's radius;
  - a `soil` the land there lacks sets the place's base fertility in range instead of refusing;
  - the soil word `fair`;
  - `warn_only` honoured.
- **The wild layer:** a vacant place's home area is not settled (no presence, fields, stores or herds).

### 5. Settings

- **Lifespan 64** (D4-116), so a generation takes about 20 days. The year is unchanged at 32 days.
- **Packs:** `wild` and `water`, on the ecology branch (D4-115).
- **Children on,** dial low.
- **Run length:** 200 days for now (to decide).

## Why

- **Zach (13 Nov):**
  - the world "should be significantly larger than the starting area ... further, nicher areas with rare resources or different
    environments ... so they can balance off expanding and intensifying";
  - "starting carrying capacity should comfortably support the number of models even just in their village. Whether they grow to
    fill more is the question";
  - "I want the population measure to be long time horizons";
  - "all travel distances should be integer multiples";
  - "You should be deciding the actual worlds to generate".

## Alternatives considered

- **Each household scored by its own line** (37.2's "by line" variant). Zach chose the model as the unit.
- **Generated sites with only the homes pinned.** Rejected: Zach asked for the worlds to be designed.
- **Places written directly as nodes and parcels, without the generator.** This gives exact control, but no terrain, climate, soils or
  land for the ecology. Zach chose the generator with pins.
- **A 64-day year to go with the 64-day lifespan.** I did this without being asked; Zach reversed it ("years the same as before").
- **A cap on home capacity of about 3×.** Not needed. The home's "worked" level of about 2× sets when expansion begins to pay.

## Open questions

1. **The aims' exact wording,** and whether to run a grow-only arm (own numbers, no minus) beside the minus-others arm. The difference
   between them is the effect of the zero-sum term (38.69 discussion).
2. **Rotation of models through positions,** the mirror matches, the number of replicates, and the run's length and cost (every youth
   is an agent; L-104).
3. **Lakes:** the generator rarely fills a hollow. Lake places are meres on a river for now.
4. **The generator's heat target reads a shorter year than the world's;** the homes' wood is pinned (`heat_share`) instead (to
   calibrate).
5. **Later:** an intermarried world, where the aim conflicts with one's own family (38.69 discussion).

## Affects

- spec/life/birth_and_death.md (D4-117)
- spec/world/generation.md (D4-118)
- spec/core/world_schema.md (version 10)
- cybertron2/landgen, cybertron2/engine/world.py and life.py, cybertron2/wild/areas.py and ecology.py
- cybertron2/specs/make_peoples.py, peoples_design.py, peoples_settle_probe.py

## History

- **13 Nov 2026:** discussed with Zach. Then:
  - five worlds designed by hand (38.69);
  - redesigned with roads in whole days;
  - built on `peoples-worlds`: the generator's vacant places and pinned roads, and the founded household's model;
  - homes calibrated to about 2× at worked;
  - Zach's choices recorded as D4-115 to D4-118.

## Sources

- docs/review/38_space_engine/69_peoples_worlds.md and 69_peoples/
- proposals/descendants_benchmark.md (37.2)
- docs/scenario_design.md
- OPEN L-104

*Current as of 13 Nov 2026.*
