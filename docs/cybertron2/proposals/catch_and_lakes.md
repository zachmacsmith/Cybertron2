# Luck in the catch, a lake's fish by its size, and a fishing household

**Status:** retrospective, accepted: D4-119, D4-120, D4-121 (17 Nov 2026). Built on `ecology-water` (f6fbb83, 4f580ca).

**Owner:** 37.4. The water worlds and their data are 37.2's (make_water_worlds.py); these changes were made at Zach's request.

## Summary

- A catch by hand or by rod now has luck in it.
- A lake's fish are sized by the lake's area, with a slow regrowth.
- A water village has a household that knows nets and wicker traps.

## What was built

1. **Luck in the catch (D4-119).**
   - A `stock` yield with `spread` draws each unit's catch from a uniform between (1 − spread) and (1 + spread) times the expected catch.
     The expected catch is the method's most × the stock's fullness (S/K) × skill and tool. The draw never takes the stock below its
     refuge.
   - `fish by hand` (0.6) and `angle` (1.5) have spread 0.5. Other stock yields (gathering) are unchanged.
   - The mean is exact, so the capacity model reads the same.
2. **A lake's fish by its size (D4-120)**, in make_water_worlds `water_stocks`:
   - a village's largest water parcel on a lake (at least 0.5 km² in its home and ring) holds K = LAKE_FISH (7,500 a km²: about 150
     kg a hectare at about 2 kg a fish unit) × the lake's area;
   - it regrows at r = 4 × LAKE_TURNOVER (0.4 a year) × K × 32/365 ÷ K ÷ 32, under the `threshold` rule. That is plain logistic
     regrowth with no 1% refill of the gap, and no regrowth below 15% of K;
   - so the stock is not scaled by the short year (a fish in the lake is a fish), and its flow is, as harvests are;
   - Meresby's mere holds 19,575, gives at most about 690 a world year, and the capacity model reads 557 a year for good;
   - other water keeps K 8 a unit of size, as a fast stock.
3. **A fishing household (D4-121)**, a stopgap for proposals/livelihood_archetypes.md:
   - at each village with fish in its water, the largest household's adults know `net` and `trap in water` (skill 1.2);
   - in the runs-only world, every household does.

## Why

- **Zach (16 to 17 Nov):**
  - "For now, let a fishing household know nets and traps";
  - "it's a pretty big lake";
  - "would not the limit on fishing be the extraction not the store itself? for a big lake scaling capital would get more until it
    is overfished";
  - "yes, add the small chance, then change the capacity of the lake to make sense then do another version of the run".
- **The first lake run (38.74):**
  - the village's only fish water was a pond the generator named the Brook, fished out in ten days;
  - nobody knew nets or traps.

## Alternatives considered

- **The lake at 16** (8 a unit of parcel size): a pond's stock, about 34 food a year for a 2.6 km² mere.
- **The lake's stock at its area with a pond's regrowth** (r 0.3, a fast stock): about 41,000 food a year, absurd.
- **Scaling the stock itself by the short year:** wrong, because the stock is fish in the water now and only flows are compressed.
- **A chance of a catch or nothing,** rather than a spread about the mean: more lumpy, less like a day's fishing.

## Open questions

1. LAKE_FISH and LAKE_TURNOVER are from memory, not researched: real lakes hold roughly 50 to 300 kg a hectare and produce 30 to 60%
   a year. For 37.2 to calibrate (OPEN L-75).
2. Rivers and big rivers keep K 8 a unit of size: their resident fish by length and flow.
3. The water measure's double count (37.2's branch `water-measure`) bears on the wild fish-eaters, not on these parcel stocks.

## History

- **17 Nov 2026:** built and recorded after a day of back and forth.
  - 16 became 19,575 with the pond's regrowth (absurd), then was reverted to 16.
  - Then came the split between the stock (the area, unscaled) and the flow (scaled), with the threshold rule.
- **17 Nov 2026 (later):** D4-120's per-parcel lake stock is replaced by D2-229 (one fish stock per water body, 37.2's decision), built
  on branch `water-bodies` (38.76): the body holds the stock once, every parcel on it shares it, and the lake's K is to be sized from
  the whole lake (37.2's calibration, D2-228).

## Sources

- docs/review/38_space_engine/74_lake_run1.md
- cybertron2/engine/yields.py
- cybertron2/specs/make_water_worlds.py
- cybertron2/engine/renewal.py

*Current as of 17 Nov 2026.*
