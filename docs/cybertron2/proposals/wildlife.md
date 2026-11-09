# Proposal: the first wild kinds (what lives on the land, what each is for)

**Status:** partly accepted: D2-192 to D2-196 (8 Nov; spec/environment/wildlife.md). Not built. §11 (other kinds and niches) and §12 (the general mechanisms) are discussion. **Owner:** 37.2 (the kinds, their numbers and their goods), with
37.4 (the engine). **Affects:** data (RESOURCES rows with population fields; new goods and techniques, as a `wildlife` pack, D4-104);
spec/environment/resources.md, spec/economy/goods.md and production.md; landgen/ecology.py (habitats and starting populations);
proposals/living_populations.md (the mechanism this content runs on).

## Summary

Zach, 8 Nov: "design the first key ecosystems. I want some level of diversity, some being valuable for different reasons, some rare,
maybe some are hard to hunt unless someone is specifically good at hunting that one ... start with some richness possible albeit
obviously not always happening all at once in one place. Consider ... the different core purposes we might want to serve ... and the
interesting roles wildlife have played in real life."

This proposes **17 kinds in four waves**, chosen so that each serves different purposes of the simulation and differs from the
others on several axes:
- where it lives and how it moves;
- its season;
- how it is taken, and by whom;
- what it gives, and its danger;
- how rare it is.

Each is one row of data on the mechanism of living_populations.md. Every kind has its own way of being taken, with its own skill, so
a good deer stalker is a poor fowler; some need a crew, gear or a trained beast. Rarity comes from habitat and the world's seed: a
fen world has fowl and eels in thousands and no bear, and a wildwood frontier may hold one.

## 1. What wildlife is for in this simulation

| Purpose | What it creates | Kinds that serve it |
|---|---|---|
| **Partial observability** (§0 of living_populations) | hidden, shifting populations known by signs, catches and lore; trackers and foresters worth having | all; ravens as pure signs |
| **Carrying capacity and the lean season** | wild food as a buffer, sustainable or overdrawn; seasonal pulses | deer, boar, hares, fish, eels, fowl |
| **Specialisation and dependence** | each kind its own technique and skill; gear, crews and trained beasts; trades (stalker, fowler, trapper, fisher, honey-gatherer, falconer) | all |
| **Commons and management** | open stocks that collapse, or rules that keep them: closed seasons, rights, quotas | salmon, eels, deer, beaver |
| **Danger and collective action** | threats that need many hands: the watch, a hunt by many, a bounty | wolves, boar, bear |
| **Damage and conflict over land** | animals that eat crops, herds or stores; who pays, who guards | deer, boar, hares, wolves, foxes, rats |
| **Status and inequality** | prized goods and privileged rights: venison, falcons, furs, swans; poaching as crime | deer, falcon, beaver, marten, swan |
| **Trade goods and material chains** | goods worth carrying: hides, furs, wax, salted fish, castoreum | deer, beaver, otter, marten, bees, salmon, eels |
| **Land that changes** | animals that change the land, and land change that moves animals | beaver (dams), deer (browsing), boar (rooting) |

## 2. Roles wildlife played in real life (the hooks)

- **Forest law.** Norman and later kings made "forests" where deer and their cover (venison and vert) belonged to the king; taking a
  deer was a crime, and the Charter of the Forest (1217) eased it. Status, enclosure and poaching.
- **Eels as rent.** Domesday records rents paid in eels by the thousand. Eel fisheries and weirs were valuable held rights.
- **Salmon and weirs.** Fish weirs blocked rivers and runs. Magna Carta (1215, clause 33) ordered weirs removed from the Thames,
  the Medway and all England. This is the upstream-downstream conflict.
- **Wolves and bounties.** Tribute and bounties in wolf heads, and organised extermination in England by about 1500. Collective
  action against a common threat.
- **The beaver's extinction in Britain** (by about the 16th century), for fur and castoreum. Easy to trap and slow to breed: the
  model of a stock lost to open access.
- **Mast and pannage.** Pigs fattened on acorns and beech mast in the woods, a right paid for. Mast years boom and bust (D2-76's
  ecology era).
- **Honey and wax.** Honey was the sweetener. Wax made church candles and seals, so it was a demanded good with no substitute.
- **Royal birds and fish.** Swans and sturgeon were claimed by the Crown. Some wildlife belongs to the powerful by law.
- **Falconry.** A trained hawk was status and a hunting partner, taken from a cliff eyrie and trained for months.
- **Ravens and crows.** They gather at carcasses and battlefields: a sign of death read from far off.
- **Warrens, dovecotes, fishponds, deer parks.** Wild kinds brought under husbandry, usually as a lord's privilege.

## 3. How the kinds differ: the design axes

- **Habitat and range:** woods by type and depth; open land; rivers by size; fen and coast; cliffs.
- **Movement:** sedentary, a home range with wandering, roaming, seasonal runs (living_populations §2c).
- **Count:** density, or whole groups (living_populations §3).
- **Season:** a run, a winter arrival, the rut, a mast year.
- **How it is taken** (§5):
  - a technique and its skill;
  - gear (spear, snares, nets, traps, rod);
  - a crew;
  - a trained beast (hound, hawk);
  - danger to the taker.
- **What it gives:** meat, fat, hide, fur, feathers and down, honey and wax, antler, castoreum.
- **Value type:** food now; materials with a use now (hides); trade and prestige (furs, falcons); goods waiting for a use (wax for
  seals and candles, feathers for arrows).
- **Rarity:** common, local, scarce, rare (§7).
- **Effect on people:** none; damage (crops, herds, stores); danger.

## 4. The kinds

Numbers are first values to calibrate. Densities are per km² of suitable habitat; a 50 km window is 2,500 km².

### Woods

| Kind | Count, range, movement | Season | Taken by | Gives | Role | Rarity |
|---|---|---|---|---|---|---|
| **Red deer** | herds of 5 to 15; a home range in a wood, wandering to its edge and into fields at night; down to lower woods in winter. 3 to 8 a km² of wood. | the rut (autumn): stags careless, easier | **stalking** (skill, a bow or spear later; a crude weapon now). The capital deer is the noble's: hounds and a hunt (crew). | meat, hide, antler | food; hides for bedrolls and tents; crop damage; **the noble's beast** (forest law) | common in large woods |
| **Wild boar** | sounders of 4 to 12, sows and young; mast-driven: boom after a mast year, thin after a bust | autumn: fattening on mast | **a boar hunt:** a spear and two or more people, or hounds. Alone it is dangerous: a wound or death, so it needs a crew. | much meat, fat, hide | food; danger (a crew); **crop damage**: rooting fields | local, in oak and beech woods |
| **Wolf** | packs of 3 to 8; a range of 100 to 300 km² around a large wood's core; roams. 2 to 6 packs a region. | winter: hunger, nearer villages; young disperse in autumn | **trapping or a drive** with many (crew); dangerous at bay | pelt | **danger and collective action**: takes deer, then herds and carcasses; the watch, fences, dogs, a bounty | scarce |
| **Brown bear** | single animals; a large range in wildwood and upland cores; 0 to 2 in a region | sleeps in winter; spring hunger | a hunt by many with spears and hounds; very dangerous | meat, fat, great pelt | **rarity and legend**; danger; takes honey, carrion, beasts | rare: present in about 1 world in 3 with wildwood |
| **Wild bees** | colonies in hollow old trees, 0.5 to 2 a km² of old wood; sedentary | summer: honey; take in late summer | **honey-gathering:** finding the tree (tracking the bees: a knack), smoke, climbing; stings | honey, wax | food (sweet, keeps for ever); **wax**: demanded later for seals and candles; hives are husbandry (later) | local, in old wood cores |
| **Pine marten** | single; old wood cores; few | winter pelt | trapping (skill) | fine fur | **trade and prestige** (waits for clothing or trade value) | scarce |

### Open land

| Kind | Count, range, movement | Season | Taken by | Gives | Role | Rarity |
|---|---|---|---|---|---|---|
| **Hare** | density: 10 to 40 a km² of grassland, downs and field edges; sedentary | all year; scarce in a hard winter | **snaring** (low skill: anyone can learn) or coursing with a hound | small meat, a pelt | **the poor man's food:** always some, never much; eats young crops | common |
| **Fox** | single or a pair; field edges and woods; 0.5 to 2 a km² | spring: cubs, takes young beasts | trapping, or a hunt with hounds | pelt | **a pest:** takes lambs (with sheep, L-36) and hares; a scavenger; signs | common |

### Waters

| Kind | Count, range, movement | Season | Taken by | Gives | Role | Rarity |
|---|---|---|---|---|---|---|
| **Trout** | density in brooks and small rivers; resident; diffuses along the stream | all year, best in summer | by hand (tickling) or **rod** (the water pack: built) | fish | food; a steady small catch | common in brooks |
| **Eel** | density in rivers, fen and meres; resident; **the silver eels run downstream to the sea in autumn** | the autumn run | **eel traps** set at night (wicker; a knack), or at a weir; spears in the fen | fish (keeps well smoked) | **food and rent**: the run caught at traps and weirs; held fisheries | common in fen and rivers |
| **Salmon** | density; **runs upstream from the sea in autumn** along large rivers; few resident | the autumn run | rod, spear, net, and **the weir** | big fish (salted or smoked) | **the upstream-downstream commons**: what is taken or blocked below never arrives above | local: large rivers to the sea |
| **Beaver** | families of 4 to 6 on slow rivers with woods; one lodge per 1 to 3 km; sedentary; **slow to breed** | winter pelts best | **trapping** (skill); easy to find by its dams | fur, castoreum (medicine, trade), meat | **land that changes**: fells trees, dams streams, makes ponds and wet ground; a fur good; **the open-access extinction** | scarce |
| **Otter** | single; 1 per 5 to 15 km of river; roams the river | all year | trapping, hounds | fine fur | **a rival at the weir**: takes fish; fur | scarce |

### Fen, coast and sky

| Kind | Count, range, movement | Season | Taken by | Gives | Role | Rarity |
|---|---|---|---|---|---|---|
| **Wildfowl** (ducks, geese) | density; **winter flocks** of hundreds to thousands arriving from beyond the map on fen, saltmarsh and meres; few in summer | winter | **fowling:** nets and decoys, or a fowling piece much later; a knack and patience | birds (meat), feathers and down | food in the lean season; feathers and down (bedding now; arrows later) | common in fen and on the coast, in winter |
| **Swan** | pairs on rivers and meres; few | all year | easy to take | meat, feathers | **a claimed bird**: a world may give swans to the lord (a right) | scarce |
| **Raven** | pairs, 1 per 10 to 50 km²; gather where there is carrion | all year | (not taken) | nothing | **pure information**: ravens circling show a carcass, a kill or a death far off | common |
| **Falcon** (peregrine) | pairs nesting on cliffs: 0 to 2 in a region | spring: eyasses in the nest | **taking an eyass** from a cliff (a climb), then months of training | a trained hawk | **prestige and a hunting partner**: takes fowl and hares for its keeper | rare: only where there is high rock |

### Later, as husbandry and pests

| Kind | Role | Waits for |
|---|---|---|
| Rats and mice in stores | raise a store's spoilage by its size and cover; cats, dogs, staddle stones; ties to the 10% spoiled (water_and_preservation §2) | the stores' upkeep (L-48) |
| Rabbits and the warren | brought in and farmed: a lord's privilege, poached | warrens as works |
| Pigeons and the dovecote | a lord's privilege; eat crops | dovecotes as a fitting |
| Fishponds, deer parks, hives | wild kinds under husbandry | each kind's wave |

## 5. Ways of taking them: one technique each, and the skills they need

Each is a technique (D4-103's one form). The engine already has skill by practice and an untaught try at half (process model
mechanism 2), so "hard to hunt unless someone is good at that one" is just this table.

| Technique | Kinds | Skill | Gear | Crew | Danger | Note |
|---|---|---|---|---|---|---|
| stalking | red deer | high: practice matters most | a weapon | 1 | low | best in the rut |
| a boar hunt | boar | high | a spear (later; a crude weapon now) | 2 or more, or hounds | **high** alone | a wound or death when it goes wrong |
| a drive | wolves, deer | low each, many hands | weapons | 4 or more | some | collective action |
| snaring | hares | low | snares (cord) | 1 | none | anyone can learn it |
| trapping | wolf, beaver, otter, marten, fox | medium; one knack across them | traps (D2-23, not built) | 1 | low | set and checked: theft and watching |
| eel trapping | eels | medium | wicker traps | 1 | none | set at night, the run in autumn |
| fishing | trout, salmon | low to medium | rod (built) | 1 | none | the water pack |
| fowling | wildfowl | medium | nets, decoys (fibre: L-13) | 1 or 2 | none | winter |
| honey-gathering | bees | medium: finding the tree is the knack | smoke, a climb | 1 | stings | late summer |
| taking an eyass, and training | falcon | **very high**; months of practice | a climb; a mews later | 1 | a fall | a trained hawk is a tool and a status good |
| tracking | finding any kind | a skill of its own | | | | makes rare kinds findable: the signs a tracker notices that others don't |

**Hounds** are a trained beast that multiplies stalking, drives, boar hunts and coursing: a kennel is capital. Dogs exist today only
as a building's watcher. Hounds wait for beasts beyond cattle (L-36).

## 6. Goods

| Good | From | Use now | Use later |
|---|---|---|---|
| meat | deer, boar, hare, fowl, bear | food (exists) | |
| fish | trout, eels, salmon | food (the water pack: built) | smoked or salted (water_and_preservation §7) |
| fat (lard) | boar, bear | food (rich) | tallow for light |
| hide | deer, boar | **bedrolls, tents, packs, harness, rods (all built)** | leather |
| fur (pelts) | wolf, beaver, otter, marten, fox, bear | trade and prestige only | warmth and clothing (L-14) |
| feathers and down | fowl, swan | bedding | arrows (bows later) |
| honey | bees | food that never spoils | mead |
| wax | bees | (none yet) | seals for documents, candles |
| antler | deer | (none yet) | tools, combs |
| castoreum | beaver | trade (medicine) | |
| a trained hawk | falcon | takes fowl and hares for its keeper | |

**The design rule:** a kind earns its place in the first waves only if what it gives has a use now (food, hides) or it makes a
pressure now (danger, damage, signs). Furs, wax and antler wait until clothing, documents or tools give them demand. Before that they
would be trade goods only, which agents may not value.

## 7. Richness and rarity

- **Presence by habitat and seed:**
  - each kind is present where its habitat exists, with a chance by its rarity (common: always; local: usually; scarce: sometimes,
    few; rare: seldom, one or two);
  - the world's seed draws it, and a world file can pin a kind in or out.
- **Not everything everywhere:**
  - a fen world: eels, fowl and fen fish in thousands, hares on its islands, no bear;
  - a wildwood frontier: deer, boar, wolves, bees, perhaps the bear;
  - a coast: fowl, salmon in the estuary, perhaps falcons on its cliffs;
  - downland: hares, little else.
- **Legendary individuals:** a rare, named animal as an individual on demand (living_populations §3): the white hart (an omen), the
  great boar of a wood, the old dog-wolf. Seldom, and only where its kind lives.

## 8. The first web of interactions

| Eater | Eats | Effect people see |
|---|---|---|
| deer | young growth, grass, crops at night | coppice that will not regrow; grazed young crops |
| boar | mast, roots, crops | rooted fields |
| hares | grass, young crops | nibbled field edges |
| wolves | deer, boar young, then herds and carcasses | a missing calf; howling near the village in a hard winter |
| bear | honey, carrion, beasts | a raided hive or carcass |
| fox | hares, carrion, lambs | |
| otter | fish | fewer fish at the weir |
| beaver | trees by the water | felled trees, a dam, a new pond and wet ground (a change of land, D4-103 mechanism 5) |
| ravens | carrion | circling ravens: a sign of death |

## 9. Waves

| Wave | Kinds | With which step of living_populations | Why first |
|---|---|---|---|
| 1 | red deer, hare, trout, eel, salmon, wildfowl, raven | steps 1 and 2 (the field; runs) | food and hides with uses now; the river commons; signs; the observability core |
| 2 | wolf, wild boar, fox, wild bees | step 3 (a predator) | danger, crews, crop and herd damage, honey |
| 3 | beaver, otter, pine marten, brown bear, falcon, swan | after wave 2 | rarity, prestige, furs and land change; waits partly for clothing and trade value |
| later | rats, rabbits, pigeons, fishponds, deer parks, hives, hounds | with husbandry and L-36 | wild kinds under husbandry, and pests in stores |

## 10. Management: what each invites

| Kind | Rules societies made | What the experiment can ask |
|---|---|---|
| salmon, eels | weirs held as rights; weirs removed by law; closed times | does the downstream village restrain, trade or fight? |
| deer, boar | forest law; the lord's beasts; poaching punished | who takes the rights, and is it enforced? |
| beaver, marten | none, historically: trapped out | does open access drive a slow breeder out? |
| wolves | bounties, drives, the watch | does a common threat produce collective action? |
| wildfowl | decoys held as rights; seasons | |
| bees | a hollow tree marked as someone's | do claims on wild things appear? |

## 11. Other kinds and niches considered (8 Nov)

Zach: "Are there any others we would want to consider? Any other needs or niches in the world we could fill?" Each candidate below
fills a niche the world lacks. Those marked **new purpose** add something the 17 kinds do not.

| Candidate | Niche it fills | Why it is interesting | When |
|---|---|---|---|
| **Wild plants as kinds:** hazel nuts, berries, crab apples and sloes, mushrooms (some poisonous), herbs | foraging is one generic stock today | **new purpose: knowledge as safety.** A wrong mushroom harms, so who knows what is worth something. Seasons: nuts and fungi in autumn, berries in summer. | with wave 1 or 2 |
| **Medicinal herbs** | no healing exists | the healer's materials, when disease comes (Q-16) | with disease |
| **Crows and rooks on sown fields** | children have little work | **new purpose: children's work.** Bird-scaring was a child's job. A field watched loses less seed. | with wave 1 |
| **Mosquitoes and the fen ague** | the fen is rich but has no cost | **new purpose: a place that feeds but sickens.** Malaria (ague) was real in the English fens. | with disease |
| **Ticks** | deer bring a cost to people | a disease carrier from wild beasts | with disease |
| **Mast** (acorns, beech nuts) as a stock | boar and pigs need it; mast years swing | pannage: the right to turn pigs into a wood (D2-76's mast eras) | with boar (wave 2) and pigs (L-36) |
| **Seals** | the coast has no large game | meat, oil and skins from the shore | with the coast |
| **Seabirds and their eggs** | the coast in spring | **new purpose: dangerous gathering:** climbing cliffs for eggs | with the coast |
| **A stranded whale** | a windfall | **a rare event worth a fight:** meat and oil for a whole village, and the Crown's claim on "royal fish" | an incident, with the coast |
| **Lampreys, crayfish** | river variety | a delicacy (lampreys were royal fare) | later |
| **Wild materials:** withies and willow, rushes, bracken, heather, gorse | building, bedding, light and oven fuel come only from trees and straw | baskets and traps (withies); bedding (bracken); thatch (heather); gorse burns hot (ovens) | with the water proposal's reeds and peat |
| **Oak galls** | writing has no ink | ink, for documents | with documents |

**A chain worth noting: writing is made from wild things.**
- parchment from hides (calf or deer);
- quills from goose feathers;
- ink from oak galls;
- seals from beeswax.

So the information economy (documents, letters, records) would depend on hunters, fowlers and honey-gatherers. That is a dependence
the design guide likes, and a reason furs and feathers are not only trade goods.

**Needs the world has no system for, and which wildlife would supply:**
- **clothing and warmth:** furs, leather (L-14, parked);
- **light:** tallow from fat, rushlights, wax candles (no light need exists);
- **health:** herbs (Q-16);
- **writing materials:** as above.

Each waits for its need to exist; wildlife then supplies it without a mechanism of its own.

**Domestic kin of wild kinds** (L-36):
- dogs (hounds, watch and herd dogs, D2-196);
- cats against rats;
- poultry (eggs; foxes take them);
- pigs on mast;
- sheep (wool; foxes and wolves take lambs).

## 12. Does this all work as data, or need one-off code?

Almost all of it is data, on seven general mechanisms. Each mechanism serves many kinds; no kind needs code of its own. Most are
already in D4-103's list of mechanisms to design in (process_model.md):

| Mechanism | What it carries | Status |
|---|---|---|
| **1. The population field**, the movement rule and observation | where every kind lives and moves; resident ranges, seasons, migrations; the collapse | proposed (living_populations.md) |
| **2. Diet**, between populations and stocks | predators and prey; grazers and young growth; pests on crops and stores; mast; otters at weirs | proposed (living_populations.md, "eat"); D4-103 mechanism 3 ("stocks that act on each other") |
| **3. Acts as processes, with yields as distributions** | every technique and its skill; gear multipliers; the wrong mushroom as an outcome that harms; danger as a wound or death outcome (D2-193) | built in part (D4-103 parts 1 and 2; mechanism 7: hazards as distributions) |
| **4. Work by several at once** | boar hunts, drives, weirs, a whale on the shore | designed (D4-103 mechanism 1), not built |
| **5. Trained and led beasts as tools** | hounds, hawks, ferrets; like the pack ox they go with a person and multiply some techniques; their needs | led beasts exist (D4-58); beasts' needs designed (D4-103 mechanism 8); "a beast as a tool" is the general step |
| **6. Presence that deters** | a watch, a scarecrow, a child bird-scaring, a fence, dogs: people's presence lowers a kind's habitat score or its take on a place | new, general: one term in the movement rule's habitat score |
| **7. Land changed by animals and people** | beaver dams making ponds; deer stopping coppice; felling moving the animals | designed (D4-103 mechanism 5) |

**What stays a row, not code:**
- every kind (a RESOURCES row with population fields);
- every good (ITEMS);
- every technique (TECHNIQUES, with skill and gear);
- rights (claims, D2-194);
- signs (the sign rules);
- rare events such as the whale (the scheduler's incidents, when built);
- legendary individuals (individuals on demand);
- seasons (clocks);
- packs to switch any of it on or off (D4-104).

**Where one-off code could creep in, and the general form to use instead:**
- **A "wolf raid" handler.** Use the diet term plus the movement rule, with incidents raised from what happened, not scripted.
- **A beaver-dam special case.** Use land change by an act or a population's effect on a patch.
- **Per-kind hunting code.** Use techniques with yield distributions and hazards.
- **Disease from fens.** Use hazards that read a place's state, when disease is designed.

## Cautions

- **Seventeen kinds is a catalogue, not a first build.** Wave 1 has seven, and only four of them are taken in new ways.
- **Wild food must not dominate.** It is a buffer and a pulse (fowl in winter, runs in autumn). The capacity model counts each
  kind's sustainable take, and the 30% rule holds.
- **Value needs uses.** Furs, wax and antler wait for clothing, documents and tools.
- **Calibration:** predator and prey numbers, and boom and bust, are tested over simulated years before any run.

## Open questions (for Zach)

1. ~~The four waves, and wave 1's seven kinds?~~ Decided: D2-192.
2. ~~Danger~~ Decided: D2-193.
3. ~~Royal kinds and rights~~ Decided: D2-194.
4. ~~Legendary individuals~~ Decided: D2-195.
5. ~~Hounds and hawks~~ Decided: D2-196 (hounds in wave 2 with the wolves; hawks in wave 3 with the falcon).
6. Which of §11's candidates to add, and when? Wild plants as kinds (knowledge as safety) and bird-scaring (children's work) fit wave 1.

## History

- 8 Nov: Zach asked for the first key kinds, with diversity, value for different reasons, rarity, kinds hard to take without a
  specialist, richness that is not everywhere at once, the purposes they serve, and the roles wildlife played in real life. 37.2
  proposed 17 kinds in four waves.
- 8 Nov: Zach: "Yes to all" to questions 1 to 4: decided as D2-192 to D2-195 and written into spec/environment/wildlife.md. Question 5
  (hounds and hawks) asked again with what hounds do.
- 8 Nov: Zach: "Yes" to hounds in wave 2 and hawks in wave 3 (D2-196). Then: "Are there any others ... Any other needs or niches ...
  would all of these work in the engine as data ... rather than one off fixes?" Added §11 (candidates and niches) and §12 (seven
  general mechanisms; none per kind).

- 9 Nov: §12's "no kind has code of its own" replaced by D2-203: each kind's behaviour is designed first and built as a
  module of its own, acting only through the animal interface and the engine's primitives (wild_behaviour.md). The rule had been
  meant to stop one-off handlers; in the build it flattened the kinds' behaviour into settings of one machine (02zq).

## Sources

- proposals/living_populations.md (the mechanism), water_and_preservation.md, ecosystems.md, temperate_landscapes.md (D2-191);
- engine data (TECHNIQUES, ITEMS: hides' uses);
- D2-23 (traps), D2-76 (mast eras), D2-77 (wolves), D2-95 (scavengers);
- OPEN L-2, L-13, L-14, L-36, L-37, L-48;
- history: the Charter of the Forest (1217); Magna Carta (1215) clause 33 on weirs; Domesday's eel renders; the beaver's extinction
  in Britain by about the 16th century.
