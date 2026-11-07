# 38.60: Carrying capacity: the model, the worlds, and every past run against its land

Session 37.4, 7 Nov 2026. Built at Zach's request after the takeover runs starved (38.59). D4-102; the rules are in
spec/measurement/capacity.md, the record in proposals/carrying_capacity.md, and the engine side in proposals/process_model.md.
Figures and per-world reports are in `60_capacity/`.

## 1. What it measures

**The question is a ratio:** the food the land gives each year, eaten, against the food the people need each year. Stores are a buffer,
reported apart. The model also gives:
- the days to the first harvest the people bring in;
- any standing crop the frost takes first;
- for a run, the day food first runs short.

Five levels, each a bundle of practice and technology, each lowered to what the world can reach:

| Level | Practice | Grain worth | Kept in |
|---|---|---|---|
| bare | wild food only, raw | (none) | the open |
| as it stands | one grain crop a year, unbroken, unweeded | 0.7 boiled | a house |
| worked | the best sequence of crops and rest; broken, weeded, manured | 1.0 as meal | bins |
| best | plough, full weeding, master farmers, seed selection, rye over winter | 1.3 as bread | a granary |
| ceiling | best, and meadow, pasture, scrub and woods turned to field while the woods still keep the hearths | 1.3 | a granary |

**Fuel** is its own need, in three levels: dead wood; adding young growth; adding trees felled at their growth.

**Every rule is the engine's own.** The model calls the engine's functions and the world's calendar:
- 14 rules (regrowth, spoilage, sowing yield, frost, soil and others) were moved out of the night's code into pure functions.
  Nothing changed: 353 tests pass before and after.
- The agreement tests run the engine on a real world. One caught the model's first mistake: the engine takes wild food by day and
  regrows it at night, so the steady stock is the one after a night's regrowth.

## 2. What the levels cost (Wenbridge, at the people each level feeds)

| Level | Fed | Food a plot a year | Food a unit of work | Work a head a year | Capital a head, with materials |
|---|---|---|---|---|---|
| bare | 1.3 | (none) | 0.23 | 181 | (none) |
| as it stands | 5.5 | 16 | 0.93 | 36 | 12 |
| worked | 42 | 186 | 1.09 | 30 | 9 |
| best | 76 | 340 | 1.45 | 22 | 12 |
| ceiling | 135 | 357 | 1.55 | 21 | 11 |

**Food a plot rises 20-fold from "as it stands" to "best".** The extra comes from more crops a year (grain takes 8 days in a
32-day year with 24 days free of frost), broken soil (4.5 times the seed, against 3), weeding (up to +50%), and milling and baking
(grain worth 1.3 against 0.7).

**Food a unit of work does not fall as the land is worked harder; it rises a little.** Measured on the production graph, the work in a
grain of grain:
- 0.52 units, as it stands;
- 0.72 when worked (more labour a plot);
- 0.52 at best (the plough, copper tools and the mill take the labour back).

So the engine has both intensification (more work a plot) and capital deepening (tools and mills raise output a unit of work).

**The Wenbridge "best" level here** has no plough (no oxen) and no copper tools (no ore). Its gain is from field practice and
milling alone.

**Sensitivity at "worked" (figure: takeover/sensitivity.svg):**
- eating raw instead of cooking cuts the people fed from 42 to 7;
- one crop a year instead of the best sequence cuts it to 15;
- not breaking the soil cuts it to 26;
- seed selection and a master farmer add about a quarter each;
- storage hardly matters at this level (39 to 43);
- tools change nothing here: they make work faster, and work is not what binds (food takes 16% of the people's work at "worked").

**A caution.** "Worked" and "best" assume people sow again as soon as they reap, every crop of the year. That is allowed by the
engine but untested in any run: no run has seen it, and no scripted bot has played it through. Each piece agrees with the engine;
the whole year has not been run. Before relying on the upper levels, run a scripted farm at "worked" (section 6).

## 3. Every past run against its land

**Coverage:**
- 93 of 103 runs were analysed, from the world each started from.
- 10 M1 runs are left out: their world files have no nodes; the M1 engine predates the graph of places.
- The 93 runs held 1,389 starting people; 140 died, 115 of hunger; 22 were born.

`retro.png` plots each run's worst-fed village ("as it stands" ratio) against the share of its people who died of hunger.

**Findings:**
1. **Every famine came from a village that could not feed its own as it stands, or from a long run.** The famines (a quarter or more
   dead of hunger), with the worst village's ratio:
   - w3 region: 0.04;
   - r1 region: 0.05;
   - wb2 Wenbridge: 0.20;
   - takeover and Orwell: 0.31;
   - Wide Country: 0.57 over 72 days;
   - Combe c2: 0.95 over 79 days (2 of 3 people).
   No run where every village fed its own as it stands starved in 40 days or less.
2. **A low ratio is not enough on its own. Run length against the buffer decides.** Nine runs had a village under 0.5 and no famine:
   - most were short: the valleys and v3 at 17 to 19 days, wb1 at 14, wb3 at 9;
   - some had wide land to roam: the wild band b1 (its region at 4.3) and the frontier (its region at 1.8);
   - in Hollins, the villages were designed to trade.
   The famines began once the stores ran out and the first own harvest had not covered the gap.
3. **The region's ratio hides the famine; the worst village shows it.** The Wide Country could feed 1.53 times its people as it stood,
   pooled, yet 19 of 23 died of hunger. Its worst village, Wynford, stood at 0.57, and food had to be carried a day. Hollins and the
   regions are the same pattern.
4. **The aggregate horizon is close; the deaths come earlier.**
   - Takeover and Orwell: the model says food runs short on day 29 at "as it stands"; the first death was day 16 and most fell
     between days 20 and 31.
   - r1: the model says day 35; 17 had died by day 23.
   The gap is distribution. The model pools a village's food; the runs did not (the poor die first, 38.59).
5. **No run reached "worked", and every world could have fed its people at that level.**
   - Every world's "worked" ratio is 2 to 19 times its people. The exceptions are villages with no fields: the frontier, Coppergate,
     Millford and Ashwood, which depend on others by design.
   - Agents farmed at or below "as it stands": a crop a year, sown thin, often unbroken. The takeover Hearnes sowed 0.3 of a plot at a
     time in spring.
   So these famines are failures of practice, timing and distribution, not of land. If the upper levels hold (section 2's caution),
   the engine's land is generous and the gap is in what agents do.
6. **Births are few whatever the land: 22 in 93 runs.** Births are bounded by the life mechanics (pregnancy length against run length),
   not by capacity. No run tested a population growing into its capacity.
7. **Fuel binds by flow almost everywhere, but not within a run.** The valley, hamlet and region worlds burn their woods' yearly
   growth 10 to 50 times over (fuel ratios 0.02 to 0.08). Their standing woods hold 1.5 to 4 years of the people's need, so no run
   was long enough for fuel to bite. Wenbridge's own woods keep 6 of its 12 people warm; Holm Wood, a day off, holds the rest.

## 4. Other needs that should become their own modules

Food and fuel are built. In order of what the engine already has:
1. **Shelter.** Being housed changes the food a person needs: unsheltered ×1.5, and in the cold up to ×2 (PHYSICS shelter). Shelter
   then depends on beds, rooms, upkeep (building breaks) and timber. A people without houses has a lower food capacity on the same land.
2. **Beasts' feed.** Grass a plot (25), hay for the winter. Herds are now taken as they are; they should be capped by grazing and hay,
   and grazing lost to clearing should be counted.
3. **Seed.** A stock that must be kept back. It is in the run horizon; as a need it ties this year's harvest to next year's.
4. **Care.** Units a day for infants and children (D2-142). It is labour taken from food work, and grows with births.
5. **Labour as the joint limit.** Food, fuel, shelter, care and upkeep share each person's 5 to 7 units a day. A "work budget" module
   would report the share each need takes. scenario_design.md's lesson is that food should take 30% or less.
6. **Not in the engine, so not needed yet:** water, clothing, health beyond illness.

## 5. Over several nodes

Three views are built:
- **each node alone;**
- **the region pooled;**
- **a short node's reach.** Each neighbour's surplus counts at e(d) = 1 − 2d × ration / carry, the carrier's meals both ways.

**Expansion** (`frontier.svg`) takes land outward from home in road days. Two curves:
- **settled:** people move to the land;
- **carried home:** everyone stays and the food comes home, worth e(d).

Each step carries its capital: houses, fittings and stores for the people it adds.

**Next:**
- carrying as a process in the production graph (proposals/process_model.md, mechanism 6), so transport costs work as well as meals;
- households as units of distribution, which finding 4 shows is where runs actually die.

## 6. Proposed experiment (Zach, 7 Nov: "put them in environments of different carrying capacities ... what sophistications they can support, if they tend toward a natural sophistication level")

Not run; for Zach's decision.

**Design:**
- One society: about 12 people, Opus at the poles, Sonnet in the middle, Haiku in the bulk.
- One land, scaled to four "as it stands" ratios: 0.5, 1, 2 and 4. Field sizes and wild stocks are scaled; the techniques reachable
  are the same in every arm.
- A null arm at 4 with stores for the whole run (no pressure).
- 2 seeds each; 40 days, so a winter falls inside.

**Read:**
- The level each arm actually reaches. Place the food it produced a plot and a unit of work against the level table: this is the
  "realised level".
- Practices adopted: crops a year, ground broken, weeding, mills and stores built.
- The share of work on food.
- Deaths and births.
- Whether the realised level settles at the lowest one that feeds them (necessity drives intensification) or stays at "as it stands"
  however short they are (no intensification under pressure). The runs so far point to the second.

**Before it:**
- A scripted bot farming at "worked" for a year, to check that level holds in the engine (section 2's caution). Bots only, no cost.

**Cost:** about 9 arms (with seeds) × 40 days × about $1 a day ≈ $360.

## 7. Limits

- **Distribution** within a node is not modelled. Capacity is the land's, not a household's.
- **The ceiling** ignores grazing lost to clearing and the work of ditching and terracing.
- **Wild drawdown** (overharvesting standing stocks) enters a run only through the stores and standing crops.
- **Old runs are read with today's engine.** Most of their worlds build; numbers for runs before D4-38 (the plot of 16 seed) may
  differ from their own engine's.
- **The M1 runs** cannot be read.

*Current as of 7 Nov 2026.*
