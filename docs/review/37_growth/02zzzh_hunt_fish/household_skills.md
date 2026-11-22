# Household skills: livelihoods as data, who in a house knows what and how deeply, the capital that goes with it, and the generator's pin-and-fill

22 Nov 2026, 37.2 (subagent). A session note for the livelihood archetypes (W-70, D2-243), knowledge in their own words (Q-81,
D2-266) and the founders' starting knowledge (founders_knowledge.md, answered in D2-268). No code changed; nothing decided.

**Zach (22 Nov):** "design archetypes / distributions of household skills: eg a house can have 1-2 core livelihoods / trades, with
most people knowing some broad set of related things, a smaller set being very capable in less, and one or two experts in the core
skills. The amount of seeded knowledge should vary based on expert or not, and if there are multiple experts probably best to be
different things eg one might be very good with the weirs like building them and nets while another knows the fishing by hand and
rod and the butchering techniques etc. The depth of seeded memories should track both the assigned expertise and age, and also
households can start with multiple quite distinct skill sets eg maybe they are farmers and leather tanners or traders etc. ...
design this system so skill distributions within and between households can be either hand designed or generated for a world, or
like the generator some elements can be pinned like 'this household is expert on this etc' and other gaps filled in like neighbours
having some knowledge or an intermarriage bringing knowledge." And: "It should also connect in with the capital and resources of
the world: if we give a family a mill that should definitely be related to their seeded memories."

**D2-268, as relayed:**
- Seeded lines are ordinary kept lines that can be dropped and replaced ("a seeding that can grow or die").
- Templates are written by hand and tested, and filled from state where they state a fact.
- The sets are built up front and tested as the materials network (W-73) is integrated.
- A founder's set depends on their age and expertise.
- Arms with less seeded knowledge, to see how much they can learn.

**Read with:** founders_knowledge.md (the base set, the practice sets, the budget); proposals/livelihood_archetypes.md;
trying_and_learning.md (difficulty classes); hunt_fish_materials.md (the network's goods and works); crafts_evaluation.md (gate
faults); `cybertron2/landgen/write.py` (TRADES, lines, capital by trade); `cybertron2/engine/generate.py` (knows, aware_of,
`line_born`, trade, cast); `cybertron2/engine/lore.py`; `cybertron2/specs/make_nutrition_runs.py`; `cybertron2/landgen/gates.py`,
`economy.py`.

## The short answer

- **A livelihood is a data row.** It lists its crafts in a **broad** band (what most of the household does), a **capable** band,
  and two to four **specialisms**, each with its own crafts and knowledge lines. It also lists where it fits, the capital it
  plausibly holds, and whom it depends on. Fourteen livelihoods cover the engine's crafts and the network's new ones (§1).
- **Capital and knowledge are one record.** Every holding (a mill, a weir, a brine pan, a forge, a herd, a withy bed) names the
  crafts that work it and mend it, the band its keeper needs, and the lines it seeds (what it does, its batch, its upkeep, its
  season, who depends on it). Pin a livelihood and the generator fills its capital; pin capital and it fills the household's
  knowledge. The gate check refuses a world where a holding has no keeper, or a craft has no capital or route to it (§2).
- **A household** has one or two core livelihoods and at most one secondary trade:
  - Most working members are broad in its core.
  - About a third are capable.
  - One or two are experts, in different specialisms where there are two.
  - Depth follows age: youths are broad and rough, prime adults are the experts, elders hold the deepest lines but a fading hand.
  - Seeded lines follow band and age: an expert about 16 to 19 lines (about 650 to 750 words), a broad adult about 11, a youth
    about 6, a child at most 2 (§3).
- **Between households:**
  - Neighbours in a village are aware of each other's broad crafts and rough at one, and hold one line for each other livelihood.
  - A spouse who married in brings their natal household's broad band and up to three of its lines.
  - A village holds two to five livelihoods with at least one chokepoint inside it and one dependence outside it (§4).
- **Pin and fill** (§5): a world can hand-write any part, and the generator fills the rest in a fixed order with keyed seeds, so
  pinning one household does not reshuffle the others. Today's `FARMING` for every household, `TRADES` round-robin and "every adult
  knows every line craft" become this.
- **Worked examples** (§6): the runs world's three Eelmouth households, a farming-and-tanning house, a fishing-and-trading house,
  the river run's smiths (and the Brooks' salt without a pan), and a five-household village.
- **Knobs** (§7): seeded depth (full, half, base only, none); expertise spread; whether experts differ; how often marriages carry
  knowledge; neighbour awareness; the capital-knowledge coupling itself.

## 0. What the code does now, and what changes

| Now | Where | Becomes |
|---|---|---|
| Every generated household gets `FARMING` (sow, reap, hoe, weed, milk, select seed); a heavy-soil or first household also gets the plough | `landgen/write.py` 28, 384 | livelihoods drawn by fit and the village mix (§5); farming only where there are fields to hold |
| Trades by place: smith near a seam, mason by rock or hills, carpenter by managed wood, miller at a mill site, trapper near forest; dealt round-robin to households | `write.py` 29, 374 to 389 | the livelihood rows' `fits`; quotas for village and region; no fisher, salter, herder or fowler trade exists today |
| Capital by trade: a smith gets a forge (hearth, anvil, 4 charcoal); a miller the mill (millstones, water wheel, bins); the first household the byre, the plough and a bull | `write.py` 405 to 420 | the livelihood's `capital` row, both ways (§2) |
| Every adult of a line knows every line craft at `known`, skill by age (basic 1.0 to 1.5, trade 0.8 to 1.8); youths `rough` or `capable` by age; children nothing | `generate.py` 352 to 364 | bands and specialisms by member, level and skill by the craft's difficulty class (§3) |
| A spouse's natal line's crafts carried (`line_born`) | `generate.py` 355 | kept, and widened to lines and a chance of a specialism (§4.2) |
| Every other line's crafts `aware_of` "you have seen the {line}s at it all your life" | `generate.py` 366 to 368 | the neighbour rule: aware of the broad band, rough in one craft by exposure, one line (§4.1) |
| `trade` = the labels of the first two crafts: "By trade: sowing a field broadcast and reaping a crop" for everyone | `generate.py` 378 | the livelihood and specialism: "By trade: a fisher, best at the weir and its nets" |
| Strong models to the adults who know the most crafts (`opus_extra`) | `generate.py` 383 to 387 | to the holders of the chokepoints and the heads (scenario_design: Opus at every pole of leverage) |
| One lore row (sowing) to field holders | `lore.py` | line templates per livelihood, specialism and capital, with conditions (D2-268: hand-written, tested, filled from state) |
| World makers override knows uniformly per arm (runs world: low rough 0.6, medium known 1.0, high known 1.6 for every adult) | `make_nutrition_runs.py` 48 to 102 | the depth and spread knobs (§7) |
| Gate probe: each gather or work craft tried once by the best-suited person; economy checks for food, heat, runway, burden | `gates.py`, `economy.py` | plus a static capital-knowledge check before the dry run (§2.3) |

## 1. Livelihoods as data

### 1.1 The shape

```yaml
fisher:
  status: built            # built | network (W-73) | later
  fits: {covers: [water], best: "a river with runs", near: []}
  broad: [fish by hand, angle, fishing rod, trap in water, dry fish]          # most of the household; simple at known, practised at rough
  capable: [salt fish, smoke fish, tend the smoke, wicker trap*, creel*]      # about a third, at capable
  specialisms:
    weir_and_nets: {crafts: [weir, fish net*, twist cord*], capital: [weir], lines: [F9, W-gap, N1]}
    traps_and_runs: {crafts: [trap in water, wicker trap*, cut withies*], lines: [F1, F2, F3, F4, F5]}
    hand_rod_dressing: {crafts: [fish by hand, angle, fishing rod, dress the catch*], lines: [F7, F8, D1]}
    keeping: {crafts: [smoke fish, tend the smoke, smoke racks, salt fish, dry fish], capital: [smokehouse], lines: [F6, F10, K1]}
  lines: {broad: [F1, F4, F6], capable: [F5, F7]}     # the practice set (founders_knowledge §2.3) split by band
  capital: {likely: [wicker traps x6, smoke racks], sometimes: [weir, smokehouse, withy bed*, creel*]}
  depends: {needs: [salt, withies, cord], gives: [fish, dried fish]}
  neighbour_line: N-fisher
```

Rules:
- A craft sits in one band of a livelihood, but may sit in several livelihoods (salting is the salter's core and the fisher's
  capable band).
- A specialism may repeat a broad craft at expert depth (the hand-and-rod expert is `known` at a high skill in what the broad
  band does roughly).
- Skilled-class crafts (smelting, smithing, tanning) appear only in specialisms.
- The row lives in one feature unit with its lines and capital (D2-244 seams): `engine/livelihoods.py` beside the data, or rows in
  `data.py` as LIVELIHOODS with the line templates in `lore.py`.

### 1.2 The livelihoods

★ = a network good or craft (hunt_fish_materials.md, W-73, not built); † = later (not in the network either). Difficulty class from
trying_and_learning.md: s simple, p practised, k skilled.

| Livelihood | Broad (most) | Capable (about a third) | Specialisms (one or two experts, different) | Capital it implies (likely / sometimes) | Fits | Status |
|---|---|---|---|---|---|---|
| **Farmer** (arable) | sow, hoe, weed, reap, manure, dung, clear, burn the stubble, pest work, guard the field, bins (s) | plough (p), select seed, dry fodder, bread at a hearth | **ploughman and oxen** (plough, harness, ditch or terrace); **seed and harvest** (select seed, the calendar's lines, granary); **hedge and field** (fence, gates, clappers, pest work) | fields held, a granary floor, bins / an ox pair and plough, a byre | fields by soil | built |
| **Herder or dairy** | herd, milk (s), fence, gates, hay, dung, stalls | slaughter (s), dry fodder, a hurdle★ | **dairy** (milk, cheese (p), cellar); **stock and breeding** (herd, slaughter, the bull and oxen, murrain); **hay and winter** (hay, dry fodder, the count) | a herd, pasture and meadow held, a byre / a cellar, hay in store | pasture, meadow, fen | built (cheese built) |
| **Fisher** | fish by hand, angle, fishing rod, set wicker traps (s, p), dry fish | salt fish, smoke fish, tend the smoke, a wicker trap★ (p), a creel★ | **weir and nets** (weir (p, a crew's), fish net★ (p), twist cord★); **traps and the runs** (set traps, wicker traps★, cut withies★); **hand, rod and dressing** (edge, line, rod, bone hooks★, gutting and dressing the catch★); **keeping** (smoke racks, the smokehouse, salt and dry) | traps (about 6), smoke racks / a weir, a smokehouse, a withy bed★ | water; best a river with runs | built, gear ★ |
| **Hunter and trapper** | hunt the wild, snare (s), dry meat, a crude weapon, a camp, a pack | stalk (p), den work, salt meat, a tent, a bedroll | **stalking and drives** (stalk, drive, a horn); **snares and small game** (snare, making snares★, den work); **dressing the kill** (dress★, hide, tallow, bone; tallow lights) | a weapon, snares, a camp at a far wood / a tent, hides in store | wood, scrub, heath, the wild | built, dressing ★ |
| **Fowler** | net, the fowling method★ (p), snare, gather young and eggs | a fowling net★ (p), dry meat | **nets and decoys** (fowling net★, decoy†); **the freeze and the flight** (fowling in frost, dusk and dawn) | a fowling net★ | fen, flooded meadow, open water | built as `net`; ★ |
| **Salter** | boil salt (s), salt meat, salt fish, firewood, cut | mend the brine pan, salt pans on the saltmarsh | **the pan** (boil, mend, build the pan with the smith's copper); **salting for keeping** (salt meat, fish, cheese's salt); **carrying salt** (the trader's lines, §1.3) | a brine pan in a salt house at a spring / saltmarsh pans held | a brine spring or saltmarsh | built |
| **Smith and miner** | charcoal (p), fetching ore, firewood | mine (on rock, with a tool), copper tool (k) at rough | **smelting and tools** (smelt (k), copper tool, coin, the anvil); **mining and charcoal** (mine, charcoal, where the ore lies); **fittings** (the brine pan, the plough share, copper hooks★) | a forge (hearth, anvil and bellows), charcoal / a claim on the ore | rock with ore within a day | built |
| **Miller and baker** | grind (s), bread at a hearth, bins | mill at millstones, oven bread (p), dress millstones | **the mill** (water mill, clear the leat, dress the stones, the wheel's gap); **the oven** (oven bread, reline, the batch) | a mill (millstones, a water wheel and leat) / an oven, a hand mill | a mill site; grain within a day | built |
| **Carpenter** | fell, small room, beds, bins, repair, woodshed, stalls | medium room, granary, handcart, smoke racks | **houses and halls** (medium room, hall); **wheels and frames** (water wheel, plough frame, handcart) | timber in store, a managed wood / a woodshed | managed wood | built |
| **Mason** | quarry (with a tool), clear for building | wall, hearth, cellar | **hearths and ovens** (hearth, oven, cellar); **stones and walls** (millstones, wall, footing, vault, standing stone) | stone in store / a quarry claim | rock within a day | built |
| **Charcoal burner** (woodsman) | fell, cut, firewood | charcoal (p), a camp | **charcoal** (the burn); **coppice**† (the wood's young growth managed) | a managed wood's claim | managed wood | built |
| **Basket maker** (withies) | cut withies★ (s), hurdles★ (p) | wicker traps★, creels★, pack baskets★ | **traps and creels**; **the withy bed** (plant, fence, cut) | a withy bed★ | wet ground with willow | ★ |
| **Cord and nets** (with flax) | twist cord★ (s) | sow and pull flax★, ret flax★ | **flax and linen** (ret, dress and spin★, the retting pit★); **nets** (fish and fowling nets★) | a flax close★ / a retting pit★ | a close of good soil; still water or a pit | ★ |
| **Tanner** | dress hides (from the kill or slaughter) | harness, a pack, a bedroll from leather† | **the pits** (tanning† (k): hides, oak bark, water, months) | tan pits† by water, bark from an oak wood | water, oak wood, hides from herders or hunters | †: not in W-73 either (its §10 leaves tanning for "a tanning step after this") |
| **Trader or carrier** | carry, travel, offers | a handcart, a pack ox | **the road** (ways, loads, nights out, beasts); **the market** (who makes what, who lacks what) | a handcart or pack ox, coin, a pack | a road with a track; villages a day or two apart | built (carrying), knowledge only |

### 1.3 Lines by specialism (the fisher in full; the rest by pattern)

The founders' fisher set (founders_knowledge §2.3, F1 to F10) split by band and specialism, with the new lines it needs:

| Band or specialism | Lines | New line (about 40 words) |
|---|---|---|
| broad (everyone in a fisher house) | F1 the eels, F4 a trap's scale, F6 keeping in brief | |
| capable | + F5 spate and otters, F7 the shallows | |
| **weir and nets** | F9 the weir's share and its gap; W1 the weir's upkeep; N1 nets | W1: "A wattle weir wants about six bundles of withies a section each year, and a spate wears it twice as fast; a timber one lasts longer and costs ten timber a section." (WATER_WORKS weir material, wear by flow) |
| **traps and the runs** | F1 to F5 in full, with F2 and F3 where the river has them | |
| **hand, rod and dressing** | F7, F8, D1 | D1: "A fish gutted and split the day it is caught dries in the rack; one left whole goes soft. The guts bait the traps." (★ dressing; offal as bait, L-145; write only once built) |
| **keeping** | F6 in full, F10 salt's source, K1 the smokehouse | K1: "The smokehouse takes forty at a time for three nights; tend its fire once a day or it dies, and a wattle smokehouse can catch and burn." (`smokehouse` fire, tend) |

The other livelihoods follow the same pattern: founders_knowledge §2.3's practice lines tagged to one specialism each (the
farmer's A1 and A4 to seed and harvest, A7 to the ploughman, A6 to hedge and field), with each holding's lines (§2.2) going to its
keeper's specialism. The trader's lines are about roads and needs, never prices: "{Highpool} boils salt and lacks grain; {Middleham}
has grain after harvest and no salt"; "A pack ox carries six loads where one on foot carries one, but wants grazing on the way"
(`pack_ox.carry` 60 against the foot's 10; `graze`).

## 2. Capital and knowledge, both ways

### 2.1 What each holding asks of the household

| Holding | Built? | Working craft, band its keeper needs | Mending or upkeep craft | Lines it seeds to its keeper (and a short form to the household) | The fault it guards against |
|---|---|---|---|---|---|
| **A water mill** (millstones, water wheel and leat) | built | water mill, mill: the miller's **mill** specialism | clear the leat (yearly), dress millstones (2,000 grain) | M-mill: "Our mill grinds up to {batch} grain at a turn; the leat silts and wants clearing once a year, the stones dressing after about two thousand grain. The farm houses bring their grain after harvest." M-gap: "Shut, the hatches hold the river and the wheel turns full; drawn, they let the fish by and it turns slow." | river run: the Fletchers held Middleham Mill and never milled (its 200-grain minimum against at most 40 in their store) |
| **An ox mill** (millstones) | built | mill: capable, and an ox | dress millstones | "The stones turn with an ox: {batch} grain at a time." | |
| **A hand mill** | built | grind: broad | | (none: broad knowledge) | |
| **An oven** | built | oven bread: the **oven** specialism | reline after 10 bakings | "The oven bakes a hundred loaves from a hundred flour and four timber, and wants relining after about ten bakings; bread keeps less well than flour." | |
| **A weir** | built | weir: **weir and nets**; its crew capable | the sections' wear by flow; withies or timber | F9, W1 | runs world low and medium: no weir; high: the weir fed the village |
| **Wicker traps** (gear) | built as sets; ★ as gear | set traps: broad | ★ mend at the throat; a spate wrecks | F4, F5 | |
| **A smokehouse** (smoke racks) | built | smoke fish or meat, tend the smoke: **keeping** | the fire tended; fire risk | K1 | the lake run: known by all, used by none |
| **A salt house and brine pan** | built | boil salt: **the pan** | mend after 60 boilings; copper from the smith | S1 to S3 (founders_knowledge) | river run: the Brooks had the craft and the spring but no pan until day 3 |
| **Saltmarsh pans** (a cover held) | built | salt pan: broad salter | | "The pans on the marsh make salt in the sun; in winter they give little." (once the season is in the yield) | |
| **A forge** (hearth, anvil and bellows) | built | smelt, copper tool: **smelting and tools** | charcoal in store; stone and hide for the anvil | M1 to M4 | river run: smiths with no rock in reach |
| **A cellar** | built | cheese: **dairy** | | H1 | |
| **A granary floor** | built | broad | | C3 (holds 300 grain) | |
| **A herd** (cows, oxen, a bull) | built | herd, milk: broad herder; slaughter: capable | hay for winter; the bull's breeding | H2 to H5 | pw1: "Slaughter ... took our last cow, not the bull" |
| **A plough and harness, an ox pair** | built | plough: **ploughman** | the plough's copper share from the smith | A7 | |
| **Fields held** (and their state: crop, fallow, last crop) | built | sow, reap: broad farmer | manure, rest | A1 to A5, read from the fields' own state ("the Long Field is in beans; next year it bears barley well") | |
| **Pasture and meadow held** | built | herd, hay | fence, gates | H2, H4 | |
| **A managed wood held** | built | fell, cut, charcoal | | "Young growth in {wood} cut comes again; the dead wood once gathered is gone." | |
| **A withy bed** | ★ | cut withies, plant: **the withy bed** | a fence against beasts | "The bed bears from its third year for thirty, if beasts are kept off it; cut in winter." | |
| **A flax close, a retting pit** | ★ | sow, pull, ret, dress and spin: **flax and linen** | | "Retted in the river, flax fouls the water three nights for the fishers below; the pit does not." | the fishers' conflict (W-73 §8.2) |
| **Tan pits** | † | tanning (k): **the pits** | bark, water | (written when built) | |
| **A handcart, a pack ox** | built | carry: the trader | a road with a track; grazing | the trader's road lines | |
| **A boat** | † | (with the seine) | | | |
| **Stores** (stock in a house) | built | | | B5's household figure read from the store at the start ("the store holds about twelve nights for six of us") | |

### 2.2 Both ways in the generator

- **A pinned or drawn livelihood fills its capital.**
  - The `likely` capital is placed if the land allows it (a mill only at a mill site, a weir only on a water parcel, a brine pan
    only at a spring).
  - Each `sometimes` item is placed by a keyed draw (knob: `capital_share`).
  - What the land refuses is reported, not forced (the fisher on a lake gets no weir).
- **Pinned capital fills its keeper.** A household given a mill gets the miller's livelihood, as core or secondary, if it has none
  that works it. At least one member becomes its keeper: the expert in the specialism that works it, or capable if the household
  is small. Its lines are seeded.
- **A holding held outside the household's livelihoods** (a farmer's hand mill) needs only the broad craft and seeds nothing more.
- **Holdings are lines, not lists.** Each holding's lines are rendered from its state at the start: its batch, its wear so far, its
  stock ("the stones were dressed last winter" if its wear is low). So the mill in the store and the mill in the memory are the
  same mill.

### 2.3 The gate check, extended

A static check before the dry run (`gates.py` stays the dry probe; this reads the spec). Refuse means the world is not run as is;
warn means it is reported in the world's report.

| Check | Level | The river run would have failed it |
|---|---|---|
| A holding whose working craft no member of its household knows at capable or above | refuse | |
| A holding whose batch is more than any store in reach can hold or gather before its season ends | refuse (until W-75's "up to" batches; then a warning) | the water mill: 200 grain in one act, at most 178 in any store, 40 in the Fletchers' |
| A holding whose mending craft nobody in reach knows (a pan and no smith in the region, a mill and no mason) | warn | |
| A craft known at capable or above with no capital it needs within a day and no route to build it (materials and a builder in reach) | refuse for a core livelihood, warn for a secondary | the Brooks' boil salt with no pan (raised on day 3 by intervention); the Brooks' mining and the Marshes' quarrying with no rock in their villages (rock one or two days off) |
| A livelihood whose `fits` fail where its household lives | refuse | "By trade: sowing" in a world with no fields (02zzy) |
| A seeded line whose condition is false here (salmon lines on a river without salmon; a mill line without a mill) | refuse (the template is skipped) | |
| A chokepoint craft (smith, salter, miller) held nowhere in a region whose other livelihoods depend on it | warn (a designed scarcity is allowed) | |
| An expert specialism with no capital and no means to make it in reach | warn | |
| Two experts of one household in the same specialism when the knob says they differ | warn | |

## 3. A household

### 3.1 Livelihoods

- **Core:** one or two livelihoods. Two only where both fit the land and do not crowd each other's working days, e.g. the river
  run's Brooks as smiths and salters.
- **Secondary trade:** at most one. Its broad band goes to some members, its capable band to one, no expert.
- **Mixes that make sense** in one house: farmer with herder (the common case); farmer with miller or baker; farmer with tanner;
  fisher with salter, basket maker or trader; hunter with tanner or charcoal burner; herder with cord-and-flax; smith with charcoal
  burner or salter; fowler with fisher.
- **Mixes that do not:** two livelihoods each needing a chokepoint the house holds alone (miller and smith); two that want the same
  season's whole days (fisher in the autumn run and hunter in autumn's fat deer, unless the house is large).

### 3.2 Who knows what, by band and age

For a household's working members (youth and older):

| Role | Share | Core crafts | Specialism | Skill (by class: simple / practised / skilled) |
|---|---|---|---|---|
| **Expert** | 1 if the household has 2 to 4 working members, 2 if 5 or more; never more than 1 per specialism unless the knob says so | broad and capable at known | one specialism at known, its skilled crafts too | top half of the class's range (simple 1.1 to 1.3, practised 1.2 to 1.6, skilled 1.3 to 2.0) |
| **Capable** | about a third of the rest | broad at known, capable band at capable | one specialism's crafts at rough (the one they help the expert with) | middle of the range |
| **Broad** | the rest | broad band: simple at known, practised at rough | none | low end of the range |
| **Secondary trade** | 1 to 2 members | that trade's broad band; one at capable | none | |

Depth by age (the engine's stages, LIFE spans):

| Stage | Bands open to it | Level and skill | Notes |
|---|---|---|---|
| Child | none | none | at most two lines, as if passed on by a carer (founders_knowledge B8's default); children born in the run have only what is passed |
| Youth | broad; capable at the older end | rough, capable from about 15 years (as `generate.py` now) | may be **apprenticed**: rough in the expert's specialism and named as learning it (the youth's existing aim "learn {craft} as the {line}s do it" turns on the household's own expert) |
| Young adult | broad, capable | known in broad, capable in capable | an expert only if no older member can be |
| Prime adult | any; experts drawn here first | | |
| Elder | any; the deepest lines | knowledge at its peak, skill faded toward its floor (D4-105: never below 60% of its best gain) | holds the history and season lines (the hard winter, the year the run failed); a natural teacher |

The draw within a household: rank the working members by age within the prime span, give the first the specialism that works the
household's most valuable holding, and give the second a different specialism (by the livelihood's order, or the second holding).
Then draw the capable share among the rest, preferring the experts' spouses and oldest children. Each draw is keyed (§5.3).

### 3.3 The seeded lines each member gets

| Role | Base set (B1 to B8) | Core practice lines | Specialism | Holdings' lines | Secondary trade | Neighbours | Lines (words) |
|---|---|---|---|---|---|---|---|
| Expert, prime | 8 | broad 3 and capable 2 | 4 to 6 of their own | 1 to 3 for what they keep | 0 to 2 | 1 each, 2 to 3 | 16 to 19 (about 650 to 750) |
| Expert, elder | 8 | 5 | 5 to 6 | 1 to 3 | 0 to 2 | 2 to 3, plus one history line | 17 to 20 |
| Capable adult | 8 | 5 | 1 to 2 (the one they help with) | 0 to 1 | 0 to 2 | 2 to 3 | 13 to 15 (about 550) |
| Broad adult | 8 | 3 | 0 | the household's short form, 0 to 1 | 0 to 1 | 1 to 2 | 11 to 13 (about 450) |
| Youth | 5 (B1, B2, B3, B5, B8) | 2 | 1 if apprenticed | 0 | 0 | 0 to 1 | 6 to 9 |
| Child | 0 | 0 | 0 | 0 | 0 | 0 | 0 to 2 |

Against the kept places: seeded lines are ordinary kept lines (D2-268) and do not use the places that open each stretch (D2-266).
A person may drop one to free its place, and lines may grow or die. An expert's 750 words is about what the river run's Fable
agents held in their rewritten memory (498 words a stretch, crafts_evaluation Part 5), so it sits at the top of what a strong model
carries well; Haiku members (the bulk, scenario_design) are mostly broad and get the short sets.

## 4. Between households

### 4.1 Neighbours

| Who | Knows of another household's livelihood | Source |
|---|---|---|
| Same village | aware of every craft in its broad band; **rough in one** that their own household uses the product of (a farmer of the miller's grinding, a fisher of the salter's salting), by a keyed draw | today's `aware_of` "seen at it all your life", narrowed to the broad band |
| Same village | one neighbour line per livelihood: what they do, what they have to spare, and when ("in late autumn they have fish to spare") | the livelihood's `neighbour_line`, read from the household and its capital |
| A village within a day | the chokepoint crafts only (smith, salter, miller, a weir): aware, and one line naming the household and place ("the Brooks boil salt at Highpool") | the place lines' "its people know ..." today, replaced by who and what |
| Further | nothing seeded | exploring finds it |

### 4.2 Marriages and others from outside

- **A spouse who married in** brings their natal household's broad band at the level they had when they left, as `line_born` does
  today. They also bring up to three of its lines, in their own voice ("At home at Highpool we boiled salt from the spring; four
  firewood to four salt").
- **Taken in, fostered, or a widow come back:** the same, from the household they grew up in.
- **A specialism from home:** with a small chance (knob `marriage_expert`, default 0.15), the spouse was capable in a specialism of
  their natal livelihood. This is livelihood_archetypes.md's sixth question: "certain individuals might know specific skills, e.g.
  especially if they came from another household".
- **The family tree decides who married in** (`generate.simulate` already records `line_born`). The knob `marriage_carry` (default
  1.0, 0 for the arm without it) sets whether the knowledge comes with them.

### 4.3 The village and the region

| Rule | Default | Why |
|---|---|---|
| Livelihoods a village holds | 2 to 5, no more than one household in four of a chokepoint livelihood | specialisation and dependence (scenario_design: leverage and dependence) |
| A chokepoint inside the village | at least one (the mill, the weir, the salt house, the forge), held by one household | leverage inside; a pole for an Opus |
| A dependence outside the village | at least one need met only from another village (salt, copper, stone) | the existing `dependence` design check (stone, metal) widened to every livelihood's `needs` |
| Region quotas | a smith within two days of every plough; a salter within two days of every fisher and herder (cheese) | the needs table; a world may pin scarcity |
| Shared flows that set households against each other | where they arise from the land, kept: the weir above the mill, retting above the fishers, two herds on one common | W-73 §8.3 |
| Cast | the experts of the chokepoints and the heads Opus; capable adults Sonnet; broad members and youths Haiku | scenario_design §1; replaces "who knows the most crafts" |

Mixes that work:
- **A river village:** fisher, farmer, salter or a salt road, and a basket maker.
- **A vale village:** farmer, herder, miller, and a smith a day off.
- **An upland village:** herder, hunter, charcoal burner and smith, with grain from below.
- **A fen edge:** fowler, fisher, cord and flax, and herder.

## 5. The generator's interface: write it, generate it, or pin and fill

### 5.1 What a world file may say

```yaml
skills:
  depth: full                  # full | half | base | none (§7)
  spread: {experts: [1, 2], capable_share: 0.33, experts_differ: true}
  marriage_carry: 1.0
  marriage_expert: 0.15
  neighbours: rough_one        # none | aware | rough_one
  capital_share: 0.5           # the chance each "sometimes" holding is placed
  village_mix: {fisher: 0.4, farmer: 1.0, salter: 0.2, miller: 0.3}   # draw weights among livelihoods that fit
  region: {smith: 1, salter: 1}
households:                    # any household may be pinned in part or in full
  Wright:
    livelihoods: [fisher]
    trade: trader
    experts: [weir_and_nets, keeping]
    capital: {weir: {parcel: Lowstrand_7, position: first}}
  Fletcher:
    capital: {water mill: {}}  # the livelihood (miller) and its keeper are filled
  Field: {}                    # everything filled
agents:                        # a person may be pinned too
  Aldric: {expert: weir_and_nets}
  Lucy: {band: capable, born_line: Marsh}
```

A fully hand-written world lists every agent's `knows` and `kept` as now. The generator then fills nothing and only runs the
gate check.

### 5.2 The fill order

| Step | Fills | From | Code |
|---|---|---|---|
| 1 | land, villages, sites, covers | the configuration | `landgen` as now |
| 2 | pinned households' livelihoods and capital | the world file | new |
| 3 | unpinned households' livelihoods | `village_mix` weights over the rows whose `fits` hold; region quotas first | replaces `FARMING` and the `TRADES` round-robin |
| 4 | capital from livelihoods, and livelihoods from pinned capital | §2.2 | replaces capital by trade (`write.py` 405 to 420) |
| 5 | the family tree, households' members, marriages (`line_born`) | `generate.simulate` with the lines now carrying livelihoods | as now |
| 6 | each member's band, specialism, level and skill | §3.2, keyed per household | replaces `generate.py` 352 to 364 |
| 7 | what spouses and fosterlings carry | §4.2 | widens `line_born` |
| 8 | neighbours' awareness and lines | §4.1 | replaces the `aware_of` loop |
| 9 | the seeded lines, rendered from templates against the state | §3.3; D2-268 (hand-written, tested) | `lore.py` widened; `MEM.seed_line` with source "family lore" |
| 10 | the gate check | §2.3 | new static check beside `gates.py` and `economy.py` |
| 11 | the cast, the trade line, aims | §4.3 | `generate.py` 378 to 400 |

### 5.3 Repeatability

- Every draw is keyed by what it is about, as `landgen/keyed.py` already does: `keyed.rng(seed, "skills", household)`,
  `(seed, "expert", household, k)`, `(seed, "neighbour", person, livelihood)`.
- Pinning one household or one person leaves every other draw as it was, so a pinned arm and its unpinned twin differ only where
  pinned.
- The depth knob changes only step 9 and the levels in step 6. A depth arm and its full twin have the same people, holdings and
  bands.

## 6. Worked examples

### 6.1 The runs world: Eelmouth, three households on a big river with a brine spring (W-69)

**Now** (`runs_high.yaml`):
- All six adults know the same seven crafts at the same skill (boil salt, net, salt fish, smoke fish, tend the smoke, trap in
  water, weir; 1.6 in high).
- All are "By trade: sowing a field broadcast and reaping a crop", in a world with no fields.
- Each household has a smokehouse; the Marshes hold the weir; a salt house at the spring.
- Hamon, a master smoker, wrote the river off as "fished out" on day 1 (02zzy).

**Proposed:**

| Household | Livelihoods | Holdings (filled from the livelihood, or pinned) | Members (role, specialism) | Seeded lines |
|---|---|---|---|---|
| **Marsh** | fisher | the weir (pinned, high arm); wicker traps; smoke racks at the hearth | Peter, expert: **weir and nets**, keeper of the weir; Nichola, expert: **traps and the runs**; Nigel (youth), broad, apprenticed to the weir | Peter 18 (F9, W1, the weir's gap and wear from its state); Nichola 17 (F1 to F5 in full); Nigel 7 |
| **Shepherd** | fisher; secondary fowler (Eelmouth Fen) | the smokehouse; traps; a fowling net★ when built | Hamon, expert: **keeping** (the smokehouse's keeper); Gunnild, expert: **hand, rod and dressing**; both broad in fowling | Hamon 17 (F6, K1, F10); Gunnild 16 (F7, F8) |
| **Brook** | salter; secondary fisher | the salt house and its brine pan (the salter's `likely` capital, placed because the spring is there); salt in store | Oliver, expert: **the pan**, its keeper; Katherine, capable fisher (traps, F1 and F4); Petronel (youth), broad salter | Oliver 17 (S1 to S4, the pan's wear); Katherine 14; Petronel 6 |

- **Gate check:** the weir has a capable keeper and crew (Peter, Nichola); the smokehouse has Hamon; the pan has Oliver. No fields,
  so no farmer and no sowing lore. All pass. Today's world fails "a livelihood whose fits fail": everyone is a sower with no
  fields.
- **Dependence:**
  - The Marshes take the run at the weir; the Brooks have the salt.
  - The Shepherds have the smokehouse and the fen's fowl in winter.
  - Each lacks what another holds, where today each house holds everything.
- **Arms:** the old low, medium and high become depth (none, half, full) on the same people and holdings, plus the weir pinned in or
  out (§7).

### 6.2 A farming-and-tanning household

- **The Tanners of a vale village:** core farmer; secondary tanner (†, a skilled craft: hides, oak bark, water, a season in the
  pits).
- **Holdings:**
  - fields (two plots) and a granary floor;
  - tan pits† on a water parcel by the oak wood (pinned or drawn with the secondary);
  - hides in store from their own slaughter and bought from the hunters.
- **Members:**
  - the elder, expert in **the pits** (skill faded, knowledge deepest; the indenture of 1424 is ten years: trying_and_learning
    §1);
  - a prime adult capable in tanning (his apprentice of long standing);
  - the rest broad farmers; one capable in the plough.
- **Lines:**
  - The elder: B1 to B8, the farmer's broad 3, the pits' 5 (written once tanning is built: the bark, the season in the pits,
    "the hides from the hunters come in autumn"), and a history line.
  - The farmers: the farmer's set plus one tanning line ("Father's pits want bark stripped in spring, when the sap rises").
- **Gate:**
  - The pits need water and an oak wood in reach, and hides from a herder or hunter within a day (the `needs`). A tanner with no
    hides in reach warns.
  - Until tanning is built the secondary cannot be drawn; the row has `status: later`.

### 6.3 A fishing-and-trading household

- **The Wrights of Lowstrand:** core fisher; secondary trader.
- **Holdings:**
  - wicker traps (6), smoke racks at the hearth, a creel★;
  - a handcart (the trader's `likely`, placed because the Lowstrand to Middleham road has a track);
  - a pack.
- **Members:**
  - Aldric, expert: **traps and the runs**.
  - Lucy, expert: **keeping**. In the river run she found "fresh meat rots in the hand ... dry or salt every scrap the same day"
    on day 25; seeded, she starts with it.
  - Matthew, capable fisher and the house's carrier: the trader's road lines, "Middleham has grain after harvest and no salt;
    Highpool boils salt and lacks grain", and one line on the handcart's road.
  - Wilmot and Payn, broad.
- **Gate:** the handcart needs a road with a track from its home (pass). The keeping expert needs salt or racks in reach (the
  racks pass).

### 6.4 A smith: the river run's Brooks of Highpool

**Now:**
- Every Brook adult knows mining, smelting, copper tools and coin at known (skill 1.25).
- Brook's Forge holds a hearth, anvil and 4 charcoal.
- Highpool has no rock; the ore is at Scarlow, a day off and unexplored.
- The household also held the salter's craft and the brine spring, but no pan until day 3.

**Proposed:**
- **Livelihoods:** core smith and salter. Two chokepoints in one house is allowed here because they share the forge's copper (the
  pan is copper), but the village rule (§4.3) warns.
- **Holdings:**
  - the forge (hearth, anvil and bellows);
  - charcoal;
  - **the brine pan**, filled by step 4 because the salter's `likely` capital at a spring is a pan;
  - a claim on Scarlow's seam, known to the miner (D2-187).
- **Members:**
  - Lambert, expert: **smelting and tools** (M1 to M4, the forge's upkeep: "the anvil wants charcoal by the load, and the forge
    goes cold without it").
  - Peter, expert: **mining and charcoal** ("the ore lies at Scarlow, a day off by the hill road; three ore and a charcoal smelt
    one copper").
  - Mabel, expert: **the pan** (S1 to S3).
  - Saer and Matilda, broad in both (in the run Matilda was taught boil salt on day 23).
- **Gate:**
  - With the pan placed, salt passes.
  - Mining passes: Scarlow's rock is within a day and Peter knows the way.
  - The quarrying the Marshes were given with no rock in Highpool warns (rock is at Stanwood, a day off; route only).

### 6.5 A mixed village of five households: Wenford, on a big river, clay fields, a mill site

The salt spring is at Saltwell, a day downstream; the copper smith is at Highpool, a day up the hill road.

| Household | Livelihoods | Holdings | Experts (specialism) | Capable / broad | Cast | What neighbours know of it |
|---|---|---|---|---|---|---|
| **Field** | farmer; secondary herder | 4 field plots, the granary floor, an ox pair, the plough and harness, the byre, 2 cows | Osric (ploughman and oxen); Orabel (seed and harvest) | Baldwin capable in the herd; Drew, Hawise broad; Hob youth, apprenticed to the plough | Osric Opus (head, the largest land) | "The Fields hold the big fields and the plough team; after harvest they have grain, and at reaping they want hands." |
| **Fletcher** | miller and baker; secondary farmer | the water mill (millstones, wheel and leat) at the mill site, a bake oven, a field plot | Hamo (the mill: leat, stones, the hatches); Annora (the oven) | Alard capable miller; Piers broad | Hamo Opus (chokepoint) | "The Fletchers keep the mill; bring them grain after harvest." |
| **Wright** | fisher; secondary basket maker★ | the weir (upstream of the mill), the smokehouse, wicker traps, a withy bed★ on the fen | Aldric (weir and nets); Lucy (keeping) | Matthew capable (traps and the runs); Wilmot broad, cuts withies | Aldric Opus (chokepoint) | "The Wrights work the weir; in late autumn they have fish to spare." |
| **Hunt** | hunter-trapper; secondary charcoal burner | a camp at the far wood, snares, the managed wood's claim | Clement (stalking and drives); Odo (dressing the kill★) | Idonea capable (snares) | Clement Sonnet; Opus not needed (no chokepoint) | "The Hunts go to the woods in autumn and trade hides and meat; they burn charcoal for the smith." |
| **Shepherd** | herder or dairy; secondary cord and flax★ | the common's herd (4 cows, a bull), a cellar, a flax close★ by the backwater | Fulk (stock and breeding); Sabina (dairy) | Margery capable (flax); Rose, Tobin broad | Sabina Sonnet | "The Shepherds keep the cows on the common; they have milk in summer and cheese in winter." |

**The holdings' lines,** filled from state:
- Hamo: M-mill, M-gap, "the leat was last cleared in autumn".
- Aldric: F9, W1, and the weir's position above the mill: "our weir takes the eels before the mill's hatches do".
- Lucy: K1.
- Fulk: H3 and H5. Sabina: H1. Margery: the retting line.

**Dependence and leverage:**
- The mill needs the Fields' grain.
- The Fields need the Fletchers' mill to make grain go further, and the Highpool smith for the plough share.
- The Wrights need salt from Saltwell (a trade route, the Hunts or the Wrights' carrier) and cord from the Shepherds' flax.
- The Shepherds' retting above the weir fouls the Wrights' water unless a pit is dug (W-73 §8.2).
- The mill's hatches and the weir's gap share the salmon (Q-51).
- Chokepoints inside: the mill and the weir. Outside: salt and copper.

**Gate check:**
- Every holding has a keeper.
- The mill's batch passes only with W-75's "up to": if the Fields' granary holds about 150 grain at harvest, the water mill's 200-grain
  minimum refuses it.
- The cellar's cheese needs salt from Saltwell, which is reachable: warn, it is a dependence.
- The flax close needs still water or a pit: the backwater passes.

**Seeded words:** the five households' 21 working members carry about 290 lines (about 12,000 words), against today's system text
of about 5,700 words told to each of them (crafts_evaluation Part 5).

## 7. The experiment knobs

| Knob | Values | What it tests | Pairs with |
|---|---|---|---|
| **Seeded depth** (D2-268: arms with less, "to see how much they can learn") | `full` (§3.3); `half` (base set, broad core lines, the holdings' short forms; no specialism lines); `base` (the base set only; craft levels as the bands); `none` (no seeded lines; crafts at the bands' levels only) | what living and teaching recover of what was not seeded: the sowing windows, the runs, keeping; time to the first run fished well, to the first cheese, to the first false belief | the told-knowledge arm (D2-266): the same lines in everyone's system text |
| **Expertise spread** | experts per core 0, 1, 2; capable share 0.2 to 0.5; skill ranges by class | whether experts make dependence and teaching (17 river lessons, all within households) | |
| **Experts differ** | on (different specialisms) / off (two of the same) | whether a household with two kinds of expert fishes and keeps better than one with two weir-wrights | |
| **Marriage carries** | `marriage_carry` 0 to 1; `marriage_expert` 0 to 0.3 | knowledge crossing households: the river run's Marsh and Brook marriages | |
| **Neighbour awareness** | none, aware, rough_one | whom people ask; whether awareness turns into lessons or trade | |
| **Capital-knowledge coupling** | on / off (holdings placed without keepers, or crafts without holdings, as the river run was) | how much the coupling and the gate check are worth: a fault arm, run once | |
| **Cultural strands** | founders_knowledge Part 3 (passing on, taboos, exploring, sharing crafts) | as there | |

Each arm keeps the same seed, so the people, households, holdings and bands are the same and only the knob differs (§5.3).

## Open questions

1. Expert count: one per two to four working members and two for five or more, or a world parameter only?
2. Two core livelihoods both holding a chokepoint in one house (the Brooks' forge and pan): allow with a warning, or forbid?
3. The apprenticed youth: named as learning the expert's specialism (rough, with an aim), or no different from other youths?
4. The elder's fading: today's floor (D4-105) on skill, with knowledge lines at their fullest, as proposed?
5. Holdings' lines rendered from the start's state (the stones' wear, the leat last cleared): yes, as proposed, at the cost of a
   template per holding?
6. The trader's knowledge: roads and needs only, never prices (founders_knowledge Part 4), as proposed?
7. Tanning: wait for its own step after W-73, or add the tanner's row now with `status: later` so worlds can name it?
8. Where the rows live: `engine/livelihoods.py` as one feature unit with its templates (D2-244 seams), or LIVELIHOODS in `data.py`?

*Current as of 22 Nov 2026.*

## Addendum, 22 Nov: changes to the livelihoods after Zach's review (exploration)

- **Carpenter and mason become one builder livelihood** with two specialisms: the **wright** (timber framing, wheels, the plough
  frame, the handcart) and the **mason** (hearths, ovens, millstones, walls). Neither lived by building alone in a village: work came
  in lumps and they were usually a secondary trade beside farming, or travelled for big jobs (churches, mills, a lord's house).
  Builders are faster (about half the units at master) and build sounder (craftsmanship sets a building's wear and breaks),
  proposals/building_clock.md; the timber economy (W-76) carries them further.
- **The charcoal burner becomes the woodsman:** coppice and poles, withies, firewood and charcoal; a real full-time living only
  where a smith or a salter buys the fuel.
- **A cottager added:** a household with a cottage and a garden and little or no land of its own, living by work for others (paid
  in food or coin: work-for-pay offers exist), a few beasts on the common, gathering and by-crafts (spinning, basketry); a village's
  labour supply, and a test of labour markets.
- **The tanner row is added now** (D2-270), its uses (the pack frame's straps, harness, bellows, shoes) arriving in the same build
  (hunt_fish_materials.md §7.6).
- **Elders teach from their peak skill** (trying_and_learning.md §6), so an elder past their best still teaches what they knew.

