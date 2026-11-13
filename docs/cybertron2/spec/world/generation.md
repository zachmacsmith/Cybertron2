# Generating a landscape

## Summary

When a landscape is generated, it is generated physical-first: elevation, moisture, rivers by drainage, then kinds of land from the
terrain, then settlement. Every layer can be set by hand instead.

## Decided

- D4-22: the landscape is generated physical-first (elevation, moisture, rivers by drainage, kinds from terrain), every layer
  overridable by hand.
- D2-208: the world keeps the land it runs on: the generated land at its full grain (the cells and every field made of them)
  goes with the world, into each run's record and its publication; the engine loads it, keeps the run's changes to it on top, and
  a run is reproduced from what it kept, never by regenerating.

## Mechanics

The order: points on a hidden plane and their neighbours; elevation and moisture; rivers (each point drains to its lowest neighbour;
enough flow makes a river along edges and through nodes); kinds of land from elevation, moisture and rivers; resources from the
terrain; edges and their costs from the terrain; settlement (D4-22). Any layer given in the world file is kept and the rest filled
in.

## Open

- The biome table, resource rules and checks before a world is used (38.04 §6): to decide.
- The first worlds are hand-made (38.04 §6).

## Sources

38.04 §5-§6.

## A designed world (D4-118)

- **Places pinned:** each place by position (`at`, within `within` km, default 4), soil (`rich`, `fair`, `poor`: set on the place's
  land, in that range, where the site lacks it), resources (copper, stone) and water (`on`: river, sea, lake; `has`: mill site).
- **Vacant places** (`vacant: true`): land laid out by a `land` word (open, wood, waste, rock; or `mix`), as much as `room`
  households would work (`cells` sets it outright), each cell keeping the cover the land has, and a one-cell clearing to build on.
  Nothing is built, sown, held or kept there, and no one lives there.
- **Roads pinned** (`roads:` a list of pairs): only those roads are built; a long one still gets its stopping places.
- **`warn_only`** takes a check off the required list.

*Current as of 13 Nov 2026: D4-22, D2-208, D4-118.*
