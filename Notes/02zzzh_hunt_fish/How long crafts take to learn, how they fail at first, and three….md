---
id: docs/review/37_growth/02zzzh_hunt_fish/learning_times.md
kind: note
updated: "2026-11-22"
---
# How long crafts take to learn, how they fail at first, and three difficulty classes for trying and learning

*note · `docs/review/37_growth/02zzzh_hunt_fish/learning_times.md`*


22 Nov 2026, 37.2 (subagent). Research note for the general system of attempting and learning crafts. No code changed.

Zach (22 Nov): "failures always have to be more informative and give in-engine knowledge as well as instruction ... more
informative the more times they fail ... learning should be relatively forgiving for learning the minimal / awareness of new
things ... some should be basic while others require more mastery ... the familiarity multipliers probably shouldn't be the same
for everything but depend on the difficulty of a craft. Some if anyone tries they can probably do, while others require deep
practice or teaching."

**Read with:** the crafts evaluation ([crafts_evaluation.md](crafts_evaluation.md): the knowledge levels and their paths as
built, `aware` made tryable for 10 rows), fibre and cord ([fibre_and_cord.md](fibre_and_cord.md) §5: who did the fibre work),
withies and wood ([withies_wood_materials.md](withies_wood_materials.md): hurdle and trap rates), the hunting ladder
([hunting_ladder.md](hunting_ladder.md)).

**How the sources were read.** Web search only. The one page fetch tried (engr.psu.edu, the Penn State charcoal essay) was
blocked by the session's network (host not allowed); every source below was read from search-result summaries and abstracts, not
full texts. Where a number comes from a summary of a paper, it is given as the summary states it. Everything marked **(est.)** is
my estimate, not a source.

---

## 0. In brief

- **The evidence splits crafts three ways, much as the design proposes.** Some work crudely on the first try and improve mostly
  in speed and yield (line fishing, snares, cord, salting, the quern, dressing a carcass). Some work on the first try only now and
  then, take a season or a few years to do reliably, and are learnt in the household by watching and trying (baskets and traps,
  netting, hurdles, smoking, spinning flax, oven baking, charcoal, a hunting bow, ploughing). A few were held by specialists under
  long apprenticeships (five to ten years), fail outright for a beginner, and were taught, not picked up (smithing, copper
  working, tanning).
- **Apprenticeship terms:** about seven years was the norm for a trade, made the legal minimum in England by the Statute of
  Artificers of 1563; blacksmiths 5 to 7 (some sources 5 to 10); a Bridgwater tanner's apprentice in 1424 was bound for ten
  years; basketmakers seven ("five" in another account); servants in husbandry bound to 21; a modern longbow apprenticeship of
  three years; Langda stone adze makers five to ten years (Stout 2002).
- **Skill takes long even where the craft is "simple" in steps:** Tsimane hunting skill keeps rising ten to twenty years past
  adult body size (Gurven et al. 2006); across 40 societies hunting returns peak at about 33 (Koster et al. 2020). But Meriam
  children's line and spear fishing returns show no significant age effect (Bird and Bliege Bird 2002): fishing with a line is
  the clearest case of a craft that anyone who tries can do.
- **Skill acts on yield in some crafts and on waste or quality in others.** Charcoal is the best measured: FAO gives 1 ton of
  charcoal from 4 tons of wood as good practice and 1 from 6 as common, "varying with skill of burning, dryness of fuelwood and
  air-tightness" (a 1.5 times range). Netting and hurdles differ mostly in speed (an experienced netter about 1,300 knots an
  hour; a hurdle maker 2.5 to 3 hurdles a day, a beginner about half). Smoking, salting, tanning and baking differ in waste (the
  spoiled batch), smithing and bows in both waste and quality.
- **What the engine should take:** three classes, each setting first-try chance and waste by level, the practice to rise, how
  far practice alone goes, and how wide the skill curve is; the practice measured as a share of a life (scaled with the
  lifespan, [[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], as the hunt already is), because a seven-year apprenticeship is more work than an engine life holds. And each
  failure reports one lesson from an ordered list per craft, the next one not yet learnt, so the second failure says something
  the first did not (§4, §5).

---

## 1. Mapping real learning times onto the engine

The engine has two clocks: the ecology's year is 32 days (a real year, 1:1 on seasons, as the salmon's return and a withy bed's
years are), but a life is far shorter: the lifespan is a world setting ([[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], default 32 days to old age; the worlds in
`cybertron2/specs/` mostly use 96, some 48 or 64, [[D4-116 Lifespan 64 in the peoples worlds; the year unchanged|D4-116]]). Learning belongs to the life clock: an apprentice's seven years are
seven years of his life, not seven ecological years.

| | Real | Engine at lifespan 96 (est.) |
|---|---|---|
| Life to old age | about 55 years (est., a medieval working life) | 96 days |
| One year of life | about 250 to 300 working days, 2,500 to 3,000 hours | about 1.75 days, about 10 units of work |
| Share of one's work at one's main craft | most of it for a specialist; less in a household | about a third to a half: **3 to 5 units of the craft a life-year** (est.) |
| A seven-year apprenticeship | 15,000 to 20,000 hours | 12 days of life, **about 25 to 35 units at the craft** |
| Ten to twenty years to a hunter's or smith's peak | | **35 to 100 units at the craft** |

Hours cannot be mapped one to one: a seven-year apprenticeship (about 8,000 to 10,000 units by hours) is more than an engine life
holds (about 96 x 6 = 580 units). So the practice a class needs is set as **units of the craft, at lifespan 96, scaled with the
lifespan** (practice counting lifespan-96 / lifespan times over, as `practice_x` already does for the hunt). On this mapping the
current `tau` 50 (95% of the way after 150 units) sits at the slow end: right for a skilled craft, too slow for a simple one.

---

## 2. The crafts

Each table: first attempts and what goes wrong; time to competence and to mastery; how it was learnt and from whom; what skill
changes; the engine row it touches. Sources by letter (§7).

### 2.1 Setting snares (engine: `snare`, gather, basic)

| | |
|---|---|
| First tries | A snare is easy to make and set; a first line of snares usually catches little. The failures are placement and setting: noose set too high or low for the grass (rabbits duck under or knock it aside), loop too large or small (guides give a fist, about 15 to 18 cm; a beginner's 10 cm "until you become familiar"), set off the run or at a "seat" instead of on the fast beats between them, the snare knocked and sprung without a catch ("set a couple of inches further along the run until you get it right"), the peg pulled. [a] |
| Competence, mastery | Competence in days to weeks of setting (est.); a warrener's or keeper's yield (one practitioner reports 89 catches from 100 peg snares on pasture, anecdotal) after years of reading runs. [a] |
| Learnt | Watching and trying, boys with a father or keeper; "learn by trial and error". [a] |
| Skill acts on | Yield (catches a set), not waste: the snare is kept. |
| Class | **Simple.** |

### 2.2 Twisting cord by hand (no engine row yet; fibre_and_cord.md proposes one)

| | |
|---|---|
| First tries | Works on the first try, crudely: "the first few attempts may be loose or uneven". The one hard rule: twist each ply one way and wrap the plies the other way; twist and wrap the same way and the cord unravels. Thick and thin plies give a weak cord that breaks at the thin place; splices pull out if the new fibre is not overlapped. [b] |
| Competence, mastery | Hours to an even cord (est.); speed and evenness keep improving for years; "pretty slow going" by hand even for the practised. [b] |
| Learnt | Watching and trying, in the household; women, children and old men did most fibre work [fibre_and_cord §5]. |
| Skill acts on | Yield (metres an hour) and quality (strength). |
| Class | **Simple.** |

### 2.3 Weaving a wicker eel trap or basket (engine: `trap in water` uses traps; making them is not a row)

| | |
|---|---|
| First tries | A first basket can be made in a one-day course and comes out "a little wonky". What goes wrong: a lopsided base when butts and tips of the stakes are not alternated; a base that twists from uneven tension; stakes that crack at the upsett (the bend up from the base) if dry or not pricked; weavers too thick to bend; fresh green willow that shrinks the first time it dries and leaves the weave loose. For a trap the hard part is the throat (the inward cone, "chale"): too wide and the eels go back out. [c] |
| Competence, mastery | A serviceable basket in days to weeks (est.); the trade apprenticeship was seven years (another account, five) [c]. Severn putchers were made by the fishermen themselves in winter [c]. |
| Learnt | Fishing families for traps; specialist basketmakers for the trade; a craft that declined fast once the old makers died ("in the evening of their lives", Green 1992) [c]. |
| Skill acts on | Speed (yield) and tightness and life of the trap (quality). |
| Class | **Practised.** |

### 2.4 Netting (knotting a net; engine: `net` is netting birds; making net is not a row)

| | |
|---|---|
| First tries | The netting knot is learnt in an hour and holds on the first net; the first net is badly shaped: meshes uneven unless the knot is drawn close to the mesh stick, knots slip if not drawn tight, a dropped mesh leaves a hole. [d] |
| Competence, mastery | A good pace is "15 or more knots a minute" (900 an hour); experienced netters averaged about 1,300 knots an hour on fine string (about 1,750 at most) [d]; a beginner's first hours perhaps 100 to 300 (est.): a five times range. |
| Learnt | In fishing villages women, girls and old men knitted the nets through the winter [fibre_and_cord §5]; learnt young, alongside knitting. [d] |
| Skill acts on | Speed (yield) above all; evenness (quality). |
| Class | **Practised** (easy to do at all, slow to do fast). |

### 2.5 Fishing with a line (engine: `angle`, gather, basic; `fishing rod`, make, basic)

| | |
|---|---|
| First tries | Usually catches something where fish are many. Failures: wrong place or hour (no fish feeding there), hook too large for the fish, bait washed off or dead, line seen in clear water, striking too soon or too late. (est., from general angling practice) |
| Competence, mastery | Among the Meriam, line and spear fishing returns showed **no significant variation with age-correlated experience**; children reach adult efficiency faster in fishing than in shellfish collecting (which strength limits) [e]. |
| Learnt | Watching and trying, children with adults. [e] |
| Skill acts on | Yield, mostly through knowing places and times; small range. |
| Class | **Simple.** |

### 2.6 Building a wattle weir or hurdle (engine: `weir`, build 24 units, basic; `fence`, work, basic)

| | |
|---|---|
| First tries | A beginner makes about half a hurdle in a day, a skilled maker 2.5 to 3 [f; withies note]. Failures: rods not twisted at the turn round the end sail, so they snap; sails too far apart, so the weave sags; weavers not beaten down, so the hurdle is loose. A weir's own failures are siting and strength: set where the flood takes it, the trap gap off the main flow. Excavated estuary weirs were rebuilt often, some at least once a year, and lasted no more than about ten years (Fergus estuary, tree rings) [g]. |
| Competence, mastery | A five-day course teaches the hurdle; "much quicker, and neater, with experience"; makers with 25 to 30 years at it [f]. |
| Learnt | Hurdles from a maker (one trained by a family "making hurdles for over 300 years") [f]; weirs by the fishermen who worked them, rebuilding and emptying them at each low tide [g]. |
| Skill acts on | Speed (yield) and life of the work (quality: how long before the flood or the sheep break it). |
| Class | **Practised.** |

### 2.7 Smoking fish (engine: `smoke fish`, `smoke meat`, `tend the smoke`, make/work, basic)

| | |
|---|---|
| First tries | Usually yields something edible; the batch is what is at risk. FAO on traditional kilns: if the fire bursts into flame the lower rails cook; hurried smoking ("flying") gives a case-hardened fish, dry outside and wet within, that spoils; heat kept in the walls can spoil fish loaded hours before the smoke; fish must first be dried (the skin toughened) before heavy smoke. [h] |
| Competence, mastery | Arbroath smokies: "an experienced smokie maker knows exactly when they are ready", the method "handed down by generations of fishing families" [h]. A season to reliability (est.). |
| Learnt | Household and fishing families. [h] |
| Skill acts on | Waste (fish cooked, case-hardened or spoiled) and keeping quality. |
| Class | **Practised.** |

### 2.8 Salting fish or meat (engine: `salt fish`, `salt meat`, make, basic)

| | |
|---|---|
| First tries | Works if the rule is kept (gutted, enough salt, cool, packed tight). Failures: too little salt and the flesh near the backbone rots before the salt reaches it; too strong or too fast and "salt burn" hardens the surface and stops the salt going in; red ("pink") in warm weather; fatty fish turns yellow-brown ("rust") as the oil oxidises; poor cleaning. Inadequate salting and imperfect cleaning were the main defects found in a survey of curers. [i] |
| Competence, mastery | Days for the household (est.); the herring girls learnt the trade cure at 12 to 15 from relatives [j]. |
| Learnt | Household; trade curing from relatives in fishing families. [i, j] |
| Skill acts on | Waste (spoiled batches); little on yield. |
| Class | **Simple** (household salting); a trade cure for sale would be practised. |

### 2.9 Butchering and skinning game (engine: `slaughter`, work, basic; dressing a kill sits in the hunt's yield)

| | |
|---|---|
| First tries | Gets the meat; wastes some. Failures: cutting too deep and puncturing the gut or bladder, tainting the meat; a dull knife; holes cut in the hide; hair left on the meat; a warm carcass left too long, so it bloats and spoils. "The first time you butcher your own deer the results are going to be less than perfect, and your second deer will be easier." [k] |
| Competence, mastery | A handful of animals to competence (est.); the butcher's trade had its own apprenticeship (est., the seven-year norm). |
| Learnt | Household, watching and helping. |
| Skill acts on | Waste (meat tainted, hide spoiled for tanning). |
| Class | **Simple.** |

### 2.10 Spinning flax with a spindle (no engine row; fibre_and_cord.md proposes one)

| | |
|---|---|
| First tries | Yarn comes on the first try, thick and thin; drafted too thin it breaks and the spindle drops; overtwisted it kinks back on itself; undertwisted it drifts apart. Flax is harder than wool: it sticks "but also may come apart if you look at it wrong", needs damp fingers and a dressed distaff (the strick tied at one end and fanned), and many spinners "shy away" from it; line flax and tow spin differently. [l] |
| Competence, mastery | Girls began as young as four or five (a popular source, unverified) and spun daily for years; fine, even linen yarn is a matter of years (est.). [l] |
| Learnt | From mothers in the household; the distaff and spindle carried all day. [l] |
| Skill acts on | Yield (length an hour) and quality (fineness, evenness). |
| Class | **Practised.** |

### 2.11 Hand milling with a quern (engine: `grind`, make, basic; `hand mill`, build, basic)

| | |
|---|---|
| First tries | Works at once; it is hard work rather than hard skill. Failures: grain fed too fast (coarse meal, half-cracked grain), the stones set too close (grit, heat) or too far (cracked grain), damp grain clogging, worn stones that need dressing. (est., from milling practice) |
| Competence, mastery | Volunteers in an experiment ground 4.3 times more efficiently on a rotary than a saddle quern, with more fine flour [m]: the tool matters far more than the hand. About an hour a day for a household's bread (Mills Archive) [m]. |
| Learnt | A daily household chore, mostly women's. [m] |
| Skill acts on | Yield a little (speed, fineness); small range. |
| Class | **Simple.** |

### 2.12 Baking bread in an oven (engine: `oven bread`, make 3, basic; `bread` at a hearth)

| | |
|---|---|
| First tries | Bread comes out, often burnt below and raw within. Failures: the oven floor too hot (heat comes up from the hearth faster than from the dome), ashes left in, loaded too soon after firing (a beginner's floor at about 340°C "was a big mistake"), hot spots (found with a pinch of flour that burns), the oven not fired long enough to hold heat for the bake, dough under-proved. [n] |
| Competence, mastery | Judging the oven by the dome's colour and the flour test takes many bakes (est., a season); the baker's trade had the seven-year norm, and a German ordinance asked two years more as a helper before a master's shop [n]. |
| Learnt | Household for hearth bread; the baker's trade by apprenticeship. [n] |
| Skill acts on | Waste (burnt loaves) and fuel; quality. |
| Class | **Practised.** |

### 2.13 Making charcoal (engine: `charcoal`, make 2, trade woodsman)

| | |
|---|---|
| First tries | A first clamp usually gives some charcoal with much waste. Failures: the cover breaks through and the clamp flares and burns to ash; parts stay half-burnt ("brands", FAO's word); wet wood; a cover too thin or too thick; the clamp left unwatched in a wind; drawn too early. The collier judged it by the colour of the smoke. [o] |
| Competence, mastery | Yields "vary with skill of burning, dryness of fuelwood and air-tightness": 1 ton from 4 tons of air-dry wood is good practice, 1 from 6 more common [o]; a first clamp perhaps 1 from 10 (est.). |
| Learnt | Collier families living with the clamp in the wood (est., not confirmed by the sources reached). |
| Skill acts on | Yield (charcoal from wood), a 1.5 times range between common and good practice, more for a novice. |
| Class | **Practised** (at the edge of skilled: the failure is total, but the first burn rarely is). |

### 2.14 Smithing iron (engine: no iron row yet; `copper tool`, make, trade smith)

| | |
|---|---|
| First tries | Usually fails or gives a poor piece. Failures: iron overheated until it burns and sparks; worked too cold until it cracks or folds (a cold shut); a fire with too much air, so scale forms and a forge weld will not take; the anvil drawing the heat out of a small piece; thick stock not left to soak. [p] |
| Competence, mastery | Apprenticeship about seven years (5 to 7, some sources 5 to 10), the legal minimum for a trade after 1563 [q]. |
| Learnt | Taught, by a master in a shop; "becoming a blacksmith requires an apprenticeship" (Lancy) [r]. |
| Skill acts on | Quality and waste of metal and fuel. |
| Class | **Skilled.** |

### 2.15 Copper working: smelting and casting (engine: `smelt`, make 3, trade smelter; `copper tool`)

| | |
|---|---|
| First tries | Smelting often fails outright: experimental bowl furnaces were "largely unsuccessful" in early campaigns, so much so that it deterred further work; success depends on "the entire technological system, including fuel, furnace construction, air supply" [s]. Casting fails as a misrun (metal too cold or poured too slowly, the mould not filled), a cold shut (two streams that meet but do not fuse), porosity (gas from a damp or unvented mould) [s]. |
| Competence, mastery | As smithing (est.). |
| Learnt | Taught; held by specialists. |
| Skill acts on | Waste (ore and charcoal for nothing) and quality. |
| Class | **Skilled.** |

### 2.16 Tanning leather (no engine row)

| | |
|---|---|
| First tries | Fails often, and late. Failures: a liquor too weak or strengthened too slowly, so the hide rots and the hair slips; too strong at the start, so the surface tans and seals the centre raw ("case hardening", a risk "only in the beginning of tanning"); bark left in rain loses its tannin; hides not limed or scraped clean. [t] |
| Competence, mastery | A Bridgwater tanner's apprentice in 1424 was bound for **ten years**; a hide took months in the pits, up to 12 to 18 months or two years for sole leather [t]. Few tries a life, each slow. |
| Learnt | Taught by a tanner. [t] |
| Skill acts on | Waste (hides lost) and quality. |
| Class | **Skilled.** |

### 2.17 Making a bow (no engine row)

| | |
|---|---|
| First tries | A first bow often breaks or takes a set (follows the string) while it is tillered; a back that cuts through the growth ring splits; a stave too stiff to string. Bowyers advise a forgiving first stave and a sawn or turned board over a chased ring; "more bows survive once braced than fail" at the later stages. "A painful process of trial and error as no two pieces of wood are identical." Yew staves dry one to two years first. [u] |
| Competence, mastery | A modern three-year apprenticeship, "the only formal qualification in longbow making"; weaker sources give 4 to 7 [u]. Tsimane learn bow and arrow making by adolescence; proficiency at high-skill crafts (boats, pots) peaks in mid to late adulthood (Schniter et al. 2015) [v]. |
| Learnt | Self-taught or apprenticed for a war bow; in the household for a hunting bow. [u, v] |
| Skill acts on | Waste (staves broken) and quality (draw weight, life). |
| Class | **Practised** for a hunting self-bow (ash, hazel, elm); a yew war bow would be skilled. |

### 2.18 Plough farming (engine: `plough`, work 1, trade farmer; `wooden plough`, make, carpenter)

| | |
|---|---|
| First tries | A ploughman's first furrows wander and leave balks unturned, the share is set too deep and the oxen stall or too shallow and skids; the team is driven too hard. A ploughman had to train his oxen before he could rely on them [w]. Medieval furrows were not straight but curved (the long turn of an ox team) [w]. |
| Competence, mastery | The Seneschaucy (about 1270) asks ploughmen to be men of intelligence who can sow, mend ploughs and harrows, till well, and yoke and drive the oxen without hurting them (paraphrased from Lamond's 1890 translation; not reread this session) [x]. Servants in husbandry were bound to 21 under the 1563 statute [q]. One man and two bullocks plough about a quarter hectare a day (Ethiopia, anecdotal) [w]. |
| Learnt | Boys drove the team for the ploughman before holding the plough (est., the "fugator"); household and manor. [w, x] |
| Skill acts on | Yield (area a day; ground turned well, so the crop), little waste. |
| Class | **Practised.** |

---

## 3. The classes

| Class | What marks it in the sources | Crafts |
|---|---|---|
| **Simple** | Works crudely the first time; one rule to keep; competence in hours to days; learnt by watching in the household; skill mostly speed or yield, small range | setting snares, twisting cord, fishing with a line, salting, butchering and skinning, the quern |
| **Practised** | First tries often fail or give a poor thing; several steps and a judgment (tension, heat, siting); a season to a few years to reliability; learnt in the household or from a maker by watching and trying; skill wide in speed or waste | wicker traps and baskets, netting, hurdles and weirs, smoking, spinning flax, oven baking, charcoal, a hunting bow, ploughing |
| **Skilled** | First tries usually fail outright; long cycles (a smelt, a tan) and hidden states (heat, liquor strength) the beginner cannot read; five to ten years of apprenticeship; taught by a specialist; skill wide in quality and waste | smithing iron, copper smelting and casting, tanning (and a yew war bow) |

---

## 4. Parameters proposed

**As built** (`TRY`, `SKILL` in `cybertron2/engine/data.py`; `knowledge.tried`): `aware` cannot try (but 10 rows marked `untaught:
tryable`); rough uses 1.7 times the materials and works half the time, capable 1.3 and three in four, known 1.0 and always; a
level rises at a score of 2 (a success 1, a failure 0.5); skill rises as 1 - e^(-p / 50) on all work, between 0.5 and 2.0 for a
trade, 1.0 and 1.5 for a basic craft. A failed `make` loses its inputs.

**Proposed, by class** (first values, calibrate):

| | Simple | Practised | Skilled |
|---|---|---|---|
| Chance at **aware** (may try) | 0.6 | 0.35 | 0.15 |
| Chance at **rough** | 0.8 | 0.55 | 0.35 |
| Chance at **capable** | 0.95 | 0.8 | 0.65 |
| Chance at **known** | 1.0 | 1.0 | 1.0 |
| Materials at aware / rough / capable / known | 1.3 / 1.15 / 1.05 / 1.0 | 1.8 / 1.5 / 1.2 / 1.0 | 2.0 / 1.8 / 1.4 / 1.0 |
| **Materials per good result** (materials / chance) at aware / rough / capable | 2.2 / 1.4 / 1.1 | 5.1 / 2.7 / 1.5 | 13 / 5.1 / 2.2 |
| A failure's score toward the next level | 1 at aware, 0.5 above | 1 at aware, 0.5 above | 1 at aware, 0.5 above |
| Score to rise aware to rough | 1 (one try) | 2 | 3 (or three sightings, as now) |
| Score to rise rough to capable | 2 | 3 | 4 |
| Score to rise capable to known | 2 | 4 | **not by practice**: a lesson (`teach`) from someone who knows it |
| Tries to capable from aware (expected) | about 3 | about 6 | about 9 |
| Skill curve: tau, units of the craft at lifespan 96, scaled with lifespan | 10 | 25 | 50 |
| Units to master (85% of the way, 1.9 tau) | about 20 | about 50 | about 95 |
| Skill range (novice to master, on what the craft's skill acts on) | 0.8 to 1.3 | 0.6 to 1.6 | 0.5 to 2.0 |
| Practice alone takes skill to | the top | the top | **half the way ("skilled" word)**; beyond it only while taught or working beside a master (as the hunt's lead, `lead_hard`) |

**Why these numbers.**

- *Aware may try in every class* (Zach: forgiving for "the minimal / awareness"), but a skilled craft tried from hearsay wastes
  about 13 times the materials for a good result: tried, it teaches (each failure a lesson, §5), but it does not pay.
- *Simple*: Meriam fishing (no age effect), the one-day snare or cord: three in five at the first try, near certain once shown,
  little waste. Mastery in about 20 units of the craft: a few real years at the life mapping (§1) for a warrener's eye.
- *Practised*: a first basket "wonky", half a hurdle a day; one in three at hearsay, one in two with a rough idea; capable after
  about six tries, known after about ten (10 to 30 units at 1 to 3 units a try): one to three real years at the mapping, the
  household's way of learning. The skill range 0.6 to 1.6 covers netting and hurdles (a five times speed range between a
  first-day novice and an old maker, compressed because the novice soon leaves the bottom) and charcoal (1.5 times).
- *Skilled*: five to ten years of apprenticeship is about 20 to 35 units of the craft at lifespan 96 (§1): practice reaches
  capable in about 9 tries (about 27 units at 3 units a try), then a master's lessons are needed for known and for the top half
  of the skill curve, which is what made an apprentice worth binding for seven years and the master worth paying. The current tau
  50 is kept for this class.
- *Tau scaled with lifespan*: at lifespan 32 (the default) the same crafts take a third of the units; this is how `practice_x`
  already scales the hunt ([[D2-153 The lifespan is a world setting that scales every part of a life|D2-153]], brief 4c §3.3).

**Per craft, a field for what the skill acts on:** `yield` (gives more: snares, line, quern, netting, hurdles, charcoal, plough,
spinning), `waste` (the inputs a good result takes: salting, smoking, butchering, baking, tanning), or `quality` (the thing made
wears slower or works better: traps, bows, smith's work). The skill multiplier then lands on the one that matters for that craft.

**A three-way outcome is worth considering** (an option, not part of the class table): for the simple and practised classes, part
of the draw that now fails could instead give a crude result (a share of the yield, or a thing of a lower grade where the engine
has grades) with a lesson, matching "usually works crudely". A failure would then mean the batch is lost, and a crude result
that it was got badly.

---

## 5. Failure lines

**How a failure picks its line.** Each craft carries an ordered list of lessons (an input, a step, a place, a season). A failure
first looks for a cause the state really holds (the season out, the wood wet, an input short, the tide or weather wrong): if one
holds, it reports that. Otherwise it reports the first lesson on the list the person has not yet been given, marks it given, and
the next failure reports the next one; once all are given, it says that the skill is the shortfall ("you did it as you knew how;
your hands are not yet sure of it"). So the more one fails, the more one has learnt, and no line claims a state cause that is
false (the senses guide: grounded in state, worth acting on). A line given is written to the person's knowledge of the craft (a
"lesson" note), so explanation and teaching can pass it on. Lines below are drafts in the agents' register.

| Craft | Lines (each teaches one thing) |
|---|---|
| Snares | "The noose hung too high: a rabbit ran under it. Set it a hand above the ground." (step) / "It was set where they sit, not where they run: set it on the run between the marks of their feet." (place) / "Something knocked it aside and went on: set it a little further along the run." (step) |
| Cord | "It came apart as you let go: twist each strand one way and wrap them the other." (step) / "It broke at a thin place: keep the strands the same thickness, and overlap a new length well before the old one ends." (step) / "The fibre was brittle and short: bast from stems retted and dried, or bark cut in early summer, makes cord." (input, season) |
| Wicker trap or basket | "The withies cracked at the bend: they were dry. Soak them, or cut them in winter and weave them green." (input, season) / "The base came out lopsided: lay the stakes butt to tip, turn and turn about." (step) / "The throat was too wide: an eel went in and out again. Close the cone to a finger's width." (step) |
| Netting | "The meshes came out all sizes: draw each knot down hard against the mesh stick." (step) / "A knot slipped and opened a hole: pull the knot tight before the next." (step) / "The twine frayed and parted: net from good cord, tightly twisted." (input) |
| Line fishing | "Nothing took the bait here: try the deep water under the bank, at dusk or dawn." (place, hour) / "A fish took it and was gone: the hook was too large for the fish here." (input) / "The bait was gone each time you drew it in: bait with a worm threaded on the hook, not hung from it." (step) |
| Hurdle or weir | "The rods snapped at the end post: twist each rod as you turn it round the end." (step) / "The flood took the stakes: set the weir where the stream is broad and slow, and drive the stakes deeper." (place) / "The weave sags: the uprights are too far apart, a forearm apart at most." (step) |
| Smoking | "The fire flared and cooked the lowest fish: keep the fire smouldering, damp it with green wood or sawdust." (step) / "The fish are hard outside and soft within, and will not keep: you hurried it. Dry them first in a light smoke, then smoke them slow." (step) / "The fish were soft before they went up: smoke them the day they are caught and salted." (input) |
| Salting | "The flesh at the backbone has gone bad: there was too little salt, or it was not cut open enough for the salt to reach in." (input, step) / "The fish has turned red in the warm: keep the salted fish in the cool." (place, season) / "It went bad from the belly: gut and wash it clean before it is salted." (step) |
| Butchering, skinning | "You cut into the gut and the meat is tainted: cut shallow, lifting the skin away from the belly as you go." (step) / "The hide is cut through in places: skin with the blade turned to the hide, not into it." (step) / "The carcass has begun to spoil: open and cool it as soon as it is killed." (step, season) |
| Spinning flax | "The thread broke and the spindle dropped: you drew it too thin; let more fibre into the twist." (step) / "The fibre will not draw, it clings and tangles: wet your fingers, and dress the distaff, the fibre tied at the top and spread." (step) / "The yarn kinks back on itself: too much twist; draw out more before you let it run up." (step) |
| Quern | "The meal is coarse, half the grain is cracked only: feed the grain slower." (step) / "The meal is gritty: the stones are set too close. Raise the upper stone." (step) / "The grain is damp and clogs the stones: dry it first." (input) |
| Oven bread | "The loaves are burnt below and raw within: the floor was too hot. Rake out the fire and let the oven settle before you load it." (step) / "The loaves are pale and heavy: the oven was not fired long enough to hold its heat." (step) / "They burnt at the back: the oven has hot places; throw a pinch of flour on the floor and see where it scorches." (step) |
| Charcoal | "The clamp broke through and burnt to ash: cover it thick with earth and turf, and stop every hole that smokes." (step) / "Half of it is still wood (brands): the wood was wet, or you drew it too soon. Wait until the smoke runs thin and blue." (input, step) / "The wind fanned it overnight: build a screen of hurdles on the windward side, and watch the clamp through the night." (place, step) |
| Smithing | "The iron burnt and threw sparks: it was too hot, white. Take it out at bright orange." (step) / "It cracked under the hammer: you went on striking after the colour went. Put it back in the fire." (step) / "The weld would not take: there was scale on it; less air on the fire, and clean the faces." (step) |
| Copper | "The ore gave slag and no copper: the fire was not hot enough; it needs bellows and charcoal, not wood." (input, step) / "The casting did not fill the mould: the metal cooled; pour it hotter and quicker." (step) / "The casting is full of holes: the mould was damp. Dry it by the fire first." (input) |
| Tanning | "The hair slips and the hide stinks: the bark liquor was too weak. Add fresh bark, and strengthen it week by week." (input, step) / "The outside is leather and the middle raw: the first liquor was too strong. Start weak, and go stronger." (step) / "The bark gives little: it lay in the rain. Strip oak bark in spring and keep it dry." (input, season) |
| Bow | "The bow broke as you bent it: one place was bending more than the rest. Take wood off evenly, a little at a time, and bend it often." (step) / "The back split along the grain: you cut across the growth ring. Keep the back on one ring." (step) / "It has taken a bend and stays bent: the wood was green. Season the stave a winter first." (input, season) |
| Plough | "The oxen stalled: the share was set too deep. Raise it." (step) / "The furrow wandered and left strips unturned: keep your eye on a mark at the headland." (step) / "The clay stuck to the share and broke nothing: it was too wet; plough it when it crumbles in the hand." (season, place) |

---

## 6. What is estimate, and what is open

- **Estimates (mine):** the life mapping (55 real years to old age; 3 to 5 units of one's craft a life-year); every "(est.)" in
  §2 (first-try odds for each craft, competence times where no source gave one, a first clamp's yield, a beginner's knot rate,
  the line fishing and quern failure modes); all parameters in §4.
- **Sourced but weak:** blacksmith apprenticeship 5 to 10 years and children spinning from four or five (popular sites); longbow
  apprenticeship 4 to 7 (weak pages; the modern three-year figure is from a guild source); the 89 in 100 snare catch (one forum
  post); oven temperatures (oven sellers and forums).
- **Strongest sources:** FAO on charcoal yields and skill [o] and on smoking-kiln faults [h]; Gurven et al. 2006 and Koster et al.
  2020 on hunting skill [y]; Bird and Bliege Bird 2002 on Meriam fishing [e]; the Statute of Artificers [q]; the Bridgwater 1424
  indenture [t]; Stout 2002 on adze-making apprenticeship [r]; the Fergus estuary weir tree rings [g]; the saddle and rotary quern
  experiment [m]; Schniter et al. 2015 on Tsimane skill ontogeny [v].
- **Not reached:** no source gave a collier's training or a ploughboy's years; the Seneschaucy line is from memory of Lamond's
  translation and should be checked; Pargeter et al.'s 90-hour knapping training study (26 novices, gains "to an extent" in
  quality; teaching mattered more for the handaxe than for flaking) [r] supports a skilled class stalling without teaching, but
  its full result was not read.
- **For the design:** whether `aware` may try every craft (the classes say yes, at a cost) or only `untaught: tryable` rows;
  whether the class sets the skill range or each craft does; whether a crude result (§4) is wanted; where lesson notes live in
  `Mind.know`.

---

## 7. Sources

[a] Snares: Shooting UK, "How do I set rabbit snares on a known run?" https://www.shootinguk.co.uk/?p=11325 ; The Hunting Life,
"Professional rabbit snaring for amateurs" https://thehuntinglife.com/?p=34 and "Rabbit snaring" (Woodga)
https://thehuntinglife.com/html/sections/articles/ferreting_trapping/rabbit-snaring-snares.html ; GWCT, how to set a snare
https://gwct.org.uk/advisory/guides/fox-snaring-guidelines/how-to-set-a-snare/ ; bushcraftuk thread
https://bushcraftuk.com/community/threads/snaring-rabbits.164157/page-2

[b] Cord: Wilderness College, cordage https://www.wildernesscollege.com/cordage.html ; S. Edholm, leg-rolled cordage
https://steven-edholm.squarespace.com/blog/2014/01/12/about-leg-rolled-cordage-and-why-you-should-learn-it ; Primitive Ways,
cordage https://primitiveways.com/cordage.html

[c] Baskets and traps: Basketmakers' Association makers' pages https://basketmakersassociation.org.uk/?p=11864 ; Robin Wood
https://www.robin-wood.co.uk/?p=644 ; putcher fishing https://en.wikipedia.org/wiki/Putcher_fishing ; Museum Wales putcher
https://museum.wales/collections/online/object/75f88735-74ab-35bd-98f1-6929a403936a ; University of Reading MERL eel traps
https://reading.ac.uk/adlib/Details/collect/4761 ; Green 1992, The Severn Fisheries
https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-2776-1/dissemination/pdf/VOL_03_1992/Green_1992_The_Severn_Fisheries.pdf ;
beginner faults: Mother Earth News https://www.motherearthnews.com/diy/crafting/basket-making-zm0z22mazols/ , bushcraftuk
https://bushcraftuk.com/community/goto/post?id=1973487 , Joybilee Farm https://joybileefarm.com/?p=16511

[d] Netting: Workshop Receipts, "Netting" https://chestofbooks.com/crafts/mechanics/Workshop-Receipts-5/Netting-Part-3.html ;
Mother Earth News, net making https://www.motherearthnews.com/diy/net-making-zmaz83mjzraw/ ; NOAA leaflet 579
https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet579.pdf ; FAO Bay of Bengal net braiding
https://fao.org/docrep/pdf/007/ae118e/ae118e00.pdf ; fisher women's work https://wovencommunities.org/collection/the-herring-industry/

[e] Bird, D. W. and Bliege Bird, R. 2002, "Constraints of knowing or constraints of growing? Fishing and collecting by the
children of Mer", Human Nature 13 https://link.springer.com/doi/10.1007/s12110-002-1009-2 ;
https://pure.psu.edu/en/publications/constraints-of-knowing-or-constraints-of-growing-fishing-and-coll/

[f] Hurdles: Country Life https://countrylife.co.uk/gardens/traditional-fence-maker-turning-wattle-hurdles-nearly-25-years-172302 ;
Farmers Weekly https://www.fwi.co.uk/arable/orders-pour-in-for-traditional-hazel-hurdles ; Woodlands.co.uk
https://tom.woodlands.co.uk/?p=30672 ; Conservation Handbooks
https://www.conservationhandbooks.com/woodlands/green-woodworking/hurdles/ ; lowimpact.org https://lowimpact.org/categories/hurdles

[g] Weirs: CORDIS, fish weirs (Fergus estuary) https://cordis.europa.eu/article/id/150828-learning-more-about-fish-weirs and
https://cordis.europa.eu/docs/results/272490/final1-cca-publishable-summary.pdf ; phys.org on the Irish medieval weirs
https://phys.org/news/2011-02-irish-medieval-fishing-site-lost.html ; Nottinghamshire HER, Anglo-Saxon fish weir
https://her.nottinghamshire.gov.uk/Monument/MNT13022 ; Norfolk HER 52921 https://nhe.esdm.co.uk/Monument/MNF58112

[h] Smoking: FAO, traditional kilns https://www.fao.org/4/x5890e/x5890e01.htm and https://www.fao.org/4/x5953e/x5953e01.htm ;
Arbroath smokie https://en.wikipedia.org/wiki/Arbroath_smokie ; Borough Market
https://boroughmarket.org.uk/market-blog/what-it-takes-fish-smoking/

[i] Salting: ICAR, quality defects in cured fish
https://krishi.icar.gov.in/jspui/bitstream/123456789/83713/1/4.%20QUALITY%20DEFECTS%20IN%20CURED%20FISH%20PRODUCTS.pdf and
cured and dried fish https://krishi.icar.gov.in/jspui/bitstream/123456789/83224/1/10.%20Cured%20and%20dried%20fish%20products.pdf ;
Vikaspedia, spoilage of fish products
https://vikaspedia.in/agriculture/fisheries/post-harvest-and-marketing/processing-in-fisheries/spoilage-of-fish-products

[j] Herring girls: Lloyd's Register Foundation https://hec.lrfoundation.org.uk/whats-on/stories/strong-and-independent-women-in-the-19th-century-scottish-fishing-trade ;
ZME Science https://www.zmescience.com/feature-post/pieces/scotlands-herring-lassies-who-defied-gender-rules-and-built-an-industry

[k] Butchering: Outdoor Life, how to skin a deer https://www.outdoorlife.com/hunting/how-to-skin-a-deer/ ; hunter-ed.com
https://hunter-ed.com/blog/tips-and-tricks-for-field-dressing-a-deer/ ; American Hunter
https://www.americanhunter.org/content/how-to-field-dress-a-big-game-animal ; Mother Earth News
https://www.motherearthnews.com/sustainable-living/nature-and-environment/how-to-gut-and-skin-a-deer-zebz1308znsp/

[l] Spinning: Spin Off, drop spindle https://spinoffmagazine.com/about-drop-spindle-spinning/ and flax
https://spinoffmagazine.com/a-guide-to-spinning-flax-linen-spun-from-flax-fibers ; Knitty, spinning flax
https://knitty.com/ISSUEspring08/KSspinningflax.html ; Joy of Handspinning, flax https://joyofhandspinning.com/flax/ ;
childhood spinning (popular) https://historyrise.com/article/crafts-and-skills-taught-to-medieval-children/ and
https://ruthjohnston.com/AllThingsMedieval/?p=52 ; Penn State flax exhibit https://exhibitions.psu.edu/s/flax/item/4963

[m] Querns: the saddle and rotary quern experiment (16 volunteers; abstract via search)
https://searchworks.jioinstitute.edu.in/articles/asx__117268749 ; Mills Archive, "The first milling stones"
https://new.millsarchive.org/from-quern-to-computer-the-history-of-flour-milling/4

[n] Baking: Forno Bravo, bread and oven temperature https://www.fornobravo.com/blog/bread-baking-and-oven-temperature/ ; The
Fresh Loaf, wood-fired basics https://www.thefreshloaf.com/node/23589 ; Forno Bravo forum
https://community.fornobravo.com/forum/brick-oven-cooking/hearth-bread-and-flatbread/7923-i-suck ; World History Encyclopedia,
medieval trades https://www.worldhistory.org/Medieval_Trades/ ; German bakers' ordinance
https://germanhistorydocs.org/en/from-the-reformations-to-the-thirty-years-war-1500-1648/ghdi:document-3963 ; Coventry bakers
https://www.history.org.uk/files/download/29481/1737550350/The_Bakers_Company_of_Coventry_by_Phillip_Willcox.pdf

[o] Charcoal: FAO Forestry Paper 41, Simple technologies for charcoal making https://www.fao.org/4/X5328E/X5328E00.htm and
https://www.fao.org/4/X5328E/X5328E07.htm ; Booth, FAO https://www.fao.org/4/p2070E/p2070e08.htm ; Penn State, making charcoal
https://engr.psu.edu/MTAH/essays/making_charcoal.htm (fetch blocked; summary only) ; Wyre Forest
https://www.revolutionaryplayers.org.uk/?p=2368

[p] Smithing faults: iForgeIron, common beginner mistakes https://www.iforgeiron.com/topic/28858-common-beginner-mistakes/ and
https://www.iforgeiron.com/topic/5960-common-mistakes-that-beginners-make/ ; Grit, forge welding
https://www.grit.com/tools/hand-tools/starting-blacksmithing-forge-welding-techniques-zm0z23sozawar/

[q] Apprenticeship terms: Statute of Artificers https://en.wikipedia.org/wiki/Statute_of_Artificers_1562 and
https://britannica.com/topic/Statute-of-Artificers ; Encyclopedia Virginia, the 1563 act
https://encyclopediavirginia.org/primary-documents/an-acte-towching-dyvers-orders-for-artificers-laborers-servantes-of-husbandrye-and-apprentises-1563/ ;
Wallis, apprenticeship (LSE) https://www.lse.ac.uk/Economic-History/Assets/Documents/Research/FACTS/WorkingPapers/2007/2207Wallis.pdf ;
Medieval Sourcebook, apprentice contracts https://sourcebooks.web.fordham.edu/Halsall/source/1248apprentice-barber.asp ; Wareham
Forge https://warehamforge.ca/on-smith/apprentice.html ; Encyclopedia.com, apprenticeships
https://www.encyclopedia.com/history/news-wires-white-papers-and-books/training-children-work-apprenticeships

[r] Teaching and apprenticeship: Stout 2002, Langda adze makers, Current Anthropology 43(5)
https://www.journals.uchicago.edu/toc/ca/2002/43/5 ; Stout 2005 https://scholarblogs.emory.edu/stoutlab/files/2013/07/Stout-2005b.pdf ;
Science News, "The stone masters" https://www.sciencenews.org/article/stone-masters ; Pargeter, Khreisheh and Stout, handaxe
training https://par.nsf.gov/servlets/purl/10109965 ; EXARC report https://exarc.net/ark:/88735/10202 ; Lancy, learning without
lessons https://www.davidlancy.org/learning-without-lessons and the chore curriculum https://digitalcommons.usu.edu/sswa_facpubs/274

[s] Copper: EXARC, Chalcolithic copper experiment https://exarc.net/ark:/88735/10601 ; EXARC bowl furnaces
https://exarc.net/ark:/88735/10622 ; Moravian ores https://opac.geologie.ac.at/ais312/dokumente/Mitt_OEMinGes_156_115-128.pdf ;
Newcastle blowpipe furnace https://research.ncl.ac.uk/expeditionresearchscholarships/postergalleries/2018posters/Marco%20Pitone%20&%20Team.pdf ;
casting defects https://en.wikipedia.org/wiki/Casting_defect

[t] Tanning: Medievalists.net, making leather https://www.medievalists.net/2026/10/dirty-business-making-leather-middle-ages/ ;
Unusual Historicals, medieval tanning (Bridgwater 1424 indenture)
https://unusualhistoricals.blogspot.com/2016/11/odd-jobs-tanning-medieval-dirty-job.html ; NPS, tanning in the 17th century
https://www.nps.gov/jame/learn/historyculture/tanning-in-the-seventeenth-century.htm ; Herefordshire
https://htt.herefordshire.gov.uk/1197.aspx ; Edholm, bark tanning mistakes
https://steven-edholm.squarespace.com/blog/2013/04/14/the-most-common-bark-tanning-mistakes-pitfalls-to-avoid-on-your-way-to-beautiful-leather ;
Encyclopaedia Britannica 1810 https://jimclifford.ca/early_encyclopedia_britannica/articles/1810/eb_4th_1810_020179.html ;
Leather (Gutenberg) https://gutenberg.org/cache/epub/43377/pg43377-images.html

[u] Bows: Bow International, traditional bowmaking https://www.bow-international.com/?p=6053 ; Wikipedia, bowyer
https://en.wikipedia.org/wiki/Bowyer ; Wilderness Awareness, bowmaking basics https://wildernessawareness.org/articles/bowmaking-basics/ ;
Primitive Ways, tillering https://w.primitiveways.com/bow_tillering.html ; E. Myers, tips https://www.oocities.org/~emyers/bowyers/mytips.htm ;
Medieval Chronicles, bowyer https://www.medievalchronicles.com/medieval-people/medieval-tradesmen-and-merchants/medieval-bowyer-needs-images

[v] Schniter, Gurven, Kaplan, Wilcox and Hooper 2015, "Skill ontogeny among Tsimane forager-horticulturalists", AJPA 158
https://www.gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/schniteretal2015.pdf ;
https://www.pubmed.gov/25921880/

[w] Ploughing: Agecroft Hall, the plowman's burden https://www.agecrofthall.org/single-post/outdoor-work-the-plowman-s-burden
and training the team https://www.agecrofthall.org/single-post/outdoor-work-training-the-team ; Essex Field Club on medieval
furrows https://essexfieldclub.org.uk/archivetext.php/s/092/o/0014 ; Historic UK, ridge and furrow
https://www.historic-uk.com/HistoryUK/HistoryofEngland/Ridge-Furrow-Medieval-Field-System/ ; Botany One, learning bullock
ploughing in Ethiopia https://www.botany.one/bullock-ploughing-plowing-in-ethiopia/ ; Medievalists.net, children's work
https://www.medievalists.net/?p=83809

[x] Walter of Henley's Husbandry with the Seneschaucie, ed. and tr. E. Lamond, 1890
https://www.archive.org/download/walterofhenleysh00henluoft/walterofhenleysh00henluoft.pdf ; Carlin on the Seneschaucy
https://sites.uwm.edu/carlin/?p=306

[y] Gurven, Kaplan and Gutierrez 2006, "How long does it take to become a proficient hunter?", J. Human Evolution 51
https://www.gurven.anth.ucsb.edu/sites/secure.lsit.ucsb.edu.anth.d7_gurven/files/sitefiles/papers/gurvenetal2006JHE.pdf ;
Koster et al. 2020, "The life history of human foraging", Science Advances 6(26) https://pmc.ncbi.nlm.nih.gov/articles/PMC7314517
