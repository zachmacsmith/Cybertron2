---
id: docs/review/37_growth/02zzj_economy_research/09_engine_mapping.md
kind: note
updated: "2026-11-15"
---
# 09: Mapping economic layers onto the engine, from foragers to the modern city (15 Nov 2026)

*note · `docs/review/37_growth/02zzj_economy_research/09_engine_mapping.md`*

> The engine already holds a whole village economy as physics. Goods sit in containers at places (`world.py`). Acts are data rows with inputs, fittings, tool tiers and skill (`TECHNIQUES`, `knowledge.py`). Buildings carry fittings, and those fittings are the capital (`FITTINGS`, `buildings.py`). Land 


Part 9 of the economy research folder (WORK [[W-40 Economy research, hunter-gatherers to the 21st-century urban economy|W-40]]). Zach (15 Nov), through the coordinator: map every layer, from
hunter-gatherers to the urban economy of the 21st century; say what representation each would need and which engine primitives;
show feasibility as how far each layer is from the engine, not as a cost cut-off; keep the notes on cost as information, not limits.
This is analysis to think with. Nothing here is proposed for building, and nothing is decided.

**What I read.** The engine on `main` at `bdfad76` (39 goods, 93 techniques, 14 fittings in `cybertron2/engine/data.py`), and the
branch `peoples-worlds` at `2020b9e`, the version the peoples run used (63 goods, 123 techniques, 15 fittings; it adds
`engine/wild.py`, `engine/parties.py` and the `cybertron2/wild/` package with the ecology). Where the two differ I say which. The
spec is `docs/cybertron2/spec/` as of 23 Oct to 13 Nov. Cybertron 1 is at `/home/user/cybertron/cybertron/`. Its institution layer
is a likely porting source.

## Summary

The engine already holds a whole village economy as physics. Goods sit in containers at places (`world.py`). Acts are data rows
with inputs, fittings, tool tiers and skill (`TECHNIQUES`, `knowledge.py`). Buildings carry fittings, and those fittings are the
capital (`FITTINGS`, `buildings.py`). Land is held as claims with bundles of rights (`world.rights`). Offers and agreements are
made of legs and settle each day (`agreements.py`), and work can be a leg. People are born, come of age as agents, and die
(`life.py`). Goods, people and news move only by being carried over roads that take whole days ([[D4-9 Transport and communication between nodes are delayed and carried|D4-9]], [[D4-35 Everything happens in a place|D4-35]]). Above the village
the engine thins out fast. The only kind of institution in use is the household. Ledgers, bonds, notice and remedies are decided
in the spec ([[D2-33 Ledgers|D2-33]], agreements.md) but not built. Prices as dated beliefs ([[D2-29 Prices are only what agents witnessed or were told|D2-29]]) and letters (letters_and_documents.md) are not
in the code. Standing orders exist only for children ([[D2-148 A child's menial work is set by the household head's standing order|D2-148]]). No act enforces anything. So the next layers (lordship, the market
town, merchants) need **social primitives** more than new goods: parties beyond the household, standing relations, ledgers,
enforcement by people, and records that others can see. Most of these are designed already, and Cybertron 1 built several of them
(`courts.py`, `institutions.py`, `credit.py`, `lawlang.py`).

Past the market town the obstacle changes. It is no longer missing primitives but **representation**. Every person is an LLM agent
called two to four times a day (38.42). A town of two thousand would be about 64,000 agent-days a year. The engine's own rule
caps a node at 15 to 20 people (places.md) and lets everyone at a node hear and trade with everyone else ([[D4-35 Everything happens in a place|D4-35]]). So proto-industry,
the state, the industrial economy and the modern city each need some mix of five things. (1) **People who are not agents:** rule-run
households and populations stored as numbers by place. The engine already has two precedents: children on the head's standing
order (`life.children_work`) and the wild ecology's population store (`wild/ecology.py`). (2) **Agents as the poles of
leverage:** heads, office-holders, entrepreneurs, officials. (3) **Aggregate production and markets.** The capacity model
(`cybertron2/capacity/`) already computes the output of land from the engine's own rules. (4) **A hierarchy of places:**
districts, towns, regions and countries. (5) **Time at more than one rate.** By distance from the engine: foragers and lasting
villages are here now. Lordship and the market town need modest additions. Merchants, proto-industry and the early state need
major social additions on the same kernel. Industrial and modern economies need a second, aggregate layer that the agent-level
engine sits inside. The modern economy's defining parts are firms of thousands, finance, fast information networks and
technology as a growing set of capabilities. They are far from the engine but not outside its principles, provided the aggregate
layer keeps the rule that everything happens in a place.

## 1. The kernel: what the engine is, and what any layer must respect

Every layer above has to sit on, or knowingly relax, five properties of the engine.

| Property | Where | What it means for an economy |
|---|---|---|
| **Everything happens in a place** ([[D4-35 Everything happens in a place|D4-35]]) | `world.py` (`place_of`, `apply` raises `PlaceError`) | a price, a default or a law is known only where someone saw it or carried word of it; no global market can exist unless it is a place |
| **One chokepoint for change** | `World.apply`, the journal (`journal.py`, spec/record/) | every transfer, act and settlement is a logged event, so national accounts, price series and the flow of goods can be read after a run without any extra mechanics |
| **The world grows by data** ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]]) | `data.py`; one handler each for gathering and work, making, and building (`verbs.py`) | new goods, acts, fittings and presets are rows; a deeper economy costs data, not code, until it needs new kinds of relation |
| **People know only what they learned** ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]], [[D4-33 Seeded knowledge of other lines' crafts is awareness, not skill|D4-33]]) | `knowledge.py` (levels aware, rough, capable, known; `options`) | each person's prompt lists only the methods they know, so a richer catalogue does not lengthen every prompt |
| **The engine settles physics; people settle the social** (holding.md: "the engine enforces only possession") | `world.rights`, `agreements.settle` | the stated principle holds for claims. The exception is goods credit, which the engine pays automatically ([[D2-32 The settlement rule|D2-32]], OPEN [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]) |

Scale constants that bound every layer:

| Constant | Value | Source |
|---|---|---|
| a round | one day | [[D4-13 A round is a day|D4-13]] |
| a year | about 16 to 60 days; 32 in current worlds (8-day seasons) | calendar.md; peoples_benchmark.md §5 |
| work units a day | summer 7, autumn 6, winter 5, spring 6 | agents/work.md |
| a lifetime | 32 days by default, 64 in the peoples worlds | [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], [[D4-116 Lifespan 64 in the peoples worlds; the year unchanged|D4-116]] |
| a node | a place one can reach and return from before nightfall; about 15 to 20 people at most | [[D4-2 A node is a village, a valley or a camp|D4-2]], [[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]], places.md |
| a road | whole days at about 17 to 18 km a day (×1.5 over hills) | 38.69 §3 |
| a carry | 10 on foot, 20 with a pack, 60 with a pack ox, 40 with a handcart on a track | [[D2-135 Carrying capacities (OPEN C-1)|D2-135]], `ITEMS` `carry` |
| calls a person a day | about 2.4 to 3.7 with the evening | 38.42 |

## 2. What the engine already provides, layer by layer

E = in the code on `main`; W = only on `peoples-worlds`; S = decided in the spec but not built; P = proposed (economy_web.md,
02zzh, briefs).

| Layer | What exists | Files | Gaps that bite first |
|---|---|---|---|
| **Goods** | 39 goods (E), 63 (W), each with weight, food value, spoilage, decay by condition, heat, tool grade, uses before wearing out; resources on parcels as logistic stocks (S, K, r) | `data.py` ITEMS, DECAY, RESOURCES; `renewal.py`; `wear.py` | most goods are one step from the land (02zzg); no quality grades (by design, 02zzh §6); no containers that hold items |
| **Production** | 93 techniques (E), 123 (W): gather, work, make, build; inputs, `at` covers or fittings, tool multipliers (bare, crude, copper), skill by practice from novice to master ([[D2-52 Skill by practice on all work|D2-52]]), trades | `data.py` TECHNIQUES, SKILL; `verbs.py`; `knowledge.py`; `farm.py` (fields, soil, crops by season) | all production is a person's units on a day; no production that runs by itself; no output in batches over days except buildings and crops |
| **Capital** | fittings as capital (hearth, oven, anvil, millstones, water wheel, granary, cellar, vault), rooms by structure, tiers of extravagance, wear and mending (the oven's relining, the leat's silting) | `FITTINGS`, `ROOMS`, `BLUEPRINTS`; `buildings.py`; [[D2-154 One unit of space at every level|D2-154]] to [[D2-171 Extravagance in tiers|D2-171]], [[D4-105 Sowing windows are lore, not rules|D4-105]] | no capital owned by more than one party except joint claims; no depreciation in money terms (only physical wear); no machines that need power other than oxen and the river |
| **Labour** | units a day; work costs food (`labour.py`); fatigue from pushing on; skill fades; acting **for** a party (`for`), with the employer's tools ([[D2-37 Acting for others|D2-37]], [[D2-38 A worker acting for an employer may use the employer's tools in its…|D2-38]]); work legs counted from the action record ([[D2-36 Work can be a leg|D2-36]]); teaching and watching | `labour.py`; `verbs.py` `for`, `teach`, `learn`, `watch`; `settle.settle_teaching`; `agreements.settle` (work legs) | no wage relation that lasts beyond a counted number of days; no hiring market; children's work is the only rule-run labour |
| **Exchange** | offers to one person or to anyone at the node, in lots; accept, withdraw; spot trades settle both legs or neither; meetings called for the morning ([[D4-77 The evening's add-ons|D4-77]]), where all who come witness what is offered | `agreements.py` (`make_offer`, `accept`); `prompt.py` "Offers open here"; `evening.py` meetings | offers are seen only at their node; no price memory in code ([[D2-29 Prices are only what agents witnessed or were told|D2-29]] is S); no market as a mechanism ([[D2-30 Markets are seeded custom|D2-30]]: seeded custom, as in `specs/region.yaml`'s Millford market every third day) |
| **Money** | copper coin, weight 0, struck at an anvil (10 coin a copper), seeded in most worlds | ITEMS `coin`; TECHNIQUES `coin` | money is given, not emergent (38.68); grain is the de facto unit of account; no issuer but any smith |
| **Credit** | legs `by` a day, `every` n days `for` k times, work legs, land legs (plots); arrears; release and forgiveness ([[D4-37 Whoever is owed may count a debt paid|D4-37]]); goods given to a creditor credited automatically | `agreements.py` (`parse_legs`, `settle`, `_credit`, `release`) | goods legs paid by the engine when both parties are at one node ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]); no interest, bond, notice, remedy, carrier or ledger in code (all S) |
| **Property and institutions** | claims on fields (in plots), buildings and herds, with rights (access, withdrawal, management, exclusion, alienation); households with a head, members, rules for admitting and granting; join, admit, found, leave; heirs; host and grant | `world.py` (`claims_on`, `rights`, `may_grant`, institutions); `verbs.py` `claim`, `grant`, `join`, `found`, `name` | institutions are households only (`kind: household`); no offices but the head; no rules that create obligations; no enforcement acts ([[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]]) |
| **Transport** | roads in days, with tracks or not; travel at nightfall; carrying capacity by means; the pack ox led; hidden ways; meetings on the road; goods left at a door | `roads.py`; `world.capacity`; ITEMS `pack`, `handcart`; [[D2-135 Carrying capacities (OPEN C-1)|D2-135]], [[D2-136 The pack ox|D2-136]] | no carts drawn by oxen (spec says later), no boats or water edges, no bridges or fords as works; the region run's trade was capped by carrying (38.26) |
| **Information** | perception by senses and noticing; signs; speech (to a person, which wakes them, or to all at the place); lines written on buildings and monuments (the `write` verb); one memory each agent rewrites ([[D4-61 An agent rewrites its one memory each stretch, within a length that…|D4-61]]); customs and lore as kept lines | `perceive.py`, `signs.py`, `memory.py`, `lore.py`, `verbs.py` `write`; spec/information/ | letters and documents (S) not built; witnesses of agreements recorded but not perceived (38.68); no record that a third party can consult |
| **Population** | births by choice, pregnancy, nursing gap, care, coming of age as an agent with the household's model ([[D4-117 A youth's model is its household's|D4-117]]), old age, illness, starvation; a generated population with kin and history (`generate.py`, the backward people build in `proto/peoplegen/`) | `life.py`, `needs.py`, `night.py`, `generate.py` | every youth becomes an agent, so cost grows with success ([[L-104 MAJOR the descendants benchmark|L-104]]); no migration by rule |
| **Environment** | climate and weather, seasons and daylight, forests, soil fertility, crops by season, herds that breed and stray; the wild ecology: every kind's numbers in every area, stepped daily by rules (W) | `climate.py`, `environment.py`, `forests.py`, `farm.py`, `herds.py`; `wild/ecology.py` (W) | the ecology is the engine's one population run by numbers, not individuals, and the model for doing the same with people |
| **Measurement** | carrying capacity at five levels (bare, as it stands, worked, best, ceiling) computed from the engine's own tables and functions; the economy map (02zzg) read from the tables | `cybertron2/capacity/` ([[D4-102 Carrying capacity is measured, by level, from the engine's own rules|D4-102]]); `docs/review/37_growth/02zzg_economy/economy_graph.py` | this is an aggregate production model already, but it is used only to check worlds, not to run any part of them |

**Two readings of the table.** First, the material side is broad and grows by rows. economy_web.md's fifteen chains (leather,
the coppice, cord, the weir, the smokehouse) are all within the existing handlers. Second, the social side is a skeleton.
agreements.md lists eighteen presets (wages, rent, tenancy, sharecropping, apprenticeship, dues and taxes, the carrier, the
shopkeeper, the guard). The code can express only some of them, and only as legs counted day by day. There is no notice, no
remedy and no party that is neither a person nor a household. The first layers past the village are limited here.

## 3. A catalogue of primitives the further layers need

Each layer in §4 is a combination of these. I name them once so the layers can cite them. "Kernel" means the primitive fits the
five properties of §1 without relaxing any of them.

| # | Primitive | What it is | Nearest existing piece | Kernel? |
|---|---|---|---|---|
| **P1** | **Parties beyond the household** | an institution of any kind (a village, a lord's house, a partnership, a guild, a firm, a church, a state) with members, offices, a seat, a container and rules; able to hold claims and be a party to agreements | `institutions {kind, members, offices, rules}` in `world.py` already has the shape; `for` already acts for any party; Cybertron 1's `institutions.py`, `incorporation.py`, `roles.py`, `positions.py` | yes |
| **P2** | **Standing relations** | a relation that lasts until notice and carries duties both ways: employment for a wage, tenancy, service, apprenticeship, membership dues | `every` legs and work legs in `agreements.py`; the presets in agreements.md (S) | yes |
| **P3** | **Ledgers and accounts** | a container at an institution's seat where each holder has a share; payments between shares are record changes, so they run at a distance ([[D2-33 Ledgers|D2-33]]) | [[D2-33 Ledgers|D2-33]] decided; shares as claims (holding.md); Cybertron 1's `accounts.py`, `credit.py` | yes: the ledger is at a place and deposits are physical |
| **P4** | **Enforcement by people** | acts that act on another person or their goods under a claim of right: detain, fine, distrain, confiscate, exile, evict; and goods credit paid by a deliberate act, not by the engine ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]) | `attack`, `guard`, `take` (theft is recognised); [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]]; Cybertron 1's `courts.py`, `conflict.py` | yes, and it removes one exception to "the engine settles only physics" |
| **P5** | **Visible records and reputation** | agreements and defaults perceived by witnesses; documents as goods (a tally, a bond, a charter, a register) that can be carried, read, forged and lost | witnesses stored in each agreement; `write` on buildings; letters_and_documents.md (S); Cybertron 1's `documents.py`, `registers.py`, `papers.py` | yes |
| **P6** | **Markets as places and days** | a known place and day where offers are posted, prices are seen and remembered with their date, and traders gather | seeded market custom ([[D2-30 Markets are seeded custom|D2-30]], `specs/region.yaml`); morning meetings ([[D4-77 The evening's add-ons|D4-77]]); open offers to anyone | yes |
| **P7** | **Rules that create obligations** | an institution's code that creates legs: rents, dues, tolls at a gate or ford, tithes, taxes, levies of labour, fines; and who may change the code | presets "dues, levies, fines, taxes: legs created by an institution's code" (S); Cybertron 1's `lawlang.py`, `laweffects.py`, `jurisdictions.py` | yes |
| **P8** | **Public works and shared capital** | works owned by an institution and built by a crew over days (a bridge, a mill, walls, a drain), with upkeep paid by levy and access by rule | `build` over days with `for`; fittings with wear and mending; joint claims | yes |
| **P9** | **Rule-run people** | households and persons who eat, work, breed and move by rules, not by a model call; directed by an agent's standing orders or by a policy | children on the head's order (`life.children_work`, [[D2-148 A child's menial work is set by the household head's standing order|D2-148]]); the scripted `bot_plan` in `run.py` and `model: bot` (`life.come_of_age`); standing orders for adults ([[D4-16 Routine work runs on standing orders the agent sets|D4-16]], S) | yes |
| **P10** | **Populations as numbers by place** | a block of people (a village's labourers, a town's ward, a county) stored as counts by age, skill and holding, stepped by rules: births, deaths, work, consumption, migration | the wild ecology's population store (`wild/ecology.py`: counts by area, stepped daily, keyed draws) | relaxes "every person is an entity"; keeps place |
| **P11** | **Aggregate production and supply** | a block's output as a function of land, labour, capital and technique, with costs that rise with output (a supply curve); bulk goods as flows | `cybertron2/capacity/` (yield by level, labour share, the year simulated) | relaxes "every act is a person's units" |
| **P12** | **Market clearing for aggregates** | prices formed where aggregate supply meets the demand of blocks and the offers of agents, at a market place on its day | none; Cybertron 1 had no clearing either | needs a mechanism the engine has refused so far ([[D2-29 Prices are only what agents witnessed or were told|D2-29]]: no computed price shown). It can keep [[D2-29 Prices are only what agents witnessed or were told|D2-29]] if the cleared price is a posted price seen at the market and carried from there |
| **P13** | **A hierarchy of places** | districts inside a town (where presence is not "everyone hears everyone"); towns as clusters of nodes ([[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]]); regions and countries as aggregate places with their own stocks and flows | buildings already scope some hearing ([[L-70 The claims fixes|L-70]]); clusters ([[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]]); the capacity model's region (`capacity/space.py`) | yes, if each level is a place |
| **P14** | **Edges with kind and capacity** | water (river, coast, sea), carts on tracks, canals, rail, pipelines, wires; each with speed, capacity, cost and owner; tolls | roads with `days`, `track`, hidden ways (`roads.py`) | yes |
| **P15** | **Information that travels faster than goods** | post, couriers, the press, the telegraph, telephones and networks: an edge that carries messages but not goods, built and owned | [[D4-35 Everything happens in a place|D4-35]] allows anything carried; speech and messages within a node | yes, if the wire or the courier is in the world |
| **P16** | **Technology as capabilities** | techniques as data ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]]) plus discovery ([[L-103 Crafting and discovering new things|L-103]]); at the aggregate level, a technology as a shift in a production function, a new energy source or a new fitting class (engines, machines) | TECHNIQUES; KNOWN_SOMEWHERE; LEVELS | yes |
| **P17** | **Financial claims** | shares in an institution's ledger, bonds, bills of exchange, notes issued by an institution, interest, insurance pools, a lender of last resort | shares as claims (holding.md); the loan preset with interest (S); "institution-issued notes: later" (agreements.md Open) | yes, on P1 and P3 |
| **P18** | **Time at more than one rate** | agents called less than every day (standing_orders.md Open); aggregate blocks stepped by the season or the year; history runs before agents arrive | the generator's simulated people tree (`generate.py`); the ecology spun from the land; the capacity model's simulated year | yes |

P1 to P9 are **social primitives inside the kernel**. They need code, but no new kind of representation, and most are already
designed. P10 to P12 are a **second, aggregate layer**. P13 to P18 **extend place, edges, knowledge and time**. Some of those are
needed early (P14's water and carts for the market town), others late (P15's wires).

## 4. The layers, one by one

For each layer: what the engine has, the primitives it needs, how it would be represented, and how far it is from the engine.
The sequence follows 02zzi §3, extended at both ends. Real societies skip, combine and reverse these types (02zzi §8).

### 4.1 Foragers and bands

- **The economy:** gathering, hunting, fishing; sharing as the rule; gifts; little stored wealth; mobility.
- **In the engine:** forage, hunt the wild with skill and parties (W: `parties.py`, brief 4c), snares, fish by hand and angle, dry
  meat at a fire ring, camps ([[D2-68 Camps and portable shelter|D2-68]]), give, host. Agents already fall back to this when farming fails (02zzi §3.1). The wild
  ecology gives game that is wary, moves and recovers (W).
- **Needs:** mobility of a whole household (a camp that travels, goods carried by all); seasonal rounds over many nodes; sharing
  norms that are customs, not engine rules (customs as kept lines already exist, `perceive.py`).
- **Representation:** every person an agent; bands of 10 to 30 fit the node cap.
- **Distance:** **here now.** The only missing parts are ergonomic: moving a household's camp in one act, and the bow and the
  spear (P in economy_web.md §2.10).

### 4.2 Settled farming villages that last

- **The economy:** households farming their own land, kin and neighbours for big jobs, stores against the lean season, gifts and
  help. 38.68 found exactly this in the runs: gifts to the hungry, room and board for work, private ledgers.
- **In the engine:** all of it, with the stage-1 web (leather, withies, cord) proposed (economy_web.md). The capacity ladder sets
  what good farming yields ([[D4-102 Carrying capacity is measured, by level, from the engine's own rules|D4-102]]).
- **Needs:** commons rules (the coppice's rotation, the river) as customs agents make and keep; long horizons (runs of a season or
  more, 38.68's test); teaching across generations (exists); the fixes 38.70 found in the peoples worlds.
- **Representation:** every person an agent, 10 to 60 people.
- **Distance:** **here now.** The question is calibration and run length, not primitives.

### 4.3 Lordship and redistribution

- **The economy:** a lord, chief or temple takes a share of the surplus (labour days, rents in kind, tribute) and gives back
  protection, justice, feasts and big works.
- **In the engine:** a lord can be a household holding the mill, the oven or the best land (the water wheel costs 250 units and 60
  timber, `FITTINGS`), and can lease it under the rent preset by `every` legs. Work legs can stand for labour dues. Guarding exists.
- **Needs:** **P1** (the lord's house as an institution with a steward and a reeve, not only a head); **P2** (tenancy and service
  until notice); **P7** (dues created by a rule, falling on every tenant, not agreed one by one); **P4** (distraint for unpaid
  dues, eviction, a lord's court); **P8** (the lord's mill with a multure taken per batch: a `per` leg on the `mill` technique's
  output); **P5** (a manor roll as a document).
- **Representation:** every person an agent, or the lord's tenants as agents and their dependants rule-run (P9). A manor of 100 to
  200 people is several nodes.
- **Distance:** **modest additions.** Everything is on the kernel; P2 and P7 are mostly the decided presets made real. The one
  design choice is [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]: whether dues are paid by the engine or by the tenant's act.

### 4.4 Market towns and regional specialisation

- **The economy:** a market in a known place on a known day; villages specialise by their land, towns by craft; coin in common use.
  Smith's rule: the division of labour is limited by the extent of the market.
- **In the engine:** seeded market custom (Millford in `specs/region.yaml`: "Market day at Millford is every third day, on the
  Square"); a merchant household with handcarts and 40 coin ([[D2-2 One merchant household with a cart is seeded in the first region|D2-2]]); open offers to anyone; morning meetings. The region run
  (38.26: 58 people, four villages) traded 2 to 5 timber at a time, held back by carrying on foot.
- **Needs:** **P6** (posted offers that outlast the offerer's presence through a stall-keeper ([[D4-17 Units a day and the action cost table are settled by experiment|D4-17]]), and prices remembered
  with their date and place, [[D2-29 Prices are only what agents witnessed or were told|D2-29]]); **P14** (ox carts on tracks, 300 to 400 a load, already in transport.md as later; river
  boats); **P5** (weights and measures as a public standard; the market's peace); **P7** (tolls, stall fees, [[D2-30 Markets are seeded custom|D2-30]]); **P13** (a
  town of a few hundred as a cluster of nodes, with a square where all who come can deal).
- **Representation:** a town of 200 to 500 is 10 to 30 nodes at the current cap. It can be all agents at high cost (§5), or agents
  for heads, traders and craft masters with the rest rule-run (P9).
- **Distance:** **modest to major.** P6 and P14 are modest. A town larger than a cluster of 10 nodes needs P13's districts,
  because presence within a node is shared by everyone in it.

### 4.5 Merchants and commercial economies

- **The economy:** merchants carry goods between regions; credit across distance and time; partnerships; guilds that control
  entry; written contracts and courts. North: trade grows as the cost of making and enforcing deals falls.
- **In the engine:** the consignment and carrier presets (S); credit by a day (E); the merchant household ([[D2-2 One merchant household with a cart is seeded in the first region|D2-2]]); travel and pack
  oxen.
- **Needs:** **P1** (partnerships and companies as parties, with shares of profit); **P3** (ledgers at distant seats, so a debt in
  one town is paid in another: the bill of exchange); **P5** (reputation others can see; a written bond; a guild's roll of
  members); **P4** (a court or guild that rules on a breach, with the remedy column of agreements.md made real); **P14** (boats and
  sea edges; warehouses as stores at a port); **P15** (letters carried by couriers, so news of prices runs ahead of goods);
  **P17** (bills of exchange and interest).
- **Representation:** merchants, guild masters, factors and judges as agents; producers in distant regions can be aggregate (P10,
  P11), seen by the merchant only through what they offer at their market.
- **Distance:** **major additions on the kernel.** No step relaxes the kernel. Distant trading regions as aggregates are the first
  use of the second layer, and could start as fixed suppliers at the world's edge (an "outside" node with a schedule of offers).

### 4.6 Proto-industry (putting-out)

- **The economy:** a merchant gives raw material to rural households who spin and weave at home for piece wages between farm
  work, and collects the cloth. De Vries's industrious revolution: households work harder for the market to buy goods.
- **In the engine:** the piece-rate preset (S); `for` on make, so output goes into the merchant's container ([[D2-37 Acting for others|D2-37]]); the work leg
  counted per act.
- **Needs:** **P2** (piece rates: pay `per` unit of output made for the employer, a field the leg record already names); materials
  owned by one party and worked in another's house (the `for` container must be able to sit in another household's building);
  the cloth chain itself (flax or wool, retting, spinning, the loom: 02zzh tranche 5); **P9** (the spinners as rule-run households
  whose time is split between farm and loom by a policy, so a putter-out can reach hundreds); **P11** for villages beyond the map.
- **Representation:** the putter-out as an agent; a few households as agents; the bulk of the spinning population rule-run, each
  household's labour allocation a rule that responds to the piece rate and the price of bread.
- **Distance:** **major.** This is the first layer whose defining feature is many small producers, which makes P9 or P10
  necessary at any interesting scale.

### 4.7 States and fiscal power

- **The economy:** a state that taxes, borrows, keeps an army, makes law and coin, and builds roads, harbours and courts.
- **In the engine:** households, claims, guarding, attack; nothing above the household.
- **Needs:** **P1** at several levels (the crown, counties, towns, the church) with **membership of one institution in another**
  (membership.md already allows it); **P7** (taxes on land, trade or heads, by a rule, assessed from a register); **P3** (the
  treasury's ledger); **P4** (officials who collect, courts that rule, soldiers who coerce); **P8** (public works by levy);
  **P17** (state borrowing, coinage by an institution with a mint, debasement); **P13** (jurisdictions as places at a level
  above the node); **P15** (the post, so orders reach the counties).
- **Representation:** office-holders as agents (ruler, treasurer, sheriffs, judges, captains); the taxed population almost
  entirely aggregate (P10): counties as blocks whose output, tax base and willingness to pay are numbers, with a few agent
  villages as windows. Cybertron 1 is the closest precedent: its society was institutions and law (`lawlang.py`,
  `jurisdictions.py`, `courts.py`, `regimes.py`).
- **Distance:** **major, and the first layer that cannot be all agents.** A small city-state of a few thousand is 100,000 or more
  agent-days a year.

### 4.8 The industrial edge

- **The economy:** coal and steam replace wood and muscle (Wrigley's organic to mineral economy); factories gather work under one
  roof with power; canals and railways move bulk; wage labour becomes the norm; Allen's high wages and cheap fuel.
- **In the engine:** the water wheel is the one powered fitting; charcoal, timber and firewood have heat values (`ITEMS` `heat`);
  the organic ceiling is real, because fuel, food and timber all come from parcels with logistic renewal (`renewal.py`).
- **Needs:** **P16** (new energy as a resource: a coal seam is a `seam` like copper; the engine as a fitting class that turns fuel
  into power for other fittings, so a factory is a building whose fittings draw power); **P2** (wage labour as the main relation, a
  labour market where jobs are offered and taken); **P1** (the firm with an owner, managers and hundreds of workers); **P11** (the
  factory's output as a function of power, machines and workers, since nobody spins a thousand spindles one unit at a time);
  **P14** (canals and rail with capacity and owners); **P10** (the towns that grow round the mills, by migration from the
  country).
- **Representation:** owners, engineers, union organisers and magistrates as agents; workers as blocks by place and trade
  (P10), with a rule for taking or leaving jobs by wage and food price; factories as aggregate fittings (P11). A worker could
  become an agent when a role puts them at a pole: a foreman, an organiser, an inventor.
- **Distance:** **far.** The kernel holds, but most of what matters happens in P10 to P12, which do not exist. The energy step
  (P16) is cheap by comparison: a seam, a fuel, a fitting class.

### 4.9 The mature industrial economy

- **The economy:** corporations with limited liability; banks and stock markets; national labour markets; unions; mass
  production and mass consumption; railways and steamships; a central bank; cycles of boom and slump.
- **Needs:** **P17** in full (shares, bonds, deposit banking, money as ledger entries more than coin, a lender of last resort);
  **P12** (markets that clear across many traders, for goods, labour and capital); **P13** (cities of districts; a national
  economy as regions); **P15** (the telegraph and the press, so prices are known nationally within a day); **P7** (income and
  corporate taxes, regulation); **P18** (aggregate blocks stepped by the month or season; agents called when something reaches
  them).
- **Representation:** the agents are boards, bankers, ministers, union leaders and newspaper editors; firms are institutions
  (P1) whose production is aggregate; households are blocks. The engine's daily round survives as the agents' clock; the economy
  beneath runs at its own rate.
- **Distance:** **far.** It needs every second-layer primitive plus finance.

### 4.10 The modern urban economy (late 20th and 21st century)

- **The economy:** most work is services; most value is in information, organisation and intangible capital; global supply chains
  of many tiers; cities of millions with networks (water, power, transport, telecom); the welfare state; fiat money and central
  banks; digital platforms where the market itself is a firm.
- **Needs:** all of P1 to P18, plus:
  - **services as goods:** work done for others, not a thing. The engine already treats this right at the small scale: acts
    `for` a party, checked by the action record. At scale it becomes P11 for service sectors;
  - **infrastructure networks** (P14) as owned, priced, regulated edges: grids, mains, roads, fibre;
  - **technology as a growing capability set** (P16): R&D firms whose output is new techniques that others license, so knowledge
    becomes a good with property rights (patents as P7 rules over P16 rows);
  - **information goods with near-zero copying cost** (P15): an online market is a place in the network, not a square;
  - **the state as insurer** (P7, P17): pensions, health, unemployment, all transfers set by rule.
- **Representation:** the engine's agent layer becomes a set of seats: executives, regulators, politicians, journalists, a few
  households as windows on everyday life. Everything else is aggregate. The question is whether [[D4-35 Everything happens in a place|D4-35]] survives: whether the
  network is a place (a platform node that agents "go to" by a message edge) or a global commons.
- **Distance:** **far, near the edge of what the engine is for.** I would not call it out of reach. Each piece has a kernel-shaped
  version, and Cybertron's distinctive strengths (place, carried information, people who know only what they learned) are
  exactly what makes modern information economies interesting: who knows what, and when. But its centre of gravity would be the
  aggregate layer, and the agent-level engine would be the window on it.

### 4.11 Branches

| Branch | What it adds | Distance |
|---|---|---|
| **pastoral nomads** | wealth in herds; mobility; raiding; trade with settled neighbours | modest: herds, driving and leading exist (`herds.py`); needs herds at scale (P10 for beasts already has the ecology's machinery) and a household that moves |
| **river-irrigation states** | one large public work and the organisation it demands | major: P8 at scale (canals as a work of thousands), P7 (water rights by rule), water as a resource on parcels with flow between them |
| **maritime trading cities** | little land, much shipping, credit | major: P14 sea edges, P3, P17, P13 (a port of districts) |
| **frontier and colonial economies** | land plentiful, labour scarce | here to modest: vacant places exist in the peoples worlds ([[D4-118 The land generator takes a designed world|D4-118]]); settlement, claims on new land and the dependence on the home region are in place |

## 5. Representation and scale

### 5.1 What an agent costs (as information, not a limit)

| Measure | Figure | Source |
|---|---|---|
| cost per agent-day | Haiku $0.003, Sonnet $0.040, Opus $0.108 | 38.65 "Cost" (goal probe 3, rounds 1 and 2) |
| earlier estimate | Opus about $0.10, Sonnet $0.03, Haiku $0.003; prompts 1.3 to 1.4× longer since | 38.21 §4 |
| calls per agent-day | 2.4 to 2.5 without the evening, 3.7 with it | 38.42 |
| prompt size | about 7.4k input tokens a call in the first slice; a grown agent's system text about 3,700 tokens, could be about 1,500 | 38.11; 38.40 §3 |
| context growth if one conversation were kept for life | 12,000 to 25,000 tokens a day | 38.40 §10 |
| the region run | 58 people, 23 days, $33.99 (about $0.025 an agent-day, mixed models) | 38.26 |
| the peoples run | Opus against Sonnet, 10 to 24 people, 100 days, $212.91; stopped once at the 5-hour limit, on day 47 | 38.70 |
| the descendants benchmark, estimated | 40 agents over 150 days, 6,000 agent-days, $400 to $900 a run; 16 runs $7,000 to $14,000 before replicates | descendants_benchmark.md, risk 1 |

Runs go through the CLI against a subscription, so these are cache-equivalent dollars (38.40 §10). Wall-clock time is the other
cost: the peoples run took about five hours for 47 days of 20-odd people.

### 5.2 What the cost implies for population, if every person were an agent

At 32 rounds a year and about three calls a round. Cost per year is shown at a blended $0.03 an agent-day (mostly Haiku and
Sonnet, with Opus at the poles, as scenario_design.md asks) and at Opus throughout.

| Society | People | Agent-days a year | Calls a year | At $0.03 | At Opus ($0.108) |
|---|---|---|---|---|---|
| a village | 20 | 640 | about 2,000 | $19 | $69 |
| a region of villages | 150 | 4,800 | about 15,000 | $144 | $520 |
| a market town and its villages | 2,000 | 64,000 | about 200,000 | $1,900 | $6,900 |
| a county | 20,000 | 640,000 | about 2 million | $19,000 | $69,000 |
| a small kingdom | 1 million | 32 million | about 100 million | $960,000 | $3.5 million |
| a modern city | 5 million | 160 million | about 500 million | $4.8 million | $17 million |

A century of a village is 3,200 rounds and 64,000 agent-days. Cost is one constraint. The others bite earlier:
- **wall-clock time:** at the peoples run's pace (about six minutes a round for 20 people, mostly waiting on calls), a county's
  year is weeks even with heavy parallelism;
- **the node cap:** 15 to 20 people at a node (places.md), set so that one conversation can hold everyone present;
- **talk:** who hears whom grows with the square of the people at a place unless presence is divided (P13);
- **reading the run:** a qualitative end-state reading (scenario_design.md) of thousands of agents is itself a research project.

So the answer to "how far can all-agent representation scale" is a region of a few hundred people over a few years. Beyond that,
the representation has to change.

### 5.3 The ladder of representations

| Rung | Who is an agent | Everyone else | Engine today | Fits layers |
|---|---|---|---|---|
| **R0 all agents** | every youth, adult and elder | children rule-run | yes (`life.come_of_age`) | 4.1 to 4.3; 4.4 small |
| **R1 agents and standing orders** | every adult, but routine days run on their own standing orders and they are called less than every day | | standing orders decided for adults ([[D4-16 Routine work runs on standing orders the agent sets|D4-16]]), built for children only; "being called less than every day: later" (standing_orders.md Open) | 4.2 to 4.4 at two to five times the population |
| **R2 heads of household** | heads (and perhaps one heir) | members on the head's orders, like children now (P9) | children's orders; `order` verb; `model: bot` | 4.3 to 4.5 |
| **R3 agents at the poles** | lords, merchants, masters, officials, a few ordinary households as windows | rule-run households (P9), each a full entity in the world with goods, claims and a place | `bot_plan` (smoke tests only) | 4.5 to 4.7 |
| **R4 blocks** | as R3 | populations as numbers by place (P10), producing by function (P11), trading through markets (P12) | the wild ecology (`wild/ecology.py`); the capacity model | 4.6 to 4.9 |
| **R5 nested scales** | seats in the institutions of a large economy, plus a fully simulated window (a village, a ward, a firm) at R0 to R2 | the rest of the economy at R4, coupled to the window by prices, flows of goods and people, and news | none | 4.8 to 4.10 |

Three things decide whether a rung works. (1) **The agents must still matter.** Rule-run people should answer to what agents do
(a wage, a rent, a price, an order), and agents should face consequences from them (a strike, a migration, a bad harvest).
(2) **The rules for non-agents should be grounded** the way the ecology is: in the engine's own physics (food, units, spoilage,
yields), not in a separate economic model with its own constants. The capacity model shows this can be done; it computes from
`farm.soil_step`, `ITEMS` and `TECHNIQUES` and fails a test when the engine gains a food it cannot account for. (3) **The null
arm** (scenario_design.md): with rule-run people, the null is easy to build (all bots) and much more informative, because the
agents' effect is the gap between a bot-run economy and the same economy with agents at the poles.

**A history run before agents arrive** is a form of R4 in time. The generator already builds a people tree by simulating
backwards and forwards (`generate.py`; 02zzf: 17,110 simulated tries), and the ecology starts from the land. The same could give a
world its mill, its lord's claims, its debts, its roads worn by use and its customs before day 0, so a run can start at layer 4.3
or 4.4 rather than climbing from 4.2 within 100 days.

### 5.4 What changes in the prompt and the agents' load

| Step | What a person sees today | What would change |
|---|---|---|
| **village (now)** | their units; the methods they know ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]]: aware as a name, capable as a line; `knowledge.options`); what is here; offers open here; their agreements and arrears; their memory | nothing structural; economy_web.md adds lines only for those who practise a chain (02zzh §6) |
| **lordship** | as now | a steward sees the manor's roll and the dues owed; a tenant sees their dues; the court's day is a meeting ([[D4-77 The evening's add-ons|D4-77]]) |
| **market town** | offers at the node | the market's posted offers on its day; prices as last heard, with place and date ([[D2-29 Prices are only what agents witnessed or were told|D2-29]]), which is a new block of the prompt and grows with the number of goods and markets one knows |
| **merchant** | as now | letters received; accounts at distant ledgers; the bonds held; prices in several towns, each dated. The merchant's prompt is the longest; a merchant's own written ledger (a document) could replace engine-kept lines ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]'s direction) |
| **R2 head** | their own day | also the household's members, each with a line of what they did on the head's orders; the head's load grows with the household's size |
| **R3/R4 office-holder** | | reports as documents: a treasurer's account, a sheriff's return, a factory's books, a market report. These are information goods (02zzi §1) that someone made, that may be late or wrong, and that cost to produce. That keeps [[D2-29 Prices are only what agents witnessed or were told|D2-29]] and [[D4-35 Everything happens in a place|D4-35]]: nothing computed is shown unless an in-world record carried it |
| **R5 seat** | | aggregates as dashboards are the temptation. The rule that keeps the engine honest: a figure reaches an agent only through a document, a person or a published record made at a place |

The principle that people see only the methods they know ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]]) scales well in one direction: a deeper catalogue does not
lengthen the prompt. It scales badly in another. A head, a steward or an official sees more people and more records, so their load
grows with their reach. The design answer is the historical one: summaries made by subordinates, each a document with an author
(P5). The cost of governing then appears inside the world.

## 6. Time and space

### 6.1 Time

- **A year of 32 rounds with 8-day seasons** fits farming (a crop's growth is a share of the year, `CROPS`), but compresses
  everything else. A crop takes 8 rounds to grow, and so does a season's trading. A generation takes about 20 rounds at lifespan
  64 (peoples_benchmark.md §5).
- **Institutions change over decades.** A run of 100 to 200 rounds is three to six years. Lordship can form in that time;
  commutation of dues to money rents, guild formation, or the rise of a market town took generations. History runs (§5.3) and
  longer runs are the two ways in.
- **Multi-rate time (P18)** is the third way: agents keep the day, rule-run households keep the day cheaply (they are code),
  and aggregate blocks step by the season or the year. The ecology already steps daily over every area at little cost, so daily
  stepping of blocks is probably affordable in compute. The issue is less cost than whether a day is a meaningful unit for a
  county's output.
- **The work cost of a short year** ([[L-69 Work costs out of scale with a short year|L-69]]: chores took about 60% of actions in one run) is a warning. Every layer added in data
  has to be costed against 5 to 7 units a day and 8-day seasons, or people will have no time for the new layer's acts.

### 6.2 Space

- **The node** is a village or a valley: a place one can go and return from before nightfall, with 15 to 20 people ([[D4-2 A node is a village, a valley or a camp|D4-2]], [[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]],
  places.md). Parcels are its sites; buildings scope some sensing.
- **A region** in the peoples worlds is 9 to 23 places over 48 × 40 km to 124 × 104 km, with roads in whole days (38.69 §3). The
  wild region and the region run had four villages and a market town. The generator realises such worlds with pinned places and
  roads ([[D4-118 The land generator takes a designed world|D4-118]]). 02zzf measured about 60 s per seed and named the fixes.
- **A town** of a few hundred is a cluster of nodes joined by short edges ([[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]]). That works up to perhaps 10 to 20 nodes. A town
  of thousands needs **districts** (P13): a settlement place with wards, streets and buildings in which presence, hearing and
  dealing are scoped by building or ward, not by the whole node. Edges inside a town are minutes, not days, so the "travel is the
  day's last act" rule ([[D4-8 Arrive, then decide|D4-8]]) would need a short-move form.
- **A kingdom** of 100,000 km² at the current node density would be thousands of nodes. It needs **a hierarchy of places**:
  counties and regions as aggregate places with stocks, flows and their own roads between them, plus fully modelled nodes where
  the agents live. The capacity model already reads a region as a sum of nodes and asks what a short node could draw from a
  neighbour over the road (`capacity/space.py`). That is the start of a regional aggregate.
- **Edges by kind (P14)** are the transport revolution in the model: water that carries ten times the load (02zzi §2), tracks
  that let carts carry 300 to 400 (transport.md), canals and rail later, each with an owner and a toll. The region run's lesson
  (38.26) is that the extent of the market in the engine is set by carry and road days, as Smith would expect.
- **The world's edge:** a world needs an outside: places beyond the map that buy and sell at fixed or slowly moving terms. An
  "outside" node with a schedule of offers is the cheapest version, and it stays inside [[D4-35 Everything happens in a place|D4-35]] because the goods still arrive by
  a carrier.

## 7. Feasibility as distance from the engine

| Layer | What is there | What it needs (§3) | Distance | Representation |
|---|---|---|---|---|
| **4.1 foragers** | gathering, hunting with skill and parties (W), fishing, camps, gifts | a travelling household camp; bows and spears (P) | **here now** | R0 |
| **4.2 lasting villages** | everything in §2; the capacity ladder | the stage-1 web (P); commons customs; longer runs; 38.70's world fixes | **here now** | R0 |
| **4.3 lordship** | claims, shared capital, every-n legs, work legs, guarding | P1, P2, P7, P4 (light), P8 (multure), P5 (a roll) | **modest** | R0 or R2 |
| **4.4 market town** | seeded market custom, the merchant household, open offers, morning meetings, handcarts | P6, P14 (ox carts, boats), P7 (tolls), P13 for a town above a cluster | **modest to major** | R1 or R2 |
| **4.5 merchants** | consignment and carrier presets (S), credit by a day | P1 (partnerships), P3, P4 (courts), P5, P14 (sea), P15 (letters), P17 (bills) | **major, on the kernel** | R2 or R3, distant regions as fixed suppliers |
| **4.6 proto-industry** | piece-rate preset (S), `for` on make | P2 (piece rates), goods put out into another's house, the cloth chain, P9 | **major** | R3 |
| **4.7 states** | households only | P1 at levels, P3, P4, P7, P8, P13 (jurisdictions), P15 (post), P17 (mint, borrowing); P10 for the taxed population | **major, the first beyond all agents** | R3 or R4 |
| **4.8 industrial edge** | heat values, the water wheel, logistic renewal (the organic ceiling) | P16 (coal, engines as a fitting class), P2 (labour market), P1 (firms), P10, P11, P14 (canals, rail) | **far** | R4 |
| **4.9 mature industrial** | | P12, P13 (cities), P15 (telegraph, press), P17 in full, P18 | **far** | R4 or R5 |
| **4.10 modern urban** | services as acts `for` a party; information carried by people | all of P1 to P18; infrastructure networks; technology as licensable capabilities; online markets as places | **far, near the edge of what the engine is for** | R5 |
| **branch: nomads** | herds, driving, leading | herds at scale, a household that moves | **modest** | R0 to R2 |
| **branch: irrigation** | the river and the wheel | P8 at scale, water rights by rule, water flow between parcels | **major** | R3 or R4 |
| **branch: maritime** | fish, salt | P14 (sea), P3, P17, P13 | **major** | R3 |
| **branch: frontier** | vacant places ([[D4-118 The land generator takes a designed world|D4-118]]), settling | none essential | **here to modest** | R0 |

**Reading the table.** The step from "modest" to "major" is about social primitives, and most of them are designed (agreements.md,
holding.md, letters_and_documents.md, membership.md) or were built in Cybertron 1. The step from "major" to "far" is about
representation: whether the engine gains a second layer of aggregate people, production and markets. Nothing in the table is
outside the engine's principles. The modern economy strains [[D4-35 Everything happens in a place|D4-35]] only if a network or a market is treated as being everywhere at
once. Treated as a place reached by an edge, it fits.

## 8. Research questions and benchmarks each layer makes possible

| Layer | Questions | A benchmark or experiment |
|---|---|---|
| **4.1 foragers** | Do agents share by norm or by deal? Does a band split when the land runs short? | A forager world against a farming world on the same land: who survives a bad year, and what customs form |
| **4.2 villages** | When does a village specialise (02zzi §7)? Does a commons find its rules? What does a famine do to depth? | The descendants benchmark ([[L-104 MAJOR the descendants benchmark|L-104]]) and the peoples benchmark ([[D4-115 The peoples benchmark's worlds|D4-115]] to [[D4-118 The land generator takes a designed world|D4-118]]), with economy_web.md's depth measures (longest chain used, specialists, trades of intermediates) against a null arm |
| **4.3 lordship** | Does a lord emerge from holding the mill? Does redistribution or exchange win? Do tenants pay dues the engine does not enforce? | Two arms of the same manor, dues paid by the engine against dues paid by the tenant's act ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]); the lord's model varied (Opus at the pole) |
| **4.4 market town** | Do agents converge on a place and a day? Do prices converge across villages, and how fast does news of a price travel? | Seeded market against no market; carts on tracks against none; price dispersion across villages over time, read from the journal |
| **4.5 merchants** | Does credit form without the engine enforcing it? Does third-party reputation form when defaults are visible? | 38.68's two tests: defaults perceived by witnesses against not; goods credit left to choice against automatic settlement |
| **4.6 proto-industry** | Does an agent organise others' labour when the means exist? Do rule-run households answer piece rates the way history did? | A putter-out agent with material and coin among rule-run households; the share of household time on the loom against the piece rate and the bread price |
| **4.7 states** | How much can a ruler take before producers flee or revolt? Do officials skim? Does a state build public goods? | The fiscal capacity game: a ruler agent, officials as agents, counties as blocks; revenue, investment and unrest over generations |
| **4.8 industrial** | Does an agent with cheap fuel and dear labour invest in machines (Allen's argument)? Who captures the gains? | The same region with and without a coal seam, wages set by a labour market; adoption of power by agent firm-owners |
| **4.9 mature industrial** | Do bank runs and credit cycles appear from agent decisions? Do unions form? | Bankers as agents over deposit-holding blocks; a shock to one region; whether a lender of last resort is invented |
| **4.10 modern** | How do agents govern information monopolies, platforms and networks? Does regulation keep up with capability? | A platform as a market place agents can own and set rules for; regulators as agents; the welfare of the block population as the read-out |
| **across layers** | Do models differ in what kind of economy they build? Does a stronger model at a pole raise the whole society or capture it? | Model rotation through the poles of leverage on one world (scenario_design.md: Opus at every pole, Sonnet in the middle, Haiku in the bulk), read against a bot-run null |

A shared measurement asset for all of these is already built: the journal records every transfer and act at a place
(spec/record/), so prices, output, trade between places, the distribution of holdings and the flow of credit can be computed after
a run. What is missing is the read-out code, flagged in [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]].

## 9. The highest-value additions, in order

1. **Make agreements social, not automatic** ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]], P4 light, P5): goods credit paid by the debtor's act; agreements and
   defaults perceived by witnesses; a written tally or bond as a document. It is small and designed, it is the gate to every layer
   past the village, and 38.68 already shows what it would test.
2. **Parties beyond the household** (P1): institutions of any kind, with offices, a seat, a container and claims, able to be a
   party to agreements and to act through `for`. The state shape exists in `world.py`; Cybertron 1's `institutions.py` is the
   porting source.
3. **The decided presets made real** (P2, P3, P7): notice, remedies, `per` legs (multure, piece rates), ledgers at a seat
   ([[D2-33 Ledgers|D2-33]]), and legs created by an institution's rule (dues, tolls, taxes). With 1 and 2 this gives lordship, guilds and an early
   town.
4. **Standing orders for adults, and calling agents less than every day** (P9 and P18, R1 and R2): the cheapest way to raise
   population several-fold, built on what children already have.
5. **Edges by kind and the market as a place** (P14, P6): ox carts on tracks, boats on rivers, posted offers kept by a
   stall-holder, and prices remembered with place and date ([[D2-29 Prices are only what agents witnessed or were told|D2-29]]). The region run shows carry is the binding limit on trade.
6. **Rule-run households as full entities** (P9 beyond bots, R3): households whose daily acts come from a policy grounded in the
   engine's physics, answering to wages, rents and prices. It is the step that opens proto-industry and the state.
7. **Populations as numbers by place, on the ecology's pattern** (P10, P11, R4): blocks of people stepped by rules, producing by
   the capacity model's functions, coupled to agents through markets and institutions. It is the step that opens the industrial
   and modern layers.
8. **A hierarchy of places** (P13): districts inside a town, and regions as aggregate places, so a town of thousands and a
   kingdom have somewhere to be.
9. **History runs that start a world at a later layer** (P18): the generator and the ecology already simulate a past. Extending
   that to institutions, capital and debts lets a run begin with a manor or a market town in place.
10. **Technology as capabilities and discovery** (P16, [[L-103 Crafting and discovering new things|L-103]]): new energy as a seam and a fitting class, and new methods found,
    not only given. It matters most late, but it is cheap in data and changes what kind of growth a run can show.

## Sources

- Engine (`main` at bdfad76): `cybertron2/engine/data.py` (ITEMS, TECHNIQUES, FITTINGS, ROOMS, BLUEPRINTS, ROADS, LIFE),
  `agreements.py`, `world.py`, `verbs.py`, `run.py`, `prompt.py`, `knowledge.py`, `labour.py`, `life.py`, `evening.py`,
  `roads.py`, `buildings.py`, `renewal.py`; `cybertron2/capacity/`; `cybertron2/specs/region.yaml`.
- Engine (`peoples-worlds` at 2020b9e): `cybertron2/engine/wild.py`, `parties.py`, `cybertron2/wild/ecology.py`.
- Cybertron 1: `/home/user/cybertron/cybertron/` (`institutions.py`, `courts.py`, `credit.py`, `accounts.py`, `lawlang.py`,
  `jurisdictions.py`, `documents.py`, `registers.py`, `incorporation.py`).
- Spec: economy/ (agreements.md, money_and_markets.md, transport.md), world/ (places.md, holding.md), agents/ (work.md,
  standing_orders.md, models.md), environment/calendar.md, institutions/membership.md, information/letters_and_documents.md.
- Decisions: [[D2-1 Coin is carried; debts move only as information|D2-1]], [[D2-2 One merchant household with a cart is seeded in the first region|D2-2]], [[D2-29 Prices are only what agents witnessed or were told|D2-29]], [[D2-30 Markets are seeded custom|D2-30]], [[D2-32 The settlement rule|D2-32]], [[D2-33 Ledgers|D2-33]], [[D2-37 Acting for others|D2-37]], [[D2-135 Carrying capacities (OPEN C-1)|D2-135]], [[D2-148 A child's menial work is set by the household head's standing order|D2-148]], [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], [[D4-2 A node is a village, a valley or a camp|D4-2]], [[D4-11 Node scale if you could go there and be back before nightfall, it is…|D4-11]], [[D4-13 A round is a day|D4-13]], [[D4-16 Routine work runs on standing orders the agent sets|D4-16]], [[D4-20 One agent, one model, for life|D4-20]], [[D4-24 The world grows by data, and agents explore and learn it|D4-24]],
  [[D4-35 Everything happens in a place|D4-35]], [[D4-61 An agent rewrites its one memory each stretch, within a length that…|D4-61]], [[D4-77 The evening's add-ons|D4-77]], [[D4-102 Carrying capacity is measured, by level, from the engine's own rules|D4-102]], [[D4-115 The peoples benchmark's worlds|D4-115]] to [[D4-118 The land generator takes a designed world|D4-118]].
- Notes: 02zzg, 02zzh, 02zzi, proposals/economy_web.md, proposals/peoples_benchmark.md, proposals/descendants_benchmark.md;
  38.11, 38.21, 38.26, 38.40, 38.42, 38.65, 38.68, 38.69, 38.70; 02zzf; OPEN [[L-69 Work costs out of scale with a short year|L-69]], [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]], [[L-103 Crafting and discovering new things|L-103]], [[L-104 MAJOR the descendants benchmark|L-104]], [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]].

*Current as of 15 Nov 2026.*
