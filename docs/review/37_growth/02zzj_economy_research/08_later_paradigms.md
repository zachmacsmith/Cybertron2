# 08: the technology paradigms after the first industrial revolution, and how each builds on the layers below

Part of the 02zzj economy research folder (15 Nov 2026); research to think with, not a plan. It starts where the industrial
revolution file leaves off (coal, steam, iron and steel, textiles, railways, the factory) and follows seven later paradigms
(electricity; oil and the engine; chemistry and farming; water and sanitation; telecommunications; flight; computing) through the
industries and supply chains each grew, how those industries merged and split, what each needed from the layers below, and what
each did to society. It uses the chain shapes of economy_web.md §1 (shallow, accretive, paradigm switch, substitutes, joint
products, assembly, chokepoint, long skill, time capital, pulse, commons, increasing returns) and adds one the later paradigms
make unavoidable: the **network**, a chain whose value lies in a built web of lines, pipes or routes that many users share.

Three findings run through all seven. **First, each paradigm is an assembly of the layers beneath it, and it arrives late:** the
electric grid needed coal, steam engines, copper mining and the iron foundry; the car needed steel sheet, machine tools, rubber,
oil refining and roads; the chip needs electricity at scale, ultra-pure chemistry, optics and a century of physics. Each took
thirty to fifty years from first working version to changing how most people lived, because the payoff waited on complements
(wiring, roads, software, new factory layouts) and on people learning to reorganise around it (Paul David's dynamo and computer).
**Second, the decisive industries were often joint products and chokepoints rather than inventions:** gasoline was a waste
by-product of kerosene before the car; coal tar from gas works became the dye, drug and plastics industry; asphalt is a refinery
residue; the vacuum tube came out of the light-bulb industry, and the transistor out of the telephone monopoly's laboratory.
Control of a narrow step (Standard Oil's refineries, Chile's nitrate, Bell's network, ASML's lithography today) shaped each
industry more than control of its raw material. **Third, each new network rode on the rights of way, capital and institutions of
the one before:** the telegraph ran beside the railway, roads took the refineries' asphalt, fibre runs beside rail lines and
pipelines. For a simulator, none of these can be added as a machine; at most some can be aggregate capabilities that a world earns
once it holds the layers they stand on (§11).

## 0. The layer beneath, and how to read this file

The industrial revolution file covers the layer this one stands on. What later paradigms take from it, in one table:

| From the industrial layer | What later paradigms used it for |
|---|---|
| **coal** at scale | fuel for power stations, coke for steel, coal gas and coal tar for chemistry, the first source of hydrogen for ammonia |
| **the steam engine**, then the steam turbine | the first generators; pumps for water mains and mines; the model for the internal combustion engine's cycle |
| **iron and cheap steel** (Bessemer 1856, open hearth) | pipes, rails, pylons, ships, car bodies, boilers, reinforced concrete |
| **machine tools and interchangeable parts** | the precision every later engine, motor and gauge needed; the basis of mass production |
| **railways** | rights of way and a market for the telegraph; heavy freight for coal and ore; the first large managed firms |
| **the factory and wage labour** | a workforce that could be moved to the next machine; the model of a plant |
| **joint-stock companies, banks, stock exchanges** | the capital for grids, refineries and networks, which were too large for partnerships |
| **patents, contracts, courts, literacy, technical schools** | the knowledge institutions that the science-based industries (chemistry, electricity) needed |

Numbers cite the Sources section by bracketed keys such as [David 1990]; those marked *(rough)* are orders of magnitude or vary
between sources.

## 1. Electricity

### 1.1 What it is
A way of converting energy from one form (coal heat, falling water, later oil, gas, uranium, sun and wind) into a form that can be
sent along a wire and turned back into motion, light, heat or chemistry at the far end. Its economic novelty is that it
**separates where energy is made from where it is used**, and divides it into any quantity. A steam engine had to sit in the
factory and drive everything from one shaft; a power station could sit by the coal pit or the waterfall and feed a thousand
motors, lamps and furnaces miles away.

### 1.2 What it required (←)
| Layer | What it supplied |
|---|---|
| **energy** | coal and steam engines (the first stations were reciprocating steam engines driving dynamos; Parsons' steam turbine, 1884, became the standard); water power, as hydro |
| **materials** | copper (wire, windings), iron (magnet cores, frames), glass (bulbs), insulation (gutta-percha, rubber, paper, later plastics), carbon then tungsten filaments |
| **knowledge** | Faraday's induction (1831), the dynamo (1860s to 1870s), Maxwell's theory; the first science-based industry beside chemistry |
| **skills** | machinists, instrument makers, a new trade of electricians and electrical engineers, trained in new technical schools |
| **capital** | central stations and networks far beyond one owner; banks such as J. P. Morgan's financed Edison's companies |
| **infrastructure** | city streets to bury cables in; rail to bring coal; later dams |
| **institutions** | municipal franchises to dig streets; patents; then regulation of utilities as natural monopolies |
| **demand** | light (gas lighting already showed people would pay for it), then trams, motors, electrochemistry |

### 1.3 The industries and the supply chain
Electricity grew as several industries that had to arrive together:

```
coal mine / river ──► power station (boilers, turbines, generators) ──► transmission (copper, steel towers,
                                                                         transformers, insulators)
                                                                              │
              copper mine ──► smelter ──► electrolytic refinery ──► wire and cable mill
                                    (needs electricity itself)            │
                                                                              ▼
                                       distribution and meters ──► users: lamps, motors, trams,
                                                                    furnaces and cells, appliances
```

- **Generation and equipment.** Edison's Pearl Street Station in lower Manhattan opened on 4 September 1882 with six "Jumbo"
  dynamos able to light about 7,200 lamps, though it began with only about 400 lamps for between 59 and 85 customers in a district
  of a quarter to a square mile [Census 2026; IEEE Milestone] *(sources differ)*. Edison's real invention was **the system**: the
  station, the dynamo, the cables, the fuse, the meter and the lamp, each made by a separate Edison company because no one else
  made them. Those companies merged into Edison General Electric, which merged with Thomson-Houston to form General Electric in
  1892; Westinghouse built the rival alternating-current system (Tesla's motor patents, transformers that let current travel far
  at high voltage). Alternating current won after the Niagara Falls plant, with Westinghouse generators, sent power to Buffalo in
  1896. Two equipment firms dominated the United States for most of a century, as Siemens and AEG did Germany: **equipment making
  as an oligopoly from the start**.
- **Copper.** Electrification made copper strategic. Wire-grade copper is refined electrolytically, so the metal came to depend on
  the power it carried (a loop); open-pit mines (Bingham Canyon, 1906) and the copper belts of Chile and Central Africa followed
  demand.
- **Lamps.** Carbon filaments gave way to GE's ductile tungsten (Coolidge, 1910); the lamp makers, who knew how to pump glass
  empty, also made the first vacuum tubes (§5).
- **Utilities.** Samuel Insull in Chicago (Commonwealth Edison) worked out the economics that made electricity cheap: large
  stations, many kinds of customers whose peaks fall at different hours (the **load factor**), low prices to win more load, and a
  monopoly franchise in return for state regulation of rates (state commissions from 1907). This is **increasing returns** in a
  pure form: the cost of a unit falls as more is sold, so one supplier per area wins. Insull's pyramid of holding companies
  collapsed in 1932, and the Public Utility Holding Company Act (1935) broke such pyramids up: the institutions came after the
  failure.
- **Appliances** (irons, washing machines, refrigerators, radios) came decades after light: they needed wired houses and consumer
  credit (1920s instalment plans).

### 1.4 How it spread
Household electrification in the United States went from about 35% in 1920 to nearly 68% by 1929 [Richmond Fed 2020]. In 1930
nearly nine in ten urban and non-farm rural homes had access but only about one farm in ten did; by 1935 the farm figure was about
11% [Richmond Fed 2020; REA histories]. Private utilities would not build lines to scattered farms because the load did not pay
for the wire. The federal Rural Electrification Administration (May 1935) lent to farmers' cooperatives to build their own lines,
and farm electrification passed nine in ten by the mid-1950s *(rough)*. A network with increasing returns leaves out its thin
edges unless an institution (a cooperative, a state) pays for them.

### 1.5 The slow factory: Paul David's dynamo
Motors were available to factories from the 1880s, yet American manufacturing productivity barely moved for decades. Paul David
[David 1990], drawing on Warren Devine [Devine 1983], explained why. A steam factory was built around one engine turning **line
shafts** and belts on every floor, tall and narrow to keep shafts short. The first motors simply replaced the engine at the head
of the same shafts (**group drive**), and little was gained. The gains came with **unit drive**, a motor in each machine, which
let the factory be rebuilt as a single-storey plant laid out by the flow of work, with better light, overhead cranes and machines
placed where the process needed them. That needed new buildings, built only as old ones wore out, and managers who knew how to lay
out flow. Steam supplied about 80% of mechanical drive around 1900; electric motors overtook it by about 1920 and supplied most of
it by 1929 *(rough; Devine's table)*. Output per man-hour in American manufacturing rose about 1.3% a year before 1919 and about
3.1% a year after [Devine 1983]. David set these forty years beside Robert Solow's 1987 remark that "you can see the computer age
everywhere but in the productivity statistics" (§7).

**The lesson in chain-shape terms:** a general purpose technology is not a better tool dropped into an old process. It is a
**paradigm switch that waits on time capital** (buildings replaced at the end of their lives) and on **long skill** (managers and
engineers who know the new layout).

### 1.6 Electrochemistry: aluminium and its kin
Cheap power made a family of industries that are electricity turned into matter:
- **Aluminium.** Charles Hall in the United States and Paul Héroult in France found in 1886 that alumina dissolved in molten
  cryolite could be split by current. Aluminium fell from about $4.86 a pound in 1888 to about $0.78 in 1893 [Encyclopedia.com,
  Hall] as Hall's Pittsburgh Reduction Company (later Alcoa) scaled up and moved to Niagara Falls in 1895 for hydro power. Modern
  smelting uses roughly 13 to 15 kWh of electricity per kilogram *(rough)*, so smelters go where power is cheapest: Norway,
  Quebec, Iceland, the Pacific Northwest, later the Gulf and China's coal provinces. The chain is **bauxite (a place-bound ore,
  tropical) → Bayer process (alumina, 1888) → smelter (by the power) → rolling mill → users (aircraft, wire, cans)**. Its location
  is set not by its ore but by its **energy**.
- **Others:** chlor-alkali (chlorine and caustic soda from brine, which water treatment and plastics later needed, §3 and §4); the
  electric arc furnace for steel (Héroult again, 1900) and later for silicon (§7); electrolytic copper; calcium carbide (and from
  it acetylene).

### 1.7 What it enabled and its social effects
Switches: gas to electric light, shafts to unit drive, horse to electric trams (the first suburbs), ice boxes to refrigerators.
New jobs: electricians, linemen, station operators, electrical engineers, appliance trades, meter readers. Social effects: the
working day freed from daylight; housework reshaped by appliances (with debate over how far this moved women into paid work); the
farm left behind and then pulled in by cooperatives and the state; monopoly and rates as public questions.

## 2. Oil and the internal combustion engine

### 2.1 What it is
A liquid fuel of very high energy per kilogram, easy to pump, store and carry, and an engine light enough to burn it inside a
moving vehicle. Together they moved power off the rail and the shaft into any vehicle that could carry a tank: cars, trucks,
tractors, ships, aircraft. Petroleum was also the feedstock that replaced coal for most of the chemical industry after 1950.

### 2.2 What it required (←)
| Layer | What it supplied |
|---|---|
| **energy and materials** | steel for drill pipe, tanks, pipelines, engines and car bodies; rubber for tyres and seals; glass |
| **knowledge** | distillation (from chemistry and the coal-oil industry of the 1850s); thermodynamics; the Otto four-stroke cycle (1876) and Diesel's compression engine (1893) |
| **skills** | well drillers (salt-well boring was the model), refinery chemists, machinists able to work to fine tolerances |
| **capital** | refineries and pipelines with large thresholds; later the car plants |
| **infrastructure** | railways (tank cars) before pipelines; roads paved for wheels; filling stations |
| **institutions** | mineral rights (in the US the landowner owned what lay beneath, which made a scramble; elsewhere the state did); concessions abroad; later traffic law, licences, road taxes |
| **demand** | lamp oil first: a mass market for light already existed (whale oil, coal oil) |

### 2.3 The industries and how they merged
**Extraction and refining.** Edwin Drake's well at Titusville, Pennsylvania (1859) began the industry. For forty years oil was a
**lighting** business (kerosene), and gasoline a dangerous waste, often dumped. Rockefeller's Standard Oil grew not by drilling
but by controlling **refining** and transport: buying out refiners, winning railway rebates, building pipelines. By about 1880 it
refined roughly 90% of American oil *(rough, widely cited)*, until the Supreme Court broke it into 34 companies in 1911. The
**chokepoint was the middle step**: anyone could drill; few could refine and ship at scale. Electric light then took kerosene's
market just as the car made one for gasoline, and the waste became the main product; thermal cracking (Burton, 1913) and catalytic
cracking (1930s) raised its share of each barrel. Spindletop (Texas, 1901) and the Middle East fields (Persia 1908, Saudi Arabia
1938) moved the centre of supply.

**The refinery's joint products.** A refinery splits one input into a family of outputs, and each found its own industry: gasoline
(cars), diesel (trucks, tractors, ships, locomotives), kerosene (lamps, then jet fuel, §6), fuel oil (ships, power stations),
lubricants (every machine), **asphalt** (the residue that paved the roads the cars needed), and **petrochemical feedstocks**
(ethylene, propylene, benzene) for plastics, fibres and rubber. This is economy_web's **joint products** shape at industrial
scale: each product's demand subsidises the others, and a refinery is tuned by which one pays most.

**Cars: from the workshop to the integrated plant.** The car began as a craft product assembled by small firms (often bicycle and
carriage makers) from bought parts. Henry Ford's Model T (1908) and the moving assembly line at Highland Park (1913) cut the time
to build a chassis from about 12.5 hours to about 93 minutes, and the price of a Model T fell from $850 to $260 by 1925
[Britannica; The Henry Ford] *(dates and figures vary slightly by source)*; about 15 million were built by 1927. Ford then pushed
**vertical integration** further than any firm before: the River Rouge complex (land bought 1915; final assembly moved there 1927)
had its own docks, ore freighters, railway, blast furnaces, steel mill, glass plant, power station, tyre plant and foundries; it
employed more than 100,000 people at its peak, and Ford claimed a car could be built from raw ore in 28 hours (a promotional best
case) [The Henry Ford, Rouge history]. Ford also owned iron and coal mines and timberland, and in 1928 founded Fordlandia, an
Amazon rubber plantation that failed. Integration answered unreliable suppliers and the scale of a single model; it became a
burden when buyers wanted variety.

**General Motors' answer.** Alfred Sloan's GM offered "a car for every purse and purpose": divisions, annual models and consumer
credit (GMAC, 1919). It overtook Ford in the late 1920s, and its multidivisional form became the model of the large corporation
(Chandler).

**Toyota's supplier networks.** Postwar Toyota, short of capital and space, built the opposite: a core plant drawing parts **just
in time** from a pyramid of affiliated suppliers (first-tier system makers, then second and third tiers), tied by long
relationships, shared engineering and cross-shareholding (keiretsu). Toyota and other Japanese makers bought around 80% of their
parts from affiliated firms, while GM made more than half its parts in house [Japan economy text, via Asanuma and Cusumano]
*(rough; measures vary)*. The MIT study of world car plants found the lean plant built a car in about 16 hours with 45 defects per
100 cars, against about 31 hours and 130 defects for the mass-production plant [Womack, Jones and Roos 1990]. From the craft shop
to Ford's integration to Toyota's networks, **the boundary of the firm moves** as trust, information and transport costs change
(global supplier networks are the supply chains file's).

**Rubber.** Vulcanisation (Charles Goodyear, 1839) made rubber durable; Dunlop's pneumatic tyre (1888) made it a vehicle material.
Wild Amazon rubber gave way to plantations in Malaya and the Netherlands Indies, grown from seeds taken from Brazil in 1876. When
Japan took those plantations in 1942, the United States built a synthetic rubber industry from petroleum and alcohol feedstocks in
about three years *(rough)*. Rubber is a **chokepoint by climate**; its substitute needed the whole petrochemical layer.

**Steel for cars.** Demand for thin, uniform sheet led to the continuous wide-strip mill (Armco, 1920s) and pressed-steel bodies
in place of wood.

**Roads.** Cars needed roads, and roads needed public money. In the United States the Federal Aid Road Act (1916), petrol taxes
earmarked for roads (Oregon first, 1919), and the Interstate Highway Act (1956) paid for them. Asphalt from refineries and
Portland cement made the surfaces. Roads brought filling stations, motels, suburbs and trucking, and the decline of the electric
interurban and much rail passenger traffic: a network displacing the one before.

### 2.4 Tractors: farm mechanisation
Farm tractors in the United States rose from about 240,000 in 1920 to about 920,000 in 1930 and almost 1.6 million in 1940, and to
roughly 4.7 million by the mid-1950s [USDA census tables] *(rough)*. Horses and mules on farms peaked at nearly 27 million during
the First World War. The quiet gain was land: feeding those animals took about 93 million acres of cropland at the 1915 peak,
roughly a quarter of all harvested cropland, plus about 80 million acres of pasture; by 1960 nearly all of it was freed for food,
dairy and beef [Olmstead and Rhode 2001]. The tractor replaced an **organic** energy source (beasts fed from the land, Wrigley's
organic economy, 02zzi §1) with a mineral one, lifting the land ceiling a second time after coal. It also emptied the countryside
(fewer, larger farms; labour to the cities; farm debt for machines), and it needed fuel delivered to every farm, repair skills in
every county, and credit.

### 2.5 Plastics and petrochemicals
Plastics began on the coal layer: celluloid (1860s, from cellulose), and Bakelite (Leo Baekeland, 1907) from phenol, a coal-tar
chemical (§3). Polyethylene (ICI, 1933), nylon (DuPont, 1935 to 1939), PVC and polystyrene followed. After the Second World War
the feedstock switched from coal to oil and gas because steam cracking of naphtha and ethane gave ethylene and propylene in bulk:
a **paradigm switch in the chemical industry's raw material**. Global plastics production rose from about 2 million tonnes in 1950
to about 380 million tonnes in 2015, an 8.4% compound annual rate, and about 79% of the waste ever made has gone to landfills or
the environment [Geyer, Jambeck and Law 2017]. Plastics became cheap only once refining made their inputs as by-products in bulk.

### 2.6 Social effects
Personal mobility and suburbs; the end of the horse economy (stables, farriers, the hay trade); trucks freeing factories from rail
sidings; oil as a strategic resource and, from the 1970s, its price shocks as a macroeconomic force.

## 3. Chemistry, agriculture and medicine

### 3.1 Dyes: where the science-based industry began
In 1856 William Perkin, trying to make quinine, made mauveine, the first synthetic dye, from aniline, a coal-tar chemical. Coal
tar was a waste of the gas works and coke ovens of the industrial layer: a **joint product** waiting for a use. German firms
(BASF, Bayer, Hoechst) built the industry, helped by research universities that trained chemists by the hundred and by patent law;
by the First World War they made the great majority of the world's dyes *(rough; commonly given as about 80 to 90%)*. Their
decisive invention was organisational: the **industrial research laboratory**, a paid team of scientists searching for new
products on purpose. General Electric (1900), DuPont (1903) and Bell (1925) copied it. From this point new industries depended on
**organised knowledge** as an input, the long skill of a whole profession rather than of a craftsman.

### 3.2 From dyes to drugs
The dye firms already knew how to make, test and purify organic molecules, so they moved into medicine:
- **Aspirin**, sold by Bayer from 1899.
- **Salvarsan** (1910), Paul Ehrlich's arsenic compound against syphilis, the first "magic bullet", from his work on dyes that
  stained some cells and not others; made by Hoechst.
- **Prontosil** (1935), the first sulfa drug, found by Gerhard Domagk at Bayer (then part of IG Farben), was itself a red dye.
- **Penicillin**: found by Fleming (1928), made into a drug by Florey and Chain (1940), and mass produced in the United States
  during the war by **deep-tank fermentation**, which borrowed from brewing and from Pfizer's citric-acid fermentation. Pfizer's
  Brooklyn plant, in a converted ice factory with fourteen 7,500-gallon tanks, opened in March 1944 and supplied most of the
  penicillin that went ashore on D-Day [ACS landmark]; American output rose from small amounts in 1943 to about a hundred billion
  units a month by mid-1944 *(rough; units and doses are counted differently)*.
- **Institutions:** the Elixir Sulfanilamide deaths (1937) led to the US Food, Drug and Cosmetic Act (1938, proof of safety),
  thalidomide to the 1962 rule of proof of efficacy: drugs became an industry gated by **testing and regulation**, with costly
  trials as its threshold.

### 3.3 Nitrogen: Haber–Bosch
**The need.** Plants need fixed nitrogen; farms got it from manure, legumes, guano and, from the mid-nineteenth century, Chilean
sodium nitrate, which also supplied explosives. William Crookes warned in 1898 that the world's wheat supply would hit a nitrogen
limit. Chile's nitrate was a **chokepoint by geology**, and in the First World War the British blockade cut Germany off from it.

**The process.** Fritz Haber showed in 1909 that nitrogen and hydrogen combine to ammonia at high pressure and temperature over a
catalyst; Carl Bosch at BASF made it industrial, at Oppau in 1913, which required steel vessels able to hold hydrogen at about 200
atmospheres (hydrogen embrittles ordinary steel, so Bosch invented a lined reactor) and a cheap hydrogen source (originally coal,
via water gas; today mainly natural gas, by steam reforming). The plant was turned to explosives within two years.

**The scale.** About 183 million tonnes of ammonia were made in 2020, around 70% for agriculture [industry summaries] *(rough)*;
the process uses roughly 1 to 2% of the world's energy and emits about 1.3% of its carbon dioxide *(rough)*. Erisman and
colleagues estimated that about 44% of the world's population in 2000 and about 48% in 2008 were fed by Haber–Bosch nitrogen
[Erisman et al. 2008]; Vaclav Smil reached similar figures.

**The chain:**
```
coal or natural gas ──► hydrogen (reforming, water gas)
air ──► nitrogen (air separation)
           └──► high-pressure synthesis (steel, catalysts, compressors, electricity) ──► ammonia
                    ├──► urea, ammonium nitrate ──► fertiliser plants ──► rail, ship, truck ──► farms
                    └──► nitric acid ──► explosives
```
Fertiliser is **mineral energy turned into food**: it breaks the organic economy's last ceiling, the land's own fertility, as coal
broke its fuel ceiling.

### 3.4 Pesticides and the Green Revolution
**Pesticides.** After arsenic compounds came DDT (Paul Müller, 1939), used against typhus and malaria in the war, then on crops;
Rachel Carson's *Silent Spring* (1962) made its harm a public question, and the United States banned most uses in 1972. A
**commons** shape: the gain private, the harm downstream and shared.

**The Green Revolution.** From the 1940s, Norman Borlaug's programme in Mexico bred short-stemmed wheat (using the Japanese
Norin-10 dwarfing gene) that could take heavy fertiliser without falling over; the International Rice Research Institute released
IR8 rice in 1966. Brought to India and Pakistan from the mid-1960s, the new wheats helped raise Indian wheat production from about
12 million tonnes in the mid-1960s to about 20 million tonnes by 1970 *(rough; sources differ by year)*. The point for this file
is that the new seed was useless alone: it was an **assembly** of seed, fertiliser (Haber–Bosch), irrigation (§4), pesticides,
credit, extension agents who taught farmers, and state price support. Where any input was missing (rain-fed land, poor credit) the
gains were small; where all were present (the irrigated Punjab) they were large, and came with falling water tables and widening
gaps between farmers.

### 3.5 What chemistry enabled
Fertiliser and therefore population; synthetic dyes, drugs, explosives, fibres, plastics, detergents; the research laboratory;
drug regulation. New jobs: industrial chemists, pharmacists, chemical plant operators, agronomists, extension officers.

## 4. Water and sanitation

### 4.1 What it is
Piped clean water into houses, sewers carrying waste away, filtration and chlorination killing what the water carries, and dams
storing water for cities and fields. Before it, cities were **population sinks**: their death rates exceeded rural ones, and they
grew only because migrants arrived (the "urban penalty").

### 4.2 What it required (←)
| Layer | What it supplied |
|---|---|
| **materials** | cast iron and later steel pipe; brick for sewers; Portland cement (1824) and concrete; sand for filters; chlorine (from the chlor-alkali industry, §1.6) |
| **energy** | steam pumps (the Cornish engine from mining) to lift water and sewage |
| **knowledge** | John Snow's mapping of the Broad Street cholera outbreak (1854); germ theory (Pasteur; Koch identified the cholera germ in 1883); bacteriological testing of water |
| **skills** | civil engineers, surveyors, sanitary inspectors, water chemists |
| **capital** | very large, long-lived works paid back over decades: **time capital** in its purest form |
| **institutions** | municipal government able to borrow (municipal bonds), boards of health, powers to dig under private land, public health acts (Britain 1848, 1875) |
| **demand** | crowded industrial cities with cholera and typhoid; the flush toilet, which needs piped water and a sewer to be worth having |

### 4.3 How it spread, and its effects
- **London.** In the hot summer of 1858 the smell of the Thames (the Great Stink) drove Parliament to fund Joseph Bazalgette's
  plan: about 82 miles of brick intercepting sewers and about 1,100 miles of street sewers carrying waste east of the city, opened
  in 1865 and finished around 1875 [London Museum]. It was justified by the wrong theory (bad air), and worked anyway.
- **Hamburg, 1892:** a cholera epidemic killed thousands in unfiltered Hamburg while neighbouring Altona, which filtered its water
  from the same river, was largely spared: a natural experiment that made filtration standard.
- **Chlorination:** first used continuously for a public supply in Jersey City in 1908, spreading across American cities within a
  decade.
- **The measured effect:** David Cutler and Grant Miller [Cutler and Miller 2005] found that filtration and chlorination explain
  nearly half of the fall in total mortality in major American cities between 1900 and 1936, about three-quarters of the fall in
  infant mortality and nearly two-thirds of the fall in child mortality, at a social return of more than 23 to 1.
- **Scale of cities:** clean water ended the urban penalty, so cities could grow from their own births to sizes (tens of millions)
  that would earlier have been death traps.

### 4.4 Dams and irrigation
Large dams combined water supply, flood control, irrigation and hydroelectric power: the Hoover Dam (1936), the Tennessee Valley
Authority (1933), the Aswan High Dam (1970), and many in India and China. The world's irrigated area rose from about 147 million
hectares in 1961 to about 343 million hectares in 2020 [USDA ERS 2024]; irrigated land is about a fifth to a quarter of cropland
but yields roughly 40% of the world's food *(rough)*. Dams brought **upstream against downstream** conflicts at the scale of
nations (the Nile, the Indus, the Colorado), the displacement of people from reservoirs, and in groundwater pumping (electric and
diesel pumps) the classic depleting **commons**.

### 4.5 What kind of good it is
A **public good** (disease is shared, so everyone gains from a neighbour's clean water) built as **time capital** on a **commons**
(rivers, aquifers). Its gain is mostly lives, not goods, and only public institutions able to tax and borrow have built it.

## 5. Telecommunications

### 5.1 What it is
Sending information faster than goods or people can travel. Each step (telegraph, telephone, radio, television, internet) lowered
the cost and delay of knowing something at a distance, and so changed what markets, firms and governments could do. Information is
an odd good (02zzi §1): costly to make, nearly free to copy, valuable mostly before others have it.

### 5.2 The telegraph
- **Required:** electricity from batteries (Volta, 1800), electromagnetism, copper and iron wire, glass or porcelain insulators,
  poles, and **rights of way**, which the railways supplied. The railways needed it too: from 1851 the Erie Railroad dispatched
  trains by telegraph, so one track could carry trains both ways safely. The two networks grew up together.
- **Spread:** Morse's line from Washington to Baltimore (1844); Western Union dominant in the United States by 1866; Reuters' news
  service from 1851; the first transatlantic cable (1858) failed within weeks, and a durable one was laid in 1866. Submarine
  cables needed **gutta-percha**, a latex from Malayan trees and for decades the only good insulator under sea water: a tropical
  chokepoint, as rubber was for tyres.
- **Effects on markets:** before the cable, news between New York and Liverpool travelled by steamship in about 7 to 15 days;
  after it, in about a day. Claudia Steinwender [Steinwender 2018] found that the average New York–Liverpool cotton price gap fell
  by more than a third (from 2.56 to 1.65 pence a pound), its variance by more than 90%, and exports rose; the welfare gain was
  about 8% of the value of cotton exports. Within countries, the telegraph and the stock ticker (1867) let commodity exchanges
  (the Chicago Board of Trade, 1848) trade grain by grade and by future delivery, and joined regional prices into one national
  market (William Cronon's *Nature's Metropolis*).
- **Effects on organisation:** Alfred Chandler [Chandler 1977] argued that railways and the telegraph made the large managed firm
  possible: head offices could coordinate plants and branches daily, so administration replaced the market for many decisions
  ("the visible hand"). States gained the same reach over provinces and colonies.

### 5.3 The telephone
Alexander Graham Bell's patent (1876) began the Bell system. Telephones needed **exchanges** (operators, then automatic switches
from the 1890s), a pair of copper wires to every subscriber, and power, so they built on the telegraph's poles and the electric
industry's generators. Its value rose with the number of subscribers (a **network effect**), which favoured one network: AT&T
settled with the government in 1913 (the Kingsbury Commitment), was regulated as a monopoly from 1934, and was broken up only in
1984. Bell Labs (1925) produced the transistor (1947), information theory (Shannon, 1948) and Unix: a regulated monopoly funding
basic research from secure rents. The telephone let firms split head office from plant and made the operator one of the largest
new women's occupations.

### 5.4 Radio and television
- **Radio** needed theory (Maxwell, Hertz), then Marconi's engineering (across the Atlantic, 1901), then the **vacuum tube** to
  amplify: Fleming's diode (1904) came from the Edison effect in light bulbs, de Forest's triode from 1906. The lamp industry thus
  became the electronics industry. RCA was formed in 1919 from GE's and others' radio patents. Broadcasting began in 1920 (KDKA,
  Pittsburgh); by 1930 about 40% of American households had a radio [Census 2023]. Its business model was new: free to the
  listener, paid for by **advertising**, which made national brands and national markets in attention.
- **Television** followed the same model: about 9% of American households in 1950, roughly 87% by 1960 *(rough; sources differ)*,
  one of the fastest adoptions of any household good. Radio also gave navigation, radar (§6) and military command.

### 5.5 The internet
The packet-switched ARPANET (1969) joined university computers on lines leased from the telephone network; TCP/IP (1983) let
separate networks interconnect; the World Wide Web (CERN, 1989 to 1991) gave it a public face; the American backbone was opened to
commerce in 1995. About 5.5 billion people, 68% of the world, were online in 2024 [ITU 2024]. Intercontinental traffic runs mostly
on undersea fibre cables, laid often along the same routes as the telegraph cables a century and a half earlier. The internet **is
computing (§7) running on the telephone network's layer**; it later inverted the relation, carrying voice as data.

### 5.6 Information as an economic good
Friedrich Hayek (1945) argued that prices carry dispersed knowledge no planner holds; George Stigler (1961) treated searching for
prices as costly; each telecom step lowered that cost. The pattern across all five:

| Step | Delay it cut | What it changed in markets | What it changed in organisation |
|---|---|---|---|
| telegraph | days or weeks to minutes, for short coded messages | regional and transatlantic prices converged; futures and grading | the large managed firm; news agencies |
| telephone | conversation at a distance | sales and ordering by phone; local services | head office apart from plant; the office as we know it |
| radio and TV | broadcast to everyone at once | national advertising and brands | mass politics and mass culture |
| internet | near-zero cost per message, to anyone | global price search; platforms; markets for small sellers | dispersed firms; work done anywhere |

## 6. Flight

### 6.1 What it is
Carrying people and high-value goods through the air, faster than any surface route and without needing a road or rail line
between two points: only an airport at each end and a controlled sky between.

### 6.2 What it required (←)
| Layer | What it supplied |
|---|---|
| **engines** | the light petrol engine from the car industry; later the jet engine, which needed new alloys |
| **materials** | spruce and fabric first; then **duralumin** (Alfred Wilm, 1906, an aluminium alloy that hardens with age), so aircraft depended on cheap electrolytic aluminium (§1.6); later nickel superalloys and titanium for jet turbines; composites |
| **fuel** | petrol, then kerosene for jets: refinery products (§2) |
| **knowledge** | aerodynamics (wind tunnels; the Wright brothers built their own), structural engineering, metallurgy, later radar and radio |
| **skills and capital** | bicycle makers and machinists first, then aeronautical engineers and pilots (long skills); governments as the main early buyer |
| **infrastructure** | airfields, then paved runways, terminals, radio beacons, radar, weather services |
| **institutions** | airmail contracts as subsidy; licensing of pilots and aircraft; international rights to fly over and land |
| **demand** | war first; mail; then business travel; then mass tourism |

### 6.3 How it grew, and its industries
- **1903 to 1918:** the Wrights' first flight (12 seconds, 120 feet) used a light engine built in their own shop; the First World
  War made aircraft a mass-produced weapon and built the first aircraft and engine industries.
- **Mail and subsidy:** the United States Post Office flew mail from 1918; the Kelly Act (1925) put airmail out to private
  carriers, and those contracts founded the major airlines. The Air Commerce Act (1926) licensed pilots and aircraft. The Douglas
  DC-3 (1936) was the first airliner that could pay its way on passengers alone.
- **The jet:** Frank Whittle (patent 1930) and Hans von Ohain (first flight, 1939) built the jet engine; it needed turbine blades
  that keep their strength red-hot, hence nickel superalloys and, much later, single-crystal blades. The Comet (1952), the first
  jet airliner, taught through fatal fatigue failures (1954) how pressurised hulls break; the Boeing 707 (1958) and 747 (1970)
  made jet travel cheap.
- **Rules and control:** the Chicago Convention (1944) created the International Civil Aviation Organization and the system of
  rights to fly over and land in other countries. After two airliners collided over the Grand Canyon in 1956, the United States
  created the Federal Aviation Agency (1958) to run one radar-based air traffic control system. American fares and routes were
  regulated until 1978.
- **Industrial structure:** large airframes came down to two makers (Boeing and Airbus) and large jet engines to three (General
  Electric, Rolls-Royce, Pratt & Whitney): very high fixed costs of design and certification, long learning curves, and a small
  number of buyers make an **oligopoly by increasing returns and long skill**.
- **Scale:** by the mid-2020s airlines carried on the order of four to five billion passenger trips a year *(rough)*. Air cargo
  carries less than 1% of world trade by weight but close to a third by value [IATA 2025]: fresh flowers, fish, drugs, chips,
  spare parts. Flight is what lets the chip industry (§7) run one supply chain across several continents.

### 6.4 Social effects
Tourism as a mass industry; global firms with managers who fly; diasporas that keep in touch; the end of the ocean liner; the
spread of disease at the speed of a flight.

## 7. Computing and information

### 7.1 What it is
Machines that store, process and transmit information by rule. Their economic role is to make calculation, record-keeping, control
and communication so cheap that they enter almost every other activity: a general purpose technology like electricity, and, like
it, slow to show in productivity.

### 7.2 The path
| Stage | Example | What it stood on |
|---|---|---|
| **mechanical calculation and punched cards** | Herman Hollerith's tabulators for the 1890 US census; his firm became part of IBM (named 1924); office machines (cash registers, adding machines) | machine tools; electricity for relays; the office and its clerks; bureaucracies with records to count |
| **electronic computing** | ENIAC (1945): about 18,000 vacuum tubes, about 150 kW of power, built for artillery tables *(rough)* | the vacuum tube (from the lamp and radio industries); wartime money |
| **the transistor** | Bell Labs, 1947 | the telephone monopoly's laboratory; quantum physics; germanium, then silicon |
| **the integrated circuit** | Kilby (Texas Instruments, 1958), Noyce (Fairchild, 1959, the planar process) | photolithography (from printing), diffusion furnaces, pure chemicals |
| **the microprocessor** | Intel 4004 (1971), about 2,300 transistors; in 2024 one GPU package held about 208 billion [Wikipedia, transistor count] | half a century of shrinking (Moore's law), paid for by each generation's sales |
| **software as an industry** | IBM's "unbundling" (1969), selling software apart from machines; the personal computer (IBM PC, 1981) and Microsoft | universities and training in programming; copyright for code |
| **networks** | ARPANET to the internet (§5.5) | the telephone network; packet switching |

Early demand came from the state: missiles (Minuteman) and the Apollo guidance computer bought most of the first integrated
circuits, carrying the industry down its learning curve until civil markets (calculators, then computers) took over *(rough)*.

### 7.3 The supply chain: from sand to chip
The chip is the deepest assembly any economy has built, and it uses every earlier layer in this file:

```
quartz ──► metallurgical silicon (electric arc furnace, ~98–99% pure; needs cheap power)
        ──► polysilicon (chlorination and deposition; "nine to eleven nines" pure)
        ──► single-crystal ingot (Czochralski puller) ──► sliced and polished wafers
                                                        │
  photomasks ─┐                                         ▼
  lithography ┼──► FAB: hundreds of steps of patterning, etching, deposition, doping, cleaning
  (ASML: optics from Zeiss, lasers from Trumpf, ~5,000 suppliers)  │  (ultra-pure water and gases,
  photoresists, ultra-pure gases (neon, fluorine), chemicals        │   steady electricity, clean rooms)
  etch and deposition tools (US and Japanese makers)               ▼
  design: EDA software, licensed architectures ──────────────► tested die ──► packaging and test
                                                                              ──► boards ──► devices
                                                                              ──► data centres, networks
```

- **Materials:** silicon is abundant but purity is not; the rare elements (gallium, germanium, hafnium, tantalum, cobalt, helium,
  the rare earths in magnets) are minor by weight and major by dependence. China produced about 98% of the world's gallium in 2023
  [Global Taiwan Institute 2023] *(may have changed)*.
- **Lithography:** extreme ultraviolet lithography machines are made by one firm, ASML (Netherlands), from about 100,000 parts and
  some 5,000 suppliers; the newest cost about €350 million each; their mirrors come from Zeiss and their drive lasers from Trumpf
  [ASML and trade press] *(rough)*. A **chokepoint of knowledge**, built over decades with no substitute.
- **Fabrication:** a leading-edge fab costs on the order of $20 billion or more *(rough)*; TSMC in Taiwan makes roughly 90% of the
  most advanced logic chips [Global Taiwan Institute 2023; trade estimates] *(rough)*. The industry split from firms that designed
  and made their own chips (Intel, IBM, Texas Instruments) into **fabless designers** (Nvidia, Apple, Qualcomm) and **foundries**
  (TSMC, from 1987): a vertical disintegration like Ford to Toyota, resting on standard design rules and a foundry that does not
  compete with its customers.
- **Energy:** data centres used about 415 TWh in 2024, around 1.5% of the world's electricity, projected to more than double by
  2030 [IEA 2025]. Computing has come round to depend on the first layer in this file.
- **Skills:** process engineers and chip designers, a long skill concentrated in a few places and hard to move.

### 7.4 The productivity paradox, again
Solow's 1987 remark (§1.5) described two decades of computers in offices with little measured gain. American productivity growth
then revived from about 1995 to 2004, concentrated in industries that made and heavily used computers, and studies of firms
(Brynjolfsson and Hitt) found the gains came where firms changed their organisation, training and processes around the machines,
the same lesson as unit drive. Robert Gordon [Gordon 2016] argues that the earlier great inventions (electricity, the engine,
chemistry, plumbing, telecoms) did more: American total factor productivity grew about 1.89% a year from 1920 to 1970, against
about 0.64% from 1970 to 2014 *(as reported in secondary sources; check against the book's tables)*.

### 7.5 Social effects
Clerical work automated and then much routine middle-skill work; new jobs in programming, systems and design; platforms with
network effects (search, social media, marketplaces); surveillance and new forms of control; geopolitical rivalry over chips.

## 8. General purpose technologies, paradigms and long waves

### 8.1 General purpose technologies
Timothy Bresnahan and Manuel Trajtenberg [Bresnahan and Trajtenberg 1995] defined a **general purpose technology** (GPT) by three
marks: it is **pervasive** (used in many sectors), it **keeps improving**, and it **spawns innovation** in the sectors that use it
(innovational complementarities). The steam engine, the electric motor and the semiconductor are their examples. Two consequences
follow. First, the GPT sector and its users depend on each other: better motors make it worth redesigning factories, and
redesigned factories create demand for better motors, so growth comes from the pair, and neither side alone captures the gain (a
coordination problem; the market will under-invest). Second, the payoff lags: users must invent the complements, so a GPT can
lower measured productivity before raising it (Helpman's edited volume, 1998). Richard Lipsey, Kenneth Carlaw and Clifford Bekar
[Lipsey et al. 2005] list about two dozen GPTs across history, from writing and the wheel to the internet, and stress that each
restructures the economy around it.

Here electricity, the engine and computing are GPTs in the strict sense; chemistry is a family of them; water and telecoms are
infrastructures with GPT-like effects; flight is narrower.

### 8.2 Techno-economic paradigms and long waves
Nikolai Kondratiev (1925) noticed waves of about fifty years in prices and output; Joseph Schumpeter (1939) tied them to clusters
of innovation. Christopher Freeman and Francisco Louçã [Freeman and Louçã 2001] and Carlota Perez [Perez 2002] reworked the idea:
each **technological revolution** brings a new cheap key input, new infrastructure and a new "common sense" of how to organise,
and unfolds over a **great surge** of about half a century in two halves.

| Surge (Perez) | Big bang | Cheap key input | New infrastructure | Organisational model |
|---|---|---|---|---|
| 1. industrial revolution | 1771, Arkwright's Cromford mill | cotton, pig iron | canals, turnpikes, water power | the factory |
| 2. steam and railways | 1829, the Rocket | coal, iron | railways, the telegraph, ports | the joint-stock company |
| 3. steel, electricity and heavy engineering | 1875, Carnegie's Bessemer steel plant | steel, copper | steel ships, the electric grid, world telegraph | the large firm; science in industry |
| 4. oil, cars and mass production | 1908, the Model T | oil, gas, synthetic materials | roads, airports, pipelines, universal electricity, radio | mass production, the multidivisional firm, the welfare state |
| 5. information and telecoms | 1971, the Intel microprocessor | the chip | digital networks, fibre, satellites | networks, flexible firms, platforms |

**Installation and deployment.** In the first twenty to thirty years (**installation**) financial capital pours money into the new
infrastructure, ending in a bubble (canal mania, the 1840s railway mania, the 1920s, dot-com). A crash and turning point follow,
often with new institutions (utility and securities regulation after 1929). Then **deployment**: productive capital and the state
spread the paradigm through the economy for another twenty to thirty years (the postwar boom), using cheaply the infrastructure
the bubble over-built.

### 8.3 How infrastructures layer
| New network | Rode on the earlier layer's | And in turn carried |
|---|---|---|
| telegraph | railway rights of way; railway demand for signalling | price information for the railways' freight markets |
| electric grid | coal by rail; steam engines; city franchises | telephone exchanges, trams, electrochemistry, everything after |
| telephone | telegraph poles and know-how; electric power | radio's first engineers (from the lamp makers), data networks |
| roads for cars | horse roads; refinery asphalt; cement; petrol taxes | trucks, buses, suburbs, rural tractors and fuel distribution |
| water and sewers | iron pipe, steam pumps, municipal borrowing | dense cities; the workforce for every later industry |
| airways | radio, radar, aluminium, refineries | air freight for high-value supply chains |
| internet | the telephone network's lines and switching; computers | voice, video, finance, retail, software as services |
| fibre backbones | railway and pipeline corridors; old telegraph cable routes | data centres, which in turn draw on the grid |

Each new network lowers the cost of building the next one, by lending its corridors, its capital markets and its regulators; and
each also **locks in** standards (track gauge, voltage and frequency, the plug, the QWERTY keyboard, TCP/IP) that later layers
inherit.

## 9. A combined dependency tree

```
ORGANIC ECONOMY (land, wood, beasts, water wheels, crafts)       ◄── the engine today
 └─ INDUSTRIAL LAYER (other file): coal ─ steam ─ iron/steel ─ machine tools ─ railways ─ factory ─ joint-stock finance
     │
     ├─ CHEMISTRY I (coal tar, gas works) ── dyes ── research labs ── drugs ── explosives
     │                                          └── Bakelite (phenol)
     ├─ ELECTRICITY (coal/hydro + steam turbine + copper + glass + franchises)
     │    ├─ lighting ── lamp industry ── vacuum tube ──┐
     │    ├─ motors ── unit drive ── the flow factory   │
     │    ├─ electrochemistry ── aluminium, chlorine, arc steel, silicon
     │    ├─ trams ── streetcar suburbs                 │
     │    └─ appliances (needs wired houses + consumer credit)
     │                                                  │
     ├─ TELEGRAPH (batteries + wire + railway rights of way + gutta-percha)
     │    └─ TELEPHONE (+ electricity + exchanges) ── Bell Labs ── transistor ─┐
     │         └─ RADIO (+ vacuum tube) ── broadcasting ── TV                  │
     │                                                                        │
     ├─ WATER AND SANITATION (iron pipe + steam pumps + cement + germ theory + municipal bonds)
     │    └─ chlorination (+ chlor-alkali) ── dense, healthy cities ── dams + irrigation (+ hydro)
     │
     ├─ OIL (drilling + distillation + rail tank cars + pipelines)
     │    ├─ kerosene ── (displaced by electric light)
     │    ├─ gasoline/diesel + INTERNAL COMBUSTION ENGINE (+ machine tools + steel)
     │    │     ├─ CARS (+ sheet steel + rubber + glass + assembly line + consumer credit)
     │    │     │     └─ ROADS (+ asphalt + cement + petrol taxes) ── trucks, suburbs
     │    │     ├─ TRACTORS ── land freed from feeding beasts ── farm labour to cities
     │    │     └─ FLIGHT (+ aluminium + aerodynamics + airmail subsidy)
     │    │           └─ JETS (+ superalloys + kerosene + radar + ATC + ICAO) ── air freight
     │    └─ PETROCHEMICALS (steam cracking) ── plastics, synthetic rubber, fibres
     │
     ├─ CHEMISTRY II: HABER–BOSCH (high-pressure steel + coal/gas hydrogen + electricity)
     │    └─ fertiliser ─┬─ + semi-dwarf seed + irrigation + pesticides + credit ── GREEN REVOLUTION
     │                   └─ population (about half the world fed by it)
     │
     └─ COMPUTING (punched cards + office bureaucracy ── vacuum tube ── transistor ◄──┘
          + electric-arc silicon + pure chemistry + optics + lithography + clean power)
          ├─ integrated circuit ── microprocessor ── software industry
          └─ + telephone network ── INTERNET ── platforms; data centres (back onto the grid)
```

## 10. The paradigms in economy_web's vocabulary

| Paradigm | Dominant shapes | The switch it made | The chokepoints it created |
|---|---|---|---|
| electricity | network, increasing returns, time capital, long skill | shaft and belt to unit drive; gas to electric light | copper; hydro sites; equipment makers' patents; the utility franchise |
| oil and the engine | joint products, chokepoint, increasing returns, network | horse to tractor and truck; coal to oil as feedstock | refining (Standard Oil), the fields, rubber plantations |
| chemistry | joint products, long skill, assembly, commons | manure and nitrate to synthetic fertiliser | Chilean nitrate (before), patents and trial costs (after) |
| water and sanitation | time capital, public good, commons | wells and cesspits to mains and sewers | rivers and aquifers; municipal borrowing power |
| telecoms | network, increasing returns | messenger and mail to wire and wave | gutta-percha; spectrum; the monopoly network |
| flight | network, assembly, long skill | ship and train to aircraft for people and high-value goods | airports and slots; engine makers |
| computing | assembly, chokepoint, increasing returns, long skill | clerk and ledger to machine record | lithography, leading-edge fabs, rare elements |

Two shapes appear here that the medieval web lacks or holds only in miniature: the **network** (the mill race and the road are its
nearest kin) and the **science-based long skill** held by an organisation (the laboratory), not a person.

## 11. What a simulator could take from this

None of these paradigms is close to what a village-scale society of LLM agents can reach, and most will never be represented as
machines. What can be represented are their **shapes**, and a few as **aggregate capabilities** that a large, long-lived world
earns once it holds the layers they need. Three uses, nearest first.

### 11.1 Lessons that apply now, inside the medieval web
These do not need any later technology; they are how the later paradigms behaved, and the same mechanics already exist at small
scale:
- **The payoff of a switch waits on complements and reorganisation.** The village mill and oven (economy_web §2.1) should, like
  the dynamo, pay little until the people around them change how they work (bringing grain in batches, a baker's schedule, a
  rent). A simulator can show this only if the gain from a work depends on how it is used, not just on its existence.
- **Joint products decide which chains live.** Gasoline, coal tar and asphalt were wastes before they were industries. The
  medieval web's carcass, coppice and tan pit already work this way; a design that leaves by-products useful somewhere is what
  lets later chains grow.
- **The chokepoint is often the middle step.** Standard Oil controlled refining, not wells; ASML controls lithography, not
  silicon. In the village, the mill, the anvil and the weir are such middles, and their owners are the natural poles of leverage
  that docs/scenario_design.md asks for.
- **Networks leave out their thin edges** unless an institution pays (the REA's cooperatives). A road, a ford or a market that the
  far hamlet never gets is the same shape.

### 11.2 As aggregate capabilities, at town and region scale
If the world grows to regions with towns, rule-driven populations and runs of years (02zzi §6), some paradigms could exist as a
**capability of a place or an institution**: a coarse level that changes yields, costs, mortality or the speed of information,
earned by meeting its prerequisites and paid for by upkeep, never as individual machines. Paradigm by paradigm, with the coal
switch (the industrial file's) as the gate before most of them:

| Paradigm | Could it be represented? | Abstraction (a capability, not a machine) | Its ancestor in the medieval web | What the world must contain before it could emerge |
|---|---|---|---|---|
| **water and sanitation** | yes, the nearest: a town-scale work | a town's water and drains as one work that lowers death rates in proportion to crowding; upkeep in labour and coin | the well, the river, the cellar | towns dense enough to suffer an urban penalty; disease that depends on crowding and water; a town institution able to levy and borrow; stone, lime and a mason's long skill; a spring or river to draw on |
| **chemistry and fertiliser** | its early form only | a field's yield ceiling raised by a bought input; a "works" that turns a waste into a good | dung, lime and marl (L); the tan pit and the carcass's by-products | soil that runs down (D4-102's capacity ladder); a mined input found in one place (lime, marl; nitrate far later), so the gain is a trade, not a gift; by-products with no use yet, waiting for one |
| **electricity** | only as its shape: power by network | a power level at a place, supplied from a fixed source along a built line, shared by several users | the mill race and the water wheel | a power source fixed in space (river, later coal); lines as built works along the place graph with upkeep and a toll; enough users for the load to matter; an owner, so rent and regulation become questions |
| **oil and the engine** | only as its shape: cheaper movement of bulk | the cost and speed of moving goods along an edge of the graph, set by the road and the vehicle | the pack ox, carts on tracks (L) | roads as built works with upkeep and public money; a fuel or fodder that vehicles consume, from somewhere else; places worth reaching; land freed when beasts are no longer fed |
| **telecommunications** | yes, as the speed of information | the delay with which prices and news travel between places | the carrier, the traveller's news | prices that exist and differ between places ("prices that travel", 02zzi §6); markets in several places; an institution running the line that can sell or withhold its speed |
| **flight** | no, except as a far-horizon given | a fast, dear edge between distant nodes for people and high-value goods | none | a world of many regions, high-value light goods, a state to license and control routes |
| **computing** | no, except as a far-horizon given; its institutional cousin, records, is near | a cheaper cost of keeping records and coordinating at a distance | records and ledgers (D2-33) | writing and records; bureaucracies with something to count; for computing proper, the whole of §7.3 |
| **organised knowledge** (the laboratory, behind chemistry, electricity and computing) | yes, as an institution | an institution that turns resources and years into new known methods | teaching and upbringing (4c §3.3) | methods that can be discovered, not only taught; records; a patron who will pay for years before any return |

The rule for every row: the capability **must not be granted**; it should be earned by assembling its inputs, so that a world can
see the dependency structure of §9 in miniature, and fail to reach a capability for want of one layer.

### 11.3 As the far horizon, for benchmarks and generated worlds
Electricity, oil, chemistry, flight and computing at their real scale assume hundreds of millions of people, global trade, science
as a profession and states with large budgets. A society simulator could include them only in a **generated world that begins
already industrial**: its agents as heads of firms, utilities, ministries and unions, its population rule-driven, its paradigms as
given infrastructures with owners. Such a world could study the questions this history raises without simulating machines: who
captures a chokepoint (the refinery, the fab), whether a network monopoly is regulated or broken up, whether a bubble forms in the
installation phase, how long a reorganisation takes after a GPT arrives, and whether thin edges get served. These are
institutional questions, and the engine's strength is institutions; the machines would be numbers in a table.

### 11.4 What to avoid
**A tech tree of buttons** (the history is a web of assemblies, joint products and institutions, not steps that unlock steps);
**instant payoffs** (every paradigm here took decades and reorganisation to pay); and **leaving out the institutions**
(franchises, utility regulation, municipal bonds, drug testing, air traffic control and spectrum licences were as necessary as the
machines).

## Sources

Figures and claims, by key used in the text. Web sources were checked on 15 Nov 2026; numbers marked *(rough)* in the text vary
between sources or are orders of magnitude.

- **[ACS landmark]** American Chemical Society, National Historic Chemical Landmark: deep-tank fermentation of penicillin at
  Pfizer; with Hektoen International, "Propagating penicillin in Peoria" (2024), for output in units.
  https://hekint.org/2024/03/21/propagating-penicillin-in-peoria-from-discovery-to-mass-production/ ;
  https://ohsonline.com/articles/2008/06/acs-honors-pfizer-for-wwii-penicillin-innovation.aspx
- **[ASML and trade press]** EUV machine cost, part and supplier counts, Zeiss and Trumpf roles:
  https://techovedas.com/one-e350m-machine-5000-suppliers-why-the-world-cant-build-chips-without-asml/ ;
  https://siliconcanals.com/sc-q-how-does-a-single-company-in-a-dutch-town-of-roughly-48000-people-build-the-only-machines-able-to-print-the-worlds-most-advanced-chips-with-its-newest-model-costing-about-e350-million/
  ; https://laserfocusworld.com/blogs/article/14039015/how-does-the-laser-technology-in-euv-lithography-work (secondary; treat as
  approximate).
- **[Bresnahan and Trajtenberg 1995]** T. Bresnahan and M. Trajtenberg, "General purpose technologies: 'engines of growth'?",
  *Journal of Econometrics* 65 (1995) 83–108.
- **[Britannica; The Henry Ford]** Model T prices and assembly times: https://www.britannica.com/technology/Model-T ;
  https://www.historyhit.com/ford-model-t-the-invention-of-the-worlds-first-affordable-car/
- **[Census 2023]** US Census Bureau, History, radio ownership in 1930 (40.3% of households):
  https://census.gov/about/history/stories/monthly/2023/september-2023.html
- **[Census 2026; IEEE Milestone]** Pearl Street Station:
  https://www.census.gov/about/history/stories/monthly/2026/september-2026.html ;
  https://ethw.org/Milestones:Pearl_Street_Station,_1882
- **[Chandler 1977]** A. D. Chandler, *The Visible Hand: The Managerial Revolution in American Business* (1977).
- **[Cutler and Miller 2005]** D. Cutler and G. Miller, "The role of public health improvements in health advances: the
  twentieth-century United States", *Demography* 42 (2005); NBER WP 10511. https://www.nber.org/papers/w10511.pdf
- **[David 1990]** P. A. David, "The dynamo and the computer: an historical perspective on the modern productivity paradox",
  *American Economic Review* 80(2) (1990) 355–361.
- **[Devine 1983]** W. D. Devine Jr., "From shafts to wires: historical perspective on electrification", *Journal of Economic
  History* 43(2) (1983) 347–372 (steam about 80% of drive around 1900; electricity the major source by 1920; output per man-hour
  1.3% a year before 1919, 3.1% after).
- **[Encyclopedia.com, Hall]** Aluminium price 1888 and 1893:
  https://www.encyclopedia.com/science/news-wires-white-papers-and-books/hall-charles ; Science History Institute, Héroult and
  Hall: https://sciencehistory.org/education/scientific-biographies/paul-heroult-and-charles-m-hall
- **[Erisman et al. 2008]** J. W. Erisman, M. Sutton, J. Galloway, Z. Klimont and W. Winiwarter, "How a century of ammonia
  synthesis changed the world", *Nature Geoscience* 1 (2008) 636–639.
  https://www.iai.int/admin/site/sites/default/files/uploads/2008.Erisman-et-al_NatureGeo.pdf
- **[Freeman and Louçã 2001]** C. Freeman and F. Louçã, *As Time Goes By: From the Industrial Revolutions to the Information
  Revolution* (2001).
- **[Geyer, Jambeck and Law 2017]** R. Geyer, J. Jambeck and K. Law, "Production, use, and fate of all plastics ever made",
  *Science Advances* 3 (2017) e1700782. https://pmc.ncbi.nlm.nih.gov/articles/PMC5517107/
- **[Global Taiwan Institute 2023]** TSMC's share of leading-edge chips; China's share of gallium:
  https://globaltaiwan.org/2023/12/despite-chinese-market-controls-taiwans-semiconductor-supply-chain-remains-secure/
- **[Gordon 2016]** R. J. Gordon, *The Rise and Fall of American Growth* (2016); TFP figures as reported in Levy Institute WP 998:
  https://www.levyinstitute.org/pubs/wp_998.pdf
- **[IATA 2025]** IATA, "Air cargo, trade and economic growth in 2025" (under 1% of trade by weight, close to a third by value):
  https://www.iata.org/en/iata-repository/publications/economic-reports/air-cargo-trade-and-economic-growth-in-2025
- **[IEA 2025]** International Energy Agency, *Energy and AI* (2025), executive summary (data centres 415 TWh in 2024, about 1.5%;
  about 945 TWh by 2030): https://www.iea.org/reports/energy-and-ai/executive-summary
- **[Industry summaries, ammonia]** Global ammonia output (about 183 Mt, 2020), energy share and emissions:
  https://www.weforum.org/stories/2023/11/green-ammonia-climate-change-energy-transition/ ;
  https://abnamro.com/research/en/our-research/esg-economist-what-is-the-role-of-green-ammonia-in-decarbonizing-the-world
  (secondary).
- **[ITU 2024]** ITU, *Facts and Figures 2024* (5.5 billion online, 68%):
  https://www.itu.int/en/mediacentre/Pages/PR-2024-11-27-facts-and-figures.aspx
- **[Japan economy text, via Asanuma and Cusumano]** Toyota and Japanese makers buying about 80% of parts from affiliated
  suppliers, GM making more than half in house: https://muse.jhu.edu/books/9780824863050/9780824863050-31.pdf ; background in B.
  Asanuma (1985) and M. Cusumano, *The Japanese Automobile Industry* (1985).
- **[Lipsey et al. 2005]** R. Lipsey, K. Carlaw and C. Bekar, *Economic Transformations: General Purpose Technologies and
  Long-Term Economic Growth* (2005); and E. Helpman (ed.), *General Purpose Technologies and Economic Growth* (1998).
- **[London Museum]** "How Bazalgette built London's first super-sewer":
  https://londonmuseum.org.uk/collections/london-stories/how-bazalgette-built-londons-first-super-sewer/
- **[Olmstead and Rhode 2001]** A. Olmstead and P. Rhode, "Reshaping the landscape: the impact and diffusion of the tractor in
  American agriculture, 1910–1960", *Journal of Economic History* 61(3) (2001) 663–698.
  https://faculty.econ.ucdavis.edu/faculty/alolmstead/Recent_Publications/Reshaping_the_Landscape.pdf
- **[Perez 2002]** C. Perez, *Technological Revolutions and Financial Capital: The Dynamics of Bubbles and Golden Ages* (2002).
  https://en.wikipedia.org/wiki/Technological_Revolutions_and_Financial_Capital
- **[Richmond Fed 2020]** Federal Reserve Bank of Richmond, *Econ Focus* 2020 Q1, "Economic history: electrifying rural America":
  https://www.richmondfed.org/publications/research/econ_focus/2020/q1/economic_history
- **[Steinwender 2018]** C. Steinwender, "Real effects of information frictions: when the States and the Kingdom became united",
  *American Economic Review* 108(3) (2018) 657–696; summaries at
  https://cepr.org/article/how-information-frictions-affect-trade-and-price-patterns and
  https://www.richmondfed.org/publications/research/econ_focus/2018/q2/economic_history
- **[The Henry Ford, Rouge history]** https://www.thehenryford.org/visit/ford-rouge-factory-tour/history-and-timeline ; the 1940
  flow chart "Complete car can be built in 28 hours": https://www.thehenryford.org/collections/explore/artifact/33887
- **[USDA census tables]** Tractors and work animals on US farms: Census of Agriculture graphic summaries,
  https://agcensus.library.cornell.edu/ (1945, 1954, 1959 volumes); 1920 and 1930 counts as given in contemporary USDA tables
  (OCR, approximate).
- **[USDA ERS 2024]** "Global changes in agricultural production, productivity, and resource use over six decades", *Amber Waves*
  (Sept 2024):
  https://ers.usda.gov/amber-waves/2024/september/global-changes-in-agricultural-production-productivity-and-resource-use-over-six-decades
- **[Wikipedia, transistor count]** https://en.wikipedia.org/wiki/Transistor_count
- **[Womack, Jones and Roos 1990]** J. Womack, D. Jones and D. Roos, *The Machine That Changed the World* (1990).
- **Standard works behind the narrative** (not cited for specific numbers): T. P. Hughes, *Networks of Power* (1983) on Edison,
  Insull and the grid; D. Yergin, *The Prize* (1991) on oil; V. Smil, *Enriching the Earth* (2001) on Haber–Bosch and *Creating
  the Twentieth Century* (2005); W. Cronon, *Nature's Metropolis* (1991) on Chicago's markets and the telegraph; F. Hayek, "The
  use of knowledge in society" (1945); G. Stigler, "The economics of information" (1961); R. Solow, "We'd better watch out", *New
  York Times Book Review* (12 July 1987); E. Brynjolfsson and L. Hitt, "Beyond computation" (2000); C. Miller, *Chip War* (2022);
  J. Schumpeter, *Business Cycles* (1939); N. Kondratiev, "The long waves in economic life" (1925).
- **In the project:** 02zzi_economies_scaling.md (the frame, the organic economy, §6 on scaling the engine);
  docs/cybertron2/proposals/economy_web.md (chain shapes, the medieval web); docs/scenario_design.md (leverage and chokepoints);
  D4-102, D4-24, 4c §3.3 as cited in 02zzi.
