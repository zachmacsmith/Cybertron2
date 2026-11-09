# 02zu: chains, capital and actions; decay and scavenging (9 Nov)

> **Superseded in part (9 Nov):** consolidated in [02zv_wild_consolidation.md](02zv_wild_consolidation.md), whose ledger places every item here in a pack, a deferral or a proposed cut; where they differ, 02zv holds, and the build brief for the first stage is [proposals/methods_and_encounters.md](../../cybertron2/proposals/methods_and_encounters.md). Withdrawn readings are listed in 02zv §3.9 (among them: real-day conversions of acts, the attention budget, institutions written into the wildlife).

The fourth outside note, after 02zr (behaviour), 02zs (development) and 02zt (dependences). Zach asked for four things: (A) supply
chains and progression across a society's core needs and qualities, as one economy; (B) labour against capital; (C) a deep dig into
actions (verbs, techniques, skills, modifiers, gear) and how to generalise them; and (D) carcasses, bodies, food and decay as
scavenging. It is a session note: it proposes, it decides nothing.

**Rules that hold throughout.** Nothing social is forced (the engine gives physical substrate; any rule people make is theirs). No
bespoke one-kind checklists (responses are general, transferable and improvable). Perception is never filtered. **Time:** a unit is
a part of one in-game day, and acts are told as one day (forays.md; Zach, 9 Nov): acts are not converted into real days. The
ecology's own rates stay on the engine's clock: a year is 32 engine days, a season 8. Where earlier notes (02zr, 02zs, 02zt) said a
unit stands for about two real days, that reading is withdrawn (§E).

## 0. Findings in brief

1. **One economy, a few shared hubs.** Every core need (food, keeping, warmth, shelter, light, clothing, tools, carrying, water,
   health, records, defence, fertility, power) runs through a handful of hubs: **the field, the herd and its carcass, the wood and
   its coppice, water, the quarry and seam, salt, fuel, the smith, the store.** Wild things enter mostly as inputs to these hubs
   (bark, withies, fat, hides, feathers, wax, fish, game, dung) and as threats to them (pests at the field and store, predators at
   the herd). Fuel is the most contested input: hearths, smoking, rendering, salt-boiling, lime-burning, charcoal for the smith and
   burning carcasses all draw on the same woods (Part A).
2. **Food is the binding chain and must stay under 30% of actions;** the other chains are what slack is for. Wild chains add things
   worth wanting beyond food (light, leather, wax for seals, feathers for arrows, bedding), which is what husbandry.md §6 said the
   bottom of the economy lacked.
3. **Every need has a labour way and a capital way.** Watching every night or a wall; carrying on the back or a cart; hand-picking
   or a rotation; snaring by hand or a line of traps left set; grinding by hand or a mill. The transition happens when there is
   **surplus** to spend on building, **stored materials**, **tools that make tools**, **specialists**, **scale**, and above all
   **durable things that keep working while no one is there** (Part B).
4. **The engine already has the seeds of capital** (fences that hold herds each night, field works, mills, granaries, stalls, wear on
   tools, upkeep on fences). What it lacks is a general **standing work**: a thing at a place that acts each night by its own
   properties without a person (a trap, a set net, a weir's traps, a hive, a warren, a dovecote, a smokehouse batch), checked and
   emptied by whoever comes. With condition, upkeep, capacity, depreciation and possession, capital then truly substitutes for
   labour, and its trade-offs (who can afford it, dependence on makers, inheritance, theft) arise physically.
5. **The action system is already general at its core and bespoke at its edges.** One handler (`_technique`) serves `gather` and
   `work`, reading each technique's data; but it branches on about twenty **yield kinds**, six of them wild one-offs (`wild_take`,
   `wild_site`, `wild_shut`, `wild_guard`, `wild_watch`, `wild_forage`), and the ecology branch adds about twenty kind-named
   techniques. The verbs drifted from the designed 24 to 38 plus 18 event words (verbs.md; review 38.37). The bespoke parts are where
   kinds and situations leaked into the grammar (Part C).
6. **A robust general design is possible** with three moves: (a) keep about two dozen verbs as kinds of change; (b) make every
   `gather` and `work` an object of **method + target (optional, in the person's words) + place or route + gear + party**, resolved
   by **one encounter rule** that matches the method's and gear's properties against the target's traits (02zs §8.1); (c) let
   **standing works** carry capital. Kind-specific code then lives only in the animals' own modules (D2-203), never in the verbs.
7. **The hard cases pass** (a sounder's routes, a flock's following, a run with a lag, bee-lining, a decoy pond, a carcass with
   scavengers, a warren, forays, kept populations, processing, building): each is a method with properties, a structure, a standing
   work or an animal module, with no kind named in the verbs (§C.5).
8. **What the prompt should show** is the grammar once, the methods the person knows (with the gear in hand) as ways of doing,
   the places it knows with what it remembers of them, and results that say what physically happened. No menu of kind-by-kind acts;
   refusals and results teach. **New methods should enter as known-but-limited** (seeded by upbringing, gated by materials, makers
   and capital) for the common medieval methods, and **learnt** (taught, watched, tried) for specialist ones (Part C).
9. **Decay and scavenging is one rule over all organic things** (Part D): a thing's mass, its stage (fresh, ripe, putrid, dry,
   bones), the conditions that speed or slow it (heat, wet, flies, cold, frost, burial, salt, smoke, cover), and what it emits to
   each sense; scavengers come by their own traits (senses, diet by stage, boldness near people, range, time of activity), in an
   order that real carcass studies support (birds by sight first in daylight; ravens most frequent at large carcasses and recruiting
   others; foxes, badgers, boar, dogs, wolves and bears by scent at night; flies and beetles always, most in warmth; vertebrates take
   more in cold months when insects are few). People's handling (butcher, hang, bury, burn, feed to dogs or pigs, salt, smoke, carry
   home, leave) changes what comes, what disease travels, what evidence remains and what danger waits, with no custom forced.

## Part A. Supply chains and progression across the core qualities

### A.1 Each core quality, its chains, its progression, and where wild things enter

"Now" means in the engine or decided; "developed" means reachable by building, making, keeping or learning. Steps are rungs, not
eras: a society can be on different rungs for different needs.

| Quality | Chains now | Chains as a society develops | Steps of progression | Where wild things enter | Shares or competes with |
|---|---|---|---|---|---|
| **food: grain** | sow, reap, thresh; flour at millstones or a mill; bread at a hearth or oven (D2-60, D2-61) | rotations, fallows grazed, manure and dovecote dung; field works; the master farmer; seed selection; irrigation later | hoe, then plough with an ox; hand mill, then water mill; bread at a hearth, then an oven | pests at sowing and harvest (birds, boar, deer, slugs, grubs); dung from dovecotes; bone meal | land (pasture, wood, warren); labour; oxen (draught); fuel (bread) |
| **food: animal** | milk and meat from cattle; slaughter; dried meat (D2-62); cheese with salt (D2-47) | pigs on mast; sheep; poultry and eggs; fishponds; warrens; dovecotes; hunting with hounds and bows | hunt, then keep, then breed (02zs §3.1) | game, fish, fowl, eggs; bridges (boar to pig; greylag to goose) | pasture; the mast (D2-202); fodder; salt |
| **food: fish and water** | fishing by hand, rod (water pack) | traps and the weir; nets; boats; ponds; smoked and salted fish | hand, rod, traps, weir, nets and boats | eels, salmon, trout, lampreys, crayfish, fowl | the river (mill, weir, crossing); withies; salt; fuel |
| **food: wild plants** | ten plant kinds as parcel stocks (D2-200 to D2-202), gathering, leaching acorns | tended hedges, nutteries, orchards; drying and storing nuts | gather, tend, plant | everything here is wild | the mast and nuts are shared with boar, deer, squirrels, jays, mice (D2-202) |
| **food: sweet** | none | honey from wild bees, then skeps | find bee trees, keep swarms, keep apiaries | wild bees | wax (light, seals) |
| **salt** | an item with no source (D2-56, not built) | shore pans; boiling at a spring | sun-dried, then boiled with fuel | none directly; it preserves every wild take | fuel; carriage (one source a region) |
| **preservation and storage** | bins, cellar, granary fitting; drying meat; salting fish; decay by condition (D2-87, DECAY) | smokehouse batches; barrels; raised stone granaries on staddles; ice later | eat fresh, dry, salt, smoke, store securely | every pulse (runs, drives, freezes' fowl, the slaughter); store pests (rats, mice, weevils, moths) | salt, fuel, stone, the cooper |
| **warmth and fuel** | timber, firewood, charcoal in heat (D2-157); hearths, fire rings, fires in the open; shelter ladder (D2-159) | coppice rotations; peat; charcoal carried far | gather dead wood, cut young growth, fell, coppice, burn charcoal | woods shared with game; bracken and gorse as fuel; peat with fen life | every other fuel use (smoking, rendering, salt, lime, smelting, burning carcasses) |
| **shelter and building** | rooms by structure (wattle, timber, stone), fittings, capacity, upkeep; clearing for building | stone and storeys; specialised tools (felling axe for great beams, mason's chisels) | camp, wattle, timber, stone | thatch (reeds, heather), wattle (withies), lime, hides for tents; lodgers that eat the fabric (beetles, jackdaws) | timber, stone, the mason, the carpenter |
| **light** | the fire; the watch's light must be a thing the state holds (02zq one-off 1); no light good yet | rushlights (rushes and fat), tallow candles, horn lanterns, wax candles, oil | fire, rushlight, candle, lantern | fat from game and herds; wax; horn; rushes from wet ground; seal and fish oil | fat (food), wax (seals) |
| **clothing and textiles** | parked (D2-10) | leather, furs, wool, flax and hemp cloth | skins, then leather, then spun cloth | furs and skins; down and feathers for bedding | flax and hemp land; sheep pasture; the tanner |
| **tools and metal** | crude and copper tools, specialised tools (D2-48), weapons, traps (decided, not built), harness, saddle; copper mined and smelted with charcoal | iron (charcoal heavy), bronze (tin by trade) | crude, copper, then iron or bronze (02j) | hide strips, sinew, glue, horn and antler handles, feathers for arrows | charcoal (the coppice), the smith |
| **transport and carrying** | on foot 10, pack 20, pack ox 60, handcart 40 on a track (D2-135, D2-136); ox cart later (L-53) | carts, wagons, boats, roads, inns | foot, pack, beast, cart, boat | harness and packs from hides; bulk takes and light dear goods to carry | oxen (ploughing), fodder, roads |
| **water** | drawing water; a mill's wheel; fords | wells, leats, irrigation (later), ponds | carry, well, channel | fish, fowl, eels; beaver dams; retting fouls water downstream | the river (mill, weir, fishing, crossing, irrigation) |
| **health** | wounds exist, care is a technique (`care`); no illness yet (Q-16) | remedies, healers, herbs | none, then herbs, then healers | herbs, castoreum, leeches; disease from carcasses and water; poisonous plants | knowledge |
| **knowledge and records** | teaching, watching, practice (D2-52), awareness and know-how (D4-24); documents decided (D2-24), writing on buildings (D2-169) | parchment, wax seals, goose quills; tallies, year-books, maps | tell, teach, write, keep | hides (parchment), wax (seals), feathers (quills), oak galls (ink) | the hunter, herder and beekeeper |
| **defence** | `guard`, the night watch's cost (D2-21), fences and walls (D2-130), doors, dogs as a fitting | walls, folds, kennels, weapons, bows | watch, fence, wall, fortify | the same barriers and dogs serve against beasts and people | timber, stone, the smith |
| **fertility** | dung from cattle (built), manure as a stage (D2-11) | folding sheep, dovecote dung, bone meal, marl | none, then dung, then folding and dung bought | pigeon dung, bone, ash from burning | beasts, carcasses |
| **power and traction** | oxen (plough, cart), water wheel (built), hand mill | more beasts, horses (L-36), windmills later | hand, beast, water | none (dogs pull small carts in some places) | fodder, the river |
| **containers** | bins, cellars, stores (fittings); packs from hides | barrels (the cooper), baskets (withies), sacks (cloth), pots (deferred) | heap, bin, basket and barrel | withies, hides | timber, the coppice |
| **cordage and adhesives** | none | bast cord, sinew, hemp; hide and bone glue | none, bast, sinew and hemp | sinew, gut, glue from hides and bones; bast from lime trees | the coppice, the carcass |
| **exchange and money** | offers and agreements, copper coin (D2-28), prices witnessed (D2-29) | markets, ledgers, merchants | barter, coin, credit | light dear wild goods carry value far (furs, wax) | |
| **time and calendars** | seasons, daylight units, markers (built) | almanacs and year-books people keep | memory, sayings, records | markers by warmth; the year's wild events | |
| **sanitation and waste** | rotting things have signs, no health effect yet (D2-96) | middens placed, offal buried or fed to pigs, latrines | none, then placement, then works | scavengers (kites, crows, rats, dogs, flies); disease | the store and the well |

### A.2 The whole-economy map

Roots are what the land offers; hubs are where many chains meet; end uses are what people need. Arrows read "feeds".

```
ROOTS                     HUBS (shared by many chains)                       END USES
-----                     ----------------------------                       --------
field  ---------------->  GRAIN, STRAW --------------------------------->  food; fodder; bedding; skeps; thatch
pasture, meadow -------->  THE HERD (cattle; later sheep, pigs, poultry) -->  milk; draught -> transport, ploughing
                               |                                             dung -> fertility -> field
                               v
                          THE CARCASS (also every wild take) ------------->  meat -> food (fresh, dried, salted, smoked)
                               |  fat -> tallow -> light; grease               hide -> leather -> harness, packs, gear
                               |  bone -> glue, tools, bone meal               hide -> parchment -> documents
                               |  sinew, gut -> cord, bowstrings               horn -> lanterns (light), handles
                               |  offal -> dogs, ferrets, hawks, bait          antler -> handles, tools
wood ------------------>  THE WOOD AND ITS COPPICE ----------------------->  timber -> building, carts, ploughs, tools
                               |  withies -> traps, hurdles, baskets, wattle  firewood, charcoal -> FUEL
                               |  poles -> fences, pales                       bark -> tanning (leather)
                               |  bast -> cord -> snares, nets                 mast, nuts -> pigs, people, game
                               |  cover -> game; danger                        yew -> bows
water, fen ------------>  WATER --------------------------------------->  fish, eels, fowl, reeds (thatch), peat (fuel)
                               |  power -> mill; crossing; boats -> transport
quarry, seam ---------->  STONE, LIME, COPPER ---------------------------->  walls, granaries, hearths; mortar; tanning;
                               |                                             tools, coin (via THE SMITH)
shore, spring --------->  SALT ---------------------------------------->  preservation; cheese; hides
                          FUEL (from the wood, peat, bracken) ------------->  hearths; smokehouse; rendering; salt-boiling;
                                                                             lime-burning; smelting; burning carcasses
                          THE SMITH (copper or iron, charcoal) ----------->  tools, weapons, traps, nails, hoops, heads
                          THE STORE (bins, granary, cellar, barrels) ------>  every food through the year; pests at it
                          KEPT ALLIES (dogs, cats, ferrets, hawks, geese) ->  guarding, hunting, ratting, watching
bees (wild, kept) ----->  HONEY, WAX ---------------------------------->  food; seals (documents); candles (light)
```

**Shared hubs and what competes for them:**

| Hub | Many chains draw on it | What competes | What it means |
|---|---|---|---|
| **fuel** | hearths (cooking, warmth), smoking, rendering, salt-boiling, lime-burning, charcoal for smelting, burning carcasses | every heat use against the near wood's renewal (forests.md: a near wood is a commons that can collapse) | the scarcest shared input in a growing village; peat and charcoal move it; burning a carcass costs everyone's fuel |
| **the wood** | timber, fuel, withies, poles, bark, bast, mast, cover, game, yew | felling against coppicing against pannage against game cover | one parcel, many incompatible uses; the land ladder's trade-offs (02zs §5.4) |
| **the carcass** | food, light, leather, writing, cord, glue, tools, dogs' food, fertility | eating it fresh against rendering, tanning, feeding the kennel | the butcher step decides; spoilage and scavengers take what is not used (Part D) |
| **the herd** | milk, draught, dung, meat, hides, wealth | ploughing against carting against carrying (an ox that carries is not ploughing, transport.md) | draught is a bottleneck before carts |
| **land** | fields, pasture, meadow, wood, warren, park, pond, orchard | each against the others (Boserup's intensification: more output per area at more labour) | enclosure and conversion are the long-run choices |
| **labour** | everything | food at most about 30% of actions (scenario_design §4) | capital (Part B) is what frees labour for other chains |
| **the river** | fishing, the weir, the mill, the crossing, boats, irrigation, retting | each blocks or fouls another | a physical commons between upstream and downstream |
| **salt** | every preserved good, cheese, hides | one source a region; carriage | the long-distance hub |
| **the smith** | every tool, weapon and trap | metal and charcoal | the chokepoint economy_plan.md names |

### A.3 How it fits together
- **Feeds:** the herd feeds the field (dung) and the field feeds the herd (straw, hay, grain); the wood feeds the smith (charcoal),
  the tanner (bark), the trapper (withies) and the hearth; the carcass feeds the chandler, tanner, glue-boiler, kennel and scribe;
  the store feeds everyone through the year and feeds the pests; salt and fuel turn every glut into a store.
- **Competes:** fuel among all heat uses; the wood among its uses; land among its covers; draught between field and road; the river
  among its works; labour among all chains (food first).
- **Shares inputs:** withies and poles (traps, hurdles, baskets, fences, wattle walls); fat (food and light); hides (gear, leather,
  parchment, harness); stone (stores, walls, hearths, folds).
- **Develops together:** a village that climbs the processing ladder (smokehouse, salt, barrels) makes the eel run and the fen's fowl
  worth more; one that climbs the defence ladder (stone stores, hedges, kennels) frees labour from watching; one that climbs
  transport makes far grounds and wild trade goods worth gathering. Climbing one ladder raises the value of the next.

## Part B. Labour against capital

### B.1 The labour way and the capital way, need by need

| Need or family | The labour way | The capital way | What makes the change happen | What then works without a person |
|---|---|---|---|---|
| **grain at the field** | hoe; reap by hand; watch at night | plough and ox; field works; hedges and banks | surplus to feed an ox through winter; a smith for the share; a hedger | the hedge (each night), the ditch (each wet spell) |
| **grain to flour** | hand mill (every house has one: 38.57's lesson) | water mill (built), millstones | a river site; a millwright; enough grain in the catchment (economy_plan: a mill for 25 to 70 people) | the wheel, while water runs |
| **keeping food** | eat fast; guard the store; pick over the grain | bins, raised stone granary on staddles, cellar, barrels, smokehouse, salt | stone and a mason; salt; a cooper; a glut worth keeping | the granary (each night, against rats and damp); salted goods (each day, against decay) |
| **warmth** | gather dead wood daily (84 firewood a hearth a year, forests.md) | fell timber with a good axe (21 a year); charcoal carried; a coppice in rotation | a metal tool; a woodsman; a coppice cut on its cycle | the coppice regrows by itself; a store of timber |
| **shelter** | a camp each night | a house that lasts with upkeep | timber, stone, labour pooled | the house, each night, with upkeep |
| **light** | the fire | rushlights, candles, a lantern | fat to spare; a horner or chandler | a lantern burns while the watcher works |
| **tools** | bare hands; crude tools remade | copper or iron tools; specialised tools (D2-48) | a smith and metal; tools that make tools (the smith's own anvil, chisels for millstones) | none act alone; they multiply work |
| **carrying** | on the back (10) | pack (20), pack ox (60), handcart (40 on a track), ox cart (later) | an ox, a harness from a hide, a track cleared | the cart carries what a person cannot; the track lasts |
| **water** | carry it | a well, a leat, a channel | a crew; stone | flow, each day |
| **defence (people and beasts)** | guard nightly (D2-21: the night's sleep, more food, tired next day) | walls, gates, folds, a kennel of guard dogs | stone and labour; dogs fed | the wall and the fold each night; dogs each night |
| **knowledge** | tell again and again | written methods, tallies, year-books | parchment, a scribe, literacy | the document, read by anyone later |
| **take (wild)** | stalk and snare by hand each day | traps and nets left set on a line; a weir with traps; a decoy pond; a warren | cord, withies, iron later; the weir's crew; earthworks | the trap, the set net, the weir's traps and the warren take each night |
| **exclude** | turn beasts back by hand; shut the door | hedges, banks, walls, pales, mesh-tight coops, raised stores | materials and specialists; time (a hedge grows a year) | the barrier, each night |
| **guard** | a watcher all night | a kennel; geese; a lookout; walls that remove the need | dogs bred and trained; a building | dogs and geese each night |
| **reduce at source** | pick slugs; dig an earth by hand | a line of traps; terriers and ferrets; cats; a paid catcher's round | traps; kept beasts; a specialist | traps and cats each night |
| **keep** | catch young and tend them by hand | warren, dovecote, pond, apiary, park, kennel, mews | earthworks, stone, timber; stock | the kept population grows each night within its structure |
| **manage** | decide each time | rotations and coppice cycles kept as practice and records | records, a woodward | the cycle, once set, needs only its cutting |
| **process** | eat fresh; dry a little at the hearth | smokehouse batches, tannery pits, rendering, barrels | fuel; salt; the cooper; the tanner | the batch cures over days; the tan pit works for months |

### B.2 Is there a natural transition, and what drives it?
Yes, and it has the same drivers everywhere:
1. **Surplus.** Capital is labour spent now for returns later; only a household or village with food to spare can spend days on a
   wall, a weir or a warren. Food under 30% of actions (scenario_design §4) is the room for it.
2. **Stored materials.** Timber, stone, withies, cord and hides must exist in quantity before building: a woodpile and a quarry
   are capital that make capital.
3. **Tools that make tools.** The smith's anvil, the mason's chisels, the felling axe, the billhook and the net-maker's needle make
   the capital goods that replace labour elsewhere (D2-48's specialised tools repay a full-time specialist in weeks).
4. **Specialists.** A hedger, mason, smith, cooper, tanner, weir-builder or dog-breeder does the capital work far better than a
   household (skill by practice, D2-52); without them capital is costly and poor.
5. **Scale.** A hedge round many fields, a mill for a catchment, a weir across a river, a kennel for a hamlet: capital is lumpy, and
   pays only above a threshold of use (economy_plan's layers only a society can afford).
6. **Durability that works unattended.** The decisive property: a thing that keeps working while nobody is there (a wall each
   night, a set trap, the weir, the mill's wheel, a hive) frees the person for other chains. A thing that needs a person present
   (a decoy pond's decoyman, a smokehouse's tender, a cart's driver) multiplies labour but does not replace it.

### B.3 The converters: three kinds
| Kind | What it does | Examples | What it needs to be real in the engine |
|---|---|---|---|
| **works unattended** | acts each night or each day by its own properties with no one present | fences, hedges, walls, pales, folds, coops (exclude); granaries, cellars, salted and smoked goods (keep); traps, snares, set nets, a weir's traps, fish traps (take); warrens, dovecotes, ponds, hives (keep); the mill's wheel; a coppice's regrowth | a **standing work**: a thing at a place with properties, condition and capacity, resolved each night by the general rules (the encounter rule, decay, renewal); checked and emptied by whoever comes (possession is whoever takes) |
| **multiplies a person** | makes one person's units do more | tools, specialised tools, weapons, the bow, nets in hand, draught beasts, carts, dogs and hawks on a hunt, boats | goods with grades, wear and gear properties; beasts led as tools (D4-58) |
| **removes a recurring need** | makes a daily act unnecessary | stone stores (no guarding against rats), walls (no herding against straying), a well (no carrying water), a lock (no watching a door), records (no retelling) | the need itself must be physical and recurring (the watch's cost, D2-21; carrying water), so removing it is a gain |

### B.4 What the engine needs so capital really substitutes for labour
1. **Durable things with condition and upkeep.** Built: fences and fittings wear and are mended (D2-130, D4-103 phase 2, D4-114's
   yearly clock); tools wear on one scale (recipes.md §9). Needed for the rest: traps, nets, weirs, hives, warrens, pales and coops
   with condition that falls by use and weather, and mending as work.
2. **Standing works that act each night.** A general night step over things at places that have a method (a trap, a set net, a
   weir's traps): each resolves against the populations there by the same encounter rule as a person's take (Part C), puts what it
   takes into itself as a held thing, and can be robbed or emptied by whoever comes. Barriers and stores already act (herds read
   fences; spoilage reads stores); wild groups should read them by properties.
3. **Capacities.** A trap holds one beast; a weir so many traps; a smokehouse a batch; a granary a volume; a warren a number of
   mounds; a kennel a pack. Capacity makes scale a physical choice.
4. **Depreciation and failure.** Condition falls; a broken fence lets beasts through; a neglected warren leaks rabbits; a hedge
   unlaid grows gappy; a weir breaches in a flood. Capital that is not kept up stops substituting.
5. **Possession and inheritance.** Possession is all the engine enforces (D4-23); works on a plot pass with the land (fences.md,
   farming.md's field works); buildings pass with their holders. Capital that outlasts its owner is inherited or fought over by the
   same means as land.
6. **Visibility.** Capital must show: its condition, what it holds, who uses it (signs), so that others can see it, envy it, borrow
   it, rob it or copy it (husbandry.md §6: "it is visible").
7. **Costs felt in labour.** The watch's cost is real (D2-21); carrying is limited by weight; work costs food (labour.py). Capital
   matters only if the labour it saves is felt.

### B.5 Trade-offs that follow
- **Who can afford capital:** the household with surplus, materials and access to specialists; capital raises its return and widens
  the gap (inequality from physics, not rules).
- **Dependence on the maker and the repairer:** a wall needs the mason to mend it, a trap the smith, a weir its crew, a kennel its
  keeper; capital creates lasting dependence edges (02zt §4.1 hubs).
- **Lock-in:** a mill, a weir or a warren fixes a use on a place for years; changing it wastes the capital.
- **Externalities:** a weir takes what would pass downstream; a hedge sends raiders next door; a warren grazes its neighbours; a
  dovecote's birds eat the neighbours' seed (02zs §5.4).
- **Capital outlasts its owner:** it is inherited, sold, claimed or seized; it is a target for raids (a store, a herd, a smokehouse
  batch) and for theft (a trap's catch, a set net).
- **Labour displaced:** those whose labour capital replaces (the watcher, the hand-miller) must find other work or depend on the
  holder of the capital; that is the classic mill story, and it arises here from physics.

## Part C. Actions: verbs, techniques, skills, modifiers and gear

### C.1 What exists (ecology branch and the spec, surveyed 9 Nov)

**The verbs.** `verbs.py VERB` holds 38: accept, admit, attack, build, claim, come, drive, erase, fire, found, gather, give, grant,
guard, host, join, learn, leave_household, make, meet, move, name, order, part, partner, release, rest, revoke, set, sleep, take,
teach, travel, try, watch, withdraw, work, write; plus the night's and the road's choice words (review 38.37: 18 event words). The
designed grammar was 24 (verbs.md), never decided; agent_view.md point 4 would restore it. Rules against swelling exist on paper
(data first; a new verb only for a new kind of change; a coverage test; the count as a decision) and are not enforced.

**The technique record** (data.py TECHNIQUES, about 120 on the branch): `verb` (gather, work, make, build, modifier), `basic`, `at`
(covers, fittings, a building, things), `draws` (a resource), `yield` {kind and its parameters}, `tools`, `weapon` {none, armed},
`wear`, `units`, `gives`, `inputs`, `tags`, `untaught` (tryable or not), `reads_as` (whose signs it reads), `pack`, `trade`, and for
modifiers `modifies`, `key`, `value`, `changes`.

**One handler for gathering and work.** `_technique` serves both: it resolves the technique from the reply's words (`KN.resolve`),
applies modifiers (`MOD.resolve`), finds the site (`_site`: where it is done here, readiness), checks inputs (`KN.shortfall`), draws
skill (`KN.skill` x hunger), the best tool (`here.best_tool`) and a keyed random draw, then **branches on the yield kind**:

| Yield kind | What it resolves | General or bespoke |
|---|---|---|
| `stock`, `pool` | a draw from a parcel stock (plants, fish, dead wood), by skill and tool, with the stock's response | general |
| `chance` | a chance take from a threshold stock (the old `game`), weapon-scaled | general (the old hunt) |
| `fixed` | a fixed amount (quarry, fell), by season | general |
| `clear`, `clear_built` | a project on a parcel | general |
| farming kinds (sow, break, tend, manure, crop, herd, milk, slaughter, works, select, fence, gate) | farm.py acts | general within farming; `fence` and `gate` duplicate `set` and building works |
| `bury`, `mend`, `repair` | work on a body, a fitting, a building | general |
| `wild_take` | a hunt: kinds met in the areas of the range, by numbers, detectability, the technique's per-kind `takes` table, wanted kinds; flight, danger, take; pressure; legends and leaders | **bespoke by data**: the `takes` table names kinds per technique |
| `wild_forage` | wild plants in season | general (by plant data) |
| `wild_site` | a heronry, rookery or lodge: take young, trap, break the dam | **bespoke**: one site kind per technique |
| `wild_shut` | shut house and store for the night | **bespoke**: duplicates `set` on a door |
| `wild_guard` | a guard on a field against a load | **bespoke**: one load per technique |
| `wild_watch` | a night watch over a field with a named scare | **bespoke**: duplicates `guard`; one scare per technique |

**Modifiers** (D2-93, D2-112): `for`, `hidden`, `method: dibble`, `method: cairn`, `searching`, `on trouble`, `stop at`, `gather`
(on travel), `range: near | the wood around | far` (modifying a list of seven wild techniques by name), `how: fine | grand | rich`,
`looking for`. Tryable or not untaught; known ones shown in verb lines (at most 4).

**Knowledge and skill.** Levels: never heard of it, knows of it, a rough idea, capable, long practice (agent_view.md point 3);
untaught tries at the lowest level where tryable; skill by practice (D2-52), fading without practice (labour.py, D4-105); teaching
(`teach`, `learn`), watching (`watch`), trying (`try`); seeded by upbringing (D4-21). **Reading signs by skill:** `perceive.practised`
gives the crafts one practises plus each technique's `reads_as` (a deer stalker reads "hunt" signs), with an `expert:` level past
four fifths of a work's skill; `SKILL_CARRY` passes hunting skill to two wild techniques by name.

**What agents see** (`view: beliefs`, D4-78): the grammar in the system text (the verb manual: about 14,000 characters, with tool
multipliers that agent_view.md wants removed); places as one believes them, with "here one can ..." from the crafts one knows; no
"Today you could"; results and refusals that say what stopped the act (D4-95) and what came from which store (D4-96); a fallback list
(D4-76); standing orders (D4-16; children's, D2-148). **Costs:** units by act (D4-17), work costs food, pushing on costs tomorrow, the
day's walk costs units (labour.py), a night on watch costs sleep and food (D2-21).

### C.2 New kinds of action implied by 02zr, 02zs, 02zt, forays.md and wild_behaviour.md

| Implied act | Where | What kind of change it is |
|---|---|---|
| a foray: a route with an intent, units, party, gear | forays.md | travel through places and gather or look along them (a route is a new referent) |
| take by method (stalk, drive, course, snare, trap, net, shoot, spear, angle, ferret, hawk, decoy, gather young or eggs, dig, line bees) | 02zs §7, §8.2 | gather from a population |
| set a standing work (a trap line, a set net, traps in a weir) and check it | 02zs §4; Part B | build or place a thing with a method; take from a thing |
| guard with what one holds (light, noise, dog, person) | 02zr §3.4, M2 | guard (exists) with gear |
| exclude: a barrier or store with properties; a door state | 02zs §7 | build; set (exists) |
| reduce at source: work a crop against its load; den and burrow work; drive a roost | 02zs §7 | work on a place or a population |
| keep: stock a structure, feed it, harvest it, let it breed, select parents | 02zs §8.3 | work on a kept population |
| train and bond a beast | 02zr F11; 02zs §8.4 | work on a beast over days (a delayed process) |
| butcher a carcass into parts | 02zs §2.4 | work on a thing |
| process (render, tan, smoke, cure) as batches over days | 02zs §8.5; water_and_preservation.md §7 | make at a workplace with a delayed output |
| works on parcels and edges (rides, high seats, tracks, landings) | 02zt §6 | build (a field work) |
| count a herd, a heronry, a warren; keep a tally | 02zt §2.5 | gather information; write (exists) |
| mark an animal or a thing | 02zs §6 (swans) | work on a thing (a mark) |
| name a place | forays.md §5 | name (exists, for tagged things) |
| burn, bury, hang, feed to beasts, leave (a carcass) | Part D | work on a thing; give (exists) |

None of these is a new kind of change except the foray's route. Each fits `gather`, `work`, `make`, `build`, `set`, `guard`,
`give`, `take`, `travel` or `name` with an object.

### C.3 Comparison: how actions have been handled

| Question | Cybertron 1 | verbs.md (designed) | Built now | Proposed here |
|---|---|---|---|---|
| verbs | about 145 actions, one per mechanism (scenario_design; 38.06) | 24, a closed grammar of kinds of change | 38 verbs and 18 event words | about 24, as designed, plus `foray` (or `travel` with a route) |
| how variety enters | a new action | data on verbs: techniques, recipes, blueprints, fittings, settings, powers | data on verbs, plus yield kinds as hidden handlers, plus kind-named techniques | data on verbs: **methods with properties, gear with properties, structures with properties, places and routes**; the yield kinds reduced to a few general resolutions |
| how options are shown | a menu | the grammar; objects by knowledge and place; a budgeted "Today you could" | the grammar and a long verb manual; places with "here one can ..."; no menu under `view: beliefs` | the grammar; the methods one knows and the gear in hand; places as one remembers them; results and refusals that teach |
| how options are learnt | listed | seeded, taught, watched, read, practised | the same, plus untaught tries of tryable modifiers | the same; methods, not per-kind techniques, are what is taught |
| what a skill attaches to | an action | a technique | a technique, with `reads_as` and `SKILL_CARRY` patches | a **method family**, carrying to every target the method takes; readings by skill per method family |
| what gear does | multipliers | tools by method (recipes.md §8) | best tool by technique list; weapon none or armed | gear properties (reach, selectivity, size, strength, noise) read by the encounter rule |
| how kinds are met | random encounters | not designed | per-technique `takes` tables naming kinds | the encounter rule: method and gear properties against the target's traits (02zs §8.1) |

### C.4 The bespoke one-offs, and the general rule each should be an instance of

| One-off | Where | General rule |
|---|---|---|
| kind-named hunts (`stalk deer`, `boar hunt`, `snare hares`, `fowling`, `hunt`, `hunt the wild`) | data.py | `gather` with a method (stalk, drive, snare, net) and optional target words; kinds met by the encounter rule |
| `set eel traps`, `trap beavers`, `fish by hand` | data.py | `gather` with method trap or by hand; traps as standing works |
| `take the young herons`, `take the young rooks` | data.py, `wild_site` | `gather` with method gather young, at any colony |
| `dig out the fox earth` (with its `litter`) | data.py | `work` with method den work at any den or burrow, with terriers and spades as gear |
| `break the beaver dam`, `clear the leat` | data.py | `work` on a water structure (any dam or leat) |
| `shut the hens in`, `shut the gate`, `open the gate` | data.py, `wild_shut`, farming `gate` | `set {thing: door or gate, setting: shut or open}` (exists for buildings) read by every kind's module |
| `watch the field (clapper / dog / fire / horn)` | data.py, `wild_watch` | `guard {where}` with what one holds (gear as deterrents); the night's cost as D2-21 |
| `pick slugs at dusk`, `clear the grubs off the beans`, `top the beans` | data.py, `wild_guard` | `work` on a crop against its loads, with a method by load size |
| `make clappers`, `make a horn` | data.py | recipes (general already) |
| `range: near / the wood around / far` naming seven techniques | data.py modifiers | a foray's units and route, for any take |
| `reads_as` per technique, `SKILL_CARRY` by name | data.py, kinds.py | readings and skill by method family |
| per-kind `takes` tables in hunts | data.py | traits against properties |
| the lantern work and the fire watch's fire | 02zq one-off 1, now `watch` with `burns` | a light is gear with fuel; the watch is `guard` |
| `fire` as its own verb (a fire in the open) | verbs.py | `make` or `build` a fire at a place (a fitting in the open, D2-159), or keep it as a verb if it is a kind of change (warmth at a place) |
| `care` special-cased inside `_work` | verbs.py | `work` with a method on a person (healing as a method family) |
| `fence` and `gate` as farm yield kinds | verbs.py FM_KINDS | `build` a work on a parcel edge; `set` a gate |
| `drive` (a herd) as a verb | verbs.py | `work {what: drive, at: herd}` or keep (a kind of change: moving beasts) |
| `searching` and `looking for` as two modifiers | data.py | one: what one is looking for, on travel, foray or gather |

### C.5 The consolidated design

**Verbs (about 24, as designed).** travel (with a route: the foray), rest, gather, make, build, work, move, give, take, offer,
accept, set, claim, attack, guard, watch, teach, read, write, join, leave, found, conceive, invoke; free: say, tell, note, pin, name.
A new verb only for a new kind of change (verbs.md's rule).

**The object of `gather` and `work` (and `travel` as a foray):**

| Slot | What it holds | Example |
|---|---|---|
| **method** | a known way of doing (a technique of the method kind) | stalk, drive, snare, trap, net, angle, dig, gather young, tend, butcher, smoke, line bees |
| **target** (optional, the person's words) | what one hopes for; read as a preference, never a guarantee | "the hinds", "anything that runs", "the slugs on the beans" |
| **place or route** | a place here, a known place, or a route in words (forays.md) | "Hind Pool", "up the Ashbeck to the falls" |
| **gear** | what one carries or leads | a bow, a net, snares, a dog, a ferret, a lantern, clappers |
| **party** | who goes or works together | "with Wat and the dog" |
| **units** | how much of the day | 3 |
| **for** | whose the output is (D2-37) | the household |

**General rules that hold across every act:**
1. **Cost** in units: the method's base, plus travel by terrain (the day's walk, labour.py), plus what the route takes; work costs food
   (labour.py); a night out or on watch costs as D2-21 and D4-12.
2. **Who can:** anyone who can physically do it with what is at hand (use_by_physics.md, D4-114); know-how sets the level, not the
   permission; untaught methods are tried at the lowest level if tryable (D2-93), refused with a reason if not.
3. **What gear and skill change:** gear contributes properties (reach, selectivity by size, strength, noise, light, scent) that the
   encounter rule reads; skill is per method family and raises the chance and yield; neither is told as a number (agent_view.md).
4. **How it resolves:** **one encounter rule** for every method against every target: the method's and gear's properties against
   the traits of what is there (kinds, things, crops, stocks), with the noticing rule both ways (02zr M1) and keyed randomness. Kinds
   decide where they are and what they do in their own modules (D2-203); the rule decides what meets what.
5. **Standing works:** a method may leave a thing at a place (a set trap, a net, traps in a weir, a smokehouse batch, a fence) that is
   resolved each night by the same rule, holds what it takes, and is emptied by whoever comes.
6. **How results are reported:** as events from state, in order (a line for a simple act; a short story for a foray: forays.md §4),
   saying what physically happened and why it failed when it did ("the hinds winded you: the wind was at your back"; "the net came
   up empty: the birds were on the far field").
7. **How it fails:** physically (nothing there, got away, winded, hurt, trap robbed, net torn), never by a rule; refusal only when it
   cannot physically happen (no gear, no such place, too heavy), with D4-95's messages.
8. **How it is learnt:** methods are know-how (D4-24): seeded by upbringing, taught, watched, read, practised; a method once known
   applies to any target it can take.
9. **How it is read:** signs are read by skill in the method families one practises (`reads_as` generalised): a netter reads the
   flocks, a trapper the runs, a stalker the slots.
10. **How it is seen by others:** every act is an event at its place, seen by the rule; a standing work is a thing others can find.

**The method catalogue (data, not code).** Each method is a row with properties: what it needs of a target (on a run, flocking,
leaving scent, in a burrow, within range and seen, in water, a fixed home it returns to, rooted in a crop), what it is selective for
(size class), what gear it uses and how gear changes it, crew size and its effect (more hands, more noise), danger, units, whether it
leaves a standing work, and the skill family. Kinds carry the matching traits (02zs §8.1). About fifteen methods cover the take
family; a handful each cover exclude, guard, reduce, keep, manage and process.

### C.6 The hard cases

| Hard case | How the general system carries it | Kind-specific code? |
|---|---|---|
| **a sounder's route graph** (02zr M4) | the animal module keeps routes and gaps; people `guard` a place with gear (deterrents), `build` a barrier on an edge (properties: height, strength), or `gather` by drive with a crew; the encounter rule meets the group where its module put it; displacement is the module's response | only in the boar's module |
| **a flock's social following** | the flock's module lands where its kind feeds; people `gather` by net with decoys (gear whose property is "looks like a feeding bird"), or `guard` early in the day; scaring lifts the flock and its module lands it elsewhere | only in the flock's module |
| **a run with a lag** | the run's module moves fish along the river chain with the catchment's lag; people `build` or `set` traps in a weir (a standing work); the night step resolves the traps against what passes; a tally is what people write | none |
| **bee-lining** | a method "follow a line home": its property needs a target that commutes in straight lines to a fixed home (bees; also pigeons to a dovecote or roost, rooks to a rookery, herons to a heronry); one use at a place gives a bearing as a sector of places; two at different places narrow it; the finder remembers the spot | none (the trait is data) |
| **a decoy pond** | a structure (`build`) with properties (pipes by wind, screens); a method "work the decoy" with a trained dog (gear with a bond) that uses the fowl module's response to a fox-like dog; noise nearby (any act with noise) lowers fowl on the pond by the shared perception rule | none |
| **a carcass with scavengers** | a thing with mass and stage; the decay-and-scavenging rule (Part D) brings kinds by traits; people `take` from it (a search, D4-70), `work` butcher, bury or burn it, or `give` it to dogs | none |
| **a warren** | a kept population in a structure (02zs §8.3); `gather` by net with a ferret (gear, a bonded beast) at the warren; the structure's condition decides escape; the edge's grazing is the population's feeding on the next parcels | none |
| **forays** | `travel` with a route in words, an intent and units (forays.md); each leg is walked; along it, takes and finds resolve by the encounter rule with the gear carried; the story is the events | none |
| **kept populations** | `work` on a structure: feed, tend, harvest, select parents (as `select` exists for seed); breeding by the population's own rule | none |
| **processing chains** | `make` with inputs, a workplace and a delayed output (a batch at a fitting over days: smoking, tanning, curing); the butcher step as `work` on a carcass giving parts | none |
| **building** | `build` blueprints, fittings with capacities, and works on parcels and edges (fences, hedges, rides, tracks); upkeep as `work` | none |

### C.7 Is one general system robust?
Yes, on three conditions:
- **Two-sided data.** Kinds carry traits and modules; methods, gear and structures carry properties. Neither side names the other.
  New kinds and new methods then combine without new code.
- **One resolution, with escape hatches as data.** The encounter rule must accept per-pair numbers where physics is lumpy (a
  bear's danger, a heron's wariness), held as data on the kind, never as code in the verb.
- **Kinds' cleverness stays in their modules.** Routes, flocking, runs, caching, habituation and memory live in the animal modules
  behind the animal interface (D2-203); the verbs only place people, gear and works in the world.

**Risks:** the trait-property rule may be too coarse at first (expect calibration rows per kind); the foray interpreter is a model
call with its own error (forays.md tests it); and agents may not discover general methods without a menu (next).

### C.8 What the prompt should show
- **The grammar once** (about 300 tokens), with the object slots in plain words: "gather: how (a way you know), where (a place or the
  way there), with what, with whom, for how long; what you hope for, if anything".
- **The methods the person knows, as ways of doing,** each in a few words of what it is ("snaring: a noose of cord set where beasts
  run"; "netting: a net drawn over birds on the ground, or across where they fly"), at the depth of the person's knowledge
  (agent_view.md point 3), with no yields, multipliers or kind lists.
- **The gear in hand** with what each is (a net, a bow, snares, the dog), not what it is "for".
- **Places as remembered**, with what one saw there and when (forays.md §5; the belief store).
- **Results and refusals that teach physically:** what was met, what happened, why it failed in the world's terms.
- **Not:** a menu of acts; "Today you could"; per-kind techniques; numbers people would not count.

### C.9 How new methods enter a society
- **Known but limited (the default for common medieval methods):** snaring, trapping, netting, stalking, driving, angling, gathering,
  smoking, salting, drying, hedging, fencing are seeded by upbringing to the households whose life would teach them (D4-21); what
  limits them is materials (cord, withies, iron), makers (the smith, the rope-maker), capital (a weir, a smokehouse) and skill.
- **Learnt (specialist methods):** falconry, the decoy, warrening with ferrets, bee-driving, tanning, the bowyer's and fletcher's
  crafts, dog-training are held by few (or by someone elsewhere), and spread by teaching, apprenticeship, watching and documents.
- **Tryable untaught where anyone could think of it** (D2-93): setting a snare, drawing a net, hiding, going quietly; not where it
  takes being shown (training a hawk, tanning).
- **No blind crafting** (knowledge.md §6): agents cannot invent methods by combining words; a world's catalogue is the space, and
  a world may seed fewer methods to make development an experiment (an arm where cord and nets are known by one household only).

## Part D. Carcasses, bodies, food and decay as scavenging

Zach: when cattle die, a person dies, or food rots, these should generally not just disappear; they should be scavenged by
creatures, with natural decay as well (microbes, insects), so that butchering, burying, burning, hanging, storing or leaving
something has different effects, and different wildlife comes at different stages.

**What exists.** A beast that dies leaves a carcass (D4-52; things.py `leave_carcass`): meat by how it died, its hide; fit to eat
about a day (`carcass_fresh_days` 1), bones after about six (`carcass_bones_after` 6). A body shows "dead some days" for about ten
days (`body_days` 10), then bones to the season's end (D2-96); rot has signs and no health effect yet. Goods decay by condition:
open dry or wet, buried, warm, frozen (data.DECAY). A slaughter's signs include crows over the leavings (D4-71). Scavengers were
left for later (D2-95, OPEN L-2). The macro ecology keeps an area's **carrion** stock that halves each season and is eaten by kinds
with carrion in their diets (wild/ecology.py; kinds.py: raven 4, bear 2, fox 1, wolf 1, rats 1, boar 0.5); ravens wheel over an
area with carrion above a threshold (`RAVENS_OVER`).

### D.1 Stages of decay, in engine days

Real carcass decay runs through fresh, bloat, active decay, advanced decay and dry remains [1]; bloat starts within one to four days
in warm weather and may not happen at all in hard cold [1]. With an engine day standing for a stretch of real days in the ecology's
clock, a large carcass passes most of its soft stages **within one or two engine days** in the warm half of the year, while a frost
can hold it fresh for several. Proposed stages (calibrate):

| Thing | Fresh (edible, little smell) | Ripe (smells; flies; still edible to scavengers and dogs; people risk it) | Putrid (stench; maggots; soft parts going) | Dry (skin, cartilage, tough parts) | Bones | Weather and season |
|---|---|---|---|---|---|---|
| **large carcass** (cow, deer, boar) | the day of death | day 1 | day 1 to 2 | days 2 to 6 | from about day 6, lasting a season or more; scattered by scavengers | heat and wet speed it (x1.5); a frost slows it about tenfold (as DECAY's frozen 0.1) and keeps it fresh for days; flies only above a few degrees |
| **small carcass** (hen, hare, rabbit) | the day of death | usually gone overnight to a fox, dog, crow or rat | (in summer, burying beetles may bury it) | | a few feathers and bones | a frost keeps it a few days if nothing finds it |
| **human body** | the day of death | day 1 | days 1 to 3 | days 3 to 8 | after about a season | as a large carcass; on built ground it is found at once by people (D2-96), on roads and in the wild by noticing (D2-4: never announced) |
| **offal and leavings** (a slaughter's guts, blood, a gut pile left in the wood after a kill) | the day | the next day; gone within one or two engine days to birds by day and foxes, dogs, boar by night | | | | in frost, lingers and is found by birds |
| **bones** | | | | | last seasons; gnawed by dogs, foxes, wolves, rodents; deer and sheep chew bones and shed antler for minerals (osteophagy: check) | |
| **spoiled stores**: grain | | damp grain heats and moulds over days | weevils, mites, mould; mice and rats drawn | | | wet and warm speed it (DECAY open_wet 10, warm 1.2) |
| meat and fish | as DECAY | flies and maggots in warmth; dogs, cats, rats, crows if reachable | | | | a frost preserves; salt and smoke stop it |
| fruit | | wasps and flies; fermenting | | | | late summer wasps |
| **the midden** | a stock of refuse and offal added daily | smell by its size and the weather | flies, rats, dogs, pigs, kites, crows always while fed | | | it shrinks only by scavenging and rot |

**What the engine's day should resolve:** a thing's stage advances once a night by its decay rate times its conditions; scavengers
come and take their shares that night; insects and microbes take the rest by temperature. **What lingers:** bones and dry remains
(a trace for seasons), the dark patch where it lay (D4-71's next-day signs), scattered bones where scavengers dragged parts, and in
a burial pit of diseased cattle, the disease for decades (02zr §6 no. 36; anthrax spores persist in soil over a decade [2]).

### D.2 Who comes at which stage, and in what order

Real carcass studies in temperate European woodland found ravens the most frequent visitors to large carcasses (72% of carcasses
in Białowieża), then red foxes (41%) and wolves (29%), with ravens and buzzards commoner on carcasses in the open; wolves
facilitated other scavengers by opening carcasses and leaving remains [3]. In Scandinavia the first arrival at wolf kills differed by
season: foxes in late winter, large birds in autumn and early winter [3b]. Vertebrates took more than half of carrion in cooler
months, when arthropods were few, and less in warm months when insects and microbes competed [4]. Ravens are the most numerous
scavengers at wolf kills in Yellowstone and return to places where kills are common [5].

| Arrives | Kinds | Finds it by | Stage it takes | What it takes | What its arrival does |
|---|---|---|---|---|---|
| **minutes to hours, by day** | crows, magpies, ravens, kites, buzzards (eagles where present) | sight (in the open; less under trees) | fresh to ripe | eyes, soft parts, scraps; small carcasses whole (crows) | **a sign others read**: birds circling and going down (D4-71; 02zr M18); ravens call others and follow wolves; their presence raises every other kind's chance of finding it |
| **hours, in warmth** | blowflies and flesh flies | smell | fresh (eggs) to putrid (maggots) | in summer, insects take a large share of soft tissue | buzzing and maggots as signs; flies carry filth to food and wounds (with illness, later) |
| **the first night** | foxes, badgers (nocturnal), wild boar, village and feral dogs, rats near settlements, martens | smell, carried by the wind and by distance; bolder near people (dogs, rats, foxes) or shyer (boar, badgers) by their traits | fresh to putrid | meat, offal, small carcasses whole; dogs and foxes carry parts away (scattering) | tracks and drag marks; dogs and rats drawn toward the village if the carcass is near houses |
| **nights** | wolves (also as the killers), bears (and a bear **caches** a large carcass and guards it) | smell over long distances; following ravens | fresh to ripe | large shares; the bear covers it and lies up near | danger at the carcass (02zr §4.6); wolves draw ravens and foxes after them |
| **days** | wasps (taking flesh), beetles (carrion beetles; burying beetles on small carcasses), later hide beetles on dry remains | smell | ripe to dry | soft remnants, skin, sinew | |
| **seasons** | bone-chewers: dogs, foxes, wolves, rodents; deer at shed antler and bones | smell, chance | bones | bone | bones scattered and thinned |

**What the order means for people.** In warm months a carcass left out is mostly insects' and microbes' within a day or two; in cold
months it feeds vertebrates for days, so winter carcasses draw foxes, dogs, ravens, wolves and boar near wherever they lie.

### D.3 What people's handling changes

| Handling | Physical effect | What it draws | Consequences |
|---|---|---|---|
| **leave it where it fell** | full decay and scavenging | the whole succession | scavengers near that place; if near the village, rats, dogs, foxes and kites learn the place (M9 commensals); if in the wild, a windfall for wolves and bears and a place of danger; evidence stays (a poached deer's leavings; a body found by the crows) |
| **butcher promptly** | meat, fat, hide, bone, sinew taken (02zs §2.4); leavings (gut pile, blood, trimmings) left | birds by day, foxes, dogs, boar by night at the leavings | the leavings' signs mark where it was killed (evidence); a gut pile in the wood draws scavengers there, not at the village |
| **hang the meat** | in cool air it keeps; in warmth flies reach it | flies; cats, dogs, rats if reachable; kites if outdoors | a hung carcass in a shut cool room keeps; on a tree outside it feeds birds |
| **carry it home or leave it** | weight against capacity (a deer about 2.6 meat by weight at engine scale: one person can carry one) | what is left in the wood is scavenged there | a drive's or a far foray's extra meat left "hanging in the brake" (forays.md §4) is a windfall for whoever, or whatever, comes first |
| **bury it** | stops scavenging by birds and most smell; depth by labour (D2-96: 2 units soft, 4 stony, 6 frozen for a body) | shallow burial is dug by foxes, badgers and dogs | a grave or pit holds its disease (anthrax persists); burying a diseased beast where others graze keeps the risk in that ground |
| **burn it** | ends it, its smell and its disease; costs fuel and labour (a cow needs a great deal of wood: many units of firewood or timber) | nothing | a cost borne by one for others' benefit; draws on the shared fuel (Part A) |
| **give it to the dogs or pigs** | feeds kept animals (the kennel loop, 02zt §4.2) | | disease passes to them (swine fever from boar carcasses, built as a disease) |
| **put it on the midden** | adds to the waste stock | rats, kites, crows, dogs, flies to the village | the midden's place decides which houses get the rats and the stink |
| **salt, smoke, dry** | stops decay | nothing while stored securely | needs salt, fuel and a store (Part A) |
| **move a diseased carcass** | the disease goes with it | | murrain carried to a new place (D2-71's disease risk, when illness and disease spread exist) |

**What this gives without forcing any custom.** A household weighs butchering at once against labour, carrying against leaving,
burying against burning against fuel, feeding the dogs against disease risk, the midden's place against the rats; and a village sees
the consequences in rats, foxes, kites and dogs near houses, in sickness among beasts, in evidence found by others, and in danger at a
cached carcass. Whether people make rules about any of it is theirs.

### D.4 One general rule for all organic things

**The rule (one function, no kind named in it):**
1. **The thing:** every organic thing at a spot (a carcass, a body, remains, a pile of food, a midden, leavings) carries a **mass**
   (food a scavenger can take, by part: meat, offal, fat, hide, bone), a **stage** (fresh, ripe, putrid, dry, bones), its
   **conditions** (open dry or wet, warm, frozen, covered, hung inside, buried at a depth, salted, smoked), and a **disease load** if
   it died of one.
2. **Each night:** the stage advances by a rate times the conditions (the DECAY table's factors extended to stages); insects and
   microbes take a share of soft mass by temperature (more in warmth, little in frost).
3. **What it emits, by stage:** a **sight** of birds circling once any bird has found it (own conspicuousness rising with the birds),
   a **smell** that rises from fresh to putrid and travels by wind and distance (with the shared perception of 02zr M1 and a wind
   field), **flies** (sound and sight, in warmth), and **bones** (sight, low) later. People read these by the noticing rule; animals
   by their senses through the same rule.
4. **Who comes:** each kind with carrion in its diet decides through its own module (D2-203) whether to come, by its traits: senses
   (sight by day, scent at night), diet preference by stage (birds and foxes take fresh to ripe; flies and beetles ripe to putrid;
   bone-chewers bones), boldness near people (rats, dogs, foxes bold; boar, badgers, wolves shy), range (ravens and wolves far; rats
   near), time of activity (day or night), and the presence of others (ravens raise the chance of every other kind; a wolf or bear
   at it keeps smaller ones off until it leaves; a bear caches and stays).
5. **What it takes:** a share by body size and dominance, from the mass of the parts it eats; dragging parts away scatters the
   remains (a trace); disease passes to the eater.
6. **What lingers:** bones as a trace for seasons; disease in the ground where it lay or was buried.
7. **The macro link:** what scavengers near people take comes off the thing; what dies in the wild areas beyond people stays in the
   area's carrion stock (wild/ecology.py) as now. A carcass condensed near people (a wolf kill near the fold) becomes a thing at a
   parcel and runs this rule.

**Through the families (02zs §7):** people meet it through **process** (butcher, render, salt, smoke), **exclude** (a shut cool room,
a covered pit, a fenced midden), **reduce** (bury, burn, feed to beasts), **know** (reading birds, smells and bones), and **take**
(taking from a carcass is a search, D4-70). Nothing in the rule is specific to a kind or a custom.

**What the engine needs:** stages on organic things (extending `body_days`, `carcass_fresh_days` and `carcass_bones_after` to the
stages above, with DECAY's conditions); parts on carcasses (with the butcher step); a disease load on a thing; a night step that lets
kinds' modules come to things by their traits; signs per stage (sight of birds, smell by wind, flies, bones); a wind direction in the
climate (also needed for M1); the midden as a stock with a place; burning as work with a fuel cost; burial depth.

## E. What the engine needs (all four parts together)
1. **Traits on kinds and properties on methods, gear, barriers and stores, with one encounter rule** (02zs §8.1; Part C), and the
   guard test that no verb, technique or rule names a kind.
2. **The verbs consolidated to the designed grammar** with the object slots of §C.5; the wild yield kinds folded into the general
   resolutions; kind-named techniques converted to methods (§C.4).
3. **Standing works** that act each night by their properties (Part B; §C.5 rule 5), with condition, upkeep, capacity and depreciation.
4. **Delayed processes** (batches over days at a fitting: smoking, tanning, curing, training).
5. **The butcher step and parts** on carcasses (02zs §2.4; Part D).
6. **Stages, conditions and scavenging** on all organic things (Part D).
7. **Skill and readings by method family** (generalising `reads_as` and `SKILL_CARRY`).
8. **Forays** as `travel` with a route in words (forays.md), resolving takes along the route by the encounter rule.
9. **Wind direction** in the climate (02zr M1; Part D smell).
10. **Visibility of capital** (signs of condition, contents, use) and of decay (stages).
11. **Diagnostics only:** chains used and their depth; share of labour on each need; capital built and its condition; standing works'
    yield against hand work; methods used per household; scavenger visits by place and stage; evidence found; institutions that
    emerged, coded after runs.

## F. What to change in the earlier files

| File and section | Change |
|---|---|
| 02zr §0, §1.2 b and its table; any "a unit is about two real days" | withdraw the conversion of acts into real days (Zach, 9 Nov): a unit is a part of one in-game day; the ecology's rates stay on the engine's clock. The table's point that the ecology's nightly contests fall inside one engine night still holds for the ecology's side |
| 02zr §3.5 F1 (the search inside one act) and §8.1 item 4 | replaced by forays.md (a route in words; places in the person's memory) |
| 02zr M2 (the stretch contest) | recast: the watch is one night's act; the ecology resolves the group's response for that engine night against the distinct deterrents held; no "share of the stretch watched" |
| 02zs §0 header and §3.6, §8.6, §10 | spots are in the person's memory, not an engine table (forays.md §5); the engine keeps only the foray's record; "spots as knowledge items" becomes "places remembered, named and told" |
| 02zs §8.2 ("one take, with the foray") | the take's object slots as §C.5 here; `foray` as `travel` with a route |
| 02zt §0 and §2 time column | units are parts of a day; build and growth times stay in engine days |
| 02zt §2.5 "a map or list of spots" | a document people write, or memory; never an engine table |
| wild_behaviour.md F1 and §7 ("hunting becomes the search game") | replaced by forays and the encounter rule |
| things_in_places spec / carcasses.md | when Part D is taken up: stages, parts, scavenging and disease load extend D4-52 and D2-96 (OPEN L-2's scavengers) |

## Sources

1. Forensic entomological decomposition (stages; bloat in one to four days in warm weather, absent in very cold conditions):
   https://en.wikipedia.org/wiki/Forensic_entomological_decomposition
2. Soil sample analysis of *Bacillus anthracis* at animal burial sites (viable spores over a decade):
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11509789/
3. Selva et al. (2005), "Factors affecting carcass use by a guild of scavengers in European temperate woodland" (Białowieża):
   https://openpolar.no/Record/crcansciencepubl:10.1139%2Fz05-158 ; Institute publication: https://ibs.bialowieza.pl/publications/1546.pdf
   3b. Scandinavian wolf-kill scavenging by season (thesis): https://stud.epsilon.slu.se/20454/1/fagerberg-e-20240827.pdf
4. DeVault, Rhodes and Shivik (2003), "Scavenging by vertebrates" (Oikos), via SREL reprint 2685:
   https://sites.google.com/view/ugasrelpublications/reprints/2685 ; DeVault's dissertation (vertebrates took over half of carrion
   in cooler months): https://docs.lib.purdue.edu/dissertations/AAI3108337
5. Wilmers et al. (2003), trophic facilitation by grey wolves (pack size and carrion; ravens and eagles at aggregated kills):
   https://typeset.io/pdf/trophic-facilitation-by-introduced-top-predators-grey-wolf-wsef52lvxh.pdf ; ravens returning to kill
   areas (2026): https://www.sciencedaily.com/releases/2026/03/260319044643.htm
6. Domesday mills (5,624, Hodgen; about 6,000 or more by later estimates): https://en.wikipedia.org/wiki/List_of_early_medieval_watermills ;
   Historic England, mills: https://cms.historicengland.org.uk/images-books/publications/iha-mills/heag212-mills
7. Magna Carta clause 33 on weirs and kiddles (Magna Carta Project): https://magnacarta.cmp.uea.ac.uk/read/magna_carta_1215/Clause_33
8. Boserup on intensification; Sherratt's secondary products; Rackham on coppice; Hoffmann on fishponds: as cited in 02zs.

Repository sources: `docs/cybertron2/proposals/` forays.md, verbs.md, verb_modifiers.md, use_by_physics.md, act_fixes.md,
agent_view.md, refusal_messages.md, search_on_take.md, knowledge.md, recipes.md, tools.md, husbandry.md, carcasses.md, graves.md,
slaughter_signs.md, objects_in_world.md, things_in_places.md, water_and_preservation.md, transport_and_lodging.md, farming.md,
forests.md, fences.md, economy_plan.md, resources_and_goods.md; `docs/cybertron2/spec/agents/` actions.md, modifiers.md, work.md,
standing_orders.md, aims.md; `spec/information/` prompts.md, perception.md, memory.md, letters_and_documents.md;
`spec/world/things_in_places.md`; `spec/economy/` transport.md, goods.md; `docs/scenario_design.md`; reviews 38.37, 38.49, 38.50 as
cited in those files; 02zr, 02zs, 02zt; the ecology branch's `engine/verbs.py` (VERB, `_technique` and its yield kinds), `data.py`
(TECHNIQUES, ITEMS, THINGS, DECAY), `knowledge.py`, `perceive.py` (`practised`), `labour.py`, `things.py`, `engine/wild.py` (`take`,
`watch`, `shut`, `guard`), `wild/kinds.py` (diets with carrion, `SKILL_CARRY`, `RAVENS_OVER`), `wild/ecology.py` (the carrion stock).

**Claims to check before any spec:** the decay stage timings in engine days (proposed, calibrate); osteophagy by deer and sheep;
the burying beetles' role on small carcasses in this climate; the fuel to burn a cow; the scavenger arrival orders, which differ by
season and place in the studies.

## History
- 9 Nov: written at Zach's request as the third pass (chains, capital, actions), with Part D (decay and scavenging) added the same
  day; after forays.md (9 Nov).
