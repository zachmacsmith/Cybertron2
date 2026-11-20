---
id: docs/cybertron2/proposals/signs_pass_17nov.md
kind: proposal
updated: "2026-11-17"
---
# A signs pass after the lake runs (17 Nov)

*proposal · retrospective, accepted in conversation (17 Nov 2026: Zach, "Yess I agree add th · `docs/cybertron2/proposals/signs_pass_17nov.md`*

> A read-only review proposed signs for state the engine changes and nobody could sense. Each is written to docs/cybertron2/guides/senses.md: - grounded in state; - a change, not a standing fact; - its chance from the one rule (`own`, never a `p` on a new row).


**Status:** retrospective, accepted in conversation (17 Nov 2026: Zach, "Yess I agree add them"). 11 built, 1 to follow, 1 deferred.

**Owner:** 37.4.

## Summary

A read-only review proposed signs for state the engine changes and nobody could sense. Each is written to docs/cybertron2/guides/senses.md:
- grounded in state;
- a change, not a standing fact;
- its chance from the one rule (`own`, never a `p` on a new row).

They were built on branch `lake-fixes` ([[W-57 The lake runs' seven engine faults|W-57]]) with tests in tests/test_cybertron2_lake_fixes.py. The numbers are the review's.

## Built

1. **A raid on the dead or on food left at a door.** It had fallen back to the crop, herd or hen text. Now it has its own rows
   (kinds.RAID_SIGNS "carcass" and "door", any kind). Carcass and left-out targets carry a `sign`, and the trace names the beast or the
   house:
   - "the dead {beast} at {place} dragged and torn open in the night, the ground trodden round it";
   - for hunters, "{kinds} were at the dead {beast} at {place}";
   - "what was left at the door of {house} is gone: scraps and tracks".
2. **Wear on a weir.** It is no longer the house's roof text (signs.WEIR_BROKE, chosen by `wild.is_weir`):
   - "stakes torn out of {weir}, a stretch of wattle gone: the river runs through the hole";
   - in ice, "ice piled against {weir}, the stakes leaning".
4. **Fish going off in a store.** It spoils to nothing at x2, so the rotting rows never fired. The night now keeps `spoilt` on the
   building (fish, dried fish, salt fish; at least 0.2 lost). The morning after, by smell, for those at or in it: "the {fish} in {house}'s
   store going soft and starting to smell: it will not keep".
5. **A trap emptied by an otter** (`robbed_by`), on the close look (things.look_text): "your wicker traps at {place} torn at the neck,
   scales and a fish head on the withies: something has had what was in them".
6. **Traps full during a run.** A trap in water within 0.25 of its hold (3 food; a weir's `weir_hold`), on a day a run passes. Only for
   the setter or the weir's crew there: "the traps at {place} crammed full: whatever comes down now goes past".
7. **Traps smashed in a spate** (`wrecked`), that day and the next:
   - for the setter, "your wicker traps at {place} smashed against the bank in the spate" (also in their look);
   - for others, "broken wicker in the reeds below {place}".
8. **Fowl back on the thaw.** On the first day not frozen after a frost that froze the village's water over:
   - "duck and geese back on the water at {place} with the thaw";
   - for fowlers (`net`), after a great freeze (frozen_run 4, which killed a share of them), "..., fewer than before the freeze".
10. **Rain on meat or fish drying at a fire outdoors** (a rack outside, raining, not snow), at the parcel only: "rain on the {meat|fish}
    drying by the fire at {place}: wet and slimy, flies at it".
11. **Wary game for an ordinary hunter.** The hunt keeps the day a kind's learned wariness passes 0.3 on its ground (`wild.WARY_SEEN`,
    `wild.wary_seen`). That day, for those who know hunting, on the parcel: "the {deer} break and run long before you are near: hunted
    too often here".
12. **A fight on the road leaves a trace** (`kind: fight`, trace_days 2), seen on the stretch that day and the next:
    - "the ground by the road trampled and scuffed, dark spots of blood on it";
    - for hunters, "two people fought here, a day or two since: one went on toward {toward}, one back";
    - in snow, "blood trodden into the snow by the road".
13. **A party on a road's last stretch toward a village**, seen from its built parcel. That place is a presentation choice, named in
    the code: the engine does not place a road's end in the village. By day, not in rain or snow; the rule lowers sight in fog and the
    dark: "figures on the road from {from}, still far off, coming this way", adding "; one of them carries a club or a spear" when one
    does.

## To follow

9. **A lake's fish thinning.** It waits for the water-body stock ([[D2-229 One fish stock per water body|D2-229]], branch `water-bodies`, [[W-56 One fish stock per water body, the engine half|W-56]]).

## Deferred

3. **The river high or in spate.** The night's flow is not kept in state. It is flagged in OPEN, waiting on the flow level being kept
   ([[D2-215 The weir's runs the river's level, then re-measure|D2-215]]).

## Calibration

Each row's `own` follows the nearest existing row of its kind:
- the raid rows as the stores raid (0.9 to 0.95);
- the store smell above the rotting store (1.2);
- the thaw and the party far off below a near sight (0.8 to 0.9).

The chance tables of senses.md's checklist step 4 are not yet measured for these rows (to do in a bot run).

## History

- **17 Nov 2026:** proposed by a read-only review; accepted by Zach in conversation; built on `lake-fixes` ([[W-57 The lake runs' seven engine faults|W-57]]).

## Sources

The review's list (17 Nov, via the coordinator); docs/cybertron2/guides/senses.md; 38.77.

*Current as of 17 Nov 2026.*
