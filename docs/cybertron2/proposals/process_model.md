# A declared process model: the engine says what its economy is, as data an analysis can walk

**Status:** agreed in principle (Zach, 7 Nov: parts 1 and 3 to 6 yes; part 2 revised to his version below); the build awaits his go
**Owner:** 37.4 (engine), with 37.2 (economy, the checker and the generator)

## Summary

Every way the world turns one thing into another (a gathering, a making, a growing, a night's regrowth, a spoiling, a need) is
declared once, in one form, beside the code that does it. Analyses (carrying capacity, labour values, the economy check, a refusal
that says the next step, a generator aiming at a target) then walk the declarations instead of copying the engine's formulas. A test
fails when a mechanic arrives without its declaration.

## The proposal

Six parts, each its own step, each leaving every past run replaying exactly.

1. **Processes in one form.** Each act that moves goods declares inputs, outputs, work, requirements (fittings, covers, beasts,
   tools, trade, knowledge), tool multipliers and wear, and its yield model. About two thirds of TECHNIQUES already fit. Still
   handled by bespoke code: sow, reap, break, manure, clear, field works, milk, slaughter, repair, bury.
2. **Each yield is one pure function of its outcomes, as a distribution (revised 7 Nov).** Each yield kind's code (stock, chance,
   fixed, pool, crop, milk, ...) returns what can come of a unit of work and with what chance, and the state's change with each
   outcome.
   - The act draws from that distribution with the world's random stream.
   - An analysis takes its expectation.
   One piece of code serves both, so the model cannot drift from the engine: it is a projection of the implementation, not a
   second account of it. Processes over time (crops, regrowth, spoiling) are analysed by running the engine's own steps (simulation
   and search), never by closed forms. Agreement tests run the real acts many times and compare means.
3. **Each regime declares its dynamics, unconfined.** A regime's night is any function of its state and conditions, as complex as
   it needs; analyses treat it as a black box (simulate, search), so complexity costs nothing. A regime may declare best and worst
   cases for its uncertain parameters, for economic analyses to sweep. For plants, game, grass, trees, young growth and dead wood (fast, threshold, slow, young,
   dead, finite, endless, accrues): its night step and its best steady take. The steps are pure functions now (D4-102's refactor:
   night.regrow, forests.trees_step, young_step, dead_step); this part adds a registry keyed by regime.
4. **Processes that take time, in one form.** Crops (sow, wait, reap), pregnancy and building works over days become a delayed
   process:
   - a duration;
   - hazards (the frost kills a tender crop; a crop left past its window rots; blight);
   - what it occupies meanwhile (ground, a fitting, a person).
   Rotations, the frost check and "days to the first harvest" then work for any such process.
5. **Needs as data.** The night's ration by stage, heat by condition and shelter by state are declared in one table, not in
   night.py's code. Food, fuel and shelter capacity become one computation over different needs.
6. **Durability and throughput as data.** Tool life and wear (in ITEMS and TECHNIQUES now); buildings' breaks and upkeep (PHYSICS
   repair); what a fitting processes a day; what a store holds. Most of this is in the tables already.

### Clocks: every declared rate names the clock it runs on (Zach, 7 Nov: agreed)

Days stay the base unit and the tick: what agents decide, see and pay is in days. Each declared rate states its clock, and the
engine converts:

| Clock | Processes | Declared as |
|---|---|---|
| the day | eating, work units, travel, fatigue, fresh food spoiling, a fire's fuel | a day |
| the year (by season) | crops, sowing windows, wild regrowth, grain keeping through the lean season, beasts' breeding, trees' growth | a share of the year or a season |
| the life | ageing, lifespan, perhaps pregnancy | a share of a lifetime |

- "Days a year" and "years a life" are the two exchange rates. They are named settings in the world, set once and shown, where
  today they are implicit in dozens of nightly numbers.
- Yields that feed people are declared against need: a plot feeds so many person-years. So a world's capacity in people does not move
  with the year's length, and the year's length decides only how many daily decisions fall between harvests.
- A guard test fails on any declared rate that does not name its clock.

### Mechanisms to design in from the start (else they become one-off patches)

1. **Work by several at once:** a crew ditching, a yoked pair and a driver, joint attacks. A process may need several workers.
2. **The worker's state:** skill by practice, hunger's yield, untaught tries at half. The worker is an input; practice is an effect.
3. **Stocks that act on each other:** beasts stop young growth and change the soil; felling leaves brash. Regimes read and change
   other stocks.
4. **Occupancy:** ground holding a crop, a fitting one person uses at a time, a store's limit, beds. A process may hold a thing for
   a time.
5. **Land changing kind:** forest to scrub, cleared to field, built ground; a change of kind, not of quantity.
6. **Carrying as a process:** roads, loads, pack beasts; moving goods costs work and food, so reach enters the same graph.
7. **Hazards as distributions:** blight, gales, fire, illness (part 2's form).
8. **Needs of beasts:** grass and fodder in the needs table beside people's.
9. **Permission apart from physics:** claims, access, debts and wages in their own layer, so an analysis can include or leave
   them out.

### Size

About 2,000 to 3,000 lines touched:
- the yield handlers in verbs.py;
- farm.py, herds.py;
- night.py (needs);
- life.py;
- buildings (upkeep).

In six stages (regimes and yields first, then crops as delayed processes, then needs), each checked by replaying all 55 journaled
runs exactly and the test suite.

## Why

Zach, 7 Nov:
- "Is this type of analysis something that can be automatically generated off the systems of the engine, kind of like recursively
  exploring every network of things marked as able to make food and their scheduling rules, capital costs etc? Or do you have to
  hard code the analysis yourself?"
- "What would be required about the engine for the kind of way that I was describing ... and is that type of structure something we
  would want anyway for other reasons".

The carrying capacity model (D4-102) reads the tables, but copies the formulas the code holds:
- the yield of foraging, hunting and reaping;
- regrowth;
- the frost;
- what a sowing gives.

A change to the engine's physics would leave it silently wrong. Its copies were moved into pure engine functions on 7 Nov; this
proposal finishes the job.

It is wanted for other reasons too:
- **Refusals that say the next step (D4-95), for any goal.** In the takeover runs (38.59), agreements said "work on the water wheel"
  and nothing told the workers which act does that; the poorest spent their days on debts they could not pay.
- **Knowledge:** what one must learn to make a thing.
- **The economy (37.2):** labour values, prices, and a world check that cannot miss a crop the frost will kill (OPEN Q-28).
- **The generator:** worlds aimed at a target, such as "feeds 0.8 of its people as it stands and 2 when worked".
- **c2viz** can draw the chains.
- **Tests:** conservation of goods by every process, and coverage, so no mechanic arrives undeclared.

## Alternatives considered

- **Keep the analysis's own formulas.** Fast to write; drifts from the engine; every new mechanic needs the analysis rewritten.
- **Measure by running the engine with scripted bots.** Exact by construction, but slow, and it measures the bots' policy as much as
  the land. Kept as the agreement test (part of D4-102), not as the method.
- **Declare everything at once.** Too large a change to verify; the steps above each keep replay exact.

## Open questions

1. The order of work. Proposed: part 3 (regimes) first, which is small; part 2 for gathering; part 4 for crops; part 5; part 1's
   remaining techniques last.
2. Whether yields stay deterministic expectations (as now) or declare their spread, so an analysis can give a range.
3. Who owns the needs table: 37.4 (the night) or 37.2 (the economy)?

## Affects

- engine: data.py, night.py, farm.py, forests.py, verbs.py (handlers);
- spec/economy/production.md, spec/environment/resources.md, spec/core/world_schema.md (if records change shape);
- cybertron2/capacity (D4-102), landgen/economy.py (37.2).

## History

- 7 Nov (later): clocks added (Zach: "I agree with this. Add this."): every rate names its clock (day, year, life); two exchange rates as named world settings; yields declared against need.

- 7 Nov (later): Zach: 1 "yes"; 2 "wouldn't it be that we just describe how to make things and the engine could programmatically
  calculate expected output per unit of work itself? ... The model should be a projection of the reality of the implementation, or
  a compression of it, not a hope about it"; 3 "yes, but we shouldn't confine this too much ... the functions should be allowed to
  require different conditions etc, have complex behaviors"; 4, 5, 6 "yes". Part 2 revised to outcome distributions (one function,
  sampled by the act, expected by the analysis); part 3 unconfined; the mechanisms to design in, and the size, added.

- 7 Nov: proposed (37.4), from Zach's questions while the carrying capacity model was built. The night's rules were already moved into
  pure functions (commit 5a85a95) and the capacity model calls them.

## Sources

cybertron2/capacity/; review 38.60 (the capacity model and the retrospective of past runs); review 38.59 (the takeover runs).
