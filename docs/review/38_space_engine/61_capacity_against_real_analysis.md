# 38.61: The capacity model against how real societies and economies are analysed

Session 37.4, 7 Nov 2026. Zach: "compare the approaches being explored to those used / developed for real societal and economic
analysis to see if there is any insights to be found or flaws / clear holes that become more obvious". The approach compared is
38.60's: levels and the ladder of practice; capital kept apart from ongoing work; embodied work on a production graph; node reach
and expansion; and the proposed complexity measures.

The references are standard works, cited from knowledge, not searched. Each is named so it can be checked.

## 1. Where the approach already matches established practice

| Ours | Real-world counterpart | What the match tells us |
|---|---|---|
| Levels: bare, as it stands, worked, best, ceiling | **Yield gap analysis** in agronomy (van Ittersum et al. 2013): potential yield, attainable yield, actual yield | The same ladder. Agronomy's lesson: attainable is about 75 to 85% of potential, because the last steps cost more than they return. Our "ceiling" is potential, not a target. |
| No single capacity number; it depends on practice | **Cohen, *How Many People Can the Earth Support?* (1995):** human carrying capacity depends on diet, technology, distribution and choices | The levels are the right shape. A single "K" for people is a category error. |
| Intensification as soil breaking and more crops a year | **Boserup, *The Conditions of Agricultural Growth* (1965):** intensification raises output a unit of land but lowers it a unit of work, so it is adopted only under population pressure | The ladder reproduces this. Breaking the soil feeds 64 against 39 but raises work a head from 28 to 39. |
| Capital raising output a unit of work | **Capital deepening** (Solow; and earlier) | Milling lowers work a head (39 to 33) for 460 units once. |
| Embodied work on the production graph | **Leontief's input-output model** (the Leontief inverse gives each good's direct and indirect labour); **Sraffa (1960)**, vertically integrated labour; Koopmans' activity analysis | The graph is an activity-analysis model. The standard tools (the inverse, linear programming) apply directly. |
| Food a unit of work | **EROI**, energy returned on energy invested (Hall et al.); Odum | The analogue, but see hole 6: in the engine, work costs no food. |
| Steady take of wild stocks (best regrowth) | **Maximum sustainable yield** in fisheries and forestry | The match is a warning. MSY is the textbook fragile target (hole 2). |
| Expansion outward with transport cost e(d) | **von Thünen (1826):** land use in rings by distance to market; **Ricardo:** the extensive margin and rent | e(d) is a crude von Thünen. Von Thünen says more (insight C). |
| A ladder of sophistication | **White's law; Morris's Social Development Index** (energy capture a head); **Tainter, *The Collapse of Complex Societies* (1988):** diminishing returns to complexity | The direction is well trodden. Tainter warns against reading more as better (hole 8). |

## 2. Holes that the comparison makes obvious

### Hole 1. Food available is not food reachable: the entitlement problem (the largest)

**Sen, *Poverty and Famines* (1981):** famines happen without a fall in the food available. People starve because they lose their
entitlement: what they can command through what they own, their work and exchange. The Bengal famine of 1943 is his case.

**Our evidence fits exactly:**
- The Wide Country could feed 1.5 times its people, pooled, and 19 of 23 died.
- In the takeover runs the model said food would run short on day 29; the first death was day 16, and the poor died first while the
  hall held 90 to 130 grain (38.59).
- 38.60 measures food availability only. It cannot see a famine of entitlement, which is the kind the runs actually had.

**Fix:** an entitlement layer:
- each household's endowment (land held, stores, beasts, fittings) and the work its members can sell;
- the exchange rates in force (wages, prices, gifts);
- what that household can command as food.
Report capacity by household, and the share of people whose entitlement falls below their need. The engine has every input:
claims, stores, agreements and offers.

### Hole 2. Mean years against bad years: the risk problem

- **Halstead and O'Shea, *Bad Year Economics* (1989):** societies are shaped by the worst years, not the average. They buffer by
  mobility, diversification, storage and exchange.
- **Fisheries:** MSY at the mean collapses stocks under variance (Larkin, "An epitaph for the concept of maximum sustained yield",
  1977). Managers now harvest below it with control rules.

**Ours uses expected yields.** The engine is stochastic: blight (5 to 15%), weather, gales, illness. A world feeding 1.2 times its
people on average starves in a bad year. Our MSY take on game and plants leaves no margin, and the game's threshold regime means a
bad year below 15% of capacity never comes back.

**Fix:** capacity at a percentile. Run the year many times with the engine's own distributions (proposals/process_model.md, part 2,
gives them), and report the people fed in the 10th-percentile year. Harvest wild stocks below MSY (two thirds of it is a common
rule). Count storage, diversification and exchange as buffers, which they are.

### Hole 3. What people choose is not what is possible: the behaviour problem

**Chayanov (*The Theory of Peasant Economy*, 1925):** peasant households work until the drudgery of more work outweighs the need it
meets. They do not maximise output, and they work harder only as the ratio of eaters to workers rises. **Sahlins (*Stone Age
Economics*, 1972):** foragers met their needs with little work and stopped. **Optimal foraging** (Charnov's marginal value theorem):
foragers leave a patch when its return falls below the average.

**The ladder ranks steps by people fed for their cost.** That is a planner's frontier, not a prediction of what a society adopts.
Chayanov and Boserup predict the cheapest configuration in drudgery that feeds the people there: intensification only when needed.

That gives a sharp, testable hypothesis for the sophistication experiment (38.60 §6):
- **Prediction:** each arm settles at the least-work configuration that feeds it, so its realised level rises as capacity falls.
- **Observed so far:** no run intensified at all, however short of food. That would be neither Chayanov nor Boserup but a failure to
  respond. It is a finding about the agents, and worth testing directly.

**Fix:** a second ladder, "least drudgery for the people there". At each population, find the configuration that feeds them with the
least work a head. The two ladders differ exactly where intensification costs work: breaking the soil, and weeding at 16.

### Hole 4. A greedy search where a linear program gives shadow prices

**Activity analysis and linear programming** (Koopmans, Kantorovich, Dantzig) solve "most people fed, given land, labour and fuel"
exactly. Their dual gives each constraint's shadow price: what one more plot, unit of work or unit of fuel is worth in people fed.

**Ours:**
- the ceiling turns parcels to field greedily;
- the allocation of work is greedy;
- neither says which constraint binds, or by how much.

**Fix:** the production graph and the field years are linear once the year is fixed. Solve them as a linear program (scipy, or a
small simplex) and report the shadow prices. Then "fuel binds Wenbridge at 6 people; a unit of woodland is worth N people; a unit of
work is worth M" falls out. That is Liebig's law of the minimum, measured.

### Hole 5. Capital without time: interest, depreciation and the subsistence fund

**Real capital accounting:**
- depreciation (the perpetual inventory method);
- annualised cost by the capital recovery factor (interest × life).

**Böhm-Bawerk and the classical "wage fund":** how long a production process a society can afford depends on its subsistence fund,
the stored food that feeds the builders while the capital is made.

**Ours:**
- capital is once;
- the ranking spreads it over one engine year (an arbitrary choice);
- fittings do not wear in the engine;
- nothing asks whether the society has the stored food to feed 300 units of work on a water wheel, about 50 days of one person's work.

**Fix:**
- report capital's payback (capital ÷ the yearly work it saves or the food it adds);
- add the subsistence-fund test: capital is reachable only if stores (buffer days × people) can feed its building while the food work
  goes on;
- this links capital to the buffer, and explains why poor villages cannot climb. It is the poverty trap in its oldest form.

### Hole 6. Work costs nothing in food in the engine

**In real societies,** the energy of work comes from food. EROI is food energy out against the work's energy in. A day's hard work
raises intake by a third or more.

**In the engine,** the ration is fixed (1 a night, by stage and shelter); work is a budget of units with no food cost. Three
consequences:
- food a unit of work is not an EROI;
- idleness is free;
- "subsistence share" measures only time.

This is an engine idiosyncrasy, and it shapes every labour measure. Whether to give work a food cost is a design decision: it would
make hunger and hard labour trade off, as they do in life.

### Hole 7. Land and natural inputs vanish in embodied work

**Ricardo's rent and Sraffa's treatment of land:** a good's value depends on the scarce natural input at the margin, not on labour
alone. **The ecological footprint and HANPP** (Wackernagel and Rees; Haberl) account in land and in appropriated natural production.

**Ours:**
- counts embodied work only, so a grain grown on scarce land and one grown on plentiful land look alike;
- splits joint products (grain and straw) by quantity, which is arbitrary. Sraffa shows joint production makes embodied labour
  ill-defined.

**Fix:**
- report embodied land-time (plot-days) beside embodied work;
- treat straw, dung and brash as by-products with zero cost;
- or let the linear program price them.
Footprint a head and the share of the land's yearly growth taken (a HANPP analogue) are then direct.

### Hole 8. Complexity measured only as metabolism

**Turchin et al. (2018, PNAS; the Seshat databank)** found one dimension along which 51 measures of social complexity co-vary across
414 past societies. It mixes:
- scale: polity population, territory, the largest settlement;
- hierarchy levels;
- government specialisation;
- infrastructure;
- information: writing, records, texts;
- money.

**Hidalgo and Hausmann (2009):** economic complexity is the diversity of capabilities a society has and their rarity.

**Our measures** (subsistence share, capital depth, roundaboutness, intensity against productivity) are all metabolic. Societies can
be metabolically simple and organisationally complex, and the reverse.

**Fix:** add organisational axes, all readable from the journal:
- distinct roles and trades practised;
- depth of hierarchy (households, heads, offices, agreements of agreements);
- the share of food that changes hands by exchange or obligation;
- written lines and records;
- money in use;
- the size of the largest cooperating group.
Report metabolism and organisation apart. Seshat's finding that they move together is a hypothesis our societies can test, not an
assumption.

### Hole 9. Capacity as a static number, not a population equilibrium

**In ecology,** K is where births and deaths balance. It emerges from vital rates. In history, Malthusian and demographic-structural
cycles (Turchin) arise from population pressing on capacity, with lags.

**Ours:** people supported is the agronomic notion: a fixed population fed. Births are slow against our runs (22 births in 93 runs),
so no run has tested population growing into, or overshooting, its capacity.

**Insight:** "how close a society lives to its capacity, and what happens there" (overshoot, crowding, conflict) needs runs long
enough for births to matter, or a shorter generation. That is a design choice about time, not about capacity.

## 3. Insights the comparison suggests (beyond fixing holes)

- **A. Name the levels as agronomy does:** potential (ceiling), attainable (best within what the world reaches), practised (as it
  stands), actual (measured from the run). The yield gap (attainable − actual) is then a clean, portable measure of what agents leave
  on the table. "Realised reach" becomes the yield gap's complement, with the literature's meaning.
- **B. Two ladders tell you which world you are in.** If agents follow the least-drudgery ladder, they behave like peasants
  (Chayanov). If they follow neither, the gap is agent capability. The gap between the frontier and the least-drudgery ladder is the
  intensification a population must accept to grow.
- **C. Von Thünen predicts the level should fall with distance.** Land near home worked intensively; far land extensive (herds,
  foraging, wood). The expansion model should choose a level a node, by its distance, not one level for all. The rings that result are
  a test: do agent societies arrange land this way?
- **D. The subsistence fund joins capital, stores and leverage.** Whoever has the stored food to feed builders can build the mill, and
  then holds it. This is the mechanism the takeover experiment wanted (38.59), and it is measurable: a household's buffer against the
  capital its next rung needs.
- **E. Risk ranks the buffers.** Under variance, storage, diversity of crops and sources, and exchange between nodes are worth people
  fed, not only waste avoided. The percentile capacity of hole 2 prices them. This is how real subsistence economies are read.

## 4. What stands, in short

- **Sound and established:** the levels as a ladder of practice; intensification against capital deepening; embodied work on a
  production graph; transport-limited reach; no single number.
- **Must fix before the measures are trusted for experiments:**
  - entitlement by household (hole 1);
  - bad-year capacity (hole 2);
  - the least-drudgery ladder (hole 3).
- **Would sharpen:** shadow prices by linear programming (hole 4); payback and the subsistence fund (hole 5); land-time beside
  work-time (hole 7); organisational axes (hole 8).
- **Engine choices this exposed:**
  - work has no food cost (hole 6);
  - fittings do not wear;
  - births too slow for population to meet its capacity within a run (hole 9).
  These are design decisions for Zach, not bugs.

*Current as of 7 Nov 2026.*
