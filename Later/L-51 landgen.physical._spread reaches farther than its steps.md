---
id: L-51
kind: deferred
state: open
updated: "2026-11-20"
---

# L-51 · `landgen.physical._spread` reaches farther than its steps

*open · 37.2*

## Later
**`landgen.physical._spread` reaches farther than its steps:** its directions update in place, so one step can chain several cells (asked for 15 cells, it reached 31). The resource pin now tests the distance itself; the other uses (springs, flood height, wetness, site water) are calibrated as they behave, so a fix would retune them

**Decided:** 2 Nov (found building the ladder)

**Designed in:** landgen/physical.py, settle.py

**Waits on:** none


## Mentioned by
- [[W-11 Landscapes still to tune|W-11 · Landscapes still to tune]]
- [[The dependence ladder (OPEN L-50)|The dependence ladder (OPEN L-50)]]
- *and 1 index or audit notes*
