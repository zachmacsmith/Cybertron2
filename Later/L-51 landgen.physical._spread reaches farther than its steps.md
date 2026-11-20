---
id: L-51
kind: deferred
state: open
owner: "37.2"
updated: "2026-11-20"
tags: [deferred, open]
---
# `landgen.physical._spread` reaches farther than its steps:

- **state**: open
- **owner**: 37.2
- **waits_on_text**: none

## Text
**`landgen.physical._spread` reaches farther than its steps:** its directions update in place, so one step can chain several cells (asked for 15 cells, it reached 31). The resource pin now tests the distance itself; the other uses (springs, flood height, wetness, site water) are calibrated as they behave, so a fix would retune them

## Mentioned by
- [[W-11 Landscapes still to tune (OPEN L-100); the generator's _spread re|W-11: Landscapes still to tune (OPEN L-100); the generator's `_spread` reach]]
- [[dependence_ladder The dependence ladder (OPEN L-50)|The dependence ladder (OPEN L-50)]]
- [[02zz_open_sorting 02zz sorting OPEN.md's open rows into the new kinds|02zz: sorting OPEN.md's open rows into the new kinds (draft,]]
