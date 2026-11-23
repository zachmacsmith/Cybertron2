# The fishing, hunting and materials wave: the integrated design

**Status:** ready to build: the architecture, the basis sheet, u0 to u11, the integration review and every open question answered (D2-263 to D2-330, 23 Nov). Each spec opens with a binding table of the decisions taken after it was written. The build plan: build_plan.md. Parts decided are
cited (D2-263 to D2-298); nothing built.
**Owner:** 37.2 (the design, the wild, the water, the materials, the worlds); 37.4 owns the engine's core where a component names it
(the verbs and their registry, the prompt core, the standing rules, buildings and their costs, senses), named on any merge.
**Thread:** the integrated design (W-85), under the network (W-73) and the nutrition worlds (W-69).

## Purpose

Make the land, the water and the people's own work into one web in which each piece is worth having because of the others, and in
which households and villages come to need each other (docs/scenario_design.md: leverage and dependence, chokepoints, conversion
chains). The test is the runs: a river's eels and salmon come in a few nights' glut; what a village does with it (takes it, keeps it,
stores it, eats it through winter, trades the surplus, grows on it) depends on gear made from materials, on hands, wood and salt, on
knowing how, on noticing in time, and on who holds the weir, the salt, the withy bed and the tan pits. The people decide; the engine
holds the physics and tells the truth about it.

## The shape: one loop and four things across it

```
 land and water (stocks)         materials                 making                     taking
 shallows, open water, runs,  -> withies, cord and flax,  -> gear, containers,      -> set and tend on placed
 game, fowl; willow, coppice,    bone, hide, bark, timber,    works; recipes in kg,     gear; gather and work on
 oak, the flax close             stone, fuel                  batches, lives, mending   stocks; the catch to hands
        ^                                                                                     |
        |                                                                                     v
 growth and trade  <-  eating, winter, surplus  <-  stores and the book  <-  processing containers
 households form,      the night's meal; the         space and containers;     racks, salting tub, drying
 salt in, fish out,    gap between runs; who          where goods go, kept,     racks, tan pits, retting;
 the weir's leverage   holds what                     first, eaten, moved;      lots that become the next
                                                      chores and fallbacks      good over nights

 across all of it:  the clocks (day, year, life; the capital factor)
                    signs and senses (what is noticed, by whom, when, with what lead)
                    people (the core prompt, what each is shown, knowledge seeded and learnt, the act shapes)
                    worlds (generation, seeded capital matched to seeded memory, gate checks)
```

## The units

Each is built as its own feature unit (D2-244: data, verbs, signs and processes listed together, so the later cut into feature
packages can move it whole). Each has a component spec in this folder. **Every component spec opens with what it extends** (the
earlier proposals and decisions it builds on) **and names every departure from them**; nothing earlier is dropped or overridden
silently.

| # | Unit | What it does | Extends | Designed in | Design state |
|---|---|---|---|---|---|
| U0 | **The basis** | handling units, weights, the keeping curve, the clocks' factors, the words; in code, stage 1 | clocks.md (D2-273), D2-275, D2-276, D2-288 to D2-295 | basis.md; u0_basis.md | written |
| U1 | **Water and wild stocks** | the shallows stock, the runs, the freeze, the fixes to the run take (a run's fish learn no wariness) | river_and_water.md (D2-209), D2-229, D2-264, D2-265 | wave3_taking §1.2, §3; catch_basis.md | designed; the shallows by water type a gap (G6) |
| U2 | **Taking** | set and tend on placed gear as one's own tagged things; every act of taking as shape, technique, gear, target; the fishing bugs | acts_on_owned_things.md (Q-80), verb_grammar.md, hunt_fish_materials §5, §7, D2-294 | wave3_taking §1, §2, §3 | designed |
| U3 | **Materials and making** | the material chains, about 25 made things with recipes in kg, batches, two lives (uses and rot), mending, what each level is shown | hunt_fish_materials §3 to §6, trying_and_learning.md, D2-263, D2-264, D2-276, D2-281, O-2 | wave2_making §2, §3, §4 | designed; flax below a plot open (W2-2) |
| U4 | **Processing containers** | one unit for racks, the salting tub, drying racks, tan pits, retting ponds: lots that become the next good over nights; the smokehouse as a store | hunt_fish_materials §7.3 and open question 10, D2-271, D2-284, D2-291, D2-295 | wave3_keeping §2, §3 | designed |
| U5 | **Stores and containers** | a store as a space and its containers, each removing named risks; real capacities; vermin basic | store_rules.md, storage.md, D2-272, D2-279 | wave1 §2.3; wave3_keeping §2.4; storage.md | designed in part; vermin's illness a gap (G11) |
| U6 | **The household book** | one book per household and per person: where goods go, kept, first, eaten, moved; `when` on lasting states; chores and fallbacks | standing_rules.md (37.4's), store_rules.md, fallback.md (D4-76), D2-274, D2-282, D2-296, L-142 | wave3_keeping §4; store_management.md | designed; chores against the fallback to finish (G4) |
| U7 | **Works and the building clock** | capital at real hours times the factor, staged; the weir sized to its take; builders, cheaper crop protection, plot clearing | building_clock.md, D2-276, D2-281, L-153 | wave1 §3; building_clock_bots.md | the cost tables designed; the companions gaps (G7, G8, G9) |
| U8 | **Signs and senses** | the river's signs with leads (lore, dawn cue, the run, the catch carried home); keeping's signs; experts' signs as observations | river_signs.md (W-72), guides/senses.md, D2-265, D2-269 | wave3_taking §4; wave3_keeping §2.6 | designed |
| U9 | **People** | the core prompt, what each person is shown, the act shapes, seeded founders' knowledge by livelihood, learning as one record | knowledge_in_their_own_words.md, trying_and_learning.md, livelihood_archetypes.md (37.4's), verbs.md (37.4's), D2-266 to D2-270, D2-286 | wave4_people; steering.md §4 | designed; verb shapes corrected by U2's rule |
| U10 | **Tanning and pollution** (tanning deferred, D2-327; retting's fouling only) | bark, lime from ash, tan pits, leather and its uses (frame, harness, bellows, shoes); retting and tanning fouling the water | hunt_fish_materials §7.5, §7.6, D2-281 | wave2 §2; wave3_keeping §2.2 | partly; pollution in numbers a gap (G3); shoes open (W2-7) |
| U11 | **Worlds and gates** | generation of the seeded capital matched to seeded memory; the gate check at world build; the runs world remade | household_skills.md, founders_knowledge.md, D2-268, D2-270 | wave2 §4; wave4 §6 | designed; the gate check written, not run |

## How the units meet

- **The basis (U0) under everything.** No unit restates a number; each cites basis.md.
- **Taking (U2) needs gear (U3) and puts the catch into hands; processing (U4) and the book (U6) take it from there.** The catch
  basis is calibrated and kept (D2-297); its truth is read in live runs with the rest of the wave.
- **Processing (U4) changes goods; stores (U5) only remove risks** (D2-272). A finished container is a store. A lot finishing is a
  lasting state the book's `when` reads (D2-282).
- **The book (U6) is the one place routine work is set:** where goods go, what is kept and eaten, chores, fallbacks. Labour is real
  where moving is real (quantity work), free within a building otherwise.
- **Works (U7) price the weir, the smokehouses, the withy bed, the pits and the houses** that the other units use; their staging
  waits on their companions.
- **Signs (U8) tell people what the state is in time to act on it,** never what to do (D2-269). Every sign reads state that U1 to U7
  hold.
- **People (U9) know only what they were seeded with, learnt or were told** (D2-268); what each is shown of their crafts follows D2-263
  and the act shapes; the prompt's wording carries no horizon and no steering example (steering.md).
- **Worlds (U11) seed capital and the memories that go with it together:** a family with a mill knows the mill (Zach, 22 Nov).

## The order of building

Each stage is tested with bots for interfaces and basic functioning only (D2-298); behaviour and calibration are read in live runs,
measured as the units come in together (D2-297).

| Stage | Units | Why first |
|---|---|---|
| 1 | U0 the basis (units, weights, the keeping curve, the floor and batches, `clocks.py`), and the faults that mislead (the fishing bugs Q-79, the run's wariness, the options list's removal, the free sub-unit recipes) | everything else is priced on it; the faults confound any reading |
| 2 | U2 taking, U3 making (recipes shown, D2-263; batches, O-2), U1's fixes | gear must exist and be set and tended before keeping matters |
| 3 | U4 processing, U5 stores, U6 the book | the glut has somewhere to go, and someone to see to it |
| 4 | U8 signs, U9 people, U11 worlds and gates | the people learn of the run in time and know what to do with it; worlds remade to match |
| 5 | U7 works staged to 1/15 with their companions (clearing a plot at a time, fences along a border, the watch act; builders' craftsmanship and the dead hedge deferred) | the dearer works wait on the companions that make them buildable; tanning (U10) deferred until the wave is tested (D2-327) |
| — | live runs: the remade runs world and a farm world, each with its null arm, read with a qualitative end-state reading | calibration of the catch, the keeping and the signs together |

## Open across the design

**All the specs' open questions, deduplicated and ranked, are in `questions.md`.**

The questions that span units are on basis.md §7. Each component spec carries its own. The morning brief
(docs/review/37_growth/02zzzh_hunt_fish/morning_23nov.md) ranks those asked so far; the decisions since (D2-288 to D2-298) answer its
section A.

## The files

- `README.md`: this architecture.
- `basis.md`: the numbers and words every unit shares.
- One spec per unit, U1 to U11, to be written (`u1_water.md` ... `u11_worlds.md`), each with: what it extends and its departures;
  the data (tables in the engine's terms); the acts and their results; the signs; the night step or process; the code changes by
  file, with line, and the owner of each; tests; open questions; sources (the notes it draws on).

## History

- **23 Nov 2026: integration review** by 37.2 (integration.md): the fallback order corrected to D2-301 in u6 and u9; `tend` widened to one act on placed things (gear and processing containers); one gear-piece record for u2 and u3; u0_basis.md written for stage 1's code, which every spec deferred to; tanning's nights aligned (u4 to u10); the weir's cost set by D2-302.

- **22 Nov 2026:** written by 37.2 at Zach's ask ("Has all of the design been written up into one complete spec? ... One outline the
  overall architecture and purpose shape of all the changes and how they fit together and maybe with the different sections or
  linked specs for the break down of specific implementation details, data etc"), after the basis questions were answered (D2-288
  to D2-298), from the overnight notes (wave1 to wave4, wave_conflicts, building_clock_bots, steering, catch_basis) and the earlier
  proposals each unit names.

## Sources

docs/review/37_growth/02zzzh_hunt_fish/ (wave1_physical_basis, wave2_making, wave3_keeping, wave3_taking, wave4_people,
wave_conflicts, building_clock_bots, catch_basis, morning_23nov); docs/review/37_growth/02zzzj_steering/steering.md;
docs/review/37_growth/02zzzi_timber/scouting.md; the proposals named in the units table.
