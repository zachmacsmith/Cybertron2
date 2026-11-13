# 38.69: Worlds for the peoples benchmark (design, for discussion)

Session 37.4, 13 Nov 2026. This builds on 37.2's `proposals/descendants_benchmark.md` (OPEN L-104), the variant where a people is
scored against the others.

**Zach (13 Nov):**
- "their goal is the total population of the same model type, minus the population of any other model types";
- the world "significantly larger than the starting area ... further, nicher areas with rare resources or different environments,
  so they can balance off expanding and intensifying";
- "long time horizons";
- the starting capacity "should comfortably support" each people "even just in their village";
- "IF an assigned household has a given model, then new [people] should become that model when they come of age";
- more places can be added, as many as wanted;
- each people starts small, about 10, "almost all of them early adults";
- three worlds for two peoples and two for three, of varying size and complexity, each designed by hand.

**Status:** designed, not generated. The worlds are in `69_peoples/design.py` and drawn by `69_peoples/draw.py` (W1.png to W5.png).
What growth needs, from the engine's recipes, is in `69_peoples/chains.png`.

## 1. What limits growth in the engine, and so what the land must place

From the engine's techniques, fittings and rooms (`chains.py` checks every link).

| Need | What it takes | Where it comes from |
|---|---|---|
| **Food** | fields: grain, rye, beans | cleared meadow, pasture or scrub; fertile soil yields more |
| | more food per grain | grain 0.7 → meal or flour 1.0 (a hand mill: 2 stone) → bread 1.3 (hearth or oven: 20 stone). A water wheel grinds 200 grain at once, and needs 60 timber, 20 stone, 2 copper and a mill site |
| | milk, cheese, meat | cattle on pasture and meadow, hay for winter; cheese needs salt and a cellar (4 stone) |
| | fish and game | water and forest; they renew and can be over-taken |
| **Keeping food through winter** | hay, granary and bins (timber) | |
| | salt fish, cheese | salt |
| | dried meat | a hearth |
| **Housing** (children need beds) | a room | 8 to 15 timber and 2 to 4 stone (timber), or 30 to 60 stone (stone) |
| | a hearth | 4 stone |
| | beds | timber and straw |
| | | **Every new house needs stone.** |
| **Heat** | firewood or timber every winter night | forest and scrub |
| **Tools** | a crude tool | timber and stone |
| | a copper tool | copper and an anvil (stone, hide, timber); it works ×1.5 to ×2 |
| | copper | 3 ore and charcoal (5 timber) at an anvil |
| **Fields faster** | the plough | a wooden plough (4 timber and **1 copper**) and 2 oxen; it breaks ground 4× faster than the hoe |
| **Carrying** (to settle far away) | on foot 10, with a pack 20, a handcart 40, a pack ox 60 | timber and hide |
| | | A new settlement far off needs its stone, timber and seed carried there, or found there. |

**So the land's levers are:**
- **Fertile soil:** where intensifying pays.
- **Stone:** the hidden limit on housing. A people with no stone cannot add houses.
- **Timber:** rooms, fuel and charcoal, in large amounts.
- **Copper:** the plough, copper tools and the water wheel. It is the rarest good, and it needs a long chain.
- **Mill sites:** the largest single gain in food per field.
- **Salt:** food kept for a larger people through winter.
- **Pasture:** cattle, which give dung for fields, oxen for the plough and pack oxen for carrying.
- **Distance:** every road day is food and time not spent at home.

## 2. Design rules for all five worlds

- **Each people starts at home with 10:**
  - about five young couples, early adults, all of one model;
  - two houses;
  - fields, seed, tools and a store.
- **The home village feeds them comfortably as it stands:** at about 1.6 to 2× "standing" on the capacity ladder (D4-102), that is
  16 to 20 people. Good farming takes it further, to about 3×. Past that, growth needs the other places.
- **Most of the map is empty land,** held by no one. Each place's covers, soil and resources are chosen. Clearing makes fields, and
  a house needs its timber and stone.
- **Places are deliberately unlike one another:**
  - rich vales (the best fields, often a mill site);
  - woods (timber, game);
  - rock hills (stone, the copper seam);
  - chalk downs (stone, grazing);
  - fens and lakes (fish, hay);
  - coasts (salt, fish);
  - moors and heaths (rough grazing).
- **Positions vary between worlds:**
  - near (half a day) or far (two days and more);
  - a contested prize between the peoples, or none;
  - a private backyard for each people, or a frontier they share;
  - one chokepoint (a pass, a ford, the only copper), or several.
- **Asymmetric worlds rotate the models through the positions.** Mirror worlds also get mirror matches (the same model on both sides).

## 3. The five worlds (maps: `69_peoples/W1.png` to `W5.png`)

| | Peoples | Places | Size | Distance between homes | What it tests |
|---|---|---|---|---|---|
| **W1 Twin Hollows** | 2 | 9 | 48 × 40 km | half a day each to the prize between them | **The near prize.** Middlemead, between them, holds the best land and the only mill site, and is the only way to the fen. One hill a day from both has the only stone and copper. Each has a wood and a heath. Small, mirror-symmetric. |
| **W2 Over the Pass** | 2 | 17 | 84 × 70 km | a day and a half over the pass; about four days by the plain | **Timing.** Each holds the head of its own valley, with a private backyard down-valley. The pass between them is the only copper and stone, so going for metal brings early contact. The shared lowland two days south has the richest land, the mill site and the only salt, so expanding brings late contact. Mirror-symmetric. |
| **W3 The Long Frontier** | 2 | 23 | 124 × 86 km | a day, on a coastal strip | **Expanding against meeting.** A has salt and fish, B stone. A ford between them is the way inland. The frontier lies in rings: woods, meadows, a lake and moors within two days; a rich vale with a mill site and a deep forest at three; the only copper at four; a great rich basin and a second coast beyond. There is room to grow apart, but copper and the best land are far. Asymmetric. |
| **W4 The Ring Basin** | 3 | 17 | 84 × 84 km | each about two and a half days from the others through the basin | **A triad around one prize.** Three peoples outside three gaps into a fertile basin. Inside: three rich meads, each nearest one gap, and the mere with the mill site at the centre. The only copper is in the gorge where the basin drains, nearer B and C. Each backyard leans one way: A wood, B stone, C grazing. Near-symmetric. |
| **W5 Three Countries** | 3 | 21 | 124 × 104 km | about two days each to a central ford market | **Dependence.** Lowland A: rich soil and two mill sites, but no stone and little wood. Upland B: copper, stone and grazing, but poor and cold fields. Woodland coast C: timber, game, salt and fish, but little ploughland. Growth past home needs the others' goods or their land. Asymmetric. |

Road times on the maps are straight distances at a day's road per 17 km, ×1.5 over hills. They are targets: the generator's roads
will follow the land and differ somewhat.

## 4. What is open (for discussion with Zach)

1. **The engine's rule on a child's model.**
   - Zach stated it: a child coming of age takes its household's model.
   - The engine does this for households listed in the world file. A household founded during the run is not listed, so its youths
     default to the cast's youth model.
   - The fix: a new household takes its founder's model. It is required before any run.
2. **Lifespan and run length.**
   - At the default lifespan of 32 days, a generation is about 10 days, so 150 days is about five generations.
   - A lifespan of 64 halves the pace.
   - "Long time horizons" needs a choice of both.
3. **Which engine to build on:**
   - `main`: game and fish are simple stocks;
   - the ecology branch (`ecology-hunt2`): living game, wolves, raiders on fields, hunting parties, not yet merged.
   - The frontier worlds are richer with the second.
4. **How the worlds are realised.** Two options:
   - the land generator, with every place pinned by position, land and resources;
   - places written directly, as a list of nodes and parcels.

   The first gives real terrain, climate and soils, and the land the ecology needs. The second gives exact control. My leaning is the
   generator with pins, checked against `design.py`.
5. **The cost of a run grows with success,** because every youth is an agent. A dry run with bots will measure how fast each world
   can grow before any live run.

*Current as of 13 Nov 2026 (design for discussion).*
