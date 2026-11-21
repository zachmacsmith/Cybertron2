# The fishing ladder: techniques, gear, works and the water's stocks

21 Nov 2026, 37.2 (subagent). Thread W-73: fishing, hunting and their materials developed together. Read-only: no code or data
changed. Other notes in this folder cover hunting and fowling, fibres and cord, withies, coppice and wood, and the engine audit;
this one names the materials fishing needs and does not research how they are made. Salting rates are in
[02zzx](../02zzx_salting_rates.md).

**Read with:** [water_and_preservation.md](../../../cybertron2/proposals/water_and_preservation.md) §4 (the earlier ladder),
[river_and_water.md](../../../cybertron2/proposals/river_and_water.md) (the runs, the weir, the mill; D2-209, D2-210),
[economy_web.md](../../../cybertron2/proposals/economy_web.md) §2.11, [02zzy2](../02zzy2_fishing_methods_compared.md) (how agents
fished and what the methods paid), [02zzz2](../02zzz2_river_signs_audit.md) (the river's state and its signs),
02zzj parts 03 §7.1 and 10 §1.4. The engine: `engine/data.py` (TECHNIQUES `fish by hand`, `angle`, `fishing rod`, `salt fish`,
`dry fish`, `smoke fish`; BUILDINGS `weir`; WATER_WORKS), `wild/methods.py` (`trap in water`, `net`, SETS), `wild/kinds.py`
(eel, salmon, lamprey, otter; RUNS), `engine/waters.py` (one resident stock per body, D2-229).

**About the sources.** This session's network refused direct fetches (wikipedia, archive.org and the other hosts tried), so every
figure is as a search summary reported it, as in 02zzx. Figures marked **(est.)** are this note's own arithmetic or judgement.
Sources are listed at the end.

**The engine's basis** (used for every conversion): 1 food = 2,500 kcal; a unit of work = 2 hours; 1 fish = 1 kg gutted and
headed = 1,150 kcal = 0.46 food (D2-258); the year is 32 days (D2-209); real values within about 20% are kept, departures named
(D2-259). So **1 kg of gutted fish an hour = 2 fish a unit = 0.92 food a unit.** Whole fish lose about 30% to gutting and heading
(est.: eels and trout about 10 to 20% gutted only, 30 to 35% headed as well).

## The short answer

- **The water holds three foods, not one, and they behave differently.** The **shallows** (small fish, crayfish, yellow eels lying
  up under the banks) are a small stock that a few people strip in days. The **open water** (the resident fish of the river's
  pools or the lake: pike, perch, roach, bream, trout) is larger and needs a line or a net. The **runs** (silver eels down, salmon
  and lampreys up) are huge pulses, reachable only at pinch points and best by traps and the weir. The engine has the runs (built)
  and one resident stock per body (D2-229); hand fishing and the rod both draw on that one stock. Zach's "crayfish vs actual fish"
  is right: the shallows should be their own stock.
- **The ladder is three paradigms, not four rungs** (§2): personal gear added piece by piece (hands, then a line, a spear, a few
  traps, each a little better and each optional); crew gear (the seine and a boat, which need cord in quantity and a crew); and
  fixed works (the weir and the mill's race, a switch to a site that someone holds, worthless without keeping). Kept water (the
  stew and the fish pond) is a fourth, separate line: husbandry and a larder, not more catch.
- **Real rates, per hour of work, rise by about 2 to 4 times a step** (§4): hands in the shallows about 0.1 to 0.3 kg an hour; a
  rod about 0.1 to 0.5; set lines and a line of wicker traps about 0.5 to 3; a seine crew about 0.5 to 5 a person; a weir on a run
  night tens of kilograms a person-hour. What caps each is the stock (a trout brook's km yields only about 15 to 45 kg a year), and
  for the runs, the keeping.
- **Granularity** (§3): five general methods (at the edge with hands, a spear or a hand net; line fishing; set gear: wicker traps
  and set lines; drawing a seine; and the works), three stocks (shallows, open water, runs), plus kept fish. Leave out bow fishing,
  cast nets, the haaf, putchers and stake nets (coast and estuary, later), and poison, which was illegal (or keep it as a misuse
  for later).

## 1. The water and its foods

| Stock | What lives in it | How big (real) | How it renews | Who reaches it |
|---|---|---|---|---|
| **The shallows** (the margins, riffles, undercut banks, the ditches) | small fish (trout parr, minnow, gudgeon, loach), yellow eels in the mud and under stones, crayfish, freshwater mussels | small. A trout brook holds about 100 to 200 kg of fish a hectare: a 3 m brook is 0.3 ha a km, so about 30 to 60 kg a km (est. from the stream figures below) | fast in summer, slow in winter; production about the standing stock a year in trout streams (P/B 0.6 to 1.1) | anyone: by hand, a spear, small traps, crayfish pots |
| **The open water** (pools, the channel, the lake) | pike, perch, roach, bream, chub, trout in pools, yellow eels | larger and spread: lake and lowland-river production of the order of 20 to 150 kg a hectare a year (est., from stream and pond figures); a wide river 2 ha or more a km | moderate | rod and hand line, set lines, nets (seine, gill net); a lake's middle needs a boat |
| **The runs** | silver eels going down (autumn, dark wet nights), salmon and sea trout going up (spates, autumn and winter), lampreys up (spring) | very large and brief: a fishery's yearly render could be 5,000 to 27,000 eels (§4); built in `RUNS` at a real river's size (D2-258) | the eel by recruitment from the sea (b 3.0 in `KINDS`), the salmon by spawners that got past | traps and the weir; hand nets, spears and hands at falls and shallows; the mill race |
| **Kept fish** (later) | fish alive in a keep box, a stew or a pond | a pond's unfed yield is only 30 to 45 kg a hectare a year (§4) | stocked from the wild; the pond drained every few years | the holder |
| The foreshore (coast, later) | cockles, mussels, limpets, crabs | rich: about 1,500 kcal an hour at low tide, only 2 to 3 hours on about 10 days a month (Pinnacle Point experiments) | the tide | anyone at low water |

Two consequences:
- **The shallows deplete first and fastest.** The Brook fished out by four people in about ten days (OPEN Q-57c) is what a real
  brook does: at 0.3 kg an hour, one person takes a km's year of trout production in 50 to 150 hours (est.). It is the floor, and
  it should be a meagre one.
- **Yellow eels are resident, silver eels run.** The same kind sits in two stocks: the yellow eel in the shallows and open water all
  year (traps, lines, spears), the silver eel as the autumn run (built).

## 2. The catalogue

Fields: what it needs (materials and tools, with amounts), the work to make it and to keep it and its life, the crew, the skill and
how it was learnt, the water and season, the stock it reaches, and the catch. Engine status in the last column. Catch figures are
real where sourced, else **(est.)**; §4 turns them into the engine's units.

### 2a. With the body and a stick

| Technique | Needs | Make / keep / life | Crew, skill | Water, season | Reaches | Catch | Engine |
|---|---|---|---|---|---|---|---|
| **Tickling, groping** (trout under banks, eels under stones) | nothing | none | one; a knack, learnt by watching and doing as a child | brooks and small rivers, low clear summer water | shallows | slow: perhaps 0.1 to 0.3 kg gutted an hour in good water, nothing in high or cold water (est.) | `fish by hand` (0.6 a unit at full stock) |
| **Crayfish and mussels by hand** | nothing; a sack | none | one; none | brooks, clean rivers (crayfish); slow rivers, lakes (mussels); summer | shallows | crayfish carry little food: about 50 to 80 g whole, about a fifth meat (est.); mussels a famine food | merged into `fish by hand` |
| **Crayfish pots, small baited baskets** | withies (a small basket, about 1 kg, est.), bait | an hour or two each (est.) | one; low | as above, night | shallows | 1 to 4 crayfish a trap-night where stocks are fair, under 1 where weak, up to 50 in the richest (Estonian monitoring) | not built |
| **Spearing and leistering** (a pronged spear by day in clear low water, "sunning"; by torchlight, "burning the water"; the eel glaive or pick worked blind in the mud) | a leister or glaive: iron tines by a smith (about 0.5 to 1 kg of iron, est.) on a pole; a torch for night | a smith's hour or two; lasts years | one; aimed spearing needs practice, the glaive less | salmon in shallows and pools in the run; eels in the mud in winter, also through ice | shallows and the run at a shallows | winter eel spearing could bring home "near half a bushel" a person (Martha's Vineyard, a day; about 10 to 15 kg, est.); reef spearfishers search at about 290 kcal an hour, the best on meeting a fish 2,500 | not built; the run at a shallows reaches `fish by hand` only (and not where no resident stock is, 02zzy2 fix 1) |
| **Bow and arrow fishing** | a bow, barbed arrows on a line | | one; a hunter's skill | clear shallow water | shallows, runs | marginal in temperate Europe | leave out |
| **Stunning** (a mallet on clear thin ice over a fish; a stone dropped on a rock it hides under) | a mallet | | one | brooks, early winter ice | shallows | marginal | leave out |
| **Poisoning** (crushed plants or quicklime in a pool: mullein, spurge; cocculus indicus later, imported) | the plant or lime | | one or two | small pools, low water in summer | everything in the pool, fry included | a pool emptied at once; kills the next years' fish | illegal in the record found: lime and spurge in Ireland's Fisheries Act 1939; lime in a fishpond in the Malicious Damage Act 1861; hot lime on the Tweed in 1857. Medieval bans are likely (continental fishing ordinances) but were not checked here. Leave out, or later as a misuse that empties the shallows and is noticed |

### 2b. Hook and line

| Technique | Needs | Make / keep / life | Crew, skill | Water, season | Reaches | Catch | Engine |
|---|---|---|---|---|---|---|---|
| **Gorge** (a bone or thorn sliver, baited, swallowed lengthwise) | bone or a blackthorn spine, a line | minutes | one; low | any | open water, eels | worse than a hook (more fish lost; est. half a hook's catch) | not built |
| **Hand line, rod and line** | a line (horsehair, plaited; gut; plant cord), a hook (bone or thorn, then iron by a smith: a 4 cm hook in Viking finds), a rod (a hazel or ash pole, optional), bait (worms dug in minutes; offal; small fish) | a rod and line in an hour or two; hooks lost often; a line lasts a season (est.) | one; quick to learn, slow to master (reading the water) | rivers and lakes, all year, best in summer and autumn; through ice in winter | open water | modern creel surveys: 0.35 to 1.45 fish an angler-hour (trout and reservoir fish), so about 0.1 to 0.3 kg gutted an hour; unfished medieval waters perhaps twice that (est.) | `angle` (1.5 a unit at full stock; a rod of 0.5 timber and 0.1 hide, 30 uses) |
| **Set lines, night lines, trotlines** (a long line with many baited hooks, set at dusk, lifted at dawn; a "ledger" or a line of droppers from the bank) | cord (30 to 50 m of line, est. 0.2 to 0.5 kg), 20 to 50 hooks, bait (worms, small fish) | a day to make; hooks replaced; baiting is the daily work | one; low | rivers, lakes; eels and pike; warm months | open water, yellow eels; the eel run | not found as a sourced rate; est. a fish per 5 to 10 hooks a night, so a 30-hook line 3 to 6 fish, 1.5 to 3 kg gutted for about 1.5 hours of baiting, setting and lifting | not built |

### 2c. Traps

| Technique | Needs | Make / keep / life | Crew, skill | Water, season | Reaches | Catch | Engine |
|---|---|---|---|---|---|---|---|
| **Wicker eel trap** (grig, putcheon, hive, eel pot, wheel: a tube of willow about 4 ft long with one or two inward throats, a plug at the end, baited, staked down overnight) | withies: two- or three-year willow rods cut October to February, seasoned three weeks (Severn practice); about 150 to 250 rods, 3 to 5 kg (est.); bait (rabbit, lamprey, offal); a stake and a cord | about a working day to weave by a basketmaker (one modern account: 6 hours); lasts one to three seasons (est.); mended | one; basketry is a long craft learnt young; where to set is local knowledge | ditches, drains, rivers, fens; yellow eels in the warm months, silver eels on run nights | shallows and open-water eels, the eel run | modern fyke nets: Shannon 30 to 45 eels, 4.5 to 8.5 kg per 10 fykes a night (0.45 to 0.85 kg each); Iniscarra 1,162 kg from 70 nets over 10 nights (1.7 kg a net-night); New Zealand 2.7 to 3.1 kg a net-night, 4 to 6 kg a lift. A wicker trap is smaller: est. 0.1 to 0.5 kg a night off the run, 2 to 5 kg on a good run night | `trap in water`: one trap a set (1 unit), 8 nights, holds 10 kg (20 heads) |
| **Eel bucks, a trap street on a weir** (big baskets let down in a frame across the gap at night) | a frame of timber, the weir, bucks of withies (each several times a grig) | a buck is days of basketry; the frame is carpentry | one or two to lower and lift; the weir's crew | rivers; the silver eel run on dark nights, "most between nine and midnight" | the run | "on a good night the take from a team of six bucks could top half a hundredweight" (about 25 kg, 4 kg a buck); "often hundredweights are taken in a night" (Thames, 19th century) | the weir's traps (WATER_WORKS) |
| **Traps in a mill race** (shown in the 14th-century Luttrell Psalter: green-willow baskets in the race for silver eels) | baskets as above; the mill | as above | the miller | the race | the eel run | Domesday: Bottisham Mill's rent was 1,000 sticks of eels (25,000 eels, at the standard stick of 25; the stick is not defined in the source found) | built: a `trap in water` in a mill's race takes `race` 0.5 of a run passing |
| **Fyke nets** (hooped netting with wings) | cord netting on hoops (est. 2 to 5 kg of netting) | days of netting; nets rot without bark tanning | one | slow rivers, lakes, fens | as the wicker trap, larger | as above | a later trap, if nets come in |
| **Putchers, kypes** (ranks of fixed conical baskets in an estuary for salmon) | withies in thousands; stakes | a rank of 650 putchers | a family's fishery | estuaries | the salmon run | Mott's rank at Lydney (650 putchers) took about 622 salmon a year in the late 2000s, about one a putcher a season; the Severn's putchers about 18,200 a season in the 19th century | leave out (estuary, later) |

### 2d. Nets

| Technique | Needs | Make / keep / life | Crew, skill | Water, season | Reaches | Catch | Engine |
|---|---|---|---|---|---|---|---|
| **Dip, scoop and lave nets** (a bag on a frame or a forked pole) | 1 to 3 m2 of netting (est. 0.2 to 0.4 kg of cord), a pole | a day or two | one; timing and footing | falls, below weirs and dams, eddies on a run; also for lifting traps | the run at a pinch point; shallows | depends wholly on the fish passing: at a great falls fishery, "several hundred fish a day" (Celilo, the whole fishery), near nothing elsewhere | not built (the net met 48 salmon and took none, 02zzy2) |
| **Cast net** | 10 to 20 m2 of fine netting, lead or stone weights | 4 to 12 hours to knot a 6 ft one (how-to guides) | one; a long skill to throw | clear shallow water | shallows | | Mediterranean and Asian, rare in medieval northern Europe: leave out |
| **Seine, drag net** (a long wall of net, shot in a curve from a boat or waded, hauled to the bank) | **cord in quantity**: est. 100 to 800 m2 of netting (50 to 200 m by 2 to 4 m), at about 100 to 150 g a m2 of hemp or flax netting, so 15 to 100 kg of twine; head and foot ropes (two of 100 m, about 13 kg); floats (wood or bark); sinkers (stones, about 10 to 20 kg); usually a boat | knotting about 1 hour a m2 (about 920 meshes a m2 at 5 cm stretched mesh; netters tie 10 to 15 knots a minute), so 100 to 800 hours, before the spinning of the twine (the cord note); tanned in bark and dried after use; lasts 2 to 4 years (est.); mending a tenth of fishing time (est.) | **a crew**: a few on a river pool, 6 to 12 on a lake (est.); marine beach seines 8 to 80; a master who directs; the netting learnt as household winter work | slow rivers' pools, lakes, estuaries; all seasons; under the ice in winter in Finland (the Puruvesi winter seine, recorded since the 14th century) | open water at scale; a run lying in a pool | marine beach seines 22 to 57 kg a haul (Alexandria) to 132 to 501 kg (Australian estuaries); inland est. 5 to 50 kg a haul, 4 to 6 hauls a day | not built |
| **Gill and trammel nets** (a wall that meshes fish by the gills; a trammel has three walls) | est. 30 m by 1.5 m, about 45 m2 of fine linen or hemp twine, about 1 to 2 kg; floats and stones | 45 to 70 hours of knotting (est.); fine twine wears fast | one or two; a boat in deep water | lakes, slow rivers, at night | open water | survey nets saturate above about 6 kg a net-night (EN 14 757); est. 1 to 6 kg a net-night | not built |
| **Stake nets, kiddles, haaf nets** (fixed nets on stakes in tideways; Viking-derived hand frames on the Solway) | | | | estuaries, coast | runs | modern catches are licence-limited and say little | leave out (coast, later). Note: Magna Carta (1215, c. 33) ordered all fish-weirs, kiddles among them, removed from the Thames, the Medway and all England except the sea coast |

### 2e. Works and capital

| Work | Needs | Make / keep / life | Crew | Water, season | Reaches | Catch | Engine |
|---|---|---|---|---|---|---|---|
| **The weir** (stakes driven across the river, wattle hurdles between, the fish led to a gap with traps or bucks) | est. for a river 15 to 20 m wide: 30 to 40 stakes 2 to 3 m long, 15 to 30 hurdles (about 1,500 rods), 3 to 6 traps or bucks; stone for footing; the oldest known (Kalø Vig, Denmark) about 6420 BC, the Nekselø weir of hazel wattle panels on hundreds of poles about 3200 BC | est. 10 to 20 person-days for a small river's first section; "labour and resource intensive, requiring communal effort" (Syltholm); heavy upkeep after spates and ice | a crew to build and to work the gap | rivers; the runs | the runs; open-water fish moving | renders: a fishery 5,000 eels a year (1103), two weirs 6,000 for 20 s; Wisbech about 14,000 a year to Ely; Doddington 27,150; one manor (Harmston) 75,000. At 0.2 to 0.4 kg an eel, 1 to 10 t a year, most in a few weeks of run nights | built: sections, a 30% share and 100 kg a night for the first section, wear by the river (D2-210, W-69) |
| **The keep box, corf, live well** (a wicker box or perforated chest moored in the river, holding live fish and eels) | withies (est. as two or three traps), a mooring | a day (est.) | one | any water | | keeps eels alive for weeks and fish for days: the cheapest keeping there is | not built; D2-211 already keeps fish alive in a set trap or weir until lifted |
| **The stew** (a small pond or tank by the house or kitchen, holding fish caught or taken from the big pond until eaten) | digging, a small inlet and outlet | est. tens of person-days | a household with land and a stream | | kept fish | none: it keeps, it does not produce | not built |
| **The fish pond** (a dammed valley or dug basin, a sluice; stocked with bream, pike, tench, later carp; drained every few years and the fish taken out) | an earth dam, a timber or stone sluice, a dry valley with a stream; fry from the wild | large: Bohemia's great ponds were works of a lifetime (Rožmberk, about 500 ha, begun 1584); an English manor's ponds tens to hundreds of person-days (est.); the bank and sluice kept | the lord's servants, a keeper | lowland valleys | kept fish | **unfed yields were small**: about 45 kg a hectare a year of bream (Eynsham's estimate; standing stock about 227 kg a hectare); Czech ponds about 30 kg a hectare a year in the 14th century and 40 by the end of the 16th; harvests like 4,638 carp, 650 bream and 533 pike from one Burgundian pond (one pike to 10 or 20 others). The Rožmberk pond's harvest was 219 t in 1607 | not built |
| **Boats**: the logboat (one oak trunk hollowed), the coracle (willow and hazel laths, one cow or horse hide, pitch), the punt (sawn planks) | logboat: a big oak and an axe and adze (a 13 m reconstruction with iron-age tools took 30 days of work, crew not given); coracle: one hide, laths of winter willow split and shaved, a woven gunwale, no nails (about three days or more, est.); punt: planks, nails or pegs, pitch | a coracle lasts a few years, its hide re-pitched (est.); a logboat decades | one to two (coracle fishing on the Teifi: a pair of coracles drifting at night with a net between them) | lakes' middles, big rivers, crossings | open water at depth; nets shot from the water | a means, not a catch | not built (water_and_preservation.md §8) |
| **Ice fishing** (holes cut through the ice; hand lines, spears, set lines, and the winter seine drawn between holes) | an axe or ice chisel; the lines and nets above | | one; the winter seine a large crew | lakes and slow rivers frozen | open water | | today a freeze stops nothing in the engine (02zzz2) |

### 2f. Keeping, only as far as it binds

- **Fresh fish keep a day or two** in warm weather. The binding steps: gutting (and heading for salting), then salting (salt about
  1 kg to 4 or 5 kg of fish; the rate is in 02zzx), smoking (eels and salmon; a smokehouse, fuel), or drying (thin fish, cold dry
  wind, later stockfish on cold coasts).
- **Alive is the cheapest keeping.** Eels live for weeks in a wet box or a keep in the river; that is why they were rents and why
  live eel trade existed. The engine already treats fish in a set trap or the weir as alive until lifted (D2-211); a keep box would
  extend that to fish already caught.
- **A run's glut is the only fishing that outruns its keeping.** A household's line, spear and a few traps take a few kilograms a
  day, which a family eats fresh. A weir's 100 kg night or a seine's 200 kg day needs salt, a smokehouse, racks and fuel at once.

## 3. The developmental structure

### 3a. What depends on what (text graph)

```
nothing ............................ hands (tickling, groping, crayfish, mussels) ........ shallows
  + a pole ......................... (a rod is optional: a hand line works)
  + cord or horsehair or gut ....... line ──┐
  + bone / thorn (gorge, hook) ..... ───────┼─ hand line, rod ......................... open water
  + iron hook (a smith) ............ ───────┘   (iron doubles the hook's worth, est.)
  + worms or offal (bait) .......... ─────── set lines, night lines (cord + many hooks) . open water, yellow eels
  + iron tines (a smith) + pole .... spear, leister, eel glaive ......................... shallows; runs at shallows; eels in mud
  + withies + basketry ............. wicker traps, crayfish pots, keep box .............. shallows, eels, the eel run
  + cord in quantity + netting ..... dip / lave net (a little) ─────────────────────────── runs at pinch points
                                     gill net (a few kg)  ──┐
                                     seine (15 to 100 kg) ──┼─ + a crew ─ + a boat (lakes) open water at scale
  + hide + withies + pitch / oak ... boat ──────────────────┘
  + stakes, hurdles (withies), traps, stone, a crew, a river ..... the weir ............ the runs (a share of all)
  + a mill (the miller) + traps .................................. the race traps ...... the eel run
  + a valley, an earth dam, a sluice, fry, years ................. the fish pond ....... kept fish
every catch beyond a family's day ── gutting ── salt (pans, a brine spring, fuel) / smokehouse (fuel) / racks / alive in a keep
```

The materials named for the other notes: **withies** (willow and hazel rods, one to three years, cut in winter; traps, hurdles,
the keep, coracle laths), **stakes and poles** (coppice; the weir, spear shafts, rods), **cord** (bast, nettle, flax or hemp
twine for lines and nets; horsehair and gut for lines), **bark** (tanning nets), **hide and pitch** (the coracle), **oak** (the
logboat), **iron** (hooks, tines; a smith), **bone and thorn** (gorges, the first hooks), **stone** (sinkers, the weir's footing),
**salt and fuel** (keeping).

### 3b. What a household can do with nothing, a little capital, and a village's work

| Level | What it is | Its gear | What it reaches | Real return (§4) | What it does to a society |
|---|---|---|---|---|---|
| **Nothing** | anyone, any day | hands | the shallows | about 0.1 to 0.3 kg an hour while the shallows last; a brook is stripped in days | a meagre floor; the shallows are a commons that runs out |
| **A little capital** (a household's, accretive: each piece optional) | a line and hooks, a spear, three to ten wicker traps, a set line, a keep box | an iron hook or two and a spear from the smith; cord; a day of basketry a trap | the open water and the yellow eels; the edge of a run | about 0.2 to 3 kg an hour, rising with each piece | steady protein beside farming; traps and lines are set things that can be robbed, so stretches of bank get claimed |
| **A household's large capital, or a few households'** | a seine or gill nets, a boat | 15 to 100 kg of cord and hundreds of hours of netting; a coracle or logboat | the open water at scale, a lake's middle, a run lying in a pool | about 0.5 to 5 kg a person-hour, for a crew | crew work and shares in the catch; the net and the boat are the capital a fishing family owns |
| **A village's work** (or a lord's) | the weir and its trap street; the race traps on the mill | a crew of days, stakes and 1,500 rods, upkeep every season | a share of every run passing | tens of kilograms a person-hour on run nights; little between | fixed capital and a chokepoint; the village below gets less; held as a lord's fishery; it only pays with keeping |
| **A lord's** | the fish pond and its stews | a dam, a sluice, a keeper | kept fish | about 30 to 45 kg a hectare a year unfed | a larder of fresh fish for fast days and guests, a mark of rank; not a village's food |

### 3c. Where the paradigms switch

Zach's frame (a ladder of four rungs is wrong; paradigms that differ; fewer layers giving less; the full process worth much more;
more at scale) fits the record well:

1. **Accretive personal gear (no switch).** Hands, then a line, a spear, a few traps. Each is optional and each adds to the last:
   a person can skip straight to traps with withies and no cord, or to a line with cord and no withies. Fewer layers give less,
   never nothing. This is where "iterate and add new things" belongs.
2. **Switch one: from one person's gear to a crew's net.** The seine needs cord in a quantity no household spins in a season
   (tens of kilograms), a crew, and in lakes a boat. It takes the open water at a rate personal gear cannot, and it makes shares
   and a master. Optional: a village without a seine still fishes, at a third of the rate.
3. **Switch two: from catching to holding a site.** The weir takes a share of everything passing, so its worth is set by the run
   and not by the work. It is site-bound, held, upkeep-heavy, harms those downstream and blocks boats (Magna Carta's clause). It is
   the paradigm in which keeping (salt, smoke, fuel) becomes the bottleneck. The full chain (weir, traps, smokehouse, salt) is
   worth far more than its parts; the weir alone, with no keeping, wastes most of a run night.
4. **A separate line: keeping fish alive.** The keep box is cheap and belongs with traps. The fish pond is a different paradigm
   (husbandry, not capture) and returns little food for its cost; its point is fresh fish on demand and rank.

The two switches are not in sequence. A run river village can go to the weir without ever owning a seine; a lake village without
runs goes to the seine and the boat and never builds a weir.

## 4. Numbers to calibrate against

Conversions: kg gutted an hour x 2 = fish a unit; x 0.92 = food a unit. A village of 15 eats 15 food a day, 480 in a 32-day year.

| Method | Real figure (source or est.) | kg gutted an hour (est.) | Fish a unit | Food a unit | Engine now | Departure |
|---|---|---|---|---|---|---|
| Hands in the shallows | no sourced rate; est. | 0.1 to 0.3 | 0.2 to 0.6 | 0.1 to 0.28 | 0.6 a unit at full stock (0.28 food) | at the top; keep, but on the shallows stock |
| Rod or hand line | creel: 0.35 to 1.45 fish an hour, about 0.1 to 0.3 kg gutted; unfished waters perhaps twice (est.) | 0.1 to 0.5 | 0.2 to 1.0 | 0.1 to 0.46 | 1.5 at full stock (0.69 food) | **about 1.5 to 3 times the real central (0.5)**; lower to about 1.0 at full stock or name it |
| Set line (30 hooks) | est. 1.5 to 3 kg a night for about 1.5 h | 1 to 2 | 2 to 4 | 0.9 to 1.8 | not built | |
| Wicker trap, off the run | modern fykes 0.45 to 3 kg a net-night; a wicker trap est. 0.1 to 0.5 kg | a line of traps: 0.5 to 2 (est., at 10 to 15 minutes a lift and reset) | 1 to 4 | 0.5 to 1.8 | about 0.2 to 0.3 food a unit measured (02zzy2); one trap a 2-hour set | the set act lays one trap where real work lays 6 to 10 (§5 question 3) |
| Wicker trap or buck, run night | six bucks over 25 kg on a good night (4 kg a buck); "hundredweights" a night at a buck weir | 5 to 20 | 10 to 40 | 4.6 to 18 | trap holds 10 kg; weir first section 100 kg a night | the holds are within the real range (D2-258) |
| Spear, winter eels or a run at shallows | "near half a bushel" a day (est. 10 to 15 kg) | 1 to 2 | 2 to 4 | 0.9 to 1.8 | not built | |
| Seine crew | marine 22 to 501 kg a haul; inland est. 5 to 50 kg a haul, 4 to 6 hauls, crew of 6 | 0.5 to 5 a person | 1 to 10 | 0.5 to 4.6 | not built | |
| Gill net | est. 1 to 6 kg a net-night (saturates near 6) | 1 to 4 | 2 to 8 | 0.9 to 3.7 | not built | |
| Weir, a year | renders of 5,000 to 27,000 eels a year a fishery (1 to 10 t, est.) | | | | D2-210: about 60 to 70 food a year a section, 180 to 200 a full weir; the high arm took 991 kg in 80 lifts (02zzy2) | at the small end of the real, right for a village weir |
| Fish pond | 30 to 45 kg a hectare a year unfed | | | about 14 to 21 food a hectare a year | not built | |
| A full-time fisher, a year | Welcomme's river fisheries: about 4 t a fisher a year at low fisher density, falling as fishers crowd | about 1 to 2 (est., at 1,500 to 2,000 hours) | 2 to 4 | 0.9 to 1.8 | | a ceiling for gear fishing on good stock |
| Foragers' fishing (any gear) | 2,000 to 5,000 kcal an hour (02zzj part 10) | | | 1.6 to 4 | | rich waters, tropical included |
| Shellfish on the foreshore (coast, later) | about 1,500 kcal an hour, 2 to 3 hours on about 10 days a month; gleaning about 300 | | | 1.2 (0.24 gleaning) | | |

**Stocks:**
- A trout brook: biomass about 100 to 200 kg a hectare (Minnesota streams 162 kg a hectare, production 156 a year; Pyrenean streams
  production 31 to 168 kg a hectare a year, mean 82; Michigan 95; Le Cren's English small streams 2 to 12 g a m2 a year, that is
  20 to 120 kg a hectare). A 3 m brook is 0.3 ha a km: **about 30 to 60 kg standing a km, and 10 to 45 kg a year to take.**
- A collapsed lowland river: about 2 g a m2 (20 kg a hectare, the Ely Ouse after zander); a healthy one some times that.
- A fishpond's standing stock about 227 kg a hectare unfed.
- **The compressed year is a lever here.** A real brook km yields its 10 to 45 kg in a year. If the engine's resident stock renews a
  real year's production in 32 days, a brook is about 11 times richer per day than a real one; if it renews a 32-day share, the
  shallows are nearly nothing after the first stripping. Neither is decided; L-75's K 8 a unit of size was never checked against
  real biomass (02zzu). This needs a choice (§5 question 2).

**What binds, read against farming:** plough farming is about 2.4 to 2.8 food a unit (02zzu, D2-258). On real values the hand and
the rod are well below it (0.1 to 0.5), gear fishing about at or below it (0.5 to 2), and only run nights at a trap or the weir far
above it (5 to 18) for a few nights. That ordering is the one to keep; the stocks, not the hourly rates, keep fishing from feeding
everyone (food binds without dominating, at most 30% of actions).

## 5. Granularity for the engine

**Stocks (Zach, 16 Nov: "Do by hand and rods draw from the same stores, because wouldn't they be like crayfish vs actual fish").**
Recommended:
1. **The shallows**, its own resident stock per water body (or per water parcel's edge), small and fast-renewing in summer: small
   fish, crayfish, yellow eels at the edge. Hand methods and small traps draw on it. A brook is nearly all shallows; a lake's
   shallows are a thin rim of a large body.
2. **The open water**, the body's resident stock as now (D2-229): lines, set lines, nets, and the boat for a lake's middle.
3. **The runs**, as built (eel, salmon, lamprey).
4. **Kept fish** as goods alive (a keep box, later a pond's stock), only if a keep or a pond is built.

The yellow eel sits in 1 and 2 (no new kind is needed: the resident stock includes eels). Traps take from 1 and 3, with a little
from 2; lines and nets from 2 and a run lying in a pool.

**Methods (D2-204: general methods, gear deciding the rest).** Five, of which three exist:

| Method | Merges | Gear (multipliers, est.) | Draws on | Status |
|---|---|---|---|---|
| **Fishing at the edge** (`fish by hand`, relabelled "by hand or with a spear or a hand net") | tickling, groping, crayfish and mussels, spearing, leistering, the eel glaive, dip and lave nets | a spear x2 to 3 on the run at a shallows and on eels in the mud; a hand net x3 or more at a pinch point on a run (below a shut dam, a falls) | the shallows; a run where it passes a shallows or pinch | exists; needs 02zzy2 fix 1 (reach the run with no resident stock) |
| **Line fishing** (`angle`) | rod, hand line, gorge, hooks, fishing through ice | an iron hook against bone or thorn x2; a rod against a hand line little (est. x1.2, reach) | the open water | exists; the rod should not need hide (cord or hair, Q-57b) |
| **Set gear in the water** (`trap in water`, and a set line) | wicker traps, crayfish pots, fykes, set lines, night lines; later set gill nets | the gear decides the stock: a wicker trap takes the shallows' eels and the runs; a baited set line the open water | as the gear says | traps exist; a set line is new (a SETS row and a gear) |
| **Drawing a net** (new) | the seine, drag net, the winter seine | a net item (cord in quantity) and a crew (`with`); a boat on a lake | the open water at scale; a run in a pool | new; also split fowling nets from fish nets (W-73's list) |
| **The works** (`weir`, the race, later the pond) | the weir and its bucks, the race traps, later the fish pond and stew | sections (built) | the runs; kept fish | the weir and race are built |

**Leave out:** bow fishing, stunning, the cast net, putchers, stake nets, kiddles and haaf nets (estuary and coast, with boats
later), and poisoning (or later, as a misuse that empties a pool's shallows and the next year's fry, and is seen).

**Small capital worth adding with the set gear:** the keep box (a wicker box in the water, a day of withies) so a family can keep a
glut of eels alive for days, extending D2-211; it is the cheapest rung of keeping and a real one.

**Later:** boats (opening a lake's middle and the seine on a lake), the fish pond (a lord's larder, low yield), ice fishing (a line
and the winter seine through holes; today a freeze changes nothing).

## 6. Open questions (for Zach)

1. **The shallows as a stock of its own** (§5): small and quick to strip, drawn on by hands and small traps, with the body's stock
   left to lines and nets? Recommended: yes.
2. **How the compressed year renews resident stocks** (§4): a real year's production in 32 days (a brook about 11 times richer a
   day than a real one), or a 32-day share of it (the shallows near nothing once stripped)? This decides whether the brook is a
   floor that lasts. No default.
3. **A set of wicker traps laid in one act**: a real unit of work (2 hours) sets about 6 to 10 traps along a bank, not one. Make the
   trap a line, as the snare is (5)? Recommended: a line of 6, each holding its 10 kg.
4. **The rod's rate**: 1.5 a unit at full stock is about 1.5 to 3 times the real central figure. Lower it to about 1.0, or keep it
   and name the factor (D2-259)?
5. **The set line**: a new set method beside the trap (cord and hooks, the open water), or the same `trap in water` with gear
   deciding the stock? Recommended: one set-gear method with the gear naming what it takes, if the agents can read it; two names if
   they cannot (02zzy2 shows they confuse setting and lifting already).
6. **The spear and the hand net as gear on fishing at the edge**, rather than methods of their own? Recommended: yes.
7. **The seine**: build it now (it opens the cord chain to fishing and makes crew shares), or wait for boats?
8. **The keep box**: a cheap withy fitting that keeps caught fish alive (D2-211 extended)?
9. **The fish pond**: worth building at all, given 30 to 45 kg a hectare a year? It earns its place only as a lord's larder and a
   mark of rank.
10. **Bait**: implicit (worms are free), or an input that ties line fishing to offal and the slaughter? Recommended: implicit.
11. **Poison**: leave out, or a later misuse?
12. **Who knows what**: net-making and basketry were household winter crafts learnt young; the weir and the seine crew's skills
    were collective. Seed fishing households with these crafts and with the lore of what each method takes (02zzy2 fix 6,
    02zzz2)?

## Sources

Read through search summaries only (direct fetches refused in this session); verify before quoting as primary.

- Severn putchers and willow: [Basketry & Beyond, putchers and kypes](https://www.basketryandbeyond.org.uk/putchers-kypes-river-severn/);
  [HCR Law on the Mott case](https://www.hcrlaw.com/news-and-insights/salmon-fishing-in-the-high-court/);
  [R (Mott) v Environment Agency [2018] UKSC 10](https://www.remedylegal.ai/resources/case-law/uksc-2018-10);
  [Severn Salmon Online](http://severnsalmon.blogspot.com/2012/02/severn-in-nineteenth-century.html).
- Eel traps and bucks: [The Fishing Museum, eel bucks](http://www.fishingmuseum.org.uk/eel_bucks.html);
  [University of Reading MERL eel trap](https://www.reading.ac.uk/adlib/Details/collect/9921);
  [Museum of Cambridge, eel traps](https://www.museumofcambridge.org.uk/2025/09/eel-traps-and-haunted-inns/);
  [Ely Museum, catching eels](https://www.elymuseum.org.uk/wp-content/uploads/2021/01/HAH-Eels-Catching-Eels.pdf);
  [bushcraft trap account](https://bushcraftuk.com/community/threads/wicker-eel-crayfish-trap.23605/);
  [Duchas schools collection, willow bundles](https://duchas.ie/en/cbes/4605945/4604629).
- Eel rents: [Foods of England, Fenland eels](https://foodsofengland.info/fenlandeels.html);
  [Historia Cartarum, eel rents and payments](https://historiacartarum.org/wp-content/uploads/2017/10/Eel-Rents-and-Payments.htm);
  [The Elver Wars](https://richardfleming.substack.com/p/the-elver-wars);
  [Worcester Cathedral Library, fish weirs](https://worcestercathedrallibrary.wordpress.com/2020/10/19/fishy-tales-the-medieval-fish-ponds-and-fish-weirs-of-the-priory-of-worcester/);
  [Fishing the Thames estuary c. 1250-1550](https://www.researchgate.net/publication/352157147_Fishing_the_Thames_estuary_in_the_later_middle_ages_environment_technology_and_the_metropolitan_market_for_fish_c_1250-1550).
- Modern eel catch rates: [Shannon silver eel study](https://www.researchgate.net/publication/258762998_Silver_eel_Anguilla_anguilla_population_dynamics_and_production_in_the_River_Shannon_Ireland);
  [TEGE 2024 report](https://www.fisheriesireland.ie/sites/default/files/2026-06/TEGE_Annual_Report_2024.pdf);
  [NZ eel CPUE review](https://fs.fish.govt.nz/Doc/22482/EEL9701%20Eel%20commercial%20fishery%20final.pdf.ashx);
  [FAR 2025/25](https://fs.fish.govt.nz/Doc/25883/FAR-2025-25-Catch-per-unit-effort-CPUE-analyses-and-characterisation-of-the-South-Island-commercial-freshwater-eel-fishery-1990-91-to-2022-23.pdf.ashx).
- Spearing: [Denny Abbey, the eel glaive](https://dennyfarmlandmuseum.org.uk/every-object-tells-a-story-the-eel-glaive-a-forgotten-tool-for-a-forgotten-industry/);
  [Vineyard Gazette 1964](https://vineyardgazette.com/node/112996);
  [Walter Scott Club, Scott on salmon](https://walterscottclub.com/blog/scott-on-salmon).
- Angling rates: [Idaho Boise River creel](https://idfg.idaho.gov/press/creel-surveys-boise-river-popular-local-anglers);
  [NY Oatka Creek creel](https://extapps.dec.ny.gov/docs/fish_marine_pdf/oatkacreel2004.pdf);
  [Minnesota creel 2013](https://files.dnr.state.mn.us/areas/fisheries/lanesboro/2013-su-creel.pdf);
  [USGS Lake Scanewa](https://www.usgs.gov/publications/evaluation-angler-effort-and-harvest-rainbow-trout-oncorhynchus-mykiss-lake-scanewa).
- Foraging returns: [Blombos to Pinnacle Point intertidal returns](https://www.sciencedirect.com/science/article/abs/pii/S0047248416000221);
  [Kiribati shellfish gathering](https://www.researchgate.net/publication/226182506_The_Behavioral_Ecology_of_Shellfish_Gathering_in_Western_Kiribati_Micronesia_1_Prey_Choice);
  [Hill et al. 1987, Ache](https://content.csbs.utah.edu/~hawkes/Hill_al87ForagingAcheOFT.pdf).
- Nets: [Mother Earth News, netting](https://www.motherearthnews.com/diy/net-making-zmaz83mjzraw/);
  [Cornell knot-a-net sheet](https://bpb-us-e1.wpmucdn.com/blogs.cornell.edu/dist/c/10116/files/newlogoknotnetting-technique-1xgwj9w-uxseqn.pdf);
  [Salt and Prepper, net weaving](https://www.saltandprepper.com/learn/food/net-weaving);
  [FAO, twine and sinking materials](https://www.fao.org/4/ah827e/AH827E03.htm);
  [FAO catalogue of Ghana gear](https://www.fao.org/4/R0395E/R0395E03.htm);
  [Alexandria beach seine](https://www.sciencedirect.com/science/article/pii/S1687428514000235);
  [Australian estuary beach seines](https://www.researchgate.net/publication/238374190_Catch_characteristics_of_the_commercial_beach-seine_fisheries_in_two_Australian_barrier_estuaries);
  [Puruvesi winter seine](https://wiki.aineetonkulttuuriperinto.fi/wiki/Winter_seine_fishing_in_Lake_Puruvesi);
  [gillnet saturation, EN 14 757](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2022.1000087/epub).
- Weirs: [Nekselø weir](https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/0AD8CB78CCC2DEB6ECB405CB7DFEF632/S003382222100014Xa.pdf/the-nekselo-fish-weir-and-marine-reservoir-effect-in-neolithization-period-denmark.pdf);
  [Syltholm Fjord stationary structures](https://www.cambridge.org/core/product/5A369D414D231A844450162B300CD53D).
- Ponds: [Eynsham Abbey fishponds](https://eynsham-pc.gov.uk/variable/organisation/167/attachments/fishponds_archaeology-1.pdf);
  [BAHS, the early history of the carp](https://www.bahs.org.uk/AGHR/ARTICLES/39n2a1.pdf);
  [Hampshire Field Club, Roberts 1986](https://www.hantsfieldclub.org.uk/publications/hampshirestudies/digital/1980s/vol42/Roberts.pdf);
  [Rožmberk Pond](https://en.wikipedia.org/wiki/Ro%C5%BEmberk_Pond);
  [World Aquaculture, June 2012 (Czech pond yields)](https://www.was.org/Magazine/2012/02/20/).
- Boats: [Coracle Society, Teifi](https://www.coraclesociety.org.uk/coracles/types/teifi);
  [Nation Cymru, making a coracle](https://nation.cymru/culture/how-i-got-to-grips-with-the-dying-craft-of-making-a-welsh-coracle);
  [Leiden dug-out replica](https://www.universiteitleiden.nl/en/news/2018/02/maiden-voyage-of-prehistoric-dug-out-canoe-replica);
  [EXARC logboat experiment](https://exarc.net/ark:/88735/10176).
- Stocks and yields: [Minnesota trout production](https://pubs.usgs.gov/publication/70020118);
  [Michigan trout production](https://www2.dnr.state.mi.us/publications/pdfs/IFR/ifrlibra/Research/abstracts/1877abs.htm);
  [Wessex chalkstream biomass dataset](https://www.data.gov.uk/dataset/c6cdda8c-8b85-4fcc-9922-f5da52a24ce7/fish-biomass-and-density-data-for-3-intensively-studied-wessex-chalkstream-sites-england-uk);
  [Anglian zander study](https://hull-repository.worktribe.com/OutputFile/4217245);
  [FAO, Welcomme's river fisheries](https://www.fao.org/4/u6650e/U6650E07.htm).
- Crayfish: [Estonian and Nordic crayfish CPUE](https://www.kmae-journal.org/articles/kmae/pdf/2011/02/kmae100083.pdf).
- Law: [Irish Fisheries Act 1939 s.26](https://www.irishstatutebook.ie/1939/en/act/pub/0017/sec0026.html);
  [Malicious Damage Act 1861](https://www.irishstatutebook.ie/1861/en/act/pub/0097/sec0032.html);
  [Canal & River Trust, early fisheries law](https://canalrivertrust.org.uk/enjoy-the-waterways/fishing/related-articles/the-fisheries-and-angling-team/the-early-history-of-salmon-and-freshwater-fisheries-law).
  Magna Carta c. 33 is from general knowledge, not fetched.
- Hooks: [The Viking World, iron fishhook](https://scalar.usc.edu/works/viking-world/iron-fishhook);
  [Ottaway, Coppergate ironwork thesis](https://etheses.whiterose.ac.uk/10826/1/276512_vol1.pdf).
- In the repository: the files named under "Read with" above.
