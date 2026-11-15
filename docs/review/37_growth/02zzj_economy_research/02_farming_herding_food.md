# 02: Farming, herding and food, from the first fields to the global food system

Part 2 of the 02zzj economy research folder (15 Nov 2026). This is research to design from. Nothing here is decided. It uses the
vocabulary of shapes in [economy_web.md](../../../cybertron2/proposals/economy_web.md) (shallow, accretive, paradigm switch,
substitutes, joint products, assembly, chokepoint, long skill, time capital, pulse, commons, increasing returns) and extends it
where needed. It ties each system to what the engine holds now (E), using the values in `cybertron2/engine/data.py`.

## Summary

Food was the largest sector of every economy before about 1850. Farming, herding and food processing used most of the labour, most
of the land and most of the capital. The deepest finding across ten thousand years is the same one in every period: **farming
systems are set by how much land each person has and by how nitrogen gets back onto the fields.** When land is plentiful, people
farm extensively, with long fallows, fire and little labour per acre. As people per acre rise, they shorten the fallow, add manure,
labour and works, and get more food per acre but less per hour of work (Ester Boserup's intensification). In north-west Europe the
binding limit for a thousand years was the **manure gap**. Grain needs nitrogen. Nitrogen came from dung. Dung came from beasts.
Beasts needed grass and hay, and grass competed with grain for the same land. Each big change closed the gap a little more
(legumes, grass leys, clover and turnips, guano), until synthetic nitrogen broke the link between beasts and fields altogether; it
now feeds roughly 40 to 50% of humanity.

The social shape of food comes from its processing capital. Grinding, baking and brewing all began as household work, mostly
women's, and all had paradigm switches to shared capital: the quern to the lord's mill, the hearth to the village oven, the
household brew to the alehouse and then the brewery. Each switch made **a centre, an owner, a rent and a quarrel**. Medieval
English tenants owed suit of mill and paid a toll of a sixteenth to a twenty-fourth of their grain; lords confiscated hand querns.
Roller mills, packers, refrigerated cars, poultry integrators
and supermarkets later did the same at industrial scale. In the United States the four largest packers
went from a quarter of steer and heifer slaughter in 1976 to 85% in 2019, and the farmer's share of the food dollar fell to around
15 cents. Labour went the other way: 250 to 300 hours to grow 100 bushels of wheat in 1830, 15 to 20 hours by the 1930s. Farm
labour fell from about 40% of US workers in 1900 to under 2%. For a simulator, the core is a small set of state and choices: land
per person, fertility and the fodder triangle, the harvest peak, the mill as a chokepoint with a toll, ale as the barley sink, the
carcass as joint products, and later the decoupling of herd from field and the concentration of processing.

## How to read the numbers

- **[c]** checked in this session against a source found by search (listed in Sources).
- **[s]** a standard figure from the reference named, not re-checked here (this session's search budget ran out before every figure
  could be checked).
- **[r]** rough, contested or varying widely by place and source. Treat as an order of magnitude.

Units: an acre is 0.405 ha. A Winchester bushel of wheat weighs about 27 kg, so 10 bushels an acre is about 0.67 t/ha. A quarter is
8 bushels. Medieval yields are often given as **yield ratios** (grain harvested per grain sown), because customary acres and bushels
varied so much that bushels per acre are hard to compare [c, Miller and Hatcher via the Norfolk study].

---

## 1. Origins: domestication and the first farming

### 1.1 Dates and places

| Centre | Founder plants | Founder animals | Rough date of domestication |
|---|---|---|---|
| Fertile Crescent (south-west Asia) | emmer, einkorn, barley, lentil, pea, chickpea, bitter vetch, flax | goat, sheep, then cattle and pig | crops from about 9500 BCE [c]; goats and sheep about 11,000 to 10,000 years ago, cattle and pigs shortly after [c, Zeder 2008, 2011] |
| China (Yellow and Yangtze rivers) | foxtail and broomcorn millet, rice | pig, chicken (contested) | about 9,000 to 7,000 years ago [s, r] |
| Mesoamerica | maize (from teosinte), beans, squash | turkey | maize about 9,000 years ago; slow to become a staple [s, r] |
| Andes | potato, quinoa | llama, alpaca, guinea pig | about 8,000 to 5,000 years ago [s, r] |
| New Guinea, Sahel, eastern North America | taro, banana; sorghum, pearl millet; sunflower, goosefoot | | independent centres [s] |

Dates vary by several thousand years between studies, and earlier claims for domestic barley and emmer in the southern Levant have
been largely overturned [c, Zeder 2011]. The point that matters here is how slow it was. Cultivating wild cereals came first;
grain that stays on the stalk (a non-shattering rachis) took one to two thousand years or more to become common [s, r, Fuller 2007].

### 1.2 What farming did to work and to society

- **Food per area rose; food per hour did not.** Ethnographic and archaeological work suggests early farmers worked harder than
  foragers for each calorie, and skeletons of early farmers show shorter stature and worse teeth [s, r, Cohen and Armelagos 1984].
  What farming gave was more food from the same land, so more people. This is the first instance of Boserup's rule (§2.1).
- **Grain is visible, storable and countable,** so taxable and lendable; James C. Scott argues this is why early states grew on
  cereals [s, Scott 2017].
- **The secondary products revolution.** Animals were first kept for meat. Milk, wool and traction came later; Andrew Sherratt put
  the package (milk, wool, the ard, the cart) in the 4th millennium BCE [s, Sherratt 1981]. Milk residues in pottery push dairying
  back to the 7th millennium BCE in places [s, r, Evershed et al. 2008]. Traction is the turning point: an ard pulled by oxen lets one
  person work far more land, and makes the household that owns oxen different from the one that does not.
- **The first processing capital** was the saddle quern and the pot; grinding took hours a day per household [r].

**Shapes:** foraging to farming is a **time capital** switch (clear, sow, wait, store) and a switch from **commons** (wild land) to
use rights over a plot. Herds are **time capital** with **joint products**. Traction is an **assembly** (beast, yoke, ard, a person
who can drive). **Depends on:** storage (pots, pits, bins), stone (querns), wood (ards, handles), fire (clearing).

---

## 2. Farming systems and how they change

### 2.1 Boserup's sequence: land per person drives the system

Ester Boserup (1965) turned Malthus around: instead of food limiting population, rising population pushes farmers to work the land
harder. She sorted systems by how often a plot is cropped:

| System | Cropped | Fallow | Tools | Fertility from | Labour per unit of food |
|---|---|---|---|---|---|
| **forest fallow** (swidden) | 1 to 2 years | 15 to 25 years, until forest returns | axe, fire, digging stick | ash; the regrown forest | lowest |
| **bush fallow** | 2 or more years | 6 to 10 years, bush | axe, hoe | ash, bush | low |
| **short fallow** | 1 to 2 years | 1 to 2 years, grass | hoe, ard, plough | grazing animals on the fallow; some manure | middling |
| **annual cropping** | every year | a few months | plough, animals | manure, legumes, rotation | high |
| **multicropping** | 2 or 3 crops a year | none | irrigation, intensive tools | manure, night soil, silt, later fertiliser | highest |

Source: Boserup 1965 [s]. Fallow periods are her rough bands [r].

**Output per acre rises and output per hour falls** as fallow shortens, so farmers intensify when they must, not when they
discover how. Each step adds work: stumping for the plough, carting manure, weeding the grass that fire used to clear, fencing,
works. **It runs backwards too:** after the Black Death, farmers turned arable back to grass and kept more sheep [s].

### 2.2 Shifting cultivation (swidden)

- **How:** fell or ring the trees, burn in the dry season, sow into the ash with a digging stick, crop for one to three years until
  weeds and falling fertility make it not worth it, then move on.
- **Numbers:** the land needed per person is large: with one year in crop and fifteen to twenty in fallow, the total territory is
  fifteen to twenty times the cropped area. Population densities that swidden supports are low, typically under a few tens per km²
  [r]. In Finland and Sweden, slash-and-burn rye on the ash of spruce forest gave first-crop yield ratios of 1:20 or more, far above
  open-field grain [s, r].
- **Labour:** mostly the felling and burning, and fencing against animals; little weeding in the first year. Returns per hour are
  among the highest of any farming [s, r, Boserup; Clark and Haswell 1967].
- **Livestock:** not needed; often pigs or none.
- **Institutions:** a lineage or village holds a territory; a household has use rights to the plot it cleared while it crops it.

**Shape:** **shallow** in skill and capital, but **time capital** in land (the forest's regrowth is the stored fertility), and a
**commons** (the territory). **Depends on:** forest cover, fire, axes (metal raises the felling rate a lot: the engine has fell at
bare x0.25, crude x1, copper x2).

### 2.3 Infield–outfield

The system of Scotland, Ireland, Wales, northern England, Scandinavia and parts of the Low Countries and Germany [s]:

- **Infield:** the land nearest the steading, cropped every year (in Scotland bere barley and oats), getting all the manure from the
  byre and the midden.
- **Outfield:** further out, cropped for a few years (oats) after cattle had been folded on it, then left in grass for several years.
- **Hill grazing and shielings** beyond, used in summer (transhumance, §4.6).
- **Numbers:** the infield was a small share of the arable, often put at a quarter to a third [r]. Yields on outfield oats were low,
  ratios of 2 or 3 to 1 [r].
- **Institutions:** in Scotland, joint-tenant farms (the fermtoun) worked in run-rig: strips reallocated among tenants, sometimes
  by lot [s].
- Fertility flows from outfield and hill, through the beasts' dung, to the infield.

**Shape:** a **gradient** around a centre (a shape worth adding to the vocabulary: intensity falls with distance from the house,
J. H. von Thünen's rings at farm scale). **Depends on:** cattle (dung, folding), turf and peat for byre bedding.

### 2.4 Two- and three-field open fields

The system of the English Midlands and much of northern France and Germany from the 9th to 13th centuries until enclosure [s].

**How it worked:**
- A township's arable lay in two or three great fields, each divided into furlongs and strips. A household held strips scattered
  across all the fields.
- **Two-field:** one field in crop, one in fallow each year: half the arable fallow.
- **Three-field:** winter corn (wheat or rye, sown in autumn), spring corn (barley, oats, peas and beans), fallow. A third fallow.
  Going from two fields to three raises the cropped share from 50% to 67%, a third more crop from the same arable [s, arithmetic].
  It also spreads ploughing and harvest across two seasons, spreads risk across two crops, and adds legumes.
- The fallow and the stubble after harvest were **grazed in common** by the township's beasts, which dunged them. The sheep fold
  (hurdles moved nightly over the fallow) put dung where it was wanted.
- Meadow for hay was held in strips or lots and grazed in common after the hay was taken.

**Numbers (England c.1250 to 1450):**

| Measure | Figure | Mark |
|---|---|---|
| wheat sown | 2 to 2.5 bushels an acre (Walter of Henley's minimum) | [c, Postles 1979, Oseney Abbey] |
| barley, oats sown | about 4 and 4 to 5 bushels an acre | [s, r] |
| wheat yield ratio | about 4:1 gross; often 3.5 to 5 | [s, r, Campbell 2000] |
| barley, oats yield ratios | about 3.5 to 4 and 2.5 to 3 | [s, r] |
| wheat yield | about 10 to 15 bushels an acre gross, 0.7 to 1 t/ha | [r] |
| a good case | marled land, 16 bushels an acre at 4x the seed | [c, one priory account] |
| tithe | a tenth of the sheaves, taken in the field | [c, Campbell crop-yields database notes] |
| eastern Norfolk | among the highest medieval yields, from intensive legumes, manure and weeding | [c, Campbell 1983] |

So after seed (a quarter of the crop) and tithe (a tenth), a household kept about two-thirds of the gross harvest. **The engine's
ratio of 3 (harvest 3x the seed) and its fallow, manure and break gains sit inside this range.**

**Labour:** a plough team was expected to plough roughly an acre a day; the statute acre (a furrow long by a chain wide) is often
read as a day's ploughing [s, r]. Harvest was the peak: with the sickle, a reaper cut roughly a quarter to half an acre a day [r,
see §3.4]. Demesnes drew harvest labour from tenants' labour services (boon works) and hired workers.

**Institutions the system needed:**
- **a common rotation**, so that the whole field could be fenced or opened together;
- **stints**: limits on how many beasts each holding could put on the common, in proportion to its arable;
- **byelaws** made and enforced in the manor court: dates for opening the stubble, gleaning rules (often for the poor only),
  penalties for straying beasts;
- **labour services** for the lord's demesne, later commuted to money rents.

**What pushed it:** more people per acre in the 11th to 13th centuries, the heavy plough, lordship. **Its limit:** the manure gap
(§4.7): grain spread onto pasture, fewer beasts meant less dung, and yields stagnated before 1348 [s, r, Postan; qualified by Campbell].

**Shape:** a **commons** run as a **coordination problem**: no household can change its rotation alone. **Accretive** at the
margins (more legumes, marling, folding). **Depends on:** oxen (traction), sheep (folding), timber and withies (hurdles, fences),
the lord (court, mill).

### 2.5 Convertible ("up-and-down") husbandry and water meadows

From the late 15th to the 17th century, especially in the English Midlands [s, Kerridge 1967]:
- **Ley farming:** a field alternates several years in grain with several years in sown or tumbled grass, instead of a permanent
  split between arable and pasture. The grass years build fertility and carry more beasts; the grain years cash it.
- **Results:** more stock and more grain at once; yields rose, by some estimates a third or more [r]. Eric Kerridge called this
  the real agricultural revolution (1560 to 1767), a claim most historians now hold too early but not empty [s, r].
- **Needs:** control of one's own land (enclosure, or agreement within the open field to make leys in strips), fences, and capital
  to stock the grass years.
- **Floated water meadows** (Wessex chalk valleys, 17th century on): channels and sluices flood a meadow with a thin sheet of
  moving water in winter, keeping frost off and warming the grass. They gave an **early bite** for ewes in March (the hungry gap)
  and heavier hay crops [s, r]. Ewes fed by day on the meadow were folded by night on the arable: the **sheep-corn system**, which
  moved fertility from the valley to the downs. A meadow needed a drowner (a skilled specialist) and agreement between users along
  the stream.

**Shape:** **accretive**, then a **paradigm switch** where it needed enclosure. Water meadows are **assembly** (works, a skilled
operator, a river) with a **commons** along the water. **Depends on:** fences and hedges, the river, labour to build channels.

### 2.6 The Norfolk four-course rotation

- **The rotation:** wheat, then turnips, then barley, then clover (a ley of one or two years), then wheat again. No bare fallow.
- **Why each crop:**
  - **turnips** are hoed in rows, which cleans the land of weeds (the old reason for fallow), and feed sheep and cattle in winter,
    often eaten off in the field by folded sheep, which dung it;
  - **clover** fixes nitrogen from the air and makes hay and grazing. One estimate gives clover about half of the rise in crop yields
    between the 14th and the early 19th century [c];
  - wheat and barley are the cash crops.
- **Numbers:** English wheat yields rose by about a quarter from 1700 to 1800, then by about a half again from 1800 to 1850 [c,
  Overton]. National wheat yields reached about 20 to 22 bushels an acre by 1800 [s, r] and about 30 bushels (2.1 t/ha) by the
  1890s [c].
- **Adoption was slow.** Turnips were not common until the mid-18th century and the full four-course not widespread until the 19th
  [c, Overton 1996]. Earlier Flemish farming had already combined fodder crops, stall feeding and heavy manuring [s].
- **Labour and capital:** more labour per acre (hoeing, carting, folding, root lifting) and more stock per acre. The tenant had to
  stock the farm with sheep and cattle and buy seed; the landlord built barns, yards and roads.
- **Institutions:** large tenant farms on long leases with rotation covenants (Coke of Holkham) [s]: landlord, capitalist tenant and
  landless labourer. Overton calls it two revolutions, in output and in institutions [c]. **Pushed by** rising prices after 1750,
  London's market, and enclosure.

**Shape:** an **assembly** (four crops that need each other: clover's nitrogen, turnips' cleaning and fodder, the beasts' dung) and a
**paradigm switch** from open-field fallow. It also **closes a loop**: the fodder, the beasts and the fertility are on the same farm
(a shape worth naming: **closed loop**, or **mixed farming**). **Depends on:** sheep and cattle, markets for meat and grain, the
seed drill and horse hoe (for turnips in rows), enclosure.

### 2.7 Enclosure

- **What it was:** replacing open fields, common pasture and waste with consolidated, hedged or walled holdings held in severalty.
  It happened in waves: by agreement and by lords from the 15th century (often for sheep), and by **Act of Parliament** mostly from
  1750 to 1830.
- **Scale:** parliamentary enclosure covered about a fifth of England (roughly 6.8 million acres) under about 4,000 acts [s, r, Turner
  1980; Tate and Turner 1978].
- **Effects on output:** contested. Robert Allen found modest gains and argued that enclosure mostly redistributed income to
  landlords as higher rent, and that the yeoman's decline came from other causes [c, Allen 1982, 1992]. Heldring, Robinson and
  Vollmer (2021), using 15,000 parishes, found that parliamentary enclosure raised yields by about 45% by 1830 in their instrumented
  estimate (3% in plain OLS), and raised land inequality [c].
- **Costs** (the act, surveyors, fencing) fell on proprietors by allotment; small holders often sold rather than pay [s, r].
- **Social effects:** cottagers and the landless lost common rights (grazing a cow, gathering fuel, gleaning) that had been worth a
  large share of a poor family's income, by some estimates as much as an adult man's wage in some places [s, r, Humphries 1990;
  Neeson 1993]. Earlier enclosure for sheep depopulated villages; Thomas More wrote in 1516 that sheep "devour men" [s].

**Shape:** an institutional **paradigm switch**: from **commons** to private property, with a **one-off capital cost** (fences,
surveys, the act) and a redistribution of rights. **Depends on:** the state (Parliament, commissioners), hedges and walls (labour,
quicksets, stone), markets that reward choosing one's own rotation.

### 2.8 Other paths: wet rice and the labour road

Not every region went from labour to capital. Wet-rice farming in East and South-East Asia intensified by adding **labour and
skill** to small plots: transplanting, water control, double cropping, night soil, careful weeding. Francesca Bray (1986) calls this
a skill-oriented path, against Europe's capital- and animal-oriented one [s]. Yields per acre were far higher than European grain,
plots far smaller, and the key capital was the irrigation works, often built and kept by communities or states. Kenneth Pomeranz and
others argue that by 1750 the Yangzi delta matched England in living standards on this path [s, r, Pomeranz 2000]. For a simulator
this is a reminder that **labour-intensive is not backward**: it is the right answer when people are many, land is scarce and beasts
are costly to feed.

### 2.9 A summary table of the pre-industrial systems

| System | Fallow share | Labour per acre | Yield per acre | Livestock link | Capital | Institutions |
|---|---|---|---|---|---|---|
| swidden | 90 to 95% of territory | very low | first crop high, falls fast | none needed | axe, fire | territory, use rights |
| infield–outfield | most of outfield in grass | low on outfield, high on infield | low; infield better | central: dung moves to infield | byre, folds | joint tenancy, run-rig |
| two-field | 50% of arable | low to middling | low | stubble and fallow grazing | oxen, plough | common rotation, manor court |
| three-field | 33% of arable | middling | low (wheat 4:1) | as above; more legumes | oxen, plough, fold | common rotation, stints, byelaws |
| convertible | grass years instead of fallow | middling | higher (+ a third, r) | grass leys | fences, stock | enclosure or agreement |
| Norfolk four-course | 0% bare fallow | high | wheat ~20 to 30 bu (1800 to 1890) | closed loop: roots, clover, folding | stock, drill, barns | tenant farms, leases, enclosure |
| wet rice | none; 2 crops a year | very high | very high | buffalo, pigs, night soil | irrigation works | water rules, communities, state |

---

## 3. Tools, traction and works

### 3.1 The tillage tools

| Tool | What it does | Rate and needs | Notes |
|---|---|---|---|
| digging stick | holes for seed | one person | swidden; dibbling |
| spade | turns soil deep | very slow; days per acre [r] | gardens, Irish lazy beds for potatoes; the most intensive tillage |
| hoe | breaks and weeds | slow; one person | the base of African and much tropical farming; weeding everywhere |
| ard (scratch plough) | scores the soil without turning it | a pair of oxen; ploughed twice across | light soils; Mediterranean and prehistoric Europe |
| heavy mouldboard plough (carruca) | cuts with a coulter, undercuts with a share, turns the furrow with a mouldboard | a big team (8 oxen in Domesday's standard team) [c]; about an acre a day [r] | heavy clays; makes ridge and furrow, which also drains |
| harrow | breaks clods, covers seed | a horse or oxen | horse harrowing is shown on the Bayeux Tapestry [s] |
| roller, clod-breaker | breaks clods | | |
| seed drill | sows in rows at set depth | horse; saves seed, allows hoeing | Jethro Tull (1701); slow to spread until the 19th century [s] |

The **engine** has hoe (0.0625 plots a unit) and plough (0.25 plots a unit, 2 oxen, a wooden plough and 2 harness), so a plough team
does four times a hoer's work. History would make the gap larger in area per day and adds the ard as a cheaper middle step.

Lynn White (1962) made the heavy plough, horse collar and three fields the engine of medieval growth [s]; most historians now think
the plough followed population and soils rather than leading them [s, r].

### 3.2 Oxen against horses

- **Oxen** are cheaper to feed (grass and hay, little oats), need simpler harness (a yoke), need no shoes, and at the end of their
  working life are fattened and eaten. Walter of Henley (13th century) argued for the ox on exactly these grounds: an old horse is
  worth only its hide, an old ox is meat [s].
- **Horses** are faster (commonly put at a third to a half more work a day [r]) and better for carting and harrowing, but need oats,
  shoes and a padded collar.
- **Adoption:** John Langdon found that on English demesnes oxen still outnumbered horses by about two to one at the end of the 14th
  century, while **peasants adopted horses faster than lords**, especially smallholders, who valued their versatility [c, Langdon
  1986]. Horses' speed mattered most for **carting to market** [c, Claridge].
- **The land cost of the horse:** a working horse needed about three acres of cropland for feed a year (US, late 19th and early
  20th century) [c]. In 1915 about 93 million US acres fed horses and mules [c], roughly a quarter of the harvested area [r]. That
  land was freed when tractors came (§6.1). US horses and mules peaked near 27 million in the First World War [c].

**Shape:** **substitutes with trade-offs**: speed against feed cost and salvage value. **Depends on:** hay and oats, leather
(harness), metal (shoes), the smith.

### 3.3 Works on the land

| Work | What it does | Numbers | Who does it |
|---|---|---|---|
| ridge and furrow | ploughing in the same direction for years builds ridges; the furrows drain | ridges a few metres wide | the plough team |
| ditching and open drains | takes water off heavy or wet land | the engine: 40 units a plot by a crew (D2-66) | crews, the township |
| marling | spreads marl (lime-rich clay) on light or acid soils | heavy dressings (tens of tons an acre) lasting a generation or more [r]; "marl for your son" proverbs | the landholder; a medieval and 16th to 18th century practice |
| liming | burns limestone in kilns to quicklime, spread on acid soils | needs a kiln and much fuel [r] | lime burners; links to fuel and building |
| paring and burning | cuts and burns turf to ash on new or sour ground | | |
| floated water meadows | §2.5 | | the drowner, a specialist |
| under-drainage | buried channels of stones, bushes, then clay pipes | Victorian pipe drainage was lent millions of pounds of public money after the 1846 Drainage Act [s, r] | contractors; landlords borrowing |
| terraces | flat steps on hills | the engine: 60 units and 6 stone a plot (D2-66) | crews |
| irrigation | channels, tanks, wheels | the main capital of wet-rice and dry-land irrigation systems | communities, states |

**Shape:** **time capital** (paid once, yields for decades) with **upkeep** (the engine's works have upkeep). Many are **club or
public goods** (a drain only works if the neighbour's ditch is clear). **Depends on:** labour crews, lime and fuel, clay pipes
(kilns), credit.

### 3.4 Harvest: sickle, scythe and the harvest peak

- **The sickle** cuts a handful at a time, close to the ear or the ground. A reaper cut roughly a quarter to half an acre a day [r];
  a mid-19th-century farm manual put the smooth sickle at around an acre a day for a good worker [c, Stephens via secondary, OCR
  uncertain].
- **The scythe** was always used for hay. For grain it spread from the late Middle Ages for barley and oats and in the 18th and 19th
  centuries for wheat. A mower cut about 2 to 3 acres of wheat a day [c, Stephens], and **total harvest costs fell by 20 to 30%** where
  the scythe replaced the sickle [c]. But it shed more grain and needed binders and rakers following.
- **Why the switch was late:** E. J. T. Collins argued farmers cut labour costs first by using more labour more intensively, and only
  turned to the scythe and heavy hook when labour became scarce [c, Collins 1969]. J. A. Perkins disputed the link to labour markets
  [c]. On the Wolds by the 1830s "all the wheat is mown" [c].
- **The harvest peak** (most of a year's extra labour in three to six weeks) set the labour force: migrant gangs, boon works, high
  harvest wages. Harvest workers' food shifted from bread and ale towards meat after the Black Death [s, Dyer 1988].

**Shape:** a **pulse** in labour (the crop must be cut in a window) with **substitutes** (sickle or scythe). **Depends on:** metal
(blades), the smith (sharpening, setting), hired labour.

### 3.5 Threshing and winnowing

- **The flail** beat the grain out on a barn floor through the winter. Hand threshing took about a quarter of all farm labour by the
  18th century [c], and threshing gave up to half of a rural labourer's winter income [c, Clark 2001, via Caprettini and Voth].
  Rates varied widely with crop and worker; a few bushels to about ten bushels of wheat a day are typical estimates [r].
- **Winnowing** in the wind between the barn doors, then the cranked fanning mill (18th century) [s].
- **The threshing machine** (Andrew Meikle, 1786) raised output per worker by about **5 times with horse power and 10 times with
  water power** [c, Caprettini and Voth]. The flail stayed dominant in much of England for half a century [c].
- **The Swing riots** (from August 1830, more than 3,000 riots across 45 counties) targeted threshing machines, because they took
  the winter work that had kept labourers off poor relief [c].

**Shape:** a **labour sink spread across the slack season** that a machine removes. This is a useful general lesson: some work is
valuable because it **fills a slack season**, and mechanising it hurts more than its share of hours suggests. **Depends on:** barns,
horses or water (machines), later steam.

---

## 4. Herding and livestock

### 4.1 Cattle

- **Products:** traction (oxen), milk (butter and cheese), beef and veal, hides (leather), tallow (candles, soap, grease), horn, bone,
  dung.
- **Size:** medieval cattle were small, about 1.1 m at the withers [r]; carcass weights roughly doubled or more between the late
  Middle Ages and the 19th century with breeding and better feed [s, r].
- **Dairy yields:** an English estate rule expected a cow to make **seven stone (98 lb) of cheese and one stone (14 lb) of butter**
  between May and Michaelmas [c, local history, original basis not seen; r]. The 13th-century *Hosebondrie* gave careful estimates of
  milk and its yield of butter and cheese, for ewes as well as cows [c]. Rough modern readings put a medieval cow at a few hundred
  litres a lactation [r]. By the 1860s a Gloucestershire cow gave about 525 gallons a year [c]; a US cow now gives about 24,000 lb
  (roughly 11,000 litres) [s]. That is a rise of perhaps twenty- to thirty-fold [r].
- **Dairy leasing:** lords often let the dairy herd to a dairyman or dairywoman for a fixed sum per cow a year, passing the risk and
  the work to them [s, r]. Dairying was women's work in most of England until the 18th and 19th centuries.
- **Regions specialised** from the 16th century: cheese (Cheshire, Suffolk), droving store cattle from Wales and Scotland [s].

The **engine** has milk (a herd of 3 cows in milk, 1.6 each), cheese (6 milk and 0.2 salt in a cellar), slaughter (cow 40 meat and 2
hide; ox 50), dung (20 a head a year), traction (plough, pack ox) and hay.

### 4.2 Sheep and wool

- **Products:** wool (the main medieval English export), milk (ewe's milk cheese, valued at almost double cow's milk in one local
  account [c, r]), meat (mutton, mostly from old animals), skins (parchment, leather), tallow, dung (the fold).
- **Fleece:** a medieval fleece weighed about 1.5 lb (0.7 kg) against 9 lb or more for a modern one [c, VCH Gloucestershire;
  Stephenson 1988]. A sack of wool (364 lb) held the fleeces of about 240 sheep [c].
- **Scale:** English wool exports in the early 14th century ran to tens of thousands of sacks a year, roughly 30,000 to 40,000 at
  their height, that is several million fleeces [s, r, Power 1941]. The adult sheep population fell only about 13% from 1310 to 1440
  [c, Oldland 2014].
- **The chain:** flocks → wool merchants and the Staple at Calais → Flemish and Italian clothmakers; from the 15th century, cloth made
  at home replaced wool as the export. The wool customs paid for the Crown's wars; sheepwalks depopulated villages [s].

**Shape:** a **cash crop for export** with a **chokepoint** (the port, the Staple, the tax). **Joint products** with the fold's dung
and the arable. **Depends on:** pasture and downland, hurdles (withies), shepherds (long skill), shearing (a pulse), merchants,
transport.

### 4.3 Pigs and pannage

- **Pigs convert waste:** kitchen scraps, whey, spent grain from brewing, and in autumn the woods' acorns and beech mast.
- **Pannage:** the right to turn pigs into a wood in autumn, usually paid to the lord, often as one pig in ten or a money fee per pig
  [s, r]. Domesday Book measured some woodland by the number of pigs it could feed [s].
- **Numbers:** a sow has a litter of several piglets twice a year; a pig fattens to slaughter in one to two years. This makes pigs
  the quickest meat to grow [s].
- **Joint products:** meat that salts and smokes well (bacon, ham), lard, bristles, skin.
- **In towns:** pigs roamed streets and middens; towns made rules against them.

**Shape:** a **converter** of by-products and of a **seasonal pulse** (mast) on a **commons** (the woods). **Depends on:** woods,
brewing and dairying (spent grain, whey), salt (keeping).

### 4.4 Goats, poultry and the rest

- **Goats** browse what cattle and sheep cannot and give milk on poor land, but damage young trees; many medieval woods and forests
  banned them [s, r].
- **Hens** give eggs and meat from scraps and gleanings; rents in hens at Christmas and eggs at Easter were common customary dues
  [s]. **Geese** grazed stubble and commons and went to market on foot.
- **Doves** (a lordly privilege that ate peasants' grain, a grievance in 1789), **bees** (honey, wax) and **rabbits** (lordly
  warrens after 1066) [s].

### 4.5 Transhumance and droving

- **What:** moving flocks and herds seasonally between lowland winter pasture and upland summer pasture.
- **Forms:** short-range (Alpine villages to their high pastures; British shielings, where women and young people went with the
  cattle for the summer and made butter and cheese [s]); long-range (the Castilian Mesta, chartered in 1273, moving merino sheep
  hundreds of kilometres between north and south; flocks of a few million head in the early 16th century [s, r]).
- **Institutions:** protected drove roads (cañadas), grazing rights at both ends, tolls, the Mesta's own courts, and quarrels with
  farmers on the routes [s].

**Shape:** **seasonal switching between places**, a **commons** at each end, and a **corridor** (the drove road) that needs a
**public or club good** to stay open. **Depends on:** a state or guild, routes, upland and lowland, markets for wool.

### 4.6 Winter feeding and hay

- In northern Europe the winter is the bottleneck. Grass grows little from November to March. Beasts live on **hay**, straw, leaves
  (pollarded trees cut for leaf hay), and later roots and clover.
- **Hay meadow was the most valuable land.** Medieval meadow was often valued at two to three or more times arable per acre in
  extents [s, r].
- **The autumn slaughter** of beasts that could not be fed through winter was once thought massive; historians now think most beasts
  were overwintered and that the slaughter was partial, of those meant for meat [s, r].
- A cow needs very roughly a ton or more of hay to see a northern winter [r]. Haymaking is a **pulse** in early summer, needing dry
  weather and many hands.
- The **engine** has hay cut from pasture and meadow (3 a unit in summer), drying a green crop into hay, and cattle that eat hay when
  grass is short.

**Shape:** a **pulse** (haymaking) that feeds a **bottleneck** (the winter) and so sets the size of the herd. **Depends on:** meadow,
scythes, dry weather, barns and ricks.

### 4.7 Manure and the manure gap

- **The cycle:** grain takes nitrogen and phosphorus out of the soil. Beasts eat grass and hay from meadow, pasture and fallow and drop
  dung. Folded or carted onto the arable, the dung puts some of those nutrients back. Each field's fertility is therefore borrowed from
  somewhere else: the meadow, the waste, the outfield, the hill.
- **The gap:** when people pressed arable onto pasture (13th-century England), there were fewer beasts per sown acre and less dung, and
  yields were held down. Bruce Campbell's work on demesnes measures livestock per 100 sown acres and finds wide regional differences,
  with eastern Norfolk's high yields resting on legumes and intensive manuring rather than numbers of beasts [s, r, Campbell 2000].
- **Closing it, step by step:**
  1. legumes in the spring field (peas, beans, vetch) of the three-field system;
  2. folding sheep, water meadows, convertible husbandry: more grass, more dung;
  3. clover and turnips (§2.6): nitrogen from the air and more fodder on the same land;
  4. imported fertility: bones, Peruvian guano (1840s to 1870s), Chilean nitrate, superphosphate (John Bennet Lawes, 1842) [s];
  5. synthetic nitrogen (Haber–Bosch, 1909 to 1913) [s], which ends the dependence on beasts (§6.2).
- **The engine** has this triangle already: manure takes about 10 dung a plot (1.9 a unit for 0.1875 plots), a beast gives 20 dung a
  year (dung for 2 plots), grazing and fallow raise soil, and the engine's notes call cattle's dung "for 2 plots a head a year". That
  is the core of the manure gap and it is worth keeping visible.

**Shape:** a **closed loop with a leak**: nutrients cycle between herds and fields, and every harvest sold away from the farm leaks
some. A **commons** (the fallow and the fold). **Depends on:** herds, fodder, labour to cart and spread, later trade (guano) and
industry (fertiliser).

### 4.8 The joint products of a carcass

| Part | Share of a beast | Uses |
|---|---|---|
| dressed carcass (meat and bone) | about half or a little more of live weight [s, r] | fresh, salted, smoked meat |
| hide | several percent of live weight [r] | leather: harness, shoes, buckets, bellows |
| tallow, suet, lard | variable with fatness | candles, soap, grease, cooking |
| offal (heart, liver, lungs, tripe) | | food, often for the poor and servants; pies, sausages |
| blood | | black puddings, fertiliser |
| guts | | sausage casings, strings (catgut), bowstrings |
| bone | | glue, knife handles, combs, bone meal, buttons |
| horn | | cups, spoons, lantern panes, combs |
| hair and bristles | | plaster binder, brushes |
| dung, gut contents | | fertiliser |

At industrial scale, the by-products made the margin: the Chicago packers sold glue, fertiliser, soap, lard and gelatin from what had
been waste, "everything but the squeal" [s]. The engine has slaughter giving meat and hide only; economy_web.md §2.4 proposes
butchering with skill as the step that releases tallow, offal, bone and antler.

**Shape:** **joint products** in the purest form, and a **hub** that feeds leather, light, glue and fertiliser. **Depends on:**
skill (butchery), salt (keeping), tanners and chandlers downstream.

---

## 5. Food processing and its capital

### 5.1 Milling

**The ladder:**

| Rung | How | Rate and capital | Who |
|---|---|---|---|
| saddle quern | rubbing stone on a slab | slow: rotary querns are about 4.3x as efficient [c, experimental study] | women of the household |
| rotary quern | two round stones, the upper turned by hand | about 20 kg of stone when new [c]; a household's daily flour in an hour or two [r] | household |
| animal mill | large stones turned by a donkey, horse or ox | Roman bakeries (Pompeii) | bakers; estates |
| water mill | horizontal ("Norse") or vertical wheel driving stones through gears | a medieval vertical wheel of a few horsepower did the work of tens of people [r, Reynolds 1983] | the lord; the miller |
| windmill | post mill, later tower mill | in England from about 1185 [s] | the lord; the miller |
| roller mill | steel or porcelain rollers in stages, with sifting | Budapest 1870s, Minneapolis 1880s [s]; white flour in bulk | millers become milling companies |

**Numbers for England:**
- Domesday Book (1086) records about 5,624 water mills by Margaret Hodgen's count (1939) [c]; others count over 6,000, more than 5,000
  in Great Domesday [c]. Roughly one mill for every 50 households [r].
- By about 1300, England had about **10,000 mills** (Langdon), or 10,000 to 15,000 by another estimate, with **about two water mills
  for every windmill**, and they ground **about 80% of the grain** [c, Langdon 2004].
- **The toll (multure):** by the custom cited as the statute of 1266 to 1267, a miller took **a twentieth or a twenty-fourth part**
  according to the strength of the water; in places a sixteenth by custom [c]. In Scotland, tenants **thirled** to a mill paid
  multure at customary rates [c, s].
- **Suit of mill:** tenants of a manor were bound to grind at the lord's mill. Lords confiscated querns. At St Albans the abbey's
  tenants fought over hand mills for a century, and the abbot paved a parlour floor with confiscated millstones; in 1381 the rebels
  broke it up [s].

**Thresholds:** a water mill needs a site, a dam and leat, gears, stones and a millwright, and pays only with many customers. The
engine's ladder mirrors this: quern 3 grain a unit; ox mill 64 grain for 2 units
(10x); water mill 200 grain for 2 units (33x), costing 60 timber, 20 stone, 2 copper and 250 units, on a river; with upkeep
(dressing the stones, clearing the leat). The historical toll (1/16 to 1/24) is a ready number for the miller's share if the engine
ever makes rent for shared capital a rule (economy_web.md open question 3).

**Later merging:** roller milling made flour a national industry of branded millers (Washburn-Crosby, later General Mills;
Pillsbury); small mills closed [s].

**Shape:** **paradigm switch**, **increasing returns**, and a **chokepoint** that lords made into a **legal monopoly** (the
banality). **Depends on:** stone (millstones, often imported: French burrs, German lava), timber, iron (gears, spindles), water or
wind, millwrights, carts for grain.

### 5.2 Baking

- **Household baking:** flat breads on a bake-stone or griddle, bread under an upturned pot in the embers, or small clay ovens.
  Rural households often ate **pottage** (grain and pulses boiled with vegetables) more than bread [s].
- **The communal or lord's oven:** in France the *four banal* was a seigneurial monopoly like the mill: tenants paid to bake there
  [s]. In England the lord's oven was less common and less enforced [s, r]. A bread oven is heated by burning faggots inside it,
  raking out the ash and baking on the stored heat. **It only pays if fired often with a full load:** a small batch costs nearly the
  fuel of a big one. The engine: a hearth bakes 10 bread for 1 timber; an oven bakes 100 for 4 timber, two and a half times less fuel
  a loaf.
- **Bakers:** in towns, bakers were a guild trade early. The **Assize of Bread and Ale** (about 1266 to 1267) fixed the weight of a
  penny loaf according to the price of wheat, enforced by local courts, with fines and the pillory for short weight [s]. It lasted in
  London until 1815 [s].
- **Bread marked rank:** white manchet for the rich; maslin, rye and horse bread for the poor [s]. **Later**, bread moved from
  household to baker to factory (sliced 1928, Chorleywood 1961) to the supermarket's frozen dough [s].

**Shape:** **paradigm switch** with **two ways that coexist at different scales** (home baking goes on beside the baker for
centuries). A **regulated price** (the assize) is an institution worth noting: a rule that ties a processed good's price to its input.
**Depends on:** flour (mill), fuel (woods, faggots), stone or clay (ovens), salt, yeast (from brewing: barm).

### 5.3 Malting and brewing

- **The chain:** barley (or oats, wheat) is steeped in water, spread on a floor to germinate for several days, then dried in a kiln:
  that is **malt**. Malt is ground, mashed in hot water, the liquid (wort) boiled and fermented with yeast. **Ale** is unhopped and
  sours within days; **beer** is hopped and keeps for weeks or months.
- **How much:** Judith Bennett estimates that adults drank about **a gallon of ale a day** on average in medieval England [c, Bennett;
  r as an average], children less; institutional staff in the early modern period drank 6 to 10 pints a day [c]. Ale was food:
  calories, a safe drink, and part of wages. Harvest workers got ale with their food [s, Dyer 1988].
- **Grain sink:** brewing took a large share of the barley crop; a substantial fraction of all grain consumed went as drink [r]. Spent
  grain went to pigs and cattle.
- **Who:** in the 14th and 15th centuries **most ale was brewed by women** (brewsters, alewives), first for the household and then
  for sale; brewing was a by-employment that wives and widows did between other work. After 1350, and especially with hopped beer
  from the Low Countries in the 15th century, brewing became bigger, longer-lasting, more capitalised and male [c, Bennett 1996].
- **Regulation:** the assize fixed prices, ale-tasters tested quality, and routine fines worked as a licence fee [s]. **Later**: the
  London porter breweries (18th century) were among the largest firms of their day, then tied houses [s].

**Shape:** a **long skill** (malting and brewing well), **perishable** output (ale must be drunk within days, so brewing is local and
frequent until hops), then a **paradigm switch** (hops: keeping → scale → capital → men). A large **grain sink** that competes with
bread. **Depends on:** barley, water, fuel (the kiln and the copper), vessels (barrels: the cooper), hops (a regional crop).

### 5.4 Preservation

| Way | Keeps | Needs | Notes |
|---|---|---|---|
| drying | months to years | sun, wind or a kiln | grain, pulses, fruit, stockfish (cod dried in Norwegian air) [s] |
| smoking | months | fuel, a smokehouse or a chimney | bacon, ham, fish |
| salting | a year or more | **salt**, barrels | herring (the Baltic and North Sea trade, the Hanse), salt pork and beef for navies [s] |
| cheese | months to years | milk, salt, rennet, a cool store | the way to keep milk |
| butter | weeks; salted, months | salt | |
| pickling, fermenting | months | vinegar, salt, vessels | sauerkraut, pickled herring |
| ice houses | months | ice cut in winter, a pit | for the rich, from the 17th century [s] |
| canning | years | tin plate, heat, solder | Nicolas Appert (glass, 1810); Peter Durand's tin can patent (1810) [s] |
| refrigeration and freezing | months | ice, then machines | §6.4 |

**Salt** is the chokepoint for keeping protein, from Hallstatt's prehistoric salt mines to the Hanse's control of Lüneburg salt for
Baltic herring [s]. The engine already makes it so (salt pans on saltmarsh, salt fish, cheese).

### 5.5 Storage

- **On the farm:** grain in the sheaf in barns or ricks (stacks on staddle stones against rats), threshed grain in bins and chests;
  roots in clamps; hay in ricks and lofts.
- **Communal and lordly:** the tithe barn (the church's tenth); the lord's granary; town granaries in dearth.
- **State:** China's ever-normal granaries bought in plenty and sold in dearth [s, Will and Wong 1991].
- **Losses** to rats, damp and insects were heavy, often put at a tenth or more a year [r].
- **The engine** has bins, granary and cellar, and spoilage rates by good.

### 5.6 Household, communal, specialist: the thresholds

| Process | Household | Communal or lordly | Specialist trade | What sets the threshold |
|---|---|---|---|---|
| grinding | quern | the lord's mill with suit of mill | the miller | site (water, wind), capital, the lord's monopoly |
| baking | hearth, pot oven | the village or lord's oven (France) | the town baker | fuel per loaf falls with batch size; town demand |
| brewing | household brewing | the church ale, the alehouse | the brewster, then the brewer | ale spoils fast (local); hops allow scale |
| dairying | the cow and the wife | the leased dairy; summer shielings | the cheese factor; later the creamery | milk spoils; cheese keeps and travels |
| slaughter | the household pig | | the town butcher (a guild; slaughter rules) | towns, markets, rules against blood in streets |
| malting | | | the maltster | a floor and a kiln; skill |
| keeping | drying, salting | the tithe barn, the granary | salters, curers | salt, barrels, scale |

The pattern: **perishable goods stay local and household**; **goods whose processing has big fixed costs or a site** become lordly or
communal; **goods that keep and travel** become trades and then industries.

---

## 6. The modern food system

### 6.1 Mechanisation

| Stage | Machines | Hours for 100 bushels of US wheat | Mark |
|---|---|---|---|
| 1830 | walking plough, brush harrow, hand broadcasting, sickle, flail | 250 to 300 (50 to 60 an acre at 20 bushels) | [c, USDA chronology] |
| 1890 | gang plough, seeder, harrow, binder, thresher, horses | 40 to 50 | [c] |
| 1930 | tractor, 3-bottom plough, disk, 12-foot combine, trucks | 15 to 20 | [c] |
| 1980s | large tractors, combines, trucks | about 3 | [s, r] |

- **Reaper and binder:** Cyrus McCormick's reaper (1831, patented 1834), self-binders in the 1870s and 1880s [s]. The **combine**
  (reaping and threshing in one) was used in California from the 1880s with teams of 20 or more horses and spread with tractors from
  the 1920s and 1930s [s].
- **Tractors:** about 246,000 US tractors in 1920, nearly 4.7 million in 1954 [c]. Horses and mules peaked near 27 million in the
  First World War and fell to about 4 million by 1954; **tractors first outnumbered them in 1954** [c]. Land used to feed work animals
  fell from about 93 million acres (1915) to about 5 million (1960) [c]: tens of millions of acres turned from oats and hay to food
  and feed for sale.
- **The farm population:** about 40% of US workers were in farming in 1900, under 2% by 2000 [s, Dimitri, Effland and Conklin 2005].
  The mechanical cotton picker (1940s and 1950s) pushed sharecroppers off Southern farms and fed the Great Migration [s, r].
- **Capital:** machines bought on credit from makers and banks; farms grew because a combine pays only over many acres; custom
  harvest crews let small farms rent it [s].

**Shape:** a **paradigm switch** from animal and human power to fossil power, with **increasing returns** to farm size. **Depends on:**
steel, oil, engines, credit, rural roads, dealers and repair.

### 6.2 Fertiliser

- **Before synthesis:** guano from Peru (1840s to 1870s), Chilean sodium nitrate, bone meal, and superphosphate (bones or rock
  phosphate treated with sulphuric acid; Lawes's patent 1842, and the Rothamsted experiments from 1843) [s].
- **Haber–Bosch:** Fritz Haber fixed nitrogen from the air as ammonia in the lab (1909); Carl Bosch scaled it up at BASF's Oppau plant
  (1913) [s]. It uses high pressure, heat and hydrogen, now mostly from natural gas.
- **How many it feeds:** Vaclav Smil estimated that about **40% of the world's people in 2000** depended on food grown with synthetic
  nitrogen; Erisman et al. put it at 44% in 2000 and **48% in 2008** [c]. Without it, crop harvests would be about half of today's [c,
  Smil]. Our World in Data puts the number supported at about 3.5 billion people in 2015 [c].
- **What it did to farming's shape:** fertility stopped being borrowed from beasts. Grain farms could run with no animals; animals
  could be kept far from where their feed grew. The closed loop of §2.6 opened: grain belts in one place, feedlots and poultry
  houses in another, manure becoming a disposal problem rather than a resource.

**Shape:** an **energy transition** in fertility (from the organic economy's dung to mineral energy: E. A. Wrigley's terms). It
**decouples** two chains (herds and fields) that had been bound together for ten thousand years. **Depends on:** natural gas, chemical
industry, phosphate and potash mines (chokepoints: Morocco holds most of the world's phosphate rock reserves [s]), transport.

### 6.3 Hybrid seed and the Green Revolution

- **Hybrid maize** (US, 1930s) gave higher yields but does not breed true, so farmers had to **buy seed every year**. Seed became an
  industry (Pioneer Hi-Bred, founded 1926) [s]. Seed selection, which the engine has as a farmer's skill (D2-65), moved from the
  farmer to the company.
- **The Green Revolution:** semi-dwarf wheats bred by Norman Borlaug in Mexico from the Japanese Norin 10 genes, and IR8 rice from the
  International Rice Research Institute (1966). Short stalks did not fall over under heavy fertiliser [s]. It came as a **package**:
  the seed, fertiliser, irrigation, pesticides, credit, extension advice and often guaranteed prices.
- **Numbers:** in the developing world, cereal production **tripled** over about fifty years while the cultivated area rose only about
  **30%**, as population more than doubled [c, Pingali 2012]. The first Green Revolution period is usually put at 1966 to 1985 [c]. The
  research is estimated to have saved 18 to 27 million hectares from being brought into farming [c, Stevenson et al. 2013].
  Sub-Saharan Africa largely missed it [c].
- Gains went first to farmers with water and credit; groundwater and diversity costs are debated [s, r].

**Shape:** an **assembly** (the package: if any input is missing, the seed does worse than the old one), with a **chokepoint** in
seed and in water. **Depends on:** fertiliser, irrigation works, credit, research institutions (a public good), state procurement.

### 6.4 Meatpacking and the cold chain

- **Disassembly lines:** Cincinnati ("Porkopolis") in the 1830s to 1850s packed pork on lines where each worker made one cut as
  carcasses moved on overhead rails [s]. Henry Ford later said the Chicago packers' lines inspired his assembly line [s].
- **Chicago:** the Union Stock Yards opened in 1865 [c], at the meeting point of the western railways and the eastern market.
- **The refrigerated car:** in 1878 Gustavus Swift ordered ten refrigerated cars designed by Andrew Chase, with ice above the load so
  cold air fell through it, and built icing stations along the route [c]. Shipping **dressed beef** instead of live cattle cut freight
  weight (the inedible half stayed in Chicago), and the by-products became a business of their own. By 1920 Swift's line ran about
  7,000 ice-cooled cars [c].
- **Concentration:** Swift, Armour and Morris (with Cudahy and Wilson, the Big Five) dominated by 1900 [c, s], and drew the Meat
  Inspection Act (1906), the 1920 consent decree and the Packers and Stockyards Act (1921) [s].
- **The second wave:** Iowa Beef Packers (IBP, 1960s) built plants in the cattle country, used low-skilled labour on fast lines, and
  shipped **boxed beef** (vacuum-packed cuts) instead of carcasses [s]. The four-firm share of US steer and heifer slaughter rose from
  **about 25% in 1976** to about 36% in 1980 and **85% in 2019** [c, GIPSA; USDA ERS].
- **Poultry integration:** in 1925 a broiler took **112 days** to reach 2.5 lb on 4.7 lb of feed per pound, with 18% mortality; now
  about **47 days** to around 6.5 lb on roughly 1.7 to 1.9 lb of feed per pound [c, National Chicken Council; others]. Contract growing
  began in the 1950s, and by the mid-1960s over 90% of broilers came from integrated firms. About 40 integrators contract with about
  29,500 growers for 95% of US broilers; the company owns the birds and feed, the grower owns the houses and carries their debt, and is
  paid per pound against the performance of other growers [c, USDA; industry manual].
- **The cold chain:** ice, then machines (1870s); frozen New Zealand mutton to London (1882); Birdseye's quick freezing (1920s);
  home refrigerators (most US homes by the 1950s); reefer containers [s]. It is only as good as its weakest cold store.

**Shape:** **joint products** at industrial scale, **increasing returns**, and **vertical integration** (one firm owning or
contracting every stage: a shape worth adding, the **merged chain**). The cold chain is an **assembly** in time (every link needed).
**Depends on:** railways, ice and then refrigeration, feed grain (maize, soy), cheap labour, regulation.

### 6.5 Food processing industries

| Industry | Key change | Date | Mark |
|---|---|---|---|
| canning | Appert's bottling; Durand's tin can | 1810 | [s] |
| condensed milk | Gail Borden's patent | 1856 | [s] |
| margarine | Mège-Mouriès, for Napoleon III's navy | 1869 | [s] |
| roller flour | Budapest, then Minneapolis | 1870s to 1880s | [s] |
| breakfast cereals | Kellogg, Post | 1890s | [s] |
| beet sugar | French Napoleonic blockade; later European subsidy | 1810s on | [s] |
| frozen food | Birdseye | 1920s | [s] |
| factory bread | sliced bread; Chorleywood | 1928; 1961 | [s] |

**How the chains merged:** each industry took a household or craft step (preserving, dairying, milling, baking) into a factory and then
attached a **brand** and **national distribution** to it. Food processors became the largest buyers of farm goods and set grades,
varieties and contracts (tomatoes bred for machine picking and canning; potatoes for chips). The farmer moved from selling to a
market to supplying a processor to a specification.

### 6.6 Retail

- **Chain stores:** the Great Atlantic & Pacific Tea Company (A&P) grew to the largest US retailer by the 1920s and 1930s [s].
- **Self-service:** Piggly Wiggly (Memphis, 1916) let customers take goods from shelves [s]. **The supermarket:** King Kullen (Queens,
  1930) combined self-service, low prices, volume and a car park [s].
- **Later:** hypermarkets; Walmart became the largest US grocer [s], with something like a fifth to a quarter of US grocery sales [r].
  Supermarkets spread through Latin America, Asia and Africa from the 1990s, taking large shares of urban food sales within two decades
  [s, r, Reardon et al. 2003].
- **What it does to the chain:** buyer power. Retailers set standards, private labels, delivery windows and prices. The US farmer's
  share of each food dollar spent is about **15 cents** in USDA's food dollar series [s, r]; the rest goes to processing, packaging,
  transport, retail and food service.
- **What it does to households:** food fell from most of a household's spending (perhaps 70 to 80% for a medieval or early modern
  labourer [r, the Phelps Brown and Hopkins basket]) to about a tenth of disposable income in the United States [s]. Cooking moved
  partly out of the home (ready meals, restaurants).

### 6.7 Global supply chains

- **Grain:** the Chicago Board of Trade (1848), grain grading and elevators (1850s), futures contracts (1860s): grain became a
  commodity sold by grade, not by the farmer's sack [s, Cronon 1991]. A few trading houses (ADM, Bunge, Cargill, Louis Dreyfus) handle
  much of world grain and oilseed trade [s].
- **Feed:** soybeans from Brazil and the US feed pigs and poultry in China and Europe; maize feeds feedlots. **Livestock eats about a
  third of the world's cereal crop** [s, r].
- Reefers and air freight carry fresh food across hemispheres; aquaculture integrates like poultry.
- Private and state **standards** decide who can sell.
- **Fragility:** concentration and just-in-time stocks make the system efficient but brittle. In 2020 COVID-19 outbreaks closed a
  handful of US packing plants and backed up hogs and cattle on farms [s].

**Shape:** a **network of chokepoints** (traders, ports, packers, retailers, seed and fertiliser makers) joined by **cold and bulk
transport**. Comparative advantage at the scale of continents. **Depends on:** shipping, finance, standards, energy.

---

## 7. Paradigm switches and their social effects

| Area | Before | After | Who does the work | Who owns the capital | Rents and institutions that follow |
|---|---|---|---|---|---|
| getting food | foraging | farming and herding | households, much more labour | households own stores and beasts | property in land and herds; inheritance; storage; taxes in grain |
| tillage | hoe, ard | heavy plough | the ploughman and team | those with oxen; teams shared | co-aration (sharing teams); open fields; the manor |
| fallow | two fields | three fields | more labour, spread over two seasons | the township's common rotation | byelaws, stints, manor court |
| fertility | fallow and grazing | Norfolk four-course | more hired labour | capitalist tenant; landlord's buildings | leases with covenants; landlord, tenant, labourer |
| land | open fields and commons | enclosure | fewer hands per acre in some places | proprietors | loss of common rights; rural poverty; poor law |
| harvest | sickle | scythe, then reaper, binder, combine | fewer, stronger hands; then machines | farmer; custom harvesters | harvest gangs fade; machine dealers and credit |
| threshing | flail | threshing machine | machine crews | farmer; travelling machine owners | the Swing riots; contract threshing |
| traction | oxen | horses, then tractors | | farmer; then manufacturers' credit | feed land freed; dealers, fuel |
| fertility | dung | guano, then synthetic N | | chemical firms | herds and fields decouple; a fertiliser industry |
| seed | saved seed | hybrids, Green Revolution | | seed companies, public research | seed bought yearly; intellectual property |
| grinding | quern | the lord's mill; then roller mills | the miller; then mill workers | the lord; then milling companies | suit of mill, multure (1/16 to 1/24); brands |
| baking | hearth | oven; baker; factory | the baker; then factory workers | the lord (banal oven), guild bakers; then firms | oven fees; the assize of bread; branded bread |
| brewing | household | alehouse; brewery | women, then men | brewsters; then brewers | the assize of ale, licensing; tied houses |
| dairying | the farm wife | leased dairy; creamery; dairy companies | dairymaids; then factory workers and milkers | lord or farmer; then cooperatives and firms | dairy leases; milk marketing boards |
| meat | household slaughter, town butchers | packing houses, integrators | line workers; contract growers | packers; integrators | meat inspection; antitrust; contract growing |
| selling | markets, shops | chains, supermarkets | shop staff | retail chains | buyer power; private standards |

Three patterns run through the table:
1. **The capital moves up the chain.** In each era the stage with the biggest fixed cost becomes the chokepoint and takes the rent:
   the mill in 1300, the land in 1800, the packer and the railway in 1900, the retailer and the seed and fertiliser makers in 2000.
2. **Each switch moves work between people.** From women at the quern to the male miller; from brewsters to brewers; from many
   reapers to a few mowers to a machine; from family farms to contract growers and line workers. The switch decides who has work in
   the slack season and who is paid in kind.
3. **Each switch makes an institution to argue over:** suit of mill and the toll; stints and byelaws; leases; enclosure acts; the
   assizes; antitrust and meat inspection; grower contracts; standards.

---

## What a simulator could take from this

**The systems and switches that matter most to model**, roughly in order:

1. **The fertility triangle: field, beast, fodder.** This is the deepest constraint in pre-industrial farming and the engine already
   holds it (dung for about 2 plots a beast a year; manure, fallow and grazing on the soil). Keep it binding and visible, so that
   ploughing up the pasture for grain is a real trade-off that pays now and costs later. Each later system is a different answer to
   it: legumes, folding, clover and roots, then bought fertility.
2. **Land per person drives the method (Boserup).** Let the extensive method give more food per unit of work and the intensive one
   more food per plot. Then intensifying is something a crowded village chooses under pressure, and something a depopulated one
   undoes. This also gives the engine a reason for swidden or long-fallow methods on the frontier.
3. **The open field as a coordination problem.** A common rotation, stints on the common, dates for opening the stubble, gleaning
   rules. These are institutions agents would have to make and enforce, and they set up enclosure as a later fight between those who
   gain and those who lose common rights.
4. **The harvest pulse and the slack season.** The harvest sets the labour force: hiring, boon work, migrant gangs, the scythe as a
   switch when labour is short. Threshing filled the winter; a machine that removes winter work can cause riots. The engine's
   seasons and windows (the farming `window`) already give the pulse.
5. **The mill as the first chokepoint, with a toll.** The historical numbers are clean: a sixteenth to a twenty-fourth of the grain;
   suit of mill; querns seized. The engine's ladder (quern 3 a unit, ox mill 32, water mill 100) is a good shape. A rule or a common
   agreement for the miller's share would make the mill's owner a real power (economy_web.md open question 3).
6. **Ale as a grain sink, a food and a wage.** Barley into malt into ale, perishable in days, brewed by women for sale, priced by an
   assize. It competes with bread for grain, gives a trade to households without land, and is the natural wage in kind.
7. **The carcass as joint products.** Slaughter should release hide, tallow, offal and bone, with skill deciding how much
   (economy_web.md §2.4). At any scale, the by-products decide whether processing pays.
8. **Hay and the winter bottleneck.** Herd size is set by winter feed, and meadow is the most valuable land. Haymaking is a second
   labour pulse.
9. **Oxen against horses.** A clean substitute: speed against feed and salvage. Peasants adopting faster than lords is a nice
   emergent test.
10. **Wool or another export crop** that pays lords to convert arable to pasture, so that the cash economy and the subsistence
    economy pull the same land in different directions.

**For the modern arc**, if the engine ever goes there, the useful variables are few:
- **labour hours per unit of output** (250 to 300 hours per 100 bushels of wheat in 1830, 15 to 20 by 1930, about 3 by the 1980s);
- **the energy subsidy** (fossil fuel for traction, gas for nitrogen), which decouples herd from field and farm from village;
- **concentration at one stage** (packers, integrators, retailers) and the **share of the final price** that reaches the farmer;
- **time to spoil** as the thing the cold chain changes, which turns local markets into continental ones;
- **contracts that move risk** (the grower owns the houses and the debt; the integrator owns the birds).
These can be regime parameters rather than simulated acts: each era is a different set of costs, spoil times and owners.

**What to aggregate or leave out:**
- **Crop species beyond three kinds** (a winter grain, a spring grain, a legume or fodder crop) add names without decisions. The engine's
  grain, rye and beans are already enough to express the three-field and four-course logic.
- **Sub-steps of tillage** (harrowing, rolling, cross-ploughing) fold into the plough's rate.
- **Exact yields per variety, per soil and per year** beyond a mean, a variance and the fertility effects.
- **Winnowing and cleaning** fold into threshing; threshing itself can stay folded into reaping unless the engine wants the winter
  labour sink.
- **Minor beasts** only where they make a conflict (doves on grain, the lord's warren, goats in the woods).
- **The full modern supply chain** (standards, futures, private labels) is better summarised as concentration and price shares than
  built as acts.

---

## Sources

Checked in this session ([c]) and standard references ([s]). Where a figure came through a secondary page, the page is listed too.
Two hosts (millsarchive.org and bahs.org.uk) could not be fetched from this session, and the web search budget ran out before every
[s] figure could be checked.

**Origins**
- Zeder, M. A. (2008). Domestication and early agriculture in the Mediterranean Basin. *PNAS* 105(33). https://pmc.ncbi.nlm.nih.gov/articles/PMC2575338
- Zeder, M. A. (2011). The origins of agriculture in the Near East. *Current Anthropology* 52(S4). https://www.journals.uchicago.edu/doi/10.1086/659307
- National Geographic Education, "The development of agriculture". https://www.nationalgeographic.org/article/development-agriculture
- Fuller, D. Q. (2007). Contrasting patterns in crop domestication and domestication rates. *Annals of Botany* 100. [s]
- Cohen, M. N. and Armelagos, G. J., eds. (1984). *Paleopathology at the Origins of Agriculture*. Academic Press. [s]
- Scott, J. C. (2017). *Against the Grain: A Deep History of the Earliest States*. Yale. [s]
- Sherratt, A. (1981). Plough and pastoralism: aspects of the secondary products revolution. In *Pattern of the Past*, Cambridge. [s]
- Evershed, R. P. et al. (2008). Earliest date for milk use in the Near East and southeastern Europe. *Nature* 455. [s]

**Farming systems**
- Boserup, E. (1965). *The Conditions of Agricultural Growth*. Allen & Unwin. [s]
- Clark, C. and Haswell, M. (1967). *The Economics of Subsistence Agriculture*. Macmillan. [s]
- Campbell, B. M. S. (2000). *English Seigniorial Agriculture, 1250–1450*. Cambridge. Crop yields database notes: https://www.bahs.org.uk/crop-yields-database/
- Campbell, B. M. S. (1983). Arable productivity in medieval England: some evidence from Norfolk. *Journal of Economic History* 43(2). https://resolve.cambridge.org/core/journals/journal-of-economic-history/article/arable-productivity-in-medieval-england-some-evidence-from-norfolk/75CD5C8160488863D54BA7EBED38EB89
- Postles, D. (1979). Grain issues from some properties of Oseney Abbey, 1274–1348. *Oxoniensia* 44. https://www.oxoniensia.org/volumes/1979/postles.pdf
- Schneider, E. B. Prices and production: agricultural supply response in fourteenth-century England. Nuffield paper. https://www.nuff.ox.ac.uk/economics/history/Paper90/schneider90.pdf
- Kerridge, E. (1967). *The Agricultural Revolution*. Allen & Unwin. [s]
- Overton, M. (1996). *Agricultural Revolution in England: The Transformation of the Agrarian Economy 1500–1850*. Cambridge. https://www.cambridge.org/core/books/agricultural-revolution-in-england/agricultural-revolution-reconsidered/C86519B90B0D380E6E804189D4AECE53
- "British Agricultural Revolution", Wikipedia (yields, clover's share, Overton's dating). https://en.wikipedia.org/wiki/British_Agricultural_Revolution
- Chorley, G. P. H. (1981). The agricultural revolution in northern Europe, 1750–1880: nitrogen, legumes and crop productivity. *Economic History Review* 34(1). [s]
- Allen, R. C. (1982). The efficiency and distributional consequences of eighteenth century enclosures. *Economic Journal* 92. https://www.amherst.edu/media/view/107450/original/allen_1982_enclosure.pdf
- Allen, R. C. (1992). *Enclosure and the Yeoman*. Oxford. [s]
- Heldring, L., Robinson, J. A. and Vollmer, S. (2021). The economic effects of the English parliamentary enclosures. NBER w29772. https://www.nber.org/system/files/working_papers/w29772/w29772.pdf ; digest: https://www.nber.org/digest/202204/enclosure-rural-england-boosted-productivity-and-inequality
- Turner, M. (1980). *English Parliamentary Enclosure*. Dawson; Tate, W. E. and Turner, M. (1978). *A Domesday of English Enclosure Acts and Awards*. [s]
- Humphries, J. (1990). Enclosures, common rights, and women. *Journal of Economic History* 50(1). [s]
- Neeson, J. M. (1993). *Commoners: Common Right, Enclosure and Social Change in England, 1700–1820*. Cambridge. [s]
- Bray, F. (1986). *The Rice Economies: Technology and Development in Asian Societies*. Blackwell. [s]
- Pomeranz, K. (2000). *The Great Divergence*. Princeton. [s]

**Tools, traction, harvest, threshing**
- Langdon, J. (1986). *Horses, Oxen and Technological Innovation: The Use of Draught Animals in English Farming from 1066 to 1500*. Cambridge. https://ideas.repec.org/b/cup/cbooks/9780521525084.html ; thesis: https://etheses.bham.ac.uk/id/eprint/14029
- Claridge, J. The adoption of the horse... LSE working paper 251. https://www.lse.ac.uk/asset-library/information/wp251.pdf
- Domesday plough teams: https://sites.google.com/site/domesdaymaterials/domesday-book/data-terminology/manors/ploughs
- White, L. (1962). *Medieval Technology and Social Change*. Oxford. [s]
- Collins, E. J. T. (1969). Harvest technology and labour supply in Britain, 1790–1870. *Economic History Review* 22(3); with Stephens's *Book of the Farm* figures as reported in *Tools and Tillage*: https://digi.ub.uni-heidelberg.de/diglit/tools_tillage1976_1979/0049 and https://digi.ub.uni-heidelberg.de/diglit/tools_tillage1976_1979/0133/text_ocr
- Caprettini, B. and Voth, H.-J. Rage against the machines: labor-saving technology and unrest in industrializing England. https://www.jvoth.com/Rage_Against_the_Machines.pdf ; citing Clark, G. (2001), farm wages and living standards.
- "Threshing machine", Wikipedia. https://en.wikipedia.org/wiki/Threshing_machine
- Olmstead, A. L. and Rhode, P. W. Reshaping the landscape: the impact and diffusion of the tractor in American agriculture. https://faculty.econ.ucdavis.edu/faculty/alolmstead/Recent_Publications/Reshaping_the_Landscape.pdf
- US Census of Agriculture 1954, *A Graphic Summary*. https://agcensus.library.cornell.edu/wp-content/uploads/1954-Agriculture_1954_A_Graphic_Summary-CHARTS_AND_MAPS-1087-Table-62.pdf
- Tractors and horse feed acreage (dissertation reference): https://people.duke.edu/~rcd2/Dissertation/References/Theory/Tractor%20Ag.pdf

**Herding**
- Stephenson, M. J. (1988). Wool yields in the medieval economy. *Economic History Review* 41(3). [s]
- Oldland, J. (2014). Wool and cloth production in late medieval and early Tudor England. *Economic History Review* 67(1). https://ideas.repec.org/a/bla/ehsrev/v67y2014i1p25-47.html
- Victoria County History (Gloucestershire), on Cotswold fleece weights and the sack. https://ihr-archive.github.io/vch-explore/node/20682.html
- Power, E. (1941). *The Wool Trade in English Medieval History*. Oxford. [s]
- Henham local history, medieval farming (cheese and butter per cow). https://www.henhamhistory.org/medieval-farming/
- Fussell, G. E., on butter and cheese making and the *Hosebondrie*. https://www.taylorfrancis.com/chapters/mono/10.4324/9780429280504-5/butter-cheese-making-fussell
- Milton Abbas History Group, sheep and wool. https://miltonabbashistorygroup.com/sheep-and-wool/
- Oschinsky, D. (1971). *Walter of Henley and Other Treatises on Estate Management and Accounting*. Oxford. [s]
- Dyer, C. (1988). Changes in diet in the late Middle Ages: the case of harvest workers. *Agricultural History Review* 36. [s]

**Processing**
- Hodgen, M. T. (1939). Domesday water mills. *Antiquity* 13. Cited in Cambridge: https://core-prod.cambridgecore.org/core/journals/anglo-saxon-england/article/parts-of-an-anglosaxon-mill/554F5F1EAD1E1096BDAD7A1364963C05 ; and https://windmillworld.com/watermills/domesday.htm
- Langdon, J. (2004). *Mills in the Medieval Economy: England 1300–1540*. Oxford. Review: https://muse.jhu.edu/article/186647/pdf
- Holt, R. (1988). *The Mills of Medieval England*. Blackwell. [s]
- Mill toll of a twentieth or twenty-fourth part, a sixteenth by custom: legal treatise transcribed at Maryland State Archives. https://msa.maryland.gov/megafile/msa/speccol/sc2900/sc2908/000001/000153/html/am153--253.html
- Experimental quern efficiency (saddle against rotary) and quern weights: Journal of Lithic Studies. https://journals.ed.ac.uk/lithicstudies/article/download/5008/7201/16427
- Reynolds, T. S. (1983). *Stronger than a Hundred Men: A History of the Vertical Water Wheel*. Johns Hopkins. [s]
- Bennett, J. M. (1996). *Ale, Beer, and Brewsters in England: Women's Work in a Changing World, 1300–1600*. Oxford. Interview: https://endeavors.unc.edu/spr97/brew.html
- Early modern beer, interdisciplinary case study. *Historical Journal* (2023). https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/76C118F73B8D35FED9E5B69CB3E966FB/S0018246X23000043a.pdf/understanding_early_modern_beer_an_interdisciplinary_casestudy.pdf
- Will, P.-E. and Wong, R. B. (1991). *Nourish the People: The State Civilian Granary System in China, 1650–1850*. Michigan. [s]

**Modern**
- USDA chronology of farm labour per unit (Yearbook 1940) and the history of American agriculture: https://ageconsearch.umn.edu/record/358888/files/AgHistoryChronologyYB1940.pdf ; https://www.farms.com/news/the-history-of-american-agriculture-181954.aspx
- Dimitri, C., Effland, A. and Conklin, N. (2005). *The 20th Century Transformation of U.S. Agriculture and Farm Policy*. USDA ERS EIB-3. [s]
- Smil, V. (2001). *Enriching the Earth: Fritz Haber, Carl Bosch, and the Transformation of World Food Production*. MIT. [s]
- Erisman, J. W. et al. (2008). How a century of ammonia synthesis changed the world. *Nature Geoscience* 1. https://www.iai.int/admin/site/sites/default/files/uploads/2008.Erisman-et-al_NatureGeo.pdf
- Our World in Data, "How many people does synthetic fertilizer feed?" https://ourworldindata.org/how-many-people-does-synthetic-fertilizer-feed
- Pingali, P. L. (2012). Green Revolution: impacts, limits, and the path ahead. *PNAS* 109(31). https://pmc.ncbi.nlm.nih.gov/articles/PMC3411969/
- Stevenson, J. R. et al. (2013). Green Revolution research saved an estimated 18 to 27 million hectares. *PNAS* 110(21). https://pmc.ncbi.nlm.nih.gov/articles/PMC3666715
- "Swift Refrigerator Line" and "Gustavus Franklin Swift", Wikipedia. https://en.wikipedia.org/wiki/Swift_Refrigerator_Line ; https://en.wikipedia.org/wiki/Gustavus_Franklin_Swift
- Chicago Public Library, "Union Stockyards, Part 1". https://chipublib.org/?p=39407
- Aduddell, R. and Cain, L. The refrigerator car and the growth of the American dressed beef industry. *Business History Review*. https://www.cambridge.org/core/journals/business-history-review/article/abs/refrigerator-car-and-the-growth-of-the-american-dressed-beef-industry/51CE48F7F8021D23C854602C16D402AF
- Beef packer concentration (GIPSA data; USDA ERS): https://ageconsearch.umn.edu/record/94758/files/25-2%20Assessing%20competition.pdf ; https://ers.usda.gov/webdocs/publications/106795/eib-256_summary.pdf?v=4878.9
- National Chicken Council, "U.S. broiler performance, 1925 to present". https://www.nationalchickencouncil.org/?p=162 ; vertical integration: https://www.nationalchickencouncil.org/industry-issues/vertical-integration/
- USDA ERS, broiler contracts and grower pay. https://www.ers.usda.gov/webdocs/publications/41403/17882_aer807b_1_.pdf?v=9940 ; https://www.ers.usda.gov/amber-waves/2008/september/small-farms-still-important-in-broiler-production
- US Poultry Industry Manual (integrators and growers). https://www.thepoultrysite.com/articles/poultry-industry-manual-broilers-scope-of-the-broiler-industry
- Cronon, W. (1991). *Nature's Metropolis: Chicago and the Great West*. Norton. [s]
- Reardon, T., Timmer, C. P., Barrett, C. B. and Berdegué, J. (2003). The rise of supermarkets in Africa, Asia, and Latin America. *American Journal of Agricultural Economics* 85(5). [s]
- USDA ERS, Food Dollar Series (farm share of the food dollar). https://www.ers.usda.gov/data-products/food-dollar-series/ [s]
- Wrigley, E. A. (2010). *Energy and the English Industrial Revolution*. Cambridge. [s]

**Engine**
- `cybertron2/engine/data.py` on this checkout: TECHNIQUES (sow, hoe, plough, ditch, terrace, manure, reap, hay, milk, slaughter,
  grind, mill, water mill, bread, oven bread, cheese), PHYSICS `farming` and `cattle`, FITTINGS (oven, millstones, water wheel).
- [economy_web.md](../../../cybertron2/proposals/economy_web.md); [02zzh](../02zzh_economy_layers.md); [02zzi](../02zzi_economies_scaling.md);
  [02zzg](../02zzg_economy/README.md).
