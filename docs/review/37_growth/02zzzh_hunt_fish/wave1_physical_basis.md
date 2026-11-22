# Wave 1, part 1: the physical basis (weights, shelf lives, making costs, carrying)

22 Nov 2026, 37.2 (subagent). Thread: design wave part 1 (W-77), under fishing, hunting and their materials (W-73). A design
document for review. No code was changed and nothing was committed. Zach decided that the next wave is designed in full before it
is built (D2-278). This part is the physical basis everything else is priced on. Part 2 (materials and making) and part 3 (taking
and keeping) are to be priced from these tables.

**Read with:**
- the decisions: the three clocks (D2-273), a unit of work is 2 hours (D2-275), making durable things on the year clock (D2-276),
  the factor's target of about 1/7 reached through about 1/15 (D2-281), weights in kilograms and gear life by material (D2-264),
  food on one basis (D2-258 to D2-262), real values within about 20% (D2-259), smoking in three depths (D2-271), stores never slow
  a food below its base (D2-272, D2-279), tanning, bark, the pack basket and the frame (D2-281); `spec/core/clocks.md`;
- the proposals: `proposals/hunt_fish_materials.md` (§3 goods, §5 gear, §6 works, §7.3 keeping, §7.4 stores, §13 targets),
  `proposals/building_clock.md`, `proposals/store_rules.md` (the moving rates), `proposals/shared_units.md`;
- the research notes in this folder: building_clock.md (the inventory of real hours), storage.md, smokehouse_capacity.md,
  fibre_and_cord.md, withies_wood_materials.md, hunting_ladder.md, fishing_ladder.md; and 02zzu_shared_units.md, 02zzu_lookup.md,
  02zzv_carrying_in_runs.md, 02zzx_salting_rates.md, 02z_forest_model.py;
- the open rows: the racks' load (Q-83), salting's rate (Q-73), salt's fuel (L-110), hens on the old clock (L-138), clearing a plot
  at a time (L-153), the stores' scale gap (L-154), rest days (L-157); the carrying thread (W-71);
- the engine on main, 22 Nov: `engine/data.py` (ITEMS, DECAY, FITTINGS, ROOMS, BLUEPRINTS, STORES, WATER_WORKS, FENCES, CLEARING,
  TECHNIQUES, PHYSICS), `engine/night.py` (`decay_rate`, `spoil_rate`), `wild/kinds.py` (goods by kind).

**Marks.** Every figure carries one:
- **[s]** sourced, with the source named. Every web figure came from search-result summaries: page fetches were refused by the
  session's network (en.wikipedia.org did not resolve; the sibling notes record the same for fao.org, archive.org and others).
  Hosts would have to be allowed in the session's network settings to read the full texts.
- **[n]** from a sibling note in this folder, named; those notes mark their own figures, mostly search summaries and estimates.
- **[m]** measured: read from the engine's data or code on main, or computed from it.
- **[k]** a standard figure from the literature as I know it, not re-checked this session.
- **[e]** my estimate, with the reasoning given.

**The basis used throughout.**
- A unit of work is 2 hours (D2-275). A world year is 32 days at 6, 7, 6 and 5 units by season: **192 units, 384 hours** a person [m].
- A real working year is about 2,700 hours [n building_clock.md]. **The labour factor** f = 384 / 2,700 = **1/7.0**: the target
  (D2-281). The stage before it is 1/15; today's works sit at about 1/40, gear at or above real hours [n building_clock.md].
- **The calendar factor** is 32 / 365 = **1/11.4** (D2-273): for durations, never for work.
- **Units of capital** = real hours × f ÷ 2: real hours ÷ 14 at 1/7, ÷ 30 at 1/15. Things used up in one go or a handful of uses:
  real hours ÷ 2.
- **Weight** in ITEMS becomes kilograms a unit, and the carry limits are read in kilograms (D2-264).

---

## 0. In brief

**Weights (§1).**
- The food goods are coherent: a unit is about a kilogram (bread about 1.4 kg).
- The bulk goods are not. The present units cannot be made coherent by stating a kilogram figure alone:
  - a timber is "about 240 kg", a figure taken by compressing a real year's fuel into the engine's year (02z), against the day
    clock that now governs fuel burned a night;
  - a stone weighs 3, yet 30 stone build a 40 t room;
  - straw at 1 kg gives 4.7 kg a plot reaped against a real 50 to 100 kg;
  - hay at 1 kg is "a beast's day of feed", which is about 10 kg;
  - charcoal weighs 2 and is burnt from 5 timber.
- **Recommended: each bulk good gets a handling unit of a stated weight, and every recipe is rewritten in real kilograms:**
  - timber 25 kg (a pole or a hewn length, what one person shoulders);
  - stone 25 kg (a building stone);
  - firewood 10 kg (a bundle);
  - straw 16 kg (the statute truss of 36 lb [s]);
  - hay 10 kg (a beast's day [e]);
  - charcoal 20 kg;
  - withies and bark in 10 kg bundles.
- With these, three present rates become real with no change of number: straw's 4.7 a plot, fuel cut at 5 a unit, and salt's 1
  firewood a salt.

**Shelf lives (§2).**
- One keeping curve puts every shelf life on the year clock with the floor of a night or two: nights = min(d, 2) + (d − 2) / 11.4
  for a food that keeps d real days.
- The order is restored: fresh fish 1.5 nights, hot smoke 2.4, keeping smoke 9.7 (a season), hard cure 25, salt 34 (a year), dried
  41.
- Against a house's store today:
  - smoked fish keeps 10 nights in place of 462;
  - salt fish 34 in place of 231;
  - bread 2.3 in place of 46;
  - fresh meat 2.1 in place of 7.3;
  - grain a little longer, 221 in place of 138.
- Each store then removes a named penalty on top of the base rate: the open, wet, heat, flies, floor damp, frost, the heap, out of
  brine.

**Making costs (§3).** At 1/7, and at 1/15 in brackets:
- a wattle cottage 19 to 39 units (9 to 18), with about 2.5 t of materials;
- a timber small room 32 to 51 (15 to 24), with 5.5 to 8.5 t;
- a stone small room 45 to 90 (21 to 42), with 42 t;
- a hurdle fence round a 2 ha field 77 (36), or 14 (6) per 100 m;
- a gill net 3 to 4 units (1.3 to 2), plus its kilogram of cord;
- a wicker trap 0.3 to 0.6: six for 3 units (six for 1);
- a set of smoke racks 1 unit;
- **a wattle smoke hut** of one set (about 250 fish) 6 to 13 units, plus 1 for its racks;
- **a timber smokehouse** of 3 to 4 tiered sets (750 to 1,000 fish) 32 to 51 units, plus 3 to 4 for its racks.
- About 40 rows fall below the 1-unit floor and are batched (§5.3).
- One rule needs deciding: a life counted in nights (a bedroll, a tent) takes the calendar's 1/11.4, while a life counted in acts of
  work takes 1/7.

**Carrying (§4).**
- Real limits:
  - on foot about 10 kg is an arms' carry (real 15 to 20; kept as a named departure);
  - a creel +5;
  - the withy pack basket +15 (25 in all);
  - the leather-strapped frame +20 (30);
  - a pack ox about 100 kg against the engine's 60;
  - a handcart 100 to 150 on a track against 40;
  - a cart load 18 cwt, about 900 kg [s].
- A building's materials are 2.5 t (wattle), 5.5 to 8.5 t (timber) or about 42 t (stone).
- At the provisional moving rate (1 unit per 800 kg a parcel step), carrying adds about 8 to 16%, 14 to 33% and 58 to 117% to the
  build at 1/7 for each parcel step from the source.
- Carrying binds the stone house, the wall and any timber moved between villages; it does not bind wattle.
- **Timber should be hewn at the stump** (fell gives hewn lengths, the slab and sapwood left as firewood), shouldered as poles within
  the village, and moved between villages only by ox or cart.

**Consistency (§5).**
- A fishing household's making and mending at 1/7 is about 5% of its year with flax and a withy bed, and about 8% by wild cord and
  wild willow; fuel adds 3 to 4%, and its smoking fuel 3 to 9%.
- The network proposal's 10 to 20% target (§13) was set on the old gear prices. It holds only with fuel and keeping counted, or with
  clothing, which is parked.
- Food a unit of work by method is unchanged; food eaten a unit of work falls for gluts, as intended.
- Twenty-eight contradictions are listed (§5.4).

**Open questions (§6):** six.

---

## 1. Weights: every good's unit in kilograms

**The rule proposed.**
- `weight` in ITEMS is the kilograms of one unit.
- A food good's unit stays its kilogram on the D2-258 basis.
- A bulk material's unit is a handling unit of a stated weight (a bundle, a truss, a load), chosen so that one person handles one
  and recipes come out in whole or near-whole numbers.
- A discrete thing (a tool, a trap, a hide) is a count with a stated weight.
- Recipes state materials in these units, from real kilograms. A recipe never uses a unit as a stand-in for "some wood".

**What "now" means.** "Now" is the engine's `weight` [m]. Where the engine never said what a unit is, the column gives what its
other numbers imply.

### 1.1 Food goods

| Good | Unit proposed | kg | Now | Food a unit [m] | Source or reasoning | Flag |
|---|---|---|---|---|---|---|
| grain, rye | 1 kg threshed | 1 | 1 | 0.7 | [n 02zzu]: USDA 20004, 20062 | |
| beans | 1 kg dried peas or beans | 1 | 1 | 0.6 | [n 02zzu] | |
| flour, meal | a grain's worth | 0.9 | 1 | 1.0 | wholemeal 0.9 to 0.95 of the grain [k] | within 20%: keep 1, named |
| bread | a grain's worth of loaves | **1.4** | 1 | 1.3 | [n 02zzu]: "1.4 kg loaves"; bread is about 1.4 to 1.5 times the flour's weight [k] | **+40%**: set 1.4 |
| green grain, green rye, green beans | 1 kg cut green | 1 | 1 | 0.24 (fodder 0.8) | [n 02zzu] as food | **incoherent:** fodder 0.8 a kg makes 1 kg of green crop 0.8 of a beast's day, where a beast's day is about 30 kg green [e]; and `dry fodder` turns 10 kg green into 8 hay, a gain of mass (§5.4) |
| seed | the grain sown | 1 | 1 | | | |
| meat | 1,500 kcal of meat as eaten | **1.0** (0.6 for fat beef, 1.25 for venison) | 1 | 0.6 | [n 02zzu part 1] | one good with one value cannot be exact in both; the carry of a kill is understated about 25% for venison |
| fish | 1 kg gutted | 1 | 1 | 0.46 | D2-258 | |
| salt fish, salt meat | 1 kg of the cure | 1 | 1 | 0.46, 0.57 | [n 02zzx]: kept weight | wet-salted fish keeps about 0.8 to 0.9 of its weight [k]: within 20% |
| ★ hot-smoked fish (D2-271) | 1 kg, from 1.5 kg fresh | 1 | | 0.69 | eel 100 kg fresh gives about 60 kg smoked [n smokehouse_capacity] | new good |
| smoked fish (the keeping smoke) | 1 kg, from 2 kg fresh | 1 | 1 | 0.92 | the engine smokes to half [m]; a keeping smoke leaves 0.4 to 0.6 [n smokehouse_capacity] | |
| ★ hard-cured fish (D2-271) | 1 kg, from 2.5 kg fresh, salted first | 1 | | 1.15 | a hard smoke leaves about 0.3 to 0.35 [n smokehouse_capacity]; salting takes up part of the loss [e] | new good |
| dried fish, dried meat | 1 kg, from 2 kg fresh | 1 | 1 | 0.92, 1.2 | the engine dries to half [m] | **a named departure:** a hard-dried fish or strip is 0.25 to 0.35 of its fresh weight [n smokehouse_capacity], so a real kilogram would be 1.3 to 1.8 food |
| smoked meat | 1 kg, from 2 kg | 1 | 1 | 1.2 | as fish | |
| ★ hard-cured meat (bacon, ham: salted, then smoked) | 1 kg | 1 | | 0.6 | salt meat's weight [e] | proposed beside D2-271, which names fish; for Zach to confirm with part 3 |
| smoking fish, drying fish, smoking meat, drying meat | as fresh | 1 | 1 | as fresh | [m] | |
| milk | 1 kg | 1 | 1 | 0.256 | D2-260 | |
| cheese | 1 kg, from 6 kg of milk | 1 | 1 | 1.61 | [n 02zzu]; a soft or young cheese takes 6 to 7 kg of milk a kilogram, a hard one about 10 [k] | |
| egg | **1 kg of eggs in shell, about 17** | 1 | 1 | 0.6 | [n 02zzu] | **the name misleads:** "an egg" in a line reads as one egg (about 60 g, 0.035 food); laying runs on the old clock (L-138) |
| greens, mushrooms, watercress, samphire, berries, hedge fruit, roots | 1 kg as gathered | 1 | 1 | 0.04 to 0.33 | [n 02zzu, 02zzu_lookup] | |
| hazel nuts, beech nuts, acorns | 1 kg in shell or husk | 1 | 1 | 1.03, 1.2, 0.034 | [n 02zzu] | |
| acorn meal | 2 from 3 kg of acorns: about 0.8 kg leached and dried | 0.8 | 1 | 1.0 | the kernel is about 0.75 of the acorn, and leaching loses about 15% [n 02zzu] | within 20% |
| wild food (legacy) | 1 kg of a gathered mix | 1 | 1 | 0.41 | [n 02zzu] | |
| offal | 1 kg | 1 | 1 | 0 | | spoil 0 (§2): incoherent |
| rotting meat | 1 kg | 1 | 1 | 0 | | |

### 1.2 Fodder and the harvest's bulk goods

| Good | Unit proposed | kg | Now | Source or reasoning | What it makes coherent |
|---|---|---|---|---|---|
| **straw** | **a truss** | **16** | 1 | the statute truss of straw, 36 lb; 36 trusses made a cart load of 18 cwt [s: Truss (unit), Wikipedia, via search; Hay and Straw Act 1796] | reaping's **4.7 a plot** becomes about 75 kg a plot. A plot behaves as about 0.1 ha (16 kg of seed is about 160 kg a ha; 48 to 72 kg of grain is 480 to 720 kg a ha [m, with k: medieval sowing 135 to 270 kg a ha]), and long-straw cereals give 1 to 2 kg of straw a kg of grain [k]: 50 to 140 kg. At 1 kg a unit, straw is a fifteenth to a thirtieth of real. As fodder a truss is about 0.6 of hay's value a kg [k], so 1.0 fodder a truss is about right |
| **hay** | a beast's day | **10** | 1 | a cow of 300 to 400 kg eats about 2.5% of its weight a day, 8 to 10 kg of hay [e from k] | its `fodder` 1.0 ("a beast's day of feed a unit") and the pack ox's 1 hay a day. Making hay at 3 a unit becomes 15 kg an hour against a real 30 to 50 kg an hour all in (mowing about 0.4 ha a day at 2 to 3 t a ha [k], then turning, raking and carrying): **low about 2 to 3 times**, for part 2 |
| dung | (undefined) | ? | 1 | | **incoherent, for part 2:** a field takes 10 dung a plot, gathering gives 5 a unit and a head gives 20 a year; anchored on any one of these, the unit lies anywhere from about 25 to 250 kg [e] |

### 1.3 Wood and fuel

| Good | Unit proposed | kg | Now | Heat a unit (now, proposed) | Source or reasoning |
|---|---|---|---|---|---|
| **timber** | a pole or a hewn length: a green pole of 3 to 4 m and 12 to 15 cm, or a squared piece of the same mass | **25** | 2 (stated "about 240 kg" in 02z and the notes) | 2.0 → **1.25** (by mass, as firewood) | a green pole of that size is 0.03 to 0.04 m³ at 900 to 1,000 kg a m³, 27 to 40 kg [e from k]; 25 kg is a shoulder load. **The 240 kg came from dividing a household's real year of fuel by a hearth's 21 timber a 24-day year** [m 02z_forest_model.py, lines 17 to 18]: fuel compressed by the calendar. D2-273 puts fuel burned a night on the day clock, so the 240 kg has no basis now |
| **firewood** | a bundle of cut wood or brush | **10** | 1 (stated 60 kg) | 0.5 (kept) | a faggot or a bundle one carries [e]. With heat 0.5, the present need of 1 heat a normal night is 20 kg, and 4 a cold night 80 kg |
| **charcoal** | a sack | **20** | 2 | 6.0 → **2.0** | 5 timber (125 kg) giving 1 charcoal is a yield of 16%; real clamp yields run 12 to 25% by mass [k; n withies_wood_materials: about 8 kg of wood a kg]. Charcoal holds about 29 MJ a kg against wood's 15 [k]: 20 kg is about 3.9 bundles, so about 2 heat |
| bark (★, D2-281) | a bundle of peeled and dried oak bark | **10** | | | the same handling bundle as withies [e] |
| withies (★) | a bundle of green rods: about 25 hazel rods of 2 to 3 m, or a hundred fine willow rods | **10** | (1 in the withies note; 10 in the proposal) | | [n withies_wood_materials §3.1; hunt_fish_materials §3]. **The two documents disagree:** on D2-264's basis it is 10 |

**Fuel a night (proposed with the resize).**
- Organic energy ran about 10 to 20 GJ a person a year in pre-industrial western Europe, about half of it firewood [s: Warde,
  summaries of *Energy consumption in England and Wales 1560 to 2000* and *Historia Agraria* 2019].
- That is 5 to 10 GJ of wood, about 0.35 to 0.7 t a person a year at 15 MJ a kg [k], or 1.7 to 3.3 t for a household of five: 5 to
  9 kg a day on average [e].
- An open hearth in an English winter burns more [e], so the proposal is **about 10 kg a normal night and 30 kg a cold one**: heat
  0.5 and 1.5 in place of today's 1 and 4. At the new firewood unit those are 1 and 3 bundles.
- Today's numbers would burn 20 and 80 kg a night at 10 kg a bundle, and 120 and 480 kg at the old 60 kg.

### 1.4 Stone, earth, metal, salt, coin

| Good | Unit proposed | kg | Now | Source or reasoning | Flag |
|---|---|---|---|---|---|
| **stone** | a building stone, a load | **25** | 3 | a load one person lifts and carries [e] | **incoherent now:** a small stone room's 30 stone is about 40 t of wall, about 1.3 t a stone; a cellar's 4 stone line it with about 28 t, 7 t a stone [n storage §3.11, §11]; a crude tool's 0.5 stone is a head of about 1 kg |
| copper ore | a basket of ore | 3 (kept) | 3 | three of them smelt to 1 kg of copper | a rich ore at about 33% [e]; for part 2 |
| copper | 1 kg | 1 | 1 | | |
| salt | 1 kg | 1 | 1 | | |
| coin | a coin | **0.005 to 0.01** | 0 | a copper coin of a few grams [k] | **incoherent:** 1 copper makes 10 coin, so a coin is 100 g; for part 3 |
| clay, daub, lime | (no good) | | | daub is dug and mixed on the spot (work, no good) [n building_clock proposal]; tanning's lime is folded into wood ash from hearths [e] | clay waits on pottery |

### 1.5 Animal materials

| Good | Unit proposed | kg | Now | Source or reasoning | Flag |
|---|---|---|---|---|---|
| **hide** | a hide the size of a red deer's, dried | **6 green, about 3 dried** | 1 | a hide is about 7% of live weight [s: a Thai study of beef cattle via search, 41 and 35 kg hides at 470 to 550 kg live]; a 90 kg red deer gives about 6 kg [e] | **incoherent now:** a fox, a stoat, an otter, a roe and a red deer each give 1 hide, and a cow 2. Proposed by weight: a red deer or a boar 1, a roe 0.3, a cow 3 to 4 (20 to 25 kg green), a young beast 1; fox, stoat, otter and beaver give a **pelt** (a good for later: fur), not hide |
| ★ leather (D2-281) | 1 kg of bark-tanned leather | 1 | | sole leather from oak bark is 48 to 54 lb from 100 lb of green hide [s: Scientific American table, via search]: a hide (6 kg green) gives about 3 kg | |
| tallow | 1 kg | 1 | 1 | | a slaughtered cow gives 4 [m]; real cattle give more, 5 to 20 kg by condition [e] |
| tallow light | a dip | 0.2 | 0.2 | 1 tallow gives 4 today | a dip candle of 50 to 100 g, a rushlight 1 to 2 g of fat [n withies_wood_materials: over 1,600 rushes to the pound]; 5 dips from 1 kg is nearer [e] |
| ★ bone | 1 kg fit for working | 1 | | about 5% of a deer's live weight [n hunt_fish_materials §4.3] | |
| antler | a cast antler | 1.5 | 1 | a red stag's pair is 2 to 6 kg [n hunting_ladder] | |
| horn | a horn | 0.5 | 0.5 | | |
| beaver pelt, castoreum | a pelt; a pair of glands | 0.7, 0.2 | 1, 0.2 | [e] | |
| hen, cat (carried live) | one beast | 2, 3.5 | 1, 1 | [k] | minor |

### 1.6 Fibre

| Good | Unit | kg | Source |
|---|---|---|---|
| ★ cord | 1 kg of cord, twine, line or light rope | 1 | [n fibre_and_cord] |
| ★ flax | 1 kg of pulled straw | 1 | [n hunt_fish_materials §3] |
| ★ retted flax | 1 kg | 1 | about 8 kg of retted straw gives 1 kg of cord: a scutched fibre yield of 12 to 15% [n fibre_and_cord: 450 to 550 kg of fibre a ha from 3 to 5 t of straw, k] |

### 1.7 Gear, tools, weapons and containers (weight a piece)

| Item | kg a piece | Now | Source or reasoning |
|---|---|---|---|
| crude tool (a stone-headed axe, adze or hoe, hafted) | 1.5 | 1 | [e] |
| copper tool | 1.5 | 1 | a head of 0.5 to 1 kg and a haft [e] |
| crude weapon (a club or a wooden spear) | 1.5 | 1 | [e] |
| ★ spear (copper head) | 2 | | a head of 0.3 to 0.5 kg and an ash shaft [e from n hunting_ladder] |
| ★ bow and a quiver of arrows | 1.5 | | [e] |
| fishing rod | 0.8 | 1 | a hazel or willow pole [n withies_wood_materials] |
| ★ hand line, set line | 0.05, 0.5 | | [n fibre_and_cord, fishing_ladder] |
| ★ hooks, 5 of bone or 10 of copper | 0.05 | | [n hunt_fish_materials §5] |
| ★ leister or eel glaive | 2 | | [n fishing_ladder] |
| ★ wicker trap | 2.5 | | 0.4 to 0.5 withies, about 4 to 5 kg green, dried to about half [n withies_wood_materials §1.2, e] |
| ★ snares, a bundle of 25 | 0.2 | | 3 to 4 g of cord a snare, and pegs [n fibre_and_cord §3] |
| ★ fish net (gill, 20 m by 1.5 m), with floats and stone sinkers | 4 | | 1 kg of cord, 2 to 3 kg of sinkers and floats [e] |
| ★ fowling net (clap, 10 m by 2 m) | 2 | | 0.8 kg of cord and lines [n fibre_and_cord] |
| ★ dip or hoop net | 1 | | [e] |
| ★ seine (later) | 35 | | 10 kg of cord, ropes, floats and sinkers [n fibre_and_cord, fishing_ladder] |
| ★ creel | 1 | | 0.2 to 0.3 withies dried [e] |
| ★ withy pack basket (replaces the pack, D2-281) | 2 | pack: 1 | 0.4 withies dried, rawhide straps [e] |
| ★ leather-strapped frame (D2-281) | 3 | | a split ash or hazel frame of about 2.5 kg, 0.5 kg of leather [e] |
| ★ hurdle (1.8 m by 0.9 m) | 10 | | about 30 rods, one bundle [n withies_wood_materials §1.2] |
| handcart | 40 | 0 | [e] |
| wooden plough (an ard with a copper share) | 25 | 4 | [e] |
| harness (a yoke and traces) | 12 | 1 | [e] |
| bedroll | 3 | 1 | a dried hide or a blanket [e] |
| tent | 18 | 6 | three dried hides and poles [e] |
| clappers | 0.5 | 0.5 | |
| ★ sack (holds 50 kg) | 0.6 | | [n storage §3.2] |
| ★ basket (holds 25 kg) | 1.5 | | [n storage §3.3] |
| ★ chest or ark (holds 400 kg) | 60 | | about 100 kg of boards less the waste [n storage §3.4, e] |
| ★ barrel (holds 120 kg) | 25 | | [k]; from about 0.24 m³ of stave bolt [n storage §3.6] |
| ★ keep box | 8 | | about two traps' withies [n fishing_ladder] |
| ★ coracle (later) | 15 to 20 | | a cow hide and laths [n fishing_ladder] |

### 1.8 What the resize touches beyond ITEMS

- **Stocks and holds that count the old units:**
  - FORESTS' timber, young growth and dead wood (a timber now 25 kg: about 9.6 times the count at the 240 kg reading; firewood about
    6 times);
  - the woodshed's `holds` (40 timber at 240 kg is the real 9 to 10 t [n storage §3.13]: hold it in kg, 9,600);
  - the bins' 60 food and the cellar's 40 food a space (held in kg: storage.md's 300 kg and 30 kg a space with containers);
  - STORES' `kinds` (timber and firewood counted alike: hold them by kg);
  - the camp store's 10 (kg already);
  - the prompt's weights line ("timber 2, stone 3, ... everything else 1").
- **Recipes:** every recipe that takes timber, stone, firewood, straw, hay, charcoal or hide is restated from real kilograms (§3).
  They are not converted by a factor, because the old quantities were never on one basis: a crude tool's 1 timber stood for about
  1 kg of wood, a room's 8 timber for 0.1 to 0.6 t a timber, and the rod's 0.5 timber for 120 kg.
- **Rates of getting** (§3.1): felling, cutting, gathering and quarrying in the new units.
- **Kinds:** `wild/kinds.py` goods (hide by weight); `slaughter` (hide 3 to 4 a cow).

---

## 2. Shelf lives on the year clock

### 2.1 The rules

**The keeping curve.** For a food that keeps d real days when well kept, its half-life in nights is:

> **nights = min(d, 2) + max(0, d − 2) / 11.4**

- A day or two keeps its real nights (the floor, D2-273).
- Beyond that the extra compresses at the calendar's 1/11.4.
- The curve is continuous and rising, so the keeping order can never invert. A floor applied as max(d / 11.4, a night or two) would
  give the same 2 nights to everything from 2 days to 3 weeks: fresh meat, bread, hot smoke and soft fruit alike.
- Shelf life keeps a floor of real nights because a food is eaten a night on the day clock: a loaf that keeps a week should feed
  about as many meals as it really did. For d from 3 to 20 days the curve gives fewer nights than real days (7 days give 2.4): a
  named departure.

**Process times** (a wait: smoking, retting, tanning) compress whole at 1/11.4, at least one night, rounded to whole nights. The
two differ for this reason: a process is a wait before the good exists, and shelf life governs how much of a good is eaten before
it goes.

**Rates.**
- "Keeps d days" is read as about half lost or unfit by then: the half-life.
- The base rate is r = 1 − 0.5^(1/nights), the share lost a night when well kept (covered, dry, out of the sun: D2-272).
- **Penalties multiply the hazard, not the share:** r' = 1 − (1 − r)^k, so no penalty can take more than everything.
- In a house today the engine's rate is the item's `spoil` × 0.3 (`house_spoil`), × 2 for fresh fish (D2-212), and × the best
  fitting's `spoil` [m `night.spoil_rate`]. D2-272 removes the 0.3 and the fittings' multipliers.
- **The new `spoil` is the base rate, not an in-hand rate.** Hands take the open's penalties (§2.3).

### 2.2 The table

"Real" is the keeping when well kept, at an average season (the warm season's penalty is on top, §2.3). "Now in hand" and "now in a
house" are the engine's half-lives [m]. The new base half-life comes from the curve.

| Good | Real keeping (well kept) | Source | Base half-life (nights) | New base rate | Now in hand / in a house (half-life, nights) | Change in a house |
|---|---|---|---|---|---|---|
| **fresh fish**, gutted | 1 to 2 days (summer 1, cold weeks 3 to 5) | [k]; clocks spec ("fresh fish or meat about 1 to 2 nights") | **1.5** | **0.37** | 1.9 / 3.5 | x2.3 faster |
| **offal** | a day | [k] | 1.0 | 0.50 | never spoils (0) | **from none** |
| **milk** | a day in a cool place | [k] | 1.0 | 0.50 | 0 / 1.9 | x1.9 faster |
| **fresh meat** | 2 to 4 days hung cool | [k]; game hung up to a week in cold weather [k] | **2.1** (d 3) | **0.28** | 1.9 / 7.3 | x3.5 faster |
| green grain, rye, beans | heats in a heap within 1 to 2 days | [k]; DECAY `green crop` [m] | 1.5 | 0.37 | 3.1 / 11.2 | x7 faster |
| greens, watercress, mushrooms, berries | 1 to 3 days | [k] | 2.0 | 0.29 | 1.9 to 2.4 / 7.3 to 8.9 | x4 faster |
| samphire | 3 to 5 days | [k] | 2.2 | 0.27 | 3.1 / 11.2 | x5 faster |
| ★ **hot-smoked fish** (D2-271) | days to a couple of weeks; take 7 | [n smokehouse_capacity §3] | **2.4** | **0.25** | (new) | |
| **bread** | about a week (a coarse or rye loaf longer) | [k] | **2.3** (d 5) | **0.26** | 13.5 / 45.9 | **x20 faster** |
| wild food (legacy mix) | about 2 weeks | [e: an autumn mix of fruit, nuts and roots] | 3.1 | 0.20 | 4.3 / 15.1 | x5 faster |
| eggs | 3 to 5 weeks unchilled | [k] | 4.5 (d 30) | 0.14 | 13.5 / 45.9 | x10 faster |
| hedge fruit (sloes, haws, crabs, hips) | 2 weeks to months; take a month | [k] | 4.5 | 0.14 | 22.8 / 76.7 | x17 faster |
| roots (pignut, silverweed) | about 2 months kept cool and covered | [k: root crops in a clamp keep months] | 7.1 (d 60) | 0.093 | 13.5 / 45.9 | x6 faster |
| **flour, meal** | 1 to 3 months for wholemeal (the germ goes rancid) | [k] | **9.7** (d 90) | **0.069** | 41.2 / 138 | **x14 faster**: grind as needed |
| ★ **smoked fish, smoked meat** (the keeping smoke) | about a season | D2-271; [n smokehouse_capacity §3] | **9.7** (d 90) | **0.069** | 138 / 462 | **x48 faster** |
| cheese (pressed, farmhouse) | a season or more | [k] | 12.4 (d 120) | 0.055 | 34.3 / 115 | x9 faster |
| acorn meal | months, dried | [e] | 12.4 | 0.055 | 34.3 / 115 | x9 faster |
| beech nuts | months; oily, goes rancid | [k] | 12.4 | 0.055 | 115 / 385 | x31 faster |
| acorns (unleached) | half a year, dry | [k] | 17.6 (d 180) | 0.039 | 69 / 231 | x13 faster |
| ★ **hard-cured fish** (D2-271) | most of a year; take 270 days | D2-271; [n smokehouse_capacity §3] | **25.5** | **0.027** | (new) | |
| **salt fish, salt meat** | about a year, packed in its salt or brine | the brief; [n 02zzx; storage §3.6] | **33.8** (d 365) | **0.020** | salt fish 69 / 231; salt meat 231 / 770 | **x7 and x23 faster** |
| ★ hard-cured meat (bacon, ham) | about a year | [k] | 33.8 | 0.020 | (new) | |
| hazel nuts in shell | about a year | [k] | 33.8 | 0.020 | 173 / 577 | x17 faster |
| tallow | about a year (goes rancid slowly) | [k] | 33.8 | 0.020 | never | from none |
| **dried fish, dried meat** (kept dry) | a year to a year and a half, kept dry; stockfish years | the brief's order; [n smokehouse_capacity: hard-dried fish 6 to 9 months in the tropics] | **41.3** (d 450) | **0.017** | 34.3 / 115 | x2.8 faster |
| **grain, rye, beans** (dry; vermin apart, D2-279) | loses about 5 to 10% a year to insects and moulds | [k] | 221 (d about 2,500) | **0.003** | 41.2 / 138 | **x0.6: slower** |
| hay, straw (in a rick or a barn) | about 5% a year | [e] | about 430 | 0.0016 | never | from none (penalty in the open wet) |
| flax, retted flax (dry) | a year and more | [k] | about 430 | 0.0016 | (new) | |
| bark (dry, in a shed) | loses its tannin when weathered | [s: hemlock bark exposed two months lost nearly a quarter of its tannin, via search] | dry about 70 | 0.01 | (new) | open: x5 (§2.3) |
| hide (dried rawhide) | a year and more dry; a green hide rots in 2 to 3 days | [k] | 33.8 | 0.020 | `abs` 0.01 to 0.03 open, 0 in a store | the drying folded into dressing (a named compression) |
| leather, bone, antler, horn, cord, withies, timber, firewood, stone, salt, copper, charcoal | do not spoil when kept dry | | | 0 | 0 | penalties only (§2.3) |
| smoking fish or meat, drying fish or meat (in the smoke) | a well-run smoke loses a few per cent | [e] | | 0.03 a night in the smoke | 0.011 a night (0.15 × 0.3 × 0.25) | fire out: the fresh rate in the open |

**The order holds:**

| | Fresh fish | Hot smoke | Keeping smoke | Hard cure | Salt | Dried |
|---|---|---|---|---|---|---|
| half-life (nights) | 1.5 | 2.4 | 9.7 | 25.5 | 33.8 | 41.3 |
| rate | 0.37 | 0.25 | 0.069 | 0.027 | 0.020 | 0.017 |

Dried keeps longest only when kept dry: its damp penalty is the harshest (§2.3), so the store decides. A hearth-dried fish in a damp
cottage keeps less than salt fish in its brine.

**What the year does with it (an autumn run on night 18, the hungry spring at nights 32 to 40):** fish kept from the run to the end
of winter (14 nights) and to the end of the hungry spring (22 nights) [e from the rates]:

| Kept as | Left at the end of winter | Left at the end of spring |
|---|---|---|
| a keeping smoke | 37% | 21% |
| a hard cure | 68% | 55% |
| salt (in brine) | 75% | 64% |

A keeping smoke feeds the winter; a hard cure or salt carries the spring, and so trade.

### 2.3 What each store removes (the penalties on top of the base)

Each penalty multiplies the hazard (§2.1). The factors marked [m] are DECAY's today. Storage.md's estimates are marked [n storage
§7]; the rest are [e].

| Penalty | Goods it applies to | Factor | Removed by |
|---|---|---|---|
| **the open, dry** (sun, flies, scavengers' reach) | everything | DECAY `open_dry`: fresh meat and fish 2, grain 4, bread 3, cheese 3, dried 2, default 2 [m] | any roof |
| **the open, wet** | everything | DECAY `open_wet`: fresh 2.5, grain 10, bread 8, dried 6, cheese 5, default 4 [m]; **hay and straw 10, bark 5** [e] | any roof; for fuel, a woodshed (wet wood gives 0.7 of its heat [n storage, Q-24 (7)]) |
| **in hand** (carried all day) | fresh foods | 1.5 (sun and flies) [e] | a creel or basket with a cover: none [e] |
| | dry goods | 1 | |
| **the warm season** | fresh meat and fish, milk, cheese, eggs | DECAY `warm` 1.5 [m] | **a cellar** (D2-272: "a cellar's cool for the foods heat ruins") |
| | others | DECAY `warm` 1.2 | none |
| **flies** (warm season) | fresh and drying meat and fish, cheese | 1.5 [n storage §7] | smoke (a smoke loft, the racks: DECAY `smoke` 0.25 [m] stands for it), a barrel, bagging |
| **floor damp** | grain, rye, beans, flour, meal, salt, bread; dried fish and meat x3 [e] | 2 (x1.5 in sacks) [n storage §7] | bins, a chest, a barrel, a granary floor, staddles, a boarded upper floor; for dried goods a smoke loft or a dry loft |
| **cellar damp** | the same goods | 2 [n storage §7] | none in the cellar: keep them elsewhere |
| **frost** | roots (and later apples) | 3 (read as damage) [n storage §7] | a cellar, a clamp |
| **the heap** (sweating) | roots loose | 1.5 [n storage §7] | baskets, a clamp |
| **out of its brine or salt** | salt fish, salt meat | 2 [n storage §3.6] | a barrel in brine (a tub or crock later); on a dry floor packed in salt, 1.5 [e] |
| **a store's wear** | everything inside | as now, `wear.damp` 1.5 gappy, 3 holed [m] | mending |
| **vermin** | dry goods, by exposure | a share a night, separate from spoiling (D2-279; storage §6) | chests, bins, a granary on staddles, barrels, a cat, an owl, a terrier |

**Fresh fish in a store** keeps its D2-212 factor of 2 against fresh meat, within its own base: fresh fish at 0.37 already holds
that, against meat's 0.28 (about 1.4 times the hazard). The extra x2 in a store is dropped. Keeping it would make a house worse than
the open for fish.

**Salt** dissolves in the open wet: 0.2 lost a night [e]. Under a roof it does not spoil.

### 2.4 Process times on the year clock

Each is real days ÷ 11.4, at least one night, in whole nights.

| Process | Real | Nights | Source | Engine now |
|---|---|---|---|---|
| hot smoke | 2 to 18 hours | the same day (the act) | [n smokehouse_capacity §3] | (new) |
| keeping smoke | 4 to 14 days | **1** | [n smokehouse_capacity §8] | 3 |
| hard cure: salt, then a long cold smoke | salted up to 3 days, smoked 3 weeks to a month and more | **2 to 3** (after the salting) | [n smokehouse_capacity §3]; D2-271 | (new) |
| drying at a hearth rack | days to about 2 weeks for thin fish or strips | **1** | [n smokehouse_capacity §9 q5] | 3 (the same check as Q-83) |
| salting, settling in the barrel | about 10 days | 1 | [n 02zzx] | none (at once) |
| retting in water | 1 to 2 weeks | 1 | [n fibre_and_cord §2] | (new) |
| retting on grass (dew) | 3 to 6 weeks | 3 to 4 | [n fibre_and_cord §2] | (new) |
| liming a hide | 2 to 6 weeks | 2 to 4 | [k] | (new) |
| tanning in bark pits | 6 to 18 months (11 to 18 for heavy leather) | **16 to 48** | [s: 11 to 18 months, sometimes two years; Encyclopaedia Britannica 1810, via search]; [n hunt_fish_materials §7.6] | (new) |
| charcoal clamp burning | 2 to 5 days | 1 | [k] | at once |
| a bow stave seasoning | months to a year | 8 to 32 | [n hunting_ladder §1.3] | (new) |
| a withy bed coming into yield | 3 years | 3 world years | D2-264 (decided) | (new) |

---

## 3. Making costs

### 3.0 The rules applied

1. **The clock (D2-276's test): what ends its life.**
   - A thing used up in one go, or within a handful of uses, is on the day clock at real hours. "A handful" is where its real life
     in uses × 1/7 comes to under about 2 [n building_clock §2].
   - Anything that lasts is capital, on the year clock: real hours × f.
   - Materials are goods, got at real hours whatever they go into.
2. **The floor and batches.**
   - `verbs.cost` takes `int(units)`, so anything under 1 unit is free [m]. Every recipe takes at least 1 unit.
   - A thing under 1 unit is made in a batch that brings the act to about 1 unit (5 hurdles a unit, as tallow lights give 4).
   - A `build` act costs 2 units and puts in 2 × skill [m `_build`], so a fitting under 2 units still takes a whole act unless several
     go in one (beds and stalls already take `qty`).
3. **Lives come in three counts**, so that a life takes the factor of what wears it:
   - **worn by acts of work** (a net's sets, a tool's acts, a plough's plots): real uses × f (1/7; at the 1/15 stage, × 1/15, so a
     use costs the same);
   - **worn by nights** (a bedroll or tent slept in, a hearth's nights): nights happen at the calendar's rate, so real nights × 1/11.4.
     That is real years as world years;
   - **worn by time** (weather, rot, floods): real years as world years.
   - D2-276 names only the first and the last. The middle one follows from the same reasoning and is open question 4.
4. **Upkeep goes with the thing:** real hours × f, as often as its wear says.
5. **The trade's skill:** units are for one who knows the craft (a novice about twice); a master builder about half
   (proposals/building_clock.md). Nothing here changes D2-52's skill curve.
6. **Real hours** are from building_clock.md's inventory where it has them [n], with each one's own mark; new rows are marked.

### 3.1 The day clock: used up in one go or a handful of uses (real hours ÷ 2)

| Recipe or work | Real rate | Source | Units, as proposed | Engine now [m] | Inputs, proposed (new units) | Note |
|---|---|---|---|---|---|---|
| **fell** (fell, cross-cut and hew to lengths) | 55 to 110 kg an hour with steel [n building_clock §1.2] | est. | **4 timber a unit** (crude tool); copper x1.5 | 3 timber a 2-unit act (1.5 a unit) | standing trees | at 25 kg: 50 kg an hour, at the low end (a stone axe is slower than steel [k]). Hewing is folded in: what is left is firewood, 1 bundle a timber (02z's brash rule) |
| **cut** (young growth, coppice) | about 25 kg an hour [e] | est. | 5 firewood a unit (kept) | 5 firewood a unit | young growth | at 10 kg a bundle the present rate becomes real (it was 150 kg an hour at 60 kg) |
| **cut poles** (a managed wood's young growth as timber) | as cut | est. | **2 timber a unit** | the alias "cut poles" gives firewood [n withies_wood_materials] | young growth: 2.5 firewood-mass a timber | poles without felling standards |
| **firewood** (gather dead wood) | 15 to 40 kg an hour [e] | est. | 3 a unit (kept) | 3 a unit | dead wood | |
| **quarry** | 0.5 to 1 t a day by hand with wedges and picks: 50 to 100 kg an hour [e] | est. | **4 stone a unit** (crude) | 2 stone a 2-unit act | rock | |
| **cut withies** | wild: about 1.5 bundles a unit; a bed: about 4 [n withies_wood_materials §1.1] | est. | 1.5; 4 (kept from the proposal) | (new) | | winter full, summer a third |
| ★ **peel bark** (D2-281) | a peeler takes 3 to 6 t of bark a year in the April to June season of about 540 hours: 5.5 to 11 kg an hour [s: withies note's search summary] | sourced (sec.) | **1.5 bundles a unit**, late spring only (2 to 3 nights of the compressed year) | (new) | oak poles in a managed wood (the poles then go to charcoal or stakes) | |
| ★ **twist cord** (wild) | 35 to 80 hours a kg [n fibre_and_cord §2] | est. | 0.04 cord a unit (25 units a kg) | (new) | nettle, bast in season | |
| ★ **dress and spin** (flax) | 15 to 20 hours a kg, coarse 2-ply [n fibre_and_cord §2] | est. | 1 cord from 8 retted flax: **8 units** | (new) | retted flax 8 | fine net twine is 3 to 4 times dearer; folded into the net's units |
| ★ **ret flax** (a set) | a few hours a batch [n fibre_and_cord §2] | est. | 1 unit to lay, 1 to lift | (new) | flax | 1 night in water, 3 to 4 on grass |
| ★ **dress a kill** | a red deer 1 to 2 hours skilled; a roe about half an hour; a hare 10 to 15 minutes [n hunting_ladder §1.7] | est. | **1 unit**: a red deer or boar, 4 roe, or 10 hares or fowl | (none: a kill arrives dressed) | the carcass | gives hide (by weight, §1.5), tallow, bone, offal |
| ★ **tan** (soak, lime, scrape, bate, tan, dry, curry) | 6 to 12 hours of handling a cow hide over the months [e]; a deer-sized hide about 3 hours [e] | est. | **1.5 units a hide** (a 6 kg hide), spread over the pit's nights | (new) | a hide, 2 bark (20 kg), wood ash | gives 3 leather. The bark: sole leather holds about a third of its weight in tannin [k] and oak bark about 10% [s: tannin, via search], so about 10 kg of bark a hide at full use and 20 kg in practice [e] |
| grind (a quern) | 1 to 1.5 kg an hour [n building_clock §1.3] | est. | 3 grain a unit (kept) | 3 | | right |
| mill (ox), water mill | 10 to 20 and 50 to 150 kg an hour [n building_clock §1.3] | est. | 64 and 200 in 2 units (kept) | as kept | | D4-97 |
| bread (a hearth) | about 10 kg of loaves in 3 to 4 hours [n building_clock §1.3] | est. | **2 units** for 10 | 1 unit | flour 10, **0.5 firewood** (5 kg) | was 1 timber (25 kg at the new unit) |
| oven bread | 100 loaves in 8 to 10 hours with kneading [n building_clock §1.3] | est. | **4 units** for 100 | 3 | flour 100, **3 firewood** (30 kg, the oven's heating) | the oven's lining wears a firing |
| **salt fish, salt meat** (with gutting) | a non-specialist guts 30 to 60 kg an hour and salts gutted fish into a tub at 50 to 150 [n 02zzx §3] | est. | **40 fish a unit** (about 20 kg an hour), 10 salt | 4 a unit (Q-73) | salt 1 to 4 fish, 1 to 8 meat [n 02zzx] | the proposal's rate (hunt_fish_materials §7.3); Q-73 is Zach's |
| ★ hot smoke (at a hearth or fire) | a batch of 10 to 20 kg in 2 to 4 hours [n smokehouse_capacity §3] | est. | **1 unit for 10 fish**, the same day | (new) | 1 to 2 firewood | gives 6.5 hot-smoked fish |
| smoke fish, smoke meat (hang a keeping smoke) | 25 to 30 fish units a unit of work, splitting included [n smokehouse_capacity §5] | sourced (sec.) | **30 a unit** | 40 in 1 unit, whatever the batch | fuel 1 to 2 kg a kg: **0.1 to 0.2 firewood a fish** | 1 night; tend 1 unit a night (a named departure, x0.1 to x0.2) |
| ★ hard cure | salt fish hung as above | | 30 a unit, after salting | (new) | 2 to 3 kg of wood a kg over 2 to 3 nights [e]: 0.25 firewood a fish | timber or stone smokehouse only (D2-271) |
| dry fish, dry meat (a hearth rack) | thin fish or strips in days to about 2 weeks [n smokehouse_capacity §9] | est. | 8 a unit (kept) | 8 in 1 unit, 3 nights | the hearth's own fire | 1 night proposed |
| tend the smoke | 1 to 3 hours a real day [n smokehouse_capacity §5] | est. | 1 unit a night (kept) | 1 | | a named departure |
| boil salt | at medium brine, about 10 kg of wood a kg of salt [e: 3 kg of water a kg from 25% brine, about 7 MJ, at 10 to 20% efficiency in an open pan]; seawater about 3 times that [e] | est. | 4 salt a unit (kept) | 4, for 4 firewood | **1 firewood a salt** (10 kg) | at the new unit, today's ratio is real (L-110) |
| salt pan (saltmarsh) | | | 1 a unit (kept) | 1 | | summer |
| charcoal | stacking and tending about 1 to 2 hours for 20 kg [n building_clock §1.3] | est. | **1 unit** | 2 | 5 timber (125 kg) | burns 1 night |
| smelt | a small furnace run of 6 to 10 hours for 1 to 5 kg of copper [e] | est. | 3 units (kept) | 3 | 3 ore, 1 charcoal (20 kg), or 5 timber | for part 2 |
| leach acorns | about 1 kg an hour shelled, ground and leached [e] | est. | 1 unit for 3 (kept) | 1 | | |
| cheese | 1 to 2 hours of active work for a batch of 10 to 20 kg of milk [e] | est. | 1 unit for 20 milk and 0.6 salt | 1 for 6 | | for part 2 (the herder's) |
| tallow lights | dips at dozens an hour [k] | | 1 unit for 5 | 1 for 4 | 1 tallow | |
| ★ snares, a bundle of 25 | about 10 minutes a snare with the cord in hand [n fibre_and_cord §3] | est. | **2 units** | the set costs nothing [m `wild.set_work`] | 0.1 to 0.15 cord | each snare lasts 3 to 10 settings: under a handful at 1/7 |
| ★ bone hooks, 5 | under an hour each with a metal knife [n withies_wood_materials §1.8] | est. | **1 unit for 5** | (new) | 0.05 bone | lost or broken in 10 to 30 uses: a handful at 1/7 |
| ★ arrows | 1 to 2 hours each by hand [n hunting_ladder §1.3] | est. | **1 unit for 2** | (new) | withies 0.05 each, a head of bone 0.01, feathers (folded in) | lost or broken in 5 to 10 shots: day clock |
| a camp (lean-to and fire ring) | 3 to 5 hours [n building_clock §1.1] | est. | **2 units** | 1 | **3 timber** (75 kg of poles and brush) | lasts 10 nights (D2-68) |

### 3.2 Gear, tools and weapons (capital: real hours × f)

Lives are at 1/7 (at 1/15 a use-counted life is 7/15 of the figure, so a use costs the same).

| Item | Real hours | Source | 1/7 | 1/15 | Engine now [m] | Materials (new units) | Life (count) | Upkeep |
|---|---|---|---|---|---|---|---|---|
| crude tool | 4 to 10 | est. [n building_clock §1.2] | 0.3 to 0.7: **1 for 2** | **1 for 4** | 1 unit; 1 timber, 0.5 stone; 10 uses | 0.04 timber, 0.04 stone each | real 300 to 1,000 hours of use: **20 to 70 acts** | |
| copper tool | 4 to 8 beyond the metal | est. | 0.3 to 0.6: **1 for 2** | 1 for 4 | 3 units at an anvil; 1 copper, 0.5 timber; 40 | 1 copper, 0.02 timber | 1,000 to 3,000 hours: **70 to 210 acts** | |
| crude weapon | 2 to 4 | est. | **1 for 3** | 1 for 6 | 1 unit; 1 timber; 10 | 0.06 timber | 50 to 150 uses: **7 to 21** | |
| ★ spear (copper head) | 2 to 4 (a smith's hour or two, and a shaft) | est. [n hunting_ladder] | 1 (floor) | 1 for 2 | | 0.5 copper, 0.08 timber | 200 to 500 uses: 30 to 70 | |
| ★ bow | 8 to 16 to tiller and finish | est. [n hunting_ladder §1.3] | **1** | 1 for 2 | | 0.1 timber (a stave), 0.02 cord (the string) | 300 to 500 hunts: **40 to 70**; the string every 7 to 14 | the stave seasons 8 to 32 nights first |
| fishing rod | 1 to 2 | est. | **1 for 5** | 1 for 10 | 1 unit; 0.5 timber, 0.1 hide; 30 | 0.1 withies (1 kg) | 150 to 300 uses: **20 to 45** | |
| ★ hand line | 1 to 2 | [n fibre_and_cord §3] | **1 for 5** | 1 for 10 | | 0.02 cord, hooks | 30 to 100 uses: 4 to 14 | |
| ★ set line (20 to 50 hooks) | about a day, 8 to 10 | [n fishing_ladder] | **1** | 1 for 2 | | 0.3 cord, 30 hooks | a season of 50 to 100 sets: 7 to 14 | hooks lost and replaced |
| ★ copper hooks, 10 | 2.5 to 5, a smith | est. | **1** | 1 for 20 | | 0.05 copper | 30 to 100 uses: 4 to 14 | |
| ★ leister, eel glaive | 2 to 4 | [n fishing_ladder] | 1 (floor) | 1 for 2 | | 0.5 copper (tines), 0.08 timber | years: 40 and more | |
| ★ **wicker trap** | 4 to 8 | [n withies_wood_materials §1.2] | 0.3 to 0.6: **a line of 6 for 3** | **6 for 1** | the set costs nothing | 0.45 withies each | 200 to 300 sets with repair: **30 to 45** (the proposal's 30) | spate and flood wrecks (kept) |
| ★ **fish net** (gill, 20 m by 1.5 m) | 40 to 60 beyond the cord | [n fibre_and_cord §3] | **3 to 4** | 1.5 to 2 | (the proposal's 30) | 1 cord, 0.1 stone (sinkers) | 200 to 450 sets: **30 to 65** | mending 10 to 20% of the netting time a season [n fibre_and_cord]: about 0.5 a world year; barking a few kg of bark |
| ★ fowling net (clap, 10 m by 2 m) | 50 to 70 | [n fibre_and_cord §3] | **4 to 5** | 2 | (the proposal's 30) | 0.8 cord, 0.1 timber (poles) | as the net: 30 to 60 | as the net |
| ★ dip or hoop net | 3 to 4 | [n fibre_and_cord §3] | **1 for 2** | 1 for 4 | | 0.1 cord, 0.2 withies | 100 to 300 uses: 15 to 45 | |
| ★ seine (later) | about 500 | [n fibre_and_cord §3] | **36** | 17 | | 10 cord, 0.5 stone | 2 to 4 years of use: 30 to 90 | as the net |
| ★ creel | 4 to 8 | [n withies_wood_materials §1.2] | **1 for 2** | 1 for 4 | (the proposal's 1) | 0.25 withies | years (time): 3 to 5 world years | |
| ★ **withy pack basket** (D2-281) | 6 to 10 | est. [n building_clock §1.2] | **1** | 1 for 2 | pack: 1 unit; 1 hide, 1 timber; no life | 0.4 withies, 0.1 hide (straps) | wears faster: **2 to 3 world years** | |
| ★ **leather-strapped frame** (D2-281) | 6 to 12 | est. | **1** | 1 for 2 | | 0.1 timber, 0.5 leather | **5 to 10 world years** | restrap 0.2 leather |
| ★ **hurdle** | 2.7 to 3.2 | [n withies_wood_materials §1.2: 2.5 to 3 hurdles a day] | 0.2: **5 for 1** | **10 for 1** | (the proposal's 1.5) | 1 withies each | 5 to 10 world years dry | |
| harness (a yoke and traces) | 9 to 18 | est. [n building_clock §1.2] | **1** | 1 | 2 units; 2 timber, 1 hide; 80 days | 0.4 timber, 1.5 leather (or 0.5 hide as rawhide) | 500 to 1,000 working days: **70 to 140** | |
| wooden plough (an ard, a copper share) | 27 to 45 | est. | **2 to 3** | 1 to 1.5 | 4 units; 4 timber, 1 copper; 60 plots | 1.2 timber, 1 copper | 600 to 1,500 hours of ploughing: **11 to 27 plots** | |
| handcart | 27 to 72 | est. | **2 to 5** | 1 to 2.5 | 3 units; 6 timber; no life | 2 timber (50 kg) | **5 to 10 world years** | |
| bedroll | 2 to 4 | est. | **1** | 1 for 2 | 1 unit; 1 hide; 40 nights | 0.5 hide (dried) | 200 to 500 nights: **18 to 44 nights** (×1/11.4) | |
| tent | 6 to 12 | est. | **1** | 1 | 2 units; 3 hide, 2 timber; 30 nights | 1.5 hide, 0.4 timber | 200 to 500 nights: **18 to 44 nights** | |
| clappers | 1 to 2 | est. | **1 for 5** | 1 for 10 | 1 unit; 0.5 timber | 0.02 timber | years | |
| horn | 4 to 8 | est. | **1** | 1 for 2 | 2 units; 1 antler | 1 antler | years | |
| ★ keep box | 8 to 10 | [n fishing_ladder] | **1** | 1 for 2 | | 1 withies | 2 to 3 world years | |
| ★ coracle (later) | 24 to 30 | [n fishing_ladder] | **2** | 1 | | 3 hide (a cow's), 2 withies | a few world years | re-pitch (later) |

### 3.3 Containers (the store's fit-out, D2-279)

| Container | Holds | Real hours | Source | 1/7 | 1/15 | Materials | Life (time) | Protects (§2.3) |
|---|---|---|---|---|---|---|---|---|
| sack | 50 kg of dry goods; 12 a space | 3 to 5 beyond the cord | [n storage §3.2] | **1 for 3** | 1 for 6 | 0.6 cord | 3 world years | floor damp halved; vermin 0.8 / 0.7 |
| basket | 25 kg of roots, nuts, fruit, eggs, dried and smoked goods, cheese; 10 a space | 4 to 8 | [n storage §3.3] | **1 for 2** | 1 for 4 | 0.3 withies | 2 world years | the heap; vermin 0.8 / 0.7 |
| chest or ark | 400 kg of dry goods; 1 a space | 18 to 27, a carpenter | [n storage §3.4] | **2** | 1 | 4 timber (100 kg of boards) | 30 world years | floor damp; vermin 0.2 / 0.15 |
| barrel | 120 kg, or salt goods in brine; 4 a space | 8 to 11, a cooper (one a day) | [n storage §3.6] | **1** | 1 for 2 | 7 timber (stave bolt), 0.3 withies (hoops) | 10 world years | brine; flies; damp; vermin 0.05 |
| (crock) | 20 kg | | [n storage §3.5] | deferred until clay | | | | |

### 3.4 Fittings

| Fitting | Real hours | Source | 1/7 | 1/15 | Engine now [m] | Materials (new units; kg) | Life | Upkeep |
|---|---|---|---|---|---|---|---|---|
| hearth | 9 to 18 | est. [n building_clock §1.1] | **1** | 1 | 3 units; 4 stone | 20 stone (0.5 t) | decades (time) | |
| fire ring | 1 to 4 | est. | **1** | 1 | 1; 1 stone | 4 stone (100 kg) | years | |
| owl hole | 1 to 4 | est. | **1** | 1 | 1; 1 timber | 0.1 timber | years | |
| bins (boarded, built in; 300 kg) | 9 to 18 | est.; [n storage §3.4] | **1** | 1 | 1; 3 timber; holds 60 food | 3 timber (75 kg) | 10 world years | |
| granary floor (boarded loft; 1,200 kg) | 27 to 45 | est. | **2 to 3** | 1 to 1.5 | 4; 6 timber; holds 300 | 20 timber (0.5 t of joists and boards) | 20 to 30 world years | |
| hand mill (quern) | 18 to 45 | est. | **1.5 to 3** | 1 to 1.5 | 2; 2 stone | 2 stone (50 kg; a real pair is 30 to 60 kg [k]) | decades | |
| oven (stone) | 36 to 72 | est. | **3 to 5** | 1 to 2.5 | 12; 20 stone, 2 timber; lining 10 firings | 60 stone (1.5 t of stone and clay daub) [e], 0.4 timber | shell: decades; lining: real 200 to 500 firings, **30 to 70 firings** | reline: 1 unit, 4 stone |
| anvil and bellows | 27 to 45 | est. | **2 to 3** | 1 to 1.5 | 4; 6 stone, 2 hide, 1 timber | 4 stone, 2 leather (the bellows: D2-281), 0.4 timber | years; the bellows' leather a few | |
| cellar, timber-lined | 30 to 52 a space of footprint | [n storage §3.11: 20 to 35 days under 30 m²] | **2 to 4 a space** (12 to 22 under a cottage) | 1 to 1.7 a space | 6 flat; 4 stone | 1.5 timber a space | 10 world years (the lining rots) | |
| cellar, stone-lined | 60 to 105 a space | [n storage §3.11: 40 to 70 days] | **4.5 to 7.5 a space** (26 to 45 under a cottage) | 2 to 3.5 a space | | **190 stone a space** (4.7 t; 28 t under a cottage) | decades | |
| millstones | 180 to 360 | est. | **13 to 26** | 6 to 12 | 10; 10 stone; dressed every 2,000 grain | 60 stone (1.5 t; a pair 1 to 2 t [e]) | dress every 1,400 to 3,600 grain (real 10 to 25 t × 1/7) [e] | dress: 1 unit |
| water wheel and leat | 1,440 to 4,680 | est. | **100 to 330** | 48 to 156 | 250; 60 timber, 20 stone, 2 copper | 200 to 400 timber (5 to 10 t), 80 to 200 stone, 2 copper [e] | the leat silts in a year (time) | clear the leat: 2 to 6 units a year (real 3 to 10 days) |
| stalls (each) | 4 to 9 | est. | **1** | 1 for 2 | 1; 1 timber | 2 timber | 10 world years | |
| beds (each) | 4 to 9 | est. | **1** | 1 for 2 | 1; 1 timber, 2 straw | 1 timber, 1 straw (a truss) | 10 world years; the straw renewed yearly | 1 straw a year |
| woodshed (holds 9,600 kg) | 18 to 36 | est. | **1.5 to 2.5** | 1 | 1; 2 timber | 20 timber (posts and a roof of 0.5 t), 15 straw (thatch) | 15 to 20 world years | |
| brine pan | 18 to 36 | est. | **1.5 to 2.5** | 1 | 4; 1 copper, 2 timber; 60 boilings | **10 copper** (a pan of 10 to 30 kg [e]), 4 stone (the furnace) | real 300 to 600 boilings: 40 to 90 | mend: 0.25 copper |
| vault | 900 to 1,800 | est. | **64 to 129** | 30 to 60 | 30; 40 stone | about 3,000 stone (75 t of a vaulted stone room) [e] | centuries | |
| smoke loft (hooks in the roof) | 2 to 4 | [n storage §3.12] | **1** | 1 | (new) | 0.2 timber | years | |
| carved post | 18 to 45 | est. | **1.5 to 3** | 1 to 1.5 | 2; 2 timber | 2 timber | decades | |
| standing stone | 18 to 45 with a crew | est. | **1.5 to 3**, crew 4 | 1 to 1.5 | 4; 4 stone | one stone of its own (1 to 5 t): **not a count of stone** | centuries | |
| cairn | 6 to 12 | est. | **1** | 1 | 3; 6 stone | 80 to 240 stone (2 to 6 t, gathered on the spot) | centuries | |

### 3.5 Rooms and buildings

Materials are real (the room of storage.md §11: 30 m² of floor, about 44 m² of wall, a roof of 40 to 50 m² with its eaves). The thatch
is long straw at about 27 kg a m²: about 150 bundles make a tonne and cover about 37 m² [s: East Anglian thatchers' guidance, via
search]. Storage.md's proposal halved the straw (400 kg, "a factor of about 0.5, named"); here it is real. Daub is about 4 m³ of
earth dug and mixed on the spot: its work is in the hours, and it is no good.

| Room | Real hours | Source | 1/7 | 1/15 | Engine now [m] | Materials (new units) | Total | Life | Upkeep |
|---|---|---|---|---|---|---|---|---|---|
| **small room, wattle** (6 spaces) | 270 to 540 | [n building_clock §1.1, storage §4: 30 to 60 days] | **19 to 39** | 9 to 18 | 6 units; 8 timber | **36 timber** (0.9 t of posts and poles), **35 withies**, **75 straw** (1.2 t) | 2.5 t | 20 to 40 world years [k: peasant houses rebuilt about each generation] | 2 to 3 units a year, 1 withies and 2 straw a level; rethatch every 10 to 20 years: 4 to 7 units and 75 straw [e] |
| **small room, timber** (a frame on a stone sill, wattle panels) | 450 to 720 | [n building_clock §1.1] | **32 to 51** | 15 to 24 | 6; 8 timber, 2 stone | **160 timber** (3 to 5 t of green oak [n storage §11]), **60 stone** (a sill of 1 to 2 t), 15 withies, 75 straw | 5.5 to 8.5 t | centuries with upkeep | 1 timber a level (as now) |
| **small room, stone** | 630 to 1,260 | [n building_clock §1.1] | **45 to 90** | 21 to 42 | 40; 30 stone, 4 timber, mason | **1,600 stone** (40 t [n storage §11]), 40 timber (the roof, 1 t), 75 straw | 42 t | centuries | 1 stone a level; rethatch as wattle |
| medium room, timber (12 spaces) | 720 to 1,350 | [n building_clock §1.1] | **51 to 96** | 24 to 45 | 15; 15 timber, 4 stone | x1.7 of the small [n storage §11]: 270 timber, 100 stone, 25 withies, 130 straw | 9 to 14 t | | |
| medium room, stone | 1,080 to 2,250 | [n building_clock §1.1] | **77 to 160** | 36 to 75 | 90; 60 stone, 8 timber | 2,700 stone, 70 timber, 130 straw | 72 t | | |
| hall, timber (30 spaces) | 3,600 to 8,100 | [n building_clock §1.1] | **257 to 579** | 120 to 270 | 200; 80 timber, 20 stone | x3.5: 560 timber, 210 stone, 50 withies, 260 straw | 20 to 30 t | | |
| hall, stone | 5,400 to 10,800 | [n building_clock §1.1] | **386 to 771** | 180 to 360 | 250; 150 stone, 20 timber | 5,600 stone, 140 timber, 260 straw | 150 t | | |
| ★ **hut room, wattle** (2 spaces: the smoke hut's) | 90 to 180 | est.: a third of a small wattle room | **6.5 to 13** | 3 to 6 | (none) | 12 timber, 16 withies, 30 straw (about 18 m² of roof) | 0.95 t | 10 to 20 world years | as wattle |
| ★ granary on staddles (a raised small timber room) | 500 to 800 | est.: a small timber room, 9 staddles and a tight floor | **36 to 57** | 17 to 27 | (new; storage.md priced it at the old scale) | 170 timber, 60 stone (9 staddles of 150 to 200 kg), 75 straw | 6 to 9 t | centuries | |
| ★ barn (later) | as a medium timber room | [n storage §3.8] | as medium | | | | | | |
| ★ hay rick | 27 to 36 (a team of four for a day) | [n storage §3.9] | **2 to 2.5** | 1 | (new) | 1 straw a tonne of hay to thatch it | a year (time) | |
| ★ root clamp | 8 to 10 | [n storage §3.10] | **1** | 1 | (new) | 1 straw a tonne of roots | a winter | |
| ★ sealed grain pit | 8 to 10 | [n storage §3.16] | **1** | 1 | (new) | 1 straw (the seal) | dug once, refilled for years (time) | must be emptied once opened |
| camp | | | | | 1 | (day clock: §3.1) | | | |

**Builders as a trade** (proposals/building_clock.md): a master builder takes about half these units, and a novice of a trade
(D2-52's 0.5) about twice.

### 3.6 The smokehouses, as revised

The brief sets the loads: a wattle smoke hut holds one set of racks of about 250 fish; a timber or stone smokehouse holds several
tiered sets, about 750 to 1,000 fish in all. This is smaller than storage.md §11's 500 and 1,500, which put 250 fish on a space and
2 spaces to a set.
- A real hut of 7 to 10 m² held about 210 to 500 kg at 30 to 70 kg a m² [n smokehouse_capacity §2].
- One set of about 250 fish on one space (5 m², 50 kg a m²) is the middle of that range [n].
- A tiered set in a timber house stacks racks to the roof.

| Part | Real hours | Source | 1/7 | 1/15 | Materials (new units) | Holds | Life | Risk |
|---|---|---|---|---|---|---|---|---|
| **a set of smoke racks** (two hurdles over a frame of poles, rails) | 6 to 10 | [n withies_wood_materials §3.4] | **1** | 1 | **2 withies, 2 timber** (50 kg of frame poles; the withies note's "1 timber" was a 240 kg one) | about **250 fish** on 1 space | 5 world years (rot) | burns with the house |
| **a tiered set** (taller frame, three tiers of rails) | 10 to 14 | est. | **1** | 1 | 3 withies, 3 timber | about 250 fish on 1 space, hung higher | 5 world years | |
| **wattle smoke hut** (D2-271): a hut room and one set | 96 to 190 | as its parts | **7 to 14** | 3 to 6 | 12 timber, 18 withies, 30 straw | **250 fish** | 10 to 20 world years | hot and keeping smokes; can burn with its batch (PHYSICS `smokehouse.fire` wattle 0.02 a night burning [m]) |
| **timber smokehouse**: a small timber room and 3 to 4 tiered sets | 480 to 776 | as its parts | **35 to 55** | 17 to 26 | 169 to 172 timber, 60 stone, 24 to 27 withies, 75 straw; a carpenter | **750 to 1,000 fish** on 3 to 4 spaces; 2 spaces to work, hang and keep the fire | centuries; the racks 5 years | all three smokes; seldom burns (0.008 [m]) |
| **stone smokehouse**: a small stone room and 3 to 4 tiered sets | 660 to 1,316 | as its parts | **48 to 94** | 22 to 44 | 1,600 stone, 49 to 52 timber, 9 to 12 withies, 75 straw; a mason | 750 to 1,000 | centuries | all three; almost never burns (0.0003 [m]) |

**What a full house takes to run** (§3.1's rates):
- **Hanging:** 250 fish is about 8.5 units; 1,000 fish is about 33 units (two people for two to three days).
- **Fuel for a keeping smoke:** 25 to 50 firewood for 250 fish (250 to 500 kg); 100 to 200 for 1,000.
- **Tending:** 1 unit a night.

A run's glut is then bound by hands, wood and the number of houses, as in reality [n smokehouse_capacity §6]. The racks' own hold
needs to be a number of the fitting (`holds`), not the technique's batch [n smokehouse_capacity §8].

### 3.7 Works on land and water

| Work | Real hours | Source | 1/7 | 1/15 | Engine now [m] | Materials (new units) | Life | Upkeep |
|---|---|---|---|---|---|---|---|---|
| **hurdle fence, per 100 m** | about 190 (56 hurdles at 3 a day, stakes driven) | [n storage §4; withies_wood_materials §1.2] | **13.5** | 6.3 | 4 timber, 10 units × √size, a close charged as a field (`fence_need` floors the size at 1) | 56 withies (the hurdles), 13 timber (112 stakes of 3 kg) | 5 to 10 world years | D4-114: a quarter of the build a year; real hurdles last 5 to 10 years, so 10 to 20% a year: **1.4 to 2.7 units per 100 m** |
| a close of 0.2 ha (180 m) | about 340 | [n storage §4] | **24** | 11 | about 3 to 10 | 100 withies, 24 timber | as above | 2.5 to 5 a year |
| a field of 2 ha (566 m) | about 1,080 | [n storage §4] | **77** | 36 | 10 | 315 withies, 75 timber | as above | 8 to 15 a year |
| ★ dead hedge, per 100 m (stakes and brushwood) | 22 to 45 | est. [n building_clock §1.1: 20 to 40 m a day] | **1.6 to 3.2** | 0.75 to 1.5 | (new) | 1 to 2 t of brush cut on the spot (the cutting is in the hours) | 2 to 3 world years | rebuilt |
| **dry-stone wall, per 100 m** | 150 to 300 (3 to 6 m a day) | [n storage §4] | **11 to 21** | 5 to 10 | 8 stone, 20 units × √size, mason | **4,000 to 8,000 stone** (100 to 200 t: 1 to 2 t a metre [n storage §4]) | keeps | little |
| clearing turf to field (a unit of size) | 54 to 90 | est. [n building_clock §1.1] | **4 to 6.5** | 2 to 3 | 6 | | | |
| clearing scrub to field | 360 to 900 | est. | **26 to 64** | 12 to 30 | 10 | brash as firewood | regrowth if left | |
| clearing for building | as turf | est. | 4 to 6.5 | 2 to 3 | 4 (scrub 10) | | | |
| ditching wet ground | 180 to 360 | est. | **13 to 26** | 6 to 12 | 40 | | silting | 1.5 a year (kept) |
| terracing a hillside | 1,800 to 3,600 | est. | **129 to 257** | 60 to 120 | 60, 6 stone | the slope's own stone | slumping | 1.5 a year |
| ★ **withy bed** (200 m²) | about 18 to 24 (840 cuttings, two days' digging) | [n withies_wood_materials §3.3] | **1.5** | 1 | (the proposal's 10) | 1 withies (the cuttings) | 30 years | a fence or hurdles against beasts (31 hurdles round 56 m) |
| ★ **retting pit** | 18 to 45 | est. [n building_clock §1.1] | **1.5 to 3** | 1 to 1.5 | (the proposal's 10) | | silting: 10 world years | |
| ★ **tan pits** (3 to 5 pits by water, lined) | 30 to 60 | est. | **2 to 4** | 1 to 2 | (new) | 4 timber (planks or wattle), clay puddled on the spot | 20 world years | |
| ★ flax close | the farming verbs | | | | | | | manure |
| **weir: an added wattle section** | about 21 | [n withies_wood_materials §3.4] | **1.5** | 1 | 16 units, 6 timber | 12 withies, **7 timber** (25 stakes of 5 to 8 kg) | floods (wattle wear 1.0) | D2-210: about a third to a half of a section a year: **6 withies, 0.5 to 0.8 units** |
| weir: the first section, at the research note's size | 36 to 51 | [n building_clock §1.1] | **2.6 to 3.6** | 1.2 to 1.7 | 24 units, 12 timber | 14 withies, **40 timber** (heavy posts across the river, about 1 t) | floods | as above |
| weir: the first section, sized to take 30% of a large river's run | 150 to 500 | est. [n building_clock §1.1] | **11 to 36** | 5 to 17 | | about 3 to 10 times the above | floods | |
| weir: a timber section | 30 to 50 | est. | **2 to 3.5** | 1 to 1.7 | 25, 10 timber | 40 to 80 timber (1 to 2 t) | floods (wear 0.5) | |
| weir: a stone footing | 45 to 135 | est. | **3 to 10** | 1.5 to 4.5 | 15, 10 stone | 200 to 600 stone (5 to 15 t) | floods (wear 0.1) | |

### 3.8 Upkeep, together

| Thing | Real upkeep | Source | 1/7 | 1/15 |
|---|---|---|---|---|
| a wattle cottage | 3 to 5 days a year (daub, thatch patched) | est. | 2 to 3 units a year (PHYSICS `repair`: 1 unit and 1 timber per 4 spaces a level, at least 2 [m]; in range) | 1 to 1.5 |
| rethatching a small room (long straw) | every 10 to 20 years [k]; 60 to 100 hours | est. | 4.3 to 7 units and 75 straw, every 10 to 20 world years | 2 to 3.3 |
| a hurdle fence, per 100 m | 10 to 20% of its build a year | est. | 1.4 to 2.7 | 0.6 to 1.3 |
| a weir section | a third to a half of a section a year | D2-210 | as §3.7 | |
| a net | mending 10 to 20% of its netting time a season | [n fibre_and_cord §2] | about 0.5 a world year | 0.25 |
| an oven | a relining each 30 to 70 firings | above | 1 unit and 4 stone | 1 |
| millstones | a dressing each 1,400 to 3,600 grain | above | 1 unit | 1 |
| a leat | clearing yearly, 3 to 10 days | est. | 2 to 6 | 1 to 3 |

---

## 4. Carrying

### 4.1 The limits, against real loads

The limits apply on the road (`World.capacity`). Inside a village nothing is capped, and moving goods between buildings is labour
(store_rules.md: about 1 unit per 800 kg a parcel step, a quarter on the same parcel, a handcart three times a trip, a pack ox six;
provisional, D2-274) [m; n 02zzv §1].

| Means | Engine now [m] | Real | Source | Proposed (kg) |
|---|---|---|---|---|
| on foot (in the arms, a bundle on the shoulder) | 10 | about 15 to 20 kg over a day's walk with no carrier [e]; "a person carries about 20 to 25 kg" with something to carry it in [n hunting_ladder §2.3] | est. | **10, kept as a named departure** (about x0.5 to x0.7) |
| a creel | (new) | fish and small goods | [n hunt_fish_materials §5] | **+5**, for fish and small goods only |
| **the withy pack basket** (D2-281) | the pack: +10 | 25 to 30 kg with a basket [n hunt_fish_materials §5; W-71] | sourced (sec.) | **+15** (25 in all) |
| **the leather-strapped frame** (D2-281) | | a frame carries more and lasts longer | D2-281 | **+20** (30 in all) |
| a handcart (on a track) | 40 in all | 100 to 150 kg pushed on a track [e] | est. | **120** |
| a pack ox, led | 60 | a pack pony carried about 110 kg in two panniers [s: Packhorse, Wikipedia, via search]; medieval wool packs were smaller than the modern 80 kg [s: Fell Pony Museum, via search]; an ox about the same as a pony [e] | sourced and est. | **100** |
| an ox cart (later) | 300 to 400 | a cart load was 36 trusses, 18 cwt (about 900 kg) [s: an 1834 account quoted under Truss (unit), via search] | sourced | **800 to 900** |

### 4.2 What a carry holds, in the new units

| Good (kg a unit) | On foot (10) | Basket (25) | Frame (30) | Pack ox (100) | Cart (900) |
|---|---|---|---|---|---|
| grain, fish, meat, salt (1) | 10 | 25 | 30 | 100 | 900 |
| firewood, hay, withies, bark (10) | 1 | 2 | 3 | 10 | 90 |
| straw (16, the truss) | 0 | 1 | 1 | 6 | 56 (36 by bulk, the cart load [s]) |
| timber, stone (25) | 0 | 1 | 1 | 4 | 36 |
| a hurdle (10) | 1 | 2 | 3 | 10 | |
| wicker traps (2.5) | 4 | 10 | 12 | 40 | |
| a fisher's gear: a net (4) and six traps (15) | no | yes, with 6 kg to spare | yes | | |
| a red deer's meat (33 units, about 40 kg of venison) | no | no | no: about three quarters | yes | |

A hunter alone brings home 10 to 30 kg of a red deer: the carry, with keeping, binds the hunt [n hunting_ladder §2.3].

### 4.3 What a building's materials cost to carry

Three rates for comparison:
- **The provisional rate** (store_rules.md): 1 unit per 800 kg a parcel step.
- **By hand, real:** 25 kg loads over a step of about 200 m, about 7 minutes a round trip loaded and empty, so about 8 trips and 200
  kg an hour, about 400 kg a unit a step [e]. A parcel of a unit of size (about 2 ha) is about 140 m across [m, 02z basis]. The
  provisional rate is about twice the hand rate: a named departure, near a sledge's rate.
- **Between villages (an edge is a day):** a carrier with a frame (30 kg), a pack ox (100) or a cart (900), for each trip.

| Work | Materials (kg) | Units a parcel step (provisional) | Build at 1/7 | Carrying as a share of the build, a step | Trips between villages: frame / ox / cart |
|---|---|---|---|---|---|
| a hurdle fence, 100 m | 0.9 t | 1.1 | 13.5 | 8% | 30 / 9 / 1 |
| a wattle smoke hut | 0.95 t | 1.2 | 7 to 14 | 9 to 17% | 32 / 10 / 1 |
| a set of racks | 70 kg | 0.1 | 1 | 9% | 3 / 1 |
| an added weir section | 0.3 t | 0.4 | 1.5 | 25% | 10 / 3 / 1 |
| **a wattle cottage** | 2.5 t | 3.1 | 19 to 39 | **8 to 16%** | 83 / 25 / 3 |
| **a timber small room** | 5.5 to 8.5 t | 6.9 to 10.6 | 32 to 51 | **14 to 33%** | 180 to 280 / 55 to 85 / 7 to 10 |
| a timber smokehouse | 6 to 9 t | 7.5 to 11 | 35 to 55 | 14 to 31% | |
| **a stone small room** | 42 t | 52 | 45 to 90 | **58 to 117%** | 1,400 / 420 / 47 |
| a stone-lined cellar under a cottage | 28 t | 35 | 26 to 45 | 78 to 135% | |
| **a dry-stone wall, 100 m** | 100 to 200 t | 125 to 250 | 11 to 21 | **6 to 20 times** | |
| a water wheel and leat | 7 to 15 t | 9 to 19 | 100 to 330 | about 6% | |

**Where carrying binds.**
- **Not wattle:** carrying adds a tenth to a sixth a parcel step. Withies and poles come from nearby wet ground and coppice.
- **Timber framing:** a fifth to a third a step, more from a far wood. Between villages it is 180 to 280 carriers' trips, or 7 to 10
  carts.
- **Stone:** carriage is as much again as the building, or more. A stone house goes up next to its quarry, or on stony ground.
- **Walls:** the stone has to lie where the wall goes: field stone from clearing and hoeing (`hoe` already yields stone [m]). This
  is the real pattern. In medieval building accounts carriage often cost as much as the stone [k: Salzman, *Building in England*];
  the lowland fenced with hedges and hurdles, and walls belong to stony uplands [k].
- **The road:** no building's materials cross an edge on foot. Timber and stone between villages move only by ox or cart.

### 4.4 Timber: carried as poles, or worked where it is felled

Both, by size:
1. **Poles for wattle, fences, racks, stakes and the weir's wattle** come from coppice and young growth (`cut poles`, §3.1) as
   25 kg lengths. They are shouldered or basketed within the village and dragged by an ox from a far wood.
2. **Framing timber is hewn at the stump.** `fell` gives hewn lengths, and the slab, sapwood and brash stay in the wood as firewood
   and dead wood (02z's brash rule). Squaring a log leaves about half to two thirds of its mass [e], so the hewing saves a third to
   a half of the haul.
   - Real builders felled every tree a house needed at once, from one wood or adjacent ones, and used the oak green [s: a
     dendrochronology source via search]. Seasoning a frame member of 150 to 200 mm would take six to eight years [s: Forestry
     Commission Scotland, *Green oak in construction*, via search].
   - Rackham found that the Cressing Temple barley barn's 600 timbers came from about 480 mostly small oaks [s: Robin Wood's blog on
     Rackham, via search].
   - So a village's houses come from its own wood, and a building's timber is a felling in that wood, not a trade good.
3. **Hauling:** an ox led with a harness drags a sledge or a log. Store_rules' "a pack ox six times a trip" (about 4.8 t a unit a
   step) is generous: real oxen snig about 0.5 to 1 t a pull [e]. Keep it for now, named.
4. **What it gives the design:** the village's own wood becomes a chokepoint for building (scenario_design.md); a village without
   wood buys hewn timber delivered by cart, or builds in wattle. This hands straight to the timber economy (W-76).

---

## 5. Consistency checks

### 5.1 A household's year against what it must make and mend

Two adults, 384 units a world year. All at 1/7, with the lives of §3 [e from §3's rows].

| Item, a world year | Fishing household: flax cord, a withy bed | Fishing household: wild cord, wild willow | Farming household: a fenced close, a plough |
|---|---|---|---|
| a net (half a net a year: 1.8 units of netting and 0.5 kg of cord) | 5.8 (cord at 8 units a kg) | 14.3 (cord at 25) | |
| mending the net | 0.5 | 0.5 | |
| traps (4 a year replaced, at 0.43 units each, with their withies) | 2.2 | 2.9 | |
| lines and hooks | 1 | 1 | |
| snares (a bundle a year and its cord) | 3.2 | 5.8 | |
| tools and a weapon | 1.3 | 1.3 | 2.3 (4 tools a year) |
| a plough (every 1 to 2 years) and harness | | | 2.2 |
| the close's fence (10 to 20% of 24 units) | | | 3.6 |
| the house: upkeep 2.5, rethatching 0.4, rebuilding a share 1.0 | 3.9 | 3.9 | 3.9 |
| the smoke hut and racks (a share of 15 years) | 0.9 | 0.9 | |
| containers (sacks, baskets) and stores | 1 | 1 | 1.3 |
| the bed's hurdles (a share) | 0.3 | | |
| **making and mending** | **20 (5%)** | **32 (8%)** | **13 (3.5%)** |
| fuel for the hearth (48 bundles at 3 to 5 a unit) | 10 to 16 (3 to 4%) | 10 to 16 | 10 to 16 |
| fuel for smoking 500 fish (50 to 100 bundles) | 10 to 33 (3 to 9%) | 10 to 33 | |
| **with fuel** | **40 to 70 (10 to 18%)** | **52 to 81 (14 to 21%)** | **23 to 29 (6 to 8%)** |

**Reading.**
- Making and mending alone is 3 to 8% of the year, below the network proposal's 10 to 20% (§13). That target was set on its own gear
  prices (a net 30 units, a trap 2.5, a hurdle 1.5), which D2-276 replaces. With the fuel a keeping household cuts, the fishing
  households land at 10 to 21%.
- Real making and mending of tools, gear, houses and fences was perhaps 5 to 10% of a household's work, **excluding textiles**,
  which took a large share of women's time (spinning above all) [k; n fibre_and_cord §5]. Clothing is parked (D2-10).
- So the engine's share is near real for what it contains, and the proposal's target should be read with fuel included, or with
  clothing once it exists.
- The wild-cord household spends about 12 units more than the flax household, the difference §4.2 of the proposal wants: about
  three days of one person's year, not a third of it (the proposal's "an eighth to a third" was on the old making prices).
- **Building lumps:** a wattle cottage is 19 to 39 units with about 2.5 t of materials, and a timber room 32 to 51 with 5.5 to 8.5 t.
  For one adult that is 3 to 10 days, a couple's week or two, plus carrying (§4.3).

### 5.2 Food a unit of work, by method: unchanged by this part

This part changes no rate per hour of taking. The calibration targets (network proposal §13; 02zzu) stand:

| Method | Food a unit of work (target) | What part 1 changes around it |
|---|---|---|
| plough farming | 2.4 to 2.8 | flour keeps about 10 nights: grind as needed (§2.2); straw now real for thatch (§1.2) |
| hands at the edge, line fishing | 0.1 to 0.5 | gear nearly free: a rod at the floor, a line batched |
| set gear and snares off a run | 0.4 to 2 | a trap's making falls from 2.5 units to about 0.5; snares on the day clock |
| set gear and the weir on run nights | 5 to 18 for a few nights | keeping binds harder: fresh fish 1.5 nights, the keeping smoke 10 nights; salting at 40 a unit in place of 4; hanging 30 a unit |
| hunting: novice / capable / master near / master far | 0.08–0.3 / 0.4–1.2 / 1.2–3.2 / 3–6 | the carry (§4.2); dressing a kill 1 unit; fresh meat 2.1 nights |
| fowling | 0.24 to 2.2 | the fowling net 4 to 5 units in place of 30 |

**What moves is food eaten a unit of work, not food taken:**
- Gear's share of a unit of fishing falls from about 5 to 10% (on the proposal's prices) to about 1 to 3%. This raises net food
  slightly.
- Faster spoiling of fresh and kept foods lowers what a glut feeds unless it is salted or hard-cured. This is the binding the
  network wants: "the stocks and the keeping, not the hourly rates" (§13).

### 5.3 What falls below the 1-unit floor (batch it)

**The code needs two things:**
- `verbs.cost` floors at 1, in place of `int()`, which makes anything under a unit free [m].
- Each batch is a recipe's `gives` quantity.

| At 1/7 (a unit gives) | At 1/15 (a unit gives) |
|---|---|
| crude tool 2; copper tool 2; crude weapon 3; fishing rod 5; hand line 5; clappers 5; hurdles 5; wicker traps 2 (a line of 6 for 3); creels 2; dip nets 2; sacks 3; baskets 2; bone hooks 5 (day clock); arrows 2 (day clock) | crude tool 4; copper tool 4; crude weapon 6; rod 10; hand line 10; clappers 10; hurdles 10; traps 6; creels 4; dip nets 4; sacks 6; baskets 4; copper hooks 20; spears, bows, leisters, set lines, pack baskets, frames, bedrolls, horns, keep boxes 2 each |
| at the floor of 1 (one a unit): spear, bow, set line, copper hooks (10), leister, pack basket, frame, harness, bedroll, tent, horn, keep box, barrel, hearth, fire ring, owl hole, bins, stalls, beds, smoke loft, a set of racks, a tiered set, root clamp, grain pit, cairn | as at 1/7, and also: the withy bed, the retting pit's lower end, the tan pits, an added weir section, a dead hedge of 100 m, the woodshed, a quern, the plough, a chest |

**A `build` act costs 2 units** [m], so a fitting at the floor of 1 still takes a whole act, unless fittings take `qty` (as beds and
stalls already do). Either the act's cost follows the work (1 unit), or small fittings are built several to an act.

### 5.4 Contradictions found

1. **Timber's 240 kg** was taken by compressing a real year's fuel into the engine's year (02z_forest_model.py), while D2-273 puts
   fuel burned a night on the day clock. At 240 kg a timber, a normal night burns 120 kg against a real 10 kg or so.
2. **Fuel a night** is 2 to 3 times real even at a 10 kg bundle (20 kg a normal night, 80 a cold one), and 10 to 15 times at 60 kg.
3. **Stone** weighs 3, yet 30 stone make a 40 t room (1.3 t a stone) and 4 line a 28 t cellar (7 t a stone).
4. **Straw** at 1 kg gives a fifteenth to a thirtieth of a plot's real straw. It is coherent only as a truss of 16 kg.
5. **Hay** at 1 kg cannot be "a beast's day of feed". That is about 10 kg.
6. **Green crops:** 1 kg is 0.24 food and 0.8 of a beast's day, and `dry fodder` turns 10 kg of green crop into 8 hay, a gain of
   mass. Dried, 10 kg of green crop gives about 3 kg of hay [k].
7. **Charcoal** weighs 2, from 5 timber (1.2 t at the 240 kg reading), with 3 times the heat of a timber.
8. **Withies:** a bundle of 10 kg green has weight 1 in the withies note and 10 in the proposal.
9. **Small recipes in timber** are 10 to 200 times their real wood at any one unit weight: a crude tool's 1 timber, the rod's 0.5,
   clappers 0.5, bins 3 (720 kg at 240), the handcart 6, the pack 1.
10. **Hide:** a stoat, a fox, an otter, a roe and a red deer each give one hide, and a cow two.
11. **Offal never spoils** (spoil 0), though it is raw organ meat kept for bait.
12. **Coin:** 10 from 1 kg of copper makes a coin of 100 g.
13. **The proposal's gear and works are priced at real hours** (§5: a net 30, a trap 2.5, a hurdle 1.5, a pack 2; §4.1 and §4.2: the
    withy bed 10, the retting pit 10), against D2-276. On the rule they are 3 to 4, 0.3 to 0.6, 0.2, 1, 1.5 and 1.5 to 3.
14. **The 10 to 20% gear share** (§13) assumes those old prices. On D2-276 it is 3 to 8% (§5.1).
15. **Smokehouse loads:** storage.md §11 has 500 a set (two spaces) and 1,500 a timber house; smokehouse_capacity.md has 500 on
    two spaces; the brief has 250 a set and 750 to 1,000 a house. This document follows the brief. The open row on the racks' load
    (Q-83) should be read against it.
16. **Kept foods keep far too long:** a loaf keeps 46 nights in a house today, smoked fish 462, salt meat 770, against real weeks, a
    season and a year compressed.
17. **Lives counted in nights:** a bedroll's 40 nights and a tent's 30 are on target only at 1/11.4. D2-276's "real uses × the
    factor" at 1/7 would give 29 to 71.
18. **Fresh fish's x2 in a store** (D2-212), kept on top of a well-kept base, would make a house worse than the open for fish.
19. **The hearth rack's 3 nights** are about a month of real drying, against real days to two weeks: 1 night. This is the same
    check as the racks' load (Q-83, smokehouse_capacity.md §9 q5).
20. **Salt fish reaches its year only in brine,** that is in a barrel, and the cooper is not yet a trade (storage.md asks). Without
    it, salt fish keeps 1.5 to 2 times worse.
21. **Stores count units, not kilograms:** the woodshed counts timber and firewood alike (`STORES.kinds`), the bins hold "60 food"
    (a food value), and the cellar 40 food a space.
22. **The carry limits are below real** (a pack ox 60, a handcart 40) while the weights become real, and the hunt adds pack and ox
    where travel takes the larger (02zzv §1).
23. **The brine pan** is made from 1 kg of copper. A pan is 10 to 30 kg [e].
24. **The dry-stone wall's 8 stone** (24 kg today, 200 kg at 25 kg) stand for 566 to 1,132 t round a field.
25. **The egg unit** reads as one egg but is a kilogram, and laying runs on the old clock (L-138).
26. **The weir** priced at the research note's size is about fifty times cheaper than a field's fence under the rule. Its size must
    be set to its take first (building_clock.md issue 8; D2-262).
27. **Lives:** the plough's 60 plots and the crude tool's 10 acts against 11 to 27 and 20 to 70 on the rule. The handcart and the
    pack have no life.
28. **Dried last in the order** holds only with the damp penalty. A hearth-dried fish in a damp house keeps months, less than salt
    fish in brine.

---

## 6. Open questions for Zach

1. **The bulk goods in handling units (recommended).** Each bulk good gets a handling unit of a stated weight: timber and stone a
   25 kg load, firewood a 10 kg bundle, straw the 16 kg truss, hay 10 kg, charcoal 20 kg, withies and bark 10 kg bundles. Every
   recipe is rewritten in real kilograms and the forests' stocks converted. The alternative keeps the present units and states their
   large weights (a timber about 240 kg, a stone over a tonne), with fractional recipes and timber that can never be carried on foot.
2. **Fuel a night at its real weight.** About 10 kg of wood a normal night and 30 a cold one (heat 0.5 and 1.5 in place of 1 and
   4), on the day clock as food is?
3. **The keeping curve for every shelf life.** Nights = min(d, 2) + (d − 2) ÷ 11.4 for a food that keeps d real days, with process
   times compressed whole at 1/11.4. Bread then keeps about 2 nights, a keeping smoke about 10, a hard cure about 25, salt about 34,
   and grain a little longer than now.
4. **Lives counted in nights at the calendar's 1/11.4.** A bedroll or a tent would take the calendar's 1/11.4, beside lives counted
   in acts of work at 1/7. D2-276 names only "real uses × the factor".
5. **Moving a building's materials to the site.** On the day clock as carrying, a stone room's carriage is about as much again as its
   building and a wall's 6 to 20 times. The alternative counts it as part of the build at the factor. And should the carry limits
   rise to real (a pack ox about 100 kg, a handcart about 120, a cart about 900)?
6. **Field walls.** With stone real, 100 m of dry-stone wall takes 4,000 to 8,000 stone. Should walls stand only where the land gives
   its stone (clearing, hoeing, a quarry beside them), or take a named factor on their stone?

---

## 7. Handed on (not settled here)

- **To part 2 (materials and making):**
  - the hay-making rate (2 to 3 times low);
  - dung's unit;
  - green fodder and `dry fodder`'s mass;
  - copper ore's grade and smelting's charcoal;
  - the brine pan's copper;
  - the cheese rate;
  - the cooper as a trade (barrels, and so salt's year);
  - leather's uses (the frame, harness, bellows, shoes: D2-281);
  - tanning's lime (wood ash is assumed here);
  - pelts as a good;
  - bow, arrows and the spear, if they come in this wave.
- **To part 3 (taking and keeping):**
  - coin's weight;
  - the hard-cured meat good;
  - containers' protections against theft (the locked chest, deferred: L-156);
  - stores' capacity against the compressed year (L-154).
- **To 37.4 (the code's owner):**
  - the floor in `verbs.cost`;
  - a `capital` clock in `engine/clocks.py` with one conversion from real hours;
  - per-portion keeping in `night.decay_rate`, with penalties as hazard multipliers;
  - the racks' own `holds`;
  - the weights line in the prompt.
- **To the timber economy (W-76):**
  - builders as a trade;
  - felling and hewing at the stump;
  - hauling by ox;
  - the wood as a building chokepoint.
- **Q-73 (salting's rate):** this document uses the proposal's 40 a unit (about 20 kg an hour with gutting). Q-73 is still Zach's.

---

## Sources

**In the repository:**
- `cybertron2/engine/data.py` (ITEMS, DECAY, FITTINGS, ROOMS, BLUEPRINTS, SPACE, STORES, WATER_WORKS, FENCES, CLEARING, TECHNIQUES,
  PHYSICS) and `engine/night.py` (`decay_rate`, `spoil_rate`), read on main, 22 Nov; `wild/kinds.py` (goods by kind);
- `docs/cybertron2/spec/core/clocks.md`, `spec/economy/transport.md`, `DECISIONS.md` (D2-135, D2-258 to D2-281);
- `proposals/hunt_fish_materials.md`, `building_clock.md`, `store_rules.md`, `shared_units.md`;
- this folder's building_clock.md, storage.md, smokehouse_capacity.md, fibre_and_cord.md, withies_wood_materials.md,
  hunting_ladder.md, fishing_ladder.md;
- `docs/review/37_growth/` 02zzu_shared_units.md, 02zzu_lookup.md, 02zzv_carrying_in_runs.md, 02zzx_salting_rates.md,
  02z_forest_model.py, 02g_resources_and_transport.md §3.

**On the web** (search summaries only; the fetch of en.wikipedia.org was refused by the session's network):
- Truss (unit): straw 36 lb, old hay 56 lb, new hay 60 lb; 36 trusses a load; a cart of 18 cwt: [Truss (unit)](https://en.wikipedia.org/wiki/Truss_(unit))
- Packhorse loads: [Packhorse](https://en.wikipedia.org/wiki/Packhorse); [Fell Pony Museum, 15th and 16th centuries](https://fellponymuseum.org.uk/fells/15_16C/packpony.htm)
- Long straw thatch, bundles to a tonne and to a square metre: [East Anglia Master Thatchers, long straw guidance](https://www.eamta.co.uk/media/lx3ppkna/long-straw-guidance-copy.pdf); [EAMTA, long straw](https://eamta.co.uk/about-thatch/long-straw/)
- Energy and firewood: [Warde, Energy Consumption in England and Wales](https://histecon.fas.harvard.edu:443/energyhistory/data/Warde_Energy%20Consumption%20England.pdf); [Warde 2019, Historia Agraria](https://repositori.uji.es/xmlui/bitstream/10234/181747/1/77%2c%207-32.pdf); [History and Policy, Warde](https://historyandpolicy.org/policy-papers/papers/facing-the-challenge-of-climate-change-energy-efficiency-and-energy-consump/)
- Hide weight as a share of live weight: [Thai beef cattle study](https://ebook.tsu.ac.th/store/book/research/full2009/full2009/assets/basic-html/page263.html); [UNIDO, hides](https://downloads.unido.org/ot/48/13/4813527/20001-_22423.PDF)
- Tanning: [Scientific American, Practical suggestions on tanning leather](https://www.scientificamerican.com/article/practical-suggestions-on-tanning-le/) (sole leather 48 to 54 lb from 100 lb of green hide); [Bark tanning basics](https://braintan.com/barktan/1basics.htm) (oak bark about 10% tannin); [Encyclopaedia Britannica 1810, tanning](https://jimclifford.ca/early_encyclopedia_britannica/articles/1810/eb_4th_1810_020179.html) (11 to 18 months); [NPS, tanning in the seventeenth century](https://www.nps.gov/jame/learn/historyculture/tanning-in-the-seventeenth-century.htm)
- Timber for buildings: [Robin Wood on Rackham at Cressing Temple](https://www.robin-wood.co.uk/wood-craft-blog/2010/09/06/ancient-carpentry-and-ancient-woodland/); [Forestry Commission Scotland, Green oak in construction](https://forestry.gov.scot/images/corporate/pdf/green-oak-in-construction-2007.pdf); [DBRG dendrochronology summary](https://www.dbrg.org.uk/sites/default/files/PDF-embeds/TOTAL%20DENDRO%20151122%20FINAL%20BF.pdf)
- Load carrying: [Pack animal](https://en.wikipedia.org/wiki/Pack_animal)

*Current as of 22 Nov 2026 (W-77; nothing decided).*
