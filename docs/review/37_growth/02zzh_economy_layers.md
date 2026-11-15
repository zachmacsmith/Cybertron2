# 02zzh: the economy's layers and trees of dependence, across the domains (14 Nov 2026)

> **Superseded in part (15 Nov):** §2's single four-rung ladder is replaced by shapes and paradigm switches in
> [proposals/economy_web.md](../../cybertron2/proposals/economy_web.md). The rest stands as analysis.

Zach (14 Nov): "a deep dive into the different potential layers of the economy and fleshing out the connections ... what would the
ladders (or more like trees) and the different trees of dependence be? How do these unlock more things, more complex economies and
societies? What is the relation to labour v capital intensive? Connect to the different domains we have like hunting or farming or
fishing or building or travel."

This is an analysis to design from, not a proposal: nothing here is decided. It builds on the economy map (02zzg: 63 goods, 59 acts,
read from the engine's tables on `peoples-worlds` at 2020b9e) and the conversation of 13 to 14 Nov (purposes, substitutes, skill in
processing, the test for adding a good). Costs quoted from the engine are its current values.

## 1. The shape: layers of transformation

Every good sits at a depth: how many transformations stand between it and the land. Each transformation needs some mix of seven
things, and which of them it needs decides what kind of economy forms around it.

| Needs | What it means | Engine today |
|---|---|---|
| **labour** | units of work per output | `units` on every act |
| **skill** | yield, quality, speed, waste; slow to learn | per-technique skill and levels (D2-52); the hunt's own curve (4c) |
| **tools** | multiply labour; wear; made by other chains | bare / crude / copper factors on acts |
| **capital** | fittings and buildings without which a step cannot be done, or not at scale | `at: fittings` (hearth, anvil, millstones, water wheel, oven, cellar) |
| **energy** | heat, animal or water power | fuel inputs (timber, charcoal), oxen for the plough, the river for the wheel |
| **time** | days of waiting or tending; years for land and trees | crops growing; the rack's 3 nights; buildings over days |
| **place** | where it can be done | covers (forest, rock, water, saltmarsh); the river for the wheel |

The layers (a good may skip one):

| Layer | What happens | Mostly needs | Examples |
|---|---|---|---|
| **L0 the land and the living** | sources | place | fields, woods, rock, water, herds, wild kinds |
| **L1 getting** | harvest, extract, catch | labour, place, crude tools | grain, timber, firewood, stone, ore, meat, hides, fish, withies, bark |
| **L2 first processing** | one material made usable | skill, a simple fitting, time | meal, charcoal, dried meat, leather, cord, boards, lime |
| **L3 making** | several chains combined into a thing | tools, skill, inputs from several L2 chains | metal tools, harness, nets, bows, barrels, carts, boats, a stone house |
| **L4 shared capital** | large fixed works, many users, tied to a place | capital, crews, maintenance | the water mill, the oven, the weir, the smokehouse, tan yards, kilns, roads and fords, the deer park, the fishpond |
| **L5 institutions** | what the deeper layers demand and enable | people agreeing | trades and apprenticeship, rents for using capital, credit for building it, rules for commons, tolls at chokepoints, markets |

**Where the engine is now:** L0 to L2 are broad; L3 is thin (about ten made things); L4 exists only in farming (mills, oven) and
metal (anvil), with the weir and smokehouse designed (brief 5); L5 is the agreements system, coin and households. Most goods are
one step from the land and one from being eaten (02zzg).

## 2. Labour against capital

**In engine terms:** a labour-intensive method spends many units per output and little else (fishing by hand, gathering, hoeing,
the quern). A capital-intensive one spends goods once, on a fitting, a tool or works, and then much less labour per output (the
water mill: 250 units and 60 timber, 20 stone and 2 copper once; then 200 grain a batch for 2 units, against the quern's 3 grain a
unit). Time is a third kind: land broken, a coppice on rotation, a hedge grown, a skill learned.

**The core rule: capital pays only above a threshold of demand.** A rung that costs C once and saves s units an output pays after
C/s outputs. A household that grinds for itself never pays back a water wheel; a village does; a region does well. So:
- **small, poor or insecure societies stay labour-intensive**, which is right, and is what the runs show (quern, racks, bare hands);
- **depth unlocks with numbers, surplus, peace and trade**: more people to feed, food to spare for specialists, no raids on the mill,
  roads to bring the grain;
- **shared capital creates leverage**: whoever owns the mill, the weir or the oven sits on a chokepoint, and the others pay, rent,
  queue or fight. That is where institutions come from (L5).

**Every domain has the same four-step ladder**, and the economy is richer when the domains climb it at different paces:

| Step | Farming (in the engine) | The shape |
|---|---|---|
| 1. hands | bare hands (reap x0.6, hoe x0.5, fell x0.25) | labour only |
| 2. a tool | crude tool (1 timber, 0.5 stone) x1; copper tool x1.5 to 2 (copper from ore, charcoal and an anvil) | a tool from another chain multiplies labour |
| 3. power and works | the plough (a wooden plough: 4 timber and 1 copper; 2 harness: hide and timber; oxen); broken ground; manure; fences | animal power and works on the land; ties metal, leather and herds in |
| 4. shared capital | millstones (10 stone, an ox) then the water wheel; the oven (20 stone); the granary and cellar | one owner, many users |

## 3. The trees, domain by domain

Each tree lists its rungs from labour to capital and marks with **→** where it draws on another domain. (E) is in the engine;
(B) is in a written brief; (P) is proposed here or in the conversation; (L) is later.

### 3.1 Fields (farming)
- **Getting:** sow (seed grain) (E); weed, hoe (E); reap with bare hands, a crude tool or copper (E) → **metal**.
- **Power and works:** the plough (E) → **metal** (copper), **leather** (harness), **herds** (oxen); breaking ground (E) turns up
  fieldstone → **building**; manure (E) → **herds** (dung); fences (E) → **woods** (timber; hurdles of **withies** (P)); lime on the
  fields (L) → **minerals**.
- **Processing:** quern (E, labour) → ox millstones (E, capital, → herds) → water wheel (E, shared capital, → river, metal); bread at
  a hearth (E) → oven (E, capital) → **fuel**; malt and ale (L) → fuel, water, **containers**.
- **By-products:** straw (E) → beds, thatch (L), fodder; bran and spent grain (L) → pigs and cattle.
- **Storage:** bins (E) → granary (E) → cellar (E) → **building**.

### 3.2 Herds (cattle now; other beasts with K6)
- **Getting:** milk (E), slaughter (E), dung (E), traction (E: the plough, the pack ox).
- **Works:** stalls (E), fences and folds (E; hurdles of withies (P)), hay meadows (E), hedges (L, K7).
- **Processing:** **butchering with skill** (P): meat, a leather-grade hide, tallow, offal as food, bone and antler; cheese (E: milk,
  salt, a cellar) → **salt**, **building**; butter (L).
- **By-products into other trees:** hide → **leather**; tallow → **light**; dung → **fields**; oxen → **fields**, **travel**.
- **Kept beasts (P, K6):** hens (eggs), the cat (stores), the dog (guarding, hunting, herding), later pigs (pannage → **woods**),
  sheep (wool → cloth, L).

### 3.3 Woods
- **Getting:** fell with an axe (E: bare x0.25, crude x1, copper x2) → **metal**; firewood and brushwood (E).
- **Time capital: the coppice** (P): hazel, willow and oak cut on a rotation of years, giving **withies** (P), **poles**, **bark** (P)
  and charcoal wood. A coppice is capital in time: worthless if cut too often, rich if kept.
- **Processing:** charcoal (E, 5 timber → 1 charcoal at a forest) → **metal**, smoking; boards in a saw pit (L) → **making**; cleft
  oak into staves (L) → barrels; bark → **leather**.
- **Other claims on the woods:** pannage for pigs (L), deer and boar (**hunting**), the lime kiln and salt pans' fuel (L). The woods
  are the most contested commons.

### 3.4 Rock, clay and minerals
- **Getting:** quarry stone (E, mason), mine copper ore (E, miner), dig clay (L).
- **Processing:** smelt ore with charcoal at the anvil (E) → copper; lime burned in a kiln (L) from limestone and a lot of fuel;
  pots and tiles fired in a kiln (L).
- **Sinks:** stone into hearths (4), cellars (4), ovens (20), millstones (10), the water wheel (20), stone rooms (30 to 150) (E);
  copper into tools, coin, the plough (E); lime into mortar, tanning and fields (L).

### 3.5 Metal
- **Tree:** ore (rock) + charcoal (woods) + an anvil (6 stone, **2 hide**, 1 timber: the bellows' leather is already in the
  recipe as raw hide) (E) → copper → tools, plough, coin (E); spear and arrow heads, hooks, a saw (P, L).
- **Why it is the deepest tree:** it draws on three domains (rock, woods, herds) and feeds every other domain's tool rung. Metal is
  the economy's multiplier on labour.

### 3.6 Wild: hunting and gathering
- **Gathering (E):** the wild plant foods; consolidate to a few kinds that differ in keeping (P).
- **Hunting rungs:** bare hands → club (E: 1 timber) → copper-headed spear (P → **metal**) → bow (P: a stave → **woods**, a string of
  **cord** (P), arrows of poles, feathers and heads → **metal**, **fowl**); set gear: snares and nets (P → **cord**); dogs (P →
  **kept beasts**); parties and a led ox (E → **herds**); works on the land: rides, high seats, pits (L, K7); the deer park (L:
  a pale → **woods**).
- **Processing:** butchering with skill (P), as for herds; the carcass and decay (E).
- **Raiders (E):** pressure on **fields**, **stores** and **herds**; answered by **watching** (labour), fences and walls
  (capital), dogs (kept beasts), and the cat and the owl hole (stores).

### 3.7 Water: fishing and the river
- **Fishing rungs:** by hand (E) → line and hook (P: a rod of a pole; a line of **cord**; hooks of **bone** → hunting and herds, or
  **copper** → metal; bait of offal) → wicker traps (P → **withies**) → nets (P → **cord**) → boats (L: a coracle of **leather** and
  **withies**; a punt of boards) → the weir (B: stakes and wattle, a crew; shared capital with a downstream take) → the fishpond (L,
  K6: digging and a sluice).
- **Processing:** gutting with skill (P); salting (E → **salt**); smoking (B: the smokehouse → **fuel**); fish oil for lamps (P).
- **The river's other users:** the water wheel (E), tanning and retting (P, L: they foul the water below), ferries and fords
  (travel). The river is contested along its length.

### 3.8 Building
- **Walls:** wattle (E: 8 timber; with **withies** and daub (P, L) instead) → timber frame (E: timber and some stone, a carpenter) →
  stone (E: 30 to 150 stone, a mason; with lime mortar (L)).
- **Roofs:** thatch of straw or reed (L) → shingles of cleft oak (L) → tiles (L → **clay**, kiln).
- **Fittings** are where every other tree's capital lives: hearth, oven, anvil, millstones, water wheel, granary, cellar, bins,
  stalls, woodshed (E); tan pits, smoke racks, a lime kiln, a malting floor (P, L).
- **Building is the sink** that turns surplus into lasting capital. It is also where fire, wear and abandonment destroy it (E:
  shelter levels).

### 3.9 Travel and transport
- **Rungs:** on foot (E: carry 10) → a pack (E: hide and timber; +10) → the pack ox (E: 60, → **herds**, **leather**) → the cart
  (L: a wheelwright, boards, an iron tyre, **grease**; only on a track) → boats and ferries (L → **water**).
- **Works:** tracks and roads (E: some roads have tracks), fords and bridges (L), camps and lodging (E).
- **Why it matters for depth:** place-bound inputs (limestone here, clay there, salt on the coast, oak bark in the old woods) only
  become a regional economy if they can be moved. Transport is the tree that turns local chains into trade.

### 3.10 Keeping food
- **Rungs:** eat fresh → dry on a rack (E, 4c) → smoke (B: the smokehouse) → salt (E: salt; with barrels (L)) → a cool cellar (E).
- **It ties together** salt (a regional chokepoint), fuel, containers and building, and it decides how much of a glut (a slaughter,
  a run, a harvest) becomes food over the winter.

### 3.11 Light and fat (later; OPEN L-107)
- **Rungs:** the hearth's glow → rushlight (E: tallow; with rushes from wetland (L)) → tallow candle (L: a wick of cord) → beeswax
  (L, K6 bees) → oil lamp (P: fish or linseed oil).
- **Fat's other sinks:** soap (fat with lye from **wood ash**, a by-product of every hearth), grease for axles, harness and the mill.

### 3.12 Exchange
- **Rungs:** barter (E) → coin (E: copper at the anvil) → agreements, credit and rent (E: D2-31 to D2-39) → markets (L).
- **Capital needs it:** a water wheel costs 250 units; only credit, shared labour or a lord gets one built. Rent for using shared
  capital (the mill's multure, the weir's share) is the first institution the deeper layers demand.

## 4. Where the trees cross

| Hub (good or place) | The trees it ties together | Today |
|---|---|---|
| **fuel**: firewood, timber, charcoal, later peat | heat, cooking, metal, smoking, lime, pottery, salt boiling, malting | firewood, timber, charcoal (E) |
| **the coppice**: withies, poles, bark | building (wattle), fences and folds, fishing (traps, the weir), hunting (shafts, rods), leather (bark), charcoal | missing |
| **leather** | farming (harness), metal (bellows), travel (packs, saddles), water (coracles), storage (bags, buckets) | raw hide stands in |
| **cord** | fishing (lines, nets), hunting (snares, bowstrings, nets), building (lashing), wells | missing |
| **metal edges** | every tool rung: fields, woods, rock, hunting heads, fishing hooks | copper (E) |
| **containers** (barrels, sacks, baskets) | keeping (salt meat and fish), ale, carrying, grain storage | bins and granary only |
| **lime** | building (mortar), leather (tanning), fields (fertility) | missing |
| **water** | the mill, fishing, tanning, retting, malting | the river and the wheel (E) |
| **herds' by-products**: hide, tallow, dung, bone | leather, light, fields, hooks and handles | hide, tallow, dung (E); bone (P) |
| **labour time and skill** | everything; the scarcest input in every run | units and skill (E) |

**The conflicts these crossings create**, which are what make the deeper economy social:
- **the river:** the mill and the weir want the water held; fish want it clean while tanning and retting foul it; the village below
  wants the run the weir takes (brief 5);
- **the woods:** charcoal, building timber, the coppice's rotation, pannage, game, the lime kiln and the salt pans all want them;
  over-cutting ruins the coppice and drives off the deer;
- **the land near the village:** field, pasture and building ground compete; the peoples run built over its pasture and fenced the
  common into barley (37.4's run, 13 Nov);
- **the chokepoints:** salt, ore, limestone, the mill site, the ford.

## 5. How depth unlocks a more complex society

Each mechanism below needs the layers above: none of it can appear while every good is one step from the land.

1. **Division of labour.** A deeper chain has more steps that reward skill (the tanner, the smith, the collier, the net-maker, the
   miller). Skill is slow to learn (4c's pace), so specialists form, and with them dependence between households.
2. **Dependence between places.** Inputs tied to place (limestone, clay, ore, salt, oak bark, a river for the wheel) make villages
   need each other. Transport decides whether that becomes trade or stays a lack.
3. **The surplus ladder.** A specialist eats food someone else grew. Every layer added needs a larger food surplus per head to
   support it, so depth rises with farming's productivity (the plough, the mill) and falls back in a famine, as the peoples run
   showed.
4. **Capital and inequality.** Shared capital (the mill, the weir, the oven) is built by some and used by many; rent, access and
   control create the first lasting differences between households, and the first disputes worth an institution.
5. **Coordination.** Crews (the weir, a drive, a harvest, raising a hall) and commons (woods, river, pasture) need agreements,
   rules and enforcement: the material for institutions acting on each other (the 37 growth packages).
6. **Long horizons.** A coppice on rotation, a hedge growing, broken ground, a fruit tree, an apprentice learning: investments that
   pay over seasons or years ask the agents to plan beyond the next meal.
7. **Risk and keeping.** Preservation, storage and salt let a household carry a glut through the lean season, and turn food into
   something that can be lent, so credit and insurance appear.
8. **Knowledge that travels with people.** Methods are known by upbringing, watching and teaching (D4-24, 4c §3.3), so a deep economy
   is also a map of who knows what, and losing a master loses a rung.

## 6. Keeping it within the engine's abstractions and the agents' load

From the conversation of 14 Nov:
- **Add a good only if** it changes a decision, ties a chain to a place, skill or capital, fits the existing acts and fittings, and
  connects what exists or gives a dead end a use.
- **People see only the methods they know** (D4-24), so a deeper economy adds lines only for those who practise it: the tanner's
  household sees tanning; others see leather offered.
- **Containers are fittings or carrying gear with a property, never items holding items.** Tools stay in tiers. Quality comes
  from skill's yield, not grades on goods. Processes over days share one mechanism (a batch in a fitting over nights, with tending).
  Small by-products fold into recipes.
- **Consolidate as we add**, so the count of goods stays roughly flat.

## 7. A staged path

| Tranche | Adds | Ties together | New decisions it creates |
|---|---|---|---|
| **1. materials** | butchering and gutting with skill; **leather** (hide, bark, tan pits, time); **bark**; **withies** (the coppice); **cord** (bast, nettle); **bone and antler**; **fur**. Consolidations: the wild plant foods, wild food, eels as fish, castoreum, offal as food | herds, hunting, woods, building, fishing, metal (bellows), travel (packs) | tan or sell the hide; cut the coppice now or let it grow; who becomes the tanner |
| **2. gear on the materials** | the line and hook, wicker traps and nets (fishing); the spear and the bow, snares of cord (hunting); kept beasts (hens, the cat, dogs) | hunting, fishing, kept beasts, metal | which gear to make or trade for; who keeps the hounds |
| **3. capital on the water and in keeping** | brief 5: the weir, the run, the smokehouse; barrels as a store fitting; salt pans burning fuel | water, keeping, fuel, salt, between villages | open or shut the gap; build a smokehouse or rent one |
| **4. deeper food and building** | malt and ale; lime (mortar, fields, tanning); clay (daub, pots, tiles); saw pits and boards | fields, rock, woods, building | brew or eat the grain; build in stone with mortar |
| **5. cloth, carts and light** | flax, hemp and wool into cloth; the wheelwright and carts on tracks; candles, soap and grease | fields, herds (sheep), travel, light | when clothing and evening acts return |

**Measures that would show depth working**, read against a null arm:
- the longest chain used in a run;
- the number of distinct specialists (households doing most of one L2 or L3 step);
- trades of intermediates between households and between villages;
- shared capital built and rented;
- disputes over the river and the woods.

## Sources

02zzg (the economy map and its data); the conversation of 13 to 14 Nov (purposes and substitutes, skill in processing, the test
for adding goods); engine tables on `peoples-worlds` at 2020b9e (TECHNIQUES, FITTINGS, ROOMS, ITEMS); water_and_preservation.md;
river_and_water.md (brief 5); hunt_calibration.md (brief 4c); 02zv (the packs); 38.70 (the peoples run); D2-31 to D2-39, D2-52,
D4-24, D4-102.
