# Withies, coppice and the other wood and wild materials for fishing and hunting gear

Session 37.2, thread W-73 (fishing, hunting and their materials developed together), 21 Nov 2026. A research and design-input note:
nothing here is decided, and no code was changed. It covers the materials the gear and its capital need from the woods, the wet
ground and the carcass: withies and osiers, coppice and poles, bark, and the benched wild materials (reeds, rushes, sedge, bracken,
heather, gorse, pitch and tar, glue, bird lime, wax, bone, antler and horn, leather as far as gear needs it). Fishing methods, hunting
and fowling, fibre and cord, and the engine audit are covered by the other notes in this folder.

Marks: **(est.)** my estimate from the figures given; **(m)** a standard figure not re-checked in this session; **(sec.)** read only in
a search summary or a secondary source. The session could not fetch conservationhandbooks.com or archive.org (both outside the
session's allowed network), so the figures from those sites and from the old willow bulletins come through search summaries.
Verify them before the numbers go into data.

Engine basis used throughout: a unit of work is 2 hours; the compressed year is 32 days (D2-209); a unit of size is about 2 ha (the
land a plot takes, 02z model); a timber is about 240 kg of wood (02z model), firewood a quarter of a timber's mass (about 60 kg);
on foot a person carries 10 weight; real values are kept within about 20% (D2-259), with every departure named.

## 0. What the engine has now

- **Goods:** `timber` (weight 2, heat 2), `firewood` (weight 1, heat 0.5), `charcoal` (5 timber), `straw`, `hide`, `tallow`, `tallow
  light` ("a rush or rag dipped in tallow"), `antler`, `horn`, `offal`, `fishing rod` (0.5 timber and 0.1 hide). No withies, poles,
  bark, bone, cord, reeds, pitch or glue (`engine/data.py` ITEMS).
- **The woods:** forest and scrub parcels hold trees, young growth and dead wood (`FORESTS`, `engine/forests.py`, D2-156). A
  `managed wood` (600 trees, 400 young growth a unit of size, regrowing 1.0 a year) is the engine's coppice: the generator makes a
  village's own wood a managed one, written "coppiced, hazel under oak standards" (`landgen/settle.py`, `landgen/write.py`). Young
  growth does not regrow while beasts graze the parcel, and a sign already says deer have stripped the young ash and the coppice
  regrowth will die back (`wild/kinds.py`). Hazel nuts are 1.5 times as thick in a managed wood (`wild/plants.py`).
- **Cutting:** the `cut` technique (aliases "coppice", "coppicing", "cut poles") takes young growth at forest and scrub and gives 5
  **firewood** a unit with a crude tool. So "cut poles" today gives firewood, never a pole.
- **The weir** (D2-209, D2-210, W-69; `WATER_WORKS`, `wild/gear.py`): a wattle section 6 timber and 16 units, a timber section 10
  and 25, and the first section adds the weir's stakes across the river and its trap, 6 timber and 8 units; so a wattle first
  section is 12 timber and 24 units. Wear by material: wattle 1.0, timber 0.5, a stone footing 0.1; a year's upkeep about half a
  wattle section's cost.
- **Set traps in water** (`wild/methods.py` SETS, `trap in water`): a wicker trap set overnight, holding 10 kg, wrecked on a spate
  at 0.5 and a flood at 0.85. **It costs nothing to make**: there is no trap good.
- **Covers** (`COVERS`): forest, scrub, fen, heath, moor, meadow, pasture, water, saltmarsh. Wet ground is read from the position,
  the ecosystem (alder carr, wet grassland, fen, reedbed and others) and the river (`plants.WET_ECOS`, `suit`).
- **Proposals:** economy_web.md §2.6 (the coppice: withies, poles, bark, brushwood), its open question 2 (the coppice as a parcel
  state with a rotation or as a wood's yield with no rotation); wildlife.md (withies and willow, rushes, bracken, heather, gorse as
  benched wild materials); river_and_water.md open question 7 and OPEN L-111 (withies and cord for the hunting and resources build,
  "a soon follow-up").

## 1. The materials

### 1.1 Withies and osiers (willow)

Withy and osier mean the same thing: a one-year willow rod. The basket willows are *Salix viminalis* (common osier), *S. triandra*
(almond willow, the Somerset staple) and *S. purpurea* (purple osier); the wild sallows (*S. cinerea*, *S. caprea*) give coarser,
branched rods. Willow grows on wet ground: river banks, ditches, fen edges, alder carr, wet meadows.

| | Wild willow (bank, fen, carr) | A withy bed (osier bed, holt) |
|---|---|---|
| **Source** | sallows and osiers along the water; pollards on the bank | cuttings planted close on wet, fertile ground near water |
| **Establishing** | none; pollarding a bank of willows gives straight rods from the second or third year after the first cut (m) | cuttings of about 25 cm pushed into dug ground: **about 17,000 to 17,500 an acre** (sec.); the first year's growth cut back and of little use; not fully productive for about **three years** (sec.) |
| **Yield** | scattered, crooked, branched; a gatherer gets perhaps a third of a bed's rate (est.) | **6 to 9 short tons green an acre a year** on average for basket willows, 12 to 15 at best (USDA Farmers' Bulletin 622, Lamb; sec.), about 13 to 20 t/ha green; modern short-rotation willow 7 to 12 oven-dry t/ha a year (Forest Research; sec.). About ten rods a stool a year (sec.) |
| **Life** | indefinite while it is cut and not grazed | **up to about 30 years** with care (sec.) |
| **Cutting** | dormant season, after leaf fall: **November to March** (sec.); summer rods are leafy, brittle and weaken the stool | the same, with a hook; tied in bundles ("bolts", measured round the band at the butt: m) |
| **Preparing** | **brown**: cut and dried with the bark on; soaked before use (days to about two weeks for long rods: a Devon maker soaks 1 to 2 weeks, sec.); used green within a few weeks, no soaking. **Buff**: boiled **9 to 10 hours** (sec.), the bark then stripped; the tannin stains the rod. **White**: stood butt-down in water pits through the winter until the sap rises in spring, then stripped through a **brake** (an iron or wooden fork), rod by rod, work done mostly by **women and children** (sec.); drum strippers from the 1920s. Peeled and dried rods weigh perhaps a third to a half of green (est.) | |
| **Labour** | cutting wild rods: about 1.5 bundles of 10 kg a unit (est.) | cutting in a bed: about 4 bundles a unit (est.); planting a 200 m² bed about 10 units with digging (est., below) |
| **Uses** | wattle, hurdles, eel traps, weir panels, rough baskets, withy ties (twisted rods as rope) | the same, and fine baskets, putchers, lobster and crab pots |
| **Competing uses** | grazing (beasts and deer eat the regrowth), fuel | land from meadow and pasture; the beasts must be kept off |

### 1.2 Wicker gear: rates and life

| Thing | Material | Hours (skilled) | Life | Sources |
|---|---|---|---|---|
| **withy pot** (a crab or lobster pot, the largest common wicker trap) | 9 ft and 4 ft willow rods; a 10 ft trough soaks enough for about 3 pots | **4 to 5 hours** for one man; another maker 4 hours | **1.5 to 2 years with constant repair** | Reading "Sense of Place" blog on Dave French (2013); Fishing News; sec. |
| **putcher** (Severn salmon trap, a willow cone in a basket-weir of hundreds) | willow, some hazel | not found; about a putcher pot's (est.) | **replaced about every two years**; the weir's elm frame lasted **up to 20 years** | Gloucestershire estuary fishing report; Museum Wales; sec. |
| **eel trap** (grig, hive, eel pot: two cones, the inner one just large enough for a good eel) | fine willow, young and green; about 2 to 3 kg dry rods (est.) | about 4 to 8 hours (est., from the pot) | about 2 years (est., from the putcher and the pot) | Denny Farmland Museum; Fergus estuary double basket trap of hazel and alder rods under 1 cm (13th c.); sec. |
| **hazel hurdle** (6 ft by 3 ft, a sheep hurdle) | about 25 to 35 rods, mostly cleft, with 7 uprights ("sails") about 30 cm apart; 10 to 15 weavers a foot of height | **2.5 to 3 hurdles a day** for a skilled maker today (about 2.7 to 3.2 hours each); a beginner half a hurdle in a day | 5 to 10 years dry (m) | Farmers Weekly; woodlands.co.uk; lowimpact.org; sec. |
| **wattle panel in place** (a weir, a fold, a wall) | whole or cleft rods woven on driven stakes; about 20 rods a m² (est., from the hurdle) | about 1 hour a m² woven, a quarter hour a stake driven from the bank or a stage (est.) | a weir's wattle mended every season it is used (D2-210's target); in a wall, years under daub | 03_crafts §4.5; river_and_water.md §3b |
| **basket** (a creel, a carrying or storage basket) | 1 to 2 kg dry rods (est.) | about 4 to 8 hours (est.) | a few years (m) | |

### 1.3 Coppice and poles

| | Hazel | Ash | Alder | Oak (bark coppice) | Wild young growth (scrub, unworked wood) |
|---|---|---|---|---|---|
| **Rotation** | **7 to 10 years**; Hayley Wood was cut on a **7-year cycle** in the Middle Ages (Rackham, via RFS; sec.); short rotations of about six years were the common medieval form (sec.) | 10 to 25 years (m) | 15 to 25 years (m) | **20 to 30 years** where kept for bark, upland Britain by 1800 (sec.) | none: what is there |
| **Stools** | 1,500 to 2,000 a ha (600 to 800 an acre) (sec.) | | | | |
| **Yield** | **about 10,000 rods an acre** of good hazel at the cut, enough for **about 300 hurdles** of 6 by 3 ft, 5,000 pea sticks, 250 bean rods, thatching wood and stakes (Durham 1956, via Forest Research; sec.); 25,000 to 30,000 rods a ha at 8 to 9 years; about 2.5 t/ha a year dry wood for broadleaf coppice (03_crafts §1.1) | poles and stakes, tool handles, spear shafts, hurdle uprights (m) | poles; rods for traps (the Fergus trap's inner basket is mostly alder) | bark, then the peeled poles for charcoal or stakes | crooked rods, fewer straight ones; mostly firewood |
| **Labour** | cutting, sorting and bundling an acre of hazel: about 2 to 3 weeks for one man (est.), about 500 to 700 rods a day | | | **peeling April to June**, when the sap rises and the bark lifts; at other times it sticks (sec.); one modern peeler 3 to 6 t of bark a year (sec.) | |
| **Durability** | hazel stakes a few years in the ground (m) | not durable in the ground (m) | **very durable kept wet**: alder piles at Ravenna (Vitruvius) and under the Rialto (Evelyn) (sec.; a modern caution: permeable woods suffer bacterial decay in water); rots fast at the wet-and-dry line (m) | oak heartwood stakes decades (m) | |
| **Capital** | a wood held and fenced against beasts and deer for its first years after each cut (bank, ditch, hedge), cut in panels (03_crafts §1.4) | | | | none |
| **Competing uses** | firewood, charcoal, grazing and browse, pannage, game cover, the standards' timber | | | tanning against charcoal for the same oak (03_crafts §6) | |

Charcoal only as a competing use: about 8 kg of wood a kg of charcoal (archaeometallurgy); the engine's 5 timber to 1 sits inside
the range of clamp yields (03_crafts §1.2). A collier on a coppice takes the same young wood the hurdle-maker wants.

### 1.4 Bark

| | Oak bark (tanning) | Bark for nets (barking) |
|---|---|---|
| **Source** | oak coppice under about 40 years (the inner bark richest in tannin); or oaks felled in spring (sec.) | oak or birch bark decoction; cutch (an imported extract) after 1850 (sec.) |
| **Season** | **April to June only** | any time the bark is to hand |
| **Yield** | no clean figure found; a modern peeler 3 to 6 t a year, another 660 kg from about an acre (sec.); bark is perhaps 10 to 15% of a small oak pole's mass (est.) | small: a few kg for a net (est.) |
| **Labour** | peeling with a spud, drying in stacks (m) | nets soaked in a hot or cold decoction; new nets barked before use and regularly after (sec.) |
| **Uses** | the tan pit: 6 to 8 months for leather, more for sole (03_crafts §6) | slows the rot of nets, lines, sails and cod traps of plant fibre |
| **Capital** | the coppice, the tan pits | a bark pot (a copper or cauldron) |

### 1.5 Reeds, rushes, sedge

| | Water reed (*Phragmites*) | Rushes (soft rush, *Juncus*; bulrush, *Schoenoplectus*) | Sedge (*Cladium*) |
|---|---|---|---|
| **Source** | fen, reedbed, river margins | wet pasture, fen edge, river margins | fen |
| **Yield** | **about 300 bundles an acre** (750 a ha) of a decent bed, a rule of thumb (thatchinginfo; sec.); an annual ("single wale") or two-yearly ("double wale") crop | dense; not quantified | cut every 3 to 4 years (m) |
| **Season** | **November to mid-March**, not in wet weather (sec.) | late summer, full grown (m) | summer (m) |
| **Labour** | **about 100 bundles a day** cutting by hand (sec.); a roof needs 1,500 to 2,000 bundles (sec.) | rushlights: peeled to the pith with one strip of rind, dried, dipped in fat. **Over 1,600 to the pound**; a rush of 28.5 inches burned **57 minutes** (Gilbert White, 1775; sec.) | |
| **Uses** | thatch (water reed lasts longest of the thatches, up to about 50 years, 03_crafts §4), screens, arrow shafts in some cultures | rushlights, strewing floors, mats, chair seats, baskets (frails, bass bags for fish) | ridges of thatch, fuel for ovens and kilns |
| **Gear** | little: reed screens in some fisheries | a fish frail | none |

### 1.6 Bracken, heather, gorse

| | Bracken | Heather (ling) | Gorse (furze, whin) |
|---|---|---|---|
| **Source** | heath, wood edges, hill pasture | heath, moor | heath, rough pasture |
| **Season** | late summer and autumn (m) | any; pulled or cut (m) | winter (m) |
| **Uses** | bedding for beasts and people, thatch under-layer, flooring, packing and lining pits (a bird-lime pit lined with fern), quick fuel, potash from its ash (sec.) | thatch, besoms, ropes, bedding, fuel for kilns (sec.) | **the favourite fuel for bread ovens** wherever it grew, cut and tied in **faggots** (sec.); kiln fuel; bruised as winter fodder for horses (m); cut perhaps every 3 years (Surrey; sec., unverified) |
| **Rights** | cutting rights registered on Welsh commons in 1965 (sec.) | | commoners' fuel; one Oxfordshire limit, as much as one could carry on one's back (sec., unverified) |
| **Gear** | none | none | none |
| **Caution** | poisonous to beasts as fodder | | |

### 1.7 Pitch and tar, glue, bird lime, wax

| | Pine tar and pitch | Birch tar | Hide and fish glue | Bird lime | Beeswax |
|---|---|---|---|---|---|
| **Source** | resinous pine roots and stumps, dry-distilled in a pit or kiln; pitch is tar boiled down (m) | birch bark, dry-distilled | hide scraps, hooves, sinew, bone; fish skins and swim bladders | **holly** bark (or mistletoe berries) | wild or kept bees (wildlife.md) |
| **Yield** | a modern Finnish pyre of **60 m³ of roots gives about 2,000 litres** in a four-day burn; small Viking-age settlement pits rarely over **15 litres a firing**, large forest pits 200 to 300 (Viking Ship Museum; Antiquity 2018; sec.) | **1 to 10 g a 100 g of bark** by method (ash mound about 1, pit roll 2.4, raised structure up to 9.6; Kozowyk et al. 2017; sec.) | glue about **5 to 10%** of the waste's mass (leather-industry study; sec.); scraps simmered about 6 hours a batch (sec.) | not found; a season's pot for a fowler (est.) | about 1 part wax to 10 to 20 of honey (m) |
| **Labour** | **3,000 to 4,000 hours for 1,000 litres** (3 to 4 hours a litre) (Viking Ship Museum; sec.) | hours of tending a small fire for grams (est.) | boiling, skimming, drying (m) | bark stripped about midsummer (m); **boiled 6 to 12 hours**; buried or pitted **2 to 3 weeks** to ferment; pounded and washed in running water; fermented again **4 to 5 days**; a third part of oil or grease worked in (Encyclopaedia Britannica 1860; Otago Daily Times 1923; sec.) | rendering the comb (m) |
| **Uses in gear** | boats' seams, tarred lines and nets, rope | hafting arrow and spear heads, sealing | fletching, backing bows, hafting | **limed twigs** for small birds | waxing bowstrings and thread |
| **Capital** | a tar pit or kiln; pine woods (scarce in a lowland temperate world) | none | a pot | a pit | a hive |

### 1.8 Bone, antler, horn; leather for gear

| | Bone | Antler | Horn | Leather (for gear only) |
|---|---|---|---|---|
| **Source** | every carcass | cast antler (engine: `antler`) or a kill's | cattle and sheep horn (engine: `horn`) | hide |
| **Working** | sawn, split, ground; a gorge or simple hook under an hour with a metal knife (est.) | **soaked** (days to weeks) to soften, though it can be worked dry at great labour (Langley and Wisher, EXARC 2019; Osipowicz; sec.); a barbed point several hours with flint, an hour or two with metal (est.) | soaked and heated, split and pressed into plates (lantern panes), spoons, handles (03_crafts §6) | rawhide, tawed or oil-dressed hide does for straps, quivers, sling pouches and hawk furniture; bark tanning takes 6 to 18 months in pits (03_crafts §6) |
| **Uses in gear** | gorges, hooks, net needles and mesh gauges, points, awls | harpoons and leister points, handles, net-making tools | handles, nocks, horn bows (composite; outside this world), hunting horns (engine already has `make a horn`) | straps, quivers, packs, sling pouches |
| **Capital** | none | none | none | none for rawhide; tan pits for leather |

## 2. The developmental structure

### 2.1 The paradigm shift: from wild rods to a managed bed or coppice

The supply of rods has two states, and the move between them is the shift:

- **Wild (anyone, nothing needed):** cut rods where they grow: sallow and osier along the water, hazel and young ash in scrub and
  unworked wood. The rods are scattered, crooked and branched, slow to gather and seasonal (winter rods are good; summer rods are
  leafy and brittle). Wild willow is hard to exhaust: cut, it sprouts again (that is coppicing). What kills it is grazing, deer and
  beasts on the regrowth, which the engine already models for young growth.
- **Managed (a household or a village, years of waiting):** plant a withy bed on wet ground by the water, or cut a hazel wood in
  panels on a rotation behind a fence. The rods are straight, even, near at hand and three or more times as fast to cut; the bed or
  coppice is held, not common, and it must be kept from the beasts. A household can plant a bed; a coppice is a village's or a
  lord's, with rights and a calendar.

What a managed source changes is the **rate and the certainty**, not whether gear can be made at all. Every piece of gear can be made
from wild rods, more slowly: Zach's "it should be possible to do things with less layers, that have less beneficial outputs".

### 2.2 What each scale can do

| Scale | Supply | Gear | What it costs |
|---|---|---|---|
| **A person with nothing** (bare hands or a knife) | wild rods at the water or in scrub, about 1.5 bundles a unit in winter, much less in summer (est.) | a crude wicker trap, a hurdle, a rough basket; hand fishing and a rod | slow; untaught work about twice as long and the trap lasts about half as long (est.) |
| **A person with the skill** (taught or practised) | the same | traps, hurdles and baskets at the skilled rates of §1.2 | the know-how only |
| **A household** (a bed or the right to cut) | a withy bed of about 200 m² on wet ground: 1 bundle of cuttings and about 10 units; about half its yield in the second world year and full from the third; about 30 bundles a year at full yield, cut at 4 a unit (est.) | traps renewed every year or two; hurdles for a fold or smoke racks; a share of a weir's wattle | wet ground near water, kept from the beasts; two world years of waiting |
| **A village** (a crew, a coppice, rights) | a coppice in panels: about 125 bundles a ha a year of hazel rods (about 250 a unit of size), poles for stakes without felling the standards, oak bark in spring later (est., from Durham 1956) | the weir (a crew of 2 or more); later the deer hay, the park pale, fish garths | rights over the wood across years, fencing, the commons' fights over firewood against rods |

### 2.3 Shallow ladders

Two rungs on the supply side (wild, managed) and two on the gear side (a set trap for a household, a weir for a village) are enough;
each rung is optional and each is worth having on its own. The processing steps between a cut rod and gear (sorting, soaking,
boiling to buff, pitting and stripping to white) matter to a fine basket and not to a trap, a hurdle or a weir, so they are
compressed out (§3.2). The four-rung chain (rods, then sorted rods, then prepared rods, then gear) is exactly what Zach called "a
terrible idea"; the gear here is one making step from a cut rod.

The chokepoints that come with it (docs/scenario_design.md): wet ground by the water is held by whoever holds the meadow; the
coppice is the holder's (in Wenbridge, "the lord's hazel and ash coppice by the river"); the weir needs a crew and a site; and the
grazing that kills regrowth puts the herds against the rods. A household without wet ground must cut wild rods, buy them, or ask.

## 3. Granularity for the engine

### 3.1 Goods

| Material | Recommendation | Why |
|---|---|---|
| **withies** | **add**: one good for willow and hazel rods alike; a unit is a bundle of about 10 kg green rods (about 25 hazel rods of 2 to 3 m, or a hundred fine willow rods), weight 1 | traps, hurdles, the weir's wattle and baskets need rods and nothing else in the engine stands for them; the species is a presentation choice (words), not a state |
| **poles and stakes** | **fold into timber**, but let a managed wood's young growth give timber as poles (`cut poles` at a managed wood: about 4 firewood-mass of young growth a timber, as `FORESTS.per_timber`) | stakes are timber in every recipe now; what is missing is getting them without felling standards; and the alias "cut poles" now gives firewood |
| **bark** | **wait** for leather (L-111, tan pits): then one good, peeled only in spring, a joint product of felling oak or cutting poles in an oak-ash or managed wood (about 0.1 to 0.15 of the wood's mass, est.) | gear needs no tanned leather; net barking is a small step folded into net making |
| **pitch and tar** | **leave out** until boats; birch tar for hafting folded into the gear recipe (grams) | a lowland temperate world has little pine; tar is heavy labour for little gear use |
| **glue** | **fold** into the recipes that need it (a little hide or offal in a bow or arrows) | used in grams |
| **bird lime** | **leave out** unless the fowling note adds a limed-twig method; then one good, made from holly bark (§1.7) in a pit over weeks | it is a clean example of a cheap method with a slow, waiting preparation |
| **wax** | leave out of gear | bowstring wax is grams |
| **bone** | **an open question** (§4): add `bone` at butchering, or let gear take `antler` or `horn` for hooks, gorges and points | economy_web.md proposes bone with horn and antler as one good; the engine already has `antler` and `horn` |
| **reeds** | leave out of gear; add with thatch when roofs come (the building owner's area) | |
| **rushes** | **folded already** into `tallow light` | |
| **sedge** | leave out | |
| **bracken, heather** | leave out, or a non-fodder bedding good later | folding them into `straw` would let beasts eat bracken, which poisons them |
| **gorse** | **fold into firewood**: let `cut` take young growth at heath (gorse and broom faggots), the oven's fuel | one row's `at`, no new good |
| **leather** | gear takes `hide` (rawhide or dressed) for straps and quivers | leather waits for its own brief |

### 3.2 Steps compressed or left out

- **Preparing rods** (sorting, soaking, boiling, pitting, stripping): out. Withies have no state; brown rods are the default. Fine
  white and buff work is a basket-maker's quality, not a gear input.
- **Seasoning:** out. A rod cut green weaves at once; a dry one is soaked. The difference is days and belongs inside the making's units.
- **Rotation by panels:** out as a state. The young-growth stock with its logistic regrowth stands for a wood cut in panels; cutting
  too much leaves the stock low and the rate falls, which is the rotation's lesson without a panel record (economy_web.md open
  question 2: this answers it as "a wood's yield, no rotation state", with the regrowth as the rotation).

### 3.3 Where rods come from

- **Cut withies** (a new gather technique): at a **managed wood** it draws young growth, about 0.1 of a firewood's young growth a
  bundle (est.: a bundle is about 10 kg green, about 6 kg dry, against firewood's 60 kg), at **4 bundles a unit** with a crude tool;
  at **any other forest or scrub** at about 1.5 a unit (crooked rods); at **wet ground** (fen, alder carr, wet meadow or pasture, a
  parcel on a river) from a **wild willow** stock at about 1.5 a unit; bare-handed 0.3, a copper blade 1.3. By season: winter 1.0,
  autumn 0.8, spring 0.5, summer 0.3 (est.).
- **Wild willow:** a stock on wet parcels in the young-growth regime (it regrows fast, not while beasts graze), small: about 30 to
  60 bundles a unit of size, regrowing 1.0 a year (est.). Either a new resource row with `renewal: young`, or the young-growth stock
  extended to wet parcels of fen and meadow (an open question).
- **A withy bed** (a work, not a parcel use): a unit of size is about 2 ha and a bed for a household is about 200 m², a hundredth of
  that. So a bed is a **work on a wet parcel** (as the smokehouse and the weir are works), built with 1 withies (the cuttings) and
  about 10 units (digging and planting; est.: about 840 cuttings and two days' digging), holding its own small stock: nothing the
  first world year, half the second, full from the third, about 30 bundles a year (13 to 20 t/ha green), cut at 4 a unit; stopped
  while beasts graze the parcel; lasting the run. Whether it keeps the real two to three years or is compressed as the salmon's
  return was (D2-209) is an open question.

### 3.4 Gear on the engine's basis

| Thing | Materials | Units | Life and wear | Real basis |
|---|---|---|---|---|
| **wicker trap** (a new good, `uses` on `trap in water`) | **0.5 withies** | **3** (taught); about 6 untaught | about two world years in use (calibrate: about 30 set nights), and the spate and flood wreck as now | an eel trap of 2 to 3 kg dry rods (about 5 kg green); a withy pot 4 to 5 hours; putchers and pots last about 2 years with repair |
| **hurdle** (a new good) | **1 withies** | **1.5** | 5 to 10 world years dry (calibrate) | 2.5 to 3 hurdles a day; about 30 rods |
| **smoke racks** (the fitting, "hurdles over a smouldering fire") | 2 hurdles and 1 timber, or **2 withies and 1 timber** (was 2 timber) | 2 (was 2) | as now | two hurdles on a frame |
| **wattle weir section, added** | **12 withies and 1 timber** (was 6 timber) | **16** (as now) | wattle wear 1.0; a level's mend about 1 withies | about 15 m² of wattle (10 m by 1.5 m) at about 20 rods a m², about 300 rods or 120 kg; about 25 stakes of 5 to 8 kg, about 150 to 200 kg (one timber); about 15 hours weaving and 6 driving stakes, so 21 hours or 11 units against the engine's 16 (within its spread for work in water) |
| **the first section's base** (stakes across the river and its trap) | **4 timber and 2 withies** (was 6 timber) | **8** (as now) | | heavier posts across the river (oak or alder), and the trap in the gap |
| **wattle first section** (base and wattle) | **5 timber and 14 withies** (was 12 timber) | 24 (as now) | | |
| **timber section** | 10 timber (as now) | 25 (as now) | 0.5 | upgrading a wattle section pays its 9 timber and 9 units; the withies are not returned |
| **fishing rod** | **0.1 withies** (one long rod) and the line (with the cord note) (was 0.5 timber, about 120 kg) | 1 | 30 days' use (as now) | a hazel or willow pole of about 1 kg |
| **basket** (optional) | 0.3 withies | 3 | a few world years | only if a carrying or keeping use is wanted |

What it does to the weir's year: D2-210's upkeep of about half a wattle section's cost a year becomes about **6 withies a year** a
wattle section. A household bed of 200 m² (about 30 bundles a year) keeps one section and a few traps; the weir's crew needs a bed,
a coppice, or a week of cutting wild rods each winter. The carrying is unchanged: 12 withies and 1 timber weigh 14 against 6 timber's
12, so a section is still two loads from the wood to the river.

### 3.5 Engine seams (D2-244)

A withies unit is its own feature: the good (`ITEMS`), the gather technique and its `by_season`, the wild-willow stock (a `RESOURCES`
row or the young-growth extension), the withy-bed work, the gear recipes (`wicker trap`, `hurdle`), the weir's `WATER_WORKS`
materials, the `trap in water` method's `uses`, and the signs (a stripped bank, a bed grazed down, a winter's rods cut). Listed
together, the cut into feature packages can move it whole. Signs follow the senses guide (docs/cybertron2/guides/senses.md): a bank
cut bare or a bed browsed is a change worth acting on; the standing fact that willow grows somewhere is not.

## 4. Open questions

1. **Withies as one good** for willow and hazel, a bundle of about 10 kg green rods at weight 1?
2. **The withy bed as a work on a wet parcel** (about 200 m², its own small stock) rather than a parcel use, and its years to full
   yield: kept at two to three world years, or compressed to one as the salmon's return was (D2-209)?
3. **Wild willow:** a new stock on wet parcels in the young-growth regime, or the existing young growth extended to wet fen and
   meadow?
4. **Poles from a managed wood's young growth as timber**, so stakes need no felling; and the `cut` alias "cut poles", which now
   gives firewood?
5. **The weir on withies:** a wattle added section 12 withies, 1 timber and 16 units; the first section's base 4 timber, 2 withies
   and 8 units; upkeep about 6 withies a year a section. Do the units stay at D2-210's values?
6. **Traps that cost something:** a wicker trap at 0.5 withies and 3 units, lasting about two world years; how existing worlds and
   seeded households get their traps (seeded with some, or none)?
7. **The fishing rod** at 0.5 timber (about 120 kg of wood) is about a hundred times a real rod's mass: change it to 0.1 withies?
8. **Bone:** a new good at butchering, or hooks and points made from `antler` and `horn`?
9. **Bracken and heather as bedding:** a non-fodder bedding good, or left out?
10. **Gorse:** let `cut` take young growth at heath, as firewood (faggots for ovens)?
11. **Left out for now:** bark (until leather), pitch and tar (until boats), glue, wax, reeds (until thatch), sedge, and bird lime
    unless fowling takes a limed-twig method. Agreed?
12. **Labour figures** for craft work are wider than D2-259's 20%: the hurdle and the withy pot are measured today; the eel trap,
    the weir's wattle in water and the bed's cutting rate are estimates. Calibrate them as named levers?

## Sources

Engine and project: `cybertron2/engine/data.py` (ITEMS, TECHNIQUES `cut`, `fell`, `firewood`, `fishing rod`, FORESTS, COVERS,
RESOURCES, WATER_WORKS), `cybertron2/engine/forests.py`, `cybertron2/wild/plants.py`, `cybertron2/wild/methods.py` (SETS),
`cybertron2/wild/gear.py`, `cybertron2/wild/kinds.py`, `cybertron2/landgen/settle.py`, `cybertron2/specs/make_wenbridge.py`;
docs/cybertron2/spec/environment/resources.md (Forests, D2-156); docs/cybertron2/proposals/economy_web.md (§2.6, open question 2),
economy_later.md, wildlife.md, river_and_water.md (§3b, open question 7); docs/review/37_growth/02z_forest_model.py (a timber about
240 kg; a unit of size about 2 ha), 02zzw_water_fixes.md, 02zu_wild_chains_capital_actions.md,
02zzj_economy_research/03_crafts_woods_metal_building.md (§1, §4, §6, §7); OPEN L-111; D2-209, D2-210, D2-259.

Withies and osiers:
- Planting density, harvest season, bed life: [Farmers Weekly, willow diversification](https://www.fwi.co.uk/farm-life/willow-diversification-secures-beef-farm-s-future); [woodlands.co.uk, willow and wetlands](https://woodlands.co.uk/blog/woodland-activities/willow-and-wetlands); [Osier bed](https://en.wikipedia.org/wiki/Osier_bed).
- Basket willow yields: G. N. Lamb, *Basket Willow Culture*, USDA Farmers' Bulletin 622 ([Wikimedia Commons scan](https://upload.wikimedia.org/wikipedia/commons/7/73/Basket_willow_culture_(IA_CAT31127691).pdf), read through a search summary); [Forest Research, growing short rotation coppice](https://cdn.forestresearch.gov.uk/2022/02/growing_short_rotation_coppice_tcm6_2004.pdf); [University of Kentucky willow profile](https://publications.ca.uky.edu/sites/publications.ca.uky.edu/files/willow.pdf).
- Brown, buff and white; boiling hours; the brake; peelers: [Northumbria Basketry Group, Somerset visit 2010](https://northumbriabasketrygroup.co.uk/gallery/somerset-visit-november-2010); [lowimpact.org, how to create white willow](https://www.lowimpact.org/posts/how-to-create-white-willow); [Lives in War, the willow industry](https://everydaylivesinwar.herts.ac.uk/wp-content/uploads/2017/09/8-The-willow-industry.pdf); [MERL brake record](https://www.reading.ac.uk/adlib/Details/collect/24063).
- Withy pots: [Reading, Making a withy pot](https://blogs.reading.ac.uk/sense-of-place/?p=958); [Fishing News, Dave French](https://fishingnews.co.uk/a-day-in-the-life/a-day-in-the-life-of-withy-pot-maker-dave-french/).
- Putchers and the basket-weir: [Gloucestershire, fixed trap fishing](https://www.gloucestershire.gov.uk/media/k02ltwvz/6-2a-fishing-on-the-estuary-1-fixed-trap-fishing.pdf); [Museum Wales, putcher](https://museum.wales/collections/online/object/75f88735-74ab-35bd-98f1-6929a403936a).
- Eel traps: [Denny Farmland Museum, everything eels](https://www.dennyfarmlandmuseum.org.uk/content/museum-blog/everything-eels); Fergus estuary weirs and the hazel and alder double basket trap: [excavations.ie, Boarland Rock](https://excavations.ie/?p=21287), [phys.org, Irish medieval fishing site](https://phys.org/news/2011-02-irish-medieval-fishing-site-lost.pdf).

Coppice and hurdles:
- Durham 1956 (10,000 rods an acre, 300 hurdles) via [Forest Research FCIN056](https://cdn.forestresearch.gov.uk/2004/01/fcin056.pdf); stools a hectare: [Conservation Handbooks, species and growth](https://conservationhandbooks.com/?p=379) (search summary only).
- Hayley Wood's medieval 7-year cycle (Rackham): [Royal Forestry Society, Leslie, July 2025](https://rfs.org.uk/leslie-july-2025-qjf); O. Rackham, *Ancient Woodland* (1980) and *Trees and Woodland in the British Landscape* (1976), to verify.
- Hurdle rates: [Farmers Weekly, hazel hurdles](https://www.fwi.co.uk/arable/orders-pour-in-for-traditional-hazel-hurdles); [lowimpact.org, hurdles](https://www.lowimpact.org/categories/hurdles); [woodlands.co.uk, making hazel hurdles](https://woodlands.co.uk/tv/2013/10/making-hazel-hurdles/comment-page-1).
- Alder in water: [Carpentry Principles, alder](https://chestofbooks.com/home-improvement/woodworking/Carpentry-Principles/Alder-Alnus-Glulinosa.html); bacterial decay caution: [Structure magazine, timber piles](https://structuremag.org/wp-content/uploads/2014/08/C-StrucForensics-Vatovec-Dec131.pdf).

Bark: [Bolton-le-Sands, oak bark peeling](https://boltonlesandsparish.gov.uk/amenities/thwaite-brow-woods/oak-bark-peeling/); [ODI, productive potential of ancient oak coppice](https://cdn.odi.org/media/documents/1070.pdf); net barking: [Bark pot](https://en.wikipedia.org/wiki/Bark_pot), [As Manx as the Hills, nets](https://asmanxasthehills.com/nets-and-equipment-for-herring-mackerel-fishing-isle-of-man-manx/), [NOAA fishery leaflet 66](https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet66.pdf).

Reeds, rushes, sedge: [Conservation Handbooks, reedbeds](https://conservationhandbooks.com/?p=3905) (search summary); [Thatch Advice Centre](https://www.thatchadvicecentre.co.uk/?p=211); [thatchinginfo, water reed and sedge](https://thatchinginfo.com/?p=281); Hawke and José, *Reedbed management for commercial and wildlife interests* (RSPB 1996), not seen; rushlights: [Rushlight](https://en.wikipedia.org/wiki/Rushlight), [rushlight.org](https://rushlight.org/wp-content/uploads/articles/juncus.html), Gilbert White, *Natural History of Selborne*, letter to Barrington (1775), to verify against the text.

Bracken, heather, gorse: [Historic England, bracken palaeoethnobotany](https://cms.historicengland.org.uk/content/docs/advice/bracken-the-palaeoethnobotany-of-pteridium-aquilinum); [Legendary Dartmoor, gorse](https://www.legendarydartmoor.co.uk/2016/03/23/gorse_bush/); [Sidmouth Herald, gorse](https://www.sidmouthherald.co.uk/news/sid-valley-biodiversity-group-gorse-6862600); [Kildare Libraries, furze](https://kildarelibraries.ie/ehistory/?p=7820).

Tar, glue, bird lime: [Viking Ship Museum, tar](https://www.vikingeskibsmuseet.dk/en/visit-the-museum/exhibitions/previous-exhibitions/the-reconstructed-ship/tar); [Antiquity 2018, Viking-age tar production](https://doi.org/10.15184/aqy.2018.22); [Kozowyk et al. 2017, birch bark tar](https://pmc.ncbi.nlm.nih.gov/articles/PMC5579016); [CAMEO, hide glue](https://cameo.mfa.org/wiki/Hide_glue); [Encyclopaedia Britannica 1860, birdlime](https://jimclifford.ca/early_encyclopedia_britannica/articles/1860/eb_8th_1860_003311.html); [Otago Daily Times 1923](https://paperspast.natlib.govt.nz/newspapers/ODT19230113.2.34); [Birdlime](https://en.wikipedia.org/wiki/Birdlime).

Antler: [Langley and Wisher, EXARC 2019](https://exarc.net/ark:/88735/10419); [Osipowicz, bone and antler softening, EuroREA 4](https://EXARC.net/sites/default/files/EuroREA_4-www-Grzegorz_Osipowicz-Bone_and_Antler.pdf).

Current as of 21 Nov 2026 (W-73; nothing decided).
