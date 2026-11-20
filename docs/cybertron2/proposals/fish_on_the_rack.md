# Fish on the hearth rack

**Status:** retrospective, accepted: D4-122 (17 Nov 2026).

**Owner:** 37.4.

## Summary

Fish can be hung to dry at a hearth or a fire ring as meat is: `dry fish`, a batch of up to 8 fish for 3 nights, drying to `dried fish`
at half the weight (food 2.0 a unit, keeping as dried meat). It shares the hearth's one rack with meat. The smokehouse is unchanged.

## The proposal (as built)

- **The technique** (`engine/data.py`): `dry fish` (water pack, basic):
  - at a hearth or fire ring;
  - takes 8 fish and gives 8 `drying fish`;
  - a batch of whatever one has, up to 8;
  - a rack of 3 nights into `dried fish`, ratio 0.5;
  - smoke-bearing, as `dry meat`.
- **The goods:**
  - `drying fish` (food 1.0, spoil 0.15, decays as drying meat);
  - `dried fish` (food 2.0, spoil 0.02, decays as dried meat).
  
  All calibrate.
- **One rack:** fish and meat count against the same rack's room (`keeping.room`: what hangs with the drying-meat decay), so a hearth holds
  one batch of 8 of either or both.
- **A sign:** the smell of fish drying in smoke at a house, as for meat (`signs.py`).
- **The same batch minimum** as meat: a batch of less than 0.1 fish is refused (W-57).

## Why

- **Zach (17 Nov):** "fish can go on the hearth rack."
- **The lake runs (38.75):** a fishing household had no way to keep its catch. There was no salt in the world and no smokehouse built,
  and `dry meat` took meat only.

## Alternatives considered

- Fish only in a smokehouse (as before). It kept the smokehouse's role, but left a fishing household nothing at the hearth.
- A separate rack for fish at a hearth. This would double a hearth's drying, against the one-batch rule (brief 5 choice 1, OPEN Q-53).

## Open questions

- The spec text belongs in the economy spec (37.2's: goods.md, a `dried fish` row). It is asked of 37.2 in OPEN.
- Calibrate: dried fish's food and spoil.

## Affects

engine/data.py (ITEMS, TECHNIQUES), engine/signs.py (the smell), tests/test_cybertron2_lake_fixes.py.

## History

- **17 Nov 2026:** built at Zach's word on branch `lake-fixes` (W-57) and written up as retrospective, accepted: D4-122.

## Sources

38.75 (the lake runs); 38.77 (the build note); brief 4 §5 and 4c §6 (drying), brief 5 §4a (the smokehouse).

*Current as of 17 Nov 2026.*
