# Proposal: what people make of wild things: economies, husbandry, tools and skills

**Status:** discussion (8 Nov). Nothing decided, nothing to build. **Owner:** 37.2 (the economy, goods and recipes), with 37.4 (the
engine). **Affects:** data (ITEMS, TECHNIQUES, FITTINGS, BLUEPRINTS, KINDS, as packs, D4-104); spec/economy/production.md, goods.md,
buildings.md, livestock.md; proposals/wildlife.md, wild_plants.md, water_and_preservation.md, living_populations.md; OPEN L-13, L-14,
L-36.

## Summary

Zach, 8 Nov: "(b) are there any economies or things etc that come from the different wildlife or could be interesting to come from
different plants ... (c) are there different ways these new wildlife could be domesticated, bred, used etc. what types of tools,
skills etc would these need?"

- **(b) Economies.** Wild things feed four kinds of economy:
  - **trades** (the fowler, the eeler, the woodward, the tanner, the thatcher);
  - **material chains** (hide to leather or parchment; withies to traps and wattle; fat and wax to light; feathers to quills);
  - **a calendar of seasonal goods** that makes trade between seasons and places;
  - **rights in wild things,** the old common rights (pannage, turbary, estovers, piscary), which are institutions waiting to
    happen.
- **(c) Husbandry.** Each wild kind has a path from taking to keeping: from hunting a wild thing, to tending it where it lives, to
  holding it in a place made for it, to breeding it. Each step needs a tool or a structure and a skill. In the engine it is one
  general move: **a population becomes "kept" when its habitat is a held place** (a pen, a warren, a dovecote, a pond, a hive, a
  coppice) **and its food is a need someone meets.** Domestic herds already are this; husbandry generalises herds.py.

## 1. Economies from wild things (b)

### 1a. Trades

Each trade is a set of techniques that one household or person comes to specialise in (D2-52's skill by practice):

| Trade | Works with | Sells |
|---|---|---|
| stalker, hunter | deer, boar | venison, hides |
| warrener | rabbits (kept), ferrets, nets | rabbits, skins |
| fowler | wildfowl, decoys, nets | birds, feathers, down |
| fisher, eeler | trout, salmon, eels; rods, traps, weirs | fresh, smoked, salted fish |
| trapper, furrier | wolves, beaver, otter, marten, fox | pelts |
| honey-gatherer, beekeeper | wild bees, skeps | honey, wax |
| falconer | hawks | a hunt; a trained hawk |
| woodward | coppice, timber, withies | poles, withies, bark |
| charcoal burner | wood (exists) | charcoal |
| basket-maker | withies | baskets, eel traps, hurdles |
| thatcher | reeds, heather | roofs (with building upkeep, L-48) |
| tanner | hides, oak bark, lime | leather |
| parchment-maker | hides, lime | parchment |
| chandler | fat, wax, rushes | candles, rushlights |
| herbalist, healer | herbs | remedies (with disease) |
| rope-maker | lime bast, hemp | rope, cord, nets |

### 1b. Material chains (the ones worth having)

| Chain | Steps | Why it matters |
|---|---|---|
| **Leather** | hide → tanning with oak bark in pits, **months** (a delayed process, D4-103 part 4) → leather | shoes, harness, buckets, bellows; the tanner as a trade that needs both hunters and woods |
| **Parchment** | hide → lime and stretching → parchment | **documents are made from wild things** (wildlife.md §11): parchment, goose quills, oak-gall ink, beeswax seals |
| **Light** | fat → tallow; wax → candles; rushes and fat → rushlights | nights become usable time (if light is ever a need) |
| **Withies** | coppiced hazel and willow → hurdles, baskets, eel traps, wattle | **the coppice becomes valuable for more than fuel**; fences and traps from the wood |
| **Thatch** | reeds, heather → roofs | the fen and the moor sell to the vale |
| **Pannage** | mast in a wood + pigs (L-36) → pork → salted bacon | a wood's autumn worth, paid for as a right |
| **Rope and nets** | lime bast, hemp → cord → snares, nets | opens fowling and net-fishing (L-13's "fibre") |
| **Smoked and salted goods** | fish, meat + smoke or salt → keeping goods | the water proposal's preservation ladder (water_and_preservation §7) |

### 1c. A calendar of seasonal goods

| Season | Goods coming in |
|---|---|
| spring | greens (the hungry gap), eggs (seabirds, pigeons), bark for tanning |
| summer | honey, berries, hay, samphire, rushes |
| autumn | nuts, mast, hedge fruit, fungi, the salmon and eel runs, the slaughter |
| winter | wildfowl, furs, withies and reeds cut, peat |

Different villages have different seasons' plenty: the fen in winter, the wood in autumn, the coast in spring. That is what makes
trade between them worth the walk, and a reason to store and sell.

### 1d. Rights in wild things: the old common rights

English commons named the rights to take wild things, and they are exactly institutions over shared stocks:

| Right | Over |
|---|---|
| pannage | turning pigs into a wood for mast |
| estovers | taking wood (fuel, repair) from a common |
| turbary | cutting peat or turf |
| piscary | fishing |
| common of pasture | grazing |
| warren, dovecote, fishery, park | a lord's privilege to keep certain kinds |

D2-194 already lets a world give rights in wild kinds at its start. These names give agents a vocabulary for rights they may create,
dispute or sell: a dispute over turbary is a commons problem in the open.

## 2. Husbandry: from taking to keeping (c)

### 2a. The ladder

| Rung | What it is | Example |
|---|---|---|
| 1. Take | hunt or gather from the wild | stalking deer; gathering hazel nuts |
| 2. Tend | look after a wild stock where it lives | coppicing hazel; marking a bees' tree as yours; feeding deer in winter |
| 3. Keep | hold it in a place made for it | a warren, a dovecote, a fishpond, a deer park, a skep, an osier bed |
| 4. Breed | choose which breed | hounds for scent or speed; pigs; plants by seed or grafting |

Each rung costs more and gives more, and each is held: keeping is a claim on the place and the animals.

### 2b. Kinds that can be kept

| Kind | How it is kept | Structure | Tools and gear | Skill | Gives |
|---|---|---|---|---|---|
| **dogs** (hounds, mastiffs, sheepdogs) | bred and trained; kennelled | kennel | collar, leash | breeding, training | hunting, guarding, herding (D2-196) |
| **hawks** | taken young and trained, not bred | mews | glove, hood, jesses, lure | falconry (months) | a hunt for fowl and hares; status |
| **ferrets** | kept for rabbiting | hutch | purse nets | warrening | rabbits from burrows |
| **rabbits** | farmed in a warren | warren: pillow mounds and a bank | nets, ferrets | warrening | meat, skins; a lord's privilege, poached |
| **pigeons** | kept in a dovecote | dovecote | | | squabs, eggs, **dung** (the best manure); a privilege; they eat crops |
| **bees** | kept in skeps or log hives | skeps, a bee bole | smoke, a skep | swarm-catching, beekeeping | honey, wax, and pollinated crops |
| **pigs** | herded in woods for mast | sty | | swineherding | pork, bacon, lard (L-36) |
| **deer** | kept in a park | the pale: bank, ditch and fence | | park-keeping | venison for the holder; status |
| **fish** (bream, tench, pike) | stocked in fishponds | stew ponds, a sluice | nets | pond-keeping | fish in Lent; drained and harvested |
| **swans** | owned, marked, pinioned | | | | a status bird (D2-194) |
| **poultry and geese** | kept at the house | coop | | | eggs, meat, feathers and quills; foxes take them |
| **cats** | kept against rats | | | | fewer rats in stores |
| **wild young** (a fawn, an otter cub, a raven) | tamed one at a time | | | | a novelty, a pet, status |

### 2c. Plants that can be kept

| Plant | How | Tools | Skill | Gives |
|---|---|---|---|---|
| hazel, willow | coppice and osier beds, cut in a cycle | billhook | woodmanship | withies, poles |
| thorn hedges | planted and laid | billhook, gloves | hedgelaying | fences that grow (herds, L-24) |
| apples, pears | orchards, grafted | grafting knife | grafting | fruit, cider |
| herbs | a healer's garden | spade | herb lore | remedies |
| flax, hemp | sown in fields, retted in ponds (a delayed process) | ripple, brake, spindle | spinning | fibre for cord, nets, cloth (L-13, L-14) |
| dye plants | sown | | dyeing | colours (later) |
| wild greens and fruit | left standing at field edges, tended | | | the hungry gap's food nearer home |

### 2d. Tools and gear, in one list

| Tool | Made from | For |
|---|---|---|
| snares | cord (bast, hemp) | hares, rabbits |
| traps (deadfall; later iron) | timber; iron later | furbearers, wolves (D2-23) |
| wicker traps | withies | eels, fish |
| nets (purse, fowling, fishing) | cord | rabbits, fowl, fish (fibre: L-13) |
| a boar spear | an ash shaft and a crossbar; a copper or iron head | boar, bear (D2-193) |
| bows and arrows | yew; sinew; goose feathers; heads | game, later war |
| decoys | timber, feathers | wildfowl |
| a fishing rod | built (water pack) | fish |
| skeps | straw | bees |
| falconry gear | leather (glove, hood, jesses), a lure | hawks |
| a billhook | copper; iron later | coppice, hedges, withies |
| a grafting knife | copper | orchards |
| a turf spade | timber and metal | peat (turbary) |
| tanning pits | dug ground, timber | leather |

## 3. The skills

All are techniques with skill by practice (D2-52). Some are shared knacks; most are their own. "Hard to do unless someone is good at
that one" is the default:
- tracking;
- stalking;
- trapping;
- fowling;
- eeling;
- fishing;
- swarm-catching and beekeeping;
- falconry;
- dog breeding and training;
- warrening;
- woodmanship (coppicing, hedgelaying);
- grafting;
- basketry;
- thatching;
- tanning;
- parchment-making;
- herb and mushroom lore (safety);
- rope-making;
- spinning;
- park-keeping and pond-keeping.

Taught by someone who knows, or learnt slowly alone (untaught tries at half, D4-103 mechanism 2): **knowledge is a scarce good that
households hold and trade.**

## 4. In the engine: general mechanisms, no special cases

| Need | General mechanism | Status |
|---|---|---|
| a kept population | **a kind's population whose habitat is a held place and whose food is a need someone meets.** Domestic herds already work so (herds.py); it generalises them to any kind (a RESOURCES row with population fields) | proposed (generalises built herds) |
| a structure that keeps a kind | a building or fitting (warren, dovecote, skep, fishpond, pale, kennel, mews) whose capacity is a habitat | built mechanism: fittings with capacities (02zh) |
| a trained animal as a tool | a led beast that multiplies techniques (hounds, hawks, ferrets; like the pack ox) | led beasts built (D4-58); the multiplier is general |
| processes that take time | tanning, retting, training a hawk, a coppice cycle, a fishpond season, smoking | D4-103 part 4 (delayed processes), designed |
| breeding for type | a kept population's traits as a few numbers shifted by choosing parents (hounds' scent or speed) | new, small; later |
| rights | claims (D2-194; world/holding.md) | built |
| tools | items with tool multipliers and wear | built |

**Nothing here needs code for one kind.** A warren, a dovecote and a fishpond are the same thing: a kept population in a held
structure, fed or feeding, with a take by a technique.

## 5. What to build first, and what to leave

- **Now, because demand exists:**
  - **withies** (wattle from rods; eel traps and hurdles), which the coppice already grows as young growth;
  - **leather tanning,** because hides have uses now (packs, harness, tents) and leather would extend them;
  - **pannage,** with pigs (L-36).
- **With wave 2 and 3** (wildlife.md): hounds (D2-196), skeps and the beekeeper, falconry.
- **Wait for their need:**
  - parchment (documents);
  - candles (light);
  - flax and cloth (clothing, L-14);
  - herbs (disease).
- **Leave:** breeding for traits until a kept kind shows it matters.

## 6. Does it add richness at the bottom of the economy? (Zach, 8 Nov)

**The bottom layer today is thin** (38.57):
- need produces hoarding and self-provision, not exchange;
- "slack needs something worth wanting": on richer land, food stayed 85 to 90% of work and households stockpiled;
- a chokepoint with cheap substitutes is not one (every house had a hand mill);
- kin carried all the trade between villages.

**These additions add richness by:**
- things worth wanting beyond food, so slack has a use;
- different places with different things;
- different seasons with different plenty, so storing, carrying and credit across the year pay;
- chains with tradable middle goods (bark and hides to the tanner, leather to the harness-maker);
- capital that wears, so demand repeats;
- skills that take time;
- rights that earn rents and cause disputes.

**It works only if:**
1. **Specialisation pays:** a practised hand is far better than a novice, learning takes real time, and some trades need capital.
   Otherwise every household does everything itself, which is the hand-mill lesson again.
2. **Demand exists:** only goods with a use now (§5).
3. **Place and season differ for real:** no village has everything.
4. **Gear wears.**
5. **It is visible:** what others make and offer, and what is going off.
6. **The prompt stays small:** each agent sees only its place's techniques and its own knowledge.

**The risks:**
- more options can mean more self-provision, not more exchange, if condition 1 fails;
- food may still dominate unless capacity allows slack (the 30% rule);
- it does not fix how agents act (they use leverage more than they create it). It gives that behaviour more to act on.

**The test:** the same world with these packs on and off. Compare:
- the share of goods acquired by exchange against made at home;
- how specialised households' work is (concentration of each household's work);
- the number of distinct goods traded, and between which villages;
- food's share of work against the 30% gate;
- a reading of the end state.

## 7. Wild and domestic as one lineage (Zach, 8 Nov)

Zach: the domestic animals should be special cases of wild ones, built on the same wildlife system, so that taming a new wild kind
works like the herds that exist.

### 7a. History: most stock came already domesticated

| Domestic | Wild ancestor | In the temperate envelope (medieval Britain) |
|---|---|---|
| cattle | aurochs | **imported domesticated** (Neolithic, from the Near East); the aurochs was gone from Britain by the Bronze Age |
| sheep, goats | Asian mouflon, bezoar | **imported**; no wild ancestor in northern Europe |
| horses | wild horse | **imported**; the native wild horse had died out early |
| hens | junglefowl (Asia) | **imported** |
| cats | Near Eastern wildcat | **imported**; the native wildcat interbreeds with them |
| pigs | wild boar | **both:** imported stock, crossed with local boar; sows in pannage are served by wild boars |
| geese | greylag | **native wild**; goslings caught and kept |
| ducks | mallard | **native wild** |
| doves (dovecotes) | rock dove | **native** on the coast |
| bees | honey bee | **native**; hives are filled with caught swarms |
| dogs | wolf | domesticated long before; the wolf is still there |
| ferrets | polecat | kept domestic form; the polecat is wild beside it |

So a world needs no aurochs to have cattle: the herds arrive with people, as they did. But **the habitats that support them are the
same ones**: cattle eat what the aurochs ate (grassland, wood pasture, fen edges). What domestic forms add is **dependence**: they need
hay in winter, a byre, protection from wolves, and milking.

### 7b. The model: a lineage, a state, a few traits

1. **Kind = a RESOURCES row**, as in living_populations.md. A wild kind and its domestic form are **two rows of one `lineage`** (boar
   and pig; aurochs and cattle; greylag and goose). They interbreed where they meet: the young join the mother's population, with
   the traits mixed.
2. **State = wild, kept or feral**, a property of a population, not of a kind:
   - **wild:** its own habitat, nobody's;
   - **kept:** its habitat is a held place (§4): pasture with a fence, a byre, a sty, a park, a warren, a pond, a hive. A kept wild
     kind (park deer, warren rabbits, a hawk, a swarm) is the same state;
   - **feral:** a kept population that nobody holds for long enough (pigs gone wild in the wood, ponies on the common).
3. **Traits = a few numbers per row:**
   - docility (how close it lets people come; flight);
   - dependence (the share of its winter food and shelter people must give);
   - growth and yield (milk, wool, eggs, meat, draught);
   - size;
   - generation length.

   A domestic row is just a lineage with its traits far toward docile and dependent.
4. **Domestication = traits drifting in a kept population**, by which parents breed (§4, "breeding for type"):
   - It is slow, so it shows only in fast breeders under deliberate choice. Geese, ducks and pigs breed every year; cattle every 4
     or 5. A 30-year run is 6 to 30 generations. Belyaev's foxes were markedly tamer within about 10.
   - Nothing is scripted. A long run that keeps and selects boar could make them tamer. A short run never will, and taming in it
     means keeping wild stock (park, warren, pond, hive) or taming one individual (a hawk, a hand-raised fawn).

### 7c. What it does to the built herds

herds.py is already most of the general mechanism, written for cattle:

| Built for cattle | General form |
|---|---|
| wandering toward the most attractive parcel (D2-117, D2-123) | the movement rule (living_populations §2c) with home = the holder's pasture |
| the walk home at dusk (D4-54) | home fidelity |
| splitting by how many head the people with it hold (D2-128) | splitting (§2c) |
| roles cows, oxen, bulls, young | **per-row data:** females, castrated males, males, young (ewes, wethers, rams, lambs; sows, hogs, boars, piglets) |
| fences crossed at their odds | a held place's hold on a population, by state |
| lost on the road, or found | a population with no held place: astray, then feral |

So the order is: **herds become the first kept population**, and wild kinds use the same rule with no held place. Their roles move
from code (herds.py `ROLES`) into data. That change is in 37.4's code, so it waits for a board agreement and for living_populations
step 1. It is a generalisation of built behaviour, and the built tests are its check: cattle must behave exactly as now.

### 7d. What a world sets

- **Which lineages exist and in which states:** a medieval world has cattle, sheep, pigs, hens and geese kept, with boar, greylag
  and wolves wild; an earlier frontier world could have aurochs wild and cattle few.
- **Where the stock came from:** in the start state, or by trade (L-36). Nothing needs a local wild ancestor.

## Open questions (for Zach)

1. The rule that keeping is one general mechanism (a kept population in a held structure), generalising herds?
2. First: withies, tanning and pannage, because their goods have uses now?
3. The common rights (pannage, turbary, estovers, piscary) as named rights a world can seed and agents can create?
4. Breeding for traits: later, as proposed?
5. Wild and domestic as two rows of one lineage, with state (wild, kept, feral) on the population and a few traits per row (§7b)?
6. Herds generalised into the first kept population, roles as per-row data, with the built herd tests as the check (§7c)? This is
   37.4's code, so it is a board item.

## History

- 8 Nov: Zach asked (b) what economies come from wildlife and plants, and (c) how they could be domesticated, bred and used, with
  what tools and skills. 37.2 proposed this.
- 8 Nov: Zach: "Could these add richness at the lower layer of the economy?" Added §6: how, the conditions it needs (from 38.57's
  lessons), the risks, and the on/off test.
- 8 Nov: Zach asked whether domestic animals should be special cases of wild ones that could be found and tamed, whether that needs
  environments that support cattle or whether cattle were imported, and whether it should all run on the wildlife system. Added §7:
  most stock was imported domesticated, but on the same habitats; wild and domestic as two rows of one lineage; wild, kept and feral
  as a population's state; traits that drift under breeding; herds.py as the first kept population. Questions 5 and 6.

## Sources

- proposals/wildlife.md (D2-192 to D2-196), wild_plants.md, water_and_preservation.md, living_populations.md, process_model.md (D4-103,
  part 4 and mechanisms 1, 2, 5, 8), economy_later.md (L-13);
- engine: herds.py, led beasts (D4-58), fittings (02zh), hides' uses in TECHNIQUES;
- English common rights: pannage, estovers, turbary, piscary, common of pasture.
