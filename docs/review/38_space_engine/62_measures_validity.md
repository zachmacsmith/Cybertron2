# 38.62: Do the capacity measures make sense, are they valid, and can they test agents?

Session 37.4, 7 Nov 2026. Zach asked four things:
- Does the analysis expose mechanics that make no economic sense?
- Are engine-dependent measures valid for comparisons within an engine?
- Is seeding societies at a complexity level or capacity ratio, and watching them climb or decay, a worthwhile test of ability?
- How could the measures be made more robust?

## 1. Mechanics that do not make economic sense

Proposed changes are in proposals/economic_calibration.md. In order of how much they distort the measures:

1. **Time is compressed for crops but not for regrowth, spoilage or eating.**
   - The year is 32 nights. A grain crop takes 8, beans 5, and resowing is immediate, so a plot gives four or five harvests a year.
   - Wild plants regrow at 0.3 a night, so a meadow yields about twice its standing stock a year.
   - Grain loses 0.5% a night in a house, so storage across an 8-night winter barely matters.
   - The "worked" level's 3 to 4 times over "as it stands" is mostly this.
2. **Processing creates food.** Grain boiled is 0.7 a unit; milled and baked it is 1.3, from 1 grain to 1 flour to 1 bread at 1.3.
   Real milling loses mass; bread and porridge give about the same energy.
3. **Beans dominate.** They are fastest, free to the soil and as productive as grain, so the best rotation is mostly beans.
4. **Work costs no food.** The ration is fixed, so a unit of work has no food cost. Any work that yields anything pays, and an idle unit is pure loss. There is no break-even below which work is not worth doing, and labour measures are time only.
5. **Fittings never wear.** Capital, once built, is free forever. This removes the maintenance problem real societies face.
6. **Births are slow for the runs' length.** 22 births in 93 runs, so no population has met its capacity.

**Plausible as they stand:**
- the 3:1 seed ratio;
- cattle weak per acre (a cow about 24 food a year on half a plot of grass, against about 186 a plot of field at "worked");
- raw grain at 0.2 of a meal;
- carrying 10 on foot;
- buildings that break and are repaired.

## 2. Are within-engine measures valid?

**Yes, for relative comparisons, on four conditions:**
- **One engine version.** Each run records its code; the capacity baseline should be computed by that version and stored in the run
  (economic_calibration.md G).
- **Normalised by the world's own ladder,** not in raw units. For example: the share of the way from bare to attainable reached (log
  scale); the yield gap closed; work share; capital in days of the population's work; buffer in days of need. Dimensionless ratios
  travel across worlds within an engine.
- **Repeated seeds and a null arm.** The same food world gave 55 meals, then 26 (38.55).
- **Not dominated by an exploit.** While item 1 stands, "sophistication" partly measures who discovers rapid recropping or beans.

**The test of validity is simple:** a measure is valid within the engine if changing an engine detail that should not matter (the
compression factor, a plot's size) leaves it unchanged. That is a check we can run with the capacity model alone, before any agent
run.

## 3. Is seeding societies at a level or ratio a worthwhile test of ability?

**Yes, if three things are controlled. It then tests what matters for AI societies:**
- noticing scarcity;
- choosing to invest;
- coordinating work and capital;
- distributing;
- keeping up what they hold.

**The controls:**
1. **Information.** Agents must know how farming works as well as they know the menu (38.57 lesson 15: menus decide). Otherwise "no
   intensification" may mean "never told". Give every arm the same plain account of the techniques. The test then measures choice and
   coordination, not discovery.
2. **Time.** At least one full year (32 days or more) with a winter, so capital can pay back and a bad season can bite.
3. **The engine's exploits removed or held fixed** (section 1).

**Two complementary designs:**
- **Climbing.** Start low (land below "as it stands"; nothing built) and watch whether they climb, how far, and in what order. Compare
  the order with the two ladders: the frontier ("most fed for cost") and least drudgery (38.61 hole 3).
- **Keeping.** Start high (fields broken, a mill, a granary, stores) on land that needs that level, and watch whether they maintain it
  or fall back. This needs fittings to wear (section 1, item 5). It is less contingent on discovery, and it tests institutions and
  upkeep, which matter more for agent societies than invention.

**What to measure:**
- the realised rung;
- the yield gap closed;
- work share;
- capital built and kept, in work-days;
- deaths and births a person-year;
- the share fed by their own entitlement (38.61 hole 1).
Each is against the null arm and over seeds.

**What would make it too contingent:**
- one seed;
- runs shorter than a year;
- worlds where one exploit decides;
- comparing raw numbers across engine versions.

## 4. Making the measures robust

1. **One time scale** (economic_calibration.md A). Every rate per year in the data; the engine converts. The compression becomes one
   dial and the measures stop depending on it.
2. **Calibrate to stylised facts that set incentives** (B to F): one main harvest per crop, pulses below cereals, processing that
   saves work but makes no food, work that costs food, capital that wears.
3. **Invariance checks.** The capacity model, run on the same world at different compression factors and plot sizes, should give the
   same dimensionless measures. If it does not, the measure is an artefact.
4. **The baseline in the run** (G): capacity, ladder and buffer at day 0, computed by the run's engine.
5. **Percentiles, not means** (38.61 hole 2): capacity in a bad year, from the engine's own distributions.
6. **Equal information** across arms about how the world works.
7. **Report metabolic and organisational measures apart** (38.61 hole 8). Neither stands for "complexity" alone.

*Current as of 7 Nov 2026.*
