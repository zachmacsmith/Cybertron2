# Proposal: water and wetland life, fishing, preservation, and boats

**Status:** discussion (4-5 Nov conversation with Zach; written up 7 Nov). Nothing decided, nothing to build. **Owner:** 37.2 (design,
numbers); 37.4 would build the engine parts. **Affects:** spec/economy/production.md, goods.md, buildings.md, transport.md,
livestock.md; spec/environment/resources.md; data.py (TECHNIQUES, ITEMS, DECAY, fittings); landgen (stocks on water, fen, coast);
landgen/economy.py and capacity.py (count fish); OPEN L-13, L-23, L-37, L-38, L-53.

## Summary

Water is where food, trade goods and chokepoints sit in a temperate world, and boats are the cheapest answer to the carrying burden
that killed every food-dependent village so far (02zl). Almost none of it exists.

This proposal adds, in order:
1. **Water ecosystems** with their own life.
2. **Fishing**, by a ladder of gear, up to **fixed works** (traps, the weir) that someone holds.
3. **Wetland goods:** salt (which has no source today, so cheese cannot be made), reeds and peat.
4. **The coast** as a place of its own.
5. **A preservation ladder:** smaller hearth batches, the **smokehouse** as a batch process over days, salting, rack-drying.
6. **Boats**, in two stages: small boats for fishing and crossings, then water transport for trade.

The cautions come with it: fishing is another food source that can dissolve scarcity, and it is worth building only where it makes
leverage.

**With 37.4's engine_overhaul.md (7 Nov):** that proposal is the machinery (a process model in which each benched system is
mostly data) and makes fishing, with salt and a fish run, its acceptance test (stage 1b). This proposal is the content for it: what
lives in which water, the gear and the fixed works, the wetland goods, the coast, preservation and boats. Its question 2 ("line and
weir now; nets with fibre, and boats, later?") matches §10's order here.

## 1. What exists now (surveyed 4 Nov)

| | Engine | Generator |
|---|---|---|
| Rivers, lakes | a `water` cover with no resources; used by a mill's wheel, fords, beasts drinking | water parcels beside villages on rivers |
| Fen, saltmarsh, moor, heath | covers with only foraging and grazing (D2-185 left their crafts for later; D2-189 grazing) | placed by the landscape systems (D2-191) |
| Fish, eels, wildfowl | nothing | planned in stage 1 ("fish in rivers and lakes, by flow"), not built |
| Salt | an item, needed by cheese (0.2), with no source in any world | saltmarsh exists; nothing yields salt (02zo A1) |
| Reeds, peat | nothing | in stage 1's resource table, not built |
| Hunting | one `game` stock per wood, a chance roll, x3 with a weapon | game by wood type and depth (D2-191) |
| Gear | crude tool, copper tool, crude weapon | |
| Preservation | `dry meat` at a hearth or fire ring: 2 meat to 1 dried meat, 1 unit, done at once; cheese (needs salt); grain keeps longest in a granary | |
| Boats | deferred (economy_later.md: nets need flax fibre; boats need timber, pitch, a boatwright; L-13) | flow and fords recorded; navigability flagged (L-38) |

## 2. Evidence from the runs

**Spoilage** (38 published runs, review 02zl data; 4 Nov):
- 948 meals' worth of food rotted against 8,630 eaten, about 10%.
- By food: grain 30% (big stores, slow), fresh meat 21% (0.3 a day), wild food 12%, bread 10%, milk 10%, dried meat 8%.
- The worst runs lost a quarter: p1_combe_evening (25%, mostly a carcass), b1_wild (25%), m2_V (22%).

**Drying meat** (19 runs' turn logs, 4 Nov):

| Run | Meat got | Dried | Rotted | Note |
|---|---|---|---|---|
| p1_combe_evening | about 250 (over-counted) | 32 | 33 | a slaughter's carcass |
| w2_two_valleys | 111 | 42 | 7 | the best |
| b1_wild | 79 | 20 | 18 | at camp fires |
| m2_V | 58 | 0 | 20 | no hearth anywhere |
| v3 | 46 | 0 | 10 | five hearths; nobody thought of it |

What it shows:
- **When meat comes, most is eaten fresh or rots.** A quarter to a third was dried.
- **Most refusals were a gate since fixed.** "It needs 2 meat; you have 1.7 to hand": making now draws on the stores at home (D4-96).
- **Some worlds had nowhere to dry, and some agents never thought of it.** So visibility matters as much as a new building: a
  meat line saying "it will rot in about 3 days".

## 3. Water ecosystems

Each water body gets its own life, as woods now differ by type (D2-191), with depth carrying over: the middle of a mere or the open
sea needs a boat.

| Water | Life | Seasonal | Who gets at it |
|---|---|---|---|
| brook | trout, small fish | | anyone, by hand or rod |
| large river | eels; salmon runs in autumn (a periodic resource, resources.md) | the run | rod, traps, the weir |
| mere, lake | pike, eels; wildfowl at the edge | | the edge by rod; the middle by boat |
| fen, reedbed | eels, wildfowl, reeds | fowl in winter | traps, fowling, reed-cutting |
| estuary, coast | shellfish on the foreshore, sea fish, salt | | the foreshore at low water; the sea by boat |
| saltmarsh | salt, samphire, grazing | | salt pans, foraging, herds |

**From the generator:**
- stocks on water parcels by the river's size (flow is recorded already);
- meres and wetlands from the varied-landscapes plan (shallow hollows as marsh, a few deep ones as meres);
- ponds as parcel features (a field pond, a mill pond).

Wildfowl and fish are guilds in ecosystems.md §7's sense (L-37).

## 4. Fishing: a ladder of gear

| Method | Where | Needs | Yield (first values; calibrate) | What it does to a society |
|---|---|---|---|---|
| By hand: shellfish, tickling trout | foreshore, brooks | nothing | low, like foraging | a meagre floor |
| Rod and line; a fish spear | rivers, meres' edges | a rod (wood), a line (hair or gut), the knowledge | about 1 to 2 fish a unit | one person's steady catch |
| Traps (wicker eel traps) | rivers, fen | withies, a unit to set; checked next day | 2 to 4 eels a trap a night | set and checked: theft, watching, claims on stretches of water |
| **A weir** | across a river | timber, stone, many hands, upkeep | many a day in a run | **fixed capital and a chokepoint**, held as medieval lords held fisheries. It competes with mills and boats for the same river. |
| Fowling: nets, decoys | fen, saltmarsh | nets (fibre) | seasonal | wetland game |
| Nets, a seine | lakes, coast | flax or hemp fibre; often a boat | high | opens the flax chain (L-13) |

**The leverage is in the fixed works**, not in a uniform "fish 1 a unit":
- the weir, and who may set traps on which stretch;
- the salt pan and the harbour (§5, §6);
- the ferry (§8).

## 5. Wetland goods

- **Salt:**
  - from saltmarsh pans, sun-dried in summer or boiled with fuel, or at a salt spring inland (D2-56 decided this; not built);
  - **it is needed now:** cheese needs it and no world has it (02zo A1);
  - it keeps fish and meat;
  - the classic long-distance trade good, which ties the coast to inland villages.
- **Reeds:** cut in the fen, for thatch, a building material.
- **Peat:** cut on wet moor and fen, dried, burnt where wood is short. It makes fuel locality (02zl §1.5) a design choice, not a death.

Each is a gather technique on its cover, with a stock that regrows slowly (peat hardly at all).

## 6. The coast

- **The tide:** the foreshore is gathered at low water. In a world of whole days, it is "a tide's gathering a day" on foreshore
  parcels; no clock is needed.
- **Sea fishing only by boat,** at risk in a gale (the weather exists, D2-69).
- **Salt pans** on the saltmarsh.
- **A harbour** as a chokepoint: where boats can land in a storm.
- Coastal communities differ by their coast:
  - saltmarsh and estuary give salt and wildfowl;
  - a rocky shore gives shellfish and sea fish;
  - dunes give little but rabbits and marram.

## 7. Preservation: a ladder, and the smokehouse

| Way | Where | Costs | Keeps | What it creates |
|---|---|---|---|---|
| **Hearth drying** | any hearth or fire ring | today 2 meat a unit, instant. **Make it a small batch** (a few units at a time), so the shed is worth having | fair | the household floor |
| **Smoking** | **a smokehouse** (a shed, or a fitting on a building) | a batch takes days (about 3 or 4) of slow fire, fuel every day, the fire tended | well, weeks to months | village capital with a capacity; a shared fire to tend; fuel demand; fire risk (L-48) |
| Salting | anywhere with salt | salt, a little work | best | demand for salt; the coast gains something everyone wants |
| Rack-drying (stockfish) | cold, windy coasts | weather, time | very long | a coastal speciality, lost in damp spells |

**Why the smokehouse earns its place:**
- **Time and capacity make it real capital.** A batch loaded on day 3 is ready on day 6. Meanwhile the space is taken, the fire must
  be kept and fed, and the goods can be watched or stolen: a shared asset to control, like the mill.
- **It links chains:** catch, then smoking, then trade. Fuel matters more, peat becomes worth cutting, and smoking competes with
  salting.
- **It meets gluts in time:** salmon runs and the slaughter come at a season, so the bottleneck is how much can be preserved before
  it rots.

**What it needs in the engine:**
- a **batch process over days**: load, wait, take out. It is the first of its kind; it is like a crop growing or a building in
  progress.
- the smokehouse as a building or fitting with a capacity and a fuel draw;
- **smoked fish and smoked meat** as goods: about half their fresh weight, spoiling at about 0.02 to 0.03 a day;
- **fresh fish:** food about 1.0 a unit, spoiling fast (about 0.4 a day);
- **salted fish and meat:** spoiling about 0.01 a day.

**Visibility, from the evidence:** a perishable good's line says when it will rot ("the meat will rot in about 3 days"), and the
store says what is going off. Without it, a smokehouse will not help the v3 kind of failure, where nobody thought of preserving at
all.

## 8. Boats, in two stages

**Stage A, small boats:**
- a punt or a coracle (hide on a frame) and a fishing boat: timber, hides or pitch, a boatwright's craft;
- they open the meres' middles, the coast and **ferry crossings**;
- a ferry at a large river is another held chokepoint, beside the ford and, later, the bridge (L-5, L-34).

**Stage B, water transport:**
- river edges between villages on the same river: fast downstream, slow or towed upstream;
- landings at villages; coastal runs between harbours;
- **a boat carries hundreds of units against a person's 10:** the direct answer to the carrying burden (02zl, L-52) and to trade at
  scale.

Stage B merges with L-38 (travel by water) and L-53 (transport and traders). Which comes first depends on the dependence ladder's
answer (L-50): carriage, or coordination.

## 9. Cautions

- **Fishing is another food tap, and it can dissolve scarcity.** Food should bind without dominating (at most 30% of actions,
  scenario_design §4). Catches must be calibrated, and **the economy and capacity checks must count fish**, or they will misjudge
  every river village.
- **It is only interesting where it makes leverage:** the weir, the ferry, the salt pan, the harbour, the smokehouse. A uniform
  stock on every river would just be more foraging.
- **Most of it is engine work (37.4's).** 37.2's part is the design, the numbers, and where each water body and its catch sit on the
  map.
- **Nets and boats pull in fibre (flax, hemp) and pitch.** These are material chains (good), but each is a build.

## 10. Order proposed

1. Salt-making at saltmarsh: data only, unblocks cheese (02zo A1).
2. The visibility of rot.
3. Water ecosystems and the gear ladder (hand, rod, traps), counted by the economy checks.
4. The weir as fixed works; reeds and peat.
5. The preservation ladder: hearth batches smaller, the smokehouse, salting.
6. The coast.
7. Small boats and ferries.
8. Water transport, with L-53, after the ladder.

## Open questions (for Zach)

1. The scope: all of §3 to §8, or stop after preservation (§7) until the ladder has run?
2. Salt now (data only), ahead of the rest?
3. Hearth drying made a small batch, so the smokehouse matters?
4. The weir: who may build one and who holds it. As held works (claims), or by custom?
5. Boats: stage A with the water goods, or both stages together with transport (L-53)?

## History

- 4 Nov: Zach: "Should we build out fishing, more water ecosystems in rivers, marshes etc, ways to hunt them with sticks, rods etc.
  the coast would be different ... boats, both for fishing and water transport, that could scale to facilitate trading". 37.2
  surveyed what exists (§1) and proposed the shape in conversation.
- 4 Nov: Zach: "What about also adding smoking sheds that takes a while but is another way to try and preserve food?" Added the
  preservation ladder (§7).
- 4 Nov: spoilage measured across the runs, and meat drying from 19 runs' turn logs (§2).
- 7 Nov: written up (37.2). Zach: "Did you write up all of our discussion about water ecosystems in a new proposal?" It had not
  been. This is it.

## Sources

- The conversation of 4 Nov.
- review 37_growth/02zl (economics), 02zo (open decisions);
- proposals/engine_overhaul.md (37.4: the process model; fishing as the acceptance test);
- proposals/economy_later.md (nets, boats), ecosystems.md (§3, §7), generator_stage1.md (the resource table), temperate_landscapes.md;
- spec/environment/resources.md (periodic resources);
- OPEN L-13, L-23, L-37, L-38, L-50, L-52, L-53.
