---
id: L-51
kind: deferred
state: open
updated: "2026-11-22"
---

# `landgen.physical._spread` reaches farther than its steps (L-51)

*open · 37.2*

## Later
**`landgen.physical._spread` reaches farther than its steps:** its directions update in place, so one step can chain several cells (asked for 15 cells, it reached 31). The resource pin now tests the distance itself; the other uses (springs, flood height, wetness, site water) are calibrated as they behave, so a fix would retune them

**Decided:** 2 Nov (found building the ladder)

**Designed in:** landgen/physical.py, settle.py

**Waits on:** none


## Linked
- bears on: [[W-54 The twelve calibration worlds and an audit of the generator across…|The twelve calibration worlds and an audit of the generator across… (W-54)]]


## Mentioned by
- [[W-11 Landscapes still to tune|Landscapes still to tune (W-11)]]
- [[The dependence ladder (OPEN L-50)|The dependence ladder (OPEN L-50)]]
- *and 2 index or audit notes*
