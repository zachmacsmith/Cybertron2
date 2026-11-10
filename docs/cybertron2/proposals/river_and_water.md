# River and water: the runs, the weir and what lives by the water: build brief 5

**Status:** draft (10 Nov), for Zach's go after brief 4. **Build brief 5** for the wild layer: pack K4 (02zv §4) without its fen-only
and boat parts, on the engine as built by briefs 1 to 4.
**Owner:** 37.2 (author; the wild pack's data, `engine/wild.py`, the ecology; the test worlds from the generator). Works on a water
parcel, their condition and the manual are 37.4's (§6).
**Affects:** spec/environment/wildlife.md; spec/economy/buildings.md (the weir as a work); on the branch: `wild/kinds.py`,
`wild/ecology.py`, `wild/areas.py` (`down`), `engine/wild.py`, `engine/data.py`, `engine/night.py`, `engine/signs.py`.

## Summary

What exists:
- **Kinds:** eels as a kind that moves on a cue (`mover: cue`: the autumn run on rain after dry weather); wildfowl; heronries and
  beaver lodges as sites, with their signs.
- **Methods:** `trap in water` as a set work, `net` for flocks of fowl, `fish by hand`, the fishing rod, salt fish.
- **The land:** every area knows its downstream area (`land.down`), its river length and its lakes.

What is missing is the river as a **line that ties villages together**. A run starts upstream and reaches each village in turn, a
day or two later. A weir with its gap shut takes a share of everything passing and leaves less for those below. A salmon taken
before it spawns is a salmon fewer in three years. Cold drives the fowl onto open water and then weakens them. The otter robs the
traps, and the beaver's dam floods one meadow and fills a pond. This brief builds that, so the strongest commons between villages
(02zp §27: eels mattered in 13 of 20 villages) is physical.

## 1. For the builder

**This file holds for this brief.** Read:
- briefs 1 to 4 and their tests;
- 02zv K4;
- 02zp §27 (the eel analysis);
- on the branch:
  - `wild/kinds.py`: the eel's rows, `mover`, the `when` rows of `trap in water`; the heronry and beaver sites;
  - `wild/ecology.py`: movement;
  - `wild/areas.py`: `down`, `river_km`, `big_river_km`, `lake_km2`;
  - `engine/wild.py`: `take`, `_set_night`, sites, `cond`;
  - `engine/data.py`: TECHNIQUES `trap in water`, `net`, `fish by hand`, `break a dam`;
  - the climate's rain and frost by node (D4-109);
  - brief 4's shelter levels, for the weir's condition.

**Do not** name kinds in rule code (a run is a mover's rule over any kind with `mover: run`); invent rivers the land does not have;
cap signs. Dry runs only.

**Branch:** `ecology-water`, from brief 4's branch.

**Worlds:** 37.2 supplies two generated worlds with the land kept (D2-208): two villages on one river, one upstream of the other;
and a lowland village with a lake. They are made with `cybertron2/specs/make_wild_tests.py`.

## 2. The run along the river (C6 on `land.down`)

1. **A run** is a mover's rule over any kind with `mover: run` and a direction (down to the sea, or up to spawn).
   - The eel's silver run goes down in autumn; the salmon and the lamprey go up.
   - The cue is the kind's own `when` row: for the eel, rain after dry weather in autumn, on dark nights. It is read over the
     **catchment**: the rain on the area and on its upstream areas over the last days, through `land.down` reversed.
2. **The lag:**
   - The run leaves an area on its cue night and reaches the next area down after about a day for each 10 km of river between them
     (`river_km`; calibrate).
   - So a village downstream sees the run a day or two after the one above, and one who has watched the upstream village knows it
     is coming.
3. **Numbers:**
   - The eels running are a share of each area's eels (the silver eels, about a fifth a year; calibrate). They leave the area's
     count as they pass, so the run thins as it goes, and what reaches the sea is gone.
   - The stock is made up by elvers coming up in spring, by the area's suitability (the ecology's growth). Years of heavy takes lower
     the run that follows.
4. **What it gives people:** on a run night at a village's water, `trap in water`, `net` and `fish by hand` take from the run by the
   take rule (stage A of brief 4), with the run's density in place of the resident stock. The `when` multipliers built in brief 1
   become the run itself.

## 3. The weir (a standing work on a water parcel; C7)

1. **Built** at a water parcel on a river by a crew: stakes and wattle (timber) and units. It is a work with a condition (brief 4's
   levels): floods and ice wear it, and it is mended like a building.
2. **The gap:** open or shut, set by an act at the weir (`set` with a gap, as shutting is built).
   - **Shut:** the weir's traps take a share of every run passing (about half when sound; less as it wears; calibrate), into the
     weir's set things.
   - **Open:** it takes little and lets the run pass.
3. **Downstream:** what a shut weir takes is not there below. The next village down sees the run thinner by that share, on the lag
   day. Two shut weirs on one river leave little for a third.
4. **Robbing:** the weir's set things, like any set thing, can be emptied by anyone at the parcel. Taking from another's leaves a
   trace (D4-48), read by those who know the weir.
5. **Signs:** the weir and its gap seen at the parcel; the run seen ("eels thick in the weir's traps"); below, "the run was thin
   this year" for those who know it.

## 4. The kinds on the water

| Kind | What to add (data on the rules, unless said) | Test |
|---|---|---|
| **eel** | `mover: run`, down, autumn; silver share; elvers up in spring; meat 0.2 (brief 4) | the run reaches each weir on its lag day; years of heavy takes thin it |
| **salmon** (new kind) | RESOURCES and ecology rows: in areas with a big river; `mover: run`, up in autumn and early winter, to the upper areas; returns in about three years by the spawners that reached the upper areas; meat about 2; taken at weirs, by net and by spear (`stalk` on water as a method's use, or `fish by hand`) | a year of shut weirs lowers the run three years on |
| **lamprey** (new kind) | on the same module, up in spring; small meat; for the lord's table later | a spring run at the weir |
| **wildfowl** | pushed by cold: frost on the land raises the fowl on open, unfrozen water at the node (the climate's frost; lakes and big rivers stay open longest); after a long freeze they weaken (flee lower, so easier to take), then die (the great-freeze regime, built); survivors return | a freeze crowds the open water and makes nets pay; a long one empties it |
| **otter** (new kind) | in areas with rivers; diet fish and eels; takes from set things in water and from weirs at night (brief 2's targets, `water: true`); hide; trapped by `snare` set at water | an unwatched weir loses part of its catch to an otter; trapping it stops that |
| **beaver** (the site, built) | the dam floods the meadow below: the meadow parcel next to the lodge's water loses hay (a cut, calibrate) and the water parcel's fish stock rises; `break a dam` (built) ends both for a season; trapping takes the pelt and castoreum (built) | the dam lowers the meadow's hay and raises the fish; breaking it reverses both |
| **heron** (the site, built) | herons take fish from the village's water and from a fish pond (a cut of its stock); the heronry's size follows the fish | a big heronry lowers a small water's fish |

## 5. Not in this brief

- **Fen only:** the decoy pond (it needs a trained dog, K6), reedbeds, crane and bittern with drainage, the fen ague. They wait on
  the generator making fen worlds with people: none of eight seeds passed its capacity check (02zzd, 37.2's to fix).
- **Boats:** punts and coracles (water_and_preservation.md, stage A of boats).
- **Retting** flax and crayfish downstream; the pearl mussel; eel spearing in winter: later (K4's low ranks).
- **Forays to the river beyond the village:** the forays track (OPEN L-105).

## 6. Touches in 37.4's files

- **`data.py`:**
  - TECHNIQUES `build weir`, and the weir's gap as `set`;
  - the weir as a work with a structure (timber);
  - RESOURCES `salmon`, `lamprey`, `otter`;
  - ITEMS for salmon (or `fish`).
- **`night.py`:** the weir's condition by floods and ice (brief 4's levels and weather).
- **`signs.py`:** the run, the weir and its gap, a thin run below, the dam's flooded meadow.
- **The manual:** the weir's acts for those who know them.
- **37.2's own:**
  - `wild/kinds.py`: the run rows, the new kinds;
  - `wild/ecology.py`: runs along `down`, with the lag, the silver share and elvers;
  - `engine/wild.py`: the run as a take's density; the weir's take;
  - the test worlds.

## 7. Tests (the gate)

**Unit:**
- A run leaves an upstream area on its cue and reaches each area below on its lag day, thinner by what was taken.
- A shut weir takes about its share, and an open one takes little.
- A weir's set things can be emptied by another, leaving a trace.
- Salmon returns follow spawners.
- Frost crowds the fowl onto open water, and a long freeze weakens and then kills them.
- An otter takes from an unwatched weir.
- The beaver's dam cuts the meadow's hay and raises the fish; breaking it reverses both.

**Society-level** (dry, scripted, the two-village river world):
- The downstream village's run-night catch falls by about the upstream weir's share when that weir is shut, against open.
- Three years of shut weirs lower the salmon run.

**Food a unit:** 02zzd's harness extended to run nights (traps, nets, the weir). An eel run night should pay well for a few nights
a year (a target: about 1 to 2 food a unit at a weir on a run night, near nothing otherwise; calibrate).

**Regression:**
- The probe worlds with bots.
- Worlds without rivers unchanged.
- All tests pass.

**Gate:** the above and a short dry-run report to Zach; then a small live run on the river world if he allows one, read against the
pack off: crews on run nights, weirs built and kept, the gap disputed between the villages.

## Why

- 02zp §27: eels mattered in 13 of 20 generated villages. They are the strongest commons between villages that the land already
  holds.
- 02zv K4 ranked the eel run with its lag, traps, the weir and its gap, salmon and wildfowl first in water worlds.
- Zach (10 Nov): build the other wildlife before forays.

## Alternatives considered

- **Eels as a resident stock with a seasonal multiplier** (as built): no line between villages, so no upstream and downstream.
- **The weir as a fitting with a fixed yield:** simpler, but nothing passes it, so it has no effect downstream.

## Open questions (for Zach)

1. The salmon's three-year return compressed into the world's years (a year is 32 days), or shortened.
2. Whether the weir's gap has a customary rule seeded in any world (no: nothing social is forced), or is only physical (proposed).
3. The run-night target at a weir (§7).

## History

- 10 Nov 2026: written by 37.2 as brief 5 at Zach's request ("rewrite the briefs to address the other aspects of wildlife in the
  first briefs before any foraging").

## Sources

02zv §4 (K4); 02zp §27; hunt_and_fixes.md (brief 4); briefs 1 to 3; wild/areas.py (`down`); water_and_preservation.md; D4-48,
D4-109, D2-208.
