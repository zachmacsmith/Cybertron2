---
id: docs/review/37_growth/02zzzh_hunt_fish/building_clock.md
kind: note
updated: "2026-11-22"
---
# The building clock: what pricing lasting things on the year clock would touch

*note · `docs/review/37_growth/02zzzh_hunt_fish/building_clock.md`*


22 Nov 2026, 37.2 (subagent). An analysis note. No code was changed and nothing was committed.

Zach (22 Nov): "Look at everywhere this new building clock would touch and if you think that would make sense / what issues /
recalibrations it might raise?"

**The proposed rule (OPEN [[Q-84 The building scale|Q-84]]; not decided).** Things consumed day by day (food, fuel, keeping food) are made at real rates per hour
(the day clock). Things consumed over years (buildings, works, gear, tools, and the materials for them) cost their real share of a
year: real hours compressed by about 1/11 (the year clock). Today, works are built at about 1/30 to 1/70 of real hours while crafts
are priced at real hours (storage.md §4).

**Read with:** [[D2-273 Three clocks, each system on one|D2-273]] and `docs/cybertron2/spec/core/clocks.md` (the three clocks), [[D2-264 The fishing, hunting and materials network|D2-264]] (gear life in uses; weights in kg), [[D2-259 The food values are anchored on real values|D2-259]]
(real values within 20%, levers named), [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] and [[D2-262 The runs at a real river's size|D2-262]] (the weir's upkeep and size), [[D4-114 What is physically there can be used|D4-114]] (fences wear by the year), [[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]
(practice at a 64-day lifespan); `engine/data.py` (ITEMS, FITTINGS, ROOMS, BLUEPRINTS, MONUMENTS, WATER_WORKS, FENCES, CLEARING,
TECHNIQUES), `engine/buildings.py` (`room_cost`), `engine/farm.py` (`fence_need`), `engine/verbs.py` (`cost`, `_build`, `_make`),
`engine/clocks.py` (RATES), `wild/methods.py` (SETS); `proposals/hunt_fish_materials.md` §4 to §6; the sibling notes
[storage.md](storage.md), [withies_wood_materials.md](withies_wood_materials.md), [fibre_and_cord.md](fibre_and_cord.md),
[crafts_evaluation.md](crafts_evaluation.md).

**The basis used throughout.**
- A unit of work is 2 hours.
- The engine's year is 32 days at 7, 6, 5 and 6 units a day by season (PHYSICS `units`): **192 units, 384 hours**.
- A real working year is about 2,500 to 3,000 hours (fibre_and_cord.md).
- A real day of work is taken as 9 hours (8 to 10). Where a source gives days, I convert at 9 hours.
- So there are two factors, and they are not the same:
  - **the calendar factor**, 32 nights against 365: **1/11.4**. [[D2-273 Three clocks, each system on one|D2-273]] compresses durations by this factor.
  - **the labour factor**, 384 hours against about 2,700: **about 1/7** (1/6.5 to 1/7.8). This factor is "a real share of a year"
    of work.
- The tables give the cost under the rule at 1/11, as [[Q-84 The building scale|Q-84]] states it, and at 1/7. Section 5 argues for 1/7.

**Marks.** Figures with a sibling note's name come from that note. **(est.)** marks my own estimate, which needs a source before it
goes into data. "Now ÷ real" is the engine's hours over the real hours: 1/20 means twenty times cheaper than real, and 1.5 means
half as dear again as real.

---

## 1. The inventory

### 1.1 Works: buildings, rooms, fittings, monuments, the weir, fences, works on land

Every row here lasts seasons or years, so the rule puts every one on the year clock.

| Work | Now (materials, units) | Real hours | Its life ends by | Now ÷ real | Rule at 1/11 (units) | At 1/7 (units) |
|---|---|---|---|---|---|---|
| small room, wattle | 8 timber, 6 | 270 to 540 (30 to 60 days, storage §4, est.) | weather (wear by night) | 1/23 to 1/45 | **12 to 24** (x2 to 4) | 19 to 38 (x3 to 6) |
| small room, timber | 8 timber, 2 stone, 6 | 450 to 720 (50 to 80 days, est.) | weather | 1/38 to 1/60 | **20 to 32** (x3.3 to 5.3) | 32 to 51 (x5 to 8.5) |
| small room, stone | 30 stone, 4 timber, 40, mason | 630 to 1,260 (70 to 140 days, est.) | weather | 1/8 to 1/16 | 28 to 55 (x0.7 to 1.4) | 45 to 90 (x1.1 to 2.2) |
| medium room, timber | 15 timber, 4 stone, 15, carpenter | 720 to 1,350 (80 to 150 days, est.) | weather | 1/24 to 1/45 | **32 to 59** (x2 to 4) | 51 to 96 (x3.4 to 6.4) |
| medium room, stone | 60 stone, 8 timber, 90, mason | 1,080 to 2,250 (est.) | weather | 1/6 to 1/12 | 47 to 99 (x0.5 to 1.1) | 77 to 160 (x0.9 to 1.8) |
| hall, timber | 80 timber, 20 stone, 200, carpenter | 3,600 to 8,100 (400 to 900 days, est.) | weather | 1/9 to 1/20 | 158 to 355 (x0.8 to 1.8) | 256 to 576 (x1.3 to 2.9) |
| hall, stone | 150 stone, 20 timber, 250, mason | 5,400 to 10,800 (est.) | weather | 1/11 to 1/22 | 237 to 474 (x1 to 1.9) | 384 to 768 (x1.5 to 3) |
| room added, upper storey, tier | x0.75; x1.5 or x2; work x2, x4, x8 (SPACE, TIERS) | | | | multipliers kept | |
| camp | 3 timber, 1; lasts 10 days | 3 to 5 (a lean-to, est.) | 10 days | about 1/2 | 1 (the floor) | 1 |
| cellar (stone-lined, flat) | 4 stone, 6, mason | 360 to 630 (40 to 70 days, storage §3.11) | weather, damp | 1/30 to 1/53 | **16 to 28** (x2.6 to 4.6) | 26 to 45 (x4.3 to 7.5) |
| cellar, timber-lined (storage proposal) | (none) | 180 to 315 (20 to 35 days, storage) | rot | | 8 to 14 | 13 to 22 |
| vault | 40 stone, 30, mason | 900 to 1,800 (est.) | weather (fireproof) | 1/15 to 1/30 | 40 to 79 (x1.3 to 2.6) | 64 to 128 (x2 to 4.3) |
| hearth | 4 stone, 3, mason | 9 to 18 (est.) | use and time | 1/1.5 to 1/3 | 1 (floor; x0.33) | 1 |
| oven | 20 stone, 2 timber, 12, mason; lining 10 firings | 36 to 72 (est.) | shell: time; lining: firings | 1/1.5 to 1/3 | **2 to 3** (x0.15 to 0.25) | 3 to 5 |
| bins | 3 timber, 1 | 9 to 18 (an ark's 2 to 3 days less, storage §3.4, est.) | rot, vermin | 1/4.5 to 1/9 | 1 (floor) | 1 |
| granary floor | 6 timber, 4 | 27 to 45 (est.) | rot | 1/3.4 to 1/5.6 | 1 to 2 (x0.3 to 0.5) | 2 to 3 |
| hand mill (quern) | 2 stone, 2 | 18 to 45 (est.) | grinding (decades) | 1/4.5 to 1/11 | 1 to 2 | 1 to 3 |
| millstones | 10 stone, 10, mason; dressed every 2,000 grain | 180 to 360 (20 to 40 days, est.) | grinding (years) | 1/9 to 1/18 | 8 to 16 (x0.8 to 1.6) | 13 to 26 |
| water wheel and leat | 60 timber, 20 stone, 2 copper, 250, carpenter; silts in a year | 1,440 to 4,680 (160 to 520 days, est.) | silting (a year), rot | 1/3 to 1/9 | 63 to 205 (x0.25 to 0.8) | 102 to 333 (x0.4 to 1.3) |
| anvil and bellows | 6 stone, 2 hide, 1 timber, 4, smith | 27 to 45 (est.) | use | 1/3.4 to 1/5.6 | 1 to 2 | 2 to 3 |
| stalls, beds (each) | 1 timber (and 2 straw), 1 | 4 to 9 (est.) | time | 1/2 to 1/4.5 | 1 (floor) | 1 |
| woodshed | 2 timber, 1 | 18 to 36 (est.) | rot | 1/9 to 1/18 | 1 to 2 | 1 to 3 |
| owl hole, fire ring | 1 timber or 1 stone, 1 | 1 to 4 (est.) | | about 1 | 1 (floor) | 1 |
| smoke racks | 2 timber, 2 (proposed: 2 withies, 1 timber) | 6 to 10 (two hurdles and a frame, withies §3.4) | rot, fire | 1/1.5 to 1/2.5 | 1 (floor; x0.5) | 1 |
| brine pan | 1 copper, 2 timber, 4, salter; 60 boilings | 18 to 36 (est.) | boilings | 1/2 to 1/4.5 | 1 to 2 | 1 to 3 |
| carved post, standing stone, cairn | 2 timber, 2; 4 stone, 4; 6 stone, 3 | 18 to 45; 18 to 45; about 9 (est.) | weather (slowly) | 1/1.5 to 1/11 | 1 to 2 each | 1 to 3 |
| **weir, first section, wattle** | 12 timber, 24, crew 2 (proposed: 5 timber, 14 withies) | 36 to 51 at the research note's size (a 10 m section about 21 h, withies §3.4, plus the base, est. 15 to 30); 150 to 500 if a weir that takes 30% of a large run is 50 to 150 m of wattle and stakes driven in a current (est.) | floods, ice (the year's flow) | **1.0 to 1.3** at the note's size; 1/3 to 1/10 at a large river's | **2 to 3** (x0.1); 7 to 22 at the large size | 3 to 4; 11 to 36 |
| **weir, added section, wattle** | 6 timber, 16 (proposed: 12 withies, 1 timber) | about 21 (withies §3.4) | floods | **1.5** | **1** (x0.06) | 1.5 |
| weir, timber section | 10 timber, 25 | 30 to 50 (est.) | floods | 1.0 to 1.7 | 1 to 2 | 2 to 4 |
| weir, stone footing | 10 stone, 15 | 45 to 135 (est.) | floods (slowly) | 1/1.5 to 1/4.5 | 2 to 6 | 3 to 10 |
| **wood fence, a field** (2 ha) | 4 timber, 10 x √size | about 1,080 (315 hurdles at 3 a day and stakes, about 120 days, storage §4) | a level a year ([[D4-114 What is physically there can be used|D4-114]]) | **1/54** | **47** (x4.7) | 77 (x7.7) |
| wood fence, a close (0.2 ha) | the same: **10 units**, as `fence_need` floors the size at 1 | about 315 (35 days, storage §4) | a level a year | 1/16 | 14 (x1.4) | 22 (x2.2) |
| a dead hedge round 2 ha (stakes and brushwood) | (none) | 127 to 255 (20 to 40 m a day, est.) | 2 to 3 years (est.) | | 6 to 11 | 9 to 18 |
| dry-stone wall, a field | 8 stone, 20 x √size, mason | 850 to 1,700 (3 to 6 m a day, storage §4); 1 to 2 t of stone a metre | keeps | 1/21 to 1/42 | **37 to 75** (x2 to 3.7) | 60 to 121 (x3 to 6) |
| clearing turf to field (CLEARING, a unit of size) | 6 | 54 to 90 (breaking 2 ha of sod with oxen, est.) | the field persists | 1/4.5 to 1/7.5 | 2 to 4 (x0.4 to 0.7) | 4 to 6 |
| clearing scrub to field | 10 | 360 to 900 (grubbing 2 ha by hand, est.) | regrowth if left | 1/18 to 1/45 | **16 to 40** (x1.6 to 4) | 26 to 64 |
| ditching wet ground (works) | 40 a unit of size, upkeep 1.5 | 180 to 360 (about 400 m of ditch, est.) | silting | 1/2.2 to 1/4.5 | 8 to 16 (x0.2 to 0.4) | 13 to 26 |
| terracing a hillside | 60 and 6 stone a unit of size | 1,800 to 3,600 (est.) | slumping | 1/15 to 1/30 | **79 to 158** (x1.3 to 2.6) | 128 to 256 |
| withy bed (proposal §4.1) | 1 withies, 10 | about 20 (840 cuttings, two days' digging, withies §3.3) | 30 years | about 1 | **1** (x0.1) | 1.5 |
| retting pit (proposal §4.2) | 10 | 18 to 45 (est.) | silting | 1/1 to 1/2 | 1 to 2 | 1 to 3 |
| granary on staddles, clamp, sealed pit, rick (storage §3.7 to §3.16) | about 11 units with 10 timber and 5 stone; 1; 2; 3 | priced in storage.md at the building scale (1/30 to 1/70) | rot, weather | 1/30 to 1/70 | x3 to 6 the proposed figure | x5 to 10 |

**What the column "now ÷ real" shows.** The engine is not on one building scale.
- **Light works are compressed 20 to 60 times:** the wattle and timber rooms, the cellar, the field's fence, scrub clearing, the wall
  and the terrace.
- **Stone works and the great works are compressed 6 to 20 times:** stone rooms, halls, millstones and the water wheel.
- **Small fittings are compressed 1.5 to 5 times:** the hearth, the oven, the granary floor, smoke racks, the brine pan and the
  anvil.
- **The weir's sections are at real hours or dearer:** 1.0 to 1.5.

So the rule does not lift everything by 3 to 6 times. It raises the light works, leaves the stone works and halls about where they
are, and cuts the small fittings and the weir.

### 1.2 Gear and tools (engine rows and the proposed ones)

| Gear | Now (materials, units; life) | Real hours to make | Real life | Now ÷ real (making) | Rule at 1/11 | At 1/7 | Life under the rule (real uses x 1/7) |
|---|---|---|---|---|---|---|---|
| crude tool | 1 timber, 0.5 stone, 1; **10 uses** | 4 to 10 (est.) | 300 to 1,000 h of use (est.) | 1/2 to 1/5 | under 1 (floor or batch) | under 1 | **20 to 70 acts** (x2 to 7 now) |
| copper tool | 1 copper, 0.5 timber, 3 at an anvil; 40 | 4 to 8 beyond the metal (est.) | 1,000 to 3,000 h (est.) | about 1 | under 1 (x0.1) | under 1 | 70 to 200 |
| crude weapon | 1 timber, 1; 10 (about 3 fights) | 2 to 4 (est.) | 50 to 150 uses (est.) | about 1 | under 1 | under 1 | 7 to 20 |
| wooden plough | 4 timber, 1 copper, 4, carpenter; **60 plots** | 27 to 45 (est.) | 600 to 1,500 h of ploughing (est.) | 1/3.4 to 1/5.6 | 1 to 2 | 2 to 3 | **11 to 27 plots** (now 2 to 5 times too long) |
| harness | 2 timber, 1 hide, 2, leatherworker; 80 days | 9 to 18 (est.) | 500 to 1,000 working days (est.) | 1/2 to 1/4.5 | 1 | 1 | 70 to 140 (on target) |
| handcart | 6 timber, 3, carpenter; **no life** | 27 to 72 (est.) | 5 to 10 years (est.) | 1/4.5 to 1/12 | 1 to 3 | 2 to 5 | 5 to 10 world years (never in a run) |
| pack | 1 hide, 1 timber, 1; no life | 3 to 6 (est.) | years | 1/1.5 to 1/3 | 1 (floor) | 1 | |
| bedroll, tent | 1 hide, 1; 3 hide, 2 timber, 2; 40 and 30 nights | 2 to 4; 6 to 12 (est.) | 200 to 500 nights (est.) | about 1; 1/1.5 to 1/3 | 1 (floor) | 1 | 30 to 70 (on target) |
| fishing rod | 0.5 timber, 0.1 hide, 1; 30 uses (proposed 0.1 withies) | 1 to 2 | 150 to 300 uses (est.) | 1 to 2 | 1 (floor) | 1 | 20 to 45 (on target) |
| clappers, horn | 0.5 timber, 1; 1 antler, 2 | 1 to 2; 4 to 8 (est.) | years | about 1; 1/1 to 1/2 | 1 (floor) | 1 | |
| **wicker trap** (proposal §5) | 0.4 to 0.5 withies, 2.5 to 3; 30 sets | 4 to 8 (withies §2) | about 2 years with repair: 200 to 300 sets (est.) | **about 1** | under 1: **a line of 6 for 2** | 6 for 2 to 4 | 30 to 45 (on target) |
| snares, a line of 5 (proposal) | 0.02 cord, 1; 10 sets | about 1, plus the cord (fibre §3) | a few settings | 2 | day clock: kept | kept | kept (real) |
| hand line (proposal) | 0.01 cord, **0.5** | 1 to 2 (fibre §3) | 30 to 100 uses (est.) | about 1 | 1 (floor) | 1 | |
| **fish net**, gill 20 m by 1.5 m (proposal) | 1 cord, about 30; 60 to 80 uses | 40 to 60 beyond the cord (fibre §3) | 1 to 3 years: 50 to 450 sets (est.) | **1.0 to 1.5** | **2 to 3 and the cord** | 3 to 4 and the cord | 7 to 65 (now at or above) |
| fowling net (proposal) | 0.8 cord, 30 | 50 to 70 beyond the cord (fibre §3) | as the fish net | about 1 | 2 to 3 and the cord | 4 to 5 | |
| seine (later) | 10 cord, about 200 | about 500 (fibre §3) | as the net | about 1 | 22 and the cord | 36 | |
| creel, pack basket (proposal) | 0.3 withies, 1; 1 withies, 0.1 hide, 2 | 4 to 8; 6 to 10 (est.) | a few years | 1/1.5 to 1/4 | 1 (floor) | 1 | |
| hurdle (proposal) | 1 withies, 1.5 | 2.7 to 3.2 (withies §2) | 5 to 10 years dry | about 1 | **7 hurdles for 1** | 5 for 1 | |
| chest, barrel, sack, basket (storage §3) | 1 timber, 10; 0.7 timber, 0.3 withies, 5; 0.6 cord, 2; 0.3 withies, 1 | 18 to 27; 8 to 11; 3 to 5 beyond the cord; 4 to 8 (storage) | 30, 10, 3, 2 world years | about 1 | 1 each (x0.1 for the chest and barrel) | 1 to 2 | the years as given |

**The materials** (cord, withies, flax, timber, stone, hide, bone) are goods, and their getting is on the day clock whatever they go
into (section 2):
- **wild cord:** 25 units a kg, against a real 35 to 80 hours (fibre §2);
- **flax cord:** 7 to 8 units a kg, against a real 15 to 20 hours;
- **withies:** cut at 1.5 to 4 bundles a unit (withies §3.3);
- **timber:** felled at 3 a 2-unit act, about 180 kg an hour, against a real 55 to 110 kg an hour (est.).

### 1.3 Goods consumed day by day (the day clock; the rule leaves them, and the check is in passing)

| Work | Now | Real | Now ÷ real | Note |
|---|---|---|---|---|
| grind (quern) | 3 grain a unit | 1 to 1.5 kg an hour (est.) | about 1 | right |
| ox mill, water mill | 64 and 200 grain in 2 units ([[D4-97 Decisions on 38.51's list|D4-97]]) | 10 to 20 and 50 to 150 kg an hour (est.) | about 1 | right; batches decided ([[D4-97 Decisions on 38.51's list|D4-97]], [[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]) |
| bread at a hearth, oven bread | 10 in 1 unit; 100 in 3 | 10 kg in 3 to 4 hours; 100 kg in 8 to 10 (est.) | 1/1.5 to 1/2 | a little cheap |
| salt fish, salt meat | 4 a unit | about 20 kg an hour with gutting ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]'s proposal) | **about 10** | dear; [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] settles it |
| dry, smoke | 8 and 40 a unit | hanging 333 kg about 11 units (smokehouse §) | about 1 | right |
| charcoal | 5 timber to 1 charcoal in 2 units | 12 to 18 hours of stacking and tending for 240 kg (est.) | 1/3 to 1/4.5 | cheap |
| fell, cut firewood, gather dead wood | 3 timber in 2 units; 5 firewood a unit; 3 a unit | 0.5 to 1 t a day of logs or cordwood (est.) | 1/1.5 to 1/3 | cheap |
| tallow lights, cheese, leach acorns, boil salt, hay, dung | as data | not checked | | |

These belong to their own threads ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] for salting; the fuel calibration, OPEN [[L-110 Salt's fuel, to recalibrate|L-110]]). They matter here only because a material's
getting stays on this clock under any version of the rule.

---

## 2. The test for which clock a cost is on

Two pieces of arithmetic decide it.

**First: work in the engine runs at about 1/7 of a real year.** A world year holds about 1/7 of a real year's working hours, so
anything done by work happens about 1/7 as often per world year as per real year: uses of a tool, sets of a net, felling, building.
Eating runs per night, so a world year eats 1/11 of a real year's food. Food work is therefore about 7/11 of its real share of the
year, which is why food binds at about 30% of the work (scenario_design.md).

**Second: what has to stay real is the share of the year.** Two kinds of thing keep that share:

- **A thing that wears by time** (weather, rot, floods; a house, a fence, a weir) lives its real number of years as world years,
  because those durations are on the year clock. It keeps its real share of a year only if it is made at **real hours x 1/7**.
  - At 1/11 it gets about 0.64 of its real share.
  - At real hours it gets about 7 times its real share.
- **A thing that wears by use** (a net's sets, a tool's acts, a plough's plots) keeps its real cost per use, whichever factor its
  making takes, **as long as its life in uses takes the same factor as its making.** Its share of the year then follows the share
  of its activity, as food work does.
  - If the making is compressed and the life is not, gear becomes nearly free per use.
  - If the life is compressed and the making is not, as with the proposal's wicker trap (real making, a two-world-year life),
    gear is 7 to 10 times dear per use.

So the line [[Q-84 The building scale|Q-84]] draws (day by day against over years) is the right line. It needs three amendments.

> **The test.** Ask what ends the thing's life.
> 1. **Used up in one go, or within a handful of uses** (food, fuel, salt, bait, lights, seed, a snare's noose, a camp's few
>    nights: its real life in uses x 1/7 comes to less than about two): **day clock.** Real hours a piece, life in real uses.
> 2. **Anything else lasts: it is capital,** whether time or use wears it: **year clock.** Its making is **real hours x the
>    year's labour share** (about 1/7). Its life is its real life in years counted as world years, or its real uses x the same
>    share.
> 3. **Materials are goods.** A kg of cord, a bundle of withies, a timber: their quantities are real ([[D2-264 The fishing, hunting and materials network|D2-264]]), and their getting is
>    always on the day clock, whatever they are made into.
> 4. **Upkeep goes with the thing.** Mending capital is priced at the capital factor, and how often it is needed follows the clock
>    of the wear (a level a year for a fence, a level a flood for a weir, a tear every so many sets for a net).
> 5. **Learning and travel do not move.** A lesson costs its real hours (day clock) and gives what the life clock gives ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]).
>    Walking and carrying are on the day clock.

The test needs no judgement about whether a thing is "daily". Rule 1's threshold comes from the arithmetic, and every row in §1
falls on one side of it.

---

## 3. Where the line is hard, case by case

| Case | Where it falls | Why |
|---|---|---|
| **Firewood** (daily fuel, cut in bulk) | day | It is burned in one use. Cutting a winter's stack ahead is timing, not capital. The woodshed that keeps it dry is capital. |
| **Cord for snares** (used up fast) and **cord for a net** | day, both | Cord is a material: one good with one rate. A rate for cord that depended on its use would need two goods. What differs is the snare (rule 1) and the net (rule 2). |
| **Salt** | day | consumed in salting. The brine pan and the salt pan's works are capital. |
| **Charcoal** | day | fuel consumed in smelting. The clamp is built and burned each time, so it is part of the charcoal's work. |
| **Bread and the oven** | bread day; oven capital | The oven's shell is time-worn. Its lining wears by firings (10 now), and the relining (2 units and 2 stone) is capital upkeep at the factor. A real lining lasts hundreds of firings, so under the rule it should last about 15 to 40. |
| **Seed** | day | It is food sown. Seed selection, a lasting improvement, is 1 unit and can stay as it is. |
| **Repairs and upkeep** | with the thing (rule 4) | House repair (2 units a level, about 1 to 3 levels a world year) is already about the rule's 1 to 2 units a year (a real 3 to 5 days, est.). The fence's mend (0.25 of the build a year, [[D4-114 What is physically there can be used|D4-114]]) scales up with the build, x5 under the rule. The weir's mend (0.06 of a section a level) scales down with the section. Net mending (a real 10 to 20% of the netting time, fibre §2) takes the factor with the net. |
| **Gear lives in uses** ([[D2-264 The fishing, hunting and materials network|D2-264]]) | year, with the life x 1/7 | Engine lives today, against real uses x 1/7: crude tool 10 against 20 to 70; copper 40 against 70 to 200; plough 60 plots against 11 to 27; harness 80 days, bedroll 40, rod 30, the proposal's trap 30 and net 60 to 80 are all about on target. So lives need changing for the tools and the plough. The rest only need their making compressed. |
| **Teaching** | day for the cost, life for the effect | A lesson is real hours. What it gives is on the life clock ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]). Nothing changes. |
| **Carrying building materials** | day | See issue 4: with weights in kg ([[D2-264 The fishing, hunting and materials network|D2-264]]), carrying could become the largest cost of building. |
| **Crew works** | the drive: day; the weir build: year | A drive is a day's use of the crew's labour. A weir is a standing work worn by floods. The crew is about people being there at once, not about hours, so it is unaffected. |
| **Process times** (retting, smoking, a withy bed's years) | year, as durations ([[D2-273 Three clocks, each system on one|D2-273]]) | Already decided. A building's duration in days is labour, not a process time. Keep the two apart. |
| **A camp** | either | It lasts 10 days. Its making at the floor of 1 unit is right on either clock. |

---

## 4. The biggest moves, and what they do to play

### 4.1 The ten biggest moves (rule at 1/11; at 1/7 in brackets)

| # | What | Now | Under the rule | Move |
|---|---|---|---|---|
| 1 | a wood fence round a field (2 ha), and its yearly mend | 10 units; mend 2.5 a year | **47** (77); mend 12 (19) | **x4.7 up** (x7.7) |
| 2 | a timber small room | 6 | 20 to 32 (32 to 51) | x3.3 to 5.3 up |
| 3 | a stone cellar | 6 | 16 to 28 (26 to 45) | x2.6 to 4.6 up |
| 4 | a medium timber room; a wattle small room | 15; 6 | 32 to 59; 12 to 24 | x2 to 4 up |
| 5 | a dry-stone wall round a field; scrub cleared to field | 20; 10 | 37 to 75; 16 to 40 | x2 to 4 up |
| 6 | the storage proposal's granary on staddles, clamp, pit, rick (priced at the old scale) | as storage.md | x3 to 6 | up |
| 7 | **the weir's sections** | first 24; added 16; timber 25 | first 2 to 3 at the research size (7 to 22 if a large river's weir is the large work it should be); added 1; timber 2 | **x0.06 to 0.1 down** (x0.3 to 0.9 at the large size) |
| 8 | **nets: the making** | about 30 and 1 kg cord | 2 to 3 and 1 kg cord (8 units flax, 25 wild) | **x0.08 to 0.1 on the making; x0.3 to 0.6 in all** |
| 9 | the oven; the smoke racks; the hearth | 12; 2; 3 | 2 to 3; 1; 1 | x0.15 to 0.5 down |
| 10 | traps, hurdles, creels, baskets, chests, barrels, tools, weapons | 1 to 10 each | the 1-unit floor, or batches | x0.1 to 0.5 down |

Roughly unchanged: stone rooms, halls, millstones, the water wheel, the vault (x0.5 to 2), bins, beds and stalls (at the floor
either way).

### 4.2 What it does

**Houses.**
- At 1/11, a two-room wattle cottage (a small room and an added one) is 21 to 42 units against 10.5 now: 4 to 7 days of one adult's
  work, or half a season for a couple. A timber house with a medium room is 47 to 83 units, a couple's season. A hall is 158 to
  355, a crew of four for one to two seasons on half their units.
- All of these still fit a season or two. At 1/7, multiply by 1.6.
- The cellar stops being the cheapest fitting a mason builds, and storage.md's cost by footprint matters more.

**Fences become a major investment.**
- One field's fence is a whole season of one adult (47 units; 77 at 1/7), and its mend is 12 units a year.
- A herder household with three fenced fields spends most of an adult's world year building them. Real enclosure was dear, so
  herding (the `herd` technique) against fencing becomes a real choice.
- What the engine calls "a wattle fence" is costed as hurdles. A dead hedge of stakes and brushwood costs about what the engine
  charges now (6 to 11 units under the rule). That gives the cheap-and-worse option storage.md asks for: a dead hedge, gappy,
  lasting 2 to 3 years, against hurdles or a wall.
- `fence_need` floors the size at 1, so a close is charged as a whole field. A close's fence is only x1.4 under the rule.

**Weirs get cheaper, not dearer.**
- Priced from the research note's 10 m section, the weir is already at or above real hours. Under the rule a section is 1 to 3
  units, and [[D2-262 The runs at a real river's size|D2-262]]'s large takes would cost almost nothing to build.
- The weir only stays dear if its real size is set by what it takes. A weir that takes 30% of a large river's run is tens of
  metres of wattle and hundreds of stakes driven in a current.
- The weir's size has to be settled before the rule touches it (issue 8).

**Gear: capital binds through materials, trades and sites, not hours.**
- Nets fall to their cord (8 to 25 units a kg), so the flax switch decides even more than the proposal intends. A wild-cord net is
  three times a flax net.
- Traps, hurdles, creels and tools become nearly free: that is what they cost in real life, about 1% of a year.
- A seine is still a lump: about 22 units of netting and 10 kg of cord.
- Scenario_design.md wants leverage from access, and this delivers it: who holds the flax close, the withy bed, the copper and the
  smith, the rock, the weir's water. The labour of making stops being a barrier.
- The risk is that gear lasts too long or is made too freely for the materials network to have buyers. The cord demand of a fishing
  household (1 to 3 kg a world year, proposal §4.2) holds under the rule because nets still wear in 60 to 80 uses. It would not
  hold if net lives were set to real uses without the factor.

**A household's year of making** (two adults, 384 units; a fishing and farming household with one net, six traps, two snare lines,
tools, a two-room wattle house and one fenced field; est.):

| | Now (with the proposal's gear) | Rule at 1/11, lives as now | Rule at 1/7, lives x 1/7 |
|---|---|---|---|
| net (one every 2 world years, flax cord) | 19 | 5.4 | 6.2 |
| traps (3 worn out a year) | 9 | 1 | 1.3 |
| snares | 2 | 2 | 2 |
| tools | 3 | 3 (the floor) | 1.4 |
| house upkeep | 4 | 4 | 4 |
| fence upkeep | 2.5 | 12 | 19 |
| **in all** | **about 40 (10%)** | **about 27 (7%)** | **about 34 (9%)** |
| one-off: build the house and fence | 20 | 68 to 89 | 110 to 145 |

The share of the year spent making stays at about 7 to 10%, at the low end of the real 10 to 20% that [[Q-84 The building scale|Q-84]]'s brief gives (not
checked here). It moves from gear to works and land: today gear costs about three times its real share and works about a fifth of
theirs, and the rule brings both to their real shares. Building lumps grow three to five times.

**The play evidence cuts the other way.**
- Investment crafts are already crowded out. In the river run the weir, at 24 units, was asked for on days 6, 8 and 9 and never
  begun, and a smoke-racks build failed for want of one unit (crafts_evaluation.md §7). Across about 5,500 agent-days nobody built
  a weir or a smokehouse.
- Raising fences, rooms and cellars three to five times without fixing what crowds them out would make building rarer still: the
  gates, recipes shown, spare units, and the goal ([[W-75 Gates checked and recipes shown|W-75]]).
- The rule's cheaper weir, racks and gear help in the same places.

**The nutrition worlds ([[W-69 Nutrition worlds|W-69]]).**
- The arms seed their capital: no weir, racks and salt; racks; or a weir of three timber sections and racks
  (`specs/make_nutrition_runs.py`). The build costs never enter.
- What enters is upkeep. The high arm's weir mend falls about tenfold at the research size, so the high arm's food per unit of
  work rises slightly. The upkeep test pins shares of cost, not units, so it holds.
- Once gear is a good ([[W-73 Fishing, hunting and their materials developed together|W-73]]), the low and medium arms pay for traps. Under the rule that cost is negligible. Under the proposal's
  prices it is about 5 to 10% of fishing work.
- Each arm's reading against its null arm is unchanged in kind.

**The calibration suite** (`specs/calibration/expectations.yaml`: weather, land, water, ecosystems, wildlife) is untouched.

**Committed worlds.**
- Seeded buildings, fences and weirs pay nothing, so the worlds' seeded capital and larders are unchanged.
- The rule reaches them through two routes:
  - building during a run. In wild_region_s7, granaries were built at Carter, Holt and Wood between days 10 and 29; fences go up in
    the farm worlds; rooms are built for new households.
  - upkeep: fence mends x5, weir mends x0.1.
- The farm worlds and wild_region would show it first. The fishing and nutrition worlds hardly would.

**Tests that pin costs.**
- These break on literal numbers:
  - `test_cybertron2_water_fixes.py`: a timber section costs 10 timber and 25 units, the upgrade 4 and 9, a footing 10 timber, 10
    stone and 40 units.
  - `test_cybertron2_water5_river.py`: a timber first section of 33 units; the timber spent, 16, 6 and 4.
  - `test_cybertron2_buildings.py`: a fine small room is "about 10 units", that is 6 x 2 less the 2 done.
- These read the tables and survive: the fence's kept share (`test_cybertron2_use_by_physics.py`), the weir's upkeep shares
  (`test_cybertron2_water5_river.py` around line 590), the added-room 0.75, and the mill's and salt's units, which are day clock and
  unchanged.
- `test_cybertron2_clocks.py` checks that every rate names its clock (`engine/clocks.py` RATES). Units of making are not in its
  list today.

---

## 5. Issues

1. **The factor: 1/7, not 1/11.**
   - 1/11 is the calendar's 32 nights against 365. It is the right factor for durations ([[D2-273 Three clocks, each system on one|D2-273]]).
   - "Its real share of a year" is a share of work: 384 engine hours against about 2,700 real, 1/6.5 to 1/7.8. The gap comes from
     two things: the engine's day has 12 working hours (6 units), and it has no rest days.
   - At 1/11, everything time-worn costs about two-thirds of its real share.
   - Define the factor from the world itself: units a year x 2 hours ÷ about 2,700 real hours. It then moves with a world's year
     and day, as [[D2-214 Two clocks|D2-214]] ties the seasonal stocks to the year's days. Name it as one lever under [[D2-259 The food values are anchored on real values|D2-259]].
2. **No class needs its own factor.**
   - The unevenness in §1.1 (rooms x2 to 5, stone x1, the weir x0.1) is the engine's present prices being uneven, not the classes
     needing different compression.
   - Per-row departures are named beside the data as [[D2-259 The food values are anchored on real values|D2-259]] asks: the wall's stone, the weir's size, any hall kept cheap for
     lords.
   - If runs show building crowded out, the fix is one named play lever on all capital (say 0.5 of the rule), not a factor for
     each class.
3. **Rounding.**
   - `verbs.cost` takes `int(TECHNIQUES[tech]["units"])`, so a recipe under one unit truncates to nothing. The proposal's hand line
     at 0.5 units would be free today.
   - A build act costs 2 units and puts in 2 x skill (`_build`, VERB `build` cost 2). So a work under 2 units still takes a whole
     act, unless several small fittings go in one act (beds and stalls already take `qty`).
   - Under the rule about 25 rows fall below one unit: hearth, bins, stalls, beds, owl hole, smoke racks, hurdle, trap, creel,
     basket, chest, barrel, tools, weapon, harness, pack, rod, and the weir's added section.
   - The remedy is a floor of one unit, with small things made in batches (a unit gives 7 hurdles or a line of 6 traps, as tallow
     lights give 4), and each floor written as a departure.
4. **Materials and carrying.**
   - The rule compresses the work of making, never a material (rule 3). A material-heavy thing is therefore dearer than its real
     share by its materials' share of the real hours:
     - small for buildings, where most real hours are conversion and assembly (hewing, framing, daubing, thatching);
     - large for nets, where cord becomes 70 to 90% of the cost;
     - the wall's 8 stone is about 1/100 to 1/300 of a real field wall's stone, already a departure to name. Hoeing yields stone,
       which is the right source for walls.
   - Carrying is the bigger catch. Under [[D2-264 The fishing, hunting and materials network|D2-264]] every weight goes into kg. A timber is about 240 kg (withies §0) and is weight 2
     today. At a real carry of 25 to 30 kg on foot, a small room's 8 timber (1.9 t) is about 65 loads.
   - On the day clock that could dwarf the room's compressed 12 to 24 units.
   - The timber unit's kg and the carrying ([[W-71 How carrying works in the live runs|W-71]]: handcart, pack ox) have to be settled together with this rule, or the house
     becomes a haulage problem.
5. **Gear lives must move with the making.**
   - Compressing the making while leaving lives as they are makes tools almost free per use (x11 cheaper). That is the "capital
     stops binding" failure.
   - With lives at real uses x 1/7:
     - the crude tool's 10 uses become 20 to 70 and the copper tool's 40 become 70 to 200;
     - the plough's 60 plots fall to 11 to 27;
     - the rest stay.
   - The handcart and the pack have no life today and need one.
6. **Batch processes are unaffected.**
   - The mill's 64 and 200, the oven's 100, the racks' 40 ([[D4-97 Decisions on 38.51's list|D4-97]], [[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]) are day-clock work per kg.
   - Their fittings move with the rule (the oven x0.2, the racks to the floor, the millstones about unchanged).
   - Their wear by use (dressing, relining, boilings) is capital upkeep at the factor, as often as the use says.
7. **Skill and practice.**
   - Building progress is 2 x skill (a trade 0.5 to 2.0, basic 1.0 to 1.5) x the yield multiplier, and practice counts units
     (tau 50, [[D2-52 Skill by practice on all work|D2-52]]).
   - With works x3 to 5, a carpenter gets three to five times the practice from one house and reaches master after one or two
     medium rooms. A novice's 0.5 makes a hall at 1/11 a world year or more of one person's work.
   - With gear x0.1, a net-maker needs ten times the nets to master the craft, which is still realistic.
   - Practice counts per unit (day clock) against a threshold set on the life clock ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]), so nothing breaks. The trade novice's
     0.5 on large works may want revisiting.
8. **The weir.**
   - Priced as it stands, the rule makes the weir about ten times cheaper. Its upkeep falls with it, since a quarter to a third of
     its cost a year ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]) is a share of that cost.
   - Before applying the rule, size the weir to its take. A first section that takes 30% of a large river's run should be the
     large work (150 to 500 real hours, est.: 7 to 22 units at 1/11), and an added section a share of that.
   - [[D2-262 The runs at a real river's size|D2-262]] ("the weirs take being big feels fine") makes the large work the consistent reading.
9. **The life clock's demand.**
   - A world's lifespan is 64 days, about two world years, against 40 to 50 real working years. Households form about 20 times as
     often per world year as per real year, and each needs a house at the year clock's price.
   - A village of 15 households forming about 10 a world year would spend about 120 to 250 units on cottages, 2 to 4% of its labour,
     against a real fraction of a per cent.
   - That is manageable, but growth worlds (37_growth) should read it.
10. **Labour by season.**
    - Units run 7, 6, 5 and 6 by season. Real building and making were done in the slack: after harvest, and in winter for withies,
      nets and spinning (proposal §8.5).
    - Under the rule, dearer works compete with harvest work. Nothing breaks; the season only shapes the choice.
    - A frost rule for digging (cellars, ditches, pits) belongs with environment work, not here.
11. **Where the rule lives in the code.**
    - `engine/clocks.py` already names each rate's clock ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]]), and `test_cybertron2_clocks.py` checks it. Units of making are not
      among its rates.
    - The clean seam, under [[D2-244 The engine's reworking into feature packages|D2-244]]:
      - a `capital` clock in RATES;
      - one conversion, `work_units(real_hours, clock, w)`;
      - data rows that carry real hours, with the clock beside them.
    - Then data holds real values ([[D2-259 The food values are anchored on real values|D2-259]]) and the compression is one lever in one place, not a hand-scaled number in every row.

---

## 6. Verdict

**The rule makes sense, and the engine needs it.**
- Today it prices gear at about three times its real share of a year and light works at a twentieth to a fiftieth. The rule
  corrects both, on the same footing the clocks already use.
- Under the rule a cellar, a room and a field's fence each cost their real share of a year.

The rule as written needs four changes:
1. The factor is the year's **labour** share, about 1/7, defined from the world, not the calendar's 1/11.
2. Gear lives in uses take the same factor as their making.
3. Materials stay real in quantity and rate; only the work of making compresses.
4. Things used up within a handful of uses stay at real hours.

It is not a uniform rise. Light works go up three to five times, stone works and halls hardly move, and the weir, ovens, racks and
gear come down.

**What to decide ([[Q-84 The building scale|Q-84]]):**
1. The test in §2: used up within a handful of uses, day clock; capital, year clock; materials, day clock; upkeep with the thing.
2. The factor: the labour share from the world's own numbers (about 1/7), named as one lever. Or 1/11, if Zach wants building
   cheaper on purpose, written as a departure.
3. Lives compressed with the making (real uses x the factor, or real years as world years).
4. A one-unit floor with batches for small things.
5. The fence as two works: a dead hedge, and hurdles or a wall.
6. The weir sized to its take before it is repriced.

**What to recalibrate first:**
1. **The gear in [[W-73 Fishing, hunting and their materials developed together|W-73]]'s build.** The proposal's §5 table is not yet in `data.py`, so it can be written on the rule from the start
   at no recalibration cost:
   - nets about 3 units and their cord;
   - a line of 6 traps for about 2 units;
   - 7 hurdles a unit;
   - lives as in §1.2.
2. **Timber and stone in kg, and carrying ([[D2-264 The fishing, hunting and materials network|D2-264]], [[W-71 How carrying works in the live runs|W-71]]),** before any work is repriced. These set the materials' day-clock share of
   every building.
3. **The works that runs actually build:** rooms (with storage.md §11's wattle room), the cellar by footprint (storage.md §3.11),
   the fence split, the granary floor and the smoke racks. Do this with the floor in `verbs.cost` and the conversion in
   `engine/clocks.py`.
4. **The weir**, sized to its take and then repriced, with [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]'s upkeep shares kept.
5. **Then the tools' and plough's lives, clearing and terracing.** Repin the tests above, and read building in a farm world against
   its null arm, as scenario_design.md asks.
