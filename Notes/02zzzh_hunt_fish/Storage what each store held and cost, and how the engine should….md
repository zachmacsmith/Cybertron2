---
id: docs/review/37_growth/02zzzh_hunt_fish/storage.md
kind: note
updated: "2026-11-22"
---
# Storage: what each store held and cost, and how the engine should keep goods

*note · `docs/review/37_growth/02zzzh_hunt_fish/storage.md`*


22 Nov 2026, 37.2 (subagent). This is a research and design note. No code was changed and nothing was committed.

Zach (22 Nov): "Get an agent on digging into each type of storage mechanism, how much it thinks it should actually store, how much
it should cost, consider the new ones you listed, should they require different resources or things (like being underground,
stone, etc.) also wouldn't actual cellars be a lot more expensive? Or no? It feels kinda weird if they can build a cellar much faster
than a fence? Maybe we should make the good options more realistically costly but just cheaper, easier worse options? Like baskets
and barrels etc.? And yes: explore how spilling onto a house's floor could bring vermin?"

He followed up three times during the work:
- "within stores would you not need to build shelves or baskets or barrels or whatever in them to store things?"
- On whether containers would be too much, he agreed that the containers are a fit-out and goods are sorted into them automatically.
- "allowing manual interventions or moving things if they want but not needed? E.g there could be a secure chest with a key where
  only one person can move things in the store into or out of it unless someone else gets the key?"

Sections 5 and 9 answer these.

**Read with:**
- the decisions: [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]] (stores remove outside penalties and never slow a food below its base), [[D2-264 The fishing, hunting and materials network|D2-264]] (weights in kg), [[D2-259 The food values are anchored on real values|D2-259]]
  (real values within 20%), [[D2-45 Cellar and stalls|D2-45]], [[D2-58 Grain spoils a little|D2-58]], [[D2-155 Storage takes space|D2-155]] (the cellar, the grain rates, storage takes space), [[D2-212 Fresh fish keep twice as badly as meat in a store|D2-212]] (fresh fish in a store),
  [[D2-206 The cat comes by itself or is found|D2-206]] (the cat), [[D2-214 Two clocks|D2-214]] (two clocks), [[D4-23 Holding is a recognised claim|D4-23]] (a household's store: members use it, the head manages it);
- the open rows: OPEN [[Q-24 Built for the building package|Q-24]] (6) (a store keeps all of its goods at its best fitting's rate, not by where each good lies; confirmed as
  built, now [[L-131 The wild layer's live points from briefs 1 to 3|L-131]]) and [[L-137 Stores may be too strong against preserving|L-137]], closed by [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]];
- the proposal on targets, `proposals/acts_on_owned_things.md` ([[Q-80 Whether acts on owned things default to one's own|Q-80]]);
- the sibling notes [smokehouse_capacity.md](smokehouse_capacity.md), [fibre_and_cord.md](fibre_and_cord.md) and
  [withies_wood_materials.md](withies_wood_materials.md);
- the code: `cybertron2/engine/data.py` (FITTINGS 234-286, ROOMS and BLUEPRINTS 290-312, STORES 323-331, PHYSICS `house_spoil` and
  `cellar_spoil` 776-777, FENCES 961-971, DECAY 117-131), `engine/buildings.py` (`stores`, `alloc`, `overflow`), `engine/night.py`
  (`decay_rate`, `spoil_rate` 316-352), `engine/wild.py` (`_stores` 2839, `_stops` 2747, `_follow_harvest` 674, `_store_beasts`
  2797, DRY_STORES 24), and `cybertron2/wild/kinds.py` (rats and voles and mice 51 and 69, STORE_STOPS, CAT, OWL, LEFT_OUT,
  EATEN_SIGNS, PRESENCE).

**How the sources were read.** I used web search only. Both page fetches I tried failed because the session's network does not
allow the host (penelope.uchicago.edu and buildingconservation.com), so I stopped fetching. Every figure below comes from search
summaries and abstracts, and I quote each figure as the summary gave it. Anything marked **(est.)** is my own estimate.

**The engine's basis:**
- A unit of work is 2 hours, and a person works about 6 units a day.
- A space is about 5 m² of floor ([[D2-154 One unit of space at every level|D2-154]]).
- A unit of size is about 2 ha (02z).
- A timber is about 240 kg of wood, and a withies bundle is about 10 kg of rods (withies_wood_materials.md).
- A food good weighs about 1 kg a unit ([[D2-264 The fishing, hunting and materials network|D2-264]]).
- A person eats about 1 food a day (PHYSICS `ration`), so a household of 6 eats about 192 food in a 32-day world year: about 275 kg
  of grain boiled, or about 150 kg if baked as bread.
- Slow processes, including keeping and spoiling over months, move about 11.4 real days in each engine night ([[D2-214 Two clocks|D2-214]]; the ecology's
  `SEASON_DAYS_REAL` 91 over 8 nights). So "keeps a season" means it keeps about 3 real months.
- Wheat weighs about 770 kg a m³ in bulk, barley 600 to 620 and oats 410 to 420 [Engineering ToolBox].

---

## 0. In brief

- **The houses are not too big; their keeping is too good.**
  - In wild_region_s7 on day 10, Holt House held 550 grain against bins of 60. The other 490 kg lay legally on its free floor:
    28 spaces at 30 kg a space.
  - 490 kg of grain is about 0.7 m³, or ten sacks. A real house holds that easily.
  - What is wrong is that the engine keeps all of it at the bins' rate, safe from vermin as the bins are ([[Q-24 Built for the building package|Q-24]] (6)). In the code
    (`spoil_rate` and `_stops`), the best fitting multiplies the whole stock.
  - The 763 grain that overflowed outside the doors on day 29 only spoils in the open. The vermin never touch it, because the
    take at the door reads only `LEFT_OUT`, which is meat, fish and milk.
- **Stores should be two layers: a space and the containers in it.**
  - The space (a room's floor, a loft, a granary, a cellar, a clamp, a rick) gives the climate: dry or damp, cool or warm, raised
    or on the ground.
  - The containers (sacks, baskets, bins and chests, barrels, later crocks) give protection against vermin and flies, and order.
  - Goods lying loose on a space are exposed.
  - I recommend the fit-out form (§5):
    - containers are goods made or traded and kept in a store, like the cat;
    - the engine sorts each good into the best container it has room in;
    - the person reads one line;
    - a manual move, and a locked chest with its key, are optional (§9).
- **The capacities should stay real; the compressed year should not shrink them.** For a sense of scale: a real household's year
  of grain (1.5 to 2.5 t) is about 11 world years of its eating, and is a granary's worth. Scaling capacity down by 11 would make a
  sack hold 5 kg. At real capacity, an ark of about 400 kg plus a few sacks holds a large household's harvest. Storage then binds
  on cost, craft and protection, not volume, except after a big harvest in a small house. A granary of several tonnes becomes a
  village's or a lord's store, a chokepoint that scenario_design.md would want.
- **The cellar against the fence.**
  - **Real hours.** A real stone-lined cellar under a 30 m² cottage takes about 40 to 70 days of work (est.): digging about 60 m³
    at 2 to 3.5 m³ a day, about 28 t of stone set by a mason, and a floor over it. A hurdle fence round a 2 ha parcel takes about
    105 days of hurdle-making alone (315 hurdles at 3 a day), plus stakes. A fence round a small close of about 0.2 ha takes about
    35 days.
  - **The engine.** Every building and fence in the engine is about 30 to 70 times cheaper than real hours: a cellar 6 units, a
    fence 10, a wattle room 6. On that one scale, the engine's 6 units for a small house's cellar is about right, and real cellars
    were cheaper than a field's fence.
  - **What is actually wrong with the cellar:**
    - it costs the same under a hall as under a cottage, though it holds by footprint;
    - it has no site rule (wet ground, rock);
    - it keeps everything at a quarter, where it should be cool for the foods heat ruins and damp for grain;
    - vermin pass straight in.
  - **Proposed:** cost by footprint (about 1 unit a space timber-lined, 1.5 stone-lined, with stone 2 a space), a site rule, and
    [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]]'s specific protections.
  - **Flagged for Zach:** the engine's building scale is a named lever of its own, and is set against the real hours of crafts. It
    should be a decision.
- **Make the good options costly and the cheap options worse at something specific.**
  - **Cheap and basic:**
    - loose on the floor: free; damp and every vermin;
    - baskets of withies: roots and dried goods; vermin get in; grain sifts through;
    - sacks of cord: portable; rats gnaw them;
    - a sealed grain pit: dug in a day; must be emptied once opened;
    - a clamp: roots against frost; rats and boar;
    - a rick: hay against rain; fire and mice.
  - **Dear, and needing a craft:**
    - a joined chest or ark: a carpenter and a timber; nearly vermin-proof;
    - a barrel: a cooper; brine, flies, vermin;
    - a granary on staddle stones: a mason's staddles and a carpenter's floor; the best against damp and vermin; can burn, stands
      apart;
    - a cellar: a mason, a dry site, digging; cool but damp, vermin pass;
    - a vault: fire and theft.
- **Vermin take what is exposed, and exposed food draws them.**
  - Each portion of a store (loose, sacked, chested, raised) loses the night's vermin share times its exposure, by kind. Rats and
    mice differ, and the cat and the owl stop mice better than rats (Elton 1953).
  - Grain at the door is taken too.
  - The vermin's food in the ecology becomes the *exposed* store, so a house with grain on its floor feeds and draws more of them.
    In a house of chests it falls away.
  - The signs follow where the loss was: "grain scattered and trodden on the floor, mouse droppings in it", "the sacks gnawed
    through at the bottom", "gnaw marks at a corner of the ark".
- **The rooms and the smokehouses (§11).**
  - A wattle room costs as much timber as a timber one (8 timber). A real wattle-and-daub room is about 4 timber of posts and poles,
    about 30 withies, daub and thatch.
  - Proposed for a small room:
    - wattle: 3 timber, 30 withies, 400 straw, 6 units;
    - timber: 14 timber, 2 stone, 10 withies, 400 straw, 8 units, a carpenter;
    - stone: as now, plus thatch.
  - A new 2-space wattle hut room serves the smoke hut: the hut 1 timber, 10 withies, 130 straw, 2 units, with racks of 4 withies,
    1 timber and 2 units, holding 500 fish.
  - A timber or stone smokehouse is a small room with two tiered sets of racks, about 1,500 fish.
- **The piles in the runs, by kind (§2):**
  - in the farm worlds, overflow grain at harvest (wild_region_s7: 763 of 790 food outside doors on day 29; the river run: 51 on
    day 10);
  - in pw1, drying and dried meat on racks at the doors (69 to 109 food from day 15 to day 70), not a storage failure;
  - small foraged goods left in the fields (acorns, hedge fruit: 10 to 22);
  - meat in sets (kills and catches waiting: 2 to 25);
  - a little in remains.

---

## 1. What the engine does now

| Store | Holds | Costs | Keeps (spoilage) | Against vermin |
|---|---|---|---|---|
| free floor in a room | 30 kg a space, any goods | none | the house rate (x0.3 of the in-hand rate); with any keeping fitting, **that fitting's rate for all the stock** | all the stock gets the building's fittings' stops |
| bins | 60 food, 1 space | 3 timber (about 720 kg of wood), 1 unit, basic | x0.5 of the house rate | tiny kinds x0.7 (STORE_STOPS) |
| granary floor | 300 grain, 3 spaces | 6 timber, 4 units, basic | x0.2 | climbing and tiny x0.3 |
| cellar | 40 food a space of footprint | 4 stone, 6 units, mason, **flat whatever the footprint** | x0.25 | none |
| woodshed | 40 timber, 2 spaces of ground | 2 timber, 1 unit | none (no wet timber, [[Q-24 Built for the building package|Q-24]] (7)) | - |
| vault | 30 kg a space, 4 spaces, its own room | 40 stone, 30 units, mason | the house rate; fireproof | none |
| a pile at the door | the overflow ([[D4-89 Goods left at a door stay the house's|D4-89]]) | - | the open (grain x4 dry, x10 wet) | **only LEFT_OUT goods (meat, fish, milk); dry goods untouched** |

For comparison, against the engine's own works:
- a wood fence round a parcel: 4 timber and 10 units x the root of its size;
- a dry-stone wall: 8 stone and 20 units;
- a small wattle room: 8 timber, 6 units;
- a small stone room: 30 stone, 4 timber, 40 units;
- a hearth: 4 stone, 3 units;
- a weir's wattle first section: 12 timber, 24 units.

The vermin's take (`wild._stores`) runs as follows:
- The ecology's night gives a share eaten of "stores", kind by kind. It is the model's eaten over its year of store, capped at 0.5.
- That share is multiplied by the building's stops (bins, granary, a cat in the stock, an owl nesting, a dog) and by a vole plague.
- It is then taken from every dry good in the stock (`DRY_STORES`: grain, rye, oats, beans, meal, flour), and from racks inside the
  house.
- Food at the door (LEFT_OUT) is taken at twice the share.
- The ecology sees the real store through `_follow_harvest`: its total dry goods against their running mean, clipped to 0.2 to 3.

---

## 2. What the runs show (measured 22 Nov, the downloaded journals)

The script, `scratchpad/storage_scripts/piles.py`, reads each checkpoint's world, sorts every container's food by kind (stock, pile
at a door, rack at a door or inside, pile in the field, set, carcass, remains, hands), and lists the houses by food against their
fittings.

| Run, day | Stocks | Outside the stores, by kind | Notes |
|---|---|---|---|
| wild_region_s7, d10 | 2,189 food in 10 stocks (grain 1,943) | field pile 30 (grain), door 17 (green grain), sets 1 | Holt 560 (550 grain), Carter 539, Wood 437: halls of 30 to 36 spaces with one bins (60); the rest **on free floor**, legally |
| wild_region_s7, d29 | 2,255 (grain 2,108) | **piles at doors 790: grain 763**, dried meat 26 on racks; field 9; sets 0.4 | after the harvest, with granaries built at Carter, Holt and Wood: Holt 335 at the door, Wood 267, the Holt byre 144, Hayward 29, Cotter 15 |
| pw1_opus_sonnet_r1, d15 | 127 | **door pile 99 (grain 96)**, racks at doors 69 (drying meat 53, dried 16), sets 6 | Reed House (12 spaces, beds 6) overflowed its grain |
| pw1, d30 to d99 | 20 to 77 (nuts, acorn meal) | **racks at doors 63 to 109 (dried and drying meat)**; field piles 10 to 22 (acorns, hedge fruit, a little fish); sets 2 to 25 (meat); remains 0 to 4 | the meat kept on its racks at the door, not taken in |
| water_runs_models_r1, d10 | 473 (grain 366) | door 51 (grain, Wood House) | then little outside: d20 carcass 12, rack inside 7 |

**How to read them:**
1. The houses "over their bins" are within their floor, and real in mass. What is not real is that 500 kg of loose grain on an
   earth floor keeps as well as the bins and is as safe from mice.
2. The overflow outside the door is the harvest, and it is never touched by vermin. It sits in the open at four to ten times the
   house rate: 2 to 5% of it lost a night (an estimate from DECAY).
3. pw1's piles are a keeping step, meat drying on racks at the door. That belongs to the smoking and drying design ([[D2-271 Smoking in three depths|D2-271]]), not to
   storage.

---

## 3. What each store really held, cost and protected against

Each table gives the real figures and then the proposal on the engine's basis. "Building scale" means the engine's present
compression of building work, about real hours ÷ 30 to 70 (§4). "Craft hours" means real hours, as the gear and cord are priced
([[D2-264 The fishing, hunting and materials network|D2-264]], fibre_and_cord.md).

### 3.1 The house floor (goods loose, in heaps)

| | |
|---|---|
| **Real** | A beaten-earth or rush-strewn floor; heaps against a wall, sacks set on it. Mass is not the limit: a heap of wheat 0.5 m deep on 5 m² is about 1.9 t (est.). The limit is living room. Peasants put their wealth in beasts and fodder more than household goods (Briggs, Walsham inventories). It removes rain and sun only. The floor is damp from the earth, and grain on it is trodden, spilt and open to every mouse. |
| **Holds (proposed)** | 30 kg a space loose (as now: a heap or two by the wall, the room still lived in); containers set on the floor take its spaces (§3.2 to §3.6). |
| **Costs** | Nothing. |
| **Protects** | Rain and sun (the [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]] outside penalties). |
| **Worse at** | **Floor damp** for dry goods (grain, meal, flour, beans, salt): x2 the base (est.); **vermin exposure 1.0**; draws vermin (§6). |

### 3.2 Sacks

| | |
|---|---|
| **Real** | A sack or "bag" of 2 bushels, about 54 kg of wheat (wheat sold by the bag of 2 bushels at Saltash and Modbury; a bushel of wheat 60 lb, 27.2 kg). 19th-century mill sacks took 4 bushels. Coarse hemp or linen cloth, about 1.2 m² a sack (est.); 0.5 to 0.6 kg of yarn (est.). Cord takes about 8 units a kg in flax, field to yarn (fibre_and_cord.md), and weaving runs at about 2.5 yards of cloth a working day (Munro's Flemish weaver, wool). So a sack is about 14 to 18 hours of work (est.), mostly spinning. It lasts a few years with mending (est.). It removes damp when on boards, and keeps order and carriage (to the mill, to market). Rats and mice gnaw through: the classic sign is "the sacks gnawed through at the bottom". |
| **Holds (proposed)** | 50 kg of dry goods (grain, rye, beans, meal, flour, nuts, salt). 12 sacks to a space, stacked with a walkway (est.): 600 kg a space. |
| **Costs** | 0.6 cord and 2 units (weave and sew; basic). Craft hours: about 7 units in all with the cord's own. |
| **Life** | 3 world years (est.; it wears with each emptying). |
| **Protects** | Order; carried as one load; floor damp halved (x1.5 in place of x2). |
| **Worse at** | Vermin 0.8 (rats), 0.7 (mice); a sack gnawed loses a little more, as spilt. |

### 3.3 Baskets

| | |
|---|---|
| **Real** | A bushel basket holds about 36 L: 27 kg of wheat, or about 20 to 25 kg of roots or apples (est.). An experienced maker weaves an average basket in a few hours, and a field basket in a couple. The rods are soaked or mellowed first. Withies are about 2 to 3 kg a basket (est.). It lasts a few years. It gives air (roots and fruit sweat in a heap) and gets them off the floor. Grain sifts through unless the basket is lined, and it gives no defence against mice. |
| **Holds (proposed)** | 25 kg of roots, nuts, fruit, eggs, dried or smoked meat and fish, cheese (not grain, meal or flour). 10 to a space (est.): 250 kg. |
| **Costs** | 0.3 withies and 1 unit (basketry, basic; craft hours). |
| **Life** | 2 world years (est.). |
| **Protects** | Air for roots (the heap penalty, x1.5, removed); off the floor. |
| **Worse at** | Vermin 0.7; not for grain or meal. |

### 3.4 Bins, chests and the corn ark

| | |
|---|---|
| **Real** | The ark or hutch ("wheat hutch", "meal hutch", "corn hutch" in inventories) held grain, meal or bread at home from the 14th century. It was riven oak boards with tight joints against pests (V&A; Shakespeare Birthplace Trust). Survivors are mostly 16th and 17th century, and one source holds that the medieval ones held linen, not grain. I found no capacity. From surviving sizes, about 1.2 to 1.5 m by 0.55 to 0.65 by 0.7 to 0.9 m, it held about 0.5 to 0.8 m³: **300 to 600 kg of wheat** (est.). Work: a joined ark is about 2 to 3 carpenter's days (est.), from about 100 kg of boards (est.: about half a timber). It lasts for centuries. It removes damp (it stands on stiles), and stops mice and slows rats, which gnaw at the corners. |
| **Holds (proposed)** | **Bins** (the present fitting, boarded, built in): 300 kg of dry goods in 1 space. **A chest or ark** (a fit-out good): 400 kg of dry goods in 1 space. |
| **Costs** | Bins: 1 timber, 3 units, basic (was 3 timber, 1 unit, holding 60). Chest: 1 timber, 10 units, carpenter (craft hours). |
| **Life** | Bins 10 world years; a chest 30 (est.). |
| **Protects** | Floor damp removed. Vermin: bins 0.4, a chest 0.15. A chest can take a lock (§9). |
| **Worse at** | A carpenter and a timber for the chest; neither can be moved when full. |

### 3.5 Clay jars and crocks (later: no clay or potter yet)

| | |
|---|---|
| **Real** | Storage jars run from about 4 L to 40 L. A Roman amphora as a unit is 26 L, and the size of storage jars varies widely (Ashmolean PotWeb). I found no medieval storage jar's capacity or a potter's rate. A thrown jar of about 20 L takes well under an hour on the wheel (est.), then drying and a firing in a kiln of hundreds of pieces. It suits butter, lard, honey, salted meat, pickles and seed grain. It removes vermin entirely with a weighted lid, and damp and flies. It breaks. |
| **Holds (proposed)** | 20 kg; 15 a space (300 kg). |
| **Costs** | About 10 kg of clay and a share of a firing; a potter. |
| **Life** | Until broken: about 5% a world year (est.). |
| **Protects** | Vermin 0.05, flies, damp. |
| **Worse at** | Needs clay and a kiln; small; breaks. **Deferred** until there is a clay good. |

### 3.6 Barrels (a cooper) and the salt barrel in brine

| | |
|---|---|
| **Real** | A herring barrel held about 30 gallons (136 L): 500 to 1,100 fish, with pickle-salted contents of about 320 lb (145 kg). A modern cure is about 1 part salt to 4 of fish by weight (100 kg fish to 25 kg salt). Baltic trials ran 10 to 30 kg of salt to 100 kg of fish. A 19th-century barrel of pork took 40 to 50 lb of salt, and meat left above the brine "will become wormy". **Work:** a master cooper takes about 8 to 11 hours a barrel by hand, about one a day. **Timber:** about 100 board feet of stave bolt a barrel, about 0.24 m³ of log, or 0.7 of a timber (est.). Medieval hoops were often split hazel or willow (est.). It lasts years. **It protects against:** vermin, flies and damp; brine makes salt goods keep; it travels. |
| **Holds (proposed)** | 120 kg of dry goods, or salt fish or salt meat in brine; 4 to a space (480 kg). |
| **Costs** | 0.7 timber, 0.3 withies (hoops) and 5 units; **a cooper's trade** (new). Salting in it is the existing salting work and salt (about 1 salt to 4 or 5 fish, as [[Q-70 Adopt the food values on one basis, and fix the runs, the weir and…|Q-70]]). |
| **Life** | 10 world years (est.). |
| **Protects** | Vermin 0.05; flies; damp. **In brine, salt fish and salt meat keep at their base.** Out of brine (in a sack, on the floor) they take a "dry, open" penalty of x2 (est.) and flies in summer. |
| **Worse at** | A cooper; dear. |

### 3.7 The granary floor and the granary on staddle stones

| | |
|---|---|
| **Real** | Varro (I.57) describes raised granaries in Hispania and Apulia, aired and out of reach of pests. Columella wants them cool, aired and dry, and sealed against cracks that let animals and weevils in. In England, free-standing timber granaries on staddle stones were common in the south in the 18th century (Weald and Downland's of 1731). The staddles numbered five for a small one, 12 (four by three) typically, and 36 at Upper Hexford. Their mushroom caps stop climbing rats, though not entirely, and the top step was left out. They are a timber frame, weatherboarded, with a tight floor. I found no capacity. A granary of 3.5 by 3.5 m with grain to about 1 m holds about 10 m³, **6 to 7 t** (est.). Before the Black Death, demesne storage was in barns. Purveyors' stores were modest and like households' own (Claridge and Langdon, 2011). Carryover from one harvest to the next was rare on the Winchester manors. Later medieval tenant farmers built smaller barns (Journal of Medieval History, 2023). |
| **Holds (proposed)** | **Granary floor** (a boarded loft or upper floor in a building; the present fitting, 3 spaces): grain loose, **400 kg a space** (1,200; was 300 in all), or containers. **Granary on staddles** (a building of its own: a small timber room raised): 6 spaces at 400 kg a space loose, **2.4 t**, or containers. |
| **Costs** | Floor: 2 timber, 6 units, basic. On staddles, a small timber room (today 8 timber, 2 stone, 6 units; as §11 proposes, 14 timber, 2 stone, 10 withies, 400 straw, 8 units) plus 9 staddles (3 stone, 3 units, mason) plus a tight floor (2 timber, 2 units): about **10 timber, 5 stone and 11 units** at today's room cost (about 16 timber, 5 stone and 13 units at §11's), with a mason's part. |
| **Protects** | Floor damp removed; air. Vermin: the floor 0.6 (a loft keeps out only the lazy); **on staddles 0.25** for climbing and tiny kinds (STORE_STOPS's 0.3). |
| **Worse at** | Fire (timber); stands apart, so it can be robbed unseen; not cool. |

### 3.8 The barn (sheaves, hay, straw)

| | |
|---|---|
| **Real** | Grain was kept in the ear in the barn and threshed through the winter. Threshed grain stored in bulk tends to rot, so it was kept with its chaff and winnowing was put off (Tools and Tillage). The flail does 5 to 8 bushels of wheat a day. Great barns took 400 to 500 oaks, and Harmondsworth (1425-27) cost about £50 to £100, about 18 months of the manor's profit. Tenants' barns were smaller. A barn of 3 bays, about 10 by 5 m (est.), holds a few hectares' sheaves. It is a winter workplace, holds wool, and its mice are the owls' prey (the owl hole). |
| **Holds (proposed)** | Hay, straw and (later) sheaves: **1,000 kg a space** stacked to the roof (est. from hay at 110 to 170 kg a m³ and about 6 to 8 m³ a space). |
| **Costs** | As a timber room (a medium timber room: 15 timber, 4 stone, 15 units, carpenter); a building of its own. |
| **Protects** | Rain; hay and straw kept dry. |
| **Worse at** | Vermin 0.8 among sheaves; fire. **Sheaves and threshing are not in the engine**: until they are, a barn is a dry room for hay, straw and timber. |

### 3.9 The hay rick (and the rick on staddles)

| | |
|---|---|
| **Real** | Settled hay takes 6 to 9 m³ a tonne (250 to 300 ft³ a ton for stacked hay; fluffy hay 400). So a 10 t rick is about 70 to 90 m³: about 6 by 4 by 3.5 m (est.). It is built by a team in about a day (est.) and thatched. Ricks also stood on staddles against mice. Its risks are rain, heating if stacked wet, fire, and mice. |
| **Holds (proposed)** | A rick on a parcel (a thing, as a pile is): hay or straw, up to 10 t. |
| **Costs** | 3 units for a team (building scale) and 1 straw a tonne to thatch it (est.); staddles 9 stone and 3 units (mason). |
| **Protects** | Rain, once thatched. **Hay does not spoil in the engine today** (spoil 0), so a rick protects nothing until hay rots in the open wet (est.: x3 of a small base). |
| **Worse at** | Fire; mice 0.6 (on staddles 0.2). |

### 3.10 The root clamp

| | |
|---|---|
| **Real** | A long heap of roots under loose dry straw 60 to 100 cm deep (12 to 20 cm compressed) and 5 to 10 cm of earth, run north-south so the sun clears frost from its walls. Rotting tubers are taken out first (ISO 5525). Rot spreads through a heap in weeks, and frosted roots break down (Rothamsted clamp studies; Manitoba). A clamp 1.5 m wide, 1 m high and 5 m long is about 3.75 m³, about 2.5 t of roots (est.), made in about a day (est.). |
| **Holds (proposed)** | Roots (and later potatoes, turnips, apples in straw): up to 3 t. A thing on a parcel. |
| **Costs** | 1 unit and 1 straw a tonne (building scale); basic. |
| **Protects** | Frost (roots' frozen loss removed); rain. |
| **Worse at** | Rats 0.8; **boar in frost** (WHEN already says "will come to the clamps and the stores"); opening it lets the frost in (est.: x2 the night it is opened in frost); rot spreading (est.: x1.5 once any has gone). **Roots are only a wild good now**, so the clamp waits on root crops. |

### 3.11 The cellar

| | |
|---|---|
| **Real** | A root cellar is best at 0 to 4.5 °C and 85 to 95% humidity, with its floor below the frost line. Ground 4 to 6 ft down holds about 10 to 14 °C in temperate America, so a cellar is cool and steady rather than cold, and always damp. In medieval England, cellars are mostly urban or high status (Leicester's 12th-century undercroft, Norwich's Cowgate). The finest are wine cellars shown to guests (Wright, 2025). A rural one is rare: Well Wood, Aylesford, was 13th century and filled in soon after. **Work under a 30 m² footprint:** dig about 60 m³ at 3.5 m³ a day (ILO: soft 5, medium 3.5, hard 3, very hard 2; by hand 0.6 to 0.76 m³ an hour), about 17 to 30 days; line it, about 22 m of wall 2 m high and 0.4 m thick, about 17 m³ or 28 t of stone (at about 1.6 t a m³), set by a mason in about 15 to 25 days with a labourer; joists and a hatch. **About 40 to 70 days in all, or 20 to 35 timber-lined (est.).** It removes heat, frost and light. It adds damp (bad for grain, meal, flour and salt). Rats live in cellars. |
| **Holds (proposed)** | A space by footprint (as now); **its floor holds loose goods at 30 kg a space, and containers** (barrels, crocks, baskets, shelves of cheese) as a room's floor does. That is up to about 400 kg a space with barrels (was 40 food a space at a quarter of the rate). |
| **Costs** | **By footprint:** dug and timber-lined, 1 unit and 0.25 timber a space; stone-lined, 1.5 units and 2 stone a space, mason. Under a small room (6 spaces): 6 units and 1.5 timber, or 9 units and 12 stone. Under a hall (30): 30 units and 7.5 timber, or 45 units and 60 stone. **Site:** not on fen, saltmarsh or a parcel that floods (it fills); on rock, the dig is doubled. A timber lining rots (10 world years, est.). |
| **Protects** | **Heat** (the warm season's factor removed for meat, fish, cheese, milk, butter, eggs; [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]]'s "a cellar's cool for the foods heat ruins"); **frost** (roots, apples); light. |
| **Worse at** | **Damp** for grain, meal, flour and salt (x2, est.: keep them in a granary); vermin 1.0 (it stops none); dear and a mason's for stone. |

### 3.12 The smokehouse loft and hanging (hooks in the roof)

| | |
|---|---|
| **Real** | Meat was hung in the roof space over the open fire "where the smoke would help cure it", or in the chimney (the common English advice). Salt did the keeping, and the smoke's heat could turn fat rancid. Flitches were bagged in calico against flies (1908). An 18th-century Scottish smokehouse held 120 flitches. |
| **Holds (proposed)** | Hung goods (smoked, dried or salt meat and fish, bacon) in the roof of a room with a hearth: 40 kg a space of the hearth's room, up to 120 kg (est.). |
| **Costs** | 0.5 timber (poles and hooks), 1 unit, basic. |
| **Protects** | Flies (the smoke factor, as `drying meat` smoke 0.25); vermin 0.3 (hung). |
| **Worse at** | Small; meat fat a little worse for the heat (x1.1, est.); only above a lit hearth. The keeping smokes of [[D2-271 Smoking in three depths|D2-271]] stay in the smoke hut and smokehouse. |

### 3.13 The woodshed

| | |
|---|---|
| **Real** | A cord is 3.6 m³ stacked, and seasoned oak weighs 1.6 to 1.9 t a cord. Green wood is 70 to 100% heavier, and oak takes up to two years to season. |
| **Holds (proposed)** | **As now:** 40 timber (about 9.6 t) on 2 spaces of ground. Stacked 2 m high on 10 m², that is about 20 m³, about 5.5 cords, about 9 to 10 t. **The engine's figure is real.** |
| **Costs** | As now: 2 timber, 1 unit, a lean-to. |
| **Protects** | Rain on fuel. That only counts once wood outside gets wet ([[Q-24 Built for the building package|Q-24]] (7): est., wet wood gives 0.7 of its heat). |
| **Worse at** | Fire, if against the house. |

### 3.14 The vault

| | |
|---|---|
| **Real** | A stone-arched undercroft: a merchant's or lord's store (Leicester, Norwich). It does not burn ([[D2-49 Stone resists fire but is not fireproof|D2-49]]) and has a door that locks. |
| **Holds (proposed)** | A space: its floor holds loose goods at 30 kg a space, and containers. Up to about 400 kg a space with barrels and chests (was 30 kg a space in all). |
| **Costs** | As now (40 stone, 30 units, mason). |
| **Protects** | Fire; **theft** (a locked door: §9's lock on the room); vermin 0.5 (stone, few gaps); cool, if half sunk (as a cellar). |
| **Worse at** | Dear. |

### 3.15 The ice house (later)

| | |
|---|---|
| **Real** | 18th and 19th century, on estates: brick-lined, domed and mostly underground. Scotchtown's is a shaft about 9 by 9 ft and about 30 ft deep. Monticello's took 62 wagon loads to fill and cost £70 in 1803. An 1894 brick one held about 200 t of ice. It needs ice cut each winter. |
| **Proposed** | **Deferred:** out of period for a medieval village, and needs ice harvesting and a frozen water body. If built, it is a cellar that removes heat entirely, so fresh meat and fish keep at their base. That would be its own entry in OPEN's deferred table. |

### 3.16 Not asked, worth having: the sealed grain pit

| | |
|---|---|
| **Real** | Iron Age storage pits at Danebury averaged about 2.2 m³ early and about 4.35 m³ later: about **1.4 to 3.3 t of wheat** at 0.77 t a m³ (my conversion). Reynolds's experiments at Butser found pit storage "a successful method of bulk grain storage" when sealed. The grain at the walls rots while the interior keeps, the grain using up the air. Iberian household silos held 1,000 to 3,000 L (Antiquity, 2019). |
| **Holds (proposed)** | A pit dug on a parcel (a thing, as a buried cache is): up to 2 t of grain or beans. |
| **Costs** | 2 units to dig and line, and clay or 1 straw to seal (building scale); basic. |
| **Protects** | Vermin 0.05; at the grain's base, sealed. **The engine's `buried` x2 for grain is the reverse of this:** a sealed pit should keep at base, with an edge loss of about 2% of what goes in (est.). |
| **Worse at** | **Once opened it must be emptied:** about x3 a night after (est.), so it suits seed grain and a year's reserve, not daily use. It lies outside, where it can be found and robbed. |

---

## 4. Costs against each other: the cellar, the fence and the room

| Work | Real (est. where marked) | Engine now | Engine ÷ real |
|---|---|---|---|
| hurdle fence round a 2 ha parcel (566 m) | 315 hurdles at 3 a day, about 105 days, plus stakes and cutting rods; about 120 days (est.) | 10 units (3.3 days) | about 1/35 |
| hurdle fence round a close of 0.2 ha (180 m) | about 35 days (est.) | the same formula at size 0.1: about 3 units | about 1/70 |
| dry-stone wall round 2 ha | 566 m at 3 to 6 m a day, about 100 to 190 days; about 1 to 2 t of stone a m | 20 units (6.7 days), 8 stone | about 1/15 to 1/30 |
| a small wattle-and-daub room of 30 m² | about 30 to 60 days (est.) | 6 units | about 1/30 to 1/60 |
| a stone-lined cellar under 30 m² | about 40 to 70 days (§3.11, est.) | 6 units and 4 stone | about 1/40 to 1/70 |
| a timber-lined cellar under 30 m² | about 20 to 35 days (est.) | (none) | - |
| a joined ark | about 2 to 3 days (est.) | bins: 1 unit | about 1/12 |
| a barrel | about 1 day | (none) | - |
| a sack, field to sack | about 2 days (est.) | (none) | - |

**What the table says:**
1. **On real hours a cellar is not dearer than a fence: a field's fence is about twice a stone cellar.** Zach's sense that a cellar
   should not be quicker than a fence holds against a close's fence, not a field's.
2. **The engine builds every work at about 1/30 to 1/70 of real hours**, while crafts (cord, traps, nets, the weir's sections) are
   priced at real hours ([[D2-264 The fishing, hunting and materials network|D2-264]], the gear notes). Under that one scale the engine's cellar is in line with its fence and its room;
   its mistakes lie elsewhere (§0).
3. **The proposal prices works (spaces) on the building scale and containers at craft hours.**
   - **Spaces** (rooms, a cellar by footprint, a granary, a clamp, a rick, a pit) are on the building scale. A timber-lined cellar
     under a cottage is then 6 units, a stone one 9 units and 12 stone, against a field's fence at 10 and a wall at 20.
   - **Containers** (sacks, baskets, chests, barrels) are at craft hours. A chest is 10 units, a barrel 5, a sack about 7 with its
     cord, a basket 1.
   - The good containers are therefore realistically dear and need a craft and a material. The cheap stores are a basket, a heap,
     a clamp, a pit.
4. **For Zach (an ask):** the building scale is a lever of its own, about 1/30 to 1/70 of real hours today, and uneven: the close's
   fence is the most compressed. Under [[D2-259 The food values are anchored on real values|D2-259]] it should be named and decided. One option is building at about 1/11, the compressed
   year's factor, so a season's real building is a world season. That would make a cottage about 3 to 5 world days of one person's
   work, and a fence round a field about 11.

---

## 5. Two layers: the space and the containers in it (Zach's follow-ups)

**The model.**
- **The space** holds goods loose on its floor and gives the climate.
  - A room: covered, out of the sun, with floor damp.
  - A loft or granary floor: dry, aired.
  - A granary on staddles: dry and raised.
  - A cellar: cool, frost-free, damp.
  - A smoke loft: smoke.
  - A clamp: frost-free.
  - A rick: shed rain.
  - A pit: sealed.
- **Loose on a space** (on the floor, in heaps), goods are fully exposed to vermin, and dry goods take the floor damp.
- **The containers** in a space add protection and order: sacks, baskets, bins and chests, barrels, later crocks. Shelves and hooks
  are part of the room or loft, as Zach's coordinator suggested, so they are not containers.
  - Each container has a capacity, a protection by risk, a life, and the goods it suits: grain in sacks or a chest, salt fish in a
    barrel, roots and cheese in baskets or on the room's shelves, smoked fish hung.
  - Each takes floor: sacks 12 a space, baskets 10, a chest or bins 1, barrels 4, crocks 15.
- **The present fittings map as follows:**
  - **bins** are both layers at once (a boarded container built into the floor), and stay a fitting;
  - the **granary floor**, **cellar**, **woodshed** and **vault** are spaces;
  - **smoke racks** belong to keeping ([[D2-271 Smoking in three depths|D2-271]]);
  - **stalls** are not storage.

**Three ways to build it.**

| | One layer (fittings only, kept per portion) | **The fit-out (recommended)** | Full two layers (agents place goods) |
|---|---|---|---|
| What agents do | build fittings as now | make or trade containers and keep them in a store (a sack made at home goes into the house's store, as goods do); goods go "into the store" | make containers, then put each good into a named container |
| What the engine does | keeps each good by the store it lies in (closes [[Q-24 Built for the building package|Q-24]] (6)) | sorts each good into the best container with room for it (grain: chest, then bins, then sacks, then loose); keeps and exposes each portion by its container and space | as told; loose if not |
| Legibility | as now | one line: "Holt House keeps 735 grain (400 in the ark C3, 300 in 6 sacks, 35 loose on the floor), 9 beans in a basket; 335 grain lie outside the door" | many acts, misread (agents already miss recipes; storage acts compete for units) |
| Engine cost (est.) | small: `alloc` returns portions; `decay_rate` and `_stores` take a portion; about 60 lines | container goods with holds and guards (a few ITEMS rows, the cat's precedent); `alloc` over containers by protection; per-portion keeping and vermin; the store line; making techniques for sack, basket, chest; about 250 to 350 lines and tests | the fit-out plus a placement verb, per-container state, refusals; about 500 lines and a prompt section |
| Value | fixes the measured problem | the measured fix; **buyers for the materials network** (cord, withies, timber, a cooper and a carpenter); cheap-but-worse choices that are real; a tradeable, portable store; a lock (§9) | little beyond the fit-out |

**Recommended: the fit-out, in three stages.**
1. Per-portion keeping and vermin, with the existing fittings and the loose floor, the bins resized, the cellar by footprint, and
   door piles taken. This fixes what the runs show.
2. Sacks, baskets and chests as fit-out goods, when cord and withies exist as goods. They are proposed in hunt_fish_materials.md
   but not yet in `data.py`.
3. Barrels with a cooper; crocks with clay; clamps, ricks and pits with their crops and things.

---

## 6. Vermin: what lies open is taken, and draws more

**The take, per portion.** Tonight's share for a kind *k* (from the ecology, as now) is taken from each portion *a* of each
building's dry goods as:

`take = q_a × share_k × exposure(a, k) × stops(building, k) × plague`

The exposure numbers are estimates, to calibrate. A space's exposure multiplies its container's.

| Where it lies | Rats | Mice |
|---|---|---|
| a pile at the door (outside; dry goods too, which are taken today only if LEFT_OUT) | 1.5 | 1.5 |
| loose on a floor, or in a cellar | 1.0 | 1.0 |
| a basket | 0.8 | 0.7 |
| a sack | 0.8 | 0.7 |
| bins (boarded) | 0.5 | 0.4 |
| hung from the roof | 0.3 | 0.3 |
| a chest or ark | 0.2 | 0.15 |
| a barrel, a crock, a sealed pit | 0.05 | 0.05 |
| a clamp | 0.8 | 0.6 |
| a rick | 0.6 | 0.6 |
| a rick on staddles | 0.2 | 0.2 |
| (space) a granary floor | x0.6 | x0.6 |
| (space) a granary on staddles | x0.25 | x0.25 |

**The stops** (a building's beasts, `_stops`) are split by kind, on the evidence:
- **A cat:** mice x0.4, rats x0.7. Elton (1953): cats keep a clean farm clean but do not clear an established rat infestation. The
  feral-cat study of 2018 saw 20 stalks in 300 videos.
- **A barn owl** in its hole: mice x0.6, rats x0.9.
- **A dog** (a terrier): rats x0.5, mice x0.8.
- **A vole plague:** as now.

**The draw.** In `_follow_harvest` and `_store_food`, the store the ecology sees becomes the **exposed** store, Σ q_a × mean
exposure. This has three effects:
- grain spilt or heaped on a floor, or lying at the door, raises the vermin's food and, through the follow-harvest scale, their
  numbers on the village's land;
- a village that keeps its grain in chests and barrels starves them down;
- the PRESENCE row for rats at home (density 60 and over: "droppings along the walls and something scuttling in the thatch at
  night") then shows the change.

**The numbers to calibrate against.**
- A 250 g rat eats about 25 g a day, about 6.5 to 9 kg a year (FAO), and fouls or spills several times that: 7.5 times in a
  laboratory study, and 25 rats eat and damage about half a tonne a year (IRRI).
- A mouse eats 3 to 4 g a day and leaves 20 to 75 droppings. In a closed population in stored wheat, 55% of the seeds were fouled
  with urine in 150 days.
- Losses to rodents of about 2.5% of stored products are a common Indian estimate.

**Proposed targets** (est., for the wild tests world's `kept` arm, `specs/make_wild_tests.py`), for vermin losses over a world year
in an ordinary year:

| How it is kept | Lost to vermin |
|---|---|
| loose on a floor | about 15 to 25% |
| in sacks | about 10 to 15% |
| in bins | about 6 to 10% |
| in chests with a cat | about 2 to 4% |
| in a granary on staddles | about 2% |

(The compressed year is already absorbed: the take is a share of the model's own year of store, applied to the real store.)

**Signs, by where the loss was** (EATEN_SIGNS "stores", made specific):
- loose: "grain scattered and trodden into the floor, mouse droppings in it";
- sacks: "the sacks gnawed through at the bottom, grain run out on the floor";
- a chest: "fresh gnaw marks at a corner of the ark";
- at the door: "the heap outside the door dug into and scattered in the night";
- a clamp in frost: "the clamp opened at one end, roots dragged out and gnawed".

These follow senses.md: grounded in a change, worth acting on, and never an act the person did not choose.

**Spilling.** I propose no separate spill act. The exposure of loose and sacked grain stands for spilt grain, and its draw on the
vermin is the exposed store. If a finer rule is wanted later: a share of 0.5% of loose or sacked grain moved in a day lies spilt
for a season, at exposure 1, and draws vermin (est.).

---

## 7. Spoilage under [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]], per portion

Each portion keeps at the food's base (its well-kept rate), times every outside penalty its space and container do not remove. All
factors are estimates except those already in DECAY.

| Penalty | Applies to | Factor | Removed by |
|---|---|---|---|
| open, dry or wet (DECAY's rows) | everything outside | as DECAY | any roof |
| floor damp | grain, rye, beans, meal, flour, salt, bread | x2 (x1.5 in sacks) | bins, chest, barrel, crock, a granary floor, staddles, an upper storey's boarded floor |
| cellar damp | the same | x2 | (added by the cellar) |
| heat (the warm season) | meat, fish, cheese, milk, butter, eggs (DECAY `warm`) | as DECAY | a cellar; an ice house (later) |
| flies (summer) | fresh and drying meat and fish, cheese | x1.5 (est.; today the `smoke` row, 0.25, stands for removing them) | smoke (loft, racks), barrel, crock, bagging |
| frost | roots, (later) apples and potatoes | DECAY `frozen` read as damage, x3 for roots (est.) | cellar, clamp |
| heaped roots sweat | roots loose | x1.5 | baskets, clamp |
| out of brine | salt fish, salt meat | x2 | a barrel in brine |
| a store's own wear (gappy, holed) | everything inside | `wear.damp` as now | mending |

Fresh fish's x2 in a store ([[D2-212 Fresh fish keep twice as badly as meat in a store|D2-212]]) stays, as the fish's own rate. Today's `house_spoil` and the fittings' `spoil` multipliers go,
as [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]] says.

---

## 8. What changes in the engine, and which worlds

**Data (`engine/data.py`):**
- FITTINGS:
  - bins: holds 300, 1 timber, 3 units;
  - granary: holds 400 grain a space of its 3, 2 timber, 6 units;
  - cellar: holds loose at the floor rate, cost by footprint (`units_a_space`, `materials_a_space`, `lining`: timber or stone),
    `site` (no fen, saltmarsh or flood; rock doubles), `protects` heat and frost, adds damp;
  - vault: holds as a floor with containers;
  - a smoke loft;
  - a granary on staddles (a BLUEPRINT: a raised small timber room).
- New fields replacing `spoil` on fittings: `protects` (penalties removed) and `exposure` (by body).
- New container ITEMS, with `holds` {kind: kg}, `space_holds` (n a space), `protects` and `exposure`, and `life`: sack, basket,
  chest, barrel, later crock.
- PHYSICS: drop `house_spoil` and `cellar_spoil` ([[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]]).
- DECAY: add the `floor_damp`, `cellar_damp`, `flies`, `heap` and `brine` penalties; `buried` for grain becomes a sealed pit's
  base, with the opening rule.
- STORES `floor`: 30 kept.

**Buildings (`engine/buildings.py`):**
- `stores` and `alloc` return portions: {container or space: {good: qty}}.
- The sort order is by each good's best protection, and a manual hold or move is honoured (§9).
- `full_words` and the store line show the portions.

**Night (`engine/night.py`):**
- `decay_rate` per portion, by its space's and container's removed penalties. This closes [[Q-24 Built for the building package|Q-24]] (6) and the live point in [[L-131 The wild layer's live points from briefs 1 to 3|L-131]].

**Wild (`engine/wild.py`, `wild/kinds.py`):**
- `_stores` per portion with `exposure`;
- door piles of dry goods taken at 1.5;
- `_stops` split by kind (cat, owl, dog);
- `_store_food` and `_follow_harvest` read the exposed store;
- EATEN_SIGNS by portion;
- STORE_STOPS's granary and bins rows move into the fittings' `exposure`.

**Prompt (`engine/prompt.py:513`):**
- "a store keeps food 3 times better" becomes what each store and container protects against, in a line;
- the store's one-line summary.

**Techniques:** make a sack (weaving, basic; cord), a basket (basketry, basic; withies), a chest (carpenter), a barrel (cooper: a new
trade), with their lives through the gear's wear.

**Committed worlds whose stores change:**
- **Every world with bins.** landgen/write.py seeds bins: 1 in every house, mill and byre, and the makers seed them too (make_frontier,
  make_plenty, make_wenbridge, make_goal_probe, make_fishing_probe, and about 25 yaml worlds). Bins go from 60 to 300 and keep only
  what is in them, so a seeded house's loose floor goods now keep worse and are exposed.
- **The granary worlds:** hollins, hollins_s7, hollins2, hollins2_s8, barleyfield_s1, region, region_s1, region_c, region_c_s27,
  wenbridge, takeover, orwell.
- **The cellar worlds:** region, region_s1, region_c, region_c_s27, two_valleys, two_valleys_s1, wenbridge, takeover, orwell. Their
  cellars would cost by footprint if rebuilt, and keep cool but damp, so grain moves to bins or the granary.
- **The vault worlds:** wenbridge, takeover, orwell.
- **The wild tests world's `kept` arm** (make_wild_tests: a granary, a cat, an owl hole) is the calibration bed for §6.
- **The subsistence and calibration worlds** ([[W-69 Nutrition worlds|W-69]], [[W-64 Food, weight and work on one basis|W-64]]) are where [[D2-272 A food's base rate of spoiling is its rate when well kept|D2-272]] and preserving are read against stores ([[L-137 Stores may be too strong against preserving|L-137]]).

---

## 9. Manual moves and the locked chest (Zach's third follow-up)

1. **Automatic by default.** Goods put into a store are sorted by the engine (§5). A manual act is optional: `keep {item, qty,
   in: <container tag> | "loose", from: <container tag>}` moves named goods into or out of a named container. A container can also be
   **held back** from the sorting (`keep {hold: C3}`): only goods put in by hand go there, and the sort never takes them out.
   - Containers carry tags as things do ([[D4-68 Short tags, and names given|D4-68]]), shown in the store line.
   - A move within a building is light work: free under 50 kg, else 1 unit a 300 kg (est.).
2. **The locked chest.**
   - **Made:** a chest with a lock: the chest's cost, plus 0.2 copper and 2 units, a smith. It comes with **a key**, an item of no
     weight: "the key to the ark C3".
   - **Who may use it:** only those holding a key may put in or take out, and the automatic sort never places goods in it or takes
     goods from it. It is always held back.
   - **The key:** it can be **given**, **lent** (an agreement), **stolen** (taking it from another's hands or store is theft, as
     any good), or **copied** (a smith, 1 unit and 0.05 copper, with the key in hand that day; est.).
   - **Breaking the lock:** an act on the chest by its tag: 2 units with a tool, 4 bare-handed (est.). It **makes a noise** (a
     sound sign at the place: "a splintering crack from inside Holt House"), **leaves a sign** on the chest ("the hasp of the ark
     wrenched off, the lid split"), and ruins the lock until a smith mends it (1 unit, est.).
   - **Against vermin and damp,** a locked chest is a chest (0.15).
3. **How it sits with holding, theft and targets.**
   - **A household's store** is held by the household: its members may use it, and the head manages it ([[D4-23 Holding is a recognised claim|D4-23]], holding.md).
   - **A locked chest in it** is held by whoever made or bought it, an individual holding (holding.md "an individual") kept in a
     household building. Its contents are that person's, and the household's members cannot take them unless they hold a key.
   - **Taking from another's chest is theft**, as taking from a store one may not use is now (actions.md). Breaking the lock is a
     second act, and leaves a sign whether or not anyone saw.
   - **On the thing as the target** (acts_on_owned_things.md, [[Q-80 Whether acts on owned things default to one's own|Q-80]]): every act on a container names it by its tag ("take 20 grain
     from the ark C3"). Unnamed, an act touches only one's own or one's household's containers. A named act on another's locked
     chest is refused without a key ("the ark C5 is Anna's and locked; you hold no key"), and with a key it is done and the result
     says whose it is.
   - **The store line** distinguishes them: "your locked chest (C3)", "Anna's locked chest (C5)".
   - **An owner's rule:** a head of household who wants the whole store under key locks the store room's door instead, a lock on
     the room as on the vault. That rule belongs to the door, not the containers.

---

## 10. What is estimate, and the asks this raises

**Measured or sourced:**
- the run figures (§2);
- grain bulk densities;
- a rat's and a mouse's intake, droppings and fouling;
- the cats' evidence;
- hurdles at 3 a day;
- wallers at 2.7 to 8 m a day and 1 to 2 t a metre;
- digging norms (modern);
- hay at 6 to 9 m³ a tonne;
- the clamp's construction;
- a root cellar's temperature and humidity;
- the cord's weight and volume;
- a barrel's work (modern master coopers);
- a herring barrel's size and contents;
- a sack of 2 bushels;
- Danebury's pit volumes and Butser's finding;
- staddle counts and dates;
- Varro and Columella;
- the barns' costs and oaks;
- the rarity of rural cellars;
- the ice-house figures.

**Estimates:**
- an ark's capacity and work;
- a sack's and a basket's work and life;
- a granary's capacity;
- a cellar's and a room's real days;
- the exposure numbers;
- the penalty factors;
- the loss targets;
- every engine cost and life proposed above;
- the building scale's range.

**Asks for Zach** (for OPEN, by the coordinator):
- Whether storage becomes the fit-out (§5), staged as proposed.
- Whether capacities stay real, not scaled to the compressed year (§0).
- Whether the engine's building scale is named as a lever and decided (§4), and whether stores follow it, with containers at craft
  hours.
- Whether the cellar costs by footprint, needs a dry site and is damp for grain (§3.11).
- Whether a sealed grain pit and a clamp join as cheap stores (§3.10, §3.16), with hay spoiling in the open wet so a rick and a barn
  matter (§3.8, §3.9).
- Whether the cooper is a new trade (§3.6).
- The locked chest and its key (§9).
- The room costs corrected in kind (wattle with withies and thatch, timber with more wood and a carpenter), a 2-space hut room, and
  the three smokehouses priced on that basis (§11). This is the building owner's area: the board first.

**Deferred:** crocks (wait on clay and a potter), the ice house (out of period; ice harvesting), sheaves and threshing in the barn.

---

## 11. The smokehouses ([[D2-271 Smoking in three depths|D2-271]]) and the room costs on the same basis

**What there is now.**
- The ROOMS table, through `buildings.room_cost`, prices a small room (6 spaces) at:
  - wattle: 8 timber, 6 units;
  - timber: 8 timber, 2 stone, 6 units;
  - stone: 30 stone, 4 timber, 40 units, a mason.
- Smoke racks are 2 timber, 2 units and 3 spaces, holding 40.
- A smokehouse is a building `apart` with racks, so today any of [[D2-271 Smoking in three depths|D2-271]]'s three kinds is a small room plus racks.

**The fault.** Wattle costs as much timber as a timber frame. A real wattle-and-daub building is mostly other things:
- a few posts and roof poles;
- withies woven between the posts;
- daub (clay or mud with dung and straw, dug on the spot);
- thatch.

It is cheap in wood, but it wears and burns. A timber frame is several times the wood, and a carpenter's work.

**Real materials for a small room** (30 m² of floor, about 22 m round, walls about 2 m high: about 44 m² of wall and about 40 m² of
roof). All figures are est., built from the withies note's 20 rods a m² of wattle (about 0.8 withies a m²) and a timber of about
240 kg.

| | Wood | Rods | Daub, stone | Thatch | Craft |
|---|---|---|---|---|---|
| **Wattle and daub** | posts and roof poles about 0.8 to 1 t: **about 4 timber** | 44 m² of wattle, about 35 withies | about 4 m³ of daub (earth on site: work, not a good) | about 40 m² of long straw at about 20 to 25 kg a m²: 800 to 1,000 kg of straw | none (basic) |
| **Timber frame** (on a stone sill, wattle or board panels) | a frame of 3 to 5 m³ of green oak, 3 to 5 t: **about 12 to 20 timber** | panels: about 15 withies if wattle | a sill: about 2 stone | as wattle, or shingles | a carpenter |
| **Stone** | roof timbers about 4 timber | none | about 26 m³ of wall, about 40 t (30 stone as now) | as wattle, or slate | a mason |

**Proposed: the room costs corrected in kind** (the work kept as now, on the building scale, except the timber room's craft):

| Small room | Now | Proposed |
|---|---|---|
| wattle | 8 timber, 6 units | **3 timber, 30 withies, 400 straw, 6 units, basic** |
| timber | 8 timber, 2 stone, 6 units | **14 timber, 2 stone, 10 withies, 400 straw, 8 units, carpenter** |
| stone | 30 stone, 4 timber, 40 units, mason | **30 stone, 4 timber, 400 straw, 40 units, mason** (as now, plus thatch) |

- The straw is a thinner coat than the real 800 to 1,000 kg (a factor of about 0.5, named), so a house is not a whole harvest's
  straw.
- Medium rooms and halls scale with their walls and roofs: about 1.7 and 3.5 times a small room's materials (est.).
- Mending follows the same kinds: wattle with withies and straw, timber with timber.
- This correction belongs to the building owner's area. It should go to the board and to OPEN, and is not decided.
- **It needs two goods the engine lacks:** withies (proposed in hunt_fish_materials.md) and straw for thatch. Straw exists (`straw`,
  1 kg a unit, from the grain harvest), but nothing builds with it yet.

**The smokehouses on that basis.** [[D2-271 Smoking in three depths|D2-271]]'s three depths:
- a wattle smoke hut takes hot and keeping smokes, and can burn with its batch;
- a timber or stone smokehouse takes all three, holds more a space (tiers, an upper storey) and seldom burns.

The racks follow the smokehouse note's proposal: about 250 fish a space, 2 spaces holding 500, made with withies and a timber.

| Kind | Room | Racks | Holds | Craft | Risk |
|---|---|---|---|---|---|
| **wattle smoke hut** | **a hut room of 2 spaces** (proposed: a third of a small wattle room): **1 timber, 10 withies, 130 straw, 2 units**, basic | **4 withies, 1 timber, 2 units** (2 spaces) | **500 fish** | none | burns with its batch (as now); wears as wattle |
| **timber smokehouse** | a small timber room as proposed above (14 timber, 2 stone, 10 withies, 400 straw, 8 units), carpenter | racks in tiers, 2 sets: each **6 withies, 2 timber, 3 units** on 2 spaces, holding **375 fish a space** (x1.5 for tiers, est.) | about **1,500 fish** on 4 spaces, with 2 spaces to work and hang in | carpenter | seldom burns; wears as timber |
| **stone smokehouse** | a small stone room (30 stone, 4 timber, 400 straw, 40 units), mason | as timber: 2 tiered sets | about **1,500 fish** | mason | seldom burns; a hard cure's long cold smoke ([[D2-271 Smoking in three depths|D2-271]]) |

How these sit against the stores and works on the same scale:
- the hut at 2 units with racks at 2 is about a tenth of a field's fence in work;
- a timber smokehouse (8 units and about 18 timber with its racks) is between a timber-lined cellar under a cottage (6 units) and a
  dry-stone wall (20 units);
- a stone smokehouse, at 46 units with its racks, is about two walls.

This is the order [[D2-271 Smoking in three depths|D2-271]] means: the hard cure, which travels, is the costly one.

**The hut room is new.** ROOMS has no room smaller than 6 spaces. A "hut" of 2 spaces (wattle only) is needed for the smoke hut, and
would also serve a store hut or a hen-house. It costs the room table one row; `room_cost` reads it as it does the others.

**Whether the room costs in general need the same correction: yes.**
- Wattle against timber is wrong for every building, not only the smokehouse. A wattle cottage today takes the wood of a timber one,
  and that hides the real choice between them: wattle is cheap, burns and wears; timber is dear, needs a carpenter, and lasts.
- Correcting it puts withies and straw in demand. That gives the materials network its biggest buyer: a cottage takes about 30
  withies, three times a weir section.
- It also makes the upgrade costs (`upgrade_cost`, wattle to timber) mean something.
- What changes in committed worlds is only what they build after the change. Seeded buildings are given, not paid for.

---

## Sources

Search summaries only; fetches were blocked (penelope.uchicago.edu, buildingconservation.com).

- Grain storage, pits: [Reynolds, Butser underground grain storage (tDAR)](https://core.tdar.org/document/414463/a-general-report-of-underground-grain-storage-experiments-at-the-butser-ancient-farm-research-project); [Experimental Iron Age storage pits (PPS)](https://resolve.cambridge.org/core/journals/proceedings-of-the-prehistoric-society/article/experimental-iron-age-storage-pits-an-interim-report/45BEF896B38038D91BACC82C7E02EC3F); [Underground storage in NE Iberia (Antiquity 2019)](https://resolve.cambridge.org/core/journals/antiquity/article/from-the-earliest-farmers-to-the-first-urban-centres-a-socioeconomic-analysis-of-underground-storage-practices-in-northeastern-iberia/9B3BB34552AF141E2776EB0F43158F47); [Danebury pits (Cunliffe, ADS)](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-281-1/dissemination/pdf/RR073a_Danebury_vol4.pdf); [Grain Storage in Iron Age Britain (LacusCurtius; via search)](https://penelope.uchicago.edu/Thayer/E/Journals/LacusCurtius/Grain_Storage_in_Iron_Age_Britain%2A%2A.html); [FAO grain storage](https://www.fao.org/4/s1250e/S1250E0w.htm)
- Medieval storage: [Claridge and Langdon 2011 (LSE)](https://researchonline.lse.ac.uk/id/eprint/101317); [Barns, granaries and security (JMH 2023)](https://searchworks.jioinstitute.edu.in/articles/edb__174192338); [Winchester carryover (Nash)](https://deirdremccloskey.com/docs/graham/nash.pdf); [Storage and threshing in preindustrial Europe (Tools and Tillage)](https://digi.ub.uni-heidelberg.de/diglit/tools_tillage1988_1991/0125); [Threshing (Wikipedia)](https://en.Wikipedia.com/wiki/Threshing); [Harmondsworth Barn (English Heritage)](https://www.english-heritage.org.uk/visit/places/harmondsworth-barn/history/); [Country Life on great barns](https://www.countrylife.co.uk/?p=192124); [Dyer, how carpenters built medieval England](https://www.medievalists.net/2025/11/how-carpenters-built-medieval-england/); [Briggs, manorial court roll inventories](https://www.medievalists.net/2011/02/manorial-court-roll-inventories-as-evidence-for-english-peasant-consumption-and-living-standards-c-1270-c-1420/)
- Arks and chests: [V&A ark](https://api.vam.ac.uk/v2/object/O130488); [Shakespeare Birthplace Trust grain ark](https://www.shakespeare.org.uk/explore-shakespeare/blogs/shakespeare-100-objects-grain-ark/); [ckbk on arks](https://app.ckbk.com/section/cook18873c07s001)
- Granaries: [Staddle stones (Wikipedia)](https://en.wikipedia.org/wiki/Staddle_stones); [NPTA staddle stones](https://www.npta.org.uk/straddle-stones/); [Historic England, Smewhins granary](https://historicengland.org.uk/services-skills/education/educational-images/granary-at-smewhins-cottage-shottesbrooke-berkshire-3339); [Roman farming (Wikipedia: Varro, Columella)](https://en.wikipedia.com/wiki/Roman_farming); [Pliny XVIII.73](https://peterburk.github.io/pliny/ChaptersHtml/18.%20Book%20XVIII.%20The%20Natural%20History%20Of%20Grain./73.%20Chap.%2073-The%20Methods%20Of%20Storing%20Corn..html)
- Cellars: [Wright, Some thoughts on cellars (Triskele 2025)](https://triskeleheritage.triskelepublishing.com/2025/07/15/mediaeval-mythbusting-blog-30-some-thoughts-on-cellars/); [Well Wood, Aylesford (Kent Archaeology)](https://www.kentarchaeology.org.uk/journal/126/medieval-site-well-wood-aylesford); [Leicester undercroft (ADS)](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-4493-1/dissemination/2010_84/2010_84_117-149_kipling.pdf); [Norwich undercrofts (ADS)](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-3749-1/dissemination/pdf/vol_37/NorfolkArchaeology37_P19_P55.pdf); [UAF root cellars](https://www.uaf.edu/ces/publications/database/food/vegetable-storage.php); [Root cellar (Wikipedia)](https://EN.wikipedia.com/wiki/Root_cellar); [How deep should a root cellar be](https://engineerfix.com/how-deep-should-a-root-cellar-be/)
- Digging, walls, hurdles: [ILO productivity norms](https://www.academia.edu/7463085/PRODUCTIVITY_NORMS); [Manpower norms](https://www.scribd.com/document/339269703/Manpower); [HS2 archaeology rates](https://learninglegacy.hs2.org.uk/document/managing-occupational-health-risks-in-archaeology); [Conservation handbooks, dry stone walling](https://conservationhandbooks.com/?p=548); [Low Impact, dry stone wall](https://www.lowimpact.org/how-to-build-or-repair-a-dry-stone-wall/); [Fine Homebuilding, dry stone walls](https://www.finehomebuilding.com/project-guides/foundations-and-masonry-work/building-dry-stone-walls); [Radnorshire Society, hurdles](https://radnorshiresociety.org/?p=2339); [Farmers Weekly, hurdles](https://www.fwi.co.uk/arable/orders-pour-in-for-traditional-hazel-hurdles); [Woodlands blog, hurdles](https://tom2.woodlands.co.uk/?p=436)
- Baskets, sacks, cloth: [Country Life, the basket-maker](https://countrylife.co.uk/luxury/art-and-antiques/the-secrets-of-the-basket-maker-with-a-basket-you-watch-it-grow-before-your-very-eyes-224653); [UMD basket making](https://extension.umd.edu/agnr.umd.edu/sites/extension.umd.edu/files/2021-03/RES_05BasketMaking.pdf); [Nottingham, volumes and capacity](https://nottingham.ac.uk/manuscriptsandspecialcollections/researchguidance/weightsandmeasures/volumes.aspx); [Bushel (Wikipedia)](https://en.Wikipedia.com/wiki/Bushel); [Reading MERL sacks](https://www.reading.ac.uk/adlib/Details/collect/2614); [Munro, medieval textile statistics](https://www.economics.utoronto.ca/munro5/MedTextileStats.pdf)
- Pots: [Ashmolean PotWeb, size](https://potweb.ashmolean.org/NewBodleian/07-Size.html); [Amphora (unit)](https://Www.wikipedia.org/wiki/Amphora_(unit)); [Medieval Ceramics 1989](https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-5456-1/dissemination/1989/MedievalCeramics_1989-13_3-8.pdf)
- Barrels and salting: [Imbibe, the master cooper](https://imbibemagazine.com/the-craft-of-the-master-cooper/); [Munchies, a Napa cooper](https://munchies.vice.com/en_us/posts/getting-blazed-with-a-napa-valley-master-cooper); [Cooper (Wikipedia)](https://en.wikipedia.org/wiki/Cooper_(profession)); [UKY stave bolts](https://publications.mgcafe.uky.edu/sites/publications.ca.uky.edu/files/for9.htm); [Hogshead (Wikipedia)](https://en.wikipedia.org/wiki/Hogshead); [Fordham glossary, herring barrel](https://memp.ace.fordham.edu/?p=702); [FAO salted fish](https://www.fao.org/4/x5898e/x5898e01.htm); [Baltic herring salting (journal.fi)](https://journal.fi/afs/article/download/71305/33102/95388); [Salting (food) (Wikipedia)](https://Www.Wikipedia.org/wiki/Salt_meat); [Civil War Talk, salt pork](https://civilwartalk.com/threads/salt-pork.123976/); [Townsends, salt pork](https://www.townsends.us/blogs/blog/preparing-salt-pork)
- Smoke, bacon: [Colonial Williamsburg smokehouses](https://research.colonialwilliamsburg.org/Foundation/journal/Winter04-05/smoke.cfm); [Florilegium, medieval bacon](https://florilegium.org/files/FOOD-MEATS/Medvl-Bacon-art.html); [Researching food history, bacon racks](https://researchingfoodhistory.blogspot.com/2020/09/bacon-racks-held-soap-paper-bags-of.html); [Earthworm Express, Henderson's smokehouse](https://earthwormexpress.com/bacon-and-the-art-of-living/chapter-10-02-01-robert-henderson-and-the-invention-of-the-smokehouse/)
- Hay, clamps, wood, ice: [Measuring a haystack (Papers Past 1929)](https://dynamic-rsnz.natlib.govt.nz/newspapers/SNEWS19290111.2.29); [Taylor and Francis, stack volumes](https://www.taylorfrancis.com/books/9780080937878/chapters/10.4324/9780080937878-12); [ISO 5525 potato clamps](https://cdn.standards.iteh.ai/samples/11581/adf7ae95b7c44844b41b2d2c58b0badf/ISO-5525-1978.pdf); [Crook 1950, potato storage (Rothamsted)](https://repository.rothamsted.ac.uk/download/149275f7f4bd40f2e428cbee8b2973f7d891083379db05448123c7109a015d3e/5797137/Crook-1950-Studies-on-the-storage-of-potatoes-.pdf); [Manitoba Co-operator, potato storage](https://www.manitobacooperator.ca/crops/potato-growers-battling-storage-woes); [Cord (unit)](https://wikipedia.com/wiki/Cord-foot); [The Chimney Sweep, wood weights](https://hearth.com/articles/chimneysweep/howood.htm); [Ice house (Wikipedia)](https://en.wikipedia.org/wiki/Ice_house_(building)); [Monticello ice house](https://www.monticello.org/encyclopedia/ice-house); [Scotchtown ice house](https://preservationvirginia.org/patrick-henrys-scotchtown/scotchtown-ice-house/); [Hancock Shaker ice house](https://mass.historicbuildingsct.com/?p=6685)
- Vermin: [FAO, other storage pests](https://www.fao.org/4/X5048E/x5048E0f.htm); [FAO, rodent pests](https://www.fao.org/4/x5065e/x5065E0j.htm); [IRRI, of rice and rats](https://ricetoday.irri.org/of-rice-and-rats/); [UNL CropWatch, vertebrate pests](https://cropwatch.unl.edu/part-i-protecting-your-harvest-vertebrate-pests-unl-cropwatch-june-14-2012); [Maine ICWDM, mice](https://apps.web.maine.gov/dacf/php/gotpests/othercritters/factsheets/mice-ICWDM.pdf); [Mus musculus in stored wheat (AGRIS)](https://agris.fao.org/search/fr/records/6471cc8a77fd37171a6fa5cd); [NC State, mice](https://content.ces.ncsu.edu/biology-behavior-of-common-structure-invading-mice); [Cats vs rats (ZME Science)](https://zmescience.com/science/news-science/cats-vs-rats-nope-03102018); [Biodiversity Council on farm cats](https://biodiversitycouncil.org.au/resources/are-cats-important-to-farm-operations-to-protect-equipment-from-rodents); [Black rat in Britain (Antiquity)](https://www.cambridge.org/core/journals/antiquity/article/rattus-rattus-the-introduction-of-the-black-rat-into-britain/DC79D9061B47BE2E4080A6184D516245); [Black rat DNA (York 2022)](https://york.ac.uk/news-and-events/news/2022/research/black-rat-europe)
- Densities: [Engineering ToolBox, bulk densities](https://engineeringtoolbox.com/foods-materials-bulk-density-d_1819.html)
