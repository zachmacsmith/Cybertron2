---
id: docs/review/37_growth/02zzzh_hunt_fish/smokehouse_capacity.md
kind: note
updated: "2026-11-22"
---
# How much a smokehouse held, how long it took, and what the engine's racks should hold

*note · `docs/review/37_growth/02zzzh_hunt_fish/smokehouse_capacity.md`*


22 Nov 2026, 37.2 (subagent). Research note for Zach's question on the smokehouse's capacity. No code changed.

Zach (22 Nov): "does smoke house need to hold more capacity? Compare to reality? I imagine it might be way too low rn?"

**Read with:** the engine audit ([engine_audit.md](engine_audit.md): the keeping rows), the fishing ladder
([fishing_ladder.md](fishing_ladder.md): what a run night offers), the lookup note's keeping section
(`docs/review/37_growth/02zzu_lookup.md`, "What binds the keeping of a catch"), the smokehouse's design
(`docs/cybertron2/proposals/river_and_water.md` §4a), and the code (`cybertron2/engine/data.py:272-277` the fitting, `:621-638`
the verbs, `:832-836` PHYSICS `smokehouse`; `cybertron2/engine/keeping.py`; `cybertron2/engine/verbs.py:790-831`).

**How the sources were read.** I used web search only. Every page fetch failed because the session's network does not allow the
host: www.fao.org, epe.lac-bac.gc.ca, www.herripedia.com and www.djo.org.uk through the fetch tool, and fisherybulletin.nmfs.noaa.gov,
repository.library.noaa.gov, en.wikipedia.org and archive.org through curl. So every figure below comes from search-result
summaries and abstracts, not from full texts, and I quote each figure as the summary gives it. The primary manuals (FAO's West
African smoking guide and Technical Paper 634, the Torry Advisory Notes 9, 48 and 82, and US Fishery Leaflet 196) were seen only
in fragments. Anything marked **(est.)** is my own estimate, not a source.

**The engine's basis:** a fish unit is about 1 kg gutted ([[D2-258 The food values are put on one physical basis|D2-258]]), a unit of work is 2 hours, the year has 32 days ([[D2-209 Brief 5 (river and water) is built|D2-209]]), so a
real day becomes about 1/11 of an engine night. Daily work rates stay real. A space is about 5 m² of floor ([[D2-154 One unit of space at every level|D2-154]],
`spec/economy/buildings.md`). A firewood unit is about 60 kg of wood (a quarter of a timber's 240 kg; withies_wood_materials.md,
from the 02z model). Real values within about 20% are kept, and every departure is named with its factor ([[D2-259 The food values are anchored on real values|D2-259]]).

---

## 0. In brief

- **Zach is right: the racks hold far too little.** The engine's set of smoke racks holds 40 kg on 3 spaces (about 15 m²), which is
  about 2.7 kg per m² of floor. A real household or camp smokehouse of 7 to 10 m² held a few hundred kg at once (est. 30 to 70 kg
  per m²). Herring houses and tray kilns held more. Per square metre the engine is **about 10 to 25 times low**. Per real day of
  throughput it is **about 15 to 40 times low**, because its 3-night batch also stands for about a month of real time.
- **The batch time is a red herring's, not a salmon's.** At 1/11, 3 nights is about 33 real days. That matches a hard "red" cure
  for export (3 weeks to a month in the 19th century, up to 10 to 12 weeks today). The keeping smoke the sources describe for
  salmon took 4 days to about 2 weeks. West African hard smoking at high heat took 2 to 3 days and kept 6 to 9 months. Hot
  smokes (kipper, bloater, eel, Bornholm herring) took hours and kept only days.
- **What bound a real glut was hands, wind and fuel, not the hut.** A Fraser Canyon woman cut and hung 50 to 60 salmon a day, and
  "processing took longer than catching". A glut was split: wind-dried on open pole racks first and finished in the smokehouse, or
  salted first (red herring, bloaters, Maine herring) and then smoked. Places that lived on the trade built many houses (Grand
  Manan had about 300 smokehouses).
- **Proposal** (§8): racks hold **about 250 fish a space** (50 kg/m², the middle of the estimate). The fitting becomes 2 spaces
  holding 500, the size of a real smoke hut. A lot smokes for **1 night** (about 11 real days, against about 2 weeks: inside the
  20%, and the engine's floor). Hanging costs **1 unit per 30 fish**, the Fraser rate. Fuel is **1 firewood per 60 fish hung**
  (about 1 kg of wood per kg of fish). Tending stays 1 unit a night, a departure named for the compressed calendar. The work and
  the wood then bind a glut, as they did in reality, and the hut's volume no longer does.

---

## 1. The engine now

| What | Value | Where |
|---|---|---|
| smoke racks (a fitting) | 3 spaces, 2 timber, 2 units, basic, in a building of its own; `racks: 1` | data.py:275-277 |
| room on the racks | the number of fittings x `racks` x the technique's batch (40), less what still hangs; each act's lot is its own rack pile with its own nights | keeping.py:38-47, verbs.py:790-831 |
| smoke fish / smoke meat | up to 40 a batch (whatever is to hand), **1 unit whatever the size**, 3 nights of tended fire, into half the weight | data.py:623-635 |
| tend the smoke | 1 unit a day, or the fire dies that night and the batch pauses and spoils at the open rate | data.py:636-638, keeping.py |
| fuel | `fuel` 0.5 heat a night burning, which is 1 firewood (heat 0.5) | data.py:835, :44 |
| hearth rack (dry fish, dry meat) | 8 a batch, 3 nights | river_and_water.md §4a |

So one set of racks keeps **40 kg per 3 nights, about 13 kg a night**. That is **about 1.2 kg per real day** (3 nights at 1/11 is
about 33 real days). It burns **3 firewood (about 180 kg of wood) per 40 kg: about 4.5 kg of wood per kg of fish**. Loading costs
1 unit (2 h) per 40 kg, so **about 20 kg an hour**, and the gutting is free because the unit arrives gutted (02zzu_lookup).

In the runs world a peak night at Lowstrand offers 333 kg and a weir section takes 100 (02zzu_lookup). The bot runs found a
household keeping 58 to 300 kg against a glut of several hundred kg a run night. A peak night needs about 8 smokehouse-nights.

---

## 2. How much a smokehouse held at once

| Where, what | Held at once | Floor or rack | Per m² or per rod | Source |
|---|---|---|---|---|
| Northwest Coast, a typical First Nations smokehouse | not given (hundreds of salmon a family a season) | "a wooden building about nine feet square" (about 2.7 m square, about 7.5 m²) | est. 200 to 500 kg: 3 tiers of poles about 0.3 m apart, a split salmon (about 2 kg, est.) every 0.25 m, gives about 270 fish (**est.**); so 30 to 70 kg/m² (**est.**) | LAC "Preserving" page, via search summary |
| Interior Alaska camp (modern) | not given | a 7 ft x 11 ft plywood smokehouse (about 7 m²) beside an 8 ft x 16 ft drying rack | | smokingmeatforums anecdote |
| Tlingit, modern family smoking | 45 to 50 lb of smoked salmon a batch (20 to 23 kg; about 40 to 60 kg fresh, est.) | | | Sitka Seafood Market |
| A modern First Nations smokehouse | 100 to 200 fish **a year** | | | cost analysis cited in IndigiNews, via search summary |
| Maine and New Brunswick herring houses (19th to 20th century) | "a horse will hold 45 sticks or about one barrel of herring" | sticks about 40 in (1 m) long, hung in vertical bays from the floor fires to the roof | **25 to 35 herring a stick**; a barrel about 90 kg (est.), so about 2 kg a stick (est.); at about 10 sticks a metre of rack and 6 to 10 tiers, 100 to 200 kg/m² of floor (**est.**) | US Fishery Leaflet 196 (fragments); Maine Memory, McCurdy smokehouse |
| Lowestoft, a small working red herring smokehouse today | "190 kg of red herring hanging from the spits" | not given | | EADT feature |
| 19th-century Yarmouth red herring | | "spits ... round rods made of fir, about 4 ft long"; fish hung by the mouth and gills | | search summary of a 19th-century description (page not opened) |
| Chorkor oven (Ghana, improved; hot to hard) | **up to 18 kg a tray x 15 trays, about 270 kg a load** | a mud or brick box, two chambers (dimensions not confirmed) | 18 kg a tray | Practical Action, *Smoked foods* |
| AFSMO-150 (improved Chorkor type) | 150 kg fresh a batch, **3 hours** | | | CSIR Food Research Institute, Ghana |
| Nigerian tray kiln | 40 to 52 kg (190 to 198 catfish), 6 trays | trays about 0.43 x 0.33 m in another design | 20 to 28 fish a tray | Oduntan 2019; a Nigerian design paper |
| Gjerstad kiln (Lake Turkana) | 75 to 100 kg hot smoked in about 2 hours | | | FAO, via search summary |
| Torry mechanical kiln | 375 kg capacity | | | Torry Advisory Note 82, via search summary |
| German brick herring kilns (early 20th century) | "400 cwt, or 20,000 lb, of herrings per 24 hours" a kiln | | | US Fishery Leaflet 208 (garbled OCR) |
| Ghana traditional oven | 528 kg a session of 53 hours | | | Tropical Conservation Science 2019, Ghana mangrove fuel study |

**Reading.** Every source that gives a load puts a single smoking unit in the range of **tens to hundreds of kg**, and a household
or camp house in the low hundreds. On area, a small house hung in a few tiers comes to about **30 to 70 kg per m² of floor**, and a
tall herring house to 100 to 200 (both **est.**, from the stick and pole counts). For a rod or speet the figure is **25 to 35
herring**, about 2 to 5 kg depending on the fish (herring weight est.).

---

## 3. How long it took, and how long it kept

| Product | Smoking | Kept | Source |
|---|---|---|---|
| Hot smoke: Bornholm herring | about 2 h of drying over flames, then about 2 h in dense smoke | days (sold fresh) | bornholm.info (Allinge Røgeri); Royal Danish Academy report |
| Hot smoke: eel | several hours hung to dry, then 1 to 3 h at 60 to 80 °C; 100 kg fresh gives about 60 kg smoked | days chilled; a drier kiln product about 8 months at 30 to 35% moisture | meatsandsausages; fishconsult (Dutch eel); ICAR eel study |
| Hot smoke: tray kilns | 2 to 3 h (Gjerstad, AFSMO); bonga 4 to 13 h | | FAO bonga paper; CSIR |
| Cold smoke: kipper (Craster) | 14 to 18 h over oak, after brining | days | Craster kipper accounts |
| Cold smoke: bloater | dry salted 6 to 24 h, smoked 4 to 16 h | about 1 to 4 days | US Fish Bulletin; FAO storage table |
| Hard smoke, West Africa | **2 to 3 days**, down to 10 to 15% moisture | **6 to 9 months** | FAO, artisanal fish smoking |
| Ghana traditional oven, hard smoke | 53 h a session | | Ghana mangrove fuel study |
| Salmon, Northwest Coast | "half-smoked salmon requires one to three days smoking; fully smoked salmon may require four or more days"; poles and racks 2 to 4 days "depending on the desired taste" | half-smoked stays soft and needs further keeping; fully smoked is dry and keeps "in a cool, dry place" over winter | UBC text; LAC pages |
| Salmon, Gitksan (wilpsihon) | ts'al half-smoked about 2 days after thinning, then **about two more weeks** hung from the smokehouse ceiling, then to a root cellar | the winter | LAC "Preserving" page |
| Salmon, interior Alaska | strips rotated round the house "until fully dehydrated ... a few days up to two weeks"; a 14-day cure; or 10 days to 2 weeks on racks, then up to 7 days in the smokehouse | the winter | Chena village marker; Alaska camp accounts |
| Salmon, Fraser Canyon (wind, no house) | filleted fish hung in the canyon wind **3 to 4 days** | the winter, and traded | SFU archaeology publication; Keatley Creek project |
| Red herring, 19th-century Yarmouth | "three weeks or a month, depending on whether the fish were for home use or export" | "many weeks or months" (FAO) | search summary of a 19th-century description; FAO |
| Red herring, heavy then light smoke | heavy smoke up to 2 days, then lighter smoke up to 6 weeks | keeps very well | cooksinfo |
| Red herring, Lowestoft today | salted up to 3 days (turned daily, "rousing"), smoked up to 10 weeks; another house about 12 weeks | | EADT; herripedia (Waveney Valley) |
| Hard-smoked herring, Magdalen Islands | a month, or 2 to 3 months, in the rafters | | Saltscapes; Économusée de la boucanerie |

**Reading.** There are three classes:
- **Hot smoking takes hours** and the fish keeps days. It is for eating soon or for market.
- **A keeping smoke for salmon or eel takes about 4 days to 2 weeks** under a low fire, often after wind-drying or a half-smoke.
  The fish is dry and keeps through the winter.
- **A hard cure for trade takes 3 weeks to several months**, after heavy salting, and keeps for months.

The engine's smoked fish keeps for months (spoil 0.005), so it is the second or third class.

**An aside on the weight ratio** (not asked): the engine smokes to half the weight. Fresh fish is about 72 to 75% water, and hard
smoked fish 10 to 15%, so a full hard smoke leaves about 30 to 35% of the weight (**est.**, from the FAO and catfish moisture
figures). A hot-smoked eel leaves about 60%. The engine's 0.5 sits between a half-smoke and a hard smoke.

---

## 4. Fuel per kg

| Kiln | Wood per kg of fish | Source |
|---|---|---|
| Ghana traditional oven | 1,205 kg of wood for 528 kg of fish: **about 2.3 kg/kg** | Ghana mangrove fuel study |
| Ghana cinderblock (improved) oven | 122 kg for 160 kg in 5 h: **about 0.76 kg/kg** | same |
| AFSMO-150 | 39.5 kg for a 150 kg batch: 0.33 kg per kg of *smoked* fish | CSIR |
| Torry mechanical kiln | about 13 kg an hour for a 375 kg kiln: **about 0.2 kg/kg** if a cycle is about 6 h (cycle length **est.**) | Torry Advisory Note 82 |
| FAO, all smoked fish | **0.2 to 16 kg/kg** | FAO table, via search summary |
| A Ghana kiln comparison | Chorkor 6 g/kg (units look wrong; not used) | JSFA 2024, via search summary |

I found no measured figure for the long low smoulder of a salmon house or a red herring house. A smoulder of chips and rotten wood
burns slowly, but it burns for one to several weeks. I put it at **about 1 to 2 kg of wood per kg of fish (est.)**, between the
improved and the traditional West African ovens. **The engine's 4.5 kg/kg is about 2 to 4 times the traditional figure.**

---

## 5. The work per kg

- **Cutting and hanging salmon:** "on average, a woman could process about 50 to 60 salmon per day", and in the Fraser Canyon "it
  was the women's work to butcher and dry the salmon, and this took more time than the catching of salmon": men caught hundreds
  in an hour but tired after half an hour (SFU archaeology publication). At about 2.5 kg a fish and a 10-hour day (both **est.**),
  that is **about 13 to 15 kg an hour, or about 25 to 30 fish units a unit of work**, splitting included.
- **Stringing brined herring on sticks:** one stringer did 500 to 1,000 sticks a day at 25 to 35 a stick (Fishery Leaflet 196, as a
  search summary states it). That is a specialist on small, already-brined herring, and very fast (**est.** about 90 to 250 kg an
  hour at 70 g a fish).
- **Gutting herring for salt:** 40 a minute on average, 60 to 65 for an experienced gutter (Scottish herring girls; a 1924
  Pittenweem timing). This is gutting only.
- **Tending:** a smoulder was watched and fed through the day and night: fires on the floor with windows set for the draught
  (Maine), fish moved round the house as they dried (Chena), and bonga turned often. I found no hours figure. **About 1 to 3 hours
  a day for a single house (est.).**
- **Reading:** the hanging is quick, and the cutting is the work. The engine's 1 unit for 40 (about 20 kg an hour, with gutting
  free) is about 1.3 to 1.5 times the Fraser rate. That is outside 20%, and becomes a large gap once a batch is bigger than 40 at
  the same 1 unit.

---

## 6. How a glut was handled

1. **Dry in the open first, smoke to finish.** Fraser Canyon salmon were wind-dried on pole racks for 3 to 4 days, with no house at
   all. Alaskan practice dried 10 days to 2 weeks on racks and then smoked up to 7 days. The Gitksan half-smoked and then hung the
   fish a further two weeks. The house took the finishing, and the open rack took the bulk.
2. **Salt first, then smoke.** Red herring were salted up to 3 days before the spits, bloaters dry-salted 6 to 24 h, and Maine
   herring brined. At Yarmouth most herring was dry-salted "white", and only some, from about 1300, was smoked "red" (Cambridge
   summary). Lowestoft favoured red (Historic England).
3. **More houses, and bigger ones.** Grand Manan had about 300 smokehouses and a thousand workers by the late 19th century, and was
   the largest supplier in the world by 1884. Yarmouth's works had "a long range of smoke houses" (Tower Curing Works, 1880) and
   five smoke chambers off one passage (Trinity Place). Seal Cove keeps 54 such buildings.
4. **More hands.** The household needed enough women to keep up with the men's catch (SFU), and the herring trade moved crews of
   gutters from port to port.
5. **A quick smoke to sell.** Hot smoking (Bornholm, eel, kipper, bloater) turned a catch into a product within a day, for market,
   not for the winter.

---

## 7. The comparison

| | Engine now | Real (household or camp smokehouse) | Factor |
|---|---|---|---|
| Held at once, per m² of floor | 2.7 kg (40 on 15 m²) | 30 to 70 kg (**est.**, §2) | engine x0.04 to x0.09 |
| Held at once, one unit | 40 kg | 200 to 500 kg in a 7 to 10 m² house (**est.**); tray kilns 40 to 270 kg; a small herring house 190 kg | x0.1 to x0.2 |
| Batch time, real days | about 33 (3 nights) | keeping smoke 4 to 14 days; hard red cure 21 to 30 and more | 2 to 3 times long for salmon or eel; about right for a red herring |
| Throughput a real day | about 1.2 kg | 200 to 500 kg / 4 to 14 days: about 15 to 100 kg (**est.**) | x0.01 to x0.08 |
| Fuel | about 4.5 kg of wood per kg | 0.2 (Torry) to 2.3 (Ghana traditional); smoulder est. 1 to 2 | 2 to 4 times high |
| Hanging work | 20 kg an hour, any batch size | 13 to 15 kg an hour with splitting | x1.3 to x1.5 |
| Tending | 1 unit a night (each night is 11 real days) | est. 1 to 3 h a real day | the compression's cut (below) |

The capacity gap is not one factor but two multiplied: the floor holds about a tenth to a twentieth of the real load, and the batch
takes two to three times the real keeping-smoke time.

---

## 8. The proposal (for Zach; nothing decided)

| Lever | Now | Proposed | Real anchor | Factor and reason |
|---|---|---|---|---|
| **Racks' hold** | 40 on 3 spaces | **250 fish a space**; the fitting at **2 spaces holding 500** | 50 kg/m², the middle of the est. 30 to 70; a real hut of 7 to 10 m² | x1 on the middle estimate. 2 spaces, because a real smoke hut is 7 to 10 m², not 15. (Alternative: keep 3 spaces and hold 750) |
| **Batch time** | 3 nights | **1 night** a lot | a keeping smoke of 4 days to about 2 weeks, /11 = 0.4 to 1.3 nights | 1 night is about 11 real days, against the sources' about 2 weeks: x0.8, inside 20%, and the engine's floor |
| **Hanging work** | 1 unit for up to 40 | **1 unit for up to 30**; a full set takes about 17 units | Fraser: 25 to 30 fish units a unit of work with splitting | x1. The racks fill over several acts, and each act's lot keeps its own night |
| **Fuel** | 1 firewood a night (about 4.5 kg/kg) | **1 firewood per 60 fish hung** (about 1 kg/kg); a full set 8 to 9 firewood | 0.2 to 2.3 kg/kg; smoulder est. 1 to 2 | x0.5 to x1 on the smoulder estimate. It is a lever if fuel should bind harder: up to 2 kg/kg is still real |
| **Tending** | 1 unit a day | **unchanged** (1 unit an engine night) | est. 1 to 3 h a real day for about 11 real days, which would be 11 to 33 h | **a named departure: x0.1 to x0.2.** A compressed calendar with real daily work rates cannot carry a duration's daily chores whole. The fire-dies-if-untended rule keeps it a real chore |
| **smoke meat** | as fish | the same values | no meat figures found (Sámi reindeer smoked in the lávvu, no times or loads) | **est.**: by analogy with fish |

**What it changes in the runs world (est., by arithmetic, not run):**
- A peak night's 333 kg at Lowstrand fits one set of racks, with room for most of a second night.
- Hanging the 333 kg takes about 11 units, about 2 person-days at 5 to 7 units a day.
- The fire takes about 5 to 6 firewood.

So the binding moves from the hut to the hands, the wood and the fresh fish spoiling while it waits for hands (0.30 a night).
That is the real picture (§5, §6). One set now keeps about 500 kg a night where it kept 13. Salt, the hearth rack and a second
smokehouse stay useful because the hands to hang the fish run out before the racks do.

**Engine work it needs (for the builder; not done):**
- **The racks' hold must be a number of the fitting's own** (`holds`). Today room on the racks is fittings x `racks` x the technique's
  batch (keeping.py:38-47), so raising the batch to 500 would also make one 1-unit act hang 500 kg.
- With `holds`, the act's batch stays the work rate (30), and the racks hold many lots, each with its own night count. That already
  holds per act: each act is its own rack pile (verbs.py:809-816).
- The fuel per night should follow what hangs (PHYSICS `smokehouse.fuel` scaled by kg on the racks), not be flat a night.
- The `does` and `manual` texts (data.py:277, :627-629, :633-635) and keeping.py's docstring all say "40" and "3 nights".
- The tests in brief 5's gate ("a 40-eel run loses under 10% through a smokehouse") would be re-pinned in kg.

**A hard red cure** (3 weeks to months, salted first, keeping a year, for trade) is a different product from the keeping smoke. If a
world wants it, a separate `hard smoke` lot of 3 nights after salting would carry today's 3 nights at its real length (21 to 33 real
days, /11 = 2 to 3 nights). Today's 3 nights is that product's time, put on the wrong product.

---

## 9. What is estimate, and open questions

**Estimates:**
- the per-m² loads (30 to 70 kg for a tiered hut, 100 to 200 for a herring house): from stick and pole counts and my spacing
  assumptions;
- the weight of a split salmon (about 2 to 2.5 kg) and of a smoking herring (70 to 250 g);
- a herring barrel at about 90 kg;
- the smoulder's fuel at 1 to 2 kg/kg;
- the tending at 1 to 3 h a day;
- the Torry cycle length;
- the hard-smoke weight ratio.

**Sourced, but only from search summaries:**
- the 25 to 35 herring a stick, 45 sticks a horse and 500 to 1,000 sticks a stringer's day (Leaflet 196, garbled OCR);
- the 19th-century Yarmouth "three weeks or a month" and the 4 ft fir spits (the source page was not opened);
- the Fraser 50 to 60 salmon a woman's day (one secondary source).

**Open questions for Zach:**
1. Should the racks hold their real load (about 250 a space) and let the work and the wood bind a glut, or be kept low (a named
   factor below 1) so that the hut binds too? The sources say the hut was not the limit.
2. Should the fitting be 2 spaces (a real hut) or 3?
3. One keeping smoke at 1 night, or that and a hard cure at 3 nights after salting (§8)?
4. Tending at 1 unit an engine night is a departure of x0.1 to x0.2. Is that acceptable as the compression's cut, or should a
   smokehouse night take 2 tends?
5. Not asked: the same 1/11 argument puts the hearth rack's 3 nights (dry fish, dry meat, 8 a batch) at about a month of real
   time; a real rack in the house smoke dried thin fish or meat in days to about 2 weeks. That is worth the same check.

---

## Sources

All of these were read as search-result summaries; no page could be fetched (see the top of this note).

- Fishery Leaflet 196, *Smoking and pickling herring* (US Fish and Wildlife Service): https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet196.pdf ; catalogue: https://mocat.library.unt.edu/catalog/625-ch427
- Fishery Leaflet 208 (German herring kilns): https://fisherybulletin.nmfs.noaa.gov/sites/default/files/legacy-pdfs/leaflet208.pdf
- US Fish Bulletin (bloaters): https://fisherybulletin.nmfs.noaa.gov/sites/default/files/pdf-content/fish-bull/fb22.1.pdf
- McCurdy smokehouse, Lubec: https://www.maine.gov/sos/maineatlas/explore-the-atlas/mccurdy-smokehouse ; https://maineboats.com/node/4702 ; https://mainememory.net/record/35587 ; https://www.mainememory.net/record/33330
- Grand Manan and Seal Cove: https://www.lonelyplanet.com/pois/1360971 ; https://pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=863
- Magdalen Islands: https://saltscapes.com/food-travel-guide/stories/2537-magdalen-s-herring-smokehouse.html ; https://artisansaloeuvre.com/en/artisans/economusee-de-la-boucanerie/
- Lowestoft red herring: https://www.eadt.co.uk/news/21740093.food-farming-feature-historic-smokehouse-keeps-herring-tradition-alive/ ; https://www.herripedia.com/?p=2733 ; https://www.herripedia.com/smokehouse-tales-will-buckenham/ ; Historic England, Whapload Road: https://historicengland.org.uk/research/results/reports/7747/311%E2%80%93333WhaploadRoadLowestoftSuffolk%E2%80%93HistoricAreaAssessment ; https://historicengland.org.uk/listing/the-list/list-entry/1467786
- Yarmouth: https://www.greatyarmouthmercury.co.uk/lifestyle/21026203.magazine-told-tales-red-herrings-towns-fishing-trade/ ; Tower Curing Works: https://historicengland.org.uk/listing/the-list/list-entry/1096791 ; Trinity Place: https://nhe.esdm.co.uk/Monument/MNF29038 ; Cambridge summary: https://resolve.cambridge.org/core/books/abs/catch/going-beyond-natural-local-ecosystems-ii/CBD0BB990012923BA30267E881F0BD18 ; *All the Year Round* (speets, oak): https://djo.org.uk/all-the-year-round/volume-ii-new-series/page-131.html
- Red herring smoking: https://www.cooksinfo.com/red-herrings ; FAO storage note (Torry): https://www.fao.org/4/x5925e/x5925e01.htm
- Craster kippers: https://en.wikipedia.org/wiki/Craster_kipper ; https://www.countrylife.co.uk/food-drink/kipper-smoker-lot-lads-made-undress-outside-get-home-176963
- Torry Advisory Notes: https://emuseum.aberdeencity.gov.uk/objects/124992/torry-advisory-note-no48-kippers ; https://emuseum.aberdeencity.gov.uk/objects/124953/torry-advisory-note-no9-smoked-white-fish-recommended-prac
- Bornholm: https://bornholm.info/en/?p=8547 ; https://royaldanishacademy.com/sites/default/files/project-downloads/venarcular_architecture_final.pdf
- Eel: https://fishconsult.org/?p=11112 ; https://meatsandsausages.com/fish/smoked-fish/eel ; https://epubs.icar.org.in/index.php/FT/article/view/60932
- Chorkor and improved kilns: https://samplecontents.library.ph/en-practical_action/Food%20processing/KnO-100642_Smoked%20Foods/page5.html ; https://researchspace.foodresearchgh.org/bitstream/123456789/1045/1/Design_Construction_AFSMO_Improved_Fish_Smoking_Oven_Blay_et%20al.pdf ; https://ugspace.ug.edu.gh/server/api/core/bitstreams/f1f3accf-3ce7-43bd-adb1-62a1e0828866/content ; https://www.fao.org/newsroom/detail/New-fish-drying-technology-boosts-livelihoods-in-Ivorian-towns/en
- Nigerian kilns: https://www.agricultura.mendelu.cz/wcd/w-rek-agriculturaits/fulltexts/ats_2019_1_oduntan.pdf ; https://www.academia.edu/94533197
- FAO artisanal smoking (2 to 3 days, 10 to 15%, 6 to 9 months): https://www.fao.org/flw-in-fish-value-chains/value-chain/processing-storage/artisanal-fish-smoking/appropriate-technology/en ; FAO bonga: https://www.fao.org/4/T3536E/T3536E07.htm
- Fuel, Ghana: https://bioone.org/journals/tropical-conservation-science/volume-12/issue-1/1940082919833300/Potential-Impact-of-Fish-Smoking-on-Mangrove-Resources-in-Southwest/10.1177/1940082919833300.full ; FAO fuel table: https://www.fao.org/4/y9155b/y9155b0c.htm
- Northwest Coast: https://epe.lac-bac.gc.ca/100/205/301/ic/cdc/salmonstory/preserving.htm ; https://epe.lac-bac.gc.ca/100/205/301/ic/cdc/pacificfisheries/techno/natpro.html ; UBC text: https://ubcischool.arcabc.ca/_flysystem/repo-service/2025-03/3966-Extracted%20Text.txt ; https://sitkaseafoodmarket.com/blogs/stories/how-alaskans-smoke-their-salmon ; IndigiNews: https://indiginews.com/?p=23628
- Fraser Canyon: https://archpress.lib.sfu.ca/index.php/archpress/catalog/download/38/11/422?inline=1 ; https://www.sfu.ca/archaeology/museum/exhibits/past-exhibits/keatley-creek/the-project.html
- Alaska: https://www.hmdb.org/m.asp?m=257593 ; https://www.adn.com/rural-alaska/article/kuskokwim-river-fish-camp-smokehouses-fill-fish-and-tradition/2014/07/20/ ; https://www.smokingmeatforums.com/threads/traditional-salmon-smoking-in-alaska.56645/latest
- Herring gutting rates: https://www.highlifehighland.com/archives/highland-archive-service/online-exhibitions/wk-history-of-a-harbour/herring-gutters ; https://oldweirdscotland.com/66-hpm/ ; https://movingimage.nls.uk/film/8201
- Sámi reindeer smoking: https://munin.uit.no/handle/10037/25974
