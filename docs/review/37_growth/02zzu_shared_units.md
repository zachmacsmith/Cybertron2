# 02zzu: shared units for food, weight and work: the analysis for 37.4's proposal

37.2, 20 Nov 2026 (WORK W-64). The brief is 37.4's [proposals/shared_units.md](../../cybertron2/proposals/shared_units.md),
"The analysis asked of 37.2", in six parts. Zach (20 Nov): "Before running these we want to do the nutrition aims that was
brought up earlier, e.g fixing eels others". It is a prerequisite for the nutrition worlds
([proposals/subsistence_worlds.md](../../cybertron2/proposals/subsistence_worlds.md), D2-242, D2-257).

**Code read:** the read-only worktree `/home/user/c2-units` (branch runs-models, `b3013b98`): `engine/data.py` (ITEMS, TECHNIQUES,
WATER_WORKS, PHYSICS, LIFE), `wild/kinds.py` (KINDS, TAKEN, RUNS), `wild/methods.py`, `wild/plants.py`, `wild/runs.py`,
`engine/wild.py` (forage, the weir's night), `engine/yields.py`, `cybertron2/capacity/`.

**Files:** the script [02zzu_shared_units.py](02zzu_shared_units.py) (the table, the conversions, the checks, the run harness and
the capacity runs); the machine-readable table and every result in [02zzu_shared_units.json](02zzu_shared_units.json) (`table`:
goods, animals, methods with sources; `runs`: the recorded run pulses and the weir; `capacity`: the worlds before and after).
Nothing in either checkout was changed; no agents or models were run. The engine was only stepped with no one acting (the runs)
and the capacity model run with the values patched in memory.

**The basis is not decided** (OPEN Q-69). Everything is worked in kcal and hours and converted at the end, with the brief's
defaults: **one food = 2,500 kcal, a unit of work = 2 hours**, children 0.6, elders 0.8. Part 7 shows 2,000 and 3,000 kcal and
1.5 hours.

**What is measured and what is inferred:** the engine's numbers (its tables, the run pulses, the capacity model) are measured
here. The real values are from standard tables and the literature, as recalled; only the eel's energy was looked up this session
(USDA FDC 174193, 184 kcal a 100 g). Each row in the JSON says which: `checked`, `standard` (a standard table's value, to be
checked against it when the data change is written), or `estimate` (no table; a reasoned range). The return rates by method are
the weakest part: ranges from the hunter-gatherer and agricultural-history literature, wide on purpose.

## Summary

**The premise is half right.** Most plant foods are several times too rich a kilogram, milk twice, meat and fish two to two and
a half times a unit. But **the eel is not a fifth of its real value.** At the engine's own eel (0.5 kg) it is 0.27 food on the
basis against 0.2 now, and a run's real mean eel (0.2 to 0.4 kg, where males are many) is 0.1 to 0.2. The salmon is over: 1.4 food
on the basis against 2.0. The proposal's fifth came from reading a kilogram of whole fish as a day's food. It is about half a
day's food for an eel (184 kcal a 100 g of flesh, 0.72 of it eaten), and about a third of a day's for river fish.

**So fixing the eel and salmon values does not make the weir pay at a middle station** (Middleham 0.37 food a unit of weir work
now, 0.48 after; a unit pays at about 0.36 for a household). What decides it is **the runs' size and where the salmon go**:
- the engine's runs are 2.5 to 7 times below a real river's, scaled to the engine's year by catchment;
- the salmon hardly reach above the lowest station (0.5 a year at Middleham), because they spawn only in head waters.

With the run sizes of a real river, a one-section weir pays at every station: 1.4 to 3.9 food a unit at the upper and middle
stations (2.8 to 3.9 at Middleham), 3.6 to 4.6 at the lowest. At the lowest station it is bounded by D2-210's nightly hold, which is then what keeps the
weir within its targets (part 6).

**The largest corrections** (food a unit or a head, now and on the basis at 2,500 kcal; the factor is basis over now):

| # | Good, kind or method | Now | On the basis | Factor | What it does |
|---|---|---|---|---|---|
| 1 | watercress (a kg) | 0.4 | 0.04 | 0.09 | 11 kcal a 100 g: water |
| 2 | samphire (a kg) | 0.5 | 0.075 | 0.15 | |
| 3 | greens, mushrooms (a kg) | 0.6 | 0.11 | 0.19 | spring gathering falls from 0.28-0.77 a unit to 0.06-0.17 |
| 4 | lamprey (a head) | 0.45 | 0.10 | 0.21 | the engine gives it 0.3 meat, as if 0.3 kg of venison |
| 5 | berries (a kg) | 0.8 | 0.17 | 0.21 | |
| 6 | hens' eggs (a hen's day) | 0.10 | 0.0075 | 0.08 | laying is still on the old compressed-day clock (node_ecology.md) |
| 7 | a slaughtered young beast (a head) | 15 | 31 | 2.0 | the herd's calves feed twice what they do now |
| 8 | an ox, a cow (a head) | 75, 60 | 126, 91 | 1.7, 1.5 | the cow was a quarter of its weight in meat units |
| 9 | meat, fish (a unit) | 1.5, 1.0 | 0.6, 0.46 | 0.40, 0.46 | offset by more units a kill: wild game 0.66 to 1.0 a head |
| 10 | milk (a kg) | 0.5 | 0.26 | 0.51 | with the yield at about 3 kg a cow a day, a cow's food is unchanged |
| 11 | acorn meal (a unit) | 1.0 | 1.48 | 1.48 | leached acorns are a rich food (about 5,000 kcal a kg dried) |
| 12 | hazel nuts (a kg in shell) | 1.6 | 1.08 | 0.68 | the kernel is 0.43 of the nut |
| 13 | salmon (a head) | 2.0 | 1.41 | 0.70 | |
| 14 | eel (a head of 0.5 kg) | 0.2 | 0.27 | 1.32 | 0.1 to 0.2 at a run's mean size |

**What barely moves:** the grain ladder. Bread at 1.3 is already the grain's whole energy at 2,500 kcal (1.33), and boiled whole
grain at 0.7 is the ladder's deliberate penalty (0.54 of the full value, D2-60, D4-107). The engine's grain values amount to a
food of about 2,550 kcal. Farming's food a unit of work moves by 2%, and at 1.4 to 2.9 it sits at or a little under the medieval
range (1.2 to 6 a unit).

**Where the order changes:**
1. **Greens and berries against grain:** now about level a kilogram (0.6 and 0.8 against 0.7); on the basis a sixth and a quarter.
2. **The master hunter against the ploughman:** now 2.5 against 2.35, the hunter ahead; on the basis 1.9 against 2.4, the hunter
   behind (still inside the real range of 1.2 to 3.2). This runs against D2-255's "a very skilled hunter brings in a
   disproportionate amount", and is for Zach (part 4).
3. **Milking against farming:** now 2.4 against 1.8, milking ahead; on the basis 1.2 and behind. With a real milking rate (about
   six cows a unit, 3 kg each) it is 4.6 and ahead again.
4. **Autumn gathering against the capable hunter:** now 1.1 to 1.7 against 0.7; on the basis 0.55 to 0.9 against 0.5, about
   level.
5. **Acorns against grain:** acorn meal goes above flour (1.48 against 1.02), and leaching becomes one of the best units of work
   (2.8 a unit). Realistic: acorn bread was Europe's famine food.
6. **The weir against fishing by hand at Middleham:** now 0.37 against 0.6, behind; on the basis 0.48 against 0.28, ahead, but
   only because hand fishing falls. It still loses to farming and gathering.
7. **Unchanged:** farming over gathering, a master over a novice, autumn over winter, the mill ladder.

**What the worlds need under the new numbers** (part 5): the recommended values lower the wild and dairy food and raise the
slaughtered beasts'. Measured with the capacity model on seven worlds (part 5):
- **Farming worlds hold.** Fields gain 2 to 3%, herds lose 3 to 4%. With the needs on the basis, people supported rise 15 to 20%.
- **Fishing worlds lose about half their fish food:** the lake from 1.46 to 1.11 of its people, w1 from 0.69 to 0.52, the fishing
  probe from 0.74 to 0.40. They need about 2.2 times the resident fish (kilograms a unit of size), or fewer people.
- **Wild plants and the legacy hunt fall to about 0.4.** The legacy hunt's kill needs its units raised about 2.5 times.
- **The runs world** needs its runs 3 to 6 times larger, its salmon spread up the river, the weir's hold in kilograms and fewer,
  denser run nights (part 6).

## 1. The table

The full table, with every source, is in the JSON (`table.goods`, `table.animals`, `table.methods`, `table.sources`). The basis
of each unit:
- **A plant good, a grain, milk, cheese, eggs:** 1 kg as gathered or kept (in shell, in husk, unleached, threshed).
- **The grain ladder's goods:** grain-equivalents. 1 grain makes 1 meal or flour and 1 bread, as the engine's techniques have it,
  so flour and bread carry the grain's energy, not their own weight's.
- **Meat and fish:** a *kcal-standard kilogram* of what is eaten. Meat is 1,500 kcal a unit, fish 1,150. Each kill's food is then
  exact by kind, and the weight is within about a quarter of the real: a unit is 1.25 kg of venison or 0.6 kg of fat beef. One good
  with one value cannot be both exact in weight and exact in food for lean and fat meats. The alternative is a good per kind
  (venison, pork, beef, eel), which gives more rows and no better play.

**Food goods** (kcal a 100 g edible; the edible share of a unit; now, the physical value, the design factor kept, the
recommendation; all at 2,500 kcal):

| Good | Unit | kcal/100 g (range) | Edible | Now | Physical | Design | Rec. | Source | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| grain | 1 kg threshed grain | 340 (327-389) | 0.92 | 0.7 | 1.25 | 0.54 of bread's | 0.72 | USDA 20004, 20072, 20038 | standard |
| rye | 1 kg | 338 | 1.0 | 0.7 | 1.35 | as grain | 0.72 | USDA 20062 | standard |
| beans | 1 kg dried peas or beans | 341 | 1.0 | 0.6 | 1.36 | 0.53 | 0.72 | USDA 16052, 16085 | standard |
| meal, flour | a grain's worth | 340-350 | 0.97-1.0 | 1.0 | 1.36 | 0.77 of bread's | 1.02 | USDA 20080 | standard |
| bread | a grain's worth (1.4 kg loaves) | 252 | | 1.3 | 1.33 | 1.0 | 1.33 | USDA 18075 | standard |
| meat | 1,500 kcal edible | 114-250 | 1.0 | 1.5 (raw 0.8) | 0.6 | raw 0.53 | 0.6 (raw 0.32) | USDA 17164, 17165, 17178, beef | standard |
| fish | 1,150 kcal edible | 88-184 | 1.0 | 1.0 (raw 0.6) | 0.46 | raw 0.6 | 0.46 (raw 0.28) | USDA trout, pike, perch, carp, 15025, 15076 | standard |
| dried, smoked meat | half the weight | | | 3.0 | | rule 5 | 1.2 | D2-62 | rule |
| dried, smoked fish | half the weight | | | 2.0 | | rule 5 | 0.92 | | rule |
| salt meat, salt fish | the same weight | | | 1.4, 1.0 | | rule 5 | 0.57, 0.46 | | rule |
| milk | 1 kg | 61-70 | 1.0 | 0.5 | 0.26 | | 0.26 | USDA 01077 | standard |
| cheese | 1 kg (from 10 milk) | 330-410 | 1.0 | 2.5 | 1.6 | | 1.6 | USDA 01009 | standard |
| egg | 1 kg in shell | 143 | 0.88 | 0.6 | 0.50 | | 0.50 | USDA 01123; MW | standard |
| greens | 1 kg | 22-42 | 0.8 | 0.6 | 0.11 | | 0.11 | USDA 35205, 11616 | standard |
| roots | 1 kg pignut, silverweed | 50-110 | 0.8 | 0.8 | 0.26 | | 0.26 | no table: parsnip, burdock | estimate |
| mushrooms | 1 kg | 22-38 | 0.9 | 0.6 | 0.12 | | 0.12 | USDA 11239, 11260 | standard |
| watercress | 1 kg | 11 | 0.85 | 0.4 | 0.04 | | 0.04 | USDA 11591 | standard |
| samphire | 1 kg | 15-30 | 0.85 | 0.5 | 0.08 | | 0.08 | no USDA row | estimate |
| berries | 1 kg | 32-57 | 0.95 | 0.8 | 0.17 | | 0.17 | USDA 09042, 09050, 09316 | standard |
| hedge fruit | 1 kg | 50-162 | 0.7 | 0.6 | 0.21 | | 0.21 | USDA 09003, 09136 | standard |
| hazel nuts | 1 kg in shell | 628 | 0.43 | 1.6 | 1.08 | | 1.08 | USDA 12120 | standard |
| beech nuts | 1 kg in husk | 576 | 0.6 | 1.2 | 1.38 | | 1.38 | USDA 12014 | standard |
| acorns | 1 kg unleached | 387 | 0.75 | 0.1 | 1.16 | 0.035 (tannin) | 0.04 | USDA 12058 | standard |
| acorn meal | 2 from 3 acorns | 501 dried | | 1.0 | | | 1.48 | USDA 12060; leaching loses about 15% | estimate |
| green grain, rye | 1 kg | 40-90 | 1.0 | 0.15 | 0.24 | | 0.24 | green forage | estimate |
| wild food (legacy) | a gathered mix | | | 1.0 | | | 0.41 | the autumn mix | rule |
| tallow | 1 kg fat | 902 | 1.0 | 0 | 3.6 | 0 (the lights' good) | 0 | USDA 04001 | standard |

**Animal kinds** (live weight, dressing (carcass over live), the edible share of the carcass, edible offal at 3% of live for the
mammals, kcal a kg of what is eaten; food a head now (the engine's goods × 1.5 for meat, × 1.0 for fish) and on the basis):

| Kind | Live kg (range) | Dressing | Edible | kcal/kg | Edible kg | Food now | Basis (range) | Factor | Goods now → rec. | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| red deer | 90 (60-150) | 0.57 | 0.75 | 1,200 | 41 | 30 | 19.8 (13-33) | 0.66 | 20 → 33 meat | Mitchell et al.; USDA 17164 |
| roe deer | 22 (18-30) | 0.60 | 0.72 | 1,200 | 10 | 6.8 | 4.9 (4.0-6.7) | 0.72 | 4.5 → 8.1 | Mitchell et al. |
| wild boar | 70 (50-120) | 0.68 | 0.70 | 1,600 | 35 | 22.5 | 22.7 (16-39) | 1.01 | 15 → 38 | USDA 17165 (lean); autumn fat |
| brown hare | 3.5 (3-4.5) | 0.60 | 0.75 | 1,140 | 1.6 | 1.05 | 0.75 (0.64-0.96) | 0.71 | 0.7 → 1.25 | USDA 17178 |
| woodpigeon | 0.5 | 0.50 | 0.70 | 1,420 | 0.17 | 0.15 | 0.10 | 0.66 | 0.1 → 0.17 | USDA 05153 |
| wildfowl (mallard) | 1.1 (0.9-1.3) | 0.60 | 0.70 | 1,700 | 0.46 | 0.45 | 0.31 | 0.70 | 0.3 → 0.52 | USDA 05141 |
| brown bear | 250 (150-350) | 0.60 | 0.70 | 1,610 | 113 | 60 | 72 (43-101) | 1.21 | 40 → 121 | USDA 17146 |
| **eel** | 0.5 (0.1-1.5) | whole | 0.72 | 1,840 | 0.36 | 0.2 | **0.27 (0.05-0.80)** | **1.32** | 0.2 → 0.58 fish | Tesch; USDA 15025 (checked); FAO-fish |
| **salmon** | 4.0 (2-8) | whole | 0.62 | 1,420 | 2.5 | 2.0 | **1.41 (0.70-2.8)** | **0.70** | 2.0 → 3.1 fish | USDA 15076; FAO-fish |
| lamprey | 0.15 (0.05-1.5) | whole | 0.80 | 2,000 | 0.12 | 0.45 | 0.10 | 0.21 | 0.3 meat → 0.21 fish | estimate |
| cow | 300 (250-350) | 0.50 | 0.70 | 2,000 | 114 | 60 | 91 (76-106) | 1.52 | 40 → 152 | Albarella (size); beef |
| ox, bull | 400 (350-500) | 0.52 | 0.70 | 2,000 | 158 | 75 | 126 (110-158) | 1.68 | 50 → 210 | as cow |
| young (calf, yearling) | 120 (80-160) | 0.55 | 0.70 | 1,500 | 51 | 15 | 31 (20-41) | 2.04 | 10 → 51 | estimate |

Read: on the basis, wild game is about 0.7 of its food a head now (meat at 1.5 a unit overstates what each unit holds), except
the boar and the bear (fat). The farm beasts are 1.5 to 2 times now (the cow was set at a quarter of its weight). The eel is a
little low at the engine's size and fair at a run's; the salmon and the lamprey are high.

**Return rates by method** (kcal an hour; the real food a unit is the rate × 2 h ÷ 2,500):

| Method | Real kcal an hour | Real food a unit | Source | Conf. |
|---|---|---|---|---|
| farming, ox plough, sickle, flail (net of seed) | 4,000-7,000 | 3.2-5.6 | Titow; Campbell; Clark; Henley (an acre a day a team) | standard |
| farming, hoe or spade | 1,500-3,000 | 1.2-2.4 | Clark; spade work 1/20 to 1/10 acre a day | estimate |
| milking alone | 8,000-14,000 | 6.4-11 | Trow-Smith (about 3 kg a cow a day); hand milking 6 to 10 cows an hour | estimate |
| gathering nuts (with cracking) | 1,000-3,000 | 0.8-2.4 | Holst 2010; Kelly ch. 3 | standard |
| gathering greens and berries | 300-1,400 | 0.24-1.1 | greens 2 to 4 kg an hour at 300 kcal/kg; berries 1 to 3 kg at 450 | estimate |
| gathering in winter (roots, haws) | 150-800 | 0.12-0.64 | | estimate |
| acorns, gathered and leached | 1,000-1,800 | 0.8-1.4 | Kelly (Californian acorns with processing) | standard |
| hunting, including search: novice, capable, master | 100-400; 500-1,500; 1,500-4,000 | 0.08-0.32; 0.4-1.2; 1.2-3.2 | Hill et al. 1987 (Ache men about 1,300 an hour of hunting); Kelly (deer 18,000 to 31,000 after the encounter) | standard |
| snares (hares) | 500-1,500 | 0.4-1.2 | Simms (jackrabbit after the encounter 13,500); a line set and lifted | estimate |
| fowling with nets | 300-2,700 | 0.24-2.2 | Simms (ducks 1,975-2,700 after the encounter) | standard |
| fishing by hand | 200-900 | 0.16-0.72 | 0.2 to 0.8 kg an hour | estimate |
| angling, hand line | 300-1,800 | 0.24-1.4 | Kelly (hook and line, wide) | standard |
| a weir or race trap on a run night | 5,000-60,000 | 4-48 | Darby (Domesday mills and fisheries rendering hundreds to thousands of eels a year); Bush | estimate |
| grinding by quern | (no food) | 1-2 kg grain an hour | experimental querns | estimate |

The hunting rates include the search. Kelly's post-encounter rates (15,000 to 31,000 kcal an hour for deer) are the pursuit alone.

**The runs, real** (`table.real_runs`): silver eels 20 to 50 a km² of catchment a year at Burrishoole (over 4,000 a year before
1982 and about 2,000 after, from about 90 km², Poole et al. 2018), and several times more before the recruitment collapse (ICES
WGEEL); taken here as 20 / 50 / 150. Adult salmon about 5 to 20 a km² (the River Bush: about 20,000 wild smolts a year and 5,000
or more Bush fish taken at sea, 1987-91, from about 340 km²; the area is recalled). The run sizes are compressed to the engine's
year by 32/365, as rule 7 asks.

## 2. Before and after

**Food a unit of each good** is in part 1. **Food a unit of work by method**, now and after (at the same kilograms a unit; only
the food a kg changes), against the real rate:

| Method | Now | After | After, with the rate fix | Real | Verdict after |
|---|---|---|---|---|---|
| farming, unbroken ground, crude reap | 1.77 | 1.81 | | 1.6-3.6 | pays, in range |
| farming, hoe-broken | 1.37 | 1.40 | | 1.2-2.4 | pays, in range |
| farming, plough-broken | 2.35 | 2.41 | | 3.2-5.6 | pays; a little under the real |
| farming, plough and copper reap | 2.80 | 2.87 | | 3.6-6.0 | pays; a little under |
| milking (3 cows a unit) | 2.4 | 1.23 | 4.6 (6 cows, 3 kg each) | 6.4-11 | pays |
| gathering, autumn (novice to skilled) | 1.07-1.72 | 0.55-0.88 | | 0.8-2.4 | pays, the low end |
| gathering, spring and summer | 0.28-0.77 | 0.06-0.17 | 0.16-0.43 (2.5 times the kg) | 0.24-1.1 | thin |
| gathering, winter | 0.19-0.43 | 0.08-0.17 | | 0.12-0.64 | never pays (as real) |
| leaching acorns (the gain) | 1.7 | 2.84 | | 0.8-1.4 (with gathering) | rich |
| hunting, novice armed, near | 0.2-0.3 | 0.14-0.22 | | 0.08-0.32 | never pays (as real) |
| hunting, capable armed, near | 0.7 | 0.51 | | 0.4-1.2 | pays |
| hunting, master armed, near | 2.5 | 1.87 | | 1.2-3.2 | pays |
| snares, lifted | 0.9 | 0.64 | | 0.4-1.2 | pays |
| netting fowl | 0.11-0.70 | 0.08-0.49 | | 0.24-2.2 | pays at the top |
| fishing by hand (full stock) | 0.6 | 0.28 | | 0.16-0.72 | feeds only the fisher |
| angling | 1.5 | 0.69 | | 0.24-1.4 | pays |
| eel trap, resident, a night (02zzd, before 4c) | 0.02-0.08 | 0.01-0.04 | | 0.16-1.2 | never pays; far under the real |
| trap in a mill race, run night | 1.1-6.5 | 1.5-8.6 | | 4-32 | pays |
| weir, eel run night (3 units, 38.73) | 0.3-1.4 | 0.4-1.9 | | 4-32 | far under the real |
| weir, salmon run night (3 units, 38.73) | 4.5-5.5 | 3.2-3.9 | | 4-48 | pays |
| hand mill, ox mill, water mill (the gain) | 0.9, 9.6, 30 | 0.92, 9.8, 31 | | none | a design gain (part 3) |
| baking, hearth and oven (the gain) | 3.0, 10 | 3.1, 10.2 | | none | a design gain |

Sources of the "now" column: 02zzd (9 Nov: farming, milk, gathering, the resident eel trap), hunt_calibration.md §2 (4c's
targets, which the build met on its gate), the wild region run (snares), 38.73 (the river's gate: race, weir, nets), and the
engine's data (the mills, the fishing yields at a full stock). The hunting "after" weights each hunter's take by kind (the master
40% red deer, 40% roe, 20% boar; the capable half roe, 40% hares; the novice mostly hares): `HUNT_MIX` in the script, an
assumption.

**Two things change besides the values:**
- **Cheese:** the engine's 6 milk to a cheese becomes 10 to 1, as a hard cheese is made (1.6 food a kg).
- **Milking:** milk at about 3 kg a cow a day (Trow-Smith: medieval cows about 100 to 170 gallons a lactation) and about six cows a
  unit. A cow's food a day then stays where it is (0.77 against 0.8 now), and the unit of milking is near the real rate.

**Eggs** are on the old clock. A kept hen lays 5 eggs an engine day at 0.02 food each (`engine/wild.py`, "an engine day is about
11 real days"), 0.1 food a hen a day. On rule 7 (a day is a day) a medieval hen gives about 0.3 eggs a day, 0.0075 food. Hens fall
to a garnish, which they were. Either way the egg unit (0.1 weight, 0.6 food) should become a kilogram of eggs (0.5 food).

## 3. The design choices kept

Each is a place the game departs from the physical basis on purpose. Each is stated as a factor on the physical value, so the next
good added has a rule.

| # | Choice | Physical | The game | Factor | Why it is kept |
|---|---|---|---|---|---|
| 1 | **The grain ladder** (D2-60, D4-107) | boiled whole grain about 0.85-0.9 as available as bread | grain 0.7, meal and flour 1.0, bread 1.3 | whole grain 0.54, meal 0.77, bread 1.0 of the grain's energy | Zach kept the mill's food gain (D4-107). On this basis the gain is a penalty on whole grain, not food made from nothing: bread is the grain's whole energy (1.33 at 2,500 kcal), and nothing passes it. The engine's values already sit on it (×1.02). |
| 2 | Raw grain, flour | raw grain poorly digested | 0.2, 0.5 | 0.15, 0.38 of bread's | the hearth matters (D2-160) |
| 3 | Beans "less food" (D2-53) | as grain a kg | 0.6, and a crop yield of 0.6 | 0.44 now; 0.53 recommended (grain's rung) | Two penalties at once. Keep the yield's 0.6 (real pulses yield about 0.8 of a cereal by weight), and put beans on grain's rung: 0.72. For Zach. |
| 4 | Cooked against raw meat and fish | cooking adds 10 to 30% of net energy | raw 0.53, 0.6 of cooked | as now | fire matters |
| 5 | Raw acorns | inedible for tannin | 0.1 | 0.035 | physical; stated as a factor so leaching is the way in |
| 6 | Tallow | the densest food there is (3.6 a kg) | 0 | 0 | the lights' good (brief 3 §5). A starving house would eat it: for Zach whether it is food in a famine. |
| 7 | The mills' and ovens' throughput | a mill saves work and makes no food | the ox mill 9.8 food a unit, the water mill 31, the oven 10 | the ladder × the batch | D4-97, D4-107. Flagged in part 4 as the richest units of work in the game. |
| 8 | The hunt's chances and skill curve | | 4c's calibration | | The basis changes only the food a kill, not how often one kills. |
| 9 | The weir's share (0.30 a wattle section) and hold | | 10 food a night | a hold in kilograms: 30 kg (60 eels, 7 salmon) | Physical: a trap holds weight, not food. 30 kg is about the same food now (10.6 in salmon, 16 in eels). |
| 10 | The compressed year (rule 7) | | | growth, breeding and run sizes × 32/365; returns an hour and the day's need real | as the proposal. Two places use the old principle (node_ecology.md: an engine day as 11 real days): the hens' laying and the TAKEN comment "real content × Y/365". Spoilage uses both clocks: fresh goods by the night, kept goods (grain 0.5% a night in a house, about 15% an engine year) by the year. Rule 6 should say which clock each rate is on. |
| 11 | Plant stocks set by food | stocks by biomass | `plants.niche` sizes each kind's capacity as the parcel's food ÷ its food a unit, floored at 0.3 | | On the basis, greens, mushrooms, cress, samphire, berries, hedge fruit and roots fall below the floor, so the parcel's plant food falls by up to a third of what it was. The stock should be sized in kilograms (a standing crop a hectare), not food. |
| 12 | The carry | | 10 on foot, 20 with a pack | | Not a departure, a consequence: a red deer becomes 33 units (41 kg eaten), two loads with a pack. That is real, and it makes the pack ox and the trip out (D2-256) matter. |

## 4. The check for every activity

**What a unit of work must give** (`breakeven`): on the basis a day with no work needs 0.84 food (2,100 kcal: PAL 1.4 × BMR
1,500, FAO-WHO 2004), and a unit of manual work adds 0.08 (100 kcal an hour over a working day's rests: about 3 METs against 1.5,
Compendium 2011). A six-unit day is 1.32 food (3,300 kcal, PAL about 2.2, a heavy farm day). So a unit of food work must give:
- **0.22** to feed the worker alone;
- **0.36** to feed a household of five with two workers (two adults, an elder at 0.8, two children at 0.6).

Against the labour rule now (0.04 a unit), the basis doubles work's cost and lowers the resting ration a sixth.

**The verdicts** are in part 2's last column:
- **Never pays, as in life:** winter gathering (0.08 to 0.17), the novice hunting near home (0.14 to 0.22), spring gathering
  without the rate fix (0.06 to 0.17). These are lean-season fallbacks, not livings.
- **Feeds only the worker:** fishing by hand at a full stock (0.28).
- **Far under the real rate:**
  - the weir on an eel night (0.4 to 1.9 against 4 to 32): the runs' size (part 6);
  - the resident eel trap (02zzd's 0.01 to 0.04, measured before 4c's set works; to remeasure);
  - spring gathering, where the kilograms a unit (about 1.2) are a third of real picking (greens 4 to 8 kg in two hours):
    raise `ease` about 2.5 times for greens and berries (giving 0.16 to 0.43);
  - milking (3 cows a unit against 12 to 20 by hand).
- **Absurdly rich:** the ox mill (9.8 food a unit) and the water mill (31), the oven (10); and slaughter, 45 food a unit on the basis
  (90 food in 2 units), though that is capital drawn down, not production. Leaching acorns at 2.8 is above the acorn's real rate
  with gathering (0.8 to 1.4), but leaching alone is only part of the work. Nothing else is more than twice its real top.
- **The order of livelihoods on the basis:** milking (with the fix) 4.6 > plough farming 2.4 to 2.9 > the master hunter 1.9 >
  hoe farming 1.4 > autumn gathering 0.55 to 0.9 ≈ angling 0.7 ≈ snares 0.6 > the capable hunter 0.5 > fishing by hand 0.3 > spring
  and winter gathering and the novice hunter, under 0.22.

**For Zach: the master hunter.** D2-255 has a very skilled hunter bring in a disproportionate amount, and 4c's target is 2.5 a
unit, above the best gatherer and near the farmer. On the basis the same kills give 1.9: still the best wild living by a wide
margin, and inside the real range (1.2 to 3.2), but under the ploughman. To keep 2.5, the hunt's take would have to rise by about
a third (more kills, not more food a kill). The physical answer is that real farming out-yields real hunting an hour on good land,
and hunting wins on land that cannot be farmed and in a season with nothing to reap. Default taken here: report it and change
nothing in 4c.

## 5. The worlds re-checked

**Measured:** the capacity model (`cybertron2.capacity`, D4-102) on every committed world with people that it can read (seven
worlds), three times each:
- **now:** today's values;
- **goods:** the recommended values patched in memory (`patch_engine("goods")`): every food good's value, the kills' goods, the
  slaughter yields, milk at 3 kg a cow and six cows a unit, cheese 10 to 1;
- **needs:** the same, with the needs on the basis as well (the ration 0.84, work 0.08 a unit, a child 0.6, an infant 0.4, a
  pregnancy 0.1).

People supported, the whole region, at three of the model's levels ("as it stands", "worked", "best"), with the ratio to the
people there in brackets; and food a year as it stands by source:

| World | People | Standing: now / goods / needs | Worked: now / goods / needs | Best: now / goods / needs | Food a year as it stands, now → goods |
|---|---|---|---|---|---|
| runs (runs_models) | 45 | 35.6 (0.79) / 30.4 (0.68) / 36.3 (0.81) | 168 / 168 / 201 | 308 / 318 / 386 | fields 616 → 631; fish 289 → 133; herds 184 → 177 |
| river | 26 | 25.8 (0.99) / 24.9 (0.96) / 29.4 (1.13) | 98 / 103 / 121 | 252 / 261 / 310 | fields 596 → 611; fish 68 → 31; herds 184 → 177 |
| lake | 14 | 20.4 (1.46) / 15.6 (1.11) / 18.1 (1.29) | 55 / 53 / 62 | 80 / 82 / 97 | fields 291 → 298; fish 274 → 126; herds 92 → 89 |
| peoples w1 | 20 | 13.9 (0.69) / 10.5 (0.52) / 11.9 (0.59) | 45 / 43 / 50 | 77 / 77 / 90 | fields 147 → 151; fish 203 → 93; herds 123 → 118 |
| fishing probe (fishing/water) | 8 | 5.9 (0.74) / 3.2 (0.40) / 3.6 (0.45) | 9.4 / 6.7 / 7.6 | 11.3 / 8.7 / 10.0 | fields 33 → 34; fish 143 → 66; wild plants 8.5 → 3.5 |
| plenty (brookend) | 8 | 22.0 (2.75) / 19.6 (2.45) / 23.2 (2.89) | 117 / 120 / 141 | 208 / 213 / 255 | fields 425 → 436; plants 68 → 28; game 59 → 23; herds 154 → 148 |
| wenbridge | 12 | 3.9 (0.32) / 2.6 (0.22) / 2.9 (0.24) | 14.0 / 13.0 / 14.7 | 25.2 / 25.0 / 28.7 | fields 66 → 67; plants 36 → 15; game 34 → 14 |

forest_households.yaml could not be read by the model (its spec has no `days`), and peoples w4 was not run.

**The larders** (the houses' stocks at the start, in food): unchanged within 5% where they are grain and beans (river, lake, w1,
the fishing probe, brookend, wenbridge). The runs world's falls a quarter (353 → 265), since its smoked fish and dried meat halve.

**Read (inference):**
1. **Farming worlds hold.** The fields' food rises 2 to 3% (the grain ladder is on the basis), the herds' falls 3 to 4% (the milk
   offset by the calves), and the needs on the basis add 15 to 20% to the people supported: a resting day costs less (0.84), and
   only the work adds.
2. **Fish carries the water worlds, and fish falls by 0.46** where its stock is counted in units (kilograms), as `K` is (8 a unit of
   size, OPEN L-75). The lake's standing capacity goes from 1.46 to 1.11 (1.29 with the needs), w1's from 0.69 to 0.52 (0.59), the
   fishing probe's from 0.74 to 0.40 (0.45).
   - To keep the fishing worlds where they are, the resident fish stocks need about 2.2 times the kilograms a unit of size.
   - Or the fishing worlds take the lower capacity as the truth: a fishing village of 8 on that water is then about twice too many.
   - Which one is real depends on a unit of size in hectares and a real standing biomass (50 to 300 kg a hectare of river and lake)
     that the worlds do not fix (part 8).
3. **The wild plants and the legacy hunt fall by about 0.4** (brookend, wenbridge).
   - The plants fall by the food a kilogram. The legacy `hunt` falls because its kill (2 to 6 meat units) keeps today's units. On
     the basis its range should be about 5 to 15, as the wild pack's kills rise.
   - The wild pack's own gathering and hunting are not in the model (part 8); the methods table (part 2) gives their change: about
     0.5 for gathering, 0.7 for hunting.
4. **What each world needs to stay viable on the basis:**

| World | Needs |
|---|---|
| runs | the runs sized as part 6 (the model does not count them, so its 0.68 is a floor); its fields carry it as they stand; keeping capacity (smokehouses, salt) for a run several times larger |
| river | nothing for capacity (0.96 standing, 1.13 with the needs); the runs as part 6 for the weir to matter at Saltwell |
| lake | fish stocks × about 2.2 to stay a fishing world; otherwise it holds as a mixed one (1.1 to 1.3) |
| peoples w1 | already short as it stands (0.69 now); more fields worked (it is 2.2 worked), or the fish stocks × 2 |
| fishing probe | fish stocks × 2.2, or fewer people (4 to 5), or angling's kilograms a unit raised (it is a fishing-only probe) |
| brookend | nothing: still plenty (2.45 standing) |
| wenbridge | as now: it was short as it stands (0.32) and is viable only worked (1.08 to 1.22) |
| the nutrition worlds (D2-257) | each livelihood measured on the basis from the start; the fishing and runs arms need their stocks and runs resized first, or they measure the old units |


## 6. The runs and the weir

**Measured:** the run pulses at each village's stretch, the runs world (`specs/water/runs_models.yaml`, the world of W-58's model
run) and the river world (`specs/water/river.yaml`), stepped 36 nights from the start with no one acting (`runs` mode; recorded
in the JSON, `runs.<world>.nights`). Heads a year passing each station, before any take:

| World | Station | Catchment above (km²) | River above (km) | Eels a year | Salmon a year | Eel nights |
|---|---|---|---|---|---|---|
| runs | Highpool (upper) | 108 | 15 | 74 | 0.5 | 7 |
| runs | Middleham (middle) | 235 | 33 | 169 | 0.5 | 10 |
| runs | Lowstrand (lower) | 1,050 | 141 | 623 | 21 | 14 |
| river | Saltwell (upper) | 267 | 41 | 77 | 10 | 2 |
| river | Millham (lower) | 886 | 130 | 336 | 31 (and 18 held below the dam) | 5 |

**Against a real river** (compressed to the engine's year, 32/365, by catchment): eels 20 / 50 / 150 a km² a year give
Highpool 190 / 470 / 1,400, Middleham 410 / 1,030 / 3,100, Lowstrand 1,840 / 4,600 / 13,800. **The engine's eel runs are 2.5 to 7
times below even a modern river at its low end.** Salmon at 5 / 10 / 20 a km² give Middleham 100 / 200 / 410 and Lowstrand 460 /
920 / 1,840. **The engine's salmon are 20 to 90 times below at Lowstrand and about 200 to 800 times below at Middleham.**

**Why the salmon miss the middle of the river** (from `wild/runs.py`):
- the run returns only to head-water stretches (`Net.heads`: those with nothing above), at `cap_km` 1.5 spawners a km of the head
  stretch;
- Beverton-Holt with r 2 settles at s = 1.5 × km, so the whole river carries about 1.5 salmon a km of head water, some 20 to 30 a
  year;
- most of the head waters join below Middleham.

Real salmon spawn in gravel along the main stem and every tributary, so every station sees the fish bound above it, the middle more
than the head. The fix:
- spawn by the river km (or catchment) above each stretch, not by head waters;
- size the return by catchment, about 5 to 20 adults a km² before compression, so 0.4 to 1.8 a km² of the engine's year.

**The eel and salmon values:** the eel on the basis is 0.27 food at the engine's 0.5 kg (×1.32), and the salmon 1.41 (×0.70).
The weir's year (one wattle section: share 0.30, hold 10 food a night; work = 45% of its build a year as upkeep, D2-210, plus
shutting and opening, plus a unit to lift each run night; the build is 24 units and 12 timber at 2/3 unit a timber; in the first
year the whole build is added):

| Station | As built: food a year, a unit | Eel and salmon on the basis | Real run, low | Real run, mid | Real run, high |
|---|---|---|---|---|---|
| Highpool | 4.7, **0.17** | 6.1, 0.22 | 35, 1.4 | 67, 2.8 | 74, 3.0 |
| **Middleham** | 10.4, **0.37** | 13.6, **0.48** | 76, **2.8** | 105, **3.9** | 106, 3.9 |
| Lowstrand | 50, 1.6 | 58, 1.9 | 113, 3.6 | 132, 4.2 | 143, 4.6 |
| Saltwell (river world) | 10.4, 0.37 | 10.2, 0.36 | 64, 2.2 | 84, 3.0 | 105, 3.7 |
| Millham (river world) | 38.5, 1.3 | 39.6, 1.35 | 114, 3.9 | 125, 4.3 | 127, 4.3 |

First-year food a unit, with the whole build counted, is about 60% of these figures (JSON: `first_year_food_a_unit`). With the
real runs, salmon were not run in the engine above the lower stations. They are spread here over the station's eel nights, an
assumption.

**Read:**
1. **As built, the weir pays only at the lowest station** (1.3 to 1.6 a unit), as the runs-world analysis found. The values on
   the basis barely change it: the eel's gain and the salmon's loss nearly cancel.
2. **With a real river's runs it pays at every station**, about 1.4 to 3.9 a unit at the upper and middle ones (Middleham 2.8 to
   3.9). That is above
   plough farming (2.4) on its nights and in D2-209's "1 to 2 food a unit, more on a run night" band, counted over the whole year.
3. **At the lowest station the hold binds.** Lowstrand's 4,600 eels and 920 salmon would give about 380 food uncapped. The 10-food
   hold keeps it at 113 to 143 over 14 nights. So **D2-210's hold, not the run, is what keeps a weir in its targets** (about 60 to
   70 food a year for one section). With the engine's 10 to 14 run nights, one section takes 100 to 140 at the lower stations,
   above the target, because D2-210 assumed about 8 run nights. Either the hold falls to about 6 food (18 kg), or the runs
   concentrate onto fewer nights.
4. **The runs' nights.** Rule 7 compresses a year's run size by 32/365 while the engine keeps about real numbers of run nights
   (10 to 14 at the lower stations). So each night carries about a twelfth of a real night's fish, and a run night is never the glut
   it is on a real river. The better compression is fewer nights at about real density: an eel run of 3 to 5 dark, wet nights,
   salmon on 3 to 5 spates. That gives the weir and the race the "short burst of plenty" D2-210 asks for, with the hold and the
   keeping as the bounds.
5. **The share** (0.30 for a wattle section, to 0.5 for a full weir) is reasonable: medieval weirs could take nearly everything,
   which is why Magna Carta (cl. 33) ordered the kiddles off the Thames and the Medway. The hold should be stated in kilograms (30
   kg, about the same food now), so that a heavier eel or salmon does not change what a trap holds.

**What the runs world needs** (inference):
- the eel run about 3 to 6 times larger (the `RUNS.eel.year` share of the stock from 0.2 toward about 0.6, or more eels a km² of
  habitat);
- the salmon spread up the river by km and sized by catchment (`cap_km` about 15 to 30, or the rule above);
- the hold in kilograms;
- the run nights concentrated.

With those, a middle-station weir pays (about 3 a unit), the lowest station is capped by its hold, and the keeping (smokehouses,
salt, fuel: D2-210 §8) becomes the bottleneck it was meant to be.

## 7. How the results move with the basis

The basis changes nothing that is a ratio of energies. What a unit produces and what a person needs are both in kcal, so
**whether an activity pays, and the order of activities, do not depend on the kcal of a food.** What moves is every food number,
in proportion, and so how far today's values are from the physical ones:

| | 2,000 kcal | 2,500 kcal | 3,000 kcal |
|---|---|---|---|
| bread, flour, grain (the ladder kept) | 1.66, 1.28, 0.90 | 1.33, 1.02, 0.72 | 1.11, 0.85, 0.60 |
| meat, fish (a standard unit) | 0.75, 0.58 | 0.60, 0.46 | 0.50, 0.38 |
| greens a kg | 0.14 | 0.11 | 0.09 |
| red deer, roe, eel, salmon (a head) | 24.7, 6.1, 0.33, 1.76 | 19.8, 4.9, 0.27, 1.41 | 16.5, 4.1, 0.22, 1.17 |
| plough farming, master hunter (food a unit, after) | 3.0, 2.3 | 2.4, 1.9 | 2.0, 1.6 |
| ration (no work), a unit's work | 1.05, 0.10 | 0.84, 0.08 | 0.70, 0.07 |
| a unit must give: worker, household | 0.28, 0.45 | 0.22, 0.36 | 0.18, 0.30 |

- **The engine's grain values sit at about 2,550 kcal a food.** 2,500 is the one basis that leaves the grain ladder, and so every
  farming world, where it is. At 2,000 every grain value rises by a quarter, and at 3,000 falls by a sixth.
- **Hours a unit** move the real food a unit in proportion (1.5 h: three quarters of the 2 h figures). They move the day's units
  the other way: at 2 h the summer's 7 units are 14 hours, too long, and 6 units (12 h) is the most a day should hold. At 1.5 h the
  engine's 5 to 7 units are 7.5 to 10.5 h, about right, but every real rate a unit falls by a quarter, putting farming and the
  hunt a little further under. The engine's numbers fit 2 h better.

## 8. What could not be established

- **Most values are recalled, not looked up.** Only the eel's 184 kcal was checked this session. The USDA numbers given are
  standard and should be confirmed against FoodData Central, row by row, when the data change is written. The roots, samphire,
  lamprey, acorn meal and green crops have no table and are estimates.
- **The return rates are wide.** Ethnographic rates are from other continents and peoples; the medieval farm rates are per acre
  and season, converted. Neither says what a British forager got from pignut, nettle or hazel in an hour, and no source gives it
  directly (Holst 2010 is the nearest, for hazel).
- **The run sizes:** the Bush catchment (about 340 km²) is recalled. Lowland medieval rivers' silver eel runs are not known. The
  historical high end (150 a km²) is an inference from the recruitment collapse, not a count.
- **The edible shares of fish** (eel 0.72, salmon 0.62) are from FAO-type yield tables as recalled, ±0.1.
- **The gathered mixes by season** (`AUTUMN_MIX` and the others) and the hunters' takes by kind (`HUNT_MIX`) are assumptions. A
  re-run of 02zzd's and 4c's harnesses with the recommended values would measure them.
- **The capacity model leaves out** gathering wild food (the wild pack's `wild_forage`), the wild pack's hunting methods, the runs
  and the weir (capacity/graph.py says so). So part 5's capacities for the wild and water worlds are fields, resident fish, herds
  and the legacy forage only.
- **The calibration suite's twelve worlds** (D2-245) are generator specs with no people, which the capacity model skips. Part 5 uses
  the committed worlds with people instead.
- **The resident fish stocks** (K 8 food a unit of size, OPEN L-75) were not checked against real standing biomass: that needs a
  unit of size in hectares, which the worlds do not fix.

## Sources

The table's sources are in the script's `SOURCES` and the JSON's `table.sources`:
- **Food composition:** USDA FoodData Central SR Legacy; McCance and Widdowson's composition of foods; FAO Fisheries Technical
  Paper 309.
- **Energy needs and work:** FAO-WHO-UNU 2004; the Compendium of Physical Activities (2011).
- **Medieval farming and herds:** Titow 1972; Campbell 2000; Clark 1991; Walter of Henley (ed. Oschinsky 1971); Langdon 1986;
  Trow-Smith 1957; Albarella 1997.
- **Foraging and hunting:** Kelly 2013; Simms 1987; Hill et al. 1987; Holst 2010; Mitchell, Staines and Welch 1977.
- **Eels and salmon:** Tesch 2003; Poole et al. 2018; ICES WGEEL; Darby 1952 and 1971 (Domesday); the River Bush salmon station
  (AFBI; Hansard written answers 1990-95).
- **In this repository:** 02zzd and 02zzd_ev; hunt_calibration.md; river_and_water.md §2, §3b; 38.73 (the brief 5 gate);
  node_ecology.md (the old scaling principle); D2-53, D2-60, D2-62, D2-167, D2-209, D2-210, D2-216, D2-255, D4-97, D4-107.

*Current as of 20 Nov 2026.*
