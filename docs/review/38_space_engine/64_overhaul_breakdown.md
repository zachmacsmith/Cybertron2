# 38.64: The engine overhaul after phases 1 and 2: how the general system works, where it stops, and what to decide

Session 37.4, 8 Nov 2026. The breakdown Zach asked for before phase 3 ("You can do the first 2 phases and then I'll want a deep
break down before continuing"; "break it down for me so I can make sure it's what I want and not something just a similar vibe").
What was built and checked: 38.63. Rules: spec/core/processes.md. Decisions: D4-103, D4-104.

## 1. The idea in one paragraph

The engine states its economy as **data plus a small number of registered rules**. A stock on the land says which rule brings it
back. A technique says what it draws on, what it gives, and which kind of yield it is. Each yield kind is a function that returns
the act's outcome as a distribution. The act samples that distribution with the day's random stream. An analysis takes its mean or
runs the same rule forward. So the analysis is the engine, compressed, not a second account of it. A new food source is rows in
the tables: a stock, a technique, a good. It needs code only if it needs a rule or a yield kind that does not exist yet.

## 2. The pieces

| Piece | What it is | Where | A new thing supplies (data) | A new thing needs code when |
|---|---|---|---|---|
| **Stocks** | something on a parcel with a level S, a ceiling K and a rate r (plants, game, fish, grass, trees, a seam, salt, dung) | RESOURCES rows; a parcel's `state` | a row: its renewal rule, its words at low and high; per parcel its K, S, r and the rule's own parameters | never, if an existing rule fits |
| **Renewal rules** | how a stock comes back each night: a pure function `rule(p, res, ctx) -> S` | engine/renewal.py | its name in the row (`renewal`), or in a stock's own record to override the row | it comes back in a new way (a coppice cycle, a fish that spawns in one place and is caught in another) |
| **Response to density** | how a unit of work's take answers the stock's level: (S/K) ** b | renewal.response, yields.py | `response` in the row or the stock: proportional, hyperstable, hyperdepleted or a number | the take depends on something other than the level (a shoal found or not) |
| **Techniques and yield kinds** | an act: what it draws on, gives, needs (cover, fitting, tool, trade, beast, season, pack); its kind is a function returning the outcome | TECHNIQUES rows; engine/yields.py (stock, chance, fixed, pool); farm.py (crops, herds) | a row naming an existing kind and its numbers | the act's outcome has a new shape |
| **Outcomes** | distributions: a constant, a uniform, a scaled draw with a cap, a chance, a branch, a joint (a catch and a hide) | engine/outcomes.py | nothing | a new shape of chance (rare) |
| **Needs** | a person's food a night: one pure function of the night (shelter, cold, warmth, gear, fire, the road, the ration's factors, care, and since phase 2 the day's work) | engine/needs.py | the tables it reads (PHYSICS ration, shelter, camping, heat) | a new kind of need (heat and water as needs are phase 5) |
| **Clocks** | every rate in the data names its clock: day, year, life, use, event. The exchange rates are the world's days a year and its lifespan | engine/clocks.py | the rate's clock in RATES | never (a test fails on a rate without one) |
| **Packs** | switchable bundles of rows: a row with `"pack": "water"` exists only in a world with `packs: [water]` | engine/packs.py | the pack's name on the rows, and in the world | never |
| **Labour** (phase 2) | what work costs: food a unit, pushing on and fatigue, the walk, skill fading | engine/labour.py; PHYSICS labour | the values | a cost that depends on the task (hauling against weaving) |
| **Wear** (phase 2) | a fitting wears with use or time and works at half until mended | engine/wear.py; FITTINGS wear | `wear: {life, count, mend}` or `{years, mend}` and a mending technique | wear that is not "half until mended" (a gradual loss, a breakage that destroys) |

**The analysis side** (cybertron2/capacity/) reads these, not the engine's internals:
- **Sources:** the wild source finds every stock that a known technique draws on for food. It takes the stock's best steady take
  from its own renewal rule, and the food a unit of work from the technique's own outcome mean. It names no stock.
- **Fields** run the crop year through farm.py's own pure functions (crop_base, fail_chance, frost_kills, fallow_gain, manure_gain,
  soil_step, weed_gain, grow_days).
- **Herds** have their own source.

## 3. Worked example: fish, as data only

What was added for the water pack, all rows with `"pack": "water"`:
- **Stocks:** fish (renewal `periodic`), salt (`endless`).
- **Goods:** fish, salt fish, a fishing rod.
- **Techniques:**
  - fish by hand (kind `stock`, base 0.6);
  - angle (kind `stock`, base 1.5, uses a rod);
  - making a rod (`make`);
  - a salt pan (kind `fixed`, saltmarsh, summer);
  - salting fish (`make`).

What it took in code:
- **One new rule:** `periodic`. It is a run that comes in its seasons toward `run_K` and leaves again.
- **The packs mechanism.** Without it, adding basic techniques changed every older world's prompt.

What followed with no code naming fish:
- Agents found the crafts, made rods, fished, salted, and talked about the commons.
- The capacity model gave Ferrybank 0.77 of its people with water and 0.16 without (E1a: water 0 deaths, dry 4).

## 4. Worked example: each ecosystem its own rule (D4-104)

Two meres in one world, each given its own stock record:

```yaml
fb_mere:  {state: {fish: {K: 8, S: 8, r: 0.3}}}                                           # the row's default: periodic rule, proportional take
fen_mere: {state: {fish: {K: 8, S: 8, r: 0.15, renewal: threshold, response: hyperstable}}}
```

- **The fen mere:**
  - it does not recover below its threshold share;
  - a catch there holds up as the stock thins: (S/K) ** 0.4, so a fisher does not notice the decline until it is late.
- **The night, the act and the capacity model** all follow the record. A test checks that the hyperstable mere gives the same steady
  take for less work.
- **The generator's ecosystem layer (37.2's)** can write these fields per patch. That is how "each environment decides its own
  regeneration and how this relates to being fished" is meant to work.

## 5. What a unit of work costs now (phase 2)

| | Before phase 2 | Now (first values, calibrate) |
|---|---|---|
| Food | a ration a night whatever one did | the ration and 0.04 a unit worked (7 units: 0.28); a night on guard 0.3. The work's share also counts toward going hungry |
| Past the day's units | not possible | up to 2 more if the reply asks (`overwork`): each costs double food and a unit off tomorrow |
| Distance in a node | free | each parcel on the day's route past the first two: a quarter unit, carried until whole, off a later day |
| Skill | rose by practice, never fell | fades 1% a night of its gain after 8 days unpractised |
| Capital | lasted for ever | millstones 600 grain, an oven 10 firings, a leat a season; then half until mended (2 to 3 units) |

**Where it binds.** Work's food takes 3 to 5% off the farming levels of capacity. It takes 10 to 30% off foraging and hunting
("bare"), because these give little food a unit of work. That is the break-even 38.61 said was missing: idling now saves food,
and the least productive work stops paying first.

## 6. Where it is not general (what still needs code), most likely to bite first

1. **Crops and herds are bespoke modules.**
   - Their timing is data (CROPS share and sow_seasons, PHYSICS cattle) and their hazards are pure functions.
   - But "a process that takes time" is not one generic form (process_model part 4).
   - An eel trap, a cheese maturing or a pregnancy each needs its own code today. The capacity model's crop year (rotation.py) is
     its own search over farm.py's functions.
2. **The capacity model's allocation is greedy.**
   - It gives work to the flows with most food a unit, and ignores *when* the food comes.
   - Phase 2 exposed this: being fed is not monotone in the population. The search now copes, but the allocation is still wrong in
     principle for seasonal sources.
   - A linear programme over days (38.61's shadow prices) is the right fix.
3. **The woods' three stocks** (trees, young growth, dead wood) call their rules by name, because they feed each other. A stock's
   own `renewal` does not apply to them.
4. **Yield kinds are a closed registry.** A new kind is code in yields.py, verbs.py and the capacity model's KINDS. The guard test
   catches a missing one.
5. **Work's food is the same for every task.** Felling and weaving cost alike.
6. **The walk costs time but does not change choices.** It is charged after the day, from the route. Nothing prices a far parcel
   when the agent plans.
7. **Year-length invariance is not built.** process_model.md said yields would be declared against need ("a plot feeds so many
   person-years"), so a world's capacity in people would not move with the year's length. They are still declared per act. A
   longer year gives the same harvest a sowing and more nights to feed.

## 7. What phase 2 changed for existing worlds

- **Upper levels fell by a third to a half** (38.63 §7); "as it stands" rose slightly.
- **A world that starts in summer can no longer sow grain until spring.** 74 of the 76 world files that are not variants start in
  summer (summer is also the default). Their earlier runs lived partly by resowing grain in summer. They are now harsher, so their earlier results are not
  comparable to new runs.
- **Wenbridge cannot mill.** It has millstones and no oxen (it was so before phase 2).
- **Fishing is untouched** and still strong (E1a's caution).

## 8. Decisions that are Zach's before phase 3

1. **Are these the mechanisms you meant?** In particular:
   - work's food counting toward hunger;
   - pushing on as the agent's explicit choice;
   - wear as "half until mended".
2. **Values.** All are first values. The ones that move results most:
   - grain's spring-only window: summer-start worlds wait three seasons;
   - work's 0.04 a unit;
   - fishing's yields.
3. **Year-length invariance:** build it (yields against need) before phase 3, or leave it.
4. **The allocation:** replace the greedy allocation with a programme over days now, or after phase 3 (variance and risk will lean
   on it).
5. **Existing scenarios:** recalibrate the summer-start worlds (start them in spring, or give them a standing crop), or keep them
   harsh as they are.

## 9. E2 (after phase 2): Wenbridge, a full year, labour on against off

(Running; results added when the two runs end.)

*Current as of 8 Nov 2026 (E2 running).*
