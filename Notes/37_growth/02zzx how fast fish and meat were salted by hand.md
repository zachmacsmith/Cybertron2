---
id: docs/review/37_growth/02zzx_salting_rates.md
kind: note
updated: "2026-11-20"
---
# 02zzx: how fast fish and meat were salted by hand

*note · `docs/review/37_growth/02zzx_salting_rates.md`*


20 Nov 2026, 37.2 (subagent; for whether salting fish and meat stays at 4 kg a unit of work ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]), under [[W-64 Food, weight and work on one basis|W-64]])

Zach (20 Nov): salting is kept for now at its current rate, "flag to follow up. Actually get an agent to check that in the
background." Read-only: no code or data was changed. The web pages were read only through search summaries (the session's network
refused direct fetches of fao.org, herripedia.com, stornowayhistoricalsociety.org.uk and epe.lac-bac.gc.ca), so every figure below
is as a secondary page reports it. Figures marked **estimate** are this note's own arithmetic or judgement.

## 1. The question

Is 2 kg an hour (4 kg a unit of 2 hours) real for one person salting fish or meat by hand in a pre-industrial setting? Which steps
does the real work have (gutting and heading, splitting, salting and packing, turning and repacking over days), how fast was each,
how much salt a kilogram, how long in the salt before it keeps, and what is lost?

## 2. What the engine does now

- `salt fish` (data.py 618): 4 fish and 1 salt make 4 salt fish, 1 unit, anywhere, a basic craft. Done at once: no rack, no wait.
  `salt meat` (data.py 620): the same, 4 meat and 1 salt to 4 salt meat.
- **A fish unit is about 1 kg gutted and headed** (data.py 47, [[D2-258 The food values are put on one physical basis|D2-258]]). It arrives gutted from every catch; gutting has no step and
  costs no work (02zzu_lookup.md, "What binds the keeping of a catch").
- So the engine's 4 kg a unit is **salting and packing alone, on fish already dressed**: 2 kg an hour.
- The weight is kept: 4 kg in, 4 kg out; salt fish has the fresh fish's food a kilogram (0.46).
- Salt: 1 to 4 by weight. A saltmarsh pan gives 1 salt a unit (summer); boiling gives 4 a unit for 4 firewood.
- There is no barrel, cask or tub as an item; nothing about the container binds.
- At this rate a weir's 100 kg night needs 25 units of salting and 25 salt (02zzu_lookup.md): the tightest bind on keeping a catch.

## 3. Real rates by step

Rates per worker-hour. Weights: a Scotch-cure herring barrel held about 700 to 1,100 fish (about 900 typical) and about 113 kg
(250 lb) of fish (Oregon State compendium); so a herring is about 0.11 to 0.15 kg (**estimate** from those two). A Newfoundland
quintal (112 lb of dried fish) was weighed off as 300 lb of split fish fresh from the knife.

| Step | Rate a worker-hour | In kg an hour | Source | Sureness |
|---|---|---|---|---|
| **Herring gutting** (Scotch cure: gills and guts nicked out with one cut; not headed or split) | 40 a minute average, 60 for a skilled crew, 65 to 66 as records: 2,400 to 3,600 fish | **about 300 to 450 kg** of whole herring | Pittenweem timing, 1920s (Old Weird Scotland, citing the Dundee Courier); Highland Archive (Wick); Stornoway Historical Society; a film intertitle (65) | good on fish a minute; the kg is an estimate |
| **Herring crew, all steps** (2 gutters and 1 packer: gutted, roused in salt, packed head to tail in layers with salt between) | 3 barrels an hour a crew at 750 fish (Shetland Museum); a barrel of 1,000 in 15 minutes (Suffolk Archives); 288 barrels in 4 days (Gorleston, "a good week") | **about 110 to 165 kg a person**; the packer alone, salting and packing, 330 to 450 kg | Shetland Museum and Archives; Suffolk Archives, "Following the Fish"; Kate Newland (Museum Stavanger) | fair; the two crew rates disagree by a third |
| **Herring filling up** (after about 10 days the barrel has settled; pickle drawn off, more fish packed in, pickle returned; coopers) | not found | **estimate:** a quarter of a barrel's packing again, a few minutes a barrel | Stornoway Historical Society; Shetland Museum; herripedia (as summarised) | process good; no rate |
| **Cod gutting** (at sea, modern hand gutting) | 240 six-pound cod an hour; 300 for small codling, 150 for large | **about 650 kg** of round fish | FAO-hosted Torry Advisory Note "The Cod" (x5911e) | good (a measured trade figure, 20th century) |
| **Cod splitting** (by hand: opened to the tail, sound bone cut out) | 250 "mediums" an hour (Gloucester, 1903); 3 to 4 quintals an hour at full speed, 3 an hour average (Newfoundland splitters, oral history); 4 to 5 seconds to take out a bone | **about 400 to 550 kg** of split fish (3 to 4 quintals at 300 lb); the summary gives "roughly 1,200 to 1,400 pounds" | Library and Archives Canada, "Splitting Fish" (Hard Racket exhibit; Bulgin 1978); Shorpy (Gloucester 1903) | fair; oral history and one period account |
| **A cod stage crew, all steps** (cut-throat, header, splitter, salter, and often a boy carrying and washing; the splitter sets the pace) | 4 to 5 people at the splitter's pace | **about 80 to 140 kg** of split fish a person | **estimate** from the splitter's rate and the crew (Canadian Museum of History, "Lifelines"; LAC) | estimate |
| **Kench salting** (the salter spreads salt with a shovel and brush over each layer of split fish in a pile) | keeps pace with the splitter | **about 400 to 550 kg** | **estimate**; LAC; DFO "Handling and processing salt cod" | estimate |
| **Repiling, washing and drying salt cod** (piles turned; then washed and spread on flakes, taken up at night, for days to weeks) | not found for the pre-industrial trade | | | the largest labour in salt cod, uncounted here |
| **Artisanal salting and drying, everything** (26 small women-owned firms, 8-hour days, including buying, drying and selling) | 102 person-days a tonne of dried fish | **about 1.2 kg of product, about 3.5 to 5 kg of fresh fish** an hour (estimate: 3 to 4 kg fresh a kg dried) | FAO, "The contribution of post-harvest activities" (openknowledge.fao.org) | fair; the country and year were not in the summary |
| **Salting a pig** (cutting the carcass into flitches and hams; rubbing salt in; laid rind down) | not found as a rate | **estimate:** the first salting 50 to 100 kg an hour (a few minutes a piece); turning and rubbing daily for a month about as much again; so **20 to 50 kg an hour** all in, after the killing and cutting | period farm texts (Wiltshire cure in chestofbooks, "How to cure bacon"; Cobbett, foodsofengland); no measured rate | estimate |

What this says:
- **The salting and packing step alone** went at **300 to 500 kg an hour** for a trained packer or salter: 150 to 250 times the
  engine's 2 kg.
- **With the dressing included** (gutting, heading, splitting), a trained crew still put through **about 80 to 165 kg a person an
  hour**.
- **Gutting and splitting are the real labour**, not the salting. In the herring crews two of every three hands gutted; in the cod
  stages the splitter's knife set the pace for the salter.
- **The slowest all-in figure found**, small artisanal firms counting drying and selling, is about 3.5 to 5 kg of fresh fish an
  hour: still above the engine's 2 kg, and it counts far more than salting.
- These are specialist rates (piece-work crews, paid by the barrel or the quintal). An untrained villager would be slower. A
  **non-specialist** salting fish already gutted into a tub is put at **50 to 150 kg an hour**, and gutting and heading 1 kg fish
  at about a minute each at **30 to 60 kg an hour** (both **estimates**).

## 4. Salt a kilogram

| Cure | Salt to fish or meat by weight | Source |
|---|---|---|
| Herring, barrel (Scotch cure) | 25 to 30 lb a 100 lb (1 to 3.3 or 4); "about 100 pounds of salt each barrel" of about 250 to 320 lb (1 to 2.5 to 3) | Oregon State seafood compendium, ch. 1; Cecelski, "Herring week: salt" |
| Baltic herring, dry-salted (a trial) | 20 to 30 kg a 100 kg kept well; under 20 it went off slowly | Nikkilä (journal.fi, Acta Agriculturae Scandinavica) |
| Dry salting in general (FAO) | 30 to 40% of the prepared weight; a strong cure about 30 kg a 100 kg | FAO, "Fish salting 101"; a reproduced handling text |
| Cod, heavy cure (kench) | at least 55 lb a 100 lb of split fish (about 1 to 1.8); trials at 60 kg a 100 kg | DFO, "Fishing for quality: handling and processing salt cod" |
| Cod, light salted (Newfoundland shore) | "one hogshead to ten quintals" as the least to hold it till drying | DFO-hosted history of the inshore fishery (as summarised; the hogshead's weight not given) |
| Bacon and pork, farm dry cure | 8 to 10 lb a 100 lb (about 1 to 10 or 12), turned and re-rubbed | US farm cures, 1950 (Saturday Evening Post); period recipes |
| Pork, crude long keeping | "entirely covered with salt" for six weeks | New Zealand farm note, 1913 (Papers Past) |

The engine's 1 to 4 is right for barrelled herring and light-salted fish. It is half a heavy cod cure. For meat it is generous: a
farm dry cure used a third to a half of it.

## 5. Time in the salt, and losses

- **Herring:** the barrels settled about 10 days ("a few days" in some accounts) as the fish shrank in their own pickle. Then they
  were filled up and the pickle returned. Then the barrel was branded and kept for months.
- **Cod:** heavy salting in bulk ran about 20 days to a month (Memorial University, Dictionary of Newfoundland English). Light
  salted fish lay only a short time in salt bulk (no day count found). Then washing and drying on flakes for days to weeks.
- **Dry-salted herring** reach their lowest weight within about two days, and lose more weight the more salt is used (Nikkilä).
- **Bacon:** a day a pound in a dry cure, two to three days a pound in brine; turned daily for a month in the Wiltshire cure.
- **Losses by weight:**
  - herring shrink enough in 10 days that a barrel needs topping up, a part in four to five (**estimate** from the filling up);
  - cod: 300 lb of split fish make 112 lb of dry fish (37%);
  - round cod to fully salted, a factor of 2.5 to 3.1 (NAFO conversion studies, 1953 to 1956): 32 to 40% of the round weight;
  - one older example loses 25 kg of 100 kg round in the salting and 25 kg more in the drying (NOAA Fishery Bulletin).
- **From gutted weight, wet-salted fish is about 70 to 85%** (**estimate**). The engine keeps it at 100%, but gives salt fish the
  fresh food value a kilogram, so the food kept is about right.

## 6. Recommendation

- **4 kg a unit is too slow by one to two orders of magnitude.**
  - For salting alone, the step the engine counts, even a slow non-specialist is 25 or more times faster.
  - Counting gutting, a trained crew is 50 to 80 times faster.
  - [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]'s recommendation ("nearer 10 to 20 kg an hour") is the low end of the evidence, not its middle.
- **Proposed figure: 40 fish and 10 salt make 40 salt fish in a unit** (20 kg an hour), with the same for meat. That is meant to be
  a villager's rate **with the gutting folded in**:
  - it sits at the bottom of the non-specialist estimates;
  - it is about a sixth of a trained crew's rate;
  - a weir's 100 kg night becomes 2.5 units of one person's day and 25 salt: something a household can keep up with if it has the
    salt.
  - If 37.4's run nights need a harder bind, 20 to 30 kg a unit (10 to 15 kg an hour) is still defensible for clumsy hands. Below
    about 10 kg an hour nothing found supports it.
- **Then salt binds, as it really did.** In every trade read here, the limit on keeping a glut was salt, barrels and hands enough to
  gut the catch before it spoiled, not the salting itself.
  - The engine's salt is already scarce: a pan gives 1 a unit in summer, boiling 4 a unit for 4 firewood.
  - At 1 to 4, salt is the bind once the work is fast.
  - There is no barrel or cask. Barrels could join the material chain (a cooper's craft from timber); that would be an entry in
    `docs/engine_gaps.md` or OPEN.md, not part of this change.
- **Salt meat's salt could drop to 1 to 8** (a farm dry cure is 1 to 10 or 12; a ship's hard cure more). Keep fish at 1 to 4.
- **Gutting: do not add a separate verb.** The fish unit is gutted weight for every use (eaten fresh, smoked, dried, salted). Two
  places to count it, the second preferred:
  - in each keeping technique's rate: the 40 a unit above already includes it;
  - as a small cost on the catch itself, about 1 unit a 50 to 100 kg landed (**estimate**), so that fresh fish pays it too.
  - A separate whole-fish good would only be worth it if offal, roe or oil came into the world (cod liver oil, herring roe).
- **Time in salt** is a second-order fix. The engine makes salt fish keep at once, where the real cure took 10 days (herring) to 3
  or 4 weeks (heavy cod), with one repacking. Salted fish was safe in its pickle from the first day or two, so for keeping the
  engine's shortcut is mostly harmless. If modelled, it would be a rack-like wait with one tending ("filling up") at about 10
  nights, like the smokehouse's.

**How sure:**
- **High** that 2 kg an hour is far too slow for salting, and that gutting and splitting, not salting, were the labour.
- **Fair** on the professional rates: herring 40 to 60 a minute; crews about 1 barrel a person-hour; cod 3 to 4 quintals a splitter
  an hour. These come from museum, archive and oral-history pages, read only as summaries.
- **Low** on non-specialist and meat rates, which are estimates.
- No pre-1700 per-hour figure was found. The medieval Scania and Dutch buss trades are described (women gutters, salt from Lüneburg)
  but not timed.

## Sources

- Highland Archive Service, "Wick: history of a harbour: herring gutters":
  https://www.highlifehighland.com/archives/highland-archive-service/online-exhibitions/wk-history-of-a-harbour/herring-gutters
- Old Weird Scotland, "66 hpm" (Pittenweem timing): https://oldweirdscotland.com/66-hpm/
- Stornoway Historical Society, "Work of the herring girls": https://stornowayhistoricalsociety.org.uk/work-of-the-herring-girls/
- Shetland Museum and Archives, "Preparing for the herring":
  https://shetlandmuseumandarchives.org.uk/blog/herring-blog-photos-from-archive?page=5
- Suffolk Archives, "Following the Fish": https://suffolkarchives.shorthandstories.com/following-the-fish/
- Kate Newland, "Doon to Lerwick and up to Yarmouth" (1999):
  https://www.museumstavanger.no/uploads/sm/1999-KATE-NEWLAND-Doon-to-Lerwick-and-up-to-Yarmouth.pdf
- herripedia, "Herring lasses": https://www.herripedia.com/herring-lasses/
- Oregon State University, Seafood compendium ch. 1 (acidified, fermented and salted fish):
  https://seafood.oregonstate.edu/sites/agscid7/files/snic/compendium/chapter-1-acidified-fermented-salted.pdf
- D. Cecelski, "Herring week, day 9: salt": https://davidcecelski.com/2018/04/02/herring-week-day-9-salt/
- sizes.com, herring barrel: https://www.sizes.com/units/barrel_herring.htm ; Wikipedia, "Cran (unit)":
  https://en.wikipedia.org/wiki/Cran_(unit)
- FAO / Torry Advisory Note, "The Cod": https://www.fao.org/4/x5911e/x5911e01.htm
- Library and Archives Canada, "Splitting fish (continued)":
  https://epe.lac-bac.gc.ca/100/205/301/ic/cdc/fisheries/hardracket_05.asp ; "Newfoundland salt fisheries":
  https://epe.lac-bac.gc.ca/100/205/301/ic/cdc/fisheries/student.asp
- Shorpy, "Fish in a barrel: 1903" (Gloucester splitters): https://www.shorpy.com/node/22497
- Canadian Museum of History, "Lifelines": https://historymuseum.ca/cmc/exhibitions/hist/lifelines/lipof01e.html
- DFO, "Fishing for quality no. 4: handling and processing salt cod":
  https://waves-vagues.dfo-mpo.gc.ca/library-bibliotheque/40600476.pdf
- Memorial University, Dictionary of Newfoundland English, "heavy salted":
  https://openpolar.no/Record/ftmemorialunivdc:oai:collections.mun.ca:elrcdne%2F33699/Details ; "split":
  https://www.heritage.nf.ca/dictionary/azlist/pages/4522.html
- Newfoundland quintal and the weighing-off of split fish: https://electriccanadian.com/history/newfoundland/newfoundland/chapter14.htm
- NAFO conversion factors (Peters): https://www.nafo.int/Portals/0/PDFs/Studies/s13/peters.pdf
- Nikkilä, dry salting of Baltic herring: https://journal.fi/afs/article/download/71305/33102/95388
- FAO, "Fish salting 101": https://www.fao.org/flw-in-fish-value-chains/resources/articles/Fish-salting-101-What-you-need-to-know/en
- FAO, "The contribution of post-harvest activities":
  https://openknowledge.fao.org/server/api/core/bitstreams/bfd73ff8-d11c-4ef6-a0c0-4531c6011f36/content
- NOAA Fishery Bulletin (salted and dried cod yields): https://spo.nmfs.noaa.gov/sites/default/files/pdf-content/fish-bull/fb4.193.pdf
- Bacon cures: https://chestofbooks.com/food/recipes/London/How-To-Cure-Bacon.html ; https://foodsofengland.info/cobbettsbacon.html ;
  https://www.saturdayeveningpost.com/2018/03/4-farm-recipes-home-cured-ham-1950/ ;
  https://paperspast.natlib.govt.nz/newspapers/PGAMA19130311.2.45
- Scania market: https://en.wikipedia.org/wiki/Scania_market
