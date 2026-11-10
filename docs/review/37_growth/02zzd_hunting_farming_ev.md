# 02zzd: hunting, gathering and farming, food per unit of work, measured in generated worlds

The calibration below is taken into build brief 4: docs/cybertron2/proposals/hunt_and_fixes.md. The harness is in 02zzd_ev/.

37.2, 9 to 10 Nov 2026 (WORK W-22). Zach (9 Nov): "Generate some actual worlds from the generator and compare the desired expected
values from hunting and farming across the various conditions and see what seems off and needs calibrating." Code measured: 37.4's
branch `ecology-raiders` (`f290e2c`, briefs 1 and 2), read only.

## Method

- Worlds from the generator with people: seed 7 and seed 5 "settled lowland and frontier", seed 11 "upland and moor", seed 3 "sand
  country"; each in all four seasons; three settlements each. (Seeds 23, 31, 41 and eight seeds of "fen with islands" and two of "scarp
  and vale" were refused people by the generator's own capacity check: the land fed 0.6 to 0.85 of the people. That is a finding for
  the generator, below.)
- Each method at each settlement tried 60 times (set works 20) on a fresh copy of the world at its start, the draws varied, so nothing
  depletes between tries. Food is the edible goods gained (ITEMS food a unit; meat 1.5). Units are the method's plus the range's.
- Hunters: **novice** (the curve's low end, familiarity 0) and **skilled** (the curve's high end, familiarity 0.8 with every kind).
  Hunting was run twice: unarmed (four worlds) and holding a crude weapon (three worlds).
- Depletion: one armed, skilled hunter stalking every day for 16 days, nights run, with a control of 8 nights with no hunting; and one
  gatherer working one forest parcel six units a day for three days.
- Farming is computed from the engine's data, not run: seed 16 a plot, ratio 3, break gain 1.5, grain 0.7 food; hoe 16 units a plot,
  plough 4, sow 2.7, weed about 2, reap 8 (crude) or 5.3 (copper), manure 5.3. Breaking is spent at each sowing (farm.py, sowing moves
  `broken` into the crop), so it is a cost every year.

## Results: food a unit of work

| Way of getting food | Novice | Skilled | Notes |
|---|---|---|---|
| Farming, unbroken ground, crude reap | 1.77 | | per year, every year |
| Farming, hoe-broken | 1.37 | | breaking 16 units a plot |
| Farming, plough-broken | 2.35 | | |
| Farming, plough and copper reap | 2.80 | | |
| Milk, three cows | up to 2.4 | | |
| Gathering wild food, autumn (forest / open) | 1.16 / 1.07 | 1.72 / 1.48 | |
| Gathering, spring and summer | 0.28 to 0.57 | 0.40 to 0.77 | open ground better than forest |
| Gathering, winter | 0.19 to 0.31 | 0.28 to 0.43 | |
| Stalk, armed, the wood around (4 units) | 0.10 | 0.51 | success 13% and 73% a trip |
| Stalk, armed, far (6 units) | 0.06 | 0.33 | the same food a trip as the wood around |
| Stalk, armed, near (3 units) | 0.04 | 0.25 | the home area is 0.2 to 0.5 km² |
| Hunt the wild, armed, the wood around | 0.06 | 0.10 | mostly hares and pigeons |
| Stalk, unarmed, the wood around | 0.02 | 0.10 | the weapon factor is 0.2 unarmed |
| Snare, one snare a unit, one night | 0.04 | 0.08 | hares 0.18 meat |
| Eel trap, one night | 0.02 | 0.08 | eel 0.1 meat; the autumn run barely shows |

The targets agreed on 9 Nov:

| Hunter | Near a settled village | Far in wild land |
|---|---|---|
| Novice | 0.1 to 0.2 | about 0.5 |
| Master | 1 to 1.5 | 4 to 5 |

**Against them:**
- The novice near a village is on target (0.10).
- The master near a village is 2 to 3 times low (0.51).
- Far hunting misses most: the master is about 12 to 15 times low (0.33), and the novice about 8 times low (0.06).

**Gathering against farming:** autumn gathering, 1.1 to 1.7 a unit, is level with hoe farming for the few days a parcel lasts. The
rest of the year it is a quarter to a half of farming.

**Depletion:**
- *Gathering on one parcel:* day 1 gave 1.53, 1.55, 1.57, 1.25, 0.93, 0.68 over its six units. Day 2 started at 1.56 and day 3 at
  1.15, so a parcel recovers only partly overnight.
- *Daily stalking in the wood around* (roe in the ring of 19 km²):
  - with stalking, 196 fell to 14 in 16 days, of which only 7 were killed;
  - in the control with no hunting, 196 fell to 180 in 8 nights.
  - The red deer fell from 9 to 2, and none of them were killed.
  - The catch was a roe on 6 of the first 8 days and 1 in the last 8: 11.6 food over 64 units, or 0.18 a unit.
- *Daily stalking at far range:* red deer in the ring rose from 9 to 32, pushed in from the wild areas, then fell. The catch was 8 roe
  in 16 days, 0.14 a unit.

## What is off, and why (from the code)

1. **Meat per kill is 3 to 5 times too small against the engine's own cow.**
   - A slaughtered cow gives 40 meat, which puts one meat at about 3 kg.
   - On that scale a red deer would be about 20 meat (now 3.9), a roe about 4.5 (1.1), a boar about 15 (3.5), a hare 0.7 (0.18),
     a mallard 0.3 (0.2) and an eel about 0.2 (0.1).
   - This is the rescale proposed on 9 Nov, and it alone moves the master near a village to about 2.2 a unit.
2. **The master succeeds too often; the novice is close.**
   - The chance of a kill is `0.55 x skill x weapon x (1 - flee) x familiarity`. Skilled and armed, against roe, that is 0.77.
   - With the meat rescaled, a master would take a deer on three trips in four, at about 2 food a unit: reliable, not "very
     uncertain".
   - A wider, slower curve fits the targets, and the numbers below have it reach 3. That is skill 0.4 to 3 for the hunting methods
     with the constant lowered to about 0.19. On the rescaled meat it gives:
     - a master about 40% a trip, at 1.1 to 1.5 a unit;
     - a novice about 4% a trip, at 0.10 to 0.14 a unit.
   - Both are on target near a village.
3. **Range costs time but buys nothing.**
   - Whether anything is met is `1 - exp(-0.03 x weight x effort)`, where effort is the method's units over 2 and never the range's.
   - In the wood around, the chance of meeting a deer is already 0.9 to 1.0, so far range adds 3 units and no more meetings.
   - A trip meets at most one beast. The far areas also count for less (`1 / (1 + 0.3 x index)`).
   - So far range always does worse, and the 4 to 5 a unit target for the far master cannot be reached by any parameter.
   - What it needs: meetings over the time spent (a number of meetings by density, ease of finding and units, each with its own kill
     chance), wild land where the game is not wary, and a carry limit so that a red deer ends the trip.
4. **Seasons do not touch hunting.** The returns a trip were the same in all four seasons. The seasonal rows (the rut's detect x1.5)
   act on finding, and finding is already saturated. Once meetings scale with time (item 3), the rut, snow tracking and summer cover
   will show.
5. **Hunting pressure drives game out about ten times too hard.** This is my ecology (wild/ecology.py, kinds.HUNTED), not 37.4's
   code.
   - Each hunt adds 0.25 pressure to every area in reach, whatever its size. The ring is 19 km²; the home area is 0.4 km².
   - Each night a share of 0.2 times the pressure of the roe leaves, up to half of them.
   - One hunter a day therefore holds the pressure near 1 and moves a fifth of the roe in 19 km² out every night.
   - Fix: pressure by the ground a day's hunt covers, about 0.25 x min(1, 3 km² / the area's km²), and a lower share. One hunter
     should move 1 to 2% a night, and a crew working the ring daily much more.
6. **Hunt the wild pays least of all.**
   - Its takes weigh every kind at 0.99, foxes, stoats and wolves included (hide, no food). In the lowland, the hares (0.27 food)
     are 56 to 85% of what is met.
   - That is defensible as "whatever comes", but after the rescale it should be checked again.
7. **Snares and eel traps are a tenth of a modest top-up.**
   - One snare a unit catches 0.07 to 0.15 a night, and a hare is 0.27 food.
   - With a line set in one unit (about five snares, as proposed) and hares at 0.7 meat, a snare line would give about 0.3 to 0.5 a
     unit a night.
   - Eels at about 0.2 meat, with the autumn run multiplying the catch (now x2 to x3, which barely shows), would put the trap at about
     0.3 in autumn.
8. **Near the village is poor for the wrong reason.** The home area is tiny (0.2 to 0.5 km²), so few beasts stand on it. Their
   density there is the same as in the ring: the red deer are at 2.5 a km² on the home area and 2.1 in the ring. The ecology does
   not thin game near people. The result happens to fit the target, but by size, not by people.
9. **The labour cost is too small to matter.**
   - Work costs 0.04 food a unit, 0.24 for a day of six units.
   - So "worth it" is set by what else the units could do, not by the food the work burns.
   - At 0.10 a unit, a day's hunting (0.4 to 0.6 food) feeds the hunter about half a ration.
10. **The generator refuses most seeds** for the capacity check (seeds 23, 31 and 41; "fen with islands" on eight of eight seeds). The
    check may be right, but most configurations do not make worlds with three settlements of people. This is mine (W-11).

## Proposed calibration (for Zach, then 37.4's code; item 5 is mine)

| # | Change | Where | Expected effect |
|---|---|---|---|
| 1 | Meat a kill on the cow's scale (red deer 20, roe 4.5, boar 15, hare 0.7, fowl 0.3, pigeon 0.1, eel 0.2) | RESOURCES `taken.goods` | the master near a village x4 |
| 2 | Hunting methods on a curve of their own, 0.4 to 3, slower to learn; the kill constant to about 0.19 | knowledge.SKILL, wild.take | master about 40% a trip, novice about 4% |
| 3 | Meetings by time spent (the units with the range), several a trip, with a carry limit | wild.take | far pays when the near land is hunted or thin |
| 4 | Pressure by area hunted; flee share lower | wild/ecology.py, kinds.HUNTED (37.2) | one hunter moves 1 to 2% a night |
| 5 | A snare line in one unit; the eel run's multiplier shown | data, set works | snares 0.3 to 0.5 a unit; eels about 0.3 in autumn |
| 6 | Game thinner near people (a people-pressure term in the ecology's suitability) | wild/ecology.py (37.2) | near hunting poor by density, not by size |
| 7 | Rerun this measurement after 1 to 3 (the scripts are short) | 37.2 | |

Not changed: farming (1.4 to 2.8 a unit) and gathering, which are in the shape agreed. Farming's lead is in food per land and in
reliability, not food per unit, and autumn gathering matching farming per unit for a few days is realistic.

## Limits
- Each try is a single trip in a fresh world: no crews, no learning, no carrying home, and meat spoiling at 0.30 a night is not
  counted.
- Farming is from data, not a run.
- Per land is not measured. Using the capacity model's plot (64 grain from 16 seed, a cell of about 2 ha), the ring's big game, rescaled
  and taken sustainably, is about 15 to 20 plots' worth of food from about 1,900 ha. That rests on an assumed yearly offtake of about
  a fifth of the roe.

## Addendum, 10 Nov: brief 4 as built (`ecology-calibrate`, `58bb2d3`), checked by 37.2

**`wild_tame` (x8)** multiplies the density a hunter meets in any area the generator labelled `wild`: the blocks of unheld land,
about 8 km across, beyond the 2.5 km ring round each village. It is a label, not a history. `home_shy` (x0.3 on a village's own
area) is the same kind of factor, applied when the hunt reads density and nowhere else in the state. The ecology has one more
label of this kind: `busy` lowers a shy kind's suitability by area kind (home 1.0, ring 0.4, wild 0). People's background take in
the history is the same share everywhere, weighted by farmland, and not by how far an area is from a village.

**Recovery from hunting** (`recover.py`; seed 7, autumn; the ring's roe and red deer halved, then the pure ecology run for two
years):
- the halved ring had closed 38% of its gap at 12 days, 77% at 32 days (one year) and 97% at two years;
- the control's own yearly swing, a birth pulse and then deaths, is 169 to 259 roe;
- immigration fills the gap: deer move a share a day toward better land (`move` 0.15 a season, daily).

A hunted-out wood is therefore mostly full again within a year, and inside a single year the effect of hunting is smaller than
the natural swing.

**Rats** (`rat_check.py`, `rat_check2.py`):
- In the first 8 nights of a run, rats fall about 60% on brief 2's branch (5,813 to 2,286) and on brief 4's (5,432 to 2,217).
  The ecology alone, with no engine at all, does the same.
- The cause is the ecology's demography. All births come on the first day of each breeding season and deaths run through the
  season, so rats swing about threefold within a season, and foxes about 2.4 times over a year.
- That is realistic for once-a-year breeders (deer, foxes, wolves). It is wrong for rats, mice, voles and hares, which breed
  through their seasons.
- The 21% in 02zx compares two points of this sawtooth, not an effect of brief 4: carrion fell 4.5 times, while rats differ by
  about 3%.

**The cow left by the herd** (19 kills against 19 over a week): the raid loop does what brief 4 asked. A group fed at the carcass
remembers the herd it saw and comes back for it, but in that world the pack already raids the herd every night, so there is
nothing to add. The model also has no way for a carcass to draw more animals:
- each village has one group per kind, and its size does not follow the food;
- the ecology's movement draws animals by suitability and condition, not by carrion lying there.

So a carcass can redirect the village's own pack, but cannot bring a second one in.
