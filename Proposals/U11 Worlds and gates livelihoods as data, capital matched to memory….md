---
id: docs/cybertron2/proposals/w73_design/u11_worlds.md
kind: proposal
updated: "2026-11-22"
---
# U11 Worlds and gates: livelihoods as data, capital matched to memory, pin and fill, the gate check, the worked villages

*proposal · discussion (component spec, 22 Nov 2026). Nothing built; the gate check written, · `docs/cybertron2/proposals/w73_design/u11_worlds.md`*


**Status:** discussion (component spec, 22 Nov 2026). Nothing built; the gate check written, not run. The parts decided are cited
([[D2-266 Knowledge in their own words|D2-266]], [[D2-268 The founders' starting knowledge|D2-268]], [[D2-270 Household skills|D2-270]], [[D2-279 Stores, as answered|D2-279]], [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]], [[D2-288 Bulk goods are counted in handling units of a stated weight and every…|D2-288]] to [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]); the rest are defaults or open, marked.
**Owner:** 37.2 (the rows, the generator's people and capital, the worlds, the check); 37.4 is named on the merge where this unit
calls its core (the knowledge record, kept lines, the cast's models) (`engine/generate.py`'s knowledge, kept lines and cast).
**Thread:** the wave's integrated design ([[W-85 The wave's integrated design|W-85]]), under [[W-73 Fishing, hunting and their materials developed together|W-73]] and the nutrition worlds ([[W-69 Nutrition worlds|W-69]]).
**Feature units** ([[D2-244 The engine's reworking into feature packages|D2-244]]): **livelihoods** (the rows, their keeper and household lines' ids, the fill steps that read them),
**holdings** (the capital-knowledge registry and its two-way fill), **the gate check** (one runner over the people, making and dry
checks). The founders' line templates are U9's (`u9_people.md` §5); this unit places them.

## Extends

| Earlier | What this spec takes from it |
|---|---|
| docs/review/37_growth/02zzzh_hunt_fish/household_skills.md (with its 22 Nov addendum; answered in [[D2-270 Household skills|D2-270]]) | livelihoods as data rows with bands and specialisms; capital and knowledge as one record, filled both ways; the household's bands by age; neighbours and marriages; the village rule; pin and fill in eleven keyed steps; the static gate check; the knobs; the worked Eelmouth and Wenford |
| founders_knowledge.md (answered in [[D2-268 The founders' starting knowledge|D2-268]]) | the base and practice sets, the cultural strands, what not to seed, the budget |
| wave4_people.md §6 | fifteen rows; [[D2-270 Household skills|D2-270]]'s changes to the fill; the four people gate rows; Eelmouth remade and Hollinford end to end; the arms |
| wave2_making.md §4 (U3's) | the making gates M1 to M8 and the probe of today's worlds (`w2/gates_making.py`): the runs world fails M4 (no rock), M2 (no flax seed) and M3 (starts summer day 4) |
| proposals/livelihood_archetypes.md (37.4's, read, not edited) | archetypes chosen by the generator from the place and a world setting; tiers and a controllable spread; the generator's check that every resource or work has someone in reach who knows it; old worlds unchanged |
| proposals/knowledge_in_their_own_words.md §6 | a common set seeded to the founders only; culture as a parameter |
| docs/scenario_design.md | leverage and dependence; Opus at every pole of leverage, never an all-Haiku society; verify every access gate in a dry run, per action; read against a null arm |
| Decisions | [[D2-268 The founders' starting knowledge|D2-268]] (templates by hand, tested, from state; sets by age and expertise; less-seeded arms), [[D2-270 Household skills|D2-270]] (experts follow household size; two chokepoints in one household only when a world asks; apprenticed youths tried; the trader's lines roads and needs; the tanner row now; each coupling on by default, off only by explicit setting), [[D2-266 Knowledge in their own words|D2-266]] (the told-knowledge arm in early testing), [[D2-279 Stores, as answered|D2-279]] (management lines to the head), [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] (tanning in this build), [[D2-297 The catch stays as calibrated|D2-297]] and [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]] (the catch kept as calibrated; bots test interfaces only), [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]] (lifespan and stages), [[D4-64 Lines kept for good, passed on through care, replacing customs|D4-64]] (customs as kept lines seeded to those alive at the start) |
| Zach, 22 Nov (household_skills, opening) | "if we give a family a mill that should definitely be related to their seeded memories"; "design this system so skill distributions within and between households can be either hand designed or generated for a world, or like the generator some elements can be pinned" |
| Code | `engine/generate.py` (knows, aware_of, `line_born`, trade, cast, memories 270-430), `landgen/write.py` (FARMING 28, TRADES 29, capital by trade 384-420), `landgen/gates.py` (the dry probe), `engine/lore.py`, `engine/perceive.py` (seed_knowledge 53-89), `specs/make_nutrition_runs.py`, `specs/nutrition/runs_high.yaml` |

## Departures

| # | From | This spec | Why |
|---|---|---|---|
| 1 | household_skills §3.3 (16 to 19 lines an expert), founders_knowledge §4.2 (14 to 18), wave4 §3.2 (19 to 20) | one cap, 20 lines and about 800 words, with U9's protected lines and drop order | one number for the gate check to test (U9 §5.2; Basis row B9-2, open) |
| 2 | household_skills §2.3: "a seeded line whose condition is false: refuse (the template is skipped)" | skipped and reported, not a refusal | a false condition is the template working ([[D2-268 The founders' starting knowledge|D2-268]]'s "filled from state"); refusing would make every world without salmon fail |
| 3 | household_skills §2.1 seeds a holding's lines to its keeper and "a short form to the household"; wave4 dropped the short form | each household gets one holdings line naming every holding and its keeper; each holding a keeper line (U9 §5.6); a check refuses a holding with neither | Zach, 22 Nov; [[D2-270 Household skills|D2-270]]'s capital-knowledge coupling; one line a household rather than one a holding, because the heads of mixed houses would not fit the cap otherwise (worked in §7) |
| 4 | the runs world today (`runs_high.yaml`): the Salt House the Marshes', beside the weir | the Salt House and the Fen's spring to the Brooks | [[D2-270 Household skills|D2-270]]: two chokepoints in one household only when the world asks; the default fill does not make it (open question 2 asks whether this world should ask) |
| 5 | household_skills §6.1: Nichola an expert in traps and the runs | Nichola capable; one expert in a household of three working members | [[D2-270 Household skills|D2-270]]'s size rule |
| 6 | the runs world's arms (low, medium, high: skill and capital together; `make_nutrition_runs.py` ARMS) | two axes on the same people: seeded depth (full, half, base, none) and capital (as the old arms' holdings), each holding filling its keeper and lines both ways | [[D2-268 The founders' starting knowledge|D2-268]]'s less-seeded arms; the coupling means capital and its knowledge move together unless a world turns it off |
| 7 | `generate.py:352-364`: every adult of a line knows every line craft at known | bands and specialisms by member, level and skill by the craft's class (§3) | household_skills §0; the river run's equality (everyone knew the weir, nobody built one) |
| 8 | `generate.py:378`: "By trade:" from the first two crafts' labels | the livelihood line (U9 §2.2) | "sowing a field broadcast and reaping a crop" for every adult of a world with no fields |
| 9 | `generate.py:383-400`: strong models to the adults who know the most crafts | to the heads and the keepers of the chokepoints; capable adults Sonnet; broad and youths Haiku | scenario_design §2 |
| 10 | `generate.py:270-331`: four generated `memories` (founders, "hard winters you remember", a feud, a debt), shown as "What you remember" | PE1 to PE3 as kept lines (U9 §5.3); `memories` stays readable for hand-written worlds | [[D2-268 The founders' starting knowledge|D2-268]]: seeded lines are ordinary kept lines; 36 of 45 founders had the same hard-winter sentence |
| 11 | landgen `FARMING` for every household and the `TRADES` round-robin (`write.py:28-29, 384-400`) | livelihoods drawn by fit and the village mix; farming only where there are fields to hold | household_skills §5.2 step 3 |
| 12 | wave4 §6.4's Eelmouth: no seeded gear, the salt as today | each fishing household seeded with its likely gear (six wicker traps a member at capable or above who sets traps); the larder and salt as today | the world starts on summer day 4: wave2 §4.3 finds it fails M3 unless gear is seeded |
| 13 | wave4 §6.5's Hollinford rendered with today's engine rows | rendered on the current basis where basis.md gives the figure, the figure left to its unit where it does not | brief rule 3 |
| 14 | household_skills' carpenter and mason, charcoal burner | the builder (wright and mason) and the woodsman; the cottager added (the addendum, exploration) | the addendum; wave4 adopted it |
| 15 | the old gate (`landgen/gates.py`: each gather or work craft tried once) | one runner: the people checks here, U3's making checks, then the dry probe extended to make and build (U3's M8) | scenario_design §4: verify every access gate in a dry run, per action |

## Purpose

A world's households must need each other (scenario_design §1), and what a household holds and what its people remember must be
the same thing: a family with a mill knows the mill, a household with a weir knows the runs, and a household of fishers is not told
it lives by sowing. This unit makes the generator place livelihoods, capital and knowledge together, lets a world pin any part and
fills the rest, and refuses a world whose people cannot use what they hold before any run is spent on it.

---

## 1. Livelihoods as data

### 1.1 The row

One row a livelihood, in `engine/livelihoods.py` (one feature unit with its fill steps; the line templates it names are U9's in
`engine/founders.py`):

```yaml
fisher:
  status: built                     # built | network (this wave, by unit) | later
  fits: {covers: [water], best: "a river with runs"}
  words: {lives: "fishing", head: "the river"}                  # for U9's livelihood line
  broad: [fish by hand, angle, fishing rod, wicker traps (set), dry fish]
  capable: [salt fish, smoke fish, tend the smoke, wicker traps (make), creel]
  specialisms:
    weir_and_nets: {words: "the weir and its nets", crafts: [weir section, gill net, twist cord, mend gear],
                    capital: [weir], lines: [FI9, FI10, FI11, FI12]}
    traps_and_runs: {words: "the traps and the runs", crafts: [wicker traps (set), wicker traps (make), cut withies],
                     lines: [FI4, FI6, FI7, FI8]}
    hand_rod_dressing: {words: "the hand, the rod and dressing the catch", crafts: [the edge, a line, fishing rod, bone hooks, dress the catch],
                        lines: [FI5, FI13, FI14, FI15]}
    keeping: {words: "keeping the catch", crafts: [smoke fish, tend the smoke, smoke racks, salt fish, dry fish],
              capital: [smokehouse], lines: [FI16, FI17, FI18, FI19]}
  lines: {broad: [FI1, FI2, FI3], capable: [FI4, FI5], youth: [FI1, FI2], second: [FI1, FI2, FI3, FI5]}
  capital: {likely: [wicker traps x6 a setter, smoke racks], sometimes: [weir, smokehouse, withy bed, creels, gill net]}
  keeper_lines: {weir: FI12, smokehouse: FI17}
  depends: {needs: [salt, withies, cord], gives: [fish, dried fish, smoked fish]}
  neighbour_line: NB-FI
  apprentice: true                  # a youth may be apprenticed to a specialism of it ([[D2-270 Household skills|D2-270]])
```

Rules (household_skills §1.1): a craft sits in one band of a livelihood but may sit in several livelihoods; a specialism may repeat a
broad craft at expert depth; skilled-class crafts appear only in specialisms; a row whose `status` is not built cannot be drawn,
only pinned (and pinning it is a gate refusal until built).

### 1.2 The fifteen rows

★ a craft or holding of this wave (its unit named); † later. The crafts' classes are U3's (U9 §4.2).

| Livelihood | Fits | Broad | Capable | Specialisms | Capital likely / sometimes | Needs / gives | Keeper lines | Status |
|---|---|---|---|---|---|---|---|---|
| fisher | water, best a river with runs | as §1.1 | as §1.1 | weir and nets; traps and the runs; hand, rod and dressing; keeping | wicker traps, smoke racks / weir, smokehouse, withy bed★, creels★, gill net★ | salt, withies, cord / fish | FI12, FI17 | built; gear ★ (U2, U3) |
| farmer (arable) | fields by soil | sow, hoe, weed, reap, manure, dung, clear, burn the stubble, pest work, guard a field, bins | plough, select seed, dry fodder, a hearth loaf | ploughman and oxen; seed and harvest; hedge and field | fields, a granary floor, bins / an ox pair, plough and harness, a byre | the smith, the miller / grain | FA7, FA9 | built |
| herder or dairy | pasture, meadow, fen | herd, milk, fence, gates, hay, dung, stalls | slaughter, dry fodder, a hurdle★ | dairy; stock and breeding; hay and winter | a herd, grazing held, a byre / a cellar, hay | salt, hay land / milk, cheese, oxen, dung | HE7 | built |
| hunter and trapper | wood, scrub, heath, the wild | hunt, snares (set), dry meat, a crude weapon, a camp | stalk, den work, salt meat, a tent, a bedroll, snares (make) | stalking and drives; snares and small game; dressing the kill★ | a weapon, a bundle of snares, a far camp / a tent, hides | points, salt / meat, hides, bone | | built; dressing ★ (U3) |
| fowler | fen, flooded meadow, open water | fowling★, snares, gather young and eggs | a fowling net★, twist cord★, dry meat | nets and decoys; the freeze and the flight | a fowling net★ | cord / fowl | | ★ (U2, U3) |
| salter | a brine spring or saltmarsh | boil salt, salt meat, salt fish, firewood, cut | mend the brine pan, the saltmarsh pans | the pan; salting for keeping; carrying salt | a brine pan in a salt house / saltmarsh pans | copper, fuel / salt | SA4 | built |
| smith and miner | rock with ore within a day | charcoal, fetching ore, firewood | mine, a copper tool (rough) | smelting and tools; mining and charcoal; fittings | a forge, charcoal / a claim on the ore | charcoal, ore / copper | SM4 | built |
| miller and baker | a mill site; grain within a day | grind, a hearth loaf, bins | mill at millstones, oven bread, dress millstones | the mill; the oven | a mill / an oven, a hand mill | grain, the mason, the wright / meal, bread | MI3, MI5 | built |
| builder (wright, mason) | managed wood; rock within a day | fell, a small room, beds, bins, repair, clear for building, a woodshed | a medium room, a granary, a hearth, smoke racks | the wright; the mason | timber or stone in store, a woodshed / a quarry or wood claim | timber, stone / rooms, wheels, hearths | | built; builders ★ (U7, G7) |
| woodsman | managed wood | fell, cut young growth, firewood | charcoal, a camp, cut withies★ | charcoal; coppice† ([[W-76 The timber economy|W-76]]) | a wood's claim | buyers / charcoal, poles, firewood | | built; coppice † |
| basket maker | wet ground with willow | cut withies★, hurdles★ | wicker traps★, creels★, pack baskets★ | traps and creels; the withy bed | a withy bed★ | / traps, creels, hurdles | BA5 | ★ (U3, U7) |
| cord and nets | a close of good soil; still water or a pit | twist cord★ | sow and pull flax★, ret flax★ | flax and linen; nets | a flax close★ / a retting pit★ | / cord, nets | | ★ (U3, U4; flax below a plot open, W2-2) |
| tanner | water, an oak wood, hides within a day | dress hides | harness, a pack frame, shoes (leather work)★ | the pits (tanning, skilled) | tan pits★ by water, bark in store | hides, bark / leather | TA5 | ★ (U10; [[D2-270 Household skills|D2-270]], [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) |
| trader or carrier | a road with a track; villages 1 to 2 days apart | carry, travel, offers | a handcart, a pack ox | the road; the market | a handcart or pack ox, coin / a pack basket | / carrying | | built (always a second living) |
| cottager | a cottage and garden; work to hire | gather, a garden, the common's beasts, work for pay | spinning, baskets | none | a cottage, a garden lot / a beast on the common | work / labour | | built |

**Mixes in one household** (household_skills §3.1): at most two core livelihoods and one second trade; mixes that make sense (farmer
with herder, miller, baker or tanner; fisher with salter, basket maker, fowler or trader; hunter with tanner or woodsman; herder with
cord and flax; smith with woodsman or salter); not two livelihoods each holding a chokepoint unless the world asks ([[D2-270 Household skills|D2-270]]), nor two
that want the same season's whole days in a small house.

---

## 2. Holdings: capital and knowledge as one record ([[D2-270 Household skills|D2-270]]'s coupling)

### 2.1 The registry

One row a kind of holding, in `engine/livelihoods.py` beside the rows:

| Holding | Built? | Working craft; its keeper's band | Mending or upkeep craft | Keeper line (U9) | HL name and fact clause (U9 §5.6) | Fault it guards against |
|---|---|---|---|---|---|---|
| water mill (millstones, wheel, leat) | built | water mill, mill: the miller's **mill** specialism | clear the leat, dress millstones | MI3 | the mill | river run: the Fletchers held Middleham Mill and never milled |
| ox mill | built | mill: capable, and an ox | dress millstones | MI3 (its ox form) | the mill | |
| oven | built | oven bread: the **oven** specialism or capable | reline | MI5 | the oven | |
| weir | built | the weir's sections: **weir and nets** | the sections' wear by flow (U7) | FI12 | the weir | runs world low and medium: no weir; high: the weir fed the village |
| smokehouse (its racks) | built (U4 rebuilds) | smoke fish, tend the smoke: **keeping**, or capable | the fire; fire risk ([[D2-271 Smoking in three depths|D2-271]]) | FI17 | the smokehouse | the lake run: known by all, used by none |
| salt house and brine pan | built | boil salt: **the pan** | mend the pan with copper | SA4 | the Salt House | river run: the Brooks had the craft and the spring but no pan until day 3 |
| saltmarsh pans | built | the salt pans: broad salter | | (SA7) | the pans | |
| forge (hearth, anvil, bellows) | built | smelt, copper tool: **smelting and tools** | charcoal; the bellows' leather ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) | SM4 | the forge | river run: smiths with no rock in reach |
| cellar | built | cheese: **dairy** | | (HE5) | the cellar | |
| granary floor, bins (U5's containers) | built (U5 rebuilds) | broad | | (HH4) | the granary | |
| herd | built | herd, milk: broad herder; slaughter: capable | hay for winter | HE7 | the herd | pw1: "Slaughter ... took our last cow, not the bull" |
| ox pair, plough and harness | built | plough: **ploughman** | the share from the smith | FA7 | the ox team | |
| fields held | built | sow, reap: broad farmer | manure, rest | FA9 | the fields | |
| managed wood | built | fell, cut, charcoal | | (WO1) | | |
| withy bed | ★ U3, U7 | cut withies, plant: **the withy bed**, or capable | a fence against beasts | BA5 | the withy bed | |
| flax close, retting pit | ★ U3, U4 | sow, pull, ret: **flax and linen** | | (CO2, CO3) | the flax close | the fishers' water (U10) |
| tan pits | ★ U10 | tanning: **the pits** | bark, water | TA5 | the pits | |
| handcart, pack ox | built | carry: the trader | a road with a track; grazing | (TR2) | | |

A line in brackets is a livelihood line that covers the holding where no keeper line exists; such a holding is kept by any member
at its band, and is still named in the HL line.

### 2.2 Both ways

- **A pinned or drawn livelihood fills its capital.** `likely` capital is placed where the land allows it (a mill only at a mill
  site, a weir only on a water parcel on a river reach, a brine pan only at a spring); each `sometimes` item by a keyed draw
  (`capital_share`, default 0.5); what the land refuses is reported, not forced ("the fisher on a lake gets no weir").
- **Pinned capital fills its keeper.** A household given a mill gets the miller's livelihood (core or second) if it has none that
  works it; at least one member becomes its keeper: the expert in the specialism that works it, or a capable member in a small
  household; their keeper line and the household's HL line are seeded. **This is Zach's rule** (22 Nov): no holding is placed
  without the memory of it in its family.
- **A holding outside the household's livelihoods** (a farmer's hand mill) needs only the broad craft and seeds only its HL name.
- **Lines from state.** The keeper line is rendered from the holding's state at the start (its batch, wear so far, stock), after
  every holding is placed (step 9, §4), so the line and the state agree.
- **Gear** (traps, nets, snares, a handcart) is likely capital placed as goods in the household's store or the setter's hands; it
  seeds no holding line. Default count: a line of six wicker traps for each member at capable band or above who sets traps (Basis
  row B11-4; household_skills: "about six"; an estimate the live runs read, [[D2-297 The catch stays as calibrated|D2-297]]).

### 2.3 Who is a keeper

The keeper of a holding is a person (`holdings[h].keeper`), chosen in step 6: the household's expert whose specialism lists the
holding, else its most able member in the working craft at capable or above, else (a small house) the head raised to capable in it,
reported. The keeper is who the HL line names and who is told the holding's state; any member may work it (a household's things
count as every member's own: basis §6), and anyone may work a crew ([[D2-66 Field works in the first worlds, before weather exists|D2-66]]).

---

## 3. A household's people

### 3.1 Bands and specialisms by size ([[D2-270 Household skills|D2-270]])

| Role | Share | Core crafts | Specialism | Skill (by class: simple / practised / skilled) |
|---|---|---|---|---|
| expert | **1 for 2 to 4 working members, 2 for 5 or more** ([[D2-270 Household skills|D2-270]]; a world may set `experts`); never two in one specialism unless set | broad and capable at known | one at known, its skilled crafts too | the top half of the class's range (U9 §4.2): 1.05 to 1.3 / 1.1 to 1.6 / 1.25 to 2.0 |
| capable | about a third of the rest | broad at known, capable at capable | the expert's specialism at rough (the one they help with) | the middle of the range |
| broad | the rest | broad band: simple at known, practised at rough | none | the low end |
| a second trade | 1 to 2 members | that trade's broad band; one at capable | none | |

Depth by age ([[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]]'s stages; household_skills §3.2): youths broad and rough, capable from the older half of youth; prime adults the
experts (drawn first); elders the deepest lines, their skill faded toward its floor (U9 §4.3), their peak kept for teaching. The draw
within a household: rank working members by age within the prime span; the first takes the specialism that works the household's
most valuable holding; the second (if two) a different one; then the capable share, preferring the experts' partners and oldest
children. Each draw keyed (§4.3).

**Apprentices** ([[D2-270 Household skills|D2-270]]: tried): a youth in the older half of youth (at lifespan 64, 18 to 24 days old; [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]]'s shares) in a house
with an expert is apprenticed to that specialism by a keyed draw (`apprentice`, default 0.5): rough in it, its first line, the
livelihood line "learning ... from <expert>" (U9 §2.2), and the aim "learn <craft> from <expert>" (aims unshown, [[D4-29 No aims for now|D4-29]]; it drives
the bots and the measurement).

**Aptitudes** (U9 §4.8): set from each founder's seeded crafts' skills through their profiles, so a founder's aptitudes agree with
what they do.

### 3.2 The cast (scenario_design §2; departure 9)

| Who | Model (the world's `cast`) |
|---|---|
| each head; each keeper of a chokepoint (a mill, a weir, a brine pan, a forge, tan pits) | head (Opus) |
| capable adults, experts who are not chokepoint keepers | middle (Sonnet), one per household before a second (as `sonnet_extra` spreads now) |
| broad adults, youths | rest (Haiku) |

A world may override by person. The gate refuses an all-Haiku cast (§5, P17).

### 3.3 Neighbours, marriages, culture

As U9 §5.7 (household_skills §4): neighbours in a village aware of each other's broad bands, rough in one craft whose product their
household uses (a keyed draw), one neighbour line per other livelihood before the cap; a village within a day, its chokepoint crafts
aware and one line; further, nothing. A spouse who married in (the tree's `line_born`, `origin`) brings their natal broad band at the
level they left with and up to three of its broad lines; with `marriage_expert` (default 0.15) a capable specialism; `marriage_carry`
(default 1.0) turns it off. An origin outside the world brings only PE1's married form. A world's `culture` names one strand per
people (founders_knowledge Part 3), whose line U9 places.

---

## 4. Pin and fill: the generator's steps

### 4.1 What a world file may say

```yaml
skills:
  depth: full                  # full | half | base | none (U9 §5.2)
  experts: by_size             # by_size ([[D2-270 Household skills|D2-270]]) | an int per household
  spread: {capable_share: 0.33, experts_differ: true}
  apprentice: 0.5
  marriage_carry: 1.0
  marriage_expert: 0.15
  neighbours: rough_one        # none | aware | rough_one
  capital_share: 0.5
  village_mix: {fisher: 0.4, farmer: 1.0, salter: 0.2, miller: 0.3}
  region: {smith: 1, salter: 1}
  two_chokepoints: false       # [[D2-270 Household skills|D2-270]]: true lets one household hold two
  couple: {capital_knowledge: true, livelihood_land: true, crafts_capital: true, gates: true}   # [[D2-270 Household skills|D2-270]]: off only explicitly
households:                    # any household may be pinned in part or in full
  Marsh: {livelihoods: [fisher], experts: [weir_and_nets], capital: {weir: {parcel: Eelmouth_8, sections: [timber, timber, timber]}}}
  Brook: {livelihoods: [salter, fisher]}
agents:
  Nichola: {band: capable}
culture: {passing_on: a}       # founders_knowledge Part 3; U9 §5.7
```

A fully hand-written world lists every agent's `knows` and `kept` as now; the generator then fills nothing and runs only the gate
check. A world without `skills` keeps today's generation (old worlds replay).

### 4.2 The fill order

| Step | Fills | From | Code (today's) |
|---|---|---|---|
| 1 | land, villages, sites, covers | the configuration | `landgen` as now |
| 2 | pinned households' livelihoods and capital | the world file | new |
| 3 | unpinned households' livelihoods | `village_mix` over rows whose `fits` hold; region quotas first; the village rule (§5, P18) | replaces `FARMING` and `TRADES` (`write.py:28-29, 384-400`) |
| 4 | capital from livelihoods, and livelihoods from pinned capital | §2.2 | replaces capital by trade (`write.py:405-420`) |
| 5 | the family tree, members, marriages (`line_born`) | `generate.simulate` with lines carrying livelihoods | as now |
| 6 | each member's band, specialism, level, skill, aptitudes; keepers; apprentices | §2.3, §3.1, keyed per household | replaces `generate.py:352-364` |
| 7 | what spouses and fosterlings carry | §3.3 | widens `line_born` (`generate.py:355`) |
| 8 | neighbours' awareness and lines | §3.3 | replaces the `aware_of` loop (`generate.py:366-368`) |
| 9 | the seeded lines, rendered from U9's templates against the state of steps 4 to 8, with the cap and drop order | U9 §5 | `founders.render` (new; `lore.seed` widened), `memory.seed_line` with source "family lore" or "a holding" |
| 10 | the gate check | §5 | new runner (`landgen/gate_check.py`) beside `gates.py` and `economy.py` |
| 11 | the cast, the livelihood line, aims | §3.2; U9 §2.2 | replaces `generate.py:378-400` |

### 4.3 Repeatability

Every draw is keyed by what it is about (`landgen/keyed.py`): `(seed, "skills", household)`, `(seed, "expert", household, k)`,
`(seed, "apprentice", person)`, `(seed, "neighbour", person, livelihood)`, `(seed, "capital", household, holding)`. Pinning one
household or person leaves every other draw as it was, so a pinned arm and its unpinned twin differ only where pinned. The depth knob
changes only step 9 (and step 6's levels only at `none`), so a depth arm and its full twin have the same people, holdings and bands.

---

## 5. The gate check at world build

### 5.1 How it runs

One runner, `landgen/gate_check.py`, after step 9 (and for a hand-written world, after loading), in three passes: **the people
checks** (this unit, P1 to P21), **the making checks** (U3's M1 to M8, wave2 §4.2), **the dry probe** (`gates.py`, extended by U3's
M8 to try each make and build on a fresh copy). Each check is **refuse** (the world is not run as is), **warn** (reported in the
world's report, `<world>.report.json` beside the yaml, as now) or **report** (a fact for the reader). A coupling turned off in
`skills.couple` ([[D2-270 Household skills|D2-270]]) turns its checks to report, and the report lists every coupling off. The runner is deterministic and needs no
model.

### 5.2 The people checks

| # | Check | Level | Reads |
|---|---|---|---|
| P1 | a holding whose working craft no member of its household knows at the keeper's band (§2.1) | refuse | holdings, `knows` |
| P2 | a holding with no keeper line to its keeper, or a household holding anything with no HL line (Zach, 22 Nov) | refuse | the kept lines' sources against the holdings |
| P3 | a livelihood whose `fits` fail where its household lives (a farmer with no field) | refuse | rows, parcels |
| P4 | a template whose condition is false here | report (skipped; departure 2) | step 9's log |
| P5 | a founder's set over the cap after U9's drop order | refuse (the templates are too long) | step 9 |
| P6 | a filled line over 40 words, or a stated figure that differs from the state it names | refuse (the template's test failed) | step 9 against the state |
| P7 | a craft known at capable or above with no lesson rows | warn (its failures will only say "your hands") | U3's rows |
| P8 | a youth apprenticed to a specialism no one in the household holds at expert | refuse | step 6 |
| P9 | a craft at capable or above with no capital it needs within a day and no route to build it | refuse for a core livelihood, warn for a second | rows, holdings, roads |
| P10 | a holding whose mending craft nobody in reach knows (a pan and no smith in the region, a mill and no mason) | warn | holdings, the region |
| P11 | a chokepoint craft (smith, salter, miller) held nowhere in a region whose livelihoods need it | warn (a designed scarcity is allowed) | `depends.needs` |
| P12 | two experts of one household in one specialism when `experts_differ` | warn | step 6 |
| P13 | a household whose expert count differs from [[D2-270 Household skills|D2-270]]'s size rule when the world did not set it (a hand-written world) | warn | step 6 |
| P14 | a head without HH1, HH3 and HH7, or a head's partner or named heir without HH1 and HH3 ([[D2-279 Stores, as answered|D2-279]]) | refuse | step 9 |
| P15 | a pinned row whose `status` is not built | refuse | rows |
| P16 | a head or a chokepoint keeper not on the head model | warn | §3.2 |
| P17 | every acting person on one model of the weakest tier (an all-Haiku society) | refuse unless the world sets `cast.allow_weak: true` (a model-contrast arm) | the cast |
| P18 | the village rule: 2 to 5 livelihoods that hold capital (cottagers apart); at least one chokepoint inside; at least one need met only from outside, and a village in reach to meet it | warn | rows, holdings, roads |
| P19 | a weir with fewer than two working members in its household and no agreement for a crew | warn | holdings |
| P20 | a seeded `kept` or `custom` line naming a price, a score or a grade (a word list: "graded", "score", "points", a price pattern) | refuse (scenario_design §3; founders_knowledge Part 4.1) | kept lines, customs |
| P21 | the old prompt reachable (no `view: beliefs`, or the options list in the code) | refuse ([[D2-286 The list of what one could do today|D2-286]]) | the world spec; the code |

### 5.3 What today's worlds show (read from the files, not run)

- **The runs world** (`specs/nutrition/runs_*.yaml`): P3 fails for every adult (no livelihood rows; "By trade: sowing a field
  broadcast and reaping a crop" in a world with no fields); P2 fails for the three smokehouses and the weir (no line about any of
  them; the seeded `memories` are founders, a hard winter, a feud, a debt); with the salt house the Marshes' beside the weir, two
  chokepoints in one household without the world asking (departure 4). U3's probe (wave2 §4.3): M4 (no rock, three crude tools for
  twelve people), M2 (no flax seed), M3 (summer day 4 start, no gear).
- **The river worlds, Wenbridge, the region and frontier worlds:** U3's table (wave2 §4.3). The people checks on them are not
  worked here (I have not read them as closely; they are not the worlds this wave runs).

---

## 6. The arms this generation makes

The same seed with: **depth** full, half, base, none ([[D2-268 The founders' starting knowledge|D2-268]]'s less-seeded arms; U9 §5.2); **capital** as the old runs arms' holdings
(high: weir, smokehouses, salt house; medium: smokehouses, no weir; low: none), each filling its keepers and lines both ways; **the
told-knowledge arm** (every line to everyone in the system text; [[D2-266 Knowledge in their own words|D2-266]]: early testing only); **experts differ** on or off;
**marriage carries** on or off; **one cultural strand at a time** (BS8's passing on first, U9 §5.7); **a coupling off** by explicit
setting ([[D2-270 Household skills|D2-270]]), run once as a fault arm. Each read against the null arm of the same set-up and a qualitative end-state reading
(scenario_design §6); the catch is read as calibrated, in live runs ([[D2-297 The catch stays as calibrated|D2-297]]).

---

## 7. Eelmouth remade (the runs world)

**Now** (`runs_high.yaml`; read 22 Nov): one village of three households on the Isel (a big river reach), lifespan 64, 64 days from
summer day 4 (two autumn runs, two winters), `view: beliefs`, evening on, tags on. Ten parcels: the Street (built), Clay Field and
Eelmouth Field (scrub), Brook Meadow (meadow), Eelmouth Common and the Leaze (pasture), the Spinney and Hazel Copse (forest), Eelmouth
Fen (fen, with the brine spring), the Isel (water); two wild nodes (Oakhurst, Cragton). No herds, no fields, no rock. Each house holds
28 timber, firewood (60, 60, 42), dried meat and roots for about the 8-day larder; a smokehouse each on scrub off the Street (one set
of racks, the wattle hut); the Marshes hold the weir (three timber sections) and the Salt House (a brine pan, 10 salt, 20 firewood).
All six adults know the same seven crafts at skill 1.6 (high arm), and the same "By trade: sowing".

**The fill, step by step:**

1. Land as the world has it.
2. **Pinned** (this world's design, [[W-69 Nutrition worlds|W-69]]: can a village live off the runs alone; the maker's docstring): Marsh fisher with the weir (the high and weir-in
   arms); Shepherd fisher, with fowling as a second living (the fen); Brook salter, with fishing as a second living. `village_mix`
   is not used: the three are pinned. Herders and farmers are kept out by the world (no herds, no fields), as today.
3. No unpinned households.
4. **Capital:** the weir to the Marshes (pinned); the Salt House and its pan to the Brooks (the salter's likely capital at the
   spring; departure 4); the three smokehouses kept, the Shepherds' as the keeping specialism's capital, the Marshes' and Brooks' as
   `sometimes` capital (each household smokes); gear: six wicker traps for each member at capable or above who sets traps (Basis
   row B11-4): the Marshes 12 (Peter, Nichola), the Shepherds 6 (Hamon), the Brooks 6 (Katherine); a gill net to the weir-and-nets
   expert (U3's net; ★ until built). The larder and the salt (10 kg: salt for 40 kg of fish at [[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]]'s 1 to 4) as today; the
   salt's sufficiency is the live runs' to read ([[D2-297 The catch stays as calibrated|D2-297]]).
5. **Members** as the tree has them (the three wives came from Ashby, outside the world).
6. **Bands and keepers** ([[D2-270 Household skills|D2-270]]: one expert in each household, all three having two or three working members):

| Household | Livelihoods | Head | Members: band, specialism, keeping | Cast |
|---|---|---|---|---|
| **Marsh** | fisher | Peter | Peter: expert, **weir and nets**, keeper of the weir; Nichola: capable fisher (helps at the weir: rough in weir and nets), keeper of the Marsh Smokehouse; Nigel (youth, 18 days, the older half of youth): broad, apprenticed to the weir and nets **if the keyed draw falls so** (default 0.5; I do not know which way seed 5's draw falls; shown apprenticed); Henry (child, 5 days), Denise (infant) | Peter Opus, Nichola Sonnet, Nigel Haiku |
| **Shepherd** | fisher; fowling second | Hamon | Hamon: expert, **keeping**, keeper of the Shepherd Smokehouse; Gunnild: broad fisher, broad fowler | Hamon Opus, Gunnild Haiku |
| **Brook** | salter; fishing second | Oliver | Oliver: expert, **the pan**, keeper of the Salt House; Katherine: broad salter, capable fisher, keeper of the Brook Smokehouse; Petronel (youth, 14 days, the younger half: not apprenticed): broad salter; Margery (child), Basilia (infant) | Oliver Opus, Katherine Sonnet, Petronel Haiku |

7. Marriages: Nichola, Gunnild and Katherine came from Ashby, outside the world: PE1's married form only.
8. Neighbours: each household aware of the others' broad bands; rough in one craft whose product it uses by the keyed draw (the
   Shepherds and Marshes at salting fish, the Brooks at setting traps, if the draws fall so); one neighbour line per other livelihood.
9. **The seeded lines** (U9 §5; with every ★ line of this wave built; the cap's steps named):

| Person | Lines before the cap | Steps taken | Seeded (20 or fewer) |
|---|---|---|---|
| Peter | 27: BS1 to BS9, PE1, PE2 (the pig), HH1, HH3, HH5, HH6, HH7, HH8, FI1 to FI3, FI9 to FI12, HL, NB-SA, NB-FO | 1, 2, 3, 4, 7 (BS9, BS7, BS6) | **20** |
| Nichola | 22: BS1 to BS9, PE1 (married), HH1, HH3, FI1 to FI5, FI9 (helping), FI17 (keeper), HL, NB-SA, NB-FO | 1, 7 (BS9) | **20** |
| Nigel | 10: BS1, BS2, BS3, BS5, BS8, PE1, FI1, FI2, FI9 (apprenticed), HL | none | **10** |
| Henry | 2, as if passed by Nichola in care: FI1, HL | | **2** |
| Hamon | 25: BS1 to BS9, PE1, HH1, HH3, HH5, HH6, HH7, HH8, FI1, FI2, FI16 to FI19, FO1, FO2, NB-SA (no HL: he keeps the household's only holding) | 3, 4, 6 (FO2), 7 (BS9, BS7) | **20** |
| Gunnild | 20: BS1 to BS9, PE1 (married), PE2 (the timber she owes Peter, the grain Oliver owes her), HH1, HH3, FI1 to FI3, FO1, FO2, NB-SA, HL | none | **20** |
| Oliver | 28: BS1 to BS9, PE1, PE2 (the pig), HH1, HH3, HH5, HH6, HH7, HH8, SA1, SA2, SA3, SA4, FI1, FI2, FI3, FI5, HL, NB-FI, NB-FO | 1, 2, 3, 4, 6 (FI2, FI3, FI5), 7 (BS9) | **20** |
| Katherine | 21: BS1 to BS9, PE1 (married), HH1, HH3, SA1, FI1 to FI5, FI17 (keeper), HL, NB-FO | 7 (BS9) | **20** |
| Petronel | 8: BS1, BS2, BS3, BS5, BS8, PE1, SA1, HL | none | **8** |

   Rendered from the state: FI1 reads `RUNS.eel` (autumn, the cue `rain_after_dry`); FI6 is not in any set here (no traps-and-runs
   expert); FI7 drops unless the Isel has lampreys; FI19 renders for Hamon with no road ("Salt comes from the Brooks' Salt House on
   the Fen; the salter there wants firewood and grain"), its second sentence dropped (no farm household in reach); SA6 drops (no
   village within two days); HH2 drops everywhere (no fields); BS2's fields clause drops (no fields); BS7's frost clause drops (no
   crops). HH1 for the Marshes, from today's store and [[D2-292 The food unit|D2-292]]'s rations (two adults and a youth at 1, a child 0.6, an infant 0.5:
   4.1 a night): "Our store at Marsh House holds about 11 nights' food for the 5 of us as it stands; winter is 8 nights, and the
   hungry time is its end and the first days of spring." (18 dried meat x 1.2 + 84 roots x 0.263 = 43.7 food; a youth's ration of 1
   is an assumption: [[D2-292 The food unit|D2-292]] names adults, children and elders only.) The Marshes' HL is U9 §5.6's example.

10. **The gate check:**

| Check | Result |
|---|---|
| P1 keepers | the weir Peter (known), the Shepherd Smokehouse Hamon (known), the Marsh Smokehouse Nichola (capable), the Brook Smokehouse Katherine (capable), the Salt House Oliver (known): pass |
| P2 memory | every holding has its keeper line; the Marshes' and Brooks' HL lines name theirs: pass |
| P3 fits | fisher (the Isel, a river with runs), salter (the Fen's brine spring), fowling (the fen): pass. Today's world fails here for every adult |
| P5, P6 cap and lines | pass on the counts above; the 40-word test is the templates' (U9 §7) |
| P7 lessons | warn until U3 writes lessons for boil salt, the weir section and tend the smoke (learning_times §5 has smoking, salting, netting and the hurdle, not the pan) |
| P8 apprentice | Nigel to Peter's weir and nets: pass |
| P9 capital in reach | smoking to the smokehouses, boil salt to the pan, wicker traps to withies on the fen and banks, the net to wild cord: pass |
| P10 mending | the brine pan wears and wants copper; no smith in the region: **warn** |
| P11 chokepoint craft | copper held nowhere; the pan needs it: **warn** (designed scarcity, or not: open question 4) |
| P16, P17 cast | three Opus at the three heads, who are the three keepers of chokepoints and of keeping; two Sonnet; three Haiku: pass |
| P18 village rule | two livelihoods holding capital (fisher, salter), chokepoints inside (the weir, the pan), needs from outside (copper, stone) with **no village in reach** to meet them: **warn** (by design: the world tests whether a village lives off the runs alone) |
| P19 weir crew | the Marshes have three working members: pass |
| P20 kept lines | no price, score or grade: pass (the river run's seeded "YOUR GOAL, on which you will be graded" is not in this world) |
| U3's making checks | M4 no rock within a day: **warn** (three crude tools; when they wear out no one can remake one); M3 the start on summer day 4: pass with the seeded traps; M2 no flax household: not applicable |

    **Pass, with five warnings** (P7's lifts when U3 writes the lessons).

11. Cast and livelihood lines: "You live by fishing, and you are best at the weir and its nets, and you keep the weir on the Isel"
    (Peter); "You live by boiling salt at the spring, and by fishing beside it, and you keep the Salt House" (Oliver); "You live by
    fishing, and by fowling on the fen beside it, and you are best at keeping the catch, and you keep the Shepherd Smokehouse"
    (Hamon).

**Dependence:** the Marshes take the run at the weir and hold the most traps; the Brooks hold the salt every keeper needs for the
hard cure and salt fish; the Shepherds keep best and have the fen's fowl in winter. Each lacks what another holds, where today each
house holds everything. Inside, two chokepoints (the weir, the pan) in two households, and the keeping skill in a third; outside,
nothing can be had (by the world's design). **Arms:** depth (full, half, base, none) x capital (high, medium, low as the old arms'
holdings) on the same people; the told-knowledge arm once in early testing.

---

## 8. Hollinford, a mixed village, end to end (a configuration; the farm world for the live runs, open question 5)

A middle river with runs (eels, no salmon), clay and loam fields, an oak wood, a wet fen edge with willow, a mill site; Highpool (the
smith, with rock) a day up the hill road with a track; Saltwell (the salter) a day downstream. Lifespan 64, `view: beliefs`, evening
on.

1. Land: twelve parcels (four fields, two pastures, a meadow, the oak wood, the fen edge, the river, the Green, a garden lot).
2. Pinned: none. `village_mix: {farmer: 1.0, miller: 0.4, fisher: 0.5, builder: 0.3, tanner: 0.2, cottager: 0.3}`, `region: {smith:
   1, salter: 1}`.
3. Six households drawn (keyed).
4. Capital from livelihoods: the mill at the site (the miller's likely), a weir on the river above the mill (the fisher's
   sometimes, drawn), tan pits by the ditch below the mill (the tanner's), a withy bed on the fen edge (the basket maker's, the
   Fenns' second living), a granary floor and an ox pair (the farmer's).
5. to 8. Members, bands, marriages, neighbours ([[D2-270 Household skills|D2-270]]'s size rule throughout):

| Household (working) | Livelihoods | Holdings | Expert | Capable / broad / youth | Keepers | Cast |
|---|---|---|---|---|---|---|
| **Field** (5) | farmer; herder | four plots, a granary floor, an ox pair and plough, a byre, three cows | Osric (ploughman and oxen), Orabel (seed and harvest): two, for five | Baldwin capable herder; Drew, Hawise broad; Hob youth, apprenticed to the plough if drawn | Osric the team; Orabel the fields; Baldwin the herd | Osric Opus (head, the largest land), Orabel Sonnet, Baldwin Sonnet |
| **Fletcher** (4) | miller and baker; farmer | the water mill, an oven, a plot | Hamo (the mill) | Annora capable (oven bread); Alard broad; Piers youth | Hamo the mill; Annora the oven | Hamo Opus (head, chokepoint) |
| **Fenn** (4) | fisher; basket maker | the weir above the mill, a wattle smoke hut (one set of racks, [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]]), two lines of traps, the withy bed | Aldric (weir and nets) | Lucy capable (keeping at rough); Matthew broad, cuts withies; Wilmot youth | Aldric the weir; Lucy the smoke hut; Matthew the withy bed (raised to capable in cutting withies, reported: P1) | Aldric Opus (head, chokepoint) |
| **Mason** (3) | builder; farmer | stone and timber in store, a woodshed, a plot | Ralf (the mason) | Emma capable (the wright at rough); Simon youth | | Ralf Sonnet (head; no chokepoint held, though every hearth and the mill's stones need him: P16 warn) |
| **Tanner** (3) | tanner; farmer | tan pits below the mill, a plot, hides in store | Godric, an elder (the pits; skill faded toward its floor, peak kept) | Agnes capable tanner; Walter broad | Godric the pits | Godric Opus (head, chokepoint: the leather of every pack frame, harness and bellows) |
| **Cotter** (3) | cottager | a cottage, the garden lot, a cow on the common | none (a cottager has no specialism) | Tobin, Rose broad (spinning capable); Joan youth | | Tobin Haiku |

Rose Cotter married in from the Fenns: she carries the fisher's broad band at rough and FI1 and FI3 in her own voice ("At home with
the Fenns we went back to every trap each morning of the run").

9. The heads' seeded lines (U9 §5; ★ lines counted as built):

| Head | Lines before the cap | Steps | Seeded |
|---|---|---|---|
| Hamo | 30: BS1 to BS9, PE1, HH1, HH2, HH3, HH5, HH6, HH7, HH8, MI1, MI2, MI3, MI4, HL, FA1, FA2, FA3, five NB | 1, 3, 4, 6 (FA2, FA3), 7 (BS9, BS7) | **20** |
| Aldric | 31: BS1 to BS9, PE1, HH1, HH3, HH5, HH6, HH7, HH8, FI1 to FI3, FI9 to FI12, HL, BA1, BA2, five NB | 1, 3, 4, 6 (BA2), 7 (BS9, BS7, BS6), 8 | **20** |
| Godric | 32: BS1 to BS9, PE3, PE1, HH1, HH2, HH3, HH5, HH6, HH7, HH8, TA1 to TA5, HL, FA1, FA2, FA3, five NB | 1, 3, 4, 6 (FA2, FA3), 7 (BS9, BS7, BS6), 8 | **20** |
| Osric | 31: BS1 to BS9, PE1, HH1, HH2, HH3, HH4, HH5, HH6, HH7, HH8, FA1, FA2, FA3, FA6, FA7, HL, HE1, HE2, five NB | 1, 3, 4, 6 (HE2), 7 (BS9, BS7, BS6), 8 | **20** |
| Tobin | 23: BS1 to BS9, PE1, HH1, HH3, HH5, HH6, HH7, HH8, CT1, CT2, five NB (no HL: he keeps the cow, the household's one holding) | 1 | **19** |

   Rendered on the current basis where basis.md gives the figure: HH6 for every house, "The hearth burns about a bundle of firewood
   a night and three on a cold one: a winter wants about {8 to 24} bundles in by autumn's end" ([[D2-290 Fuel a house burns a night is at its real weight|D2-290]]: 8 winter nights; the figure
   reads the climate's expected cold nights, which I do not know for this configuration); BS2's "about three times"; HU2's and SA6's
   ten kilos on foot (basis §5); FA7's plough and hoe units and MI3's batch from U7's and U3's rows (not set here). The rest read the
   generated state and cannot be rendered before the generator runs.

10. **The gate check:** P1 every holding has a keeper at its band (the withy bed's Matthew raised to capable and reported); P2 every
    household's HL line and every keeper line placed; the mill's batch passes with "up to" ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]); the pits below the mill and the
    weir above it: TA5 renders "downstream of us there is no one", so no fishery is fouled (U10 reads it); P10 the mill's stones and
    the hearths have a mason in the village (Ralf), the plough's share a smith a day off (Highpool): pass; P11 salt and copper are
    made a day off (Saltwell, Highpool), reached by road: pass, a designed dependence; the tanner's hides come only from the Fields'
    herd (no hunter within a day): warn (P9, a second need); P16 Ralf, the mason, is not on the head model though the mill's stones
    and every hearth need him: warn; P18 five livelihoods hold capital (farmer, miller, fisher, builder, tanner), three chokepoints
    inside (the mill, the weir, the pits), salt and copper from outside: pass. U3's M2: no flax household, so no flax seed needed; M4
    rock at Highpool, a day off: pass. **Pass, with two warnings and one report** (and P7's, until U3's lessons are written).

**Dependence and leverage:** the mill needs the Fields' grain and the Fields need the mill to make grain go further; the weir above
the mill shares the eels with the mill's hatches (MI4, FI9); the tanner needs the Fields' hides and the oak wood's bark and gives the
leather of packs, harness and the smith's bellows; the Masons are needed by every hearth, the oven and the mill's stones; the Cotters
are the hands at reaping and the runs. Three chokepoints inside, one each; salt and copper outside (scenario_design §1: several
interlocking chokepoints).

---

## 9. Code changes

| File | Where | Change | Owner |
|---|---|---|---|
| `engine/livelihoods.py` (new) | | the fifteen rows (§1), the holdings registry (§2.1), the fill steps 2 to 4 and 6 to 8 | 37.2 |
| `engine/generate.py` | 270-331 (memories), 352-378 (knows, aware_of, trade), 383-400 (cast) | read the rows and the registry when `skills` is set; PE lines in place of `memories`; the cast by poles of leverage; old behaviour when `skills` is absent | 37.2 (named to 37.4) |
| `landgen/write.py` | 28-29, 384-420 | `FARMING`, `TRADES`, capital by trade kept for worlds without `skills`; new worlds go through `livelihoods` | 37.2 |
| `engine/founders.py` (new; U9's templates) | | `render(w, name, role)` called in step 9; the cap and drop order | 37.2 |
| `engine/perceive.py` | `seed_knowledge` 53-89 | seed the rendered lines with their sources ("family lore", "a holding", "a custom"); `come_of_age` as now | 37.4 |
| `landgen/gate_check.py` (new) | | the runner of §5: P1 to P21, U3's M1 to M8, then `gates.py`; writes the report | 37.2 |
| `landgen/gates.py` | 45 (gather and work only) | extended to make and build (U3's M8) | 37.2 |
| `specs/make_nutrition_runs.py` | ARMS 37-48, the high arm's weir crew 54 | rewritten on `skills`: the three pinned households of §7, depth and capital as two axes | 37.2 |
| `specs/` a Hollinford maker (new) | | §8's configuration | 37.2 |
| `tests/` | new | §10 | 37.2 |

## 10. Tests

| Test | Checks |
|---|---|
| `test_fill_keyed` | pinning one household leaves every other draw as it was; a depth arm and its full twin have the same people, holdings and bands |
| `test_both_ways` | a pinned mill fills a miller with a keeper, a keeper line and an HL line; a pinned fisher on a lake gets no weir and the report says why |
| `test_experts_by_size` | 2 to 4 working members give one expert, 5 or more two, different specialisms |
| `test_apprentice` | only youths in the older half of youth, in a house with an expert, by the keyed draw |
| `test_gate_people` | each of P1 to P21 refuses or warns on a fixture built to fail it, and passes the remade Eelmouth with exactly §7's five warnings |
| `test_old_worlds` | every world without `skills` generates as before (byte-identical yaml) |
| `test_cast` | heads and chokepoint keepers on the head model; an all-Haiku cast refused unless allowed |

**What live runs should read** ([[D2-297 The catch stays as calibrated|D2-297]], [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]; scenario_design §6): on the remade Eelmouth and on Hollinford, each against its null
arm and with a qualitative end-state reading: whether keepers use their holdings (the weir's gap, the smokehouse's racks, the pan, the mill);
whether the less-seeded arms learn the runs and keeping, and how fast; what is taught and to whom (the apprentices); trade between
households for salt and fish; whether the cap's dropped lines (BS6, BS7, BS9, the neighbours) are missed.

## Basis rows needed

| Row | Value | Mark |
|---|---|---|
| **B11-1 Experts by household size** | 1 for 2 to 4 working members, 2 for 5 or more; a world may set it | decided ([[D2-270 Household skills|D2-270]]) |
| **B11-2 Apprentices** | the older half of youth (18 to 24 days at lifespan 64), in a house with an expert, by a keyed draw of 0.5 | decided in rule ([[D2-270 Household skills|D2-270]]); the age and draw default |
| **B11-3 Generation knobs** | `capital_share` 0.5, `marriage_carry` 1.0, `marriage_expert` 0.15, `capable_share` 0.33, `neighbours` rough_one | default |
| **B11-4 Seeded gear** | a line of six wicker traps for each member at capable band or above who sets traps; a gill net to a weir-and-nets expert | default (estimate; the catch read in live runs, [[D2-297 The catch stays as calibrated|D2-297]]) |
| **B11-5 The village rule** | 2 to 5 livelihoods holding capital; at least one chokepoint inside; at least one need from outside, with a village in reach | default (household_skills §4.3) |
| **B11-6 The cast** | heads and chokepoint keepers on the head model; capable adults the middle; broad and youths the rest; never all on the weakest | decided in rule (scenario_design §2); default as the generator's rule |
| **B11-7 A youth's ration** | 1 food a night (as an adult) for HH1's and BS5's figures | open: [[D2-292 The food unit|D2-292]] names adults, children and elders only (U0) |

## Gaps

| Gap | State |
|---|---|
| Matching capital to memory (Zach, 22 Nov) | designed (§2, P2) |
| The gate check's people side | designed (§5.2); written, not run |
| A village whose outside needs no village can meet (the runs world) | reported by P18 as a warning; the design choice is open question 4 |
| The salt's sufficiency in the remade Eelmouth (10 kg) | left to the live runs ([[D2-297 The catch stays as calibrated|D2-297]]); not recalibrated here |
| No rock within a day of Eelmouth (U3's M4) | warned; open question 3 |
| The generator's history dates its hard winters in tree years, four within a few days of each other in `runs_high.yaml` (`history` days -6, -4, -3, -2) | PE3 counts them as written; I do not know whether `day` there is in days or years, so PE3 waits on a check of `generate.simulate`'s `year` (gap for 37.2) |
| The told-knowledge arm's place in the system text | designed in U9 §5.2 |
| Tanning, retting and the withy bed in the remade worlds | the rows are ★ until U3, U4, U7 and U10 build them; worlds needing leather or a bearing bed in their first year seed them in their state (audit q23's (a)) |

## Open questions for Zach

1. **Whether this reading of your mill rule is right: every holding gives its keeper a line about it, and every household one line
   naming all it holds and who keeps each** (no id; [[D2-270 Household skills|D2-270]]'s capital-knowledge coupling; household_skills, 22 Nov). Options: (a) a
   keeper line a holding and one household line a household (this spec); (b) a line a holding to every member (the heads of mixed
   houses then exceed the cap of 20); (c) the keeper only. Recommend (a). Blocks: step 9 and check P2.
2. **Whether the remade runs world should keep the Salt House with the Marshes beside the weir** ([[D2-270 Household skills|D2-270]]: two chokepoints in one
   household only when a world asks). Options: (a) the Salt House to the Brooks, as the default fill does; (b) the world asks for two
   in the Marshes, as today. Recommend (a): three households each holding something another lacks is the leverage the world is for.
   Blocks: the remade runs world.
3. **Eelmouth has no rock within a day, so its three crude tools cannot be remade once worn** (U3's M4). Options: (a) add a rock
   parcel a day off (a quarry road); (b) seed more crude tools; (c) accept it as part of the runs-only test. Recommend (a): the
   world's question is the runs, not tools, and stone from outside is a dependence worth having. Blocks: the remade runs world's long
   arms (64 days).
4. **Whether the runs world should have any village in reach** (P18; the runs-only design, [[W-69 Nutrition worlds|W-69]]). Options: (a) none, as today: copper, stone and
   trade cannot be had; (b) one village a day or two off with a smith or grain, so salt and fish can be traded. Recommend (a) for the
   runs-only arm (it is the experiment) and (b) as a separate arm later. Blocks: nothing now.
5. **Hollinford as the farm world for the live runs** (README's last stage). Options: (a) Hollinford as configured here; (b) a
   remade existing farm world (Brookend or Barleyfield) with livelihoods pinned; (c) both. Recommend (b) first, for comparison with
   past runs (checked against later fixes, [[D2-287 Reviewing past runs|D2-287]]), then (a). Blocks: the live runs' second world.
6. **Gear seeded with the fishers** (B11-4). Options: (a) six traps a capable setter and a net to the weir expert; (b) none, so the
   first summer is spent making gear (wave2 §5.1: 56 of 80 units before the first run); (c) a world setting. Recommend (a) for the
   remade runs world, (b) as an arm. Blocks: the remade runs world.
7. **A youth's food a night** (B11-7; [[D2-292 The food unit|D2-292]] names adults, children and elders). Options: (a) as an adult; (b) between child and
   adult (0.8). Recommend (a) until U0 says otherwise. Blocks: HH1's and BS5's figures only.

## Sources

`docs/review/37_growth/02zzzh_hunt_fish/household_skills.md` (and addendum), `founders_knowledge.md`, `wave4_people.md` §6,
`wave2_making.md` §4, `wave_conflicts.md` §5, §6 (questions 10, 15, 23), `morning_23nov.md`; proposals `livelihood_archetypes.md`
(37.4's), `knowledge_in_their_own_words.md` §6; `w73_design/README.md`, `basis.md`, `u9_people.md`; `docs/scenario_design.md`;
DECISIONS [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], [[D2-266 Knowledge in their own words|D2-266]], [[D2-268 The founders' starting knowledge|D2-268]], [[D2-270 Household skills|D2-270]], [[D2-279 Stores, as answered|D2-279]], [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]], [[D2-286 The list of what one could do today|D2-286]], [[D2-288 Bulk goods are counted in handling units of a stated weight and every…|D2-288]] to [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]], [[D4-29 No aims for now|D4-29]], [[D4-64 Lines kept for good, passed on through care, replacing customs|D4-64]]; items [[W-69 Nutrition worlds|W-69]], [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]], [[W-85 The wave's integrated design|W-85]].
Code read: `cybertron2/engine/generate.py`, `landgen/write.py`, `engine/lore.py`, `engine/perceive.py`, `engine/memory.py`,
`engine/data.py` (ITEMS, PHYSICS, LIFE), `wild/kinds.py` (RUNS), `specs/make_nutrition_runs.py`, `specs/nutrition/runs_high.yaml`
(its agents, buildings, stores, tree and history, read 22 Nov).

*Current as of 22 Nov 2026: [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] to [[D2-298 Bot runs test interfaces and basic functioning only|D2-298]].*
