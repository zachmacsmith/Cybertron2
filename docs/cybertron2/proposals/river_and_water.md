# River and water: the runs, the weir, the mill, salt and what lives by the water: build brief 5

**Status:** accepted for building: D2-209 (16 Nov), question 5 open; after brief 4c (`hunt_calibration.md`), the merge left to the building session.
**Build brief 5** for the wild layer: pack K4 (02zv §4) without its fen-only and boat parts, on the engine as built by briefs 1 to
4b and calibrated by 4c; with the river as one site with many claims (the mill and the weir), salt boiled inland (D2-56), and fuel
as a real draw. A runs-only world follows the gate as a test of its own (§8).
**Owner:** 37.2 (author; the wild pack's data, `engine/wild.py`, the ecology; the test worlds from the generator). Works on a water
parcel, the mill's gap, the salt pan, their condition and the manual are 37.4's (§6).
**Affects:** spec/environment/wildlife.md; spec/economy/buildings.md (the weir as a work; the salt pan); spec/economy/production.md
(the mill's gap; boiling salt); on the branch: `wild/kinds.py`, `wild/ecology.py`, `wild/areas.py` (`down`), `engine/wild.py`,
`engine/data.py`, `engine/night.py`, `engine/signs.py`; the generator (a brine spring).

## Summary

What exists:
- **Kinds:** eels as a kind that moves on a cue (`mover: cue`: the autumn run on rain after dry weather); wildfowl; heronries and
  beaver lodges as sites, with their signs.
- **Methods:** `trap in water` as a set work, `net` for flocks of fowl, `fish by hand`, the fishing rod, salt fish.
- **Salt:** only from saltmarsh pans, dried by the sun (`salt pan`), so an inland village has none.
- **The mill:** a water wheel (`site: water`) that grinds 200 grain a day and silts in a year; it takes nothing from the river but
  water.
- **The land:** every area knows its downstream area (`land.down`), its river length and its lakes.

What is missing is the river as a **line that ties villages together**. A run starts upstream and reaches each village in turn, a
day or two later. A weir with its gap shut takes a share of everything passing and leaves less for those below. A salmon taken
before it spawns is a salmon fewer in three years. Cold drives the fowl onto open water and then weakens them. The otter robs the
traps, and the beaver's dam floods one meadow and fills a pond. This brief builds that, so the strongest commons between villages
(02zp §27: eels mattered in 13 of 20 villages) is physical.

**What the economy research adds** (02zzj, read in full for this revision; the border note 02zzk puts all of it inside the border):
- **The river is one site with many claims.** "Mills hold water, fish need runs, tanning and retting foul it", answered in history
  by "mill rights, weir laws, fixed fishing times" (02zzj part 01 §2.9); water power "bound to specific stretches of river, with
  fixed capacity, and in conflict with fish runs" (part 01 §6.1); fisheries and weirs were valuable lords' rights, and a weir
  blocked boats (part 05 §2.4). So the mill on a run's river is a second weir with a different owner (§3a).
- **A glut must be kept, and keeping costs fuel and salt.** Drying, smoking and salting turn a pulse into months of food (part 10
  §1.5; part 02 §5.4); salt is "the chokepoint for keeping protein" (part 02 §5.4). Medieval Droitwich boiled brine in lead pans,
  with woods in other manors owing carts of fuel in return for salt (part 01 §5.2, checked). Inland, salt comes from a spring and
  costs fuel (§4b, as D2-56 decided and never built).
- **Fuel is the largest flow a household has.** In a cool climate fuel, not food, is a household's largest energy flow: 1 to 2 t of
  wood a head a year, and a village of 50 households needs of the order of 40 to 170 ha of coppice (part 01 §3.3). The smokehouse
  and the salt pan must draw on the same woods as the hearth (§4c).
- **A run can carry a society by itself.** Where a dense, predictable, storable run could be held, foragers settled, stored, and
  developed property in fishing stations and rank without farming (part 10 §1.4 and §1.5, Testart and Woodburn; part 06 §3.6: ranking
  followed the intensification of salmon storage). That is the runs-only world after the gate (§8).

## 1. For the builder

**This file holds for this brief.** Read:
- briefs 1 to 4c and their tests (4b: hunt_followups.md; 4c: hunt_calibration.md, for the take as calibrated and set things found
  at their parcel);
- 02zv K4;
- 02zp §27 (the eel analysis);
- 02zzj parts 01 §2.9, §3.3, §5.2; 02 §5.4; 03 §7.1; 05 §2.4; 10 §1.4 and §1.5; 18 §2.4 (the passages this revision rests on);
- on the branch:
  - `wild/kinds.py`: the eel's rows, `mover`, the `when` rows of `trap in water`; the heronry and beaver sites;
  - `wild/ecology.py`: movement;
  - `wild/areas.py`: `down`, `river_km`, `big_river_km`, `lake_km2`;
  - `engine/wild.py`: `take`, `_set_night`, sites, `cond`;
  - `engine/data.py`: TECHNIQUES `trap in water`, `net`, `fish by hand`, `break a dam`, `water mill`, `salt pan`, `salt fish`,
    `firewood`; FITTINGS `water wheel`;
  - the climate's rain and frost by node (D4-109);
  - brief 4's shelter levels, for the weir's condition.

**Do not** name kinds in rule code (a run is a mover's rule over any kind with `mover: run`); invent rivers the land does not have;
cap signs; seed any custom about the gap, the mill or the spring (nothing social is forced). Dry runs only.

**Branch:** `ecology-water`, from main once briefs 1 to 4c are merged (otherwise from brief 4c's branch).

**Worlds:** 37.2 supplies two generated worlds with the land kept (D2-208), before the build starts. `land.down` exists only in
generated worlds, so they come from the generator (not `make_wild_tests.py`, whose worlds are written by hand). Each starts late in
summer, so a run of 14 days holds the autumn run. The wild region (02zze: Weirford on its river, the Mere) is a third check.
1. **The river world:** two villages on one river with a big river for salmon, inland (no saltmarsh), pinned so each holds what the
   other needs:
   - **Upper village:** the brine spring (§4b); the first take of the eels' run down.
   - **Lower village:** a water mill on the river (§3a), whose dam stands between the salmon running up and the upper village's
     water and spawning areas.
   - So the upper village's weir thins the lower's eels, the lower village's dam thins the upper's salmon, and the lower village
     needs the upper's salt to keep its run except by smoke.
2. **The lake world:** a lowland village with a lake (the fowl and the freeze).

**Made (16 Nov), on branch `water-worlds` (cc6f38d), from `peoples-worlds`:** `cybertron2/specs/water/` (`river.yaml` seed 9,
`lake.yaml` seed 3, `runs.yaml` seed 5; README there), by `cybertron2/specs/make_water_worlds.py`, with two new generator pins:
`has: brine spring` (a `brine` stock on the village's lowest open ground) and `on: big river` (the village's water cut from the
large river itself; the travel costs skip its cells, so `on: river` gave a side channel or none). In the river world Saltwell's
water drains to Millham's ring through 34.6 km of river. Each world ran two days with bots, with no errors.

## 2. The run along the river (C6 on `land.down`)

1. **A run** is a mover's rule over any kind with `mover: run` and a direction (down to the sea, or up to spawn).
   - The eel's silver run goes down in autumn; the salmon and the lamprey go up.
   - The cue is the kind's own `when` row: for the eel, rain after dry weather in autumn, on dark nights. It is read over the
     **catchment**: the rain on the area and on its upstream areas over the last days, through `land.down` reversed.
2. **The lag:**
   - The run leaves an area on its cue night and reaches the next area down after about a day for each 10 km of river between them
     (`river_km`; calibrate).
   - So a village downstream sees the run a day or two after the one above, and one who has watched the upstream village knows it
     is coming.
3. **Numbers:**
   - The eels running are a share of each area's eels (the silver eels, about a fifth a year; calibrate). They leave the area's
     count as they pass, so the run thins as it goes, and what reaches the sea is gone.
   - The stock is made up by elvers coming up in spring, by the area's suitability (the ecology's growth). Years of heavy takes lower
     the run that follows.
4. **Where a run meets a village:** the chain of areas follows each area's largest river cell, so it passes a village's **ring**,
   beside its small home area (which holds only the village's water cells). A run is at a village's water when it is in the
   village's home **or ring** area (found building the worlds, 16 Nov).
5. **What it gives people:** on a run night at a village's water, `trap in water`, `net` and `fish by hand` take from the run by the
   take rule (stage A of brief 4), with the run's density in place of the resident stock. The `when` multipliers built in brief 1
   become the run itself.

## 3. The weir (a standing work on a water parcel; C7)

1. **Built** at a water parcel on a river by a crew: stakes and wattle (timber) and units. It is a work with a condition (brief 4's
   levels): floods and ice wear it, and it is mended like a building.
2. **The gap:** open or shut, set by an act at the weir (`set` with a gap, as shutting is built).
   - A weir is crew work: built and worked by a declared party (brief 4b's `with`), not by people who happen to be there.
   - **Shut:** the weir's traps take a share of every run passing (about half when sound; less as it wears; calibrate), into the
     weir's set things.
   - **Open:** it takes little and lets the run pass.
3. **Downstream:** what a shut weir takes is not there below. The next village down sees the run thinner by that share, on the lag
   day. Two shut weirs on one river leave little for a third.
4. **Robbing and lifting:** the weir's set things, like any set thing, can be emptied by anyone at the parcel. Taking from another's
   leaves a trace (D4-48), read by those who know the weir. As brief 4c builds for snares and traps:
   - the crew finds the catch by going to the weir, never by being told;
   - one who knows the weir sees its catch when at the parcel;
   - a full trap is plainer to anyone;
   - a remembered weir says what was seen and when, never "empty" by default.
5. **Signs:** the weir and its gap seen at the parcel; the run seen ("eels thick in the weir's traps"); below, "the run was thin
   this year" for those who know it.

## 3a. The mill on the run's river (new, 16 Nov)

A water mill holds the river with its dam and sends the water through its race. On a river with a run it stands where a weir would,
and its owner chooses between grinding and the fish.

1. **The mill's gap:** a water wheel on a river parcel where a run passes has a gap like the weir's, open or shut, set by an act at
   the mill (the same `set` with a gap).
   - **Shut** (the water held): the mill grinds at its full rate (200 grain a day, as built).
   - **Open** (water let past): it grinds at a lower rate (about half; calibrate), because the head of water is lost.
   - A new water wheel starts shut, as a miller would build it.
2. **What a shut dam does to the runs:**
   - **Running up** (salmon, lamprey): a shut dam stops a share of the run (about half; calibrate) from passing to the areas above,
     so fewer spawners reach the upper areas and fewer salmon return (§4). The stopped fish gather below the dam, where anyone at the
     parcel can take them by `net` or `fish by hand` on that night at the run's density.
   - **Running down** (eels): the shut dam sends the run through the race. A `trap in water` set in the race (at the mill's water
     parcel) takes the weir's share of the passing run, into that trap; without a trap in the race, the run passes through the wheel
     and below as before.
   - **Open:** the runs pass as if there were no dam.
3. **Whose:** the mill's gap is set by whoever may manage the water wheel (its claim's rights, as for any building); the trap in the
   race is anyone's set thing, robbed and remembered by brief 4c's rules.
4. **What it makes:** two chokepoints on one river with different owners (the weir's crew and the mill's), the village below or
   above short when either is shut, and a miller who trades flour against fish. The engine settles none of it: who may shut, when,
   and for what in return is for the people (OPEN L-106).
5. **Signs:** the mill's gap seen at the parcel ("the mill's hatches are shut; the water stands high above the dam"); salmon leaping
   at the dam on a run night, plain to anyone there; above the dam, "few salmon came up this year" for those who know the run.

## 3b. The weir in sections, its cap and its upkeep (Zach, 16 Nov; D2-210)

A run should be a short burst of plenty, worth more a night than farming, but only on a few nights a year; the limits are what
the weir can hold and what people can keep (Zach: "storage and keeping food does become the real bottleneck"). All values calibrate.

1. **One weir per water parcel** (the parcel is its site). Weirs on one stretch take in turn from upstream, each from what the ones
   above let through.
2. **Built in sections**, as the mill is built by adding parts (D2-61); upgrading costs only the difference, and a weir can be part
   upgraded:

   | Section | Cost each | Adds |
   |---|---|---|
   | the first (stakes and wattle across part of the river, one trap) | 12 timber, 24 units, a crew of 2 (as built) | takes 30% of a run passing, holds about 10 food a night |
   | each further timber section, up to three | about 10 timber, 25 units | about 7% more of the run and about 7 food more a night, to about 50% and 30 food |
   | stone footing, a section at a time | about 10 stone, 15 units | that section wears at a tenth of wattle's rate |

3. **A night's catch** is the share of the run passing, capped by what the weir holds (later also by what its crew can lift).
4. **A year's take, the target:** about 60 to 70 food for one section, about 180 to 200 for a full weir (about 13% and 40% of a
   village of 15's food in a 32-day year: 480), from about 5 salmon nights and 3 eel nights. A run night pays about 3 to 6 food a
   unit of work, above farming's 2.8, for a few nights only.
5. **Wear follows the river**, per section and night: the material's rate (wattle; timber about half; stone-footed about a tenth) ×
   the water type (lowland river ×1, large river ×1.5, upland beck ×2) × the flow (low ×0.5, normal ×1, high ×2, spate ×5, flood ×15)
   × the gap shut in high water (×1.5: traps and a closed gap catch the debris) × ice (×3, more at the break-up). Until the river
   level exists (environment_systems.md, phase 1), the flow is read from the catchment's rain of the last days, the signal §2
   already computes for the eel's cue.
6. **Targets:** a wattle section on a lowland river loses about a level in a week of normal flow (mended every season it is used);
   a spate night often costs one or two levels; a flood with the gap shut usually takes the section, with it open about half that.
   A year's upkeep: wattle about 40 to 50% of its cost, timber 20 to 25%, stone-footed 5 to 10%; a full weir a quarter to a third of
   its cost a year, against a few percent for a house.
7. **The choice it makes:** runs come with rain, so the nights the fish run are the nights the river rises. Keep the gap shut and
   catch the run while risking the weir, or open it to save the weir and lose the fish.
8. **Keeping is the bottleneck:** a full weir's salmon night (about 15 fish, 30 food) is more than one smokehouse can take (40 fish
   a batch over 3 to 4 nights) or one salt spring supplies quickly (1 salt for 4 fish); fresh fish spoil in days. So the weir, the
   smokehouses, salt and fuel bind together, as the research found (02zzj parts 06, 10: storage, not the catch, made a run into
   wealth).
9. **Proposed, not decided: fresh fish spoil faster than meat**, about 0.5 a night against meat's 0.3 (the data has fish "as
   meat"): fish goes off within a day in warmth, a carcass can hang for days in cool weather.

## 4. The kinds on the water

| Kind | What to add (data on the rules, unless said) | Test |
|---|---|---|
| **eel** | `mover: run`, down, autumn; silver share; elvers up in spring; meat 0.2 (brief 4) | the run reaches each weir on its lag day; years of heavy takes thin it |
| **salmon** (new kind) | RESOURCES and ecology rows: in areas with a big river; `mover: run`, up in autumn and early winter, to the upper areas; returns in about three years by the spawners that reached the upper areas (past shut weirs and dams, §3, §3a); meat about 2; taken at weirs, below a shut dam, by net and by spear (`stalk` on water as a method's use, or `fish by hand`) | a year of shut weirs or a shut dam lowers the run three years on |
| **lamprey** (new kind) | on the same module, up in spring; small meat; for the lord's table later | a spring run at the weir |
| **wildfowl** | pushed by cold: frost on the land raises the fowl on open, unfrozen water at the node (the climate's frost; lakes and big rivers stay open longest); after a long freeze they weaken (flee lower, so easier to take), then die (the great-freeze regime, built); survivors return | a freeze crowds the open water and makes nets pay; a long one empties it |
| **otter** (new kind) | in areas with rivers; diet fish and eels; takes from set things in water and from weirs at night (brief 2's targets, `water: true`); hide; trapped by `snare` set at water | an unwatched weir loses part of its catch to an otter; trapping it stops that |
| **beaver** (the site, built) | the dam floods the meadow below: the meadow parcel next to the lodge's water loses hay (a cut, calibrate) and the water parcel's fish stock rises; `break a dam` (built) ends both for a season; trapping takes the pelt and castoreum (built) | the dam lowers the meadow's hay and raises the fish; breaking it reverses both |
| **heron** (the site, built) | herons take fish from the village's water and from a fish pond (a cut of its stock); the heronry's size follows the fish | a big heronry lowers a small water's fish |

## 4a. The smokehouse: keeping a glut (moved here from brief 4c, Zach 13 Nov)

A run of eels or salmon, like a herd slaughtered before winter, brings more food in a few nights than a household's hearth rack can
keep: a rack dries about 8 meat every 3 nights (about 2.7 a night), while fresh fish and meat spoil fast. The smokehouse is the
scale above the rack (water_and_preservation.md §7).

1. **Its own building, apart:** a small room with **smoke racks** (a fitting; about 2 timber and 2 units), on any parcel with room.
   - **Wattle** (cheap): a smoulder in clay-daubed wattle can catch; a keyed fire chance each night it burns (calibrate), the danger
     being to the buildings on its own parcel.
   - **Stone** (dear): near no risk. Built on another parcel than the houses (a croft, a field's edge), a fire there reaches no
     house: the engine counts space in a parcel, so "apart" is another parcel.
2. **A batch:** up to about **40** fish or meat, loaded in one act; **3 to 4 nights**.
3. **The fire:** a smoulder of hardwood or chips, about 1 firewood a night, drawn from the same stores as the hearth (§4c). **Tended
   once a day** (a unit, at the place); banked, it lasts the night. A day untended, the fire dies that night: the batch pauses and
   spoils that night at the open rate. Nobody sits up with it.
4. **It gives smoked fish and smoked meat:** about half the weight; keeping about four times as long as dried meat (slow smoke dries
   further and preserves). Their uses: laying in for winter, food carried on a long journey, trade.
5. **Whose:** its builder's household. Others use it by agreement (a rent or a share), so it is a thing to control, like the mill;
   it can be robbed while a batch is in. Its owners see its state when at the place, by brief 4c §6.4's rule ("the smokehouse: 30
   eels curing, 2 nights left, the fire low").
6. **Tests:** a 40-eel run loses under 10% through a smokehouse and about half without; a day untended pauses the batch; a wattle
   smokehouse sometimes catches, a stone one almost never; a neighbour pays to use it.

## 4b. Salt inland: a brine spring boiled with fuel (new, 16 Nov; D2-56)

D2-56 decided that "shore salt is sun-dried, inland springs are boiled". Only the shore half is built, so an inland village cannot
salt its run or make cheese. This builds the other half.

1. **The spring:** a `brine` resource at a spring on one parcel (endless, like the shore's `salt`, but at one site). The generator
   places brine springs where the land holds them (37.2: a spring feature, rare; pinned in the river world, §1).
2. **The salt pan:** a fitting (a shallow lead or iron pan over a hearth; about 1 copper or iron and 2 timber, a few units; calibrate)
   in a building at or near the spring. It wears like other fittings and is mended.
3. **Boiling:** `boil salt`, a make at the salt pan: brine (drawn there) and **firewood** give salt. About **1 firewood for each salt**
   from a strong spring (calibrate: a near-saturated brine needs a few kilograms of wood for each kilogram of salt; a weak one much
   more), 1 unit for each 4 salt, a skill of its own (a trade: the salter). Done in any season, unlike the sun-dried pans.
4. **What it makes:** a site that one village holds and others need, a steady draw on the woods (§4c), and salt fish and salt meat
   (built) possible inland, so a run can be kept by salt instead of smoke. Salt becomes the classic good between villages and
   between the coast and inland (water_and_preservation.md §5).
5. **Signs:** steam and the smell of the pans at the spring; white crusts on the pan's rim; "the salter's fire burned all night".
6. **Tests:** an inland village with a spring makes salt only by burning firewood; a village without one has none unless it trades;
   salted fish keep as built.

## 4c. Fuel: the woods as the shared draw (new, 16 Nov)

Fuel is the largest flow a household has in a cool climate (part 01 §3.3). The hearth, the smokehouse (§4a) and the salt pan (§4b)
all burn firewood, gathered or cut from the same woods (forests.py), so a run kept by smoke or salt is paid for in wood.

1. **No new mechanic:** the smokehouse and the salt pan take firewood as inputs from stores, as the hearth does; gathering and the
   woods' regrowth are as built.
2. **A budget test** (dry, the river world, one year, bots): report firewood burned by use (hearths, smokehouse, salt pan) and the
   woods' standing stock and regrowth by area. The target: a village that smokes its run and boils its salt draws its nearer woods
   down within a year or two unless it gathers further out or cuts back, so fuel binds without starving the hearth in an ordinary
   year (calibrate the smokehouse's and the pan's draw, not the hearth's).
3. **What it is for:** the woods become a thing the fish, the salt and the hearth compete for, as in part 01 §2.9 ("fuel for the
   house against fuel for industry": "iron, salt, glass and lime works bid up the woods").

## 5. Not in this brief

- **Fen only:** the decoy pond (it needs a trained dog, K6), reedbeds, crane and bittern with drainage, the fen ague. They wait on
  the generator making fen worlds with people: none of eight seeds passed its capacity check (02zzd, 37.2's to fix).
- **Boats:** punts and coracles (water_and_preservation.md, stage A of boats). Historically the river mattered more as a road than as
  a fishery (part 04: water carriage far cheaper than land); that is the transport track (part 09 §9, addition 5), not this brief.
- **The hunting economy** (benched by Zach, 16 Nov): stage 1 materials and stage 2 gear (economy_web.md). Nets for fish need cord and
  wicker traps withies from there; this brief uses the traps and nets already built (Open question 7).
- **The fishpond:** keeping fish alive instead of catching them, the lordly "living larder" (part 03 §7.1; part 06 §7 lists fishponds
  as a capturable control point). At the border, behind L-106 (02zzk).
- **Rules of the fishing commons:** close seasons, net mesh, leases of a fishery, a weir's rent (part 18 §2.4; part 05 §2.4). Close
  seasons need nothing from the engine (people can agree them); the rest wait on L-106, and mesh on nets of cord.
- **Retting** flax and crayfish downstream; tanning fouling the water; the pearl mussel; eel spearing in winter: later (K4's low
  ranks; tanning with the benched materials).
- **Forays to the river beyond the village:** the forays track (OPEN L-105).

## 6. Touches in 37.4's files

- **`data.py`:**
  - TECHNIQUES `build weir`, and the weir's gap as `set`;
  - the weir as a work with a structure (timber);
  - the water wheel's gap (`set` with a gap) and `water mill`'s rate by the gap (§3a);
  - RESOURCES `salmon`, `lamprey`, `otter`, `brine`;
  - FITTINGS `salt pan`; TECHNIQUES `boil salt`, the salter's trade;
  - ITEMS for salmon (or `fish`).
- **`night.py`:** the weir's condition by floods and ice (brief 4's levels and weather).
- **`signs.py`:** the run, the weir and its gap, the mill's gap and the salmon at the dam, a thin run below or above, the dam's
  flooded meadow, the salt pans.
- **The manual:** the weir's and the mill's gap, and boiling salt, for those who know them.
- **37.2's own:**
  - `wild/kinds.py`: the run rows, the new kinds;
  - `wild/ecology.py`: runs along `down`, with the lag, the silver share and elvers; the share a shut dam stops;
  - `engine/wild.py`: the run as a take's density; the weir's take; the race trap's take; the fish below a dam;
  - the generator: brine springs;
  - the test worlds.

## 7. Tests (the gate)

**Unit:**
- A run leaves an upstream area on its cue and reaches each area below on its lag day, thinner by what was taken.
- A shut weir takes about its share, and an open one takes little.
- A weir's set things can be emptied by another, leaving a trace.
- Salmon returns follow spawners.
- A shut mill dam stops about its share of a run going up, and the stopped fish can be taken below it; an open one passes the run
  and grinds at the lower rate; a trap in the race takes about the weir's share of a run going down.
- Boiling salt burns firewood at its rate; an inland village without a spring has no salt.
- Frost crowds the fowl onto open water, and a long freeze weakens and then kills them.
- An otter takes from an unwatched weir.
- The beaver's dam cuts the meadow's hay and raises the fish; breaking it reverses both.

**Society-level** (dry, scripted, the river world):
- The downstream village's run-night catch falls by about the upstream weir's share when that weir is shut, against open.
- Three years of shut weirs, or the lower village's dam kept shut, lower the salmon run at the upper village.
- The fuel budget (§4c) over a year of smoking and boiling.

**Food a unit:** 02zzd's harness extended to run nights (traps, nets, the weir, the race trap). An eel run night should pay well for
a few nights a year (a target: about 1 to 2 food a unit at a weir on a run night, near nothing otherwise; calibrate).

**Regression:**
- The probe worlds with bots.
- Worlds without rivers, mills on rivers without runs, and coastal salt unchanged.
- All tests pass.

**Gate:** the above and a short dry-run report to Zach; then a small live run on the river world if he allows one, read against the
pack off: crews on run nights, weirs built and kept, the gaps of the weir and the mill disputed between the villages, salt traded.

## 8. After the gate: a runs-only world (a test of its own, Zach 16 Nov)

**The question.** Can a run, with storage and fishing places a group can hold, produce property and rank without farming? The
research says it did: where a dense, predictable, storable run could be held, foragers settled, stored large surpluses and
developed property in fishing stations, specialists and rank (part 10 §1.4); assets that must be guarded and inherited (stores,
traps, boats, weirs) bring property and binding kin rules (Woodburn's delayed return, part 10 §1.5); on the Northwest Coast
"ranking followed the intensification of salmon storage" (part 06 §3.6). It is a cleaner test of social structure made by people
around physical facts (OPEN L-106) than a farming world, and it needs nothing past this brief.

**The world** (generated, the land kept, pinned):
- One river with strong salmon and eel runs and three stations along it (upper, middle, lower), each a node with water parcels
  good for a weir; game and wild plants enough for summer and not for winter, so the stores decide the winter.
- **No farming:** no fields, no seed, no herds. Farming's rows carry no pack (D4-103), so it cannot be switched off: the world
  makes it impossible instead (fields to scrub, no grain, beans, flour, bread, hay or beasts; the farming crafts not known). An
  engine `farming` pack would make the arm exact (OPEN L-112). Made: `runs.yaml` (seed 5, 48 people, 60 days). Fire, racks, smokehouses, weirs, traps, nets,
  forage and the hunt as built. No spring and no mill: kept by drying and smoke, with the woods as fuel (§4c).
- **People:** three or four households at each station, kin across stations; Opus at each station's leading household, Sonnet in
  the middle, Haiku in the bulk (scenario_design §2). Goals in-world (keep your people through the winter), never scores.
- **Length:** long enough for a salmon return under the compressed year (Open question 1): about 50 to 70 days, starting late in
  summer.

**What to read** (against a null arm with the runs replaced by a resident stock of the same yearly food, so storage has no pulse to
answer):
- whether stores become unequal between households and stations, and stay so;
- claims on stations, weirs and smokehouses, and who may use them;
- the gaps: whether upper stations shut their weirs, and what the lower ones do about it (agreements, gifts, raids);
- whether people restrain the take for the salmon's return;
- giving and feasting (gifts of stored food) and who gives;
- a qualitative end-state reading, as scenario_design asks.

**Order:** after this brief's gate and the river world's live run, and after Zach's go for a live run. The world is 37.2's to
generate; nothing in the engine changes for it.

## Why

- 02zp §27: eels mattered in 13 of 20 generated villages. They are the strongest commons between villages that the land already
  holds.
- 02zv K4 ranked the eel run with its lag, traps, the weir and its gap, salmon and wildfowl first in water worlds.
- Zach (10 Nov): build the other wildlife before forays.
- The economy research (02zzj, Zach 16 Nov: "revisit the fishing"): the river as one site with many claims, keeping a glut by fuel
  and salt, fuel as the household's largest flow, and the run as the base of a society (Summary, §3a, §4b, §4c, §8).

## Alternatives considered

- **Eels as a resident stock with a seasonal multiplier** (as built): no line between villages, so no upstream and downstream.
- **The weir as a fitting with a fixed yield:** simpler, but nothing passes it, so it has no effect downstream.
- **The mill as the river's only work** (no weir): simpler, but one owner holds the only lever; two works with different owners give
  interlocking chokepoints (scenario_design §1).
- **Salt only on the coast, carried inland:** the decided rule (D2-56) has springs too; without them inland worlds have no salt at
  all, and no salt fish or cheese.
- **A fuel mechanic of its own for the woods** (a coppice cycle, charcoal at its real weight): left to the materials stage and the
  border's fuel row (02zzk); this brief only makes its new uses draw on the woods as built.

## Open questions (for Zach)

1. The salmon's three-year return compressed into the world's years (a year is 32 days, so 96 days, longer than any run so far), or
   shortened. Proposed: one world year (32 days), so a run of 45 days or more sees a shut weir's cost. That is a compression like the
   lifespan's, stated as such.
   **Answered (D2-209): one world year.**
2. Whether the weir's gap has a customary rule seeded in any world (no: nothing social is forced), or is only physical (proposed).
   The same for the mill's gap and the spring.
   **Answered (D2-209): nothing seeded; physical only.**
3. The run-night target at a weir (§7). Proposed: about 1 to 2 food a unit at a sound, shut weir on a run night, near nothing
   otherwise. Over an autumn that is a few good nights, above brief 4c's master near home only on those nights.
   **Answered (D2-209): about 1 to 2 food a unit, to calibrate.**
4. Whether the weir waits for 37.4's merge of briefs 1 to 4c (proposed), or starts on the stacked branch.
   **Answered (D2-209): the building session decides.**
5. **The mill's trade** (§3a): open, the mill grinds at about half its rate. Proposed: half, so a miller who lets the salmon through
   loses half a day's grinding on each run night, and a lower village with a mill has a real choice.
   **Still open** (16 Nov: Zach asked what the gap open means; explained in conversation).
6. **Salt's fuel** (§4b): about 1 firewood for each salt from a strong spring, the pan a fitting of a few units, the salter a trade.
   Proposed as stated, to calibrate in the fuel budget (§4c).
   **Answered (D2-209): yes for now; revisit in calibration (OPEN L-110).**
7. **Withies and cord:** they sit in the benched materials stage, but they make fishing gear (wicker traps, nets) as well as hunting
   gear. Proposed: leave them benched for this brief (it uses the traps and nets already built), and split them from the hunting
   economy when gear for fishing comes up.
   **Answered (D2-209): benched for this brief; they go to the hunting and resources build, a soon follow-up (OPEN L-111).**
8. **The runs-only world (§8):** to design now and run after the gate, or only to keep as an idea. And its cast: proposed Opus at each
   station's lead household (three), Sonnet and Haiku as scenario_design §2.
   **Answered (D2-209): designed now by 37.2 while the build starts, then handed to the building session to run after the gate.**

## History

- 10 Nov 2026: written by 37.2 as brief 5 at Zach's request ("rewrite the briefs to address the other aspects of wildlife in the
  first briefs before any foraging").
- 10 Nov 2026: rebased on brief 4b (hunt_followups.md): its branch, declared parties for crew work, wariness and recovery in the
  ecology the runs move through.
- 12 Nov 2026: revised for Zach's check: after brief 4c (the take as calibrated; set things found by going to them, and remembered
  without "empty", Zach 12 Nov); the branch from main after the merge; the worlds from the generator, starting late in summer, with
  the region as a third check; proposed answers to the salmon's return and the run-night target.
- 13 Nov 2026: the smokehouse added (§4a), moved from brief 4c (Zach: "that sounds valid"): its own building, wattle with a fire
  risk or stone, apart on another parcel, tended once a day, giving smoked fish and meat that keep about four times as long as dried.
- 16 Nov 2026: revised from the economy research (02zzj, read in full: parts 01, 02, 03, 05, 06, 10, 18), at Zach's request ("bench
  the hunting economy, but revisit the fishing ... write up the edited water brief, with the runs-only world as a test world to do
  after"). Added: the mill on the run's river with a gap of its own (§3a); salt boiled inland from a brine spring with fuel (§4b,
  completing D2-56); fuel as the shared draw, with a budget test (§4c); the river world pinned so each village holds what the other
  needs (§1); the runs-only world as a test after the gate (§8); boats, the fishpond, the commons' rules and the benched hunting
  economy named in §5; open questions 5 to 8. Nothing in §2 to §4a changed except the salmon's passage past a shut dam and the
  smokehouse's fuel.
- 16 Nov 2026: accepted for building (D2-209), Zach: "1. yes. 2. yes. 3. sure. 4. I'll be passing this to the other agent ... 5. what is
  its gap open. 6. for now but flag as revisit ... 7. yes. This will be for the hunting and resources build which should be flagged as a
  soon follow up. 8. yeah ... you can design the world while it gets started and then pass it on". Question 5 open.
- 16 Nov 2026: the worlds made (branch `water-worlds`, cc6f38d): the river, lake and runs-only worlds and the generator's brine spring
  and big-river pins (§1); where a run meets a village (§2.4, found building them); §8's "no farming" made physical, since farming has
  no pack (OPEN L-112).
- 16 Nov 2026: §3b, the weir in sections, its nightly cap, a year's targets and upkeep by the river (D2-210), after the build
  measured salmon nights at 4.5 to 17 food a unit with no cap (38.72). Zach: "storage and keeping food does become the real
  bottleneck"; "a weir seems like quite high upkeep ... a lot more than a house"; "if you think the numbers above match that then it
  is fine". Fresh fish spoiling faster than meat proposed (§3b.9).

## Sources

02zv §4 (K4); 02zp §27; hunt_and_fixes.md (brief 4); briefs 1 to 3; wild/areas.py (`down`); water_and_preservation.md (§4, §5, §7);
D4-48, D4-109, D2-56, D2-61, D2-166, D2-208, D4-103; 02zzj parts 01 (§2.9, §3.3, §5.2, §6.1), 02 (§5.4), 03 (§7.1), 04, 05 (§2.4),
06 (§3.6, §7), 09 (§9), 10 (§1.4, §1.5), 18 (§2.4); 02zzk (the border); scenario_design §1, §2; OPEN L-105, L-106.
