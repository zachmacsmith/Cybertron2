# 07: The industrial revolution as layers on the pre-industrial economy (15 Nov 2026)

Part of the 02zzj economy research folder (37.2). A research note, not a plan: what the industrial revolution was, industry by
industry, and how each industry was built on the ones before it. The frame and the words for the shapes of chains (shallow,
accretive, paradigm switch, substitutes, joint products, assembly, chokepoint, long skill, time capital, pulse, commons,
increasing returns) are those of `docs/review/37_growth/02zzi_economies_scaling.md` and `docs/cybertron2/proposals/economy_web.md`.

## Summary

The British industrial revolution (roughly 1760 to 1870, with roots back to 1700 and a second wave to 1914) was not one
invention. It was a handful of supply chains that had grown up separately in the organic economy (coal for London's hearths,
charcoal iron, wool and linen spun at home, water mills, carts and river boats) and that, over about a century, **fused into one
web**. Coal fed coke, coke fed iron, iron and coal fed the steam engine, the steam engine drained the coal mines and blew the
furnaces, iron rails and steam engines became the railway, and the railway carried coal. Beside this loop ran a second complex,
cotton: slave-grown fibre from the American South, shipped through Liverpool, spun and woven in Lancashire mills on machines
built by Manchester engineers, bleached and dyed with chemicals from Glasgow and Widnes, and sold back to the world, including to
India, whose hand spinners it displaced. The engineering workshops that built textile machinery went on to build locomotives and
machine tools; the chemical works that began by making bleach for linen and cotton went on to make soda for glass and soap, and
then dyes from the tar left by the gasworks. Every one of these steps needed something earlier: a fuel, a material, a skill pool,
a market, a road or a canal, a way to raise capital, a law.

E. A. Wrigley's summary is the one to keep: the revolution was the shift from an **organic economy**, in which almost all energy
and materials came from what grew on land each year, to a **mineral economy**, in which they came from stores laid down long ago
(coal, then iron ore and limestone on a vast scale). That broke the land ceiling that binds every economy the engine can model
today. The shift was slow: output per head grew only about 0.5% a year before 1830, steam mattered little to productivity until
after 1830, and wages stayed flat for decades while the towns grew sick. For a simulator the lesson is that each industrial layer
is a **paradigm switch with prerequisites**, usually several at once, and that the social forms (wage labour at scale, the
factory, the joint-stock company, the industrial town and its diseases) came with the technology rather than after it. Section 11
sets out which layers a simulator could represent, and what a world must hold before each could emerge.

**Marks used.** [R] a rough figure (an order of magnitude, a commonly cited estimate, or a figure that differs between sources);
[C] a contested figure or claim, with the dispute named. Figures without a mark are well established. British tons (long tons,
2,240 lb) unless said otherwise.

---

## 1. Energy: coal and steam

### 1.1 The organic ceiling

In an organic economy, heat comes from wood, charcoal, peat and straw; mechanical work comes from muscle (people, oxen, horses
fed on land), wind and falling water. Every one of these competes for the same land: an acre growing oats for horses is not
growing wheat for people or oak for charcoal. Wrigley's point is that this sets a hard ceiling. Growth by specialisation and trade
(Adam Smith's kind) could raise output per head, but not without limit, because every extra unit of energy or material needed
more land.

Wrigley's rule of thumb is that an acre of woodland, cut on a sustained rotation, yields fuel equal to about a ton of coal a year
[R]. On that reckoning, English coal output of about 15 million tons around 1800 did the heating work of something like 15 million
acres of woodland, a large fraction of England's 32 million acres, and by the 1850s the coal burnt each year was equal to more
woodland than the whole surface of Britain [R]. Coal let Britain grow without finding that land.

- **Coal came first as a heating fuel.** London burnt Newcastle "sea coal" from the sixteenth century because wood near the city
  ran short; collier ships, coal hearths, and coal in brewing, salt and soap boiling, brick, lime and glass all existed by 1700.
  The industrial uses were grafted onto an existing chain.
- **Coal is a substitute with trade-offs.** More heat per ton and per acre than wood, but its sulphur and smoke spoil iron, malt
  and glass. Much of its history is keeping the fumes off the product: covered glass pots, reverberatory furnaces (flame over the
  charge, fuel apart), coke instead of raw coal.
- **Coal is a chokepoint of geology.** Industries moved to the coalfields (the Black Country, Tyneside, South Wales, Lanarkshire,
  the West Riding, Lancashire).

### 1.2 Coal mining

| Year | British coal output | Notes |
|---|---|---|
| 1700 | about 3 million tons [R] | Flinn; some series give 4 million tonnes |
| 1750 | about 5 million | |
| 1800 | about 15 million [R] | Flinn 15; other series 17 million tonnes |
| 1830 | about 30 million [R] | Flinn and Church |
| 1850 | about 50 to 65 million [R] | estimates differ by source |
| 1870 | over 100 million | |
| 1900 | over 200 million | |
| 1913 | 287 million (292 million tonnes) | the all-time peak; about 1.1 million miners [R] |

**How it grew.** Not by machines at the face (pick-and-shovel work until the twentieth century; output per miner rose little [R])
but by more men, deeper pits, and better drainage, ventilation and haulage:
- **Water:** pits below the water table flooded; horse gins and wheels pumped shallow ones; the steam engine (1.3) was invented
  for this.
- **Air:** firedamp in deep pits; ventilation furnaces, then fans; the Davy and Stephenson safety lamps (1815).
- **Haulage:** coal pays only near water. Tyneside ran wooden wagonways to the river staithes from the early 1600s; Coalbrookdale
  laid cast-iron rails on them in 1767. The railway is a grown-up wagonway.
- **Labour:** families worked underground until the Mines Act of 1842 barred women and boys under ten.

**What coal fed.** Household heat (the largest use until late in the century [R]); salt, brewing, soap, lime, brick and glass;
then coke for iron (2), steam (1.3), gas (1.4), railways and steamships (5), and exports (about a third of output by 1913 [R]).

### 1.3 The steam engine

| Engine | Date, place | What it did | Fuel use (duty) | What it required |
|---|---|---|---|---|
| Savery's "fire engine" | patent 1698 | raised water by steam pressure and vacuum, no piston | very poor; burst at depth | brass and copper work, solder |
| **Newcomen atmospheric engine** | 1712, Coneygree colliery near Dudley Castle | a piston pulled down by vacuum under a cylinder of condensed steam, working a beam and a pump; about 5.5 horsepower [R] | about 4 to 6 million foot-pounds per bushel (94 lb) of coal [R] | a large cast brass (later cast iron) cylinder; a beam; a boiler of copper or iron plate; a mine needing drainage with **unsaleable small coal at the pithead to burn** |
| Smeaton's improved Newcomen | 1760s to 1770s | careful proportions and boring | about 9 to 10 million [R] | systematic testing |
| **Watt's separate condenser** | idea 1765, patent 1769; **Boulton & Watt** from 1775 (Soho, Birmingham) | steam condensed in a separate vessel, so the cylinder stays hot | about 20 to 30 million [R]: roughly a third to a quarter of Newcomen's coal for the same work | **John Wilkinson's cannon-boring mill (1774)** to bore the cylinder true; Matthew Boulton's capital and workshop; an Act of Parliament (1775) extending the patent to 1800 |
| Rotative Watt engines | sun-and-planet gear 1781; double acting 1782; parallel motion 1784; governor 1788 | turned a shaft, so could drive mills, not only pumps | as above | gear cutting, precision fitting |
| High-pressure engines | Trevithick from about 1799; Woolf compound about 1804 to 1814 | small, light engines with steam well above atmospheric pressure; the locomotive | Cornish engines rose to 60 to 100 million by the 1830s to 1840s [R] | **stronger boilers of wrought-iron plate**, better rivets; the end of Watt's patent in 1800 |

**Key dependencies.**
- The Newcomen engine was hugely wasteful, and still paid at **collieries**, because it burnt slack that could not be sold. In
  **Cornwall's copper and tin mines**, which had no coal and paid to ship it from South Wales, it was costly; so Cornwall was the
  first market for Watt, who charged a royalty of **a third of the fuel saved** against a Newcomen engine. Who buys a new technique
  first depends on the price of the input it saves.
- Watt's engine could not be built until boring could make a cylinder true to "the thickness of an old shilling" over a diameter of
  several feet [R]. Wilkinson's boring mill was a cannon-making machine. **Military demand made the machine tool that made the
  engine.**
- After Watt's patent lapsed (1800), Cornish mines published engine performance monthly in *Lean's Engine Reporter* (from 1811),
  and duty roughly tripled: Nuvolari's **collective invention**, driven by shared information, not patents [C: how far Watt's
  patent held progress back is disputed].

**Diffusion.** About 2,200 steam engines were built in Britain in the eighteenth century (Kanefsky and Robey; perhaps 2,400 to
2,500 in all), of which about 450 to 480 were Boulton & Watt engines, 268 of them rotative (Tann). Nicholas Crafts's summary of
installed power, from Kanefsky [R; Kitsikopoulos revises 1800 upward]:

| Year | Steam horsepower | Water horsepower |
|---|---|---|
| 1760 | about 5,000 | about 70,000 |
| 1800 | about 35,000 | about 120,000 |
| 1830 | about 165,000 | about 160,000 (parity) |
| 1870 | about 2,000,000 | about 230,000 |
| 1907 | about 9,700,000 | small |

Water did most early industrial work (Arkwright's mills were water mills). Crafts finds steam added a few hundredths of a point a
year to labour productivity growth before 1830, and roughly 0.3 to 0.4 points only in 1850 to 1870 [R]. **A general-purpose
technology takes decades to pay**: it needs cheap engines, people to build and mend them, cheap coal, and machines designed
around it.

### 1.4 Gas, coke and tar: coal's joint products

Heating coal in a closed retort gives three things at once: **gas**, **coke** and **tar** (with ammonia liquor). William Murdoch,
Boulton & Watt's engineer in Cornwall, lit his house with gas in 1792 and the Soho works in 1798; the Gas Light and Coke Company of
London was chartered in 1812, and most British towns had gas lighting by the 1830s [R]. Gas lighting let mills run long shifts in
winter. Coke went to the iron furnaces and later to household use. The tar was a waste for decades, then became the feedstock of
creosote, pitch for roads, naphtha (which Charles Macintosh used in 1823 to dissolve rubber for waterproof cloth), and, from 1856,
the synthetic dye industry (6.4). A textbook **joint product** whose by-products made later industries.

---

## 2. Iron and steel

### 2.1 The sequence

| Stage | Date, place, person | What changed | What it required | What it enabled |
|---|---|---|---|---|
| **Charcoal blast furnace and finery** | from the 1490s; the Weald, Forest of Dean, Shropshire | ore + charcoal + limestone in a furnace blown by water-powered bellows → pig iron; refined in a charcoal finery to bar iron under a water hammer | the coppice of thousands of acres per furnace [R]; ore, wood and water on one site; leather bellows | guns, pots, nails, tools; output capped by charcoal (about 25,000 tons a year about 1720 [R]); much bar iron imported from Sweden and Russia |
| **Coke smelting** | Abraham Darby I, Coalbrookdale, Shropshire, 1709 | coke (coal baked to drive off sulphur and tar) in place of charcoal | a coal that cokes well and low-sulphur ore (Coalbrookdale had both); a market for cast iron (Darby made thin-walled cast pots) | at first only foundry iron (coke pig made poor bar iron). Spread slowly: coke iron became cheaper than charcoal iron only from the 1750s, as charcoal grew dearer and furnaces bigger (Hyde). By 1788, 53 of 77 British furnaces used coke; by 1806, 162 of 173 |
| **Steam-blown furnaces** | 1776 onward (Wilkinson's Broseley blowing engine was among the first Boulton & Watt engines) | steam engines blew the furnaces and pumped water back over wheels | the Watt engine | furnaces off the river: sited on the coalfield, larger and running all year |
| **Puddling and rolling** | Henry Cort, patents 1783 to 1784 | pig iron stirred ("puddled") in a coal-fired reverberatory furnace into wrought iron, then passed through grooved rolls instead of under the hammer | the reverberatory furnace (from glass and lead smelting); steam rolling mills; **puddlers, a heavy long skill of judgement** | wrought iron from coal alone; the end of the finery; Merthyr Tydfil's ironworks (Cyfarthfa, Dowlais) became the world's largest |
| **Hot blast** | James Neilson, Glasgow, 1828 | air heated before it entered the furnace | iron pipes and stoves; Scotland's blackband ironstone (found by David Mushet, 1801) and raw splint coal | fuel per ton of pig cut by more than half [R]; Scottish pig iron rose roughly fifteen-fold between 1830 and the late 1840s [R] |
| **Crucible steel** | Benjamin Huntsman, Sheffield, about 1740 | blister steel melted in clay crucibles → uniform cast steel | Swedish bar iron (low phosphorus); coke; refractory clay; Sheffield's cutlers | cutlery, tools, springs, files; but in pots of tens of pounds, dear [R] |
| **Bessemer converter** | Henry Bessemer, 1856 (paper at Cheltenham); his own Sheffield works from 1858 | air blown through molten pig iron burns out carbon in about 20 minutes, with no fuel; tons per blow | low-phosphorus (haematite) pig iron, from Cumberland or Spain; Robert Mushet's addition of spiegeleisen (manganese) to fix the metal; Göransson's trials in Sweden | **cheap steel**: steel rails, plates, wire. The price of British Bessemer steel fell from about $80 a ton in 1873 to under $20 in 1886 [R]; steel rails fell from £10 to £18 a ton before 1875 to about £4 10s in 1886 |
| **Open hearth** | Siemens regenerative furnace (1856 to 1861); Pierre-Émile Martin, 1864 to 1865 | waste heat recycled through brick chequers to reach steelmaking temperature; slower than Bessemer, more controllable, takes scrap | gas producers; refractory brick; chemistry | ship plate and structural steel; overtook Bessemer by about 1900 [R] |
| **Basic process** | Sidney Gilchrist Thomas and Percy Gilchrist, 1878 to 1879 | a limestone or dolomite lining removes phosphorus | chemistry of slags | the phosphoric ores of Lorraine and Luxembourg became usable: **German and Belgian steel surged**; basic slag sold as fertiliser (a joint product) |

### 2.2 Output and the shift of leadership

| Year | British pig iron | British steel | Others |
|---|---|---|---|
| 1720 | about 25,000 tons [R] | small | |
| 1788 | about 68,000 [R] | small | |
| 1806 | about 250,000 [R] | small | |
| 1830 | about 680,000 [R] | small | |
| 1850 | about 2.25 to 2.5 million [R] | about 60,000 [R] | Britain made about half the world's pig iron [R] |
| 1870 | about 6 million [R] | about 0.3 million [R] | |
| 1913 | about 10 million [R] | about 7.7 million [R] | United States about 31 million tons of steel, Germany about 17 million [R] |

Britain was overtaken in steel by the United States about 1886 to 1890 and by Germany about 1893 [R]. The technologies Britain
invented spread to places with bigger markets, newer plant, and (after Thomas and Gilchrist) the ore to use them.

### 2.3 What iron fed

- **Engines and boilers** (1.3): cast-iron cylinders and beams, wrought-iron plate.
- **Rails** (5): cast-iron rails on wagonways from 1767; Birkinshaw's rolled wrought-iron rails (Bedlington, 1820) on the Stockton
  & Darlington; steel rails from the 1860s, lasting many times longer [R]. The railway manias took a large share of iron output [R].
- **Buildings and bridges**: Charles Bage's flax mill at Ditherington, Shrewsbury (1797), the first iron-framed building, built so
  textile mills would not burn; the Iron Bridge (Darby III, 1779); Telford's Menai bridge (1826); the Crystal Palace (1851).
- **Machines and ships**: textile machines moved from wood to iron frames (needing the workshops of section 4); iron hulls
  (Brunel's *Great Britain*, 1843), then steel.

**Shapes.** Iron is an **assembly** (ore, fuel, flux, blast, refractories, skill), a **chokepoint** (ore and coal in the same
place, or carried cheaply), a **long skill** (the furnace keeper, the puddler, the roller), **increasing returns** (bigger furnaces
use less fuel per ton) and a series of **paradigm switches** each with its own prerequisite (charcoal → coke needs a coking coal;
hammer → rolling needs steam; bar iron → Bessemer steel needs low-phosphorus ore; acid → basic needs slag chemistry).

---

## 3. Textiles

### 3.1 Before the factory

Wool was England's great industry in the organic economy: spun by women in their homes on the wheel, woven by men on handlooms,
fulled in water mills (the fulling mill is one of the first water-powered industrial uses, from the twelfth century), finished in
towns. The **putting-out system** (02zzi §3.6) organised it: a clothier or merchant owned the wool and the yarn, households owned
their wheels and looms and were paid by the piece. The industry was rural, part-time, and run on merchant credit. Cotton was a
small, new branch in Lancashire, usually woven with linen warps (fustians), protected from Indian calicoes by the Calico Acts
(1700, 1721; repealed 1774).

The bottleneck was **spinning**: one loom needed the yarn of several spinners [R: three to five is commonly cited, more after the
flying shuttle].

### 3.2 The inventions

| Invention | Date, place | What it did | Prerequisites |
|---|---|---|---|
| Flying shuttle | John Kay, Bury, 1733 | one weaver threw the shuttle across a wide loom alone; roughly doubled weaving speed [R] | a handloom; spread slowly, against weavers' resistance |
| Roller spinning | Lewis Paul and John Wyatt, Birmingham, 1738 | rollers drew out fibre; worked poorly | the idea that Arkwright made work |
| **Spinning jenny** | James Hargreaves, Stanhill, Lancashire, about 1764 to 1765; patent 1770 | one spinner worked 8, then 16 to 120 spindles; a hand machine for the cottage or workshop | a wooden frame a joiner could make; weft only (the thread too weak for warp) |
| **Water frame** | Richard Arkwright (with John Kay the clockmaker), patent 1769; **Cromford mill, Derbyshire, 1771**, with Jedediah Strutt and Samuel Need | rollers and flyers driven by water: strong yarn fit for warp, so all-cotton cloth | **a water wheel, a millwright, capital** (Strutt and Need were hosiers); a site on a fast stream; a labour force brought to the valley and housed (Cromford village) |
| **Mule** | Samuel Crompton, Bolton, 1779 | combined the jenny's moving carriage and the frame's rollers: fine, strong yarn able to match Indian muslins | not patented; worked by hand, then by water and steam for part of the cycle |
| Steam-driven mills | first Boulton & Watt rotative engine in a cotton mill, Papplewick, Nottinghamshire, 1785 | mills freed from streams: to towns, on coal | the rotative Watt engine |
| Power loom | Edmund Cartwright, 1785; made practical by Horrocks (Stockport, 1803), Roberts (1822) and others | weaving by power | iron-framed looms, dressing machines for the warp; came forty years after power spinning |
| **Self-acting mule** | Richard Roberts, Manchester, 1825 and 1830 | the whole spinning cycle automatic; one minder and piecers over a thousand or more spindles | the engineering workshop (4); commissioned by mill owners after a spinners' strike |
| Cotton gin | Eli Whitney, Georgia, 1793 | separated seed from short-staple upland cotton; one worker cleaned many times what he could by hand [R] | the demand of the British mills |

### 3.3 Productivity

The widely cited estimates from Harold Catling (*The Spinning Mule*, 1970) of operative hours to spin 100 lb of cotton
[R: estimates, but consistent across the literature]:

| Method | About | Hours per 100 lb |
|---|---|---|
| Indian hand spinner | before 1750 | 50,000 |
| Crompton's mule | 1780 | 2,000 |
| 100-spindle mule | 1790 | 1,000 |
| Power-assisted mule | 1795 | 300 |
| Roberts's self-acting mule | 1825 | 135 |
| Modern ring spinning | 1990 | 40 |

A fall of more than 300 times in about seventy years, most of it in the first twenty. Prices followed: C. Knick Harley's work on
yarn prices and profits shows yarn prices falling sharply by the 1780s, once Arkwright's patents were overturned (1785) and
competition spread, with no evidence of super-profits afterward.

**Scale.** British raw cotton imports [R: series differ]:

| Year | Million lb | Where from |
|---|---|---|
| 1760 | about 2.5 | West Indies, Levant |
| 1780 | about 5 | |
| 1787 | about 22 | West Indies, Brazil |
| 1790 | about 31 | Brazil about 40% of Liverpool imports in 1791 to 1801 |
| 1800 | about 50 to 55 | the United States becomes the largest supplier in 1799 to 1802 |
| 1815 | about 99 | |
| 1830 | about 200 to 260 | the United States over 70% from the late 1820s |
| 1840 | about 590 | |
| 1860 | about 1,400 | the United States about three-quarters or more [R] |

Cotton goods were about two-fifths to a half of British exports by value in the 1830s [R], and the cotton industry employed
several hundred thousand people in factories by mid-century [R].

### 3.4 The cotton chain from plantation to market

This is the clearest case of supply chains fusing across an ocean.

1. **Land and labour in the Americas.** Upland cotton spread across the American South once the gin made it cleanable: from about
   1.5 million lb in 1790 to about 2 billion lb in 1860 [R]. The enslaved population rose from about 700,000 to about 4 million
   over the same years, mostly by natural increase after the import trade was banned (1808); the internal slave trade moved perhaps
   a million people to the cotton states [R]. Cotton was the largest US export.
2. **Merchants and credit.** Factors in New Orleans, Mobile and Charleston advanced credit to planters, who borrowed on land and on
   enslaved people as collateral; London and Liverpool houses (Barings, Browns) financed the crop with bills of exchange.
3. **Shipping** to **Liverpool**, Britain's leading slave-trading port in the late eighteenth century (roughly half or more of the
   British trade [R]), which turned its docks, merchants and credit to cotton; its brokers' market set the world price.
4. **Carriage inland.** The Mersey and Irwell Navigation and the Bridgewater Canal, then the **Liverpool & Manchester Railway
   (1830)**, built to break the canal's hold on the 35-mile route.
5. **Spinning and weaving** in Manchester ("Cottonopolis") and its ring of towns (Oldham, Bolton, Preston, Stockport, Blackburn):
   McConnel & Kennedy and the Murrays in Ancoats (mule spinning from the 1790s); Greg's Quarry Bank Mill at Styal (1784), worked by
   pauper apprentice children; New Lanark (Dale and Arkwright, 1786; Robert Owen from 1800), about 2,000 workers [R].
6. **Finishing.** Bleaching, dyeing and calico printing works (Peel's in Lancashire, the Turkey-red dyers of the Vale of Leven), the
   customers of the chemical industry (6).
7. **Markets.** The Manchester Royal Exchange sold cloth to merchants for home sale and export: Europe, the Americas, and from the
   1820s to India, whose own industry had been the world's leading cotton producer. By the mid-nineteenth century India was
   importing British cloth and exporting raw cotton [C: the extent and causes of Indian deindustrialisation are debated].

**Shocks travel along the chain.** When the American Civil War cut cotton supplies (1861 to 1865), the "Lancashire cotton famine"
idled most of the county's mills [R]; Britain turned to Indian, Egyptian and Brazilian cotton, and Egyptian and Indian growers
borrowed heavily, then suffered when prices fell after 1865.

**Slavery and the revolution** [C]. Eric Williams (1944) argued slave-trade and plantation profits financed British industry;
critics (Engerman, O'Brien, Eltis) find those profits a small share of investment. Recent work (Inikori; Beckert, 2014; Berg and
Hudson, 2023) puts the link elsewhere: **cheap fibre from land worked by coerced labour**, Atlantic markets for British goods, and
the credit and shipping networks the slave economy built. At abolition in the colonies (1833) Britain paid £20 million to slave
owners, not to the enslaved, about two-fifths of a year's government spending [R].

### 3.5 From putting-out to the factory

| | Putting-out (about 1600 to 1800) | Factory (from 1771) |
|---|---|---|
| Who owns the tools | the household (wheel, loom) | the mill owner |
| Who owns the material | the merchant | the mill owner |
| Power | the household's hands | water, then steam |
| Where | in homes, in villages | one building; a town |
| Time | the household's own; work round the farm year | the bell and the clock: fixed hours, fines for lateness |
| Pay | by the piece | wages by time or piece; children paid less |
| Supervision | none; embezzlement of yarn was a constant complaint | overlookers |
| Capital | working capital (the stock of wool and yarn) | fixed capital (building, wheel or engine, machines) |

Powered machines could not be put out: they needed a wheel or engine, shafting and constant attention. Discipline and the end of
embezzlement also counted [C: Marglin against Landes on how much].

**The social change.** The switch did not end the hand trades at once: handloom weaving grew for decades on cheap machine yarn,
to perhaps a quarter of a million weavers about 1820, then collapsed as power looms rose (a few thousand in 1813, about 100,000 in
1833, about 250,000 in 1850 [R]) and piece rates fell by more than half [R]. Hence the Luddites (1811 to 1816) and factory reform.
Child labour was central to the early mills; the Factory Acts (1802, 1819; 1833, the first with paid inspectors) and the Ten Hours
Act (1847) were the response.

---

## 4. Machines and engineering

### 4.1 The engineering workshop and its lineage

Before about 1800, a machine was built on site by millwrights (carpenters and smiths who built wheels, gears and frames) and
clockmakers. The engineering workshop that made machines in iron, to drawings, with machine tools, grew out of a few shops whose
men trained one another:

- **Joseph Bramah** (London, lock patent 1784; hydraulic press 1795) employed **Henry Maudslay** to make lock machinery.
- **Maudslay** (own shop from 1797, Lambeth) built the screw-cutting lathe with slide rest and change gears (about 1800), true
  plane surfaces, and his bench micrometer. With **Marc Brunel** and Samuel Bentham he built the **Portsmouth Block Mills**
  (1803 to 1808): 45 machines making ship's pulley blocks, about 130,000 blocks in 1808; it was claimed that ten unskilled men did
  the work of 110 skilled blockmakers. The first mass production by machine tools.
- **Maudslay's shop trained** Richard Roberts (planing machine 1817; later the self-acting mule and locomotives), Joseph Clement
  (precision lathes; Babbage's difference engine), **James Nasmyth** (steam hammer 1839; Bridgewater Foundry at Patricroft, sited
  between the Bridgewater Canal and the Liverpool & Manchester Railway), **Joseph Whitworth** (standard screw threads 1841;
  measuring machines to very fine tolerances; Manchester), and others.

### 4.2 Textile machinery → locomotives → machine tools

The great Manchester engineering firms began as textile-machine makers, because the mills were their customers:

- **Sharp, Roberts & Co.** (Manchester, from 1820s; Atlas Works 1828) made textile machinery and machine tools, built its first
  locomotive, *Experiment*, for the Liverpool & Manchester in 1833, and became Sharp Stewart, which built thousands of locomotives
  before moving to Glasgow (1888) and merging into the North British Locomotive Company (1903). Its chief engineer Charles Beyer
  left to found **Beyer, Peacock** (Gorton, 1854), a leading exporter of locomotives.
- **Robert Stephenson & Co.** (Newcastle, 1823), the first purpose-built locomotive works, came from the colliery wagonway world:
  George Stephenson was a colliery enginewright. *Rocket* won the Rainhill trials in 1829.
- **Railway company works**: the London & North Western at **Crewe** (1843) and the Great Western at **Swindon** (1843) made whole
  towns around locomotive shops, with their own housing, schools and steelworks (Crewe made its own Bessemer steel from 1864).

The pattern Nathan Rosenberg called **technological convergence**: the same operations (turning, boring, planing, drilling,
milling to tolerances) serve many industries, so a machine-tool industry grows by serving one customer and then moves to others.
Textile machinery → locomotives → marine engines → machine tools for sale → arms, sewing machines, bicycles, cars.

### 4.3 Interchangeable parts: the American system

- French and American military armouries pursued uniform parts for muskets (Honoré Blanc in France, 1780s; the US Springfield and
  Harpers Ferry armouries from the 1810s). John Hall at Harpers Ferry made rifles with interchangeable parts by the late 1820s
  using jigs, fixtures and gauges; Thomas Blanchard's copying lathe (1818) turned gunstocks.
- Private makers (Colt; Robbins & Lawrence in Vermont) carried it into commerce. At the 1851 Great Exhibition the Americans
  surprised British observers; a British committee visited US armouries (1854) and the **Royal Small Arms Factory at Enfield**
  (1855 to 1857) was equipped with American machines.
- The method needed **gauges and a tolerance discipline**, special-purpose machines, a large uniform order (the army), and it cost
  more at first than hand fitting [C: David Hounshell shows full interchangeability was slow and costly until well after 1850].

### 4.4 Skills and their spread

- The key industrial skills were long skills held by people: millwrights, enginewrights, puddlers, mule spinners, pattern makers,
  fitters, turners. They spread by **apprenticeship and movement of men**, not by books.
- Britain prohibited the emigration of skilled artisans (until 1825) and the export of machinery (until 1843); both leaked
  (Samuel Slater carried the Arkwright system in his head to Rhode Island in 1789; Francis Cabot Lowell memorised power looms).
- Mokyr and Meisenzahl's study of several hundred British "tweakers" and "implementers" finds the revolution rested on a broad
  upper tail of skilled mechanics who improved others' inventions.

---

## 5. Transport

### 5.1 The sequence

| Layer | Dates | What it was | What it needed | Effect |
|---|---|---|---|---|
| **Turnpikes** | from 1663; most trusts 1750 to 1772; about 1,000 trusts and 20,000 miles by the 1830s | road trusts set up by private Acts of Parliament, borrowing on tolls to resurface roads | an Act for each trust; local landowners and merchants as trustees; toll collection; road engineering (Metcalf, Telford, McAdam) | freight rates fell about 20% on average where trusts ran (Bogart); travel times fell sharply; fast coaches and the mails |
| **River navigations** | 1600s to 1700s | dredging and locks on rivers | Acts; capital | bulk by water inland |
| **Canals** | **Bridgewater Canal 1761** (the Duke's Worsley coal mines to Manchester; engineer Brindley); Trent & Mersey 1777 (promoted by Wedgwood); the 1790s mania; about 4,000 miles by the 1830s [R] | still-water cuts with locks and aqueducts; horse boats of 20 to 30 tons [R] | bulk to carry; an Act; statutory company shares; surveyors; navvies | **Manchester's coal price halved** within a year; Wedgwood's pottery reached ports unbroken |
| **Railways** | Stockton & Darlington 1825 (a coal line); **Liverpool & Manchester 1830** (the first intercity, steam-only, timetabled line); about 1,500 miles by 1840, 6,000 by 1849, 15,000 by 1870, 20,000 about 1914 [R] | iron rails on graded track; locomotives; signals | **wrought-iron rails**; high-pressure engines; engineering workshops; joint-stock capital on a new scale (the 1845 to 1847 mania several percent of GDP a year [R]; cumulative investment about 60% of GDP by 1913 [R]); private Acts with compulsory purchase; navvies (about 250,000 in 1847 [R]) | real freight charges per ton-mile in 1870 about a twentieth of 1700's wagons (Bogart); national markets for milk, fish and meat; railway time (Greenwich, 1847); the telegraph along the lines (1837) |
| **Steamships** | *Comet* on the Clyde 1812; *Great Western* across the Atlantic 1838; Cunard 1840; *Great Britain* (iron, screw) 1843; Holt's compound-engined ships to China 1865; Suez 1869 | coal-fired engines; iron then steel hulls | **coaling stations** worldwide (Welsh steam coal); iron plate; Clyde, Tyne and Mersey engine builders; compound engines frugal enough for long voyages | ocean freight fell sharply after 1850 (Harley); tramp rates roughly halved from the early 1870s to the early 1910s (Hatton); the Chicago to Liverpool wheat price gap fell from over half to under a sixth, 1870 to 1895 [R]: a world grain market |

### 5.2 Costs per ton-mile

Exact British series are hard to find in consistent units; orders of magnitude [R throughout]:

| Mode | Relative cost per ton-mile (horse wagon on an unimproved road about 1700 = 100) |
|---|---|
| Wagon on unimproved road, 1700 | 100 |
| Wagon on turnpike, 1820 | about 60 to 80 |
| Canal, 1800s | about 25 to 50 |
| Coastal shipping | lower still, slow and seasonal |
| Railway, 1870 (real terms) | about 5 |

American figures (George Rogers Taylor) tell the same story: about 15 to 20 cents per ton-mile by wagon before 1860, 1 to 2 cents by
canal or railway [R]; the Erie Canal (1825) cut the cost of a ton from Buffalo to New York from about $100 to about $10 and the
journey from about three weeks to about a week [R].

### 5.3 Effects on markets and location

- **Industries moved to coal** once transport made coal cheap where it was mined and dear far from it; and to ports.
- **Markets widened** (Smith's "extent of the market"), so specialisation deepened: Lancashire for cotton, Sheffield for cutlery
  and steel, the Potteries for ceramics, Northampton for shoes.
- **The railway was itself the largest new customer** of iron, coal, engineering and capital in mid-century; its social saving to
  the British economy by 1865 was estimated by Gary Hawke at roughly 7 to 11% of national income [R, C: Robert Fogel's lower US
  estimate for 1890 started the debate on whether railways were "indispensable"].
- **New towns** grew on the lines (Crewe, Swindon, Middlesbrough, founded 1830 as a coal port and an iron town by the 1850s after
  Cleveland ironstone was found); old ones off the lines declined.

---

## 6. Chemicals and materials

### 6.1 Why textiles made the chemical industry

Cloth must be **bleached**, **soured**, **dyed** and **printed**. In the organic economy that meant lye from wood or kelp ash,
souring in buttermilk, and weeks to months laid on grass in the sun, on bleachfields near towns. When spinning and weaving output
rose many times, bleaching became the bottleneck (land, months, ash, buttermilk). Each step was replaced by a chemical:

| Organic way | Chemical replacement | Who, where, when | Prerequisite |
|---|---|---|---|
| sour milk | dilute **sulphuric acid** | Roebuck and Garbett's **lead-chamber process** (Birmingham 1746, Prestonpans 1749): acid in lead rooms, not glass globes | lead sheet; Sicilian sulphur; saltpetre; a chemist's training |
| sun and grass | **chlorine**, then **bleaching powder** | Berthollet (France, 1785); **Charles Tennant**, patent 1799, at **St Rollox, Glasgow**, the world's largest chemical works in the 1830s and 1840s (over 100 acres; "Tennant's Stalk", 1842, 435 feet) | sulphuric acid, salt, manganese dioxide, lime |
| wood ash, kelp, barilla | **soda ash** by the **Leblanc process** | Leblanc (France, 1791); in Britain after the salt tax cut of 1823: **Muspratt** at Liverpool, then St Helens and **Widnes**. About 140,000 tons by 1852 and 200,000 a year in the 1870s, more than the rest of the world [R] | Cheshire salt, acid, coal, limestone, all near the Mersey |
| madder, indigo | **synthetic dyes** | Perkin's **mauve** (London, 1856, aged 18, a student of Hofmann); alizarin (1868 to 1869); indigo (BASF, 1897) | **coal tar from the gasworks** (benzene → aniline, needing nitric acid); organic chemistry; laboratories |

### 6.2 The alkali chain and its by-products

The Leblanc process is an **assembly with joint products and a commons**. Salt is heated with sulphuric acid to make salt cake
(sodium sulphate) and **hydrogen chloride**; salt cake is roasted with limestone and coal to give "black ash", which is leached
to give soda. For every eight tons of soda ash, about five and a half tons of hydrogen chloride gas and seven tons of calcium
sulphide waste ("galligu") [R]. At first the gas went up the chimneys and killed crops and trees for miles around Widnes and St
Helens; the waste heaps leached poison into streams.
- The **Alkali Act of 1863**, Britain's first major air pollution law, required works to absorb 95% of the hydrogen chloride and
  set up the Alkali Inspectorate. The captured acid was then **turned into a product**: it made chlorine for bleaching powder (the
  Weldon and Deacon processes, 1860s to 1870s). **Regulation turned a waste into a joint product.**
- The **Solvay ammonia-soda process** (Ernest Solvay, Belgium, 1861 to 1863), with less waste, was licensed in Britain by
  **Brunner Mond** at Winnington, Cheshire (1873 to 1874) and displaced Leblanc by about 1900. The Leblanc firms merged into the
  United Alkali Company (1890) to survive; Brunner Mond became a founder of ICI (1926).

### 6.3 What soda and acid fed

- **Soap** (soda + tallow or vegetable oil; soap tax repealed 1853; Lever Brothers, Port Sunlight, 1888, using palm and coconut
  oil from West Africa and the Pacific).
- **Glass** (soda + sand + lime).
- **Bleaching** and dyeing.
- **Fertiliser**: John Bennet Lawes treated bones and mineral phosphates with sulphuric acid (**superphosphate**, patent 1842;
  Rothamsted). Industry fed back into farming.

### 6.4 Dyes: Britain invents, Germany scales

Perkin's mauve was British, but by 1900 to 1913 German firms (BASF 1865, Bayer 1863, Hoechst 1863, Agfa 1867) made most of the
world's synthetic dyes [R: often put at about 80 to 90%]. The reasons usually given: university chemistry and research
laboratories inside firms; patent law (the German Patent Act of 1877); and bank finance. Synthetic alizarin destroyed the madder
fields of France and the Low Countries within a decade; synthetic indigo hit Bengal's indigo plantations after 1897. **A paradigm
switch in one country removes a land-based chain in another.**

### 6.5 Glass

- **Plate glass**: the British Cast Plate Glass Company at Ravenhead, St Helens (1773), using French casting methods.
- **Pilkington** (St Helens, 1826): St Helens had coal, sand and, after the 1820s, the alkali works next door.
- **Sheet glass** by the cylinder method: Chance Brothers (Smethwick, from 1832). The glass excise was repealed in 1845, and the
  price fell.
- **The Crystal Palace** (Paxton, 1851) used about 300,000 panes of Chance glass (about 900,000 square feet) on a cast and
  wrought-iron frame of standard parts, built in about five months [R]: iron, glass, standardisation and the railway (to bring
  the parts) in one building.

### 6.6 Cement and concrete

- John Smeaton's study of hydraulic lime for the Eddystone lighthouse (1756 to 1759).
- James Parker's "Roman cement" (1796).
- **Joseph Aspdin's Portland cement** (patent 1824, Leeds), improved by William Aspdin and Isaac Johnson (higher-temperature
  clinker, 1840s). Firing it needed coal kilns; grinding it needed steam mills.
- Joseph Bazalgette's London main drainage (1859 to 1875) used Portland cement on a vast scale and with systematic strength
  testing [R]. Reinforced concrete (Monier, 1867; Hennebique, 1892) joined cement to cheap steel.

---

## 7. Organisation

### 7.1 The factory and wage labour at scale

- **Early "manufactories"** gathered hand workers under one roof before power did: Matthew Boulton's Soho Manufactory
  (Birmingham, 1766, several hundred workers [R]); Josiah Wedgwood's Etruria (Stoke, 1769), with a fine division of labour,
  clocking-in and rules. Lombe's silk mill at Derby (1721) was a powered precursor.
- **Discipline and time**: E. P. Thompson's essay on time and work discipline and Sidney Pollard's *Genesis of Modern Management*
  describe the bell, fines, overlookers, the move from task time to clock time.
- **Labour law and response**: the Combination Acts (1799 to 1824) forbade unions; the Truck Act (1831) required wages in coin;
  unions, friendly societies, cooperatives (Rochdale, 1844), Chartism (1838 to 1848).
- **Living standards**: real wages were flat or nearly so from about 1780 to 1830 or 1840 while output per worker rose (Robert
  Allen's "Engels' pause"); Charles Feinstein estimated a rise of only about 30% in real wages between the late 1770s and the
  1850s [R]. Hans-Joachim Voth finds working hours rose, so consumption per head adjusted for leisure barely changed from 1760 to
  1830.

### 7.2 Capital, companies and banks

- **Most industrial capital came from partners, kin, retained profit and trade credit** (François Crouzet). An early cotton mill
  cost a few thousand pounds [R]; fixed capital was small, working capital (stocks of fibre and yarn) large.
- **The Bubble Act (1720)** restricted joint-stock companies; until its repeal (1825), large undertakings that needed many
  investors (canals, turnpikes, docks, then railways) were set up **one at a time by private Act of Parliament** as statutory
  companies.
- **General incorporation**: the Joint Stock Companies Act (1844, registration), the **Limited Liability Act (1855)** and the
  Companies Act (1862). Most manufacturing firms stayed partnerships until late in the century.
- **Banks**: the Bank of England (1694); country banks grew from about a hundred in the 1770s to several hundred by 1810 [R],
  issuing notes and discounting bills; in Lancashire **bills of exchange** circulated as money. Crises (1825, 1847, 1857, 1866)
  broke weak banks; the Bank Charter Act (1844) gave the Bank of England control of note issue. The London Stock Exchange
  (formalised 1801) traded government debt, then canal, railway and foreign shares.

### 7.3 Patents and knowledge

- The **Statute of Monopolies (1624)** allowed patents for new inventions. Before 1852 an English patent cost about £100, and one
  covering England, Scotland and Ireland about £300 or more [R]: a cost that shut out most workmen. The **Patent Law Amendment Act
  (1852)** cut the fee to about £25 for the first stage, and patenting rose several-fold [R].
- Patents mattered unevenly: Arkwright's patents were overturned in 1785; Watt's was extended; Crompton never patented; the
  Cornish engineers shared (1.3). Petra Moser finds most exhibits at the 1851 Crystal Palace were not patented: secrecy and
  first-mover advantage protected much innovation.
- **Useful knowledge** moved through societies (the Lunar Society of Birmingham: Boulton, Watt, Wedgwood, Priestley), lectures,
  mechanics' institutes and journals.

### 7.4 Urbanisation and its problems

| | 1700 | 1800 | 1851 | 1911 |
|---|---|---|---|---|
| England's population in towns | about 17% (towns of 5,000 or more) [R] | about 27% [R] | about half (the census) | about 80% [R] |
| London | about 575,000 [R] | about 960,000 (1801) | about 2.4 million | about 7 million (greater London) [R] |
| Manchester (with Salford) | small market town | about 90,000 (1801) [R] | about 400,000 [R] | |

The towns grew faster than water, drains and housing:
- **Housing and water**: back-to-backs, courts, cellar dwellings; cesspools and shared privies; rivers for both water and sewage.
  Cholera in 1831 to 1832, 1848 to 1849, 1853 to 1854 and 1866; John Snow traced the 1854 Broad Street outbreak to a pump.
- **Mortality**: Edwin Chadwick's *Report on the Sanitary Condition of the Labouring Population* (1842) gave average ages at death of
  17 for labourers in Manchester against 38 in rural Rutland, and 38 against 52 for professionals [C: average age at death is a poor
  measure, depressed by infant deaths, but the gap was real]. Urban life expectancy at birth in the worst industrial towns in the
  1840s was in the high twenties to low thirties [R].
- **Responses**: Public Health Acts (1848, 1875); after the "Great Stink" of 1858, Bazalgette's sewers (about 80 miles of main and
  1,100 of street sewers [R]); municipal gas and water (Chamberlain's Birmingham, 1870s). **Public goods at a scale no village
  faces**, needing rates, borrowing and engineers.

---

## 8. Why Britain, why then

| View | Who | Claim | Main critiques |
|---|---|---|---|
| **High wages, cheap energy** | Robert Allen, *The British Industrial Revolution in Global Perspective* (2009) | wages were high relative to capital and energy prices (Newcastle coal among Europe's cheapest energy); England's wage to capital-price ratio rose to about 1.7 by 1820 while France's stayed flat. Machines that saved labour and used coal paid in Britain first (the jenny: profitable in England, not France or India); improved, they paid everywhere | Humphries and Schneider (2019): spinning wages were not high, and hand spinners' earnings were low; Gragnolati, Moschella and Pugliese: under looser assumptions the jenny paid in France too; Kelly, Mokyr and Ó Gráda: high wages reflect better-fed, more productive workers, not just factor prices [C] |
| **Culture of growth, Industrial Enlightenment** | Joel Mokyr, *The Enlightened Economy* (2009), *A Culture of Growth* (2016) | a belief that nature could be understood and used for progress; scientists and craftsmen in contact; a deep pool of skilled mechanics; institutions that let innovators profit | hard to measure; Europe shared the Enlightenment; Allen: culture explains the supply of invention, not where it was used first [C] |
| **Coal and colonies** | Kenneth Pomeranz, *The Great Divergence* (2000) | the Yangzi delta and England were alike until about 1750 to 1800; England escaped the land ceiling by two accidents: **coal near London and water**, and the **"ghost acres" of the Americas** (cotton, sugar, timber from land worked by the enslaved) | Broadberry, Guan and Li: China had fallen behind by 1700 [C]; Kander, Warde and Theodoridis (2019): Britain was usually a net exporter of embodied land except in the early 1800s, so coal mattered more than colonies [C] |
| **Slavery and Atlantic trade** | Eric Williams; Joseph Inikori; Berg and Hudson | see 3.4 | O'Brien, Eltis and Engerman on the small share of profits [C] |
| **Institutions** | North and Weingast (1989) | the settlement of 1688 secured property and the public debt | Clark and others: property was secure before 1688; growth did not jump after it [C] |
| **Industrious revolution (demand)** | Jan de Vries | households worked harder for the market to buy new goods (tea, sugar, cottons), creating demand before supply changed | timing and scale debated |
| **Agricultural surplus** | many (Wrigley; Allen; Overton) | English agriculture fed a population with a small share of the labour force by 1800 [R: perhaps 35 to 40% of men], freeing labour for industry | the "agricultural revolution's" timing is disputed |

**A reading that fits most of them.** The prerequisites stacked (wood squeezed near London; coal near the sea and the market;
high wages, a large market and cheap credit; millwrights, clockmakers and smiths; Atlantic trade), **the first machines paid in
one place** (pit drainage, cotton spinning), and improvement by use spread them. The Netherlands is the counter-example: high
wages, commerce and peat, but the peat ran down and coal was far.

---

## 9. The fused web: how the chains merged

The industries of sections 1 to 7 were not separate. Four clusters, each joining several chains:

### 9.1 The coal, iron, steam and rail loop

```
coal seam ─ drained by → STEAM ENGINE ← cylinders, boilers ← IRON ← coke ← COAL
   │                         │                                   ↑
   │                         └── blows furnaces, rolls iron ─────┘
   └─ hauled on wagonways → iron rails + high-pressure engine = RAILWAY → carries coal, iron, everything
```

Each part was both customer and supplier of the others: **a self-reinforcing loop**, which is why output grew slowly for a century
and then explosively (coal tripled from 1830 to 1870). Places where all of it sat together became the classic industrial
districts: **Coalbrookdale** (coke iron, iron rails, the Iron Bridge), **the Black Country** (coal, ironstone and limestone on one
field; nails, chains, ironworks), **South Wales** (Merthyr's ironworks, then steam coal for the world's navies), **Tyneside and
Teesside** (coal export, locomotives, ships, Middlesbrough iron), **Lanarkshire and the Clyde** (blackband iron, hot blast,
marine engines, shipbuilding).

### 9.2 The cotton complex

Plantation (land, coerced labour, the gin) → Atlantic shipping and credit → Liverpool (docks, brokers) → canal and railway →
Lancashire mills (water then steam, mules, power looms; coal from the Lancashire field) ← textile machinery from Manchester
engineers ← iron → finishing (bleach, soda, acid, dyes) → Manchester exchange → world markets.

### 9.3 The chemical complex on the Mersey and Clyde

Cheshire salt + Lancashire coal + Derbyshire limestone + imported sulphur and pyrites → acid and soda (Widnes, St Helens) → glass
(St Helens), soap (Warrington, then Port Sunlight), bleach (St Rollox, then Widnes) → textiles. With pollution laws turning wastes
into products. Later the gasworks' tar → dyes.

### 9.4 The engineering complex

Millwrights and clockmakers → textile-machine makers → steam engine makers (Soho) → machine-tool makers (Maudslay's school) →
locomotive builders (Stephenson, Sharp Roberts, Beyer Peacock, Crewe, Swindon) → marine engines (Clyde, Thames) → machine tools for
sale, arms, sewing machines, bicycles. Each step widened the market for the skills of the step before.

---

## 10. A dependency tree

For each technology: what it needed (materials, fuel, skills, capital, demand, transport, institutions), what it enabled, its
chain shape, and whether it was a **paradigm switch** (PS) and what social change came with it.

| Technology (date) | Needed: materials, fuel | Needed: skills | Needed: capital, demand, transport, institutions | Enabled | Shape | PS and social change |
|---|---|---|---|---|---|---|
| **Coal for heat** (1500s to 1700s) | coal seams near water | hewers; colliers' boats | London's market (wood scarce); coastal shipping; wagonways | coal-fired trades (salt, brewing, brick, glass); later all of section 1 | substitute; chokepoint of geology | PS from wood: mining villages; a coal trade with its own guilds and fleets |
| **Newcomen engine** (1712) | brass or iron cylinder; boiler plate; slack coal | enginewrights; millwrights | mines needing drainage; a patent (Savery's covered it until 1733) | deep coal and metal mines | assembly; increasing returns at a mine | not yet a PS for work; a new trade (enginewright) |
| **Coke iron** (1709) | coking coal; low-sulphur ore; limestone | furnace keepers; founders | a cast-iron market (pots); river (Severn) transport | cheap cast iron; later all iron | substitute fuel; time capital (furnace campaigns) | PS from charcoal over 50 to 80 years; ironworks move to coalfields |
| **Watt engine** (1769 to 1776) | precision-bored cylinder (Wilkinson); iron | instrument making (Watt); fitters (Soho) | Boulton's capital; Cornish demand (dear coal); the 1775 patent extension | rotative power; mills off rivers; furnace blowing | assembly; long skill | PS for power, slowly (parity with water about 1830): mill towns on coalfields |
| **Jenny** (1764) | wood frame; spindles | joiners; spinners | putting-out merchants; a cotton market | more weft; cheaper yarn | shallow; accretive (more spindles) | not a PS: stays in the cottage |
| **Water frame and Cromford** (1769 to 1771) | water site; wheel; gears; cotton | millwrights; clockmakers | hosiers' capital; patent; labour brought to the site | warp yarn; all-cotton cloth; the factory | paradigm switch; increasing returns | **PS: the factory**, wage labour of families and children, mill villages |
| **Mule** (1779), self-actor (1825) | iron frames (later); power | mule spinners (adult male, skilled); later machine makers | mill capital; high demand for fine yarn | British muslins; displacement of Indian fine cloth | long skill then automation | PS within the mill: skilled spinners' power then its erosion |
| **Puddling and rolling** (1784) | pig iron; coal; reverberatory furnace; rolls | puddlers (a long skill) | steam engines for rolls; ironmasters' capital; navy and canal demand | wrought iron from coal; rails, plate, bars | long skill; increasing returns | PS: charcoal forge ends; iron towns (Merthyr) of thousands |
| **Gas lighting** (1792 to 1812) | coal; retorts; iron pipes | gas engineers | chartered companies; urban streets | long winter shifts; street safety; coke and tar | joint products | PS for light: night work and night streets |
| **Chemical bleaching** (1785 to 1799) | sulphuric acid; salt; manganese; lime | chemists; works managers | the textile boom; patents | bleachfields freed; chemicals at scale | assembly; joint products; commons (fumes) | PS: months to days; land released |
| **Leblanc soda** (1791; Britain 1823) | salt; acid; coal; limestone | chemists; furnacemen | salt tax cut (1823); Mersey transport | soap, glass, bleach, textiles | assembly with toxic joint products | PS from plant ash: kelp-burning on Scottish coasts collapses; pollution law (1863) |
| **Machine tools** (1774 to 1840) | iron; steel cutters; power | Maudslay's school; fitters and turners | demand from engines, textiles, navy (block mills), locomotives | precision; standard parts; all later machinery | long skill; increasing returns; convergence | PS for making: skilled fitters and engineering firms; standards (Whitworth threads) |
| **Canals** (1761 to 1830s) | puddled clay; stone; timber | surveyors (Brindley); navvies | bulk cargo (coal, pottery); private Acts; shareholders | cheap bulk inland; location on coal | time capital; commons (water supply); increasing returns | PS for bulk carriage: new ports and towns; the statutory company |
| **Railways** (1825 to 1850) | wrought-iron rails; coal; timber sleepers; stone | locomotive engineers; navvies; signalmen; clerks | enormous capital (joint stock, stock exchange, manias); Acts with compulsory purchase; national demand | national markets; time standard; telegraph; tourism; suburbs | increasing returns; network; time capital | **PS for all land transport**: a national labour market, the railway company as the first big firm with professional managers |
| **Iron steamships** (1838 to 1880s) | iron and steel plate; coal at stations | marine engineers; boilermakers; shipwrights in iron | world trade; mail subsidies; coaling stations (empire) | world markets in grain, meat, people (emigration) | chokepoint (coal stations); increasing returns | PS at sea: global grain price convergence; the tramp ship |
| **Portland cement** (1824) | chalk and clay; coal for kilns | kiln burners; testing | building and harbour demand | sewers, docks, foundations; then concrete | assembly | accretive, not a PS until reinforced concrete |
| **Bessemer and open hearth steel** (1856 to 1865) | low-phosphorus pig; spiegeleisen; refractory brick; gas | metallurgists; chemists | rail and ship demand; large plant | cheap steel: rails, ships, bridges, tools, wire | increasing returns; chokepoint (ore chemistry) | PS: steel towns; scale shifts to the USA and Germany |
| **Synthetic dyes** (1856 to 1897) | coal tar; nitric acid; benzene | trained chemists | research labs; universities; patents; bank finance | colours for textiles; then drugs (aspirin, 1897), explosives | long skill (science); increasing returns | PS from plant dyes: madder and indigo farming collapse; the research laboratory |

---

## 11. What a simulator could take from this

This section does not limit itself by what is cheap to run. It names layers a society simulator could plausibly represent, at
what grain, and what a world must already hold before each could emerge. The engine's present economy (farming, herding, crafts,
copper smelted with charcoal, water mills, ovens, roads and carts) is the organic base of the table in section 10. Every layer below
rests on it.

### 11.1 Principles from the history

1. **Each layer is a paradigm switch with several prerequisites at once.** Coke iron needs coking coal, suitable ore and a
   market for cast iron; the Watt engine a precise cylinder, a capitalist and a buyer paying dearly for fuel; the railway rails,
   engines, capital and law. Gate a layer on **conjunctions of states the world already holds**, not on a tech tree.
2. **The first buyer is the one who saves most.** Newcomen paid at collieries burning slack; Watt paid in Cornwall where coal was
   dear; the jenny paid where wages were high (Allen). Diffusion should follow **relative prices in the world**, so the same
   technique spreads at different speeds in different places.
3. **Improvement comes from use.** Duty tripled after Watt's patent lapsed; spinning hours fell six-fold after the mule was made.
   Techniques should **improve with cumulative use and shared information**, not arrive finished.
4. **Joint products and wastes make later industries** (tar → dyes; Leblanc's acid → bleach; basic slag → fertiliser): chains
   should leave by-products in the state for a later chain to use.
5. **Chains fuse into loops.** Coal-iron-steam-rail grew slowly, then fast, because each was the others' customer; letting one
   chain's outputs be another's inputs shows this without scripting.
6. **Social forms arrive with the technique** (the factory, wage and child labour, the company, the town, pollution law): model
   the **organisation as part of the chain**: who owns the machine, who works it, who is paid how.
7. **The gains come late and unevenly.** Wages stagnated for decades; towns were deadly. Read any metric of "industrial growth"
   against a null arm and a qualitative reading of who gained (the project's rule).

### 11.2 Layers a simulator could represent

| Layer | Abstraction that fits the engine's model | Preconditions in the world |
|---|---|---|
| **Coal as a fuel** | a mineral resource in rock parcels at depth; a **pit** as a building that yields coal per worker and needs drainage below a depth; coal as a substitute for charcoal and wood, with a penalty (fumes) for some uses unless coked or fired apart | coal seams on the map, preferably near water; a fuel shortage (wood scarce, the coppice overcut) so coal is worth the labour; carts or boats to move it |
| **Pumping engines** | a fitting at a pit that burns fuel per day to keep it dry; its fuel use a number that falls with improvements | iron or brass founding; a smith's long skill at a higher tier; pits deep enough to flood |
| **Coke and the iron chain** | ore + fuel + flux in a **furnace** (a building run in campaigns, with keepers as a long skill), giving pig; pig to wrought iron by a finery (charcoal) or puddling furnace (coal); each a technique with its own fuel and output | ore, limestone and a coking coal reachable together; the charcoal chain already strained; bellows (leather, as in economy_web.md 2.8) then a blowing engine |
| **Power from engines** | a rotative engine as a fitting that delivers units of mechanical work, a substitute for the water wheel that is not tied to a river but eats coal | the pumping engine; precise cylinders (a machine-tool skill); coal delivered cheaply |
| **Textiles beyond the household** | fibre (wool, flax, cotton) → yarn → cloth → finished cloth; spinning as the first bottleneck; the wheel, the jenny (more spindles per worker, in the home), the frame and the mule (needing power, in a mill); weaving later | sheep or flax land (economy_web.md 2.9); a market for cloth larger than the village; putting-out as an agreement where one party owns the material; water or steam power |
| **The factory** | a building with a power source, machines and many places for workers; work as a standing wage relation with hours; output per worker many times the home's | wage labour as a standing obligation (02zzi §3.6 N); people who are not agents (households as rule-driven labour pools) so that hundreds can work in one place; capital from one or several owners |
| **Chemicals** | acid, alkali and bleach as intermediates made from salt, sulphur, lime and coal; each process leaving wastes (acid gas fouling air and land downwind; liquid wastes fouling water) as state on parcels | salt (already a chokepoint in the engine), sulphur or pyrites, coal; a textile chain whose finishing is the bottleneck; then soap and glass as further customers |
| **Machine tools and engineering** | a **precision** attribute on tools and machines; machine tools as a technique that raises the precision ceiling; higher-precision machines as prerequisites for engines, mules and locomotives; skill passed by apprenticeship from a few masters | iron; power; a demand for precise parts (engines, the navy, textiles); the long-skill and teaching model (methods known by upbringing and teaching, 4c §3.3) |
| **Turnpikes and canals** | roads with a **surface** attribute that lowers cart costs, built and kept by a trust that charges tolls; canals as new edges for boats, built at great labour, giving bulk carriage at a quarter or less of road cost | carts and roads (E); a group able to raise capital and collect tolls; an authority that grants the right (an institution); a bulk cargo (coal) worth moving |
| **Railways** | track edges that need iron rails per unit length and a locomotive; very cheap per ton, very costly to build; a network whose value rises with its reach | wrought iron in quantity; high-pressure engines; machine tools; a company able to raise capital from many holders; rights over land along a route (compulsory purchase or bargaining) |
| **Steamships and a world market** | sea edges with coal consumption; coaling stations as chokepoints; distant regions whose grain and fibre can be bought | engines, iron plate, coal export; a world beyond the region (02zzi §6 notes a kingdom is not yet within the model of space) |
| **Plantation and coerced-labour chains** | a distant region of plentiful land and forced labour, linked to the core by credit and shipping | a frontier or colony; credit; demand at the core. With care: slavery is the moral weight of this history, not a mechanic to optimise; a simulator that includes it should show its costs to the people inside it |
| **Companies, banks, patents** | firms as parties that own capital with shareholders; limited liability as a rule; banks that lend and issue notes; patents as rights over a method for a term, with a fee | agreements with credit legs (E), ledgers at institutions (E: D2-33), enforcement by people rather than the engine (OPEN L-106), records and writing (information as a good, 02zzi §1) |
| **Industrial towns and public health** | a town node whose density raises disease and fouls water unless drains and water are built by levy | births and migration (demography work); an authority able to tax; engineers; signs of sickness grounded in state (senses guide) |

### 11.3 What a world needs before any of this can emerge

Gathered from sections 1 to 10, the prerequisites stack in this rough order:

1. **A strained organic economy**: wood scarce near people, land fully used, food for beasts competing with food for people. Without
   a ceiling, coal is not worth digging.
2. **Mineral resources in the right places**: coal near water and near people; iron ore with limestone near coal; salt. Geography
   decides where industry can start.
3. **A market wider than the village**: towns, regional trade and carriers, so that a mill's output can be sold (Smith's extent of
   the market). Without it, a jenny or a mill has no reason to exist.
4. **Relative prices that reward saving labour and using fuel**: labour dear, coal cheap. In a simulator this is a property of
   the world's state that the designer can vary between arms (Allen's test).
5. **A skill pool and a way to pass it on**: long skills (smiths, millwrights, enginewrights), apprenticeship, and movement of
   skilled people between places.
6. **Capital and the institutions to gather it**: savings, partnerships, credit, then companies; and enforcement of contracts
   that people provide (L-106).
7. **Transport that can carry bulk**: roads with carts, rivers and boats, then canals.
8. **Information that travels**: prices heard from traders, methods shared, records kept.
9. **Time**: over a century from Darby (1709) to the railway (1830). A simulator would need **multi-generation runs**, histories
   simulated before the agents arrive, or worlds that start part-way up the tree.
10. **People who are not all agents**: hundreds per works, hundreds of thousands per region. 02zzi §6 applies with force: agents
    as owners, managers, officials, union leaders and heads of household, the bulk as rule-driven households; Opus at the poles
    of leverage (ironmaster, banker, engineer, mill owner, reformer), Sonnet in the middle, Haiku in the bulk.

### 11.4 Questions a simulator could study

- **Does a fuel ceiling produce a fuel switch,** and who owns the pits?
- **Who captures a paradigm switch:** pooled households, a merchant, a lord?
- **Do relative prices steer invention?** Vary wages and fuel prices between arms.
- **Do chains fuse into a loop that takes off,** and how long does it take?
- **What happens to the displaced** (the handloom weavers): linger, collapse, resist?
- **Do wastes create rules,** and do the rules turn wastes into products?
- **Who pays for the drains** when a town's water spreads disease?

---

## Sources

Figures marked [R] are rough; [C] are contested. Where sources gave different figures, the text gives a range.

**Energy and coal**
- E. A. Wrigley, *Continuity, Chance and Change* (1988); *Energy and the English Industrial Revolution* (2010): organic and mineral
  economies; woodland-equivalent of coal [R].
- M. W. Flinn, *The History of the British Coal Industry, vol. 2, 1700 to 1830* (1984); R. Church, *vol. 3, 1830 to 1913* (1986);
  J. Hatcher, *vol. 1, before 1700* (1993): coal output. Long-run series as compiled by Our World in Data
  (https://ourworldindata.org/grapher/coal-production-by-country), Statista (UK historic coal production) and Thunder Said Energy
  (UK output 4 million tonnes in 1700, 17 in 1800, peak about 290 in 1913).
- J. Kanefsky and J. Robey, "Steam engines in eighteenth-century Britain", *Technology and Culture* 21 (1980): about 2,191 engines;
  J. Tann (1981): 451 Boulton & Watt engines, 268 rotative. Summarised at https://coalpitheath.org.uk/engines/history and in
  A. Nuvolari, B. Verspagen and N. von Tunzelmann, "The early diffusion of the steam engine in Britain, 1700 to 1800: a reappraisal",
  *Cliometrica* (2011), https://link.springer.com/doi/10.1007/s11698-011-0063-6.
- N. Crafts, "Steam as a general purpose technology: a growth accounting perspective", *Economic Journal* (2004); LSE working paper
  75/03, https://www.lse.ac.uk/asset-library/information/wp7503.pdf: installed horsepower; steam's small early contribution [R].
- H. Kitsikopoulos, *From Hero to Newcomen* and "The extent of steam power diffusion in Britain, 1774 to 1800: a revision" (2023),
  https://ideas.repec.org/h/spr/conchp/978-3-031-27362-9_1.html: upward revision for 1800.
- A. Nuvolari, "Collective invention during the British Industrial Revolution: the case of the Cornish pumping engine", *Cambridge
  Journal of Economics* (2004).
- Engine duty figures: 19th-century compilations, e.g. "Waste and economy of fuel", *Scientific American* (1869),
  https://www.scientificamerican.com/article/andldquowasteandrdquo-and-andldquoe-1869-03-13/, and *Popular Science Monthly* vol. 13;
  World History Encyclopedia, "The steam engine in the British Industrial Revolution", https://www.worldhistory.org/article/2166
  [R: units vary between sources].

**Iron and steel**
- C. K. Hyde, *Technological Change and the British Iron Industry, 1700 to 1870* (1977): coke versus charcoal costs; furnace counts
  (1788: 24 of 77 on charcoal; 1806: 11 of 173); pig iron output series [R].
- Archaeology Data Service thesis chapter, "Production of the iron industry",
  https://archaeologydataservice.ac.uk/catalogue/adsdata/arch-405-1/dissemination/pdf/thesis_text/6_Production_of_the_Iron_Industry.pdf;
  Grace's Guide, *The Basic Industries of Great Britain* (Aberconway), ch. XX, https://gracesguide.co.uk/The_Basic_Industries_of_Great_Britain_by_Aberconway:_Chapter_XX:
  pig iron about 2.25 to 2.5 million tons around 1850.
- Bessemer steel and rail prices: *Popular Science Monthly* vol. 31 (1887) ($80 a ton in 1873 to under $20 in 1886; British iron
  rails £5 in 1883, steel rails £4 10s in 1886); *Encyclopaedia Britannica* 1911 vol. 14 (rails £10 to £18 before 1875) [R].
- B. R. Mitchell, *British Historical Statistics* (1988): steel output; international comparisons [R].

**Textiles and cotton**
- H. Catling, *The Spinning Mule* (1970): operative hours per 100 lb of cotton, widely reproduced [R].
- C. K. Harley, "Prices and profits in cotton textiles during the industrial revolution", Oxford Economic and Social History working
  paper 81, https://www.nuffield.ox.ac.uk/economics/history/Paper81/harley81.pdf; J. Maw, "After the great inventions: technological
  change in UK cotton spinning, 1780 to 1835", *Economic History Review* (2021),
  https://eprints.whiterose.ac.uk/175067/.
- Raw cotton imports: *Statesman's Year-Book* (1871) (1815: 99 million lb; 1820: 152; 1830: 204; 1840: 592); papers on Brazilian
  and American supply (Brazil 40% of Liverpool imports 1791 to 1801; the US the largest supplier from 1799 to 1802; over 70% from the
  late 1820s), including the AEA 2008 paper at https://aeastaging.aeaweb.org/annual_mtg_papers/2008/2008_588.pdf [R].
- E. Williams, *Capitalism and Slavery* (1944); J. Inikori, *Africans and the Industrial Revolution in England* (2002); S. Beckert,
  *Empire of Cotton* (2014); M. Berg and P. Hudson, *Slavery, Capitalism and the Industrial Revolution* (2023); D. Eltis and
  S. Engerman, "The importance of slavery and the slave trade to industrializing Britain", *Journal of Economic History* (2000);
  Legacies of British Slavery database (UCL) [C].
- S. Marglin, "What do bosses do?" (1974); D. Landes, "What do bosses really do?" (1986): the factory debate [C].
- D. Bythell, *The Handloom Weavers* (1969): weaver numbers and earnings [R]; E. Baines, *History of the Cotton Manufacture* (1835):
  power-loom counts [R].
- Spinning mule history: Belper North Mill, https://www.belpernorthmill.org.uk/collections/our-favourite-things/the-spinning-mule/;
  Grace's Guide, https://gracesguide.co.uk/Cotton_Spinning_Machinery.

**Machines and engineering**
- Portsmouth Block Mills: Historic England, *The Portsmouth Block Mills: the start of a revolution*,
  https://historicengland.org.uk/research/results/reports/7165/THEPORTSMOUTHBLOCKMILLS-THESTARTOFAREVOLUTION; Britannica, "block
  mill", https://www.britannica.com/technology/block-mill (130,000 blocks in 1808; 10 men for 110, a contemporary claim).
- Sharp, Roberts & Co.: Grace's Guide, https://www.gracesguide.co.uk/Sharp,_Roberts_and_Co; Science Museum Group,
  https://collection.sciencemuseumgroup.org.uk/people/cp3899; steamindex, https://steamindex.com/manlocos/sharp.htm.
- L. T. C. Rolt, *Tools for the Job* (1965); N. Rosenberg, "Technological change in the machine tool industry, 1840 to 1910",
  *Journal of Economic History* (1963): technological convergence; D. Hounshell, *From the American System to Mass Production*
  (1984) [C].
- R. Meisenzahl and J. Mokyr, "The rate and direction of invention in the British Industrial Revolution: incentives and
  institutions" (NBER, 2012).

**Transport**
- D. Bogart, "Turnpike trusts, infrastructure investment, and the road transportation revolution in eighteenth-century England",
  *Journal of Economic History* (2005), https://gwern.net/doc/economics/2005-bogart.pdf; Bogart's survey of transport (railway freight
  in 1870 about a twentieth of 1700 wagon rates in real terms); UC Irvine working papers,
  https://www.econ.uci.edu/files/docs/workingpapers/2004-05/Bogart-02.pdf.
- Bridgewater Canal: Britannica (coal cost in Manchester halved), Grace's Guide, https://www.gracesguide.co.uk/Bridgewater_Canal;
  Historic UK.
- A. Odlyzko, papers on the British railway manias, https://www-users.cse.umn.edu/~odlyzko/doc/mania18a.pdf: mileage, investment
  as a share of GDP [R]; M. Casson on cumulative investment (about 60% of GDP by 1913) [R]; G. Hawke, *Railways and Economic Growth
  in England and Wales, 1840 to 1870* (1970); R. Fogel, *Railroads and American Economic Growth* (1964) [C].
- G. R. Taylor, *The Transportation Revolution, 1815 to 1860* (1951): US ton-mile costs [R]; Erie Canal figures from New York State
  canal histories, e.g. https://considerthesourceny.org (range of $4 to $10 a ton after 1825) [R].
- C. K. Harley, "Ocean freight rates and productivity, 1740 to 1913: the primacy of mechanical invention reaffirmed", *Journal of
  Economic History* 48 (1988), https://econpapers.repec.org/RePEc:cup:jechis:v:48:y:1988:i:04:p:851-876_00; T. Hatton, IZA
  discussion paper 18692 (2026), https://docs.iza.org/dp18692.pdf (tramp rates roughly halved early 1870s to early 1910s).
- K. O'Rourke and J. Williamson, *Globalization and History* (1999): the Chicago to Liverpool wheat price gap [R].

**Chemicals and materials**
- St Rollox and Tennant: Grace's Guide, https://gracesguide.co.uk/Charles_Tennant_and_Co; Science Museum Group,
  https://collection.sciencemuseumgroup.org.uk/people/cp86957/charles-tennant-and-company (largest chemical works in the 1830s and
  1840s; the 1842 chimney, 435 ft).
- Leblanc process and alkali law: Royal Society of Chemistry, *Chemistry World*, "A revolutionary casualty",
  https://www.chemistryworld.com/features/a-revolutionary-casualty/3004475.article; Environment and Society Portal, "England passes
  first Alkali Acts", https://www.environmentandsociety.org/tools/keywords/england-passes-first-alkali-acts; Environmental Chemistry
  Group, "150th anniversary of the Alkali Inspectorate", https://envchemgroup.com/150th-anniversary-of-the-establishment-of-the-alkali-inspectorate.html;
  production figures (140,000 tons in 1852; about 200,000 in the 1870s) and waste ratios as given in the standard accounts of the
  Leblanc process [R].
- A. S. Travis, *The Rainbow Makers* (1993): Perkin and the dye industry; J. J. Beer, *The Emergence of the German Dye Industry*
  (1959) [R on German share].
- T. C. Barker, *The Glassmakers: Pilkington* (1977); the Crystal Palace figures from standard histories of the 1851 Exhibition [R].
- Portland cement: A. J. Francis, *The Cement Industry 1796 to 1914* (1977) [R].

**Organisation, towns and living standards**
- N. Crafts and C. K. Harley, "Output growth and the British industrial revolution", *Economic History Review* (1992): output growth
  about 1% a year 1760 to 1801, about 1.9% 1801 to 1831; P. Antràs and H.-J. Voth, "Factor prices and productivity growth during the
  British industrial revolution", *Explorations in Economic History* (2003), https://www.jvoth.com/Factor_Prices.pdf; H.-J. Voth,
  "The longest years" (hours of work), https://www.crei.cat/wp-content/uploads/users/working-papers/voth_longestyears.pdf.
- C. Feinstein, "Pessimism perpetuated: real wages and the standard of living in Britain during and after the industrial
  revolution", *Journal of Economic History* (1998) [R]; R. Allen, "Engels' pause", *Explorations in Economic History* (2009).
- F. Crouzet, *The First Industrialists* (1985); S. Pollard, *The Genesis of Modern Management* (1965); E. P. Thompson, "Time,
  work-discipline and industrial capitalism", *Past and Present* (1967).
- C. MacLeod, *Inventing the Industrial Revolution: the English Patent System, 1660 to 1800* (1988); H. I. Dutton, *The Patent System
  and Inventive Activity during the Industrial Revolution* (1984); P. Moser, "How do patent laws influence innovation?", *American
  Economic Review* (2005) [R on fees and counts].
- E. Chadwick, *Report on the Sanitary Condition of the Labouring Population of Great Britain* (1842); the table of average age at
  death reproduced in J. Hanley, "Edwin Chadwick and the poverty of statistics", *Medical History* (2002),
  https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DB9628F9922A0EB9CC7988BD4CB0246A/S0025727300068721a.pdf/div-class-title-edwin-chadwick-and-the-poverty-of-statistics-div.pdf
  (Manchester labourers 17, professionals 38; Rutland labourers 38, professionals 52) [C].
- E. A. Wrigley, "Urban growth and agricultural change: England and the Continent in the early modern period", *Journal of
  Interdisciplinary History* (1985): urban shares [R]; census of 1851.

**Why Britain**
- R. C. Allen, *The British Industrial Revolution in Global Perspective* (2009); "The industrial revolution in miniature: the
  spinning jenny in Britain, France, and India", *Journal of Economic History* (2009),
  https://economics.web.ox.ac.uk/node/1467141; CORE Econ, *The Economy*, unit 2,
  https://books.core-econ.org/the-economy/microeconomics/02-technology-incentives-07-industrial-revolution-technologies.html
  (England's wage to capital-price ratio rising to 1.7 by 1820).
- J. Humphries and B. Schneider, "Spinning the industrial revolution", *Economic History Review* (2019); Economic History Society
  summary, https://ehs.org.uk/spinning-little-stories-why-cotton-in-the-industrial-revolution-was-not-what-you-think;
  U. Gragnolati, D. Moschella and E. Pugliese, "The spinning jenny and the industrial revolution: a reappraisal", *Journal of Economic
  History* (2011); review of the critiques at https://pseudoerasmus.com/2016/12/01/allen/ [C].
- J. Mokyr, *The Enlightened Economy* (2009); *A Culture of Growth* (2016); M. Kelly, J. Mokyr and C. Ó Gráda, "Precocious Albion"
  (*Annual Review of Economics*, 2014).
- K. Pomeranz, *The Great Divergence* (2000), appendix on "ghost acreage"; A. Kander, P. Warde and S. Theodoridis, "Trade and
  overcoming land constraints in British industrialization: an empirical assessment", *Journal of Global History* (2019),
  https://lup.lub.lu.se/search/publication/28401396-37cd-4d75-85a1-1ff976d2b245; S. Broadberry, H. Guan and D. Li, "China, Europe,
  and the great divergence" (2018) [C].
- D. North and B. Weingast, "Constitutions and commitment" (1989); G. Clark, *A Farewell to Alms* (2007); J. de Vries, *The
  Industrious Revolution* (2008); P. Parthasarathi, *Why Europe Grew Rich and Asia Did Not* (2011).

**In the project:** `docs/review/37_growth/02zzi_economies_scaling.md` (the frame, §3.6 proto-industry, §3.8 the mineral edge, §6
scaling the engine); `docs/cybertron2/proposals/economy_web.md` (chain shapes; metal, fuel, cord and leather chains); OPEN L-104
(populations that are not agents), L-106 (enforcement by people); D2-33 (ledgers at institutions); `docs/scenario_design.md`
(model tiers, null arms).
