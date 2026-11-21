# Fibre, cord, twine, line and net: the supply chain (W-73)

Session 37.2, 21 Nov 2026. A research and design-input note for the thread on fishing, hunting and their materials developed
together (W-73), which gathers the hunting and resources build (OPEN L-111) and the deferred nets (OPEN L-13). Zach (21 Nov):
gear should cost real materials, and the benched resources "like cord and withies" are to be explored, "the different levels and
granularities and ladders and supply chains / developmental processes of techniques and tools and capital". This note covers
**fibre, cord, rope, twine, line and net** only; fishing, hunting and fowling, withies and coppice wood, and the engine audit are
other notes in this folder. It proposes; nothing here is decided.

**Read first:** `proposals/economy_web.md` §1 and §2.9 (cord: "shallow, then a paradigm switch"), `economy_later.md` (nets
deferred: "fibre is deferred"), `recipes.md` §6 (wear: a trap 20 nights), `tools.md`, `02zu_wild_chains_capital_actions.md`
(cordage "none" in the engine; the net-maker's needle as a tool that makes tools), `02zzj_economy_research/01` §4.4, `03` §5 and
§7, `10` §1.3. **Code read:** `cybertron2/engine/data.py` (ITEMS, TECHNIQUES), `cybertron2/wild/methods.py` (METHODS, SETS),
`cybertron2/wild/plants.py`.

**What the engine has now.** No cord, fibre, flax or rope anywhere in the code. The fishing rod is made of `timber 0.5, hide 0.1`
(the comment says "a line of hair or gut"). The snare line (5 nooses, 4 nights), the fowling net (`net`) and the wicker trap in
water are methods with **no gear and no inputs**: they cost only the units of setting. Nettles exist only as food, inside "wild
greens". The work basis: a unit of work is 2 hours, a day 5 to 7 units, a year 32 days (8 a season), so **a person's engine year
is about 190 units, some 380 hours**, against 2,500 to 3,000 real working hours.

**Marks.** **[f]** a published figure seen this session (in a search result); **[k]** from the literature as I know it, not
re-checked this session (check before it goes into data); **[e]** my estimate or calculation, with the working shown. Fetching
pages was blocked in this session (the proxy refused chestofbooks.com, vikingeskibsmuseet.dk and gutenberg.org), so the [f]
figures are from search abstracts; the hosts would have to be allowed to read the full texts.

---

## 0. Findings in brief

1. **Cord is labour, not land, until flax.** Wild fibre (nettle, lime and willow bast) is everywhere and free, but slow: about
   **15 to 50 g of nettle fibre an hour** of picking and stripping [f, practitioners], then hand-twisting at a similar rate. A kg
   of wild cord is **about 35 to 80 hours** [e]. A snare line needs 15 to 20 g of it, an hour's work; a net needs a kilogram or
   more, which is a fortnight.
2. **Flax (and hemp) moves the cost from finding to growing.** A field gives fibre in bulk: **450 to 550 kg of scutched flax a
   hectare** in 19th-century Ireland [f], perhaps 250 to 400 kg in a medieval field [e]. Fibre then costs **about 4 to 7 hours a
   kg** [e], against 20 to 60 for wild nettle. But it takes land from grain, fouls the water it is retted in (laws forbade it in
   rivers and common ponds [f]), and pulses through the year: sown in spring, pulled in summer, retted, dressed in autumn, spun in
   winter.
3. **Spinning is the bottleneck once fibre is cheap.** By the weight of cord, coarse 2 to 3 mm cord spins at about 10 to 15
   hours a kg on a spindle [e]; fine net twine (under 1 mm) at 50 to 80 hours a kg [e], because spindle output is roughly fixed in
   metres (40 to 100 m an hour [k, Kania]). Fineness, not weight, sets the price of a gill net.
4. **Netting is slow and countable.** A netter ties **350 to 1,300 knots an hour** [f: 350 for a modern craftsman, about 1,300
   on fine string in a Victorian workshop text, about 900 in a practitioner guide]; 600 to 900 is a fair working rate [e]. A small
   gill net (20 m by 1.5 m, 7 cm mesh) is about 14,000 knots and 1 kg of cord: **some 55 to 70 hours in all, about 30 units** [e].
   A small river seine is ten times that.
5. **Nets rot.** Untreated bast or linen in water lasts weeks to a season [k]; barked (boiled in oak-bark tannin) or tarred, it
   lasts several seasons if re-barked through the season [f, k]. Barking ties the net to the tanner's bark and a pot.
6. **The ladder is shallow, and the floor is old.** Three-ply bark cord is about 41,000 to 52,000 years old (Abri du Maras [f]);
   knotted bast nets are Mesolithic (Antrea, about 8300 BC, willow bast, 27 to 30 m by 1.3 to 1.5 m, 6 cm mesh [f]); Neolithic
   lake villages made fine gill nets of flax yarn while keeping lime bast for coarse work [f]. So: **two rungs** in the engine
   (wild cord; flax cord), with rope walks and the roper later.
7. **Recommendation:** one good, **cord**, plus **flax** as the field's harvest. Four techniques (twist cord; ret flax; dress
   and spin; make a net), a gear item or two (a net; snares), and a mend (bark the net). Retting in running water fouls the
   parcel for fish: the cord that makes nets spoils the water the nets are set in, which is the kind of interlock the scenario
   guide asks for.

---

## 1. Fibre sources and their chains

Rates are per person. "Fibre" means cleaned fibre ready to twist or spin. Durability is of the finished cord in use.

| Source | Where, when | Chain | Fibre yield | Labour to fibre | Strength and durability | Period | Sources |
|---|---|---|---|---|---|---|---|
| **Nettle** (*Urtica dioica*) | rich ground, woods' edges, middens, alder carr; cut Aug to Oct after flowering, or winter stems retted standing | cut; strip green (peel the skin off the woody core) or ret and break; scrape; twist | about **1 g of good fibre a stem** [f, practitioners]; cultivated clones 8 to 16% of stalk dry matter, 0.3 to 1.0 t fibre a ha [f, Hartl and Vogl 2002]; wild stands lower and patchy [e] | **1.2 to 4 minutes a stem** to pick and peel [f, practitioners]: 15 to 50 g an hour, **20 to 65 h a kg** | long, fine, strong (near flax) [k]; rots in water untreated as flax does | Neolithic to early modern (Bronze Age Danish nettle cloth; La Draga cordage of nettle and lime [f]) | Pointer 2021; Hartl and Vogl; Herrero-Otal et al. 2023 |
| **Lime (linden) bast** (*Tilia*) | young lime, or coppice poles; strip in **May to June** when the sap runs | strip bark; **ret in still water 2 to 8 weeks** [f, practitioners; 6 weeks in a tub]; peel the layers; dry; twist or plait | a pole's bark gives a few hundred g of bast [e] | stripping is quick; peeling and cleaning the retted layers some 10 to 20 h a kg [e] | coarse, stiff dry, good wet; **hemp's breaking load is about three times bast's**, and bast "does not respond well to being twisted" [f, Viking Ship Museum, Gislinge rig] | Mesolithic to the 19th c. (Russian bast shoes, mats, ship's rope); Ötzi's sheath and cords [k] | Viking Ship Museum; Karg 2022; Jack Raven (6 weeks) |
| **Willow and other bast** (willow, oak, elm; clematis bark) | wet ground, river banks; spring and summer | as lime | as lime [e] | as lime [e] | weaker than lime [k] | the Antrea net is willow bast [f]; oak bast nets Neolithic [f] | Antrea; Hornstaad literature |
| **Conifer inner bark** | pine, spruce | strip, split, twist | | | | the Abri du Maras 3-ply cord, 41 to 52 ka [f] | Hardy et al. 2020 |
| **Rushes, sedges, grass, straw** | fens, meadows; straw from the grain harvest | twist green or dry, by hand or a twister (a "thraw-hook") | unlimited near fen and field | very fast: tens to hundreds of metres an hour of thick rope [e] | weak, short-lived, rots; for thatch, stacks, bundling, seats [k] | always | ethnography of straw and hay rope [k] |
| **Flax** (*Linum usitatissimum*) | a field or close on good, manured, weeded land; **sown March to April, pulled about 100 days later (July to August)** [k] | pull (not cut, to keep the fibre's length); ripple off the seed; **ret** (water 1 to 2 weeks; dew 3 to 6 weeks) [k]; dry; break; scutch; hackle (line and tow); spin; ply | 19th-c. Ireland **28 to 35 stones of scutched flax an acre** (14 lb stones: 180 to 220 kg an acre, **450 to 550 kg a ha**) [f, Hansard 1906, 1921]; medieval perhaps 250 to 400 kg a ha [e] | field work 1.5 to 2 h a kg of fibre; break, scutch and hackle 2 to 4 h a kg [e]: **4 to 7 h a kg** | strong (2 to 3 times lime bast [e from the hemp figure]); untreated linen net in water a season [k]; barked, several | Neolithic (Hornstaad gill net of plied flax yarn, about 3900 BC [f]) to now | Hansard; Hornstaad (Propylaeum); König 2020 (EXARC) |
| **Hemp** (*Cannabis sativa*) | "hemp-yards" and "hempland" closes by the house, heavily manured [k]; sown May; the male plants pulled in August, the female in September to October [k] | as flax; coarser; dressed by hackling; rope walks | of the order of flax or more [k] | as flax [e] | the strongest; rope, sail, sacking, nets; tarred rope lasts years [k] | grown in England since at least AD 800 [f, Hall]; peak in the 16th c. [f] | Hall (medieval hemp processing in eastern England) |
| **Horse hair** | horses' tails (white for lines, Berners) | pull, sort, twist or plait in links | a few hundred g a tail [e] | an hour or two for a rod line [e] | good in water; the angler's line until silk-worm gut (17th to 18th c.) and silk [k] | medieval to early modern | Berners 1496 [k] |
| **Sinew** | the carcass (the back strap and leg tendons) | dry, pound, split into threads, twist | perhaps 50 to 100 g of dry sinew a deer [e] | a few hours a carcass [e] | very strong, stretches and fails when wet: bowstrings, sewing, bow backing, not fishing [k] | prehistoric; the steppe | Plains and Miwok ethnography [f, qualitative only] |
| **Gut** | sheep and cattle intestines | clean, split, twist, dry | | | strong dry, poor wet; bowstrings, harps, sieves [k] | ancient to modern | [k] |
| **Rawhide thong** | any hide | cut in a spiral; stretch | a cow hide gives tens to hundreds of metres of thong [k] | a few hours a hide [e] | strong, stretches wet, rots; lashing, harness, heavy snares [k] | always | [k] |
| **Wool, goat hair** | sheep, goats | spin | | | stretches and weakens wet; not for fishing; goat hair rope in the Mediterranean [k] | | [k] |

**What this says.** For a temperate village the real choices are **nettle and lime bast in the wild** and **flax and hemp on the
land**. Rushes and straw make weak rope for the farm and roof; horse hair makes fine fishing line and bird nooses where there are
horses; sinew, gut and rawhide are joint products of the carcass good for bowstrings and lashing but poor in water. Fishing gear is
in water, so the plant fibres win.

---

## 2. The steps, with labour

Per person, by hand, unless said. The hours are for a competent worker.

| Step | What it is | Rate | Notes | Sources |
|---|---|---|---|---|
| gathering wild fibre | nettle stems cut and green-stripped; bast stripped from poles | nettle 15 to 50 g of fibre an hour; bast faster to strip, slower to clean [e] | nettle best late summer; bast only in sap time | [f] Pointer; [e] |
| **retting** | soaking or dewing the stems so bacteria free the fibre from the woody core and the gums | **water: 1 to 2 weeks** in warm water (flax); **dew: 3 to 6 weeks** on grass, turned [k]; lime bast 2 to 8 weeks [f] | mostly waiting; a few hours a batch to sink, weight, lift and spread [e]. Fouls the water: oxygen used up, smell, dead fish | [k]; Severn Act 1678 [f] |
| breaking | crushing the dried stems in a wooden brake | 5 to 15 kg of straw an hour [e] | often men's work [k] | [e] |
| scutching | beating the broken stems with a wooden blade over a board to drop the shives | perhaps 5 to 10 kg of fibre a day by hand [e] | Irish growers often scutched by hand rather than use the mill [f, ILN 1859]; mill scutching from the 18th c. | [f] ILN; [e] |
| hackling | combing through iron-toothed hackles to split and straighten; separates long line from short tow | a few kg an hour [e] | the hackle is a smith's product: iron teeth in a board | [k]; Chatham had a hatchelling house [f] |
| spinning | twisting fibre into yarn on a drop spindle (distaff and spindle; the wheel from the 13th c. [k]) | **40 to 100 m of yarn an hour** [k, Kania; repo 03 §5.2] | rate is roughly fixed in metres, so coarse yarn is cheap by weight and fine yarn dear | [k] |
| plying | twisting two or three yarns together the other way | about twice the singles' rate in metres [e] | a 2-ply twine costs about 2.5 times one yarn's spinning [e] | [e] |
| twisting by hand | thigh-rolling or reverse-wrapping fibre straight into 2-ply cord, no tool | **5 to 10 m an hour of 3 mm cord** (about 25 to 50 g an hour) [e] | the floor: no spindle, no field | [e] |
| laying rope | on a rope walk: yarns spun walking backward from a turned hook, then strands laid into rope with a top | many times faster per kg than a spindle [k]; the walk's length sets the rope's length [f] | a trade (the roper); Bridport rope from the 13th c. [k]; Chatham's rope house about a quarter-mile long [k] | Ryan 2011; Ure [f] |
| **net-making** (braiding, knitting) | knotting meshes over a gauge with a loaded netting needle | **350 to 1,300 knots an hour** [f]; take 600 to 900 [e] | the knot count is what costs (below); the gauge sets the mesh | Workshop Receipts; Indiana Traditional Arts; Mother Earth News [f] |
| mounting | lacing the netting to head and foot ropes, floats and sinkers | 3 to 5 hours a small net [e] | floats of wood or bark (cork imported), sinkers of stone or clay (lead later) | [e] |
| **barking or tarring** | boiling nets and sails in an infusion of oak bark (tanbark; cutch later), or tarring | a few hours a batch [e]; repeated through the season [k] | "sails, ropes and nets keep much longer" treated with tannin [f]; oak or hemlock bark if no cutch [f, NOAA]; barking kettles in fishing villages [f, Newfoundland] | NOAA leaflet 66; Heritage NL |
| mending | re-knotting torn meshes | 10 to 20% of the netting time over a season [e] | done by men on the shore, women at home [k] | [e] |

**Labour per kg of finished cord** [e, from the rows above]:

| Path | Fibre | Spin and ply, or twist | Total per kg | Engine units per kg |
|---|---|---|---|---|
| wild nettle or bast, hand-twisted 3 mm 2-ply | 15 to 60 h | 20 to 40 h | **35 to 80 h** | 18 to 40 |
| flax, spindle-spun coarse 2 to 3 mm 2-ply | 4 to 7 h (field and dressing) | 10 to 14 h | **15 to 20 h** | 7 to 10 |
| flax, spindle-spun fine net twine (under 1 mm, 2-ply) | 4 to 7 h | 50 to 80 h | **55 to 85 h** | 28 to 43 |
| hemp on a rope walk (rope, 10 mm and up) | 4 to 7 h | 1 to 3 h | **5 to 10 h** | 3 to 5 |

So flax makes coarse cord about **three times cheaper** than wild cord, and rope on a walk ten times; fine twine stays dear on
any fibre because spinning metres is the cost.

---

## 3. What the gear takes

**Netting arithmetic** [e]. For a diamond mesh with bar length *a* (the stretched mesh is 2*a*), hung at the usual ratio of 0.5,
one mesh covers about 1.73 *a*² of net, so there are 1 / (1.73 *a*²) knots a square metre, and each mesh takes about 2*a* of twine
plus some 2 to 3 cm for its knot. At a 7 cm stretched mesh (*a* = 3.5 cm): **about 470 knots and 45 m of twine a square metre**.
At 4 cm: about 1,440 knots and 87 m.

| Gear | Size | Cord | Work | Engine (1 unit = 2 h) | Notes |
|---|---|---|---|---|---|
| **a snare** | a noose of 0.5 to 0.6 m and a tether, on a peg | about 1 m of 2 mm cord, **3 to 4 g** | 10 minutes with cord in hand | | horse-hair nooses (springes) for small birds, 2 to 6 hairs [k]; wire snares are 19th-c. |
| **a line of 5 snares** (the engine's `line: 5`) | | **15 to 20 g** | 1 h to make, plus the cord (0.5 to 1.5 h wild) | **cord 0.02 + 1 unit** | a snare survives a few settings: chewed, broken, lost [k] |
| **a rod line** | rod length plus a few metres | horse hair: a few g; Berners grades lines by hairs, from one for the minnow up to about fifteen for the salmon [k, check the text] | 1 to 2 h to plait or twist | **cord 0.01** in place of `hide 0.1` | the hook is the costly part (bone, then metal) |
| **a hand line** | 10 to 20 m of 1 mm twine | **10 to 20 g** | 1 to 2 h | cord 0.02 | |
| **a bowstring** | about 1.8 m of 4 mm, 3-ply | **15 to 25 g** | 1 to 2 h | cord 0.02 | linen or hemp in the English longbow (Ascham, 1545 [k]); sinew or gut elsewhere |
| **a hoop or dip net** | 1 to 2 m² on a withy frame | 0.1 kg | 3 to 4 h | cord 0.1 + 2 units (+ withies) | |
| **a gill (set) net** | 20 m by 1.5 m hung, 7 cm mesh | twine 1,300 m (0.5 kg) + head and foot ropes 40 m of 4 mm (0.5 kg): **about 1 kg** | knots 14,000 (16 to 24 h) + mounting 4 h + fine twine's extra spinning 20 to 30 h = **40 to 60 h** beyond the cord | **cord 1 + 25 units** | Antrea was 27 to 30 m by 1.3 to 1.5 m at 6 cm [f]: this size |
| **a fowling net** (one clap or drop net) | 10 m by 2 m, 4.5 cm mesh | twine 1,500 m (0.5 kg) + lines 0.3 kg: **about 0.8 kg** | knots 23,000 (25 to 40 h) + mounting + fine spinning = **50 to 70 h** | **cord 0.8 + 30 units** | plover and lark nets were worked in pairs [k] |
| **a small river seine** | 60 m by 2 m, 4 cm mesh, with a bag | twine 10 km (5 kg) + ropes 120 m of 8 mm (5 kg): **about 10 kg** | knots 170,000 (190 to 280 h) + fine spinning 200 h + ropes = **about 500 h** | **cord 10 + about 200 units** | a household's winter or a crew's capital; real seines were often larger [k] |
| **a well rope** | 20 m of 12 mm | **about 2 kg** | wild: 70 to 160 h; flax by spindle: 30 to 40 h; a walk: 10 to 20 h | cord 2 | rope as cord by weight |

The units in the "Engine" column count only the making beyond the cord itself; the cord's own work is in §2's last table.

---

## 4. Durability

- **Untreated plant cord in water** rots in weeks to a season [k]: bacterial decay, and "breakings become more numerous when the
  net is weakened by rotting" [f, Taylor's net preservation report].
- **Barked or tarred** nets last **two to four seasons** with re-barking during the season [k, e]; tanning shrinks the net and
  tightens the knots [f, Plymouth note]. Hemp herring drift nets were barked repeatedly through the season [k].
- **Snares** last a few settings [k]; horse-hair lines a season [k]; a bowstring months of shooting [k]; tarred hemp rope years
  [k].
- **The engine compresses gear life already.** recipes.md §6 gives a wicker trap 20 nights, where a real one serves a year or more,
  hundreds of nights [e]. A real gill net used some 100 to 150 nights a season for 2 to 3 seasons is 200 to 450 uses [e]. At the
  trap's compression a net would last **20 to 40 uses**; at real uses it would last 6 to 14 engine years, longer than an engine
  life (old age at 32 days, D2-153). That choice decides what a net costs per use (§7, question 2).

---

## 5. Who did it, and when

- **Women's work, mostly:** spinning everywhere ("spinster"); flax dressing (scutching and hackling) and pulling largely women and
  children, breaking often men [k]. Net-making in fishing villages by women, girls and old men through the winter: James
  Paterson's net-knitting machine (Musselburgh, invented about 1812, a factory about 1820) was built to "relieve the women from the
  tedious task of net-making" [f].
- **Men's trades:** the roper; the fisherman mending on the shore; barking the nets.
- **Children:** gathering, rippling seed, turning the rope walk's wheel [k].
- **The year:** lime bark in May and June; nettle in August to October; flax sown March to April, pulled July to August, retted
  August to September, dressed autumn and winter, spun all year and above all in winter; hemp sown in May, pulled August and
  September to October; nets knitted in winter, barked before the season. **On the engine's year** (8 days a season, one engine
  night standing for about 11 real days on the ecology's clock): flax sown in spring, pulled in summer, **water retting 1 to 2
  nights, dew retting 3 to 4**, dressed and spun in autumn and winter.

---

## 6. The capital

| Capital | Who has it | Made of | Lasts | Engine |
|---|---|---|---|---|
| a spindle and whorl, a distaff | every household | a stick and a whorl of stone, clay, bone or lead | years | fold into knowledge (too cheap to be a good) |
| a netting needle and a mesh gauge | every fishing or fowling household | wood or bone | years | fold into knowledge of net-making |
| a flax plot or hemp-yard | a household or the village; in England **a quarter acre of flax or hemp for every sixty acres tilled** was required by 24 Hen. VIII c. 4 (1533) [f] | good, manured land, weeded | a crop a year; flax should not follow flax for some years [k] | a plot's crop |
| a retting pond or pit | the village; on the manor, fines for steeping hemp or flax in common water [k] | a dug pit or a dammed pool; medieval retting pits in eastern England [f, Hall] | years | the parcel's water (no building needed); or a pit as a small building later |
| a brake, a scutching board and blade, hackles | a household (brake, board) and the smith (hackles' iron) | wood; iron teeth | years | fold into the technique; hackles would bind flax to the smith (leave out at first) |
| a barking pot or kettle | the fishing village | metal (or clay) | years | needs a pot and fuel; or a hearth |
| a rope walk | a roper or town | a long straight ground or shed, a wheel or hooks, a top | decades | later |
| the spinning wheel | households, from the 13th c. | wood | years | later |

**The law shows the cost to others.** The Severn Act of 1678 (30 Cha. 2 c. 9) set a forfeit of **£5 each time** for watering hemp
or flax in the river, alongside its rules on spawning fish [f]; earlier rules on fry and spawn go back to Elizabeth (1 Eliz. c. 17)
[f]. Manorial courts fined steeping in the common pond where beasts drank [k].

---

## 7. Competing demand (why cord is worth something)

Cord is an intermediate (repo 01 §1.2): a shortage spreads to every user. Besides nets, snares and lines it went into **rope**
(wells, lashing frames and scaffolds, boats, tethers, bell ropes, the plough's and cart's traces where leather was dear),
**bowstrings**, **sacks** (linen and hemp sacking for the grain trade), **thatch and stack ties** (straw and bast rope),
**harness parts**, and above all **linen cloth**, the big sink of flax. A shirt's yarn is of the order of 0.3 to 0.5 kg spun fine,
50 to 100 hours [e from repo 03 §5.2]. Clothing is parked (D2-10), so in the engine cord's competing uses are building, wells,
bows and later cloth.

---

## 8. The developmental structure

**The floor: cord with nothing.** Anyone can strip nettle or lime and twist cord by hand, as people did 50,000 years ago. Its limits
are rate (a kg is a fortnight), season (bast only in sap time; nettle late summer), strength (bast a third of hemp) and fineness
(hand-twisted cord is too coarse for a gill net). It is enough for **snares, lashings, a hand line and a coarse net**, which is the
Mesolithic kit: Antrea's willow-bast net and Friesack's bast nets [k].

**The household.** A spindle (no real cost) and the knowledge of spinning and netting make cord finer and faster; a household can
spin wild nettle on a spindle, which is better than twisting by hand but still limited by gathering. A household can keep a small
flax or hemp patch near the house and dew-ret it on its own grass (slow, clean) or water-ret it (fast, fouling). It can knit and
mend its own nets in winter.

**What needs a village.** Water to ret in that does not foul the drinking and fishing water (a pond or pits, and a rule about
them); land in the rotation for flax (it competes with grain on good, manured land); the barking pot and oak bark (the tanner
wants the same bark); and later the rope walk and the roper, which only pay where rope is in demand (boats, wells, building, a
market).

**The paradigm switch** (economy_web.md §1): **from gathering bast to growing flax**. Not a better tool but a different social
form: land taken from grain, water fouled below, a calendar of pulses (pull, ret, dress), and a winter of women's spinning. The
second switch, **the rope walk**, turns cord into a trade good made in bulk by a specialist.

**Shallow rungs, and less with fewer layers** (Zach: "having 4 ladder rungs is a terrible idea ... it could be a lot more shallow";
"it should be possible to do things with less layers, that have less beneficial outputs"). The ladder needs only two rungs:

| Rung | Layers | What it gives | What it costs |
|---|---|---|---|
| wild cord | 1 technique | coarse cord at ~25 units a kg; enough for snares, lines and a net if one spends a fortnight | time; season |
| flax cord | crop + ret + dress and spin (3 acts, the crop on the existing farming verbs) | coarse cord at ~8 units a kg, in quantity, stronger | land, water fouled, the calendar |

Everything a fisher or snarer needs can be made on the first rung, at three times the work. Trade (cord for fish) lets a household
skip both. A net's knots cost the same on either rung, so the switch matters most for large nets and rope.

**Prehistoric and early-modern contrast.** Before farming: bark and bast cord, sinew and gut, knotted bast nets, all labour and no
land. Neolithic: flax arrives with the first farmers and soon takes fine nets (Hornstaad's plied flax gill net about 3900 BC [f]);
"finely produced flax fibre fishing nets generated a significant increase in the catch spectrum" [f]; lime bast stays for coarse
rope. Medieval: flax and hemp by the house, nets of hemp and linen, the roper in town; England's 1533 act shows the crown treating
fibre as strategic. Early modern: hemp for navies (much of it Baltic), rope walks a quarter of a mile long, net machines from about
1820 [f], cotton nets in the 19th c. [f].

---

## 9. Granularity for the engine

### 9.1 Goods

- **One good: `cord`** (a kg), standing for cord, twine, line and light rope alike. A rope is cord by weight (a well rope is 2 cord).
  Fineness is not a good; its cost (the extra spinning of fine twine) goes into the units of making the gear that needs it (the
  net).
- **`flax`**: the field's harvest, pulled straw with its seed, about **8 kg of straw a kg of fibre** [e: 3 to 4 t of straw and 400
  kg of fibre a ha]. Hemp is named in its words ("flax or hemp"), not a second crop.
- **`retting flax`**: flax set in water or on grass (a set, as a trap is), turning back into `flax` marked retted, or into a
  `retted flax` good if a state is not possible. One extra good at most.
- **Not modelled:** fibre, bast, yarn, twine, line or rope as goods; sinew, gut, horse hair, rawhide, wool, rushes and straw rope;
  linseed as a joint product (oil and fodder; flag for when oil and light come); quality grades.

### 9.2 Techniques

| Technique | Verb | At | Inputs | Units | Gives | Notes |
|---|---|---|---|---|---|---|
| **twist cord** | gather (basic, untaught tryable) | forest, scrub, fen, wet meadow, field edges (nettle and lime) | none | 1 | **0.04 cord** in summer and autumn, 0.03 in spring (bast peels), 0.015 in winter | about 25 units a kg (real 35 to 80 h [e]); optionally a plant stock with slow renewal so nettle beds are a place |
| **grow flax** | the farming verbs on a plot (sow in spring, pull in summer) | a field plot | seed (flax) | pulling about 1 unit for each 30 to 40 flax [e: 15 to 25 person-days of 10 h a ha for 3,500 kg] | flax: about 3,000 to 4,000 kg a ha | competes with grain for the plot and its manure; flax after flax fails more (production.md's rule) |
| **ret flax** | work, leaving a set | in water: 1 to 2 nights; on meadow or pasture: 3 to 4 nights | flax | 1 a batch of up to 50 flax [e] | retted flax | **in running water the parcel is fouled**: fish there leave or die for some nights, beasts will not drink; on grass no fouling but the parcel's grazing is taken |
| **dress and spin** | make (known) | a house | 8 retted flax | 7 to 8 | **1 cord** | breaking, scutching, hackling, spinning and plying in one act (real 15 to 20 h a kg) |
| **make snares** | make (basic) | anywhere | cord 0.02 | 1 | a line of snares (gear, about 10 sets) | gives the snare method a cost |
| **make a net** | make (known) | a house | cord 1 | 25 | a net (gear) | knotting, mounting and the fine twine's extra spinning; serves the fowling net and a set net for fish |
| **bark the net** | work (mend) | a hearth | bark 0.5, firewood 1 | 1 | the net's life renewed (part) | ties the net to the tanner's oak bark (another note's good) |
| fishing rod (existing) | make | | timber 0.5, **cord 0.01** (was hide 0.1) | 1 | fishing rod | the line, in hair or twine |

A seine (cord 10, about 200 units, a crew to haul) and a rope walk (later) are left for the fishing note and the later economy.

### 9.3 The levers to name

- **Gear life.** Real labour per net with life compressed like the trap's (20 to 40 uses) makes a net about ten times dearer per
  use than it really was; real life (200 to 450 uses) makes a net an heirloom that outlives its maker. A middle course: life 60 to
  80 uses with barking renewing it, so care pays more than replacement (as it did). This is a named departure from real values.
- **Wild cord rate.** 0.04 a unit is inside the real range. Raising it shrinks the flax switch; lowering it below 0.02 makes the
  floor useless for nets.
- **Fouling.** How long and how far a retting batch fouls the river is the lever that makes flax a conflict with fishers below.

### 9.4 Interlocks it gives

- the **flax plot against grain** (land, manure), a choice each spring;
- **retting against fishing** (the water fouled), across households and villages on one river;
- **the net against the tanner** (oak bark), and against the woods (firewood for the pot);
- **the net-maker's winter** (units in the dead season against spinning cloth later);
- cord as a **trade good** between flax villages and fishing villages ("good flax land" is already among the uneven endowments in
  economy_web.md §3).

---

## 10. Open questions

1. **One good or two?** One `cord` (recommended), or `cord` and `twine` (fine) so a gill net needs the fine one? Two would show
   fineness but add a good and a spinning technique.
2. **Gear life against real work** (§9.3): compressed like the trap (20 to 40 uses), real (hundreds), or the middle course with
   barking? Bears on every piece of gear in W-73, not only nets.
3. **Is flax a field crop on a plot or a garden close?** Medieval flax and hemp were mostly small closes by the house; the engine
   has plots, not gardens. And how many hectares is a plot (no figure found in the spec)?
4. **Retting's harm:** how many nights, how far downstream, and does a pond (a parcel with water and no run) take it harmlessly?
5. **Should snares consume cord each set, or be gear with a life?** Gear (recommended) matches the trap and the net.
6. **Wild fibre as a stock or free?** Nettle beds and lime trees could be a plant row with renewal (nettle could leave "wild
   greens" for its own row, eaten in spring and stripped in autumn), or `twist cord` could be unlimited.
7. **Barking's pot:** is a hearth enough, or does it need a kettle (metal)? And whose good is bark (the withies and coppice note)?
8. **Horse hair and sinew:** leave out (recommended), or let butchering give sinew as a cord substitute for bowstrings and snares?
9. **The seine:** a crew's capital now, with the fishing build, or later?
10. **Who does it:** the engine seeds nothing social, so gender and age are not modelled; is that right here, where spinning and
    netting were so strongly women's winter work?
11. **Linseed:** a joint product of the flax plot (oil, food, cattle cake), or left out until oil and light are built?

---

## Sources

Seen this session (search results; full texts not fetched):
- Hardy, B. L. et al. 2020, "Direct evidence of Neanderthal fibre technology and its cognitive and behavioral implications",
  *Scientific Reports* 10: 4889 (Abri du Maras, 3-ply cord, conifer inner bark, 41 to 52 ka):
  https://www.nature.com/articles/s41598-020-61839-w
- Antrea net (willow bast, 27 to 30 m by 1.3 to 1.5 m, 6 cm mesh, about 8300 BC): https://en.wikipedia.org/wiki/Antrea_Net; the
  palaeoenvironment study, *Iskos*: https://journal.fi/iskos/article/view/110409
- Hornstaad-Hörnle and the Neolithic lake villages (flax gill net of plied yarn; lime and oak bast nets), Propylaeum (Heidelberg):
  https://books.ub.uni-heidelberg.de/propylaeum/catalog/view/643/1047/90370
- Herrero-Otal, M. et al. 2023, La Draga cordage (lime and nettle): https://ddd.uab.cat/pub/artpub/2023/7df72699be6e/1-s2.0-S2352409X23002675-main.pdf
- Hartl, A. and Vogl, C. R. 2002, nettle clones grown in Austria, *American Journal of Alternative Agriculture*:
  https://www.cambridge.org/core/journals/american-journal-of-alternative-agriculture/article/dry-matter-and-fiber-yields-and-the-fiber-characteristics-of-five-nettle-clones-urtica-dioica-l-organically-grown-in-austria-for-potential-textile-use/B1D7A9C89633F04617CD401E7E12173F
- Pointer, S. 2021, on nettle fibre (Nettles for Textiles reports: 1 g a stem, 1.2 to 4 minutes a stem): https://sallypointer.blogspot.com/2021
- Viking Ship Museum, lime bast rope for the Gislinge boat (hemp's breaking load three times bast's):
  https://vikingeskibsmuseet.dk/en/news/lime-bast-rope-for-the-gislinge-boats-rig-1
- Jack Raven Bushcraft, lime bark cordage (6 weeks' retting): https://www.jackravenbushcraft.co.uk/lime-bark-cordage
- Karg, S. 2022, labour input for lime bast (Springer): https://link.springer.com/chapter/10.1007/978-3-030-92170-5_11
- Hansard: Irish flax yields, 1906 (28¾ and 34¾ stones an acre) and 1921 (34.1 in 1913):
  https://api.parliament.uk/historic-hansard/commons/1906/feb/26/flax-cultivation-in-ireland ;
  https://api.parliament.uk/historic-hansard/written-answers/1921/mar/03/flax
- *Illustrated London News* 1859, spreading flax in the north of Ireland (hand scutching): https://victorianweb.org/periodicals/iln/ireland/36.html
- König, A. 2020, flax fibre extraction techniques in the late Middle Ages, *EXARC Journal*: https://exarc.net/ark:/88735/10501
- Hall, A. R., medieval hemp processing in eastern England: https://eprints.whiterose.ac.uk/1832/1/halla6.pdf
- 24 Hen. VIII c. 4 (1533), sowing of flax and hemp: https://discovery.nationalarchives.gov.uk/details/r/7cb5cd0b-1fb0-432b-90c4-8e726a9a8547 ;
  the quarter-acre in sixty from Froude's *History of England*, ch. 1 (Wikisource)
- 30 Cha. 2 c. 9 (1678), the Severn (watering hemp or flax, £5): https://www.legislation.gov.uk/aep/Cha2/30/9
- Netting rates: *Workshop Receipts* (about 1,300 knots an hour, 1,750 at best):
  https://chestofbooks.com/crafts/mechanics/Workshop-Receipts-5/Netting-Part-3.html ; Indiana Traditional Arts (350 an hour):
  https://traditionalarts.indiana.edu/Programs/Apprenticeships/Current%20Recipients/Danny%20Cain%20and%20Ervin%20Garrison.html ;
  Mother Earth News (15 a minute): https://www.motherearthnews.com/diy/net-making-zmaz83mjzraw/
- Net preservation: NOAA Fishery Leaflet 66 (cutch, tanbark, oak bark):
  https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet66.pdf ; Taylor, *Preservation of fishing nets*:
  https://www.archive.org/download/preservationoffi00tayl/preservationoffi00tayl_bw.pdf
- Paterson's net machine, Musselburgh: https://electricscotland.com/hiStory/industrial/industry13a.htm ; Science Museum Group:
  https://collection.sciencemuseumgroup.org.uk/objects/co44682
- Rope walks: Ryan, J. 2011 (Chatham and Plymouth roperies): https://gala.gre.ac.uk/id/eprint/7781/1/Joan_Ryan_2011.pdf ; Labour/Le
  Travailleur 1980 (Ure on spinning on the walk): https://releve.erudit.org/fr/revues/llt/1980-v6-llt_6/llt6doc01.pdf

From the literature, not re-checked this session [k]: Kania, K. 2015 (spinning 40 to 100 m an hour; repo note 03 §5.2); Andersson
Strand, E. and the Tools and Textiles project (spindle whorls and thread); Hurcombe, L. 2014, *Perishable Material Culture in
Prehistory*; Berners, J. 1496, *A Treatyse of Fysshynge wyth an Angle* (horse-hair lines graded by hairs:
https://gutenberg.org/cache/epub/57943/pg57943.txt); Ascham, R. 1545, *Toxophilus* (bowstrings); the Friesack nets.
