# The water fixes: the weir by position and material, gear sharing a run, the wear calibrated (W-69, 20 Nov)

37.2, 20 Nov 2026, W-69, branch `w69-water-fixes` (on main `49d6d49c`, the food values merged). Built at Zach's request (20 Nov:
"after the water fixed"), after the bot runs on the food values (02zzu_lookup.md, "Applied") found the traps taking a run before
the weir, floods wrecking the weir, and the spates sweeping the traps. The rules changed are written up in
`proposals/river_and_water.md`, History (20 Nov). No decision is added; every value calibrates.

## 1. A weir's sections: position decides share and hold, material wear and cost

The code: `cybertron2/wild/gear.py` (one unit, D2-244), called by `engine/wild.py` (`sections`, `weir_share`, `weir_hold`,
`_weir_wear`) and `engine/verbs.py` (`_monument`, `_weir_part`, `_weir_mend`, `_upgrade`). The data: `WATER_WORKS["weir"]`,
`position`, `material` and `footing`.

| | Share of a run | Hold a night | Wear | Cost |
|---|---|---|---|---|
| the first section (index 0) | 0.30 | 100 kg | its material's | its material's + the weir's stakes and trap (6 timber, 8 units) |
| each added section, up to three | 0.07 | 70 kg | its material's | its material's |
| wattle | | | 1.0 | 6 timber, 16 units |
| timber | | | 0.5 | 10 timber, 25 units |
| a stone footing under a section | | | 0.1 | 10 stone, 15 units more |

- A wattle first section costs 12 timber and 24 units, as built (the MONUMENTS row). A timber added section costs 10 and 25, as
  before. A timber first section costs 16 and 33. A wattle added section costs 6 and 16.
  A level's mend (0.06 of the build, at least one of each material) stays at 1 timber and under 2 units for any section, so
  one mending act at skill 1 still mends a level (17 and 34 for the timber first section had put it just over: 2 timber).
- **Upgrading** a wattle section to timber pays the difference: 4 timber and 9 units. Its level is kept, so an upgrade is not a
  cheap mend.
- **Built by:**
  - `build weir` with `"structure": "timber"` (the first section in timber);
  - `build wattle section` or `timber section` (`weir section` is timber unless `structure` says wattle);
  - `build section upgrade`, or `upgrade` the weir `to timber`.
- **Old worlds load the same.** A list of sections as before (the first wattle, the others timber) keeps its share, hold and
  wear, and a list of the material names alone loads as sound sections at the building's level.
- **Default taken (for Zach):** splitting the first section's cost into a base (the stakes across and the trap) and the
  material. Read literally, "wattle at today's wattle cost" (12 timber) and "timber at 10 timber" would make timber the cheaper
  section, which is Zach's question the other way round.

## 2. Gear in one parcel shares a run; between parcels, in turn

**Before:** a set trap took its heads from the run in `_set_night`, one at a time, before the weir took its share of what was
left. In the high arm the traps took 481 food and the weir 43.

**Now:** the run at a village's stretch is shared in the river's night (`gear.share_run`, from `wild._runs_night`).
- **Within a parcel** the gear share the run passing at the same time: the weirs, a trap in a shut mill's race, and the set traps.
  Each takes its share of what reaches the parcel:
  - a weir's share is `weir_share`, the race's is `race`;
  - a set trap's is the heads it met of the run that night, against the run as it arrived. `_set_night` keeps these draws and the
    trap's room for them, and takes no heads.

  When the shares pass the whole run they are scaled down together. Each gear is capped by its own hold, and a full hold does
  not cut the others.
- **Between parcels** a run going down (the eels) meets the upstream gear first, and a run going up (salmon, lampreys) meets the
  downstream gear first. Before, the weirs took upstream first for every run.

**Tests:** proportional sharing, independent of the order the gear is listed; a full hold; down and up between parcels; and on
the river world, a weir beside nine traps still takes its 30% (60 of 200 eels).

## 3. The wear calibrated to D2-210's year

D2-210 asks for wattle at about 40 to 50% of its cost a year to keep, timber 20 to 25%, stone-footed 5 to 10%, and a full weir
(wattle and three timber) a quarter to a third.

**The measure:** the expected levels lost a night are E[min(Poisson(λ), 5)], from each night's flow, frost and gap. These are
taken from the world's own weather over 8 compressed years, times `mend` (0.06 of the section's build a level).
- **The gap kept right:** open in high water and above, shut otherwise. The bots also shut it on a run night in high water.
- **The river:** Eelmouth's large river has about 12 low, 9 normal, 4 high, 4 spate and 3 flood nights a year, and about 6 frozen
  ones.

| Factor | Before | After |
|---|---|---|
| flow: low, normal, high, spate, flood | 0.5, 1, 2, 5, 15 | 0.5, 1, 1.5, 2.5, 5 |
| the gap shut in high water | x1.5 | x2 |
| ice, the thaw | x3, x5 | x1.5, x2 |
| a large river (lowland 1, beck 2 kept) | x1.5 | x1.2 |
| base (a level a week of normal flow, lowland wattle) | 0.143 | 0.143 (kept) |

| Upkeep, share of the build a year | Before | After | D2-210 |
|---|---|---|---|
| wattle (Eelmouth, gap right) | 1.27 | 0.50 | 0.40 to 0.50 |
| timber | 0.67 | 0.25 | 0.20 to 0.25 |
| stone-footed | 0.14 | 0.05 | 0.05 to 0.10 |
| a full weir, gap right | 0.82 | 0.31 | 0.25 to 0.33 |
| a full weir, gap shut in high water all year | 1.09 | 0.51 | clearly more |
| the river world's Saltwell (lowland): wattle / full | 1.18 / 0.75 | 0.46 / 0.29 | |

| A night, a wattle section on the large river: levels lost | Before, open / shut | After, open / shut |
|---|---|---|
| spate | 1.07 / 1.60 | 0.43 / 0.86 |
| flood | 3.04 / 4.04 (taken whole about half the time) | 0.86 / 1.71 (taken whole about 4% shut) |

**In the high arm's bot run** the all-timber weir lost 26 to 27 levels over 54 days, in 18 to 19 nights of wear. That is about
0.31 of a timber section's build a year, a little over the band in a run with more floods than the mean (9 flood nights in 54,
against about 5 expected). It was never down: its best section stayed sound or worn.

**Not met (for Zach):** §3b.6's per-night targets cannot hold with D2-210's year on a river with about 4 spates and 3 floods a
compressed year. Those targets were a spate night one or two levels, and a flood with the gap shut usually the whole section.
The year's band was taken.

## 4. Spates, otters and fires (reported, not tuned)

- **Spates and traps.** A trap emptied in the morning loses nothing to the spate. Of the 240 to 410 kg swept in a run, 97 to 100%
  was caught that same night: low 240 of 240 kg, high 400 of 410 kg. A trap lifted before the spate, or sprung, is not swept.
  - The loss is large because the runs' set nights fall on flood nights in this world's first autumn: days 6, 7, 9 and 10 are
    floods and day 8 a spate. The bots set their traps whatever the river, so 40 to 46% of the trap catch was on spate or flood
    nights.
  - The rate a night (0.5 in a spate, 0.85 in a flood) is D2-218's. A trap's catch is one night's, and losing it with the trap
    in a flood is plausible. Not tuned.
  - What is off is how often the flow class reads spate or flood: 17 of 54 nights in this run, about 6 of 32 a year in the mean.
    That waits on the river's level (D2-215, 37.4).
- **Otters** took 81 to 163 kg, about a fifth of the trap catch (14 to 25%), as before.
- **Fires.** The maker puts the smoke racks in the houses on the Street, so a fire spreads to the houses beside it and burns their
  stores. On day 9 in the high arm, Marsh House, Brook House and the Brook Byre burned together. Lost to fire: 79 food in medium,
  and 253 to 283 food in high. In high the fires came on days 9 and 46, with one more on day 17 in the run with `weir_traps`; each spread to two or three
  houses, and the worst took the winter's store.
  - Brief 5 §4a puts a smokehouse apart, on another parcel. The maker does not. For Zach.

## 5. The bots

One change, in `bots_livelihood.py`, knob `weir_traps` (2):
- each fisher of the weir's household keeps 2 traps, and its keeper none.

The reason: with 8 traps a fisher, the weir's household spent whole days lifting traps. A lift is one act for a kg or two, so on
days 41 to 44 every member did 4 to 6 lifts and the keeper had no units left to salt, while 126 kg of fish spoilt in that house
with salt in store. The weir now takes its share whatever the traps beside it, and its lift is one act for its whole catch.

The gap rule was kept: shut when a run is at the water, else open in high water and outside the windows.

## 6. The bot runs

`python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_<arm>.yaml --bots runs --days 64`, on the regenerated arms:
seed 5, 12 people, a larder of 8 days (104.5 food). The high arm's weir has three timber sections and its crew (Nichola, Peter).

How to read the table:
- Food is fish food, at 0.46 a kg.
- "Fed per fisher" is fish food a unit of fishing work times 7 units (a full-time adult's day), over 1.1 food a person a day. It is
  given on the catch and on the fish eaten.
- Fishing work counts every act of it: setting and lifting traps, nets, the gap, mending, the racks, salting and boiling salt.
- The two "no fires" runs are diagnostics: the smokehouse fire chance set to 0 in the process, the world and code as committed.
- The runs and their analysis are this session's (scratchpad), not kept in the repository.

| Arm | Catch by gear, food | Weir and trap heads | Kept made, kg: smoked / dried / salted | Fresh fish eaten / spoilt, kg | Lost: swept, kg / otters, kg / fire, food | Store at winter's start, food (alive) | First missed meal | Deaths (last) | Food a unit | Fed per fisher: caught / eaten |
|---|---|---|---|---|---|---|---|---|---|---|
| low | traps 341 | traps: eel 1,217, lamprey 17 | 0 / 50 / 0 | 297 / 11 | 240 / 92 / 0 | day 13: 101 (11) | 24 | all 12 (36) | 0.52 | 3.3 / 1.8 |
| medium | traps 385, nets 10 | traps: eel 1,389, lamprey 7 | 58 / 3 / 0 | 177 / 8 | 316 / 96 / 79 | day 13: 42 (10); day 45: 47 (2) | 9 | all 12 (54) | 0.63 | 4.0 / 1.2 |
| high, 8 traps a fisher (the policy before) | traps 655, weir 437, nets 9 | weir: eel 572, salmon 202; traps: eel 2,372 | 189 / 0 / 100 | 459 / 318 | 410 / 163 / 253 | day 13: 177 (10); day 45: 154 (7) | 9 | all 12 (53) | 0.95 | 6.1 / 2.2 |
| high, `weir_traps` 2 (the policy now) | traps 363, weir 408, nets 9 | weir: eel 557, salmon 184; traps: eel 1,308 | 153 / 3 / 80 | 337 / 135 | 248 / 111 / 283 | day 13: 192 (11); day 45: 49 (2) | 9 | all 12 (53) | 1.16 | 7.4 / 2.5 |
| medium, no fires (diagnostic) | traps 365, nets 9 | traps: eel 1,292 | 109 / 4 / 0 | 199 / 2 | 301 / 81 / 0 | day 13: 102 (11) | 23 | all 12 (36) | 0.53 | 3.4 / 1.8 |
| high, `weir_traps` 2, no fires (diagnostic) | traps 370, weir 825, nets 16 | weir: eel 1,244, salmon 350; traps: eel 1,301 | 307 / 3 / 232 | 449 / 901 | 270 / 141 / 0 | day 13: 310 (11); day 45: 297 (5) | 29 | 7; 5 alive at day 64, 120 food left | 1.40 | 8.9 / 3.3 |

**Against the previous figures** (02zzu_lookup.md "Applied", the larder at 104.6 food):

| Arm | Weir food | Trap food | Kept | Swept / otters | Food a unit | Deaths |
|---|---|---|---|---|---|---|
| low, before | none | 363 | 47 dried | 219 / 86 | 0.56 | all by day 34 |
| low, now | none | 341 | 50 dried | 240 / 92 | 0.52 | all by day 36 |
| medium, before | none | 431 | 70 smoked | 302 / 85 | 0.72 | all by day 54 |
| medium, now | none | 385 | 58 smoked | 316 / 96 | 0.63 | all by day 54 |
| high, before | 43 | 481 | 98 | 339 / 97 | 0.84 | all by day 56 |
| high, now | 408 to 437 (10 times) | 363 to 655 | 236 to 289 | 248 to 410 / 111 to 163 | 0.95 to 1.16 | all by day 53, or 5 alive with no fires |

### What binds

- **Medium starves, by the length of the gap between the autumn runs.** It is about 24 days, days 13 to 36, with only the
  spring's lampreys between them, at about 13 food a day for the village.
  - Medium's keeping is three houses' smoke racks: 58 kg smoked with a fire, 109 kg without. Medium has no salt.
  - It reaches the first winter with 42 food (102 with no fires) against the gap's need of about 300, and every arm dies at the
    end of winter or in spring (days 20 to 36).
  - Fresh fish is not what is short: medium spoilt only 2 to 8 kg. The catch is eaten fresh over the glut, at up to twice a ration
    a person, and lost to the river.
  - The traps' 300 kg swept is more fish than was eaten fresh (177 to 199 kg).
  - Medium cannot keep enough of a run to carry the gap. It needs more keeping capacity, salt, or fewer losses to the river. On
    this world the bots alone do not make medium survivable.
- **High has no surplus as it stands, because of the fires.** The smoke racks in houses that stand together burn the winter's
  store: 253 to 283 food in two or three fires.
  - With no fires (the diagnostic), high reaches both winters with 297 to 310 food and ends with 5 alive and 120 food. The fed
    per fisher is 8.9 on the catch, inside the target of 6 to 15 (3.3 on the fish eaten).
  - It still loses 7 people in the spring gap (days 33 to 38). The store sits in the weir's household, and the bots do not share
    food between households.
- **Salting binds in the high arm** (salting kept at 4 kg a unit, Q-73):
  - **In the runs as committed:** 80 to 100 kg salted against 135 to 318 kg of fresh fish spoilt.
    - In the first autumn the salt ran out on the glut nights: 0 salt on day 12, when 61 kg spoilt, and on day 21, when 37 kg
      spoilt that night and 27 the next.
    - In the second autumn 126 kg spoilt in Marsh House with salt in store, because the keeper had no units left after the
      lifts. The `weir_traps` change is for this.
  - **With no fires:** 232 kg salted against 901 kg spoilt. Salting all of it at 4 kg a unit would take about 225 more units of
    the keeper's work and 225 salt (about 56 boils).
  - Salt and salting work, together with the racks, are what stands between the weir's catch and a winter.
- **The weir now pays.** It takes 408 to 825 food in two autumns (eels and salmon), against 43 before. It is the high arm's main
  gear, at a lift a day.

*Current as of 20 Nov 2026.*
