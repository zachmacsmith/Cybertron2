---
id: Q-65
kind: ask
state: open
updated: "2026-11-20"
---

# Q-65 · Delete the 16 empty branches

*open · Zach (37.2)*

## The question
16 remote branches hold nothing that is not on main (4c-dry, 4c-hunt, 4c-pred, 4c-sets, climate-calibration, ecology, ecology-calibrate, ecology-carcass, ecology-hunt2, ecology-hunt3, ecology-methods, ecology-raiders, peoples-worlds, use-by-physics, weather-by-place, w65-records; records branches). [[D2-238 Branches|D2-238]]: no empty branches. This session's git proxy refuses deletes (403), so they need deleting on GitHub, or a token that may delete

**Recommended:** delete all 16 (nothing is lost: each is on main)

**Where:** python3 tools/records.py branches


## Linked
- parent: [[W-65 Tracking threads automatically|W-65 · Tracking threads automatically]]
