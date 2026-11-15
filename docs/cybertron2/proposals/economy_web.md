# The economy as a web of chains of different shapes

**Status:** discussion (15 Nov). Nothing decided or built.
**Owner:** 37.2 (design). The economy's code and much of its spec are 37.4's; parts that touch them are proposals to 37.4 and Zach.
**Affects:** spec/economy/ (production, goods, buildings, transport); spec/environment/ (wildlife, resources); data.py (ITEMS,
TECHNIQUES, FITTINGS, ROOMS); the wild pack's data; briefs 5 onward.

## Summary

The engine's economy is mostly one step deep: 63 goods, most of them one act from the land and one from being eaten (02zzg). This
proposes a web of about fifteen chains that interlock, each with its own **shape**, so that working out which shape you are in
(when to invest, trade, specialise, wait or share) is part of what people have to navigate.

It replaces the single four-rung ladder of 02zzh §2 (Zach, 14 Nov: "having 4 ladder rungs is a terrible idea"). Instead:
- some ways of meeting a need are **shallow** (one way, a skill that plateaus);
- some **accrete**: separate improvements adopted one at a time, in any order;
- some **switch paradigm** at a threshold of capital, demand or knowledge, and the switch changes who does the work and how
  people are organised (hand baking to the village oven; the quern to the mill; hunting the wild to a deer park).

## 1. Shapes a chain can have

| Shape | What it is | What it asks of people |
|---|---|---|
| **shallow** | one way, learned fast, a low ceiling | nothing to plan; a fallback anyone has |
| **accretive** | improvements adopted one at a time, each paying alone, combinable | which to add first, given what one has |
| **paradigm switch** | past a threshold, a different way altogether, usually shared and specialist | gather the capital or the crew; who owns it; rent |
| **substitutes with trade-offs** | several ways, each better at something | choose by purpose, not by tier |
| **joint products** | one act gives several goods | the by-products decide whether it is worth doing |
| **assembly** | one thing needs several chains at once; the scarcest input limits it | find the bottleneck; trade for it |
| **chokepoint** | no substitute: access or trade | dependence, tolls, control |
| **long skill** | slow to learn, a high ceiling | specialists, teaching, apprentices |
| **time capital** | invest now, paid back over seasons or years | patience; restraint; rights over the future |
| **pulse** | supply in a glut at one time | capacity to keep, not to get |
| **commons** | value depends on others' use | rules, disputes, cooperation |
| **increasing returns** | cheaper per unit the more it is used | a single centre, sharing, rent |

A chain usually combines two or three. **The design rule:** the web's chains should differ in shape, and a new chain earns its
place partly by adding a shape or a combination the world lacks.

**Paradigm switches deserve their own rule.** A switch is not a better tool; it changes the social form:

| Need | Household paradigm | Switches to | What changes |
|---|---|---|---|
| flour and bread | the quern and the hearth (E) | the mill and the village oven (E), a miller and a baker | one centre, a rent (the miller's share), bread as a traded good |
| meat from the wild | hunting the wild (E, 4c) | the deer park or the warren (L) | keeping instead of catching; a fence to build and guard; rights in game |
| fish | by hand, line, traps (E, P) | the weir (brief 5), then the fishpond (L) | a crew, a structure, a downstream cost; keeping fish |
| wild plant food | gathering (E) | gardens and orchards (L) | land set aside; years to bear |
| fuel | cutting what one finds (E) | the coppice on rotation (P) | restraint and rights over years |
| cord | gathering bast or nettle (P) | flax on a field, retted in water (L) | land taken from grain; water fouled below |
| carrying | on foot, a pack (E) | the pack ox (E), then carts on tracks (L) | beasts and roads; carriers as a trade |

## 2. The web

Each chain: its need, its shape, how it is done, what it takes from other chains (**←**), what it gives them (**→**), and what it
binds to a place or a person. (E) in the engine; (B) in a written brief; (P) proposed here; (L) later.

### 2.1 Grain to bread *(paradigm switch, increasing returns, a pulse at harvest)*
- **Household:** reap (E) → quern (E: 2 stone) → meal for porridge; bread at a hearth (E: 10 flour a batch).
- **Village:** ox millstones (E: 10 stone, an ox) or the water wheel (E: 60 timber, 20 stone, 2 copper, 250 units, a river) →
  flour; the oven (E: 20 stone, 100 bread a batch) → bread for many.
- **←** stone (rock), timber and fuel (woods), oxen (herds), copper (metal), the river (water).
- **→** bread and flour to everyone; bran and straw to herds and building.
- **Binds:** the mill to the river; the miller and baker as trades; a rent for using them.

### 2.2 Tillage and fertility *(accretive, time capital)*
Separate improvements, each paying alone: breaking ground (E), manure (E: dung), the plough (E: assembly of a wooden plough, two
harness and oxen), fences and hurdles (E; hurdles of withies (P)), lime or marl (L). No order is forced.
- **←** dung and oxen (herds), harness (leather), copper (metal), withies (coppice).
- **→** grain, straw; fieldstone turned up (building).

### 2.3 Herds *(time capital, joint products)*
- Breeding (E), milk (E), traction (E), dung (E), slaughter (E).
- **Paradigm:** grazing loose (E) or herded and folded, with stalls and hay through winter (E). The switch pays when winters kill
  or land is short.
- **→** milk (cheese, with salt and a cellar (E)), traction (fields, travel), dung (fields), the carcass (butchering).
- **←** hay (meadows), pasture (land), salt (cheese), withies (folds).

### 2.4 Butchering and gutting *(joint products, long skill)*
- The step after any kill or slaughter (P). Skill decides how much meat, whether the hide is whole, and what by-products are kept:
  meat, hide, tallow, offal (food, bait, dog food), bone and antler.
- **←** herds, hunting, fishing; a knife (the tool tiers).
- **→** food (keeping), hide (leather), tallow (light), bone and antler (hooks, handles), offal (bait, dogs).

### 2.5 Leather *(assembly, time)*
- Hide + oak bark + water + weeks in **tan pits** (a fitting) → leather (P). One paradigm; better with skill.
- **←** hide (butchering), bark (coppice or felled oak), water (a river or pond).
- **→** harness (fields, travel), packs (travel), the **anvil's bellows** (metal: the anvil takes leather where it takes hide now),
  later coracles (water).
- **Binds:** tan yards to water and oak woods; the tanner as a trade; fouled water below (water).

### 2.6 The coppice *(time capital, joint products, commons)*
- **Paradigm switch:** from cutting the wood as one finds it (E) to a coppice on rotation (P): a woodland parcel cut in panels, each
  left for years. Cut too often, it yields less; kept, it gives every year.
- **→** **withies** (P: wattle walls, hurdles, fish traps, the weir, baskets), **poles** (charcoal, rods, shafts, stakes), **bark**
  (P: leather), brushwood (fuel).
- **Binds:** rights over a wood across years; the most contested commons.

### 2.7 Fuel *(substitutes with trade-offs)*
| Fuel | Good for | Bad for |
|---|---|---|
| firewood, brushwood (E) | gathered anywhere | bulky; low heat |
| timber (E) | dense heat in a house | competes with building |
| charcoal (E) | smelting and smithing; light to carry far | wasteful for heating a house |
| peat (L) | where there is no wood | cut in summer, dried for weeks |

- **→** heat and cooking (everyone), metal, smoking, lime and pottery (L), salt pans (L).
- **←** the woods and the coppice; bogs (peat).

### 2.8 Metal *(assembly, chokepoint, long skill)*
- Ore (E: a seam) + charcoal (E) + bellows of leather (P) + an anvil (E) → copper (E) → the smith → tools, plough, coin (E); spear
  and arrow heads, hooks (P).
- **←** ore (rock: a chokepoint), charcoal (fuel), leather (bellows), stone and timber (the anvil).
- **→** every tool tier: fields, woods, rock, hunting, fishing, building.
- **Binds:** villages without ore to those with it; the smith as the deepest trade.

### 2.9 Cord *(shallow, then a paradigm switch)*
- **Shallow:** gather bast (lime) or nettle (P): anyone, slow, weak cord.
- **Switch (L):** flax on a field → retting in water → spinning → strong cord in quantity. It takes land from grain and fouls water
  below.
- **→** nets, snares, fishing lines, bowstrings (hunting, fishing), rope (wells, lashing), later cloth.

### 2.10 Hunting *(long skill, joint products, commons; paradigm switch to keeping)*
- **Hunting the wild** (E, 4c): skill from x1 to x8; a party; a led ox. Gear: the club (E), a copper-headed spear (P), the bow (L:
  a stave, a cord string, shafts, feathers, heads).
- **Set gear** (E, P): snares and nets of cord.
- **Dogs** (P, kept beasts).
- **Switch (L):** the deer park (a pale round a wood) or the warren: keeping instead of catching.
- **←** metal, cord, poles, dogs, oxen; the game (a commons with wariness and slow recovery).
- **→** the carcass (butchering); fur (trade, later warmth).

### 2.11 Fishing *(a pulse on a commons; paradigm switch to fixed works)*
- **By hand** (E) → **line and hook** (P: a pole, cord, hooks of bone or copper, bait of offal) → **traps** (P: withies) and **nets**
  (P: cord) → **switch:** the weir (B: a crew-built structure taking a share of every run, the village below getting less) →
  the fishpond (L).
- **←** cord, withies, bone or metal, offal.
- **→** fish (keeping), fish oil (light, P).
- **Binds:** villages along a river to each other.

### 2.12 Keeping food *(substitutes by how long; made necessary by pulses)*
| Way | Keeps | Needs |
|---|---|---|
| eaten fresh | days | |
| the rack at a hearth (E, 4c) | weeks | a hearth; any batch up to 8 |
| the smokehouse (B) | months | its own building, fuel, tending once a day |
| salting (E) | longest | **salt** (a chokepoint); barrels (L) |
| the cellar (E) | slows all | stone |

### 2.13 Building *(substitutes with trade-offs; where capital is sunk)*
| Walls | Cost | Risk |
|---|---|---|
| wattle and daub (E; withies (P)) | cheap, quick | burns; wears fast |
| timber frame (E) | middling; a carpenter | burns |
| stone (E; lime mortar (L)) | dear; a mason | lasts; fireproof; warm |

Fittings host every other chain's capital: hearths, ovens, the anvil, millstones, the water wheel, granaries, cellars, tan pits,
smoke racks.

### 2.14 Travel *(thresholds)*
On foot (E: 10) → a pack (E: +10; leather (P)) → the pack ox (E: 60; harness) → carts on tracks (L) → boats (L). Fords and bridges
(L) as works. **It turns place-bound chokepoints into trade.**

### 2.15 Exchange and the institutions the web demands
- Barter, coin, agreements and credit (E).
- **Rents for shared capital:** the miller's share, the oven fee, the weir's take, the smokehouse's hire.
- **Credit to build a threshold work.**
- **Rules for commons:** the coppice's rotation, the river's gap and its foul water, the game.
- **Tolls at chokepoints:** the ford, the salt, the ore.

## 3. Where the chains cross

| Hub | Fed by | Feeds |
|---|---|---|
| **withies and poles** (the coppice) | woods | building, fields (hurdles), herds (folds), fishing (traps, the weir), hunting (shafts), fuel (charcoal) |
| **leather** | herds and hunting (hides), woods (bark), water | fields (harness), travel (packs), metal (bellows), water (coracles) |
| **cord** | the wild (bast, nettle), later fields (flax) | fishing, hunting, building, wells |
| **charcoal** | woods | metal, smoking, carrying fuel far |
| **metal edges** | rock, fuel, leather | every tool tier |
| **the carcass's by-products** | herds, hunting, fishing | leather, light, hooks, dogs, bait |
| **salt** | coasts and brine | keeping, cheese |
| **the river** | | the mill, the weir, tanning, retting; each harms another |
| **the woods** | | the coppice, timber, charcoal, game, pannage |

**Conflicts the web creates on purpose:**
- **upstream against downstream:** the weir's take, and tanning and retting fouling the fish;
- **the woods' many claims:** cutting now, or the coppice's years;
- **land near the village:** fields, pasture, flax and building ground;
- **who owns the thresholds:** the mill, the oven, the weir, the park.

## 4. Why I think this would work

1. **No village is self-sufficient:** ore, salt, limestone, oak bark, a river for the mill and good flax land are spread across a
   region, so trade and dependence come from the land.
2. **Every chain has a floor anyone can reach:** gathering, the quern, the club, hand fishing, bast cord. Nobody starves for want
   of a chain. Climbing is a choice that pays only with numbers, surplus and peace.
3. **The switches create institutions:** each paradigm switch makes a shared work, a specialist and a rent, which is what the
   society needs to argue about.
4. **The shapes differ, so choices differ:** a bottleneck to find (assembly), patience (time capital), storage (pulses),
   restraint (commons), the right scale (increasing returns).
5. **Few new goods:** leather, bark, withies, cord, bone and antler, fur, then flax and peat later; consolidations remove about as
   many (02zzh §6).
6. **It fits the engine's abstractions:** goods in stores, acts with inputs and fittings, tool tiers, one mechanism for
   batches over nights, and containers as fittings or carrying gear rather than items holding items.
7. **It stays within what agents can hold:** people see only the methods they know (D4-24); the tanner's household sees tanning,
   the rest see leather offered.

## 5. Staging

| Stage | Adds | Shapes it brings in |
|---|---|---|
| 1. materials | butchering and gutting with skill; leather and tan pits; bark; withies and poles from a coppice; cord from bast and nettle; bone and antler; fur; consolidations; the anvil, harness and pack taking leather; wattle taking withies | joint products, assembly, time capital, a commons |
| 2. gear and kept beasts | line and hook, traps, nets; the spear; snares of cord; hens, cats and dogs as beasts | accretive, long skill |
| 3. water and keeping | brief 5: the run, the weir, the smokehouse; barrels as a store fitting; salt pans burning fuel | pulse, paradigm switch, chokepoint |
| 4. land deeper | flax and retting; peat; lime; malt and ale; the bow | paradigm switch, substitutes |
| 5. later | cloth (with clothing), carts on tracks, candles and soap, the deer park and warren, gardens and orchards | thresholds, keeping instead of catching |

## Why

Zach, 14 to 15 Nov: "the economy itself should have a heterogeneous shape"; "there should potentially be different paradigms for
different things ... it could be a lot more shallow, or maybe you iterate and add new things, or maybe you completely switch
paradigms after a certain capital amount"; "design a web of interconnected economy". The runs show the gap: hides, tallow and antler
unused, dried meat rotting at doors, villages never reaching a resource two days away (02zze, 38.70).

## Alternatives considered

- **One ladder of rungs for every domain** (02zzh §2): uniform and predictable; nothing to navigate.
- **Adding every historical intermediate** (02zzh §3): realistic, but too many goods and acts for agents, and many would be leaves.
- **Leaving the economy shallow and deepening society only through institutions:** institutions then have little to be about.

## Open questions (for Zach)

1. Stage 1 as the next economy brief, with the kept beasts brief beside it?
2. The coppice as a parcel state with a rotation (time capital), or as a wood's yield of withies and bark with no rotation?
3. Rents for shared capital (the miller's share) as an engine rule, or left to agreements?

## History

- 15 Nov 2026: written by 37.2 at Zach's request ("Write up these types of chains and design a web of interconnected economy that
  you think would work well"), replacing 02zzh §2's single ladder with shapes and paradigms.

## Sources

02zzg (the economy map), 02zzh (layers and trees), the conversation of 13 to 15 Nov; engine tables on `peoples-worlds`;
water_and_preservation.md; river_and_water.md; hunt_calibration.md; 02zv; 38.70.
