# U7: works and the building clock

**Status:** discussion (a component spec of the wave's integrated design, W-85). Nothing here is decided beyond the decisions it
cites; nothing is built. Estimates are marked (est.); figures from the overnight notes carry the note's name.
**Owner:** 37.2 (the rule and its numbers, the weir's size, fences' and clearing's numbers, the companions' design). **37.4 owns
buildings, rooms, fittings and their cost code** (`engine/buildings.py`, the `build` verb in `engine/verbs.py`, `night.py`'s breaks
and wear), the verbs and their registry, the knowledge and skill code, the senses, and the fence and herd mechanism (`herds.py`,
fences.md's author) and clearing's holding rules (clearing.md); each code change below names its owner, and 37.4 is named on any
merge that touches its files. **Thread:** W-85, under W-73; the timber economy (W-76) extends the builders designed here.


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-302:** the weir's cost set directly (basis §4).
> - **D2-303:** poles are timber until the timber thread.
> - **D2-306:** material got at the site (field stone, brush, daub, turf) counted in the work at the factor.
> - **D2-309:** one capital factor for every lasting thing; existing works held until their companions.
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-320:** crop protection as it is (dead hedge postponed); a rough watch act (units watching over a field, herd or building, by day or night), widening `guard`.
> - **D2-321:** builders' craftsmanship postponed: all wear the same.
> - **D2-322:** fences along one border, in targetable sections; attending shows where fences stand.
> - **D2-323:** a cleared plot becomes a field part of its parcel.
> - **D2-324:** a build act costs what is left (1 or 2 units).
> - **D2-328:** a wattle house's default roof is turf or brush got at the site; straw thatch the better roof.
> - **D2-330:** the worlds' defaults (questions C1 to C7).

## Extends

Each read in full, not only its summary.

| Earlier work | What it says that this spec builds on |
|---|---|
| **D2-276** (building_clock.md, accepted in principle) | What ends a thing's life decides its clock; capital costs real hours times about 1/7, worked out from each world's own numbers as one named lever; its life its real years as world years or its real uses times the same factor; materials real in quantity and rate; upkeep priced with the thing; brought in by stages with builders as a trade, cheaper ways to protect crops and clearing a plot at a time |
| **D2-281** | The factor's target about 1/7, reached in stages from today's (about 1/40) through about 1/15, read with bots between |
| **D2-275**, **D2-273** (spec/core/clocks.md) | A unit is 2 hours, 7, 6 and 5 units a day by season; the three clocks; making durable things on the year clock |
| **D2-288**, **D2-264** | Bulk goods in handling units of stated weight (timber and stone 25 kg, firewood 10 kg, straw a 16 kg truss, withies and bark 10 kg); every recipe in real kilograms |
| **D2-259** | Real values within about 20%; every departure a named lever |
| **D2-298**, **D2-297**, **D2-293** | Bots test interfaces only; the catch kept as calibrated (the weir's 30% share and 100 kg hold); calibration read in live runs |
| **D2-52**, **D2-171**, **D2-154**, **D2-155**, **D2-166**, **D2-168** | Skill by practice (trade 0.5 to 2.0, basic 1.0 to 1.5); finish tiers plain to grand (materials x1 to x4, work x1 to x8); space; storage; large capital village-scale (a hall about 300 units, a water mill 300 to 500 in all); breaks by structure |
| **D2-209**, **D2-210**, **D2-262**, Q-74, Q-75 | The weir in sections, upkeep a quarter to a third of its build a year; the weir's take allowed to be big at the low stations; the base split of a first section (Q-74, default taken); the yearly upkeep band (Q-75, default taken) |
| **D2-130**, **D2-132**, **D4-114**, fences.md, L-24, L-11, Q-30 | Fences round a parcel, wood or stone, with gates; a wood fence wears a level a year unless mended a quarter of its build; fences on borders, hedges and night folds flagged for later (L-24); livestock.md's table still says "a season" (Q-30) |
| **D2-148**, D2-128 | A head may set the household's children to herd (the `order` verb); a herder holds about 30 head |
| **D4-60** (clearing.md), **L-153** | Clearing turns a whole parcel into a field when all its work is done; clearing a plot at a time flagged (L-153, "waits on the timber economy or the building clock") |
| **D2-271**, **D2-284**, **D2-291** | The smoke hut and the timber or stone smokehouse; racks of about 250 kg on 1 space; the building caps the sets |
| **D2-274**, D2-279 | Moving between buildings about 1 unit per 800 kg a parcel step, provisional; the stores of storage.md |
| L-157 | Rest days flagged; they would lower the factor |
| hunt_fish_materials.md §6 | The works list: weir, racks, withy bed, retting pit, flax close |
| household_skills.md addendum (22 Nov, exploration) | Carpenter and mason as one builder livelihood (wright and mason), faster and sounder at master |
| Overnight drafts | wave1_physical_basis.md §3 and §4 (the cost tables at 1/7 and 1/15, carrying); building_clock.md (the audit); building_clock_bots.md (W-82: the switch and its 7 faults); wave_conflicts.md (K7, S13, E12, G7, G8, G9, G13, question 7); 02zzzi_timber/scouting.md (T4, questions 11 to 13) |

## Departures

Every place this spec differs from what it extends, with the reason.

1. **A timber is 25 kg, not 240.** building_clock.md stage 4 ("a timber is about 240 kg, so a small room's 8 timber is about 65 loads"),
   the audit's issue 4 and the timber scouting note's basis use the old 240 kg. D2-288 replaces it (basis §2). Every material here is
   in basis units; the 65-loads warning is re-derived in §8.
2. **The audit's tables at 1/11 are not used.** D2-276 set the labour factor (about 1/7), not the calendar's 1/11.
3. **The weir is sized by its water, not at a large river's size everywhere.** W-82's switch priced every first section at 325 real
   hours (a large river's take) so that the weir kept today's price. Sizing it by the kind of water it stands in (§3) is what the audit
   and building_clock.md asked for ("the weir sized to its take"); on a lowland river it comes out much cheaper than today.
4. **The switch's materials were today's units** (a fence's 4 timber, a room's 8 timber at the old weight). Its units of work are the
   audit's and are re-derived here; its run results are read for interfaces only (D2-298) and are not evidence of whether building
   happens or what starves. The fence-against-herding arithmetic is re-derived in §6 without the bots' herding hours.
5. **The audit's issue 7 ("a carpenter gets three to five times the practice from one house") is not what the code does.** A build
   act credits no practice; the finisher gets 1 unit of practice at the end (`verbs.py:1396`), a fitting 1 at its start
   (`verbs.py:1338`), a tier or a room 1 at the end (`verbs.py:1279`). Fixed in §5 under D2-52 (practice counts units of work).
6. **The reading between stages is a live run, not bots.** D2-281 says "read with bots between"; D2-298, later, says bots test
   interfaces and are no evidence of behaviour. The stage table (§4) follows D2-298: bots check that each stage's interfaces work,
   a live run with its null arm reads whether building still happens.
7. **Gear is not "on the rule from the start" at 1/7 while works are staged** (building_clock.md stage 1; K7). All capital priced
   in hours reads one lever at each stage (§1), so gear is never dearer per real hour than a house. The existing works are held at
   today's units until their companions are in (§4). Asked as question 2.
8. **Hurdles: 5 a unit at 1/7 and 10 at 1/15** (wave1 §3.2), not building_clock.md's "about 7 a unit" (C3). Hurdles are U3's gear;
   this spec only uses them.
9. **A cottage at 1/7 is 19 to 39 units in wattle and 32 to 51 in timber** (wave1 §3.5), not building_clock.md's "about 36 units for
   500 real hours" (C31), which mixed the two.
10. **The wood fence is woven wattle (or hurdles) on stakes, in withies and stakes**, not 4 timber a unit of size (data.py:966). The
    engine's row stood for "wattle or post and rail" with no materials of its own.
11. **Fences along one border are brought forward from L-24** (flagged for later in D2-130's sweep), because they are the "fence priced
    by its length" D2-276 asks for (§6.3). The mechanism is 37.4's.
12. **Clearing a plot at a time keeps the parcel whole.** clearing.md's alternative ("clearing part of a parcel into a new parcel:
    parcels are whole in the graph; left for when land is generated") is not taken; a cleared part is held as plots within the parcel
    (§7), as fields held in shares already are (D2-172).
13. **The dead hedge's brush is got in place, its cutting in the hours** (wave1 §3.7's reading), which bends D2-276's "materials stay
    real in rate" for material got at the site in the course of the work. This is the default taken; it is asked as question 1,
    together with field stone for walls.
14. **Herding by an adult stays 1 unit a day** (D2-128), against a real day of watching (about 5 units). This is an existing departure,
    named here because it sets what a fence must beat (§6). Asked as question 9.
15. **The cellar is priced by footprint** (storage.md §3.11, D2-279's set), replacing D2-155's flat 4 stone and 6 units; S4 already
    lists D2-155 and D2-166 as replaced without being marked so.
16. **A standing stone is one stone of its own** (1 to 5 t), not "4 stone" (wave1 §3.4); a cairn of 80 to 240 stone is gathered on the
    spot. Both are flagged, not built in this wave (monuments are not on the wave's path).

## Purpose

Make durable things cost their real share of a year (D2-276) without stopping villages from building, by pricing every work from
its real hours through one lever, sizing the weir to its water, and building the three companions that make the dearer works
buildable: builders as a trade, cheaper crop protection, and clearing a plot at a time. The works priced here (houses, the weir,
the smokehouses, the withy bed, the pits, fences, clearings) are what the other units' keeping, stores and taking stand on, and the
holders of these works are the wave's chokepoints (scenario_design.md §1): the weir's site and right, the wood, the builder, the
stone, the straw.

## The design

### 1. The capital factor: one named lever in `clocks.py`

**The lever** (new, `data.py` beside PHYSICS, read only through `clocks.py`):

```
CAPITAL = {
    "factor": "1/15",          # the stage (D2-281): "1/15", then "world"; any fraction for a sensitivity arm
    "real_year": 2700,         # real working hours a year (D2-276: "about 2,700 real")
    "hold": ["rooms", "fittings", "monuments", "weir", "fences", "clearing", "works"],   # classes at today's units until stage 5
    "floor": 1,                # every capital act costs at least 1 unit (basis §1)
}
```

- **"world"** is D2-276's factor worked out from the world's own numbers: `units a year x 2 hours / real_year`. The units a year are
  the adult's day by season (PHYSICS `units`) times the season's days (`year_days / 4`). In a 32-day world: (7 + 6 + 5 + 6) x 8 =
  192 units = 384 hours, so the factor is 384 / 2,700 = **1/7.03**. A world with a longer year or a shorter day gets its own factor;
  rest days (L-157) would lower it.
- **A fraction** ("1/15", "1/40") is a stage or an arm, named in the world's settings when it is not the default.
- **One lever, every class.** Rooms, fittings, monuments, the weir, fences, clearing, field works, containers (U5), processing
  works (U4) and gear (U3) all read it. No class has its own factor (audit issue 2). A class in `hold` keeps its row's `units` as
  written today, a named departure that is removed class by class at stage 5 (§4).

**The conversions** (new functions in `clocks.py`, 37.2):

| Function | What it returns | Rule |
|---|---|---|
| `capital_factor(w)` | the factor for this world | "world": `sum(PHYSICS units by season) x year_days/4 x 2 / real_year`; else the fraction; a world spec may set `capital_factor` |
| `capital_units(row, w, n=1)` | the units of work a capital row takes | if the row's class is held: its `units` x n; else `max(floor, hours x n x factor / 2)`, rounded to a tenth |
| `capital_life(uses, w)` | a life counted in acts of work | `max(1, round(uses x factor))`, so a use costs the same at every stage (wave1 §3.0) |
| `night_life(nights)` | a life counted in nights | `max(1, round(nights x 32 / 365))`, the calendar's (basis §1, open: lives in nights) |

- **Rows carry real hours.** Every capital row gets `hours` (the middle of the real range, D2-259) and keeps `units` only while
  its class is held. Lives in uses carry `uses` (real) and are converted by `capital_life`. Units are never copied out of a row at
  import: the build techniques read them through `capital_units` (this fixes W-82's fault 4: the shown units going stale).
- **Upkeep goes with the thing** (D2-276): a share of the build (a fence's quarter, a weir level's 0.06) follows the build's units;
  a fixed upkeep (the house repair's 1 unit a 4 spaces a level, PHYSICS `repair`) is kept, since it already sits at the rule's figure
  (audit §3; wave1 §3.8).
- **RATES** gains `("*.hours", "capital")`, `("*.uses", "capital")` and the clock name `capital` in `clock_of`, so
  `test_cybertron2_clocks.py` checks that every capital row names its clock.

### 2. The works: real hours, units at each stage, materials, life and upkeep

Units are `hours x factor / 2` with the floor of 1 (§1). "Today" is data.py on main. Materials are in basis units (§2: timber and
stone 25 kg, withies 10 kg, straw a 16 kg truss, firewood and brush 10 kg). Real hours and materials are wave1 §3.4 to §3.7 [n],
themselves mostly estimates from the audit and storage.md; I have not re-sourced them.

**"Getting"** is the day-clock work to get the materials at real rates (D2-276: materials real in quantity and rate), at wave1
§3.1's proposed rates (U3's and U0's; a basis row is needed): fell 4 timber a unit with a crude tool, quarry 4 stone a unit, cut
withies 4 a unit from a bed and 1.5 wild, brush 5 bundles a unit; straw is a by-product of reaping (no work, but scarce: §2.3). It
is not part of the build's units; it is shown because for the heavy works it is the larger cost.

#### 2.1 Rooms, huts and smokehouses

| Work | Real hours | Today | 1/15 | 1/7 | Materials | Getting | Life (time) | Upkeep |
|---|---|---|---|---|---|---|---|---|
| small room, wattle (6 spaces) | 270 to 540 | 6 | 9 to 18 | 19 to 39 | 36 timber (posts and poles), 35 withies, 75 straw (2.5 t) | 18 to 32 | 20 to 40 world years | repair as now; rethatch every 10 to 20 years, 60 to 100 h and 75 straw |
| small room, timber (frame on a stone sill) | 450 to 720 | 6 | 15 to 24 | 32 to 51 | 160 timber, 60 stone, 15 withies, 75 straw (5.5 to 8.5 t) | 59 to 65 | centuries with upkeep | 1 timber a level (as now) |
| small room, stone | 630 to 1,260 | 40 | 21 to 42 | 45 to 90 | 1,600 stone, 40 timber, 75 straw (42 t) | 410 | centuries | 1 stone a level |
| medium room, timber (12) | 720 to 1,350 | 15 | 24 to 45 | 51 to 96 | 270 timber, 100 stone, 25 withies, 130 straw | 99 to 109 | | |
| medium room, stone | 1,080 to 2,250 | 90 | 36 to 75 | 77 to 161 | 2,700 stone, 70 timber, 130 straw | 693 | | |
| hall, timber (30) | 3,600 to 8,100 | 200 | 120 to 270 | 257 to 579 | 560 timber, 210 stone, 50 withies, 260 straw | 205 to 226 | | |
| hall, stone | 5,400 to 10,800 | 250 | 180 to 360 | 386 to 771 | 5,600 stone, 140 timber, 260 straw | 1,435 | | |
| **hut room, wattle** (2 spaces; new) | 90 to 180 | none | 3 to 6 | 6.4 to 13 | 12 timber, 16 withies, 30 straw | 7 to 14 | 10 to 20 world years | as wattle |
| **wattle smoke hut** (a hut room and 1 set of racks; D2-271) | 96 to 190 | none | 3.2 to 6.3 | 6.9 to 14 | 14 timber, 18 withies, 30 straw | 8 to 16 | 10 to 20 world years | hot and keeping smokes; burns with its batch (U4) |
| **timber smokehouse** (a small timber room and 4 tiered sets) | 490 to 776 | none | 16 to 26 | 35 to 55 | 172 timber, 60 stone, 27 withies, 75 straw; a carpenter | 65 to 76 | centuries; racks 5 years | all three smokes; seldom burns (U4) |
| stone smokehouse (a small stone room and 3 to 4 tiered sets) | 660 to 1,316 | none | 22 to 44 | 48 to 94 | 1,600 stone, 49 to 52 timber, 9 to 12 withies, 75 straw; a mason | about 415 | centuries | almost never burns |
| granary on staddles (U5's store) | 500 to 800 | none | 17 to 27 | 36 to 57 | 170 timber, 60 stone (9 staddles), 75 straw | 58 | centuries | |
| camp (day clock: lasts 10 nights) | 3 to 5 | 1 | 2 (day clock, real hours / 2) | 2 | 3 timber | 1 | 10 nights | none |

Added rooms (x0.75), upper storeys (x1.5, x2), upgrades (x0.75 of materials) and tiers (D2-171) keep their multipliers on the
converted units (SPACE, TIERS; `buildings.room_cost`).

#### 2.2 Fittings, stores and monuments

| Work | Real hours | Today | 1/15 | 1/7 | Materials | Getting | Life | Upkeep |
|---|---|---|---|---|---|---|---|---|
| beds (each) | 4 to 9 | 1 | 1 | 1 | 1 timber, 1 straw | 0.2 | 10 world years | 1 straw a year |
| hearth | 9 to 18 | 3 | 1 | 1 to 1.3 | 20 stone | 5 | decades | |
| fire ring | 1 to 4 | 1 | 1 | 1 | 4 stone | 1 | years | |
| owl hole | 1 to 4 | 1 | 1 | 1 | 0.1 timber | 0 | years | |
| bins (boarded, 300 kg) | 9 to 18 | 1 | 1 | 1 to 1.3 | 3 timber | 0.8 | 10 world years | |
| granary floor (1,200 kg) | 27 to 45 | 4 | 1 to 1.5 | 1.9 to 3.2 | 20 timber | 5 | 20 to 30 world years | |
| hand mill | 18 to 45 | 2 | 1 to 1.5 | 1.3 to 3.2 | 2 stone | 0.5 | decades | |
| oven (stone) | 36 to 72 | 12 | 1.2 to 2.4 | 2.6 to 5.1 | 60 stone, 0.4 timber | 15 | shell decades; lining 30 to 70 firings at 1/7 (`capital_life` of 200 to 500) | reline: its share of the build, 4 stone |
| anvil and bellows | 27 to 45 | 4 | 1 to 1.5 | 1.9 to 3.2 | 4 stone, 2 leather (U10), 0.4 timber | 1 | years | |
| cellar, timber-lined, a space of footprint | 30 to 52 | 6 flat | 1 to 1.7 | 2.1 to 3.7 | 1.5 timber a space | 0.4 | 10 world years | |
| cellar, stone-lined, a space of footprint | 60 to 105 | 6 flat | 2 to 3.5 | 4.3 to 7.5 | 190 stone a space | 48 a space | decades | |
| millstones | 180 to 360 | 10 | 6 to 12 | 13 to 26 | 60 stone | 15 | dressed every 1,400 to 3,600 grain at 1/7 | dress: its share |
| water wheel and leat | 1,440 to 4,680 | 250 | 48 to 156 | 103 to 334 | 200 to 400 timber, 80 to 200 stone, 2 copper | about 110 | leat silts in a year | clear the leat: 3 to 10 real days, at the factor |
| stalls (each) | 4 to 9 | 1 | 1 | 1 | 2 timber | 0.5 | 10 world years | |
| woodshed | 18 to 36 | 1 | 1 to 1.2 | 1.3 to 2.6 | 20 timber, 15 straw | 5 | 15 to 20 world years | |
| brine pan | 18 to 36 | 4 | 1 to 1.2 | 1.3 to 2.6 | 10 copper, 4 stone | 1 (and the copper) | 40 to 90 boilings at 1/7 | 0.25 copper |
| vault | 900 to 1,800 | 30 | 30 to 60 | 64 to 129 | about 3,000 stone | 750 | centuries | |
| smoke loft | 2 to 4 | none | 1 | 1 | 0.2 timber | 0 | years | |
| smoke racks, a set (250 kg on 1 space; D2-284, D2-291) | 6 to 10 | 2 | 1 | 1 | 2 withies, 2 timber | 1 to 2 | 5 world years | |
| smoke racks, a tiered set | 10 to 14 | none | 1 | 1 | 3 withies, 3 timber | 2 to 3 | 5 world years | |
| hay rick, root clamp, sealed pit (U5) | 27 to 36; 8 to 10; 8 to 10 | none | 1 to 1.2; 1; 1 | 1.9 to 2.6; 1; 1 | 1 straw a tonne held | 0 | a year; a winter; years | |
| carved post | 18 to 45 | 2 | 1 to 1.5 | 1.3 to 3.2 | 2 timber | 0.5 | decades | |
| cairn | 6 to 12 | 3 | 1 | 1 | 80 to 240 stone gathered on the spot | (in place) | centuries | |

#### 2.3 Works on land and water

| Work | Real hours | Today | 1/15 | 1/7 | Materials | Getting | Life | Upkeep |
|---|---|---|---|---|---|---|---|---|
| **withy bed** (200 m², U3's) | 18 to 24 | none (proposal's 10) | 1 | 1.3 to 1.7 | 1 withies (the cuttings) | 0.3 | 30 years | a fence or a dead hedge against beasts |
| **retting pit** (U3, U10) | 18 to 45 | none | 1 to 1.5 | 1.3 to 3.2 | none (dug) | 0 | silts in 10 world years | |
| **tan pits**, 3 to 5 by water (U10) | 30 to 60 | none | 1 to 2 | 2.1 to 4.3 | 4 timber, clay puddled on the spot | 1 | 20 world years | |
| wattle fence, 100 m (§6.3) | about 190 | (see the parcel row) | 6.3 | 14 | 56 withies, 13 timber (stakes) | 17 to 41 | 5 to 10 world years | a quarter of the build a year (D4-114) |
| wattle fence round a size-1 parcel (566 m) | about 1,075 | 10 | 36 | 77 | 317 withies, 74 timber | 98 to 230 | as above | as above |
| **dead hedge, 100 m** (§6.2; new) | 22 to 45 | none | 1 to 1.5 | 1.6 to 3.2 | 1 to 3 t of brush and thorn, got in place (est.) | in the hours (default; question 1) | 2 to 3 world years | a third of the build each half year |
| dry-stone wall, 100 m | 150 to 300 | (8 stone, 20 units x √size) | 5 to 10 | 11 to 21 | 4,000 to 8,000 stone | 1,000 to 2,000 if quarried; in place on stony ground (question 1) | keeps | little |
| clearing turf to field, a plot (§7) | 54 to 90 | 6 | 1.8 to 3 | 3.9 to 6.4 | none | none | the field persists | |
| clearing scrub to field, a plot | 360 to 900 | 10 | 12 to 30 | 26 to 64 | none; leaves the plot's brash as dead wood | none | regrows if left | |
| clearing for building, a plot | turf 36 to 60; scrub as scrub clearing | 4; 10 | 1.2 to 2; as scrub | 2.6 to 4.3; as scrub | none | none | | |
| ditching wet ground, a plot | 180 to 360 | 40 | 6 to 12 | 13 to 26 | none | none | silting | 1.5 a year (D2-66, kept) |
| terracing, a plot | 1,800 to 3,600 | 60 and 6 stone | 60 to 120 | 129 to 257 | the slope's own stone | in place | slumping | 1.5 a year |
| the weir | §3 | | | | | | | |

**Two checks.** D2-166 wants a hall and a water mill to be village-scale: a timber hall is 120 to 270 units at 1/15 and 257 to 579 at
1/7, with 205 to 226 units of getting its materials; a water mill (wheel, leat and millstones) 54 to 168 and 116 to 360, with about
125 of getting. The hall lands in D2-166's 300 to 500 in all at 1/15 (325 to 496) and above it at 1/7; the water mill below it at
1/15 (179 to 293) and in it at 1/7 (241 to 485). And a small wattle room plus its getting is 27 to 50 units at
1/15 and 37 to 71 at 1/7, against 6 plus about 5 of felling today.

**What the getting column shows.** Under D2-276 as decided, the stone works cost several times their real share of a year: a small
stone room is 45 to 90 units of building at 1/7 but about 410 of quarrying (a real 400 to 800 hours, about a fifth of a real year,
becomes two world years of one adult), because the making is compressed and the material's getting is not. The same holds for walls
(1,000 to 2,000 units a 100 m) and, less, for fences (withies). Real stone houses and walls were mostly of stone got at or beside
the site, field stone above all. This is question 1.

**Straw for thatch.** A small room's roof is 75 trusses (1.2 t of long straw at about 27 kg a m², wave1 §3.5 [s]). Reaping gives
4.7 trusses a plot (basis §2's truss on data.py's rate), so one roof is about 16 plots' straw: about half a year of a 30-plot village's
straw, before beds, fodder and the hay rick. I don't know whether the plot's straw rate or the real roof is the one to trust; it
means thatch could bind house building in the first live run. Asked as question 10; a gate check (U11) should count a world's straw
against the houses it may need.

#### 2.4 Gear, containers and processing works

Their rows are U3's, U5's and U4's; they carry `hours` and `uses` and read the same lever (§1). At 1/15 the gear table of wave1 §3.2
roughly halves its batches (a unit gives 10 hurdles, 6 traps, 4 crude tools) and its lives in uses fall by 7/15 so a use costs the
same; at 1/7 they are wave1 §3.2's figures.

### 3. The weir sized to its take

> **Replaced 23 Nov by D2-302** (Zach: "Record weir cost as you put for now"): the weir's cost is set directly, from what it returns, not from the hours model below; see basis.md ("The weir's cost"). The model is kept as the reasoning it replaced.

**The rule.** The take is fixed by the catch basis (basis §4: the first section 30% of a run passing up to 100 kg a night, each added
section 7% up to 70, at most three; D2-293, D2-297). What varies is the work: a weir that takes that share must reach across a share
of its channel, so its size, materials and hours follow the river it stands in. The engine already names three kinds of weir water
(`wild.water_kind`, wild.py:2966): an upland **beck**, a **lowland** river, and a **large** river (the stretch holds big river). The
weir is sized by that kind.

**The model** (all est.; no sourced figure for a medieval weir's length and depth was found in the notes):
- A full weir (the first section and three added) is a V of wattle on stakes across the whole channel to the gap where the traps sit:
  wings about 1.4 times the channel's width in all.
- **The first section** is the crib (the heavy posts that hold the trap at the gap) and the inner 40% of the wings; **each added
  section** a further 20%.
- **Wattle in place** about 2.1 hours a metre at 1.5 m high (withies_wood_materials.md: a 10 m by 1.5 m section in about 21 hours),
  in proportion to the height; in a large river's current half as much again, its stakes twice as heavy.
- **Materials a metre** at 1.5 m high: 1.2 withies and 0.7 timber of stakes (the same note: 12 withies and 7 timber for 10 m), in
  proportion to the height.

| Water | Channel (est.) | Wattle height (est.) | Crib | First section: hours, materials | 1/15 | 1/7 | An added section: hours, materials | 1/15 | 1/7 |
|---|---|---|---|---|---|---|---|---|---|
| **beck** | 3 to 6 m | 1.0 m | 4 to 8 h, 8 timber | 6 to 13 h; 2 withies, 9 timber | 1 | 1 | 1 to 2 h; 1 withies, 1 timber | 1 | 1 |
| **lowland** | 10 to 20 m | 1.5 m | 15 to 30 h, 40 timber | 27 to 54 h; 10 withies, 46 timber | 1 to 1.8 | 1.9 to 3.8 | 6 to 12 h; 5 withies, 3 timber | 1 | 1 |
| **large** | 30 to 60 m | 2.3 m | 40 to 80 h, 100 timber | 122 to 243 h; 47 withies, 154 timber | 4.1 to 8.1 | 8.7 to 17 | 41 to 82 h; 23 withies, 27 timber | 1.4 to 2.7 | 2.9 to 5.8 |
| today (any water) | | | | 24 units, 12 timber (old weight) | | | 16 units, 6 timber | | |

- **A timber section** (D2-210) takes 1.7 times its wattle section's hours (wave1 §3.7: 30 to 50 h against 21), no withies, and 4
  timber a metre more in proportion to the height; **a stone footing** 3 times the hours and 20 stone a metre in proportion to the
  height (wave1: 200 to 600 stone a section); upgrading costs the difference (D2-210, kept).
- **The lowland weir matches the research size** the audit started from (36 to 51 hours): that note's weir was a lowland one.
- **Upkeep** keeps D2-210's band through Q-75's calibration: a level's mend is 0.06 of its section's build. With builds near the floor,
  one mending act must mend as many levels as its work covers (today one act mends one level: verbs.py:1232), or the floor makes
  upkeep dearer than the build. Its withies stay real: about 6 withies a wattle section a year (withies_wood_materials.md), so the
  weir's crew needs a bed or a wild source (U3).
- **What this means.** On a beck or a lowland river the weir becomes a few units of a crew's work, about a tenth of today's price.
  Its leverage is not its labour but its site and right (one weir a water parcel, upstream first: D2-210), the crew (2, named), the
  withies and stakes, its upkeep and above all keeping the glut (U4, U5). That matches the record: weirs were valuable as rented
  fisheries, for their site, not their hours (catch_basis.md §2). A large river's weir stays a real work (9 to 17 units at 1/7).
- **Data** (37.2 for the numbers; the code that reads them is wild/gear.py and verbs.py): `WATER_WORKS["weir"]["size"] = {kind:
  {"width": m, "height": m, "current": x, "stake": x, "crib": {"hours": h, "timber": n}}}`; `position.first.share_of_wings: 0.4`,
  `added: 0.2`; `material.*` as hours and materials a metre. **MONUMENTS["weir"] loses its own units and materials**: the first section's
  cost comes from WATER_WORKS alone, by the site's water (W-82's fault 2: the cost was held twice).

### 4. The stages and what each waits on

| Stage | What moves | Waits on | Read by |
|---|---|---|---|
| **1** (with U0, README stage 1) | `CAPITAL` and the conversions in `clocks.py`; every capital row gains `hours` (and `uses`); all existing works **held** at today's units; the 1-unit floor in `verbs.cost` (U0's) and a build act that costs what is left (§5.4); practice for every build act (§5.2); the weir's cost in one place; units read through the function; the act log; `PHYSICS.cattle.stray` removed (W-82's faults 1 to 5) | U0's handling units (D2-288), since materials are rewritten in kilograms in the same stage | unit tests; a bot run for interfaces |
| **2 to 4** | U3's gear, U4's processing works (racks, the smoke hut, the smokehouses, the tub, pits), U5's containers and stores: **new rows, priced on the lever at 1/15 from the start** (no "today" to hold) | their units | their tests |
| **5a: the companions** | builders as a trade, minimal (§5); children herding daily, the dead hedge, fences along a border (§6); clearing a plot at a time (§7); the weir sized by its water (§3); building materials carried to the site (§8) | 37.4's mechanism for border fences and plot holdings; question 1 for in-place materials | unit tests; a bot run for interfaces |
| **5b: release the hold** | first rooms, fittings, monuments, the weir and the stores to 1/15; then fences, clearing and field works to 1/15, once 5a's companions pass their tests | 5a | bot interface run; then **a short live run** (D2-281) against its null arm: a farm world with a newcomer household (W-82's Brookend arm) and the remade founding world (U11) |
| **5c: the target** | `factor: "world"` (about 1/7) | the 5b live reading: houses, fields, fences and the weir begun and finished, the share of work in building against the null arm, and an end-state reading of who holds the works (scenario_design.md §6) | a second live run |

- **Why hold the existing works** (rather than raise them at stage 1): the bot arithmetic (W-82 §3.4, re-derived in §6) shows the fence
  and the scrub field breaking before their companions exist, and the houses' straw (§2.3) is not yet checked.
- **Why gear is not held:** it has no today's price to keep (U3's gear is new), and at 1/15 it stays far below today's net (30 units)
  and trap (2.5).
- **K7 in this plan:** during stages 1 to 4 gear sits at 1/15 while held light works sit near 1/40: gear is dearer per real hour than
  a held house for those stages. That is the price of holding; it ends at 5b. The alternative (everything at 1/15 at stage 1) is
  question 2's option (a).

### 5. G7: builders as a trade (minimal; W-76 extends)

What the engine already has: an act of building does `2 x skill` units of work (verbs.py:1258, 1354, 1380), so a master of a trade
(2.0) already does four times a novice's (0.5) work an act, and the units a row states are for one at skill 1.0 (wave1 §3.0: a novice
about twice, a master about half). Medium rooms, halls and the water wheel need a carpenter; stone needs a mason. Five things are
missing.

**5.1 One skill a trade, not one a blueprint.** Today skill is kept per technique: a carpenter's practice on medium rooms gives
nothing on a hall or a timber smokehouse. Two knowledge-only techniques hold a trade's skill: **carpentry** (`trade: carpenter`, the
timber structure and the carpenter's fittings) and **masonry** (`trade: mason`, the stone structure, hearths, ovens, cellars,
millstones, vaults, walls); wattle and camps stay basic. They have no verb of their own: an act of building uses
`max(KN.skill(mind, tech), KN.skill(mind, craft))`, where `craft` is the work's structure's trade record. A person seeded knowing any
carpenter's or mason's technique is given that craft at the same level and skill (as knowledge.py:99-103 already gives a seeded mason
walling). Nothing else is seeded; the builder livelihood with wright and mason specialisms (household_skills.md addendum) is U9's and
U11's.

**5.2 Practice for every act** (D2-52: practice counts units of work). Each act of building, on a room, a fitting, a monument, a weir
part, a tier or an upgrade, calls `KN.tried(here, mind, tech, True, units=<the act's units>)`, and the same units to the craft record
for timber and stone work; the finisher's and starter's single credits go (verbs.py:1279, 1338, 1396). On the trade curve (0.5 to
2.0, tau 50: D2-52's SKILL), a carpenter with about 35 units of practice (skill about 1.25) who frames a timber smokehouse at 1/15
(16 to 26 units, about 10 acts of 2) reaches about 1.5; a novice (0.5) reaches 1.25 after about 35 units of acts, within one medium
timber room at 1/15.

**5.3 Soundness from craftsmanship.** A building records `sound`, a multiplier on its wear and breaks, the work-weighted mean over the
acts that built it of each act's multiplier from its builder's skill share s (0 at the curve's foot, 1 at its top, `knowledge.py`
`SKILL_WORDS`'s share):

| Curve | Multiplier m(s) | novice / ordinary (s = 0) | competent (0.2) | skilled (0.5) | master (0.85 to 1) |
|---|---|---|---|---|---|
| a trade (timber, stone) | 1.5 − s, at least 0.5 | 1.5 | 1.3 | 1.0 | 0.65 to 0.5 |
| basic (wattle, a camp) | 1.0 − 0.5 s | 1.0 | 0.9 | 0.75 | 0.58 to 0.5 |

- The basic curve starts at 1.0 so that today's wattle houses keep their calibrated breaks (D2-168, shelter in levels); seeded
  buildings get `sound: 1.0` unless the world says.
- **Applied:** `night.py:222` (the break chance) and `night.py:622-626` (minor and serious wear) multiply by `b.get("sound", 1.0)`.
  A rebuilding (an upgrade) sets `sound` afresh from its own acts; mending does not change it (W-76 may).
- **Result line at the finish,** appended to today's: m ≤ 0.7 "The work is fine and true: it will stand long."; 0.7 to 1.1 "The work is
  sound."; above 1.1 "The work is rough: it will want mending often."
- **Seen by those who can judge** (D2-269: an expert's observation, a standing fact, so in the place's layout, not a sign): one whose
  skill in the trade is skilled or above reads the building's line with "soundly framed" / "finely built and true" or "roughly put
  up: its wattle is loose" (layout.py's building words; 37.4).

**5.4 A build act costs what is left** (W-82's question 4, option b). `verbs.cost` for `build` on an unfinished work (or a fitting
whose whole work is under 2 units) is `max(1, min(2, ceil(left / (skill x yield))))`; the act puts in that many units times skill.
Without this the 1-unit floor is a 2-unit floor for every fitting and small work (W-82's fault 1). Beds and stalls keep `qty`, so
several go in one act.

**5.5 Finish tiers need a builder of skill.** D2-171's tiers multiply work by 2, 4 and 8, and at the factor a grand hall is a lord's
years of work: the tier is the builder's show. A tier above plain is begun only by one whose trade skill is at its word or above:
**fine** competent, **rich** skilled, **grand** master. Others may work on it at half their act's work (the rough work under a better
hand; est.). Refusal: "A fine finish needs a hand of some skill at carpentry (competent or better), and you are a novice at it: build
it plain, or have one with the skill begin it." The tier's soundness is set as in 5.3.

**Left to W-76** (scouting T4, questions 11 to 13): the raising as crew work, a framed cottage needing a builder at capable, seasoning
and boards, framing at the wood and carrying the frame, a builder's mending setting soundness. Nothing here forecloses them.

**Hiring a builder** needs nothing new: anyone may carry on an unfinished building at their node (verbs.py:919-921), and work for
another is an agreement (D2-36 to D2-40). Whether households hire builders is a live-run reading.

### 6. G8: cheaper ways to protect crops

**What a fence must beat** (re-derived, not from the bots' hours). A herd strays when it is neither herded that day nor held by a
shut fence (livestock.md "Staying put"); herding is 1 unit a day a herd (D2-128; departure 14). Crops stand within a herd's reach
for perhaps 16 to 24 days of a 32-day year (est.), so an adult's herding costs 16 to 24 units a year, and a child's nothing of an
adult's day. A wattle fence round a 6-plot pasture (1,386 m) is 88 units at 1/15 and 188 at 1/7, its mend a quarter of that a year
(22 and 47), plus 776 withies (194 to 517 units of cutting) and 182 timber; it never pays against herding, and the protections below
are the real choice, as open-field villages had it.

**6.1 Herding by children** (the order exists: D2-148, `order {what: herd}`, LIFE `children_work`).
- **Daily, not every other day.** At the high dial a child does the order half the days (`child_works` 0.5, life.py:242), which suits
  small output work (forage, firewood) but leaves a herd unwatched every other day. Herding is watching: a child ordered to herd herds
  every day (`LIFE["children_daily"] = ["herd"]`, skipped from the share).
- **Fewer head:** a child herder holds about **15 head** (est.; I found no source), a youth or adult 30 (`HERDS["capacity"]["child"]`;
  farm.py:677 counts herders by stage).
- **The order names the herd, not only a place:** `order {what: herd, herd: "the Croft cows"}`, so it follows a herd that is driven.
- **The head is told when it fails** (a change worth acting on, not every day): "Tom could not watch the Croft cows today: they were
  not on Long Pasture." (the children's result line, shown to the head at evening; 37.4's prompt).
- **What it makes:** a household with children protects its crops at no adult cost; one without needs an adult, a hedge or a
  neighbour's child (an agreement). A dependence, cheaply.

**6.2 The dead hedge** (new: FENCES kind `hedge`, technique `dead hedge`).

| Field | Value |
|---|---|
| technique | `dead hedge`, verb `work`, basic, aliases "hedge", "dead hedging", "brush hedge", "thorn hedge", "hedge it"; at pasture, meadow, field, scrub |
| hours | 34 a 100 m (22 to 45, wave1 §3.7 [n]: 20 to 40 m a day), the cutting and carrying of the brush from beside it folded in (default; question 1) |
| brush | about 150 bundles a 100 m (1 to 3 t, est.; I found no sourced figure), drawn in place in proportion to each act's work from the parcel's or an adjoining parcel's young growth or dead wood (forest, scrub, or brash left by clearing: §7) |
| holds | a herd gets through at 0.35 a day whole, 0.7 gappy (est.; a wattle fence 0.3 and 0.6) |
| wear | loses a level each half year unless mended a third of its build that half year (est.: brush rots and settles); a fallen one keeps nothing |
| life | 2 to 3 world years kept up; it is topped up, never rebuilt whole |
| words | ("hedge", "a dead hedge of thorn and brush") |

- **Refused with no brush near:** "There is no brush to hand at Long Pasture or beside it: a dead hedge is made of thorn and brush cut
  close by. Make it where scrub, a wood or a hedge is near, or put up a wattle fence."
- **Progress:** "You worked on a dead hedge along Long Pasture by East Field: about 40 parts in a hundred done."
- Built round a parcel or along one border (6.3), with the same gates.

**6.3 Fences priced by their length, and along one border.**
- **By length.** FENCES rows hold hours and materials a 100 m; a parcel's round is 566 m x √size (a plot about 2 ha, 141 m a side;
  basis row needed), which is today's `x √size` made explicit. `fence_need`'s floor at size 1 goes (no parcel is smaller, so nothing
  changes but the arithmetic's honesty).
- **Along one border** (L-24's "fences on the borders between parcels", brought forward): `work {what: fence | wall | dead hedge, at:
  <parcel>, along: <the parcel next to it>}`. The border's length is 141 m x √(the smaller parcel's size) (est.: the parcel graph holds
  no border lengths; a deterministic estimate, named). The record sits on the pair (`w.s["borders"]["<a>|<b>"]`, sorted ids), with
  kind, level, units, mend, gate and pending as a parcel's fence has, and wears and is mended the same way (herds.py `_fences`).
- **What a border does:** a herd's step from one parcel to the other crosses it at its odds, besides each parcel's own fence
  (herds.py `target` and `wander`); a parcel fenced round is unchanged. Holders of either parcel may work on it; it is a joint work
  (fences.md), and its mending is for custom or an agreement.
- **The cheap case:** the 6-plot pasture's border with the 18-plot field is 345 m: a dead hedge there is about 117 hours, 3.9 units at
  1/15 and 8.4 at 1/7, from brush beside it; a wattle fence there 22 and 47 units plus 193 withies. Fencing the crop's side, not the
  pasture round, is a quarter of the length or less.
- **Signs:** the FENCE bundle (signs.py:243-300) gains the hedge's words and the border's context: "the dead hedge along Long
  Pasture has sagged and opened: gaps a beast could push through" (sight, `own` 0.5, knack fence); "the brush of the dead hedge by East
  Field has gone grey and brittle" (sight, `own` 0.4, in its last half year unmended: a change that asks for mending); the existing
  "nobody is watching ..., and the fence between them and ... has gaps" row reads a border too. `own` values are first estimates, to be
  checked through `perceive.chance_of` (senses guide, checklist 4).

**6.4 Moved folds: designed, recommended to wait for sheep.** A fold is U3's hurdles (10 kg, 1 withies each) pitched as a pen on a
parcel: about 4.4 √n hurdles for n head (est.: a cow about 4 m², a hurdle about 1.8 m), pitched or taken up at about 20 hurdles a unit
(est.); a herd driven into it is held and does not wander or trample, but grazes only the fold's ground, so it must be fed from
stores or the fold moved each day (about 1 unit); a folded herd's dung goes onto the plot under it. For cattle at the engine's day
resolution this costs what herding costs and duplicates stalls; its real use was sheep folded on fallow (L-36, L-119's "sheep, folds
and lambs"). **Recommended: defer folds to sheep** (a deferred row, waiting on L-36).

**Stone walls** stay as built (D2-130), led by one who knows walling; with stone real, a wall needs its stone where it stands
(question 1; wave1 question 6).

### 7. G9: clearing a plot at a time (L-153)

**The state.** A parcel's `clearing` becomes `{"units": u, "plots": n}`: the work put in, and the whole plots cleared so far
(`n` from 0 to its size). Each `clear` act adds its work (as now, with the tool's and skill's multipliers, bare hands 0.4); when
`units` reaches `(n + 1) x` the cover's work a plot (CLEARING, converted by `capital_units`), a plot is done and `n` rises.

**A cleared part.** While `0 < n < size` the parcel keeps its cover (scrub, meadow or pasture) and holds a field part of `n` plots:
- **Breaking, sowing, weeding and reaping** are allowed on it: the technique's cover check (`at.covers: ["field"]`) passes for a parcel
  with `n ≥ 1`, and the ground they may use is the cleared plots only (farm.py `_break`'s room, `_sow`'s `phys`). Seed sown there takes
  no turf penalty (farm.py:999 reads the part, not the cover).
- **Whose:** if nobody held the parcel, the clearer (or their household, or the party) claims the plots cleared, a part claim with
  `plots: n` and grounds "cleared" (D4-60's custom, by plots as D2-172 holds fields in shares), growing with each plot. If someone holds
  it, the cleared plots are theirs, as today.
- **Fertility** of each cleared plot: CLEARING's by cover (meadow 1.1, pasture 1.0, scrub 0.85), unless the land says.
- **The rest of the parcel** keeps its stocks in proportion: grass K (pasture, meadow) and young growth and dead wood (scrub) x
  `(size − n) / size`, set as each plot is cleared. **The brash of a scrub plot** (its share of the young growth) is left as dead wood on
  the parcel (D2-156's brash rule): firewood, and the dead hedge's brush (§6.2) round the new plot.
- **Herds** on the uncleared part can reach the cleared part's crop as any field's (herds.py's value reads every holding's crop): a
  dead hedge on the part, or herding, protects it. Border fences do not split a parcel; the part's protection is the parcel's own
  fence or a hedge round the part, priced at 566 m x √n (est.).
- **When the last plot is cleared** the cover becomes field, as today (verbs.py:2269 to 2283), and the part claims become the parcel's
  shares (D2-172).

**Lines** (verbs.py `_clear`, 37.4):
- Progress: "You cleared ground at the Brakes: about 14 units of work left before the next plot is clear (1 of 3 plots cleared)."
- A plot done: "You finished clearing a plot of the Brakes: it is ready to be broken and sown, and yours: you cleared it. 2 plots of it
  are still scrub."
- The layout's line for the parcel (a standing fact): "the Brakes: scrub, 1 plot of it cleared" and, once sown, its crop as any field's.

**Signs** (a new CLEARING bundle in signs.py, 37.4's senses):
- the day a plot is finished, and lingering two days: "a plot of the Brakes has been grubbed out: bare earth, root holes and heaped
  brash among the scrub" (sight, near, `own` 0.8);
- while clearing work is done there that day: "the thud of mattocks and the crack of roots from the Brakes" (sound, around, `own`
  0.6).

**What it changes, in numbers:** a 3-plot scrub field at 1/15 is about 21 units a plot (12 to 30), so a couple's spare units clear the
first plot in days and sow it that season, against 63 units before anything could be sown; at 1/7, 45 a plot against 135.

**Clearing for building** stays whole: it is cheap (a plot of turf 1.2 to 2 units at 1/15) and built ground's spaces come with the
plot.

### 8. A work's materials carried to its site

Materials are drawn when a work is begun, from hands and the stores at the node one may take from (`verbs._consume`). Under the
provisional moving rate (basis §5: about 1 unit per 800 kg a parcel step, a quarter on the same parcel; D2-274), materials drawn from a
store on another parcel than the site add their moving units to the work left, at that rate (default; basis §5 marks it open, wave1
question 5). The result line names it: "The timber is carried over from the Croft woodshed: about 7 more units of work." On the
road, nothing changes (the carry limits apply: basis §5). Wave1 §4.3's reading follows: carrying adds about a tenth a parcel step to
wattle, a fifth to a third to timber framing, as much again as the building for stone (52 units a step for a stone room's 42 t). The
timber scouting note's 65 loads on foot for a small room (at 240 kg a timber) do not arise: a small timber room's 160 timber is 4 t,
about 5 units a parcel step.

## Code changes

By file, with line on main as of 22 Nov (66b61bd2). **37.4** marks buildings, rooms, fittings and their cost code, verbs, knowledge,
senses, herds and fences' mechanism; **37.2** the rule, numbers and data rows of the wave's own.

| File | Line | Change | Owner |
|---|---|---|---|
| `engine/clocks.py` | after 67; RATES 19-40 | `capital_factor`, `capital_units`, `capital_life`, `night_life`; RATES `*.hours`, `*.uses` as `capital`; `capital` in the clocks named by `clock_of` | 37.2 |
| `engine/data.py` | new beside PHYSICS (743) | `CAPITAL` lever (§1) | 37.2 |
| `engine/data.py` | ROOMS 290-300, BLUEPRINTS 302-311 | `hours` per structure; materials in basis units (wave1 §3.5; with U0's resize); BLUEPRINTS' units read through `capital_units` | 37.4 (37.2 numbers) |
| `engine/data.py` | FITTINGS 234-285 | `hours` per fitting; the cellar by footprint; `uses` for the oven's lining, the millstones' dressing, the brine pan's boilings | 37.4 (37.2 numbers) |
| `engine/data.py` | MONUMENTS 334-346 | the weir row loses its own units and materials (fault 2) | 37.4 |
| `engine/data.py` | WATER_WORKS 376-390 | `size` by water kind; materials and hours a metre; position shares of the wings (§3) | 37.2 |
| `engine/data.py` | TIERS 391-396 | `skill` word a tier (§5.5) | 37.4 |
| `engine/data.py` | 721-724 | build techniques no longer copy `units`; a `units` lookup through `capital_units` (fault 4) | 37.4 |
| `engine/data.py` | CLEARING 222-226 | hours a plot by cover; `built` the same | 37.2 (numbers), 37.4 (holding) |
| `engine/data.py` | TECHNIQUES fence 527, wall 531; new `dead hedge` | `along` argument; the new technique | 37.4 (37.2 numbers) |
| `engine/data.py` | FENCES 963-971 | hours and materials a 100 m; `hedge` kind; `decays_every` (years) and `rots`; border length constants | 37.2 (numbers), 37.4 (mechanism) |
| `engine/data.py` | HERDS (973); LIFE 1146 | `capacity.child` 15; `children_daily: ["herd"]` | 37.2 |
| `engine/data.py` | PHYSICS 825; clocks.py:25 | remove the dead `cattle.stray` (fault 5) | 37.4 |
| `engine/data.py` | new beside SKILL (732); TECHNIQUES | `SOUND = {"trade": [1.5, 0.5], "basic": [1.0, 0.5]}`; the knowledge-only `carpentry` and `masonry` (§5.1) | 37.4 |
| `engine/buildings.py` | 261-274, 276-291, 293-308 | `room_cost`, `upgrade_cost`, `base_cost` read units through `capital_units(w)` (they take the world) | 37.4 |
| `engine/verbs.py` | 116-158 | `cost` for `build`: what is left, 1 to 2 units (§5.4); `make`'s floor in place of `int()` at 142 is U0's | 37.4 |
| `engine/verbs.py` | 869-877, 1254-1286, 1347-1375, 1377-1400 | the trade skill (§5.1); practice for every act (§5.2); `sound` accumulated (§5.3); the finish line; the tier's skill (§5.5) | 37.4 |
| `engine/verbs.py` | 992-1030, 1153-1200, 1225-1240 | the weir's first section and parts by water kind; one act mends several levels | 37.4 (reads 37.2's data) |
| `engine/verbs.py` | `_consume` calls at 967, 1015, 1073, 1108, 1127, 1336 | materials from another parcel add moving units (§8) | 37.4 |
| `engine/verbs.py` | 2257-2284 | `_clear` a plot at a time (§7) | 37.4 |
| `engine/verbs.py` | VERB `work` 19, `order` 77; `_order` 2452 | `along`; the order names a herd | 37.4 |
| `engine/farm.py` | 861-900 | `fence_need` by length, round or along; `_fence` for borders and the hedge's brush drawn in place | 37.2 (farm), 37.4 (fences' mechanism) |
| `engine/farm.py` | 922-1024, 1098-1126; 677-685 | sowing and breaking on a cleared part; a child herder's capacity | 37.2 |
| `engine/knowledge.py` | 157-161, 448; seed 85-103; `where` 171 | the craft's skill read with the technique's; practice credit to both; seeding the craft; the cover check passing a cleared part | 37.4 |
| `engine/herds.py` | 52-58, 60-89, 125-131, 152 | border odds in `through`, `target`, `wander`; borders' wear in `_fences`; the hedge's half-year decay | 37.4 |
| `engine/life.py` | 236-257 | herding daily under the order | 37.2 (D2-148's; owner to confirm) |
| `engine/night.py` | 222, 622-626 | breaks and wear x `sound` | 37.4 |
| `engine/signs.py`, `engine/layout.py` | FENCE 243-300, `fence_context` 1790; new CLEARING bundle; building words | hedge and border signs; plot cleared; soundness for those who can judge | 37.4 |
| `wild/gear.py`, `engine/wild.py` | `cost` 86-105; `water_kind` 2966 | a section's cost by its water | 37.2 |
| `engine/run.py` | 1008, 1036 | the act log of W-82 (each act with its units and result), for bot interface tests and live readings (fault 3) | 37.4 |
| prompt and knowledge cards | (D2-263's recipes shown) | a work's units shown at the world's factor | 37.4 |

## Tests

**Unit tests** (new `tests/test_cybertron2_capital.py`, and additions to the buildings, water and livestock tests):
- `capital_factor` is 1/7.03 for a 32-day world with PHYSICS units, 1/15 when set; a world spec's `capital_factor` wins.
- `capital_units`: a held class returns today's units; a released row `hours x f / 2`, floored at 1; `capital_life` keeps the cost a use
  equal at 1/15 and 1/7.
- Every capital row names `hours` and its clock (the clocks test fails on a row without).
- The units shown for a build technique equal `capital_units` at the world's factor after the lever changes (fault 4).
- A build act on a work with 0.6 units left costs 1 unit; a bed costs 1; a 2-unit act on a 12-unit room at skill 1.0 leaves 10.
- Practice: ten acts on a timber smokehouse raise the builder's `carpentry` by the curve for 20 units of practice; a hall then uses
  that skill; a seeded carpenter starts with `carpentry`.
- Soundness: a room built by a master wears at half a novice's chance, seeded at 1.0; the finish line matches its band.
- A fine tier refused to a novice; a competent builder begins it; a novice's act on it puts in half.
- The weir's first section on a beck, a lowland and a large river costs §3's units at 1/15 and 1/7; MONUMENTS carries no weir cost;
  one mending act mends as many levels as it covers.
- Fences: a size-1 round is 566 m; a border between a 6- and an 18-plot parcel 345 m; a herd's step across a shut border is taken at its
  odds; a dead hedge is refused with no brush near, draws brush in place, loses a level a half year unmended.
- Children: a child ordered to herd herds every day at the high dial; a herd of 20 with one child herder can split (capacity 15).
- Clearing: on a 3-plot scrub parcel the first plot's work makes `plots: 1`, the clearer holds 1 plot, sowing on it takes no turf
  penalty and is refused beyond it, the scrub's stocks fall by a third, the last plot makes it a field with the shares intact.
- Materials from another parcel's store add moving units at the provisional rate.

**Bot interface run** (D2-298: interfaces and basic functioning only): W-82's building layer and farming policy (`bots_build.py` on the
branch) kept as a test tool, not as evidence (W-82's question 5, option a, read under D2-298): at each stage, every work in §2 can be
begun, carried on by a second person, finished, mended, and its units read back from the act log; a dead hedge, a border fence and a
plot cleared work end to end; nothing starves the bots that did not before for a reason other than the price.

**What live runs should read** (scenario_design.md §6), each against its null arm with a qualitative end-state reading:
- whether people begin and finish houses, a field's first plot, a hedge or a fence, the weir; how many begun works are left;
- the share of work in building against the null arm, and food at the end;
- who holds the weir, the cleared ground, the wood, the builder's skill; whether builders are asked or paid to build;
- whether children are set to herd, and whether crops are trampled;
- whether straw for thatch binds (§2.3);
- K8: how many households form and whether each is housed.

## Basis rows needed

| Row | Value | Mark |
|---|---|---|
| A real working year | about 2,700 hours | decided in D2-276's text ("about 384 engine hours a year against about 2,700 real") |
| The capital factor "world" | units a year x 2 hours / 2,700 (1/7.03 at 32 days and 7, 6, 5, 6 units) | decided: D2-276 ("worked out from each world's own numbers"); the stage 1/15: D2-281 |
| The hold | existing works at today's units until stage 5 | default (question 2) |
| A plot (a unit of size) | about 2 ha, about 141 m a side; a round 566 m x √size | default (02z basis; the audit) |
| A shared border | 141 m x √(the smaller parcel's size) | default (est.) |
| The weir's water | beck 3 to 6 m wide, wattle 1.0 m; lowland 10 to 20 m, 1.5 m; large 30 to 60 m, 2.3 m, current x1.5 | default (est.) |
| Wattle in place | about 2.1 hours, 1.2 withies and 0.7 timber a metre at 1.5 m high | default (withies_wood_materials.md, est.) |
| Getting rates for building materials | fell 4 timber a unit (crude tool), quarry 4 stone, cut withies 4 (bed) and 1.5 (wild), brush 5 bundles | default (wave1 §3.1; U3's and U0's) |
| Brush | a 10 kg bundle, firewood's unit | default |
| In-place materials | brush for a dead hedge, field stone for a wall, daub and puddled clay: got as part of the work, at the factor | default taken, open (question 1) |
| Soundness | a trade 1.5 to 0.5, basic 1.0 to 0.5 | default |
| A child herder | about 15 head | default (est.) |
| Herding | 1 unit a day a herd (D2-128), against a real day's watching | as built; named departure (question 9) |

## Gaps

| Gap | Where it stands |
|---|---|
| G7 builders as a trade | designed minimal (§5); the raising, framing needing a builder, seasoning and boards wait on W-76 |
| G8 cheaper crop protection | designed (§6): children daily, the dead hedge, fences by length and along a border; folds designed and recommended deferred to sheep (L-36) |
| G9 clearing a plot at a time | designed (§7) |
| G13, E12 a bot that builds | exists on the W-82 branch; kept as an interface test tool (Tests), not as evidence (D2-298) |
| K7 the staging's direction | designed: one lever, a hold on existing works (§1, §4); question 2 |
| S13 companions on deferred work | the companions are designed here at the size stage 5 needs; W-76 and L-36 take them further |
| The weir's size | designed by water kind (§3) |
| Material-heavy works under real materials | found here (§2.3); question 1 |
| Thatch's straw | found here (§2.3); question 10; a gate check for U11 |
| Q-30 (livestock.md's fence upkeep says a season) | 37.2's to bring in line with D4-114 when FENCES is rewritten |
| Building practice credited once | found here (Departure 5); fixed in §5.2 |
| Moving fallen fences' and hedges' parts, frost on digging, rest days (L-157) | deferred: frost with the environment work; rest days with health (L-157) |

## Open questions for Zach

Ranked by what they block. Each stands alone.

1. **Whether material got at the site is part of the work** (D2-276; wave1 question 6; new). D2-276 keeps materials real in quantity and
   rate while the making is compressed, so a work whose mass is great costs several times its real share of a year: a small stone room
   is 45 to 90 units of building at 1/7 and about 410 of quarrying (two world years of one adult), a 100 m dry-stone wall 1,000 to
   2,000 of quarrying, and a dead hedge's brush about 30 units a 100 m if it is cut as firewood is. Real walls and hedges used stone and
   brush from beside them, field stone above all. **Options:** (a) as decided: every material at real rates; stone houses and walls
   become rare lumps for villages and lords; (b) material got at or beside the site in the course of the work (field stone for a wall,
   brush for a dead hedge, daub, puddled clay, turf) is part of the work's hours at the factor, while goods brought (felled timber,
   quarried stone, withies, straw) stay real; (c) a named factor on the quantity of bulk building materials. **Recommend (b):** it is how
   wave1 already treats daub, it keeps every traded good real, and it lets the dead hedge be the cheap protection D2-276 asks for.
   **Blocks:** the dead hedge's cost, walls, stone rooms, and whether stage 5b's houses are buildable.

2. **How the capital factor is staged, and whether gear moves with the works** (D2-281; W-82 question 1; wave_conflicts question 7; new).
   **Options:** (a) all capital to 1/15 at once at stage 1, then to about 1/7; (b) the lever at 1/15 from stage 1 for gear and new works
   (racks, smoke huts, pits, containers), the existing works held at today's units until their companions are in (stage 5), then rooms,
   fittings and the weir to 1/15, then fences and clearing, then about 1/7 after a live run; (c) gear at 1/7 from the start and works
   staged (building_clock.md as written). **Recommend (b):** no class gets its own factor, gear is never dearer per real hour than a
   house once the hold ends, and the works that break without their companions (fences, scrub fields) wait for them. **Blocks:** U3's
   prices, the stage plan, W-82's reading.

3. **What size the weir is priced at** (D2-262, D2-210; W-82 question 3). **Options:** (a) the research size everywhere (a lowland one:
   1 to 2 units at 1/15); (b) a large river's size everywhere (W-82's switch: about today's price at 1/7); (c) by the water it stands
   in: a beck at the floor, a lowland river 1 to 2 units at 1/15 and 2 to 4 at 1/7, a large river 4 to 8 and 9 to 17 (§3). **Recommend
   (c):** it is the weir sized to its take, and its leverage then comes from the site, the right, the crew, the withies and the keeping,
   as real weirs' did. **Blocks:** the weir's repricing and its upkeep.

4. **Whether a builder's skill sets how sound a building is, and whether finer finishes need skill** (building_clock.md question 4; timber
   scouting question 11). **Options:** (a) soundness from skill only (a master's building wears at half a novice's); (b) soundness, and
   fine, rich and grand finishes begun only by a builder at competent, skilled and master; (c) neither now, all in W-76. **Recommend (b),
   kept minimal:** it is "can build sturdier or better houses if more skilled" with the least new machinery, and W-76 adds the raising
   and framing. **Blocks:** stage 5a's builders.

5. **Which cheaper crop protections come first** (building_clock.md question 5; W-82 question 2). **Options:** (a) herding by children
   every day (the order exists); (b) the dead hedge; (c) fences priced by length and along one border; (d) moved folds of hurdles.
   **Recommend (a), (b) and (c) together, and (d) deferred to sheep (L-36):** at the engine's day resolution a fold of cattle costs what
   herding costs. **Blocks:** stage 5b's fences.

6. **Whether fences along one border come in now** (L-24, flagged for later; 37.4's mechanism). They are the fence priced by length: the
   crop's side fenced instead of the pasture round, a quarter of the length or less. **Options:** (a) now, with the companions; (b)
   later with L-24's hedges and wolves. **Recommend (a).** **Blocks:** 6.3.

7. **Whether a cleared plot becomes a field part of its parcel** (L-153). **Options:** (a) the parcel keeps its cover and holds `n` cleared
   plots that can be broken and sown, claimed by plots as fields in shares are (§7); (b) split the parcel in the graph (clearing.md's
   alternative); (c) keep clearing whole. **Recommend (a):** no change to the graph, and the shares machinery already holds part of a
   parcel. **Blocks:** stage 5b's clearing.

8. **Whether a build act may cost less than 2 units when less work is left** (W-82 question 4). **Options:** (a) keep the flat 2; (b) an
   act costs what is left, 1 or 2 units; (c) small fittings in batches only. **Recommend (b), with beds and stalls keeping `qty`.**
   **Blocks:** the 1-unit floor for every fitting and small work.

9. **Whether herding stays 1 unit a day** (D2-128; new). A real herder watched all day (about 5 units); the engine's 1 unit is what a
   fence must beat, and at it no fence round a pasture ever pays. **Options:** (a) keep 1 unit, named; (b) raise it toward real.
   **Recommend (a)** with children herding daily: open fields were the real pattern, and a dearer herd day would push every household to
   fences it cannot afford. **Blocks:** nothing now; the reading of fences in live runs.

10. **Whether thatch's straw is a binding limit** (building_clock.md question 6; new). A small room's roof is 75 trusses (1.2 t), about
    16 plots' straw at reaping's 4.7 a plot. **Options:** (a) as real: thatch binds and straw becomes a good worth holding; (b) other roofs
    got in place (reed from a reed bed, turf, heather) as wattle's alternatives; (c) a named factor on thatch. **Recommend (a) with a gate
    check in each world** (U11), and (b) for reeds when the fen comes (L-125). **Blocks:** whether houses get built at stage 5b.

11. **The short live run D2-281 asks for: which world and when** (W-82 question 7). **Recommend:** after stage 5a, the farm world with a
    newcomer household (W-82's Brookend arm) at 1/15 against its null arm, then the remade founding world (U11). It costs money.

## Sources

- Decisions: D2-36 to D2-40, D2-52, D2-66, D2-128, D2-130, D2-132, D2-148, D2-154, D2-155, D2-156, D2-166, D2-168, D2-171, D2-172,
  D2-209, D2-210, D2-259, D2-262, D2-264, D2-269, D2-271, D2-273 to D2-276, D2-279, D2-281, D2-284, D2-288, D2-291, D2-293, D2-297,
  D2-298, D4-60, D4-114; records L-11, L-24, L-36, L-119, L-120, L-153, L-157, Q-30, Q-74, Q-75, W-76, W-82.
- Proposals and spec: proposals/building_clock.md, clearing.md, fences.md, hunt_fish_materials.md §6, hiring.md; spec/core/clocks.md,
  spec/economy/buildings.md, spec/economy/livestock.md; proposals/w73_design/README.md, basis.md; docs/cybertron2/guides/senses.md;
  docs/scenario_design.md.
- Notes: docs/review/37_growth/02zzzh_hunt_fish/wave1_physical_basis.md §3, §4, §5; building_clock.md; building_clock_bots.md; wave_conflicts.md
  (K7, K8, S4, S13, C3, C31, E12, G7 to G9, G13, question 7); withies_wood_materials.md; catch_basis.md §2; household_skills.md
  (addendum); docs/review/37_growth/02zzzi_timber/scouting.md (§1.7, §2, T4, questions 11 to 13).
- Code on main (66b61bd2): `engine/data.py` (CLEARING 222, FITTINGS 234, ROOMS 290, BLUEPRINTS 302, MONUMENTS 334, WATER_WORKS 376,
  TIERS 391, build techniques 721, SKILL 732, PHYSICS 743, FENCES 963, HERDS 973, LIFE 1142-1146), `engine/clocks.py`,
  `engine/buildings.py` (room_cost 261), `engine/verbs.py` (cost 116, _build 899, _monument 992, _weir_part 1153, _build_work 1377,
  _fitting 1288, _clear 2257, _order 2452), `engine/farm.py` (herd 785, fence_need 861, _sow 922, _break 1098), `engine/herds.py`,
  `engine/knowledge.py` (skill 157, tried 448), `engine/life.py` (children_work 236), `engine/night.py` (breaks 222, _wear_night 593),
  `engine/wild.py` (water_kind 2966), `wild/gear.py` (cost 86); branch `w82-clock-bots` (10a88532): `engine/capital_clock.py`,
  `engine/bots_build.py`.

## History

- **23 Nov 2026:** written by a 37.2 design subagent for W-85 from the sources above; the cost tables re-derived on basis units, the
  weir sized by its water, the three companions designed, the materials and thatch findings added.

*Current as of 23 Nov 2026: D2-263 to D2-300 (D2-299 and D2-300 touch nothing here).*
