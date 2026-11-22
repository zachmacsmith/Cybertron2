---
id: docs/review/37_growth/02zzzh_hunt_fish/wave2_making.md
kind: note
updated: "2026-11-22"
---
# Design wave part 2: materials and making (withies, cord and flax, bone, hide, bark and tanning; gear made, worn and mended)

*note · `docs/review/37_growth/02zzzh_hunt_fish/wave2_making.md`*


22 Nov 2026, 37.2 (subagent). Thread: design wave part 2, materials and making ([[W-83 Design wave part 2, materials and making|W-83]]), under fishing, hunting and their materials
([[W-73 Fishing, hunting and their materials developed together|W-73]]). A design note for review: no code, proposal, spec or record was changed, nothing was committed, and nothing here is decided.
The next wave is designed in full before it is built ([[D2-278 The next wave of the fishing, hunting and materials network|D2-278]]). This part is priced on part 1 (wave1_physical_basis.md, final), and
fits making to how crafts are shown and learnt in part 4 (wave4_people.md). Keeping (processing containers, stores) is part 3a's
(wave3_keeping.md) and taking (set and tend, the weir, snares) part 3b's (wave3_taking.md); this note points to them and does not
design them.

**Read with:**
- the decisions: recipes shown by level ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]), the network as answered ([[D2-264 The fishing, hunting and materials network|D2-264]]), household skills and the tanner row ([[D2-270 Household skills|D2-270]]),
  making durable things on the year clock ([[D2-276 Making durable things runs on the year clock|D2-276]]), tanning, bark, the pack basket and the frame, the factor's stages ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]),
  salting ([[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]]), racks at 250 kg a set ([[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]]), bulk processes "up to" their batch ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]), weapons wear ([[D2-46 Weapons wear|D2-46]]), skill by
  practice ([[D2-52 Skill by practice on all work|D2-52]]); the offer to make the eleven bulk processes take up to their batch ([[O-2 Make the eleven bulk processes take up to their batch|O-2]]); `spec/core/clocks.md`;
- the proposals: `hunt_fish_materials.md` (§3 to §7), `building_clock.md`, `trying_and_learning.md`;
- the notes in this folder: wave1_physical_basis.md (§1 units, §2 keeping curve, §3 making costs, §4 carrying, §5.4, §7), wave4_people.md
  (§2.2 crafts under shapes, §3.5.11 to §3.5.13 the basket maker, cord and nets, the tanner, §4 learning, §5 shapes),
  fibre_and_cord.md, withies_wood_materials.md, byproducts_and_substitutes.md, crafts_evaluation.md, learning_times.md,
  household_skills.md;
- the code on main, 22 Nov: `cybertron2/engine/data.py` (ITEMS, TECHNIQUES, FITTINGS, FORESTS, TRY), `verbs.py` (`cost`, `_make`),
  `knowledge.py` (`card`, `crafts_lines`, `batch_share`, `tried`), `wear.py`, `world.py` (`p_wear`), `wild/methods.py` (SETS),
  `engine/wild.py` (`set_work`), `farm.py` (plot shares), `forests.py` (`young_step`), `landgen/gates.py`.

**Marks.** As part 1: **[s]** sourced (search summaries only; page fetches were refused in these sessions), **[n]** from a sibling
note, named, **[m]** measured from the engine or computed from it, **[k]** a standard figure as I know it, not re-checked, **[e]** my
estimate with its reasoning. The probes and sums are in the scratchpad (`w2/gates_making.py`, `w2/calc.py`); they are read-only.

**Checked against [[D2-286 The list of what one could do today|D2-286]] and [[D2-287 Reviewing past runs|D2-287]]** (Zach, 22 Nov, after this note was drafted). Nothing here uses or sorts the "Today you could"
options list. What a person is shown of their crafts is part 4 §2, carried by §3.4 here. The two findings this note takes from past
runs (crafts_evaluation.md) were checked against main at commit fdefff0d and the current worlds' settings, and both still hold:
- the water mill takes 200 grain in one act with no batch (`TECHNIQUES["water mill"]`), so [[O-2 Make the eleven bulk processes take up to their batch|O-2]] is not built;
- the make lines show no inputs (`prompt._craft_note`, `knowledge.crafts_lines`), so [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] is not built.

Every other fault named here comes from today's code, with file and line, or from this note's own probe of the world files as they
stand, not from a run. No finding of a past run is reported here as already fixed: none of those cited has been fixed since.

**The basis** (part 1, unchanged): a unit is 2 hours; a person's world year is 192 units (spring 6 a day, summer 7, autumn 6,
winter 5, eight days each); two adults 384. Capital costs real hours × f ÷ 2, f = 1/7 (the target) or 1/15 (the stage before).
Materials and things used up in a handful of uses cost real hours ÷ 2. Withies, bark and firewood come in 10 kg bundles, timber
and stone in 25 kg loads, cord and leather by the kilogram.

---

## 0. In brief

1. **Every chain is priced end to end** (§2): withies wild, from coppice and from a withy bed; cord twisted wild or grown as flax;
   bone and antler from dressing a kill; hide dressed to rawhide or tanned to leather; oak bark peeled in late spring. Each has a
   way open to anyone with nothing and a way that needs land, a work, a season's wait or another group.
2. **Materials dominate making.** [[D2-276 Making durable things runs on the year clock|D2-276]] keeps materials at real hours and puts the making step at 1/7, so in the engine the cord in
   a net costs 64 to 93% of the net (real: 20 to 67%), and materials are 37 to 60% of a fishing household's making at 1/7 and 55 to
   76% at 1/15 [m, w2/calc.py]. The flax switch is worth about 2.5 times more in the engine than in life. This follows the decision
   rather than breaking it, and it makes cord and withies worth trading, but it is the largest effect of this part and the first
   question (W2-1).
3. **The share of a year spent making holds** (§5): a fishing household's steady making and mending is **7.7% of its year by wild
   cord and willow, 4.9% by flax and a bed**, against part 1 §5.1's 8% and 5%; at 1/15, 6.1% and 3.3%. A household starting from
   nothing in late summer spends about 56 of its 80 units in the five days before the first run making its traps and a net:
   making binds hardest at the start, as it should.
4. **Flax does not fit the engine's plots.** A household needs 0.5 to 1 kg of cord a year, 25 to 50 m² of flax; the engine's smallest
   holding is a whole plot (about 0.1 ha) of one crop (`farm.py:229-235`), which gives 30 to 50 kg of cord and 240 to 400 units of
   spinning, more than a person's year. And no world anywhere holds flax seed [m, probe]. Flax as "a close" ([[D2-264 The fishing, hunting and materials network|D2-264]]) needs a
   garden share smaller than a plot and seed in the world (W2-2, W2-3).
5. **Gear has two lives**: uses (sets, acts, days worked, at 1/7 of the real count) and rot (world years, by material). Mending
   restores uses, never rot (§3.3). Today no gear exists: sets cost nothing and last 4 or 8 nights (`wild/methods.py:86`,
   `engine/wild.py:909`), and only tools, weapons, the plough, tent and bedroll wear (`world.py:686`).
6. **Batches of whole things**: a recipe states its batch (5 hurdles a unit) and a make of fewer costs the same unit, the "up to"
   rule of [[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]] carried to things made whole. `verbs.cost` truncates a recipe's units before multiplying by the quantity
   (`verbs.py:142`, `:156`), so every recipe under one unit is free today: about 30 rows of this wave would be (W2-6).
7. **Tanning is a by-trade of a market village.** A village of 12 wears out 24 to 49 pairs of shoes a world year (4 to 8 hide units
   of leather), far more than its frames, harness and bellows. A peeler in a 5 to 6 night bark season supplies about 20 to 27 hide
   units; a tanner handling 15 hide units a year spends about 47 units, a quarter of one person's year. The bark season's length
   sets the trade's scale (W2-5); shoes set the demand (W2-7).
8. **Gates** (§4): a read-only probe of 94 villages in 52 world files finds wild cord reachable in all, coppice rods in 91,
   withies from wild willow in 49, hides in 76, tanning in 55 (if a forest without a named species counts as oak), copper hooks in
   38, stone to remake a crude tool in 38, and flax in none (no seed). The runs world's Eelmouth can make every wild chain but has no
   rock: once its three crude tools wear out, no one can remake one. The gate probe tries only gather and work (`gates.py:45`), so
   no making chain has ever been probed.
9. **Questions** (§9): nineteen, each standing alone; the five that matter most are at the end of the reply and of §9.

---

## 1. What this part settles, and the rules it uses

### 1.1 What part 1 handed on (§7 of part 1), and the answer here

| Handed on | Answer here | Where |
|---|---|---|
| leather's uses (frame, harness, bellows, shoes) | priced; shoes set the demand | §3, §5.2 |
| tanning's lime | wood ash from any hearth, folded into the liming nights (no good) | §2.4 |
| pelts as a good | one good, `pelt` (fox, stoat, otter, beaver), trade only for now; snares and den work give pelts, not hide | §2.4 |
| hay-making rate (2 to 3 times low) | 7 hay (10 kg) a unit in summer, about 35 kg an hour all in, against today's 3 | §2.7 |
| dung's unit | a barrow-load of 50 kg [e]: a plot's 10 dung is 0.5 t (about 5 t a ha, a light medieval dressing [k]); gathering 5 a unit is 125 kg an hour of forking [e]; a housed head's 20 a year is 1 t | §2.7 |
| green fodder and `dry fodder`'s mass | green crop 0.035 fodder a kg (a beast's day is about 30 kg green [e]); `dry fodder` takes up to 30 green to 1 hay (10 kg), not 10 to 8 | §2.7 |
| copper ore's grade, smelting's charcoal | ore at 3 to 1 kept (a rich oxide ore, named); the charcoal kept at 1 (20 kg) a smelt, which is 2 to 6 times the fuel of a small furnace [e]: a named departure, or 0.5 | §2.7 |
| the brine pan's copper | 10 copper (a pan of 10 to 30 kg [e]; real pans were lead, which the engine lacks), mend 0.25 copper | §3.2 |
| the cheese rate | up to 20 milk and 0.6 salt a unit, giving 3.3 cheese (part 1), "up to" with [[O-2 Make the eleven bulk processes take up to their batch|O-2]] | [[O-2 Make the eleven bulk processes take up to their batch|O-2]] |
| the cooper (barrels) | the barrel as part 1 §3.3 (7 timber of stave bolt, 0.3 withies of hoops, 1 unit); the cooper a specialism of the wright, with [[W-76 The timber economy|W-76]]; what a barrel keeps is part 3a's | §3.2, §7 |
| bow, arrows, spear | the spear (a copper head) now, a smith's tie; the bow and arrows later, with sinew, feathers and the stave's seasoning | §6 |

Part 1's contradictions that fall to this part (its §5.4): #8 (withies at 10 kg: taken), #9 (small recipes in timber: every recipe
here is restated in kilograms), #10 (hide by weight: §2.4), #13 and #14 (the proposal's gear prices and the 10 to 20% share: §3
and §5), #17 (lives in nights: §3.3), #23 (the brine pan's copper), #27 (lives of the plough, tools, handcart and pack: §3.3).

### 1.2 Rules used throughout

1. **Materials at real hours, making at the factor** ([[D2-276 Making durable things runs on the year clock|D2-276]]). A material (withies, cord, retted flax, bark, leather, bone, hide) is
   a good got at real hours whatever it goes into. The making of a lasting thing is real hours × f.
2. **A recipe never exceeds a day.** An act's units come out of one day (5 to 7). A material whose real hours run to days is made
   by the unit: dress and spin takes up to 1 retted flax a unit (0.125 cord), not 8 retted flax in 8 units. A thing whose making is
   more than a day (a seine, about 36 units) is built over days like a building (later).
3. **Batches.** Each recipe states the units of one act and what one act gives at most (its batch). A make of fewer gives fewer for
   the same units ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]], carried to whole things). A make of more is several acts (`qty`). The cost is `units × ceil(qty ÷ batch)`.
4. **Two lives** for lasting things: uses at 1/7 of the real count, and rot in world years (real years as world years, [[D2-276 Making durable things runs on the year clock|D2-276]]).
   Whichever comes first ends it. Things worn by nights (bedroll, tent, shoes on days walked) count calendar days at 1/11.4 (part
   1's open question 4).
5. **Mending** restores uses, never rot; it costs a tenth of the materials and about a fifth of the making (§3.3).
6. **Classes and lessons** (part 4 §4): every craft row carries a class (simple, practised, skilled), a curve shape, a profile over
   the seven aptitudes, two to four lessons with their failure lines, and capability points where they open something.
7. **Shown by level** ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]): at capable and known, the inputs with the batch ("up to"), what it gives, its units and its place or
   fitting; at rough, the inputs as the card shows them; at aware, the name only; basic crafts with no inputs show none.

---

## 2. The material chains, end to end

### 2.1 Withies

**What a bundle is.** 10 kg of green rods: about 25 hazel rods of 2 to 3 m or a hundred fine willow rods [n withies §3.1]; dried,
about 5 to 6 kg [e]. One good for willow and hazel; the species is words.

**Three sources.**

| Source | Where | Rate (bundles a unit) | Season | Stock | Capital | Real anchor |
|---|---|---|---|---|---|---|
| **wild willow** | fen, alder carr, reedbed, wet grassland, and any meadow, pasture, scrub or wood parcel bordering water (a bank) | **1.5** with a crude tool; bare hands 0.5; a copper blade 2.0 [e: the withies note's 0.3 bare-handed is for no blade at all; a knife cuts rods] | winter 1.0, autumn 0.8, spring 0.5, summer 0.3 of the rate (sap down in winter) [n withies §3.3] | the rods are a yearly crop on stools (below) | none | scattered, crooked rods; perhaps a third of a bed's rate [n withies §1.1, est.] |
| **coppice rods** | a managed wood (hazel); any wood or scrub at the wild rate | 4 in a managed wood; 1.5 elsewhere | winter as above | the wood's young growth: a bundle of rods draws 1 bundle-mass of young growth (10 kg), shared with `cut` for firewood | the managed wood (exists) | Durham: about 10,000 rods an acre at the cut, about 300 hurdles [s via withies note]; hazel on a 7-year cycle [s, Rackham via withies note] |
| **a withy bed** | a work on a wet parcel the household holds | 4 | as above | about **30 bundles a year** at full yield: none in its first world year, half in its second, full from its third ([[D2-264 The fishing, hunting and materials network|D2-264]]), for about 30 years | build: 1.5 units at 1/7 (1 at 1/15), 1 withies of cuttings; a fence or dead hedge against beasts | 13 to 20 t a ha a year green [s, USDA bulletin 622 via withies note]: 200 m² gives 260 to 400 kg, 26 to 40 bundles [m] |

**Wild willow as a stock** (proposed). Willow rods are a one-year crop on long-lived stools, so the stock is two-level, not one
logistic pool:
- the **stools** set the year's capacity: about **60 bundles a unit of size of fen or carr, 20 of a bank parcel** [e: a fen is mostly
  reed and sedge with willow at its edges; this is about 0.3 t a ha a year of usable rods, a fiftieth of a bed's rate; I do not
  know the real figure, and it is the lever that decides whether wild willow binds];
- the **rods** regrow to the stools' capacity each year (the `seasonal` renewal the plants use), cut down by cutting;
- **summer cutting harms the stools:** each bundle cut in summer lowers the capacity by a tenth of a bundle [e]; **grazing** halves the
  year's growth on a parcel beasts graze, as young growth already stops (`forests.py`, [[D2-156 A forest is three stocks|D2-156]]);
- the capacity recovers toward its base at the young-growth rate when unharmed.

This is better than the young-growth regime (`forests.young_step`, logistic at r = 1 a year), whose most sustained take is a
quarter of the stock a year: a one-year rod is not a slow-growing stock. Real wild willow is hard to exhaust and easy to kill by
grazing [n withies §2.1]; the two-level stock says exactly that.

**The village's demand against the supply** (Eelmouth's land: fen of size 3 and two bank parcels; three households) [m, w2/calc.py]:

| Use | Bundles a world year |
|---|---|
| traps (12 a household, 6 replaced a year) | 8.1 |
| creels, rods, baskets, pack baskets | 1.6 |
| smoke racks (a set a household, every 5 years) | 1.2 |
| wattle houses' upkeep and rebuilding | 8.0 |
| a wattle weir of four sections (6 a section a year, [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] and part 1 §3.7) | 24 |
| hurdles for folds, or a bed's fence (a share) | 3 |
| **all** | **46** |

- Supply from the stools at full: about 220 a year. **At Eelmouth wild willow does not bind; labour and season do:** 46 bundles take 31
  units of winter cutting wild, or 11 from beds (about 1.5 beds).
- **Where it binds:** a village with one bank parcel (20 a year) cannot keep a wattle weir by wild cutting. It plants a bed, buys
  rods, or builds the weir in timber (wear 0.5, no withies). This is the chokepoint the network wants: wet ground held, or bought rods.
- **The weir dominates withy demand** (half of all). A timber weir (the high arm's) needs none.

**The switch:** a bed saves about 20 units of cutting a year for the village and costs 1.5 units, a bundle of cuttings, a fence and
two years' wait. At 1/7 the switch is cheap; what binds it is wet ground held and the wait.

**The bed's fence.** 31 hurdles round 56 m (withies note) is 31 withies and 6 units at 1/7, four times the bed. A dead hedge of cut
thorn and brush is 1 to 2 units for 56 m (part 1 §3.7) and lasts 2 to 3 world years. Both should be allowed (W2-13).

**Merges, substitutes, competition.** Withies feed traps, creels, baskets, the pack basket, hurdles, smoke racks, the weir's
wattle, wattle rooms (35 a cottage, part 1 §3.5), the keep box, barrel hoops and the fishing rod. They compete with:
- **firewood** for the same young growth in a managed wood (`cut` and coppice rods draw one stock; firewood is cut in any season,
  rods best in winter);
- **grazing** for wet ground (beasts on the bank kill the stools; a bed needs a fence);
- **timber** as the weir's material (wattle sections need 12 withies and 7 timber; timber sections 40 to 80 timber and no withies).

### 2.2 Cord: wild fibre against flax

**The good.** `cord`: 1 kg of cord, twine, line or light rope; rope is cord by weight (fibre note §9.1). One good (W2-11 asks whether
fine twine should be its own).

**Wild cord** (gather, simple, untaught tryable).

| | |
|---|---|
| Where | nettle on rich, disturbed ground: built ground, middens, field edges, wood edges, alder carr; lime and willow bast from coppice poles and wet ground |
| Rate | **0.04 cord a unit** in summer and autumn (nettle), 0.03 in spring (bast, which also wants a retting the twist cord act folds in), 0.01 in winter (standing stems retted by the weather) [n fibre §9.2]: 25 units a kg |
| Real anchor | nettle fibre 15 to 50 g an hour picked and stripped [s, practitioners via fibre note]; hand-twisting 25 to 50 g an hour [e]; **35 to 80 hours a kg** [n fibre §2] |
| Stock | none: nettle and bast are not scarce for cord at these rates (a village twists a few kilograms a year) [e]. Spring nettle shoots taken as greens are the same plants; leave the competition as words |
| Tools | bare hands |
| Quality | coarse, strong enough for snares, lines, lashings and a coarse net (the Mesolithic Antrea net was willow bast [s via fibre note]) |

**Flax** (four acts on the farming verbs and one make).

| Step | Shape (part 4) | What | Rate | Clock and season | Real anchor |
|---|---|---|---|---|---|
| sow flax | work | on a field plot or a garden share (W2-2), with flax seed | as grain's sowing; seed about 10 kg a plot (100 to 120 kg a ha for fibre [k]) | spring | |
| pull flax | work | pulled, not cut | about 25 m² an hour [e: 15 to 25 person-days a ha, fibre note]: a household's 50 m² is under a unit | summer, about 100 days after sowing (a season in the engine) | |
| ret flax | set and lift (part 3a's processing container) | in water 1 night, on grass 3 to 4 | 1 unit to lay, 1 to lift, up to 50 flax a batch | late summer | water 1 to 2 weeks, dew 3 to 6 [n fibre §2]; retting in water fouls it ([[D2-264 The fishing, hunting and materials network|D2-264]]; §7.5 of the proposal; part 3a) |
| dress and spin | make (practised) | break, scutch, hackle, spin and ply in one act | **up to 1 retted flax a unit, giving 0.125 cord**: 8 units a kg | best in winter | 15 to 20 hours a kg of coarse 2-ply [n fibre §2] |

**The mass chain.** 10 kg of pulled straw → 8 kg retted → 1 kg cord [e]. The proposal's 0.7 retted from straw with 8 retted a cord
(11.4 kg of straw a kg) and the fibre note's 8 kg of straw a kg of fibre differ by 40%; scutched fibre is 12 to 15% of retted straw
[n fibre, via part 1 §1.6] and retting loses perhaps 15 to 20% of the dry straw [k]. 10 to 8 to 1 sits between them.

**What a close is** [m, w2/calc.py, at 3 to 5 t of straw a ha]:

| Cord a year | Close | Pull | Ret | Spin |
|---|---|---|---|---|
| 1 kg | 20 to 33 m² | under an hour | 2 units | 8 units |
| 2 kg | 40 to 67 m² | about an hour | 2 units | 16 units |
| a whole plot (about 0.1 ha) | 1,000 m² | about 20 hours | several batches | **30 to 50 kg of cord: 240 to 400 units of spinning** |

- **A household's cord is a strip by the house**, as medieval flax and hemp were (the 1533 act asked a quarter acre in sixty tilled
  [s via fibre note]).
- **A whole plot of flax is a village's or a region's supply**, and its bound is the spinning: one spinner's whole year (192 units) is
  24 kg of cord. A flax household with a plot sells cord or retted flax to every fishing household within reach; that is the trade
  the proposal wants (§4.2, §8.2), and its bind is spinners, not land.
- **The engine cannot hold a strip.** A holding is whole plots, one crop each (`farm.py:229-235`). Options are in W2-2.

**Wild against flax, per kilogram** [m]: wild 25 units; flax about 10 (spin 8, plus about 2 for sowing, pulling and a retting
batch, less a kg the more one grows). **Flax is about 2.5 times cheaper**, a little under the proposal's three (§4.2). For a household's
0.5 to 1 kg a year the saving is 7 to 15 units, 2 to 4% of its year. The proposal's "an eighth to a third of a person's year" for wild
cord was on the old gear prices; it is now a twelfth to a sixth of one person's year at the most (1 to 2 kg).

**Seed.** Flax seed is saved from the crop (the crop row's `seed`, as grain's). No world has any [m, probe §4.3], and wild flax is
not a practical source [k]. A world with a flax livelihood must seed it in a store (W2-3).

**Cord's uses and a fishing household's need** (a world year): half a gill net 0.5 kg, two hand lines 0.04, a set line 0.3 every
year or two, snares 0.1 to 0.15 a bundle (a hunter's), sacks 0.6 each, a bowstring later 0.02. **A fisher needs about 0.6 kg a year, a
hunter about 0.3, a household that stores grain in sacks 1 to 2 more.**

**The net's fine twine.** A gill net's 1 kg is mostly fine twine, whose spinning costs 3 to 4 times coarse cord's [n fibre §2]. Part 1
folded the extra spinning (20 to 30 real hours) into the net's making (at 1/7). Kept here, named: the alternative is a `twine` good
at real hours (another 10 to 15 units a net), W2-11.

### 2.3 Bone and antler

**Dress a kill** (work, simple; part 1 §3.1). One act on a carcass: **1 unit for a red deer or a boar, 4 roe, or 10 hares or fowl**
(real: a red deer 1 to 2 hours skilled [n hunting §1.7]). It gives:

| Kind | Meat | Hide (units, §2.4) | Bone (kg) | Tallow | Antler |
|---|---|---|---|---|---|
| red deer (about 90 kg live) | as today's take | 1 | 4.5 (5% of live weight, calibrate [n proposal §4.3]) | in autumn fat, about 2 kg [e] | a stag in season, 1 (1.5 kg) |
| roe (about 25 kg) | | 0.3 | 1.2 | | |
| wild boar (about 80 kg) | | 1 | 4 | in autumn, 3 to 5 kg [e] | |
| hare, fowl | | a pelt for the hare (later fur) | | | |
| a slaughtered cow (`slaughter`, D2 farming) | as built | **3.5** (20 to 25 kg green) | 20 | 4 kept (real 5 to 20 [e]) | |

- **By level:** one who knows dressing gets all of it; a novice (aware or rough) loses about 15% of the meat and the hide at half
  (holes cut in it; learning_times §2.9); bone and tallow only from one capable or better.
- **Bone never binds.** Five hooks take 0.05 kg; a red deer gives 4.5 kg, enough for 450 hooks [m]. Its only gate is someone who
  dresses a kill. It earns its place ([[D2-264 The fishing, hunting and materials network|D2-264]]) only as the hook the forge's copper competes with (§3.2), and later points, needles and
  combs. No stock or market logic is needed for it.
- **Antler** (exists): a cast antler found, or a stag in season. It makes the horn (exists) and later leister points.

### 2.4 Hide, rawhide and leather

**Units.** `hide`: one hide the size of a red deer's, dressed and dried (rawhide): about 6 kg green, 3 kg dried (part 1 §1.5). A
roe 0.3, a boar 1, a calf 1, a cow 3.5. Fox, stoat, otter and beaver give a **pelt** (a good for trade now, fur later) [part 1]. The
drying is folded into dressing (part 1: a named compression), so there is no green hide good: a dressed hide keeps a year and more
dry (half-life 33.8 nights), and the wet and the open take it faster (part 1 §2.3).

**Two paths.**

| Path | Steps | Work | Time | Gives | Good for | Poor at |
|---|---|---|---|---|---|---|
| **rawhide** (the short path) | dressed and dried with the kill | in the dressing | none beyond | hide | snares' thong, straps, lashings, rawhide shoes (pampooties [k]), a rawhide harness, a coracle's skin later | stretches and rots wet: about a third of leather's life in wet use [e] |
| **bark-tanned leather** (the long path) | soak, lime (wood ash) to loosen the hair, scrape, bate, tan in pits of oak-bark liquor made stronger by stages, dry and curry with tallow | **1.5 units a hide unit** in all (part 1): lay 0.5, strengthen twice at 0.25, lift and curry 0.5 with 0.1 tallow [e] | **liming 2 nights; pits 16 nights for a light hide (deer, calf), 32 for a heavy one (cow)** [part 1 §2.4: 6 to 18 months at 1/11.4, 16 to 48 nights] | **3 leather a hide unit** (sole leather 48 to 54 lb from 100 lb of green hide [s, Scientific American via part 1]) | frame straps, harness, bellows, shoes; buckets and bags later | months in the pit; bark, water, a skilled tanner |

- **Lime is wood ash** from any hearth, folded into the liming nights (no good). Burnt lime joins when lime burning comes (mortar,
  building, [[W-76 The timber economy|W-76]]) (W2-10).
- **The pits are part 3a's processing container** (goods change state over nights inside it). This part prices the build (§3.2) and
  the work; the container's grammar, rules and signs are 3a's.
- **Bark in the pits:** 2 bundles (20 kg) a hide unit in practice [part 1 §3.1, e from about 10% tannin in oak bark and a third of
  sole leather's weight in tannin]. A cow (3.5 units) takes 7 bundles, 70 kg.
- **Currying** takes 0.1 tallow a hide unit [e]: tallow gets its second use (it has lights only today).
- **Tanning is skilled** (trying_and_learning §1): failures come late and cost the hides. Proposed: the try's outcome is drawn when
  the hides are laid, by level, and shown when they are lifted, with the lesson; **a failure loses a share of the batch** (skilled:
  a half at aware, a third at rough, a fifth at capable [e]), not all of it, since a pit of twenty hides does not all rot at once (W2-8).
- **Pollution** (the proposal §7.5; [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]): pits foul the water below them all year. Part 3a and the pollution unit own it; the
  tanner's row (part 4 TA5) reads it.

### 2.5 Bark

**The good.** `bark`: a 10 kg bundle of peeled, dried oak bark (part 1 §1.3). Keeps dry (half-life about 70 nights in a shed),
loses its tannin in the wet: the open wet ×5 (part 1 §2.3; hemlock bark lost nearly a quarter of its tannin in two months exposed [s via
part 1]).

**Peel bark** (gather, practised).

| | |
|---|---|
| Where | a wood with oak: an oak-ash wood, an upland oak wood, a managed wood with oak standards; **a forest whose ecosystem is not named counts as oak** (hand-written worlds name none, §4.3) |
| Rate | **1.5 bundles a unit** (7.5 kg an hour) with a crude tool (a spud is folded in) [part 1, from a peeler's 3 to 6 t a year in an April to June season of about 540 hours, 5.5 to 11 kg an hour, s via withies note] |
| Season | **only while the sap is up**: late spring into the first of summer. Real mid-April to the end of June, about 10 weeks, is **about 6 nights** at 1/11.4; part 1 gave 2 to 3. Proposed: 5 nights, spring day 5 to summer day 1 (W2-5) |
| What it draws | oak poles from young growth (in a managed wood) or the felled oak (with `fell`, a joint product, below) |
| Leaves | the peeled poles as firewood or timber where they lie: bark is 10 to 15% of a small oak pole's mass [n withies §1.4, est.], so a bundle of bark leaves about 6 to 9 bundles of peeled pole wood |

**Two sources, both real:**
- **oak coppice peeled in spring**, the poles then going to charcoal or stakes (the joint product ties the tanner to the woodsman
  and the smith);
- **oak felled in spring**: `fell` in late spring gives its timber and, by one who peels, about 1 bark a 4 timber felled, for 0.5 unit
  more [e: the bark of small timber at about 10% of its mass]. This ties the tanner to the wright felling green oak for a frame ([[W-76 The timber economy|W-76]]).

**What a peeler supplies in a season** [m]: at 6 units a day, 5 nights give 45 bundles, enough for **22 hide units**; 3 nights (part
1's) give 27 bundles, 14 hide units; 6 nights, 27. The season's length is the tanner's scale.

**Other uses:** barking nets (0.5 bark, 1 firewood and 1 unit a net a year at a hearth; it keeps a net three years where an untreated one
rots in one: fibre note §4; §3.3 here) gives fishers a reason to buy bark.

**Competition:** charcoal and firewood take the same oak poles (but after peeling, not instead: a joint product); felling for timber
takes the standards ([[W-76 The timber economy|W-76]]); the season clashes with spring sowing, so a farmer-tanner peels or sows.

### 2.6 Where the chains meet

| Meeting | What competes or substitutes | What decides it |
|---|---|---|
| **withies against timber for the weir** | wattle sections (12 withies, 7 timber, wear 1.0) or timber (40 to 80 timber, wear 0.5) | wet ground or a bed for wattle; a wood and a crew for timber; the upkeep (6 withies a year a wattle section) |
| **withies against cord for traps** | a wicker trap (0.45 withies) against a net set overnight (1 cord) | which stock is reached: traps meet eels and the edge, nets the open water and salmon (proposal §7.1); the trap is cheaper by far |
| **withies in hurdles, racks, baskets and wattle rooms** | one stock, many uses; the weir and houses take most | a bed pays where a weir stands; elsewhere wild willow |
| **young growth: rods, firewood, bark poles, charcoal** | one stock in a managed wood | season (rods in winter, bark in spring, firewood any time); a wood's holder chooses |
| **cord: wild, flax, rawhide** | wild (labour), flax (land, seed, retting water, spinners), rawhide thong (land snares only, rots wet) | who holds flax land and spinners; trade in cord |
| **hooks: bone or copper** | bone free from a kill, life 10 to 30 uses; copper from the smith, 30 to 100, takes somewhat more | the forge's reach |
| **straps and harness: rawhide or leather** | rawhide now, a third of the life wet; leather after a world year in the pits | a tanner in reach; time |
| **shoes: rawhide or leather, or none** | rawhide shoes last days; leather weeks | as above; what shoes do is part 4's and 3's (W2-7) |
| **sacks or baskets** | a sack (0.6 cord: 5 units by flax, 15 wild) holds 50 kg and keeps grain; a basket (0.3 withies, about 1 unit) holds 25 kg of roots, nuts, dried goods and leaks grain | sacks pay only with flax; storage.md's protections decide which goods want which (part 3a) |
| **leather against the forge** | the bellows' leather (2 a fitting, re-leathered every few years) | the tanner supplies the smith: the tie [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] named |
| **bark: tanning against nets** | 2 bundles a hide against 0.5 a net a year | the peeling season's supply |
| **tallow: lights against currying** | 1 tallow gives 5 dips, or curries 10 hides | the slaughter |

---

## 3. The made things

### 3.1 How each row reads

- **Recipe in real kg** (the materials in their handling units, with kilograms).
- **Units at 1/7, and at 1/15** (part 1 §3.2 to §3.4), as the units of one act and its batch.
- **Life:** uses (at 1/7 of the real count; at 1/15 a use costs the same, so the use count is 7/15 of it, part 1) and rot (world years).
- **Wear and mending** (§3.3), **failure** (by class and lesson), and **what is shown** (§3.4).

### 3.2 The table

Real hours are from part 1 §3 and the notes it cites [n]; new rows are marked [e].

| Thing | Recipe (units; kg) | Real hours each | Act at 1/7 (units, batch) | At 1/15 | Life: uses / rot | Class | Shape, at |
|---|---|---|---|---|---|---|---|
| **wicker trap** | 0.45 withies (4.5 kg green, about 2.5 kg dried) | 4 to 8 [n withies §1.2] | **1 unit, up to 2** (a line of 6 in 3) | 1, up to 6 | 30 to 45 sets / **2 world years** (soaked and dried each use) | practised | make, anywhere |
| **creel** | 0.25 withies | 4 to 8 | 1, up to 2 | 1, up to 4 | carried, no use count / 3 to 5 | practised | make |
| **basket** (holds 25 kg) | 0.3 withies | 4 to 8 [n storage §3.3] | 1, up to 2 | 1, up to 4 | / 2 | practised | make |
| **pack basket** ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]; replaces the pack) | 0.4 withies, 0.1 hide (rawhide straps, 0.3 kg) | 6 to 10 | 1, 1 | 1, up to 2 | / 2 to 3 (wears fast) | practised | make |
| **leather-strapped frame** ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) | 0.1 timber (2.5 kg of split ash or hazel), 0.5 leather | 6 to 12 | 1, 1 | 1, up to 2 | / 5 to 10; restrap 0.2 leather | practised (leather work) | make |
| **keep box** | 1 withies | 8 to 10 [n fishing ladder] | 1, 1 | 1, up to 2 | / 2 to 3 (in water) | practised | make |
| **hurdle** (1.8 by 0.9 m) | 1 withies | 2.7 to 3.2 [n withies §1.2] | **1, up to 5** | 1, up to 10 | / 5 to 10 dry | practised | make |
| **smoke racks** (a set, [[D2-271 Smoking in three depths|D2-271]], [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]]) | 2 withies, 2 timber (50 kg of frame poles) | 6 to 10 [n withies §3.4] | 1 (a fitting: build) | 1 | / 5 (rot); holds about 250 fish | practised | build, in a smokehouse |
| **fishing rod** | 0.1 withies (one hazel or willow pole, 1 kg) | 1 to 2 | 1, up to 5 | 1, up to 10 | 20 to 45 uses / | simple | make |
| **hand line** | 0.02 cord, 2 hooks | 1 to 2 [n fibre §3] | 1, up to 5 | 1, up to 10 | 4 to 14 uses (hooks lost) / | simple | make |
| **set line** (20 to 50 hooks) | 0.3 cord, 30 hooks | 8 to 10 [n fishing ladder] | 1, 1 | 1, up to 2 | 7 to 14 sets / 1 (cord in water) | simple | make |
| **bone hooks** | 0.05 bone for 5 | under an hour each [n withies §1.8] | 1, up to 5 (day clock: lost in 10 to 30 uses) | same | 10 to 30 uses | simple | make |
| **copper hooks** | 0.05 copper for 10 | 2.5 to 5 for 10 | 1, up to 10 (capital; a smith's, at an anvil) | 1, up to 20 | 30 to 100 uses | skilled (the smith's) | make, at an anvil |
| **snares**, a bundle of 25 | 0.12 cord (3 to 4 g a snare and its tether), or 0.05 hide as thong | about 10 minutes a snare [n fibre §3] | **2 units, 1 bundle** (day clock) | same | each snare 3 to 10 settings; thong rots in a wet night | simple | make |
| **gill net** (20 by 1.5 m, 7 cm mesh) | 1 cord, 0.1 stone (2.5 kg of sinkers), floats folded in | 40 to 60 beyond the cord, the fine twine's extra spinning included [n fibre §3] | **4 units, 1** | 2, 1 | 30 to 65 sets / **1 untreated, 3 barked** | practised | make, at a house |
| **fowling net** (clap, 10 by 2 m) | 0.8 cord, 0.1 timber (poles) | 50 to 70 | 4, 1 (or 5: a day's units in winter) | 2, 1 | 30 to 60 sets / 1, 3 barked | practised | make |
| **dip or hoop net** | 0.1 cord, 0.2 withies (the hoop) | 3 to 4 | 1, up to 2 | 1, up to 4 | 15 to 45 uses / 1 | practised | make |
| **harness** (yoke and traces) | 0.4 timber, 1.5 leather; or 0.5 hide as rawhide | 9 to 18 | 1, 1 | 1, 1 | 70 to 140 days worked; rawhide half / 5 | practised (leather work) | make |
| **shoes**, a pair | 0.5 leather; or 0.3 hide as rawhide | 3 to 5 [e: a cordwainer's turnshoe] | **1, up to 3 pairs** | 1, up to 7 | **8 to 16 days worn** (real 90 to 180 days of wear [e], at 1/11.4); rawhide 2 to 4 | practised (leather work) | make |
| **bellows** (in the anvil fitting, [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) | 2 leather, 0.2 timber | in the anvil's units | the anvil: 2 to 3 units, 4 stone, 2 leather, 0.4 timber (part 1 §3.4) | | the leather / 3 to 5; re-leather 1 unit and 2 leather | (the smith's fitting) | build |
| **sack** (holds 50 kg) | 0.6 cord (spun and woven; the loom folded in, as the spindle is) | 3 to 5 beyond the cord [n storage §3.2] | 1, up to 3 | 1, up to 6 | / 3 | practised | make |
| **chest** (holds 400 kg) | 4 timber of boards (100 kg) | 18 to 27, a wright [n storage §3.4] | 2, 1 | 1, 1 | / 30 | skilled (the wright's) | make; boards from [[W-76 The timber economy|W-76]] |
| **barrel** (holds 120 kg) | 7 timber of stave bolt, 0.3 withies of hoops | 8 to 11, a cooper [n storage §3.6] | 1, 1 | 1, up to 2 | / 10 | skilled (the cooper: a wright's specialism) | make; what it keeps is 3a's |
| **brine pan** (fitting) | **10 copper**, 4 stone (the furnace) | 18 to 36 | 1.5 to 2.5 (build) | 1 | 40 to 90 boilings; mend 0.25 copper | skilled (the smith's) | build |
| **spear** (copper head) | 0.5 copper, 0.08 timber (an ash shaft) | 2 to 4 | 1, 1 | 1, up to 2 | 30 to 70 hunts ([[D2-46 Weapons wear|D2-46]]'s wear) | skilled (the smith's head) | make, at an anvil |

**The works of this part** (build; part 1 §3.7): the **withy bed** (1.5 units at 1/7, 1 withies, a wet parcel held, a fence or dead
hedge; 30 years), the **retting pit** (1.5 to 3; by water; silts in 10 years), the **tan pits** (2 to 4 units, 4 timber of planks or
wattle, clay puddled on the spot; by water; 20 years; **hold about 10 hide units a pit, three to five pits** [e: a pit of about 3 m³
holds a layered batch of some 20 to 30 deer-sized hides; a village tanner's few pits]).

**Recipes now in the engine and what they become** [m, `data.py`]:

| Row today | Now | Becomes |
|---|---|---|
| `fishing rod` (`data.py:605-606`) | 0.5 timber (120 kg at the old reading), 0.1 hide; 1 unit; life 30 | 0.1 withies; 5 a unit; the line separate |
| `pack` (`data.py:587`, item `:105`) | 1 hide, 1 timber; 1 unit; +10 carry; no life | the pack basket and the frame ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) |
| `harness` (`data.py:664-665`) | 2 timber, 1 hide; 2 units; trade "leatherworker" (no such livelihood); life 80 days | as above, by the tanner or one who knows leather work |
| `anvil` (`data.py:254`) | 6 stone, 2 hide, 1 timber; 4 units | 4 stone, 2 leather, 0.4 timber; 2 to 3 units |
| `smoke racks` (`data.py:275`) | 2 timber; 2 units; "up to 40 fish, 3 nights" | 2 withies, 2 timber; 1 unit; 250 fish a set ([[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]]) |
| `bedroll`, `tent` (`data.py:660`, `:662`) | 1 hide; 3 hide and 2 timber | 0.5 hide; 1.5 hide and 0.4 timber; lives in nights at 1/11.4 (part 1) |
| `crude tool` (`data.py:666`) | 1 timber, 0.5 stone; life 10 | 0.04 timber, 0.04 stone each, 2 a unit; life 20 to 70 acts (part 1) |
| `slaughter` cows' hide (`data.py:548`) | 2 hides a cow | 3.5 hide units |

### 3.3 Wear and mending

**Two lives.** Each lasting thing carries `uses` (what wears it, at 1/7 of the real count) and `rot` (world years, by material, in
water or dry). It is gone at whichever comes first.

| Material, in use | Rot (world years) | What a use is |
|---|---|---|
| withies in water (traps, keep box) | 2 [n withies §1.2: pots and putchers about 2 years with repair] | a set night |
| withies dry (hurdles, baskets, creels) | 2 to 10 by thing | carrying wears none; a hurdle in a fold none |
| cord in water, untreated | **1** (weeks to a season [k], compressed generously; a named departure) | a set or a cast |
| cord in water, barked | **3** (two to four seasons [n fibre §4]) | as above |
| cord on land (snares, lines kept dry) | 2 | a setting |
| leather | 5 to 10 | days worked (harness), days walked (shoes) |
| rawhide in wet use | a third of leather's | as leather |
| bone, copper | (no rot) | a use; lost at random |
| timber boards (chest, barrel) | 10 to 30 | |

**Mending** (make, on the thing as target, part 4 §5.3: "mend T7", unnamed one's own of that kind here):
- **restores half the thing's full uses**, never its rot: a net is mended, not remade, until it is rotten (proposal §5);
- **costs a tenth of its materials and about a fifth of its making units**, with one act mending all of one kind one holds at a
  place (a line of traps, a net), at the floor of 1 unit;
- **the mending craft is the making craft**: one capable or better mends at no risk; rough mends at its odds and may spoil the
  materials (not the thing);
- **barking** a net (0.5 bark, 1 firewood, 1 unit at a hearth) sets its rot from 1 to 3 world years from that day, once a year;
- **real check:** net mending is 10 to 20% of the netting time a season [n fibre §2]: half a unit a world year at 1/7; the rule gives
  about 0.8 units a mend (a fifth of 4), once or twice in a net's life. Within the spread.

**Wrecks and losses** are part 3b's (a spate wrecks set traps, a flood most; snares torn; hooks lost). They take the thing whole,
not uses.

**What this replaces in code:** sets with a life of 4 or 8 nights and no gear (`wild/methods.py:86`; `engine/wild.py:909`
`set_work` places a set that costs nothing); tools wearing by `TECHNIQUES[..]["wear"]` per act and breaking at `ITEMS[..]["life"]`
(`world.py:686`), with no rot and no mending for items. The record would hold a thing's uses left and its made day (or barked day),
on the thing (the set or the item) rather than the container's `wear` map, since part 3b makes gear a thing with a tag.

### 3.4 What a person is shown ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]])

[[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]: at capable or known, the inputs with the batch, what it gives, its units, and its place or fitting; a rough idea shows its
inputs as its card does; awareness shows the name only; basic crafts with no inputs show none. Part 4 §2.2 renders these under the
shapes. Rendered for this wave (numbers at 1/7):

| Craft | Known | Capable | Rough | Aware |
|---|---|---|---|---|
| wicker traps | wicker traps (known, a skilled hand: up to 2 traps from 0.45 withies each, 1 unit; soak the rods) | wicker traps (capable: up to 2 traps from 0.45 withies each, 1 unit; works about 4 times in 5, a fifth more withies) | wicker traps (a rough idea: withies; you have not yet got the throat right) | wicker traps (you have seen Nichola at it) |
| a gill net | a gill net (known: 1 cord and 0.1 stone, 4 units, at a house; gives a net for 30 to 65 sets; bark it yearly) | a gill net (capable: as known; works about 4 times in 5) | a gill net (a rough idea: cord, at a house) | a net (you have seen one at the Marshes') |
| twist cord | twist cord (best in late summer and autumn) | | | |
| dress and spin | dress and spin (known: up to 1 retted flax a unit, gives 0.125 cord; best in winter) | as known, "works about 4 times in 5" | dress and spin (a rough idea: retted flax; the fibre tangles) | dress and spin flax (you have heard of it) |
| hurdles | hurdles (known: up to 5 from 1 withies each, 1 unit) | as known with the odds | hurdles (a rough idea: withies) | |
| peel bark | peel bark (known: oak, while the sap is up, late spring; 1.5 bundles a unit) | | | |
| lay hides in the pits | tan hides (known, a master's hand: up to 10 hide units a pit, 2 bark and 0.5 unit each; 16 nights for deer and calves, 32 for cows; strengthen twice; gives 3 leather a hide) | tan hides (capable: as known; a fifth of a batch lost about 1 time in 3) | tan hides (a rough idea: hides and oak bark in pits by water) | tanning (you know the Tanners do it) |
| shoes | shoes (known: up to 3 pairs from 0.5 leather each, 1 unit) | as known with the odds | shoes (a rough idea: leather) | |

Rules for these lines:
- **"up to"** appears on processes ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]: spinning, tanning, salting) and on batched whole things (§1.2.3).
- **Basic crafts with no inputs** (cut withies, twist cord, peel bark: gathers) show the name and, as part 4's season clause, the
  season: "best in late summer and autumn" is the craft's own fact, not lore, because the yield is the state the act reads.
- **Lessons** show as short clauses (part 4 §2.2).
- **Conflict:** part 4 §2.2 shows rough as "the main input and the place"; [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] and the card (`knowledge.py:381-383`) show rough with
  all the inputs and their amounts. This table follows [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] as decided, with the amounts dropped where the card's amounts would
  read as known (W2-17).

### 3.5 Learning data for each new craft (the fields part 4 asks of part 2)

Class and lessons from learning_times.md §2 and §5 where it has them; new ones marked [e]. Profiles from part 4 §4.8.

| Craft | Class, curve | Profile | Lessons (in order; the first is the main input) | Capability points |
|---|---|---|---|---|
| cut withies | simple, shallow | G.6 H.4 | rods are cut when the sap is down (season); cut the stool clean and low (step) [e] | |
| plant a withy bed | simple, shallow | G1 | cuttings a forearm long, pushed in wet ground in winter (input, season); keep the beasts off (step) [e] | |
| twist cord | simple, shallow | H1 | the strands one way, the wrap the other; even strands, long overlaps; stems retted and dried (learning_times §5) | |
| dress and spin | practised, steady | H1 | too thin, the spindle drops; wet fingers and a dressed distaff; too much twist (learning_times §5) | fine twine (0.6): a net in 3 units in place of 4 [e] |
| ret flax | simple, shallow | W.6 G.4 | still water, not the river (place); lift it when the stems part from the fibre (step) [e] | |
| dress a kill | simple, shallow | H.6 B.4 | cut shallow at the belly; the blade to the hide; open and cool it at once (learning_times §5) | |
| peel bark | practised, steady | G.6 H.4 | only while the sap is up (season); keep it dry under a roof (input) (learning_times tanning lesson, as a lesson here) | |
| tan hides | skilled, deep | F.8 H.2 | the liquor weak at first, stronger by stages; bark kept dry; limed and scraped clean (learning_times §5); the last only from a teacher | heavy leather (0.6): cow hides; before it, deer and calves only [e] |
| wicker traps | practised, stepped | H.8 W.2 | the rods soaked or green; butts and tips turn about; the throat to a finger's width (learning_times §5) | a tight throat (0.5): traps hold a fifth more [e, a crude-result rule's inverse] |
| hurdles | practised, steady | H.8 S.2 | twist each rod at the end post; uprights a forearm apart; beat the weavers down (learning_times §5) | |
| netting (gill, fowling, dip) | practised, steady | H1 | knots drawn hard to the mesh stick; pulled tight; good tight cord (learning_times §5) | |
| leather work (frame, harness, shoes) | practised, steady | H1 | leather wetted before it is shaped; stitch close at the strain; rawhide for a season only [e] | a turnshoe (0.4): shoes; before it, straps and harness [e] |
| mend gear | as the thing's craft | as the thing's | as the thing's | |

---

## 4. Gates

### 4.1 Who can reach each chain from a fresh world

| Chain | Tools | Places within a day | Season (the compressed year) | Knowledge | Time to first output |
|---|---|---|---|---|---|
| withies, wild | a crude tool (bare hands at a third) | wet ground or a bank | any; winter full, summer a third | none (simple, tryable) | the same day |
| coppice rods | a crude tool (`cut` refuses bare hands today) | a wood or scrub | winter best | none | the same day |
| a withy bed | a crude tool to dig | a wet parcel the household holds | plant in winter | simple | 2 world years to half, 3 to full |
| wild cord | bare hands | built ground, field or wood edges, fen | late summer and autumn (spring a little less, winter a quarter) | none | the same day, 0.04 a unit |
| flax | a crude tool to sow and weed | a field plot or a garden share; still water, a pit or meadow grass | sow spring, pull summer, ret late summer, spin winter | sow (broad); ret, dress and spin (capable) | **sown in spring, cord in winter: a world starting after spring waits up to 1.75 years** |
| bone, hide | a crude tool or weapon for the kill | game or herds | game best in autumn | dress a kill (simple) | the day of the kill |
| bark | a crude tool | a wood with oak | **late spring only, about 5 nights** | peel bark (practised) | up to a year's wait |
| leather | | tan pits by water; bark in store; hides; a hearth's ash | hides mostly in autumn; bark from spring | tan hides (skilled: a teacher for the top) | **16 to 32 nights after laying: a world needing leather in its first year must seed it** |
| copper hooks | | an anvil and copper (or ore and rock) | | the smith's | the day |
| a new crude tool | | rock, or a field hoed (hoeing gives stone) | | broad | the day |

### 4.2 The gate check to run at world build

An addition to household_skills §2.3's check, and an extension of `gates.py` (which tries only gather and work: `gates.py:45`).
Refuse means the world is not run as is; warn means it is reported.

| Check | Level |
|---|---|
| **M1 source.** For each material a seeded craft uses (withies, cord, retted flax, bark, hide, bone, leather, copper, stone), a source within a day: the cover, the stock, or a holding household with the producing craft | refuse for a core livelihood's craft; warn for a secondary |
| **M2 seed.** Flax seed held in the region when any household grows flax | refuse |
| **M3 season against need.** For each piece of gear a livelihood needs before its material's next season (traps before the run, a net before the run, leather before the pits can give it), the gear or its material seeded | warn, with the units the household would need to spend before the need |
| **M4 tools last.** A cutting tool in each household that cuts, felling or peeling, and stone within a day to remake one (rock, or a field to hoe) | warn: "no stone within a day: crude tools cannot be remade" |
| **M5 processing site.** Retting water or a pit for a flax household; a tan-pit site by water for a tanner, with the parcels below it named (pollution) | refuse for the core |
| **M6 knowledge.** A member capable or better in each making craft the livelihood needs, or a teacher within a day | refuse for the core |
| **M7 scale.** No recipe's least input above what a household can hold or gather in its season (the bed's 30 bundles, the pits' 10 hides a pit, a whole plot of flax against its spinners) | warn |
| **M8 the make and build probe.** `gates.py` extended to try each make and build on a fresh copy with its inputs supplied, so a refusal that is the code's, not the world's, shows before a run | report |

### 4.3 Which current worlds fail (probe, read-only, 22 Nov)

`w2/gates_making.py` loads every world file with people (52 files, 94 villages; the 42 goal-probe copies of one small world counted
once) and reads, for each village, its own parcels and those of nodes one day away: wet ground and banks, still water, woods,
named oak, fields, rock, game (red deer, roe and boar in the wild layer's populations) and herds, anvils, copper and hides in store.
Limits: it reads covers and stocks, not who holds them, nor the start date, nor knowledge (no one in any world knows any new craft).

| Chain | Villages that can reach it [m] |
|---|---|
| wild cord | 94 of 94 |
| coppice rods | 91 |
| oak bark (a forest without a named species counted as oak) | 91 (by named ecosystem only: 18, since hand-written worlds name none) |
| hides (game, herds or hides in store) | 76 |
| flax ground (a field) | 72 |
| retting water (fen, still water or a river) | 63 |
| tanning (bark, hides, water) | 55 |
| withies from wild willow (wet ground or a bank) | 49 |
| copper hooks (an anvil and copper or rock) | 38 |
| stone to remake a crude tool (rock within a day) | 38 |
| **flax seed** | **0** |

**The worlds that matter:**
- **The runs world** (`specs/nutrition/runs_*.yaml`, Eelmouth): fen, banks, oak-ash woods, 275 deer and boar within a day,
  retting water: every wild chain, bark and tanning are reachable. It **fails M4**: no rock and no field, three crude tools for twelve
  people (`holdings`); once they wear out (10 acts today, 20 to 70 under part 1) no one can remake one, and coppice cutting, peeling
  and felling stop. It **fails M2** for flax (and has no field: Clay Field is scrub, clearable at 10 units a unit of size). It fails
  copper hooks (no forge). And it starts on **summer day 4**: the low arm has no traps and must cut withies at a third of the rate
  before the autumn run (§5.1), which **fails M3** unless gear is seeded.
- **The river worlds** (`water/runs.yaml`, `runs_models.yaml`: Highpool, Lowstrand, Middleham): Middleham reaches everything but
  flax seed; Lowstrand has no rock or forge; Highpool no field.
- **Wenbridge** (`wenbridge.yaml`, and e2, takeover): its river, the Wen, borders no parcel in the graph (its `adj` is empty) so no
  bank exists to cut willow on; no herds and no wild layer, so **no hides, no bone, no tanning**; no anvil. A data fault (the river's
  adjacency) and a design gap (a village with no beasts at all).
- **The region worlds** (region_c0, c1, c_s27, s1): Barleyfield and Coppergate have no wet ground and must buy withies; Coppergate has
  no hides; Ashwood and Millford have no rock.
- **Frontier camps:** no hides (no wild layer, no herds), though a frontier is where hides should be easiest.
- **Every world without the wild pack** (barleyfield, combe, hamlet, hollins, two_valleys, wide, ...): game counts zero, so hides and
  bone come only from slaughter.

---

## 5. Worked chains

### 5.1 A fisher household making its season's gear from nothing (Eelmouth, as the runs world starts)

Peter and Nichola Marsh, two adults, Eelmouth, low arm: no gear, a crude tool, the larder's 8 days. The world opens on summer day
4 (year day 12); the first eel run night is about autumn day 2 (year day 18). Summer days are 7 units each, autumn 6. They need
before the run: 12 wicker traps (two lines of 6), a creel; after the run's first nights, a gill net for the open water. By the wild
path (no flax in the world, no bed) [m, w2/calc.py; rates of §2 and §3].

| Day (year) | Season | Peter (units) | Nichola (units) | Stock at night |
|---|---|---|---|---|
| 12 | summer | cut withies at Eelmouth Fen, 7 units at 0.45 a unit (summer, a third): 3.2 bundles | twist cord by the Street's middens, 7 units at 0.04: 0.28 kg | 3.2 withies, 0.28 cord |
| 13 | summer | cut withies, 7: 6.3 | twist cord, 7: 0.56 | |
| 14 | summer | cut withies, 4: 8.1; make wicker traps 3 units: 6 traps (2.7 withies) | twist cord, 7: 0.84 | 6 traps; 5.4 withies |
| 15 | summer | make wicker traps, 3: 6 more (12 in all); make a creel, 1: 2 creels | twist cord, 5: 1.04; make 2 hand lines and a rod (1 unit, from 0.04 cord and a pole) | 12 traps, 2 creels, 2.1 withies, 1.0 cord |
| 16 | autumn | (food, 6) | make a gill net, 4 units (1 cord, 0.1 stone: needs a stone; **none at Eelmouth**, so floats and sinkers of clay or wood, a named substitute, or the net is refused) | a net |
| 17 | autumn | set the traps in the Isel, two lines (part 3b) | food | |
| 18 | autumn | the first run night: lift (part 3b) | | |

- **Making before the run: about 56 of their 80 units** (Peter 25, Nichola 31), 70% of five days, 15% of their year in the first
  week. The cord took more than the traps (26 units against about 25 for withies and traps together).
- **The summer rods:** cut in summer they give a third, and the trap lessons say summer rods crack (learning_times §5). Proposed:
  the state cause is real (rods cut in summer) and the result is a trap that lasts half its uses (a crude result), not a failure,
  since green summer rods do weave [e].
- **A world opening with no gear seeded would see the low arm miss the first run nights** if the Marshes hunted or gathered first;
  the gate check's M3 would warn: "Marsh: traps and a net needed by autumn day 2; materials out of season; about 56 units".
- **The stone for sinkers** is a small new gate the probe did not catch: a net wants 2 to 3 kg of sinkers, and Eelmouth has no
  rock. Real fishers on clay used fired clay or stone from the river bed [k]: proposed, a net's sinkers may be 0.1 stone or nothing
  at a parcel with a river bed (the water parcel gives pebbles), named.

**The switch to flax and a bed** (the same household, from year 1, steady state at its end):

| When | Act | Units |
|---|---|---|
| year 1, winter days 24 to 31 | cut withies for next year at the full rate (1.5 a unit): 6 bundles in 4 units; plant a withy bed on Brook Meadow's wet edge (1.5 units, 1 bundle of cuttings) with a dead hedge (1 to 2 units) | about 8 |
| year 2, spring | sow a flax strip of 25 to 50 m² (if a strip can be held, W2-2) with **seed bought from another village** (M2: none in the world) | under 1 |
| year 2, summer | pull flax (under a unit); ret on Brook Meadow's grass 3 to 4 nights (not the Fen, which is the Isel's brook: water retting fouls it for the fishers, [[D2-264 The fishing, hunting and materials network|D2-264]]) | 2 to 3 |
| year 2, autumn | the run: traps mended (1 unit, a tenth of their withies), the net barked (1 unit, 0.5 bark bought from the tanner) | 2 |
| year 2, winter | dress and spin 8 retted flax to 1 cord (8 units over four evenings' worth of winter days); the bed gives half (15 bundles) | 8 |
| year 3 on | the bed at 30 bundles a year: the Marshes' 6 a year leave 24 to sell to the weir's crew | |

**The year against part 1 §5.1** (steady state, two adults, 384 units) [m]:

| | Wild cord, wild willow | Flax, a bed | Part 1 §5.1 |
|---|---|---|---|
| withies cut | 3.8 | 1.3 | |
| traps made (6 a year) | 3.0 | 3.0 | 2.2 (with withies) |
| net: half a net's netting; mending and barking | 1.8; 1.0 | 1.8; 1.0 | 5.8 / 14.3 with the cord; 0.5 |
| cord (0.56 kg) | 14.0 | 5.6 | |
| lines, rod; creel, pack basket, baskets; racks | 1.0; 1.1; 0.2 | 1.0; 1.1; 0.2 | 1; 1 |
| the house | 3.9 | 3.9 | 3.9 |
| **making and mending** | **29.8 (7.7%)** | **18.8 (4.9%)** | 32 (8%) / 20 (5%) |
| at 1/15 | 23.4 (6.1%) | 12.5 (3.3%) | |
| materials' share of the making, 1/7 / 1/15 | 60% / 76% | 37% / 55% | |

Fuel for the hearth (3 to 4%) and for smoking (3 to 9%) come on top, as part 1 §5.1 has them.

### 5.2 A tanner's year

Alan and Joan Tanner, a farming and tanning household on the river below Middleham, with Hazel Copse's oaks a parcel away and
hides from the hunters and the slaughter. They tan **15 hide units a year**: 6 red deer from the hunters, 2 cows and 2 calves from
the Martinmas slaughter (7 and 2). A year in steady state, the pits holding last year's heavy hides.

| Days (year) | Season | Work | Units | Pits and stores |
|---|---|---|---|---|
| 0 to 4 | spring | sowing (the farm); Joan curries and stocks last autumn's light hides lifted on day 4 (laid day 20 last year + 16) | 3 (lift and curry 6 hides: 3; 0.6 tallow) | 18 leather |
| 5 to 8 | late spring, the sap up | **Alan peels bark in Hazel Copse**: 4 days at 6 units, 24 units at 1.5: 36 bundles; Joan sows alone | 24 | 36 bark, in the bark shed (kept dry) |
| 8 to 15 | summer | hay and weeding; Joan makes shoes from the light leather: 24 pairs in 8 units (12 kg); a frame for the Marshes (0.5) | 9 | 5.5 leather left |
| 16 to 21 | autumn | hides come in dressed from the hunt (6 deer): 2 nights in the ash pit (liming), then laid (0.5 a hide, 2 bark each) | 3 | pit 1: 6 deer hides, 12 bark |
| 22 to 23 | autumn | the slaughter: 2 cows, 2 calves (Alan dresses them: slaughter as built); limed 2 nights | | |
| 24 to 25 | winter | lay the cows and calves (0.5 a hide unit: 4.5 units; 18 bark); **lift last year's cows and calves** (laid day 25 last year + 32): curry (0.5 a hide unit: 4.5) | 9 | pit 2: 2 cows and 2 calves; 27 leather out |
| 26 to 31 | winter | strengthen the liquor twice in each pit (0.25 a hide unit each time: 7.5 units); harness for the miller (1.5 leather), bellows' leather for Highpool's smith (2) | 9 | 30 of the spring's 36 bark used; 6 sold to the Marshes for barking their net |

- **The tanning's work: about 47 units** (peeling 24, laying, tending and lifting 22.5) of Alan's and Joan's 384:
  **12% of the household, a quarter of one person.** Shoes and leather goods add 10 to 15. Part 4's tanner row has it right: a by-trade
  beside farming.
- **The bark binds first**, then the pits: one peeler's whole 5 nights give 45 bundles, 22 hide units. A sixth night or a second peeler is
  the only way past it, and the peeling clashes with sowing.
- **The pits are never empty.** A cow laid in winter comes out the next winter, on the days the new ones go in; the deer laid in
  autumn come out in spring. The pits hold about 15 hide units most of the year: 2 pits of 10, a third for slack.
- **Leather out: about 45 kg a year**, against a village of 12's need of 12 to 24 kg for shoes and a few for frames, harness and
  bellows [m, §5.3]: one tanner supplies two or three villages, or tans for coin and sells down the river. This is the market-town
  tanner of history, and it gives the trader (part 4 §3.5.14) a load: leather is 1 kg a unit, 30 to the frame.

### 5.3 How much leather a village wears

[m, w2/calc.py; shoes at 0.5 leather a pair, real 90 to 180 days of wear at 1/11.4]

| Use | A village of 12, a world year |
|---|---|
| shoes | 24 to 49 pairs: 12 to 24 kg, **4 to 8 hide units** |
| frames (one a household, 5 to 10 years, restrapping) | 1 kg |
| harness (with an ox team) | 1 to 2 kg |
| bellows (one forge in the region) | under 1 kg |
| **all** | **about 15 to 28 kg: 5 to 9 hide units, 10 to 18 bundles of bark** |

**Shoes are three quarters of the demand.** Without shoes, leather has almost no use a village feels each year, and tanning would
not earn its place by the proposal's own test (§ "What the design is for": two of four). What shoes do (a lower cost to walking and
the cold, per day) is part 4's and part 3's to set; the demand only exists if they do something (W2-7).

### 5.4 Withies through a village's year (Eelmouth, three households and a wattle weir)

| Season | Withies cut | Used |
|---|---|---|
| winter | 40 (27 units, wild, at 1.5) | stored green or dried; the weir's mending begins in late winter at low water |
| spring | 4 (5 units at half the rate) | wattle house repairs, racks |
| summer | | hurdles for folds; rods soaked for traps |
| autumn | 2 (2 units at 1.2) | traps made and mended before the run; the weir's gap |
| **all** | **46 in about 34 units** | half to the weir |

With two beds (60 a year), the cutting falls to 12 units and the beds' holders sell 14 a year. Without a weir, 22 bundles in 15 units.

---

## 6. Alternatives considered

| Choice | Taken | Alternatives | Why |
|---|---|---|---|
| materials' clock | real hours ([[D2-276 Making durable things runs on the year clock|D2-276]]) | materials made only for capital (cord, bark, leather) at the factor, as embodied labour | the decision; it keeps a material a good with one price whatever it goes into, and makes supply chains worth trading. The cost: the flax switch and material trades weigh 2.5 to 4 times their real share (W2-1) |
| wild willow | rods a yearly crop on stools | the young-growth logistic (r = 1 a year); unlimited | a one-year rod regrows in a year; the logistic would make wild willow bind at a quarter of its stock a year; unlimited loses the grazing conflict |
| the withy bed's fence | hurdles or a dead hedge | hurdles only | a dead hedge is a quarter the cost and real |
| cord | one good | cord and twine | twine is the net's cost and is folded in; a second good adds a spinning technique for one user (W2-11) |
| flax | a strip below a plot, or a plot as a village's supply | flax as a field crop | a household needs 25 to 50 m²; a whole plot is 20 to 50 households' cord (W2-2) |
| dress and spin | by the unit (0.125 cord a unit) | 8 units in one act | no act exceeds a day |
| hide | one good, dried with the kill | green hide and rawhide as two goods | part 1's compression; a green hide's days of rot fall inside the night of the kill |
| tanning failure | a share of the batch lost, shown at lifting | all lost at once (today's make); no failure | a pit of hides does not all rot; skilled crafts should fail late and costly but not all-or-nothing (W2-8) |
| tanning's lime | wood ash folded in | a lime good from burnt limestone or chalk | ash was used; lime waits for lime burning (W2-10) |
| gear life | uses and rot, mending restores uses | uses only (the proposal); rot only | a net that is never used still rots; one used daily wears through before it rots; both are real and [[D2-276 Making durable things runs on the year clock|D2-276]]'s "what ends its life" names both |
| mending | half the uses for a tenth of the materials and a fifth of the units | full restore; a fixed count of mends | half and the rot cap keep "mended until it is rotten" without a counter |
| shoes | in this build, worn by days walked | later, with clothing | shoes are three quarters of leather's demand; without them tanning has no steady buyer (W2-7) |
| bone | a good from dressing, never binding | folded into the hook recipe from the carcass | [[D2-264 The fishing, hunting and materials network|D2-264]] lists it; it costs nothing to keep and serves later points and needles |
| sacks | cord, with weaving folded in | a cloth good and a loom | the engine has no cloth; a sack is cord plus a few hours (W2-19) |
| batches of whole things | "up to" the batch for the act's units | quantity × fractional units; a minimum batch | under a unit is free today; a minimum repeats the water mill's 200-grain fault (crafts_evaluation; still in the data on 22 Nov) (W2-6) |
| bark's season | about 5 nights | part 1's 2 to 3; the whole spring | real mid-April to June is about 6 nights at 1/11.4 (W2-5) |
| the spear | now, a copper head | with the bow later | a hunting weapon from the smith, cheap to add; the bow wants sinew, feathers and seasoning |

---

## 7. Conflicts found

### 7.1 With the code (main, 22 Nov)

| Where | What | Consequence |
|---|---|---|
| `verbs.py:142`, `:156` | `cost` takes `int(TECHNIQUES[tech]["units"])` and then multiplies by `qty` | every recipe under 1 unit is free at any quantity; about 30 rows of this wave fall under 1 unit at 1/7 and more at 1/15 (part 1 §5.3) |
| `verbs.py:23-24` | `build` costs 2 units an act | a fitting at 1 unit (racks, a withy bed at 1/15, the tan pits' low end) takes a whole 2-unit act |
| `verbs.py:845` | a failed make spoils all its inputs | tanning, a batch over nights, would lose every hide; trying_and_learning's materials multipliers and crude results are not built |
| `data.py:730` | TRY: one rule for every craft (rough 1.7 inputs at 0.5; capable 1.3 at 0.75) | the classes of part 4 §4.2 replace it |
| `knowledge.py:381-383` | the card at rough shows inputs with amounts | part 4 §2.2 says main input only; [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] says as the card (§3.4) |
| `knowledge.py:389-409` | `crafts_lines` lists names and sources, never inputs | [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] is not built; crafts_evaluation's finding 2 still holds on main (checked 22 Nov, [[D2-287 Reviewing past runs|D2-287]]) |
| `landgen/gates.py:45` | the gate probe tries only gather and work | no make or build chain has ever been probed (M8) |
| `wild/methods.py:86`; `engine/wild.py:909-918` | sets have lives of 4 (snare) and 8 (trap) nights and cost nothing to place | gear has no existence, materials or uses; part 3b replaces sets with gear things |
| `world.py:686-694` | items wear by a use count to `ITEMS[..]["life"]`, one break at a time, no rot | gear needs uses and rot (§3.3) |
| `farm.py:229-235` | a holding is whole plots, one crop | flax "in a close" ([[D2-264 The fishing, hunting and materials network|D2-264]]) cannot be held below a plot |
| `data.py:105`, `:587` | the pack: 1 hide, 1 timber, +10 carry, no life | replaced by [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] |
| `data.py:254` | the anvil's bellows of 2 hide | [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]'s bellows are leather |
| `data.py:275` | smoke racks of 2 timber, "up to 40 fish, 3 nights" | [[D2-271 Smoking in three depths|D2-271]] (withies), [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]] (250 kg a set), part 1's keeping smoke of 1 night |
| `data.py:605-606` | the fishing rod of 0.5 timber and 0.1 hide | 120 kg of wood at the old reading; a rod is a 1 kg pole (part 1 #9) |
| `data.py:664-665` | harness's trade is "leatherworker", a livelihood no document defines | the tanner row ([[D2-270 Household skills|D2-270]]) or leather work |
| `data.py:434` | `cut` has the aliases "coppice" and "cut poles" but gives firewood | coppice rods and poles need their own yields (part 1 §3.1 `cut poles`) |
| `data.py:548` | `slaughter` gives 2 hides a cow, 1 a young beast | 3.5 and 1 hide units by weight |
| `data.py` ITEMS | no withies, cord, flax, retted flax, bone, bark, leather, pelt, or any gear item | all new |
| `specs/wenbridge.yaml` (and e2, takeover) | the Wen's parcel has no adjacency | no bank for willow; a data fault |

### 7.2 With decisions and documents

| Between | What | Proposed |
|---|---|---|
| [[D2-264 The fishing, hunting and materials network|D2-264]] (flax in a close) and the engine's plots | above | W2-2 |
| [[D2-276 Making durable things runs on the year clock|D2-276]] (materials real) and the proposal's §13 target (10 to 20%) | the target was on old prices; the share is 5 to 8% (part 1 #14) | read the target with fuel, as part 1 says |
| hunt_fish_materials §4.2 ("wild cord a third of a person's year"; flax "three times cheaper") | now a twelfth to a sixth of a person's year; 2.5 times | the proposal's numbers to update |
| hunt_fish_materials §5 (trap 2.5 units, net 30, hurdle 1.5, pack 2, bone hooks 1, snares 1) and §4.1, §4.2 (withy bed 10, retting pit 10) | [[D2-276 Making durable things runs on the year clock|D2-276]] prices: 0.5, 4, 0.2, 1, 1 for 5, 2 for 25; 1.5 and 1.5 to 3 | part 1 #13; this note's §3 |
| hunt_fish_materials §4.3 (dressing 0.5 unit a deer) | part 1 and here: 1 unit a red deer | 1 unit |
| hunt_fish_materials §4.2 (retted flax 0.7 of the straw; 8 retted a cord) and fibre_and_cord §9.1 (8 straw a fibre) | 11.4 against 8 kg of straw a kg of cord | 10 straw, 8 retted, 1 cord (§2.2) |
| part 1 §3.1 (bark late spring, 2 to 3 nights) | real April to June is about 6 nights at 1/11.4 | 5 nights (W2-5) |
| part 1 §3.2 (the net's fine spinning folded into the making at 1/7) and [[D2-276 Making durable things runs on the year clock|D2-276]] (materials real) | the fine spinning is material work priced as capital | kept, named (W2-11) |
| part 4 §2.2 (rough shows the main input) and [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] (as its card) | above | W2-17 |
| part 4 §4.10 (Henry's trap: 0.4 withies, 2.5 units, network's numbers) | 0.45 withies, 2 a unit at 1/7 | part 4's example to take these numbers |
| learning_times §5 (summer withies crack) and a real green weave | summer rods can be woven green | a crude result (half life), not a failure (§5.1) |
| withies_wood_materials §3.3 (cut withies bare-handed 0.3) | a knife cuts rods | bare hands 0.5 of the crude rate's 1.5 (with no blade, the note's 0.3 stands as an alternative) |
| [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] (pack basket +15, frame +20) and part 1 §4.1 | consistent | |
| household_skills §2.1 (the tan pits "written when built") | no lines yet | part 4 TA1 to TA5 are those lines; their numbers from §2.4 here |

---

## 8. Couplings

### 8.1 To part 1 (the physical basis)

- Handling units (withies, bark 10 kg; timber 25 kg; leather and cord 1 kg), weights a piece (§1.7 of part 1) carried into the
  recipes; the hide by weight; pelts.
- The keeping curve for the new goods: bark (dry about 70 nights, open wet ×5), hide (33.8 nights dry), leather, cord, withies, bone
  (no spoiling, penalties only); retting and tanning times at 1/11.4 (part 1 §2.4).
- The factor's stage: every row has its 1/15 column; at 1/15 materials are 55 to 76% of making.
- Carrying: a fisher's net (4 kg) and six traps (15 kg) fit a pack basket (part 1 §4.2); a bundle of withies or bark is 10 kg, one
  on foot; the tanner's leather sells by the frame (30 kg).

### 8.2 To part 3a (keeping: wave3_keeping.md)

- **Processing containers:** retting (water, grass, a pit) and tanning (lime pit, tan pits) are 3a's containers; this part gives
  their inputs, outputs, times, work and failure.
- **Containers as stores:** sacks, baskets, chests and barrels are made here (§3.2); what each protects and holds is 3a's
  (storage.md's figures).
- **Pollution** from retting and tanning (the proposal §7.5) reads these batches: a batch of flax in water (up to 50 flax) and a
  tannery's pits.
- **Bark and hides as stored goods:** bark must be kept under a roof, hides dry; their places in the store's rules.

### 8.3 To part 3b (taking: wave3_taking.md)

- **Gear as things:** traps, nets, lines, snares and the weir's sections are made here with their uses and rot; set and tend,
  the counting of a use (a set night, a lift), wrecks and losses are 3b's.
- **The snare bundle:** made here (25 for 0.12 cord, 2 units); how many are lost a setting is 3b's.
- **The weir's withies** (12 a wattle section, 6 a year's upkeep): priced here; built and worn there.
- **Bait** (offal) and **hooks** (bone or copper) as inputs to lines.

### 8.4 To part 4 (the people: wave4_people.md)

- **Craft rows:** class, curve, profile, lessons, capability points (§3.5).
- **Shown lines:** §3.4 under the shapes (gather: cut withies, twist cord, peel bark; work: dress a kill, sow and pull flax; set and
  lift: ret flax; make: every recipe, dress and spin, tan hides, mend; build: the withy bed, retting pit, tan pits, racks).
- **The seeded lines' numbers:** BA1 (summer a third), BA3 (the pack basket's carry), BA4 (three years, thirty), CO1 (a kilo in many
  days: 25 units, about 4 days of one person's units), CO2 (a close), CO4 ({flax_in}: 8 retted), CO5 ({net_cord}: 1 kg; every 2
  to 3 years), TA1 ({hide_days}: a dried hide keeps a year), TA3 ({tan_time}: 16 nights for deer, 32 for cows; {bark_in}: 20 kg a
  hide).
- **Livelihoods:** the basket maker (a bed's holder sells 24 bundles a year), cord and nets (a flax plot's holder is a region's
  supplier, bound by spinners), the tanner (a by-trade, about a quarter of one person's year), the woodsman (bark poles and
  charcoal as a joint product), the builder's wright (chests, barrels as the cooper, spring felling's bark).
- **Shoes' effect** (W2-7) and **a fresh world's gear** (seeded by livelihood, M3).

### 8.5 To the timber economy ([[W-76 The timber economy|W-76]])

- **Poles and boards:** the frame's split ash (0.1 timber), the chest's boards (4 timber), the barrel's stave bolt (7 timber), racks'
  frame poles, the weir's stakes: from coppice poles (`cut poles`) or hewn timber (part 1 §4.4).
- **Spring felling gives bark** (§2.5): the wright felling green oak for a frame in spring supplies the tanner.
- **The managed wood's one stock** of young growth serves rods, firewood, bark poles and charcoal; its holder's choices by season
  are the wood's economy.
- **The cooper** as a specialism of the wright.
- **Wattle rooms** (35 withies a cottage) draw the same rods as the weir and the traps.

---

## 9. Questions for Zach

Each stands alone. The ids are this note's (W2-n); none is yet a row in OPEN.md.

**W2-1. Whether materials made only to feed lasting things (cord, bark, leather) stay at real hours, which makes the cord in a net
cost about eight times its knotting (W2-1).** [[D2-276 Making durable things runs on the year clock|D2-276]] keeps materials real and prices the making at 1/7. A net's kilogram of wild
cord is then 25 units and its knotting 4 (real: 35 to 80 hours against 40 to 60, about equal); materials are 60% of a fishing
household's making by wild cord, 76% at the 1/15 stage. Options: (a) keep, named: cord and withies become the goods worth trading,
and flax saves 7 to 15 units a household-year; (b) price a material whose only use is capital at the factor too (cord at about 3.5
units a kg wild, 1.1 by flax), which restores the real proportions but makes cord nearly free and the flax switch small; (c) a middle
lever on material rates (cord's real rate doubled). **Recommend (a)**: the shares of a year stay near real (5 to 8%), and the
dependences the network wants run through materials. Blocks: every material rate in the data.

**W2-2. Whether a household can grow a strip of flax smaller than a plot, so that flax is "a close" as decided (W2-2).** A household
needs 25 to 50 m² for its 0.5 to 1 kg of cord; the engine's smallest holding is a whole plot of about 0.1 ha, one crop
(`farm.py:229-235`), which gives 30 to 50 kg of cord and 240 to 400 units of spinning. Options: (a) a garden share: a holding of a
tenth or a twentieth of a plot for a garden crop (flax now, hemp and herbs later); (b) flax only by whole plots, so a flax household
is a village's or region's supplier and its spinners are the bind; (c) both. **Recommend (c)**: a strip for the household that wants
its own, a plot for the supplier, so the trade and the self-sufficient strip both exist. Blocks: flax in the data and `farm.py`.

**W2-3. Where flax seed comes from, since no world holds any (W2-3).** The probe found flax seed in none of 94 villages, and wild flax
is no practical source. Options: (a) seeded in the store of every household whose livelihood grows flax, with the gate check
refusing a flax livelihood without it; (b) also in a trader's goods, so a village without flax can start it by trade; (c) a
gatherable wild flax at a low rate. **Recommend (a) with (b)**: seed as capital of the livelihood, trade as the way in. Blocks: any
flax world.

**W2-4. Whether gear has two lives, uses and rot, with mending restoring uses but never rot (W2-4).** Proposed: each lasting thing is
gone at its uses (at 1/7 of the real count) or its rot (world years by material: withies in water 2, cord in water 1 and barked 3,
leather 5 to 10), whichever comes first; mending gives back half the uses for a tenth of the materials and a fifth of the making;
barking a net sets its rot to 3 years. Options: (a) both lives and this mending; (b) uses only, as the proposal (§5); (c) rot only.
**Recommend (a)**: "mended until it is rotten" falls out without a counter, and an unused net still rots. Blocks: the gear record
(part 3b's things) and `world.p_wear`.

**W2-5. How long the bark season is, which sets how many hides a tanner can tan (W2-5).** Bark peels only while the sap is up, real
mid-April to the end of June, about 6 nights at the calendar's 1/11.4; part 1 gave 2 to 3. One peeler in 5 nights supplies about 22
hide units (45 bundles), in 3 nights 14. Options: 3, 5 or 6 nights; or bark also from spring felling (1 bark a 4 timber felled).
**Recommend 5 nights (spring day 5 to summer day 1), with bark from spring felling too.** Blocks: the bark row and the tanner's scale.

**W2-6. Whether a batch of whole things is made "up to" its batch, so five hurdles a unit can be two for the same unit, with a 1-unit
floor on every act (W2-6).** `verbs.cost` truncates units to a whole number before multiplying by the quantity (`verbs.py:142`,
`:156`), so every recipe under a unit is free today; about 30 rows of this wave are under a unit at 1/7. Proposed: each recipe holds
its units and its batch; an act costs `units × ceil(qty ÷ batch)`, at least 1; fewer than the batch give fewer for the same units
([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]] carried to whole things); `build` costs what is left of the work, not a fixed 2. Options: (a) this; (b) fractional units
summed over the day; (c) minimum batches. **Recommend (a)**; with [[O-2 Make the eleven bulk processes take up to their batch|O-2]]'s eleven bulk processes it is one change to `cost` and the
recipe rows. Blocks: every gear recipe.

**W2-7. Whether shoes come in this build, worn by days walked, since they are three quarters of leather's demand (W2-7).** A
village of 12 wears 24 to 49 pairs a world year (a pair lasting 8 to 16 world days, real 3 to 6 months of wear at 1/11.4), 4 to 8 hide
units of leather; frames, harness and bellows together are 2 to 3 kg. Without shoes, tanning has no steady buyer. Options: (a) shoes
now, with an effect on walking and the cold set by parts 3 and 4; (b) shoes later with clothing ([[D2-10 Clothing is parked|D2-10]] parked), tanning living on
frames, harness and bellows; (c) shoes now with no effect (a demand that does nothing). **Recommend (a)**; (c) would be a dial. Blocks:
the tanner's trade and [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]'s list.

**W2-8. Whether a long process that fails (tanning, retting) loses a share of its batch, shown when it is lifted, rather than all of
it at once (W2-8).** Today a failed make spoils all its inputs at once (`verbs.py:845`). A tan pit of twenty hides does not all rot.
Proposed: the outcome is drawn when the batch is laid, by class and level, and shown at lifting with its lesson; a skilled craft
loses a half at aware, a third at rough, a fifth at capable. Options: (a) this; (b) all or nothing, as now; (c) no failure, only
skill acting on yield. **Recommend (a)**. Blocks: tanning, retting and part 3a's containers.

**W2-9. Whether wild willow is a yearly crop of rods on stools that grazing and summer cutting harm (W2-9).** Proposed: the stools
set the year's rods (about 60 bundles a unit of size of fen or carr, 20 of a bank, estimates), the rods regrow each year, summer
cutting lowers the stools a tenth of a bundle a bundle cut, grazing halves the year's growth. At Eelmouth it gives about 220 bundles a
year against a village's 46, so labour and season bind there; a village with one bank cannot keep a wattle weir by wild cutting.
Options: (a) this; (b) the young-growth logistic, which binds at a quarter of the stock a year; (c) unlimited. **Recommend (a)**.
Blocks: the withies resource row.

**W2-10. Whether tanning's lime is wood ash from any hearth, folded in, until lime burning comes (W2-10).** Real unhairing used lime or
wood-ash lye. Options: (a) ash, no good, the liming as 2 nights; (b) a lime good burnt from limestone or chalk in a kiln (another
chain, rock-bound). **Recommend (a)**, lime with mortar and building later. Blocks: the tanning row.

**W2-11. Whether a net's fine twine stays folded into the net's making, rather than being its own good spun at real hours (W2-11).** A
gill net's cord is mostly fine twine, three to four times the spinning of coarse cord; part 1 put the extra 20 to 30 hours into the
net's making at 1/7, which is material work priced as capital. Options: (a) keep folded, named; (b) a `twine` good, a net then 10 to 15
units dearer; (c) a capability point (fine twine) that cuts the net's making. **Recommend (a) with (c)**. Blocks: the net recipe.

**W2-12. Whether hides are counted by weight (a red deer's hide 1, a roe 0.3, a cow 3.5) and the small furs become pelts (W2-12).**
Today a stoat and a red deer each give one hide and a cow two. Part 1 proposed this; it fixes tanning's bark and leather per hide.
Options: (a) by weight, pelts as a trade good; (b) by count, as now. **Recommend (a)**. Blocks: `wild/kinds.py`, `slaughter`.

**W2-13. Whether a withy bed can be fenced with a dead hedge as well as hurdles (W2-13).** Hurdles round a bed are 31 withies and 6
units, four times the bed; a dead hedge of cut brush is 1 to 2 units and lasts 2 to 3 years. Options: either; hurdles only.
**Recommend either**, the dead hedge cheaper and shorter-lived. Blocks: the bed's build.

**W2-14. Whether rawhide stands in for leather in snares, straps, harness and shoes, at a third of leather's life in wet use (W2-14).**
It is the short path a household has without a tanner (byproducts §2a). Options: (a) yes, in those four; (b) snares only (the
proposal); (c) none. **Recommend (a)**: it gives the long path a reason (life) and the short a place. Blocks: the leather recipes.

**W2-15. Whether a world's gear is seeded by livelihood, with the gate check warning when a household must make its gear out of
season before its first need (W2-15).** The runs world opens in late summer: a low-arm household with no traps spends about 56 of
its 80 units in five days making them and a net before the run. Options: (a) seed each livelihood's gear and a season's materials;
(b) seed nothing and let the first season bind; (c) by arm (the low arm bare, as the experiment's point). **Recommend (a) by default
and (c) where an arm is about it.** Blocks: the world makers.

**W2-16. Whether the bark of nets is in this build (W2-16).** Barking (0.5 bark, 1 firewood, 1 unit a net a year) keeps a net three
years against one; it gives fishers a reason to buy from the tanner's peeler. Options: now; with boats and the seine. **Recommend
now**: it is one recipe and a tie. Blocks: the net's rot.

**W2-17. Whether a rough idea shows a craft's inputs with their amounts (as [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] and the card) or only the main input (as part 4
proposes) (W2-17).** Options: (a) all inputs and amounts, as decided; (b) the main input only, the amounts at capable. **Recommend (b)
if Zach is willing to revisit [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]'s wording**, since amounts at rough make the level read as known and the lessons are what rough
should hold; otherwise (a). Blocks: the craft lines.

**W2-18. Whether bone is kept as a good though it never binds (W2-18).** A red deer's 4.5 kg is 450 hooks. Options: (a) keep ([[D2-264 The fishing, hunting and materials network|D2-264]]
lists it); (b) fold the hook's bone into dressing a kill. **Recommend (a)**, with no stock logic. Blocks: nothing much.

**W2-19. Whether sacks are made of cord with the weaving folded in, so that sacks pay only where there is flax (W2-19).** A sack is
0.6 cord, 5 units by flax and 15 wild, against a basket's 1 unit; real sacks were linen and hemp. Options: (a) cord, weaving folded;
(b) a cloth good and a loom, with clothing; (c) sacks cheap by a named factor. **Recommend (a)**. Blocks: storage's containers (part
3a).

**The five that matter most:** W2-1 (materials at real hours, the cord's weight), W2-2 (flax below a plot), W2-4 (gear's two lives
and mending), W2-6 (batches of whole things and the 1-unit floor), W2-7 (shoes, which decide whether tanning has a buyer).

---

## Sources

**In the repository:** `cybertron2/engine/data.py` (ITEMS lines 20 to 115; TECHNIQUES, the make rows 496 to 680; FITTINGS 234 to
286; FORESTS 207 to 220; TRY 730; BATCH_LEAST 757), `verbs.py` (`cost` 116 to 157, `_make` 760 to 856, VERB build 23 to 24),
`knowledge.py` (`card` 368 to 386, `crafts_lines` 389 to 409, `batch_share` 305, `tried` 448), `wear.py`, `world.py` (`p_wear` 686),
`wild/methods.py` (SETS 86), `engine/wild.py` (`set_work` 909), `farm.py` (plot shares 228 to 235), `forests.py` (`young_step` 52),
`landgen/gates.py` (45); the world files under `cybertron2/specs/` (probed, read-only); records via `tools/records.py` ([[D2-46 Weapons wear|D2-46]],
[[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]], [[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]], [[D2-262 The runs at a real river's size|D2-262]] to [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]], [[O-2 Make the eleven bulk processes take up to their batch|O-2]], [[W-76 The timber economy|W-76]], [[W-80 Design wave part 3a, keeping|W-80]], [[W-81 Design wave part 3b, taking|W-81]]). The documents listed under "Read with".

**Calculations and probes** (scratchpad, read-only): `w2/gates_making.py` (the gate probe of §4.3) and `w2/calc.py` (§2.1, §2.2,
§5): flax closes, the gear table at 1/7 and 1/15, withies' supply and demand, the fishing household's year, the tanner's year,
leather's demand.

**On the web:** none fetched in this session. Every sourced figure ([s]) comes through part 1 or the sibling notes, which give
their search sources (USDA Farmers' Bulletin 622 on basket willow, Durham 1956 via Forest Research, Rackham, Scientific American on
tanning yields, Encyclopaedia Britannica 1810 on tanning times, the Irish flax yields in Hansard, the 1533 flax act, the Severn act
of 1678, practitioners' nettle rates, netting rates in *Workshop Receipts*, the withy pot makers, Farmers Weekly on hurdles).

*Current as of 22 Nov 2026 ([[W-83 Design wave part 2, materials and making|W-83]]; nothing decided).*
