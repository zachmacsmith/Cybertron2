---
id: docs/review/37_growth/02zzzh_hunt_fish/hunting_ladder.md
kind: note
updated: "2026-11-21"
---
# Hunting, trapping, fowling and the kill: techniques, capital and ladders (W-73, 21 Nov)

*note · `docs/review/37_growth/02zzzh_hunt_fish/hunting_ladder.md`*


**Session note for 37.2, thread [[W-73 Fishing, hunting and their materials developed together|W-73]]** (Zach, 21 Nov: recalibrate the fishing and hunting signs and mechanisms together with the
economies and resources around them; "explore the different levels and granularities and ladders and supply chains /
developmental processes of techniques and tools and capital"). This note covers **hunting, trapping, fowling and the processing of
the kill**. Fishing, fibres and cord, withies and wood, and the engine audit are covered by other notes in this folder. This is
research and design input only: no code is changed and nothing here is decided.

**Read before writing:** `proposals/hunt_calibration.md` (brief 4c, as built), `proposals/wildlife.md` §5 and §6,
`proposals/economy_web.md` §2.4, §2.10 and stages 1 and 2, `02zu_wild_chains_capital_actions.md` part B, `02zzu_shared_units.md`
parts 1, 2 and 4 (the master hunter at 1.9 on the basis), the economy research `02zzj_economy_research/` 01, 02, 03 (§6, §7) and 10
(§1.3, the return tables). Engine as read on 21 Nov: `wild/methods.py` (METHODS, TAKE_BASE, SWEEP, SETS), `wild/kinds.py` (TAKEN,
TRAITS, KINDS rows for the game), `engine/data.py` (ITEMS: meat, hide, tallow, antler, crude weapon; SKILL `hard`; `dry meat`).

**Marks.** **[firm]**: a published figure seen in this session's searches. **[recalled]**: a standard figure from the literature
that I could not re-open here (the fetch tool could not reach wwt.org.uk, bahs.org.uk or gutenberg.org from this session, so
several primary texts were read only through search summaries). **[estimate]**: my own reckoning, with its working shown.

**Conversions used throughout** (the engine's basis, [[D2-258 The food values are put on one physical basis|D2-258]]): 1 food = 2,500 kcal; a unit of work = 2 hours, so **food a unit =
kcal an hour ÷ 1,250**; 1 meat = 1,500 kcal = 0.6 food (about 1 kg of venison as eaten); a person eats 1 food a day; the
compressed year is 32 days. Food a head of game is the basis table in 02zzu part 1: red deer 19.8, roe 4.9, boar 17 to 23, hare
0.75, mallard 0.31, woodpigeon 0.10. For kinds the engine lacks: rabbit about 0.31 food (1.5 kg live x 0.6 dressing x 0.75 edible x
1,140 kcal/kg), teal about 0.10, fallow deer about 10 (50 kg live), skylark about 0.012 **[estimate, same method]**.

---

## 0. In brief

- **Hunting is many small ladders, not one.** Every method has a version that needs nothing: hands, a stick, a stone. Each step of
  capital multiplies the take by about 2 to 5 for the game that method reaches, and often opens game that was out of reach before.
  There are four real breaks in kind. One is **range**: the bow, and later the crossbow, let one person kill at a distance. One is
  **kept beasts as tools**: dogs, ferrets, hawks. One is the **crew and its works**: drives, hays, the decoy, the moult drive. The
  last is **keeping instead of catching**: the park, the warren, the dovecote, the managed heronry. After that last break the take
  no longer depends on searching, and the yield of a square kilometre goes up 5 to 10 times.
- **For a skilled hunter, hunting pays at once, but the land's yield sets the ceiling.** Including search time, real hunting gives
  a novice 0.08 to 0.3 food a unit, a capable hunter 0.4 to 1.2 and a master 1.2 to 3.2. Once a beast is found the rate is 13 to 25
  food a unit for deer. On fresh, unhunted ground a master's rate rises toward 3 to 6 **[estimate]**, and the carry then caps what
  one person brings home. Sustained over a year, a temperate wood yields only about 50 to 120 food a km² from all its big game
  **[estimate]**. That is why real hunters lived at 0.05 to 0.2 people a km².
- **The engine's compressed year makes the wild about 11 times too generous per mouth.** Breeding is scaled to the 32-day year, but
  the daily need is real. So a village's ring of about 20 km² can feed 30 to 75 people's whole diet from its game, against 3 to 7
  in reality (§4.4). This explains 4c's second miss (a master hunting one wood daily for 16 days held 2 to 3 a unit). It is the
  biggest calibration question in this note, and it needs a lever named for it, as the runs already have (x 32/365).
- **Granularity:** keep the general methods. Let the gear carry the ladder: bow, spear, dog, ferret, net, lime. **Split the
  engine's `net`:** it takes salmon at the same weight as wildfowl (`yield.takes`: salmon 3.0, wildfowl 3.0) because salmon match
  "small to medium, in a flock, in water". Fowling needs a trait of its own for birds. Add a pulse (the moult drive), eggs, and
  keeping as its own package. Leave out pitfalls, hawks and the crossbow for now.
- **Winter wildfowl:** the best modern refuges hold 400 to 1,500 waterbirds a km² of wet ground (the Somerset Levels 73,000 to
  97,000 birds; the Ouse Washes over 20,000 on about 25 km²). A whole wet district averages perhaps 50 to 300 a km². The engine's
  150 a km² of wet habitat on arrival is in range. Its 4 to 52 a km² over whole areas is low for a true fen and fair for mixed land.

---

## 1. The catalogue

Columns: what it takes; what it needs to make (materials and work, its life); crew; skill and how it is learnt; season and ground;
the take, real, with the source; and food a unit on the engine's basis. "fau" = food a unit of work.

### 1.1 With nothing, or with what lies to hand

| Technique | Game | Make and life | Crew | Skill | Season, ground | Take (real) | fau |
|---|---|---|---|---|---|---|---|
| **taking by hand** (hares in the form, beasts in deep snow, frozen or weak fowl, carrion) | hare, fowl in a freeze, the dead | nothing | 1 | low; knowing where | hard frost and snow; a great freeze puts fowl on the last open water | pulses only; the engine's "great freeze" sign already says "birds so weak you could pick them up" | 0 most days; 1 to 3 in a freeze **[estimate]** |
| **throwing stick, stones** | hares, rabbits, birds on the ground | a club or stick, 0.5 to 1 unit; lasts until lost | 1 | high for a good throw, years | open ground | low: hunter-gatherer small-game rates of 300 to 1,000 kcal an hour **[recalled, Kelly]** | 0.1 to 0.4 |
| **digging out** (an earth, a burrow, a lodge) | fox, badger, rabbit, beaver | a spade or digging stick; a dog helps greatly | 1 to 2 | medium; knowing the earth | any; best when the young are in it (spring) | an earth a day or two of digging; cubs at the earth in spring (the engine's fox `litter`) | low as food; the take is pelts and riddance |
| **robbing nests: eggs and young** | gulls' eggs, wader and duck eggs, young rooks, herons, pigeons | nothing; a climb or a boat | 1 | low | spring only, for a few weeks | Scoulton Mere gullery (Norfolk) about 20,000 gulls' eggs a year **[firm via a secondary source, undated]**; the licensed English harvest of black-headed gulls' eggs 31,518 in 2015 **[firm]** | high in the window: a gull's egg is about 40 g, about 0.025 food, so 100 eggs a day is 2.5 food a day, 0.4 to 0.5 fau **[estimate]** |

### 1.2 Set gear: snares, nooses, traps

| Technique | Game | Make and life | Crew | Skill | Season, ground | Take (real) | fau |
|---|---|---|---|---|---|---|---|
| **snare (noose on a run)** of cord, sinew, gut or horsehair; wire only from the 18th century | hare, rabbit; fox and roe in a stronger noose | about 1 m of cord or 6 to 10 tail hairs plaited and a peg a snare; 20 to 50 snares in 1 to 2 units; a snare lasts a season or until sprung and torn | 1 | low to learn, long to master: reading the runs, the height, the scent | all year; best in winter, on runs through hedges and gaps | snares set for foxes caught hares at 3.5 to 8.5 per 1,000 snare-nights **[firm: GWCT and Defra trials]**. That is a floor, as those nooses were not set for hares. A practised snarer on known runs takes 5 to 15 per 100 snare-nights **[estimate]** | 0.4 to 1.2 (02zzu); engine 0.64 to 0.9 lifted |
| **springe** (a bent stick and a horsehair noose; "springes to catch woodcocks") | woodcock, snipe, thrushes, partridge | a hazel rod, hair, a trigger peg; minutes each | 1 | low | autumn and winter, on the birds' walks in woods and wet ground | woodcock were taken in numbers in the west (Cornwall, Devon) **[recalled]**; no per-day figure found | 0.1 to 0.4 **[estimate]** |
| **deadfall** (figure-4 or paiute trigger, a stone or log) | small mammals, pine marten, birds | a flat stone or log and three sticks; about 0.25 unit each; lasts years | 1 | medium: the trigger is a knack | any; no cord needed | ethnographic small-game trapping: the Hadza trapping trial gave a catch on about 1 day in 3 over 102 hunter-days **[firm, Hawkes et al. 1991]** | 0.1 to 0.5 **[estimate]** |
| **pitfall** (a pit with a cover, often in a line with fences) | elk, reindeer, red deer, boar, wolves | 1 to 3 person-days a pit; a line of tens of pits; it lasts centuries with recutting | a household or village to dig, 1 to check | low | the beasts' passes; boreal and upland | Scandinavian elk-pit systems ran from the Mesolithic to the 1800s **[recalled]**; a catch a pit a year is low, about 0.1 to 0.5 **[estimate]** | low a unit once built; a village work like the weir |
| **cage, box and tunnel traps** | rats, mustelids, live hares, birds | timber or withies, 1 to 2 units; years | 1 | low | any | vermin control, not food | ~0 as food |
| **gin (iron jaw) trap** | vermin, rabbits, otters | iron and a spring: a smith's work | 1 | low | any | early modern (17th to 19th century) | out of period |
| **purse nets and ferrets** at a warren or burrow | rabbits | purse nets of cord (a few hundred metres of netting in total for 20 to 50 nets: several days of netting); a ferret kept and fed; nets last years | 1 to 2 | medium; ferret handling | winter (no young in the burrows) | a boy with ferrets took 60 to 100 a day where rabbits were a plague (New Zealand, 1919); 15 to 20 pairs a day (Australian recollection) **[firm, both pest densities]**. Medieval warrens: "few culled more than 3,000 a year" (Bailey); Gooderstone 348 in 1370; Blythburgh about 1,000 a year in the 1460s **[firm via Norfolk and Suffolk HERs]** | at pest densities 2 to 6; at a medieval warren's 0.5 to 2 **[estimate]** |
| **long net at night** | rabbits feeding out, hares | 50 to 100 m of net, stakes; days of netting | 2 | medium | dark nights, wind toward the net | no checked figure | high in a good warren, as purse nets |

### 1.3 Weapons in hand

| Weapon | Game it opens | Make and life | Skill and learning | Note |
|---|---|---|---|---|
| **club, fire-hardened spear** (the engine's `crude weapon`) | anything cornered: a beast held by dogs, in snow, at a den or in a drive | 1 timber and 1 unit (engine); lasts while it holds | low | the Schöningen spears (about 300,000 years old) show the wooden spear alone killed horses **[firm, 02zzj/10]** |
| **sling** | birds, small game; a shepherd's weapon | a cord and a leather pouch, 0.5 unit; years | **very high**: years from childhood | low take, no capital; leave it out of the engine |
| **hunting spear, boar spear** (an iron head with lugs or a crossbar, an ash shaft) | boar and deer at bay; the thrust that holds a charging boar | a smith's head (about 0.5 to 1 kg of iron) and an ash pole; the shaft lasts years | medium; the danger is the skill | with hounds to hold the boar at bay; alone, a boar kills (the engine's `danger`) |
| **self bow** (one stave: yew, elm, ash, hazel) | deer at 20 to 40 m, hares, birds; one person hunts alone | a stave seasoned months to a year (faster roughed out); 4 to 8 units of a skilled maker's work to tiller and finish **[estimate, from primitive-bow practice]**; a string of flax, hemp, sinew or gut; it lasts years with care | **long**: shooting well takes years. English statutes (1512, 1541) bound boys from 7 to keep a bow and practise **[recalled]** | brought small fast game into reach and made the solo deer hunt common (02zzj/10) |
| **arrows** | | a shaft (birch, ash, hazel shoots), a head (fire-hardened, bone, flint, then iron), 3 fletchings, glue and binding: about 0.5 to 1 unit each by hand **[estimate]**; lost or broken often | | the five chains: wood, cord, feathers, heads, glue (02zzj/10) |
| **longbow** | the same game as the self bow; the war bow's draw is not needed to kill a deer | the same craft at more draw weight; a bowyer's trade | **from youth** | for the engine, the same item as the bow at a higher skill: not a separate weapon |
| **crossbow** | deer; the parker's and the poacher's weapon from the 13th century | a steel or composite prod, a tiller, a nut and trigger: a specialist's work; costly | **days to weeks**: easy to learn, low ceiling | the opposite of the bow: capital instead of skill. Leave it out until there is a smith and a trade in mechanisms |

Rates for a weapon hunt, including search. Ache men (bows, then shotguns) brought game home on 48% of days; men's hunting gave about
750 to 1,300 kcal an hour, **0.6 to 1.0 fau** **[firm, Hill et al. 1987; Hill and Kintigh 2009]**. Modern bowhunters at a
Maryland base took 35 hours of hunting per recovered white-tailed deer **[firm, Indian Head study, 1989 to 2006]**. That is about
27 kg edible, 32,000 kcal, so 920 kcal an hour, **0.74 fau**, with modern bows, tree stands and dense deer. Once a beast is found,
the rate is far higher: deer 16,000 to 31,000 kcal an hour, **13 to 25 fau**; jackrabbit 13,000 to 16,000, **10 to 13 fau**
**[firm, Simms via Kelly]**. Hadza bow hunters killed large game on only 1 to 3% of hunter-days **[firm, Hawkes et al. 1991; Wood
and Marlowe 2013]**. That is savanna big game with very lumpy returns, and it is not the shape a temperate wood should take.

### 1.4 Beasts as tools

| Beast | What it adds | Cost to keep | Make and life | Skill | Note |
|---|---|---|---|---|---|
| **cur, terrier** (a farm dog) | finds and bolts game at earths and burrows; turns vermin; guards | a 8 to 12 kg dog needs 600 to 900 kcal a day, **0.25 to 0.35 food a day**, much of it scraps and offal **[estimate: 130 x kg^0.75 kcal, an active dog]** | a pup raised in months; works 8 to 10 years | low to medium | the engine already has `dog` as a watcher (a home fitting) |
| **hound, greyhound, lymer** (scent and sight hounds) | finds (detect up), holds game at bay (flee down, danger down), courses hares on open ground | a 25 to 30 kg hound needs about 1,700 kcal a day at rest and 2,500 to 3,300 on a hunting day: **0.7 to 1.3 food a day**, nearly a person's **[estimate]**. Royal accounts paid about ½d a day a hound, against a labourer's 1 to 2d **[recalled, Cummins 1988]** | trained 1 to 2 years; a kennel and a keeper | high, for the huntsman | a pack of 20 hounds eats like 15 to 25 people. That is why hounds belonged to lords, and why the law kept them from the poor (§2.5) |
| **ferret** | bolts rabbits into purse nets | about 150 to 250 kcal a day, **under 0.1 food** **[estimate]** | bred and handled | medium | with rabbits only; the engine's hare is a rabbit proxy |
| **hawk, falcon** | takes hares, rabbits, partridges, duck, herons | about 0.1 food a day of meat; a mews | months of daily manning; a skill of years | very high; aristocratic | small food; a status good (wildlife.md §6). Leave it out of the engine for food |

### 1.5 Crews and works

| Technique | Game | Capital and crew | Season, ground | Take (real) | Note |
|---|---|---|---|---|---|
| **the drive with beaters and spears** (the engine's `drive`) | boar sounders, deer, wolves | 4 to 20 people; spears; dogs help | autumn and winter, woods and fen | no per-person-day figure checked; a pulse | built: the crew bonus for the drive only (4c §5) |
| **the hay (deer hay, haia)**: long nets, or a hedged funnel and enclosure | red and roe deer driven into nets | nets of strong cord, hundreds of metres, or a hedge and bank funnel; a work of a lordship | woods | Domesday records about 31 to 37 hays and parks, most in Cheshire and Shropshire, "where wild animals were caught" **[firm]** | a **standing work**: like the weir for deer. The deer-hay wind (a ramp) is a park-edge variant |
| **bow and stable** (the Master of Game's last chapter) | deer driven past archers at stands, greyhounds slipped at the edges | a huntsman, beaters, archers, a "stable" of men and hounds at the stations | woods, a park or a forest | a royal hunt could kill several dozen to hundreds in a day **[firm, summary]**; Henry III's Christmas 1251 drew 830 deer, 200 boar and 1,300 hares from his forests **[firm, secondary]** | a drive whose crew carry bows; the engine's drive with the bow as gear |
| **the deer park** (a pale of cleft oak, a bank and ditch round a wood and lawns) | fallow deer above all; red deer | the pale: a park of 100 acres has about 2.5 km of pale; perhaps 100 to 400 person-days a km of pale and bank, and oak in quantity **[estimate]**; a parker; winter hay and browse | year round; culled in season | Havering (1,300 acres, 5.3 km²) held 1,200 deer, about one an acre **[firm, Essex Field Club]**. At a 25% cull, 300 deer of about 10 food each is **about 570 food a km² a real year** **[estimate]**. About 3,200 parks covered about 2% of England by 1300 **[firm, Rackham]** | the switch to keeping. Jean Birrell (1992): parks were "essentially farms for the production of venison" |

### 1.6 Fowling

| Technique | Birds | Capital | Crew | Season, ground | Take (real) | fau |
|---|---|---|---|---|---|---|
| **bird lime** (holly bark or mistletoe berries boiled, fermented for weeks and pounded into a glue; on twigs or lime-rods by a call bird or at a roost) | small birds, thrushes, sometimes duck on lime-lines | a pot of lime is days of slow work over weeks; it keeps | 1 | autumn and winter; hedges, bushes, a pool's edge | no figure found | low; it needs no cord |
| **clap net (day net)** with a stale (a tethered decoy), a call bird, a lark glass (a turning mirror) | larks, finches, plovers; ducks at the water's edge | two nets of 10 to 20 m on poles with a pull line: days of netting; years | 1 to 2 | autumn and winter, open fields, downs, the shore | Dunstable sent about 50,000 larks to London a year; Leadenhall took up to 400,000 a year early in Victoria's reign **[firm, secondary]**. A Hertfordshire catcher claimed about £1 a day at 1s 7d a dozen (1912), which is about 150 larks **[firm, one man's claim]** | about 1.8 food a day at 150 larks, **0.3 to 0.35 fau** **[estimate]**. Its worth was in the market, not the calories |
| **flight net, cockshoot net** (a net hung across a glade or a ditch the birds flight through at dusk and dawn; "cockshut time") | woodcock in woods; duck flighting over the fen | a tall net on poles, lines and stones to drop it; a glade cut through the wood (the cockshoot) | 1 to 2 | dusk in autumn and winter; woodland rides, fen ditches | a cockshoot in a park at North Duffield is recorded in 1473-4 **[firm]**; no take figure | 0.2 to 1 **[estimate]** |
| **bat-fowling, trammel at night** | roosting birds in hedges, larks in stubble | a lantern, a net on poles, a trammel of 9 m (30 ft) between two men | 2 | dark winter nights | Victorian trammels of 30 ft dragged over the fields by two men **[firm]** | low to medium |
| **the moult drive** (flightless moulting duck driven by boats and beaters into a funnel of nets) | mallard and other ducks in moult, July and August | long funnel nets, boats, a crew of tens | a village | summer moult, the open fen and meres | "as many as 4,000 birds at one drive" in Deeping Fen (Willughby 1678); 3,000 driven into nets at one time (Gough, 1720) **[firm via Essex Field Club]**. An act of 1534 set a close time "to avoide distruction of wilde fowle" **[firm]** | 3,000 to 4,000 mallard-sized birds is 930 to 1,240 food. With 30 to 60 people for a day, that is **15 to 40 food a person-day, 3 to 8 fau** **[estimate]**. A pulse once a year, and it empties the breeding stock |
| **the duck decoy** (a pond of 1 to 3 acres with 4 to 8 curved pipes of hoops and netting, screens, a dog and tame decoy ducks; 17th century in England, from the Dutch *eendenkooi*) | wild duck, teal, wigeon in winter | the pond dug and the pipes built: a large work **[estimate: hundreds of person-days]**; the pipes renewed every few years; a decoyman full time in the season and a trained dog | 1 decoyman (and a boy) | October to March; a quiet pond in wet country | Ashby, Lincolnshire, 1833-4 to 1867-8: 48,664 wild duck, 44,568 teal and 2,119 wigeon, about **2,700 a season** **[firm]**. Ten decoys near Wainfleet sent 31,200 in one season, about 3,100 each (Pennant) **[firm]**. Modern working decoys average about 1,000 **[firm]** | at about 0.21 food a bird (Ashby's mix), 2,700 birds over about 150 days is 18 a day, about 3.8 food a day, **0.6 to 0.8 fau** for the decoyman **[estimate]**: steady, unlike the moult drive |
| **eggs and young at colonies** (heronries, rookeries, gulleries; the engine's `gather young`) | young herons (branchers), young rooks, gulls' eggs | the colony is the capital; a lord's or a parish's | 1 to a few | spring; tall trees, meres | see §1.1 | high in a short window |
| **the dovecote** | domestic pigeons (rock dove), squabs | a stone or timber cote of 500 to 700 nest holes (Garway 666, Palmer's Farm 657, Minster Lovell 600, Dunster 540 **[firm]**); a potence (a turning ladder) | 1, an hour or two a week | squabs from spring to late autumn | no medieval yield found. At 60% of holes in use and about 3 squabs a hole a year taken, a 600-hole cote gives about 1,000 squabs, **about 110 food a real year** **[estimate]**, for about 50 units: **about 2 fau**. The pigeons feed on everyone's fields | a lord's right in the Middle Ages: the grain it ate was the peasants' grievance (02zzj/02) |
| **swans** (marked on the bill, upped each summer) | mute swans | the right and the marks | crew at the upping | summer | a crown and lords' bird from the 12th and 13th centuries **[recalled]** | out of scope |

### 1.7 Processing the kill

| Step | What it gives | Work | Skill | Feeds |
|---|---|---|---|---|
| **gralloch and butchering** (field dressing, skinning, breaking up; the medieval ritual "unmaking" of the deer) | meat at dressing 0.57 to 0.68 and edible 0.70 to 0.75 of the carcass (02zzu part 1); offal (liver, heart, kidneys, lungs) about 5 to 8% of live weight; blood; fat; marrow | a red deer 1 to 2 hours skilled (0.5 to 1 unit); a roe about half an hour; a hare 10 to 15 minutes **[estimate]** | a novice loses 10 to 20% of the meat (gut punctures that taint, wasted cuts, bone left in) and cuts the hide **[estimate]** | food; offal for dogs and bait (the engine's carcass offal 0.25 of the meat) |
| **marrow and bone grease** (bones cracked and boiled) | 5 to 10% more kcal from a big beast **[estimate, ethnographic grease rendering]** | about 1 unit a beast | low | food, in a lean season |
| **rawhide** (scraped and dried) | lashings, thongs, snares for big game, drum heads, parchment's raw stuff | 1 to 2 units, days to dry | low | cord in place of fibre (§2.4) |
| **dressed skin**: brain-tanned and smoked buckskin, or **tawed** (alum and salt, egg yolk and flour; the medieval whittawyer's craft) | soft skins: clothing, gloves, bags, bellows, purses; furs are tawed | brain and smoke: 4 to 10 units a deer skin over a few days **[estimate, experimental practice]**; tawing days to weeks in the vat | medium | clothing; the skinner and the furrier |
| **bark-tanned leather** (lime to unhair, then layers in pits of oak bark liquor) | heavy leather: soles, harness, belts, buckets, bellows | light skins 3 to 6 months, heavy hides 12 to 18 months in the pits **[recalled]**; bark several times the hide's weight over a tanning **[recalled]** | a trade: the tanner | harness, packs, the anvil's bellows (economy_web §2.5); bark from the coppice (another note) |
| **fur** | pelts of fox, otter, pine marten, squirrel, rabbit (coney), wolf, beaver; prime only in winter | skinned whole or cased, stretched, then tawed | medium | warmth and trade; a 1363 statute kept the poor to lamb, coney, cat and fox fur **[recalled]**; a gown lined with squirrel took hundreds of skins **[recalled]** |
| **sinew** (the long back sinews and leg tendons, dried and shredded) | thread, bowstrings, bow backing, arrow and point binding | a deer gives 50 to 150 g dry **[estimate]**; a string takes about 15 to 30 g **[estimate]** | medium | cord for the bow and the snare (§2.4) |
| **gut** | strings (catgut), bowstrings, sausage casings | a day's cleaning and twisting | medium | strings |
| **hide glue** (scraps, hooves and sinew boiled down) | glue for bows, fletching, hafting | a pot over a day, about 10 to 15% of the scrap's weight **[estimate]** | low | the bow and arrow chain |
| **antler** (cast in spring, or from the kill) | combs, handles, picks, points, toggles, the horn to blow (engine: `make a horn` from antler) | a red deer stag's pair is 2 to 6 kg **[recalled]**; most medieval comb antler was gathered cast antler, not killed | medium; the comb-maker | tools; the Neolithic flint mines used hundreds of antler picks a shaft (02zzj/10) |
| **bone** | needles, awls, pins, skates, handles, dice, fish hooks | hours a piece | medium | sewing (the hide chain), fishing (hooks) |
| **horn** (cattle, sheep, goats; deer carry antler, not horn) | cups, spoons, combs, lantern panes | soaked, heated and pressed | a trade: the horner | the herds' chain more than the hunt's |
| **feathers and down** | fletching (goose wing feathers above all), bedding, quills | plucked with the bird | low | arrows: Henry V's writ of 1417 is said to have asked the sheriffs for six wing feathers from every goose **[recalled, unverified]**; a featherbed takes several kilograms, the down of 50 to 100 birds **[estimate]** |
| **tallow and lard** | light (rushlights), grease, waterproofing, bowstring wax | rendered at the hearth | low | deer are lean (a stag carries a few kg of suet in autumn **[recalled]**); boar and bear carry much; the engine already has tallow and tallow light |

---

## 2. The developmental structure

### 2.1 Not one ladder: what each kind of capital does

The methods do not stand on one ladder. Each kind of capital changes one factor of the take, and most combine:
- **Finding** (meetings a unit): knowing the ground, reading signs, a dog's nose, more eyes in a party, unhunted ground.
- **Closing** (the chance that a beast met is killed or held): the weapon, a dog that holds game at bay, a net, a noose.
- **Working while one is away** (time capital): snares, springes, deadfalls, pits, the decoy's pipes, the hay.
- **Gathering many at once** (a crew and a work): drives, hays, moult drives, the bow and stable.
- **Keeping** (the stock fed and guarded, culled rather than searched for): the park, the warren, the dovecote, the colony kept
  undisturbed.
- **Carrying and keeping the kill:** the pack, the pack ox, drying on the spot, salt.

Each step multiplies the factor it touches by about 2 to 5, never 10. The step after it is usually a different factor, not a
bigger version of the same one. This is Zach's "maybe you iterate and add new things, or maybe you completely switch paradigms".

### 2.2 What a person can do with what

| Means | Methods open | Real return (fau, including search) | What it needs |
|---|---|---|---|
| **nothing** | hands, stones, a stick; nests and eggs in spring; fowl in a great freeze; carrion; digging out | 0 to 0.3 most days; pulses of 1 to 3 | nothing; knowing where and when |
| **a few hours of one's own work** | a club or wooden spear (0.5 to 1 unit); 20 to 50 snares of cord or hair (1 to 2 units); deadfalls; springes | snares 0.4 to 1.2; weapon hunting as a novice 0.1 to 0.3 | cord or horsehair (another note's chain); a straight pole |
| **a season of one's own work** | a bow and a quiver (a stave seasoned, 4 to 8 units of making, arrows at 0.5 to 1 unit each, years of practice); a clap net; purse nets; a pot of bird lime | bow hunting, capable 0.4 to 1.2, master 1.2 to 3.2 | flax or sinew, feathers, glue, heads: five chains (§2.4) |
| **a household's keep** | a dog (0.3 to 1.3 food a day); ferrets; a kept call bird and stale for the clap net | raises finding and closing x1.5 to 3 **[estimate]** | food to spare every day, the year round |
| **a crew** | the drive; the moult drive; the bow and stable | the drive's crew bonus (built); the moult drive 3 to 8 fau, once a year | people who will turn out together; boats and nets for the moult drive |
| **a village's or a lordship's work** | the hay; a pit line; the decoy pond (17th c.); a kennel of hounds; a deer park; a warren; a dovecote | park: about 570 food a km² a year against about 50 to 120 wild; decoy 0.6 to 0.8 fau steady; dovecote about 2 fau | land enclosed and guarded; a keeper; law, or the threat of force, to stop others taking |

What Zach asks for, read off this table:
- **"Possible to do things with less layers, that have less beneficial outputs":** every row works without the row above it. A
  village with no cord still has deadfalls, clubs, digging out and eggs. A village with no smith still has the bow (fire-hardened or
  bone heads) and the drive with wooden spears.
- **"Completely switch paradigms after a certain capital amount":** two real switches. **Hounds and the park.** The cost of keeping
  them is so high (a pack eats like a hamlet; a park is kilometres of pale and a keeper) that only a large surplus can carry it, and
  then the yield of the land changes in kind. **Keeping in general.** The warren, the dovecote and the colony take the search away:
  the cull is a chore, not a hunt, and the ceiling is the stock the structure holds.
- **"Shallow":** the bow is the only piece of capital with a deep chain (stave, string, shafts, heads, feathers, glue). Everything
  else is one step from its material.

### 2.3 The very skilled hunter ([[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]])

What the evidence supports:
- **Near home, sustained:** a master's food a unit is 1.2 to 3.2 including search (02zzu), at the top of any wild living, but
  bounded by the land's yield (§4.4). Real hunting does not beat good farming an hour on good land. The master wins on land that
  cannot be farmed, in seasons with nothing to reap, and when away.
- **Far, on fresh ground:** naive, unhunted game is met more often and flees less. After encounter, deer run at 13 to 25 fau, so a
  meeting every 4 to 8 hours gives about **3 to 6 fau** **[estimate]**. Medieval evidence of the scale: the king's huntsmen were sent
  to named forests with hounds and nets to take tens of deer for a feast. Henry III's Christmas of 1251 drew 830 deer and 200 boar,
  taken over weeks across many forests **[firm, secondary]**. The day rate of such a professional team is not found here: perhaps
  about a deer a huntsman-day, about 20 food, 4 fau **[estimate]**.
- **The binding limits are the carry and the keeping, not the kill.** A red deer is 33 meat; a person carries about 20 to 25 kg,
  about 20 meat. So the trip's ceiling for one person is about 12 food carried. A pack ox (60) lifts it about three times, and
  drying on the spot (half the weight) about two times. This is already the shape of brief 4b: the party, the led ox, the carry.
- **The medieval ceiling, lower but not too low:** forest law, parks and the game statutes cut the common hunter off from deer, not
  from hares, rabbits outside the warren, or birds. A village with no lord (most engine worlds) is not under that ceiling. Where a
  lord is modelled, the law moves the commoner's take to snares, nets, birds and poaching, with the risk of being caught.

### 2.4 The chains that feed the hunt, and those it feeds

```
cord (bast, nettle, flax: another note) ─┬─> snares, springes ──> hares, rabbits, birds
horsehair (the herds) ───────────────────┤
sinew, gut (the kill) ───────────────────┘
                                          ┌─> purse nets, long nets ──(+ ferrets)──> rabbits
cord in quantity ─────────────────────────┼─> clap nets, flight nets, cockshoot nets ──> birds
                                          └─> the hay, the moult drive's funnel ──> deer, moulting duck
stave (yew, elm, ash: the wood note) ─┐
string (flax, hemp, sinew, gut) ──────┤
shafts (hazel, birch, ash shoots) ────┼─> BOW AND ARROWS ──> one hunter alone at range: deer, hares, birds
heads (fire, bone, flint, iron) ──────┤
fletching (goose and other feathers) ─┤
glue (hide glue) and binding ─────────┘
iron (the smith) ──> spear head, arrow heads, (later) the crossbow, the gin trap
food to spare ──> dogs (finding, holding, guarding), ferrets, hawks
oak, labour, law ──> the pale ──> the park; banks and pillow mounds ──> the warren; stone or timber ──> the dovecote

THE KILL ──┬─> meat (fresh, dried, smoked, salt: built)
           ├─> offal ──> dogs, bait (fishing, the traps), food
           ├─> hide ──┬─> rawhide (lashing, big-game snares)
           │          ├─> tawed or brain-dressed skin, fur ──> clothing, bags, bellows
           │          └─> bark-tanned leather (the tan pit: bark from the coppice) ──> harness, packs, bellows
           ├─> sinew, gut ──> bowstrings, thread, snares
           ├─> bone, antler ──> needles, points, hooks, handles, combs, picks, the horn
           ├─> fat ──> tallow ──> light (built), grease
           ├─> feathers ──> fletching, bedding
           └─> scraps, hooves ──> glue ──> the bow, the arrows
```

The loops worth having, because they bind: **the kill makes the next hunt's gear** (sinew to strings, feathers to fletching, glue to
the bow, offal to the dogs and bait). **The hunt and the herds share the hide chain.** **The bow is the one place where four
chains meet**, so a village that can make bows depends on a coppice (shafts), on fowl or geese (feathers), on cord or the kill
(string) and on hide (glue).

### 2.5 Law and season, only as they shape a village

- **Forest law** covered perhaps a quarter to a third of England at its height around 1200 **[recalled]**. It protected the
  "beasts of the forest" (red, fallow and roe deer, boar) and their cover. The Charter of the Forest (1217) ended the death
  penalty for taking deer **[recalled]**. Within a forest, mastiffs had three claws cut from a forefoot (lawing) so they could not
  run deer **[recalled]**.
- **Free warren** gave a lord the small game (hare, rabbit, pheasant, partridge) on his land **[recalled]**. **The 1389-90
  statute** (13 Ric. II) barred laymen with land worth under 40s a year from keeping greyhounds or other hunting dogs **[firm, in
  summary]**. In my recollection it also barred ferrets, hays, nets, hare-pipes, cords "and other engines" for taking deer, hares
  and conies **[recalled]**. Its complaint was that "artificers and labourers kept greyhounds and other dogs, and destroyed the game
  in parks and warrens".
- **Close seasons:** the 1534 act for the moulting wildfowl, and a later clause on their eggs **[firm]**.
- **Who ate it:** in the bones, wild game is a small share of medieval rural assemblages (red and roe deer each under 0.5% of
  identified bones at the West Cotton manor, Raunds **[firm]**), and a larger one at castles and other high-status sites after
  1066 **[firm, Historic England review; Sykes]**. Hunting fed the lord's table and his status. The peasant snared, netted birds and
  poached.
- **The season shapes the methods more than the law does:** deer in the rut (autumn), boar in the mast (autumn), fowl from autumn to
  winter, moulting duck in summer, nests and eggs in spring, fur prime in winter, snaring all year but best in winter. The engine's
  phenology already carries most of this.

### 2.6 Prehistoric and early-modern contrast

- **Mesolithic Britain** (Star Carr): red deer, roe, elk, aurochs and boar; bows and dogs; hunter-gatherer densities in temperate
  forest of about 0.05 to 0.2 people a km² **[recalled, Kelly's table]**. That fits §4.4's sustained yield.
- **Medieval:** the same methods divided by rank. Lords had hounds, parks, the drive and the bow and stable; commoners had snares,
  nets, lime and poaching. The new switches were keeping (parks, warrens from about 1100 when the rabbit came with the Normans,
  dovecotes) and the specialist (parker, warrener, huntsman, fowler).
- **Early modern:** the decoy pond (from about the 1620s, Dutch), wire snares, the gin trap, the fowling piece. The gun ends the
  bow's skill ladder: a lower skill floor, a higher take, and the game laws tightened in turn (1671). It is out of period, but it
  shows the shape: capital replaces skill.

---

## 3. Granularity for the engine ([[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]: general methods, not a technique per kind)

### 3.1 What exists (methods.py, 21 Nov)

`hunt the wild`, `stalk`, `drive`, `snare`, `net`, `trap in water`, `den work`, `gather young`, plus guarding and pest work.
Measured take tables (`yield.takes`, at load):
- hunt the wild: the deer, boar, hare, fox, stoat, wolf 0.99; bear and woodpigeon 0.33;
- stalk: red and roe 2.5, boar 0.3;
- drive: boar and wolf 3.0, red deer 0.45;
- snare: hare 3.0, fox, otter, stoat 2.0, roe 0.06;
- **net: salmon 3.0, wildfowl 3.0, woodpigeon 0.2**;
- trap in water: eel, lamprey 3.0, wildfowl 0.3;
- den work: bear, fox, stoat, wolf 4.0.

Gear: only `crude weapon`.

### 3.2 Keep, merge, add, leave out

| Method | Recommendation | Why |
|---|---|---|
| **hunt the wild** and **stalk** | **keep both.** Hunt the wild is the open search that takes what it meets; stalk is the slow approach to a beast that keeps to its paths | they differ in finding (sweep) and closing (weapon dependence), as built |
| **coursing** (greyhounds on hares, on open ground) | **not a method:** hunt the wild with a dog as gear, on open covers | a dog multiplies the hare's take on grass |
| **drive** | **keep.** Add the **hay** as a standing work at a wood's edge (a fitting with a hold, like the weir) that multiplies the drive there. **Bow and stable** is the drive with bows as gear | the hay is capital on the ground, not in the hand |
| **the moult drive** | **a season of the drive on water**, not a new method: wildfowl gain a summer row (`flee` about 0.1, `detect` up) while moulting; the drive's covers gain `water` and `fen`; nets as gear x3 to 5 | engine wildfowl are winter migrants only (`migrant: autumn, winter`); a resident moulting stock (mallard) is needed first. Flag: this pulse empties the next year's breeders (the 1534 close time) |
| **snare** | **keep one set-noose method** for snares, springes and nooses for birds: the set's target by trait (runs for mammals, walks for ground birds). Fold the **deadfall** in as the same set made of stone and sticks instead of cord: lower take, no cord | one method of "set something on a run and come back", whatever it is made of; the material decides the take |
| **pitfall** | **leave out**, or later as a village work in upland and boreal worlds | rare in a temperate lowland world; a weir-like work if it comes |
| **cage, box, gin traps** | **leave out** as food methods; the box trap can be pest work's tool | vermin, not food |
| **den work** | **keep**, with gear: a spade, a terrier, and **ferrets with purse nets** for burrows when rabbits come | ferreting is den work at a warren |
| **net** (fowling) | **split from fish.** The bird net needs a trait birds carry and fish lack: `flies: True` on wildfowl, woodpigeon and later larks and woodcock, with `needs: {"flies": True}`. Fish nets go to the fishing note's methods. Within fowling, **one method** with its gear deciding the setting: clap net and stale (open ground, by day), flight and cockshoot nets (at dusk, at water or a ride), bird lime (no cord). The **decoy pond** later as a fitting with a decoyman present | the engine's `net` takes salmon at the same weight as wildfowl today, from shared size and flock traits: a fish net and a fowling net share nothing but the knots |
| **gather young** | **keep and widen**: eggs (gulleries, wader and duck nests) and young (heronries, rookeries) in spring, by site or by density; the leaving rule ([[D2-198 Kinds answer people's scares in different ways|D2-198]]) as built | the spring pulse is one of the few things a person with nothing can take in quantity |
| **keeping: park, warren, dovecote** | **a package of its own** (kept wild stock in a structure: a fitting or a parcel state with a pale, a hold and a cull), with kept beasts, not hunting | the take is a cull of a fed, guarded stock; it is the paradigm switch, and it makes poaching |
| **hawking** | **leave out** for food; a status good later | small food, very long skill |
| **butchering** | **one technique for any carcass** (wild or slaughtered): skill decides meat yield (novice about 0.85, master 1.0 of the carcass's meat **[estimate]**), whether the hide comes whole, and which by-products come out (offal, sinew, fat, bone, antler) | economy_web §2.4 already proposes it |
| **hides** | **three ways, by what they make:** rawhide (dried: lashings), dressed (brain, smoke or tawing: soft skins and furs, days), tanned (bark pits: leather, months) | different inputs, times and products; one item per stage: hide, skin or fur, leather |
| **fur** | **not a good of its own kind:** the hide of a fur kind, prime in winter (a `prime` flag in its season), dressed | fewer goods (economy_web's rule 5) |
| **sinew, gut** | **one good, "sinew"**, from the kill, that counts as cord for strings, binding and snares | the hunt's own cord; it feeds back into the hunt |
| **bone and antler** | **one good** (antler exists; add bone) for tools: needles, points, hooks, handles, combs | hooks for the fishing note, needles for the hide chain, points for arrows |
| **feathers** | **one good**, from fowl and geese, for fletching and bedding | the bow's chain |

### 3.3 Weapons and kept beasts as gear (the multipliers of 4c §3.1)

| Gear | Methods it serves | Multiplier, first values **[estimate]** | Made from |
|---|---|---|---|
| crude weapon (built) | hunt, stalk, drive, den | as built: x2, x5, x6, x1.25 | 1 timber, 1 unit |
| **spear** (iron head) | drive, den, stalk at close range; lowers the boar's danger | x1.5 over the crude weapon on the drive and at bay | iron (the smith), a pole |
| **bow and arrows** | stalk (x2 to 3 over the crude weapon), hunt the wild (x2), birds on hunt the wild (opens them) | the bow's own skill curve: slower than the hunt's, with a higher top | a stave, a string (cord or sinew), shafts, feathers, glue; arrows wear |
| **dog** (cur or hound) | finding x1.5 to 2 on hunt, drive and den; flee x0.7 (held at bay); danger x0.5 | eats 0.3 to 1.3 food a day | a pup and a year's keep |
| **nets** (fowling) | the fowling method x3 to 5 over bare hands and lime; the moult drive | worn by use | cord in quantity |
| **ferret and purse nets** | den work at burrows | x3 to 5 | a kept ferret; cord |
| **pack, pack ox** (built) | the carry | as built | |

Leave the longbow as the bow at a higher skill, not a new item. Leave out the crossbow, the sling and the throwing stick (the last
two fold into bare hands and the crude weapon).

---

## 4. Numbers to calibrate against (on the engine's basis)

### 4.1 Food a unit, real (including search unless said)

| Way | Real fau | Source | Engine now (02zzu basis) |
|---|---|---|---|
| novice with a weapon, near | 0.08 to 0.32 | 02zzu, Hill et al. | 0.14 to 0.22 |
| capable hunter, near | 0.4 to 1.2 | Ache 0.6 to 1.0 (Hill et al. 1987); bowhunter 0.74 (Indian Head) | 0.51 |
| master hunter, near | 1.2 to 3.2 | 02zzu | 1.87 |
| master, far, fresh ground | **3 to 6 [estimate]**, capped by the carry (about 12 food a trip alone, about 3 times with an ox) | post-encounter deer 13 to 25 fau (Simms via Kelly) | 2.10 (4c far, before the basis) |
| after the encounter: deer; hare or rabbit; duck | 13 to 25; 10 to 13; 1.6 to 2.2 | Simms via Kelly | (no such rate in the engine) |
| snares on runs, lifted | 0.4 to 1.2; a set of 30 at 5 to 15 per 100 snare-nights | 02zzu; GWCT floor 3.5 to 8.5 per 1,000 | 0.64 |
| ferrets and purse nets | 0.5 to 2 at a medieval warren; 2 to 6 at plague densities | Bailey; NZ 1919 | none |
| clap nets for larks | 0.3 to 0.35 | 1912 claim, about 150 a day | none |
| the decoy (decoyman) | 0.6 to 0.8, steady over the winter | Ashby 2,700 a season; Wainfleet 3,100 | none |
| the moult drive | 3 to 8, a day a year | Willughby 4,000; Gough 3,000 | none |
| fowling with nets, general | 0.24 to 2.2 | 02zzu | 0.08 to 0.49 (low) |
| dovecote | about 2 (the pigeons feed off the fields) | estimate from nest holes | none |
| eggs at a gullery | 0.4 to 0.5 in the window | about 20,000 a year at Scoulton | none |

### 4.2 Skill and the tools

- Learning to hunt: capable in about a week of regular hunting, a master in about half an adult life (4c §3.3, as built). The bow
  should learn slower than the club and reach higher: years, from youth (the archery statutes).
- A bow: a stave seasoned months to a year; 4 to 8 units to make; arrows 0.5 to 1 unit each, often lost **[estimate]**.
- Butchering a red deer: 0.5 to 1 unit skilled; a novice loses 10 to 20% of the meat **[estimate]**.
- Dressing a deer skin by brain and smoke: 4 to 10 units over days. Bark tanning: 3 to 18 months, by the hide's weight **[recalled]**.
  How the compressed year shortens a months-long process is a question for the clocks ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]]); rule 7 of 02zzu scales only
  growth, breeding and the runs.

### 4.3 Upkeep of beasts as tools

- A hound: 0.7 to 1.3 food a day in work, 0.5 to 0.7 at rest; a farm dog 0.25 to 0.35; a ferret or a hawk under 0.1 **[estimate]**.
- A pack of 20 hounds eats like 15 to 25 people **[estimate]**. It pays only where offal and scraps are plentiful and the hunt is
  frequent.

### 4.4 The land's sustained yield, and the compressed year

Sustained yield of big game, a real year, good temperate habitat **[estimate: density x the share that can be culled x food a head]**:

| Kind | Density a km² | Cull a year | Food a km² a year |
|---|---|---|---|
| red deer | 8 (the engine's `ref`) | about 25% | about 40 |
| roe deer | 15 (`ref`) | about 35% | about 25 |
| wild boar | 4 (`ref`) | about 70% | about 50 |
| brown hare | 25 (`ref`) | about 50% | about 9 |
| all big game in a good wood | | | **about 50 to 120** |
| **a deer park** (Havering, about 2.3 a ha) | 226 | about 25% | **about 570** |

A person needs 365 food a real year, so wild game alone supports about **0.15 to 0.35 people a km²**. Real temperate
hunter-gatherers lived at 0.05 to 0.2, eating plants and fish too. The two agree.

**In the engine:** a village's ring is the land within 2.5 km (`RING_KM`), about 20 km² less the village's own land. At real
densities its sustained game is about 1,000 to 2,400 food a year. The engine's year is 32 days and breeding is scaled to it, while
each person still eats 1 food a day: 32 food a year. So **the ring's game feeds 30 to 75 people's whole diet in the engine, against
3 to 7 in reality: about 11.4 times (365 / 32)**. My reading of the code is that births are a head's real yearly rate at the start
of each 32-day year (`b` with `litters: burst`). That needs checking by 37.4, but it is consistent with 4c's miss (2): a master
hunting one wood daily for 16 days held 2 to 3 a unit, because the ring holds about 230 large beasts.

This is the same gap the runs met, and they were closed with a named lever: run sizes x 32/365 by catchment (02zzu part 6, [[D2-259 The food values are anchored on real values|D2-259]]).
For game there are two options:
- **(a)** Keep standing densities real, so the rate a trip stays real, and scale the year's recruitment, or the surplus that
  hunting can take, by about 32/365.
- **(b)** Accept the generosity as a design departure, so hunting can feed a hamlet, and name it.

It is Zach's call (§5). The calibration suite measures red deer at 2.1 to 2.4 a km² over the whole land (02zzt §4), below the good
habitat `ref` of 8, so a world's real sustained yield is nearer the low end. That does not change the factor of 11.

### 4.5 Winter wildfowl on a fen or a water meadow

| Place | Area | Waterbirds (peak, winter) | A km² |
|---|---|---|---|
| Somerset Levels and Moors SPA | about 64 km² **[recalled]** | 73,014 (5-year peak mean to 1998) and 97,155 (1998-99 to 2002-03), of them about 36,000 lapwing and 13,700 wigeon **[firm]** | about 1,100 to 1,500 (ducks alone perhaps 400 to 500) |
| Ouse Washes SPA | 2,469 to 2,513 ha **[firm]** | over 20,000 (Ramsar criterion) **[firm]**; single Welney counts of 3,000 to 6,000 wigeon in a winter **[firm]** | about 800 or more |
| ten decoys near Wainfleet (pre-drainage Lincolnshire fen) | unknown | 31,200 taken in one season **[firm, Pennant]**: the standing flock was several times that | |
| a whole wet district, averaged, pre-drainage | | | **about 50 to 300 [estimate]** |

These are refuges: the birds roost there and spread out to feed by night, so a refuge's density is an upper bound and a district
average is far lower. **The engine:** wildfowl arrive at 150 a km² of wet habitat (`arrive`), and the suite measured 4 to 52 a km²
averaged over whole areas (02zzt §4). The first is in the real district range; the second is fair for mixed land and low for a
true fen. The brief's "about 8 birds an area" sits at the bottom of the real range for any wet ground: 10 to 100 times below a fen
in a hard winter. The cold's push (PUSHED `most` 4.0, onto the last open water) gives the concentration the real refuges show, and
should be kept. A mallard is 0.31 food, so a winter fen at 200 ducks a km² holds about 60 food a km² standing, and a decoy takes
about 3,000 a season from what is likely tens of km² of feeding ground.

### 4.6 The values to hold (the short list)

1. Food a unit = kcal an hour ÷ 1,250.
2. Hunting including search: novice 0.08 to 0.3, capable 0.4 to 1.2, master 1.2 to 3.2; far on fresh ground 3 to 6 **[estimate]**,
   capped by the carry.
3. After encounter: deer 13 to 25 fau, hare 10 to 13, ducks 1.6 to 2.2.
4. Kill frequency: Ache game on 48% of days; a bowhunter's deer every 35 hours (about 17 units); Hadza big game on 1 to 3% of days.
5. Snares: 0.4 to 1.2 fau; 5 to 15 catches per 100 snare-nights on known runs **[estimate]**.
6. Ferrets: up to 60 to 100 rabbits a day at pest densities; medieval warrens culled no more than about 3,000 a year.
7. The decoy: about 2,700 to 3,100 ducks a season (Ashby; Wainfleet), about 0.7 fau; the moult drive 3,000 to 4,000 in a day.
8. Winter wildfowl: 400 to 1,500 waterbirds a km² at refuges, 50 to 300 over a district.
9. A deer park: about one deer an acre (Havering), about 570 food a km² a year, against 50 to 120 wild.
10. A hound eats 0.7 to 1.3 food a day; a pack of 20 like a hamlet.
11. Sustained game supports 0.15 to 0.35 people a km² real; the compressed year multiplies it about 11 times per mouth.
12. Butchering a deer is 0.5 to 1 unit; a novice loses 10 to 20%.

**[[D2-259 The food values are anchored on real values|D2-259]] (real values within about 20%):** the food a head of game is already on the basis. The departures to name are:
- the compressed year's sustained yield (x11, §4.4);
- the engine's net fowling (0.08 to 0.49 fau, under the real 0.24 to 2.2);
- the far master's carry, if the master far is to be "disproportionate".

---

## 5. Open questions (for Zach, and for 37.4 where marked)

1. **The compressed year and the game (the most important).** At real densities, the engine's year makes the ring's game feed
   about 11 times as many people as reality. Should recruitment, or the cull that the land can bear, be scaled by 32/365 as the runs
   are, keeping the rate a trip real? Or should hunting stay generous by design, as a named departure? 37.4: confirm the reading of
   births and deaths per 32-day year.
2. **The master far ([[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]):** is 3 to 6 fau on fresh ground, capped by the carry (12 food a trip alone, more with an ox and drying
   on the spot), the "disproportionate" that is wanted? Or should the cap rise, for instance with a party's shared carry?
3. **Split `net`:** add a `flies` trait for birds, so fowling no longer takes salmon. This touches the water note's fish nets; the
   split should be agreed with that note's owner.
4. **Keeping as a package** (park, warren, dovecote, managed colonies): build it with kept beasts, or later? It is the real paradigm
   switch, but it needs exclusion (a pale), a hold, a keeper, and someone to stop others.
5. **The bow:** one item with its own, slower skill curve and a higher top, depending on five chains? Or wait until cord, feathers
   and glue exist (stage 4 of economy_web puts the bow late)?
6. **Dogs:** one kept beast (`dog`) with a hunting use beside its watch, costing food every day; or two (cur, hound)? Does the
   1390 statute's kind of limit (who may keep hounds) belong in worlds with lords?
7. **The moult drive and a resident duck:** add a resident, moulting wildfowl stock for the summer pulse (and the close season that
   real law set against it)? Or keep wildfowl as winter migrants only?
8. **Rabbits:** the hare stands in for the rabbit today. Warrens, ferrets and purse nets only make sense with a rabbit (a Norman
   introduction in England): add it with keeping, or never?
9. **Butchering with skill:** a novice at about 0.85 of a master's meat, and by-products (sinew, bone, fat, a whole hide) only
   above some skill? This is economy_web §2.4's proposal, and the values here are estimates.
10. **Hide in three stages** (rawhide, dressed skin or fur, tanned leather): how do months-long processes (tanning 3 to 18 months)
    sit in the 32-day year? This is a clocks question for 37.4 ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]]).
11. **The hay and the decoy as standing works**, like the weir (a fitting with a hold that multiplies a crew's or a keeper's take)?
    Or leave them out until lords and keepers exist?
12. **Fowling's food a unit** in the engine (0.08 to 0.49) is below the real range (0.24 to 2.2): raise `take_base` for fowling,
   or the density in fen and water areas, once the net is split?

---

## Sources

Seen in this session (search summaries; full texts not reachable from this session for wwt.org.uk, bahs.org.uk and gutenberg.org):
- Hawkes, O'Connell and Blurton Jones 1991, *Phil. Trans. R. Soc. B* 334: Hadza large game on about 3% of hunter-days, trapping a
  catch on 1 day in 3 over 102 hunter-days; Wood and Marlowe 2013 (0.97%). Via [Hawkes et al. 2010](https://content.csbs.utah.edu/~hawkes/Hawkes_al10notJustprovisioningG&Hcorrec.pdf), [Springer 2013](https://link.springer.com/doi/10.1007/s12110-013-9173-0).
- Hill et al. 1987, Ache foraging: [PDF](https://content.csbs.utah.edu/~hawkes/Hill_al87ForagingAcheOFT.pdf); Ache game on 48% of days (Hill and Kintigh 2009).
- Simms, Great Basin post-encounter returns, via Kelly; repeated in `02zzj_economy_research/10` §1.3.
- Indian Head bowhunting study: 35 hours per recovered deer ([SEAFWA, wounding rates](https://seafwa.org/sites/default/files/journal-articles/Pedersen-31-34.pdf)).
- GWCT and Defra snare trials: [results compared](https://www.gwct.org.uk/media/199147/defra_and_gwct_snare_studies_compared_by_results_1.pdf).
- Rabbit warrens: [Norfolk Heritage Explorer](https://nhe.esdm.co.uk/theme/tnf2329) (Bailey: few warrens over 3,000 a year;
  Gooderstone 348 in 1370); [Suffolk HER, Brandon Warren](https://heritage.suffolk.gov.uk/Monument/MSF13407); Blythburgh about
  1,000 a year in the 1460s.
- Ferreting rates: [Papers Past, 1919](https://paperspast.natlib.govt.nz/newspapers/LCP19190717.2.21); [National Museum of Australia](https://nma.gov.au/explore/features/rabbits-in-australia/your-stories).
- Duck decoys: Ashby 1833-68 and Pennant's Wainfleet figure, [Essex Field Club archive](https://essexfieldclub.org.uk/archivetext.php/s/028/o/0215);
  moult drives (Willughby 1678, Gough 1720) and the 1534 act, [Essex Field Club](https://essexfieldclub.org.uk/archivetext.php/s/003/o/0162);
  Borough Fen decoy 1776-1959 ([Wildfowl](https://wildfowl.wwt.org.uk/index.php/wildfowl/article/view/128), not opened); modern
  decoys about 1,000 a season (WWT review).
- Larks: [Dunstable larks](https://dunstabledownsgolf.co.uk/dunstable-larks); Mayhew, [London Labour and the London Poor](https://dl.tufts.edu/teiviewer/parent/rv043431c/chapter/c2s6);
  [Massacre in Larkland](https://www.hertsmemories.org.uk/content/herts-history/towns-and-villages/royston/massacre-in-larkland).
- Cockshoots: [Wikipedia, Cockshoot](https://en.wikipedia.org/wiki/Cockshoot); [Yorkshire dictionary](https://yorkshiredictionary.york.ac.uk/words/cockshoot) (North Duffield, 1473-4).
- Dovecotes: [Palmer's Farm](https://www.exploringbuildinghistory.co.uk/statement-dovecotes-part-1-15th-c-pigeon-house-at-palmers-farm-wilmcote/), [Dunster](https://en.wikipedia.org/wiki/Dunster_Dovecote), [Minster Lovell](https://historicengland.org.uk/services-skills/education/educational-images/dovecote-at-minster-lovell-manor-minster-lovell-10671).
- Deer parks: [Havering's 1,200 deer on 1,300 acres](https://essexfieldclub.org.uk/archivetext.php/s/229/o/0036); [Wikipedia, Deer park (England)](https://en.Wikipedia.com/wiki/Medieval_deer_park) (Rackham's 3,200 parks, 2%);
  Birrell 1992, *AgHR* 40 ([medievalists.net summary](https://www.medievalists.net/2008/11/deer-and-deer-farming-in-medieval-england/)); Sykes et al. on fallow deer ([NORA](https://nora.nerc.ac.uk/id/eprint/516876/)).
- Domesday hays: [Domesday materials, enclosure](https://sites.google.com/site/domesdaymaterials/domesday-book/data-terminology/manors/enclosure); [Little Wenlock, VCH](https://prod.british-history.ac.uk/node/11396).
- Henry III's Christmas 1251 and royal deer: [National Archives](https://www.nationalarchives.gov.uk/explore-the-collection/explore-by-topic/arts-and-culture/historic-food-and-drink-at-christmas/); [Cambridge chapter on royal consumption of deer](https://resolve.cambridge.org/core/books/studies-in-medieval-and-renaissance-history/royal-consumption-and-gifts-of-deer-in-thirteenthcentury-england/BBE3F558EA490CB9D3B3F23E45BAD63E).
- The 1389-90 statute: [Robin Hood Legend, the decline of the forest](https://robinhoodlegend.com/?p=5411).
- The Master of Game (Edward of York, c. 1406-13): [Wikipedia](https://en.wikipedia.org/wiki/The_Master_of_Game); [Medieval hunting](https://en.wikipedia.org/wiki/Medieval_hunting).
- Zooarchaeology: [Historic England, central England review](https://historicengland.org.uk/research/results/reports/7896/AReviewofAnimalBoneEvidencefromCentralEngland); Albarella and Davis 2010; Sykes 2001 thesis ([Southampton](https://eprints.soton.ac.uk/464572/)); [Sykes, Fair game](https://www.tandfonline.com/doi/full/10.1080/00438243.2016.1269666).
- Wildfowl: [Ramsar, Ouse Washes](https://rsis.ramsar.org/ris/77); [WWT Welney counts](https://www.wwt.org.uk/wetland-centres/welney/wildlife/latest-sightings/wetland-bird-survey-wwt-welney-and-ouse-washes); Somerset Levels and Moors ([BirdLife](https://datazone.birdlife.org/site/factsheet/somerset-levels-and-moors-iba-united-kingdom/details); [Ramsar sheet](https://rsisd7.unepgrid.ch/RISapp/files/RISrep/GB914RIS.pdf)).
- Gulls' eggs: [Wikipedia, Gull egg](https://www.wikipedia.org/wiki/Gull_egg); [Country Life](https://www.countrylife.co.uk/food-drink/delicacy-black-headed-gulls-eggs-84813).

Recalled, not re-opened here: Kelly, *The Lifeways of Hunter-Gatherers* (2013), densities and small-game rates; Cummins, *The
Hound and the Hawk* (1988), hound allowances; Rackham, *The History of the Countryside*, forest law's extent; the archery statutes
of 1512 and 1541; the 1363 sumptuary statute; the 1417 goose-feather writ; tanning times; antler weights; Scandinavian elk pits.

In the repository: `proposals/hunt_calibration.md`, `wildlife.md`, `economy_web.md`; `02zu`, `02zzu`, `02zzt` §4; `02zzj` 01, 02,
03, 10; `cybertron2/wild/methods.py`, `kinds.py`, `areas.py`; `cybertron2/engine/data.py`.

## History

- 21 Nov 2026: written by a research agent for 37.2 ([[W-73 Fishing, hunting and their materials developed together|W-73]]), alongside the fishing, fibre, wood and engine-audit notes in this
  folder. No code changed; nothing decided.
