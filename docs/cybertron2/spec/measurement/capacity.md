# Carrying capacity

What a world's land can feed and keep warm, at named levels of practice and technology (D4-102). Built as
`cybertron2/capacity/`; run as `python -m cybertron2.capacity WORLD_OR_RUN ... --figures --png`.

## The measure

| Rule | Value | Decision |
|---|---|---|
| The measure is a ratio: food eaten in a year against food needed in a year (people x their rations x the year's days) | `decided` | D4-102 |
| Food eaten is the land's yield net of seed, worth what its route makes it (raw, boiled, ground, milled), less what spoils between harvest and eating, given the work the people have | `decided` | D4-102 |
| The year is simulated day by day from empty stores for five years; a population is fed for good when the last two years run no shortfall | `decided` | D4-102 |
| Stores are a buffer, not capacity: reported as days of food, with the days to the first harvest the people bring in themselves and any standing crop the frost takes first | `decided` | D4-102 |
| A run's horizon: from the world's day, with its stores, standing crops and seed, the day food first runs short at a level | `decided` | D4-102 |
| Fuel is its own need: a hearth's heat a year shared by PEOPLE_A_HEARTH, against the woods' steady take at three levels (dead wood; and young growth; and trees) | `decided` | D4-102 |

## The levels

| Level | What it assumes | Decision |
|---|---|---|
| bare | wild food only, eaten raw as gathered; no fields, no fire, no store | D4-102 |
| as it stands | one crop a year on the fields as they are, unbroken, unweeded; grain boiled; kept in a house | D4-102 |
| worked | the best crops and rest the year allows; soil broken, weeded, manured where there are beasts; ground to meal; bins | D4-102 |
| best | everything the world's techniques reach: ploughing, full weeding, master farmers, seed selection, rye over the winter, flour and bread, a granary | D4-102 |
| ceiling | best, with meadow, pasture, scrub and woods turned to field while the region's woods keep the hearths | D4-102 |

Each level is lowered to what the world reaches (materials on the land or in store, the techniques someone knows or is aware of,
beasts, seed), and says what it gave up.

## Rules

- **One source for every rule.** The model calls the engine's own functions (night.regrow, slow_season, spoil_rate, eaten_worth;
  farm.crop_base, fail_chance, frost_kills, fallow_gain, manure_gain, soil_step, weed_gain, grow_days; forests.trees_step,
  young_step, shed_a_night) and the world's calendar. It keeps no formula of its own for what the engine decides (D4-102).
- **Agreement tests:** tests/test_cybertron2_capacity.py runs the engine's rules on a real world and fails if the model differs
  (wild regrowth under the model's take, spoilage, eating raw, a sowing's yield).
- **Guard tests:** they fail when the engine gains an edible good, a yield kind or a resource the model does not read.
- **Costs:** each level at the people it feeds:
  - its work a year, a head and as a share of all their work;
  - its capital: processing fittings by the year's throughput, stores for the peak stock, houses and hearths, tools worn,
    ground cleared;
  - each in units with the work its materials embody (the production graph, graph.py).
- **Space:** each node on its own; the region pooled; a short node's reach (neighbours' surplus x e(d) = 1 - 2 d x ration / carry);
  expansion outward from home, settled or carried home.

*Current as of 7 Nov 2026.*
