---
id: docs/review/37_growth/02zzzl_waters_calib/brief.md
kind: note
updated: "2026-11-23"
---
# Brief: the waters calibrated across many generated environments (thread W-108)

*note · `docs/review/37_growth/02zzzl_waters_calib/brief.md`*


Session 37.2, 23 Nov 2026. Two agents work from this brief: **A, the sweep** (sections 1 to 5) and **B, the generality read** (section
6). Neither edits engine code, specs or the design files; each writes its own files in `docs/review/37_growth/02zzzl_waters_calib/`
(scripts beside them) and commits only those, on main, with `git add <your files>` and a plain `git commit` whose message's last
paragraph is exactly:

```
Agent: 37.2
Thread: [[W-108 The waters calibrated across many generated environments|W-108]]
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

(no other trailers; do not use `records.py commit`, which sweeps in other sessions' record work). Then `git pull --rebase` and
`git push origin main`. No model calls, no live runs; generated worlds and the ecology without people (or with bots, [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]) only.

## Zach's question (23 Nov)

"Right now for these worlds weren't the runs scheduled specifically according to set times while in reality we want them to have
probabilities with different conditions. I want you to do a calibration across a bunch of different generated environments, water
ways at once, to test that it is working in different situations, and look at both how resident fish and shallows populations vary
based on water sizes and shapes and different types, and also are there different types of fish in different places? And then
explore different conditional effects on when runs happen and if we should add other runs, overall seeing what changes total food
quantities that go past. How well is this system currently built as a generalized system of mechanisms that would work robustly
across diverse environments vs overengineered for the specific test worlds that we ran?"

Decided just before ([[D2-347 A water-only village should be able to last the year|D2-347]], [[D2-348 A water-only village is made able to last the year by|D2-348]]): a water-only village should be able to last the year; to that end stage 5b adds a spring
calendar (a lamprey run, coarse fish spawning in the shallows in spring) and resident fish and shallows big enough to matter, at
their best about a quarter of the village ([[D2-316 A runs world means a water-only world|D2-316]] still holds: water's resident fish alone do not carry it). This study is the
evidence base for building that generally, not for Eelmouth alone.

## What is known (37.2, from the code; confirm, do not assume)

- The runs are not set dates: `cybertron2/wild/runs.py` and `kinds.py` `RUNS` give each run kind a season window, a weather cue over
  the catchment (`rain_after_dry`, `spate`) and a nightly share; the up-runs' heads come from last year's spawners (Beverton-Holt,
  `cap_km` a km); the rest enters on the window's last day. Three run kinds only: eel (down, autumn), salmon (up, autumn and early
  winter, big rivers), lamprey (up, spring). Whether this behaves as probabilities under conditions, or as near-fixed dates, is
  for the sweep to measure.
- Resident fish are one generic stock `fish` a water body (`engine/waters.py`, [[D2-229 One fish stock per water body|D2-229]]): Eelmouth's reach holds K 8.8 kg (about
  0.3 food a night at best). `make_water_worlds.py` says fish are "stocked after generation as the peoples worlds do (OPEN [[L-75 The generator's lakes and heat target|L-75]])".
  The shallows are per parcel ([[D2-317 The shallows are one stock per parcel, distinct from the resident…|D2-317]]; `cybertron2/wild/water.py`, `engine/verbs.py` near the shallows take).
- Live run 1 set B's year: docs/review/37_growth/02zzzh_hunt_fish/spring_gap.md.

## Read first

CLAUDE.md; `docs/scenario_design.md`; `docs/cybertron2/proposals/river_and_water.md` (brief 5) and `w73_design/u1_water.md` (with
its "Decisions since" table); `cybertron2/wild/runs.py`, `river.py`, `water.py`, `kinds.py` (RUNS, the fish rows), `engine/waters.py`,
`engine/renewal.py`, the river and shallows parts of `engine/wild.py` (`_runs_night` and around) and `engine/verbs.py`; the land
generator (`cybertron2/landgen/`: `physical.py`, `ecology.py`, `write.py`) and the world makers (`specs/make_water_worlds.py`,
`make_nutrition_runs.py`, `make_eelmouth.py`, `specs/calibration/make_calibration_worlds.py`); the open items that bear on this:
[[L-75 The generator's lakes and heat target|L-75]], [[L-100 Landscapes still to tune|L-100]], [[L-114 The river high or in spate as a sign|L-114]], [[L-116 The wild layer's fish and a water body, two ways|L-116]], [[L-150 Environmental effects on fishing refined after the rest works|L-150]] (`python3 tools/records.py show L-n`).

## A: the sweep

1. **A set of generated environments, at once:** at least 30 worlds from the land generator across seeds and settings, so the set
   holds big lowland rivers, small rivers, becks and brooks, lakes and meres, fens, an estuary or coast if the generator makes one,
   upland and lowland, wet and dry climates, villages high and low on their river. Say how each was made (the call, the seed, the
   settings) so it can be remade. Where the generator cannot make a kind of water, say so; that is a finding.
2. **Resident fish and shallows:** for every water body and water parcel, its K, r, renewal and starting S, against its size (river
   km, km2, margin), shape, kind and place; whether the values come from the generator's physics or from a maker's hand stocking;
   their best sustained yield in food a night (r K / 4 x food a kg) against a village of ten (about 11 food a night). Plot or
   tabulate by water kind and size. Are there different fish in different places (kinds, by water)? Today, and what the engine's
   data could hold.
3. **The runs:** run the ecology without people (or with bots) for at least three years on each world (the wild layer's own night
   loop; find the cheapest faithful way), and record per run kind and year: the first and last night it passed the village's
   water, the nights it ran, the heads and kg that passed, and what triggered each night (the cue, the window's last day). How
   much does the timing vary across years and worlds, and with what (rain, flow, river size, the spawners)? Is it a probability
   under conditions or a near-fixed date? How often does a run fail or come all on one forced night?
4. **Food passing in a year:** for each world, the food that passes the village's water by month or season, from each source
   (runs by kind, resident fish at best yield, shallows), against a village's need by season; where the gaps fall and how deep, by
   water kind. Show which settings change the total most (river size, climate, the village's place on the river, dams).
5. **Experiments on the conditions, run on copies of the data, never in the engine:** what changes if a run's timing were drawn
   from conditions (water temperature or season's warmth, flow, rain, the moon as a later idea) rather than a window; what other
   runs a temperate lowland river would have (spring lamprey sized as real, elvers and glass eels, shad, sea trout, smelt, spring
   salmon, coarse fish spawning in the shallows: pike, perch, bream, roach, tench) and what each adds by season; resident stocks
   sized from real productivity (kg a hectare a year of a river, a lake, a fen water; cite sources by name) against today's. For each,
   the year's food passing and the spring gap.

**A's output:** `sweep.md` (the method, the worlds, the tables, the findings, with every number from a script run), the scripts,
and the data as small text or JSON files. End with what the sweep recommends for stage 5b part 4 and what it found broken.

## B: the generality read

6. **An independent read of the waters' code** (do not read A's files; A and B run at the same time): how general are the
   mechanisms (water bodies, resident fish, shallows, runs, the river's record, the weir, the signs that read them) as a system that
   works across diverse environments, against fitted to the test worlds? Find: constants and thresholds tuned to one world (cite
   the comment or commit that tuned them, file:line); kinds or places named in code where a rule should read data; behaviour that
   only a hand-written maker supplies (hand stocking, pinned waters); paths a generated world never reaches; conditions that are
   windows where they should be conditions; what a new run kind or a new resident kind would need to be added (data only, or code);
   and what breaks or goes silent on a lake, a fen, a beck, an estuary, a dry year, a dam. Grade each mechanism (general; general
   with fitted constants; fitted; missing) with the evidence.

**B's output:** `generality.md`, every claim with file:line, ending with the changes that would make it general, ranked by how much
they matter for worlds other than Eelmouth.
