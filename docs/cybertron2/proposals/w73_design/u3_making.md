# U3. Materials and making: the chains, the made things in kilograms, batches, two lives, mending, and what each level is shown

**Status:** discussion (component spec of the integrated design, W-85). Parts decided are cited; the rest are defaults taken to
write on, marked, or open questions at the end. Nothing built.
**Owner:** 37.2 (the materials, the gear's data, the crafts' data, the gate check). 37.4's core where named below (the cost of an
act and `make` in `verbs.py`, the craft lines in `knowledge.py`, item wear in `world.py` and `wear.py`), named on any merge.
**Thread:** the integrated design (W-85), under the network (W-73); the draft was design wave part 2 (W-83).

---

## Extends

Read in full for this spec, and built on:

- **proposals/hunt_fish_materials.md** §3 (the goods), §4 (each material's ways and its switch), §5 (gear made, held, set, worn,
  mended), §6 (the works), §7.3 to §7.6 (keeping, stores, pollution, tanning), §8 (the network), §13 (the share of a year).
- **proposals/trying_and_learning.md** (difficulty classes, every attempt teaches, capability points, profiles).
- **proposals/building_clock.md** (what ends a thing's life decides its clock; capital at real hours times the factor; the 1-unit
  floor and batches; data rows holding real hours).
- **Decisions:** D2-263 (recipes shown by level), D2-264 (gear life by material; weights in kg; the withy bed's three years; flax in
  a close; retting in water fouls it), D2-247 (a bulk process takes up to its batch; a whole thing takes its inputs whole), D2-251
  (a ladder of detail by familiarity), D2-267 (practice at a 64-day lifespan), D2-270 (the tanner row; couplings and gate checks on
  by default, off only by an explicit setting), D2-271 (racks made with withies and a timber), D2-273 (the clocks), D2-275 (a unit is
  2 hours), D2-276 (making durable things on the year clock), D2-281 (bark a good; the pack basket and the frame; the factor staged),
  D2-286 (the options list gone), D2-288 (handling units, every recipe in real kg), D2-289 (shelf life as a quarter lost), D2-46
  (weapons wear; a smith mends), D2-52 (skill by practice); the offer O-2 (the eleven bulk processes up to their batch; Zach's
  conditional go, folded into the next build).
- **The overnight drafts:** wave2_making.md (all of it), wave1_physical_basis.md §1, §3, §5.3, §5.4, wave_conflicts.md (C2, C19,
  C20, C32, K5, K6, K7, K11, E6, E13, E17, G2, G14), wave4_people.md §2.2, §3.5.11 to §3.5.13, §4.2.
- **Notes:** fibre_and_cord.md, withies_wood_materials.md, byproducts_and_substitutes.md, crafts_evaluation.md, learning_times.md,
  household_skills.md.
- **Code read (main, 22 Nov):** `engine/data.py` (ITEMS 20-115, CROPS 137-147, RESOURCES 179-205, FORESTS 207-220, FITTINGS
  234-286, TECHNIQUES 413-716, TRY 730, SKILL 732), `verbs.py` (VERB 17-40, `cost` 116-159, `_make` 760-856), `knowledge.py`
  (`inputs_words` 300, `batch_share` 305, `card` 368-386, `crafts_lines` 389-409, `tried` 448-477), `wear.py`, `world.py`
  (`p_wear` 686-694), `farm.py` (plot shares 228-300, `_sow` 922-1023, `_reap` 1128-1166, `ready` 1191-1249), `landgen/gates.py`,
  `wild/kinds.py` (TAKEN 631-657), `clocks.py`.

Tanning, leather and pollution are U10's (u10_tanning_pollution.md); this unit gives them bark, hides, the leather goods' recipes
and the shared rules (batches, two lives, mending, shown lines). Processing containers (retting, the pits, racks) and their night
step are **U4's** (u4_processing.md): this unit gives each process row's inputs, outputs, ratio, labour and failure, never the
container's night.

## Departures

Every place this spec differs from what it extends, with the reason. Where an overnight draft departed silently from a proposal or
decision, it is named here and the decision followed.

| # | From | This spec | Why |
|---|---|---|---|
| 1 | hunt_fish_materials §4 to §6 (trap 2.5 units, net about 30, hurdle 1.5, pack basket 2, withy bed 10, retting pit 10) | units derived from real hours at the world's capital factor (§2.1): a trap is 1 unit for up to 2 at 1/7 | D2-276 (C2); the proposal's prices were real hours or today's engine |
| 2 | building_clock.md stage 1 ("new gear written on the rule from the start", i.e. at 1/7 while works sit at 1/15) | all capital, gear and works alike, on the one factor the world is at; the data hold real hours | K7: gear at 1/7 beside works at 1/15 costs more per real hour than a house; D2-276 names "one named lever". Default, since the staging is open (basis §1, §7) |
| 3 | wave2 §1.2 and §3.2: set gear's uses at 1/7 of the real count (traps 30 to 45 sets, nets 30 to 65) | set gear, bedrolls, tents and shoes count their uses in nights at the calendar's 1/11.4 (traps about 20 nights set, a barked net about 25) | basis §1 "Lives" (default); K6 |
| 4 | wave2 §3.3: untreated cord in water rots in 1 world year ("compressed generously", a named departure) | 10 nights in water untreated, 32 barked: its real time in water as world time | D2-276 ("its real years as world years"); under it, barking is what keeps a net, which ties the fisher to the peeler |
| 5 | wave2 §2.4, §2.5: hide's and bark's keeping read as half-lives (33.8 and 70 nights) | read as a quarter lost by then (hide 0.85% a night, bark 0.44% a night dry) | D2-289 replaced the half reading |
| 6 | wave2 §3.4 renders rough lines without amounts ("withies; you have not yet got the throat right") | rough shows the inputs with their amounts, as the card does | D2-263 is decided; wave2 departed from it without a decision. W2-17 stays a question (§12) |
| 7 | wave2 §3.2's batches, picked by hand (rods and lines 5 a unit, bedroll 1, crude weapon 3) | one rule: batch = the whole pieces one unit's work makes, from real hours (§2.1): rods and lines 9, bedroll 4, crude weapon 4 at 1/7 | one rule the staging can move; the hand picks used the low end of each range |
| 8 | wave2 §2.5 and wave1 §3.1: the bark season 5 nights (W2-5) or 2 to 3 | 6 nights, year days 4 to 9 (spring day 4 to summer day 1) | D2-273 compresses mid-April to the end of June (about 75 days) to about 6.6 nights; U10 §2.2 |
| 9 | wave1 §3.2 and wave2 §3.2: the frame restrapped with 0.2 leather | no restrap: the frame's life is its straps' (rot), and it is remade | mending restores uses, never rot (§3.4); a part with its own life is a later refinement (§11) |
| 10 | hunt_fish_materials §4.2: a fishing household needs 1 to 3 kg of cord a year; retted flax 0.7 of the straw, 8 retted a cord | 0.7 kg a year with a barked net, 1.8 untreated; 10 kg straw to 8 kg retted to 1 kg cord | K5, K11: the need follows the net's life (§3.3); the mass chain sits between the proposal's 11.4 and the fibre note's 8 (wave2 §2.2) |
| 11 | hunt_fish_materials §4.3: dressing a deer about 0.5 unit | 1 unit for a red deer or a boar, 4 roe, 10 hares or fowl | real 1 to 2 hours skilled (hunting_ladder §1.7); the 1-unit floor |
| 12 | hunt_fish_materials §5: "pack basket (frame and straps)", 1 withies and 0.1 hide, one item | two items: the withy pack basket and the leather-strapped frame | D2-281 (C20) |
| 13 | D2-271 and hunt_fish_materials §6: racks of "2 withies, 1 timber" | 2 withies and 2 timber (50 kg of frame poles) | the timber in D2-271's day was the 240 kg reading; D2-288's 25 kg load makes the frame two loads (C32). The decision's substance (withies and timber) is kept |
| 14 | withies_wood_materials §3.3: wild willow in the young-growth regime (`renewal: young`) | a yearly crop of rods on stools: the stools set the year's rods, summer cutting and grazing harm them (§1.1) | the logistic binds at a quarter of its stock a year, which a one-year rod does not (W2-9) |
| 15 | trying_and_learning §2: classes at lifespan 96 | wave4 §4.2's values at lifespan 64 | D2-267 |
| 16 | today's code: a failed make spoils all its inputs at once (`verbs.py:845`); tools destroyed at their life (`world.py:686-694`) | a broken piece stays, unusable, until mended or rotten; long processes lose a share (U10 §2.4) | two lives and mending (§3); a pit of twenty hides does not all rot (W2-8) |
| 17 | D2-247: "making a whole thing still takes its inputs whole" | kept: each piece takes its inputs whole; what is new is that one act's units make **up to** its batch of pieces | the rule carried to things made below a unit (O-2's conditional go; basis §1 "The 1-unit floor") |
| 18 | wave1 §3.2: the gill net's fine twine (20 to 30 real hours of spinning) folded into the net's making at the factor | kept, named | material work priced as capital, against D2-276's "materials real"; the alternative (a twine good) is W2-11 (§11) |

Nothing else from the sources is dropped. Wave2's numbers that rest on its 1/7 set-gear lives (§5.1's six traps a year, its 7.7%
and 4.9% shares) are re-derived in §6.

---

## Purpose

Make every piece of gear, every container and the leather goods real things with real materials, so that a household's year of
taking depends on wet ground, a wood, nettles or flax, a kill, the peeler and the smith, and so that the cheap path (wild rods, wild
cord, rawhide) and the dear path (a withy bed, flax and a spinner, a tanner's leather, a smith's copper) are both open and differ
in what they need (scenario_design §1: restricted access, conversion chains). Every recipe is in real kilograms on the handling
units (basis §2; D2-288), every act's units come from real hours on the clocks (basis §1; D2-276), every lasting thing wears by use
and rots by time, and each person sees of a craft exactly what their level of it holds (D2-263).

---

## 1. The material chains

Units of work, handling units and clocks are basis §1 and §2. Rates are for one who knows the craft with a crude tool; skill acts on
them as D2-52 says. [s] sourced, [n] a sibling note, [k] standard figure not re-checked, [e] my estimate, [m] read from the engine.

### 1.1 Withies (a 10 kg bundle of green rods, basis §2)

**The act: cut withies** (gather, simple, basic). Draws by where it is done:

| Where | Rate (bundles a unit, crude tool) | What it draws |
|---|---|---|
| wild willow: fen, alder carr, reedbed, wet grassland, and any meadow, pasture, scrub or wood parcel bordering water | 1.5 | the parcel's `willow` stock (below) |
| a managed wood (hazel coppice) | 4 | young growth: 10 kg of it a bundle, the stock `cut` draws for firewood |
| any other forest or scrub | 1.5 (crooked rods) | young growth as above |
| a withy bed (U7's work) | 4 | the bed's own stock |

- **Tools** [e]: bare hands 0.33 of the rate (0.5 a unit; a knife or a stone flake is a tool, so bare means without one), crude 1.0,
  copper 1.33. Today `cut` refuses bare hands (`data.py:434-437`); cut withies does not.
- **Season** [n withies §3.3]: winter 1.0, autumn 0.8, spring 0.5, summer 0.3 of the rate. Summer rods are leafy and few.
- **The wild willow stock** (`RESOURCES["willow"]`, renewal `seasonal` like the wild plants'): capacity **K = 0.3 t a hectare a year
  of usable rods on fen and carr, 0.1 on a bank parcel's margin** [e: a fen is mostly reed and sedge, willow at its edges; about a
  fiftieth of a bed's 13 to 20 t]. At the land's unit of size (about 2 ha, `landgen/field.py:3`) that is 60 bundles a unit of size of
  fen and 20 of a bank parcel. The rods regrow to K each spring. **Summer cutting harms the stools**: each bundle cut in summer lowers
  K by 0.1 bundle, recovering a tenth of the loss a year. **Grazing** on the parcel halves the year's regrowth (as young growth
  already stops under beasts, D2-156). I do not know the real wild figure; it is the lever that decides whether wild willow binds
  (W2-9). The unit of size's area is a basis question (§10, §12).
- **Keeping:** green rods are worked within weeks or dried and re-soaked; withies keep about a year [e]: a quarter lost by 33.8
  nights on the keeping curve (basis §3; D2-289), 0.85% a night, the open wet x2.

**Where it binds** (wave2 §2.1, re-checked on these rates): Eelmouth (fen of size 3, two bank parcels) holds about 220 bundles a
year against a village's 46, so labour and the season bind there, not the stock; a village with one bank parcel (20 a year) cannot
keep a wattle weir (6 bundles a section a year) by wild cutting and must plant a bed, buy rods, or build in timber. The weir is half
of all withy demand where one stands.

### 1.2 Cord (1 kg of cord, twine, line or light rope, basis §2)

**Wild cord: twist cord** (gather, simple, basic, bare hands). Nettle on rich disturbed ground (built ground, field and wood edges,
fen, alder carr); lime and willow bast in spring. **0.04 cord a unit** in summer and autumn, 0.03 in spring, 0.01 in winter (stems
retted standing) [n fibre §9.2]: 25 units a kg (real 35 to 80 hours a kg, fibre_and_cord §2). No stock: a village twists a few kg a
year from plants that are not scarce at these rates [e]. Coarse; enough for snares, lines, lashings and a coarse net.

**Flax** (four acts on the farming verbs, one make, one process):

| Step | Shape | What | Rate | Clock, season | Real anchor |
|---|---|---|---|---|---|
| sow flax | work (`sow`, item `flax seed`) | on a strip of a held plot (§1.3) or a whole plot | 11 kg of seed a plot (100 to 120 kg a ha [k]) | spring | |
| pull flax | work (new technique, kind `crop` on flax) | pulled by the root | 0.05 plot a unit, at least 1 unit (about 25 m2 an hour if a plot is 0.1 ha by yield) [e: 15 to 25 person-days a ha] | summer, at ripe | gives flax straw and seed rippled from it |
| ret flax | load a processing container (U4) | in water 1 night; on grass 3 nights; in a retting pit 1 night | 1 unit to lay up to 50 flax, 1 to lift | late summer | water 1 to 2 weeks, dew 3 to 6 (basis §1 process times); in water it fouls (U10 §3) |
| dress and spin | make, practised | break, scutch, hackle, spin and ply in one act | **up to 1 retted flax a unit, giving 0.125 cord** (8 units a kg) | best in winter | 15 to 20 hours a kg of coarse 2-ply [n fibre §2] |

**The mass chain:** 10 kg of pulled straw, 8 kg retted, 1 kg of cord [e; wave2 §2.2]. Retting's ratio is 0.8 by weight.
**Flax seed:** pulling ripples about 0.1 kg of seed from each kg of straw [e: fibre flax pulled at yellow ripeness still sets most of
its seed, 300 to 500 kg a ha]; a strip's 10 kg of straw returns about 1 kg of seed for the 0.28 kg sown. Seed keeps as grain does.
**Wild against flax per kg of cord:** wild 25 units; flax about 10 (spin 8, the rest sowing, pulling, a retting batch). About 2.5
times cheaper.

### 1.3 Flax below a whole plot: the strip (W2-2, designed here)

A household needs 0.5 to 2 kg of cord a year (§6), 5 to 20 kg of straw, which a plot's yield gives on **a fortieth to a fifth of a
plot**. Today a holding is whole plots with one crop (`farm.py:228-300`), so a household cannot hold its flax as the close D2-264
decided. The design:

- **A strip crop** is a CROPS row with `strip`: the most of a plot it may take as a strip (flax: 0.25 [e]). Hemp and herbs can use the
  same field later.
- **A strip is a second crop record on a holding**, kept in the holding's record under `strips` (a list of crop records of today's
  shape, `farm.py:1003-1007`), each with its own sown day, ripe day, seed, area, base and left. A holding has at most one strip of
  each strip crop.
- **Sowing:** `work sow` with item `flax seed`. If the seed sown is a strip's worth or less (area at most `strip` of a plot), it goes
  into a strip on the holding: room = the holding's plots less what its main crop and its other strips already take. Above that, flax
  is the holding's main crop, as grain is. No new verb and no new argument: "sow 0.3 flax seed in Long Field" makes a strip.
- **On a meadow or pasture held by plots** (the fishing households hold no field: Eelmouth's Clay Field is scrub): a strip needs
  its turf broken first. `work dig a strip` (new technique, kind `strip_ground`, basic): breaks up to a sixth of a plot a unit
  [e: CLEARING's meadow rate of 6 units a unit of size, 1 unit floor], on a meadow or pasture plot the household holds. The dug
  strip takes a strip crop with no turf penalty (`PHYSICS.farming.turf`), and the parcel stays meadow or pasture. Grazing beasts on
  the parcel trample it as they trample an unfenced field's crop; fencing a strip waits on fences priced by length (U7, G8).
- **Growing:** each strip grows on the night as a crop does (`grow_night`), with its own frost, blight (`fail_chance`) and weeding.
  The holding's soil steps after a strip is pulled by the strip's area share (`soil_step` scaled by area / plots).
- **Targeting:** `weed`, `pull flax` and `reap` take the crop by its name: `pull flax` finds the flax (the strip, or the main crop if
  flax); `reap` and `weed` with no crop named take the main crop, as now. The resolver's own-first rule (U2, basis §6) is unchanged.
- **The flax row:** `CROPS["flax"] = {seed: "flax seed", gives: "flax", seed_kg: 11, strip: 0.25, share: 0.27 (about 100 days),
  growth: {spring 1.0, summer 1.0, autumn 0.5, winter 0}, yield: 5.5, hardy: False, takes: 0.15, restores: [0.10, 1.0], straw:
  False, also: {"flax seed": 0.1}, names: ["flax", "linseed"]}`. With `crop_base` (`farm.py:66`) a dug plot of flax at fertility 1
  gives 16 x 4.5 x 5.5 = **about 400 kg of straw** (4 t a ha if a plot yields as 0.1 ha, wave1 §1.2), unbroken turf a tenth of it.
  `seed_kg` converts kg of flax seed to plot-seed (`plot_seed` 16 / 11).
- **Who is shown it:** the holding's line names the strip: "a strip of flax (about a fortieth of a plot), sown spring day 3,
  beside your barley".

A **whole plot of flax** is a village's or a region's supply (about 400 kg of straw, 40 kg of cord, 320 units of spinning: more than
one spinner's world year), so its bind is spinners, not land. The strip is the household's own; the plot is the supplier's. Both are
open (W2-2's (c)).

### 1.4 Bone, hide, tallow, antler: dressing the kill

**dress a kill** (work, simple; on a carcass thing, U2 §2: the kill lies where it fell, the hunter's). **1 unit for a red deer or a
boar, 4 roe, or 10 hares or fowl** [n hunting_ladder §1.7: a red deer 1 to 2 hours skilled]. By level:

| Kind | Meat | Hide (units, basis §2) | Bone (kg) | Tallow (kg) | Antler |
|---|---|---|---|---|---|
| red deer (90 kg live) | the kind's goods (`wild/kinds.py:633`) | 1 | 4.5 (5% of live weight) | about 2 in autumn [e] | a stag in autumn or winter: 1 (1.5 kg) |
| roe (22 kg) | as above | 0.3 | 1.1 | | |
| wild boar (70 kg) | as above | 1 | 3.5 | 3 to 5 in autumn [e] | |
| brown bear (250 kg) | as above | 3 | 12 | 10 [e] | |
| hare, fowl | as above | (none) | | | |
| fox, stoat, otter, wolf, beaver | | **a pelt** (trade now, fur later), not hide | | | |
| a slaughtered cow (`slaughter`) | as built (`data.py:548-556`) | **3.5** (20 to 25 kg green); ox and bull 4; a young beast 1 | 15 | 4 (kept) | |

- **One who knows dressing** (known or capable) gets all of it. **A novice** (aware or rough) loses about 15% of the meat, takes the
  hide at half (holes cut in it) and no bone or tallow (learning_times §2.9).
- **An undressed carcass** can still be cut and carried (`take`) at the novice's share of the meat; the hide, bone and tallow are
  lost with it.
- **Bone never binds** (a red deer's 4.5 kg is 900 bone hooks at 5 g): it is kept as a good because D2-264 names it and the copper
  hook competes with it; no stock logic.
- **Hide keeps** a year dried (dressing includes drying: no green hide good): a quarter lost by 33.8 nights (basis §3; D2-289), 0.85%
  a night well kept, the open wet x3 (`DECAY["hide"]`, now a hazard on that base rather than today's `abs` share).

### 1.5 Bark (a 10 kg bundle of peeled, dried oak bark, basis §2; D2-281)

Peeling, its season and what it draws are U10 §2.2. For this unit: bark is an input to tanning (U10) and to barking nets (§3.4),
and keeps about two years dry [e]: a quarter lost by 65.9 nights, 0.44% a night; the open wet x5 (wave1 §2.3: exposed hemlock bark
lost nearly a quarter of its tannin in two months).

### 1.6 Leather (1 kg of bark-tanned leather)

Made in the tan pits (U10 §2): 3 kg a hide unit. Keeps about ten years [e]: 0.09% a night. Its uses are the frame, harness, the
bellows and shoes (§2.2).

### 1.7 Where the chains meet (wave2 §2.6, kept)

Withies against timber for the weir; withies against cord for traps; one young-growth stock for rods, firewood, bark poles and
charcoal; cord wild, from flax or as rawhide thong; hooks of bone or copper; straps and harness of rawhide or leather; sacks of
cord against baskets of withies; leather for the forge's bellows; bark for the pits against bark for nets; tallow for lights against
currying. Each is a choice with different needs, which is what the network's test asks (hunt_fish_materials, "What the design is
for").

---

## 2. The made things

### 2.1 How a row is priced: real hours, the factor, the floor and the batch

- **Each recipe row holds its real hours a piece** (`hours`) and its clock (`clock: capital` or `day`), never a unit count. The
  engine converts once (U0's `clocks.py` conversion, basis §1 "Making capital"):
  - a piece's units `u` = hours x f / 2 for capital (f the world's capital factor, basis §1), hours / 2 for the day clock;
  - **if u is 1 or more**, one act makes one piece for round(u) units;
  - **if u is under 1**, one act costs **1 unit** (basis §1 "The 1-unit floor") and makes **up to** its batch, b = floor(1 / u) pieces,
    each piece taking its inputs whole (D2-247); making fewer than b costs the same unit.
- **A make of more than the batch** is several acts: units = per-act units x ceil(qty / b). `qty` in the make act is now the number
  of pieces wanted, not the number of acts (today `qty` repeats the act, `verbs.py:156`, `:775`).
- **No act exceeds a day:** a thing whose units exceed a person's day (a seine, later) is built over days as a work (U7).
- **Bulk processes** on the day clock (grinding, milling, baking, salting, drying, dry fodder, leaching, charcoal, cheese, spinning)
  take up to their batch of inputs (D2-247; O-2), table §2.4.
- **What changes in code:** `verbs.cost` takes `int(units)` and multiplies by the act count (`verbs.py:142`, `:156`), so every
  recipe under a unit is free (E6). It becomes `units_of(tech, w) x ceil(qty / batch_of(tech, w))`, at least 1.

### 2.2 The table (at 1/7, the target, and at 1/15, the stage before; basis §1)

Real hours are wave1 §3's midpoints, marked there; the units and batches follow from §2.1 [m, scratch `u3/calc.py`]. Materials in
handling units with kilograms (basis §2). Lives are §3.3's.

| Thing | Recipe (each piece) | Real hours | 1/7: units, batch | 1/15 | Weight (kg) | Class; shape; at |
|---|---|---|---|---|---|---|
| **wicker trap** | 0.45 withies (4.5 kg green) | 6 | 1 unit, up to 2 | 1, up to 5 | 2.5 | practised; make; anywhere |
| **creel** | 0.25 withies | 6 | 1, up to 2 | 1, up to 5 | 1 | practised; make |
| **basket** (holds 25 kg) | 0.3 withies | 6 | 1, up to 2 | 1, up to 5 | 1.5 | practised; make |
| **withy pack basket** (D2-281) | 0.4 withies, 0.1 hide (rawhide straps, 0.3 kg) | 8 | 1, 1 | 1, up to 3 | 2 | practised; make |
| **leather-strapped frame** (D2-281) | 0.1 timber (2.5 kg of split ash or hazel), 0.5 leather | 9 | 1, 1 | 1, up to 3 | 3 | practised (leather work); make |
| **keep box** | 1 withies | 9 | 1, 1 | 1, up to 3 | 8 | practised; make |
| **hurdle** (1.8 by 0.9 m) | 1 withies | 2.8 | 1, up to 5 | 1, up to 10 | 10 | practised; make |
| **fishing rod** | 0.1 withies (one 1 kg pole) | 1.5 | 1, up to 9 | 1, up to 20 | 0.8 | simple; make |
| **hand line** | 0.02 cord, 2 hooks | 1.5 | 1, up to 9 | 1, up to 20 | 0.05 | simple; make |
| **set line** (20 to 50 hooks) | 0.3 cord, 30 hooks | 9 | 1, 1 | 1, up to 3 | 0.5 | simple; make |
| **bone hook** (day clock) | 0.005 bone | 0.4 | 1, up to 5 | 1, up to 5 | 0.005 | simple; make |
| **copper hook** | 0.005 copper | 0.4 | 1, up to 35 | 1, up to 75 | 0.005 | skilled (the smith's); make, at an anvil |
| **snare** (day clock) | 0.005 cord (a noose and tether, about 1 m), or 0.002 hide as rawhide thong | 0.17 | 1, up to 12 | same | 0.008 | simple; make |
| **gill net** (20 by 1.5 m, 7 cm mesh) | 1 cord; 0.1 stone of sinkers (2.5 kg), or none made at a node with river or brook water (pebbles from the bed [e]); floats folded in | 50 (the fine twine's extra spinning folded in: Departure 18) | 4, 1 | 2, 1 | 4 | practised (netting); make, at a house |
| **fowling net** (clap, 10 by 2 m) | 0.8 cord, 0.1 timber (poles) | 60 | 4, 1 | 2, 1 | 2 | practised (netting); make, at a house |
| **dip or hoop net** | 0.1 cord, 0.2 withies (the hoop) | 3.5 | 1, up to 4 | 1, up to 8 | 1 | practised (netting); make |
| **harness** (yoke and traces) | 0.4 timber, 1.5 leather; or 0.4 timber, 0.5 hide as rawhide | 13.5 | 1, 1 | 1, up to 2 | 12 | practised (leather work); make |
| **shoes**, a pair (U10 §2.6, an option) | 0.5 leather; or 0.3 hide as rawhide | 4 | 1, up to 3 | 1, up to 7 | 0.6 | practised (leather work); make |
| **sack** (holds 50 kg) | 0.6 cord (the weaving folded in, as the spindle is) | 4 | 1, up to 3 | 1, up to 7 | 0.6 | practised; make |
| **chest** (holds 400 kg) | 4 timber of boards (100 kg) | 22 | 2, 1 | 1, 1 | 60 | skilled (the wright's); make |
| **barrel** (holds 120 kg) | 7 timber of stave bolt, 0.3 withies of hoops | 9.5 | 1, 1 | 1, up to 3 | 25 | skilled (a cooper: the wright's specialism); make; whether barrels or a tub come now is U5's (G10) |
| **spear** (copper head) | 0.5 copper, 0.08 timber (an ash shaft) | 3 | 1, up to 4 | 1, up to 10 | 2 | skilled (the smith's head); make, at an anvil |
| **crude tool** | 0.04 timber, 0.04 stone (1 kg each) | 7 | 1, up to 2 | 1, up to 4 | 1.5 | simple; make |
| **copper tool** | 1 copper, 0.02 timber | 6 | 1, up to 2 | 1, up to 5 | 1.5 | skilled; make, at an anvil |
| **crude weapon** | 0.06 timber | 3 | 1, up to 4 | 1, up to 10 | 1.5 | simple; make |
| **bedroll** | 0.5 hide | 3 | 1, up to 4 | 1, up to 10 | 3 | simple; make |
| **tent** | 1.5 hide, 0.4 timber | 9 | 1, 1 | 1, up to 3 | 18 | simple; make |
| **wooden plough** | 1.2 timber, 1 copper | 36 | 3, 1 | 1, 1 | 25 | practised (the carpenter's); make |
| **handcart** | 2 timber | 50 | 4, 1 | 2, 1 | 40 | practised (the carpenter's); make |

Note on snares: at 12 a unit a line of 25 takes three acts as written, two by the hours (4.2 real hours). A make of qty 25 is
ceil(25 / 12) = 3 acts; I take that over a special case, and a bundle of 24 in 2 acts is what a careful maker would do. Snares and
bone hooks are on the day clock (used up in a handful of uses, D2-276), so their units do not move with the factor.

**Fittings and works this unit supplies recipes for, priced by U7** (buildings and their costs are 37.4's): a set of **smoke racks**
2 withies, 2 timber, real 8 hours (1 unit at both stages, D2-271, D2-284; capacity U4); a **tiered set** 3 withies, 3 timber, 12
hours; the **anvil and bellows** 4 stone, 2 leather, 0.4 timber (the bellows leather, D2-281; U10 §2.6); the **brine pan** 10 copper
and 4 stone (wave1 §3.4, contradiction 23); the **withy bed** (1 withies of cuttings on a wet parcel the household holds; a fence or a
dead hedge; nothing its first world year, half its second, 30 bundles a year from its third for 30 years, D2-264); the **retting
pit** (by water; silts in 10 world years). Their units are U7's tables; the wave1 estimates (racks 1, bed 1.5 at 1/7) are handed to
it as inputs.

### 2.3 What today's rows become (data.py, 22 Nov)

| Row today | Now [m] | Becomes |
|---|---|---|
| `fishing rod` (ITEMS `:51`, TECHNIQUES `:605`) | 0.5 timber (120 kg at the old reading), 0.1 hide; 1 unit; life 30, never worn | 0.1 withies; 1 unit for up to 9; the line a separate item; uses §3.3 |
| `pack` (ITEMS `:105`, TECHNIQUES `:587`) | 1 hide, 1 timber; 1 unit; +10 carry; no life | removed; the withy pack basket (+15) and the frame (+20) (basis §5; D2-281); a world's seeded packs read as pack baskets |
| `harness` (`:108`, `:664`) | 2 timber, 1 hide; 2 units; trade "leatherworker" (no such livelihood); 80 days | 0.4 timber, 1.5 leather or 0.5 hide as rawhide; the craft "leather work", the tanner's row (D2-270) or anyone taught |
| `anvil` (FITTINGS `:254`) | 6 stone, 2 hide, 1 timber; 4 units | 4 stone, 2 leather, 0.4 timber; units U7's; the bellows wear (U10 §2.6) |
| `smoke racks` (FITTINGS `:275`) | 2 timber; 2 units; "up to 40 fish, 3 nights" | 2 withies, 2 timber; capacity and nights U4's (D2-284, D2-291) |
| `bedroll`, `tent` (`:109-110`, `:660-663`) | 1 hide; 3 hide and 2 timber | 0.5 hide; 1.5 hide and 0.4 timber; lives in nights (§3.3) |
| `crude tool` (`:102`, `:666`) | 1 timber, 0.5 stone; life 10 | 0.04 timber, 0.04 stone; up to 2 a unit; life 40 acts at 1/7 |
| `crude weapon` (`:104`, `:668`) | 1 timber; life 10 | 0.06 timber; up to 4; life §3.3 (D2-46's fight wear kept) |
| `copper tool` (`:103`, `:673`) | 1 copper, 0.5 timber; 3 units; 40 | 1 copper, 0.02 timber; up to 2 a unit; 140 acts |
| `wooden plough` (`:107`, `:657`) | 4 timber, 1 copper; 4 units; 60 plots | 1.2 timber, 1 copper; 3 units; 18 plots (wave1 §3.2: 11 to 27) |
| `handcart` (`:106`, `:589`) | 6 timber; 3 units; no life | 2 timber; 4 units; rots in 7 world years |
| `slaughter` (`:548-556`) | 2 hides a cow or ox, 1 a young beast | hide 3.5 a cow, 4 an ox or bull, 1 a young beast; bone 15 a cow (§1.4) |
| `wild/kinds.py` TAKEN (`:631-657`) | a hide from a stoat, fox, otter, wolf, roe or red deer alike; a bear 2 | the kill a carcass whose goods come by `dress a kill` (§1.4): hide by weight, pelts for the small furs |
| `cut` (`:434`) | aliases "coppice", "cut poles", gives firewood | the aliases "coppice" and "cut poles" move to cut withies and to U7's poles (W-76) |
| `hide` (ITEMS `:89`, DECAY `:125`) | weight 1; an `abs` loss | weight 3 (dried, a red deer's); base 0.0085 a night, the open wet x3 (§1.4) |

**New goods** (ITEMS rows; weights basis §2 or §10 below): withies (10), cord (1), flax (1, pulled straw), retted flax (1), flax seed
(1), bone (1), bark (10), leather (1), pelt (by kind, 0.3 to 2 [e]), and every item of §2.2.

### 2.4 The bulk processes up to their batch (O-2; D2-247)

Units on the day clock at real hours (basis §1; wave1 §3.1). Each takes **up to** its batch for its units; less is less worth it.

| Technique | Up to (a unit's act unless said) | Gives | Fuel | Note |
|---|---|---|---|---|
| grind | 3 grain | 3 meal | | kept |
| mill (ox) | 64 grain in 2 units | 64 flour | | D4-97, kept |
| water mill | 200 grain in 2 units | 200 flour | | the 200-grain least is gone (crafts_evaluation; still in the data, `data.py:582`) |
| bread (hearth) | 10 flour in 2 units | 10 bread | 0.5 firewood | wave1 §3.1 |
| oven bread | 100 flour in 4 units | 100 bread | 3 firewood | wave1 §3.1 |
| salt fish, salt meat | 40 fish or meat, 10 salt (fish 1 to 4, meat 1 to 8) | as much salt fish or meat | | D2-283; whether salting is a make or a tub's loading is U4's |
| dry fodder | 30 green crop | 1 hay (10 kg) | | 10 kg green dries to about 3 [k]; today 10 to 8, a gain of mass (wave1 §5.4 #6) |
| leach acorns | 3 acorns | 2 acorn meal | | kept |
| charcoal | 5 timber (125 kg) in 1 unit | 1 charcoal (20 kg) | | burns 1 night (U4) |
| cheese | 20 milk, 0.6 salt | 3.3 cheese | | wave1 §3.1, at a cellar as now |
| dress and spin | 1 retted flax | 0.125 cord | | §1.2 |

---

## 3. Two lives, wear, rot and mending

### 3.1 The record: a piece

Today a container holds goods as `{item: qty}` and one wear count per item (`c["wear"][item]`, `world.py:686-694`), so six traps
share one count and nothing rots. Made things get **pieces**: for every item with a life, the container keeps
`c["pieces"][item] = [{"u": uses left, "rot": share of its rot life used, "of": the input it was made of ("leather" | "rawhide"),
"barked": day barked or None, "tag": its tag when placed}]`, one entry a piece, the list as long as the count. The primitives that
move goods (`create`, `destroy`, `move`, `give`, `take`, a set's laying and taking up in U2) move pieces with them, the most worn
first out of a container (a rule, deterministic; a person names a tag to choose). U2's placed gear (`uses_left` a piece,
wave3_taking §1.3) is the same record. A world saved before this has no `pieces`; loading builds them from the wear map (each piece
at the item's full life less the count), so an old run's replay stays exact under the old data.

### 3.2 The three counts of a use, and rot

- **Worn by acts of work** (tools, weapons, rods, hand lines, fowling and dip nets, harness, the plough): each act takes a use; the
  item's uses are its real uses x f (basis §1 "Lives"), so at the 1/15 stage a use costs the same share of a life.
- **Worn by nights** (set gear: traps, gill nets, set lines; bedrolls and tents slept in; shoes worn): each night of use takes one;
  the uses are real uses x 1/11.4 (basis §1 "Lives", default; G14). A "night of use" for shoes is a day spent out of doors working or
  walking.
- **Used up** (day clock: snares, bone hooks): real uses, uncompressed, since D2-276 puts them on the day clock. A set snare is torn
  or lost at about 1 in 6 a night set (real 3 to 10 settings [n fibre §4]); sprung snares are U2's.
- **Rot**, the second life, by time and condition (D2-276: real years as world years): each night a piece's `rot` rises by 1 /
  (its rot years x the world's year days), at the **wet** rate on a night in water (set, or a keep box in use) and the **dry** rate
  otherwise. At `rot` 1 the piece is gone.
- **At 0 uses a piece is broken**: it stays where it is, unusable, shown "broken: wants mending", until it is mended or rots (today a
  tool vanishes at its life, `world.py:690-692`).

### 3.3 Lives by thing

Real uses from wave1 §3.2 and the notes; engine uses at 1/7 (acts) or 1/11.4 (nights) [m, scratch `u3/calc.py`]; rot by material
[n withies §1.2; fibre §4; k].

| Thing | Count | Uses (1/7; at 1/15 for acts) | Rot: wet / dry (world years) | Mending (§3.4) |
|---|---|---|---|---|
| wicker trap | nights set | 20 (real 200 to 300 with repair: 18 to 26) | 2 (64 nights in water) / 5 | yes |
| keep box | (in water) | none | 2 / 5 | no |
| gill net | nights set | 25 (real 200 to 450 barked: 18 to 39) | **untreated 0.3 (10 nights in water); barked 1 (32)** / 5 | yes; barking §3.4 |
| set line | nights set | 6 (real 50 to 100: 4 to 9); the hooks lost with it | as cord / 5 | yes, with 15 hooks |
| fowling net | acts | 40 (19 at 1/15); real 200 to 450 | none wet / 2 (out in dew and frost) | yes; barking as the gill net |
| dip or hoop net | acts | 25 (12) | / 2 | yes |
| fishing rod | acts | 30 (14) | / 3 | no (remade) |
| hand line | acts | 8 (4); hooks lost with it | / 2 | yes, with 1 hook |
| copper hook, bone hook | (inputs) | lost with the line they are on | none | |
| snare | used up | 1 in 6 a night set | thong of rawhide rots on a wet night | no |
| creel, basket, pack basket | (carried) | none | / 4; 2; 2.5 | no |
| frame | (carried) | none | / 7 (its straps; Departure 9) | no |
| hurdle | (standing) | none | / 7 dry | no |
| harness | acts (days worked) | 100 (47); rawhide half | / 7; rawhide 2 | yes |
| shoes | nights (days worn) | 12 (real 120 to 240 days: 11 to 21); rawhide 3 | / 5 | resoled: yes |
| sack, chest, barrel | (standing) | none | / 3; 30; 10 (the barrel's leaking end of life, U5) | no |
| spear | acts (hunts) | 45 (21) | none | yes (the smith's, D2-46) |
| crude tool, copper tool | acts | 40 (19); 140 (65) | none | yes (copper: the smith's) |
| crude weapon | acts | 14 (7); a fight as D2-46 | none | yes |
| bedroll, tent | nights slept | 30 (real 200 to 500: 18 to 44) | / 5 (hide) | no |
| wooden plough | plots ploughed | 18 (wave1: 11 to 27) | / 10 | yes |
| handcart | (moves) | none | / 7 | no |
| smoke racks | (standing) | none | / 5; they burn with the house (U4) | no |

### 3.4 Mending (and barking)

- **The act:** `make mend` with the thing named or unnamed (unnamed: all of one's own of that kind held or placed at the place, U2's
  own-first rule, basis §6). One act mends all of one kind one holds at a place (a line of traps, a net and its floats).
- **What it does:** each piece mended gets back **half its full uses**, never above full, and **never any rot**: a net is mended,
  not remade, until it is rotten (hunt_fish_materials §5).
- **What it costs:** a tenth of the piece's materials each, and a fifth of the making's units for the lot, at the floor of 1 unit. A
  row may name its own mend inputs (a hand line 1 hook, a set line 15 hooks; shoes 0.05 leather, "resoled").
- **Who can:** the making craft is the mending craft. Known and capable mend at no risk; rough and aware mend at their class's odds
  (wave4 §4.2), and a failure spoils the mending materials, never the thing. Mending is practice of the craft (`tried`).
- **Barking a net** (`make bark nets`, practised, at a hearth): up to 4 nets a unit, each 0.5 bark and 0.25 firewood [e: a pot of
  oak bark boiled]; for one world year from that day the net rots at the barked rate (1 world year wet in place of 0.3). Barking never
  lowers the rot already used. Re-barked each year, a net lasts about three years in use, an untreated one under a year (fibre §4:
  weeks to a season untreated, two to four seasons barked).

**Real check** (wave2 §3.3): net mending is 10 to 20% of the netting time a season [n fibre §2], about half a unit a world year at
1/7; the rule gives 1 unit a mend (the floor), once or twice in a net's life. Inside the spread, with the floor's rounding up.

### 3.5 Results, in their words

- **A make within the batch:** "You made 2 wicker traps from 0.9 withies (1 unit). Each is good for about 20 nights set before it
  wants mending." Fewer than the batch: "You made 1 wicker trap from 0.45 withies (1 unit; the same unit would have made 2)."
- **A make above the batch:** "You made 6 wicker traps from 2.7 withies (3 units)."
- **A refusal for an input** (as today's form, D4-95): "Refused: make wicker traps: it needs 0.45 withies; you have 0.2 to hand
  (withies are cut from willow on wet ground or from a withy bed)."
- **A broken piece**, in the holder's own things (shown, not sensed: one knows one's own gear): "6 wicker traps (T4): 2 broken,
  wanting mending; the rest good for about 8 more nights set". On the night it breaks, the U2 tend result names it.
- **A mend:** "You mended your 6 wicker traps (T4) with 0.27 withies (1 unit): each is good for about 10 more nights set." Failed:
  "Your mending of the wicker traps went wrong and the 0.27 withies are spoilt; the traps are as they were. The rods split at the
  weave: they want soaking first." (the lesson, §5).
- **Rotten:** in the morning's own things: "Your gill net (T3) has rotted through in the water and is gone." "The bedroll in Reed
  House has rotted and is gone."
- **Barking:** "You barked 2 gill nets in the bark pot at Reed House's hearth (1 bark, 0.5 firewood, 1 unit): they will keep in the
  water a year."

---

## 4. What a person is shown of a craft, at each level (D2-263)

D2-263: at **capable and known**, a craft shows, where the person looks (their crafts in the system prompt, the make verb's line),
its inputs with its batch ("up to"), what it gives, its units and its place or fitting; at **rough**, its inputs as its card shows
them; at **aware**, its name only; basic crafts with no inputs show none. D2-251 adds the life and the season at known as the
specifics one who knows it well has. U9 places these lines under the act shapes (wave4 §2.2); this unit gives their content.

### 4.1 The line's form

- **known:** `{label} (known, {skill word}: {inputs}, {units} unit{s}{, at place}; gives {gives}{; life}{; season}{; lessons had as
  clauses}{; capability points held})`.
- **capable:** as known, with "works about {n} times in {d}" from the class (wave4 §4.2) and the class's extra materials ("about a
  fifth more withies").
- **rough:** `{label} (a rough idea: {inputs}{, at place}{; the lessons had}{; the next lesson missed, as "you have not yet ..."})`.
  The amounts are shown, as the card shows them today (`knowledge.py:379-383`) and D2-263 decides (Departure 6).
- **aware:** `{label} ({source})`. The source ("you have seen Nichola at it") is today's record field, not recipe content, so it
  stays (`knowledge.py:395`).
- **basic gathers with no inputs** (cut withies, twist cord, peel bark): the name and, at known, the season clause ("best in winter"),
  the craft's own fact since the yield the act reads depends on it. No inputs.
- **For whole things in batches:** "up to {b} {things} a unit, each from {inputs}". For bulk processes: "up to {inputs}, {units}
  units, gives {as much ...}".
- Numbers come from the data at the world's factor, never written into the line (so the staging moves them).

### 4.2 Rendered (at 1/7)

| Craft | Known | Capable | Rough | Aware |
|---|---|---|---|---|
| wicker traps | wicker traps (known, skilled: up to 2 traps a unit, each from 0.45 withies; anywhere; each good for about 20 nights set or 2 years in the water; soak the rods; a tight throat) | wicker traps (capable: up to 2 traps a unit, each from 0.45 withies, about a fifth more withies; anywhere; works about 4 times in 5) | wicker traps (a rough idea: 0.45 withies a trap, anywhere; you have not yet got the throat right) | wicker traps (you have seen Nichola at it) |
| a gill net | a gill net (known: 1 cord and 0.1 stone for sinkers, 4 units, at a house; gives a net good for about 25 nights set; bark it yearly or it rots in the water in about 10 nights) | as known, "works about 4 times in 5" | a gill net (a rough idea: 1 cord and 0.1 stone, at a house) | a gill net (you have seen one at the Marshes') |
| twist cord | twist cord (best in late summer and autumn) | | | |
| dress and spin | dress and spin (known: up to 1 retted flax a unit, gives 0.125 cord; at a house; best in winter) | as known, "works about 4 times in 5" | dress and spin (a rough idea: 1 retted flax a unit; the fibre tangles) | dress and spin flax (you have heard of it) |
| hurdles | hurdles (known: up to 5 hurdles a unit, each from 1 withies) | as known with the odds | hurdles (a rough idea: 1 withies a hurdle) | |
| mend | shown under each craft at its level: "mend: a tenth of the materials, 1 unit for all you hold at a place" | | | |
| shoes | shoes (known: up to 3 pairs a unit, each from 0.5 leather, or 0.3 hide as rawhide for a few days' wear; resole with 0.05 leather) | as known with the odds | shoes (a rough idea: 0.5 leather a pair) | |
| salt fish (a bulk process) | salt fish (known: up to 40 fish and 10 salt a unit, gives as much salt fish) | as known with the odds | salt fish (a rough idea: fish and salt, 4 to 1) | |

The tanning and peeling lines are U10 §2.7's.

### 4.3 Code

`knowledge.card` (`:368-386`) already shows inputs, places, units and gives at capable and known; it gains the batch ("up to b"),
the per-piece form, the life and season at known, and the lessons. `knowledge.crafts_lines` (`:389-409`) lists names and sources
only, so D2-263 is not built (crafts_evaluation's finding, re-checked on main 22 Nov, D2-287): it renders each known and capable craft
through `card`'s known and capable form, rough through its rough form, aware as now. Nothing here sorts or lists today's options
(`knowledge.options`, `:412-432`), which D2-286 removes.

---

## 5. Learning data for each craft (the fields U9 asks of this unit)

Classes and parameters are wave4 §4.2 (lifespan 64, D2-267); lessons from learning_times §2 and §5 where it has them, the rest [e].
Profiles over the seven aptitudes (H hands, F fire, B beasts, W water, G growing, S structure, D dealing).

| Craft | Class, curve | Profile | Lessons (the first is the main input) | Capability points |
|---|---|---|---|---|
| cut withies | simple, shallow | G.6 H.4 | the rods are cut when the sap is down (season); cut the stool clean and low (step) | |
| twist cord | simple, shallow | H1 | the strands one way, the wrap the other; even strands, long overlaps; stems retted and dried | |
| sow and pull flax | simple, shallow | G1 | pulled by the root, not cut (step); pulled when the stems yellow at the foot (season) | |
| ret flax | simple, shallow | W.6 G.4 | still water or the grass, not the open river (place); lift it when the stems part from the fibre (step) | |
| dress and spin | practised, steady | H1 | too thin, the spindle drops; wet fingers and a dressed distaff; too much twist | fine twine (0.6): a gill net in 3 units in place of 4 |
| dress a kill | simple, shallow | H.6 B.4 | cut shallow at the belly; the blade to the hide; open and cool it at once | |
| wicker traps | practised, stepped | H.8 W.2 | the rods soaked or green; butts and tips turned about; the throat to a finger's width | a tight throat (0.5): traps hold a fifth more (U2 reads it) |
| hurdles, creels, baskets, pack baskets | practised, steady | H.8 S.2 | twist each rod at the end post; uprights a forearm apart; beat the weavers down | |
| netting (gill, fowling, dip) | practised, steady | H1 | knots drawn hard to the mesh stick; pulled tight; good tight cord | |
| leather work (frame, harness, shoes) | practised, steady | H1 | leather wetted before it is shaped; stitch close at the strain; rawhide for a season only | a turnshoe (0.4): shoes; before it, straps and harness only |
| bark nets | simple, shallow | F.6 W.4 | the bark boiled to a dark liquor (step); the net dried before it is barked (step) | |
| mend | the thing's craft | the thing's | the thing's | |

**Summer rods:** a trap made of withies cut in summer is a crude result, not a failure: it lasts half its uses (green summer rods do
weave, but crack sooner; learning_times §5). The state holds the cause (the withies' cut season, kept on the lot of withies as
`summer: share`), so the line says it: "the traps are made, but the summer rods are brittle and will not last". Tanning's lines are
U10 §2.7's.

---

## 6. A fishing household's year, re-derived

Two adults, 384 units a world year (basis §1). Lives of §3.3; units of §2.2. A household sets 12 traps and one gill net about 16
nights a world year [e: the autumn run and the summer shallows] [m, scratch `u3/calc2.py`].

| | Wild cord, wild willow, barked net | Flax and a bed, barked | Wild, net untreated | Flax and a bed, untreated |
|---|---|---|---|---|
| traps replaced a year (rot: 16 of 64 wet nights, 16 dry nights of 5 years) | 4.2 | 4.2 | 4.2 | 4.2 |
| withies (traps, mending, creel, baskets, pack basket, racks' share) | 4.2 bundles, 2.8 units cut | 4.2, 1.0 | 4.2, 2.8 | 4.2, 1.0 |
| nets a year (a barked net 32 nights in water, an untreated 10) | 0.5 | 0.5 | 1.6 | 1.6 |
| cord a year (nets, lines, a set line's share) | 0.7 kg, 17 units | 0.7 kg, 7 units | 1.8 kg, 45 units | 1.8 kg, 18 units |
| barking (5 kg of bark bought) | 1 unit | 1 | | |
| making and mending in all (with the house's 3.9) | **33 units (8.5%)** | **21 (5.4%)** | **64 (16.6%)** | **35 (9.2%)** |
| at 1/15 | 31 (8.0%) | 19 (4.9%) | 60 (15.5%) | 31 (8.1%) |

- **The barked net halves the household's making.** Untreated cord rotting in ten nights in the water costs a wild-cord household 30
  units a year more than buying 5 kg of bark. Barking is the strongest tie between the fisher and the tanner's peeler in this design.
- **The flax switch** saves 10 to 30 units a household-year, 3 to 8% of it; materials stay 40 to 75% of making (W2-1).
- **The cord need** is 0.7 to 1.8 kg a year, so flax is a strip (§1.3), not a field; the proposal's 1 to 3 kg holds only for an
  untreated net (K5, K11).
- **The start binds hardest:** a household with nothing in late summer (the runs world opens on summer day 4) spends about 56 of its 80
  units in the five days before the first run making 12 traps, a creel and a net (wave2 §5.1, whose making it re-checks on these
  units: the traps' 3 units and the net's 4 are unchanged at 1/7). The gate check warns of it (§7, M3); U11 seeds gear by livelihood.

---

## 7. The gate check at world build (the making part)

`landgen/gates.py` today tries only gather and work (`:45`), so no making chain has ever been probed (wave2 §4). This adds a check run
when a world is built and a probe that tries every make and build. Each coupling is on by default and is turned off only by an
explicit setting in the world's spec (D2-270): `gates: {making: false}` for all, or `gates: {M4: false}` for one. The check runs only
for a world whose packs include the materials pack, so the worlds written before it keep running (hunt_fish_materials §11). U11 calls
it with the world part of the check (household_skills §2.3).

```python
# cybertron2/landgen/gates.py (37.2)
from dataclasses import dataclass

@dataclass
class Finding:
    check: str          # "M1" .. "M8"
    level: str          # "refuse" | "warn" | "report"
    village: str
    household: str | None
    text: str           # the line written to the build report, in plain words

def making_gates(w, spec) -> list[Finding]:
    """The making chains' gates at world build (u3_making.md §7). Reads the built world `w` and its spec; changes nothing."""
    off = (spec.get("gates") or {})
    if off.get("making") is False or not PK.on({"pack": "materials"}, PK.of(w)):
        return []
    reach = within_a_day(w)                     # {node: set of nodes one day away or less, by road}
    src = sources()                             # {good: [(technique, what it needs)]}, from TECHNIQUES' gives and yields
    out = []
    for hh in households(w):
        crafts = livelihood_crafts(w, hh)       # the household's livelihood rows' crafts (household_skills §1), with core/secondary
        for tech in crafts:
            for good, need in inputs_of(tech):  # each input at one act's batch
                if not source_within(w, reach, hh, good, src):           # M1
                    out.append(Finding("M1", "refuse" if crafts[tech] == "core" else "warn", village(hh), hh,
                        f"{name(hh)}: {label(tech)} needs {good}, and none is to be had within a day: no {where_from(good)}"))
        if grows(hh, "flax") and not held_within(w, reach, hh, "flax seed"):                          # M2
            out.append(Finding("M2", "refuse", village(hh), hh, f"{name(hh)} grow flax, and there is no flax seed within a day"))
        for gear, need_day, units in season_needs(w, hh):                                             # M3
            if not seeded(w, hh, gear) and units > spare_units(w, hh, w.day, need_day):
                out.append(Finding("M3", "warn", village(hh), hh,
                    f"{name(hh)}: {gear} needed by {day_words(need_day)}; materials out of season; about {units} units to make"))
        if cuts(hh) and not (has_tool(w, hh) and stone_within(w, reach, hh)):                         # M4
            out.append(Finding("M4", "warn", village(hh), hh,
                f"{name(hh)}: no stone within a day: crude tools cannot be remade once these wear out"))
        for proc in processes_of(crafts):                                                             # M5
            site = process_site(w, hh, proc)    # retting water or a pit; a tan-pit site by water with the parcels below it
            if site is None:
                out.append(Finding("M5", "refuse", village(hh), hh, f"{name(hh)}: no {proc_site_words(proc)} within reach"))
        for tech in crafts:                                                                           # M6
            if not knower_or_teacher(w, reach, hh, tech, level="capable"):
                out.append(Finding("M6", "refuse" if crafts[tech] == "core" else "warn", village(hh), hh,
                    f"{name(hh)}: no one capable of {label(tech)} in the house, and no teacher within a day"))
        for tech in crafts:                                                                           # M7
            least = least_input(tech)            # a work's whole need: the bed's 30 bundles, a pit's 20 hide units, a plot of flax
            if least.units_to_gather(w, hh) > season_units(w, hh, least.season):
                out.append(Finding("M7", "warn", village(hh), hh, f"{name(hh)}: {least.words} is more than the house can gather in its season"))
    out += probe_making(spec)                                                                         # M8
    return out
```

- **`source_within`** is true if, at a node within a day: a gather or work technique that gives the good has its cover there and a
  stock above nothing (`draws`); or a make that gives it has each of its own inputs so (two steps deep at most); or a store holds at
  least one act's batch; or a household there holds the producing craft at capable. "Within a day" is road distance of a day or less,
  as `gates_making.py` reads it.
- **`season_needs`** comes from a small table on each livelihood row (household_skills §1): the fisher's traps and a net before the
  first run night of the year (`wild/runs.py`), the tanner's bark before the season ends, the flax grower's seed before spring. The
  units are §2.2's at the world's factor, the materials' rates at their season between the world's start and the need.
- **`probe_making(spec)`** (M8) extends `probe()` (`gates.py:30-97`): for each make and build technique the world's packs switch on, at
  each village, the best-suited person tries it on a fresh copy of the world **with its inputs put into their hands** (one act's batch)
  and, if it is done at a fitting, at a building of theirs that has it or a copy given one. A refusal that is not situational
  (`SITUATIONAL`) or a crash is reported: it is the code's gate, not the world's.
- **Refuse** means the world is not run as written: `World` raises at build with the findings; **warn** and **report** go to the
  build report (`out/<world>/gates.json`) and the first line of the run's log.
- The probe of 22 Nov (wave2 §4.3, `wave2_making/gates_making.py`) is what this would have found: wild cord everywhere; flax seed
  nowhere (M2 refuses any flax livelihood until U11 seeds it); Eelmouth fails M4 (no rock), M3 (no gear on summer day 4); Wenbridge's
  river borders no parcel (a data fault, U11).

---

## 8. Code changes

| File, line | Change | Owner |
|---|---|---|
| `engine/data.py` ITEMS `:20-115` | new goods (withies, cord, flax, retted flax, flax seed, bone, bark, leather, pelt) and items (§2.2) with weight, `hours`, `clock`, `uses` (real count and its kind: act, night, used), `rot` (wet, dry); the rows of §2.3; `pack` removed | 37.2 |
| `engine/data.py` CROPS `:137-147` | `flax` (§1.3) with `seed_kg`, `strip`, `also` | 37.2 |
| `engine/data.py` RESOURCES `:179-205` | `willow` (seasonal; K by cover, summer harm, grazing) | 37.2 |
| `engine/data.py` TECHNIQUES `:413-716` | cut withies, twist cord, pull flax, dig a strip, dress and spin, dress a kill, mend, bark nets; every make row of §2.2 on `hours`; O-2's eleven with `batch` (§2.4); `slaughter` hide by weight | 37.2 |
| `engine/data.py` DECAY `:117-136` | `hide` as a base with hazards (§1.4); `bark`, `withies`, `leather`, `cord` rows | 37.2 |
| `engine/data.py` TRY `:730` | replaced by the classes (U9, wave4 §4.2); each row of this unit carries its class | 37.2 (data), 37.4 (the read) |
| `engine/clocks.py` | `capital_units(hours, w)` and `batch_of` (U0's conversion; stage 1); `RATES` gains `ITEMS.*.uses`, `ITEMS.*.rot.*` | 37.4 (U0) |
| `engine/verbs.py` `cost` `:142`, `:156` | `units x ceil(qty / batch)`, at least 1 (§2.1) | 37.4 |
| `engine/verbs.py` `_make` `:760-856` | `qty` as pieces; one act makes up to its batch; inputs whole a piece; the result lines of §3.5; the `of` field set by the input used (leather or rawhide); summer rods as a crude result; a failure by the class (U9) | 37.4 |
| `engine/verbs.py` VERB `:23-24` | `build`'s fixed 2 units become what the work needs, at least 1 (U7's table) | 37.4 |
| `engine/world.py` `p_wear` `:686-694` | wears a piece; at 0 uses the piece is broken, not destroyed | 37.4 |
| `engine/gear.py` (new, the feature unit, D2-244) | pieces: create, move, wear, rot each night by condition, mend, bark; the own-things lines | 37.2 (37.4 named) |
| `engine/night.py` | call `gear.rot_night(w)` once a night, after the wild and before the morning's lines | 37.4 |
| `engine/knowledge.py` `card` `:368-386`, `crafts_lines` `:389-409` | §4 | 37.4 |
| `engine/farm.py` `:228-300`, `_sow` `:922-1023`, `_reap` `:1128-1166`, `ready` `:1191-1249`, `target` `:624` | strips (§1.3): the record, sowing into a strip, growth, targeting by crop name, pulling, the soil step, trampling, the holding's words | 37.2 (37.4 named) |
| `wild/kinds.py` TAKEN `:631-657` | the kill's hide, bone and tallow given by dressing; pelts | 37.2 |
| `landgen/gates.py` | `making_gates`, `probe_making` (§7) | 37.2 |
| `engine/data.py` `cut` `:434` | aliases moved (§2.3) | 37.2 |

---

## 9. Tests

**Unit tests** (each with the world's factor set to 1/7 and to 1/15):
- `cost` gives 1 unit for 1 or 2 wicker traps at 1/7, 2 units for 3 or 4; 1 unit for up to 5 at 1/15; a gill net 4 and 2. No recipe
  costs 0 (E6). `qty` counts pieces.
- O-2's eleven: each takes up to its batch; less takes the same units; the water mill grinds 30 grain.
- A piece record: made with full uses and rot 0; a night set takes a use and adds wet rot; a dry night dry rot; at 0 uses broken and
  kept; at rot 1 gone with its line; mending restores half the full uses, never rot; a failed mend spoils only the materials;
  barking sets the wet rate for a world year and never lowers rot used.
- Moving pieces: give, take, set and take up keep each piece's record; the most worn leaves first.
- The strip: 0.3 flax seed sown on a holding with barley standing makes a strip and the barley stands; 3 kg makes flax the main crop
  on a bare holding; `pull flax` takes the strip; `reap` takes the barley; dig a strip on a meadow plot then sow; frost kills a strip
  as a crop; the soil steps by area.
- D2-263's lines for each level for every craft of §2.2, and that no line carries a number not in the data.
- `making_gates` on a toy world: a fisher household with no wet ground refuses M1; flax without seed refuses M2; a world with
  `gates: {making: false}` returns nothing; M8 catches a make refused for a code reason (a test fixture with a broken row).

**Bot interface tests** (D2-298: interfaces and basic functioning only): a bot cuts withies, makes traps, sets and tends them (U2),
mends them, lets a net rot unbarked and barks another; a bot sows a flax strip, pulls, rets (U4), spins. Read: every act's result
line, no free act, no crash, replay with no mismatch.

**What live runs should read** (D2-297, with the rest of the wave): whether households make gear before the run when they know they
must; whether fishers buy bark for their nets; whether any household grows a strip of flax or buys cord; whether a withy bed is
planted where a weir stands; the share of units spent making against §6, read against the null arm and with a qualitative
end-state reading (scenario_design §6).

---

## 10. Basis rows needed

| Row | Value | Mark |
|---|---|---|
| **The area of a unit of size** | the land's cell is about 2 ha (`landgen/field.py:3`), while a field's plot yields as about 0.1 ha (16 seed, 64 grain; wave1 §1.2): two scales in one word | **open**: this spec uses 2 ha for land stocks (willow) and 0.1 ha for a plot's yield (flax), and says so |
| Units and batches from real hours | units = hours x f / 2 (capital), hours / 2 (day); at u >= 1, round(u) for one piece; under 1, 1 unit for up to floor(1/u) | default (§2.1) |
| Lives' three counts | acts at f; nights at 1/11.4; used-up things (day clock) at real uses | default (extends basis §1 "Lives") |
| Rot by material, wet and dry | withies 2 / 5; cord untreated 0.3 / 5, barked 1; cord on land 2; leather 7; rawhide wet 2; timber goods 7 to 30 (§3.3) | default |
| Mending | half the full uses, never rot; a tenth of the materials; a fifth of the making's units, floor 1 | default (hunt_fish_materials §5; wave2 W2-4) |
| Weights of the new goods | leather 1, bone 1, flax straw 1, retted flax 1, flax seed 1, pelt by kind 0.3 to 2; gear a piece as §2.2 (wave1 §1.7) | default |
| Hide units by beast | red deer, boar, a young beast 1; roe 0.3; cow 3.5; ox and bull 4; bear 3; small furs a pelt | default (extends basis §2 "Hide") |
| Keeping of the new goods | hide 0.85% a night, bark 0.44%, withies 0.85%, leather and cord 0.09%, bone none (D2-289's curve) | follows D2-289; the shelf lives [e] |
| Seasons of the materials | cut withies winter 1, autumn 0.8, spring 0.5, summer 0.3; twist cord summer and autumn 0.04, spring 0.03, winter 0.01 | default |
| Dung's unit | a barrow-load of 50 kg (a plot's 10 dung is 0.5 t; wave2 §1.1) | default |
| Hay making | 7 hay (10 kg) a unit in summer, 35 kg an hour all in (wave2 §1.1) | default |
| Copper ore and smelting's charcoal | ore 3 to 1 kept; 1 charcoal (20 kg) a smelt, 2 to 6 times a small furnace's fuel, a named departure | default (wave2 §1.1) |

---

## 11. Gaps

**Designed here:** batches of whole things and the floor (W2-6); two lives and mending (W2-4); the strip below a plot (W2-2); wild
willow as a stock (W2-9); hide by weight and pelts (W2-12); the gate check's making part (M1 to M8); the piece record U2 shares;
O-2's eleven.

**Deferred, with what each waits on:**
- **Parts with their own lives** (a frame's straps, a net's floats, a tool's haft): wait on a part model; for now one life a thing.
- **A twine good** for nets (W2-11): waits on Zach's answer; folded for now.
- **Cloth and the loom** (sacks of cloth, W2-19): with clothing (D2-10 parked).
- **The bow, arrows, sinew, feathers, the stave's seasoning:** after this wave (wave2 §6).
- **Fencing a strip and the bed:** fences priced by length and the dead hedge (U7, G8).
- **Boards and poles** (the chest's boards, the barrel's stave bolt, `cut poles`): the timber economy (W-76).
- **The seine and boats:** later (hunt_fish_materials §12).

---

## 12. Open questions for Zach

**Whether materials made only to feed lasting things (cord, withies, bark, leather) stay at real hours, which makes a net's cord
cost about four times its knotting (W2-1).** D2-276 keeps materials real and the making at the factor, so materials are 40 to 75% of
a fishing household's making (§6) where real life has them nearer half. Options: (a) keep, named: cord and withies become the goods
worth trading, and flax and a bed save 10 to 30 units a household-year; (b) price a material whose only use is capital at the factor
too, which makes cord nearly free and the flax switch small; (c) a middle lever on material rates. **Recommend (a).** Blocks: every
material rate in the data.

**Whether a household may grow flax in a strip on a held plot, below a whole plot, as designed in §1.3 (W2-2).** Default taken: both
the strip (up to a quarter of a plot, as a second crop on a holding) and the whole plot as a supplier's crop. The alternative is
flax by whole plots only, which makes every flax household a region's supplier bound by spinners. **Recommend the strip and the
plot.** Blocks: flax in the data and `farm.py`.

**Whether set gear, bedrolls, tents and shoes count their uses in nights at the calendar's 1/11.4, while tools count acts at the
factor (G14; basis §1 "Lives", open).** Default taken: nights at 1/11.4 (a trap 20 nights set, a barked net 25). At 1/7 a trap would
outlast its rot in ordinary use, and the net's life would decide whether a household needs 1 kg of cord a year or 10 (K5). Options:
(a) nights at 1/11.4, acts at the factor; (b) everything at the factor. **Recommend (a).** Blocks: the life table (§3.3) and the
cord need.

**Whether gear moves to the 1/15 stage with the works, on one factor, rather than going straight to 1/7 (K7).** Default taken: one
factor for all capital, read from the world, so at 1/15 a trap line is 1 unit for up to 5 and a net 2 units. Options: (a) one factor
at each stage; (b) gear at 1/7 at once, works staged. **Recommend (a).** Blocks: the first stage's numbers, every craft line's units.

**Whether a rough idea shows a craft's inputs with their amounts, as D2-263 and today's card do, or only the main input, as wave4
proposes (W2-17).** This spec follows D2-263 (amounts shown). Options: (a) as decided; (b) the main input only at rough, amounts from
capable, since amounts at rough make the level read as known and the lessons are what rough should hold. **Recommend (b) if you are
willing to revisit D2-263's wording, else (a).** Blocks: the craft lines' rough form only.

**What area a unit of size is (new; §10).** The land generator's cell is about 2 ha, but a field's plot yields like about 0.1 ha. Wild
stocks priced by area (the willow's rods, the shallows) differ by twenty times on the reading. Options: (a) name the two scales as a
departure (land at 2 ha, a plot's yield at 0.1 ha, a plot standing for a twentieth of the land it lies on); (b) re-scale plots to the
land. **Recommend (a) for this wave**, with the reading in basis.md. Blocks: the willow stock's K and U1's shallows by area.

**Whether rawhide stands in for leather in straps, harness, shoes and snares at a fraction of the life (W2-14).** Designed with it:
rawhide harness half the uses and 2 years' rot; rawhide shoes 3 days worn; rawhide snare thong rots on a wet night. **Recommend yes.**
Blocks: the leather recipes' alternatives.

---

## Sources

The repository: `cybertron2/engine/data.py`, `verbs.py`, `knowledge.py`, `wear.py`, `world.py`, `farm.py`, `clocks.py`,
`landgen/gates.py`, `landgen/field.py`, `wild/kinds.py`, read on main 22 Nov; `docs/cybertron2/DECISIONS.md` (D2-46, D2-52, D2-247,
D2-251, D2-263 to D2-298); `tools/records.py show O-2`; `proposals/hunt_fish_materials.md`, `trying_and_learning.md`,
`building_clock.md`; `proposals/w73_design/README.md`, `basis.md`; `docs/review/37_growth/02zzzh_hunt_fish/` wave2_making.md (and
its `wave2_making/gates_making.py`, `calc.py`), wave1_physical_basis.md, wave_conflicts.md, wave3_keeping.md §2, wave3_taking.md §1
to §2, wave4_people.md §2.2, §3.5, §4, fibre_and_cord.md, withies_wood_materials.md, byproducts_and_substitutes.md,
crafts_evaluation.md, learning_times.md, household_skills.md. The scratch sums for §2.2, §3.3 and §6 are in the session scratchpad
(`u3/calc.py`, `u3/calc2.py`), read-only. Every sourced figure ([s]) comes through those notes, which name their search sources; no
page was fetched for this spec.

*Current as of 22 Nov 2026 (W-85; nothing decided beyond the decisions cited).*
