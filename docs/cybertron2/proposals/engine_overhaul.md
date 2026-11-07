# The engine overhaul: the process model, its calibration, and the benched systems it makes cheap

**Status:** discussion (the plan; its parts carry their own statuses)
**Owner:** 37.4 (engine), with 37.2 (economy, environment and the generator: the specs most of the content lands in)

## Summary

One planned overhaul gathers three things:
- **the declared process model:** processes, stocks, waiting processes, needs and wear as data, every rate naming its clock;
- **the economic calibration:** one time scale; harvest windows; pulses; processing that saves work but makes no food; work that
  costs food; wear;
- **the benched systems** that are the same machinery: building upkeep and risks, fishing and water, shelter and water as needs,
  levels of fire, overexertion and fatigue, distance inside a node.

The process model makes each benched system mostly data. Fishing in particular is the overhaul's acceptance test: a new food system,
on its own clocks, added as rows, which the carrying-capacity model must read with no change to its code.

## The benched proposals, sorted

### Fold in: the same machinery, cheap once declared, and each tests it

| Benched item | Where it is now | Why it belongs here | Folds into |
|---|---|---|---|
| **Building and fitting upkeep and risks** | building_risks.md (deferred, OPEN L-48); mill_and_oven_scale.md's upkeep (D4-97 moved it there) | **Upkeep** is durability, process model part 6: millstones dressed after about 300 grain, an oven relined after about 10 firings, the leat cleared each season. **Risks** are outcomes as distributions (part 2), triggered by state the world already holds: weather, lying snow, a parcel's height, structure, use. It is calibration F (fittings wear). | parts 2 and 6 |
| **Fishing and water as a food system** (content: 37.2's [water_and_preservation.md](water_and_preservation.md), 7 Nov) | economy_later.md (nets, boats: deferred); layout.md (water parcels "fish periodic"); spec/environment/resources.md (a periodic stock: "a fish run"); generator.md (fish by flow); ecosystems.md (carr, fen, coast) | A second food system on different clocks: daily fishing from a stock that regrows by season, with runs at their time. Its catch spoils fast fresh and keeps salted or dried. It gives water parcels a use and makes river and coast villages differ from farming ones. **The acceptance test:** added as rows (a stock, a regime, a gathering process with its distribution, a weir or line as capital, salting as a keeping form), it must appear in the capacity report with no change to the capacity code. | parts 1 to 3; needs nothing new beyond the format |
| **Shelter as a need** | shelter.md (its table built as data: housed ×1.0, unsheltered ×1.5, ×2.0 in the cold) | It is a need, and it changes the need for food. Part 5's needs table should hold it beside food and heat, so capacity counts houses as part of what feeds people. | part 5 |
| **Water as a need, minimal** | environment_state.md §8 (OPEN L-23) | A household draws from a source (well, spring, river) for a small daily cost in units by distance; a source can fail. Just the need and the labour, no cleanness or disease yet. It makes where people live depend on water, and gives wells and the river a use. | part 5; distance (below) |
| **Overexertion and fatigue** | OPEN Q-2 (deferred "to revisit with fatigue") | The other half of "work costs food" (calibration E): working past a day's units costs more and leaves fatigue that lowers tomorrow's units. Labour then has a cost in food and in time to come. | the labour side of parts 1 and 5 |
| **Distance inside a node** | OPEN L-35 | A small work cost a step from where one slept: infields and outfields. It is how carrying and walking enter the process graph (mechanism 6), and what lets a von Thünen pattern form inside a village. | mechanism 6 |
| **Levels of fire** | fire_levels_and_camps.md (deferred, L-46) | A fire is a process: fuel in, heat and cooking for so many people out. A big fire, a small one and a warm hearth's carry-over are three rows and one state, a natural part of the fuel need. | parts 1 and 5 |
| **Beasts as eaters** | livestock.md (fodder, herding: built at 02o's numbers, scattered in herds.py) | Grass and hay as a beast's need in the same table as people's, so herds are capped by grazing and winter feed, and clearing pasture costs herds. | part 5 |
| **The fallback (D4-97)** | spec/agents/actions.md | With work costing food, filling every spare unit by default could starve a hungry household. It must respect a limit, or stop when a work's yield is under its food cost. | the labour side |

### Fold in the hooks, not the content: design the format so these slot in later as data

| Benched item | Where | The hook the overhaul should leave |
|---|---|---|
| The land's hidden state (water table, damp, vermin, cleanness) | environment_state.md (L-23) | Hazards' triggers read named state variables. Start with those that exist (weather, snow, height, structure, condition); new variables join as rows with their own clock. |
| Disease | OPEN L-9 | A hazard with an outcome distribution on people, triggered by state (crowding, damp, cleanness when it exists). |
| Ecosystems as data | ecosystems.md §6 | Stocks and their regimes are declared per cover. A later "ecosystem" row (an oak-ash wood, a carr, a fen) is then a different set of stocks and rates, not new code. |
| Carts, pack beasts, boats, river travel | OPEN L-53, L-38; economy_later.md | Carrying is a process (mechanism 6): a load, a pace, a cost a day. A cart or a boat is a row with its capacity and its track. |
| Later tools and farming (nets, boats, the seed drill, irrigation, slash and burn, new crops) | economy_later.md (L-13) | Each is a process or a modifier row once declared. Irrigation also needs water state. |
| Livestock kinds and transhumance | OPEN L-36 | Herds declared as stocks with needs and outputs; a sheep or a pig is a row. |
| Harsher weather and camps built out | fire_levels_and_camps.md (L-47) | Weather as a state variable that risks read; extremes come with the environment scheduler, not here. |

### Decided in the spec but not built (checked against the engine, 7 Nov)

**Fold in:**

| Decided, unbuilt | Spec | Why it belongs |
|---|---|---|
| **The environment scheduler beyond the day's weather:** eras, years' severity, spells drawn (not hand-written), incidents and their spreads, and the kinds (drought, river flood, gale, hail, late frost, blizzard, house fire, wildfire, blight, smut, rats in stores, murrain, wolves; windfalls: a bumper harvest, flood silt, storm-felled oaks, a mast year, a fish run) (D2-69 to D2-79) | environment/scheduler.md: "as built (5 Nov): only the day's weather within a spell is drawn" | The overhaul's outcome distributions need a source of variance, and this is the decided one. Bad-year capacity (38.61 hole 2) needs years' severity. Building risks need incidents (house fire, flood, rats). Take the economic kinds and the windfalls now; disease kinds (fen fever, winter cough, pestilence) as hooks only. |
| **The periodic regime** ("a crop, a fish run: comes at its time and must be taken in its window", D4-7) | environment/resources.md | Crops have it in their own code; nothing else does. Declared once as a regime, it carries the fish run, the mast year, and the hay's summer. |
| **Woods feeding game and forage:** game's capacity rises with trees and young growth; forage rises where the trees are thinned (D2-156) | environment/resources.md | Stocks that act on each other (process model, mechanism 3), decided and never built. Felling then changes hunting and foraging, as it should. |
| **Drought dries dead wood; timber left out in rain is no fuel until dried** | resources.md; economy/buildings.md ("outside") | Weather acting on stores and stocks: the same triggers as building risks (damp fuel, the woodshed). |
| **The night watch:** a watcher skips the night's sleep and eats more for it, detects first, can wake the others (D2-21) | conflict/defence.md: "not built (5 Nov)" | Its cost is "work costs food", already decided for one act. Build it with the energy model, and the defence effect (fuse events exist) comes almost free. |
| **Skill fades without practice** | economy/production.md: "fading is not built" | The worker as input (mechanism 2): practice raises skill, disuse lowers it. |
| **Salt from the shore or a spring** (D2-56) | economy/goods.md: "salt is a good with no source in any world yet" | Keeping fish and meat, and cheese. With fishing it closes a chain: catch, salt, keep, carry. |
| **Carts:** the ox cart (300 to 400 on a track), and the merchant's cart (D2-2, D2-23, D2-135) | economy/transport.md; goods.md | Carrying as a process (mechanism 6). A cart is a row: a load, a track, a pace, an ox. |
| **Traps** (D2-23) | goods.md | A gathering process on small game: a row once declared. |

**Keep apart:**

| Decided, unbuilt | Why not now |
|---|---|
| Blades and better weapons; joint attacks | the combat package you set aside ("not for now") |
| Locks | the permission layer (who may take), not the physics |
| The saddle, and horses | waits on livestock kinds (L-36) |
| Parchment, documents, letters' later forms | the information system |
| The felling axe and great trees | waits on worlds with great trees (the generator) |
| Irrigation (D2-67, "later") | waits on water's hidden state; a hook only |
| Care's effects on health and learning (L-26); disease (L-9) | life and health; hooks only |
| Building on landmarks: bridges, wells, waystations (L-5, L-34) | waits on the generator's physical facts |

### Keep apart: not economic machinery, or not ready

- **Social and institutional systems:** law.md, beliefs_and_values.md (L-25), gates.md, attacks_and_walls.md, households.md,
  notes.md.
- **seeing.md and senses.md:** each new risk and system needs its signs (guides/senses.md), but the sense model itself stays as it is.
- **The verb list (OPEN Q-27) and knowledge.md:** one consequence matters. With processes declared, "what you can do here" and a
  refusal's next step can be generated from them (D4-95; the water-wheel debts of 38.59). Whether the prompt lists options at all is
  a separate decision, given the menu effect (38.57 lesson 15).
- **run_data_interface.md part 2:** separate, but take one item now: the run stores its day-0 capacity report (economic_calibration G).
- **layout.md's one model of structures on any land (Zach, 4 Nov):** occupancy and land changing kind are in the overhaul
  (mechanisms 4 and 5). The full rework of where structures stand is its own step after.

## The stages

Each stage is replay-verified where it should change nothing. Each stage that changes behaviour is one marked engine version.

| Stage | What | Changes behaviour? |
|---|---|---|
| 0 | Invariance checks with the capacity model: which measures move with the year's length and a plot's size | no (no engine change) |
| 1 | The declaration format, with clocks: stocks and regimes (the periodic one included), processes with outcome distributions, waiting processes, needs, durability. Every existing rule moved into it | no: exact replay of the 55 journaled runs, and the tests |
| 1b | **The acceptance test:** fishing, with salt and a fish run, added as rows only (gear to the weir, salt, preservation: water_and_preservation.md §10's first steps). The capacity model must report it with no change to its code | adds a system; marked as version 1 |
| 2 | Calibration and labour:<br>• the time scale; harvest windows; pulses; processing;<br>• work's food cost, with the watch (D2-21), overexertion and fatigue (Q-2);<br>• skill fading; distance (L-35); the fallback's limit;<br>• fittings' wear and upkeep | yes: version 2 |
| 3 | Variance and risk:<br>• the scheduler's years, spells and economic incidents and windfalls (D2-69 to D2-79);<br>• building risks (first: house fire, floods on low ground, snow load on wattle, rats in stores, damp fuel);<br>• woods feeding game and forage;<br>• bad-year capacity | yes: version 3 |
| 4 | Needs and carrying: shelter, water (minimal), beasts' feed in the needs table; levels of fire; carts and traps as rows | yes: version 4, or with 3 |
| 5 | Checks and experiments:<br>• capacity on every world;<br>• a scripted bot farming at "worked" for a year;<br>• the dependence ladder;<br>• a fishing village against a farming village;<br>• the sophistication experiment | runs |

**Size:**
- Stage 1 touches about 2,000 to 3,000 lines.
- Stage 2 is mostly data, plus the labour mechanics (a few hundred lines).
- Stage 3 is about 300 lines each for fishing and risks, and less for water and fire.

## Why

Zach, 7 Nov: "I think we should do a major engine update / overhaul with this. I have a bunch of currently benched changes in
proposals ... see which of them would make the most sense or integrate with this update? E.g. ... upkeep and risks as data that can
be stored for different buildings, places that depend on environment etc. and maybe integrating fishing and water ecosystems as a
distinct source of food could work now as a separate system to test the calibration alongside to see how things work with multiple
systems."

## Open questions (for Zach)

1. **The overhaul and its stages:** go ahead as staged, with stage 1 behaviour-preserving?
2. **Fishing's first scope:** line and weir (timber and work; no fibre) now; nets with fibre, and boats, later?
3. **Water:** as a need now (sources and their cost by distance only), or leave it for the hidden state?
4. **Building risks:** which first? Proposed:
   - house fire from hearths and ovens;
   - floods on low ground;
   - mill upkeep;
   - snow load on wattle;
   - rats in stores.
5. **Levels of fire:** now, or with the harsher weather that makes them matter?
6. **Ownership:** most of the content lands in 37.2's specs (economy, environment, the generator's fish resource). 37.2 owns those
   specs; 37.4 writes the engine code. Agree the split on the board.

## Affects

- engine: data.py, night.py, farm.py, forests.py, herds.py, verbs.py, buildings.py, life.py;
- 37.2's specs: economy, environment;
- the generator's resources;
- cybertron2/capacity: none by design (stage 3's acceptance test).

## History

- 7 Nov (later): 37.2 wrote the content for fishing and preservation (water_and_preservation.md); linked as stage 1b's content.

- 7 Nov (later): what the spec decides but the engine lacks, checked against the code and sorted (fold in: the scheduler's economic kinds, the periodic regime, woods feeding game, drought and wet fuel, the watch, skill fading, salt, carts, traps; keep apart: blades, locks, the saddle, documents, the felling axe, irrigation, disease, landmark works). Stages re-cut: fishing as the acceptance test right after the format.

- 7 Nov: proposed (37.4) after Zach asked for an overhaul around the process model, with the benched proposals sorted into fold in,
  hooks only, and keep apart.

## Sources

process_model.md, economic_calibration.md, carrying_capacity.md, building_risks.md, mill_and_oven_scale.md,
fire_levels_and_camps.md, shelter.md, environment_state.md, ecosystems.md, economy_later.md, livestock.md, layout.md; OPEN Q-2,
L-9, L-13, L-23, L-35, L-36, L-38, L-46 to L-48, L-53; review 38.57 to 38.62.
