---
id: docs/review/38_space_engine/77_lake_fixes.md
kind: note
updated: "2026-11-17"
tags: [note, open]
---
# 38.77: The lake runs' faults, fish on the hearth rack, and a signs pass (build note)

## Text
# 38.77: The lake runs' faults, fish on the hearth rack, and a signs pass (build note)

Session 37.4, 17 Nov 2026 (WORK [[W-57 The lake runs' seven engine faults (38.75 a death told to one mem|W-57]]). Branch `lake-fixes` (from `floodplains`), not merged. The tests are in
tests/test_cybertron2_lake_fixes.py.

## The seven faults (38.75)

1. **A death in the night told to one member.**
   - The cause: old age's and starvation's death events carried no `concerns`, so they were read only by the evening rule's chance
     and its cap of 5 lines.
   - The fix: `life.death_told` gives the event the dead one's whole household and everyone who slept under the same roof that night,
     and names the house in `about`. Housemates read it in full (perceive.happened_to); household members elsewhere read it by the
     rule.
   - It applies to old age, a young one's death and hunger.
2. **`travel` to a parcel in one's own village refused with "the open road" three times.**
   - Naming a parcel here now says: "{place} is here at {village}, not a road away: name it as where you work in the act itself
     ("at": ...), and you go there to do it."
   - Ways of the same name are told apart by where they lead ("the open road to the east"), from the places' positions (y north), or
     numbered when they have none (`Here.roads`).
3. **Herding "for my household" took another household's herd.** Unnamed, `farm._herd_on` takes one's own household's beasts first. A
   herd named by its name or tag is still taken as named.
4. **The cat sign said "it came to your hand" when it did not.** A find row now carries what is said when it comes ("it came to your
   hand") and when it does not ("it watched you a while and slipped back into the hedge"). The draws are unchanged.
5. **A drying batch printed unrounded** ("2.9525"). The made line rounds to 2 places; what is stored is unchanged.
6. **A drying batch of nearly nothing** ("0.0286 drying meat (from 0 meat)") held the rack 3 nights.
   - The fix: a batch of less than 0.1 of its input is refused (`verbs.BATCH_LEAST`, calibrate): "there is too little to make a batch (...): it takes at least 0.1".
   - It is 0.1, not 1 as asked, because brief 4c §6.1 lets a hare's meat (0.7) hang, and its test holds that.
7. **The killing frost said "the water is frozen through"** on water that stays fishable. The water clause is dropped (Zach: ice
   stopping fishing is ignored for now).

## Fish on the hearth rack ([[D4-122 Fish on the hearth rack|D4-122]])

`dry fish` at a hearth or fire ring:
- a batch of up to 8 fish, 3 nights, into `dried fish` at half the weight (food 2.0, keeping as dried meat; calibrate);
- one rack with meat (the room is shared);
- a smell sign as for meat.

Records: proposals/fish_on_the_rack.md; OPEN [[L-115 Dried fish in the economy spec|L-115]] asks 37.2 for the goods row in the economy spec.

## The signs pass (17 Nov, accepted in conversation)

11 built; 9 (a lake's fish thinning) waits for the water-body stock; 3 (the river in spate) is deferred, OPEN [[L-114 The river high or in spate as a sign|L-114]]. Each sign, its
state and its rows are in proposals/signs_pass_17nov.md. The state added:
- the trace names the beast or the house of a raid (`beast`, `house`);
- a building's `spoilt` (schema);
- the wild layer's `wary_seen` (by parcel);
- a road trace of kind `fight` (`ROADS.trace_days` 2).

The rest read existing state: `broke.by`, `robbed_by`, `set.wrecked`, the run's passings, `frozen_run`, the great freeze, a rack
outside, a party's transit.

## Noted, not changed

- **`make` at a full own rack** goes on to another household's hearth at the village (KN.where and the site order). Seen in the rack
  test, and not changed here.
- **Calibration:** the new rows' `own` follows the nearest rows of their kind. senses.md's chance tables for them are not yet measured
  (a bot run).

## Tests

- The fault and rack tests: 8.
- The signs pass: 10.
- The full suite on `lake-fixes`: 659 pass and 15 fail. The 15 are 37.2's list on the old layouts (water5_fowl 9, water5_river 2,
  water5_keep 1, wild 1, wild_range4c 2), which are the other fork's on `water-bodies`.
- The world schema is now 11 (`buildings.spoilt`). If `water-bodies` also bumps it, the merge renumbers one of them.

*Current as of 17 Nov 2026.*

