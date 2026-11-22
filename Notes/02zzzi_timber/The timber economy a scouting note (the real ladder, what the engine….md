---
id: docs/review/37_growth/02zzzi_timber/scouting.md
kind: note
updated: "2026-11-22"
---
# The timber economy: a scouting note (the real ladder, what the engine holds, where the leverage is)

*note · `docs/review/37_growth/02zzzi_timber/scouting.md`*


Session 37.2, thread [[W-76 The timber economy|W-76]] (the timber economy: felling, coppice and standards, seasoning, sawing, carpentry and building as a trade,
carting, and the woods it draws on), 22 Nov 2026. Scouting only. Nothing here is decided, no code was changed, nothing was run. Zach
chose timber as the next economy after the fishing, hunting and materials wave ([[W-73 Fishing, hunting and their materials developed together|W-73]]). This note is groundwork for its own design wave.

**Marks.** **(sec.)**: seen only in a search engine's summary of the page, not on the page itself. This session could fetch no page
(Wikipedia, buildingconservation.com, the UWE timber-framing pages, Peter Follansbee's pit-sawing posts and cdn.odi.org were all
outside the session's allowed network), so **every web figure here is (sec.)**. Check each against its page before it goes into data.
**(m)**: a standard figure from memory or an earlier note, not re-checked this session. **(est.)**: my estimate from the figures
given, with the working shown.

**Engine basis** (as the earlier notes use it): a unit of work is 2 hours ([[D2-275 A unit of work is 2 hours|D2-275]]); 7, 6 and 5 units a day by season; a world year
is 32 days, seasons of 8 ([[D2-209 Brief 5 (river and water) is built|D2-209]]); making capital costs real hours times about 1/7, materials stay real in quantity and rate ([[D2-276 Making durable things runs on the year clock|D2-276]],
staged through about 1/15, [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]); a unit of size is about 2 ha; **a timber is about 240 kg of wood**, firewood about 60 kg
(02z_forest_model.py). Green oak weighs about 1,000 to 1,060 kg a m³ and seasoned oak about 860 to 930 (an old carpentry text's 62.5
to 66 lb a ft³ green, 53.5 to 58 seasoned; sec.), so **a timber is about 0.23 m³ of green oak: about 8 ft³, a log about 30 cm across
and 3.3 m long** (est.). A medieval "load" of timber was 50 ft³ (m), about six timbers.

Read first: docs/cybertron2/proposals/building_clock.md ([[D2-276 Making durable things runs on the year clock|D2-276]]; builders as a trade); docs/review/37_growth/02zzzh_hunt_fish/
withies_wood_materials.md (withies, coppice, poles, bark), building_clock.md (the audit), storage.md §11 (room costs in kind),
household_skills.md (the carpenter, woodsman and builder livelihoods); 02zzj_economy_research/03_crafts_woods_metal_building.md §1, §4,
§6 (woods, building, tanning); 02z_forest_model.py and 02zb (the forest package, [[D2-156 A forest is three stocks|D2-156]] to [[D2-161 Seed nodes below what they sustain|D2-161]]).

## 0. In brief

- **The real ladder is short in tools and long in time.** An axe, an adze, wedges and a beetle, an auger, later a pit saw: that is
  the whole kit. What is long is time: standards grown for 50 to 100 years, underwood for 5 to 30, bark only six weeks of spring,
  timber best felled in winter, boards seasoned a year an inch, and the frame worked green the season it was felled.
- **The woods were the most contested land in the manor**: the holder's timber and game, the commoners' firewood, browse and
  pannage, the collier's and the tanner's underwood, the deer. Restraint was a fence and a calendar enforced by a woodward and a court.
- **The engine already has the woods' bones** (three stocks, [[D2-156 A forest is three stocks|D2-156]]; rights, [[D2-158 Default rights in woods|D2-158]]; a carpenter's trade on medium rooms and halls;
  skill cutting the units of building) **but none of the conversion**: timber is one good from felling to frame, light as a sack
  (weight 2, so a person carries 1.2 t of oak), charcoal is burned from standing trees rather than underwood, poles are firewood,
  there are no boards, no seasoning, no saw, no carriage problem, no bark, no woodward, and no building is better for its builder.
- **Where the leverage is:** standing trees (the holder), carriage (whoever has oxen, a cart and a track), the master carpenter
  (often one in a valley), the raising (a frame needs many hands on one day), the smith's tools and the smith's charcoal (from the
  same coppice), the spring bark (the tanner against the builder's winter felling), and great timber (a mill shaft, a boat's keel, a
  hall's tie-beam: rare, slow, held).
- **A candidate scope** (§4) in five feature units: timber in kilograms and its carriage; the woods' products by kind (standards,
  poles, cordwood, bark); conversion (cleave, hew, saw) to a small set of goods; builders as a trade with soundness and the raising;
  rights and the woodward. Fifteen questions for Zach, each standing alone, close the note.

## 1. The real ladder, early to high medieval northern Europe

### 1.1 Woodland kinds and how they were managed

| Kind | What it is | What it gives | Who holds and uses it | Notes |
|---|---|---|---|---|
| **Wildwood, high forest** | unmanaged or lightly used woods of big trees | great timber (keels, mill shafts, tie-beams), mast, game, dead wood | lords, the king's forests, the commons on the edge | already scarce in lowland England by Domesday: about **15%** of the land recorded was woodland or wood pasture, in 6,208 of 12,580 settlements (Rackham, via Herefordshire Through Time; sec.) |
| **Coppice** (underwood) | trees cut to the stool on a rotation; shoots regrow | rods, poles, stakes, faggots, cordwood for charcoal and kilns, bark (oak) | the holder; cut by woodsmen, hurdle-makers, colliers, sold by the acre | must be fenced (bank, ditch, hedge) against beasts and deer for its first years after each cut (03_crafts §1.4; m) |
| **Coppice with standards** | coppice with timber trees left standing among it | both: underwood every few years, timber every few cycles | the lowland medieval wood's form | a statute of 1543 required at least **12 standards an acre** (30 a ha) left at each fell (sec.); a modern range of about 30 large and up to 150 young standards a ha (sec.); the overstorey cycle a multiple of the coppice cycle (Teagasc paper; sec.) |
| **Pollards** | trees cut 2 to 4 m up, above the beasts' reach | poles and leaf fodder (ash, elm, willow, hornbeam, oak) | wood pasture, parks, hedges, river banks | fodder pollards cut every **2 to 6 years**, wood pollards every **8 to 15** (sec.); pollarding belongs to grazed land, coppice to fenced wood (sec.) |
| **Wood pasture** | grazed land with scattered trees (commons, parks, chases, forests) | grazing and browse, pannage, pollard wood, some timber | commoners and the lord together | palatable trees (ash, elm, hazel) decline under grazing; oak, beech, hornbeam survive (sec.); Domesday measures much wood by the swine it fed ("wood for 2,000 swine" at Harrow; sec.) |
| **Hedges and hedgerow trees** | living hedges, laid, with timber trees in them | haybote (fencing wood), poles, some timber | the holder of the land | m |

**How the ladder moved.** Early medieval (c. 500 to 1000): much wood, used extensively; earth-fast posts and split planks; woods
mostly wood pasture and common, coppice known (it is prehistoric). High medieval (c. 1000 to 1300): population and cultivation peak,
woods shrink and are enclosed, coppice-with-standards is the managed norm in the lowlands, woods are valued by acre and cycle, and
royal forest law covers a large share of the country (Langton and Jones put the royal forests at their greatest at over a quarter of
England; sec.). After 1348 labour is dear and land is let go to wood and pasture again (m).

### 1.2 Rotations and yields

| | Rotation | Yield | Source |
|---|---|---|---|
| hazel coppice | **7 to 10 years**; Hayley Wood (Cambs) cut on a **7-year cycle** in the Middle Ages | about 10,000 rods an acre at the cut (25,000 to 30,000 a ha at 8 to 9 years) | Rackham via RFS; Durham 1956 via Forest Research (sec.; withies note §1.3) |
| mixed underwood (ash, oak, lime, alder, chestnut) | **5 to 30 years** (generally 10 to 30; as often as yearly for willow) | **about 2.5 t a ha a year dry** wood to 5 cm (6 t for poplar and willow) | conservation handbooks; Forest Research (sec.) |
| oak bark coppice | 20 to 30 years (bark from oak under about 40 years, the inner bark richest) | no clean figure; one modern peeler 3 to 6 t of bark a year (sec.) | Edlin 1973 via Forest Research (sec.) |
| standards (timber oaks) | felled **before 60 or 70 years** of age, on a cycle of about 60 | a standard's few cubic metres each cycle (est.) | sec. |
| a wood kept for charcoal | about **1 t an acre a year** of charcoal-making wood in a well-managed wood (about 2.5 t a ha) | | Franklin, ancient oak coppice (sec.) |
| labour | about **300 acres of managed coppice** kept one person in full-time work (Franklin; sec.), so a coppice-worker cuts an acre or two a year's worth of cycle (est.: unclear what the 300 acres counts) | | sec. |

**What a building takes from a wood.** Medieval building used ordinary standards, small and young, not giants: Rackham's study of
Grundle House at Stanton (Suffolk; late 15th century, a hall and two cross-wings) found its frame built of many small oaks, by his
figure about 330 trees (m; the Suffolk HER confirms the 1972 article on "the quantities of timber in certain East Anglian buildings
in relation to local supplies", not the count; sec.). Rackham counted the Barley Barn at Cressing Temple (felled 1205 to 1235) as
about **600 timbers from 480 mostly quite small oaks** (sec.). Great timbers were the scarce ones, moved far or bought abroad.

**On the engine's basis** (est.): a cottage frame of 3 to 5 m³ is 12 to 20 timber (storage.md §11); a hall-house of the Bayleaf kind
perhaps 20 to 40 m³, about 85 to 170 timber; an aisled barn several hundred trees. A managed wood's standards at 12 an acre give
perhaps one cottage's oaks from 2 to 4 acres at each fell (est.).

### 1.3 Felling

- **Tools:** the felling axe (iron in the medieval north; bronze about as good as steel in replica tests, stone 2 to 4.5 times slower
  than steel, about 75 more strokes a tree: Penn Museum, Putz; sec.); the two-man cross-cut saw for felling is early modern (m).
- **Rate:** no measured medieval figure found. A modern skilled axeman fells a 50 cm tree in about 8 minutes with a double-bit axe;
  a beginner took about an hour (forum reports; sec.). With snedding (limbing) and cross-cutting into lengths with the axe, a small
  oak of 30 to 40 cm (one to two timbers of usable trunk) is about **1.5 to 3 hours** for a skilled man with an iron axe (est.), so
  **about 0.3 to 1 timber an hour in the round** (75 to 240 kg an hour; est.). The audit's 55 to 110 kg an hour (building_clock.md
  §1.2) includes stacking and is the low end.
- **Seasons:** timber oak was best felled in **winter**, sap down: it dried more slowly and split less (sec.). Bark peels only in
  **spring** (late April to mid-June: Wyre Forest 24 April to 14 June; sec.), so oak for bark was felled in spring, or peeled
  standing in spring and felled the next winter, an old practice "meant to get both the bark and the timber" (an 1820 Royal Society
  paper; sec.). Underwood was cut in the dormant season, October to March (m).
- **The brash:** branches and tops went to faggots, firewood and charcoal (the engine already leaves brash as dead wood, [[D2-156 A forest is three stocks|D2-156]]).

### 1.4 Conversion: cleaving, hewing, sawing

| Method | What it gives | When it dominated | Real hours | Notes |
|---|---|---|---|---|
| **cleaving (riving)** with wedges, a beetle (maul), a froe | radially split planks, posts, boards, laths, shingles, pales, staves | early medieval: "on medieval sites radially split timbers predominate"; cleft structural timbers "extremely rare" in buildings after 1200 (Thompson, buildingconservation; sec.) | quartering a log under an hour; riven boards a few an hour (est.; no measure found) | straight-grained, knot-free oak only: a wildwood tree. Wainscot was riven oak boards from big, slow-grown forest trees, later imported from the Baltic (sec.). Clapboard is named for splitting (sec.) |
| **hewing** with felling axe and broad axe (and adze) | a squared beam: boxed heart (one beam a log), or halved, or quartered by sawing | throughout; "nearly all buildings with structural timbers have some visible hewn surfaces" (sec.) | **about 4 to 6 hours a 12-ft (3.7 m) beam**: an amateur's 4 hours with a pole axe; a professional's 25 hours a 50-ft beam, about 110,000 strokes (sec.) | boxed heart for posts, beams and purlins; halved for plates, joists and rafters (Historic England; sec.); a beam of a timber's log after hewing is perhaps 0.6 to 0.7 of it (est.) |
| **sawing**: first trestle "see-sawing", then the **saw pit** (top sawyer on the log, bottom sawyer in the pit) | boards, planks, halved and quartered scantlings | sawing from about the end of the 12th century; the pit saw adopted gradually from the end of the 14th to the mid-16th (UWE; sec.) | **about 12 boards a day for a pair** (sec.); paid by the hundred feet run, oak the dearest ("Sawing by the hundred not above 4s 6d for boards", a price list; sec.) | a pair of sawyers is a trade of its own; boards about 1.7 person-hours each (est.: 20 hours for 12); a timber's log gives about 8 to 10 boards of 25 mm (est.), so about **15 person-hours a timber to boards** (est.) |
| **water-powered saws** | boards | Villard de Honnecourt's drawing c. 1230 (m); a mill saw "up to 200 boards a day" against a pit's 12 (sec.) | | later than this note's ladder in the north; a mill-holder's chokepoint if ever taken in |

**Order of the switch:** split and hewn (axe and wedge) to hewn and sawn (the saw). The saw made boards from crooked or knotty oak
that would not cleave, so it widened which trees were good; cleaving needs the best trees. That is a quality ladder in the wood, not
only in the tool.

### 1.5 Seasoning: green against seasoned

- **Frames were worked green.** Medieval carpenters had "a decided preference for working with freshly felled green timber" (Miles
  2014, via Triskele; sec.); green oak is much easier to cut and joint, and air-seasoning timbers of frame section was impractical
  (UWE; sec.). Builders "usually obtained all the wood needed for a given structure by felling the necessary trees in a single
  operation from one patch of woodland" (sec.). A Tower of London truss felled 1538 to 1539 was used very soon after (sec.). A frame
  might stand a year uncladded to settle before infill (sec.).
- **Seasoned wood was for joinery and goods:** boards for chests and doors, panelling, barrel staves, wheel hubs and spokes, tool
  handles, bows. Oak air-dries at about **a year an inch** (25 mm) of thickness (a timber merchant's rule; sec.); green oak is 60 to
  80% moisture (sec.). Wheelwrights kept elm, oak and ash for years (m).
- **On the year clock** ([[D2-273 Three clocks, each system on one|D2-273]]): a real year's drying is a world year (32 days): an inch board seasons in a world year, a 2-inch
  plank in two (est.). Frames take no waiting at all.

### 1.6 Carriage

- **Weight is the fact:** a timber (0.23 m³ green oak) is about 240 kg; a cottage's frame 3 to 5 t; a hall's 20 to 40 t (est.). On
  the back a person carries about 25 to 30 kg ([[W-71 How carrying works in the live runs|W-71]]'s measured pack basket load): a timber is eight to ten loads, or four to six
  people carrying a log on poles a short way (est.).
- **Dragging and sledges:** logs were snaked out by oxen or horses on chains; sledges in winter on frozen or wet ground carry far
  more than wheels (a 19th-century logging sled up to about 7 t; sec., American, not medieval).
- **Carts:** two-wheeled carts and wagons drawn by oxen or horses; ox carts "could carry only a few tons" (sec., general); a
  medieval two-wheeled cart perhaps 0.5 to 1 t, two to four timbers (est.). The engine's transport spec plans an ox cart at 300 to
  400 weight (transport.md; later).
- **By water:** timber travelled by river and sea wherever it could. Dendrochronology shows logs floated from distant inland woods
  to 9th-century Dorestad and Wolin (Ważny; sec.); the Baltic board trade (wainscot, sawn pine) is well documented by the 13th to
  14th centuries (sec.); the great Rhine rafts (200 to 400 m, thousands of logs) are early modern (sec.). **Green oak, at about its
  own weight in water, barely floats** (est. from the densities above): rafts were mainly softwood, or oak lashed to lighter wood or
  carried in boats (m).
- **Cost:** "much of any building's cost was carriage" (03_crafts §4.3; m); prefabrication at a framing place near the wood cut the
  weight carried, since the frame left its offcuts behind (m).

### 1.7 Carpentry: framing a cottage, a barn, a hall

- **Structure over time:** earth-fast posts (rot at the foot; rebuilt every generation or two) until about 1200; posts on stone
  pads from about 1210 (a Cheddar building), then sills on low plinth walls (UWE; sec.); lap joints, then pegged mortise and tenon,
  scarf joints for long plates (Cressing's barns show the 13th-century change, sec.); crucks in the Midlands and the west; box frames
  in the east and south; the aisled barn. Infill wattle and daub, later boards or brick; roofs thatch, shingles (cleft oak), tiles.
- **Prefabrication:** the frame was laid out and cut at a framing yard, marked with carpenters' numerals, carried and **raised in a
  day by a crew** (m: neighbours and hired labour; the raising is the one step that needs many hands at once).
- **Hours:** no carpenter-day count for a medieval house was found. Dyer's survey of carpenters (1200 to 1540): jobs from mending a
  door for a few shillings to "a small house or a parish church roof for £5 or £10" (sec.); more than 10,000 carpenters at work
  about 1380 (poll taxes; sec.); a carpenter's day wage about 3 to 4d before 1348 and 5 to 6d after (m). If half of a £5 small house
  was carpenters' wages at 4 to 6d, it is about 100 to 150 carpenter-days (est.). The Sidbury (Devon) accounts of 1461 cost a whole
  village house, cob walls with jointed timber, possibly three bays (sec.; the figures not seen). A modern frame has several hundred
  joints (sec.).
- **Estimates for the engine** (est.; the building_clock audit's ranges where it has them):

| Building | Timber | Real carpenter hours (frame, est.) | Crew to raise | At 1/7 (units) | Engine now |
|---|---|---|---|---|---|
| cottage, one or two bays (a small timber room) | 12 to 20 | 300 to 700 | 6 to 10 for a day | 21 to 50 | small room, timber: 8 timber, 2 stone, 6 units, no trade |
| a two- or three-bay house (a medium room) | 25 to 45 | 700 to 1,500 | 8 to 12 | 50 to 107 | 15 timber, 4 stone, 15 units, carpenter |
| a hall-house or lord's hall | 85 to 170 | 1,500 to 4,000 | 15 to 25 | 107 to 285 | hall, timber: 80 timber, 20 stone, 200 units, carpenter |
| an aisled barn | several hundred trees | 3,000 to 8,000 | 20 or more | 214 to 570 | no barn |
| a water wheel and leat | 60 | 1,440 to 4,680 (the audit) | | 103 to 334 | 60 timber, 20 stone, 2 copper, 250 units, carpenter |
| a clinker boat: the Sea Stallion (a 30 m warship) | 14 oaks for planks, 4 for keel and stems, 2 for keelson and mast step, 250 crooks | **27,000 hours** for the hull (Viking Ship Museum; about 40,000 with tar, iron, rope and sail; sec.) | | about 1,900 | no boats |

- **The skill gap is real and large.** A master carpenter lays out, a journeyman cuts, a labourer hews and carries; a household
  without one can raise posts and wattle but not a jointed frame. English journeymen came to earn about two-thirds of a master's
  wage by the 15th century (sec.). Sons learned from fathers; formal indentures are rare before 1500; "celebrity" carpenters
  designed and supervised and "did not wield an axe" (Dyer; sec.).

### 1.8 Charcoal

- Charcoal was burned from **underwood** (cordwood from coppice, about 5 to 15 cm), not timber trees: the collier stacked billets
  round a central flue, covered them with turf and earth, and watched the burn for **2 to 10 days** and nights, then let it cool for
  days (sec.). A skilled collier got up to about **25% charcoal by weight** (sec.); archaeometallurgists use about 8 kg of wood a kg
  (03_crafts §1.2; m). Charcoal is light, so it travels where wood cannot: the smith, the salter (Wyre Forest charcoal for the
  Droitwich brine pans from the 12th or 13th century; sec.), later the iron works.
- The smith's charcoal and the smith's axe close a loop: **no charcoal, no iron tools; no tools, no felling** (m).

### 1.9 Bark (the tanning link, [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]])

- [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] brings tanning into the current build, with **bark as a new good**. Its supply is the timber economy's: oak bark from coppice
  under about 40 years, or from oaks felled in spring; peeled **late April to mid-June** with a slit and a peeling iron, then
  stacked to dry (sec.). Bark is perhaps 10 to 15% of a small oak pole's mass (est., withies note §1.4).
- **The clash:** bark wants spring felling; timber wants winter felling. Either the tanner gets spring-felled oak (worse timber), or
  the oaks are peeled standing in spring and felled the next winter (both, at a year's delay), or bark comes from coppice poles (the
  collier's and hurdle-maker's wood). Tanning and iron competed for the same oak coppice (03_crafts §6.2; m).
- How much bark a hide takes was not found (to source before data).

### 1.10 The trades

| Trade | Work | Capital | Where it lived | Notes |
|---|---|---|---|---|
| **woodward** (wood-reeve) | keeps the lord's woods: allots and marks the cut, guards against theft and beasts, presents offenders at the manor court | none of his own; an office | an ancient manorial office (the Froyle woodward "a most important officer"; sec.) | an Earls Colne woodward was himself accused of cutting three cartloads from the demesne park (sec.): the office is a lever both ways |
| **woodsman, hurdle-maker** | cuts coppice by the acre (bought standing), makes hurdles, stakes, faggots | a hook and a bill | the wood, in winter | buys the cut of an acre: a market in standing underwood (m) |
| **collier** (charcoal burner) | burns charcoal | the hearth in the wood, a hut | lives in the wood for the burning season | a margin trade; full-time only where a smith or salter buys (household_skills.md addendum) |
| **sawyer** (a pair) | pit sawing boards and scantling | the saw (iron, dear), the pit | itinerant or on a big job | paid by the hundred feet (sec.) |
| **carpenter** | frames, roofs, floors, doors, mills | axes, adze, augers, chisels, a framing yard | village, town and forest; travelled for big jobs (Dyer's 158 cases; sec.) | more than 10,000 about 1380 (sec.) |
| **wright** (wheelwright, cartwright, millwright, shipwright) | wheels, carts, ploughs, mill gear, boats | seasoned stock (years), a shop | village and town | the word for any worker in wood; the shipwright and millwright are the great-timber trades (m) |
| **cooper, turner, joiner** | barrels and buckets; bowls and handles; joined chests, panelling (late medieval joiners split from carpenters in towns) | seasoned staves and boards | towns, some villages | m |
| **carter** | carriage of timber, stone, goods | oxen or horses, a cart, harness | the holder of beasts | carriage is a large share of any building's cost (m) |
| **tanner** | bark tanning | pits, hides, bark | by water, downstream | [[D2-270 Household skills|D2-270]], [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] |

### 1.11 Who controlled the woods

- **The holder owned the trees** (timber, and the right to sell the underwood); **tenants held allowances** ("botes", collectively
  **estovers**): **housebote** (wood to build and repair houses on the manor), **haybote** (thorns and underwood for hays and fences),
  **firebote**, **ploughbote** (Lancaster manorial glossary; Hampshire Field Club; on record from c. 1170; sec.). Commoners had
  pannage, grazing and dead wood. Over-cutting under a bote, or cutting standards, was a court matter.
- **Royal forest law** (vert and venison) put the king's deer and their cover above everyone's use in the forests, with its own
  courts and officers (m).
- **The calendar and the fence** were the rules: panels cut by year, fenced after the cut, beasts kept out for several years,
  standards left at each fell.
- **Regional differences.** Scandinavia, Finland, the Baltic and Russia built in **horizontal logs** (laft) of pine and spruce, the
  commonest technique there (cross-timbering in Norway by about 1000; Oslo houses all log-built with cogged joints, Sørheim; sec.),
  with stave building for churches; western and deciduous Europe framed (sec.); German half-timbering (Fachwerk) spreads from the
  14th century (sec.). Log building takes many more trees but little jointing skill and no saw; framing takes few trees and a
  carpenter. Mediterranean Europe built in stone and imported timber (m). The **ship** was the north's largest single sink of big
  oak (Skuldelev 2: about 20 large oaks and 250 crooks; sec.).

## 2. What the engine has now, and what it lacks

### 2.1 What it has

| Area | What is there | Where |
|---|---|---|
| **goods** | `timber` (weight 2, heat 2), `firewood` (weight 1, heat 0.5), `charcoal` (weight 2, heat 6); no boards, poles, bark, seasoned wood | `cybertron2/engine/data.py:87`, `:44`, `:43` |
| **the woods** | three stocks a parcel: trees (`wood`, timber), young growth, dead wood ([[D2-156 A forest is three stocks|D2-156]]); kinds old forest (2,500 / 50 / 300 a unit of size), managed wood (600 / 400 / 100), copse, scrub; trees grow 0.5 to 1% a year, young growth 50 to 100%, brash 1 firewood a timber felled, under 40% of its trees a forest turns to scrub, gales throw trees | `data.py:204-220`; `engine/forests.py:17-115`; `engine/renewal.py:84-95`; spec `environment/resources.md` "Forests" |
| **the generator's coppice** | a village's own wood is always a managed wood, written "coppiced, hazel under oak standards" | `landgen/settle.py:523`; `landgen/write.py:176` |
| **felling** | `fell`: a forest, draws trees, 3 timber in 2 units (crude tool 1.0, copper 2.0, bare hands 0.25), wear 1, brash left | `data.py:421-423`; `engine/verbs.py:636`; spec `economy/production.md` "Wood" |
| **cutting and gathering** | `cut` (aliases "coppice", "cut poles"): young growth, 5 firewood a unit, a tool; `firewood`: dead wood by hand | `data.py:434-437`, `:424-427` |
| **charcoal** | 5 timber to 1 charcoal in 2 units at a forest, the woodsman's trade; smelting takes 1 charcoal or 4 timber | `data.py:655-656`, `:670-671` |
| **rights** | dead wood, and young growth on common land, anyone's; trees the holder's; felling another's is heard ([[D2-158 Default rights in woods|D2-158]]) | spec `world/holding.md:140-148`; `verbs.py:601` (`_against`) |
| **signs** | a wood thinned, bare, "the good straight trees are gone", "tall, straight timber standing", a gale's roar, axes heard; deer stripping coppice regrowth | `engine/signs.py:692-702`, `:964`; `wild/kinds.py:378` |
| **the carpenter's trade** | medium room, hall (timber), water wheel, handcart and plough carry `trade: carpenter`; a building's level is its blueprint's technique; the generator deals a carpenter by a managed wood | `data.py:262`, `:296-308`, `:589-590`, `:657-659`; `verbs.py:871-880`; `landgen/write.py:30`, `:386` |
| **skill cuts building time** | each act does `2 × skill` units (trade curve 0.5 to 2.0 by practice, tau 50 units): a master does four times a novice's work an act | `verbs.py:1259`, `:1354`, `:1381`; `data.py:732`; `engine/knowledge.py:58-63` |
| **structures** | wattle, timber, stone; wear and breaks by structure (timber half wattle's), mending a timber building takes timber; tiers plain to grand (materials ×1 to ×4, work ×1 to ×8) | `data.py:778`, `:783-791`, `:391-396` |
| **works using timber** | rooms (`ROOMS`), fittings (beds, bins, granary, woodshed holding 40 timber, smoke racks, water wheel), the weir (wattle 6 timber a section; timber 10), fences (4 timber, 10 units a unit of size), the camp, the handcart (6 timber), plough (4 timber, 1 copper), pack (1 hide, 1 timber), fishing rod (0.5 timber), crude tool (1 timber, 0.5 stone) | `data.py:234-311`, `:345`, `:376-379`, `:963-967`, `:587-669` |
| **carrying** | on foot 10 weight, a pack +10, a handcart +30 on a track, a pack ox 60 | `data.py:812`, `:105-106`, `:991`; spec `economy/transport.md:28-36` |
| **crews** | the weir is crew work (2, named); walling is a crew trade; no building's raising needs a crew | `verbs.py:987-999`; `data.py:345`, `:531` |
| **clocks** | the woods' rates on the year clock (`FORESTS.*.grow`, `regrow`, `shed`, `rot`); `forests.seed` takes the world's year (4 × season length) | `engine/clocks.py:19-40`; `engine/world.py:117` |

### 2.2 Against the ladder: what it lacks

| Ladder step | Engine now | Gap | Size |
|---|---|---|---|
| **timber's weight** | weight 2 against 10 on foot: a person carries **5 timber, about 1.2 t of oak** | the real load on the back is about 25 to 30 kg, an eighth of one timber; [[D2-264 The fishing, hunting and materials network|D2-264]] decided kilograms, not yet built for timber | **the biggest**: it removes carriage, the cart and the raising as levers; the building clock's 65-loads-on-foot warning (building_clock.md stage 4) |
| **standards' growth** | managed wood trees K 600, logistic 1% a year: at best 1.5 timber a unit of size a year, **about 180 kg a ha a year**, and nothing at full stock | real standards in coppice add perhaps 0.3 to 1 t a ha a year (est.); a regrowing high forest 4 to 8 m³ a ha a year (m); old forest's best (375 kg a ha) is 10 to 20 times slow for a wood that was felled and regrows | a calibration (the young growth is close: managed best 3 t a ha a year green against a real 4 to 5) |
| **underwood's products** | young growth gives only firewood; "cut poles" gives firewood | poles and stakes (for weirs, fences, rafters, hurdle uprights), cordwood for charcoal, bark; withies proposed in [[W-73 Fishing, hunting and their materials developed together|W-73]] | central: the coppice's whole value is its joint products |
| **charcoal's wood** | burned from 5 **timber** (standing trees) | real charcoal came from underwood cordwood; the engine puts the smith against the builder on the standards, where the real clash was the smith against the hurdle-maker and tanner on the underwood | a wrong conflict, cheap to fix |
| **conversion** | none: felled timber goes straight into frames, chests, ploughs, rods and racks | cleaving, hewing, sawing; boards as a good (chests, doors, barrels, boats, shingles); the saw as a tool from the smith; the sawyer pair | a ladder rung with real choices (split the best trees, saw the rest) |
| **seasoning** | none | boards and staves seasoned a year an inch (a world year on the year clock); frames green | small mechanism, one keeping process (as smoking and retting) |
| **seasons of felling** | `fell` any day, any season | winter for timber, spring for bark, dormant season for underwood | `by_season` already exists on techniques (`verbs.py:632-633`) |
| **quality of trees** | one timber; a sign says the straight trees are gone below half stock | great timber (long straight oaks for a tie-beam, a keel, a mill shaft) scarce and slow; cleavable trees; crooks for boats and braces | a design choice: a share of the stock, or a separate good |
| **builders as a trade** | the carpenter's trade on medium rooms and halls; skill speeds work | soundness from craftsmanship ([[D2-276 Making durable things runs on the year clock|D2-276]]'s companion, building_clock.md Q4); the small timber room needs no carpenter; carpenter and mason as one builder livelihood with specialisms (household_skills.md addendum) | the building clock's first companion |
| **the raising** | one person can build any building alone, act by act | a frame raised in a day by a crew: many hands at once | an enforcement-needs-people lever (scenario_design.md §1.4) |
| **prefabrication** | a building is built where it stands | framing at the wood, carried as a frame (lighter than the logs) | optional; matters only once carriage is real |
| **carriage** | handcart, pack ox; ox cart "later" | dragging, sledges (winter), ox carts on tracks, floating downstream | follows from kilograms |
| **rights and office** | [[D2-158 Default rights in woods|D2-158]]'s default rights; possession enforced, felling heard | botes (housebote, haybote) as allowances; a woodward who allots and presents; closed seasons; fenced panels (OPEN [[L-120 Wildlife pack K7 land works and infrastructure|L-120]], coppice rotation, deferred) | institutions on a resource; the engine has offices and standing orders to build them on |
| **boats** | none (OPEN [[L-38 Travel by water|L-38]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]) | logboats (most British dated finds early medieval; sec.), coracles (hide on withies), clinker plank boats (cleft oak, a shipwright, great timber) | after the fishing wave |
| **bark** | none | spring-peeled oak bark ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]] adds it) | in this build already |
| **forests.seed's year** | default 24 days | the engine passes the world's year; the default and the docstring still say 24 (`forests.py:17`); `clocks.py:13` notes it | a tidy-up, not a gap |
| **felling rate** | 0.75 timber an hour with a crude (stone and wood) tool, 1.5 with copper | real 0.3 to 1 an hour with iron (est.); stone 2 to 4.5 times slower than steel (sec.) | the crude tool is fast for stone; copper about right; no iron |

## 3. Leverage and dependence

### 3.1 The dependency graph (scenario_design.md §1)

| Group | Produces | Lacks | Gets it from | What the other side can do to it |
|---|---|---|---|---|
| **the wood's holder** (lord, or a village with a common wood) | standing timber, the cut of the underwood, bark, pannage; the woodward's allotment | labour to cut, carriage, a carpenter, the smith's tools | woodsmen, carters, carpenter, smith | refuse to cut or carry; steal (cut by night, heard); let beasts into the panels |
| **commoners** | labour; beasts | housebote and firewood; fencing wood | the holder's allowance; dead wood (anyone's) | graze the coppice regrowth (kills it); take more than the allowance; refuse the raising |
| **the carpenter** (often one in a valley: Wenbridge's Wright, `make_wenbridge.py:93-95`) | frames, mills, carts, ploughs | timber (the holder's), carriage, a crew to raise | holder, carter, neighbours | the only one who can frame: sets the price and the order of work |
| **the carter** (oxen, a cart, a track) | carriage of logs and frames | fodder, the wright's cart | herders, the wright | the bottleneck once timber weighs what it weighs |
| **the smith** | axes, adzes, augers, saws, nails | charcoal (from underwood), ore | the collier, the holder's coppice | no tools, no felling or conversion; tools wear |
| **the collier** | charcoal | cordwood (the holder's underwood) | the holder | the smith's fuel |
| **the tanner** | leather (straps, harness, bellows) | bark (spring oak), hides, lime | the holder, hunters and herders | the bellows: the smith needs the tanner too |
| **fishers** | fish | weir stakes and poles, withies, a boat | the coppice, the withy bed, the wright | the weir's holder takes a share of the run |
| **the salter, the smokehouse** | salt, smoked goods | fuel by the cartload | the holder's underwood, the carter | fuel is bulk: carriage again |

No node here needs nothing from anyone, provided **carriage is real** and **the frame needs a carpenter and a crew**.

### 3.2 Chokepoints

1. **The standing trees** (the holder, with the woodward): who may fell, which trees, when. Felling another's is heard ([[D2-158 Default rights in woods|D2-158]]).
2. **Great timber**: the few long straight oaks a mill shaft, a hall's tie-beam or a boat's keel needs; slow (50 to 100 years), so a
   felled one is gone for the run.
3. **Carriage**: oxen, a cart, a track into the wood (OPEN [[L-120 Wildlife pack K7 land works and infrastructure|L-120]] names cart tracks into woods); in winter a sledge; on a river, the
   current downstream only.
4. **The master carpenter**: the skill to lay out and joint a frame; years to learn ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]'s learning times).
5. **The raising**: a crew of 6 to 25 on one day; whoever can call that many people out (kin, the lord's labour dues, a feast).
6. **The saw and the smith**: boards need a saw (iron or copper, the smith's) and a pair of sawyers.
7. **Spring**: six weeks when bark peels; the tanner and the builder want the same oaks at different seasons.
8. **The fenced panel**: a coppice cut this year must be kept from the beasts for several years; the herders want it open.

### 3.3 Conversion chains

- standing oak → felled log (fell; winter) → beam (hew) or boards (saw; season) → frame (carpenter) → raised building (crew) →
  shelter, a store, a smokehouse, a mill.
- coppice → poles and stakes (weirs, fences, rafters), rods (withies: hurdles, wattle, traps), cordwood → charcoal → the smith → axes
  and saws → felling again (a loop).
- spring oak → bark → tan pits ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) → straps, harness, bellows → the pack frame, the ox's harness, the smith's forge.
- underwood → faggots and firewood → the smokehouse, the brine pan, the oven, the hearth.
- great timber → the mill's shaft and wheel → grain ground for the village (the miller's chokepoint rests on the carpenter's and the
  holder's).

### 3.4 Where timber meets the other systems

| System | Timber's part | Engine now | What changes with a timber economy |
|---|---|---|---|
| **fishing** ([[W-73 Fishing, hunting and their materials developed together|W-73]]) | weir stakes (oak, alder, hazel poles: about 25 a 10 m section, 5 to 8 kg each; withies note §3.4), wattle, smoke racks, the smokehouse, rods, later boats and barrels | the weir in timber (6 a section) and proposed withies; no boats | poles from the coppice, not felled timber; boats as the great-timber and shipwright chokepoint (after this wave); barrels need a cooper and seasoned staves |
| **building** ([[D2-276 Making durable things runs on the year clock|D2-276]]) | the frame, the roof, floors, shingles, doors | rooms in timber, a carpenter on the larger | the frame's real timber in kilograms, a carpenter's craftsmanship, the raising; wattle on posts and withies (storage.md §11) |
| **fuel** | firewood (hearth), cordwood and charcoal (smith, salt), faggots (oven) | firewood from dead wood and young growth; charcoal from timber | charcoal from cordwood; salt and smoking as bulk fuel buyers of the underwood (Droitwich's brine pans "consumed vast quantities of wood", pole wood, Leland's "great and notable destruction of wood"; sec.) |
| **tanning** ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]) | oak bark | none yet | bark from spring-felled or peeled oak or oak coppice; the clash with winter felling |
| **farming and herding** | ploughs, harrows, carts, hurdles, fences, the haybote | plough, harness, fence in timber | the hurdle and dead hedge from underwood (building_clock.md's cheaper crop protections); beasts against the coppice |
| **metal** | charcoal; tool handles | charcoal from timber | the collier's demand sets the coppice's cycle (03_crafts §1.2) |

## 4. A candidate scope for the timber wave

Written as feature units ([[D2-244 The engine's reworking into feature packages|D2-244]]: each with its data, verbs, signs and processes together, so the later cut can move it whole), and
as shallow ladders: every rung optional and worth having alone, the bottom rung always open to a household with nothing (Zach, [[W-73 Fishing, hunting and their materials developed together|W-73]]:
"it should be possible to do things with less layers, that have less beneficial outputs").

**T1. Timber by weight, and its carriage** (needs [[D2-264 The fishing, hunting and materials network|D2-264]]'s kilograms first). Timber at about 240 kg; a person cannot carry a timber,
can drag one (a unit a short way, est.), or carry a share with others; a pack ox or a horse drags or carries one or two; a cart on a
track takes 2 to 4; a sledge in winter more; a raft or boat downstream more again. Signs: the drag marks, the cart rutting the track,
logs stacked at the wood's edge. This alone makes the carter and the track levers.

**T2. The woods' products by kind.** Trees as standards (timber), young growth as underwood giving **poles** (timber-mass stakes, from a
managed wood without felling standards; the withies note's question 4), **cordwood** (for charcoal: charcoal moved off standing timber),
firewood and, from oak, **bark** in spring ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]); `by_season` on felling (winter better for timber; spring for bark) and cutting
(dormant season). Optionally a **great timber** share of the trees stock (long straight oaks), thinned first and slow to return,
needed by mills, halls and keels. The standards' growth calibrated against real increments (§2.2).

**T3. Conversion.** Kept to one making step from a log: **hew** (a beam; folded into the frame's units, so no beam good) and **saw or
cleave** to **boards** (one new good, the joinery and cooperage input; cleaving only from good trees, sawing needs a saw and a pit
and two people). **Seasoning** as a keeping process on boards (a year an inch, a world year). Frames take green timber with no wait.

**T4. Builders as a trade** (building_clock.md's first companion). The builder livelihood with wright and mason specialisms
(household_skills.md addendum); framed buildings need a builder at capable or above, wattle and posts none; skill cuts units (as now)
and sets **soundness**, which slows wear and breaks beside structure and tier; the **raising** as crew work for any framed building
(a day, a crew by size); optional framing at the wood, the frame carried (lighter than its logs).

**T5. Rights and the woodward.** Botes as allowances (housebote, haybote) that a holder grants and an office keeps; a woodward who
allots the cut and presents those who take more; closed seasons; a coppice panel fenced after cutting (OPEN [[L-120 Wildlife pack K7 land works and infrastructure|L-120]], deferred, where
this meets hedges and banks). Built on offices and standing orders that exist.

**Out of this wave, unless Zach says otherwise:** boats ([[L-38 Travel by water|L-38]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]]), the water-powered saw, coopers and barrels (storage.md §3.6),
the joiner's trade, log building for a northern world, iron.

**Measurement** (scenario_design.md §6): a farm or fishing world with a managed wood, read against its null arm (today's timber): does
building still happen, who carries, who raises, does the wood hold its standards over a run, does the coppice get grazed out, does a
holder use the wood as a lever. Bots first, then a short live run ([[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]'s staging pattern).

### 4.1 Questions for Zach (each stands alone)

1. **Timber's weight in kilograms:** should a timber weigh its real 240 kg or so, so that no one can carry one on their back and
   carriage (dragging, an ox, a cart, a river) becomes the step every building waits on?
2. **A timber's size:** keep one timber as about 240 kg (a log about 30 cm by 3.3 m), or set it to a larger real measure such as a
   medieval load of 50 ft³ (about 1.4 t), fewer and heavier?
3. **Poles from coppice:** should cutting a managed wood's young growth give poles and stakes (counted as timber, or as a new pole
   good) without felling the standards, so that weirs, fences and rafters come from the underwood as they really did?
4. **Charcoal from underwood:** should charcoal be burned from cordwood cut from young growth rather than from felled timber, so the
   smith competes with the hurdle-maker and the tanner for the coppice rather than with the builder for the standards?
5. **Seasons of felling:** should timber felled in winter be better (or spring-felled timber worse), and bark peel only in the six
   weeks of late spring, so that the tanner and the builder want the same oaks at different times?
6. **Great timber:** should a wood hold a small, slow share of long straight trees that mills, halls and keels need and ordinary
   timber cannot replace, so that great timber is scarce and held?
7. **The standards' growth:** a managed wood's trees now regrow at best about 180 kg a hectare a year against a real figure perhaps
   two to five times higher, and a felled old forest ten to twenty times slower than real regrowth; raise them to real rates on the
   year clock, or keep woods slow on purpose so that felling is a lasting loss within a run?
8. **Boards as a good:** should there be one converted good, boards (riven or sawn), for chests, doors, floors, shingles and later
   barrels and boats, with beams folded into the frame's work rather than made a good of their own?
9. **The saw:** should sawing boards need a saw (a smith's tool) and two people at a pit, while cleaving needs only wedges but only
   works on good straight trees?
10. **Seasoning:** should boards need seasoning before joinery (about a world year an inch, as a real year an inch), while frames are
    built from green timber with no wait, as medieval carpenters did?
11. **Craftsmanship:** should a builder's skill set how sound a building is (how slowly it wears and how seldom it breaks), beside
    its structure and tier? (The same question as building_clock.md Q4, asked here with the timber frame in view.)
12. **The raising:** should a framed building need a crew on one day to raise its frame (a few people for a cottage, many for a
    hall), so that building needs neighbours, kin or a lord's labour?
13. **A framed cottage needs a builder:** should even a small timber room need someone who knows framing (at capable or above),
    while posts-and-wattle stays open to anyone?
14. **Rights in the wood:** should a holder be able to grant allowances (wood for building, wood for fences) and name a woodward who
    allots the cut and reports those who take more, with closed seasons and fenced panels after a cut?
15. **Northern log building:** for a northern or upland world with pine, should log building (many trees, little skill, no saw) be a
    separate path beside framing (few trees, a carpenter), or left out?

## Sources

**Engine and project:** `cybertron2/engine/data.py` (ITEMS 43, 44, 87, 105-106; FORESTS 204-220; CLEARING 222; FITTINGS 234-287;
ROOMS 290-300; BLUEPRINTS 302-311; MONUMENTS 334-346; WATER_WORKS 376-379; TIERS 391; TECHNIQUES `fell` 421, `firewood` 424, `cut` 434,
`fence` 526, `wall` 531, `pack` 587, `handcart` 589, `charcoal` 655, `wooden plough` 657, `smelt` 670; SKILL 731-741; PHYSICS breaks 778, wear 783,
carry 812; ENV felled 916; FENCES 963; pack ox 991); `cybertron2/engine/forests.py`; `cybertron2/engine/renewal.py`;
`cybertron2/engine/verbs.py` (601, 631-637, 871-880, 987-999, 1259, 1354, 1377-1395); `cybertron2/engine/buildings.py` (261-290);
`cybertron2/engine/knowledge.py` (40-75); `cybertron2/engine/signs.py` (692-702, 964); `cybertron2/engine/clocks.py`;
`cybertron2/engine/world.py` (117); `cybertron2/wild/kinds.py` (378); `cybertron2/wild/plants.py` (60, 112);
`cybertron2/landgen/settle.py` (523); `cybertron2/landgen/write.py` (30, 176, 386); `cybertron2/specs/make_wenbridge.py` (26-27,
61, 93-95). Spec: core/clocks.md ([[D2-273 Three clocks, each system on one|D2-273]], [[D2-275 A unit of work is 2 hours|D2-275]], [[D2-276 Making durable things runs on the year clock|D2-276]]); environment/resources.md "Forests" ([[D2-156 A forest is three stocks|D2-156]], [[D2-158 Default rights in woods|D2-158]]); economy/production.md
"Wood"; world/holding.md "Wood"; economy/transport.md. Decisions [[D2-156 A forest is three stocks|D2-156]] to [[D2-161 Seed nodes below what they sustain|D2-161]], [[D2-264 The fishing, hunting and materials network|D2-264]], [[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]], [[D2-270 Household skills|D2-270]], [[D2-276 Making durable things runs on the year clock|D2-276]], [[D2-281 Tanning comes in this build, with bark as a new good|D2-281]]. OPEN [[L-38 Travel by water|L-38]],
[[L-110 Salt's fuel, to recalibrate|L-110]], [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-120 Wildlife pack K7 land works and infrastructure|L-120]], [[L-125 Brief 5's fen and boats half (pack K4's rest)|L-125]], [[L-146 Peat as fuel where there is bog|L-146]], [[L-153 Clearing a plot at a time|L-153]], [[L-157 Rest days, with health, fatigue and illness|L-157]]. Notes: proposals/building_clock.md; proposals/hunt_fish_materials.md (§7.6);
02zzzh_hunt_fish/withies_wood_materials.md, building_clock.md, storage.md (§11), household_skills.md (addendum);
02zzj_economy_research/03_crafts_woods_metal_building.md (§1, §4, §6); 02z_forest_model.py; 02zb_build_brief_forests_and_fuel.md.

**Web (all read through search summaries; sec.):**
- Woodland, coppice, standards, pollards: [Overstory #47, coppice-with-standards](https://agroforestry.org/the-overstory/217-overstory-47-coppice-with-standards-new-forestry-with-ancient-roots); [Teagasc, coppice-with-standards](https://t-stor.teagasc.ie/server/api/core/bitstreams/38aa5f50-34a3-4db8-9117-8ce4e328dfd4/content); [Forestry Commission leaflet 83 (1984)](https://cdn.forestresearch.gov.uk/1984/04/fclf083_1984.pdf); [conservation handbooks, coppicing](https://conservationhandbooks.com/woodlands-introduction/a-brief-history-of-woodlands-in-britain/coppicing/); [Gabriel Hemery, coppice with standards](https://gabrielhemery.com/knowledge/topics/coppice-with-standards/); [Rackham, Yale colloquium paper](https://macmillan.yale.edu/sites/default/files/files/colloqpapers/07rackham.pdf); [Franklin, the productive potential of ancient oak coppice (ODI)](https://cdn.odi.org/media/documents/1070.pdf); [Woodland Trust, wood pasture](https://www.woodlandtrust.org.uk/media/1825/wood-wise-wood-pasture.pdf); [PTES, pollard trees](https://ptes.org/campaigns/wood-pasture-parkland/wildlife/pollard-trees/); [Pollarding](https://wikipedia.com/wiki/Pollarded).
- Domesday woodland, royal forests, rights: [Herefordshire Through Time, woodland](https://htt.herefordshire.gov.uk/herefordshires-past/the-medieval-period/countryside-and-landscape/woodland); [TÜBA, royal hunting forests](https://www.tuba.gov.tr/files/yayinlar/raporlar/TUBA-978-3-902762-91-7_ch04.pdf); [Darby, Domesday England: woodland and forest](https://core-prod.cambridgecore.org/core/books/domesday-england/woodland-and-forest/49916C01CF3BCD6FAA14F5914BD7FDCF); [Lancaster manorial records glossary](https://www.lancaster.ac.uk/fass/projects/manorialrecords/glossary/index.htm); [Hampshire Field Club, Hants life](https://www.hantsfieldclub.org.uk/publications/hampshirestudies/digital/Shore_Memorial/Hants_life.pdf); [Yorkshire dictionary, hay boot](https://yorkshiredictionary.york.ac.uk/words/hay%20boot); [Froyle, officers and servants](https://froyle.com/oands.htm); [Earls Colne court rolls](https://wwwe.lib.cam.ac.uk/earls_colne/ecrolls2/66501481.htm); [Forests and chases glossary (St John's, Oxford)](https://info.sjc.ox.ac.uk/forests/glossary.htm).
- Buildings and their timber: [Suffolk HER, Grundle House](https://heritage.suffolk.gov.uk/Monument/MSF25615); [Historic England, Grundle House](https://historicengland.org.uk/listing/the-list/list-entry/1285805); [Friends of Cressing Temple, barns and medieval carpentry](https://thefriendsofcressingtemple.org/the-barns-and-medieval-carpentry-new/); [Robin Wood, Rackham at Cressing](https://www.robin-wood.co.uk/wood-craft-blog/2010/09/06/ancient-carpentry-and-ancient-woodland/); [UWE, traditional timber framing](https://fet.uwe.ac.uk/conweb/house_ages/timber/print.htm); [Triskele, dendrochronology and green timber](https://triskeleheritage.triskelepublishing.com/mediaeval-mythbusting-blog-14-dendrochronology-dates-the-timber-not-the-building-and-other-fallacies/); [Thompson, the conversion of structural timbers](https://buildingconservation.com/articles/structural-timber-conversion/structural-timber-conversion.htm); [Historic England, timber conservation](https://historicengland.org.uk/images-books/publications/timber-conservation/timber-marketing-spreads); [Butser, Anglo-Saxon hall](https://the-past.com/news/butser-ancient-farm-launches-latest-reconstruction/); [Weald and Downland, Bayleaf](https://www.wealddown.co.uk/?p=16303); [designing buildings, green wood](https://www.designingbuildings.co.uk/wiki/Green_wood).
- Carpenters and costs: [Medievalists.net, how carpenters built medieval England (Dyer)](https://www.medievalists.net/2025/11/how-carpenters-built-medieval-england/); [Building a cob house in Devon in 1461 (Vernacular Architecture)](https://informahealthcare.com/doi/full/10.1080/03055477.2020.1801313); [Mortimer village, timber](https://www.mortimervillage.org.uk/sites/mvp/files/MTTA/Timber.pdf); [Salzman, Building in England down to 1540](https://businesshistoryexplorer.businessarchivescouncil.org.uk/publications/27815).
- Conversion: [Sawpit](https://Www.wikipedia.org/wiki/Sawpit); [Follansbee, pitsawing part 2](https://peterfollansbeejoinerswork.substack.com/p/pitsawing-part-2); [Core77, saw pits](https://core77.com/posts/53118/A-Brief-History-of-Wood-Splitting-Technology-Part-2-Saw-Pits); [Mittelzeit, saw pit and sawyer](https://mittelzeit.blogspot.com/2016/09/saw-pit-sawyer.html); [Press Herald, hewing beams](https://www.pressherald.com/?p=7385688); [permies, hand hewing beams](https://permies.com/mobile/t/58723/Hand-hewing-beams); [Hewing](https://www.Wikipedia.org/wiki/Hewing); [Riving](https://www.Wikipedia.com/wiki/Riving); [Clapboard](https://EN.wikipedia.com/wiki/Clapboard).
- Felling and seasons: [Penn Museum, a tree falls](https://www.penn.museum/sites/expedition/a-tree-falls-in-philadelphia/); [Palafittes, felling trees](https://archeologie.culture.gouv.fr/palafittes/en/felling-trees); [MDPI Forests 14(2) 202, stone and steel axes](https://www.mdpi.com/1999-4907/14/2/202); [hearth.com, felling with an axe](https://www.hearth.com/talk/goto/post?id=1369419); [Philosophical Transactions, spring and winter-felled oak](https://jimclifford.ca/philosophical-transactions-ocr-1665-1869/articles/jstor-107552/); [Chest of Books, felling timber](https://chestofbooks.com/home-improvement/woodworking/Carpentry-Principles/Felling-Timber.html).
- Seasoning and weight: [Chest of Books, weight of timber green and seasoned](https://www.chestofbooks.com/home-improvement/woodworking/Carpentry-Principles/456-Weight-Of-A-Cubic-Foot-Of-Timber-When-Green-And-When-Seasoned.html); [Hardwoods Group, how long green oak takes to season](https://hardwoodsgroup.com/?p=482); [forestry.gov.scot, green oak in construction](https://forestry.gov.scot/images/corporate/pdf/green-oak-in-construction-2007.pdf).
- Carriage: [Timber rafting](https://en.wikipedia.org/wiki/Timber_rafting); [Ważny, Baltic timber (medievalists.net)](https://www.medievalists.net/2011/04/the-origin-assortments-and-transport-of-baltic-timber); [waldwissen, Holländer logs](https://www.waldwissen.net/en/people-and-forests/forest-history/the-trade-in-hollaender-logs); [Weller, loads](https://humanist.de/rome/rts/load.html); [historyrise, siege engines](https://historyrise.com/article/the-engineering-challenges-of-transporting-large-siege-engines/); [Maine Forest and Logging Museum, the two sled](https://www.maineforestandloggingmuseum.org/wp-content/uploads/The-Incredible-Two-Sled.pdf).
- Charcoal and bark: [Revolutionary Players, charcoal burning](https://www.revolutionaryplayers.org.uk/?p=2371); [Sadb farm, charcoal clamps](https://sadbfarm.blogspot.com/2017/06/charcoal-clamps.html); [Springer, charcoal temperatures](https://link.springer.com/article/10.1007/s12520-009-0018-z); [Revolutionary Players, work and labour (bark)](https://www.revolutionaryplayers.org.uk/work-and-labour/); [Bolton-le-Sands, oak bark peeling](https://boltonlesandsparish.gov.uk/amenities/thwaite-brow-woods/oak-bark-peeling/); [Forest Research, oak age report](https://cdn.forestresearch.gov.uk/2022/02/freunw_oak_age_report.pdf).
- Salt and fuel: [Salt Association, the Middle Ages](https://saltassociation.co.uk/education/salt-history/middle-ages/); [Birmingham Post, Droitwich](https://www.birminghampost.co.uk/lifestyle/flavour-droitwich-spas-rich-history-4042811); [Dodderhill parish survey, salt](https://dodderhillhistory.org.uk.dodderhillparishcouncil.co.uk/dodderhill-parish-survey-project-local-trades-salt.php.html).
- Fish weirs and boats: [Historic England, Anglo-Saxon hurdles and basketry, Collins Creek](https://historicengland.org.uk/research/results/reports/4488/ANGLO-SAXONHURDLESANDBASKETRYCOLLINSCREEKBLACKWATERESTUARYESSEX); [Archaeology Data Service, Blackwater fish traps](https://archaeologydataservice.ac.uk/archives/view/essexcou1-90254); [Viking Ship Museum, the Sea Stallion](https://www.vikingeskibsmuseet.dk/en/visit-the-museum/exhibitions/the-five-reconstructions/the-sea-stallion-from-glendalough-skuldelev-2); [Viking Ship Museum, Skuldelev 2 reconstruction](https://www.vikingeskibsmuseet.dk/en/professions/boatyard/experimental-archaeological-research/ship-reconstruction/skuldelev-2); [Society of Antiquaries of Scotland, logboats](https://journals.socantscot.org/index.php/psas/article/download/10066/10033/10017); [Encyclopedia.com, boats and boatbuilding](https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/boats-and-boatbuilding).
- Regional building: [museum-digital, log construction](https://brandenburg.museum-digital.de/tag/17194); [Designing Buildings, log construction](https://www.designingbuildings.co.uk/wiki/Log_construction); [Britannica, construction in timber and brick](https://www.britannica.com/technology/building-construction/Construction-in-timber-and-brick); [Timber framing (Fachwerk)](https://en.Wikipedia.com/wiki/Fachwerk).

To verify before data (could not be fetched): Rackham's Grundle House count (1972), the Sidbury 1461 figures, a medieval felling or
hewing rate, a pit-sawing rate per foot, bark per hide, standards' real increment in a coppice, and the Franklin labour figure.

*Current as of 22 Nov 2026 ([[W-76 The timber economy|W-76]]; scouting, nothing decided).*
