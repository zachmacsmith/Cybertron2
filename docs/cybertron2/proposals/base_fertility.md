# Proposal: the land's base fertility (multiplicative)

**Status:** retrospective, accepted: D4-112 (8 Nov; built). **Owner:** 37.4 (the engine). The land's fixed, slow and fast
properties as a whole are 37.2's (its message of 8 Nov); this is the engine's first use of them. **Affects:** engine/farm.py,
world.py, verbs.py (clearing), schema.py (version 4); capacity/rotation.py, sources.py; spec/core/processes.md,
spec/core/world_schema.md.

## Summary

A parcel may carry `land: {base_fertility: b}`. Every level its soil comes back toward is the table's level times b: rest
(1.0 x b), grazing and dung (1.15 x b), a crop's restoring, and a new clearing's starting fertility. The current `fertility`
(per holding) keeps its meaning: what the crop sees, lowered by cropping and raised by the stages. Default 1.0, so every
existing world is as before.

## Why

- 37.2 proposed a base fertility plus a slow "fertility offset". I first proposed only moving the rest level to the base, and no
  offset (the existing `fertility` already is the slow stock).
- Zach: "I think the fertility offset is because e.g. river plains are very fertile but even adding dung can't make desert sand
  fertile enough?" Right: farm.py's ceilings were absolute (dung toward 1.15 anywhere), so under my first version dung would
  have raised sand at 0.3 to 1.15.
- Zach: "yes multiplicative if that makes sense."

## The proposal (as built)

- `farm.base(par)`: the parcel's `land.base_fertility`, else 1.0.
- `fallow_gain`, `manure_gain`, `soil_step` and the night's grazing take the base and scale their target levels by it. The rules
  are linear in the soil and the level, so a field's steady soil under any rotation is b times its steady soil at 1.0.
- A cleared parcel starts at CLEARING's fertility for its cover x b; a parcel the spec gives no `fertility` starts at b.
- The capacity model's field year (rotation.best_year) starts from b and passes it to the same functions.
- Signs read the absolute fertility ("worn out" below 0.55): poor ground reads as poor, whatever its cause.

## Alternatives considered

- **Additive (base + offset):** dung adds the same amount everywhere, so poor ground gains most in share (sand 0.3 to 0.45, +50%;
  a plain 1.3 to 1.45, +12%). Rejected for the multiplicative form, which matches "dung can't make sand fertile enough".
- **A separate offset field:** equivalent to fertility / base - 1. Not stored: the engine keeps one number, the current fertility.
- **Only the rest level by base:** the first proposal; wrong, as above.

## Open questions

1. Should long improvement raise the base itself (centuries of turf and dung made plaggen soils on sand)? That would be 37.2's
   slow layer; as built nothing moves the base.
2. Signs by the absolute level: should a farmer also tell "naturally poor" from "worn out"? Not built.
3. Base fertility is nutrients only; soil water (37.2's fast layer) will carry sand's other poverty. Not built yet.

## History

- 8 Nov: built at Zach's request after 37.2's message and the exchange above (D4-112). Tests:
  tests/test_cybertron2_base_fertility.py (dung to each ground's own ceiling; rest to the base; the capacity model's steady soil
  scales with it); base 1.0 is the old rule exactly.

## Sources

37.2's message of 8 Nov (fixed, slow and fast land properties); farm.py (D4-39); 02l section 2.
