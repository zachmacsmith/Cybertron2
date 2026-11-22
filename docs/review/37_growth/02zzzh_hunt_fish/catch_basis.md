# The catch basis checked against real eel fisheries: can a household bank a winter?

22 Nov 2026, 37.2 (subagent). Thread W-85. Zach decided (D2-293): one shared catch basis for every part of the fishing design, the
calibrated bot runs, "checked against real eel-fishery records before building, so whether a household can bank a winter is a
finding and not an artefact of an assumed catch". This note is that check. No code, data, spec, proposal or record changed; nothing
decided; no model runs. One arithmetic script ran in the scratchpad (§4).

**Read first:** [fishing_ladder.md](fishing_ladder.md) (§2c, §2e, §4: real trap, buck and weir figures already found),
[smokehouse_capacity.md](smokehouse_capacity.md), [wave1_physical_basis.md](wave1_physical_basis.md) §2 (the keeping curve),
[wave3_keeping.md](wave3_keeping.md) §5 and [wave3_taking.md](wave3_taking.md) §5 (their worked households, on catches they
assumed), [02zzw_water_fixes.md](../02zzw_water_fixes.md) §6 and §7 (the bot runs), [02zzz_live_runs_world.md](../02zzz_live_runs_world.md),
[02zzy_why_they_did_not_fish.md](../02zzy_why_they_did_not_fish.md), [02zzy2](../02zzy2_fishing_methods_compared.md),
[02zzu_lookup.md](../02zzu_lookup.md) (the unit of fish, the run sizes, the weir a year). **Code read:** `engine/data.py:47-49`
(the fish unit), `:360-379` (WATER_WORKS: the weir and the trap), `wild/kinds.py:58`, `:649-651` (eel, salmon, lamprey goods),
`:860-882` (RUNS, RUN), `wild/methods.py:72-88` (`trap in water`, SETS), `wild/gear.py:18-24` (gear sharing a run),
`engine/bots_livelihood.py:492-514`, `:684-698` (the bots' traps), `specs/nutrition/runs_high.yaml` (the households).

**How the sources were read.** Page fetches failed: historiacartarum.org, foodsofengland.info and gutenberg.org do not resolve in this
session's network, so I stopped trying further hosts. Every outside figure is from **web search summaries** of the pages named, or
from the earlier notes in this folder (which were also search summaries). Marks on every figure:
- **(sec.)** a search summary of the page cited; **(sec., ladder)** the same, carried from fishing_ladder.md;
- **(m)** my memory, not checked this session;
- **(est.)** my own arithmetic or judgement;
- **[r]** read in this repository (code or a run report).
No figure here was read on its source page.

---

## 0. In brief

- **Per night, the engine is real.** A set trap lands about 1 kg of eel a run night on average and up to about 3 kg on a big one
  (hold 10 units); real wicker traps, bucks and fykes took about 0.5 to 5 kg on a run night. A weir's first section holds 100 units
  (86 kg of whole eel) a night and a full three-section weir 240; a small real buck weir took 25 kg to "hundredweights" on a good
  night, and the big fisheries 0.5 to 1.5 t (one Bann night with nets, 40 t). The engine's weir is a small village weir, inside the
  record.
- **Per season, in kilograms, the traps are real and the weir is low.** The bots' traps landed about 11 units a trap an autumn
  (about 9.5 kg of whole eel), inside my estimate of a real wicker trap's season (5 to 40 kg, est.; no sourced figure). The bots'
  weir took about 630 eels (about 310 kg) an autumn and 180 salmon. A Domesday fishery rendered 300 to 27,150 eels a year as rent
  alone; a real village weir's catch was perhaps 2,000 to 20,000 eels (est.). In kilograms the engine's weir is **about 3 to 15 times
  low**.
- **But the engine's year is 32 nights.** A kilogram feeds the same night in the engine as in life, and the winter is 8 nights, not
  about 90 days. Measured as a **share of a year's food**, the bots' trap households took 70 to 85% of their year's food from one
  autumn's traps (landed, before spoiling), and the village 140%. In the record, fish gave 3 to 5% of the calories in medieval
  rations (sec.), and where eels or salmon were the staple the run fed perhaps 5 to 25% of a year (est.). On that basis the engine's
  traps are **about 3 to 25 times rich** (central about 7), and the weir is about right (a real weir's 25% efficiency on a run cut to
  the 32-night year, which is what the engine does).
- **The finding, on the bots' basis and D2-289's curve:** a household of four needs about **165 units landed with salt (180 with a
  keeping smoke) to bank the 8-night winter, and about 330 (440) to reach the next run**, after eating about 40 food during the run
  itself. At the bots' 11 units a trap that is **about 15 traps for the winter and 30 to 40 for the gap**. A household with D2-264's
  set of 6 cannot feed itself through the run on its traps; 12 traps bank about 4 winter nights; the Brooks' 19 about 12. **A weir
  household banks the whole gap with a large surplus.**
- **Against history:** a weir household's surplus is true to the record (weirs and fisheries made the renders, the trade and the
  winter stores, and they were held). A trap household banking a winter from its own traps is not: the sources show the eels of a
  household's own gear as a few weeks' food and a supplement, taken fresh through the winter too ("dig them out of their beds all
  the winter", Winslow 1621, (m)). In the engine a household with about 15 traps can bank a winter **because of the 32-night year,
  not because of the catch**.
- **Recommended** (§5): keep every per-night figure, the weir's share and the run sizes; **cut the set trap's take of a passing run
  by about 3** (the low end of the 3 to 25), so a trap's autumn is about 4 units and a trap household banks a winter only with about
  40 traps, a share of the weir, or other food. The alternative is to keep the traps and name the departure (D2-259) at about 3 to 10
  on the share of the year. Zach's choice (§6, question 1).

---

## 1. The engine's basis

| What | Value | Where |
|---|---|---|
| a unit of fish | 1,150 kcal of flesh, "about 1 kg gutted and headed"; for eel it is **0.86 kg of whole eel** (0.63 kg of flesh); 0.46 food a unit, so **0.53 food a kg of whole eel** | data.py:47-49; 02zzu_lookup.md:189, :260 [r] |
| an eel | 0.58 units (about 0.5 kg whole); a salmon 3.06 units (4 kg); a lamprey 0.19 | kinds.py:649-651 [r] |
| a set trap | holds 10 units (17 eels); one trap a set act now, up to about 6 a set decided (D2-264); wrecked 0.5 in a spate, 0.85 in a flood | data.py:367, :387; methods.py:87 [r] |
| a weir | first section 30% of a run passing, up to 100 units a night; each added section 7%, up to 70; at most 3 added | data.py:377-378 [r] |
| the run's size | Burrishoole's 20 to 50 silver eels a km² of catchment a year, x 32/365 (the year compressed); the eel's recruitment b 3.0 | kinds.py:55-58, :866-873 [r] |
| a run night at Eelmouth (the runs world, no one fishing, seed 5) | about 5,900 eels in ten nights, 350 to 1,100 a night (about 3.4 t) | wave3_taking.md §5.1 [r] |
| the year | 32 nights; durations compress at about 1/11.4, daily rates stay real (D2-209, D2-259) | spec [r] |
| food | 1 food = 2,500 kcal; an adult 1 a night, a child 0.6, an elder 0.8 (D2-292): a household of four about 4 a night | DECISIONS [r] |
| keeping (D2-289) | "keeps d days" = a quarter lost by then, on the curve nights = min(d, 2) + (d - 2)/11.4 | DECISIONS; wave1 §2.1 [r] |

**The keeping rates under D2-289** (my arithmetic on wave1 §2.1's curve; the old "half lost" rates beside them):

| Kept as | Real keeping | Curve nights | A night, a quarter lost (D2-289) | A night, half lost (wave1, replaced) |
|---|---|---|---|---|
| fresh fish | 1 to 2 days | 1.5 | 0.17 | 0.37 |
| keeping smoke | about a season (90 days) | 9.7 | 0.029 | 0.069 |
| hard cure | most of a year (270) | 25.5 | 0.011 | 0.027 |
| salt fish | about a year (365) | 33.8 | 0.0085 | 0.020 |
| dried fish, kept dry | 450 days | 41.3 | 0.0069 | 0.017 |

**The bot runs (D2-293's basis)**, the high arm, `--bots runs`, 64 days (two autumns), 12 people in three households (8 who work:
Brook 3 and 2 children, Marsh 3 and 2, Shepherd 2), three timber sections at the Marshs' weir [r, 02zzw §7]:

| | Two autumns | One autumn | Notes |
|---|---|---|---|
| weir | 841 food = **1,830 units**: 1,254 eels (727 units) and 360 salmon (1,102 units) | about 915 units: **630 eels (364 units) and 180 salmon (551)** | 60% of the weir's take by weight is salmon |
| traps | 342 food = **743 units** landed: 1,210 eels | about **371 units**, 605 eels | lost besides from the traps: 257 units swept, 95 to otters (two autumns) |
| village, all gear | about 2,600 units | **about 1,300 units (590 food)** | the village eats about 13 food a day (02zzw §6): about 416 food a year |
| fresh fish spoilt | 969 units | | the bots salted 120 and smoked 278 |

**Traps in the water** (est. from the bot policy, not counted in the run): `traps` 8 a fisher, the keeper (head) 3, in the weir's
household 2 each and the keeper none (`bots_livelihood.py:500`, `:614`, `:654`). That is Brook 19 (3 + 8 + 8), Shepherd 11 (3 + 8),
Marsh 4 (2 + 2): **about 34**. Over about 10 run nights an autumn that is about 340 trap-nights, so the traps **landed about 1.1 units a
trap-night (0.9 kg of whole eel) and caught about 1.6** before the river and the otters took their part, and **about 11 units a trap
an autumn**. The same figure, "each adds about 11 kg over the run", came out of wave3_taking §5.1's walk.

**By household, one autumn, landed** (est., traps shared out by the count above):

| Household | People (food a night) | Gear | Landed | Food | Share of its 32-night year |
|---|---|---|---|---|---|
| Brook | 3 adults, 2 children (4.2) | 19 traps | about 207 units | 95 | **about 70%** |
| Shepherd | 2 adults (2.0) | 11 traps | about 120 units | 55 | **about 85%** |
| Marsh | 3 adults, 2 children (about 4.4) | the weir, 4 traps | about 960 units | 440 | **about 310%** |

---

## 2. Real catches

### 2.1 A trap, a pot, a net or a buck, one night

| Gear, place, time | A night | In kg (whole eel) | Mark, source |
|---|---|---|---|
| a wicker trap off the run (yellow eels) | | 0.1 to 0.5 | est., fishing_ladder §2c |
| fyke nets, Shannon (modern survey) | 30 to 45 eels, 4.5 to 8.5 kg per 10 fykes | 0.45 to 0.85 a fyke | sec., ladder |
| fyke nets, Iniscarra (Lee) | 1,162 kg from 70 nets in 10 nights | 1.7 a net | sec., ladder |
| fyke nets, New Zealand commercial; Pouto lakes survey | 2.72 and 3.06; 5.08 kg a net-night | 2.7 to 5.1 | sec. ([FAR 2014/21](https://fs.fish.govt.nz/Doc/23527/FAR_2014_21_EEL2010-03%20(obj.%202,%20MS7).pdf.ashx)) |
| fyke nets, poor Irish lakes, 1968 (Moriarty) | "less than 100 g per net per day" | under 0.1 | sec. ([FAO](https://www.fao.org/4/aa043b/AA043B06.htm)) |
| eel bucks on a Thames weir, 19th century | "a team of six bucks could top half a hundredweight" on a good night | about 4 a buck (a buck is several grigs, ladder) | sec., ladder ([Fishing Museum](http://www.fishingmuseum.org.uk/eel_bucks.html)) |
| a Thames buck weir | "often hundredweights are taken in a night" | 50 and more, the weir | sec. ([Eel buck](https://en.wikipedia.org/wiki/Eel_buck)) |
| Peter Carter, a Fen eel catcher, 1980s | "150 lb of eels from the river in one night"; later "lucky to gather 50 lb in an entire month" | 68 a night across his gear (the number of traps not given) | sec. (search summary of press reports on Carter) |
| stow net (Hamen), Elbe, 1956 to 1971 | mean 11.55 kg a net a day; yearly means 7 to 21 (1965-69); a few kg in spring, 10 and more at the peak | about 12 a net-day | sec., poor OCR ([ICES 1968 M5](https://www.ices.dk/sites/pub/CM%20Doccuments/1968/M/1968_M5.pdf), [ICES 1974 M3](https://www.ices.dk/sites/pub/CM%20Doccuments/1974/M/1974_M3.pdf)) |
| an eel net worked from a boat by two, an English manual (19th or early 20th c.) | "it is a poor night's work not to catch from half a hundredweight to a hundredweight of eels"; far more "if it is the first freshet after a long drought in September and October" | 25 to 50, for two people | sec. ([Eel Trapping](https://bookdome.com/outdoors/fishing/Fishing/Chapter-XXIII-Eel-Trapping.html)) |
| a Ngāi Tahu elder fishing from a river bank for the winter supply | 180 eels one night, 120 the next | est. 50 to 300 in all (0.3 to 1 kg an eel, est.) | sec. ([Te Ara, te hopu tuna](https://teara.govt.nz/en/te-hopu-tuna-eeling)) |

**Reading.** A single wicker trap on a run night: **about 1 to 5 kg (est.)** from the bucks, the fykes and Carter's night; off the run a
few hundred grams. A professional's whole gear on a good night: tens of kilograms. I found **no sourced figure for one wicker trap
on one night**.

### 2.2 A weir, a channel or a fishery, one night

| Where, when | A night | In kg (whole) | Mark, source |
|---|---|---|---|
| Plymouth, September 1621 (Winslow's letter in *Mourt's Relation*) | "a hogshead of eels in a night, with small labour" | a hogshead about 240 litres: **est. 150 to 200** | sec. for the line ([Pilgrim Hall](https://www.pilgrimhall.org/?p=2022)); the kg est. |
| a stone V weir on the upper Delaware (Hancock, NY), modern | "over 1,000 eels" on a peak night, **about half of the season's catch**; one or two a day in July | est. 400 to 1,000 (American silver eels, mostly females, about 0.4 to 1 kg (m)) | sec. ([The Eel Deal](https://roadfood.com/?p=53046)) |
| Te Waihora (Lake Ellesmere), one channel cut through the gravel bar | "two to three thousand eels" on a good moonless night of the run | est. 600 to 2,000 | sec. ([Te Ara](https://teara.govt.nz/node/8562)) |
| Killaloe eel weir, Shannon (1986 paper) | "probably 1.5 tonnes maximum per night at the time of peak silver eel migration" | 1,500 | sec. ([FAO, Moriarty](https://www.fao.org/docrep/009/ae996b/AE996B06.htm) and the search summary) |
| Lower Bann, early 1980s, a small team with nets | "almost 40 tonnes" from dusk to dawn | 40,000 | sec. ([Irish Times](https://www.irishtimes.com/news/shadowy-weedy-water-world-of-eels-1.1099171)) |
| Te Waihora, recent: escapement, not a catch | "19 tonnes of eel made it over the bar" in one night | (passing) | sec. ([ECan](https://www.ecan.govt.nz/get-involved/news-and-events/2025/tuna-eel-stranding-at-te-waihoralake-ellesmere)) |

**Reading.** A small village weir or buck weir: **tens to a couple of hundred kg on a good night**; a channel or a weir at a great run:
**half a tonne to 1.5 t**; a whole river netted: tens of tonnes. The engine's 86 to 206 kg is the first kind.

### 2.3 Seasons and years

| Who, where | A season or year | In kg (whole, est. at 0.2 to 0.4 kg an eel for European runs) | Mark, source |
|---|---|---|---|
| Domesday (1086), rents in eels a year: Stuntney 24,000; Doddington 27,150; Wisbech 14,000 and 1,500; Ely 3,750; Swavesey 3,750 and 225; Harefield and Harmondsworth (Middlesex) 1,000 each; Downham 300 | renders: rent, not the catch | 0.06 to 11 t; a middling fishery's render 1 to 1.5 t | sec. ([VCH Ely](https://www.british-history.ac.uk/vch/cambs/vol4/pp33-40), [Doddington](https://prod.british-history.ac.uk/node/15061), [Wisbech](https://www.british-history.ac.uk/node/15084), [domesdaybook.co.uk](https://domesdaybook.co.uk/cambridgeshire1.html)) |
| Domesday, the River Ouse | "52,000 eels ... in just one year" | 10 to 21 t | sec. (press summary, not checked against the text) |
| Domesday, England | "over 540,000 eels" a year in rents | | sec., a popular source ([History Hit](https://historyhit.com/?p=5168940)) |
| a fisherman at Wisbech (Domesday) | 5,000 eels a year to the abbot of Bury | 1 to 2 (his rent; his catch more) | sec. ([Wisbech](https://www.british-history.ac.uk/node/15084)) |
| Ramsey Abbey | "more than 70,000 eels each year" due from tenants; a 1194 lease: 1,000 eels a year | | sec. ([History Hit](https://historyhit.com/?p=5168940)) |
| Harmston (Lincs), one manor | 75,000 a year | | sec., ladder |
| the stick | 25 eels; a bind 10 sticks; London 1273: a stick at 2d | | sec. |
| the Delaware V weir | about twice its peak night (above): est. 2,000 to 3,000 eels | est. 1 to 2 t | est. from sec. |
| Shannon, silver eels, the whole river | at least 69 t a year before 1928 (65 t in 1927); 17.8 t a year in the 1940s; 9.6 in the 1950s; about 47 in the 1980s | | sec. ([FAO, Moriarty](https://www.fao.org/docrep/009/ae996b/AE996B06.htm)) |
| Lough Neagh's two weirs on the Bann (Toome, Kilrea) | about 150 t of silver eels a year (c. 2000); the weirs' long-run efficiency about **25%** of the run | | sec. ([Kennedy, Toome](https://files.libcom.org/files/2026-09/357kEelFisheryToome.pdf); [AFBI note](https://www.daera-ni.gov.uk/sites/default/files/2026-06/AFBI%20advice%20note_eel%20conservation%20target%20compliance_2026.PDF)) |
| Lough Neagh's fishermen | about 300 fishermen in 150 boats (an older FAO figure); about 550 t of yellow eels a year (c. 2000) | **est. about 1.8 t a fisherman a year** | sec. ([FAO](https://www.fao.org/fishery/docs/CDrom/aquaculture/a0844t/docrep/009/C2876B/C2876B27.htm)); the division est. |
| Swedish coastal eel fishermen | a catch limit of 8 t a fisherman a year | (a cap: some caught more) | sec. ([SLU](https://pub.epsilon.slu.se/id/document/20367549)) |
| Spakenburg, Zuiderzee | "over 90 kilograms of eels per hectare" | | sec. ([Intrafish](https://www.intrafish.com/news/a-troubled-fish/1-1-629190)) |
| Burrishoole (the engine's reference river, about 90 km²) | 2,200 to 2,900 silver eels a year (2002-2019); escapement 1.1 to 1.2 kg/ha | | sec. ([Marine Institute](https://www.marine.ie/site-area/areas-activity/fisheries-ecosystems/eel-census); [Poole et al. 2018](https://fishlarvae.org/wp-content/uploads/2017/10/Poole-et-al.-2018_Long-term-variation-in-numbers-and-biomass-of-silver-eels.pdf)) |

**What an eel weighs.** Burrishoole's silver eels averaged 95 g in the early 1970s and 215 g in the 1990s and 2000s (sec., Marine
Institute). An Erne model takes males at 114 g and females at 680 g (sec., [AFBI/Erne](https://data.jncc.gov.uk/data/20810981-e500-4207-a1df-b37cd9eb47e1/jncc-report-745.pdf)).
A mixed run is **about 0.2 to 0.4 kg an eel (est.)**; a female-heavy lowland run more. The engine's eel is 0.5 kg whole, at the
female end. Since the engine sizes its runs in Burrishoole's *numbers* a km², its run carries about **1.3 to 2.5 times Burrishoole's
kilograms** for the same count (est.).

**Reading.** A village weir's real season, **est. 2,000 to 20,000 eels, 0.5 to 5 t**, from the renders (which were rent, so the catch
was larger; I do not know by how much) and the Delaware weir. A full-time fisher with modern gear: **about 2 to 8 t a year**. A
household's own few traps: **no sourced figure.** My estimate is **5 to 40 kg of whole eel a trap a season** (est.: 10 to 20 nights
that count, at 0.5 to 2 kg, with the Delaware weir's half-the-season-on-the-peak-night as the shape of a run).

### 2.4 What households laid by, and what share of a year the eels gave

| Who | What | Mark, source |
|---|---|---|
| a Ngāi Tahu household (20th-century recollection) | the winter supply: 300 eels in two nights of bank fishing. **Est. 50 to 300 kg, 25 to 160 food, about 6 to 40 days of a household of four's whole food** | sec. ([Te Ara](https://teara.govt.nz/en/te-hopu-tuna-eeling)); est. |
| a Ngāi Tahu feast | 20,000 dried eels on hand | sec. (Te Ara) |
| Plymouth colony, 1621 | a hogshead a night in September; and (m) "can dig them out of their beds all the winter": eels taken fresh through the winter, not only banked | sec. and (m) |
| Native people of Massachusetts (Wood, 1634) | ate eels and salted the surplus for winter; "a single night's work was enough for a season's worth of eel suppers" (second-hand) | sec. ([Woods Hole Museum](https://woodsholemuseum.org/oldpages/sprtsl/v21n1-Eel.pdf)) |
| St Lawrence peoples | weirs, spears from boats and through the ice; "salted or smoked, this fish kept very well"; eels "enough food to survive the long winters" | sec. ([Community Stories](https://www.communitystories.ca/v2/la-peche-a-l-anguille_eel-fishing/story/aboriginal-and-european-techniques/)) |
| the Montagnais near Quebec (Le Jeune, *Relation* of 1634) | eels smoked in autumn, the main food until the snow allowed the moose hunt | **(m), not checked**; est. 2 to 3 months, 15 to 25% of a year |
| Budj Bim (Gunditjmara) | eels smoked in hollow trees, stored and traded; trap sections held by family groups; permanent stone houses | sec. ([Budj Bim](https://www.visitmelbourne.com/things-to-do/aboriginal-victoria/regional-spotlight-budj-bim-cultural-landscape)); no yield found |
| medieval Europe, reconstructible rations | fish gave **3 to 5% of calories** and took 10 to 20% of the food budget | sec. ([Springer](https://link.springer.com/content/pdf/10.1007/s10152-004-0203-5.pdf)) |
| the Columbia Basin (Craig and Hacker) | 50,000 people at **1 lb of salmon a day** each | sec. ([NW Council](https://www.nwcouncil.org/history/IndianFishing/)); est. 15 to 25% of energy |

**Reading.** Eels from a household's own traps were a few weeks' food. A winter's whole food of eels for a household of four (about 90
days, 360 food) is **about 700 kg of whole eel (est.)**; I found no household that laid by that much, though a weir or fishery holder
took several times it (and paid it in rent or sold it). Where eels or salmon were the staple, the run fed perhaps **5 to 25% of a
year (est.)**, more in the months after it. Generally, medieval fish was 3 to 5% of calories. **I do not know** a sourced share of a
year's food for any eel people.

### 2.5 Salmon, for comparison

| Gear, place | Catch | Mark, source |
|---|---|---|
| a rank of 650 putchers, Lydney (Severn), late 2000s | about 622 salmon a year, about one a putcher a season | sec., ladder |
| the Severn's putchers, 19th century | about 18,200 salmon a season | sec., ladder |
| Celilo Falls, dip nets | "several hundred fish a day" for the fishery | sec., ladder |
| Fraser Canyon | men caught "hundreds in an hour"; a woman processed 50 to 60 a day, and the processing took longer than the catching | sec., smokehouse_capacity §5 |
| the engine's weir | about 180 salmon an autumn (550 units) | [r] |

The engine's salmon weir sits at the low end: a modern, depleted Severn rank of putchers takes three times its salmon. I did not
search salmon weirs further (Northwest Coast weir capture rates exist in a UNBC thesis on the Babine weirs, sec., not read).

---

## 3. The engine against the record

Two bases. **A, in kilograms**: the engine's rule, daily rates real. **B, as a share of a year's food**: a real season's catch divided by
11.4, because the engine's year is 32 nights and a household eats a real night's food each of them. B is what "bank a winter" tests.

| Measure | Engine (bot basis) | Real | A: in kg | B: share of a year |
|---|---|---|---|---|
| **a trap, a run night** | about 1.1 units landed (0.9 kg whole), 1.6 caught, up to about 3.4 on a big night; hold 10 | 1 to 5 kg on a run night (est., §2.1); 0.1 to 0.5 off it | **in range, low middle** (x0.3 to 1) | (a night is a night) |
| **a weir, a run night** | first section 100 units (86 kg); full 240 (206 kg); Lowstrand's peak offers 333 | small weir 25 to 200 kg; great fisheries 0.5 to 1.5 t | **in range for a village weir**; x0.1 to 0.4 of a great one | |
| **a trap, a season** | about 11 units (9.5 kg whole) | est. 5 to 40 kg | **in range** (x0.25 to 2) | real / 11.4 = 0.4 to 3.5 kg: **engine x3 to 25 high**, central about x7 |
| **a household's traps, a season** | 6 traps 65 units; 12 traps 130; 19 (Brook) 207 | 6 traps est. 30 to 240 kg; 12 traps 60 to 480; a winter supply of 300 eels (50 to 300 kg) | in range, low | Brook's 70% of its year against est. 5 to 25% where eels were a staple: **x3 to 14** |
| **a fisher, a season** | 8 traps: about 90 units (77 kg) | 2 to 8 t a year (modern full-time); a 5,000-eel rent (1 to 2 t) | **x0.01 to 0.08: low** (a real fisher ran far more gear for months, yellow eels too) | real / 11.4 = 160 to 700 kg: **x0.1 to 0.5** |
| **a weir, a season (eels)** | about 630 eels, 364 units (313 kg whole) | est. 2,000 to 20,000 eels, 0.5 to 5 t | **x0.06 to 0.6: low** | real / 11.4 = 45 to 440 kg: **in range** (x0.7 to 7) |
| **a weir household's share** | about 310% of its year (about 120% on eels alone) | a weir holder's catch est. 0.5 to 5 t against a household's 1,460 food a year: 20 to 180% (est.), the rest rent and trade | | **in range to high** |
| **the village, a season** | about 1,300 units (590 food) against 416 food a year: **140%** | fish 3 to 5% of medieval calories; a staple 5 to 25% (est.) | | **far above**: the runs world has farming off by design (02zzz) |

**What it comes to.**
- **Per night the engine is honest.** A person sees a real trap's night and a real small weir's night.
- **The weir is right on share and low on kilograms**, and that is the compression working as intended: the run is sized to a real
  river x 32/365 (kinds.py:866) and the weir takes 30% of it (real: 25%). Its holds bind on the few big nights.
- **The traps are right on kilograms and rich on share.** A trap takes real kilograms from a run that is a twelfth of a real one,
  so it takes a far larger share of the passing eels than a real trap does (about 0.006 of those passing a river trap a night,
  wave3_taking §5.1), and the run's ten nights give it a real season's kilograms to feed a 32-night year.
- **No single setting makes a trap real on both bases.** A real trap's real season divided by 11.4 is 0.4 to 3.5 kg; a real trap's
  one good night is 1 to 5 kg. Even a run of one night (the floor) gives a trap more than its share. The departure for traps can be
  narrowed, not removed.
- **The weir's take is 60% salmon by weight.** "The eel weir" in the bot basis is half a salmon weir.

---

## 4. The finding: can a household bank a winter?

**The arithmetic** (a scratchpad script, not the engine): a household of four eating 4 food a night; the run's catch landed evenly over
10 nights; the household eats from it first (40 food over the run), and the rest is salted or smoked the same day (no fresh loss,
which favours the household); then the store is eaten at 4 a night through the 8-night winter and on toward the next run (24 nights
in all). Loss nightly at D2-289's rates (§1). Landed figures are net of what the river and the otters took. No other food counted.

| Household, one autumn | Landed | Food | Banked at winter's start (salt / smoke) | Nights fed after the run (salt / smoke) |
|---|---|---|---|---|
| 6 traps (D2-264's set), bot rate | 65 units | 30 | 0 / 0: **the run is not fed** | 0 / 0 |
| 12 traps, bot rate | 130 | 60 | 19 / 17 | **4 / 4** |
| 19 traps (the Brooks), bot rate | 207 | 95 | 52 / 48 | **12 / 10**: the winter, not the spring |
| 12 traps, share basis (real / 11.4; range 12 to 73) | about 40 | 18 | 0 / 0 | 0 / 0 |
| 12 traps at the top of real kg (40 kg a trap a season) | 557 | 256 | 208 / 190 | 24 / 24: the whole gap |
| the weir household (4.4 a night), eels only | 364 | 167 | 119 / 108 | **24 / 18** |
| the weir household, all its gear | 915 | 421 | 363 / 331 | **24 / 24**, about 300 food spare at the end of winter |

**What is needed** (same arithmetic): **about 165 units landed with salt, 180 with a keeping smoke, to bank the 8-night winter; about
330 with salt and 440 with smoke to reach the next run.** At the bots' 11 units a trap: **15 to 16 traps for the winter, 30 to 40 for
the gap.** (Under the replaced half-lost reading the smoke figures are worse: 19 traps feed 7 nights; wave3_taking's "30 to 40 traps"
was on that reading and holds here too.) Salt at 1 to 4 (D2-283) is about 25 kg of salt per 100 kg kept.

**Answers.**
1. **A trap household (6 to 12 traps) cannot bank a winter** on the bots' basis; with about 15 traps it can bank the 8-night winter,
   and with 30 to 40 the gap to the next run. On the share basis it cannot bank anything with 12 traps; it would need about 40 traps
   for the winter. **In the record a household did not bank a winter of eels from its own traps**: its eels were weeks of food, and
   winter eels were taken fresh (spears, digging, the ice).
2. **A weir household banks the winter and the whole gap with a large surplus** on every basis. That is the record: weirs and fisheries
   made the renders of thousands, the trade and the winter stores, and they were held by lords, abbeys and families.
3. **Where eels were the staple** they gave perhaps 5 to 25% of a year's food (est.; the Montagnais' autumn to the snow (m), a Ngāi
   Tahu winter supply of about 6 to 40 days, the Columbia's salmon at about 1 lb a person a day). In medieval England fish was 3 to
   5% of calories. **I have no sourced share for any eel people.**
4. **So the bots' basis makes trap households about 3 to 14 times richer, as a share of their year, than any real trap household**,
   and the result "a household with 15 traps banks a winter" is an artefact of the 32-night year meeting real per-night traps.
   "A weir household banks the gap" is a finding.

---

## 5. Recommended calibration

1. **Keep** the trap's hold (10 units), the weir's holds (100, 70), the weir's 30% share of a run (real weirs: 25%), the run sizes
   (Burrishoole x 32/365) and the keeping rates of D2-289. They match the record per night, and the weir matches it per year.
2. **Cut the set trap's take of a passing run by about 3**: from about 0.006 of the eels passing a river trap a night to about 0.002
   (the fen's 0.003 to 0.001). The lever is the trap's meeting with a run (`SETS["trap in water"]` `meet` 0.3 and `base` 0.5, or the
   run's `dense` 3.0 for traps only, `kinds.py:882`); the builder chooses which, and must leave the resident (shallows) take alone.
   A trap's autumn becomes about 4 units, a run night about 0.3 to 1 unit (a big one about 1.2), and a trap household banks the
   8-night winter only with about 40 traps, a share of the weir, or its other food. Why 3 and not 7: the real per-trap season is my
   estimate, not a source, and 3 keeps a trap's big night near the bottom of the real 1 to 5 kg.
   - **The cost:** a trap's night then reads below a real trap's (about 0.4 kg on an average run night). That is a named departure,
     x0.3 per night, in exchange for the share of the year coming within about x2 of the record.
   - **The alternative:** keep the traps as they are and name the departure as about x3 to x10 on the share of the year (D2-259),
     accepting that a household with about 15 traps banks a winter. The design then needs other binds to stop traps undercutting
     the weir's leverage (the withies, the wreck in spates, the otters, the hands to salt).
3. **Re-run the bots** after any change, then state the basis again in kg a trap-night, kg a trap-autumn and the household table of
   §4, before the keeping and taking parts build on it.
4. **Not recommended now:** the eel's weight (0.5 kg against a mixed run's 0.2 to 0.4) and the run nights' concentration (37.4's
   part); both are questions below. A concentrated run does not fix the traps: fewer, thicker nights give a trap the same season.

---

## 6. Questions for Zach

1. **Which basis should the traps keep: a real night or a real share of the year?** On the 32-night year a trap cannot have both.
   Today a set trap takes a real night's eels, so over the run's ten nights it lands a real season's kilograms, and that feeds a
   household about 3 to 14 times more of its year than a real trap did. Recommended: cut the trap's take of a run by about 3 (a run
   night about 0.4 kg, a named departure), keeping the hold, the weir and the run sizes. Alternative: keep the trap and name the
   departure on the year's share.
2. **Is a household with its own traps meant to be able to bank a winter alone?** The record says no: a household's traps gave weeks
   of food, the winter stores and the surpluses came from weirs and fisheries that were held, and winter eels were taken fresh. With
   the cut in question 1 it would take about 40 traps; without it about 15.
3. **Should the weir's catch stay half salmon?** The bots' weir took 630 eels and 180 salmon an autumn, 60% salmon by weight. If the
   design reads the weir as an eel weir, the salmon run's size (`cap_km` 6) or the weir's share of an up-run is the lever; if not,
   the basis should be called the run catch, not the eel catch.
4. **Should an eel weigh 0.5 kg or about 0.3?** The runs are sized in Burrishoole's numbers a km², and Burrishoole's eels average 215 g;
   the engine's 0.5 kg makes its run 1.3 to 2.5 times Burrishoole's in kilograms. A female-heavy lowland run (Lough Neagh, the Fens)
   supports the heavier eel. Recommended: keep 0.5 for lowland rivers and say so; lighter in a small upland river if worlds vary.
5. **Should eels be taken through the winter as well as banked?** Real households speared, dug and iced yellow eels all winter, so the
   run was not their only eel. That is the shallows and open-water stock (D2-264), absent from the runs world. Whether a household
   banks a winter then depends on that stock as much as on the run.
6. **Should the bot basis carry over to worlds with farming?** It comes from the runs world with farming switched off, where one autumn's
   landed catch is 140% of the village's year. Every household figure in §4 counts no other food; in a world with grain, a trap
   household's share of its year from eels falls toward the record without any change to the catch.

---

## 7. What is estimate, and what I did not find

**Estimates (mine):**
- the traps in the water in the bot run (34, from the policy) and so the per-trap-night and per-trap-autumn figures;
- a single wicker trap's run night (1 to 5 kg) and season (5 to 40 kg);
- eel weights for converting counts (0.2 to 0.4 kg a European eel, 0.4 to 1 kg an American silver eel, 0.3 to 1 kg a New Zealand
  one), and so every "in kg" of a count;
- a hogshead's eels (150 to 200 kg);
- a real village weir's season (2,000 to 20,000 eels, 0.5 to 5 t), from rents that were not the catch;
- the shares of a year (5 to 25% for a staple; the Ngāi Tahu supply as 6 to 40 days; the Columbia's 15 to 25%);
- the Lough Neagh figure per fisherman (1.8 t), by division of totals from different years;
- the §4 arithmetic's shape (an even landing, no fresh loss, no other food).

**From memory, unchecked:** Winslow's "dig them out of their beds all the winter"; Le Jeune's Montagnais living on smoked eels until the
snow; American silver eel weights.

**Not found:** a sourced catch for one wicker trap on one night or one season; a household's season of eels from its own traps; the
catch (not the rent) of any medieval weir; the weight of a medieval stick of eels; a per-night figure for Toome, the Corrib or the
Erne; Dutch or Baltic per-fisher figures before 1940 (Dekker's review, [SLU](https://pub.epsilon.slu.se/id/document/19512942), is the
lead); Hewes's per-capita salmon figures (the EPA heritage-rate reports cite them); the Babine weirs' capture rates (UNBC thesis).

## Sources

All read as search summaries; none opened. Hosts that would not resolve: historiacartarum.org, foodsofengland.info, gutenberg.org.

- Domesday and medieval rents: [VCH Ely](https://www.british-history.ac.uk/vch/cambs/vol4/pp33-40); [Doddington](https://prod.british-history.ac.uk/node/15061); [Wisbech manors](https://www.british-history.ac.uk/node/15084); [Swavesey](https://prod.british-history.ac.uk/node/8883); [domesdaybook.co.uk, Cambridgeshire](https://domesdaybook.co.uk/cambridgeshire1.html); [History Hit](https://historyhit.com/?p=5168940); [Atlas Obscura](https://atlasobscura.com/articles/medieval-eel-rent-map-england); [Mapping the Medieval Rural Economy](https://mdr-maa.org/?p=4938).
- Thames and Fens: [Eel buck](https://en.wikipedia.org/wiki/Eel_buck); [Fishing Museum, eel bucks](http://www.fishingmuseum.org.uk/eel_bucks.html); [Eel Trapping (manual chapter)](https://bookdome.com/outdoors/fishing/Fishing/Chapter-XXIII-Eel-Trapping.html); Peter Carter: [Ely Standard](https://www.elystandard.co.uk/news/22783783.eel-man-heartbroken-plans-ban-eel-fishing/), [Scottish Daily Mail](https://www.pressreader.com/uk/scottish-daily-mail/20160123/282222304771449); [Denny Farmland Museum](https://www.dennyfarmlandmuseum.org.uk/content/museum-blog/everything-eels); [Hampshire Archives Trust](https://hampshirearchivestrust.co.uk/stories/fishing-for-eels-in-the-archives).
- Ireland: [FAO, Moriarty](https://www.fao.org/docrep/009/ae996b/AE996B06.htm); [FAO, Irish lakes](https://www.fao.org/4/aa043b/AA043B06.htm); [Kennedy, Toome eel fishery](https://files.libcom.org/files/2026-09/357kEelFisheryToome.pdf); [AFBI advice note 2026](https://www.daera-ni.gov.uk/sites/default/files/2026-06/AFBI%20advice%20note_eel%20conservation%20target%20compliance_2026.PDF); [AFBI escapement 2024](https://www.daera-ni.gov.uk/sites/default/files/2026-06/AFBI%20information%20note_eel%20escapement%202024.docx_Redacted.PDF); [Irish Times, the Bann](https://www.irishtimes.com/news/shadowy-weedy-water-world-of-eels-1.1099171); [JNCC report 745](https://data.jncc.gov.uk/data/20810981-e500-4207-a1df-b37cd9eb47e1/jncc-report-745.pdf); [FAO, Lough Neagh fleet](https://www.fao.org/fishery/docs/CDrom/aquaculture/a0844t/docrep/009/C2876B/C2876B27.htm); [Marine Institute, eel census](https://www.marine.ie/site-area/areas-activity/fisheries-ecosystems/eel-census); [Poole et al. 2018](https://fishlarvae.org/wp-content/uploads/2017/10/Poole-et-al.-2018_Long-term-variation-in-numbers-and-biomass-of-silver-eels.pdf); [ESB fisheries](https://esb.ie/who-we-are/ask-esb/esb-and-fishery-operations).
- Continent and Baltic: [ICES 1968 M5](https://www.ices.dk/sites/pub/CM%20Doccuments/1968/M/1968_M5.pdf); [ICES 1974 M3](https://www.ices.dk/sites/pub/CM%20Doccuments/1974/M/1974_M3.pdf); [Dekker, history of European eel fisheries](https://pub.epsilon.slu.se/id/document/19512942); [SLU, Swedish eel fishery](https://pub.epsilon.slu.se/id/document/20367549); [Intrafish, Spakenburg](https://www.intrafish.com/news/a-troubled-fish/1-1-629190).
- North America: [The Eel Deal, Delaware weir](https://roadfood.com/?p=53046); [Upper Delaware Council](https://upperdelawarecouncil.org/?p=740); [Pilgrim Hall, primary sources](https://www.pilgrimhall.org/?p=2022); [Mourt's Relation (Gutenberg)](https://gutenberg.org/files/66359/66359-h/66359-h.htm); [Woods Hole Museum, eels](https://woodsholemuseum.org/oldpages/sprtsl/v21n1-Eel.pdf); [Community Stories, eel fishing](https://www.communitystories.ca/v2/la-peche-a-l-anguille_eel-fishing/story/aboriginal-and-european-techniques/); [Rabaska, Kamouraska](https://www.erudit.org/en/revue/rabaska/2017/v15/n/1041116ar.pdf); [NW Council, Indian fishing](https://www.nwcouncil.org/history/IndianFishing/).
- New Zealand and Australia: [Te Ara, te hopu tuna](https://teara.govt.nz/en/te-hopu-tuna-eeling); [Te Ara, Canterbury lakes](https://teara.govt.nz/node/8562); [ECan, Te Waihora](https://www.ecan.govt.nz/get-involved/news-and-events/2025/tuna-eel-stranding-at-te-waihoralake-ellesmere); [FAR 2014/21](https://fs.fish.govt.nz/Doc/23527/FAR_2014_21_EEL2010-03%20(obj.%202,%20MS7).pdf.ashx); [NZ eel CPUE review](https://fs.fish.govt.nz/Doc/22482/EEL9701%20Eel%20commercial%20fishery%20final.pdf.ashx); [Budj Bim](https://www.visitmelbourne.com/things-to-do/aboriginal-victoria/regional-spotlight-budj-bim-cultural-landscape).
- Diet share: [fish in medieval rations](https://link.springer.com/content/pdf/10.1007/s10152-004-0203-5.pdf).
- Carried from fishing_ladder.md and smokehouse_capacity.md: the Shannon and Iniscarra fykes, the Severn putchers, Celilo, the Fraser Canyon.
- In the repository: the files and lines named under "Read first" and "Code read".

*Current as of 22 Nov 2026.*
