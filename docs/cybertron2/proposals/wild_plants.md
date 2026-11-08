# Proposal: wild plants, and the slow ecosystems they make

**Status:** discussion (8 Nov). Nothing decided, nothing to build. **Owner:** 37.2, with 37.4 (the engine). **Affects:** data
(RESOURCES, ITEMS, TECHNIQUES as a `wild plants` pack, D4-104); landgen/ecology.py (where each grows); spec/environment/resources.md;
proposals/wildlife.md §11, living_populations.md, temperate_landscapes.md; husbandry.md (what people make of them).

## Summary

Zach, 8 Nov: "would more types of wild plants make sense? Varying based on environments? Should we have any plant ecosystems as well
or no? Obviously these change at much slower scales, but they can also be quite complex? I don't think it should go too far ... but
maybe there is some relevant / helpful level of variability?"

Yes, at two levels, and no further:
1. **Wild plant kinds** as stocks on parcels: about 20, grouped by what they give (food, materials, medicine), each growing where its
   ecosystem is, with its own season and its own year-to-year swing. They replace the one generic "plants" stock.
2. **Slow plant ecosystems as succession:** each patch of land sits on a ladder (bare, grassland, scrub, young wood, old wood, and
   the wet and heath variants), climbs it when left alone, and is held back or pushed down by use: grazing, cutting, burning,
   clearing. Management is what keeps a meadow a meadow, a heath a heath, a coppice a coppice.

No competition between species and no seeds spreading: the variability that helps is seasonal, yearly and patchy, and it is all
data on existing mechanisms (renewal rules, periodic stocks, outcome distributions, land changing kind).

## 1. What exists now

- **Forage:** one `plants` stock (renewal: fast) on forest, meadow, pasture, scrub and the D2-185 covers. It is the same wherever it
  grows, in every season.
- **Trees, young growth, dead wood:** three stocks with their own renewal; five wood types and depth bands from the landscape
  (D2-191). Under 40% of its trees a wood turns to scrub.
- **Grass** on pasture, meadow and rough grazing (D2-189).
- **Land changing kind:** forest to scrub, clearing to field (D4-60). That is all of succession today.
- **Wattle** is built from timber (data: 8 timber a small room). Real wattle is woven hazel or willow rods, which are young growth.

## 2. The wild plant kinds

Each is a stock on the parcels whose ecosystem it grows in, with its own season (D4-103's clocks), its own swing between years, and
a patchiness drawn at generation (one hazel copse rich, the next poor). Densities and yields are first values to calibrate.

### Food

| Kind | Grows in | Season | Gives | Note |
|---|---|---|---|---|
| **Wild greens:** nettle, sorrel, wild garlic | wood edges, hedges, damp ground | **spring** | greens (fresh, spoil fast) | **the hungry gap:** food in spring, when the stores run low and nothing is ripe |
| **Hazel nuts** | wood edges, coppice, hedges | **autumn** | nuts (**keep for months**) | dense food that stores: a reason to gather in autumn |
| **Acorns, beech mast** | oak and beech woods | autumn, **in mast years** | mast | pigs' and boar's food (pannage); people's famine food only after leaching (a knack) |
| **Berries:** bramble, bilberry, wild strawberry | scrub, wood edges, heath and moor (bilberry) | summer | berries (spoil fast) | a summer pulse |
| **Hedge fruit:** crab apples, sloes, haws, rose hips | hedges, scrub, wood edges | autumn | fruit (some keep, some only cooked) | crab apples and sloes keep into winter |
| **Mushrooms and fungi** | woods, pasture | autumn, after rain | fungi (spoil fast) | **some are poisonous:** knowledge is safety (§4) |
| **Roots:** pignut, silverweed | grassland, damp ground | spring to autumn | roots | famine food: hard work for little |
| **Watercress, brooklime** | brooks, springs | spring and summer | greens | |
| **Samphire, seaweed** | saltmarsh, shore | summer (samphire); all year | greens; seaweed also feeds sheep and the fields (manure) | the coast's plants |

### Materials

| Kind | Grows in | Season | Gives | Used for (husbandry.md) |
|---|---|---|---|---|
| **Withies:** hazel and willow rods | coppice, river and fen edges | winter cutting | withies | wattle (instead of timber), hurdles, baskets, eel traps, fish weirs |
| **Reeds, sedge** | fen, reedbed | winter | reeds | thatch (water_and_preservation §5) |
| **Rushes** | wet grassland, fen edges | summer | rushes | rushlights (with fat), floor strewing, mats |
| **Heather** | heath, moor | all year | heather | thatch, brooms, bedding |
| **Bracken** | heath, wood edges | autumn | bracken | bedding, and potash when burnt |
| **Gorse** | heath, scrub | all year | gorse | **oven fuel** (burns hot and fast); crushed for fodder |
| **Bark:** oak bark; lime bast | oak woods (with felling); lime | spring, when the bark peels | bark | **tanning** hides into leather (oak bark); rope (lime bast) |
| **Oak galls** | oak woods | autumn | galls | ink |
| **Birch bark** | birch woods | spring | bark | tar (glue, waterproofing), containers |
| **Dye plants:** woad, madder, weld | grassland, waste ground | summer | dye stuff | cloth (with clothing, L-14) |

### Medicine and poison

| Kind | Grows in | Gives | Note |
|---|---|---|---|
| **Healing herbs:** yarrow, comfrey, willow bark, feverfew | grassland, wood edges, river banks | herbs | the healer's materials, when disease exists (Q-16) |
| **Poisonous plants:** hemlock, foxglove, deadly nightshade, yew | damp ground, woods, churchyards (yew) | (not gathered as food) | **knowledge as safety:** mistaken for food by someone who does not know; yew poisons cattle that graze it |

### Timbers (the wood types, D2-191, given uses)

The five wood types already exist. What would differ is the timber each gives:

| Timber | Use |
|---|---|
| oak | building (the best) |
| ash | tool handles, spear shafts |
| hazel and willow | withies, as coppice |
| beech | firewood and charcoal; poor outdoors |
| alder | posts in water |
| yew (in some woods) | bows (later); poisons beasts |

That is a `kind` on the wood's trees, which the generator already knows; it becomes a property of the timber taken.

## 3. Slow plant ecosystems: succession, held back by use

**Every patch sits on a ladder, and climbs it when left alone:**

| Land | Left alone becomes (on the year clock) | Held where it is by | Pushed down by |
|---|---|---|---|
| bare or cleared ground | grassland, in a season or two | | |
| grassland, meadow | scrub (bramble, thorn, gorse) in a few years | grazing, mowing for hay | |
| heath | birch scrub, then wood | **grazing and burning** (lowland heath exists only because of them) | |
| scrub | young wood (birch, hazel) | grazing | clearing, burning |
| young wood | old wood | coppicing (a cycle of about 7 to 15 years) | felling |
| old wood | | | felling, to scrub (built: under 40% of trees) |
| fen, reedbed | carr (alder, willow), then wet wood | **cutting reeds and sedge** | draining (to grassland) |

**Why it is the right level:**
- **Long runs see consequences:**
  - an abandoned field goes to scrub;
  - an ungrazed common turns to wood;
  - a heath unburnt turns to birch;
  - a cut-over wood comes back.
- **Management becomes real work with a reason:** mowing, grazing, coppicing, burning and reed-cutting keep the land useful.
- **It is mostly built:**
  - "land changing kind" is D4-103 mechanism 5;
  - the wood-to-scrub rule exists;
  - the generator's state layer (temperate_landscapes.md §3c) already places these states by use.

  Succession adds the clock and the climb.
- **On the field (living_populations.md):** succession changes each patch's ecosystem, which changes every wild kind's habitat score.
  So the animals follow the plants without any rule of their own.

**What it leaves out:** competition between plant species, seeds spreading, and soil building over centuries. None ends in
leverage within the runs we can afford.

## 4. The variability that helps

- **By season** (the clocks): greens in spring, berries in summer, nuts, mast, fungi and hedge fruit in autumn, withies and reeds
  cut in winter. The year gets a shape, and the hungry gap in spring becomes real.
- **By year:**
  - mast years and bad ones (D2-76's ecology era);
  - a berry year, a nut year: a draw per kind per year (37.4's stage for variance and risk);
  - storing in a good year pays.
- **By patch:** one copse rich in hazel, another poor, drawn at generation. **Knowing where the good patches are is lore:** it lives
  in people's memories of places and can be told or kept.
- **By knowledge:** a poisonous mushroom looks like a good one. Gathering fungi by someone untaught carries a chance of harm (an
  outcome in the act's distribution, D4-103 part 2), so knowledge has a value you can see.

## 5. What it costs

- **About 20 kinds, as rows:** stocks with a season and a renewal rule; goods; gathering techniques. They are on existing mechanisms
  (D4-103, D4-104): periodic stocks for seasons, outcome distributions for poison, packs to switch them on.
- **Succession:** a transition table per ecosystem, on the year clock, with "held by" and "pushed by" acts (D4-103 mechanism 5).
  Small.
- **The generator:** each kind's habitat in ecology.py's palette, and the patchiness draw. Small.

## Steps

1. **Wild food kinds with seasons and knowledge** (greens, hazel nuts, berries, hedge fruit, fungi). They replace the generic
   `plants` stock in worlds with the pack on; the rest keep it.
2. **Withies, reeds, heather, gorse and bark,** with the husbandry that uses them (husbandry.md: wattle from withies, thatch, tanning).
3. **Succession** on the year clock, with management holding it.
4. **Herbs and dyes,** when disease and clothing exist.

## Open questions (for Zach)

1. Replace the one `plants` stock with these kinds (step 1), in worlds that switch the pack on?
2. Poisonous plants: may an untaught gatherer be harmed (knowledge as safety)?
3. Succession: in, on the year clock, with management holding it back?
4. Wattle from withies instead of timber (a change to a built recipe)?

## History

- 8 Nov: Zach asked about more wild plants by environment, plant ecosystems at slower scales, and "some relevant / helpful level of
  variability". 37.2 proposed the kinds, succession held back by use, and four kinds of variability.

## Sources

- engine data (RESOURCES, FORESTS, ROOMS: wattle from timber), proposals/process_model.md (D4-103, mechanisms 5 and 7);
- temperate_landscapes.md (D2-191: wood types, the state layer), living_populations.md, wildlife.md §11, water_and_preservation.md;
- D2-76 (mast eras), D2-185 (the new covers), D4-60 (clearing).
