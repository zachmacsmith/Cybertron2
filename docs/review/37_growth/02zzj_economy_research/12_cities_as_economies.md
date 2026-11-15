# 12. The city as an economy, across history

Part of the 02zzj economy research folder (37.2, 15 Nov 2026). It uses the frame and vocabulary of 02zzi (kinds of good, the
organic economy, the limits on pre-industrial economies) and of `proposals/economy_web.md` (chain shapes: chokepoint, threshold,
paradigm switch, joint products, pulse, commons, increasing returns). It is research to think with, not a build list.

**How to read the numbers.** Figures are cited to a source in brackets; the list is at the end. A figure marked **≈** is a rough
order of magnitude (often my own arithmetic from cited inputs, and said so). A figure marked **†** is contested: scholars give
ranges that differ by a factor of two or more, and the range is given where known. Ancient and medieval populations are almost all
†. Some sources could only be checked through secondary summaries in this session; where that matters, it is said.

## Summary

A city is a place where more people live than the land around them can feed, so every city is first a **supply problem**: food,
water, fuel and building material must come in every day, and waste and the dead must go out. The size a city can reach is set by
how cheaply it can draw those flows from how far away, and that is mostly a question of transport. Before railways, bulk goods
moved by water at a small fraction of the cost by land (Diocletian's price edict implies river freight about five times sea
freight, and land freight dozens of times sea freight), so the great pre-industrial cities (Rome, Chang'an, Kaifeng, Baghdad,
Venice, London, Amsterdam, Edo) all sat on water and reached into hinterlands hundreds or thousands of kilometres away. Their
food came through institutions, not just markets: Rome's annona, the Tang and Song canal grain tribute, Paris's police of the grain
trade, London's licensed markets. Their own death rates exceeded their birth rates until the late 19th century, so they also
consumed people: London around 1700 needed roughly 8,000 net migrants a year just to keep growing (Wrigley 1967). Industrial
cities broke the organic ceiling with coal and rail, and Chicago shows the result most clearly: a hub that turned the grain, pine
and cattle of a continent into graded, tradeable commodities (Cronon 1991).

Why cities grow, once fed, is that density pays. Firms and workers in bigger cities are more productive (a doubling of city size
raises productivity by roughly 2 to 8 per cent in the econometric literature), and socio-economic outputs scale super-linearly with
population (wages, patents and crime with exponents near 1.1 to 1.3) while infrastructure scales sub-linearly (road surface, cable
length, petrol stations near 0.8) (Bettencourt et al. 2007). Jane Jacobs's account is that cities are where new work is added to
old. But each step up in size was gated by a layer of infrastructure that had to exist first: streets and a market, then clean
water, then drainage, then bulk transport, then fuel networks, then mechanical transport within the city, then electricity and
lifts for height, then sewage treatment and public health for megacity density. This document sets out the metabolism with its
numbers per inhabitant, a history of fourteen cities as economies, the theory of urban growth, the city's own trades and services,
the infrastructure layers and their dependencies, dependency trees from market town to megacity, and what a simulator could take.

---

## 1. The metabolism of a city

Abel Wolman named the idea in 1965: a city, like an organism, takes in materials and energy and gives out wastes, and its health
depends on handling both (Wolman 1965). The metabolism is the most direct way to see a city as an economy, because every flow is a
supply chain with a hinterland, a transport mode, an institution that keeps it going, and a chokepoint where it can fail.

### 1.1 What one inhabitant needs, by era

| Flow | Walking-city era (to c.1800) | Industrial city (c.1850 to 1900) | Modern city (late 20th to 21st c.) |
|---|---|---|---|
| **Grain / staple food** | ≈ 200 to 250 kg grain a year (Rome: at least 200 kg per resident, Erdkamp via Rickman-type estimates; London: about a quarter of wheat, ≈ 220 kg) | similar calories, more meat, sugar, tea; much imported | ≈ 2 kg of food a day in Wolman's US city (Wolman 1965); a 2017 revision gives 3.8 kg including what is wasted |
| **Water** | wells and carriers: ≈ 5 to 20 litres a day; Rome's aqueducts were far more generous on paper (see §1.3) | London domestic supply ≈ 20 imperial gallons (≈ 90 l) a day in 1850, 28 in 1900 (Hardy 1991) | ≈ 625 kg (625 l) a day in all uses in Wolman's city; domestic use ≈ 120 to 150 l in Europe, ≈ 300 l in the US |
| **Fuel** | wood: Paris ≈ 1.6 stères per head c.1700, ≈ 2.5 by the 1780s (≈, from Jandot's totals); coal: London ≈ 0.8 t per head c.1700 (≈) | London coal ≈ 1 t per head in 1850, ≈ 2.5 t in 1890 (Clay and Troesken, NBER) | ≈ 9.5 kg of fuel a day in Wolman's city (≈ 3.5 t a year) |
| **Total energy** | Paris ≈ 19 GJ per head c.1700, ≈ 30 GJ in 1800 (Kim and Barles 2012) | ≈ 50 to 100 GJ (≈) | rich cities ≈ 100 to 200 GJ; megacities differ by a factor of 28 per head (Kennedy et al. 2015) |
| **Building material** | timber, brick, stone, lime: a house is a decades-long store; whole cities rebuilt after fires | brick by the billion; iron, then steel | steel and cement; megacities' steel use per head differs by a factor of 35 (Kennedy et al. 2015) |
| **Sewage** | cesspits and night soil: ≈ 1 to 1.5 l a day of excreta per person, collected | water-carried: the flush toilet multiplies the volume by the water used | ≈ 120 US gallons (≈ 450 l) a day per person in Wolman's city |
| **Solid refuse** | ash, bones, broken pottery, dung; much reused | ash and horse manure dominate | ≈ 4 lb (≈ 1.8 kg) a day per person in Wolman's city |
| **People** | deaths exceed births: a net demand for migrants | the same until sanitation, then natural increase | natural increase plus migration; the biggest flows are of commuters |

Wolman's hypothetical American city of one million needed in a day about 625,000 tons of water, 2,000 tons of food and 9,500 tons
of fuel, and gave out about 500,000 tons of sewage, 2,000 tons of refuse and 950 tons of air pollutants (Wolman 1965; the per-head
sewage and refuse figures are confirmed in secondary accounts; the other totals are as usually quoted). The proportions are the
point: **water outweighs everything else by two orders of magnitude**, and fuel outweighs food by a factor of five.

### 1.2 Food: hinterlands, rings and the institutions that fed cities

**Transport cost sets the hinterland.** The basic fact behind every pre-railway city: moving grain by land quickly eats its value.
Duncan-Jones's reading of Diocletian's Price Edict (301 AD) is that moving wheat 100 Roman miles by land cost about 55 per cent of
its value, by sea about 1.3 per cent; the edict also set river freight at about five times sea freight (Duncan-Jones 1982, pp.
367-8, as summarised by Scheidel 2013 and others). The often quoted ratio "sea 1 : river 5 : land 30 to 60" is a reading of the
same edict and is †, but the order is not in doubt. Early modern figures say the same: English coastal shipping of coal cost about
0.8 pence per ton-kilometre in 1700, falling to 0.4 by 1785 (Clark and Jacks), far below road haulage.

| Mode (pre-railway) | Relative cost per ton-km | What it meant for a city |
|---|---|---|
| sea | 1 | a port city could draw grain from a whole sea basin (Rome from Egypt and Africa) |
| river or canal | ≈ 5 | inland capitals were built on rivers and fed by canals (Chang'an, Kaifeng, Paris, Baghdad) |
| land, by cart or pack | ≈ 30 to 60 † | grain could come only tens of kilometres by road; bulky low-value goods (firewood, hay) even less |

**Von Thünen's rings.** Johann Heinrich von Thünen (*Der isolierte Staat*, 1826) asked what a farmer should grow at each distance
from a single city on a featureless plain. Each crop's rent is its market price less production and transport cost, and transport
cost rises with distance and with weight and perishability. The answer is concentric rings:

| Ring (from the city outwards) | Use | Why there |
|---|---|---|
| 1 | market gardens, dairy, intensive farming fed by the city's dung | perishable, heavy per unit of value; the city's manure comes back cheaply |
| 2 | managed forest for fuel and timber | heavy and bulky: wood cannot bear long carriage (this surprises modern readers and matches early modern Paris and London) |
| 3 | arable with rotations, grain | grain keeps and bears carriage moderately |
| 4 | three-field system and pasture | lower intensity as rent falls |
| 5 | ranching, livestock | animals walk themselves to market |
| beyond | wilderness | nothing pays |

A river or a canal stretches the rings along it, and a second town makes its own set. Von Thünen's model is the root of all later
land-rent theory (Alonso's bid-rent city of 1964 is the same model turned inward: offices at the centre, then flats, then houses).
The model is a design tool: **put one city on a plain with transport costs by mode, and the land around it sorts itself**.

**A rough sizing (≈, my arithmetic).** With grain yields of ≈ 0.6 to 1 t per hectare net of seed and a fallow year in two or three,
one person's 220 kg needs ≈ 0.3 to 0.6 ha of arable. A town of 10,000 then needs ≈ 30 to 60 km² of arable alone, plus pasture for
draught beasts, woods for fuel and meadows for hay: a radius of ≈ 10 to 15 km if half the land is farmed, which is about a day's
cart journey there and back. A city of 100,000 by land alone would need a radius of ≈ 35 to 50 km, beyond which road carriage
doubles the cost of grain. That is why large cities needed water.

**London c.1300.** The *Feeding the City* project (Campbell, Galloway, Keene and Murphy 1993) reconstructed the grain supply of a
London of perhaps 60,000 to 80,000 people † (some argue higher). The Thames corridor and estuary formed the core of its hinterland,
with the closest price integration; grain came down the river and from north Kent (Faversham), and the city's demand shaped what
was grown across ten counties. Its hinterland was wider by water than by road, as von Thünen would predict.

**Rome (1st and 2nd centuries AD).** Rome of perhaps 750,000 to 1 million people † imported, on estimates that range from about
150,000 tonnes (Erdkamp's minimum, at 200 kg a head) through 200,000 (Rickman) and 237,000 (Mattingly and Aldrete) to 400,000
tonnes a year (a reading of Josephus and Aurelius Victor) (summarised from the Cura Annonae literature). Josephus said Africa
supplied eight months of the year and Egypt four, so Egypt supplied about a third †. Part went as a free monthly ration (the
*frumentatio*) to a list of citizens: Augustus fixed it at about 200,000 recipients, each receiving 5 *modii* (≈ 33 kg) a month.
The rest came through the market, with the state's prefect of the grain supply (*praefectus annonae*) contracting shippers, granting
privileges to merchants who built ships for the grain trade, and holding stocks in the warehouses (*horrea*) at Ostia, Portus and
in the city. Oil came the same way: Monte Testaccio, a hill made entirely of broken oil amphorae from Spain and North Africa, holds
perhaps 53 million of them (≈ 6 billion litres of oil), with up to 130,000 dumped a year at the peak in the late 2nd century; many
are stamped as deliveries to the annona (Monte Testaccio studies, as summarised). The lesson for design: **the largest city of the
ancient world was a public-private supply chain run by a state office, using a sea, with a chokepoint at the harbour mouth**. When
the grain fleet was late, Rome rioted.

**London in the 18th century.** London grew from about 575,000 in 1700 to about 960,000 in 1801 (Wrigley; Finlay and Shearer give
≈ 490,000 for 1700 †), about a tenth of England's population. Its food came by a set of specialised chains, each a different shape:

| Good | Where from | How | Numbers |
|---|---|---|---|
| grain and flour | the Home Counties and East Anglia by coaster and Thames barge; Kent | corn factors at Bear Key and the Corn Exchange (Mark Lane, 1747) | ≈ 1 quarter of wheat a head a year |
| cattle and sheep | Scotland, Wales, the north, fattened in the Midlands and Home Counties | droved on the hoof to Smithfield, slaughtered in the city | about 74,000 cattle and 570,000 sheep a year in the 1740s (figures in several secondary sources, †); 76,210 cattle and 514,700 sheep in 1732 (Youatt); ≈ 1.7 million animals a year by the 1820s |
| vegetables and fruit | market gardens in Middlesex, Surrey, Essex, fed by London dung | carts to Covent Garden | the first von Thünen ring, made by the city's own manure |
| milk | cows kept in the city and on its edge | carried and sold door to door | a perishable that forced production inside the city |
| fish | the North Sea, the Thames | Billingsgate | |
| coal (fuel, §1.4) | Newcastle and Sunderland | the coastal colliers | |

Each was regulated: chartered markets, a bread assize setting the price or weight of the loaf, inspectors of weights and measures,
the City's monopoly of markets within its bounds. Wrigley's argument (1967) is that this demand restructured English agriculture
and transport: London's market drew specialisation across the whole country.

**Paris in the 18th century.** Paris (≈ 500,000 to 650,000 †) was fed through a deliberately managed system that Steven Kaplan
calls "provisioning": the *police des grains*, which treated bread as a public matter. Grain came from the Beauce, the Brie, Picardy
and down the Seine and its tributaries; merchants needed licences; the zone within a set distance of Paris was reserved for the
capital's supply; the Halle au blé (rebuilt 1763 to 1767) was the central market; and over the century, as Kaplan shows, flour
overtook grain in the trade and millers overtook merchants (Kaplan 1984; 1996 on the bakers). The state's legitimacy rested on the
price of the four-pound loaf, and the "flour war" of 1775, after a trial of free grain trade, is the standard example of what
happens when a provisioning regime is changed abruptly.

**Edo (1720s).** Edo reached roughly a million by the 1720s (the Tokyo metropolitan government cites ≈ 1.3 million in 1721;
other sources date a million to 1733 †). It was fed largely by rice shipped by sea from Osaka and the north, sold through the
rice brokers who turned the daimyo's tax rice into cash, and by vegetables from farms around the city fertilised with the city's
night soil (§1.6).

**The industrial break.** Railways and steamships cut land transport costs by an order of magnitude and refrigeration (refrigerated
rail cars in the 1870s and 1880s, refrigerated ships to Britain from Australia and Argentina from 1880) removed perishability as a
limit. The von Thünen rings did not vanish; they became continental. Chicago's hinterland was the American West (§2).

### 1.3 Water

| Stage | Technique | Per head | Example |
|---|---|---|---|
| river and wells | carry from the river, dig wells, collect rain in cisterns | ≈ 5 to 20 l a day | most cities until the 19th century |
| gravity aqueducts to public fountains | channels on a steady fall from springs or rivers; public fountains, baths, a few private connections | nominally hundreds of litres a day †, much of it running to waste | Rome: 11 aqueducts by 226 AD |
| conduits and water companies | lead or wooden pipes from conduits; private companies sell piped water to paying houses a few hours a week | tens of litres | London's Great Conduit (1245); the New River (1613, built by Hugh Myddelton, ≈ 60 km from Hertfordshire springs, cost £18,524) |
| pressurised municipal supply | steam pumps, reservoirs, iron mains, constant supply | ≈ 90 to 150 l | London domestic ≈ 20 imperial gallons a day in 1850, 27.8 in 1900; total supply grew from 28.8 million gallons a day in 1828 to 202 million in 1898 (Hardy 1991) |
| long-distance aqueducts and filtration | dams and tunnels from distant catchments; sand filtration, then chlorination (from about 1908) | ≈ 300 to 600 l in all uses | New York's Croton aqueduct (1842): built for 60 to 90 million US gallons a day †; 18 million used at first by ≈ 300,000 people |

**Rome's aqueducts.** Frontinus, water commissioner around 97 AD, recorded 14,018 *quinariae* delivered by nine aqueducts and
about 10,000 more being stolen. Converting a quinaria (a pipe size, not a volume) to flow is the whole dispute: Herschel's
conservative reading gives ≈ 84 million gallons a day; popular accounts give ≈ 1 million m³ a day for the eleven, ≈ 1 m³ a head;
studies of channel size and travertine (Keenan-Jones et al. 2015) put flows lower. **† ≈ 300 to 1,000 litres a head a day
nominal.** The shape is not in doubt: continuous flow to fountains, baths and a few paying private connections, the surplus
flushing the sewers. A public good with rationed private access, whose main problem was theft.

**Edo** stood on reclaimed land with salty wells, so it imported water early: the Tamagawa aqueduct (1653-54) brought it ≈ 43 km
by open channel and then wooden and stone pipes to street wells, with more than 30 branch canals irrigating farms on the way.

**Cholera** taught that water without drainage poisons a city: Snow's Broad Street pump (1854), and Hamburg in 1892 (about 8,600
dead while neighbouring Altona, which filtered its water, was spared). Each is **an external effect between neighbours on a shared
chain**: one intake downstream of another's sewer.

**Rule of thumb (≈).** A walking city lives at ≈ 10 l a head; a city with piped water and flush toilets needs ten to thirty times
that, and the water then has to go somewhere: **piped water before sewers creates the crisis that sewers solve**.

### 1.4 Fuel

| City | Fuel | Source and route | Numbers |
|---|---|---|---|
| Rome | wood and charcoal | Italian woods, by river and coast | unquantified; baths alone burned great quantities |
| Kaifeng (11th c.) | coal, beside wood and charcoal | Shanxi and Hebei coalfields, by canal and cart | Northern Song saw a wood fuel crisis and wide use of mineral coal in the capital (Hartwell 1962, 1967); iron output ≈ 75,000 to 125,000 t a year c.1078 † |
| Paris (16th to 19th c.) | firewood, then charcoal | the Morvan forest, floated down the Yonne and Seine as loose logs and then rafts (*trains de bois*) | ≈ 3,000 rafts a year c.1700, 5,000 by c.1800; Paris burned ≈ 315,000 stères a year in the late 16th century, 830,000 c.1700, 1.5 million by the 1780s (Jandot 2016, as summarised) |
| London (1580 to 1900) | sea coal | Tyne and Wear pits by collier ships down the North Sea coast | ≈ 450,000 t a year by 1700 (a figure attributed to Wrigley, ≈); ≈ 1 t a head in 1850, ≈ 2.5 t a head in 1890 (Clay and Troesken); London probably burned more coal than any other city (Cavert 2016) |
| industrial cities | coal by rail, town gas from coal (London from 1812), then electricity | | Manchester and Chicago ran on rail coal |
| modern cities | oil, gas, electricity | pipelines, grids, tankers | megacities in 2010: 6.7 % of world population, 9.3 % of electricity, about 10 % of gasoline (Kennedy et al. 2015) |

**London's coal is a model chokepoint chain.** Coal was dug on Tyneside by miners bound to annual contracts, carried in keels to
the colliers, shipped down the coast (the tonnage of coal from the north-east often exceeded all of England's imports), unloaded by
coal-heavers in the Pool of London, measured by sworn meters, sold through the Coal Exchange, and taxed by the City (coal dues
paid for rebuilding St Paul's and the City churches after 1666). The Newcastle "hostmen" ran a cartel at the mouth, the "Limitation
of the Vend" restricted supply, and London buyers complained of combinations at both ends. The chain had **a monopoly at the
pit-head port, a pulse with the sailing season and war (privateers, press gangs), a tax at the city end, and a pollution cost that
fell on everyone** (Cavert 2016 on smoke and its politics). Wrigley's argument (02zzi §3.8) begins here: London's coal is the first
large city fuelled by mineral energy.

**Paris's wood is a model pulse chain.** Wood was cut in the Morvan in winter, stacked by streams, released in a spring flood when
dams were opened (*flottage à bûches perdues*), caught and sorted at Clamecy, bound into rafts and floated to Paris, where it was
stacked in the wood ports. A whole region's forest was managed as Paris's fuel ring, at the distance von Thünen's model would
forbid by land and allow by water.

### 1.5 Building materials

- **Local geology and fuel decide the material:** mud brick with fired brick and bitumen in Mesopotamia; tuff, brick and concrete
  (lime and pozzolana) in Rome; timber and thatch in medieval northern Europe until fires and bylaws forced tile and brick;
  Amsterdam on wooden piles driven into peat; Edo in wood, burning repeatedly (the Meireki fire of 1657 killed tens of thousands †).
- **Fire changes materials.** Rome 64 AD, London 1666, Chicago 1871: each brought building codes, brick or stone, wider streets,
  fire insurance (the Fire Office, London 1680) and brigades.
- **Industrial cities ran on brick and then steel:** Chicago's balloon frame (standard sawn pine and machine-made nails, from the
  1830s) let unskilled labour build houses; the steel-frame skyscraper followed in 1885. Megacities' steel use per head differs by
  a factor of 35 (Kennedy et al. 2015), a sign of where each is in its building cycle.
- **Housing is a stock, not a flow:** rents and crowding follow from whether building keeps pace with migrants. Rome's *insulae*
  (blocks of five or six storeys let by the room), Edo's back-alley *nagaya* and New York's 1879 "dumbbell" tenements are the same
  answer to the same pressure.

### 1.6 Waste and sanitation

| Regime | What happens | Example | What it depends on |
|---|---|---|---|
| **night soil as a resource** | excreta collected from privies and cesspits and sold to farmers as fertiliser; the city returns fertility to its first ring | Edo, Osaka, Chinese cities; Paris's *poudrette*; London's nightmen | a market in manure; farms near enough to carry it; no cheaper fertiliser |
| **cesspits and dumps** | waste accumulates; scavengers and rakers paid by the parish or city | medieval and early modern Europe; Paris's Montfaucon dump | |
| **water-carried waste into rivers** | flush toilets (spreading after the 1850s) send waste into old storm drains and the river | London in the 1840s and 1850s | piped water; drains |
| **intercepting sewers** | trunk sewers carry waste beyond the city | Bazalgette's London (1858-75): about 1,100 miles of street drains feeding 82 miles of main intercepting sewers, discharging east of the city | a public authority (the Metropolitan Board of Works, 1855), a rate, a crisis (the Great Stink, 1858) |
| **treatment** | sewage farms, then biological treatment (activated sludge, 1914) | | electricity, chemistry |
| **municipal solid waste** | collection, landfill, incineration, recycling | ≈ 1.8 kg a head a day in Wolman's city | |

**Edo's night soil market** is the best documented case of waste as a traded good. By the start of the 18th century farmers and
dealers paid for human waste. The rights belonged to the landlord of a tenement (urine often to the tenants), and were sold under
annual contracts, sometimes for rice or vegetables; historians cite the night soil of ten households for a year as worth two to
three *bu* of silver, over half a *ryō*, when a ryō bought a year's grain for one person (Tajima, as reported). In the later 18th
century rival collectors bid prices up, and in 1789 the villages around Edo petitioned the shogunate over the price (Kumazawa 1985).
Waste here is a **joint product** of the city that closes the nutrient loop and has owners, contracts and price disputes.

**London lost its night soil market.** Cheap imported guano from the 1840s and growing distance to farms made night soil worth less
than the cost of carting it, cesspits overflowed, and the new flush toilets sent waste into the Thames, from which the water
companies drew. The Great Stink of 1858 made Parliament act within weeks. This is a **paradigm switch forced by the collapse of a
market** (a substitute fertiliser), with a public works answer.

**Horses** were the industrial city's other waste stream. Sanitary experts c.1900 put a city horse's manure at 15 to 30 lb a day
(about 22 on average) (Tarr 1971); New York had somewhere between 100,000 and 200,000 horses around 1900 †, giving ≈ 1,000 to
2,000 tons of manure a day on the streets, plus dead horses, urine and flies. The motor vehicle was welcomed as a sanitary reform.

### 1.7 People: the urban graveyard

Until the late 19th century most large cities had more deaths than births: crowding, contaminated water, and diseases that need a
dense host population (smallpox, measles, typhus, tuberculosis, cholera). London is the best measured case. Wrigley's "simple
model" (1967) computed that London, to grow as it did between 1650 and 1750, needed more than 8,000 net migrants a year beyond its
own natural decrease; on his reckoning a large share of all English adults (often quoted as one in six) spent part of their lives
there. The city was therefore **a demographic sink and a social mixer**: it drew young adults from the countryside, trained them
(apprenticeship, service), killed many, and sent some back with new habits and connections. The switch to natural increase came
with clean water, sewers, and later vaccination and antibiotics: by 1900 big cities in Europe and North America could grow from
their own births.

---

## 2. Cities through time

| City | When | Population (†) | What fed it | What it lived by | Key institutions | Key infrastructure |
|---|---|---|---|---|---|---|
| **Uruk** | c.3300-2900 BC | ≈ 20,000 to 50,000 (some say 40,000 by 3100 BC, 80,000 to 90,000 with its surroundings) | irrigated barley, dates, sheep from the alluvium | temple and palace estates; wool textiles; long-distance trade for metal, stone, timber (Algaze) | temple households; rations; scribes; the first writing (proto-cuneiform), used for accounts | canals; the city wall (≈ 9 km by c.2900 BC); ≈ 250 ha in the Late Uruk period, larger later |
| **Rome** | 1st-2nd c. AD | ≈ 750,000 to 1 million | Egyptian, African, Sicilian grain by sea; Spanish and African oil | the empire's taxes and rents spent in the capital; services, building, crafts | the annona; patron and client; collegia (trade associations); the dole | Ostia and Portus; 11 aqueducts; *horrea*; insulae; Cloaca Maxima |
| **Chang'an** (Tang) | 7th-9th c. | ≈ 800,000 to 1 million in ≈ 84 km² walls | tax grain from the Yangzi by the Grand Canal and Wei river | the court, officials, the army; the Silk Road | 108 walled wards with gates shut at night; two official markets (East and West) under market officials, with fixed hours and price records | the grid; canals; granaries |
| **Kaifeng** (Northern Song) | 960-1127 | ≈ 1 million (Rozman), "more than a million" in 1102-06 | Yangzi rice by the Bian canal (annual tax grain of several million *shi* †) | the court; commerce; crafts; printing | wards opened up, shops on every street, night markets; guilds (*hang*); paper money (jiaozi from Sichuan, 1020s) | canals; coal as household fuel |
| **Baghdad** (Abbasid) | 762 to 10th c. | ≈ 300,000 to 1 million (840,000 in one estimate; texts only, the city is built over) | Sawad irrigated grain; Tigris and Euphrates boats | caliphal court; the hub of routes from India to the Mediterranean | suqs by trade in Karkh; money changers (*jahbadh*); cheques (*sakk*) and transfer bills (*suftaja*); paper mills (from c.794) | the Round City (762-66); canals linking Tigris and Euphrates |
| **Venice** | c.1300-1500 | ≈ 100,000 to 120,000 before 1348 | grain by sea from Apulia, the Black Sea, Sicily; a state grain office | carrying trade and credit between Byzantium, the Levant and Europe; salt; glass | the commune and Great Council; state galley convoys (*mude*) auctioned to merchants; the *colleganza* partnership | the Arsenal: 1,500 to 2,000 workers normally, 4,000 to 5,000 in war (16,000 at times is an often repeated figure †); "perhaps the largest industrial plant of that time" (Lane) |
| **Florence** | c.1338 | ≈ 90,000 to 120,000 (Villani); ≈ 40,000 to 50,000 after the Black Death | Tuscan grain plus imports from Sicily and Apulia, often through its own merchant-bankers | woollen cloth (Villani: ≈ 30,000 people paid by the cloth industry; ≈ 200 workshops and 70,000 to 80,000 cloths a year, as usually quoted †); banking | the *Arti* (guilds), which ran the commune; the florin (1252); the Bardi and Peruzzi, who failed in the 1340s after lending to Edward III | |
| **Bruges** | c.1300-1450 | ≈ 40,000 to 46,000 | Flemish and French grain; Baltic grain by Hanse ships | the market of northern Europe: Flemish and English cloth, wool, Baltic and Italian goods | foreign nations' houses (the Hanseatic *Kontor*, Italian lodges); brokers and hostellers; the "bourse" (named after the Van der Beurse inn where merchants met) | the Zwin channel to the sea (its silting ended Bruges's role) |
| **London** | 1550-1800 | ≈ 70,000 to 75,000 (1550), 200,000 (1600), 490,000 to 575,000 (1700), ≈ 960,000 (1801) | §1.2; coal §1.4 | port, court, Parliament, law, finance, crafts, the season; re-exports | livery companies; the Royal Exchange (1571); the Bank of England (1694); insurance (Lloyd's) | the Thames and the Pool; the New River (1613); London Bridge (the only one until 1750) |
| **Amsterdam** | 1600-1700 | ≈ 60,000 (1600), ≈ 175,000 (1650), ≈ 200,000 (1700) (de Vries and van der Woude) | Baltic grain (the "mother trade"); Dutch dairy | the entrepôt of Europe: staple goods stored, graded and re-exported; shipping; the VOC | the VOC (1602); the Wisselbank (1609: 708 account holders in 1611, 1,202 by 1620); the Bourse (1611), where VOC shares traded; printed price currents | canal rings (1613 onwards); warehouses; piles |
| **Manchester** | 1770-1850 | ≈ 23,000 (1773; another estimate 43,000 †), 75,000 (1801), 303,000 (1851; 401,000 with Salford) | Lancashire, Irish and imported food by canal and rail | cotton spinning: mills from 3 to 19 in the 1790s, 108 at the peak (1853); merchants and warehouses | the Cotton Exchange; factory discipline; working-class housing by speculative builders | the Bridgewater canal (1761); the Liverpool and Manchester railway (1830); steam power |
| **Chicago** | 1833-1900 | 350 (1833), 29,963 (1850), 298,977 (1870), 1,099,850 (1890), 1,698,575 (1900) | its own hinterland: it was the food hub | grain, lumber and meat for the East and Europe; rail; manufacturing | the Board of Trade (1848); grain grading (1856); futures; the Union Stock Yards (1865); the packers | the I&M canal (1848); railways; elevators; refrigerator cars |
| **New York** | 1900-1960 | 3.4 million (1900), ≈ 7.9 million (1950) | national markets by rail and sea | port; finance; garment industry; publishing; headquarters | Wall Street; the Port Authority (1921); city government | Croton and Catskill water; Bazalgette-scale sewers; subway (1904); electricity (Pearl Street, 1882); skyscrapers |
| **Tokyo** | 1600 to now | Edo ≈ 1 million (1720s); Tokyo ≈ 33 million (UN 2025) | Edo: sea rice from Osaka; now global | Edo: the shogun's capital, with daimyo required to live there in alternate years (*sankin-kōtai*); now finance, headquarters, manufacturing | Edo: rice brokers, merchant houses (Mitsui, from 1673); now ministries and keiretsu | Tamagawa aqueduct (1653); rail: Shinjuku ≈ 3.5 million passengers a day across all operators |
| **Shanghai** | 1842 to now | ≈ 3 to 3.5 million by the 1930s ≈; ≈ 25 to 30 million now | the Yangzi basin; global | the treaty-port gateway to China; then industry; since 1990 finance (Pudong) and the world's busiest container port | foreign concessions with their own councils; compradors; now state planning | the Bund and docks; now metro, port, airports |

Notes on what each shows, in the vocabulary of 02zzi and economy_web.md:

- **Uruk: the first city is a household writ large.** The temple and palace were great estates that fed dependants with rations
  of barley, oil and wool, recorded on clay. The mass-produced bevelled-rim bowls found in their millions are usually read as
  ration bowls †(others read them as bread moulds for feasts). Writing was invented to keep these accounts. Guillermo Algaze argues
  that Uruk grew because the alluvium had cheap water transport and high yields, and because it traded textiles for the metals,
  stone and timber it lacked: a **chokepoint economy** (no local stone, metal or timber) solved by exchange and colonies upstream.
  Redistribution (Polanyi) came before markets.
- **Rome: the parasitic and the productive city.** Rome lived on the taxes and rents of an empire (the "consumer city" of Weber and
  Finley †, disputed by those who stress its crafts and services). Its economy is still instructive: a dole for some, markets for
  the rest, contracting for the state, and a harbour as the chokepoint.
- **Chang'an to Kaifeng: the controlled market opens.** Tang Chang'an confined trade to two supervised markets with set hours, inside
  a city of walled wards closed at night. Over the late Tang and Song the ward walls fell, shops opened onto streets, night markets
  ran, and commercial taxes rose above the land tax in importance: the "medieval urban revolution" (Elvin, Shiba). Kaifeng is the
  first city known to have used coal as a common fuel and among the first to use paper money. **The same city size can be organised
  by supervision or by markets**, and the switch changes everything inside it.
- **Baghdad: a hub on the routes.** Built as a planned capital, it grew beyond its walls into the commercial Karkh. Its credit
  instruments let merchants move value across the caliphate without coin, and its paper mills made a cheap information good.
- **Venice: the state as merchant.** Venice owned the galleys, auctioned voyages to syndicates, ran its own grain office and built
  ships in the Arsenal on something like an assembly line (galleys fitted out as they were towed past stores). **A city of little
  land lives entirely by carrying and credit** (02zzi §3.9's maritime trading cities).
- **Florence: an industrial city before industry.** Wool from England, alum from the Levant, dyes, and a putting-out system with
  thousands of wage workers who could not form guilds of their own (the Ciompi revolt of 1378). Its banks were the deepest
  financial network of the 14th century, and their failure shows **default chains** (02zzi §3.5) at city scale.
- **Bruges: a market as an institution.** Bruges's role came from hosting foreign merchants under its law, with brokers, hostellers
  who doubled as bankers, and a meeting place. When its channel silted and Antwerp offered better terms, the market moved: **a
  hub's advantage is an equilibrium, not a resource**.
- **London: growth by drawing a nation.** Port, court and capital in one; its demand specialised England's agriculture and
  transport (Wrigley 1967).
- **Amsterdam: the entrepôt.** It made money not by producing but by storing, grading, pricing and re-exporting the goods of
  others, with the cheapest shipping, the best information (printed price currents) and the most trusted bank money (the
  Wisselbank's bank guilders traded at a premium over coin). A city as **an information and trust good**.
- **Manchester: the shock city of industry.** Coal, canals, cotton, steam, and housing built faster than drains or water. Engels's
  *Condition of the Working Class in England* (1845) describes the result.
- **Chicago: the hub that made commodities.** Cronon's *Nature's Metropolis* (1991) is the key text. Chicago sat between the West's
  raw materials and the East's markets at the meeting of lake, canal and (from 1848) railways. Three chains:
  - **Grain:** before 1850 grain moved in sacks, each farmer's lot kept separate. Steam elevators lifted it in bulk into bins; in
  1856 the Board of Trade set grades (white winter, red winter and spring wheat, each with quality standards), so an elevator could
  give back an equal quantity of equal grade instead of the farmer's own grain. Ownership separated from the physical grain;
  elevator receipts became money-like; trading in "to arrive" contracts became futures. Shipments more than tripled between 1853
  and 1856, to 21 million bushels in 1856 (as quoted from Cronon). **Grading turned a good into a commodity.**
  - **Lumber:** white pine from Michigan and Wisconsin floated down rivers to lake ports and came to Chicago by schooner, to be
  sold to the treeless prairie by rail; by the 1850s Chicago was the largest lumber market in the world (Cronon's lectures), with
  receipts in the 1880s and 1890s of the order of billions of board feet ≈. The forest was cut over in a generation.
  - **Meat:** the Union Stock Yards opened on 25 December 1865 and received 1.29 million hogs and 384,000 cattle in 1866; cattle
  receipts passed a million a year by 1876-79; by the 1920s more than 15 million animals a year passed through † (summarised from
  the Encyclopedia of Chicago and Union Stock Yards histories). Swift's refrigerator cars (from 1878) let dressed beef replace live
  cattle on the rails, and the packers used "everything but the squeal": joint products (hides, glue, lard, fertiliser) paid for
  the line.
  - Cronon's lesson: **the city and its hinterland are one system**; the city makes the country into a market and the market
  hides the land and labour behind the price.
- **New York: the vertical city.** Its 20th-century form needed every layer of §5: distant water, intercepting sewers, electricity
  for lifts and lighting, a subway to bring a million workers into lower and midtown Manhattan, and the telephone to coordinate
  offices.
- **Tokyo: a capital by statute, then a metropolis by rail.** Edo was a city made by an administrative rule: the daimyo's
  alternate residence put perhaps half the population in samurai households ≈, and their spending built the merchant economy.
  Modern Tokyo is a rail metropolis: private railways built lines and department stores and suburbs together.
- **Shanghai: a gateway city.** Its growth came from being the port where China met the world, under foreign concessions; after 1990
  it was rebuilt as a planned global city.
- **21st-century megacities and global cities.** The UN's 2025 revision (with a new, density-based definition) counts 33 cities
  above 10 million, against 8 in 1975, with Jakarta (≈ 42 million), Dhaka (≈ 37 to 40 million) and Tokyo (≈ 33 million) the largest,
  and 45 per cent of the world's 8.2 billion people in cities (UN DESA 2025). Many megacities grow faster than their infrastructure:
  UN-Habitat counts roughly a billion people in slums ≈. **Saskia Sassen's** *The Global City* (1991) argued that globalisation
  dispersed production but concentrated control: New York, London and Tokyo became the places where the producer services that run
  a global economy (finance, law, accounting, advertising, consulting) are produced and traded, so the most global activity is the
  most centralised. The same cities polarise: highly paid professionals and the low-paid service workers who serve them. Global
  cities are ranked by networks of firms' offices (the GaWC rankings) rather than by size: Lagos is larger than Zurich, Zurich is
  more global.

---

## 3. Why cities grow

### 3.1 Five reasons a place becomes a city

| Reason | What it is | Examples | Shape (economy_web.md) |
|---|---|---|---|
| **a surplus collected** | rents and taxes from a large territory are spent where the collector lives | Rome, Chang'an, Edo, Versailles-era Paris, Washington | redistribution; a chokepoint of authority |
| **a break in transport** | goods change mode (sea to river, river to road, lake to rail) and need storage, handling, finance | Rome's Portus, Bruges, Amsterdam, Chicago, Shanghai | chokepoint; increasing returns |
| **a market for a region** | the central place where a region's households trade (Walter Christaller's central place theory, 1933: a nested hierarchy of hamlet, village, market town, regional city, capital, spaced by the range of the goods each sells) | every market town | increasing returns; a pulse (market day) |
| **a resource or a production advantage** | coal, ore, water power, a skilled trade | Manchester, Sheffield, Pittsburgh, Florence's cloth | assembly; long skill |
| **agglomeration itself** | once there, density pays (§3.2) and the city grows because it is big | London, New York, Tokyo | increasing returns |

Most great cities combined several: London was port, capital and market. Pre-industrial societies rarely sustained more than
10 to 15 per cent of their population in cities (Bairoch), because the farm surplus per farmer was small. Industrial and
agricultural productivity removed that ceiling.

### 3.2 Agglomeration economies

Alfred Marshall (*Principles of Economics*, 1890) named three reasons firms cluster: **a pooled labour market** (workers with the
right skills are near, and workers can find employers); **shared suppliers** (specialised inputs and services that a single firm
could not support); and **knowledge spillovers** ("the mysteries of the trade become no mysteries; but are as it were in the
air"). Duranton and Puga (2004) restate them as **sharing** (of indivisible facilities, suppliers, risks), **matching** (better
matches between workers and jobs, buyers and sellers) and **learning** (the creation and spread of knowledge). Economists also
separate **localisation** (benefits of many firms in one industry) from **urbanisation** (benefits of a large, diverse city).

How big are they?

| Estimate | Finding | Source |
|---|---|---|
| doubling city size | productivity rises 3 to 8 per cent (the "consensus" in a major review) | Rosenthal and Strange 2004 |
| doubling city size, France, controlling for worker sorting | 2 to 7 per cent, by sector and method | Combes et al. 2008 onwards |
| doubling employment density, US states | labour productivity rises several per cent; later estimates that net out sorting about halve it | Ciccone and Hall 1996; later work as summarised by the New York Fed |
| doubling city size | ≈ 15 per cent more per head in wages, patents and also crime (the "15 per cent rule") | West 2017, from Bettencourt et al. 2007 |

The two literatures disagree in size (2 to 8 per cent against 15) mostly because the scaling work does not separate the effect of
city size from who chooses to live in big cities (sorting); both say the effect is positive and persistent. **Agglomeration has
costs:** rents, congestion, commuting time, pollution, disease (until sanitation), crime. The size of a city is a balance between
the two, and the costs are what the infrastructure layers of §5 push back.

### 3.3 Jane Jacobs: cities as the source of new work

Jacobs's *The Economy of Cities* (1969) and *Cities and the Wealth of Nations* (1984) make four claims:

1. **New work is added to old work.** A new product or service starts as a division of an existing one: a brassiere maker grows out
   of dressmaking, the 3M company out of sandpaper. The more and more varied existing work a place has, the more combinations it
   can make. This is why diverse cities (urbanisation economies) generate innovation more than one-industry towns.
2. **Import replacement.** A city grows explosively when it starts making locally what it used to import, which frees its earnings
   to import new things; the new local production then feeds further divisions of work. Cities trade above all with other cities.
3. **City regions.** A vigorous city reshapes its surrounding region (suburbs, markets, transplanted industry), while regions that
   only supply distant cities (supply regions, plantations, "transplant" regions) stay undeveloped.
4. **Cities before agriculture.** Her claim that cities came first and agriculture was invented in their hinterlands is now
   generally rejected by archaeologists, but the general point (that dense exchange drives invention) has strong support in the
   scaling data (patents scale super-linearly).

For a simulator, the first two are mechanisms, not just observations: **new methods arise by combining methods present in the same
place, and a place gains when it substitutes its own production for an import.**

### 3.4 Urban scaling laws

Bettencourt, Lobo, Helbing, Kühnert and West (2007) showed that many urban quantities Y follow a power law in population N:
Y = Y₀ N^β, across cities of one country at one time. The values below are those usually reported from the paper's Table 1 (the
paper itself could not be opened in this session; the grouping into β ≈ 1.2, ≈ 1 and ≈ 0.8 is confirmed by its abstract, the
decimals should be checked against it before reuse).

| Group | Quantity (country) | β |
|---|---|---|
| **super-linear: socio-economic** | new patents (US) | ≈ 1.27 |
| | inventors (US) | ≈ 1.25 |
| | private R&D employment (US) | ≈ 1.34 |
| | "supercreative" employment (US) | ≈ 1.15 |
| | total wages (US) | ≈ 1.12 |
| | GDP (China ≈ 1.15; EU ≈ 1.26; Germany ≈ 1.13) | |
| | total bank deposits (US) | ≈ 1.08 |
| | new AIDS cases (US) | ≈ 1.23 |
| | serious crimes (US) | ≈ 1.16 |
| **linear: individual needs** | total employment, housing, household electricity and water use | ≈ 1.0 |
| **sub-linear: infrastructure** | petrol stations (Germany) | ≈ 0.77 |
| | petrol sales (US) | ≈ 0.79 |
| | length of electrical cables (Germany) | ≈ 0.87 |
| | road surface (Germany) | ≈ 0.83 |

**What it means.** With β ≈ 1.15, a city ten times larger produces about 14 times the wages and patents in total, so about 40 per
cent more per head; with β ≈ 0.85, it needs only about 7 times the roads and cables, so about 30 per cent less per head. Bettencourt
(2013) derives the values from a model of cities as networks of social interaction overlaid on infrastructure: interactions per
person grow with density, infrastructure is shared. The pace of life also rises with size: walking speed, the spread of disease and
of ideas. West's argument (*Scale*, 2017) is that super-linear growth produces finite-time singularities, so cities must innovate at
an accelerating rate to avoid stagnation.

**Ancient cities follow the same laws.** Ortman and colleagues found in more than 1,500 prehispanic settlements in the Basin of Mexico
that settled area grows with population with an exponent between 2/3 and 5/6, and that monument building and house size show
increasing returns (Ortman et al. 2014, 2015): the scaling comes from people living closer together and interacting more, not from
modern technology. **Caveats:** results depend on how a city is bounded (administrative city or metropolitan area); some exponents
fall close to 1 under other definitions (Arcaute et al. 2015 on British cities); and scaling describes a cross-section, not the path
of one city as it grows.

### 3.5 What stops growth

- **Supply cost:** the hinterland's edge, set by transport (§1.2). Bruges lost its channel; Rome lost its fleet.
- **Disease:** the urban graveyard (§1.7), and plagues: Florence lost perhaps half its people in 1348.
- **Congestion and commuting:** the travel time budget. Studies collected by Schafer and Victor find people travel on average about
  an hour a day (45 to 90 minutes), across cultures and eras (the "Marchetti constant", from Zahavi's work); London and New York
  average about 46 and 41 minutes each way. Each faster transport mode enlarges the city that fits in the budget (§4.2).
- **Housing:** rents rise when building lags migration; slums form when it lags far.
- **Political:** loss of the court or the empire (Rome after 330 and 410; Chang'an after the Tang). A capital city lives on a flow
  that can be redirected.
- **Hub shift:** a better-placed rival (Antwerp over Bruges, Amsterdam over Antwerp after 1585, Chicago over St Louis after the
  railways; in 1850 St Louis handled twice Chicago's grain).

---

## 4. The city's own industries and services

A city exports goods and services to its hinterland and other cities, and supplies itself. The second part (the "non-basic" sector
in the economic base model) is usually larger: most people in any city work for other people in the same city.

### 4.1 Trades and services by era

| Domain | Pre-industrial city | Industrial city | Modern city |
|---|---|---|---|
| **food trades** | bakers (price fixed by an assize), butchers, brewers, millers, cooks' shops and street food; most households bought bread | factory bread, flour mills, breweries, the packers | supermarkets, restaurants, delivery |
| **crafts** | guilds (Florence's *Arti*, London's livery companies, Song *hang*, Roman *collegia*) controlling entry, apprenticeship (7 years in London), quality, prices, and often city government | factories replace much craft; craft survives in luxury trades and repair | design, specialised manufacture, maker trades |
| **markets** | the market place and market day; chartered fairs; specialised markets (Smithfield, Billingsgate, Covent Garden; Chang'an's two markets) | wholesale produce markets; exchanges for commodities | wholesale hubs at the edge; online markets |
| **finance** | money changers, pawnbrokers, merchant bankers; bills of exchange; deposit banks (Venice, the Wisselbank) | joint-stock banks, stock exchanges, insurance, clearing houses (London 1773) | the financial district; global markets (Sassen) |
| **information** | criers, notaries, scribes; printing (from the 1450s in Europe, Song China far earlier); newspapers and price currents | the press, the telegraph, advertising | telecoms, media, software |
| **retail** | shops on the street front, often workshop and shop in one; pedlars | the department store (Paris's Bon Marché, 1852; Mitsukoshi in Tokyo, from the Mitsui drapery of 1673) | malls, chains, e-commerce |
| **transport within the city** | porters, carters, watermen (London's Thames watermen), sedan chairs, hackney coaches (licensed in London from 1654) | omnibus, tram, underground, cab | metro, bus, taxi, ride hailing, delivery |
| **housing and construction** | the building trades (masons, carpenters, bricklayers); speculative builders; ground rents and leases | mass speculative building; tenements; building societies | developers, mortgage finance, public housing, zoning |
| **utilities** | water carriers; conduit keepers; nightmen; scavengers | water companies, gas companies (London 1812), electricity (1880s), telephones (1870s on) | grids, networks, regulated utilities |
| **public health** | plague orders and quarantine (Venice's lazaretto, 1423); hospitals as charity | medical officers of health (London from 1848), sanitary boards | public health departments, hospitals |
| **order** | the watch, ward constables, guild and market courts; the city's own law | professional police (London's Metropolitan Police, 1829) | police, courts, regulators |
| **schooling** | church and guild schools; universities (Bologna, Paris) | compulsory schooling (England 1870-80) | universities as city industries |
| **entertainment** | festivals, processions; Rome's games and baths; theatres (London's Bankside), taverns, coffee houses (London's first 1652) | music halls, sport, cinema | culture, tourism, sport as export industries |

**Guilds** deserve a note because they are the institution that most often stood between a city's market and its producers. Their
functions combined restriction (who may practise, how many apprentices, minimum prices) with public goods (training, quality marks,
mutual insurance, a voice in government). Economic historians still dispute whether they were mainly rent-seeking cartels
(Ogilvie 2019) or mainly solutions to quality and training problems (Epstein 1998) †. In design terms a guild is **a club good
with exclusion**, and the dispute is the design question: who benefits from limited entry.

### 4.2 Transport within the city, and the city it makes

The size of the built-up area follows the speed of the cheapest daily transport, because people keep their travel time about
constant (§3.5). The radii below are my arithmetic (≈) at half an hour each way, with typical speeds.

| Mode | When | Speed (≈) | Radius in 30 min (≈) | Built-up area that implies (≈) | The city it made |
|---|---|---|---|---|---|
| walking | always | 4 to 5 km/h | ≈ 2.5 km | ≈ 20 km² | the walking city: mixed uses, the rich at the centre, the poor at the edges; most cities until 1850 were within this |
| horse omnibus | Paris 1828, London 1829 | ≈ 8 km/h | ≈ 4 km | ≈ 50 km² | the first middle-class commuting; fares too high for workers |
| horse tram on rails | New York 1832, widespread 1850s to 1880s | ≈ 10 km/h, twice the load per horse | ≈ 5 km | ≈ 80 km² | the streetcar suburb begins |
| steam railway and underground | London's Metropolitan Railway 1863 | ≈ 25 to 35 km/h | ≈ 12 to 15 km along lines | a star of corridors | railway suburbs; workmen's fares (from the 1860s in London) |
| electric tram | Richmond, Virginia, 1888 (Sprague) | ≈ 15 to 20 km/h | ≈ 8 to 10 km | ≈ 250 km² | the streetcar suburb (Sam Bass Warner on Boston); land developers built lines to sell lots |
| electric metro | London 1890 (deep tube), Budapest 1896, Paris 1900, New York 1904 | ≈ 30 km/h with stops | ≈ 15 km | dense centres and linear suburbs | the office downtown fed by trains |
| car and expressway | from the 1920s in the US, 1950s to 1970s elsewhere | ≈ 30 to 60 km/h | ≈ 20 to 30 km | ≈ 1,500 to 3,000 km² | dispersed suburbs, edge cities; the centre's share of jobs falls |
| commuter rail at scale | Tokyo, from the 1920s private railways | ≈ 40 to 60 km/h | ≈ 30 to 40 km | ≈ 3,000+ km², dense | the rail metropolis of 30+ million |

Each mode needed the one before (the omnibus needed paved streets; the tram needed rails in the street and a franchise; electric
traction needed generating stations; the metro needed tunnelling, electricity and ventilation; the car needed paved roads, fuel
distribution and traffic rules) and each set new land values: land near stations rose, and developers and railway companies
captured that rise (Tokyo's private railways built the department stores at their terminals and the suburbs at the end of the
lines).

---

## 5. Urban infrastructure as layered networks

Every layer of infrastructure is a public good or a club good (02zzi §1), usually a threshold investment, and most were first
built privately and then taken over or regulated by the city once their external effects (fire, disease, monopoly pricing) became
plain. Each depends on the layers beneath.

### 5.1 The layers

| Layer | What it gives | What it needs first | First at scale | Who provided it |
|---|---|---|---|---|
| **0. site** | defence, drinking water, access to water transport, a fertile hinterland | nothing | always | nature and choice |
| **1. streets, walls, gates, a market place** | movement, safety, a place where offers meet; tolls at the gates | a site; labour; an authority | Uruk; every walled town | the ruler or commune |
| **2. bulk supply routes** | food and fuel from far | a port, river or canal; ships and boats; storage | Rome, Chang'an and Kaifeng, Baghdad | the state; merchants |
| **3. storage** | buffers against pulses and shortfalls | buildings; an institution to own and guard them | Rome's *horrea*; Chinese ever-normal granaries; Chicago's elevators | the state; merchants |
| **4. water supply** | drinking, washing, fire fighting, industry | a source; gradient or pumps; pipes; an authority to stop theft and fund repair | Rome; London's New River (1613); steam pumping (18th c.); constant supply (19th c.) | the state; then private companies; then municipal |
| **5. drainage and sewers** | removal of excreta, rainwater, wash water | water supply (water-carried sewage needs water); a public authority and a tax; outfalls or treatment | Rome's Cloaca Maxima; Bazalgette's London (1858-75); Paris (Belgrand, 1850s to 70s) | municipal |
| **6. fuel and gas networks** | heat, light | bulk fuel supply (layer 2); pipes in streets (layer 1) | London gas lighting (1812); coal by rail | private companies, then municipal |
| **7. mechanised transport within the city** | a bigger city within the travel time budget | paved streets (1); franchises; later electricity (8) | omnibus 1820s; horse tram; underground 1863; electric tram 1888 | private, franchised, later municipal |
| **8. electricity** | power, light, lifts, electric traction | fuel or water power (2); generating stations; street conduits (1) | Edison's Pearl Street, New York, 1882 | private, then regulated or municipal |
| **9. height: lifts and steel frames** | density without spreading | electricity (8) or hydraulic power; steel (an industrial supply chain); pumped water to upper floors (4); fire codes | Otis safety lift (1853); Chicago's steel frame (1885); New York's towers | private, under building codes |
| **10. communications** | coordination, offices, markets at a distance | streets and poles (1); electricity (8) | the post; the telegraph (1840s); the telephone (1876 on); fibre and mobile | private and state |
| **11. public health** | life expectancy above the countryside's | water (4), sewers (5), statistics, medicine | medical officers (1848); filtration and chlorination (1900s); vaccination | municipal and state |
| **12. cold chain and mass distribution** | perishables from anywhere | railways and ships (2); electricity (8) or ice | refrigerated rail (1870s to 80s); supermarkets | private |
| **13. metropolitan systems** | megacity density: metro, expressways, airports, container ports, waste treatment, grids, data | all of the above, plus planning and finance | 20th and 21st centuries | public, private and public-private |

### 5.2 How the layers depend on each other

```
                          megacity density (10 million and more)
                                     |
      +--------------+---------------+---------------+---------------+
      |              |               |               |               |
  metro and      sewage          electricity     cold chain      planning, finance
  commuter rail  treatment       grid            and container   and municipal
      |              |               |           port                  taxes
      |              |               |               |               |
  tunnelling,    intercepting    generating      rail, ships,    statistics,
  electric       sewers          stations        refrigeration   land registry,
  traction           |               |               |           bonds
      |          water-carried   fuel by rail        |
      |          waste           or pipeline         |
      |              |               |               |
      +------- piped water at pressure (pumps, reservoirs, mains) ---+
                     |
              a water source and a gradient or pumps
                     |
      streets, a public authority able to tax, and bulk supply by water
                     |
                   the site
```

Four dependencies stand out, each of which was a historical bottleneck:

1. **Roads before trams, trams before suburbs.** Paved streets carried omnibuses; rails in the street doubled what a horse could
   pull; electricity removed the horse; each step widened the city.
2. **Water before density, sewers after water.** A city cannot grow dense without water brought in (wells fail and are fouled),
   and water brought in creates the sewage problem that sewers solve. London's piped water and flush toilets of the 1840s, with no
   sewers, made the Thames a sewer and the source of cholera.
3. **Electricity before skyscrapers and the metro.** A tall building needs safe lifts (Otis), pumped water, artificial light and
   (later) ventilation; deep tube railways needed electric traction, since steam in tunnels was barely tolerable.
4. **Sanitation and public health before megacities.** Until about 1900 cities killed their people faster than they bred; megacity
   populations became possible when water treatment, sewers and later medicine made the city healthier than the countryside.
   Where infrastructure has not kept pace (informal settlements in many 21st-century megacities), density brings back the old
   diseases.

---

## 6. Dependency trees, from market town to megacity

Each tree reads downwards: the thing at the top exists only if everything below it holds. Leaves are the land and labour of the
organic economy (02zzi §1) or, after the industrial break, mineral energy.

### 6.1 Market town (≈ 2,000 to 10,000 people)

```
market town
├── a market place and a market day (a charter from a lord or king; tolls)
│   ├── peace on the roads (the lord's protection, the market's own court)
│   └── households in villages within a day's walk with a surplus to sell (≈ 10 to 15 km)
├── food from its own fields and the villages around (the von Thünen rings at small scale)
│   └── grain, beasts, gardens fed with the town's dung
├── crafts: smiths, tanners, weavers, bakers, brewers, carpenters
│   ├── raw materials from the hinterland (hides, wool, timber, iron by trade)
│   └── guilds or the town's own rules for entry and quality
├── water: wells, a stream or river
├── fuel: woods and coppice within a cart's reach
└── coin, weights and measures (a mint or a lord's standard)
```

### 6.2 Pre-industrial capital (≈ 100,000 to 1 million: Rome, Chang'an, Kaifeng, Edo)

```
capital city
├── a flow of taxes and rents from a large territory (the court and officials live here)
│   └── a state that can tax: records, officials, an army
├── bulk food by water
│   ├── a sea or a canal system (the Grand Canal, the Bian, the Mediterranean)
│   ├── ships, boats, crews, shipbuilders
│   ├── granaries and warehouses at the port and in the city
│   └── a provisioning institution (the annona, tax grain, the police of grain)
│       └── officials, contracts with shippers, a dole or price controls
├── water (aqueducts, canals, wells) ── an authority to build, guard and repair
├── fuel from managed forests or coalfields by water
├── building materials (brick, stone, lime, timber) ── kilns and their fuel
├── markets (supervised or open) and their officials
├── crafts and services for the court and the people
└── migrants to replace the dead (the urban graveyard)
```

### 6.3 Merchant city (≈ 50,000 to 200,000: Venice, Bruges, Amsterdam)

```
merchant city
├── a port and shipping (shipyards: the Arsenal; timber, hemp, pitch, sailcloth by trade)
├── trust among strangers
│   ├── a law merchant, courts, notaries
│   ├── banks and bank money (Venice's banks, the Wisselbank)
│   └── information: brokers, price currents, letters, the bourse
├── goods to carry: cloth, spices, grain, salt, wine
├── food imported by sea (a grain office for bad years)
└── a government of merchants (the Great Council, the burgomasters)
```

### 6.4 Industrial city (≈ 300,000 to 1 million: Manchester, 1850)

```
industrial city
├── factories (cotton mills)
│   ├── machines (spinning mules, power looms) ── machine makers ── iron and engineering
│   ├── steam engines ── coal by canal and rail ── coalfields
│   ├── raw cotton ── Liverpool port ── American plantations (enslaved labour) and later India, Egypt
│   └── wage labour ── migrants from the countryside and Ireland
├── merchants and the exchange (selling yarn and cloth to the world)
├── housing for workers ── speculative builders ── brick, timber, land
├── food from a national market by rail
├── water and sewers (lagging: cholera in 1832 and 1849)
└── banks and credit for working capital
```

### 6.5 Hub city (Chicago, 1890)

```
Chicago as hub
├── transport breaks: Lake Michigan ↔ the I&M canal ↔ railways (in all directions)
├── grain
│   ├── farms of the prairie (a hinterland of a million km²)
│   ├── steam elevators ── grading rules ── the Board of Trade ── futures
│   └── telegraph prices (so New York and Liverpool prices reach the prairie)
├── lumber ── northern pine forests ── rivers and lake schooners ── rail to the prairie
├── meat ── western cattle and hogs ── the Union Stock Yards ── packers ── refrigerator cars ── ice or refrigeration
├── banks, insurance, wholesale houses (Marshall Field, Sears' mail order)
└── a city built fast: balloon frames, then steel frames, water from the lake (the Chicago river reversed in 1900 to take sewage away from it)
```

### 6.6 Megacity and global city (10 to 40 million)

```
megacity / global city
├── metropolitan transport (metro, commuter rail, expressways, buses)
│   └── electricity, tunnelling, finance for capital works, land use planning
├── water from distant catchments, treated; sewers and treatment plants
├── energy grids ── national and global fuel and power markets
├── food by global cold chains ── ports, airports, distribution centres
├── housing at density ── steel, cement, lifts, building codes; or informal settlements when these fail
├── producer services (finance, law, accounting, consulting, media) ── global firms' networks (Sassen)
├── universities, hospitals, culture as export industries
├── telecoms and data
├── a city government able to tax, borrow, plan and police
└── migrants and natural increase ── public health
```

### 6.7 The transitions between them

| From → to | What had to come first | The threshold |
|---|---|---|
| village → market town | a surplus to sell, peace, a charter, coin | enough households in a day's walk to support specialists |
| market town → regional city | water transport or good roads; merchants; a court or bishop | a hinterland larger than a day's cart journey |
| regional city → capital or entrepôt | a state's taxes or a trade network's goods; bulk water transport; a provisioning institution | food from beyond any land hinterland |
| capital → industrial city | mineral energy, machines, wage labour, rail | the organic ceiling broken |
| industrial city → metropolis | water, sewers, mechanised transport, electricity | deaths fall below births; the travel time budget covers a wider area |
| metropolis → megacity / global city | metro and roads at scale, treatment, grids, global supply chains, producer services | infrastructure growth keeping up with migration |

---

## 7. What a simulator could take from this

Grouped by kind, each tied to the 02zzi and economy_web.md vocabulary, and named for what Cybertron 2 has (E), has proposed (P) or
would need (N) only where 02zzi already places it; the rest is offered as possibility, not as a gap list.

**The city as a supply problem.**
- **Per-head budgets as rules.** A town node with population that eats, drinks, burns and builds at per-head rates (the table in
  §1.1) gives the town needs that are not chosen by agents. The ratios matter more than the units: water ≫ fuel > food per head.
  This is 02zzi's "a town as a node that grows by drawing people and food from its region" (N), with its inputs named.
- **Transport cost by mode decides the hinterland.** If carriage by land, river and sea costs in roughly 30 : 5 : 1 proportions,
  von Thünen's rings and the advantage of river and coastal towns should emerge without being scripted. A simple check: does the
  land use around a town sort by distance?
- **Provisioning as an institution, not just a market.** Every large city's food came through an office (annona, tax grain, the
  police of grain, licensed markets, the bread assize). These are natural roles for agents (a grain officer, a market warden) with
  a rule-driven population below, and they make supply into politics: shortages raise prices, and prices raise riots.
- **Pulses and stores.** Harvests, sailing seasons, the Morvan's spring flood: city chains pulse, and storage (granaries,
  warehouses, elevators) is the capital that turns a pulse into a steady supply (economy_web.md's "pulse" shape).

**Chokepoints and shared works.**
- **Water, a bridge, a harbour mouth, a canal lock, a pit-head port.** Cities are made of chokepoints, and the history above is full
  of who controlled them (the Newcastle hostmen, the City's coal dues, Rome's grain fleet, Venice's galleys). Several interlocking
  chokepoints (CLAUDE.md's design rule) arise naturally: food by water, fuel by water, water by aqueduct, all through one port.
- **Infrastructure as club and public goods with thresholds.** Aqueducts, sewers, granaries, market halls and roads each pay only
  above a scale of use, need a tax or a fee, and create free-rider and theft problems (Frontinus's illegal taps). They are the
  urban counterpart of the mill and the weir.
- **Layer dependencies as a works tree.** §5's table is a ready-made dependency graph: piped water before dense housing, sewers
  after piped water (or disease), mechanised transport to extend the city, height only with lifts. A world could let density be
  capped by the layers present.

**Waste as a joint product.**
- Night soil and stable manure as goods with owners, contracts and prices, which close the loop to the first ring of farms (Edo's
  market); and the failure of that loop when a substitute fertiliser appears or the farms move too far (London's collapse into the
  Great Stink). Fouled water downstream is a cost one place imposes on another (economy_web.md's tan yards at town scale).

**People.**
- **The urban graveyard.** A city with more deaths than births needs a steady flow of migrants from its region; this alone makes
  town and country depend on each other and gives the region's villages a reason to send their young (service, apprenticeship).
  Sanitation is what turns the sink off.
- **People who are not agents** (02zzi §6): a town's thousands as households fed by rule, with agents as the heads of trades,
  officials, merchants, landlords. Aggregate supplies (the bakers as a supply of bread at a price) fit the bread assize directly.

**Why cities grow, as checks rather than inputs.**
- **Agglomeration and scaling as things to measure, not to impose.** If interaction is cheaper in dense places, do larger towns
  in a run show more methods learned, more agreements, more trades per head (super-linear) and less road per head (sub-linear)?
  Bettencourt's exponents give a reference to compare against, read against a null arm (CLAUDE.md).
- **New work by combination (Jacobs).** If methods can arise from combining methods known in the same place, diverse towns should
  out-invent one-trade towns; import replacement (a town learning to make what it bought) is a measurable event.
- **Hubs as equilibria.** Bruges, Antwerp, Amsterdam, St Louis and Chicago show that a hub's advantage can move when a channel
  silts, a route opens or a rival offers better terms. A world with two candidate market towns could test whether trade tips to one.

**Institutions the city demands.**
- Markets with officials, weights and measures, and visible prices (02zzi §6's "prices that travel": Amsterdam's printed price
  currents and Chicago's telegraph prices are the historical form); guilds as club goods with exclusion; grading as the step that
  turns goods into commodities and receipts into money (Chicago's 1856 grades); banks and bank money as trust goods; police,
  inspectors and courts as enforcement that needs people (L-106).
- **Supervised and open markets as two settings.** Tang Chang'an and Song Kaifeng are the same size of city run two ways; the
  switch from one to the other is a natural experiment for a world.

**What a world at city scale would hold that a village does not.**
- Ports, warehouses, granaries, conduits, sewers and markets as buildings with owners and fees; housing as a stock with rents and
  crowding; water as a flow with a quality; fuel as an imported good with a monopoly at the source; transport within the town with
  a time budget; a demographic sink; and offices (grain, market, water, health) that agents can hold.

---

## Sources

Figures above are cited to these. Where a figure came through a secondary summary in this session, the secondary page is listed
too, and the figure should be checked against the primary before it is relied on.

**Metabolism and urban systems**
- Wolman, A. (1965). "The Metabolism of Cities." *Scientific American* 213(3). Summary: [Metabolism of Cities library](https://library.metabolismofcities.org/items/3245); [archive visualisation](https://archive.metabolismofcities.org/datavisualizations/51-abel-wolman-039s-metabolism-of-cities).
- Kennedy, C. et al. (2015). "Energy and material flows of megacities." *PNAS* 112(19): 5985-5990. [ADS abstract](https://ui.adsabs.harvard.edu/abs/2015PNAS..112.5985K); [phys.org summary](https://phys.org/news/2015-04-megacity-energy-resource-largest-urban.html).
- Kim, E. and Barles, S. (2012). "The energy consumption of Paris and its supply areas from the eighteenth century to the present." *Regional Environmental Change*. [Springer](https://link.springer.com/article/10.1007/s10113-011-0275-0).
- UN DESA (2025). *World Urbanization Prospects 2025*. [Press release](https://www.un.org/sustainabledevelopment/blog/2025/11/press-release-wup2025/); [UN DESA feature](https://desapublications.un.org/un-desa-voice/feature/december-2025/latest-urbanization-data-reveal-worlds-most-populous-cities).

**Food and transport costs**
- von Thünen, J. H. (1826). *Der isolierte Staat*.
- Duncan-Jones, R. (1982). *The Economy of the Roman Empire*, pp. 367-8; Scheidel, W. (2013), "Explaining the maritime freight charges in Diocletian's Prices Edict." [PDF](https://www.ancientportsantiques.com/wp-content/uploads/Documents/ETUDESarchivees/MedNavigationRoutes/ORBISprices-Scheidel2013.pdf).
- Rome's grain supply estimates (Rickman, Erdkamp, Mattingly and Aldrete, Josephus): [Cura Annonae summary](https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Cura_Annonae); [core.ac.uk paper](https://core.ac.uk/download/217234998.pdf).
- Monte Testaccio: [summary](https://wikipedia.com/wiki/Monte_Testaccio).
- Campbell, B., Galloway, J., Keene, D., Murphy, M. (1993). *A Medieval Capital and its Grain Supply*. [IHR project page](https://archives.history.ac.uk/ihrcms/cmh/projects/research/feeding-the-city.html).
- Wrigley, E. A. (1967). "A simple model of London's importance in changing English society and economy 1650-1750." *Past and Present* 37: 44-70. Secondary: [The Metropole](https://themetropole.blog/2020/05/11/).
- London populations: [Sorbonne 18th-century cities table](https://18thc-cities.sorbonne-universite.fr/-Demography-.html); [Encyclopedia.com](https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/london-growth); Finlay, R. and Shearer, B. (1986), in Beier and Finlay, *London 1500-1700*.
- Smithfield: [The impact of quadrupeds in Hanoverian London (thesis)](https://etheses.whiterose.ac.uk/19495/1/The%20impact%20of%20quadrupeds%20in%20Hanoverian%20London.pdf); [British History Online, the Metropolitan Meat-Market](https://www.british-history.ac.uk/node/37793).
- Kaplan, S. L. (1984). *Provisioning Paris*; (1996). *The Bakers of Paris and the Bread Question*. [Cambridge review](https://cambridge.org/core/journals/journal-of-economic-history/article/abs/provisioning-paris-merchants-and-millers-in-the-grain-and-flour-trade-during-the-eighteenth-century-by-steven-laurence-kaplan-ithaca-ny-cornell-university-press-1984-pp-666-3995/9CF5A5F38163D61E7ECD35E29E4E1E5C).

**Water**
- Frontinus, *De aquaeductu*; Herschel's commentary: [Thayer, TAPA](https://penelope.uchicago.edu/Thayer/E/Journals/TAPA/33/Water_Supply*.html); [quinaria](https://penelope.uchicago.edu/~grout/encyclopaedia_romana/romanurbs/quinaria.html); [Live Science on Keenan-Jones et al. 2015](https://www.livescience.com/51167-water-carried-roman-aqueduct.html).
- Hardy, A. (1991). "Parish pump to private pipes: London's water supply in the nineteenth century." *Medical History*. [PDF](https://cambridge.org/core/services/aop-cambridge-core/content/view/DD62A3ECE0531CCBA6CE355F256E37C6/S002572730007112Xa.pdf/parish-pump-to-private-pipes-londons-water-supply-in-the-nineteenth-century.pdf).
- New River: [New River Company](https://en.wikipedia.org/wiki/New_River_Company). Croton: [Baruch NYC data](https://www.baruch.cuny.edu/nycdata/infrastructure/croton_aqueduct.html); [Linda Hall Library](https://www.lindahall.org/experience/digital-exhibitions/centuries-of-civil-engineering/06-viaducts-aqueducts/b-the-croton-aqueduct/).
- Edo: [Tokyo Waterworks / IHCSA on the Tamagawa Josui](https://ihcsacafe-en.ihcsa.or.jp/news/josui/); [Tamagawa Aqueduct](https://en.wikipedia.org/wiki/Tamagawa_Aqueduct); [Tokyo Metropolitan Government history](https://www.metro.tokyo.lg.jp/english/about/history/history01.html).

**Fuel**
- Cavert, W. (2016). *The Smoke of London*. [Review](https://reviews.history.ac.uk/review/2186/print/).
- Clay, K. and Troesken, W., "Did Frederick Brodie discover the world's first environmental Kuznets curve? Coal smoke and the rise and fall of the London fog," NBER. [PDF](https://www.nber.org/chapters/c11990.pdf).
- Clark, G. and Jacks, D. (2007). "Coal and the Industrial Revolution, 1700-1869." *European Review of Economic History*.
- Paris wood: [Connexion France on the Morvan rafts](https://www.connexionfrance.com/news/wooden-raft-reaches-paris/480270); Jandot, O. (2016), as summarised in [r/AskHistorians](https://redlib.nohost.network/r/AskHistorians/comments/1cleoh8/why_was_firewood_so_expensive/l3imdx2/?context=3) (secondary; check); [OpenEdition on flottage](https://books.openedition.org/momeditions/9812).
- Hartwell, R. (1962). "A revolution in the Chinese iron and coal industries during the Northern Sung." *Journal of Asian Studies*. [Cambridge](https://www.cambridge.org/core/journals/journal-of-asian-studies/article/revolution-in-the-chinese-iron-and-coal-industries-during-the-northern-sung-9601126-ad/C4ED428E19B0A04C7225BB57822C89DF).

**Waste**
- Bazalgette's sewers: [London Museum](https://londonmuseum.org.uk/collections/london-stories/how-bazalgette-built-londons-first-super-sewer/); [ICE](https://www.ice.org.uk/what-is-civil-engineering/meet-the-engineers/sir-joseph-bazalgette).
- Edo night soil: [Guernica, "Raising a stink"](https://www.guernicamag.com/raising-a-stink/); Kumazawa (1985), [Shigaku abstract](https://www.jstage.jst.go.jp/article/shigaku/94/4/94_KJ00003673629/_article/-char/en); [Nichibun paper](https://nichibun.repo.nii.ac.jp/record/229/files/JN2006.pdf).
- Tarr, J. (1971). "Urban pollution: many long years ago." *American Heritage*. [Link](https://www.americanheritage.com/urban-pollution-many-long-years-ago?page=2); [Access magazine, "Horse Power"](https://www.accessmagazine.org/wp-content/uploads/sites/7/2016/07/Access-30-02-Horse-Power.pdf).

**Cities**
- Uruk: Algaze, G. (1993, 2008). *The Uruk World System*; *Ancient Mesopotamia at the Dawn of Civilization*. [Bevelled rim bowl](https://en.wikipedia.org/wiki/Beveled_rim_bowl); [World History Encyclopedia](https://www.worldhistory.org/uruk).
- Chang'an: [Chang'an](https://en.wikipedia.org/wiki/Chang%27an); [Lin 2015, "From closed capital to open metropolis"](https://urbanauapp.org/wp-content/uploads/Lin_2015.pdf); [Silk Road Seattle](https://depts.washington.edu/silkroad/exhibit/tang/essay2.html).
- Kaifeng and the Song: [Seshat](https://seshat-db.com/core/polity/425); [LSE working paper](https://www.lse.ac.uk/asset-library/information/wp178.pdf); Elvin, M. (1973), *The Pattern of the Chinese Past*; Shiba, Y. (1970), *Commerce and Society in Sung China*.
- Baghdad: [History of Baghdad](https://EN.wikipedia.com/wiki/History_of_Baghdad); [Cambridge book part](https://www.cambridge.org/core/product/identifier/9781009444958%23CN-BP-8/type/BOOK_PART).
- Venice: Lane, F. C. (1973), *Venice: A Maritime Republic*; [World History Encyclopedia on the Arsenale](https://www.worldhistory.org/article/2776/arsenale/).
- Florence: Villani, *Nuova Cronica* XI.94 (XII.94 in some editions); [Villani's Chronicle, Gutenberg](https://www.gutenberg.org/ebooks/33022); [Harsch 2019 on wage labour in the Arte della Lana](https://air.uniud.it/retrieve/77c353a6-51d6-46ed-b94e-d3effd304776/Harsch%2c%20Le%20travail%20salari%c3%a9%20dans%20l_Art%20de%20la%20Laine%20florentin%20avant%20la%20Peste%20noire%2c%202019.pdf).
- Amsterdam: de Vries, J. and van der Woude, A. (1997). *The First Modern Economy*; [Carleton on the Wisselbank](https://earlymoderneurope.hist.sites.carleton.edu/items/show/213); [Chicago Fed, "How Amsterdam got fiat money"](https://www.chicagofed.org/-/media/others/events/2010/money-banking-payments-finance/paper-how-amsterdam-got-fiat-money-pdf.pdf).
- Manchester: [Cottonopolis](https://en.wikipedia.org/wiki/Cottonopolis); Engels, F. (1845), *The Condition of the Working Class in England*.
- Chicago: Cronon, W. (1991). *Nature's Metropolis*. [Cameron Blevins notes](https://www.cameronblevins.org/quals/Cronon_NaturesMetropolis.html); ["Train whistles and futures" (quotes Cronon)](https://thegamming.org/2014/12/14/train-whistles-and-futures/); [Cronon lecture on logging](https://williamcronon.net/courses/469/handouts/469-westward-march-of-logging.html); [Encyclopedia of Chicago, Union Stock Yards](https://encyclopedia.chicagohistory.org/pages/30.html); [Encyclopedia of Chicago, lumber](https://encyclopedia.chicagohistory.org/pages/767.html); [Union Stock Yards](https://en.wikipedia.org/wiki/Union_Stock_Yards); [Census history](https://www.census.gov/about/history/stories/monthly/2021/october-2021.html).
- Tokyo: [Shinjuku passenger tally, nippon.com](https://www.nippon.com/en/features/h00273/); UN DESA 2025 above.
- Sassen, S. (1991; 2nd ed. 2001). *The Global City: New York, London, Tokyo*. [Princeton University Press](https://press.princeton.edu/books/paperback/9780691070636/the-global-city).

**Why cities grow**
- Bettencourt, L., Lobo, J., Helbing, D., Kühnert, C., West, G. (2007). "Growth, innovation, scaling, and the pace of life in cities." *PNAS* 104(17): 7301-7306. [PubMed](https://pubmed.ncbi.nlm.nih.gov/17438298/); [ScienceDaily](https://sciencedaily.com/releases/2007/04/070416193304.htm). Bettencourt, L. (2013). "The origins of scaling in cities." *Science* 340. West, G. (2017). *Scale*.
- Ortman, S. et al. (2014). "The pre-history of urban scaling." *PLOS ONE*; (2015) "Settlement scaling and increasing returns in an ancient society." *Science Advances*. [RePEc](https://econpapers.repec.org/RePEc:plo:pone00:0087902); [SFI working paper](https://santafe.edu/research/results/working-papers/urban-scaling-in-prehispanic-central-mexico).
- Arcaute, E. et al. (2015). "Constructing cities, deconstructing scaling laws." *Journal of the Royal Society Interface*.
- Marshall, A. (1890). *Principles of Economics*, IV.x. Duranton, G. and Puga, D. (2004). "Micro-foundations of urban agglomeration economies." *Handbook of Regional and Urban Economics* 4.
- Rosenthal, S. and Strange, W. (2004), *Handbook* 4; Combes, P.-P. et al. (2008, 2012); Ciccone, A. and Hall, R. (1996), *AER*. Summaries: [IZA DP 6502](https://docs.iza.org/dp6502.pdf); [New York Fed SR 440](https://resources.newyorkfed.org/medialibrary/media/research/staff_reports/sr440.pdf).
- Jacobs, J. (1969). *The Economy of Cities*; (1984). *Cities and the Wealth of Nations*.
- Christaller, W. (1933). *Die zentralen Orte in Süddeutschland*. Bairoch, P. (1988). *Cities and Economic Development*. Alonso, W. (1964). *Location and Land Use*.
- Travel time budget: [Marchetti's constant](https://en.wikipedia.org/wiki/Marchetti%27s_constant); Marchetti, C. (1994), "Anthropological invariants in travel behavior," *Technological Forecasting and Social Change* 47; Schafer, A. and Victor, D. (2000).
- Guilds: Ogilvie, S. (2019). *The European Guilds*; Epstein, S. R. (1998), "Craft guilds, apprenticeship and technological change," *Journal of Economic History*.
- Warner, S. B. (1962). *Streetcar Suburbs*.
