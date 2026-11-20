---
id: docs/review/37_growth/02zzj_economy_research/13_modern_global_industries.md
kind: note
updated: "2026-11-15"
---
# 13: Modern global industries and their supply chains (20th and 21st centuries)

*note · `docs/review/37_growth/02zzj_economy_research/13_modern_global_industries.md`*

> The twentieth century turned production from something a firm did in one place into something a network of firms does across the world. Ford's Highland Park and River Rouge plants (1913 to 1927) put nearly everything under one owner and one roof: ore came in by Ford's own ships and left as cars. Toy


Part of the 02zzj economy research folder (37.2, 15 Nov 2026), for the designers of Cybertron 2. Another file covers the
technology paradigms themselves (electricity, oil, chemistry, flight, computing); this one covers the industries built on them
as an economy: how mass production was organised and reorganised, seven supply chains traced end to end, logistics, energy
systems, services, the chokepoints of today, and the dependency trees behind ordinary goods. Chain shapes are named in the
vocabulary of `docs/cybertron2/proposals/economy_web.md` §1 (shallow, accretive, paradigm switch, substitutes, joint products,
assembly, chokepoint, long skill, time capital, pulse, commons, increasing returns). Figures carry a source tag (list at the end);
**(rough)** marks an order of magnitude or a commonly repeated figure I could not pin to a primary source; **(contested)** marks a
figure that serious sources dispute. Nothing here is limited by what a simulator could afford to run.

## Summary

The twentieth century turned production from something a firm did in one place into something a network of firms does across
the world. Ford's Highland Park and River Rouge plants (1913 to 1927) put nearly everything under one owner and one roof: ore came
in by Ford's own ships and left as cars. Toyota, from the 1950s, showed that a car maker could do better by owning less and
coordinating more: a tiered web of long-term suppliers delivering just in time, with problems stopped at the line rather than
buffered with stock. From the 1980s cheaper communication, the container and the opening of China let firms cut the chain into
fine slices and put each slice where it was cheapest or best done. By 2008 about half of world trade was in intermediate goods
crossing borders inside such chains (World Bank WDR 2020). The design, brand and after-sales ends of a chain capture most of the
value; fabrication and assembly in the middle capture little (the "smile curve"). Every finished good now rests on a dependency
tree of hundreds of firms in dozens of countries, and a few nodes in each tree have no substitute.

Two consequences matter most for a simulator. First, **specialisation compounds wealth and fragility together**: concentrating
each step where it is done best makes the whole cheaper and makes the whole depend on single points (one Dutch firm for EUV
lithography, one Taiwanese firm for most leading-edge chips, one North Carolina town for most high-purity quartz, one country
for most rare-earth separation, a handful of straits and two canals for shipping). Shocks at those points (the 2011 Japan
earthquake, the 2021 chip shortage, the Ever Given, the Red Sea attacks, the 2025 rare-earth export licensing) propagate through
the whole tree in weeks. Second, **the economy became mostly services**: in the United States farming fell from 41% of the
workforce in 1900 to under 2% by 2000, manufacturing peaked at 32% of non-farm jobs in 1953 and is now under 9%, and the world as
a whole moved from 44% farming in 1991 to about 27% by 2019, with services passing half of all jobs. The goods economy did not
shrink; it became so productive and so coordinated that most people now work at coordinating it, financing it, selling it, or
caring for each other.

## 1. Mass production and its organisation

### 1.1 Fordism: the moving line and vertical integration

| Step | What changed | Numbers |
|---|---|---|
| Interchangeable parts, fixed jigs | parts made to gauge, no fitting at assembly | precondition (American system, 19th century) |
| Moving assembly line, Highland Park, 7 Oct 1913 | the work moves past the worker; each does one task | chassis time from about 12.5 hours to about 93 minutes over 1913 to 1914 (sources differ on whether elapsed time or labour hours; AM) |
| The five-dollar day (Jan 1914) | wages doubled to hold workers on dull, fast work | turnover had been several hundred per cent a year (rough) |
| Price falls | volume and learning | Model T from $850 (1908) to about $260 (mid 1920s) (AM) |
| River Rouge (1917 to 1927) | ore, coal, sand and rubber in; cars out | ore to finished car in about 28 hours (Britannica; commonly cited, not precisely documented); about 100,000 workers at peak; Ford owned railways, ore freighters, mines, forests and a Brazilian rubber plantation; still at least 6,000 outside suppliers (BRIT, CLUI) |

**The shape:** a paradigm switch with increasing returns. Past a volume threshold, one owner of the whole chain (vertical
integration) is cheaper than buying at each step, because the line cannot stop for a late or bad part. The cost is rigidity: one
model, one colour (the Model T), and the whole chain idle when demand changes. General Motors under Alfred Sloan answered in the
1920s with a range of models at price steps and the annual model change, and with divisions run on financial targets: the
**multidivisional firm**, which Alfred Chandler made the centre of his account of modern business (*The Visible Hand*, 1977).

**What it did to society:** mass employment in very large plants, the industrial union (the UAW, the 1937 sit-down strike at GM),
the company town, and a consumer who could buy what he made. "Fordism" became a name for a whole social settlement of high wages,
mass consumption and standardised goods.

### 1.2 Lean production: Toyota and the supplier network

Toyota after 1950 could not afford Ford's scale or stocks. Taiichi Ohno and Eiji Toyoda built what became the **Toyota Production
System**:

- **Just in time (JIT):** each part arrives when needed, in the quantity needed; the downstream process pulls with a card
  (*kanban*) rather than the upstream process pushing to a plan.
- **Jidoka:** a machine or worker stops the line at the first defect (the andon cord), so problems are fixed at their source
  rather than buffered.
- **Small lots and quick die changes,** so many models share one line.
- **Keiretsu suppliers:** a tiered network of long-term suppliers, often part-owned, who design parts with Toyota, share costs and
  improvements, and are not dropped for a cheaper bid.

The MIT International Motor Vehicle Program's comparison (Womack, Jones and Roos, *The Machine That Changed the World*, 1990)
found the typical mass-production plant needed about 31 labour hours per car, with 130 defects per 100 cars and about two weeks
of parts stock; the lean plant needed about 16 hours, 45 defects and about two hours of stock (MIT IMVP, reported via TST; the
plant-level pair was GM Framingham against Toyota Takaoka). NUMMI (1984), the GM-Toyota joint venture in a closed GM plant,
showed that much of the gap was organisation, not culture or machinery.

**The supplier network as a capability.** In February 1997 a fire destroyed Aisin Seiki's Kariya plant, which made about 99% of
the brake proportioning valves (P-valves) Toyota used; with about two hours of stock, Toyota's assembly stopped. More than 200
firms of the Toyota group, about 70 of them making valves they had never made, improvised production from Aisin's drawings, and
Toyota's plants were running again within about five days (Nishiguchi and Beaudet 1998; WIKI-AISIN; sources give two to five
days). The single source was a fragility; the network of trust around it was a resilience that a market of arm's-length bidders
would not have had.

### 1.3 Outsourcing, offshoring and the second unbundling

| Phase | Driving change | Form |
|---|---|---|
| 1950s to 1970s | tariffs falling (GATT rounds); the container (§3) | multinationals build whole plants abroad to serve local markets |
| 1970s to 1990s | export-processing zones (Mexico's maquiladoras, East Asian zones, Shenzhen 1980) | labour-intensive steps (garments, electronics assembly) moved to low-wage coasts |
| 1990s to 2008 | cheap telecoms and the internet; China in the WTO (2001); India's IT services | the chain cut into fine slices across countries; contract manufacturers (Foxconn, Flextronics); fabless chip firms and foundries (TSMC, 1987) |
| 2008 to now | trade growth slows; wages rise in China; shocks; industrial policy | "China plus one", near-shoring, re-shoring of strategic steps (chips, batteries, drugs) |

Richard Baldwin (*The Great Convergence*, 2016) calls the first step the **first unbundling** (steam and the ship let goods be
made far from where they are used) and the 1990s step the **second unbundling** (information technology let the *factory* be
split, with know-how sent with the work). The World Bank's *World Development Report 2020* puts trade inside global value
chains at almost half of all world trade, growing fast through the 1990s and 2000s and stalling after 2008 (WDR 2020).

### 1.4 Global value chains, governance, and the smile curve

**Gary Gereffi** (1994) separated **producer-driven chains** (cars, aircraft, chips: the lead firm controls technology and
production) from **buyer-driven chains** (garments, toys, food: the lead firm is a brand or retailer that designs and sells but
owns no factory). Gereffi, Humphrey and Sturgeon (2005) gave five forms of governance between a lead firm and its suppliers,
from least to most explicit coordination and power (GHS 2005):

| Form | When it arises | Example |
|---|---|---|
| **market** | simple, codifiable transactions; capable suppliers | commodity steel, grain |
| **modular** | complex product, but specifications can be written down; capable suppliers | electronics contract manufacturing |
| **relational** | complex, hard to codify; capable suppliers; trust and reputation | Toyota's keiretsu; luxury apparel |
| **captive** | codifiable, but suppliers weak; dependent on one buyer | small garment factories for one brand |
| **hierarchy** | complex, uncodifiable, no capable suppliers | vertical integration (Ford's Rouge) |

**The smile curve** (Stan Shih, founder of Acer, about 1992): plot value added along the chain, from R&D and design, through
components, fabrication and assembly, to marketing, distribution and service. The curve is high at both ends and low in the
middle. The iPhone shows it most clearly: in 2010 Apple kept about 58.5% of the sale price as profit, materials were about 21.9%,
non-Chinese labour about 3.5%, and Chinese assembly labour about 1.8% (Kraemer, Linden and Dedrick 2011, KLD). The country of
assembly records the whole value as an export while adding a sliver of it.

### 1.5 Just in time and its fragility

| Shock | What failed | Effect |
|---|---|---|
| Aisin fire, Feb 1997 | one plant, about 99% of one valve | Toyota stopped; restarted in about five days through the supplier network (§1.2) |
| Tohoku earthquake and tsunami, Mar 2011 | Renesas Naka plant and many tier 2 and tier 3 suppliers | Renesas then about 18 to 20% of automotive microcontrollers (some sources say 40% of auto chips, likely a broader measure); Naka out for about three months; car output cut worldwide; Toyota found it did not know its own tier 3 suppliers (TTAC, IEEE) |
| Thailand floods, late 2011 | hard-drive plants and parts makers on one flood plain | world hard-drive supply cut sharply for months (rough) |
| COVID-19, 2020 to 2022 | factories, ports, container positioning | container freight Shanghai-Europe and transpacific spot rates up several-fold; Drewry's composite index peaked at about $10,375 per 40-foot box in Sep 2021 (DREWRY) |
| Chip shortage, 2021 | car makers cancelled chip orders in 2020, chip makers reallocated to electronics; then Texas freeze, Renesas Naka fire (Mar 2021) | about 7.7 million vehicles of production lost and $210 billion of revenue in 2021 (AlixPartners, Sep 2021; ALIX) |
| Ever Given, Mar 2021 | one ship aground in the Suez Canal for six days | about $9 to 10 billion of trade held up per day (Lloyd's List estimate, LL) |
| Red Sea attacks, late 2023 on | ships diverted round the Cape | Suez trade volume down about 50% year on year in early 2024; container transits down far more (IMF PortWatch; IMF) |
| China's rare-earth licensing, Apr 2025 | export licences for seven medium and heavy rare earths and their magnets | magnet exports more than halved in a month; some car plants outside China cut output for lack of magnets (SMM, ENGNEWS) |

**The lesson the car industry drew:** just in time removes buffer stock, which is cheap insurance; once removed, every single
source becomes a point of failure. The 2021 response was **just in case**: buying chips directly, holding months of stock of
critical parts, mapping suppliers to tier 3 and beyond. Toyota itself, after 2011, built a supplier database and held stocks of
chips, which is one reason it weathered 2021 better than most.

## 2. Seven supply chains, end to end

Each traced from the ground to the user. Countries and shares are the largest or most typical, not the only route.

### 2.1 A car

**The shape:** assembly (the scarcest of about 30,000 parts limits the whole), increasing returns at the assembler, a long tiered
web of suppliers, and since 2020 a chokepoint in chips.

```
car (OEM: Toyota, VW, GM, Hyundai, Stellantis, BYD, Tesla)
├── body in white: sheet steel (≈ 0.9 t of steel per car, rough) ← steel mill ← iron ore (Australia, Brazil) + coking coal
│                  aluminium (closures, EV frames) ← smelter (cheap power) ← alumina ← bauxite (Guinea, Australia)
├── powertrain
│   ├── ICE: engine block (cast iron or aluminium), crankshaft (forged steel), turbo, fuel system, exhaust with
│   │        catalytic converter ← platinum, palladium, rhodium (South Africa, Russia)
│   └── EV: battery pack ← cells (CATL, LG, BYD, Panasonic) ← cathode (lithium, nickel, cobalt, manganese or iron phosphate)
│           + anode (graphite, China > 90%) + electrolyte + separator; motor ← rare-earth magnets (NdFeB; China ≈ 90%)
│           + copper windings; inverter ← silicon carbide power chips
├── transmission and axles ← gears (alloy steel), bearings (SKF, Schaeffler)
├── electronics: 1,000 to 3,000 chips in a modern car (estimates vary from a few hundred to 3,000 with the definition of
│   "chip"; CHI-FED, YOLE): microcontrollers (Renesas, NXP, Infineon), sensors, power chips, memory, displays
│   ├── wiring harness: ≈ 1 to 5 km of copper wire, hand-assembled in Mexico, Morocco, Eastern Europe, Philippines (rough)
│   └── software: tens to hundreds of millions of lines of code (rough)
├── interior: seats (foam ← petrochemicals; steel frames; textiles or leather), dashboard plastics, glass (float glass)
├── tyres ← natural rubber (Thailand, Indonesia) + synthetic rubber (oil) + carbon black + steel cord
├── paint ← pigments (titanium dioxide), resins
└── services: design and engineering; crash testing and type approval; finance (loans, leasing); insurance; dealers; fuel
    or charging; repair and parts; roads
```

| Layer | Who | What they hold |
|---|---|---|
| OEM (assembler) | 15 or so groups make most of the world's ~90 million vehicles a year (rough) | brand, platform design, final assembly, the dealer network |
| Tier 1 | Bosch, Denso, ZF, Magna, Continental, Hyundai Mobis, CATL | whole systems: brakes, seats, electronics, batteries |
| Tier 2 | thousands of firms | components: chips, bearings, castings, harness parts |
| Tier 3 and raw | tens of thousands | raw materials, basic parts, chemicals |

**Minerals:** the IEA's 2021 estimate is that a typical electric car needs about six times the mineral input of a conventional one
(about 207 kg against about 34 kg, excluding steel and aluminium), mostly copper, graphite, nickel, lithium, manganese and cobalt
(IEA 2021, rough at the kg level).

**The 2021 lesson:** a car with 30,000 parts stops for want of a $1 microcontroller. Car chips are mostly on older, cheap
nodes made by a few firms; car makers were small customers for chip makers (around a tenth of chip demand, rough) and had
cancelled orders. The car chain had no say over a node on which it wholly depended.

### 2.2 A smartphone

**The shape:** assembly across the most countries of any common good; chokepoints at both the deepest raw end (minerals) and the
most advanced manufacturing end (leading-edge chips, EUV); the smile curve at its steepest.

```
smartphone (brand: Apple, Samsung, Xiaomi; design in California, Seoul, Beijing)
├── system-on-chip (A-series, Snapdragon)
│   ├── design: brand or Qualcomm/MediaTek; ARM instruction set (UK); EDA software (Synopsys, Cadence: US)
│   ├── fabrication: TSMC (Taiwan) at 3 to 5 nm
│   │   ├── lithography: ASML EUV (Netherlands) ← Zeiss optics (Germany, sole source) + Cymer light source (US) +
│   │   │   TRUMPF CO2 laser (Germany) + ≈ 5,000 suppliers
│   │   ├── other tools: Applied Materials, Lam, KLA (US); Tokyo Electron (Japan)
│   │   ├── wafers: Shin-Etsu, SUMCO (Japan) ← polysilicon ← quartz; crucibles of Spruce Pine high-purity quartz (US)
│   │   ├── photoresists (JSR, TOK: Japan), specialty gases (neon: Ukraine pre-2022), ultra-pure water, fluorine chemicals
│   │   └── power and water: a leading fab uses as much electricity as a mid-sized city (rough)
│   └── packaging and test: ASE (Taiwan), Amkor; substrates (Ajinomoto build-up film: Japan, near-sole source)
├── memory: DRAM and NAND (Samsung, SK Hynix: Korea; Micron: US; Kioxia: Japan)
├── display: OLED (Samsung Display, LG Display: Korea; BOE: China) ← indium tin oxide, glass (Corning Gorilla Glass: US)
├── radio: modem, RF front end (Qualcomm, Broadcom, Skyworks, Qorvo: US) ← gallium arsenide (China ≈ 98% of primary gallium)
├── cameras: image sensors (Sony: Japan), lenses (Largan: Taiwan)
├── battery: lithium-ion cell (ATL: China) ← lithium (Australia, Chile), cobalt (DRC ≈ 75% mined, China ≈ 80%+ refined),
│            graphite (China)
├── magnets: speakers, haptics, camera stabilisation ← neodymium, praseodymium, dysprosium (China ≈ 90% separation)
├── frame: aluminium or titanium; tin solder (Indonesia, Myanmar); tantalum capacitors (DRC, Rwanda, Brazil); gold contacts
├── assembly: Foxconn, Pegatron, Luxshare (China; increasingly India and Vietnam)
└── services: operating system and app store (platform), mobile networks (spectrum, towers), cloud, repair, recycling
```

| Value split, iPhone 4 (2010) | Share of price |
|---|---|
| Apple's profit | ≈ 58.5% |
| materials (inputs) | ≈ 21.9% |
| non-Chinese labour (Japan, Korea, Taiwan, US, EU) | ≈ 3.5% |
| Chinese labour (assembly) | ≈ 1.8% |
| profits of Korean, Japanese, Taiwanese and other suppliers; distribution | the rest |

(KLD 2011; estimates from teardowns.) A 2023 teardown estimate put the iPhone 15 Pro Max's components at about $502 against a
$1,199 retail price (Counterpoint, CP).

**Elements:** a smartphone uses several dozen elements, often quoted as around 60 to 70 (rough). The cobalt end runs through
DRC mines, including artisanal mining with documented child labour (a part of DRC output, size contested), and through Chinese
refineries; the tantalum, tin, tungsten and gold ends are the "conflict minerals" of US Dodd-Frank §1502 (2010).

### 2.3 A cotton T-shirt

**The shape:** a buyer-driven chain (Gereffi), labour-intensive in the middle; substitutes with trade-offs at the fibre (cotton
against polyester); a long tail into secondhand trade. Pietra Rivoli's *The Travels of a T-Shirt in the Global Economy* (2005)
followed one shirt: cotton from near Lubbock, Texas, shipped to Shanghai for spinning, knitting and sewing, back to the US for
printing and sale, then donated and sold as used clothing in Tanzania (RIV).

```
T-shirt (brand or retailer: designs, orders, sells; owns no factory)
├── fibre
│   ├── cotton: seed (often GM Bt cotton) + fertiliser + pesticides + water (irrigated in much of India, Pakistan, Central Asia)
│   │   → picking (machine in US, Australia, Brazil; hand in much of India and Africa) → ginning (lint from seed; joint
│   │   product: cottonseed for oil and feed) → bales
│   │   Producers: China and India ≈ 25 to 28 million bales each; Brazil ≈ 17; US ≈ 14 (2024/25, USDA via Cotton Inc.)
│   │   Exporters: Brazil passed the US as largest in 2023/24; US ≈ 29% of world exports (USDA ERS)
│   └── or polyester ← PTA + MEG ← oil and gas (polyester is now over half of all fibre made; cotton about a fifth: rough)
├── yarn: spinning mills (China, India, Vietnam, Pakistan, Bangladesh)
├── fabric: knitting (jersey) → bleaching, dyeing, finishing (water, dyes, chemicals; heavy local water pollution)
├── garment: cutting, sewing (Bangladesh, Vietnam, Cambodia, China, Turkey, Honduras); trims, thread, labels; printing
├── logistics: carton → container → port → distribution centre → store or parcel
├── retail: the brand's margin, marketing, stores, e-commerce
└── after use: donation → sorting → bale export → secondhand markets (East Africa, Eastern Europe) → rags, landfill
```

**Numbers and structure:**
- Bangladesh: garments are over 80% of its exports, about $46 billion in 2022 (DT); the Rana Plaza collapse (24 April 2013)
  killed 1,134 garment workers and led to the Bangladesh Accord on fire and building safety (WIKI-RANA).
- The quota system of the Multi Fibre Arrangement (1974 to 2004) spread garment making across dozens of countries; its end in
  2005 concentrated it in China, Bangladesh and Vietnam.
- Water: a figure of about 2,700 litres for one cotton T-shirt is widely repeated (WWF and the Water Footprint Network); it
  depends heavily on irrigation and should be read as **(rough)**.
- The sewing worker's wage is commonly put at around 1% of the retail price or less **(rough, contested)**.

**Why it travels so far:** each step goes where it is cheapest given trade rules. Rivoli's finding was that politics (US cotton
subsidies, quotas, rules of origin) shaped the route as much as markets did.

### 2.4 A loaf of bread and a supermarket chicken

**The shape of bread:** the old grain-to-bread chain of economy_web.md §2.1, with every step now an industry. The farm share of a
US food dollar is about 12 to 16 cents depending on the USDA series (15.9 cents for 2023 in the older series; 12.1 cents in the
revised one; ERS); the other 84 to 88 cents go to processing, packaging, transport, retail, food service and energy.

```
sliced loaf in a supermarket
├── wheat
│   ├── seed (breeders; hybrid and licensed varieties)
│   ├── nitrogen fertiliser ← ammonia (Haber-Bosch) ← natural gas (hydrogen) + air; phosphate rock (Morocco, China) and
│   │   potash (Canada, Russia, Belarus)
│   ├── machinery: tractor, combine (Deere, CNH, AGCO) ← steel, engines, GPS, chips; diesel
│   ├── crop protection: herbicides, fungicides (Bayer, Syngenta, Corteva, BASF)
│   └── farm credit, crop insurance, futures (Chicago Board of Trade) to set and hedge price
├── storage and trade: country elevator → rail or barge → export terminal (US Gulf, Black Sea, Australia, Canada, Argentina)
│   → bulk carrier → import terminal; grain traders (ADM, Bunge, Cargill, Louis Dreyfus, COFCO); Russia and Ukraine together
│   were around 30% of world wheat exports before 2022 (rough)
├── flour mill: roller milling (joint products: flour, bran, germ → feed)
├── industrial bakery: flour + water + yeast + salt + fats + enzymes and improvers; the Chorleywood process (UK, 1961) cut
│   fermentation to minutes and made most British bread (rough share ≈ 80%); slicing and bagging machines; plastic bags
│   (polyethylene ← oil and gas)
├── distribution: bakery depot → supermarket regional distribution centre (cross-dock) → store, daily
└── supermarket: tens of thousands of product lines (rough); a cold chain, card payments, scanning, loyalty data
```

**The chicken:** the most industrialised animal chain. US broilers went from about 112 days to reach about 2.5 lb with a feed
conversion of 4.7 in 1925 to about 47 days to reach about 6.6 lb at a feed conversion of 1.69 in 2024 (NCC; USDA via FS).

```
packaged chicken breast
├── genetics: grandparent stock from two breeding firms (Aviagen, Cobb-Vantress) that supply most of the world's broiler
│   lines (rough: a large majority)
├── integrator (Tyson, Pilgrim's, Perdue, Sanderson/Wayne; in Brazil BRF and JBS) owns: breeder flocks → hatchery → chicks
│   → feed mill → processing plant → brand
├── contract grower owns the barns and labour, raises the integrator's birds, is paid per pound under a ranking ("tournament")
│   against other growers; bears the capital risk of the barns
├── feed: maize + soybean meal (Brazil, US, Argentina) + vitamins, amino acids (lysine, methionine from fermentation and
│   chemistry), antibiotics or replacements; the feed bill is most of the cost of a bird
├── processing: line speeds of over a hundred birds a minute (rough); chilling; cutting; packaging (plastic, foam trays)
├── cold chain: refrigerated trucks, distribution centres, store chillers (refrigerants; electricity)
└── inspection: state veterinary and food safety services; joint products: feet to China, feathers and offal to rendering
    (feed, pet food), litter to fields
```

**The shape of the chicken:** a vertically integrated chain where one firm holds every step except the barn, which is the step
with the most capital risk and the least power. It is Gereffi's captive governance inside a hierarchy.

### 2.5 Steel, from ore to building

**The shape:** increasing returns (huge blast furnaces, huge ore ships), joint products (slag to cement), and a substitute route
(the electric arc furnace on scrap) that switches the chain from mining to recycling.

```
steel beam or rebar in a building
├── route 1: blast furnace and basic oxygen furnace (BF-BOF), ≈ 70% of world steel (rough)
│   ├── iron ore (≈ 1.4 t per t of crude steel): Pilbara (Australia: Rio Tinto, BHP, Fortescue), Brazil (Vale), then India,
│   │   China; crushed, concentrated, pelletised or sintered; seaborne in 200,000 to 400,000-tonne bulk carriers
│   ├── coking coal (≈ 0.8 t of coal per t): Queensland (Australia), US, Canada, Russia, Mongolia → coke ovens (joint products:
│   │   coke-oven gas, tar, benzene)
│   ├── limestone (≈ 0.3 t) as flux → slag (→ cement and road base)
│   ├── scrap (≈ 0.12 t) in the converter
│   └── oxygen (air separation plants), refractories (magnesia, alumina), electricity, water
├── route 2: electric arc furnace (EAF), ≈ 30% (rough): scrap or direct-reduced iron (DRI, from gas or hydrogen) + electricity
│   (a city's worth of power per large furnace, rough) + graphite electrodes (needle coke)
├── secondary: ladle refining, alloying (manganese, chromium, nickel, molybdenum, vanadium, niobium), continuous casting
├── rolling: hot rolling to sections, plates, bars, coils; cold rolling, galvanising (zinc), coating
├── fabrication: steel service centres, fabricators cut, drill and weld sections to a design
└── services: structural engineering, codes and testing, trade finance, freight, erection crews, cranes
```

(Raw-material ratios from worldsteel, WSA-RM.) **Numbers:** world crude steel output was 1,882.6 million tonnes in 2024; China made
1,005.1 million tonnes, 53% (worldsteel, WSA). About half of all steel goes into buildings and infrastructure (worldsteel, rough).
Steel is commonly put at 7 to 9% of global CO2 emissions **(rough)**.

**The geography:** the ore is in Western Australia and Brazil, the coal in Queensland, the furnaces in China, and the steel in
Chinese cities. Australia-China iron ore is the world's largest bulk trade by tonnage (rough). In the BF-BOF route each step has
huge scale economies; in the EAF route, mini-mills (Nucor in the US, from the 1970s) made small, flexible plants competitive and
destroyed much of the old integrated industry (Clayton Christensen's standard example of disruption).

### 2.6 A pharmaceutical drug

**The shape:** time capital at its extreme (10 to 15 years before a sale), a pulse of profit during patent life, then a switch to
a commodity (generics) with the chain moved to the cheapest maker; chokepoints in a few ingredients and plants.

```
tablet at a pharmacy
├── discovery and development (≈ 10 to 15 years)
│   ├── basic science (universities, public funding: NIH ≈ $45 to 50 billion a year, rough)
│   ├── target, screening, medicinal chemistry; increasingly biotech start-ups licensed to large firms
│   ├── preclinical tests (contract research organisations; lab animals)
│   ├── clinical trials Phase I → II → III (thousands of patients; CROs: IQVIA, ICON); a small fraction of drugs entering
│   │   Phase I are approved, often put at about one in ten (rough)
│   ├── regulator review (FDA, EMA), patents and exclusivity
│   └── cost: about $2.6 billion per approved new drug including failures and the cost of capital (Tufts CSDD, DiMasi et al.
│       2016; TUFTS; **contested**: critics put it far lower, and it covers new chemical entities only)
├── manufacture
│   ├── key starting materials → intermediates → active pharmaceutical ingredient (API): fine chemicals, often made in China
│   │   and India; India's makers import about 70% of their API inputs from China (rough, IQVIA-linked reporting)
│   ├── formulation: API + excipients (lactose, starch, cellulose) → tablets, capsules; or sterile fill-finish for injectables
│   │   (glass vials, stoppers, syringes: a recurrent shortage)
│   └── quality systems (GMP), inspection, batch release
├── biologics instead: cell lines → bioreactors → purification → cold chain; the Pfizer-BioNTech COVID vaccine needed, by
│   Pfizer's account, about 280 materials and components from 86 suppliers in 19 countries (rough, company figure)
├── distribution: wholesalers (in the US three firms handle most volume: McKesson, Cencora, Cardinal; rough ≈ 90%),
│   pharmacy benefit managers, pharmacies, hospitals
└── payment: insurers, national health systems, patient co-payments; prices set by negotiation, not production cost
```

**Generics:** Indian firms supplied about 47% of all US generic prescriptions in 2022 (IQVIA, via IBEF/IPA). China's share of
finished API by volume for US drugs is small (about 8%, USP), but its share of key starting materials and of some whole classes
(older antibiotics) is very high (USP; estimates vary widely). **The fragility:** generics sell near cost, so makers cut to one or
two plants per molecule; one failed inspection or plant fire can cause a national shortage of a cheap essential drug (the
US cisplatin shortage of 2023 after one Indian plant halted, rough).

### 2.7 Concrete and a modern building

**The shape:** a heavy, local chain (aggregates and ready-mix cannot travel far by road), resting on a few global chains
(cement is regional, steel and glass are global, lifts and electrics are global assemblies); the building itself is a long
assembly of dozens of trades.

```
an office or apartment tower
├── concrete (concrete is the most used material after water, by volume, rough)
│   ├── cement (10 to 15% of concrete by mass, rough): limestone + clay or shale (quarry) → raw meal → rotary kiln at
│   │   ≈ 1,450 °C (coal, petcoke, gas, waste fuels) → clinker + gypsum → ground → cement
│   │   World ≈ 4.1 billion t (2023); China ≈ 2.0 to 2.2 billion t, about half (GC, statistics differ); cement CO2 ≈ 2.3 billion t,
│   │   ≈ 6 to 8% of global emissions (rough; half from the chemistry of limestone, half from fuel)
│   ├── aggregates: sand and gravel; the world uses about 50 billion t of sand and gravel a year, the most extracted solid
│   │   material (UNEP 2022); desert sand is too rounded; river and marine sand mining is contested and in places criminal
│   ├── water; admixtures (plasticisers, retarders: chemical industry); supplementary materials (fly ash from coal power,
│   │   slag from blast furnaces: joint products of other chains)
│   └── ready-mix plant → drum truck (must pour within about 90 minutes, rough) → pump → formwork (timber, steel, plywood)
├── reinforcement: rebar (EAF steel), post-tensioning strand
├── structural steel (§2.5), bolts, welding
├── envelope: float glass (Pilkington process, 1950s) ← silica sand + soda ash + limestone + gas; aluminium frames;
│   insulation (mineral wool, foam ← petrochemicals); sealants
├── services in the building: lifts (Otis, Schindler, KONE, TK), HVAC (compressors, refrigerants), electrical (copper cable,
│   switchgear, transformers), plumbing (copper, PVC), fire systems, data cabling, controls (chips again)
├── finishes: gypsum board (gypsum, or synthetic gypsum from power-plant scrubbers), tiles, paint, carpet, furniture
└── services to build it: land and planning permission, architects, structural, MEP and geotechnical engineers, quantity
    surveyors, a main contractor and many subcontractors, cranes, insurance, a construction loan, a mortgage market, building
    codes and inspectors, utilities hook-ups
```

Vaclav Smil's widely quoted comparison: China used more cement in 2011 to 2013 (about 6.6 billion t) than the United States did
in the whole twentieth century (about 4.5 billion t) (Smil, *Making the Modern World*, 2014; rough). **What makes buildings
different:** most of their chain is local and seasonal (aggregates, ready-mix, labour, permits), so construction ties the global
economy to land, credit and law: the mortgage, the planning permission and the building code are as much inputs as cement.

### 2.8 The seven chains compared

| Chain | Lead firm power | Main chokepoints | Typical shape | Where value is |
|---|---|---|---|---|
| car | OEM (producer-driven) | chips, batteries, magnets, harness labour | assembly; tiered network; increasing returns | brand, design, finance, after-sales |
| smartphone | brand (modular) | EUV, leading fabs, rare earths, gallium, quartz | assembly across most countries; smile curve | design, platform, chips |
| T-shirt | retailer (buyer-driven) | few; cotton land and water, trade rules | labour-intensive middle; substitutes | brand and retail |
| bread | retailer and miller | fertiliser (gas, potash), Black Sea wheat | old chain made industrial | retail and processing (≈ 85% of food dollar) |
| chicken | integrator (hierarchy) | two genetics firms; soy | vertical integration with captive growers | integrator, retail |
| steel | mills (market) | seaborne ore and coal | increasing returns; recycling substitute | volume, scale |
| drug | originator (relational) | APIs, sterile capacity, regulators | time capital, then commodity | patents, regulators, payers |
| building | developer and contractor | land, permission, credit; transformers | local assembly of global parts | land and finance |

## 3. Logistics

### 3.1 Containerisation

On 26 April 1956 Malcolm McLean, a North Carolina trucking entrepreneur, sent the converted tanker *Ideal X* from Newark to Houston
with 58 truck bodies on deck. Loading loose cargo on a medium cargo ship then cost $5.83 a ton; McLean's people put the cost of
loading the *Ideal X* at 15.8 cents a ton (Marc Levinson, *The Box*, 2006; LEV). The box itself was not the invention: the
system was. It needed:

| Element | What it took |
|---|---|
| a standard box | ISO standards for 20- and 40-foot boxes and corner fittings (1960s), after fights between firms and countries over sizes |
| cellular ships | ships built around stacks of boxes; McLean's Sea-Land; US military supply to Vietnam showed it at scale |
| new ports | gantry cranes, large flat yards, deep berths; the old docks (Manhattan, London's East End, Liverpool) died and new ones grew where land was (Port Newark-Elizabeth, Felixstowe, Rotterdam's Maasvlakte) |
| labour settlements | long fights with dockers' unions (the ILA, ILWU), buyouts and guaranteed incomes; dock employment fell to a fraction |
| intermodal links | the same box on ship, rail (double-stack trains in the US from 1984) and truck; deregulation of US rail and trucking (1980) |
| information | bills of lading, customs, tracking: later the electronic manifest |

**Effect:** Bernhofen, El-Sahli and Kneller estimate that containerisation raised trade between adopting rich countries by about
700% over 20 years, more than all the tariff cuts of the period (BEK 2016). Levinson's case is that the box made the second
unbundling possible: once moving a part across an ocean cost little and took a predictable time, a factory could depend on one.

### 3.2 Global shipping today

- **Volume:** about 12.3 billion tonnes of seaborne trade in 2023 and about 12.7 billion in 2024 (UNCTAD Review of Maritime
  Transport 2024 and 2025; UNCTAD). Sea carries the large majority of world trade by volume (commonly put at about 80%, rough).
- **Ships:** the largest container ships carry about 24,000 TEU (twenty-foot equivalent units) (rough); bulk carriers for ore up
  to 400,000 tonnes; tankers (VLCCs) about 2 million barrels each.
- **Concentration:** a handful of carriers (MSC, Maersk, CMA CGM, COSCO, Hapag-Lloyd, ONE, Evergreen) in a few alliances run most
  container capacity (rough: the top nine well over 80%). The largest container port is Shanghai, about 50 million TEU a year
  (rough).
- **Cost:** in normal years a container from China to Northern Europe has cost one to two thousand dollars, a few cents to a few
  dollars per item of consumer goods (rough); the 2021 peak of about $10,000 a box (DREWRY) showed what the system's slack had
  been worth.
- **Services around ships:** ship finance (Greek, Norwegian, Chinese leasing), marine insurance and P&I clubs (London), ship
  registries (Panama, Liberia, Marshall Islands: flags of convenience), classification societies, brokers (London's Baltic
  Exchange), shipbuilding (China, Korea, Japan build almost all large ships, rough).

### 3.3 Trucking, rail, air, warehouses

| Mode | Role | Numbers |
|---|---|---|
| **trucking** | most domestic freight in most countries; door to door | in the US trucks carry around 70% of freight tonnage (American Trucking Associations, rough) |
| **rail** | bulk (coal, grain, ore) and boxes over long land distance | North America double-stack; China-Europe rail as a small middle option between sea and air |
| **pipelines** | oil, gas, refined products, water | the cheapest way to move fluids over land |
| **air freight** | light, valuable, urgent: chips, phones, drugs, flowers, fresh fish, spare parts | about a third of world trade by value, under 1% by volume (IATA; ICAO 2014: 34.6% of value, 0.5% of volume) |
| **inland water** | barges on the Mississippi, Rhine, Yangtze | the Yangtze is the busiest inland waterway by tonnage (rough) |

**Warehousing and fulfilment:** the 20th-century warehouse stored; the 21st-century distribution centre flows. Walmart's
cross-docking and its own logistics (1980s, with satellite links and bar codes: the UPC, first scanned in 1974) set the
template; Amazon's fulfilment network (about 1.5 million employees in 2025, most in operations, and around a million robots)
carried it to the parcel (WSJ via RSF; GEEK). E-commerce is about a fifth of world retail sales (about 20% in 2024 by eMarketer's
estimate; others give 17 to 22%; EMK). **The shape:** increasing returns (the denser the network, the cheaper and faster each
parcel), which is why a few firms dominate, and a last mile that is the most expensive step per item.

### 3.4 Canals and straits as chokepoints

| Chokepoint | What passes | Disruptions |
|---|---|---|
| **Suez Canal** | 12 to 15% of world maritime trade before 2024 by most estimates (measures differ); over 20% of container trade (UNCTAD) | 1956 crisis; closed 1967 to 1975; Ever Given six days in 2021; Red Sea attacks from late 2023 (trade volume down about 50%, container traffic down far more; IMF, COFACE) |
| **Panama Canal** | about 5% of world trade by volume; locks fed by fresh water from Gatun Lake (rough: about 200 million litres per transit) | 2023 to 2024 drought: daily transits cut from about 36 to 38 to about 24 by November 2023, with deeper cuts planned for 2024; draft limits (GCAP, ME) |
| **Strait of Hormuz** | about 20 million barrels a day of oil in 2023 (over a quarter of seaborne oil trade, about a fifth of world liquids use) and much of the world's LNG (Qatar) (EIA) | tanker war 1984 to 1988; repeated threats; 2019 seizures |
| **Strait of Malacca** | about 23.7 million barrels a day of oil in 2023, the largest oil chokepoint; most East Asia-Europe trade (EIA) | piracy; congestion |
| **Bab el-Mandeb** | the Red Sea's southern gate to Suez | the 2023 to 2025 attacks |
| **Bosporus, Danish straits** | Black Sea grain and oil; Baltic trade | 2022 war in Ukraine: the Black Sea Grain Initiative (Jul 2022 to Jul 2023) |
| **Taiwan Strait** | a large share of world container traffic and the island's chip exports | the risk of blockade dominates strategic planning |

**The pattern:** each chokepoint is a place where geography forces many routes into one, and its value is set by the cost of the
alternative (round the Cape, adds 10 to 14 days Asia-Europe, rough; across the Andes and Isthmus by rail, much costlier).

## 4. Energy systems

### 4.1 Oil and gas

```
petrol, diesel, jet fuel, plastics, fertiliser
├── upstream: exploration (seismic, geology), drilling (rigs, steel pipe, drilling fluids, oilfield services: SLB,
│   Halliburton, Baker Hughes), production (Saudi Arabia, US shale, Russia, Iraq, UAE, Canada, Brazil);
│   world oil use ≈ 100 to 105 million barrels a day (rough); OPEC+ sets quotas
├── midstream: pipelines, tankers through §3.4's chokepoints, storage (Cushing, Rotterdam, Singapore)
├── refining: crude → distillation → cracking, reforming → fuels; joint products: every barrel gives a mix of petrol, diesel,
│   jet, fuel oil, naphtha, LPG, asphalt, coke; refiners choose crude and units to tilt the mix
├── petrochemicals: naphtha and ethane → ethylene, propylene, benzene → plastics (PE, PP, PVC, PET), synthetic fibres,
│   rubber, solvents, detergents
└── gas: wells → processing (joint products: ethane, propane, helium in some fields) → pipeline (Russia to Europe until 2022)
    or liquefaction → LNG tanker (US, Qatar, Australia the largest exporters) → regasification → power plants, industry,
    homes, ammonia (fertiliser: the Haber-Bosch link to food)
```

**The shape:** a commodity chain with a cartel at the top, a joint-product refinery in the middle, and chokepoints in transit.
Synthetic nitrogen fertiliser made from natural gas feeds roughly half of humanity (estimates from about 27% to "nearly half":
Erisman et al. 2008, Smil 1999, Our World in Data; OWID), which ties food to gas as firmly as transport is tied to oil. The 2022
cut of Russian pipeline gas to Europe raised European gas and power prices several-fold and closed fertiliser plants.

### 4.2 Power grids

A grid is the purest example of a coordination problem: supply must equal demand every second, across a whole synchronous area.

| Part | What it takes | Chokepoints and scale |
|---|---|---|
| generation | coal, gas, hydro, nuclear, wind, solar plants | fuels (§4.1), turbines (GE Vernova, Siemens Energy, Mitsubishi: a few makers of large gas turbines, with years-long order books) |
| transmission | high-voltage lines, towers, large power transformers, substations | large transformers are custom, made by few firms, and lead times stretched to two to four years in the 2020s (rough); grain-oriented electrical steel has few makers |
| distribution | local lines, distribution transformers, meters | copper and aluminium; utility crews |
| balancing | dispatch, reserves, storage, interconnectors, markets | grid operators; wholesale markets; capacity payments |
| demand | lights, motors, heat pumps, data centres, EV charging | AI data centres are a new, concentrated demand (rough: several per cent of US power by the late 2020s) |

**The social form:** grids began as private firms (Edison), became regulated monopolies or state utilities (one wire network per
place: a natural monopoly), and since the 1990s many have been split into competing generators, regulated wires and a market.

### 4.3 Nuclear

Uranium mining (Kazakhstan the largest producer, then Canada, Namibia, Australia) → milling to yellowcake → conversion to UF6 →
enrichment (Russia's Rosatom about 44% of world enrichment capacity in 2024; Urenco in UK, Netherlands, Germany, US; Orano in
France; China's CNNC) → fuel fabrication → reactor → spent fuel storage or reprocessing (POWERTECH; estimates 40 to 46%).
Reactors themselves rest on a very few forges for large pressure vessels (Japan Steel Works historically, rough), on
regulators, and on long-trained operators. **The shape:** time capital (a decade or more to build), long skill, and a chokepoint
at enrichment that survived the 2022 sanctions because the West had let its own capacity run down.

### 4.4 Renewables and batteries

```
solar panel
├── polysilicon ← metallurgical silicon ← quartz + coal or charcoal in arc furnaces (lots of power)
├── ingots and wafers ← high-purity quartz crucibles (Spruce Pine)
├── cells ← silver paste, dopants, glass, aluminium frames, EVA encapsulant, junction box (copper, plastics)
└── China holds over 80% of every manufacturing stage and over 95% of polysilicon and wafers (IEA 2022; IEA-PV)

lithium-ion battery
├── lithium: brine (Chile, Argentina) or spodumene rock (Australia); Australia ≈ 37%, Chile ≈ 20%, China ≈ 17% of 2024 mine
│   output (USGS via OWID); refined mostly in China
├── nickel: Indonesia ≈ 59% of 2024 mine output (from USGS MCS 2025 figures), much processed by Chinese-owned plants with
│   high-pressure acid leaching
├── cobalt: DRC ≈ 75% of mine output (USGS MCS 2025); China ≈ 80 to 88% of refining (IISD)
├── graphite (anodes): China over 90% of battery-grade output (IEA)
├── manganese, phosphate, copper foil, aluminium foil, electrolyte (lithium hexafluorophosphate), separators
├── cells: CATL, BYD, LG Energy Solution, Panasonic, SK On, Samsung SDI (China roughly three quarters of world cell capacity,
│   rough)
└── packs, battery management chips, thermal systems → cars, grid storage, phones
```

**The IEA's summary** (Global Critical Minerals Outlook 2025): China is the leading refiner for 19 of 20 energy-related minerals
analysed, with an average share of about 70%, and over 95% for battery-grade graphite and rare earths (IEA-CMO). Mining is spread
more widely than refining; **refining is the chokepoint**, because it needs cheap power, chemistry skill, tolerance of pollution
and years to build, and China built it while others did not.

## 5. Services and the knowledge economy

### 5.1 The shift of employment

| United States | Farming | Manufacturing | Services |
|---|---|---|---|
| 1900 | ≈ 41% of workforce (USDA ERS, Dimitri et al. 2005) | | |
| 1953 | | peak: 32% of non-farm jobs (BLS) | |
| 1979 | | 22% of non-farm jobs, peak headcount ≈ 19.5 million (BLS) | |
| 2000 | ≈ 1.9% of workforce (USDA ERS) | | |
| 2019 | | ≈ 9% of non-farm jobs (BLS) | ≈ 80% of jobs (rough) |

| World (ILO modelled) | Agriculture | Industry | Services |
|---|---|---|---|
| 1991 | 44% | 22% | 34% |
| 2019 | 27% | 22% | 51% |

(OWID and ILO.) This is the **three-sector pattern** of Allan Fisher and Colin Clark (1930s to 1940): as income rises, labour moves
from primary to secondary to tertiary work. Manufacturing output did not fall in rich countries; its employment fell because
productivity rose faster than demand, and some work moved abroad. William Baumol's **cost disease** explains the other half:
services such as teaching, nursing and live music cannot raise productivity as fast as factories, so their relative price rises
and they absorb a growing share of spending and work.

### 5.2 What the service economy is

| Service | What it does to the goods economy | Scale and structure |
|---|---|---|
| **finance** | moves money across time (credit, savings), space (payments, trade finance), and risk (insurance, derivatives); allocates capital to firms and chains | foreign exchange turnover about $9.6 trillion a day in April 2025 (BIS); a few clearing houses, card networks (Visa, Mastercard), messaging (SWIFT) are themselves chokepoints |
| **insurance** | lets firms take risks (ships, plants, crops, lives) by pooling them; reinsurance (Munich Re, Swiss Re) pools the pools | marine insurance and Lloyd's go back to the 17th century; modern supply chains carry business-interruption and contingent-supplier cover |
| **retail and wholesale** | the buyer-driven end of chains: decides what is made by deciding what is sold | Walmart (about 2.1 million employees, rough), Amazon, Costco, Carrefour, Tesco; retailers' data on what sells sets factory orders |
| **healthcare** | the largest employer in many rich countries | about 17% of US GDP (rough); long skill (doctors take 10+ years), licensing, huge public payers |
| **education** | produces the long skill every other sector needs | mass schooling (19th to 20th century), then mass higher education; credentials as signals |
| **software and platforms** | coordinates everything else; near-zero marginal cost; network effects | operating systems, app stores, search, marketplaces, cloud (AWS, Azure, Google Cloud: three firms most of the market, rough) |
| **business services** | law, accounting, consulting, advertising, logistics management, staffing, IT | the US professional and business services share of jobs reached a record 14% in 2017 (BLS) |
| **government** | law, courts, regulators, standards, defence, infrastructure | the frame every chain relies on: property, contract, standards, customs |

### 5.3 Platforms as a new chain shape

A platform (an app store, a marketplace, a ride-hailing service, a payment network) is a two-sided market: it is worth more to
each buyer the more sellers it has, and the reverse. It has **increasing returns of a social kind**: not cheaper per unit
produced, but more valuable per user joined. That gives one or two winners per market, a toll on every transaction through it
(app stores typically took 15 to 30%), and power over the firms that sell through it. It is the modern form of the miller's share
in economy_web.md §2.15: a rent for shared capital, here a network rather than a mill.

### 5.4 The urban service economy

Most people in rich countries now live in cities and work in services; over half the world is urban (rough, UN). The 21st-century
city runs on chains it does not see: food from a few distribution centres (a big city holds only a few days of food, rough), power
from a grid, water and sewage from public works, parcels from a fulfilment network, and the knowledge work of the people in it
from the software and finance of a few firms. Economists from Alfred Marshall to Edward Glaeser explain why: cities share
infrastructure, match workers to jobs, and let ideas spread (**agglomeration**). The urban economy is an extreme of both
specialisation (almost no one makes anything they use) and dependence (almost everything comes through a chain someone else
runs).

## 6. Chokepoints and interdependence today

### 6.1 Semiconductors: the deepest tree with the narrowest nodes

The SIA and BCG (2021) counted more than 50 points in the chip value chain where one region holds over 65% of global share, and
found that all of the world's leading-edge logic capacity (below 10 nm) was in Taiwan (92%) and South Korea (8%) (SIA-BCG 2021;
the "more than 50 points" is from the same report, rough as quoted). A chip may cross many borders, often quoted as 70 or more, as
it moves from wafer to fab to test to device (rough).

| Node | Holder | Why there is no quick substitute |
|---|---|---|
| EUV lithography | ASML (Netherlands), sole maker | decades of R&D; Zeiss optics (sole); a light source that hits tin droplets with a laser tens of thousands of times a second; machines cost about €150 million to over €350 million (High-NA) and come from about 5,100 suppliers (ASML annual report via LS; CNBC) |
| leading-edge foundry | TSMC (Taiwan) | yield learning; customers' designs tied to its process; a fab costs $20 billion or more (rough) |
| EDA software | Synopsys, Cadence (US), Siemens EDA | decades of tools and libraries; designers trained on them |
| instruction-set IP | Arm (UK, Japanese-owned) | ecosystem of software and designers |
| photoresists, wafers | JSR, TOK, Shin-Etsu, SUMCO (Japan) | process chemistry and purity know-how |
| high-purity quartz | Spruce Pine, North Carolina: two firms, about 70 to 90% of high-purity quartz (TT, BNEF via BNN) | geology; Hurricane Helene shut both mines for about two weeks in Sep to Oct 2024 |
| semiconductor-grade neon | Ukraine (Ingas, Cryoin) about 45 to 54% before 2022 (Reuters via CNBC) | by-product of steel-plant air separation; the industry had stock and others ramped up |
| gallium, germanium | China (about 98% of primary gallium, rough) | China licensed exports from Aug 2023 and banned some to the US from Dec 2024 (rough) |

**Export controls:** since 2019 the Netherlands has not licensed EUV tools to China, and from 2022 the US controlled exports of
advanced chips and chip-making tools; China answered with controls on gallium, germanium, graphite and rare earths. The
chokepoint became an instrument of state power, which is Henry Farrell and Abraham Newman's argument in *Underground Empire*
(2023): states that sit on network hubs (the dollar, SWIFT, chip tools) can "weaponise interdependence".

### 6.2 Rare earths

| Stage | China's share | Notes |
|---|---|---|
| mining | about 60 to 70% (rough; other sources: US Mountain Pass, Myanmar, Australia) | Myanmar's mines supply heavy rare earths, often unregulated |
| separation and refining | about 90% (91% of magnet rare earths in 2024, IEA) | hundreds of solvent-extraction stages; chemistry skill; acid waste |
| magnets (NdFeB) | about 90% (rough) | needed for EV motors, wind turbines, phones, missiles |

The April 2025 licensing of seven medium and heavy rare earths and their magnets halved magnet exports within a month and stopped
some car lines in Europe, the US and India (SMM; ENGNEWS). It showed that a chokepoint can be used as a dial (slow licences)
rather than a switch.

### 6.3 Why specialisation raises both wealth and fragility

Shipping lanes (§3.4), critical minerals (§4.4), chips and rare earths are one pattern at different scales: a few places or
firms where many chains converge, with a substitute that costs much more or takes years.

| Mechanism | Wealth | Fragility |
|---|---|---|
| **scale economies** (one huge fab, one huge port) | lower unit cost | one site carries a large share of the world |
| **learning by doing** (TSMC's yields, Spruce Pine's processing) | quality others cannot match | no second source can be made quickly |
| **lean inventory** (JIT) | less capital tied up in stock | no buffer when a supplier stops |
| **long trees** (more tiers, more countries) | each step where it is best | the lead firm cannot see its tier 3; a shock anywhere propagates |
| **network hubs** (canals, clearing, platforms) | lower transaction costs | a single blockage or a hostile owner can stop the whole |
| **geographic clustering** (Shenzhen, Silicon Valley, Taiwan's Hsinchu) | shared suppliers, skills, ideas | one earthquake, storm or blockade hits the cluster |

The trade-off has a name in operations research (efficiency against resilience) and was the theme of supply-chain policy
everywhere after 2021: the US CHIPS Act (2022) and Inflation Reduction Act (2022), the EU Chips Act and Critical Raw Materials
Act, Japan's subsidies for TSMC's Kumamoto fab. These pay a premium for redundancy that markets did not buy.

## 7. Dependency trees: how many sectors a modern good draws on

### 7.1 The classic illustrations

- **"I, Pencil"** (Leonard Read, 1958): no single person knows how to make a pencil. Cedar from Oregon, graphite from Sri Lanka,
  wax from Mexico, rubber from Indonesia, brass ferrule, lacquer, glue, rail, sawmills, power: thousands of people cooperating
  with no one in charge. The point is the price system as coordination.
- **The Toaster Project** (Thomas Thwaites, 2009 to 2010): an attempt to build a cheap toaster from raw materials. It had about
  400 parts (rough); he smelted iron in a microwave, made plastic from potato starch, and spent months and over a thousand pounds
  for a toaster that worked for a few seconds (rough). The gap between his toaster and the shop's is the value of the tree.
- **Economic complexity** (César Hidalgo and Ricardo Hausmann, *The Atlas of Economic Complexity*, 2011): a country's wealth tracks
  the number and rarity of products it can make, because each product needs a set of capabilities, and countries with many
  capabilities can combine them into many products.

### 7.2 A generic dependency tree of the modern economy

```
FINAL GOODS AND SERVICES
  car · phone · shirt · loaf · chicken · drug · building · flight · hospital stay · bank account · app
        ▲
ASSEMBLIES AND SYSTEMS
  engines · battery packs · chips · displays · garments · baked goods · processed meat · formulated drugs · structures
        ▲
INTERMEDIATES (the hubs: each feeds many goods)
  steel · aluminium · copper wire · cement · glass · plastics · synthetic fibre · yarn and fabric · flour · feed
  · ammonia and fertiliser · sulphuric acid · chlorine and caustic soda · industrial gases (O2, N2, Ar, Ne, He)
  · silicon wafers · refined lithium, nickel, cobalt · rare-earth oxides and magnets · API · electricity · diesel · paper
        ▲
PRIMARY
  iron ore · bauxite · copper ore · limestone · sand and gravel · crude oil · natural gas · coal · uranium
  · phosphate · potash · salt · quartz · rare-earth ore · lithium brine/rock · cobalt-copper ore · wood · cotton · wheat
  · maize · soy · water · land
        ▲
CAPITAL GOODS AND SERVICES UNDER EVERY LAYER
  machine tools · cranes · ships · trucks · rail · ports · pipelines · grids · telecoms · software · finance · insurance
  · law and courts · standards · education · research · regulators · customs
```

### 7.3 How many sectors each good draws on

Input-output tables (Wassily Leontief's method, 1930s on) measure this directly: the total requirement of each sector for a unit of
final demand from another. In a detailed table (the US uses about 400 industries) the total requirements for almost any
manufactured good draw on almost every industry, however little. The counts below are a reading of the trees in §2, not a
measurement, and are **(rough)**:

| Good | Distinct industries or sectors touched (rough) | Countries typically involved (rough) | Deepest tier (rough) |
|---|---|---|---|
| T-shirt | 30 to 50 (farming, chemicals, machinery, energy, textiles, logistics, retail) | 4 to 8 | 5 to 6 |
| loaf of bread | 40 to 60 (seed, fertiliser, gas, machinery, fuel, milling, packaging, refrigeration, retail, finance) | 2 to 10 | 6 |
| chicken | 50 to 70 | 3 to 10 | 6 to 7 |
| steel beam | 30 to 50 | 3 to 6 | 4 to 5 |
| drug | 80 to 150 (chemistry, biology, glass, plastics, clinical services, regulation, distribution) | 5 to 20 | 7 to 10 |
| car | 150 to 300 | 20 to 40 | 8 to 10 |
| smartphone | 200 to 400 | 30 to 50 | 10 or more (the EUV tool is itself a tree of 5,000 suppliers) |
| office tower | 100 to 200 | 10 to 40 | 8 |

**Hubs:** a few intermediates appear in almost every tree: electricity, diesel and shipping, steel, plastics, chips, industrial
gases, sulphuric acid, and finance. A failure at a hub is felt everywhere at once (the 2022 gas shock in Europe; the 2021 chip
shortage reaching washing machines and toothbrushes).

### 7.4 How the industries merged

Through the century the separate chains grew into one web:

| Merger | What joined | Why |
|---|---|---|
| **food with oil and gas** | Haber-Bosch fertiliser, diesel machinery, plastic packaging, refrigeration | the green revolution and the supermarket (1950s to 1970s) |
| **cars with chips and batteries** | the car became a computer on wheels; the EV a battery with a car around it | electronics (1970s on), then electrification (2010s) |
| **steel and cement with energy and climate** | the largest industrial CO2 sources; green steel needs hydrogen and power | 2010s decarbonisation |
| **retail with logistics and software** | Walmart's data, Amazon's network; the store became a node in a chain | bar codes, then the internet |
| **finance with everything** | supply-chain finance, commodity futures, leasing, insurance; global firms owned by global funds | deregulation of the 1980s; the dollar system |
| **energy with minerals** | renewables and batteries made energy a materials industry (lithium, nickel, copper, silver, polysilicon) | the 2010s to 2020s energy transition |
| **everything with data** | chips and software in every good; cloud and AI as a new hub that draws power, chips and water | 2000s on |

## 8. What a simulator could take from this

Not a build list. The point is what makes a modern economy *work as an economy*, so a designer can choose which of its forms to
bring into a world, and why.

**Shapes this part adds to the economy_web.md vocabulary:**

1. **Tiered assembly.** A good made from many sub-assemblies, each made by others from parts made by others. The scarcest input
   limits the whole, and the assembler often cannot see the deepest tier. A world could hold goods two or three tiers deep where
   each tier is a different household or village, so the deepest dependency is invisible to the user at the top until it fails.
2. **Ownership switch: integrate or buy.** Ford owned the chain; Toyota coordinated a network of trusted suppliers; Apple owns
   design and brand and buys everything else. The same chain can be held in any of Gereffi's five governance forms, and which one
   people choose depends on how hard the part is to specify, how capable suppliers are, and how much they trust them. That is a
   choice agents could face: build your own smithy, sign a standing agreement with a smith, or buy at market each time.
3. **Just in time against just in case.** Stock is insurance; carrying less is cheaper until a supplier fails. A world with
   storage costs (spoilage, space, capital tied up) and supplier failures (illness, a flood, a quarrel) makes this a real
   decision, and the first disruption teaches it.
4. **The smile curve.** Where value is captured depends on what is scarce and hard to copy: design, brand, the market place, the
   platform, the patent. Assembly is easy to move and earns little. A simulated economy that values only material inputs and
   labour time will miss this; one that lets agents hold rights (a mark, a method, a market day, a list of customers) can show it.
5. **The hub intermediate.** A few goods (steel, power, fuel, chips, finance) feed nearly every chain. In the medieval web the
   hubs are withies, leather, cord, charcoal and metal edges (economy_web.md §3); the modern lesson is that hubs multiply and a
   failure at one is felt everywhere at once.
6. **The concentrated chokepoint built by learning, not geography.** Spruce Pine and Hormuz are geography; ASML and TSMC are
   accumulated skill, which no one can buy or seize quickly. A world could have both kinds: a single ore seam, and a single
   master whose skill took years to reach and whose apprentices are the only second source.
7. **The chokepoint as a dial.** China's 2025 licensing did not cut supply; it slowed it and chose who got it. A holder of a
   chokepoint in a world could ration, license, toll or delay, not only refuse.
8. **Time capital with a cliff.** A drug costs a decade and billions, earns monopoly rents for the life of a patent, then becomes a
   commodity made by the cheapest maker. Any rule that grants a temporary monopoly to an innovation (a guild privilege, a royal
   licence, a patent) creates this shape.
9. **Network increasing returns.** Containers, ports, parcel networks and platforms get cheaper or more valuable with more users,
   so one or two win, and they collect a toll. The mill and the oven are the village version; the market town is the regional one.
10. **Joint products and by-product chains.** Slag to cement, fly ash to concrete, cottonseed to oil, offal to feed, refinery
    cuts, coke-oven gas, neon from steel plants. Many modern chokepoints (neon, helium, gallium) are by-products of other
    industries, so their supply does not respond to their own price.

**Mechanisms worth modelling, at any scale:**

- **Transport cost as the master variable.** The container cut loading costs about 97% and trade between adopters rose about
  sevenfold over twenty years. In a world of places and roads, the cost and reliability of moving goods decides how far
  specialisation can go (Smith's extent of the market). Lowering it should, by itself, produce specialisation, concentration and
  new dependencies.
- **Standards as public goods.** The box worked because its size and fittings were standard; the bar code, the ISO norm, weights
  and measures and the coin do the same. A standard is an institution that someone has to set and others have to accept.
- **Visible and invisible tiers.** Toyota did not know its tier 3 suppliers until 2011. Information about who depends on whom is
  itself a good that is costly to gather (the senses guide's rule: signs grounded in state, worth acting on).
- **Shock propagation.** A failure at one node travels down the tree at the speed of stock running out: hours for JIT, weeks for
  normal stock, months for strategic reserves. A world where stocks are visible lets agents see a shortage coming.
- **Labour moving between sectors.** As farming gets more productive, fewer people are needed to feed everyone, and the rest move
  to making things, then to services. In a world, the share of households that grow food is a readable measure of how far an
  economy has grown, read against a null arm (scenario_design.md).
- **Services as goods.** Finance, insurance, carrying, teaching, healing and judging are what most people in a modern economy do.
  Each has a medieval form (the moneylender, the mutual guild, the carrier, the master, the healer, the court) that a world could
  hold as acts done for others for pay.
- **State power over hubs.** Export controls, sanctions, tolls on straits and canals, and subsidies for second sources show that
  once an economy has chokepoints, institutions grow up to use and defend them. That is a route by which economic structure
  produces politics, which is what a society simulator is for.

**Scale cautions for a reading of runs:**

- Real modern chains have hundreds of firms per good; a world's chain will have a handful of steps. The shapes (tiers, hubs,
  chokepoints, governance forms) carry over at small scale; the numbers do not.
- Most of the modern economy's growth came from productivity gains spread over decades (Fordism, lean, containers); a world that
  runs for a few seasons will show the structure, not the growth.
- Fragility shows only under shocks. A world without floods, illness, quarrels or blockages will make specialisation look free.

## Sources

Tags used in the text, with the pages consulted (accessed Nov 2026). Books are cited by author and title in the text.

- **AM**: Assembly Magazine, "The moving assembly line turns 100": https://www.assemblymag.com/articles/91581-the-moving-assembly-line-turns-100 ; Design World, "Ford launches moving assembly line": https://www.designworldonline.com/today-in-engineering-history-ford-launches-moving-assembly-line/
- **BRIT, CLUI**: Britannica, Henry Ford: https://www.britannica.com/money/Henry-Ford/Control-of-the-company ; CLUI, River Rouge Plant: https://clui.org/ludb/site/river-rouge-plant ; Assembly Magazine, The Rouge: https://assemblymag.com/articles/83966-special-section-the-rouge-an-industrial-icon
- **MIT IMVP, TST**: The Systems Thinker on Womack, Jones and Roos: https://thesystemsthinker.com/?p=4790 ; MacDuffie and Pil chapter: https://faculty.wharton.upenn.edu/wp-content/uploads/2012/05/MacDuffiePil_LeanWork_Chap9.pdf
- **WIKI-AISIN**, Nishiguchi and Beaudet: https://en.wikipedia.org/wiki/1997_Aisin_fire ; https://sloanreview.mit.edu/article/the-toyota-group-and-the-aisin-fire ; https://dspace.mit.edu/handle/1721.1/1457
- **WDR 2020**: World Bank, World Development Report 2020: https://worldbank.org/en/publication/wdr2020
- **GHS 2005**: Gereffi, Humphrey, Sturgeon, "The governance of global value chains", RIPE 12(1): https://www.soc.duke.edu/sloan_2004/Papers/governance_of_gvcs_final.pdf
- **KLD**: Kraemer, Linden, Dedrick, "Capturing Value in Global Networks" (2011): https://monthlyreview.org/wp-content/uploads/2015/07/10.1.1.466.3897.pdf ; CACM summary: https://cacmb4.acm.org/news/144802-analyzing-apple-products
- **CP**: Counterpoint Research, iPhone 15 Pro Max BoM: https://counterpointresearch.com/cn/insights/bom-analysis-iphone-15-pro-max-costs-37-7
- **TTAC, IEEE**: The Truth About Cars on Renesas (2011): https://www.thetruthaboutcars.com/2011/03/parts-paralysis-a-shuttered-chip-plant-could-cost-up-to-11-million-cars-worldwide/ ; IEEE Spectrum: https://spectrum.ieee.org/how-japanese-chipmaker-renesas-recovered-from-the-earthquake
- **ALIX**: CNBC on AlixPartners (Sep 2021): https://www.cnbc.com/2021/09/23/chip-shortage-expected-to-cost-auto-industry-210-billion-in-2021.html
- **DREWRY**: Drewry WCI reports via Hellenic Shipping News: https://www.hellenicshippingnews.com/?p=889555
- **LL**: Suez blockage estimates: https://porteconomicsmanagement.org/suez-canal-blockage-2021/ ; https://www.tbsnews.net/world/global-economy/suez-blockage-holding-96-billion-goods-day-222343
- **IMF, COFACE**: IMF blog, "Red Sea Attacks Disrupt Global Trade" (Mar 2024): https://www.imf.org/en/Blogs/Articles/2024/03/07/Red-Sea-Attacks-Disrupt-Global-Trade ; Coface: https://www.coface.com/news-economy-and-insights/houthi-attacks-in-the-red-sea-why-maritime-trade-is-still-not-smooth-sailing ; UNCTAD via Free Malaysia Today: https://www.freemalaysiatoday.com/category/business/2024/01/26/un-reports-42-drop-in-suez-traffic-following-houthi-attacks
- **SMM, ENGNEWS**: SMM on rare-earth controls: https://news.metal.com/newscontent/103361822/ ; Creamer Media: https://newsletter.en.creamermedia.com/article/chinas-rare-earth-export-curbs-hit-the-auto-industry-worldwide-2025-06-05 ; NAM: https://nam.org/china-suspends-critical-minerals-exports/
- **CHI-FED, YOLE**: Chicago Fed Letter 473: https://www.chicagofed.org/publications/chicago-fed-letter/2022/473 ; Yole: https://www.yolegroup.com/press-release/automotive-semiconductor-a-100-billion-device-industry-in-2028/
- **IEA 2021**: IEA, The Role of Critical Minerals in Clean Energy Transitions (2021), from memory of the report's headline figure (rough).
- **IEA-CMO, IEA**: IEA Global Critical Minerals Outlook 2024 executive summary: https://www.iea.org/reports/global-critical-minerals-outlook-2024/executive-summary ; 2025 coverage: https://www.engineeringnews.co.za/article/lack-of-geographic-diversification-in-critical-minerals-supply-a-cause-for-concern-iea-report-shows-2025-05-21
- **IEA-PV**: IEA, Solar PV Global Supply Chains (2022): https://www.iea.org/reports/solar-pv-global-supply-chains/executive-summary
- **USGS, IISD, OWID-MIN**: USGS MCS 2025 nickel: https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-nickel.pdf ; lithium: https://pubs.usgs.gov/periodicals/mcs2025/mcs2025-lithium.pdf ; USGS Congo page: https://www.usgs.gov/centers/national-minerals-information-center/congo-kinshasa ; IISD cobalt profile: https://www.iisd.org/system/files/2026-05/commodity-profile-cobalt.pdf ; OWID minerals: https://ourworldindata.org/explore-updated-data-on-metals-and-minerals
- **LS, CNBC (ASML)**: https://lightsource.ai/blog/asml-vs-china-chip-equipment-supply-chains ; https://www.cnbc.com/2022/03/23/inside-asml-the-company-advanced-chipmakers-use-for-euv-lithography.html
- **SIA-BCG 2021**: https://www.semiconductors.org/wp-content/uploads/2021/05/BCG-x-SIA-Strengthening-the-Global-Semiconductor-Value-Chain-April-2021_1.pdf ; 2024 update: https://www.semiconductors.org/wp-content/uploads/2024/05/Emerging-Resilience-in-the-Semiconductor-Supply-Chain_SIA-Summary.pdf
- **TT, BNN (quartz)**: https://www.techtarget.com/whatis/feature/How-Hurricane-Helene-may-cause-semiconductor-chip-shortages ; https://bnnbloomberg.ca/investing/commodities/2024/10/02/hurricane-helene-halts-quartz-mines-vital-for-chipmaking-and-solar
- **Neon**: CNBC (Reuters figures): https://www.cnbc.com/2022/03/25/russia-ukraine-war-laser-neon-shortage-threatens-semiconductor-industry.html ; USITC: https://www.usitc.gov/publications/332/executive_briefings/ebot_decarlo_goodman_ukraine_neon_and_semiconductors.pdf
- **LEV**: Levinson, *The Box*, figures via https://www.theobjectivestandard.com/p/marc-levinson and https://marclevinson.net/McLean%20Smithsonian%20061617.pdf
- **BEK 2016**: Bernhofen, El-Sahli, Kneller, "Estimating the effects of the container revolution on world trade", J. Int. Econ. 98: https://www.nottingham.ac.uk/gep/documents/papers/2013/2013-02.pdf
- **UNCTAD**: Review of Maritime Transport 2024: https://unctad.org/publication/review-maritime-transport-2024 ; UNCTADstat: https://unctadstat.unctad.org/insights/theme/244
- **IATA, ICAO**: https://www.iata.org/en/iata-repository/publications/economic-reports/value-of-air-cargo-air-transport-and-global-value-chains-summary ; https://icao.int/sustainability/economic-policy/Pages/Facts-and-Figures.aspx
- **EIA**: World Oil Transit Chokepoints: https://www.eia.gov/international/content/analysis/special_topics/World_Oil_Transit_Chokepoints/wotc.pdf
- **GCAP, ME (Panama)**: https://gcaptain.com/severe-drought-forces-panama-canal-to-restrict-number-of-daily-vessel-transits ; https://maritime-executive.com/article/panama-canal-plans-to-cut-transits-by-40-due-to-ongoing-drought ; https://www.cnbc.com/amp/2023/11/03/panama-canal-drought-hits-new-crisis-level-amid-severe-el-nino.html
- **RSF, GEEK, EMK**: Amazon workforce: https://redstagfulfillment.com/how-many-people-work-for-amazon/ ; robots: https://www.geekwire.com/2025/amazons-robot-workforce-hits-1-million-heres-what-they-all-do/ ; eMarketer: https://emarketer.com/content/worldwide-ecommerce-sales-break-6-trillion
- **WSA, WSA-RM**: worldsteel 2024 production: https://worldsteel.org/?p=61045 ; https://recyclinginternational.com/commodities/slight-fall-in-2024-steel-production/59613 ; raw materials fact sheet: https://steel.org.au/getattachment/458fa31b-2586-47bb-a645-9411140863dd/WSA_fact_raw_materials_2018.pdf
- **GC (cement)**: https://www.globalcement.com/news/17836-update-on-china-april-2024 ; https://statista.com/statistics/1285624/china-share-of-global-cement-production
- **UNEP 2022**: Sand and Sustainability: https://www.unep.org/news-and-stories/press-release/our-use-sand-brings-us-against-wall-says-unep-report
- **ERS (food dollar)**: https://www.ers.usda.gov/data-products/food-dollar-series/quick-facts ; https://www.ers.usda.gov/amber-waves/2023/december/ers-food-dollar-s-three-series-show-distributions-of-u-s-food-production-costs
- **NCC, FS (chicken)**: National Chicken Council, "1925 to Present": https://www.nationalchickencouncil.org/?p=7546 ; Feed Strategy: https://www.feedstrategy.com/poultry/how-poultry-performance-has-improved-over-the-last-decade
- **OWID (fertiliser)**: https://ourworldindata.org/how-many-people-does-synthetic-fertilizer-feed ; Smil 1999, Nature: https://www.nature.com/articles/22672
- **RIV**: Rivoli, *The Travels of a T-Shirt*, via NPR: https://www.npr.org/transcripts/131450313 and https://wwwtest.midamericafreight.org/wp-content/uploads/2018/10/T-shirts.pdf
- **USDA cotton**: https://ers.usda.gov/sites/default/files/_laserfiche/outlooks/110593/CWS-24k.pdf ; Cotton Inc.: https://cottoninc.com/wp-content/uploads/2024/12/2024-12-Monthly-Economic-Letter.pdf
- **DT, WIKI-RANA**: Dhaka Tribune: https://www.dhakatribune.com/amp/business/283661/10-years-after-rana-plaza-changes-and-challenges ; https://www.wikipedia.org/wiki/Rana_Plaza
- **TUFTS**: https://www.policymed.com/?p=1225 ; critique: https://pharmexec.com/view/tufts-figures-drug-development-spark-debate
- **IQVIA, USP**: https://www.ibef.org/news/indian-pharmaceutical-firms-supplied-47-of-all-generic-prescriptions-in-us-in-2022 ; https://qualitymatters.usp.org/over-half-active-pharmaceutical-ingredients-api-prescription-medicines-us-come-india-and-european ; https://www.ipa-india.org/wp-content/uploads/2024/05/IQVIA-US-India-Medicine-Partnership.pdf
- **POWERTECH (enrichment)**: https://power-technology.com/newsletters/nuclear-fuel-costs-soar-as-conversion-and-enrichment-bottleneck-strains-supply ; Columbia CGEP: https://www.energypolicy.columbia.edu/research/commentary/reducing-russian-involvement-western-nuclear-power-markets
- **USDA ERS (farm labour)**: Dimitri, Effland, Conklin, EIB-3 (2005): https://primary.ers.usda.gov/webdocs/publications/44197/13566_eib3_1_.pdf
- **BLS**: "Forty years of falling manufacturing employment": https://www.bls.gov/opub/btn/volume-9/forty-years-of-falling-manufacturing-employment.htm ; professional and business services: https://www.bls.gov/opub/ted/2018/share-of-employment-in-professional-and-business-services-at-all-time-high-of-14-percent-in-2017.htm
- **OWID and ILO (sectors)**: https://ourworldindata.org/grapher/share-of-employment-in-agriculture ; https://posts.voronoiapp.com/other/The-Service-Sector-now-Represents-about-Half-of-Global-Employment-944
- **BIS**: Triennial Survey 2025: https://www.bis.org/press/p250930.htm

Standard works named in the text: Alfred Chandler, *The Visible Hand* (1977); Womack, Jones and Roos, *The Machine That Changed the
World* (1990); Taiichi Ohno, *Toyota Production System* (1978, English 1988); Gary Gereffi, "The organization of buyer-driven
global commodity chains" (1994); Marc Levinson, *The Box* (2006); Pietra Rivoli, *The Travels of a T-Shirt in the Global
Economy* (2005); Richard Baldwin, *The Great Convergence* (2016); Vaclav Smil, *Making the Modern World* (2014) and *Enriching
the Earth* (2001); Leonard Read, "I, Pencil" (1958); Thomas Thwaites, *The Toaster Project* (2011); Hidalgo and Hausmann, *The
Atlas of Economic Complexity* (2011); Henry Farrell and Abraham Newman, *Underground Empire* (2023); Chris Miller, *Chip War*
(2022); Colin Clark, *The Conditions of Economic Progress* (1940); William Baumol on cost disease (1967); Clayton Christensen,
*The Innovator's Dilemma* (1997); Edward Glaeser, *Triumph of the City* (2011).

In the project: `docs/cybertron2/proposals/economy_web.md` (chain shapes), `docs/review/37_growth/02zzi_economies_scaling.md`
(the sequence of societies, which stops at §3.8, the edge of mineral energy), `docs/scenario_design.md` (null arms).
